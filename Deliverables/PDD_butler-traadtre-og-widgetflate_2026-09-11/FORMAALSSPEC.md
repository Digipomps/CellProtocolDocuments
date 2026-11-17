# FORMÅLSSPEC — Butler Chat: trådtre med skop, og widgetflate

Status: **venter på G1**. Ingen planlegging, kode eller skjelettendring før Kjetil sier ordet.

## §0 Intensjon (Kjetils ord, uendret)

> «Dette er det nye designet - slikt ser det ikke ut på web»
> (vedlagt `butlerchatmockup.html` + fem skjermbilder, 2026-09-11)
>
> «Dette er begge ting som er viktige. Et forslag er å starte to Codex (med ChatGPT 6
> Astra) tråder så de parallelt tar unna begge oppgaver. Dette må også paritets
> avstemmes med HAVEN app. Både mønsteret med å dra elementer ut fra et område i en
> flate som widgeter og vising av referenser til data i en trestruktur som trådtreet
> er, er generelle mønstre som kan gjenbrukes i mange sammenhenger. Dette må også
> dokumenteres.»

> «Butler chat er den administrerende chatten som skal forstå brukerens formål og hvilke
> verktøy som best oppfyller brukerens formål. Underhjelperne som kan være chat-hjelpere
> eller faktiske chatter vil utgjøre et tre som har Butler som rot. Meldingene og eventer
> blir sendt til den som ligger over og eventuelt routet videre. Selve chat-loggen skal
> fremstå som en chat — bestemt av hvilket scope brukeren har valgt ved å trykke på noder
> i treet. Slik kan vi ha en fleksibel fallback og få forslag til nye hjelpere som vil
> dukke opp som nye noder i treet.» (2026-09-12)

### Revisjon av påstander og forutsetninger

| Påstand / forutsetning | Status | Kilde |
|---|---|---|
| Designet finnes ikke på web | **retrieved** | `git grep -i` på «Flaten rundt», «Undertre», «Dokk til venstre», «grener i skop» i `Sources/ Public/ Resources/` på `origin/main`: 0 treff |
| Designet finnes ikke i noen gren heller | **retrieved** | samme søk over 250 remote-grener: 0 treff |
| Chatten har ingen trådmodell i dag | **retrieved** | `conversationId\|threadId\|conversations` i `PersonalCopilotCloudStore.swift`: 0 treff. Modellen er én liste, `promptMessages` |
| Rendereren kan drag-and-drop i dag | **retrieved** | `Public/js/skeleton-runtime.js`: 74 treff på `dragstart\|dragover\|drop` |
| Det finnes et primitiv for flate-elementer | **retrieved** | `pinnedComponentSurfaces` / `minimizedComponentSurfaces` + `restoreComponentSurface` i `PersonalCopilotConfigurationFactory.swift:1624–1671`; styleRole `chat-workbench-layout` finnes |
| #230 leverte startkort/hjelpelinje/svarkvalitet, ikke denne flaten | **retrieved** | `git diff --name-only 2b18bc07~1 ec627836`; `PersonalCopilotConfigurationFactory.swift:3878` |
| HAVEN app er paritetsflaten | **retrieved** | `handoff/PARITET_APP.md`: appen (Binding, iOS/macOS) rendrer chat generisk fra skjelett, men har **sin egen lokale chatfabrikk** — en endring i webfabrikken oppdaterer ikke appen. App-rendereren mangler generisk dra-og-slipp (bare filslipp påvist). Trådtre med skop mangler som ferdig mønster begge steder |
| Skjelettformatet kan uttrykke et tre med skop | **retrieved — delvis** | `handoff/KAPASITET_SKJELETT.md`: nestet komposisjon finnes (VStack/List/Reference), men ingen `parentKeypath`/`childrenKeypath`, ingen selvrekursiv radmal, ingen ekspanderbar rad, ingen «descendants»-operator. Skop finnes bare som synlighet (`SkeletonCondition`), ikke som undertreoperasjon. Anslag M |
| Skjelettformatet kan uttrykke dra-ut-til-flate | **retrieved — finnes deklarativt** | `SkeletonModifiers` har `draggableRole`, `dragPayloadKeypath`, `dragPreviewRole`, `dropTargetRole` (web). Det som mangler er kontrakten som identifiserer et strømelements *kilde* og oppretter en selvstendig, levende widgetinstans — anslag L. `pinnedComponentSurfaces` er lagret UI-tilstand uten levende innhold; `restoreComponentSurface` laster ikke `targetCellEndpoint` og nullstiller ikke `pinned` |

