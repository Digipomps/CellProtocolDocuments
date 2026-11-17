# k14-r2 — korrespondanseverten aktivert på staging

12.10.2026. **HD-0218: COMMITTED_VERIFIED.**
Opprinnelig k14-rapport er først sikkerhetskopiert byte for byte til
`handoff/STAGING-LAGRINGSROT-RAPPORT-k14.md`.

Kjetils «Ja, skru på» 12.10 14:26Z og k14-r2-oppdraget autoriserte bare
staging, én miljøinnstilling, privat katalog på eksisterende datamount og
omstart av samme versjon. Kravet om eksplisitt bridge-origin var agentens;
korrespondanse-tråden (ikke Kjetil) fjernet det i k14-r2-oppdraget. Ingen bridge-origin-variabel ble satt.

## Endring og forhåndskontroll

**Effektiv origin via WebAuthn-fallback: samsvarer.** Eksakt deployet kilde
på `9ff06f84` ble lest fra `CorrespondenceRelationshipHost.install` og
WebAuthn-konfigurasjonen, og sammenligningen ble utført på verten mot
kjørende env. Ingen origin-/env-verdi er gjengitt her.

En privat katalog ble opprettet under eksisterende skrivbar datamount,
med appbrukerens eier og gruppe, modus **0700** og bekreftet skrivetilgang
for appen. Lagringen er **bind-mount fra vertens disk**, uavhengig av
containerens skrivbare lag. Samme mount, kilde, destinasjon, type og
rettigheter ble verifisert etter containerbytte og kontrollert restart.
Dette er ikke en påstand om separat datadisk. Ingen data ble slettet.

| Kontroll | Før | Etter |
| --- | --- | --- |
| Ledig plass ved datamount | 47 674 798 080 byte | 47 674 560 512 byte |
| Minimumskrav | 10 000 000 000 byte | Bestått |
| Vedvarende env-fil | 6 linjer | 7 linjer |
| Kjørende env | 94 linjer | 95 linjer |
| Øvrig env | Beregnet uendret | Verifisert uendret |
| Apprevisjon | `9ff06f8446b6331da49272f5fd72b947b4092ece` | Uendret |
| Image | Eksakt kjørende image | Uendret |

Nøyaktig én linje ble lagt til: variabelen `HAVEN_CORRESPONDENCE_DATA_ROOT`.
Verdien utelates. Alle opprinnelige byte i env-filen er bevart; kjørende
miljø har nøyaktig samme øvrige nøkler og verdier. Env-filens eier/modus og
staging-deploykonfigurasjonen er uendret. Sikker kopi ligger privat på verten.
Prod ble ikke inspisert eller endret. Ingen ny image, build eller SHA.

## Cutover-kvittering og health

Vertstilgang gikk gjennom `HAVEN-Deploy/lib/vert.sh`. Installert
`haven-deploy --env-only` brukte `SET_ENV_FILE`, samme fulle commit og image,
fingeravtrykk-vakt, parkert rollback-container, readiness ved første start
og readiness etter kontrollert restart. Installerte verktøy hadde samme
SHA-256 som k14-bevisene; repo-kopien ble ikke brukt som deployutfører.
En forsinket prøvestart beviste terminalfri sudo og sluttmarkør etter at
SSH-kallet hadde returnert.

- Transaksjon: `20261012T163526Z-staging-9ff06f84`.
- Utfall: `committed_verified`, exit-kode **0**, avsluttet **16:36:01Z**.
- Fingeravtrykk før, etter første start og etter restart: identiske.
- Kildens kvitteringshash: `82d742afaa3f0057e754a0654c43fe217077e22407b38c3b2e547ac9e0c19026`.
- Redigert kvitteringsprojeksjon: `HAVEN-Deploy/_handoff/KORR-UT/k14-r2/receipt.json`.

