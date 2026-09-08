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
    sh.getRange(1,1,1,HEADERS.length).setValues([HEADERS]);
    sh.setFrozenRows(1);
  } else {
    const current = sh.getRange(1,1,1,Math.max(sh.getLastColumn(),HEADERS.length)).getValues()[0].slice(0,HEADERS.length);
    if (current.join('|') !== HEADERS.join('|')) throw new Error('sheet_header_mismatch');
  }
  return sh;
}

function sendInternal_(r) {
  const subject = '[' + r.priority + '][' + r.queue + '][' + r.request_id + '] ' + (r.company || r.name);
  const html = '<div style="font-family:Arial,sans-serif;line-height:1.5;color:#111">' +
    '<h1>Új HIPStudio ajánlatkérés</h1>' +
    '<p><strong>Azonosító:</strong> ' + h_(r.request_id) + '<br><strong>24 órás válasz-határidő:</strong> ' + h_(formatDate_(r.response_due_at)) + '</p>' +
    section_('Automatikus triage — emberi felülvizsgálattal', [
      ['Queue',r.queue],['Prioritás',r.priority],['Komplexitás',r.complexity_score+'/10'],['Brief teljessége',r.completeness_score+'%'],['Következő lépés',r.next_action],['Routing flag-ek',r.routing_flags],['Owner',r.owner_suggestion],['Routing verzió',r.routing_version]
    ]) +
    section_('Kapcsolat', [['Név',r.name],['Cég',r.company],['E-mail',r.email],['Telefon',r.phone],['Preferált kapcsolat',r.preferred_contact]]) +
    section_('Projekt', [['Terület',r.pillars],['Szolgáltatás',r.services],['Cél',r.goals],['Kiinduló helyzet',r.project_summary],['Sikeres eredmény',r.desired_outcome],['Must-have',r.must_have]]) +
    section_('Időzítés és helyszín', [['Határidő',r.deadline],['Időpontok',[r.preferred_date_1,r.preferred_date_2,r.preferred_date_3].filter(Boolean).join(', ')],['Rugalmasság',r.date_flexibility],['Helyszíntípus',r.location_type],['Helyszín',r.location_details],['Referencia / brief',r.reference_url]]) +
    section_('Business scope', pickRows_(r,['business_company_size','business_entities','business_payroll_headcount','business_monthly_invoices','business_countries','business_engagement','business_current_systems','business_process_scope','business_reporting_need'])) +
    section_('HIPStudio scope', pickRows_(r,['creative_people_count','creative_final_assets','creative_locations_count','creative_languages','creative_addons','creative_channels','creative_usage_rights','creative_brand_requirements','photo_outfits_setups','photo_retouched_images','photo_event_guests','photo_parallel_tracks','photo_property_spaces','photo_area_sqm','photo_print_quantity','photo_key_people_moments','photo_aerial_requirements','video_final_length','video_shoot_days','video_speakers','video_script_status','stream_platform','stream_viewers','video_audio_music','video_deliverables','podcast_speakers','podcast_episodes','podcast_episode_length','podcast_distribution','repurposing_outputs'])) +
    section_('Flúgos scope', pickRows_(r,['experience_participants','experience_duration','experience_languages','experience_environment','experience_travel','experience_team_profile','experience_objective','experience_constraints','experience_branding','experience_logistics'])) +
    '<hr><p><strong>A triage csak munkaszervezési javaslat.</strong> Nem jelent automatikus elfogadást, árat vagy szerződéses döntést.</p><p>Válaszolj az ügyfélnek az <a href="mailto:' + h_(HIPSTUDIO.CENTRAL_EMAIL) + '">' + h_(HIPSTUDIO.CENTRAL_EMAIL) + '</a> központi cím használatával.</p></div>';
  sendMail_(HIPSTUDIO.INTERNAL_RECIPIENTS.join(','), subject, stripHtml_(html), html, HIPSTUDIO.CENTRAL_EMAIL);
}

function sendConfirmation_(r) {
  const copy = {
    hu:{subject:'HIPStudio — megkaptuk az ajánlatkérésedet',hello:'Köszönjük az ajánlatkérést.',promise:'Az egyedi ajánlatot 24 órán belül összeállítjuk.',id:'Ajánlatkérés azonosítója'},
    en:{subject:'HIPStudio — we received your quote request',hello:'Thank you for your quote request.',promise:'We prepare your tailored quote within 24 hours.',id:'Request ID'},
    de:{subject:'HIPStudio — Ihre Anfrage ist eingegangen',hello:'Vielen Dank für Ihre Anfrage.',promise:'Wir erstellen Ihr individuelles Angebot innerhalb von 24 Stunden.',id:'Anfrage-ID'}
  }[r.language];
  const html = '<div style="font-family:Arial,sans-serif;line-height:1.5;color:#111"><h1>' + h_(copy.hello) + '</h1><p>' + h_(copy.promise) + '</p><p><strong>' + h_(copy.id) + ':</strong> ' + h_(r.request_id) + '</p><p>HIPStudio<br><a href="mailto:' + h_(HIPSTUDIO.CENTRAL_EMAIL) + '">' + h_(HIPSTUDIO.CENTRAL_EMAIL) + '</a></p></div>';
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
