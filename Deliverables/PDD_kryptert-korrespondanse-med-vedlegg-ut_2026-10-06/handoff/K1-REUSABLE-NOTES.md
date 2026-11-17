# Gjenbrukbare funn fra k1

Kildebaserte funn og avgrensede prøver, ikke bevis for en ferdig produktflyt.

## k13 — readiness før staging-testpar

Målt 2026-10-11 på CellScaffold `9ff06f84`, CP `b4100f57`: `/health/ready`
returnerte HTTP 200 og global `status=ready`, samtidig som `correspondence`
var `configured=false, ready=true, storageAvailable=false`. Eksakt deployet
`CorrespondenceRelationshipHost.install` returnerer uten installasjon når
`HAVEN_CORRESPONDENCE_DATA_ROOT` mangler; readiness bruker denne kombinasjonen
når verten ikke er installert. Les både `/health/build` og de tre
korrespondansefeltene før klientbygg eller opprettelse av testidentiteter.
Generell readiness beviser ikke at korrespondansehosting er aktivert.
Ved forbud mot env-/vertsendringer: stopp og rapporter manglende konfigurasjon;
ikke bruk eldre innmeldingsruter eller andres profiler som erstatning.
Bevis: `HAVEN-Deploy/_handoff/KORR-UT/k13/`; rapport: `handoff/STAGING-TESTPAR-RAPPORT-k13.md`.

## k14 og k14-r2 — effektiv origin og én env-linje

K14 stoppet 2026-10-12 fordi oppdragsteksten krevde eksplisitt
`CELL_SCAFFOLD_BRIDGE_ORIGIN`. Kjetil avklarte i k14-r2 at dette var agentens
krav, ikke hans, og fjernet det. Ikke viderefør det som en teknisk
forutsetning: deployet `CorrespondenceRelationshipHost.install` på `9ff06f84`
faller tilbake til konfigurert WebAuthn-origin. `RP_ORIGIN` i kjørende staging
ga nøyaktig forventet origin. Kontrollen rapporterer bare «samsvarer» eller
«samsvarer ikke», og stopper ved avvik.

K14-r2 aktiverte verten med bare `HAVEN_CORRESPONDENCE_DATA_ROOT` via installert
`haven-deploy --env-only` og `SET_ENV_FILE`. Privat katalog eies av appbrukeren,
modus 0700, på eksisterende skrivbar bind-mount fra vertens disk. Mounten
ble bevart over containerbytte og kontrollert restart. Dette beviser vedvarende
lagring over containerbytte; det hevder ikke separat datadisk eller backup av
korrespondanseinnhold. Kapasitetskravet var minst 10 000 000 000 ledige byte.
Runtime-env gikk fra 94 til 95 linjer og env-filen fra 6 til 7, med alle
øvrige verdier/byte bevart. Samme image og revisjon, uendrede fingeravtrykk,
og alle tre korrespondansefelter true etterpå. Installerte deployverktøy må
leses og hashbindes; repo-kopien var ulik vertens.

Kontrollfallgruver målt i k14-r2:
- Docker inspect kan returnere mounts i en annen rekkefølge. Sammenlign
  samtlige felt sortert etter Destination; bare listeorden var forskjellig.
- Et mislykket claim-kall må stoppe alle avhengige mutasjoner. I k14-r2 ble
  katalog/env klargjort før claim etter to lokale kallfeil; claim var først
  bekreftet før cutover. Dette er et dokumentert avvik, ingen godkjent mal.
  Kontroller exit-kode og faktisk claim før hvert muterende steg.
- Bruk strukturert subprocess-argv og shlex.quote for det ene eksterne
  shell-argumentet. Første manuelt nestede prøvestart mistet quoting; den
  korrigerte femsekundersprøven beviste terminalfri sudo og sluttmarkør etter
  at SSH hadde returnert. Bash-login fant dessuten en inkompatibel python3;
  lokal orkestrering brukte den faktisk kjørende Python-tolken.
- Marker kommando-posten done mens claim fortsatt er aktiv, før release.
  En avsluttet claim gjør at hd nekter også etterfølgende done-registrering.

Bevis: `HAVEN-Deploy/_handoff/KORR-UT/k14-r2/`. Opprinnelig stopp er bevart i
`handoff/STAGING-LAGRINGSROT-RAPPORT-k14.md`; full leveranse og rollback-vei i
`handoff/STAGING-LAGRINGSROT-RAPPORT.md`. Ingen innholdsmeldinger eller
klientflyt ble prøvd i denne env-aktiveringen.

## Swift 6 og mutable protokollobjekter

Contract og Identity er mutable referansegrafer. Actor-isolert historisk verifikasjon feilet ved overføring til CPs async verifikasjon selv om objektet var deklarert med let. I klientens retting sendes bare immutable Data til en privat statisk async helper; den dekoder sine egne Contract/Identity-objekter og returnerer Bool. Ingen mutable graf eller vault returneres. Avbrytelses- og generasjonssjekk kjøres etter await før forespørselen lagres. c150 kompilerte og de samme sju native prøvene bestod. Dette er ikke generell godkjenning av andre CP-actor-overføringer.

## Andre fangede funn — bevart utenfor det ucommittede arbeidstreet

