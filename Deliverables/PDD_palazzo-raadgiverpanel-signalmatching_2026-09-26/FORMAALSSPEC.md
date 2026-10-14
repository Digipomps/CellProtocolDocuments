# Formålsspesifikasjon — palazzo raadgiverpanel signalmatching

Oppgavemappe: `PDD_palazzo-raadgiverpanel-signalmatching_2026-09-26` · Opprettet 2026-09-26 · Iterasjon 2 (G1 ikke godkjent)

> Regel: ingen plan før G1 er godkjent av Kjetil. For GUI: ingen implementering før G1-GUI (rendret bilde) er godkjent.
> Et dokument om leveransen teller aldri som leveransen.

## 0. Intensjon (ordrett) og brief-audit

> Sett opp et rådgiverpanel som kan hjelpe til med å lage relevante signalmatchinger, og teste seg frem til bedre formålsdekomponering og forståelse av tekst.

<a id="audit"></a>

| Påstand i intensjonen / antatt kapabilitet | Audit | Kilde (lest 2026-09-26) |
|---|---|---|
| Palazzo har en signalgraf og en matcher | retrieved | `PalazzoScaffold/Sources/App/Models/PalazzoSignalGraph.swift`, `…/PalazzoSignalGraphMatcher.swift`, `PalazzoScaffold/docs/Signalgraf_2026-09-21.md` (Last verified against code 2026-09-22) |
| Tekstforståelsen i dag er et håndskrevet leksikon + normaliserte tokens, ingen språkmodell | retrieved | `PalazzoScaffold/Sources/App/Models/PalazzoRememberModels.swift:139` (`PalazzoTagLexicon`), `PalazzoSignalGraph.normalizedToken/normalizedText` |
| Matchingen kjører i gjestens entitet; huset publiserer signaler (D1) | retrieved | `PalazzoComunaleScaffold/docs/Vurdering_Signalmatching_Familietilhorighet_2026-09-05.md` §9 |
| Over grensen går dom + forklaring gjesten har godkjent + tillitspakke; to grants per treff (D2, D3) | retrieved | samme, §9 og §10 |
| Match-API-et er levende i den deployede revisjonen | retrieved | `HAVEN-Deploy/_handoff/HD-0077/STATUS-BRO-OG-FLATER-20260926.md`, `…/STATUS-FLATER-DETALJ2-20260926.md` (401 uten gateway-token, 200 med) |
| Produksjonen har signaler og treff å måle på | **contradicted** | `/api/content/signals`, `match/pending`, `match/shared` er alle tomme lister 2026-09-26. Korpus og fasit må lages, ikke hentes |
| Et gjenbrukbart løp for å måle formålsforståelse finnes | retrieved | `Book/38_Measuring_Purpose_Understanding_Without_A_Model.md`; `pkg.std.maal-formaalsforstaaelse`; `Deliverables/PDD_butler-onboarding-og-formaalsforstaaelse_2026-09-23/maaling/score.py` |
| Book 38 peker på Palazzo som neste matcher løpet skal brukes på | retrieved | Book 38, innledningen |
| Panelferdigheten `haven-panel-task-decomposition` er tilgjengelig i denne økten | **unavailable** | ikke i øktens ferdighetsliste 2026-09-26. Panelreglene hentes derfor fra fan-out-lærdommen (motstandsagent + maskinell validering) og Book 38 §2 |
| Gjesteflaten over broen kan brukes til å prøve matchingen | **contradicted** | broen er av i produksjon, og en anmoder over bro kan ikke få opprettet identitetsunike celler på CellProtocol main — `HAVEN-Deploy/_handoff/HD-0077/BRO-DIAGNOSE-GJEST-20260920.md` |
| «Rådgiverpanel» er roller i et løp, ikke en flate | retrieved (tolkning) | Book 38 §2 rolletabell (generator, tolk, dommer, måler, poengsetter) + fan-out-regelen om motstandsagent. Rådgiverrollene under er nye og navngis her |

## 1. Formålstre

| purposeRef | Tittel | Forelder | Goal (outcome) | Verifier | Status |
|---|---|---|---|---|---|
| purpose://candidate.palazzo-signalforstaaelse.root | Gjesten får treff som er relevante, forklarbare med egne ord, og aldri mot eget veto | purpose://test.acceptance | En måling viser før/etter for treffkvalitet på frosset korpus og på uavhengig korpus, uten tap på negativer og uten et eneste brutt veto | Rapport fra `score.py` + Swift-harness | candidate |
| purpose://candidate.palazzo-signalforstaaelse.panel-kan-kjores-igjen | Panelet er et løp som kan kjøres på nytt av andre | purpose://handoff.runnable-without-guessing | Panelmappa har roller, inventar, MANGLER-regel, kjørerekkefølge og én køjobb per rolle; en ny runde krever ingen forklaring i chat | `test.handoff.dry-run` + tørrkjøring av panelkjøringen | candidate |
| purpose://candidate.palazzo-signalforstaaelse.husets-signaler-treffer | Husets signaler bærer ordene en gjest faktisk bruker | purpose://candidate.palazzo-signalforstaaelse.root | For korpuset dekker husets publiserte tagger de ordene gjestene bruker om de samme rettene, med dekning målt per artikkel og falske treff listet rad for rad | `test.palazzo.tekst-til-noder` (dekningskolonnen) | candidate |
| purpose://candidate.palazzo-signalforstaaelse.tekst-til-noder | Gjestens egne ord blir noder som kan spores til teksten | purpose://measurement.production-path | Hver utledet node (tagg, interesse, formål, polaritet) kan begrunnes med et sitat fra meldingen; presisjon og dekning måles mot gullfasit | `test.palazzo.tekst-til-noder` | candidate |
| purpose://candidate.palazzo-signalforstaaelse.dom-og-forklaring | Dommen er riktig og forklaringen er gjestens egne ord | purpose://candidate.palazzo-signalforstaaelse.root | Per (melding × signal): dom positiv/negativ/uavklart stemmer med fasit, og forklaringen siterer gjestens tekst — ikke husets tittel | `test.palazzo.dom-og-forklaring` | candidate |
| purpose://candidate.palazzo-signalforstaaelse.veto-ufravikelig | Et negativt svar fra gjesten kan ikke overstyres av en positiv sti | purpose://candidate.palazzo-signalforstaaelse.root | Ingen positiv anbefaling finnes for en artikkel gjesten har avvist, i noen variant, i noen kjøring | `test.palazzo.veto-ufravikelig` | candidate |
| purpose://candidate.palazzo-signalforstaaelse.ingen-profil-over-grensen | Ingenting annet enn dom, godkjent forklaring og tillitspakke krysser grensen | purpose://cell.authorization-honours-keypath | Målerapporten viser hvilke felt som ville blitt delt; settet er nøyaktig D2/D10-feltene, og et treff gir ingen rettighet | `test.palazzo.ingen-profil-over-grensen` | candidate |
| purpose://measurement.gain-on-unseen-data | Gevinsten måles på data ingen endring er begrunnet med | purpose://test.acceptance | Som pakken: holdout urørt, uavhengig korpus etter frysing, vunnet/tapt per melding | `test.maal.holdout-urort`, `test.maal.uavhengig-korpus` | candidate (fra pakke) |
| purpose://measurement.honest-labels | Sølvfasit fra blind tolk, gullfasit fra dom med lokkeduer | purpose://test.acceptance | Som pakken: opake id-er til tolken, lokkeduer i hver dom, maks fem oppgaver per økt | `test.maal.opake-id`, `test.maal.lokkeduer` | candidate (fra pakke) |
| purpose://measurement.negatives-guarded | Negativer uten handling er egen kategori og blir ikke dårligere | purpose://test.acceptance | Småprat, allergi/avvisning og «ikke gjør noe» gir ingen anbefaling, og andelen er ikke lavere etter endring | `test.maal.negativer` | candidate (fra pakke) |

