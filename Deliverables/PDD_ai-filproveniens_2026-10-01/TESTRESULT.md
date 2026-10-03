# TESTRESULT — HD-0154, 2026-10-03

G1, G1-GUI og G2 er godkjent. G3 er fortsatt åpen. Implementeringen er ikke komplett, aktivert eller deployet.

| Kandidat | Head | Review |
|---|---|---|
| CellProtocol | e8c158ab79f18c68d84982f3f6abcea2dd5b6044 | https://github.com/Digipomps/CellProtocol/pull/57 |
| HavenAgentD | b5adebd3e85f859b8d99c7963f7c44a5be7dee4f | https://github.com/Digipomps/HavenAgentD/pull/28 |
| CellScaffold | 78969ca8db1f96d1ffb0d2359daa05242228b976 | https://github.com/Digipomps/CellScaffold/pull/278 |

- 15 Python-tester for innsamling og 12 eksisterende bounded-runner-fixtures bestått.
- 28 kompilerte Swift-tester i Scaffold bestått: artefakter, GraphStore og Workbench-konfigurasjon.
- 32 kompilerte Swift-tester i AgentD bestått: metadatahjelper, Workbench-klient, jobbavslutning og konfigurasjon.
- 29 deploy-miljø-/kapasitetstester: 28 bestått, én root-avhengig utelatt.
- 14 GUI-kontroller bestått med produksjonsskeleton og svar fra faktisk GraphStore-test: lys/mørk, 1440/390 px, tre faner, valg/filter, tom/feil. Ingen sidefeil eller dokument-overflyt. Dette er innspilte cellesvar i lokal browser, ikke en autentisert staging-test.
- Grafgeometri: 10 målinger med maksimalt avvik under 0,02 px etter resize/zoom/pan/valg.
- ValueType-vakt, shell-syntaks og diffkontroll bestått. Ingen endring i Package.resolved.

Eksakte logger, bilder, kommandoer og SHA-256-manifest finnes i øktens eksterne artefaktområde; plasseringen er registrert i HAVEN-Deploy/_handoff/HD-0154/EVIDENCE-20261003.json. GitHub-CI startet én ordinær kjøring per Swift-PR. Status må leses fra de konkrete run-ID-ene 37113316662 (AgentD) og 37113317631 (Scaffold), ikke fra dette notatet. CellProtocol-scriptstiene utløste ingen workflow.

## Gjenværende

Automatisk leveranse/reconnect, konkret graf-target/grant, vert/laptop-enrollment, daemonens rapportmapper, prosjektkobling, Linux-lineage og ferske bevaringskontroller er ikke fullført. Ingen artefakt får ryddekandidatstatus på ufullstendig grunnlag. Linux-kjøring lokalt er ikke utført fordi Docker-daemonen ikke er tilgjengelig. Ekte staging-Porthole, restart og autorisasjon må verifiseres før G3.

Automatisk godkjenningskontroll avviste bakgrunnssending av filstier/metadata til et uverifisert mål. Ingen slik kode ble brukt. Konkret overføringsgjennomgang ligger i CellScaffold/Documentation/Operations/Artifact_Provenance_Transfer_Review.md (PR278). Seneste MCP-probe svarte Transport closed; lokal AgentD-konfigurasjon har bare to lesemål for WorkItem/Project.

T0/T1-preflight er ikke grønn: eksisterende treff i uendrede filer/pinner og gammel ENV-001 på 10 prosent gjenstår. Ingen blokkerende kildefunn peker på endrede filer. Byggene passerte den uttrykkelig godkjente 5-prosentvakten med reserve. Ingen terskel ble senket, ingen cache slettet.

Et tidligere forslag om å skrive om alle graf-rader ble avvist. Løsningen som er testet gjør bare eksakte upserts i proveniensområdet og bevarer øvrige rader. Replay, konflikt og rollback er testet i SQLite.


## Videreføring 2026-10-03, kandidat 5dc229f

- CellScaffold 78969ca8: run 37113317631 success, alle focused control-plane gates inklusive gjentatt broregresjon. Ingen imagepublisering fra draft-PR.
- AgentD b5adebd: run 37113316662 kompilerte på 392 sekunder, men teststeget nådde ytre tidsgrense. Rått testutdata stopper på nøyaktig 32768 bytes fra suitestart, midt i en bestått testlinje. Dette er et spor for utdataflyt, ikke bevist rotårsak eller bevis mot siste testnavn.
- AgentD 5dc229f: bare Python/shell/docs er endret siden b5adebd. Swift-kilder, testkilder og begge Package-filer er identiske. Korrigert testløper kjørte alle sju forhåndsbygde testpakker én gang: 332 bestått på 12,2 sekunder med lokal Xcode 27. CI bruker Xcode 26.3; run 37120365881 pågår.
- Åtte scriptprøver bestått: tidsgrenser, barn/barnebarn, exitstatus, stor stdout/stderr, komplett testpakkevalg og fail-closed ved XCTest. Første sandkasseforsøk ble avvist ved ps; eksplisitt tillatt prøve uten den begrensningen bestod. Pakkingsressursprøver, zsh-syntaks og diff hygiene bestod. Ingen ny kompilering eller cacheopprydding.
- Collector 266078e: 18 Python-prøver bestått; bytegrense, tom stdout ved for stor snapshot, journalbevaring og senere komplett replay er testet. Ingen transport/sendefunksjon eller live grafimport er bevist.

