# Opprydding av grener og arbeidstrær – 2026-09-18

Utført etter Kjetils avgrensning: bare lokale grener med bevist ancestry til ferskt hentet `origin/main` og godkjent sletting med `git branch -d`.

Måleperiode: 2026-09-18 09:39:01 CEST – 2026-09-18 09:45:49 CEST.
Antall før og etter er målt rundt oppryddingen i hvert enkelt repo.

## Resultat

| Repo | Lokale før | Lokale etter | Slettet | Avvist av -d | Registreringer prunet | Arbeidstrær på disk | Fjerngrenkandidater |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| CellProtocol | 64 | 52 | 12 | 0 | 0 | 18 | 8 |
| CellScaffold | 240 | 201 | 39 | 16 | 4 | 49 | 95 |
| CellProtocolDocuments | 31 | 27 | 4 | 0 | 4 | 4 | 0 |
| HavenAgentD | 18 | 15 | 3 | 0 | 0 | 8 | 2 |
| Binding | 61 | 53 | 8 | 0 | 2 | 11 | 3 |
| HAVEN-Deploy | 1 | 1 | 0 | 0 | 0 | 1 | Ikke vurdert |
| **Totalt** | **415** | **349** | **66** | **16** | **10** | **91** | **108** |

**HAVEN-Deploy:** `origin` er ikke konfigurert. `git fetch origin main` feilet; videre opprydding og vurdering av fjerngrener ble derfor ikke gjennomført i dette repoet.

## Metode og etterkontroll

- Rekkefølge per repo med vellykket fetch: `git fetch origin main`, `git worktree prune`, lokale ancestry-tester og eventuelt `git branch -d`, deretter kun lesing av fjerngrener.
- `origin/main` ble kontrollert mot `FETCH_HEAD`. Hver slettet gren bestod `git merge-base --is-ancestor <gren> origin/main` med exitkode 0. Full SHA ble registrert før sletting.
- `main`, `master`, nåværende gren, grener utsjekket i eksisterende arbeidstrær og `pdd/tillitspakke-agentflaate` ble beholdt. Alle grener der ancestry ikke ble bevist, ble også beholdt.
- `git worktree prune --dry-run --verbose` ble kontrollert først: alle registreringer som faktisk ble prunet, pekte til kataloger som allerede manglet. Selve oppryddingen brukte vanlig `git worktree prune` uten endring av utløpstid.
- Ingen eksisterende arbeidstrær eller arbeidstrefiler ble fjernet. Ingen tvangssletting, checkout, commit, push eller merge ble utført. Ingen fjerngrener eller lokale fjernreferanser ble slettet.
- Fetch fikk midlertidige prosessinnstillinger som hindret automatisk pruning av fjernreferanser, rekursiv submodul-fetch og automatisk GC/vedlikehold. Ingen slike Git-innstillinger ble endret varig.
- Fjerngrenlisten ble hentet direkte med `git ls-remote --heads origin`. Kandidatene ble testet mot SHA-en annonsert av origin, og remote main var fortsatt lik den hentede main-SHA-en. `main`, `master` og `pdd/tillitspakke-agentflaate` er ikke kandidater.
- Git-status, HEAD og SHA-256 av staged/unstaged diff var uendret før/etter Git-oppryddingen i alle 91 eksisterende arbeidstrær. Alle kontrollkommandoene lyktes. Dette er status-/diff-kontroll, ikke hashing av innholdet i alle utrackede filer.
- Etterkontroll bekreftet at øvrige lokale grenreferanser beholdt samme SHA, og at alle eksisterende arbeidstrekataloger fortsatt fantes. Rapporten ble opprettet etter disse kontrollene; ingen eksisterende uncommittede filer ble redigert.

En slettet gren kan gjenopprettes i riktig repo med `git branch <navn> <full-SHA>`. Tabellene nedenfor inneholder hele navnet og hele SHA-en.

## Avgrensninger

- **CellScaffold:** vanlig prune fjernet 4 registreringer, mens 22 registreringer til stier som ikke finnes på denne maskinen, ble stående. De er listet nedenfor. Ingen registreringer ble manuelt fjernet, låst opp eller tvangsprunet.
- **HavenAgentD:** repoet har grunn historikk (shallow). Bare positive ancestry-tester ble brukt som bevis. Negative tester betyr her «ikke bevist med tilgjengelig historikk». Historikken ble ikke utvidet.
- Fjerngrenkandidatene er et øyeblikksbilde til Kjetils vurdering. **Ingen av dem er slettet.**

## CellProtocol

Repo: `/Users/kjetil/Build/Digipomps/HAVEN/CellProtocol`.
Lokale grener: **64 → 52**. Nåværende gren: `pdd/tillitspakke-agentflaate`.
Fetch utført: 2026-09-18 09:39:03 CEST. Exitkode: 0.
Hentet `origin/main`: `b5b7282b495e96a7899a189087592581426f4bfb`.

### Slettede lokale grener

| Gren | Full SHA før sletting |
| --- | --- |
| `claude/angry-matsumoto-f69734` | `35c8484c35a8f5e6e04b003c2b58c0981e6972f3` |
| `codex/correspondence-durable-snapshot-20260717` | `e3658834cad9c9e6bda0cdc2c6a2fd454a7cd2d2` |
| `codex/device-ingress-fileutils-ci-20260719` | `dafdf7c83c86920d84992b285496f543d2a9686f` |
| `codex/entity-authority-durable-replica` | `279ff3e2c52a1795c95b132d2384e5fcd03f9290` |
| `codex/haven-robustness-core` | `d9d95145fc67910d2b4242c78af0ccc30cdabd6d` |
| `codex/identity-entity-anchor-live-resolution` | `b7cef19fd6dc9cbb37ea9e028a1ff191ccbe4685` |
| `codex/integrate-main-20260716` | `90956f2037924c6d72eda57935403bb28f6562df` |
| `codex/owner-proof-diagnostic-20260808` | `1632ed65d5e4aaf663b26cee1cdddfdcdd5e4412` |
| `codex/proof-bound-runtime-rehydration-20260717` | `829070410d2810f52880548d63733d475d1d8a85` |
| `codex/proved-claim-vc` | `c7248ac672652c5cf1f4ec3fafa6a3aa49032c61` |
| `codex/trusted-issuer-admission` | `bfc176ffecd4f718cd47e4a9db6183a2b0378def` |
| `codex/trusted-issuer-proof-admission` | `080bb934bf4457ac59a1fe7679d598b2beaf4bc7` |

### Beholdt fordi utsjekket / eksisterende arbeidstrær

Alle arbeidstrær i tabellen finnes fortsatt på disk. Alle navngitte grener er beholdt fordi de er utsjekket; detached HEAD har ingen utsjekket gren.

