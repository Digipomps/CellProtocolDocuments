# d168b — Biblioteket og brukerens egne varianter

Til G1 · 07.10.2026 · Ingen implementering er gjort i denne oppgaven.

## Først: svar på Kjetils antakelse

**Antakelsen stemmer delvis. Private utkast kan allerede lagres og hentes. Det finnes også oppslag av endret konfigurasjon fra kildecellen. Men bibliotekets bootstrap slår ikke opp brukerens private Studio-varianter, og den undersøkte koden viser ingen ferdig kobling «min variant stammer fra denne innebygde».**

Alle CellScaffold-henvisninger nedenfor gjelder git-objektet `381094bbb18e390bd8fd2b8955524b5fa3e4f9ea` (`381094bb`), lest med `git show`/`git grep`, ikke arbeidskopiens nyere HEAD. Stier er fra HAVEN-roten; linjetall gjelder den angitte revisjonen. CellProtocol ble lest i arbeidskopien med HEAD `253b4afe11af8b58bfcc433d9b7dc7393c761e24`; dette er ikke verifisert som staging sin avhengighetsrevisjon. Leseren er Codex i denne økten. Henvisningene angir konkret leste utsnitt, ikke at hele repoene er lest. Ingen kjørende tjeneste er målt og ingen tester er kjørt.

### 1. Egne konfigurasjoner: hva finnes?

| Kilde, fil og linje | Det koden viser | Det den ikke beviser |
|---|---|---|
| `CellScaffold/Sources/App/Cells/CellConfigurationStudio/CellConfigurationStudioCell.swift:457–473, 483–506, 550–587` | Import og lagring sender selve CellConfiguration til DraftVersion gjennom `draft.create` og `draft.commit`. Dette er private, requester-bundne versjoner. | At et lagret utkast automatisk blir en bibliotekoppføring. |
| Samme fil `:509–540, 590–633` | `version.get` gjenoppretter en versjon; `version.list` henter historikken. `subjectRef` er `cell-configuration://<configuration.uuid>`. | En særskilt relasjon til en annen konfigurasjon som original. `parentVersion` er versjonshistorikk, ikke bevis for opphav i en innebygd flate. |
| Samme fil `:301–313, 347–354` | Studio gir privat preview uten automatiske writes. Valglisten er innebygde konfigurasjoner med requester-bundet overlay. | At preview gir rettigheter til cellene konfigurasjonen refererer til. |
| `CellScaffold/playwright/cellconfiguration-studio-upload.smoke.spec.js:10–60` | Testen beskriver innlogget import, preview-tekst og at utkastnavnet overlever en side-reload. | At testen er grønn nå; varig lagring etter serverstart; synlighet i biblioteket; isolasjon mellom to brukere. Dette er lest testkode. |
| `CellScaffold/Sources/App/Cells/PersonalCopilot/PersonalCopilotConfigurationFactory.swift:676–694` og `CellScaffold/Sources/App/Cells/PersonalCopilot/PersonalCopilotCells.swift:1956–1987` | «Personal Co-Pilot Catalog» / `personalCatalog` returnerer godkjente factory-konfigurasjoner i personal-copilot-v1. `entries.unavailable` er en tom liste. | Navnet «Personal» betyr ikke at katalogen søker i brukerens egne utkast. Her er den en produktkatalog, ikke et variantlager. |
| `CellScaffold/Sources/App/Cells/ConfigurationCatalog/ConfigurationCatalogCell.swift:27–37, 351–367, 435–442, 492–507` | Katalogoppføringer inneholder `purpose`, `goal` og `configuration`, og oppføringene encode/decode-lagres. Lesing kan bruke overlay. | Å legge til/redigere/oppdatere gjennom de gamle kataloghandlingene virker ikke som variantflyt: handlingene svarer `deprecated: edit owning cell configuration instead`. |
| `CellScaffold/Sources/App/Services/EditableCellConfigurationSupport.swift:843–875, 890–899, 925–953, 968–1015` | Overlay henter editable state eller Library-konfigurasjon fra kildecellen med requester, og kan bruke en lagret override. Apply skriver til kildecellen. Matching bruker blant annet navn, UUID eller skeleton-signatur. | Et generelt søk i private Studio-versjoner eller en eksplisitt bruker→variant→innebygd-relasjon. Om kildecellen er personlig eller delt må avgjøres for hver konkret celle. |
| `CellScaffold/Sources/App/Cells/ConfigurationCatalog/BuiltInConfigurationIdentity.swift:6–16, 122` | Kjente innebygde får stabil UUID ved oppslag i en fast mapping med endpoint + navn som nøkkel; ukjente varianter beholder sin identitet. | Brukereierskap, opphavsrelasjon eller at to konfigurasjoner med samme navn er samme variant. |

