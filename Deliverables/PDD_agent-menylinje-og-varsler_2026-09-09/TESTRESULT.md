# TESTRESULT — agent menylinje og varsler

> ## Retraksjon, 2026-09-11
>
> **Påstanden «`main` bygger ikke» var feil.** Den ble meldt som et faktum om
> prosjektet. Det den egentlig handlet om, var én commit som bare fantes på
> Kjetils maskin.
>
> `ba14895 «Land the correspondence MCP as a CellProtocol client»` lå på den
> **lokale** `main`-grenen og var aldri pushet. Den avhang av CellBase-kode som
> heller aldri var pushet. `origin/main` lå fire commits lenger fram, pinnet
> CellProtocol til `e03923cb` — som **er** på CellProtocol sin main — og hadde
> grønn CI hele tiden.
>
> Verifisert 2026-09-11 med en ren klone **fra GitHub**, uten dev-link, uten
> lokale søsterutsjekk:
>
> ```
> origin/main 79b359f: EXIT_BUILD=0
> Test run with 179 tests in 37 suites failed after 4.113 s with 1 issue
>   decodedDefaultAgentCellsInstallBindingsOnceBeforeImmediateStateReads (ustabil)
> ```
>
> Den ekte main bygger. Alt under her ble målt mot den lokale, upushede
> commiten, og tallene er derfor **ikke** sammenlignbare med prosjektets main.
> Arbeidet er nå spilt av på nytt oppå `origin/main`; se `#ekte-main`.
>
> Feilen min var ikke bare tallet. Det var å svare på en rød baseline med
> `swift package edit` mot lokale utsjekk i stedet for å spørre hvorfor den var
> rød. Da bygde alt — på én maskin — og jeg meldte det som verifisert.

Alle kjøringer er på macOS i worktreet `HavenAgentD::.worktrees/menylinje-20260909`,
branch `pdd/agent-menylinje-og-varsler`, base `main` `ba1489554bdf8b27f10ef0fdc8fa727689fa0c98`.
Loggene ligger i `HavenAgentD::.build/menylinje-baseline/` og er ikke slettet.

## Baseline <a id="baseline"></a>

**Funn før en eneste linje ble skrevet: `main` bygger ikke.**

Første forsøk, mot de pinnede avhengighetene i `Package.swift`
(`cellprotocol 4107d27a`, `sprout 473d6998`): **79 kompileringsfeil**, alle i
`Sources/HavenCorrespondenceMCP/`. Logg: `baseline-pinned.build.log`.

```
error: cannot find type 'CorrespondenceStoredEnvelope' in scope        (6)
error: cannot find 'CorrespondenceAgreementTemplates' in scope         (10)
error: type 'CorrespondenceInboxResponse' does not conform to 'Codable' (12)
...
```

Årsak: repoet bygges i praksis i **utviklingsmodus**. `Scripts/dev-link.sh`
kobler `cellprotocol` og `sprout` til lokale søsterutsjekker med
`swift package edit`. Etter samme kobling i worktreet falt feilene til to:

```
CorrespondenceClient.swift:155: error: value of type 'AgentIdentityStore' has no member 'loadExisting'
CorrespondenceClient.swift:189: error: extra arguments at positions #2, #3 in call
```

Begge peker på `AgentIdentityStore`. `git diff` i det delte arbeidstreet viser
at `loadExisting()` og den tre-argumenters `loadOrCreate` finnes **bare som
ucommittet endring** — 22 linjer som aldri ble landet. HEAD-commiten på `main`
heter «Land the correspondence MCP as a CellProtocol client», og den landet
altså kode som avhenger av en endring som ikke ble med.

Konsekvens: en ren klone av `main` kan verken bygge eller kjøre testene, fordi
`HavenCorrespondenceMCPTests` avhenger av målet. Dette er ikke innført av denne
PDD-en, men det er nå dokumentert. Se `handoff/GIT_ADMIN_STATUS.md`.

