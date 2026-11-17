// Renders the G1-GUI images for PDD forskningsdata-verktoy with the real CellScaffold
// web renderer (Public/js/skeleton-runtime.js, porthole-webo.css, admin-skeleton.css).
// Three surfaces: the student's research dashboard, the entity's request card, and the
// student's request builder. Every keypath under research.*, researchRequest.* and
// researchInbox.* is a proposal; none exists in CellScaffold today.
// Today's chart drops points without a number (skeleton-runtime.js:3504-3523), so a
// suppressed bucket is shown as a line under the chart. WP6 draws it in the chart itself.
// Usage: node render.js <cellscaffold> <out-images> <out-skeleton>
const fs = require('node:fs');
const path = require('node:path');
const { chromium } = require('playwright');
const [scaffold, outImages, outSkeleton] = process.argv.slice(2);
const pub = path.join(scaffold, 'Public');

const ink = '#172033', muted = '#556273', teal = '#0F766E', red = '#B91C1C';
const text = (t, o = {}) => ({ Text: { text: t, modifiers: { foregroundColor: ink, ...o } } });
const key = (k, o = {}) => ({ Text: { keypath: k, modifiers: { foregroundColor: ink, ...o } } });
const when = (keypath, equals) => ({ visibility: { when: { equals, keypath, scope: 'root' } } });
const card = (elements, extra = {}) => ({ VStack: { spacing: 10, elements, modifiers: {
  padding: 16, background: '#FFFFFF', cornerRadius: 12, borderWidth: 1, borderColor: '#E2E8F0', maxWidthInfinity: true, ...extra } } });
const secondary = { background: '#FFFFFF', borderColor: '#CBD5E1', borderWidth: 1, cornerRadius: 6, foregroundColor: '#334155' };
const list = (keypath, rowElements) => ({ List: { elements: [], keypath, selectionMode: 'none', modifiers: { itemSpacing: 8 },
  flowElementSkeleton: { VStack: { spacing: 2, elements: rowElements } } } });

// ---------- 1. Mitt forskningsdashbord ----------
const tile = (i) => ({ VStack: { spacing: 4, elements: [
  key(`research.state.tiles.${i}.label`, { fontSize: 13, foregroundColor: muted }),
  key(`research.state.tiles.${i}.value`, { fontSize: 26, fontWeight: '700' }),
  key(`research.state.tiles.${i}.provenance`, { fontSize: 12, foregroundColor: muted }),
], modifiers: { padding: 14, background: '#F8FAFC', cornerRadius: 10, borderWidth: 1, borderColor: '#E2E8F0', minWidth: 160 } } });

const dashboard = { VStack: { spacing: 14, elements: [
  card([
    text('Mitt forskningsdashbord', { fontStyle: 'title2', fontWeight: '700' }),
    key('research.state.subtitle', { fontSize: 14, foregroundColor: muted }),
  ]),
  card([
    text('Du har ikke forskertilgang ennå', { fontStyle: 'headline' }),
    text('Forskertilgang er en avtale med noden. Den gir deg samletall uten navn eller id-er, og lar deg sende forespørsler til medstudenter. Du ser vilkårene før du sier ja.', { fontSize: 14, foregroundColor: muted }),
    { Button: { keypath: 'research.role.request', label: 'Be om forskertilgang', payload: {} } },
  ], when('research.state.hasRole', false)),
  { VStack: { spacing: 14, modifiers: when('research.state.hasRole', true), elements: [
    { HStack: { spacing: 10, modifiers: { wrap: true }, elements: [tile(0), tile(1), tile(2)] } },
    card([
      key('research.state.chart.title', { fontStyle: 'headline' }),
      { Visualization: { kind: 'chart', keypath: 'research.state.chart.spec' } },
      key('research.state.chart.suppressedNote', { fontSize: 13, foregroundColor: red }),
      key('research.state.chart.provenance', { fontSize: 12, foregroundColor: muted }),
    ]),
    card([
      text('Mine forespørsler', { fontStyle: 'headline' }),
      list('research.state.requests', [
        { HStack: { spacing: 8, elements: [ key('title', { fontWeight: '700' }), { Spacer: {} }, key('status', { fontSize: 13, foregroundColor: teal }) ] } },
        key('detail', { fontSize: 13, foregroundColor: muted }),
      ]),
      { HStack: { spacing: 8, modifiers: { wrap: true }, elements: [
        { Button: { keypath: 'researchRequest.new', label: 'Ny forespørsel', payload: {} } },
        { Button: { keypath: 'research.export.csv', label: 'Last ned CSV med manifest', payload: {}, modifiers: secondary } },
      ] } },
    ]),
    card([
      text('Opphav', { fontStyle: 'headline' }),
      list('research.state.provenance', [
        { HStack: { spacing: 8, elements: [ key('label', { fontSize: 13, foregroundColor: muted }), { Spacer: {} }, key('value', { fontSize: 13 }) ] } },
      ]),
    ]),
  ] } },
] } };

