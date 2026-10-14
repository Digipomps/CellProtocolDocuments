# STATUS — workbench perspective chat

- surfaces: binding, cell, scaffold, skeleton, web
- tags: agent, chat, event, history, privacy, purpose, workbench

## Porter
- G1: godkjent 2026-10-10 (Kjetil: «Jeg godkjenner», svar på G1-spørsmålet)
- G1-GUI: godkjent 2026-10-11 (Kjetil: «Jeg godkjenner G1-GUI»; 54 bilder låst i evidence/g1-gui-approval.json)
- G2: godkjent 2026-10-12 (Kjetil: «Jeg godkjenner G2»; godkjent plan låst i evidence/g2-approval.json)
- G3: venter        (akseptanse: forventning mot faktisk, alle avledede tester grønne)

Sett en port til `godkjent <dato>` kun når Kjetil har sagt det. `purpose_dev.py validate <mappe>` nekter porter uten artefakter.

## Planbytter (dato — hvorfor)
- Ingen implementeringsplan før G1. Dette er nytt samlet omfang; eldre Workbench-porter kopieres ikke inn.

## Logg
- 2026-10-10: opprettet

- 2026-10-10: kildeaudit, handlingsmatrise, eventkrav og testbare forventninger skrevet. Ingen produktkode, nye kjøringer, GitHub Actions, merge eller deploy startet.
- Oppgavemappen ligger lokalt og er ikke pushet. Formålstrær-synk mangler ArtifactData-verktøy.
- Runtime-avhengigheter er ikke godkjent: Safari krevde innlogging, og AgentD Workbench state feilet.
- Historisk før godkjenning: G1 ventet; GUI-bilder og G2-plan gjenstod.

- Dokumentkontroll: åtte distinkte oppgaveformål med verifikator; global PDD-validator exit 1 på fem eksisterende lesson-referanser. Ikke grønn produkt- eller PDD-status.

- Uavhengig dokumentkontroll og etterkontroll: PASS innenfor avgrenset kilde-/dokumentkontroll, se REVIEW.md. Ingen produktakseptanse.
- Læring L-2026-10-10-kjetil-presiserte-at-workbench-hovedsakelig-er er applied/synced til haven-work-intake. Lokale Codex-/Claude-kopier og ZIP er oppdatert; allerede opplastede Cowork-plugin-kopier krever egen opplasting.

- 2026-10-10: G1 registrert etter Kjetils uttrykkelige godkjenning. P1-GUI startet; G1-GUI/G2/G3 er fortsatt venter.

- 2026-10-10 P1-GUI: 54 referansekandidater rendret med uendret web-renderer og eksplisitt kandidat-CSS. Ingen JS-/komponentfeil eller horisontal overflyt i de prøvde bredder; minst 4,99:1 målt tekstkontrast. 926 lokale kontrollhandlinger på 43 keypaths registrert. Dette er ikke produktakseptanse.
- GUI integrasjonsgap: skriv→Send og skriv→Lagre sender ikke automatisk siste TextArea-utkast i renderer-only-prøven. Backend/host, Explore, Flow/persistens, native og faktisk utføring gjenstår.
- GUI-galleri og avgrensning: GUI_GALLERY.html, GUI_REVIEW.md, images/README.md. G1-GUI/G2/G3 er fortsatt venter.
- Læring L-2026-10-10-component-draft-send-gui applied/synced i cellconfiguration-skeleton-authoring; kanon, Codex, Claude, Desktop-store og ZIP er oppdatert. Cowork-upload er ikke utført.

- Uavhengig GUI-/dokumentkontroll og etterkontroll: fire P2-presiseringer og ett P3-statuspunkt rettet, ingen resterende funn innenfor avgrensningen i GUI_INDEPENDENT_REVIEW.md. Ingen G3-akseptanse.

- 2026-10-11: G1-GUI godkjent uttrykkelig av Kjetil. Alle 54 PNG-hasher er verifisert mot godkjent manifest. P2-planlegging startet; G2/G3 venter. Tidligere ventestatus i loggen er historisk.

- 2026-10-11 P2: G2-plan med sju bladpakker, dataflyt, foreslåtte kontrakter, retentiongrenser og køhandoff skrevet. Dokumentkontroll: 22 testrefs og 43 kandidat-actions koblet; 54 godkjente PNG-er uendret; 8 syntetiske kontrakteksempler kontrollert. Ingen produkttester eller køjobber kjørt. Uavhengig G2-kontroll pågår; G2/G3 venter.

- 2026-10-11 P2 etterkontroll: to P2-funn rettet (milepæl-avhengighet og GUI-domeneeierskap). Uavhengig etterkontroll PASS innenfor G2-dokumentomfanget; se G2_INDEPENDENT_REVIEW.md. Plan og separate lanediagram klare for G2. Produktimplementering, runtime-tester, køsubmit og deploy er ikke startet. G2/G3 venter.
- 2026-10-11 læring: L-2026-10-11-porthole-main-9ff06f8-flushes-top-level-fields applied/synced i cellconfiguration-skeleton-authoring. Kanon, Codex og Claude har identiske hasher for SKILL.md og referansen; Desktop-store/ZIP oppdatert av synkverktøyet. Opplastet Cowork-plugin er ikke oppdatert. Global lærings-/PDD-backlog er ikke erklært grønn.

