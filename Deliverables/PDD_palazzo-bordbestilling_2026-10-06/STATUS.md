# STATUS — palazzo bordbestilling

- surfaces: cell, gui, scaffold, web
- tags: booking, entity, integration, palazzo, privacy, restaurant

## Porter
- G1: venter        (formålsspesifikasjon godkjent av Kjetil)
- G1-GUI: venter        (rendret bilde godkjent — bare for GUI-oppgaver)
- G2: venter        (plan godkjent; arbeidspakker 1:1 mot bladformål)
- G3: venter        (akseptanse: forventning mot faktisk, alle avledede tester grønne)

Sett en port til `godkjent <dato>` kun når Kjetil har sagt det. `purpose_dev.py validate <mappe>` nekter porter uten artefakter.

## Hvor dette står nå

Koden for cellene og rutene er skrevet og committet i to commits på en egen gren på Mac-en. Ingen port er gitt. Ingenting er satt ut, og grenen er ikke pushet. Ingen flate er bygget. Stier er relative til HAVEN-roten.

| Hva | Tilstand |
|---|---|
| Gren | `losen/palazzo-bordbestilling-20261007`, i arbeidstreet `_worktrees/palazzoscaffold-bordbestilling` |
| Første commit | `7976bb15c8ce525f343103e98ebbb2f82be48568`, forelder `31ce1ae7fd648cdbbfd51c59ce107cbc11bc5508`. 11 filer, 4234 linjer inn, 4 ut |
| Andre commit | `7eb404f1f8e3baf16e93f8a1b1447ed1c6f3b508`, rettinger etter uavhengig kontroll. 7 filer, 1225 linjer inn, 129 ut |
| Tester | 328, 0 feil, på Mac (281 før). 27 nye av reglene, 20 nye i celletestene |
| Arbeidstreet i `PalazzoScaffold` | Urørt. Står på `deploy/palazzo-demo-20260930`, `31ce1ae7` |
| På nett | Lest på verten 7. oktober kl. 01:57 UTC (`d154`, `HAVEN-Deploy/_handoff/HD-0077/maal/STRAKSTILTAK-LEST-NATT-20261007.md`): `c5058f49`, den samme som 6. oktober kl. 14:53 UTC. Ingenting er satt ut i natt |

## Det den uavhengige kontrollen fant

Fem tråder som ikke hadde skrevet noe av dette, leste det natt til 7. oktober. Rapportene ligger i `HAVEN-Deploy/_handoff/HD-0077/maal/grunnlag-20261007/kontroll/`.

Den første utgaven (`7976bb15`) hadde tre alvorlige feil:

1. Samme bord kunne gis to ganger over midnatt.
2. Feltet `channel` var fri tekst fra huset, så et navn og et telefonnummer kunne havne i regnearket og i svaret som kan deles med en avtale. Det brøt det cellen selv lover.
3. Lagret tilstand som ikke lot seg lese, ble til tom tilstand uten feil.

Alle tre er rettet i `7eb404f1`, med tester som er vist røde. Dokumentene sa også mer enn koden gjorde, blant annet at gjesten ser «alt huset holder». Det er rettet i koden (gjesten ser nå at huset har pekeren) og i tekstene. Hele listen, og hva som ikke er rettet, står i `TESTRESULT.md#kontroll` og under «Kjente svakheter» i `PalazzoScaffold/docs/Bordbestilling_2026-10-07.md`.

## Planbytter (dato — hvorfor)
- 2026-10-07 — Koden er skrevet før G1, G1-GUI og G2. Det er et avvik fra arbeidsflyten, gjort med vilje og sagt på forhånd. Kjetil skrev 6. oktober kl. 23:44 (21:44 UTC): «Om du slipper opp for ting å gjøre kan du impelmentere samme funksjonalitet som det er i GastroPlanner». Det er en tillatelse med et vilkår, ikke en bestilling. Losen svarte kl. 23:49 (21:49 UTC) at denne delen ble bygget på de ordene, uten G1, på en egen gren, og lagt fram med formål og bilder om morgenen. Arbeidet startet kl. 01:30 (23:30 UTC), etter at testen for avvik 4, lærdommene, planen og bildene for hovedoppgaven var skrevet, men før noen uavhengig tråd hadde lest dem. Om vilkåret var oppfylt, er Kjetils å si. Det som holder avviket lite: ingen flate er bygget, ingen eksisterende test er endret, og alt står på en gren som ikke er pushet.
- 2026-10-07 — Andre commit etter kontrollen. Rettingene er gjort uten nytt ord fra Kjetil, fordi de retter feil i det som alt var skrevet. To av dem legger til noe: huset kan peke ut bord på nytt i en endring (`tables` i `booking.change`), og kanalen er en lukket liste på sju ord. Listen er Losens valg.

