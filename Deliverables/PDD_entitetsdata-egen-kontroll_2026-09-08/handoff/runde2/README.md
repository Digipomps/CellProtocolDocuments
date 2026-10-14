# handoff/runde2 — entitetsdata WP3–WP5

`runde2.patch` er skrevet mot origin/main 33ad8d7 (etter #47). `runde2.sh` lager worktreet
`~/Build/Digipomps/HAVEN/CellProtocol-pdd-entitetsdata-r2` på branch `pdd/entitetsdata-runde2` fra
origin/main, legger på patchen, bygger, kjører `EntityAnchorAccessBoundaryTests`, runde 1-testene og
hele CellBaseTests, og committer + pusher + åpner utkast-PR bare hvis alt er grønt. Tørrkjøring uten
`--go`. Rører aldri Kjetils utsjekk. Ingen force. Dobbeltklikk `runde2.command` i Finder.

Filer i patchen: `Sources/CellBase/PersistingCells/EntityChangeTrace.swift` (ny),
`Sources/CellVapor/Cells/EntityAnchorCell.swift`, `Sources/CellApple/Cells/EntityAnchorCell.swift`,
`Tests/CellBaseTests/TestSupport/SimulatedEntity.swift` (ny),
`Tests/CellBaseTests/EntityAnchorAccessBoundaryTests.swift` (ny), `EntityAnchorGenesisTests.swift` (kommentar).
