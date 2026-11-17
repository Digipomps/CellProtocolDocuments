## Baseline-relative acceptance

When the owner requests comparison against an unchanged baseline, known red
baseline tests do not stop implementation. Run and retain the complete baseline
first, including exact revisions, dependency pins, command, exit code, failing
test names and terminal bundle summaries. After the change, compare failing
names and require every bundle to finish; report new failures separately. Do not
turn a build failure, aborted suite or a filtered run into a full-regression pass.
Keep additional baseline failures visible even when the owner only named three.

Verified in the third correspondence attachment attempt (2026-09-30): CP
81601a6 had the three documented AppleIdentityVaultKeyStorage failures; unmodified
HavenAgentD ea558ba with CP pin 5609a9a also had
`decodedDefaultAgentCellsInstallBindingsOnceBeforeImmediateStateReads` /
`ownerProofUnavailable`. Report a dependency-pin change separately; disappearance
of that failure with a newer CP does not prove the attachment change fixed it.
Evidence: `CellProtocolDocuments/Deliverables/VEDLEGG_IMPL_3_2026-09-30.md`.

