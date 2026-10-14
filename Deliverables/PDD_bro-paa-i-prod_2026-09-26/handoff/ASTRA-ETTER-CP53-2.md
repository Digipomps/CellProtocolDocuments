STATUS: LEVERT — anbefaling: merge etter 2 rettinger, 1 nye funn (1 blokkerer)

# Astra — kontroll 2 av CellProtocol PR #53

Dato: 2026-09-27. Vurdert head: **`22d79190806f80b1d9dcb31d45e04dacd06fed22`**. Beslutningseier: Kjetil.

**Ikke merge foreliggende head. R1/N01 og R4/N04 er lukket for de identifiserte feilforløpene. R2/N02 er ikke lukket:** den nye ressursleasen frigir en reservasjon også når initialiseringens acquire feiler. Det gjør at fortsatt aktive kanaler/feeds blir undertelt. **R3/N03 står dessuten igjen.** Binding har indirekte runtime-bruk av CP-skanneren, selv om direkte `ScannerService`-treff er begrenset til tester. Det er derfor ikke grunnlag for å erklære Scanner-funksjonen ubrukt og utsette R3 uten en eksplisitt støttet funksjonsgrense.

«2 rettinger» betyr den nye R2-feilen N06 og eksisterende R3. Bare N06 telles som nytt funn; R3 telles ikke på nytt. Testpresiseringene nedenfor er vurdering av bevisstyrke, ikke ytterligere påviste kodefeil. Alle fem CI-kjøringer for head er grønne, og **de samme tre navngitte lokale Keychain-testene består i CI**.

## 1. Kildegrunnlag og hva som er kontrollert

Lest: forrige `ASTRA-ETTER-CP53.md`, særlig N01–N05, §5 og §7; implementørens `CP53-RETTINGER.md`; endringene fra `283cc3fecedcbb94505501feb24fd886c6dac763` til head og relevante omkringliggende kilder. De fire oppgitte rettingscommittene inngår i denne sammenligningen. CP-kode er lest med `git show <sha>:<fil>` og `git diff` på commitobjekter, **ikke fra det skitne hovedarbeidstreet**.

`BridgeChannelSession.swift`, `BridgeChannelTransport.swift`, `BridgeChannelClientOperation.swift`, de nye lifetime-/sequence-/process-testfilene og de supplerte testforløpene er lest. `BridgeBase.swift`, `BridgeMultiplexing.swift`, resolver, adaptere, Scanner, konsumenter og eldre testfiler er lest i de henviste utsnittene og relevante diff/søk. Øvrige deler er **ikke lest**. Dette er en avgrenset etterkontroll, ikke en ny full revisjon av alle PR-ens opprinnelige endringer.

Alle CP-henvisninger nedenfor gjelder head over, med disse prefiksene:

| Prefiks | Full bane relativt til HAVEN-roten |
|---|---|
| `B/` | `CellProtocol/Sources/CellBase/Cells/Bridging/` |
| `T/` | `CellProtocol/Tests/CellBaseTests/` |
| `CP/` | `CellProtocol/` |

Konsumenthenvisninger er uttrykkelig **ikke CP-head**: Binding-main `8ce634f6533f5e63386229639c69c43aac25c31f`, HAVEN_MVP-main `5dc692fc5e397371f32f7819e5332559442a397a`. Begge er kontrollert mot remote main med `git ls-remote`. CP-main/base er fortsatt `a6fa51a8db059c64d5171cbc8d454eea412ada9d`. Eksisterende dokumenter er lest som de foreligger i dokumentrepoet.

Jeg har ikke kjørt CP-bygg, CP-testsuite, radio-/to-enhetsprøve, belastningstest eller staging-/produksjonsprøve. Jeg har kjørt to små Swift-prober via standard input: én for throwing-init/deinit-semantikken, én med **uendret lease-klasse hentet fra head**, men en minimal sesjonsstub. Det siste er et avgrenset språk-/lease-bevis, ikke en påstått kjørt ende-til-ende-utnyttelse. Ingen kildefil ble opprettet eller endret for probene; Swift brukte modulcache under `/private/tmp`.

## 2. R1, R2 og R4

