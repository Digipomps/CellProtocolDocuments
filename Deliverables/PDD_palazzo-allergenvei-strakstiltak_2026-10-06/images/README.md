Referansebilder: `<flate>-<tilstand>-v<n>.png`. Bare bilder Kjetil har godkjent i FORMAALSSPEC.md §3 teller.

## RENDERINGSERKLÆRING

Bildene er ikke skjermbilder fra nett, og de er ikke rendret fra et skjelett. Siden er HTML, så det finnes ikke noe skjelett å rendre. Stier er relative til HAVEN-roten. Slik er bildene laget:

- Siden er rendret i Chromium (Playwright) med sidens egne filer fra `PalazzoScaffold/Public` på `a3fc5042`: `PalazzoScaffold/Public/palazzo/index.html` (md5 `f285fcf46925c89c0b81920bf7733297`), `PalazzoScaffold/Public/js/palazzo-communale.js` (md5 `0e929f12959bc122e82c6ed66c6b7beb`), `PalazzoScaffold/Public/css/palazzo-communale.css` (md5 `63284bdc9f370ff05786749f0388be4b`), og skriftene og bildene under `PalazzoScaffold/Public/css/themes/palazzo/`.
- Tjenesten er byttet ut med faste svar. `POST /palazzo/api/ask`, `POST /palazzo/api/menu` og `POST /palazzo/api/beverages` gir ett svar fra en fil. `GET /palazzo/api/state` gir en fast tjenestestatus som er satt sammen etter koden, ikke hentet fra nett.
- Svarene merket «I dag» er hentet fra nett 6. oktober 2026, felt for felt: kl. 06:27 UTC `HAVEN-Deploy/_handoff/HD-0077/maal/KONVOLUTTER-20261006.md`, svar 2 («Er det hvete i Carpaccio di polpo?») og svar 4 («Hva er Carpaccio di polpo?»), kl. 08:23 UTC `HAVEN-Deploy/_handoff/HD-0077/maal/KONVOLUTTER-2-20261006.md`, kall 12 («Er det mandler i Orata al forno a legna?»), og kl. 09:16 UTC `HAVEN-Deploy/_handoff/HD-0077/maal/KONVOLUTTER-4-20261006.md`, kall 1 («Hva bør jeg bestille når jeg ikke kan spise mandler?»).
- Svarene merket «Etter», «A» og «B» finnes ikke i koden ennå. Henvisningen (ordlyd A) er satt sammen for hånd etter `PalazzoCommunaleProjection.blocked`, uten kilder. Ordlyd B er et forslag til ny tekst, med én linje under. Svarene med linjen om allergener er det målte svaret (kall 1, 3 og 12 i `HAVEN-Deploy/_handoff/HD-0077/maal/KONVOLUTTER-2-20261006.md`, kall 1 i `HAVEN-Deploy/_handoff/HD-0077/maal/KONVOLUTTER-4-20261006.md`, og svar 4 i `HAVEN-Deploy/_handoff/HD-0077/maal/KONVOLUTTER-20261006.md`) med én ny linje lagt først blant advarslene. Ingenting annet i svaret er endret.
- Drikkelisten er hentet fram slik en gjest gjør det, ved å trykke sidens egen snarvei «Hva kan jeg drikke?». De andre spørsmålene er skrevet i spørrefeltet og sendt med Enter.
- For tillegget er attributtet `placeholder` i `PalazzoScaffold/Public/palazzo/index.html` byttet mens siden ble rendret. Fila er ikke endret.
- Bildene viser kortet med spørrefeltet og svaret, ikke hele siden. Bredden er 1280 punkter, og 390 for telefonbildet. Den gule rammen rundt svaret er fokusmarkeringen siden setter når spørsmålet er sendt med tastaturet. Den vises ikke når snarveien er trykket med musen.
- Overskriftene og tekstene over hvert bilde («I dag», «Etter», «A», «B») er lagt på etterpå og er ikke en del av siden.
- Verktøyene og svarene bildene er laget av, ligger i `HAVEN-Deploy/_handoff/HD-0077/maal/grunnlag-20261006/render/`: `render.py` (rendrer ett svar), `sett_sammen.py` (setter to bilder ved siden av hverandre), `lag_bilder.sh` (kommandoene med overskriftene og tekstene, ordrett), og én JSON-fil per svar. `render-v1.py` og `sett_sammen-v1.py` er utgavene de første bildene ble laget med. Alt er kjørt i Losens skyarbeidsområde, og stiene inne i `render.py` viser dit.

| Bilde | Venstre | Høyre |
|---|---|---|
| `concierge-allergi-foer-etter-v3.png` | `idag-hvete.json` (målt) | `etter-henvisning.json` (ordlyd A, avvisningen som står på nett i dag, uten kilder) |
| `concierge-allergi-henvisning-mobil-v2.png` | `etter-henvisning.json` (ordlyd A), bredde 390 | – |
| `concierge-allergi-ordlyd-v5.png` | `etter-henvisning.json` (ordlyd A) | `etter-egen-setning-v2.json` (ordlyd B) |
| `concierge-linje-om-allergener-v2.png` | `idag-rett.json` (målt) | `etter-rett-med-linje.json` (målt svar med linjen for én rett) |
| `concierge-linje-to-retter-v1.png` | `idag-to-retter.json` (målt) | `etter-to-retter-med-linje.json` (målt svar med linjen for flere retter) |
| `concierge-linje-under-lister-v1.png` | `etter-pizzaliste-med-linje.json` (målt svar med linjen) | `etter-drikkeliste-snarvei-med-linje.json` (målt svar fra snarveien, med linjen) |
| `concierge-linje-bordbestilling-v1.png` | `idag-bordbestilling.json` (målt) | `etter-bordbestilling-med-linje.json` (målt svar med linjen) |
| `concierge-eksempel-v2.png` | `idag-eksempel.json` (siden som den er) | `etter-eksempel.json` (nytt eksempel) |

Bildene som ikke gjelder lenger, ligger i `erstattet/`: de tre første i utgave 1 (viste ordlyd B som anbefalt), `concierge-allergi-foer-etter-v2.png`, `concierge-allergi-ordlyd-v2.png`, `concierge-allergi-ordlyd-v3.png` og `concierge-allergi-ordlyd-v4.png` (tekstene over bildene er rettet i senere utgaver; utgave 3 av ordlydbildet sa «huset har kontrollert merkingen», som sier mer enn kilden, og utgave 4 sa «Ingen ny tekst» uten å si at det gjelder henvisningen), og `concierge-linje-om-allergener-v1.png` og `concierge-eksempel-v1.png` (overskriftene kalte linjen «Tillegg 1» og eksempelet «Tillegg 2»; linjen er en del av tiltaket, og eksempelet er det eneste tillegget).
