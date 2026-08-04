# Publiserings- og datakvittering

Dato: 1. august 2026  
Formål: publisere den reviderte, statiske HAVEN-informasjonssiden.

## Publisering

- Mottaker: egen HAVEN-VPS, `89.167.90.101`.
- Transport: nøkkelautentisert SSH/rsync.
- Aktiv release: `/var/www/haven-public-new-releases/20260801T095935Z`.
- Offentlige mål: `https://digipomps.org` og den noindex-merkede testverten `https://new.haven.digipomps.org`.
- Aktiv Nginx-konfigurasjon ble sikkerhetskopiert som `/etc/nginx/sites-available/haven_public.conf.backup-20260801T1001Z` før kontrollert utskifting.
- `nginx -t`: bestått. Tjeneste: aktiv.
- Integritetskontroll: lokal og aktiv SHA-256 er identisk for `index.html`, `site.css` og `site.js`.

## Personopplysninger og organisasjonsdata

Ingen nye personfelt ble funnet eller utledet. Den statiske siden publiserer:

| Felt | Kilde | Formål | Status |
|---|---|---|---|
| `kjetil@digipomps.org` | Allerede offentlig kontaktpunkt i eksisterende nettstedskilde | Kontakt om pilot, rettelse, kode, styring og personvern | Videreført uendret |
| Stiftelsen Digipomps, org.nr. 922 135 134 | Brønnøysundregistrene | Identifisere ansvarlig organisasjon og gjøre registrert formål kontrollerbart | Verifisert og publisert |

Privat adresse fra organisasjonsregisteret ble ikke tatt med. Ingen informasjonskapsler, besøkslogger, autentiseringsdata eller hemmeligheter ble lest, lastet opp eller publisert.

## Ekstern tilgang

- Offentlige standard-, kode- og organisasjonskilder ble lest for kildekontroll.
- VPS-en ble lest og endret bare for filpublisering, Nginx-test, symlink-bytte og tjenesteomlasting.
- Produksjon og testvert ble kontrollert med uautentiserte HTTPS-forespørsler og vanlige nettleservisninger.
- Et forsøk på å lese Nginx-loggrotasjon via den begrensede `ops`-kontoen ble avvist fordi `sudo` krevde passord. Selve loggene ble ikke lest.

## Lagring og sletting

- Den publiserte releasen lagres varig på VPS-en til en senere, separat opprydding.
- Arbeidsdokumenter og testresultater lagres i dette daterte leveranseområdet.
- Ingen personopplysninger ble skrevet til HAVEN Entity eller annen profil-/identitetslagring.
- Faktisk retensjon og tilgangsrutine for ordinære Nginx-logger er fortsatt et åpent driftspunkt; personvernsiden sier dette uttrykkelig.

## Verifikasjon

- Begge vertsnavn returnerer HTTP 200 for alle nye hovedsider og HTTP 404 for ukjent sti.
- Produksjon sender CSP, Permissions Policy, HSTS, `nosniff` og rammeforbud.
- Testverten sender i tillegg `X-Robots-Tag: noindex, nofollow, noarchive`.
- Produksjon er testet uten horisontal overflyt på 1280 px og 390 px.
- Mobilmeny, Escape-lukking, artikkelfilter, gamle fragmentlenker og nye legacy-omdirigeringer er kontrollert.
