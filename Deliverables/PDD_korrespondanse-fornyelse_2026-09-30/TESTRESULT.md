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

## HD-0006

Skriptene som skal fornye tilgangen hos mottakerne, ligger i `HAVEN-Deploy/_handoff/HD-0006/`. Dette er testene av dem, kjørt 05.10.2026. **Alt er kjørt mot stedfortredere. Ingenting er kjørt mot staging, og ingen ekte klient er brukt.**

| Skript | Hvor | Tester | Resultat |
|---|---|---|---|
| `forny-haven-tilgang.sh` (fila mottakerne får, SHA-256 `e4ca57eddda23736378ffcdefcb052ebfbfb8dceda3d02eca7205e39990c7438`) | macOS 27.0, `/bin/bash` 3.2.57, Python 3.9.6 | 55, to runder: uten språkinnstilling og med `LANG=nb_NO.UTF-8` | grønt i begge, kl. 20:09Z (`HAVEN-Deploy/_handoff/HD-0006/maal/SELVTEST-3-20261005.md`) |
| samme | Linux i skyen | de samme 55 | grønt under bash 5, `dash`, `bash --posix`, Python 3.9 og 3.11 |
| `lag-invitasjoner.sh` og `proev-fornyelse.sh` | macOS 27.0, `/bin/bash` 3.2.57, Python 3.9.6 | 28, hver i sin egen midlertidige HAVEN-rot | grønt, kl. 20:42Z (`HAVEN-Deploy/_handoff/HD-0006/maal/SELVTEST-PROEVEN-1-20261005.md`) |
| samme | Linux i skyen | de samme 28 | grønt |
| `bytt-invitasjoner.sh` | Linux i skyen, mot en oppdiktet vert | 22 | grønt. Ikke kjørt på macOS: testen ville brukt den ekte `ssh` der. |

De to første kjøringene på Macen var røde:

```
== proev-fornyelse: selvtest, 2026-10-05T19:43:36Z ==
-- maskinen: macOS 27.0, bash 3.2.57(1)-release, Python 3.9.6
   FAIL: test_den_nyeste_invitasjonen_velges_paa_tvers_av_mappene (__main__.Forny)
   Ran 52 tests in 32.525s
   FAILED (failures=1)
```

Skriptet valgte invitasjonsfil med `ls -t` over tre mønstre. På macOS sorterer `ls` ikke bare etter tid når ett av mønstrene ikke treffer noen fil. Skriptet tar nå den nyeste selv.

```
== proev-fornyelse: selvtest, 2026-10-05T20:04:17Z ==
-- runde 1: uten språkinnstilling (slik køen kjører)
   Ran 54 tests in 36.306s
   OK
-- runde 2: LANG=nb_NO.UTF-8 (slik Terminal kjører)
   ERROR: test_annen_enhets_id_i_fila_stopper_foer_noe_sendes (__main__.Forny)
   …
   Ran 54 tests in 37.711s
   FAILED (errors=8)
```

Med UTF-8 leser bash 3.2 på macOS første byte av «, », æ, ø og å som en bokstav. `$PROFIL»` ble navnet på en variabel som ikke finnes, og seks feilmeldinger ble til «unbound variable». Rettet med klammer (`${PROFIL}»`), og en test nekter skrivemåten uten.

```
== proev-fornyelse: selvtest, 2026-10-05T20:09:37Z ==
ok  forny-haven-tilgang.sh har sjekksummen som er ventet (e4ca57eddda23736378ffcdefcb052ebfbfb8dceda3d02eca7205e39990c7438)
-- maskinen: macOS 27.0, bash 3.2.57(1)-release, Python 3.9.6
-- runde 1: uten språkinnstilling (slik køen kjører)
   Ran 55 tests in 31.059s
   OK
-- runde 2: LANG=nb_NO.UTF-8 (slik Terminal kjører)
   Ran 55 tests in 32.477s
   OK
SELVTESTEN ER GRØNN: forny-haven-tilgang.sh gjør det testene krever, med bash og verktøyene på denne Macen,
både uten språkinnstilling og med LANG=nb_NO.UTF-8.
```

Begge er målt hver for seg etterpå, med `HAVEN-Deploy/_handoff/HD-0006/maal-macos-skall.sh` (kl. 20:26Z):

```
-- 1. ls -t: den nyeste forst?
   to filer som finnes:                                ny.json
   pluss en som ikke finnes, med navn pa /Users:       gammel.json
   pluss en som ikke finnes, med navn pa ./ :          gammel.json
   pluss en som ikke finnes, med navn pa /zzz:         ny.json
-- 2. en variabel rett foran et tegn utenfor ASCII, med og uten UTF-8
   LANG=(tom)        $P foran c2bb : kode 0, skrev [verdi??]
   LANG=nb_NO.UTF-8  $P foran c2bb : kode 127, skrev /bin/bash: P?: unbound variable
   LANG=nb_NO.UTF-8  $P foran 2e : kode 0, skrev [verdi.]
   med klammer, LANG=nb_NO.UTF-8: [verdi??]
```

