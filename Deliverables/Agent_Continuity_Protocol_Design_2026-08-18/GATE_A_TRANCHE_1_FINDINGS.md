# Gate A tranche 1 — R01/R02-funn og C01-kontraktretning

**Arbeids-ID:** `agent-continuity-design-20260818`
**Tranche:** `gate-a-tranche-1`
**Beslutningseier:** Kjetil
**Observed at:** 2026-08-18, Europe/Oslo
**Status:** `TRANCHE_1_COMPLETE / READY_FOR_TRANCHE_REVIEW / NO_IMPLEMENTATION`

> Historisk tranchestatus. Kjetils nyere instruks 2026-09-10 åpnet en avgrenset
> Gate B-referanseimplementasjon. Se
> `GATE_B_IMPLEMENTATION_DECISION_2026-09-10.md`. Dette endrer ikke funnene om
> Candidate A, providerportabilitet, tokengevinst eller adoption.

## Brief audit

Kjetils beslutning åpner avgrenset forskning og kontraktkandidatarbeid. Den
beviser ikke at continuity-feil er hyppige, at et schema er bedre enn en kort
manuell standard, at alle providerflater kan bære samme semantikk, eller at en
automatisk evaluator er nødvendig. Tranche 1 undersøker derfor bare:

- `R01`: om repoet viser et konkret problem, gjenbrukbare baselines og et gap;
- `R02`: hva tre navngitte providerflater dokumentert kan representere,
  utføre og verifisere;
- `C01`: hvilken liten core/profile-retning funnene tillater uten schemafrys.

Funnklassene er `retrieved/verified`, `repo-observed`, `user-proposed`,
`inferred`, `contradicted` og `unavailable`. Providerpåstander er
versjonsavhengige og ble kontrollert mot offisielle kilder 2026-08-18. Ingen
innlogging, privat export, betalt kall, runtimeendring eller funksjonell
provider-test inngår. Dermed er «dokumentert capability» ikke det samme som
«testet end-to-end i Kjetils konto».

## Trancheresultat

| WP | Resultat | Konsekvens |
|---|---|---|
| R01 problem-fit | `NARROW / PREVALENCE_UNAVAILABLE` | Repoet viser reelle omission-, stale- og ephemeral-artifact-feil, men ikke frekvens eller skadeomfang som forsvarer en runtime. |
| R01 baseline | `CURRENT_MANUAL_PRACTICE_IS_INCUMBENT` | En versjonert, kort Markdown-standard er en foreslått baseline; dens sufficiency er uprøvd og den kan senere bli terminal løsning. |
| R02 capabilities | `SURFACE_SPECIFIC / PARTIAL` | Alle tre kan bære en menneskelesbar contract. Bare Codex/Claude Code med lokale repo-/filflater gir sterk maskinverifiserbar prosjektkontekst; ingen kilde viser felles automatisk authority/fold. |
| C01 boundary | `CANDIDATE_A_MUST_SPLIT` | Candidate A er ikke et vendor-nøytralt minimum. HAVEN, repository, delta/fold, health, provider og detailed evidence må ut av obligatorisk core. |
| Byggbeslutning | `NO_TECHNICAL_BUILD_NOW` | Ingen ny runtime, validator, evaluator, adapter eller schemafrys er evidensmessig begrunnet eller autorisert av tranche 1. Dette motbeviser ikke en liten semantic core som forskningshypotese. |

Sterkeste støttede retning er en liten **semantisk continuation-standard** med
Markdown som første carrier, og valgfrie profiler. JSON/schema må konkurrere
mot denne baselinen i senere autorisert forskning; det er ikke felles minimum
ennå.

## R01 — problem-fit, failure cases og gjenbruk

### Repo-observerte failure cases

