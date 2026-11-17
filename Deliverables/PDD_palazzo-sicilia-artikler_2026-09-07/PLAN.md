# PLAN — Sicilia-artikler (PDD_palazzo-sicilia-artikler_2026-09-07)

G1 godkjent 2026-09-07 (Kjetils ord) med §6-forslagene som beslutninger. G2 auto. G1-GUI godkjent 2026-09-07 — WP-GUI kjører (handoff/GUI.md).
Bygger på husk-oppgaven (levert 2026-09-07, 82/82). Repo: `HAVEN/PalazzoScaffold`. Utfører: Codex via `_losen-queue`.

| WP | purposeRef | Utfører | Hva | Tester | Status |
|---|---|---|---|---|---|
| WP0 | pkg.std.everything-works | Codex | Baseline-kjøring (forventet ≈ 82, fra Rapport_Husk 2026-09-07 — bekreft ved kjøring). | test.build, test.regression | GODKJENT |
| WP1 | articles-published-with-tags + articles-are-signals | Codex | `PalazzoPublishedContent.articles` får `id`, `region`, `origin` (opphav/kilde), `tags`; samme tagg-flyt som retter (`content.draft.tags.*` dekker artikler; `PalazzoTagLexicon` utvides med sicilianske retter/steder/råvarer). `content.publish` kompilerer `PalazzoContentSignal(kind: article)` for artikler med godkjente tagger; `content.signals` returnerer begge kinds; husk-matcheren matcher artikkelsignaler likt. | test.sicilia.articles, test.sicilia.signal | GODKJENT |
| WP2 | reaction-becomes-record + persistent | Codex | Ny keypath `entity.article.react` (set, owner) payload `{articleID, reaction: wantToTaste|interesting|notForMe, comment?}` → skriver via eksisterende record-append: wantToTaste→`purpose`, interesting→`interest`, notForMe→`interest` med `attributes.polarity="negative"`, comment→`interaction` (gjestens tekst). `title` = artikkeltittel, `tags` = artikkelens godkjente tagger, `source: self`. Persistens: test kaster cellen og laster snapshot. | test.sicilia.reaction, test.sicilia.persist | GODKJENT |
| WP3 | queryable-by-consent | Codex | `insight.interests` returnerer `interests` (uten negative) og ny `avoid` (negative); `insight.purposes` uendret + artikkeltagger. Uten policy → denied (som i dag). | test.sicilia.query, test.cell.auth-negative | GODKJENT |
| WP4 | no-reading-surveillance (antiformål) | Codex | `guest.article.configuration` (get) og artikkellisting skriver aldri poster/events med gjest+artikkel; test åpner konfigurasjonen og sjekker at `entity.records` og event-loggen er uendret. | test.sicilia.no-tracking | GODKJENT |
| WP5 | tester + ruter + docs | Codex | `Tests/AppTests/PalazzoSiciliaTests.swift` (testnavn = testRef), ruter `/api/entity/article/react`, `/api/guest/article/configuration`; README + `docs/Remember_contract` oppdatert; TESTRESULT.md/ACCEPT.md/rapport. | test.sicilia.e2e (HTTP) | GODKJENT |
| WP6 | (innhold) | Losen | 8 artikkelutkast i `content/artikler_v1.md` med opphav/kilde og foreslåtte tagger; seed-JSON i `content/artikler_v1.json` som WP5 bruker som fixture. | artefakt | Losen |
| WP-GUI | gui.* | Codex | Fabrikker: «Fra Sicilia»-seksjon i gjesteflaten (liste), `guest.article.configuration` (åpen artikkel + tre knapper + kommentar), husets artikkel-utkast i draft-flaten. 1:1 med `skeleton/*.json`. | test.skeleton.* | GODKJENT (G1-GUI 2026-09-07) → handoff/GUI.md G1–G6 |

Ikke i planen: anbefalt rekkefølge, lesestatistikk, artikler fra andre hus.
