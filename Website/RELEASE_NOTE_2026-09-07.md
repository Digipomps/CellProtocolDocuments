# Release-note 2026-09-07 — /tjenester/ tatt ned, ny artikkel nb + en

Endrede/nye filer (alt annet skal være byte-identisk med kjørende release `20260809T083528Z`):
- `artikler/fra-2019-skissen-til-i-dag/index.html` (ny)
- `en/artikler/from-the-2019-sketch-to-today/index.html` (ny — første side på engelsk; hreflang begge veier)
- `artikler/index.html` (nytt kort øverst, teller 19 → 20)
- `rettelser/index.html` (ny innførsel 7. september 2026, øverst)
- `sitemap.xml` (to nye url-er)

## Funn som utløste dette
`https://digipomps.org/tjenester/` serverte 7. september 2026 fortsatt 2019-teksten fra WordPress
(«global digital plattform», «maksimerer verdi», «løser svakhetene …»). Den sporede
`nginx-digipomps.conf` har `location = /tjenester/ { return 301 /; }` (linje 19), men
produksjonsverifikasjonene 1. og 9. august lister ikke `/tjenester/` blant testede redirects.
**Enten er den aktive `haven_public.conf` eldre enn den sporede fila, eller så svarer noe annet på
den stien.** Dette må sjekkes på serveren før release.

## På serveren (89.167.90.101), i denne rekkefølgen
1. `curl -sI https://digipomps.org/tjenester/ | head -5` — forventet `301` → `/`. Får du `200` med
   WordPress-innhold: `diff /etc/nginx/sites-enabled/haven_public.conf <sporet nginx-digipomps.conf>`
   og `grep -rn tjenester /etc/nginx/sites-enabled/`.
2. Ny release som kopi av kjørende: `cp -a /var/www/haven-public-new-releases/20260809T083528Z
   /var/www/haven-public-new-releases/<UTC-stempel>` og bytt ut nøyaktig de fem filene over.
3. `diff -rq` mot forrige release skal bare vise de fem.
4. `sha256sum` på de fem, lokalt og utrullet, skal være like — før inn i `DEPLOYMENT_STATUS.md`.
5. Pek symlinken `/var/www/haven-public-new` på ny release; `nginx -t && systemctl reload nginx`.
6. Verifiser: `/tjenester/` → 301; `/artikler/fra-2019-skissen-til-i-dag/` → 200;
   `/en/artikler/from-the-2019-sketch-to-today/` → 200 med `lang="en"`; `/artikler/` viser 20;
   `/rettelser/` har 7. september øverst; `/sitemap.xml` har begge nye.
7. `python3 tools/verify_app_entry.py` skal fortsatt si OK (kjørt lokalt 7. september: OK).

## Ikke gjort
- Nettleser-/a11y-smoke (`tests/app_entry_browser_smoke.js`) er ikke kjørt mot de nye sidene.
- `/en/` er én side, ikke en engelsk utgave av nettstedet; menyen på den engelske siden peker til norske sider (merket med `hreflang="nb"`). Full lokalisering: se
  `Kallimachos/Verdifordeling/Sachs_2026-09-07/Nettside/LOKALISERING_Vurdering_2026-09-07.md`.
- Ordet «må» om de fire reglene er unngått (rettelsesloggen 5. august avviste «må følge» som håndhevelsespåstand): sidene sier «er laget for å» / «is designed to».
