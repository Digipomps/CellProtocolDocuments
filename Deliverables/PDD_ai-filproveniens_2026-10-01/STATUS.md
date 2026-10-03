# STATUS — ai filproveniens

- surfaces: cell, codex, gui, scaffold, terminal
- tags: cleanup, filesystem, graph, provenance

## Porter
- G1: godkjent 2026-10-02 (Kjetils uttrykkelige godkjenning i Workbench-oppgaven)
- G1-GUI: godkjent 2026-10-02 (Kjetil: «Jeg godkjenner G1-GUI/G2»)
- G2: godkjent 2026-10-02 (Kjetil: «Jeg godkjenner G1-GUI/G2»)
- G3: venter        (akseptanse: forventning mot faktisk, alle avledede tester grønne)

Sett en port til `godkjent <dato>` kun når Kjetil har sagt det. `purpose_dev.py validate <mappe>` nekter porter uten artefakter.

## Planbytter (dato — hvorfor)
- 2026-10-01: Fra manuell filoversikt til avgrenset automatisk proveniens gjennom eksisterende graf, etter brukerens presisering. Ingen implementering er startet.

## Logg
- 2026-10-01: opprettet

- 2026-10-01: Kildekartlegging og G1-utkast ferdig. Importskisse er offline; MCP targets svarte Transport closed. Diskmargin er fortsatt utilstrekkelig. Ingen kode, CI, deploy eller sletting utført.

- 2026-10-02: Kjetil: «Jeg Godkjenner dette omfanget for registrerte agent-, bygg- og deployjobber på begge maskiner». Godkjenningen gjelder §1–§3 i FORMAALSSPEC. G1-GUI og G2 er fortsatt til gjennomgang.

- 2026-10-02: PLAN.md, metadatautkast, dataflyt og ti GUI-bilder er klare. Fixturekontroller bestått i lokal Chrome; ingen live funksjonstest. AgentD svarer igjen, men ingen graf-target er annonsert. G1-GUI/G2 avventer konkret bilde-/plangjennomgang.

- 2026-10-02: Kjetil godkjente G1-GUI/G2 uttrykkelig. Implementering startet; G3 krever faktisk akseptanse og er fortsatt åpen.

- 2026-10-03: Tre draft-PR-er opprettet (#57 CellProtocol, #28 AgentD, #278 CellScaffold). 60 lokale Swift-tester og 14 produksjonsskeleton-GUI-kontroller bestått; se TESTRESULT.md. Automatisk sender ble avvist av godkjenningskontroll, graf-target/grant er uverifisert, bevaringskontroller gjenstår. G3, merge og deploy er ikke gjennomført.


## Videreføring 2026-10-03, kandidat 5dc229f

Kjetil har godkjent automatisk metadataoverføring til sin egen kjetil2-graf på staging. Samtykkeblokkeringen over er dermed erstattet. Konkret graf/owner/requester/grant er fortsatt uverifisert; Chrome venter på passkey. MCP annonserer to lesemål, men prosjekt-state er utilgjengelig. Ingen metadata er sendt.

CellScaffold CI 37113317631 bestod på 78969ca8, inkludert ferske broregresjoner. AgentD CI 37113316662 kompilerte, men teststeget hang. Ny testløper er verifisert mot 332 eksisterende Swift-tester (12,2 sekunder), åtte Python-prøver og pakkingskontroller. AgentD PR28 er pushet til 5dc229f; én ny CI 37120365881 går. Swift-kilder og pins er uendret siden det lokale bygget. Ingen ny lokal kompilering, installasjon, merge eller deploy.

CellProtocol PR57 er pushet til 266078e: komplett bytegrense for snapshot, uten journaltap; 18 tester består. Automatisk sender, enrollment, prosjektmapping, daemon-rapportfangst, Linux-linjeidentitet og fersk bevaringskontroll gjenstår. HD-0154 beholder PREPARING; G3 er åpen.


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
