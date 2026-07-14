# E3b: deterministisk seleksjon og LCA

Dato: 2026-07-14. Status: holdt-ut eksperiment ferdig; E3b-modellvei venter på
Kjetils valg.

## Konklusjon

Restgapet i E2–E4 var i stor grad et bokføringsproblem: LCA ble utledet fra
modellens overvalgte JA-sett. Når `nearestSharedPurposeRef` i stedet utledes fra
resolverens egen prompt-evidens, blir LCA korrekt i 20/20 holdt-ut-caser for
alle fire modell-lag. Strict-score blir da begrenset av formålsseleksjonen, ikke
LCA.

En parameterfri, resolver-kompatibel multi-select-policy løftet holdt-ut
strict-score slik:

| Modell-lag | Tidligere relevant baseline | Prompt-evidens-LCA | Constrained multi-select |
| --- | ---: | ---: | ---: |
| Apple on-device ca. 3B | 85 % (gate 8) | 95 % | **100 %** |
| Ministral 3B | 65 % | 100 % | **100 %** |
| Qwen3 8B | 55 % | 90 % | **90 %** |
| gpt-5.5 | 60 % | 80 % | **90 %** |

Ingen av de nye policyene tapte et tidligere riktig holdt-ut-case. Mot den
relevante tidligere baselinen ga constrained-policyen 3/0, 7/0, 7/0 og 6/0
parvise gevinster/tap for henholdsvis Apple, Ministral, Qwen og gpt-5.5.

Resultatet støtter hovedfunnet «arkitektur slår modellstørrelse» på dette
fikstursettet. Det beviser ikke tilsvarende generalisering utenfor settet:
resolveren og gullsettet er samutviklet, og 20 testcaser betyr at ett case er
fem prosentpoeng. Den samme test-splitten er dessuten gjenbrukt gjennom E2–E4;
det kjente aggregerte feilmønsteret motiverte LCA-arbeidet. Dette er derfor
holdt-ut fra trening, men ikke et nytt blindsett.

## Formål og Goals

| purposeRef / goalRef | Metric, baseline og mål | Evidens | Status |
| --- | --- | --- | --- |
| `purpose://grounding.local-model-assisted-decomposition` / `goal.grounding.local-model-assisted-decomposition` | Metric: strict pass-rate på frosne modellutganger. Baseline: Apple 85 %, Ministral 65 %, Qwen 55 %, gpt-5.5 60 %. Mål i denne kjøringen: løft alle lag uten parvise tap; modellforslag forblir forslag under deterministisk validering. | `e3b_deterministic_lca_report.json`, uavhengig standardscorer | **satisfied in-distribution** |
| `purpose://test.acceptance.purpose-decomposition` / `goal.test.acceptance.purpose-decomposition` | Metric: reproduser baseline, lås 30/20-splitt, 0 ugyldige refs, 6/6 no-candidate/unknown-kontroller. Mål: alt oppfylt i samme kjøring. | split-hash, input-hasher, scorer-resultat | **satisfied** |
| Samme testformål, ekstern generalisering | Metric: strict og unknown-atferd på et nytt blindsett skrevet etter at policyen er frosset. Baseline: ikke målt. Mål: ingen regresjon mot dagens pipeline og minst samme LCA-korrekthet uten resolver/fikstur-samutvikling. | Krever nytt blindsett | **blocked** — manglende uavhengig datasett; eier: Kjetil/forskningssporet |

## Hypoteser og claim-adjudikering

| Claim | Type | Vurdering | Evidens / motargument |
| --- | --- | --- | --- |
| `claim.e3b.lca-is-deterministic-bottleneck`: LCA fra modellens JA-kjerne er hovedårsaken til strict-feilene. | causal, moderated | **supported på dette settet** | Prompt-evidens-LCA gir 100 % LCA-korrekthet i alle fire lag og 0 parvise tap. |
| `claim.e3b.constrained-selection-closes-all-errors`: Resolver-kompatibel multi-select fjerner hele restgapet i alle lag. | predictive, moderated | **contradicted** | Qwen og gpt-5.5 stopper på 90 % fordi to holdt-ut-caser per lag fortsatt mangler påkrevde formål. LCA er korrekt; dette er underseleksjon. |
| `claim.e3b.apple-100-generalizes`: Apples 100 % betyr at oppgaven er løst i produksjon. | predictive, assertive | **unsupported/open** | Bare 20 holdt-ut-caser, og resolver/fasit er samutviklet. Krever blind OOD-evaluering. |
| `claim.e3b.architecture-beats-lane-size`: Bedre deterministisk sammensetting gir større løft enn å gå til et større modell-lag i dette regimet. | causal, moderated | **supported på frosne E2–E4-utganger** | Apple går 85→100; gpt-5.5 går 60→90 med samme modellutganger. Ingen nye modellkall. |

