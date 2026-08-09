# HAVEN public website deployment status

Last updated: 2026-08-09 10:40 Europe/Oslo

## HAVEN app entry

- status: `blocked` (controlled 2026-08-03)
- no canonical production origin or installation URL for the HAVEN app is
  documented in the checked repositories
- `haven.digipomps.org`, `app.haven.digipomps.org` and `app.digipomps.org` do
  not resolve in public DNS
- the documented CellScaffold host is staging and is not a publication target
- live staging also fails the installation prerequisites checked here:
  `/install` returns 404, the manifest has empty `name` and `short_name`, and
  its 192 px, 512 px and Apple touch icons return 404
- production `digipomps.org` therefore has no app/install CTA and remains
  byte-for-byte unchanged; the review hero also remains fail-closed, with a
  test-proof entry and a link to the human-and-community explanation
- the sole future activation point is marked in `Website/index.html`; a
  read-only release guard rejects wrong maturity copy, staging/local/review
  targets, new-tab behavior and a third hero action
- local release-guard tests pass (8 cases); Chromium passes the blocked hero
  with JavaScript on and off, accessible link names, visible keyboard focus,
  200 % text and a 390 px mobile viewport without horizontal overflow
- this is not an app-availability claim and not a new production release; the
  prepared information site is deployed only to the isolated, noindex review host

## Production domain

- canonical URL: `https://digipomps.org/`
- `www`: redirects permanently to the same path and query on
  `https://digipomps.org`
- authoritative DNS:
  - `digipomps.org A 89.167.90.101`
  - `www.digipomps.org CNAME digipomps.org`
- active Nginx site: `/etc/nginx/sites-enabled/haven_public.conf`
- tracked source config: `Website/nginx-digipomps.conf`
- docroot symlink: `/var/www/haven-public-new`
- release: `/var/www/haven-public-new-releases/20260809T083528Z`
  (ny artikkel «Hvor kontrollen slutter» med oppdatert artikkeloversikt og
  sitemap; bygget som en kopi av `20260807T132725Z` med bare de tre filene
  endret. Tidligere releaser `20260807T132725Z`, `20260806T124500Z` og
  `20260804T051327Z` beholdt for tilbakerulling)

### Production verification 2026-08-09

Releasen ble laget ved å kopiere den kjørende produksjonsreleasen og bytte
ut nøyaktig tre filer. Alt annet er byte-identisk med det som allerede lå ute,
inkludert forsiden.

- endringen mot forrige release, kontrollert med `diff -rq`: bare
  `artikler/hvor-kontrollen-slutter/` (ny), `artikler/index.html` og
  `sitemap.xml`
- lokale og utrullede sjekksummer er like:
  - `artikler/hvor-kontrollen-slutter/index.html`:
    `944e05ab27fd366365c5dff141936b7e939018c9b2c09cfa618adef9aa5c82e7`
  - `artikler/index.html`:
    `0d9d40a2f1ba0dba36434128deb2bdff1c6d7c2b5ce88932550beadc4342ee05`
  - `sitemap.xml`:
    `93dd200bd109120e9415d6645a54cbe02aa5e3337393922ba966601209ce3169`
- forsiden er uendret før og etter byttet:
  `a2442fbf54573288f9294009861773fd5e256779577e5a0d05339e37f6237d84`
- releasen ble verifisert isolert over loopback før symlenken ble byttet:
  alle nøkkelsider 200, ukjent sti 404, `19 artikler` i oversikten og artikkelen
  i sitemap
- `nginx -t`: bestått; Nginx aktiv etter reload
- live HTTPS 200 for `/`, `/artikler/`, `/artikler/hvor-kontrollen-slutter/`,
  `/artikler/haven-og-standardene/`, `/bevis/tilgangskontroll/`, `/kilder/`,
  `/om/`, `/personvern/`, `/rettelser/` og `/sitemap.xml`; ukjent sti 404
- `www` og `http` gir fortsatt 301 til apex
- artikkelen beholder CSP, ettårs HSTS og nosniff, og sender ingen
  `X-Robots-Tag`
- `app_entry_browser_smoke.js` bestått mot live `https://digipomps.org`
- lokalt før utrulling: `verify_app_entry.py` bestått, app-entry-unittester 8/8,
  TextReliability `rhetorical_pressure: low`, og lokal nettleserkontroll på
  desktop og 375 px uten horisontal overflow

