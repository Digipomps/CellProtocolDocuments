# PLAN — formålsregister som graf

Utkast 2026-09-12. **G2 venter på Kjetil.** G1 godkjent 2026-09-12.
Stier relative til `HAVEN/`.

Arbeidspakkene står 1:1 mot bladformålene i `FORMAALSSPEC.md` §1. Hver pakke navngir
formålet den tjener, hvem som utfører den, testene den skal gjøre grønne, og artefaktene
den produserer for §3. Rekkefølgen er avhengighetsrekkefølge.

**Låst av Kjetil 2026-09-12:** registeret bor i **CellProtocol** · dimensjoneres mot
**100 000 noder** · **én motor fra første dag**, ingen overgangsperiode · **invarianskrav**
på kvalitetsporten · kilden er resultatet av forsoningen, ikke en av dagens filer.

## Blokkeringer før WP3

| # | Hva | Hvem | Status |
|---|---|---|---|
| B1 | De fem ja/nei i `contract/taksonomi-forsoning.md` (D0, INN-IA, tabell A/B/C) | Kjetil | **lukket 2026-09-15** (D0/A/B/C ja 13.09; INN-IA = facet 15.09, v-innia) |
| B2 | Motorvalget M1 mot M2 (§6 Q6b) | analyse levert 2026-09-13: **kan ikke avgjøres uten måling X**. Erstattet av WP4a | lukket som spørsmål, åpen som måling |
| B3 | Fasit: menneskedommer — runde 1 ga «ja» på alle 197 (kan ikke skille motorene); runde 2 publisert 15.09, streng, 5 oppgaver / 75 rader, se `maaling/DOMMER_RUNDE2.md` | Kjetil | venter (runde 2) |

B1 blokkerer WP1. B2 blokkerer WP4, men **ikke WP4b** — de to håndrullede matcheveiene må bort uansett hvem som vinner. B3 blokkerer WP11 og dermed enhver kvalitetspåstand.
Alt annet kan starte.

## Arbeidspakker

