# Sikkerhetsrevisjon 2026-11-25 — entitetsutvidelse og egne agenter

Rapporten ligger som dokument: https://claude.ai/artifact/DktCEAQ49hkTeiChwZej4S

Kort:

- Lukket i CellProtocol #114 (`cbfb881`): R1 agent kunne nå EntityAnchor og skrive rå lenkepost; R2 kjør/del-biter i lenke; R3 ingen øvre levetid; R4 bare første lenke vurdert; R5 ingen størrelsesgrenser.
- Åpne i eksisterende kode, venter på Kjetils valg: E1 eierløs Python-celle åpen (PyCellProtocol `general_cell.py:409`, `cells/chat.py:203`); E2 rå skriving til `identityLinks.records.*` gir hel lenke uten passkey (`EntityAnchorCell.swift`, brukt av `FlowPlacementHomeVenue.swift:115`); E3 fullføring av lenke binder ikke utsteder til eieren; E4 avtalemalen til EntityAnchor gir `rw--` på `identityLinks` og `proofs`.
- Ikke kjørt: full `swift test` på macOS, staging, Binding.
