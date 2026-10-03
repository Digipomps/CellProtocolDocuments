Du er Codex-utfører for PDD «scaffold-administrator og delegering». Oppgavemappe (P): `CellProtocolDocuments/Deliverables/PDD_scaffold-admin-delegering_2026-09-08/` (relativt HAVEN-roten, som er cwd).

Les først `P/handoff/README.md` (felles regler, særlig 4, 6, 7, 8 og **10**), `P/PLAN.md` (WP1), `P/FORMAALSSPEC.md` §1 (`org-is-registered-administrator`), `P/contract/scaffold-administrator_v1.json` og `P/dataflow.md` (kantene K1–K6). Utfør **kun WP1 — administrator-registrering per scaffold**.

**Arbeidstre:** `CellScaffold/_wt-sad-20260909` — et eget git-worktree på branch `pdd/scaffold-admin-delegering`, opprettet fra `main` `e1f3e22f`. **Alt arbeid skjer der.** Det delte `CellScaffold/`-treet står på `pdd/tillitspakke-agentflaate` og skal ikke røres av denne jobben (`lesson.baseline-measured-another-pdds-branch`).

**Forhåndssjekk (regel 7), gjør denne først:**

    cd CellScaffold/_wt-sad-20260909 && git branch --show-current && git rev-parse --short HEAD && git status --porcelain | wc -l

Forventet: `pdd/scaffold-admin-delegering`, `e1f3e22f`, og et lavt antall skitne filer (0 ved start). Er branchen en annen: **stopp umiddelbart**, skriv én linje i `P/STATUS.md` og ikke rør en eneste fil.

**Les dette først — mønsteret finnes allerede.** Baselinen avdekket at delegering av et identitetsbundet, handlingsbegrenset bevis fra admin til ikke-admin allerede er implementert og virker: `CellScaffold/_wt-sad-20260909/Sources/App/Cells/Arendalsuka/ArendalsukaImportAccessCredentialSupport.swift`, med `proofs.index.byKeypath.<hash>`-indeksen i mottakerens egen EntityAnchor, og testene `ArendalsukaImportAuthorizationRoutesTests.testAdminDelegatesIdentityBoundCredentialToNonAdminImporter` og `ConferenceSurfaceRoutesTests.testArendalsukaImportActionSupportsAdminSessionAndRejectsMismatchedSignedProof`. Begge er røde i baselinen, men **ikke på autorisasjon** — de feiler på `Abort.500: Published Arendalsuka atlas is unavailable through the resolver`, et lag under. Autorisasjonen logger «authorized ... via accepted_vc» før den feilen.

Generaliser dette mønsteret. Ikke bygg en parallell mekanisme ved siden av. Det som mangler er organisasjonsleddet (utsteder er en entitet, ikke en person), tilbakekallet og terskelpolicyen.

**WP1 leverer:**

1. `ScaffoldAdministratorRegistry` som celle, med de tre get-nøklene og de tre set-nøklene i kontrakten. Registreringen er **per scaffold**; `administrator.transfer` er en egen handling med eget revisjonsspor, ikke en stille overskriving av `administrator.register` — den trengs når Arendalsuka/konferanser flyttes fra Digipomps til DiMy.
2. `administrator.state` skal kunne leses av enhver identitet og skal **ikke** inneholde noen personidentitet. Test at svaret bare navngir en organisasjonsentitet.
3. De to advarslene fra kontraktens `advisories`: `scaffold_administrator_not_provisioned` når registreringen mangler ved oppstart, og `scaffold_administrator_threshold_below_two` så lenge `requiredSignatures < 2`. Begge i `runtimeAdvisories`, begge skal navngi scaffoldet.
4. Terskelen er **registrert policy**, ikke en konstant. `administrator.thresholdPolicy.set` skal kunne heve den til 2 uten kodeendring. Sett startverdien til 1 med begrunnelse «utviklingsfase, styreleder alene» og dato.
5. Ingen kodesti der en adminrolle (`admin.observer/operator/nodeAgent/security`) gir myndighet her. Regel 10. Baselinen målte 48 forekomster av `requireAdminUser` og 33 av `AdminRoleProfile` i CellScaffolds `Sources` — de tallene skal ikke vokse som følge av WP1.

**Tester:** `test.admin.registry-read` fra kontrakten. Skriv dem slik at de går gjennom produksjonens egen kodevei, ikke en testhjelper (`lesson.tested-a-different-path-than-production`).

**Bygg og test:** legg **ikke** en full `swift test` inn i denne køjobben. Baselinen viste at `workspace-write` ikke får kjøre swift build/test for CellScaffold (`sandbox-exec: sandbox_apply: Operation not permitted`, `lesson.codex-workspace-write-cannot-build-cellscaffold`). Skriv koden og testene, kjør det du kan, og marker byggverifiseringen som `blocked` med den årsaken — den kjøres som eget detached skript.

**Leveranse:** kode + tester i CellScaffold, utdrag under `## Registerlesing <a id="registry"></a>` i `P/TESTRESULT.md`, én linje i `P/STATUS.md`, og sluttmelding `## WP1 — sluttmelding` nederst i `P/TESTRESULT.md` med hva som er ubygd og hva WP2 trenger.

Ingen git-operasjoner utover de to lesekommandoene. Ingen docker. Ingen deploy.
