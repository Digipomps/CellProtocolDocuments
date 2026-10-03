# Dataflyt — conciergens formulering (runde 2)

Stier er relative til HAVEN-roten. `PS` står for `PalazzoScaffold`.

```
Gjest
  │ POST /palazzo/api/ask {query}
  ▼
PalazzoCommunaleFacade.perform            PS/Sources/App/Controllers/PalazzoCommunaleFacade.swift
  │ kunnskapscellen svarer
  ▼
PalazzoCommunaleProjection.project        godkjent svar (status, answer, citations, warnings)
  │
  ▼
PalazzoConciergePhrasing                  PS/Sources/App/Services/PalazzoConciergePhrasing.swift
  │  [3] skal modellen spørres?           ENDRES: svar med forbehold, kontaktopplysninger
  │      nei ─────────────────────────┐   eller flere kolon sendes ikke
  │      ja                           │
  ▼                                   │
PalazzoAnthropicPhraser               │   PS/Sources/App/Services/PalazzoAnthropicPhraser.swift
  │  [4] godkjent svar og kildetitler │   ENDRES: instruksen; årsak når det ikke kommer tekst
  │      (aldri gjestens spørsmål)    │
  ▼                                   │
PalazzoPhrasingGuard                  │
  │  [5] innholdet uendret?           │   ENDRES: innholdet tegn for tegn, rammen fra lukket liste
  │      rammen lukket?               │
  ├── godtatt ──▶ route: model        │
  └── forkastet ─▶ route: native ◀────┘
  │
  ├─▶ [6] én linje i containerens logg    NY: utfallet med navngitt grunn
  ▼
Gjest leser svaret (samme konvolutt som før)
```

| Kant | Endepunkt eller funksjon | Finnes i kontrakt eller kode | Endres i runde 2 |
|---|---|---|---|
| 1 | `POST /palazzo/api/ask` | `PalazzoCommunaleFacade.boot` | nei |
| 2 | `PalazzoCommunaleProjection.project` | samme navn | nei |
| 3 | `PalazzoConciergePhrasing.mayRephrase` | samme navn | ja |
| 4 | `PalazzoAnthropicPhraser.rephrase` | protokollen `PalazzoAnswerPhraser` | instruksen og feilårsaken |
| 5 | `PalazzoPhrasingGuard.accept` | samme navn | ja |
| 6 | logglinje `concierge-formulering utfall=…` | ny | ny |
| 7 | svaret, skjema `haven.palazzo.communale.guest-concierge.v1` | `PalazzoCommunaleFacade.schema` | nei |