| ID | Observasjon | Evidens | Vurdering |
|---|---|---|---|
| `R01-F01` | Repoet har allerede en eksplisitt kort durable handoff, men innholdet er manuelt og sist oppdatert 2026-06-12. | `Prompts/CurrentState.md:3-4,6-35,37-43,73-123,125-127` | `repo-observed`; viser både en brukbar baseline og stale-risiko. |
| `R01-F02` | CurrentState viser til en repo-lokal checkpoint-skill som ikke finnes i denne worktree-en. | `Prompts/CurrentState.md:67`; read-only `test -e .codex/skills/context-checkpointing/SKILL.md` → `not_found` 2026-08-18 | `repo-observed`; konkret reference-decay. |
| `R01-F03` | To kompakte handoffs dekker objective/current state/status, constraints, verification/open questions og next step, men er provider-/oppgavespesifikke og mangler felles freshness/base/receipt. | `Deliverables/Handover_To_ChatGPT_SmallModel_Research_2026-07-14.md:3-17,27-44`; `Deliverables/Codex_Handoff_E3b_Norwegian_LoRA_Adapter_2026-07-13.md:3-13,34-96` | `repo-observed`; dagens manuelle praksis har høy reuse-verdi. |
| `R01-F04` | En cross-model handoff peker til tre `/tmp`-artefaktmapper. Ingen av dem finnes nå. Dokumentet sier også at Claude Desktop ikke kunne lese de lokale stiene, slik at kontaktark måtte limes inn manuelt. | `Deliverables/Conference_Design_Handoff_2026-04-30.md:18-32,49-57,110-140`; tre read-only existence checks → `NOT_FOUND` 2026-08-18 | `repo-observed`; konkret ephemeral-artifact- og surface-boundary-feil. |
| `R01-F05` | Kontekstgraf-planen har relevante stale/elision/replay/token-gates, men status er «ikke påbegynt» og planen sier selv at grafen ikke automatisk er ground truth. | `Deliverables/Kontekstgraf_For_Kodeagenter_Plan_2026-08-09.md:3-6,12-21,92-111,178-225,266-294,334-358` | `repo-observed`; research/design precedent, ikke implementert continuity-mekanisme. |
| `R01-F06` | Targeted søk fant ingen eksisterende generell handoff-envelope med stable work ID, base revision, lifecycle receipt og provider-uavhengig compatibility policy. | `rg` over repoet etter handoff-/lifecycle-/revisionfelter 2026-08-18 | `NOT_FOUND_UNDER_CHECKS`; kan falsifiseres av en konkret oversett fil/symbol. |
| `R01-F07` | CellScaffolds varige `assistant_handoff.md` er 742 linjer, advarer selv om at historiske notater ikke gir autoritet, og blander superseded/resolved tilstand fra mange arbeidsspor. | `Documentation/Operations/assistant_handoff.md:1-15,326-373,736-742` i inspisert CellScaffold-worktree | `repo-observed`; full recap er en nyttig negativ baseline, ikke ønsket standard. |

### Hva repoet faktisk gjenbruker

1. **Manuell checkpointstruktur.** `Prompts/CONTRIBUTING.md:12-18` krever kort,
   strukturert og faktuell goal/files/decisions/next-step-oppdatering.
2. **Dokumentert goal/work/evidence-semantikk.** De tidligere inspiserte
   `GoalDefinition`, `WorkItemCell`, `ProjectPortfolioCell` og
   `DevelopmentStatusSnapshotProducerCore` gir nyttige domain-profiler og
   `available/stale/unavailable`-presedens, men ikke én komplett
   continuation-contract.
3. **Retrievalgrenser.** Book/RAG-kontraktene skiller canonical kilde fra
   derived retrieval og prompt-transformasjon. Det støtter resolve-or-stop,
   men gjør ikke graph/RAG til eier av prosjektstatus.
4. **Kontekstgraf-gater.** Planen krever budgeted retrieval, synlig elision,
   content hashes, stale-fail og deterministisk replay. Dette er mulige senere
   profiler, ikke nødvendige core-felter.

### Problem-fit og baselines