const dashboardStates = {
  'dashbord-fylt': { research: { state: {
    hasRole: true,
    subtitle: 'Samletall fra noden staging.haven.digipomps.org. Ingen navn, ingen id-er. Tall under 5 vises ikke.',
    tiles: [
      { label: 'Identiteter med egne celler', value: '38', provenance: 'Uke 46 · k=5 · mal identities.total v1' },
      { label: 'Har en delt samtale', value: '21', provenance: 'Uke 46 · k=5 · mal adoption.chat v1' },
      { label: 'Har et dokument', value: 'færre enn 5', provenance: 'Uke 46 · k=5 · skjult' },
    ],
    chart: { title: 'Nye identiteter per uke', spec: { chartType: 'bar', points: [
      { label: 'Uke 42', value: 6 }, { label: 'Uke 43', value: 9 }, { label: 'Uke 45', value: 12 }, { label: 'Uke 46', value: 7 } ] },
      suppressedNote: 'Uke 44 er skjult: færre enn 5.',
      provenance: 'Kilde: AdminResolverStats via ResearchAggregateCell · faste kalenderuker · hentet 17.11 09:40' },
    requests: [
      { title: 'Meldinger per uke i «HAVEN Master 2026»', status: '6 av 9 har sagt ja', detail: 'Samlet svar · til 15.12 · svaret vises når minst 5 har sagt ja' },
      { title: 'Tid fra invitasjon til første melding', status: 'Utkast', detail: 'Ikke sendt' },
    ],
    provenance: [
      { label: 'Node', value: 'staging · bygg 57ce8c0' }, { label: 'Minste gruppe (k)', value: '5' },
      { label: 'Utleveringer i dag', value: '3' }, { label: 'Manifest-hash', value: 'sha256:4b1e…9c07' } ],
  } } },
  'dashbord-uten-rolle': { research: { state: { hasRole: false,
    subtitle: 'Her ser du samletall fra noden og svar på forespørslene dine når du har forskertilgang.',
    tiles: [], chart: {}, requests: [], provenance: [] } } },
};

