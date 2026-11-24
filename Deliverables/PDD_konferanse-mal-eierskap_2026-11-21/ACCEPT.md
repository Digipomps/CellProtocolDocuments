# Aksept — konferanse mal og eierskap (fase 1)

Forventning (FORMAALSSPEC §3) mot det som faktisk ble levert. Skrevet 2026-11-24 av Losen.

| Leveranse | Forventet | Faktisk | Status |
|---|---|---|---|
| Kontrakt for arrangør, arrangement og mal v0 | `Book/conference_entity_template_v0.json` | Finnes på main (CellProtocolDocuments #58), med lagringsvalget ført inn | levert |
| Fixtures, gyldige og ugyldige | `contract/fixtures/` | 13 fixtures, ett eller flere per bladformål | levert |
| Validator | `checks/validate_contract.py`, TESTRESULT#contract | 13/13; blir rød når to fixtures endres | levert |
| Måling av lagring av en uregistrert nøkkelsti | TESTRESULT#lagring | Alle seks stier «lagret» i begge ankrene etter WP4; ingen stille tap | levert |
| Lagring av malens røtter (WP4, lagt til etter Kjetils valg 21.11) | ikke i §3 opprinnelig | `EntityTemplateRoots.swift` + intercepts i begge EntityAnchor (CellProtocol #103); 4/4 + 38/38 på Mac | levert |
| `ConferenceDefinition` med eier og mal | CellScaffold-PR, grønn testmengde | #498 merget; 3/3 på Mac; CI-port grønn | levert |
| Book 37 oppdatert | diff i `Book/37_EntityData.md` | §7b, «Last verified» oppdatert | levert |
| Brevet til Vegar | sendt brev med messageID | Sendt 24.11, seq 39, messageID 6EFDA6B3-A6D1-49D7-A616-FE981870B6FD | levert |

## Avvik

- WP4 sto i planen bare som «hvis WP1 viser stille tap». Lesingen av koden viste i stedet at nye røtter ble avvist høyt. Kjetil valgte likevel å åpne røttene (valgkort 21.11 13:39Z), så WP4 ble gjort.
- Målingen ble tatt etter WP4 og viser derfor ikke tilstanden før. Tilstanden før er lest i koden, ikke målt.
- Hele CellScaffold-testmengden er ikke kjørt lokalt; CI-porten bygger alle mål.

## docs

- [x] Book 37 §7b
- [x] Kontrakten bærer lagringsvalget
- [x] Lærdommen `lesson.entityanchor-keypaths-are-registered` er oppdatert (se P6)

## status

STATUS.md speiler G1, G2, G3 og leveransene. G3 godkjent av Kjetil 24.11.

## stubs

Ingen tomme stubber i endrede filer (`EntityTemplateRoots.swift`, begge `EntityAnchorCell.swift`, `ConferenceDomainModels.swift`).

## svar-vegar

Sendt 24.11 etter Kjetils «G3 godkjent og send»: relasjon vegar, seq 39, messageID 6EFDA6B3-A6D1-49D7-A616-FE981870B6FD. Agenda-deling på tvers av vaults besvares separat.
