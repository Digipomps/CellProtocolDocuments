# WP-S1 — mottaker-skopet feed på AssistantCorrespondenceCell (HD-0072)

Du jobber i worktreet `_worktrees/cellscaffold-corr-varsel-s1` (CellScaffold, gren `pdd/corr-varsel-recipient-feed` fra `origin/main`). Ikke rør `.git`, ikke commit, ikke push — det gjøres etterpå av et eget steg. Skriv aldri «levert» eller «verifisert»: rapporter «skrevet, ikke verifisert» inntil et bygg utenfor denne sandkassen har kjørt.

## Formål (mål alt du gjør mot dette)
`purpose://candidate.corr-varsel.recipient-scoped-events` — En enrollet principal skal kunne abonnere på correspondence-cellens hendelser over bro og bare få hendelser adressert til seg (`message.send` / `message.ack` med egen `recipientID`), uten meldingsinnhold og uten å se andre principalers metadata. Måles ved tester: (1) abonnent uten grant får `StreamState.denied`; (2) abonnent med aktiv grant får egen `message.send`-hendelse; (3) samme abonnent får IKKE en annen mottakers `message.send`; (4) `inbox.list`- og `message.read`-hendelser når aldri en abonnent; (5) ingen hendelse bærer `content`.

## Dagens tilstand (lest 2026-09-12, fil:linje i CellScaffold og CellProtocol)
- `Sources/App/Cells/Agent/AssistantCorrespondenceCell.swift`: `emitEvent(operation:result:requester:)` l. 1720–1735 pusher én FlowElement per operasjon via `pushFlowElement(flow, requester:)`, tittel `haven.assistant.correspondence.<operasjon>`, topic `AssistantCorrespondenceContracts.flowTopic` (`AssistantCorrespondenceContracts.swift` l. 16), med `message` uten `content`; kalles for alle operasjoner fra l. 441. Malen `configureAgreementTemplate()` l. 159–169 har ingen grant på `feed`.
- CellProtocol `Sources/CellBase/Cells/GeneralCell/GeneralCell.swift`: `flow(requester:)` l. 1192 krever `r---` på `feed` (bare eier i dag); feeden er én felles `PassthroughSubject` (l. 309); `pushFlowElement` l. 2392 krever skriverett for den som utløser; `makeCellOwnedFlowEmitterForRuntimeBinding` l. 2406 er celle-eid emitter.
- Presedens: `Sources/App/Cells/Agent/AgentConversationInboxCell.swift` l. 290 (`override func validateCellSpecificAccess`), CellProtocol `Sources/CellBase/Cells/Chat/ChatCell.swift` l. 517 (`override func flow(requester:)` som filtrerer), `Sources/App/Cells/Agent/AgentTrustPackageCell.swift` (bruk av celle-eid emitter).
- Tester: `Tests/AppTests/AssistantCorrespondenceCellTests.swift` (abonnerer og sender som eier i dag, l. 66, 107, 1398–1405).

## Gjør
1. `validateCellSpecificAccess`: gi `r---` på keypath `feed` til en identitet som har en aktiv, godkjent relasjon/grant i cellen (identityUUID + nøkkelfingeravtrykk slik cellen allerede binder principaler). Ingen andre keypaths endres.
2. `override func flow(requester:)`: returner en publisher som bare slipper gjennom FlowElements der `message.recipientID == requesterens principalID` og operasjonen er `message.send` eller `message.ack`. Eieren beholder dagens ufiltrerte feed.
3. Bytt `pushFlowElement(flow, requester:)` i `emitEvent` til den celle-eide emitteren, slik at hendelsen sendes uavhengig av avsenderens skriverett.
4. Behold at `content` aldri er med. Ikke endre HTTP-rutene.
5. Tester i `Tests/AppTests/AssistantCorrespondenceCellTests.swift` for (1)–(5) over, med navn som sier hva de sjekker. Ikke fjern eller svekk eksisterende tester.
6. Dokumentasjon i samme endring: kort avsnitt i den dokumentasjonen som beskriver correspondence-cellen under `Documentation/` (finn filen med `grep -rl AssistantCorrespondence Documentation`), med «Last verified against code: 2026-09-12».

## Ikke-forhandlingsbart
Ingen sentral profilering; ingen hendelse med meldingsinnhold; ingen ny polling; ingen endring av andre cellers autorisasjon; `Swift.DecodingError` når du mener standardbibliotekets; sammenlign aldri hele `ValueType.object`-verdier i tester (kanonisk JSON eller felt for felt).

## Rapport (obligatorisk)
Skriv `CORR_VARSEL_S1_RAPPORT.md` i worktreets rot (ikke legg den til i git): hva som er skrevet (fil:linje), hva som ikke ble gjort og hvorfor, hvilke tester som finnes, og linjen «Status: skrevet, ikke verifisert». Hvis noe i «Dagens tilstand» viste seg feil, si det først.