Selve DraftVersion lagrer payload i Codable-records og encode/decode av draft-/versjonskart: `CellScaffold/Sources/App/Cells/ProjectOperations/DraftVersionCell.swift:19–41, 66–94`. Dette viser en lagringsrepresentasjon, ikke en måling av restart eller isolasjon i staging.

**Svaret er derfor ikke «ingenting finnes».** Studio/DraftVersion og kildecelle-overlay er eksisterende byggeklosser. Den fullstendige personlige bibliotekflyten i denne oppgaven er ikke vist av dem.

### 2. Hvorfor kommer eier-flatene med i biblioteket?

Bootstrap setter `availableConfigurations` fra en funksjon uten requester: `CellScaffold/Sources/App/Controllers/PortholeWebSessionSupport.swift:1159–1160, 1218, 1233`. Funksjonen tar default-katalogen og filtrerer den med `portholePublishedConfigurations`: samme fil `:2901–2925`. Den slår ikke opp Studio-versjoner i denne kjeden.

Default betyr her innebygde factory-konfigurasjoner: `CellScaffold/Sources/App/Cells/ConfigurationCatalog/ConfigurationCatalogCell.swift:2753–2771`. Porthole-filteret sjekker renderbart innhold, noen routingregler og tillatte endpoints; det fjerner duplikater og sorterer. Det spør ikke om requester, eierbevis eller brukerrolle: samme fil `:2783–2799, 2902–2939`.

De tre Prompt Admin-variantene opprettes i default-katalogen på `:1618–1635` og katalogiseres på `:2398–2424`. Project Operations opprettes på `:1651` og katalogiseres på `:2542–2544`. Endepunktene RAGPromptAdmin og ServiceCatalog er i tillatelseslisten på `:259, 267`. **Dette er den kodebaserte forklaringen på at også en vanlig requester kan få disse oppføringene.** At kjetil2 faktisk fikk akkurat denne bootstrapen i staging, og den eksakte årsaken til hver HTTP 422, vet jeg ikke uten respons/logg fra det løpet.

Det finnes filtre, men de må holdes fra hverandre:

- Den requester-bundne kataloglesingen bruker `accessibleEntries`, men eierflatene testes ikke der. `isCatalogEntryAccessible` gir `true` dersom oppføringen ikke omfattes av særkravene for remote event-konfigurasjoner: `CellScaffold/Sources/App/Cells/ConfigurationCatalog/ConfigurationCatalogCell.swift:645–674`.
- Den separate offentlig lesbare katalogen bruker et strengere filter, som utelater blant annet admin, RAGPromptAdmin og ServiceCatalog: samme fil `:2801–2841, 2844–2873`. `CellScaffold/Sources/App/Cells/ConfigurationCatalog/PublishedConfigurationCatalogCell.swift:73–90` bruker dette. Bootstrap-kjeden over bruker det ikke. «Publisert» i bootstrapens funksjonsnavn betyr dermed ikke «denne brukeren får åpnet alt».
- Rettigheter håndheves senere av cellene. RAGPromptAdmin krever signerende eier ved runtime-binding: `CellScaffold/Sources/App/Cells/RAG/RAGPromptAdminCell.swift:61–70`. Project Operations har flere referanser, blant annet RAGCatalogIngestion og RAGIngestMedia: `CellScaffold/Sources/App/Cells/ProjectOperations/ProjectOperationsConfigurationFactory.swift:20–48`. Disse kan kaste `ownerProofRequired`: `CellScaffold/Sources/App/Cells/RAG/RAGCatalogIngestionCell.swift:71` og `CellScaffold/Sources/App/Cells/RAG/RAGIngestMediaCell.swift:67`. Det er ikke grunnlag for å si at ServiceCatalog alene forklarer hele feilkjeden.

### 3. Formål med relasjon til en lokal CellConfiguration

**Ja, en formålsmodell finnes allerede. Nei, dette beviser ikke en ferdig personlig bibliotekflyt.**