Rålogger og eierskapsmanifest er referert fra HAVEN-Deploy/_handoff/HD-0154/EVIDENCE-20261003.json. Passkey-innlogging, faktisk grafmottaker og grant mangler. Metadataomfanget er godkjent; G3/runtimeakseptanse er fortsatt åpen.


### Sluttresultat for CI-kandidaten 2026-10-03

AgentD CI 37120365881 er SUCCESS på 5dc229f: 332 tester i 57 suiter bestod på 22,45 sekunder med Xcode 26.3; kompilering, røykprøve og lagring av testet runtime bestod. Hele jobben tok 6m44s. Dette erstatter «pågår» over; opprinnelig rotårsak er fortsatt ikke endelig bevist.

Scaffold PR278 er oppdatert til 31d234cc med bare godkjenningsdokumentasjon og læring i to skills. Swift-kilder, tester og Package-filer er identiske med CI-grønne 78969ca8. Den rene dokumentasjonscommiten bruker skip-ci for å unngå et nytt fullt bygg; det finnes ikke et nytt CI-resultat på 31d234cc. Kodekandidaten er fortsatt utkast og ikke merge-/deployklar.

Køeier rettet Codex-snarveien med jobb a3-codex-lenke-20261003; versjon 0.160.0 er bekreftet. Ingen eldre hold-jobber ble sluppet. Git- og samarbeidsskillen er distribuert og seks lokale kopier av hver har samme hash; ingen skyopplasting eller reload av eksisterende samtaler er påstått.

EVIDENCE-20261003-followup.json i HD-0154-overleveringen er gjeldende revisjonsoversikt. Tre arbeidstrær er rene og pushet. Mac-en er låst; passkey/grafverifisering venter. Vertsrot har 36739660 KiB ledig, under 40 GiB. Ingen sletting, ny lokal kompilering, grafimport, installasjon, merge eller deploy i denne videreføringen. Automatisk sender og de øvrige akseptansepunktene gjenstår; G3 er åpen.


### Innlogget GUI og fersk MCP-diagnose 2026-10-03

Dette erstatter tidligere opplysninger om låst Mac og ventende passkey. Chrome er verifisert innlogget som kjetil2; Safari er meldt innlogget av Kjetil, men ikke separat testet. Staging /health/build bekrefter fortsatt app 415ea3d278dc85be5547c137d917aa343dadb38a fra 30. september. Workbench Access Grant viser konkret grafcelle og requesteridentitet. Den deployede kildens eierbindingskontroll og graph.state-probe er kontrollert; toolbarens Porthole-UUID er ikke requesterbevis. Konkrete identiteter er kun i den private enrollment-kvitteringen.

Ny instans av installert MCP-adapter svarte på initialize, tools/list, config.validate, targets og state.refresh; agenten hadde ferskt livstegn. Chatens beholdte MCP-forbindelse svarer Transport closed. Begge eksisterende staging-mål svarte unavailable på state. Agentens offentlige identitetsbeskrivelse er identifisert, men signert fjernaksess, transport og grant er ikke verifisert. Grafoperasjonene er ikke installert. Ingen omstart, konfigurasjonsendring, grantutstedelse eller grafimport.

Live GUI: én prosjektportefølje og ett prosjekt synlig. Biblioteket lister konfigurasjoner som ikke kan åpnes; Tilbake feiler også for Workbench Access Grant. En normal navn/endepunkt-rute virker. Fabrikk-UUID-er på tvers av forespørsler er en kildebasert hypotese, ikke testet rotårsak. Ett konkret bug-work-item er registrert via Intake, og full tittel/beskrivelse er lest tilbake etter ny sideinnlasting; antall oppgaver gikk 4 → 5. Dette er vanlig oppgavefangst, ikke grafmetadataimport.

Scaffold PR278 har head 08f237a8813b624e25d0a304773136a75b29cd5e, kun dokumentasjon/skill siden forrige hode. Sources, Tests og Package-filer er fortsatt identiske med CI-grønne 78969ca8. Ingen ny CI startet; øvrige PR-heads og CI-resultater er uendret. GUI-læringen er anvendt og synkronisert; fem eksisterende lokale skillfiler har samme hash, mens én konto-styrt Desktop-bøtte ikke beholdt kopien. Skyopplasting og reload av aktive samtaler er ikke verifisert.

EVIDENCE-20261003-enrollment.json og enrollment-kjetil2-staging-20261003.json i HAVEN-Deploy/_handoff/HD-0154 er gjeldende. Metadataomfanget er fortsatt godkjent; ingen gjentatt samtykkeforespørsel trengs. Automatisk sender, aktiv agenttilgang, øvrig registrert jobbdekning, bevaring og stagingakseptanse gjenstår. Lokal kompilering er fortsatt stoppet av 5-prosentvakten med reserve. HD-0154 er PREPARING og G3 åpen; ingen merge/install/deploy.
