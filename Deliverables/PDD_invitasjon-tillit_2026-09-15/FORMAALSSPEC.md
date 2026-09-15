# Formålsspesifikasjon — invitasjon og tillit

Oppgavemappe: `PDD_invitasjon-tillit_2026-09-15` · Opprettet 2026-09-15 · Iterasjon 1 (ikke godkjent)

> Regel: ingen plan før G1 er godkjent av Kjetil. For GUI: ingen implementering før G1-GUI (rendret bilde) er godkjent.
> Et dokument om leveransen teller aldri som leveransen.

## 0. Intensjon (ordrett) og brief-audit

> Vi må også ta opp igjen selve brukeropplevelsen av invite — finn gjerne ut om det finnes forskning på dette. Vi må lage - helst generelle konsepter - som for brukeren er tilitsvekkende, enkelt å bruke, forståelig, med en god hjelpechat, og skal kunne invitere både personer vi vet har en representasjon i HAVEN og dem som ikke har det.

### 0.1 Den ene setningen som styrer resten

«Personer **vi vet** har en representasjon i HAVEN» er den dyre delen av briefen, og den er dyr på en
måte som ikke er åpenbar. For å vite det, må noen spørre — og et system som svarer på «finnes denne
personen hos dere?» er en katalog. Forskningen under sier at en slik katalog ikke lar seg beskytte
med hashing, og at den i praksis blir tømt. For en plattform hvis hele poeng er datasuverenitet er
det en selvmotsigelse å drive den.

Forslaget i dette dokumentet er derfor å snu spørsmålet: **medlemskap opplyses av mottakeren, ikke av
plattformen.** Det gir samme resultat for brukeren i de tilfellene som betyr noe, og fjerner
angrepet. Prisen er en vekstfunksjon vi da gir fra oss, og den prisen er §6.1 — et spørsmål til deg,
ikke et valg jeg har tatt.

### 0.2 Brief-audit

| Påstand i intensjonen / antatt kapabilitet | Audit | Kilde |
|---|---|---|
| «Det finnes forskning på dette» | **retrieved** — fire relevante arbeider, se §0.3 | Hagen m.fl. TOPS 2022; Biczók & Chia FC'13; Wijesekera m.fl. USENIX Sec '15; Perkins v. LinkedIn |
| «Vi vet at noen har en representasjon i HAVEN» | **contradicted** — kan ikke gjøres trygt som oppslag; se §0.1 og formål A | Hagen m.fl. 2022 |
| HAVEN har allerede en invitasjonsflyt mellom to parter som begge er inne | **retrieved** — Kapittel 18 fase 2–4 modellerer nøyaktig dette for konferanse | `Book/18_Conference_ConnectionHubCell_...md:174-264` |
| Aksept blir en tosidig signert avtale i begge entiteter | **retrieved** — `entity.batchPersist`, ett konvolutt per entitet | Kap. 18 fase 4 |
| Identiteter er domenebundne pseudonymer | **retrieved** | `Book/33_Correspondence_First_Class.md:150` |
| En som sier ja uten å ha HAVEN må lande et sted | **retrieved, uavklart** — hjemme-scaffold-valg finnes som modell, ikke som flyt for nykommere | `Book/32_Cross_Scaffold_Entity_Enrollment.md:54` |
| Import av adressebok skaper entitydata og dermed genesis | **retrieved** — avklart av Kjetil 2026-09-15 | `PDD_entitetsdata-egen-kontroll_2026-09-08/STATUS.md` |
| Nearby-scanner kan gi en verifiserbar peker uten katalog | **recalled** — finnes i Binding, ikke revidert for dette formålet | må verifiseres i P2 |
| Det finnes en hjelpechat som kan nås av noen uten HAVEN-konto | **unavailable** — ingen slik flate i dag | — |

### 0.3 Hva forskningen faktisk sier

**Kontaktoppdagelse basert på hashede telefonnumre er ikke beskyttelse.** Hagen m.fl. (ACM TOPS,
2022) viser at hele verdens mobilnummerrom kan itereres på under 150 sekunder på ett forbruker-GPU,
og at en 30,4 GB regnbuetabell gir 99,99 % treff. De spurte seg gjennom 10 % av amerikanske numre hos
WhatsApp og 100 % hos Signal med én laptop, et VPN-abonnement og en app for engangsnumre. De fant
også at 5 av 12 undersøkte meldingstjenester rett og slett laster opp hele adresseboken og lagrer
den — som lar tilbyderen bygge hele den sosiale grafen til hver bruker.
→ *Konsekvens for oss: ikke bygg katalogen. Formål A.*