Baselinen er derfor målt på **`main` + den ene ulandede filen**
(`Sources/HavenAgentRuntime/AgentIdentityStore.swift`), tatt inn som egen
forutsetnings-commit som skal droppes når det egentlige arbeidet landes.

### Målt baseline <a id="build"></a>

```
TAG=baseline2   EXIT_BUILD=0   Build complete! (107.18s)
Test run with 165 tests in 33 suites failed after 4.112 seconds with 1 issue.
  Test decodedDefaultAgentCellsInstallBindingsOnceBeforeImmediateStateReads()
    recorded an issue at AgentCellsTests.swift:198:6: Caught error: ownerProofUnavailable
```

### Flakhetskontroll av baselinen <a id="flaky"></a>

Første kjøring med mine endringer viste **to** røde i stedet for én, og den nye
var `hostedAgentIdentityProvesRemoteBridgeControl` — i en fil jeg hadde endret.
Det kunne ikke antas å være flaks. Et eget worktree på ren base
(`.worktrees/menylinje-base-20260909`, detached på `ba14895` + samme
forutsetningsfil) ble derfor kjørt **tre ganger uten noen av mine endringer**:

```
=== kjøring 1 === 165 tester, 2 issues
  decodedDefaultAgentCellsInstallBindingsOnceBeforeImmediateStateReads  ownerProofUnavailable
  hostedAgentIdentityProvesRemoteBridgeControl                          requesterAuthorityUnavailable
=== kjøring 2 === 165 tester, 1 issue
  decodedDefaultAgentCellsInstallBindingsOnceBeforeImmediateStateReads  ownerProofUnavailable
=== kjøring 3 === 165 tester, 2 issues
  decodedDefaultAgentCellsInstallBindingsOnceBeforeImmediateStateReads  ownerProofUnavailable
  hostedAgentIdentityProvesRemoteBridgeControl                          requesterAuthorityUnavailable
```

Konklusjon: `hostedAgentIdentityProvesRemoteBridgeControl` er **flaky på basen**
(2 av 3), og `decodedDefaultAgentCells…` er **konsekvent rød på basen** (3 av 3).
Ingen av dem er innført her. Logg: `base.summary.txt`, `base.run1–3.log`.

## Regresjon <a id="regression"></a>

```
TAG=wp6   EXIT_BUILD=0
Test run with 200 tests in 36 suites failed after 4.151 seconds with 2 issues.
  decodedDefaultAgentCellsInstallBindingsOnceBeforeImmediateStateReads  (rød på basen 3/3)
  hostedAgentIdentityProvesRemoteBridgeControl                          (flaky på basen 2/3)
```

Siste kjøring, etter at miljøoverstyringen og dens tester kom til:

```
TAG=wp7   EXIT_BUILD=0
Test run with 204 tests in 37 suites failed after 4.108 seconds with 1 issue.
  hostedAgentIdentityProvesRemoteBridgeControl   (flaky på basen, 2 av 3)
```

**165 → 204 tester: 39 nye, alle grønne. Null nye feil.**

Merk at `decodedDefaultAgentCellsInstallBindingsOnceBeforeImmediateStateReads`,
som var rød i alle tre basiskjøringene, var grønn i `wp7`. Begge de to gamle
røde er altså ustabile — de skifter fra kjøring til kjøring uavhengig av dette
arbeidet. Akseptansen her måler **ingen nye feil**, ikke alle grønne.

## Menylinjens tilstander <a id="menu"></a>

`test.menu.three-states` og `test.menu.unknown-is-not-ok`, i
`Tests/HavenAgentMenuCoreTests/MenuPresentationTests.swift`.

Den bærende egenskapen er `claimsAllClear`, som er sann på nøyaktig **ett**
sted: alle kilder lest og ingenting som venter. Testen
`noFailureIsEverDrawnAsCalm` kjøres over alle fem feilutfall
(`missingConfiguration`, `missingToken`, `unauthorized`, `unreachable`,
`malformed`) og krever for hvert av dem at ikonet er `unknown`, at
`claimsAllClear` er falsk, at radlisten **ikke** er tom, og at hver rad er
merket som problem. `eachFailureGetsItsOwnHeadlineSoTheFixIsObvious` krever at
de fem overskriftene er innbyrdes forskjellige — «det virker ikke» hjelper
ingen; «token avvist» og «ingen kontakt» krever hver sin handling.

