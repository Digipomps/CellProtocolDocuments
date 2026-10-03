# PLAN — agent menylinje og varsler

Gren: `pdd/agent-menylinje-og-varsler` i `HavenAgentD`, fra `main` `ba1489554bdf8b27f10ef0fdc8fa727689fa0c98`.
Worktree: `HavenAgentD::.worktrees/menylinje-20260909` (opprettet fra macOS —
`lesson.worktree-created-from-vm-has-unusable-gitdir`).
Det delte treet står på `main` med 19 skitne oppføringer fra AgentJobs-arbeidet. Ikke rørt.

Utfører er Claude med Codex som byggearm, med mindre annet står. Bygg og tester kjøres
**detached med full tilgang**, aldri som køjobb (`lesson.codex-workspace-write-cannot-build-cellscaffold`).
Ingen arbeidspakke er levert før et faktisk bygg er grønt (`lesson.syntax-check-reported-as-delivered`).

| WP | Bladformål | Hva den lager | Test som må bli grønn | Utfører |
|---|---|---|---|---|
| WP0 | — (pakke) | Målt baseline av `HavenAgentD` på ren `main`: bygg + hele testmengden | `test.build`, `test.regression` (baseline) | Codex, detached |
| WP1 | `challenge-inbox` | `contract/agent-challenge_v1.json` + fixtures (positive, negative, ulesbar kilde) | `test.challenge.inbox-shape` | Claude |
| WP2 | `challenge-inbox`, `absence-is-explained` | `ChallengeInboxService` i `HavenAgentRuntime`: samler kilder, og gir **`unreadable` med grunn** når en kilde ikke kan leses | `test.challenge.sources` | Claude |
| WP3 | `answerable-where-seen` | Kontrollbro: `GET /challenges`, `POST /challenges/:id/respond`, `GET /status/summary`. Svar går gjennom `RemoteIntentReview`s egen godkjenningsfunksjon | `test.challenge.answer-uses-real-path` | Claude |
| **WPC1** | — | **Commit av WP1–WP3 så snart bygget er grønt** (`lesson.branch-is-empty-after-eight-work-packages`) | `test.branch-has-commits` | Codex |
| WP4 | `status-at-a-glance` | Nytt appmål `HavenAgentMenu` (`LSUIElement`, `MenuBarExtra`): ikon i tre tilstander, meny med «Trenger deg» og «Nå» | `test.menu.three-states`, `test.menu.unknown-is-not-ok` | Claude |
| WP5 | `admin-surface` | Adminvindu med hele `AgentStatusReport`, challenge-liste med svarknapper, lenker til `/onboard` og scaffold-admin | `test.menu.admin-window-shows-report` | Claude |
| WP6 | `notification-when-needed`, `no-secrets-in-notification` | `UNUserNotificationCenter`-kategorier med handlinger, formålsfilter, dedup, hemmelighetsfilter i tekst | `test.notify.purpose-gate`, `test.notify.no-duplicates`, `test.notify.no-secrets` | Claude |
| **WPC2** | — | Commit av WP4–WP6 ved grønt bygg | `test.branch-has-commits` | Codex |
| WP7 | — | Kjøre appen på Kjetils Mac, skjermbilder av menyen i tre tilstander, adminvinduet og et **faktisk varsel i varslingslisten** | `test.notify.appears-in-center`, L5, L6 | Codex på macOS |
| WP8 | — | LaunchAgent + pakking/notarisering av appen. **Utenfor G3** hvis Kjetil ikke sier noe annet | — | senere |
| WP9 | pakke | Docs i samme endring (`Docs/`, `README`), STATUS, ACCEPT | `test.docs-updated`, `test.status-current` | Claude |

## Rekkefølge og avhengigheter

WP1 → WP2 → WP3 → WPC1 → WP4 → WP5 → WP6 → WPC2 → WP7 → WP9.
WP4 kan ikke testes mot ekte data før WP3 svarer, men kan bygges mot fixtures fra WP1.

## Risiko som er kjent på forhånd

1. **App-bundle i SwiftPM.** `swift build` lager en kjørbar, ikke en `.app`. Menylinje og
   `UNUserNotificationCenter` krever bundle med bundle-ID. Løses ved at WP4 også lager et lite
   `Packaging/menu-app/` som pakker den kjørbare i en `.app` med `Info.plist` (`LSUIElement`),
   eller ved et Xcode-mål. Hvilken vei som ble valgt skrives i TESTRESULT — ikke antatt her.
2. **Varselsamtykke.** Første kjøring spør brukeren. Nektes det, skal appen si det i menyen,
   ikke feile stille. Egen rad i `test.menu.unknown-is-not-ok`.
3. **Scaffold-køen kan ikke leses ennå.** `entity:digipomps`/`entity:dimy` finnes ikke på staging.
   Da er riktig oppførsel `unreadable` med grunn — det er nettopp det WP2 måles på.
4. **Usignert app.** Gatekeeper vil klage første gang. Det er WP8, og det skal stå i det Kjetil får se.
