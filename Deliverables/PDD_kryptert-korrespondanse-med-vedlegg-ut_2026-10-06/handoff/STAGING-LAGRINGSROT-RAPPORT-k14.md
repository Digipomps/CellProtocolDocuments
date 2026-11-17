# k14 — staging-lagringsrot: stoppet før mutasjon

12.10.2026. Oppgave **HD-0218**, `HANDOFF_REQUIRED`.

**`CELL_SCAFFOLD_BRIDGE_ORIGIN` er ikke satt i staging-containeren.**
`CELL_SCAFFOLD_OWNER_CONTEXT` er satt. Oppdraget krever begge, men tillater
bare én ny env-linje: `HAVEN_CORRESPONDENCE_DATA_ROOT`. Den manglende
forutsetningen kan derfor ikke rettes innenfor det godkjente omfanget.
Ingen miljøverdier er gjengitt.

Godkjenningen som ble lagt til grunn: Kjetil 12.10 14:26Z valgte
«Ja, skru på» på kortet: «Skru på korrespondansen på staging ved å gi den en egen lagringsmappe?»
Kortets kontekst var bare staging, én miljøinnstilling og en mappe på
datadisken, samme versjon startet på nytt og en vei tilbake.
Det er ikke manglende godkjenning av denne endringen som stoppet arbeidet;
det er en ekstra miljøforutsetning utenfor én-linje-mandatet.

## Hva som ble gjort og endret

Bare lesende vertskontroller. Ingen katalog opprettet, ingen env-linje endret,
ingen omstart, ingen image-/SHA-endring og ingen datasletting. Prod ble ikke
inspisert eller endret. Lokalt ble denne rapporten, verdifrie bevis og
HD-0218 registrert.

Den etablerte release-veien for 2026.10.4, `wp-rel-deploy.sh`, installert
`haven-deploy`/`haven-deploy-doctor` og env-cutover-mønsteret i
`HAVEN-Deploy/_handoff/HD-0006/bytt-invitasjoner.sh` ble lest.
Vertstilgangen gikk gjennom `HAVEN-Deploy/lib/vert.sh`, samme inngang som
release-verktøyet. Ingen alternativ deployvei ble brukt.
Den installerte deployutgaven har `SET_ENV_FILE`, env-only-modus,
fingeravtrykk-vakt, rollback-container og readiness etter start og kontrollert
restart. Repo-kopien er ikke identisk med den installerte utgaven.

| Forhåndskontroll | Målt resultat |
| --- | --- |
| Apprevisjon / lokalt image | Eksakt `9ff06f8446b6331da49272f5fd72b947b4092ece`; kjørende image-ID lik bildet for revisjonen |
| Eierkontekst | Satt; verdi ikke hentet ut |
| Eksplisitt bridge-origin | **Ikke satt** |
| Lagringsrotvariabel | Mangler både i kjørende env og vedvarende env-fil |
| Vedvarende env-fil | 6 linjer; sikker eier/modus; avsluttende linjeskift |
| Kjørende env | 94 linjer |
| Nåværende deploy-sammenslåing | Ingen andre verdiforskjeller beregnet på verten |
| Datamount | Eksisterende skrivbar bind-mount; samme filsystemenhet som vertens rot. Separat datavolum er ikke bevist |
| Ledig plass ved datamount | 47 701 348 352 byte, over kravet 10 000 000 000 |
| Appens bruker | Bruker/gruppetilhørighet identifisert; PID 1 samsvarer med appbrukeren |
| Ny katalog / modus 0700 | Ikke opprettet eller aktivert, fordi forhåndskontrollen stoppet |

Env-linjeantallene er førmålinger; en endring på +1 og bevaring etter cutover
kan ikke hevdes når ingen cutover ble kjørt. Ingen eksisterende env-verdier
ble returnert fra verten.

## Health før og etter avsluttet forhåndskontroll

Endepunkt: `https://staging.haven.digipomps.org`.
«Etter» betyr etter lesende kontroll og stopp, ikke etter en deploy.

| Måling | Før | Etter |
| --- | --- | --- |
| `/health/build`, HTTP | 200 | 200 |
| Apprevisjon | `9ff06f8446b6331da49272f5fd72b947b4092ece` | Uendret |
| CellProtocol | `b4100f5734bb0b3781600845a267e424e55c0989` | Uendret |
| Miljø / buildstatus | staging / ok | Uendret |
| `/health/ready`, HTTP | 200 | 200 |
| Global status / acceptsNewTraffic | ready / true | ready / true |
| correspondence.configured | false | false |
| correspondence.ready | true | true |
| correspondence.storageAvailable | false | false |

Build målt 2026-10-12T14:37:20.931678+00:00 og 2026-10-12T14:38:20.054098+00:00.
Readiness målt 2026-10-12T14:37:21.030171+00:00 og 2026-10-12T14:38:20.230247+00:00.
De lagrede build-projeksjonene er identiske, inkludert byggtid og alle fire
revisjonsfelter. Readiness-projeksjonene er også identiske.

## Cutover-kvittering og rollback

**Ingen cutover-kvittering finnes for k14**, fordi utførelse ikke ble startet.
`result.json` er en forhåndskontrollkvittering, ikke en deploykvittering.
Ingen claim ble tatt, ingen rollback-container laget, og rollback var ikke
nødvendig. Staging står med den allerede kjørende versjonen.

Ved senere godkjent utførelse er den leste rollback-veien den eksisterende
`haven-deploy --env-only`-transaksjonens gjenoppretting av gammel container,
med verifisert readiness og revisjon. Vedvarende env må deretter legges tilbake
fra sikker kopi først når deployen er avsluttet, låsen er fri og gammel
container er bekreftet. Lagringsdata skal beholdes. Denne veien ble lest,
ikke kjørt eller nytestet i k14.

Eksakt deployet kilde (`Sources/App/Services/CorrespondenceRelationshipHost.swift`,
`install`) har fallback fra eksplisitt bridge-origin til WebAuthn-origin.
Dette er ikke bevis for at den eksplisitte variabelen er satt, og k14 har ikke
verifisert fallbackens verdi eller brukt den som erstatning for akseptansekravet.
Det hevdes derfor heller ikke at hosting teknisk er umulig med fallback.

## Bevis og videre avklaring

Verdifrie bevis ligger under `HAVEN-Deploy/_handoff/KORR-UT/k14/`:
`host-preflight.json`, `health-build-before.json`, `health-build-after.json`,
`health-ready-before.json`, `health-ready-after.json`, `tool-source-hashes.json`,
`read-only-preflight.py` og `result.json`. `SHA256SUMS` binder disse filene.
Rapporten bruker relative bevisstier, uten private vertsstier.

HD-0218 bevarer blokkeringen: det må avklares om også den manglende
bridge-origin-innstillingen skal settes, eller om akseptansekravet skal endres.
Ingen slik utvidelse er utført. Før eventuell ny kjøring må mountens
vedvarende datavolum og fersk diskplass også bekreftes.

Gjenbrukbar læring er anvendt i `handoff/K1-REUSABLE-NOTES.md`, post
`L-2026-10-12-ved-env-only-aktivering-av-korrespondanse-ma`.
Dokumentmålet følger git; ingen commit eller push er utført.
Global læringskontroll har eldre åpne poster; k14-posten er ferdigbehandlet.
Deployregisteret validerer med 0 problemer.

STATUS: STOPPET — CELL_SCAFFOLD_BRIDGE_ORIGIN mangler; å sette den krever en ekstra env-endring utenfor det godkjente én-linje-omfanget.