| Funn | Konklusjon | Kilde og konkret bevis |
|---|---|---|
| **N01 / R1** | **Lukket for de rapporterte get/set/sign-denial-forløpene.** | Mux-send kontrollerer nå at senderens transportobjekt er identisk med den aktive kanalpostens transport; gjenbrukt kanal-ID alene er utilstrekkelig. Gammel logisk close kontrollerer samme objekt. `B/BridgeMultiplexing.swift:1097–1123,1272–1286`. Base fanger transport ved command-inngang, og sign-avslag bruker argumentet også etter awaited audit: `B/BridgeBase.swift:1204–1225,1342–1354,1513–1587`. |
| **N02 / R2** | **Ikke lukket; ny regresjon N06.** | Lukkede poster beholdes nå til ressursene faktisk er borte, og globale operation/feed/channel/work-tak finnes. Det løser den opprinnelige «slett hele posten ved disconnect»-mekanismen. Men feilslått lease-init gjør regnskapet uriktig; se N06. `B/BridgeChannelSession.swift:30–43,105–188,372–386`. |
| **N04 / R4** | **Lukket.** | Poolen deler pending og aktiv sesjon med samme sikkerhetsbundne nøkkel, skiller terminal/utløpt tilstand og pensjonerer erstattede poster. Felles setup-feil markerer sesjonen terminal. `B/BridgeMultiplexing.swift:189–216,329–349,365–393`; `B/BridgeChannelSession.swift:331–335`. Resolverens faktiske factory lager auth-wrapperen: `CP/Sources/CellBase/Cells/CellResolver/CellResolver.swift:2312–2338`. |

R1-testen `testRetiredMultiplexGetSetAndSignDenialCannotReachReusedChannelOrCID` suspenderer faktisk alle tre varianter, gjenbruker kanal-ID og cid=7 og krever bare ny respons pluss fungerende søskenrespons. Den bruker autentisert fixture, ikke en nettverkssocket (`T/BridgeChannelTransportTests.swift:408–445`). Den fysiske varianten bruker `setTransport`/ny fixture (`:448–477`); separat sign-denial-test bruker faktisk `renewAuthenticatedChannel` og nytt håndtrykk (`:620–640`). Dette er presist nok til å lukke de opprinnelige R1-forløpene. Det er ikke et løfte om å tilbakekalle bytes som fysisk adapter allerede har akseptert; den avgrensningen er dokumentert (`CP/Docs/BridgeIdentitySecurity.md:192–201`).

R4-testen bruker åtte `CellResolver.cellAtEndpoint`-kall, holder proof suspendert, krever én fysisk instans og åtte opens med samme fingerprint, og prøver abort etterfulgt av én ny instans (`T/BridgeMultiplexingTests.swift:909–944`). Auth-klienten er virkelig resolverkode; fysisk nettverk/server er testtransport (`:143–240`). Testnavnet er rimelig. De sju ekstra kallene får 50 ms til å nå poolen, ikke en barriere som bekrefter at alle sju faktisk har nådd den (`:923–928`); dette er en mulig forbedring i determinisme, ikke et nytt funn i poolkoden.

### N06 — Høy, blokkerer merge: mislykket lease-opptak frigir en annens reservasjon

`BridgeChannelResourceLease` starter med `released = false`. Initialiseringen setter alle lagrede felter **før** `try session.acquire(resource)`. Hvis acquire kaster, blir den ferdig initialiserte klassens `deinit` kjørt. Den kaller `release()`, som nå trekker fra telleren selv om denne leasen aldri reserverte noe. Den underliggende release kjenner bare sesjon og ressurstype; den trekker én fra eksisterende feed/channel-teller med `max(0, … - 1)`. Kilder: **`B/BridgeChannelSession.swift:377–386`** og `:126–134`.

Dermed er «release exactly once» bare en garanti om ett fratrekk per objekt, ikke ett fratrekk per **vellykket opptak**. Klassen ble innført i rettingssettet. Både logiske kanaler og feeds bruker den: `B/BridgeMultiplexing.swift:1038–1055`; `B/BridgeBase.swift:1708–1716`.

Konkret forløp på én autentisert mux-forbindelse:

