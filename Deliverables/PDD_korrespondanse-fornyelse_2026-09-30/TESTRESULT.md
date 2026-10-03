# TESTRESULT: fornyelse av utløpt korrespondansetilgang

Grenen er `claude/korrespondanse-fornyelse-20260930`. Commit `415ea3d2`, bygget på `feec2372`. Testene kjørte på Kjetils Mac via jobbløperen 30.09.2026.

## #build

`swift build --build-tests` ga rc 0. Første bygg i den nye worktreen tok 19:35:43–19:39:53. Bygget etter rettingen tok 10 s. Logg: `HavenAgentD/.tmp-clang-module-cache/agentd-diag/korr-bygg-20260930T193542.full.log`.

## #t1 #t2 #t3

`swift test --filter AssistantCorrespondence`: **30 tester kjørt, 0 feil**. Utdata ligger i `evidence/T1-T4-korrespondansetester-20260930T1941.log`.

- T1 `testExpiredRecipientGrantRenewsThroughFreshInviteAndOwnerApproval` passerte. Testen gjenskaper Vegars `recipient_not_allowed` etter at Kjetils tilgang går ut. En fersk invitasjon gir `pending_approval` med `renewsGrantID`, og godkjenningen gir et nytt bevis med samme mottakerliste. Vegars sending gir `sent`, og Kjetils `inbox.list` viser meldingen.
- T2 `testRevokedExpiredGrantCannotRenewThroughFreshInvite` passerte. En tilbakekalt principal gir ingen ny forespørsel, og `pendingCount` er 0.
- T3 `testExpiredGrantCannotMoveToAnotherDeviceThroughFreshInvite` passerte. En annen enhet gir `principal_already_enrolled`.

## #t4

Alle 27 eksisterende `AssistantCorrespondence*`-tester passerer uendret. Det gjelder også `testApprovedGrantEnrollmentBehaviorRemainsUnchanged`, som viser at en aktiv tilgang oppfører seg som før.

Full `swift test` på grenen ble kjørt 30.09 kl. 19:51–20:39. **57 unike testnavn feilet**, og ingen av dem gjelder korrespondanse. Listen ligger i `evidence/regresjon-feilende-415ea3d2.txt`.

Sammenlignet med baselinelisten fra 09.09 (`e1f3e22f`, 59 navn):

- **To navn var nye:** `PortholeIdentityContinuityRoutesTests.testCoPilotChatLoadsWhileUnprovenHistoricalAuxiliariesRemainUntouched` og `SkeletonRuntimeSourceTests.testRuntimeDispatchesDropTargetPayloadAndHorizontalScrollAxis`. Begge feiler likt på `feec2372` uten fornyelsen (2 tester, 4 feil) og på `415ea3d2` (2 tester, 4 feil). De var altså allerede røde i commiten staging kjører, og fornyelsen innførte dem ikke.
- **Fire navn** fra baselinen er grønne nå.

**Ingen nye feil kommer fra endringen.**

## #t6 #t7 #t8

Commit `06f32050` (fornyelse de siste sju dagene før fristen), bygget og testet 02.10.2026 kl. 12:56–12:57. `swift test --filter AssistantCorrespondence`: **33 tester kjørt, 0 feil**.

- T6 `testActiveGrantNearExpiryRenewsBeforeItLapses` passerte. Med to døgn igjen gir en fersk invitasjon `pending_approval` med `renewsGrantID`. Før godkjenningen når avsenderen fram, og det gamle beviset leser innboksen. Etter godkjenningen avvises det gamle beviset, og det nye har fristen fra den nye invitasjonen. Forbi den gamle fristen virker alt fortsatt.
- T7 `testActiveGrantOutsideRenewalWindowKeepsExistingGrantBehavior` passerte. Med åtte døgn igjen svarer serveren `already_enrolled` uten `renewsGrantID`.
- T8 `testRevokedPrincipalNearExpiryCannotRenewThroughFreshInvite` passerte. Ingen ny forespørsel, og `pendingCount` er 0.

Full `swift test` på `06f32050` (02.10 kl. 12:57–13:02): 57 unike feilende testnavn, de samme som på `415ea3d2`. Ingen nye, og ingen som ble grønne. Liste: `HavenAgentD/.tmp-clang-module-cache/agentd-diag/korr-vindu-regresjon-20261002T125722.feilende.txt`.

