# Scaffold-vert som installasjonskonfigurasjon — 2026-09-29

**Status: committet WIP-kandidat; full bygg- og testverifikasjon er blokkert av diskporten. Ingen push eller deploy.**

## Mål

Installasjonen skal kunne velge scaffold uten nytt bygg, og en operatør skal kunne
observere hvilken verdi prosessen faktisk bruker. Staging skal være standard.
Swarm er en separat tjeneste-/audience-rolle. Endringen skal ikke flytte noe til prod.

| Delmål | Observerbart suksessignal | Verifikator |
| --- | --- | --- |
| Ett instansvalg ved installasjon | Samme binær velger ny vert etter filendring og omstart | Fil-/restarttest og separat prosess med custom origin |
| Virksom standard | Ingen konfigurasjon gir staging i alle standardkonsumenter | Konfigurasjonstest og konsumenttester |
| Se kjøretid | PID, innlesingstid, kilde og effektive rolleendepunkter samsvarer med konsumentene | Binding runtime-fil, server /health/instance |
| Bevare rollegrenser | Endret scaffold flytter ikke swarm-audience eller gir issuer-rettigheter | Rolle-/avvisningstester og diffkontroll |
| Ingen ny regresjon | Baseline og kandidat har samme gamle feil, ingen nye | Full før/etter-kjøring, foreløpig blokkert |

Formålsreferanser: `purpose://quality.build-and-regression`,
`purpose://quality.docs-in-same-change` og kandidat
`purpose://candidate.scaffold-instance.installation-selects-and-observes`.
Bestillingen gir eksplisitt arbeidsmandat og kriterier. Ingen separat G3-aksept er påstått.

## Påstander og evidens

| Påstand | Status / hva den bygger på |
| --- | --- |
| De opprinnelige HTTPS-tallene stemmer | Målt i den eksisterende arbeidskopien før kodeendringer; tabell nedenfor |
| «Det finnes ingen instanskonfigurasjon» | Delvis: ingen samlet kilde, men enkeltfunksjoner har miljøvariabler; nyere origin/main har også DeviceIngress Info.plist/build-innstillinger |
| haven.local er lokal utviklingsvert | Avkreftet for disse sju treffene: alle er schema-identifikatorer |
| Koden velger fra ett dokument og beholder en prosess-snapshot | Konfigurasjonsleseren er typekontrollert, seks XCTest-metoder passerer og to prosesslivsløp er målt. App-/Vapor-integrasjonen gjenstår |
| Appen/serveren fungerer etter endringen | **Ikke verifisert**; diskporten stopper kompilering/teststart |
| Tre Keychain-feil er gamle | Oppgitt av Kjetil, ikke reprodusert her fordi teststart er blokkert; ingen feilnavn er funnet på |
| Endringen er i prod eller pushet | Nei |

## Måling før endring

Søk i `Binding/Cells`, `Binding/Sources`, `CellScaffold/Sources` og rotens
`Binding/*.plist`, med eksakte HTTPS-prefikser:

| Vert | Målt |
| --- | ---: |
| staging | 10 + 1 teksteksempel med etterfølgende punktum |
| swarm | 2 |
| prod | 1 |
| haven.local | 7 |

`rg` var ikke installert; målingen brukte Python over Git-listede filer. Utvidet
søk tok med alle versjonerte tekstfiler i Binding og CellScaffold, også `cell://`,
`wss://`, bare vertsnavn, Xcode-prosjekt, entitlements, tester, deployment og docs.
Byggprodukter, `.git` og innebygde worktrees ble ikke tolket som appkilder.

Det finnes mange lokale endringer fra andre oppgaver. Den første målingen gjelder
arbeidskopien Kjetil henviste til. Implementasjonen ligger i separate arbeidskopier
fra oppdatert `origin/main`, derfor er noen linjenumre og enkelte produksjonsvalg
annerledes. Ingen eksisterende dirty kildefiler er overskrevet.

Fullstendige råinventarer med **alle filstier, linjenumre og matchende linjer**:

- [Binding, opprinnelig arbeidskopi](SCAFFOLD_VERT_KONFIG_2026-09-29_evidence/Binding-hosts-before.json)
- [CellScaffold, opprinnelig arbeidskopi](SCAFFOLD_VERT_KONFIG_2026-09-29_evidence/CellScaffold-hosts-before.json)
- [Binding, ren implementasjonsbase](SCAFFOLD_VERT_KONFIG_2026-09-29_evidence/Binding-implementation-base-hosts.json)
- [CellScaffold, ren implementasjonsbase](SCAFFOLD_VERT_KONFIG_2026-09-29_evidence/CellScaffold-implementation-base-hosts.json)

Inventarene er substring-kandidater: negative tester, dokumenthistorikk, subdomener
som `admin.staging…` og enkelte minifiserte linjer står også der. De er ikke alle
operativt instansvalg. Tabellene nedenfor klassifiserer de operative kildene og resten
av filene uten å gjøre slike råtreff til en påstand om aktiv konfigurasjon.

## Operative kildefiler og behandling

Linjer er fra ren implementasjonsbase med mindre filen bare finnes i første måling.

