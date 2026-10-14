# W1 — første lokale testresultat 2026-10-12

Køkjørt engangsjobb `g2-w1-journal-20261012`, kildebase 9ff06f84 og de fire låste nye filene; CellProtocol 2026.9.7. Input/pinner verifisert av jobben. Bygget kom gjennom og kjørte 17 AppTests. Resultat: **15 bestått, 2 feilede testmetoder, 4 feilede assertions; exit 1**.

Alle 13 WorkbenchSessionJournalTests bestod. Entity-probene for rekonstruksjon og urelatert legacy-skriving bestod. Følgende feilet:
- `testLegacyBatchCannotOverwriteSignedJournalLeaf`: legacy-skriving kvitterte persisted og erstattet den beskyttede verdien.
- `testLegacyBatchCannotRemoveSignedJournalViaParentReplacement`: legacy-skriving kvitterte persisted og fjernet verdien ved erstatning av forelder.

Dette stemmer med den tidligere kildeanalysen. Testene ble kjørt mot den pinnede avhengigheten, ikke mot den separate CellProtocol-rettelsen. En grønn intern journal er ikke en fungerende integrert chat.

Evidens: `evidence/w1-first-test-result-20261012.json`; full logg/exit under `HAVEN-Deploy/_handoff/ARBEIDSBENK/G2-W1-20261012`. Maskinell opptelling skiller testmetoder fra assertions.

## Klargjort rettelse og foreslått neste verifikasjon

Kandidaten i `_worktrees/codex-workbench-entity-journal-20261012` bygger på CellProtocol 2026.9.7. Apple/Vapor legacy batch-stier validerer kandidaten mot journalens beskyttede verdier under eksisterende CommitGate før snapshot kan lagres. Åtte nye tester er skrevet og kildegransket, ikke kjørt. Patch: `HAVEN-Deploy/_handoff/ARBEIDSBENK/G2-W1-20261012/cellprotocol-legacy-batch-candidate.patch`; detaljgrense/review: W1_ENTITY_BOUNDARY.md og W1_ENTITY_INDEPENDENT_REVIEW.md.

Foreslått avgrenset godkjenning: én ny koordinert lokal verifikasjonsrunde av denne rettelsen, først de åtte nye CellProtocol-testene, deretter de 17 consumer-testene mot kandidaten når første del er grønn. Bruk eksisterende capacity/lease/bounded runner. Lokal avhengighetsoverstyring er bare utviklingsbevis; opprinnelige remote-pinner skal bevares og kontrolleres. Ingen betalt CI, endring av committede tester, PR/main/deploy eller automatisk ny kjøring etter rødt følger av testgodkjenningen.

## Stopp

PLAN.md linje 177: «Ikke kjør kontrollen på nytt uten Kjetils ord.» Ingen rerun eller kandidatbygg er startet. Køtråden er ikke UI-varslet om dette sluttresultatet: Macen låste seg før meldingen kunne sendes. Denne kvitteringen og RERUN-HOLD.md er skrevet lokalt; ikke påstå at Claude har lest dem.

## Ny eksplisitt testgodkjenning

2026-10-12: «Jeg godkjenner G1/G1-GUI for prosjektflaten og den avgrensede lokale testingen av CellProtocol-rettelsen. Fortsett.» Godkjenningen gjelder den avgrensede runden over. Kvittering: evidence/entity-retest-approval-20261012.json. Ingen ny Swift-kjøring er startet ved registreringen; nytt byggvindu avstemmes med køeier. Den gamle engangsjobben gjenbrukes ikke.

## Klargjort og overtatt av køeier

Ny pakke: HAVEN-Deploy/_handoff/ARBEIDSBENK/G2-W1-RETEST-20261012. Uavhengig scriptreview og C/UTF-8 check-only passerte. Deploy prosjekt køadministrasjon har lest pakken og bekreftet engangsaktivering etter d239-runden (KOORDINERING 12:25Z). Ingen Swift-kjøring/attempt startet ved denne oppdateringen. Nytt resultat er derfor fortsatt ukjent.
