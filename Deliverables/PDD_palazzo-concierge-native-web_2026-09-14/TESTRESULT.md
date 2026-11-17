# TESTRESULT — Palazzo concierge native web

2026-09-14 · Astra (Codex) · WP0–WP4: **skrevet, verifisert med full regresjon**.
Native arm64-bygg: grønt. Full `swift test`: **116 XCTest-tester, 0 feil, exit 0**, med det eksplisitte lokale arkitekturvalget nedenfor. WP5 (selvstendig oppstart og visuell paritet) er ikke utført her.

Arbeidsgrunnlaget er filene i HAVEN-arbeidsområdet, ikke en kontrollert upstream-revisjon. Ingen git-kommandoer eller nettverkskall er utført. Ingen endringer er gjort under `CellProtocol/` eller `CellScaffold/`. Førbildet av PalazzoScaffold-filene ligger i [wp0-files.json](evidence/wp0-files.json).

## build

Kjørt i `PalazzoScaffold` før og etter implementeringen:

```sh
swift build --disable-sandbox --disable-automatic-resolution --skip-update
```

| Måling | Faktisk resultat | Rålogg |
|---|---|---|
| WP0 før endring | exit 0; Build complete, 15,47 s | [wp0-build.log](evidence/wp0-build.log) |
| WP4 native arm64 | exit 0; Build complete, 11,38 s | [wp4-build.log](evidence/wp4-build.log) |

De ekstra oppløsningsflaggene bruker allerede tilgjengelige avhengigheter og unngår oppdatering. Det ble ikke endret pakkeversjoner eller manifest. SwiftPM varsler om skrivebeskyttet delt manifest-cache og to eksisterende test-fixtures uten ressursdeklarasjon; begge bygg fullførte. En tidlig kompileringsfeil i den nye controllerens header-literal ble rettet; råloggen beholdes som `wp1-build.log`.

## regression

Forventet baseline var omtrent 105 tester (rapport fra 2026-09-08). Målt baseline var **105 XCTest-tester**; avsluttende kjøring er **105 eksisterende + 11 nye = 116**. Ingen eksisterende tester er endret, fjernet eller filtrert bort.

| Kjøring | Faktisk resultat | Evidens |
|---|---|---|
| WP0 `swift test --disable-sandbox` med offlineflagg | exit 1; ingen XCTest-tester startet: pakken er arm64, lasteren krever x86_64 | [første](evidence/wp0-test.log), [gjentakelse](evidence/wp0-test-repeat.log) |
| WP0 `arch -arm64 swift test …` | samme lasterfeil, exit 1 | [logg](evidence/wp0-test-arm64.log) |
| WP0 direkte arm64-XCTest, to kjøringer | 105 tester; én eksisterende omstartstest feilet med to assertions fordi dens xcrun-underprosess krevde x86_64 | [første](evidence/wp0-xctest-arm64.log), [gjentakelse](evidence/wp0-xctest-arm64-repeat.log) |
| WP4 direkte arm64-XCTest, nye fasadetester | 11 tester, 0 feil | [logg](evidence/wp4-facade-second.log) |
| WP4 `swift test`, eksplisitt x86_64 | alle 116 XCTest-tester grønne, deretter krasj i den tomme Swift Testing-kjøreruten på arm64 | [logg](evidence/wp4-test-x86_64.log) |
| **WP4 avsluttende full `swift test`** | **116 tester, 0 feil, exit 0**; også omstartstesten er grønn | [rålogg](evidence/wp4-regression.log), [kommando/exit](evidence/wp4-regression.json) |

Avsluttende kommando i `PalazzoScaffold`:

```sh
swift test --disable-sandbox --disable-automatic-resolution --skip-update --triple x86_64-apple-macosx13.0 --disable-swift-testing -j 4
```

Alle prosjektets tester bruker XCTest. [Statisk kontroll](evidence/static-audit.json) teller 116 testmetoder og finner ingen Swift Testing-tester. `--disable-swift-testing` slår derfor av en ubrukt kjørerute; den fjerner ingen tester. Kommandoen har verken `--filter` eller `--skip`. Dette er et lokalt verktøykjedevalg. Standard arm64-`swift test` er fortsatt **blocked** av den dokumenterte lasterfeilen; full regresjon er verifisert med x86_64-kommandoen. [KJOR-SELV-build.sh](handoff/KJOR-SELV-build.sh) gjentar den kontrollerte bygg-/testkombinasjonen.

