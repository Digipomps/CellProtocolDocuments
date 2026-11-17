# handoff — testmatrise og APNs-chat

Last verified against files: 2026-10-06. «Planlagt» betyr at scriptet ikke finnes ennå.

## Regler som gjelder alle script her

- Dry-run er standard; `--go` gjør noe. Ingen forklaring på samme linje som en kommando.
- Git som committer eller pusher kjøres på Macen (VM-en har ingen git-identitet og ingen SSH-nøkler). Fra VM-en: bare objektlesende git mot en revisjon, aldri `status`/`add`/`commit` mot `$HOME/mnt`.
- Script startes ved at Kjetil dobbeltklikker `.command`-filen i Finder — eller Claude gjør det via Finder med computer use. Kontroller at raden er riktig før dobbeltklikk (listen flytter seg når nye filer kommer).
- Mac-ens `/usr/local/bin/python3` virker ikke (x86 uten Rosetta). Script velger `/usr/bin/python3`.
- Grønn-port: bare siste «Executed»-linje, POSIX `case` (se `lesson.green-gate-must-read-the-last-summary-line`).
- Aldri `pkill -f <mønster>`.

## Rekkefølge

| # | Script | Hva | Utfall å forvente | Status |
|---|---|---|---|---|
| 1 | `handoff/snapshot-alle.sh` (+ `start-snapshot-alle.command` tørr, `start-snapshot-alle-go.command` skarp) | wip-snapshot av ucommittet arbeid i fire repoer uten å røre checkout | tørrkjøring viser per repo «går med / holdt ute»; `--go` gir «uberørt: JA» og lik lokal/origin-hash | **kjørt 04.10** (se STATUS.md) |
| 2 | `handoff/baseline.sh` | ren eksport av origin/main for CellProtocol, CellScaffold, Binding (`git archive`), bygg + full test, tre ganger om noe er rødt | `TESTRESULT.md#build`, `#regression` | planlagt (WP0) |
| 3 | `contract/validate_contract.py` | kjører positive og negative fixtures mot `apns_invite_v1.json` | siste linje «RESULT: N grønne, 0 røde» | **finnes** (11/11, 06.10) |
| 4 | `handoff/two-scaffolds.sh` | starter 2–3 lokale scaffold-instanser (egen port, eier, vault, lagring) og stopper dem på PID, ikke på navn | to prosesser svarer på `/health` side om side | planlagt (WP6) |
| 5 | `handoff/matrix.sh <profil>` | kjører scenario for en enhetsprofil: `mac-app`, `ios-sim-iphone`, `ios-sim-ipad`, `linux-client` | én rad i matrisen per profil | planlagt (WP10) |
| 6 | `handoff/prod-smoke.sh` | **bare GET** mot prod; skriver URL, statuskode, hva som ble lest | `TESTRESULT.md#prod-smoke`. Kjøres ikke før Kjetil har sagt ja til lesing fra prod | planlagt (WP9) |
| 7 | `handoff/iphone-sjekkliste.md` | manuell sjekkliste, Kjetil krysser av | forventet observasjon per steg | planlagt (WP10) |
| 8 | `handoff/apns-real-send.sh` | ett sandbox-varsel mot Apple. Leser `APNS_*` fra scaffoldets miljø — **Claude leser aldri nøkkelen** | `apns-id` i logg, varsel vises | planlagt (WP11) — blokkert til Kjetil har satt miljø og gitt token |

## Hva Kjetil må gjøre selv (og når)

1. Si ja til lesing fra prod før script 6.
2. Før script 8: sette `APNS_TEAM_ID`, `APNS_KEY_ID`, `APNS_PRIVATE_KEY_PATH` (sti til `.p8` på scaffoldets disk), `APNS_BUNDLE_ID`, `APNS_USE_SANDBOX=true` på skyscaffoldet vi tester mot; bygge appen fra Xcode med push-entitlement; sende meg *ikke* nøkkelen, Team-ID i klartekst er greit å si, token trenger jeg ikke se.
3. Krysse av i iPhone-sjekklisten.