| Alternativ | Hva det dekker nå | Gap/risiko | Trancheverdict |
|---|---|---|---|
| `MANUAL_STANDARD` | Foreslått versjonert Markdown med captured time, objective/done-when, current situation, constraints/decisions, next/stop, risks og verification routes. | Sufficiency er uprøvd; ingen automatisk schema/CAS/replay og avhenger av receiver-verifikasjon. | Foreslått baseline; test før den kalles løsning. |
| `CURRENT_REPO_PRACTICE` | CurrentState og oppgavespesifikke handoffs finnes allerede. | Ulik struktur, stale refs, `/tmp`, ingen uttrykkelig non-authority. | Tilpass til manual standard. |
| `PROVIDER_NATIVE` | Projects, Codex worktree/internal handoff/import og Claude sessions/resume kan hjelpe innen hver flate. | Ulik semantikk, account/plan/version drift, ingen felles authority/fold. | Bruk der dokumentert; ikke kall det protokollequivalent. |
| `CANDIDATE_A_JSON` | Representerer hele HAVEN/repo/delta/health-ambisjonen i én fil. | For tung og domainbundet som core; self-reported verification/authority. | Rebutted som minimum. |
| `SMALL_CORE_PLUS_PROFILES` | Kan standardisere continuation uten å gjøre runtime-/domainfelt universelle. | Verdi over manual carrier er ikke målt; krever senere ablation/portability. | Forskningskandidat, ikke build. |
| `RUNTIME_AUTOMATION` | Kan senere validere/fold/evaluere. | Problemfrekvens, safety, cost og portability er ikke påvist. | `NO_TECHNICAL_BUILD_NOW`. |

R01 viser **at feiltypen finnes**, men ikke prevalence, kausal skade eller
netto nytte av automatikk. En eneste manglende `/tmp`-pakke rettferdiggjør en
bedre artifactregel; den rettferdiggjør ikke alene graph, evaluator eller
delta-runtime.

## R02 — capability- og enforceability-matrise

Kategorier:

- `R`: representable i flaten;
- `U`: dokumentert user-executable operasjon;
- `M`: maskinverifiserbar fra tilgjengelig lokal struktur/metadata;
- `E`: flaten dokumenterer håndheving av akkurat invariantet;
- `X`: unsupported eller ikke dokumentert for den avgrensede profilen;
- `?`: unavailable i denne read-only tranchen.

