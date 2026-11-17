# Codex første runde — implementasjon skrevet, ikke grønn

Gren: `codex/spillverksted-runde1`. Arbeidstre: `tmp/codex-spillverksted-r1`. Ingen merge eller utsetting. PR: https://github.com/Digipomps/CellScaffold/pull/312 (OPEN, draft). Push bekreftet; commit `12d5be6efa3dd480331eddfdb617476560bd0d07`. CI-kjøring `37991437821` er rød før checkout: Initialize containers feilet med Docker Hub unauthenticated pull rate limit. Ingen kode ble sjekket ut eller kompilert. package-release-policy er grønn. Ingen merge.

| Oppdrag (utført i denne rekkefølgen) | Skrevet | Verifikasjon / gjenstår |
|---|---|---|
| WP-E2 | GameProjectCell: persistent identityUnique metadata, ti endringer + revert, forslag/avvisning, 200 000 UTF-8-byte, ingen kjøring av kode, versjonsflyt og revisjonert pending-URL | Fire Swift-testmetoder skrevet (inkl. Workbench- og tilgangstest). Ingen Swift-test kjørt. Typesjekking og persistens ikke bevist. |
| WP-D2 | GET /spill/sandbox/:project/:version, CSP, nosniff, no-referrer, Set-Cookie-fjerning rundt sessions, feilrapportør og relative linjer. Ruten slår opp scaffold-eierens celle; kontoidentiteten må ha eksplisitt r--- på project.preview.<id>. | 8 nye mal-/CSP-tester + 6 eksisterende gamePreview-tester grønne. Tre Swift-hode-/middleware-/404-testmetoder skrevet, ikke kjørt. Levende HTTP/kontoidentitet og eksplisitt delt tilgang ikke verifisert. |
| WP-E1 | project.create bruker ProjectPortfolio.capture + WorkItem.capture til ett prosjekt og to oppgaver med samme prosjekt-id. Delvise feil rapporteres med stabile id-er. | Integrasjonstest skrevet (inngår i de fire over), ikke kjørt. Inspeksjonen i levende portefølje gjenstår. Ingen egen prosjektadministrasjon. |
| WP-C2 | GameToolLibraryCell: bundlet JSON, eksakt formål → søsken → ordtreff, matchedBy og fem grupper fra verktøyflaten. | 5 eksisterende Node-bibliotektester grønne. Bundle-kopi byte-lik original. To Swift-testmetoder skrevet, ikke kjørt. Uavhengig tjueønskers-fikstur mangler, derfor ingen T-C2-treffrate. |

## Kontrollert

- 14/14 Playwright-tester grønne på lokal Chromium. Dette bruker samme bundlete HTML-mal og CSP-streng, men starter ikke Swift-server.
- 5/5 eksisterende Node-bibliotektester grønne.
- Ni nye Swift-testmetoder inngår i ci/test-filter.txt; ingen uregistrerte testsuiter i kildebasert inventar.
- Swift syntakskontroll exit 0; dette er ikke bygg eller typesjekking.
- Explore-kildeaudit: seks statisk gjenkjente handleroperasjoner, seks komplette kontrakter, null funn. Beregnede/dynamiske nøkler er ikke runtime-verifisert av dette.
- ValueType-literalkontroll grønn; Package.resolved uendret.

## Blokkert

Swift-testkommandoen med 10 %-gulvet fra AGENTS stoppes før kompilering: se TESTRESULT.md#runde1-sluttkontroll og råloggen. Byggeskriptets lavere standard på 5 % er ikke brukt til å omgå regelen. Ingen sletting av cache eller økning av jobbtall.

T-C2 krever fiksturen fra den uavhengige skribenten. Den fantes ikke i PDD-mappen ved inventaret. Egenutformede enhetstester erstatter ikke treffratemålingen.

Katalogens template.* står to-write og har ingen kodefiler; templateId avvises med unsupported_template. Tom prosjektopprettelse og forslag er skrevet. Ingen templates er presentert som kjørbare.

Runde 2 er ikke startet. Første runde er ikke grønn eller akseptert. Ingen G3 er satt.

## Bevis og læring

Kilde, tester og råresultater ligger i arbeidstreets Documentation/Spillverksted/evidence/runde1/. Læringen om uendret iframe-URL og feilrapportørens stackramme er lagt i Documentation/Spillverksted/README.md. haven_learn capture/applied/sync/check er kjørt med arbeidstreet som isolert HAVEN_ROOT; bare dokumentmålet distribueres med Git. Global læringskanon og øvrige sjekkouter er ikke endret.

Uavhengig kilde-/beviskontroll gjennomført. Den fant loader-navnekollisjon, som er rettet med IIFE og testet i siste 14/14-kjøring; ny kontroll bekreftet rettingen og kildehashene. Ingen runtime/typer/persistens ble bevist av kontrollen.

CI-bevis: https://github.com/Digipomps/CellScaffold/actions/runs/37991437821. Ingen manuell nykjøring eller endring av container/credentials.
