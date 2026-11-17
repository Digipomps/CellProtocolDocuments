# Formålssammensetning — leveranserapport

Dato: 2026-09-09. Kontrakt: `Book/36_Purpose_Composition.md`, med oppdragets
uttrykkelige godkjenning og unntak for regel 1. Book 23 er ikke migrert.

## Lokal commit

Kode, tester og rapport er ferdigstilt i arbeidsmappen. **Lokal commit er
foreløpig blokkert**: `git add` returnerte 128 fordi `.git/index.lock` finnes.
Ingen filer var staged før forsøket. Låsen er ikke fjernet av denne jobben.
Ingen push, tagging eller branchbytte er utført. Nåværende branch er
`codex/docs-cleanup-20260810`.

Faktisk utdata fra stagingforsøket:

```text
fatal: Unable to create '/Users/kjetil/Build/Digipomps/HAVEN/CellProtocolDocuments/.git/index.lock': File exists.

Another git process seems to be running in this repository, e.g.
an editor opened by 'git commit'. Please make sure all processes
are terminated then try again. If it still fails, a git process
may have crashed in this repository earlier:
remove the file manually to continue.
```

Låsen hadde mtime `2026-09-09T14:06:49.347346` ved kontroll kl.
`2026-09-09T14:11:13.605948`. `lsof .git/index.lock` viste en åpen lesereferanse
fra `com.apple`, PID 81725. Prosessinventar via `ps` ble avvist av miljøet
(`Operation not permitted`). Dette beviser ikke at låsen trygt kan fjernes.

## Endrede filer

- `Book/haven_purpose_knowledge_base_v0.json` — Kun schemaRef og compatibility.model. De 57 nodene og changePolicy er urørt.
- `Book/haven_purpose_packages_v0.json` — schemaRef til pakkeschema. Eksisterende pakker er urørt.
- `Book/haven_purpose_composition_v0.schema.json` — Felles JSON Schema-definisjoner for fem kombinatorer, barnerekkefølge og atskilte kjøringsdata.
- `Book/haven_purpose_knowledge_base_v0.schema.json` — KB-schema med felles node- og execution-form.
- `Book/haven_purpose_packages_v0.schema.json` — Pakkeschema med samme form for purposes.
- `Book/haven_purpose_composition_run_v0.schema.json` — Schema for oppgavens PURPOSE_COMPOSITION.json.
- `Tools/PurposePackages/purpose_dev.py` — Kobler validate og gates til sammensetningskontrollen; skriver advarselsantall og separat portstatus.
- `Tools/PurposePackages/purpose_composition.py` — Ren stdlib: struktursjekk, historiske målinger, grenvalg og invariantkontroll.
- `Tools/PurposePackages/tests/test_purpose_composition.py` — 29 unittest-tester med grønne og negative veier for hver av reglene og tabellradene, samt tids-, blocker-, schema- og CLI-regresjoner.
- `Tools/PurposePackages/README.md` — Bruksanvisning, loggformat, tidsregler, returverdier og syntetisk sekvenseksempel.
- `_leveranse/FORMAALSKOMPOSISJON_RAPPORT.md` — Denne leveranserapporten med faktisk testutdata.

`purpose_dev.py` lå allerede i arbeidsmappen, men var ikke sporet av Git ved
oppstart. Den eksisterende funksjonaliteten er beholdt; den lokale commiten
må derfor inkludere hele filen, i tillegg til den nye evalueringsmodulen.
Andre eksisterende endringer, blant annet i Book 23, katalogen,
lærdomsregisteret, Explore, nettstedet og øvrige leveranser, er ikke inkludert.
Den foreliggende Book 36-filen var også usporet og er ikke endret her.
Correspondence-repoene, staging og Swift package-konfigurasjon er ikke endret.

## Målinger

### Uendrede kanoniske data

Sammenligningen brukte en kopi tatt før redigering. Faktisk utdata:

```text
57 nodes unchanged: JSON and byte comparison PASS
changePolicy unchanged: PASS
nodes SHA256: 7c2db1c77a3802d0cfea9cf9489369adc399bfb910057185db7e73fff784dfaa
Existing packages unchanged: PASS
Tools/PurposePackages/purpose_dev.py Python 3.9 grammar PASS
Tools/PurposePackages/purpose_composition.py Python 3.9 grammar PASS
Baseline script exists in git HEAD: False
```

SHA256 gjelder `json.dumps(nodes, sort_keys=True).encode()`. I tillegg ble
selve nodes-arrayens tekst sammenlignet byte for byte. Git-diffen for
kunnskapsbasen inneholder bare `schemaRef` og den nye model-strengen
`single-parent-tree-with-explicit-composition-and-cross-cutting-facets`.
`changePolicy` har samme verdi som før.

### WP-2 — advarselsantall

**18 noder** utløser regel 1-advarselen. Alle 18 er blant de 57 Book 23-nodene.
Ingen pakkeformål eller oppgavenoder kommer i tillegg ved `validate` uten
oppgavemappe. Returkode: 0.

Kommando:

```sh
python3 Tools/PurposePackages/purpose_dev.py validate
```

Faktisk utdata fra sluttkjøringen:

```text
ADVARSEL: purpose://root: ikke-løvnode uten composition (regel 1; migrering gjenstår)
ADVARSEL: purpose://human-agency: ikke-løvnode uten composition (regel 1; migrering gjenstår)
ADVARSEL: purpose://contact.communication: ikke-løvnode uten composition (regel 1; migrering gjenstår)
ADVARSEL: purpose://event.participation: ikke-løvnode uten composition (regel 1; migrering gjenstår)
ADVARSEL: purpose://digital-work: ikke-løvnode uten composition (regel 1; migrering gjenstår)
ADVARSEL: purpose://digital-work.coordinate: ikke-løvnode uten composition (regel 1; migrering gjenstår)
ADVARSEL: purpose://project-work.overview-and-sharing: ikke-løvnode uten composition (regel 1; migrering gjenstår)
ADVARSEL: purpose://digital-work.collect-structured-input: ikke-løvnode uten composition (regel 1; migrering gjenstår)
ADVARSEL: purpose://questionnaire.campaign.complete: ikke-løvnode uten composition (regel 1; migrering gjenstår)
ADVARSEL: purpose://gui.quality.functional-accessible: ikke-løvnode uten composition (regel 1; migrering gjenstår)
ADVARSEL: purpose://quality: ikke-løvnode uten composition (regel 1; migrering gjenstår)
ADVARSEL: purpose://governance: ikke-løvnode uten composition (regel 1; migrering gjenstår)
ADVARSEL: purpose://access.audit.privacy: ikke-løvnode uten composition (regel 1; migrering gjenstår)
ADVARSEL: purpose://validation: ikke-løvnode uten composition (regel 1; migrering gjenstår)
ADVARSEL: purpose://test.acceptance: ikke-løvnode uten composition (regel 1; migrering gjenstår)
ADVARSEL: purpose://knowledge: ikke-løvnode uten composition (regel 1; migrering gjenstår)
ADVARSEL: purpose://grounding: ikke-løvnode uten composition (regel 1; migrering gjenstår)
ADVARSEL: purpose://self-determination.data: ikke-løvnode uten composition (regel 1; migrering gjenstår)
Composition regel 1: 18 noder uten composition (18 Book 23-noder) — advarsel, ingen default
5 pakker, 13 pakkeformål, 31 lærdommer, 57 Book 23-noder — OK
```

Lærdomsregisteret endret seg fra 29 til 31 poster under arbeidet gjennom
andre arbeidsendringer. Det er ikke redigert eller staged av denne jobben.
Advarselsantallet for formål var 18 både før og etter dette.

### WP-4 — Python 3.13.5, macOS

```sh
python3 -m unittest discover -s Tools/PurposePackages/tests -v
```

Faktisk utdata (returkode 0):

