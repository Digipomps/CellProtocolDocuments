# Akseptanse — tillitspakke for agentflåte

## Stubs <a id="stubs"></a>

WP2 registrerer følgende reserverte handlere med komplette Explore-kontrakter. Ved autorisert kall med kontraktens objektpayload returnerer hver handler eksplisitt `status: not-implemented`, med `action` og `reason`. De endrer ikke pakke-digest eller flåteceller. Ukjent formål eller feil requester avvises før handleren kan utføre noe.

| Metode | Keypath | Grant | Videre slice |
|---|---|---|---|
| SET | `trustPackage.adjust.whitelist` | `rw--` | WP6 |
| SET | `trustPackage.adjust.credentials` | `rw--` | WP6 |
| SET | `trustPackage.adjust.webfetchWrite` | `rw--` | WP6 |
| SET | `trustPackage.approve` | `rw-s` | WP7 |
| SET | `trustPackage.fleet.stop` | `rw--` | WP7/10 |
| SET | `trustPackage.open.instruction` | `r---` | WP10 |
| SET | `trustPackage.open.receipt` | `r---` | WP10 |
| SET | `trustPackage.open.package` | `r---` | WP10 |
| GET | `trustPackage.state.audit` | `r---` | WP10 |

Ingen stille no-op-handlere i WP2. `trustPackage.state.audit` inne i state har samme eksplisitte status. `reach`/`edges` er tomme (WP3). Justering, godkjenning, stopp og navigasjon er ikke implementert. GUI-paritet og payload-substitusjon er ikke vurdert her (WP11).

## Docs <a id="docs"></a>

WP12, 2026-09-09 — `purpose://quality.docs-in-same-change`, `purpose://cell.contract-explicit`. Tabellen under avstemmer dokumentasjonen mot levert WP1–WP10-kode og de siste sluttmeldingene i TESTRESULT. **Stubs-seksjonen over er historikk fra WP2, ikke gjeldende implementasjonsstatus:** alle deklarerte v0-handlere er implementert etter WP10.

