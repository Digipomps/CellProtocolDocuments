# TESTRESULT — varsel om ny post, hendelsesbasert (HD-0069)

Ekte utdata under ankrene testene i FORMAALSSPEC.md §5 navngir. «blocked» + grunn der en test ikke kunne kjøres. Ingenting her er «levert» før ACCEPT.md sier det.

## Baseline (WP0) <a id="build"></a>

Kjørt 2026-09-12 kl. 21:42–21:50 (Oslo) av Kjetil via `handoff/KJOR-SELV-forbered-wp0-og-wp-s1.sh --run` → `evidence/wp0/baseline.sh --run`. Ren eksport (`git archive origin/main`) til `_worktrees/baseline-corr-varsel-20260912T214235/`. Logg: `evidence/wp0/baseline-20260912T214235.log`, sammendrag: `evidence/wp0/SUMMARY-20260912T214235.md`.

| Repo | origin/main | swift build | Test | Resultat |
|---|---|---|---|---|
| HavenAgentD | 551d37a | exit 0 | `swift test` (fullt) | **241 tester i 48 suiter, alle grønne** (`Test run with 241 tests in 48 suites passed after 4.119 seconds`) |
| CellScaffold | 649255bb | exit 0 | `swift test --filter AssistantCorrespondenceCellTests` | **16 XCTest-tester, 0 feil** (`Executed 16 tests, with 0 failures`); Swift Testing-linjen «0 tests in 0 suites» gjelder det tomme Swift Testing-målet |

Avvik i selve baseline-kjøringen: `Scripts/preflight_before_landing.sh` og `Scripts/assert_dependencies_are_on_their_main.sh` ga exit 127 («No such file») fordi skriptet kjørte dem i den *lokale* HavenAgentD-utsjekken, som står på lokal main ba14895 (før skriptene fantes) — ikke i eksporten. Rettet i `baseline.sh` 12.9 kl. 22:10 (kjøres fra eksporten neste gang). Baseline-tallet er ikke berørt.

## Regresjon <a id="regression"></a>

Forventet ≈ 241 (HavenAgentD, fra WP0 12.9) og ≈ 16 i det filtrerte CellScaffold-løpet. Kjøres på nytt etter hver arbeidspakke; første måling etter WP-S1 venter (se #auth).

## Server: mottaker-skopet feed (WP-S1, HD-0072) <a id="auth"></a>

Kode og ni tester **skrevet av Codex 12.9 kl. 21:43–21:57** i `_worktrees/cellscaffold-corr-varsel-s1` (gren `pdd/corr-varsel-recipient-feed`), rapport `CORR_VARSEL_S1_RAPPORT.md`, Losens gjennomlesing i `evidence/wp-s1/GRANSKNING.md`. **Status: skrevet, ikke verifisert** — Codex' sandkasse kan ikke bygge; bounded bygg + testklasse kjøres av Kjetil (post 1 på HD-0072), utdata legges her:

### Måling 2026-09-14 kl. 23:03 (Kjetil kjørte `KJOR-SELV-wp-s1-bounded-test.sh --run`)

Logg: `evidence/wp-s1/bounded-test-20260914T230304.log` (7,3 MB), sammendrag `evidence/wp-s1/RESULT-20260914T230304.md`.

```text
Executed 25 tests, with 10 failures (0 unexpected) in 1.759 seconds
exit=1
```

25 = 16 baseline + 9 nye. **Alle 16 baseline-testene er fortsatt grønne — ingen regresjon.**
De 10 feilene er assertions fordelt på **6 av de 9 nye testene**:

| Ny test (linje i AssistantCorrespondenceCellTests.swift) | Utfall | Symptom |
|---|---|---|
| `testFeedWithoutGrantOrWithPendingApprovalThrowsStreamStateDenied` (1393) | grønn | — |
| `testFeedRejectsSameUUIDWithWrongKeyAndIdentityWithoutKeyControl` (1409) | grønn | — |
| `testActiveGrantReceivesOwnSendFromSenderWithoutFeedWriteAccess` (1423) | **rød** | `XCTUnwrap failed: expected non-nil value of type "FlowElement"` |
| `testRecipientFeedExcludesOtherRecipientsSendAndAck` (1465) | **rød** | fikk `[message.send]`, ventet `[message.send, message.ack]` |
| `testInboxListAndMessageReadNeverReachRecipientFeed` (1513) | grønn | — |
| `testOwnerKeepsAllOperationEventsAndNoFeedEventContainsMessageContent` (1537) | **rød** | fikk 3 hendelser, ventet 4 — `message.ack` mangler |
| `testExpiredOrRevokedGrantDeniesNewFeedAndStopsExistingSubscription` (1590) | **rød** | `XCTUnwrap failed: expected non-nil FlowElement` |
| `testRecipientFeedExcludesAdministrativeTopicAndMalformedEvents` (1617) | **rød** | `0 != 1 — Owner must still see the event` (5 assertions) |
| `testRecipientFeedAndCellOwnedEmissionSurviveRuntimeRebindingAfterDecode` (1649) | **rød** | fikk `[]`, ventet `[message.send]` |

**Mønster (måling, ikke årsak):** alle tre grønne er *negative* tester — de krever at noe **ikke** når fram. Alle seks røde krever at en hendelse **faktisk ankommer**. En feed som ikke leverer noe som helst består de negative testene trivielt; de tre grønne er derfor svakt bevis så lenge de seks røde står.

**Hypoteser som er testet og forkastet** (lest i `Sources/App/Cells/Agent/AssistantCorrespondenceCell.swift` i worktreet):
- «`operation` ligger bare i `FlowElement.title`, så filteret på `event["operation"]` bommer» — **forkastet**: `"operation"` settes i resultatobjektet (l. 1461, 1481, 1552, 1583).
- «`message.ack` returnerer en status utenfor `["sent","acknowledged","ok"]`, så `emitEvent` aldri kalles» — **forkastet**: ack returnerer `"acknowledged"` (l. 1582), som er i lista (l. 550).

**Ikke avklart:** hvorfor hendelser uteblir. Gjenstående spor er `emitCorrespondenceFlow` som er `nil` på testenes init-vei (emitteren settes i `setupKeys(owner:)`, l. 188, og `emitCorrespondenceFlow?(flow)` dropper stille når den er nil, l. 2014) — nøyaktig risikoen `GRANSKNING.md` flagget som «Merk (ikke stopp)». Det forklarer *ikke* tilfellet der `send` kommer fram men `ack` ikke gjør det; der må det være minst én defekt til. Overlatt til diagnosejobb `wp-s1-diagnose-20260915`.

**Status for testradene:**
- test.cell.auth-negative: **grønn, men svak** — 3/3 negative tester passerer, se forbeholdet over
- test.corr.flow-received (server-halvdel): **rød** — 6/9 nye tester feiler; WP-S1 er ikke klar for PR

## Øvrige ankre

#flow-received (agent), #no-polling, #challenge-shape, #no-duplicates, #no-body, #no-secrets, #ack-resolves, #no-auto-ack, #contract, #challenge-flow, #identity, #bridge, #menu-latency, #unreadable, #catch-up, #e2e, #running, #contract-skew, #staging-path, #staging-build: venter (arbeidspakkene er ikke startet).
