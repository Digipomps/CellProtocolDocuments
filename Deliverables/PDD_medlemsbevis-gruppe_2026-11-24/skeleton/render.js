// Renders the G1-GUI images for PDD medlemsbevis-gruppe with the real CellScaffold web renderer
// (Public/js/skeleton-runtime.js, porthole-webo.css, admin-skeleton.css), same harness as
// PDD_informasjonssystemer-gruppeentitet. Three surfaces: the member's «Medlemsbevis», the
// moderator's queue, and the one-vote-per-credential example. Every keypath under membership.*,
// moderation.* and vote.* is a proposal; none exists in CellScaffold today.
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
const itemWhen = (keypath, equals) => ({ visibility: { when: { equals, keypath, scope: 'item' } } });
const card = (elements, extra = {}) => ({ VStack: { spacing: 10, elements, modifiers: {
  padding: 16, background: '#FFFFFF', cornerRadius: 12, borderWidth: 1, borderColor: '#E2E8F0', maxWidthInfinity: true, ...extra } } });
const secondary = { background: '#FFFFFF', borderColor: '#CBD5E1', borderWidth: 1, cornerRadius: 6, foregroundColor: '#334155' };
const danger = { background: '#FFFFFF', borderColor: '#FCA5A5', borderWidth: 1, cornerRadius: 6, foregroundColor: red };
const list = (keypath, rowElements) => ({ List: { elements: [], keypath, selectionMode: 'none', modifiers: { itemSpacing: 8 },
  flowElementSkeleton: { VStack: { spacing: 4, elements: rowElements } } } });
const row = (l, r, ro = {}) => ({ HStack: { spacing: 8, elements: [key(l, { fontWeight: '700' }), { Spacer: {} }, key(r, { fontSize: 13, foregroundColor: teal, ...ro })] } });
const buttons = (...b) => ({ HStack: { spacing: 8, modifiers: { wrap: true }, elements: b } });
const btn = (keypath, label, modifiers) => ({ Button: { keypath, label, payload: {}, ...(modifiers ? { modifiers } : {}) } });

