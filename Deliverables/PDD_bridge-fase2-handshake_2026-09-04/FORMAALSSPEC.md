# Formålsspesifikasjon — bridge fase 2 (handshake-scope, kanaltak)

Oppgavemappe: `PDD_bridge-fase2-handshake_2026-09-04` · Opprettet 2026-09-04 · Iterasjon 2 (§6 besvart; G1-ordet gjenstår)

> Regel: ingen plan før G1 er godkjent av Kjetil. Et dokument om leveransen
> teller aldri som leveransen.

## 0. Intensjon (ordrett) og brief-audit

> Vurder om det kan være nyttig om celler i seg selv kan bevise sin autensitet.
> Jeg tenker det kan være nyttig å vite helt sikkert at den cellen som bruker
> set/get eller andre ting er den man forventer. Med samme mekanisme som
> Identity bruker men knyttet til celle. Slik at man ikke kan lure inn en feil
> celle i en eller annen sammenheng. Kanskje også for å få bedre sikkerhet over
> bridge? *(2026-08-28)*

> Ja skriv det og fortsett med fase 2 *(2026-09-04)*

**Tolkning som må bekreftes ved G1:** «fase 2» leses som **bridge fase 2** —
`native-porthole/session`-ruten med handshake-scope og kanaltak, port nr. 2 i
Samlet_Oversikt 2026-08-24 — fordi det var den åpne porten vurderingsnotatet
pekte på. Ikke PalazzoScaffold fase 2. **Status 2026-09-04:** Kjetil besvarte de
fire designspørsmålene i §6 med bridge-lesningen lagt til grunn.

| Påstand / antatt kapabilitet | Audit | Kilde |
|---|---|---|
| «Fase 2» er definert: `native-porthole/session` er P0-resten etter fase 1, med to åpne spørsmål (scope, kanaltak) | retrieved | `CellScaffold/Documentation/Operations/Codex_Handoff_Bridge_Multiplex_Host_Route_2026-08-20.md` («Gjenstår før produksjon», «Åpne spørsmål til Kjetil»); `Samlet_Oversikt_2026-08-24.md` port 2; tokenplan-gate 2 |
| Klientsiden for v2-multipleks er komplett i CellProtocol (pool, sesjon, kanaler, kontinuitet) | retrieved | `CellProtocol/Sources/CellBase/Cells/Bridging/BridgeMultiplexing.swift`; `CellResolver.swift:2167–2249`; 18 multiplekstester grønne per handoff-dok |
| Fase 1 (AdminScaffold `/session`) er implementert og ligger i **gjeldende arbeidstre** | retrieved | `CellScaffold/Sources/ScaffoldKit/AdminScaffoldBridgeRoutes.swift:28,86,91,315,418` (`AdminScaffoldMultiplexSessionRegistry`, tak 64, `registerMultiplexSessionRoute`); `Tests/AppTests/AdminScaffoldBridgeMultiplexRouteTests.swift` finnes. Checkout: `claude/working-tree-salvage-20260829` (lest fra `.git/HEAD` som fil) |
| Fase 1 **er** på CellScaffold `origin/main` (`dd72f4ed` «Add opt-in v2 bridge multiplexing…»), og `BridgeMultiplexing.swift` er på CellProtocol `origin/main` | retrieved | Codex read-only git-verifikasjon 2026-09-04 (`git ls-tree origin/main`, `git log -S registerMultiplexSessionRoute`); arbeidstrærne står på andre grener (`claude/working-tree-salvage-20260829`, `claude/perspective-entities-invite-20260822`) |
| Admin-handshaken i dag: HMAC-SHA256 med delt nøkkel; signerer keyID/clientID/timestamp/nonce/method/**path**/scheme/authority; replay-nonce; clock-skew-tak; **ingen scope-felt** | retrieved | `CellScaffold/Sources/ScaffoldKit/AdminBridgeHandshakeAuthentication.swift:325–520` |
| Admin-handshaken er én bred delt nøkkel, ikke per-enhet signeringsbevis — kjent P1-residual | retrieved | `CellProtocolDocuments/Deliverables/HAVEN_Cross_Repo_Robustness_Audit_2026-07-13.md` (~linje 1922) |
| native-porthole-upgrade i dag: publisher-scopet (`pubId` + allowlist), resolver-utstedt **signert kontrakt** med `capability_grants`, expiry, issuer-sjekk og `bridge_endpoint`-binding, validert ved socket-upgrade | retrieved | `CellScaffold/Sources/App/Services/SproutResolverCompatibility.swift:839–880`; `VaporSproutResolver.swift:60–90` |
| Kanaltak: CellProtocol-default 128 per sesjon; fase 1 valgte 64 for AdminScaffold («én klient skal ikke tømme verten fra ett socket») | retrieved | `BridgeMultiplexing.swift` (`maximumChannels: 128`); `AdminScaffoldBridgeRoutes.swift:91` |
| Reconnect er et bekreftet hull: `resumeFromSequence` har ingen produsent/konsument; socket-tap gjør kanaldelegater foreldreløse uten varsel | retrieved | handoff-dok «Svar på de tre kjente hullene» pkt. 1, med fil:linje |
| `sendSetValueState` svelges av multipleks-sesjonene (oppsettsfeil når ikke kanalene) | retrieved | samme, pkt. 2 (`BridgeMultiplexing.swift:610,1145`) |
| Ingen backpressure/kreditt per kanal; head-of-line blocking mulig | retrieved | samme, pkt. 3 |
| Signatur alene beviser ikke «riktig celle»; bindingen (hvem sier nøkkel K er celle X, og hva X er) gjør jobben | retrieved | `CellProtocolDocuments/Deliverables/Celle_Autentisitet_Vurdering_2026-09-04.md` §3; audit ~1137/1484 |