1. Åpne kanaler til per-key-kvoten er full, med lokal mux-kapasitet fortsatt ledig. Standardene er 16 kanaler per nøkkel, mens mux tillater 128 (`B/BridgeChannelSession.swift:21,118–123`; `B/BridgeMultiplexing.swift:859–868,995–1005`).
2. Neste open når lease-init; acquire avviser. `deinit` trekker likevel én fra eksisterende kanalkvote. `open` fanger feilen og sender `channelRejected`, uten å lukke en ellers fungerende fysisk forbindelse (`B/BridgeChannelSession.swift:378–386`; `B/BridgeMultiplexing.swift:1040,1074–1094`).
3. Et nytt open kan nå lykkes selv om ingen aktiv kanal er lukket. Gjentatte avslag/opptak kan omgå det tiltenkte per-key-/globale kanalregnskapet. Senere legitim release fra de opprinnelige leasene trekker fra den allerede feilaktig lave telleren (`B/BridgeChannelSession.swift:118–134`). Andre kapasitetsgrenser består; jeg hevder ikke ubegrenset allokering.

Feed-varianten rammer tilsvarende når en avvist ny feed forsøkes på en sesjon som allerede eier feeds. Ved avslag på en **annen** sesjon med null lokale feeds/channels skjules feilen av `max(0, …)` (`B/BridgeChannelSession.swift:115–132`; `B/BridgeBase.swift:1710`).

Den kjørte proben tok klassekoden direkte fra head, brukte en minimal kapasitet=1-sesjonsstub og beholdt den første leasen levende. Resultat, exit 0:

```text
first active; charged: 1
second rejected; charged: 0
first and third both active; charged: 1
```

**Nødvendig retting:** bare en vellykket acquire må aktivere lease-eierskapet. En throwing initializer skal ikke kunne frigjøre noe den ikke fikk. Behold samtidig vern mot dobbel release etter vellykket opptak. Regresjonen må bruke samme sesjon med en eksisterende lease: fyll grensen, avvis flere opptak, bekreft at nytt opptak fortsatt avvises frem til faktisk eier frigir. Gjør dette for både feed og channel, per-key og globalt, og gjennom en reell mux-open/reject/open-sekvens. Test også at close pluss senere fullføring frigir nøyaktig det som fortsatt eies.

Dagens tester finner ikke dette: mange-nøkler-testen lager en ny sesjon for hvert forsøk, og nummer ni har ingen lokal reservasjon å trekke fra (`T/BridgeChannelLifetimeQuotaTests.swift:98–135`). Den direkte ressurskvotetesten kaller `session.acquire` uten lease-klassen (`T/BridgeChannelAuthenticationTests.swift:379–383`). Grønne resultater fra disse testene motbeviser derfor ikke N06.

### Øvrig livsløps- og låsekontroll

For **vellykkede** opptak er følgende forbedringer reelle:

- `trackedWork` reserverer før task-oppretting, viderefører cancellation, og workerens defer frigir først etter retur. Send-bytes frigjøres også etter await. Close beholder transportreservasjonen gjennom delegate-opprydding og fysisk close. `B/BridgeChannelTransport.swift:98–104,117–132,202–242`.
- En fjernet `ChannelRecord` holdes levende gjennom pågående dispatch, eier channel-leasen og kansellerer egne tasks. Lukking av én kanal pensjonerer ikke søsken. `B/BridgeMultiplexing.swift:791–824,938–958,970–971,1137–1155`.
- Feed-lease har idempotent release ved fullføring/stop/close; feed-delivery reserverer operation-kvote før task-oppretting og frigir i defer. `B/BridgeBase.swift:1731–1745,1757–1805,2006–2020`; `B/BridgeChannelSession.swift:382–386`.
- Stream-historikken komprimeres også ved remove/reopen uten eviction, og tømmes når aktivt sett er tomt. Tester gjentar 1000 sykluser med søskenstream og observerer lagrede slots og sekvens. `B/BridgeMultiplexing.swift:91–127,1185–1222`; `T/BridgeMultiplexingTests.swift:1023–1064`.

