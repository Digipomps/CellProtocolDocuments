STATUS: LEVERT — staging og prod kjører sha-60e5a64d1c2a4a9f4e2b3fa53e45ed2d63f6aaba (leveranse 2 + formålsgraf v3)

# Formålsgraf v3 — steg B2: staging og prod

Skrevet av `HAVEN-Deploy/_handoff/BUTLER-MAALING/graf/wp-graf-b2-ut.sh` 2026-09-24T07:40:52Z.

Image: `ghcr.io/digipomps/cellscaffold-web:sha-60e5a64d1c2a4a9f4e2b3fa53e45ed2d63f6aaba`

## staging

`sudo -n haven-ghcr-prefetch 60e5a64d1c2a4a9f4e2b3fa53e45ed2d63f6aaba` → exit 0
`sudo -n haven-deploy-doctor staging` → exit 0
`sudo -n haven-deploy staging 60e5a64d1c2a4a9f4e2b3fa53e45ed2d63f6aaba --preflight` → exit 0
Enhet `haven-deploy@staging-60e5a64d1c2a4a9f4e2b3fa53e45ed2d63f6aaba`: `inactive`
```text
Sep 24 07:39:14 ubuntu-16gb-hel1-1 haven-deploy[2064841]: 2026-09-24T07:39:14Z PREFLIGHT miljoe=staging commit=60e5a64d1c2a4a9f4e2b3fa53e45ed2d63f6aaba txn=20260924T073914Z-staging-60e5a64d
Sep 24 07:39:16 ubuntu-16gb-hel1-1 haven-deploy[2064841]: 2026-09-24T07:39:16Z PREFLIGHT_GREEN prev=03fc0effe8e2dcc5df322b9d745f499582d187b6 image=sha256:fc34ac79d2639dcdb9681d63fb27a9f380f2be40bc07de61727f71340276d9f8
Sep 24 07:39:18 ubuntu-16gb-hel1-1 haven-deploy[2064841]: 2026-09-24T07:39:18Z STOPPED cellscaffold-app-1 — nedetiden starter her
Sep 24 07:39:31 ubuntu-16gb-hel1-1 haven-deploy[2064841]: 2026-09-24T07:39:31Z READY_OK (foerste-start) etter 15s
Sep 24 07:39:42 ubuntu-16gb-hel1-1 haven-deploy[2064841]: 2026-09-24T07:39:42Z READY_OK (restart) etter 15s
Sep 24 07:39:43 ubuntu-16gb-hel1-1 haven-deploy[2064841]: 2026-09-24T07:39:43Z COMMITTED_VERIFIED
Sep 24 07:39:43 ubuntu-16gb-hel1-1 haven-deploy[2064841]: 2026-09-24T07:39:43Z FERDIG — bevis i /mnt/disk1/app/haven-staging-evidence/deploy/20260924T073914Z-staging-60e5a64d
```
`https://staging.haven.digipomps.org/health/build`: `{"dimymicropayments_revision":"836ba8e6d71663d78836e2ec67a1e6f38bd8655b","cellprotocol_revision":"473357cf4efee831cb3b55ae87bc921d4bb63c10","environment":"staging","status":"ok","app_revision":"60e5a64d1c2a4a9f4e2b3fa53e45ed2d63f6aaba","build_timestamp":"2026-09-24T04:05:43Z","dimymint_revision":"af`

## production

`sudo -n haven-ghcr-prefetch-production 60e5a64d1c2a4a9f4e2b3fa53e45ed2d63f6aaba` → exit 0
`sudo -n haven-deploy-doctor production` → exit 0
`sudo -n haven-deploy production 60e5a64d1c2a4a9f4e2b3fa53e45ed2d63f6aaba --preflight` → exit 0
Enhet `haven-deploy@production-60e5a64d1c2a4a9f4e2b3fa53e45ed2d63f6aaba`: `inactive`
```text
Sep 24 07:40:10 ubuntu-16gb-hel1-1 haven-deploy[2068142]: 2026-09-24T07:40:10Z PREFLIGHT miljoe=production commit=60e5a64d1c2a4a9f4e2b3fa53e45ed2d63f6aaba txn=20260924T074010Z-production-60e5a64d
Sep 24 07:40:12 ubuntu-16gb-hel1-1 haven-deploy[2068142]: 2026-09-24T07:40:12Z PREFLIGHT_GREEN prev=03fc0effe8e2dcc5df322b9d745f499582d187b6 image=sha256:fc34ac79d2639dcdb9681d63fb27a9f380f2be40bc07de61727f71340276d9f8
Sep 24 07:40:23 ubuntu-16gb-hel1-1 haven-deploy[2068142]: 2026-09-24T07:40:23Z STOPPED cellscaffold-production-app-1 — nedetiden starter her
Sep 24 07:40:32 ubuntu-16gb-hel1-1 haven-deploy[2068142]: 2026-09-24T07:40:32Z READY_OK (foerste-start) etter 10s
Sep 24 07:40:38 ubuntu-16gb-hel1-1 haven-deploy[2068142]: 2026-09-24T07:40:38Z READY_OK (restart) etter 10s
Sep 24 07:40:38 ubuntu-16gb-hel1-1 haven-deploy[2068142]: 2026-09-24T07:40:38Z COMMITTED_VERIFIED
Sep 24 07:40:38 ubuntu-16gb-hel1-1 haven-deploy[2068142]: 2026-09-24T07:40:38Z FERDIG — bevis i /mnt/HC_Volume_104775511/haven-production-evidence/deploy/20260924T074010Z-production-60e5a64d
```
`https://haven.digipomps.org/health/build`: `{"dimymicropayments_revision":"836ba8e6d71663d78836e2ec67a1e6f38bd8655b","cellprotocol_revision":"473357cf4efee831cb3b55ae87bc921d4bb63c10","app_revision":"60e5a64d1c2a4a9f4e2b3fa53e45ed2d63f6aaba","package_resolved_source":"\/app\/BuildMetadata\/Package.resolved","dimymint_revision":"af41630bbc01ce`

