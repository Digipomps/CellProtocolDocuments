// Renders the G1-GUI images for PDD formal-velger-modellkilde with the real CellScaffold
// web renderer (Public/js/skeleton-runtime.js, porthole-webo.css, admin-skeleton.css).
// Base: the AI panel's provider list in playwright/fixtures/butler-chat-skeleton.json
// (chatHub.state.assistant.providerChoices, selection to chatHub.assistant.provider.select),
// dumped from PersonalCopilotConfigurationFactory on CellScaffold main. New here: each row
// shows where the model runs and its facts, a «Min maskin» section and an event log.
// Keypaths under chatHub.state.localModelAvailability.* are proposals, not implemented.
// The provider list uses styleRole admin-table, which hides the web renderer's «[x]» text
// marker (admin-skeleton.css:553); without it the selected row shows two «[x]» markers.
// Usage: node render.js <cellscaffold> <out-images> <out-skeleton>
const fs = require('node:fs');
const path = require('node:path');
const { chromium } = require('playwright');
const [scaffold, outImages, outSkeleton] = process.argv.slice(2);
const pub = path.join(scaffold, 'Public');

const ink = '#172033', muted = '#556273';
const text = (t, o = {}) => ({ Text: { text: t, modifiers: { foregroundColor: ink, ...o } } });
const key = (k, o = {}) => ({ Text: { keypath: k, modifiers: { foregroundColor: ink, ...o } } });
const when = (keypath, equals) => ({ visibility: { when: { equals, keypath, scope: 'root' } } });
const card = (elements, extra = {}) => ({ VStack: { spacing: 10, elements, modifiers: {
  padding: 16, background: '#FFFFFF', cornerRadius: 12, borderWidth: 1, borderColor: '#E2E8F0', maxWidthInfinity: true, ...extra } } });

const providerList = { List: { elements: [], keypath: 'chatHub.state.assistant.providerChoices',
  selectionActionKeypath: 'chatHub.assistant.provider.select', selectionMode: 'single', selectionPayloadMode: 'item_id',
  selectionStateKeypath: 'chatHub.state.ui.selectedProviderID', selectionValueKeypath: 'id',
  modifiers: { styleRole: 'admin-table', itemSpacing: 8 },
  flowElementSkeleton: { VStack: { spacing: 4, elements: [
    { HStack: { spacing: 8, elements: [ key('title', { fontWeight: '700' }), { Spacer: {} }, key('badge', { fontSize: 12, foregroundColor: '#0F766E' }) ] } },
    key('whereLabel', { fontSize: 13, foregroundColor: muted }),
    key('factsLabel', { fontSize: 13, foregroundColor: muted }),
  ] } } } };

const skeleton = { VStack: { spacing: 14, elements: [
  card([
    text('Velg modell', { fontStyle: 'headline' }),
    { HStack: { spacing: 8, elements: [ text('Valgt modell'), key('chatHub.state.ui.selectedProviderTitle', { fontWeight: '700' }) ] } },
    providerList,
    key('chatHub.state.ui.selectedProviderReview', { fontSize: 13, foregroundColor: muted }),
    { HStack: { spacing: 8, modifiers: { wrap: true }, elements: [
      { Button: { keypath: 'chatHub.assistant.provider.confirm', label: 'Godkjenn én sending', payload: { confirm: true } } },
      { Button: { keypath: 'chatHub.assistant.provider.select', label: 'Bruk lokale regler', payload: 'none',
        modifiers: { background: '#FFFFFF', borderColor: '#CBD5E1', borderWidth: 1, cornerRadius: 6, foregroundColor: '#334155' } } },
    ] } },
  ]),
  card([
    text('Min maskin', { fontStyle: 'headline' }),
    key('chatHub.state.localModelAvailability.statusTitle', { fontWeight: '700' }),
    key('chatHub.state.localModelAvailability.statusDetail', { fontSize: 13, foregroundColor: muted }),
    { Button: { keypath: 'chatHub.localModelAvailability.withdraw', label: 'Gjør utilgjengelig', payload: {},
      modifiers: { background: '#FFFFFF', borderColor: '#FCA5A5', borderWidth: 1, cornerRadius: 6, foregroundColor: '#B91C1C',
        ...when('chatHub.state.localModelAvailability.available', true) } } },
  ], when('chatHub.state.localModelAvailability.isOwner', true)),
  card([
    text('Hendelser', { fontStyle: 'headline' }),
    { List: { elements: [], keypath: 'chatHub.state.localModelAvailability.events', selectionMode: 'none',
      flowElementSkeleton: { VStack: { spacing: 0, elements: [ { HStack: { spacing: 10, elements: [ key('time', { fontSize: 13, foregroundColor: muted }), key('label', { fontSize: 13 }) ] } } ] } } } },
  ]),
] } };

