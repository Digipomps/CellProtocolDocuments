# STATUS — correspondence vedlegg

- surfaces: bridge, cell, scaffold
- tags: celle, correspondence, kryptering, personvern, vedlegg

## Porter
- G1: venter        (formålsspesifikasjon godkjent av Kjetil)
- G1-GUI: ikke relevant        (rendret bilde godkjent — bare for GUI-oppgaver)
- G2: venter        (plan godkjent; arbeidspakker 1:1 mot bladformål)
- G3: venter        (akseptanse: forventning mot faktisk, alle avledede tester grønne)

Sett en port til `godkjent <dato>` kun når Kjetil har sagt det. `purpose_dev.py validate <mappe>` nekter porter uten artefakter.

## Planbytter (dato — hvorfor)
-

## Logg
- 2026-09-04: opprettet
- 2026-09-04: §0–§7 fylt ut. Iterasjon 1 av formålstreet. Venter på G1 og på svar på tre spørsmål i §6.
- 2026-09-04: iterasjon 2 — Kjetil besvarte alle tre §6-spørsmålene. Vedlegg bundet til én melding; chunk-transport låst i kontrakt og bygges etter S5; `attachmentStreamV1` bygges i denne oppgaven. Venter fortsatt på G1.
- 2026-09-04: blokkerende avhengighet notert — S5 (MCP som celleklient) er ikke gjort; dagens MCP sender plaintext med maxLength 16384. Vedlegg kan ikke testes før den er grønn.
- 2026-09-04: S5-handoffen er skrevet (`Codex_Handoff_Corr_S5_MCP_Celleklient_2026-09-04.md`, status READY, seks slices). Den er den blokkerende avhengigheten for denne oppgaven; vedlegg festes ikke før den er grønn.