| Capability | `surface.chatgpt.projects.manual-file` | `surface.codex.desktop.local-worktree` | `surface.claude-code.cli.local` |
|---|---|---|---|
| Bære objective/state/constraints/next action som tekst/fil | `R/U`; prosjektfiler, sources og lagrede svar | `R/U/M`; workspacefil kan leses og versjoneres | `R/U/M`; workspacefil/CLAUDE.md kan leses og versjoneres |
| Vedvarende prosjektinstruksjon | `R/U`; project instructions, overstyrer global instructions innen prosjektet | `R/U`; AGENTS-kjede lastes før arbeid, med dokumentert scope/precedence/size limit | `R/U`; CLAUDE.md/rules lastes etter dokumentert scope; behandles som context, ikke sikkerhetspolicy |
| Native gjenopptakelse innen samme provider | Project chats og project memory kan gi kontinuitet; memory er retrieval, ikke listbar canonical state | Local↔Worktree Handoff beholder chat/worktree-assosiasjon; dette er Codex-intern flytting | Sessions lagres lokalt; `--continue`, `--resume`, branch og `/export` er dokumentert |
| Context pressure/compaction-signal | `R/U` betinget på desktop; `/status` viser context usage og `/compact` finnes, men web/desktop er ikke én lik capability | `R/U`; desktop `/status` viser context usage og `/compact` finnes; ingen maskinlesbar per-task-måling dokumentert | `R/U/M`; `/context` og status-line JSON gir faktisk forbruk, `/compact` erstatter historikk med sammendrag |
| Canonical revision/digest/CAS | `X`; ingen slik project-source-kontrakt dokumentert | `M` for Git-/filrevisjon; `X` for en generell project-state CAS/fold | `M` for Git-/filrevisjon og lokale transcripts; `X` for generell canonical fold |
| Contract schema/invariant enforcement | `X`; prosjektinstruksjon og memory er ikke schema-validator | Mulig senere lokal validator, men ingen er bygget/autorisert her; AGENTS er instruksjon | Mulig senere lokal validator, men ingen er bygget/autorisert her; CLAUDE.md er context |
| Native cross-vendor import | `X` i manual-file-profilen; adjacent desktop-import finnes | OpenAI dokumenterer inbound import fra Claude Code/Cowork/Cursor; mapping er ikke testet som continuation-contract | Anthropic dokumenterer `/import codex` av lokale konfigurasjonstyper fra v2.1.213; one-shot, ikke session-/state-roundtrip |
| Authority/approval transfer | `X`; fil/chat skaper ikke write authority | `X`; import, memory, AGENTS eller worktree-handoff er ikke canonical approval receipt | `X`; session/export/CLAUDE.md er ikke external approval receipt |
| Structured usage/cost output | `X/?` for denne profilen | `?`; ikke verifisert i denne surface-auditen | `U/M` for non-interactive run: dokumentert structured JSON med usage/cost |
| Transport bytes/Git verifiability | `X` for uploaded project state | `M` for lokal fil, hash, HEAD og dirty state | `M` for lokal fil/transcript path, hash, HEAD og dirty state |
| Semantic continuation verified | `X`; ingen native contract-orakel | `X`; Git/importstatus beviser ikke mening, freshness eller instruction adherence | `X`; transcript/importstatus beviser ikke summary fidelity, authority eller next action |

### Primærkildefunn og negative grenser

**ChatGPT Projects.** OpenAI dokumenterer prosjektfiler, project instructions,
project sources, flytting av chats og project memory. Et ChatGPT-prosjekt gir
ikke direkte lokal mappetilgang; sources må lastes opp eller kobles. Project
memory kan ikke inspiseres som en liste, og tilgjengelighet/retensjon/limits
avhenger av konto, plan og workspace. Desktopappen dokumenterer `/status` med
chat-ID, context usage og rate limits, samt `/compact`, men kommandoer varierer
med environment/access. Gate A-profilen bør derfor senere splittes i web og
desktop. Dette er retrieval-/workspace-/observability-capabilities, ikke
dokumentert revisjonert canonical state eller felles continuation-protokoll.

**Codex.** OpenAI dokumenterer AGENTS-discovery, separate lokale Codex-memories,
Codex-intern Local↔Worktree Handoff og import fra Claude Code/Cursor. Importen
kan mappe instructions, project folders, Claude project memories og nylige
chats, men kilden krever eksplisitt review av blant annet permissions, hooks og
connections etter import. Tranche 1 testet ikke mapping, roundtrip, semantic
loss eller automatic-update-adferd. Den inbound kanten og optional
automatic-update-moden er `retrieved/verified` som dokumentert
produktcapability for de navngitte dataklassene. Faktisk update-adferd i
Kjetils build/konto, semantic fidelity, roundtrip og protocol portability er
fortsatt `unavailable`.

Lokal Codex-memory er generated background state, kan oppdateres sent eller
hoppe over en pass nær rate limit, og er av som default. OpenAI sier at
obligatorisk team guidance skal ligge i AGENTS/checked-in docs. Memory kan
derfor ikke være canonical current state.

