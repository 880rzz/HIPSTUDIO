/* Deterministic HIPStudio lead triage.
 * No price calculation, automatic acceptance/rejection or personal owner assignment.
 * The result is an operational suggestion for human review.
 */

const HIPSTUDIO_ROUTING_VERSION = 'quote-routing-v1';

function triage_(p, now) {
  now = now instanceof Date ? now : new Date();
  const pillars = list_(p.pillars);
  const services = list_(p.services);
  const addons = list_(p.creative_addons);
  const flags = [];
  let complexity = 0;

  let queue = 'MANUAL_REVIEW';
  if (pillars.length > 1) {
    queue = 'CROSS_PILLAR';
    complexity += 2;
    flags.push('MULTI_PILLAR_COORDINATION');
  } else if (pillars[0] === 'business') queue = 'BUSINESS';
  else if (pillars[0] === 'creative') queue = 'CREATIVE';
  else if (pillars[0] === 'experiences') queue = 'EXPERIENCE';

  if (services.length >= 3) complexity += 1;

  if (pillars.indexOf('business') >= 0) {
    if (num_(p.business_entities) >= 2) complexity += 1;
    if (num_(p.business_payroll_headcount) >= 50) complexity += 1;
    if (num_(p.business_monthly_invoices) >= 200) complexity += 1;
    if (multi_(p.business_countries)) {
      complexity += 1;
      flags.push('CROSS_BORDER_REVIEW');
    }
    if (['ongoing','both'].indexOf(String(p.business_engagement || '')) >= 0) complexity += 1;
    if (services.indexOf('ai-automation') >= 0) flags.push('PROCESS_DISCOVERY_REQUIRED');
  }

  if (pillars.indexOf('creative') >= 0) {
    if (num_(p.creative_people_count) >= 10) complexity += 1;
    if (num_(p.creative_locations_count) >= 2) complexity += 1;
    if (multi_(p.creative_languages)) complexity += 1;
    if (addons.indexOf('mobile-studio') >= 0) complexity += 1;
    if (addons.indexOf('instant-retouch') >= 0) complexity += 1;
    if (addons.indexOf('printing') >= 0) complexity += 1;
    if (addons.indexOf('express') >= 0) {
      complexity += 2;
      flags.push('EXPRESS_DELIVERY');
    }
    if (num_(p.photo_event_guests) >= 100) complexity += 1;
    if (num_(p.photo_parallel_tracks) >= 2) complexity += 1;
    if (num_(p.video_shoot_days) >= 2) complexity += 1;
    if (num_(p.stream_viewers) >= 200) complexity += 1;
    if (num_(p.podcast_episodes) >= 4) complexity += 1;
    if (services.indexOf('photo-aerial') >= 0 || cleanListText_(p.photo_aerial_requirements)) flags.push('AERIAL_FEASIBILITY_REVIEW');
    if (services.indexOf('streaming') >= 0) flags.push('STREAMING_TECHNICAL_REVIEW');
    if (cleanListText_(p.creative_usage_rights)) flags.push('USAGE_RIGHTS_REVIEW');
  }

  if (pillars.indexOf('experiences') >= 0) {
    if (num_(p.experience_participants) >= 50) complexity += 1;
    if (multi_(p.experience_languages)) complexity += 1;
    if (cleanListText_(p.experience_travel)) complexity += 1;
    if (cleanListText_(p.experience_constraints)) flags.push('ACCESS_AND_CONSTRAINTS_REVIEW');
    if (cleanListText_(p.experience_branding)) complexity += 1;
  }

  const urgency = urgency_(p, now);
  if (urgency.flag) flags.push(urgency.flag);

  let priority = 'NORMAL';
  if (urgency.days !== null && urgency.days <= 3) priority = 'URGENT';
  else if (addons.indexOf('express') >= 0) priority = 'URGENT';
  else if (complexity >= 5 || pillars.length > 1) priority = 'HIGH';

  const completeness = completeness_(p);
  let nextAction = 'HUMAN_SCOPE_REVIEW';
  if (completeness < 65) nextAction = 'REQUEST_MISSING_SCOPE_INFORMATION';
  else if (flags.indexOf('AERIAL_FEASIBILITY_REVIEW') >= 0 || flags.indexOf('STREAMING_TECHNICAL_REVIEW') >= 0) nextAction = 'TECHNICAL_FEASIBILITY_REVIEW';
  else if (queue === 'CROSS_PILLAR') nextAction = 'ASSIGN_CROSS_PILLAR_LEAD';

  return {
    routing_version: HIPSTUDIO_ROUTING_VERSION,
    route: queue,
    queue: queue,
    priority: priority,
    complexity_score: Math.min(complexity, 10),
    completeness_score: completeness,
    owner_suggestion: 'MANUAL_ASSIGNMENT',
    next_action: nextAction,
    routing_flags: unique_(flags).join(', ')
  };
}