## 1. Formålstre

Kjernen i én setning: **én fysisk socket per (identitet, vert) skal bære mange
logiske kanaler uten at noen sikkerhetsgrense blir svakere enn i dag — og
handshake-kontrakten som nå låses skal ha plass til celle-nivå bevis, så
celle-autentisitet ikke krever redesign senere.**

| purposeRef | Tittel | Forelder | Goal (outcome) | Verifier | Status |
|---|---|---|---|---|---|
| `purpose://candidate.bridge-fase2.root` | Multipleks uten svekket grense | `purpose://access.audit.privacy` | `native-porthole/session` bærer N logiske kanaler over én socket; hvert avslag er typed; ingen kontroll som finnes i dag er fjernet eller svekket | Hele §5-matrisen grønn | candidate |
| `purpose://candidate.bridge-fase2.session-scope-explicit` | Handshake-scope er eksplisitt | root | Sesjonskredensialen/kontrakten erklærer hvilket scope den gir (hvilke flater/kanaler den kan åpne). En kredensial for én flate kan ikke åpne kanaler utenfor sitt scope; «ingen scope-felt» tolkes fail-closed som *bare* legacy-ruter, aldri som alt. *(Besluttet 2026-09-04: eget scope-felt)* | Negative tester: kontrakt uten scope mot `/session`; kontrakt med scope A mot flate B | candidate |
| `purpose://candidate.bridge-fase2.channel-authz-per-open` | Autorisasjon per kanalåpning | root | Hver `openChannel` autoriseres i `channelFactory` mot kontraktens grants — samme mønster som fase 1: avvist kanal gir `channelRejected`, resten av sesjonen overlever | Test: to kanaler, én autorisert + én utenfor scope; den første fortsetter å levere | candidate |
| `purpose://candidate.bridge-fase2.no-weakened-upgrade` | Upgrade-kjeden beholder dagens styrke | root | Sesjonsnivå-validering på `native-porthole/session` beholder minst: kontraktsignatur, expiry, issuer-sjekk, `bridge_endpoint`-binding, publisher-allowlist. Ingen svekkelse for å «få det til å virke» | Inspeksjon + negative tester: utløpt kontrakt, feil issuer, feil endpoint, forfalsket signatur, replay | candidate |
| `purpose://candidate.bridge-fase2.cell-proof-fields-reserved` | Kontrakten har plass til celle-bevis | root | Handshake-/kanalkontrakten (versjonert JSON) definerer valgfrie felter for celle-nivå bevis begge veier: aktør-celle fra klient ved `openChannel`, vert-celle-proof over transkript med nonce fra scaffold. Fase 2 implementerer **ikke** bevisene — bare feltene, versjoneringen og fail-closed-atferden når policy krever felt som mangler. *(Besluttet 2026-09-04: feltene reserveres)* | Kontraktfixtures: felter til stede/utelatt/krevd-men-mangler; dekoding avviser ikke ukjente valgfrie felter | candidate |
| `purpose://candidate.bridge-fase2.channel-cap-explicit` | Kanaltaket er besluttet og håndhevet | root | Taket per fysisk sesjon er konfigurerbart med default **64** *(besluttet 2026-09-04; fase 1-presedens, under CellProtocols 128)*. Kanal N+1 får typed avslag; de N består | Test: fyll til taket, åpne én til, verifiser avslag + at eksisterende kanaler leverer | candidate |
| `purpose://candidate.bridge-fase2.socket-loss-explicit` | Socket-tap er en beslutning, ikke et uhell | root | V1-atferd *(besluttet 2026-09-04)*: klienten bygger broene på nytt; hver kanaldelegat får eksplisitt closed-signal; `resumeFromSequence` fjernes eller implementeres — ikke halvdeklarert | Test: dropp socket med to aktive kanaler; begge delegater varsles; ingen foreldreløse celleregistreringer på verten | candidate |
| `purpose://candidate.bridge-fase2.setup-errors-reach-channels` | Oppsettsfeil når kanalene | root | `sendSetValueState`-signal fannes ut til alle aktive kanaldelegater i stedet for å svelges | Test som utløser transport-oppsettsfeil og observerer varsel på hver kanal | candidate |

