# Rollebevis for Kjetil og Vegar — Astra, 2026-09-23

**Status: lokal patch og seremoniutkast levert; ingen utstedelse, installasjon, bygg, SSH eller deploy utført. `applied` er ikke verifisert.**

Formålet er at Kjetil (`kjetil2`) og Vegar kan godkjenne top-up med CellProtocol-autoritet i staging og prod, også på første HTTP-kall etter restart uten å åpne admin-Porthole. Stagingmålet er `POST /admin/api/funding-requests/D03228B6-4B53-4F8D-83CB-2E326DF63131/approve` → `request.status=applied`. Prod trenger en egen, faktisk forespørsel; staging-ID-en skal ikke brukes der.

Kø: **HD-0125** følger patch, bygg, seremoni og miljøaksept. **HD-0126** følger fornyelse før utløp. Oppgaven supplerer HD-0029, som gjelder HTTP-adminadgang. Ingen køpost er merket levert til miljø.

## Konklusjon fra kilde

På `origin/main = 77a922bc301a0ea7586a6b3677a87c2b1e0f73f7` er en bootstrap-bundle alene **ikke nok**. Det finnes tre brudd:

1. Webs `AdminFunding` bruker `hasRoleProof(.operator)`, som slår opp **lokal** `cell:///AdminRoleEnrollment` og krever `AdminRoleEnrollmentCell`. Den registreres bare i `local_workbench`. `registerRemoteHost` omskriver ikke hostløse lokale endpoints. I remote-modus gir dette ikke remote-verifikasjon, og en bro kan heller ikke castes til den lokale klassen.
2. `requestEntry` og `requestRole` gjør `requester.set(identity.proofs...)` **i AdminScaffold-prosessen**. Den dedikerte prosessen registrerer ikke `EntityAnchor`. Og bare å registrere en anchor ville fremdeles ikke løse kjeden: den pinnede CellProtocol-versjonen `473357cf4efee831cb3b55ae87bc921d4bb63c10` begrenser broens identitetssignering til den direkte cellens domene/resource, ikke en tilfeldig ny undercelle. Det skal ikke løses med bredere signeringsadgang.
3. `authenticatedRequester` registrerer offentlig identitet, men kaller ikke `restoreAcceptedCredentials`. Den eksisterende restore-kroken ligger i full Porthole-bootstrap med adminreferanser. Approve-ruten er derfor ikke selvstendig etter restart. Entity-persistens finnes i kode, men gjenpresentering i riktig prosess mangler på denne brukerbanen.

Den målte 500-feilen forklares i tillegg av at `issuePrepaid` bare håndterer returstrengen `denied`. Den fanger ikke `CellAuthorizationError.denied` fra Meddle-dispatch.

Dette er kildefunn, ikke nye målinger av verten. Claudes oppgitte feil, miljømodus, containere, identitetskoblinger og WP10-resultat er brukt som mottatt. Ingen nett- eller helsesjekk ble kjørt.

### Kildekart

Alle CellScaffold-stier nedenfor er relative til `/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-admin-levering-20260923`. For **før**-oppførsel: les filene med `git show 77a922bc:<sti>`; arbeidsfilene inneholder patchen.

