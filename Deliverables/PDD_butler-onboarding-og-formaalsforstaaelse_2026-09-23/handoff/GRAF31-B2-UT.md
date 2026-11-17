STATUS: LEVERT — staging og prod kjører sha-6c70a59211e6be93ec33f5ba46a033bd103cb9ac (leveranse 2 + formålsgraf v3.1)

# Formålsgraf v3.1 — steg B2: staging og prod

Skrevet av `HAVEN-Deploy/_handoff/BUTLER-MAALING/graf/wp-graf31-b2-ut.sh` 2026-09-24T11:54:19Z.

Image: `ghcr.io/digipomps/cellscaffold-web:sha-6c70a59211e6be93ec33f5ba46a033bd103cb9ac`

## staging

`sudo -n haven-ghcr-prefetch 6c70a59211e6be93ec33f5ba46a033bd103cb9ac` → exit 0
`sudo -n haven-deploy-doctor staging` → exit 0
`sudo -n haven-deploy staging 6c70a59211e6be93ec33f5ba46a033bd103cb9ac --preflight` → exit 0
Enhet `haven-deploy@staging-6c70a59211e6be93ec33f5ba46a033bd103cb9ac`: `inactive`
```text
Sep 24 11:53:10 ubuntu-16gb-hel1-1 haven-deploy[2400270]: 2026-09-24T11:53:10Z PREFLIGHT miljoe=staging commit=6c70a59211e6be93ec33f5ba46a033bd103cb9ac txn=20260924T115310Z-staging-6c70a592
Sep 24 11:53:12 ubuntu-16gb-hel1-1 haven-deploy[2400270]: 2026-09-24T11:53:12Z PREFLIGHT_GREEN prev=60e5a64d1c2a4a9f4e2b3fa53e45ed2d63f6aaba image=sha256:3c36b6b491c1386bfcf462a3ac6914f74ab0ef892c6e3e498982d08ae345967c
Sep 24 11:53:23 ubuntu-16gb-hel1-1 haven-deploy[2400270]: 2026-09-24T11:53:23Z STOPPED cellscaffold-app-1 — nedetiden starter her
Sep 24 11:53:36 ubuntu-16gb-hel1-1 haven-deploy[2400270]: 2026-09-24T11:53:36Z READY_OK (foerste-start) etter 15s
Sep 24 11:53:47 ubuntu-16gb-hel1-1 haven-deploy[2400270]: 2026-09-24T11:53:47Z READY_OK (restart) etter 15s
Sep 24 11:53:47 ubuntu-16gb-hel1-1 haven-deploy[2400270]: 2026-09-24T11:53:47Z COMMITTED_VERIFIED
Sep 24 11:53:47 ubuntu-16gb-hel1-1 haven-deploy[2400270]: 2026-09-24T11:53:47Z FERDIG — bevis i /mnt/disk1/app/haven-staging-evidence/deploy/20260924T115310Z-staging-6c70a592
```
`https://staging.haven.digipomps.org/health/build`: `{"package_resolved_source":"\/app\/BuildMetadata\/Package.resolved","dimymicropayments_revision":"836ba8e6d71663d78836e2ec67a1e6f38bd8655b","app_revision":"6c70a59211e6be93ec33f5ba46a033bd103cb9ac","status":"ok","cellprotocol_revision":"473357cf4efee831cb3b55ae87bc921d4bb63c10","dimymint_revision":"`

## production

`sudo -n haven-ghcr-prefetch-production 6c70a59211e6be93ec33f5ba46a033bd103cb9ac` → exit 0
`sudo -n haven-deploy-doctor production` → exit 0
`sudo -n haven-deploy production 6c70a59211e6be93ec33f5ba46a033bd103cb9ac --preflight` → exit 0
Enhet `haven-deploy@production-6c70a59211e6be93ec33f5ba46a033bd103cb9ac`: `inactive`
```text
Sep 24 11:53:58 ubuntu-16gb-hel1-1 haven-deploy[2403546]: 2026-09-24T11:53:58Z PREFLIGHT miljoe=production commit=6c70a59211e6be93ec33f5ba46a033bd103cb9ac txn=20260924T115358Z-production-6c70a592
Sep 24 11:54:00 ubuntu-16gb-hel1-1 haven-deploy[2403546]: 2026-09-24T11:54:00Z PREFLIGHT_GREEN prev=60e5a64d1c2a4a9f4e2b3fa53e45ed2d63f6aaba image=sha256:3c36b6b491c1386bfcf462a3ac6914f74ab0ef892c6e3e498982d08ae345967c
Sep 24 11:54:00 ubuntu-16gb-hel1-1 haven-deploy[2403546]: 2026-09-24T11:54:00Z STOPPED cellscaffold-production-app-1 — nedetiden starter her
Sep 24 11:54:08 ubuntu-16gb-hel1-1 haven-deploy[2403546]: 2026-09-24T11:54:08Z READY_OK (foerste-start) etter 10s
Sep 24 11:54:14 ubuntu-16gb-hel1-1 haven-deploy[2403546]: 2026-09-24T11:54:14Z READY_OK (restart) etter 10s
Sep 24 11:54:14 ubuntu-16gb-hel1-1 haven-deploy[2403546]: 2026-09-24T11:54:14Z COMMITTED_VERIFIED
Sep 24 11:54:14 ubuntu-16gb-hel1-1 haven-deploy[2403546]: 2026-09-24T11:54:14Z FERDIG — bevis i /mnt/HC_Volume_104775511/haven-production-evidence/deploy/20260924T115358Z-production-6c70a592
```
`https://haven.digipomps.org/health/build`: `{"dimymicropayments_revision":"836ba8e6d71663d78836e2ec67a1e6f38bd8655b","app_revision":"6c70a59211e6be93ec33f5ba46a033bd103cb9ac","cellprotocol_revision":"473357cf4efee831cb3b55ae87bc921d4bb63c10","package_resolved_source":"\/app\/BuildMetadata\/Package.resolved","status":"ok","dimymint_revision":"`

