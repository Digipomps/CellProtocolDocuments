# ACCEPT — Palazzo: se hva reaksjonen ble tolket som

## parity

Kjørt 2026-10-13 kl. 21:24Z (00:06 lokal tid) på Kjetils Mac.

- **Oppsett:** Palazzo kjørte lokalt på 127.0.0.1:8091 fra grenen `losen/wp8-palazzo-bro-20261013`. Appen var HAVEN-WP8d.app, bygget fra Binding-grenen `losen/wp8-palazzo-lokal-20261013` mot CellProtocol-grenen `losen/resolver-proof-scope-20261013`. Testidentiteten var ny (`pins-skjermbilder-20261013.json`).
- **Vei:** appen åpnet artikkelflaten over broen: Verktøy → «Palazzo artikkel (lokal)». Ingen fixture og ingen mock var med.
- **Skjermbildene** er tatt i Binding (macOS, mørkt tema). Alle trinnene ble gjort i én visning, uten å navigere ut og inn.
- **Referansen** er `../images/artikkel-tolkning-v1.png`, variant B. Den er en HTML-mockup i lyst tema.

### test.article.row-refresh: PASS (radteksten, alle fire trinn)

| Trinn | Forventet | Faktisk | Bilde |
|---|---|---|---|
| 0 | Ingen rad før første trykk | Ingen rad | `wp8-0-artikkel-aapnet.jpg` |
| 1 | «Interessant» gir én lukket rad | «▸ Registrert: Interessant · tolket som 7 emner», lukket | `wp8-1-interessant-lukket-rad.jpg` |
| 2a | Raden åpnes | Raden åpnes med 7 brikker | `wp8-2a-rad-aapnet.jpg`, `wp8-2a-rad-aapnet-zoom.jpg` |
| 2 | «Vil smake» viser «Vil smake», og raden er fortsatt åpen | «▾ Registrert: Vil smake · tolket som 7 emner», fortsatt åpen | `wp8-2-vil-smake-fortsatt-aapen.jpg` |
| 3 | «Ikke for meg» viser teksten fra avvik 2 | «Registrert: Ikke for meg · tolket som mindre interesse for 7 emner», ordrett som avvik 2 | `wp8-3-ikke-for-meg.jpg` |
| 4 | «Vil smake» igjen gir positiv tekst | «Registrert: Vil smake · tolket som 7 emner» | `wp8-4-vil-smake-igjen.jpg` |

### test.gui.parity: FAIL, med tre nye avvik som må rettes eller godkjennes

Avvikene fra FORMAALSSPEC §3 står som før:

- Avvik 1 (brikker) er rettet. Brikkene brytes over linjer slik bildet viser.
- Avvik 2 stemmer ordrett.
- Avvik 3 stemmer: raden viser siste trykk.

Nye avvik, sett i den kjørende flaten:

| # | Avvik | Bilde | Forslag |
|---|---|---|---|
| N1 | **Brikkene er uleselige i mørkt tema.** Brikken har lys bakgrunn, men teksten er hvit. I lyst tema (`native-brikker-aapen.png`) er de fine. | `wp8-2a-rad-aapnet-zoom.jpg` | Rett: brikkens tekstfarge og bakgrunn må følge samme tema (Binding-renderer). |
| N2 | **Etter «Ikke for meg» erstattes tittelen, ingressen og opphavet med «Innholdet er ikke tilgjengelig akkurat nå.»** Det kommer tilbake etter «Vil smake». Dette følger trolig av B2 (artikkelen stenges), men bildet viser artikkelen uendret. Gjesten mister teksten hun nettopp reagerte på. | `wp8-3-ikke-for-meg.jpg` | Kjetils valg: la artikkelen stå til hun navigerer bort, eller godta dette. |
| N3 | **Valgt reaksjon vises ikke som valgt.** Bildet viser «Interessant» som fylt knapp. I appen er knappene ren tekst. Et grønt hake-merke vises rett etter trykket, men forsvinner ved neste oppdatering (trinn 2a og 4). Kommentarfeltet «Vil du legge til noe med egne ord?» finnes ikke i flaten. | `wp8-1-…`, `wp8-2a-…`, `wp8-4-…` | Kjetils valg: rett, eller godta som eget arbeid utenfor denne PDD-en. |

Testsettet bruker alternativ 1, altså forhåndslagde celler og en lokal pin-fil. Det er en testoppkobling, ikke produktets oppstart.