**Claude Code CLI.** Anthropic dokumenterer lokale sessions/transcripts,
resume/branch, `/export`, `/context` og `/compact`. `/context` gir denne profilen
et ekte observerbart context-pressure-signal. Claude Code v2.1.213+ dokumenterer
også `/import codex|gemini`, som kan ta med instruction files, MCP servers,
commands, subagents og skills. Kommandoen er versjons-/provideravhengig, er en
engangsimport og dokumenterer ikke chats, project state, continuous sync eller
semantic roundtrip. Contextguiden dokumenterer dessuten at deler av message
history oppsummeres bort og at ulike instructionmekanismer reloades forskjellig.
CLAUDE.md/auto memory kan støtte continuity, men er ikke external authority
eller canonical fold.

Cross-vendor capability må derfor modelleres som en **rettet kant per
dataklasse og operasjon**—for eksempel `claude-code -> codex : recent-chats`
eller `codex -> claude-code : instruction-files`—med mode (`one-shot` eller
`sync`) og surface/version. Candidate As ene bool
`automaticCrossVendorTransfer` kan verken uttrykke asymmetrien eller skille
konfigurasjon fra continuation state.

### Drift og revalidering

Capability records må senere minst bindes til `surfaceProfile`, client/version
der kjent, `observedAt`, official source, account/plan dependency,
`lastVerified` og revalidation trigger. En dokumentendring, endret importmapping,
plan-/workspacebegrensning eller manglende kommando skal sette capability til
`unknown/unavailable`; adapteren må ikke simulere den.

Skjulte avhengigheter i kildene omfatter at Codex worktrees krever desktop,
Codex mode og Git; OpenAI-import kan være rollout-/buildavhengig; Codex memory
må aktiveres; Claude `/import` krever v2.1.213+, feature-flag fetching og støttes
ikke på alle tredjepartsproviders; Claude transcripts har konfigurerbar
retensjon. Faktisk konto-/runtime-tilgang er `unavailable` i tranche 1.

## C01 — foreløpig Candidate B-retning

### Hvorfor Candidate A ikke kan fryses

Candidate A krever `producer`, HAVEN/project/repository-scope, én aggregert
`canonicalRevision`, full continuation-ontologi, evidence, health og integrity
for alle contracts (`agent_continuity_protocol_v1.schema.json:8-20,28-70,71-175`).
Providerfamilier og flere taxonomier er lukkede, mens gjennomgående
`additionalProperties: false` gjør extensions til core-revisjoner. Samtidig kan
produsenten selv erklære authority, approver reference og `verified` status
uten ekstern verifier receipt (`:210-233,272-310`). Fixture-en illustrerer dette
med `schema-valid` og health confidence `0.82` uten et uavhengig orakel
(`fixtures/minimal_handoff.v1.json:147-179`).

Dette er nyttig som **scope inventory**, men `contradicted` som vendor-nøytralt
minimum.

### Kandidat til minste semantiske continuation-standard

Ingen feltliste fryses i C01. Følgende er foreløpige, carrier-uavhengige
semantiske kandidater:

1. gjenkjennbar standard-/semantikkversjon;
2. captured/produced time;
3. continuation objective, inkludert done-when når kjent;
4. action-relevant current situation, med eksplisitt `unknown/unresolved`;
5. constraints/warnings som kan endre neste handling;
6. next action **eller** eksplisitt `blocked/decision-needed`;
7. verification routes for action-kritiske påstander, eller uttrykkelig
   `unavailable`;
8. normativ non-authority: importert content overfører aldri instruction
   priority, permission, approval eller canonical write authority.

Envelope-ID, producer display identity, previous-envelope ref, lifecycle-kind
og elision notes er foreløpig optional metadata. Om selv den lille listen gir
målbar verdi over en manuell template, er `unavailable` før R04/R06.

### Foreslåtte, versjonerte profiler