- `CellProtocol/Sources/CellBase/PurposeAndInterest/Purpose.swift:13–23, 40–75` har `goal: CellConfiguration?`, `helperCells: [CellConfiguration]` og relasjoner til andre formål/entiteter. Feltene kan dekodes. `goal` er her en konfigurasjon som beskriver målet; det er ikke automatisk en «stammer fra»-relasjon.
- `CellProtocol/Sources/CellBase/PurposeAndInterest/PerspectiveNode.swift:13–22, 41–58` har relasjonstyper som parts, partOf, purposes og entities. `CellProtocol/Sources/CellBase/PurposeAndInterest/EntityRepresentation.swift:61–111` knytter entitetsrepresentasjoner til formål og eierens kunnskap. `CellProtocol/Sources/CellBase/ValueTypes/Types/Object.swift:7` definerer Entity som Object.
- `CellProtocol/Sources/CellBase/PersistingCells/EntityRelationRecordV1.swift:270–321` har entitetsreferanser, `purposeRefs` og en entitetsrepresentasjon; den undersøkte posttypen er for relasjoner til personer/organisasjoner, ikke et ferdig variantregister. `CellProtocol/Sources/CellBase/PersistingCells/EntityAnchorPersistence.swift:6–28` gir lagringsbinding/kryptering for sidefiler, ikke selve variantkontrakten.
- `CellProtocolDocuments/Book/haven_purpose_packages_v0.json:2–14, 30–38` beskriver formålspakker med mål, tester og artefakter. Dette er utviklingsmetodens JSON, ikke runtime-lagring av brukerens bibliotek. Pakkene gir uttrykkelig ingen rettigheter.
- CellScaffold bruker `purpose://` blant annet som katalogkrav (`CellScaffold/Sources/App/Cells/ConfigurationCatalog/ConfigurationCatalogCell.swift:129–142, 149–180`). En slik streng alene etablerer ikke en lagret relasjon.
- Den aktuelle bibliotekoppsett-cellen oppgir at formål ikke kan lagres eller aktiveres der ennå, og avviser preview til en CP-grafadapter finnes: `CellScaffold/Sources/App/Cells/EntityPurposeLibrarySetup/EntityPurposeLibrarySetupCell.swift:7–9, 39–48, 74–101`. Den eldre flate kontrakten er eksplisitt pensjonert: `CellScaffold/Sources/App/Support/EntityPurposeLibrarySetupContract.swift:14–28`.

**Vet ikke:** om en annen, ikke undersøkt runtime-flyt allerede persisterer akkurat bruker→formål→variant→innebygd som Kjetil ønsker. Ingen slik ferdig flyt er påvist i de undersøkte kildeveiene. Hele Entity-/relasjonssystemet og staging sitt lagringsinnhold er ikke gjennomgått.

## 0. Intensjon og kontroll av antakelser

Spørsmål (ordrett): skal Doc Prompt Admin, Innorag Prompt Admin, RAG Prompt Admin og Project Operations (de krever at eieren signerer) ligge i biblioteket for en vanlig innlogget bruker i staging?

Kjetils svar 07.10 (ordrett):

> Nei, flatene skal bare ligge hos bruker om brukeren har laget egne varianter. (Her regner jeg med at du ikke har implementert at man slår opp i egne cellconfigurations om man har en personlig endring. Kanskje lagre det i formål med relasjon til lokal CellConfiguration?)

Oppdragets ramme: lesejobb og formålsspesifikasjon fram til G1. Bare denne filen og STATUS.md; ingen kode, commit, push eller køjobb. De ønskede bibliotekreglene nedenfor er framtidige mål, ikke implementert atferd.

| Antakelse | Audit-status | Grunnlag |
|---|---|---|
| Egne konfigurasjoner kan ikke lagres | contradicted | Studio har privat versjonslagring; se svar 1. |
| Bibliotekets bootstrap finner ikke private Studio-varianter | retrieved | Kjeden på PortholeWebSessionSupport.swift:2901–2925 bruker statiske defaults. |
| Ingen formålsmodell knytter til CellConfiguration | contradicted | Purpose.goal/helperCells finnes; se svar 3. |
| Alle fire får 422 for kjetil2 nå | unavailable | Oppgitt i oppdraget; ikke målt her. Eierkrav er lest, konkret feilårsak vet ikke. |
| En variant er automatisk åpnbar fordi brukeren eier JSON-en | contradicted | Preview gir ikke cellegrants; runtime krever egne rettigheter. |