Rådgiverrollene i panelet (navngitt her, ikke av en modell). Hver rolle får inventaret i §2 og MANGLER-regelen:

| Rolle | Oppgave | Leverer til |
|---|---|---|
| Vertsrådgiver | Hvilke signaler huset bør publisere per artikkel/rett, sett fra bordet | `forslag/SIGNALFORSLAG-v1.md` |
| Råvarerådgiver (Sicilia) | Råvarer, allergener, regionale og italienske ord gjesten kan bruke | `forslag/LEKSIKON-v1.md` |
| Gjesteadvokat | Vokter D1–D3: matching i gjestens entitet, to grants, ingen profil, negativ polaritet som veto | avvisninger i begge forslagsfilene |
| Matcher-ingeniør | Oversetter forslagene til det kodeveien faktisk kan bruke (leksikonoppføringer, tagger, vekter, toleranse/hops); skriver «MANGLER: …» i stedet for å oppfinne kapabiliteter | `forslag/LEKSIKON-v1.md`, `maaling/grafendringer/` |
| Generator-personaer (4) | Naturlige gjestetekster: reaksjoner, kommentarer, «husk det jeg sa» | `maaling/korpus/palazzo-v1.jsonl` |
| Tolk (rask modell, blind) | Sølvfasit på opake, stokkede id-er | `maaling/fasit/palazzo-solv-v1.jsonl` |
| Dommerbenken (Kjetil) | Gullfasit der generator og tolk er uenige, med blinde lokkeduer, maks fem oppgaver per økt | `maaling/dommerbenk/` |
| Motstandsagent (sist) | Finner det som ikke holder i hele settet; skal ikke oppsummere | `MOTSTAND-v1.md`, og rettelsene inn i forslagene |

## 2. Avgrensning og avhengigheter

Hva dette IKKE er:
- Ikke en språkmodell i produksjon. Matcheren forblir AI-løs; tolk og generator brukes bare til å bygge korpus og fasit (Book 38 §1).
- Ikke matching på hussiden, og ikke i kelnerbriefen (D1 og invarianten om at F2 ikke bruker matching).
- Ikke publisering av signaler i produksjonen. Panelets forslag er filer; å publisere dem i det kjørende scaffoldet er en egen beslutning og en egen jobb.
- Ikke broen, og ikke gjesteflaten i HAVEN-appen (broen er av; første kontakt over bro er blokkert i CellProtocol main).
- Ikke endringer i CellProtocol. `WeightedGraphRuntime` er gitt; bare Palazzo-siden røres.
- Ikke en ny GUI-flate. Trengs en flate for dommerbenken eller forslagene, blir det egen G1-GUI i egen runde.

| Kapabilitet oppgaven bygger på | Kilde (fil) | Avgrensning | Må virke før test? |
|---|---|---|---|
| Signalgraf: noder, kanter, vekter, polaritet | `PalazzoScaffold/Sources/App/Models/PalazzoSignalGraph.swift`; `docs/Signalgraf_2026-09-21.md` | Grafen bygges av gjestens egne poster; huset ser den aldri | ja |
| Matcher: taggsnitt, `WeightedGraphRuntime`, veto, uavklart ved budsjett | `PalazzoScaffold/Sources/App/Models/PalazzoSignalGraphMatcher.swift` | Ingen semantisk likhet, bare normaliserte tokens | ja |
| Leksikon: term → tagger | `PalazzoScaffold/Sources/App/Models/PalazzoRememberModels.swift:139` | Håndskrevet; ingen bøyningsanalyse, ingen flertydighet | ja |
| Husets signaler og taggforslag med godkjenning | `PalazzoScaffold/Sources/App/Cells/PalazzoContentCell.swift` (`draftTags*`) | Tagger godkjennes av huset før de blir signal | nei (målingen bruker fixtures) |
| Måleløpet: korpus, holdout, tolk, dommerbenk, `score.py` | `Book/38_…md`; `PDD_butler-onboarding-og-formaalsforstaaelse_2026-09-23/maaling/` | Tre ting byttes: etikettrom, adapter, etikett-kart (Book 38 §5) | ja |
| Artikkelkorpus (Sicilia, 15 artikler) | `PalazzoScaffold/Tests/AppTests/Fixtures/artikler_v1.json` | Byte-lik kopi av PDD-fasiten; ikke husets levende meny | ja |
| Køen som utfører (skript/Codex) | `HAVEN/_losen-queue/LES_MEG.md` | Lange bygg kjøres som detached skript, ikke `workspace-write`-jobb | ja |

## 3. Forventningskontrakt — «Det du kommer til å se»

Én rad per leveranse. Dette er det eneste som teller som fremdrift etter G2. Alle stier er relative til denne oppgavemappa.

| Leveranse | Type | Hvor | Referanse | Godkjent |
|---|---|---|---|---|
| Panelet: roller, inventar, MANGLER-regel, kjørerekkefølge | fil | `panel/README.md`, `panel/roller/*.md` | §1 rolletabell | nei |
| Frosset korpus med 25 % holdout, fire personaer | fil | `maaling/korpus/palazzo-v1.jsonl` | Book 38 regel 2 og 8 | nei |
| Sølvfasit (tolk, opake id-er) og gullfasit (dommerbenk med lokkeduer) | fil | `maaling/fasit/`, `maaling/dommerbenk/` | `test.maal.opake-id`, `test.maal.lokkeduer` | nei |
| Etikett-kart + dumpet katalog fra samme kjøring | fil | `maaling/etikett-kart.json`, `maaling/katalog.json` | Book 38 regel 10 | nei |
| Harness over produksjonens egen kodevei | testutdata | `PalazzoScaffold/Tests/AppTests/PalazzoSignalForstaaelseMaalingTests.swift` → `maaling/rapport/*.resultat.jsonl` | `test.maal.produksjonsvei` | nei |
| Måling før endring (baseline) | testutdata | `maaling/rapport/RAPPORT-foer.md` | `TESTRESULT.md#forstaaelse` | nei |
| Panelets signalforslag per artikkel, med motstandsrundens avvisninger | fil | `forslag/SIGNALFORSLAG-v1.md` | §1 vertsrådgiver | nei |
| Leksikon-/vektforslag, hver endring med treningsradene den retter | fil | `forslag/LEKSIKON-v1.md`, `maaling/grafendringer/GRAFENDRINGER-v1.md` | `test.maal.holdout-urort` | nei |
| Måling etter endring, holdout og uavhengig korpus, negativer for seg | testutdata | `maaling/rapport/RAPPORT-etter-v1.md`, `maaling/rapport/RAPPORT-uavhengig-v1.md` | `test.maal.uavhengig-korpus`, `test.maal.negativer` | nei |
| Motstandsrunden | fil | `MOTSTAND-v1.md` | fan-out-regelen | nei |

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
    - artefakt FORMAALSSPEC.md (port G1): Godkjent formålsspesifikasjon.
    - artefakt PLAN.md (port G2): Arbeidspakker 1:1 mot bladformål.
    - artefakt TESTRESULT.md (port G3): Utdata fra alle avledede tester.
    - artefakt ACCEPT.md (port G3): Forventning mot faktisk, per leveranse.
    - artefakt STATUS.md (port G3): Gate-tilstand og planbytter.
