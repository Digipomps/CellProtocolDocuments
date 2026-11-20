# STATUS — modell i felles chat

- surfaces: binding, cell, gui, python, scaffold, skeleton, web
- tags: agreement, ai-gateway, chat, collaboration, model-participant

## Porter
- G1: godkjent 2026-11-20 (Kjetil: «2. a 3 a a nå G1 G1-GUI Godkjent», 23.43 Oslo)        (formålsspesifikasjon godkjent av Kjetil)
- G1-GUI: godkjent 2026-11-20 (samme melding; referansebildene er images/modellchat-*-v1.png)        (rendret bilde godkjent — bare for GUI-oppgaver)
- G2: godkjent 2026-11-20 (Kjetil: «G2 Godkjent», 23.55 Oslo; Opus 5.5-ruten ikke med, ikke besvart)        (plan godkjent; arbeidspakker 1:1 mot bladformål)
- G3: venter        (akseptanse: forventning mot faktisk, alle avledede tester grønne)

Sett en port til `godkjent <dato>` kun når Kjetil har sagt det. `purpose_dev.py validate <mappe>` nekter porter uten artefakter.

## Planbytter (dato — hvorfor)
-

## Logg
- 2026-11-15: opprettet
- 2026-11-15: iterasjon 1 av FORMAALSSPEC og 6 bilder rendret fra skeleton-JSON. G1 og G1-GUI bedt om. Venter også på svar på §6 (hvor samtalen bor, hvem må si ja, ekstern modell, Python/Go).
- 2026-11-15 11.31 Oslo: Kjetil valgte §6 spm. 1 (a): Samtaler flyttes til ChatCell. G1 og G1-GUI er fortsatt ikke godkjent.
- 2026-11-20: G1 og G1-GUI godkjent, §6 spm. 2–4 besluttet (a). PLAN.md (WP0–WP17) skrevet, G2 bedt om.
- 2026-11-20 23.55: G2 godkjent. Implementering starter: WP0 på Mac, WP1–WP4 i CellProtocol.
- 2026-11-21 natt: WP1–WP4 i CellProtocol PR #101 (utkast). Modellen slippes inn gjennom chattens eksisterende `member`/`invitationAccepted`-betingelse, som for modellens identitet gjelder bare mens alle medlemmer har sagt ja (Agreement-betingelser er OG-et, så en egen betingelse ville også stengt mennesker). Scenariofixtures i `fixtures/interop/chat-model-v1`. 73 tester grønne på Linux (Docker swift:6.1-noble). Testene ble skrevet sammen med koden, ikke kjørt røde først.
- 2026-11-21 natt: WP5 PyCellProtocol PR #4 (303 grønne), WP6 GoCellProtocol PR #38 (`go test -race` grønn). Begge sjekker samme fixture og har en falsk modell.
- 2026-11-21 natt: WP9–WP12 kjernen i CellScaffold startet som `ScaffoldKit/Samtaler/SamtaleModelHost.swift` (bygges og testes i skyen mot CellProtocol-grenen). WP7–WP8 (Samtaler-lageret på ChatCell) krever App-bygg på Mac.