### To lagringsalternativer — Kjetil velger

Begge alternativene skal oppfylle samme mål: brukereid konfigurasjon, entydig opphav i en lokal innebygd, varig gjenfinning og ingen tilgang til originalens private data uten rettighet.

| Valg | Hva det betyr | Taler for | Taler imot / mangler |
|---|---|---|---|
| A: formål med relasjon | Brukerens formål peker på egen CellConfiguration og på den innebygde den stammer fra. | Følger Kjetils forslag; Purpose har allerede konfigurasjoner og grafrelasjoner; brukerens grunn til varianten kan følge den. | Ingen ferdig lagrings-/bibliotekadapter påvist. Opphavsrelasjon, eierskap og betydningen av goal/helperCells må avklares. Den pensjonerte flate kontrakten kan ikke tas som implementert løsning. |
| B: videreføre Studio/DraftVersion og kildecelle-overlay | Private konfigurasjoner versjoneres med eksisterende lagringsvei; biblioteket gjenfinner dem. En eksplisitt kobling til originalen må føyes til, og kildecelle-overlay brukes der kildecellen faktisk er brukerens. | Privat import, payload-lagring, historikk, gjenoppretting og preview finnes i kode. Mindre ny lagringsmekanikk. | Dagens subjectRef beskriver konfigurasjonen selv, ikke dens originale innebygde. Automatisk bibliotekoppslag mangler i bootstrap. Apply til en delt kildecelle er ikke det samme som en privat variant; det kan ikke brukes som privat lagring uten verifisert eierskille. |

Ingen av alternativene er valgt. En formålsrelasjon gir ingen autorisasjon. En kopi av en admin-konfigurasjon gir heller ingen autorisasjon. Med «lokal innebygd» menes her en innebygd konfigurasjon i scaffolden; om Kjetil mener på brukerens enhet, er åpent spørsmål 1 også en avklaring av dette.

## 1. Formålstre med observerbare mål

Eksisterende forelder: `purpose://gui.quality.functional-accessible` (Book 23). Tilgangsgrense: `purpose://access.audit.privacy`. `purpose://skeleton.owner-entity-access` er en eksisterende draft-node, ikke bevis for implementering. Nye blad er task-lokale kandidater, ikke endringer i den kanoniske formålsboka.

```text
Brukeren finner sine flater og får åpnet dem
├── F1: Vis de innebygde flatene denne brukeren kan åpne
├── F2: Vis eier-originaler bare for eieren
├── F3: Finn igjen brukerens egne varianter og deres opphav
└── F4: Vis ingen utilgjengelig flate som åpnbar
```

| Blad / purposeRef | Forelder | Goal: utfall og suksessignaler | Verifier |
|---|---|---|---|
| F1 `purpose://candidate.bibliotek-egne-varianter.innebygde` | `purpose://gui.quality.functional-accessible` | Ved innlogging består bibliotekets innebygde, åpnbare oppføringer av flater brukeren har tilgang til og som laster nødvendig innhold. På et avtalt sett skal alle slike flater vises, uten duplikater. | T1: sammenlign bibliotekrespons og faktisk åpning for eier og to vanlige brukere. |
| F2 `purpose://candidate.bibliotek-egne-varianter.eierflater` | `purpose://access.audit.privacy` | De fire originale eierflatene vises for eieren dersom de kan åpnes; de vises ikke som originaler hos vanlig bruker. Når bruker A har laget egen variant, er det A sin variant som blir tilgjengelig hos A, ikke originalen eller A sin variant hos B. | T2: samme fire flater, eier/A/B, før og etter variant. |
| F3 `purpose://candidate.bibliotek-egne-varianter.egne-varianter` | `purpose://gui.quality.functional-accessible` | Egen variant er en brukereid CellConfiguration med egen entydig identitet og eksplisitt opphavsrelasjon til lokal innebygd identitet. Den kan finnes igjen etter ny innlogging og serverstart; originalen og andre brukeres varianter er uendret. Lagring A eller B velges av Kjetil. | T3: lagre, gjenfinn og kontroller eierskap, opphavsrelasjon og uendret original. |
| F4 `purpose://candidate.bibliotek-egne-varianter.aerlig-aapning` | `purpose://gui.quality.functional-accessible` | En kjent utilgjengelig flate tilbys ikke som åpnbar. Manglende eierbevis/grants, ugyldig konfigurasjon og svikt i nødvendige referanser gir ingen falsk Åpne-handling. Dersom tilgang bortfaller etter listevisning, forklares det forståelig ved klikk. | T4: feiltilstander før listevisning og tilgangstap etterpå. |