Backpressure/kreditt per kanal er bevisst **utenfor** (P2, eget arbeid) — se §2.

Regler: velg fra Book 23 og pakkene først; nye noder er `purpose://candidate.…`
og navngis her, aldri av en modell. Hvert bladformål har test i §5.

## 2. Avgrensning og avhengigheter

Hva dette IKKE er:

- Ikke implementering av celle-autentisitet (nøkler, enrollment, signerte
  envelopes). Det er steg 1–4 i `Celle_Autentisitet_Vurdering_2026-09-04.md` og
  krever bl.a. WO-E. Fase 2 reserverer bare kontraktsfeltene.
- Ikke endring av default `.dedicated` → `.multiplexedV2` noe sted. Opt-in består.
- Ikke backpressure/HOL-blocking-løsning (P2 fra fase 1-funnene; eget arbeid).
- Ikke E2EE (`Fabel_E2EE_Assessment_2026-07-21.md` er egen sak).
- Ikke merge/opprydding av CellScaffold-gaffelen; men P2-planen må vite hvor
  fase 1-koden faktisk er.
- Ikke `wsce`/browserhead-ruten.

| Kapabilitet/avhengighet | Kilde | Avgrensning | Må virke før test? |
|---|---|---|---|
| Fase 1-koden (`/session` på AdminScaffold) | `AdminScaffoldBridgeRoutes.swift:315,418`; `origin/main` `dd72f4ed` | Verifisert på origin/main av Codex 04.09; arbeid skjer i friske worktrees fra main | ja |
| `BridgeMultiplexServerSession` + `channelFactory`-hook | `BridgeMultiplexing.swift` | Server-siden finnes; per-kanal avregistrering ved `closeChannel` mangler hook (P1 fra fase 1) | ja |
| Resolver-utstedt signert tilgangskontrakt (native) | `SproutResolverCompatibility.swift:839` | Finnes for dagens per-celle-rute; sesjonsnivå + per-kanal er det som skal bygges | ja |
| `handshakeVerifier` (admin-ruter) | `AdminBridgeHandshakeAuthentication.swift` | Delt nøkkel uten scope-felt; P1-residual — fase 2 skal ikke arve «ingen scope = alt» | ja |
| Swift-bygg/test på maskinen | fase 1 kjørte `swift test --filter` grønt 20.08 | `arch -arm64` kreves for testbundelen | ja |
| Codex som utfører | `codex exec` via terminal | MCP-kanalen kuttes ~60 s (`lesson.codex-mcp-60s`); git aldri via mount (`lesson.mount-is-not-git`) | ja for P3 |

## 3. Forventningskontrakt — «Det du kommer til å se»

