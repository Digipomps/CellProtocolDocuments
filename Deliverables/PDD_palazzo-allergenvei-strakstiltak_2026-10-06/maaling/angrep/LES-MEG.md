# LES-MEG: blindt spørsmålssett B2

Skrevet 6. oktober 2026 av den blinde tråden B2.

## Formål

Settene skal brukes til å måle hvor godt en mekanisme kjenner igjen gjestespørsmål om allergi, intoleranse
eller om maten er trygg for helsen, på spørsmål den ikke er laget etter.
Jeg kjenner ikke mekanismen og har ikke sett det tidligere settet. Alt er skrevet ut fra menyen og siden gjesten skriver på.

## Antall

| Fil | Antall | Hva settet er | Riktig utfall |
|---|---|---|---|
| `sett-A.json` | 60 | allergi, intoleranse, trygg mat | skal kjennes igjen |
| `sett-B.json` | 60 | vanlige spørsmål | skal ikke kjennes igjen |
| `sett-C.json` | 20 | grensetilfeller | ingen fasit |
| `sett-D.json` | 20 | som A, men sagt med uvanlige ord | skal kjennes igjen |
| `sett-E.json` | 20 | som B, men med ord som ligner på helse | skal ikke kjennes igjen |

I alt 180 spørsmål. Hvert element har `id`, `tekst`, `slag` og `hvorfor`.
`slag` og `hvorfor` er skrevet på bokmål uansett hvilket språk `tekst` har.

## Språk

Språk eller dialekt står i `slag` for alt som ikke er bokmål, så det går an å telle og filtrere på det.

| Sett | Engelsk | Svensk | Dansk | Tysk | Italiensk | Nynorsk | Dialekt | Bokmål |
|---|---|---|---|---|---|---|---|---|
| A | 12 | 2 | 2 | 2 | 2 | 5 | 4 | 31 |
| B | 12 | 2 | 2 | 2 | 1 | 5 | 4 | 32 |
| C | 4 | 1 | 1 | 1 | 0 | 2 | 1 | 10 |
| D | 4 | 1 | 1 | 1 | 1 | 1 | 2 | 9 |
| E | 4 | 1 | 1 | 1 | 0 | 1 | 2 | 10 |
| I alt | 36 | 7 | 7 | 7 | 4 | 14 | 13 | 92 |

Engelsk er 36 av 180, altså en femtedel. Dialektene er trøndersk, nordnorsk, bergensk og muntlig østlandsk.

## Varianter

- Lengde: fra 13 tegn (B02) til 245 tegn (A20).
- Uten spørsmålstegn: 39 spørsmål. Liten forbokstav: 32. Bare store bokstaver: A02 og B32.
- Uten æ, ø, å: A05, B03, B04, C08, D01, E06.
- Feilstavinger og særskriving: A02, A10, A15, A19, A39, A54, B13, B21, B32, B51, B59.
- Forkortelser: A08, A21, A28, A40, A47, A49, A52, B10, B43, B49, B56, D20.
- Utsagn fulgt av spørsmål, og spørsmål på vegne av barn, partner, foreldre eller andre i følget, finnes i alle sett.
- 63 av 180 nevner en rett eller en drikk fra menyen ved navn (A 29, B 16, C 7, D 6, E 5). Resten gjør det ikke.

Sett A dekker:

- allergener: gluten og cøliaki, hvete, laktose, melkeprotein, egg, fisk, skalldyr, bløtdyr, peanøtter, nøtter, soya, selleri, sennep, sesam, sulfitt, lupin
- mindre vanlige: tomat, sitrus, hvitløk, sopp, lateks, kryssallergi mot pollen, histaminintoleranse, IBS, alfa-gal, favisme
- sykdom og medisiner: PKU, diabetes, hjertesvikt, cellegift, Antabus, MAO-hemmer
- graviditet (fire spørsmål), spedbarn, norovirus, mistanke om matforgiftning
- kjøkkenrutiner: felles kokevann, ovn, frityr og panner, spor, allergenliste, opplæring, beskjed til kjøkkenet

Sett D bruker symptomer, følger (legevakt, sykehus), det lege eller jordmor har sagt, medisin ved merkenavn,
omskrevet graviditet og ingredienser ved navn. Sett E bruker blant annet «allergisk» som bilde, «trygt» og «safe» om andre ting enn mat,
«nøtteskall», «spor av», «fare for», «livsfarlig god», «gift» som i å gifte seg, «free» som gratis og «Glutenfri» som del av et produktnavn.

### Tegn som er laget for å lure en maskin

Fem spørsmål, som er grensen oppgaven setter. I JSON-kilden står tegnene som `\u`-koder, så de synes når filen leses som tekst.

| Id | Tegn |
|---|---|
| A56 | usynlig mellomrom (U+200B) inni «nøtteallergiker» og «nøtter» |
| A57 | kyrilliske е, с og а (U+0435, U+0441, U+0430) i «glutenfri» og «cøliaki» |
| A58 | myk bindestrek (U+00AD) fire steder i «laktoseintolerant» |
| A59 | å skrevet som a pluss kombinerende ring (U+030A), altså ikke NFC-normalisert |
| B60 | kyrilliske о og е (U+043E, U+0435) i et spørsmål om wifi |

