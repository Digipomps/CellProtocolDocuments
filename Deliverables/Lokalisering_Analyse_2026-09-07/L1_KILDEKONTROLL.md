# Kildekontroll og sluttstatus — lokaliseringsanalysen

Kontrollert: 2026-09-07T15:26:21+02:00. Alle eksterne kilder ble åpnet 2026-09-07.

Arbeids-ID: `localization-analysis-20260907`. Status: **VERIFIED for analyseleveransen**. Eier/integrator: denne Codex-oppgaven. Beslutningseier: Kjetil. Base-ref/branch/commit: ikke undersøkt, i samsvar med oppdragets «ingen git». Dette er ikke status for implementering eller integrasjon.

Leveranse: [L1_ANALYSE.md](/Users/kjetil/Build/Digipomps/HAVEN/CellProtocolDocuments/Deliverables/Lokalisering_Analyse_2026-09-07/L1_ANALYSE.md). Handoffet og prompten er beholdt. Bakgrunnslauncheren er ikke brukt: analysen ble utført direkte i den allerede aktive Codex-oppgaven. Det er derfor ikke opprettet en launchctl-jobb, `_svar.md` eller en kunstig `.done`-markør.

## Verifikasjon og grenser

- Alle 24 lokale kildeankre i rapporten peker på eksisterende filer og gyldige linjer. Linjer nedenfor er startankre; konkrete intervaller står ved påstandene i rapporten.
- 31 unike primærkildelenker brukes. Normativ standardstatus og dokumentert bibliotekstøtte holdes atskilt. Bibliotekene ble ikke installert, bygget eller konformitetstestet.
- JSON-eksemplene er forslag. De er syntaktisk kontrollert, men ikke validert som eksisterende CellConfiguration/Explore-kontrakter. Ingen nye runtime-capabilities er implementert.
- Det er ikke kjørt Swift-tester, nettlesertester, staging-/produksjonssjekker eller modellbasert masseoversettelse. PDD-tabellens tester er foreslåtte fremtidige akseptansetester.
- Bare leveransefiler ble skrevet i handoff-mappen; mellomutkast ble laget i /private/tmp. Ingen endringer i kildekode, Book, git eller eksterne tjenester.
- Rapporteringssummer er kontrollert: 198–350 tekniske arbeidstimer; første Butterpop 52–92 timer. Estimatene er ikke tidsmålinger.

## Reproduserbare omfangsmål

| Område | Resultat | Metode / begrensning |
|---|---:|---|
| porthole-webo.js | 9 884 linjer; 73 linjer med æ/ø/å; 34 synk-kandidater | Tekstlesing og regex; ikke AST-inventar eller faktisk oversettelsesantall |
| butterpop_studio.leaf | 327 linjer; 100 tekstnoder (96 unike); 10 tekstattributter (9 unike) | Python HTMLParser, normalisert whitespace; script/style-data utelatt |
| butterpop-studio.js | 1 080 linjer; 29 med æ/ø/å; 47 synk-kandidater | Samme heuristikk; fanger ikke alle HTML-template-tekster |
| PersonalCopilotCloudStore.swift | 15 190 linjer; 339 med æ/ø/å | Omfatter kode/kommentarer og gjentakelser; ikke 339 selvstendige svar |
| Resources/Views | 25 .leaf-filer | Rekursiv filinventering |
| Website | 29 HTML-filer; én under en/ ved kontrollen | Lokale kilder; ingen konklusjon om produksjon |
| Binding/Binding og Binding/Cells | 107 filer i rg-inventaret | Ingen lokaliseringsressurser eller eksplisitte API-treff i angitt scope |

Synk-regex: `textContent\s*=|\.notice\s*=|\.placeholder\s*=|\.innerHTML\s*=|\.title\s*=`. Tekstattributter: `placeholder`, `title`, `alt`, `aria-label`. HTML-tekstnoder telles bare når de inneholder minst én bokstav fra `[a-zA-ZæøåÆØÅ]`; merkevarer og tekniske verdier kan inngå.