Jeg fant ikke en ytterligere konkret låssyklus i de leste standardløpene. Limits-revoke tar ut callbacks før de kjøres; session-terminate slipper sin lås før limits-release og callback (`B/BridgeChannelSession.swift:197–200,360–368`). Transport/kanal venter på tasks uten å holde registrenes låser, men kaller `Task.cancel()` inne i lås ved close/retire (`B/BridgeChannelTransport.swift:119–131,224–231`; `B/BridgeMultiplexing.swift:806–823`). Vilkårlige vertsspesifikke cancellation-handlere og generell samtidighet er **ikke verifisert** av denne kildekontrollen eller dagens TSAN-utvalg.

Arbeid som aldri returnerer kan fortsatt holde kvote permanent. Det er tilsiktet regnskap for arbeid som faktisk fortsatt finnes, ikke en påvist ny lekkasje: postene fjernes først når `hasResources` er falsk, og opptak teller beholdte poster (`B/BridgeChannelSession.swift:38–39,78–81,151–188`). Testene slipper barrierene eksplisitt og beviser gjenoppretting etter retur; de beviser ikke at vilkårlig ikke-samarbeidende cellekode kan stoppes (`T/BridgeChannelLifetimeQuotaTests.swift:69–80,139–148,244–252`). Hostens grenser og timeouts er fortsatt nødvendige; regnskapet skal ikke «repareres» ved å glemme slikt arbeid.

## 3. §5-matrisen og testnavn

**Testene passerer i CI, men det betyr ikke at samtlige opprinnelige §5-krav nå er lukket.** CP-dekningen er vesentlig bedre. Kvoter feiler som sikkerhetsinvariant på grunn av N06; generisk attach og reelle konsument-/produksjonsløp er fortsatt avgrenset bort.

