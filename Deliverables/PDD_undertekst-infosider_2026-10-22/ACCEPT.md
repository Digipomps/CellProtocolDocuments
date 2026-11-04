# ACCEPT — undertekst infosider (G3 godkjent 2026-11-04)

FORMAALSSPEC §1 og §5 rad for rad: forventet → faktisk, med evidens. G3 er Kjetils ord; denne fila er grunnlaget.

**Kontrollert:** 2026-11-04 15:46Z fra skyøkt med digipomps.org som tillatt domene.
**Produksjon = `origin/main` ef53d0e:** `curl` av `/`, `/artikler/`, `/artikler/mennesket-forst/` og `/assets/site.css` er byte-for-byte lik `git show origin/main:Website/…` (alle fire `cmp` uten avvik). PR #32 (919c391) og PR #37 (5461c1b) er altså begge rullet ut.

## Formålene (§1)

| Formål | Forventet | Faktisk i produksjon | Evidens | Status |
|---|---|---|---|---|
| …forside | Seksjonen `#mennesket-og-fellesskapet` har essensen som eyebrow og underteksten som overskrift | Eyebrow «Mennesket først – ikke mennesket alene», h2 «Din grense, båret av fellesskapet.» Seksjonens HTML er identisk med grenen fra 2026-10-22 | `images/prod-forside-seksjon.png`, `-mobil.png` | oppfylt |
| …artikkel | Ingressen begynner med underteksten; og:description er underteksten | Ingress «Din grense, båret av fellesskapet: HAVEN begynner ved individets grense …»; `og:description` = «Din grense, båret av fellesskapet.» | `images/prod-artikkel.png`; curl under | oppfylt |
| …oversikt | Kortet begynner med underteksten | «Din grense, båret av fellesskapet: råderetten må støttes av …» | `images/prod-artikkeloversikt-kort.png` | oppfylt |
| …utrulling | `curl` mot de tre sidene viser underteksten | Ett treff på forsiden, ett i oversikten, to i artikkelen (ingress + og:description) | curl under | oppfylt |
| quality.build-and-regression | Vakt OK, 8 tester grønne, hero uendret | Uendret siden TESTRESULT 2026-10-22; ingen ny kode i denne runden | TESTRESULT#build, #regression | oppfylt |

```
== /
      1 Din grense, båret av fellesskapet.
== /artikler/
      1 Din grense, båret av fellesskapet: råderetten må støttes av rettigheter, trygge standardvalg, fellesskap og ansvarlige institusjoner.
== /artikler/mennesket-forst/
      1 Din grense, båret av fellesskapet: HAVEN begynner ved individets grense, men grensen må bæres av et økosystem som gjør gode valg enkle og misbruk vanskelig.
      1 meta property="og:description" content="Din grense, båret av fellesskapet."
```

## Paritet {#parity}

Samme skript (`tools/shots.js`), samme selektorer og viewporter (1280 × 900, 390 × 900), Chromium/Playwright. Piksler regnet som ulike når en kanal avviker mer enn 40.

| Flate | Referanse (G1-GUI) | Faktisk (prod) | Side om side | Diff |
|---|---|---|---|---|
| Forsiden, seksjon, 1280 | `images/etter-forside-seksjon.png` (1280 × 799) | `images/prod-forside-seksjon.png` (1280 × 800) | `images/side-om-side-forside-seksjon.png` | 2,23 % — samme tekst; seksjonen er 1 px høyere, og «mu-lig» i fjerde kort bryter med orddeling |
| Forsiden, seksjon, 390 | `images/etter-forside-seksjon-mobil.png` | `images/prod-forside-seksjon-mobil.png` | `images/side-om-side-forside-seksjon-mobil.png` | 1,28 % — samme tekst; «sto-ler» bryter med orddeling |
| Artikkeloversikt, kort | `images/etter-artikkeloversikt-kort.png` | `images/prod-artikkeloversikt-kort.png` | `images/side-om-side-artikkeloversikt-kort.png` | 0 px |
| Artikkelen | `images/etter-artikkel.png` | `images/prod-artikkel.png` | `images/side-om-side-artikkel.png` | 0 px |

**Avvik på forsiden, forklart:** seksjonens HTML i produksjon er identisk med grenen som ble godkjent. Forskjellen kommer fra `assets/site.css` slik PR #37 endret den (blant annet `hyphens: auto` og ny cache-versjon `?v=20261030a`), som kom etter G1-GUI-bildene. Det er en endring i linjebryting, ikke i innhold eller plassering. Ber om Kjetils ord på at dette er greit (eller at orddelingen skal fjernes i en egen sak).

## Dokumentasjon {#docs}

Artikkelen viser «Sist faglig gjennomgått 22. oktober 2026» (se `images/prod-artikkel.png`). Utgivelsesnotatet `Website/RELEASE_NOTE_2026-10-22.md` finnes. Oppfylt.

## Status {#status}

STATUS.md er oppdatert med denne runden; mappen har FORMAALSSPEC, STATUS, TESTRESULT, ACCEPT, `tools/shots.js` og `images/` med for-, etter-, prod- og side-om-side-bilder. Oppfylt.

## Dom

Alle formål oppfylt i produksjon. Ett kjent avvik (orddeling på forsiden fra PR #37s CSS) venter på Kjetils ord. G3 står som `venter` til Kjetil sier ja.

**2026-11-04:** Kjetil: «ja til G3». Orddelingsavviket ble lagt frem i samme spørsmål og regnes som godtatt.
