# Plan – godkjent scope 2026-09-29

1. HD-0143: isoler adminfeil med eksisterende signert handshake; rett callback-livssyklus med tester; bygg/installér Binding fra publisert TLS-rettelse; verifiser riktig innlogget native bro uten å åpne en usikret rute.
2. HD-0144: opprett eierens ConferenceScaffold-prosjekt, rett prosjektvalg, registrer og les tilbake fire oppgaver med stabile ID-er og relasjoner. HD-køen er deploybevis, ikke erstatning for WorkItem.
3. HD-0145: fullfør produktgrensen rundt faktiske Conference/Arendalsuka-celler og bootstrap før ny host. EventCells-uttrekket alene er ikke en komplett deltakerreise. Bevar manifest-/resolver-/identitetskontroll, ett persistent skriveansvar og eksplisitt miljøbinding. Ikke kopier hele monolitten som en ferdig migrering.
4. HD-0146: revalider aktiv claim, kapasitet og staging-differanse (inkludert betalinger), integrer og test eksakt kandidat, lokale porter før CI, immutable artefakter, staging funksjon/restart/rollback, produksjon og kvittering tilbake til oppgaven.

Dataflyt: Workbench-eier -> ProjectPortfolio/WorkItem -> lokalt autorisert agentarbeid -> Git/test/artefakt -> ekstern deploykontroller -> Admin-observasjon -> WorkItem-evidens. Admin Workbench får ikke shell/Docker-autoritet.