- **pkg.std.cell-contract** — Cellekontrakt
    - purpose://cell.contract-explicit: Book/<celle>_contract_v<n>.json finnes, og en validator kjører grønt på alle fixtures.
        - test test.cell.contract-fixtures [command]: Kjør kontraktvalidator mot positive/negative fixtures. → TESTRESULT.md#contract
    - purpose://cell.authorization-honours-keypath: Negative tester viser at feil requester, feil keypath og purpose://prompt.unknown alle avvises.
        - test test.cell.auth-negative [command]: Feil requester / feil keypath / ukjent formål avvises. → TESTRESULT.md#auth
    - purpose://cell.no-empty-stubs: Ingen endepunkt i kontrakten er implementert som no-op uten status 'not-implemented'.
        - test test.cell.stub-scan [inspection]: Liste alle no-op-handlere og avstem mot Gap_Analysis.md. → ACCEPT.md#stubs
    - artefakt contract/ (port G2): Kontrakt-JSON + fixtures (kan være lenke til Book/).
- **pkg.std.cell-combination** — Cellekombinasjon og dataflyt
    - purpose://cells.dataflow-declared: dataflow.md (eller .graffle/.json) finnes med alle kanter navngitt med endepunkt/event.
        - test test.cells.dataflow-matches-contracts [inspection]: Hver kant i dataflow finnes i en kontrakt. → PLAN.md#dataflow
    - purpose://cells.capabilities-declared-with-boundary: FORMAALSSPEC.md §2 lister hver antatt kapabilitet med kildefil og hva den ikke dekker.
        - test test.cells.capability-audit [inspection]: Alle kapabilitetspåstander har audit-status retrieved. → FORMAALSSPEC.md#audit
    - artefakt dataflow.md (port G2): Diagram + kant-tabell.
- **pkg.std.codex-handoff** — Overlevering til Codex/terminal
    - purpose://handoff.runnable-without-guessing: README.md i _handoff-mappen har rekkefølge, forventet utfall per steg, og alle skript støtter --dry-run/--go.
        - test test.handoff.dry-run [command]: Tørrkjøring gir 0 og lister hva som ville skjedd. → TESTRESULT.md#dry-run
    - artefakt handoff/README.md (port G2): Rekkefølge og kommandoer.
- **pkg.std.maal-formaalsforstaaelse** — Måle og forbedre formålsforståelse
    - purpose://measurement.gain-on-unseen-data: Rapporten viser før/etter både på holdout og på et uavhengig korpus skrevet etter frysing, med vunnet/tapt per melding.
        - test test.maal.holdout-urort [inspection]: Ingen endring begrunnes med en holdout-rad. → TESTRESULT.md#forstaaelse
        - test test.maal.uavhengig-korpus [measurement]: Frosset variant målt på nytt korpus fra nye skribenter. → TESTRESULT.md#uavhengig
    - purpose://measurement.production-path: Måleløpet går gjennom produksjonens funksjon, og den eksisterende CI-fasiten gir fullt treff i samme kjøring.
        - test test.maal.produksjonsvei [command]: Harnessen kaller produksjonens egen funksjon. → TESTRESULT.md#forstaaelse
        - test test.maal.tilregnelighet [command]: CI-fasiten scorer fullt i samme kjøring. → TESTRESULT.md#forstaaelse
    - purpose://measurement.honest-labels: Sølvfasit fra blind tolk og gullfasit fra dom der lokkeduene avsløres.
        - test test.maal.opake-id [inspection]: Tolkens innfiler har opake id-er. → TESTRESULT.md#fasit
        - test test.maal.lokkeduer [inspection]: Dommerrunden har lokkeduer og ble avslørt. → TESTRESULT.md#fasit
    - purpose://measurement.negatives-guarded: Negativer uten handling er rapportert for seg og er ikke lavere etter endringen.
        - test test.maal.negativer [measurement]: Negativer uten handling er ikke lavere enn før. → TESTRESULT.md#forstaaelse
    - artefakt maaling/ (port G3): Korpus, fasit, rapporter per variant (se Book 38).

## Lærdommer du må lese før dekomponering
- **lesson.plan-instead-of-delivery** (2026-08-21, major): Kjetil ba om en leveranse flere ganger og fikk planer/dokumenter om leveransen i stedet.
    - forebygging: G1 godkjenner formål, ikke arbeid; etter G2 telles bare artefakter listet i §3 'Det du kommer til å se' som fremdrift. Et dokument om leveransen teller aldri som leveransen.
- **lesson.undocumented-plan-switch** (2026-08-24, major): Tre produktive døgn (22.–24.08) så tomme ut i alle statusdokumenter fordi planbyttet fra bølge 1–3 til deploy-seremonien aldri ble skrevet ned.
    - forebygging: STATUS.md i oppgavemappen oppdateres ved hvert planbytte med dato og hvorfor; sjekkes i test.status-current.
- **lesson.planned-documented-as-implemented** (2026-08-24, major): Book/05_Flows_Lifecycle.md beskrev sekvensnummer, signatur og replay som ikke finnes i structen.
    - forebygging: Docs-diff i samme endring, med 'Last verified against code'-dato; planlagt oppførsel merkes eksplisitt.
- **lesson.bridge-inferred-architecture-from-one-use** (2026-08-09, major): En kodeassistent sluttet fra én observert bruksmåte av bridge til en egenskap ved arkitekturen og konkluderte feil.
    - forebygging: Erklær hver kapabilitet oppgaven bygger på som eget formål med kilde og Avgrensning (pkg.std.cell-combination).
- **lesson.cellscaffold-two-holes** (2026-09-01, blocker): CellScaffold har tomme booking-/concierge-stubber og autorisasjon som kaster nøkkelstien og bare sjekker eierskap.
    - forebygging: Ikke porter celler fra CellScaffold til PalazzoScaffold uten å lukke begge hullene; test.cell.auth-negative og test.cell.stub-scan må være grønne.
- **lesson.purpose-never-grants-rights** (2026-08-03, blocker): Risiko for at formålsmatch tolkes som tilgang.
    - forebygging: Et formål kan innsnevre en rettighet, aldri opprette, utvide eller arve en; exact match; purpose://prompt.unknown feiler lukket.
- **lesson.zsh-no-inline-comments** (2026-08-25, minor): Begge kommandolinjene feilet med 'ukjent argument: #' og ingenting kjørte.
    - forebygging: Aldri forklaring på samme linje som en kommando; skript har '"#"*) break ;;' i argumentparseren.
- **lesson.mount-is-not-git** (2026-08-25, major): Hver git-kommando fra device_bash etterlot en index.lock som ikke kunne fjernes og blokkerte Kjetils commits; seks repoer låst 24.08.
    - forebygging: Aldri git mot $HOME/mnt fra device_bash; les .git/refs som filer; all git kjøres av Kjetil eller codex exec.
- **lesson.codex-mcp-60s** (2026-08-18, major): Codex-MCP-kall kuttes etter ~60 s; registerlesning og Swift-bygg sprengte taket.
    - forebygging: Bygg/test/lange jobber går via terminal codex exec eller filbasert overlevering, aldri via Codex-MCP.
- **lesson.corr-approval-surfaces-timed-out** (2026-08-30, major): Corr-godkjenningen (Vegar) er utestet fordi flater/godkjenninger timet ut før testing rakk å skje.
    - forebygging: FORMAALSSPEC.md §2 lister avhengigheter som egne formål med verifier; pkg.std.everything-works og gui.surface-loads-in-time må være grønne før den egentlige testen kjøres.
