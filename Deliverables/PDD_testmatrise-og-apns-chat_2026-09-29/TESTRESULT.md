# TESTRESULT — testmatrise og apns chat

Alle tall er limt fra logger på Kjetils Mac (`handoff/…`), kjørt 06.10.2026 14:07–15:00. «Grønn» betyr siste sammendragslinje for riktig test-bundle, `0 failures (0 unexpected)` (jf. `lesson.green-gate-must-read-the-last-summary-line`; `swift test` i CellScaffold skriver flere bundler — AppTests-linjen er den som teller).

## #build
WP0 — `handoff/baseline-20261006-140714/baseline.log` (origin/main: CellProtocol 1ec56d5, CellScaffold e5c34345, Binding 8ce634f6).

| Repo | Mot hva | Resultat |
|---|---|---|
| CellProtocol | main (1ec56d5) | `swift build`: OK |
| CellScaffold | pinnet CellProtocol 2026.9.4 (81601a6) + DiMyMint/DiMyMicropayments 2026.9.4 | `swift build`: OK |
| CellScaffold | CellProtocol **main** | **FEILET** — `VaporPersonEntityReadRoute.swift:172:15: error: call can throw but is not marked with 'try'` (og samme i `Tests/AppTests/EntityPersonBridgeProcessTests.swift:470`). Årsak: CellProtocol #53 gjorde `BridgeTransport.sendData` throwing. Ikke et release-brudd (CellScaffold er pinnet til taggen), men CellScaffold må få to `try` før pinnen kan løftes. |
| Binding | macOS, `CODE_SIGNING_ALLOWED=NO` | `** BUILD SUCCEEDED **` |

## #regression
**Baseline (før vår kode)**

- CellProtocol main, `swift test --filter CellBaseTests`: `Executed 1528 tests, with 5 tests skipped and 0 failures (0 unexpected) in 45.697 seconds` → GRØNN.
- CellScaffold pinnet, hele suiten, AppTests-bundelen: `Executed 2746 tests, with 17 tests skipped and 139 failures (6 unexpected) in 329.035 seconds` → RØD fra før. 36 røde testcaser, listet i `handoff/baseline-failures-pinned.txt` (Book-ruter, AIAssistantThreadCellTests, ConferenceSurfaceRoutesTests, MarkdownRendererCellTests, SkeletonRuntimeSourceTests m.fl.). Kjørt to ganger mot pinnen (baseline 140714 og fase 1-kjøringen 142305): samme 36 begge ganger. `lesson.a-new-red-test-needs-a-repeated-baseline` ber om tre; en tredje kjøring gjenstår før listen kan kalles stabil.
- CellScaffold main × CellProtocol main (kontroll, bare `try`-rettelsene): `Executed 2746 tests, with 17 tests skipped and 152 failures (10 unexpected)`, 42 røde — 6 flere enn mot pinnen: `AdminEntryRemoteBridgeLoopbackTests.testStoredEntryCredentialVerifiesThroughRunningAdminScaffoldBridge`, `EntityPersonBridgeProcessTests` (2), `PortholeWebRemoteConfigurationTests.testRemoteLookupLoadsExportOverInMemoryBridgeAndReadsLivePublisher`, `SkeletonElementParityMatrixTests` (2). Følger av CellProtocol main, ikke av oss. Liste: `handoff/baseline-failures-cpmain.txt`.

**Etter vår kode**

- CellProtocol (gren `pdd/testmatrise-apns`), hele CellBaseTests: `Executed 1559 tests, with 5 tests skipped and 0 failures (0 unexpected) in 45.780 seconds` → GRØNN (1528 + 31 nye). `handoff/phase1/run-cp-20261006-143637/apply.log`.
- CellScaffold fase 1 (gren `pdd/testmatrise-apns`, pinnet CellProtocol): 36 røde = baseline, «NYE RØDE: ingen». `handoff/phase1/run-20261006-142305/apply.log`.
- CellScaffold fase 2 (gren `pdd/testmatrise-apns-dev`, mot CellProtocol-grenen): `Executed 2766 tests, with 17 tests skipped and 152 failures (10 unexpected)`; røde sett **identisk** med kontrollen (`diff` tomt, 42 = 42). Ingen regresjon som skyldes vår kode. `handoff/phase1/run-p2-20261006-144523/`.

