# Rotårsaksvurdering: «Run document live collaboration proof»

Dato: 2026-09-11. Kjøring **34574674480**, jobb **103184321906**, CellScaffold **649255bb777b3a5135bd9c50512d3074bd23935b** (#238).

**Den konkrete CI-rotårsaken er ukjent.** Hypotesen om den ubegrensede konfliktløkken som årsak til denne kjøringen er avkreftet i Kjetils logganalyse og legges bort. Det bekreftede feilpunktet er lagret-status i sesjon A etter første tekstinnskriving, ikke bygg, oppstart eller B-sesjonens senere redigering. Uten Playwright-tracen kan jeg ikke fastslå siste statustekst, faktisk HTTP-tid eller hvorfor kjøringen varierer.

Kildeanalysen og isolerte tester bekrefter to **separate kodefeil**: HTTP-timeouten opphører før en vellykket responskropp er ferdig lest, og konfliktgrenen kan sende samme avviste operasjon ubegrenset. Begge har foreslått diff og før/etter-test nedenfor. **Ingen av diffene er en bevist reparasjon av kjøring 34574674480.** Ingen timeout økes, og ingen kildekodeendring er anvendt i CellScaffold.

## Grunnlag og arbeidsgrenser

- Alle `CellScaffold/...:linje` nedenfor viser til git-objektet `649255bb777b3a5135bd9c50512d3074bd23935b`, lest med `git show`/`git grep`. Dagens lokale kildefiler er eldre og til dels endret.
- CellScaffold HEAD: `1dbdee23f5272a3485a4c6b8263c84c4351eaf28`. CellProtocolDocuments HEAD: `f6aa54460d82ae52ede8a7475c4dff133175d4a7`. Begge repoene har mange eksisterende endringer. Bare denne rapporten er oppdatert i arbeidsrepoene.
- Ingen push, checkout, switch, rebase, merge, reset, stash, Docker, Swift-bygg, Swift-test, køjobb, CI-rerun eller deploy er kjørt. Testene er korte Node-kjøringer på kildekopier i `/private/tmp`.
- Bygggrensen finnes også i `CellProtocolDocuments/Book/haven_lessons_register_v0.json:456–461` (`lesson.codex-workspace-write-cannot-build-cellscaffold`).
- Loggopplysningene nedenfor kommer fra Kjetils gjennomgang i oppgaven, ikke en ny fullstendig loggnedlasting i denne økten. Den tidligere rapportens utsagn om ukjent feilassertion og mulig feil ved senere bilde/chat-trinn er erstattet av det nye beviset.

## 1. Hva som er bekreftet i CI, og hva som mangler

| Spørsmål | Funn |
| --- | --- |
| Bygg | Grønt ifølge gjennomgått logg. Dokumentsteget var nådd med `steps.build.outcome == 'success'`. Workflow-vakten står i `CellScaffold/.github/workflows/admin-scaffold-image.yml:339–340`. |
| Oppstart | Begge sesjoner passerte synlig `Dokumenttekst` og `contenteditable="true"`, `CellScaffold/playwright/rich-document-live.spec.js:18–19`. |
| Feil | Samme spec, linje 23: filtrert `.document-status` ble ikke synlig innen default 15000 ms. Testen varte 20,9 s. Eneste `##[error]` var exit code 1. |
| Trafikk | Oppgaven oppgir 17 bootstrap-GET og omtrent 19 action-POST, totalt 36 rutetreff i dokumentstegets logg. Ingen varm konfliktløkke legges til grunn for denne analysen. |
| Hva A faktisk viste ved timeout | **ukjent**. Fravær av statustekster i serverloggen er ikke fravær av teksten i nettleseren: `say()` skriver bare `status.textContent`, `CellScaffold/Public/js/haven-rich-document.js:33`. |
| En action-rundes tidsbruk / samlet kødrenering | **ukjent**. Antall rutetreff er ikke tidsmålinger av forespørsel/svar. |
| Hvorfor akkurat denne CI-feilen er ikke-deterministisk | **ukjent**. Mulige tids- og rekkefølgeavhengigheter er beskrevet nedenfor, uten å erklæres som CI-årsak. |
| Kausal diff og rød/grønn regresjon for CI-hendelsen | **ukjent** inntil trace/payload viser den faktiske banen. Testene nedenfor gjelder avgrensede, reproduserte kodefunn. |

En presisering av premisset: Lagret-teksten settes ikke bare på slutten av `accept()`. Den settes også i `pump()`-catch når den sendte operasjonen allerede er fjernet fra køen, på **`CellScaffold/Public/js/haven-rich-document.js:113–114`**, og denne grenen sjekker ikke `stopped` før statusen skrives. En observert lagret-status beviser derfor ikke alene at siste `accept()` fullførte normalt.

## 2. Spørsmål 1: veier uten fullført accept, og busy som blir stående

Alle adapterreferanser i denne seksjonen gjelder `CellScaffold/Public/js/haven-rich-document.js`.

| Bane etter at tekst er lagt i kø | Kilde og konsekvens |
| --- | --- |
| En tidligere send er uavklart | Linje **100–108**: `busy=true` settes før `await options.send(payload)`. Så lenge promiset verken fullføres eller avvises, nås ikke `unwrap`, `accept`, catch eller linje 120. Nye teksthendelser legges i kø på **264–266**, men deres pump stopper på busy-vakten. Adapteren har ingen egen frist for dette await-et. |
| Flow kvitterer før HTTP-svaret | Linje **77–78,97,100**: Flow kan fjerne første køelement og kalle pump, men busy er fremdeles true. Hvis det finnes en annen endring i køen, blir den stående til send-promiset fullføres. Hvis hele køen allerede er tom, kan `accept` likevel vise lagret på **96** selv om busy fortsatt er true. |
| Send eller unwrap kaster, operasjonen er fortsatt i køen | Linje **45–48,112–118**: `accept` kjøres ikke for dette svaret. Feilmelding vises; catch returnerer **med busy=true**, men callback på **117** setter busy=false etter 2500 ms og pumper igjen. Dette er en bevisst ventetilstand, ikke i seg selv en permanent lås. Ved nye feil gjentas ventingen uten øvre grense. |
| Send/accept kaster, men Flow eller accept har allerede fjernet operasjonen | Linje **113–114** setter busy=false umiddelbart, oppdaterer status og pumper neste element før return. Denne catch-returen etterlater ikke busy=true. |
| Serverstatus er verken conflict, accepted eller duplicate | Linje **111** setter stopped og avvisningsstatus uten å kalle accept. Linje **120** slipper busy; linje **121** og senere vakt på **100** hindrer videre sending. Dette er et eksplisitt stopp, ikke en glemt busy-reset. |
| Hull i historikken | Linje **73** setter stopped, viser meldingen om ufullstendig historikk og returnerer fra accept. Ved normal retur til pump kjøres **120** fortsatt. Stopped tilbakestilles ikke i denne controllerens levetid. Videre brukerinput kan fortsatt endre status på **266**, siden den handleren ikke sjekker stopped. |
| Tidlig accept-retur | Linje **52–56**: disposed; manglende/feil snapshot-schema; eldre sequence for samme documentId; eller manglende Quill/chat/help. Dersom accept ble kalt fra pump, slipper pump likevel busy på **120** etter normal retur. En ubrukelig `current` kan derfor la køen stå og retry fortsette, ikke nødvendigvis låse busy. Chat/help har ingen teksteditor som enqueuer her. |
| Kast inne i accept | Delta-komponering/-transformasjon, Quill eller notat/markørrendering på **74–95** kan avbryte før statuslinje **96**. Når accept kalles i pump-try, går kastet gjennom **112–118**; som separat `controller.update` har det ingen lokal catch i accept. Hvilket eventuelt kast CI hadde er **ukjent**. |
| disposed | `destroy()` på **280** setter disposed og kansellerer retry-timeren. En busy-verdi kan da bli stående i den gamle controlleren, men den er ikke lenger en aktiv flate. Ny controller må laste/gjenopprette eget utkast. Om renderer remountet i CI er **ukjent**; documentId-bytte håndteres i `CellScaffold/Public/js/skeleton-runtime.js:2808–2814`. |
| `!confirmed` / tom kø | Vakten på **100** er normal. Ved ordinær brukerinnskriving er `!confirmed` allerede filtrert bort på **265**, og confirmed nullstilles ikke etter initialisering. Tom kø betyr ingen usendt tekst; en annen melding kan likevel ha overskrevet lagret-status. |
| Synkront kast før try | Busy settes på **101**, men try begynner først på **107**. Et kast på **102–106** ville derfor etterlate busy=true. De normale køelementene er vanlige objekter, og `saveDraft` fanger lagrings-/JSON-feil på **36–39**. Ingen vanlig utløsende bane eller CI-observasjon for et slikt kast er funnet. |

**Svar: Ja, busy kan bli stående true**, særlig ved et uavklart send-promis. De to vanlige catch-returene har derimot hver sin eksplisitte mekanisme for å slippe busy. Det er derfor ikke begrunnet å bare flytte `busy=false` inn i en generell finally: det ville endre retry- og serialiseringsoppførselen, og løser ikke et await som aldri fullføres.

### Bekreftet hull i HTTP-timeouten

Hele avhengighetskjeden er kildebelagt:

1. `CellScaffold/Public/js/haven-rich-document.js:108` venter på `options.send`.
2. `CellScaffold/Public/js/skeleton-runtime.js:2840,5564–5569` returnerer resultatet fra rendererens `onAction`.
3. Dokumentgrenen i `CellScaffold/Public/js/porthole-webo.js:8178–8182` kaller `requestActionPayload(..., 30000)` direkte.
4. HTTP sendes via `CellScaffold/Public/js/porthole-webo.js:9754–9762,10070–10076`.
5. `fetchJSON` oppretter AbortController/timer på **10030–10035**, venter på Fetch på **10038**, men bruker **`return response.json()` uten await på 10057**. Finally på **10063–10065** slår dermed av timeren mens JSON-body-promiset fortsatt kan være uavklart.

Et HTTP-200-svar med mottatte headere, men en responskropp som ikke blir ferdig, kan derfor beholde busy og tekstkøen uten en aktiv timeout. Isolert regresjon bekrefter dette: originalen er fortsatt `pending` etter simulert 30000-ms-frist; varianten med await avviser med `Request timed out after 30000ms.`.

Dette er **ikke bevis for CI-årsaken**. Assertionen feiler allerede etter 15000 ms, mens dokumenttransportens nominelle frist er 30000 ms. Selv en korrekt transporttimeout ville ikke nødvendigvis ha utløpt før assertionen. Om noen responskropp hang eller var treg i denne kjøringen er **ukjent**.

## 3. Spørsmål 2: 19 POST-er og 15 sekunder

**Faktisk varighet per POST i CI: ukjent.** Det er ikke riktig å beregne den som `15 / 19` eller `20,9 / 19`. Vi mangler start/slutt for hvert kall, hvilket vindu kallene tilhører, kommando-kind, operationId, og hvilke forespørsler som var samtidige. Bootstrap-trafikken går også i to sesjoner og kan overlappe tekstsendingene.

Kildekoden gjør terskelhypotesen mulig, men ikke bevist:

- Testen bruker `keyboard.type(marker)` på `CellScaffold/playwright/rich-document-live.spec.js:21–22`. Markøren er 32 tegn med et 13-sifret Date.now(). Adapteren enqueuer hver Quill-`text-change` separat på `CellScaffold/Public/js/haven-rich-document.js:264–266`; pump sender ett køelement om gangen på **100–108**. Det finnes ingen sammenkobling av ventende deltaer her. Faktisk antall Quill-hendelser i CI er **ukjent**; det må leses fra operasjonene, ikke likestilles blindt med tegnantallet.
- Dermed kan normal kødrenering kreve mange seriellbehandlede kall. Eksempelvis ville 32 endringer med 0,5 s hver bruke omtrent 16 s før tilleggskostnader; dette er kun regning for å vise mekanismen, **ikke en CI-måling**. En del kan være lagret allerede mens typing pågår.
- En akseptert endring kan innebære persistens, gjenlesing og sammenligning før svar: `CellScaffold/Sources/App/Cells/RichDocument/RichDocumentCell.swift:89–91,105,113–123`. Presence deler lås og persistensbane. Kostnaden på løperen er **ukjent**.
- Workflowen velger `ubuntu-24.04` på `CellScaffold/.github/workflows/admin-scaffold-image.yml:36`. Opplysningen om to kjerner kommer fra oppgaven; CPU-belastning og faktisk ventetid er ikke målt her.

**Var 15 s bevisst? Ukjent.** Koden velger den ikke eksplisitt på linje 23; assertionen arver `expect.timeout = 15000` fra `CellScaffold/playwright.config.js:23–24`. Hele testens frist er 90000 på **22**. Synlig editor velger 45000 på spec-linje **18**, og de etterfølgende innholdsassertionene velger 30000 på **24,26,40–47**. Specen kom inn med #238; verken den eller den gjennomgåtte operasjonsbeskrivelsen begrunner en særskilt 15-sekunders lagringsfrist. Manglende eksplisitt override er bekreftet; forfatterens hensikt er ikke det.

**Det foreslås ingen timeoutøkning.** For å konkludere «bare en terskel» må vi se sammenhengende normale aksept/kvitteringer, gyldig fremdrift og når siste køelement faktisk ble bekreftet i forhold til starten på assertionen. En trace som slutter ved timeout, kan vise uferdig kø og langsomme svar, men ikke alene bevise når en avbrutt operasjon senere ville blitt ferdig.

Når tracen er tilgjengelig, mål hver action fra request-start til response-end, skill delta/presence/andre kall, og sammenhold operationId og `current.events`. Serveren legger allerede ved `actionDiagnostics.durationMs`, jf. `CellScaffold/Sources/App/Controllers/PortholeWebSessionSupport.swift:96–107,3198–3211,3491–3499`. Det må sammenlignes med nettleserens totale tid; det er ikke det samme som full HTTP-/body-tid. Ikke bruk tidspunktet hvor cleanup skriver serverloggens siste 200 linjer som request-varighet (`CellScaffold/.github/workflows/admin-scaffold-image.yml:355–361`).

## 4. Spørsmål 3: pendingMetadata og presence

**Ingen direkte klientlås:** `pendingMetadata` er et kart for å gjenbruke samme konvolutt, ikke en kø pump venter på. `sendMeta` setter eller leser ikke busy; det sjekker bare latest/disposed og kølengde før sending, `CellScaffold/Public/js/haven-rich-document.js:123–130`. Dokumentgrenen går direkte til HTTP og hopper over Portholes vanlige `runAction`, `CellScaffold/Public/js/porthole-webo.js:8178–8190`. En hengende presence-request hindrer derfor ikke at senere tekst starter sin POST. Dette er reprodusert i kontrollflyttesten.

**Indirekte forsinkelse er mulig:** Et presence-kall som startet da køen var tom, kan fortsatt være underveis når brukeren skriver. Både presence og delta må gjennom samme `mutationLock` og persistens-/readback-bane i `CellScaffold/Sources/App/Cells/RichDocument/RichDocumentCell.swift:89–91,113–123`. Låseventing, lagring og konkurranse om nettleser/serverressurser kan forsinke tekst. Faktisk presence-trafikk, låseventing og forsinkelse i CI er **ukjent**.

**Metadataretensjonen er bekreftet, men er ikke en tekstlås:** `CellScaffold/Public/js/haven-rich-document.js:126–135` beholder pending-posten dersom send eller unwrap kaster. Neste kall med samme kind/fields får samme operationId og gamle baseRevision. En tolket conflict-respons sletter derimot posten på **131**, før conflict-meldingen på **133**. Blind sletting i catch ville også fjerne konvolutten som trengs for idempotent retry etter en usikker kvittering; det foreslås ikke her.

**Presence kan endre status etter at tekst er lagret:** Et allerede startet metadata-kall kan komme tilbake etter siste tekstkvittering. Conflict på **133** overskriver lagret-status, selv om tekstkøen er tom. Catch på **135** kan gjøre det samme med en feilmelding. Dette er deterministisk reprodusert ved å styre svarrekkefølgen; om det skjer i en virkelig test avhenger av timing og neste Flow/bootstrap-oppdatering. Det innebærer ikke nødvendigvis at all polling i 15 s ville misse lagret-status, og er **ikke bekreftet i CI**.

**30-sekunders-heartbeat er ikke en forklaring på denne første feilen:** Den installeres når editoren starter, etter at Quill er lastet (`CellScaffold/Public/js/haven-rich-document.js:184–186,273`). Hele den rapporterte testen var 20,9 s. Med den oppgitte varigheten og nye contexts på spec-linje **8** rekker ingen ordinær 30000-ms-heartbeat å fyre. Den første automatiske presence-muligheten er selection-change-timeren på **268–270** etter 600 ms; også den sender bare hvis køen er tom og busy=false når callbacken kjører. Tidlig presence før typing, eller presence etter at køen tømmes, må eventuelt dokumenteres i tracen. Kartet kan også få flere pågående metadata-kall fordi sendMeta ikke har noen egen in-flight-vakt.

Presence, kommentarer, hjelp og chat øker **sequence**, men ikke **revision**. Bare delta øker revision: `CellScaffold/Sources/App/Cells/RichDocument/RichDocumentModel.swift:112–153`; `documentEvents` filtreres på delta på **97**. Presence skaper derfor ikke dokumentrevisjonshull på denne serverbanen.

## 5. Spørsmål 4: artefakten og beviset som gjenstår

Tracen er **ikke lest**. Tilgangsforsøkene i denne økten ga:

- Lokal `gh api repos/Digipomps/CellScaffold/actions/runs/34574674480/artifacts`: `error connecting to api.github.com`.
- GitHub-koblingens `fetch_workflow_run_artifacts` for samme repo/run: HTTP 404. Dette fastslår ikke at artefakten mangler; tilgang og eksistens kan ikke skilles med dette svaret.
- Nettlesøkverktøyets åpning av [kjøringssiden](https://github.com/Digipomps/CellScaffold/actions/runs/34574674480): fetch-feil / cache miss.
- Ingen `trace.zip`, dokument-proof-artefakt eller fil navngitt med run-ID ble funnet under lokale `CellScaffold/test-results` eller denne leveransemappen.

**Kjetil må laste ned dokumentartefakten fra kjøringen og oppgi lokal ZIP-sti.** Workflowen bruker hele SHA-en i `document-proof-${{ github.sha }}` (`CellScaffold/.github/workflows/admin-scaffold-image.yml:379–386`), så navnet kan være `document-proof-649255bb777b3a5135bd9c50512d3074bd23935b`, ikke bare den korte formen. `browser-proof-...` inkluderer også samme testresultatmappe på **397–405**.

Les deretter, før eventuell kodefiks:

1. DOM-snapshot i **sesjon A** ved/under linje 23: alle `.document-status`-tekster, hvilken som tilhører editoren, editorens innhold/redigerbarhet, og om flaten er remountet. Testen filtrerer bort noder med andre statustekster, så selve assertion-utskriften behøver ikke vise den faktiske teksten. Assertionen krever også synlighet: en lagret-tekst i en skjult eller fjernet flate ville heller ikke passere. Tidligere synlig editor beviser ikke at samme DOM var synlig helt frem til linje 23.
2. Trace-konsoll og page errors: eventuelle kast i Delta/Quill/rendering og transportfeil. `say` skriver ikke til konsollen; DOM-snapshot er nødvendig i tillegg.
3. Action-request/-response for første tekstsekvens: kind, operationId, baseRevision, status, current.revision/sequence/events, request-start, responsheadere og fullført body. Ta med `actionDiagnostics` dersom kroppen finnes.
4. Tidsrekkefølge mellom Flow-/bootstrap-oppdateringer, HTTP-svar og mulige presence-kall. Se spesielt etter svar som aldri fullføres, manglende current, et allerede bekreftet første element med mer kø, eller metadata som skriver over lagret-status.

Siste statustekst vil skille mellom flere forklaringer. Hvis den er «Lagrer endringer …», kreves nettverkstidslinjen fortsatt for å skille langsom normal kø fra en uavklart operasjon. Den teksten alene beviser ikke terskelhypotesen.

## 6. Foreslått diff A: behold HTTP-timeout til body er lest

**Selvstendig bekreftet transportfeil; ikke bekreftet CI-fiks. Ikke anvendt.** Endringen gjelder `CellScaffold/Public/js/porthole-webo.js:10057` og påvirker alle brukere av denne helperen. Den eksisterende request-fristen dekker også asynkron body-lesing, og AbortError fra body går gjennom samme catch. Den øker ingen frist og innfører ingen parallell retry.

```diff
--- a/Public/js/porthole-webo.js
+++ b/Public/js/porthole-webo.js
@@ -10054,7 +10054,7 @@
       throw new Error(message);
     }
 
-    return response.json();
+    return await response.json();
   } catch (error) {
     if (error instanceof DOMException && error.name === "AbortError") {
       throw new Error(`Request timed out after ${timeoutMs}ms.`);
```

Dette setter ikke en grense på synkron JSON-parsing som blokkerer eventløkken, og garanterer ikke lagret-status innen 15 s. En utløpt transportfrist treffer fortsatt adapterens eksisterende 2500-ms-retry med samme operationId. Det er en avgrenset reparasjon av timeoutens levetid.

## 7. Foreslått diff B: separat sikring mot konflikt uten fremdrift

**Dette er det sekundære funnet, ikke årsaken til den røde kjøringen. Ikke anvendt.** `CellScaffold/Public/js/haven-rich-document.js:109,120–121` sletter den sendte konvolutten og retryer med nulltimer uten backoff, teller eller fremdriftssjekk. Etter initialisering flyttes confirmed.revision bare via events på **71–76**. Første initialisering uten lagret utkast leser faktisk `snapshot.revision` på **66**; «leser aldri snapshot.revision» gjelder derfor ikke denne første grenen.

Hvis snapshot har nyere revision, men tom/avkortet deltahale, eller et gjenopprettet utkast ligger foran serveren, kan samme baseRevision/ops/operationId sendes igjen uten endring. Dersom en faktisk nyere event hopper over en revisjon, stopper dagens **73** allerede; den stopper ikke en helt manglende hale. Normalserveren projiserer revisjon og komplett deltahistorikk sammen (`CellScaffold/Sources/App/Cells/RichDocument/RichDocumentCell.swift:139–151`) og stopper ved kapasitet fremfor å trunkere (`CellScaffold/Sources/App/Cells/RichDocument/RichDocumentModel.swift:91–94,110,114`). De manglende-historikk-testene er negative fixturer, ikke dokumentasjon på at CI-serveren produserte dem.

R-F45 sier maks ett retry per bekreftet årsak og stopp/handoff ved samme fingeravtrykk, jf. `HAVEN-Deploy/AGENTS.md:29` og `HAVEN-Deploy/docs/Regler.md:79`. Her velges stopp straks uendret konflikt er bekreftet; venting alene reparerer ikke manglende revisjonsgrunnlag. Lokal kø/utkast beholdes, editoren deaktiveres, og eksport av lokalt innhold er fortsatt tilgjengelig i eksisterende kode (`haven-rich-document.js:202–210`). Fysisk eksport er ikke prøvd i disse Node-testene.

Vakten sammenligner også med **den avviste konvoluttens** baseRevision: Flow kan allerede ha flyttet confirmed før svaret kommer. Bare å sammenligne før/etter accept ville stoppe en legitim rebase. Den sjekker dessuten at samme køelement fortsatt finnes, slik at et allerede kvittert element ikke stopper neste endring.

```diff
--- a/Public/js/haven-rich-document.js
+++ b/Public/js/haven-rich-document.js
@@ -106,7 +106,19 @@
       item.sent = payload; saveDraft();
       try {
         const result = unwrap(await options.send(payload));
-        if (result.status === "conflict") { delete item.sent; accept(result.current); }
+        if (result.status === "conflict") {
+          const revisionBefore = confirmed.revision;
+          delete item.sent;
+          accept(result.current);
+          // Flow may have advanced confirmed before this reply arrived.
+          const advanced = confirmed.revision > revisionBefore || revisionBefore > payload.baseRevision;
+          if (!stopped && queue.includes(item) && !advanced) {
+            stopped = true;
+            quill.enable(false);
+            saveDraft();
+            say("Lagringen er stoppet fordi dokumentversjonen ikke kunne avstemmes. Last ned utkastet før du åpner dokumentet på nytt.");
+          }
+        }
         else if (["accepted", "duplicate"].includes(result.status)) accept(result.current);
         else { stopped = true; say(`Endringen ble avvist (${result.status}). Utkastet er beholdt; last ned en kopi.`); }
       } catch (error) {
```

Forslaget setter ikke confirmed.revision blindt fra snapshot; det ville skjule uanvendte tekstoperasjoner. Det begrenser bare uendret konflikt. Catch-retry etter nettverk/`persistencePending`, metadata-heartbeat og accepted/duplicate uten køfremdrift er fortsatt egne, ubegrensede baner. Det er ikke en generell implementering av retry-budsjett for hele adapteren.

## 8. Regresjonstester og faktisk resultat

Kjørt med **Node v22.14.0**, originale kildefiler fra `649255bb`, og hver diff separat på en midlertidig kildekopi. Ingen Swift/server/browser bygges eller startes av testene.

| Testgruppe | Original | Foreslått variant |
| --- | --- | --- |
| HTTP-body-timeout, 4 tester | **1 feil, 3 bestått**, exit 1. Hengende body forblir pending etter fristen. | Diff A: **4 bestått**, exit 0. Body avbrytes; vanlig suksess, venting på headere og JSON-feil beholder forventet oppførsel. |
| Konflikt uten fremdrift, 7 tester | **3 feil, 4 bestått**, exit 1. Tre stoppkrav observerer 9 identiske sendinger etter åtte simulerte retry-timere. | Diff B: **7 bestått**, exit 0. Uendrede konflikter stopper etter én sending; normal rebase, Flow før svar, eldre svar og eksisterende history-gap-stopp passerer. |
| Busy/presence-karakterisering, 5 tester | **5 bestått**, exit 0. Bekrefter uavklart send + mer kø, begge catch-banene, presence uten klientlås, sen statusoverskriving og pending-retensjon/opprydding. | Ingen produktfiks testes i denne gruppen; testene beskriver eksisterende oppførsel. |
| Live-kjøring 34574674480 | Kjetils logg: feil på spec-linje 23. | **ukjent**. Ingen ny live-kjøring, og ingen påstand om grønn main. |

HTTP-testen evaluerer den eksakte `fetchJSON`-funksjonen fra kildefilen; den implementerer ikke helperen på nytt. Fetch/body og timere er testdobler. Adaptertestene evaluerer hele den faktiske `haven-rich-document.js`, med DOM/Quill/timer-dobler. Delta-dobbelen støtter bare identitetsdelta og enkel egen kvittering. Testene verifiserer kontrollflyt, konvolutter, utkast og timeouthåndtering; de måler **ikke** CI-latens, Quills virkelige tastaturhendelser, OT generelt, persistens eller full brukerflyt.

De komplette testfilene står i vedlegget. De er forslag til senere installering, ikke lagt inn i CellScaffold. Plasser filene sammen, f.eks. i en midlertidig mappe, og velg de undersøkte kildekopiene eksplisitt:

```sh
PORTHOLE_SOURCE=/absolutt/sti/porthole-before.js node --test /absolutt/sti/body-timeout.test.cjs
PORTHOLE_SOURCE=/absolutt/sti/porthole-after.js node --test /absolutt/sti/body-timeout.test.cjs
DOCUMENT_ADAPTER=/absolutt/sti/adapter.js node --test /absolutt/sti/retry-regression.cjs /absolutt/sti/control-flow.test.cjs
DOCUMENT_ADAPTER=/absolutt/sti/retry-after.js node --test /absolutt/sti/retry-regression.cjs
```

Arbeidskopier og testtranskripsjoner for denne analysen ligger i `/private/tmp/document-ci-analysis-uh72s74x/`. Denne rapporten inneholder diffene og fullstendige tester slik at analysen ikke avhenger av at tempmappen overlever.

Kilde-SHA256: adapter `f9a92c462b346bad48fabc5b19991d68a7a644f2fa1583a07d295f8d3f056939`; Porthole `a020c8b38f18a45c8a7a2019907f450f947b431ed6264ca7814b5d39963f868f`.

## Vedlegg: harness.cjs

```javascript
// Run from CellScaffold: node --test scripts/rich-document-retry.test.cjs
// Optional fixture override: DOCUMENT_ADAPTER=/absolute/path/adapter.js
const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const { randomUUID } = require('node:crypto');
const adapterPath = process.env.DOCUMENT_ADAPTER || 'Public/js/haven-rich-document.js';
const source = fs.readFileSync(adapterPath, 'utf8');
const clone = value => JSON.parse(JSON.stringify(value));

// DOM/Quill doubles: test adapter control flow, not rendering or OT mathematics.
class Element {
  constructor() { this.children = []; this.textContent = ''; this.classList = { add() {} }; }
  appendChild(child) { this.children.push(child); return child; }
  append(...children) { this.children.push(...children); }
  prepend(...children) { this.children.unshift(...children); }
  replaceChildren(...children) { this.children = children; }
  setAttribute() {}
  addEventListener() {}
  get childElementCount() { return this.children.length; }
}
class Delta {
  constructor(ops = []) { this.ops = ops; }
  compose(other) {
    // Remote peers use identity deltas; the own acknowledgement inserts a prefix.
    if (!other.ops.length) return new Delta(this.ops);
    assert.ok([...other.ops, ...this.ops].every(op => typeof op.insert === 'string'));
    return new Delta([{ insert: [...other.ops, ...this.ops].map(op => op.insert).join('') }]);
  }
  transform(other) { assert.equal(this.ops.length === 0 || other.ops.length === 0, true); return other; }
}
async function flush() { for (let i = 0; i < 12; i++) await Promise.resolve(); }
function snapshot(revision, events = []) {
  return { schema: 'haven.document.v1', documentId: 'retry-proof', revision,
    sequence: revision, ops: [{ insert: '\n' }], events, comments: [], presence: [] };
}
function event(revision, operationId = randomUUID()) {
  return { revision, sequence: revision, author: 'peer', command: {
    schema: 'haven.document.change.v1', operationId, clientId: randomUUID(),
    kind: 'delta', baseRevision: revision - 1, ops: [] } };
}
async function harness(initial, reply, savedDraft) {
  let quill;
  class Quill {
    static imports = { 'formats/visualization': true };
    static import(name) { assert.equal(name, 'delta'); return Delta; }
    constructor() { quill = this; this.root = new Element(); this.container = new Element(); this.handlers = {}; }
    on(name, callback) { (this.handlers[name] ||= []).push(callback); }
    setContents(delta) { this.contents = clone(delta.ops); }
    enable(value) { this.enabled = value; }
    getSelection() { return null; }
    updateContents(delta) { assert.equal(delta.ops.length, 0); }
    hasFocus() { return false; }
    type() {
      this.contents = [{ insert: 'lokalt utkast\n' }];
      for (const handler of this.handlers['text-change']) handler({ ops: [{ insert: 'lokalt utkast' }] }, null, 'user');
    }
  }
  const timers = new Map(), intervals = new Map(), storage = new Map(), calls = [];
  if (savedDraft) storage.set('haven.document.draft:retry-proof', JSON.stringify(savedDraft));
  let timerId = 0;
  const window = { Quill, addEventListener() {}, removeEventListener() {} };
  const context = vm.createContext({ window, crypto: { randomUUID },
    document: { head: new Element(), querySelector: () => true, createElement: () => new Element() },
    sessionStorage: { getItem: key => storage.get(key) ?? null, setItem: (key, value) => storage.set(key, value), removeItem: key => storage.delete(key) },
    setTimeout: (fn, delay) => { const id = ++timerId; timers.set(id, { fn, delay }); return id; },
    clearTimeout: id => timers.delete(id),
    setInterval: (fn, delay) => { const id = ++timerId; intervals.set(id, { fn, delay }); return id; },
    clearInterval: id => intervals.delete(id) });
  vm.runInContext(source, context, { filename: adapterPath });
  const root = new Element();
  const controller = window.HavenRichDocument.mount(root, { send: async payload => {
    calls.push(clone(payload)); return clone(await reply(payload, calls.length));
  } });
  controller.update(initial);
  await flush();
  if (!savedDraft) assert.equal(quill.enabled, true);
  return { controller, quill, calls, storage, timers, intervals,
    get status() { return root.children[0].textContent; },
    async tick() {
      const entry = timers.entries().next().value;
      if (!entry) return false;
      const [id, timer] = entry; timers.delete(id); timer.fn(); await flush(); return true;
    } };
}


module.exports = { harness, snapshot, event, clone, flush };
```

## Vedlegg: retry-regression.cjs

```javascript
const { test } = require('node:test');
const assert = require('node:assert/strict');
const { randomUUID } = require('node:crypto');
const { harness, snapshot, event, clone, flush } = require('./harness.cjs');

for (const [name, initial, current] of [
  ['empty events with newer server revision', snapshot(0), snapshot(1)],
  ['all events already confirmed but server revision newer', snapshot(1, [event(1)]), snapshot(2, [event(1)])],
]) {
  test(name + ': stop identical conflict and preserve draft', async t => {
    const h = await harness(initial, () => ({ status: 'conflict', current }));
    t.after(() => h.controller.destroy());
    h.quill.type(); await flush();
    for (let i = 0; i < 8; i++) await h.tick();
    t.diagnostic(JSON.stringify({ sends: h.calls.length, distinctPayloads: new Set(h.calls.map(JSON.stringify)).size, status: h.status }));
    assert.equal(h.calls.length, 1, 'no unchanged automatic retry after confirmed conflict');
    assert.match(h.status, /Last ned utkastet/);
    assert.equal(h.quill.enabled, false);
    assert.match(JSON.stringify(h.quill.contents), /lokalt utkast/);
    const draft = JSON.parse(h.storage.get('haven.document.draft:retry-proof'));
    assert.equal(draft.confirmed.revision, initial.revision);
    assert.equal(draft.queue[0].operationId, h.calls[0].operationId);
    assert.deepEqual(draft.queue[0].ops, h.calls[0].ops);
    // A repeated runtime update must not restart the stopped pump.
    h.controller.update(current); await flush(); await h.tick();
    assert.equal(h.calls.length, 1);
  });
}

for (const flowRevision of [0, 1, 2]) {
  test('valid conflict rebases once, Flow revision before reply=' + flowRevision, async t => {
    const current = snapshot(1, [event(1)]);
    const advanced = flowRevision === 2 ? snapshot(2, [...current.events, event(2)]) : current;
    let resolveConflict;
    const h = await harness(snapshot(0), (payload, count) => count === 1
      ? new Promise(resolve => { resolveConflict = resolve; })
      : { status: 'accepted', current: snapshot(advanced.revision + 1, [...advanced.events, { ...event(advanced.revision + 1), command: clone(payload) }]) });
    t.after(() => h.controller.destroy());
    h.quill.type(); await flush();
    if (flowRevision) h.controller.update(advanced);
    resolveConflict({ status: 'conflict', current }); await flush(); await h.tick();
    assert.deepEqual(h.calls.map(c => c.baseRevision), [0, advanced.revision]);
    assert.equal(h.calls[0].operationId, h.calls[1].operationId);
    assert.match(h.status, /Alle endringer er lagret/);
    assert.equal(h.quill.enabled, true);
    assert.equal(h.storage.has('haven.document.draft:retry-proof'), false);
    assert.equal(h.timers.size, 0);
  });
}

test('existing history-gap stop remains bounded', async t => {
  const h = await harness(snapshot(0), () => ({ status: 'conflict', current: snapshot(2, [event(2)]) }));
  t.after(() => h.controller.destroy());
  h.quill.type(); await flush();
  for (let i = 0; i < 8; i++) await h.tick();
  assert.equal(h.calls.length, 1);
  assert.match(h.status, /Endringshistorikken er ufullstendig/);
});


test('restored browser draft ahead of complete server history stops', async t => {
  const current = snapshot(1, [event(1)]);
  const saved = { clientId: randomUUID(),
    confirmed: { documentId: 'retry-proof', revision: 2, ops: [{ insert: 'nyere kopi\n' }] },
    queue: [{ operationId: randomUUID(), ops: [{ insert: 'lokalt utkast' }] }] };
  const h = await harness(current, () => ({ status: 'conflict', current }), saved);
  t.after(() => h.controller.destroy());
  for (let i = 0; i < 8; i++) await h.tick();
  t.diagnostic(JSON.stringify({ sends: h.calls.length, distinctPayloads: new Set(h.calls.map(JSON.stringify)).size }));
  assert.equal(h.calls.length, 1);
  assert.equal(h.calls[0].baseRevision, 2);
  assert.match(h.status, /Last ned utkastet/);
  assert.equal(h.quill.enabled, false);
  assert.match(JSON.stringify(h.quill.contents), /lokalt utkast/);
  assert.equal(JSON.parse(h.storage.get('haven.document.draft:retry-proof')).queue[0].operationId, saved.queue[0].operationId);
});
```

## Vedlegg: control-flow.test.cjs

```javascript
const { test } = require('node:test');
const assert = require('node:assert/strict');
const { harness, snapshot, event, clone, flush } = require('./harness.cjs');
function acknowledge(payload, revision, events = []) {
  return { status: 'accepted', current: snapshot(revision,
    [...events, { ...event(revision), command: clone(payload) }]) };
}
test('Flow confirms first edit while an unresolved send still blocks the second', async t => {
  let resolveFirst, first;
  const h = await harness(snapshot(0), (payload, count) => {
    if (count === 1) { first = acknowledge(payload, 1); return new Promise(resolve => { resolveFirst = resolve; }); }
    return acknowledge(payload, 2, first.current.events);
  });
  t.after(() => h.controller.destroy());
  h.quill.type(); h.quill.type(); await flush();
  h.controller.update(first.current); await flush();
  assert.equal(h.calls.length, 1);
  assert.match(h.status, /Lagrer endringer/);
  assert.equal(h.timers.size, 0, 'adapter has no in-flight deadline');
  resolveFirst(first); await flush(); await h.tick();
  assert.equal(h.calls.length, 2);
  assert.match(h.status, /Alle endringer er lagret/);
});
test('thrown send retains exact envelope and releases busy on the 2500 ms timer', async t => {
  const h = await harness(snapshot(0), (payload, count) => {
    if (count === 1) throw new Error('synthetic offline');
    return acknowledge(payload, 1);
  });
  t.after(() => h.controller.destroy());
  h.quill.type(); await flush();
  assert.equal(h.calls.length, 1);
  assert.equal([...h.timers.values()][0].delay, 2500);
  await h.tick();
  assert.deepEqual(h.calls[0], h.calls[1]);
  assert.match(h.status, /Alle endringer er lagret/);
});
test('send rejection after Flow acknowledgment releases busy immediately', async t => {
  let rejectFirst;
  const h = await harness(snapshot(0), () => new Promise((resolve, reject) => { rejectFirst = reject; }));
  t.after(() => h.controller.destroy());
  h.quill.type(); await flush();
  h.controller.update(acknowledge(h.calls[0], 1).current);
  rejectFirst(new Error('late network failure')); await flush();
  assert.equal(h.timers.size, 0);
  assert.match(h.status, /Alle endringer er lagret/);
  h.quill.type(); await flush();
  assert.equal(h.calls.length, 2);
});
test('pending presence does not lock text, but a late conflict overwrites saved status', async t => {
  let resolvePresence, saved;
  const h = await harness(snapshot(0), payload => {
    if (payload.kind === 'presence') return new Promise(resolve => { resolvePresence = resolve; });
    saved = acknowledge(payload, 1); return saved;
  });
  t.after(() => h.controller.destroy());
  h.quill.hasFocus = () => true;
  const heartbeat = [...h.intervals.values()][0];
  assert.equal(heartbeat.delay, 30000);
  heartbeat.fn(); await flush();
  h.quill.type(); await flush();
  assert.deepEqual(h.calls.map(p => p.kind), ['presence', 'delta']);
  assert.match(h.status, /Alle endringer er lagret/);
  resolvePresence({ status: 'conflict', current: saved.current }); await flush();
  assert.match(h.status, /Dokumentet ble endret/);
  assert.equal(h.storage.size, 0);
});
test('failed metadata envelope survives text saves, then a conflict clears it', async t => {
  let presenceCount = 0, saved;
  const h = await harness(snapshot(0), payload => {
    if (payload.kind === 'delta') { saved = acknowledge(payload, 1); return saved; }
    presenceCount++;
    if (presenceCount === 1) throw new Error('synthetic metadata failure');
    return { status: presenceCount === 2 ? 'conflict' : 'accepted', current: saved.current };
  });
  t.after(() => h.controller.destroy());
  h.quill.hasFocus = () => true;
  const heartbeat = [...h.intervals.values()][0].fn;
  heartbeat(); await flush();
  h.quill.type(); await flush();
  assert.match(h.status, /Alle endringer er lagret/);
  heartbeat(); await flush(); heartbeat(); await flush();
  const presence = h.calls.filter(p => p.kind === 'presence');
  assert.deepEqual(presence[0], presence[1]);
  assert.equal(presence[1].baseRevision, 0);
  assert.equal(presence[2].baseRevision, 1);
  assert.notEqual(presence[1].operationId, presence[2].operationId);
});
```

## Vedlegg: body-timeout.test.cjs

```javascript
const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const source = fs.readFileSync(process.env.PORTHOLE_SOURCE || 'Public/js/porthole-webo.js', 'utf8');
const begin = source.indexOf('async function fetchJSON(url, options = {}) {');
const end = source.indexOf('\nfunction postJSON(', begin);
assert.ok(begin >= 0 && end > begin, 'use exact fetchJSON source');
const flush = async () => { for (let i = 0; i < 20; i++) await Promise.resolve(); };
function network({ pendingHeaders = false } = {}) {
  const timers = new Map();
  let next = 0, signal, resolveBody, rejectBody;
  const body = new Promise((resolve, reject) => { resolveBody = resolve; rejectBody = reject; });
  const response = { ok: true, json: () => body };
  const context = vm.createContext({ AbortController, DOMException, window: {
    setTimeout(fn, ms) { const id = ++next; timers.set(id, { fn, ms }); return id; },
    clearTimeout(id) { timers.delete(id); }
  }, fetch: async (_url, options) => {
    signal = options.signal;
    signal.addEventListener('abort', () => rejectBody(new DOMException('Aborted', 'AbortError')));
    if (!pendingHeaders) return response;
    return await new Promise((resolve, reject) => {
      signal.addEventListener('abort', () => reject(new DOMException('Aborted', 'AbortError')));
      body.catch(() => {});
    });
  } });
  vm.runInContext(source.slice(begin, end), context);
  return { fetchJSON: context.fetchJSON, timers, resolveBody, rejectBody,
    get signal() { return signal; },
    deadline() { for (const [id, timer] of [...timers]) { timers.delete(id); timer.fn(); } }
  };
}
test('success headers with unfinished JSON body remain covered by request timeout', async () => {
  const n = network();
  let outcome = 'pending';
  n.fetchJSON('/browserhead/porthole/action', { timeoutMs: 30000 }).then(
    () => { outcome = 'resolved'; }, error => { outcome = error.message; }
  );
  await flush();
  n.deadline(); await flush();
  assert.equal(outcome, 'Request timed out after 30000ms.');
  assert.equal(n.signal.aborted, true);
  assert.equal(n.timers.size, 0);
});
test('completed JSON resolves and clears timeout', async () => {
  const n = network();
  const pending = n.fetchJSON('/action', { timeoutMs: 30000 });
  n.resolveBody({ result: { status: 'accepted' } });
  assert.deepEqual(await pending, { result: { status: 'accepted' } });
  assert.equal(n.timers.size, 0);
  assert.equal(n.signal.aborted, false);
});
test('waiting for headers is already bounded', async () => {
  const n = network({ pendingHeaders: true });
  const pending = n.fetchJSON('/action', { timeoutMs: 30000 });
  n.deadline();
  await assert.rejects(pending, /Request timed out after 30000ms/);
});
test('malformed JSON remains a parse error and clears timeout', async () => {
  const n = network();
  const pending = n.fetchJSON('/action', { timeoutMs: 30000 });
  await flush(); n.rejectBody(new SyntaxError('synthetic bad JSON'));
  await assert.rejects(pending, /synthetic bad JSON/);
  assert.equal(n.timers.size, 0);
});
```
