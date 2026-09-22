#!/bin/bash
set -euo pipefail
WT="${CELLPROTOCOL_WORKTREE:-$HOME/Build/Digipomps/HAVEN/CellProtocol-pdd-entitetsdata}"
cd "$WT"
if [ -z "$(git status --short --untracked-files=no)" ]; then
  echo "ingenting a committe i $WT"
  git log --oneline -1
  exit 0
fi
git add -A Sources Tests
git status --short
git commit -q -F - <<'MSG'
Genesis seals the entity to its initiator; only local-anchor links open it

purpose://candidate.entitetsdata.genesis-seals-to-initiator
purpose://candidate.entitetsdata.authorization-resolves-entity

WP1: EntityGenesisService (CellBase/Identity/EntityGenesis.swift) builds and
signs a seal plus a same_entity IdentityLinkRecord issued by the initiator to
itself. EntityAnchorCell (Vapor and Apple) exposes identityLinks.genesis, seals
on first owner-proven batchPersist, refuses a second genesis, refuses revoke of
the genesis link, and treats identityLinks.genesis* as immutable for any set.

WP2 hardening on top of the IdentityLinkRegistry that already resolves
same-entity links: sameEntityLink requires entityBinding.mode ==
localEntityAnchor (pairwise/blinded prove membership to others, they do not
open the anchor), and restoreIdentityLinkRegistry drops a genesis record whose
seal does not verify against the key in the record.

Tests: EntityGenesisTests (6), EntityAnchorGenesisTests (9),
IdentityLinkRegistryBindingTests (1). Full CellBaseTests: 1244 passed,
0 failed. Sealing on first batchPersist is implemented but not covered:
the feed intercept needs the flow harness round 2 builds.

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_0166zoWBapoQ3R6iiJrhd2xx
MSG
git log --oneline -2
echo "commit: OK pa $(git branch --show-current). Ikke pushet."