Alle grønne i `wp6`-kjøringen.

## Challenge-innboksen <a id="challenge"></a>

`test.challenge.inbox-shape` og `test.challenge.sources`, i
`Tests/HavenAgentRuntimeTests/AgentChallengeInboxTests.swift` (19 tester).

Kjernen: tjenesten skriver alltid ut en rad for **hver** kjent kilde, også der
det ikke finnes noen leverandør. En ulesbar kilde blir dessuten sin egen sak i
listen, slik at flaten ikke blir roligere jo mindre den får lest.
`unreadableReasonThatLooksLikeASecretNeverReachesTheChallengeText` viser at en
begrunnelse som inneholder noe token-lignende blir erstattet, ikke videreført.

De negative fixturene (8 poster i `inbox-negative.json`) kjøres én for én, og
hver enkelt må avvises med sin egen oppgitte grunn.

## Ende til ende mot en ekte agent <a id="e2e"></a>

`test.challenge.answer-uses-real-path`. Agenten ble startet i en engangsrot på
port 43119 og spurt over HTTP. Kjetils kjørende agent ble ikke rørt.
Full logg: `e2e.log`.

```
GET /challenges  uten token   → HTTP 401  {"reason":"Local control bridge token missing or invalid."}
GET /challenges  med token    → HTTP 200
GET /status/summary           → HTTP 200  {"state":"attention","attentionCount":1,"headline":"1 venter på deg"}
```

Innboksen fra den faktiske agenten:

```json
"sources": [
  { "source": "intent-review",  "state": "read",           "lastReadAt": "2026-09-09T23:43:37Z" },
  { "source": "scaffold-queue", "state": "not-configured",
    "reason": "Godkjenningskøen i scaffolden er ikke koblet til denne agenten ennå. Åpne scaffold-admin for tilgang og påfyll." },
  { "source": "agent-health",   "state": "read",           "lastReadAt": "2026-09-09T23:43:37Z" },
  { "source": "job",            "state": "not-configured",
    "reason": "Ingen leverandør er koblet til for denne kilden i denne versjonen." }
]
```

Den ene challengen agenten fant i engangsroten var ekte: `config.json` finnes
ikke der, og agenten meldte det som noe et menneske må ordne — ikke som en
tom liste.

Svarveien, verifisert over HTTP:

```
POST /challenges/respond  {"challengeID":"intent-review:finnes-ikke","response":"approve"}
  → {"accepted": false, "answeredVia": "ReviewCommandService.approve"}

POST /challenges/respond  {"challengeID":"agent-health:identity-missing","response":"approve"}
  → {"accepted": false, "answeredVia": "ingen",
     "detail": "Denne saken kan ikke besvares herfra ennå. Åpne flaten som eier den."}
```

`answeredVia` er ikke pynt: den er navnet på funksjonen svaret faktisk gikk
gjennom, og den er den samme som `haven-agentd review-approve` bruker. En sak
flaten ikke kan besvare får `"answeredVia": "ingen"` i stedet for en snarvei.

## Varsler <a id="notify"></a>

`test.notify.purpose-gate`, `test.notify.no-duplicates`, `test.notify.no-secrets`,
i `Tests/HavenAgentMenuCoreTests/NotificationDeciderTests.swift` (9 tester, alle grønne).

- Bare `needsHuman` varsles.
- Samme sak sett tre ganger gir ett varsel.
- Besvart sak gjenoppstår ikke; «ignorer i dag» demper varselet uten å påstå at saken er løst.
- Over tre samtidige saker samles de til ett varsel.
- En sak som forsvinner og kommer tilbake kan varsle på nytt.
- Hver varslet tekst kjøres gjennom hemmelighetsfilteret.

`test.notify.appears-in-center` er **ikke kjørt**: det krever en våken skjerm
og at et menneske har gitt varselsamtykke. Se `#gjenstår`.

