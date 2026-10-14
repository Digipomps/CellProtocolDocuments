STATUS: LEVERT — produksjon kjoerer sha-77a922bc301a0ea7586a6b3677a87c2b1e0f73f7, verifisert mot /health/build

# Leveranse steg 5 — produksjon

Skrevet av `HAVEN-Deploy/_handoff/WP-R/wp-lev-prod.sh` 2026-09-22T21:24:23Z. Bevis: `evidence/leveranse-prod/`.

Maal: `production` paa https://haven.digipomps.org, image `ghcr.io/digipomps/cellscaffold-web:sha-77a922bc301a0ea7586a6b3677a87c2b1e0f73f7` — samme digest som staging.

Forutsetning (R-D24): staging kjoerer `77a922bc301a0ea7586a6b3677a87c2b1e0f73f7` og svarer med den. Kontrollert foer vi roerte noe.

Foer deploy svarte https://haven.digipomps.org/health/build: `{"dimymicropayments_revision":"cd44d59f584cccf618ff5a33d9a7c5d2c082e6a0","dimymint_revision":"ffdb0da85fc45be16926bfa5d335b247205f1b79","app_revision":"e3ae9fc0526e3582128a0ae88ab2d93d5bd5f2d8","environment":"production","build_timestamp":"2026-09-18T12:21:55Z","cellprotocol_revision":"533b42d5dc25c`

`sudo -n haven-ghcr-prefetch-production 77a922bc301a0ea7586a6b3677a87c2b1e0f73f7` → exit 0.

```text
sha-77a922bc301a0ea7586a6b3677a87c2b1e0f73f7: Pulling from digipomps/cellscaffold-web
Digest: sha256:6999ea6203e77e9e1d91943bf9cb6c10bf241ae517a66a7ddce3b3c8b1cadefe
Status: Image is up to date for ghcr.io/digipomps/cellscaffold-web:sha-77a922bc301a0ea7586a6b3677a87c2b1e0f73f7
ghcr.io/digipomps/cellscaffold-web:sha-77a922bc301a0ea7586a6b3677a87c2b1e0f73f7
GHCR_PREFETCH_OK environment=production commit=77a922bc301a0ea7586a6b3677a87c2b1e0f73f7 source=ghcr.io/digipomps/cellscaffold-web:sha-77a922bc301a0ea7586a6b3677a87c2b1e0f73f7 destination=cellscaffold-production-candidate:sha-77a922bc301a0ea7586a6b3677a87c2b1e0f73f7 image_id=sha256:6999ea6203e77e9e1d91943bf9cb6c10bf241ae517a66a7ddce3b3c8b1cadefe
```

`sudo -n haven-deploy-doctor production` → exit 0.

```text
   manifest     mot kjoerende container                                                    OK       samme revisjon
   manifest     miljoenavn                                                                 OK       VAPOR_ENV=production
   eier         kontekst                                                                   OK       HavenProduction
   kontinuitet  modus                                                                      OK       continuation mot installert forgjenger
   konfig       containernavn stemmer                                                      OK       cellscaffold-production-app-1
   juks         CELL_SCAFFOLD_STAGING_MANIFEST_BYPASS                                      OK       ikke satt
   bevis        katalog                                                                    OK       /mnt/HC_Volume_104775511/haven-production-evidence/deploy (0o700 0:0)
   laas         katalog                                                                    OK       /run/lock/haven (0o711 0:0)
   som uid 995  vault lesbar                                                               OK       /mnt/HC_Volume_104775511/haven-production/IdentityVaults
 ! som uid 995  vault-masternoekkel lesbar                                                 ADVARSEL /etc/haven/cellscaffold-production-runtime-secrets/cell-vault-master-key - 995 naar ikke fram; seremonien kopierer den inn selv
   seremoni     arbeidskatalog kan exec                                                    OK       /var/lib/haven-cellscaffold-provision
   seremoni     writer-forutsetninger                                                      OK       katalog- og filkontrollene passerer som uid 995
   verktoey     unshare                                                                    OK       /usr/bin/unshare
   verktoey     setpriv                                                                    OK       /usr/bin/setpriv
   verktoey     jq                                                                         OK       /usr/bin/jq
   verktoey     curl                                                                       OK       /usr/bin/curl
   verktoey     flock                                                                      OK       /usr/bin/flock
   helse        svarer                                                                     OK       http://127.0.0.1:8084 serverer e3ae9fc0526e3582128a0ae88ab2d93d5bd5f2d8

0 feil, 1 advarsler — alle referanser peker riktig.
```

`sudo -n haven-deploy production 77a922bc301a0ea7586a6b3677a87c2b1e0f73f7 --preflight` → exit 0.

