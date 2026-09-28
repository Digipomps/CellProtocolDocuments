# ACCEPT — scaffold-administrator og delegering

Dato: 2026-09-09. **G3-underlag, ikke G3-godkjenning.** G3 venter på Kjetil.
WP9 er dokumentasjon og kildeinspeksjon mot `CellScaffold/_wt-sad-20260909`,
branch `pdd/scaffold-admin-delegering`. Ingen bygg eller tester er kjørt i WP9.
Alle kjøreresultater nedenfor viser til tidligere faktiske kjøringer i TESTRESULT.
Flaten er ute av scope etter [planbyttet 2026-09-09](STATUS.md#planbytter-dato--hvorfor);
denne akseptansen har derfor ingen GUI-rader.

WP1–WP8 er implementert og verifisert innenfor de dokumenterte grensene.
Siste fulle regresjon er **2150 tester, 90 feil, 29 unike feilende tester,
null nye mot baseline**. Baselinen på `main` `e1f3e22f` er 2129 tester,
346–347 feil og 59 unike feilende tester. Dette er akseptanse for «ingen nye»,
ikke «alle grønne». De 29 gjenstående røde var røde fra før; de er ikke innført
av denne PDD-en. At 30 andre tidligere røde nå er grønne tilskrives ikke oss,
fordi ren eksport og worktree har ulike miljøforutsetninger.
Bevis: [seneste regresjon](TESTRESULT.md#auth),
[baseline og regresjonsavvik](TESTRESULT.md#regression).

## Forventningskontrakten, rad for rad

Radene speiler [FORMAALSSPEC §3](FORMAALSSPEC.md#3-forventningskontrakt--det-du-kommer-til-å-se).
En levert fil betyr ikke at dens planlagte driftshandlinger er utført.

| Rad | Forventning | Faktisk leveranse og status | Bevis i TESTRESULT |
| --- | --- | --- | --- |
| L1 | Denne formålsspesifikasjonen, fil i oppgavemappen | [FORMAALSSPEC.md](FORMAALSSPEC.md) finnes; G1 er registrert godkjent 2026-09-08 i STATUS. Den historiske brief-auditen og åpne avhengighetene er ikke skrevet om til påstander om staging. | [Artefaktinspeksjon](TESTRESULT.md#wp9-artifacts) |
| L2 | Kontrakt for administrator-registrering og mandat, JSON + fixtures i `contract/`, speilet i `Book/` | Begge [registerkontrakten](contract/scaffold-administrator_v1.json) og [mandatkontrakten](contract/scaffold-mandate_v1.json) finnes, med 2 positive, 14 negative og 6 terskelcaser. WP9 har oppdatert implementasjonsstatus, faktisk signeringskonvolutt og kjente avvik samt lagt byte-identiske kontraktspeil i Book. Fixtures er uendret. Mandatbasert registerhistorikk og manglende målcellehandlinger er eksplisitt `not-implemented`. | [Kontrakt og fixture-presiseringer](TESTRESULT.md#contract), [grønn WP2-kjøring](TESTRESULT.md#auth), [speilinspeksjon](TESTRESULT.md#wp9-artifacts) |
| L3 | Dataflyt: hvem utsteder hva til hvem, fil `dataflow.md` | [dataflow.md](dataflow.md) har K1–K14 og de fire forbudte kantene. WP9 presiserer separat representantbevis, intern tilbakekallskontroll og hvilke målcellekanter som bare er planlagt. | [Kantavstemming](TESTRESULT.md#wp9-dataflow), [verifisert målcellebruk](TESTRESULT.md#revoke) |
| L4 | Kodeendring i CellScaffold, egen gren, ett commit per bladformål | Koden og testene finnes i det oppgitte worktreet på riktig branch. WP3 og WP5–WP8 er dekket av WP1/WP2, som STATUS forklarer. Commit per bladformål, landing og review er **ikke kontrollert eller utført av WP9**; det ligger hos integratoren. Branchpekeren er lest som fil, uten git-kommando. | [Forhåndssjekk](TESTRESULT.md#wp9-artifacts), [register](TESTRESULT.md#registry), [mandat/rollevernet](TESTRESULT.md#auth), [terskel](TESTRESULT.md#threshold) |
| L5 | Testutdata for hver rad i §5, fil `TESTRESULT.md` | Eksisterende bygg-/testbevis er beholdt; tidlige blocked-forsøk leses sammen med senere verifikasjon. Tabellen nedenfor dekker §5. WP9 har lagt til dokument-/kildeinspeksjoner, ingen ny runtime-kjøring. Full suite er fortsatt rød, med null nye feil. | [Bygg](TESTRESULT.md#build), [senere grønt bygg og regresjon](TESTRESULT.md#auth), [WP9-inspeksjoner](TESTRESULT.md#wp9-documentation) |
| L6 | Akseptanse: forventning mot faktisk, fil `ACCEPT.md` | Denne filen er levert med L1–L7, docs, stubs, status og audit. Kjente avvik er synlige; G3 er fortsatt **venter**. | [Artefaktinspeksjon](TESTRESULT.md#wp9-artifacts), [statusavstemming](TESTRESULT.md#wp9-status) |
| L7 | Deploykø-post i HAVEN-Deploy, eier Kjetil | [handoff/WP10_DEPLOYKO.md](handoff/WP10_DEPLOYKO.md) finnes som forberedt posttekst. **Ingen kvittering for registrert post i HAVEN-Deploy er dokumentert eller kontrollert av WP9. WP10 deploy er ikke kjørt.** Dette er ikke dokumentert levering av en ekstern køpost eller drift. | [Artefaktinspeksjon og manglende kø-/deploybevis](TESTRESULT.md#wp9-artifacts) |

## Avledede tester i FORMAALSSPEC §5

«Grønn» nedenfor gjelder det oppgitte lokale testomfanget. Det betyr ikke at
organisasjoner, signatarer eller brukertilgang er provisjonert på staging.

| Test | Faktisk og grense | Bevis |
| --- | --- | --- |
| `test.admin.registry-read` | Grønn gjennom produksjonsresolveren i testmiljø: organisasjon per scaffold, ingen personidentitet i offentlig state. Staging-oppslag gjenstår. | [registry](TESTRESULT.md#registry) |
| `test.admin.mandate-shape` | Grønn: alle fem påkrevde felt, avgrensning, ekte signaturer og negative fixtures; ingen standardutfylling av manglende myndighetsomfang. | [contract](TESTRESULT.md#contract), [senere grønn WP2](TESTRESULT.md#auth) |
| `test.admin.role-is-not-authority` | Grønn: fire roller × fire handlinger, samme avslag som fremmed, samt tellertest 48/33. | [auth](TESTRESULT.md#auth) |
| `test.cell.auth-negative` | Grønn: feil requester, keypath, ressurs/celleinstans og formål avvises; `purpose://prompt.unknown` feiler lukket. | [auth](TESTRESULT.md#auth) |
| `test.admin.threshold-is-policy` | Grønn: lagret 1 → 2 uten kodeendring, én avvist mot 2, to distinkte godtatt, duplikater teller én, ugyldig policy endrer ikke state. | [threshold](TESTRESULT.md#threshold) |
| `test.admin.fresh-root-advisory` | Grønn: `scaffold_administrator_not_provisioned`, separat datarot arver ingen registrering. | [advisory](TESTRESULT.md#advisory) |
| `test.admin.audit-pair` | Grønn test av organisasjon + handlende identitet ved målcellebruk; kilden viser feltene ved utstedelse. Privat lagret spor, ingen staging-utstedelseslogg. Se [audit](#audit). | [revoke](TESTRESULT.md#revoke), [WP9-auditinspeksjon](TESTRESULT.md#wp9-audit) |
| `test.admin.owner-can-list-mandates` | Grønn: eierlesing og avslag til ikke-eier, også ved tom ressurs. Ingen egen flate levert. | [mandates](TESTRESULT.md#mandates) |
| `test.admin.org-link-revocable` | Grønn: rolleavtale alene gir ingen myndighet; tilbakekall og bevarte entitetsdata/gjenlasting. Dette er programvareformen, ikke en faktisk Vegar-avtale. | [revoke](TESTRESULT.md#revoke) |
| `test.cell.stub-scan` | Kildeinspeksjon ferdig; alle normale endepunkt har logikk. Betingede no-op/fallback-grener og manglende atferd er avstemt mot Gap Analysis med `not-implemented`; se [stubs](#stubs). | [wp9-stubs](TESTRESULT.md#wp9-stubs) |
| `test.build` / `test.regression` | Tidligere grønt bygg og 48 relevante tester uten feil; 2150 i full regresjon, 90 feil/29 unike, null nye. Ingen ny kjøring i WP9. | [auth](TESTRESULT.md#auth), [regression](TESTRESULT.md#regression) |
| `test.docs-updated` | Dokumentdiff skrevet og kildeavstemt i WP9; datert og branchavgrenset. Landing sammen med kode gjenstår hos integrator. | [wp9-documentation](TESTRESULT.md#wp9-documentation) |
| `test.status-current` | Én ny logglinje speiler WP9, tidligere verifikasjon og gjenstående arbeid; ingen port er godkjent av utføreren. | [wp9-status](TESTRESULT.md#wp9-status) |

De 48 grønne relevante testene er register 7 + mandat 9 + rollevern 4 og
tellertest 1 + OrchestratorPersistence 8 + TopUpCheckout 19. De to siste
suitene er fortsatt grønne etter feilrettingene; TopUp-forventningene er ikke
hevet for å skjule en ekstra bootstrap-celle.

## Dokumentasjon <a id="docs"></a>

`test.docs-updated`: **dokumentarbeidet er utført**. Last verified against code:
2026-09-09, CellScaffold `pdd/scaffold-admin-delegering`.
Den konkrete dokumentdiffen følger endret oppførsel slik:

| Dokument | Hva diffen beskriver | Atferdsbevis |
| --- | --- | --- |
| [Book 04 — Agreements](../../Book/04_Agreements_Contracts.md#13-scaffold-administrator-and-single-hop-mandates) | Mandatet som eneste delegerte myndighetsbærer i denne modellen, fem felt, ett ledd, separat representant-Contract, rollevern, tilbakekall og privat audit. Eksisterende eier-/Agreement-grunnlag består. | [auth](TESTRESULT.md#auth), [revoke](TESTRESULT.md#revoke) |
| [Book 07 — Scaffold](../../Book/07_Scaffold_Runtime.md#scaffold-administrator) | Organisasjon per scaffold, eget administratorskifte, offentlig state, datarot/provisjoneringsgrenser, lagret terskel 1 med «utviklingsfase, styreleder alene», advarsel under 2. | [registry](TESTRESULT.md#registry), [threshold](TESTRESULT.md#threshold), [advisory](TESTRESULT.md#advisory), [regression](TESTRESULT.md#regression) |
| [Book 22 — Explore](../../Book/22_Explore_Contracts_For_Skeleton_Authoring.md#scaffold-administrator-contracts) og kontraktene med Book-speil | Faktiske GET/SET-operasjoner, signeringskonvolutt, private lesesuffikser, feilkode-/fixture-presiseringer og generiske schema-begrensninger. | [contract](TESTRESULT.md#contract), [wp9-artifacts](TESTRESULT.md#wp9-artifacts) |
| [Gap Analysis](../../Gap_Analysis.md#scaffold-admin-delegering), [dataflow](dataflow.md), [WP10-posttekst](handoff/WP10_DEPLOYKO.md) | Skiller grønne kodeveier fra betingede fallbacks, manglende registerhistorikk via mandat, manglende `publisherAccess.issue`, planlagte målceller og ukjørt staging. | [wp9-stubs](TESTRESULT.md#wp9-stubs), [wp9-dataflow](TESTRESULT.md#wp9-dataflow) |

Ingen kapittel er lagt til, omdøpt eller flyttet; katalogens dokument-ID-er,
titler og browse-metadata er uendret. `book_catalog.json` er derfor urørt.
De nye JSON-speilene er lenket fra de eksisterende kapitlene og fra
PDD-kontraktene. Fixtures er ikke omskrevet. Dokumenter og kode er **ikke
committet eller landet av WP9**; integrator må beholde dokumentdiffen sammen
med den implementerte endringen. Planlagt atferd er ikke gjort til implementert
atferd ved å oppdatere datoen (`lesson.planned-documented-as-implemented`).

## Stubber og no-op-avstemming <a id="stubs"></a>

`test.cell.stub-scan`: **utført som kildeinspeksjon med eksplisitte avvik**,
ikke kjørt som Swift-test. Begge nye celler og felles handlerhjelpere er lest
mot de to kontraktene. Det finnes **ingen ubetinget tom kontrakthandler**.
Alle 13 normale operasjoner har faktisk logikk:

| Celle | Operasjon | Implementert normalsti |
| --- | --- | --- |
| ScaffoldAdministratorRegistry | GET `administrator.state` | Leser persistert organisasjonsstate uten personidentitet. |
| ScaffoldAdministratorRegistry | GET `administrator.thresholdPolicy` | Leser registrert policy. |
| ScaffoldAdministratorRegistry | GET `administrator.history` | Leser registrerings-/overføringskvitteringer, med eier-/Agreement-kontroll. Mandat alene støttes ikke, SAD-02. |
| ScaffoldAdministratorRegistry | SET `administrator.register` | Eierbevis, validering, registrering, audit, snapshot/gjenlesing og kvittering. |
| ScaffoldAdministratorRegistry | SET `administrator.transfer` | Eierbevis, separat administratorskifte med audit og persistert kvittering. |
| ScaffoldAdministratorRegistry | SET `administrator.thresholdPolicy.set` | Eierbevis, verdi-/begrunnelsesvalidering, lagring og advisory-oppdatering. |
| ScaffoldMandate | GET `mandate.list` | Kontrollerer eierskap/administratormandat og filtrerer aktive mandater per ressurs. |
| ScaffoldMandate | GET `mandate.read.<UUID>` | Kontrollerer eier, verifisert representant eller subjekt og leser beholdt mandat. |
| ScaffoldMandate | GET `orgLink.list` | Leser subjektets eller verifisert representants avtaleposter; uvedkommende avvises. |
| ScaffoldMandate | SET `mandate.issue` | Validerer form, representant, signaturer/terskel og omfang; lagrer mottakerbevis, sentral post og audit. |
| ScaffoldMandate | SET `mandate.revoke` | Kontrollerer eier/representant; beholder post med tilbakekall og audit. |
| ScaffoldMandate | SET `orgLink.issue` | Binder rolleavtalen til organisasjon og subjekt, uten Grants; lagrer med audit. |
| ScaffoldMandate | SET `orgLink.revoke` | Beholder avtalen, tilbakekaller dens mandater og lagrer audit. |

Hele inventaret av betingede no-op/fallback-grener og idempotente returgrener:

| Sted i cellen | Betingelse og faktisk retur uten normal effekt | Avstemming |
| --- | --- | --- |
| Registry `setupKeys`, GET `administrator.state` | Svak `self` mangler → `.null`. | SAD-03: eksplisitt feil er `not-implemented`; ikke runtime-verifisert. |
| Registry `setupKeys`, GET `administrator.thresholdPolicy` | Svak `self` mangler → `.null`. | SAD-03, samme status. |
| Registry `setupKeys`, GET `administrator.history` | Svak `self` mangler → `.list([])`. En ekte tom historikk kan også gi `[]`. | SAD-03 for livsløpsgrenen; ikke bevis for at null `self` er en legitim tom historikk. |
| Registry `registerMutation`, alle tre SET-nøklene | `guard let self else { return .null }`: ingen mutasjon eller feil når `self` mangler. | SAD-03: eksplisitt feil er `not-implemented`. Denne no-op-grenen skjules ikke som grønn feilbehandling. |
| Registry `mutate`, `administrator.register` | Samme organisasjon registreres igjen → eksisterende state, ingen ny kvittering. | Tilsiktet kontraktsfestet idempotens, grønn WP1-test. |
| Mandate `revokeMandate` | Allerede tilbakekalt → beholdt post, ingen ny mutasjon/audit. | Tilsiktet idempotens, eksplisitt grønn WP2-assertion. |
| Mandate `mutate`, `orgLink.revoke` | Allerede tilbakekalt → beholdt rolleavtale, ingen ny mutasjon/audit. | Tilsiktet idempotent gren sett i kilde; separat retry-bevis er ikke dokumentert. |

`ScaffoldMandateCell` har ingen tom vellykket `self == nil`-handler; GET og SET
kaster `persistenceUnavailable`. Namespace-nøklene `mandate`, `orgLink` og
bare `mandate.read` går til reell lesekontroll og avvises som ufullstendige valg.
`catch { }` i `validateCellSpecificAccess` etterfølges av `false`; dette er
avslag, ikke vellykket no-op. `nil` i metodekrav delegerer til ordinær kontroll.
`orgLinkRef == nil` hopper bare over den valgfrie tilknytningskontrollen;
mandatets øvrige myndighetskontroller gjelder fortsatt.

Avstemt mot [Gap Analysis SAD-01–SAD-05](../../Gap_Analysis.md#scaffold-admin-delegering).
`publisherAccess.issue` mangler helt i målcellen på denne branchen og står som
`not-implemented`; det er ikke en skjult handler i en av de to nye cellene.
Mandatbasert registerhistorikk står også som `not-implemented`.
Ingen kontraktendepunkt er ført som implementert med en skjult ubetinget no-op,
og de betingede no-op-grenene er navngitt med manglende atferd og status.
Dette oppfyller dokumentasjonsavstemmingen i
`lesson.cellscaffold-two-holes`; det beviser ikke at SAD-03 er rettet eller testet.
Bevis: [WP9-stubinspeksjon](TESTRESULT.md#wp9-stubs).

## Faktisk status og gjenstående arbeid <a id="status"></a>

`test.status-current`: [STATUS.md](STATUS.md) har én ny WP9-logglinje.
Tidligere blocked-rapporter er historikk og erstattes for nåstatus av de senere
grønne WP1/WP2/WP4-kjøringene. WP3 og WP5–WP8 er dekket, ikke droppet.
G1 og G2 er godkjent; **G3 er fortsatt venter**. Arbeidet her kan ikke godkjenne
porten på Kjetils vegne. Bevis: [statusavstemming](TESTRESULT.md#wp9-status).

Følgende er uttrykkelig **ikke gjort**:

- **WP10 deploy er ikke kjørt; ingenting fra denne PDD-en er i drift på staging.**
  Postteksten finnes, men registrering i HAVEN-Deploy er uten kontrollert kvittering.
- **`entity:digipomps` og `entity:dimy` er ikke opprettet på staging.** Faktiske
  representantbevis og signeringsoppsett er heller ikke provisjonert der.
- **Vegars publiseringstilgang er ikke gjenopprettet.** Det er en egen oppgave;
  se [VEGAR_HURTIGFIKS_FUNN.md](handoff/VEGAR_HURTIGFIKS_FUNN.md). De tidlige
  forventningene om at mandatet alene løser dette må leses med SAD-01 og
  den presiserte WP10-postteksten.
- **Den juridiske siden av organisasjonstilknytningen er ikke vurdert av jurist.**
  Testene etablerer programvareformen, ingen juridisk gyldighet.
- **29 unike tester er fortsatt røde fra før i CellScaffold.** De er ikke våre;
  akseptansen måler ingen nye feil, ikke alle grønne.
- Kode-/dokumentlanding, commitstruktur per bladformål og ekstern deploykøføring
  er ikke utført eller verifisert av WP9. SAD-01–SAD-05 er ikke lukket ved kodeendring.

## Revisjonsspor: organisasjon og handlende identitet <a id="audit"></a>

`test.admin.audit-pair` avstemmes mot
[testbeviset for bruk og tilbakekall](TESTRESULT.md#revoke) og
[WP9s kildeinspeksjon](TESTRESULT.md#wp9-audit).

- `ScaffoldMandateCell.issue` legger inn `operation = mandate.issue`,
  `mandateID`, `issuerEntityRef`, `actingIdentityUUID`, `reason` og `at` før
  snapshot-lagring/gjenlesing. Organisasjonsreferansen kommer fra det validerte
  mandatet og gjeldende register; aktøren kommer fra den verifiserte requesteren.
- `authorize(recordUse: true)` beholder organisasjonen fra mandatet og
  identiteten som bruker det, med mandat-ID og begrunnelse. Den grønne
  `testTargetCellChecksMandateOnEveryCallAndRevocationRetainsDataAndAuditPair`
  kontrollerer `issuerEntityRef = entity:digipomps` og subjektets faktiske UUID
  ved reset-handlingen, og eierens UUID ved tilbakekall.
- Registerets `AuditEntry` beholder `fromEntityRef`, `toEntityRef`,
  `actingIdentityUUID`, `reason`, `changedAt` og `receiptID`.
  `testTransferIsSeparateAuditedActionAndSurvivesProductionStorageReload`
  verifiserer Digipomps → DiMy, to ulike kvitteringer, gjenlasting og handlende
  eieridentitet i lagret audit.

Dette er **privat persistert celle-audit**. Den offentlige registerstaten har
`registeredBy/setBy = null`; historikkprojeksjonen og Flow-kvitteringene
eksponerer ikke hele personsporet. WP9 har ikke hentet noen produksjonslogg,
utstedt et ekte mandat eller levert et nytt audit-GET. Testen av aktørparet
beviser ikke i seg selv assertions på samtlige utstedelsesfelt; de øvrige
feltene er avstemt direkte mot `issue`/`audit`/`persist` i kilden.

## WP9 — sluttmelding

Skrevet: Book 04/07/22, to oppdaterte kontrakter med Book-speil, Gap Analysis,
presisert dataflyt og WP10-posttekst, WP9-inspeksjonsankre i TESTRESULT,
denne radvise akseptansen og én linje i STATUS. Dokumentenes lenker,
kontraktspeil og fixturelikhet er kontrollert som filinspeksjon.

Ikke gjort: bygg, testkjøringer, kodeendringer, git, Docker, deploy, faktisk
organisasjons-/representantprovisjonering, Vegars tilgang eller juridisk vurdering.
Ingen port er godkjent. Integratoren trenger å reviewe dokumentdiffen sammen
med koden, håndtere de navngitte avvikene og commitkravet, og la Kjetil vurdere
G3 og den faktiske HAVEN-Deploy-posten før WP10. Bevar testloggene som bevis.

## Tillegg etter WP9 — 2026-09-09, commit av L4

Skrevet etter WP9, av gjennomgangen, ikke av WP9. WP9s tekst over står uendret.

L4 sa at commit per bladformål «ikke er kontrollert eller utført av WP9». Ved
gjennomgangen viste `git branch -v` at `pdd/scaffold-admin-delegering` fortsatt
pekte på basen `e1f3e22f`: **branchen var tom, og hele WP1–WP8 lå ucommittet i et
worktree på én maskin.** Det er nå rettet. Branchen står på `bcaf1e5e` med seks
commits, ett per bladformål, 18 filer, +2910/−336, og rent arbeidstre:

`099eeae0` refaktorering til `EntityAnchorProofSupport` · `148c4291` register ·
`00938d67` mandat · `9b10a039` målcellebruk · `a9c0e2e1` rollevern ·
`bcaf1e5e` oppstart og readiness.

**Ingen push.** Ingen bygg eller tester er kjørt etter commiten; commitene
inneholder nøyaktig de filene som var verifisert i regresjonen 13:55–14:01.
Landing og review ligger fortsatt hos integratoren, og **G3 venter fortsatt på
Kjetil**. Kvittering: [handoff/COMMIT_RAPPORT.md](handoff/COMMIT_RAPPORT.md);
det stoppede forsøk 1: [handoff/COMMIT_RAPPORT_forsok1_stoppet.md](handoff/COMMIT_RAPPORT_forsok1_stoppet.md).

Gjennomgangen fant ingen feil i WP9s akseptanse: alle sju L-rader og alle fjorten
§5-tester er dekket, alle 29 lenker og ankere løser, Book-speilene er byte-identiske
med kontraktene, og påstandene om weak-self-grener og manglende
`publisherAccess.issue` er verifisert i kilden.

---

# G3-underlag — 2026-09-25

Akseptansen over ble skrevet 9. september og sa uttrykkelig at WP10 ikke var
kjørt, at `entity:digipomps` ikke fantes noe sted, og at Vegars tilgang ikke var
gjenopprettet. Alt dette er gjort siden. Dette tillegget måler forventningen mot
**dagens** tilstand, med ferske tall, og sier hva porten faktisk avgjør.

Målingene under er hentet 2026-09-25 kl. 09:37Z. Rå utdata:
[evidence/g3-20260925/tilstand.md](evidence/g3-20260925/tilstand.md).

## Hvordan arbeidet landet

Ikke gjennom grenen `pdd/scaffold-admin-delegering` (`bcaf1e5e`) — den ble aldri
pushet. Innholdet landet på `CellScaffold` main 2026-09-18 i **#247**, målt på
innhold og ikke på ancestry: 11 av 18 filer byte-identiske, 7 utvidet på main
(STATUS 2026-09-23 11:38Z). På main `18c14c32` i dag ligger:

```
Sources/App/Cells/Admin/ScaffoldAdministratorRegistryCell.swift
Sources/App/Cells/Admin/ScaffoldMandate.swift
Sources/App/Cells/Admin/ScaffoldMandateCell.swift
Sources/App/Cells/Admin/ScaffoldMandateProofSupport.swift
Sources/App/Support/ScaffoldAdministratorProvisioner.swift     ← kom til i leveransen
Sources/App/Support/ScaffoldAdministratorRuntimeSupport.swift
Tests/AppTests/Fixtures/ScaffoldMandate/{mandate-positive,mandate-negative,threshold-policy}.json
```

## Forventningskontrakten (§3), rad for rad — i dag

| Rad | Forventning | I dag | Bevis |
|---|---|---|---|
| L1 | Formålsspesifikasjon | levert, G1 godkjent 2026-09-08 | [FORMAALSSPEC.md](FORMAALSSPEC.md) |
| L2 | Kontrakt + fixtures, speilet i Book | levert; fixturene ligger nå også i CellScaffold main | `contract/`, `Book/scaffold-*_v1.json` |
| L3 | Dataflyt | levert | [dataflow.md](dataflow.md) |
| L4 | Kode i CellScaffold, egen gren, commit per bladformål | **landet på main** — men via #247, ikke via den opprinnelige grenen. Commit-per-bladformål gjelder den grenen, ikke #247 | STATUS 2026-09-23 11:38Z |
| L5 | Testutdata for §5 | levert 2026-09-09; CI grønn på #255 etter én ustabil krasj | [TESTRESULT.md](TESTRESULT.md), `evidence/lev2/` |
| L6 | Akseptanse | denne filen | — |
| L7 | Deploykø-post, eier Kjetil | **utført**: staging 2026-09-23, prod 2026-09-24 04:03Z | [handoff/WP10-PROD-20260923.md](handoff/WP10-PROD-20260923.md) |

## Er det i drift nå?

Målt 2026-09-25 09:37Z, ikke lest fra gårsdagens logg.

| | app_revision | status | scaffold-administrator-advarsel |
|---|---|---|---|
| prod | `e6277af1` (bygget 2026-09-25 01:50Z) | `ready` / `serving` | ja: `requiredSignatures=1`, `setAt=2026-09-09` |
| staging | `4dd70c52` (bygget 2026-09-24 13:35Z) | `ready` / `serving` | ja, samme |

Prod-revisjonen `e6277af1` er en **forfar av** CellScaffold main `18c14c32`
(`git merge-base --is-ancestor` exit 0). Prod kjører altså kode som er landet.

Det som gjør dette sterkere enn kvitteringen alene: registreringen har overlevd
flere utrullinger. Den ble satt 2026-09-24 på revisjon `03fc0eff`; prod kjører nå
`e6277af1` og advarselen står fortsatt. Det er persistert tilstand, ikke en
engangseffekt av provisjoneringsskriptet.

**Presisjon som ikke skal glattes over:** readiness-advarselen oppgir
`scaffold=scaffold:cellscaffold` og `requiredSignatures=1`. Den oppgir **ikke**
hvilken entitet som er administrator. At det er `entity:digipomps` hviler på
provisjoneringskvitteringene fra 24. september, ikke på dagens helsesvar.

## Kvitteringene fra provisjoneringen

Fra `wp-sad-prod.sh` 2026-09-24T04:03:35Z, begge representanter exit 0:

```
status                     committed_verified
environment                production
administratorEntityRef     entity:digipomps
scaffoldRef                scaffold:cellscaffold
authorityActions           mandate.issue, mandate.revoke, orgLink.issue, orgLink.revoke
requiredSignatures         1
registryReceiptID          7D562AE9-5452-47CB-B396-78AF457243F7
approvalReference          G3:user-approved:2026-09-23
writableBindsBackedUp      3   (CellsContainer, IdentityVaults, Database)
networkDuringProvisioning  none
backupDisposition          deleted_after_verified_restart
validUntil                 2026-12-23T04:03:05Z
```

Representanter i prod: **kjetil2** (`87FA1CF0…`) og **Vegar** (`836F624A…`),
hver med egen `representativeBindingSHA256`.

## Hva porten faktisk avgjør

G3 sier ikke «alt er ferdig». Den sier: **det som ble lovet i §3, er levert, og
det som ikke er levert står navngitt under.** Det er den avgjørelsen som ligger
til deg.

## Uttrykkelig ikke gjort

- **`entity:dimy` er ikke opprettet noe sted.** Bare `entity:digipomps`. Q1 i
  FORMAALSSPEC (hvilke scaffolds DiMy eier) er fortsatt ubesvart i praksis.
- **Terskelen er 1.** Bevisst valgt («utviklingsfase, styreleder alene»), men
  advarselen står i readiness i både prod og staging, og vil stå til den heves.
- **Mandatene utløper 2026-12-23.** Ingen fornyelsesrutine er dokumentert. Tre
  måneder er kort nok til at det bør stå i en kalender, ikke i en logg.
- **Staging mangler `arendalsuka_published_read_access_not_provisioned`-oppsettet.**
  Advarselen står i staging, ikke i prod.
- **Ingen jurist har vurdert organisasjonstilknytningen.** Testene etablerer
  programvareformen, ikke juridisk gyldighet.
- **Gap Analysis er utdatert på to punkter** og må rettes: SAD-01 sier
  `publisherAccess.issue` ikke har handler — den finnes nå på main
  (`ArendalsukaPublisherBootstrap.swift` gir `rw-s` på nøkkelen). SAD-04 sier
  WP10 er «planned / not executed» — den er utført i begge miljøer.
  SAD-02, SAD-03 og SAD-05 står fortsatt.