const laptop = (owner) => ({ id: 'agent.local-model.kjetil-mbp', title: owner ? 'Din laptop · Gemma 4 12B' : 'Kjetils laptop · Gemma 4 12B',
  badge: owner ? 'Valgt' : '', whereLabel: owner ? 'Kjører på maskinen din. Spørsmålet forlater ikke maskinen.' : 'Kjører på Kjetils maskin. Spørsmålet sendes dit.',
  factsLabel: 'Svartid ca. 4 s · gratis · kan forsvinne når maskinen sover' });
const mistral = (badge) => ({ id: 'dimy.mistral-small', title: 'Mistral Small (EU)', badge,
  whereLabel: 'Hostet hos Mistral i EU, tilbudt av DiMy.', factsLabel: 'Svartid ca. 3 s · fra kvoten din · tilgjengelig hele døgnet' });
const rules = { id: 'chat.local-rules', title: 'Lokale chat-regler', badge: '',
  whereLabel: 'På serveren, uten modell.', factsLabel: 'Umiddelbart · gratis · alltid tilgjengelig' };

const states = {
  'valgliste-laptop-tilgjengelig': { owner: true, available: true,
    choices: [laptop(true), mistral(''), rules], selected: 'agent.local-model.kjetil-mbp', selectedTitle: 'Din laptop · Gemma 4 12B',
    review: 'Valgt fordi formålet er «utvikle og teste», og maskinen din er erklært tilgjengelig og svarte på helsesjekken for 2 min siden.',
    statusTitle: 'Tilgjengelig siden 09:20', statusDetail: 'Du sa fra i AgentD på laptopen. Synlig for deg og for dem du har gitt Agreement. Gyldig til du trekker den.',
    events: [ ['09:20', 'Tilgjengelig: du sa fra på laptopen'], ['09:21', 'Helsesjekk ok, svartid 3,8 s'], ['09:34', 'Svarte deg (Gemma 4 12B)'] ] },
  'valgliste-laptop-trukket': { owner: true, available: false,
    choices: [mistral('Valgt'), rules], selected: 'dimy.mistral-small', selectedTitle: 'Mistral Small (EU)',
    review: 'Laptopen din er ikke tilgjengelig. Valgt fordi den oppfyller kravene til «egen støtte i daglig bruk».',
    statusTitle: 'Ikke tilgjengelig', statusDetail: 'Du trakk den tilbake 10:05. Gjør den tilgjengelig igjen fra AgentD-menyen eller Binding på laptopen.',
    events: [ ['09:20', 'Tilgjengelig: du sa fra på laptopen'], ['09:58', 'Svarte ikke innen 8 s; Mistral svarte i stedet'], ['10:05', 'Utilgjengelig: du trakk den tilbake'] ] },
  'valgliste-laptop-annen-bruker': { owner: false, available: true,
    choices: [mistral('Valgt'), laptop(false), rules], selected: 'dimy.mistral-small', selectedTitle: 'Mistral Small (EU)',
    review: 'Valgt automatisk fordi den er tilgjengelig hele døgnet. Kjetils laptop kan du velge selv; den velges aldri automatisk.',
    statusTitle: '', statusDetail: '',
    events: [ ['09:20', 'Kjetils laptop er tilgjengelig'], ['09:21', 'Helsesjekk ok, svartid 3,8 s'] ] },
};