**Å invitere noen er en avgjørelse om deres data, ikke dine.** Biczók & Chia (Financial Crypto 2013)
kalte dette *interdependent privacy*: «personvernet til den enkelte avgjøres av andres valg».
Adressebok-opplasting er skoleeksempelet — B sine opplysninger havner hos en tredjepart uten at B har
sagt noe som helst. Forfatterne anbefaler blant annet vernende standardvalg og at bruker gjøres
oppmerksom på eksternaliteten.
→ *Konsekvens for oss: det jeg holder om Vegar er min uverifiserte påstand om Vegar, og han skal kunne
kreve, rette og slette den. Formål C.*

**Folk godtar det de mener oppgaven trenger, og blokkerer resten.** Wijesekera m.fl. (USENIX Security
2015) fant at 35 % av forespørslene ville blitt blokkert om brukeren fikk velge, at 80 % ville stanset
minst én i løpet av en uke, og at den sterkeste enkeltfaktoren (53 % av blokkeringene) var at brukeren
ikke mente appen trengte dataene til det den gjorde. Anbefalingen er å spørre ved første faktiske
bruk, og å begrunne.
→ *Konsekvens for oss: importer det invitasjonen faktisk sender til, ikke hele boka «for å være klar».
Formål D.*

**Purringer er det som ender i retten.** Perkins v. LinkedIn (N.D. Cal., forlik 2015: 13 mill. USD
til krav pluss 3,25 mill. i salærer) handlet ikke om selve importen, men om at LinkedIn sendte **to
påminnelser** til importerte kontakter som brukeren aldri hadde sagt ja til å sende. Dommer Koh la til
grunn at brukerne ikke hadde samtykket til påminnelsene ved registrering.
→ *Konsekvens for oss: én melding. Purring er en ny, bevisst handling fra avsenderen. Formål E.*

### 0.4 De generelle konseptene som følger

Fire setninger. Resten av dokumentet er dem, gjort testbare.

1. **Ingen katalog å slå opp i.** Du får vite at noen er i HAVEN på tre måter: de har gitt deg en
   peker, de svarer deg, eller noen dere begge kjenner introduserer dere. Ingen av dem er et spørsmål
   til en server om et menneske.
2. **Én invitasjon, to leveranser.** Det samme signerte objektet uansett hvem som mottar det.
   Mottakerens medlemskap endrer *leveransen*, ikke *modellen*.
3. **En invitasjon er en påstand om en annen.** Den bærer med seg hva jeg holder om dem, hvor det kom
   fra, og en forpliktelse jeg ikke kan skru av.
4. **Å si nei skal være like lett som å si ja.** Uten å registrere seg, og med virkning hos
   avsenderen.

## 1. Formålstre

