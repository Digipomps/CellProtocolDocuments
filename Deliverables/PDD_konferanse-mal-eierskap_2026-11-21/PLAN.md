# Plan — konferanse mal og eierskap (fase 1)

Formålsspesifikasjon: `Deliverables/PDD_konferanse-mal-eierskap_2026-11-21/FORMAALSSPEC.md` (G1 godkjent 21.11.2026).
Lanebilde: `images/plan-v1.png`.

## Dette skal du gjøre

| Når | Hva | Hvorfor |
|---|---|---|
| Nå | Si «G2 godkjent», eller hva som skal endres | Ingen kode før planen er godkjent |
| Etter WP1 | Si «Slipp inn» for byggejobben i køen på Macen (WP1 og WP3) | Nye byggejobber går bare inn på ditt ord |
| Hvis WP1 viser stille tap | Velg: cellen lagrer uregistrerte stier (anbefalt), eller avviser dem høyt | Det er en endring i EntityAnchor, og den er din å velge (§6 spørsmål 2) |
| Når utkastet ligger i tråden | Les brevet til Vegar og si «send» | Brev ut av prosjektet sendes bare på ditt ja |
| PR-ene er åpne | Merge | Losen merger ikke |
| G3 | Les ACCEPT.md og si «G3 godkjent» | Aksept mot forventningskontrakten |

## Arbeidspakker

Én pakke per bladformål, i rekkefølge. Utførende: **Losen** (Claude i skyen, skriver i CellProtocolDocuments og CellScaffold via PR), **Kø** (skript eller Codex på Kjetils Mac, bare etter «Slipp inn»), **Kjetil**.

| WP | purposeRef | Hva | Utfører | Test som skal bli grønn | Artefakt (§3) |
|---|---|---|---|---|---|
| WP1 | …lagring | Les `ConferenceEntityRelationBridge.swift`, `ConferenceEntityPersistenceBridge.swift` og finn EntityAnchor-implementasjonen. Skriv én test som skriver en uregistrert sti og leser den tilbake. Kjør den i køen | Losen skriver, Kø kjører | test.kme.lagring-rundtur (måling: verdi, feil eller stille tap) | TESTRESULT.md#lagring |
| WP2 | …arrangor, …eierskap, …mal-v0, …utvidelse, …deltakerpost | Kontrakten `Book/conference_entity_template_v0.json`: arrangør (v2 `groups`-form), arrangement (`event.ownedBy`, `event.partOf`, `template.ref/version`), malen v0 med faste og reserverte stier, utvidelser og forslag (samme form som `person.attributes[].promotedTo`), deltakerens `conference.<uuid>` med bare referanser. Gyldige og ugyldige fixtures. Validator i ren Python | Losen | test.kme.arrangor-*, eierskap-*, mal-validator, utvidelse-*, deltakerpost-* | `contract/`, `checks/validate_contract.py`, TESTRESULT.md#contract |
| WP3 | …kode | `ConferenceDefinition`: valgfri `ownerEntityRef` og `templateRef`, med enhetstest for dekoding med og uten. PR til CellScaffold; bygg og hele testmengden i køen med den lokale gaten (#490) så lenge CI-budsjettet er tomt | Losen skriver, Kø bygger | test.kme.swift-dekoding, test.build, test.regression | CellScaffold-PR, TESTRESULT.md#build |
| WP4 | …lagring | Bare hvis WP1 viser stille tap: retting i EntityAnchor etter ditt valg, med testen fra WP1 som bevis. Egen PR | Losen skriver, Kø bygger | test.kme.lagring-rundtur grønn | PR, TESTRESULT.md#lagring |
| WP5 | (pkg.std.everything-works) | Book 37: konferanse-entitet, arrangør, mal og deltakerpost; «Last verified against code» | Losen | test.docs-updated | ACCEPT.md#docs |
| WP6 | …svar-vegar | Brevutkast til Vegar, ett avsnitt per forslag, med lenke til kontrakten fra WP2. Legges i tråden | Losen, så Kjetil | test.kme.svar-vegar | sendt brev med messageID |
| WP7 | alle | TESTRESULT.md, ACCEPT.md, lærdommer, STATUS | Losen | test.status-current | ACCEPT.md |

WP2, WP5 og WP6 venter ikke på WP1. WP3 og WP4 går til køen og venter på «Slipp inn».

## Dataflyt

| Kant | Kontrakt |
|---|---|
| konferanse `event.ownedBy` → arrangør-uuid | `conference_entity_template_v0.json#/$defs/Event` |
| arrangør → liste over arrangementer | bygges ved dekoding fra `event.ownedBy`, lagres ikke |
| konferanse `template.ref`/`version` → mal | `#/$defs/Template` |
| deltaker `conference.<uuid>` → konferanse-entitet og EntityRepresentasjoner | `#/$defs/ParticipantSlice`, bare referanser |
| utvidelse brukt av flere → forslag til mal | `#/$defs/TemplateProposal` |

## Stoppregler

- Enhver committet test som må endres, også en Losen skrev samme dag: stopp og spør Kjetil.
- En rød sjekk i køen, også når kallet aldri kom fram: stopp, si fra, ikke kjør igjen uten Kjetils ord.
- Ingen bygg på verten. Ingen endring i prod eller staging i denne fasen.
- Brev til Vegar sendes ikke før Kjetil har sagt «send».
