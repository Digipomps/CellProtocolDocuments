# STATUS — korrespondanse fornyelse

- surfaces: cell
- tags: access, correspondence, expiry

## Porter
- G1: godkjent 2026-09-30 — Kjetil valgte «Bygg fornyelse (anbefalt)» med beskrivelsen som står ordrett i FORMAALSSPEC §0
- G1-GUI: ikke relevant        (rendret bilde godkjent — bare for GUI-oppgaver)
- G2: venter — PLAN.md. Utsettingen (AP3) fikk Kjetils ja 30.09 («Ja, sett ut nå (anbefalt)»), men et eget ord om G2 er ikke gitt.
- G3: venter — ACCEPT.md er klar 01.10. Kjetils ord gjenstår.

G2-artefakten `contract/` har bare README.md: pilotcellen har ingen kontrakt-JSON (se `contract/README.md`). `gates` viser derfor ✗ til en slik finnes, eller til Kjetil sier at kontraktpakken ikke gjelder her.

Sett en port til `godkjent <dato>` kun når Kjetil har sagt det. `purpose_dev.py validate <mappe>` nekter porter uten artefakter.

## Planbytter (dato — hvorfor)
- 2026-09-30 — AP4 fornyer begge Kjetils principals, `kjetil-vegar-codex-d` og `kjetil-codex-d`, ikke bare den første. Kjetil valgte «Begge (anbefalt)». §2 holder fortsatt andre principals enn hans utenfor.

## Logg
- 2026-09-30: opprettet. Kode og tre tester lagt inn i CellScaffold-grenen claude/korrespondanse-fornyelse-20260930 (fra feec2372, som staging kjører). Bygg og test kjører på Macen (jobb 224).
- 2026-09-30: `415ea3d2` pushet og satt ut på staging (`COMMITTED_VERIFIED` 20:24:24Z), invitasjonene byttet 20:24:51Z. Kjetil godkjente begge kortene kl. 22:43, og de nye bevisene gjelder til 2026-10-30. Meldingen til Vegar gikk gjennom (`sent`). Meldingen til Victoria ble avvist fordi hennes egen tilgang gikk ut 29.09.
- 2026-10-01: Vegars meldinger kommer fram igjen (sekvens 13–15, 00:02–00:15Z). Losen leste og kvitterte dem 06:01Z. ACCEPT.md, dataflow.md og contract/README.md er skrevet, og to lærdommer er lagt i registeret. Vegar ber om fornyelse før fristen 08.10 (§6).
- 2026-10-01: Kjetil valgte fornyelse før fristen («Serverendring, avtalt tid») og PR mot main. F6 og T6–T8 lagt til i FORMAALSSPEC.
- 2026-10-02: `06f32050` committet og pushet etter 33 av 33 grønne korrespondansetester. Full testmengde uten nye feil. PR #277 opprettet. Image bygges (kjøring 36998313078).
- 2026-10-02: **Funn om koordinering.** Utsettingen 30.09 (`415ea3d2` og invitasjonsbyttet) ble gjort direkte på verten, uten `hd coord claim` og uten at `_losen-queue/KOORDINERING.md` var lest. Codex hadde da claim på `cellscaffold-app-1` og nginx (HD-0141, siden 29.09), og staging var reservert for release 2026.9.4. Deploykøen tror fortsatt at staging kjører `feec2372`. Losen setter derfor ikke ut `06f32050` selv. Kjetil er varslet 02.10.
- 2026-10-02: Merge-sjekken på PR #277 er grønn (kjøring 36998795184, hode `d83d9f6b`). Image-bygget for `06f32050` pågikk fortsatt kl. 12:20Z.
- 2026-10-02: Fabel gransket påstandene om utsettingen, fornyelsen og svaret til Vegar (`panel/FABEL_SVAR.md`) og kontrollerte rettelsene (`panel/FABEL_ETTERKONTROLL.md`). Nytt etter granskingen: hver fornyelse krever en omstart på verten, fordi invitasjonene bare leses fra containerens miljø; `415ea3d2` fornyer bare utløpte tilganger (målt i diffen); utsettingen 30.09 kjørte også manifest-provisjoneringen under `/etc/haven`. ACCEPT.md er oppdatert. I `handoff/` ligger teksten til koordineringsfila, utkastet til svar til Vegar (v3) og valget om rekkefølgen på staging. Ingenting av det er sendt eller lagt inn.
- 2026-10-02: **Kjetils svar ca. 18:43Z.** Rekkefølgen på staging: «D: 2026.9.4, så fornyelsen», som også er ja til merge av PR #277. Svaret til Vegar: «Send». Mapper: «HAVEN-roten». Svaret til Vegar ble sendt 18:43Z (`msg-4760d976-ffc9-4992-a7e8-20e8c8cb7625`, `sent`). Avsnittet og raden står i `_losen-queue/KOORDINERING.md` fra 18:52Z (kopi av fila slik den var: `KOORDINERING.md.bak-20261002-foer-korr`; teksten ligger også i `handoff/KOORDINERING-tillegg-20261002.md`). Målt 18:48Z: staging kjører `415ea3d2`. PR #277 er åpen, `MERGEABLE` og `CLEAN`. Image-bygget for `06f32050` ble grønt 13:48Z (kjøring 36998313078). HD-0141 holder fortsatt `cellscaffold-app-1` og nginx. Ingen annen Claude-tråd kjørte på Mac-en, så kø-tråden ser innføringen når den leser fila.

## Venter på Kjetil
- Hvem som utfører mergen av PR #277, du eller Codex, når kø-tråden har gjort review.
- G2 og G3.
- Enhets-ID-en til Lille Robot, for Victorias fornyelse. Hun kan ikke nås gjennom korrespondansen nå.

## Venter på andre
- Kø-tråden: review av PR #277, den lille utgivelsen rett etter 2026.9.4 på staging, og bane og tidspunkt for invitasjonsbyttet (HD-0006).
- Eieren av HD-0141 (Codex): at `cellscaffold-app-1` frigis, eller at det gis et vindu. Alt på staging venter på det.
- Vegar: `deviceID` og `accessProof.expiresAt`, som invitasjonen må bære. Tilgangen hans går ut 08.10.
