# Handoff: correspondence-endringene inn i main, i riktig rekkefølge

Skrevet av Losen 2026-09-09. Utfører: Codex eller integrator.
Godkjenner: Kjetil.

---

## §0 Formål

**Formålet er ikke «få koden inn i git». Formålet er «funksjonalitet er
deployet og virker».**

Det skillet er hele grunnen til at dette dokumentet finnes. Commiten
`ba14895` i HavenAgentD ble målt mot en aktivitet — «land the correspondence
MCP» — og aktiviteten ble utført. Formålet ble ikke oppfylt, fordi commiten
ikke bygger. Hadde verifikatoren vært formålets («HavenAgentD bygger og består
sine tester fra en ren utsjekk»), ville commiten strøket på sin egen port.

| | |
|---|---|
| **Outcome** | `origin/main` i CellProtocol og HavenAgentD inneholder correspondence-arbeidet, og en ren utsjekk av hver bygger og består testene. |
| **Successsignal 1** | `git clone` av HavenAgentD på ny revisjon, uten `swift package edit`, `swift build` exit 0. |
| **Successsignal 2** | Alle correspondence-tester grønne mot den pinnede CellProtocol-revisjonen, ikke mot et arbeidstre. |
| **Successsignal 3** | Hver commit som når `origin/main` er grønn **alene** — ikke bare tuppen. |
| **Verifikator** | WP-6 nedenfor. Kjørt av et menneske, ikke av en agent. |

---

## §1 Hvorfor det fortsatt er ucommittet kode

Tre årsaker, i rekkefølge etter hvor mye de forklarer.

### 1.1 Commitene ble målt mot aktivitet, ikke mot formål

`ba14895` «Land the correspondence MCP as a CellProtocol client» landet tolv
filer under `Sources/HavenCorrespondenceMCP/`. Den landet **ikke** endringen i
`Sources/HavenAgentRuntime/AgentIdentityStore.swift` som de tolv filene er
avhengige av. De to nye API-ene der — `loadOrCreate(...)` og
`loadExisting() async throws -> AgentIdentityMaterial?` — finnes bare i
arbeidstreet.

Resultatet er en commit som ser fullført ut og ikke bygger. Ingen port fanget
det, fordi ingen port var definert. Dette er `lesson.plan-instead-of-delivery`
i speilvendt form: her ble en delleveranse forvekslet med leveransen.

### 1.2 `swift package edit` skjuler feilen

`HavenAgentD/Packages/cellprotocol` er en aktiv edit-symlink til det lokale
CellProtocol-treet, satt 7. sept. 21:09. Alle lokale bygg ser derfor de
**ucommitterte** CellProtocol-endringene. Ingenting i den daglige arbeidsflyten
tvinger fram oppdagelsen av at den committede revisjonen ikke holder.
Nattjobben flagget nøyaktig dette; feilen overlevde flaggingen.

Beslektet lærdom: `L-2026-08-26-local-package-override-drift`.

### 1.3 Arbeidstreet er delt mellom mange parallelle oppgaver

Målt i dag:

| Repo | Branch | Skitne stier |
|---|---|---|
| CellProtocol | `pdd/tillitspakke-agentflaate` | 35 |
| HavenAgentD | `main` | 18 |
| CellScaffold | `pdd/tillitspakke-agentflaate` | 183 |

I CellProtocol ligger correspondence side om side med lokalisering, media,
audio, kvitteringer og tillitspakke — minst fem oppgaver i samme tre. Hver tråd
har committet sin egen skive og latt resten ligge. Krysskoblinger mellom
skivene blir da systematisk ucommittet, fordi ingen av trådene eier dem.

Dette er ikke en tilfeldig slurv. Det er den forutsigbare konsekvensen av at
flere agenter arbeider i ett delt arbeidstre uten en port som krever grønt bygg
per commit.

---

## §2 Målt tilstand, 2026-09-09 kl. 09:20Z

Alt nedenfor er lest, ikke husket. Kommandoen står i parentes.

**CellProtocol** (`git -C CellProtocol log/status`)
- branch `pdd/tillitspakke-agentflaate`, HEAD `4096760`
  «feat(crypto): add attachmentStreamV1 with authenticated chunk finalization»
- `origin/main` = `8c09560`, datert **1. september**. Main har ikke beveget seg
  på åtte dager.
