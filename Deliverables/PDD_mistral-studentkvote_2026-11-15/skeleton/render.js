// G1-GUI images for PDD_mistral-studentkvote, rendered with the real CellScaffold
// web renderer (Public/js/skeleton-runtime.js + porthole-webo.css).
// Usage: node render.js <cellscaffold/Public> <out-dir>
const path = require('node:path');
const { chromium } = require('playwright');
const publicDir = process.argv[2];
const out = process.argv[3];

// Kallimachos palette (KallimachosAdvisorConfigurationFactory.Palette)
const ink = '#0F172A', secondary = '#475569', meta = '#64748B', accent = '#0F766E';
const body = { foregroundColor: ink };
const subtle = { foregroundColor: secondary, fontSize: 14 };
const caption = { foregroundColor: meta, fontSize: 13 };
const h1 = { foregroundColor: ink, fontSize: 24, fontWeight: 'bold' };
const h2 = { foregroundColor: ink, fontSize: 17, fontWeight: 'semibold' };
const primary = { background: accent, foregroundColor: '#FFFFFF', cornerRadius: 8 };
const secondaryBtn = { background: '#FFFFFF', foregroundColor: '#334155', borderColor: '#CBD5E1', borderWidth: 1, cornerRadius: 8 };
const selected = { background: '#F0FDFA', foregroundColor: accent, borderColor: accent, borderWidth: 2, cornerRadius: 8 };
const card = { padding: 14, cornerRadius: 12, background: '#FFFFFF', borderColor: '#E2E8F0', borderWidth: 1 };
const soft = { padding: 12, cornerRadius: 10, background: '#F0FDFA', borderColor: '#99F6E4', borderWidth: 1 };
const warn = { padding: 14, cornerRadius: 12, background: '#FFF7ED', borderColor: '#FED7AA', borderWidth: 1 };
const when = (keypath, equals = true) => ({ visibility: { when: { scope: 'root', keypath, equals } } });
const T = (text, m = body) => ({ Text: { text, modifiers: m } });
const K = (keypath, m = body) => ({ Text: { keypath, modifiers: m } });
const B = (keypath, label, m = secondaryBtn) => ({ Button: { keypath, label, payload: {}, modifiers: m } });
const V = (elements, modifiers = {}, spacing = 8) => ({ VStack: { elements, spacing, modifiers } });
const H = (elements, spacing = 8) => ({ HStack: { elements, spacing, modifiers: { wrap: true } } });
const L = (keypath, row) => ({ List: { keypath, elements: [], flowElementSkeleton: row } });
const sel = (flag, keypath, label) => ({ VStack: { spacing: 0, elements: [
  { Button: { keypath, label, payload: {}, modifiers: { ...selected, ...when(flag, true) } } },
  { Button: { keypath, label, payload: {}, modifiers: { ...secondaryBtn, ...when(flag, false) } } },
] } });

const header = V([T('Kallimachos', h1), T('Bibliotekaren i HAVEN. Svarer fra HAVEN-boka med kilder, og kan bruke en språkmodell du velger.', subtle)], {}, 4);

const sourcePicker = V([
  T('Hvem skal svare?', h2),
  H([
    sel('src.native', 'kallimachos.source.select', 'Bare bibliotekaren'),
    sel('src.local', 'kallimachos.source.select', 'Lokal modell'),
    sel('src.dimy', 'kallimachos.source.select', 'Hostet av DiMy · Mistral Small (EU)'),
    sel('src.own', 'kallimachos.source.select', 'Egen nøkkel'),
  ]),
  K('src.facts', caption),
], {}, 8);

const quota = V([
  H([T('Studentkvote', h2), K('quota.badge', { foregroundColor: accent, fontSize: 14, fontWeight: 'semibold' })]),
  K('quota.today', body),
  K('quota.term', subtle),
  K('quota.rule', caption),
], { ...soft, ...when('quota.show') }, 4);

const question = V([
  T('Spørsmålet ditt', h2),
  { TextArea: { keypath: 'draft', placeholder: 'Spør om HAVEN …', minLines: 3, maxLines: 6 } },
  H([B('kallimachos.ask', 'Spør Kallimachos', primary)]),
], card, 8);

const answer = V([
  T('Svar', h2),
  K('answer.text', body),
  L('answer.sources', V([K('label', caption)], {}, 0)),
  K('answer.servedBy', { foregroundColor: accent, fontSize: 13, fontWeight: 'semibold' }),
  K('answer.cost', caption),
], { ...card, ...when('answer.show') }, 8);

