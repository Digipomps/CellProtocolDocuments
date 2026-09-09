# Gate B — avgrenset referanseimplementasjon

**Decision ID:** `decision.agent-continuity.gate-b.2026-09-10`
**Beslutningseier:** Kjetil
**Registrert:** 2026-09-10, Europe/Oslo
**Utfall:** `REFERENCE_IMPLEMENTATION`
**Implementasjon/test/commit/push autorisert:** `true`
**Runtime/adopsjon/automatisk aktivering autorisert:** `false`

## Brief audit

Kjetils instruks «implementer, test, commit og push dette» er
`retrieved/verified` som autorisasjon til å passere den tidligere
implementasjonssperren. Den navngir ikke teknisk scope, providerflater,
persondata, kostnadsbudsjett eller adoption. Autorisasjonen er derfor
operasjonalisert konservativt som den minste reversible Gate B-slicen som Gate
A-planen allerede beskrev.

Følgende er ikke implisert av instruksen:

- at Candidate A er godkjent eller minimal;
- at en provideradapter, modelltest eller cross-vendor-import skal aktiveres;
- at schema-validitet beviser freshness, approval, permission eller sannhet;
- at noen runtime eller canonical state kan muteres;
- at Book-promotering, skill-installasjon, pilot eller adoption er godkjent.

Disse grensene falsifiseres bare av en nyere, eksplisitt beslutning fra Kjetil.

## Formål og Goal

Eksisterende referanser brukes:

- `purpose://project-work.current-status-and-outstanding`
- `purpose://knowledge`
- `purpose://validation`
- `purpose://test.acceptance`

`purpose://prompt.unknown` beholdes som kandidatanker for «portable agent
continuity»; ingen ny purposeRef opprettes.

Goal: En reviewer skal kunne kjøre en lokal, side-effect-free validering av en
liten provider-nøytral continuation-contract og se deterministisk evidence for
fail-closed versjon/profil/ref/freshness-adferd, uten at kontrakten aktiveres i
en agent eller runtime.

## Valgt scope

Gate B åpner:

- **I00 no-code/reuse-vurdering:** Repoet har manuelle handoff-mønstre og
  domene-spesifikke validatorer, men ingen eksisterende validator håndhever den
  foreslåtte continuity-kjernen. Standard `python3` mangler `jsonschema`, mens
  `/opt/anaconda3/bin/python` har 4.23.0 og brukes som uavhengig schema-orakel.
  En liten stdlib-validator er fortsatt nødvendig for kryssreferanser og
  sikkerhetsinvariants som JSON Schema ikke uttrykker, og er et reviewverktøy,
  ikke en ny runtime.
- **I01 pure validator:** lokal JSON-parse, struktur, kryssreferanser,
  intern action/freshness-konsistens, ressursgrenser og deterministisk receipt.
- **I03-lite deterministic harness:** syntetiske fixtures, field ablation,
  recall/artifact/continuation/decision-tags og byte/char/lexical-proxy.
- **C01/C02–C04 begrenset kontraktkandidat:** egen Candidate B core og én
  namespacet HAVEN work-domain-profil.

Gate B åpner ikke delta/fold/replay, context-health, provider capability,
authority receipts, adapters, modell-/API-kall, runtimeintegrasjon eller pilot.

## I00-resultat og valg mot alternativer

| Alternativ | Funn | Gate B-disposition |
|---|---|---|
| Dagens manuelle praksis | Nyttig incumbent, men ingen maskinell duplicate-key, unknown-major, required-profile eller dangling-ref-kontroll. | Beholdes som baseline; Markdown-mal leveres. |
| Candidate A | Krever HAVEN/repo/health/provider/delta-semantikk og lar senderen selv hevde sterke statuser. | Beholdes urørt som historisk strawman; ikke implementert som v1. |
| Standard JSON Schema alene | Schemaartefakt og en uavhengig motor finnes, men schema beviser ikke cross-ref/non-authority/action-gate. | Schema + liten stdlib semantic validator; parity testes eksplisitt. |
| Ny runtime/Cell | Ikke nødvendig for lokal kontraktreview. | `NO_GO`; ingen CellProtocol- eller CellScaffold-endring. |