| Leveranse | Type | Hvor | Referanse | Godkjent |
|---|---|---|---|---|
| Handshake-/kanalkontrakt som versjonert JSON med fixtures (positive + negative), inkl. scope-felt og reserverte celle-bevis-felter | fil + testutdata | `contract/bridge_session_handshake_contract_v1.json` (+ kandidat til `Book/`) · `TESTRESULT.md#contract` | — | nei |
| `native-porthole/session`-rute som aksepterer én socket per (identitet, vert) og N kanaler | kode + testutdata | `CellScaffold/Sources/App/...` · `TESTRESULT.md#session-route` | — | nei |
| Negativ-matrise: uten scope, feil scope, utløpt/forfalsket/replayet kontrakt, kanal over tak, socket-tap | testutdata | `TESTRESULT.md#auth` og `#cap` og `#socket-loss` | — | nei |
| Beslutningene (scope-modell, kanaltak, reconnect-v1) nedfelt der de hører hjemme | doc-diff | `Docs/BridgeCachingAndMultiplexing.md` + `Book/08` («Last verified against code») | — | nei |
| Kjørbar Codex-ordre for P3 | fil | `handoff/README.md` i denne mappa | — | nei |
| Oppdatert ledgerpost | entry | `SISTE_OPPDATERING.md` | — | nei |

## 4. Tilknyttede formålspakker og lærdommer (auto fra purpose_dev.py lookup)

## Formålspakker som festes
- **pkg.std.everything-works** — Alt skal virke (standard kvalitetsport)
    - purpose://quality.build-and-regression: Alle berørte mål bygger og eksisterende tester passerer uten at tester er fjernet eller svekket.
        - test test.build [command]: Bygg alle berørte mål. → TESTRESULT.md#build
        - test test.regression [command]: Kjør hele eksisterende testmengde. → TESTRESULT.md#regression
    - purpose://quality.docs-in-same-change: Alle dokumenter som beskriver endret oppførsel er oppdatert og datert 'Last verified against code'.
        - test test.docs-updated [inspection]: Hver endret kontrakt/atferd har tilsvarende doc-diff. → ACCEPT.md#docs
    - purpose://quality.work-is-visible: Oppgavemappen har oppdatert STATUS.md med gate-tilstand, og et eventuelt planbytte er datert og begrunnet.
        - test test.status-current [inspection]: STATUS.md speiler faktisk tilstand. → ACCEPT.md#status
    - artefakt FORMAALSSPEC.md (port G1) · PLAN.md (G2) · TESTRESULT.md (G3) · ACCEPT.md (G3) · STATUS.md (G3)
- **pkg.std.cell-contract** — Cellekontrakt
    - purpose://cell.contract-explicit: kontrakt-JSON finnes, validator grønn på alle fixtures. → TESTRESULT.md#contract
    - purpose://cell.authorization-honours-keypath: feil requester, feil keypath og purpose://prompt.unknown avvises. → TESTRESULT.md#auth
    - purpose://cell.no-empty-stubs: ingen no-op-endepunkt uten 'not-implemented'. → ACCEPT.md#stubs
    - artefakt contract/ (port G2)
- **pkg.std.cell-combination** — Cellekombinasjon og dataflyt
    - purpose://cells.dataflow-declared: dataflow.md med alle kanter navngitt. → PLAN.md#dataflow
    - purpose://cells.capabilities-declared-with-boundary: §2 lister hver antatt kapabilitet med kilde og grense. → FORMAALSSPEC.md#audit
    - artefakt dataflow.md (port G2)
- **pkg.std.codex-handoff** — Overlevering til Codex/terminal
    - purpose://handoff.runnable-without-guessing: README med rekkefølge, forventet utfall, --dry-run/--go. → TESTRESULT.md#dry-run
    - artefakt handoff/README.md (port G2)

## Lærdommer du må lese før dekomponering
- **lesson.plan-instead-of-delivery** (2026-08-21, major): G1 godkjenner formål; etter G2 teller bare §3-artefakter som fremdrift.
- **lesson.undocumented-plan-switch** (2026-08-24, major): planbytter dateres i STATUS.md.
- **lesson.planned-documented-as-implemented** (2026-08-24, major): Book/05 beskrev signatur/replay som ikke finnes — direkte relevant: Book/08 §1 gjør det fortsatt for envelope-signatur. Doc-diff i samme endring.
- **lesson.bridge-inferred-architecture-from-one-use** (2026-08-09, major): hver kapabilitet erklæres med kilde — derfor audit-tabellen i §0.
- **lesson.cellscaffold-two-holes** (2026-09-01, blocker): autorisasjon som kaster nøkkelstien og bare sjekker eierskap skal ikke arves — scope-formålet finnes nettopp for dette.
- **lesson.purpose-never-grants-rights** (2026-08-03, blocker): scope innsnevrer; formål/match oppretter aldri tilgang; ukjent feiler lukket.
- **lesson.zsh-no-inline-comments** (2026-08-25, minor) · **lesson.mount-is-not-git** (2026-08-25, major) · **lesson.codex-mcp-60s** (2026-08-18, major): gjelder P3-utførelsen.
- **lesson.corr-approval-surfaces-timed-out** (2026-08-30, major): avhengigheter i §2 har verifier og sjekkes før den egentlige testen.

