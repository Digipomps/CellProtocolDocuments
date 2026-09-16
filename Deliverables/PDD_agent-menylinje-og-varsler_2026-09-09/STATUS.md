# STATUS — agent menylinje og varsler

- surfaces: gui,binding,xcode
- tags: menylinje,varsler,agent,macos,challenge,tilgang,topup

## Porter
- G1: godkjent 2026-09-10 (Kjetil: «Bare få ut G1, G1-GUI og G3»)
- G1-GUI: godkjent 2026-09-10 (referansebildene i images/ — menu-ok, menu-attention, menu-down, admin-window, notification)
- G2: godkjent 2026-09-10 (implisitt — arbeidet var bestilt utført)
- G3: godkjent 2026-09-10, med forbehold Kjetil selv satte: «sjekk at ting virker før du får det inn i main»

Sett en port til `godkjent <dato>` kun når Kjetil har sagt det. `purpose_dev.py validate <mappe>` nekter porter uten artefakter.

## Planbytter (dato — hvorfor)
-

## Logg
- 2026-09-09: opprettet
- 2026-09-09 kveld: P0+P1 skrevet. Auditen fanget to feil i min egen forståelse før noe ble bygget: jobbkøen (`awaitingApproval`) finnes bare som usporede filer i det delte treet, ikke på `main`, og verken menylinje- eller varselkode fantes fra før. Fire referansebilder rendret til `images/` (tegnede, ikke skjermbilder). PLAN.md skrevet med WP0–WP9.
- 2026-09-09 natt: **WP0-baseline avdekket at `main` ikke bygger.** 79 kompileringsfeil mot pinnede avhengigheter; to feil igjen i utviklingsmodus, begge fordi HEAD-commiten landet kode som kaller `AgentIdentityStore.loadExisting()` — en funksjon som bare finnes ucommittet i det delte treet. Baselinen er derfor målt på `main` + den ene filen, tatt inn som egen forutsetnings-commit. Målt baseline: 165 tester, 1–2 røde (ustabile).
- 2026-09-10: **WP1–WP7 implementert og verifisert.** Challenge-kontrakt med fixtures, `ChallengeInboxService`, tre nye endepunkt på kontrollbroen, `HavenAgentMenuCore` og menylinjeappen med adminvindu og varsler. Ende-til-ende bekreftet mot en faktisk kjørende agent over HTTP. Sju commits på grenen. **212 tester, ingen feil** (165 → 212, 47 nye).
- 2026-09-10: **Kodegjennomgangen fant åtte mangler**, hvorav «`start()` kalles aldri» alene ville gjort demoen død. Alle rettet med hver sin test. Skjematekst presisert der den var strengere enn koden.
- 2026-09-10: **Gjenstår før G3:** bilde av den kjørende menyen og et faktisk varsel i varslingslisten (skjermen sov; krever at Kjetil logger inn og gir varselsamtykke). Appen kjører på maskinen hans. Den kjørende agenten på 43110 er forrige binær uten `/challenges` og må startes på nytt for ekte data. G1, G1-GUI og G3 venter alle på Kjetil.
- 2026-09-10 03:00: **Ni commits, 224 tester, null nye feil.** Tre runder kodegjennomgang fant til sammen tjue reelle feil i kode som bygde grønt — inkludert to som ville gjort appen ubrukelig (`start()` ble aldri kalt; samlevarsel ville gjentatt seg hvert 20. sekund). Alle rettet, med tester. Appen kjører på Kjetils maskin med siste bygg. Fem nye lærdommer lagt i registeret. Gjenstår for G3: bilde av kjørende meny og et faktisk varsel — begge krever våken skjerm og Kjetils samtykke.

- 2026-09-11: **Retraksjon og retting.** Påstanden «main bygger ikke» var feil. Den handlet om `ba14895`, en commit som bare lå på den lokale main-grenen og aldri var pushet, og som avhang av CellBase-kode som heller ikke var pushet. `origin/main` var fire commits lenger fram og grønn hele tiden — verifisert med ren klone fra GitHub: bygg grønt, 179 tester, én ustabil rød fra før. Mitt svar på den røde baselinen — `swift package edit` mot lokale utsjekk — gjorde at alt bygde på én maskin og ble meldt som verifisert. Det er rettet: de ni menylinje-commitene er spilt av på origin/main uten konflikter, forutsetnings-commiten er droppet, og tre sjekker er lagt inn som gjør feilen synlig med én gang (`Scripts/preflight_before_landing.sh`, `Scripts/assert_dependencies_are_on_their_main.sh`, samme sjekk i CI). Reglene står i `HavenAgentD::Docs/Bygg_og_landing.md`.
- 2026-09-10: **Portene gitt av Kjetil.** G1, G1-GUI og G3, med hans eget forbehold om at ting skal være verifisert før det lander i main.
