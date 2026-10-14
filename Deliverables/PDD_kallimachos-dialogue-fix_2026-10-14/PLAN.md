# Plan og gjennomføring

Direkte autorisert av Kjetils oppdrag 2026-10-14. Ingen push, deploy eller finjustering.

1. Rotagent: bygg og kjør eksisterende CommonsLibrarian/Advisor-tester før kildeendring; bevar faktisk baseline.
2. Kontekst: avgrenset historikk per requester/relation, referanseavklaring, reload og bekreftet sletting. Test deterministisk først.
3. Retrieval: prioriter definisjonsoverskrifter for nevnte begreper i offentlig profil; bevar eksakte utdrag og standard søk.
4. Validering: kontroller struktur, kilde-ID, modenhet og konkrete myndighetspåstander. Avvist modellprosa fjernes; deterministiske kilder og faktisk kostnad beholdes.
5. Modell: allowlist av lokale profiler, identitet i runtime; Qwen3.5 thinking av i HTTP-adapteren.
6. Bygg endret kilde; kjør berørte tester og verdi-literal-port. Deretter kjør faktisk CommonsLibrarian → Advisor → AIGateway → Qwen3.5 med frosset offentlig Book-korpus.
7. Uavhengig blindsett er frosset før implementering; leses først etter kandidatfrys. Rapporter kvalitet separat fra transport og validator.
8. Uavhengig kodediff-review og læringsfangst. Modellvalg vurderes først etter målingene.

## Dataflow
Se dataflow.md. Tidligere modellsvar er bare kontekst, aldri kilder eller myndighet.

## Byggegrunnlag
CellScaffold origin/main 308fbd071bb5cd89dd46f07647e8744d9bd7b056. Primært arbeidstre er urørt. Bygg bruker scripts/run_tests_isolated.sh, to jobber og 40 GiB/10 % ledig-disk-port. Ingen gamle binærer kan verifisere nye rettinger.