(`c2bb` er tegnet », `2e` er punktum, og spørsmålstegnene står for byte utenfor ASCII.) Hele utskriften: `HAVEN-Deploy/_handoff/HD-0006/maal/MAAL-MACOS-SKALL-1-20261005.md`.

Begge feilene var usynlige på Linux. Den uavhengige kontrollen gikk gjennom første utgave kommando for kommando for macOS (`panel/FABEL_HD0006_SKRIPT.md`, M12), regnet `ls -t` som i orden og vurderte ikke språkinnstillingen. Det var kjøringen på Macen som fant dem.

Bevisste feil ble lagt inn i kopier av skriptene, én om gangen, for å se at testene blir røde. På det endelige settet ble alle fanget: 62 av 62 for `forny-haven-tilgang.sh`, 42 av 42 for `lag-invitasjoner.sh` og `proev-fornyelse.sh`, og 21 av 21 for `bytt-invitasjoner.sh`. Verktøyet og utskriftene ligger i `handoff/hd0006-skript-og-tester-20261005.tar.gz`.

Per 05.10 var ingenting kjørt mot staging eller med en ekte klient. Det som er kjørt 06.10, står under. T6–T8 over er fortsatt bare enhetstester.

## Prøven mot staging, 06.10.2026

Kjetil 06.10 ca. 07:05Z: «Kjør prøven». Stempelet er `20261006`. Rekkefølgen står i `HAVEN-Deploy/_handoff/HD-0006/LES-MEG.md`. Jobbene går i bane b i `_losen-queue`, og utskriftene ligger i `HAVEN-Deploy/_handoff/HD-0006/maal/` (kopier i `evidence/`).