## 5. Avledede tester (samlet)

| Test | Type | Dekker | Evidens |
|---|---|---|---|
| test.bridge.session-scope-negative | command | session-scope-explicit: kontrakt uten scope avvises på `/session`; scope A når ikke flate B | TESTRESULT.md#auth |
| test.bridge.channel-open-authz | command | channel-authz-per-open: autorisert + uautorisert kanal på samme socket; `channelRejected`; første kanal leverer videre | TESTRESULT.md#auth |
| test.bridge.upgrade-parity | command + inspection | no-weakened-upgrade: utløpt/feil issuer/feil endpoint/forfalsket/replay avvises på sesjonsruten nøyaktig som på dagens rute | TESTRESULT.md#auth |
| test.bridge.contract-fixtures | command | cell-proof-fields-reserved + pkg.std.cell-contract: fixtures med felter til stede/utelatt/krevd-men-mangler; versjonering | TESTRESULT.md#contract |
| test.bridge.channel-cap | command | channel-cap-explicit: N kanaler ok, N+1 typed avslag, de N består | TESTRESULT.md#cap |
| test.bridge.socket-loss | command | socket-loss-explicit: dropp socket, alle delegater varsles, ingen foreldreløse registreringer; `resumeFromSequence` fjernet/implementert | TESTRESULT.md#socket-loss |
| test.bridge.setup-error-fanout | command | setup-errors-reach-channels | TESTRESULT.md#setup-error |
| test.build + test.regression | command | pkg.std.everything-works (CellProtocol + CellScaffold, `arch -arm64`) | TESTRESULT.md#build, #regression |
| test.cells.dataflow-matches-contracts | inspection | dataflow klient-pool → sesjon → kanal → BridgeBase → celle | PLAN.md#dataflow |
| test.docs-updated | inspection | Docs/BridgeCachingAndMultiplexing.md + Book/08-avsnittet om envelope merket riktig | ACCEPT.md#docs |
| test.handoff.dry-run | command | Codex-ordren tørrkjører grønt | TESTRESULT.md#dry-run |

## 6. Åpne spørsmål til Kjetil (G1) — besvart 2026-09-04

| # | Spørsmål | Kjetils svar (2026-09-04) |
|---|---|---|
| 1 | Tolkningen: «fase 2» = `native-porthole/session` (bridge), ikke PalazzoScaffold fase 2 | Lagt til grunn ved at designspørsmålene ble besvart; bekreftes endelig av G1-ordet |
| 2 | Scope-modellen | **Eget scope-felt** i sesjonskontrakten; hver kanalåpning valideres mot det; kredensial uten scope når bare legacy-ruter (fail-closed) |
| 3 | Kanaltak per fysisk sesjon | **64** på native-porthole (konfigurerbart) |
| 4 | Socket-tap v1 | **Bygg på nytt**: klienten bygger broene på nytt, hver kanaldelegat får eksplisitt closed-signal, `resumeFromSequence` fjernes |
| 5 | Celle-bevis-felter | **Reserveres** i kontrakt v1 som versjonerte, valgfrie felter; fail-closed bare når policy eksplisitt krever dem |

Gjenstår før G2: Kjetils G1-ord på formålstreet som helhet.

## 7. Revisjonslogg

| Iterasjon | Dato | Endring |
|---|---|---|
| 1 | 2026-09-04 | Første utkast etter kildelesing i CellProtocol/CellScaffold/HavenAgentD; §0-audit fylt; §6-spørsmålene stilt |
| 2 | 2026-09-04 | §6 besvart av Kjetil (eget scope-felt; tak 64; socket-tap: bygg på nytt; celle-bevis-felter reserveres); besluttede verdier ført inn i §1-målene |
| 3 | 2026-09-04 | G1 godkjent («G1 godkjent - og bruk codex»). WP0 utført: fase 1 verifisert på origin/main via Codex; §0/§2-radene oppdatert fra unavailable til retrieved. P2-artefakter skrevet (PLAN.md, contract/ 9/9 PASS, dataflow.md, handoff/) |