Alle påstander er nå `retrieved`. Det som var `unavailable` er besvart av de to leserapportene 2026-09-11, og det de avdekket er tatt inn i §2 og §3.

## §1 Formålstre

**Rot — `purpose://candidate.butler.surface-as-workbench`**
Butler Chat skal være en arbeidsflate: samtalen er inngangen, men det brukeren finner fram
skal kunne bli stående ved siden av, og samtaler skal kunne deles i spor uten å miste sammenhengen.
*Outcome:* Kjetil kan følge flere parallelle spor og beholde det han har hentet fram, uten å scrolle tilbake.
*Verifier:* `test.gui.parity` mot godkjent bilde + handlingene i §3 finnes i `reachableActionKeypaths`.

### A. Hjelpertre med ruting og skop — `purpose://candidate.pattern.reference-tree`

Det generelle mønsteret: *vise referanser til data i en trestruktur, med et skop som avgjør
hvor mye av undertreet som gjelder.* I Butler Chat er treet **hjelperhierarkiet**: Butler er
rot, underhjelpere (chat-hjelpere eller faktiske chatter) er noder, og meldinger og eventer
sendes til noden over og rutes eventuelt videre. Chat-loggen er én chat, bestemt av skopet
brukeren har valgt ved å trykke på noder.

Seed i dagens kode (`PersonalCopilotCloudStore.swift:969–1205`): `activeHelper`,
`helperRows` og `visibleKinds` finnes allerede, men flatt — ingen forelder, ingen ruting.

- **A1 `…reference-tree.model`** — En node er en hjelper med forelder; Butler er rot. En node peker på det den kan (verktøy, celle, chat), ikke eier historikken alene.
  *Signals:* nye hjelpere kan legges til som noder uten å endre rot; to noder kan peke på samme verktøy.
  *Verifier:* kontraktstest på node/forelder/referanse, `TESTRESULT.md#tree-model`.
- **A2 `…reference-tree.scope`** — Å trykke på en node setter skop: «undertre» viser loggen for noden og alt under, «bare denne» viser bare nodens egne meldinger. Loggen fremstår alltid som én chat.
  *Signals:* skopbytte endrer meldingsmengde og teller; grenopphav er synlig per melding.
  *Verifier:* `test.scope.switch`, `TESTRESULT.md#scope`.
- **A3 `…reference-tree.routing`** — En melding sendt i et skop går til nærmeste hjelper som kan svare; kan den ikke, går den til noden over, helt til Butler. Butler er alltid fallback.
  *Signals:* ingen melding blir ubesvart fordi en hjelper mangler; ruten er sporbar per melding.
  *Verifier:* `test.routing.fallback` med en hjelper som avslår, `TESTRESULT.md#routing`.
- **A4 `…reference-tree.suggest-helper`** — Når Butler ser at brukerens formål ikke dekkes av noen node, foreslår den en ny hjelper, som dukker opp som ny node i treet når brukeren sier ja.
  *Signals:* forslaget kommer fra formålsmatching, ikke fra en fast liste; avslått forslag gjentas ikke uendret.
  *Verifier:* `test.helper.suggestion` mot simulerte brukere med formål utenfor dagens hjelpere, `TESTRESULT.md#suggest`.
  *Merk:* A4 og B2c er de to første produktbrukene av formålsmatchingen; målingen i `PDD_formaalsregister-som-graf_2026-09-11` gjelder begge.