De 20 eksisterende `PalazzoConciergeTests` er grønne i den fulle kjøringen. Den avsluttende kjøringen omfatter også den eksplisitte produksjonstesten uten Authorization. Tidlige feil i nye testhjelpere (XCTVapors normalisering av Content-Length, JSON-escaping og et typenavn) er rettet; mellomlogger beholdes i [run-summary.json](evidence/run-summary.json).

## public-ask

`testPublicAskReturnsAllFiveCitedPizzasWithoutCredentials` kjører den virkelige HTTP-ruten gjennom XCTVapor, resolver, husets identitet og bundlet `PalazzoConciergeCorpusCell`.

`POST /palazzo/api/ask {"query":"Hvilke pizzaer har dere?"}` → **200**, `status: answered`, `route: native`, `citation_count: 1`, `last_verified: 2026-06-03`, med alle fem pizzanavn. [Faktisk svar](evidence/responses/public-ask.json). Samme forespørsel er også kjørt uten noen Authorization/principal i produksjonsmodus med gateway-token satt: [produksjonssvar](evidence/responses/production-anonymous-ask.json).

Ingen Python-tjeneste, språkmodell eller HTTP-transport til CellScaffold inngår i denne svarbanen.

## envelope

`testEnvelopeStateAndConfigurationHavePublicTypesAndDatedCorpusStatus` og felles assertions kontrollerer nøyaktig feltsett og typer for ask/menu/beverages:

`answer audience citation_count citation_summary citations confidence last_verified needs_human_review route schema status warnings reason_code`.

`schema` er `haven.palazzo.communale.guest-concierge.v1`; `route` er `native`; audience låses til `guest`. Alle kilder har offentlig tittel, aktiv status og gyldig dato. Feilformat, ugyldige datoer, streng i stedet for bool, interne audiences, kandidat-/ukjente kilder, utrygge URL-er og ukjente sikkerhetsadvarsler stopper publisering.

Evidens: [meny](evidence/responses/envelope-menu.json), [drikke](evidence/responses/envelope-beverages.json), [state](evidence/responses/state.json), [configuration](evidence/responses/configuration.json).

State har alle de avtalte feltene og riktige typer, `remoteMode: PalazzoConciergeCorpus (native)` og `serviceStatus: limited` når bundlet korpus er lastet (`unavailable` i kodebanen for manglende korpus). `serviceMessage` henter datoen fra cellens `guestReadyScope.last_verified`; teksten sier at grunnlaget er datert. Meldingen bevares også etter at JS viser et svar. Tellerne lagrer ikke spørsmål eller svar. Kunnskapscellens eksisterende lokale hendelser er dokumentert separat fra fasadens lagring.

`configuration` gir webmetadata med navn, apiBase, flate og tre handlinger. Den gamle CellScaffold-rutens Porthole-CellConfiguration er ikke portert: Porthole-skjelett er utenfor denne slicen, og webklienten bruker ikke den gamle skeleton-konfigurasjonen. Validerings-/rate-feil beholder `{error, reason}` med norsk tekst; de er ikke kunnskapssvar.

## auth

`testAuthBoundaryInProductionIgnoresForgedFacadePrincipalAndProtectsGenericAPI` bekrefter:

- Produksjonsmodus med token satt: offentlig ask uten Authorization → **200**; state/configuration → **200**.
- Falsk Authorization, staff-principal, audience, endpoint og keypath i offentlig inndata gir ingen styring over cellekallet.
- `POST /api/cell/get` uten token, med husprincipal → **401**; med riktig token → **200**. `/api/concierge/ask` uten token → **401**.
- Offentlige refresh/sources/booking/audit/claim/cell-get-ruter finnes ikke → **404**.
- 30 POST-forsøk tillates; ugyldige spørsmål teller også. Forsøk 31 på en annen offentlig handling → **429 + Retry-After**. Første X-Forwarded-For-verdi bestemmer klienten; ny klient får egen kvote. Remote-address-fallback, tomt første forwarding-felt og utløp etter 600 sekunder er testet.
- Faktisk body og oppgitt Content-Length over 4096 byte → **413** for alle tre handlingene. Gyldig JSON på nøyaktig 4096 byte → **200**. 1201 tegn eller Unicode-body over bytegrensen → **413**. Ugyldig JSON og feil medietype får norske feil.