| Offentlig måling | Før 16:33:13Z | Etter 16:36:37Z |
| --- | --- | --- |
| `/health/build`, HTTP | 200 | 200 |
| Apprevisjon | `9ff06f84` | `9ff06f84` |
| Miljø / buildstatus | staging / ok | staging / ok |
| Hele build-projeksjonen | Målt | Identisk, inkludert byggtid og avhengighetsrevisjoner |
| `/health/ready`, HTTP | 200 | 200 |
| Global status / acceptsNewTraffic | ready / true | ready / true |
| correspondence.configured | false | **true** |
| correspondence.ready | true | **true** |
| correspondence.storageAvailable | false | **true** |

## Rollback-vei

Rollback var ikke nødvendig. Den gamle containeren finnes fortsatt, stoppet,
med original container-ID; sikker env-kopi er beholdt privat på verten.
Transaksjonens originale kvittering identifiserer rollback-containeren.
Den lokale forberedelseskoden identifiserer den private sikkerhetskopien;
private vertsstier utelates fra rapporten.

Ved feil under transaksjonen ville installert deployverktøy gjenopprettet
original container og verifisert readiness/revisjon. Env-gjenoppretting er
et separat trinn: sluttmarkør, fri deploylås, bekreftet original container,
gammel env og health må foreligge før bare den tilføyde linjen fjernes med
sikkerhetskopien som grunnlag. `verify.py` inneholder denne betingede veien;
den ble ikke utløst i denne kjøringen. Katalog og data beholdes.

Ved senere tilbakerulling av den vellykkede aktiveringen: ta ny claim,
kontroller at ingen annen deploy eller env-endring har skjedd, fjern
bare den nye env-linjen med sikker kopi som grunnlag, og bruk samme installerte env-only-
transaksjon på verifisert gjeldende revisjon. Den bevarte gamle containeren
er også tilgjengelig som gjenopprettingsgrunnlag. Ingen slik senere
rollback er utført eller påstått testet her.

## Avvik og registrering

Katalog og env ble forberedt **før vellykket claim**, fordi lokal
claim-registrering feilet og et avhengig kall likevel ble kjørt. Først
feilet Python-oppslaget i bash med inkompatibel binær; neste parseregel
fant ikke containernavnet med mellomrom i konfigen. Ingen overlappende
claim var observert. Claim ble bekreftet **før cutover**, og feilen er
registrert på HD-0218 og i deploy-læringen. Dette avviket skal ikke brukes
som mønster for nye kjøringer.

Første prøvestart feilet på lokal quoting; korrigert forsinket prøvestart
bestod før env-endringen. Første etterkontroll ga falskt mount-avvik fordi
Docker endret listeorden. Alle felter var identiske ved sammenligning per
destinasjon; første kontroll er bevart separat. Etter avsluttet deploy ble
claim sluppet før done-registreringen, som hd derfor avviste. En kort ny
registreringsclaim lukket posten uten nye vertsendringer og ble frigitt.

HD-0218 er oppdatert med oppfylt origin-avklaring, gjennomført kommando-post,
cutover-bevis og COMMITTED_VERIFIED. Ingen claim står igjen for oppgaven.
Gjenbrukbare funn er anvendt i `handoff/K1-REUSABLE-NOTES.md`, læringspost
`L-2026-10-12-k14-r2-origin-claim-mounts`. Dokumentet følger git; ingen
commit/push er utført. Deployregisteret validerer med 0 problemer.

Bevis er samlet i `HAVEN-Deploy/_handoff/KORR-UT/k14-r2/`: health før/etter,
lesende preflight, katalog/env-forberedelse, cutover- og akseptansekontroll,
redigert kvittering og kildekoden til kontrollene. `SHA256SUMS` binder disse.
Rå env og rå deploylogg er ikke hentet fra verten. Denne leveransen beviser
vertsaktivering; sending/mottak mellom klienter inngikk ikke i oppdraget.

STATUS: LEVERT
