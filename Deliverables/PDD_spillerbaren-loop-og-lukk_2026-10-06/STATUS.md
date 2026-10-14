# STATUS — rettelse: spilleren og overskriften

2026-10-06 · funnet mens bildene til album og rekkefølge ble laget

Ingen formålsspec: dette er en rettelse, ikke ny funksjon.

## Feilen
Loop-knappen ble lagt inn av Losen 2026-09-03 (`6fb299f44`, merget i PR #211 natt til
04.09) uten at spillerbarens rutenett fikk en kolonne til. Fire deler i tre kolonner.
Det er Losens egen feil, og Losens egne prøver som ikke fanget den.

| Hvor | Hva som skjer | Hvordan det er kjent |
|---|---|---|
| Skjerm | «Lukk» faller ned på egen rad; baren blir 140 px høy i stedet for 84 | **Sett**: målt i Chromium mot filene på `origin/main` e5c34345 |
| Telefon (390 px) | Loop og «Lukk» ligger i samme rute. Loop lar seg ikke trykke | **Sett**: nettleseren avviste klikket — «Lukk» tok imot det |
| Telefon | «Utgivelser» deles midt i ordet når «Spill alle» vises; knappeteksten går over to linjer | **Sett**: samme måling |
| I prod, på en ekte telefon | — | **Ikke sjekket** |

Bilde: `images/spiller-rettelse-foer-etter.png`.

## Hvorfor det ikke ble fanget
`playwright/butterpop-queue.spec.js` klikket bare på skjermbredde og målte ingen
plassering. En prøve som ikke kunne ha feilet på dette.

## Rettelsen (gren `fix/spillerbaren-loop-og-lukk`, av `origin/main` @ e5c34345, tupp `ec692f52`)
- `Public/css/butterpop-studio.css`: ni nye linjer, to byttet ut.
- `playwright/butterpop-queue.spec.js`: tre nye prøver som måler plasseringen på 1280
  og 390 px og klikker på ordentlig. Spec-en kjøres alt i CI.

| Hva | Hvordan det er kjent |
|---|---|
| De tre nye prøvene feiler uten rettelsen | **Sett**: 3 av 3 feiler, hver med sin melding |
| Med rettelsen | **Sett**: 7 av 7 i `queue`; `mix-tidy` og `statistics` urørt, 25 av 25 |
| Sammen med profil-lenka | **Sett**: stilarket slår seg sammen uten konflikt, 42 av 42 |
| I CI | **Ikke sjekket** — grenen er ikke pushet |

Playwright 1.55.1, Chromium, Linux, med adressen CI bruker.

## Ikke gjort
- Grenen er **ikke pushet**. Det er synlig kode, og Kjetil har ikke sett bildet.
- `?v=` på stilarket er ikke bumpet her. Profil-lenka bumper både CSS og JS, og en
  bump her ville gitt konflikt på samme linje. Går denne ut uten den, må `?v=` bumpes.
