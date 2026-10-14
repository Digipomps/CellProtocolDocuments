# Dataflyt — gjestens spørsmål etter strakstiltaket

Stier er relative til HAVEN-roten. `PS` står for `PalazzoScaffold`.

```
Gjest
  │ POST /palazzo/api/ask {query}          POST /palazzo/api/menu     POST /palazzo/api/beverages
  ▼                                             │                          │
PalazzoCommunaleRequestMiddleware          (samme)                     (samme)        teller mot 30 per ti minutter
  ▼                                             │                          │
ask: tomt? for langt?                           │                          │           som i dag (422, 413)
  ▼                                             │                          │
[1b] PalazzoAllergiHenvisning.treffer      ─────┼──────────────────────────┼──  NY (regel 1)
  ├── ja ──▶ henvisningen ──────────────────────┼──────────────────────────┼──┐
  └── nei                                       │                          │  │
  ▼                                             ▼                          ▼  │
PalazzoCommunaleFacade.perform                                                │
  │ [2] oppslaget (PalazzoConciergeCorpusCell), urørt                         │
  ▼                                                                           │
PalazzoCommunaleProjection.project                                            │
  │ [3] svaret kontrolleres for form, som i dag                               │
  │     har svaret « er merket med: »?  ── ja ──▶ henvisningen ───────────────┤   NY (regel 2)
  │     avvist av oppslaget, uten kilder osv.  ──▶ avvisningen, som i dag     │
  │     publiseres: linjen om allergener først i warnings, hvis ingen         │   NY (regel 3)
  │     advarsel har ordet allergi eller allergen                             │
  ▼                                                                           │
PalazzoConciergePhrasing.rephrasedWithOutcome                                 │
  │ [4] modellen og vakten, urørt. Leser aldri warnings                       │
  ▼                                                                           ▼
[5] én linje i containerens logg       utfall=…  som i dag        utfall=allergi-henvisning:ordliste | :merking
  ▼                                                                           ▼
[6] svaret til gjesten: samme 13 felt                              reason_code: allergy-referral
```

| Kant | Endepunkt eller funksjon | Finnes i kode | Endres |
|---|---|---|---|
| 1 | `POST /palazzo/api/ask`, `/menu`, `/beverages` | `PalazzoCommunaleFacade.boot` | nei |
| 1b | `PalazzoAllergiHenvisning.treffer` | NY, `PS/Sources/App/Services/PalazzoAllergiHenvisning.swift` | ny |
| 2 | `PalazzoCellAccess.set` mot `PalazzoConciergeCorpus` | `PalazzoCommunaleFacade.perform` | nei |
| 3 | `PalazzoCommunaleProjection.project` | samme navn | ja |
| 4 | `PalazzoConciergePhrasing.rephrasedWithOutcome` | samme navn | nei |
| 5 | loggeren `palazzo.concierge.formulering` | `PalazzoCommunaleFacade` | to nye utfall |
| 6 | svarkonvolutten | `PalazzoCommunaleProjection.envelope` | ny verdi og ny linje, se `contract/README.md` |

Veier inn til oppslaget som tiltaket ikke står foran: det interne API-et (`/api/concierge/*`, krever husets nøkkel) og brohodet for HAVEN-klienter. Brohodet er av på verten: `PALAZZO_BRIDGEHEAD_ENABLED=false` i `/opt/palazzo/.env`, lest 6. oktober kl. 11:00 UTC.
