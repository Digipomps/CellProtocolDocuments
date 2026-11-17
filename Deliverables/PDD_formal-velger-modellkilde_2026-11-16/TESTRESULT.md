# TESTRESULT — La formålet velge språkmodellkilde

Fylles ut etter hvert som arbeidspakkene lander. Rader uten utdata er ikke kjørt.

## build
<a id="build"></a>
- 2026-11-17, WP0 baseline: CellScaffold main `57ce8c0`, sjekkene «Image pipeline contract checks» og «Look up green gate for this exact tree» er grønne. Full testkjøring er ikke kjørt som baseline her; første fulle bygg er CI på CellScaffold #454. HavenAgentD-baseline på Mac: **ikke kjørt**.
- 2026-11-17, WP2–4 i isolert pakke (Docker `swift:6.1-noble`, ekte CellBase 2026.9.15, stedfortredere for `ChatPurposeContext`, `ChatPurposeResourceMatch`, `ChatAIGatewayRequest`): `Build complete!`. Hele App-målet er ikke bygget i skyen (private DiMy-pakker).

## krav
<a id="krav"></a>
- Python-referanse: `python3 Tools/ModelSourceEligibility/model_source_eligibility.py` → `35/35 vektorer stemmer`.
- Swift: `ModelSourceEligibilityTests` → `Executed 5 tests, with 0 failures`.

## fakta, filter, uttalt, laptop
<a id="fakta"></a><a id="filter"></a><a id="uttalt"></a><a id="laptop"></a>
- Swift: `ModelSourceRoutingTests` → `Executed 12 tests, with 0 failures` (samlet kjøring: `Executed 17 tests, with 0 failures`).
- To forventninger i testene var feil ved første kjøring og ble rettet, ikke koden: lokale regler rangeres foran en erklært hostet kilde (uendret rangering), og en laptop uten måling mangler også helse og svartid i «tjeneste for andre».
- De nye testene er ikke kjørt røde mot koden uten filteret.

## sprak
<a id="sprak"></a>
- Swift og Python gir samme svar på 35 vektorer. Go: **ikke kjørt**. PyCellProtocol-porten: ikke laget (referansen ligger i CellProtocolDocuments).

## si-fra, vertscelle, hendelser, helse
<a id="si-fra"></a><a id="vertscelle"></a><a id="hendelser"></a><a id="helse"></a>
- 2026-11-17, CellScaffold `b533ecd` i isolert pakke (Docker `swift:6.1-noble`, ekte CellBase 2026.9.15; stedfortredere for `PortholeRuntimeBindingEnsuring` og `makeCellProtocolTestIdentity`): `Executed 41 tests, with 0 failures`.
- T-SI-FRA, `LocalModelAvailabilityTests` (20): registrering alene gir ikke valg; erklæring fra broen godtas; fra annen identitet, feil kontrakt, ukjent kilde eller uten `cap.local_model.generate` avvises; eieren trekker tilbake fra en annen økt; maskinen trekker tilbake over broen; fremmed kan ikke; lukket bro og utløpt kontrakt trekker tilbake med grunn.
- T-HELSE: ingen måling og måling eldre enn 10 min gir ingen helse; treg måling beholdes; feilet måling trekker tilbake med `health_failed`; måling fra annen identitet avvises.
- T-HENDELSER: rekkefølgen `available, health, selected, fallback_used, unavailable`; hendelsene inneholder verken spørsmålet eller svaret; loggen er begrenset til 100 per eier.
- T-VERTSCELLE, `LocalModelAvailabilityCellTests` (1): eieren leser tilstand og hendelser og trekker tilbake gjennom cellen; en identitet uten Agreement får verken tilstand, hendelser eller tilbaketrekking.
- Ikke dekket ennå: at en Agreement-holder (ikke eier) ser modellen gjennom cellen. Registeret støtter det (`declarations(visibleTo:hasAgreement:)`, testet), men ingen flate spør med Agreement før WP10.
- Ikke bygget i skyen: endringene i `OrchestratorCell.swift`, `PersonalCopilotCloudStore.swift` og `configure.swift`. Første bygg er CI på #454.

## CI på #454
- `b2b344c`: «Focused control-plane gates» feilet i `ci/test-suite-coverage.sh` før Swift-bygget, fordi de nye testsuitene ikke sto i `ci/test-filter.txt`. Rettet i `51538da`.

## laptopsiden (WP7)
<a id="enhet"></a>
- 2026-11-17, HavenAgentD `a7142d9` (utkast-PR #43), bygget på Kjetil-sin-M5 i eget arbeidstre: `Build complete!`. `LocalModelAvailabilityTests` → `Executed 5 tests, with 0 failures`. `LocalModelAvailabilityClientTests` → `Executed 2 tests, with 0 failures`. `PortholeIngressSessionTests` → 3 tester bestått.
- CellScaffold #454 `b533ecd`: CI «Focused control-plane gates» grønn; `LocalModelAvailabilityTests`, `LocalModelAvailabilityCellTests`, `ModelSourceEligibilityTests`, `ModelSourceRoutingTests` og `NativeLocalModelBridgeTests` kjørte og besto der.
- Ikke kjørt: en ekte kunngjøring fra AgentD mot en vert med #454. Helsemålinger fra laptopen er ikke skrevet.

## Ikke kjørt ennå
T-ROT (staging), T-VERT, T-LIKEVERDIG, T-ENHET, T-TJENESTE, T-INGEN, T-FORKLART, test.cell.auth-negative på tvers, test.regression, test.gui.*. Ende-til-ende laptop mot vert er ikke kjørt.
