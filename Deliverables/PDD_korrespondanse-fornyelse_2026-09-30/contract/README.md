# Kontrakt: AssistantCorrespondenceCell, fornyelse

Pilotcellen `AssistantCorrespondenceCell` (CellScaffold, `Sources/App/Cells/Agent/`) har ingen kontrakt-JSON i `Book/`. `Book/correspondence_cell_contract_v0.json` beskriver den kommende førsteklasses `CorrespondenceCell` (kapittel 33), ikke pilotcellen. For piloten er det koden og testene i `Tests/AppTests/AssistantCorrespondenceCellTests.swift` som er kontrakten.

## Endringen i kontrakten (commit `415ea3d2`)

Før endringen fantes det ingen vei tilbake. En ny innmelding med utløpt tilgang endte i `credential_issuance_failed`, og fra en annen enhet i `principal_already_enrolled` (FORMAALSSPEC §0).

| Situasjon ved `enroll` med fersk invitasjon | Svar nå | Test |
|---|---|---|
| Tilgangen er utløpt og ikke tilbakekalt; samme enhet, nøkkel og entitet | ny tilgangsforespørsel, `pending_approval`, med `renewsGrantID` | T1 |
| Principalen er tilbakekalt, og tilgangen er utløpt | ingen ny forespørsel | T2 |
| Annen enhet eller nøkkel | `principal_already_enrolled`, som før | T3 |
| Tilgangen er aktiv | eksisterende tilgang og et bevis med tilgangens frist, som før | `testApprovedGrantEnrollmentBehaviorRemainsUnchanged` |

Tilgangsforespørselen (`accessRequestObject`) har fått det valgfrie feltet `renewsGrantID`. Det står bare der når forespørselen fornyer en tilgang. Rutene, feilkodene, `message.send` og `inbox.list` er uendret.