// ---------- 2. Forespørselskortet entiteten ser ----------
const row = (label, k) => ({ VStack: { spacing: 2, elements: [ text(label, { fontSize: 12, foregroundColor: muted }), key(k, { fontSize: 14 }) ] } });
const inbox = { VStack: { spacing: 14, elements: [
  card([
    text('Forskningsforespørsler', { fontStyle: 'title2', fontWeight: '700' }),
    text('Bare du ser dette. Ingen data deles før du sier ja, og du kan trekke deg når som helst.', { fontSize: 14, foregroundColor: muted }),
  ]),
  card([
    key('researchInbox.state.card.who', { fontStyle: 'headline' }),
    key('researchInbox.state.card.purpose', { fontSize: 14 }),
    row('Hva det gjelder', 'researchInbox.state.card.what'),
    row('Hvem som ser hva', 'researchInbox.state.card.recipients'),
    row('Periode og lagring', 'researchInbox.state.card.duration'),
    row('Hvis du trekker deg', 'researchInbox.state.card.withdraw'),
    { HStack: { spacing: 8, modifiers: { wrap: true, ...when('researchInbox.state.card.status', 'ny') }, elements: [
      { Button: { keypath: 'researchInbox.decide', label: 'Ja', payload: { decision: 'yes' } } },
      { Button: { keypath: 'researchInbox.decide', label: 'Ikke nå', payload: { decision: 'notNow' }, modifiers: secondary } },
      { Button: { keypath: 'researchInbox.decide', label: 'Aldri', payload: { decision: 'never' }, modifiers: secondary } },
    ] } },
    { VStack: { spacing: 8, modifiers: when('researchInbox.state.card.status', 'godtatt'), elements: [
      key('researchInbox.state.card.receipt', { fontSize: 13, foregroundColor: teal }),
      { Button: { keypath: 'researchInbox.withdraw', label: 'Trekk samtykket', payload: {},
        modifiers: { background: '#FFFFFF', borderColor: '#FCA5A5', borderWidth: 1, cornerRadius: 6, foregroundColor: red } } },
    ] } },
  ]),
] } };
const cardBase = {
  who: 'Sara Nilsen, masterstudent ved UiO, spør deg',
  purpose: 'Formål: «Undersøke hvor aktivt studentgrupper bruker en delt samtale gjennom et semester.»',
  what: 'Antall meldinger du har sendt per uke i gruppen «HAVEN Master 2026». Tallet regnes ut hos deg.',
  recipients: 'Tallet ditt legges sammen med de andres av HAVEN-noden. Sara ser bare summen, og bare når minst 5 har sagt ja. Hun ser ikke ditt tall eller navnet ditt.',
  duration: 'Fra i dag til 15.12.2026. Summene lagres i oppgaven til 30.06.2027.',
  withdraw: 'Nye utregninger tar deg ikke med. Summer som alt er regnet ut, blir stående.',
};
const inboxStates = {
  'kort-ny': { researchInbox: { state: { card: { ...cardBase, status: 'ny', receipt: '' } } } },
  'kort-godtatt': { researchInbox: { state: { card: { ...cardBase, status: 'godtatt',
    receipt: 'Du sa ja 17.11 kl. 09.52. Kontrakten varer til 15.12.2026. Kvittering: sha256:a83f…11d2' } } } },
};

