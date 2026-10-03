# STATUS — testmatrise og apns chat

- surfaces: bridge, cell, codex, scaffold, terminal, xcode
- tags: apns, chat, invitasjon, push, samarbeid, scaffold, test

## Porter
- G1: venter        (formålsspesifikasjon godkjent av Kjetil)
- G1-GUI: ikke relevant        (rendret bilde godkjent — bare for GUI-oppgaver)
- G2: venter        (plan godkjent; arbeidspakker 1:1 mot bladformål)
- G3: venter        (akseptanse: forventning mot faktisk, alle avledede tester grønne)

Sett en port til `godkjent <dato>` kun når Kjetil har sagt det. `purpose_dev.py validate <mappe>` nekter porter uten artefakter.

## Planbytter (dato — hvorfor)
-

## Logg
- 2026-09-29: opprettet

- 29.09 (T6, tørrkjøring, ingenting skrevet i noe repo): `handoff/snapshot-alle.sh` målt mot refreshet indeks-kopi. CellProtocol main@81601a6: 0 å ta vare på. CellScaffold codex/entitetsutvidelse-20260929: 582 går med (200 endret, 59 slettet, 420 uspora), 1 holdt ute (hemmelighet-regex). Binding codex/havenagentd-…: 855 går med, 41 198 holdt ute som bygg-rot (`.havenbuild`, test-logs), 2 for store. CellProtocolDocuments codex/entitetsutvidelse-20260928: 5 303 går med, 27 for store, 1 hemmelighet-treff. Detaljer: `handoff/_dry/run4/`. `--go` ikke kjørt — venter på Kjetils ja.
