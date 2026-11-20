# Vurdering — hva studentene trenger for å hente forskningsdata fra HAVEN

Dato: 2026-11-17. Skrevet for Kjetil, som grunnlag for formålstreet i `FORMAALSSPEC.md` og planutkastet i `PLAN.md`.
Kilder lest denne økten: CellScaffold `main` `57ce8c0` (17.11), CellProtocol `main` `14fd9dc` (12.11), CellProtocolDocuments `main` `e7808fe` (16.11), og på Macen `PyResearchScaffold` (gren `codex/research-scaffold-wp5`, `a7871d8`) og to lokale PDD-er (`PDD_python-research-scaffold_2026-11-06`, `PDD_scaffold-admin-komponentdashboard_2026-11-01`). Ingenting er kjørt mot staging i denne økten.

## 1. Kort svar

Studentene trenger fem ting, uansett tema:

1. **En katalog over hva som kan måles**, med definisjon, kilde, tidsoppløsning og minste gruppestørrelse for hvert tall. Uten den vet ingen hva et tall betyr, og forskningen kan ikke gjentas.
2. **Anonyme samletall fra noden** (det operatøren av scaffoldet ser), men gjennom en egen forskningsprojeksjon. Det adminflaten viser i dag er ikke anonymt: den lister identitets-uuid-er og hvilke celler hver identitet har (se funn 1).
3. **En måte å spørre entitetene på**, der entiteten ser nøyaktig hva som spørres om, svarer ja, ikke nå eller aldri, og kan trekke seg. Svaret blir en kontrakt på entitetens egen celle via Agreement-vilkår, likt i Swift, Python og Go. To former: *spørring* (et tall regnes ut hos entiteten og legges sammen med andres) og *lagring* (entiteten gir studenten et sted i sin egen entitet å skrive forskningsdata, for eksempel dagbok eller eksperimentlogg).
4. **Eksport med opphav**: hvert datasett har et manifest (kilde, tidsvindu, gruppestørrelse, antall samtykker, malversjon, hash), og kan leses rett inn i PyResearchScaffold for analyse og figurer.
5. **Visningskomponenter som viser personvernet**: et skjult tall skal stå som «færre enn 5», ikke forsvinne. I dag dropper både web og Binding datapunkter uten tall (funn 6).

Et eget forskningsdashbord som første oppgave i onboardingen er et godt valg. Studenten lærer celler, keypaths, Agreement og skeleton på noe de faktisk trenger, og vi får målt om verktøyene virker for en ny bruker.

Jeg anbefaler å bygge i tre faser: (1) katalog, anonyme samletall, visning og dashbord i onboarding, (2) spørre entitetene, (3) lagring hos entiteten, syntetisk populasjon og sterkere personvern (støy, sikker summering).

## 2. Hva forskningen trenger, og hva HAVEN har i dag

