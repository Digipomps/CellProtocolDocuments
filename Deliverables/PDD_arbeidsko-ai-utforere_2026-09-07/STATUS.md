# STATUS — arbeidsko ai utforere

- surfaces: cell, codex, scaffold, terminal
- tags: agent, celle, claude, codex, deploy, ko, launchd

## Porter
- G1: godkjent 2026-09-07 (Kjetil: «ingen grunn til å ikke gjøre det»; §6: samme kø som HAVEN-Deploy, claude-local primær (Claude Code 2.1.221 funnet), AIGatewayCell-adapter nå, bare Kjetil/Losen kan legge workspace-write, GUI etter)
- G1-GUI: ikke relevant        (rendret bilde godkjent — bare for GUI-oppgaver)
- G2: godkjent 2026-09-07 (auto — samme bestilling)
- G3: blocked 2026-09-07 — implementasjon og lokale tester levert; ekte Codex/Claude/celleprøver stoppet, Cowork/launchd-e2e avventer Kjetils WP7. Ikke godkjent.

Sett en port til `godkjent <dato>` kun når Kjetil har sagt det. `purpose_dev.py validate <mappe>` nekter porter uten artefakter.

## Planbytter (dato — hvorfor)
-

## Logg
- 2026-09-07: opprettet
- 2026-09-07: iterasjon 1 sendt Kjetil for G1 (parallelt med Codex-jobb husk-impl)
- 2026-09-07: WP0–WP6 lagt i _losen-queue som arbeidsko-impl-20260907-2006 (kjører etter sicilia-impl)

- 2026-09-07: Codex utførte WP0–WP6 i rekkefølge. 88 tester, 87 bestått og én git-fixture skippet ved sluttkontroll; hd validate 267 poster/0 problemer.
- 2026-09-07: Ekte dispatcher-prøver HD-0013 (Codex EPERM), HD-0014 (Claude Not logged in), HD-0015 (lokal HTTP nektet) står HANDOFF_REQUIRED med evidens og lessons.
- 2026-09-07: Plist skrevet/validert, ikke installert. WP7 er fortsatt Kjetils; WP-GUI fortsatt blocked til bilde. TESTRESULT.md, ACCEPT.md og HAVEN-Deploy/docs/Rapport_Arbeidsko_2026-09-07.md er skrevet.
- 2026-09-07: Avvik registrert: baseline-testen kjørte git i temp-fixture før dette ble oppdaget; videre git sperret av test_no_git.py. Ingen git mot HAVEN-repoene.
- 2026-09-07: Kildekorreksjon: endpoint er cell:///AIGateway, med autentisert Porthole-handling aiGateway.ai.invoke. Polling støttes for konfigurert asynkront tekstendepunkt; dagens Porthole svarer synkront.