| Fil | Linjer før endring | Rolle / behandling |
| --- | --- | --- |
| `Binding/Binding.xcodeproj/project.pbxproj` | 529, 532, 607, 610 | DeviceIngress build-provenance, origin/audience og issuer-pin. Beholdt sikkerhetsbinding; runtime nekter mismatch. |
| `Binding/Binding/AgentConversationClient.swift` | 10 | Standard for AgentConversationInbox → konfigurasjonens agentrolle. |
| `Binding/Binding/Binding-iOS.entitlements` | 9, 10 | Signerte Apple Associated Domains, beholdt. Ikke servervalg. |
| `Binding/Binding/Binding.entitlements` | 17, 18 | Signerte Apple Associated Domains, beholdt. Ikke servervalg. |
| `Binding/Binding/BootstrapView.swift` | 2932, 11087, 11088, 11105, 11475 | AI-gateway, launcher og tillatte IdentityLink-audiences/origins → valgt scaffold. |
| `Binding/Binding/CellConfigurationEndpointRetargeting.swift` | 232 | Retarget/fallback matcher valgt scaffold; eksplisitte eksterne referanser beholdes. |
| `Binding/Binding/ChatWorkbenchParityCells.swift` | 1341 | Treff i lokal dirty arbeidskopi; origin/main har ikke dette samme hardkodede uttrykket. |
| `Binding/Binding/ContentView.swift` | 585 | Katalog, broregistrering og standardendepunkter → valgt scaffold. |
| `Binding/Binding/DeviceCallbackCapabilityContract.swift` | 25, 26 | Fantes i opprinnelig arbeidskopi; erstattet av DeviceIngress i implementasjonsbasen. |
| `Binding/Binding/DeviceIngressRolloutPolicy.swift` | 13, 15, 24, 26 | Beholdt eksakt staging/production-sikkerhetspolicy. Ikke instansvelger. current() avviser mismatch mot aktiv instans. |
| `Binding/Binding/IdentityLinkFlow.swift` | 79 | Kun installasjonens valgte HTTPS-vert er normalt betrodd; utviklings-loopback og øvrige proof-sjekker uendret. |
| `Binding/Binding/IdentityLinkNearby.swift` | 114, 115 | To eksplisitte lenker merket Produksjon/Staging; endrer ikke instanskonfigurasjonen. Beholdt. |
| `Binding/Binding/IdentityLinkUIFixture.swift` | 34, 36, 37 | Debug/UI-testbillett, beholdt som fixture. |
| `Binding/Binding/NotificationCallbackClient.swift` | 9 | Opprinnelig standard-HTTP-adresse; implementasjonsbasen bruker pinnet DeviceIngress. |
| `Binding/Binding/RemoteCatalogSupport.swift` | 11 | Katalog/brovertsjekker og offentlig parity-fixture → valgt scaffold. |
| `Binding/Binding/WorkflowStudioSupport.swift` | 97 | AIGateway-standard → valgt scaffold. |
| `Binding/Cells/AgentEnrollmentCell.swift` | 304 | Standard scaffoldDomain → valgt scaffold. |
| `Binding/Cells/AgentProvisioningCell.swift` | 258 | Standard domain → valgt scaffold. |
| `Binding/Cells/ConfigurationCatalogCell.swift` | 64, 72, 74, 5440, 5985, 6043, 6062, 6080, 6097, 6237, 6275, 6347, 6507, 6523, 6539, 6554, 6860, 6873, 6886, 6899, 6912, 6925, 6938, 6951, 6964, 6977, 6990, 7003, 7016, 7029, 7042, 7077, 7093, 7109, 7127, 7319, 7321, 7323, 7325, 7331, 7333, 7351, 7355, 7359, 7372, 7387, 7389, 7396, 7404, 7421, 7839, 7847, 8541, 8566, 8622, 8638, 8686, 8760, 11351 | Genererte cell-referanser, universalLink og spesialisering → valgt scaffold; Release standard følger også staging. |
| `Binding/Cells/EntityScaffoldExtensionCell.swift` | 228 | Hjelpeteksteksempel → aktiv origin. |
| `Binding/Cells/InvitationCell.swift` | 79, 83 | Nye invitasjoner → valgt origin, ingen automatisk prod/staging-reserve. Lagrede billetter beholder utstedelsesvert. |
| `Binding/Cells/PalazzoConciergeMenuConfiguration.swift` | 20, 80, 89 | Egen concierge-rolle i dokumentet; discovery og faktisk referanse samsvarer. |
| `CellScaffold/Sources/App/Cells/Admin/AdminFundingCell.swift` | 120 | Eksakt prod-allowlist for live-betaling; beholdt, aldri flyttet med instansvalg. |
| `CellScaffold/Sources/App/Cells/PersonalCopilot/PersonalCopilotCloudStore.swift` | 8723 | Delingslenker → snapshot; gamle public-base-varianter kan ikke overstyre det. |
| `CellScaffold/Sources/App/Cells/PersonalCopilot/PersonalCopilotConfigurationFactory.swift` | 967 | Universal links → snapshot. |
| `CellScaffold/Sources/App/Cells/SkeletonParity/SkeletonParityFixtureCells.swift` | 383, 384, 385 | Kjørbare eksempelruter → snapshot for cell/HTTP/WSS. |
| `CellScaffold/Sources/App/Cells/SwarmIdentityAdmission/SwarmIdentityAdmissionCell.swift` | 312, 626 | Observer-VC audience og /swarm/cells → egen swarmOrigin. Ny swarmBaseURL; stagingBaseURL beholdt som wire-alias. |
| `CellScaffold/Sources/App/Cells/WorkbenchAccess/WorkbenchAccessGrantCell.swift` | 2236 | Access-invitasjonslenker → snapshot. |
| `CellScaffold/Sources/App/Resources/ProjectControl/HAVEN_Workbench_Seed_2026-06-11.json` | 516, 749, 990 | Datert Workbench-kildebevis og doneWhen-tekst, ikke operativ klientadresse; beholdt. |
| `CellScaffold/Sources/App/Services/PalazzoConciergeRemoteService.swift` | 46, 63 | Concierge-standard → egen rolle fra snapshot; eksisterende rute/timeout/transportpolicy beholdes. |
| `CellScaffold/Sources/App/Support/AgentActionCapabilityCatalogV1.swift` | 90 | haven.local er JSON Schema $id; beholdt. |
| `CellScaffold/Sources/App/Support/EntityAnchorDataV1Contract.swift` | 88, 628, 643, 658, 673, 687 | haven.local er $id og fem Sprout schema-ID-er; beholdt. |
| `CellScaffold/Sources/App/Support/ExactStagingDeviceIngressPilot.swift` | 40, 41 | Eksakt staging-pilotgrense; beholdt. |
| `CellScaffold/Sources/App/Support/ScaffoldAdministratorProvisioner.swift` | 47, 48, 53, 54 | Navngitte admin-provisioneringsprofiler for staging/prod; beholdt som separate roller/policy. |
| `CellScaffold/Sources/App/configure.swift` | 622, 623 | Eksakt staging manifest-bypass er en sikkerhetsgrense; beholdt. Ny oppstartsdiagnostikk viser aktiv konfigurasjon. |