## #apns
| Test (§5) | Dekket av | Resultat |
|---|---|---|
| `test.apns.token-registration-signed` | `HavenPushRegistrationTests` (usignert, endret token, annen entitet, ugyldig token/bundle, utdatert, nøkkelbytte), `InvitePushDispatcherTests.testRegisterPersistsAndSurvivesARestart`, `testStoredFileHoldsNoNameAndNoTokenAfterRevocation`, `testUnsignedRegistrationIsNotStored` | `Executed 31 tests … 0 failures` (CellProtocol), `Executed 20 tests … 0 failures` (CellScaffold) |
| `test.apns.token-revoke` | `testRevokeClearsTokenAndKeepsOnlyTheTime`, `testOnlyTheOwnerCanRevoke`, `testApnsUnregisteredMarksTheTokenRevokedInternally`, dispatcher `testApnsUnregisteredRevokesTheTokenAndNextDispatchSaysTokenRevoked` | grønn |
| `test.apns.payload-has-no-content` | `InviteApnsPushTests` (gylden payload byte for byte, kun avtalte nøkler, ingen avsendernavn/tekst, headers, utløp = min(billett, 14 d), ugyldig input, tilpasset ticketID), `contract/validate_contract.py` | `Executed 9 tests … 0 failures`; `RESULT: 12 grønne, 0 røde` |
| `test.apns.wrong-audience-not-pushed` | `testOnlyTheNamedEntitysDevicesAreTargets`, `testIssuerNamingThemselvesIsWrongAudience`, `testMalformedAudienceEntityIsWrongAudience`, `testTamperedPublicationIsNotPushed`, dispatcher `testDispatchSendsExactlyOnePushToTheNamedAndRegisteredEntity` | grønn |
| `test.apns.tombstone-blocks-push` | planlegger `testTombstoneFromTheSameIssuerToTheSameAudienceBlocksPush`, dispatcher `testRevokedAndTombstonedAreNotSent` | grønn |
| `test.apns.expired-not-pushed` | `testExpiredTicketIsNotPushed`, `testRevokedTicketIsNotPushed` | grønn |
| `test.apns.unresolved-not-pushed` | `testNoAudienceEntityMeansNoPush`, dispatcher `testNothingIsSentWithoutANamedAudienceEntity` (selve oppslaget, WP13, er ikke bygget) | delvis grønn: beslutningen ja, resolveren ikke |
| `test.apns.tap-opens-verified-invitation` | — | **blocked**: app-siden (Binding) ikke skrevet; avhenger av invitasjon runde A del 2 |
| `test.apns.real-sandbox-send` | — | **blocked**: venter på `APNS_*`, push-entitlement og enhets-token fra Kjetil (`handoff/iphone-sjekkliste.md`) |

Tillegg som ikke var i §5: `HavenInvitePushPlannerTests.testSenderViewHasNoVocabularyForPushOutcomes` og `testAudienceEntityIsSignedButNotInTheTicket` (lenken navngir aldri mottakerentiteten; feltet er dekket av signaturen; gamle publiseringer får uendrede kanoniske bytes).

## #push
`test.push.*` (WP5) — `handoff/snapshot-alle-go-20261004.log`:

- `test.push.hash-read-after-push`: lokal = origin for alle fire grener: CellProtocol `c74d654`, CellScaffold `d3bc59a`, Binding `79332f8`, CellProtocolDocuments `d17c845`.
- `test.push.snapshot-no-disturbance`: «uberørt: JA» for alle fire (HEAD, indeks og arbeidstre uendret).
- `test.push.no-secrets`: tre hemmelighet-regex-treff holdt ute (innhold ikke åpnet), 22 filer > 5 MB holdt ute; ingen av dem på grenene.

## #contract
`python3 contract/validate_contract.py` → siste linje `RESULT: 12 grønne, 0 røde` (positive: payload_invite, register_valid; negative: 10, hver feiler av riktig grunn). Gylden payload i `InviteApnsPushTests` er sjekket likeverdig med `fixtures/positive/payload_invite.json`.

## #blocked
- `test.matrise.same-scaffold-three`, `cross-scaffold-chat`, `staging-waiter-chain`: venter på invitasjon runde A del 2 og WP7 (ChatCell-klar), og Palazzo-vert.
- `test.matrise.admin-cannot-enter-other-scaffold` (WP8a), `test.matrise.prod-readonly-smoke` (WP9a, venter på Kjetils eget ja), `test.matrise.device-profiles` (script `matrix.sh` skrevet, ikke kjørt), `test.invite.resolve-*` (WP13): ikke kjørt ennå.
- `test.apns.tap-opens-verified-invitation` (UI-del), `test.apns.real-sandbox-send`: se #apns.

## Funn som ikke var i planen
1. CellScaffold main kan ikke bygges mot CellProtocol main (to manglende `try`, se #build).
2. 36 røde tester i CellScaffold allerede mot pinnet CellProtocol, 42 mot main. Eies ikke av denne oppgaven, men er nå dokumentert og låst som baseline.
3. `Package.resolved` i CellScaffold endres av SPM når den bygges mot lokale pakker — skal ikke med i commit.
