STATUS: LEVERT — image-settet publisert for sha-77a922bc301a0ea7586a6b3677a87c2b1e0f73f7 (kjoering 35731001599)

# Leveranse steg 3 — image-settet for main

Skrevet av `HAVEN-Deploy/_handoff/WP-R/wp-lev-bilde.sh` 2026-09-22T15:08:24Z. Bevis: `evidence/leveranse-bilde/`.

CellScaffold `origin/main` @ `77a922bc301a0ea7586a6b3677a87c2b1e0f73f7`.

Koordinering: foer = (no active claims); claim exit 2 — hd: invalid task id 'deploy-skjelettrunden-20260922' (expected HD-nnnn).

Dispatch sendt med release_note: «Skjelettrunden: Butler-arbeidsflaten, web-renderer-paritet og de nye pinnene (CellProtocol 473357cf, DiMyMicropayments 836ba8e6, DiMyMint af41630b). main 77a922bc301a0ea7586a6b3677a87c2b1e0f73f7.»

Kjoering: `35731001599` — https://github.com/Digipomps/CellScaffold/actions/runs/35731001599

Sluttilstand: `in_progress  77a922bc301a0ea7586a6b3677a87c2b1e0f73f7`.


## Venting

Venter videre paa kjoering `35731001599` — https://github.com/Digipomps/CellScaffold/actions/runs/35731001599

Sluttilstand: `completed success 77a922bc301a0ea7586a6b3677a87c2b1e0f73f7`.

```text

✓ main AdminScaffold immutable images · 35731001599
Triggered via workflow_dispatch about 2 hours ago

JOBS
✓ Focused control-plane gates in 52m16s (ID 106756253602)
✓ Publish signed-source image pair in 1h49m38s (ID 106775910889)

ANNOTATIONS
! Node.js 20 is deprecated. The following actions target Node.js 20 but are being forced to run on Node.js 24: actions/upload-artifact@v4. For more information see: https://github.blog/changelog/2025-09-19-deprecation-of-node-20-on-github-actions-runners/
Focused control-plane gates: .github#2

! Input 'app-id' has been deprecated with message: Use 'client-id' instead.
Focused control-plane gates: .github#1

! Input 'app-id' has been deprecated with message: Use 'client-id' instead.
Focused control-plane gates: .github#1

! Node.js 20 is deprecated. The following actions target Node.js 20 but are being forced to run on Node.js 24: actions/upload-artifact@ea165f8d65b6e75b540449e92b4886f43607fa02, docker/build-push-action@263435318d21b8e681c14492fe198d362a7d2c83, docker/login-action@74a5d142397b4f367a81961eba4e8cd7edddf772, docker/setup-buildx-action@e468171a9de216ec08956ac3ada2f0791b6bd435. For more information see: https://github.blog/changelog/2025-09-19-deprecation-of-node-20-on-github-actions-runners/
Publish signed-source image pair: .github#6

! Input 'app-id' has been deprecated with message: Use 'client-id' instead.
Publish signed-source image pair: .github#1

! Input 'app-id' has been deprecated with message: Use 'client-id' instead.
```

Image-settet er `ghcr.io/digipomps/cellscaffold-web:sha-77a922bc301a0ea7586a6b3677a87c2b1e0f73f7` (og -admin, -node-admin-tools).

Neste steg: staging fra dette imaget — `haven-ghcr-prefetch`, `haven-deploy-doctor staging`, `haven-deploy staging 77a922bc301a0ea7586a6b3677a87c2b1e0f73f7 --preflight`, `systemctl start haven-deploy@staging-77a922bc301a0ea7586a6b3677a87c2b1e0f73f7`, og verifisering mot /health/build.
