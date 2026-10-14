# Deploy coordination — skjelettrunden til staging — 2026-09-22

```yaml
work_id: deploy-skjelettrunden-20260922
status: QUEUED
created_at: "2026-09-22T10:35:00+02:00"
host: ops@89.167.90.101
containers: { staging: cellscaffold-app-1 (health 127.0.0.1:8081), production: cellscaffold-production-app-1 (health 127.0.0.1:8084) }
current: { staging: sha-945d5c02 (2026-08-26), production: sha-e3ae9fc0 (2026-09-18) }
code_change: CellScaffold PR #251 (Butler-arbeidsflate, web-renderer-paritet, radbryting, tre nye pinner)
mutation_type: image-deploy via haven-deploy (ingen env-endring, ingen skjemaendring)
owner: Kjetil
executed_by: Claude (Butler) gjennom `_losen-queue` på Kjetils Mac — Kjetil ga tillatelsen 2026-09-22 («Jeg kjører hele veien til staging»)
registered_in_advance: true
depends_on: []
```

## Formål

Funksjonaliteten som er implementert på Kjetils maskin skal ende opp deployet på prod, via
`origin/main`, derfra staging, derfra prod (`HAVEN-Deploy/docs/Leveransegap.md`). Denne runden
tar den til **staging**. Prod røres ikke uten at Kjetil sier fra.

## Kjeden som er kjørt til nå

| Ledd | Revisjon | Status |
|---|---|---|
| CellProtocol | `473357cf` | PR #44 merget |
| DiMyMicropayments | `836ba8e6` | PR #14 merget |
| DiMyMint | `af41630b` | PR #14 merget (pin + eksakt-kilde-porten flyttet sammen) |
| CellScaffold | PR #251 | venter på `Focused control-plane gates` |

SwiftPM godtar bare ett revisjonskrav per pakke, og hvert ledd bærer sitt eget krav til det
under. Derfor måtte kjeden ryddes nedenfra før CellScaffold kunne peke på den nye CellProtocol.

## Stegene som gjenstår

| Steg | Kommando | Verifiseres av |
|---|---|---|
| 1 | merge PR #251 → `origin/main` | `gh pr view` viser MERGED, ny main-sha |
| 2 | `gh workflow run admin-scaffold-image.yml --ref main -f release_note=…` | kjøringen ender `success`; image `ghcr.io/digipomps/cellscaffold-web:sha-<main>` |
| 3 | `sudo -n haven-ghcr-prefetch <sha>` (ops) | exit 0, retag til `cellscaffold-staging-local` |
| 4 | `sudo -n haven-deploy-doctor staging` | exit 0 |
| 5 | `sudo -n haven-deploy staging <sha> --preflight` | exit 0 |
| 6 | `sudo -n systemctl start haven-deploy@staging-<sha>` | enheten ender ikke som `failed`; journal viser COMMITTED_VERIFIED |
| 7 | `curl https://staging.haven.digipomps.org/health/build` | svaret inneholder `<sha>` |

Auto-rollback ved feilet readiness er innebygd i `haven-deploy`; den gamle containeren beholdes
som `<navn>-rollback-<txn>`.

## Kjent hull i bevisføringen

Det lokale CI-filteret (`ci/run-tests.sh`) kom ikke i gang i PR-runden: diskvakten krever
≥40 GiB **og** ≥5 % ledig, og maskinen har 43 GiB av 927 GiB (4 %). Klassifiseringen ble tom.
Porten inn til main er GitHub-CI (`Focused control-plane gates`), og den er det som gjelder her.
`wp-lev-cs-pr.sh` er rettet slik at en tom klassifisering aldri igjen teller som grønn.
