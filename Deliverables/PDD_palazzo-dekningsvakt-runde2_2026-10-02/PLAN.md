# PLAN — palazzo dekningsvakt runde 2

G1 godkjent 2026-10-03. G2: Kjetil valgte «Auto: bygg, test, deploy» 2026-10-03.
Stier er relative til HAVEN-roten. `HD` står for `HAVEN-Deploy/_handoff/HD-0077`, `PS` for `PalazzoScaffold`.

**Du skal ikke gjøre noe før G3.** Da ser du på siden og på `ACCEPT.md`, og sier om det er
dette du mente.

## Kort

Regelen som bygges: navn, lister og beskrivelser settes inn uendret, og modellen skriver
bare ordene rundt.

```
1 Tester først ─▶ 2 Vakten ─▶ 3 Angrep utenfra ─▶ 4 Commit og CI ─▶ 5 Deploy ─▶ 6 Mål på nett ─▶ 7 ACCEPT ─▶ G3 (du)
  røde mot          alt         funn blir            rundt 35 min      rundt        tolv kall
  dagens vakt       grønt       tester                                 15 min       og loggen
```

Hver pakke svarer til ett bladformål i `FORMAALSSPEC.md` §1. Etter denne planen teller bare
radene i §3 som fremdrift.

## Arbeidspakker

| Pakke | Formål | Hva det innebærer | Utfører | Test som skal bli grønn | Leveranse (§3) |
|---|---|---|---|---|---|
| WP1 Tester først | F4 `….failures-are-tests` | De nye «skal forkastes»-testene skrives før koden endres, og kjøres mot dagens vakt. De skal være røde: da er hullene målt, ikke bare lest. De fire svarene fra 2. oktober kl. 12:56 og setningen fra 1. oktober står ordrett | Losen, gjennom køen på Mac-en | test.vakt.roed-foerst, test.vakt.publiserte-feil | `HD/maal/PINTEST-RUNDE2-ROED-<dato>.md` |
| WP2 Innholdet uendret | F1 `….content-verbatim` | Vakten deler det godkjente svaret ved kolonet. Alt etter kolonet skal stå tegn for tegn sist i modellens tekst. Tillatt: stor eller liten forbokstav, «og» for det siste kommaet i en liste, og andre anførselstegn rundt det samme ordet. Alle andre tegn enn bokstaver, tall og tegn som sto i svaret, forkastes | Losen | test.vakt.innhold-uendret, test.vakt.trofast-godtas | `PS/Sources/App/Services/PalazzoConciergePhrasing.swift` |
| WP3 Rammen kan ikke påstå noe | F2 `….frame-cannot-claim` | Setningen foran en liste: én setning uten tegnsetting, bygd av en kort liste småord, ordene i den godkjente innledningen (også bøyd: «pizzaer» for «pizzaene») og ordene i kildetittelen. Et tall må stå foran samme ord som i innledningen. Etter et rettnavn: ett bindeledd fra en fast liste («er», «er en», «er et», «serveres som», «består av», «lages av», «lages med»). Instruksen til modellen beskriver de to formene | Losen | test.vakt.ramme, test.vakt.trofast-godtas | samme fil, og `PS/Sources/App/Services/PalazzoAnthropicPhraser.swift` |
| WP4 Skjøre svar sendes ikke | F3 `….fragile-answers-verbatim` | Før modellen spørres: har det godkjente svaret en nektelse, et forbehold, et modalverb, en lenke, en e-postadresse eller et telefonnummer, eller mer enn ett kolon, publiseres det ordrett uten kall. Bestillingssvaret blir da også 1,3 sekunder raskere | Losen | test.vakt.sendes-ikke | samme fil |
| WP5 Grunnen i loggen | F7 `….reason-in-log` | Hvert svar får én linje i containerens logg: publisert fra modellen, forkastet med navngitt regel, ingen tekst fra modellen med årsak (tidsavbrudd eller statuskode), eller ikke sendt og hvorfor. Linjen har aldri gjestens spørsmål eller nøkkelen | Losen | test.vakt.grunn, test.live.grunn-i-loggen | `PS/Sources/App/Controllers/PalazzoCommunaleFacade.swift` (én logglinje), `HD/maal/VAKTLOGG-RUNDE2-<dato>.md` |
| WP6 Angrep utenfra | F5 `….independent-attack` | En ny tråd som ikke har skrevet reglene, får koden og de fire svarene på nett, og skriver omskrivinger for å slippe gjennom og endre meningen. Hver kjøres gjennom Swift-vakten, ikke gjennom en kopi. Funn tettes og blir tester. Et nytt sett etter frysing måles én gang | Uavhengig agent skriver; Losen kjører gjennom køen | test.vakt.uavhengig-kode | `HD/maal/VAKT-UAVHENGIG-KODE-<dato>.md` |
| WP7 På nett | F6 `….model-visible-and-covered-live` | Commit av bare navngitte filer, push, CI, deploy med egen claim og uten å laste nginx på nytt. Deretter tolv kall på tre spørsmål, innenfor taket på 30 kall per ti minutter. Skriptet kontrollerer at innholdet står uendret, og jeg leser hvert svar | Losen, gjennom køen | test.commit.bare-mine-filer, test.deploy.claim-foer-vert, test.live.modellen-syns | `HD/maal/SPOER-RUNDE2-<dato>.md`, `HD/maal/VERTSDEPLOY-RUNDE2-<dato>.md` |
| WP8 Alt virker | `pkg.std.everything-works` | Hele testmengden før og etter, dokumentene i samme endring, STATUS.md, regnearket | Losen | test.build, test.regression, test.docs-updated, test.status-current | `TESTRESULT.md`, `ACCEPT.md`, `HD/HD-0077-status-<dato>.xlsx` |

