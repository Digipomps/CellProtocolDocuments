# k16 — PR67: isoler inbound signeringskvote

Dato: 2026-10-13. Utfører: Codex. PR: https://github.com/Digipomps/CellProtocol/pull/67

Arbeidstreet er `_worktrees/k15-candidate/CellProtocol`, på den autoriserte grenen
`codex/k15-attachment-staging`. Utgangspunkt: `fee5cbacd254be97d5775b819b4f2f907373724e`.
Ny head: `80112915443e52d1f642525d34abcce89c5fb71d`. Pushet til samme gren; PR-beskrivelsen er oppdatert. Alle fem CI-kontroller er grønne på denne headen. Ingen merge, tag, deploy, installerbygg eller vertsendring.
Kun syntetiske testidentiteter. Urelaterte endringer i hovedklonene er ikke tatt med.

## Funn og retting

Filhenvisninger under gjelder CellProtocol i arbeidstreet på denne grenen.

| Funn | Endring / vurdering | Kilde |
|---|---|---|
| Inbound belaster delt kvote | Retning er eksplisitt og obligatorisk. Bare utgående `signMessageForIdentity` bruker native endpoint/publisher-scope; inbound bruker broens UUID. | `Sources/CellBase/Cells/Bridging/BridgeBase.swift:1147`, `:1254`, `:1276`, `:1574` |
| For bred pre-effekt-catch | `sendMessage` binder retry bare rundt `authorizeAttachment`; `storage.publish` har separat vanlig feilbehandling. `performAttachment` binder retry umiddelbart rundt autorisasjonen, før effektene. Registrert handler videreformidler bare allerede bundet avslag. | `Sources/CellBase/Cells/Correspondence/CorrespondenceCell.swift:771`, `:778`, `:1270`, `:1282` |
| Vedleggstekst på alle GET-avslag | Retry-avslag bruker `signingTemporarilyUnavailable`. Markør, reasonCode og retryAfterSeconds er uendret; vanlig vedleggsfeil er uendret. | `Sources/CellBase/Cells/Bridging/BridgeSigningBackpressure.swift:17`; `Tests/CellBaseTests/BridgeSigningBackpressureCodecTests.swift:6` |
| Upinnet policy i lagringsfeiltest | Egen controller og eksplisitt `.localProtection`, med gjenoppretting i defer. | `Tests/CellBaseTests/BridgeSigningBackpressureTests.swift:159` |
| Punkt 2: historisk backpressure innen én kommando | Vurdert, ikke endret. Tilstanden er fortsatt per kommando, men et tidligere kvoteavslag kan prege et senere reelt avslag. Bare å nullstille ved signeringsstart dekker ikke autorisasjonsavslag uten et nytt signeringsforsøk; en full retting bør binde feilårsaken til den konkrete autorisasjonsvurderingen og teste flere/samtidige bevisforsøk. Dette er et åpent, ikke-blokkerende restpunkt. | `Sources/CellBase/Cells/Bridging/BridgeSigningBackpressure.swift:39`; `Sources/CellBase/Identity/BridgeIdentityVault.swift:24`; `Sources/CellBase/Cells/Correspondence/CorrespondenceCell.swift:432` |

### Presisering av trusselbeskrivelsen

Oppdraget sier at identiteten i inbound `.sign` er «peer-valgt og ikke autentisert».
Den delen støttes ikke av den leste native-stien: `BridgeBase.consumeCommand`
kaller `channelSession.checkInbound` før rate-limit. `BridgeChannelSession.checkInbound`
(`Sources/CellBase/Cells/Bridging/BridgeChannelSession.swift:303`) kaller for native-kanalen
`check(identity:requiresIdentity:)` (`:405`), som sammenligner identiteten med kanalens
autentiserte public identity. At `requester(for:)` hoppes over betyr ikke at denne
første identitetskontrollen hoppes over. Lokal operation/permit-autorisasjon skjer senere.

