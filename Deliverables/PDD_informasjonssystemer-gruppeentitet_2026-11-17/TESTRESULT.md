# TESTRESULT: Informasjonssystemer som gruppeentitet

Status 2026-11-19. G1, G1-GUI og G2 er godkjent. G3 er ikke vurdert.

## Baseline (WP0), før endringer

| Kjøretid | Resultat | Hvor |
|---|---|---|
| Swift CellBase, Linux-porten (Docker `swift:6.1-noble`, samme kopiering som `cellprotocol-swift-linux.yml`) | 42 tester, 1 hoppet over, 0 feil | CellProtocol b9e7576 |
| Python | 256 bestått, 1 hoppet over | PyCellProtocol b874d65 |
| Go | 86 PASS | GoCellProtocol 9ea5cc9 |

## Etter WP1–WP10

| Kjøretid | Resultat | PR |
|---|---|---|
| Swift, Linux-porten med organisasjons-, TrustedIssuer- og IdentityLink-suitene | 108 tester, 1 hoppet over, 0 feil | CellProtocol #91 |
| Swift, Linux-porten slik CI kjører den (inkl. interop-fixturene) | 65 tester, 1 hoppet over, 0 feil | CellProtocol #91 |
| Python `pytest` | 327 bestått (71 nye), 1 hoppet over | PyCellProtocol #3 |
| Go `go test ./...` | 95 PASS (9 nye), `go vet` rent | GoCellProtocol #37 |

## På Mac-en, 2026-11-19

Kjørt i nye kloner under `/tmp/orgtest-20261119/` på Kjetils Mac (Xcode 27.2, Swift 6.4.2, macOS 27; CI bruker macos-26). Logger i `/tmp/orgtest-20261119/logs/`, sammendrag i `/tmp/orgtest-20261119/logs/summary.txt`.

| Kontroll | Resultat |
|---|---|
| CellProtocol #91 (4878dd5), `swift test --filter InteropFixturesV1Tests` | 2 tester, 0 feil, 1 hoppet over |
| CellProtocol #91, hele suiten | 1977 tester, 0 feil, 6 hoppet over |
| CellProtocol #91, TSan-steget fra `security-regression-macos.yml`, 3 ganger | 249/249, 249/249, og 1 feil i tredje kjøring (se under) |
| `Scripts/verify-transport-security-floor.sh` | PASS |
| CellProtocol main (1ddf107), hele suiten og TSan én gang | 1967 tester, 0 feil; 249/249 |
| Binding (scheme HAVEN, macOS) bygget mot 4878dd5 | Bygger. CellApple kompilerer. |
| BindingTests, pin 36e2959 (dagens) mot 4878dd5 | 707 bestått og 6 feil, mot 706 bestått og 7 feil (738 tester, 25 hoppet over) |
| PyCellProtocol #3, `pytest` | 327 bestått, 1 hoppet over. Slik CI installerer (`.[scaffold,dev]`): 336 bestått |
| GoCellProtocol #37, `go vet` og `go test ./...` | rent; 95 PASS |

Feil som ikke kommer fra dette arbeidet:

- `BridgePeerV3Tests.testPeerMuxHeldPhysicalSubmissionFencesReusedIDAndCIDWhileSiblingWorks` (`BridgeMuxSendLifetimeTests.swift:57`) feilet én av tre TSan-kjøringer. Alene er den 10/10 grønn både på #91 og på main. Den leser deinit-telleren rett etter `hold.release()` og taper kappløpet under last. Samme linje har feilet i CI på en annen gren (fd60666) og på main 9a5bae5. #91 rører ingen bro-, mux- eller transportfiler. Testen kan fortsatt gjøre CI rød til den er rettet.
- To Binding-tester mot `cell://staging.haven.digipomps.org/ConferenceAIGatewayPreview` henger med ny CellProtocol. De henger også med main b9e7576 uten #91, og er grønne med 36e2959. Årsaken ligger i main-endringene mellom de to (bro-livssyklus #87 og admission #90 er nærmest) sammen med levende staging. Binding har ingen CI, så dette møter den som flytter pinnen i Binding.
- `BindingTests/localStartupPortholeExposesAgentSetupWorkbenchWhenOptedIn()` hang i over 20 minutter på dagens pin og ble hoppet over.

## Tester knyttet til formålene

| Test | Swift | Python | Go |
|---|---|---|---|
| test.ge.genesis (forsegling, endret felt, manglende signatur, utenforstående) | ✓ | ✓ | ✓ |
| test.ge.not-person (ingen person blir same_entity med gruppa) | ✓ | – (ingen IdentityLinkRegistry i portene) | – |
| test.ge.agreement-templates (8 tilfeller, umulig krav avvises når policyen lages) | ✓ | ✓ | ✓ |
| test.ge.owner-change (Kjetil alene → Petter lagt til → tredje eier krever begge) | ✓ | ✓ | ✓ |
| test.ge.chain-negative (hoppet versjon, feil forgjenger, byttet innhold, rolleforslag som endring) | ✓ | ✓ (delvis) | ✓ (delvis) |
| test.ge.vault-negative (feil nøkkel, gjenbrukt nonce, endret innhold, feil sammendrag) | ✓ | – (hvelvet er Swift-only) | – |
| test.ge.journal (hvem godkjente hva, hashkjede) | ✓ | – | – |
| test.ge.role-vc-fixture (samme bytes og signatur på tvers) | ✓ | ✓ | ✓ |
| test.ge.revoke-next-access, test.ge.status-offline | ✓ | ✓ | ✓ |
| test.ge.condition-interop (felles tabell, 7 scenarioer) | ✓ | ✓ | ✓ |
| test.ge.issuer-not-trusted | ✓ | ✓ | ✓ |

Felles fasit: `fixtures/interop/v1/org.*` (23 signerte tilfeller) og `org.access-matrix.json` (7 scenarioer), laget av Swift og kopiert uendret til Python og Go. Hver port bygger også policy, forsegling, rolle-VC og statusliste selv og får de samme bytene som Swift.

Testene er kontrollert mot én bevisst feil ("én person teller én gang" slått av): 6 Python-tester og 3 Go-tester feilet, som de skal.

## Avvik fra planen

- Den første, tomme statuslisten (sekvens 1) signeres når hvelvet opprettes, uten en godkjenningsrunde, slik at speilet finnes fra første dag. Den journalføres med ruleID `genesis`.
- Hvelvet har sin egen journal og sitt eget nonce-sett, i stedet for å gjenbruke `EntityAuthorityJournal` eller `CellSecuritySigningChallengeReplayStore`, som begge er laget for andre formål.
- Python og Go porterer ikke selve `ProvedClaimCondition`, men de TrustedIssuer-sjekkene vilkåret bygger på (`role_access` / `RoleAccess`), med de samme årsakskodene. Den felles tabellen viser at de gir samme svar.
- Tilgangsmatrisen kjører som tabelltester i hver kjøretid, ikke som en levende node-til-node-matrise i `interop/matrix`. En levende "org"-flyt kan legges til der senere.
- Python-CI kjører ikke `pytest`, bare den levende matrisen. Python-testene er derfor bare kjørt lokalt.

## Funnet underveis, ikke rettet

`AnyKeypathExpression.parseStatement` (Swift) leser `a == "x"` som operatoren `=` med verdien `= "x`, fordi `=` står før `==` i regex-alternativene. Et vilkår skrevet med `==` treffer derfor aldri en tekstverdi. Det stenger, det åpner ikke. Vilkårene i dette arbeidet bruker `=`, som de eksisterende testene.
