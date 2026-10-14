# Overlevering — hvordan strakstiltaket kjøres

Alt kjøres på Mac-en (bruker kjetil) gjennom køen `_losen-queue` som `skript`-jobber i bane d.
Stier er relative til HAVEN-roten. `HD` står for `HAVEN-Deploy/_handoff/HD-0077`, `PS` for `PalazzoScaffold`.
Les `_losen-queue/LES_MEG.md` og `_losen-queue/KOORDINERING.md` først. Prompt før `.job`, via `.tmp` og `mv -n`.
Aldri git mot Cowork-monteringen. Ingen vertsmutasjon uten egen claim. Ingen bygging på verten.

| Steg | Skript | Argument | Forventet utfall | Tørrkjøring |
|---|---|---|---|---|
| Grunnlinje | `HD/mac/strakstiltak-t0b-20261006.sh` | – | `T0 GROENN tester=265` | leser og bygger; den eneste sporede filen som røres, er `Package.resolved`, som legges tilbake |
| Svarene før | `HD/mac/strakstiltak-kjede-20261006.sh` | `foer` | svarene i `HD/maal/`, fiksturen «før» | legger inn usporede filer i `PS`, og legger `Package.resolved` tilbake |
| Tester først | samme | `roed` | de 265 gamle grønne; T1, T3 og T5 røde | som over |
| Endringen | samme | `groenn` | hele testmengden grønn; `node --test` grønn | endrer arbeidstreet; committer ikke |
| Rydd | samme | `rydd` | treet som `a3fc5042` | – |
| Et sett gjennom koden | `HD/mac/strakstiltak-sett-20261006.sh` | JSON-fil under `HD/` | én rad per spørsmål; sluttlinjen sier antall merkinger og svar uten linje. Skriptet stopper ikke selv | endrer ingen kildefil; skriver svarene til `HD/maal/sett-ut/` og legger `Package.resolved` tilbake |
| Commit | `HD/mac/deploy-commit-20261003.sh` | meldingsfil under `HD/`; fillisten ved siden av med endelsen `.filer` | commiten har nøyaktig filene i listen | nei |
| Push og CI | `HD/mac/deploy-push-20261003.sh` | `deploy/palazzo-demo-20260930` | `conclusion=success` og image `sha-<commit>` | nei |
| Lest før byttet | `HD/mac/strakstiltak-les-foer-utsetting-20261006.sh` | 40 tegn sha for utgaven som står | `claims_paa_verten=0 gammelt_image_lokalt=ja ghcr_gammelt=ok` | endrer ingenting på verten; skriver to logger under `HD/evidence/`; GHCR-kontrollen logger inn fra verten med en midlertidig konfigurasjon |
| Utsetting | `HD/mac/strakstiltak-utsett-20261006.sh` | 40 tegn commit-sha | leser først og stopper for enhver claim; så `HD/mac/deploy-vert-20261003.sh`: claim, bytte, kontroll utenfra, `COMMITTED_VERIFIED`, claimen sluppet | nei |
| Måling på nett | `HD/mac/strakstiltak-maal-nett-20261006.sh` | liste under `HD/mac/` | én rad per kall; sluttlinjen sier antall merkinger og svar uten linje | kun lesing |
| Veien tilbake | `HD/mac/tilbake-vert-20261006.sh` | `<40 tegn sha>` tørrkjører; `<40 tegn sha>:utfoer` bytter | `TILBAKE FERDIG` | ja, uten `:utfoer` |

Veien tilbake brukes bare på Kjetils ord. Utgaven før tiltaket er `a3fc5042e15bbb6d2b896c116d980cad0b21bf2e`.

Det som ikke har tørrkjøring: commit, push og utsetting. Det er samme hull som i runde 2, og det står.