| Ledd | Kilde og avgjørende kontrakt |
|---|---|
| Utstedelse | `Sources/ScaffoldKit/AdminScaffoldBootstrap.swift`: offentlig Identity; eksisterende signérbar AdminScaffold-owner; entry + eksplisitt valgte roller; separat eksklusiv 0600-output. Ingen mottakerinstallasjon. |
| Stopp/volume/vault | `Documentation/AdminScaffold_M4_Runbook.md`, «Credential-bootstrap». Service lock i `AdminScaffoldBootstrap.swift`. |
| Lokal/remote registrering | `Sources/App/configure.swift`, registrering av AdminFunding og betinget AdminRoleEnrollment; `Sources/ScaffoldKit/AdminControlPlaneRouting.swift`, `endpoint(for:)`, `registerRemoteHost`, `registersInfrastructureCellsLocally`. |
| Beskyttet handling | `Sources/App/Cells/Admin/AdminFundingCell.swift`, `validateCellSpecificAccess` → `AdminMetricsSupport.hasRoleProof(.operator)`. Ressurs: lokal AdminFunding, handling: `issuePrepaid`, tillatelse `-w--`. |
| Autoritet | `Sources/ScaffoldKit/AdminRoleEnrollmentCell.swift`, `issuerAllowed`, `verifyOrRequestRole`, `verifiesStoredRoleCredential`; `AdminSecurityPolicyCell.swift`. |
| Entry | `Sources/ScaffoldKit/AdminEntryCell.swift`, `evaluate`, `verifyEntry`, `verifiesStoredEntryCredential`. |
| UI-opplasting | `Sources/App/Controllers/PortholeWebSessionSupport.swift`, `porthole.submitAccessRequirementCredential`; `Sources/App/Cells/AccessRequirementPrompt/AccessRequirementPromptCell.swift`, `submitCredential`. |
| Varig lagring | `Sources/App/Support/AdminEntityProofPersistenceSupport.swift`: `proofs.credentials.<localCredentialID>` + `proofs.index.byKeypath.k<sha256>`, batch-ack og readback gjennom `IdentityEntityPersistenceSupport`. |
| HTTP-identitet | `Sources/App/Controllers/VaporAdminMVP.swift`, `authenticatedRequester`, `adminFundingCell`, `issuePrepaid`; `Sources/ScaffoldKit/BrowserClientIdentityVault.swift`. |
| Broens bevisgrense | **CellProtocol ved pin `473357cf`**, `Sources/CellBase/Cells/Bridging/BridgeIdentityProofAuthorization.swift`, `BridgeBase.swift`, `BridgeBase+Config.swift`. Lokal CellProtocol HEAD var `561d34a7`, og er ikke brukt som kontrakt for denne endringen. |

### Hvilken utsteder godtas?

`AdminRoleEnrollment` godtar DID-en til **sin egen AdminScaffold-owner** når `allowScaffoldOwnerIssuer` er sann, eller en eksplisitt betrodd DID i **AdminScaffolds AdminSecurityPolicy** når `allowTrustedIssuers` er sann. Begge flagg er sanne i standardpolicy, men issuer må faktisk matche owner eller listen. `AdminEntry` har tilsvarende owner-/trusted-issuer-policy, med sin egen liste. Dedikert runtime avviser når revokeringsregisteret ikke kan leses.

Deretter kreves riktig credentialtype, gyldig signatur, subject-DID lik mottakerens signerings-DID, riktig rolle/rolle-keypath, samsvarende credential-ID, gyldig levetid og ingen revokering. Patchen krever også direkte bevis på mottakerens nøkkelkontroll ved remote entry-/rollepresentasjon. Kopiert offentlig identitet er ikke nok.

Web-scaffold-owner er **ikke** automatisk betrodd av AdminScaffold. Verken `MVP_ADMIN_*`, `entity:digipomps`, representative mandates eller WP10 gir denne issuer-/operatorautoriteten. Seremonien bruker nøkkelen til den **eksisterende AdminScaffold-eieren i miljøets vault**. Kjetils root-kjøring er den menneskelige utstedelsesbeslutningen; credentialen signeres ikke av Kjetils passkey med mindre det faktisk er samme owner-identitet.

## Patch og valg

Arbeidstre: `/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-admin-levering-20260923`.
Gren: `claude/admin-levering-20260923`, HEAD `77a922bc`. Ingen commit eller push laget.

Endringene er avgrenset til:

- `AdminMetricsSupport.swift`: velger remote `cell://<konfigurert-admin-authority>/AdminRoleEnrollment` og `Meddle.set(verifyRoleCredential)` fra web. Feil, utilgjengelig bro eller avslag blir `false`. Dedikert AdminScaffold bruker lokal verifier, også for entry, slik at intern verifikasjon ikke går over egen WSS-bro.
- `AdminEntryCell.swift`, `AdminRoleEnrollmentCell.swift` og ny `AdminPresentedCredentialStore.swift`: dedikert AdminScaffold holder **midlertidige signerte presentasjoner** per UUID + signeringsfingerprint. Direkte nøkkelkontroll og eksisterende signatur-/issuer-/subject-/expiry-/revocation-sjekker gjelder. RoleEnrollment krever verifisert entry for sine avgrensede operasjoner. Lagringen serialiseres ikke. Local-workbench-oppførselen beholdes.
- `AdminEntityProofPersistenceSupport.swift`: etter aksept og varig batch-ack legges credentialen også på webidentitetens kanoniske proof-keypath. Restore gjør samme lokale presentasjon først etter remote aksept. Entity-record/index er varig kilde, kopien på proof-keypath er ikke autoritet i seg selv.
- `VaporAdminMVP.swift`: restore på HTTP-rutens `authenticatedRequester`; typed Meddle-denial blir den eksisterende 403-teksten med `reasonCode=<decision.reasonCode eller path>`. Legacy `denied` får `reasonCode=agreement_or_proof_required`.