| Steg | Jobb | Kjørt | Utfall | Utskrift |
|---|---|---|---|---|
| 1 Lag invitasjoner | `b21-hd0006-lag-invitasjoner-1-20261006` | 07:13:10Z | Grønt. Fire invitasjoner i tjenerfila (prøveparet, Vegar, Victoria), gyldige til 2026-10-13T07:13:10Z, tilgang til 2026-11-05T07:13:10Z, ingen med enhets-ID. | `PROEVE-1-LAG-INVITASJONER-20261006.md` |
| 2 Forbered | `b21-hd0006-forbered-1-20261006` | 07:14:20Z, 22 s | Grønt. Første kjøring med de ekte `pkgutil`, `codesign` og `lipo`. Begge pakkeklientene: sjekksum som ventet, gyldig signatur, `x86_64 arm64`. Den installerte pilotklienten: `arm64`. Alle tre leste begge prøveidentitetene. `sim-a` prøves med klienten fra pakken 08.09, `sim-b` med den installerte. | `PROEVE-2-FORBERED-20261006.md` |
| 3 Les, før byttet | `b21-hd0006-les-1-20261006` | 07:15:51Z | Grønt. Første kjøring av `forny-haven-tilgang.sh` med ekte klienter mot staging. `status` ga kode 0 for begge, og `profile.json` er uendret. | `PROEVE-3-LES-FOER-BYTTET-20261006.md` |
| 4 Les verten (`toerr`), utgave 3 av skriptet | `b21-hd0006-toerr-1-20261006` og `-2` | 11:24Z og 11:32Z | Bare lesing. Den første stoppet på en feil i skriptets helsekontroll, den andre var grønn. Utgaven ble forkastet samme time: den byttet lista et sted neste utsetting ville skrevet over. Se «Byttet på staging: skriptet» under. | `PROEVE-4-TOERR-20261006.md`, `PROEVE-4-TOERR-2-20261006.md` |
| 4a Les verten som ops, og prøvestart haven-deploy (utgave 5) | `b24-hd0006-les-1-20261006` og `b25-hd0006-proevestart-1-20261006` | 17:05Z og 17:06Z | Grønt, uten HINDER. Ingenting på verten er endret ut over et startmerke og en logg på to linjer hos ops. | `LES-1-20261006.md`, `PROEVESTART-1-20261006.md` |
| 4a på nytt, med skriptet etter fjerde runde | `b28-hd0006-les-2-20261006` og `b29-hd0006-proevestart-2-20261006` | 18:26Z og 18:27Z | Grønt, uten HINDER. Startkallet var ferdig på under ett sekund, og skallet ventet fem før det kjørte sudo. Et startmerke og en logg til hos ops. | `LES-2-20261006.md`, `PROEVESTART-2-20261006.md` |
| 4b Les fila under `/etc/haven` som root (`toerr`, utgave 5) | `b32-hd0006-toerr-3-20261006` | 19:42Z | Grønt, uten HINDER, etter Kjetils «Ja til root» ca. 19:40Z. Root slipper inn med samme nøkkel som ops. Fila eies av root, har rettighet 600 og seks variabler, og invitasjonsvariabelen står én gang, på linje 1. Lista i fila er den samme som i containeren. Ingen claimer på verten. Ingenting er endret. | `TOERR-UTGAVE5-1-20261006.md` |
| 5 Bytt lista på staging (`utfoer`, utgave 5) | `b33-hd0006-utfoer-1-20261006` | 21:05:35Z–21:06:45Z | Grønt: `<!-- BYTTE FERDIG -->`, EXIT=0, ingen HINDER eller MERK. Meldt i `_losen-queue/KOORDINERING.md` kl. 20:57Z, før kjøringen. Linja ble byttet i `/etc/haven/staging-correspondence-invites.env` 21:05:54Z. haven-deploy sluttet med kode 0 og COMMITTED_VERIFIED 21:06:30Z. Samme revisjon, ny container, og lista i containeren og i fila har sjekksummen til tjenerfila. Claimen ble frigitt. | `UTFOER-1-20261006.md` |
| 6 Les, etter byttet | `b34-hd0006-les-etter-byttet-1-20261006` | 21:08:46Z | Grønt. `status` ga kode 0 for begge prøveprofilene: tilgangen gjelder til 2026-10-08T13:03:23Z, og tjeneren godtar den. Ingenting er endret. | `PROEVE-6-LES-ETTER-BYTTET-20261006.md` |
| Det gamle beviset, før steg 7 (`maal-gammelt-bevis.sh vis`) | `b35-hd0006-gammelt-bevis-vis-1-20261006` | 21:09:56Z | Tjeneren godtar beviset begge prøveprofilene hadde før prøven (kode 0, HTTP 200). Profilene har det samme beviset som før. Ingen profil er endret. | `GAMMELT-BEVIS-VIS-1-20261006.md` |
| 7 Setup | `b36-hd0006-setup-1-20261006` | 21:11:06Z | Grønt. Invitasjonene ble hentet fra staging, og `forny-haven-tilgang.sh` ga kode 0 for begge. To forespørsler venter på Kjetil. Profilene venter på godkjenning med samme enhet, identitet og nøkkel som før. Kopi av hver profil ligger ved siden av den. | `PROEVE-7-SETUP-20261006.md` (i `evidence/` er forespørsels-ID-ene tatt ut) |
| Det gamle beviset, mens forespørslene venter (`maal-gammelt-bevis.sh godtas`) | `b37-hd0006-gammelt-bevis-godtas-1-20261006` | 21:12:16Z | Som ventet: tjeneren godtar fortsatt beviset begge hadde før prøven (kode 0, HTTP 200). Profilene har ikke noe bevis nå, så de ble ikke prøvd. | `GAMMELT-BEVIS-GODTAS-1-20261006.md` |
| 8 Kjetil godkjenner | | 07.10 ca. kl. 10:00Z | Kjetil, ordrett: «Jeg har godkjent prøveparet». Godkjenningen ble gjort på adminsiden; denne tråden har ikke sett den, bare følgen av den i steg 9. | |
| 9 Aktiver, og en melding hver vei | `b38-hd0006-aktiver-1-20261006` | 07.10 kl. 10:01:03Z | Grønt: «PRØVEN ER GRØNN». `forny-haven-tilgang.sh aktiver` ga kode 0 for begge. De nye tilgangsbevisene gjelder til 2026-11-05T07:13:10Z, tjeneren godtar dem, og enhet, identitet og nøkkel er de samme som før. En melding hver vei ble sendt, listet, lest og kvittert. Releasejobben for 2026.9.6 skrev i `_losen-queue/KOORDINERING.md` at staging ble satt ut på nytt 07.10 kl. 02:47Z; revisjonen er målt av denne tråden først kl. 13:43Z (raden under). | `PROEVE-9-AKTIVER-20261006.md` |
| Det gamle beviset, etter godkjenningen (`maal-gammelt-bevis.sh avvises`) | `b39-hd0006-gammelt-bevis-avvises-1-20261006` | 07.10 kl. 10:01:33Z | Som ventet: tjeneren avviser beviset begge hadde før prøven (kode 2, HTTP 401, `invalid_access_credential`), og godtar det nye (kode 0, HTTP 200). Ingen profil er endret. | `GAMMELT-BEVIS-AVVISES-1-20261006.md` |
| Lista i containeren etter utsettingen av 2026.9.6 (`bytt-invitasjoner.sh les`) | `b40-hd0006-les-3-20261007` | 07.10 kl. 13:43:35Z | Grønt, bare lesing som ops. Containeren kjører `381094bbb18e390bd8fd2b8955524b5fa3e4f9ea`, og `/health/build` oppgir det samme. Lista som kjører, har fire invitasjoner, og alle gjelder. Låsen til haven-deploy er fri. | `LES-3-20261007.md` |
| De ferdige meldingene til Vegar og Victoria | (lest på Macen, ingen jobb) | 07.10 kl. 13:44Z | Hver melding har én lenke, mottakerens egen, og riktig profil i `aktiver`-linja. Fila ved siden av har samme SHA-256 som den prøven kjørte (`e4ca57ed…`). Sammenlignet uten å skrive ut noen lenke. Lenkene selv er ikke prøvd. | |