Alle fire er foreslåtte mål. Produktregelen er «kan åpnes», ikke bare «har et skeleton». Eierstatus alene er heller ikke bevis for at alle referanser virker. Egen variant kan vises som brukerens lagrede innhold selv om den ikke kan åpnes, men da uten en aktiv Åpne-handling; om slike oppføringer skal skjules helt, avgjøres i spørsmål 4.

## 2. Avgrensning og avhengigheter

Denne leveransen er bare kildegrunnlag og G1-spesifikasjon. Den endrer ikke bibliotek, roller, grants, celler eller lagring. Den reparerer ikke staging. Ingen plan for implementering er laget. Det er ingen publisering til Formålstrær-verktøyet; treet over ligger i denne filen etter oppdragets regel om bare to filer.

| Avhengighet før framtidige produktmål kan verifiseres | Kilde / avgrensning | Verifier nå / før gjennomføring |
|---|---|---|
| Bibliotekresponsen for eier, kjetil2 og en annen vanlig bruker | Bootstrap-kjeden i svar 2. Personlig oppslag må skilles fra statisk liste. | Kode lest; **ikke målt** i staging. Før gjennomføring må faktiske liste- og åpneresponser registreres, inkludert serverens feilspor for de fire. |
| Gyldig eierbevis og tilstrekkelige rettigheter for alle nødvendige referanser | RAGPromptAdmin og Project Operations-referansene i svar 2. | Kode lest; **ikke målt**. Eieren må også prøves; en rollebetegnelse er ikke et rettighetsbevis. |
| Privat lagring og requester-isolasjon | Studio/DraftVersion i svar 1. | **Ikke målt**: lagre/gjenfinn med to adskilte identiteter, etter serverstart. Lest reload-test dekker mindre. |
| Stabil originalidentitet og eksplisitt variantopphav | BuiltInConfigurationIdentity i svar 1. | Stabil UUID er lest; **ikke målt**. Ingen ferdig opphavsrelasjon påvist. Kontroller variant med samme navn som original og variant med nytt navn. |
| Lagringsvei A eller B | Alternativtabellen; tilgjengelighetscellen i svar 3. | Valg mangler. A krever vist grafadapter; B krever vist opphavsrelasjon og bibliotekoppslag. |
| Hvordan biblioteket ser ut i viktige tilstander | Ingen bilder er laget i denne lesejobben. | Før visuelt arbeid/implementering trengs G1-GUI med rendret bilde og avtalt opptaksvei. `images/` er bare framtidig artefakt, ikke levert. |

Rekkevidden er ikke målt: vi kjenner ikke antall reelt åpnbare flater per bruker i staging. Koden viser listeutvelgelsen, ikke en sertifisering av at listen virker.

## 3. Forventningskontrakt — det du får nå

Stiene i tabellen er relative til denne oppgavemappen.

| Leveranse | Type | Hvor | Hva Kjetil kan vurdere | Godkjent |
|---|---|---|---|---|
| Kildesvar, to lagringsvalg og formålstre | Fil | `FORMAALSSPEC.md` | Om reglene og målene uttrykker ønsket bibliotek | Nei, G1 venter |
| Tydelig stopp ved G1 | Fil | `STATUS.md` | Hva som er lest, ikke målt og fortsatt uavklart | Nei |

En framtidig kjørende flate eller et bilde er ikke levert her. G1 godkjenner ønsket atferd, ikke en ferdig løsning, et lagringsvalg som ikke er besvart, eller en implementeringsplan.

## 4. Formålspakker og lærdommer

`purpose_dev.py lookup --tags library configuration access --surfaces web cell` ble kjørt før formålstreet ble skrevet. `new` ble også kjørt. De automatisk festede pakkene og testene er bevart nedenfor. Standard kvalitet, GUI, cellekontrakt og cellekombinasjon gjelder framtidig gjennomføring; bygge-/GUI-/runtime-tester er ikke relevante å kjøre for denne avgrensede dokumentleveransen. Ingen pakke gir rett til å gå videre fra G1.

