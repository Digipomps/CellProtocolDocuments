# Formålsspesifikasjon — Butler: onboarding som virker og synes, og AI-løs forståelse som treffer

Oppgavemappe: `PDD_butler-onboarding-og-formaalsforstaaelse_2026-09-23` · Opprettet 2026-09-23 · Iterasjon 1 (ikke godkjent)

> Regel: ingen plan før G1 er godkjent av Kjetil. For GUI: ingen implementering før G1-GUI (rendret bilde) er godkjent.
> Et dokument om leveransen teller aldri som leveransen.

## 0. Intensjon (ordrett) og brief-audit

Kjetil, 2026-09-23 (chat, midt i admin-leveransen):

> Jeg så endelig nytt butler design på prod - det var bra. Men jeg fikk "GuidedOnboardingCell is not available in this Porthole runtime" når jeg klikket på "Koble til modell". Vi må tydelig markere i chatten når vi er i gang med en chatbasert onboarding - kanskje en tekst i stedetfor "Skriv til Butler". Vi må vel også ha prompt om skriv api -nøkkel etc. Vi må også forbedre den ai-løse praten ved å ha en større graf med formål og matche mot. Vi må sette opp et løp hvor vi genererer opp naturlige meldinger til butleren - vi teste tolkningen med en kapabel men helst rask språkmodell og så tester vi matchingen med bare formål og justerer formålsgrafen så det blir riktigere treff. Det behøver ikke være perfekt men vi kan nå få det svært mye bedre enn det er i dag. Dokumenter metodikk som funker så vi kan gjenbruke det - for eksempel i kallimachos.

Alle kodepåstander er lest fra `origin/main` = `77a922bc` (arbeidstreet `CellScaffold/_wt-admin-levering-20260923`, som står på den revisjonen), jf. `lesson.read-origin-main-before-writing-a-mechanism`.

| Påstand i intensjonen / antatt kapabilitet | Audit | Kilde |
|---|---|---|
| Meldingen «GuidedOnboardingCell is not available in this Porthole runtime» kommer når «Koble til modell» trykkes | **retrieved** | `Sources/App/Cells/PersonalCopilot/PersonalCopilotCloudStore.swift:3084–3091` (`chatOnboardingAction`); knappen `chatHub.onboarding.start` i `PersonalCopilotConfigurationFactory.swift:1450` |
| Meldingen forteller hvorfor den feiler | **contradicted** | `scopedCellSet` (`PersonalCopilotCloudStore.swift:10228`) bruker `try?` både på oppslaget og på `set`. Uregistrert celle, nektet tilgang og kastet feil gir alle samme tekst. Rotårsaken i prod er **ukjent** til sonden `wp-onboarding-sonde.sh` har lest prods logg og runtime-manifest |
| `GuidedOnboardingCell` er registrert i resolveren | **retrieved**, men med forbehold | `configure.swift:1213` og `:1391` (`identityUnique`, persistent). I release-miljø kan registrering utsettes eller begrenses av eier-verifikasjon og det signerte runtime-manifestet (`configure.swift:1000–1060`); om det skjer for denne cellen er **ukjent** |
| Chatten har i dag ingen markering av at man er i onboarding | **retrieved** | Skrivefeltet har fast `placeholder: "Skriv til Butler …"` (`PersonalCopilotConfigurationFactory.swift:1699`) |
| Onboarding kan spørre om API-nøkkel | **retrieved** (i cellen, ikke i flaten) | `GuidedOnboardingCell.swift:96–113`: steg har `isSecret`, svaret redigeres bort (`never_returned_by_get`, `owner_scoped_cell_redacted`). Om *skrivefeltet* skjuler inndata når steget er hemmelig: **ukjent** — ikke funnet i fabrikken |
| Den AI-løse praten matcher mot en liten, håndskrevet formålsliste | **retrieved** | `ChatPurposeResourceRouter.swift:2320` `purposeLexicon` — 26 oppføringer i Swift-kode, pluss `tokenAliases` (`:3603`) og ordlikhet mot konfigurasjonsoppdagelse, dokumentasjon og RAG-saker |
| Det finnes en større formålsgraf å matche mot | **retrieved** | `Book/haven_purpose_knowledge_base_v0.json` (57 noder) og formålspakkene; `PDD_formaalsregister-som-graf_2026-09-11` (G1 12.09, G2 15.09) gjør registeret til graf og skal gi **én** matchemotor |
| Det finnes målemetode for formålsmatching | **retrieved** | `PDD_formaalsregister-som-graf_2026-09-11/handoff/TESTSTRATEGI_MATCHING.md` (+ `maaling/evaluer.py`, frosset korpus): TF-IDF beste utrente kandidat (R+@10 0,476), lærte vekter vinner bare på trening. `handoff/DOMMERBENK_MONSTER.md`: menneskelig dom med lokkeduer |
| Kallimachos har egen formålsmatching | **retrieved** | `Sources/App/Support/KallimachosCapabilityIndex.swift:299` `matchPurposes` — en fjerde håndrullet vei, i tillegg til de to WP4b i formaalsregister-som-graf skal fjerne og Butlers leksikon |
| En «kapabel men rask» språkmodell er tilgjengelig for løpet | **unavailable** | Ingen bestemt modell/nøkkel for et gjentakbart løp er avklart. Losen kan kjøre raske modeller som underagenter i en økt, men det er ikke det samme som et løp Kallimachos kan kjøre selv (se §6 Q1) |

## 1. Formålstre

Rot: **purpose://candidate.butler-forstaaelse.root** — *Butler forstår hva brukeren vil, også uten språkmodell, og brukeren ser alltid hvilken modus Butler er i.*

