# Ordklasser, lemma og engelsk i AI-løs formålsmatching (2026-10-10)

Spørsmål (Kjetil): vil ordklasser og lemma gjøre det lettere å knytte meldinger til formål?

Data: Universal Dependencies (CC BY-SA 4.0), UD_Norwegian-Bokmaal, -Nynorsk, -NynorskLIA og UD_English-EWT, til sammen
67 278 ordformer med lemma og ordklasse (`lemma/ud_leks.json`, bygget av `lemma/bygg.py`). Kode: `r6.py`.
Tidligere datasett fra Kallimachos-arbeidet ble ikke funnet på Macen (søkt i HAVEN/Kallimachos og hele HAVEN).

Test: fersk DEV5 (tre nye skribenter: nynorsk fra Sogn, svensk-norsk utvikler som ofte skriver engelsk, pratsom pensjonist
med mange navn og uregelmessige verb; 431 ekte + 135 negativer, sølv). Terskel satt på DEV3+DEV4, aldri på DEV5.
Forseglet sett er brukt opp og er ikke rørt.

| Variant | DEV5 top1, 0 % falske forslag | DEV5 top1, ≤10 % falske | Butler v2 (uavhengig) |
|---|---|---|---|
| R3 (fra 7.10) | 0.510 | 0.787 | 12/112 |
| + lemma + navn tatt ut | 0.652 | 0.775 | 13/112 |
| **+ ordklassestyrt ramme** | **0.729** | 0.796 | 14/112 |
| + engelske erklæringer, språkrutet | 0.466 | 0.747 | 24/112 |
| + engelsk rutet + ordklasseramme + lemma + navn | 0.499 | 0.789 | 23/112 |

Samme mønster på DEV3+DEV4: ordklasseramme 0.270 → 0.526 ved 0 % falske, nøytral ved 10 %.

## Hva det betyr

- **Ordklasser hjelper, lemma alene gjør det ikke.** Lemma ga ingen målbar gevinst: Fables erklæringer har alt de bøyde
  formene, og stemming og fuzzy dekker resten. Ordklassene gir gevinst når de brukes til Kjetils regel: verbet i meldingen
  slås opp mot formålets handlinger, substantivene mot objektene, aldri omvendt. Da blir de riktige svarene mye sikrere
  (top1 ved null falske forslag fra 51 % til 73 %). Ved 10 % falske forslag er det likt (McNemar 11–11).
  Praktisk: med ordklasseramme kan Butler foreslå en flate uten å spørre i langt flere tilfeller.
- **Navn som argumenter** (egennavn tatt ut før matching) ga ingenting målbart.
- **Engelske erklæringer** doblet Butler v2 (12 → 24 av 112, top3 14 % → 30 %), men engelske irrelevante meldinger fikk
  da forslag (20 % ved terskelen fra norske data). Trenger egen terskel for engelsk, kalibrert på engelske negativer.

## Anbefaling

1. Ta inn ordklassestyrt ramme (r6.pos_frame) i matcheren. Krever en form→ordklasse-tabell i Swift (forhåndsberegnet fra
   UD, ingen NLTagger på Linux-serveren).
2. Engelske erklæringer med egen terskel; lag et engelsk negativsett først.
3. Lemma og navnefjerning: ikke verdt det nå.

Forbehold: genererte meldinger; Fable både tolk og forfatter; DEV5 er brukt til å velge mellom fem varianter, så tallene
er litt optimistiske for vinneren.