```text
test_composition_on_package_purpose_and_kb_node_reaches_cli (test_purpose_composition.CommandLineAndSchema.test_composition_on_package_purpose_and_kb_node_reaches_cli) ... ok
test_gates_cli_all_states_and_validate_false_green (test_purpose_composition.CommandLineAndSchema.test_gates_cli_all_states_and_validate_false_green) ... ok
test_gates_uses_root_composition_not_implicit_allof_over_descendants (test_purpose_composition.CommandLineAndSchema.test_gates_uses_root_composition_not_implicit_allof_over_descendants) ... ok
test_missing_and_malformed_task_files_fail_closed (test_purpose_composition.CommandLineAndSchema.test_missing_and_malformed_task_files_fail_closed) ... ok
test_schema_references_resolve_and_composition_is_shared (test_purpose_composition.CommandLineAndSchema.test_schema_references_resolve_and_composition_is_shared) ... ok
test_validate_repository_warning_count_and_preserved_canonical_nodes (test_purpose_composition.CommandLineAndSchema.test_validate_repository_warning_count_and_preserved_canonical_nodes) ... ok
test_allof_green_and_red (test_purpose_composition.GateTable.test_allof_green_and_red) ... ok
test_anyof_green_and_red (test_purpose_composition.GateTable.test_anyof_green_and_red) ... ok
test_blocked_is_not_hidden_by_an_invalid_sequence_attempt (test_purpose_composition.GateTable.test_blocked_is_not_hidden_by_an_invalid_sequence_attempt) ... ok
test_blocked_is_preserved_for_every_kind_even_if_quorum_met (test_purpose_composition.GateTable.test_blocked_is_preserved_for_every_kind_even_if_quorum_met) ... ok
test_firstof_cannot_resume_after_revoked_success (test_purpose_composition.GateTable.test_firstof_cannot_resume_after_revoked_success) ... ok
test_firstof_green_and_red (test_purpose_composition.GateTable.test_firstof_green_and_red) ... ok
test_firstof_preference_order_stop_and_unknown_branch (test_purpose_composition.GateTable.test_firstof_preference_order_stop_and_unknown_branch) ... ok
test_green_report_is_checked_at_report_time_not_using_future_evidence (test_purpose_composition.GateTable.test_green_report_is_checked_at_report_time_not_using_future_evidence) ... ok
test_invariant_failure_cannot_be_bypassed_by_anyof_quorum (test_purpose_composition.GateTable.test_invariant_failure_cannot_be_bypassed_by_anyof_quorum) ... ok
test_invariant_green_and_red (test_purpose_composition.GateTable.test_invariant_green_and_red) ... ok
test_invariant_missing_or_misordered_measurements_and_unfinished_step (test_purpose_composition.GateTable.test_invariant_missing_or_misordered_measurements_and_unfinished_step) ... ok
test_invariant_over_firstof_checks_only_executed_alternatives (test_purpose_composition.GateTable.test_invariant_over_firstof_checks_only_executed_alternatives) ... ok
test_malformed_input_is_rejected_without_traceback (test_purpose_composition.GateTable.test_malformed_input_is_rejected_without_traceback) ... ok
test_measurements_cannot_be_replaced_by_opinions_or_green_reports (test_purpose_composition.GateTable.test_measurements_cannot_be_replaced_by_opinions_or_green_reports) ... ok
test_nested_sequence_checks_historical_composed_predecessor (test_purpose_composition.GateTable.test_nested_sequence_checks_historical_composed_predecessor) ... ok
test_sequence_green_and_red_at_attempt_time (test_purpose_composition.GateTable.test_sequence_green_and_red_at_attempt_time) ... ok
test_sequence_revocation_equal_timestamp_missing_attempt_and_retry (test_purpose_composition.GateTable.test_sequence_revocation_equal_timestamp_missing_attempt_and_retry) ... ok
test_rule_1_non_leaf_requires_composition_warning_during_migration (test_purpose_composition.ValidationRules.test_rule_1_non_leaf_requires_composition_warning_during_migration) ... ok
test_rule_2_sequence_order_unambiguous (test_purpose_composition.ValidationRules.test_rule_2_sequence_order_unambiguous) ... ok
test_rule_3_anyof_threshold (test_purpose_composition.ValidationRules.test_rule_3_anyof_threshold) ... ok
test_rule_4_green_firstof_requires_registered_branch (test_purpose_composition.ValidationRules.test_rule_4_green_firstof_requires_registered_branch) ... ok
test_rule_5_invariant_requires_over_inside_same_tree (test_purpose_composition.ValidationRules.test_rule_5_invariant_requires_over_inside_same_tree) ... ok
test_rule_6_green_report_must_follow_table_for_every_kind (test_purpose_composition.ValidationRules.test_rule_6_green_report_must_follow_table_for_every_kind) ... ok

----------------------------------------------------------------------
Ran 29 tests in 1.229s

OK
```

