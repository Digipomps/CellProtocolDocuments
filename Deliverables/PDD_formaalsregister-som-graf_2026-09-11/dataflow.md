# Dataflyt — formålsregister som graf

Utkast 2026-09-12. Stier relative til `HAVEN/`. Hver kant navngir kontrakten den går på.

## Kanter

| Fra | Til | Hva som går | Kontrakt | Merknad |
|---|---|---|---|---|
| forsont kildefil | generator | taksonomien som data | `contract/taksonomi-forsoning.md` | eneste kilde (Q1) |
| generator | `Book/haven_purpose_knowledge_base_v1.json` | generert Book-utgave | hash-par lagres | divergens = rød |
| generator | runtime-tabell i CellScaffold | generert Swift-tabell | hash-par lagres | divergens = rød |
| forsont kildefil | `cell:///PurposeRegistry` | noder og kanter, **bare fra `parentRef`** | `contract/purpose_registry_contract_v0.json` | D0: aldri fra punktum i ref |
| `cell:///PurposeRegistry` | matchemotoren | `PerspectiveNode`-graf | intern | én motor (Q6) |
| oppslagsvei | `cell:///PurposeRegistry` | `registry.match(signal:)` | Explore + eier-scopet Grant | ingen tokens i vanlig tilfelle |
| `Signal` | noder underveis | `localVariables`, `hops`, `ttl` | `Signal.swift` | lag 2 leser det lag 1 la igjen |
| matchemotoren | kaller | `HitCollector` + score + forklaring per kant | intern | forklaring uten å lekke mer enn i dag |
| `cell:///PurposeRegistry` | `AIGatewayPurposePolicy` | `taxonomyDigest` | A4 | endres taksonomien, må signerte pakker utstedes på nytt |
| ingen treff | kaller | `purpose://prompt.unknown`, differensiert etter polaritet | A4 | **åpner ingenting** |

## Det som ikke går noen vei

- Ingen personnode inn i fellesregisteret. Entiteter representeres i eierens egen entitet.
- `RelationalLearningEngine` kobles **ikke** på fellesregisteret i denne oppgaven.
- Et matchresultat blir aldri en rettighet. Purpose kan snevre inn en rett, aldri skape den.
- Ingen kant utledes av ref-strengens punktform (D0).