// ---------- 1. Medlemsbevis (medlemmet) ----------
const member = { VStack: { spacing: 14, elements: [
  card([
    text('Medlemsbevis', { fontStyle: 'title2', fontWeight: '700' }),
    key('membership.state.groupName', { fontSize: 14, foregroundColor: muted }),
    text('Beviset viser at gruppa har godtatt deg som én entitet i gruppa. Det gir ingen tilgang alene; en celle må kreve det i avtalen sin.', { fontSize: 13, foregroundColor: muted }),
  ]),
  // tom: velg vei
  card([
    text('Hvordan vil du bli godtatt?', { fontStyle: 'headline' }),
    card([
      text('Bevis med eID (fødselsnummer eller D-nummer)', { fontWeight: '700' }),
      text('Du blir godtatt med en gang. Gruppa lagrer aldri nummeret ditt, bare et pseudonym som gjelder i denne gruppa. Ett nummer kan ha ett medlemskap.', { fontSize: 13, foregroundColor: muted }),
      key('membership.state.eidNote', { fontSize: 12, foregroundColor: amber }),
      btn('membership.eid.start', 'Fortsett med eID'),
    ], { padding: 12, background: '#F8FAFC' }),
    card([
      text('Be en moderator', { fontWeight: '700' }),
      text('En moderator ser søknaden din og godtar eller avviser den. Denne veien sjekker ikke om du allerede er medlem med en annen identitet.', { fontSize: 13, foregroundColor: muted }),
      btn('membership.moderator.request', 'Send søknad til moderator', secondary),
    ], { padding: 12, background: '#F8FAFC' }),
  ], when('membership.state.phase', 'choose')),
  // samtykke før eID
  card([
    text('Før du går videre til eID', { fontStyle: 'headline' }),
    text('Dette lagrer gruppa hvis du fortsetter:', { fontSize: 14 }),
    list('membership.state.stored', [ key('line', { fontSize: 14 }) ]),
    text('Dette lagres ikke:', { fontSize: 14 }),
    list('membership.state.notStored', [ key('line', { fontSize: 14, foregroundColor: muted }) ]),
    text('Medlemsbeviset du får inneholder ikke pseudonymet. Melder du deg ut, slettes pseudonymet med en gang.', { fontSize: 13, foregroundColor: muted }),
    buttons(btn('membership.eid.consent', 'Jeg godtar, gå til eID'), btn('membership.eid.cancel', 'Avbryt', secondary)),
  ], when('membership.state.phase', 'consent')),
  // venter
  card([
    text('Søknaden venter på en moderator', { fontStyle: 'headline', foregroundColor: amber }),
    key('membership.state.pendingDetail', { fontSize: 14 }),
    btn('membership.moderator.withdraw', 'Trekk søknaden', secondary),
  ], { ...when('membership.state.phase', 'pending'), borderColor: '#FCD34D' }),
  // avvist
  card([
    text('Søknaden ble avvist', { fontStyle: 'headline', foregroundColor: red }),
    key('membership.state.rejectedDetail', { fontSize: 14 }),
    buttons(btn('membership.eid.start', 'Prøv med eID'), btn('membership.moderator.request', 'Søk på nytt', secondary)),
  ], { ...when('membership.state.phase', 'rejected'), borderColor: '#FCA5A5' }),
  // allerede medlem
  card([
    text('Dette nummeret er allerede medlem', { fontStyle: 'headline', foregroundColor: amber }),
    key('membership.state.duplicateDetail', { fontSize: 14 }),
    text('Flytter du medlemskapet, trekkes det gamle beviset tilbake og du får et nytt her. Moderator får beskjed. Det vanligste er en ny eller tapt telefon.', { fontSize: 13, foregroundColor: muted }),
    buttons(btn('membership.eid.move', 'Flytt medlemskapet hit'), btn('membership.eid.cancel', 'Avbryt', secondary)),
  ], { ...when('membership.state.phase', 'duplicate'), borderColor: '#FCD34D' }),
  // godtatt
  card([
    { HStack: { spacing: 8, elements: [ text('Du er medlem', { fontStyle: 'headline', foregroundColor: teal }), { Spacer: {} }, key('membership.state.credential.status', { fontSize: 13, foregroundColor: teal }) ] } },
    key('membership.state.credential.issuer', { fontSize: 14 }),
    key('membership.state.credential.via', { fontSize: 14 }),
    key('membership.state.credential.validity', { fontSize: 13, foregroundColor: muted }),
    key('membership.state.credential.usedBy', { fontSize: 13, foregroundColor: muted }),
    buttons(btn('membership.credential.show', 'Vis beviset', secondary), btn('membership.leave', 'Meld deg ut', danger)),
  ], { ...when('membership.state.phase', 'member'), borderColor: '#99F6E4' }),
  card([
    text('Hva beviset ikke garanterer', { fontStyle: 'headline' }),
    list('membership.state.limits', [ key('line', { fontSize: 13, foregroundColor: muted }) ]),
  ]),
] } };

const limits = [
  { line: 'Moderator-veien hviler på moderatorens skjønn og hindrer ikke at én person har to identiteter som medlem.' },
  { line: 'eID-veien gjelder bare norske numre. Med dobbelt statsborgerskap har du to nasjonale identifikatorer.' },
  { line: 'Samme person kan få nytt nummer (D-nummer til fødselsnummer, endret juridisk kjønn).' },
  { line: 'Den som drifter gruppa kan regne ut pseudonymet. Beviset er ikke anonymt.' },
];
const base = { groupName: 'Informasjonssystemer (Ifi, UiO)', limits,
  eidNote: 'Staging: bare test-eID med syntetiske numre. Ekte ID-porten er ikke koblet til.' };