Merknad: produksjon sto på `20260807T132725Z` da dette arbeidet startet. Den
releasen (hero-film `haven-hero-film-20260807`) var ikke ført opp her, og
kildefilene for den ligger fortsatt ukommittert i arbeidstreet. Det er ikke
rørt; den nye releasen viderefører den uendret.

### Tidligere produksjonsrelease (20260806T124500Z)

Persona-historie, ny seksjonsrekkefølge, film øverst i problemseksjonen,
navngitt styre og finansieringslinje; promotert fra den verifiserte
review-releasen 2026-08-06.

### Production verification 2026-08-06

Produksjon er en byte-identisk kopi av review-release `20260806T124500Z`.

- `index.html` sjekksum, lokalt, på review, på produksjon og live:
  `17387fd5090a2aeba101aa5f409f41bf968389f044faf20ef8fbc93d2b545e3f`
- `nginx -t`: bestått
- HTTPS 200 for `/`, `/om/`, `/rettelser/`, `/artikler/`,
  `/artikler/verktoy-som-samarbeider/`, `/kilder/`,
  `/bevis/tilgangskontroll/`, `/personvern/` og filmen; ukjent sti 404
- `www` og `http` gir 301 til apex; `/cellprotocol-explained/` gir 301 til
  `/artikler/hva-er-en-cell/`
- filmen svarer HTTP 206 på Range-forespørsler, så spoling virker
- produksjon beholder CSP og ettårs HSTS, sender ingen `X-Robots-Tag`
- `app_entry_browser_smoke.js` bestått mot live `https://digipomps.org`

### Tidligere produksjonsrelease (20260804T051327Z)

### Production verification 2026-08-04

The concern-first variant was promoted to production after passing on the
review host. The production release is a byte-identical copy of review release
`20260804T051327Z`.

- production `index.html` checksum, local and live:
  `593fb0bdd6ba56b3eba3ce54d92798e27bfee6642ff1a668e9c0790b9a4fcc90`
- `nginx -t`: passed
- HTTPS 200 for `/`, `/artikler/`, `/artikler/verktoy-som-samarbeider/`,
  `/kilder/`, `/bevis/tilgangskontroll/`, `/om/`, `/personvern/` and
  `/rettelser/`; unknown path returns 404; `/sitemap.xml` returns 200
- `https://www.digipomps.org/` and `http://digipomps.org/` both return 301 to
  `https://digipomps.org/`
- legacy WordPress redirects verified: `/cellprotocol-explained/` and
  `/en/cellprotocol-explained/` → `/artikler/hva-er-en-cell/`, `/om-oss/` → `/om/`
- production retains CSP and one-year HSTS, emits no `X-Robots-Tag`, and
  `robots.txt` still allows crawling
- `app_entry_browser_smoke.js` passed against live `https://digipomps.org`:
  blocked app entry, copy order, sources, images, JS on/off, accessible link
  names, keyboard focus, 200 % text and 390 px mobile layout

### Earlier production verification (release 20260801T095935Z)

- ordinary TLS verification succeeds for both production names
- certificate:
  - subject: `digipomps.org`
  - SANs: `digipomps.org`, `www.digipomps.org`
  - issuer: Let's Encrypt `YE2`
  - valid from 2026-07-17 14:13:56 UTC
  - valid until 2026-10-15 14:13:55 UTC
- Certbot renewal dry-run for `digipomps.org`: passed
- HTTPS responses:
  - `/`: HTTP 200 with the exact deployed HAVEN `index.html`
  - `/artikler/`: HTTP 200 with 16 individually addressable articles
  - `/artikler/agent-pa-dine-vegne/`: HTTP 200
  - `/artikler/haven-og-standardene/`: HTTP 200
  - `/bevis/tilgangskontroll/`: HTTP 200 with pinned component proof
  - `/kilder/`: HTTP 200
  - `/om/`, `/personvern/` and `/rettelser/`: HTTP 200
  - unknown path: HTTP 404 with the custom HAVEN 404 page
- HTTP redirects permanently to the corresponding HTTPS apex URL
- HTTPS `www` redirects permanently to the corresponding apex URL
- legacy WordPress paths redirect to their closest current page; the Cell,
  purpose and organization paths now use the articles' and organization page's
  own URLs