Særlig relevante lærdommer, med deres forebygging:

- `lesson.purpose-never-grants-rights`: «Et formål kan innsnevre en rettighet, aldri opprette, utvide eller arve en». F2/F4 og T2/T4 skal holde denne grensen.
- `lesson.planned-documented-as-implemented`: planlagt oppførsel må merkes som planlagt. Alle produktmål her er foreslått; kildesvar står separat.
- `lesson.bridge-inferred-architecture-from-one-use`: kapabiliteter trenger egen kilde og avgrensning. §2 skiller datamodell, lagring, bibliotek og åpning.
- `lesson.text-ux-is-not-design`: rendret bilde godkjennes før implementering. Denne lesejobben avsluttes ved G1; G1-GUI er ikke godkjent.
- `lesson.surface-load-alias-miss`: mål faktisk lasting og les feilspor. Oppføringen og dens klikk må verifiseres sammen, ikke bare HTTP-status eller tilstedeværelse i listen.
- `lesson.plan-instead-of-delivery`: G1 godkjenner formål, ikke arbeid. Leveransen nå er de to bestilte filene, ikke en påstått bibliotekrettelse.

<details>
<summary>Fullt automatisk oppslag: pakker og lærdommer (bevart fra verktøyet)</summary>

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
- **lesson.picker-state-keypath-is-read-and-written** (2026-09-24, minor): Velgeren «Verktøy» i «Gi tilgang» sto på «Velg verktøy» selv om cellen hadde valgt verktøyet.
    - forebygging: `selectionStateKeypath` skal være en nøkkel cellen både leser (`{selected}`) og skriver; test rundturen (`pickerSelectionRoundTrips`).
- **lesson.pairing-can-outlive-the-identity** (2026-09-24, major): Agenten var paret med en HAVEN-identitet fra 4. mai («Binding Local Session», nøkkel 13BF…), mens HAVEN brukte en annen privat identitet (D362…, identitetsfilen skrevet 18.09). Svar fra HAVEN ville blitt avvist; ingen test i noen av endene kunne se det.
    - forebygging: En flate som ber eieren signere for agenten sammenligner egen nøkkel med agentens forankring og viser forskjellen før signering, med vei til ny paring (test: `offerIsRefusedHereWhenThisHavenHoldsAnotherKey`, `theOwnerNeverSignsWhatFailedTheCheck`). Sjekk nøkkelkontinuitet før live-test av noe som signeres.
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
- **lesson.corr-grant-expired-without-renewal-path** (2026-09-30, major): 30.09 fikk Vegar `recipient_not_allowed` da han sendte til `kjetil-vegar-codex-d`, Kjetils klient avviste sitt eget bevis, og meldingen til Victoria ble avvist på samme måte; korrespondansen sto stille i over ett døgn.
    - forebygging: En tilgang eller et bevis med utløpstid tas ikke i bruk før fornyelsesveien er testet ende til ende (utløpt tilgang → fersk invitasjon → eiergodkjenning → ny frist → sending virker), og fristen står i pilotens STATUS med en påminnelse minst sju dager før.
- **lesson.renewal-invite-must-carry-device-id** (2026-09-30, major): Gjennomgangen av korrespondanseklienten 30.09 viste at `setup` gjenbruker `identity.json`, men tar enhets-ID-en fra invitasjonen (`invite.deviceID ?? tilfeldig`); en fornyelsesinvitasjon uten profilens `deviceID` ville gitt ny enhet og `principal_already_enrolled` i stedet for fornyelse.
    - forebygging: En fornyelsesinvitasjon lages bare med `deviceID` hentet fra deltakergrafen eller profilen (`haven-correspondence-mcp identity`), og generatoren nekter uten; test: fornyelsesinvitasjonens `deviceID` er lik profilens, og `setup` gir `pending_approval` med `renewsGrantID`.
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
- **lesson.approved-image-had-no-way-to-be-photographed-on-the-live-page** (2026-10-06, minor): Telefonbildet som ble godkjent ved G1-GUI, kunne ikke få et skjermbilde fra nett ved siden av seg ved G3: nettleserverktøyet holder vinduet på 1280 punkter, og siden nekter å bli vist i en ramme.
    - forebygging: Ved G1-GUI står det for hvert bilde hvordan motstykket på nett skal tas ved G3, og veien er prøvd én gang mot siden slik den står. Kan et bilde ikke tas, sies det ved G1-GUI. Test: hvert godkjent bilde har en navngitt opptaksvei som har gitt en fil.
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

