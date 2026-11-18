# Formålsspesifikasjon — forskningsdata for studentene

Oppgavemappe: `PDD_forskningsdata-verktoy_2026-11-17` · Opprettet 2026-11-17 · Iterasjon 1 (ikke godkjent)

> Regel: ingen plan før G1 er godkjent av Kjetil. For GUI: ingen implementering før G1-GUI (rendret bilde) er godkjent.
> Et dokument om leveransen teller aldri som leveransen.
>
> Kjetil ba uttrykkelig om en plan. `PLAN.md` ligger derfor ved som utkast, slik `PDD_python-research-scaffold_2026-11-06` gjorde. Utkastet godkjenner ingenting; G2 bes om først etter G1 og G1-GUI.

Vurderingen bak treet, med funn i koden og datatrappen N0–N4, står i `VURDERING.md` i samme mappe.

## 0. Intensjon (ordrett) og brief-audit

Kjetil, 17.11.2026 kl. 09.23 (prosjektet «HAVEN Master oppgaver 2026»):

> Vi kan la det være åpent om det skal presenteres som et nytt forskningstema, men du burde spinne ut en ny tråd som vurderer hva studentene vil trenge av verktøy for å ekstrahere data de kan trenge i forskningen sin uansett hva temaet er. Det bør være både helt anonym data som f.eks scaffold admin har tilgang til og mulighet for å be entiteter om tilgang til spørringer og eller lagring. Gjør en grundig vurdering av hva som kan være nyttig i et forskningperspektiv og lag en plan. Vi må ha komponenter for å vise data også. Og kanskje oppgaven med å sette opp sitt eget student-dashboard kan være en del av onboardingen til HAVEN for studentene.

Stående regler som gjelder: tilgang til en celle avgjøres bare av vilkårene i Agreement, og skal virke likt i Swift, Python og Go (Kjetil 28.10). Swift er referansen og skal virke i hver flyt (Kjetil 28.10).

Lesing av «lagring»: jeg leser det som at en entitet gir studenten et sted i sin egen entitet å skrive og lese forskningsdata (dataene blir hos entiteten). At en organisasjon gir studenten lagringsplass til egne datasett, dekkes av samme mekanisme, fordi en organisasjon også er en entitet.

Revisjoner lest: CellScaffold `main` `57ce8c0`, CellProtocol `main` `14fd9dc`, CellProtocolDocuments `main` `e7808fe`, PyResearchScaffold på Macen (gren `codex/research-scaffold-wp5`, `a7871d8`).

| Påstand / antatt kapabilitet | Audit | Kilde |
|---|---|---|
| Scaffold-admin har data som kan gis videre som «helt anonym» | **contradicted** | `CellScaffold/Sources/ScaffoldKit/AdminMetricsSupport.swift:138–197`: `identityNamedCells` er nøklet på identitets-uuid og viser hvilke celler hver identitet har. Tellinger som `identitiesWithPersonalCells` er anonyme; resten må projiseres |
| Adminflatene er beskyttet med Agreement-vilkår | retrieved | `AdminMetricsSupport.applyRoleCondition` (`:1331`): `ProvedClaimCondition` med `AdminRoleCredential`, claim `granted` |
| Det finnes kode for k-anonymitet, støy eller sikker summering | **contradicted** | Søk i CellScaffold `Sources/` og CellProtocol `Sources/`: 0 treff |
| Spørreskjemaet holder «bare samlede tall» og «pseudonymisert» | **contradicted** | `QuestionnaireCampaignCell.swift:1405–1409` er bare tekst; `responseInsights` (`:1164–1176`) og CSV (`:3630`) har alltid `recipientID` og `displayName` |
| En entitet kan godkjenne en ventende forespørsel i en generell innboks | **contradicted** | `GeneralCell.swift:1657`: `ownerApprovalRequired` avviser alle som ikke er eier |
| Det finnes et mønster for samtykke som Agreement-vilkår | retrieved | CellBase `ChatCell`: signert invitasjon + signert aksept, `LookupCondition target.audience.admission.*`, `automaticWhenConditionsMet` (`ChatCell.swift:1918–1996`); Py/Go har samme vilkår (`PDD_dele-dokumenter` §0) |
| Gjenbrukbar invitasjon/opptak (InvitationAdmission) finnes | unavailable | Foreslått i `PDD_dele-dokumenter_2026-11-14`; G1 venter |
| Tilbakekalling stopper tilgang | retrieved (lest, ikke kjørt) | `GeneralCell.swift` rundt 1640: kontrakt tilbakekalles og `feedAuthorizations.revalidate` kjøres |
| Diagrammer kan vise skjulte verdier | **contradicted** | Web `skeleton-runtime.js:3504–3523` og Binding `SkeletonView.swift:2303–2331` dropper punkter uten tall |
| Diagram og tabell virker i både web og Binding | retrieved | Web `skeleton-runtime.js:4085–4096`; Binding `SkeletonView.swift` `case "table"`, `"chart"` |
| PyResearchScaffold kan analysere eksporterte data | retrieved, med forbehold | Datasett, regresjon, figurer og CellBridge med Agreement finnes (README, WP1–WP4). `contracts/dataset-v1.json` krever enhetene `x_V`/`y_mV` |
| Studio kan ta imot et ferdig dashbordutkast | retrieved | `setDraftConfiguration`, `importDraftConfigurationFile` (minne `haven-student-skeleton-help`, `PDD_studentflater`) |
| Staging kan brukes til ekte persondata | **contradicted** | `KOM_I_GANG.md`: «Ikke legg inn ekte persondata om andre der» |
| Studentene må melde prosjektet til Sikt | recalled | Ikke sjekket mot UiO denne økten. Brukes ikke som bærende antakelse; se §6 spørsmål 1 |
| Hva adminflatene returnerer på staging nå | ikke målt | Krever adminrolle. Måles i WP0 |

## 1. Formålstre

Rot: en masterstudent kan hente data til sin egen forskning fra HAVEN, uansett tema, med personvernet bygd inn, og se dem i sitt eget dashbord.

Gjenbruk fra Book 23: `purpose://self-determination.data.verifiability` (etterprøvbarhet, også brukt av `PDD_python-research-scaffold`) som forelder for opphav og eksport. Resten er kandidater navngitt her. Hver kandidat i samtykkedelen dekker en node under `purpose://self-determination.data` i Book 23, og testene er laget for å vise at den noden holdes:

| Book 23-node | Dekkes av |
|---|---|
| `…data.use-purpose` (formålsbinding) | request, entity-decides (formål står på kortet og i kontrakten) |
| `…data.scope` (omfang) | consent-as-agreement (kontrakten gir nøyaktig omfanget), anonymous-aggregates |
| `…data.manner` (behandling og avledede data) | query-at-entity, pseudonymous-rows (svarform samlet eller per person) |
| `…data.recipients` (mottakere) | request-reach, query-at-entity (noden samler, studenten mottar) |
| `…data.duration` (varighet, trekk, sletting) | withdraw, entity-storage |
| `…data.verifiability` (etterprøvbarhet) | release-log, export |
| `…data.exercisability` (kontroll som faktisk kan brukes) | entity-decides, withdraw (ett trykk, synlig status) |
| `…data.locality` (sted) | entity-storage (dataene blir hos entiteten) |

