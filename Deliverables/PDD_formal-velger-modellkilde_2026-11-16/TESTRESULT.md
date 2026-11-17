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

## Ikke kjørt ennå
T-ROT (staging), T-VERT, T-SI-FRA, T-VERTSCELLE, T-LIKEVERDIG, T-HENDELSER, T-ENHET, T-HELSE, T-TJENESTE, T-INGEN, T-FORKLART, test.cell.auth-negative, test.regression, test.gui.*.
