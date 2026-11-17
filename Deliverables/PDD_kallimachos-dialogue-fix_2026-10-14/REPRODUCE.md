# Reproduser lokal verifikasjon

Dette gjelder en isolert kandidat, ikke main eller staging. Kjør fra et CellScaffold-arbeidstre med basisrevisjon `308fbd071bb5cd89dd46f07647e8744d9bd7b056` og den vedlagte `evidence/implementation.patch`. Patchen inkluderer nye kildefiler og tester. Ikke legg den blindt over en annen skitten arbeidskopi.

## Forutsetninger

- Apple Silicon, eksisterende MLX/VLM-runtime og Qwen3.5-9B-4bit fra den tidligere lokale målingen. Modellfilhashene og pin ligger i `evidence/model.json`.
- Neutral modellalias `/private/tmp/haven-qwen35-9b`; loopback-server på 127.0.0.1:8087. Kjør bare én modell på denne porten. Modellserverens `/v1/models` må inkludere nøyaktig aliaset.
- Frosset offentlig Book-korpus ved revisjon `c8029847502fe007833d1ebd371bcb5adc01c3ae`, med provenienssidecar. De 37 filhashene finnes i den forrige leveransens `Deliverables/Kallimachos_RAG_Chain_2026-10-13/evidence/public-corpus.json` (CellProtocolDocuments-relativt).
- Bruk repoets bounded wrappers, 2 jobber og gjeldende Mac-kapasitetspolicy. Ikke kjør direkte swift test/build eller lag en ny ad-hoc cache.

## Avgrensede tester

Sett `KALLIMACHOS_HELDOUT_VALIDATORS` til denne leveransens `evidence/heldout/dialogue-cases.json`, `KALLIMACHOS_HELDOUT_VALIDATOR_RESULTS` til en eksplisitt lokal JSON-utfil og `HAVEN_COMMONS_CORPUS_ROOT` til det frosne Book-korpuset.

```sh
scripts/run_tests_isolated.sh --filter 'KallimachosDialogueRegressionTests|KallimachosAdvisorCellTests|CommonsLibrarianCellTests|AIGatewayProviderToolsOffTests'
```

## Reell kjede

Sett disse miljøvariablene i samme prosess som testkommandoen:

- `RUN_KALLIMACHOS_DIALOGUE_REGRESSION=1`
- `KALLIMACHOS_ADVISOR_LOCAL_PROFILE=qwen3.5-9b`
- `HAVEN_COMMONS_CORPUS_ROOT`: frosset offentlig korpus
- `KALLIMACHOS_DIALOGUE_MATRIX`: denne leveransens `evidence/live-matrix.json`
- `KALLIMACHOS_DIALOGUE_RESULTS`: eksplisitt lokal JSON-utfil
- valgfritt `KALLIMACHOS_RAW_MODEL_RESULTS`: rå modellutdata for syntetiske/offentlige tester, lokalt

```sh
scripts/run_tests_isolated.sh --skip-build --filter KallimachosDialogueRegressionTests.testLiveDialogueMatrix
```

Testen kobler faktiske Cell-instanser i testresolveren og bruker produksjonsadapteren til modellen. Den sertifiserer ikke GUI, nettverksruting til en deployet Cell eller produksjonsauth. Gateway-quota er testens noop-policy. Verktøypolicyen er deny-all, og egress til modellen går bare over loopback.

## Kildebytte og offline

`KallimachosAdvisorCellTests.testCanaryGroundingMatrixThroughAdvisorCell` krever `RUN_KALLIMACHOS_CANARY_TEST=1`, eksplisitt `KALLIMACHOS_ADVISOR_LIVE_TIER=local`, samme modellprofil, `KALLIMACHOS_CANARY_CORPUS_A/B/C` og syntetisk `KALLIMACHOS_CANARY_NONCE`. Armene har henholdsvis 7/11, fraværende fakta og endret 3/5. D spør modellen uten evidens. En bestått tallkontroll alene beviser ikke at D avstår fra oppdiktede forklaringer.

Stopp bare den modellprosessen testen selv startet, bekreft at porten er lukket, og kjør dialogrunneren med `KALLIMACHOS_EXPECT_OFFLINE=1` og `evidence/offline-matrix.json`. Behold deterministisk rute/svar/citations; AI-svar skal være null og status deterministic-fallback.

## Tolkning

`complete` er ikke en semantisk kvalitetsdom. Vurder summary, claims og gaps mot faktisk medsendte kilder. Frosne kriterier endres ikke etter observasjon. Runde 2 og senere er ublindede regresjonsmålinger, ikke nye blindtester. Rapporter inkluderer ikke requester-ID-er, lokale hjemmestier, modellforespørselsbody eller private dokumenter. Eksplisitte testrapporter og modelllogger ligger utenfor relation-sletting.
