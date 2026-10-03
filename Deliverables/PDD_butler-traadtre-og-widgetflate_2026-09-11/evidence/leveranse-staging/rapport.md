Maal: `staging` paa https://staging.haven.digipomps.org, image `ghcr.io/digipomps/cellscaffold-web:sha-77a922bc301a0ea7586a6b3677a87c2b1e0f73f7`.

Foer deploy svarte https://staging.haven.digipomps.org/health/build: `{"cellprotocol_revision":"533b42d5dc25cf1453cbe5ad08f523d47d5d32e9","dimymicropayments_revision":"cd44d59f584cccf618ff5a33d9a7c5d2c082e6a0","environment":"staging","package_resolved_source":"\/app\/BuildMetadata\/Package.resolved","build_timestamp":"2026-09-18T12:21:55Z","status":"ok","dimymint_revi`

`sudo -n haven-ghcr-prefetch 77a922bc301a0ea7586a6b3677a87c2b1e0f73f7` → exit 0.

```text
77a9af8c900a: Pulling fs layer
44136fa355b3: Already exists
4f4fb700ef54: Already exists
e45cc2189107: Download complete
77a9af8c900a: Download complete
a498f3668772: Download complete
d0f748ddc3d8: Download complete
f5e02259e8aa: Download complete
073d99072504: Download complete
bc1cc0ddb153: Download complete
073d99072504: Pull complete
bc1cc0ddb153: Pull complete
4f4fb700ef54: Pull complete
a498f3668772: Pull complete
77a9af8c900a: Pull complete
f5e02259e8aa: Pull complete
Digest: sha256:6999ea6203e77e9e1d91943bf9cb6c10bf241ae517a66a7ddce3b3c8b1cadefe
Status: Downloaded newer image for ghcr.io/digipomps/cellscaffold-web:sha-77a922bc301a0ea7586a6b3677a87c2b1e0f73f7
ghcr.io/digipomps/cellscaffold-web:sha-77a922bc301a0ea7586a6b3677a87c2b1e0f73f7
GHCR_PREFETCH_OK environment=staging commit=77a922bc301a0ea7586a6b3677a87c2b1e0f73f7 source=ghcr.io/digipomps/cellscaffold-web:sha-77a922bc301a0ea7586a6b3677a87c2b1e0f73f7 destination=cellscaffold-staging-local:sha-77a922bc301a0ea7586a6b3677a87c2b1e0f73f7 image_id=sha256:6999ea6203e77e9e1d91943bf9cb6c10bf241ae517a66a7ddce3b3c8b1cadefe
```

`sudo -n haven-deploy-doctor staging` → exit 0.

```text
   manifest     mot kjoerende container                                                    OK       samme revisjon
   manifest     miljoenavn                                                                 OK       VAPOR_ENV=staging
   eier         kontekst                                                                   OK       Scaffold
   kontinuitet  modus                                                                      OK       continuation mot installert forgjenger
   konfig       containernavn stemmer                                                      OK       cellscaffold-app-1
   juks         CELL_SCAFFOLD_STAGING_MANIFEST_BYPASS                                      OK       ikke satt
   bevis        katalog                                                                    OK       /mnt/disk1/app/haven-staging-evidence/deploy (0o700 0:0)
   laas         katalog                                                                    OK       /run/lock/haven (0o711 0:0)
   som uid 995  vault lesbar                                                               OK       /mnt/disk1/app/CellsContainer.staging-f76de5a/IdentityVaults
 ! som uid 995  vault-masternoekkel lesbar                                                 ADVARSEL /etc/haven/cellscaffold-runtime-secrets-f76de5a/cell-vault-master-key - 995 naar ikke fram; seremonien kopierer den inn selv
   seremoni     arbeidskatalog kan exec                                                    OK       /var/lib/haven-cellscaffold-provision
   seremoni     writer-forutsetninger                                                      OK       katalog- og filkontrollene passerer som uid 995
   verktoey     unshare                                                                    OK       /usr/bin/unshare
   verktoey     setpriv                                                                    OK       /usr/bin/setpriv
   verktoey     jq                                                                         OK       /usr/bin/jq
   verktoey     curl                                                                       OK       /usr/bin/curl
   verktoey     flock                                                                      OK       /usr/bin/flock
   helse        svarer                                                                     OK       http://127.0.0.1:8081 serverer e3ae9fc0526e3582128a0ae88ab2d93d5bd5f2d8

0 feil, 3 advarsler — alle referanser peker riktig.
```

`sudo -n haven-deploy staging 77a922bc301a0ea7586a6b3677a87c2b1e0f73f7 --preflight` → exit 0.

