# STATUS — correspondence varsel hendelsesbasert

- surfaces: bridge, cell, gui
- tags: agent, correspondence, hendelse, macos, varsler

## Porter
- G1: godkjent 2026-09-12 (Kjetil: «10 og 9 … og G1»; spm. 9 → egen identitet, spm. 10 → tilstand i cellen)
- G1-GUI: godkjent 2026-09-12 (Kjetil: «GUI ser fint ut så vi bruker det» — notification-new-message-v1, menu-new-message-v2, menu-correspondence-unreadable-v1, admin-window-correspondence-v1)
- G2: godkjent 2026-09-12 (Kjetil: «Gå videre med G2»)
- G3: venter        (akseptanse: forventning mot faktisk, alle avledede tester grønne)

Sett en port til `godkjent <dato>` kun når Kjetil har sagt det. `purpose_dev.py validate <mappe>` nekter porter uten artefakter.

## Planbytter (dato — hvorfor)
-

## Logg

- 2026-09-15 (runde 2): **WP-S1 grunnlag og testsynkronisering committet; ikke verifisert ved kjøring.** Commit 1: `2de94770ccebc16e4ba573a2272a97de79bbf893` (inkl. WP-S1-endringen i `Staging_Deployment.md`); commit 2: `f729d1feb96ff17027468687d6da83ef7fe4bd95`. Siste barriere lagt til i `testRecipientFeedExcludesOtherRecipientsSendAndAck:1505`; payload, antall, rekkefølge og adgangsavslag bevart statisk. Swift-parsing exit 0, rent worktree; rapport og patch flyttet til `evidence/wp-s1/`. [DIAGNOSE-20260915.md](evidence/wp-s1/DIAGNOSE-20260915.md) dokumenterer utfallet. Kjetils neste bounded-kjøring må gi 25 tester, 0 feil; ingen bygg eller tester kjørt i runde 2.

- 2026-09-15: **WP-S1-patch ikke anvendt; avventer avklaring om ucommittet grunnlag.** Riktig gren, men arbeidstreet har eksisterende produktkode-, test- og dokumentasjonsendringer samt usporet rapport, i strid med anvendelsesoppdragets krav om rent tre. `git apply --check` passerer; statisk kravtabell og én gjenstående leveringsbarriere før andre mottakeres tomhetsmåling er dokumentert i [DIAGNOSE-20260915.md](evidence/wp-s1/DIAGNOSE-20260915.md). Ingen ny SHA, syntakssjekk, bygg eller testkjøring; Kjetils avklaring om asynkron levering er registrert ordrett der. Krav ved Kjetils neste kjøring: 25 tester, 0 feil.

- 2026-09-14 kl. 23:03: **WP-S1 målt for første gang — rød.** Kjetil kjørte bounded-skriptet etter at cache-sperren ble ryddet (første forsøk kl. 20:20 ga `exit=64`: `haven-swiftpm.sh` nektet å bruke en gammel cache-mappe uten eierskapsmerke — ikke en testfeil). Måling: `Executed 25 tests, with 10 failures`, exit=1. 16 baseline grønne (ingen regresjon), 6 av 9 nye tester røde. Alle tre grønne nye er negative tester; alle seks røde krever at en hendelse faktisk ankommer — en feed som ikke leverer noe består de negative trivielt. To årsakshypoteser lest i koden og forkastet (`operation` finnes i resultatobjektet; ack returnerer `"acknowledged"` som er i emitterings-allowlista). Gjenstående spor: `emitCorrespondenceFlow` nil på testenes init-vei — men det forklarer ikke at `send` ankommer og `ack` ikke gjør det, så det er minst to defekter. Full tabell i `TESTRESULT.md#auth`. Diagnose-/rettejobb `wp-s1-diagnose-20260915` lagt i `_losen-queue`; den kan ikke bygge, så Kjetil må kjøre bounded-skriptet på nytt etterpå.

