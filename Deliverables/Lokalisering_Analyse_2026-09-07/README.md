# Lokalisering — analyseoppdrag (2026-09-07)

Innhold: `HANDOFF.md` (formål, audit, leveranse), `L1_ANALYSE_prompt.md` (prompten), `run_l.sh` (start Codex i bakgrunnen).

## Kjøre med Codex (fra Terminal på Macen)
```
cd /Users/kjetil/Build/Digipomps/HAVEN/CellProtocolDocuments/Deliverables/Lokalisering_Analyse_2026-09-07
./run_l.sh L1_ANALYSE
```
- Starter `codex exec` via `launchctl submit` (label `haven.codex.l10n.L1_ANALYSE`) med `model_reasoning_effort=xhigh`, `workspace-write` i denne mappen. Ferdig når `.L1_ANALYSE.done` finnes; svaret er `L1_ANALYSE.md`; Codex' sluttmelding er `L1_ANALYSE_svar.md` (`-o`).
- Vil du teste en annen modell (f.eks. «Astra»): `CODEX_MODEL=<modellnavn> ./run_l.sh L1_ANALYSE` — scriptet legger til `-m $CODEX_MODEL` når variabelen er satt. Skriv modellnavnet slik Codex forventer det; scriptet validerer ikke.
- Ikke start fra Cowork/Claude sitt `codex-local`-verktøy: `danger-full-access` blokkeres av klassifikatoren, og i `workspace-write` overlever ikke launchctl-jobben (lærdom 07.09).

## Kjøre med Claude i stedet
Gi en ny Claude-tråd `HANDOFF.md` og `L1_ANALYSE_prompt.md`; be den skrive `L1_ANALYSE.md` her.

## Etterpå
Losen (eller tråden som eier lokalisering) leser `L1_ANALYSE.md`, oppsummerer for Kjetil, og lager PDD-mappen når Kjetil har svart på Q1–Q4 i HANDOFF §5.
