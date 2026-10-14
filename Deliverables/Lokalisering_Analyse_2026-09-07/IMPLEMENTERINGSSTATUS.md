# Lokalisering i Skeleton — første implementeringsdel

Dato: 7. september 2026. Arbeidet startet etter Kjetils beskjed om å gå i gang med implementeringen. Endringene ligger i de lokale arbeidskopiene; ingen commit, push eller utrulling er gjort.

En første gjennomgående løsning er implementert for samme Skeleton-konfigurasjon i web/Porthole og den felles SwiftUI-rendereren som Binding bruker. Dette er en avgrenset første del av S0–S3, med noen tidlige validerings- og målearbeider fra S4–S5. Hele implementeringsplanen er ikke ferdig.

## Det som virker

- Additiv `CellConfiguration.localization` og `modifiers.localization`, med gamle strenger som reserve. Ingen endring av action-keypaths, payloads, referanseidentifikatorer eller brukerens redigerbare tekst.
- Versjonert JSON-katalog, ICU MF1-plural/select, tall, dato/tid, typede argumenter og eksplisitte dataeide listeetiketter. Bare godkjente oversettelser brukes; angitt kildehash kontrolleres mot godkjenningen.
- `Text.text`, `Button.label`, `TextField.placeholder` og `TextArea.placeholder`. Andre posisjoner avvises av lokaliseringsvalideringen til de er implementert.
- Én og samme FormatJS-pakke på web og via offentlig JavaScriptCore på Apple. Pakken er omtrent 43 kB uten komprimering. Tredjepartslisensene følger både web- og Apple-ressursene.
- Språkbytte oppdaterer eksisterende tekstbindinger. Det bygger ikke et nytt Skeleton og gjør ingen ekstra katalog- eller argumentforespørsler. Formattere gjenbrukes i avgrensede cacher.
- Porthole tar imot språk-kontekst fra bootstrap, bruker ellers nettleserspråk og oppdaterer katalogrevisjon uten å bytte det viste treet. Chat- og konferansevertene sender også katalog og nettleserkontekst til den delte rendereren; disse vertene har ikke egne komplette funksjonstester i denne leveransen.
- Binding sender konfigurasjonen til den felles native verten. Native vert kan bytte språk og tar inn en autorisert argument-snapshot. Deklarerte rotargumenter hentes ved konfigurasjon og lokal mutasjon, ikke av enkeltetiketter. Item/context og knapp-payloads blir ikke ekstra rotoppslag. Bytte av requester tømmer native lokaliseringsdata og kataloger.
- CLI for forfattervalidering og utvidet Explore-validering. Book 12 og 22 beskriver faktisk levert støtte og kjente mangler.

## Verifikasjon

| Kontroll | Resultat |
| --- | --- |
| Node: formatter, språkpolicy, kataloger og forfattervalidering | 32 bestått |
| Swift: lokalisering og eksisterende handlingskontrakter | 15 bestått |
| CellScaffold: bootstrap-projeksjon | 11 bestått |
| Playwright/Chromium: lokaliserings-, Porthole-, navigasjons-, felt- og valideringsregresjoner | 22 bestått |
| Explore-verktøyenes Python-tester | 11 bestått, 1 eksisterende test hoppet over |
| Binding/HAVEN macOS-bygg, uten signering | BUILD SUCCEEDED |
| Felles formatter-fixture | 22 av 22 tilfeller samsvarer i Node, faktisk Chromium og Apple-adapteren |
| ICU4C-prøve, macOS 78.3 og Linux 74.2 | 19 av 20 ikke-reservetilfeller samsvarer eksakt; ett kjent mellomromsavvik |

Native-testen monterer det faktiske `SkeletonView` i et AppKit/SwiftUI-vindu, leser tilgjengelighetstreet og tar skjermbilder. Den verifiserer engelsk/norsk tekst, plassholder, samme input-instans, uendret utkast, markering og mutasjonsversjon. Dette er renderertesten i en isolert vert; den er ikke et fullført gjennomklikk av den kjørende Binding-appen med reelle private celler.

Web-testene verifiserer blant annet utkast/fokus/markering, 0 nettverksforespørsler under språkbytte, pågående lagring med uendret payload og busy-status, riktig plural ved dataendring, katalogrevisjon uten DOM-utskifting, avvisning av ugyldig konfigurasjon og at argumenter med HTML vises som tekst. Testen av selve Porthole-verten bruker de faktiske appskriptene med en kontrollert bootstrap-respons.