| purposeRef | Tittel | Forelder | Goal (outcome) | successSignals | Verifier | Status |
|---|---|---|---|---|---|---|
| purpose://candidate.butler-forstaaelse.root | Butler forstår og viser modus | — | Se over | Alle blad under er grønne | ACCEPT.md | candidate |
| purpose://candidate.butler-forstaaelse.onboarding | Veiledet onboarding virker og synes | root | En bruker uten modell kan koble til en modell fra chatten uten å bli forvirret om hva som skjer | A1–A4 grønne | ACCEPT.md#onboarding | candidate |
| purpose://candidate.butler-forstaaelse.onboarding.koble-til-modell-virker | «Koble til modell» starter onboardingen | onboarding | Klikk i prod og staging gir første steg, ikke en feilmelding | onboarding-tilstand `active` med `currentStep`; ingen `guided_onboarding_unavailable` | Kjetil klikker i prod (evidens: skjermbilde) + `test.onb.start-i-kjoerende-miljoe` | candidate |
| purpose://candidate.butler-forstaaelse.onboarding.feil-sier-hvorfor | Feil navngir årsaken | onboarding | Hvis onboardingen ikke kan starte, sier meldingen *hvilken* av tre årsaker (ikke registrert / nektet / steget avviste) | tre ulike `code`-verdier, én per årsak | `test.onb.tre-feil-tre-koder` | candidate |
| purpose://candidate.butler-forstaaelse.onboarding.synlig-modus | Chatten viser at vi er i onboarding | onboarding | Mens onboarding pågår står steget i skrivefeltet (i stedet for «Skriv til Butler …»), med steg x av n og en synlig vei ut | placeholder = stegets spørsmål; «Avbryt onboarding» nåbar | G1-GUI-bilde + `test.gui.parity` + `test.skeleton.purpose-actions-reachable` | candidate |
| purpose://candidate.butler-forstaaelse.onboarding.hemmelig-inndata | API-nøkkel skrives trygt | onboarding | Når steget er hemmelig, skjules tegnene i feltet, og nøkkelen havner aldri i chatloggen, i tilstand som kan leses, eller i logger | maskert felt; nøkkelen finnes ikke i transkript, `state` eller logg | `test.onb.noekkel-aldri-i-logg` | candidate |
| purpose://candidate.butler-forstaaelse.forstaaelse | AI-løs forståelse treffer mye bedre | root | Uten modell kobles vanlige meldinger til riktig formål langt oftere enn i dag, og «vet ikke» er ærlig | B1–B3 grønne | TESTRESULT.md#forstaaelse | candidate |
| purpose://candidate.butler-forstaaelse.forstaaelse.stoerre-graf | Matcher mot formålsregisteret, ikke 26 håndskrevne oppføringer | forstaaelse | Butlers AI-løse vei slår opp i den samme formålsgrafen som resten av HAVEN, gjennom den ene motoren formaalsregister-som-graf leverer | leksikonet i Swift er erstattet eller er data i grafen; ingen ny, femte matchevei | `test.reg.en-motor-i-kode` (fra formaalsregister-som-graf) + kodegjennomgang | candidate |
| purpose://candidate.butler-forstaaelse.forstaaelse.maalt-mot-fasit | Forbedringen er målt | forstaaelse | Treffrate før og etter på samme frosne korpus, med holdout | topp-1-treff og R@3 på holdout; forbedring med konfidensintervall | `test.fs.foer-etter-holdout` | candidate |
| purpose://candidate.butler-forstaaelse.forstaaelse.vet-ikke-er-aerlig | «Vet ikke» i stedet for feil gjetning | forstaaelse | Meldinger utenfor grafen gir `purpose://prompt.unknown` og tilbyr modell/bibliotek — ikke et galt formål | presisjon på negativ-/utenfor-settet | `test.fs.negativer` | candidate |
| purpose://candidate.butler-forstaaelse.loep | Et gjentakbart løp som forbedrer grafen | root | Én kommando går fra generering til rapport, og kan kjøres igjen etter hver grafendring | rapport med tall og feilliste per kjøring | `test.loep.en-kommando` | candidate |
| purpose://candidate.butler-forstaaelse.loep.naturlige-meldinger | Naturlige meldinger til Butler | loep | Et korpus av realistiske meldinger, fordelt på formål, personer og måter å si ting på (kort/langt, skrivefeil, indirekte, dialekt), pluss meldinger som *ikke* hører til noe formål | frosset, versjonert korpus med fordelingstabell; stikkprøve godkjent av Kjetil | `test.loep.korpus-fordeling` + `test.loep.stikkproeve` | candidate |
| purpose://candidate.butler-forstaaelse.loep.tolkning-med-rask-modell | Rask modell tolker, med lokkeduer | loep | En kapabel, rask modell setter formål på hver melding og kan svare «ingen»; uenighet med generatoren går til Kjetil i Dommerbenken, alltid med lokkeduer | sølvfasit + liten gullfasit; dommer skiller lokkedue fra ekte | `test.loep.lokkeduer-avsloeres` | candidate |
| purpose://candidate.butler-forstaaelse.loep.matching-bare-formaal | Matchingen måles uten modell | loep | Den AI-løse veien kjøres over korpuset og sammenlignes med fasiten | topp-1, R@3, MRR, negativpresisjon per formål | `test.fs.foer-etter-holdout` | candidate |
| purpose://candidate.butler-forstaaelse.loep.juster-grafen | Grafen justeres, ikke koden | loep | Feil fra målingen blir foreslåtte grafendringer (nye noder, fraser, relasjoner) som kan leses og godkjennes; holdout rører man ikke | hver endring har en feilrad den retter; holdout-tall rapporteres separat | `test.loep.endring-har-grunn` | candidate |
| purpose://candidate.butler-forstaaelse.metode | Metoden kan gjenbrukes | root | Det som virket — og det som ikke virket — står skrevet slik at en annen flate kan kjøre løpet med sin egen graf | metodedokument; Kallimachos kjører løpet med bare konfigurasjonsbytte | `test.metode.kallimachos-toerrkjoering` | candidate |

