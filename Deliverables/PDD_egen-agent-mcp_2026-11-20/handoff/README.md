# Handoff — egen agent mot HAVEN

Kjøringer på Macen går med Remote Control i et arbeidstre under `/Volumes/Backup/build/egen-agent-<dato>/` (aldri intern disk), med `CELLPROTOCOL_PUBLISHED_API=1` for CellScaffold. Ingen git gjennom den delte mappen.

Kommandoer per repo (WP0 fyller inn tallene):
- CellProtocol: `swift build && swift test`
- PyCellProtocol: `python3 -m pytest`
- GoCellProtocol: `go test ./...`
- CellScaffold: CI på PR; full kjøring på Macen før en PR tas ut av utkast
- HavenDocsMCP: `python3 -m unittest discover Tools/HavenDocsMCP/tests`

Claude fletter, tagger og slipper aldri. Staging går via FORESPOERSEL til HAVEN-Deploy.