- **A5 `butler.helper-tree-model`** — Cellen får et hjelpertre med forelder/barn og ruting. **Ny datamodell, ikke skjelettendring.** Dagens flate `helperRows` migreres til barn av Butler uten tap.
  *Signals:* eksisterende samtaler og hjelpere overlever migrering; `promptMessages` får nodetilhørighet.
  *Verifier:* migreringstest på ekte staging-data, `TESTRESULT.md#migration`.

### B. Dra element ut av en flate og feste det — `purpose://candidate.pattern.detachable-surface-element`

Det generelle mønsteret: *et element vist i en strøm kan dras ut, festes i en flate ved siden av,
og fortsette å være levende mot samme kilde.* Widgetflaten er første bruk.

- **B1 `…detachable.grip-and-drop`** — Et kort har et grep, og en flate tar imot.
  *Signals:* dra viser plassholder og spøkelse; slipp fester kortet; avbrutt dra endrer ingenting.
  *Verifier:* `test.dnd.attach`, `TESTRESULT.md#dnd`.
- **B2 `…detachable.live-binding`** — Et festet element er ikke et bilde: det oppdateres når kilden endres.
  *Signals:* endring i cellen slår gjennom i widgeten uten ny henting fra brukeren; «Fra: … oppdatert 09:26» stemmer.
  *Verifier:* `test.widget.live`, `TESTRESULT.md#live`.
- **B2b `…detachable.owned-and-persisted`** — Festede widgets lagres i Portholens CellConfiguration. De er brukerens, og persisteres i cellen — ikke i nettleseren, ikke per økt. (Kjetil, 2026-09-12.)
  *Signals:* lukk nettleseren, åpne igjen: widgetene står der; en annen enhet med samme identitet ser det samme der det er valgt.
  *Verifier:* `test.widget.persisted`, `TESTRESULT.md#persist`.
- **B2c `…detachable.propagation-scope`** — Når brukeren fester eller endrer en widget, kan brukeren spørres om endringen skal gjelde *alle* brukerens Portholes, *bare denne*, eller *et utvalg*. Spørsmålet skal komme med et **godt forslag utledet av hva brukeren prøver å oppnå** — ikke et nøytralt valg. (Kjetil, 2026-09-12.)
  *Signals:* forslaget treffer i de fleste tilfeller uten at brukeren må endre det; valget er alltid synlig og reverserbart.
  *Verifier:* `test.widget.scope-suggestion` mot et sett simulerte brukere med ulike formål (se `lesson`-krav om simulerte roller), `TESTRESULT.md#scope-suggestion`.
  *Merk:* dette er første produktbruk av formålsmatchingen som måles i `PDD_formaalsregister-som-graf_2026-09-11` — forslaget skal komme fra matching på brukerens formål, og målingen der gjelder her.
- **B3 `…detachable.full-surface`** — Et festet element kan ta hele flaten og vise flere kolonner enn i kompakt form.
  *Signals:* full flate viser Innleder-kolonnen som ikke fins i kompakt; retur gir samme tilstand.
  *Verifier:* `test.gui.parity` mot bilde `full`.
- **B4 `…detachable.reachability`** — Alt widgeten kan gjøre, kan også bes om i chatten.
  *Signals:* hver handling i widgeten finnes som keypath nåbar fra samtalen.
  *Verifier:* `test.skeleton.purpose-actions-reachable`, `ACCEPT.md#ways-in`.

### C. Paritet og gjenbruk — `purpose://candidate.pattern.parity-and-reuse`

- **C1 `…parity.haven-app`** — Begge mønstrene oppfører seg likt i HAVEN app og på web, eller avviket er navngitt og begrunnet.
  *Signals:* samme handlinger nåbare begge steder; ulik layout er tillatt, ulik oppførsel er det ikke.
  *Verifier:* `test.gui.parity` per flate i begge klienter, `ACCEPT.md#parity`.
  Merk `lesson.parity-was-correctness-not-decoration`: paritet er korrekthet, ikke pynt.
