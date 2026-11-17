# Vektbenken — oppsummering og anbefaling (WP6)

Grunnlag: `maaling/vektbenk-v1.md` (kjørt 29.9 04:21 UTC, arbeidstre `7e390e5`, referanse på `f548282`).
Bilde: `images/vektbenk-valg-v1.png`.

## Kort

- **I dag** oppfyller Palazzo formålet for 3 av 7 simulerte gjester.
- **De foreløpige tallene i koden** (terskel 0,05, negativ vekt 1,0) gir 5 av 7. Vegetaren og Palermo-gjesten får ikke det de skal.
- **Anbefalt** (sett S032): terskel **0**, negativ vekt **0,5**, alt annet uendret. Det gir 7 av 7 og 0 røde flagg.

Bare to av tallene avgjør utfallet for disse gjestene: terskelen og den negative vekten. Tilnærming (`approach`) og forsterkning (`reinforce`) endrer summene, men ikke hva noen får. De stilles best med ekte bruk senere.

## Hvorfor de to endringene

- **Terskel.** Ett felles emne av sju gir 1/7 av trykkets styrke. Et enkelt «Interessant» gir derfor 0,07, og vegetarens beste treff er 0,043. Fra 0,1 og oppover mister gjesten med ett trykk alle tilbud (rødt flagg), og fra 0,2 går de fleste gjestene uten det de skal ha.
- **Negativ vekt.** Vegetaren avviser sarde-pastaen. Med vekt 1,0 trekker det felles emnet «pasta» Pasta alla Norma ned med 0,143, mens «aubergine» fra caponata løfter den med 0,114. Da forsvinner Norma. Med 0,5 blir summen +0,043. En artikkel hun avviser direkte er fortsatt helt stengt.

Losen har regnet summene for sett S032 og S041 på nytt, uavhengig av benken, med formelen fra WP3. De stemmer med benken.

## Det du bør vite før du velger

1. **Terskel 0 betyr «alt med felles emner og en sum som ikke er negativ».** Med åtte artikler er det greit. Med en stor meny kan det bli mange svake tilbud, sortert etter sum. Terskel **0,02** gir samme resultat for alle sju gjestene (regnet, ikke målt), og hindrer tilbud der pluss og minus opphever hverandre til 0. Velger du 0,02, legger Losen den inn i rutenettet og kjører benken én gang til før tallet settes.
2. **Palermo-gjesten får Norma (Catania) øverst**, foran sarde-pastaen fra Palermo. Det skyldes at et trykk på arancini teller alle emnene i artikkelen, og arancini er også fra Catania. Tallene kan ikke rette dette. Det er grensen i formålet: et trykk på en artikkel kan ikke si at bare ett emne var viktig. Brikkene i reaksjonsraden (WP5) er stedet der det senere kan skje.
3. **Grunnstyrkene** (Vil smake 0,8, Interessant 0,5, Ikke for meg 1,0) er ikke variert i denne benken. Du sa 26.9 at noe mening er mer absolutt enn annet. Vil du prøve andre grunnstyrker, kan de legges til i rutenettet.
4. Tallene er brukerens data (`PalazzoWeightPolicy`, Codable). Valget nå er standardverdien i koden.

## Dette gjør du

Svar med én av disse:

- **A — Anbefalt:** terskel 0, negativ vekt 0,5, tilnærming 0,5, forsterkning 0,25 (S032).
- **B — Som A, men terskel 0,02.** Losen måler den først.
- **C — Et annet sett:** oppgi S-nummeret fra `maaling/vektbenk-v1.md`, eller tallene.

Deretter gir Losen Codex WP6: standardverdiene settes i `PalazzoWeightPolicy`, og testen `test.weights.single-positive-gets-offer` med flere får de valgte tallene.