// ---------- 3. Lag forespørsel (studenten) ----------
const builder = { VStack: { spacing: 14, elements: [
  card([
    text('Ny forespørsel', { fontStyle: 'title2', fontWeight: '700' }),
    { Picker: { label: 'Hva vil du spørre om', keypath: 'researchRequest.state.templates', optionLabelKeypath: 'label',
      selectionStateKeypath: 'researchRequest.state.selectedTemplate', selectionValueKeypath: 'id', selectionPayloadMode: 'item_id', placeholder: 'Velg mal fra katalogen' } },
    { Picker: { label: 'Gruppe', keypath: 'researchRequest.state.groups', optionLabelKeypath: 'label',
      selectionStateKeypath: 'researchRequest.state.selectedGroup', selectionValueKeypath: 'id', selectionPayloadMode: 'item_id', placeholder: 'Velg gruppe du er med i' } },
    { Picker: { label: 'Svarform', keypath: 'researchRequest.state.forms', optionLabelKeypath: 'label',
      selectionStateKeypath: 'researchRequest.state.selectedForm', selectionValueKeypath: 'id', selectionPayloadMode: 'item_id', placeholder: 'Velg svarform' } },
    { TextArea: { label: 'Formål', sourceKeypath: 'researchRequest.state.purpose', targetKeypath: 'researchRequest.purpose.set', placeholder: 'Hva skal tallene brukes til?' } },
    key('researchRequest.state.periodLabel', { fontSize: 13, foregroundColor: muted }),
  ]),
  card([
    text('Feil i forespørselen', { fontStyle: 'headline', foregroundColor: red }),
    list('researchRequest.state.errors', [ key('message', { fontSize: 14, foregroundColor: red }) ]),
  ], { ...when('researchRequest.state.valid', false), borderColor: '#FCA5A5' }),
  card([
    text('Slik ser kortet ut for dem du spør', { fontStyle: 'headline' }),
    key('researchRequest.state.preview.who', { fontWeight: '700' }),
    key('researchRequest.state.preview.what', { fontSize: 14 }),
    key('researchRequest.state.preview.recipients', { fontSize: 14, foregroundColor: muted }),
    { HStack: { spacing: 8, modifiers: { wrap: true }, elements: [
      { Button: { keypath: 'researchRequest.send', label: 'Send til gruppen', payload: {}, modifiers: when('researchRequest.state.valid', true) } },
      { Button: { keypath: 'researchRequest.saveDraft', label: 'Lagre utkast', payload: {}, modifiers: secondary } },
    ] } },
  ]),
] } };
const builderBase = {
  templates: [ { id: 'chat.messagesPerWeek.v1', label: 'Meldinger per uke i en gruppe (v1)' }, { id: 'onboarding.firstMessage.v1', label: 'Tid fra invitasjon til første melding (v1)' } ],
  forms: [ { id: 'aggregate', label: 'Samlet svar (studenten ser bare summen)' }, { id: 'rows', label: 'Per person, med pseudonym' } ],
  selectedTemplate: 'chat.messagesPerWeek.v1',
  purpose: 'Undersøke hvor aktivt studentgrupper bruker en delt samtale gjennom et semester.',
  periodLabel: 'Periode: 17.11–15.12.2026 · lagring til 30.06.2027 · minste gruppe 5',
  preview: { who: 'Sara Nilsen, masterstudent ved UiO, spør deg', what: 'Antall meldinger du har sendt per uke i gruppen. Tallet regnes ut hos deg.',
    recipients: 'Summen vises for Sara når minst 5 har sagt ja.' },
};
const builderStates = {
  'foresporsel-utfylt': { researchRequest: { state: { ...builderBase, valid: true, errors: [],
    groups: [ { id: 'g1', label: 'HAVEN Master 2026 (9 medlemmer)' } ], selectedGroup: 'g1', selectedForm: 'aggregate' } } },
  'foresporsel-avvist': { researchRequest: { state: { ...builderBase, valid: false,
    errors: [ { message: 'Gruppen «Lesesal 3» har 3 medlemmer. Samlet svar krever minst 5.' },
              { message: '«Per person» krever en begrunnelse for hvorfor summen ikke er nok.' } ],
    groups: [ { id: 'g2', label: 'Lesesal 3 (3 medlemmer)' } ], selectedGroup: 'g2', selectedForm: 'rows',
    preview: { ...builderBase.preview, recipients: 'Kan ikke sendes før feilene over er rettet.' } } } },
};

const surfaces = [
  ['dashbord', dashboard, dashboardStates, ['Mitt forskningsdashbord']],
  ['foresporselskort', inbox, inboxStates, ['Hvis du trekker deg']],
  ['foresporsel', builder, builderStates, ['Slik ser kortet ut for dem du spør']],
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
  await page.goto('http://research.test/');
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
    'dashbord-fylt': ['Uke 44 er skjult', 'færre enn 5', 'Mine forespørsler', '6 av 9 har sagt ja'],
    'dashbord-uten-rolle': ['Be om forskertilgang'],
    'kort-ny': ['Ikke nå', 'Aldri', 'Sara ser bare summen'],
    'kort-godtatt': ['Trekk samtykket', 'Kvittering'],
    'foresporsel-utfylt': ['Send til gruppen'],
    'foresporsel-avvist': ['krever minst 5', 'krever en begrunnelse'],
  };
  const notIn = { 'dashbord-uten-rolle': ['Mine forespørsler'], 'kort-ny': ['Trekk samtykket'], 'kort-godtatt': ['Ikke nå'], 'foresporsel-avvist': ['Send til gruppen'] };
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
