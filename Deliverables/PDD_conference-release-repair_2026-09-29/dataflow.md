# Dataflow — current and required

Last verified against source and live UI: 2026-09-29.

1. Authenticated staging owner -> Developer Workbench -> owner-scoped ProjectPortfolio and WorkItem via existing Meddle actions. ConferenceScaffold project and four tasks were created and survived page reload. Their internal IDs and structured project links have not yet been read back. HD-0143–HD-0146 are deploy queue IDs, not WorkItem IDs.
2. Authorized local agent -> isolated CellScaffold Git worktree -> source patch and tests -> bounded local build gate. This flow currently stops before compilation for insufficient capacity.
3. After local tests and CI: immutable image with exact commit/pins/digest -> external deploy controller and scoped host claim -> staging -> functional web/native/admin checks -> restart/rollback -> production receipt -> WorkItem evidence. Not executed.
4. Developer Workbench -> existing authenticated admin transport -> TLS proxy -> dedicated AdminScaffold -> cell-level requester/role checks -> observable admin state. Signed upgrade succeeds; application-level reads are still unverified. Admin Workbench is not granted Docker/shell authority.
5. Native HAVEN -> explicit staging catalog -> WSS route -> admitted CellProtocol bridge -> conference cells. Installed app fails ATS; main contains a TLS fix, but installation and safe server admission remain outstanding.
6. Required isolated ConferenceScaffold: own process, storage and identities; explicit conference/organizer context; package exports and scoped runtime registry. Existing EventCells extraction remains partial and is not an implemented standalone service.

Secrets stay in the existing credential store. Probe artifacts retain only booleans and HTTP status. No participant data, identity vaults or runtime databases are copied into the new repository.