const memberStates = {
  'medlem-velg': { membership: { state: { ...base, phase: 'choose' } } },
  'medlem-samtykke': { membership: { state: { ...base, phase: 'consent',
    stored: [ { line: '• Et pseudonym for nummeret ditt, bare gyldig i Informasjonssystemer' }, { line: '• Tidspunktet du ble godtatt, og at det skjedde med eID' } ],
    notStored: [ { line: '• Fødselsnummeret eller D-nummeret ditt' }, { line: '• Navnet ditt fra eID og innloggingsbeviset fra eID-leverandøren' } ] } } },
  'medlem-venter': { membership: { state: { ...base, phase: 'pending',
    pendingDetail: 'Sendt 25.11.2026 kl. 09:52. Moderator: Kjetil. Du får beskjed her når søknaden er avgjort.' } } },
  'medlem-avvist': { membership: { state: { ...base, phase: 'rejected',
    rejectedDetail: 'Kjetil avviste søknaden 25.11.2026: «Jeg kjenner ikke igjen denne identiteten. Bruk eID, eller skriv til meg.»' } } },
  'medlem-allerede': { membership: { state: { ...base, phase: 'duplicate',
    duplicateDetail: 'Nummeret du beviste med eID er allerede knyttet til et medlemskap fra en annen identitet (godtatt 20.11.2026).' } } },
  'medlem-godtatt': { membership: { state: { ...base, phase: 'member', credential: {
    status: 'gyldig', issuer: 'Signert av Informasjonssystemer (Ifi, UiO)', via: 'Godtatt med eID (norsk nummer)',
    validity: 'Gyldig til 30.06.2027 · sjekkes mot gruppas statusliste', usedBy: 'Brukes av: Avstemming om temaer for seminaret' } } } },
};

// ---------- 2. Moderatorkøen ----------
const moderation = { VStack: { spacing: 14, elements: [
  card([
    text('Medlemmer i Informasjonssystemer', { fontStyle: 'title2', fontWeight: '700' }),
    key('moderation.state.summary', { fontSize: 14, foregroundColor: muted }),
    text('Som moderator kan du bare godta og trekke tilbake medlemskap. Andre roller gis av eierne.', { fontSize: 13, foregroundColor: muted }),
  ]),
  card([
    text('Søknader', { fontStyle: 'headline', foregroundColor: amber }),
    list('moderation.state.requests', [
      row('who', 'when', { foregroundColor: muted }),
      key('note', { fontSize: 14 }),
      buttons(btn('moderation.admit', 'Godta med passkey'), btn('moderation.reject', 'Avvis', danger)),
      text('Du kan ikke godta din egen søknad.', { fontSize: 12, foregroundColor: muted, ...itemWhen('own', true) }),
    ]),
  ], { ...when('moderation.state.hasRequests', true), borderColor: '#FCD34D' }),
  card([
    text('Ingen søknader venter.', { fontSize: 14, foregroundColor: muted }),
  ], when('moderation.state.hasRequests', false)),
  card([
    text('Meldinger', { fontStyle: 'headline' }),
    list('moderation.state.notices', [ key('when', { fontSize: 13, foregroundColor: muted }), key('what', { fontSize: 14 }) ]),
  ], when('moderation.state.hasNotices', true)),
  card([
    { HStack: { spacing: 8, elements: [ text('Medlemmer', { fontStyle: 'headline' }), { Spacer: {} }, key('moderation.state.count', { fontSize: 13, foregroundColor: muted }) ] } },
    list('moderation.state.members', [
      row('who', 'via'),
      { HStack: { spacing: 8, elements: [ key('detail', { fontSize: 13, foregroundColor: muted }), { Spacer: {} },
        btn('moderation.revoke', 'Trekk tilbake', { ...danger, fontSize: 13, ...itemWhen('revocable', true) }) ] } },
    ]),
  ]),
] } };
const members = [
  { who: 'Ola Student', via: 'eID', detail: 'godtatt 20.11 · gyldig til 30.06.2027', revocable: true },
  { who: 'Kari Testesen', via: 'moderator', detail: 'godtatt av Kjetil 21.11 · gyldig til 30.06.2027', revocable: true },
  { who: 'Testkonto 3', via: 'eID', detail: 'meldte seg ut 22.11 · pseudonymet er slettet', revocable: false },
];
const moderationStates = {
  'moderator-ko': { moderation: { state: { summary: 'Moderator: Kjetil · 2 aktive medlemmer · 2 søknader',
    hasRequests: true, requests: [
      { who: 'Per Prøvesen', when: 'i dag 09:52', note: 'Ber om medlemskap via moderator. Melding: «Masterstudent fra høsten, veileder er Petter.»', own: false },
      { who: 'Identitet …a91f', when: 'i dag 10:05', note: 'Ber om medlemskap via moderator. Ingen melding.', own: false },
    ],
    hasNotices: true, notices: [ { when: '24.11 18:20', what: 'Ola Student flyttet medlemskapet sitt til en ny identitet med fersk eID. Det gamle beviset er trukket tilbake.' } ],
    count: '2 aktive', members } } },
  'moderator-tom': { moderation: { state: { summary: 'Moderator: Kjetil · 2 aktive medlemmer',
    hasRequests: false, requests: [], hasNotices: false, notices: [], count: '2 aktive', members } } },
};