**Valg gjort eksplisitt:**

| Spørsmål | Alternativer | Anbefaling / patch |
|---|---|---|
| Presentasjoner i dedikert admin | Ny EntityAnchor med nye undercelle-signeringstillatelser; eller liten verifier-eid presentasjonslagring | Sistnevnte, implementert. Ingen endring i CellProtocol, broens signeringsomfang eller issuer-policy. |
| Offentlig eksport | Dekryptere web-vault med nytt root-verktøy; eller eksportere offentlig nøkkel fra autentisert `did:key` | Nettleserhjelperen bruker offentlig DID og den oppgitte konto/UUID-koblingen. Kontroller requesterUUID i Inspector; ingen vault eller private nøkler åpnes. |
| Installasjon | Navigere et admin-dashboard som også ber om observer/security; eller gå direkte gjennom eksisterende AccessRequirementPrompt | Hjelperen bruker samme `submitCredential` som upload, med entry først og operator etterpå. Ingen ekstra roller trengs. |
| Roller | Entry + operator; eller i tillegg observer/security | Bare entry + operator utstedes. Øvrige roller krever egen begrunnelse. |
| Levetid | 30 dager; eller endre felles policy | Behold 30 dager nå. Fornyelsesrutine i HD-0126. |

Ingen endringer er gjort av Astra i `ScaffoldAdministratorProvisioner.swift`, `scripts/provision-scaffold-administrator-*.sh` eller `Tests/AppTests/ScaffoldAdministratorProvisioner*`. Disse hadde/har samtidige Claude-endringer og skal håndteres separat. Package-filer og CellProtocol-pin er urørt.

### Restart-kontrakten etter patch

1. UI `requestEntry`/`requestRole` verifiserer mot dedikert AdminScaffold.
2. Samme UI-handler kaller `persistAcceptedCredential`: privat web-Entity-record + index lagres med kvittering og readback.
3. Web- eller AdminScaffold-restart kan miste aktive presentasjoner.
4. Første ekte approve-kall løser samme BrowserClientIdentityVault-identitet, leser Entity-recordene og gjenpresenterer **entry før roller**.
5. Remote-verifier sjekker dagens policy/signatur/subject/utløp/revokering; lokal AdminFunding ber remote om operator-verifikasjon og utsteder først ved `granted=true`.

Dette fjerner avhengigheten av å åpne admin-Porthole. Varig lagring krever fortsatt intakt web-Entity/vault og stabile miljøvolumer. Reell webprosess-restart og faktisk funding-apply er **akseptporter som gjenstår**, ikke bevist av kodelesing. Utilgjengelig AdminScaffold gir avslag; det finnes ingen lokal autoritetsfallback. Restore kalles hver gang, ikke bare ved tom cache, slik at en varm presentasjon ikke skal omgå ny revokering.

## Seremonifiler — ikke kjørt

Alt ligger under `/Users/kjetil/Build/Digipomps/HAVEN/HAVEN-Deploy/_handoff/ADMIN/rollebevis-20260923/`:

| Fil | Bruk |
|---|---|
| `install-in-browser.js` | To eksplisitte knapper: offentlig eksport, deretter installasjon av egen bundle. Kun same-origin `/admin/api/session` og `/browserhead/porthole/action`. Ingen funding-godkjenning. |
| `public-identity.py` | Alternativ offline-konvertering av kopiert `did:key` til offentlig CellProtocol Identity. Ingen nettverk, vault eller private felt. |
| `ceremony.sh` | `prepare`, `apply`, `collect`. Sourcer `HAVEN-Deploy/lib/vert.sh`; bruker `$SSH_ROOT` og `vert_scp`, med BatchMode/IdentitiesOnly. |
| `host-ceremony.py` | Linux-root-worker. Oppdager riktig container, eksakt lokal image-ID, lagringsmount, vault-key-mount og owner-UUID; skriver plan; avviser drift mellom plan og apply. Stopper riktig tjeneste, kjører Bootstrap uten nettverk, starter tjenesten igjen i `finally`, kontrollerer healthy. |
| `preflight.json` | Lokal T0/T1-rapport; ikke miljø- eller byggebevis. |
| `source-manifest.json` | Baseline, gren og SHA-256 for de ni Astra-eide kilde-/testfilene; skiller dem fra samtidige provisioner-endringer. |

Stagingcontainer er `cellscaffold-admin-scaffold-1` (Docker-manager); production er `admin-scaffold-production-app-1`, administrert av `admin-scaffold-production.service`. Prod-managerens kommandoer kontrolleres før stopp. Image-tag, releasekatalog og volume-sti er ikke hardkodet: den faktiske containerens immutable image-ID og mounts brukes. Inline vault-master-key eller avvikende mount-/manager-kontrakt gir stopp, ikke gjetning.

Worker kjører `/app/AdminScaffoldBootstrap --roles operator --valid-days 30` mens samme AdminScaffold er stoppet, med samme vault/lager og eksisterende owner. Begge mottakere tas i ett stopp per miljø. Ingen env-rollebro, trust-list-endring, DB-skriving eller mottakerinstallasjon på verten. Output splittes til `.entry.json` og `.operator.json` for vanlig UI-upload, og beholdes også som `.bundle.json` for nettleserhjelperen.

### 1. Bygg og deploy patchen først — Kjetil/Claude-jobben

Bygg både web og AdminScaffold fra samme gjennomgåtte patch på den pinnede CellProtocol-versjonen. Den dedikerte prosessen trenger også endringen; en ren webdeploy er ikke tilstrekkelig. Bruk eksisterende deployløp og koordinering, ikke seremoni-skriptet til deploy.

Fokus for jobben, med repoets eksisterende bounded/isolated runners:

```bash
cd /Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-admin-levering-20260923
scripts/run_swift_bounded.sh build --force-resolved-versions --product AdminScaffold
scripts/run_swift_bounded.sh build --force-resolved-versions --product AdminScaffoldBootstrap
zsh scripts/run_tests_isolated.sh --force-resolved-versions --filter 'AdminFundingCredentialRoutesTests|AdminPresentedCredentialStoreTests|AdminEntityProofPersistenceSupportTests|AdminRoleEnrollmentCellTests|AdminFundingCellTests|AdminCredentialPolicyTests|AdminCredentialRevocationTests|AdminScaffoldBootstrapTests|AdminControlPlaneRoutingTests'
zsh scripts/run_tests_isolated.sh --force-resolved-versions --filter AdminEntryRemoteBridgeLoopbackTests
```

Loopback-testen finner `AdminScaffold` ved testbinæren; ved separat build må jobben sette `ADMIN_SCAFFOLD_TEST_BINARY` til **faktisk bygget** executable. Ikke bruk en gammel binær eller uverifisert lokal CellProtocol-override. Nye testsuiter er ikke lagt automatisk til CI-filteret; kjør dem eksplisitt som over.

### 2. Eksporter for hver bruker i staging

Kjetil og Vegar gjør dette i hver sin autentiserte nettlesersesjon, med vanlig konto og uten konferansepersona:

1. Åpne `https://staging.haven.digipomps.org/porthole?configurationName=Access%20Requirement%20Prompt&configurationEndpoint=cell%3A%2F%2F%2FAccessRequirementPrompt`.
2. Vent til **Access Requirement Prompt** er lastet. Åpne utviklerverktøy → **Console**.
3. Les og lim inn innholdet i `/Users/kjetil/Build/Digipomps/HAVEN/HAVEN-Deploy/_handoff/ADMIN/rollebevis-20260923/install-in-browser.js`. Trykk Enter.
4. Klikk **Eksporter min offentlige identitet**. Hjelperen sjekker innlogget FidoUser mot de fire oppgitte konto-ID-ene og henter DID fra den samme requesterens AccessRequirementPrompt.
5. Kontroller **requesterUUID** i Porthole Inspector mot raden nedenfor. Ved avvik: stopp og få den nye koblingen målt; ikke rediger UUID for å få bootstrap til å gå gjennom.
6. Samle `kjetil2.public.json` og `vegar.public.json` i en privat staging-inputkatalog. Kjetil gjennomgår offentlig DID, konto, miljø og UUID før utstedelse.