| Utsjekket gren / tilstand | Arbeidstre |
| --- | --- |
| `pdd/tillitspakke-agentflaate` (repoets nåværende) | `/Users/kjetil/Build/Digipomps/HAVEN/CellProtocol` |
| `codex/prod-complete-20260917` | `/private/tmp/haven-prod-20260917/CellProtocol` |
| `codex/runtime-capacity-ci` | `/Users/kjetil/.codex/worktrees/443a/CellProtocol` |
| detached HEAD `79740304167aa4f4daadd148c5a369e919d25a6a` | `/Users/kjetil/.codex/worktrees/a027/CellProtocol` |
| `pdd/bridge-provenance` | `/Users/kjetil/Build/Digipomps/HAVEN/_worktrees/cellprotocol-bridge-provenance` |
| `pdd/formaalsregister-som-graf` | `/Users/kjetil/Build/Digipomps/HAVEN/_worktrees/cellprotocol-formaalsregister-wp0` |
| `losen/visionos-sim-20260916` | `/Users/kjetil/Build/Digipomps/HAVEN/_worktrees/visionos-20260916/CellProtocol` |
| detached HEAD `35c8484c35a8f5e6e04b003c2b58c0981e6972f3` | `/Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/.claude/worktrees/angry-matsumoto-f69734` |
| `claude/bridge-query-credential-20260830` | `/Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/_wt-bridge-credential-20260830` |
| `claude/bro-bridgehead-20260915` | `/Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/_wt-bro-20260915` |
| `codex/condition-resolution-native-20260828` | `/Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/_wt-condition-resolution-20260828` |
| `claude/identity-link-runtime-policy-20260904` | `/Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/_wt-identity-link-wp1-20260904` |
| detached HEAD `8c0956091c5bb534e5b43ac161020f348e0d4f7c` | `/Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/_wt-invite-merge-20260901` |
| `claude/list-tree-followtail-20260905` | `/Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/_wt-list-tree-20260905` |
| `claude/skeleton-overlay-20260902` | `/Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/_wt-overlay-20260902` |
| `claude/skeleton-style-parity-20260828` | `/Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/_wt-skeleton-parity-20260828` |
| `claude/parity-renderer-20260904` | `/Users/kjetil/Build/Digipomps/HAVEN/parity/CellProtocol` |
| `codex/entity-correspondence-20260910` | `/Users/kjetil/Build/Digipomps/HAVEN/sprout/implementation/entity-correspondence/CellProtocol` |

Andre uttrykkelig beskyttede grener: `main`.
Øvrige grener beholdt uten bevist ancestry til main: **36**.

### Slettinger Git nektet

Ingen.

### Prune av arbeidstreregistreringer

**0 registreringer prunet** (18 → 18 registreringer). Eksisterende arbeidstrær er listet ovenfor.

### Fjerngrenkandidater på origin – ikke slettet

Fersk grenliste lest 2026-09-18 09:39:07 CEST. **8 kandidater.**

- `origin/claude/invite-types-to-main-20260901` — `8c0956091c5bb534e5b43ac161020f348e0d4f7c`.
- `origin/codex/cell-access-proof-20260507` — `5a297e8ef8bd8ea1f5d04b193fbe8cd13da9f23a`.
- `origin/codex/cellprotocol-identity-hardening` — `23167bd9b286ba3b5e30472532ca4a454b435d37`.
- `origin/codex/correspondence-durable-snapshot-20260717` — `e3658834cad9c9e6bda0cdc2c6a2fd454a7cd2d2`.
- `origin/codex/entity-authority-durable-replica` — `279ff3e2c52a1795c95b132d2384e5fcd03f9290`.
- `origin/codex/integrate-entity-authority-main-20260717` — `81d41e427b6227db309137650f36bdc3fec2a350`.
- `origin/codex/persisted-named-scaffold-restore-20260718` — `61ffc8990afd34a601231e332e423b905e04535f`.
- `origin/codex/proof-bound-runtime-rehydration-20260717` — `829070410d2810f52880548d63733d475d1d8a85`.

Utelatt som beskyttet: `origin/main`, `origin/pdd/tillitspakke-agentflaate`.

Etterkontroll: 18 eksisterende arbeidstrær kontrollert; ingen endring i status, HEAD eller staged/unstaged diff under Git-oppryddingen.

## CellScaffold

Repo: `/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold`.
Lokale grener: **240 → 201**. Nåværende gren: `pdd/tillitspakke-agentflaate`.
Fetch utført: 2026-09-18 09:39:19 CEST. Exitkode: 0.
Hentet `origin/main`: `87256f9ac643b27fa4667ec167023249f2a2a5e6`.

### Slettede lokale grener

| Gren | Full SHA før sletting |
| --- | --- |
| `claude/action-requester-symmetry-20260830` | `2f3056897857654ffd3729a455242654b01dfcb3` |
| `claude/bootstrap-read-count-20260830` | `e27d5c6e485f94ec17b1e79d1dedf8641d811a2e` |
| `claude/corr-approval-visible-denial-20260829` | `ff8707cc24992c9d988e0a2e6addd65f21648914` |
| `claude/corr-invite-runbook-20260828` | `51559449a457cb325fd371536ba3410bb23b3498` |
| `claude/corr-runbook-image-correction-20260828` | `fe95d7e9cb9457bd0559a794474116ee2ecb162e` |
| `claude/correspondence-principal-guard-20260820` | `feef0e4d037fd6bf806a599f45b06938ac469b08` |
| `claude/deploy-kvittering-20260831` | `664be661c20ce4d5fe6ca50aca07869179f5e2e0` |
| `claude/deploy-notes-sessions-ghcr-20260830` | `491f0143fda0635960de0c4fa5056d8941b4d9db` |
| `claude/handoff-korreksjon-20260831` | `2f6bd3ca658877ba5acbca8d191a38c62c0df963` |
| `claude/haven-deploy-env-only-20260828` | `ebe61e55fd56e7564dd424349bfba29f707a9b4a` |
| `claude/invitasjonslanding-fra-156-20260901` | `a2f5f7686c3b52115d23027b1e2eafc3cb1460cb` |
| `claude/notification-diagnostic-20260830` | `0a9a663dcf2001e618758dc6a435c897714e65f6` |
| `claude/porthole-bounded-discovery-20260825` | `2ac5c81c0ebc532e840ae9e300ff14a8b4a363be` |
| `claude/porthole-projection-ancestor-b` | `3d8753bf725eff17890b76f1033f4cb7a4d93bda` |
| `claude/salvage-on-main-20260829` | `b62b3ecccb2255576232b8ec2afb5b37801dd87a` |
| `claude/set-env-file-20260830` | `16103531085ba80d554b1cd57a586d81d14bb86f` |
| `claude/testgjeld-tre-bolker-20260901` | `63ecc5b1d3cb854a8cf18f3c8f088e6b813bde5e` |
| `codex/arendalsuka-thursday-p0-release-20260901` | `078362903cd10198ea816c0f30c1b4c637465b6a` |
| `codex/butler-chat-router-20260831` | `807e5000d8a90b2f39fb5087d78c3327ef0ab573` |
| `codex/butler-chat-scroll-restore-20260820` | `feef0e4d037fd6bf806a599f45b06938ac469b08` |
| `codex/butler-scroll-raf-race-20260902` | `aca734fe3b2ef45a2d788fe3440d30162a56c491` |
| `codex/cell-owned-access-authority-20260902` | `86d0ba420a768ec55ad2bcf0817637eaa4c132dc` |
| `codex/corr-owner-route-release-20260821` | `6f6e819d8af9ce220db95abf3df6836a9b57f9b8` |
| `codex/correspondence-approval-surface-20260826` | `d30e8c944691d96d9a103e7514fbccdd48d958ce` |
| `codex/deploy-autonomy-phase0-v3-v4-20260901` | `4fbd04937c1abe8807c2ac17cd5715a5b12de348` |
| `codex/docs-evening-salvage-20260821` | `e1f3e22f02239e44eacaf12a741d78b4066d0c35` |
| `codex/ghcr-prefetch-production-20260901` | `08c748554e23f227ff8d04ec33d624f08d8217d8` |
| `codex/image-publish-capacity-20260821` | `77c2c09f9a7776405231f5805d410cd9d8b0c933` |
| `codex/music-free-price-and-resolution-20260828` | `1f1457c13ec055c8ec6c23aa21c603e56f5f1d50` |
| `codex/palazzo-p0-w1-w5b-20260821` | `e1f3e22f02239e44eacaf12a741d78b4066d0c35` |
| `codex/pr185-main-rebase` | `2318a5b24d26bb66bbc01246b34a924b765d10a8` |
| `codex/staging-deploy-preflight-fix-20260818` | `f76de5a984501cb4d67e275c892d62ce3fc348c7` |
| `codex/staging-identical-key-recovery-20260818` | `744e7e10df44e313a4fdd7925af223dd89a17fea` |
| `fix/butler-chat-scroll-restore` | `aee0d7c5fefbb1a1d4da58bb021329f982842383` |
| `release-main` | `e085fdc511761d712eacd803dcc49b7112ec6715` |
| `release-main-1d11b5e0` | `1d11b5e0c50aed06c0178ca4b61099feb99edd84` |
| `release-main-3a4cc2b7` | `3a4cc2b73ba5b01c0ee786f112372b2fe1da56f0` |
| `release-main-3d24c678` | `3d24c67875a40b3fc57b08de8020b30ab2613c6f` |
| `release-main-7dff2c11` | `7dff2c11f27cac5539f7741aa4b182cc15c2cf77` |