Regresjonen beviser derfor kvoteinterferens mellom forbindelser for **samme autentiserte
identitet**, endepunkt og publisher, ikke at en annen autentisert identitet kan forgifte
vilkårlige lokale identiteters kvoter. Rettingen av det delte inbound-scopet er likevel
nødvendig for isolasjonen oppdraget krever.

## Rød → grønn

Ny test: `Tests/CellBaseTests/BridgeSigningBackpressureTests.swift:60`,
`testInboundSigningFloodDoesNotExhaustAnotherConnectionQuota`.
To ekte autentiserte fixture-sessioner bruker samme identitet, endepunkt og publisher.
Den første sender 24 inbound `.sign` uten en aktiv lokal operation/permit; alle avvises.
Den andre må fortsatt få et signert bevis, som verifiseres kryptografisk.

| Kjøring | Resultat | Bevis under `HAVEN-Deploy/_handoff/KORR-UT/k16/` |
|---|---|---|
| Uendret produksjonskode på `fee5cba`, bare ny test lagt til | **Rød**, exit 1, én test / én assertion-feil: søskenforbindelsen fikk `BridgeSigningBackpressure(retryAfterSeconds: 60)` | `red-test-r2.log`, `red-test.patch` |
| Rettet kandidat, filter `BridgeSigningBackpressure` | **Grønn**, exit 0, 10 tester, null feil | `green-focused.log` |
| Full `swift test` i begrenset prosess | Exit 1; tre Keychain-feil i `AppleIdentityVaultKeyStorageTests` (`EPERM` / `-25291`). Dette er ikke rapportert som grønn fullport. | `full.log` |
| Første Mac-køforsøk | Exit 153 før tester; Swift traff køens standardgrense på 2 GiB per fil | `full-native.log`, `full-native-queue.txt` |
| Full lokal Mac-port, samme filgrenseinnstilling som k15 | **Grønn**, exit 0; 1699 tester, fem utelatt, null feil (26 HavenCommons + 3 CellNearby + 1670 CellBase) | `full-native-r2.sh`, `full-native-r2.log`, `full-native-r2-queue.txt` |

De tre sandbox-feilene var `testLegacyEmbeddedPrivateKeyMigratesToApplicationTagAndSigns`,
`testLegacyEmbeddedPrivateKeyStillSigns` og `testScopedSecretDataStaysStableInUnsignedTestHost`.
Alle passerte i den fullførte native-kjøringen. Test-/skripthasher står i `evidence-sha256.json`.

Fokusert grønn kjøring inkluderer eksisterende
`testNewAuthenticatedConnectionDoesNotResetSigningQuota` (`:110`), som krever avslag
etter kanalbytte når utgående kvote er brukt opp; begge indre/ytre autorisasjonsgrenser;
og negativer for ukjent lagringsutfall, sen autorisasjonsfeil og barneavslag etter
foreldreeffekt. Den nye codec-testen verifiserer at friteksten ikke styrer retry-dekoding.

De to første testoppsettene ble korrigert før det gyldige røde beviset: feil arbeidskatalog
(`red.log`, fant ikke Package.swift) og async-kall i XCTest-autoclosure
(`red-test.log`, kompileringsfeil). Disse teller ikke som regresjonsbevis.

Kommandoen i alle kjøringer bruker den eksisterende
`CellScaffold/_worktrees/k15-attachment-staging/scripts/run_swift_bounded.sh`, fra
CellProtocol-arbeidstreet, med `test --jobs 2`; de direkte sandbox-kjøringene legger til
`--disable-sandbox`. Fokuserte filtre er angitt over. Samme cache-nøkkel som k15:
`k15-protocol-tests`; kapasitetssjekk, leie og to jobber beholdes. Runneradapteren
`k16/swiftpm-retain` setter `--dry-run` for å unngå cache-sletting. Ingen delt datamappe
ble ryddet. Native r2 bruker samme `ulimit -S -f unlimited` som k15s fulltest;
diskkapasitetsporten er uendret. Eksakt diff-hash, Swift/plattform og hash av Package.resolved står i
`candidate.json`; køskriptet verifiserer base, gren og diff før/etter fulltesten.

