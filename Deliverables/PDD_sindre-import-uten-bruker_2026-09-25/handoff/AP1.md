STATUS: STOPPET — Etter-tester og grønn CI er ikke ferdige innen ventetidsgrensen på 60 minutter; lokalt Swift-bygg er blokkert av diskvakten.

Oppdatert: 2026-09-26 18:48 UTC.

Arbeid: `PDD_sindre-import-uten-bruker_2026-09-25` AP1, formål `…katalogen-virker`.
Eier: Codex. Integrator: Losen. G2-godkjenning: Kjetils oppdrag 2026-09-26.
Repo/worktree: `CellScaffold/_wt-pub-katalog-20260926`.
Base: `ea8949911bc0ee8fb754e1b8946d573f7584f9d0` (`origin/main` etter fetch).
Gren: `pdd/pub-katalog-500`.
PR: https://github.com/Digipomps/CellScaffold/pull/266
Sluttcommit: `7599ac3eda642f92543e42bbdeee21c34719e0e7`, pushet og kontrollert med `git ls-remote`.
Ingen merge eller utrulling er utført.

Årsak (kildelest mot urettet `ce2b3e1e`, samme Publication-kode i målt prod `18c14c32`):

- `Sources/App/Controllers/VaporPublication.swift:206` slår opp `cell:///Publication`, ikke en annen katalogcelle. `Sources/App/configure.swift:1295` og `:1371` registrerer `PublicationCell` som scaffold-unik og persistent. Ruta binder en lokal signerende eier på `VaporPublication.swift:209` og leser `publicDirectory` på `:44`.
- `Sources/App/Cells/Publication/PublicationCell.swift:119`–`:123` starter ved dekoding en ikke-avventet `Task` som forsøker eierhydrering og `setupKeys`. Cellen overstyrte ikke `installCellRuntimeBindingsForAccess`, så resolverens avventede readiness-steg installerte ingen Publication-handlere.
- `Sources/ScaffoldKit/PaymentGateOwnerIdentitySupport.swift:371`–`:373` avviser hydrering når den lagrede vault-referansen ikke stemmer. `signingIdentity(for:)` på `:44`–`:53` faller da tilbake til den usignerte eierbeskrivelsen. `GeneralCell.isAllowedToSetupIntercepts`, `CellProtocol/Sources/CellBase/Cells/GeneralCell/GeneralCell.swift:2300`–`:2313` (prod-pin `473357cf`), avviser registrering uten eierbevis når kallet ikke skjer under runtime-installasjonstokenet.
- Det finnes ingen ny registrering etter at ruta binder eieren. Derfor kan autorisasjonen lykkes, men GET-handleren fremdeles mangle og gi `KeyValueErrors.notFound` → HTTP 500. `publicDirectory` fantes allerede i første Publication-commit `83f0e364`; dette er ikke et nytt datafelt som mangler i eldre JSON.
- Den offentlige eierbeskrivelsen (`GeneralCell.swift:348`, `Identity.publicIdentitySnapshot`) fjerner vault-referansen. Det forklarer hvorfor rutens senere lokale eieroppslag kan lykkes mens Publication-dekoderens separate, lagrede eierbeskrivelse ikke lot seg hydrere.

Produksjonsevidens: nytt anonymt GET `/pub` i denne kjøringen ga HTTP 500. GET `/health/build` viste app `18c14c32cb6e2957c1d13a20a4b2d97ece2f02b6`, CellProtocol `473357cf4efee831cb3b55ae87bc921d4bb63c10`. Et avgrenset, skrivebeskyttet loggsøk viste fortsatt Publication-mappingen fra diagnosen 24.09. Krypterte produksjonsdata og den konkrete lagrede vault-referansen er ikke inspisert. Den gamle vault-referansen er en kontrollert reproduksjon av kodefeilen, ikke en påstått måling av produksjonsmetadata. Endelig prod-akseptanse krever utrulling og nytt HTTP-kall.

Rettingen: `Sources/App/Cells/Publication/PublicationCell.swift:119`–`:125` installerer alle kontrakter og GET/SET-handlere gjennom den eksisterende `installCellRuntimeBindingsForAccess()`-hooken. Nye celler avventer `ensureRuntimeReady()` på `:101`; dekoding starter ingen bakgrunnsoppgave. Resolveren og GET/SET avventer samme instansbundne installasjon. Normal requester-autorisasjon beholdes. Det er ingen catch som skjuler feilen, ingen datanullstilling og ingen endring i CellProtocol.

Testene ligger i `Tests/AppTests/PublicationCellTests.swift:34` og `:38`, i suiten som allerede står i `ci/test-filter.txt:195`. De serialiserer og dekoder cellen, bevarer UUID og publisert innhold, modellerer en gammel vault-referanse, registrerer den gjenopprettede cellen på den ekte resolveren og kaller den ekte HTTP-ruta. De krever 200 både med katalogførte sider og tom katalog, utelukker utkast/ikke-katalogførte sider, gjentar GET, kontrollerer frontsidens SET-lesehandler og avviser en usignert requester. `debugValidateAccessForEverything` slås eksplisitt av; eksisterende suite bruker ellers en debug-bypass som skjuler registreringsfeilen.

