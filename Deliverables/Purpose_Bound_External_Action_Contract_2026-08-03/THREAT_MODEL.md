# Threat model — formålsbundet ekstern handling

Dato: 2026-08-03  
Status: normativ trusselmodell for A1; ikke bevis på at truslene er mitigert i
dagens runtime.

## Beskyttede verdier

- Brukerens kontroll over ytre effekt: provider-kall, sending, publisering,
  filskriving, shell, bridge og annen disclosure.
- Private data, payload-minimering, secrets og retention.
- Gyldigheten til Contract/Grant, domeneidentitet og revokasjon.
- Formålsintegritet: handlingens begrunnelse skal ikke skifte underveis.
- Reviderbar forklaring av allowance og denial.

## Tillitsgrenser

```text
Bruker / owner
  -> formålsdekomponering (uautorisert forslag)
  -> Intent + policy ceiling + authority context
  -> [A4: kontrollert Resolver/egressadapter]
  -> ekstern effekt / mottaker / provider

Trust package og modelloutput er evidens ved siden av beslutningen;
de er ikke en pil som gir authority.
```

## Trusler og normative mottiltak

| ID | Trussel | Angrepsvei | A1-mottiltak | Residual / A4-behov |
| --- | --- | --- | --- | --- |
| T1 | Purpose laundering | Bredt formål, f.eks. «hjelp brukeren», brukes for disclosure. | Én konkret effekt, exact primary purpose, destinasjon- og dataceiling. | Krever menneskelig taxonomy-governance og A4-gate. |
| T2 | Prompt injection | Utrustet tekst forsøker å endre formål, policy eller destinasjon. | Modelloutput er bare proposal; policy leser validerte wire-felter. | A4 må isolere system-/tool-input og teste injeksjon. |
| T3 | Parent escalation | Parent-formål godtas for ubundet child-handling. | `parentPurposeImpliesChild=false`; exact match. | Fremtidig delegering trenger eksplisitt schema-revisjon. |
| T4 | Facet escalation | Privacy/quality-facet tolkes som rettighet til action. | `facetsAreNonAuthorizing=true`. | UI må ikke skjule dette skillet. |
| T5 | Confused deputy | AI/script bruker eierens eller gatewayens brede tilgang. | Policy ceiling, effect binding, owner-path-no-bypass og egen purpose-bound Cell med ett Grant. | Implementert for `PurposeBoundAIGatewayCell.ai.invokePurposeBound`; øvrige action-familier gjenstår. |
| T6 | Direkte script-egress | Script åpner nettverk/shell/fil uten Cell action. | A1 krever mediert I/O; ellers er action denied/out of scope. | Sandbox/host-policy må implementeres og angripes i test. |
| T7 | Config/policy substitution | Klient bytter CellConfiguration, policy eller plan etter preview. | Alle relevante digests bindes i intent/context/receipt. | Velg canonicalization og signer/forankre den. |
| T8 | Payload substitution | Godkjent action kjøres med annen payload/data. | `payloadDigest` er nødvendig binding. | Håndhev at faktisk request bytes gir samme digest. |
| T9 | Storage → disclosure | `s` eller cache tolkes som videresendingsrett. | Separate storage/disclosure-felter og capabilities. | Kontroller logger, backups, trainer og downstream. |
| T10 | Trust theater | Signert eller detaljert pakke vises, men gateway ignorerer den. | Trust package merkes non-authorizing; receipt viser policy/authority path. | End-to-end allow/deny-test og deployed path evidence. |
| T11 | Stale evidence | Utløpt trust package, consent eller provider-faktum brukes videre. | Context må binde evidence status/expiry; unknown feiler lukket. | Definer tidskilde og revocation distribution. |
| T12 | Owner bypass | Owner path overskriver ekstern action ceiling. | Normativ `ownerPathMayBypassExternalActionCeiling=false`. | Negativt testet for A4-v1; må fortsatt finnes og avvises i hver øvrige adapter. |
| T13 | Receipt overclaim | «allowed» tolkes som at ekstern effekt faktisk skjedde. | Receipt skiller `decisionStatus` fra `executionStatus`. | Faktisk effect receipt krever separat transport-/mottakerbevis. |
| T14 | Audit-log leakage | Full prompt, secrets eller private data kopieres til receipt. | Bare digests/manifester; secrets er forbudt i receipt. | A4 må klassifisere og teste logger, krasjrapporter og telemetri. |
| T15 | Documentation-to-runtime gap | En bok eller schema tolkes som generell purpose-håndheving. | Claim ledger og A4-rapport skiller den dedikerte Cell/keypathen fra restscope. | Capability-påstand kan gis for `PurposeBoundAIGatewayCell.ai.invokePurposeBound`, ikke for generell egress. |

## Denial-atferd

Et deny skal være typed, saklig og sikkert å vise:

- ikke inneholde secret, rå payload eller unødvendig privat kontekst
- angi hvilken policy-/bindingstest som feilet
- ikke foreslå en ny capability som automatisk fallback
- ikke utføre «best effort» egress etter denial
- være loggbar med hashes og correlation ID når retention er lovlig

## Testminimum før A4 kan kalles beskyttende

1. Ukjent formål og prompt-injection gir denial uten sideeffekt.
2. Parent- og facet-only match gir denial.
3. Feil action, destinasjon, datamanifest, plan, config, policy, taxonomy eller
   payload digest gir denial.
4. Owner path uten action ceiling gir denial.
5. `s` uten disclosure-capability gir denial av disclosure.
6. Utløpt/revokert Contract, consent eller evidens gir denial.
7. Direkte script-nettverk/shell er teknisk blokkert eller er fraværende fra
   execution-miljøet.
8. Faktisk provider-/transportrequest kan korreleres med en gyldig receipt,
   men rå hemmeligheter havner ikke i loggen.
