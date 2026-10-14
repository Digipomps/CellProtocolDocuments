STATUS: LEVERT

# HD-0196 h3 — admin-feedens capacity-årsak

Årsaken ligger i CellScaffolds testfixtur: tilbakekalling lukker feedens transport, men fixturen sendte deretter GET på samme transport. Eksakt `capacity`-gren var **stopped=true, inFlight=0**. Ingen in-flight-kvote var full. Fixturen er rettet uten å øke kvoter eller frister. CP og applikasjonens produksjonskode er uendret av h3.

## Kausalkontroll

På CS-basen `d726890683d1ad0ccf0f0c70d290a1fb438f01cd`, med originale vaultfiler og CP `afa8cbf98f1b49dd8adee93f61a178b360afcc40` før #63, feilet originaltesten. Første baseline og tre diagnostiske gjentakelser ga hver én test / to failure-events / exit1. Alle tre diagnostiske løp viste stopped-grenen ved GET etter revoke. Diagnostikk og kilder ble MD5-restaurert.

Den bestilte bisekten av #63 var betinget av grønn før-baseline og ble derfor ikke utløst. Mellomcommitene `7ebb4f5`, `36959ae`, `fe799b6` ble ikke runtime-testet; alle #63-endringer er ikke erklært regresjonsfrie. Den komplette transportfilen har identisk hash på afa8cbf, disse tre commitene, main97b3484 og h2503f688: kildebevis, ikke ekstra grønne testløp.

`AdminOverview`-feedens feil etter tilbakekalling utløser `BridgeBase.failFeedDelivery`, som lukker transporten. Testfixturen blandet denne lukkingen med autorisasjonskontroll ved å bruke den pensjonerte gaten. Første rettingsforsøk var fortsatt rødt: peer-gaten ble ikke fysisk lukket og sendte sen stopFeed. Diagnose viste capacity ved stopFeed. Endelig paired-close lukker begge gatenes generasjoner og undertrykker sen stopFeed slik en lukket socket gjør.

## Rettelsen og motbevis

Testen etablerer nå en separat read-kanal før revoke, beviser autorisert read før revoke, observerer fysisk lukking av feedtransporten, krever ingen videre feed-elementer og krever denied read etter revoke på den allerede etablerte read-kanalen. Begge entry-/observer-credentials testes. De eksisterende close/no-feed-fristene er beholdt, og alle tre gatene ryddes.

Tre faktiske gjentakelser på CP503f688 passerte, hver1/0. Negativ kontroll fjernet selve revoke-effekten, men beholdt gyldig revoke-ack:1 test /6 assertionsfeil /exit1, fordelt på manglende close, fortsatt feed og fortsatt read for begge credentials. Produktkilden ble MD5-restaurert. En tidligere mutant av bare den ekstra flow-guarden var grønn og brukes ikke som rødt mutasjonsbevis. Et avbrutt fixtureforsøk uten cache-eierskapsmarkør startet ingen test og telles ikke som rød test.

## Andre blokkeringer i fullporten

- Parity-proveniens: foreldet CP-referanse oppdatert til503f688 etter byte-identisk kontroll av begge refererte kilder fra h2s14181968 og kopiens a2b1fc2. Corpuscaser, klassifikasjoner og assertions er uendret. Pinnevakt og tre reelle matrix-tester passerer. Native GUI-paritet er ikke påstått.
- Første h2-fullport fullførte30/32. To forged-owner-forventninger brukte gammel feiltype. Bare de berørte greinene kontrollerer nå den konkrete pre-readiness `CellAuthorizationError.denied`, inkludert allowed=false, mismatch-path/reason og eksakt cell/keypath/permission. Ekte eier-recovery/count1 og øvrige korrespondanseavslag beholdes. Avvisningsfunksjonen er kildeidentisk før #63, på main97 og h2; de to konsumenttestene ble ikke runtime-kjørt på afa8cbf. Fokus6/0, deretter komplett32/32 på559bf3f8.
- Første #286-kopiport fullførte32/33, med rød person-bridge-bolk27. Uendret case ga grønn/grønn/rød på tre gjentakelser. WebSocketKit/NIO-kilden viser at connect-futuren kan fullføre før socketinstallering. Eventloop-basert25ms diagnose traff nøyaktig `missing-underlying-before-send` og ga1 test /2 failure-events /exit1; kilden MD5-restaurert. Testtransporten bruker nå synkron callback på socketens eventloop og separat readinesspromise, venter på faktisk atomisk installering, feiler pending setup ved close og avviser sen installering. Assertions/frister uendret. Tre gjentakelser med begge person-caser ga6 parent-tester /0 feil.
- Neste h2-fullport fullførte31/32: bolk10 aborterte før Swift/teststart fordi ubevoktet `du|awk` kunne feile ved ufullstendig cachemåling. Kopiens eksisterende guarded måler ble portert; shellkontroll viser gammel exit1 uten runner, rettet exit0 med unknown-metric og rettet ekte runner-exit7 bevart. Ingen faktisk Swift-test ble simulert som akseptanse. Ny komplett32/32 ble kjørt på nytt hode.

Feilede diagnostikkforsøk er bevart: første person-delay traff NIOLoopBound-precondition/signal5 uten gyldig grenmarkør, og en wrapper ble feilaktig endret mens den kjørte. Dette forsøket er ikke grenbevis. Etterpå ble hvert køskript og hver wrapper frosset før oppstart. En første shellprobe manglet executablebit og er heller ikke akseptert årsaksbevis.

