# Handoff til Codex — fase 1b (APNs-invitasjon: kjør, koble, Binding)

Fra: Claude (Cowork), 06.10.2026. Til: Codex på Kjetils Mac. Skriv resultatet til `RESULT_fase1b.md` i denne mappen (se «Slik leverer du»).

## Mål
Fase 1 er ferdig og pushet. Tre ting gjenstår som kan gjøres uten Kjetils hender: (1) kjøre testinfrastrukturen som er skrevet men aldri kjørt, (2) koble tokenregisteret og dispatcheren til scaffoldets ruter, (3) undersøke og, der det lar seg gjøre, bygge Binding-siden. Les først, i denne rekkefølgen:

1. `../../PLAN.md` §7 (status per arbeidspakke) og §2 (WP2, WP3, WP4)
2. `../../TESTRESULT.md` (hva som er målt, og baseline-tallene du skal sammenligne mot)
3. `../../contract/apns_invite_v1.json` (versjon 1.2.0) og `../../dataflow.md`
4. `../../STATUS.md` (siste fem logglinjer)

Stier (alle på Macen): `BASE=/Users/kjetil/Build/Digipomps/HAVEN`, `CHECK=$BASE/../../pdd-check` = `/Users/kjetil/Build/pdd-check`, PDD-mappen = `$BASE/CellProtocolDocuments/Deliverables/PDD_testmatrise-og-apns-chat_2026-09-29`.

## Faste regler (gjelder alle slices)
- Arbeid bare i engangs-worktrees under `/Users/kjetil/Build/pdd-check/` og i PDD-mappens `handoff/`. **Ikke** rediger eller kjør git i Kjetils egne checkouts (`$BASE/CellProtocol`, `$BASE/CellScaffold`, `$BASE/Binding`, `$BASE/CellProtocolDocuments`).
- Bygg og test med de samme miljøvariablene som skriptene bruker: `CELLPROTOCOL_LOCAL_PACKAGE_PATH`, `DIMYMINT_LOCAL_PACKAGE_PATH`, `DIMYMICROPAYMENTS_LOCAL_PACKAGE_PATH`. CellProtocol-katalogen må hete `CellProtocol`, og søsken-pakkene må ligge ved siden av (se `phase1/apply-phase2.sh`).
- Grønn-port: les AppTests-bundelen (`Test Suite 'AppTests.xctest' passed|failed` + neste `Executed`-linje), aldri bare siste «Executed». Tom linje = testene kompilerte ikke = ikke «0 røde».
- Sammenlign røde tester mot `../baseline-failures-cpmain.txt` (CellProtocol-gren) eller `../baseline-failures-pinned.txt` (pinnet). Nye røde utover disse = stopp og rapporter, ikke fiks i bakgrunnen.
- **Ikke commit, ikke push.** La endringene ligge ukommittet i worktreen; Claude committer og pusher via `commit-fase1.sh`. Rør ikke `Package.resolved`.
- Ingen hemmeligheter: ikke les, skriv eller lim `.p8`, `.env`, tokens eller nøkler. Ingen ekte APNs-sending. Ingen nettverkskall mot `palazzo.digipomps.org`, prod eller staging.
- Hvis noe stopper (sandbox, manglende simulator, avhengighet): skriv nøyaktig feilmelding i RESULT, gjør ingen omgåelse, gå videre til neste slice.
- Ikke endre `STATUS.md` gates (G1/G2/G3), `ACCEPT.md` eller lessons-registeret.

## Slice 1 — kjør testinfrastrukturen — STATUS: GODKJENT
Ingen kodeendring. Kjør og lim ekte utdata i RESULT:

1. `cd $PDD/handoff && ./two-scaffolds.sh` (tørrkjøring) → `./two-scaffolds.sh start 3` → `./two-scaffolds.sh probe` → `./two-scaffolds.sh stop`. Binæren bygges først i `$CHECK/impl/CellScaffold` (`swift build` med env over) hvis `.build/debug/Run` mangler. Hvis `serve --hostname --port` ikke er riktig kommandolinje for `Run`, finn riktig (les `Sources/Run/main.swift` / `entrypoint.swift` i worktreen) og **rett scriptet**; rapporter hva som var galt. Mål: tre prosesser på 8181–8183, hver med egen SQLite og egne hemmeligheter, helsesvar fra alle tre, ren stopp uten gjenværende prosesser (`pgrep -f 'Run serve'`).
2. `cd $PDD/handoff && ./matrix.sh` (tørrkjøring) → `./matrix.sh --go`. Profilene `ios-sim-iphone`/`ios-sim-ipad` hoppes over hvis simulator mangler; si hvilke som ble kjørt og hvilke som ikke. Binding-worktree er `$CHECK/Binding` (origin/main, 8ce634f6).
3. Rett feil i scriptene bare i `handoff/` og forklar hver rettelse i RESULT.

## Slice 2 — rutene og publish-koblingen — STATUS: GODKJENT
Worktree: `$CHECK/impl/CellScaffold`, gren `pdd/testmatrise-apns-dev` (bygger mot CellProtocol-grenen `pdd/testmatrise-apns` i `$CHECK/impl/CellProtocol`). Kjør `phase1/apply-phase2.sh --go` først hvis worktreen ikke står på cb2037a2, så du starter fra kjent tilstand.