| Miljø | Konto | FidoUser UUID | Forventet requester Identity UUID |
|---|---|---|---|
| staging | kjetil2 | C8C99783-8522-40DE-A427-03E409090587 | DF8D4644-15B2-46F4-A708-CEEB323DA3FE |
| staging | vegar | C2A12943-7CD8-4A02-B325-A2EA17B4769F | 8DCE5C5A-35E7-443E-A4A6-EDE781746CA4 |
| production | kjetil2 | 87FA1CF0-6E67-451D-BCDD-7CE2BFA52C34 | E027291A-7FC8-45CF-8FF9-908DBA41593C |
| production | Vegar | 836F624A-502C-4375-9BDD-5D44784C1F94 | ABA68006-7515-49E8-9160-F4334F948746 |

UUID-er kommer fra Kjetils/Claudes måling i oppgaven, ikke fra ny DB-lesing. DID kommer fra autentisert runtime ved eksport. Eksporten dekoder DID-nøkkelen til `publicSecureKey`; `privateKey:false` er formatets offentlige diskriminator, ikke privat nøkkelmateriale. `date:0` betyr ukjent nøkkelopprettelsesdato i denne eksporten. Ingen `properties`, home-vault-reference, grants, privat nøkkel eller key-agreement-state eksporteres. Bootstrap validerer offentlig input på nytt.

### 3. Root-utstedelse i staging

Forutsetning: patchen er testet/deployet, riktig konto/DID er gjennomgått, fersk koordinering/claim for admincontaineren og et planlagt kort avbrudd. **Kjetil kjører.** `<...>` nedenfor er eksplisitte operatørverdier, ikke ferdige kommandoer.

```bash
/Users/kjetil/Build/Digipomps/HAVEN/HAVEN-Deploy/_handoff/ADMIN/rollebevis-20260923/ceremony.sh prepare staging <absolutt-privat-staging-inputkatalog>
```

`prepare` kopierer bare worker og offentlig input til en ny root-eid 0700-transaksjonskatalog. Den skriver ut en plan med owner, offentlige subjects/DID-er, image-ID og mounts. Den stopper/utsteder ikke. Kontroller planen, og bruk transaksjons-ID-en den skrev ut:

```bash
/Users/kjetil/Build/Digipomps/HAVEN/HAVEN-Deploy/_handoff/ADMIN/rollebevis-20260923/ceremony.sh apply staging <transaksjons-ID>
/Users/kjetil/Build/Digipomps/HAVEN/HAVEN-Deploy/_handoff/ADMIN/rollebevis-20260923/ceremony.sh collect staging <transaksjons-ID> <ny-absolutt-privat-outputkatalog>
```

`apply` er den konkrete eierautoriserte utstedelsen. Den nekter gjenbruk av samme transaksjon og overskriver ingen bundle. En delvis feil kan allerede ha utstedt én bundle: ikke kjør blind retry. Les transaksjonsartefaktene og avklar gjenstående utstedelse. `finally` forsøker alltid å starte opprinnelig manager; hvis restart feiler, blir det feilstatus. Ingen automatisk cleanup eller rollback av signerte bevis.

### 4. Installer hos mottakeren gjennom opplastingsflyten

Hver bruker åpner samme Access Requirement Prompt-side og legger inn nettleserhjelperen igjen ved behov.

1. Klikk **Velg og installer min admin-bundle**.
2. Velg **sin egen** `kjetil2.bundle.json` eller `vegar.bundle.json` fra riktig miljø.
3. Hjelperen sammenligner bundlens subject-DID med innlogget requester, setter promptens proof-keypath og sender **entry først, operator etterpå** til `accessRequirementPrompt.submitCredential` via eksisterende Porthole action-rute.
4. Vent på teksten om at begge er akseptert. Feilmelding om manglende Entity-lagring stopper installasjonen; remote aksept alene er utilstrekkelig. Kontroller kvittering/Entity-record i den eksisterende flaten før restart-testen.