- production headers include CSP, Permissions Policy, one-year HSTS, nosniff
  and frame denial
- production does not emit `X-Robots-Tag`; `robots.txt` allows crawling
- desktop and mobile browser passes show the HAVEN page, logo and illustration
  without horizontal overflow
- the production mobile menu opens and closes with the correct accessibility
  state
- no browser warnings or errors were observed on the production page
- the live article filter changes the visible count from 16 to 9 for
  `Vis konkret`
- the old `/artikler/#mennesket-forst` campaign link is upgraded by the client
  to `/artikler/mennesket-forst/`
- active Nginx configuration was backed up as
  `/etc/nginx/sites-available/haven_public.conf.backup-20260801T1001Z`
- `nginx -t` reports an existing `protocol options redefined` warning for
  `rag_proxy.conf`; syntax testing still passes and Nginx is active

During the DNS cutover, one browser initially displayed its still-fresh cached
WordPress response for the bare URL. A normal reload fetched the HAVEN page;
unique and direct HTTPS requests had already returned the new release. Existing
visitors with an old browser cache may therefore need one reload during the
cutover window.

## Review host

- VPS: `89.167.90.101`
- web server: Nginx 1.24.0
- release: `/var/www/haven-public-review-releases/20260806T120500Z`
  (som `20260806T113801Z`, men filmen går ikke i sløyfe og stopper på siste
  bilde, Arendalsuka-datoene 10.–14. august 2026 er oppgitt på forsiden og
  `/om/`, og finansieringslinjen «ingen ekstern finansiering, egeninnsats» er
  publisert sammen med en oppfordring om deltakelse, praktisk hjelp, sponsing
  eller interesse. Verifisert live 2026-08-06: browser-smoke grønn, video 200
  med 2,0 MB, produksjon uendret)
- forrige release: `/var/www/haven-public-review-releases/20260806T113801Z`
  (persona-historien «Marte skal bestille en time», ny rekkefølge på tolv
  seksjoner, egen «Forskningsspor»-seksjon, de fem spørsmålene, navngitt styre
  på `/om/`, generelt kontaktpunkt `digipomp@digipomps.org`, og filmen
  `haven-hva-sa-du-ja-til-20260806.mp4` med plakat i problemseksjonen.
  Verifisert 2026-08-06: alle nøkkelsider 200, ukjent sti 404, video svarer
  `video/mp4` 2,0 MB med HTTP 206 på Range, produksjon uendret på
  `20260804T051327Z`, og browser-smoken passerer mot live review-host.
  Forrige review-release beholdt for tilbakerulling)
- forrige release: `/var/www/haven-public-review-releases/20260804T051327Z`
  (concern-first forside, 18 artikler inkl. `verktoy-som-samarbeider`,
  kildetabell `#forside-statistikk`; hero-kildesetningen forenklet til
  «Kilde: Datatilsynets personvernundersøkelse 2024.» — lenke i heroen er
  utelukket fordi release-guarden teller alle lenker i `section.hero`;
  tidligere releaser `20260804T044212Z` og `20260803T162639Z` beholdt
  for tilbakerulling)
- active docroot symlink: `/var/www/haven-public-review`
- active Nginx site: `/etc/nginx/sites-enabled/haven_public_new.conf`
- tracked source config: `Website/nginx-new-haven.conf`

The release was uploaded as an isolated static bundle. Files are owned by
`root:root`; directories are mode `0755` and files are mode `0644`.

## Verified

- `nginx -t`: passed
- Nginx service after reload: active
- review and production now have separate docroot symlinks; production remains
  `/var/www/haven-public-new-releases/20260801T095935Z`
- `Host: new.haven.digipomps.org` against VPS loopback:
  - `/`: HTTP 200
  - `/artikler/`: HTTP 200 with expected HAVEN article content
  - unknown path: HTTP 404
- review-host headers include CSP, Permissions Policy, one-year HSTS, nosniff,
  frame denial and `X-Robots-Tag: noindex, nofollow, noarchive`
- both GoDaddy authoritative nameservers return:
  - `new.haven.digipomps.org CNAME staging.haven.digipomps.org`
  - `staging.haven.digipomps.org A 89.167.90.101`