## App-bundle <a id="app"></a>

```
Build of product 'haven-agent-menu' complete! (12.72s)
Packaging/menu-app/make_app.sh debug → .build/debug/HAVEN Agent.app
Identifier=io.digipomps.haven.agentmenu
Format=app bundle with Mach-O thin (arm64)
CodeDirectory v=20400 flags=0x2(adhoc)   Signature=adhoc
```

Appen ble startet på Kjetils maskin kl. 01:47 lokal tid og kjører (PID 44404).
Kjetils egen agent svarer på 43110 (HTTP 401 uten token, altså i live).

## Det som ikke er verifisert <a id="gjenstår"></a>

| Rad | Hvorfor ikke |
|---|---|
| L5, kjørende meny med bilde | `screencapture` ga svart bilde: skjermen sover. Appen **kjører**, men et bilde av menylinjen krever at skjermen er våken. Kjetil ser den selv når han logger inn. |
| L6, faktisk varsel i varslingslisten | Krever at et menneske svarer på macOS' samtykkedialog første gang. Appen ber om det ved oppstart og viser svaret i menyen («Varsler: …»). |
| Scaffold-køen med ekte data | `entity:digipomps`/`entity:dimy` finnes ikke på staging, og agentidentiteten har ingen dokumentert leserett til `AdminFundingQueueCell`. Kilden melder erklært fravær — den later ikke som den er tom. |
| Den kjørende agenten på 43110 | Den kjører **forrige** binær, uten `/challenges`. Menyen vil derfor vise «Agenten kjører en versjon uten challenge-innboks» til daemonen startes på nytt med dette bygget. Jeg har ikke restartet Kjetils produksjonsagent mens han sov. |


## Kodegjennomgang og rettelser <a id="review"></a>

Commit-jobben leste hele diffen før den committet, og fant åtte konkrete
mangler. Alle er rettet, hver med sin egen test. Dette er den mest verdifulle
enkeltrunden i hele oppgaven, og den kom av at en annen leser gikk gjennom
koden linje for linje.

| # | Funn | Rettelse | Test som binder den |
|---|---|---|---|
| 1 | `AgentMenuModel.start()` ble aldri kalt. Appen ville aldri hentet noe, aldri bedt om varseltillatelse, aldri startet timeren. **Dette alene ville gjort demoen død.** | `.task { model.start() }` på menylinjeetiketten — den eneste visningen som alltid finnes | verifiseres av at appen faktisk henter (se `#e2e` og kjørende app) |
| 2 | «Åpne» ble sendt til broen som et svar, og en `accepted: true` markerte saken som besvart | `.open` og `.dismissToday` håndteres lokalt; modellen setter et flagg vinduet leser | — (flatehandling) |
| 3 | Menyen tilbød Godkjenn/Avvis på alle saker, uavhengig av sakens `responses`. En helsesak fikk knapper broen ikke støtter | `MenuRow` bærer sakens egne `responses`; varselkategorien velges av dem | `aHealthChallengeOffersNoApproveButton`, `anApprovableChallengeCarriesItsOwnOptions` |
| 4 | Saker ble merket varslet **før** varselet var levert. Et varsel som aldri nådde fram gjorde saken taus resten av økten | `pending(for:)` husker ingenting; `markNotified` kalles først når `post` returnerer `true` | `pendingDoesNotRememberAnythingOnItsOwn`, `aNotificationThatNeverArrivedStaysPending` |
| 5 | «Ignorer i dag» varte til appen ble startet på nytt, ikke til i morgen | Dempingen lagres med dato og utløper med døgnet | `dismissForNowExpiresWithTheDay` |
| 6 | Hemmelighetsfilteret gjaldt bare den syntetiske saken, ikke kildelistens `reason` — som går ut på flaten på lik linje | `ChallengeInboxService.safeReason` brukes på alle begrunnelser | `aSecretLikeReasonIsFilteredInTheSourceListToo` |
| 7 | Kontrollbroen serialiserte innboksen uten å validere den | Broen validerer først og svarer 500 med grunn hvis den bryter sin egen kontrakt | samme test validerer innboksen |
| 8 | `validate()` sjekket ikke `contractVersion`, så en fremtidig versjon ville sluppet gjennom | Versjonen kontrolleres, med egen feil | `anUnknownContractVersionIsRejected` |

