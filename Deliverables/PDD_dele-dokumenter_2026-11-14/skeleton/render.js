// Renders the G1-GUI images for PDD_dele-dokumenter with the real CellScaffold
// web renderer (Public/js/skeleton-runtime.js + porthole-webo.css + Quill).
// Usage: node render.js <cellscaffold/Public> <out-dir>
const path = require('node:path');
const { chromium } = require('playwright');
const publicDir = process.argv[2];
const out = process.argv[3];

const body = { foregroundColor: '#172033' };
const subtle = { foregroundColor: '#475569', fontSize: 14 };
const h1 = { foregroundColor: '#172033', fontSize: 24, fontWeight: 'bold' };
const h2 = { foregroundColor: '#172033', fontSize: 17, fontWeight: 'semibold' };
const primary = { background: '#1D4ED8', foregroundColor: '#FFFFFF', cornerRadius: 6 };
const secondary = { background: '#FFFFFF', foregroundColor: '#334155', borderColor: '#CBD5E1', borderWidth: 1, cornerRadius: 6 };
const danger = { background: '#FFFFFF', foregroundColor: '#B42318', borderColor: '#F3C1BC', borderWidth: 1, cornerRadius: 6 };
const card = { padding: 12, cornerRadius: 10, background: '#F8FAFC', borderColor: '#E2E8F0', borderWidth: 1 };
const when = (keypath, equals = true) => ({ visibility: { when: { scope: 'root', keypath, equals } } });
const T = (text, m = body) => ({ Text: { text, modifiers: m } });
const K = (keypath, m = body) => ({ Text: { keypath, modifiers: m } });
const B = (keypath, label, m = secondary, extra = {}) => ({ Button: { keypath, label, payloadKeypath: 'id', ...extra, modifiers: m } });
const V = (elements, modifiers = {}, spacing = 8) => ({ VStack: { elements, spacing, modifiers } });
const H = (elements, spacing = 8) => ({ HStack: { elements, spacing, modifiers: { wrap: true } } });
const L = (keypath, row) => ({ List: { keypath, elements: [], flowElementSkeleton: row } });

const section = (title, listKeypath, hasKeypath, emptyText, row) => V([
  T(title, h2),
  { Text: { text: emptyText, modifiers: { ...subtle, ...when(hasKeypath, false) } } },
  { VStack: { spacing: 8, elements: [L(listKeypath, row)], modifiers: when(hasKeypath) } },
], {}, 6);

const librarySkeleton = V([
  T('Dokumenter', h1),
  T('Dokumenter du eier, og dokumenter andre har invitert deg til.', subtle),
  H([B('documents.create', 'Nytt dokument', primary, { payload: {} })]),
  section('Invitasjoner til deg', 'documents.state.invitations', 'documents.state.hasInvitations', 'Ingen ventende invitasjoner.',
    V([K('title', h2), K('summary', subtle), H([B('documents.acceptInvitation', 'Godta', primary), B('documents.declineInvitation', 'Avslå')])], card)),
  section('Mine dokumenter', 'documents.state.mine', 'documents.state.hasMine', 'Du har ingen dokumenter ennå. Trykk «Nytt dokument» for å lage det første.',
    V([K('title', h2), K('people', subtle), K('updated', subtle), H([B('documents.open', 'Åpne', primary), B('documents.share', 'Del')])], card)),
  section('Delt med meg', 'documents.state.shared', 'documents.state.hasShared', 'Ingen har delt dokumenter med deg ennå.',
    V([K('title', h2), K('people', subtle), K('updated', subtle), H([B('documents.open', 'Åpne', primary), B('documents.leave', 'Forlat')])], card)),
], { padding: 4 }, 16);

const sharePanel = V([
  T('Del dokumentet', h2),
  T('Velg en person du har en samtale med, og hva personen kan gjøre. Personen må godta før de får tilgang.', subtle),
  { Picker: { label: 'Person', keypath: 'share.state.contacts', optionLabelKeypath: 'name', placeholder: 'Velg person' } },
  { Picker: { label: 'Rolle', keypath: 'share.state.roles', optionLabelKeypath: 'label', placeholder: 'Velg rolle' } },
  H([B('share.invite', 'Send invitasjon', primary, { payload: {} })]),
  T('Deltakere', h2),
  L('share.state.participants', V([K('name', h2), K('summary', subtle), H([B('share.remove', 'Fjern', danger)])], card, 4)),
], card, 10);

const docTitle = V([T('Metodekapittel', h1), T('Eier: deg · 3 deltakere · lagret 15.11 kl. 01.12', subtle)], {}, 4);
const documentSkeleton = { HStack: { spacing: 20, modifiers: { layoutVariants: [{ maxAvailableWidth: 760, axis: 'vertical' }] }, elements: [
  V([docTitle, { Visualization: { kind: 'richDocument', keypath: 'document.current', actionKeypath: 'document.change' } }], { minWidth: 320 }, 12),
  { VStack: { ...sharePanel.VStack, modifiers: { ...card, width: 360, layoutVariants: [{ maxAvailableWidth: 760, width: null }] } } },
] } };

