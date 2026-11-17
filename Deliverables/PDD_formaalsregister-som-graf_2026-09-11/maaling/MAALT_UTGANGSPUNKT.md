# Målt utgangspunkt for formålsmatching (2026-09-11)

Alle tall er kjørt, ikke antatt. Skript ligger i samme mappe.

| Mål | Dagens tag-matcher (`purpose_dev.py lookup`) | Deterministisk TF-IDF, topp-10 |
|---|---|---|
| Jaccard mellom oppgavepar | 0,82 | **0,20** |
| Lærdommer returnert til ALLE 18 oppgaver | 23 | **0** |
| Vist per oppgave | 34,9 av 44 | 10 |
| Kjøretid hele korpuset | — | 109 ms (inkl. Python-oppstart) |

Korpus: 44 lærdommer, 57 Book 23-noder, 19 PDD-oppgaver. Spørringen i TF-IDF-varianten
er §0-intensjonsteksten i `FORMAALSSPEC.md`; dokumentene er lærdommenes
symptom + cause + prevention + tags. Ren stdlib, grov norsk stamming (7 og 5 tegn).

**Kvalitativ kontroll:** arbeidskø-oppgaven får `paste-command-instead-of-queue`,
`codex-sandbox-cannot-reach-docker`, `codex-workspace-write-cannot-build-cellscaffold`.
Skjelett-paritetsoppgaven får `test-corpus-is-not-shipped`,
`unresolvable-condition-is-invisible`, `scaffold-without-porthole-has-no-preview`.
Treffene er riktige uten et eneste AI-kall.

## Hva dette ikke beviser

TF-IDF er en pose med ord: ingen struktur, ingen negasjon, ingen forplantning langs
kanter. Den skiller bedre enn tags, men den kan ikke vite at «deploy» henger sammen
med «rollback». Og uten fasit — hvilke lærdommer som faktisk var relevante — er 0,20
bare *spredning*, ikke *presisjon*. Spredning uten fasit kan oppnås ved å velge
tilfeldig; det er fasiten som skiller matching fra støy.

## Andre mål som holder

- Bare **15 av 44** lærdommer er referert fra en formålspakke og kan bli en `derivedTest`.
  **29** må huskes av et menneske.
- **0 av 44** er døde: alle når fram til minst én oppgave. Selektiviteten er problemet,
  ikke innholdet.
- Gjentatte temaer: `codex` 9 par, `handoff` 5, `gui` 3.
- Gjentakelsesmålet selv er **forkastet**: 16 par ved terskel «2 felles tags», 0 ved 3.