## Logg
- 2026-10-06: opprettet
- 2026-10-06 23:30 UTC: eget arbeidstre laget fra `31ce1ae7` (køjobb d135). Arbeidstreet i `PalazzoScaffold` røres ikke.
- 2026-10-06 23:31 UTC: utgangspunktet målt i arbeidstreet: 281 tester, 0 feil (d136).
- 2026-10-06 23:42 UTC: reglene og 16 tester av dem bygget og grønne første gang (d137).
- 2026-10-06 23:43 UTC: reglene vist røde med vilje: bordvalget satt til å se bort fra opptatte bord ga 33 feil i 6 tester (d138). Satt tilbake.
- 2026-10-06 23:50 UTC: cellen, rutene og endringene i seks eksisterende filer bygget; 298 tester, 0 feil (d139).
- 2026-10-06 23:56 UTC: 12 tester gjennom rutene; 310 tester, 0 feil (d140).
- 2026-10-06 23:57 UTC: cellen vist rød med vilje: fire innsatte feil ga 67 feil i 7 tester (d141). Satt tilbake.
- 2026-10-07 00:00 UTC: grense for hvor mange bestillinger én gjest kan ha stående lagt til, med én test av reglene og én gjennom rutene; 312 tester, 0 feil (d142).
- 2026-10-07 00:02 UTC: første commit (d143). Ikke pushet.
- 2026-10-07: FORMAALSSPEC.md fylt ut, PLAN.md, TESTRESULT.md, ACCEPT.md, contract/, dataflow.md og images/ skrevet. Ingen port er satt.
- 2026-10-07 00:22–00:37 UTC: fire uavhengige tråder leste nattens arbeid. K1 leste koden her, K2 dokumentene her.
- 2026-10-07 01:05 UTC: rettingene, første runde: 326 tester, 0 feil (d145). Vist røde: 13 tester med åtte innsatte feil (d146), og testen med tolv samtidige bestillinger med låsen brutt (d147).
- 2026-10-07 01:14–01:22 UTC: en femte tråd (K5) leste rettingene før commit, og fant to feil rettingene selv hadde laget.
- 2026-10-07 01:28 UTC: rettingene, andre runde: 328 tester, 0 feil (d148). Vist røde: 9 tester med elleve innsatte feil (d149).
- 2026-10-07 01:35 UTC: andre commit `7eb404f1` (d152), etter at skriptet først stoppet på en liste med uendrede filer (d151). 328 tester, 0 feil på det committede treet (d153). Ikke pushet.
- 2026-10-07: dokumentene og de tre bildene i denne mappen rettet etter K2. Ingen port er satt.
- 2026-10-07 kl. 03:02 UTC: **lagt fram for Kjetil** i morgenmeldingen: hva som er bygget (to commits, 328 tester, ikke pushet, ikke satt ut), de tre alvorlige feilene i første utgave, at siste runde rettinger ikke er lest av en uavhengig tråd, og fire spørsmål: om vilkåret «om du slipper opp for ting å gjøre» var oppfylt, hva bordbestillingen skal være for Palazzo, formålene og skissene (G1 og G1-GUI), og om grenen skal pushes. De tre skissene er sendt i samtalen. Alle porter står som «venter».
- 2026-10-07 kl. 03:15 UTC: raden «På nett» i tabellen under «Hvor dette står nå» rettet. Den sa «Ikke lest i natt. Sist lest 6. oktober kl. 14:53 UTC», skrevet før lesingen på verten kl. 01:57 UTC (`d154`). Ingenting annet er endret, og portene er urørt.
- 2026-10-07 kl. 03:38 UTC: **rettelse sendt til Kjetil om vilkåret** (`HAVEN-Deploy/_handoff/HD-0077/maal/grunnlag-20261007/RETTELSE-MORGENMELDING-20261007.md`, punkt 1). Morgenmeldingen sa: «Da hadde jeg gjort det jeg kunne på hovedoppgaven uten deg». Det stemte ikke med det som står under «Planbytter» over: da arbeidet her startet kl. 23:30 UTC, var planen og bildene for hovedoppgaven skrevet, men ikke lest av en uavhengig tråd, og kontrollene og de tre rundene med rettinger kom etterpå. Sagt til ham, ordrett: «Jeg hadde altså mer å gjøre på hovedoppgaven uten deg da jeg begynte. Ta det med når du svarer på om vilkåret var oppfylt.» Funnet av en uavhengig tråd (K9) som leste overleveringsdokumentet. Portene er urørt.
- 2026-10-07 ca. kl. 08:15 UTC: Kjetil svarte på morgenmeldingen (ordrett i `CellProtocolDocuments/Deliverables/PDD_palazzo-concierge-formaalsmatch_2026-10-05/STATUS.md`, «Kjetils svar 7. oktober 2026»). Meldingen nevner ikke bordbestillingen. Spørsmål 4–7 står ubesvart: om vilkåret var oppfylt, hva den skal være for Palazzo, formålene og skissene (G1 og G1-GUI), og om grenen skal pushes. «G1-GUI godkjent.» i meldingen er lest som bildene for conciergen, ikke skissene her. Ingenting er gjort med grenen. Portene er urørt.
