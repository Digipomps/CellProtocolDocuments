# OIW — gjenopptaking etter første byggstopp

Dato 2026-10-05. Les STATUS, ACCEPT og TESTRESULT først. Alle WP0–WP10 og design er godkjent av Kjetil; G3 er ikke gitt. Arbeidet skal fortsette uten ny design-/planrunde.

## Før neste kjøring

1. Les Kjetils eventuelle svar på spørsmålet om automatisk retting og ny testing. Spørsmålet ble stilt etter første mislykkede bygg; ingen svar forelå da dette notatet ble skrevet. Uten svar skal samme mislykkede sjekk ikke kjøres igjen, jf. PDD A11. Unngå gjentatte spørsmål.
2. Worktree er `CellScaffold/.worktrees/oiw-conference-20261005`, låst mot prune, gren `codex/oiw-conference-20261005`, base `e5c3434510884275cae4a732935ab4b55cf7fad9`. Alt kandidatkodearbeid ligger ukommittert der. Ikke bruk shared primary eller overskriv andre tråders arbeid. Package.resolved er ikke endret.
3. Les `_losen-queue/KOORDINERING.md`, gjeldende git-/diskregler og mål ledig plass på nytt. Bruk samme bounded-runner og delt lease; ingen GC/cleanup. Første bygglease ble frigitt da kommandoen avsluttet.
4. Etter tillatelse: bygg/test begge nye suitene og relevante eksisterende publisher-regresjoner, deretter nødvendige integrasjons- og fullregresjonssjekker. Ikke svekk eller endre committede tester uten konkret godkjenning. Logg nye kjøringer separat; bevar `evidence/first-build.log`.

## Kilde og bevis

`evidence/candidate-manifest.json` lister de berørte filene med SHA256 og 21 testmetoder. Manifestet dokumenterer kildeinventar, ikke beståtte tester. Foundation.DecodingError-feilen er rettet, og en rekke senere rettelser er aldri kompilert. Modell/policytester alene kan ikke bevise Cell/HTTP/cryptographic transport/persistens/GUI.

Lokal bygge-wrapper ble laget i midlertidig område med innholdet nedenfor. Gjenskap ved behov, men først etter testtillatelse. `--dry-run` slår bare av cache-GC:

```sh
#!/usr/bin/env bash
exec "$HAVEN_ROOT/CellProtocol/Scripts/haven-swiftpm.sh" --dry-run "$@"
```

## Åpne forhold som ikke må forsvinne i et grønt modellbygg

- WP1/2/3: faktisk resolver/HTTP, korrekt lagringsfeil og restart, publikumsavgrensning, per-tab form-/versjonsisolasjon og full brukerreise. Dagens lokale intention-matcher erstatter ikke den gamle faste recommendation-listen. Rettelsesmodell finnes, men UI sender foreløpig ingen supersedes.
- Snapshot-usikkerhet sperrer skriving og privat lesing og beholder kandidat ved encoding; operativ gjenoppretting er ikke implementert. Bakgrunnssletting av utløpt møtemateriale mangler.
- Godkjenningsknapper sender nå eksplisitt mål/versjon og relevant publikum. Dette må prøves i flere samtidige faner med reelle handlinger; statisk JSON er ikke tilstrekkelig.
- WP4: ingen provider kalt. Bruk faktiske Cell-use grants, synlig datavei og avgrenset budsjett.
- WP5: gjenbruk eksisterende Bridge-ingressarbeid; rådgiverrapporten peker på egne kandidater. Ren CP scanner-oppfølging er 14181968c8998c4543b42282c3559bc74ed6bddc; dagens stabile avhengighet er før PR53. Ikke løft gamle pins blindt. Mottakerlokal autoritet, idempotent kvittering og restart må vises.
- WP6: **ikke kjør `/private/tmp/oiw-company-candidate.py`**. Den er ubrukteksperiment med kritiske feil dokumentert i `evidence/oiw-company-review-20261005.md`. Bare read-policy/additive felt/ny creator-binding er brukt. Monoton medlemsledger, alle-skrivere-fence, persistence/read-back, trygg migrering og siste gyldige admin kreves.
- WP7/8: ingen faktisk web/native GUI kjørt; ingen mikrofon. Gjenbruk nyere Tree/List og faktiske executionRequesterIdentity-paths. Etter OS permission await må plan/epoch kontrolleres på nytt umiddelbart før capture. Nearby må vise reelle invitationID/decisionID og testes med to fysiske enheter.
- WP9: eksisterende admin/Swarm lifecycle finnes; domeneexecutor og semantiske kvitteringer gjør ikke det i denne kandidaten. Fixture-seed alene gir ikke identitetsreplay eller bevist opprydding.
- WP10: runbook og syntetisk fixture er forberedelse. Ingen gjester invitert, ingen pilotresultater, ingen G3.

## Midlertidig preview og patch-skript

En statisk fixture-preview ble forberedt i `/private/tmp/oiw-conference-preview-20261005` og en loopback HTTP-server startet på port 9866. Den ble aldri åpnet/verifisert. Serveren skal stoppes ved kontrollpunkt; se `evidence/preview-cleanup.txt` for faktisk resultat. Ingen PNG fra ny runtime finnes.

Tidligere Python patch-skript i `/private/tmp/oiw-*.py` er engangsskript og skal ikke blindt kjøres om igjen; flere er ikke idempotente og kan overskrive senere rettelser. Aktuell worktree er kilden.

## Læring og koordinering

Læring L-2026-10-05-godkjenningsknapper-ma-sende-eksplisitt-mal er fanget, canonical cellconfiguration-skeleton-authoring oppdatert, applied og sync fullført. Global strict learning-check viste andre tråders tidligere backlog; ikke rapporter global kø grønn eller ta eierskap til deres læringer.

Ingen commit, push, PR, paid CI eller deploy er utført i denne tråden. Andre tråders deploy/hostclaims må fortsatt leses ferskt før noen senere deploy.

## Avsluttet kontrollpunkt

Uavhengig dokumentkontroll er bevart i `evidence/document-review.md`; kontrollens eksakte dokumenthash står der. ACCEPT/TESTRESULT er ikke endret etter kontrollen. WP6: ikke tolk faktisk delmengde som rådgiverens sikkerhetsgodkjenning; både creator-binding og Commons strict-switch var utover opprinnelig anbefaling. Previewprosessen er avsluttet; opprinnelig exec returnerte 143 etter SIGTERM. Kilde eller teststatus er ikke endret. Disse gjenopptakingsopplysningene er lagt til etter dokumentkontrollen.
