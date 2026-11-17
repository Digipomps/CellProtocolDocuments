# Bokprosjektet – regenerering stoppet 2026-09-23

Status: **Stoppet ved forutsetningskontrollen. Ingen regenerering utført.**

Kontrollert 23. september 2026 kl. 13:12 CEST (11:12 UTC).

## Forutsetningen

GitHub API bekreftet at `Digipomps/CellProtocol/main` pekte på
`03d173881e8d6c662b402f716c985572b91d3183`. Lokal `origin/main` pekte på samme
commit. Skjemaet ble lest fra dette Git-objektet, ikke fra arbeidskopien:

`Docs/EntityData-Review-2026-09-11/EntityData.v2.schema.json`

| Krav før oppstart | Resultat |
| --- | --- |
| `groups.<uuid>.partOf` finnes på `origin/main` | Ikke oppfylt. Gruppeobjektet har bare `name` og `members`. |
| `relations.bokprosjekt` er tatt ut | Ikke oppfylt. Feltet finnes fortsatt i `properties.relations.properties`. |

Gruppeobjektet har dessuten `additionalProperties: false`; `partOf` er dermed
ikke tillatt i den kontrollerte skjemaversjonen. Forutsetningen som jobben
`grupper-partof-20260923` skal levere, var ikke på `main` ved kontrollen.

Kilder: [main via GitHub API](https://api.github.com/repos/Digipomps/CellProtocol/branches/main)
og [skjemaet i kontrollert commit](https://github.com/Digipomps/CellProtocol/blob/03d173881e8d6c662b402f716c985572b91d3183/Docs/EntityData-Review-2026-09-11/EntityData.v2.schema.json).

`git fetch --no-tags origin main` svarte ikke og ble avbrutt med exit 130.
Den ferske fjernkontrollen ble derfor utført med en lesende GitHub-API-forespørsel.
Ingen deltakerdata ble sendt til GitHub.

## Data og endringer

| Generert i denne kjøringen | Antall |
| --- | ---: |
| Entiteter | 0 |
| Rotgrupper, nivå 1 | 0 |
| Kapittelgrupper, nivå 2 | 0 |
| Arbeidsgrupper, nivå 3 | 0 |
| Medlemskap | 0 |
| Relasjonsposter | 0 |

Ingen resultatdata ble skrevet; det finnes derfor ingen ny resultatsti å oppgi.
Regnearket `Binding/.sprout/import/HAVEN_import_bokprosjekt.xlsx` ble ikke åpnet
eller endret. Oppgitt antall 189 deltakere er ikke kontrollert mot kilden.

Ingenting ble slettet. Den gamle importkoden i
`CellScaffold/Sources/App/Support/BookProjectEntityPresenceSupport.swift` og
eventuelle gamle importdata er urørt. Ingen generator eller fixtures ble endret.
Eksisterende endringer i arbeidskopiene ble ikke tatt med eller endret.

Eneste nye prosjektfil fra denne kjøringen er denne rapporten:
`CellProtocolDocuments/Deliverables/BOKPROSJEKT_REGENERERT_2026-09-23.md`.
Rapporten inneholder ingen deltakerdata. Ingen commit, staging eller push ble utført.

## Kontroller som ikke ble kjørt

Regenerering og tilhørende kontroller ble stoppet etter brukerens uttrykkelige
instruks om ikke å bygge mot et skjema som ikke finnes:

- Radantall mot antall entiteter: ikke kjørt.
- Medlemskap, mest spesifikke gruppe og dobbeltelling: ikke kjørt.
- Gyldige foreldrereferanser og fravær av sykler: ikke kjørt.
- Validering av et generert resultat mot målskjemaet: ikke kjørt; intet resultat finnes.
- Ingen `relations.records` ble laget; dette er ikke en attestasjon av eksisterende data.
- Lesing av gammel gruppeutledning, implementering, Swift-bygg og tester: ikke kjørt.

Arbeidet kan gjenopptas når begge skjemaforutsetningene er bekreftet på
`CellProtocol/origin/main`. Først da skal gammel import erstattes, nye tilfeldige
UUID-er genereres, resultatstien kontrolleres med `git check-ignore -v`, og
deltakerdata genereres og valideres.
