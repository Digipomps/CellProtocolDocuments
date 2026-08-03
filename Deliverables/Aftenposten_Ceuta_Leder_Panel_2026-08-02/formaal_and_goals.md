# Formål og Goals — Aftenposten-leder om Ceuta

Dato: 2026-08-02. Oppdragsgiver: Kjetil. Metode: `haven-panel-task-decomposition`
(Book 23/27/29/30). Panelet er ikke stemmemaskin — mennesket eier beslutningen.

## Avgrensning

Objektet er **teksten og saken**, aldri personer. Ingen rangering av mennesker,
ingen omdømmescore, ingen karakteristikk av redaktører. Anti-gapestokk-prinsippet
gjelder. Analysen er sideeffektfri: ingenting publiseres, legges i RAG eller
gjøres til offentlig påstand uten en separat, eksplisitt handling — og i så fall
gjennom `haven-claim-review`.

## Formål

Ingen node i Book 23-taksonomien dekker «evaluere en publisert argumenterende
tekst». Per skillens regel brukes derfor `purpose://prompt.unknown` med registrert
kandidat — ingen purposeRef er oppfunnet.

| ID | purposeRef | Intensjon |
|----|-----------|-----------|
| F1 | `purpose://prompt.unknown` (kandidat: `knowledge.evaluate-published-argument`) | Fastslå hva lederen faktisk hevder, med sitatforankring, skilt fra hva den forutsetter uten å si det |
| F2 | `purpose://prompt.unknown` (kandidat: `source.methodology.current`) | Fastslå om lederens faktapåstander holder mot uavhengig hentede kilder, med ærlige revisjonsstatuser |
| F3 | `purpose://prompt.unknown` (kandidat: `knowledge.evaluate-published-argument`) | Fastslå om argumentasjonen bærer: holder slutningene, er dikotomien uttømmende, er kontrafaktiske utsagn testet mot virkelige instanser |

## Goals (`haven.goal-definition.v1`)

| Goal | Formål | Metrikk | Baseline | Mål | Evidenskilde | Status |
|------|--------|---------|----------|-----|--------------|--------|
| G1 | F1 | Andel bærende claims med verbatim `quoteAnchor` eller eksplisitt `isInferred=true` | 0 % (ingen ledger finnes) | 100 % | Panelets claim-ledger | `unknown` |
| G2 | F2 | Andel bærende faktapåstander med revisjonsstatus fra navngitt hentet kilde | 0 % | 100 % (status satt; `recalled` teller som ikke-støtte, ikke som mangel) | Faktabakgrunn hentet 2026-08-02 + panelets kildegransking | `unknown` |
| G3 | F3 | Andel kontrafaktiske/prediktive utsagn sjekket mot en virkelig instans før sannsynlighet tilskrives (Q6) | 0 % | 100 % | Naturlig-eksperiment-granskerens leveranse | `unknown` |
| G4 | F1+F3 | Andel rot-claims i terminal tilstand (supported / contradicted / logget åpen med grunn og eier) (Q8) | 0 % | 100 % | Adjudikatorrunden | `unknown` |
| G5 | F2+F3 | Andel funn som er klassifisert etter deadline-disiplin: (a) feil ut fra det som var kjent 31.07 21:44, (b) senere utvikling — ikke feil, (c) rammevalg sårbart for noe som alt var i emning | 0 % | 100 %; null kritikk av lederen for post-deadline-hendelser | Panelets funnlister + tidslinjen i briefen | `unknown` |

G5 er den viktigste rettferdighetsvakten i denne saken: mye av eskaleringen
(Italias faktiske grensekontroller, brevet fra 22 regjeringer, dødstallet 67)
kom etter lederens deadline fredag 31.07.2026 kl. 21:44. Kildeteksten er
komplett — se `article_source.md`.

## Panelroller (Book 27 → konkret artefaktansvar)

| Rolle | Modell | Leverer |
|-------|--------|---------|
| Tekstintern analytiker | `openai/gpt-5.6-terra-pro` | Claim-ledger; sitatforankring; kartlagte hull |
| Kildegransker | `google/gemini-3.1-pro-preview-high` | Støtteposter med ærlige revisjonsstatuser |
| Skeptiker | `anthropic/claude-opus-4.8:thinking` | `rebuts`/`undercuts`-komposisjoner |
| Steelman/rimelighetsgransker | `deepseek/deepseek-v4-pro:thinking` | Basestyrking fra motpartskilder; stråmannskontroll |
| Domeneekspert | `x-ai/grok-4.5` | Schengen-/Dublin-hjemler; skjulte premisser |
| Naturlig-eksperiment-gransker | `moonshotai/kimi-k2.6:thinking` | Kontrafaktiske utsagn testet mot Ceuta 2021, Melilla 2022, Evros 2020, Belarus 2021, EU–Tyrkia 2016 |
| Adjudikator | runde 2, i sesjon | Book 29-evaluering; Q1–Q10-blokk |

Modell-ID-ene er verifisert mot NanoGPTs katalog 2026-08-02 (653 modeller).
Modellmangfold er tilsiktet: regime-testen 2026-07-11 viste at mangfoldet i seg
selv har verdi.

## Kjøring

```
python3 build_panel_spec.py
NANOGPT_API_KEY=$(security find-generic-password -a nanogpt -s com.digipomps.cellscaffold.aigateway -w) \
  python3 ../../Tools/ModelKnowledge/run_advisory_panel.py --provider nanogpt \
  --spec ../../Tools/ModelKnowledge/panels/aftenposten_ceuta_leder_2026-08-02.json
```