Fra steg 3:

```
-- sim-a
   forny-haven-tilgang.sh status sim-a ga kode 0 og skrev:
      Klient:  /Users/kjetil/Build/Digipomps/HAVEN/korrespondanse-privat-20261006/pakkebin/sep/haven-correspondence-mcp
      Profil:  sim-a (sim-torrkjoring-a)
      Tilgang: gjelder til 2026-10-08T13:03:23.640Z, og tjeneren godtar den (prøvd nå).
   ok  tjeneren godtar tilgangen sim-a har
-- sim-b
   forny-haven-tilgang.sh status sim-b ga kode 0 og skrev:
      Klient:  /Users/kjetil/Library/Application Support/HAVEN/AssistantCorrespondence/bin/haven-correspondence-mcp
      Profil:  sim-b (sim-torrkjoring-b)
      Tilgang: gjelder til 2026-10-08T13:03:23.640Z, og tjeneren godtar den (prøvd nå).
   ok  tjeneren godtar tilgangen sim-b har
```

Kontrollert etter steg 1, uten å skrive ut noe privat: deltakergrafen er lik den fra 30.09 for alle sju deltakerne, invitasjonsfilene har de samme feltene som i settene fra 30.08, 08.09 og 30.09 (bortsett fra kode, nummer og tidspunkter), og lenkene går til staging.

Det steg 1–3 ikke viser: noe om fornyelsen selv. Tjeneren fikk invitasjonene i steg 5.

Fra steg 5 (`evidence/UTFOER-1-20261006.md`), et utdrag der linjer er hoppet over. Linjene med innrykk er fra loggen til haven-deploy på verten, slik skriptet viste dem; `<skjult>` er satt inn av skriptet:

```
2026-10-06T21:05:54Z ok  linja HAVEN_ASSISTANT_CORRESPONDENCE_INVITES_BASE64 er byttet i /etc/haven/staging-correspondence-invites.env, der den sto. Kopi av fila fra før: /etc/haven/staging-correspondence-invites.env.foer-20261006-210553
2026-10-06T21:05:55Z starter haven-deploy staging current --env-only (samme revisjon, nytt miljø fra fila)
   2026-10-06T21:05:57Z PREFLIGHT_GREEN prev=<skjult> image=<skjult>
   2026-10-06T21:06:08Z STOPPED cellscaffold-app-1 — nedetiden starter her
   2026-10-06T21:06:08Z DEPLOYING gammel runtime parkert som cellscaffold-app-1-rollback-20261006T210555Z-staging-e5c34345
   2026-10-06T21:06:19Z READY_OK (foerste-start) etter 15s
   2026-10-06T21:06:19Z kontrollert restart
   2026-10-06T21:06:30Z READY_OK (restart) etter 15s
   2026-10-06T21:06:30Z COMMITTED_VERIFIED
   HAVEN_DEPLOY_SLUTT=0
2026-10-06T21:06:43Z ok  /health/build oppgir e5c3434510884275cae4a732935ab4b55cf7fad9 og miljøet staging etter byttet
2026-10-06T21:06:44Z ok  cellscaffold-app-1 har de samme korrespondansevariablene som før (bare navnene er sammenlignet)
2026-10-06T21:06:45Z ok  cellscaffold-app-1 er en ny container, og lista i den har sjekksummen til tjenerfila
2026-10-06T21:06:45Z ok  lista i /etc/haven/staging-correspondence-invites.env har samme sjekksum, så neste utsetting setter den samme lista
2026-10-06T21:06:45Z ferdig: invitasjonslista fra 20261006 er i kraft på staging, og claimen er frigitt
<!-- BYTTE FERDIG -->
```

Loggen sier «etter 15s» to ganger, mens det er 11 sekunder mellom klokkeslettene på linjene. Hva de 15 sekundene regnes fra, er ikke lest. Hvor lenge staging var utilgjengelig utenfra, er ikke målt.

Fra steg 9 (`evidence/PROEVE-9-AKTIVER-20261006.md`), et utdrag:

```
ok  begge har fått nytt tilgangsbevis, og tjeneren godtar dem
   sim-a -> sim-b: sendt (sent)
   sim-b: meldingen står i innboksen
   sim-b: lest, og innholdet er det som ble sendt
   sim-b: kvittert, og kvitteringen står i innboksen
   sim-b -> sim-a: sendt (sent)
   sim-a: meldingen står i innboksen
   sim-a: lest, og innholdet er det som ble sendt
   sim-a: kvittert, og kvitteringen står i innboksen
ok  en melding hver vei er sendt, listet, lest og kvittert
```

Det prøven ikke viser, med prøvens egne ord: «Prøven sier ikke noe om hva tjeneren har lagret for Vegar og Victoria, eller om klientene på deres maskiner.» Den viser heller ikke fornyelse med denne fila på en tilgang som alt er utløpt (Victorias tilfelle).

## Byttet på staging: skriptet (06.10.2026)

`HAVEN-Deploy/_handoff/HD-0006/bytt-invitasjoner.sh` ble skrevet om to ganger 06.10, og utgave 5 ble rettet i fire runder etter uavhengige kontroller. Her står hva som ble funnet, hva som er prøvd, og hva som ikke er det. Byttet selv ble kjørt 06.10 kl. 21:05Z, én gang, og står i tabellen over (steg 5).

**Det som ikke virket**

| Utgave | Hva som var galt | Hvordan det ble funnet | Kostnad |
|---|---|---|---|
| 1 til 3 | Byttet lista i containeren som kjører, med `/home/ops/cutover-invites-20260908.sh`. haven-deploy setter lista fra `/etc/haven/staging-correspondence-invites.env` hver gang den kjører, så neste utsetting ville skrevet den gamle tilbake. | Den installerte haven-deploy og journalen fra utsettingen 05.10 ble lest etter `toerr` og før `utfoer` (`evidence/HAVEN-DEPLOY-PAA-VERTEN-20261006.md`). Tittelen på HD-0006 sa det samme, og var ikke lest godt nok. | Ingenting på verten. En halv dag. |
| 1 til 3 | Helsekontrollen lette etter revisjonen i de første 400 tegnene av svaret fra `/health/build`. Svaret er lengre, og feltet står ikke først. | Første `toerr` mot verten stoppet på en vert som var i orden (`evidence/PROEVE-4-TOERR-20261006.md`). Etterligningen i testene hadde et kortere svar enn det ekte. | Ingenting. |
| 4 | Avgjorde om haven-deploy var ferdig ved å se etter prosessen i `/proc` og etter ord i loggen. I tre forløp la skriptet fila tilbake og frigav claimen mens haven-deploy ennå gikk, og sa «staging står som før». | Uavhengig kontroll (`panel/FABEL_BYTT_UTGAVE4.md`), som kjørte forløpene mot etterligningen. | Ingenting. Utgave 4 ble aldri kjørt mot verten. Testene var grønne (63 av 63, og 64 av 64 bevisste feil fanget), fordi etterligningen skrev loggen rett i fila, mens den ekte haven-deploy skriver gjennom `tee`. |
| 5, første runde | En invitasjonsliste som ikke lot seg pakke ut, ble lest som en tom liste. Skriptets egen Python ble prøvd med 3.11, mens Macen har 3.9.6. | Uavhengig kontroll nr. 2 (`panel/FABEL_BYTT_UTGAVE5.md`). | Ingenting. |
| 5, tredje runde | Startkallet satte `umask 077` for hele kallet, for å lukke loggen hos ops. Etter sudos standard følger den med til haven-deploy (sudo legger brukerens umask sammen med sin egen), og haven-deploy setter ikke umask selv. Låsefila den lager etter en omstart av verten, ville da blitt lukket for alle andre enn root. Det samme kunne gjelde det `cellscaffold-deploy-status` skriver; det verktøyet er ikke lest. Hvilken umask haven-deploy ville fått, er ikke målt på verten. | Uavhengig kontroll av bare endringen siden forrige kontroll (`panel/FABEL_BYTT_UTGAVE5_DELTA3.md`, 17:45Z). 118 tester var grønne: ingen test spurte hvilken umask etterligningen av haven-deploy ble startet med. | Ingenting på verten. Prøvestarten kl. 17:06Z gikk med det gamle startkallet, men haven-deploy sluttet på linje 55, før den lager noe. Feilinnsettingen ble stoppet etter 72 av 127 og startet på nytt. |
| 5, tredje runde | Prøvestartens to vilkår (kode 2, og linja om revisjonen én gang) var bare prøvd sammen. To innsatte feil, én for hvert vilkår, ble ikke fanget. | Utskriftene per innsatt feil fra kjøringen som ble stoppet. | Ingenting. Nå prøver én test hvert vilkår alene. |
| 5, tredje runde | Prøvestarten skrev at skallet «levde i 5 sekunder etter at forbindelsen var lukket». Skriptet hadde ikke målt det: ventingen kunne feile uten at det syntes, og tiden på startkallet ble ikke tatt. | Samme kontroll. | Ingenting. På verten er loggen fra kjøringen 17:06Z sist endret fem sekunder etter startmerket (`evidence/PROEVEFILER-1-20261006.md`), så påstanden holdt for den kjøringen, men utskriften beviste den ikke. |