Før-kjøring: https://github.com/Digipomps/CellScaffold/actions/runs/36260514376, testcommit `ce2b3e1e21759a136774ac206bbb52d64671c787` uten retting.
Etter-kjøring: https://github.com/Digipomps/CellScaffold/actions/runs/36261749462, sluttcommit `7599ac3eda642f92543e42bbdeee21c34719e0e7`.


Før-resultatet er målt: de to nye testene feilet, og hver av dem fikk HTTP 500 to ganger med samme feilklasse som i prod. Ordrette linjer fra jobb `108455295086`:

```text
2026-09-26T18:29:45.5117629Z 2026-09-26T18:29:45+0000 warning codes.vapor.application: method=GET request-id=F6EB56DF-3349-4B58-9260-8ED85283A2E0 url=/pub userAgent=[] [Vapor] CellBase.GeneralCell.KeyValueErrors.notFound
2026-09-26T18:29:45.5119512Z AP1 restored directory sites=false: HTTP 500
2026-09-26T18:29:45.7851147Z AP1 restored directory sites=true: HTTP 500
2026-09-26T18:29:45.7837852Z Test Case 'PublicationCellTests.testRestoredDirectoryReturns200WhenEmptyAndOwnerIsDetached' failed (0.229 seconds)
2026-09-26T18:29:45.8532588Z Test Case 'PublicationCellTests.testRestoredDirectoryReturns200WithPublishedPagesAndDetachedOwner' failed (0.285 seconds)
```

`PublicationCellTests`: 11 tester, 18 assertion-feil, 0 uventede feil; bare de to nye testene feilet. `PublicationPublicSurfaceTests`: 8 tester, 0 feil. To av assertion-feilene kom fra forhåndssjekken omtalt nedenfor. Bygget før rettingen bestod: `Build complete! (1742.84s)`.

Hele før-workflowen har status `cancelled`, ikke `success` eller `failure`: jeg avbrøt den for å slippe sluttkjøringen frem i køen. En delvis loggnedlasting var forsinket og viste først ikke Publication-testene; den fullstendige loggen dokumenterer dem på 18:29:45 UTC, før avbrytelsen 18:34:35 UTC. Det er derfor ikke påvist at Porthole-testen hang.

Etter-resultat ved avsluttet CI-venting 2026-09-26 18:48 UTC: kjøringen er fortsatt `in_progress`, steget `Build every target`. Ingen etter-testutdata foreligger, og grønn CI er ikke bekreftet. Ordrett terminal statuskontroll:

```json
{"conclusion":"","headSha":"7599ac3eda642f92543e42bbdeee21c34719e0e7","jobs":[{"conclusion":"","currentSteps":["Build every target"],"name":"Focused control-plane gates","status":"in_progress"}],"status":"in_progress","url":"https://github.com/Digipomps/CellScaffold/actions/runs/36261749462"}
```

Bare ventingen er avsluttet; sluttkjøringen fortsetter på GitHub. PR-en er kontrollert `OPEN`, `isDraft: true`, med eksakt slutt-SHA som over. AP1 kan ikke merkes LEVERT før de nye testene faktisk passerer og CI-status er grønn. Neste integrator leser resultatet fra den samme kjøringen, retter eventuelle relevante feil og oppdaterer rapporten; ingen merge er autorisert.

For å være presis om testendringene: sluttcommiten korrigerer også en forhåndssjekk til å bruke den faktisk lagrede eierbeskrivelsen, fremfor `storedOwnerIdentity` som allerede har fjernet vault-metadata. HTTP-assertene er uendret. Før-kjøringens to ekstra feil i den forhåndssjekken skal ikke regnes som bevis for HTTP-feilen.

Lokale kommandoer ble forsøkt gjennom den påkrevde wrapperen, før og etter rettingen:

```sh
HAVEN_BUILD_MIN_FREE_PERCENT=10 scripts/run_swift_bounded.sh build
HAVEN_BUILD_MIN_FREE_PERCENT=10 scripts/run_swift_bounded.sh test --filter 'Publication(Cell|PublicSurface)Tests'
HAVEN_PYTHON=/usr/bin/python3 ci/check-value-literals.sh
```

Bygg/test ble stoppet før kompilering. Første forsøk:

```text
Build capacity: 42.0 GiB free (4%); reserving 10 GiB leaves 32.0 GiB (3%).
ERROR: build blocked: projected free space must remain at or above 40 GiB and 10%.
```

Etter-forsøk:

```text
Build capacity: 43.9 GiB free (4%); reserving 10 GiB leaves 33.9 GiB (3%).
ERROR: build blocked: projected free space must remain at or above 40 GiB and 10%.
```

Ingen lokal Swift-test hevdes bestått. Diskvakten er ikke omgått og ingen opprydding er gjort. Literal-sjekken og `git diff --check` bestod:

```text
ValueType-literaler over 20 oppfoeringer: 23 | dekket av baseline: 23
OK: ingen ValueType-literal er stor nok til aa velte typesjekkeren.
```

Lokale kjørelogger: `/private/tmp/ap1-pub-evidence/`. Kildeendringens dokumentasjon er `Documentation/Publication_Runtime_Restore.md` i PR-en. De allerede skitne hovedarbeidstrærne er bevart; rapporten er en lokal fil i dokumentrepoet. Sluttcommiten inneholder begge påkrevde Claude-trailere.