Dette er samme cellehandling, credential-parser, `requestEntry`/`requestRole` og `persistAcceptedCredential` som UI-opplastingen. Forskjellen er at hjelperen velger to konkrete proof-keypaths i den eksisterende personlige prompten, slik at man slipper å få observer/security for å navigere dashboardet. Ingen ny installasjons-API er innført. JavaScriptet godkjenner ingen top-up.

Ved vanlig **Last opp admin-bevis**-kontroll skal `.entry.json` brukes når flaten ber om `AdminEntryCredential`, og `.operator.json` når den ber om operator. Hele `.bundle.json` er ikke et gyldig enkeltcredential for den kontrollen. Ikke last opp operator på et observer-krav.

### 5. Aksept før prod

Kjetil/Claude-jobben utfører og lagrer miljøbevis, uten nye testkjøp eller ekstra kvoteutstedelser utover eksplisitt valgte forespørsler:

- Kjetil godkjenner stagingforespørsel `D03228B6-4B53-4F8D-83CB-2E326DF63131`. Kontroller HTTP 200, `request.status=applied`, `TOPUP_APPLIED` og riktig mottaker/beløp. En 200-respons fra opplasting er ikke dette beviset.
- HTTP-kallet bruker autentisert sesjon, `Content-Type: application/json`, `X-HAVEN-Admin-Request: 1`, og den gjennomgåtte beslutningsbodyen. Tom `{}` beholder forespørselens beløp der policy tillater det. Ikke sett `confirmHighRisk` automatisk.
- Restart **web** kontrollert. Før åpning av admin-Porthole: godkjenn en separat, avtalt reell forespørsel som fortsatt trenger apply. Gjenta etter separat **AdminScaffold**-restart. Samle eksakt web/admin-image og `applied`-bevis.
- Vegar må utføre en reell autorisert handling i sin egen sesjon, i begge miljøer. Kjetils sesjon teller ikke for Vegar.
- Kall mot en **allerede applied** forespørsel returnerer tidlig og utøver ikke `issuePrepaid`. En slik retry beviser **ikke** restart-/rollebanen. Bruk den bare for å sjekke eksisterende idempotent svar.
- Manglende/feil/utløpt/revokert credential skal gi avslag og ingen ny kvote. Bruk fokuserte tester for negative scenarier; ikke revoker eneste fungerende prodcredential som et improvisert forsøk.

Når staging har disse bevisene, gjenta eksport/prepare/apply/collect/installasjon med `production` og `https://haven.digipomps.org` i URL-en. Bruk production-identitetene og egen outputkatalog. Aldri gjenbruk staging-bundle i prod. Seremonikvitteringen sier med hensikt `installed=false` og `approveVerified=false`; senere bevis må registreres separat.

## Fornyelse og 30-dagersgrensen

Grensen er håndhevet både av CLI (`1...30`) og felles `AdminCredentialPolicy.maximumLifetime`. Den gjelder **både entry og operator**, fra hver credentials `issuanceDate`. Endring av `validUntil` i JSON bryter signaturen. Det er ingen automatisk fornyelse i denne leveransen.

For Kjetil betyr dette ny eierutstedelse og ny installasjon for begge brukere i hvert miljø før utløp. Bruk faktisk `validUntil` i bundlene, og planlegg minst sju dager før; policyens `expiringWindow` er sju dager, men det er ikke dokumentert at et varsel faktisk blir levert. Fire personer/miljø-koblinger betyr åtte aktive credentials. Ny utstedelse får nye credential-ID-er; gamle kan revokeres etter at erstatningene er testet.

**Anbefaling: behold 30 dager nå.** Lengre operatorbevis reduserer driftsarbeid, men forlenger konsekvensen av kompromittert adgang. Den praktiske forbedringen bør være en eksplisitt eiergodkjent fornyelsesrutine uten tjenestestopp, med kvittert installasjon og revokering. Det krever eget design/beslutning; HD-0126 fanger dette. Ingen livstidsøkning eller ubetjent root-signering er lagt inn.

