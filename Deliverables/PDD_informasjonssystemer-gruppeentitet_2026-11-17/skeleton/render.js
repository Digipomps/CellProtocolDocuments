// Renders the G1-GUI images for PDD informasjonssystemer-gruppeentitet with the real CellScaffold
// web renderer (Public/js/skeleton-runtime.js, porthole-webo.css, admin-skeleton.css).
// Three surfaces: the owners' group surface, «Gi rolle», and the member's «Min rolle».
// Every keypath under group.* and myRole.* is a proposal; none exists in CellScaffold today.
// Usage: node render.js <cellscaffold> <out-images> <out-skeleton>
const fs = require('node:fs');
const path = require('node:path');
const { chromium } = require('playwright');
const [scaffold, outImages, outSkeleton] = process.argv.slice(2);
const pub = path.join(scaffold, 'Public');

const ink = '#172033', muted = '#556273', teal = '#0F766E', red = '#B91C1C', amber = '#92400E';
const text = (t, o = {}) => ({ Text: { text: t, modifiers: { foregroundColor: ink, ...o } } });
const key = (k, o = {}) => ({ Text: { keypath: k, modifiers: { foregroundColor: ink, ...o } } });
const when = (keypath, equals) => ({ visibility: { when: { equals, keypath, scope: 'root' } } });
const card = (elements, extra = {}) => ({ VStack: { spacing: 10, elements, modifiers: {
  padding: 16, background: '#FFFFFF', cornerRadius: 12, borderWidth: 1, borderColor: '#E2E8F0', maxWidthInfinity: true, ...extra } } });
const secondary = { background: '#FFFFFF', borderColor: '#CBD5E1', borderWidth: 1, cornerRadius: 6, foregroundColor: '#334155' };
const danger = { background: '#FFFFFF', borderColor: '#FCA5A5', borderWidth: 1, cornerRadius: 6, foregroundColor: red };
const list = (keypath, rowElements) => ({ List: { elements: [], keypath, selectionMode: 'none', modifiers: { itemSpacing: 8 },
  flowElementSkeleton: { VStack: { spacing: 2, elements: rowElements } } } });
const row = (l, r, ro = {}) => ({ HStack: { spacing: 8, elements: [key(l, { fontWeight: '700' }), { Spacer: {} }, key(r, { fontSize: 13, foregroundColor: teal, ...ro })] } });
const picker = (label, k, sel, ph) => ({ VStack: { spacing: 4, elements: [ text(label, { fontSize: 13, foregroundColor: muted }),
  { Picker: { keypath: k, optionLabelKeypath: 'label', selectionStateKeypath: sel, selectionValueKeypath: 'id', selectionPayloadMode: 'item_id', placeholder: ph } } ] } });
const field = (label, src, tgt, ph) => ({ VStack: { spacing: 4, elements: [ text(label, { fontSize: 13, foregroundColor: muted }),
  { TextField: { sourceKeypath: src, targetKeypath: tgt, placeholder: ph } } ] } });

// ---------- 1. Gruppeflaten (eiere) ----------
const group = { VStack: { spacing: 14, elements: [
  card([
    text('Informasjonssystemer (Ifi, UiO)', { fontStyle: 'title2', fontWeight: '700' }),
    text('Forskningsgruppe ved Institutt for informatikk. Gruppa er ikke UiO og har ikke organisasjonsnummer.', { fontSize: 14, foregroundColor: muted }),
    key('group.state.keyNote', { fontSize: 13, foregroundColor: amber }),
  ]),
  card([
    text('Venter på godkjenning', { fontStyle: 'headline', foregroundColor: amber }),
    list('group.state.proposals', [
      key('title', { fontWeight: '700' }),
      key('summary', { fontSize: 14 }),
      key('rule', { fontSize: 13, foregroundColor: muted }),
      { HStack: { spacing: 8, modifiers: { wrap: true }, elements: [
        { Button: { keypath: 'group.proposal.approve', label: 'Godkjenn med passkey', payload: {} } },
        { Button: { keypath: 'group.proposal.reject', label: 'Avvis', payload: {}, modifiers: danger } },
      ] } },
    ]),
  ], { ...when('group.state.hasProposals', true), borderColor: '#FCD34D' }),
  card([
    { HStack: { spacing: 8, elements: [ text('Eiere', { fontStyle: 'headline' }), { Spacer: {} }, key('group.state.policyLabel', { fontSize: 13, foregroundColor: muted }) ] } },
    list('group.state.owners', [ row('name', 'since') ]),
    { Button: { keypath: 'group.owner.propose', label: 'Foreslå ny eier', payload: {}, modifiers: secondary } },
  ]),
  card([
    text('Eierskapsavtale', { fontStyle: 'headline' }),
    list('group.state.agreement', [ row('action', 'requires', { foregroundColor: ink }) ]),
    picker('Bytt til en annen avtale', 'group.state.agreementTemplates', 'group.state.selectedTemplate', 'Velg mal'),
    { Button: { keypath: 'group.agreement.propose', label: 'Foreslå endring', payload: {}, modifiers: secondary } },
    text('En endring blir en ny policyversjon og må godkjennes etter regelen for styring.', { fontSize: 12, foregroundColor: muted }),
  ]),
  card([
    { HStack: { spacing: 8, elements: [ text('Utstedte roller', { fontStyle: 'headline' }), { Spacer: {} }, key('group.state.rolesCount', { fontSize: 13, foregroundColor: muted }) ] } },
    list('group.state.roles', [
      row('holder', 'status'),
      { HStack: { spacing: 8, elements: [ key('detail', { fontSize: 13, foregroundColor: muted }), { Spacer: {} },
        { Button: { keypath: 'group.role.revoke', label: 'Trekk tilbake', payload: {}, modifiers: { ...danger, visibility: { when: { equals: true, keypath: 'revocable', scope: 'item' } }, fontSize: 13 } } } ] } },
    ]),
    { Button: { keypath: 'group.role.new', label: 'Gi rolle', payload: {} } },
  ]),
  card([
    text('Journal', { fontStyle: 'headline' }),
    list('group.state.journal', [ { HStack: { spacing: 8, elements: [ key('when', { fontSize: 13, foregroundColor: muted }), key('what', { fontSize: 13 }) ] } } ]),
  ]),
] } };