Bygg (kun CellScaffold, ikke CellProtocol):
1. **Vapor-ruter** `POST /push/register` og `POST /push/revoke` (ny controller, registrert der `VaporInviteLanding` registreres). Body = JSON av `HavenPushRegistration` / `HavenPushRevocation`. Svar: register → `{"registrationID": "..."}`; feil → statuskoder med kontraktens `denies`-koder i svaret (`unsigned`, `signature_does_not_match_entity`, `bad_token_format`, `stale`, `key_changed` …; bruk `HavenPushVerifier.Failure.code`). Ingen ekko av token i svar eller logg. `PushRegistryService` med `FilePushRegistryStore` finnes (`InvitePushDispatcher.swift`); legg registry-filen i scaffoldets vanlige datakatalog (følg hvordan andre små tilstandsfiler plasseres; ikke finn på ny konvensjon).
2. **Kobling i `VaporInviteLanding.publish`**: etter at billetten er lagret, kall `InvitePushDispatcher.dispatch(publication:)` i en `Task` som ikke blokkerer svaret, og som ikke kan endre svaret. Svaret til avsender skal være byte-identisk uansett utfall (test det: samme respons med og uten registrert mottaker). `sender` = `APNSPushProviderAdapter` hvis `APNSPushConfiguration(environment:)` gir konfigurasjon, ellers `nil` (da logges `transport_refused`/`apns_not_configured`).
3. Tombstone-ledger og revoked-ticket-liste er ennå ikke persistert i scaffoldet: gi dispatcheren ledger fra en tom `HavenInviteTombstoneLedger` og revoked-IDer fra `InviteTicketRecord.revokedAt != nil` (spørring), og kommenter at ledgeren kommer med invitasjon runde A del 2.
4. `audienceEntity`: `InviteTicketRecord` trenger ikke lagre den; dispatch skjer med publiseringen i hånden.

Tester (Tests/AppTests, XCTVapor der det trengs): registrer → 200 + registrationID; usignert → avvist med riktig kode; samme entitet med annen nøkkel → `key_changed`; revoke av andres registrering → `not_the_owner_of_registration`; publish med navngitt+registrert mottaker → dispatcher får kall (bruk en stub-sender injisert i app-konfigurasjonen), publish uten `audienceEntity` → ingen sending; svar til avsender identisk i begge tilfeller; token finnes ikke i noen logglinje. Kjør nye tester, så hele suiten, sammenlign med `baseline-failures-cpmain.txt` (42 røde forventet, identiske).

## Slice 3 — Binding — STATUS: GODKJENT TIL UNDERSØKELSE, BYGGING BARE HVIS DET ER ENKELT
Worktree: `$CHECK/Binding` (detached origin/main). Opprett gren `pdd/testmatrise-apns` lokalt der.
1. Undersøk først, og skriv svaret i RESULT: hvordan henter Binding CellProtocol (lokal sti, tagg, revisjon i `Binding.xcodeproj`/`Package.resolved`)? Kan den peke på `$CHECK/impl/CellProtocol` uten å endre prosjektfilen i Kjetils checkout? Hvor ligger `NotificationEnrollmentManager.swift`, hvordan hentes APNs-token i dag, og hvor fanges `userInfo` ved trykk på varsel?
2. **Hvis** Binding kan bygges mot CellProtocol-grenen uten store prosjektendringer: (a) lag signert registrering (`HavenPushRegistration.make(entity:environment:bundleId:token:)`) med bundle-ID `org.digipomps.haven`, environment fra build-konfigurasjon (debug = `.sandbox`, release = `.production`), sendt til `POST /push/register` hos scaffoldet appen allerede snakker med; lagre `registrationID`. (b) ved trykk på varsel: les `haven.k == "invite"` og `haven.id`, hent billetten fra scaffoldet (samme GET som landing), verifiser med `HavenInviteVerifier`, åpne eksisterende invitasjonsflate. Ingen auto-aksept, ingen UI-endringer ut over å åpne flaten som finnes; ugyldig billett → feilflate. Skriv ren logikk adskilt fra UI slik at den kan enhetstestes (`xcodebuild test` hvis et testmål finnes).
3. **Hvis ikke** (krever pin-endring, ny tagg, eller invitasjonsflaten fra runde A del 2 finnes ikke i origin/main): ikke bygg noe. Skriv en presis liste over hva som må skje først, og stopp. Det er et fullverdig svar.
4. Ingen ny GUI. Oppdager du at appen trenger en ny flate: stopp og skriv det i RESULT.

## BLOKKERT — ikke start
- Ekte APNs-sending (T5.5): venter på `APNS_*`, push-entitlement og enhets-token fra Kjetil.
- Alt mot prod, staging eller `palazzo.digipomps.org` (Kjetil har ikke gitt ja til lesing mot prod).
- Kjede-/chat-tester (T1/T2/T3), WP7, WP8b: avhenger av invitasjon runde A del 2.
- Merge, tagging, løfting av pinner, push, sletting av grener.

## Slik leverer du
Skriv `RESULT_fase1b.md` i denne mappen med, per slice: hva du kjørte (kommandoer), siste relevante utdata limt inn (ikke parafrasert), hva som er grønt/rødt/blokkert, filene du endret (`git -C <worktree> status --short`), og åpne spørsmål. Avslutt med én linje: `FERDIG slice 1/2/3: <ja|delvis|nei>`.