## Book 23-noder som kan være forelder/gjenbruk (leksikalsk forslag, verifiser)
- purpose://gui.quality.functional-accessible [active] — Functional accessible GUI
- purpose://skeleton.owner-entity-access [draft] — Owner entity access affordance
- purpose://governance [active] — Governance
- purpose://access.audit.privacy [active] — Access, audit and privacy


</details>

## 5. Avledede tester — foreslått, ikke kjørt

Evidensstiene nedenfor gjelder framtidig gjennomføring etter godkjenning. Disse filene er ikke opprettet i lesejobben.

| testRef | Formål | Hvordan | Evidens | Status |
|---|---|---|---|---|
| T1 | F1 | Inspection + measurement: frys forventet sett av tilgjengelige innebygde for eier/A/B; sammenlign både bootstrap og bibliotekvisning; åpne hver oppføring og sjekk nødvendig innhold. Registrer også tilgjengelige flater som mangler i listen. | `TESTRESULT.md#bibliotek` | venter |
| T2 | F2 | Measurement: de fire originalene er fraværende hos A/B; åpnes hos eier dersom alle krav er oppfylt. Lag en variant hos A: A ser egen variant, B ser den ikke; verken kopi eller formålsrelasjon gir tilgang til originalens admin-data. | `TESTRESULT.md#eierflater` | venter |
| T3 | F3 | Measurement: lagre to navnelike varianter av samme original med adskilte identiteter; hent etter logout/login og serverstart. Inspiser bruker-eierskap, egen variantidentitet, eksplisitt originalreferanse og originalrevisjon. Kontroller originalen uendret. Flere varianter testes hvis Kjetil velger det. | `TESTRESULT.md#varianter` | venter |
| T4 | F4 | Measurement: manglende grant, eierbevis, nødvendige referanser og ugyldig konfigurasjon før listevisning gir ingen aktiv Åpne-handling. Fjern tilgang etter at listen er vist: klikk gir forståelig melding og ingen data fra uautorisert kilde. | `TESTRESULT.md#aapning` | venter |

<details>
<summary>Automatisk avledede pakketester — alle venter på eventuell gjennomføring</summary>

### Automatisk testgrunnlag — Avledede tester (samlet)

| testRef | Formål | Hvordan | Evidens | Status |
|---|---|---|---|---|
| test.build | purpose://quality.build-and-regression | Prosjektets byggkommando (xcodebuild / swift build / pytest) — angis i PLAN.md. | TESTRESULT.md#build | venter |
| test.regression | purpose://quality.build-and-regression | Prosjektets testkommando; sammenlign antall tester før/etter. | TESTRESULT.md#regression | venter |
| test.docs-updated | purpose://quality.docs-in-same-change | Les diff; kryss av i ACCEPT.md. | ACCEPT.md#docs | venter |
| test.status-current | purpose://quality.work-is-visible | Sammenlign STATUS.md med filene i mappen. | ACCEPT.md#status | venter |
| test.gui.reference-image-exists | purpose://gui.expectation-agreed-before-build | purpose_dev.py validate sjekker images/ mot FORMAALSSPEC.md §3. | images/ | venter |
| test.gui.parity | purpose://gui.parity-with-approved-image | Screenshot fra Porthole/Binding i samme viewport som referansen; lim inn i ACCEPT.md. | ACCEPT.md#parity | venter |
| test.gui.load-time | purpose://gui.surface-loads-in-time | Stoppeklokke/logg-tidsstempel; noter alle tre tider. | TESTRESULT.md#load-time | venter |
| test.skeleton.no-unreachable-elements | purpose://gui.ways-in-are-reachable | xcodebuild -only-testing:BindingTests/CellConfigurationVerifierXCTest/testNoLocalSurfaceHidesItsOwnWaysIn | TESTRESULT.md#reachability | venter |
| test.skeleton.purpose-actions-reachable | purpose://gui.ways-in-are-reachable | Sammenlign §3-radene mot SkeletonReachabilityAudit.reachableActionKeypaths(skeleton). | ACCEPT.md#ways-in | venter |
| test.cell.contract-fixtures | purpose://cell.contract-explicit | python3 checks/validate_contract.py | TESTRESULT.md#contract | venter |
| test.cell.auth-negative | purpose://cell.authorization-honours-keypath | Tre enhetstester navngitt etter tilfellet. | TESTRESULT.md#auth | venter |
| test.cell.stub-scan | purpose://cell.no-empty-stubs | Søk i berørte filer; skriv listen i ACCEPT.md. | ACCEPT.md#stubs | venter |
| test.cells.dataflow-matches-contracts | purpose://cells.dataflow-declared | Tabell kant→kontrakt i PLAN.md. | PLAN.md#dataflow | venter |
| test.cells.capability-audit | purpose://cells.capabilities-declared-with-boundary | Tabell i FORMAALSSPEC.md §0. | FORMAALSSPEC.md#audit | venter |