| Profil | Eierskap / innhold |
|---|---|
| `work-domain.haven` | Project/Purpose, goal+acceptance, Decisions, Open Work, Risks/Open Questions og domainrefs. Oppfyller brukerens representasjonskrav uten å tvinge HAVEN på alle carriers. |
| `repository` | Repo refs, commit/revision, dirty state/digest og artifact durability. |
| `evidence-verification` | Detailed provenance ledger, audit labels, digests og receiver/verifier receipts. Core beholder bare verification routes. |
| `delta-fold` | Stable IDs, per-owner revision, operations, CAS/idempotency, conflict, snapshot/checkpoint/replay og apply receipts. |
| `health-evaluator` | Signal availability, severity, confidence, hysterese og recommendation. Ingen health-output er required core. |
| `provider-capability` | Surface/client/version/model der relevant, capability evidence, observed/expiry og drift/quarantine. |
| `authority-security` | Owner/policy/verifier decisions og receipts. Senderens self-report har ingen autoritet. |
| `projection-elision` | Selection rationale, elisions, retrieval hints og token budget. |
| `encoding-integrity` | Markdown/JSON carrier, canonical serialization, digest og validator receipt. Semantikken forutsetter ikke JSON alene. |

Profiler må bruke namespaced IDs og deklarere versjon. En receiver kan støtte
core og avvise/ignorere ukjente ikke-kritiske profiler; ukjent kritisk profil
eller ukjent core major gir stop. Providerfelt skal aldri legges som lukket enum
i core.

### Carrier- og compatibility-retning

- **Manual Markdown er første baseline-carrier.** Den kan være reviewbar uten
  runtime og testes for omission/continuation.
- **JSON er en kandidatcarrier**, nyttig først når maskinell validering eller
  profiler gir påvist verdi.
- Semantisk equivalence mellom carriers må senere ha deterministiske testcases
  der det går og menneske-/modelgrader bare for uunngåelig myk semantikk.
- `verified`, `approved`, `current` og capability confidence får ingen effekt
  fordi senderen skriver dem. Receiver-policy må løse refs og innhente riktig
  receipt/freshness-resultat.

## Claim ledger

| Claim | Klasse | Status etter tranche 1 | Falsifikator / neste evidens |
|---|---|---|---|
| Thread/chat er working context, ikke durable ground truth. | architecture | `supported_with_scope` | En surface med dokumentert, revisjonert canonical ownership og conflict policy for chat state. Ingen funnet. |
| Canonical project state er durable ground truth. | architecture | `too_strong / contradicted` | Repoet viser flere felteiere og stale manual state. Autoritet må være field-/owner-/revision-spesifikk, ikke én global «project state». |
| Graph=relasjoner, RAG=semantikk, thread=ny kontekst. | taxonomy | `inferred / too_coarse` | Eksisterende graph-plan omfatter episodisk state/retrieval; RAG har provenance/citations; fersk thread kan være feil. Bruk capability/authority/freshness, ikke lagtype alene. |
| Delta er mer tokenøkonomisk enn full recap. | efficiency | `unavailable` | Krever autorisert paired cost/eval, inkludert fold/refetch/recovery og cache. |
| Projection skal bare inneholde action-relevant info. | design principle | `supported_as_principle` | Krever senere field ablation; «kan endre handling/tolkning» er ennå ikke et reproduserbart orakel. |
| Health bør baseres på observerbar degradering, ikke én maxlengde. | evaluation | `supported_as_direction` | Claude har `/context`, de andre profiler mangler verifisert capacity. Effekt over simple baselines er ikke testet. |
| Minimal handoff er continuation contract, ikke historisk recap. | design principle | `supported_by_repo_patterns` | Manual baseline må senere testes mot omissions/retention og full recap. |
| Én vendor-neutral core med små adaptere er mulig. | portability | `plausible_but_unverified` | Core faller hvis en surface må fabrikere felt eller originating chat fortsatt trengs. Candidate A oppfyller ikke hypotesen. |
| Validert JSON er felles minimum. | transport | `contradicted` | ChatGPT manual-file og eksisterende repo-baseline kan bære semantikken som Markdown; schemaets merverdi er ikke vist. |

## Sources/evidence ledger

### Search coverage og verifiserte revisjoner