| §5-rad | Vurdering på head |
|---|---|
| **Første kommando / F01** | **Dekket for CP-admission.** Alle 29 enum-cases, ukjent kommando og separat response i begge retninger; null factory/oppslag/get/set. Suspendert proof-policy får konkurrerende get uten lookup/cellekall. Velformede feilsekvenser og gjentatte auth-rammer prøves begge veier. Navnene stemmer med innholdet. `T/BridgeChannelTransportTests.swift:32–95`; `T/BridgeChannelSequenceTests.swift:17–102`. Dette er ikke funksjonsbevis for alle 29 kommandoer. |
| **Identitetsbytte/forfalskning** | **Dekket for de etterspurte gate-variantene.** Positiv kontroll før annen nøkkel/samme UUID, annen UUID, nøkkelløs, nil og server-owner; ingen ekstra resolver-/cellekall. `T/BridgeChannelTransportTests.swift:480–506`. Samme UUID er reelt: hver fersk `MockIdentityVault` begynner på samme syntetiske UUID, men lager egen signeringsnøkkel (`T/TestSupport/MockIdentityVault.swift:15,27–38,86–100`). Ekte owner-proof før principalbytte finnes også (`T/BridgeChannelTransportTests.swift:98–129`). |
| **Replay/scope** | **Dekket på CP-sesjonsnivå.** Scope-varianter regenererer selvkonsistente signingData og prøver publisher, bro-ID, host, staging-host og domene. Andre instanser/ny state etter close avviser gammelt proof; parallelt consume gir én vinner. Navn korrigert fra tidligere overpåstand. `T/BridgeChannelAuthenticationTests.swift:55–76,157–190`. «Restart» betyr ny sesjonsstate i samme prosess; ingen klynge-/deploy-restart-test. |
| **Tid** | **Dekket for de navngitte CP-grensene.** +5/+5.001 og −29.999/−30/−30.001, selvkonsistent for lang/utløpt challenge, veggklokke alene, bakoverskew med monotont utløp, suspendert signer og suspendert send. `T/BridgeChannelAuthenticationTests.swift:193–260`; `T/BridgeChannelLifetimeQuotaTests.swift:204–222`. Ny revalidering etter signer og før aktivering finnes (`B/BridgeChannelClientOperation.swift:51–67`; `B/BridgeChannelSession.swift:286–300`). |
| **Proveniens / ingen serverhemmelighet** | **Nye CP-bevis dekker de etterspurte tilleggene; Scanner/Binding gjenstår.** Lightweight uten delegate og fysisk dekoder→auth→mux-observasjon av både command og response før Base er reelle testløp (`T/LightweightBridgeTransportTests.swift:167–218`). Separat macOS-serverprosess får offentlig descriptor, gjør beskyttet read og har signer-trap=0; parent sjekker syntetisk privat markør i wire, serialisert celle, sesjoner og logg (`T/BridgeChannelProcessTests.swift:13–52,55–114`). Testen kontrollerer disse artefaktene, ikke vilkårlig prosessminne eller all produksjonslogging. |
| **Signeringsorakel** | **Bedre, men presiser beviset.** `testRawSignAfterAuthenticationIsDeniedWithoutLocalPermit` sender `.signData(Data([1,2,3]))`; dette avvises av challenge-parseren før permit-vakten. Navnet bør si malformed/raw-sign, eller testen bør bruke gyldig challenge uten aktiv permit. `T/BridgeChannelTransportTests.swift:510–520`; `B/BridgeBase.swift:1509–1520,1546–1555`. Gyldig unsolicited challenge etter avsluttet operasjon er dekket av eldre fixture-test (`T/BridgeIdentityBoundaryTests.swift:294–336`), og permit-scope/reset av enhetstester (`T/BridgeIdentityProofAuthorizationTests.swift:11–68`). Ny suspendert lokal signer dekker cancel og klokkeutløp, ikke eksplisitt renew/revoke mens selve signer er suspendert (`T/BridgeChannelAuthenticationTests.swift:243–260`); den faktiske renew-testen suspenderer **denial-audit**, som navnet korrekt sier (`T/BridgeChannelTransportTests.swift:620–640`). |
| **Funksjon/formål/autorisasjon** | **Dekket for de eksplisitte cellehandlingene, ikke hele generiske bridge-API-et.** Ny test krever ekte `--x-` for invoke og utfører faktisk `GeneralCell.attach`; den prøver permissions, keypath, domene, expiry/revoke og formål lokalt/fjernt (`T/BridgeChannelTransportTests.swift:573–617,729–748`). Dette er en set-transportert cellehandling, ikke en ny execute-wirekommando. Eldre get/set/feed-avslag beholdes (`:237–297`). Testnavnet er nå tydelig «CellActions…RealAttach», og begrensningen for `BridgeBase.attach`/manglende `connectEmitter`-handler er eksplisitt dokumentert (`CP/Docs/BridgeIdentitySecurity.md:277–282`; dispatch `B/BridgeBase.swift:1367–1653`). |
| **Revokasjon** | **Dekket for lokal nøkkelrevokasjon under celle-/send-await.** To autentiserte klienter, én nøkkel revokeres, lokal cutoff <1 s, den andre svarer fortsatt og sen respons uteblir. `T/BridgeChannelTransportTests.swift:524–551`. Testens wire kontrollerer closed igjen etter barrieren (`:688–699`); dette er ikke garanti om å trekke tilbake allerede avleverte nettverksbytes. Lenkerevokasjon og propagasjon mellom verter er ikke dekket av denne testen. |
| **Kvoter** | **Ikke lukket.** Policy/factory/cell/feed/send/close testes med reelt suspendert arbeid og beholdte kvoter, men ikke feilslått lease-acquire på en sesjon med allerede eide ressurser. N06 viser hvorfor grønt ikke er tilstrekkelig. `T/BridgeChannelLifetimeQuotaTests.swift:41–222`; `B/BridgeChannelSession.swift:377–386`. Navnet `testManyKeysCannotEscapeGlobalCellFeedChannelAndSendLimitsByDisconnecting` er også bredere enn én isolert bytekvoteprøve: dens send-variant treffer operation-taket; egne send-byte-asserts ligger i testen ved `:152–186`, som delvis fyller budsjettet med direkte `acquireSend`. Ingen produksjons-RSS/CPU/NAT-rettferdighet måles. |
| **Robusthet** | **R1/R4 og tapt write-svar har konkrete regresjoner.** Write-testen utfører én mutasjon, mister svaret og oppretter et nytt autentisert klientpar; ingen ny set eller ekstra mutasjon observeres (`T/BridgeChannelTransportTests.swift:555–570`). Det er ikke automatisk reconnect på samme klientobjekt. Reell socket som henger før HTTP-upgrade lukkes i eksisterende prøve (`T/BridgeChannelWebSocketTests.swift:12–40`). App-drain og målt staging-reconnect gjenstår. |
| **TLS/proxy, route/release, ekte konsumenter** | **Fortsatt ikke bestått/sertifisert av CP-suiten.** Faktisk socket og subprocess bruker eksplisitt lokal WS, ikke WSS/proxy/discovery (`T/BridgeChannelWebSocketTests.swift:71–94`; `T/BridgeChannelProcessTests.swift:35–38,79–87`). R4 prøver ekte resolverklientkode med testtransport. AP5–AP9b og konsumentmigrering krever separat bevis. |