### Beholdt fordi utsjekket / eksisterende arbeidstrær

Alle arbeidstrær i tabellen finnes fortsatt på disk. Alle navngitte grener er beholdt fordi de er utsjekket; detached HEAD har ingen utsjekket gren.

| Utsjekket gren / tilstand | Arbeidstre |
| --- | --- |
| `pdd/tillitspakke-agentflaate` (repoets nåværende) | `/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold` |
| `codex/admin-transaction-20260918` | `/private/tmp/haven-admin-ops-20260918` |
| `codex/prod-complete-20260917` | `/private/tmp/haven-prod-20260917/CellScaffold` |
| detached HEAD `b8df547ea244c08beea4d527fd83c7ef791207a4` | `/Users/kjetil/.codex/worktrees/29a7/CellScaffold` |
| detached HEAD `b8df547ea244c08beea4d527fd83c7ef791207a4` | `/Users/kjetil/.codex/worktrees/29ed/CellScaffold` |
| `codex/entity-fabric-20260911` | `/Users/kjetil/.codex/worktrees/c8a4/CellScaffold` |
| detached HEAD `b8df547ea244c08beea4d527fd83c7ef791207a4` | `/Users/kjetil/.codex/worktrees/e34a/CellScaffold` |
| `pdd/butler-hjelpertre` | `/Users/kjetil/Build/Digipomps/HAVEN/_worktrees/cellscaffold-butler-hjelpertre` |
| `pdd/butler-widgetflate` | `/Users/kjetil/Build/Digipomps/HAVEN/_worktrees/cellscaffold-butler-widgetflate` |
| `pdd/corr-varsel-recipient-feed` | `/Users/kjetil/Build/Digipomps/HAVEN/_worktrees/cellscaffold-corr-varsel-s1` |
| `fix/dokumentbevis-koalesering` | `/Users/kjetil/Build/Digipomps/HAVEN/_worktrees/cellscaffold-dokumentbevis` |
| `fix/registrer-bridgehead-rute` | `/Users/kjetil/Build/Digipomps/HAVEN/_worktrees/cellscaffold-registrer-bridgehead-rute` |
| `codex/async-app-test-20260912` | `/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold-async-app-test-20260912` |
| `release/corr-staging-gate-20260820` | `/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold-corr-deploy` |
| `claude/palazzo-transport-p0-20260821` | `/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_salvage/wt-palazzo-p0` |
| `claude/admin-gui-20260902` | `/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-admin-gui-20260902` |
| `claude/admin-production-controller-wo-20260902` | `/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-admin-wo-20260902` |
| `claude/bridge-identity-proof-20260830` | `/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-bridge-identity-20260830` |
| `claude/bro-bridgehead-20260915` | `/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-bro-20260915` |
| detached HEAD `b8df547ea244c08beea4d527fd83c7ef791207a4` | `/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-butler-baseline-20260908` |
| `claude/butler-no-model-20260902` | `/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-butler-nomodel-20260902` |
| `claude/butler-signal-20260908` | `/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-butler-signal-20260908` |
| `claude/butler-smoke-prereq-copy-20260902` | `/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-butler-smoke-20260902` |
| `claude/chatlog-scroll-20260902` | `/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-chatlog-20260902` |
| `codex/ci-bolk-diagnostics-20260909` | `/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-codex-ci-bolk-20260909` |
| `claude/credits-epoke-entities-20260909` | `/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-credits-epoke-20260909` |
| `claude/deploy-evidence-20260902` | `/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-deploy-evidence-20260902` |
| `claude/deploy-green-20260909` | `/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-deploygreen-20260909` |
| `claude/invitasjonslanding-kode-20260901` | `/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-deployhandoff-20260831` |
| `claude/registry-drift-check-20260903` | `/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-driftcheck-20260903` |
| `claude/identity-link-web-20260904` | `/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-identity-link-web-20260904` |
| `claude/integration-20260902` | `/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-integration-20260902` |
| `claude/kallimachos-capable-model-demo-20260902` | `/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-kallimachos-fix` |
| `claude/arendalsuka-knowledge-off-20260904` | `/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-know-off` |
| `claude/butler-latency-20260902` | `/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-latency-20260902` |
| `claude/skeleton-list-tree-followtail-20260905` | `/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-list-tree-20260905` |
| `claude/mix-tidy-20260904` | `/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-mix-tidy-20260904` |
| `claude/onboarding-connect-model-20260902` | `/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-onboarding-20260902` |
| `claude/porthole-projection-ancestor-20260830` | `/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-projection-20260830` |
| `claude/arendalsuka-publisher-bootstrap-20260909` | `/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-publisher-bootstrap-20260909` |
| `claude/publication-cell-20260902` | `/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-publishing-20260902` |
| `codex/purpose-cell-fase1-20260828` | `/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-purpose-cell-20260828` |
| `claude/player-queue-20260903` | `/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-queue-20260903` |
| `pdd/scaffold-admin-delegering` | `/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-sad-20260909` |
| `claude/skeleton-parity-20260903` | `/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-skeleton-parity-20260903` |
| `claude/tabs-optimistic-hold-20260904` | `/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-tabs` |
| `claude/wallet-handoff-resultat-20260909` | `/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-wallet-handoff-doc-20260909` |
| `claude/workbench-decisions-2-5-20260905` | `/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-wb-decisions-20260905` |
| `codex/scaffold-admin-staging-20260911` | `/Users/kjetil/Build/Digipomps/HAVEN/DiMyMint/CellScaffold-session-recovery` |