Målingene av 200 monterte tekster og 1000 listeetiketter ligger i `evidence/localization-performance.json` og `evidence/localization-list-performance.json`. De måler bare synkront bindingsarbeid ved varmt språkbytte, ikke tid til ferdig tegnet skjerm. Testene beholdt nodene; listetesten beholdt også rulleposisjonen. 200-teksttesten brukte to kompilerte ICU-meldinger for de to språkene. Tallene er lokale utviklingsmålinger på macOS 26.5.1/arm64, Node 22.14.0 og Playwright 1.55.1, med andre bygg i gang. De er ikke en release-garanti eller en native ytelsesmåling.

## Avklaring fra S0

Planens opprinnelige forslag var FormatJS i web og pakket ICU4C i Swift. Apple-prøven viste at samme lille FormatJS-pakke kan brukes via offentlig JavaScriptCore. Den løsningen er nå valgt for Apple: ingen private ICU-symboler og ingen Homebrew-avhengighet i appen. Reproduserbare verktøy, eksakte npm-versjoner og lisensfiler er lagt inn.

ICU4C-prøven beholdes som separat portabilitetsbevis. Både macOS og Linux ga `12:00` + U+202F + `AM`, mens den delte web/Apple-fixturen forventer U+0020. Forskjellen er ikke normalisert bort. Swift-interpreteren i den emulerte amd64 Linux-containeren hang; Linux-resultatet er derfor fra C++-adapteren kjørt direkte i containeren, styrt av Python på verten. Testcontaineren er stoppet. Det finnes ikke en produksjonsklar Linux-formatteradapter i denne leveransen.

Offisielle referanser: [Apple JavaScriptCore/JSContext](https://developer.apple.com/documentation/javascriptcore/jscontext), [FormatJS ICU-syntaks](https://formatjs.github.io/docs/core-concepts/icu-syntax/), [ICU4C MessageFormat](https://unicode-org.github.io/icu-docs/apidoc/released/icu4c/classicu_1_1MessageFormat.html). Lokale prøver og kildekode er grunnlaget for kompatibilitetsresultatene over.

## Det som gjenstår

1. Fullføre S2: hente og lagre eiers språkpreferanse gjennom eksisterende kontrakter, synlig feil ved lagringssvikt og en språkvelger. Native språkvalg oppbevarer foreløpig den effektive locale; opprinnelsen til språkvalget må føres konsekvent videre sammen med requested/ui/resolved-kontekst.
2. Fullføre S3: en gjenbrukbar demo/testcelle med eksplisitte Explore-data/handlinger, native oppdatering ved innkommende remote Flow, og test av katalog-/argumentisolasjon gjennom faktisk bytte av eier i begge appverter. Dagens native test bruker registrerte GeneralCell-intercepts; web bruker testdata/action-handler.
3. S4: Picker/Tabs/Toggle, autocomplete, navigasjonsbar, upload, tilgjengelighet og rendererens egne status-/feiltekster. Test at editor preview/commit, kopiering og publisering bevarer lokaliseringsmetadata og ressurser. Utvide uttrekk/oversettelse/godkjenning utover validatoren.
4. S5: native 200-/1000-målinger, tid til ferdig tegnet flate, langtekst, mobil/desktop-layout, tredje språk på reell flate, RTL og release/rollback-prøve. Polske pluralformer finnes i formatter-fixturen; full RTL-støtte er ikke verifisert.
5. S6 og videre innføring: Butterpop, infosider og migrering av Interest/Purpose. Ingen av disse produktene er oversatt av denne endringen.

Neste konkrete utviklingsdel er S2-preferanser og en demo-konfigurasjon som kan åpnes, deretter de resterende Skeleton-posisjonene. Det generelle formatet og rendererene kan nå brukes som grunnlag for dette arbeidet.

## Filer og gjentakelse

- `CellProtocol/Tools/Localization/README.md` beskriver bygging, validering, avhengigheter og ressurskopiering.
- `CellProtocol/fixtures/localization/skeleton.json` er den delte konfigurasjonen; ekstra testfelter er testdata, ikke lovede produksjonsendepunkter.
- `CellProtocol/Tests/CellBaseTests/SkeletonLocalizationTests.swift` og `CellScaffold/playwright/{skeleton-localization,porthole-skeleton-localization}.spec.js` inneholder gjennomgående tester.
- `evidence/` inneholder native skjermbilder/tilgjengelighetstekst, ICU-differanser, målinger, komprimerte testlogger og kildehasher. Fullstendige lokale bygglogger ligger i `/private/tmp/haven-localization-*.log`.
- `CellProtocol/Docs/Localization_Implementation_Status_2026-09-07.md` er gjenopptakelsesnotatet.

Alle repoene hadde annet pågående arbeid. Det er bevart. Særlig har `Package.swift`, Portholes hovedskript og Bindings `ContentView.swift` også endringer fra før denne oppgaven; en senere commit må velge lokaliseringsendringene bevisst.