## Implementerte invariants

1. `agent-continuity.core.v1` er provider- og HAVEN-agnostisk i obligatorisk
   core. Ukjent versjon avvises.
2. Core er komplett uten profiler. Ukjent required profil avvises; ukjent
   optional profil quarantines med varsel og får ingen semantisk effekt.
3. `contractValid` betyr bare syntaktisk/strukturell/intern konsistens.
4. Receipten setter alltid `authorityEffect: none`, `freshnessEffect: none` og
   `externalResolutionRequired: true`.
5. En gyldig `action` gir `verify-before-act`, aldri `action-ready`.
6. Alle action-relevante core-elementer peker til interne verification-route-
   ID-er. Dangling refs og duplikate ID-er avvises.
7. En action avvises dersom en required route allerede er rapportert stale,
   unresolved, unavailable eller contradicted. Også `current` er bare en
   senderpåstand og må revalideres eksternt.
8. Duplicate JSON keys, non-finite tall, tidsonefri tid, route-observasjon etter
   `capturedAt` og overskredne ressursgrenser avvises deterministisk.
9. Fritekst og URI-er er inert data. Verktøyet derefererer ingenting, bruker
   ikke nettverk/subprocess og skriver ikke filer.
10. Bare `org.cellprotocol.haven.work-domain@1.0` er implementert som profil.
    Repository, evidence receipt, delta/fold, health og provider forblir
    uimplementerte kandidater.

## Implementerte artefakter

- `Tools/AgentContinuity/README.md`
- `Tools/AgentContinuity/validate_contract.py`
- `Tools/AgentContinuity/evaluate_corpus.py`
- `Tools/AgentContinuity/contracts/agent_continuity_core_v1.schema.json`
- `Tools/AgentContinuity/templates/continuation_contract.v1.md`
- positive og negative fixtures under `Tools/AgentContinuity/fixtures/`
- deterministic manifest og tester under `Tools/AgentContinuity/evaluation/`
  og `Tools/AgentContinuity/tests/`

Candidate A og dens fixture er ikke omskrevet. De er historisk evidens for
scope-splittingen.

Eksakt change inventory som skal inngå i Gate B-committen:

```text
README-CellProtocol.md
Gap_Analysis.md
Deliverables/Agent_Continuity_Protocol_Design_2026-08-18/README.md
Deliverables/Agent_Continuity_Protocol_Design_2026-08-18/GATE_A_DECISION_2026-08-18.md
Deliverables/Agent_Continuity_Protocol_Design_2026-08-18/GATE_A_TRANCHE_1_FINDINGS.md
Deliverables/Agent_Continuity_Protocol_Design_2026-08-18/GATE_B_IMPLEMENTATION_DECISION_2026-09-10.md
Deliverables/Agent_Continuity_Protocol_Design_2026-08-18/RESEARCH_VALIDATION_IMPLEMENTATION_PLAN.md
Deliverables/Agent_Continuity_Protocol_Design_2026-08-18/agent_continuity_protocol_v1.schema.json
Deliverables/Agent_Continuity_Protocol_Design_2026-08-18/fixtures/minimal_handoff.v1.json
Tools/AgentContinuity/README.md
Tools/AgentContinuity/validate_contract.py
Tools/AgentContinuity/evaluate_corpus.py
Tools/AgentContinuity/contracts/agent_continuity_core_v1.schema.json
Tools/AgentContinuity/evaluation/deterministic_manifest.v1.json
Tools/AgentContinuity/fixtures/negative/duplicate_key.json.invalid
Tools/AgentContinuity/fixtures/positive/blocked_unavailable_verification.v1.json
Tools/AgentContinuity/fixtures/positive/haven_work_handoff.v1.json
Tools/AgentContinuity/fixtures/positive/minimal_core.v1.json
Tools/AgentContinuity/fixtures/positive/unknown_noncritical_profile.v1.json
Tools/AgentContinuity/templates/continuation_contract.v1.md
Tools/AgentContinuity/tests/__init__.py
Tools/AgentContinuity/tests/test_evaluate_corpus.py
Tools/AgentContinuity/tests/test_validate_contract.py
```