**Utgave 5 slik den står** (fjerde runde: SHA-256 `2e0fac7cda9ce133609dd3016c03e0d7dea30ec37b1c49b9683540aecbf1fe39`, 1053 linjer. Tredje runde, som `LES-1` og `PROEVESTART-1` ble kjørt med, hadde `425c9cee…f810f64`.)

| Hva | Hvor | Resultat |
|---|---|---|
| 133 tester mot en etterligning av verten (`proeve-sky/test_bytt.py`). haven-deploy er etterlignet, bortsett fra blokken som slår fila under `/etc/haven` sammen med miljøet: den er den ekte. Skriptets egen Python kjøres med 3.9. Etterligningen noterer umasken den ble startet med. | Linux i skyen, 06.10 kl. 18:23Z | Grønt, 133 av 133, 466 sekunder. (Tredje runde: 118 tester grønne kl. 17:02Z.) |
| De samme, og én test til: haven-deploy blir ikke ferdig, og låsen kan ikke leses av ops. Da skal fila ikke legges tilbake. | Linux i skyen, 06.10, startet kl. 20:49Z | Grønt, 134 av 134, 496 sekunder. Skriptet er det samme (SHA-256 `2e0fac7c…bf1fe39`). Bare testfila er endret. |
| 145 bevisste feil i skriptet, én om gangen, mot de 133 testene | Linux i skyen, 06.10 kl. 18:32–20:42Z | 144 av 145 fanget. De 29 som er nye eller endret i fjerde runde, gikk først: alle 29 fanget (kl. 19:05Z). Kjøringen stopper på første røde test for hver feil, så det er den testen som står i resultatet. Et første forsøk med bare de 29 (startet 18:24Z) ble stoppet etter sju minutter og slått sammen med denne kjøringen. **Ikke fanget:** feilen som legger fila tilbake når haven-deploy ikke har meldt seg ferdig. Alle 133 testene var grønne med den. Årsaken er målt én gang, 06.10 kl. 21:27Z, etter byttet (forfatterens avlesning): med feilen innsatt og tilfellet testene prøvde, skrev skriptet «MERK: låsen til haven-deploy holdes på verten: en utsetting går. Fila /etc/haven/staging-correspondence-invites.env er ikke rørt nå.» Låsen stoppet altså tilbakeleggingen der, og utfallet ble det samme med og uten feilen. |
| Den ene feilen som ikke ble fanget, mot den nye testen | Linux i skyen, 06.10 kl. 20:48–20:57Z | Den nye testen er grønn mot skriptet og rød mot feilen, kjørt for hånd på en kopi (kl. 20:48Z) og i en ny kjøring av bare den feilen med verktøyet («1 av 1 fanget»). De 144 andre er ikke kjørt på nytt med 134 tester. |
| Feilinnsettingen for tredje runde (127 feil) | Linux i skyen, 17:02–17:53Z | Stoppet etter 72, da skriptet måtte endres: 70 fanget. De to som ikke ble fanget, var prøvestartens to vilkår hver for seg. Nå prøver én test hvert vilkår alene. |
| Uavhengig kontroll nr. 2 og etterkontroll (`panel/FABEL_BYTT_UTGAVE5.md`, `panel/FABEL_BYTT_UTGAVE5_ETTERKONTROLL.md`) | Claude Fable, 06.10 | Ingen funn blokkerer. Ti og åtte merknader. De er rettet, bortsett fra dem som står under «Ikke bevist» her og i `HAVEN-Deploy/_handoff/HD-0006/LES-MEG.md`. |
| Uavhengig kontroll av tredje runde (`panel/FABEL_BYTT_UTGAVE5_DELTA3.md`, 17:45Z) | Claude Fable, fikk bare endringen | Ingen funn blokkerer etter kontrollørens dom. Sju merknader. Den første, umasken, sto som et forbehold med to utveier; denne tråden har behandlet den som en feil som måtte rettes før byttet. Alle sju er rettet i fjerde runde. Ett vindu fra merknad 5 kan ikke prøves. |
| Uavhengig kontroll av fjerde runde (`panel/FABEL_BYTT_UTGAVE5_RUNDE4.md`, fila er fra 18:54Z) | Claude Fable, fikk bare endringen | Ingen funn blokkerer. Seks merknader, ingen av dem feil i koden: `utfoer` er aldri kjørt mot verten, prøvestarten viser fem sekunder og ikke 35, to vinduer kan ikke treffes av testene, og rekkefølgene av svar om låsen er prøvd med innlagte svar og ikke med det ekte spørsmålet. Kontrollen sier at de sju merknadene fra forrige er svart på. |
| Kontroll av dokumentene mot kildene (`panel/FABEL_DOK_RUNDE4.md`, fila er fra 19:21Z) | Claude Fable | Tall, klokkeslett, jobb-id-er, sjekksummer og sitater stemte. Elleve avvik: slutninger skrevet som målinger (umask gjennom sudo, ventingen i prøvestarten), kontrollenes merknader gjengitt for sterkt, og låsesvaret «ukjent» utelatt. Rettet her, i `STATUS.md` og i `HAVEN-Deploy/_handoff/HD-0006/LES-MEG.md` samme kveld. Rettelsene er ikke kontrollert på nytt. |
| `bash -n`, med og uten UTF-8 | macOS 27.0, `/bin/bash` 3.2.57 (jobb `b23-hd0006-syntaks-3-20261006`, 17:04Z, og `b27-hd0006-syntaks-4-20261006`, 18:25Z, etter fjerde runde) | Grønt begge ganger. `evidence/SYNTAKS-3-20261006.md`, `evidence/SYNTAKS-4-20261006.md` |
| `les-20261006` | Macen mot den ekte verten, som ops (jobb `b24-hd0006-les-1-20261006`, 17:05Z, og `b28-hd0006-les-2-20261006`, 18:26Z, etter fjerde runde) | Grønt begge ganger, uten HINDER. `evidence/LES-1-20261006.md`, `evidence/LES-2-20261006.md` |
| `proevestart-20261006` | Macen mot den ekte verten, som ops (jobb `b25-hd0006-proevestart-1-20261006`, 17:06Z, og `b29-hd0006-proevestart-2-20261006`, 18:27Z, etter fjerde runde) | Grønt begge ganger. `evidence/PROEVESTART-1-20261006.md`, `evidence/PROEVESTART-2-20261006.md` |
| ssh-innstillingene på Macen for kallene til verten (`les-ssh-oppsett.sh`, `ssh -G`) | Macen, kontakter ingen maskin (jobb `b26-hd0006-ssh-oppsett-1-20261006`, 17:28Z) | Hvert kall er sin egen forbindelse: ingen `ControlPath`, for ops og for root. `ServerAliveInterval` 10 og `ServerAliveCountMax` 3 gjelder. `evidence/SSH-OPPSETT-1-20261006.md` |
| Umask og rettigheter på verten (`les-proevefiler.sh`) | Macen mot den ekte verten, som ops, bare lesing (jobb `b30-hd0006-proevefiler-1-20261006`, 18:29Z) | En økt hos ops uten terminal har umask 0002. De fire filene fra de to prøvestartene har rettighet 600. Loggene er endret fem og seks sekunder etter startmerkene. Låsemappen har 711, låsefila og holder-fila 644. `evidence/PROEVEFILER-1-20261006.md` |
| sudos standardinnstillinger for ops (`les-sudo-standard.sh`, `sudo -n -l`) | Macen mot den ekte verten, som ops, bare lesing (jobb `b31-hd0006-sudo-standard-1-20261006`, 19:25Z) | `env_reset`, `mail_badpass`, `secure_path` og `use_pty`. Ingen umask-innstilling og ingen `umask_override`. sudo 1.9.15p5. `evidence/SUDO-STANDARD-1-20261006.md` |
| Spørsmålet om låsen i sju filtilstander, stilt som en bruker uten rett til fila | Linux i skyen, 18:16Z | Som ventet: fri, ukjent (fil 600), ukjent (mappe 700), mangler (ingen fil), mangler (ingen mappe), holdt, ukjent (mappe 700 uten fil). Testene kjører som root og ser forbi rettighetene, derfor dette forsøket ved siden av. `evidence/FORSOEK-LAAS-MANGLER-20261006.txt` |
| `toerr-20261006` (leser også som root) | Macen mot den ekte verten, som ops og root (jobb `b32-hd0006-toerr-3-20261006`, 19:42Z) | Grønt, uten HINDER. `evidence/TOERR-UTGAVE5-1-20261006.md` |
| `utfoer-20261006` (byttet) | Macen mot den ekte verten, som ops og root (jobb `b33-hd0006-utfoer-1-20261006`, 21:05:35Z–21:06:45Z) | Grønt: `<!-- BYTTE FERDIG -->`, ingen HINDER eller MERK. `evidence/UTFOER-1-20261006.md` |