const notice = V([
  K('notice.title', { foregroundColor: '#9A3412', fontSize: 17, fontWeight: 'semibold' }),
  K('notice.message', body),
  K('notice.renew', subtle),
  H([B('kallimachos.source.select', 'Bruk lokal modell'), B('kallimachos.source.select', 'Bruk egen nøkkel'), B('kallimachos.source.select', 'Bare bibliotekaren', primary)]),
  K('notice.code', caption),
], { ...warn, ...when('notice.show') }, 8);

const kallimachos = V([header, sourcePicker, quota, notice, question, answer], { padding: 4 }, 16);

// Operator page. Today /admin/ai-usage is a Leaf HTML page, not a skeleton; this is a mockup.
const admin = V([
  T('Modeller DiMy tilbyr', h1),
  T('Bare modeller som er slått på her kan brukes på DiMys regning. Leverandørmodus koster penger og krever bekreftelse.', subtle),
  L('models', V([
    H([K('name', h2), K('state', { foregroundColor: accent, fontSize: 14, fontWeight: 'semibold' })]),
    K('facts', subtle), K('price', caption),
    H([{ Button: { keypath: 'admin.model.toggle', label: 'Slå av', payload: {}, modifiers: { ...secondaryBtn, visibility: { when: { scope: 'item', keypath: 'on', equals: true } } } } },
      { Button: { keypath: 'admin.model.toggle', label: 'Slå på', payload: {}, modifiers: { ...primary, visibility: { when: { scope: 'item', keypath: 'on', equals: false } } } } },
      B('admin.model.tariff', 'Endre pris')]),
  ], card, 6)),
  T('Studentkvote · MasterHAVEN26', h2),
  V([K('limits.day', body), K('limits.term', body), K('limits.service', body), H([B('admin.limits.edit', 'Endre grenser')])], card, 6),
  T('Forbruk i dag', h2),
  V([K('usage.total', body), L('usage.rows', V([H([K('who', body), K('spent', subtle)])], {}, 0))], card, 6),
], { padding: 4 }, 14);

const base = { draft: 'Hvordan bestemmer en Agreement hvem som får lese en celle?' };
const facts = { native: 'Svar uten språkmodell. Gratis. Ingenting forlater HAVEN.', dimy: 'Mistral Small 2603 · EU · hostet av DiMy · trekkes fra studentkvoten din.' };
const filled = { ...base,
  src: { dimy: true, native: false, local: false, own: false, facts: facts.dimy },
  quota: { show: true, badge: 'Student · MasterHAVEN26', today: 'I dag: 2,46 kr av 3,00 kr igjen (omtrent 120 svar til). Fornyes kl. 00.00.', term: 'Semesteret: 87,20 kr av 100 kr igjen.', rule: 'DiMy betaler. Kvoten kan ikke overføres eller tas ut i penger.' },
  answer: { show: true,
    text: 'En celle avgjør tilgang ut fra vilkårene i sin Agreement. Hvis vilkåret er «invitasjon akseptert», får du lese når du har godtatt invitasjonen, og ikke før. Eieren kan trekke Agreementen tilbake, og da avvises neste forespørsel.',
    sources: [{ label: 'Kilde: Book/09 Agreements og vilkår § 3' }, { label: 'Kilde: Book/12 Tilgang og nøkkelstier § 1' }],
    servedBy: 'Svart av Mistral Small (EU), hostet av DiMy',
    cost: 'Kostet 0,02 kr (812 inn, 214 ut) · kvittering lagret' } };
const exhausted = { ...base,
  src: { dimy: true, native: false, local: false, own: false, facts: facts.dimy },
  quota: { show: true, badge: 'Student · MasterHAVEN26', today: 'I dag: 0,00 kr av 3,00 kr igjen.', term: 'Semesteret: 61,40 kr av 100 kr igjen.', rule: 'DiMy betaler. Kvoten kan ikke overføres eller tas ut i penger.' },
  notice: { show: true, title: 'Dagens kvote er brukt opp', message: 'Spørsmålet ble ikke sendt, og ingenting er trukket.', renew: 'Kvoten fornyes kl. 00.00. Til da kan du bruke den lokale modellen, egen nøkkel eller få svar fra bibliotekaren uten modell.', code: 'Kode: student_quota_exhausted_today' } };