## 2. Avgrensning og avhengigheter

Hva dette IKKE er:
- **Ikke en ny matchemotor.** Formaalsregister-som-graf skal ende med én motor i produksjonsvei. Denne oppgaven leverer *korpus, fasit, måling og grafendringer* og kobler Butler til den motoren — den skriver ikke en femte vei.
- **Ikke språkmodell i den AI-løse veien.** Modellen brukes i løpet (generering, tolkning, dom) — aldri i produksjonsruten når brukeren ikke har koblet til en modell.
- **Et formålstreff gir aldri rettigheter** (`lesson.purpose-never-grants-rights`). Treff foreslår; handlinger krever fortsatt klikk og tilgang.
- **Ikke ekte brukermeldinger** uten samtykke. Korpuset er generert, og merket som generert.
- Ikke perfekt: målet er «svært mye bedre enn i dag», målt — ikke 100 %.

Kapabiliteter og avhengigheter:
| Kapabilitet | Kilde | Avgrensning | Må virke før test? |
|---|---|---|---|
| GuidedOnboardingCell løses og kan settes i prod | `configure.swift:1213/1391`, runtime-manifestet | Årsaken til dagens feil er ukjent til sonden er lest | ja — A1 |
| Hemmelige steg i onboarding | `GuidedOnboardingCell.swift:96–113` | Flaten (maskert felt) er ikke verifisert | ja — A4 |
| Formålsregisteret som graf | `Book/haven_purpose_knowledge_base_v0.json`; `PDD_formaalsregister-som-graf_2026-09-11` | Motorvalget (B2/WP4a) er ikke tatt. Løpet måler dagens vei og kandidatene mot samme korpus | ja — B1 |
| Målemetode og Dommerbenk | `TESTSTRATEGI_MATCHING.md`, `DOMMERBENK_MONSTER.md`, `Tools/PurposePackages/purpose_judgments.py` | Første dommerrunde ga 197 «ja» — lokkeduer er påkrevd | ja — C3 |
| Rask, kapabel språkmodell for løpet | — | Se §6 Q1 | ja — C2 |
| Kallimachos' matching | `KallimachosCapabilityIndex.swift:299` | Egen håndrullet vei; tørrkjøring med konfigurasjonsbytte er målet, ikke omskriving | nei — D2 |

## 3. Forventningskontrakt — «Det du kommer til å se»

| Leveranse | Type | Hvor | Referanse | Godkjent |
|---|---|---|---|---|
| Skrivefeltet i onboarding-modus (steg med spørsmål) | bilde → kjørende flate | Butler i prod og staging | `images/butler-onboarding-steg-v1.png` | nei |
| Skrivefeltet på API-nøkkel-steget (maskert) | bilde → kjørende flate | samme | `images/butler-onboarding-noekkel-v1.png` | nei |
| Onboarding som ikke kan starte, med årsak | bilde → kjørende flate | samme | `images/butler-onboarding-feil-v1.png` | nei |
| «Koble til modell» fungerer i prod | kjørende flate + skjermbilde | haven.digipomps.org | ditt klikk | nei |
| Korpus med naturlige meldinger + fordelingstabell | fil | `maaling/korpus/` | — | nei |
| Stikkprøve til Dommerbenken, med lokkeduer | kjørende flate (artefakt) | Dommerbenken | — | nei |
| Før/etter-rapport: treffrate på holdout | testutdata | `TESTRESULT.md#forstaaelse` | — | nei |
| Grafendringer med begrunnelse per endring | fil (diff) | `maaling/grafendringer/` | — | nei |
| Metodedokument (hva virket / hva ikke virket) | fil | `Book/` + denne mappen | — | nei |
| Kallimachos-tørrkjøring med samme løp | testutdata | `TESTRESULT.md#kallimachos` | — | nei |

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
- **pkg.std.gui-surface** — GUI-flate (bilde før kode)
    - purpose://gui.expectation-agreed-before-build: Et rendret bilde per flate/tilstand er godkjent av Kjetil og lagret som referanse i oppgavemappen.
        - test test.gui.reference-image-exists [artifact]: Godkjent referansebilde finnes for hver flate og hver viktig tilstand (tom, fylt, feil). → images/
    - purpose://gui.parity-with-approved-image: Screenshot av faktisk flate ligger side om side med referansebildet i ACCEPT.md, og alle avvik er enten rettet eller godkjent av Kjetil med begrunnelse.
        - test test.gui.parity [inspection]: Side-om-side referanse/faktisk per flate. → ACCEPT.md#parity
    - purpose://gui.surface-loads-in-time: Flaten er synlig innen terskelen angitt i FORMAALSSPEC.md (standard 5 s) på det avtalte miljøet.
        - test test.gui.load-time [measurement]: Lastetid ≤ terskel, tre forsøk. → TESTRESULT.md#load-time
    - purpose://gui.ways-in-are-reachable: SkeletonReachabilityAudit rapporterer ingen elementer som aldri kan sees, og handlingene FORMAALSSPEC §3 navngir finnes i reachableActionKeypaths.
        - test test.skeleton.no-unreachable-elements [command]: Ingen flate har elementer som aldri kan sees; funn navngir handlingene som gaar tapt. → TESTRESULT.md#reachability
        - test test.skeleton.purpose-actions-reachable [inspection]: Hver handling forventningskontrakten (§3) navngir finnes i flatens reachableActionKeypaths. → ACCEPT.md#ways-in
    - artefakt images/ (port G1-GUI): Godkjente referansebilder, ett per flate og tilstand.
    - artefakt skeleton/ (port G1-GUI): CellConfiguration/skeleton-JSON som bildet er rendret fra. Er bildet en mockup i stedet for Porthole-preview, kreves i stedet en renderingserklæring i images/README.md som lister hva skjelettet ikke kan rendre.
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

