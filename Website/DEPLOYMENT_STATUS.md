# HAVEN public website deployment status

Last updated: 2026-07-17 17:18 Europe/Oslo

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
- release: `/var/www/haven-public-new-releases/20260717T092605Z`

### Production verification

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
  - `/artikler/`: HTTP 200
  - `/kilder/`: HTTP 200
  - unknown path: HTTP 404 with the custom HAVEN 404 page
- HTTP redirects permanently to the corresponding HTTPS apex URL
- HTTPS `www` redirects permanently to the corresponding apex URL
- legacy WordPress paths redirect to their closest current page or section
- production headers include CSP, Permissions Policy, one-year HSTS, nosniff
  and frame denial
- production does not emit `X-Robots-Tag`; `robots.txt` allows crawling
- desktop and mobile browser passes show the HAVEN page, logo and illustration
  without horizontal overflow
- the production mobile menu opens and closes with the correct accessibility
  state
- no browser warnings or errors were observed on the production page

During the DNS cutover, one browser initially displayed its still-fresh cached
WordPress response for the bare URL. A normal reload fetched the HAVEN page;
unique and direct HTTPS requests had already returned the new release. Existing
visitors with an old browser cache may therefore need one reload during the
cutover window.

## Review host

- VPS: `89.167.90.101`
- web server: Nginx 1.24.0
- release: `/var/www/haven-public-new-releases/20260717T092605Z`
- active docroot symlink: `/var/www/haven-public-new`
- active Nginx site: `/etc/nginx/sites-enabled/haven_public_new.conf`
- tracked source config: `Website/nginx-new-haven.conf`

The release was uploaded as an isolated static bundle. Files are owned by
`root:root`; directories are mode `0755` and files are mode `0644`.

## Verified

- `nginx -t`: passed
- Nginx service after reload: active
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
  - `/artikler/`: HTTP 200
  - `/kilder/`: HTTP 200
  - unknown path: HTTP 404
- the user-supplied HAVEN logo is present in header, footer and 404 treatment;
  its deployed SHA-256 matches the supplied source file exactly
- the refreshed black/white/warm-accent design passed desktop and mobile browser
  checks on the live HTTPS host, with no horizontal overflow or browser errors
- the live mobile menu opens and closes with correct `aria-expanded` state
- the article filter changes the visible article count from 14 to 7 for
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
on the deployed release.
