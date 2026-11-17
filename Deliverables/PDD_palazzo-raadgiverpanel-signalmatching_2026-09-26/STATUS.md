# STATUS — palazzo raadgiverpanel signalmatching

- surfaces: cell, codex, python, scaffold, terminal
- tags: evaluering, formaalsmatching, holdout, korpus, matching, palazzo, signalmatching

## Porter
- G1: godkjent 2026-09-29 (Kjetil, ordrett: «palazzo-raadgiverpanel-signalmatching G1 godkjent.»; samme melding: panelet og andre ventende porter skal opp i developer workbench, «funksjonalitet som ikke kommer ut til brukerene ikke eksisterer»)
- G1-GUI: ikke relevant        (rendret bilde godkjent — bare for GUI-oppgaver)
- G2: venter        (plan godkjent; arbeidspakker 1:1 mot bladformål)
- G3: venter        (akseptanse: forventning mot faktisk, alle avledede tester grønne)

Sett en port til `godkjent <dato>` kun når Kjetil har sagt det. `purpose_dev.py validate <mappe>` nekter porter uten artefakter.

## Planbytter (dato — hvorfor)
-

## Logg
- 2026-09-26: opprettet
- 2026-09-26: iterasjon 1 av FORMAALSSPEC lagt fram for G1 (audit, formålstre med rådgiverroller, forventningskontrakt, sju Palazzo-tester, to åpne spørsmål). Ingen plan og ingen kode før G1.
- 2026-09-28: Kjetil svarte på §6 (begge virkefelt: husets signaler/tagger og leksikon/vekter i kode; sølvfasit i første runde). G1 er fortsatt ikke sagt godkjent — spesifikasjonen står i iterasjon 2.
- 2026-09-28: Kjetils prioritet denne uken er demoen for Andre onsdag 30.9 (gjest, kelner, hus matching). Den kjøres som egen leveranse i PalazzoScaffold (`docs/demo/README.md`), ikke som del av panelet.
- 2026-09-26: `purpose_dev.py validate` rapporterer fem FEIL som lå der før denne oppgaven (lærdommer som peker på `purpose://candidate.testflyt-verktoycelle.haven-lenke-begge-veier`, et formål som ikke finnes i registeret). Ikke rørt her; hører i den oppgaven som eier lærdommene.
- 2026-09-29: **G1 godkjent** (Kjetil). Spesifikasjonen sto i iterasjon 2 etter §6-svaret 28.09. Neste: PLAN.md med arbeidspakker 1:1 mot bladformålene i §1, deretter G2. Kjetil la samtidig til et krav som gjelder alle PDD-er: ventende porter skal vises i developer workbench, ikke ligge i en logg.
