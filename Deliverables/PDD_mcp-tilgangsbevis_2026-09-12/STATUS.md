# STATUS — mcp tilgangsbevis

- surfaces: bridge, cell, codex, scaffold, terminal, web
- tags: avdrift, bevis, entitet, grants, identitet, mcp, sikkerhet, testing, tilgang

## Porter
- G1: godkjent 2026-09-12        (formålsspesifikasjon godkjent av Kjetil — med vilkår: «gjør det med riktig formålsarkitektur» = PerspectiveNode; se PERSPECTIVENODE_KONSEKVENS.md)
- G1-GUI: venter        (rendret bilde godkjent — bare for GUI-oppgaver; L5–L9 i FORMAALSSPEC §3)
- G2: venter        (plan godkjent; arbeidspakker 1:1 mot bladformål)
- G3: venter        (akseptanse: forventning mot faktisk, alle avledede tester grønne)

Sett en port til `godkjent <dato>` kun når Kjetil har sagt det. `purpose_dev.py validate <mappe>` nekter porter uten artefakter.

## Beslutninger (Kjetil)
- 2026-09-12: Baselinen skal **ikke** ligge i samme celle som grantene (R1 → vedtatt).
- 2026-09-12: Grantene må ligge i en celle for å bruke CellProtocol riktig (A5 bekreftet).
- 2026-09-12: Keypath er datareferanse uten egen autoritet; tilgang avgjøres av hver celle ved traversering (tillat / avvis / Agreement challenge). Brukeren må ha verktøy for å løse en challenge: varsel i varslingssenteret, oppfyll vilkår direkte eller åpne verktøy.
- 2026-09-12: Formålsstrukturene skal være PerspectiveNode. Konsekvensanalyse bestilt og levert (iterasjon 1); Codex-gjennomgang i kø.
- 2026-09-13: `goalDefinition` skal inn i `Purpose`-dekodingen (kjernen). Astras innvendinger tas med. Rådgiverpanel ved uavklarte spørsmål. Kriterier: effektiv, fleksibel, robust.

## Planbytter (dato — hvorfor)
-

## Logg
- 2026-09-12: opprettet
- 2026-09-12: FORMAALSSPEC iterasjon 1 skrevet (§0-§7). G1 venter på Kjetils ord.
- 2026-09-12: FORMAALSSPEC iterasjon 2 - treet klassifisert mot Book 23 (57 noder); rot under purpose://access.audit.privacy, grener under purpose://self-determination.data.*
- 2026-09-12: Blokkerende avhengighet D7 (ny agent-binaer drepes av Launch Constraint Violation) ligger hos Codex. Ingen implementering kan testes foer den er loest.
- 2026-09-12: FORMAALSSPEC iterasjon 3 — §1.7 formålssammensetning (Book 36), D11, Q6. validate exit 0.
- 2026-09-12: **G1 godkjent** av Kjetil med vilkår og fire korreksjoner. FORMAALSSPEC iterasjon 4 tar dem inn (A5, A11, D5, gren 3 omdøpt, nytt blad `challenge-is-resolvable-from-notification`, R1 vedtatt).
- 2026-09-12: PERSPECTIVENODE_KONSEKVENS.md iterasjon 1 levert: inventar R1–R5, kart PDD→CellBase, K1–K10, M1–M11, fase 0–4, Q1–Q6. Codex-gjennomgang lagt i `_losen-queue` (svar → handoff/CODEX_REVIEW_PERSPECTIVENODE.md).
- 2026-09-12: Astras (Codex) gjennomgang levert etter 14 min (`handoff/CODEX_REVIEW_PERSPECTIVENODE.md`, 193 linjer): kartet holder, kompatibilitetsbeviset holdt ikke. 15 rettelser tatt inn i PERSPECTIVENODE_KONSEKVENS.md iterasjon 2; FORMAALSSPEC iterasjon 5 (D5, blad challenge-is-resolvable). Tre overdrivelser fra iterasjon 1 navngitt.
- 2026-09-13: Kjetil: «goalDefinition er kjernen her så det må inn i dekodingen. Ta med Astras innvendinger - om du syns spørsmålene er uavklart bruk rådgiverpanel. Gå etter effektiv, fleksibel og robust løsning.» → rådgiverpanel kjørt: `panel/BRIEF.md` (P1–P5), Fabel (uavhengig Claude-tråd) svarte i `panel/FABEL_SVAR.md` (2 448 ord); Astra (Codex) i kø bak nattkjeden → `panel/ASTRA_SVAR.md`.
- 2026-09-13: `BESLUTNINGER.md` iterasjon 1: B1 goalDefinition inline i Purpose med streng dekoding; B2 Book 36-semantikk normativ, Swift porteres mot delte vektorer; B3 bevis = delegert bærernøkkel + signert Agreement-grant (aldri eierbevis, strukturelt); B4 porter = ditt ord i STATUS+transkript, «signert» forbudt til port-celle finnes; B5 motor-invarianter + én observasjon per baseline-kilde; B6 tre relasjoner atskilt; B7 A–C til graf-PDD, D–E her, F senere; B8 Book 36 ikke godkjent som den er; B9 to celler. Tre spørsmål til Kjetil: K1 (agentens ord = Kjetils ord?), K2 (deling), K3 (endre Swift-composition).
- 2026-09-13: `PLAN.md` utkast til G2 med `images/plan-oversikt-v1.png` (røde sekskanter = Kjetil). Forslag: del oppgaven så Del 1 (A1–A4) og D1 kan gå på Kjetils ord nå; Del 3–5 får G2 etter G1-GUI. `handoff/A1-goaldefinition.prompt.md` klar, ikke lagt i kø.
- 2026-09-14 00:05: Astras panelsvar levert (`panel/ASTRA_SVAR.md`, 8 min i kø-kjøring). `BESLUTNINGER.md` iterasjon 2: enighet B1/B3/B4/B5, uenighet B2 (Astra: parallell type (c); valg (a) står, begrunnet). Nytt fra Astra: `Contract.signed` er gjenbrukstypen for beviset; utsteder må være cellens eier (`GeneralCell.swift:2048`) → K1 skjerpet til «hvem eier scaffold-cellene»; sikkerhetsloggen registrerer bare avslag → kvittering for tillatt bruk må bygges; Book 36 selvmotsigende om `anyOf`/`blocked` → K4.
- 2026-09-14: Neste: Kjetils ord på G2 (eller «kjør A1»), K1–K4; G1 mockups L5–L9.
- 2026-09-17: Kjetil presiserte at grensene ikke er hans, men Claudes manglende evne, og at utfoerelsen skal gaa gjennom HAVENAgentD paa laptopen med katalogovervaaking, formaalskatalog som grensesnitt, formaal i stedet for kommandolister, og modus lese/skrive/utfoere med ulikt godkjenningsnivaa. Lagt inn ordrett som (d) og (e) i FORMAALSSPEC §0.1, med avledede krav K-A1..K-A8 i §0.1.1 og spoersmaal Q9 i §6. Fem av kravene er gap mot dagens kode, ikke konfigurasjon. D7 er fortsatt roed og blokkerer all testing av ny agentkode.