## Lærdommer du må lese før dekomponering
- **lesson.text-ux-is-not-design** (2026-05-06, major): Kjetil forventet en helt annen flate enn den som ble vist; den tekstlige UX-beskrivelsen var godkjent, bildet var det ikke.
    - forebygging: Rendret bilde (Porthole-preview eller mockup) godkjennes før implementering; bildet er akseptansereferanse.
- **lesson.parity-was-correctness-not-decoration** (2026-05-06, major): Parity-audit mellom Porthole og Binding viste at problemet ikke var manglende dekorasjon, men produktkorrekthet (feil oppførsel).
    - forebygging: Akseptanse sammenligner både bilde og oppførsel (knapper trigger keypaths, felt tar input) — begge i ACCEPT.md.
- **lesson.surface-load-alias-miss** (2026-08-24, blocker): Flatelasting tok 46 541 ms (klientens 45 s-timeout) ved bom, 5 000 ms ved treff; målingen 10.08 målte en mislykket lasting.
    - forebygging: Mål lastetid tre ganger og sjekk logg for navnebom før en flate erklæres ferdig; aliaser må løses server-side eller ikke brukes.
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
- **lesson.corr-approval-surfaces-timed-out** (2026-08-30, major): Corr-godkjenningen (Vegar) er utestet fordi flater/godkjenninger timet ut før testing rakk å skje.
    - forebygging: FORMAALSSPEC.md §2 lister avhengigheter som egne formål med verifier; pkg.std.everything-works og gui.surface-loads-in-time må være grønne før den egentlige testen kjøres.
- **lesson.unresolvable-condition-is-invisible** (2026-09-05, blocker): Relasjoner-flaten viste tittel og ingen vei inn: ingen filopplasting, ingen knapper. Alle tester gronne.
    - forebygging: SkeletonReachabilityAudit kjores over hver flate; test.skeleton.no-unreachable-elements feiler med elementene som aldri kan sees og handlingene som gaar tapt med dem. Betingelser hoerer hjemme inne i List/Grid/Reference-rader, der radens verdi sendes videre; ellers skal cellen avgjore og innhold bindes.
- **lesson.test-corpus-is-not-shipped-corpus** (2026-09-05, major): Rot-probe-testen, lastetidstesten og finnbarhetsauditen var gronne i to uker mens Relasjoner-flaten var tom.
    - forebygging: Enhver flate-test skal bygge korpuset fra det som faktisk sendes ut (menykonfigurasjoner + navigasjonsdestinasjoner + verifiseringshjelperen), dedupliseres, og feile hvis korpuset er mindre enn appens egen meny.
- **lesson.tested-a-different-path-than-production** (2026-09-05, major): Rot-probene leste relations.state.* gjennom porthole.get og var gronne, mens rendereren aldri fikk de samme dataene.
    - forebygging: Naar en test skal si noe om hva brukeren ser, maa den bruke produksjonens egen kodevei - helst produksjonens egen funksjon med produksjonens egne inndata (SkeletonReachabilityAudit kaller condition.evaluate(root: nil, ...) nettopp derfor).
- **lesson.findability-is-not-usability** (2026-09-05, major): Flatene ble kalt validert fordi de bestod en beskrivelsesaudit; de var samtidig ubrukelige.
    - forebygging: En formaalssjekk maa navngi handlingene eieren skal kunne utfore, og testes mot SkeletonReachabilityAudit.reachableActionKeypaths - ikke mot hvor godt formaalet er formulert.
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
- **lesson.ciphertext-field-held-plaintext-hash** (2026-09-10, blocker): Losen fortalte Kjetil at lyd allerede var kryptert i lagring. Det var feil: filene i prod begynner med ID3 og er vanlig MP3. To ting forte dit. (1) Krypteringskoden som ble lest tilhorer MusicIngestCell paa /mvp/ingest/local, mens Butterpop publiserer gjennom MusicAssetStoreCell.storeLocalAsset, som skriver bytene slik de kommer. (2) storeLocalAsset setter ciphertextSHA256 = plaintextSHA256 = sha256(data), saa manifestet ser kryptert ut selv naar encryptionPolicy er none.
    - forebygging: En paastand om at noe er kryptert, signert eller verifisert skal bekreftes paa artefaktet - les bytene, ikke feltet. Et felt som heter ciphertext* skal ikke settes naar encryptionPolicy er none; enten utelates det, eller navnet sier hva det er. Kan bli derivedTest: manifest med encryptionPolicy none har ingen ciphertext-verdi.
- **lesson.local-main-is-not-main** (2026-09-11, major): WP0-baselinen var rød og ble meldt som «main bygger ikke». Det var feil. Den commiten baselinen ble målt mot, `ba14895`, lå bare på den LOKALE main-grenen og var aldri pushet; den avhang av CellBase-kode som heller ikke var pushet. origin/main lå fire commits lenger fram, pinnet CellProtocol til en revisjon som ER på CellProtocol sin main, og hadde grønn CI hele tiden. Et helt døgns arbeid ble bygget oppå den lokale commiten.
    - forebygging: Før du måler en baseline eller sier at main er rød: `git fetch origin main` og sammenlign. Er lokal main foran origin/main, er de commitene ikke main for andre — bygg aldri videre på dem. Se på CI for origin/main før du konkluderer. `swift package edit` skal aldri være på når noe måles eller meldes verifisert. Og den eneste sjekken som virkelig avgjør: klon fra GitHub til en tom katalog og bygg der. HavenAgentD::Scripts/preflight_before_landing.sh stiller alle fire spørsmålene.