### Python 3.9.6 fra en annen arbeidsmappe

Arbeidsmappe: `/tmp`. Kjøringen verifiserer både Python 3.9 og at import og
repo-relative dataoppslag fungerer uavhengig av terminalens arbeidsmappe.

```sh
/usr/bin/python3 -m unittest discover -s /Users/kjetil/Build/Digipomps/HAVEN/CellProtocolDocuments/Tools/PurposePackages/tests -v
```

Faktisk utdata (returkode 0):

```text
test_composition_on_package_purpose_and_kb_node_reaches_cli (test_purpose_composition.CommandLineAndSchema) ... ok
test_gates_cli_all_states_and_validate_false_green (test_purpose_composition.CommandLineAndSchema) ... ok
test_gates_uses_root_composition_not_implicit_allof_over_descendants (test_purpose_composition.CommandLineAndSchema) ... ok
test_missing_and_malformed_task_files_fail_closed (test_purpose_composition.CommandLineAndSchema) ... ok
test_schema_references_resolve_and_composition_is_shared (test_purpose_composition.CommandLineAndSchema) ... ok
test_validate_repository_warning_count_and_preserved_canonical_nodes (test_purpose_composition.CommandLineAndSchema) ... ok
test_allof_green_and_red (test_purpose_composition.GateTable) ... ok
test_anyof_green_and_red (test_purpose_composition.GateTable) ... ok
test_blocked_is_not_hidden_by_an_invalid_sequence_attempt (test_purpose_composition.GateTable) ... ok
test_blocked_is_preserved_for_every_kind_even_if_quorum_met (test_purpose_composition.GateTable) ... ok
test_firstof_cannot_resume_after_revoked_success (test_purpose_composition.GateTable) ... ok
test_firstof_green_and_red (test_purpose_composition.GateTable) ... ok
test_firstof_preference_order_stop_and_unknown_branch (test_purpose_composition.GateTable) ... ok
test_green_report_is_checked_at_report_time_not_using_future_evidence (test_purpose_composition.GateTable) ... ok
test_invariant_failure_cannot_be_bypassed_by_anyof_quorum (test_purpose_composition.GateTable) ... ok
test_invariant_green_and_red (test_purpose_composition.GateTable) ... ok
test_invariant_missing_or_misordered_measurements_and_unfinished_step (test_purpose_composition.GateTable) ... ok
test_invariant_over_firstof_checks_only_executed_alternatives (test_purpose_composition.GateTable) ... ok
test_malformed_input_is_rejected_without_traceback (test_purpose_composition.GateTable) ... ok
test_measurements_cannot_be_replaced_by_opinions_or_green_reports (test_purpose_composition.GateTable) ... ok
test_nested_sequence_checks_historical_composed_predecessor (test_purpose_composition.GateTable) ... ok
test_sequence_green_and_red_at_attempt_time (test_purpose_composition.GateTable) ... ok
test_sequence_revocation_equal_timestamp_missing_attempt_and_retry (test_purpose_composition.GateTable) ... ok
test_rule_1_non_leaf_requires_composition_warning_during_migration (test_purpose_composition.ValidationRules) ... ok
test_rule_2_sequence_order_unambiguous (test_purpose_composition.ValidationRules) ... ok
test_rule_3_anyof_threshold (test_purpose_composition.ValidationRules) ... ok
test_rule_4_green_firstof_requires_registered_branch (test_purpose_composition.ValidationRules) ... ok
test_rule_5_invariant_requires_over_inside_same_tree (test_purpose_composition.ValidationRules) ... ok
test_rule_6_green_report_must_follow_table_for_every_kind (test_purpose_composition.ValidationRules) ... ok

----------------------------------------------------------------------
Ran 29 tests in 0.662s

OK
```