Andre uttrykkelig beskyttede grener: `main`.
Øvrige grener beholdt uten bevist ancestry til main: **139**.

### Slettinger Git nektet

Disse grenene bestod ancestry-testen, men `git branch -d` nektet. De ble beholdt. Git-feilens `error:`-linjer er gjengitt ordrett; forslag om tvangssletting er utelatt.

- `claude/deploy-handoff-codex-20260831` — SHA `8830a5c853ed1ab5431ab43c11da466444d0617e`.

  ```text
  error: the branch 'claude/deploy-handoff-codex-20260831' is not fully merged
  ```

- `claude/exclude-admin-bridge-loopback-20260825` — SHA `4a22dc90499b24ab0e7bd8f6a41d76ed943ba2ce`.

  ```text
  error: the branch 'claude/exclude-admin-bridge-loopback-20260825' is not fully merged
  ```

- `claude/purpose-analysis-method-20260821` — SHA `06afb9433e266ec3b90cddec7678b5c6c9b8e965`.

  ```text
  error: the branch 'claude/purpose-analysis-method-20260821' is not fully merged
  ```

- `codex/bridge-multiplex-host-route-main-20260820` — SHA `dd72f4edd247525501e891644d9e78771a0f2124`.

  ```text
  error: the branch 'codex/bridge-multiplex-host-route-main-20260820' is not fully merged
  ```

- `codex/ci-build-admin-loopback-20260826` — SHA `70857d8f8812214b3f0b926137f85be3a9fceb19`.

  ```text
  error: the branch 'codex/ci-build-admin-loopback-20260826' is not fully merged
  ```

- `codex/haven-deploy-public-status-20260901` — SHA `772b55c066698fa0072bc24085da0eb291744f25`.

  ```text
  error: the branch 'codex/haven-deploy-public-status-20260901' is not fully merged
  ```

- `codex/purpose-cell-fase1-refresh-20260901` — SHA `5d978e807316357999a2c83490702e11a5859843`.

  ```text
  error: the branch 'codex/purpose-cell-fase1-refresh-20260901' is not fully merged
  ```

- `codex/staging-browser-proof-race-20260901` — SHA `6102cf1635412b87ed9478aebf2d01b694a165fd`.

  ```text
  error: the branch 'codex/staging-browser-proof-race-20260901' is not fully merged
  ```

- `codex/workitems-explore-contracts-20260901` — SHA `ab6a78b45d667b5aa68e6c9ed7b80e38d1876b0f`.

  ```text
  error: the branch 'codex/workitems-explore-contracts-20260901' is not fully merged
  ```

- `pr165` — SHA `62966a9016146f834491f4e516af3beede2b0198`.

  ```text
  error: the branch 'pr165' is not fully merged
  ```

- `probe-lock-test` — SHA `3a4cc2b73ba5b01c0ee786f112372b2fe1da56f0`.

  ```text
  error: the branch 'probe-lock-test' is not fully merged
  ```

- `claude/butler-demo-copy-20260902` — SHA `016093f32dd98edb83b7ab1c558a81d74d683682`.

  ```text
  error: cannot delete branch 'claude/butler-demo-copy-20260902' used by worktree at '/sessions/rcw-01ybph6m1x9vwmndzfbriqyj/mnt/CellScaffold/_wt-butler-copy-20260902'
  ```

- `claude/correspondence-reenrollment-20260820` — SHA `feef0e4d037fd6bf806a599f45b06938ac469b08`.

  ```text
  error: cannot delete branch 'claude/correspondence-reenrollment-20260820' used by worktree at '/sessions/rcw-01ldnxg8tdbpaquu8svq8oyz/mnt/CellScaffold/_salvage/wt-x'
  ```

- `claude/empty-without-text-20260904` — SHA `c7c724fa31a39320be3a12dae10d795107a86cf8`.

  ```text
  error: cannot delete branch 'claude/empty-without-text-20260904' used by worktree at '/sessions/rcw-01ybph6m1x9vwmndzfbriqyj/mnt/CellScaffold/_wt-empty-20260904'
  ```

- `claude/main-gate-contract-20260826` — SHA `aeea76b4f7b52e7fe0ac3c30ad9aa3ccf99fdc46`.

  ```text
  error: cannot delete branch 'claude/main-gate-contract-20260826' used by worktree at '/sessions/rcw-01v9wap2htt63zh5p3bh91vt/mnt/worktrees/mergegate'
  ```

- `claude/onboarding-panel-state-20260902` — SHA `42e53b70ebe9b5a3582175110bc78644fdd785e1`.

  ```text
  error: cannot delete branch 'claude/onboarding-panel-state-20260902' used by worktree at '/sessions/rcw-01ybph6m1x9vwmndzfbriqyj/mnt/CellScaffold/_wt-onboarding-panel-20260902'
  ```


### Prune av arbeidstreregistreringer

**4 registreringer prunet** (75 → 71 registreringer). Eksisterende arbeidstrær er listet ovenfor.

Følgende kataloger manglet allerede; bare registreringene ble fjernet:

- `/private/tmp/cp-security-baseline/CellScaffold`.
- `/private/tmp/cp-security-consumer/CellScaffold`.
- `/private/tmp/cp-security-published-consumer/CellScaffold`.
- `/private/tmp/haven-richtext-20260910`.

**22 registreringer står fortsatt, men stiene finnes ikke på denne maskinen:**