- Cloudflare `1.1.1.1` and Google `8.8.8.8` return the same records
- HTTP redirects to `https://new.haven.digipomps.org/`
- TLS verification succeeds for the live host (`ssl_verify_result = 0`)
- public HTTPS responses against the resolved VPS:
  - `/`: HTTP 200
  - `/artikler/`: HTTP 200 with 17 individually addressable articles
  - `/artikler/digital-uavhengighet/`: HTTP 200
  - `/artikler/mennesket-forst/`: HTTP 200
  - `/artikler/demokrati-trenger-mer/`: HTTP 200
  - `/artikler/agent-pa-dine-vegne/`: HTTP 200
  - `/artikler/haven-og-standardene/`: HTTP 200
  - `/bevis/tilgangskontroll/`: HTTP 200
  - `/kilder/`: HTTP 200
  - `/om/`, `/personvern/` and `/rettelser/`: HTTP 200
  - unknown path: HTTP 404
- review assets return HTTP 200 with correct content types:
  - `/assets/site.css?v=20260803c`: `text/css`
  - `/assets/haven-human-agency-20260803.webp`: `image/webp`
  - `/assets/haven-control-loop-20260803.webp`: `image/webp`
  - `/assets/haven-logo.png`: `image/png`
- live Chromium verifies that the logo, human-agency hero and human control-loop
  illustration have non-zero intrinsic dimensions and that the stylesheet
  changes computed colors
- the user-supplied HAVEN logo is present in header, footer and 404 treatment;
  its deployed SHA-256 matches the supplied source file exactly
- the 3 August review variant visibly includes the approved digital-independence
  hero, the five-step control loop, the labelled democracy hypothesis and the
  maturity boundary
- the refreshed warm editorial design passed desktop and mobile browser checks
  on the live HTTPS host, with JavaScript on and off, accessible link names,
  keyboard focus, 200 % text, a 390 px viewport and no horizontal overflow
- the live mobile menu opens and closes with correct `aria-expanded` state
- the article filter changes the visible article count from 17 to 10 for
  `Vis konkret`
- certificate:
  - subject/SAN: `new.haven.digipomps.org`
  - issuer: Let's Encrypt `YE2`
  - valid from 2026-07-15 22:08:05 UTC
  - valid until 2026-10-13 22:08:04 UTC
- `certbot renew --dry-run --no-random-sleep-on-renew`: passed

## Current public verification

The earlier local DNS-cache caveat has cleared. This Mac now resolves
`new.haven.digipomps.org` through `staging.haven.digipomps.org` to
`89.167.90.101`, and the public hostname has passed a final visual browser pass
on the isolated deployed review release. The production index checksum remains
`6c41f47fec6020f9e6d4531842a160dfc3b848de6a9f574cb5bedb0a29b29784`.

The review release `20260804T051327Z` (deployed 2026-08-04 ~05:13 UTC) has
matching local, deployed and live HTTPS checksums:

- `index.html`: `593fb0bdd6ba56b3eba3ce54d92798e27bfee6642ff1a668e9c0790b9a4fcc90`
- `assets/site.css`: `60499df6951b9d0d337ded72ecb8c94db6310aa6acda49bae29b9791abbd4d49`
- `assets/site.js`: `3318c99817c51e8c29d4917b5d37a72939a4d25d7b3a679c9acf3f7bab8077a6`

2026-08-04 deploy verification:

- `nginx -t`: passed; production symlink unchanged
  (`/var/www/haven-public-new-releases/20260801T095935Z`), production `/`
  checksum still `6c41f47fec6020f9e6d4531842a160dfc3b848de6a9f574cb5bedb0a29b29784`
- live HTTPS on `new.haven.digipomps.org`: `/`, `/artikler/`,
  `/artikler/verktoy-som-samarbeider/`, `/kilder/`, `/bevis/tilgangskontroll/`
  and `/rettelser/` return 200; unknown path returns 404
- review headers retain CSP, one-year HSTS and
  `X-Robots-Tag: noindex, nofollow, noarchive`
- macOS tar AppleDouble (`._*`) files were removed from the release before the
  symlink switch; files are `root:root`, dirs 0755, files 0644
- local pre-deploy verification: `verify_app_entry.py` passed, app-entry
  unittests 8/8, and `app_entry_browser_smoke.js` passed against a local
  preview after fixing an index-arithmetic bug in the test's first-"agent"
  assertion (content was correct; the test compared against the sentence
  start instead of the word position)
