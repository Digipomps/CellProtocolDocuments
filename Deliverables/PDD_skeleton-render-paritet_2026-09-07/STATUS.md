# STATUS — skeleton render paritet

- surfaces: binding, gui, porthole, skeleton, web
- tags: gui, paritet, rendering, skeleton, ytelse

## Porter
- G1: godkjent 2026-09-15 (Kjetils ord: «G1 er godkjent»)
- G1-GUI: venter        (rendret bilde godkjent — bare for GUI-oppgaver)
- G2: venter        (plan godkjent; arbeidspakker 1:1 mot bladformål)
- G3: venter        (akseptanse: forventning mot faktisk, alle avledede tester grønne)

Sett en port til `godkjent <dato>` kun når Kjetil har sagt det. `purpose_dev.py validate <mappe>` nekter porter uten artefakter.

## Planbytter (dato — hvorfor)
-

## Logg
- 2026-09-07: opprettet
- 2026-09-07: FORMAALSSPEC §0–§3, §5, §6 fylt ut fra kildelesing. Hovedfunn:
  paritetsmatrisen (`SkeletonElementParityMatrix.v1.json`, 24 caser) leses av
  CellScaffold-tester og to Playwright-spec-er, men av ingen fil i Binding —
  native-siden er `source-inspected-explicit-switch`, altså en påstand fra
  kildelesing, ikke en måling.
- 2026-09-07: `handoff/README.md` skrevet for Codex (ChatGPT 6 Astra).
- 2026-09-07: Kjetil definerte «likt»: samme elementer, rekkefølge, tekst,
  tilstand og handlinger; nedskrevet toleranse for typografi og spacing; lett
  gjenkjennelig samme flate. Skrevet ut som tre nivåer i §3b.
- 2026-09-07: Telte roller på nytt og fant to feil i egen rad 2:
  det er **34** roller i bruk, ikke 19, og det er **ikke** null tolket av web.
  `skeleton-runtime.js:4027` legger `style-role-<navn>` på hver rolle, 61 roller
  har CSS-regel, 5 av dem er i bruk i appen. `SkeletonStyleParity.webOnlyRoles`
  kjenner bare 3 JS-spesialbehandlede og stryker de 5 som «støy» — normalisatoren
  skjuler altså et ekte web/native-avvik. Ny avledet test
  `test.parity.style-parity-knows-web-css`, og den er nå første implementasjons-
  steg i overleveringen.
- 2026-09-07: `codex-local` MCP: **jeg tok feil om årsaken.** Astra er på plass —
  Kjetil sendte skjermdump av ChatGPT-appen som kjører den. Det er MCP-serveren
  som er eldre enn appen: den avviser `gpt-6-astra`, og kontoen aksepterer ingen
  fallback (`gpt-5.2-codex` og `gpt-5.1-codex` gir kontofeil). Codex ligger inne
  i ChatGPT.app og nås via symlinken `~/.local/bin/codex`, som en oppgradering
  kan la peke på forrige bundle. Diagnose i én kommando ligger i
  `handoff/README.md`. Arbeidet er ikke blokkert — Codex kjøres fra appen.
- 2026-09-07: Kjetil svarte på §6: **web slik den er i dag er fasit**; de seks
  foreslåtte rollene blir normative (`personal-list-row`,
  `personal-key-value-block`, `personal-hero`, `personal-card`,
  `personal-section-header`, `tabstrip`); og `SkeletonStyleParity` skulle rettes
  med én gang, utenfor porten.
- 2026-09-07: Presiserte egen påstand. `classify` stryker alt utenfor
  `agreedRoles` uansett `TokenKind`, så strykingen var riktig — feilen var
  **merkelappen** (`.unclaimed` i stedet for `.webOnly`) og dermed funnstrømmen.
  Forrige formulering overdrev.
- 2026-09-07: Fiksen skrevet, ligger i `patch/`:
  `SkeletonStyleParity.webOnlyRoles` splittet i `webJavaScriptRoles` (3) og
  `webStylesheetRoles` (61), pluss ny `SkeletonStyleParityCSSDriftTests` i
  CellScaffold som skanner stilarkene og feiler med differansen.
  **Ikke kompilert** — ingen Swift-verktøykjede i Cowork-VM-en.
  `patch/apply.sh --apply` lager worktrees fra origin/main, bygger og tester.
  Eier: kjetil, én kommando.
- 2026-09-07: **venter på Kjetil (G1)**: ordet på at FORMAALSSPEC.md er godkjent.
  Ingen av de tre gjenstående §6-spørsmålene blokkerer den.
- 2026-09-15: **G1 godkjent av Kjetil.** Samtidig prioritert: bro først —
  «uten bridge er hele Binding / HAVEN app ubrukelig». Paritetstesting starter
  når broen er verifisert oppe, robust og effektiv.