- [x] [Book/36](../../Book/36_Agent_Trust_Package.md) har «Last verified against code: 2026-09-09», eksplisitt kildegrunnlag og anvender `lesson.planned-documented-as-implemented`.
- [x] [Book-kontrakten](../../Book/agent_trust_package_contract_v0.json) og [PDD-kontrakten](contract/agent_trust_package_contract_v0.json) har identisk innhold og avstemt `status`: 6 deklarerte GET + 10 SET er implementert; ingen deklarerte v0-keypaths er fortsatt `not-implemented`. To konfigurasjons-GET-er og målcellens ceiling-/binding-/kvitteringsoperasjoner er oppgitt separat med Grants. Manglende funksjoner er eksplisitt `not-implemented`, uten oppdiktede keypaths.
- [x] [Book/04 §8](../../Book/04_Agreements_Contracts.md#8-signature-and-time-semantics) erstatter det utdaterte WP9-integrasjonsforbeholdet med én kort setning om signert kvittering og lenke til kapittel 36.
- [x] [Book/23 §8](../../Book/23_Purpose_Knowledge_Base.md#8-new-purpose-capture) får én kort setning om kandidatnoder brukt i levert WP1–WP10. Ingen taksonominoder promoteres; det krever Kjetil.
- [x] [book_catalog.json](../../Book/book_catalog.json) får én oppføring for kapittel 36, slik dokumentasjonsferdigheten krever for et nytt Book-kapittel; øvrige oppføringer er bevart.
- [x] Porthole-paritet, per-Grant V2, flerpartssignering og distribuert revokasjon står under «Ikke implementert». Manglende route-/instruksjonskilder, AI-metadata- og journalgrenser samt WP11/WP13-verifisering er avgrenset uttrykkelig.

| Doc-diff | Levert kodeendring den beskriver | Eksisterende implementasjonsevidens |
| --- | --- | --- |
| Book/36 §1–3; begge kontrakters status | WP1 `CellBase/Agreement/AgentTrustPackage.swift` (koding/digest); WP2 `AgentTrustPackageCell.swift`, `AgentTrustPackageContract.swift`, factory og `configure.swift`; WP3 `AgentTrustReach.swift` | [Projeksjon](TESTRESULT.md#projeksjon), [kontrakt](TESTRESULT.md#contract), [rekkevidde](TESTRESULT.md#rekkevidde) |
| Book/36 §1, §8 og kildegrenser i kontraktstatus | WP4 provider-tools-regel i pakkecellen og felles hasher i `AIGatewaySupport.swift`; adapter-body-testene | [Provider-tools](TESTRESULT.md#provider-tools) |
| Book/36 §4 og §6; kontraktstatus | WP5 `WebKnowledgeCells.swift` (WebFetchCeiling/transport); WP6 `AgentTrustPackageAdjustment.swift`, pakkecellens `adjust.*` og `AIGatewayCell.swift` (lagret policy-ceiling) | [WebFetch](TESTRESULT.md#webfetch), [justering](TESTRESULT.md#justering) |
| Book/36 §5; kontraktstatus | WP7 `AgentTrustPackageApproval.swift`, approve/approved/stop i pakkecellen, WebFetch-/AI-flåtebinding og port | [Godkjenning](TESTRESULT.md#godkjenning) |
| Book/36 §3–4; kontraktstatus | WP8 karantene for innlagt pakke-JSON og `deniedAttempts`/hendelser i pakkecellen | [Injeksjon](TESTRESULT.md#injeksjon), [pakke gir ikke rett](TESTRESULT.md#pakke-gir-rett) |
| Book/36 §7; Book/04-peker; kontraktstatus | WP9 `ReceiptSignature.swift`, `EffectReceipt.swift`, `PurposeBoundExternalAction.swift`; WP9b utstedelse i WebFetch/PurposeBoundAIGateway og `SignedCellReceiptStore.swift` | [Kvittering, inkludert fullført WP9b](TESTRESULT.md#receipt) |
| Book/36 §2, §8–9; kontraktstatus | WP10 `AgentTrustPackageAudit.swift`, samling/bevart snapshot/open.* i pakkecellen, Explore-schema og etter-factory | [Diff, siste fullførte WP10](TESTRESULT.md#diff) |
| Book/23-kandidatpeker; Book/36 §10 | De leverte cellenes/fabrikkens `purpose://candidate.tillitspakke-agentflaate.*`-referanser; capture-grensen fra Book/23 §8 | [PLAN WP12](PLAN.md), siste WP1–WP10-sluttmeldinger; ingen canonical runtime-taksonomiendring |

WP12 er dokumentasjonsakseptanse. Tidligere bygge-/XCTest-resultater er referert, ikke kjørt på nytt her. Dette krysser ikke av WP11-paritet, WP13 ende-til-ende eller G3.

- [x] `test.docs-updated`: statisk sammenligning av deklarerte keypaths/Grants mot Swift, identiske kontraktkopier, bare endret `status` i PDD-kontrakten, seks gyldige fixture-referanser, 40 nye/endrede Markdown-lenker og katalogens unike ID/slug/order er kontrollert. Eksisterende Docs-MCP-søk finner kapittel 36. Ingen bygg/XCTest i WP12.

## WP13 — forventet mot faktisk <a id="acceptance"></a>

Avstemt 2026-09-09 mot de 14 leveransene i [FORMAALSSPEC §3](FORMAALSSPEC.md#3-forventningskontrakt--det-du-kommer-til-å-se). «Levert» gjelder den angitte artefakttypen; godkjente mockups er ikke dokumentasjon på en kjørende flate. G1-GUI-godkjenningen er registrert i [STATUS](STATUS.md), selv om spesifikasjonens opprinnelige «Godkjent»-kolonne fortsatt sier «nei». G3 er ikke gitt.

| Leveranse / forventet | Faktisk ved WP13 | Evidens |
| --- | --- | --- |
| 1. «Før», tom: bilde uten konfigurert flåte | **Levert som godkjent referansemockup**, PNG 780 × 1918. Runtime-paritet er ikke levert. | [Bilde](images/tillitspakke-for-tom-v1.png), [mockup-avgrensning](images/README.md) |
| 2. «Før», fylt: AIGateway → WebFetch + ScopedCredential, tre domener, modellrute, instruksjonslenke, rekkevidde og justering/godkjenning | **Levert som godkjent referansemockup**, PNG 780 × 3888. Faktisk PurposeBound-rute/instruksjon følger invokasjonen og er ikke en lesbar gjeldende kilde i pakken; full runtime-paritet er ikke levert. | [Bilde](images/tillitspakke-for-fylt-v1.png), [kildegrenser](../../Book/36_Agent_Trust_Package.md), [e2e](TESTRESULT.md#e2e) |
| 3. «Før», feil: policy-/godkjenningsdigest avviker | **Levert som godkjent referansemockup**, PNG 780 × 3934. Startport og gammel digest er testet gjennom API; visuell feiltilstand er ikke verifisert i Porthole. | [Bilde](images/tillitspakke-for-feil-v1.png), [godkjenning](TESTRESULT.md#godkjenning), [e2e](TESTRESULT.md#e2e) |
| 4. «Etter», ingen avvik | **Levert som godkjent referansemockup**, PNG 780 × 1964. Audit-status med null avvik er testet; runtime-paritet er ikke levert. | [Bilde](images/tillitspakke-etter-ok-v1.png), [diff](TESTRESULT.md#diff), [e2e](TESTRESULT.md#e2e) |
| 5. «Etter», brudd: syntetisk fetch utenfor whitelist og credential-forsøk | **Levert som godkjent referansemockup**, PNG 780 × 2978. WP10-fixturen viser to avvik, sju effekter og fem innenfor. Det er ikke bevis for vellykket credential-oppslag eller en rendret runtime-flate. | [Bilde](images/tillitspakke-etter-brudd-v1.png), [diff](TESTRESULT.md#diff) |
| 6. Skeleton-/CellConfiguration-JSON, eller tydelig mockup-forklaring | **Levert:** begge JSON-filer og HTML-renderer med eksplisitte rendererbegrensninger. WP10 tester «etter»-factory mot JSON. Porthole-substitusjon/navigasjon er fortsatt uverifisert. | [Før-JSON](skeleton/tillitspakke-for.json), [etter-JSON](skeleton/tillitspakke-etter.json), [README](images/README.md), [diff](TESTRESULT.md#diff) |
| 7. Pakke-cellekontrakt: keypaths, skjema, positive/negative fixtures og Book-kopi | **Levert:** byteidentiske Book-/PDD-kontrakter, seks deklarerte GET og ti SET, positive/negative fixtures. Kilde-/journalbegrensninger er eksplisitte. | [Book-kontrakt](../../Book/agent_trust_package_contract_v0.json), [PDD-kontrakt](contract/agent_trust_package_contract_v0.json), [docs](#docs) |
| 8. Generert fixture-pakke med digest og regenerering med identisk digest | **Levert:** WP1s genererte JSON-kopi bærer beregnet digest; original-fixturen er bevart. E2e genererer fra tre runtime-celler og krever identisk digest ved regenerering og ny digest ved fjerning av ett domene. | [Generert pakke](contract/fixtures/fleet-webfetch.package.generated.json), [projeksjon](TESTRESULT.md#projeksjon), [e2e](TESTRESULT.md#e2e) |
| 9. WebFetch-whitelist/credential/lese-bare-ceiling, negative tester grønne | **Levert på testnivå:** mønstre/porter/HTTPS/GET, redirect og credential-avslag før oppslag/nettverk. E2e sender tre fetch-forsøk og bekrefter bare to transportkall. | [WebFetch](TESTRESULT.md#webfetch), [e2e](TESTRESULT.md#e2e), [full regresjon](TESTRESULT.md#regression) |
| 10. Injeksjon: modelltekst kan ikke legge til domene/credential/verktøy | **Levert på testnivå:** fire fixture-forsøk avvises, digest/ceiling/request beholdes og avvisninger telles. Ingen live leverandørkjøring. | [Injeksjon](TESTRESULT.md#injeksjon), [full regresjon](TESTRESULT.md#regression) |
| 11. Diff planlagt/observert over syntetiske kvitteringer, brudd synlig | **Levert på testnivå:** WP10 krever to typede avvik i sjufixturen; WP13 krever nøyaktig ett `new_destination`, tre effekter og to innenfor fra ekte WebFetch-utstedelse over fixture-transport. Avviket er et nektet forsøk. | [Diff](TESTRESULT.md#diff), [e2e](TESTRESULT.md#e2e) |
| 12. Signert ActionDecisionReceipt: verify OK, manipulert feiler | **Levert på testnivå:** WP9-modelltester og WP9b-celleutstedelse; full regresjon omfatter dem. E2e verifiserer forberedelsens AI-kvittering og alle tre WebFetch-kvitteringer med offentlig identitet, og avviser endret pakkedigest. | [Kvittering](TESTRESULT.md#receipt), [e2e](TESTRESULT.md#e2e), [full regresjon](TESTRESULT.md#regression) |
| 13. Kjørende cell:///AgentTrustPackage, nåbar «før»-flate i Porthole/Binding, ≤5 s ×3 | **Ikke levert / ikke verifisert.** Cellen er kjørt i XCTest. WP11 stoppet ved det senere rettede filantallskriteriet; ingen oppstart, screenshots eller tre lastetider finnes i WP11-resultatet. WP13 utfører ikke WP11. | [WP11-historikk](STATUS.md), [paritetsstatus](#parity), [e2e-avgrensning](TESTRESULT.md#e2e) |
| 14. Dataflyt: pakke ↔ EntityAnchor / AIGateway / WebFetch / ScopedCredential / receipts | **Fil levert, runtime-dekning avgrenset:** E1–E10 er deklarert med kontraktpekere. E3 har dokumenterte manglende PurposeBound-rute-/instruksjonskilder; E10 er ikke bevist i en kjørende renderer. WP13 verifiserer generering, godkjenning, WebFetch og kvitteringssamling. | [Dataflyt](dataflow.md), [kanttabell](PLAN.md#dataflow), [Book-kildegrenser](../../Book/36_Agent_Trust_Package.md), [e2e](TESTRESULT.md#e2e) |

## Paritet <a id="parity"></a>

**WP11, 2026-09-09: blocked / ikke levert.** Den rettede forhåndssjekken bestod: begge navngitte filer finnes og CellScaffold står på `pdd/tillitspakke-agentflaate`; filantall er ikke kontrollert. Ett lokalt oppstartsforsøk avsluttet med exit 133 og `CellBase.CellStoragePathPolicy.Violation.outsideStorageRoot`. Se [kommando, råfeil og køblokkering](TESTRESULT.md#parity). Ingen faktisk screenshot er tatt, og lastetid ≤5 s ×3 er ikke målt. Dette er en oppstartsblokkering, ikke et påvist rendereravvik. Binding er ikke kjørt i denne WP11-slicen. G3 venter fortsatt.

Referanse og faktisk opptak er stilt side om side i tabellen. «Ikke tatt» betyr at det ikke finnes et runtime-bilde å sammenligne med; mockups brukes ikke som faktisk evidens.

| Godkjent referanse | Faktisk Porthole-opptak i `images/actual/` | Paritet |
| --- | --- | --- |
| [Før, tom](images/tillitspakke-for-tom-v1.png) | Ikke tatt — oppstart blokkert | Ikke verifisert |
| [Før, fylt](images/tillitspakke-for-fylt-v1.png) | Ikke tatt — oppstart blokkert | Ikke verifisert |
| [Før, feil](images/tillitspakke-for-feil-v1.png) | Ikke tatt — oppstart blokkert | Ikke verifisert |
| [Etter, OK](images/tillitspakke-etter-ok-v1.png) | Ikke tatt — oppstart blokkert | Ikke verifisert |
| [Etter, brudd](images/tillitspakke-etter-brudd-v1.png) | Ikke tatt — oppstart blokkert | Ikke verifisert |
| [Før, fylt, skrivebord](images/tillitspakke-for-fylt-desktop-v1.png) | Ikke tatt — oppstart blokkert | Ikke verifisert |
| [Etter, brudd, skrivebord](images/tillitspakke-etter-brudd-desktop-v1.png) | Ikke tatt — oppstart blokkert | Ikke verifisert |

Ved neste kjøring gjelder begrensningene i [images/README.md](images/README.md): rekkevidde er lister, `tp-*`-farger/monospace og store overskrifter er ikke garantert, skrivebordets to kolonner er mockup-layout, og toggle-layout bestemmes av rendereren. Ingen av disse egenskapene er kontrollert visuelt her.

Hvert `_verify_in_porthole`-punkt fra de uendrede JSON-filene:

| Flate / punkt | Det som må bekreftes eller avkreftes | Resultat og evidens |
| --- | --- | --- |
| Før 1 | Button i List-rad sender radens `$id` som `cellID` | **blocked / uverifisert** — ingen Porthole-handling kjørt |
| Før 2 | Toggle skriver bool; cellen mottar `{isOn}` | **blocked / uverifisert** — ingen set-payload observert |
| Før 3 | TextArea med sourceKeypath/targetKeypath på samme celle kan submitte uten submitOnEnter | **blocked / uverifisert** — ingen submit kjørt |
| Før 4 | `$packageDigest` i Button-payload erstattes av fabrikken ved bygging, ikke i runtime | **blocked / uverifisert i Porthole** — ingen aktiv konfigurasjon/payload observert |
| Før 5 | Item-scoped visibility leser radens hasInstruction/hasModel og viser/skjuler riktig | **blocked / uverifisert** — ingen rader rendret eller undersøkt |
| Etter 1 | Button i List-rad sender radens `$id` som `receiptID` | **blocked / uverifisert** — ingen Porthole-handling kjørt |
| Etter 2 | Begge HStack-knappene under listen når sine keypaths | **blocked / uverifisert** — ingen audit eller dynamiske klikk kjørt |

## Veier inn <a id="ways-in"></a>

**WP11, 2026-09-09: blocked.** SkeletonReachabilityAudit er ikke kjørt på de to flatene etter den mislykkede oppstarten; `reachableActionKeypaths` er **ikke målt**, ikke et tomt resultat. Dynamiske brukerhandlinger og inngangen via `cell:///AgentTrustPackage` er ikke verifisert i Porthole. Tidligere API-/factory-tester beviser ikke rendererens payload-substitusjon, toggles, visibility eller navigasjon. [TESTRESULT#reachability](TESTRESULT.md#reachability).

| Flate | SkeletonReachabilityAudit | reachableActionKeypaths | Dynamiske handlinger |
| --- | --- | --- | --- |
| `tillitspakke-for.json` | Ikke kjørt | Ikke målt | Ikke kjørt |
| `tillitspakke-etter.json` | Ikke kjørt | Ikke målt | Ikke kjørt |

## Status <a id="status"></a>

- [x] `test.status-current`: én ny WP13-linje i STATUS samsvarer med ekte #e2e/#regression-resultater; G3 står fortsatt «venter». [Kontrollutdata](evidence/wp13/report-validation.json).
- [x] Forventet→faktisk-tabellen har én rad for hver av de 14 §3-leveransene; alle filreferanser finnes. Fem referansebilder er kontrollert som PNG med oppgitt oppløsning; dette er filkontroll, ikke en ny visuell godkjenning.
- [x] `test.tp.e2e`: bestått med fixture-modell både isolert og i full CellScaffold-XCTest, med én avviksrad og signaturverifisering.
- [x] `test.regression`: ingen nye røde testnavn mot WP0c; de fulle bundlene er fortsatt røde på kjente navn. [Resultater og alle navn](TESTRESULT.md#regression).
- [ ] WP11: Porthole-/Binding-paritet, faktiske brukerhandlinger og ≤5 s ×3 er ikke levert/verifisert.
- [ ] G3: krever Kjetils eksplisitte akseptanse; WP13 gir ikke portgodkjenning.