- **lesson.test-corpus-is-not-shipped-corpus** (2026-09-05, major): Rot-probe-testen, lastetidstesten og finnbarhetsauditen var gronne i to uker mens Relasjoner-flaten var tom.
    - forebygging: Enhver flate-test skal bygge korpuset fra det som faktisk sendes ut (menykonfigurasjoner + navigasjonsdestinasjoner + verifiseringshjelperen), dedupliseres, og feile hvis korpuset er mindre enn appens egen meny.
- **lesson.tested-a-different-path-than-production** (2026-09-05, major): Rot-probene leste relations.state.* gjennom porthole.get og var gronne, mens rendereren aldri fikk de samme dataene.
    - forebygging: Naar en test skal si noe om hva brukeren ser, maa den bruke produksjonens egen kodevei - helst produksjonens egen funksjon med produksjonens egne inndata (SkeletonReachabilityAudit kaller condition.evaluate(root: nil, ...) nettopp derfor).
- **lesson.paste-command-instead-of-queue** (2026-09-07, major): Kjetil fikk et innlimingsskript for å starte Codex; flagget --full-auto finnes ikke på `codex exec`, og kjøringen feilet ved første linje.
    - forebygging: Før enhver Codex-kjøring fra Cowork: `ls HAVEN/_losen-queue/inbox running; tail logs/runner.log`, legg jobben som <id>.job + <id>.prompt.md. Aldri gi Kjetil kommandoer å lime inn. Gyldige `codex exec`-flagg: --sandbox, --skip-git-repo-check, -C.
- **lesson.baseline-count-from-report-not-run** (2026-09-07, minor): PLAN.md sa «48 tester grønne»; baseline-kjøringen viste 68 tester med 3 røde.
    - forebygging: WP0/S0 baseline er alltid en ekte kjøring før endring; PLAN oppgir testtall som «forventet ≈ N (fra <kilde, dato>)», og et rødt baseline stopper ikke arbeidet men registreres som eget avvik med årsak.
- **lesson.codex-sandbox-cannot-reach-docker** (2026-09-07, major): S10 (docker compose build/up) endte i `permission denied … docker.sock` i Codex-sandkassen; deploy-slicen ble blocked.
    - forebygging: Deploy-/image-steg planlegges aldri som Codex-slice; de registreres som HAVEN-Deploy-post med eier Kjetil (eller en dispatcher-adapter med eksplisitt docker-rettighet når arbeidskø-PDD-en er levert). Se HD-0012.
- **lesson.scaffold-without-porthole-host-has-no-preview** (2026-09-07, minor): G1-GUI måtte bruke mockups rendret fra skeleton-JSON; ekte Porthole-preview var umulig.
    - forebygging: For scaffolds uten Porthole-vert: (1) images/README.md må si eksplisitt at bildene er mockups og hva skeleton ikke kan rendre, (2) paritet (test.gui.parity) planlegges som egen slice med kjørende scaffold + Binding/Porthole via bridge, ikke som del av implementeringsjobben.
- **lesson.codex-workspace-write-cannot-build-cellscaffold** (2026-09-09, major): WP0-baselinen i køen ble blocked: `sandbox-exec: sandbox_apply: Operation not permitted`. Testkommandoen brukte 1 604 sekunder uten at én eneste test startet.
    - forebygging: Lange bygg og testkjøringer legges ikke som `workspace-write`-køjobb. De kjøres som detached skript startet via Codex med `danger-full-access` og python Popen(start_new_session=True), med logg i en montert mappe som Cowork kan polle — samme mønster som produserte den notariserte HavenAgentD-pakken 2026-09-08. Køjobber brukes til analyse, kontrakter, dokumentasjon og korte kommandoer.
- **lesson.baseline-measured-another-pdds-branch** (2026-09-09, major): WP0 målte `pdd/tillitspakke-agentflaate` med 181 skitne oppføringer, ikke et rent utgangspunkt for sin egen PDD. En regresjonsbaseline derfra sier ingenting om hva denne PDD-en endrer.
    - forebygging: WP0 måler en ren eksport av den revisjonen arbeidet skal gå ut fra (`git archive <rev> | tar -x -C <scratch>`), ikke det delte arbeidstreet. Er arbeidstreet opptatt av en annen PDD, er det en planopplysning som hører i STATUS, ikke noe implementeringen skal jobbe rundt.
- **lesson.worktree-created-from-vm-has-unusable-gitdir** (2026-09-09, major): WP1 ble blocked etter ett minutt: `fatal: not a git repository: /sessions/<sesjon>/mnt/CellScaffold/.git/worktrees/_wt-sad-20260909`, exit 128. Branch og HEAD kunne ikke bekreftes.
    - forebygging: Opprett worktrees fra macOS (Codex), ikke fra VM-en. Er det allerede gjort fra VM-en: skriv om begge pekerfilene til macOS-stien og verifiser `branch --show-current` + `rev-parse HEAD` **fra macOS** før noen jobb legges i køen. En jobb skal aldri være første stedet en sti blir prøvd.
- **lesson.cellbase-decodingerror-shadows-swift** (2026-09-09, minor): WP1s nye celle ga 50 kompileringsfeil: `type 'DecodingError' has no member 'dataCorruptedError'` og `cannot infer contextual base in reference to member 'registry'`, alle fra én linje.
    - forebygging: I App-modulen: skriv `Swift.DecodingError` når du vil ha standardbibliotekets. Gjelder generelt for typenavn CellBase også definerer — sjekk med `grep -rn "enum <Navn>" CellProtocol::Sources/CellBase` før du antar at et kjent Foundation-navn er Foundations.
- **lesson.valuetype-equality-false-for-objects** (2026-09-09, major): Fire av sju WP1-tester feilet på `XCTAssertEqual` mellom to `ValueType.object` som hadde identisk innhold. Feilmeldingen viste samme nøkler og verdier på begge sider, i ulik rekkefølge.
    - forebygging: Aldri assert på hele sammensatte `ValueType`-verdier. Sammenlign kanonisk JSON (`JSONEncoder` med `.sortedKeys`) eller pakk ut og sammenlign felt for felt. Skalarer (`.string`, `.integer`, `.bool`, `.null`) sammenlignes trygt. Merk: dette er et funn i CellBase, ikke bare en testregel — App-kildene destrukturerer riktignok før sammenligning, men en fremtidig `==` på hele verdier vil stille behandle like verdier som ulike. Ikke revidert utover App-kildene.
- **lesson.syntax-check-reported-as-delivered** (2026-09-09, major): WP1 ble rapportert som «kode og 7 tester levert, syntakssjekken bestod». Et faktisk bygg ga 50 kompileringsfeil, og testene feilet 4 av 7 da de først kunne kjøre.
    - forebygging: En implementeringsslice er ikke levert før et detached bygg med `danger-full-access` er kjørt mot arbeidstreet og både bygg og de nye testene er grønne. Legg byggejobben klar FØR slicen kjøres, og skriv i prompten at slicen skal rapportere «skrevet, ikke verifisert» — ikke «levert».
- **lesson.cellbase-internal-members-look-public** (2026-09-09, minor): WP2 stoppet på `'fullPermissionString' is inaccessible due to 'internal' protection level`. Medlemmet finnes og brukes i CellBase selv, så det så ut som et gyldig API.
    - forebygging: Sjekk tilgangsnivå og faktisk returverdi før du bruker et CellBase-medlem fra App: `grep -n "var <navn>" CellProtocol::Sources/CellBase/...`. Et medlem som brukes internt i CellBase er ikke automatisk en del av API-et, og navnelikhet betyr ikke verdilikhet.
