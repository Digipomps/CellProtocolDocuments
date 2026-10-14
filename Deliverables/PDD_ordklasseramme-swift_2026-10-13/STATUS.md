# STATUS — ordklasseramme swift

- surfaces: codex, python, scaffold
- tags: nlp, parity, purpose-matching, swift

## Porter
- G1: godkjent 2026-10-13        (Kjetil valgte «Godkjent, egen pakke» 20:56Z: egen Swift-pakke i CellProtocol/commons/purpose-frame-matcher på egen gren)
- G1-GUI: ikke relevant        (rendret bilde godkjent — bare for GUI-oppgaver)
- G2: godkjent 2026-10-13        (Kjetil valgte «Godkjent, auto» 21:00Z)
- G3: venter        (akseptanse: forventning mot faktisk, alle avledede tester grønne)

Sett en port til `godkjent <dato>` kun når Kjetil har sagt det. `purpose_dev.py validate <mappe>` nekter porter uten artefakter.

## Planbytter (dato — hvorfor)
-

## Logg
- 2026-10-13: opprettet
- 2026-10-13: FORMAALSSPEC.md iterasjon 1 lagt fram for G1 (Losen, tråden «AI agent goals and constraints»)
- 2026-10-13 20:56Z: G1 godkjent av Kjetil, valget ordrett: «Godkjent, egen pakke»
- 2026-10-13 21:00Z: PLAN.md skrevet og lagt fram for G2; fasiten lagt i HAVEN-Deploy/_handoff/ORDKLASSERAMME/
- 2026-10-13 21:00Z: G2 godkjent av Kjetil, valget ordrett: «Godkjent, auto». Codex-jobb pfm1-swiftpakke-20261013 lagt i _losen-queue/inbox-pfm
- 2026-10-13 22:50Z: pfm1 (Codex) levert: commit 2033ab7a på losen/purpose-frame-matcher-20261013, 8 tester grønne, ikke pushet
- 2026-10-14 01:06Z: pfm3 (skriptjobb, uavhengig) 8 tester grønne; pfm2 stoppet på køens skrivetak før testene
- 2026-10-14 01:10Z: TESTRESULT.md og ACCEPT.md lagt fram for G3 (avvik 1: ingen sha256-sjekk ved lasting)
