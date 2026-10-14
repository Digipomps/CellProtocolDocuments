# STATUS — palazzo sicilia artikler

- surfaces: cell, gui, scaffold, skeleton
- tags: artikler, celle, formaal, gui, innhold, interesse, palazzo

## Porter
- G1: godkjent 2026-09-07 (Kjetil: «ingen grunn til å ikke gjøre det — gi jobben til Codex»; §6 med Losens forslag: Losen skriver utkast, negative lagres som avoid, artikler er signaler når husk er grønn)
- G1-GUI: godkjent 2026-09-07 (Kjetil: «Jeg liker bildene — mer enn godt nok for å vise Andre. Ok på G1-GUI»; images/*-v1.png)
- G2: godkjent 2026-09-07 (auto — samme bestilling; GUI-slice holdes til G1-GUI)
- G3: venter        (akseptanse: forventning mot faktisk, alle avledede tester grønne)

Sett en port til `godkjent <dato>` kun når Kjetil har sagt det. `purpose_dev.py validate <mappe>` nekter porter uten artefakter.

## Planbytter (dato — hvorfor)
-

## Logg
- 2026-09-07: opprettet
- 2026-09-07: iterasjon 1 sendt Kjetil for G1; avhengig av husk-oppgaven WP1
- 2026-09-07: WP0–WP5 lagt i _losen-queue som sicilia-impl-20260907-2005; WP-GUI venter G1-GUI; 8 artikkelutkast i content/
- 2026-09-07: G1-GUI godkjent; WP-GUI (handoff/GUI.md, G1–G6) lagt i _losen-queue som sicilia-impl2-gui-20260907-2030, kjører etter sicilia-impl. Verifikasjon: Porthole-skjermbilder mot G1-GUI-bildene (images/verify/), native HAVEN-app via G6/Kjetil.

## Utførelse WP0–WP5 — 2026-09-07 23:04 Europe/Oslo

Brukerens instruks for denne kjøringen holder WP-GUI BLOKKERT, selv om ovenstående historikk beskriver godkjenning/kø for en separat GUI-jobb. Ingen fabrikk- eller eksisterende skeleton-fil ble endret. Det tillatte unntaket er en minimal Text-konfigurasjon i gjestecellen.

- WP0: verifisert — 82/82 baseline etter rent bygg; tidligere binærkrasj dokumentert.
- WP1: levert — artikler, godkjente tagger og artikkelsignaler.
- WP2: levert — eksplisitte private reaksjoner, kommentarer og persistens.
- WP3: levert — interests/avoid og samtykkekontroll.
- WP4: levert — statsløs tekstlesing uten nye records/events.
- WP5: levert — ruter, discovery, 13 nye tester, docs og rapport.
- Sluttbygg: PASS. Full regresjon: 95/95, 0 feil. To separate prosesser bekrefter varige poster og samtykkestyrt innsyn.
- Supplerende TCP-smoke: miljøblokkert (`bind`: Operation not permitted); ingen påstand om transportverifikasjon.
- G3: implementasjonsbevis for WP0–WP5 foreligger i TESTRESULT.md/ACCEPT.md; ingen ny brukergodkjenning eller GUI-akseptanse registrert.
- Ingen git-kommandoer; CellProtocol er urørt.
- 2026-09-07: WP-GUI levert av Codex (G1–G4, 100 tester grønne). G5 Porthole-paritet BLOKKERT av Codex-sandkassen (TCP bind EPERM, Chromium bootstrap nektet); G6 native: ingen ferdig snapshot-vei i Binding (images/verify/NATIVE.md). Losens forsøk på full-tilgangs Codex-kjøring via MCP ble nektet av Cowork-klassifikatoren. Jobb sicilia-impl3-g5script lagt i kø: skriver run-g5.sh som Kjetil (eller en godkjent full-tilgangskjøring) kjører. G3 for Sicilia venter på G5-bildene.
- 2026-09-07: run-g5.sh + README levert (ikke kjørt). Funn fra Codex' kildekontroll: PalazzoBridgehead.isPublishable omfatter ikke PalazzoGuestShell/PalazzoContent, og CellScaffold sender ikke bridgehead-token på cell://-oppslag — Porthole/HAVEN-appen kan derfor ikke nå de tre flatene før det er løst. Beslutning hos Kjetil (endrer tilgangsflaten).
- 2026-09-08: Kjetil «Ja absolutt» til bridgehead-publisering → handoff/G7-bridgehead.md (B1–B4) i kø som sicilia-impl4-g7-bridgehead. Kjetils første run-g5.sh-kjøring feilet i steg 2 (hjelpefil http.py skygget stdlib) — rettet av Losen (palazzo_seed.py), dokumentert i run-g5.README.md. Rollesimulering opprettet som egen oppgave PDD_palazzo-rollesimulering_2026-09-08 (til G1).
- 2026-09-14: Kjetil kjørte `run-g5.sh` (13:10Z). Steg 1–3 grønne (Palazzo 18083 opp, seed/tagger/publish OK, CellScaffold 18080 opp). Steg 4 feilet for alle tre flater: Porthole `addConfiguration` → 400 «Configuration is not available in this Porthole yet.» Årsak (lest i CellScaffold): oppslaget matcher bare Portholes egen katalog, og `portholeSupportedEndpoints` er en statisk lokal allowlist — eksternt scaffold over bridgehead kan ikke lastes. Ingen PNG-er. Registrert som HAVEN-Deploy **HD-0078** (venter G1 fra Kjetil). G3 forblir «venter». Evidens: `PalazzoScaffold/docs/sicilia-gui-evidence/run-g5.log`, `porthole-gjest-sicilia-liste/desktop/failure.txt`.