| Registrert gren / tilstand | Manglende sti |
| --- | --- |
| `claude/f76-unclaimed-source-mount-20260819` | `/private/tmp/claude-f76-fix` |
| `claude/deploy-secret-env-20260904` | `/sessions/rcw-012zjixu8osf5ruf6gpa4ttw/mnt/CellScaffold/_wt-stripe-prod-env-20260904` |
| `claude/butler-chat-scroll-restore-20260820` | `/sessions/rcw-01ldnxg8tdbpaquu8svq8oyz/mnt/CellScaffold/_salvage/wt-a` |
| `claude/correspondence-reenrollment-20260820b` | `/sessions/rcw-01ldnxg8tdbpaquu8svq8oyz/mnt/CellScaffold/_salvage/wt-b` |
| `claude/ci-workbench-test-filter-20260820` | `/sessions/rcw-01ldnxg8tdbpaquu8svq8oyz/mnt/CellScaffold/_salvage/wt-ci` |
| `claude/ci-runner-disk-20260820` | `/sessions/rcw-01ldnxg8tdbpaquu8svq8oyz/mnt/CellScaffold/_salvage/wt-ci2` |
| `claude/workboard-smoke-and-seed-20260820` | `/sessions/rcw-01ldnxg8tdbpaquu8svq8oyz/mnt/CellScaffold/_salvage/wt-d` |
| `claude/docs-and-workorders-20260820` | `/sessions/rcw-01ldnxg8tdbpaquu8svq8oyz/mnt/CellScaffold/_salvage/wt-f` |
| `claude/ops-cutover-sudo-20260820` | `/sessions/rcw-01ldnxg8tdbpaquu8svq8oyz/mnt/CellScaffold/_salvage/wt-ops` |
| `claude/correspondence-reenrollment-20260820` | `/sessions/rcw-01ldnxg8tdbpaquu8svq8oyz/mnt/CellScaffold/_salvage/wt-x` |
| `losen/verk-portefolje-20260916` | `/sessions/rcw-01ljsuyhuptejnssslcbbmy3/mnt/CellScaffold/_wt-verk-20260916` |
| `claude/main-gate-contract-20260826` | `/sessions/rcw-01v9wap2htt63zh5p3bh91vt/mnt/worktrees/mergegate` |
| `claude/admin-gui-followup-20260903` | `/sessions/rcw-01ybph6m1x9vwmndzfbriqyj/mnt/CellScaffold/_wt-admin-gui-followup-20260903` |
| `claude/admin-leaf-theme-20260903` | `/sessions/rcw-01ybph6m1x9vwmndzfbriqyj/mnt/CellScaffold/_wt-admin-leaf-theme-20260903` |
| `claude/butler-demo-copy-20260902` | `/sessions/rcw-01ybph6m1x9vwmndzfbriqyj/mnt/CellScaffold/_wt-butler-copy-20260902` |
| `claude/catalog-summary-20260904` | `/sessions/rcw-01ybph6m1x9vwmndzfbriqyj/mnt/CellScaffold/_wt-catalog-summary-20260904` |
| `claude/empty-without-text-20260904` | `/sessions/rcw-01ybph6m1x9vwmndzfbriqyj/mnt/CellScaffold/_wt-empty-20260904` |
| `claude/natt-qa-docs-20260904` | `/sessions/rcw-01ybph6m1x9vwmndzfbriqyj/mnt/CellScaffold/_wt-nattqa-docs-20260904` |
| `claude/onboarding-panel-state-20260902` | `/sessions/rcw-01ybph6m1x9vwmndzfbriqyj/mnt/CellScaffold/_wt-onboarding-panel-20260902` |
| `claude/porthole-a11y-copy-20260904` | `/sessions/rcw-01ybph6m1x9vwmndzfbriqyj/mnt/CellScaffold/_wt-porthole-a11y-20260904` |
| detached HEAD `923e9c99a83ecac7a480f5341648bae3e101e8e8` | `/sessions/rcw-01ybph6m1x9vwmndzfbriqyj/mnt/CellScaffold/_wt-review-205` |
| `claude/studio-copy-20260904` | `/sessions/rcw-01ybph6m1x9vwmndzfbriqyj/mnt/CellScaffold/_wt-studio-copy-20260904` |

### Fjerngrenkandidater på origin – ikke slettet

Fersk grenliste lest 2026-09-18 09:45:49 CEST. **95 kandidater.**