const templates = [
  { id: 'roles-one-governance-all', label: 'Roller: én eier · Styring: alle eiere' },
  { id: 'all-two', label: 'Alt krever to eiere' },
  { id: 'one-alone', label: 'Én eier alene for alt' },
  { id: 'two-of-three', label: 'To av tre eiere for alt' },
];
const agreement = [
  { action: 'Gi eller trekke rolle', requires: 'én eier' },
  { action: 'Legge til eller fjerne eier', requires: 'alle eiere' },
  { action: 'Endre eierskapsavtalen', requires: 'alle eiere' },
];
const groupStates = {
  'gruppe-forslag': { group: { state: {
    keyNote: 'Testnøkkel på staging: gruppenøkkelen ligger i programvare i hvelvet til KMS finnes.',
    hasProposals: true,
    proposals: [ { title: 'Legg til Petter Nielsen som eier (policy v2)',
      summary: 'Hvelvet har laget dette sammendraget fra forslaget: Petter Nielsen (identitet …7c41) får rollen eier fra i dag. Policy v1 → v2.',
      rule: 'Regel «styring» krever alle eiere. I v1 er det bare deg. Utløper 25.11.2026.' } ],
    policyLabel: 'Policy v1 · siden 18.11.2026',
    owners: [ { name: 'Kjetil', since: 'eier siden 18.11' } ],
    agreement, agreementTemplates: templates, selectedTemplate: 'roles-one-governance-all',
    rolesCount: '1 aktiv',
    roles: [ { holder: 'Sara Nilsen', status: 'aktiv', detail: 'researcher · MasterHAVEN26 · gyldig til 30.06.2027 · gitt av Kjetil', revocable: true } ],
    journal: [
      { when: '18.11 20:10', what: 'Gruppa opprettet med policy v1 (Kjetil eneste eier)' },
      { when: '18.11 20:14', what: 'Rolle researcher gitt til Sara Nilsen, godkjent av Kjetil' },
      { when: '18.11 20:20', what: 'Forslag: Petter Nielsen som eier' },
    ],
  } } },
  'gruppe-eier-fylt': { group: { state: {
    keyNote: 'Testnøkkel på staging: gruppenøkkelen ligger i programvare i hvelvet til KMS finnes.',
    hasProposals: false, proposals: [],
    policyLabel: 'Policy v2 · siden 19.11.2026',
    owners: [ { name: 'Kjetil', since: 'eier siden 18.11' }, { name: 'Petter Nielsen', since: 'eier siden 19.11' } ],
    agreement, agreementTemplates: templates, selectedTemplate: 'roles-one-governance-all',
    rolesCount: '3 aktive, 1 trukket',
    roles: [
      { holder: 'Sara Nilsen', status: 'aktiv', detail: 'researcher · MasterHAVEN26 · gyldig til 30.06.2027 · gitt av Kjetil', revocable: true },
      { holder: 'Sara Nilsen', status: 'aktiv', detail: 'student · MasterHAVEN26 · gyldig til 30.06.2027 · gitt av Kjetil', revocable: true },
      { holder: 'Ola Student', status: 'aktiv', detail: 'student · MasterHAVEN26 · gyldig til 30.06.2027 · gitt av Petter', revocable: true },
      { holder: 'Testkonto 3', status: 'trukket 19.11', detail: 'student · MasterHAVEN26 · trukket av Petter', revocable: false },
    ],
    journal: [
      { when: '19.11 08:02', what: 'Policy v2: Petter Nielsen eier, godkjent av Kjetil' },
      { when: '19.11 09:15', what: 'Rolle student gitt til Ola Student, godkjent av Petter' },
      { when: '19.11 09:40', what: 'Rolle student trukket for Testkonto 3, godkjent av Petter' },
    ],
  } } },
};