- Correspondence-arbeidet ligger på en **annen oppgaves branch**
  (`pdd/tillitspakke-agentflaate`). Å lande det via den branchen drar
  tillitspakke-arbeidet med seg.

**HavenAgentD**
- branch `main`, HEAD `ba14895`
- `origin/main` = `cccc97c`, datert **27. august**
- `git log origin/main..HEAD` gir **nøyaktig én** commit: `ba14895`.
- `ba14895` bygger ikke. Årsak i §1.1.
- Fordi den er **upushet**, kan den rettes uten at en ødelagt commit noen gang
  når origin. Dette er den viktigste enkeltopplysningen i dokumentet.

**Ucommittet i HavenAgentD som hører til correspondence**
- `M Sources/HavenAgentRuntime/AgentIdentityStore.swift` ← byggblokkeringen
- `M Sources/HavenAgentRuntime/AgentConfig.swift`
- `M Sources/HavenAgentRuntime/AgentRuntime.swift`
- `M Tests/HavenAgentRuntimeTests/AgentConfigTests.swift`

**Ucommittet i HavenAgentD som IKKE hører til correspondence**
- `AgentJobModels.swift`, `JobStore.swift`, `JobCompletionService.swift`,
  `Contracts/agent-job-*.json`, `Docs/AgentJobs.md`,
  `Tests/.../JobCompletionServiceTests.swift`

  Dette er jobbadministrasjons-arbeidet — en annen tråds oppgave, og etter alt
  å dømme nettopp det Kjetil har bedt om at skal eies av HAVENAgentD. **Det
  skal ikke inn i denne rekkefølgen.** Egen leveranse, egen port.

---

## §3 Den ufravikelige regelen

> **Ingen commit som brekker noe får nå `origin/main`. Ikke som tupp, og ikke
> som mellomliggende commit.**

Praktiske følger:

1. En commit som ikke bygger alene, pushes ikke — den rettes før push.
   `ba14895` er upushet og skal derfor **amendes**, ikke etterfølges av en
   fikscommit. En grønn tupp over en rød commit oppfyller ikke regelen.
2. Verifikasjon skjer mot **pinnet revisjon i en ren utsjekk**, aldri mot
   arbeidstreet. Et grønt bygg under `swift package edit` er ikke bevis.
3. Rekkefølgen er nedenfra: CellProtocol før HavenAgentD, fordi HavenAgentD
   pinner CellProtocol. Motsatt rekkefølge er umulig, ikke bare uklok.
4. Hvis en port er rød: stopp. Ikke gå videre og ikke rull tilbake noe som
   allerede er grønt. Rapporter hvilken port, med utdata.

---

## §4 Rekkefølge

Hver pakke har én verifikator. Ingen pakke starter før forrige er grønn.

### WP-1 — Skill correspondence fra tillitspakke-arbeidet (CellProtocol)

Enumerer først, ikke anta:

    git -C CellProtocol fetch origin
    git -C CellProtocol log --oneline origin/main..pdd/tillitspakke-agentflaate

Cut en ny branch **fra `origin/main`**, ikke fra lokal main
(`L-2026-08-28-stale-local-main-branch-cut`), og ta med kun de commitene som
hører til correspondence — i dag kjent: `a00e3a0` (CorrespondenceCell,
envelope-typer, Agreement-maler, kontraktstester) og `4096760`
(`attachmentStreamV1`). Bekreft listen mot enumereringen; ikke stol på mine to.

`M Package.swift` i arbeidstreet må vurderes: hører endringen til
correspondence eller til en annen oppgave? Ta bare det som hører hit.

**Verifikator WP-1:** ren utsjekk av den nye branchen, `swift build
--build-tests` exit 0, og correspondence-testene grønne. Nattens miljøfelle
gjelder: `swift test` feiler på arkitektur og ser ut som en testfeil uten å
være det — bruk `arch -arm64`, eventuelt `arch -arm64 xcrun xctest` direkte.
Dokumenter kommandoen som faktisk ga exit 0.

### WP-2 — Push CellProtocol-branchen og få den inn i main

PR mot `origin/main`. Ingen force. Når den er merget, noter revisjonen — den er
inndata til WP-3.

**Verifikator WP-2:** `git ls-tree` på den mergede revisjonen viser
correspondence-filene, og CI er grønn.

### WP-3 — Rett `ba14895` i HavenAgentD

