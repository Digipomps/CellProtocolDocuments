# Kontrakt — ingen endring i runde 2

Runde 2 endrer ingen cellekontrakt og ingen felt i svaret.

- Svaret følger fortsatt skjemaet `haven.palazzo.communale.guest-concierge.v1`
  (`PalazzoScaffold/Sources/App/Controllers/PalazzoCommunaleFacade.swift`, `schema`, og
  `PalazzoScaffold/Sources/App/Controllers/PalazzoCommunaleProjection.swift`, `envelope`).
- `route` har de samme to verdiene: `native` og `model`.
- Kunnskapscellens endepunkter og autorisasjon røres ikke. De negative
  autorisasjonstestene kjøres som del av hele testmengden.

Derfor er `test.cell.contract-fixtures`, `test.cell.auth-negative` og `test.cell.stub-scan`
merket «ikke relevant» i `FORMAALSSPEC.md` §5.