```text
2026-09-22T21:23:39Z PREFLIGHT miljoe=production commit=77a922bc301a0ea7586a6b3677a87c2b1e0f73f7 txn=20260922T212339Z-production-77a922bc
2026-09-22T21:23:40Z PREFLIGHT_GREEN prev=e3ae9fc0526e3582128a0ae88ab2d93d5bd5f2d8 image=sha256:6999ea6203e77e9e1d91943bf9cb6c10bf241ae517a66a7ddce3b3c8b1cadefe
2026-09-22T21:23:40Z   celler=/mnt/HC_Volume_104775511/haven-production/CellsContainer
2026-09-22T21:23:40Z   database=/mnt/HC_Volume_104775511/haven-production/Database
2026-09-22T21:23:40Z   vault=/mnt/HC_Volume_104775511/haven-production/IdentityVaults
2026-09-22T21:23:40Z   vault-noekkel=/etc/haven/cellscaffold-production-runtime-secrets/cell-vault-master-key
2026-09-22T21:23:40Z   manifest=/etc/haven/cellscaffold-production-runtime-identity-manifest/runtime-identity-manifest.v2.json
2026-09-22T21:23:40Z PREFLIGHT_ONLY — ingenting endret
```

## Deploy-enheten `haven-deploy@production-77a922bc301a0ea7586a6b3677a87c2b1e0f73f7`

Slutt-tilstand: `inactive`. Siste linjer fra journalen:

```text
Sep 22 21:24:07 ubuntu-16gb-hel1-1 haven-deploy[3515900]: 2026-09-22T21:24:07Z READY_OK (restart) etter 10s
Sep 22 21:24:07 ubuntu-16gb-hel1-1 haven-deploy[3515900]: 2026-09-22T21:24:07Z fingerprint_second: cells_count=631 ScaffoldOrchestrator/NamedEmitters.json=52b48a78ad3cd9bfdc2f2abddbe9f80706b878f91d735ffe6857b805fa08f682 ScaffoldOrchestrator/IdentityNamedEmitters.json=fb9c62d18c967f44febd8a33564570c3a89620dea305a2d0880e42ce19a6e086 db_size=335872 vault=d89bc6dbc8c86e66e58e8ebe8b64acb1e96af3f790fe8e8a8a7a6b72702e2691
Sep 22 21:24:07 ubuntu-16gb-hel1-1 haven-deploy[3515900]: {
Sep 22 21:24:07 ubuntu-16gb-hel1-1 haven-deploy[3515900]:   "schema": "haven.cellscaffold.production-deploy.v1",
Sep 22 21:24:07 ubuntu-16gb-hel1-1 haven-deploy[3515900]:   "status": "committed_verified",
Sep 22 21:24:07 ubuntu-16gb-hel1-1 haven-deploy[3515900]:   "environment": "production",
Sep 22 21:24:07 ubuntu-16gb-hel1-1 haven-deploy[3515900]:   "transactionID": "20260922T212341Z-production-77a922bc",
Sep 22 21:24:07 ubuntu-16gb-hel1-1 haven-deploy[3515900]:   "commit": "77a922bc301a0ea7586a6b3677a87c2b1e0f73f7",
Sep 22 21:24:07 ubuntu-16gb-hel1-1 haven-deploy[3515900]:   "previousCommit": "e3ae9fc0526e3582128a0ae88ab2d93d5bd5f2d8",
Sep 22 21:24:07 ubuntu-16gb-hel1-1 haven-deploy[3515900]:   "imageID": "sha256:6999ea6203e77e9e1d91943bf9cb6c10bf241ae517a66a7ddce3b3c8b1cadefe",
Sep 22 21:24:07 ubuntu-16gb-hel1-1 haven-deploy[3515900]:   "rollbackContainer": "cellscaffold-production-app-1-rollback-20260922T212341Z-production-77a922bc",
Sep 22 21:24:07 ubuntu-16gb-hel1-1 haven-deploy[3515900]:   "dataRoot": "/mnt/HC_Volume_104775511/haven-production/CellsContainer",
Sep 22 21:24:07 ubuntu-16gb-hel1-1 haven-deploy[3515900]:   "manifestBackup": "/mnt/HC_Volume_104775511/haven-production-evidence/manifest-provision/20260922T212354Z-77a922bc/manifest.before.json",
Sep 22 21:24:07 ubuntu-16gb-hel1-1 haven-deploy[3515900]:   "ceremony": {
Sep 22 21:24:07 ubuntu-16gb-hel1-1 haven-deploy[3515900]:     "vaultFilesAdded": [],
Sep 22 21:24:07 ubuntu-16gb-hel1-1 haven-deploy[3515900]:     "bindingsGained": []
Sep 22 21:24:07 ubuntu-16gb-hel1-1 haven-deploy[3515900]:   },
Sep 22 21:24:07 ubuntu-16gb-hel1-1 haven-deploy[3515900]:   "readinessGate": "http200_status_ready",
Sep 22 21:24:07 ubuntu-16gb-hel1-1 haven-deploy[3515900]:   "targetedFingerprint": {
Sep 22 21:24:07 ubuntu-16gb-hel1-1 haven-deploy[3515900]:     "before": "cells_count=631 ScaffoldOrchestrator/NamedEmitters.json=52b48a78ad3cd9bfdc2f2abddbe9f80706b878f91d735ffe6857b805fa08f682 ScaffoldOrchestrator/IdentityNamedEmitters.json=fb9c62d18c967f44febd8a33564570c3a89620dea305a2d0880e42ce19a6e086 db_size=335872 vault=d89bc6dbc8c86e66e58e8ebe8b64acb1e96af3f790fe8e8a8a7a6b72702e2691 ",
Sep 22 21:24:07 ubuntu-16gb-hel1-1 haven-deploy[3515900]:     "firstStart": "cells_count=631 ScaffoldOrchestrator/NamedEmitters.json=52b48a78ad3cd9bfdc2f2abddbe9f80706b878f91d735ffe6857b805fa08f682 ScaffoldOrchestrator/IdentityNamedEmitters.json=fb9c62d18c967f44febd8a33564570c3a89620dea305a2d0880e42ce19a6e086 db_size=335872 vault=d89bc6dbc8c86e66e58e8ebe8b64acb1e96af3f790fe8e8a8a7a6b72702e2691 ",
Sep 22 21:24:07 ubuntu-16gb-hel1-1 haven-deploy[3515900]:     "afterRestart": "cells_count=631 ScaffoldOrchestrator/NamedEmitters.json=52b48a78ad3cd9bfdc2f2abddbe9f80706b878f91d735ffe6857b805fa08f682 ScaffoldOrchestrator/IdentityNamedEmitters.json=fb9c62d18c967f44febd8a33564570c3a89620dea305a2d0880e42ce19a6e086 db_size=335872 vault=d89bc6dbc8c86e66e58e8ebe8b64acb1e96af3f790fe8e8a8a7a6b72702e2691 "
Sep 22 21:24:07 ubuntu-16gb-hel1-1 haven-deploy[3515900]:   },
Sep 22 21:24:07 ubuntu-16gb-hel1-1 haven-deploy[3515900]:   "completedAt": "2026-09-22T21:24:07Z"
Sep 22 21:24:07 ubuntu-16gb-hel1-1 haven-deploy[3515900]: }
Sep 22 21:24:07 ubuntu-16gb-hel1-1 haven-deploy[3515900]: 2026-09-22T21:24:07Z COMMITTED_VERIFIED
Sep 22 21:24:07 ubuntu-16gb-hel1-1 haven-deploy[3515900]: 2026-09-22T21:24:07Z FERDIG — bevis i /mnt/HC_Volume_104775511/haven-production-evidence/deploy/20260922T212341Z-production-77a922bc
Sep 22 21:24:07 ubuntu-16gb-hel1-1 systemd[1]: haven-deploy@production-77a922bc301a0ea7586a6b3677a87c2b1e0f73f7.service: Deactivated successfully.
Sep 22 21:24:07 ubuntu-16gb-hel1-1 systemd[1]: Finished haven-deploy@production-77a922bc301a0ea7586a6b3677a87c2b1e0f73f7.service - HAVEN CellScaffold deploy (production-77a922bc301a0ea7586a6b3677a87c2b1e0f73f7).
Sep 22 21:24:07 ubuntu-16gb-hel1-1 systemd[1]: haven-deploy@production-77a922bc301a0ea7586a6b3677a87c2b1e0f73f7.service: Consumed 4.093s CPU time.
```