| Behov | Hvorfor i forskning | HAVEN i dag | Mangler |
|---|---|---|---|
| Vite hva som kan måles | Operasjonalisering, gjentakbarhet | Adminflatene har tall, men ingen definisjoner for forskere | Metrikkatalog med definisjon, kilde, oppløsning, k |
| Anonyme samletall | Beskrive bruk uten samtykke fra hver enkelt | `AdminResolverStats`, `AdminMetricsHistory`, `AdminCellLifecycle` (ScaffoldKit) | Projeksjon uten identifikatorer, minste gruppestørrelse, faste tidsbøtter, logg over utleveringer |
| Tilgang som forsker | Hvem får se hva, og hvorfor | Adminrollene bruker `ProvedClaimCondition` med `AdminRoleCredential` (`AdminMetricsSupport.swift:1331`) | En forskerrolle med samme mønster, utstedt av Kjetil eller veileder |
| Spørre entiteter om data | Samtykkebasert datainnsamling | `QuestionnaireCampaignCell` har samtykketekst, trekk og eksport. CellBase `ChatCell` har signert invitasjon og aksept som Agreement-vilkår | Forespørsel bundet til et smalt omfang; utregning hos entiteten; samling som studenten ikke kan se inn i |
| Lagring hos entiteten | Dagbokstudier, eksperimentlogger, longitudinelle data | Entitetsdata eid av entiteten (`PDD_entitetsdata-egen-kontroll`) | Et forskningsfelt i entiteten som studenten kan skrive til under en kontrakt |
| Trekke samtykke | Etikk, personvernforordningen | `GeneralCell` tilbakekaller kontrakt og stopper feed (`GeneralCell.swift` rundt 1640) | Synlig status for begge parter; regel for hva som skjer med tall som alt er lagt sammen |
| Eksport og opphav | Etterprøvbarhet | Spørreskjema eksporterer CSV/JSON. PyResearchScaffold leser datasett, regner regresjon, lager figurer og har signert kjørelogg | Datasettkontrakten i PyResearchScaffold er låst til kalibreringsdata (`units: x_V, y_mV`); trenger en generell v2 med manifest |
| Testdata før ekte data | Utvikle analysen uten risiko | Ingen syntetisk populasjon. `UserSimulationScaffold` er lasttest | Generator for syntetiske entiteter med samme skjemaer |
| Se dataene | Utforsking, presentasjon for veileder | `Visualization` med `table` og `chart` (søyle/linje) virker i både web og Binding | Skjulte verdier markert, flere serier, opphavskort, samtykketrakt |
| Eget dashbord | Arbeidsflate gjennom hele oppgaven | Studio (`CellConfigurationStudio`) med utkast, import og forhåndsvisning; studentguiden `LAG_DIN_EGEN_FLATE.md` | Mal for forskningsdashbord, onboardingtrinn, deling med veileder |

## 3. Datatrappen: fem nivåer, fra minst til mest risiko

| Nivå | Hva | Hvem samtykker | Agreement-vilkår | Eksempel |
|---|---|---|---|---|
| N0 Syntetisk | Genererte entiteter med samme skjema som ekte | Ingen | Ingen ekte data | Teste analyse av invitasjonsnettverk før noen er spurt |
| N1 Operatørmetadata, aggregert | Tall noden selv produserer om drift og bruk av celletyper, uten identifikatorer, med k ≥ 5 og faste tidsbøtter | Ingen enkeltperson; dekket av tjenestens vilkår (§6 spørsmål 1) | Forskerrolle (`ProvedClaimCondition`) + godtatte bruksvilkår | «Hvor mange identiteter har en delt samtale, uke for uke» |
| N2 Samtykkebasert aggregat | Et tall regnes ut i entitetens egen celle og legges sammen med andres; studenten ser bare summen når minst k har sagt ja | Hver entitet, per forespørsel | Signert aksept fra entiteten + forskerrolle; kontrakten gir samlecellen lesing av ett bidrag | «Median antall meldinger per uke i gruppen, blant dem som sa ja» |
| N3 Samtykkebasert pseudonym rad | Én rad per entitet med et pseudonym som er nytt for hver forespørsel | Hver entitet, med uttrykkelig tekst om at svaret er per person | Som N2, men kontrakten gir studenten lesing av raden | Spørreskjemasvar, svar i et eksperiment |
| N4 Lagring hos entiteten | Studenten skriver forskningsdata inn i entitetens eget forskningsfelt; entiteten ser alt, kan slette | Hver entitet | Kontrakt med skriving på ett felt med fast skjema, og lesing som i N2 eller N3 | Dagbokstudie over fire uker; logg fra en unikhetsseremoni |

Pseudonymet i N3 er H(hemmelighet, forespørsels-id). Da kan ikke to forespørsler kobles sammen på pseudonymet. Det er samme lærdom som i konseptdekket: et pseudonym per gruppe kobler alt en person gjør i gruppen.

## 4. Per tema

**Tema A, unik representasjon.** Ekte data hjelper lite før det finnes et unikhetsbevis å måle. Nyttig er: N1 «hvor mange identiteter per scaffold», og fordelingen av lenkede identiteter per entitet (histogram med k), N4 for logger fra seremonier og forsøk (hvor lang tid, hvor mange avbrøt), og N0 for angrepssimulering (sybil-identiteter i en syntetisk populasjon).