// ---------- 2. Gi rolle ----------
const giveRole = { VStack: { spacing: 14, elements: [
  card([
    text('Gi rolle i Informasjonssystemer', { fontStyle: 'title2', fontWeight: '700' }),
    field('Mottaker (invitasjonskode eller HAVEN-identitet)', 'group.state.newRole.recipient', 'group.newRole.recipient.set', 'f.eks. K7QX-2M'),
    key('group.state.newRole.recipientResolved', { fontSize: 13, foregroundColor: teal }),
    picker('Rolle', 'group.state.newRole.roles', 'group.state.newRole.selectedRole', 'Velg rolle'),
    picker('Kull', 'group.state.newRole.cohorts', 'group.state.newRole.selectedCohort', 'Velg kull'),
    field('Gyldig til', 'group.state.newRole.validUntil', 'group.newRole.validUntil.set', 'dd.mm.åååå'),
  ]),
  card([
    text('Dette signerer gruppa', { fontStyle: 'headline' }),
    key('group.state.newRole.preview', { fontSize: 14 }),
    key('group.state.newRole.rule', { fontSize: 13, foregroundColor: muted }),
    { HStack: { spacing: 8, modifiers: { wrap: true }, elements: [
      { Button: { keypath: 'group.newRole.submit', label: 'Godkjenn og gi rolle', payload: {} } },
      { Button: { keypath: 'group.newRole.cancel', label: 'Avbryt', payload: {}, modifiers: secondary } },
    ] } },
  ]),
] } };
const giveRoleStates = {
  'gi-rolle': { group: { state: { newRole: {
    recipient: 'K7QX-2M', recipientResolved: 'Ola Student (identitet …19ae), har akseptert invitasjonen',
    roles: [ { id: 'student', label: 'Student' }, { id: 'researcher', label: 'Forsker (researcher)' }, { id: 'supervisor', label: 'Veileder (supervisor)' } ],
    selectedRole: 'student',
    cohorts: [ { id: 'MasterHAVEN26', label: 'MasterHAVEN26' } ], selectedCohort: 'MasterHAVEN26',
    validUntil: '30.06.2027',
    preview: 'Informasjonssystemer bekrefter at Ola Student er student i kullet MasterHAVEN26, gyldig til 30.06.2027. Beviset kan trekkes tilbake.',
    rule: 'Regel «roller»: én eier er nok. Du godkjenner med passkey, og hvelvet signerer.',
  } } } },
};

// ---------- 3. Min rolle (medlem) ----------
const myRole = { VStack: { spacing: 14, elements: [
  card([
    text('Mine roller', { fontStyle: 'title2', fontWeight: '700' }),
    text('Roller er bevis som andre celler kan sjekke. De gir ingen tilgang til dataene dine.', { fontSize: 14, foregroundColor: muted }),
  ]),
  card([
    list('myRole.state.roles', [
      row('title', 'status'),
      key('issuer', { fontSize: 13, foregroundColor: muted }),
      key('validity', { fontSize: 13, foregroundColor: muted }),
      key('usedBy', { fontSize: 13 }),
    ]),
  ]),
  card([
    text('Rollen er trukket tilbake', { fontStyle: 'headline', foregroundColor: red }),
    key('myRole.state.revokedNote', { fontSize: 14 }),
  ], { ...when('myRole.state.hasRevoked', true), borderColor: '#FCA5A5' }),
] } };
const myRoleStates = {
  'min-rolle-gyldig': { myRole: { state: { hasRevoked: false, roles: [
    { title: 'Forsker i Informasjonssystemer', status: 'gyldig', issuer: 'Utstedt av Informasjonssystemer (Ifi, UiO), godkjent av Kjetil',
      validity: 'Kull MasterHAVEN26 · gyldig til 30.06.2027', usedBy: 'Brukes av: Mitt forskningsdashbord' },
    { title: 'Student i Informasjonssystemer', status: 'gyldig', issuer: 'Utstedt av Informasjonssystemer (Ifi, UiO), godkjent av Kjetil',
      validity: 'Kull MasterHAVEN26 · gyldig til 30.06.2027', usedBy: 'Brukes av: Språkmodell med dagsgrense' },
  ] } } },
  'min-rolle-trukket': { myRole: { state: { hasRevoked: true,
    revokedNote: 'Informasjonssystemer trakk studentrollen 19.11.2026. Celler som krevde den, slipper deg ikke inn lenger. Spør en av eierne hvis dette er feil.',
    roles: [ { title: 'Student i Informasjonssystemer', status: 'trukket 19.11', issuer: 'Utstedt av Informasjonssystemer (Ifi, UiO), trukket av Petter Nielsen',
      validity: 'Kull MasterHAVEN26 · var gyldig til 30.06.2027', usedBy: 'Var brukt av: Språkmodell med dagsgrense' } ] } } },
};