Fraværssøk ble gjort med `rg` i CellScaffolds `Sources`, `Public/js`, `Resources` etter `Accept-Language`, `preferredLanguage`, `navigator.languages`, `navigator.language`, `resolved_locale` og `LocaleResolver`. Treffet i VaporBrowserhead motsier handoffets A7. Et separat søk etter `person.preferences`/`locale` fant de eksplisitte EntityAnchor-kontraktene. Ingen fullstendig negativ bevisføring for alle repoer/alle synonymer hevdes.

Binding-søket omfattet `.xcstrings`, `.strings`, `.stringsdict`, `.lproj` og `String(localized:)`, `LocalizedStringResource`, `LocalizedStringKey`, `NSLocalizedString`. Det eksterne Apple-rendererlaget i CellProtocol ble deretter inspisert separat.

Babel/Acorn/TypeScript-parser var ikke tilgjengelig via vanlig Node-resolusjon eller de undersøkte CellScaffold-node_modules-stiene. Ingen pakker ble installert. Rapportens AST-metode er derfor en konkret anbefalt prosedyre, ikke et allerede utført AST-uttrekk.

## Lokale kilder og øyeblikksbilder

SHA-256 nedenfor identifiserer innhold ved sluttkontrollen. Det beviser ikke at andre oppgaver aldri har endret arbeidskopiene. Ingen privat entitetsdata ble lest; kontrollen gjelder kode, kontrakter og oppgitte dokumenter.