```text
2026-09-22T16:02:49Z PREFLIGHT miljoe=staging commit=77a922bc301a0ea7586a6b3677a87c2b1e0f73f7 txn=20260922T160249Z-staging-77a922bc
2026-09-22T16:02:55Z PREFLIGHT_GREEN prev=e3ae9fc0526e3582128a0ae88ab2d93d5bd5f2d8 image=sha256:6999ea6203e77e9e1d91943bf9cb6c10bf241ae517a66a7ddce3b3c8b1cadefe
2026-09-22T16:02:55Z   celler=/mnt/disk1/app/CellsContainer.staging-f76de5a
2026-09-22T16:02:55Z   database=<ingen>
2026-09-22T16:02:55Z   vault=/mnt/disk1/app/CellsContainer.staging-f76de5a/IdentityVaults
2026-09-22T16:02:55Z   vault-noekkel=/etc/haven/cellscaffold-runtime-secrets-f76de5a/cell-vault-master-key
2026-09-22T16:02:55Z   manifest=/etc/haven/cellscaffold-runtime-identity-manifest-f76de5a/runtime-identity-manifest.v2.json
2026-09-22T16:02:55Z PREFLIGHT_ONLY — ingenting endret
```

## Deploy-enheten `haven-deploy@staging-77a922bc301a0ea7586a6b3677a87c2b1e0f73f7`

Slutt-tilstand: `inactive`. Siste linjer fra journalen:

