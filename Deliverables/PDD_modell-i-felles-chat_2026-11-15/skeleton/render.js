// Renders the G1-GUI images for PDD_modell-i-felles-chat with the real CellScaffold
// web renderer (Public/js/skeleton-runtime.js + porthole-webo.css).
// Base: CellScaffold playwright/fixtures/samtaler-skeleton.js (mirrors
// PersonalCopilotConfigurationFactory.conversationsSkeleton() on main 9612217),
// extended with the model participant. Only element types Samtaler already uses.
// Usage: node render.js <cellscaffold> <out-images-dir> <out-skeleton-dir>
const fs = require('node:fs');
const path = require('node:path');
const { chromium } = require('playwright');
const scaffold = process.argv[2];
const outImages = process.argv[3];
const outSkeleton = process.argv[4];
const publicDir = path.join(scaffold, 'Public');
const { conversationsSkeleton } = require(path.join(scaffold, 'playwright/fixtures/samtaler-skeleton.js'));

const body = { foregroundColor: '#172033' };
const subtle = { foregroundColor: '#475569', fontSize: 14, styleRole: 'secondary-text' };
const small = { foregroundColor: '#5B21B6', fontSize: 13 };
const h2 = { foregroundColor: '#172033', fontSize: 16, fontWeight: 'semibold' };
const primary = { background: '#1D4ED8', foregroundColor: '#FFFFFF', cornerRadius: 6 };
const model = { background: '#6D28D9', foregroundColor: '#FFFFFF', cornerRadius: 6 };
const secondary = { background: '#FFFFFF', foregroundColor: '#334155', borderColor: '#CBD5E1', borderWidth: 1, cornerRadius: 6 };
const danger = { background: '#FFFFFF', foregroundColor: '#B42318', borderColor: '#F3C1BC', borderWidth: 1, cornerRadius: 6 };
const modelCard = { padding: 12, cornerRadius: 10, background: '#F5F3FF', borderColor: '#DDD6FE', borderWidth: 1 };
const warnCard = { padding: 12, cornerRadius: 10, background: '#FFF7ED', borderColor: '#FED7AA', borderWidth: 1 };
const when = (keypath, equals = true, scope = 'root') => ({ visibility: { when: { scope, keypath, equals } } });
const T = (text, m = body) => ({ Text: { text, modifiers: m } });
const K = (keypath, m = body) => ({ Text: { keypath, modifiers: m } });
const B = (keypath, label, m = secondary, extra = {}) => ({ Button: { keypath, label, payload: {}, ...extra, modifiers: extra.modifiers || m } });
const V = (elements, modifiers = {}, spacing = 8) => ({ VStack: { elements, spacing, modifiers } });
const H = (elements, spacing = 8) => ({ HStack: { elements, spacing, modifiers: { wrap: true } } });
const M = 'chatHub.state.conversation.model';

// 1. The model card under the people line: off, proposed, active.
const modelOff = B('chatHub.conversation.model.propose', 'Ta med en språkmodell', secondary, { modifiers: { ...secondary, ...when(`${M}.canPropose`) } });
const modelProposal = V([
  K(`${M}.proposal.title`, h2),
  K(`${M}.proposal.boundary`, body),
  K(`${M}.proposal.progress`, small),
  { VStack: { spacing: 0, elements: [H([B('chatHub.conversation.model.consent', 'Ja, ta med modellen', model), B('chatHub.conversation.model.decline', 'Nei takk')])], modifiers: when(`${M}.proposal.awaitingMe`) } },
], { ...modelCard, ...when(`${M}.hasProposal`) }, 8);
const modelActive = V([
  K(`${M}.activeSummary`, h2),
  K(`${M}.activeBoundary`, subtle),
  H([B('chatHub.conversation.model.remove', 'Fjern modellen', danger)]),
], { ...modelCard, ...when(`${M}.isActive`) }, 6);

// 2. Message bubble: as today, plus a source line on model messages (row scope).
const bubble = { VStack: { spacing: 4, elements: [
  { HStack: { spacing: 8, elements: [
    { Text: { keypath: 'author', modifiers: { ...body, styleRole: 'conversation-message-author', styleClasses: ['conversation-message-author'] } } },
    { Text: { keypath: 'time', modifiers: { ...body, styleRole: 'conversation-message-time', styleClasses: ['conversation-message-time'] } } },
  ] } },
  { Text: { keypath: 'body', modifiers: { ...body, styleRole: 'conversation-message-body', styleClasses: ['conversation-message-body'] } } },
  { Text: { keypath: 'source', modifiers: { ...small, ...when('isModel', true, 'item') } } },
], modifiers: { hAlignmentKeypath: 'align', backgroundKeypath: 'bubble', padding: 10, cornerRadius: 12 } } };