Faser (forslag, se `PLAN.md`): **F1** katalog, anonyme samletall, visning, dashbord i onboarding. **F2** spørre entitetene (N2, N3). **F3** lagring hos entiteten (N4), syntetisk populasjon, støy og sikker summering.

| purposeRef | Tittel | Forelder | Goal (outcome) | Verifier | Fase |
|---|---|---|---|---|---|
| purpose://candidate.forskningsdata-verktoy.root | Studenter henter forskningsdata med personvernet bygd inn | purpose://self-determination.data.verifiability | En ny studentkonto får forskerrollen, åpner sitt eget dashbord med minst ett samletall fra noden på web og i Binding, sender én forespørsel til medstudenter og ser et samlet svar først når minst k har sagt ja | test.fd.e2e-student | F1+F2 |
| purpose://candidate.forskningsdata-verktoy.catalog | Katalog over hva som kan måles | root | Én maskinlesbar katalog (`research.metric-catalog.v1`) lister hvert tall og hver spørringsmal med definisjon, kilde, tidsoppløsning, k, enhet og versjon. Den vises i dashbordet og i studentpakken | test.fd.katalog-dekker-kilder | F1 |
| purpose://candidate.forskningsdata-verktoy.researcher-role | Forskerrolle via Agreement | root | En researcher-VC utstedt av gruppeentiteten Informasjonssystemer (`PDD_informasjonssystemer-gruppeentitet`, §6 spm. 2; inntil den finnes, av noden). Foreløpige navn fra PR #46: credential-type `InformasjonssystemerRoleCredential`, `subjectClaimPath` = `role` med verdien `researcher`, kull i `cohort`, gyldighet i `validUntil` og godtatte bruksvilkår er vilkårene for all forskningstilgang. Samme vilkår og samme svar i Swift, Python og Go | test.fd.rolle-vilkaar, test.fd.rolle-interop | F1 |
| purpose://candidate.forskningsdata-verktoy.anonymous-aggregates | Anonyme samletall fra noden (N1) | root | `ResearchAggregateCell` gir tall fra katalogen i faste dag- eller ukebøtter. Ingen utlevering inneholder identitets-uuid, celle-uuid, visningsnavn eller fritekst. Bøtter med færre enn k er merket skjult, ikke utelatt | test.fd.ingen-identifikator, test.fd.k-terskel, test.fd.faste-bokter | F1 |
| purpose://candidate.forskningsdata-verktoy.release-log | Logg over hver utlevering | anonymous-aggregates | Hver lesing av et samletall eller et svar logges med hvem, mal og versjon, bøtte, k, antall og hash. Studenten ser sin egen logg; nodens eier ser alle | test.fd.utleveringslogg | F1 |
| purpose://candidate.forskningsdata-verktoy.questionnaire-promise | Spørreskjemaet holder det det lover | root | Med `aggregateOnly` gir innsikt og eksport bare tall, og bare når minst k har svart. Med `pseudonymized` har radene et pseudonym per kampanje og ikke navn. `personLinked` er uendret | test.fd.sporreskjema-synlighet | F1 |
| purpose://candidate.forskningsdata-verktoy.request | Studenten lager en forespørsel | root | Studenten velger mal fra katalogen, skriver formål, velger gruppe, svarform (samlet eller per person), periode og lagringstid, og ser nøyaktig det kortet entiteten vil se. Cellen avviser forespørsler som bryter regler (gruppe mindre enn k, rad-data uten begrunnelse, mal som ikke finnes) | test.fd.forespørsel-valideres | F2 |
| purpose://candidate.forskningsdata-verktoy.request-reach | Forespørselen når bare dem den gjelder | request | En forespørsel sendes bare til medlemmer av en gruppe studenten selv er medlem av, eller til dem som åpner en rekrutteringslenke studenten deler. Ingen kan sende til alle brukere | test.fd.rekkevidde | F2 |
| purpose://candidate.forskningsdata-verktoy.entity-decides | Entiteten bestemmer | root | Entiteten ser hvem som spør, formål, nøyaktig hva, svarform, periode, lagringstid og hva som skjer om den trekker seg, og velger Ja, Ikke nå eller Aldri. Ja signerer en aksept med entitetens egen identitet | test.fd.kort-viser-alt, test.fd.ja-ikke-naa-aldri | F2 |
| purpose://candidate.forskningsdata-verktoy.consent-as-agreement | Samtykket er en kontrakt via Agreement-vilkår | entity-decides | Aksepten gir kontrakt på entitetens egen forskningscelle med vilkårene signert aksept + forskerrolle, gjennom `automaticWhenConditionsMet`. Kontrakten gir nøyaktig omfanget i forespørselen og varer til sluttdato. Ingen annen vei inn. Bygger på InvitationAdmission fra `PDD_dele-dokumenter` | test.fd.opptak-via-vilkaar, test.cell.auth-negative | F2 |
| purpose://candidate.forskningsdata-verktoy.query-at-entity | Spørringen går til dataene (N2) | consent-as-agreement | Bidraget regnes ut i entitetens egen celle fra data entiteten selv eier. Bidragene samles i en celle som eies av noden, ikke av studenten. Studenten får bare summen (eller median, fordeling) når minst k har bidratt | test.fd.student-ser-ikke-bidrag, test.fd.k-terskel-svar | F2 |
| purpose://candidate.forskningsdata-verktoy.pseudonymous-rows | Rad-data med pseudonym per forespørsel (N3) | consent-as-agreement | Når svarformen er «per person», får studenten én rad per entitet med pseudonymet H(hemmelighet, forespørsels-id). To forespørsler kan ikke kobles på pseudonymet | test.fd.pseudonym-ukoblet | F2 |
| purpose://candidate.forskningsdata-verktoy.withdraw | Trekke seg, og utløp | consent-as-agreement | Entiteten trekker kontrakten med ett trykk. Neste utregning tar den ikke med, feeden stopper, og begge ser ny status. Kontrakten utløper av seg selv på sluttdatoen | test.fd.trekk, test.fd.utlop | F2 |
| purpose://candidate.forskningsdata-verktoy.entity-storage | Lagring hos entiteten (N4) | consent-as-agreement | Kontrakten kan gi studenten skriving på ett forskningsfelt i entiteten med fast skjema. Entiteten ser alt som er skrevet og kan slette. Lesing går som i N2 eller N3 | test.fd.lagring-skjema-og-sletting | F3 |
| purpose://candidate.forskningsdata-verktoy.cross-language | Likt i Swift, Python og Go | consent-as-agreement | Felles gyldne fixtures (forespørsel, aksept, opptak, avslag, trekk, k-terskel) gir samme svar i Swift, Python og Go. Swift-fixturene lages først | test.fd.interop-fixtures | F2 |
| purpose://candidate.forskningsdata-verktoy.export | Eksport med opphav | purpose://self-determination.data.verifiability | Hvert datasett eksporteres som CSV og JSON med manifest (`research.dataset.v2`: kilde, mal og versjon, bøtter, k, antall samtykker, utleveringslogg-id, hash). PyResearchScaffold leser det og lager figur | test.fd.eksport-til-pyresearch | F1 |
| purpose://candidate.forskningsdata-verktoy.synthetic | Syntetisk populasjon (N0) | root | En generator lager syntetiske entiteter og hendelser med samme skjema som katalogen, med frø, slik at studenten utvikler analysen før ekte data finnes | test.fd.syntetisk-samme-skjema | F3 |
| purpose://candidate.forskningsdata-verktoy.display | Komponenter som viser personvernet | root | Tall-flis, søyle og linje med skjulte bøtter, fordeling, samtykketrakt og opphavskort virker i web og Binding med samme data. Skjult verdi står som «færre enn k» i begge | test.gui.parity, test.fd.skjult-vises | F1 |
| purpose://candidate.forskningsdata-verktoy.display-suppressed | Skjulte bøtter i diagram | display | `{value: null, suppressed: true}` tegnes som merket hull i søyle og linje i både `skeleton-runtime.js` og CellApple `SkeletonView.swift`. Linjen trekkes ikke forbi hullet | test.fd.skjult-vises | F1 |
| purpose://candidate.forskningsdata-verktoy.dashboard-template | Mal: Mitt forskningsdashbord | root | En CellConfiguration med tall-fliser, et diagram, opphavskort og «Mine forespørsler» åpnes i Studio som eget utkast og består nåbarhetssjekken | test.fd.mal-naabar | F1 |
| purpose://candidate.forskningsdata-verktoy.onboarding | Dashbordet som onboarding | dashboard-template | Trinnene i `VURDERING.md` §9 står i studentpakken. En ny studentkonto kommer gjennom trinn 1–6 uten hjelp på under 45 minutter, målt | test.fd.onboarding-tid | F1 |
| purpose://candidate.forskningsdata-verktoy.share-with-supervisor | Del dashbordet med veileder | dashboard-template | Studenten gir veilederen lesing av dashbordet via Agreement. Veilederen ser samme tall, ikke mer | test.fd.deling-veileder | F1 |
| purpose://candidate.forskningsdata-verktoy.privacy-stronger | Støy og sikker summering | query-at-entity | Støy med budsjett per student og sikker summering der heller ikke noden ser bidragene er beskrevet som forskningsspørsmål, med målbart mål før noe bygges | test.fd.f3-spesifisert | F3 |
| purpose://quality.build-and-regression | Alt bygger, eksisterende tester passerer | pkg.std.everything-works | Som i pakken | test.build, test.regression | alle |
| purpose://gui.expectation-agreed-before-build | Bildene er godkjent før koding | pkg.std.gui-surface | Bildene i `images/` er godkjent av Kjetil | test.gui.reference-image-exists | alle |