Fra `les` og `proevestart`:

```
2026-10-06T17:05:36Z ok  haven-deploy på verten er utgaven som er lest, og ops kan kjøre den med sudo
2026-10-06T17:05:36Z ok  verten har verktøyene skriptet bruker der
2026-10-06T17:05:37Z ok  logind lar prosessene til ops leve etter utlogging (KillUserProcesses er av)
2026-10-06T17:05:37Z ok  låsen til haven-deploy er fri: ingen utsetting går på verten nå
2026-10-06T17:05:37Z ok  lista som kjører i cellscaffold-app-1, har 5 invitasjoner: 5 er utløpt, 0 gjelder fortsatt
2026-10-06T17:05:37Z ok  den nye lista tar ikke bort noen invitasjon som fortsatt gjelder, ut over det som er godtatt
2026-10-06T17:06:59Z ok  prøvestart: skallet levde i 5 sekunder etter at forbindelsen var lukket, sudo kjørte så haven-deploy derfra uten terminal, og sluttmerket kom i loggen (kode 2, som ventet for en revisjon som ikke finnes)
```

Fra `proevestart` etter fjerde runde, og fra `les-proevefiler.sh`:

```
2026-10-06T18:27:54Z ok  prøvestart: startkallet var ferdig på under 1 sekund, og skallet ventet 5 sekunder før det kjørte sudo, så forbindelsen var lukket da. sudo kjørte haven-deploy derfra uten terminal, og sluttmerket kom i loggen (kode 2, som ventet for en revisjon som ikke finnes)
-- umask i en økt hos ops uten terminal: 0002. I et skall startet derfra (sh -c): 0002
   600  ops  0  2026-10-06 17:06:48Z  /home/ops/haven-deploy-proevestart-20261006-170648.kjoer.brukt
   600  ops  90  2026-10-06 17:06:53Z  /home/ops/haven-deploy-proevestart-20261006-170648.log
   600  ops  0  2026-10-06 18:27:42Z  /home/ops/haven-deploy-proevestart-20261006-182742.kjoer.brukt
   600  ops  90  2026-10-06 18:27:48Z  /home/ops/haven-deploy-proevestart-20261006-182742.log
   711  root  /run/lock/haven
   644  root  /run/lock/haven/haven-deploy.lock
```