## Verifikasjon og åpne porter

Utført lokalt, uten å kjøre seremoni- eller installasjonsskriptene:

- `git diff --check`: OK.
- `bash -n ceremony.sh`, Python AST-parse av begge `.py`-filer, `node --check install-in-browser.js`: OK.
- `HAVEN_PYTHON=/usr/bin/python3 bash ci/check-value-literals.sh`: selvtester og kildekontroll OK. Første forsøk valgte en inkompatibel `/usr/local/bin/python3.12` («Bad CPU type»); eksplisitt system-Python rettet verktøyvalget, ingen kildeendring nødvendig.
- Køvalidering fant tre feilformede fingerprints i andre samtidige lessons; disse er ikke rettet som del av rollebevisoppgaven. HD-0125/0126 og postene er registrert; statusprojeksjonen er oppdatert.
- T0/T1: **4 block, 12 warn**, 15 pass, 3 info. Rapport i seremonikatalogen. Blokkerne er disk (47,7 GiB / 5,1 % ledig), historisk testfixture med annen CP-pin, ikke-initialisert docs-submodul og eksisterende shell-regeltreff utenfor patchen. Ingen bred opprydding, pin-endring eller submodulhenting utført. Rapporten er ikke grønn.

Skrevet, **ikke bygget/kjørt**:

- `AdminFundingCredentialRoutesTests`: faktisk HTTP approve gir 403 uten bevis, UI-handleren persisterer entry/operator, fjernede aktive proof-kopier gjenopprettes av approve uten Porthole, samme forespørsel når `applied`.
- `AdminEntryRemoteBridgeLoopbackTests`: ekte separat AdminScaffold-prosess med ikke-owner, entry+operator, faktisk prosessrestart og gjenpresentasjon, feil subject/rolle, manipulering og revokering. Eksisterende test var owner-only og kunne ikke bevise denne brukerbanen.
- `AdminPresentedCredentialStoreTests`: UUID + signeringsnøkkel, feil proof-keypath, tom ny store og lokal verifier i dedikert runtime.
- Eksisterende expiry/signatur/issuer/persistens/bootstrap/funding-suiter inngår i foreslått testfilter.

En ny faktisk webprosess etter restart, nettleserhjelperen, root-skriptenes miljøadapter og staging/prod-apply er fortsatt **uverifisert**. Brukeren ba eksplisitt om ikke å bygge/kjøre her. Ingen påstand om at top-up nå virker i miljøene.

## Data, innsyn og retensjon

Status: **forslag til gjennomføring**, ikke utført datautlevering. Kilde for konto-ID-er er oppgaven; offentlig nøkkel kommer ved eventuell bruk fra kontoens autentiserte AccessRequirementPrompt. Ingen persondata hentet eksternt i denne økten. Generiske kodekilder ble lest lokalt.

Ved kjøring: nettleser → samme HAVEN-origin, GET `/admin/api/session`; POST `/browserhead/porthole/action` med `{keypath,payload}`. Nettleseren sender eksisterende session-cookie gjennom `credentials:same-origin`; cookie/token skal ikke kopieres til filer eller logger. Payload inneholder offentlig credential eller promptinnstilling. Root-overføring går til verten valgt av `lib/vert.sh`, normalt `89.167.90.101`, med offentlig Identity og gjennomgått worker. Eiernøkkelen forblir på verten, montert read-only i en engangscontainer uten nettverk. SSH-private key leses bare av SSH på vanlig måte.

Privat web-Entity lagrer aksepterte credentials og index som før. Dedikert AdminScaffold beholder midlertidige presentasjoner; prosessrestart tømmer dem, og store rydder ut utløpte presentasjoner ved senere innlegging. Ingen påstand om distribuert backup/sletting.

Anbefalt retensjon for nedlastinger, DID-tekst og lokale/remote bundlekopier: frem til installasjon + restart-aksept er kvittert, deretter maksimalt sju dager. Behold redigerte kvitteringer, credential-ID, utløp og hash som driftsbevis. Skriptene sletter ikke materiale automatisk og endrer ikke Entity-retensjonen. Kjetil avgjør sletting; ingen sletting er utført. Ikke legg rå bundles eller nøkler i Git, køhendelser eller vanlig logg.
