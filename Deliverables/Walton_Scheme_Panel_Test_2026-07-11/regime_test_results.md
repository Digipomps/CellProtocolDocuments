# Regime-test: skjema-stillas × analytiker-styrke (empirisk)

Dato: 2026-07-11. Kjørt via `Tools/ModelKnowledge/run_advisory_panel.py` (NanoGPT).
Spec: `Tools/ModelKnowledge/panels/walton_scheme_regime_test_2026-07-11.json`.
Rådata: `Tools/ModelKnowledge/generated/panel_walton_scheme_regime_test_2026-07-11_20260711T100237Z.json`.

## Design

Samme anonymiserte case (hosted-only-forslaget) til 3 modeller × 2 armer:
uassistert kritisk analyse vs. Walton-skjema-stillas (11 kritiske spørsmål for
rot + 3 premisser, ordrett fra `ClaimSchemeCatalog`). Ingen repo-tilgang.
Scoring mot gullsett på 9 funn etablert av de kapable kjøringene + panel-testen
(G1 nabooppgave-relevans, G2 konfundere/størrelse-vs-lane, G3 TCO/volum,
G4 leverandørinnlåsing, G5 EU-region nødvendig-ikke-tilstrekkelig,
G6 dataklasse-hard-stopp, G7 hybrid-alternativ, G8 offline/resiliens-tap,
G9 ekvivokasjon på «GDPR løst»). 0 / 0,5 / 1 per funn, sitat-forankret.

## Resultat

| Modell | Uassistert | Med skjema | Delta | Merknad |
| --- | ---: | ---: | ---: | --- |
| llama-3.2-3b | 4,0 | 4,5 | +0,5 | Stillas-eksekvering svak: forvirrede ANSWERED-statuser på rot-CQ-ene; mistet G8 som uassistert fant |
| Qwen3-8B | 7,0 | 8,0 | +1,0 | Renest CQ-gevinst (G2+G9 vunnet); mistet G6 — sjekkliste-tunnelsyn |
| gpt-5.5 (kontroll) | 8,5 | 9,0 | +0,5 | Nesten tak i begge armer |

Per-funn-mønsteret er viktigere enn totalene:

- **G9 (ekvivokasjon på «GDPR løst»)**: 0/3 uassistert (gpt-5.5 0,5) → **3/3 med
  skjema.** `verbal-classification.definition` tvinger frem diagnosen på alle nivåer.
- **G2 (konfundere for benchmark-gapet)**: 1/3 uassistert (kun gpt-5.5) → **3/3
  med skjema.** `sign.alternatives` leverer deterministisk.
- Motsatt retning finnes også: skjema-armen **mistet** funn uassistert-armen
  hadde (3B: G8; 8B: G6) — modellen følger sjekklisten og slutter å lete fritt.

## Konklusjon mot regime-hypotesen

Hypotesen «verdien vokser når analytiker-styrken faller» er **ikke bekreftet i
sin enkle form**. Observert mønster:

1. **Liten positiv totaldelta på alle nivåer** (+0,5 til +1,0), størst i
   mellomsjiktet (8B), ikke hos den svakeste.
2. **Omvendt U**: 3B er for svak til å *utnytte* stillaset (statusforvirring),
   frontier trenger det knapt; mellomsjiktet tjener mest.
3. **Den reelle effekten er per-spørsmål-garanti, ikke totalløft**: bestemte
   kritiske spørsmål (definisjonskritikk, konfunder-jakt) leveres pålitelig av
   stillaset på alle nivåer, men mistes ofte uassistert under frontier-nivå.
4. **Sjekkliste-tunnelsyn er reelt**: skjema-armen kan fortrenge frie funn —
   direkte støtte for guard 1 (skjemaer som *tillegg* der CQ-er ventes åpne/
   utfordret, aldri som erstatning for fri analyse).

Bonusfunn: Qwen3-8B fant uassistert leverandørinnlåsingen (G4) som begge de
kapable baseline-kjøringene 6. juli bommet på — analytiker-*mangfold* har
selvstendig verdi uavhengig av stillas.

## Begrensninger

n=1 per celle, én case, én grader (sitat-forankret, men skjønn i 0,5-tilfeller),
og arm B har annet outputformat enn arm A (formatkrav kan i seg selv påvirke
dekning). Retningene er konsistente på tvers av modeller, men størrelsene er
ikke presise estimater.
