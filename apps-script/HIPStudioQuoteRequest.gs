/* HIPStudio quote-request backend for Google Apps Script.
 * Deploy as a Web App after review. Do not commit deployment URLs or secrets.
 * Public contact / Reply-To: info@hipstudio.hu
 * Internal recipients: nemeth.timea@hipstudio.hu, banhalmi.norbert@hipstudio.hu
 */

const HIPSTUDIO = Object.freeze({
  CENTRAL_EMAIL: 'info@hipstudio.hu',
  INTERNAL_RECIPIENTS: [
    'nemeth.timea@hipstudio.hu',
    'banhalmi.norbert@hipstudio.hu'
  ],
  SHEET_NAME: 'Ajánlatkérések',
  PAYLOAD_VERSION: 'hipstudio-quote-v1',
  MAX_PAYLOAD_BYTES: 80000,
  MAX_SUBMISSIONS_PER_EMAIL_10_MIN: 5,
  RESPONSE_HOURS: 24
});

const HEADERS = [
  'request_id','received_at','response_due_at','status','owner','owner_suggestion',
  'route','queue','priority','complexity_score','completeness_score','next_action','routing_flags','routing_version',
  'language','name','company','email','phone','preferred_contact',
  'pillars','services','goals','project_summary','desired_outcome','must_have',
  'deadline','preferred_date_1','preferred_date_2','preferred_date_3','date_flexibility',
  'location_type','location_details','reference_url','page_url',
  'business_company_size','business_entities','business_payroll_headcount','business_monthly_invoices',
  'business_countries','business_engagement','business_current_systems','business_process_scope','business_reporting_need',
  'creative_people_count','creative_final_assets','creative_locations_count','creative_languages','creative_addons',
  'creative_channels','creative_usage_rights','creative_brand_requirements',
  'photo_outfits_setups','photo_retouched_images','photo_event_guests','photo_parallel_tracks','photo_property_spaces','photo_area_sqm','photo_print_quantity','photo_key_people_moments','photo_aerial_requirements',
  'video_final_length','video_shoot_days','video_speakers','video_script_status','stream_platform','stream_viewers','video_audio_music','video_deliverables',
  'podcast_speakers','podcast_episodes','podcast_episode_length','podcast_distribution','repurposing_outputs',
  'experience_participants','experience_duration','experience_languages','experience_environment','experience_travel','experience_team_profile','experience_objective','experience_constraints','experience_branding','experience_logistics',
  'raw_json'
];

function doGet() {
  return json_({ok:true, service:'HIPStudio quote request', version:HIPSTUDIO.PAYLOAD_VERSION, routingVersion:typeof HIPSTUDIO_ROUTING_VERSION==='undefined'?'missing':HIPSTUDIO_ROUTING_VERSION});
}

function doPost(e) {
  try {
    const raw = String(e && e.postData && e.postData.contents || '');
    if (!raw || raw.length > HIPSTUDIO.MAX_PAYLOAD_BYTES) return json_({ok:false,error:'invalid_payload'});
    const incoming = JSON.parse(raw);
    if (clean_(incoming.website, 200)) return json_({ok:true});

    const p = normalize_(incoming);
    validate_(p);
    rateLimit_(p.email);

    const now = new Date();
    const requestId = requestId_(now);
    const responseDue = new Date(now.getTime() + HIPSTUDIO.RESPONSE_HOURS * 60 * 60 * 1000);
    const triage = triage_(p, now);
    const record = Object.assign({}, p, triage, {
      request_id: requestId,
      received_at: now.toISOString(),
      response_due_at: responseDue.toISOString(),
      status: 'NEW',
      owner: '',
      raw_json: JSON.stringify(Object.assign({},p,{triage:triage}))
    });

    appendRecord_(record);
    sendInternal_(record);
    sendConfirmation_(record);
    return json_({ok:true, requestId:requestId});
  } catch (err) {
    console.error('HIPStudio quote error', safeError_(err));
    return json_({ok:false,error:'submission_failed'});
  }
}