| purposeRef | Tittel | Forelder | Goal (outcome) | Verifier | Status |
|---|---|---|---|---|---|
| `purpose://contact.communication` | Contact and communication | — | Eksisterende rot: «kan kommunisere eller bli introdusert uten å eksponere private kontaktdata utenfor samtykke» | — | active (gjenbruk) |
| `purpose://contact.introduction` | Contact introduction | `contact.communication` | Eksisterende: introduksjon forberedes/leveres uten å lekke privat kontaktinfo | — | active (gjenbruk) |
| **A** `purpose://candidate.invite.no-directory-lookup` | Oppdagelse uten katalog | `contact.communication` | Ingen kan få vite om et menneske finnes i HAVEN ved å spørre systemet. Medlemskap opplyses av mottakeren selv, ved å svare. | Det finnes ingen kall som svarer på medlemskap for et endepunkt; oppramsingsforsøk avvises og logges. | candidate |
| **B** `purpose://candidate.invite.one-object-two-deliveries` | Én invitasjon, to leveranser | `contact.introduction` | Samme signerte invitasjon, enten mottakeren har entitet eller ikke. Bare transport og landingsflate skiller. | Samme invitasjons-id ender i samme aksept-/avslagstilstand gjennom begge veier. | candidate |
| **C** `purpose://candidate.invite.claim-about-another` | Invitasjonen er en påstand om en annen | `self-determination.data` | Kontaktdata jeg holder om en ikke-medlem er merket som min uverifiserte påstand, med opphav, og kan kreves, rettes eller slettes av personen når de får egen entitet. | Importert post har `unconfirmed` + opphav; en kravflyt retter eller sletter den og etterlater spor. | candidate |
| **D** `purpose://candidate.invite.minimum-for-the-send` | Minste datamengde invitasjonen trenger | `self-determination.data.scope` | Import for invitasjon persisterer bare det invitasjonen faktisk sendes til. Resten av adresseboken forlater aldri enheten. | Negativ test: fil med mange kolonner gir bare de feltene invitasjonen bruker i entitydata. | candidate |
| **E** `purpose://candidate.invite.no-automatic-reminders` | Én melding, ingen automatiske purringer | `contact.followup` | En invitasjon sendes én gang. Purring krever en ny, bevisst handling fra avsenderen, og mottakeren kan stanse den for alltid. | Negativ test: ingen jobb, timer eller regel kan sende melding nr. 2. «Aldri mer» setter en gravstein som overlever ny import. | candidate |
| **F** `purpose://candidate.invite.decline-without-account` | Nei uten å registrere seg | `human-agency` | Avslag og «aldri mer» er tilgjengelig uten å opprette noe som helst, og virker hos avsenderen. | Avslagsveien fullføres uten entitet; avsenderens neste import kan ikke invitere samme person på nytt. | candidate |
| **G** `purpose://candidate.invite.recipient-sees-what-is-held` | Mottakeren ser hva som holdes om dem | `self-determination.data.verifiability` | Invitasjonen viser de faktiske feltene avsenderen har om mottakeren — ikke en generell formulering — før mottakeren svarer. | Feltene som vises er nøyaktig de som er persistert; testen sammenligner de to listene. | candidate |
| **H** `purpose://candidate.invite.acceptance-is-bilateral` | Aksept blir en tosidig signert avtale | `contact.introduction` | Et ja gir én `entity.batchPersist`-konvolutt per entitet, med signert avtalepost, relasjon og chronicle — som kapittel 18 fase 4. | Aksept produserer to konvolutter; ingen av dem skrives uten eierbevis. | candidate |
| **I** `purpose://candidate.invite.help-chat-cannot-send` | Hjelpechat som forklarer, ikke handler | `human-agency` | Hjelpechat finnes på begge sider, også for mottakere uten HAVEN, og kan forklare og slå opp — men aldri sende, akseptere eller avslå på vegne av noen. | Negativ test: chattens handlingskeypaths inneholder ingen send/aksept/avslag. | candidate |
| **J** `purpose://gui.ways-in-are-reachable` | Flaten skjuler ikke sine egne veier inn | `pkg.std.gui-surface` | Hver invitasjonsflate viser veiene inn i tom tilstand. | `SkeletonReachabilityAudit`. | active (gjenbruk) |

Regler: nye noder er `purpose://candidate.…` og navngis her. A–I er forslag; navnene er mine og kan
endres av deg uten at innholdet endres.

## 2. Avgrensning og avhengigheter

**Hva dette ikke er:**

- Ikke selve filimporten. Den hører til `PDD_entitetsdata-egen-kontroll_2026-09-08` og er en
  forutsetning her, ikke en leveranse.
- Ikke genesis/forsegling av entiteten. Samme sted.
- Ikke konferanseflyten. Kapittel 18 er mønsteret vi generaliserer fra, ikke noe vi bygger om.
- Ikke betaling, verving mot belønning eller noen form for vekstmekanikk. Alt som ligner må gjennom
  `dimy-payment-regulatory-guardrails` først.
- Ikke en global HAVEN-katalog. Se §0.1 — det er tvert imot det formål A finnes for å hindre.

| Kapabilitet | Kilde | Avgrensning | Må virke før test? |
|---|---|---|---|
| Tosidig signert avtale i begge entiteter | Kap. 18 fase 4; `EntityBatchPersistEnvelope` | Modellert for konferanse, med hub som koordinator. En invitasjon utenfor en konferanse har ingen hub. | Ja — formål H |
| Domenebundne identiteter | Kap. 33 §4.1 | Sier hvilke identiteter som finnes, ikke hvilken en invitasjon skal sendes fra. | Ja — §6.2 |
| Hjemme-scaffold ved innrullering | Kap. 32 §3 | Beskriver valg for en entitet som finnes. En nykommer har ingen. | Ja — §6.3 |
| Filimport i egen entitet | PDD entitetsdata, formål A | Gir data inn. Sier ingenting om hva som skjer med *de andres* data. | Ja — formål C, D |
| Nearby-scanner | Binding | Gir en peker uten oppslag — kandidat til vei (a) i formål A. Ikke revidert for dette. | Verifiseres i P2 |
| `SkeletonReachabilityAudit` | CellProtocol | Finner elementer som aldri kan sees. Sier ikke om handlingen gjør riktig ting. | Ja — formål J |
| Signerte avslag / gravsteiner | **finnes ikke** | — | Ja — formål E, F |
| Flate som kan brukes uten HAVEN-konto | **finnes ikke** | Alt i Binding forutsetter en identitet i dag. | Ja — formål F, I |