**Tema B, personvernsikker simulering.** Dette er temaet verktøyene ligger nærmest. Oppgaveteksten spør: «Hvilke metrikker kan vi implementere i infrastrukturen som best bevarer personvern og allikevel ha nytte? Hva av aggregert data, metadata eller konkret data kan vi spørre entitetene om? Hvordan kan vi bygge registre som bevarer anonymitet og som tillater å gjøre sperringer mot et ønsket utvalg av entiteter?» N1–N3 er et første svar studenten kan måle og forbedre. Snapshots av en gruppe er en N2-forespørsel til alle i gruppen. Informasjonsstrømmer kan telles (meldinger per dag per gruppe), men et anonymisert nettverk av hvem som snakker med hvem er vanskelig å gjøre trygt. Det bør være N0 først.

**Andre informasjonssystem-tema.** Onboarding-trakt (fra invitasjon til første melding), hvilke flater som brukes, og samtykkeatferd: hvor mange svarer ja, ikke nå eller aldri på en forespørsel, og hva i forespørselen påvirker det. Det siste er forskning på HAVEN selv og får data fra N1 på forespørslene.

## 5. Funn i koden

| # | Funn | Kilde | Betydning |
|---|---|---|---|
| 1 | Adminens resolverstatistikk er ikke anonym. Den lister `identityNamedCells` med identitets-uuid som nøkkel og hvilke celler hver identitet har | `CellScaffold/Sources/ScaffoldKit/AdminMetricsSupport.swift:138–197` | Adminens visning kan ikke gis videre. Det trengs en egen projeksjon som bare gir tellinger |
| 2 | Adminflatene krever en rolle som `ProvedClaimCondition` med `AdminRoleCredential` | `AdminMetricsSupport.swift:1331–1339` | En forskerrolle kan bygges likt, uten ny tilgangsmekanisme |
| 3 | I spørreskjemaet endrer `aggregateOnly` og `pseudonymized` bare en tekst. Innsikt og eksport har alltid `recipientID` og `displayName`, og det finnes ingen minste gruppestørrelse | `QuestionnaireCampaignCell.swift:1405–1409` (tekst), `:1164–1176` (rader), `:3630` (CSV-kolonner) | Løftet til respondenten holdes ikke av koden. Må rettes før spørreskjema brukes til forskning |
| 4 | Ingen kode for k-anonymitet, støy (differensielt personvern) eller sikker summering | Søk i CellScaffold og CellProtocol: 0 treff (bare `epsilon` i rutevalg, `ExplorationPolicy.swift`) | Samsvarer med `IMPLEMENTERT_OG_VISJON.md` |
| 5 | `ownerApprovalRequired` avviser bare; det finnes ingen generell innboks der eieren godkjenner en ventende forespørsel | `CellProtocol/Sources/CellBase/Cells/GeneralCell/GeneralCell.swift:1657` | «Spør entiteten» bør bruke mønsteret fra `ChatCell`: signert artefakt + signert aksept + `LookupCondition target.*` med `automaticWhenConditionsMet`. Det er det `PDD_dele-dokumenter` skal gjøre gjenbrukbart (InvitationAdmission) |
| 6 | Diagrammer i web og Binding er én serie (søyle eller linje) av `{label, value}`. Et punkt uten tall forsvinner, og linjen trekkes forbi hullet | Web: `CellScaffold/Public/js/skeleton-runtime.js:3504–3523`. Binding: `CellProtocol/Sources/CellApple/.../SkeletonView.swift:2303–2331` | Et skjult tall må vises som skjult i begge, ellers villeder grafen |
| 7 | PyResearchScaffold har datasett, regresjon, figurer, kjørelogg og CellBridge med Agreement, men datasettkontrakten krever enhetene `x_V` og `y_mV` | `/Users/kjetil/Build/Digipomps/HAVEN/PyResearchScaffold/contracts/dataset-v1.json` | God analyseside å koble til, men trenger en generell datasettkontrakt |
| 8 | `AccessRequirementPromptCell` har et utkast til tilgangsforespørsel (mål, keypath, rettighet, formål, varighet), men bare som demo | `CellScaffold/Sources/App/Cells/AccessRequirementPrompt/AccessRequirementPromptCell.swift:20–60` | Feltene kan gjenbrukes i forespørselsbyggeren |
| 9 | Studentveiledningen sier at staging ikke skal ha ekte persondata om andre | `/mnt/project-files/masterhaven26/KOM_I_GANG.md` | N2–N4 med ekte deltakere kan ikke skje på staging slik regelen står (§6 spørsmål 1) |