| ID | Fil og startlinje | SHA-256 |
|---|---|---|
| R1 | [/Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellBase/Cells/Commons/CommonsTaxonomyCell.swift:184](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellBase/Cells/Commons/CommonsTaxonomyCell.swift:184>) | `1cf19f11060221927c5a9644a749722f195ab47561fd5ed07f3429be217ec7d6` |
| R2 | [/Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/commons/schemas/haven.core/Sources/HavenCoreSchemas/LocalizationContracts.swift:6](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/commons/schemas/haven.core/Sources/HavenCoreSchemas/LocalizationContracts.swift:6>) | `cdeb898d6c8762d46ac7cd131120894f37c88df213324fda55011ef1d35dc558` |
| R3 | [/Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellBase/PurposeAndInterest/PerspectiveNode.swift:41](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellBase/PurposeAndInterest/PerspectiveNode.swift:41>) | `7281be133e7e820859f1fc1ef147fa4984a6100598294c972c19cf1245ad1468` |
| R4 | [/Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellBase/PurposeAndInterest/Interest.swift:42](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellBase/PurposeAndInterest/Interest.swift:42>) | `db1407030452663a5738bc78a14dc01188ff6f9c839e603078f26fb4aaaebc6b` |
| R5 | [/Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellBase/PurposeAndInterest/Purpose.swift:41](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellBase/PurposeAndInterest/Purpose.swift:41>) | `f2af17efe01c9191035a1fce994997a2dd57302ebc471250525380c25a36c4f1` |
| R6 | [/Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellBase/PurposeAndInterest/Perspective.swift:378](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellBase/PurposeAndInterest/Perspective.swift:378>) | `b9527b7bd8c7ef47e3092a50b9f9742c003197670364cc23a7e6eeb2f83c8e09` |
| R7 | [/Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellBase/Skeleton/SkeletonDescription.swift:1752](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellBase/Skeleton/SkeletonDescription.swift:1752>) | `4d8356cc8deee346d7e07f15b63f99894d9b512d8361628ea85859e329e7c611` |
| R8 | [/Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellBase/CellConfiguration/CellConfiguration.swift:6](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellBase/CellConfiguration/CellConfiguration.swift:6>) | `9b06c0164c6fc80120ce80a806f9ae984689a1c70e644714edb68f6104f27005` |
| R9 | [/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Public/js/porthole-webo.js:1682](</Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Public/js/porthole-webo.js:1682>) | `cddc0a6ffbf6d0722662afd834d72d6263fa89bb4a91e723d9e1e4c0efee31ae` |
| R10 | [/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Resources/Views/butterpop_studio.leaf:2](</Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Resources/Views/butterpop_studio.leaf:2>) | `07ebf49e42c21608522102dfe610984cd71ec650dfad4581f1d87a5ceb90f9fc` |
| R11 | [/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Public/js/butterpop-studio.js:1](</Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Public/js/butterpop-studio.js:1>) | `24a0991ba698073df1dcf0a81a7fbdccecdca9684e3ffaf464bbac02482023cf` |
| R12 | [/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Sources/App/Cells/PersonalCopilot/PersonalCopilotCloudStore.swift:5321](</Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Sources/App/Cells/PersonalCopilot/PersonalCopilotCloudStore.swift:5321>) | `dd125c5e23b944a2b1308932c5e2a68a542f7b63c8cc08cb38f3d62b2247d49c` |
| R13 | [/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Sources/App/Controllers/VaporBrowserhead.swift:33](</Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Sources/App/Controllers/VaporBrowserhead.swift:33>) | `7ffdf5733b0fbf36ad567d0ecc4c399f578aea6533af06c76975e2209b836e51` |
| R14 | [/Users/kjetil/Build/Digipomps/HAVEN/CellProtocolDocuments/Website/RELEASE_NOTE_2026-09-07.md:3](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocolDocuments/Website/RELEASE_NOTE_2026-09-07.md:3>) | `92ebfc1184f52dba7839e346d206eaa06bee317d73c756d587860f349d00bb04` |
| R15 | [/Users/kjetil/Build/Digipomps/HAVEN/CellProtocolDocuments/Website/en/artikler/from-the-2019-sketch-to-today/index.html:13](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocolDocuments/Website/en/artikler/from-the-2019-sketch-to-today/index.html:13>) | `8ee266cc3f7e316afb3ae0b4c336ca832505418ae9ef3caecda1e54510c2ac96` |
| R16 | [/Users/kjetil/Build/Digipomps/HAVEN/PyCellProtocol/src/cellprotocol/configuration.py:86](</Users/kjetil/Build/Digipomps/HAVEN/PyCellProtocol/src/cellprotocol/configuration.py:86>) | `ab8379afd032cd6c89e84c24c6998f54174627cf8d47bb3f2cbc402acd2749da` |
| R17 | [/Users/kjetil/Build/Digipomps/HAVEN/GoCellProtocol/configuration.go:108](</Users/kjetil/Build/Digipomps/HAVEN/GoCellProtocol/configuration.go:108>) | `5c4a2f56bf12e1221ec058cd768e19d236b15783695c11911402d1b2ed4d761e` |
| R18 | [/Users/kjetil/Build/Digipomps/HAVEN/RustCellProtocol/src/configuration.rs:16](</Users/kjetil/Build/Digipomps/HAVEN/RustCellProtocol/src/configuration.rs:16>) | `c439acd555c13eea4e02d772bebabba34d81625156e9175820c992e5a541b682` |
| R19 | [/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Sources/App/Support/EntityAnchorDataV1Contract.swift:406](</Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Sources/App/Support/EntityAnchorDataV1Contract.swift:406>) | `7e7164c4269fe11b1201bded06c6e6703d74096dbf44ab83f4865341146b0cd9` |
| R20 | [/Users/kjetil/Build/Digipomps/HAVEN/CellProtocolDocuments/Book/12_Skeleton_Spec.md:1](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocolDocuments/Book/12_Skeleton_Spec.md:1>) | `805b89c21b05cea40200c8bcc4c0d49ca8cb10097b064da3478ee7a3211ada68` |
| R21 | [/Users/kjetil/Build/Digipomps/HAVEN/CellProtocolDocuments/Book/22_Explore_Contracts_For_Skeleton_Authoring.md:179](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocolDocuments/Book/22_Explore_Contracts_For_Skeleton_Authoring.md:179>) | `14dd2491d3b002c6b36bbf67cdb2fb670f31ed5ddc54e0eafee5fac4e9ac5e20` |
| R22 | [/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Public/js/skeleton-runtime.js:360](</Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Public/js/skeleton-runtime.js:360>) | `d7fde52f283875a9f09eab28dec9bbecf7b057841f09d33ae8c33c9ec5477416` |
| R23 | [/Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/Suggestion/SkeletonView.swift:1805](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/Suggestion/SkeletonView.swift:1805>) | `180758c91ca126c77da9b6f430b67e92782eb96407d878b05d972411e4aad15d` |
| R24 | [/Users/kjetil/Build/Digipomps/HAVEN/CellProtocolDocuments/Website/rettelser/index.html:23](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocolDocuments/Website/rettelser/index.html:23>) | `25c49556b6c13042445a3d469c11e0c734298900f67b5833f8216a47369cad18` |

