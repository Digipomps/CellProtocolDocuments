# Brief til Fabel: kontroll av rettelsene etter etterkontrollen

Dato: 02.10.2026, sen kveld. I `panel/FABEL_ETTERKONTROLL_G2.md` fant du tretten nye feil. Alle er forsøkt rettet. Dette er en kort kontroll av de rettelsene, ikke en ny gransking av alt.

## Hva som er endret

Sporingen står i `PLAN_VEDLEGG.md`, avsnittet «Fabels etterkontroll av G2-artefaktene». Utgavene fra før rettelsene ligger ved siden av filene med endelsen `.foer-etterkontroll`, så du kan sammenligne.

| Feil | Rettet i |
|---|---|
| 1 «Stopp jobben» på faste hendelser | `contract/trinn4-jobber-og-godkjenning.md` (tabellen over saker og kulepunktene under), `contract/trinn5-kontrollbro.md` (AP13), `contract/saker-job.example.json`, `dataflow.md` K32, `images/meny-v4.html` (tilstanden `feil`), `images/README.md`, nytt bilde `images/meny-planlagte-jobber-feil-v3.png`. Valget: saker om faste hendelser har «Kvitter» og «Åpne» i trinn 4, og får «Sett på pause» i trinn 5, når «Fortsett» finnes i lista. |
| 2 §5 | `FORMAALSSPEC.md` §5 er oppdatert og er den ene lista; `contract/trinn3-cron.md`, `trinn4` og `trinn1-2-programmer.md` viser dit. |
| 3 §6 og presiseringene | `FORMAALSSPEC.md` §1c (ny kolonne) og §6 (tre åpne spørsmål); `PLAN.md`, nytt avsnitt «Tre presiseringer du svarer på hver for seg». |
| 4 `resume` | `contract/trinn4` (styringen, og regel 6 for kjøring), `contract/trinn3-cron.md` (Pause), `contract/trinn5-kontrollbro.md`, `dataflow.md` K33. |
| 5 titler over 80 tegn | `contract/trinn4` (kulepunkt under sakene), `contract/trinn3-cron.md` (feltet `title`), `handoff/README.md` S2 steg 4, `contract/config-tillegg-trinn1-2.json` (`fra-trinn-3`). |
| 6 tidsbudsjettet | `contract/trinn1-2-programmer.md` (under `sjekk`, og i selvtesten). |
| 7 `PLAN.md` mot kontrakten | `PLAN.md`, tabellen under «Det du godkjenner i G2», og presisering 3. |
| 8 `spool-not-enabled` | `contract/mcp-verktoy.json`. |
| 9 `git push` i S0 | `handoff/README.md` S0. |
| 10 `--root` | `contract/trinn1-2-programmer.md` (Kjente grenser), `handoff/README.md` S2 steg 2. |
| 11 «15 eller 16» | `contract/trinn3-cron.md`. |
| 12 `env` i formkontrollen | `contract/trinn4` (bestillingen punkt 4, og detaljen), `contract/mcp-verktoy.json` (`invalid-job`). |
| 13 småting | `PLAN.md` (antall granskinger), `contract/trinn4` («En assistent»), `contract/fixtures/cron-forventninger.json` (fire nye tellinger: `30 */2` og `30 0-23/2` på 25.10.2026 og 28.03.2027), `contract/trinn3-cron.md` (tabellen over følger). |

`contract/kontroller_kontrakt.py` har fått kontroller for dette, og `contract/KONTROLL.txt` er kjørt på nytt (139 av 139).

## Det jeg ber om

1. For hver av de tretten: løst, delvis løst eller ikke løst, med fil og linje.
2. Nye feil rettelsene har laget, særlig: steder der to dokumenter nå sier ulike ting om saker for faste hendelser, om `resume`, eller om testene; og om regelen for `resume` lar seg bygge uten at to prosesser skriver samme fil.
3. Les avsnittet «Tre presiseringer du svarer på hver for seg» i `PLAN.md` og §6 i `FORMAALSSPEC.md` slik Kjetil leser dem. Er det klart at det er tre egne svar, og er «Sier du nei»-kolonnen sann mot kilden?

## Slik svarer du

Skriv til `panel/FABEL_ETTERKONTROLL2_G2.md`, på norsk, kort. Tabell med utfall per feil, så «Nye feil» (nummerert, med fil, linje og hva som bør stå), så én linje om presiseringene. Samme grenser som sist: bare lesing utenom rapportfila, ingen verktøy som når Macen eller andre tjenester, ingen private detaljer fra `panel/kilder-utdrag/` i rapporten. Svaret ditt til meg skal være kortversjonen: antall løst, og de nye feilene i én linje hver.
