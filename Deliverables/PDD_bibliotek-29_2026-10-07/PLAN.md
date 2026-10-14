# G2 — CellScaffold, d169 (2026-10-07)

G1 godkjent av Kjetil 07.10. Kjetil har bestilt denne planen og videre arbeid uten ny G2-runde. Ingen merge; G3 venter.

| Arbeidspakke / formål | Utfører | Test og leveranse |
|---|---|---|
| Forstå innlastingens eierbinding | Codex | Positiv AIAssistantThread-kontroll med separat servervault og eksplisitt, verifisert runtime-eierbinding; kildehenvisninger i rapport |
| Koble nøkler etter innlasting, uten endret eier/tilgang | Codex | DecodedCellStateBindingTests (Mermaid og Restaurant); runtime-hook fremfor decoder-Task |
| Dekke alle varig registrerte celletyper | Codex | Felles registry-avstemt lag/state/encode/decode/bind/ensure/state-test; begrunnede unntak uten state |
| Kontrollere avslag med a30 | Codex, skriptbane c | Samme test i isolert midlertidig arbeidstre med lokal avhengighet; ingen endring i PR-pinnen |
| Bygg og regresjon | Skriptbane c, etter tur | value-literals, build-tests, suite-coverage, full run-tests; logger i RELEASE/gui-2026.9.6/bibliotek-29 |
| Levering og aksept | Codex / Kjetil | Commit, push, PR mot main; TESTRESULT.md, ACCEPT.md, sluttrapport; G3 venter |

## Dataflyt
Persisted JSON → GeneralCell stored owner descriptor → host/resolver binds verified runtime identity with same cryptographic identity → ensureRuntimeReady → cell runtime hook → exact-home-vault check → permissions + intercepts → state read under unchanged authorization.

## Stoppregler
Ingen strict-vault-overstyring, debug-bypass, eierskifte, tilgangsutvidelse, pinneendring eller merge. Røde tester dokumenteres og årsaken undersøkes; ingen grønn port påstås før kjørt. Staging for kjetil2 må verifiseres etter separat autorisert utsetting.

## Lest av Codex
ScaffoldKit/PortholeRuntimeBindingEnsuring.swift, ScaffoldKit/PaymentGateOwnerIdentitySupport.swift, App/Cells/AI/AIAssistantThreadCell.swift (runtime-avsnitt), MermaidRendererCell.swift (decoder), RestaurantGuestShellCell.swift (decoder og nøkler), DecodedCellStateBindingTests.swift. Øvrige registrerte typer undersøkes i implementeringspakken; de er ikke lest ennå.
