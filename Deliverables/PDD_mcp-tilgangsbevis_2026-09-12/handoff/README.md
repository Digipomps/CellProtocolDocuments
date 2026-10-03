# handoff — rekkefølge og forventet utfall

Stier relative til `HAVEN/`. Alle jobber legges i `_losen-queue/inbox/` som `<id>.prompt.md` **først**, så `<id>.job` via `mv` fra tmp (`lesson.queue-job-file-before-prompt`). Ingen git gjennom VM-monteringen.

| # | Jobb | Sandkasse | Leveranse | Forventet utfall | Går når |
|---|---|---|---|---|---|
| 1 | `A1-goaldefinition` (`A1-goaldefinition.prompt.md`) | workspace-write | `handoff/A1-RAPPORT.md` | Fire filer endret på branch `pdd/goal-definition-in-purpose`, 4 nye tester, rapport «skrevet, ikke verifisert» | Kjetil sier G2 / «kjør A1» |
| 2 | `A1-build` (detached skript, `danger-full-access`, `swift build --disable-sandbox --build-tests` + `xctest` på CellBaseTests) | — | `.tmp-clang-module-cache/a1-build.log` + exit-fil | Bygg grønt, 4 nye + 5 eksisterende engine-tester + 5 composition-tester grønne | Rett etter 1 |
| 3 | `A1-commit` | workspace-write | PR-lenke i `A1-RAPPORT.md` | `git rev-parse pdd/goal-definition-in-purpose != origin/main`; CI grønn | Rett etter grønt bygg (`lesson.branch-is-empty-after-eight-work-packages`) |
| 4 | `A2-vectors` … | | | | Etter K3 |

Tørrkjøring: hver `.prompt.md` kan leses uten å kjøres; jobb 2 sitt skript støtter `--dry-run` (standard) og `--go`.

Ferdig: `handoff/CODEX_REVIEW_PERSPECTIVENODE.md` (12.09), `panel/ASTRA_SVAR.md` (i kø 13.09).