## Endelige hoder og porter

| Kandidat | Hode | Port/publisering |
|---|---|---|
| CellProtocol h2 | `503f6882db16160a8709277e957d70f343414777` | Uendret, rent; [kladd #65](https://github.com/Digipomps/CellProtocol/pull/65), live CI5/5 SUCCESS |
| CellScaffold h2+h3 | `651c7d9880fd3eda0765a2b69c4081ee115d656b` | Komplett32/32, exit0; publisert i [kladd #307](https://github.com/Digipomps/CellScaffold/pull/307) |
| Separat #286-kopi | `6b6c5bb14a2f7ec2ad8116983db0461141108625` | Komplett33/33, exit0; [kladd #286](https://github.com/Digipomps/CellScaffold/pull/286) oppdatert etter porten |

H2-full-r4:2572 faktiske loggede XCTest-utførelser =2561 bestått +11 skip,0 feil. Komplett32/32 og TEST_EXIT0. Bolk10 kjørte111 tester, admin14 parenttilfeller/1skip/0feil, strict-signering7/0, person-bridge2/0; ekte T1 og literal-/dekningkontroller passerer. Testtall inkluderer loggede child-kjøringer. Komplette case-signaturer uten linjestartanker er avstemt eksakt mot hver xctest-bundle-footer; Selected tests-footere dobbelttelles ikke. Tidligere prefikslinjetall2520/2521 undertelte flettet stdout og er korrigert i TESTRESULT.

Kopi-full-r2: alle33/33 grønne, TEST_EXIT0. 2578 faktiske loggede utførelser = 2567 bestått +11 skip,0 feil, avstemt med samme metode. Person-bridge-bolk27 grønn, admin-/strictbolk32 grønn og siste korrespondansebolk33: Host4 +native2 =6/0. Begge nye hoder ble publisert etter sluttportene og remote-head/forfar-kontroll, med vanlig fast-forward-push.

Ni felles endrede vault-/test-/corpus-/wrapperfiler er byte-identiske i begge sluttkandidater. Originalt #286-arbeidstre er beholdt på1e0634fed4baf9ff07dbaf5278345f31b53f6a02; bare separat kopi brukes til gate/push. Ingen force-push.

CP-grunnmur1671 utførelser (1666 bestått +5 skip) og fem grønne CI-sjekker er h2-evidens på uendret CP-hode. Ingen h3-CP-endring utløste ny CP-grunnmur/CI; livehode og CI er kontrollert på nytt. Ingen CP-standalone regresjonstest er lagt til, siden den påviste årsaken og rettingen ligger i CS-fixturen.

## CI og rammer

CellScaffold307s package-release-policy avviste både den tidligere kandidaten og slutt651c7d98 fordi CellProtocol er pinnet med revision fremfor release-tag. Eksakt CP65-hode er bestilt i dette oppdraget; tag/release er forbudt. Policyen er ikke svekket. Lokal Swift-port er ikke grønn samlet CellScaffold-CI eller release-klar kandidat. CI-snapshot etter sluttpush: #307: 1 ferdige OK/nøytrale, 1 røde/avbrutte, 1 ventende/kjørende. #286: 1 ferdige OK/nøytrale, 0 røde/avbrutte, 0 ventende/kjørende. Dette er en observert status, ikke en ferdig grønn CS-CI-port. Evidens: final-ci-observation.json og cs307-final-policy-failed.log (eksakt release-tag-avslag også på slutthodet).

Alle bygg gikk gjennom godkjent bounded runner og diskguard med uendret reserve, prosent-/GiB-grense, jobs og cachecap. Ingen egen isolert cache-root opprettet; egne små private temp-prober ble fjernet. Ingen merge, tag, deploy eller installerbygg utført. Ingen G3-akseptanse påstås.

## Evidens og læring

Evidensrot: `HAVEN-Deploy/_handoff/HD-0196/h3/`. Baseline/gren: bisect-afa-output.md, diagnostic-afa-output.md og transport-source-hashes.json. Fixture/motbevis: feed-r2-queue.md og revocation-effect-mutant-queue.md. Parity/denial: parity-source-comparison.json, parity-copy-source-comparison.json, owner-guard-function-hashes.json, security-focused-queue.md. Person-race: websocket-callback-source.json, nio-upgrade-order-source.json, person-race-r2-queue.md og person-fixed-queue.md. Cachemåling: cache-metric-probe.json. Sluttporter: full-r4-queue.md, copy-full-r2-queue.md og respektive scaffold-*/test.log/suites. Hoder/kildelikhet: final-candidate-heads.json og final-source-comparison.json. Publisering/CI: publication-preflight.json, published-307.json, published-286.json og cp65-final-checks.json. SHA256-manifestet beskriver endelig bevart evidens.

Fem gjenbrukbare læringer er fanget og applied i kanoniske transport-, kontrakttest- og Mac-shell-skills: feed-retirement, telling av hele fullporten, WebSocket-installering, uforanderlige kjørende skript og flettet XCTest-stdout. Desktop-ZIP-er er bygget. Hjemmedistribusjon ble avvist av filesystem-sandboxen; læringene er ikke feilaktig markert synced.