I tillegg pekte gjennomgangen på at kontraktsteksten var strengere enn
implementasjonen: skjemaet sa at **alle** kilder må være lest før ro kan
konkluderes, mens koden tillater ro når minst én er lest og resten er
`not-configured`. Koden har rett — et erklært fravær er noe annet enn et ukjent
fravær — så skjematekst og doc-kommentar er presisert i stedet for å endre
oppførselen.

### Full kjøring etter rettelsene

```
TAG=wp9   EXIT_BUILD=0
Test run with 212 tests in 41 suites passed after 4.070 seconds.
```

**212 tester, ingen feil i det hele tatt** — også de to som er ustabile på
basen var grønne denne gangen. 165 → 212: **47 nye tester**.

## Om `EXIT_TEST=1` <a id="exitcode"></a>

Andre gjennomlesing fanget noe jeg hadde oversett: `swift test` avslutter med 1
**selv når alt er grønt**. Grunnen står i loggen:

```
Pakken «HavenAgentDPackageTests.xctest» kunne ikke lastes inn fordi den ikke
inneholder en versjon for den nåværende arkitekturen.
… (mach-o file, but is an incompatible architecture (have 'arm64', need 'x86_64'))
```

XCTest-pakken lastes ikke. Den er tom — det finnes ingen `XCTestCase` i hele
repoet; alle tester er Swift Testing. Feilen finnes ordrett i det **urørte**
base-worktreet (`base.run1.log:9755`) og i baselinen (`baseline2.test.log:100`),
altså på ren `main`. Den er ikke innført her.

Konsekvensen er praktisk og verdt å vite: **exitkoden fra `swift test` kan ikke
brukes som grønt lys i dette repoet.** Signalet er linjen
`Test run with N tests … passed/failed`. Skript som sjekker `$?` vil melde feil
på et helt grønt tre — noe en CI-oppsett her vil snuble i.

## Andre gjennomlesing — seks funn til <a id="review2"></a>

Neste commit-jobb leste diffen på nytt og fant seks reelle feil som ikke var
fanget av noen test. To av dem ville gjort appen plagsom å bruke, ikke bare
unøyaktig.

| # | Funn | Rettelse | Test |
|---|---|---|---|
| 1 | `center.add` ble kalt uten completion-handler, og `post` returnerte `true` uansett. Et varsel som aldri ble registrert gjorde saken taus resten av økten — nøyaktig feilen forrige runde skulle rette, bare flyttet ett hakk ned | `try await center.add(…)`, og `false` ved feil | dekkes av kjernens kvitteringstester; selve senteret krever GUI |
| 2 | **Et samlevarsel husket bare sin egen syntetiske ID.** De seks underliggende sakene var fortsatt «ikke varslet», så appen ville laget et nytt samlevarsel **hvert 20. sekund**. Testen som skulle dekke dette brukte `decide`, som hadde sin egen løkke — appen bruker `pending` + `markNotified` | Beslutningen bærer `coveredIdentifiers`; `markNotified(decision)` merker alle | `theProductionPathAlsoRemembersWhatASummaryCovered`, `dismissingASummaryDismissesTheChallengesItCovered` |
| 3 | «Ignorer i dag» frigjorde ikke saken ved døgnskifte: dempingen utløp, men «allerede varslet» holdt den ute for alltid. Den gamle testen startet fra en sak som aldri var varslet, og traff derfor ikke det vanlige forløpet | `dismissForNow` fjerner saken fra varslet-settet | `aDismissedChallengeCanNotifyAgainTheNextDay` |
| 4 | Varselkategorien var fortsatt to faste sett. En sak med bare «Godkjenn» fikk approve/reject/open; en sak med «Avvis» uten «Godkjenn» mistet sin egen knapp. Menyradene var rettet, varslene ikke | Kategori bygges av sakens egne alternativer; logikken flyttet til `ChallengeNotifierCategory` i kjernen så den kan testes | `differentResponseSetsGetDifferentCategories`, `theSameResponseSetIsAlwaysTheSameCategory` |
| 5 | `demo.sh` kjørte `pkill -f "HAVEN Agent"` — som treffer enhver prosess med den teksten, ikke bare demoens. Fast port, og den fortsatte selv om helsesjekken aldri lyktes, slik at den kunne lese en helt annen tjeneste | Finner ledig port, starter sin egen app, stopper bare egne PID-er, avbryter hvis agenten ikke svarer | `bash -n`, og skriptet er lest linje for linje |
| 6 | Observatøren for «Åpne adminflate» lå **inne i vinduet den skulle åpne**. Før vinduet hadde vært åpnet én gang fantes den ikke | Flyttet til menylinjeetiketten, som alltid finnes | gjenstår som GUI-sjekk |

