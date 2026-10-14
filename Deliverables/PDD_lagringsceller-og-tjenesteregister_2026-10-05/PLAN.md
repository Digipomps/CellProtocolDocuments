# Plan — lagringsceller og tjenesteregister, leveranse 1

2026-10-06, revidert 2026-10-08 · Utkast til G2 · Ikke godkjent

Leveranse 1 dekker lagringscelle mot Hetzner, tjenesteregister med ni tjenester og bytte av tjeneste. Videresalg via DiMy (c://resale.*) er leveranse 2 og er ikke med her.

## Målt før planen (2026-10-06)

| Hva | Funn | Kilde |
|---|---|---|
| Main | `e5c3434` (2026-10-05). Siste CI-kjøring på main er grønn på `fdcfe7a5`; `e5c3434` er merket skip ci. | GitHub Actions |
| Lagringscellen | Uendret på main: 687 linjer, bare lokal disk, 492 linjer tester. | `Sources/App/Cells/ObjectStorage/`, `Tests/AppTests/ObjectStorageAdapterCellTests.swift` |
| S3-bibliotek | Finnes ikke i `Package.swift`. swift-crypto og Vapor finnes, så signering (SigV4) kan skrives uten ny avhengighet. | `Package.swift` |
| Tjenestenøkler | `OwnerScopedCredentialCell` finnes og er registrert per identitet. | `Sources/App/Cells/Credentials/`, `Sources/App/configure.swift:1253` |
| Entitetsklasse | Finnes ikke på main. Ingen type for enkeltindivid / selskap / ideell. | søk i `Sources/` |
| Opplasting i web | `FileUpload` sender filen som base64 i ett kall med grense 4 MB. Reell filgrense i flaten er ca. 2,9 MB. Opplasting rett til en signert adresse finnes ikke. | `Public/js/skeleton-runtime.js` (uploadMode), `Sources/App/Controllers/VaporBrowserhead.swift:365` |
| Hvem lagrer til lagringscellen i dag | Ingen. Fem steder skriver media rett til disk: musikk, publisering, personlig side, kunstnersalg og utgivelsesløpet. Konferanseinnhold ligger som base64 i celletilstand. | `MusicPublishingSupport.swift:614`, `PublicationSupport.swift:639`, `PersonalPagePublisherCell.swift:1253`, `ArtistSalesSupport.swift:342`, `MusicReleasePipeline.swift:436`, `ConferencePublishedContentCell.swift:1182` |
| Nøkkeloppslag | `OwnerScopedCredentialCell` gir aldri ut klartekst. Nøkkelen hentes i prosessen via `OwnerScopedCredentialStore.secret(ownerIdentityUUID:alias:)`, slik AIGateway gjør. | `Sources/App/Support/OwnerScopedCredentialStore.swift:149` |
| Kompilering | Skyen jeg jobber i har ikke Swift. PR-er bygges og testes av Linux-CI (`ci/run-tests.sh`). | `.github/workflows/admin-scaffold-image.yml` |

## Fem ting du må avgjøre i G2

1. **Ny opplastingsmåte i skjelettet (`uploadMode: "presigned"`).** Web tar i dag ikke filer over ca. 2,9 MB gjennom en celle. Uten ny opplastingsmåte kan flaten ikke laste opp en lydfil. Den er derfor nødvendig i leveranse 1, ikke valgfri. Det er en ny skjelettkapabilitet og krever ditt ja; den testes mot funksjon og formål i web og Binding før main.
2. **Hvem eier lagringen for felles flater?** Musikkflaten (Butterpop) er én celle per scaffold med egen eier (`music:the-butterpop-collective`), ikke en personlig celle. Den har ingen nøkler. Forslag: felles flater lagrer i scaffold-eierens lager (Digipomps betaler), personlige flater i brukerens eget lager.
3. **Betaling for selskaper i registeret.** Entitetsklasse finnes ikke i koden. Forslag: registeret er gratis for alle i leveranse 1, og AP8 bygges når Astras entitetsutvidelse er på main.
4. **Måling av trafikk ut.** Når filer hentes direkte fra tjenesten, ser ikke cellen bytene. Forslag: lagret mengde måles eksakt; trafikk ut vises som anslag, merket «anslag».
5. **Prisenhet under 1 øre (ditt svar 2026-10-08).** Forslag: alle priser og målte kostnader i registeret og lagringscellen lagres som heltall i mikroøre (1 øre = 1 000 000). Pris = kostpris + påslag (prosent i hundredeler og/eller fast beløp), vist hver for seg. Kostpris i EUR/USD omregnes med kurs lagret med kilde og dato. Brøkdeler samles per eier og trekkes som hele øre i `PaymentGateCell` (som i dag teller hele øre) når summen når 1 øre; resten føres videre. Selve trekket for lagring hører til leveranse 2; i leveranse 1 beregnes og vises beløpet.

## Arbeidspakker

Utfører: **Losen** = jeg, i en ren klone av main, levert som PR som CI bygger og tester. **Astra** = Codex. **Kjetil** = deg.

| AP | Formål (purposeRef) | Hva som lages | Tester som må bli grønne | Utfører | Det du ser |
|---|---|---|---|---|---|
| AP0 | pkg.std.everything-works | Utgangspunkt: tom PR fra main for å se at CI er grønn før endring. | test.build, test.regression (grunnlinje) | Losen | `TESTRESULT.md#baseline` |
| AP1a | c://persist | Transportlag som kan byttes ut i test (samme mønster som `PushHTTPTransport`), og inntak av det `FileUpload` faktisk sender (`dataBase64`, `chunks`). | enhetstester for inntak og etterligning | Losen | PR A |
| AP1 | c://persist | S3-transport i lagringscellen: signering, put, get, head, delete for filer opp til 8 MB (web: ca. 2,9 MB til `FileUpload` kan mer). Større filer avvises med feil som peker på AP2. | test.lagring.rundtur (CI: mot etterligning. Ekte protokoll: S3-kompatibel testtjeneste lokalt eller på verten, fjernet etterpå) | Losen | PR A, testutdata |
| AP2 | c://persist, c://true-claims | Signert adresse for store filer: `presignUpload`, `confirmUpload`, `presignRead`. Cellen sjekker størrelse hos tjenesten før referansen lagres. Referansen sier om sha256 er «kontrollert» eller «oppgitt». | test.lagring.rundtur (500 MB), test.lagring.les-bytene | Losen | PR A |
| AP3 | c://configure | Tjenestevalg som konfigurasjon: registeroppføring + nøkkelalias. Bytte av aktiv tjeneste; gamle referanser peker fortsatt på sin tjeneste. | test.lagring.bytt-tjeneste | Losen | PR A |
| AP4 | c://own | Nøkler hentes i prosessen fra `OwnerScopedCredentialStore` på eierens identitet og alias. Eierbinding for felles flater etter avgjørelse 2. Ingen nøkkel i state, flow, logg eller persistert celle. | test.cell.auth-negative, test.lagring.ingen-hemmeligheter | Losen | PR A |
| AP5 | c://meter | Bruk per eier: lagret mengde eksakt, trafikk ut som anslag (se avgjørelse 4). | test.lagring.maaling | Losen | PR A |
| AP5b | c://meter, c://register.choose | Pengetype i mikroøre med kostpris + påslag og valutakurs med kilde og dato (avgjørelse 5). Brukes av måling, rangering og prisen per oppslag (1 øre). | test.pris.mikroore (avrunding, overføring av rest, ingen tap ved summering), test.pris.kost-pluss-paaslag | Losen | PR A |
| AP6 | c://register.find | Ny celle `StorageServiceRegistry` (én per scaffold, eid av scaffold-eieren). Oppføring med kilde og dato, forslag og godkjenning, utdatert etter 90 dager. Ni tjenester som datafil, datert 2026-10-01. Scaffold-eide celler opprettes ikke av seg selv på en vert (`requireExisting`), så provisjonering på staging og prod er et eget steg i AP12. | test.register.oppforing-komplett, test.register.utdatert-merkes | Losen | PR B |
| AP7 | c://register.choose | Rangering og kostanslag ut fra krav og volum. | test.register.rangering (tallene fra dokumentet 01.10) | Losen | PR B |
| AP8 | c://register.access | Tilgang per entitetsklasse. **Blokkert** til entitetsklasse finnes på main (se avgjørelse 3). | test.register.tilgang-per-klasse | Astra + Losen | — |
| AP9 | c://surfaces | To flater: «Lagringstjenester» og «Mitt lager», som CellConfiguration. Ny uploadMode (avgjørelse 1) med test i web og Binding før main. | pkg.std.gui-surface (paritet mot godkjente bilder, veier inn, lastetid) | Losen (web), Astra (Binding) | PR C, skjermbilder ved siden av skissene |
| AP10a | c://persist (vert vokser ikke) | Musikk: `MusicLocalAssetStorage` og utgivelsesløpet lagrer via lagringscellen. | test.lagring.vert-vokser-ikke (ekte: staging) + enhetstest mot etterligning | Losen | PR D |
| AP10b | c://persist | Publisering: `PublicationLocalStorage` via lagringscellen. | som over | Losen | PR D |
| AP10c | c://persist | Personlig side og kunstnersalg via lagringscellen. | som over | Losen | PR E |
| AP10d | c://persist | Flytteskript for filer som allerede ligger på disk. Tørrkjøring som standard. | tørrkjøringsrapport | Losen skriver, deploykø kjører | rapport |
| AP11 | pkg.std.cell-contract, pkg.std.cell-combination | Kontrakter med fixtures, dataflyt, dokumentasjon i samme PR som koden. | test.cell.contract-fixtures, test.cell.stub-scan, test.cells.dataflow-matches-contracts, test.docs-updated | Losen | `contract/`, `dataflow.md` |
| AP12 | c://root | Utsetting på staging og ett sammenhengende forløp. Går via deploykøen med egen claim. | test.lagring.forloep, test.gui.load-time | Kjetil / deploykø, Losen måler | staging |
| AP13 | uavhengig kontroll | Astra går gjennom PR A–D før merge. | funn i PR | Astra | PR-kommentarer |

Rekkefølge: AP0 → AP1a, AP1–AP5 (PR A) → AP6–AP7 (PR B) → AP9 (PR C) → AP10a–b (PR D) → AP10c (PR E) → AP12. AP11 følger hver PR. Hver PR committes og pushes etter første grønne bygg, ikke til slutt.

## Det du selv må gjøre

1. Svare på de fire avgjørelsene over.
2. ~~Opprette testbøtte hos Hetzner.~~ Ikke nødvendig (2026-10-08): det testes mot en S3-kompatibel tjeneste lokalt på Mac-en eller på verten. Den startes for kjøringen og fjernes etterpå med data og image, og vertens diskgate respekteres.
3. Si fra til Astra at PR-ene kommer til gjennomgang, og at AP8 venter på entitetsutvidelsen.
4. Godkjenne utsetting på staging når PR A og B er merget.

## Hva som testes hvor

- **I Linux-CI, uten ekte tjeneste:** signering mot kjente fasitverdier, rundtur mot etterligning, bytte av tjeneste, negative tilgangstester, hemmelighetssøk, register og rangering.
- **Mot S3-kompatibel testtjeneste lokalt eller på verten:** rundtur med 500 MB, `test.lagring.les-bytene`, måling mot tjenestens egne tall. Hetzner selv testes først ved utsetting.
- **Bare på staging:** `test.lagring.vert-vokser-ikke`, `test.lagring.forloep`, lastetid, paritet mot bildene.
- `test.cell.stub-scan` og `test.cells.dataflow-matches-contracts` er inspeksjoner jeg gjør for hånd og fører i ACCEPT.md; de finnes ikke som kjørbare tester.

Konferanseinnhold som ligger som base64 i celletilstand er ikke med i leveranse 1. Det får vertens disk til å vokse på en annen måte og bør bli en egen oppgave.

## Uavhengig kontroll

En egen Fabel-tråd prøvde planen mot main 2026-10-06. Dom: «holder delvis». Rettet etter kontrollen: nøkkeloppslag går ikke via celle; 8 MB gjennom cellen var feil (web tåler ca. 2,9 MB); AP10 var undervurdert (fem lagre, ikke ett); eierspørsmålet for felles flater manglet; scaffold-eide celler må provisjoneres.

## Kjente risikoer

- Testtjenesten er ikke Hetzner. Avvik i Hetzners S3-dialekt (sjekksum, signerte adresser) sees først ved utsetting.
- Hetzner kan mangle støtte for sha256-sjekksum ved opplasting. Da merkes store filer «oppgitt», ikke «kontrollert», til en bakgrunnskontroll har lest dem.
- Ny scaffold-eid celle har gitt regresjoner før (`lesson.new-cell-must-declare-its-provisioning-mode`). AP6 følger mønsteret fra `PublicationCell`: eid av scaffold-eieren, lagt i `ownerContextConsumers`, golden-digest oppdatert.
- Arbeidstreet på Mac-en står på Astras gren. Jeg skriver ikke kode der; alt går via egen klone og PR.

<a id="dataflow"></a>
## Dataflyt

Se `dataflow.md`. Hver kant der finnes i `contract/`.
