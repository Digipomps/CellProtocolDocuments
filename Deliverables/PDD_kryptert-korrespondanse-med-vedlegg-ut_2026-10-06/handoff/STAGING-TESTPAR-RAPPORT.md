# k13-r2 — staging-testpar: innslipp og tekst vist, vedlegg stopper

Målt 2026-10-12 fra 18:06Z mot `https://staging.haven.digipomps.org`.
To ferske prøveidentiteter, A og B, én ny relasjonscelle. Ingen eksisterende
personprofiler eller innbokser er åpnet. Bare testparet mottok meldinger.

Alle bevisstier er relative til HAVEN-roten. Bevisrot:
`HAVEN-Deploy/_handoff/KORR-UT/k13-r2/`. Tabellen bruker filnavn relativt til
denne roten. `SHA256SUMS` binder bevisfilene; det er ikke vedleggsbytebevis.
Den tidligere k13-rapporten er bevart i `handoff/STAGING-TESTPAR-RAPPORT-k13.md`.

| Steg | Utfall | Bevis |
| --- | --- | --- |
| Start: revisjon og readiness | BESTÅTT. HTTP 200; CellScaffold `9ff06f84`, CP `b4100f57`. correspondence configured/ready/storageAvailable = true. Samme revisjoner og readiness ved slutt. | `health-build-start.json`, `health-ready-start.json`, `health-build-end.json`, `health-ready-end.json` |
| Start: klient og disk | BESTÅTT. PR #32-biblioteket bygget lokalt mot CP-tag 2026.9.7; bibliotek og runtime uendret. Disk 114,1 GiB; 104,1 GiB / 11 % etter 10 GiB reserve. To Swift-jobber, bounded runner og prune-låst arbeidstre. | `client-build.json`, `actual-cp-revision.txt`, `local-client.patch`, `build-attempts.json` |
| 1. A oppretter relasjonscelle over autentisert bro | BESTÅTT. `create` returnerte `created` med gyldig UUID og forventet staging-broadresse. Ingen debug-bypass. | `00-identities.json`, `01-create-attempt.json`, `01-created.json`, `process-establish.json` |
| 2. B ber om innslipp; A sammenligner seks sifre og godkjenner | BESTÅTT PÅ PROTOKOLLNIVÅ. Ventende forespørsel bandt B sine nøkler; kodene var like og seks sifre; A signerte, B hentet samme signerte avtale og `agreement.accept` svarte `accepted`. Kodesammenligningen var automatisert for testparet. | `02-join-response.json`, `02-admitted.json`, `process-admit.json` |
| 3a. Tekst begge veier | BESTÅTT. Nøyaktig tekst og avsendersignatur kontrollert hos mottakeren. Slutthistorikken inneholder to tekster, én hver vei. | `03-text-A-to-B.json`, `03-text-B-to-A.json`, `audit-history-A.json`, `audit-history-B.json` |
| 3b. Vedlegg over 1 MB begge veier; SHA-256-byteidentitet | FEILET. Begge kildene var 1 100 037 byte. A: prepare og første upload fikk svar, deretter `attachmentUnavailable`. B: samme feil allerede for chunk 0. Ingen vedlegg publisert i observert slutthistorikk; ingen ferdig mottatt fil eller mottaker-SHA-256. | `03-attachment-attempt-A.json`, `03-attachment-attempt-B.json`, `owner-transfer-attempt/trace-A-transfer-003.json` til `005.json`, `trace-B-transfer-004.json` til `006.json`, `failure-transfer.json`, `failure-transfer-b.json` |
| 4. Historikk fra ny klientøkt for begge | DELVIS BESTÅTT: ny prosess og nye klienter leste/dekrypterte de to tekstene for både A og B med senderVerified=true. Vedleggshistorikk kan ikke vises siden opplasting feilet. | `process-audit.json`, `audit-history-A.json`, `audit-history-B.json`, `trace-A-audit-*.json`, `trace-B-audit-*.json` |
| 5. Tilbakekall publisert vedlegg; henting avvises | IKKE VIST. Ingen publisert vedleggsleveranse kunne tilbakekalles. Klientens automatiske opprydding etter opplastingsfeil feilet også; B-sporet viser `attachments.revoke` → `CellBase.SetValueError`, NSError-kode 4. Dette teller ikke som vellykket tilbakekall. | `trace-B-transfer-006.json`, `failure-transfer.json`, `failure-transfer-b.json` |

## Stoppgrunn og hva som mangler

En fungerende vedleggsopplasting fra begge deltakere, etterfulgt av byteverifisert
henting og dokumentert tilbakekall, mangler fortsatt. Den konkrete avvisningen er
`status=error, message=attachmentUnavailable` fra `attachments.upload`.
For B var den utgående chunken indeks 0, ikke terminal, med 65 564 ciphertext-byte
(64 KiB klartekst pluss 28 byte kryptografisk overhead). Det er ikke en
fullført 1 MB-overføring. A fikk ett upload-svar `ok` før neste kall ble avvist;
indeks/størrelse ble ikke registrert i dette eldre sporingsbygget.

Eksakt CP-kilde på `b4100f57`,
`Sources/CellBase/Cells/Correspondence/CorrespondenceCell.swift:1242`, mapper
feil fra vedleggshåndtereren til den samme generiske meldingen.
`CorrespondenceAttachmentStorage.swift:325` kontrollerer blant annet sekvens,
størrelse og lagring. Svaret alene fastslår **ikke** hvilken kontroll som feilet.
Vertens interne feillogg, filer og env er ikke lest. Det er ikke bevist at en
invitasjon, env-verdi eller mer disk mangler, og ingen slike verdier er gjettet.
Oppfølging er registrert som **HD-0219**. Ingen vertsendring er forsøkt for å
få testen grønn.