function setup() {
  if (typeof runRoutingSelfTest === 'function') runRoutingSelfTest();
  const props = PropertiesService.getScriptProperties();
  let id = props.getProperty('SHEET_ID');
  let ss;
  if (id) ss = SpreadsheetApp.openById(id);
  else {
    ss = SpreadsheetApp.create('HIPStudio - Ajánlatkérések');
    id = ss.getId();
    props.setProperty('SHEET_ID', id);
  }
  ensureSheet_(ss);
  console.log('SHEET_ID=' + id);
  console.log('Spreadsheet=' + ss.getUrl());
  console.log('Sender alias available=' + senderOptions_().aliasAvailable);
  return {sheetId:id, sheetUrl:ss.getUrl(), senderAliasAvailable:senderOptions_().aliasAvailable, routingVersion:HIPSTUDIO_ROUTING_VERSION};
}

function normalize_(src) {
  const out = {};
  HEADERS.forEach(function(key){ if (key !== 'raw_json') out[key] = ''; });
  Object.keys(src || {}).forEach(function(key){
    if (!/^[a-z0-9_]+$/i.test(key)) return;
    const value = src[key];
    if (Array.isArray(value)) out[key] = value.slice(0,50).map(function(v){return clean_(v,1000);}).join(', ');
    else out[key] = clean_(value, key === 'project_summary' || key === 'desired_outcome' || key === 'must_have' ? 8000 : 4000);
  });
  out.language = ['hu','en','de'].indexOf(out.language) >= 0 ? out.language : 'hu';
  out.email = out.email.toLowerCase();
  out.payload_version = clean_(src.payload_version,100);
  return out;
}

function validate_(p) {
  if (p.payload_version && p.payload_version !== HIPSTUDIO.PAYLOAD_VERSION) throw new Error('payload_version');
  if (!p.name || !p.company || !p.email || !p.project_summary) throw new Error('required_fields');
  if (!p.pillars || !p.services) throw new Error('scope_required');
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(p.email)) throw new Error('invalid_email');
  if (String(p.privacy_acknowledged).toLowerCase() !== 'on' && String(p.privacy_acknowledged).toLowerCase() !== 'true') throw new Error('privacy_required');
  if (p.reference_url && !/^https?:\/\//i.test(p.reference_url)) throw new Error('reference_url');
  if (p.page_url && p.page_url.length > 2000) throw new Error('page_url');
}

function rateLimit_(email) {
  const digest = Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_256, email, Utilities.Charset.UTF_8);
  const key = 'q:' + Utilities.base64EncodeWebSafe(digest).slice(0,32);
  const cache = CacheService.getScriptCache();
  const count = Number(cache.get(key) || 0) + 1;
  if (count > HIPSTUDIO.MAX_SUBMISSIONS_PER_EMAIL_10_MIN) throw new Error('rate_limit');
  cache.put(key, String(count), 600);
}

function appendRecord_(record) {
  const id = PropertiesService.getScriptProperties().getProperty('SHEET_ID');
  if (!id) throw new Error('SHEET_ID_not_configured_run_setup');
  const lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    const sh = ensureSheet_(SpreadsheetApp.openById(id));
    sh.appendRow(HEADERS.map(function(h){ return record[h] == null ? '' : record[h]; }));
  } finally { lock.releaseLock(); }
}

function ensureSheet_(ss) {
  let sh = ss.getSheetByName(HIPSTUDIO.SHEET_NAME);
  if (!sh) sh = ss.insertSheet(HIPSTUDIO.SHEET_NAME);
  if (sh.getLastRow() === 0) {
    ensureColumns_(sh, HEADERS.length);
    sh.getRange(1,1,1,HEADERS.length).setValues([HEADERS]);
    sh.setFrozenRows(1);
    return sh;
  }

  const oldHeaders = sh.getRange(1,1,1,sh.getLastColumn()).getValues()[0].map(function(v){return String(v||'').trim();});
  while (oldHeaders.length && !oldHeaders[oldHeaders.length-1]) oldHeaders.pop();
  if (oldHeaders.join('|') !== HEADERS.join('|')) migrateSheetSchema_(sh, oldHeaders);
  return sh;
}

