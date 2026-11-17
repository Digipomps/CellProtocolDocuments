# AGENTMENY – vindusfeil, 2026-09-23

Status: blokkert før UI-førmålingen. Dagens kode er bygget og pakket. Ingen rettelse er gjort eller funksjonelt verifisert. Oppgaven er ikke ferdig.

## Miljø og faktisk installasjon

- macOS 27.0 (26A428), Apple Swift 6.4.
- `/Users/kjetil/Build/Digipomps/HAVEN/HavenAgentD` står på `main`, `ba1489554bdf8b27f10ef0fdc8fa727689fa0c98`, med eksisterende lokale endringer. Disse er ikke endret.
- `origin/main` og direkte `git ls-remote origin refs/heads/main` viste `3a28d65b9dd08e5acb23682db0631e6d7a6e7b05`.
- Eget arbeidstre: `/Users/kjetil/Build/Digipomps/HAVEN/_worktrees/HavenAgentD-agentmenu-window-20260923`, gren `codex/agentmenu-window-20260923`, fra denne revisjonen.
- `launchctl print gui/501/io.digipomps.haven.agentmenu` viste kjørende PID 71589 og program `/Users/kjetil/Applications/HAVEN Agent.app/Contents/MacOS/HAVEN Agent`.
- Denne appens `Info.plist` har `CFBundleIdentifier=io.digipomps.haven.agentmenu` og `LSUIElement=true`.
- Binærens Mach-O-UUID er `22B398C2-6A42-31D1-8822-44F7BFBAE1D4`, identisk med release-bygget i det rene arbeidstreet `/Users/kjetil/Build/Digipomps/HAVEN/HavenAgentD/.worktrees/main-20260922` på samme `origin/main`-revisjon. SHA-256 er ulik etter ulik kodesignering; UUID-samsvaret er dokumentert, ikke et påstått bit-for-bit-samsvar.
- Den eldre `/Applications/HAVEN Agent.app` har UUID `432DF647-3E1E-3217-B3DF-8EC8D3CEF5DE`; launchd peker ikke dit.

Rådata: `/Users/kjetil/Build/Digipomps/HAVEN/HAVEN-Deploy/_handoff/AGENTMENY/inventory-2026-09-23.json`.

## Hypotesen

Premisset «SwiftPM-binær uten app-bundle» stemmer ikke for den kjørende installasjonen. `Packaging/menu-app/make_app.sh` på den kontrollerte `origin/main` genererer både app-bundle, `Info.plist` og `LSUIElement=true`. At repoet ikke inneholder en fil med navnet `Info.plist`, utelukker altså ikke en generert plist.

Det er fortsatt uavklart om manglende appaktivering forklarer vindusfeilen. Ingen vindusmåling er gjennomført ennå. Fravær av `NSApp.activate` i koden beviser ikke årsaken.

