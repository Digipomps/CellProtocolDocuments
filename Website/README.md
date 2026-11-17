# HAVEN public website

Static, self-hosted first version of the public HAVEN/Digipomps site.

## What is included

- Norwegian-first landing page with three reading paths
- 18 short articles, each with its own URL, spanning introductory, concrete and technical levels
- explicit status labels for implemented, tested, prototype, pilot and research claims
- source and method page, a reproducible component proof, and organization,
  privacy and corrections pages
- accessible, responsive HTML/CSS with no analytics or third-party assets
- the official HAVEN logo, with a restrained black, white and warm-accent design system
- Caddy container with automatic HTTPS and redirects from important WordPress paths
- Nginx configurations for production `digipomps.org` and the review host
  `new.haven.digipomps.org`

This directory is isolated from the currently conflicted Book files in the
parent worktree. It does not publish anything by itself.

## Preview locally

From this directory:

```sh
python3 -m http.server 4173
```

Open `http://localhost:4173/`.

The local preview does not exercise the production redirects or security
headers in `Caddyfile`.

## App entry release gate

The public app entry is deliberately `blocked` as of 2026-08-03. No canonical
production app origin or working installation page has been documented.
Staging, local addresses and the review host must never be substituted.

The only activation point is the marked hero block between
`HAVEN_APP_ENTRY_START` and `HAVEN_APP_ENTRY_END` in `index.html`. While
blocked it contains exactly two ordinary links:

1. `Forstå HAVEN`
2. `Se et konkret testbevis`

Run the static release guard from the repository root:

```sh
python3 Website/tools/verify_app_entry.py
python3 -m unittest Website/tests/test_verify_app_entry.py
```

With the local preview running, the workspace Playwright installation can also
verify the no-JavaScript journey, keyboard focus, 200 % text and mobile layout:

```sh
node Website/tests/app_entry_browser_smoke.js http://127.0.0.1:4173
```

When the app owner has supplied a verified production origin and installation
page, change the same block to exactly two static links:

| `data-app-entry-state` | Primary link text | Secondary link |
| --- | --- | --- |
| `public-app` | `Installer HAVEN` | `Forstå HAVEN` |
| `public-demo` | `Åpne HAVEN-demoen` | `Forstå HAVEN` |
| `homescreen-demo` | `Legg HAVEN-demoen på hjemskjermen` | `Forstå HAVEN` |

The primary link must be an absolute HTTPS URL to the app's own installation
page. It must not use `target`; mobile stays in the same tab. The test-proof
entry remains in the next section instead of becoming a third hero button.

Before release, make the approved origin explicit and follow redirects during
the live check:

```sh
python3 Website/tools/verify_app_entry.py \
  --allow-origin https://VERIFIED-APP-ORIGIN \
  --check-live
```

The guard checks the information site's static contract. It does not prove
app maturity. Activation still requires dated evidence for the final URL,
manifest, icons, platform flow, and physical Android and iOS tests. Publish the
HTML and updated deployment/corrections status atomically in one release.

## Self-host with Docker Compose

Prerequisites:

1. A server with ports 80 and 443 reachable from the internet.
2. DNS `A` and/or `AAAA` records for `digipomps.org` pointing to that server.
3. An archive/backup of the current WordPress site before the DNS switch.

On the server:

```sh
docker compose up -d --build
```

Caddy requests and renews TLS certificates automatically. Certificate state is
kept in the named `caddy_data` volume.

## HAVEN VPS production deployment

The production targets are:

```text
https://digipomps.org
https://www.digipomps.org -> https://digipomps.org
```

Both names point at the HAVEN VPS `89.167.90.101`. Nginx serves the static
docroot symlink `/var/www/haven-public-new` using the tracked
`nginx-digipomps.conf`. HTTP redirects to HTTPS, `www` redirects to the apex
domain, and legacy WordPress paths retain useful redirects. The production
host is indexable and uses `robots.txt` plus the canonical production URLs in
the HTML and sitemap.

The Let's Encrypt certificate covers both production names. Certbot renewal
has been verified with a successful dry-run.

### Releasing content changes to production

Releases are immutable directories under `/var/www/haven-public-new-releases/`
named by UTC timestamp; the docroot symlink is moved to the new one. The method
(copy the running release, replace exactly the changed files, `diff -rq`,
`sha256sum` local = deployed, move the symlink, `nginx -t && reload`) is
scripted in the deploy repository:

```sh
# from the HAVEN root on a machine with the host key (never hardcode the key:
# HAVEN-Deploy/lib/vert.sh derives it)
bash HAVEN-Deploy/_handoff/FORSIDE/website-release.sh dry-run        # writes nothing, shows the diff
bash HAVEN-Deploy/_handoff/FORSIDE/website-release.sh release        # FILES from origin/main
bash HAVEN-Deploy/_handoff/FORSIDE/website-release.sh merge-release  # squash-merge BRANCH's PR first
```

`FILES`, `BRANCH` and `SETNING` (a guard sentence that must exist on
`origin/main` before a release is allowed) are set at the top of the script.
It always releases from `origin/main`, never from a working tree, keeps the
previous release for rollback and prints the rollback command in its log. It can
also run as a `skript` job in the Losen queue (`_losen-queue/LES_MEG.md`).
First use: the front-page sentence of PR #25, released 2026-09-28 as
`20260928T120959Z`; dry-run verified against the host 2026-09-29.

When verifying a release from an agent session, do not trust a single
`WebFetch` of the page: it can return a stale copy (on 2026-09-29 it showed
`/rettelser/` without the new entry although the host already served it). Add a
cache-busting query such as `?kontroll=<date>`, or compare the file on the host.

## HAVEN VPS review deployment

The active review target is:

```text
https://new.haven.digipomps.org
```

It uses the existing HAVEN VPS at `89.167.90.101`, Nginx, the static docroot
symlink `/var/www/haven-public-review`, and Certbot. Production continues to
use the separate `/var/www/haven-public-new` symlink. The tracked
`nginx-new-haven.conf` mirrors the active TLS configuration. The review host
adds `X-Robots-Tag: noindex, nofollow, noarchive`; the canonical links continue
to point at the intended production domain.

DNS currently uses:

```text
new.haven  CNAME  staging.haven.digipomps.org
```

The initial TLS installation command was:

```sh
ssh root@89.167.90.101 \
  'certbot --nginx -d new.haven.digipomps.org --redirect --non-interactive'
```

Automatic renewal has been verified with a successful Certbot dry-run. Verify
both the certificate and the user-visible pages after future Nginx or content
changes.

The current live deployment state is recorded in
[`DEPLOYMENT_STATUS.md`](DEPLOYMENT_STATUS.md).

After future content, Nginx or DNS changes, verify:

- `/`, `/artikler/`, `/bevis/tilgangskontroll/`, `/kilder/`, `/om/`,
  `/personvern/`, `/rettelser/` and `/404.html`
- mobile and keyboard navigation
- legacy redirects in `Caddyfile`
- mail and GitHub links
- the final public contact details

## Content and claim maintenance

- Date every status statement.
- Keep societal effects as hypotheses until a pilot measures them.
- Do not introduce global reputation, global person identity or hidden
  behavioural profiling.
- External sources support the problem framing; HAVEN code/tests/pilots support
  claims about HAVEN.
- Run the repository text-reliability tool and a browser smoke pass after
  substantive copy changes.

The generated hero illustration was produced with the built-in image-generation
tool using an editorial paper-collage prompt. It contains no third-party brand
assets. The HAVEN logo is a user-supplied brand asset and is published unchanged
in `assets/haven-logo.png`.
