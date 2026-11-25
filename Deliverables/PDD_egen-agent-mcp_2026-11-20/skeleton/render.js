// Renders the G1-GUI images for PDD egen-agent-mcp with the real CellScaffold web renderer
// (Public/js/skeleton-runtime.js, porthole-webo.css, admin-skeleton.css).
// One surface, «Egne agenter», in four states: request, connected, disconnected, log.
// Every keypath under ownAgents.* is a proposal; none exists in CellScaffold today.
// Usage: node render.js <cellscaffold> <out-images> <out-skeleton>
const fs = require('node:fs');
const path = require('node:path');
const { chromium } = require('playwright');
const [scaffold, outImages, outSkeleton] = process.argv.slice(2);
const pub = path.join(scaffold, 'Public');

const ink = '#172033', muted = '#556273', teal = '#0F766E', red = '#B91C1C', amber = '#92400E';
const text = (t, o = {}) => ({ Text: { text: t, modifiers: { foregroundColor: ink, ...o } } });
const key = (k, o = {}) => ({ Text: { keypath: k, modifiers: { foregroundColor: ink, ...o } } });
const when = (keypath, equals, scope = 'root') => ({ visibility: { when: { equals, keypath, scope } } });
const card = (elements, extra = {}) => ({ VStack: { spacing: 10, elements, modifiers: {
  padding: 16, background: '#FFFFFF', cornerRadius: 12, borderWidth: 1, borderColor: '#E2E8F0', maxWidthInfinity: true, ...extra } } });
const secondary = { background: '#FFFFFF', borderColor: '#CBD5E1', borderWidth: 1, cornerRadius: 6, foregroundColor: '#334155' };
const danger = { background: '#FFFFFF', borderColor: '#FCA5A5', borderWidth: 1, cornerRadius: 6, foregroundColor: red };
const list = (keypath, rowElements) => ({ List: { elements: [], keypath, selectionMode: 'none', modifiers: { itemSpacing: 8 },
  flowElementSkeleton: { VStack: { spacing: 2, elements: rowElements } } } });
const row = (l, r, ro = {}) => ({ HStack: { spacing: 8, elements: [key(l, { fontWeight: '700' }), { Spacer: {} }, key(r, { fontSize: 13, foregroundColor: teal, ...ro })] } });
const picker = (label, k, sel, ph) => ({ VStack: { spacing: 4, elements: [ text(label, { fontSize: 13, foregroundColor: muted }),
  { Picker: { keypath: k, optionLabelKeypath: 'label', selectionStateKeypath: sel, selectionValueKeypath: 'id', selectionPayloadMode: 'item_id', placeholder: ph } } ] } });

