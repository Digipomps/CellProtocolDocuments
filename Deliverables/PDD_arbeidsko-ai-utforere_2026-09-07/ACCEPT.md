# ACCEPT — arbeidskø AI-utførere

Last verified against code: 2026-09-07. Dette er Codex' leveransekontroll,
ikke Kjetils G3-godkjenning. Samlet status: **blocked for ende-til-ende-aksept**.

| Forventning | Faktisk | Vurdering |
|---|---|---|
| Ett jobbformat, bakoverkompatibel CLI og schema | Levert med felles validator og negative tester | pass |
| Dispatcher, avhengigheter, lås, timeout, events og resultat | Levert og testet gjennom faktisk dispatch-kode med kontrollerte utførere | pass lokalt |
| Fungerende ekte Codex-jobb | HD-0013 app-server EPERM | blocked |
| Fungerende ekte Claude-jobb | HD-0014 Not logged in | blocked |
| Fungerende ekte cellejobb | HD-0015 lokal HTTP utilgjengelig fra sandkassen | blocked |
| Board/list/show og Cowork-veiledning | Egen seksjon, resultatevidens, 10 linjer, gammel veiledning merket | pass |
| Losen skriver fra Cowork, starter innen to minutter | Ingen faktisk mount/ny launchd-kjøring | blocked til WP7 |
| Feil blir lærdom og command/script nektes | KO-001 og fem nye lessons, inkl. de ekte feilstubbene | pass |
| Ingen selv-eskalering | Deklarert job-origin avvises ved økte rettigheter; ingen autentisering av fri JSON-skriver | avgrenset, ekte agentprøve blocked |
| Ingen git og ingen plist-installasjon | Ingen git mot HAVEN, men baseline-temp-fixture kjørte git; ingen plist installert | git-avvik dokumentert |

## docs

CONTRACT.md, AGENTS.md, Arbeidsko.md, Arbeidsko-drift.md og gammel LES_MEG.md
beskriver faktisk implementert oppførsel og er datert. TESTRESULT.md har samtlige
pålagte ankre, tydelig skille mellom simulert og ekte evidens og åpne blokkeringer.
Rapporten peker på lokale CLI-hjelpetekster og kildekoden til cellekontrakten.

## status

STATUS.md beholder G1/G2-godkjenningene. G3 er blocked; WP7 forblir Kjetils.
Ingen ny GUI eller runtime-rettighet er implisitt godkjent her.

## stubs

`tools/executors/claude_cloud.py` er den eneste tilsiktede utførerstubben:
exit 78 og `status: not-implemented`, med forklaring om oppstart fra Claude-økt.
Ingen celle eller server-endepunkt er implementert som no-op. Cell-adapteren
bruker eksisterende autentisert Porthole-kontrakt; levende runtime gjenstår.