function migrateSheetSchema_(sh, oldHeaders) {
  if (!oldHeaders.length) throw new Error('sheet_headers_missing');
  const seen = {};
  oldHeaders.forEach(function(h){
    if (!h) throw new Error('sheet_blank_header');
    if (seen[h]) throw new Error('sheet_duplicate_header:' + h);
    if (HEADERS.indexOf(h) < 0) throw new Error('sheet_unknown_header:' + h);
    seen[h] = true;
  });

  const values = sh.getRange(1,1,sh.getLastRow(),oldHeaders.length).getValues();
  const index = {};
  oldHeaders.forEach(function(h,i){index[h]=i;});
  const migrated = values.slice(1).map(function(row){
    return HEADERS.map(function(h){ return index[h] == null ? '' : row[index[h]]; });
  });

  ensureColumns_(sh, HEADERS.length);
  sh.clearContents();
  sh.getRange(1,1,1,HEADERS.length).setValues([HEADERS]);
  if (migrated.length) sh.getRange(2,1,migrated.length,HEADERS.length).setValues(migrated);
  sh.setFrozenRows(1);
  console.log('Migrated quote Sheet schema from ' + oldHeaders.length + ' to ' + HEADERS.length + ' columns; preserved rows=' + migrated.length);
}

function ensureColumns_(sh, required) {
  const current = sh.getMaxColumns();
  if (current < required) sh.insertColumnsAfter(current, required-current);
}

const CUSTOMER_FIELDS = [
  'name','company','email','phone','preferred_contact','pillars','services','goals','project_summary','desired_outcome','must_have',
  'deadline','preferred_date_1','preferred_date_2','preferred_date_3','date_flexibility','location_type','location_details','reference_url',
  'business_company_size','business_entities','business_payroll_headcount','business_monthly_invoices','business_countries','business_engagement','business_current_systems','business_process_scope','business_reporting_need',
  'creative_people_count','creative_final_assets','creative_locations_count','creative_languages','creative_addons','creative_channels','creative_usage_rights','creative_brand_requirements',
  'photo_outfits_setups','photo_retouched_images','photo_event_guests','photo_parallel_tracks','photo_property_spaces','photo_area_sqm','photo_print_quantity','photo_key_people_moments','photo_aerial_requirements',
  'video_final_length','video_shoot_days','video_speakers','video_script_status','stream_platform','stream_viewers','video_audio_music','video_deliverables',
  'podcast_speakers','podcast_episodes','podcast_episode_length','podcast_distribution','repurposing_outputs',
  'experience_participants','experience_duration','experience_languages','experience_environment','experience_travel','experience_team_profile','experience_objective','experience_constraints','experience_branding','experience_logistics'
];

function customerLabels_(lang) {
  const common = {
    hu:{name:'Név',company:'Cég / szervezet',email:'E-mail',phone:'Telefon',preferred_contact:'Preferált kapcsolattartás',pillars:'Terület',services:'Szolgáltatás',goals:'Cél',project_summary:'Projekt / kiinduló helyzet',desired_outcome:'Elvárt eredmény',must_have:'Kötelező elem',deadline:'Határidő',preferred_date_1:'Első választott időpont',preferred_date_2:'Második választott időpont',preferred_date_3:'Harmadik választott időpont',date_flexibility:'Időpont rugalmassága',location_type:'Helyszíntípus',location_details:'Helyszín részletei',reference_url:'Referencia / brief'},
    en:{name:'Name',company:'Company / organisation',email:'Email',phone:'Phone',preferred_contact:'Preferred contact method',pillars:'Area',services:'Service',goals:'Goal',project_summary:'Project / starting point',desired_outcome:'Desired outcome',must_have:'Must-have',deadline:'Deadline',preferred_date_1:'First preferred date',preferred_date_2:'Second preferred date',preferred_date_3:'Third preferred date',date_flexibility:'Date flexibility',location_type:'Location type',location_details:'Location details',reference_url:'Reference / brief'},
    de:{name:'Name',company:'Unternehmen / Organisation',email:'E-Mail',phone:'Telefon',preferred_contact:'Bevorzugter Kontaktweg',pillars:'Bereich',services:'Leistung',goals:'Ziel',project_summary:'Projekt / Ausgangslage',desired_outcome:'Gewünschtes Ergebnis',must_have:'Pflichtanforderung',deadline:'Frist',preferred_date_1:'Erster Wunschtermin',preferred_date_2:'Zweiter Wunschtermin',preferred_date_3:'Dritter Wunschtermin',date_flexibility:'Terminflexibilität',location_type:'Ortstyp',location_details:'Ortsangaben',reference_url:'Referenz / Briefing'}
  }[lang];
  const out = {};
  CUSTOMER_FIELDS.forEach(function(k){ out[k] = common[k] || k.replace(/_/g,' '); });
  return out;
}

