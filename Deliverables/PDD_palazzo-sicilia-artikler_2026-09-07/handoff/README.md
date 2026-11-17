# Codex-handoff — Sicilia-artikler (2026-09-07)

Les i rekkefølge: `../PLAN.md`, `../FORMAALSSPEC.md` §1/§5, `../content/artikler_v1.json` (fixture), og husk-leveransen: `PalazzoScaffold/docs/Remember_contract_2026-09-07.md`, `Sources/App/Models/PalazzoRememberModels.swift`, `PalazzoMatchModels.swift`, `Cells/PalazzoContentCell.swift`, `Cells/PalazzoEntityCell.swift`.

Slicer: WP0–WP5 GODKJENT. **WP-GUI BLOKKERT** (ingen fabrikk-/skeleton-endringer i denne kjøringen, bortsett fra at `guest.article.configuration` kan returnere en minimal, testbar konfigurasjon med bare Text-elementer — den byttes ut når bildene er godkjent).

Regler: som husk-handoffen — CellProtocol røres ikke; ingen test fjernes/svekkes; hver handler kaller `validateAccess` med sin keypath; ingen språkmodell; ingen git (egen commit-jobb kommer etterpå); `swift build/test --disable-sandbox`.

Rapport: `PalazzoComunaleScaffold/docs/Rapport_Sicilia_2026-09-07.md` (rå utdata før/etter, per WP gjort/avvik, filliste) og `../TESTRESULT.md` med ankre `#build #regression #articles #reaction #persist #query #signal #no-tracking #e2e #auth`. Svar kun med rapporten.
