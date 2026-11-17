# Production recovery coordination

```yaml
work_id: HD-0100
status: PREPARING
owner: Codex
integrator: Codex
host: 89.167.90.101
containers:
  - cellscaffold-app-1
  - cellscaffold-production-app-1
  - cellscaffold-admin-scaffold-1
  - admin-scaffold-production-app-1
mutation_type: tested immutable image deployment
baseline_web_revision: b4a2779a5122d56ecdd9c9475fe772790bfd180c
candidate_revision: pending_final_tests
registered_in_advance: true
```

The current user explicitly authorized integration, build/test and production
rollout overnight. This authorization supersedes older operator-only execution
notes. The coordinator owns mutations; auditors are read-only. Existing HD-0077
Palazzo container is outside this claim. No grants or staging administrator
provisioner invocation are part of this deployment.

Required chain: reviewed main with passing checks, immutable image publication,
prefetch, doctor/preflight, staging start and controlled restart, browser proof,
same-digest production rollout and restart, exact build/readiness and Butler
thread GUI acceptance. Preserve running data, identity continuity, secret-file
configuration, and verified rollback containers/receipts. No broad install or
legacy deployment shortcut.