// 3. Ask row under the composer, only when the model is in the chat.
// Route choice: two buttons each, the selected one filled. Root visibility on
// model.mistralSelected, so no list is needed.
const routeButton = (id, label, selected) => ({ Button: { keypath: 'chatHub.conversation.model.route', label,
  payload: { route: id }, modifiers: { ...(selected ? model : secondary), fontSize: 13, ...when(`${M}.mistralSelected`, id === 'mistral' ? selected : !selected) } } });
const askRow = V([
  H([
    B('chatHub.conversation.model.ask', 'Spør modellen', model),
    T('eller skriv @modell i meldingen', subtle),
  ]),
  H([T('Modell:', subtle),
    routeButton('local', 'Qwen lokalt (gratis)', true), routeButton('local', 'Qwen lokalt (gratis)', false),
    routeButton('mistral', 'Mistral (EU)', true), routeButton('mistral', 'Mistral (EU)', false)]),
  K(`${M}.routeSummary`, subtle),
], when(`${M}.isActive`), 8);

// 4. Notice to the asker only, when the model could not answer.
const askerNotice = V([
  K(`${M}.notice.title`, h2),
  K(`${M}.notice.text`, body),
  H([B('chatHub.conversation.model.retryWith', 'Prøv med Mistral', model, { payload: { route: 'mistral' }, modifiers: { ...model, ...when(`${M}.notice.canRetryMistral`) } }),
     B('chatHub.conversation.model.dismissNotice', 'Lukk')]),
  T('Bare du ser denne meldingen.', subtle),
], { ...warnCard, ...when(`${M}.hasNotice`) }, 8);

function withModel(base) {
  const sk = JSON.parse(JSON.stringify(base));
  const layout = sk.VStack.elements[1].HStack.elements;
  const right = layout.find(e => e.VStack && e.VStack.modifiers && e.VStack.modifiers.styleRole === 'conversation-main');
  const conv = right.VStack.elements[0].VStack.elements;
  const peopleIdx = conv.findIndex(e => e.Text && e.Text.keypath === 'chatHub.state.conversation.people');
  conv.splice(peopleIdx + 1, 0, modelOff, modelProposal, modelActive);
  const list = conv.find(e => e.List && e.List.keypath === 'chatHub.state.conversation.messages');
  list.List.flowElementSkeleton = bubble;
  const composerIdx = conv.findIndex(e => e.TextArea);
  conv.splice(composerIdx + 1, 0, askerNotice);
  const sendIdx = conv.findIndex(e => e.HStack && e.HStack.elements.some(b => b.Button && b.Button.keypath === 'chatHub.conversation.send'));
  conv.splice(sendIdx + 1, 0, askRow);
  // The join-link block is unchanged and not needed in these pictures.
  return sk;
}

const me = { align: 'trailing', bubble: '#DBEAFE', isModel: false };
const them = { align: 'leading', bubble: '#F1F5F9', isModel: false };
const bot = { align: 'leading', bubble: '#F5F3FF', isModel: true };
const threads = [
  { id: 't1', title: 'Metodekapittel – gruppe 3', people: 'Du, Sara, Ola', preview: 'Språkmodell: Tre ting dere kan …', selected: true },
  { id: 't2', title: 'Veiledning uke 47', people: 'Du, Sara, Petter', preview: 'Petter: Vi sees torsdag.', selected: false },
];
const routes = (mistralSelected) => ({ mistralSelected });
const base = (extra) => ({ chatHub: { state: { composer: { body: '' }, conversation: {
  hasThreads: true, hasPendingInvites: false, hasCurrent: true, hasJoinLink: false, emptyHint: '',
  title: 'Metodekapittel – gruppe 3', threads, pendingInvites: [], ...extra } } } });

