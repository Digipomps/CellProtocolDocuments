# Utviklingsplattform på Hetzner styrt fra Co-Pilot Chat — plan

Dato: 2026-06-11. Status: **v2 — revidert etter Kjetils beslutninger samme dag.**

Beslutninger som ligger til grunn (Kjetil, 2026-06-11):
- GitHub skal uansett støttes og forblir primær git-hosting. Forgejo brukes ikke som tjeneste, men issue-/kanban-modellen der kan være inspirasjon for native celler (Forgejo er open source: non-profit-styrt Gitea-fork under Codeberg e.V., GPLv3+).
- Hovedregel: alltid native HAVEN-celler. Egne integrasjonsceller mot eksterne tjenester (GitHub) er OK.
- Agent-runner skal planlegges, men tas ikke i bruk med en gang.

## 1. Mål

Hele utviklingsløpet — kode, prosjektstyring, bygg/kompilering, deploy og drift — styres fra Co-Pilot Chat (Chat Workbench, Book 19) som sentralvindu. Kompilering og kjøring skjer på egen Hetzner-infrastruktur; GitHub forblir kodevert. Chatten foreslår, brukeren bekrefter, cellene utfører. Non-negotiables fra Book 19 gjelder hele veien: *recommendation ≠ invocation* og *ingen skjulte side effects*.

## 2. Nå-situasjon (kartlagt 2026-06-11)

- Hetzner-server finnes: `ops@89.167.90.101` (nøkkel `~/.ssh/id_ed25519_hetzner`). Kjører CellScaffold-staging via docker compose. Bygging skjer **på serveren** (git pull + `docker compose build`), helsesjekk `/health/build` på :8081.
- Dockerfiler finnes for CellScaffold, SpatialRegistryScaffold og DiMyMicropayments. Deploy-skript i `CellScaffold/scripts/deploy-staging.sh`, `SpatialRegistryScaffold/Scripts/deploy-staging.sh` og `DiMyMint/scripts/deploy-cellscaffold-staging.sh`.
- Kode hostes på GitHub.
- Swift 6.1 på Linux er bevist i drift (`swift:6.1-noble`-image), med BUILDKIT cache-mount-namespacing per bygg.
- Co-Pilot Chat: `PersonalChatHubCell` har allerede surface-aksjoner (`ui.openComponentSurface`/`minimize`/`pin`); matching-pipeline og GroundedActionPlan-verifisering finnes.
- Begrensning: Binding (macOS/SwiftUI) kan **ikke** kompileres på Hetzner — Hetzner tilbyr ikke macOS. Mac-en forblir byggmaskin for macOS-targets.

## 3. Målarkitektur

**GitHub (primær):** git-hosting, PR-er, code review, GitHub Actions som CI-orkestrator.

**Hetzner:**
1. **Bygg-node (ny):** self-hosted GitHub Actions-runner i Docker med Swift-buildcache, pluss privat container registry (registry:2 bak Caddy/TLS med auth). Senere også agent-runner (fase 5, parkert).
2. **Staging-node (dagens server):** slutter å bygge selv; trekker ferdigbygde images fra registryet og kjører `docker compose pull && up -d` + helsesjekk.

**Lokal Mac (valgfritt):** registreres som self-hosted runner med label `macos` for Binding/Xcode-bygg.

**Cellelaget — to klart adskilte roller:**

*Native HAVEN-celler (system of record for prosjektstyring):*

| Celle | Ansvar |
|---|---|
| ProjectCell | prosjekt/milepæler/mål — canonical state i HAVEN |
| IssueCell | én arbeidsoppgave med tilstandsflyt (idé → pågår → ferdig) |
| BoardCell | kanban-flate over IssueCells (komponentflate i chat) |

Datamodellen kan låne fra Forgejo/Gitea sine issue-/board-skjemaer, men staten bor i HAVEN som cell-state (konfigurerbart per bruker, ikke app-innstillinger — i tråd med Chat Workbench-prinsippene).

*Integrasjonsceller (wrappere mot eksterne API-er):*