Linux-CI er grønn: https://github.com/Digipomps/CellProtocol/actions/runs/38324578370 .
Den fullførte loggen `HAVEN-Deploy/_handoff/KORR-UT/k16/ci-linux.log` viser eksplisitt
`passed` for den nye isolasjonstesten, renewal-testen og den nye codec-testen.

## Klient og kompatibilitet

Lest `_worktrees/k15-agentd-client/Sources/HavenCorrespondenceMCP/CorrespondenceSigningRetry.swift:6`:
klienten fanger den typede `BridgeSigningBackpressure`, venter bounded og forsøker en ny
operasjon. Den tolker ikke `message`. Protokollens decoder bruker markør/reasonCode/tid.
Ingen klientendring er nødvendig for denne rettingen; HavenAgentD er ikke endret eller
bygget her. Klientens publiserte avhengighetspin må senere følge den protokollrevisjonen
som faktisk velges for integrasjon; dette oppdraget publiserer ingen release.

## Commit, CI og læring

Commit `80112915443e52d1f642525d34abcce89c5fb71d`: `Isolate inbound signing quotas and narrow pre-effect retry boundaries`.
Eksakt commit-diff matcher den fulltestede diff-hashen; arbeidstreet er rent. Eksisterende PR67-CI og siste main-CI var grønne
før arbeidet. Actions-bruk ble lest med organisasjonens billing usage summary; den gamle
billing/actions-ruten returnerte HTTP 410. Bruksoversikten beviser ikke gjenstående budsjett.

CI ferdig verifisert mot PR-ens `headRefOid` etter at `gh pr checks --watch` avsluttet
med exit 0. PR-en er fortsatt OPEN/DRAFT, på samme gren. Maskinlesbar kvittering:
`HAVEN-Deploy/_handoff/KORR-UT/k16/ci-final.json`.

| Kontroll | Resultat | Lenke |
|---|---|---|
| Persisted Cell file bounds | SUCCESS | https://github.com/Digipomps/CellProtocol/actions/runs/38324578370/job/115060175196 |
| regression | SUCCESS | https://github.com/Digipomps/CellProtocol/actions/runs/38324578352/job/115060175321 |
| Dispatch PyCellProtocol upstream sync | SUCCESS | https://github.com/Digipomps/CellProtocol/actions/runs/38324576491/job/115060170142 |
| bounded synthetic runtime matrix | SUCCESS | https://github.com/Digipomps/CellProtocol/actions/runs/38324578394/job/115060175238 |
| Vapor identity vault strict storage | SUCCESS | https://github.com/Digipomps/CellProtocol/actions/runs/38324578361/job/115060175161 |

macOS-kontrollen inkluderer ordinær test av eksakte kilder/pinner, Thread Sanitizer og
negativ kontroll av sårbar transportpinne. CI-fulltesten passerte 1699 tester med fem
utelatt og null feil; Thread Sanitizer passerte tre kjøringer à 232 tester, null feil.
Dette er gjentatte kjøringer, ikke 696 unike tester. Ny isolasjonstest og renewal
er eksplisitt bekreftet grønne også i macOS-loggen. Ferdig logg: `k16/ci-macos.log` under
bevismappen. Ingen CI-omkjøring eller ekstra kodepush var nødvendig.

Læring `L-2026-10-13-separate-incoming-and-outgoing-signing-budgets` er anvendt i
`CellScaffold/.claude/skills/cellprotocol-transport-bridging/SKILL.md`: skillen skiller
retning, autentisert principal og lokal signing-permit, og krever begge kvotetestene.
Synkronisering fullført via eksisterende Mac-kø: Claude, Codex, Desktop-store og ZIP.
Bevis: `HAVEN-Deploy/_handoff/KORR-UT/k16/learning-sync-queue.txt`.
Cowork-pluginens manuelle opplastingskopi oppdateres ikke automatisk av denne synken.
Global `haven_learn.py check --strict` er fortsatt rød på andre, eldre åpne læringer;
denne læringen er applied og synced. Ingen andres læringer er endret.

STATUS: LEVERT
