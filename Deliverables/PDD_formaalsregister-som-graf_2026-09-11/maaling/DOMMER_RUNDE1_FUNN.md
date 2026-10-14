# Dommerrunde 1 — funn (2026-09-14)

Dommer: Kjetil, i Safari, via artefaktet «Dommerbenken». Rådata: `dommer_runde1.json` i denne mappen.
Snapshot: `1437e34b…6f00f`. Stier relative til `HAVEN/`.

## Tallene

| | |
|---|---|
| Oppgaver vurdert | 15 av 15 |
| Lærdomsrader | 197 |
| «Ville endret noe» | **197** |
| «Nei» | **0** |
| «Usikker» | **0** |
| Tid per oppgave, median | 352 s |
| Tid, første to oppgaver | 7 094 s og 1 158 s |
| Tid, siste fem oppgaver | 44, 39, 36, 25, 44 s |

## Hva dette er, og hva det ikke er

**Dette er en instrumenteringsrunde, ikke en fasit.** Med 197 ja og 0 nei skiller fasiten ikke mellom
noen kandidater: begge metoder får presisjon 1,0 på den, og den kan derfor ikke avgjøre om den ene er
bedre enn den andre. Det er nøyaktig tilfellet `PurposeContract` nekter å gate på — positiv referanse lik
alt, ingen null å skille fra.

Kjetil sa det selv før tallene var telt: «Dette er en start eller utgangspunkt.» Det stemmer, og grunnen er
målbar.

## Hvorfor det ble «alle ja» — feilen er i målingen, ikke i dommeren

1. **Ingen negativer ble vist.** Radene var unionen av to metoders topp-10. Alt dommeren så, var allerede
   filtrert som «sannsynligvis relevant». Uten lokkeduer fra de 28–33 lærdommene utenfor topp-10 hadde «nei»
   ingenting å feste seg til. Det er samme feilklasse som å teste uten null.
2. **Matcheren skiller ikke mellom oppgaver.** `lesson.cellbase-decodingerror-shadows-swift` står i
   topp-10 for **11 av 15** oppgaver — også for `palazzo-sicilia-artikler` og `musikkstatistikk`, der en
   CellBase-dekodingsfeil neppe ville endret noe. `entityanchor-keypaths-are-registered` også 11 av 15.
   Når listene er nesten like fra oppgave til oppgave, kan ikke dommeren skille dem heller.
3. **Tidskurven viser tretthet.** To timer på den første, under et minutt på de fem siste. De siste fem er
   klikket gjennom, ikke dømt. Det er ikke kritikk — det er hva som skjer når en flate viser samme tretti
   lærdommer femten ganger.

## Det som faktisk virket

Notatfeltet ga et ekte signal som ja/nei-kanalen ikke kunne gi: Kjetil navnga **gjentakelser** i 8 av 15
oppgaver, konsekvent og uoppfordret. Topp: `cellbase-decodingerror-shadows-swift` (9 ganger),
`valuetype-equality-false-for-objects` (5), `ciphertext-field-held-plaintext-hash` (4),
`entityanchor-keypaths-are-registered` (4).

Det er data om **registeret**, ikke om matcheren: en lærdom som returneres til alle oppgaver bærer ingen
informasjon om noen av dem. Vekten dens i matching bør *synke* etter hvert som den dukker opp overalt.
Det er nøyaktig det Vegars Oja-glemmeterm gjør mekanisk (−η·y²·w: kanter inn til samme node konkurrerer,
og en kant som fyrer for alt, svekkes). «Nevnt før» er første feltbevis for at vi trenger den.

## Neste runde — det som må være annerledes

- **Blind blanding.** Hver oppgave viser topp-10-treff *og* lokkeduer trukket fra lærdommene utenfor
  topp-10, uten å merke hvilke som er hvilke. Da har «nei» noe å feste seg til, og en dommer som svarer ja
  på alt, avsløres av lokkeduene.
- **Strammere kriterium.** Ikke «ville endret noe», men «nevn hvilket valg, hvilken test eller hvilken
  avgrensning den ville endret». Ett ord holder. Uten et navn er svaret nei.
- **Færre oppgaver per økt.** Fem, ikke femten. Tidskurven sier at dommen dør etter den syvende.
- **Repetisjonssignalet tas inn som eget felt**, siden det var det Kjetil faktisk ga oss.

Dette er ikke bortkastet: runden avslørte at målingen manglet null, og at matcheren ikke skiller. Begge
deler var ukjent i går.