`sudo -n haven-deploy production 77a922bc301a0ea7586a6b3677a87c2b1e0f73f7 --verify` → exit 1.

```text
2026-09-22T21:24:23Z PREFLIGHT miljoe=production commit=77a922bc301a0ea7586a6b3677a87c2b1e0f73f7 txn=20260922T212423Z-production-77a922bc
2026-09-22T21:24:23Z FEIL: production kjoerer allerede 77a922bc301a0ea7586a6b3677a87c2b1e0f73f7 med manifest for samme revisjon
```

MERK: `--verify` ga ikke exit 0.
## Etter deploy

`https://haven.digipomps.org/health/build`: `{"build_timestamp":"2026-09-22T11:21:08Z","dimymicropayments_revision":"836ba8e6d71663d78836e2ec67a1e6f38bd8655b","status":"ok","cellprotocol_revision":"473357cf4efee831cb3b55ae87bc921d4bb63c10","dimymint_revision":"af41630bbc01cece2a26f3004fdf6f83724ca77e","environment":"production","package_resolved_source":"\/app\/BuildMetadata\/Package.resolved","app_revision":"77a922bc301a0ea7586a6b3677a87c2b`

Produksjon svarer med revisjonen vi deployet (`77a922bc301a0ea7586a6b3677a87c2b1e0f73f7`).

Koordinering: (no active claims) (hd-krav ble aldri registrert — id-formatet maa vaere HD-nnnn; se DEPLOY-KOORDINERING.md)

Prod og staging kjoerer naa samme digest. Gjenstaaende kjent mangel: mobil-chatten paa 375 px (se PR #251).