```text
Sep 22 16:03:45 ubuntu-16gb-hel1-1 haven-deploy[3103625]: 2026-09-22T16:03:45Z READY_OK (restart) etter 20s
Sep 22 16:03:45 ubuntu-16gb-hel1-1 haven-deploy[3103625]: 2026-09-22T16:03:45Z fingerprint_second: cells_count=1305 ScaffoldOrchestrator/NamedEmitters.json=2330c28a99814b6541f36128b3926729b1cbace73ceeda0f1fb70fcc07c57ea0 ScaffoldOrchestrator/IdentityNamedEmitters.json=2bb62353ce2fd4ced92bbbd55efae2720f0d4aa69de36e03bf23047d40fbc119 vault=89be71a68c414dd5f2e54cd7425aa2209c4976e323928d25e2760a12793ab362
Sep 22 16:03:45 ubuntu-16gb-hel1-1 haven-deploy[3103625]: {
Sep 22 16:03:45 ubuntu-16gb-hel1-1 haven-deploy[3103625]:   "schema": "haven.cellscaffold.production-deploy.v1",
Sep 22 16:03:45 ubuntu-16gb-hel1-1 haven-deploy[3103625]:   "status": "committed_verified",
Sep 22 16:03:45 ubuntu-16gb-hel1-1 haven-deploy[3103625]:   "environment": "staging",
Sep 22 16:03:45 ubuntu-16gb-hel1-1 haven-deploy[3103625]:   "transactionID": "20260922T160255Z-staging-77a922bc",
Sep 22 16:03:45 ubuntu-16gb-hel1-1 haven-deploy[3103625]:   "commit": "77a922bc301a0ea7586a6b3677a87c2b1e0f73f7",
Sep 22 16:03:45 ubuntu-16gb-hel1-1 haven-deploy[3103625]:   "previousCommit": "e3ae9fc0526e3582128a0ae88ab2d93d5bd5f2d8",
Sep 22 16:03:45 ubuntu-16gb-hel1-1 haven-deploy[3103625]:   "imageID": "sha256:6999ea6203e77e9e1d91943bf9cb6c10bf241ae517a66a7ddce3b3c8b1cadefe",
Sep 22 16:03:45 ubuntu-16gb-hel1-1 haven-deploy[3103625]:   "rollbackContainer": "cellscaffold-app-1-rollback-20260922T160255Z-staging-77a922bc",
Sep 22 16:03:45 ubuntu-16gb-hel1-1 haven-deploy[3103625]:   "dataRoot": "/mnt/disk1/app/CellsContainer.staging-f76de5a",
Sep 22 16:03:45 ubuntu-16gb-hel1-1 haven-deploy[3103625]:   "manifestBackup": "/mnt/disk1/app/haven-staging-evidence/manifest-provision/20260922T160309Z-77a922bc/manifest.before.json",
Sep 22 16:03:45 ubuntu-16gb-hel1-1 haven-deploy[3103625]:   "ceremony": {
Sep 22 16:03:45 ubuntu-16gb-hel1-1 haven-deploy[3103625]:     "vaultFilesAdded": [],
Sep 22 16:03:45 ubuntu-16gb-hel1-1 haven-deploy[3103625]:     "bindingsGained": []
Sep 22 16:03:45 ubuntu-16gb-hel1-1 haven-deploy[3103625]:   },
Sep 22 16:03:45 ubuntu-16gb-hel1-1 haven-deploy[3103625]:   "readinessGate": "http200_status_ready",
Sep 22 16:03:45 ubuntu-16gb-hel1-1 haven-deploy[3103625]:   "targetedFingerprint": {
Sep 22 16:03:45 ubuntu-16gb-hel1-1 haven-deploy[3103625]:     "before": "cells_count=1305 ScaffoldOrchestrator/NamedEmitters.json=2330c28a99814b6541f36128b3926729b1cbace73ceeda0f1fb70fcc07c57ea0 ScaffoldOrchestrator/IdentityNamedEmitters.json=2bb62353ce2fd4ced92bbbd55efae2720f0d4aa69de36e03bf23047d40fbc119 vault=89be71a68c414dd5f2e54cd7425aa2209c4976e323928d25e2760a12793ab362 ",
Sep 22 16:03:45 ubuntu-16gb-hel1-1 haven-deploy[3103625]:     "firstStart": "cells_count=1305 ScaffoldOrchestrator/NamedEmitters.json=2330c28a99814b6541f36128b3926729b1cbace73ceeda0f1fb70fcc07c57ea0 ScaffoldOrchestrator/IdentityNamedEmitters.json=2bb62353ce2fd4ced92bbbd55efae2720f0d4aa69de36e03bf23047d40fbc119 vault=89be71a68c414dd5f2e54cd7425aa2209c4976e323928d25e2760a12793ab362 ",
Sep 22 16:03:45 ubuntu-16gb-hel1-1 haven-deploy[3103625]:     "afterRestart": "cells_count=1305 ScaffoldOrchestrator/NamedEmitters.json=2330c28a99814b6541f36128b3926729b1cbace73ceeda0f1fb70fcc07c57ea0 ScaffoldOrchestrator/IdentityNamedEmitters.json=2bb62353ce2fd4ced92bbbd55efae2720f0d4aa69de36e03bf23047d40fbc119 vault=89be71a68c414dd5f2e54cd7425aa2209c4976e323928d25e2760a12793ab362 "
Sep 22 16:03:45 ubuntu-16gb-hel1-1 haven-deploy[3103625]:   },
Sep 22 16:03:45 ubuntu-16gb-hel1-1 haven-deploy[3103625]:   "completedAt": "2026-09-22T16:03:45Z"
Sep 22 16:03:45 ubuntu-16gb-hel1-1 haven-deploy[3103625]: }
Sep 22 16:03:45 ubuntu-16gb-hel1-1 haven-deploy[3103625]: 2026-09-22T16:03:45Z COMMITTED_VERIFIED
Sep 22 16:03:45 ubuntu-16gb-hel1-1 haven-deploy[3103625]: 2026-09-22T16:03:45Z FERDIG — bevis i /mnt/disk1/app/haven-staging-evidence/deploy/20260922T160255Z-staging-77a922bc
Sep 22 16:03:45 ubuntu-16gb-hel1-1 systemd[1]: haven-deploy@staging-77a922bc301a0ea7586a6b3677a87c2b1e0f73f7.service: Deactivated successfully.
Sep 22 16:03:45 ubuntu-16gb-hel1-1 systemd[1]: Finished haven-deploy@staging-77a922bc301a0ea7586a6b3677a87c2b1e0f73f7.service - HAVEN CellScaffold deploy (staging-77a922bc301a0ea7586a6b3677a87c2b1e0f73f7).
Sep 22 16:03:45 ubuntu-16gb-hel1-1 systemd[1]: haven-deploy@staging-77a922bc301a0ea7586a6b3677a87c2b1e0f73f7.service: Consumed 5.737s CPU time.
```

`sudo -n haven-deploy staging --verify` → exit 2.

```text
FEIL: commit maa vaere 40-hex, eller 'current' sammen med --env-only
```

MERK: `--verify` ga ikke exit 0.
## Etter deploy

`https://staging.haven.digipomps.org/health/build`: `{"package_resolved_source":"\/app\/BuildMetadata\/Package.resolved","app_revision":"77a922bc301a0ea7586a6b3677a87c2b1e0f73f7","cellprotocol_revision":"473357cf4efee831cb3b55ae87bc921d4bb63c10","dimymicropayments_revision":"836ba8e6d71663d78836e2ec67a1e6f38bd8655b","dimymint_revision":"af41630bbc01cece2a26f3004fdf6f83724ca77e","status":"ok","build_timestamp":"2026-09-22T11:21:08Z","environment":"st`

Staging svarer med revisjonen vi deployet (`77a922bc301a0ea7586a6b3677a87c2b1e0f73f7`).

Koordinering frigitt: hd: invalid task id 'deploy-skjelettrunden-20260922' (expected HD-nnnn)

Neste steg: prod bruker samme digest — men prod skal ikke roeres foer Kjetil sier fra.