- Behold SwiftPM-cacheleasen gjennom bygg og test, og kopier verifiserte produkter med kildehash før leasen avsluttes. Ellers kan cache-GC fjerne produktene mens en senere køjobb venter.
- DYLD-variabler må settes inne i Python-testhjelperen når den beskyttede systemtolken ikke viderefører dem fra wrapperen. Skill XCTest-loaderfeil fra funksjonell red.
- Første historikksekvens er 0. Bruk nil for ny strøm og eksplisitt 0 for gjenopptak etter første post; negativ markør avvises før abonnement.
- Køens filstørrelsesgrense kan gi SIGXFSZ under Swift-bygg. Den egne byggwrapperen justerte soft-grensen; bruk dette bare i avgrensede egne byggjobber.
- ValueType kan inneholde mutable Identity/Agreement/Cell, også rekursivt. En unchecked Sendable-wrapper gjør dem ikke trygge; klientadapteren bruker rekursiv verdi-only-grense og avviser referansecasene.
- Contract-signaturen beskytter ikke alene top-level X25519-deskriptorer. Sammenlign issuer/subject/nye nøkler med signed Agreement owner/signatories og kjent lokal nøkkel. Kombinert unsigned descriptor-tampering viste faktisk red i c149, grønn etter bindingrettingen i c150.
- Invitation signerer Cell UUID, invitation ID og tidsfelt, ikke lenkens host/owner UUID/X25519-hints. SAS sammenligner invitee-nøkler, ikke owner/host. Verifiser sluttavtalen før innmelding; vis destinasjonen.
- Native fornyelse kan fremdeles kaste signerte conditions/policy ved å bygge en ny mal. To genuinely signed negative tester er bare utkast. Rett og demonstrer red/grønn før videre leveranse.

Kildebevis: k1s private bygglogger og verdifrie evidence-filer i denne PDD-en; de opprinnelige læringsoppføringene peker på HavenAgentD-arbeidstreets Docs. Denne kopien bevarer funnene også dersom arbeidstreet senere fjernes. Ingen ferdig Flow/native/installerfunksjon hevdes.

## k2 — Native topology and evidence boundaries

On CP 3d6be30a, the scoped client proof vault delivered a pushed envelope over the host-style direct authenticated Native transport without a delay. The client previously used a multiplex session. The original c150 assertions, retained with a direct-native server fixture, and a route-binding regression passed (2 tests). A separate multiplex diagnostic failed; delaying SET-response processing 250ms made its copied assertions pass. That is a diagnostic observation, not an acceptable production delay or a complete proof of a specific internal permit race.

The larger two-profile test then delivered pushed text and 1,100,037-byte copies in both directions. Its actual thrown failure was a retained local attachment-cache lock when constructing the replacement client. Signing diagnostics appeared around stream cancellation, but do not alone establish active Flow failure. Read the exact thrown error and checkpoints before attributing a red test to a nearby log line.

Current CP legacy invitation setup needs a recipient public-key lookup through the default vault. Keep fixture signers in distinct vaults; providing that lookup during a local-only fixture is not evidence that a production host should hold participant private keys. The legacy and attachment contract fixtures must select their intended grant set; substituting an attachment contract for a legacy contract changes the negative test's premise.

With the original legacy fixture/assertions restored and its lookup adapted, 9 of 10 hosted tests passed. The remaining existing test obtains a separately signed owner agreement and expects an already-invited member operation to return unchanged. CP inviteIdentities instead checks requester UUID against the Cell owner and returns denied. Correcting that compatibility behavior belongs upstream in CP, or requires an explicit decision to change the existing contract/test; k2 did neither. No native admin, automatic reconnect, full green port, CI or installer was delivered.

## k13-r2 — innslipp grønt, vedlegg fortsatt rødt på staging

Målt 2026-10-12 med PR #32-klientbiblioteket `d91408bc`, lokalt pinnet til
CP-tag `2026.9.7` (`b4100f57`), mot staging `9ff06f84`: A opprettet en
relasjonscelle over autentisert Native-bro; B ba om innslipp, seks sifre ble
sammenlignet automatisk, A signerte og B aksepterte avtalen. Dette er
protokollbevis fra en lokal driver, ikke native-vindu/Touch ID-bevis.
To tekster, én hver vei, ble dekryptert og lest igjen fra en ny prosess for
begge. Ingen publiserte vedlegg var i slutt-historikken.

En 1 100 037-byte kilde hver vei feilet under `attachments.upload`:
A fikk ett `ok` før neste kall svarte `status=error, message=attachmentUnavailable`;
B fikk samme feil allerede for chunk 0 (65 564 ciphertext-byte). Begges
opprydding feilet; B-sporet viser `attachments.revoke` → `SetValueError`,
NSError-kode 4. Dette er ikke bevis for at tilbakekall av et publisert vedlegg
virker. Den generiske serverfeilen skjuler rotårsaken; verken lagringsfeil,
transportfeil eller manglende env er bevist. HD-0219 følger opp.

Spor hvert kall med handling, chunk-indeks/størrelse, svarform og allowlistede
feilkoder, uten nøkler, koder, innhold eller identitetsverdier. Ved ukjent
publiseringsutfall: les testparets historikk før ny sending. Bevar første feil
separat: første innmeldingsforsøk her ga en uavklart DecodingError; en
lesende kontroll fant null ventende, og innslipp på samme testpar lyktes
fra ny prosess. Ikke kall dette en rettet rotårsak.

Bevis: `HAVEN-Deploy/_handoff/KORR-UT/k13-r2/`. Grønn readiness, innslipp og
tekst er ikke en vedleggsakseptanse. Rapporten er fortsatt STOPPET.