## Det som endres i koden

- `PS/Sources/App/Services/PalazzoConciergePhrasing.swift`: vakten (WP2, WP3), hva som sendes (WP4), utfallet som navngitt grunn (WP5).
- `PS/Sources/App/Services/PalazzoAnthropicPhraser.swift`: instruksen (WP3) og årsaken når modellen ikke gir tekst (WP5).
- `PS/Sources/App/Controllers/PalazzoCommunaleFacade.swift`: én logglinje per svar (WP5).
- `PS/Tests/AppTests/PalazzoConciergePhrasingTests.swift`: nye tester. Ingen eksisterende test endres.

Det som ikke endres: svarets felt og `route`-verdiene, oppslaget, siden, taket på 30 kall, nginx.

## Stopp-regler

Jeg stopper og venter på deg i stedet for å gå videre når:

1. en eksisterende test må endres for at koden skal bli grønn;
2. angrepet finner noe ingen regel kan stoppe. Da tas svartypen ut av det modellen får
   omformulere, funnet føres opp for deg, og deployen går videre uten den svartypen;
3. CI er rød to ganger på samme commit, eller deployens egen kontroll er rød;
4. en annen tråd har claim på samme tjeneste, eller et annet vindu er åpent på verten;
5. Mac-en faller ut. Da står arbeidet til den er tilbake, og jeg sier hvor det sto.

Blir færre enn seks av tolv svar på nett modellens, løsner jeg ikke vakten. Loggen sier
hvorfor, og tallet meldes som det er.

## Dataflyt {#dataflow}

Ingen ny kant mellom celler. Tre punkter på én eksisterende vei endres (se `dataflow.md`):

| Kant | Fra → til | Kontrakt | Endres? |
|---|---|---|---|
| 1 | Gjest → `POST /palazzo/api/ask` | `haven.palazzo.communale.guest-concierge.v1` | nei |
| 2 | Fasaden → kunnskapscellen → projeksjonen (godkjent svar) | `PalazzoCommunaleProjection.project` | nei |
| 3 | Godkjent svar → skal modellen spørres? | `PalazzoConciergePhrasing.mayRephrase` | ja (WP4) |
| 4 | Godkjent svar → modellen (Anthropic Messages API) | `PalazzoAnthropicPhraser` | instruksen (WP3), årsak ved feil (WP5) |
| 5 | Modellens tekst → vakten | `PalazzoPhrasingGuard` | ja (WP2, WP3) |
| 6 | Utfallet → containerens logg | én linje, uten spørsmål og nøkkel | ny (WP5) |
| 7 | Publisert svar → gjest | samme konvolutt, `route` er `model` eller `native` | nei |