- `CellProtocolDocuments`: denne worktree-en, detached HEAD
  `b659129df27978049fd12d8b7b3b989686a9bc0c`. Targeted scan omfattet
  `Prompts/{CurrentState,CONTRIBUTING,Architecture,CoreContext,SystemPrompt-Codex}.md`,
  de tre handoff-/handoverfilene nevnt i R01-F03/F04,
  `Deliverables/Kontekstgraf_For_Kodeagenter_Plan_2026-08-09.md`,
  `Tools/HavenDocsMCP/README.md`, `Tools/RAGPromptTransformer/README.md` og
  denne seksfilspakken. Søkeordfamiliene dekket continuity, handoff,
  checkpoint, current state, resume, projection, snapshot, import/export,
  revision, replay og context graph.
- `CellScaffold`: read-only worktree
  `/Users/kjetil/.codex/worktrees/37c2/CellScaffold`, clean detached HEAD
  `c45a468faf53632ecd203752cf4fbf0b9f0a3738`. Targeted inspeksjon:
  `AGENTS.md`, `Documentation/Operations/assistant_handoff.md`,
  `Documentation/Claude_Skills_and_Codex_Collaboration.md`,
  `memory/context-ledger.md`, `Sources/App/Cells/WorkItems/{WorkItemCell,ProjectPortfolioCell}.swift`,
  `Sources/DevelopmentStatusSnapshotProducerCore/DevelopmentStatusSnapshotProducerCore.swift`,
  `Sources/App/Cells/Graph/GraphStoreCell.swift` og
  `Sources/App/Cells/RAG/RAGGatewayCell.swift`.
- `CellProtocol`: read-only worktree
  `/Users/kjetil/.codex/worktrees/a027/CellProtocol`, detached HEAD
  `79740304167aa4f4daadd148c5a369e919d25a6a`. Targeted inspeksjon:
  `Sources/CellBase/PurposeAndInterest/{GoalDefinition,Purpose}.swift` og
  `Sources/CellBase/Cells/Vault/GraphIndexCell.swift`. En pre-eksisterende
  untracked threat-model-fil ble bevart og ikke åpnet.

Dette er en bounded targeted audit, ikke bevis for repo-wide fravær. Tidligere
designrapportobservasjoner mot andre worktree-revisjoner beholdes som historisk
evidens og må ikke leses som revalidert teststatus for revisjonene over.

### Repo- og artifactkilder

| Evidence ID | Kilde / område | Status | Bruk |
|---|---|---|---|
| `E-R01-current-state` | `Prompts/CurrentState.md`; `Prompts/CONTRIBUTING.md` | `repo-observed` 2026-08-18 | Manual durable checkpoint, stale/ref-decay og formatbaseline. |
| `E-R01-handoffs` | De tre handofffilene i R01-F03/F04 | `repo-observed` 2026-08-18 | Concrete completeness og ephemeral cross-surface failure. |
| `E-R01-context-graph` | `Deliverables/Kontekstgraf_For_Kodeagenter_Plan_2026-08-09.md` | `repo-observed`; status not started | Reuse for future profile/gates, ikke implementation proof. |
| `E-C01-schema` | Candidate A-schema og illustrative fixture | `repo-observed` | Boundary critique; ingen normative semantics. |
| `E-Gate-A` | `GATE_A_DECISION_2026-08-18.md` | `retrieved/verified` som lokal decision record | Scope/stop; autoriserer ikke senere WP-er. |

### Offisielle providerkilder

Alle ble lest 2026-08-18; capabilitystatus utløper ved relevant
dokument-/produktendring.

