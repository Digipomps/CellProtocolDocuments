# k13 — staging-testpar: stoppet før opprettelse

Målt 2026-10-11 mot `https://staging.haven.digipomps.org` fra Codex med lokal shell. **Staging har riktig kode, men korrespondanseverten er ikke konfigurert.** Oppdragets stoppregel for nødvendige verts-/miljøendringer er utløst. Ingen identiteter, profiler eller relasjoner ble opprettet; ingen meldinger eller vedlegg ble sendt. Ingen eksisterende personprofiler eller innbokser ble åpnet.

Alle bevisstier under er relative til HAVEN-roten. Bevisene ligger i `HAVEN-Deploy/_handoff/KORR-UT/k13/`; `SHA256SUMS` binder de fire bevisfilene.

| Steg | Utfall | Bevis |
| --- | --- | --- |
| Start: staging-revisjon | BESTÅTT: CellScaffold `9ff06f8446b6331da49272f5fd72b947b4092ece`, CP `b4100f5734bb0b3781600845a267e424e55c0989`, miljø staging. | `HAVEN-Deploy/_handoff/KORR-UT/k13/health-build-start.json` |
| Start: korrespondansevert | STOPP: HTTP 200, global `status=ready`, men `correspondence.configured=false`, `ready=true`, `storageAvailable=false`. | `HAVEN-Deploy/_handoff/KORR-UT/k13/health-ready-start.json` |
| Start: disk og klient | Diskvakt grønn: 90,8 GiB ledig, 80,8 GiB / 8 % etter 10 GiB reserve. Klientkilden funnet; ingen bygg eller kjøring etter vertsblokkeringen. | `HAVEN-Deploy/_handoff/KORR-UT/k13/preflight.json` |
| 1. A oppretter relasjonscelle over autentisert bro | IKKE KJØRT: relasjonsfabrikken er ikke installert i applikasjonen. | `HAVEN-Deploy/_handoff/KORR-UT/k13/source-evidence.md` |
| 2. B ber om innslipp; A sammenligner sekssifret kode og godkjenner | IKKE KJØRT: stopp før prøveidentitetene ble opprettet. | `HAVEN-Deploy/_handoff/KORR-UT/k13/preflight.json` |
| 3. Tekst og vedlegg over 1 MB begge veier; SHA-256-byteidentitet | IKKE KJØRT. Ingen vedleggs- eller meldingsbevis. | `HAVEN-Deploy/_handoff/KORR-UT/k13/preflight.json` |
| 4. Historikk fra ny klientøkt for begge | IKKE KJØRT. | `HAVEN-Deploy/_handoff/KORR-UT/k13/preflight.json` |
| 5. Tilbakekall vedlegg; henting avvises | IKKE KJØRT. | `HAVEN-Deploy/_handoff/KORR-UT/k13/preflight.json` |

## Hva som mangler

En aktiv korrespondansevert med vedvarende lagringsrot på staging. I eksakt deployet kilde kaller `Sources/App/configure.swift:2636` alltid `CorrespondenceRelationshipHost.install`. Denne returnerer uten å registrere fabrikken når `HAVEN_CORRESPONDENCE_DATA_ROOT` mangler (`Sources/App/Services/CorrespondenceRelationshipHost.swift:283`). `/health/ready` bruker nettopp kombinasjonen `configured=false, ready=true, storageAvailable=false` når `app.correspondenceHost` er nil (`Sources/App/routes.swift:242`). Dette knytter det observerte svaret til deaktivert hosting; verts-env er ikke lest direkte.

Før en ny prøve må operatøren konfigurere `HAVEN_CORRESPONDENCE_DATA_ROOT` til en privat, vedvarende og skrivbar katalog i applikasjonen og aktivere den ved oppstart. Kilden krever også ordinær vertsidentitet, gyldig bro-origin og minst 10 000 000 000 frie byte ved opprettelse/opplasting. Disse forutsetningene er ikke kontrollert på verten her. Ingen konkret katalogverdi er gjettet. Ingen invitasjonsverdi er hentet eller forsøkt. Innslippet i oppdraget er relasjonscellens eiergodkjenning; den eldre HTTP-innmeldingsveien er ikke brukt som erstatning.

Ingen vertsendring, env-endring, omstart, deploy, merge, tag, push eller debug-bypass er utført. Et klientbygg kan ikke aktivere den manglende relasjonsverten, og ble derfor ikke startet etter stoppfunnet.

## Klient- og CP-versjon

- Identifisert klientkilde: HavenAgentD PR #32, `d91408bcdb4329b03bbee78fb5ec65180564ad56`, eksisterende låst arbeidstre `_worktrees/havenagentd-korr-klient-20261007`.
- Klientens manifest og lockfil peker fortsatt på CP `97b348483448fb29dfe089bd96ab4d4adb384a76`. Ingen klientbinær ble brukt mot staging. **Lokal pinning til CP-tag `2026.9.7` og bygg er ikke utført**, fordi stoppfunnet kom før dette. Det gjenstår ved en ny prøve.
- Faktisk CP på staging: `b4100f5734bb0b3781600845a267e424e55c0989` (utgivelsens tag `2026.9.7`). Faktisk CellScaffold: `9ff06f8446b6331da49272f5fd72b947b4092ece` (utgivelse `2026.10.4`). SHA-ene er lest live; tagnavnene samsvarer med utgivelsesoverleveringen.
- k9-installerpakken er ikke installert eller brukt, og denne rapporten gjør ingen ny påstand om installerakseptanse.

## /health/build ved start

Følgende er startsvaret, også bevart som egen JSON-fil. `build_timestamp` gjengis som serveren returnerte det; det er ikke tidspunktet for denne målingen. Første curl brukte `--fail` og avsluttet med 0; numerisk HTTP-status ble ikke skrevet for dette kallet. `/health/ready` skrev eksplisitt HTTP 200.

```json
{"status":"ok","cellprotocol_revision":"b4100f5734bb0b3781600845a267e424e55c0989","build_timestamp":"2026-10-10T04:50:01Z","environment":"staging","dimymint_revision":"fbdd1b624326341e485a0cb0537a0fcff4c6b662","package_resolved_source":"/app/BuildMetadata/Package.resolved","dimymicropayments_revision":"fadaddbc96a3a474ff1b0fcd89a52a0eb7660c2f","app_revision":"9ff06f8446b6331da49272f5fd72b947b4092ece"}
```

## Ikke vist

Ingen av de fem ende-til-ende-stegene er vist. Generell readiness og en autentisert bro som melder `ready` er ikke bevis for relasjonsopprettelse, innslipp med kode, levering/dekryptering, SHA-256-byteidentitet, historikk i nye økter eller avvist henting etter tilbakekall. Heller ikke native godkjenningsvindu, Touch ID, installerakseptanse eller vertsrestart er prøvd. Rapportens SHA256SUMS gjelder bevisfiler, ikke overførte vedlegg.

Læringsfangst: preflight-funnet er anvendt i `handoff/K1-REUSABLE-NOTES.md`, post `L-2026-10-11-staging-health-ready-kan-vaere-gronn-mens`. Dokumentmålet følger git; ingen push er utført. Global `haven_learn.py check --strict` er fortsatt rød med 7 eldre åpne og 31 eldre usynkede poster; k13-posten er ferdigbehandlet.

STATUS: STOPPET — korrespondanseverten er deaktivert på staging; HAVEN_CORRESPONDENCE_DATA_ROOT må konfigureres og hosting aktiveres før testparet kan kjøres.