**Ikke bevist**

- At byttet går likt en gang til. Selve byttet (skrivingen av linja som root, og en ekte `haven-deploy staging current --env-only` startet fra skriptet) er kjørt én gang, 06.10 kl. 21:05Z.
- Hva `cellscaffold-deploy-status`, som haven-deploy kaller til slutt, gjør med låsen, og hvilke rettigheter den gir det den skriver. Verktøyet er ikke lest. Skriptet venter inntil ett minutt på at låsen slippes før det legger noe tilbake, og kjører haven-deploy med samme umask som et vanlig kall.
- Hvilken umask haven-deploy får gjennom sudo på verten. sudo har ingen egen umask-innstilling for ops, så etter sudos standard blir det øktens (0002) lagt sammen med 0022. I testene noterer etterligningen umasken den ble startet med.
- At skallet i prøvestarten ventet, er ikke målt av skriptet. Det følger av at haven-deploy bare kjøres når ventingen gikk, og av tidsstemplene som ble lest på verten etterpå. Skriptet måler tiden på startkallet.
- At skallet som starter haven-deploy, alltid lever til den er ferdig. I byttet meldte haven-deploy COMMITTED_VERIFIED 35 sekunder etter at skriptet startet den (regnet fra to klokkeslett i utskriften), og sluttmerket sto i loggen da skriptet leste den. Det er én kjøring.
- Hvor lenge staging var utilgjengelig utenfra under byttet. Klokkeslettene er fra loggen til haven-deploy.
- At de 144 feilene som ble fanget med 133 tester, fanges med 134. En test som legges til, kan ikke gjøre en rød kjøring grønn, men det er en slutning og ikke en kjøring.
- Hvem som har laget låsemappen med rettighet 711. haven-deploy lager den med `mkdir -p` uten å sette rettigheter, og ville gitt 755 med umask 022.
- At 45 minutter holder for jobben når verten svarer tregt. Skriptet gjør rundt 40 korte kall utenom ventingen på haven-deploy.
- Tre ting er bare prøvd i etterligningen: at linja legges tilbake etter en tilbakerulling, at claimen blir stående når utfallet er uvisst, og at en annen utsetting som holder låsen, stopper byttet.

Kjente begrensninger (ting skriptet ikke gjør, eller som ikke kan prøves) står i `HAVEN-Deploy/_handoff/HD-0006/LES-MEG.md` under samme overskrift: bokstaver utenfor ASCII i en principal, låsespørsmålet som kan avvise en utsetting som starter i samme øyeblikk, to vinduer testene ikke kan treffe, og at skriptet ikke sletter noe hos ops.