Kilde-SHA-256 (bare de lokale syntetiske kildene):

- A: `ff242a9257e4fddc0cfdfcab62fc7993125313f0b47f1b9b037f279fabf8ed19`.
- B: `f29102ae9562f02f6f5c6924d0eb13866e2272fde4f7d806a96f6a67a6df74f8`.

## Klient- og CP-versjon brukt

- HavenAgentD PR #32, kilde `d91408bcdb4329b03bbee78fb5ec65180564ad56`.
- CP-tag `2026.9.7`, faktisk kompilert checkout
  `b4100f5734bb0b3781600845a267e424e55c0989`; pinnen er endret lokalt i både
  manifest og lockfil, uten push. Andre lockfile-pins er uendret.
- Måleflaten var en lokal Swift-driver som kaller det uendrede
  `HavenCorrespondenceMCP`-biblioteket. Den bruker separate
  `CorrespondenceIdentityVault`-instanser og klientens ordinære
  `ResolverCorrespondenceCellTransport`/autentiserte Native-bro.
  Fabrikkopprettelse bruker CP-broen med PR-klientens scopebundne proof-adapter.
  Ingen lokal serverfixture, delt privat vault eller debug-autorisasjon.
- Driveren signerer testparets innslipp direkte gjennom CPs signerings-API.
  Dette er **ikke** kjøring gjennom native godkjenningsvindu eller CLI-oppsett,
  og ikke installerakseptanse. Ingen installer er installert eller bygget her.
- Driveren fikk mer diagnostikk underveis. Hver prosesskvittering angir
  binær-SHA-256 og staging-revisjonen før kjøring. Siste driverbinær:
  `2f4b03512ab3ac895a94a03cd327f2d6728b6e73a02d72b0ac9e01f2279f4a6b`.
  Sluttkilden er bevart som `K13StagingProbe.swift`; `client-build.json`
  binder de uendrede klientbibliotekfilene med SHA-256.

## Forsøk og avgrensning

Første prosess opprettet cellen, men stoppet deretter med `Swift.DecodingError`.
Den første driveren manglet tilstrekkelig feilstedssporing. Ny lesende prosess
fant ingen ventende forespørsel. Innslipp lyktes deretter på **samme** testpar
og celle fra ny prosess; den første rotårsaken er fortsatt uavklart og ikke
rapportert som rettet (`failure-establish.json`, `inspect-*.json`).

Etter første vedleggsfeil viste lesende historikk én tekst og ingen vedlegg.
A-prøven med mer sporing gjenbrukte teksten i stedet for å sende den igjen.
Deretter ble B-retningen prøvd selvstendig. Sluttmålingen fra ny prosess fant
akkurat to tekster og ingen vedlegg for begge. Første historikkmåling er
bevart i `history-before-b/`. Opplastingsfeilene og prosessenes exit 1 er
bevart; de er ikke overskrevet med en grønn sluttdom. To lokale
kompileringsfeil i ekstra driverdiagnostikk ble rettet før kjøring;
klientbiblioteket ble ikke endret.

Ingen melding er kvittert, og ingen annen mottaker er brukt. Ingen deploy,
verts-/env-endring, SSH, omstart, merge, tag, push eller debug-bypass.
Testcellen og de to tidsbegrensede tekstene ble skrevet som oppdraget ba om.
Ufullstendige krypterte opplastinger kan ligge igjen fordi oppryddingen feilet;
vertsrydding og faktisk senere utløp er ikke kontrollert.

## /health/build ved start

HTTP 200, målt 2026-10-12T18:06:27Z. Serverens `build_timestamp` er byggtid,
ikke måletid:

```json
{
  "environment": "staging",
  "package_resolved_source": "/app/BuildMetadata/Package.resolved",
  "cellprotocol_revision": "b4100f5734bb0b3781600845a267e424e55c0989",
  "app_revision": "9ff06f8446b6331da49272f5fd72b947b4092ece",
  "dimymicropayments_revision": "fadaddbc96a3a474ff1b0fcd89a52a0eb7660c2f",
  "build_timestamp": "2026-10-10T04:50:01Z",
  "status": "ok",
  "dimymint_revision": "fbdd1b624326341e485a0cb0537a0fcff4c6b662"
}
```

## Ikke vist

Byteidentitet for mottatte vedlegg, vedleggslevering begge veier,
vedleggshistorikk og avvist henting etter vellykket tilbakekall er ikke vist.
Heller ikke push/Flow-akseptanse, native godkjenningsvindu, Touch ID/passord,
lenkeoppsett, fornyelse, vertsrestart, Intel, installer eller reelle mottakere
er prøvd. Tekst- og innslippsbevis oppfyller ikke hele PDD-en.

Læringen er anvendt i `handoff/K1-REUSABLE-NOTES.md`, post
`L-2026-10-12-k13-r2-staging-attachment-denial` (dokument følger git; ingen push).
Global læringskontroll er fortsatt rød for andre økters poster; denne posten er
ferdigbehandlet. Verdifri sluttkontroll er bevart i `verification-summary.json`. Privacy-kontrollen
fant ingen av de søkte prøveverdiene i de skannede bevisfilene eller gjenværende
private kjøreloggene; positiv kontroll slo ut. Egne private midlertidige filer,
prøvenøkler og rålogger er deretter fjernet. Delt byggcache er beholdt under
runnerens forvaltning. Se `privacy-check.json` og `cleanup.json`.

STATUS: STOPPET — vedleggsopplasting avvises med attachmentUnavailable i begge retninger; automatisk opprydding feiler, og byteidentitet/tilbakekall er ikke vist.