function customerSubmittedRows_(r, lang) {
  const labels = customerLabels_(lang);
  return CUSTOMER_FIELDS.filter(function(k){ return r[k] !== '' && r[k] != null; }).map(function(k){ return [labels[k], r[k]]; });
}

function sendInternal_(r) {
  const copy = {
    hu:{subject:'Új HIPStudio ajánlatkérés',title:'Új HIPStudio ajánlatkérés',id:'Azonosító',due:'Válasz-határidő',details:'Beküldött adatok',triage:'Belső triage — emberi felülvizsgálattal',note:'A triage csak munkaszervezési javaslat. Nem jelent automatikus elfogadást, árat vagy szerződéses döntést.',reply:'Az ügyfélnek a központi HIPStudio címről válaszolj.'},
    en:{subject:'New HIPStudio quote request',title:'New HIPStudio quote request',id:'Request ID',due:'Response due',details:'Submitted information',triage:'Internal triage — human review required',note:'Triage is only an operational suggestion. It is not an automatic acceptance, price or contractual decision.',reply:'Reply to the customer from the central HIPStudio address.'},
    de:{subject:'Neue HIPStudio Angebotsanfrage',title:'Neue HIPStudio Angebotsanfrage',id:'Anfrage-ID',due:'Antwortfrist',details:'Übermittelte Angaben',triage:'Interne Zuordnung — menschliche Prüfung erforderlich',note:'Die Zuordnung ist nur ein organisatorischer Vorschlag. Sie ist keine automatische Annahme, Preisfestlegung oder vertragliche Entscheidung.',reply:'Antworten Sie dem Kunden über die zentrale HIPStudio-Adresse.'}
  }[r.language];
  const subject = '[' + r.priority + '][' + r.queue + '][' + r.request_id + '] ' + copy.subject + ' — ' + (r.company || r.name);
  const html = '<div style="font-family:Arial,sans-serif;line-height:1.5;color:#111">' +
    '<h1>' + h_(copy.title) + '</h1>' +
    '<p><strong>' + h_(copy.id) + ':</strong> ' + h_(r.request_id) + '<br><strong>' + h_(copy.due) + ':</strong> ' + h_(formatDate_(r.response_due_at)) + '</p>' +
    section_(copy.details, customerSubmittedRows_(r, r.language)) +
    section_(copy.triage, [['Queue',r.queue],['Priority',r.priority],['Complexity',r.complexity_score+'/10'],['Brief completeness',r.completeness_score+'%'],['Next action',r.next_action],['Routing flags',r.routing_flags],['Owner suggestion',r.owner_suggestion],['Routing version',r.routing_version]]) +
    '<hr><p><strong>' + h_(copy.note) + '</strong></p><p>' + h_(copy.reply) + ' <a href="mailto:' + h_(HIPSTUDIO.CENTRAL_EMAIL) + '">' + h_(HIPSTUDIO.CENTRAL_EMAIL) + '</a></p></div>';
  sendMail_(HIPSTUDIO.INTERNAL_RECIPIENTS.join(','), subject, stripHtml_(html), html, HIPSTUDIO.CENTRAL_EMAIL);
}