| Celle | Ansvar |
|---|---|
| GitHubRepoCell | repo-status, branches, PR-er (GitHub API) |
| GitHubSyncCell | toveis kobling IssueCell ↔ GitHub Issues der ønsket; PR-status inn på BoardCell |
| BuildCell | byggstatus, trigge workflows, hente logger (Actions API) |
| DeployCell | promotere image til staging/prod via workflow_dispatch, helsesjekk |
| AgentTaskCell | kontrakt for å delegere kodeoppgave til agent-runner (fase 5, parkert) |

Flatenivåer per Book 19: inline-svar for status («bygget er grønt»), kort for bygg/issues/PR-er, komponentflate for kanban-tavle og logger.

## 4. Komponentvalg

| Behov | Anbefaling | Alternativ |
|---|---|---|
| Git-hosting + PR + review | **GitHub (beholdes som i dag)** | — |
| Prosjektstyring | **Native HAVEN-celler** (ProjectCell/IssueCell/BoardCell), GitHubSyncCell for kobling | GitHub Projects via integrasjonscelle (raskere, men bryter native-regelen) |
| CI-orkestrering | GitHub Actions | — |
| Kompilering | Self-hosted runner på Hetzner bygg-node | GitHub-hosted runners (dyrere ved Swift-byggetider, ingen lokal cache) |
| Container registry | registry:2 på bygg-noden, bak Caddy/TLS med auth | GHCR (mindre drift, men images bor utenfor Hetzner og pulls går over egress) |
| Deploy-mekanisme | Dagens compose-oppsett, trigget fra Actions-workflow | Coolify/Dokploy hvis mer UI ønskes |
| Agent-runner (parkert) | Claude Code headless / Claude Agent SDK i container | `codex exec` |
| TLS/ingress | Caddy | Traefik |
| Secrets | GitHub Actions secrets + sops/age for filer | Vault (overkill nå) |
| Overvåkning | Uptime Kuma + Netdata, alerts inn i chat | Grafana-stack senere |

## 5. Faser

### Fase 0 — Inventar (½ dag)
- Kartlegg alle repoer som skal ha CI, og alle secrets i dagens deploy-løype.
- Avklar siste åpne punkt i §9 (registry-plassering).

### Fase 1 — Bygg-node (1–2 dager)
- Ny VM (CPX41), Caddy + TLS, privat registry, self-hosted GitHub Actions-runner i Docker.
- Backup: registry-data og runner-konfig til Hetzner Storage Box + VM-snapshots; restore-test før fasen lukkes.

### Fase 2 — CI/kompilering (ca. 1 uke)
- Actions-workflow per repo: test → `docker build` → push til registry. Gjenbruk cache-namespacing-logikken fra `deploy-staging.sh`; persistent buildcache-volum på runneren.
- (Valgfritt) Mac registreres som `macos`-runner for Binding-bygg.

### Fase 3 — Deploy fra CI (2–3 dager)
- Staging-noden slutter å bygge: CI pusher image tagget `staging-<sha>`, deploy-workflow kjører `docker compose pull && up -d` over SSH + `/health/build`-sjekk. Logikken finnes i deploy-skriptene og flyttes inn i workflow.
- Promote-to-prod blir egen manuell workflow_dispatch-jobb senere.

### Fase 4a — Chat-styring: integrasjonsceller (ca. 1 uke, kan starte parallelt med fase 2)
- GitHubRepoCell, BuildCell og DeployCell som wrappere rundt GitHub API/Actions API.
- Purpose/Interest-oppføringer slik at matching-pipelinen ruter «hva er byggstatus?», «deploy staging», «vis PR-ene» riktig. Testes med prompt-matrisene (haven-prompt-purpose-testing).
- Håndhev Book 19: chat genererer GroundedActionPlan → bruker bekrefter → celle utfører; alle side effects synlige som flow.
- Grants/capabilities: muterende aksjoner (deploy, trigge bygg) krever eksplisitt grant; lesestatus er fri.