function rootFor(s) {
  return { chatHub: { state: {
    assistant: { providerChoices: s.choices },
    ui: { selectedProviderID: s.selected, selectedProviderTitle: s.selectedTitle, selectedProviderReview: s.review },
    localModelAvailability: { isOwner: s.owner, available: s.available, statusTitle: s.statusTitle, statusDetail: s.statusDetail,
      events: s.events.map(([time, label]) => ({ time, label })) } } } };
}

async function shot(width, name, s) {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width, height: 900 }, deviceScaleFactor: 2 });
  await page.route('**/*', async (route) => {
    const p = new URL(route.request().url()).pathname;
    const files = { '/js/skeleton-runtime.js': [path.join(pub, 'js/skeleton-runtime.js'), 'application/javascript'],
      '/css/porthole-webo.css': [path.join(pub, 'css/porthole-webo.css'), 'text/css'],
      '/css/admin-skeleton.css': [path.join(pub, 'css/admin-skeleton.css'), 'text/css'] };
    if (p === '/') return route.fulfill({ contentType: 'text/html', body: '<!doctype html><html lang="no"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="stylesheet" href="/css/porthole-webo.css"><link rel="stylesheet" href="/css/admin-skeleton.css"><style>body{margin:0;background:#f4f7fb;font-family:system-ui,sans-serif}#root{max-width:760px;margin:0 auto;padding:16px}</style></head><body><main id="root" class="canvas view-mode"></main><script src="/js/skeleton-runtime.js"></script></body></html>' });
    if (files[p]) return route.fulfill({ path: files[p][0], contentType: files[p][1] });
    return route.abort();
  });
  await page.goto('http://copilot.test/');
  await page.waitForFunction(() => Boolean(window.HavenSkeletonRuntime?.createRenderer));
  await page.evaluate(([sk, st]) => {
    const root = document.getElementById('root');
    const r = window.HavenSkeletonRuntime.createRenderer({ rootElement: root, skeleton: sk, layoutContext: { availableWidth: root.clientWidth } });
    r.update(st);
  }, [skeleton, rootFor(s)]);
  await page.waitForTimeout(300);
  const t = await page.locator('#root').innerText();
  for (const c of s.choices) if (!t.includes(c.title)) throw new Error(`${name}: missing row ${c.title}`);
  if (s.owner !== t.includes('Min maskin')) throw new Error(`${name}: Min maskin visible=${t.includes('Min maskin')}`);
  const withdraw = await page.getByRole('button', { name: 'Gjør utilgjengelig' }).count();
  if ((withdraw > 0 && await page.getByRole('button', { name: 'Gjør utilgjengelig' }).isVisible()) !== (s.owner && s.available)) throw new Error(`${name}: withdraw button`);
  await page.locator('#root').screenshot({ path: path.join(outImages, name) });
  await browser.close();
}

(async () => {
  fs.mkdirSync(outSkeleton, { recursive: true });
  fs.writeFileSync(path.join(outSkeleton, 'valgliste-og-min-maskin.v1.json'), JSON.stringify(skeleton, null, 2) + '\n');
  fs.writeFileSync(path.join(outSkeleton, 'tilstander.v1.json'), JSON.stringify(Object.fromEntries(Object.entries(states).map(([k, v]) => [k, rootFor(v)])), null, 2) + '\n');
  for (const [w, dev] of [[1280, 'laptop'], [390, 'iphone']])
    for (const [name, s] of Object.entries(states)) await shot(w, `${name}-${dev}-v1.png`, s);
  console.log('ok');
})().catch((e) => { console.error(e); process.exit(1); });
