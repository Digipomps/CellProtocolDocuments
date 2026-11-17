STATUS: LEVERT — kart (leser bare)

# pdd/scaffold-admin-delegering — hvor står den (2026-09-23)

Skrevet av `HAVEN-Deploy/_handoff/WP-R/wp-sad-kart.sh` 2026-09-23T11:38:53Z.

## Git

```text
origin/main: 77a922bc301a0ea7586a6b3677a87c2b1e0f73f7
gren: bcaf1e5e53655f9b98f36a6ef686b7289a27a827  base: e1f3e22f02239e44eacaf12a741d78b4066d0c35
ancestor? nei  (ventet nei ved squash/cherry-pick)

fil | status mot origin/main | siste main-commit som roerte fila
Sources/App/Cells/Admin/ScaffoldAdministratorRegistryCell.swift | identisk | 87256f9a 2026-09-18 Restore Butler workflows and verified admin deployment path (#247)
Sources/App/Cells/Admin/ScaffoldMandate.swift | identisk | 87256f9a 2026-09-18 Restore Butler workflows and verified admin deployment path (#247)
Sources/App/Cells/Admin/ScaffoldMandateCell.swift | ulik (+43/-3) | 87256f9a 2026-09-18 Restore Butler workflows and verified admin deployment path (#247)
Sources/App/Cells/Admin/ScaffoldMandateProofSupport.swift | ulik (+32/-0) | 87256f9a 2026-09-18 Restore Butler workflows and verified admin deployment path (#247)
Sources/App/Cells/Arendalsuka/ArendalsukaConfigurationPublisherCell.swift | ulik (+61/-1) | 87256f9a 2026-09-18 Restore Butler workflows and verified admin deployment path (#247)
Sources/App/Cells/Arendalsuka/ArendalsukaImportAccessCredentialSupport.swift | identisk | 87256f9a 2026-09-18 Restore Butler workflows and verified admin deployment path (#247)
Sources/App/Cells/SimpleProjectManager/ScaffoldOrchestratorCell.swift | identisk | 87256f9a 2026-09-18 Restore Butler workflows and verified admin deployment path (#247)
Sources/App/Support/CanonicalCellRuntimeReadinessStore.swift | identisk | 87256f9a 2026-09-18 Restore Butler workflows and verified admin deployment path (#247)
Sources/App/Support/EntityAnchorProofSupport.swift | identisk | 87256f9a 2026-09-18 Restore Butler workflows and verified admin deployment path (#247)
Sources/App/Support/ScaffoldAdministratorRuntimeSupport.swift | ulik (+25/-1) | 87256f9a 2026-09-18 Restore Butler workflows and verified admin deployment path (#247)
Sources/App/configure.swift | ulik (+73/-7) | 87256f9a 2026-09-18 Restore Butler workflows and verified admin deployment path (#247)
Tests/AppTests/Fixtures/ScaffoldMandate/README.md | identisk | 87256f9a 2026-09-18 Restore Butler workflows and verified admin deployment path (#247)
Tests/AppTests/Fixtures/ScaffoldMandate/mandate-negative.json | identisk | 87256f9a 2026-09-18 Restore Butler workflows and verified admin deployment path (#247)
Tests/AppTests/Fixtures/ScaffoldMandate/mandate-positive.json | identisk | 87256f9a 2026-09-18 Restore Butler workflows and verified admin deployment path (#247)
Tests/AppTests/Fixtures/ScaffoldMandate/threshold-policy.json | identisk | 87256f9a 2026-09-18 Restore Butler workflows and verified admin deployment path (#247)
Tests/AppTests/ScaffoldAdministratorRegistryTests.swift | ulik (+39/-0) | 87256f9a 2026-09-18 Restore Butler workflows and verified admin deployment path (#247)
Tests/AppTests/ScaffoldMandateTests.swift | identisk | 87256f9a 2026-09-18 Restore Butler workflows and verified admin deployment path (#247)
Tests/AppTests/ScaffoldRoleIsNotAuthorityTests.swift | identisk | 87256f9a 2026-09-18 Restore Butler workflows and verified admin deployment path (#247)

commits paa main med grenens emnelinjer:
  «Trekk ut entitetsbevis»: 87256f9a 2026-09-18 
  «Opprett register for scaffold-administrator»: 87256f9a 2026-09-18 
  «Innfør mandat»: 87256f9a 2026-09-18 
  «La målcellen spørre»: 87256f9a 2026-09-18 
  «Vis at rolle ikke gir»: 87256f9a 2026-09-18 
  «Koble de to nye cellene»: 87256f9a 2026-09-18 

provisjoneringsskript paa main:
  md5 125f673cb6c70888641f8abde2200099  linjer      300
  siste commit: 87256f9a 2026-09-18 Restore Butler workflows and verified admin deployment path (#247)
  Sources/App/Support/ScaffoldAdministratorProvisioner.swift: finnes  87256f9a 2026-09-18 Restore Butler workflows and verified admin deployment path 
  Sources/App/Support/ScaffoldAdministratorRuntimeSupport.swift: finnes  87256f9a 2026-09-18 Restore Butler workflows and verified admin deployment path 
```

## Verten

```text
== cellscaffold-app-1
  ready: ready | advarsler: ['arendalsuka_published_read_access_not_provisioned', 'scaffold_administrator_not_provisioned scaffold=scaffold:cellscaffold', 'scaffold_administrator_threshold_below_two scaffold=scaffold:cellscaffold requiredSignatures=1 reason=utviklingsfase, styreleder alene setAt=2026-09-09T00:00:00Z']
  build: 77a922bc301a0ea7586a6b3677a87c2b1e0f73f7
  fido_users-kolonner med id: ['id', 'cell_id', 'identity_id']
  bruker: C8C99783-8522-40DE-A427-03E409090587 | kjetil2 | DF8D4644-15B2-46F4-A708-CEEB323DA3FE
  bruker: C2A12943-7CD8-4A02-B325-A2EA17B4769F | vegar | 8DCE5C5A-35E7-443E-A4A6-EDE781746CA4
== cellscaffold-production-app-1
  ready: ready | advarsler: ['scaffold_administrator_not_provisioned scaffold=scaffold:cellscaffold', 'scaffold_administrator_threshold_below_two scaffold=scaffold:cellscaffold requiredSignatures=1 reason=utviklingsfase, styreleder alene setAt=2026-09-09T00:00:00Z']
  build: 77a922bc301a0ea7586a6b3677a87c2b1e0f73f7
  fido_users-kolonner med id: ['id', 'cell_id', 'identity_id']
  bruker: 87FA1CF0-6E67-451D-BCDD-7CE2BFA52C34 | kjetil2 | E027291A-7FC8-45CF-8FF9-908DBA41593C
  bruker: 836F624A-502C-4375-9BDD-5D44784C1F94 | Vegar | ABA68006-7515-49E8-9160-F4334F948746
== provisjoneringsskript paa verten?
-rwxr-xr-x  1 root root 39922 Sep  1 20:27 haven-manifest-provision
drwxr-x---  3 root ops      4096 Jul 17 12:39 .haven-admin-provision
-rw-r--r--  1 ops  ops      2968 Aug 11 03:36 haven-correspondence-provision-60336f34.bundle
-rw-r--r--  1 ops  ops      2476 Aug 11 03:34 haven-correspondence-provision-8452b4e7.bundle
vert exit 0
```