const invitationSkeleton = V([
  T('Invitasjon til et dokument', h1),
  V([K('invite.title', h2), K('invite.summary', body), K('invite.boundary', subtle),
    H([B('documents.acceptInvitation', 'Godta og åpne', primary), B('documents.declineInvitation', 'Avslå')])], card, 10),
], {}, 14);

const deniedSkeleton = V([
  T('Ingen tilgang', h1),
  V([T('Du har ikke tilgang til dette dokumentet.', h2),
    T('Dokumenter i HAVEN åpnes bare for personer eieren har invitert, og som har godtatt invitasjonen. Be eieren om en invitasjon.', body),
    H([B('documents.openLibrary', 'Til Dokumenter', primary, { payload: {} })])], card, 10),
], {}, 14);

const filled = { documents: { state: {
  hasInvitations: true, hasMine: true, hasShared: true,
  invitations: [{ id: 'i1', title: 'Litteraturgjennomgang', summary: 'Ola Nordmann inviterer deg til å skrive · utløper 22.11' }],
  mine: [
    { id: 'd1', title: 'Metodekapittel', people: 'Delt med Sara (skriver) og Petter (leser) · Ola har ikke svart', updated: 'Endret 15.11 kl. 01.12 av Sara' },
    { id: 'd2', title: 'Notater fra veiledning', people: 'Bare deg', updated: 'Endret 12.11' },
  ],
  shared: [{ id: 'd3', title: 'Felles prosjektplan', people: 'Eier: Sara Hansen · du kan skrive', updated: 'Endret 14.11 av Sara' }],
} } };
const empty = { documents: { state: { hasInvitations: false, hasMine: false, hasShared: false, invitations: [], mine: [], shared: [] } } };
const share = { share: { state: {
  contacts: [{ name: 'Ola Nordmann' }, { name: 'Sara Hansen' }, { name: 'Petter Nielsen' }],
  roles: [{ label: 'Kan skrive' }, { label: 'Kan lese' }],
  participants: [
    { id: 'p1', name: 'Sara Hansen', summary: 'Kan skrive · godtok 14.11' },
    { id: 'p2', name: 'Petter Nielsen', summary: 'Kan lese · godtok 14.11' },
    { id: 'p3', name: 'Ola Nordmann', summary: 'Kan skrive · venter på svar · utløper 21.11' },
  ] } },
  document: { current: { schema: 'haven.document.v1', documentId: 'mock', revision: 9, sequence: 20, events: [], comments: [], presence: [], messages: [], help: [],
    ops: [{ insert: 'Metode' }, { insert: '\n', attributes: { header: 2 } },
      { insert: 'Vi bygger en prototyp med to scaffolds og måler hvor mye informasjon som lekker mellom domener.\n' },
      { insert: 'Sara: Her bør vi beskrive hvordan vi velger testpersoner.\n' }] } } };
const invite = { invite: {
  title: 'Litteraturgjennomgang',
  summary: 'Ola Nordmann inviterer deg til å skrive i dokumentet. Invitasjonen gjelder bare deg og utløper 22.11.',
  boundary: 'Godtar du, ser de andre deltakerne navnet ditt og det du skriver. Du kan forlate dokumentet når du vil.' } };

async function shot(width, height, name, skeleton, state, needsQuill) {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width, height }, deviceScaleFactor: 2 });
  await page.route('https://document.test/**', route => {
    const p = new URL(route.request().url()).pathname;
    if (p === '/') return route.fulfill({ contentType: 'text/html; charset=utf-8', body: '<!doctype html><html lang="nb"><head><link rel="stylesheet" href="/css/porthole-webo.css"><meta name="viewport" content="width=device-width,initial-scale=1"></head><body><main id="root" class="canvas view-mode" style="padding:16px"></main><script src="/vendor/quill/quill.js"></script><script src="/js/skeleton-runtime.js"></script></body></html>' });
    return route.fulfill({ path: path.join(publicDir, p), contentType: p.endsWith('.css') ? 'text/css' : 'application/javascript; charset=utf-8' });
  });
  await page.goto('https://document.test/');
  await page.evaluate(({ skeleton, state }) => {
    const root = document.getElementById('root');
    window.renderer = HavenSkeletonRuntime.createRenderer({ rootElement: root, skeleton, layoutContext: { availableWidth: root.clientWidth }, onAction: async () => ({ ok: true }) });
    window.renderer.update(state);
  }, { skeleton, state });
  if (needsQuill) await page.waitForSelector('.ql-editor');
  await page.waitForTimeout(600);
  await page.screenshot({ path: path.join(out, name), fullPage: true });
  await browser.close();
}

(async () => {
  for (const [w, h, dev] of [[1280, 900, 'laptop'], [390, 844, 'iphone']]) {
    await shot(w, h, `dokumenter-fylt-${dev}-v1.png`, librarySkeleton, filled);
    await shot(w, h, `dokumenter-tom-${dev}-v1.png`, librarySkeleton, empty);
    await shot(w, h, `inviter-${dev}-v1.png`, documentSkeleton, share, true);
    await shot(w, h, `invitasjon-${dev}-v1.png`, invitationSkeleton, invite);
    await shot(w, h, `ingen-tilgang-${dev}-v1.png`, deniedSkeleton, {});
  }
})();