```
TAG=wp11   EXIT_BUILD=0
Test run with 217 tests in 42 suites failed after 4.086 seconds with 1 issue.
  hostedAgentIdentityProvesRemoteBridgeControl   (flaky på ren base, 2 av 3)
```

**165 → 217 tester: 52 nye. Null nye feil.**

### Ærlig om dekningen

Gjennomlesingen påpekte også at «én test per rettelse» ikke stemte, og den har
rett. Ingen av de nye testene kaller appens `start()`, åpner et vindu, prøver
varselsenterets kategorier mot ekte macOS, eller sender en ugyldig innboks
gjennom broens HTTP-rute. Det som er dekket er kjernens logikk; det som gjenstår
er GUI-laget og selve varselsenteret, og det krever en våken skjerm og et
menneske. Det står som ikke gjort, ikke som gjort.

To runder gjennomlesing fant til sammen **fjorten** reelle feil i kode som
bygget grønt og hadde 47 grønne tester. Det er den klareste enkeltobservasjonen
fra denne oppgaven.

## Tredje gjennomlesing — seks funn til <a id="review3"></a>

| # | Funn | Rettelse | Test |
|---|---|---|---|
| 1 | To overlappende oppdateringer kunne varsle samme sak to ganger: listen ble beregnet før ventingen på varselsenteret, og `@MainActor` gjør ikke en `await`-strekning udelelig | Oppdateringer er gjensidig utelukkende; saken reserveres før levering og frigis hvis leveringen feiler | `aReservationIsReleasedWhenDeliveryFails`, `forgettingASummaryReleasesEveryChallengeItCovered` |
| 2 | Kategorinøkkelen dekket bare sorterte handlings-ID-er. To saker med samme handling men ulik knappetekst delte kategori — den ene arvet den andres knapper | Nøkkelen dekker handling, rekkefølge, tekst og destruktiv-flagg | `sameActionDifferentLabelIsADifferentCategory`, `orderOfActionsIsPartOfTheCategory`, `identicalShapesShareOneCategory` |
| 3 | Knappetekstene går til varselsenteret, men gikk ikke gjennom hemmelighetsfilteret | `validate()` sjekker nå `responses[].label` | `aSecretLikeButtonLabelIsRejected`, `ordinaryButtonLabelsPass` |
| 4 | Et vanlig klikk på selve varselet gir Apples `UNNotificationDefaultActionIdentifier`, ikke en av våre — så klikket gjorde ingenting | Oversettes til «Åpne»; Apples avvis-handling ignoreres eksplisitt | gjenstår som GUI-sjekk |
| 5 | Demoens `curl` hadde ingen tidsgrense, så «innen 30 s» kunne bli stående i ett kall | `--max-time` på begge kall | `bash -n` + lesing |
| 6 | Demoen slettet loggen den ba deg lese | Loggen bevares i `/tmp/haven-menylinje-demo-siste.log` ved feil | lesing |

