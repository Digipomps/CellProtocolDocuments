# Release-note 2026-10-30 — HAVEN-vinkling i tre nivåer (PR #37)

Endrede filer (alt annet skal være byte-identisk med kjørende release):
- `index.html`, `om/index.html`, `rettelser/index.html`, `artikler/status-i-dag/index.html`
- `assets/site.css` (forsiden og de nye sidene henter `site.css?v=20261030a`; eldre sider bruker eldre versjonsparameter, men samme fil)
- `sitemap.xml`

Nye filer:
- `forklart/index.html`, `forklart/status/index.html`, `forklart/forskning/index.html`

## Bakgrunn
Kjetil ba 30. oktober 2026 om en generell HAVEN-vinkling i stedet for Arendalsuka-vinklingen. Innholdet på nivå 2 og 3 bygger på forklaringen til masterstudentene (MasterHAVEN26). Kjetil godkjente samme dag. Rettelsesloggen har en post datert 30. oktober 2026.

## Lokalt før release
- `python3 tools/verify_app_entry.py` → OK (heroen er uendret).
- `python3 -m unittest tests/test_verify_app_entry.py` → grønt.
- `grep -rl Arendalsuka --include='*.html' .` → ingen treff.

## På serveren (89.167.90.101), i denne rekkefølgen
1. Finn kjørende release: `readlink /var/www/haven-public-new`.
2. Ny release som kopi av kjørende: `cp -a /var/www/haven-public-new-releases/<kjørende> /var/www/haven-public-new-releases/<UTC-stempel>`, bytt ut de endrede filene og legg til `forklart/`.
3. `diff -rq` mot forrige release skal bare vise filene over.
4. `sha256sum` på filene, lokalt og utrullet, skal være like. Før dem inn i `DEPLOYMENT_STATUS.md`.
5. Pek symlinken `/var/www/haven-public-new` på ny release; `nginx -t && systemctl reload nginx`.
6. Verifiser:
   - `curl -s https://digipomps.org/ | grep -c 'Hva om dataene dine ble hos deg?'` → minst 1
   - `curl -s https://digipomps.org/ | grep -c Arendalsuka` → 0
   - `curl -s -o /dev/null -w '%{http_code}' https://digipomps.org/forklart/` → 200, samme for `/forklart/status/` og `/forklart/forskning/`
7. `python3 tools/verify_app_entry.py` skal fortsatt si OK.

Tilbakerulling: pek symlinken tilbake på forrige release og last nginx på nytt.
