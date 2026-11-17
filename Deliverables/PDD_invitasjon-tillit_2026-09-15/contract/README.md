# contract/ — invitasjon og tillit

`invite_v1.json` er kontrakten: det som finnes (lest mot origin/main 23.09, stier i `sources`) og det
som er planlagt (merket med WP-nummer fra PLAN.md). `invariants` er formålene skrevet som regler.
`fixtures/` er positive og negative eksempler; `check_fixtures.py` kjører reglene mot dem uten
avhengigheter. Alle personer og adresser i fixtures er oppdiktede.

`python3 contract/check_fixtures.py` → `12 fixtures, 0 avvik` er kravet for `test.cell.contract-fixtures`.