- **lesson.entityanchor-keypaths-are-registered** (2026-09-09, minor): WP2-testen skrev en sentinel til `profile` på abonnentens EntityAnchor og fikk `notFound` ved gjenlesing. Skrivingen ga ingen feil.
    - forebygging: Skriv aldri testdata til en oppdiktet keypath på en celle. Finn en keypath cellen faktisk registrerer, helst en annen test som allerede bruker den. At et `set` går gjennom er ikke bevis på at keypathen finnes.
- **lesson.new-cell-must-declare-its-provisioning-mode** (2026-09-09, major): To nye celler i CellScaffold ga tre nye regresjoner: `OrchestratorPersistenceTests testRequireExistingModeRejectsFreshStorageWithoutCreatingBootstrapCells` (opprettet en celle i require-existing-modus mot fersk lagring) og to `TopUpCheckoutTests` som teller celler i provision-only-modus (5 mot forventet 4).
    - forebygging: Enhver ny persistert celle i CellScaffold må eksplisitt svare på tre spørsmål før den registreres: (1) skal den opprettes i require-existing mot fersk lagring? Nei, med mindre den er kanonisk bootstrap. (2) Er den en av de kanoniske eager-bootstrap-cellene som provision-only skal lage? Nesten alltid nei — TopUpCheckoutTests teller dem eksplisitt. (3) Er den en Porthole-publisert flate? Bare da hører den i `reconcilePortholePublishedCellResolves`. Scaffold-intern tilstand registreres i egen funksjon, gated på policy OG provisionOnly, med gjenkjenning av eksisterende mapping.
- **lesson.branch-is-empty-after-eight-work-packages** (2026-09-09, major): Åtte arbeidspakker rapportert utført og verifisert, ACCEPT.md skrevet — men `git branch -v` viste at `pdd/scaffold-admin-delegering` fortsatt pekte på samme commit som `main` (`e1f3e22f`). All koden lå ucommittet i et worktree som bare finnes på én maskin. Ett tapt worktree = 2 750 linjer kode og test borte, med full dokumentasjon på at arbeidet var «levert».
    - forebygging: Skill «filene finnes» fra «branchen har dem». Sjekk `git rev-parse <branch>` mot `git rev-parse <base>` som del av hver verifikasjon som påstår at noe ligger på en branch; er de like, er branchen tom. Legg en commit-pakke inn i planen etter første grønne bygg, ikke etter siste arbeidspakke. Når worktreet bare kan leses fra macOS, kjør sjekken der — ikke hopp over den fordi verktøyet svarer feil.
- **lesson.stop-rule-too-wide-stops-the-job** (2026-09-09, minor): En commit-jobb til Codex stoppet før første `git add` fordi stoppregelen sa «finner du `.git/index.lock` eller annen låsefil: stopp». Et rekursivt søk fant 25 filer som heter `locked` under andre arbeidstrær — normale `git worktree lock`-markører som ikke blokkerer noe. Jobben gjorde ingenting, og hele runden gikk tapt.
    - forebygging: Skriv stoppregler som navn og sti, ikke som kategori: «stopp hvis `index.lock`, `HEAD.lock` eller `*.lock` finnes under `<denne stien>`». Navngi eksplisitt det som ser ut som en treffer men ikke er det, og si at det skal ignoreres. Legg alltid til «stopp hvis kommandoen faktisk avvises med denne feilen» — en filsøk-treffliste er ikke et bevis på blokkering. Samme gjelder alle vide vendinger i en prompt: «eller lignende», «eller annet», «eventuelle andre».
- **lesson.ciphertext-field-held-plaintext-hash** (2026-09-10, blocker): Losen fortalte Kjetil at lyd allerede var kryptert i lagring. Det var feil: filene i prod begynner med ID3 og er vanlig MP3. To ting forte dit. (1) Krypteringskoden som ble lest tilhorer MusicIngestCell paa /mvp/ingest/local, mens Butterpop publiserer gjennom MusicAssetStoreCell.storeLocalAsset, som skriver bytene slik de kommer. (2) storeLocalAsset setter ciphertextSHA256 = plaintextSHA256 = sha256(data), saa manifestet ser kryptert ut selv naar encryptionPolicy er none.
    - forebygging: En paastand om at noe er kryptert, signert eller verifisert skal bekreftes paa artefaktet - les bytene, ikke feltet. Et felt som heter ciphertext* skal ikke settes naar encryptionPolicy er none; enten utelates det, eller navnet sier hva det er. Kan bli derivedTest: manifest med encryptionPolicy none har ingen ciphertext-verdi.
- **lesson.local-main-is-not-main** (2026-09-11, major): WP0-baselinen var rød og ble meldt som «main bygger ikke». Det var feil. Den commiten baselinen ble målt mot, `ba14895`, lå bare på den LOKALE main-grenen og var aldri pushet; den avhang av CellBase-kode som heller ikke var pushet. origin/main lå fire commits lenger fram, pinnet CellProtocol til en revisjon som ER på CellProtocol sin main, og hadde grønn CI hele tiden. Et helt døgns arbeid ble bygget oppå den lokale commiten.
    - forebygging: Før du måler en baseline eller sier at main er rød: `git fetch origin main` og sammenlign. Er lokal main foran origin/main, er de commitene ikke main for andre — bygg aldri videre på dem. Se på CI for origin/main før du konkluderer. `swift package edit` skal aldri være på når noe måles eller meldes verifisert. Og den eneste sjekken som virkelig avgjør: klon fra GitHub til en tom katalog og bygg der. HavenAgentD::Scripts/preflight_before_landing.sh stiller alle fire spørsmålene.
- **lesson.a-new-red-test-needs-a-repeated-baseline** (2026-09-10, minor): Første fulle kjøring med nye endringer viste to røde i stedet for baselinens én, og den nye lå i en fil jeg hadde endret. Det så ut som en regresjon jeg hadde innført.
    - forebygging: Når en ny rød dukker opp: kjør basen på nytt, i et eget rent worktree, **flere ganger** (tre holder som regel), før du enten tar på deg feilen eller avfeier den. Skriv resultatet av gjentakelsen i TESTRESULT — «2 av 3 på ren base» er et svar, «den er nok flaky» er ikke. Det koster ti minutter og avgjør om du bruker natten på å jage din egen feil eller andres.
- **lesson.swift-test-exit-code-lies-in-havenagentd** (2026-09-10, minor): `swift test` i HavenAgentD avslutter med 1 selv når samtlige 212 tester passerer. Et skript som leser `$?` melder rødt på et helt grønt tre.
    - forebygging: Les resultatet fra linjen `Test run with N tests in M suites passed/failed`, ikke fra exitkoden, i alle skript og køjobber for dette repoet. Og fjern det tomme XCTest-målet, eller bygg det for riktig arkitektur, før noen setter opp CI her — ellers vil CI være rød uansett hva som gjøres.
- **lesson.pkill-pattern-killed-the-queue-job** (2026-09-10, major): En commit-jobb i Losen-køen døde med EXIT=143 tolv sekunder etter start. Ingen feilmelding, ingen commit. Årsaken var min egen opprydding i et annet skript: `pkill -f "<appnavn>"`.
    - forebygging: Bruk aldri `pkill -f <mønster>` på en maskin der andre prosesser kan ha teksten i argv. Stopp en prosess ved PID du selv startet, eller ved `pgrep -x <prosessnavn>` kombinert med en sjekk av `ps -o comm=` mot den nøyaktige kjørbare stien. Dette gjelder særlig når en jobbkø kjører prompter som argument: alt du skriver i en prompt står på en kommandolinje et sted.
