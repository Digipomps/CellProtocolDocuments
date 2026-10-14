# ACCEPT — Sicilia-artikler, WP0–WP5

Last verified against code: 2026-09-07

| Forventning | Faktisk resultat | Status |
|---|---|---|
| WP0: eksisterende kode bygger og tester | Rent baseline-bygg; 82/82 før endringer. Innledende krasj og tiltak er dokumentert i TESTRESULT. | Verifisert |
| WP1: artikler med ID, kilde, region og godkjente tagger | PalazzoArticle, bakoverkompatibel dekoding, felles taggflyt og PalazzoContentSignal(kind: article); 8 seed-fixtures. | Verifisert |
| WP2: eksplisitte reaksjoner blir varige poster | Samme append/snapshot som entity.record, self, negativ polaritet, ordrett kommentar; faktisk fil- og prosesslasting. | Verifisert |
| WP3: samtykkestyrte spørsmål | interests og avoid hver for seg; purposes beholder formatet. 403 uten policy/etter revoke. | Verifisert |
| WP4: ingen lesesporing | Uendrede records/events ved HTTP-lesing; statsløs Text-konfigurasjon. | Verifisert |
| WP5: ruter, tester og docs | To nye ruter, discovery, 13 tester, dokumentasjon og evidens. Hele suiten 95/95. | Verifisert |
| E2E med prosessomstart | To separate XCTest-prosesser; samme datalager; faktiske Vapor-ruter via XCTVapor; tre identiske poster etter omstart. | Verifisert |
| Supplerende ekstern TCP-HTTP-test | Run kunne ikke binde lokal port i sandboxen. Reproduserbart script og råfeil foreligger. | Ikke verifisert |
| WP-GUI: artikkelvelger, liste, knapper, kommentarfelt og husets nye draft-GUI | Ingen fabrikkendringer. Kun tillatt midlertidig Text-visning av alle publiserte artikler. | BLOKKERT i denne kjøringen |

## docs

README.md og docs/Remember_contract_2026-09-07.md oppdatert og datert. TESTRESULT.md dekker alle etterspurte ankre. Rapport ligger på stien overleveringen ba om i PalazzoComunaleScaffold/docs; all implementasjon ligger i PalazzoScaffold.

## status

WP0–WP5 er implementert og verifisert innenfor rammen ovenfor. STATUS.md er supplert med denne kjøringens faktiske resultat. Ingen godkjenning fra bruker er utledet av testresultatene. G3 for hele pakken, inkludert GUI, er ikke erklært godkjent.

## stubs

Ingen ny no-op-handler. entity.article.react validerer, henter publisert artikkel, skriver og persisterer. guest.article.configuration henter og viser publisert tekst; tilgjengelighet og tomtilstand har eksplisitt resultat. De eksisterende fabrikkene er uendret.

## avvik

- Før-baseline krevde rensing/gjenbygging av genererte byggeprodukter; ingen kilde- eller testendring for å få 82/82.
- Minimal konfigurasjon er en samlet Text-visning. Ingen state for valgt artikkel eller GUI-handlinger er innført.
- Eldre snapshots og seed uten ingress/kilde/region får tomme standardfelt. Seed-fixturen har åtte opphavsfelt, men ingen ingress; faktainnholdet er ikke redaksjonelt godkjent av denne implementasjonen.
- Stående menuChange-policy gjelder fortsatt bare menyendringer. Artikkeltreff bruker de samme eksakte match-grantene per treff; en ny stående artikkelpolicy er ikke innført.
- Ukjent prompt-formål avvises ved access.request. Andre formålstekster er fortsatt beskrivende metadata, ikke en ny generell formålsmotor.
- TCP-smoke er blokkert av miljøet. Prosesspersistens og appens HTTP-ruter er testet separat med to XCTest-prosesser.
- Explore-audit for PalazzoScaffold er grønn. Funnene i den lesende CellProtocol-auditen ligger utenfor oppgaven og er beholdt som åpne.