- `origin/claude/action-requester-symmetry-20260830` — `2f3056897857654ffd3729a455242654b01dfcb3`.
- `origin/claude/bootstrap-read-count-20260830` — `e27d5c6e485f94ec17b1e79d1dedf8641d811a2e`.
- `origin/claude/build-capacity-percent-floor-20260820` — `515a37b73326036a4011cbb9ffcf83e2e3527745`.
- `origin/claude/butler-demo-copy-20260902` — `9f319f316227d9fa168ee3f6a60d46cf27a2fe82`.
- `origin/claude/butler-latency-20260902` — `60cc875612bc39b06ce3e923fa38f0f3160670aa`.
- `origin/claude/butler-no-model-20260902` — `b3b98c8ff50bc33dd7c8696ec3fa6d1f3b1e005f`.
- `origin/claude/butler-signal-20260908` — `dfd8b77e3b0bf69e9229811f663e4436be9bbcd2`.
- `origin/claude/butler-spatial-optional-20260831` — `c0ee784a928db879142fc3a09ccde35e7442a6ef`.
- `origin/claude/butterpop-track-removal-20260831b` — `d910f82996649b460eb8e8e2feaa797511b56172`.
- `origin/claude/chatlog-scroll-20260902` — `d85119ad09e52d4e547ef0d01f6856b947fe98c9`.
- `origin/claude/corr-approval-visible-denial-20260829` — `ff8707cc24992c9d988e0a2e6addd65f21648914`.
- `origin/claude/corr-invite-runbook-20260828` — `51559449a457cb325fd371536ba3410bb23b3498`.
- `origin/claude/corr-runbook-image-correction-20260828` — `fe95d7e9cb9457bd0559a794474116ee2ecb162e`.
- `origin/claude/credits-epoke-entities-20260909` — `3bb6820b72696a69415acdc12361e4de0eb9e398`.
- `origin/claude/deploy-kvittering-20260831` — `664be661c20ce4d5fe6ca50aca07869179f5e2e0`.
- `origin/claude/deploy-notes-sessions-ghcr-20260830` — `491f0143fda0635960de0c4fa5056d8941b4d9db`.
- `origin/claude/empty-without-text-20260904` — `f0a4e63892b3b486a954bce225c50356e0ca8c98`.
- `origin/claude/f76-identity-migration-and-observability-20260818` — `999b0b340fc358d2b00e07bfa51aa9ac175e2efe`.
- `origin/claude/handoff-korreksjon-20260831` — `2f6bd3ca658877ba5acbca8d191a38c62c0df963`.
- `origin/claude/haven-deploy-env-only-20260828` — `ebe61e55fd56e7564dd424349bfba29f707a9b4a`.
- `origin/claude/identity-link-web-20260904` — `fa39b4524a355c8dcbccc4ae55afb6de371a4134`.
- `origin/claude/integration-20260902` — `249eec644c55170ce088678f1546e979ff03cc0e`.
- `origin/claude/invitasjonslanding-fra-156-20260901` — `a2f5f7686c3b52115d23027b1e2eafc3cb1460cb`.
- `origin/claude/invitasjonslanding-kode-20260901` — `1019743e83221cb2a10970d8d74d66df97afe728`.
- `origin/claude/kallimachos-capable-model-demo-20260902` — `8437a151472f7d148023da35d630deeb2326b7b6`.
- `origin/claude/main-gate-contract-20260826` — `aeea76b4f7b52e7fe0ac3c30ad9aa3ccf99fdc46`.
- `origin/claude/meter-access-entry-20260820` — `0938aff3c2065aeb380c82dfcbcdb5ccd75634d4`.
- `origin/claude/notification-diagnostic-20260830` — `0a9a663dcf2001e618758dc6a435c897714e65f6`.
- `origin/claude/onboarding-connect-model-20260902` — `0df60366e800ab5ee12045794922dd0e48901860`.
- `origin/claude/onboarding-panel-state-20260902` — `d0c53fcf523eeb5b4fe0ce407741762699f435cd`.
- `origin/claude/player-queue-20260903` — `6fb299f4497dbe1b899a1b022f1ebf5c69e8b66a`.
- `origin/claude/porthole-projection-ancestor-b` — `3d8753bf725eff17890b76f1033f4cb7a4d93bda`.
- `origin/claude/registry-drift-check-20260903` — `02a4d9b03c050cd41cd67b4eeecb8aaaeaf26569`.
- `origin/claude/salvage-on-main-20260829` — `b62b3ecccb2255576232b8ec2afb5b37801dd87a`.
- `origin/claude/set-env-file-20260830` — `16103531085ba80d554b1cd57a586d81d14bb86f`.
- `origin/claude/skeleton-list-tree-followtail-20260905` — `c42eb48786da748a47b2705fc00bbbaea288a1a1`.
- `origin/claude/skeleton-parity-20260903` — `c4dcb6a55e9ec825767b15c28ce88cdff4695e50`.
- `origin/claude/tabs-optimistic-hold-20260904` — `660c933b97668c5bb0fcc3d66158785e32062fb7`.
- `origin/claude/testgate-149-suiter-20260909` — `9a678a21a0fd6dcd8400a296f51913b767bba07b`.
- `origin/claude/testgjeld-tre-bolker-20260901` — `63ecc5b1d3cb854a8cf18f3c8f088e6b813bde5e`.
- `origin/claude/value-flow-viewer-20260820` — `c7115c8febb3e298fff2f89b4cff9aa78a336fb3`.
- `origin/claude/workbench-decisions-2-5-20260905` — `8249dc244032c182669282b1f879db41786c43b2`.
- `origin/codex/admin-node-fleet-dashboard-20260813` — `8cfa73580392e14fe5d8b9f2974f8a94f4a9e733`.
- `origin/codex/arendalsuka-progressive-bootstrap-20260730` — `b2cbc2d1f31895c3ecaef733cd61f816e5504f71`.
- `origin/codex/arendalsuka-publisher-vc-20260729` — `66623e7f4940416f70e4c51f741003143434126e`.
- `origin/codex/arendalsuka-thursday-demo-p0` — `2318a5b24d26bb66bbc01246b34a924b765d10a8`.
- `origin/codex/arendalsuka-thursday-p0-release-20260901` — `078362903cd10198ea816c0f30c1b4c637465b6a`.
- `origin/codex/atomic-staging-current-main-20260801` — `375fdc8b65b06999d752ad105194cce070f8c1b3`.
- `origin/codex/atomic-staging-transaction-20260731` — `6f7a175c1ddc4dc79a18a3abec12a50e7e0809aa`.
- `origin/codex/bootstrap-canonical-recovery-20260805` — `fcdee4af26f288b21098afd1f929359e95ee0593`.
- `origin/codex/butler-scroll-raf-race-20260902` — `aca734fe3b2ef45a2d788fe3440d30162a56c491`.
- `origin/codex/cell-owned-access-authority-20260902` — `86d0ba420a768ec55ad2bcf0817637eaa4c132dc`.
- `origin/codex/ci-bolk-diagnostics-20260909` — `aad6f4d6f31a13c4cb05010d08d0868eecab5156`.
- `origin/codex/ci-main-post-merge-gate-20260801` — `4f67b52c38178dee2ac7ed9a2113355428a625d0`.
- `origin/codex/conference-access-request-restart-bindings-20260812` — `c6c6597d57081e7a498748a906f74f0bf7039d1a`.
- `origin/codex/corr-owner-route-release-20260821` — `6f6e819d8af9ce220db95abf3df6836a9b57f9b8`.
- `origin/codex/correspondence-admin-approval-20260730` — `1c2af7eeeb4810d5f628a46465f816092ff1412a`.
- `origin/codex/correspondence-approval-surface-20260826` — `8116a0f1614cb05d51a28e234a10c1cf5eb85d7a`.
- `origin/codex/development-admin-release-controls-20260719` — `c9a3f0f370dd25f202362bc0367c55202073b610`.
- `origin/codex/development-status-producer-current-20260801` — `a0ef795728e85cef8c57b361f2db5f3ccce60cd4`.
- `origin/codex/device-ingress-callback-authority-20260813` — `b63fa38339935391596bb41deb2579df6af81bf7`.
- `origin/codex/device-ingress-deploy-wiring-20260813` — `423e7de054bcde140d4f4e9b6f75f93f9ca1f1f2`.
- `origin/codex/device-ingress-enrollment-handoff-20260814` — `44390d340183e301ff000e9f5849e6987a9c6cd6`.
- `origin/codex/device-ingress-release-20260813` — `078a88a280a7152084960d94cf3956ccd93a3ec3`.
- `origin/codex/device-ingress-runtime-release-20260813` — `e2ce159680e78c51297966eeb72a33efdd820258`.
- `origin/codex/device-ingress-staging-owner-pin-20260813` — `413d782eaa4343d8c8c66addd5ead07830b876a3`.
- `origin/codex/fileutils-pin-alignment-20260801` — `757d8c4f8263f0a1c1fc8825a9f75f4b6362a8bb`.
- `origin/codex/ghcr-prefetch-production-20260901` — `08c748554e23f227ff8d04ec33d624f08d8217d8`.
- `origin/codex/haven-aasa-production-hotfix-20260805` — `8eb9cca7602d277152ec089fddd8f826cbe06fc2`.
- `origin/codex/image-publish-capacity-20260821` — `77c2c09f9a7776405231f5805d410cd9d8b0c933`.
- `origin/codex/linux-runtime-manifest-fix-20260802` — `3708bc8963cfabdca2d3774ac5c373f5f19ece14`.
- `origin/codex/music-free-price-and-resolution-20260828` — `1f1457c13ec055c8ec6c23aa21c603e56f5f1d50`.
- `origin/codex/passkey-named-account-binding-20260801` — `3b23ecf6157cef788c9d8217fd1c075b3927ecfc`.
- `origin/codex/personal-chat-account-continuity-20260812` — `7f0e8b55d529629cbd41a12b57133d68f49650e0`.
- `origin/codex/personal-copilot-config-get-nonpersist-20260803` — `4582facc293e88f7e6de5ed259aeff740e4b2d7b`.
- `origin/codex/personal-entity-activity-dashboard-20260721` — `43ce1b1b9531ed43d7997abb5051ac90977d6d62`.
- `origin/codex/porthole-account-compatibility-20260811` — `823bbae12e8935ed3b23a13deea77d140fd5ddb6`.
- `origin/codex/porthole-lookup-fastfail-20260826` — `40aded7886fac1c16dde3db1537a80da2c1be595`.
- `origin/codex/porthole-navigation-refresh-race-20260812` — `3b6e98c0f79b8d6d6a359df4627dabc066511b33`.
- `origin/codex/porthole-scaffoldsetup-fastpath-20260814` — `de5e1a94a9e38575e2a6e0b81bfaf37195e00fe3`.
- `origin/codex/render-real-skeleton-icons-20260812` — `30799aad1e25bf2c464138cdc2190243659253da`.
- `origin/codex/resource-quota-durable-current-20260801` — `0b82083638b43621efb0a6493818326a5af225c8`.
- `origin/codex/runtime-identity-interrupted-provision-recovery-20260812` — `4015c75c4d9a2f08c98d507b3b11b1278c6ca392`.
- `origin/codex/runtime-identity-porthole-release-20260811` — `c74d8826411ff4a35a7a1d46df34d5c016006480`.
- `origin/codex/staging-deploy-main-20260801` — `b60a650919839eb73ef79fd7493ea40d7dd4a0fb`.
- `origin/codex/staging-deploy-workflow-guard-20260818` — `9eb76a231f9a83e2bb3078bdf8be60c9dbce6993`.
- `origin/codex/staging-identical-key-recovery-20260818` — `744e7e10df44e313a4fdd7925af223dd89a17fea`.
- `origin/codex/staging-integrated-device-ingress-20260730` — `d155252dca4283b644db5628a8182084be860bbc`.
- `origin/codex/staging-message-release-20260729` — `036cc111108fd1ebd466a8085107238b5add7960`.
- `origin/codex/staging-message-skeleton-acceptance-20260729` — `96d0350c15e1f25a75fa81e54c3558a0df44fffe`.
- `origin/codex/staging-startup-indexed-recovery-20260805` — `a718f54af687e906bbb28779a9957d0414bb8762`.
- `origin/codex/swiftpm-mirror-pin-integrity-20260801` — `b2d1c4e7fa86583ba6ac5fac4f18829b88e9ab7b`.
- `origin/codex/v2-chat-fail-fast-legacy-surfaces-20260812` — `5dc0cf13bf98074da73bd3c3371c22ddba27a3e2`.
- `origin/codex/vegar-arendalsuka-medvirkende-import` — `f76de5a984501cb4d67e275c892d62ce3fc348c7`.
- `origin/codex/vegar-arendalsuka-stands-import` — `f76de5a984501cb4d67e275c892d62ce3fc348c7`.

