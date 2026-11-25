# Sikkerhetsrevisjon 2026-11-25 — entitetsutvidelse og egne agenter

Rapporten ligger som dokument: https://claude.ai/artifact/DktCEAQ49hkTeiChwZej4S

Kort:

- Lukket i CellProtocol #114 (`cbfb881`): R1 agent kunne nå EntityAnchor og skrive rå lenkepost; R2 kjør/del-biter i lenke; R3 ingen øvre levetid; R4 bare første lenke vurdert; R5 ingen størrelsesgrenser.
- Funn i eksisterende kode, lukket i utkast etter Kjetils valg 25.11: E1 eierløs Python-celle avviser alle (PyCellProtocol #5); E2 rå lenkepost krever eierens egen nøkkel, bare én hel post, og avvises der verten krever fersk passkey, og FlowPlacement bruker signert innmelding (CellProtocol #117, CellScaffold #514); E2b batch og direkte flow-skriving avviser alt under `identityLinks` (CellProtocol #117); E3 godkjenner og utsteder må være eiernøkkelen eller en hel lenke i ankeret (CellProtocol #117); E4 avtalemalen gir ikke `identityLinks` (CellProtocol #117).
- Rester: forventet publikum og opphav hentes fortsatt fra konvolutten (E3); `proofs` står igjen i malen til CellVapor (E4); ingen flate henter passkey-bekreftelsen for hjemmescaffoldet.
- Ikke kjørt: full `swift test` på macOS, CellApple-bygg, App-målet i CellScaffold, staging, Binding.
