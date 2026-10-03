# STATUS — conference release repair

- surfaces: cell
- tags: conference, deployment, transport
- G1: godkjent 2026-09-29 – brukerens eksplisitte godkjenning av anbefaling 1–4; se FORMAALSSPEC.
- G1-GUI: ikke relevant for nåværende rettelser; eksisterende flater beholdes.
- G2: godkjent 2026-09-29 – samme eksplisitte gjennomføringsordre; PLAN konkretiserer de fire leveransene.
- G3: venter – ingen sluttakseptanse eller fullført release.

## Oppdatert 30. september

Kjetil avgrenset neste deploy til de tre rettelsene og ba om koordinering med Claude. Losen svarte og reserverte bane a: Codex eier integrasjon/test/PR; Losen eier review/merge/release. De fire opprinnelige leveransene beholdes som åpne der akseptansen ikke er oppfylt; egen runtime er utenfor denne PR-en.

- Ny base `a8f03c2a02b32deb6a87a0da53b753f82e2d1382`; PR276 head `683c1411ce1f941e89bdb66d2ca9b171a57520ad` på `codex/conference-release-20260930`.
- To Workbench-regresjoner kompilerte på uendret main og feilet som forventet (12 assertions, 0 uventede feil).
- Kandidaten kompilerte og alle 29 berørte tester er grønne (8 admin, 8 Workbench, 13 portefølje), inkludert de seks nye metodene. Pins uendret. Linux-CI 36647213012 er fullført grønn; ingen merge/deploy.
- Kapasitetsvakten passerer uten overrides. Losen har avklart at 5-prosentregelen fra commit 515a37b7 gjelder; AGENTS har foreldet 10-prosenttekst. Den separate preflightregelen ENV-001 bruker fortsatt 10 prosent uten reserve; dens scope er ikke avklart eller endret.
- Eksisterende HD-0141-claim, HD-0077-demo og fersk vertskapasitet må avklares av køeier før staging. Prod-release inkluderer mer enn disse tre rettelsene og avklares separat av Losen.
- Mac-en ble låst etter første koordinasjonssvar. Ny PR-status er lagret i handoff/køposter, men ikke sendt i Claude-vinduet ennå.

## Historiske observasjoner 29. september
- Signert admin-håndtrykk lokalt og offentlig TLS verifisert. Rootårsak i callbackrekkefølge isolert i pinnet avhengighetskilde.
- Admin-rettelse og fire livssyklustester skrevet i isolert gren codex/conference-connection-repair, base fdf1ce8e1713ac467ebca1e44707225175e72dc4.
- ConferenceScaffold-prosjekt opprettet og lest tilbake i innlogget staging-portefølje. Prosjektets Åpne-knapp feiler; parserrettelse + test skrevet. Fire WorkItems (HD-0143–HD-0146 i tittel/kilde) er opprettet og lest tilbake etter reload. Interne WorkItem-ID-er og strukturert prosjektkobling er ikke verifisert.
- Tilbake-feil til Developer Workbench er sporet til tilfeldig konfigurasjons-UUID. Fast ID og positiv/negativ katalogtest er skrevet, ikke kjørt.
- Swift kjøring stoppet før kompilering: capacity exit 75. Lokal commit b99514c297217402af0df82f651c3badc35db24e er lagret. Ingen push, CI, installasjon eller deploy.
- Selvstendig ConferenceScaffold-program ikke implementert. Ikke merk HD-0145 ferdig.
- Serverens root under 40 GiB og aktiv claim HD-0141 må avklares før cutover.

## Planbytter
2026-09-29: Ny feil i ProjectPortfolio select er del av HD-0144. Ingen redesign.

## Bevis
ConferenceScaffold/implementation/repair-20260929/repair-evidence.json og cellscaffold-repairs.patch. ConferenceScaffold ligger i separat brukerworkspace under DiMy/HAVEN, ikke den kanoniske Digipomps/HAVEN-roten.