- **C2 `…reuse.documented-pattern`** — Hvert mønster er dokumentert slik at en tredje flate kan ta det i bruk uten å lese kildekoden.
  *Signals:* dokumentet navngir kontrakten, grensene, og minst én bruk som ikke er Butler Chat.
  *Verifier:* `test.docs-updated` + en fremmed leser kan peke ut hva som må implementeres.

## §2 Avgrensning og avhengigheter

Dette er **ikke**: ny svarkvalitet i Butler (det var #230, allerede i main), ikke ny celle for
Arendalsuka, ikke endring av deploy-kjeden, og ikke en beslutning om de 93 pakkene utenfor main.

| Avhengighet | Verifier | Status |
|---|---|---|
| Skjelettformatet kan uttrykke et tre med skop, eller vi vet hva som mangler | `handoff/KAPASITET_SKJELETT.md` | **lukket** — mangler foreldre/barn-kontrakt og undertreoperasjon; må bygges i cellen |
| Skjelettformatet kan uttrykke dra-ut/feste, eller vi vet hva som mangler | samme | **lukket** — dra/slipp finnes deklarativt; kildekontrakt og levende widgetinstans mangler |
| HAVEN app sin chatflate er lest og paritetsgrensen er definert | `handoff/PARITET_APP.md` | **lukket** — grense foreslått i §6 spm. 3 |
| **Én chatfabrikk, ikke to.** Web og Binding har hver sin fabrikk for Butler Chat; alt vi bygger må ellers gjøres to ganger, og de vil drifte | inspeksjon: samme skjelett-JSON gir samme flate begge steder | **åpen — må avgjøres før G2** |
| `restoreComponentSurface` beholder `pinned` mens `activePanelSurfaces` utelukker festede poster | reprodusert i test, eller avkreftet med sti:linje | **åpen — mistenkt feil i dagens kode, må lukkes før B1** |
| App-rendereren har generisk dra-og-slipp | `Binding`-test som drar et vilkårlig element | **åpen — mangler i dag; bare filslipp påvist** |
| Staging er grønn og aksepttestene på HD-0040 er kjørt | `hd task show HD-0040` | **åpen** |

## §3 Forventningskontrakt — det du kommer til å se

| # | Leveranse | Type | Hvor | Referanse |
|---|---|---|---|---|
| 1 | Kapasitetsrapport skjelett/renderer | fil | `handoff/KAPASITET_SKJELETT.md` | WP-A2 |
| 2 | Paritetsrapport HAVEN app | fil | `handoff/PARITET_APP.md` | WP-A1 |
| 3 | Referansebilder, web: tom / fylt / dra / full flate / feil | bilder | `images/web-*-v1.png` | mockupens fire tilstander + feil (rutefallback, A3) |
| 4 | Referansebilder, app-bredde: normal / dra / tom | bilder | `images/app-*-v1.png` | mockupens to mobiltilstander + tom |
| 5 | Mønsterdokument: referansetre med skop | fil | `Book/` + `patterns/reference-tree.md` | C2 |
| 6 | Mønsterdokument: løsrivbart flate-element | fil | `patterns/detachable-surface-element.md` | C2 |
| 7 | Trådtre med skop, kjørende på staging | flate | staging | A1–A4 |
| 8 | Widgetflate med dra-ut, kjørende på staging | flate | staging | B1–B4 |
| 9 | Elementkart per del av mockupen (tre / chat / flate): mockup-element → dagens element/modifikator eller gap (nytt element, ny modifikator, renderer-semantikk), web og app hver for seg | fil | `handoff/SKJELETT_GAP_tre.md`, `_chat.md`, `_flate.md` | C1, C2 — Codex-jobber `skjelett-gap-*-20260912` |
| 10 | Kandidatskjelett per del med dagens format (det nærmeste som er mulig i dag), med starttabell for modifikatorer hentet fra mockupens CSS, handlingsliste og keypath-mangler | fil | `skjelett/<del>.candidate.skeleton.json`, `<del>.modifikatorer.md`, `<del>.handlinger.md`, `<del>.keypaths.md` | C1 — grunnlag for iterasjonene |
| 11 | Preview-scenario per del for `npm run skeleton:iterate -- --mode preview` mot staging, viewports 2000×1250 og 780×1688 (samme som referansebildene), slik at rendret flate kan legges over mockupen | fil | `skjelett/<del>.preview.json` | C1 — iterasjonene «juster modifikatorer til det ser likt ut» kjøres først når 9 er godkjent og elementene finnes |

Etter G2 teller bare disse radene som fremdrift (`lesson.plan-instead-of-delivery`).

**Det mockupen viser som dagens skjelettformat ikke kan rendre** (kravet fra `pkg.std.gui-surface`, kilde `handoff/KAPASITET_SKJELETT.md`): et navigerbart tre med utbretting og tastaturstyring; skop som *operasjon* over etterkommere (ikke bare skjul/vis); en widget som fortsetter å følge kilden etter at den er festet; automatisk bytte av kolonner mellom kompakt og full flate; og på app-siden: generisk dra-og-slipp. Referansebildene i rad 3–4 er derfor **mockups**, ikke Porthole-preview, og `images/README.md` skal si det eksplisitt (`lesson.scaffold-without-porthole-host-has-no-preview`).

## §4 Festede pakker og lærdommer

`pkg.std.everything-works`, `pkg.std.gui-surface`.

- `lesson.text-ux-is-not-design` — bildet godkjennes før kode. Mockupen Kjetil sendte er utgangspunktet, men den må suppleres med tilstandene den ikke viser (tom flate, feil).
- `lesson.unresolvable-condition-is-invisible` og `lesson.findability-is-not-usability` — reachability-audit over hver flate; et element som aldri kan ses teller som ikke levert. Dette er nøyaktig feilen fra 11.09: startkortet fantes i DOM med `display:none` og null rader.
- `lesson.tested-a-different-path-than-production` — testene skal gå gjennom produksjonens egen kodevei.
- `lesson.paste-command-instead-of-queue` — Codex startes som jobb i `_losen-queue`, aldri som kommando Kjetil limer inn.
- `lesson.codex-workspace-write-cannot-build-cellscaffold` — analyse og kontrakter som køjobb; lange bygg som detached skript.
- `lesson.parity-was-correctness-not-decoration` — C1 måler oppførsel, ikke utseende.

## §5 Avledede tester

| Test | Type | Hvordan | Bevis |
|---|---|---|---|
| `test.tree-model` | command | kontraktstest på node/gren/referanse | `TESTRESULT.md#tree-model` |
| `test.scope.switch` | command | skopbytte endrer meldingsmengde og teller | `TESTRESULT.md#scope` |
| `test.migration` | command | eksisterende samtaler og flate hjelpere overlever migrering til hjelpertre | `TESTRESULT.md#migration` |
| `test.routing.fallback` | command | melding i et skop med hjelper som avslår, ender hos noden over og til slutt Butler; ruten er logget | `TESTRESULT.md#routing` |
| `test.helper.suggestion` | measurement | simulert bruker med formål utenfor dagens hjelpere får forslag om ny node | `TESTRESULT.md#suggest` |
| `test.dnd.attach` | command | dra→slipp fester; avbrutt dra endrer ingenting | `TESTRESULT.md#dnd` |
| `test.widget.live` | command | kildeendring slår gjennom i festet widget | `TESTRESULT.md#live` |
| `test.widget.persisted` | command | widget overlever ny innlasting og ny enhet med samme identitet | `TESTRESULT.md#persist` |
| `test.widget.scope-suggestion` | measurement | forslag «alle / denne / utvalg» treffer for simulerte brukere med ulike formål | `TESTRESULT.md#scope-suggestion` |
| `test.skeleton.no-unreachable-elements` | command | SkeletonReachabilityAudit per flate | `TESTRESULT.md#reachability` |
| `test.skeleton.purpose-actions-reachable` | inspection | handlingene i §3 finnes i `reachableActionKeypaths` | `ACCEPT.md#ways-in` |
| `test.gui.parity` | inspection | referansebilde mot faktisk, web og app, samme bredde | `ACCEPT.md#parity` |
| `test.gui.load-time` | measurement | ≤ 5 s, tre forsøk | `TESTRESULT.md#load-time` |
| `test.build` / `test.regression` | command | alle berørte mål + full testmengde | `TESTRESULT.md#build`, `#regression` |
| `test.docs-updated` | inspection | mønsterdokumentene finnes og er datert | `ACCEPT.md#docs` |

## §6 Åpne spørsmål (bare de som endrer treet)

1. ~~Er trådtreet én chat med grener, eller flere celler?~~ **Besvart 2026-09-12 — ingen av delene:** treet er hjelperhierarkiet med Butler som rot; noder er underhjelpere (chat-hjelpere eller faktiske chatter); meldinger rutes oppover; skop velges ved å trykke på noder; nye hjelpere foreslås og dukker opp som nye noder. Tatt inn som A1–A5.
2. ~~Skal et festet element overleve at nettleseren lukkes?~~ **Besvart 2026-09-12:** ja — widgets lagres i Portholens CellConfiguration, de er brukerens og persisteres i cellen. Brukeren kan spørres om endringen skal gjelde alle Portholes, bare denne eller et utvalg, med et forslag utledet av formålet. Tatt inn som B2b og B2c.
3. **Paritetsgrensen — rapportens påstand, til ja eller nei:** «De to mønstrene regnes som levert først når Butler Chat på web og i Binding på iOS/macOS, med samme data og tilgang, gir samme valg av node og skop, samme meldingsutvalg og grenopphav, og samme mulighet til å feste, åpne, minimere, gjenopprette og fjerne et levende kildebundet element med samme tilstand og feilutfall; layout og plattformbetjening kan variere, men alle operasjonene må være tilgjengelige og ha samme virkning.» Ja betyr at app-rendereren må få generisk dra-og-slipp og at fabrikken må deles — omtrent dobbelt arbeid. Nei betyr web først, app som egen oppgave etterpå.

## §7 Revisjoner

| Runde | Dato | Hva endret seg |
|---|---|---|
| 1 | 2026-09-11 | Første utkast etter at mockupen ble sammenlignet med koden |
| 4 | 2026-09-12 | §6 spm. 1 besvart av Kjetil: treet er hjelperhierarkiet med Butler som rot, ruting oppover, skop ved klikk, nye hjelpere som nye noder → A-grenen omskrevet (A1–A5), to nye tester |
| 3 | 2026-09-12 | §6 spm. 2 besvart av Kjetil: widgets persisteres i Portholens CellConfiguration; propageringsskop med formålsutledet forslag → B2b, B2c, to nye tester |
| 2 | 2026-09-12 | Tatt inn `KAPASITET_SKJELETT.md` og `PARITET_APP.md`: alle påstander `retrieved`; tre nye avhengigheter (én fabrikk, restore/pinned-spenning, app-DnD); §3 lister hva skjelettet ikke kan rendre; spm. 3 er rapportens påstand ordrett |
| 5 | 2026-09-12 | §3 rad 3–4 utvidet med tilstandene *feil* (web) og *tom* (app); åtte bilder rendret fra mockupen og lagt i `images/` med README som sier at de er mockups. Ingen endring i §1 |
| 6 | 2026-09-12 | Kjetils metode for skjelett-paritet tatt inn: §3 rad 9–11 (elementkart per del, kandidatskjelett med dagens format, preview-scenario). Mockupen delt i tre deler (`images/deler/`), én Codex-jobb per del. Iterasjonsfasen (modifikatorer justeres til likt) krever en tråd med nettverk mot staging — Codex-sandkassen har ikke det. Ingen endring i §1 |
