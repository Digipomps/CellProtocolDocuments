# PLAN — ventende godkjenninger (G2)

Bygger på G1 og G1-GUI (godkjent 2026-10-10 18:10Z) og de anbefalte valgene i FORMAALSSPEC §6:
1a på Codex' «Oversikt» (HD-0210), 2a speilet på Mac-en kjører kommandoen (Kjetil 18:17Z: «Gjør anbefalt»), og 3: «implementer det også» — `SkeletonButton.urlKeypath` i skjelettformatet.

## Dette skal du gjøre

| Når | Hva | Hvorfor |
|---|---|---|
| Nå | Si G2 (eller «auto») | Ingen kode før planen er godkjent |
| Etter WP0 | Ja til en ny CellProtocol-tag med `urlKeypath` | CellScaffold og Binding pinner CellProtocol til en tag; Swift-fabrikken kan ikke sette feltet før taggen finnes |
| Før WP5 | Svar på Docker-data-spørsmålet fra 08.10 (16 GB) | Mac-porten trenger ~110 GiB ledig, nå 91 GiB. Samme blokk stopper HD-0210 |
| Før WP6 | Logg inn i arbeidsbenken på staging | Speilet skriver som din agent til `kjetil2-staging-work` |
| Etter WP6 | Se på listen på staging og si G3 | Akseptanse mot bildene (v2 med «Åpne») |

## Funnet etter G1 (påvirker planen)

- Speilet finnes allerede: `HAVEN-Deploy/tools/arbeidsbenk-speil/speil.py` skriver Losen-køen som WorkItem-kort (`speil-*`) gjennom HAVENAgentDs Workbench-bro. Jeg utvider det i stedet for å lage et nytt skript.
- Broen svarer `400 unavailable` på en ren lesing nå (målt 18:13Z i dag). Årsaken undersøkes av køjobbene i `agentd-bro-aarsak`-rekken (nå `d225-…-astra-funn-17` og `w16-…-port-14`, som kjører 18:13Z). Til broen virker, kan speilet bare tørrkjøre.
- `setStatus` på grenen godtar `decisionComment` bare som JA+done eller NEI+wont-do. «Merk som løst» sender derfor `done` uten kommentar.

## Arbeidspakker (1:1 mot bladformål)

| WP | purposeRef | Utfører | Hva | Test (§5) | Leveranse (§3) |
|---|---|---|---|---|---|
| WP0 | …row-link | Claude | CellProtocol, gren `claude/skeleton-button-url-keypath-20261010`: `SkeletonButton.urlKeypath` (init, CodingKeys, decode/encode) i `Sources/CellBase/Skeleton/SkeletonDescription.swift`. `SkeletonButtonResolutionSupport.resolve` leser `urlKeypath ?? "url"`, så dagens implisitte `url` virker som før. Dokumentasjon av feltet i skjelettkatalogen | test.vg.url-keypath-parity (CellBase-rundtur, CellApple-oppløsning) | draft-PR i CellProtocol |
| WP1 | …pointer, …fresh, …row-link | Claude | CellScaffold, ny gren `claude/venter-paa-deg-20261010` fra Codex' `d0456ccd`. `WorkItemOverview.decisionRow`: `sourceLabel` ← `source`, `deadlineText` ← `dueDate`, `whereText` ← evidence med `type: "hvor"`, `yesLabel`/`noLabel` ← labels `ja:`/`nei:`, `hasYes` false ved label `kun-peker`, `resolvedPayload`. Skjelettet i `WorkItemOverviewConfiguration` endres til det godkjente bildet. Tittelen blir «Venter på deg». `whereURL`/`hasURL` når «Hvor» er https. Web-rendereren (`Public/js/skeleton-runtime.js`) får `urlKeypath` i `resolveButtonSpec` og i validatoren; åpning går fortsatt gjennom `resolveNavigationURL` (bare https/loopback). Ingen nye felt lagres i cellen | test.vg.pointer, test.vg.stale, ny `WorkItemOverviewTests`: skjelettet fra fabrikken er kanonisk likt `skeleton/venter-paa-deg.skeleton.json` | images/*-v1.png |
| WP1b | …row-link | Claude | Binding: `SkeletonPresentationOverlayView` leser `urlKeypath ?? "url"`, og test i `SkeletonRendererParityTests`. CellProtocol-pinnen løftes når taggen finnes, begge steder (pbxproj og Package.resolved) | test.vg.url-keypath-parity (Binding) | draft-PR i Binding |
| WP2 | …complete | Claude | `speil.py --godkjenninger`: leser `hd status --json` (forkastet-banen) og lager kort `speil-godkjenning-<id>` med `kind: decision`, `assignee: kjetil`, merkelapper `ja:`/`nei:`, «Hvor» og `nextAction`. Avviste pakker vises ikke enkeltvis, men som ett samlekort. Trådforespørsler: et kort per post i `HAVEN-Deploy/_handoff/GODKJENNINGER/forespoersler.json`, som trådene skriver til | test.vg.coverage (tørrkjøring mot dagens kø: 81 → kort) | TESTRESULT.md#coverage |
| WP3 | …button-resolves | Claude | `speil.py --svar`: leser kortene. For kort som er satt til JA eller NEI siden sist, kjøres kommandoen fra en fast liste: `hd task set <HD> --status READY\|PREPARING --note "Køet på nytt av Kjetil fra arbeidsbenken <tid>"` og `hd gap decide --decision AVVIST\|INN`. Hver kommando kjøres én gang (føres i `sendt.json`). Ukjente kort nektes. Tørrkjøring er standard | test.vg.button-roundtrip, på en kopi av køen i scratch | TESTRESULT.md#button-roundtrip |
| WP4 | …complete | Claude | Skillen `haven-work-intake`: en tråd som venter på Kjetil, skriver en linje i `forespoersler.json` med tråd-lenke, filsti eller kommando som «Hvor» | inspeksjon | skill-diff |
| WP5 | quality.build-and-regression | kø (Mac) | Bygg, fokusert XCTest, `ci/run-tests.sh` og Playwright-oversikten på grenen, med samme port som c66 | test.build, test.regression | TESTRESULT.md#build |
| WP6 | gui.parity | Claude + kø | Draft-PR mot main (inneholder Codex' tre commits, med kreditering). Etter at broen virker og du er logget inn: kjør `speil.py --godkjenninger --skriv` mot staging, og ta skjermbilde ved siden av referansen | test.gui.parity | ACCEPT.md#parity, draft-PR |

## Stopp-regler

- Jeg endrer ikke eksisterende tester på Codex' gren. Må en endres, spør jeg deg først.
- Er en port rød, kjører jeg den ikke på nytt uten at du sier det.
- Ingen merge, ingen deploy, ingen push til Codex' gren. Staging-deploy av denne endringen går gjennom kø-trådens release-kjede når du sier det.
- Kjører en Codex-jobb på HD-0210 når jeg starter WP1, stopper jeg og skriver i `_losen-queue/KOORDINERING.md` før jeg fortsetter.