Apple dokumenterer at `.accessory` kan aktiveres programmatisk uten å vises i Dock, mens `.regular` vises i Dock: [NSApplication.ActivationPolicy](https://developer.apple.com/documentation/appkit/nsapplication/activationpolicy-swift.enum). En eventuell rettelse må prøves med dette skillet; permanent `.regular` er ikke innført.

## Førmåling og verifikasjon

| Tilfelle | Målt resultat |
| --- | --- |
| Dagens kode: klikk «Åpne adminflate…» | Ikke gjennomført; UI-tilgang avvist. |
| Fantes adminvinduet allerede / ble det opprettet? | Ukjent. |
| Lå vinduet bak et annet program? | Ukjent. |
| Første åpning etter rettelse | Ikke prøvd; ingen rettelse ennå. |
| Gjenåpning etter lukking | Ikke prøvd. |
| Åpning mens annet program har fokus | Ikke prøvd. |
| Dock-oppførsel | Installasjonen har `LSUIElement=true`; faktisk runtime-policy og Dock-oppførsel er ikke målt. |

## Tilgangs- og byggbegrensninger

- Datamaskinverktøyet avviste `cua.getApp('/Users/kjetil/Applications/HAVEN Agent.app')` med `Computer Use was not approved to use HAVEN Agent`. Brukeren er bedt om å gi tilgang. Avvisningen er ikke et funn om produktet.
- `ps` ble blokkert med `operation not permitted`.
- `osascript`-spørring til System Events feilet med `-10827` før vindusmåling.
- Skjermbildeferdighetens preflight rapporterte at skjermopptakskontrollen er blokkert i sandbox. Eskalering er ikke tilgjengelig i denne økten. Første preflight traff dessuten en gammel `/usr/local/bin/python3` med `Bad CPU type`; nytt forsøk med `/usr/bin` først i PATH avklarte sandbox-blokkeringen.
- Første byggforsøk ble stoppet av uskrivbar standard-modulcache. Cacheplassering ble flyttet til `/private/tmp`.
- Neste forsøk ble stoppet av SwiftPMs nestede `sandbox-exec`. `--disable-sandbox` slår av SwiftPMs ekstra sandbox; Codex-sandboxen er fortsatt aktiv.
- `swiftbuild` kom til kompilering, men Clang fikk ikke opprette en midlertidig fil. Nytt forsøk med `--build-system native`, fire byggejobber og eksplisitt `TMPDIR` under `/private/tmp` fullførte uten feil på 205,87 sekunder. Eksisterende Sendable-advarsler i `ChallengeNotifier.swift` og varsel om at native-byggsystemet er utfaset ble ikke endret; de ligger utenfor denne oppgaven.

Bygglogger ligger i `/Users/kjetil/Build/Digipomps/HAVEN/HAVEN-Deploy/_handoff/AGENTMENY/`, med navn `build-before*-2026-09-23.log`.

Vellykket byggkommando, kjørt i det nye arbeidstreet (alle cache- og tempmapper var opprettet først):

```sh
TMPDIR=/private/tmp/agentmenu-build-tmp-20260923 \
CLANG_MODULE_CACHE_PATH=/private/tmp/agentmenu-clang-cache-20260923 \
SWIFTPM_MODULECACHE_OVERRIDE=/private/tmp/agentmenu-swift-module-cache-20260923 \
swift build --disable-sandbox --build-system native -j 4 -c release \
  --product haven-agent-menu --disable-automatic-resolution \
  --cache-path /private/tmp/agentmenu-swift-cache-20260923 \
  --config-path /private/tmp/agentmenu-swift-config-20260923 \
  --security-path /private/tmp/agentmenu-swift-security-20260923
bash Packaging/menu-app/make_app.sh release
```

Det uendrede nybygget ligger i `/Users/kjetil/Build/Digipomps/HAVEN/_worktrees/HavenAgentD-agentmenu-window-20260923/.build/release/HAVEN Agent.app`. Det er kun pakket, ikke startet eller installert. Den løse nybygde binæren har SHA-256 `09943a407f943d3834ea4243aa0229727782a0837dbadd13bf806d6808e816a6` og Mach-O-UUID `0BC6EA2B-AC13-3C00-837C-68DFEF13D9D3`.

`git status --short` i dette arbeidstreet er tomt; `git diff --check` passerer. Ingen av disse sjekkene er vindusverifikasjon.

## Rettelse og bilde

Ingen produktkode er endret. Kravet om å måle hypotesen før rettelse er beholdt.

Intet bevisbilde er tatt. Det finnes derfor ingen påstand om at vinduet virker. Bildet skal lagres i `/Users/kjetil/Build/Digipomps/HAVEN/HAVEN-Deploy/_handoff/AGENTMENY/` etter faktisk UI-verifikasjon.

Ingen commit, push eller installasjonsendring er utført.

## Fortsettelse når UI-tilgang er gitt

1. Observer den installerte menylinjeappen og noter vindusliste, synlighet, aktiv app og Dock-tilstand før/etter menyklikk. Ikke aktiver appen via et hjelpeverktøy før førmålingen, siden det kan maskere feilen.
2. Kjør det uendrede nybygget ovenfor kontrollert, uten forveksling med den installerte prosessen. Gjenta menyklikket og avgjør om adminvinduet blir opprettet, men ligger bak, eller aldri blir opprettet.
3. Velg minste rettelse ut fra målingen. Det er ikke besluttet at `.regular` skal innføres. Bevar menylinjeproduktets Dock-oppførsel.
4. Bygg rettelsen, test første åpning, gjenåpning etter lukking og åpning mens et annet program har fokus. Lagre faktisk skjermbilde med dato i avtalt artefaktmappe og oppdater denne rapporten med observasjoner og berørte kildefiler.
