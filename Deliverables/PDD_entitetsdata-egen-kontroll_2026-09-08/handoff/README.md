# Overlevering til Codex — entitetsdata egen kontroll

Denne mappen fylles per runde fra `PLAN.md` §4. Én mappe per runde, ikke én stor.

## Rekkefølge

1. `runde1/preflight.sh` — sjekker uten å endre noe
2. `runde1/apply.sh` — tørrkjører som standard, endrer først med `--go`
3. `runde1/verify.sh` — kjører testene runden navngir

Hver kommando står på egen linje uten forklaring bak seg.

## Regler som gjelder alle skriptene

- Tørrkjøring er standard. `--go` er det eneste som endrer noe.
- Skriptene er idempotente: å kjøre dem to ganger gir samme tilstand som én gang.
- Preflight avbryter før første endring hvis noe ikke stemmer.
- **Ingen git-kommandoer via device_bash.** Mounten kan ikke unlinke, så `git` der etterlater
  låsefiler. Git kjøres i Kjetils terminal eller av Codex på macOS.
- Preflight sjekker alltid, før noe annet:
  - `git status --short` er ren for filene runden rører
  - `git rev-parse HEAD` mot `git rev-parse origin/main` — er lokal main foran, er de commitene
    ikke main for andre (`lesson.local-main-is-not-main`)
  - `swift package edit` er ikke aktiv
  - avhengighetspinner peker på revisjoner som ligger på avhengighetens egen main
    (`lesson.pin-must-be-on-their-main`)

## Hva som aldri hører hjemme her

`Binding/.sprout/import/HAVEN_import_bokprosjekt.xlsx` inneholder 189 virkelige personer. Den er
gitignorert og skal aldri inn i et repo, heller ikke som testfixture. Fixturer lages syntetisk.

## Hvorfor overleveringen finnes

Cowork-VM-en har ingen Swift-verktøykjede. Alt som må bygges eller kjøres i Swift går derfor
herfra til en maskin som kan det. Et skript som ikke kan kjøres uten å gjette er ikke en
overlevering — det er en beskrivelse av en overlevering.