### Isolert kopi uten øvrig arbeid i repoet

Det ble laget en midlertidig mappe med bare endrede verktøy, tester, data og
schemaer. Lærdomsregisteret ble hentet fra `git show
HEAD:Book/haven_lessons_register_v0.json`, slik at tester ikke var avhengige
av de usporede eller endrede leveransene rundt denne jobben.

Kommando i denne mappen:

```sh
/usr/bin/python3 -m unittest discover -s Tools/PurposePackages/tests -v
```

Siste linjer fra faktisk utdata (returkode 0):

```text

----------------------------------------------------------------------
Ran 29 tests in 1.714s

OK
```

`git diff --check` ga ingen utdata og returnerte 0. Tester kjører bare med
stdlib. Cowork-VM-en er ikke tilgjengelig i denne økten; en faktisk kjøring
der er derfor ikke målt.

## Slutninger fra kode og tester

- WP-1: KB og pakker bruker felles composition-schema. Ingen composition er
  satt inn i eksisterende noder, og ingen kombinator velges implisitt.
- WP-2: hver regel i Book 36 §5 har en navngitt test med godkjent og negativ
  variant. Regel 1 gir advarsel; regel 2–6 avviser. For regel 6 prøves alle fem
  kombinatorer. Grønne rapporter kontrolleres ved sitt eget `reportedAt`.
- WP-3: `sequence` kontrollerer forgjengerens tilstand før `attemptedAt`, også
  når forgjengeren er en samling. Et tidlig forsøk kan ikke bli grønt ved å
  legge til senere grønne målinger, og barnets egen grønne rapport avvises.
- WP-3: `firstOf` krever `branchRef`, følger `childOrder` og avviser nye forsøk
  etter første verifiserte suksess. Invariantmålinger er knyttet til hvert
  utført steg med `attemptRef` og `phase`, før og etter steget. Et registrert
  brudd kan ikke vaskes bort av en senere grønn måling eller omgås med `anyOf`.
- WP-3: samlet portstatus beregnes fra de øverste samlingene i oppgavens
  omfang. En ubrukt rød undersamling overstyrer ikke en grønn `anyOf` eller
  `firstOf`. Begge varianter er kjørt gjennom den faktiske CLI-en.
- WP-3: `blocked` beholdes med årsak, også ved oppfylt kvorum eller andre røde
  barn. Composition-porten gir returkode 2. Grønn/rød/ikke-verifisert gir
  henholdsvis 0/1/3. Valideringsfeil vises selv når porten er blokkert.
- Målinger, rapporterte slutninger og meninger har separate felter:
  `execution.measurements`, `execution.reports` og `execution.opinions`.
  Meninger og selvrapportert grønt erstatter ikke målinger. Utledet portstatus
  skrives i terminalen, ikke tilbake til målingsloggen.

Testene støtter at verktøyet følger Book 36 for de kontrollerte tilfellene.
De beviser ikke at en ekstern verifikator måler riktig egenskap, eller at
innrapporterte tider og observasjoner er sanne. CLI-en evaluerer en registrert
logg; den starter eller stopper ikke eksterne prosesser og gjør ingen rollback.
Eksisterende G1/G1-GUI/G2/G3 vises fortsatt som menneskelige portstatuser;
Composition-porten erstatter ingen menneskelig godkjenning.

## Meninger

Ingen mening brukes som grunnlag for godkjent verifikasjon i denne leveransen.