// ---------- 3. Avstemming: én stemme per bevis (eksempel for studentene) ----------
const vote = { VStack: { spacing: 14, elements: [
  card([
    text('Avstemming: temaer for seminaret', { fontStyle: 'title2', fontWeight: '700' }),
    text('Krever medlemsbevis fra Informasjonssystemer. Én stemme per medlemsbevis, ikke per identitet.', { fontSize: 14, foregroundColor: muted }),
  ]),
  card([
    text('Resultat så langt', { fontStyle: 'headline' }),
    list('vote.state.options', [ row('label', 'votes', { foregroundColor: ink }) ]),
    key('vote.state.counted', { fontSize: 13, foregroundColor: muted }),
  ]),
  card([
    text('Du har stemt', { fontStyle: 'headline', foregroundColor: teal }),
    key('vote.state.mine', { fontSize: 14 }),
    text('En ny identitet med samme eID-nummer får ikke stemme på nytt. Moderator-godtatte medlemmer telles som egne bevis, så samme person kan i prinsippet ha to stemmer der.', { fontSize: 13, foregroundColor: muted }),
  ], { borderColor: '#99F6E4' }),
] } };
const voteStates = {
  'avstemming-stemt': { vote: { state: {
    options: [ { label: 'Unik representasjon', votes: '2 stemmer' }, { label: 'Deling av dokumenter', votes: '1 stemme' } ],
    counted: '3 stemmer fra 3 gyldige medlemsbevis · 1 forsøk avvist (samme eID-nummer som en avgitt stemme)',
    mine: 'Unik representasjon, 25.11 kl. 10:12' } } },
};

const surfaces = [
  ['medlemsbevis', member, memberStates, ['Medlemsbevis', 'Hva beviset ikke garanterer']],
  ['moderator', moderation, moderationStates, ['Medlemmer i Informasjonssystemer']],
  ['avstemming', vote, voteStates, ['Én stemme per medlemsbevis']],
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
    'medlem-velg': ['Fortsett med eID', 'Send søknad til moderator'],
    'medlem-samtykke': ['Dette lagres ikke', 'Jeg godtar, gå til eID'],
    'medlem-venter': ['Søknaden venter på en moderator'],
    'medlem-avvist': ['Søknaden ble avvist'],
    'medlem-allerede': ['Flytt medlemskapet hit'],
    'medlem-godtatt': ['Du er medlem', 'Meld deg ut', 'Godtatt med eID'],
    'moderator-ko': ['Godta med passkey', 'Per Prøvesen', 'flyttet medlemskapet'],
    'moderator-tom': ['Ingen søknader venter'],
    'avstemming-stemt': ['1 forsøk avvist'],
  };
  const notIn = {
    'medlem-velg': ['Du er medlem', 'Dette nummeret er allerede medlem', 'Søknaden venter'],
    'medlem-godtatt': ['Hvordan vil du bli godtatt?', 'Søknaden ble avvist'],
    'moderator-tom': ['Godta med passkey', 'Meldinger'],
    'moderator-ko': ['Ingen søknader venter', 'Du kan ikke godta din egen søknad'],
  };
  for (const [slug, skeleton, states, baseChecks] of surfaces) {
    fs.writeFileSync(path.join(outSkeleton, `${slug}.v1.json`), JSON.stringify(skeleton, null, 2) + '\n');
    fs.writeFileSync(path.join(outSkeleton, `${slug}-tilstander.v1.json`), JSON.stringify(states, null, 2) + '\n');
    for (const [w, dev] of [[1280, 'laptop'], [390, 'iphone']])
      for (const [name, st] of Object.entries(states)) {
        const t = await shot(w, `${name}-${dev}-v1.png`, skeleton, st, [...baseChecks, ...(checks[name] || [])]);
        for (const m of notIn[name] || []) if (t.includes(m)) throw new Error(`${name}-${dev}: «${m}» should be hidden`);
      }
  }
  console.log('ok');
})().catch((e) => { console.error(e); process.exit(1); });