## Metode

Eksperimentet bruker bare eksisterende, frosne utganger:

- Apple: `results/e3_apple_answers.jsonl`
- Ministral og Qwen: `results/e2_micro_log_20260713T055001Z.jsonl`
- gpt-5.5: `results/e2_micro_log_20260713T154416Z.jsonl`
- fasit: `fixtures/purpose_eval_cases.v0.jsonl`

Det ble ikke gjort modellkall, finjustering eller terskelsøk. Policyene var
deklarert i kode før `expected`-feltene ble lest for evaluering. Gate 8 brukes
bare som frosset E3-komparator. Tidligere aggregerte holdt-ut-resultater var
kjent fra handoveren; «ingen testetiketter brukt» betyr her at ingen per-case
`expected`-felt eller test-sweep ble brukt til å velge policy, ikke at testen
var usett historisk.

### Eksakt splitt

85 %-baselinen reproduseres bare med protokollen som E4 faktisk brukte:

1. behold de 50 casene med minst én kandidat/modellrad;
2. sorter case-ID-ene leksikografisk;
3. bruk indeks `% 5 >= 3` som test.

Dette gir 30 train og 20 test. Split-hash:

`b82b1f0a909e9aa2df8e193fe0ef433c085a15d372ec0649e338b38ba209766a`

Den tidligere formuleringen «case-indeks `% 5 >= 3`» var for vag: bruker man
rå filrekkefølge, blir Apple gate-8-resultatet 75 %, ikke rapporterte 85 %.
Denne leveransen låser derfor sorteringsregelen eksplisitt. De seks casene uten
kandidater inngår ikke i modell-lane-sammenligningen; de ble evaluert separat
gjennom deterministisk unknown/negation-fallback og passerte 6/6.

### Policyer

`prompt_evidence_lca`:

1. behold alle kjente kandidater modellen svarer JA på;
2. bruk vanlig `expandCoverage` og Goal-utledning;
3. sett `nearestSharedPurposeRef` fra `resolvePrompt(prompt)` i stedet for fra
   JA-settet;
4. hvis resolveren er `unknown`, fall tilbake til dagens topp-2-LCA.

`constrained_multiselect`:

```text
native = resolvePrompt(prompt)
positive = kjente kandidater med modellverdict JA

if native.status == resolved:
    selected = positive ∩ native.expandedPurposeRefs
    if selected er tom:
        selected = native.topPurposeRefs
    nearestSharedPurposeRef = native.nearestSharedPurposeRef
else:
    selected = positive eller purpose://prompt.unknown
    nearestSharedPurposeRef = LCA(topp-2 positive etter resolver-score)
```

Dette er en deterministisk constraint, ikke en ny modell. På de 20 testcasene
fjernet den 26, 31, 15 og 8 positive modellvalg for Apple, Ministral, Qwen og
gpt-5.5. Fallback la deterministisk til henholdsvis 1, 0, 1 og 2 refs. Det siste
er viktig: gpt-5.5s løft fra 80 % med bare LCA-fiksen til 90 % med constrained
multi-select kommer delvis fra eksplisitt resolver-fallback, ikke fra modellen.

## Resultater i mer detalj

| Modell | Legacy core-2 | Legacy gate 8 | Prompt-LCA: selection/LCA/strict | Constrained: selection/LCA/strict | Resolver-only-tak |
| --- | ---: | ---: | ---: | ---: | ---: |
| Apple ca. 3B | 60 % | 85 % | 95 / 100 / 95 % | 100 / 100 / **100 %** | 100 % |
| Ministral 3B | 65 % | 90 % | 100 / 100 / 100 % | 100 / 100 / **100 %** | 100 % |
| Qwen3 8B | 55 % | 75 % | 90 / 100 / 90 % | 90 / 100 / **90 %** | 100 % |
| gpt-5.5 | 60 % | 75 % | 80 / 100 / 80 % | 90 / 100 / **90 %** | 100 % |

Gate-8-kolonnen for andre modeller enn Apple er en fast ablasjon, ikke en
tidligere tunet baseline. `resolver_only_ceiling` fjerner modellen helt og er
kun et benchmark-tak. Den må ikke omtales som modellforbedring.

## Beslutning for E3b-veien

