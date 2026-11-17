# Astra: uavhengig gjennomgang av WP-K2-listen

Les `CellProtocolDocuments/Deliverables/PDD_butler-traadtre-og-widgetflate_2026-09-11/handoff/SKJELETT_ELEMENTER.md`
og de tre kartene den bygger på (`SKJELETT_GAP_tre.md`, `_chat.md`, `_flate.md`).

Kjetils regel av 2026-09-12: konklusjonen skal valideres uavhengig før den legges
fram. Denne listen ble lagt fram uten den valideringen. Din jobb er å finne ut om
den holder.

Svar i `handoff/ASTRA_SVAR_K2.md`. Bruk kilder, ikke vurderinger uten kilde.

1. **Er noe på listen unødvendig?** For hvert av E1, E2 og M1–M11: kan målet nås
   med dagens format? Pek på feltet eller komposisjonen i så fall. Særlig M7
   `layoutVariants` — den innfører vertskontekst i formatet, og det er den mest
   inngripende endringen. Finnes en mindre vei?

2. **Mangler noe?** Er det rader i de tre kartene med status «ny modifikator»
   eller «nytt element» som ikke er dekket av M1–M11 eller E1/E2? Navngi rad og
   felt.

3. **Er avgrensningene riktige?** §5 sier nei til generell uttrykksmotor, ny
   Card-case, ny Error-case, ny Disclosure-case, `full` i
   `SkeletonPresentationKind`, og gjettet breakpoint. Er noen av disse nei-ene
   feil?

4. **Holder testkontrakten i §4?** Særlig rekkefølgekonflikten i K-T1: T-P1
   (formålstesten mot referansebildene) krever staging med WP-R ute, altså etter
   merge til main. Er det en reell konflikt, og hva er den beste løsningen? Finnes
   det en preview-vei som kan kjøre før main?

5. **Er `Tree`-kontrakten gjenbrukbar?** C2 krever minst én bruk som ikke er
   Butler Chat. Bærer feltlisten utviklerbenkens oppgavetre
   (`PDD_utviklerbenk-oppgavegraf_2026-09-10`) uten endring? Hvis ikke, hvilket
   felt mangler?

6. **Navngi overdrivelser.** Hvis noe i dokumentet påstår mer enn kildene bærer,
   si hvilken setning og hva kilden faktisk sier.

Ingen kodeendring. Ingen git-mutasjon. Les-only.
