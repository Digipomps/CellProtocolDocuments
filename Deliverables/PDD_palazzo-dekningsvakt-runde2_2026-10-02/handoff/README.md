# Overlevering — hvordan runde 2 kjøres

Alt kjøres på Mac-en (bruker kjetil) gjennom køen `_losen-queue` som `skript`-jobber i
bane d. Stier er relative til HAVEN-roten. `HD` står for `HAVEN-Deploy/_handoff/HD-0077`.
Ingen skript har tørrkjøring (`--dry-run`); det er et kjent hull, ført i `FORMAALSSPEC.md` §5.

| Steg | Skript | Argument | Forventet utfall |
|---|---|---|---|
| 1 Test | `HD/mac/cp-pin-verifiser-og-test-20260929.sh` | `81601a6f835252aba7e99d43786fb5d67227c245` | `swift build rc=0`, `swift test rc=0`, antall tester og null feil |
| 2 Sett gjennom vakten | `HD/mac/vakt-sett-20261003.sh` | en JSON-fil under `HD/` | én linje per omskriving: godtatt eller forkastet med regel |
| 3 Commit | `HD/mac/deploy-commit-20261003.sh` | meldingsfil under `HD/`; fillisten ligger ved siden av med endelsen `.filer` | commiten har nøyaktig filene i listen |
| 4 Push og CI | `HD/mac/deploy-push-20261003.sh` | `deploy/palazzo-demo-20260930` | `conclusion=success` og image `sha-<commit>` |
| 5 Deploy | `HD/mac/deploy-vert-20261003.sh` | 40 tegn commit-sha | claim, deploy, kontroll utenfra, `COMMITTED_VERIFIED`, claim sluppet |
| 6 Mål | `HD/mac/spoer-liste-20261002.sh` | `HD/mac/spoersmaal-runde2-20261003.txt` | tolv svar med rute og tekst |
| 7 Logg | `HD/mac/vaktlogg-20261003.sh` | antall minutter bakover | én linje per svar med utfallet |

Regler som gjelder hvert steg: les `_losen-queue/LES_MEG.md` og `_losen-queue/KOORDINERING.md`
først; prompt før `.job`, via `.tmp` og `mv`; aldri git mot Cowork-monteringen; ingen
vertsmutasjon uten egen claim.
