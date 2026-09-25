# Handoff — felles regler for Codex-slicer i denne PDD-en

Oppgavemappe (P): `CellProtocolDocuments/Deliverables/PDD_scaffold-admin-delegering_2026-09-08/`, relativt HAVEN-roten. Sett alltid cwd til HAVEN-roten.

1. **Én jobb, ett formål.** Hver slice svarer til én arbeidspakke i `P/PLAN.md` og ett bladformål i `P/FORMAALSSPEC.md` §1.
2. **Leveransestien står på linje 3 i `.job`.** Ligger den ikke under cwd, avviser runneren jobben.
3. **`workspace-write` er obligatorisk** for enhver slice som skriver noe.
4. **Ingen git.** Ingen commit, push, merge eller branchbytte. Integratoren gjør det.
5. **Ingen docker, ingen deploy.** Deploy-steg er HAVEN-Deploy-poster med eier Kjetil (`lesson.codex-sandbox-cannot-reach-docker`).
6. **Ekte tall.** Testantall og feil limes inn fra faktisk kjøring, aldri fra en tidligere rapport (`lesson.baseline-count-from-report-not-run`).
7. **Forhåndssjekk først.** Hver slice starter med å verifisere at arbeidstreet er som forventet. Stemmer det ikke: stopp, skriv én linje i `P/STATUS.md` om at slicen er blocked, ikke bruk tid på en full kjøring.
8. **Blocked er et gyldig utfall.** En test som ikke kunne kjøres registreres som `blocked` med årsak — aldri stille droppet.
9. **Sluttmelding** nederst i leveransefila: `## WP<n> — sluttmelding`, med hva som ble gjort, hva som ikke ble gjort, og hva neste slice trenger.
10. **Ingen ny myndighet fra rolleetiketter.** Ingen slice i denne PDD-en har lov til å innføre en kodesti der `admin.observer/operator/nodeAgent/security` gir cellemyndighet. Dette er formålet `role-label-grants-nothing`, og WP4 er regresjonsvernet.
11. **Stier er relative til repoet.** I prompts, dokumentasjon, kontrakter og kode skrives stier relativt (`CellScaffold/Sources/...`, `handoff/...`), aldri som `/Users/<navn>/...`. Hvor repoene ligger er en maskininnstilling; strukturen inne i repoene er lik for alle. Rå logg- og feilutdata limes inn ordrett og er unntatt — det er bevis, ikke instruks.
12. **Arbeidstre for denne PDD-en:** `CellScaffold/_wt-sad-20260909`, branch `pdd/scaffold-admin-delegering`, opprettet fra `main` `e1f3e22f`. Det delte CellScaffold-treet står på en annen PDD og skal ikke røres.