Offentlig ingress/nginx må overskrive klientstyrt `X-Forwarded-For`. Grensen er per appinstans, ikke en distribuert kvote. Ingen resolver-/gateway-policy er endret. Innkommende HTTP med streaming-body har `collect(maxSize: "4kb")`; TCP/stream-transport ble ikke kjørt her, mens allerede innsamlet body og deklarert lengde ble testet via appens responder.

## leaf

`testLeafAndEveryReferencedStaticAssetAreServedFromPublic` bekrefter **200** for `/palazzo`, JS, CSS, seks WOFF2-filer og to PNG-filer. Alle temabyter sammenlignes med filene fra `PalazzoScaffold/Public`. HTML har begge data-attributter, riktige DOM-id-er, ingen Leaf-uttrykk, og offentlig side har CSP/no-store/sikkerhetsheadere. JS inneholder ingen gateway-token eller Authorization-header.

[Statisk kontroll](evidence/static-audit.json): samme 105 HTML-elementer med samme id/klasse-struktur som leaf-kilden; alle originale CSS-regler er bevart; de åtte refererte temaressursene er byteidentiske. Fontenes opprinnelige OFL-notiser er tatt med som CSS-kommentarer, uten flere temafiler. [JS-syntaks](evidence/javascript-syntax.log): exit 0.

«Åpne i HAVEN» peker foreløpig til `https://haven.digipomps.org/porthole` med samme configurationName. Det løser ikke Porthole inne i PalazzoScaffold. Den eksterne lenken er ikke besøkt eller nettverksverifisert. Pikselparitet og lastetid i nettleser er ikke målt; WP5 tilhører Kjetil.

## refusal

`testRefusalIsBlockedAndNorwegianForSevereAllergyUnknownDishAndUnknownQuestion` bekrefter norsk **«ikke bekreftet»**, `confidence: blocked`, `needs_human_review: true`, `status: requires-review` for:

- [Alvorlig nøtteallergi / Pizza Margherita](evidence/responses/refusal-1.json).
- [Ukjent rett / wienerschnitzel](evidence/responses/refusal-2.json).
- [Ukjent spørsmål](evidence/responses/refusal-3.json).
- [Tvetydig allergenmarkering / østers](evidence/responses/refusal-4.json).
- [Vinspørsmål](evidence/responses/refusal-5.json).
- [Åpningstider](evidence/responses/refusal-6.json).

Cellens egne nekt-/allergenvakter er uendret. Fasaden beholder det gamle publikumsfilteret: `low` eller behov for menneskelig vurdering vises som `blocked`, uten interne utkast. Demo-spørsmål 5 gir et [forsiktig nekt-svar om hvete](evidence/responses/demo-wheat.json), ikke filtreringen den eldre huskelisten hevder. Demo-spørsmål 6 [viser til Gastroplanner](evidence/responses/demo-booking.json) og sier uttrykkelig at reservasjonen ikke opprettes eller endres her.

## files

[files.json](evidence/files.json) inneholder filnavn, størrelse og SHA-256 for endret/ny implementering samt oppgavemappens artefakter og evidens. Manifestet utelater sin egen hash for å unngå selvreferanse.

[Statisk kontroll](evidence/static-audit.json) viser at de eneste endrede eksisterende implementeringsfilene er `PalazzoScaffold/README.md` og `Sources/App/routes.swift`. Nye filer er to controller-/projeksjonsfiler, én testfil, HTML/JS/CSS og åtte temaressurser. Ingen eksisterende filer eller tester er fjernet. Korpuscellen, seed-korpuset, gatewayen, Package.swift og Package.resolved er uendret.

## dry-run

[KJOR-SELV-build.sh](handoff/KJOR-SELV-build.sh) har `--dry-run` som standard, `--go` for kjøring. [Tørrkjøring](evidence/handoff-dry-run.log) og [shell-syntaks](evidence/handoff-shell-syntax.log) gir exit 0. Skriptet nekter å slå av Swift Testing hvis slike tester legges til senere, og krever eksisterende lokale avhengigheter. Testtall og faktisk feilstatus kontrolleres; «0 tester passed» kan ikke gi grønt resultat.

## standalone

Ikke utført her: lokal `swift run Run serve`, curl over TCP, nettleserlastetid og skjermbilde. Dette er Kjetils WP5. Native celle og statiske filer er testet i samme PalazzoScaffold-app gjennom in-process HTTP; det erstatter ikke WP5.

<!-- PZ2 FERDIG -->
