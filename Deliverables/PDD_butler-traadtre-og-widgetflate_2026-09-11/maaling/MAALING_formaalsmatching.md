# Måling: har formålsdrevet utvikling målbar nytte av strammere formålsmatching?

Kjørt 2026-09-11 mot `Book/haven_lessons_register_v0.json` (44 lærdommer),
`Book/haven_purpose_packages_v0.json` og de 18 `Deliverables/PDD_*`-mappene.
Matcheren som måles er `Tools/PurposePackages/purpose_dev.py lookup` selv — ikke en
kopi av logikken (`lesson.tested-a-different-path-than-production`).
Skriptene ligger ved: `maal_matching.py`, `maal_haandhevelse.py`.

## Det som er målt, og som holder

**Matcheren velger nesten ikke.** Et oppslag returnerer i snitt **34,9 av 44**
lærdommer (79 %), minimum 29, maksimum 44. Jaccard-likheten mellom to vilkårlige
oppgavers treffsett er i snitt **0,82**, og **23 lærdommer returneres til alle 18
oppgavene**. En matcher som gir nesten samme svar uansett spørsmål bærer nesten
ingen informasjon.

**Registeret er ikke problemet.** **0 av 44** lærdommer er døde — hver eneste
returneres til minst én oppgave. Det er selektiviteten som mangler, ikke innholdet.

**To tredjedeler er ikke håndhevet.** Bare **15 av 44** lærdommer er referert fra en
formålspakke og kan dermed bli en `derivedTest`. De øvrige **29** finnes bare i
registeret og må huskes av et menneske ved hver dekomponering.

**Gjentakelsene klumper seg.** Temaene som går igjen er `codex` (9 par),
`handoff` (5), `gui` (3). Alvorlighet på de gjentatte: 3 blocker, 4 major, 9 minor.

## Det som IKKE lar seg måle ennå — og hvorfor

Jeg forsøkte å måle det som faktisk betyr noe: *ble en lærdom gjentatt selv om
matcheren hadde vist den på forhånd?* Første kjøring ga 8 av 11. **Det tallet holder
ikke.** Definisjonen av «samme mønster» var «minst 2 felles tags og minst én felles
purposeRef». Senker man kravet til 3 felles tags, faller antallet gjentakelsespar fra
16 til **0**. Et mål som kollapser helt ved ett hakks endring i terskelen, måler
terskelen og ikke virkeligheten.

Den underliggende grunnen er verdt mer enn tallet: **registeret har ikke struktur nok
til å definere et treff.** Det finnes ingen etikett som sier hvilke lærdommer som
faktisk var relevante for en oppgave, og ingen kobling fra lærdom til den testen som
skal hindre den. Uten en fasit kan hverken presisjon eller dekning regnes ut.

## Svaret på spørsmålet

Det er **stort målbart slingringsmonn** i matchingen — 79 % returnert, 0,82 i
overlapp, 23 lærdommer til alle. Men **nytten av å stramme den er ikke målbar i dag**,
og den har sannsynligvis et tak: når to tredjedeler av lærdommene uansett bare er noe
et menneske skal huske, flytter bedre utvelgelse hvilke 30 avsnitt som vises, ikke om
feilen skjer igjen. Den største enkeltgevinsten ligger ikke i matcheren, men i at en
lærdom blir en test.

## Hva som må instrumenteres for at spørsmålet skal kunne besvares

1. **Fasit per oppgave.** Ved G1 krysses det av hvilke av de returnerte lærdommene som
   faktisk var relevante. Etter ti oppgaver har vi presisjon, målt og ikke antatt.
2. **`preventedBy` på hver lærdom** — enten en `derivedTest`-referanse, eller eksplisitt
   `unenforced` med grunn. I dag er 29 av 44 uten.
3. **`repeatOf` når en lærdom gjentar en tidligere.** Da slipper vi tag-heuristikk, og
   gjentakelse blir et faktum noen har skrevet ned, ikke noe jeg gjetter meg til.

## Billigste ekte eksperiment

`codex` og `handoff` står for 14 av 16 gjentakelsespar. Instrumenter de to først: legg
`preventedBy` på alle codex-/handoff-lærdommene, og krev fasit-avkryssing ved G1 for de
neste ti oppgavene. Det gir et tall på om strammere matching virker, innenfor det
området der feilene faktisk gjentar seg — og det gir svaret på uker, ikke måneder.