const states = {
  forslag: base({
    threads: [{ ...threads[0], preview: 'Ola: Kan vi spørre en språkmodell …' }, threads[1]],
    people: 'Du, Sara, Ola',
    messages: [
      { author: 'Sara', time: '10:02', body: 'Skal vi bruke intervju eller spørreskjema for å måle tillit?', ...them },
      { author: 'Du', time: '10:04', body: 'Kanskje begge? Jeg er usikker på hvordan vi begrunner det.', ...me },
      { author: 'Ola', time: '10:05', body: 'Kan vi spørre en språkmodell om fordeler og ulemper?', ...them },
    ],
    model: { canPropose: false, hasProposal: true, isActive: false, hasNotice: false, ...routes(false),
      proposal: {
        title: 'Ola foreslår å ta med en språkmodell i samtalen',
        boundary: 'Modellen svarer bare når noen spør den. Den får lese spørsmålet og de siste 20 meldingene etter at den ble lagt til, aldri det som står før. Standard er Qwen, som kjører på HAVENs egen server.',
        progress: '2 av 3 har sagt ja (Ola, Sara). Venter på deg.',
        awaitingMe: true } } }),
  fylt: base({
    people: 'Du, Sara, Ola, Språkmodell (modell)',
    composer: { body: '' },
    messages: [
      { author: 'Sara', time: '10:02', body: 'Skal vi bruke intervju eller spørreskjema for å måle tillit?', ...them },
      { author: 'Ola', time: '10:09', body: '@modell Hva er fordeler og ulemper med intervju mot spørreskjema når vi vil måle tillit til en app?', ...them },
      { author: 'Språkmodell', time: '10:09', body: 'Intervju gir dybde: dere hører hvorfor folk stoler eller ikke stoler, men med få personer. Spørreskjema gir tall fra mange, men fanger dårlig begrunnelser. En vanlig løsning er et kort skjema først og intervju med noen av dem etterpå.', source: 'Spurt av Ola · Qwen lokalt · leste 6 meldinger', ...bot },
      { author: 'Du', time: '10:12', body: 'Det likte jeg. Kan den foreslå tre spørsmål til skjemaet?', ...me },
      { author: 'Språkmodell', time: '10:12', body: '1. Hvor trygg er du på at appen bare deler det du har godtatt? 2. Har du noen gang angret på noe du har delt? 3. Hva skal til for at du stoler mer på appen?', source: 'Spurt av deg · Mistral (EU) · leste 8 meldinger · 13 av 20 igjen i dag', ...bot },
    ],
    model: { canPropose: false, hasProposal: false, isActive: true, hasNotice: false, ...routes(true, 13),
      activeSummary: 'Språkmodell er med i samtalen',
      activeBoundary: 'Alle tre sa ja 15.11. Svarer bare når noen spør. Ekstern modell (Mistral) er tillatt av alle.',
      routeSummary: 'Den som spør, velger modell. Mistral trekker fra din egen dagskvote: 13 av 20 igjen i dag.' } }),
  feil: base({
    people: 'Du, Sara, Ola, Språkmodell (modell)',
    messages: [
      { author: 'Sara', time: '10:02', body: 'Skal vi bruke intervju eller spørreskjema for å måle tillit?', ...them },
      { author: 'Du', time: '10:20', body: '@modell Kan du oppsummere det vi har blitt enige om?', ...me },
    ],
    model: { canPropose: false, hasProposal: false, isActive: true, hasNotice: true, ...routes(false),
      activeSummary: 'Språkmodell er med i samtalen',
      activeBoundary: 'Alle tre sa ja 15.11. Svarer bare når noen spør. Ekstern modell (Mistral) er tillatt av alle.',
      routeSummary: 'Den som spør, velger modell. Mistral trekker fra din egen dagskvote: 14 av 20 igjen i dag.',
      notice: { title: 'Modellen svarte ikke', text: 'Den lokale modellen (Qwen) er ikke tilgjengelig akkurat nå. Spørsmålet ditt er sendt som vanlig melding, men ingen modell har lest det. Du kan prøve Mistral, du har 14 av 20 spørsmål igjen i dag.', canRetryMistral: true } } }),
};

async function shot(width, height, name, skeleton, state) {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width, height }, deviceScaleFactor: 2 });
  await page.route('https://samtaler.test/**', route => {
    const p = new URL(route.request().url()).pathname;
    if (p === '/') return route.fulfill({ contentType: 'text/html; charset=utf-8', body: '<!doctype html><html lang="nb"><head><meta charset="utf-8"><link rel="stylesheet" href="/css/porthole-webo.css"><meta name="viewport" content="width=device-width,initial-scale=1"></head><body><main id="root" class="canvas view-mode" style="padding:16px"></main><script src="/js/skeleton-runtime.js"></script></body></html>' });
    return route.fulfill({ path: path.join(publicDir, p), contentType: p.endsWith('.css') ? 'text/css' : 'application/javascript; charset=utf-8' });
  });
  await page.goto('https://samtaler.test/');
  await page.evaluate(({ skeleton, state }) => {
    const root = document.getElementById('root');
    window.renderer = HavenSkeletonRuntime.createRenderer({ rootElement: root, skeleton, layoutContext: { availableWidth: root.clientWidth }, onAction: async () => ({ ok: true }) });
    window.renderer.update(state);
  }, { skeleton, state });
  await page.waitForTimeout(500);
  await page.screenshot({ path: path.join(outImages, name), fullPage: true });
  await browser.close();
}

(async () => {
  const skeleton = withModel(conversationsSkeleton({ responsive: true }));
  fs.mkdirSync(outSkeleton, { recursive: true });
  fs.writeFileSync(path.join(outSkeleton, 'samtaler-med-modell.v1.json'), JSON.stringify(skeleton, null, 2) + '\n');
  fs.writeFileSync(path.join(outSkeleton, 'tilstander.v1.json'), JSON.stringify(states, null, 2) + '\n');
  for (const [w, h, dev] of [[1280, 900, 'laptop'], [390, 844, 'iphone']]) {
    for (const [name, state] of Object.entries(states)) {
      await shot(w, h, `modellchat-${name}-${dev}-v1.png`, skeleton, state);
    }
  }
})();