- 2026-10-12: G2 godkjent uttrykkelig. P3 startet med kilde-/køavstemming og W1. PLAN.md/plan.json beholdes som godkjent designsnapshot fra 2026-10-11; faktisk gate/progress føres her. G3 venter.

- 2026-10-12 W1: internt journal-/commitgrunnlag og 13 nye ukjørte tester skrevet på codex/workbench-perspective-chat-20261012. Uavhengig kildekontroll av første adapter fant feed- og autosave-gap; adapteren tatt ut. Eksisterende Helper er uendret. W1_FOUNDATION.md og evidence/w1-preflight-20261012.json beskriver status. Literalguard grønn; ingen Swift, CI, push eller deploy. Kø/capacity sperrer bygg. W1/G3 ikke ferdig.

- 2026-10-12 læring: L-2026-10-12-cell-journal-autosave-admission applied/synced i cellprotocol-scaffold-integration; kanon/Codex/Claude har samme filhash. Desktop-store og ZIP oppdatert; opplastet Cowork-plugin ikke oppdatert. Global lærings-/PDD-backlog er ikke erklært grønn.

- 2026-10-12 W1 etterkontroll: PASS innenfor intern kilde-/dokumentavgrensning. Command B kan ikke lenger avstemme pending A med Bs admission-callback; 13. test skrevet, ikke kjørt. Se W1_INDEPENDENT_REVIEW.md. Ingen endring i runtime-/deploystatus.

- 2026-10-12 rydderunde/W1: Claude-køen fjernet 7,32 GiB release-byggprodukter; bevart kilde/checkouts kontrollert. Mac 105,67 GiB ledig ved etterkontroll (104,14 GiB ved 07:57Z). Verten inspisert, ingen sletting der. Fire nye Entity-prober gir 17 ukjørte consumer-tester; én manifestlåst testjobb er forberedt utenfor kø. d237/w23 holder fortsatt vinduet. Separat CellProtocol-kandidat fra 2026.9.7 legger journal-konfliktvern i begge legacy batch-stier med åtte nye ukjørte tester. Se W1_ENTITY_BOUNDARY.md. Ingen Swift/CI/PR/deploy; W1/G3 uferdig. Ny chat-retention er spurt, ikke besvart.

- 2026-10-12 08:04Z+: Claude-køkontakt tilgjengelig igjen og serverkandidatene mottatt til avstemming. Chrome viste eldre Workbench-data, men navigasjon ga innloggingsside; før-inventar fortsatt ikke utført. Retention-/innloggingsbehov registrert som pekere i GODKJENNINGER, uten Workbench-synkpåstand. Ny Entity-journal-læring applied/synced, kanon/Codex/Claude hash-identiske; global læringskontroll fortsatt rød på eksisterende backlog.

- 2026-10-12 08:10Z: x41 fjernet fem avstemte gamle serverbilder; Codex etterkontrollerte alle fem borte, 32 containere/22 kjørende og uendrede prod/staging/rollback-ID-er. Docker-volum 40,62 → 59,75 GiB ledig (ca. 19,12 GiB netto). Rydding på begge maskiner fullført i denne runden. Køeier er bedt om engangsaktivering av den forberedte 17-testjobben først etter ÅPENT og ferske guards; ennå ingen bekreftet aktivering/kjøring. Uavhengig CP-kildekontroll avsluttet uten gjenværende P1/P2; åtte tester fortsatt ukjørte.

- 2026-10-12 08:11Z: deploytråden i Claude har uttrykkelig overtatt betinget engangsaktivering av den forberedte G2-testjobben. Første planlagte sjekk 09:30Z; jobb fortsatt ikke lagt i kø. Neste Codex-turn må lese kvittering/attempt-marker og aldri sende duplikat. Ny chat-retention og staging-innlogging venter fortsatt på Kjetil.

- 2026-10-12 ny brukeropplysning: Safari/Chrome innlogget; Chrome bekreftet Live med 14 prosjekter. Egen login-forespørsel fjernet fra GODKJENNINGER med backup. Eksakt requester-ID og W2 før-inventar/eksport/migrering er fortsatt umålt. Retention-spørsmålet er fortsatt ubesvart. Nytt prosjekt-dashboard/graf ligger separat i `Deliverables/PDD_project-workspace_2026-10-12`; det låste G2-testarbeidstreet er uendret. Byggvindu ÅPENT-kvittering 09:55:07Z formidlet til køeier; ingen duplikatjobb sendt av denne tråden.

- 2026-10-12 første køkjørte test ferdig: 15/17 testmetoder bestod; 2 legacy-journal-conflict-prober feilet (4 assertions), exit 1. Alle 13 interne journaltester grønne. Se W1_TEST_RESULT_20261012.md. Rettelseskandidat finnes men er ukjørt; rød stoppregel gjelder, ingen ny kjøring/CI/deploy startet.
