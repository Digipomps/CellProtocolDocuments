# Oppdrag til Codex: spillverksted, runde 2

Fra Claude, 2026-10-14. Runde 1 (PR #312) er merget til `main`.

- Plan: `../PLAN.md` (WP-B4, WP-B5, WP-A3)
- Formål: `../FORMAALSSPEC.md` §1. Alle formålene står nå i `Book/haven_purpose_knowledge_base_v0.json` som `candidate`.
- Tester: `../FORMAALSSPEC.md` §5
- Regler: som i `README.md` (runde 1), avsnittet «Regler». Les det først.

## Grunnlag

- **Worktree:** `/Users/kjetil/Build/Digipomps/HAVEN/tmp/codex-spillverksted-r2`, gren `codex/spillverksted-runde2` fra `origin/main`. Jobb bare der.
- **Fra runde 1 på main:** `Sources/App/Cells/GameWorkshop/` (`GameProjectCell`, `GameToolLibraryCell`, `GameWorkbench`), `Sources/App/Controllers/VaporGameSandbox.swift` og testene `GameProjectCellTests`, `GameSandboxTests`, `GameToolLibraryCellTests`.
- **Profilkontrakten:** `../contract/workbench-assistant-profile.v0.schema.json` og spillverkstedets profil `../contract/game-workshop.profile.v0.json`.

## Lært i runde 1 (CI fant disse; Codex kunne ikke bygge lokalt)

- `try await` kan ikke stå til høyre i `? :`. Bruk if/else.
- `registerSet`-handlere kaster ikke. Pakk `try await` i do/catch.
- `FlowElement(content:)` tar `.object(Object)`, ikke en `ValueType`.
- En fremmed `set` blir avvist ved at tilgangslaget kaster før handleren kjører. Negative tester må godta et kast (`try?`), ikke bare et `ok: false`.
- Kan du ikke bygge lokalt (kapasitetsporten), push og les CI. Kompileringsfeil står etter `KOMPILERINGSFEIL:` nederst i jobbloggen.

## Oppdrag

### WP-B4: forslag går som plan, mennesket bestemmer

**Formål:** `purpose://candidate.workbench-assistant.propose-human-decides`

- Et forslag fra hjelperen blir en `GroundedActionPlan` (se `Sources/App/Support/ExecutablePurposeGrounding.swift`) med målet `cell:///GameProject#project.propose`. Hjelperen kaller aldri `project.applyProposal` selv.
- `project.applyProposal` og `project.revert` krever et brukerklikk: payloaden må ha et bekreftelsesmerke som bare Porthole-knappen setter (for eksempel `confirmedBy: "user-click"` sammen med en engangs-nonce fra `project.preview`). Velg mekanismen som allerede brukes for bekreftelser i `PersonalCopilotCloudStore.swift`, hvis det finnes en.
- Målcellen sjekker tilgang på nytt ved hvert kall. Det gjør den allerede, så ikke legg til en ny vei utenom.
- **Test (T-B4):** Disse tre skal avvises: endring uten klikk (ingen eller feil nonce), feil bruker og ukjent formål (`purposeRef` utenfor `purpose://candidate.game-workshop.*`). Ett positivt tilfelle: med klikk går endringen gjennom.
- **Bevis:** `../TESTRESULT.md#auth`

### WP-B5: hjelperen lastes fra en profil

**Formål:** `purpose://candidate.workbench-assistant.reusable-profile` (G2-beslutning 3)

- Legg et profilregister ved siden av `switch helperRoute.keypath` (`Sources/App/Cells/PersonalCopilot/PersonalCopilotCloudStore.swift`, linje 5087 på main). De eksisterende hjelperne i switchen flyttes ikke.
- Registeret laster profiler (JSON) som valideres mot `workbench-assistant-profile.v0`. Legg skjemaet og `game-workshop.profile.v0.json` som ressurser i `Sources/App/Resources/GameWorkshop/`, og lag en liten profil til for Developer Workbench (`developer-workbench.profile.v0.json`, anker `purpose://project-work` eller nærmeste node i Book 23).
- En profil gir hjelperen formålsgren, bibliotek, forhåndsvisning, tillatte handlinger, tone og eskaleringstak. `allowedActions` er en hvitliste: en handling utenfor lista blir avvist før den sendes.
- **Test (T-B5):** begge profilene lastes av samme motor; en ugyldig profil (manglende `allowedActions`, ukjent `preview.adapter`) avvises med en lesbar feil; en handling utenfor `allowedActions` avvises.
- **Bevis:** `../TESTRESULT.md#profil`

### WP-A3: Kjetils oversikt

**Formål:** `purpose://candidate.game-workshop.learning.mentor-oversight`

- `GameProjectCell` lagrer en hendelseslogg per prosjekt: hvert forslag (tittel, `why`, tidspunkt) og hva som skjedde med det (tatt i bruk, forkastet, rullet tilbake). Den finnes ikke i dag; versjonene alene viser ikke de forkastede forslagene.
- Ny lese-keypath `mentor.overview` med siste økt først: prosjekt, antall forslag, tatt i bruk/forkastet og nivå fra profilens `levels` hvis det er satt. Tilgang `r---` for eieren og for en eksplisitt mentor-grant. Barnets egen identitet er eier.
- Legg en referanse i Developer Workbench (`Sources/App/Cells/WorkItems/DeveloperWorkbenchConfiguration.swift`) til en liten liste over `mentor.overview`. Husk at `HavenWorkbenchConfigurationTests` sjekker settet av referanse-labels og må oppdateres.
- **Test (T-A3):** enhetstest som lager to økter med forslag, og sjekker at `mentor.overview` viser den siste først med riktige tall, og at en fremmed uten grant får avslag. Målingen «Kjetil finner forrige økt på under ett minutt» tar Kjetil selv; den står i `ACCEPT.md`.
- **Bevis:** `../TESTRESULT.md#mentor`

## Ikke i denne runden

- **WP-F2 og WP-F1 (publisering):** F2 bygger på `PDD_godkjenninger-i-arbeidsbenken_2026-10-07`, der G1 ikke er gitt. F1 kommer etter F2. Begge venter.

## Når du er ferdig

1. Legg nye testsuiter i `ci/test-filter.txt` og kjør `ci/test-suite-coverage.sh` og `ci/check-value-literals.sh`.
2. Push `codex/spillverksted-runde2` og åpne en utkast-PR mot `main` med `gh pr create --draft`. Ikke merg.
3. Skriv `codex-runde2-status.md` i denne mappa underveis og til slutt: hva som er gjort, testene, PR-lenken og hva som er blokkert.
4. Legg testutdata i `../TESTRESULT.md` under ankrene over.