const surfaces = [
  ['gruppe', group, groupStates, ['Informasjonssystemer (Ifi, UiO)', 'Eierskapsavtale', 'Testnøkkel']],
  ['gi-rolle', giveRole, giveRoleStates, ['Dette signerer gruppa', 'MasterHAVEN26']],
  ['min-rolle', myRole, myRoleStates, ['Mine roller']],
];

async function shot(width, name, skeleton, state, mustContain) {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width, height: 900 }, deviceScaleFactor: 2 });
  await page.route('**/*', async (route) => {
    const p = new URL(route.request().url()).pathname;
    const files = { '/js/skeleton-runtime.js': [path.join(pub, 'js/skeleton-runtime.js'), 'application/javascript'],
      '/css/porthole-webo.css': [path.join(pub, 'css/porthole-webo.css'), 'text/css'],
      '/css/admin-skeleton.css': [path.join(pub, 'css/admin-skeleton.css'), 'text/css'] };
    if (p === '/') return route.fulfill({ contentType: 'text/html', body: '<!doctype html><html lang="no"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="stylesheet" href="/css/porthole-webo.css"><link rel="stylesheet" href="/css/admin-skeleton.css"><style>body{margin:0;background:#f4f7fb;font-family:system-ui,sans-serif}#root{max-width:820px;margin:0 auto;padding:16px}</style></head><body><main id="root" class="canvas view-mode"></main><script src="/js/skeleton-runtime.js"></script></body></html>' });
    if (files[p]) return route.fulfill({ path: files[p][0], contentType: files[p][1] });
    return route.abort();
  });
  const errors = [];
  page.on('pageerror', (e) => errors.push(String(e)));
  await page.goto('http://group.test/');
  await page.waitForFunction(() => Boolean(window.HavenSkeletonRuntime?.createRenderer));
  await page.evaluate(([sk, st]) => {
    const root = document.getElementById('root');
    const r = window.HavenSkeletonRuntime.createRenderer({ rootElement: root, skeleton: sk, layoutContext: { availableWidth: root.clientWidth } });
    r.update(st);
  }, [skeleton, state]);
  await page.waitForTimeout(300);
  if (errors.length) throw new Error(`${name}: ${errors.join('; ')}`);
  const t = await page.locator('#root').innerText();
  for (const m of mustContain) if (!t.includes(m)) throw new Error(`${name}: missing «${m}»`);
  await page.locator('#root').screenshot({ path: path.join(outImages, name) });
  await browser.close();
  return t;
}

(async () => {
  fs.mkdirSync(outSkeleton, { recursive: true });
  fs.mkdirSync(outImages, { recursive: true });
  const checks = {
    'gruppe-forslag': ['Venter på godkjenning', 'Godkjenn med passkey', 'Policy v1'],
    'gruppe-eier-fylt': ['Petter Nielsen', 'Policy v2', 'trukket 19.11'],
    'gi-rolle': ['Godkjenn og gi rolle', 'én eier er nok'],
    'min-rolle-gyldig': ['Forsker i Informasjonssystemer', 'gyldig til 30.06.2027'],
    'min-rolle-trukket': ['Rollen er trukket tilbake'],
  };
  const notIn = { 'gruppe-eier-fylt': ['Venter på godkjenning'], 'min-rolle-gyldig': ['Rollen er trukket tilbake'] };
  for (const [slug, skeleton, states, base] of surfaces) {
    fs.writeFileSync(path.join(outSkeleton, `${slug}.v1.json`), JSON.stringify(skeleton, null, 2) + '\n');
    fs.writeFileSync(path.join(outSkeleton, `${slug}-tilstander.v1.json`), JSON.stringify(states, null, 2) + '\n');
    for (const [w, dev] of [[1280, 'laptop'], [390, 'iphone']])
      for (const [name, st] of Object.entries(states)) {
        const t = await shot(w, `${name}-${dev}-v1.png`, skeleton, st, [...base, ...(checks[name] || [])]);
        for (const m of notIn[name] || []) if (t.includes(m)) throw new Error(`${name}-${dev}: «${m}» should be hidden`);
      }
  }
  console.log('ok');
})().catch((e) => { console.error(e); process.exit(1); });
