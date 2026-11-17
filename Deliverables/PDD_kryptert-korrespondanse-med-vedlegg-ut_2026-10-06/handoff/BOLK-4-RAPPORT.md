# Bolk 4 s2 — native relasjonsceller på HD-0190-kandidaten

Bygger på HD-0190-kandidaten og venter på den. Implementasjonen er levert som kladd-PR [#286](https://github.com/Digipomps/CellScaffold/pull/286) mot main, hode `1e0634fed4baf9ff07dbaf5278345f31b53f6a02`. **Fullporten er ikke grønn.** Ingen merge, deploy, installerbygg eller vertsendring.

## Kilde og avgrensning

Gren `codex/korr-staging-paa-hd0190-20261007`, fra `hd0190/on-release-2026.9.7` på `d7268906`. CellProtocol er pinnet til publisert PR #63-hode `a2b1fc2f8f6c1b9d7887a018d89c959138418d2d`; ingen CP-tagfil forelå. Dette dependency-hodets fire CI-checks er SUCCESS. Ingen kildeendring i CellProtocol, HavenAgentD, Binding eller HD-0196. Andre HD-0190/release-arbeidstrær er urørt.

Host/fabrikk bruker kandidatens ScaffoldBridgeRuntime og AuthenticatedBridgeIngress. Stabile UUID-er registreres som scaffoldUnique, snapshots lagres atomisk og trusted vedleggsrot bindes ved opprettelse og restore. Én sekunds checkpoint lagrer også timerstyrt rydding. Fabrikken krever requesterens nøkkelbevis og bare offentlig X25519-input; navn og private nøkler blir hos klienten.

For sign-only requester binder hostlaget manglende offentlig X25519 bare ved typed join.request etter signaturkontroll med den opprinnelige requesterens signing-nøkkel samt UUID/fingerprint/cellematch. Offentlig kopi beholder samme bevisproxy. Ingen ny sessionprincipal, grant, privat nøkkel eller hostvault importeres; CP avgjør fortsatt invitasjon, replay og medlemskap. Kanonisk CP-oppfølging av sign-only join er ikke tatt inn fra upublisert kilde.

## Krav og prøver

Bevis-prefiks nedenfor: `HAVEN-Deploy/_handoff/KORR-UT/bolk4/`.

| Krav | Test | Utfall | Bevis |
|---|---|---|---|
| A2/A3: opprette, adresse, stabil UUID og reload | E/H/I separate nøkkellagre, ekte lokal Vapor og autentisert bro | Bestått | full-r3/suites/bolk-33.log; e2e-r11/e2e.log |
| A3: innmelding og eierbeslutning | Fem ugyldige wirepayloads før gyldig pending, nøkkelkode, selv-godkjenning avvist, riktig nøkkels private avtale, replay | Bestått; privat-resultat GET for feil principal har transportbegrensning nedenfor | full-r3/suites/bolk-33.log |
| Tekst, vedlegg >1 MB begge veier, abonnement | Fire message Flow-hendelser; 1 100 037-byte filer, byteidentisk henting | Bestått i begge native scenarioer | full-r3/suites/bolk-33.log |
| Verten kan ikke slippe inn/åpne; ikke-medlem ingen historie/message Flow; disk uten plaintext/filnavn | Vertsignert fremmed avtale avvist, manglende deltakeridentiteter, decrypt avvist og markerskanning | Bestått | full-r3/suites/bolk-33.log |
| B2: avsenderens trusted undercelle og 10 GB reserve | Før create/prepare/upload; 9 999 999 999 bytes avviser før protokollskriving | Bestått | Host-tests; full-r3/suites/bolk-33.log |
| B2: eksplisitt filtilbakekall | To filer gir36 chunks, attachments.revoke fjerner målfilens18; målfil fetch avvist | Bestått | full-r3/suites/bolk-33.log; fysisk før/etter |
| A6: kald gjenoppretting og utløp | To uavhengige diskbilder etter stanset Vapor/runtime, historie/henting,62sek vent; ett bilde uten klientreconnect | Bestått:0 konvolutter/0 chunks | full-r3/suites/bolk-33.log |
| Helse uten innhold | Aggregate configured/ready/storageAvailable; lagringsfeil gir503 | Bestått | Host-tests |
| Offline sikkerhetskopi | Kopi/hash/tar-kontroll og nekt overskriving; C/en_US.UTF8 | Bestått lokalt | backup-selftest.txt; backup-correspondence-state.sh i foreldremappen |
| Alle lokale bolker | Full-r3 alle33 på PR-hodet | 32/33 grønne; bare bolk32 rød; exit1 | full-r3/full.log; full-r3/suites/bolk-32.log |

Rå native r11: Ingress5 + Host4 + native2 =11tester/0feil. Endelig localhost-fixture: Host4 + native2 =6tester/0feil i bolk33; hele porten avsluttet 08.10.2026 kl.04:30Z. Verdifri native utskrift er i `evidence/bolk4-staging-lokalt.txt` i denne PDD-mappen.

Full-r1:29/33 grønne; full-r2:30/33 grønne. R1s metadata-/parity-proveniensfeil er rettet med ekte detached dependency-checkout og verifisert metadata-lock; begge porter er grønne i r2/r3. Parity-pin er oppdatert, schema/config/native renderer er kildeidentiske og fixtures/klassifikasjoner uendret. R2s person-brofeil gjentok seg ikke i r3. Bolk32 feiler fortsatt på fire eksisterende AdminNonOwnerBridgeTests: browser-holder origin/domain får closed, observer-feed feiler, og fresh web-prosess seed avslutter med feil. Testene og HD-0196-koden er urørt.

Nye native prøver var røde under utviklingen: kald expiry beholdt54 chunks før trusted-root-pinnen, og join ble avvist før binding av den signerte offentlige nøkkelkonteksten. Rålogger er bevart. Min ekstra forventning om at agreement.revoke skulle slette en annen gyldig fil for eieren var feil; den er erstattet med direkte attachments.revoke, fysisk før/etter og separat avvisning av det tilbakekalte medlemmets historie. Ingen eksisterende basetest er fjernet eller svekket.

Transportbegrensning: feil principals private join-resultat GET returnerer tom payload. CP BridgeBase fullfører ikke GET-future ved nil payload, så klienten får30sek timeout. Isolert negativ prøve krever ingen avtale, med riktig principal som positiv kontroll og lik avtalesignatur. Det er ikke vist som ren strukturert denial. Den første hypotesen om SET som ødela kanalen var feil og er korrigert; ingen brokilde er endret.

## CI og eventuell utsetting

Egen Swift/image-CI er ikke kjørt eller hevdet grønn. `[skip ci]` er brukt på den blokkerte kladden med rå commit-pin; tagpolicy er beholdt. Automatisk Notify PyCellProtocol dispatch-check er SUCCESS og er ikke et funksjonelt testbevis. Den opprinnelige remote-locken er committet med bare CP-pinnen endret; lokale verifiserte CP/DiMy-overrides beviser ikke remote release-tag-resolusjon. Observasjonell du-metrikk tåler samtidig cache-GC uten å skjule Swift-status; kapasitetsvakt/leie/tak beholdt, fire probevarianter i begge locales PASS.

Utsetting krever grønn samordnet CP/HD-0190/fullport, privat vedvarende datavolum med `HAVEN_CORRESPONDENCE_DATA_ROOT`, eksisterende host-identitet via `CELL_SCAFFOLD_OWNER_CONTEXT`, kanonisk `CELL_SCAFFOLD_BRIDGE_ORIGIN` med TLS/WSS/proxy og skriverettighet. Nye relasjoner og prepare/upload krever10 000 000 000frie bytes; reads/revoke/expiry fortsetter under terskelen. Offline backup-skriptet er `HAVEN-Deploy/_handoff/KORR-UT/backup-correspondence-state.sh`; stopp skriving før bruk. Den gamle assistant-databasen har separat backupansvar.

HD-0196 kan skilles i implementasjonen: native klient bruker eget nøkkellager og ingen browser-holder. Trygg separat generell utgivelse er ikke vist med den røde admin-brobolken. Denne jobben utsetter ikke noe.

## Ikke vist

Staging, vertsmutasjon, merge/deploy, installerbygg, faktisk mottakerpakke,200MBfil/minnetopp, native GUI, OS-/prosessomstart eller grønn fullport/egen Swift-CI. «Kald» betyr stanset/gjenopprettet lokal Vapor/runtime og uavhengig diskbilde. Ingen melding sendt til mottakere.

STATUS: STOPPET — fullporten feiler i kandidatens eksisterende admin-brobolk32; relasjonscellene og native prøver er levert i kladd-PR286