`ba14895` er upushet og eneste commit foran origin/main. Amend den slik at den
inneholder alt den er avhengig av:

- `Sources/HavenAgentRuntime/AgentIdentityStore.swift` (`loadOrCreate`,
  `loadExisting`)
- `AgentConfig.swift`, `AgentRuntime.swift`, `AgentConfigTests.swift` i den grad
  correspondence faktisk trenger dem — verifiser ved å bygge, ikke ved å anta

**Ikke** ta med jobbadministrasjonsfilene fra §2. De er en annen leveranse.

**Verifikator WP-3:** `git log origin/main..HEAD` gir fortsatt én commit, og
den commiten bygger alene i en ren utsjekk.

### WP-4 — Opphev edit-tilstanden og oppdater pinnen

Rekkefølgen her er ikke valgfri:

1. `swift package unedit cellprotocol`
2. sett `Package.swift` sin `revision:` til revisjonen fra WP-2
   (i dag `4107d27a…`, som er fra før correspondence fantes)
3. `swift package resolve` i en **ren klone**, ikke i arbeidstreet
   (`L-2026-08-26-local-package-override-drift`)
4. gjenopprett `Package.resolved` byte for byte hvis SwiftPM skriver den om
   utenfor det som er tilsiktet; dokumenter med SHA-256 før/etter

**Verifikator WP-4:** `Packages/` er tom, ingen symlink, og
`swift build --build-tests` exit 0 mot pinnen.

### WP-5 — Full testkjøring mot pinnen

Alle 28: 7 i CellProtocol, 21 i HavenAgentD
(`CorrespondenceHostedCellTests`, `CorrespondenceMCPTests`,
`AgentIdentityStoreTests`). Mot pinnen, ikke mot arbeidstreet.

**Verifikator WP-5:** kjørt/passert/feilet per suite, med faktisk utdata. Én
feilende test stopper rekkefølgen.

### WP-6 — Kjetils akseptanse

Kjetil kjører selv, uten agent i sløyfen:

    git clone <HavenAgentD> /tmp/verify && cd /tmp/verify && swift build

Bygger den, er formålet i §0 oppfylt så langt det gjelder kode. Bygger den
ikke, er noe i WP-1..5 feil rapportert, og det er da det skal oppdages —
ikke i deploy.

### WP-7 — Push HavenAgentD

Først etter WP-6. PR mot `origin/main`.

---

## §5 Utenfor omfang

- **Deploy til staging.** Egen leveranse. `HD-0006` står
  `HANDOFF_REQUIRED`: SSH nådde staging, men inventarlesningene ble blokkert
  med `Operation not permitted`. Invitasjoner og enrollment er **ikke målt**.
- **Jobbadministrasjon** (`AgentJobModels`, `JobStore`,
  `JobCompletionService`, `Contracts/agent-job-*`). Egen leveranse.
- **CellScaffold.** 183 skitne stier, og ingenting der er en avhengighet for
  §0. Rør det ikke i denne rekkefølgen.
- **Vedleggstransport.** `attachmentStreamV1` er kryptolaget alene. Manifest,
  grants og MCP-verktøy kommer etter at §0 er oppfylt.

---

## §6 Krever Kjetil før start

1. **Push-godkjenning.** WP-2 og WP-7 publiserer til `origin`. Jeg har ikke
   gjort noe av det og gjør det ikke uten ditt ord.
2. **Amend eller fikscommit?** Jeg anbefaler amend av `ba14895`, siden den er
   upushet og regelen i §3 da holder uten unntak. Vil du heller ha historikken
   bevart med en fikscommit, sier du fra — da får main en rød mellomcommit, og
   det må være et bevisst valg.
3. **Hvem utfører?** Codex kan gjøre WP-1, WP-3, WP-4, WP-5. WP-2, WP-6 og WP-7
   bør være dine eller integratorens, siden de publiserer eller aksepterer.

---

## §7 Lærdom som skal registreres uansett utfall

- En commit hvis melding beskriver en aktivitet («land X») og ikke et formål
  («X bygger og virker»), har ingen port. Foreslått forebygging som
  `derivedTest`: **ingen commit til et repo med aktiv `swift package edit` uten
  et parallelt byggbevis mot pinnet revisjon.**
- `swift package edit` skjuler manglende commits systematisk. Foreslått
  forebygging: edit-tilstand skal være synlig i preflight og blokkere push.
