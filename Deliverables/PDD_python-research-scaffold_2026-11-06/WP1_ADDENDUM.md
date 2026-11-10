# WP1 — autorisert tillegg 2026-11-07

Brukeren godkjente planen og krevde CellBridge-svar fra andre scaffolds. WP1 bygger derfor en inbound WebSocket CellBridge i tillegg til lokal resolver/runtime.

- Ny ResearchRuntime-celle: offentlig, dataminimal runtime.publicStatus; beskyttet runtime.state, probe.start, job.cancel, jobs.<id>.state/events/result og Flow.
- runtime.probe/v1 er en faktisk avgrenset beregningsjobb for å verifisere supervisoren, ikke den fremtidige forskningsanalysen. Datasett-, analyse- og figurceller kommer i WP2–WP5.
- Default listener er loopback. Ekstern nettverkseksponering krever TLS; ingen deploy eller offentlig drift aktiveres her.
- Eide celler beholdes. Fjernklienter må stå i eksplisitt lokal nøkkel-/rettighetsliste og bevise nøkkelkontroll med eksisterende IdentitySigningChallenge over reverse sign. Det er en smal cellepolicy, ikke full Agreement-admission-paritet.
- WebSocket-mottaker skal håndtere tekst/binær, meldingsgrenser, samtidig sign-svar, timeout og disconnect. Anonym feed må avvises uten upstreams owner-fallback.
- Akseptanse: lokal runtime, isolert PyCellProtocol-baseline, ekte TCP/WebSocket-kall fra separat scaffold-klient, negative adgangstester, to abonnenter, persistens/idempotens, kø, cancel/timeout/restart og wheel/installasjon. Swift-integrasjon prøves mot faktisk CellBase; eventuelle uverifiserte grenser rapporteres eksplisitt.

Baseline 2026-11-07: PyCellProtocol HEAD 5a6e19f48676dfc090163916787fa1abcd5aa4d5, rent arbeidstre, arm64 Python 3.11.14, kommando python -m pytest -q -p no:cacheprovider: 46 passed in 0.48s, exit 0. Ingen PyCellProtocol-kilde endret.
