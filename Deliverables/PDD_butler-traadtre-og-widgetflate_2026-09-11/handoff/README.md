# Handoff — rekkefølge og kommandoer

Alt Codex-arbeid i denne oppgaven startes som køjobb: to filer i `_losen-queue/inbox/` (`<id>.prompt.md` først, `<id>.job` sist, se `_losen-queue/LES_MEG.md`). Kjetil limer aldri inn kommandoer for å starte Codex (`lesson.paste-command-instead-of-queue`). Køen kjører én jobb om gangen.

## Rekkefølge (fra PLAN.md §0)

1. `skjelett-gap-tre-20260912`, `-chat-`, `-flate-` — i kø 2026-09-12 20:27Z. Leveranse: `handoff/SKJELETT_GAP_*.md`, `skjelett/`.
2. Claude: `handoff/SKJELETT_ELEMENTER.md` (syntese) → Astra-motsvar → **Kjetils ja** til listen. Ingen ny skjelettkapabilitet før det.
3. WP-R som køjobb(er) på worktree fra `origin/main`, gren `pdd/skjelett-elementer`. Bygg og tester som detached skript, ikke i sandkassen.
4. A-grenen og B-grenen parallelt (to uavhengige PR-er).
5. Iterasjon (WP-K3) mot staging når WP-R er deployet dit.

## Kommandoer (repo-relative; kjøres på Mac)

Preview av et kandidatskjelett mot staging (standard `CONFERENCE_DEMO_BASE_URL` er staging, se `CellScaffold/scripts/skeleton-iterate.js:10`):

    cd CellScaffold && npm run skeleton:iterate -- --mode preview --scenario ../CellProtocolDocuments/Deliverables/PDD_butler-traadtre-og-widgetflate_2026-09-11/skjelett/tre.preview.json

Artefakter i `CellScaffold/test-results/skeleton-iterate/…` (skjermbilder, DOM, konsoll). Preview endrer ingenting persistent; `commit-runtime` brukes ikke i denne oppgaven før WP-B2b har bevist at Butler-konfigurasjonen er source-backed editable.

Rendre referansebildene på nytt:

    cd CellProtocolDocuments/Deliverables/PDD_butler-traadtre-og-widgetflate_2026-09-11/images && node render.js

Bundet bygg av CellScaffold (eksisterende starter på `origin/main`):

    cd CellScaffold && scripts/run_swift_bounded.sh build --build-tests

## Hvem kan kjøre iterasjonene

`skeleton-iterate` trenger nettverk mot staging. Codex-sandkassen (`workspace-write`) har det ikke i dag. To veier, Kjetils valg: (a) nettverk for `workspace-write` i Codex-konfigurasjonen, så WP-K3 kan gå som køjobb; (b) Claude kjører iterasjonene gjennom Chrome på Kjetils maskin og legger skjermbildene i `images/`.

## Grenser
Ingen git gjennom mount. Ingen `system prune`. Ingen endring i `/etc/haven`. Prod bare etter verifisert staging (R-D24).
