# Release-note 2026-10-22 — undertekst til essensen på tre sider

Endrede filer (alt annet skal være byte-identisk med kjørende release):
- `index.html` (seksjonen `#mennesket-og-fellesskapet`: eyebrow «Mennesket først – ikke mennesket alene», overskrift «Din grense, båret av fellesskapet.», gammel overskrift flyttet til første setning i ingressen; hero uendret)
- `artikler/index.html` (kortet «Mennesket først betyr ikke mennesket alene»: ingressen begynner med «Din grense, båret av fellesskapet:»)
- `artikler/mennesket-forst/index.html` (ingressen begynner med «Din grense, båret av fellesskapet:»; `og:description` er underteksten; «Sist faglig gjennomgått 22. oktober 2026»)

## Bakgrunn
Brand key-arbeidet 20.–22. oktober 2026 beholdt essensen «Mennesket først – ikke mennesket alene» og fant at andre ledd trenger en forklarende linje der det brukes. Kjetil godkjente 22. oktober «Din grense, båret av fellesskapet» som den linjen og ba om at den kommer ut på infosidene. Påstandsklasse: normativt prinsipp, ingen effektpåstand (jf. claim-kanonen). Ingen påstand trekkes, så rettelsesloggen får ingen post.

## Lokalt før release
- `python3 tools/verify_app_entry.py` → OK (hero er uendret).
- `python3 -m unittest tests/test_verify_app_entry.py` → 8 tester grønne.
- `grep -rln 'Din grense, båret av fellesskapet' --include='*.html' .` → nøyaktig de tre filene over.

## På serveren (89.167.90.101), i denne rekkefølgen
1. Finn kjørende release: `readlink /var/www/haven-public-new`.
2. Ny release som kopi av kjørende: `cp -a /var/www/haven-public-new-releases/<kjørende> /var/www/haven-public-new-releases/<UTC-stempel>` og bytt ut nøyaktig de tre filene over.
3. `diff -rq` mot forrige release skal bare vise de tre.
4. `sha256sum` på de tre, lokalt og utrullet, skal være like — før inn i `DEPLOYMENT_STATUS.md`.
5. Pek symlinken `/var/www/haven-public-new` på ny release; `nginx -t && systemctl reload nginx`.
6. Verifiser: `curl -s https://digipomps.org/ | grep -c 'Din grense, båret av fellesskapet'` → 1; samme for `/artikler/` → 1 og `/artikler/mennesket-forst/` → 2 (ingress og og:description). `/artikler/mennesket-forst/` viser «Sist faglig gjennomgått 22. oktober 2026».
7. `python3 tools/verify_app_entry.py` skal fortsatt si OK.
8. Gi beskjed i tråden «Brand key model for HAVEN», så tas G3-skjermbildene av produksjonssidene og legges i `Deliverables/PDD_undertekst-infosider_2026-10-22/ACCEPT.md`.
