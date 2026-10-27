# STATUS — undertekst infosider

- surfaces: web
- tags: brand, tekst, web

## Porter
- G1: venter        (formålsspesifikasjon godkjent av Kjetil)
- G1-GUI: venter        (rendret bilde godkjent — bare for GUI-oppgaver)
- G2: venter        (plan godkjent; arbeidspakker 1:1 mot bladformål)
- G3: venter        (akseptanse: forventning mot faktisk, alle avledede tester grønne)

Sett en port til `godkjent <dato>` kun når Kjetil har sagt det. `purpose_dev.py validate <mappe>` nekter porter uten artefakter.

## Planbytter (dato — hvorfor)
-

## Logg
- 2026-10-22: opprettet
- 2026-10-22: FORMAALSSPEC §0–§6 fylt. Før/etter-bilder i images/ (Chromium-render, se images/README.md). Tre HTML-filer endret på gren `claude/undertekst-infosider-20261022`; vakt OK, 8 tester grønne. Venter på G1/G1-GUI fra Kjetil. Utrulling er Kjetils steg (RELEASE_NOTE_2026-10-22.md).
- 2026-10-22 (runde 2): mobilbildene tatt om igjen som helside-klipp (toppmenyen dekket seksjonen). TESTRESULT.md skrevet med faktisk utdata (vakt OK før/etter, 8/8 tester, 3 filer med treff). test.gui.parity er blocked til Kjetil har rullet ut. PR åpnet som utkast.