const surface = { VStack: { spacing: 14, elements: [
  card([
    text('Egne agenter', { fontStyle: 'title2', fontWeight: '700' }),
    text('Her kobler du din egen Claude Code eller Codex til entiteten din. Agenten kjører på din maskin med ditt eget abonnement. HAVEN ser aldri innloggingen din, og agenten får aldri mer tilgang enn du har selv.', { fontSize: 14, foregroundColor: muted }),
  ]),
  // Request
  card([
    text('Ny forespørsel', { fontStyle: 'headline', foregroundColor: amber }),
    key('ownAgents.state.request.title', { fontWeight: '700' }),
    key('ownAgents.state.request.machine', { fontSize: 14 }),
    key('ownAgents.state.request.fingerprint', { fontSize: 13, foregroundColor: muted }),
    key('ownAgents.state.request.provider', { fontSize: 14 }),
    key('ownAgents.state.request.leavesNote', { fontSize: 13, foregroundColor: amber }),
    text('Agenten ber om', { fontSize: 13, foregroundColor: muted, fontWeight: '700' }),
    list('ownAgents.state.request.cells', [ row('name', 'access', { foregroundColor: ink }), key('note', { fontSize: 13, foregroundColor: muted }) ]),
    text('Holdes tilbake', { fontSize: 13, foregroundColor: muted, fontWeight: '700' }),
    list('ownAgents.state.request.withheld', [ key('name', { fontWeight: '700' }), key('reason', { fontSize: 13, foregroundColor: muted }) ]),
    picker('Gyldig i', 'ownAgents.state.durations', 'ownAgents.state.selectedDuration', 'Velg varighet'),
    { HStack: { spacing: 8, modifiers: { wrap: true }, elements: [
      { Button: { keypath: 'ownAgents.request.approve', label: 'Godkjenn med passkey', payload: {} } },
      { Button: { keypath: 'ownAgents.request.reject', label: 'Avvis', payload: {}, modifiers: danger } },
    ] } },
    text('Sjekk at fingeravtrykket er det samme som agenten viser i terminalen din.', { fontSize: 12, foregroundColor: muted }),
  ], { ...when('ownAgents.state.hasRequest', true), borderColor: '#FCD34D' }),
  // Connected agents
  card([
    { HStack: { spacing: 8, elements: [ text('Tilkoblede agenter', { fontStyle: 'headline' }), { Spacer: {} }, key('ownAgents.state.countLabel', { fontSize: 13, foregroundColor: muted }) ] } },
    list('ownAgents.state.agents', [
      row('title', 'status'),
      key('provider', { fontSize: 14 }),
      key('validity', { fontSize: 13, foregroundColor: muted }),
      key('cellsLabel', { fontSize: 13, foregroundColor: muted }),
      key('lastUse', { fontSize: 13, foregroundColor: muted }),
      { HStack: { spacing: 8, modifiers: { wrap: true, ...when('active', true, 'item') }, elements: [
        { Button: { keypath: 'ownAgents.agent.showLog', label: 'Vis logg', payload: {}, modifiers: secondary } },
        { Button: { keypath: 'ownAgents.agent.disconnect', label: 'Koble fra', payload: {}, modifiers: danger } },
      ] } },
      key('revokedNote', { fontSize: 13, foregroundColor: red, ...when('active', false, 'item') }),
      { HStack: { spacing: 8, modifiers: { wrap: true, ...when('active', false, 'item') }, elements: [
        { Button: { keypath: 'ownAgents.agent.showLog', label: 'Vis logg', payload: {}, modifiers: secondary } } ] } },
    ]),
    text('Ingen agenter er koblet til.', { fontSize: 14, foregroundColor: muted, ...when('ownAgents.state.hasAgents', false) }),
  ], when('ownAgents.state.showLog', false)),
  // Log
  card([
    { HStack: { spacing: 8, elements: [ key('ownAgents.state.log.title', { fontStyle: 'headline' }), { Spacer: {} },
      { Button: { keypath: 'ownAgents.log.close', label: 'Tilbake', payload: {}, modifiers: secondary } } ] } },
    key('ownAgents.state.log.summary', { fontSize: 13, foregroundColor: muted }),
    list('ownAgents.state.log.events', [
      row('tool', 'outcome'),
      key('detail', { fontSize: 13, foregroundColor: muted }),
    ]),
    text('Loggen ligger hos entiteten din. Agenten kan ikke endre den.', { fontSize: 12, foregroundColor: muted }),
  ], when('ownAgents.state.showLog', true)),
] } };

const durations = [ { id: '7d', label: '7 dager' }, { id: '30d', label: '30 dager' }, { id: 'semester', label: 'Ut semesteret (30.06.2027)' } ];
const request = {
  title: 'Claude Code vil koble seg til som deg',
  machine: 'Maskin: Saras MacBook Air (macOS)',
  fingerprint: 'Fingeravtrykk: 7F3A 91C2 0D4E B8A1',
  provider: 'Leverandør: Anthropic (Claude Code, ditt eget abonnement)',
  leavesNote: 'Det agenten leser, sendes til Anthropic under din konto. Bare data der vilkårene tillater Anthropic som mottaker, blir gitt ut.',
  cells: [
    { name: 'HAVEN-dokumentasjonen', access: 'lese', note: 'Åpen for alle' },
    { name: 'Mine dokumenter', access: 'lese og lagre utkast', note: 'Agenten kan lagre nye utkast. Den kan ikke dele, publisere eller slette.' },
    { name: 'Delt: «Unik representasjon» (fra Petter Nielsen)', access: 'lese', note: 'Petters vilkår tillater ekstern mottaker' },
    { name: 'Mitt forskningsdashbord', access: 'lese, nivå N1', note: 'Bare data uten personopplysninger' },
  ],
  withheld: [
    { name: 'Felles chat «Masteroppgave»', reason: 'Kjetil har ikke tillatt ekstern mottaker. Agenten ser bare dine egne meldinger der.' },
    { name: 'Intervjunotater (forskningsdata N3)', reason: 'Over nivået agenten kan få' },
    { name: 'Spørreundersøkelsen «Bruk av HAVEN»', reason: 'Cellen har ikke vilkår om mottaker ennå, så den er stengt for agenter' },
  ],
};
const claudeAgent = { title: 'Claude Code på Saras MacBook Air', status: 'tilkoblet', active: true,
  provider: 'Anthropic · fingeravtrykk 7F3A 91C2 0D4E B8A1', validity: 'Godkjent 21.11.2026 · gyldig til 21.12.2026',
  cellsLabel: 'Dokumentasjonen, Mine dokumenter, «Unik representasjon», Forskningsdashbord (N1)', lastUse: 'Sist brukt i dag 22:41 · 14 kall, 2 holdt tilbake' };