</details>

Verktøykontroll av dokumentleveransen: `purpose_dev.py validate` fant fem feil i det felles lærdomsregisteret og 18 felles composition-advarsler; ingen oppgavemappefeil ble meldt. Valideringen samlet er ikke grønn. `purpose_dev.py gates` viser at G1-artefakten finnes og alle porter venter. Se STATUS.md for de konkrete feilene.

## 7. Revisjonslogg

| Iterasjon | Dato | Endring | Leser/skriver |
|---|---|---|---|
| 1 | 2026-10-07 | Kildesvar på angitt CellScaffold-revisjon, formålstre og to uvalgte lagringsalternativer. Ingen G1 satt. | Codex |

Selektiv uavhengig lesekontroll: Codex-undertråden `g1_kildesjekk` kontrollerte hovedpåstandene om bootstrap/filter, Studio, personalCatalog, overlay, Purpose og bibliotekadapteren. Ingen blokkende faktafeil funnet. Ikke kontrollert: alle øvrige henvisninger, hele Entity-systemet eller staging. Siste presisering om fast UUID-mapping og tillegg om DraftVersion/validering er ikke kontrollert på nytt av undertråden.

Læringsfangst: funnene er bevart i dette bestilte dokumentet. Den vanlige `haven_learn.py`-fangsten/synkroniseringen er ikke kjørt: den ville skrive andre filer, mot oppdragets uttrykkelige tofilersgrense. Dette er et avvik fra normal øktavslutning, ikke en påstand om at funnene er distribuert til skills.

## 6. Åpne spørsmål til Kjetil

1. **Hvor skal varianten høre hjemme?** A: brukerens formål med relasjon til egen og lokal innebygd konfigurasjon. B: eksisterende Studio/DraftVersion-lagring med eksplisitt opphavsrelasjon og bibliotekoppslag. Begge har mangler som tabellen viser. Betyr «lokal» i scaffolden eller på brukerens enhet? Ingen anbefaling eller valg er lagt inn på dine vegne.
2. **Hva skal skje når originalen oppdateres?** Behold varianten knyttet til originalrevisjonen den ble laget fra, eller la brukeren uttrykkelig ta inn nye endringer? Automatisk overskriving er ikke godkjent.
3. **Hvordan skal flere varianter vises?** Én aktiv personlig variant per original, eller flere navngitte varianter side om side? Dette avgjør om biblioteket erstatter en oppføring eller viser flere.
4. **Hva med en egen variant som ennå ikke kan åpnes?** Skjul den fra biblioteket, eller vis den som lagret, utilgjengelig innhold med forklaring og uten aktiv Åpne-handling? En kopi som fortsatt refererer til andres admin-celler må behandles slik.
5. **Hva med en ikke-eier med eksplisitt delegert administrasjon?** Hold den innebygde eier-originalen skjult også for denne brukeren (slik eierregelen er skrevet), eller vis den når en gyldig delegasjon gir alle nødvendige rettigheter? Dette avklarer grensen mellom «bare eieren» og «alle som kan åpne».

### Hva Kjetil skal gjøre

| Handling | Hva avgjørelsen gjelder |
|---|---|
| Godkjenne G1, eller korrigere formålene | §1 og grensene i §2. Et rent «G1 godkjent» velger ikke A/B og besvarer ikke spørsmålene. |
| Svare på spørsmål 1–5 | Velg mellom alternativene over. Spørsmål 1 avgjør lagring; 3–5 avgjør bibliotekets synlige innhold og åpnbarhet. |

STATUS: LEVERT