- 2026-09-12: opprettet
- 2026-09-12: Iterasjon 1 av FORMAALSSPEC.md skrevet fra kode (HavenAgentD origin/main 551d37a og gren claude/varsler-og-behandlingssted-20260911, CellScaffold AssistantCorrespondenceCell, CellProtocol BridgeBase). Tre mockups i images/. Kø-poster: HD-0069 (denne), HD-0070 (Launch Constraint-blokkeringen). Venter G1 og G1-GUI fra Kjetil; fem spørsmål i §6.
- 2026-09-12: §6 besvart av Kjetil: hver melding varsles; menyens timer fjernes; grenen fra 11.9 tas inn som grunnlag (HD-0071); begge principaler; Launch Constraint = HD-0070. Iterasjon 2. Venter G1 og G1-GUI.
- 2026-09-12: Iterasjon 3 etter Kjetils presisering: én menylinjeapp som bro-klient mot agenten (bridgehead finnes allerede i AgentControlBridgeServer), varsler bare i OS-ets varslingssenter, oversikt/handling i adminflaten; «NY POST»-seksjonen trukket. Nye bilder: menu-new-message-v2, admin-window-correspondence-v1. IPC/delt minne-transport: dokumentert i Book 08, ikke implementert — egen kandidat. Venter G1 og G1-GUI + §6 spm. 6–7.
- 2026-09-12: Iterasjon 4. G1-GUI godkjent på Kjetils ord. Treet delt: `bridge-exists` (at broen finnes) mot det den løser (`event-to-app`, `admin-overview-and-action`). §1b løsningsvalg A–F; §1c validering med Fable-tråd pågår. A16 rettet: fire transporter funnet; Multipeer-bro ikke funnet i CellProtocol-utsjekken (recalled fra Kjetil). Venter G1.
- 2026-09-12 kveld: Iterasjon 5 etter Fable-validering (VALIDERING.md): «A med rettelser». Tre auditrader var feil (A6, A8, A9 — to av dem lest fra lokal main / kuttet utdata), D1 er contradicted og blir server-arbeid (`recipient-scoped-events`), tre designavgjørelser lagt i treet (`app-identity`, `change-signal-inside-agent`, «Ignorer i dag» §6 spm. 10). Venter G1.
- 2026-09-12 kveld: **G1 godkjent** av Kjetil (svar 9 → a, 10 → ii; entitetstilhørighet for app-identiteten ført som spm. 11 med standard). Går til P2: PLAN.md, dataflow.md, contract/.
- 2026-09-12 kveld: PLAN.md (WP0, WP-S1, WP-D1b, WP-D1c, WP-A1–A4, WP-M0–M2, WP-C, WP-V, WP-Docs), dataflow.md (12 kanter, 8 nye) og contract/ (utkast til `agent/challenges`-kontrakt) skrevet. Venter G2.
- 2026-09-12 kl. 19:40: Kjetil forkaster SwiftBar-pluginen (HD-0022 → forkastet; deploy-status i appen = HD-0075, egen G1-GUI), flagger at GUI-et kan trenge mer tanke, og peker på `ScannerPeerTransport` som Multipeer-transporten (A16b rettet — min feil, kuttet utdata; lesson registrert). Iterasjon 7. Venter G2.
- 2026-09-12 kl. 20:15: **G2 godkjent.** GUI-retning fra Kjetil notert for HD-0075: adminflaten er for scaffold-admin et sted for status, for å se meldinger, og først og fremst en flate for utviklerarbeidsflyt. P3 startet: WP0-baseline (`evidence/wp0/baseline.sh`) og WP-S1-jobben (`handoff/wp-s1-recipient-feed.*`) klare; `codex-local danger-full-access` blokkert av klassifikatoren, så forberedelsen (worktree + detached baseline + køjobb) ligger som KJØR-SELV-post 0 på HD-0069 for Kjetil.
- 2026-09-12 kl. 22:10: WP0 målt (HavenAgentD 241/48 grønne; CellScaffold filtrert 16/16 grønne). WP-S1 skrevet av Codex (9 tester), gransket av Claude (`evidence/wp-s1/GRANSKNING.md`): klar for bounded bygg — post 0 på HD-0072 (Kjetil). TESTRESULT.md opprettet (#build). VALIDERING-presedenser rettet (lest fra skittent tre).
- 2026-09-15 08:45Z: **Kjetils avklaring av WP-S1-testkravet** (ordrett): «Godta asynkron leveringsbarriere i WP-S1; behold payload, antall, rekkefølge og adgangsavslag.» Codex-jobb `wp-s1-anvend-patch-20260915` anvender `WP-S1-foreslaatt-testsynkronisering.patch` i worktreet; deretter kjører Kjetil `HAVEN-Deploy/_handoff/HD-0072/KJOR-SELV-wp-s1-bounded-test.sh --run` (krav 25 tester, 0 feil). Valget kom via Valgbenk-artefaktet (v-s1).
- 2026-09-15 10:15Z: **WP-S1 grønn lokalt** — Kjetil kjørte bounded-testen: 25 tester, 0 feil (`evidence/wp-s1/RESULT-20260915T115511.md`). PR-tekst skrevet (`HAVEN-Deploy/_handoff/HD-0072/PR-corr-varsel-wp-s1.md`). Neste: Kjetil pusher `pdd/corr-varsel-recipient-feed` og åpner PR; grenen må oppdateres mot main `6c391437` (bygger på `649255bb`).