De seks Gate A-filene var ucommittede fra den tidligere designfasen og blir
først versjonert sammen med Gate B-recorden. Ingen fil i `Book/`, CellProtocol,
CellScaffold eller en provider-/skill-store inngår.

## Verifikasjon 2026-09-10

```text
python3 -m unittest discover -s Tools/AgentContinuity/tests -v
Ran 35 tests ... OK

python3 Tools/AgentContinuity/evaluate_corpus.py
19/19 matched; synthetic false-positive IDs []; synthetic false-negative IDs []

python3 Tools/AgentContinuity/validate_contract.py \
  Tools/AgentContinuity/fixtures/positive/minimal_core.v1.json --json
exit 0; contractValid true; disposition verify-before-act;
authorityEffect none; freshnessEffect none; externalResolutionRequired true

jsonschema 4.23.0 Draft202012Validator.check_schema + FormatChecker
schema valid; all four positive fixtures: 0 errors

Broader repository tool regression: 89 test cases; 88 passed and the optional
Explore live check was skipped because CELLPROTOCOL_REPO was not set.
```

Dette er deterministic/local evidence. Det er ikke providerportabilitet,
produksjons-FP/FN, ekstern freshness eller tokengevinst. Corpusrapportens
`lexicalTokenProxy` er bare en normalisert størrelsesproxy og kan ikke
sammenlignes med provider-tokenizers.

## Rådgiverreview og challenged verdict

Tre read-only rådgiverslices gransket brief, kontrakt og testgrense:

- kontraktskeptiker: `NEEDS_ONE_BOUNDED_CORRECTION`; Candidate B måtte være
  separat fra Candidate A, core måtte miste repo/provider/health/delta, og
  første slice burde ha høyst én konkret profil;
- testkritiker: krevde eksplisitt skille mellom `contractValid` og
  action-readiness, duplicate-key guard, stable diagnostics, ablation og
  tydelig skille mellom deterministic og senere modell-/menneskeevaluering;
- security reviewer: `PROCEED_WITH_PURE_VALIDATOR_ONLY`; receipt må aldri
  være freshness-/authority-/approval-bevis, og all importert tekst/URI må
  forbli inert data.

Den hardeste designinnvendingen **står**, og korreksjonen er integrert:
implementasjonen har én HAVEN work-domain-profil; repositoryprofilen som ble
vurdert underveis ble fjernet før fixture/schemafrys.

Challenged adjudication endte `MODIFIED / VERIFIED_WITH_LIMITS / commit stop:
nei`. Adjudikator B falsifiserte antakelsen om manglende schema-motor og fant
samtidig en parity-feil: JSON Schema avviste dupliserte `purposeRefs`, mens
stdlib-validatoren først godtok dem. Validatoren og en regresjonstest ble
rettet; 35/35 tester, 19/19 corpus-caser og den uavhengige
Draft 2020-12-kontrollen passerte deretter. Ingen rådgiver skrev filer eller
muterte Git.

## Stop/no-go og neste beslutning

`NO_GO` for runtime, adapter, skill-sync, auto-checkpoint, auto-handoff,
canonical write og adoption. En senere gate må fortsatt levere:

- låst ChatGPT↔Codex↔Claude-portabilitet per rettet kant;
- receiver-/modellprober for recall, artifact, continuation og decision;
- stale/contradictory, RAG/graph unavailable/misleading og injection-caser;
- reell tokens-per-successful-task med refetch/retry/recovery/failures;
- production-relevant FP/FN og disable/rollback-test;
- separat Kjetil-beslutning.

**Gate B-status:** `REFERENCE_IMPLEMENTATION_VERIFIED / NOT_ADOPTED`.