function urgency_(p, now) {
  const candidates = [p.deadline,p.preferred_date_1,p.preferred_date_2,p.preferred_date_3]
    .map(function(v){ return parseDate_(v); })
    .filter(Boolean)
    .sort(function(a,b){ return a.getTime()-b.getTime(); });
  if (!candidates.length) return {days:null,flag:''};
  const days = Math.ceil((candidates[0].getTime()-now.getTime())/(24*60*60*1000));
  if (days <= 3) return {days:days,flag:'NEAR_TERM_DEADLINE'};
  if (days <= 7) return {days:days,flag:'SHORT_LEAD_TIME'};
  return {days:days,flag:''};
}

function completeness_(p) {
  const core = ['name','company','email','pillars','services','project_summary'];
  const useful = ['desired_outcome','must_have','deadline','preferred_date_1','location_type','location_details','reference_url'];
  let score = 0;
  core.forEach(function(k){ if (cleanListText_(p[k])) score += 11; });
  useful.forEach(function(k){ if (cleanListText_(p[k])) score += 5; });
  return Math.min(score,100);
}

function list_(v) {
  return String(v == null ? '' : v).split(',').map(function(x){return x.trim();}).filter(Boolean);
}
function num_(v) { const n=Number(v); return Number.isFinite(n) ? n : 0; }
function multi_(v) { return String(v || '').split(/[,;|/]+/).map(function(x){return x.trim();}).filter(Boolean).length > 1; }
function cleanListText_(v) { return String(v == null ? '' : v).trim(); }
function parseDate_(v) { if(!v)return null; const d=new Date(String(v)+'T12:00:00'); return isNaN(d.getTime())?null:d; }
function unique_(xs) { return xs.filter(function(v,i,a){return a.indexOf(v)===i;}); }

function runRoutingSelfTest() {
  const now = new Date('2026-09-08T10:00:00Z');
  const basic = triage_({pillars:'creative',services:'photo-business-portrait',name:'A',company:'B',email:'a@b.hu',project_summary:'Executive portrait'},now);
  if (basic.queue !== 'CREATIVE' || basic.priority !== 'NORMAL') throw new Error('basic_routing');
  const cross = triage_({pillars:'business, creative',services:'ai-automation, content-engine',name:'A',company:'B',email:'a@b.hu',project_summary:'Cross-pillar',deadline:'2026-09-10'},now);
  if (cross.queue !== 'CROSS_PILLAR' || cross.priority !== 'URGENT') throw new Error('cross_routing');
  const event = triage_({pillars:'creative',services:'photo-event, streaming',creative_addons:'express',photo_event_guests:'450',photo_parallel_tracks:'3',name:'A',company:'B',email:'a@b.hu',project_summary:'Conference'},now);
  if (event.priority !== 'URGENT' || event.routing_flags.indexOf('STREAMING_TECHNICAL_REVIEW') < 0) throw new Error('event_routing');
  return true;
}
