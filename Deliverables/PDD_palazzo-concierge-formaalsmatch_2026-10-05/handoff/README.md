# Overlevering — conciergen med formålsmatch

Skrevet 7. oktober 2026 (natt til 7.), av Losen. Sier hvem som gjør hva, og hvordan arbeidet kommer fra Losens skyarbeidsområde til Mac-en, GitHub og verten. Stier er relative til HAVEN-roten; `HD` står for `HAVEN-Deploy/_handoff/HD-0077`, `PS` for `PalazzoScaffold`.

## Hvem gjør hva

| Hvem | Hva |
|---|---|
| Kjetil | Portene (G1-GUI, G2, G3), valgene i `PLAN.md`, terskelen og tallene som er mål, og hvert ord som trengs for å endre en committet test, bytte ut strakstiltaket eller sette ut |
| Losen (Claude i Cowork) | Koden og testene i `PS` for arbeidspakkene som står med Losen i `PLAN.md`, målingene, dokumentene, og køen i bane d |
| Uavhengige tråder (Claude) | Den blinde tolken, angrepet, revisoren og kontrollene. Ingen av dem har skrevet det de vurderer |
| Codex | Onboardingen og veien fra siden til gjestens entitet (egen oppgave, `PS/Deliverables/PDD_palazzo-onboarding_2026-10-02/`). Løftet til kjernen, hvis den veien velges. Hver overlevering får en egen promptfil med skript som kan kjøres uten å gjette |

## Veien fra skyarbeidsområdet til verten

Den er den samme som i strakstiltaket (`CellProtocolDocuments/Deliverables/PDD_palazzo-allergenvei-strakstiltak_2026-10-06/handoff/README.md`):

1. Filer skrives i skyarbeidsområdet, kopieres til `HD/` på Mac-en under nytt navn hver gang, og md5 kontrolleres på Mac-en i et eget steg før noe bruker dem.
2. Bygg og tester kjøres på Mac-en gjennom køen (`_losen-queue/inbox-d`), med `HD/mac/cp-pin-verifiser-og-test-20260929.sh` mot pinnen for CellProtocol. Losen kjører aldri `git` gjennom den monterte mappen og ber aldri Kjetil lime inn kommandoer.
3. Røde tester først: de nye testene kjøres mot koden før endringen, og «rød først» føres per test.
4. Commit med `HD/mac/deploy-commit-20261003.sh` (bare navngitte filer; skriptet viser hva som er med, før og etter), push og CI med `HD/mac/deploy-push-20261003.sh`. Testendringene leses rett fra git med `HD/mac/testendringer-20261003.sh` før hver commit.
5. Angrepet måles én gang gjennom koden før noe pushes. Et funn stopper.
6. Utsetting med `HD/mac/deploy-vert-20261003.sh` og egen claim, etter at claimene er lest. Enhver claim på verten stopper. Loggen til utgaven som står, leses fra containeren startet, før byttet. Uten kvittering med `COMMITTED_VERIFIED` kalles ingenting satt ut.
7. Måling på nett med de samme setningene, og skjermbilder ved siden av bildene, slik Kjetil har godkjent dem.

## Kjente hull

- Skriptene i `HD/mac/` har ikke tørrkjøring (`test.handoff.dry-run` står som blokkert fra runde 2). Bare veien tilbake har det; skriptet som setter ut (`HD/mac/deploy-vert-20261003.sh`), har det ikke.
- Veien tilbake (`HD/mac/tilbake-vert-20261006.sh`) er tørrkjørt, men selve byttet er aldri kjørt. Med forslaget i `PLAN.md` blir første vei tilbake å slå av miljøvariabelen for det nye kallet, så siden bruker `ask` som i dag.
- Nøkkelen til modellen ligger bare på verten. Hvordan modellen måles i utvikling, er et valg i `PLAN.md`.