## 3. Forventningskontrakt — «Det du kommer til å se»

Ingen bilder er laget ennå. Denne tabellen er det jeg vil lage *etter* at du har godkjent G1, og
listen er en del av det du godkjenner.

| Leveranse | Type | Hvor | Referanse | Godkjent |
|---|---|---|---|---|
| Invitasjonen sett fra avsender: velg person, se hva jeg holder om dem, se hva som sendes | bilde | `images/` | `avsender-forhandsvisning-v1.png` | nei |
| Invitasjonen sett fra en mottaker **uten** HAVEN | bilde | `images/` | `mottaker-uten-haven-v1.png` | nei |
| Samme invitasjon sett fra en mottaker **med** HAVEN | bilde | `images/` | `mottaker-med-haven-v1.png` | nei |
| Avslag uten konto, og «aldri mer» | bilde | `images/` | `avslag-uten-konto-v1.png` | nei |
| Hjelpechat på mottakersiden, med det den ikke kan gjøre synlig | bilde | `images/` | `hjelpechat-mottaker-v1.png` | nei |
| Avsenderens oversikt: sendt, besvart, avslått, gravsteiner | bilde | `images/` | `avsender-oversikt-v1.png` | nei |
| Hva dagens skeleton ikke kan rendre av bildene | fil | `images/README.md` | — | nei |
| Negative tester: ingen katalog, ingen automatisk purring, chat kan ikke sende | testutdata | `TESTRESULT.md#negative` | — | nei |
| Kjørende flate: invitere én person fra bokprosjektimporten og få den besvart | kjørende flate | Binding, Relasjoner | — | nei |
| Chronicle-spor per invitasjon, aksept og avslag | testutdata | `TESTRESULT.md#trace` | — | nei |

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
    - artefakt skeleton/ (port G1-GUI): CellConfiguration/skeleton-JSON som bildet er rendret fra (når Porthole-preview er brukt).
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

## Book 23-noder som kan være forelder/gjenbruk (leksikalsk forslag, verifiser)
- purpose://questionnaire.delivery.consent [active] — Questionnaire delivery and consent
- purpose://access.audit.privacy [active] — Access, audit and privacy
- purpose://questionnaire.access.audit [active] — Questionnaire access audit


## 5. Avledede tester