Utelatt som beskyttet: `origin/main`.

Etterkontroll: 49 eksisterende arbeidstrær kontrollert; ingen endring i status, HEAD eller staged/unstaged diff under Git-oppryddingen.

## CellProtocolDocuments

Repo: `/Users/kjetil/Build/Digipomps/HAVEN/CellProtocolDocuments`.
Lokale grener: **31 → 27**. Nåværende gren: `codex/docs-cleanup-20260810`.
Fetch utført: 2026-09-18 09:39:55 CEST. Exitkode: 0.
Hentet `origin/main`: `357f2cfa0b3f1587a751c29f36540ab19f24c4a1`.

### Slettede lokale grener

| Gren | Full SHA før sletting |
| --- | --- |
| `codex/e3b-deterministic-lca` | `6b66c96775cc8f9cf5f3de4ef00af338aefdac16` |
| `codex/haven-robustness-report` | `308dff89272715a6dbef908fdd543b4b300c3d71` |
| `codex/integrate-main-staging-20260716` | `ec9f51876100e1818dd31703d2174dc6ca7856d9` |
| `codex/rwxs-docs-publish-20260716` | `7875bfb92b356867ead0bf6d416557d68f1ee213` |

### Beholdt fordi utsjekket / eksisterende arbeidstrær

Alle arbeidstrær i tabellen finnes fortsatt på disk. Alle navngitte grener er beholdt fordi de er utsjekket; detached HEAD har ingen utsjekket gren.

| Utsjekket gren / tilstand | Arbeidstre |
| --- | --- |
| `codex/docs-cleanup-20260810` (repoets nåværende) | `/Users/kjetil/Build/Digipomps/HAVEN/CellProtocolDocuments` |
| `codex/personal-data-risk-assessment-wp0-wp1-20260910` | `/Users/kjetil/.codex/worktrees/2973/CellProtocolDocuments` |
| `codex/agent-continuity-reference-20260910` | `/Users/kjetil/.codex/worktrees/30de/CellProtocolDocuments` |
| detached HEAD `be6839a7cabbdba6876afe79b2c29b1ce7333b7f` | `/Users/kjetil/.codex/worktrees/ea51/CellProtocolDocuments` |

Andre uttrykkelig beskyttede grener: `main`.
Øvrige grener beholdt uten bevist ancestry til main: **23**.

### Slettinger Git nektet

Ingen.

### Prune av arbeidstreregistreringer

**4 registreringer prunet** (8 → 4 registreringer). Eksisterende arbeidstrær er listet ovenfor.

Følgende kataloger manglet allerede; bare registreringene ble fjernet:

- `/private/tmp/cp-security-consumer/CellScaffold/CellProtocolDocuments`.
- `/private/tmp/cp-security-integration-docs`.
- `/private/tmp/cp-security-published-consumer/CellScaffold/CellProtocolDocuments`.
- `/private/tmp/relational-docs-commit`.

### Fjerngrenkandidater på origin – ikke slettet

Fersk grenliste lest 2026-09-18 09:39:57 CEST. **0 kandidater.**
Ingen ubeskyttede fjerngrener bestod ancestry-testen.

Utelatt som beskyttet: `origin/main`.

Etterkontroll: 4 eksisterende arbeidstrær kontrollert; ingen endring i status, HEAD eller staged/unstaged diff under Git-oppryddingen.

## HavenAgentD

Repo: `/Users/kjetil/Build/Digipomps/HAVEN/HavenAgentD`.
Lokale grener: **18 → 15**. Nåværende gren: `main`.
Fetch utført: 2026-09-18 09:40:55 CEST. Exitkode: 0.
Hentet `origin/main`: `551d37a4dfe587e1cf7ea7001729dc7013a9a068`.

### Slettede lokale grener

| Gren | Full SHA før sletting |
| --- | --- |
| `claude/mcp-idle-watchdog-20260826` | `4edff085009037eb02797de5b2b8ac1bf09d9b84` |
| `codex/swiftpm-development-overrides` | `819145224ca330ba1ea3d04ae6245497fb09eae3` |
| `pdd/agent-menylinje-og-varsler-v2` | `14aa660e5e2fb9e63ac071b52fb7f83506f28266` |

### Beholdt fordi utsjekket / eksisterende arbeidstrær

Alle arbeidstrær i tabellen finnes fortsatt på disk. Alle navngitte grener er beholdt fordi de er utsjekket; detached HEAD har ingen utsjekket gren.

| Utsjekket gren / tilstand | Arbeidstre |
| --- | --- |
| `main` (repoets nåværende) | `/Users/kjetil/Build/Digipomps/HAVEN/HavenAgentD` |
| `codex/prod-agentd-complete-20260918` | `/private/tmp/haven-prod-20260917/HavenAgentD` |
| `claude/agent-jobs-20260909` | `/Users/kjetil/Build/Digipomps/HAVEN/HavenAgentD/.worktrees/agent-jobs-20260909` |
| `claude/agentd-cancel-and-local-task-gate-20260908` | `/Users/kjetil/Build/Digipomps/HAVEN/HavenAgentD/.worktrees/agentd-cancel-and-local-task-gate-20260908` |
| `claude/ci-robusthet-20260911` | `/Users/kjetil/Build/Digipomps/HAVEN/HavenAgentD/.worktrees/ci-robust-20260911` |
| `pdd/agent-menylinje-og-varsler` | `/Users/kjetil/Build/Digipomps/HAVEN/HavenAgentD/.worktrees/menylinje-20260909` |
| `claude/varsler-og-behandlingssted-20260911` | `/Users/kjetil/Build/Digipomps/HAVEN/HavenAgentD/.worktrees/varsler-20260911` |
| `codex/entity-correspondence-linux-20260910` | `/Users/kjetil/Build/Digipomps/HAVEN/sprout/implementation/entity-correspondence/HavenAgentD` |
Øvrige grener beholdt uten bevist ancestry til main: **7**.

