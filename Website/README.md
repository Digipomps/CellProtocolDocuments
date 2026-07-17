# HAVEN public website

Static, self-hosted first version of the public HAVEN/Digipomps site.

## What is included

- Norwegian-first landing page with three reading paths
- 14 short articles spanning introductory, concrete and technical levels
- explicit status labels for implemented, tested, pilot and research claims
- source and method page
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

## HAVEN VPS review deployment

The active review target is:

```text
https://new.haven.digipomps.org
```

It uses the existing HAVEN VPS at `89.167.90.101`, Nginx, the static docroot
symlink `/var/www/haven-public-new`, and Certbot. The tracked
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

- `/`, `/artikler/`, `/kilder/` and `/404.html`
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