const notStudent = { ...base,
  src: { dimy: true, native: false, local: false, own: false, facts: 'Mistral Small 2603 · EU · hostet av DiMy · for studenter med studentrolle fra Informasjonssystemer.' },
  notice: { show: true, title: 'Hostet av DiMy er for studenter i MasterHAVEN26', message: 'Kontoen din har ikke studentrollen fra Informasjonssystemer, så spørsmålet ble ikke sendt.', renew: 'Er du student, be veilederen din om studentrollen. Du kan også bruke den lokale modellen, egen nøkkel eller bibliotekaren uten modell.', code: 'Kode: not_eligible' } };
const unknown = { ...base,
  src: { dimy: true, native: false, local: false, own: false, facts: facts.dimy },
  notice: { show: true, title: 'Vi kan ikke bekrefte studentrollen akkurat nå', message: 'Statuslisten fra Informasjonssystemer er ikke oppdatert de siste 10 minuttene, så spørsmålet ble ikke sendt. Det er ikke trukket noe.', renew: 'Prøv igjen om litt, eller velg en annen kilde.', code: 'Kode: role_status_unknown' } };
const adminState = {
  models: [
    { name: 'Mistral Small 2603', on: true, state: 'På', facts: 'Mistral · EU-endepunkt · hostet av DiMy', price: '1,40 kr per million tokens inn · 5,60 kr per million tokens ut · pris fra 20.11 (eksempel)' },
    { name: 'Claude Haiku 5.5', on: false, state: 'Av', facts: 'Anthropic · venter på ditt ja og pris', price: 'Ingen pris lagt inn' },
    { name: 'OpenAI (current)', on: false, state: 'Av', facts: 'OpenAI · venter på ditt ja og pris', price: 'Ingen pris lagt inn' },
  ],
  limits: { day: 'Per student per dag: 3,00 kr', term: 'Per student per semester: 100,00 kr', service: 'Hele tjenesten per døgn: 50,00 kr' },
  usage: { total: 'I dag: 7,84 kr av 50,00 kr · 14 studenter · 412 svar', rows: [
    { who: 'Sara Hansen', spent: '2,10 kr · 96 svar' }, { who: 'Ola Nordmann', spent: '3,00 kr · kvoten brukt opp 21.14' }, { who: 'Kari Berg', spent: '0,54 kr · 22 svar' } ] } };

async function shot(width, height, name, skeleton, state) {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width, height }, deviceScaleFactor: 2 });
  await page.route('https://kvote.test/**', route => {
    const p = new URL(route.request().url()).pathname;
    if (p === '/') return route.fulfill({ contentType: 'text/html; charset=utf-8', body: '<!doctype html><html lang="nb"><head><link rel="stylesheet" href="/css/porthole-webo.css"><meta name="viewport" content="width=device-width,initial-scale=1"></head><body><main id="root" class="canvas view-mode" style="padding:16px;max-width:860px"></main><script src="/js/skeleton-runtime.js"></script></body></html>' });
    return route.fulfill({ path: path.join(publicDir, p), contentType: p.endsWith('.css') ? 'text/css' : 'application/javascript; charset=utf-8' });
  });
  await page.goto('https://kvote.test/');
  await page.evaluate(({ skeleton, state }) => {
    const root = document.getElementById('root');
    window.renderer = HavenSkeletonRuntime.createRenderer({ rootElement: root, skeleton, layoutContext: { availableWidth: root.clientWidth }, onAction: async () => ({ ok: true }) });
    window.renderer.update(state);
  }, { skeleton, state });
  await page.waitForTimeout(500);
  await page.screenshot({ path: path.join(out, name), fullPage: true });
  await browser.close();
}

(async () => {
  for (const [w, h, dev] of [[1280, 900, 'laptop'], [390, 844, 'iphone']]) {
    await shot(w, h, `kvote-fylt-${dev}-v1.png`, kallimachos, filled);
    await shot(w, h, `kvote-tom-${dev}-v1.png`, kallimachos, exhausted);
    await shot(w, h, `ikke-student-${dev}-v1.png`, kallimachos, notStudent);
    await shot(w, h, `rollestatus-ukjent-${dev}-v1.png`, kallimachos, unknown);
    await shot(w, h, `drift-${dev}-v1.png`, admin, adminState);
  }
})();