## Supplerende inspiserte kilder

- [TaxonomyResolver.swift](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/commons/resolver/taxonomy-resolver/Sources/TaxonomyResolver/TaxonomyResolver.swift>); SHA-256 `247b67d289c5b78d3544eb2fc139d58727d729698efc9ac88e03fb54661cc2dc`.
- [SkeletonTests.swift](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Tests/CellBaseTests/SkeletonTests.swift>); SHA-256 `cff9393c254f796c65822f44d052e9e742674246fad024cea9940a92ce493760`.
- [HANDOFF.md](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocolDocuments/Deliverables/Lokalisering_Analyse_2026-09-07/HANDOFF.md>); SHA-256 `78c2468cec49554727d2160e5769ebbf49d0466dcfc598f74d0fc816b59c8e61`.
- [L1_ANALYSE_prompt.md](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocolDocuments/Deliverables/Lokalisering_Analyse_2026-09-07/L1_ANALYSE_prompt.md>); SHA-256 `55d1b72da9c5160fa46c17a13a7ecf56a156c71f821306d6623e6543c1841b00`.
- [README.md](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocolDocuments/Deliverables/Lokalisering_Analyse_2026-09-07/README.md>); SHA-256 `de4b63d4869617b6eb86959d508dc126d7b351b87dfb090fd080b1d1ba2a4036`.
- [LOKALISERING_Vurdering_2026-09-07.md](</Users/kjetil/Build/Digipomps/HAVEN/Kallimachos/Verdifordeling/Sachs_2026-09-07/Nettside/LOKALISERING_Vurdering_2026-09-07.md>); SHA-256 `00bf30f5b4b1d7883192559d89eb13417ea66c91db337e37f13de737f8af3172`.
- [__init__.py](</Users/kjetil/Build/Digipomps/HAVEN/PyCellProtocol/src/cellprotocol/__init__.py>); SHA-256 `ccf336eb7b31fb72a1b24492027cf2d7252d60f4880999cdf37406fc918a2035`.
- [README.md](</Users/kjetil/Build/Digipomps/HAVEN/GoCellProtocol/README.md>); SHA-256 `dea086040e3c4f08e203a5942a5800f4ac5d4257f4c59bf9583f9402189e43cc`.
- [README.md](</Users/kjetil/Build/Digipomps/HAVEN/RustCellProtocol/README.md>); SHA-256 `4b9024ab9503646bf2eb94bb8024f32980a24cc889c78b84d9bca3194ac4adef`.

## Eksterne primærkilder

Alle oppføringer: **retrieved 2026-09-07**. At en prosjektside lister en egenskap er støtte for «prosjektet dokumenterer dette», ikke uavhengig bevis for ytelse eller full konformitet.