### Slettinger Git nektet

Ingen.

### Prune av arbeidstreregistreringer

**0 registreringer prunet** (8 → 8 registreringer). Eksisterende arbeidstrær er listet ovenfor.

### Fjerngrenkandidater på origin – ikke slettet

Fersk grenliste lest 2026-09-18 09:40:57 CEST. **2 kandidater.**

- `origin/codex/swiftpm-development-overrides` — `819145224ca330ba1ea3d04ae6245497fb09eae3`.
- `origin/pdd/agent-menylinje-og-varsler-v2` — `14aa660e5e2fb9e63ac071b52fb7f83506f28266`.

Utelatt som beskyttet: `origin/main`.

Etterkontroll: 8 eksisterende arbeidstrær kontrollert; ingen endring i status, HEAD eller staged/unstaged diff under Git-oppryddingen.

## Binding

Repo: `/Users/kjetil/Build/Digipomps/HAVEN/Binding`.
Lokale grener: **61 → 53**. Nåværende gren: `codex/havenagentd-sentinel-remote-intent-icon-20260804`.
Fetch utført: 2026-09-18 09:41:12 CEST. Exitkode: 0.
Hentet `origin/main`: `285dc235c050d96195a27200d7308b22f91a1df1`.

### Slettede lokale grener

| Gren | Full SHA før sletting |
| --- | --- |
| `codex/binding-native-route-isolation` | `1fe09943a141533cd8ca5aee239e3028146d69a0` |
| `codex/entity-chronicle-authority` | `e17eb05651fd3d20766ee30839cced1856c55e03` |
| `codex/fix-binding-red-main-20260805` | `1eb61feab1e1f5cfd10bc8fdb39f4e510bc869df` |
| `codex/haven-runtime-deeplinks` | `1a1e6c462033158850ea568f1bdeac7cf8a35664` |
| `codex/integrate-main-staging-20260716` | `6071ca11c207b537ce52ee4aafb686d9a4d955ae` |
| `codex/runtime-surface-scene-local` | `c0054360a364599cd472ab2094282a739baa5698` |
| `codex/salvage-binding-red-main-tests-20260810` | `056d74ad8e4fc0834e8a8f18761294abc0e06f47` |
| `codex/scanner-explicit-actions` | `1a1e6c462033158850ea568f1bdeac7cf8a35664` |

### Beholdt fordi utsjekket / eksisterende arbeidstrær

Alle arbeidstrær i tabellen finnes fortsatt på disk. Alle navngitte grener er beholdt fordi de er utsjekket; detached HEAD har ingen utsjekket gren.

| Utsjekket gren / tilstand | Arbeidstre |
| --- | --- |
| `codex/havenagentd-sentinel-remote-intent-icon-20260804` (repoets nåværende) | `/Users/kjetil/Build/Digipomps/HAVEN/Binding` |
| `codex/prod-binding-complete-20260918` | `/private/tmp/haven-prod-20260917/Binding` |
| detached HEAD `d175e0d8e82e3f5dc18392f4bc4b9ea63b615f4f` | `/Users/kjetil/.codex/worktrees/37ab/Binding` |
| `main` | `/Users/kjetil/.codex/worktrees/50d3/Binding` |
| `codex/binding-haven-app-rehabilitation-20260817` | `/Users/kjetil/.codex/worktrees/77e2/Binding` |
| `codex/binding-apple-m1-identifiers-origin-20260721` | `/Users/kjetil/.codex/worktrees/9abf/Binding` |
| detached HEAD `f6536c497b0a4c0a5b32531416bb3712708cf47e` | `/Users/kjetil/.codex/worktrees/f750/Binding` |
| `losen/visionos-sim-20260916` | `/Users/kjetil/Build/Digipomps/HAVEN/_worktrees/visionos-20260916/Binding` |
| `codex/condition-resolution-native-20260828` | `/Users/kjetil/Build/Digipomps/HAVEN/Binding/_wt-condition-resolution-20260828` |
| `claude/identity-link-flow-20260904` | `/Users/kjetil/Build/Digipomps/HAVEN/Binding/_wt-identity-link-flow-20260904` |
| `claude/parity-snapshot-20260904` | `/Users/kjetil/Build/Digipomps/HAVEN/parity/Binding` |
Øvrige grener beholdt uten bevist ancestry til main: **44**.

### Slettinger Git nektet

Ingen.

### Prune av arbeidstreregistreringer

**2 registreringer prunet** (13 → 11 registreringer). Eksisterende arbeidstrær er listet ovenfor.

Følgende kataloger manglet allerede; bare registreringene ble fjernet:

- `/private/tmp/binding-haven-integration-20260910.V2q7pH/Binding`.
- `/private/tmp/cp-security-published-consumer/Binding`.

### Fjerngrenkandidater på origin – ikke slettet

Fersk grenliste lest 2026-09-18 09:41:16 CEST. **3 kandidater.**

- `origin/codex/copilot-chat-packages-20260628` — `66901016dad3091628e6243f276533417a47da3d`.
- `origin/codex/entity-chronicle-authority` — `e17eb05651fd3d20766ee30839cced1856c55e03`.
- `origin/codex/integrate-entity-chronicle-main-20260717` — `5486b82037e31255f9058e190eb57b4c82b466ec`.

Utelatt som beskyttet: `origin/main`.

Etterkontroll: 11 eksisterende arbeidstrær kontrollert; ingen endring i status, HEAD eller staged/unstaged diff under Git-oppryddingen.

## HAVEN-Deploy

Repo: `/Users/kjetil/Build/Digipomps/HAVEN/HAVEN-Deploy`.
Lokale grener: **1 → 1**. Nåværende gren: `main`.
Fetch utført: 2026-09-18 09:41:27 CEST. Exitkode: 128.

Fetch-feil (ordrett):

```text
fatal: 'origin' does not appear to be a git repository
fatal: Could not read from remote repository.

Please make sure you have the correct access rights
and the repository exists.
```

Repoet er urørt. Prune, ancestry-vurdering og grensletting ble ikke forsøkt uten fersk fasit.

### Slettede lokale grener

Ingen.

### Beholdt fordi utsjekket / eksisterende arbeidstrær

Alle arbeidstrær i tabellen finnes fortsatt på disk. Alle navngitte grener er beholdt fordi de er utsjekket; detached HEAD har ingen utsjekket gren.

| Utsjekket gren / tilstand | Arbeidstre |
| --- | --- |
| `main` (repoets nåværende) | `/Users/kjetil/Build/Digipomps/HAVEN/HAVEN-Deploy` |

### Slettinger Git nektet

Ingen.

### Prune av arbeidstreregistreringer

**0 prunet.** Ikke forsøkt fordi fetch feilet.

### Fjerngrenkandidater på origin – ikke slettet

Ikke vurdert: ingen konfigurert origin og ingen vellykket fetch.

Etterkontroll: 1 eksisterende arbeidstrær kontrollert; ingen endring i status, HEAD eller staged/unstaged diff under Git-oppryddingen.
