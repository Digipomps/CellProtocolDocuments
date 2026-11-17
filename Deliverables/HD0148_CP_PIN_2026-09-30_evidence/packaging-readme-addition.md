
## HD-0148: correspondence dependency blocker (2026-09-30)

Last verified against source: 2026-09-30. The pinned CellProtocol
`4107d27a691803897f7aca311573c194d89d1708` lacks the correspondence envelope
and agreement APIs used by this client. The earliest revision on CellProtocol
`origin/main` containing all seven missing public types is
`b5b7282b495e96a7899a189087592581426f4bfb`; its parent lacks them. The earlier
side-branch implementation `a00e3a01a31123bb846e04301876c7bc00ad9bf6` is not
an ancestor of `origin/main`.

A CellProtocol-only pin change cannot resolve the current package graph:
`b5b7282` requires `swift-crypto` from `4.5.2`, while the pinned Sprout
`473d6998bf5417c6355de053fe806ebdf91383e6` requires it from `3.15.1` (below
`4.0.0`). The lockfile has `3.15.1`. Resolve this compatibility decision before
retrying the pilot build; do not silently update Sprout or the crypto pin.
The packaging script itself is unchanged. Evidence and build results:
`CellProtocolDocuments/Deliverables/HD0148_CP_PIN_2026-09-30.md` (HAVEN-root
relative). This records a blocker, not a completed dependency upgrade.