- **lesson.queue-job-file-before-prompt** (2026-09-10, minor): Køjobben `formaalskomposisjon-fullfor-commit-20260910-1020` ble avvist med «mangler promptfil» 13 sekunder etter at `.job` ble skrevet; promptfilen kom to sekunder etter avvisningen og ligger foreldreløs i `_losen-queue/inbox/`, der runneren aldri ser den igjen.
    - forebygging: Skriv `<id>.prompt.md` først og `<id>.job` sist, helst som `mv` fra en tmp-fil i samme mappe — `.job` er registreringssignalet, slik `job.json` er det i HavenAgentD::Docs/AgentJobs.md. Kan bli derivedTest: runneren eller `hd validate` rapporterer enhver `inbox/*.prompt.md` uten tilhørende `.job`, eldre enn to minutter, som foreldreløs.
- **lesson.pin-must-be-on-their-main** (2026-09-11, major): En revisjonspin i Package.swift pekte på en CellProtocol-revisjon som ikke lå på CellProtocol sin main. Koden bygde bare på den ene maskinen som hadde revisjonen liggende lokalt.
    - forebygging: Å pinne er riktig — det er det som gjør bygget reproduserbart. Kravet er at revisjonen er en forfar av avhengighetens egen main. Da er «bygg fra andres main» og «reproduserbart bygg» samme krav. HavenAgentD::Scripts/assert_dependencies_are_on_their_main.sh håndhever det, og CI kjører den. Lander du en klient før cellen den bruker er på den andres main, har du laget et repo som bare bygger hos deg.
- **lesson.a-red-baseline-is-a-question-not-an-answer** (2026-09-11, major): En rød baseline ble behandlet som en opplysning om prosjektet, og arbeidet gikk videre med et tiltak som gjorde den grønn. Tiltaket skjulte årsaken i stedet for å fjerne den.
    - forebygging: Svar på tre spørsmål før du gjør noe med en rød baseline: er utsjekket mitt likt origin? er CI grønn på origin/main? hvilken commit gjorde den rød, og hvem eier den? Først når svaret er «prosjektet er faktisk rødt» er det riktig å jobbe rundt det — og da som en egen, navngitt sak, ikke som en stille lokal omgåelse.
- **lesson.judgement-without-decoys-yields-all-yes** (2026-09-14, major): Første dommerrunde for formålsoppslag ga 197 «ja» og 0 «nei» på 197 rader. Fasiten skilte ikke mellom noen kandidater, og tidskurven (7 094 s på første oppgave, 25–44 s på de fem siste) viste at de siste var klikket gjennom, ikke dømt.
    - forebygging: En menneskelig fasit-runde skal alltid blande inn lokkeduer fra utenfor topp-10, blindt, så et «nei» kan attesteres og en alle-ja-dommer avsløres. Kriteriet skal kreve et navn («hvilket valg/test/avgrensning ville den endret»), ikke et ja. Maks fem oppgaver per økt. Og en runde uten negativer merkes instrumenteringsrunde — den teller ikke som fasit, samme regel som PurposeContract håndhever for null- og positiv referanse.
- **lesson.a-conditional-artifact-must-still-cost-something** (2026-09-18, minor): purpose_dev.py validate ble rød på PDD_entitetsdata-egen-kontroll fordi artefaktet 'skeleton/' manglet, selv om G1-GUI var godkjent på bilder Kjetil faktisk hadde sett. Pakken beskrev artefaktet som påkrevd «når Porthole-preview er brukt»; validatoren krevde det alltid.
    - forebygging: Et betinget krav oppfylles av et *annet krav*, aldri av et fravær. Feltet 'satisfiedByDeclaration' peker på en fil og en overskrift og krever minst ett punkt under den: enten viser du skjelett-JSON-en bildet er rendret fra, eller du skriver ned hva skjelettet ikke kan rendre. Begge tvinger frem spørsmålet «kan flaten dette?». Feilmeldingen navngir begge veier ut. Sjekket begge veier: rød uten erklæring, grønn med.
- **lesson.location-is-not-ownership** (2026-09-22, major): dataflow.md begrunnet at AIGateway matte ligge i appen med at «en gateway utenfor entiteten gjor prompten til noen andres data». Kjetil: en celle i skyen som eies av meg er pr definisjon innenfor min entitet.
    - forebygging: Regelen er uniform og gjelder alle scaffolds likt: ingen andre, scaffold-admin inkludert, nar data ELLER funksjonalitet i en celle jeg eier uten en Agreement som sier det. Et vern som bare gjelder skyen er et tegn pa at grensen er tegnet feil. Negative tester skal kjores i begge oppsett, lokalt og sky, og gi samme svar — og de skal dekke handlinger, ikke bare felter. Den positive motsatsen ma ogsa testes: en Agreement apner nayktig sitt eget omfang.
