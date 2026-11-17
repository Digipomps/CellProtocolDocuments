# Codex-handoff — «Husk det jeg sa» (2026-09-05)

Kjør fra HAVEN-roten:

```bash
/Users/kjetil/.local/bin/codex exec --full-auto -C /Users/kjetil/Build/Digipomps/HAVEN "Les /Users/kjetil/Build/Digipomps/HAVEN/CellProtocolDocuments/Deliverables/PDD_palazzo-husk-det-jeg-sa_2026-09-05/handoff/README.md og utfør slicene som er merket GODKJENT, i rekkefølge. Svar kun med rapporten."
```

## Objektiv
Implementere formålstreet i `../FORMAALSSPEC.md` §1 i `HAVEN/PalazzoScaffold` etter `../PLAN.md` (WP0–WP10), slik at alle `test.husk.*` i §5 er grønne, de 48 eksisterende testene fortsatt er grønne, og staging-imaget bygger.

## Les først (i denne rekkefølgen)
1. `../PLAN.md` — arbeidspakkene, hva hver skal levere.
2. `../contract/palazzo_remember_contract_v0.json` + `../contract/fixtures/*.json` — bindende keypaths, typer, regler og testfixtures.
3. `../dataflow.md` — kantene; hver kant skal finnes i en kontrakt.
4. `../skeleton/*.json` — fabrikkene skal produsere 1:1 disse elementene. Feltet `_verify_in_porthole` i hver fil sier hva som er usikkert og hvilken fallback som gjelder.
5. `../images/README.md` — hva bildene viser og hva skeleton ikke kan rendre.
6. `PalazzoComunaleScaffold/docs/Rapport_PalazzoScaffold_Celler_2026-09-03.md` — hvordan pakken bygges (`--disable-sandbox`), og feilene fra forrige runde.

## Slicer

| Slice | Status | Innhold |
|---|---|---|
| S0 baseline | GODKJENT | WP0: `swift build --disable-sandbox` og `swift test --disable-sandbox` før endring. Noter testtall. |
| S1 signaler + tagger | GODKJENT | WP1. |
| S2 match i gjestens entitet | GODKJENT | WP2. Matcheren bak protokollen `PalazzoSignalMatcher` — ikke hardkod i cellen. |
| S3 to grants | GODKJENT | WP3. Gjenbruk `makeAgreement`-mønsteret; utsteder = gjest. Ingen ny CellProtocol-mekanisme. |
| S4 tillitspakke | GODKJENT | WP4. Allowlist-nøkler fra kontrakten er uttømmende. |
| S5 huset mottar bare pakken | GODKJENT | WP5, inkl. deprecation av `insight.query.interests.match` (aldri `matches`/`score` igjen). |
| S6 tilbaketrekk | GODKJENT | WP6. |
| S7 fabrikker | GODKJENT | WP7. Bruk kun elementtyper som finnes i `CellBase/Skeleton/SkeletonDescription.swift`. |
| S8 tester + ruter | GODKJENT | WP8. Ny fil `Tests/AppTests/PalazzoRememberTests.swift`. Testnavn = `testRef` fra §5 (f.eks. `testHuskTrustPacketTamperFails`). |
| S9 docs | GODKJENT | WP9. |
| S10 deploy staging | GODKJENT | WP10: `docker compose --profile staging build` og `up`, e2e mot container. Mangler docker/ssh-nøkkel → skriv `blocked` med årsak, ikke omgå. |
| S11 paritet | BLOKKERT | WP11 gjøres av Losen etter rapporten. |
| Artikler om Sicilia | BLOKKERT | Egen PDD (`PDD_palazzo-sicilia-artikler_2026-09-07`), venter G1. Ikke rør. |

## Regler
- CellProtocol røres ikke. Rett i PalazzoScaffold-pakken.
- Ingen eksisterende test fjernes eller svekkes. Testen som i dag forventer overlap fra `insight.query.interests.match` endres til å forvente `status: deprecated` — og det noteres i rapporten som en bevisst kontraktendring (FORMAALSSPEC §6.1).
- Autorisasjon: hver ny handler kaller `validateAccess` med keypathen den faktisk betjener (ikke arv CellScaffold-hullet). `match.*` get er owner-only: hus-requester skal få `denied`, ikke tom liste.
- Ingen språkmodell noe sted. Taggforslag og forklaring er ordliste + mal.
- Ingen no-op-stubber uten `status: "not-implemented"`.
- Ikke git gjennom mount; ikke commit. Kjetil committer.

## Rapport (obligatorisk, sist)
Skriv `/Users/kjetil/Build/Digipomps/HAVEN/PalazzoComunaleScaffold/docs/Rapport_Husk_2026-09-05.md` med:
1. Rå utdata (siste 30 linjer) fra `swift build` og `swift test` før og etter; testtall før/etter.
2. Per slice: gjort / avvik fra PLAN / hvorfor.
3. Per `_verify_in_porthole`-punkt: hva som ble valgt.
4. Filliste (nye/endrede).
5. Docker: utdata eller `blocked: <årsak>`.
Og fyll `../TESTRESULT.md` med ankrene `#build #regression #signal #tags #match #explanation #grants #trust-packet #house #no-label-leak #revoke #no-inference #e2e #auth #deploy` — rå utdata under hvert, `blocked: <årsak>` der noe ikke kunne kjøres.