- [OpenAI: Projects in ChatGPT](https://help.openai.com/en/articles/10169521-projects-in-chatgpt)
  — project files/instructions/sources, chat move, memory og plan/workspace-
  avhengigheter.
- [OpenAI: ChatGPT Work and Codex](https://help.openai.com/en/articles/20001275-chatgpt-work-and-codex)
  — Codex har separat view/history fra ChatGPT history.
- [OpenAI: Projects and chats](https://learn.chatgpt.com/docs/projects)
  — ChatGPT-vs-local projects, sources, folder boundary og resume via local
  project directory.
- [OpenAI: desktop slash commands](https://learn.chatgpt.com/docs/reference/slash-commands)
  — betinget `/status`, `/compact`, `/worktree` og command availability.
- [OpenAI: AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
  — Codex instruction discovery, precedence og size boundary.
- [OpenAI: Memories](https://learn.chatgpt.com/docs/customization/memories)
  — separat local Codex memory, generated/late/optional, og checked-in guidance
  som riktig sted for obligatoriske regler.
- [OpenAI: Worktrees](https://learn.chatgpt.com/docs/environments/git-worktrees)
  — Codex Local↔Worktree Handoff og Git-/ignored-filegrenser.
- [OpenAI: Import from another agent](https://learn.chatgpt.com/docs/import)
  — dokumentert Claude Code/Cursor-import og reviewbehov; ikke roundtripbevis.
- [Anthropic: Manage sessions](https://code.claude.com/docs/en/sessions)
  — local transcripts, resume/branch/export/context og structured run output.
- [Anthropic: Commands](https://code.claude.com/docs/en/commands)
  — `/import codex|gemini`, dataklasser, version og providerbegrensninger.
- [Anthropic: Context window](https://code.claude.com/docs/en/context-window)
  — live `/context`, compaction og reloadgrenser.
- [Anthropic: Status line](https://code.claude.com/docs/en/statusline)
  — maskinlesbar session/model/context/workspace-observability.
- [Anthropic: `.claude` directory](https://code.claude.com/docs/en/claude-directory)
  — lokale dataklasser, retention og plaintext/transcriptgrenser.
- [Anthropic: Memory/CLAUDE.md](https://code.claude.com/docs/en/memory)
  — persistent instructions/auto memory og negative authoritygrense.

## Rådgiverledger og challenged review

| Rolle | Første verdict | Integrasjon |
|---|---|---|
| C01 skeptic | Candidate A er et HAVEN/repository/evaluator-komposittschema, ikke genuin core. Dagens manuelle praksis er incumbent; en versjonert standard er en troverdig, uprøvd baseline. | Profile-splitt, carrier-separasjon, non-authority og avgrenset no-build er integrert. |
| R01 source analyst | `MANUAL_PRACTICE / PREVALENCE_UNAVAILABLE / NO_RUNTIME` | Repoets baselines, konkrete failure cases og no-code reuse er integrert. |
| R02 surface analyst | `PARTIAL_DIRECTIONAL_CAPABILITIES / NO_COMMON_FOLD` | Matrix, hidden dependencies og directional transfer-semantikk er integrert. |
| challenged adjudicator | `NEEDS_ONE_BOUNDED_CORRECTION`; hardeste verdict `STANDS` | Skillet incumbent praksis/proposed standard, avgrenset no-build og verified-vs-tested auto updates er korrigert. |

## Stop/go og neste beslutningspunkt

Tranche 1 anbefaler ikke Gate B-pass. Den leverer et smalere grunnlag for en ny
Kjetil-beslutning:

1. behold dagens manuelle praksis som incumbent og den versjonerte
   `MANUAL_STANDARD` som uprøvd baseline; la `NO_BUILD` for teknisk mekanisme
   forbli default;
2. avgjør om en senere tranche skal åpne **R03/R04** for corpus/field-ablation
   og en faktisk manual-vs-small-core-test;
3. åpne ikke portability, token-cost, health, delta/fold eller implementation
   før de navngitte avhengighetene er godkjent;
4. ingen Book-promotering, schemafrys, skill-sync eller providerimport følger av
   dette funnet.

**Tranchestatus:** `READY_FOR_TRANCHE_REVIEW`, aldri `READY_FOR_ADOPTION`.