## 6. Personvern: trusler og tiltak

| Trussel | Eksempel | Tiltak i planen |
|---|---|---|
| Små tall | «1 identitet brukte Dokumenter i uke 46» peker ut en person på en liten node | Minste gruppestørrelse k (forslag 5); skjult verdi vises som «færre enn 5» |
| Differanse | Tall for dag 1–7 og dag 1–8 gir dag 8 alene | Bare faste, ikke-overlappende bøtter (kalenderdag, uke). Ingen frie tidsvinduer |
| Fri spørring | En spørring som filtrerer til én person | Bare spørringsmaler fra katalogen, med versjon. Ny mal krever gjennomgang |
| Studenten eier samlecellen | Eieren av en celle kan lese alt i den, også enkeltbidrag | Bidragene samles i en celle som eies av noden, ikke av studenten. Forespørselskortet sier det rett ut. Sikker summering, der heller ikke noden ser bidragene, er et forskningsspørsmål for fase 3 |
| Kobling | Pseudonym som går igjen på tvers av forespørsler | Nytt pseudonym per forespørsel |
| Gjentatte utleveringer | Mange små utleveringer som til sammen avslører | Logg over hver utlevering (hvem, mal, bøtte, k, hash). Støy med budsjett i fase 3 |
| Trukket samtykke | Tall er alt lagt sammen | Kortet sier før ja hva som skjer: nye utregninger tar deg ikke med; lagrede summer blir stående |

## 7. Etikk og regelverk

Dette er hentet fra hukommelsen og må sjekkes med UiO før noen samler inn ekte data: et masterprosjekt som behandler personopplysninger skal normalt meldes til Sikt, og UiO har egne rutiner for samtykke og lagring. HAVEN kan gjøre samtykket presist og etterprøvbart, men erstatter ikke den vurderingen. Det trygge løpet for studentene er N0 og N1 først, og N2–N4 med ekte personer først når prosjektet er godkjent ved UiO.

## 8. Visningskomponenter

Finnes i både web og Binding: `table`, `chart` (søyle, linje, én serie), `network`, `map`, `calendar`. Bare web: `timeline`, `purposetree`. Bare Binding: `radar`.

Trengs, og må virke i både web og Binding:
- **Tall-flis** med skjult-markering og en linje om opphav («uke 46 · k=5 · 23 identiteter»). Kan settes sammen av vanlige elementer.
- **Søyle og linje med skjulte bøtter**: endring i begge renderere, slik at `{value: null, suppressed: true}` tegnes som et merket hull.
- **Fordeling (histogram)**: søylediagram med bøtter, ingen ny type.
- **Samtykketrakt**: sendt, sett, ja, ikke nå, aldri, trukket. Søylediagram eller tabell.
- **Opphavskort**: kilde, tidsvindu, k, antall, malversjon, hash. Vanlige elementer.
- **Flere serier i samme graf** (fase 2): ny evne i begge renderere.

## 9. Eget dashbord som onboarding

Forslag til første oppgave for en ny student, etter at invitasjon og chat virker:

1. Godta invitasjonen til forskerrollen (fra Kjetil eller veileder). Det er en Agreement, og studenten ser vilkårene.
2. Åpne malen «Mitt forskningsdashbord» i Studio som eget utkast.
3. Legg til ett tall fra katalogen, for hånd eller med utkasthjelpen fra `PDD_studentflater`.
4. Sjekk utkastet (nåbarhet i Studio eller `skeleton-check`).
5. Lagre, og åpne dashbordet både på web og i HAVEN-appen.
6. Del det med veilederen (lesing via Agreement).
7. Valgfritt: send en testforespørsel til en medstudent og se trakten endre seg.

Målet er at en ny studentkonto kommer gjennom trinn 1–6 uten hjelp på under 45 minutter. Det måles med en ekte testkonto.

## 10. Nytt forskningstema?

Holdes åpent, som du ba om. Jeg ser to muligheter uten å anbefale noen: verktøyene kan være infrastruktur for begge temaene, eller et delspørsmål i tema B («hvilken personvern/nytte-balanse gir N1–N3, målt på ekte bruk»). Sikker summering uten betrodd node er et selvstendig forskningsspørsmål som passer begge.
