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


### Automatisk sender og vertsrydding 2026-10-04

Erstatter tidligere bygg- og senderblokkering: Mac hadde 85.8 GiB ledig ved ny kontroll; lokal 5-prosentvakt med 10 GiB reserve bestod. Den utløpte Mac-ryddeplanen ble ikke utført av denne tråden og trengtes ikke for bygget. Automatisk godkjenningskontroll avviste tidligere apply fordi eksakt token ikke kom fra brukeren. Ingen annen slettemetode ble brukt mot disse kandidatene.

AgentD PR28: 5cf353118b1004320ca90d9ec4ffce8db250e4c6, pushet. Opt-in automatisk sender er implementert med én varig ventende payload, smal owner/host/writer/requester/target-binding, gjentatt policykontroll, filgrenser, enkeltsenderlås, omstartsreplay og varig kvittering. Nanosekunder og store heltall bevares gjennom JSON og ValueType. Status skrives i eksisterende cell-runtime-snapshot. Senderen er deaktivert; ingen aktiv konfigurasjon er endret. Alle 344 Swift-tester i 58 suiter består lokalt (15.6 sek); siste kompilering 30.56 sek. Åtte Python CI-fixturer består. CI 37160743097 er foreløpig under kjøring. Den separate ugyldige private-release-artifact-workflowen feiler fortsatt uten jobber (HD-0160); den er ikke kjørt om igjen.

CellProtocol PR57: 6452fa4a7320d31b57bbdda02c3fe212b2cba322, pushet. Privat, atomisk eksport etter journalcommit er implementert. Både macOS og Linux består 24 collectortester og 12 SwiftPM-runnerfixturer. Første Linux-overføring manglet fake-lsof; komplett testpakke bestod uten endring av runneren. Sju kopierte testfiler på verten ble hash-verifisert og fjernet etter testen; privat testrot ble fjernet. Begge vertsclaims er frigitt.

Vertsrydding: bare arkiverte systemjournaler eldre enn sju døgn fjernet via journalctl. Rot gikk fra 36,703,104 til 40,360,920 KiB ledig (35.00 -> 38.49 GiB). Ingen container eller tjeneste ble startet om. Verten mangler fortsatt ca. 1.51 GiB til 40 GiB. Reparasjonskopi, kilder, identitet og deployevidens ble bevart.

Faktisk agenttilgang blokkeres fortsatt: /bridgehead er fjernet fra staging-koden; HTTP-sonde gir 404. Native Sprout krever publisher-bundet signert kontrakt og er ikke en generell graf-rute. Køtråden bekrefter at autentisert felles CellScaffold-rute ennå ikke finnes. Den eier utrullingen; brokjeden følger PDD_bro-paa-i-prod_2026-09-26 etter PR53, sikkerhetsgjennomgang og egen server-PR. Ingen person-HTTP-omvei er introdusert. Remote grant og full eier/requester-enrollment gjenstår.

Scaffold PR278: 7e1d71ed16e3f1688bc03651a46e1a8db139e237, bare kontraktlæring siden 08f237a8. Swift-kode, tester og package-pins uendret. Læringen L-2026-10-04-artifact-delivery-integers-and-receipt-digests er applied/synced; fem eksisterende lokale skillkopier har lik hash. Global learning-check har fortsatt fire andre åpne/usynkroniserte oppføringer; de er ikke lukket av denne tråden.

Evidens: HAVEN-Deploy/_handoff/HD-0154/EVIDENCE-20261004-delivery.json og SERVER-CLEANUP-20261003.md. G3 står åpen. Ingen merge, agentinstallasjon, grafimport eller deploy. Prosjektmapping, øvrig registrert jobbdekning, bevaringskontroller og liveakseptanse gjenstår.


### CI fullført 2026-10-04

AgentD CI 37160743097 er SUCCESS på eksakt head 5cf353118b1004320ca90d9ec4ffce8db250e4c6. Alle 344 tester i 58 suiter bestod på Xcode 26.3 (21.955 sekunder); bygg og smoke-check bestod. Dette erstatter «under kjøring» over. Full rålogg og SHA-256 er registrert i EVIDENCE-20261004-delivery.json. Ingen ny kjøring startet. Den separate private-release-artifact-workflow-feilen er bekreftet i GitHubs GUI: linje 28 bruker runner.temp i job-level env, hvor runner ikke er tillatt. Den håndteres separat under HD-0160. Ingen endring i live-aktivering, G3 eller broavhengigheten.


### Avsluttende kilde- og arbeidsstatus 2026-10-04

Scaffold PR278 head er nå 1cf6042db50c8c9dcf8786c7996fa3220895dc6e etter 21 linjer Git-workflow-læring (skip-ci); Sources/Tests/Package er uendret. AgentD PR28 head er fortsatt CI-grønne 5cf3531; collector PR57 fortsatt 6452fa4. Den separate HD-0160-feilen er rettet i PR29/3111ab4: én variabel flyttet til step-level env, actionlint bekrefter før-feil og etter-pass for begge workflow-filer. Ingen ny Swift CI eller gammel release-dispatch. Seks lokale Git-skillkopier er hash-like etter synk; skyopplasting/reload er ikke verifisert.

Fersk vertsrot: 40,435,308 KiB tilgjengelig (ca. 38.56 GiB), fortsatt under 40 GiB. Den lesende ops-du av eldre evidens undertrykte permission errors og er derfor ufullstendig; den lavere synlige mappestørrelsen er ikke bevis på sletting. Ingen ekstra sletting utført. Køfila har en ny referert brukeravgrensning «Rydd alle fire», men native Claude kunne ikke åpnes fordi Mac-en var låst; denne tråden har ikke verifisert den direkte brukerbeskjeden og slettet ikke reparasjons-/gjenopprettingsdata på grunnlag av den.

PR53 er fortsatt OPEN på 55c81a2 med fem grønne sjekker; ingen påstand om sikkerhetsaksept eller merge. Authenticated shared CellScaffold-rute, remote grant, enrollment og end-to-end staging er fortsatt åpne for HD-0154. Tidligere køsvar er lest; ny HD-0160-overlevering er lagret i køoppgaven, ikke sendt i den låste Claude-samtalen. G3 åpen, ingen aktivering, installasjon, merge eller deploy.