Claude anbefalte vei 2: norsk lokal modell via NanoGPT-runneren. Nett- og
maskinverifisering 2026-07-14 viser:

- NbAiLab publiserer en norsk/multilingual 3B-instruct-GGUF på
  `NbAiLab/nb-llama-3.2-3B-Instruct-Q4_K_M-GGUF` (3B, Q4_K_M, ca. 2,02 GB) med
  dokumentert `llama-server`-bruk.
- `llama-server` finnes lokalt: build 9070 (`f3e8d149c`), Apple arm64.
- Vektene er ikke funnet i lokal cache.
- NanoGPTs offentlige `GET /api/v1/models?detailed=true` listet
  `meta-llama/llama-3.2-3b-instruct`, men ingen NbAiLab- eller NorMistral-route.

Kilder:

- https://huggingface.co/NbAiLab/nb-llama-3.2-3B-Instruct-Q4_K_M-GGUF
- https://docs.nano-gpt.com/api-reference/endpoint/models
- read-only katalogrespons fra `https://nano-gpt.com/api/v1/models?detailed=true`
  hentet 2026-07-14

Anbefalingen presiseres derfor til **vei 2b: NbAiLab lokalt via
`llama-server`**, ikke «NbAiLab via NanoGPT». Det er ingen Apple Account
Holder-gating, men modellen må lastes ned etter Kjetils godkjenning. Eksisterende
NanoGPT-harness kan gjenbrukes mot llama.cpps OpenAI-kompatible localhost-API
med en ny `e3b_*`-runner.

LCA-resultatet gir samtidig en ny forsøksregel: E3b-modellen må måles på et
nytt blindt norsk/OOD-sett i tillegg til den gamle splitten. På dagens testsett
har Apple constrained-policy 100 %, så det finnes ingen målbar headroom for en
norsk modell uten tak-effekt.

**Kjetil-beslutning som gjenstår:** godkjenn vei 2b og modellnedlasting, velg
vei 1 (Apple toolkit), eller legg modellsporet på is. Anbefaling: vei 2b, med
blindsett først.

## Filer og verifikasjon

Nye filer, alle med `e3b_`-prefiks:

- `Tools/PurposeKnowledge/e3b_deterministic_lca_experiment.mjs`
- `Tools/PurposeKnowledge/results/e3b_deterministic_lca_outputs.jsonl`
- `Tools/PurposeKnowledge/results/e3b_deterministic_lca_report.json`
- `Tools/PurposeKnowledge/results/e3b_deterministic_lca_score.json`
- `Deliverables/e3b_deterministic_selection_lca_2026-07-14.md`

Kontroller:

- Baseline-reproduksjon: 60/65/55/60 % core-2 og Apple gate 8 = 85 %.
- Uavhengig standardscorer: 848/1000 over alle fire lanes × fem policyer × 50
  caser; per-policy-tall samsvarer med eksperimentrapporten.
- Constrained-policy, alle 50 evaluerbare caser: Apple 50/50, Ministral 50/50,
  Qwen 47/50, gpt-5.5 46/50.
- Holdt-ut: 20 caser per lane; 0 ugyldige refs; LCA 20/20 for begge nye
  resolver-støttede policyer.
- No-candidate/unknown-kontroller: 6/6.
- Secret-søk i nye filer: ingen treff.

Repoet hadde før dette arbeidet uløste konflikter og andre eksisterende
endringer. Ingen av dem er berørt. Publisering gjøres fra en ren, midlertidig
worktree slik at den konfliktfylte lokale `main`-arbeidskopien ikke brukes til
staging eller commit.

## Neste deduserte arbeid

1. Kjetil velger E3b-vei. Ved vei 2b: last ned den offisielle GGUF-en, logg
   eksakt repo/revisjon/hash i en ny `e3b_*`-manifestfil, og kjør en liten smoke
   før hele 153-kandidatmatrisen.
2. Lag et nytt blindt norsk/OOD-sett etter policyfrys: nye formuleringer,
   kryssgren-formål, negasjoner, unknown, lave resolver-scorer og minst én
   kandidat utenfor native coverage. Hold dette separat fra gammel test og fra
   resolverutvikling.
3. Evaluer fire armer på blindsettet: resolver-only, Apple + prompt-LCA, Apple
   + constrained multi-select, NbAiLab + samme deterministiske policy.
4. Bare dersom blindsettet bekrefter løftet uten tap, foreslå runtime-integrasjon
   i `purpose_resolver`/scaffold. Denne forskningsrunden endrer ingen kanonisk
   runtime.
