# Granskning av WP-S1-diffen (Losen, 2026-09-12 kl. 22:05)

Diff lest linje for linje mot ren eksport av origin/main 649255bb (`diff -u` fra `_worktrees/baseline-…/CellScaffold`): `Sources/App/Cells/Agent/AssistantCorrespondenceCell.swift` (82 endrede linjer), `Tests/AppTests/AssistantCorrespondenceCellTests.swift` (435), `Documentation/Staging_Deployment.md` (13). Basissemantikk lest i CellProtocol på pinnet revisjon e03923cb (`Package.resolved`), ikke i arbeidstreet.

## Holder
- `validateCellSpecificAccess` OR-es med kontrakter i `authorizationDecisionWithoutRecording` (GeneralCell.swift l. 2028) og er slått av for eier — så `r---` på `feed` for en aktiv principal gis uten å røre malen. Riktig sted.
- Basens `flow(requester:)` (l. 1216–1224) krever `validateAccess("r---","feed")` og pakker feeden i `feedAuthorizations.publisher(authorize:)`; overstyringen kaller `super` først, slipper eier ufiltrert og filtrerer alle andre på topic + `message.send`/`message.ack` + `recipientID == principalID`, med grantsjekk per hendelse. Revokasjon/utløp stopper strømmen ved neste hendelse.
- `makeCellOwnedFlowEmitterForRuntimeBinding(requester:)` (l. 2492–2505, `@_spi(HAVENRuntime)`) krever `isAllowedToSetupIntercepts` — kalles i `setupKeys(owner:)` med eier, så emitteren finnes når nøklene finnes. Hendelsen sendes derfor uavhengig av innringerens skriverett — det som stoppet ikke-eiere over bro (VALIDERING a3).
- `emitEvent` kalles etter at `handle()` har returnert (l. 551), ikke inne i `stateQueue.sync`; filteret sjekker topic før det rører `stateQueue`, så administrative hendelser gir ingen låsing. Ingen deadlock-vei funnet.
- Tester: ingen hel-objekt-`XCTAssertEqual`, ingen `sleep`; ni tester dekker (1)–(5) fra oppdraget pluss revokasjon/utløp, administrativt topic/malformerte hendelser og rebinding etter decode.

## Merk (ikke stopp)
- `emitCorrespondenceFlow?(flow)` dropper stille hvis emitteren ikke er installert (f.eks. `setupKeys` ikke kjørt). Samme risiko som før (`pushFlowElement` droppet stille uten rett), men nå avhengig av init-veien; testen for rebinding etter decode dekker det. Vurder logglinje ved `nil`.
- `verifyRequesterIdentityControl` gjør en signeringsutfordring mot `identity.identityVault`; over bro må bro-kommandoens identitet bære vault/bevis — det er D1b/e2e som avgjør, ikke enhetstestene.
- Codex' avvik er riktige og viktige: standardavtalen bærer `r---` på `feed` (Agreement.swift:104), så filteret — ikke fraværet av grant — er det som beskytter; `AgentTrustPackageCell.swift` finnes ikke på origin/main (Fable-tråden leste det i det skitne arbeidstreet på `pdd/tillitspakke-agentflaate`); `ChatCell.flow` filtrerer ikke. Tre presedenser i VALIDERING.md var altså lest fra feil tre. Rettes i FORMAALSSPEC §1c.
- Dokumentasjonen havnet i `Documentation/Staging_Deployment.md` (det Codex fant med grep). Riktig plass er der correspondence-cellen beskrives; flyttes i WP-Docs, ikke nå.
- `@_spi(HAVENRuntime) import CellBase` i en App-celle: presedens `RichDocumentCell.swift:64` ifølge Codex; akseptabelt, men SPI er ikke API — noter i docs.

## Konklusjon
Klar for bounded bygg + testklasse (`scripts/run_swift_bounded.sh test --filter AssistantCorrespondenceCellTests` i worktreet). Ikke klar for PR før det er grønt og `swift-format`/CI-regler er kjørt i ekte bygg. Status: **skrevet, ikke verifisert**.