| WP | Formål | Hva som gjøres | Utfører | Tester | Artefakt |
|---|---|---|---|---|---|
| **WP0** | quality.build-and-regression | Baseline på **rent** utsjekk av `CellProtocol` fra `origin/main`. Antall tester og antall røde før noe endres. Ikke mål på en annen PDDs gren (lesson 2026-09-09) **Status: blocked 2026-09-15** — bygg exit 1: FileUtils-c krever HTTPS-henting som nettforbudet avviser; regresjonsbaseline ukjent. | Codex | test.build, test.regression | [TESTRESULT.md#build](TESTRESULT.md#build), [#regression](TESTRESULT.md#regression) |
| **WP1** | …en-kilde · forsoning | Bygg den forsonte taksonomien som **én** kilde, fra de godkjente radene i `contract/taksonomi-forsoning.md`. Innfør `INN-IA` som erklært egenskap. Kanter bare fra `parentRef` (D0) | Losen | test.reg.forsoning-komplett, test.reg.ref-er-ikke-sti | forsont kildefil + `contract/taksonomi-forsoning.md` signert |
| **WP2** | …en-kilde | Generator: Book-JSON og runtime-tabell genereres fra kilden. Hash av kilde og generert utgave lagres | Codex | test.reg.divergens, test.reg.generert-er-fersk | `Tools/PurposeKnowledge/generate_runtime_taxonomy.py` |
| **WP3** | …bro | Bygg `Purpose`/`Interest`-noder og kanter fra kilden. Ingen kode utleder slektskap fra punktum i ref-en | Losen + Codex | test.reg.bro-dekning, test.reg.ref-er-ikke-sti | `TESTRESULT.md#bro` |
| **WP4a** | …skal-ikke.to-motorer | **Måling `X-100k-tolket-registerkontrakt`.** X0 lås felles observerbar kontrakt (root-dekning/hops, sammensatte relasjoner, syklus, lokaler fra lag 1 til beslutning i lag 2, no-hit/unknown/polaritet, TTL/budsjett, duplikater/score/proveniens, strukturell identitet). X1 to sammenlignbare prøveadaptere i **isolert harness**, ingen produksjonsruting — trenger en kandidat ny traversal for å bestå X0, føres det som utviklingsarbeid, ikke skjules i adapteren. X2 mål ved faktisk N og 100 000, kald/varm p50/p95, minne, normal og for lav budsjettverdi. Avgjørelsesregelen settes **før** tallene sees | Losen + Codex | test.reg.100k, test.reg.kostnadsprofil | `TESTRESULT.md#kostnadsprofil`, beslutningsnotat |
| **WP4b** | …skal-ikke.to-motorer | **Fjern de to håndrullede matcheveiene** — `PerspectiveCell.swift:684` (nøkkellikhet + `min(weight)` + egen dedup) og `PurposeKnowledgeBase.resolvePrompt` (`:551`). Begge må bort uansett hvilken motor som vinner. **Ikke blokkert av B2** | Codex | test.reg.en-motor-i-kode | `TESTRESULT.md#konformans` |
| **WP4** | …skal-ikke.to-motorer | **Motorvalget iverksettes** når WP4a har gitt tallene. Den valgte motoren blir den eneste i produksjonsvei; den andre pensjoneres eller blir ren konformansreferanse | Codex | test.reg.en-motor-i-kode, test.reg.konformans | `TESTRESULT.md#konformans` |
| **WP5** | …bro | Signal fra `purpose://root` med `hops` = tredybde skal nå alle kanoniske refs | Codex | test.reg.signal-naar-roten | `TESTRESULT.md#bro` |
| **WP6** | …adjacency-i-bruk | `PurposeInterestAdjacencyIndex` bygges fra registeret og kobles på én reell oppslagsvei | Codex | test.reg.adjacency-vs-signal | `TESTRESULT.md#adjacency` |
| **WP7** | …lokale-variabler | Én produksjonsvei bruker `Signal.localVariables` lagvis: lag 2 avgjør noe lag 1 ikke kunne, uten modellkall | Codex | test.reg.lagvis-lokale-variabler | `TESTRESULT.md#lagvis` |
| **WP8** | …celle | `cell:///PurposeRegistry` i **CellProtocol**: eier grafen, eksponerer `registry.state/resolve/match/taxonomyDigest` med Explore-kontrakter og eier-scopede Grants | Losen + Codex | test.cell.contract-fixtures, test.cell.auth-negative | `contract/purpose_registry_contract_v0.json` |
| **WP9** | …strukturell-identitet | Hash-consing: like deluttrykk gir samme node og samme `key()`. Mål dedupliseringsfaktor på det faktiske registeret | Codex | test.reg.hash-cons-dedup | `TESTRESULT.md#hash-cons` |
| **WP10** | …goal-som-uttrykk · evaluering-der-dataene-er | Goals og betingelser som typede uttrykk (`real`/`vec`/`bool`). De som ikke lar seg uttrykke merkes prompt-Goal med navngitt grunn. Mål µs/kall inne i cellen mot over språkgrensen | Losen + Codex | test.reg.goal-uttrykk-dekning, test.reg.goal-uten-tokens, test.reg.evaluering-lokal | `contract/goals-som-uttrykk.md` |
| **WP11** | …en-semantikk | Referansetolk er sannheten. Konformansprøve med **nedskrevet trekkfordeling**, og negativ prøve der en uenig backend avvises i stedet for å gi stille galt svar | Codex | test.reg.backend-konformans, test.reg.ingen-stille-avvik | `TESTRESULT.md#backend-konformans` |
| **WP12** | …fasit-for-gating | Frys fasit (oppslag → forventet `purposeRef`), kvalitetsmål, baseline og beslutningsregel **før** sammenligning. Mål permutert null og fasitstyrt positiv kontroll på samme oppstilling | Kjetil (dommer) + Losen | test.reg.fasit-finnes, test.reg.null-og-positiv | `contract/fasit-oppslag.md` |
| **WP13** | …fasit-for-gating | Negativ prøve, fire tilfeller: null fjernet · positiv fjernet · begge like · referanse fra feil måleoppsett. Grønn status skal hindres, og riktig grunn følge med | Losen | test.reg.porten-hindrer-faktisk | `TESTRESULT.md#fasit` |
| **WP14** | …root (Q7) | Invarianskrav: to konfigurasjoner med samme retningsinformasjon skal ikke skilles på score alene. Både vektet statistikk og invariant test rapporteres; funn teller bare når begge forbedres | Losen | test.reg.invarians | `TESTRESULT.md#invarians` |
| **WP15** | …rammekostnad | Kostnadsprofil ved registerets faktiske N, 2N, 4N **og 100 000**. Rammebudsjett satt, og for lavt budsjett skal rapporteres, ikke skjules | Codex | test.reg.kostnadsprofil, test.reg.budsjett-rapporterer-for-lavt, test.reg.100k | `TESTRESULT.md#kostnadsprofil` |
| **WP16** | …token-okonomi | Token-andel målt før og etter på samme frosne korpus, med dato og korpusreferanse. Regresjon = rød | Losen | test.reg.token-andel | `TESTRESULT.md#token-andel` |
| **WP17** | …ukjent-feiler-lukket | Oppslag uten treff gir `purpose://prompt.unknown` differensiert etter polaritet, uten sideeffekt. Negativ test: match brukt som Grant avvises | Codex | test.reg.unknown-lukket, test.reg.match-gir-ikke-rett | `TESTRESULT.md#unknown` |
| **WP18** | …skal-ikke.profilering | Skann nodetyper: ingen node representerer en person. Forsøk på å legge til én avvises typet. Book 09 §7s fem løfter listes mot faktisk oppførsel | Losen | test.reg.ingen-person-noder, test.reg.book09-loftet | `ACCEPT.md#book09` |
| **WP19** | …celle | Konsumentene peker på registeret. Liste over hvilke, og hva som ble igjen med begrunnelse | Losen + Codex | test.reg.konsumenter | `ACCEPT.md#konsumenter` |
| **WP20** | …root | Ende-til-ende: tekst inn → klassifisering uten modell → purposeRef ut med score og forklaring; og ett oppslag som havner i `prompt.unknown` | Codex | test.reg.e2e | `TESTRESULT.md#e2e` |
| **WP21** | quality.docs-in-same-change | `Book/37_Purpose_Registry.md` beskriver registeret slik det faktisk ble | Losen | test.docs-updated, test.status-current | Book-kapittel |

## Utenfor denne planen

- **Overføringsprøven for `PurposeContract`** (§6 Q3b) — egen, liten PDD med eget G1. Den
  gjenbruker fasiten fra WP12 i stedet for å måle den to ganger.
- Swift-backend for nodegrafen (port 1) — egen PDD. Registeret skal virke tolket uten den.
- Palazzo-adapteren og ny kvalitetsevaluering — revisjonens punkt 4 og 5.
- Promotering av kandidatformål til kanonisk Book 23 — Kjetils beslutning, Book 23 §8.

## Rekkefølge og parallellitet

WP0 først. Deretter WP1 → WP2 → WP3. **WP4b kan starte nå** — den er ikke blokkert. WP4a starter når X0-kontrakten er skrevet; WP4 følger WP4a; WP5–WP7 følger WP4.
WP8–WP11 kan gå parallelt med WP5–WP7. WP12 starter i det B3 foreligger og blokkerer
WP13, WP14 og WP16. WP15 kan kjøre når WP3 står. WP17–WP21 til slutt.

Ingen pakke merkes ferdig før testene den navngir står med ekte utdata i `TESTRESULT.md`
eller som `blocked` med grunn.