**Én eldre test er snudd, ikke fjernet.** `theSameResponseSetIsAlwaysTheSameCategory`
krevde at rekkefølgen på svaralternativene *ikke* skulle påvirke kategorien. Det
var feil krav: rekkefølgen bestemmer knapperekkefølgen i varselet. Testen heter
nå `theSameResponseShapeIsAlwaysTheSameCategory` og krever at identisk form gir
samme kategori. Begrunnelsen står i testen selv, slik at ingen tror kravet ble
svekket for å få grønt.

```
TAG=wp13   EXIT_BUILD=0
Test run with 224 tests in 43 suites failed after 4.094 seconds with 2 issues.
  decodedDefaultAgentCellsInstallBindingsOnceBeforeImmediateStateReads  (ustabil på ren base)
  hostedAgentIdentityProvesRemoteBridgeControl                          (ustabil på ren base)
```

**165 → 224 tester: 59 nye. Null nye feil.**

Tre runder gjennomlesing har til sammen funnet **tjue** reelle feil i kode som
bygde grønt. Ingen av dem ble funnet av en test jeg selv skrev.

## Fjerde gjennomlesing — fire funn til <a id="review4"></a>

| # | Funn | Rettelse | Test |
|---|---|---|---|
| 1 | Kategorinøkkelen brukte `=`, `\|` og `;` som skilletegn — tegn som er lovlige i knappetekst. To helt ulike knappesett kunne gi identisk nøkkel, og den ene ville arvet den andres knapper. Gjennomlesingen leverte et konkret eksempel | Entydig serialisering med lengdeprefiks | `labelsContainingTheDelimitersDoNotCollide`, `theShapeItselfIsUnambiguous` |
| 2 | `destructive` var med i nøkkelen, men styrte ikke knappen. Feltet kontrakten tilbyr betydde ingenting i praksis | Flagget gjengis; `reject` er standard destruktiv når feltet mangler | lest i kilden |
| 3 | «Ignorer i dag» trykket **mens et varsel var underveis** ble overskrevet av kvitteringen. Dempingen ble da varig i stedet for å vare én dag | Reservasjonen angres hvis saken ble dempet under levering | `dismissingWhileTheNotificationIsInFlightIsNotUndoneByTheReceipt` |
| 4 | Demoens logg ble slettet ved feilutganger utenom de to eksplisitte, og skriptet påsto at loggen var bevart selv når kopieringen feilet | Oppryddingen bevarer loggen ved enhver feilkode, og sier det bare når det stemmer | lest, `bash -n` |

```
TAG=wp14   EXIT_BUILD=0
Test run with 227 tests in 44 suites failed after 4.263 seconds with 2 issues.
  begge er de kjente ustabile på ren base
```

**165 → 227 tester: 62 nye. Null nye feil.**

Fire runder gjennomlesing har funnet **tjuefire** reelle feil. Kurven flater ikke
ut like fort som man skulle tro: runde fire fant fortsatt en deterministisk
kollisjon og en tilstandsfeil som ville gjort «ignorer i dag» permanent.


## Mot den ekte main <a id="ekte-main"></a>

2026-09-11. De ni menylinje-commitene er spilt av på `origin/main` `79b359f`
uten konflikter, som grenen `pdd/agent-menylinje-og-varsler-v2`.
Forutsetnings-commiten `a2623d8` er **droppet** — den fantes bare for å
reparere den lokale commiten, og `origin/main` har allerede det den trengte
(AgentJobs landet som #11).

Verifisert i en ren klone fra GitHub, ikke fra maskinen:

| | bygg | tester | feilende |
|---|---|---|---|
| `origin/main` `79b359f` | grønt | 179 | 1 (ustabil fra før) |
| grenen `v2` | se under | | |

Pin-sjekken, kjørt mot de ekte fjernrepoene:

```
OK    cellprotocol: e03923cb2f1d ligger på main (1 commits bak toppen)
OK    sprout:       d5a70f35d59c ligger på main (0 commits bak toppen)
```

Begge pinene på den ekte main peker altså på andres main. Pinning er ikke
problemet; å pinne til noe som ikke er landet hos den andre, er.