## haven.local

`AgentActionCapabilityCatalogV1.swift:90` er JSON Schema `$id`.
`EntityAnchorDataV1Contract.swift:88` er `$id`; linjene 628, 643, 658, 673 og 687
identifiserer Sprouts EntityAnchorSnapshot, EntityLinkContract,
EntityInclusionProof, CrossScaffoldEntityContinuityProof og EntityAdmissionContract.
De hentes ikke som nettverksadresser av disse uttrykkene. De er beholdt byte-for-byte.

Gjenbrukbar læring: skill instansadresser, schema-ID-er, historisk proveniens og
faste sikkerhetsgrenser før erstatning. En staging-bypass må aldri utvides til en
vilkårlig konfigurerbar vert ved en tekstlig masseerstatning.

## Valgt form og installasjon

Ett JSON-dokument, lest én gang ved prosessstart til `ScaffoldInstanceSnapshot.current`.
Den Foundation-baserte leseren finnes identisk i Binding og CellScaffold, med en
kryssrepo bytekontroll. Dette er appinstallasjonspolicy og legges ikke i CellProtocol.
`.xcconfig`/Info.plist alene løser ikke installasjonskravet fordi de normalt er bakt
inn i det signerte bygget. En konfigcelle ville krevd bootstrap/ruting før instansvalget.

Standardfilen er Foundation user Application Support + `HAVEN/instance.json`.
`HAVEN_INSTANCE_CONFIG` kan velge en absolutt, lesbar fil ved tjenesteinstallasjon.
På administrert iOS støttes samme dokumentform via `HAVENInstanceConfiguration` i
MDM-konfigurasjonen. To eksplisitte kilder samtidig avvises. MDM-enhetslevering er
ikke testet her. Uadministrert iOS får ingen ny konfigurasjonseditor i denne oppgaven.

```json
{
  "scaffoldOrigin": "https://staging.haven.digipomps.org",
  "swarmOrigin": "https://swarm.haven.digipomps.org"
}
```

Manglende **standardfil** gir staging; en eksplisitt manglende fil eller ugyldig
verdi gir oppstartsfeil, aldri skjult fallback. HTTPS DNS-origin på port 443 støttes;
path, query, fragment, credentials og egendefinert port avvises fordi dagens
Cell-host-/audience-kontrakt er vertsbasert. Omstart, ikke rebuild, tar i bruk endring.

AgentConversation og Palazzo har valgfrie egne rolleendepunkter i samme dokument.
`catalogEndpoints` samler Binding-katalogkildene og erstatter de konkurrerende
`BINDING_*REMOTE_CATALOG*`-standardvalgene. `[]` velger bort remote bootstrap.
Fullt skjema, migrering av eldre miljøvariabler, konkrete installasjonssteder og
server-/Mac-/MDM-fremgangsmåte står i `Binding/Documentation/ScaffoldInstanceConfiguration.md`
og `CellScaffold/Documentation/ScaffoldInstanceConfiguration.md` på grenen.
Motstridende eldre miljøvariabler avvises; den valgte snapshoten setter de gamle
public-base-variablene for delte navigasjonskonsumenter.