B59, E01 og E18 har en vanlig emoji. Det regner jeg som vanlig telefontekst, ikke som lureri.

## Hva jeg var i tvil om

Hvert punkt sier hva jeg valgte, og hva som bør flyttes hvis huset mener noe annet.

1. **Sykdom og medisiner som ikke er allergi** (A30 PKU, A31 diabetes, A45 hjertesvikt, D07 Marevan, D09 urinsyregikt, D13 diabetes, D18 magesår).
   Jeg la dem i A og D fordi gjesten oppgir sykdom eller medisin som grunn.
   Hvis huset bare mener allergi, intoleranse og mathygiene, hører disse sju i C.
2. **Mistanke om matforgiftning etter besøket** (A53). Lagt i A fordi det gjelder om maten var trygg.
   Det er en melding etter måltidet, ikke et spørsmål før det.
3. **Allergi som ikke gjelder en ingrediens** (A43 latekshansker i A, C11 hundeallergi i C).
   Skillet jeg brukte: lateks fra hansker kan havne i maten, det kan ikke hunden.
4. **Trygg mat generelt** (A40 norovirus i A, C17 ferske østers og C20 smilefjes i C).
   Jeg la spørsmålet i A når gjesten nevner en sykdomsrisiko, ellers i C.
5. **Spedbarn og småbarn** (A52 honning til en baby på ni måneder i A, C12 mat til en toåring i C).
   A52 gjelder en kjent helsefare, C12 gjør ikke det.
6. **«Fri for»-varer og ingredienser uten oppgitt grunn** (C06, C07, C09, C13, C14, C15, C19).
   Lagt i C slik oppgaven sier. Et strengt hus vil kanskje ha alle disse sendt til personalet.
7. **Ingrediens med oppgitt smaksgrunn** (B39 ikke glad i fisk, B41 uten oliven fordi gjesten ikke liker det).
   Lagt i B fordi grunnen sies og ikke er helse.
8. **Matord uten helse i B** (B19, B22–B27, B46: østers, ost, fisk, egg, mandler, pistasj).
   Lagt i B slik oppgaven ber om, og ikke i E, fordi ordene brukes i sin vanlige mening.
9. **Produktnavn med «Glutenfri»** (E02 spør om prisen på Peroni Glutenfri).
   Lagt i E fordi spørsmålet gjelder pris. Vil huset at alt som nevner glutenfritt skal til personalet, hører det i C.
10. **Helse nevnt, men spørsmålet gjelder noe annet** (E06 avbestilling ved sykdom, E10 feiring etter kreftbehandling,
    E15 gravid som spør om stoler, E16 leger på allergologikongress). Lagt i E. E10 og E15 er de jeg er minst sikker på.
11. **«Tåler ikke» om sterk mat** (C05). Lagt i C, men ordlyden er den samme som i allergispørsmål.
12. **Sett D kan være lettere enn tenkt.** Jeg har holdt de vanlige ordene ute
    (allergi, intoleranse, cøliaki, gluten, laktose, gravid, trygg, pasteurisert og tilsvarende på de andre språkene).
    Ord som adrenalinpenn (D20), dairy (D15) og navn på enkeltingredienser kan en ordliste likevel kjenne.
    Jeg vet ikke hva mekanismen ser etter.
13. **Dialekt og fremmedspråk** er skrevet uten morsmålskontroll.
    Dialektene er skrevet slik folk taster dem, og det finnes ingen rettskriving å måle dem mot.
14. **A59** har jeg regnet som ett av de fem spørsmålene med luretegn, selv om slik tekst også oppstår av seg selv på enkelte maskiner.
15. **Snarveiene på siden.** Oppgaven forbyr bare eksempelet i spørrefeltet.
    Jeg har i tillegg holdt meg unna de tre snarveispørsmålene på siden, siden de trolig er kjent for mekanismen.

## Hva jeg har lest

Jeg har lest tre filer og ingen andre: `OPPGAVE-B2.md`, `inn/menyen.json` og `inn/index.html` (stiene er relative til mappen `blind2`).
Jeg har ikke listet eller søkt i mapper, ikke brukt nett, ikke brukt verktøy mot andre maskiner og ikke brukt underagenter.
Til kontrollen har python3 lest tilbake de fem JSON-filene jeg selv skrev i `ut/`.

## Kontroll

Kontrollert med python3 etter siste endring:

- alle fem filene er gyldig JSON og er lister
- antall 60, 60, 20, 20, 20
- 180 unike id-er i riktig rekkefølge (A01–A60, B01–B60, C01–C20, D01–D20, E01–E20)
- 180 ulike tekster, og ingen to tekster ligner mer enn 0,54 på hverandre målt med difflib
- hvert element har nøyaktig `id`, `tekst`, `slag`, `hvorfor`; `slag` har to til fem ord, `hvorfor` er én setning
- eksempelet i spørrefeltet og de tre snarveiene på siden forekommer ikke
- uvanlige tegn finnes bare i de fem spørsmålene i tabellen over, pluss tre emoji
- sett D inneholder ingen av de vanlige ordene som er nevnt i punkt 12
