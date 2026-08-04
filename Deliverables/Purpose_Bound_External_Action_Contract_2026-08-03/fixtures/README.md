# Golden fixtures

Disse er normative testdata for A1, ikke eksempler på aktive CellProtocol-
objekter eller eksterne requests. Alle `action://example/`,
`destination://example/`, `agreement://example/` og tilsvarende refs er
syntetiske og må aldri mappes direkte til en runtime-route, nøkkel eller
mottaker.

| Fixture | Forventning | Hva den låser |
| --- | --- | --- |
| `positive/purpose-bound-action-intent.json` | aksepter | Én effekt, ett valgt primærformål og alle ni bindings-digests. |
| `positive/cell-execution-policy.json` | aksepter | Exact-only ceiling med policyprovenance; policyen er ikke en grant. |
| `positive/purpose-authorization-context.json` | aksepter | Contract/Grant-vei med current evidence og alle nødvendige checks. |
| `positive/action-decision-receipt.json` | aksepter | `allowed` er separat fra `not_executed`. |
| `negative/unknown-purpose-intent.json` | aksepter som blokkert intent | Ukjent formål kan ikke be om utførelse. |
| `negative/parent-match-only-context.json` | aksepter som denial | Parent-treff gir ikke child-autorisasjon. |
| `negative/facet-match-only-context.json` | aksepter som denial | Facet-treff gir ikke action-authority. |
| `negative/binding-digest-mismatch-context.json` | aksepter som denial | Endret digest gir ikke silent fallback. |
| `negative/storage-without-disclosure-receipt.json` | aksepter som denial | `s` gir ikke disclosure. |
| `negative/owner-path-without-ceiling-context.json` | aksepter som denial | Owner path kan ikke passere en manglende action ceiling. |
| `negative/no-authority-context.json` | aksepter som denial | En denial uten gyldig authority bruker `authorityPath=none`; den skal ikke oppdiktes som owner/Contract/cell-spesifikk. |
| `negative/owner-path-with-contract-refs.json` | schema-avvis | Owner path må ikke fylle inn oppdiktede Agreement/Contract/Grant-refs. |
| `negative/cell-specific-without-cell-authority-ref.json` | schema-avvis | Cell-spesifikk authority må ha eksplisitt cell-ref. |
| `negative/current-evidence-without-evidence-ref.json` | schema-avvis | Current/expired evidence må ha en faktisk evidence-ref; `not_required` og `unavailable` trenger ikke sentinel. |

I authorization-context betyr `storagePermissionSatisfied: true` i en case
uten storage-effekt «storage-kravet er korrekt vurdert som ikke utløst»; det
er ikke bevis på eller en innrømmelse av `s`.

`fixture-manifest.json` er den autoritative listen. Kontrollskriptet laster
bare fixtures derfra, slik at en ny case ikke kan se ut som den testes uten å
bli registrert.