Apple beskriver UserDefaults-baserte MDMv1-konfigurasjoner som en støttet
bakoverkompatibel mekanisme i [Configuring managed apps and extensions](https://developer.apple.com/documentation/devicemanagement/configuring-managed-apps-and-extensions).

## Faktisk kjøretid

Binding skriver `HAVEN/instance-runtime.json` i appens Application Support ved
oppstart. Den viser innleste verdier, egne rolleendepunkter, kilde, PID og tidspunkt.
PID må bekreftes levende; en gammel fil er ikke bevis for en kjørende app.
Oppstartsloggen viser også aktiv origin og kilde.

Serverens `GET /health/instance` returnerer samme uforanderlige snapshot som
konsumentene leser, inkludert PID og tidspunkt; lokal filsti redigeres bort fra
HTTP-svaret. Den eksakte read-only-ruten er tilgjengelig også når runtime admission
er utilgjengelig. Endring av inputfil mens prosessen kjører endrer ikke rapporten.

En isolert kjøring av den faktiske Foundation-leseren er målt: første prosess beholdt
`https://first.example.test` etter filendring; en ny prosess tok i bruk
`https://second.example.test`. PID-er, kildehash og resultat står i
[leserloggen](SCAFFOLD_VERT_KONFIG_2026-09-29_evidence/foundation-reader-tests.log).
Dette bruker Swift-interpreteren med uendret produksjonskilde, ikke et nytt appbygg.

**Binding-appens og Vapor-serverens integrerte kjøretid er ikke verifisert.**
Ingen installert app eller fjernserver er omkonfigurert i denne oppgaven.

## Avgrensninger og sikkerhetsroller

- Swarm er observer-VC-audience og `/swarm/cells`; `swarmOrigin` velges uavhengig.
  Feltet `stagingBaseURL` beholdes som kompatibilitetsalias, og `swarmBaseURL` navngir rollen.
- Staging/production-allowlists for manifest-bypass, DeviceIngress-pilot,
  admin-provisionering og live-betaling er faste sikkerhetsregler. De følger ikke
  den valgte URL-en. Ingen signatur-, issuer- eller owner-sjekk er svekket.
- DeviceIngress beholder pin/rollout-betingelsene og avviser mismatch mot aktiv
  instans. Det er ikke lovet at et nytt domene automatisk får enrollment-rettigheter.
- Associated Domains i Apple-entitlements er signerte deklarasjoner. Et nytt
  Universal Link/webcredentials-domene krever separat provisioning; selve
  HTTPS/Cell-instansvalget gjør ikke dette.
- Eksplisitte brukerreferanser, lagrede invitasjoner og signerte credentials flyttes
  ikke. Ny standard retargeter ikke historiske billetter eller private data.
- De daterte Workbench-kildehenvisningene og bevis i docs endres ikke som om historien
  hadde brukt en annen vert. Ingen prod-aktivering, push eller deploy er gjort.

## Baseline før og etter

| Kjøring | Resultat |
| --- | --- |
| Første forsøk fra eksisterende lokale revisjoner | Dependency resolution stoppet: lokal CellProtocol krevde swift-crypto 4.5.2, lokal DiMyMint krevde 3.x. Ingen tester kjørt. Logg beholdt. |
| Ren origin/main-base med egne avhengighetsworktrees fra manifestets 2026.9.3-tagger | Build capacity: 54,9 GiB ledig; reserve 10 GiB → 44,9 GiB / 4 %. Eksisterende gate krever minst 40 GiB **og** 5 %. Exit 75 før Swift/teststart. |
| Kandidatens fulle Swift/Xcode-testløp | Ikke kjørt mens samme diskblokkering består. Siste gate: 55,7 GiB → 45,7 GiB / 4 %, exit 75. |
| Statisk Swift-syntaks | Siste pass: 36 filer, 0 parse-feil; kildehash per fil står i swift-syntax-only.json. Dette er ikke appkompilering. |
| Konfigurasjonsleser: Swift-typekontroll | Passerte også med `-default-isolation MainActor`, som Binding bruker. |
| Konfigurasjonsleser: isolerte XCTest-metoder | **6 kjørt, 0 feil**; ingen Keychain-/nettverksavhengighet. |
| Konfigurasjonsleser: filendring og ny prosess | **PASS**; prosessen beholdt sin snapshot, ny PID tok ny verdi, swarm forble uavhengig. |
| Kontraktskontroll | Identiske leserfiler og ingen nye hardkodede operasjonelle velgere utenfor oppgitte policyfiler. |
| Keychain-baseline, før/etter | Ikke målt; Kjetils tre oppgitte EPERM/-25291-feil er ikke brukt som stopgrunn og ikke oppgitt som observert her. |

Loggene ligger i [evidence](SCAFFOLD_VERT_KONFIG_2026-09-29_evidence/).
`CLANG_MODULE_CACHE_PATH` og `SWIFTPM_MODULECACHE_OVERRIDE` var satt til skrivbar
`/private/tmp/scaffold-instance-module-cache` før forsøket. Runneren setter dem videre
til sin administrerte cache. `--disable-sandbox`, `--jobs 4` og
`SWIFTPM_MAX_CONCURRENT_OPERATIONS=1` ble brukt. Nettverk/fetch virket.

Lesertesten fant først én ny feil: Foundation leverte fraværende fil som `NSError`
i `NSCocoaErrorDomain` kode 260, ikke som en vellykket `as CocoaError`-cast. Dette er
rettet ved eksakt domain/code-sjekk; de seks lesertestene er kjørt grønne etter rettingen.
Alle nye app-/HTTP-konsumenttester finnes, men er ikke påstått kjørt.

Det er bedt om minst 5 GiB frigjort plass. Ingen cache slettes og ingen diskgrense
senkes. Før godkjenning må ren base testes, deretter kandidaten med samme pakker,
og de faktiske feilede testnavnene sammenlignes. Nye røde tester skal undersøkes;
kjente gamle Keychain-feil stopper ikke arbeidet. Separate konsumenttester skal også
kjøres med en alternativ **testvert**, aldri prod.

## Gren og revisjoner

Gren i alle tre leveranserepoer: `codex/scaffold-instance-config-20260929`. Arbeidskopier under `.scaffold-instance-20260929/`.

| Repo | Base | Leveransecommit |
| --- | --- | --- |
| Binding | `8ce634f6533f5e63386229639c69c43aac25c31f` | `f2acd47bc47fed717cc145cfb4a892aaeda8322c` (WIP, full regresjon venter) |
| CellScaffold | `fdf1ce8e1713ac467ebca1e44707225175e72dc4` | `231fa07e2abc68d33898b51f368d6e15c52f49db` (WIP, full regresjon venter) |
| CellProtocolDocuments | `61490b81a70abe52e7d48182c0c79b391f3dd3e1` | Rapport-/evidence-commit på samme gren; hash oppgis i overleveringen. |

Avhengigheter brukt til planlagt ren baseline:

- `CellProtocol` tag `2026.9.3`, `9c60001ac53abc35ba7ad6e2c0efa2a79ab2a366`.
- `DiMyMint` tag `2026.9.3`, `2dcefac5c21a0b54e4e8677452d591b6169c2057`.
- `DiMyMicropayments` tag `2026.9.3`, `aa3d10d17b90f692e50343232961c3dfd8a66323`.

Opprinnelige git-statuser ligger i evidence. De var omfattende og beholdes urørt.
En historisk tekstfil manglet ved opprettelse av den nye CellScaffold-worktreen
(årsaken er ikke fastslått). Den ble gjenopprettet byte-for-byte fra HEAD før commit;
leveranseworktree har ingen slik sletting.

## Alle øvrige filer med vertskandidater

Disse er med i råinventarene og ikke glemt. Tester/fixtures beholder eksplisitte
forventningsverter; scripts/deployment er egne navngitte operatørkonfigurasjoner;
rapport-/dokumenthistorikk er proveniens. HavenAgentD er et separat agent-runtime
med egne tjenesteendepunkter, ikke Binding-appens scaffold-bootstrap.

| Repo / fil | Linjer i ren base |
| --- | --- |
| `Binding/BindingTests/AgentConversationClientTests.swift` | 119, 126 |
| `Binding/BindingTests/AppStoreMetadataTests.swift` | 65, 68, 72 |
| `Binding/BindingTests/BindingTests.swift` | 873, 874, 875, 876, 877, 878, 1298, 1305, 1330, 1357, 1369, 1401, 1776, 1777, 1778, 1779, 1780, 1781, 1782, 1783, 1784, 1785, 1786, 1787, 1788, 1789, 1837, 1838, 1839, 1849, 1948, 1964, 1965, 1966, 1973, 2002, 2007, 2012, 2017, 2022, 2041, 2045, 2053, 2058, 2064, 2068, 2076, 2077, 2089, 2115, 2116, 2129, 2130, 2146, 2147, 2152, 2153, 2159, 2160, 2162, 2174, 2177, 2182, 2195, 2196, 2202, 2221, 2225, 2235, 2236, 2244, 2282, 2296, 2307, 2323, 2333, 2350, 2509, 2566, 2590, 2593, 2685, 2696, 2704, 2709, 2831, 2840, 2843, 3420, 3422, 3596, 3599, 3602, 3660, 3662, 3668, 3670, 3676, 3678, 3684, 3686, 3692, 3694, 3700, 3702, 3708, 3710, 3716, 3718, 3724, 3726, 3736, 3739, 3744, 3745, 3892, 3903, 3914, 3915, 3966, 3972, 3981, 4039, 4040, 4045, 4097, 4220, 4221, 4225, 4226, 4227, 4228, 4233, 4248, 4264, 4300, 4313, 4411, 5224, 5261, 7636, 7639 |
| `Binding/BindingTests/CellConfigurationVerifierXCTest.swift` | 1219, 2601, 2756, 2869, 2889, 2952, 3018, 3061, 3067, 3648, 3660, 3666 |
| `Binding/BindingTests/DeviceIngressRegistrationClientTests.swift` | 10, 133, 167, 1150, 1151, 1156, 1157, 1174, 1182, 1183, 1231, 1232, 1239, 1240, 1269, 1289, 1319, 1334 |
| `Binding/BindingTests/IdentityLinkFlowTests.swift` | 13, 18, 30, 34, 40, 49, 53, 73, 92, 135, 158, 186, 198, 236, 277, 306, 382, 385, 390 |
| `Binding/BindingTests/InvitationResidencyTests.swift` | 47, 216, 465, 480, 498 |
| `Binding/BindingTests/NotificationCallbackClientTests.swift` | 78, 112, 288, 306, 349, 359, 362 |
| `Binding/BindingTests/NotificationEnrollmentManagerTests.swift` | 259, 260 |
| `Binding/BindingTests/PersonEntityReadClientTests.swift` | 191 |
| `Binding/BindingTests/PersonEntityReadTLSIntegrationTests.swift` | 35, 136 |
| `Binding/BindingTests/RemoteSurfaceRenderAuditXCTest.swift` | 309 |
| `Binding/BindingTests/SkeletonParityRemoteXCTest.swift` | 51, 55, 59, 64, 69, 73, 77, 81, 86, 95, 100, 105, 110, 421, 422, 423, 491, 688, 689, 1160, 1309 |
| `Binding/BindingUITests/BindingUITests.swift` | 35 |
| `Binding/Documentation/BindingP0UtilityCellsImplementationNote.md` | 78 |
| `Binding/Documentation/CellScaffoldConferenceAdminPreviewStagingHandoff.md` | 31 |
| `Binding/Documentation/ComponentDragDropPlan.md` | 332 |
| `Binding/Documentation/ConferenceAIAssistantRootCause-2026-04-03.md` | 52 |
| `Binding/Documentation/ConferenceConfigurationVerifier.md` | 56 |
| `Binding/Documentation/ConferenceDebugPlaybook.md` | 92, 209, 214, 254 |
| `Binding/Documentation/CrossVaultIdentityEnrollment.md` | 242, 293, 294 |
| `Binding/Documentation/DeviceCallbackCapabilityContract.md` | 163, 164, 168 |
| `Binding/Documentation/HAVEN_Perspective_Entities_and_Invite_Landing_2026-08-21.md` | 335 |
| `Binding/Documentation/HAVEN_Relations_Invite_and_Residency_2026-08-20.md` | 140, 215 |
| `Binding/Documentation/HavenAgentPhoneApprovalLoopRunbook.md` | 90, 97, 127, 128, 129, 429, 432, 493, 496 |
| `Binding/Documentation/PersonalCopilotV1AppStoreImplementation.md` | 10 |
| `Binding/Documentation/Porthole-and-skeleton.md` | 56, 70, 103, 104, 110 |
| `Binding/Documentation/ScaffoldChat.md` | 11 |
| `Binding/Documentation/SkeletonParitySuite.md` | 32, 148 |
| `Binding/Documentation/StagingResourceLocations.md` | 78, 112, 135, 168, 175, 208, 230 |
| `Binding/Documentation/TestData/HavenAgentD/registration-observation-v1.schema.json` | 2 |
| `Binding/Documentation/TestData/IdentityLinking/IdentityEnrollmentRequest.example.json` | 24 |
| `Binding/Documentation/TestData/IdentityLinking/SameEntityIdentityLinkCredential.example.json` | 4 |
| `Binding/Documentation/TestData/IdentityLinking/SameEntityIdentityLinkPresentation.example.json` | 4, 16, 72 |
| `Binding/Scripts/build_binding_staging_candidate.sh` | 217, 218 |
| `Binding/Tests/fixtures/personal_chat_prompt_evaluation.json` | 926, 932 |
| `CellScaffold/.claude/skills/cellconfiguration-skeleton-authoring/references/runtime-publishing.md` | 48, 61, 71 |
| `CellScaffold/.claude/skills/haven-functional-service-verification/references/porthole-demo-testing.md` | 98, 99 |
| `CellScaffold/.claude/skills/haven-functional-service-verification/references/staging-verification.md` | 23, 35, 36, 43, 44, 51 |
| `CellScaffold/.claude/skills/haven-gui-testing/references/playwright-runner-patterns.md` | 14, 15, 30, 31, 40 |
| `CellScaffold/Deliverables/PDD_entitetslenking-paa-tvers-av-scaffolds_2026-09-04/contract/identity-link-rendezvous.v1.md` | 18, 20 |
| `CellScaffold/Deliverables/PDD_entitetslenking-paa-tvers-av-scaffolds_2026-09-04/handoff/README.md` | 31, 34 |
| `CellScaffold/Deployment/admin-scaffold.env.example` | 7 |
| `CellScaffold/Deployment/monitoring/admin-scaffold/prometheus.yml.template` | 34 |
| `CellScaffold/Deployment/nginx/admin-scaffold-staging.conf` | 10, 16, 23, 25, 26 |
| `CellScaffold/Documentation/AIModelRuns/conference-ui-debate-2026-06-09T19-53-22-313Z.md` | 4 |
| `CellScaffold/Documentation/AIModelRuns/conference-ui-debate-2026-06-09T20-18-45-993Z.md` | 4 |
| `CellScaffold/Documentation/AdminScaffold_M4_Runbook.md` | 47, 81, 126 |
| `CellScaffold/Documentation/AdminScaffold_Production_Provisioning_Evaluation_2026-07-17.md` | 13, 23, 24, 79 |
| `CellScaffold/Documentation/AdminScaffold_Secret_Provisioning.md` | 3, 46, 52 |
| `CellScaffold/Documentation/Admin_Entity_Access_Continuity_2026-07-18.md` | 100, 102, 103 |
| `CellScaffold/Documentation/Arendalsuka_Maturity_Assessment_2026-07-20.md` | 5 |
| `CellScaffold/Documentation/Arendalsuka_Readiness_Evaluation_2026-07-18.md` | 12, 31 |
| `CellScaffold/Documentation/ClaudeSkills/desktop-src/cellconfiguration-skeleton-authoring/references/runtime-publishing.md` | 45, 58, 68 |
| `CellScaffold/Documentation/ClaudeSkills/desktop-src/haven-functional-service-verification/references/porthole-demo-testing.md` | 102, 103 |
| `CellScaffold/Documentation/ClaudeSkills/desktop-src/haven-functional-service-verification/references/staging-verification.md` | 27, 39, 40, 47, 48, 55 |
| `CellScaffold/Documentation/ClaudeSkills/desktop-src/haven-gui-testing/references/playwright-runner-patterns.md` | 18, 19, 34, 35, 44 |
| `CellScaffold/Documentation/Codex_Handoff_Social_Growth_Arendalsuka_2026-08-03.md` | 7, 104, 110, 114, 259 |
| `CellScaffold/Documentation/Conference_Demo_Story.md` | 49 |
| `CellScaffold/Documentation/Conference_Playwright_Smoke.md` | 94 |
| `CellScaffold/Documentation/ConfigurationCatalog/runtime-publishing-targets.json` | 8 |
| `CellScaffold/Documentation/Kallimachos_Arendalsuka_Server_AI_Demo_Runbook_2026-08-08.md` | 184 |
| `CellScaffold/Documentation/Losningsforslag/Palazzo_Communale_Service_Surface_Production_Handoff_2026-07-17.md` | 24, 108, 194, 195, 196 |
| `CellScaffold/Documentation/Native_Linux_Deployment.md` | 189, 190 |
| `CellScaffold/Documentation/Operations/Admin_Overview_Remote_Cell_Diagnose_2026-08-09.md` | 14, 17, 18, 19, 28, 53, 54, 55, 56, 57, 226, 271, 276, 283 |
| `CellScaffold/Documentation/Operations/CellScaffold_Deployment_Workflow.md` | 175, 176, 177, 178, 179 |
| `CellScaffold/Documentation/Operations/CellScaffold_DeviceIngress_Deploy_Handoff_2026-08-16.md` | 50, 51, 52, 113, 114, 134, 135, 136, 139, 230, 231, 242, 269 |
| `CellScaffold/Documentation/Operations/CellScaffold_DeviceIngress_Staging_Blocker_Continuation_2026-08-16.md` | 84 |
| `CellScaffold/Documentation/Operations/Deploy_Handoff_Codex_Staging_og_Prod_2026-08-31.md` | 53 |
| `CellScaffold/Documentation/Operations/Development_Admin_Release_Control_Runbook.md` | 80, 81, 82, 83, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380 |
| `CellScaffold/Documentation/Operations/HANDOFF_Funksjonalitet_til_Main_og_Deploy_2026-08-28.md` | 121 |
| `CellScaffold/Documentation/Operations/HANDOFF_PalazzoCommunaleScaffold_2026-08-25.md` | 32, 142, 281 |
| `CellScaffold/Documentation/Operations/HAVEN_Production_Domain_TLS_Nginx_and_Correspondence_Status_2026-08-03.md` | 19, 25, 29, 45, 52, 53, 54 |
| `CellScaffold/Documentation/Operations/Korrespondanse_Invitasjoner_Runbook.md` | 110, 187 |
| `CellScaffold/Documentation/Operations/Palazzo_Deploy_Admin_Handoff_2026-08-17.md` | 166, 167, 168 |
| `CellScaffold/Documentation/Operations/Palazzo_Main_Release_Freeze_2026-08-18.md` | 63 |
| `CellScaffold/Documentation/Operations/Palazzo_Release_Coordination_2026-08-18.md` | 138, 189, 216, 217, 218, 219, 220 |
| `CellScaffold/Documentation/Operations/Porthole_Surface_Load_Incident_2026-08-15.md` | 140, 141 |
| `CellScaffold/Documentation/Operations/Prod_Cutover_74c7a57f_2026-08-09.md` | 146, 284 |
| `CellScaffold/Documentation/Operations/Release_Scope_and_Production_Plan_2026-08-17.md` | 20 |
| `CellScaffold/Documentation/Operations/Server_Build_And_Cutover_Runbook.md` | 201, 223 |
| `CellScaffold/Documentation/Operations/Staging_Admin_Deploy_2026-08-09.md` | 7, 26, 27, 28, 123, 134 |
| `CellScaffold/Documentation/Operations/Staging_Surface_Test_Report_2026-08-09.md` | 3 |
| `CellScaffold/Documentation/Operations/Surface_Load_Timing_2026-08-10.md` | 60 |
| `CellScaffold/Documentation/Operations/Vegar_Arendalsuka_Runtime_Publishing_and_Messaging_Handoff_2026-07-28.md` | 143, 144, 145, 308, 332, 340 |
| `CellScaffold/Documentation/Operations/Vegar_Contact_Onboarding_Purpose_and_Trust_Plan_2026-08-10.md` | 131, 214 |
| `CellScaffold/Documentation/Operations/Vegar_Deployment_Report_2026-06-17.md` | 34, 180, 181 |
| `CellScaffold/Documentation/Operations/Work_Order_2026-08-09.md` | 159, 160, 189, 194 |
| `CellScaffold/Documentation/Operations/admin-container-transaction-20260918/deploy-admin-production.example.json` | 15 |
| `CellScaffold/Documentation/Operations/admin-container-transaction-20260918/deploy-admin-staging.example.json` | 15 |
| `CellScaffold/Documentation/Operations/admin-scaffold-production-controller-20260902/README.md` | 22 |
| `CellScaffold/Documentation/Operations/admin-workspace-not-runtime-ready-20260827/README.md` | 62 |
| `CellScaffold/Documentation/Operations/arendalsuka-public-reader-identity-20260902/README.md` | 43 |
| `CellScaffold/Documentation/Operations/assistant_handoff.md` | 358, 477, 479, 613, 614 |
| `CellScaffold/Documentation/Operations/correspondence-victoria-onboarding-20260827/Epost_til_Lille_Robot.md` | 15 |
| `CellScaffold/Documentation/Operations/natt-qa-20260903/Flateregister.md` | 13 |
| `CellScaffold/Documentation/Operations/nginx/haven_production.conf` | 9, 16, 23, 27, 28 |
| `CellScaffold/Documentation/Operations/nginx/staging_haven.conf` | 7, 61, 62, 68, 74 |
| `CellScaffold/Documentation/Operations/rich-document-20260910/README.md` | 169, 205 |
| `CellScaffold/Documentation/Operations/surface-load-reactive-20260824/README.md` | 410 |
| `CellScaffold/Documentation/Operations/workbench-1.0/WO-3-deploy-and-evidence.md` | 45, 64 |
| `CellScaffold/Documentation/Person_Entity_Native_TLS_Proof_2026-09-13.md` | 67 |
| `CellScaffold/Documentation/ProjectControl/Corr_Staging_Gate_Kommandoer_2026-08-20.md` | 152, 195, 303, 304, 305, 306 |
| `CellScaffold/Documentation/ProjectControl/HAVEN_DevTooling_Work_Intake_2026-08-19.json` | 283 |
| `CellScaffold/Documentation/ProjectControl/HAVEN_Workbench_Agent_Ritual_2026-06-09.md` | 96 |
| `CellScaffold/Documentation/ProjectControl/HAVEN_Workbench_Identity_Access_Principles_2026-06-12.md` | 25, 26 |
| `CellScaffold/Documentation/ProjectControl/HAVEN_Workbench_Seed_2026-06-11.json` | 348, 581, 822 |
| `CellScaffold/Documentation/ProjectControl/Palazzo_Release_Workbench_Seed_2026-08-18.json` | 145, 461 |
| `CellScaffold/Documentation/RAG_MVP_UI.md` | 43, 46, 47 |
| `CellScaffold/Documentation/Scaffold_Product_Split_Plan_2026-07-10.md` | 88 |
| `CellScaffold/Documentation/Skeleton_Parity_Fixture_Catalog.md` | 7, 75, 101 |
| `CellScaffold/Documentation/Staging_Deployment.md` | 18, 20, 21, 24, 32, 33, 43, 44, 264, 265, 279, 282, 291 |
| `CellScaffold/Documentation/SwarmScaffold_Architecture_2026-06-18.md` | 11, 193, 209, 222 |
| `CellScaffold/Documentation/SwarmScaffold_Staging_Runbook_2026-06-20.md` | 9, 10, 79, 84, 122, 123 |
| `CellScaffold/Documentation/SwarmScalabilityPerformanceTestDesign_2026-07-01.md` | 162, 163, 201, 202 |
| `CellScaffold/Documentation/Workbench_Modenhetsvurdering_2026-08-19.md` | 161 |
| `CellScaffold/Public/js/haven-localization.js` | 5 |
| `CellScaffold/README.md` | 44, 45, 68, 69, 79, 144, 145, 250, 295 |
| `CellScaffold/Tests/AppTests/AdminAuthenticatedVaporBridgeTransportTests.swift` | 24, 30, 31, 89, 98 |
| `CellScaffold/Tests/AppTests/AdminCatalogRoutesTests.swift` | 16, 30 |
| `CellScaffold/Tests/AppTests/AdminControlPlaneRoutingTests.swift` | 184, 195 |
| `CellScaffold/Tests/AppTests/AdminScaffoldRuntimeTests.swift` | 58, 69 |
| `CellScaffold/Tests/AppTests/AssistantCorrespondenceCellTests.swift` | 241 |
| `CellScaffold/Tests/AppTests/AssistantCorrespondenceOnboardingRoutesTests.swift` | 135, 217 |
| `CellScaffold/Tests/AppTests/DeviceCallbackCapabilityServerTests.swift` | 13, 426, 429, 434, 435 |
| `CellScaffold/Tests/AppTests/DeviceIngressCallbackRuntimeTests.swift` | 12 |
| `CellScaffold/Tests/AppTests/DeviceIngressIdentityLinkHandshakeContractTests.swift` | 37, 38, 164, 170, 171 |
| `CellScaffold/Tests/AppTests/ExactStagingDeviceIngressPilotTests.swift` | 12, 13, 20, 21, 33, 64, 65 |
| `CellScaffold/Tests/AppTests/Fixtures/ButlerBuiltIn-b4a2779a.json` | 133 |
| `CellScaffold/Tests/AppTests/Fixtures/ButlerBuiltIn-pretree.json` | 133 |
| `CellScaffold/Tests/AppTests/Fixtures/ButlerBuiltIn-prewb.json` | 133 |
| `CellScaffold/Tests/AppTests/HostRoutedBridgeTransportTests.swift` | 41, 52, 54, 58 |
| `CellScaffold/Tests/AppTests/IdentityLinkRendezvousStoreTests.swift` | 11 |
| `CellScaffold/Tests/AppTests/JWTAuthRoutesTests.swift` | 547, 548 |
| `CellScaffold/Tests/AppTests/NotificationPushProviderTests.swift` | 716, 736, 814, 1154, 1421, 1518, 1524, 1739, 1742, 1770 |
| `CellScaffold/Tests/AppTests/PalazzoCommunaleServiceTests.swift` | 264 |
| `CellScaffold/Tests/AppTests/PersonalCopilotV1Tests.swift` | 171 |
| `CellScaffold/Tests/AppTests/RAGGatewayConfigTests.swift` | 10, 11, 16, 17, 18, 24, 28, 34, 35, 41 |
| `CellScaffold/Tests/AppTests/ScaffoldAdministratorProvisionerTests.swift` | 159, 160, 282, 283, 345, 346, 349, 350 |
| `CellScaffold/Tests/AppTests/ScaffoldSetupCellTests.swift` | 64, 94, 95, 217 |
| `CellScaffold/Tests/AppTests/SproutBridgeDiscoveryRoutesTests.swift` | 19, 35, 42, 50, 52, 66, 74, 94, 102, 128, 136, 162, 171, 178, 185 |
| `CellScaffold/Tests/AppTests/SproutExecutableCatalogRoutesTests.swift` | 27, 29, 31, 42, 47, 60, 65 |
| `CellScaffold/Tests/AppTests/SproutResolverRoutesTests.swift` | 20, 33, 63, 73, 86, 103, 126, 136, 152, 175, 180, 192, 200 |
| `CellScaffold/Tools/ButlerParity/candidate_catalog.v1.json` | 264, 479, 725, 797, 879, 952, 990, 1108, 1169, 1259, 1295, 1334, 1418, 1466, 1520, 1578, 1618, 1661, 1941, 2052 |
| `CellScaffold/playwright.config.js` | 8 |
| `CellScaffold/playwright/butler-chat-mobile.spec.js` | 6 |
| `CellScaffold/playwright/butterpop-mix-tidy.spec.js` | 114 |
| `CellScaffold/playwright/conference-demo.smoke.spec.js` | 12 |
| `CellScaffold/playwright/fixtures/localization/messages.json` | 13 |
| `CellScaffold/playwright/fixtures/localization/skeleton.json` | 14 |
| `CellScaffold/playwright/mermaid-playground-direct.spec.js` | 6 |
| `CellScaffold/playwright/personal-chat-prompt.spec.js` | 9 |
| `CellScaffold/playwright/skeleton-scenarios/arendalsuka-participant-program.export.json` | 3 |
| `CellScaffold/playwright/surface-load-ladder.spec.js` | 23 |
| `CellScaffold/playwright/surface-load-timing.spec.js` | 8 |
| `CellScaffold/scripts/arendalsuka-data-health.js` | 9 |
| `CellScaffold/scripts/arendalsuka-import.js` | 393 |
| `CellScaffold/scripts/arendalsuka-issue-import-access-vc.js` | 13, 224 |
| `CellScaffold/scripts/arendalsuka-osm-import.js` | 194 |
| `CellScaffold/scripts/arendalsuka-stands-import.js` | 146 |
| `CellScaffold/scripts/cellscaffold-container-controller.py` | 274, 285, 734, 736, 738, 740, 742 |
| `CellScaffold/scripts/conference-ui-debate.js` | 20 |
| `CellScaffold/scripts/create-assistant-correspondence-pilot.py` | 166 |
| `CellScaffold/scripts/deploy-admin-staging.sh` | 27, 28 |
| `CellScaffold/scripts/deploy-staging-atomic-v3.py` | 56, 57 |
| `CellScaffold/scripts/deploy-staging.sh` | 61, 69 |
| `CellScaffold/scripts/native_person_tls_proxy.py` | 55 |
| `CellScaffold/scripts/native_person_tls_trust.sh` | 34, 58 |
| `CellScaffold/scripts/production/admin_browser_observation_relay.py` | 60, 61 |
| `CellScaffold/scripts/provision-admin-host-secrets.sh` | 45, 46 |
| `CellScaffold/scripts/provision-scaffold-administrator-production.sh` | 70, 71 |
| `CellScaffold/scripts/provision-scaffold-administrator-staging.sh` | 58, 59 |
| `CellScaffold/scripts/release-candidate-preflight.py` | 19 |
| `CellScaffold/scripts/skeleton-iterate.js` | 10 |
| `CellScaffold/scripts/staging-conference-message-acceptance.js` | 25 |
| `CellScaffold/scripts/staging-conference-self-message-acceptance.js` | 66 |
| `CellScaffold/scripts/staging-public-readiness.js` | 9 |
| `CellScaffold/scripts/tests/test_admin_browser_observation_relay.py` | 17, 18, 20 |
| `CellScaffold/scripts/tests/test_admin_scaffold_image_workflow.py` | 73 |
| `CellScaffold/scripts/tests/test_cellscaffold_container_controller.py` | 40, 41, 42, 57, 58, 302, 321, 322, 339, 340, 353, 354, 358 |
| `CellScaffold/scripts/tests/test_create_assistant_correspondence_pilot.py` | 83 |
| `CellScaffold/scripts/tests/test_deploy_staging_atomic_v3.py` | 255, 256, 257, 258, 259, 277, 278, 279, 280, 281, 297, 298, 299, 300, 301, 314, 315, 316, 317, 318, 333, 334, 335, 336, 337, 784, 785, 786, 787, 788 |
| `CellScaffold/scripts/tests/test_release_candidate_preflight.py` | 84 |
| `CellScaffold/verification/admin-topup-stripe-20260923/WORKLOG.md` | 13 |
| `CellScaffold/verification/ai-usage-20260924/SETUP.md` | 7 |

## Læringsfangst

Vertklassifisering og NSError-fallgruven er fanget, brukt i denne rapporten og
markert distribuert via Git av haven-learn. `check --strict` viste også to åpne og
seks ikke-distribuerte læringer fra andre oppgaver; disse er ikke endret eller
feilaktig lukket her. Den oppgavespesifikke læringsfangsten er fullført.