## 2. Avgrensning og avhengigheter

Hva dette IKKE er:
- Ikke frie spørringer. Bare maler fra katalogen, med versjon.
- Ikke en vei rundt Agreement. Også anonyme samletall krever forskerrollen.
- Ikke innsamling av ekte persondata på staging før §6 spørsmål 1 er besvart.
- Ikke et anonymisert nettverk av hvem som snakker med hvem. Det er N0 (syntetisk) til noen har vist at det kan gjøres trygt.
- Ikke analyseverktøy. Analyse og figurer er PyResearchScaffold sin jobb; her lages bare eksporten den leser.
- Ikke et vedtak om nytt forskningstema.

Avhengigheter. Hver skal være målt før den bygges på, ellers står «ikke målt».

| Kapabilitet | Kilde (fil) | Avgrensning | Målt? | Må virke før test? |
|---|---|---|---|---|
| Admincellenes data (resolver, livssyklus, historikk) | `CellScaffold/Sources/ScaffoldKit/Admin*Cell.swift` | Krever adminrolle; gir identitets-uuid-er | **Ikke målt på staging.** WP0 måler hva de gir, med Kjetils adminrolle | ja (F1) |
| Rolle som `ProvedClaimCondition` | `AdminMetricsSupport.swift:1331`, `GeneralCell.isAuthorizationEnforcingCondition` (`GeneralCell.swift:1666–1682`) | Automatisk opptak krever credential-type og claim-sti | Lest, ikke kjørt | ja |
| Rolle-VC-er fra gruppeentiteten Informasjonssystemer, og `ProvedClaimCondition` + TrustedIssuer i Py/Go | `PDD_informasjonssystemer-gruppeentitet_2026-11-17` (CellProtocolDocuments PR #46, G1 spurt 17.11) | Ifølge den tråden har Py/Go ingen `ProvedClaimCondition` i dag; porten bygges der (formålet condition), ikke her. Ikke kontrollert i denne økten | nei | ja (researcher-role, rolle-interop) |
| InvitationAdmission (felles invitasjon/opptak) | `PDD_dele-dokumenter_2026-11-14` | Ikke bygget; G1 venter | nei | ja (F2) |
| Studio-utkast og nåbarhetssjekk | `PDD_studentflater-skeletonhjelp_2026-11-14` (G1 godkjent 15.11, G1-GUI venter) | Studio kjører ikke nåbarhetssjekk i dag | nei | ja (onboarding) |
| Invitasjon og chat for nye studenter | `PDD_studentoppsett-invitasjon-chat_2026-10-26`, `KOM_I_GANG.md` | Prøvd 11.11 med ny konto på staging | ja, 11.11 | ja |
| Rendering av `table` og `chart` i Binding | CellApple `SkeletonView.swift` | Én serie | Lest, ikke kjørt i Binding denne økten | ja (F1) |
| PyResearchScaffold datasett og figur | `/Users/kjetil/Build/Digipomps/HAVEN/PyResearchScaffold/` | Datasettkontrakt låst til kalibrering; gren ikke på main | Verifisert av Codex 12.11 (README); ikke kjørt her | ja (eksport) |
| Kontrakt-tilbakekalling og feed-revalidering | `GeneralCell.swift` rundt 1640 | | Lest, ikke kjørt | ja (F2) |
| Swift-bygg | Kjetils Mac (Remote Control) eller CI | Skycontaineren har Swift bare via Docker, og CellScaffold App bygger ikke der (minne `haven-cloud-swift-docker`) | | ja |

## 3. Forventningskontrakt — «Det du kommer til å se»

| Leveranse | Type | Hvor | Referanse | Godkjent |
|---|---|---|---|---|
| Vurdering | fil | `VURDERING.md` | — | nei |
| Bilder av dashbord, forespørselskort og forespørselsbygger | bilde | `images/` | `images/README.md`, `images/*-v1.png` | nei (G1-GUI) |
| Metrikkatalog v1 | fil (JSON + tabell i studentpakken) | `contract/research-metric-catalog.v1.json` | — | nei |
| Dashbord med ekte samletall på staging, web og Binding | kjørende flate + skjermbilder | staging; skjermbilder i `evidence/` | `images/dashbord-fylt-*-v1.png` | nei |
| Skjulte bøtter tegnet likt i web og Binding | testutdata + skjermbilder | `TESTRESULT.md#skjult` | `images/dashbord-fylt-*-v1.png` | nei |
| Spørreskjema som holder synligheten | testutdata | `TESTRESULT.md#sporreskjema` | — | nei |
| Forespørsel, kort og trekk ende til ende med tre testkontoer | kjørende flate + skjermbilder | staging; `evidence/` | `images/foresporsel-*-v1.png`, `images/kort-*-v1.png` | nei |
| Interop-fixtures Swift/Python/Go | testutdata | `TESTRESULT.md#interop` | — | nei |
| Eksport lest av PyResearchScaffold med figur | fil + figur | `evidence/eksport/` | — | nei |
| Onboardingtrinn i studentpakken, med målt tid | fil + måling | `MasterHAVEN26/KOM_I_GANG.md`, `TESTRESULT.md#onboarding` | — | nei |

## 4. Tilknyttede formålspakker og lærdommer

Lærdommene som former dette treet:
- **lesson.plan-instead-of-delivery**: etter G2 teller bare radene i §3. Vurderingen og planen er ikke leveransen.
- **lesson.tested-a-different-path-than-production**: `test.fd.skjult-vises` og `test.fd.kort-viser-alt` bruker rendererne selv, i web og Binding.
- **lesson.read-origin-main-before-writing-a-mechanism**: revisjonene står i §0. Opptak bygger på InvitationAdmission, ikke en ny mekanisme.
- **lesson.lookup-again-when-a-surface-is-added**: malen og kortene sjekkes for nåbarhet (`test.fd.mal-naabar`).
- **lesson.planned-documented-as-implemented**: `KOM_I_GANG.md` og `IMPLEMENTERT_OG_VISJON.md` oppdateres bare med det som er målt.
- **lesson.valuetype-equality-false-for-objects**: tester sammenligner sortert JSON.
- **lesson.text-ux-is-not-design** og **lesson.sketch-assumed-a-renderer-it-did-not-have**: bildene er rendret med den ekte web-rendereren; hva Binding ikke viser likt, står i `images/README.md`.
- **lesson.unresolvable-condition-is-invisible** og **lesson.empty-list-keeps-its-slot**: hver liste har en rad for tom tilstand, og knapper ligger ikke bak betingelser som rotscope ikke kan løse.

Automatisk liste fra `purpose_dev.py lookup` følger.


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

## Lærdommer du må lese før dekomponering
- **lesson.plan-instead-of-delivery** (2026-08-21, major): Kjetil ba om en leveranse flere ganger og fikk planer/dokumenter om leveransen i stedet.
    - forebygging: G1 godkjenner formål, ikke arbeid; etter G2 telles bare artefakter listet i §3 'Det du kommer til å se' som fremdrift. Et dokument om leveransen teller aldri som leveransen.
- **lesson.undocumented-plan-switch** (2026-08-24, major): Tre produktive døgn (22.–24.08) så tomme ut i alle statusdokumenter fordi planbyttet fra bølge 1–3 til deploy-seremonien aldri ble skrevet ned.
    - forebygging: STATUS.md i oppgavemappen oppdateres ved hvert planbytte med dato og hvorfor; sjekkes i test.status-current.
- **lesson.planned-documented-as-implemented** (2026-08-24, major): Book/05_Flows_Lifecycle.md beskrev sekvensnummer, signatur og replay som ikke finnes i structen.
    - forebygging: Docs-diff i samme endring, med 'Last verified against code'-dato; planlagt oppførsel merkes eksplisitt.
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
- **lesson.new-cell-must-declare-its-provisioning-mode** (2026-09-09, major): To nye celler i CellScaffold ga tre nye regresjoner: `OrchestratorPersistenceTests testRequireExistingModeRejectsFreshStorageWithoutCreatingBootstrapCells` (opprettet en celle i require-existing-modus mot fersk lagring) og to `TopUpCheckoutTests` som teller celler i provision-only-modus (5 mot forventet 4).
    - forebygging: Enhver ny persistert celle i CellScaffold må eksplisitt svare på tre spørsmål før den registreres: (1) skal den opprettes i require-existing mot fersk lagring? Nei, med mindre den er kanonisk bootstrap. (2) Er den en av de kanoniske eager-bootstrap-cellene som provision-only skal lage? Nesten alltid nei — TopUpCheckoutTests teller dem eksplisitt. (3) Er den en Porthole-publisert flate? Bare da hører den i `reconcilePortholePublishedCellResolves`. Scaffold-intern tilstand registreres i egen funksjon, gated på policy OG provisionOnly, med gjenkjenning av eksisterende mapping.
- **lesson.branch-is-empty-after-eight-work-packages** (2026-09-09, major): Åtte arbeidspakker rapportert utført og verifisert, ACCEPT.md skrevet — men `git branch -v` viste at `pdd/scaffold-admin-delegering` fortsatt pekte på samme commit som `main` (`e1f3e22f`). All koden lå ucommittet i et worktree som bare finnes på én maskin. Ett tapt worktree = 2 750 linjer kode og test borte, med full dokumentasjon på at arbeidet var «levert».
    - forebygging: Skill «filene finnes» fra «branchen har dem». Sjekk `git rev-parse <branch>` mot `git rev-parse <base>` som del av hver verifikasjon som påstår at noe ligger på en branch; er de like, er branchen tom. Legg en commit-pakke inn i planen etter første grønne bygg, ikke etter siste arbeidspakke. Når worktreet bare kan leses fra macOS, kjør sjekken der — ikke hopp over den fordi verktøyet svarer feil.
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
- **lesson.a-conditional-artifact-must-still-cost-something** (2026-09-18, minor): purpose_dev.py validate ble rød på PDD_entitetsdata-egen-kontroll fordi artefaktet 'skeleton/' manglet, selv om G1-GUI var godkjent på bilder Kjetil faktisk hadde sett. Pakken beskrev artefaktet som påkrevd «når Porthole-preview er brukt»; validatoren krevde det alltid.
    - forebygging: Et betinget krav oppfylles av et *annet krav*, aldri av et fravær. Feltet 'satisfiedByDeclaration' peker på en fil og en overskrift og krever minst ett punkt under den: enten viser du skjelett-JSON-en bildet er rendret fra, eller du skriver ned hva skjelettet ikke kan rendre. Begge tvinger frem spørsmålet «kan flaten dette?». Feilmeldingen navngir begge veier ut. Sjekket begge veier: rød uten erklæring, grønn med.
- **lesson.read-origin-main-before-writing-a-mechanism** (2026-09-22, major): Runde 1 av PDD_entitetsdata skrev en egen resolver for lenkede identiteter (EntityLinkAuthorizer, ny CellAuthorizationPath.linkedIdentity, ny hook pa GeneralCell). Da patchen ble lagt mot origin/main viste det seg at IdentityLinkRegistry og GeneralCell.authorizationEvidence allerede gjorde det samme, landet av en annen oppgave (purpose://candidate.entity-link.resolver-honours-link). Hele resolveren ble forkastet.
    - forebygging: Brief-audit skal si HVILKEN revisjon noe ble lest fra, og for et formal som skal endre en mekanisme skal kilden vaere origin/main (git show origin/main:<fil>), ikke utsjekket. Preflight-skriptet sjekker na at patchen passer mot origin/main i et eget worktree for noe legges pa. Og: for du skriver en mekanisme, grep pa main etter navnet pa det den skal gjore (her: sameEntity, linkedIdentity) - ikke bare etter typen du planlegger a lage.
- **lesson.method-lived-only-on-one-machine** (2026-09-24, major): Metoden selv — Book 35 (PDD-arbeidsflyten), Book 36, lærdomsregisteret med 50 lærdommer, formålspakkene, purpose_dev.py — lå bare i ett utsjekk på Kjetils Mac på grenen codex/docs-cleanup-20260810, aldri på main; derfor verken i HAVEN eller hos andre utviklere.
    - forebygging: Metodeartefakter landes som kode: PR til main og pin-oppdatering i HAVEN. Test: git cat-file -e origin/main:<fil> for hver metodefil.
- **lesson.downstream-pin-must-come-from-the-consumer** (2026-09-24, major): Nedstrøms-baselinen for CellScaffold var rød 22.09 («cellprotocol krever swift-crypto 4.5.2, dimymint krever 3.x») og ble rapportert som prosjektets blokkering. CellScaffold main pinnet DiMyMint af41630, som løser swift-crypto 4.x; skriptet hadde hardkodet en eldre revisjon (1718fda).
    - forebygging: Et nedstrøms-skript leser alle transitive pinner fra forbrukerens egen Package.swift/Package.resolved på origin/main ved kjøring, og logger dem. En rød avhengighetsoppløsning i et skript med hardkodede pinner er ikke et funn før pinnene er bekreftet mot forbrukerens resolved.
- **lesson.disposable-worktree-must-be-reset-before-checkout** (2026-09-24, minor): pdd-check/Binding ble stående på 72f6a6c9 i to kjøringer selv om skriptet ba om origin/main: «Your local changes to project.pbxproj would be overwritten by checkout». Baselinen målte feil Binding-revisjon uten å si fra.
    - forebygging: Engangs-worktrees resettes hardt (`git reset --hard` + fjern Package.resolved) før hver utsjekk, og skriptet skriver ut revisjonen den faktisk står på — en avvikende revisjon skal stoppe kjøringen, ikke logges forbi.
- **lesson.report-the-commit-you-pushed-not-the-one-you-planned** (2026-09-24, minor): TESTRESULT og PLAN sa «commit ebb0b7f». Branchen sto på e66b7f1 — commit.sh hadde laget en ny hash — og var ikke pushet. Push-skriptets EXPECT måtte rettes før det kunne kjøre.
    - forebygging: Etter hver commit/push: les `git rev-parse --short HEAD` og `git ls-remote --heads origin <branch>` og lim inn utdataene i STATUS/TESTRESULT. Sjekk også for remote-tracking ref før du sier «pushet» (lesson.branch-is-empty-after-eight-work-packages, samme familie).
- **lesson.lookup-again-when-a-surface-is-added** (2026-09-24, major): De nye seksjonene i «Utvid entiteten» (B10) var portet på synlighet med rot-scope, og listen med verktøyets forespørsel forsvant — samme feil som lesson.unresolvable-condition-is-invisible fra 05.09.
    - forebygging: For hver ny eller endret skjelettflate: kjør `purpose_dev.py lookup --tags skeleton gui` før utformingen, og `BindingTests/CellConfigurationVerifierXCTest/testNoLocalSurfaceHidesItsOwnWaysIn` + `testPersonalCopilotLocalSurfacesLoadWithoutReferenceFailures` før flaten vises eller committes.
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
- **lesson.host-mutation-without-reading-the-coordination-file** (2026-10-02, major): 30.09 satte en Claude-tråd ut en gren-commit på staging og byttet invitasjonene, med Kjetils ja, men uten claim. En Codex-tråd hadde claim på samme container (HD-0141), staging var reservert for 2026.9.4, og deploykøen trodde i to døgn at staging kjørte forrige utgivelse.
    - forebygging: Før enhver vertsmutasjon: les `_losen-queue/KOORDINERING.md`, kjør `hd coord status`, ta egen claim på en HD-oppgave, og før utsettingen inn i køen etterpå. Test: jobbloggen for utsettingen viser `hd coord status` uten annen claim på samme tjeneste, og egen claim, før første kommando mot verten. Eierens ja til å sette ut erstatter ikke sjekken.
- **lesson.remembered-install-state-is-not-measured** (2026-10-02, minor): En plan sa at agenten på Macen var bygget fra en bestemt gren, og bygde grenvalg og et åpent spørsmål til eieren på det. Agenten var installert på nytt fra `main` av en annen tråd seks dager tidligere.
    - forebygging: Hva som er installert, måles før en plan bygger på det: dato og navn på binærene og sikkerhetskopiene i `bin/`, `launchctl print`, og om commiten er på `origin/main`. Test: påstandstabellen merker installasjonstilstand som hentet med måletidspunkt, aldri som husket.
- **lesson.own-committed-tests-changed-without-asking** (2026-10-03, major): Ti tester tråden selv hadde committet tidligere samme dag, ble endret uten å spørre: tretten endringer, og sju av dem snudde eller fjernet noe en test krevde godtatt.
    - forebygging: En committet test er eksisterende, uansett hvem som skrev den og når. Før hver commit leses testendringene rett fra git; en endring i en committet test er et spørsmål til eieren. Test: skriptet som lister testendringer fra git, viser ingen endring i en committet test uten en godkjenning ført i STATUS.md.
- **lesson.accept-written-from-memory-had-27-errors** (2026-10-03, major): Første utkast til ACCEPT.md og TESTRESULT.md hadde 27 feil da en uavhengig tråd holdt det mot bevisfilene; ett av dem var påstanden om at hver frosset utgave ble angrepet etter at den var satt ut.
    - forebygging: Tall, klokkeslett, commit-numre og sitater i ACCEPT.md og TESTRESULT.md fylles inn fra bevisfilene av kode, og en uavhengig tråd holder hver påstand mot bevisene før eieren får dokumentene. Test: rapporten fra kontrollen ligger blant bevisene, med en dom per påstand.
- **lesson.red-first-claimed-for-tests-that-were-not** (2026-10-04, minor): TESTRESULT.md sa at hver ny eller endret test var kjørt rød først. Tolv endringer i tester som alt fantes, og ti av de 24 nye i første runde, kom inn sammen med koden og var aldri kjørt røde.
    - forebygging: En påstand om alle tester føres per test: «rød først» listes med hvilke tester som fantes i den røde kjøringen, og hvilke som kom til etterpå. Test: antall tester i den røde og i den grønne kjøringen står i TESTRESULT.md, og differansen er forklart.
- **lesson.estimate-assumed-one-attack-round** (2026-10-04, minor): Planen sa «rundt tre og en halv time etter G1». Den siste utgaven var målt på nett 34 timer og 50 minutter etter.
    - forebygging: Et anslag for arbeid som skal angripes av en uavhengig tråd, oppgis per runde, og sier at antall runder er ukjent til første angrep er målt. Test: planen har tid per runde, ikke en sluttid.
- **lesson.full-path-rule-broken-in-short-references** (2026-10-05, major): Kjetil måtte for tredje gang si at filer skal stå med hele stien («Du må legge med hele banen til filer som dette: ACCEPT.md»): meldingene og spørsmålene ved G3 hadde bare filnavnet.
    - forebygging: Hver melding til eieren kontrolleres maskinelt før den sendes: et ord som ender på en filendelse og ikke begynner med en rot, stopper sendingen. Det gjelder hver gang en fil nevnes, også i spørsmål. Test: skriptet som kontrollerer meldinger, gir null funn på hver melding som ber om en port.
- **lesson.file-copied-to-the-mac-was-the-previous-version** (2026-10-05, major): En commit gikk ut med testen, men uten endringen den prøvde: filkopien fra skyøkten til Macen meldte «written», og fila på Macen var forrige utgave. To skript mistet dessuten kjørbar-biten på veien.
    - forebygging: Hver utgave som skal til Macen, legges under et nytt filnavn i utdatamappen. Sjekksummen på Macen sammenlignes med den i skyen i et eget steg, og neste steg (commit eller køjobb) startes ikke i samme kommando. Test: commit-jobben viser «git diff --cached --stat --summary» før commit, og lista over filer og moduser sammenlignes med det som skulle med.
- **lesson.pr-opened-without-reading-the-base-branch-ci** (2026-10-05, minor): PR #30 ble opprettet uten at CI-tilstanden på main var lest: løpet sto til tidsgrensen på 25 minutter av en grunn som hadde stått på main i seks dager, og den første lesningen av loggen, at det stoppet før PR-ens tester hadde startet, ble felt av den uavhengige kontrollen.
    - forebygging: Før en PR opprettes, listes løpene for basisgrenen; har hodet ikke noe grønt løp med samme testskript, rettes det først, eller rettelsen tas med. Før en årsak skrives ned for et rødt løp, leses avsnittet om CI i skillen, og siste linje i en logg kalles ikke stedet det stoppet. Test: skriptet som oppretter en PR, viser siste løp på basisgrenen og stopper når det er rødt.
- **lesson.status-message-sent-before-the-documents-were-checked** (2026-10-06, minor): Dokumentene og meldingen til eieren 06.10 om kvelden skrev slutninger som målinger («haven-deploy ville blitt kjørt med umask 077», «skallet ventet fem sekunder: målt»), gjenga kontrollenes merknader som «en feil» og «alle rettet», utelot ett av fire svar der en vakt ble beskrevet, og ga et klokkeslett for når en kjøring ville være ferdig, uten grunnlag. Meldingen var sendt et kvarter før kontrollen av dokumentene.
    - forebygging: Dokumenter, LES-MEG ved siden av et skript og meldingen til eieren kontrolleres mot kildene av en som ikke har skrevet dem, før meldingen sendes. Ved hver påstand står det om den er målt, lest eller sluttet, og et tidsanslag gis som et spenn med grunnlaget. Test: kontrollrapporten er eldre enn meldingen, og rettelser gjort etter kontrollen er merket som ukontrollert.
- **lesson.commit-file-built-on-a-stale-copy-and-the-check-got-the-same-copy** (2026-10-06, major): README.md i commiten `c5058f49` fikk 172 endrede linjer (104 ut, 68 inn) der rundt 50 nye var ventet: tekst fra tre tidligere commiter falt ut.
    - forebygging: Hver fil i en commit-pakke bygges på git-objektet i foreldercommiten, og skriptet som committer, krever ventet antall linjer inn og ut per fil og stopper ellers. Kontrolltråden får commiten og finner grunnlaget selv. Test: skriptet stopper når forskjellen mot forelderen ikke er den ventede.
- **lesson.brake-file-written-after-the-chain-had-passed-the-brake** (2026-10-06, minor): Bremsefilen ble lagt 13 sekunder etter at kjedeskriptet hadde passert bremsesjekken foran pushen, så en commit med en kjent feil ble pushet.
    - forebygging: Et tall et menneske må lese før neste steg som ikke kan angres, deler kjeden i to jobber, eller skriptet krever tallet selv. Test: kjeden stopper foran pushen når commitens linjetall avviker fra det ventede.
- **lesson.check-ran-before-the-last-numbers-and-did-not-read-the-message** (2026-10-06, minor): Kontrollen av akseptdokumentet ble gjort før de 27 siste kallene var målt, og meldingen til eieren var ikke med. En ny kontroll rett før sending fant åtte ting, blant annet at meldingen la en svakhet til angrepet alene der råsvarene fra nett viste det samme.
    - forebygging: Den siste uavhengige kontrollen kommer etter at siste tall er ført inn, regner tallene på nytt fra råfilene og leser meldingen eieren får. Test: kontrollrapporten er yngre enn siste bevisfil og eldre enn meldingen.
- **lesson.early-return-rule-changed-what-happens-when-the-lookup-is-down** (2026-10-06, minor): Et spørsmål med et ord fra ordlisten får henvisningen (HTTP 200) også når oppslaget ikke kan nås, der andre spørsmål får 503 eller 403. Det sto verken i spesifikasjonen eller i en test.
    - forebygging: For hver regel som svarer før en avhengighet spørres, sier spesifikasjonen hva som skjer når avhengigheten er nede, og en test holder det fast. Test: en test der avhengigheten er tatt bort, med ventet svar for begge grener.
- **lesson.way-back-was-called-a-way-back-after-dry-runs-only** (2026-10-06, minor): Veien tilbake fra utsettingen er tørrkjørt to ganger, men selve byttet tilbake er aldri kjørt, der spesifikasjonen krever en vei som virker også når siden er nede.
    - forebygging: En vei tilbake er vist når byttet er kjørt, for eksempel mot en egen container med samme image. Ellers står den som «ikke vist» i planen eieren godkjenner. Test: bevis for et gjennomført bytte, eller linjen «ikke vist» i planen.
- **lesson.order-of-steps-changed-to-keep-a-promised-time** (2026-10-06, minor): Utgaven ble satt ut før rettelsen av README.md var committet, mot planen, fordi kontrollen av rettelsen tok 28 minutter der 15 var ventet.
    - forebygging: Planen sier hvilke steg som kan bytte plass når noe tar lengre tid, og kontroller får en hard tidsgrense. Test: hvert planbytte har en linje i STATUS.md med hva som tapes.
- **lesson.correction-to-a-list-removed-words-it-already-caught** (2026-10-06, minor): To rettelser i ordlisten ga nye hull: et unntak som ble sammenlignet etter at ø var brettet til o, tok bort «nøtte», og en innsnevring tok bort «tolererer».
    - forebygging: Hver utgave av en liste kjøres mot alle tidligere eksempler, både ord som skal treffe og ord som ikke skal, og eksemplene ligger som fikstur. Test: en fikstur med ett eksempelord per oppføring og en liste med ord som ikke skal treffe.
- **lesson.rewritten-draft-got-new-errors-where-it-was-rewritten** (2026-10-06, minor): Seks utkast til spesifikasjonen ble lest i fem kontrollrunder som fant 110 ting til sammen. Hver runde fant feil i det som var skrevet om etter den forrige.
    - forebygging: Etter en omskriving kontrolleres det omskrevne på nytt, og eieren får vite når siste utgave ikke er kontrollert. Tall fylles inn av kode. Test: dokumentet sier hvilken utgave kontrollen leste.
- **lesson.known-pitfall-repeated-in-a-small-follow-up-without-lookup** (2026-10-06, minor): Testen for avvik 4 sammenlignet to like svarkonvolutter med `XCTAssertEqual` og var rød mot riktig kode. Den grønne kjøringen fanget det før commit.
    - forebygging: `lookup` kjøres for hvert steg som skriver kode eller tester, også små oppfølginger, og oppgaven til kontrolltråden ber den holde testen mot lærdommene for taggene. Test: commit-trinnet stopper uten grønt bevis for nettopp filene som committes.
- **lesson.full-path-rule-passed-the-checker-in-descriptions-and-file-cards** (2026-10-06, minor): Meldingen som ba om G3, gikk gjennom kontrollskriptet for hele banen, men fem filer ble sendt som kort uten bane i sendingen, og dokumenter ble nevnt med en beskrivelse («akseptdokumentet») før banen sto.
    - forebygging: Hver fil som leveres i samtalen, står med hele banen i meldingen som følger med, og en beskrivelse av en fil får banen ved første nevning. Test: antall leverte filer er lik antall baner i meldingen.
- **lesson.status-did-not-say-status-or-what-to-do** (2026-10-06, major): Eieren 06.10 om statusen han fikk: «Dette sier meg ingenting om hva status er eller hva jeg skal gjøre.» Han skrev selv formålet og spurte hva som gjensto for å få prøvd med de to mottakerne.
    - forebygging: En statusmelding åpner med hvor formålet står for dem det gjelder, så det eieren skal gjøre i nummererte punkter, så leddene som gjenstår. Arbeid på et sidespor kalles et sidespor. Test: kontrolløren får eierens ord fra §0 og svarer på om første avsnitt sier hva mottakerne har fått.
- **lesson.few-steps-was-counted-for-the-recipient-and-not-for-the-owner** (2026-10-07, minor): Utkastet til G1 talte tre håndgrep for mottakeren og skrev «én gang per person» for eieren («ett trykk» i spesifikasjonen bak). Bildet viste to Touch ID per person og en kode å sammenligne, og rekkefølgen på eierens steg sto feil. Kontrollen før framlegget fant det.
    - forebygging: Der «få håndgrep» er et formål, telles håndgrepene for hver part, eieren først, per person og per runde, fra bildene og i rekkefølgen de skjer. Et steg som følger av et forslag, merkes som forslag. Test: et opptak på en ren maskin der håndgrepene er telt.
- **lesson.a-second-safeguard-hid-that-the-first-had-no-test** (2026-10-06, major): Én av 145 innsatte feil, kalt nr. 100 i filnavnene for omkjøringen («fila legges tilbake mens haven-deploy kanskje går»), ble ikke fanget, og alle 133 testene var grønne med den.
    - forebygging: To vern foran samme handling får hver sin test der det andre ikke kan svare. En innsatt feil som ingen test fanger, leses i utskriften før den regnes som ufarlig. Test: for hvert vern finnes et tilfelle der bare det vernet står mellom skriptet og handlingen.
- **lesson.deadline-request-left-out-what-follows-when-it-passes** (2026-10-06, minor): Utkastet til meldingen etter byttet ba eieren godkjenne to forespørsler innen 24 timer, uten å si at invitasjonen da er brukt opp og at en ny trengs (etter kontrollørens lesning: nytt bytte og ny omstart av staging), og uten steget etter: hans godkjenning av mottakernes egne forespørsler. Kontrollen før sending fant det.
    - forebygging: En forespørsel med frist sier hva som skjer når fristen går ut, og nevner hvert senere steg som er eierens. Test: kontrolløren spør for hver frist i meldingen «hva følger hvis den ikke holdes?» og «hva er hans neste steg etter dette?».
- **lesson.question-used-the-repos-words-and-came-back-as-a-question** (2026-10-07, minor): To av fem nummererte punkter til eieren kom tilbake som spørsmål: «Hva gjør assistentidentiteten?» og «Hva mener du med at vedlegg kan gå til main? Vi skal ikke lagre vedlegg i git så forklar hva du mener.»
    - forebygging: Et spørsmål til eieren bruker hans ord og sier hva en ting gjør før det spør om den. Test: kontrolløren leser hvert spørsmål, slik det blir sendt, som en som ikke kjenner repoet, og sier hvilke ord som må forklares.
- **lesson.shared-swiftpm-cache-lost-its-ownership-marker** (2026-10-08, minor): Første bygg i et nytt CellProtocol-arbeidstre stoppet etter 4 s: haven-swiftpm.sh exit 64, «existing cache lacks the required ownership marker: …/T/haven-swiftpm-bounded/caches/90c10549…».
    - forebygging: Byggeskript for en PDD setter HAVEN_SWIFTPM_CACHE_KEY=<pdd-slug> (egen cache) i stedet for å reparere den delte; koster ett kaldt bygg (6 min for CellProtocol). Test: skriptet skriver cache-key i rapporten.
- **lesson.xctest-stdout-export-interleaves-with-its-own-log** (2026-10-08, minor): En test printet 49 kB JSON til stdout mellom markører for at byggeskriptet skulle klippe den ut; fila ble ugyldig ved byte 49156 — XCTests egen «Test Case '…' passed»-linje lå midt inne i JSON-en.
    - forebygging: En test som skal levere data til et skript, skriver til en fil (NSTemporaryDirectory()) og printer bare stien; skriptet validerer JSON før det kopierer. Og: /usr/local/bin/python3 på Kjetils Mac er en x86-binær («Bad CPU type in executable») under launchd — bruk /usr/bin/python3 eller node i skript.
- **lesson.shared-cellresolver-fixture-unique-names** (2026-10-12, minor): Integrasjon kunne treffe en tidligere emitter selv om nytt registerkall ikke kastet.
    - forebygging: Bruk unike registreringsnavn i sharedInstance-fixtures, og mål actual loadCell/flow mot den nye cellen.

## Book 23-noder som kan være forelder/gjenbruk (leksikalsk forslag, verifiser)

## 5. Avledede tester (samlet)

| testRef | Formål | Hvordan | Evidens | Status |
|---|---|---|---|---|
| test.fd.e2e-student | root | Tre nye testkontoer på staging (student, to medstudenter) + k satt til 2 for testen: rolle, dashbord på web og i Binding, forespørsel, to ja, samlet svar vises; med ett ja vises «skjult» | TESTRESULT.md#e2e | venter |
| test.fd.katalog-dekker-kilder | catalog | Skript: hver katalogpost peker på en kilde som finnes i koden, og hvert tall `ResearchAggregateCell` gir har en katalogpost | TESTRESULT.md#katalog | venter |
| test.fd.rolle-vilkaar | researcher-role | Swift-test: uten credential avslag; med credential men uten godtatte vilkår avslag; med begge kontrakt | TESTRESULT.md#rolle | venter |
| test.fd.rolle-interop | researcher-role | Samme tre tilfeller som fixtures i Py og Go | TESTRESULT.md#interop | venter |
| test.fd.ingen-identifikator | anonymous-aggregates | Test fyller noden med kjente identiteter og celler, henter alle maler, og leter etter hver uuid og hvert visningsnavn i utdata. Forventet 0 treff | TESTRESULT.md#anonym | venter |
| test.fd.k-terskel | anonymous-aggregates | Bøtte med k−1 gir `suppressed: true` og ingen verdi; bøtte med k gir verdien | TESTRESULT.md#anonym | venter |
| test.fd.faste-bokter | anonymous-aggregates | En forespørsel med fritt tidsvindu avvises; bare kalenderdag og uke godtas | TESTRESULT.md#anonym | venter |
| test.fd.utleveringslogg | release-log | Hver lesing gir én loggpost med mal, bøtte, k, antall og hash; studenten ser bare sine | TESTRESULT.md#logg | venter |
| test.fd.sporreskjema-synlighet | questionnaire-promise | Swift-test per synlighet: `aggregateOnly` gir ingen `recipientID`/`displayName` i innsikt eller CSV og skjuler under k; `pseudonymized` gir pseudonym, ikke navn; `personLinked` uendret | TESTRESULT.md#sporreskjema | venter |
| test.fd.forespørsel-valideres | request | Avvist: gruppe mindre enn k, rad-data uten begrunnelse, ukjent mal, sluttdato etter maks. Godtatt: gyldig forespørsel | TESTRESULT.md#foresporsel | venter |
| test.fd.rekkevidde | request-reach | Forespørsel til en gruppe studenten ikke er medlem av avvises; rekrutteringslenke virker bare for den som åpner den | TESTRESULT.md#foresporsel | venter |
| test.fd.kort-viser-alt | entity-decides | Playwright på web og test i Binding: kortet inneholder hver post i forespørselen (hvem, formål, mal, svarform, periode, lagringstid, trekk) | TESTRESULT.md#kort | venter |
| test.fd.ja-ikke-naa-aldri | entity-decides | Ja gir kontrakt; Ikke nå gir ingen kontrakt og kan svares senere; Aldri gir ingen kontrakt og ingen ny forespørsel fra samme student på samme mal | TESTRESULT.md#kort | venter |
| test.fd.opptak-via-vilkaar | consent-as-agreement | Kontrakt bare med signert aksept + rolle; forfalsket aksept, annen identitet og utløpt aksept avvises | TESTRESULT.md#opptak | venter |
| test.cell.auth-negative | consent-as-agreement | Fra pakken: alle uautoriserte kall avvises | TESTRESULT.md#opptak | venter |
| test.fd.student-ser-ikke-bidrag | query-at-entity | Studenten prøver å lese enkeltbidrag fra samlecellen og fra entitetens celle: avslag begge steder | TESTRESULT.md#n2 | venter |
| test.fd.k-terskel-svar | query-at-entity | Svar med k−1 bidrag er skjult; med k vises summen | TESTRESULT.md#n2 | venter |
| test.fd.pseudonym-ukoblet | pseudonymous-rows | Samme entitet i to forespørsler gir to ulike pseudonymer; samme forespørsel gir samme | TESTRESULT.md#n3 | venter |
| test.fd.trekk | withdraw | Etter trekk: neste utregning har ett bidrag færre, feeden stopper, begge ser «trukket» | TESTRESULT.md#trekk | venter |
| test.fd.utlop | withdraw | Kontrakt med sluttdato i fortiden gir avslag | TESTRESULT.md#trekk | venter |
| test.fd.lagring-skjema-og-sletting | entity-storage | Skriving utenfor skjemaet avvises; entiteten ser og sletter det studenten skrev | TESTRESULT.md#n4 | venter |
| test.fd.interop-fixtures | cross-language | Swift lager fixtures; Py og Go gir samme opptak/avslag på alle | TESTRESULT.md#interop | venter |
| test.fd.eksport-til-pyresearch | export | Eksport fra staging lastes i PyResearchScaffold med `research.dataset.v2`, hashen stemmer, og en figur lages | TESTRESULT.md#eksport | venter |
| test.fd.syntetisk-samme-skjema | synthetic | Generator med frø gir data som består samme skjemasjekk som ekte eksport, og samme frø gir samme data | TESTRESULT.md#syntetisk | venter |
| test.fd.skjult-vises | display, display-suppressed | Samme tilstand rendret i web (Playwright) og Binding (snapshot-test): skjult bøtte har merket og teksten «færre enn k»; linjen brytes | TESTRESULT.md#skjult | venter |
| test.gui.parity | display | Fra pakken: bilde mot godkjent referanse, samme viewport, i web og Binding | ACCEPT.md#gui | venter |
| test.fd.mal-naabar | dashboard-template | Malen importeres i Studio og nåbarhetssjekken gir 0 funn | TESTRESULT.md#mal | venter |
| test.fd.onboarding-tid | onboarding | En person uten forkunnskap (eller Claude med en ny konto og bare studentpakken) gjennomfører trinn 1–6; tid og stopp skrives ned | TESTRESULT.md#onboarding | venter |
| test.fd.deling-veileder | share-with-supervisor | Veileder med lese-kontrakt ser dashbordet; uten kontrakt avslag | TESTRESULT.md#deling | venter |
| test.fd.f3-spesifisert | privacy-stronger | Inspeksjon: F3-delen har mål, trusselmodell og målemetode før noe bygges | ACCEPT.md#f3 | venter |
| test.build | purpose://quality.build-and-regression | CellProtocol `swift build`, CellScaffold `swift build`, Binding `xcodebuild`, PyCellProtocol `pytest`, GoCellProtocol `go test ./...` | TESTRESULT.md#build | venter |
| test.regression | purpose://quality.build-and-regression | Full testmengde i hvert berørt repo; antall før og etter | TESTRESULT.md#regression | venter |
| test.docs-updated | purpose://quality.docs-in-same-change | Les diff; kryss av i ACCEPT.md | ACCEPT.md#docs | venter |
| test.status-current | purpose://quality.work-is-visible | Sammenlign STATUS.md med filene i mappen | ACCEPT.md#status | venter |

## 6. Åpne spørsmål til Kjetil

Bare spørsmål som endrer treet. Hvert har en anbefaling.

1. **Hva får noden telle uten å spørre hver enkelt, og hvor skjer ekte innsamling?** Anbefaling: N1 bare for metadata noden selv lager om drift og om hvilke celletyper som brukes, oppført i en offentlig katalog. Alt om innhold (meldinger, dokumenter) krever samtykke (N2–N4). Ekte deltakere i N2–N4 først når prosjektet er godkjent ved UiO; på staging bare testkontoer og syntetiske data.
2. **Hvem utsteder forskerrollen?** **Besluttet 18.11.2026 (Kjetil):** gruppeentiteten Informasjonssystemer, eid av Kjetil og Petter Nielsen, utsteder forskerrollen. Kjetil: «Det er den korrekte eierskapsmodellen. Den som eier hardwaren eier sannsynligvis scaffoldet, men andre kan eie sine egne celler også.» Inntil gruppa finnes, utsteder noden.
3. **Hvilken minste gruppestørrelse k?** Anbefaling: 5 som standard, 2 bare i tester. På staging blir mange tall skjult, og det er riktig.
4. **Hvem eier samlecellen i N2?** Anbefaling (endret 18.11): gruppeentiteten Informasjonssystemer eier samlecellen som sin egen celle på scaffoldet. Det følger prinsippet Kjetil ga 18.11 om at andre enn hardware-eieren kan eie egne celler. Noden kjører cellen, men eier den ikke. Ikke bekreftet av Kjetil for dette punktet. Kortet sier rett ut hvem som legger sammen tallene («Tallet ditt legges sammen av Informasjonssystemer; studenten ser bare summen»). Alternativet, sikker summering der ingen ser bidragene, er et forskningsspørsmål (F3), ikke noe vi har.

## 7. Revisjonslogg

| Iterasjon | Dato | Hva endret seg | Hvem |
|---|---|---|---|
| 0 | 2026-11-17 | Opprettet | Losen |
| 1d | 2026-11-18 | §6 spm. 2 besluttet av Kjetil (Informasjonssystemer utsteder forskerrollen). Spm. 4 anbefaling endret til at gruppa eier samlecellen | Claude |
| 1c | 2026-11-17 | §2 og researcher-role peker på PDD_informasjonssystemer-gruppeentitet (PR #46) for rolle-VC-er og Py/Go-porten av ProvedClaimCondition, så den ikke bygges to ganger | Claude |
| 1b | 2026-11-17 | §6 spm. 2 og 4: gruppeentiteten «Informasjonssystemer» (Kjetil + Petter Nielsen) lagt inn som anbefalt utsteder, etter Kjetils forslag i en annen tråd | Claude |
| 1 | 2026-11-17 | Vurdering (`VURDERING.md`), brief-audit med ni funn, tre med 23 formål i tre faser, 33 tester, 4 spørsmål, planutkast. G1 bedt om | Claude |