- **lesson.read-origin-main-before-writing-a-mechanism** (2026-09-22, major): Runde 1 av PDD_entitetsdata skrev en egen resolver for lenkede identiteter (EntityLinkAuthorizer, ny CellAuthorizationPath.linkedIdentity, ny hook pa GeneralCell). Da patchen ble lagt mot origin/main viste det seg at IdentityLinkRegistry og GeneralCell.authorizationEvidence allerede gjorde det samme, landet av en annen oppgave (purpose://candidate.entity-link.resolver-honours-link). Hele resolveren ble forkastet.
    - forebygging: Brief-audit skal si HVILKEN revisjon noe ble lest fra, og for et formal som skal endre en mekanisme skal kilden vaere origin/main (git show origin/main:<fil>), ikke utsjekket. Preflight-skriptet sjekker na at patchen passer mot origin/main i et eget worktree for noe legges pa. Og: for du skriver en mekanisme, grep pa main etter navnet pa det den skal gjore (her: sameEntity, linkedIdentity) - ikke bare etter typen du planlegger a lage.
- **lesson.dev-set-called-holdout** (2026-09-24, major): Nattens formålsmatching rapporterte 0,16 → 0,40 «holdout top-1». Astra viste at rundene 2–4 var designet mot feilene i den samme 40 %-delen, at 27 kandidater ble lest av mot den, og at valgene gain=3 og priorvekt 0,12 ikke var forhåndsbestemte treningsregler (andre verdier hadde identisk treningsmål). Tallet var reprodusert, men settet var et gjenbrukt utviklingssett. I samme rapport ble en håndskrevet spørreordstabell kalt «avledet av Book», og en nullinvariant («null tekst → null») holdt bare fordi et generisk spørreord ble regnet som tekstbevis.
    - forebygging: Kall ingenting holdout som har vært lest av mer enn én gang. Frys sluttvarianten, og gjør én evaluering på et sett skrevet og merket av noen som ikke har sett reglene eller modellutdata, splittet etter frasefamilie og forfatter, med størrelse avtalt før kjøring. Skriv utvalgsregelen for hyperparametre ned FØR runden. En invariant om «null bevis» må definere bevis som domeneforankret registertekst, ikke enhver positiv score. Kall en håndskrevet tabell håndskrevet.
- **lesson.same-writers-holdout-overstates** (2026-09-24, major): Butlers formålsgraf v3 løftet riktig forslag fra 20 % til 40 % på holdout, men bare fra 20 % til 28 % på 264 meldinger fra fire nye skribenter skrevet etter at grafen var frosset.
    - forebygging: Etter frysing: mål på et nytt korpus fra skribenter (personaer) som ikke har bidratt til treningen, og rapporter både holdout og uavhengig. Kall bare det uavhengige tallet generalisering.
- **lesson.sequential-ids-can-leak-labels** (2026-09-24, minor): Tolken var enig med generatoren i 264 av 264 meldinger når id-ene fulgte generatorens rekkefølge (etikett for etikett), og i 261 av 264 med tilfeldige, opake id-er.
    - forebygging: Gi tolken tilfeldige, opake id-er og stokket rekkefølge; behold kartet id→opak separat.
- **lesson.helper-bypassed-shared-negation-check** (2026-09-24, major): «bare så du vet, ikke gjør noe med det ennå: … flytte styremøtene til tirsdager» ga et møteforslag etter graf v3; bare det uavhengige korpuset viste det, og v3 var allerede i prod.
    - forebygging: Hver hjelper-scorer har en negativtest med «ikke/don't»; en ny scorer som ikke kaller den felles nektelsessjekken feiler testen. Mål på uavhengig korpus før prod, ikke etter.
- **lesson.method-lived-only-on-one-machine** (2026-09-24, major): Metoden selv — Book 35 (PDD-arbeidsflyten), Book 36, lærdomsregisteret med 50 lærdommer, formålspakkene, purpose_dev.py — lå bare i ett utsjekk på Kjetils Mac på grenen codex/docs-cleanup-20260810, aldri på main; derfor verken i HAVEN eller hos andre utviklere.
    - forebygging: Metodeartefakter landes som kode: PR til main og pin-oppdatering i HAVEN. Test: git cat-file -e origin/main:<fil> for hver metodefil.
- **lesson.readonly-git-is-not-all-git** (2026-09-24, minor): Et `git status` fra device_bash i CellProtocolDocuments etterlot .git/index.lock (0 byte) som ikke kunne fjernes fra VM-en, selv om git show/grep/log/rev-parse i samme økt ikke gjorde det.
    - forebygging: Fra device_bash bare objektlesende git mot en revisjon (git show/grep/log/cat-file <rev>); aldri status, diff mot arbeidstreet, add eller commit. Finnes en lås likevel: flytt den til _to_delete/ (mv virker, rm gjør ikke).
- **lesson.downstream-pin-must-come-from-the-consumer** (2026-09-24, major): Nedstrøms-baselinen for CellScaffold var rød 22.09 («cellprotocol krever swift-crypto 4.5.2, dimymint krever 3.x») og ble rapportert som prosjektets blokkering. CellScaffold main pinnet DiMyMint af41630, som løser swift-crypto 4.x; skriptet hadde hardkodet en eldre revisjon (1718fda).
    - forebygging: Et nedstrøms-skript leser alle transitive pinner fra forbrukerens egen Package.swift/Package.resolved på origin/main ved kjøring, og logger dem. En rød avhengighetsoppløsning i et skript med hardkodede pinner er ikke et funn før pinnene er bekreftet mot forbrukerens resolved.
- **lesson.disposable-worktree-must-be-reset-before-checkout** (2026-09-24, minor): pdd-check/Binding ble stående på 72f6a6c9 i to kjøringer selv om skriptet ba om origin/main: «Your local changes to project.pbxproj would be overwritten by checkout». Baselinen målte feil Binding-revisjon uten å si fra.
    - forebygging: Engangs-worktrees resettes hardt (`git reset --hard` + fjern Package.resolved) før hver utsjekk, og skriptet skriver ut revisjonen den faktisk står på — en avvikende revisjon skal stoppe kjøringen, ikke logges forbi.
- **lesson.report-the-commit-you-pushed-not-the-one-you-planned** (2026-09-24, minor): TESTRESULT og PLAN sa «commit ebb0b7f». Branchen sto på e66b7f1 — commit.sh hadde laget en ny hash — og var ikke pushet. Push-skriptets EXPECT måtte rettes før det kunne kjøre.
    - forebygging: Etter hver commit/push: les `git rev-parse --short HEAD` og `git ls-remote --heads origin <branch>` og lim inn utdataene i STATUS/TESTRESULT. Sjekk også for remote-tracking ref før du sier «pushet» (lesson.branch-is-empty-after-eight-work-packages, samme familie).
- **lesson.lookup-again-when-a-surface-is-added** (2026-09-24, major): De nye seksjonene i «Utvid entiteten» (B10) var portet på synlighet med rot-scope, og listen med verktøyets forespørsel forsvant — samme feil som lesson.unresolvable-condition-is-invisible fra 05.09.
    - forebygging: For hver ny eller endret skjelettflate: kjør `purpose_dev.py lookup --tags skeleton gui` før utformingen, og `BindingTests/CellConfigurationVerifierXCTest/testNoLocalSurfaceHidesItsOwnWaysIn` + `testPersonalCopilotLocalSurfacesLoadWithoutReferenceFailures` før flaten vises eller committes.
- **lesson.picker-state-keypath-is-read-and-written** (2026-09-24, minor): Velgeren «Verktøy» i «Gi tilgang» sto på «Velg verktøy» selv om cellen hadde valgt verktøyet.
    - forebygging: `selectionStateKeypath` skal være en nøkkel cellen både leser (`{selected}`) og skriver; test rundturen (`pickerSelectionRoundTrips`).
- **lesson.pairing-can-outlive-the-identity** (2026-09-24, major): Agenten var paret med en HAVEN-identitet fra 4. mai («Binding Local Session», nøkkel 13BF…), mens HAVEN brukte en annen privat identitet (D362…, identitetsfilen skrevet 18.09). Svar fra HAVEN ville blitt avvist; ingen test i noen av endene kunne se det.
    - forebygging: En flate som ber eieren signere for agenten sammenligner egen nøkkel med agentens forankring og viser forskjellen før signering, med vei til ny paring (test: `offerIsRefusedHereWhenThisHavenHoldsAnotherKey`, `theOwnerNeverSignsWhatFailedTheCheck`). Sjekk nøkkelkontinuitet før live-test av noe som signeres.
- **lesson.jxa-objc-method-without-arguments-is-a-property** (2026-09-24, minor): `a.terminate()` i JXA ga `TypeError: a.terminate is not a function`, men appene avsluttet likevel.
    - forebygging: Skriv `a.terminate` (uten parentes) og sjekk etterpå med `pgrep` at prosessen er borte før du går videre.
- **lesson.screencapture-from-runner-can-fail** (2026-09-24, minor): `screencapture -l <vindu>` fra jobbløperen ga «could not create image from window» for HAVEN-vinduet, med samme vindus-ID som computer use så.
    - forebygging: Ta bilder av flater med computer use (eller be Kjetil), og ikke planlegg bevis som avhenger av `screencapture` fra løperen før det er målt at det virker den dagen.
- **lesson.pgrep-pattern-must-allow-arguments** (2026-09-25, minor): Byggejobben avsluttet ikke HAVEN, og `open` hentet bare fram det gamle bygget (startet 24.09 17:29) i stedet for å starte det nye.
    - forebygging: Bruk 'HAVEN( |$)' i mønsteret, og skriv ut prosessens starttid etter omstart og sammenlign den med byggetiden før noe vises fram.
- **lesson.computer-use-image-is-not-a-file** (2026-09-25, minor): Skjermbildene av den nye flaten kunne ikke sendes til Kjetil som fil; vinduet var i tillegg på et annet skrivebord og kunne ikke gjøres større i bakgrunnen.
    - forebygging: Planlegg bildebeviset med en vei som gir en fil (Kjetils eget skjermbilde, eller skjermopptakstilgang for løperen), og si det før arbeidet, ikke etter.
- **lesson.green-gate-must-read-the-last-summary-line** (2026-09-26, major): runde2.sh committet og pushet 399f6d2 med 4 røde tester. Porten grep'et «Executed … with 0 failures» i hele loggen og traff en grønn suites linje lenger opp; siste linje sa «1262 tests, with 2 tests skipped and 8 failures».
    - forebygging: En grønn-port leser bare den siste «Executed»-linjen (tail -1) og krever « 0 failures (0 unexpected)». Sammenligningen gjøres uten pipe (POSIX case), fordi `echo | grep -q` under pipefail kan gi rødt på grønt (SIGPIPE). Porten skriver ut nøyaktig hva den sammenlignet.
- **lesson.module-and-type-share-a-name-in-cellprotocol** (2026-09-26, minor): `CellApple.EntityAnchorCell` og `CellVapor.EntityAnchorCell` kompilerte ikke: «type 'CellApple' has no member 'EntityAnchorCell'». Begge modulene har en type med samme navn som modulen.
    - forebygging: Én fil per modul som importerer bare den ene og gir typen et unikt typealias (TestSupport/AppleEntityAnchorAlias.swift, VaporEntityAnchorAlias.swift). Testfilen importerer ingen av modulene direkte.

## Book 23-noder som kan være forelder/gjenbruk (leksikalsk forslag, verifiser)
- purpose://test.acceptance.hallucination-evaluation [draft] — Hallucination evaluation gate

## 5. Avledede tester (samlet)

| testRef | Formål | Hvordan | Evidens | Status |
|---|---|---|---|---|
| test.build | purpose://quality.build-and-regression | Prosjektets byggkommando (xcodebuild / swift build / pytest) — angis i PLAN.md. | TESTRESULT.md#build | venter |
| test.regression | purpose://quality.build-and-regression | Prosjektets testkommando; sammenlign antall tester før/etter. | TESTRESULT.md#regression | venter |
| test.docs-updated | purpose://quality.docs-in-same-change | Les diff; kryss av i ACCEPT.md. | ACCEPT.md#docs | venter |
| test.status-current | purpose://quality.work-is-visible | Sammenlign STATUS.md med filene i mappen. | ACCEPT.md#status | venter |
| test.cell.contract-fixtures | purpose://cell.contract-explicit | python3 checks/validate_contract.py | TESTRESULT.md#contract | venter |
| test.cell.auth-negative | purpose://cell.authorization-honours-keypath | Tre enhetstester navngitt etter tilfellet. | TESTRESULT.md#auth | venter |
| test.cell.stub-scan | purpose://cell.no-empty-stubs | Søk i berørte filer; skriv listen i ACCEPT.md. | ACCEPT.md#stubs | venter |
| test.cells.dataflow-matches-contracts | purpose://cells.dataflow-declared | Tabell kant→kontrakt i PLAN.md. | PLAN.md#dataflow | venter |
| test.cells.capability-audit | purpose://cells.capabilities-declared-with-boundary | Tabell i FORMAALSSPEC.md §0. | FORMAALSSPEC.md#audit | venter |
| test.handoff.dry-run | purpose://handoff.runnable-without-guessing | ./<skript>.sh (uten --go) | TESTRESULT.md#dry-run | venter |
| test.maal.holdout-urort | purpose://measurement.gain-on-unseen-data | Les grafendringslogg: hver endring lister treningsrader. | TESTRESULT.md#forstaaelse | venter |
| test.maal.uavhengig-korpus | purpose://measurement.gain-on-unseen-data | score.py på korpus generert etter frysing | TESTRESULT.md#uavhengig | venter |
| test.maal.produksjonsvei | purpose://measurement.production-path | Les harnessen; kjør den. | TESTRESULT.md#forstaaelse | venter |
| test.maal.tilregnelighet | purpose://measurement.production-path | score.py på fixtures | TESTRESULT.md#forstaaelse | venter |
| test.maal.opake-id | purpose://measurement.honest-labels | Les tolk-inn-filene | TESTRESULT.md#fasit | venter |
| test.maal.lokkeduer | purpose://measurement.honest-labels | Les dommerbenk-nøkkelen etter dom | TESTRESULT.md#fasit | venter |
| test.maal.negativer | purpose://measurement.negatives-guarded | score.py, kolonnen negativer uten handling | TESTRESULT.md#forstaaelse | venter |
| test.palazzo.korpus-frosset | purpose://measurement.gain-on-unseen-data | Les korpusfila: 25 % holdout via id-hash, persona per rad, ingen rad endret etter frysing | TESTRESULT.md#fasit | venter |
| test.palazzo.tekst-til-noder | purpose://candidate.palazzo-signalforstaaelse.tekst-til-noder | score.py tabell A: presisjon/dekning per melding, sitatkrav per node | TESTRESULT.md#forstaaelse | venter |
| test.palazzo.dom-og-forklaring | purpose://candidate.palazzo-signalforstaaelse.dom-og-forklaring | score.py tabell B: dom per (melding × signal) + forklaring peker på gjestens ord | TESTRESULT.md#forstaaelse | venter |
| test.palazzo.veto-ufravikelig | purpose://candidate.palazzo-signalforstaaelse.veto-ufravikelig | Swift: for hver melding med negativ polaritet finnes ingen positiv kandidat for samme artikkel | TESTRESULT.md#veto | venter |
| test.palazzo.ingen-profil-over-grensen | purpose://candidate.palazzo-signalforstaaelse.ingen-profil-over-grensen | Inspeksjon: delingsfeltene i rapporten er nøyaktig dom + forklaring + tillitspakke | ACCEPT.md#grense | venter |
| test.palazzo.katalog-dumpet | purpose://measurement.honest-labels | Etikett-kartet er bygget fra `maaling/katalog.json` dumpet i samme kjøring | TESTRESULT.md#fasit | venter |
| test.palazzo.motstandsrunde | purpose://candidate.palazzo-signalforstaaelse.panel-kan-kjores-igjen | MOTSTAND-v1.md lister underkjente forslag, og forslagsfilene viser rettelsene | ACCEPT.md#motstand | venter |

## 6. Åpne spørsmål til Kjetil

1. **Hvor skal panelets forslag virke i første runde?** — **Besvart 2026-09-28: både husets signaler og tagger OG leksikonet og vektene i koden.** Konsekvens for treet: leksikon- og vektendringer går gjennom produksjonens kodevei, så `test.maal.produksjonsvei`, full regresjon og ny CI/deploy hører i planen; ingen endring begrunnes med en holdout-rad.
2. **Dommerbenken.** — **Besvart 2026-09-28: «Dere tar sølvfasiten.»** Første runde måles mot sølvfasit fra den blinde tolken; gullfasit med lokkeduer utsettes. Konsekvens: `test.maal.lokkeduer` står som `utsatt` med begrunnelse i TESTRESULT, og ingen tall fra denne runden kalles gullfasit.

### Nytt, fra samme melding (2026-09-28)

3. Kjetil møter Andre onsdag 30.9 og vil vise gjest, kelner og hus matching. Demoveien han valgte er
   en **lokal live demoflate** (se `PalazzoScaffold/docs/demo/README.md`). Den hører ikke til dette
   panelet, men den bruker samme kodevei panelet skal måle, og den første målingen kan derfor bruke
   samme lokale oppsett.

## 7. Revisjonslogg

| Iterasjon | Dato | Hva endret seg | Hvem |
|---|---|---|---|
| 0 | 2026-09-26 | Opprettet | Losen |
| 1 | 2026-09-26 | §0 audit, formålstre med rådgiverroller, avgrensning, forventningskontrakt, sju Palazzo-tester og to åpne spørsmål | Losen |
| 2 | 2026-09-28 | Kjetils svar på §6: forslagene skal virke både på husets signaler/tagger og på leksikon/vekter i kode; sølvfasit i første runde, gullfasit utsatt. Demoen til Andre 30.9 notert som egen leveranse | Losen |