- **W1:** [Apple: Discover String Catalogs](https://developer.apple.com/videos/play/wwdc2023/10155/).
- **W2:** [Apple: Explore localization with Xcode](https://developer.apple.com/videos/play/wwdc2025/225/).
- **W3:** [Unicode UTS #35 del 9, hentet v48.2](https://www.unicode.org/reports/tr35/tr35-messageFormat.html).
- **W4:** [ICU4C 78.3 MessageFormatter, Technical Preview](https://unicode-org.github.io/icu-docs/apidoc/released/icu4c/classicu_1_1message2_1_1MessageFormatter.html).
- **W5:** [Project Fluent: grammatikk og plattformer](https://projectfluent.org/).
- **W6:** [GNU gettext: Workflow flags](https://www.gnu.org/software/gettext/manual/html_node/Workflow-flags.html).
- **W7:** [Python: gettext](https://docs.python.org/3/library/gettext.html).
- **W8:** [i18next: prosjektets README](https://github.com/i18next/i18next).
- **W9:** [FormatJS: ICU-syntaks](https://formatjs.github.io/docs/core-concepts/icu-syntax/).
- **W10:** [ICU: Formatting Messages](https://unicode-org.github.io/icu/userguide/format_parse/messages/).
- **W11:** [ICU4C: stabil MessageFormat, navngitte argumenter](https://unicode-org.github.io/icu-docs/apidoc/released/icu4c/classicu_1_1MessageFormat.html).
- **W12:** [Lingo: JSON-syntaks og dokumenterte begrensninger](https://github.com/miroslavkovac/Lingo).
- **W13:** [Lingo-Vapor: Leaf-tags](https://github.com/vapor-community/Lingo-Vapor).
- **W14:** [messageformat: MF1, MF2 og konverteringspakker](https://github.com/messageformat/messageformat).
- **W15:** [Unicode MFWG: ikke-normativ implementasjonsliste](https://github.com/unicode-org/message-format-wg/blob/main/spec/README.md).
- **W16:** [Project Fluent: JS-implementasjon](https://github.com/projectfluent/fluent.js).
- **W17:** [Project Fluent: Python-implementasjon](https://github.com/projectfluent/python-fluent).
- **W18:** [MessageFormat Go: egen dokumentasjon, ikke uavhengig konformitetsbevis](https://github.com/kaptinlin/messageformat-go).
- **W19:** [Rust MF2-parser, ikke bevis for formatter](https://github.com/sajikix/mf2-parser).
- **W20:** [Project Fluent: Rust-implementasjon](https://github.com/projectfluent/fluent-rs).
- **W21:** [FormatJS: Rust og ICU4X-underlag](https://formatjs.github.io/docs/rust/).
- **W22:** [RFC 4647: Matching of Language Tags](https://www.rfc-editor.org/rfc/rfc4647.html).
- **W23:** [RFC 9110: Accept-Language, Content-Language, Vary](https://www.rfc-editor.org/rfc/rfc9110.html).
- **W24:** [Google Search Central: localized versions](https://developers.google.com/search/docs/specialty/international/localized-versions).
- **W25:** [FormatJS: uttrekk av deklarerte meldinger](https://formatjs.github.io/docs/getting-started/message-extraction/).
- **W26:** [Babel-parser](https://babeljs.io/docs/babel-parser).
- **W27:** [SwiftSyntax: parsing og transformasjon](https://github.com/swiftlang/swift-syntax).
- **W28:** [CLDR 48: språkspesifikke pluralregler](https://www.unicode.org/cldr/charts/48/supplemental/language_plural_rules.html).
- **W29:** [ECMA-402 redaktørutgave: Intl-formatering; ikke garanti for browserutrulling](https://tc39.es/ecma402/).
- **W30:** [Unicode LDML: datoer og tidssoner](https://www.unicode.org/reports/tr35/tr35-dates.html).
- **W31:** [W3C: strukturell RTL-markup](https://www.w3.org/International/questions/qa-html-dir).

Noen Apple-dokumentasjonssider leverte bare JavaScript-skjell, og flere GNU-manualsider ga hentefeil. Disse brukes ikke som leste innholdskilder; Apple-videoenes transkripsjoner og de hentede GNU/Python-sidene erstatter dem. Søkeresultater fra andre prosjekters arkitekturnotater og generelle innlegg ble ikke brukt som bevis for MF2/Fluent-støtte.

## Åpne punkter ved overlevering

- Kjetil velger Q1–Q4 før implementering.
- P0 skal kvalifisere Swift-/Linux-/Apple-pakking og den eventuelle xcstrings-konverteren. Disse er rapportens viktigste tekniske usikkerhet.
- Full strenginventering, all artikkeloversettelse, eksisterende datakollisjoner og full Kallimachos-dialogdekning gjenstår som implementeringsarbeid.
- Revisjonsmapping og godkjenningsflyt for private brukerlagde labels krever et faktisk avgrenset datadomene; ingen slike data ble migrert her.

Rapportens SHA-256 ved denne kontrollen: `f017c74ae7494862528a2aedc77f05ebebd3a5fc8a7810ee15a8c7c3c10873e0`.