Ingen av disse testene skal omtales som full produksjonsgodkjenning. Matrisen identifiserer hva som faktisk er observert og hvilke navn/påstander som fortsatt trenger avgrensning.

## 4. CI på eksakt head og de tre lokale feilene

[PR #53](https://github.com/Digipomps/CellProtocol/pull/53) var OPEN, med head **`22d79190806f80b1d9dcb31d45e04dacd06fed22`**, ved kontroll. GitHub Actions API filtrert på hele SHA-en returnerte nøyaktig fem kjøringer; alle hadde `status=completed`, `conclusion=success`, `run_attempt=1`. PR-ens fem check-runs var også completed/success.

| Kjøring | Resultat |
|---|---|
| [macOS regression, 36318227172](https://github.com/Digipomps/CellProtocol/actions/runs/36318227172) | Grønn. Fulltest og utvalgte navngitte tester kontrollert i jobb-loggen. |
| [CellProtocol Swift Linux, 36318227140](https://github.com/Digipomps/CellProtocol/actions/runs/36318227140) | Grønn på eksakt head; detaljert testlogg **ikke lest**. |
| [Vapor identity vault Swift Linux, 36318227221](https://github.com/Digipomps/CellProtocol/actions/runs/36318227221) | Grønn på eksakt head; detaljert testlogg **ikke lest**. |
| [Runtime capacity benchmark, 36318227214](https://github.com/Digipomps/CellProtocol/actions/runs/36318227214) | Grønn på eksakt head; benchmark-resultatene **ikke lest**. |
| [Notify PyCellProtocol, 36318225375](https://github.com/Digipomps/CellProtocol/actions/runs/36318225375) | Grønn `pull_request_target`-varsling, ikke testbevis for Swift eller PyCellProtocol-runtime. |

En viktig presisering: macOS-jobben sjekket ut GitHubs syntetiske mergecommit **`32b4793bfe693d63b4d4d93a2ab2edac71457602`**, ikke head-commitobjektet direkte. Jeg kontrollerte [mergecommitens tre](https://github.com/Digipomps/CellProtocol/commit/32b4793bfe693d63b4d4d93a2ab2edac71457602) mot `git rev-parse '22d7919^{tree}'`: **begge er `bb4b58a128fdd9e1ec01d0aba9735106145b706e`**. Fulltesten kjørte dermed identiske kilder med den bestilte headen. Workflow bruker vanlig checkout og `swift test --disable-automatic-resolution`, etterfulgt av diff-kontroll (`CP/.github/workflows/security-regression-macos.yml:24–32`).

Fulltest i [macOS-jobb 108616926444](https://github.com/Digipomps/CellProtocol/actions/runs/36318227172/job/108616926444), sluttlinje ved 12:20:24 UTC:

```text
Executed 1373 tests, with 3 tests skipped and 0 failures (0 unexpected) in 29.667 (29.932) seconds
```

De nye auth/lifetime/sequence/process/transport-suitene, R1-testene og den parallelle resolverpool-testen har eksplisitte `passed`-linjer i denne loggen. Subprocess-worker er skipped i vanlig suite, mens parent-testen som starter den separate prosessen består (`T/BridgeChannelProcessTests.swift:13–15,65–70,91–105`).

Jeg leste nå også feilene, ikke bare antallet, i implementørens `/private/tmp/cp53-final-test.log`:

| Lokal test og feil | Samme test i ny CI |
|---|---|
| `AppleIdentityVaultKeyStorageTests.testLegacyEmbeddedPrivateKeyMigratesToApplicationTagAndSigns`: NSOSStatusErrorDomain 100001 / EPERM, lokallogg linje 246–247. | **passed**, 0.042 s, loggtid 12:19:55.509551 UTC. Test `T/AppleIdentityVaultKeyStorageTests.swift:99–127`; feilpunkt `CP/Sources/CellApple/IdentityVault.swift:1372–1374`. |
| `AppleIdentityVaultKeyStorageTests.testLegacyEmbeddedPrivateKeyStillSigns`: samme 100001 / EPERM, lokallogg linje 249–250. | **passed**, 0.030 s, loggtid 12:19:55.509824 UTC. Test `T/AppleIdentityVaultKeyStorageTests.swift:81–97`; samme feilpunkt. |
| `AppleIdentityVaultKeyStorageTests.testScopedSecretDataStaysStableInUnsignedTestHost`: `unhandledError(status: -25291)`, lokallogg linje 258–259. | **passed**, 0.003 s, loggtid 12:19:55.510659 UTC. Test `T/AppleIdentityVaultKeyStorageTests.swift:69–79`; feilpunkt `CP/Sources/CellApple/IdentityVault.swift:775–780`. |

Lokal sluttlinje er bekreftet: 1344 tester, 10 skipped, 3 failures, 25.560 (25.632) s. Vault-kilde og denne testfilen er uendret mellom CP-base og head. Loggene støtter derfor konkret forklaringen om lokalt Keychain-/vertsmiljø; en egen basekjøring i nøyaktig samme lokale miljø er **ikke kjørt**. Forskjellen i testantall/skips er ikke forklart ved en full gjennomgang av begge testinventarene; det inventaret er **ikke lest**.

TSAN kjører tre repetisjoner av **bare `BridgeDescriptionConcurrencyTests`** (`CP/.github/workflows/security-regression-macos.yml:33–46`). Dette attesterer ikke generelt de nye auth-/lease-/mux-livsløpene.

## 5. R3: kan Scanner vente til etter merge?

**Min anbefaling er nei: løs R3 i samme PR/endringssett før CP53 går til main.** Alternativt kan en separat forutgående PR levere Kjetils valg B. Det er ikke grunnlag for å avskrive funksjonen som bare testkode.

CPs egen Scanner er uendret av PR53, men den bruker nå en endret Base-kontrakt: `ScannerPeerTransport` har ingen channelSession og får protokollens nil-standard; setup lager rå Base og sender ready eller forsøker description/attach. Base krever nå autentisert session og avviser ready. Kilder på head: `CP/Sources/CellApple/EntityRadar/ScannerService.swift:65–96,586–648`; `B/BridgeTransportProtocol.swift:47–49`; `B/BridgeBase.swift:1297–1299,1342–1348,1810–1812`. Til sammenligning godtok Base `.ready` på base/main `a6fa51a8…`, `Sources/CellBase/Cells/Bridging/BridgeBase.swift:1280–1282`. Det er en reell kontraktsendring for den eksisterende peer-kodeveien.

Feilen blir fortsatt lite synlig for caller: connected-status sendes før async setup, setup-feil printes, og receive fanger/print-er feil. Auth-strenger passer heller ikke Scanner-dispatchens `Command(rawValue:)`-krav. `CP/Sources/CellApple/EntityRadar/ScannerService.swift:967–980,1010–1022,1082–1118`. Lokal-vault-fallbacken står også igjen (`:1039–1049`); den er ikke rettet av R1/R2/R4.

**Direkte søk på typen undervurderer Binding-bruken.** På kontrollert Binding-main:

1. Bootstrap kaller CPs `AppInitializer.registerEntityScannerResolve` (`Binding/Binding/BootstrapView.swift:681–685`). På CP-head registrerer denne offentlige funksjonen den interne `EntityScannerCell` som **`EntityScanner`**, ikke `ConnectRadar` (`CP/Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/AppInitializer.swift:355–371`).
2. Binding slår faktisk opp `cell:///EntityScanner`, beholder Meddle og abonnerer på flow (`Binding/Binding/BootstrapView.swift:4354–4368`).
3. Runtime videresender blant annet `invite` til `scannerMeddle.set` (`Binding/Binding/BootstrapView.swift:4442–4455,4504–4507`). Katalogen annonserer start/stop/invite/kontakthandlinger (`Binding/Cells/ConfigurationCatalogCell.swift:7763–7764`).
4. CP-cellen oppretter `ScannerService` ved start, og invite-intercepten kaller dens peer-invitasjon (`CP/Sources/CellApple/EntityRadar/EntityScannerCell.swift:298–308,452–471,488–496,600–609`). Scanner inviterer inn i MCSession og starter `setupBridge` når peer blir connected (`CP/Sources/CellApple/EntityRadar/ScannerService.swift:338–349,967–979`).

Binding-testen med direkte typebruk tester publisering/discovery og sier uttrykkelig «No radio startup» (`Binding/BindingTests/NearbyScannerImplementationTests.swift:184–199`). Den beviser verken fungerende peer-bro eller fravær av runtime-konsumenter.

**Skillet mellom merge og utrulling består:** Binding-main har en eksplisitt CP-revisjonspinn `79497e85…` (`Binding/Binding.xcodeproj/project.pbxproj:806–812`). Ren merge av CP53 endrer ikke denne pinnen eller allerede installerte apper. Jeg har ikke observert dagens radiofunksjon på en kjørende Binding-installasjon, og hevder derfor ikke at et konkret produksjonsløp som er bevist fungerende i dag, allerede er blitt slått av. Men source viser en eksisterende, eksponert konsumentvei som blir inkompatibel ved opptak av ny CP. «Bare BindingTests bruker Scanner» er ikke et holdbart fritak fra R3.

HAVEN_MVP har egen Scanner-implementasjon, men den bruker fortsatt CPs `BridgeBase` med ready/description og en lokal default-vault (`HAVEN_MVP/HAVEN_MVP/ConnectRadar/ScannerService.swift:166–194,491–492`, på SHA angitt i §1). Egen kopi isolerer den fra endringer i **CPs Scanner-fil**, ikke fra Base-API-/auth-endringer. Prosjektet peker på CP-grenen `Purpose&Interest`, ikke CP-main (`HAVEN_MVP/HAVEN_MVP.xcodeproj/project.pbxproj:603–609`). Faktisk utrullet dependency, bygg og to-peer-funksjon er **ikke kontrollert**; øvrig HAVEN_MVP-kode er **ikke lest**.

Valg A må levere egnet autentisert peer-profil og positiv to-peer-funksjon. Valg B må gi en eksplisitt, testet «peer bridge authentication unsupported»-feil før rå Base/ready/registrering, rydde pending-state og nå konsumentens status-/feilkanal. Separate advertisement/discovery-funksjoner må avgrenses og verifiseres særskilt. Dagens endpointprofil er WSS eller eksplisitt WS-loopback; falsk WSS-origin eller ready-unntak er ikke en migrering (`B/BridgeChannelAuthentication.swift:77–96`). Dette er anbefalte akseptkrav, ikke kode som allerede finnes på head.

## 6. Mergeanbefaling og gjenværende porter

**Merge etter to rettinger:**

1. **Rett N06/R2** og legg til regresjoner for avvist lease-opptak på samme sesjon med eksisterende eierskap. Bevis fortsatt korrekt kvote over close/cancellation og faktisk fullføring. Grønn CI må kontrolleres på den nye headen.
2. **Fullfør R3 etter Kjetils valg A eller B før CP53 går til main.** Minste avgrensede løsning er B dersom peer-broen eksplisitt tas ut av støtte; taus funksjonssvikt er ikke B. Den lesbare indirekte Binding-konsumenten må inngå i beslutningen.

N01/R1 og N04/R4 trenger ikke ny redesign ut fra denne kontrollen. Presiser testbeviset i §3, særlig malformed-sign kontra gyldig challenge uten permit, og unngå å rapportere hele generiske attach-/produksjonsmatrisen som bestått. N05 i Bindings `PersonEntityReadTransport` er **ikke gjenkontrollert i denne runden**; den tidligere konsumentblokken er ikke opphevet. CellScaffold-/HavenAgentD-migrering, WSS/proxy/readiness og AP9b er også **ikke lest eller verifisert på nytt**; forrige rapports §7 står ved lag som integrasjons-/produksjonsporter.

Arbeidstrærne var skitne fra før. Jeg har bare skrevet denne rapporten i dokumentrepoet; ingen kildekode, commit, push, PR-kommentar, merge, dependency-pin eller utrulling er utført.