const codexAgent = { title: 'Codex på Saras jobbmaskin (Windows)', status: 'tilkoblet', active: true,
  provider: 'OpenAI · fingeravtrykk C2E0 44B7 9A18 3F65', validity: 'Godkjent 18.11.2026 · gyldig til 25.11.2026',
  cellsLabel: 'Dokumentasjonen, Mine dokumenter', lastUse: 'Sist brukt 20.11 09:12 · 3 kall' };
const base = (o) => ({ ownAgents: { state: { durations, selectedDuration: '30d', showLog: false, hasRequest: false, hasAgents: true, ...o } } });

const states = {
  'egen-agent-foresporsel': base({ hasRequest: true, request, agents: [codexAgent], countLabel: '1 tilkoblet' }),
  'egen-agent-godkjent': base({ agents: [claudeAgent, codexAgent], countLabel: '2 tilkoblet' }),
  'egen-agent-frakoblet': base({ countLabel: '1 tilkoblet', agents: [
    { ...claudeAgent, status: 'frakoblet 21.11 22:50', active: false, lastUse: 'Sist brukt i dag 22:41',
      revokedNote: 'Du koblet fra agenten. Neste kall fra den blir avvist, og nøkkelen kan ikke brukes igjen.' }, codexAgent ] }),
  'egen-agent-logg': base({ showLog: true, agents: [claudeAgent, codexAgent], log: {
    title: 'Logg: Claude Code på Saras MacBook Air', summary: 'I dag · 14 kall · 12 svar · 2 holdt tilbake',
    events: [
      { tool: '22:41 Lagre utkast', outcome: 'lagret', detail: 'Mine dokumenter · «Analyse av kapittel 2» (nytt utkast, ikke delt)' },
      { tool: '22:39 Les dokument', outcome: 'lest', detail: '«Unik representasjon» v4 · fra Petter Nielsen' },
      { tool: '22:38 Les chat', outcome: 'delvis', detail: 'Felles chat «Masteroppgave» · 6 egne meldinger gitt, 11 holdt tilbake (ingen ekstern mottaker tillatt)' },
      { tool: '22:36 Hent forskningsdata', outcome: 'avvist', detail: 'Intervjunotater · nivå N3 er over det agenten kan få' },
      { tool: '22:35 Søk i dokumentasjonen', outcome: 'lest', detail: '«entitetsutvidelse» · 5 treff i Book' },
    ] } }),
};

async function shot(width, name, state, mustContain, mustNot) {
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
  await page.goto('http://agents.test/');
  await page.waitForFunction(() => Boolean(window.HavenSkeletonRuntime?.createRenderer));
  await page.evaluate(([sk, st]) => {
    const root = document.getElementById('root');
    const r = window.HavenSkeletonRuntime.createRenderer({ rootElement: root, skeleton: sk, layoutContext: { availableWidth: root.clientWidth } });
    r.update(st);
  }, [surface, state]);
  await page.waitForTimeout(300);
  if (errors.length) throw new Error(`${name}: ${errors.join('; ')}`);
  const t = await page.locator('#root').innerText();
  for (const m of mustContain) if (!t.includes(m)) throw new Error(`${name}: missing «${m}»`);
  for (const m of mustNot) if (t.includes(m)) throw new Error(`${name}: «${m}» should be hidden`);
  await page.locator('#root').screenshot({ path: path.join(outImages, name) });
  await browser.close();
}

(async () => {
  fs.mkdirSync(outSkeleton, { recursive: true });
  fs.mkdirSync(outImages, { recursive: true });
  fs.writeFileSync(path.join(outSkeleton, 'egne-agenter.v1.json'), JSON.stringify(surface, null, 2) + '\n');
  fs.writeFileSync(path.join(outSkeleton, 'egne-agenter-tilstander.v1.json'), JSON.stringify(states, null, 2) + '\n');
  const checks = {
    'egen-agent-foresporsel': [['Ny forespørsel', 'Godkjenn med passkey', 'Holdes tilbake', 'stengt for agenter', '7F3A 91C2'], ['Vis logg Koble fra Vis logg']],
    'egen-agent-godkjent': [['Tilkoblede agenter', 'Koble fra', '2 tilkoblet'], ['Ny forespørsel']],
    'egen-agent-frakoblet': [['frakoblet 21.11 22:50', 'Neste kall fra den blir avvist'], ['Ny forespørsel']],
    'egen-agent-logg': [['Logg: Claude Code', 'holdt tilbake', 'avvist', 'Agenten kan ikke endre den'], ['Tilkoblede agenter']],
  };
  for (const [w, dev] of [[1280, 'laptop'], [390, 'iphone']])
    for (const [name, st] of Object.entries(states))
      await shot(w, `${name}-${dev}-v1.png`, st, ['Egne agenter', ...checks[name][0]], checks[name][1]);
  console.log('ok');
})().catch((e) => { console.error(e); process.exit(1); });