| testRef | Type | Beskrivelse | Hvordan | Formål | Bevis |
|---|---|---|---|---|---|
| `test.invite.no-membership-oracle` | inspection | Ingen kall, keypath eller celleaksjon svarer på om et endepunkt tilhører et medlem. | Kildegjennomgang + kontraktsinspeksjon av alle inviterelaterte aksjoner. | A | `ACCEPT.md#no-directory` |
| `test.invite.enumeration-refused` | command | N forsøk på å sjekke endepunkter på rad avvises, uansett om de finnes. | Negativ XCTest mot invitasjonscellen. | A | `TESTRESULT.md#negative` |
| `test.invite.same-object-both-paths` | command | Én invitasjon, levert begge veier, ender i samme tilstand med samme id. | XCTest med to mottakerprofiler. | B | `TESTRESULT.md#invite` |
| `test.invite.claim-is-marked` | command | Importert post om ikke-medlem har `unconfirmed` og opphav (fil, dato, kolonne). | XCTest gjennom importen. | C | `TESTRESULT.md#claim` |
| `test.invite.subject-can-erase` | command | Personen det gjelder kan slette eller rette det avsenderen holder, og det etterlater spor. | XCTest på kravflyten. | C | `TESTRESULT.md#claim` |
| `test.invite.minimum-persisted` | command | Fil med tolv kolonner gir bare feltene invitasjonen bruker i entitydata. | Negativ XCTest, teller persisterte felter. | D | `TESTRESULT.md#negative` |
| `test.invite.no-second-message` | command | Ingen jobb, timer eller regel kan sende melding nr. 2. | Negativ XCTest + inspeksjon av planlagte jobber. | E | `TESTRESULT.md#negative` |
| `test.invite.tombstone-survives-reimport` | command | Etter «aldri mer» kan samme person ikke inviteres av en ny import av samme fil. | XCTest: importer, avslå, importer igjen. | E, F | `TESTRESULT.md#invite` |
| `test.invite.decline-without-entity` | command | Avslagsveien fullføres uten at det opprettes noen entitet eller identitet. | XCTest + negativ sjekk på at ingenting ble forseglet. | F | `TESTRESULT.md#negative` |
| `test.invite.shown-equals-held` | command | Feltlisten mottakeren ser er nøyaktig den som er persistert. | XCTest sammenligner to lister. | G | `TESTRESULT.md#claim` |
| `test.invite.acceptance-two-envelopes` | command | Aksept gir én `entity.batchPersist` per entitet, ingen skriving uten eierbevis. | XCTest som kap. 18 fase 4. | H | `TESTRESULT.md#trace` |
| `test.invite.chat-cannot-act` | inspection | Hjelpechattens handlingskeypaths inneholder ingen send, aksept eller avslag. | `SkeletonReachabilityAudit.reachableActionKeypaths` + kontraktsinspeksjon. | I | `ACCEPT.md#help-chat` |
| `test.skeleton.no-unreachable-elements` | command | Ingen invitasjonsflate skjuler sine egne veier inn. | `testNoLocalSurfaceHidesItsOwnWaysIn`. | J | `TESTRESULT.md#reachability` |
| `test.build`, `test.regression` | command | `pkg.std.everything-works`. | xcodebuild + swift test. | — | `TESTRESULT.md#build` |

## 6. Åpne spørsmål til Kjetil

Disse endrer treet. Jeg har skrevet hva jeg ville valgt, men ingen av dem er mine å avgjøre.

**6.1 Gir vi fra oss «tolv av kontaktene dine er allerede her»?**
Det er den mest effektive vekstfunksjonen som finnes, og den er uforenlig med formål A. Forskningen
sier at hashing ikke redder den. Et mellomstandpunkt finnes: *gjensidig* oppdagelse — vis bare
treff der begge har hverandre i adresseboken, noe Hagen m.fl. lister som en av mitigasjonene. Den
lekker mindre, men den er fortsatt et oppslag, og den krever at vi holder noe om folk som ikke er
her. **Min anbefaling: gi den fra oss, og si tydelig hvorfor i produktet — det er en av de få
gangene et fravær kan bygge tillit.** Men dette er et produktvalg med en reell pris.

**6.2 Hvilken identitet sender invitasjonen?**
Kapittel 33 sier at domenebundne identiteter er pseudonymene. En invitasjon til en adressebokkontakt
knytter den identiteten til det mennesket permanent. Skal invitasjoner sendes fra en identitet per
identityDomain, fra én stabil «personlig» identitet, eller fra en ny per invitasjon? Dette henger
sammen med ditt eget åpne spørsmål om flere identiteter i samme identityDomain.

**6.3 Hvor lander en som sier ja og ikke har HAVEN fra før?**
Kapittel 32 beskriver hjemme-scaffold-valg for en entitet som allerede finnes. En nykommer har
ingen. Skal avsenderens scaffold være midlertidig vert — slik du åpnet for ved scanner-invitasjon —
eller skal nykommeren velge først og svare etterpå? Det første er enklere og mer innbydende; det
andre unngår at noen sin første entitet blir til på en annens scaffold.

**6.4 Utløper en invitasjon?**
Hvis «det skjer ingenting hvis du lar den ligge» skal være bokstavelig sant, må den ta slutt av seg
selv. Jeg vil foreslå en oppgitt dato i selve invitasjonen. Hvor lenge er ditt valg.

**6.5 Skal et avslag fortelle avsenderen noe som helst?**
Et avslag som er synlig for avsenderen røper at endepunktet er i bruk og at noen leste. Et avslag som
er usynlig gjør at avsenderen purrer. Jeg heller mot at avsenderen ser «besvart — ikke nå», uten
skille mellom «avslått» og «aldri mer», og at gravsteinen virker i det stille.

## 7. Revisjonslogg

- 2026-09-15, iterasjon 0: opprettet av `purpose_dev.py new`.
- 2026-09-15, iterasjon 1: formålstre, forskningsgrunnlag og åpne spørsmål skrevet. Venter på G1.