- **lesson.a-new-red-test-needs-a-repeated-baseline** (2026-09-10, minor): Første fulle kjøring med nye endringer viste to røde i stedet for baselinens én, og den nye lå i en fil jeg hadde endret. Det så ut som en regresjon jeg hadde innført.
    - forebygging: Når en ny rød dukker opp: kjør basen på nytt, i et eget rent worktree, **flere ganger** (tre holder som regel), før du enten tar på deg feilen eller avfeier den. Skriv resultatet av gjentakelsen i TESTRESULT — «2 av 3 på ren base» er et svar, «den er nok flaky» er ikke. Det koster ti minutter og avgjør om du bruker natten på å jage din egen feil eller andres.
- **lesson.swift-test-exit-code-lies-in-havenagentd** (2026-09-10, minor): `swift test` i HavenAgentD avslutter med 1 selv når samtlige 212 tester passerer. Et skript som leser `$?` melder rødt på et helt grønt tre.
    - forebygging: Les resultatet fra linjen `Test run with N tests in M suites passed/failed`, ikke fra exitkoden, i alle skript og køjobber for dette repoet. Og fjern det tomme XCTest-målet, eller bygg det for riktig arkitektur, før noen setter opp CI her — ellers vil CI være rød uansett hva som gjøres.
- **lesson.pin-must-be-on-their-main** (2026-09-11, major): En revisjonspin i Package.swift pekte på en CellProtocol-revisjon som ikke lå på CellProtocol sin main. Koden bygde bare på den ene maskinen som hadde revisjonen liggende lokalt.
    - forebygging: Å pinne er riktig — det er det som gjør bygget reproduserbart. Kravet er at revisjonen er en forfar av avhengighetens egen main. Da er «bygg fra andres main» og «reproduserbart bygg» samme krav. HavenAgentD::Scripts/assert_dependencies_are_on_their_main.sh håndhever det, og CI kjører den. Lander du en klient før cellen den bruker er på den andres main, har du laget et repo som bare bygger hos deg.
- **lesson.a-red-baseline-is-a-question-not-an-answer** (2026-09-11, major): En rød baseline ble behandlet som en opplysning om prosjektet, og arbeidet gikk videre med et tiltak som gjorde den grønn. Tiltaket skjulte årsaken i stedet for å fjerne den.
    - forebygging: Svar på tre spørsmål før du gjør noe med en rød baseline: er utsjekket mitt likt origin? er CI grønn på origin/main? hvilken commit gjorde den rød, og hvem eier den? Først når svaret er «prosjektet er faktisk rødt» er det riktig å jobbe rundt det — og da som en egen, navngitt sak, ikke som en stille lokal omgåelse.
- **lesson.judgement-without-decoys-yields-all-yes** (2026-09-14, major): Første dommerrunde for formålsoppslag ga 197 «ja» og 0 «nei» på 197 rader. Fasiten skilte ikke mellom noen kandidater, og tidskurven (7 094 s på første oppgave, 25–44 s på de fem siste) viste at de siste var klikket gjennom, ikke dømt.
    - forebygging: En menneskelig fasit-runde skal alltid blande inn lokkeduer fra utenfor topp-10, blindt, så et «nei» kan attesteres og en alle-ja-dommer avsløres. Kriteriet skal kreve et navn («hvilket valg/test/avgrensning ville den endret»), ikke et ja. Maks fem oppgaver per økt. Og en runde uten negativer merkes instrumenteringsrunde — den teller ikke som fasit, samme regel som PurposeContract håndhever for null- og positiv referanse.
- **lesson.a-conditional-artifact-must-still-cost-something** (2026-09-18, minor): purpose_dev.py validate ble rød på PDD_entitetsdata-egen-kontroll fordi artefaktet 'skeleton/' manglet, selv om G1-GUI var godkjent på bilder Kjetil faktisk hadde sett. Pakken beskrev artefaktet som påkrevd «når Porthole-preview er brukt»; validatoren krevde det alltid.
    - forebygging: Et betinget krav oppfylles av et *annet krav*, aldri av et fravær. Feltet 'satisfiedByDeclaration' peker på en fil og en overskrift og krever minst ett punkt under den: enten viser du skjelett-JSON-en bildet er rendret fra, eller du skriver ned hva skjelettet ikke kan rendre. Begge tvinger frem spørsmålet «kan flaten dette?». Feilmeldingen navngir begge veier ut. Sjekket begge veier: rød uten erklæring, grønn med.