### Fase 4b — Chat-styring: native prosjektstyring (1–2 uker)
- ProjectCell/IssueCell/BoardCell som native celler — canonical state i HAVEN, datamodell inspirert av Forgejo/Gitea.
- BoardCell som komponentflate i Chat Workbench; IssueCell som kort; opprett/flytt issue fra chat med bekreftelsessteg.
- GitHubSyncCell kobler IssueCell ↔ GitHub Issues/PR-status der det gir verdi (valgfritt per prosjekt).
- Følg eksisterende skill-løyper: cellprotocol-cell-authoring for cellene, cellconfiguration-skeleton-authoring for flatene.

### Fase 5 — Agent-runner (planlagt, **parkert**)
- Design nå, bygg senere: AgentTaskCell-kontrakten defineres i fase 4a (slik at chat-rutingen er klar), men ingen runner deployes.
- Når den aktiveres: container på bygg-noden med Claude Code headless (eller Agent SDK), egen worktree per oppgave, resultat som feature-branch + PR på GitHub. Agenten får **aldri** deploy-rettigheter — kun branch + PR. Mennesket merger.

### Fase 6 — Herding og drift (løpende)
- Uptime Kuma + Netdata; alerts surfaces som kort i chat (egen celle som leser varsler).
- SSH-hardening (kun nøkler, fail2ban), secrets-rotasjon, ukentlig restore-test.

## 6. Sikkerhet

- **Self-hosted runners kun på private repoer** (eller med påkrevd godkjenning av workflows fra forks) — fork-PR-er kan ellers kjøre vilkårlig kode på bygg-noden. Dette er den viktigste enkeltregelen i oppsettet.
- Registry bak TLS med auth; SSH kun med nøkler.
- CI-secrets bor i GitHub Actions secrets — aldri i chatten. DeployCell viser *hva* som gjøres, aldri hemmeligheter.
- HAVEN capabilities/grants avgjør hvem som kan trigge hva fra chat; bekreftelsessteg er obligatorisk for alt muterende.
- Agent-runner (når den kommer): sandboxed, egen bruker, ingen prod-nøkler, kun git-tilgang til egne branches.

## 7. Risikoer og avbøtninger

| Risiko | Avbøtning |
|---|---|
| Swift-byggetider på CI | Persistent cache-volum på runneren (mønsteret finnes); dedikert AX-server ved behov |
| macOS-gap: Binding kan ikke bygges i skyen | Mac som `macos`-runner, eller fortsatt manuelt lokalt |
| Self-hosted runner eksponert for fremmed kode | Kun private repoer / krev workflow-godkjenning (se §6) |
| Native PM-celler tar tid før de er nyttige | Fase 4a (integrasjonsceller) gir chat-styring tidlig; 4b kan modnes i eget tempo |
| Chat-feilrouting trigger feil handling | GroundedActionPlan-verifisering + bekreftelse før muterende aksjoner (Book 19) |
| GitHub nede stopper deploy | Staging kjører videre på sist pullede image; registry og images bor på Hetzner |

## 8. Kostnad (ca., eks. mva)

- Bygg-node CPX41: ~€30/mnd (dedikert AX42 ~€46/mnd hvis Swift-byggetid krever det)
- Storage Box 1 TB: ~€4/mnd
- Staging-node: uendret
- GitHub: gratis Actions-minutter brukes ikke av self-hosted runners (ubegrenset på egne runnere)

**Nytt totalt: ca. €35/mnd.**

## 9. Avklart / gjenstående

Avklart 2026-06-11:
1. ~~Forgejo vs GitHub~~ → **GitHub primær**; Forgejo kun som datamodell-inspirasjon for native celler.
2. ~~Wrapper vs native PM~~ → **Native HAVEN-celler er hovedregel**; integrasjonsceller mot GitHub er OK.
3. ~~Agent-runner~~ → **Planlegges (kontrakt i fase 4a), bygges/aktiveres ikke nå.**

Gjenstår:
4. Registry på bygg-noden (anbefalt) vs GHCR — avgjøres i fase 0.
5. Egen bygg-node CPX41 fra start (anbefalt) vs midlertidig bygging på staging-noden.