`06f32050` er pushet. Image bygges i kjøring 36998313078. Den er **ikke satt ut på staging**.

## #pr

PR #277 mot `main` ble opprettet 02.10 (https://github.com/Digipomps/CellScaffold/pull/277), etter Kjetils «Ja, lag PR (anbefalt)». Grenen har tre commits: `415ea3d2`, `06f32050` og `d83d9f6b` (statusloggen). GitHub melder at den kan merges. CI kjørte da PR-en ble sjekket.

Målt 02.10 kl. 14:18: merge-sjekken «Focused control-plane gates» er fullført og grønn (kjøring 36998795184, hode `d83d9f6b`). PR-en står som `MERGEABLE` og `CLEAN`. Image-bygget for `06f32050` (kjøring 36998313078) pågikk fortsatt.

## #t5

Live på staging 30.09.2026:

- **Utsetting:** `haven-deploy@staging-415ea3d2` ga `COMMITTED_VERIFIED` kl. 20:24:24Z. Nedetiden var i underkant av ett minutt. `/health/build` viser `app_revision` `415ea3d2`. Doctor ga 0 feil, og preflight var grønn.
- **Invitasjonsbytte:** `cutover-invites-20260908.sh` ga `COMMITTED_VERIFIED` kl. 20:24:51Z (`INVITES_BASE64` er byttet, de 94 andre miljølinjene er uendret). Listen inneholder bare to invitasjoner, for `kjetil-codex-d` og `kjetil-vegar-codex-d`, begge med profilens `deviceID`. Invitasjonene gjelder til 07.10, og tilgangene til 30.10.
- **Oppsett:** `setup` ga `pending_approval` for begge profilene med samme maskin og nøkkel. Serveren behandlet dem altså som fornyelser, ikke som nye enheter. Forespørslene var `access-request-d1a34668…` og `access-request-3c699aaf…`.
- **Godkjenning:** Kjetil godkjente begge kl. 22:43. `activate` ga `approved`, og status er `active` for begge. De nye bevisene gjelder til `2026-10-30T19:00:12Z`.
- **Innboks:** `doctor` (`inbox.list`) ga `status ok` for begge profilene. Korrespondanse-MCP-en i Claude-appen leser innboksen uten omstart.
- **Sending til Vegar:** `message.send` til `vegar-local-agent` ga `sent` (`msg-965eb01f-0997-4d51-a2f8-65e9212ab4fd`, sekvens 14).
- **Sending til Victoria:** `message.send` til `victoria-lille-robot` ga `recipient_not_allowed`. Kjetils side er fornyet, men Victorias egen tilgang gikk også ut 29.09, så det er nå hun som er en inaktiv mottaker. Hun må fornye på sin side med samme mekanisme: en fersk invitasjon med hennes `deviceID`, deretter oppsett hos henne og godkjenning fra Kjetil.
- **Vegars sending til Kjetil:** Tre meldinger fra `vegar-local-agent` til `kjetil-vegar-codex-d` kom fram etter fornyelsen: sekvens 13, 14 og 15, opprettet 01.10 kl. 00:02, 00:12 og 00:15Z. Losen leste og kvitterte dem 01.10 kl. 06:01Z. Dermed er F0 observert begge veier.

## Det som ikke virket

1. Første kjøring (`evidence/forste-kjoring-20260930T1935.log`) feilet på én påstand i T1. Testen ventet at `message.send` skulle svare `ok`, men serveren svarer `sent` (med `created: true`). Feilen lå i testens antakelse, ikke i koden. Påstanden er rettet og sjekker nå både `sent` og `created`.
2. Første forsøk på å lese Kjetils innboks via korrespondanse-MCP-en (30.09) ga «The Entity-bound correspondence access proof is invalid». Klienten avviser et utløpt bevis selv, før serveren blir spurt. Profilen `kjetil-vegar-d` viser at beviset gikk ut `2026-09-29T20:37:15Z`.
3. Vegar sendte meldingen fra 29.09 på nytt 01.10 (sekvens 14), fordi han trodde den ikke hadde kommet fram. Den hadde kommet fram: sekvens 12, opprettet 29.09 kl. 19:45Z, 52 minutter før Kjetils bevis gikk ut. Etter det kunne den verken leses eller kvitteres før fornyelsen. Avsenderen har ikke noe verktøy for å se om en sendt melding er lest eller kvittert; MCP-en har bare `send_message`, `list_inbox`, `read_message` og `ack_message`.