- **lesson.read-origin-main-before-writing-a-mechanism** (2026-09-22, major): Runde 1 av PDD_entitetsdata skrev en egen resolver for lenkede identiteter (EntityLinkAuthorizer, ny CellAuthorizationPath.linkedIdentity, ny hook pa GeneralCell). Da patchen ble lagt mot origin/main viste det seg at IdentityLinkRegistry og GeneralCell.authorizationEvidence allerede gjorde det samme, landet av en annen oppgave (purpose://candidate.entity-link.resolver-honours-link). Hele resolveren ble forkastet.
    - forebygging: Brief-audit skal si HVILKEN revisjon noe ble lest fra, og for et formal som skal endre en mekanisme skal kilden vaere origin/main (git show origin/main:<fil>), ikke utsjekket. Preflight-skriptet sjekker na at patchen passer mot origin/main i et eget worktree for noe legges pa. Og: for du skriver en mekanisme, grep pa main etter navnet pa det den skal gjore (her: sameEntity, linkedIdentity) - ikke bare etter typen du planlegger a lage.

## Book 23-noder som kan være forelder/gjenbruk (leksikalsk forslag, verifiser)
- purpose://skeleton.owner-entity-access [draft] — Owner entity access affordance
- purpose://test.acceptance.hallucination-evaluation [draft] — Hallucination evaluation gate
- purpose://self-determination.data.use-purpose [candidate] — Purpose binding for data use

## 5. Avledede tester (samlet)

| testRef | Formål | Hvordan | Evidens | Status |
|---|---|---|---|---|
| test.onb.start-i-kjoerende-miljoe | purpose://candidate.butler-forstaaelse.onboarding.koble-til-modell-virker | Klikk «Koble til modell» i staging og prod; les onboarding-tilstanden etterpå | TESTRESULT.md#onb-start + skjermbilde | venter |
| test.onb.tre-feil-tre-koder | purpose://candidate.butler-forstaaelse.onboarding.feil-sier-hvorfor | Enhetstest: uregistrert celle, nektet tilgang og avvist steg gir tre ulike `code` | TESTRESULT.md#onb-feil | venter |
| test.onb.noekkel-aldri-i-logg | purpose://candidate.butler-forstaaelse.onboarding.hemmelig-inndata | Svar på hemmelig steg med en kjent nøkkel; søk etter den i transkript, `state`, `get`-svar og logg — null treff | TESTRESULT.md#onb-noekkel | venter |
| test.gui.parity | purpose://candidate.butler-forstaaelse.onboarding.synlig-modus | Skjermbilde av kjørende flate ved siden av godkjent bilde, per tilstand | ACCEPT.md#parity | venter |
| test.skeleton.purpose-actions-reachable | purpose://candidate.butler-forstaaelse.onboarding.synlig-modus | «Avbryt onboarding» og stegets svar-handling finnes i `reachableActionKeypaths` | ACCEPT.md#ways-in | venter |
| test.loep.korpus-fordeling | purpose://candidate.butler-forstaaelse.loep.naturlige-meldinger | Fordelingstabell: meldinger per formål, stil og negativ-andel; minste antall per formål | TESTRESULT.md#korpus | venter |
| test.loep.stikkproeve | purpose://candidate.butler-forstaaelse.loep.naturlige-meldinger | Kjetil ser 20 tilfeldige meldinger i Dommerbenken: «ville en bruker skrevet dette?» | Dommerbenken-eksport | venter |
| test.loep.lokkeduer-avsloeres | purpose://candidate.butler-forstaaelse.loep.tolkning-med-rask-modell | Hver dommeroppgave har blinde lokkeduer; en runde der lokkeduene får «ja» teller ikke som fasit | TESTRESULT.md#dom | venter |
| test.fs.foer-etter-holdout | purpose://candidate.butler-forstaaelse.forstaaelse.maalt-mot-fasit, purpose://candidate.butler-forstaaelse.loep.matching-bare-formaal | Kjør dagens vei og ny vei på samme frosne korpus; rapporter topp-1, R@3, MRR på holdout med intervall | TESTRESULT.md#forstaaelse | venter |
| test.fs.negativer | purpose://candidate.butler-forstaaelse.forstaaelse.vet-ikke-er-aerlig | Andel negativmeldinger som får `prompt.unknown` (og ikke et galt formål) | TESTRESULT.md#negativer | venter |
| test.reg.en-motor-i-kode | purpose://candidate.butler-forstaaelse.forstaaelse.stoerre-graf | Fra formaalsregister-som-graf: bare én matchemotor i produksjonsvei | TESTRESULT.md#konformans | venter |
| test.loep.endring-har-grunn | purpose://candidate.butler-forstaaelse.loep.juster-grafen | Hver grafendring peker på feilraden(e) den retter; holdout er ikke brukt til å velge endringer | `maaling/grafendringer/` | venter |
| test.loep.en-kommando | purpose://candidate.butler-forstaaelse.loep | Én kommando kjører generering → tolkning → matching → rapport med fast seed | TESTRESULT.md#loep | venter |
| test.metode.kallimachos-toerrkjoering | purpose://candidate.butler-forstaaelse.metode | Samme løp mot Kallimachos' formål med bare konfigurasjonsbytte | TESTRESULT.md#kallimachos | venter |
| test.build / test.regression / test.docs-updated / test.status-current | pkg.std.everything-works | Som pakken sier | TESTRESULT.md / ACCEPT.md | venter |

## 6. Åpne spørsmål til Kjetil — besvart 2026-09-23 (AskUserQuestion)

| # | Spørsmål | Kjetils svar | Hva det endrer |
|---|---|---|---|
| Q1 | Hvilken modell kjører løpet? | **Start med Losen, bytt modell senere.** Losen genererer, raske underagenter tolker; skriptet får en modellkobling som kan byttes (API-nøkkel eller HAVENs egen kobling) | C2 bygges med et utbyttbart `tolker`-grensesnitt; D2 (Kallimachos) forutsetter ikke en bestemt modell |
| Q2 | Språk i korpuset | **Bokmål og engelsk.** Nynorsk/dialekt kan komme som egen stil senere | Korpusfordelingen har språk som akse; minst-per-formål gjelder per språk |
| Q3 | A1+A2 før G1 som feilretting? | **Ja, rett det nå.** | A2 (feilen sier hvorfor) implementeres straks, i admin-leveransen som bygges; A1 (selve årsaken) følger når årsaken er synlig |
| Q4 | To nye skeleton-kapabiliteter? | **Nye felt i CellProtocol:** `placeholderKeypath` og `secure`, i CellProtocol, web- og native-renderer, testet mot funksjon og formål før main | Egen arbeidspakke i CellProtocol med paritetstest; A3/A4 avhenger av den |

## 7. Revisjonslogg

- 2026-09-24: Tillegg (T0–T5) for læring under bruk og metodikken i HAVEN, etter Kjetils ønske samme formiddag og tre svar. Nederst i dokumentet.

| Iterasjon | Dato | Hva endret seg | Hvem |
|---|---|---|---|
| 0 | 2026-09-23 | Opprettet | Losen |
| 1 | 2026-09-23 | §0 ordrett + audit mot origin/main 77a922bc; tre med 4 grener og 14 blad; avgrensning mot formaalsregister-som-graf (én motor); forventningskontrakt; tester; tre spørsmål | Losen |
| 2 | 2026-09-23 | §6 besvart (Q1–Q4) | Kjetil / Losen |

---

## Tillegg 2026-09-24 — læring under bruk, og metodikken i HAVEN

### T0. Intensjon (ordrett) og brief-audit

> Vi bør legge opp strategier for å teste forbedringer under bruk også. Slik at man kan teste ut justeringer i formål og vekting og se om man får bedre treff og så lære av det. (eventuell tilgang til andre entiteters data må selvfølgelig godkjennes av den enkelte entiteten). Generell lærdom - er vel egentlig metodikk - bør bli tilgjengelig i HAVEN. Gå videre med G2

Svar samme formiddag (AskUserQuestion): skyggemåling på egne data **på som standard, kan slås av**; ved samtykke **velger entiteten nivå**; grafen skal bo **i en celle i HAVEN, versjonert**.

| Påstand eller antakelse | Status | Kilde (lest fra `origin/main` `6c70a592` i CellScaffold, `origin/main` i CellProtocol) |
|---|---|---|
| Butler lærer allerede av bruk | **retrieved, men bare per bruker og av som standard** | `assistant.acceptSuggestion`/`dismissSuggestion` → `recordAssistantLearning` (`PersonalCopilotCloudStore.swift`, ~l. 13786). Vekt per formål = basis + 0,05 per godtatt − 0,04 per avvist (`purposeWeightObject`), brukt som `rå × (0,75 + vekt × 0,25)`. Nye hendelser registreres bare når `learningEnabled` er på (standard `false`, l. 987); vekter fra tidligere hendelser leses uansett (Astra, l. 13809/14445). |
| Vi vet om læringen gir bedre treff | **contradicted** | Læringshendelsene lagrer formål, utfall og sikkerhet, ikke hvilken grafversjon som ga forslaget og ikke hva en annen versjon ville gitt. Ingenting sammenligner. |
| Brukerens egne meldinger finnes som materiale | **retrieved** | Chatloggen `ui.promptMessages` er persistert per bruker, med meldingen og Butlers svar med `purposeRef`. Hemmelige svar er allerede skjult (`helperPromptLogBody`). |
| Justeringer krever ny kode | **retrieved** | Leksikonet er Swift-literaler (`ChatPurposeResourceRouter.purposeLexicon`), hjelper-scorerne likeså. Fra merge til prod tok graf v3 3 t 35 min. B1 i godkjent G2 flytter dem til data. |
| Samtykke mellom entiteter har en mekanisme | **retrieved (byggestein), ikke for dette formålet** | `Agreement` (CellProtocol `Sources/CellBase/Agreement/Agreement.swift`) med signatarer, betingelser og grants. Forbilde: `ConferenceInsightAggregateCell` — «Only participants with organizerInsights consent contribute signals». Ingen avtaletype for bidrag til formålsgrafen finnes (grep på `origin/main`). |
| Book finnes i HAVEN | **retrieved** | `Dockerfile` l. 118–122 kopierer `CellProtocolDocuments/Book` inn i imaget; submodulen er pinnet til `a08f72f3`. Kapittel 38 er skrevet, men bare lokalt (ucommittet) i `CellProtocolDocuments`, som har 496 ucommittede endringer fra andre oppgaver. |
| Én motor for formålsmatching | **retrieved: ikke valgt** | `PDD_formaalsregister-som-graf_2026-09-11/STATUS.md`: motorvalget «kan ikke avgjøres uten måling X» (WP4a). B1 i vår plan sier: ingen femte matchevei. |

### T1. Formålstre (tillegg)

To nye grener under roten.

| purposeRef | Tittel | Forelder | Goal (outcome) | successSignals | Verifier | Status |
|---|---|---|---|---|---|---|
| purpose://candidate.butler-forstaaelse.laering-under-bruk | Forbedringer prøves under bruk | root | En justering i formål eller vekting kan prøves på ekte bruk, måles mot det folk faktisk gjør, og tas i bruk eller forkastes med grunn | E1–E6 grønne | ACCEPT.md#laering | candidate |
| …laering-under-bruk.graf-i-celle | Grafen bor i en versjonert celle | laering-under-bruk | Leksikon og vekter er data i en celle; Butler leser dem; en versjon kan byttes og rulles tilbake uten utrulling | startversjonen gir samme resultat som graf v3.1 på korpus v1 og v2; en dataendring endrer et treff i en test uten kodeendring; bytte og tilbakerulling i staging på minutter | test + måling | candidate |
| …laering-under-bruk.skygge-egne-data | Kandidaten regner i skyggen på egne meldinger | laering-under-bruk | For hver melding regner en kandidatversjon ved siden av; brukeren ser ingen forskjell; resultatet blir i brukerens egen celle. På som standard, kan slås av | `analyzeDraft` gir identisk svar med skygge på og av; hendelsen har prod-versjon, prod-forslag, kandidatversjon, kandidatforslag; av-bryteren stopper registreringen | test | candidate |
| …laering-under-bruk.utfall-fra-bruk | Det brukeren gjør blir et utfall | laering-under-bruk | Godtatt, avvist, valgte et annet alternativ, eller skrev om kort etter, registreres med grafversjonen som ga forslaget. Ingen meldingstekst i hendelsen | hver hendelse har utfall og versjon; ingen tekst | test | candidate |
| …laering-under-bruk.samtykke-per-entitet | Entiteten velger selv om og hvor mye den bidrar | laering-under-bruk | Nivå 0 (standard): ingenting forlater entiteten. Nivå 1: tellinger per formål og versjon. Nivå 2: i tillegg meldinger med navn og tall fjernet, som entiteten har sett og godkjent. Avtalen kan trekkes | uten avtale er eksporten tom; nivå 1 har ingen tekst; nivå 2 har bare godkjente, vaskede meldinger; trukket avtale stopper neste eksport | test | candidate |
| …laering-under-bruk.fra-bruk-til-korpus | Samtykkede meldinger blir nytt korpus | laering-under-bruk | Nivå 2-meldinger går gjennom samme løp som korpus v1/v2 (tolk med opake id-er, Dommerbenken, holdout) og blir et nytt, frosset korpus | korpus v3 finnes med fasit og fordeling | artefakt | candidate |
| …laering-under-bruk.promotering-med-vern | En kandidat tas i bruk bare med vern | laering-under-bruk | Offline: ikke dårligere på korpus v1, v2 og PromptPurposeLab, ingen tap på negativer. I skygge: over N meldinger ikke lavere godtatt-andel og ikke flere forslag brukeren ikke ba om. Tilbakerulling er et versjonsbytte | promoteringsrapport med begge delene; tilbakerulling prøvd i staging | måling | candidate |
| purpose://candidate.butler-forstaaelse.metodikk-i-haven | Metoden finnes i HAVEN | root | Den som skal måle en matcher i HAVEN finner metoden, reglene og lærdommene i HAVEN selv, ikke bare i en PDD-mappe | F1–F3 grønne | ACCEPT.md#metodikk | candidate |
| …metodikk-i-haven.bok-kapittel | Kapittel 38 i HAVENs bok i prod | metodikk-i-haven | Kapittelet kan leses i HAVEN i prod | kapittelet står i `book_catalog.json` på `CellProtocolDocuments` main; submodulen i CellScaffold peker dit; prod viser det | skjermbilde fra prod | candidate |
| …metodikk-i-haven.formaalspakke | Metoden er en standard formålspakke | metodikk-i-haven | Når en PDD handler om matching eller evaluering, festes pakken automatisk med de ti reglene som avledede tester | `purpose_dev.py lookup --tags matching,evaluering` skriver ut pakken | kommando | candidate |
| …metodikk-i-haven.laerdommer | Nattens lærdommer i registeret | metodikk-i-haven | Lærdommene fra 23.–24.09 står i `haven_lessons_register_v0.json` og vises ved neste dekomponering | `lookup` viser dem | kommando | candidate |

### T2. Avgrensning og avhengigheter (tillegg)

Ikke en del av dette: trening av språkmodeller; deling av data mellom entiteter uten avtale; A/B der brukeren ser en annen Butler uten å vite det (skyggen endrer aldri det brukeren ser); metoden som egne celler i HAVEN (neste steg, eget formål).

| Avhengighet | Verifier |
|---|---|
| Grafen i celle (E1) før skygge (E2) og promotering (E6) | E1-testene grønne |
| E1 bruker nodeformatet fra formålsregister-som-graf når motoren er valgt; til da er cellen den ene veien Butler leser, og Swift-literalene fjernes (ingen femte matchevei) | kodegjennomgang: literalene er borte etter E1 |
| Samtykke (E4) før noe forlater en entitet | E4-testene grønne; uavhengig gjennomgang av Astra før prod |
| F1 går fra et rent arbeidstre fra `origin/main`, ikke fra det delte utsjekket med 496 fremmede endringer | commit inneholder bare kapittel 38, katalogoppføringen, pakken og lærdommene |

### T3. Forventningskontrakt — «Det du kommer til å se» (tillegg)

| Leveranse | Type | Hvor |
|---|---|---|
| Kapittel 38 åpnet i HAVEN i prod | kjørende flate + skjermbilde | `images/metodikk-kap38-prod.png` |
| Formålspakken skrevet ut av `purpose_dev.py lookup` | kommandoutdata | TESTRESULT.md#metodikk |
| Nattens lærdommer i registeret | fil-diff | `Book/haven_lessons_register_v0.json` |
| Graf v3.1 som data i en celle, samme tall på korpus v1 og v2 som i Swift | måling + testutdata | TESTRESULT.md#graf-i-celle |
| Versjonsbytte og tilbakerulling i staging | logg | `evidence/graf-i-celle/` |
| Skyggehendelser fra din egen Butler: prod-forslag, kandidatforslag, hva du gjorde | kjørende + rapport | `evidence/skygge/` (egen visning i Butler kommer med G1-GUI) |
| Samtykkeavtalen med tre nivåer, og testene for 0/1/2/trukket | fil + testutdata | `contract/samtykke-bidrag.md`, TESTRESULT.md#samtykke |
| Første promoteringsrapport | rapport | `maaling/promotering/` |

### T5. Avledede tester (tillegg)

test.lub.graf-i-celle-samme-tall (måling), test.lub.dataendring-endrer-treff (command), test.lub.bytte-og-tilbakerull (command, staging), test.lub.skygge-endrer-ikke-svaret (command), test.lub.skygge-av-stopper (command), test.lub.utfall-uten-tekst (command), test.lub.samtykke-0-1-2-trukket (command), test.lub.promotering-har-vern (inspection), test.met.kap38-i-prod (artifact), test.met.pakke-i-lookup (command), test.met.laerdommer-i-lookup (command).
