# STATUS — lagringsceller og tjenesteregister

- surfaces: cell, gui, porthole, scaffold, skeleton
- tags: access, configuration, entitlement, micropayment, payment, registry, storage

## Porter
- G1: godkjent 2026-10-06 (Kjetil: «G1 og G1-GUI er godkjent.»)        (formålsspesifikasjon godkjent av Kjetil)
- G1-GUI: godkjent 2026-10-06 (Kjetil: «G1 og G1-GUI er godkjent.»)        (rendret bilde godkjent — bare for GUI-oppgaver)
- G2: godkjent 2026-10-08 (Kjetil, svar i AskUserQuestion: «Ja, G2 godkjent»; svar 5–7 fra samme dag inngår, mikroøre-representasjonen er Losens forslag og flagges i PR A)        (plan godkjent; arbeidspakker 1:1 mot bladformål)
- G3: venter        (akseptanse: forventning mot faktisk, alle avledede tester grønne)

Sett en port til `godkjent <dato>` kun når Kjetil har sagt det. `purpose_dev.py validate <mappe>` nekter porter uten artefakter.

## Planbytter (dato — hvorfor)
-

## Logg
- 2026-10-05: opprettet

- 2026-10-05: P0/P1 skrevet (iterasjon 1). Fire spørsmål stilt. Ingen bilder, ingen plan, ingen kode. Ingen porter godkjent.
- 2026-10-05: Kjetil svarte på fire spørsmål (se §6). Skisser v1 laget og sendt. G1 og G1-GUI venter på Kjetils ord.
- 2026-10-05: `purpose_dev.py validate` gir 5 feil, alle i erfaringsregisteret (lærdommer som peker på purpose://candidate.testflyt-verktoycelle.haven-lenke-begge-veier, som ikke finnes). Ingen gjelder denne mappen.
- 2026-10-06: G1 og G1-GUI godkjent av Kjetil. Starter P2 (plan).
- 2026-10-08: Kjetil svarte på spørsmål 3–5 (8 MB; enheter under 1 øre med kostpris + påslag; test lokalt eller på verten, rydd etterpå). Ført inn i FORMAALSSPEC §2/§5/§6/§7 og PLAN.md (avgjørelse 5, AP5b) av en annen Losen-tråd. Den tråden skrev «G2 venter» fordi G2-svaret ikke var ført inn ennå.
- 2026-10-08: G2 godkjent (svaret kom i Losen-tråden som laget planen; datoen i porten over er rettet til 2026-10-08). Avgjørelser: (1) ny uploadMode "presigned" i leveranse 1, testes i web og Binding før main; (2) felles flater lagrer i scaffold-eierens lager, personlige i brukerens; (3) registeret gratis for alle i leveranse 1, AP8 venter på entitetsklasse; (4) trafikk ut som anslag.
- 2026-10-08: P3 startet. Kode skrives i ren klone av main i Losens sky-arbeidsflate og leveres som PR; Linux-CI bygger og tester. Arbeidstreet på Mac-en (Astras gren) røres ikke.
- 2026-10-08: G2 godkjent av Kjetil («G2 ok»). Starter P3: PR A (AP1a, AP1–AP5b).
- 2026-10-08: Rundtur mot S3-kompatibel testtjeneste kjørt mot PR #290-koden: alle bestod etter én kompileringsrettelse (Linux typesjekk i canonicalQuery), se TESTRESULT-s3-testtjeneste-2026-10-08.md og kommentar på PR #290.
- 2026-10-08: PR A levert som CellScaffold #290 (S3-transport, signerte adresser, tjenestevalg, måling, mikroøre; + CI viser bygg- og testfeil som annotasjoner). CI grønn på 21dd5a5, alle 30 testbolker. Klar til gjennomgang (AP13), ikke merget.
- 2026-10-08: PR B levert som CellScaffold #291 (tjenesteregister, ni tjenester, rangering). Bygger på #290. CI grønn på a26932a. Klar til gjennomgang, ikke merget.
- 2026-10-08: Uavhengig Fabel-gjennomgang før CI fant 1 kompileringsfeil, 4 feil tester og et sikkerhetshull (forslag kunne overskrive prisene i startinnholdet). Alt rettet. CI fant i tillegg ett uttrykk Linux ikke rakk å typesjekke, en feil i testens etterligning og forventet gullkorn-endring. Se TESTRESULT.md.
- 2026-10-08: Ikke gjort: test mot ekte S3-tjeneste (vedtak: lokalt eller på verten), AP8, PR C (flater + uploadMode), PR D/E (flytting fra disk), AP12. Grunnlinje (AP0) ikke kjørt som egen PR; avvik står i TESTRESULT.