function sendConfirmation_(r) {
  const copy = {
    hu:{subject:'HIPStudio — megérkezett az ajánlatkérésed',hello:'Köszönjük, megérkezett az ajánlatkérésed.',promise:'Hamarosan felvesszük veled a kapcsolatot.',id:'Ajánlatkérés azonosítója',details:'Az általad beküldött adatok'},
    en:{subject:'HIPStudio — your quote request has arrived',hello:'Thank you, we received your quote request.',promise:'We will contact you shortly.',id:'Request ID',details:'The information you submitted'},
    de:{subject:'HIPStudio — Ihre Angebotsanfrage ist eingegangen',hello:'Vielen Dank, Ihre Angebotsanfrage ist bei uns eingegangen.',promise:'Wir melden uns in Kürze bei Ihnen.',id:'Anfrage-ID',details:'Ihre übermittelten Angaben'}
  }[r.language] || null;
  if (!copy) throw new Error('confirmation_language');
  const html = '<div style="font-family:Arial,sans-serif;line-height:1.5;color:#111">' +
    '<h1>' + h_(copy.hello) + '</h1>' +
    '<p>' + h_(copy.promise) + '</p>' +
    '<p><strong>' + h_(copy.id) + ':</strong> ' + h_(r.request_id) + '</p>' +
    section_(copy.details, customerSubmittedRows_(r, r.language)) +
    '<p style="margin-top:24px">HIPStudio<br><a href="mailto:' + h_(HIPSTUDIO.CENTRAL_EMAIL) + '">' + h_(HIPSTUDIO.CENTRAL_EMAIL) + '</a></p></div>';
  sendMail_(r.email, copy.subject + ' — ' + r.request_id, stripHtml_(html), html, HIPSTUDIO.CENTRAL_EMAIL);
}

function sendMail_(to, subject, plain, html, replyTo) {
  const sender = senderOptions_();
  const options = {htmlBody:html, name:'HIPStudio', replyTo:replyTo};
  if (sender.aliasAvailable) options.from = HIPSTUDIO.CENTRAL_EMAIL;
  GmailApp.sendEmail(to, subject, plain, options);
}

function senderOptions_() {
  let aliases = [];
  try { aliases = GmailApp.getAliases() || []; } catch (e) {}
  return {aliasAvailable:aliases.indexOf(HIPSTUDIO.CENTRAL_EMAIL) >= 0};
}

function section_(title, rows) {
  rows = (rows || []).filter(function(x){return x[1] !== '' && x[1] != null;});
  if (!rows.length) return '';
  return '<h2 style="margin-top:24px">' + h_(title) + '</h2><table cellpadding="6" cellspacing="0" border="0" style="border-collapse:collapse;width:100%">' + rows.map(function(row){return '<tr><td style="vertical-align:top;width:220px;border-bottom:1px solid #ddd"><strong>'+h_(row[0])+'</strong></td><td style="vertical-align:top;border-bottom:1px solid #ddd">'+linkify_(row[1])+'</td></tr>';}).join('') + '</table>';
}

function pickRows_(r, keys) { return keys.filter(function(k){return r[k];}).map(function(k){return [k.replace(/_/g,' '),r[k]];}); }
function requestId_(d) { return 'HIP-' + Utilities.formatDate(d, Session.getScriptTimeZone() || 'Europe/Budapest', 'yyyyMMdd-HHmmss') + '-' + Utilities.getUuid().slice(0,6).toUpperCase(); }
function formatDate_(iso) { try { return Utilities.formatDate(new Date(iso), Session.getScriptTimeZone() || 'Europe/Budapest', 'yyyy-MM-dd HH:mm'); } catch(e){ return iso; } }
function clean_(v,max) { return String(v == null ? '' : v).replace(/[\u0000-\u0008\u000B\u000C\u000E-\u001F]/g,'').trim().slice(0,max || 4000); }
function compact_(v,max) { v=clean_(v,max||100); return v || 'n/a'; }
function h_(v) { return String(v == null ? '' : v).replace(/[&<>"']/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];}); }
function linkify_(v) { const s=h_(v); return /^https?:\/\//i.test(String(v||'')) ? '<a href="'+s+'">'+s+'</a>' : s.replace(/\n/g,'<br>'); }
function stripHtml_(s) { return String(s).replace(/<br\s*\/?\s*>/gi,'\n').replace(/<\/p>/gi,'\n').replace(/<\/h[1-6]>/gi,'\n').replace(/<[^>]+>/g,'').replace(/&nbsp;/g,' ').replace(/&amp;/g,'&').replace(/&lt;/g,'<').replace(/&gt;/g,'>').replace(/&#39;/g,"'").replace(/&quot;/g,'"'); }
function safeError_(err) { return String(err && err.message || err || 'error').slice(0,300); }
function json_(obj) { return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON); }
