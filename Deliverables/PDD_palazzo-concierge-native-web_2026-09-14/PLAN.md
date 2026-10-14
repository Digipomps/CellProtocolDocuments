# PLAN — Conciergen native i PalazzoScaffold, /palazzo servert derfra

G1/G2 2026-09-14. Arbeidspakker 1:1 mot bladformål i FORMAALSSPEC §1. Stier relative til repoet; køjobben har cwd = HAVEN-rot.

| WP | Bladformål | Utfører | Test | Hva det innebærer | Status |
|---|---|---|---|---|---|
| WP0 | baseline | Codex | test.build, test.regression | `swift build/test --disable-sandbox` i PalazzoScaffold FØR endring; tall som «forventet ≈ 105 (2026-09-08)» | målt: 105 tester; standard XCTest-laster blocked, gjentakelse dokumentert |
| WP1 | public-facade + refuses-to-guess | Codex | test.public-ask, test.envelope, test.refusal | Ny controller i PalazzoScaffold som porterer fasadelogikken fra `CellScaffold::Sources/App/Cells/Restaurant/PalazzoCommunaleServiceCell.swift` + `VaporPalazzoCommunale.swift`: kall `PalazzoConciergeCorpus` (`concierge.knowledge.query` m.fl.) som husets/fasadens principal, pakk svaret i konvolutten, sett `route: "native"`, norsk «ikke bekreftet»-tekst | skrevet og verifisert |
| WP2 | no-secret-in-browser | Codex | test.auth-boundary | Fasaden registreres UTENFOR gateway-kravet (egen route group), med rate-limit (30/10 min per klient, `X-Forwarded-For`-bevisst) og body-tak 4096; alt annet API uendret | skrevet og verifisert |
| WP3 | leaf-served | Codex | test.leaf | Kopier `palazzo_communale.leaf` → statisk `Public/palazzo/index.html` (apiBase i data-attributt), `js/palazzo-communale.js`, `css/palazzo-communale.css`, `css/themes/palazzo/*` inn i `PalazzoScaffold::Public/`; `FileMiddleware`; `GET /palazzo` → index | skrevet og verifisert via XCTVapor; visuell WP5 venter |
| WP4 | quality.* | Codex | test.build, test.regression, docs | README-avsnitt; TESTRESULT/ACCEPT; filliste SHA-256 | skrevet, verifisert med full regresjon (116/116) |
| WP5 | standalone + parity | **Kjetil** | test.standalone, test.gui.parity | `swift run Run serve --hostname 127.0.0.1 --port 8083` i PalazzoScaffold, åpne `http://127.0.0.1:8083/palazzo`, still spørsmål 1 fra Demo-huskelisten; skjermbilde → ACCEPT.md#parity (Losen setter side om side) | venter |
| WP6 | commit-pakke | Codex (egen jobb) | | etter grønn WP4 | venter |

## Hva Kjetil selv skal gjøre
1. Vent på `_losen-queue/done/pz2-concierge-native-web-20260914.svar.md`.
2. WP5 (5 min): start scaffoldet lokalt, åpne flaten, still ett spørsmål, ta skjermbilde, si fra.
3. Skaff meny-18-08.pdf fra Andre → egen KO-01-slice (ikke her).

## Gjennomføring 2026-09-14

WP0–WP4 er utført mot lokale filer uten git/nettverk. Full testkjøring bruker
x86_64 og bare XCTest-kjøreruten fordi denne maskinens XCTest-laster og tomme
Swift Testing-kjørerute velger ulike arkitekturer. Alle 116 faktiske tester er
XCTest, og ingen er filtrert bort. Kommandoer, gjentatt baseline og faktisk
utdata finnes i TESTRESULT.md#regression. Dette endrer ikke produksjonsarkitektur
eller omfang; WP5 og WP6 står fortsatt utenfor denne kjøringen.
