# Regler for skrivetrådene (7. oktober 2026)

Du skriver setninger slik en gjest ville skrevet dem til conciergen på nettsiden til en restaurant. Du er én av flere skribenter, hver med sin stemme. Setningene brukes til å måle hvor godt en tolk forstår gjester. Det finnes ikke noe «riktig» å skrive: skriv naturlig, ikke for å treffe noe.

## Tilgang

Les BARE disse tre filene: denne regelfilen, oppgaven din, og menyen (`/home/claude/dag/gen2-inn/menyen-for-gjester.json`). Les ingenting annet under `/home/claude` eller `/mnt`, og søk ikke etter andre filer. Bruk ikke nettet. Du trenger bare Read, Write og Bash (bare for `date -u`).

## Det du leverer

Én fil med nøyaktig 50 linjer (JSON Lines), én setning per linje, skrevet med Write til stien oppgaven din navngir:

`{"nr": 1, "tekst": "<setningen slik gjesten skriver den>", "formaal": "<ett av ordene under>", "mening": "<hva gjesten mener, med dine egne ord, én kort setning>"}`

`formaal` er ett av:

- `spise`: gjesten vil ha noe å spise (et ønske, lyst på noe, «noe med …», ber om forslag til mat)
- `drikke`: gjesten vil ha noe å drikke
- `vite`: gjesten vil vite noe om huset, en rett eller en drikk («hva er …», «fortell om …», «har dere …»)
- `unngaa`: gjesten sier at det er noe hun ikke tåler, er allergisk mot eller ikke spiser, eller vil ha mat uten noe
- `bord`: bestille bord
- `aapningstid`: åpningstider
- `selv`: gjesten forteller bare noe om seg selv, hva hun liker eller ikke liker, uten å be om noe («jeg er veldig glad i sitron», «ost er ikke helt min greie»)
- `ingen`: småprat, noe som ikke har med restauranten å gjøre, eller noe som ikke lar seg forstå

Fordeling, omtrent: 12 `spise`, 6 `drikke`, 8 `vite`, 8 `selv`, 7 `unngaa`, 3 `bord`, 2 `aapningstid`, 4 `ingen`. Oppgaven din kan si noe annet.

## Krav til setningene

- Skriv som personen i oppgaven din ville skrevet. Varier lengde og form. Noen setninger skal ha to ting i seg («… men ikke …», «… og så …»).
- Bruk egne ord for mat og drikke, slik folk gjør, ikke bare ordene på menyen. Det er helt i orden å be om noe huset ikke har.
- Minst 6 setninger skal ha en nektelse («ikke», «uten», «aldri», «ingen»).
- Ingen setning er lik en annen, og ingen er en ren avskrift av en linje på menyen.
- Ikke skriv noe som er ment å lure en tolk. Dette er vanlige gjester.
- Ingen navn på virkelige personer, ingen telefonnumre og ingen e-postadresser.

## Tid

TIDEN ER HARD: 6 minutter. Kjør `date -u` når du starter og før du leverer. Skriv hele filen i ett Write-kall, og lever selv om du ikke er fornøyd. Svaret ditt til meg er kort: stien til filen, antall linjer, og start- og sluttid (UTC).
