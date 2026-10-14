# Formålsspesifikasjon — palazzo dekningsvakt runde 2

Oppgavemappe: `CellProtocolDocuments/Deliverables/PDD_palazzo-dekningsvakt-runde2_2026-10-02` · Opprettet 2026-10-02 · Iterasjon 2 (venter på G1)

Stier er relative til HAVEN-roten. `HD` står for `HAVEN-Deploy/_handoff/HD-0077`, `PS` for `PalazzoScaffold`.

> Regel: ingen plan før G1 er godkjent av Kjetil. Ingen kode før G1.
> Et dokument om leveransen teller aldri som leveransen.

## Kort — les dette først

Du valgte alternativ 1: vakten skal tåle bøyningsformer, og hullene skal tettes. Etterpå har
jeg målt mer, lest koden på nytt og latt en uavhengig tråd gå gjennom forslaget mitt. Tre
ting ble annerledes. De står først, fordi de endrer hva du godkjenner.

**1. «Vakten forkaster alt modellen skriver» var feil.** Jeg hadde målt seks kall, og alle
seks fikk det samme godkjente svaret (pizzalisten). Kl. 18:35 UTC kom ett svar på nett i
modellens ord: «Vitello tonnato serveres som tynne skiver kalveroastbiff med tunfiskmajones,
ristet kalvebrissel og asparges.» Modellen syns altså allerede på noen beskrivelser av
enkeltretter. Den syns ikke på listene.

**2. Hullene er flere enn de to jeg nevnte, og de gjelder svar som ligger på nett nå.**
Vakten krever i dag bare at ord med stor forbokstav står igjen. En omskriving av «Busiate
Primavera: Pasta med asparges, erter, fava, mandler, salvie, mynte og sitron.» kan miste
«mandler» og likevel bli publisert. Bestillingssvaret kan miste lenken og «ikke» i «kan ikke
opprette eller endre reservasjonen her». Ingen av delene er sett på nett. Begge følger av reglene
slik de står i koden, og begge blir tester.

**3. Å tåle bøyningsformer tetter ikke dette.** Den uavhengige gjennomgangen viste at en
vakt som bare ser på ord, kan lures selv når hvert ord står på plass i riktig rekkefølge:
et komma deler én rett i to, og et tall flyttes foran en annen rett. Derfor foreslår jeg en
enklere og strengere regel enn den jeg beskrev for deg:

> **Navn, lister og beskrivelser settes inn uendret. Modellen skriver bare ordene rundt.**

```
Godkjent svar
│
├─ En liste
│    «Pizzaene i kunnskapsgrunnlaget er: Pizza Margherita, … Pizza Salina.»
│    Modellen skriver setningen foran. Listen står tegn for tegn.
│    →  «Vi har følgende pizzaer: Pizza Margherita, … Pizza Salina.»
│
├─ Én rett med beskrivelse
│    «Vitello tonnato: Tynne skiver kalveroastbiff med tunfiskmajones, …»
│    Modellen bytter kolonet med et bindeledd. Navnet og beskrivelsen står ord for ord.
│    →  «Vitello tonnato serveres som tynne skiver kalveroastbiff med tunfiskmajones, …»
│
└─ Alt annet
     Bestilling (lenke, e-post, telefon, «kan ikke»), flere retter i ett svar, avvisninger.
     Gis ordrett. Sendes ikke til modellen.
```

Bøyningsformene du valgte, er med: i setningen foran en liste får modellen skrive «pizzaer»
for «pizzaene».

**Formålene** (hele treet med mål står i §1):

```
Conciergen svarer med modellens ord bare når ordene dekkes av det godkjente svaret
│
├─ F1  Innholdet står uendret                                       (skal ikke endres)
│        ingen ingrediens blir borte, ingen rett deles i to, ingenting flyttes
├─ F2  Modellens egne ord kan ikke påstå noe                        (skal ikke)
│        ingen «bare», «blant annet», «ikke», «var» eller «på tilbud» foran listen
├─ F3  Svar der ett ord kan snu meningen, sendes ikke til modellen  (skal ikke)
│        bestillingssvaret, svar med forbehold, flere retter i ett svar
├─ F4  Hvert publisert feilsvar og hvert funnet hull står igjen som test
├─ F5  Vakten er angrepet av noen som ikke har skrevet den
├─ F6  På nett kommer noen svar fra modellen, og hvert av dem holder
└─ F7  Når et svar ikke kommer fra modellen, står grunnen i loggen
         i dag kan ingen se om modellen feilet eller ble forkastet
```

**Det du kommer til å se** (hele tabellen står i §3):

1. På `https://palazzo.digipomps.org/palazzo`: spør «Hvilke pizzaer har dere?», «Hva har
   dere på menyen?» og «Fortell om Vitello tonnato.» I minst seks av tolv forsøk syns
   modellens setning eller bindeledd, og innholdet står som i det godkjente svaret.
2. En fil med tolv svar fra nett på tre spørsmål, hvert holdt mot det godkjente svaret.
3. Den uavhengige gjennomgangen: hva den fant i forslaget (ligger ved nå), og hva den
   finner i den ferdige koden.
4. Testene: 227 grønne før (målt kl. 18:33 UTC), de nye testene røde mot dagens vakt, og
   alt grønt etterpå.

**Det du skal gjøre:** svare på tre spørsmål nå (§6): om formålene er riktige, om modellen
får si «Vi har …», og hvordan du vil ha planen. Etter deployen ser du på siden og sier om
det er dette du mente (G3).

**Tiden:** jeg skrev «rundt en time». Det riktige er rundt tre og en halv time etter G1.
CI og deploy er 50 minutter av det. Mac-en må være våken og koblet til hele tiden; kl.
18:15–18:23 UTC falt den ut.

## 0. Intensjon (ordrett) og brief-audit

Kjetil, 2. oktober 2026:

> 1.

Det var svar på dette valget, som Losen la fram samme dag kl. 13:32 UTC:

> Modellen blir spurt på hvert spørsmål, og det tar 1,3–1,8 sekunder. Men vakten forkaster
> alt den skriver, fordi den krever ordene nøyaktig: «pizzaer» for «pizzaene» er nok.
> Conciergen svarer riktig, men modellen syns ikke.
>
> Vakten har også to hull, som jeg fant ved å lese den. En omskriving kan påstå «vi har
> også andre retter», eller snu et «ikke», uten å bruke et nytt innholdsord. Ingen av
> delene er sett i målingene etter deployen.
>
> 1. **Tåle bøyningsformer og tette hullene (anbefalt):** modellen blir synlig, og vakten
>    blir strengere der den i dag er for slapp. Det er én runde til, rundt en time.
> 2. **La det stå:** riktig svar hver gang, rundt 1,3 sekunder tregere enn nødvendig, og
>    hullene står.
> 3. **Slå modellen av:** samme svar som nå, uten ventetiden.

Audit av hver påstand i valget og hver kapabilitet oppgaven bygger på:

| Påstand i intensjonen / antatt kapabilitet | Audit | Kilde |
|---|---|---|
| Modellen blir spurt, og det tar 1,3–1,8 s | retrieved | `HD/maal/TID-CONCIERGEN-20261002.md` (13:20:00 UTC). Samme bilde kl. 18:33 UTC: 1,1–1,8 s for svar som sendes, 0,2–0,3 s for avvisninger (`HD/maal/SPOER-PROEVE-20261002.md`) |
| «Vakten forkaster alt den skriver» | contradicted | `HD/maal/SPOER-PROEVE-2-20261002.md` (18:35:16 UTC), rad 2: `route: model` på «Fortell om Vitello tonnato.» Påstanden bygde på seks kall med ett og samme godkjente svar (`HD/maal/SPOER-ETTER-DEPLOY-20261002.md`) |
| «… fordi den krever ordene nøyaktig» | unavailable | Hvorfor et svar blir `native`, er ikke målt: verken modellens tekst, en feil fra modellen eller vaktens grunn logges (`PS/Sources/App/Services/PalazzoConciergePhrasing.swift`, linje 65–86). At ordene må stå nøyaktig, er lest i linje 116–125. Derfor F7 |
| «Vakten har to hull» | contradicted | Det er flere. Lest i samme fil: bare ord med stor forbokstav må stå igjen (linje 126–129 og 186–201); ordene sammenlignes som mengder, så rekkefølge og antall teller ikke (linje 123–125); listen over frie ord har nektelser, modalverb, omfangsord og «var» (linje 142–167). Den uavhengige gjennomgangen fant ni mekanismer: `HD/maal/VAKT-UAVHENGIG-FORSLAG-20261002.md` |
| Fire slags godkjente svar ligger på nett: pizzalisten, 18 retter, bestilling, og én rett med beskrivelse | retrieved | `HD/maal/SPOER-PROEVE-20261002.md` og `HD/maal/SPOER-PROEVE-2-20261002.md`. Malene: `PS/Sources/App/Controllers/PalazzoCommunaleProjection.swift`, linje 130–162 |
| «Vitello tonnato: Tynne skiver kalveroastbiff med tunfiskmajones, ristet kalvebrissel og asparges.» er det godkjente svaret bak modellens setning | retrieved | `PS/Sources/App/Resources/RestaurantConcierge/palazzo_seed_corpus.json` (`menu-vitello-tonnato`) og malen i linje 151–161 |
| Busiate Primavera har mandler, og retten er merket med allergenkoden N | retrieved | Samme korpusfil (`menu-busiate-primavera`) |
| Den ene trofaste omskrivingen av pizzalisten som er publisert («Vi har følgende pizzaer: …», 12:56 UTC) har to ord dagens vakt ikke godtar: «følgende» og «pizzaer» | retrieved | `HD/maal/SPOER-FOER-DEPLOY-20261002.md`, rad 5, holdt mot linje 116–125 og 142–167. Lest, ikke kjørt |
| Siden viser advarselen om datert grunnlag under hvert svar | retrieved | `PS/Public/js/palazzo-communale.js`, linje 107–114; teksten i `PalazzoCommunaleProjection.swift`, linje 12 |
| Siden viser ikke om teksten er modellens | retrieved | Ingen bruk av `route` under `PS/Public`. Feltet står bare i API-svaret |
| Conciergen tar 30 kall per ti minutter per adresse | retrieved | `PS/Sources/App/Controllers/PalazzoCommunaleFacade.swift`, linje 156–170. Målt: kall 31 og 32 fra Mac-en fikk 429 kl. 18:35 UTC |
| På nett nå: image `sha-39d0657c…`, «healthy», modellen på | retrieved | `HD/maal/STATUS-20261002-KVELD.md` (18:10:44 UTC) |
| Arbeidstreet står på `39d0657c`, likt med origin | retrieved | `HD/maal/GIT-TILSTAND-KVELD-20261002.md` (18:10:51 UTC) |
| 227 tester grønne på dette treet nå | retrieved | `HD/maal/PINTEST-RUNDE2-FOER-20261002.md` (18:33:28 UTC) |
| En annen tråd arbeider i samme arbeidstre (`Sites/` laget 18:07–18:09 UTC, `Deliverables/` 10:50) | retrieved | `HD/maal/GIT-TILSTAND-KVELD-20261002.md` |
| Andre tråder bruker bane b og c i køen fra kl. 18:54 UTC | retrieved | `_losen-queue/logs/runner.log` |
| Hver deploy laster nginx på nytt (`KJOR-1`), og HD-0141 har claim på nginx | retrieved | `HD/host/KJOR-1-root-vhost-og-katalog.sh`, linje 80–82; `_losen-queue/KOORDINERING.md` |
| CI tar rundt 32 minutter | retrieved | `HD/maal/CI-VARIGHET-2-20261002.md` |
| «Rundt en time» | contradicted | Commit til kvittering tok 49 minutter sist (`HD/HD-0077-status-20261002.xlsx`, arket «Steg»). Kode, tester og gjennomgang kommer i tillegg |
| «Modellen skal bare formulere det kunnskapsgrunnlaget dekker» (Kjetils krav fra før) | recalled | Fra øktsammendraget; ordlyden er ikke lest fra fil i denne økten. Bærer ikke planen alene: rotformålet under sier det samme, og G1 gjør det uttrykkelig |

## 1. Formålstre

Alle noder under roten heter `purpose://candidate.palazzo-dekningsvakt-runde2.<navn>`.

| purposeRef | Tittel | Forelder | Goal (outcome) | Verifier | Status |
|---|---|---|---|---|---|
| `….root` | Conciergen svarer med modellens ord bare når ordene dekkes av det godkjente svaret | `purpose://content.review-before-publish` | Et svar merket `route: model` har det godkjente svarets innhold uendret, modellens egne ord påstår ingenting, og noen svar på nett kommer faktisk fra modellen | Bladformålene F1–F7 | candidate |
| `….content-verbatim` (F1, skal ikke endres) | Innholdet står uendret | root | I et svar fra modellen står alt etter kolonet i det godkjente svaret tegn for tegn: hvert navn, hver ingrediens, hvert tall, hvert komma. Det eneste som får variere, er stor eller liten forbokstav, og «og» for det siste kommaet i en liste | XCTest; skriptet som måler mot nett, kontrollerer det samme | candidate |
| `….frame-cannot-claim` (F2, skal ikke) | Modellens egne ord kan ikke påstå noe | root | Setningen foran en liste bygges bare av ordene i den godkjente innledningen, også i bøyd form, og en kort liste småord uten nektelse, omfang, grad, tid eller vilkår. Bindeleddet etter et rettnavn velges fra en fast liste | XCTest | candidate |
| `….fragile-answers-verbatim` (F3, skal ikke) | Svar der ett ord kan snu meningen, sendes ikke til modellen | root | Et godkjent svar med nektelse, forbehold, modalverb, lenke, e-post eller telefonnummer, eller med flere retter og beskrivelser, publiseres ordrett uten kall til modellen | XCTest: stubben får null kall | candidate |
| `….failures-are-tests` (F4) | Hvert publisert feilsvar og hvert funnet hull står igjen som test | `purpose://test.acceptance.hallucination-evaluation` | De fire svarene fra 2. oktober kl. 12:56, setningen fra 1. oktober og hvert hull funnet ved lesing og i gjennomgangen forkastes, ordrett. De nye testene er røde mot dagens vakt før noe endres | XCTest, kjørt før og etter endringen | candidate |
| `….independent-attack` (F5) | Vakten er angrepet av noen som ikke har skrevet den | `purpose://test.acceptance.hallucination-evaluation` | En tråd som ikke har skrevet reglene, får koden og finner ingen omskriving av svarene på nett som slipper gjennom og endrer meningen | Rapport, og XCTest for hvert funn | candidate |
| `….model-visible-and-covered-live` (F6) | På nett kommer noen svar fra modellen, og hvert av dem holder | root | Av tolv kall på tre spørsmål med ulike godkjente svar er minst seks `route: model` med en annen ordlyd enn det godkjente svaret, og i hvert av dem står innholdet uendret | Måling utenfra, kontrollert av skript og lest | candidate |
| `….reason-in-log` (F7) | Når et svar ikke kommer fra modellen, står grunnen i loggen | root | For hvert svar som kunne vært sendt til modellen, sier loggen én av tre ting: publisert fra modellen, forkastet med navngitt regel, eller ingen tekst fra modellen med årsak. Loggen har aldri gjestens spørsmål eller nøkkelen | XCTest; utdrag fra vertens logg etter målingen | candidate |

Forelderen `purpose://content.review-before-publish` og
`purpose://test.acceptance.hallucination-evaluation` er lest fra
`CellProtocolDocuments/Book/haven_purpose_knowledge_base_v0.json` i denne økten. Ingen ny
node er oppfunnet av en modell.

Suksessignaler, bestemt før runden kjøres:

- **F1–F4:** hver test under §5 er grønn. Ingen eksisterende test er fjernet eller svekket.
  De nye «skal forkastes»-testene er vist røde mot dagens vakt først, så hullene er målt og
  ikke bare lest.
- **F5:** null godtatte omskrivinger som endrer meningen. Et funn tettes med en regel og en
  test. Kan ingen regel tette det, tas svartypen ut av det modellen får omformulere, og
  funnet føres opp for deg i `ACCEPT.md`. Settet regnes fra første funn som utviklingssett.
  Et nytt sett, skrevet etter at reglene er frosset, måles én gang og er tallet som
  rapporteres.
- **F6:** minst 6 av 12 med annen ordlyd, og 0 med endret innhold. Blir det færre enn seks,
  løsner jeg ikke vakten. Loggen (F7) sier da hvorfor, og tallet meldes som det er.
- **F7:** hvert av de tolv kallene har en linje i loggen med utfallet.

## 2. Avgrensning og avhengigheter

Hva dette IKKE er:

- Ikke at oppslaget blir bedre. «Hva er på Pizza Siciliana?» og «Hva har dere som ikke er
  pizza?» gir fortsatt pizzalisten.
- Ikke en ny modell, og ikke en ny flate. Siden viser ikke om teksten er modellens; å vise
  det er en egen oppgave med bildeport.
- Ikke fritekstsvar uten kolon. De finnes ikke på nett i dag (se slutten av §6).
- Ikke at det godkjente svaret vises ved siden av modellens.
- Ikke en endring av taket på 30 kall per ti minutter.
- Ikke rettelse av `X-Forwarded-For` i nginx, og ikke årsaken til at enkelte kall aldri
  når verten.

| Kapabilitet | Kilde (fil) | Avgrensning | Må virke før test? |
|---|---|---|---|
| Køen på Mac-en kjører `skript`-jobber | `_losen-queue/runner.sh` (tilsyn fra 2. oktober) | Mac-en må være våken og koblet til. Falt ut kl. 18:15–18:23 UTC. Bane b og c brukes av andre tråder; denne oppgaven holder seg til bane d | Ja |
| Bygg og test av arbeidstreet | `HD/mac/cp-pin-verifiser-og-test-20260929.sh` | Hele testmengden mot pinnen `81601a6f`, med egen scratch i `/tmp/palazzo-pintest/build`. Tok 40 sekunder kl. 18:33 UTC | Ja |
| Commit av bare navngitte filer | `HD/mac/deploy-commit-20261002.sh` | Holder i dag bare `Deliverables/` utenfor. Må få en liste over filene som skal med, fordi `Sites/` er kommet til | Ja, før commit |
| CI bygger og publiserer image | `PS/.github/workflows/palazzo-image.yml` | Rundt 32 minutter | Ja, før deploy |
| Deploy med claim og kvittering | `HD/mac/deploy-vert-20260930.sh` | Laster nginx på nytt hver gang. Skal hoppe over `KJOR-1` når siden alt svarer over https | Ja, før F6 |
| Verten deles med andre utsettinger | `_losen-queue/KOORDINERING.md`, avsnittet «Korrespondanse-fornyelse» (skrevet kl. 18:52 UTC av en annen Claude-tråd) | Staging 2026.9.4 og en liten utgivelse etter den er bestilt på samme vert. HD-0077 tar egen claim og kjører ikke samtidig med et annet vindu | Ja, før deploy |
| Modellen nås fra containeren | `/opt/palazzo/.env` på verten 89.167.90.101 (bruker ops) | Måles på svaret og på loggen (F7), aldri på nøkkelen | Ja, før F6 |
| Containerens logg kan leses av ops | `docker logs` på verten, gjennom et nytt leseskript under `HD/host/` | Ikke prøvd i denne oppgaven ennå. Første steg etter deploy | Ja, før F7 |
| Måling mot nett innenfor taket | `HD/mac/spoer-liste-20261002.sh` (ny, brukt kl. 18:32 og 18:35 UTC) | 30 kall per ti minutter per adresse. Deployens egne kontroller bruker av samme kvote | Ja, før F6 |
| En uavhengig tråd som ikke har skrevet reglene | Agent startet fra denne økten | Første runde er gjort på forslaget. Neste runde får den ferdige koden, og en ny tråd | Ja, før F5 |
| Arbeidstreet deles med en annen tråd | `HD/maal/GIT-TILSTAND-KVELD-20261002.md` | Jeg rører bare `PS/Sources/App/Services/PalazzoConciergePhrasing.swift`, `PS/Sources/App/Services/PalazzoAnthropicPhraser.swift` og `PS/Tests/AppTests/PalazzoConciergePhrasingTests.swift` | Ført i `_losen-queue/KOORDINERING.md` kl. 18:31 UTC |

## 3. Forventningskontrakt — «Det du kommer til å se»

Én rad per leveranse. Dette er det eneste som teller som fremdrift etter G2. Ingen flate
endrer utseende, så det er ingen bildeport. `<dato>` er dagen målingen tas.

| Leveranse | Type | Hvor | Referanse | Godkjent |
|---|---|---|---|---|
| «Hvilke pizzaer har dere?», «Hva har dere på menyen?» og «Fortell om Vitello tonnato.» gir svar der modellens setning eller bindeledd syns i minst seks av tolv forsøk. Innholdet står som i det godkjente svaret | kjørende flate | `https://palazzo.digipomps.org/palazzo` | `ACCEPT.md#live` | nei |
| Tolv svar fra nett på tre spørsmål, hvert med rute, tekst og kontroll mot det godkjente svaret | fil | `HD/maal/SPOER-RUNDE2-<dato>.md` | `ACCEPT.md#live` | nei |
| Grunnen for hvert svar som ikke kom fra modellen | fil | `HD/maal/VAKTLOGG-RUNDE2-<dato>.md` | `ACCEPT.md#logg` | nei |
| Uavhengig gjennomgang av forslaget, før kode | fil | `HD/maal/VAKT-UAVHENGIG-FORSLAG-20261002.md` (ligger ved) | `TESTRESULT.md#uavhengig` | nei |
| Uavhengig angrep på den ferdige koden: hva som ble prøvd, og hva som slapp gjennom | fil | `HD/maal/VAKT-UAVHENGIG-KODE-<dato>.md` | `TESTRESULT.md#uavhengig` | nei |
| Hele testmengden: 227 grønne før, de nye testene røde mot dagens vakt, alt grønt etter | testutdata | `HD/maal/PINTEST-RUNDE2-FOER-20261002.md` (finnes), `HD/maal/PINTEST-RUNDE2-ROED-<dato>.md`, `HD/maal/PINTEST-RUNDE2-ETTER-<dato>.md` | `TESTRESULT.md#regression` | nei |
| Kvittering for deployen: `COMMITTED_VERIFIED`, image og tidspunkt | fil | `HD/maal/VERTSDEPLOY-RUNDE2-<dato>.md` | `ACCEPT.md#deploy` | nei |
| Regnearket oppdatert med det som ble målt | fil | `HD/HD-0077-status-20261002.xlsx` | `ACCEPT.md#status` | nei |

## 4. Tilknyttede formålspakker og lærdommer (auto fra purpose_dev.py lookup)

## Formålspakker som festes
- **pkg.std.everything-works** — Alt skal virke (standard kvalitetsport)
    - purpose://quality.build-and-regression: Alle berørte mål bygger og eksisterende tester passerer uten at tester er fjernet eller svekket.
        - test test.build [command]: Bygg alle berørte mål. → TESTRESULT.md#build
        - test test.regression [command]: Kjør hele eksisterende testmengde. → TESTRESULT.md#regression
    - purpose://quality.docs-in-same-change: Alle dokumenter som beskriver endret oppførsel er oppdatert og datert 'Last verified against code'.
        - test test.docs-updated [inspection]: Hver endret kontrakt/atferd har tilsvarende doc-diff. → ACCEPT.md#docs
    - purpose://quality.work-is-visible: Oppgavemappen har oppdatert STATUS.md med gate-tilstand, og et eventuelt planbytte er datert og begrunnet.
        - test test.status-current [inspection]: STATUS.md speiler faktisk tilstand. → ACCEPT.md#status
    - artefakt FORMAALSSPEC.md (port G1): Godkjent formålsspesifikasjon.
    - artefakt PLAN.md (port G2): Arbeidspakker 1:1 mot bladformål.
    - artefakt TESTRESULT.md (port G3): Utdata fra alle avledede tester.
    - artefakt ACCEPT.md (port G3): Forventning mot faktisk, per leveranse.
    - artefakt STATUS.md (port G3): Gate-tilstand og planbytter.
- **pkg.std.cell-contract** — Cellekontrakt
    - purpose://cell.contract-explicit: Book/<celle>_contract_v<n>.json finnes, og en validator kjører grønt på alle fixtures.
        - test test.cell.contract-fixtures [command]: Kjør kontraktvalidator mot positive/negative fixtures. → TESTRESULT.md#contract
    - purpose://cell.authorization-honours-keypath: Negative tester viser at feil requester, feil keypath og purpose://prompt.unknown alle avvises.
        - test test.cell.auth-negative [command]: Feil requester / feil keypath / ukjent formål avvises. → TESTRESULT.md#auth
    - purpose://cell.no-empty-stubs: Ingen endepunkt i kontrakten er implementert som no-op uten status 'not-implemented'.
        - test test.cell.stub-scan [inspection]: Liste alle no-op-handlere og avstem mot Gap_Analysis.md. → ACCEPT.md#stubs
    - artefakt contract/ (port G2): Kontrakt-JSON + fixtures (kan være lenke til Book/).
- **pkg.std.cell-combination** — Cellekombinasjon og dataflyt
    - purpose://cells.dataflow-declared: dataflow.md (eller .graffle/.json) finnes med alle kanter navngitt med endepunkt/event.
        - test test.cells.dataflow-matches-contracts [inspection]: Hver kant i dataflow finnes i en kontrakt. → PLAN.md#dataflow
    - purpose://cells.capabilities-declared-with-boundary: FORMAALSSPEC.md §2 lister hver antatt kapabilitet med kildefil og hva den ikke dekker.
        - test test.cells.capability-audit [inspection]: Alle kapabilitetspåstander har audit-status retrieved. → FORMAALSSPEC.md#audit
    - artefakt dataflow.md (port G2): Diagram + kant-tabell.
- **pkg.std.codex-handoff** — Overlevering til Codex/terminal
    - purpose://handoff.runnable-without-guessing: README.md i _handoff-mappen har rekkefølge, forventet utfall per steg, og alle skript støtter --dry-run/--go.
        - test test.handoff.dry-run [command]: Tørrkjøring gir 0 og lister hva som ville skjedd. → TESTRESULT.md#dry-run
    - artefakt handoff/README.md (port G2): Rekkefølge og kommandoer.

## Lærdommer du må lese før dekomponering
- **lesson.plan-instead-of-delivery** (2026-08-21, major): Kjetil ba om en leveranse flere ganger og fikk planer/dokumenter om leveransen i stedet.
    - forebygging: G1 godkjenner formål, ikke arbeid; etter G2 telles bare artefakter listet i §3 'Det du kommer til å se' som fremdrift. Et dokument om leveransen teller aldri som leveransen.
- **lesson.undocumented-plan-switch** (2026-08-24, major): Tre produktive døgn (22.–24.08) så tomme ut i alle statusdokumenter fordi planbyttet fra bølge 1–3 til deploy-seremonien aldri ble skrevet ned.
    - forebygging: STATUS.md i oppgavemappen oppdateres ved hvert planbytte med dato og hvorfor; sjekkes i test.status-current.
- **lesson.planned-documented-as-implemented** (2026-08-24, major): Book/05_Flows_Lifecycle.md beskrev sekvensnummer, signatur og replay som ikke finnes i structen.
    - forebygging: Docs-diff i samme endring, med 'Last verified against code'-dato; planlagt oppførsel merkes eksplisitt.
- **lesson.bridge-inferred-architecture-from-one-use** (2026-08-09, major): En kodeassistent sluttet fra én observert bruksmåte av bridge til en egenskap ved arkitekturen og konkluderte feil.
    - forebygging: Erklær hver kapabilitet oppgaven bygger på som eget formål med kilde og Avgrensning (pkg.std.cell-combination).
- **lesson.decomposition-is-classification** (2026-07-11, major): Modeller som genererte purpose://-refs fritt hallusinerte referanser.
    - forebygging: Dekomponering velger fra Book 23 + pakker først; nye noder merkes 'candidate' og navngis av Claude, aldri implisitt av en modell.
- **lesson.cellscaffold-two-holes** (2026-09-01, blocker): CellScaffold har tomme booking-/concierge-stubber og autorisasjon som kaster nøkkelstien og bare sjekker eierskap.
    - forebygging: Ikke porter celler fra CellScaffold til PalazzoScaffold uten å lukke begge hullene; test.cell.auth-negative og test.cell.stub-scan må være grønne.
- **lesson.purpose-never-grants-rights** (2026-08-03, blocker): Risiko for at formålsmatch tolkes som tilgang.
    - forebygging: Et formål kan innsnevre en rettighet, aldri opprette, utvide eller arve en; exact match; purpose://prompt.unknown feiler lukket.
- **lesson.zsh-no-inline-comments** (2026-08-25, minor): Begge kommandolinjene feilet med 'ukjent argument: #' og ingenting kjørte.
    - forebygging: Aldri forklaring på samme linje som en kommando; skript har '"#"*) break ;;' i argumentparseren.
- **lesson.mount-is-not-git** (2026-08-25, major): Hver git-kommando fra device_bash etterlot en index.lock som ikke kunne fjernes og blokkerte Kjetils commits; seks repoer låst 24.08.
    - forebygging: Aldri git mot $HOME/mnt fra device_bash; les .git/refs som filer; all git kjøres av Kjetil eller codex exec.
- **lesson.codex-mcp-60s** (2026-08-18, major): Codex-MCP-kall kuttes etter ~60 s; registerlesning og Swift-bygg sprengte taket.
    - forebygging: Bygg/test/lange jobber går via terminal codex exec eller filbasert overlevering, aldri via Codex-MCP.
- **lesson.corr-approval-surfaces-timed-out** (2026-08-30, major): Corr-godkjenningen (Vegar) er utestet fordi flater/godkjenninger timet ut før testing rakk å skje.
    - forebygging: FORMAALSSPEC.md §2 lister avhengigheter som egne formål med verifier; pkg.std.everything-works og gui.surface-loads-in-time må være grønne før den egentlige testen kjøres.
- **lesson.test-corpus-is-not-shipped-corpus** (2026-09-05, major): Rot-probe-testen, lastetidstesten og finnbarhetsauditen var gronne i to uker mens Relasjoner-flaten var tom.
    - forebygging: Enhver flate-test skal bygge korpuset fra det som faktisk sendes ut (menykonfigurasjoner + navigasjonsdestinasjoner + verifiseringshjelperen), dedupliseres, og feile hvis korpuset er mindre enn appens egen meny.
- **lesson.tested-a-different-path-than-production** (2026-09-05, major): Rot-probene leste relations.state.* gjennom porthole.get og var gronne, mens rendereren aldri fikk de samme dataene.
    - forebygging: Naar en test skal si noe om hva brukeren ser, maa den bruke produksjonens egen kodevei - helst produksjonens egen funksjon med produksjonens egne inndata (SkeletonReachabilityAudit kaller condition.evaluate(root: nil, ...) nettopp derfor).
- **lesson.paste-command-instead-of-queue** (2026-09-07, major): Kjetil fikk et innlimingsskript for å starte Codex; flagget --full-auto finnes ikke på `codex exec`, og kjøringen feilet ved første linje.
    - forebygging: Før enhver Codex-kjøring fra Cowork: `ls HAVEN/_losen-queue/inbox running; tail logs/runner.log`, legg jobben som <id>.job + <id>.prompt.md. Aldri gi Kjetil kommandoer å lime inn. Gyldige `codex exec`-flagg: --sandbox, --skip-git-repo-check, -C.
- **lesson.baseline-count-from-report-not-run** (2026-09-07, minor): PLAN.md sa «48 tester grønne»; baseline-kjøringen viste 68 tester med 3 røde.
    - forebygging: WP0/S0 baseline er alltid en ekte kjøring før endring; PLAN oppgir testtall som «forventet ≈ N (fra <kilde, dato>)», og et rødt baseline stopper ikke arbeidet men registreres som eget avvik med årsak.
- **lesson.codex-sandbox-cannot-reach-docker** (2026-09-07, major): S10 (docker compose build/up) endte i `permission denied … docker.sock` i Codex-sandkassen; deploy-slicen ble blocked.
    - forebygging: Deploy-/image-steg planlegges aldri som Codex-slice; de registreres som HAVEN-Deploy-post med eier Kjetil (eller en dispatcher-adapter med eksplisitt docker-rettighet når arbeidskø-PDD-en er levert). Se HD-0012.
- **lesson.scaffold-without-porthole-host-has-no-preview** (2026-09-07, minor): G1-GUI måtte bruke mockups rendret fra skeleton-JSON; ekte Porthole-preview var umulig.
    - forebygging: For scaffolds uten Porthole-vert: (1) images/README.md må si eksplisitt at bildene er mockups og hva skeleton ikke kan rendre, (2) paritet (test.gui.parity) planlegges som egen slice med kjørende scaffold + Binding/Porthole via bridge, ikke som del av implementeringsjobben.
- **lesson.codex-workspace-write-cannot-build-cellscaffold** (2026-09-09, major): WP0-baselinen i køen ble blocked: `sandbox-exec: sandbox_apply: Operation not permitted`. Testkommandoen brukte 1 604 sekunder uten at én eneste test startet.
    - forebygging: Lange bygg og testkjøringer legges ikke som `workspace-write`-køjobb. De kjøres som detached skript startet via Codex med `danger-full-access` og python Popen(start_new_session=True), med logg i en montert mappe som Cowork kan polle — samme mønster som produserte den notariserte HavenAgentD-pakken 2026-09-08. Køjobber brukes til analyse, kontrakter, dokumentasjon og korte kommandoer.
- **lesson.baseline-measured-another-pdds-branch** (2026-09-09, major): WP0 målte `pdd/tillitspakke-agentflaate` med 181 skitne oppføringer, ikke et rent utgangspunkt for sin egen PDD. En regresjonsbaseline derfra sier ingenting om hva denne PDD-en endrer.
    - forebygging: WP0 måler en ren eksport av den revisjonen arbeidet skal gå ut fra (`git archive <rev> | tar -x -C <scratch>`), ikke det delte arbeidstreet. Er arbeidstreet opptatt av en annen PDD, er det en planopplysning som hører i STATUS, ikke noe implementeringen skal jobbe rundt.
- **lesson.worktree-created-from-vm-has-unusable-gitdir** (2026-09-09, major): WP1 ble blocked etter ett minutt: `fatal: not a git repository: /sessions/<sesjon>/mnt/CellScaffold/.git/worktrees/_wt-sad-20260909`, exit 128. Branch og HEAD kunne ikke bekreftes.
    - forebygging: Opprett worktrees fra macOS (Codex), ikke fra VM-en. Er det allerede gjort fra VM-en: skriv om begge pekerfilene til macOS-stien og verifiser `branch --show-current` + `rev-parse HEAD` **fra macOS** før noen jobb legges i køen. En jobb skal aldri være første stedet en sti blir prøvd.
- **lesson.cellbase-decodingerror-shadows-swift** (2026-09-09, minor): WP1s nye celle ga 50 kompileringsfeil: `type 'DecodingError' has no member 'dataCorruptedError'` og `cannot infer contextual base in reference to member 'registry'`, alle fra én linje.
    - forebygging: I App-modulen: skriv `Swift.DecodingError` når du vil ha standardbibliotekets. Gjelder generelt for typenavn CellBase også definerer — sjekk med `grep -rn "enum <Navn>" CellProtocol::Sources/CellBase` før du antar at et kjent Foundation-navn er Foundations.
- **lesson.valuetype-equality-false-for-objects** (2026-09-09, major): Fire av sju WP1-tester feilet på `XCTAssertEqual` mellom to `ValueType.object` som hadde identisk innhold. Feilmeldingen viste samme nøkler og verdier på begge sider, i ulik rekkefølge.
    - forebygging: Aldri assert på hele sammensatte `ValueType`-verdier. Sammenlign kanonisk JSON (`JSONEncoder` med `.sortedKeys`) eller pakk ut og sammenlign felt for felt. Skalarer (`.string`, `.integer`, `.bool`, `.null`) sammenlignes trygt. Merk: dette er et funn i CellBase, ikke bare en testregel — App-kildene destrukturerer riktignok før sammenligning, men en fremtidig `==` på hele verdier vil stille behandle like verdier som ulike. Ikke revidert utover App-kildene.
- **lesson.syntax-check-reported-as-delivered** (2026-09-09, major): WP1 ble rapportert som «kode og 7 tester levert, syntakssjekken bestod». Et faktisk bygg ga 50 kompileringsfeil, og testene feilet 4 av 7 da de først kunne kjøre.
    - forebygging: En implementeringsslice er ikke levert før et detached bygg med `danger-full-access` er kjørt mot arbeidstreet og både bygg og de nye testene er grønne. Legg byggejobben klar FØR slicen kjøres, og skriv i prompten at slicen skal rapportere «skrevet, ikke verifisert» — ikke «levert».
- **lesson.cellbase-internal-members-look-public** (2026-09-09, minor): WP2 stoppet på `'fullPermissionString' is inaccessible due to 'internal' protection level`. Medlemmet finnes og brukes i CellBase selv, så det så ut som et gyldig API.
    - forebygging: Sjekk tilgangsnivå og faktisk returverdi før du bruker et CellBase-medlem fra App: `grep -n "var <navn>" CellProtocol::Sources/CellBase/...`. Et medlem som brukes internt i CellBase er ikke automatisk en del av API-et, og navnelikhet betyr ikke verdilikhet.
- **lesson.entityanchor-keypaths-are-registered** (2026-09-09, minor): WP2-testen skrev en sentinel til `profile` på abonnentens EntityAnchor og fikk `notFound` ved gjenlesing. Skrivingen ga ingen feil.
    - forebygging: Skriv aldri testdata til en oppdiktet keypath på en celle. Finn en keypath cellen faktisk registrerer, helst en annen test som allerede bruker den. At et `set` går gjennom er ikke bevis på at keypathen finnes.
- **lesson.new-cell-must-declare-its-provisioning-mode** (2026-09-09, major): To nye celler i CellScaffold ga tre nye regresjoner: `OrchestratorPersistenceTests testRequireExistingModeRejectsFreshStorageWithoutCreatingBootstrapCells` (opprettet en celle i require-existing-modus mot fersk lagring) og to `TopUpCheckoutTests` som teller celler i provision-only-modus (5 mot forventet 4).
    - forebygging: Enhver ny persistert celle i CellScaffold må eksplisitt svare på tre spørsmål før den registreres: (1) skal den opprettes i require-existing mot fersk lagring? Nei, med mindre den er kanonisk bootstrap. (2) Er den en av de kanoniske eager-bootstrap-cellene som provision-only skal lage? Nesten alltid nei — TopUpCheckoutTests teller dem eksplisitt. (3) Er den en Porthole-publisert flate? Bare da hører den i `reconcilePortholePublishedCellResolves`. Scaffold-intern tilstand registreres i egen funksjon, gated på policy OG provisionOnly, med gjenkjenning av eksisterende mapping.
- **lesson.branch-is-empty-after-eight-work-packages** (2026-09-09, major): Åtte arbeidspakker rapportert utført og verifisert, ACCEPT.md skrevet — men `git branch -v` viste at `pdd/scaffold-admin-delegering` fortsatt pekte på samme commit som `main` (`e1f3e22f`). All koden lå ucommittet i et worktree som bare finnes på én maskin. Ett tapt worktree = 2 750 linjer kode og test borte, med full dokumentasjon på at arbeidet var «levert».
    - forebygging: Skill «filene finnes» fra «branchen har dem». Sjekk `git rev-parse <branch>` mot `git rev-parse <base>` som del av hver verifikasjon som påstår at noe ligger på en branch; er de like, er branchen tom. Legg en commit-pakke inn i planen etter første grønne bygg, ikke etter siste arbeidspakke. Når worktreet bare kan leses fra macOS, kjør sjekken der — ikke hopp over den fordi verktøyet svarer feil.
- **lesson.stop-rule-too-wide-stops-the-job** (2026-09-09, minor): En commit-jobb til Codex stoppet før første `git add` fordi stoppregelen sa «finner du `.git/index.lock` eller annen låsefil: stopp». Et rekursivt søk fant 25 filer som heter `locked` under andre arbeidstrær — normale `git worktree lock`-markører som ikke blokkerer noe. Jobben gjorde ingenting, og hele runden gikk tapt.
    - forebygging: Skriv stoppregler som navn og sti, ikke som kategori: «stopp hvis `index.lock`, `HEAD.lock` eller `*.lock` finnes under `<denne stien>`». Navngi eksplisitt det som ser ut som en treffer men ikke er det, og si at det skal ignoreres. Legg alltid til «stopp hvis kommandoen faktisk avvises med denne feilen» — en filsøk-treffliste er ikke et bevis på blokkering. Samme gjelder alle vide vendinger i en prompt: «eller lignende», «eller annet», «eventuelle andre».
- **lesson.ciphertext-field-held-plaintext-hash** (2026-09-10, blocker): Losen fortalte Kjetil at lyd allerede var kryptert i lagring. Det var feil: filene i prod begynner med ID3 og er vanlig MP3. To ting forte dit. (1) Krypteringskoden som ble lest tilhorer MusicIngestCell paa /mvp/ingest/local, mens Butterpop publiserer gjennom MusicAssetStoreCell.storeLocalAsset, som skriver bytene slik de kommer. (2) storeLocalAsset setter ciphertextSHA256 = plaintextSHA256 = sha256(data), saa manifestet ser kryptert ut selv naar encryptionPolicy er none.
    - forebygging: En paastand om at noe er kryptert, signert eller verifisert skal bekreftes paa artefaktet - les bytene, ikke feltet. Et felt som heter ciphertext* skal ikke settes naar encryptionPolicy er none; enten utelates det, eller navnet sier hva det er. Kan bli derivedTest: manifest med encryptionPolicy none har ingen ciphertext-verdi.
- **lesson.local-main-is-not-main** (2026-09-11, major): WP0-baselinen var rød og ble meldt som «main bygger ikke». Det var feil. Den commiten baselinen ble målt mot, `ba14895`, lå bare på den LOKALE main-grenen og var aldri pushet; den avhang av CellBase-kode som heller ikke var pushet. origin/main lå fire commits lenger fram, pinnet CellProtocol til en revisjon som ER på CellProtocol sin main, og hadde grønn CI hele tiden. Et helt døgns arbeid ble bygget oppå den lokale commiten.
    - forebygging: Før du måler en baseline eller sier at main er rød: `git fetch origin main` og sammenlign. Er lokal main foran origin/main, er de commitene ikke main for andre — bygg aldri videre på dem. Se på CI for origin/main før du konkluderer. `swift package edit` skal aldri være på når noe måles eller meldes verifisert. Og den eneste sjekken som virkelig avgjør: klon fra GitHub til en tom katalog og bygg der. HavenAgentD::Scripts/preflight_before_landing.sh stiller alle fire spørsmålene.
- **lesson.a-new-red-test-needs-a-repeated-baseline** (2026-09-10, minor): Første fulle kjøring med nye endringer viste to røde i stedet for baselinens én, og den nye lå i en fil jeg hadde endret. Det så ut som en regresjon jeg hadde innført.
    - forebygging: Når en ny rød dukker opp: kjør basen på nytt, i et eget rent worktree, **flere ganger** (tre holder som regel), før du enten tar på deg feilen eller avfeier den. Skriv resultatet av gjentakelsen i TESTRESULT — «2 av 3 på ren base» er et svar, «den er nok flaky» er ikke. Det koster ti minutter og avgjør om du bruker natten på å jage din egen feil eller andres.
- **lesson.swift-test-exit-code-lies-in-havenagentd** (2026-09-10, minor): `swift test` i HavenAgentD avslutter med 1 selv når samtlige 212 tester passerer. Et skript som leser `$?` melder rødt på et helt grønt tre.
    - forebygging: Les resultatet fra linjen `Test run with N tests in M suites passed/failed`, ikke fra exitkoden, i alle skript og køjobber for dette repoet. Og fjern det tomme XCTest-målet, eller bygg det for riktig arkitektur, før noen setter opp CI her — ellers vil CI være rød uansett hva som gjøres.
- **lesson.pkill-pattern-killed-the-queue-job** (2026-09-10, major): En commit-jobb i Losen-køen døde med EXIT=143 tolv sekunder etter start. Ingen feilmelding, ingen commit. Årsaken var min egen opprydding i et annet skript: `pkill -f "<appnavn>"`.
    - forebygging: Bruk aldri `pkill -f <mønster>` på en maskin der andre prosesser kan ha teksten i argv. Stopp en prosess ved PID du selv startet, eller ved `pgrep -x <prosessnavn>` kombinert med en sjekk av `ps -o comm=` mot den nøyaktige kjørbare stien. Dette gjelder særlig når en jobbkø kjører prompter som argument: alt du skriver i en prompt står på en kommandolinje et sted.
- **lesson.queue-job-file-before-prompt** (2026-09-10, minor): Køjobben `formaalskomposisjon-fullfor-commit-20260910-1020` ble avvist med «mangler promptfil» 13 sekunder etter at `.job` ble skrevet; promptfilen kom to sekunder etter avvisningen og ligger foreldreløs i `_losen-queue/inbox/`, der runneren aldri ser den igjen.
    - forebygging: Skriv `<id>.prompt.md` først og `<id>.job` sist, helst som `mv` fra en tmp-fil i samme mappe — `.job` er registreringssignalet, slik `job.json` er det i HavenAgentD::Docs/AgentJobs.md. Kan bli derivedTest: runneren eller `hd validate` rapporterer enhver `inbox/*.prompt.md` uten tilhørende `.job`, eldre enn to minutter, som foreldreløs.
- **lesson.pin-must-be-on-their-main** (2026-09-11, major): En revisjonspin i Package.swift pekte på en CellProtocol-revisjon som ikke lå på CellProtocol sin main. Koden bygde bare på den ene maskinen som hadde revisjonen liggende lokalt.
    - forebygging: Å pinne er riktig — det er det som gjør bygget reproduserbart. Kravet er at revisjonen er en forfar av avhengighetens egen main. Da er «bygg fra andres main» og «reproduserbart bygg» samme krav. HavenAgentD::Scripts/assert_dependencies_are_on_their_main.sh håndhever det, og CI kjører den. Lander du en klient før cellen den bruker er på den andres main, har du laget et repo som bare bygger hos deg.
- **lesson.a-red-baseline-is-a-question-not-an-answer** (2026-09-11, major): En rød baseline ble behandlet som en opplysning om prosjektet, og arbeidet gikk videre med et tiltak som gjorde den grønn. Tiltaket skjulte årsaken i stedet for å fjerne den.
    - forebygging: Svar på tre spørsmål før du gjør noe med en rød baseline: er utsjekket mitt likt origin? er CI grønn på origin/main? hvilken commit gjorde den rød, og hvem eier den? Først når svaret er «prosjektet er faktisk rødt» er det riktig å jobbe rundt det — og da som en egen, navngitt sak, ikke som en stille lokal omgåelse.
- **lesson.a-conditional-artifact-must-still-cost-something** (2026-09-18, minor): purpose_dev.py validate ble rød på PDD_entitetsdata-egen-kontroll fordi artefaktet 'skeleton/' manglet, selv om G1-GUI var godkjent på bilder Kjetil faktisk hadde sett. Pakken beskrev artefaktet som påkrevd «når Porthole-preview er brukt»; validatoren krevde det alltid.
    - forebygging: Et betinget krav oppfylles av et *annet krav*, aldri av et fravær. Feltet 'satisfiedByDeclaration' peker på en fil og en overskrift og krever minst ett punkt under den: enten viser du skjelett-JSON-en bildet er rendret fra, eller du skriver ned hva skjelettet ikke kan rendre. Begge tvinger frem spørsmålet «kan flaten dette?». Feilmeldingen navngir begge veier ut. Sjekket begge veier: rød uten erklæring, grønn med.
- **lesson.location-is-not-ownership** (2026-09-22, major): dataflow.md begrunnet at AIGateway matte ligge i appen med at «en gateway utenfor entiteten gjor prompten til noen andres data». Kjetil: en celle i skyen som eies av meg er pr definisjon innenfor min entitet.
    - forebygging: Regelen er uniform og gjelder alle scaffolds likt: ingen andre, scaffold-admin inkludert, nar data ELLER funksjonalitet i en celle jeg eier uten en Agreement som sier det. Et vern som bare gjelder skyen er et tegn pa at grensen er tegnet feil. Negative tester skal kjores i begge oppsett, lokalt og sky, og gi samme svar — og de skal dekke handlinger, ikke bare felter. Den positive motsatsen ma ogsa testes: en Agreement apner nayktig sitt eget omfang.
- **lesson.read-origin-main-before-writing-a-mechanism** (2026-09-22, major): Runde 1 av PDD_entitetsdata skrev en egen resolver for lenkede identiteter (EntityLinkAuthorizer, ny CellAuthorizationPath.linkedIdentity, ny hook pa GeneralCell). Da patchen ble lagt mot origin/main viste det seg at IdentityLinkRegistry og GeneralCell.authorizationEvidence allerede gjorde det samme, landet av en annen oppgave (purpose://candidate.entity-link.resolver-honours-link). Hele resolveren ble forkastet.
    - forebygging: Brief-audit skal si HVILKEN revisjon noe ble lest fra, og for et formal som skal endre en mekanisme skal kilden vaere origin/main (git show origin/main:<fil>), ikke utsjekket. Preflight-skriptet sjekker na at patchen passer mot origin/main i et eget worktree for noe legges pa. Og: for du skriver en mekanisme, grep pa main etter navnet pa det den skal gjore (her: sameEntity, linkedIdentity) - ikke bare etter typen du planlegger a lage.
- **lesson.method-lived-only-on-one-machine** (2026-09-24, major): Metoden selv — Book 35 (PDD-arbeidsflyten), Book 36, lærdomsregisteret med 50 lærdommer, formålspakkene, purpose_dev.py — lå bare i ett utsjekk på Kjetils Mac på grenen codex/docs-cleanup-20260810, aldri på main; derfor verken i HAVEN eller hos andre utviklere.
    - forebygging: Metodeartefakter landes som kode: PR til main og pin-oppdatering i HAVEN. Test: git cat-file -e origin/main:<fil> for hver metodefil.
- **lesson.readonly-git-is-not-all-git** (2026-09-24, minor): Et `git status` fra device_bash i CellProtocolDocuments etterlot .git/index.lock (0 byte) som ikke kunne fjernes fra VM-en, selv om git show/grep/log/rev-parse i samme økt ikke gjorde det.
    - forebygging: Fra device_bash bare objektlesende git mot en revisjon (git show/grep/log/cat-file <rev>); aldri status, diff mot arbeidstreet, add eller commit. Finnes en lås likevel: flytt den til _to_delete/ (mv virker, rm gjør ikke).
- **lesson.downstream-pin-must-come-from-the-consumer** (2026-09-24, major): Nedstrøms-baselinen for CellScaffold var rød 22.09 («cellprotocol krever swift-crypto 4.5.2, dimymint krever 3.x») og ble rapportert som prosjektets blokkering. CellScaffold main pinnet DiMyMint af41630, som løser swift-crypto 4.x; skriptet hadde hardkodet en eldre revisjon (1718fda).
    - forebygging: Et nedstrøms-skript leser alle transitive pinner fra forbrukerens egen Package.swift/Package.resolved på origin/main ved kjøring, og logger dem. En rød avhengighetsoppløsning i et skript med hardkodede pinner er ikke et funn før pinnene er bekreftet mot forbrukerens resolved.
- **lesson.disposable-worktree-must-be-reset-before-checkout** (2026-09-24, minor): pdd-check/Binding ble stående på 72f6a6c9 i to kjøringer selv om skriptet ba om origin/main: «Your local changes to project.pbxproj would be overwritten by checkout». Baselinen målte feil Binding-revisjon uten å si fra.
    - forebygging: Engangs-worktrees resettes hardt (`git reset --hard` + fjern Package.resolved) før hver utsjekk, og skriptet skriver ut revisjonen den faktisk står på — en avvikende revisjon skal stoppe kjøringen, ikke logges forbi.
- **lesson.report-the-commit-you-pushed-not-the-one-you-planned** (2026-09-24, minor): TESTRESULT og PLAN sa «commit ebb0b7f». Branchen sto på e66b7f1 — commit.sh hadde laget en ny hash — og var ikke pushet. Push-skriptets EXPECT måtte rettes før det kunne kjøre.
    - forebygging: Etter hver commit/push: les `git rev-parse --short HEAD` og `git ls-remote --heads origin <branch>` og lim inn utdataene i STATUS/TESTRESULT. Sjekk også for remote-tracking ref før du sier «pushet» (lesson.branch-is-empty-after-eight-work-packages, samme familie).
- **lesson.lookup-again-when-a-surface-is-added** (2026-09-24, major): De nye seksjonene i «Utvid entiteten» (B10) var portet på synlighet med rot-scope, og listen med verktøyets forespørsel forsvant — samme feil som lesson.unresolvable-condition-is-invisible fra 05.09.
    - forebygging: For hver ny eller endret skjelettflate: kjør `purpose_dev.py lookup --tags skeleton gui` før utformingen, og `BindingTests/CellConfigurationVerifierXCTest/testNoLocalSurfaceHidesItsOwnWaysIn` + `testPersonalCopilotLocalSurfacesLoadWithoutReferenceFailures` før flaten vises eller committes.
- **lesson.picker-state-keypath-is-read-and-written** (2026-09-24, minor): Velgeren «Verktøy» i «Gi tilgang» sto på «Velg verktøy» selv om cellen hadde valgt verktøyet.
    - forebygging: `selectionStateKeypath` skal være en nøkkel cellen både leser (`{selected}`) og skriver; test rundturen (`pickerSelectionRoundTrips`).
- **lesson.pairing-can-outlive-the-identity** (2026-09-24, major): Agenten var paret med en HAVEN-identitet fra 4. mai («Binding Local Session», nøkkel 13BF…), mens HAVEN brukte en annen privat identitet (D362…, identitetsfilen skrevet 18.09). Svar fra HAVEN ville blitt avvist; ingen test i noen av endene kunne se det.
    - forebygging: En flate som ber eieren signere for agenten sammenligner egen nøkkel med agentens forankring og viser forskjellen før signering, med vei til ny paring (test: `offerIsRefusedHereWhenThisHavenHoldsAnotherKey`, `theOwnerNeverSignsWhatFailedTheCheck`). Sjekk nøkkelkontinuitet før live-test av noe som signeres.
- **lesson.jxa-objc-method-without-arguments-is-a-property** (2026-09-24, minor): `a.terminate()` i JXA ga `TypeError: a.terminate is not a function`, men appene avsluttet likevel.
    - forebygging: Skriv `a.terminate` (uten parentes) og sjekk etterpå med `pgrep` at prosessen er borte før du går videre.
- **lesson.screencapture-from-runner-can-fail** (2026-09-24, minor): `screencapture -l <vindu>` fra jobbløperen ga «could not create image from window» for HAVEN-vinduet, med samme vindus-ID som computer use så.
    - forebygging: Ta bilder av flater med computer use (eller be Kjetil), og ikke planlegg bevis som avhenger av `screencapture` fra løperen før det er målt at det virker den dagen.
- **lesson.pgrep-pattern-must-allow-arguments** (2026-09-25, minor): Byggejobben avsluttet ikke HAVEN, og `open` hentet bare fram det gamle bygget (startet 24.09 17:29) i stedet for å starte det nye.
    - forebygging: Bruk 'HAVEN( |$)' i mønsteret, og skriv ut prosessens starttid etter omstart og sammenlign den med byggetiden før noe vises fram.
- **lesson.computer-use-image-is-not-a-file** (2026-09-25, minor): Skjermbildene av den nye flaten kunne ikke sendes til Kjetil som fil; vinduet var i tillegg på et annet skrivebord og kunne ikke gjøres større i bakgrunnen.
    - forebygging: Planlegg bildebeviset med en vei som gir en fil (Kjetils eget skjermbilde, eller skjermopptakstilgang for løperen), og si det før arbeidet, ikke etter.
- **lesson.green-gate-must-read-the-last-summary-line** (2026-09-26, major): runde2.sh committet og pushet 399f6d2 med 4 røde tester. Porten grep'et «Executed … with 0 failures» i hele loggen og traff en grønn suites linje lenger opp; siste linje sa «1262 tests, with 2 tests skipped and 8 failures».
    - forebygging: En grønn-port leser bare den siste «Executed»-linjen (tail -1) og krever « 0 failures (0 unexpected)». Sammenligningen gjøres uten pipe (POSIX case), fordi `echo | grep -q` under pipefail kan gi rødt på grønt (SIGPIPE). Porten skriver ut nøyaktig hva den sammenlignet.
- **lesson.module-and-type-share-a-name-in-cellprotocol** (2026-09-26, minor): `CellApple.EntityAnchorCell` og `CellVapor.EntityAnchorCell` kompilerte ikke: «type 'CellApple' has no member 'EntityAnchorCell'». Begge modulene har en type med samme navn som modulen.
    - forebygging: Én fil per modul som importerer bare den ene og gir typen et unikt typealias (TestSupport/AppleEntityAnchorAlias.swift, VaporEntityAnchorAlias.swift). Testfilen importerer ingen av modulene direkte.
- **lesson.host-mutation-without-reading-the-coordination-file** (2026-10-02, major): 30.09 satte en Claude-tråd ut en gren-commit på staging og byttet invitasjonene, med Kjetils ja, men uten claim. En Codex-tråd hadde claim på samme container (HD-0141), staging var reservert for 2026.9.4, og deploykøen trodde i to døgn at staging kjørte forrige utgivelse.
    - forebygging: Før enhver vertsmutasjon: les `_losen-queue/KOORDINERING.md`, kjør `hd coord status`, ta egen claim på en HD-oppgave, og før utsettingen inn i køen etterpå. Test: jobbloggen for utsettingen viser `hd coord status` uten annen claim på samme tjeneste, og egen claim, før første kommando mot verten. Eierens ja til å sette ut erstatter ikke sjekken.
- **lesson.remembered-install-state-is-not-measured** (2026-10-02, minor): En plan sa at agenten på Macen var bygget fra en bestemt gren, og bygde grenvalg og et åpent spørsmål til eieren på det. Agenten var installert på nytt fra `main` av en annen tråd seks dager tidligere.
    - forebygging: Hva som er installert, måles før en plan bygger på det: dato og navn på binærene og sikkerhetskopiene i `bin/`, `launchctl print`, og om commiten er på `origin/main`. Test: påstandstabellen merker installasjonstilstand som hentet med måletidspunkt, aldri som husket.
- **lesson.md5-differs-for-images-written-from-the-cloud** (2026-10-02, minor): Etter at seks PNG-filer ble skrevet fra en Cowork-økt til Macen, stemte ikke md5 mot originalene, mens alle tekstfilene stemte. Det så ut som feilen der en gammel utgave blir skrevet.
    - forebygging: Kontroller tekstfiler med md5. Kontroller bilder ved å sammenligne `IDAT`-dataene eller størrelsen minus `caBX`-blokken, ikke md5 av hele fila. Test: kontrollskriptet for overførte filer skiller de to tilfellene.

## Book 23-noder som kan være forelder/gjenbruk (leksikalsk forslag, verifiser)
- purpose://grounding.local-model-assisted-decomposition [active] — Local model assisted decomposition

### Hva som gjelder denne oppgaven

Ikke relevant, og hvorfor:

- `pkg.std.cell-contract`: ingen cellekontrakt endres. Svaret har samme felt som før, og
  `route` har de samme to verdiene. De negative autorisasjonstestene kjøres likevel, som
  del av hele testmengden.
- `pkg.std.cell-combination`: ingen ny kant i dataflyten. `dataflow.md` viser de to
  punktene som endres: hva som sendes til modellen, og vakten etterpå.

Lærdommene som styrer denne oppgaven:

- `lesson.plan-instead-of-delivery`: etter G2 teller bare radene i §3.
- `lesson.dev-set-called-holdout` og `lesson.same-writers-holdout-overstates`: eksemplene
  jeg skriver selv, er et utviklingssett. Tallet som rapporteres, kommer fra en tråd som
  ikke har skrevet reglene, målt én gang etter at reglene er frosset.
- `lesson.tested-a-different-path-than-production`: testene kaller vaktens egen funksjon
  og conciergens egen vei, og målingen går mot nett.
- `lesson.baseline-count-from-report-not-run`: testmengden er kjørt før endringen (227,
  kl. 18:33 UTC), og kjøres på nytt etter.
- `lesson.host-mutation-without-reading-the-coordination-file`: deployen leser
  `_losen-queue/KOORDINERING.md`, kjører `hd coord status` og tar egen claim før verten røres.
- `lesson.branch-is-empty-after-eight-work-packages`: commit etter første grønne kjøring.
- `lesson.mount-is-not-git` og `lesson.paste-command-instead-of-queue`: all git og alle
  bygg går gjennom køen.

Egen lærdom fra i dag, som denne spesifikasjonen selv brøt i første utkast: seks kall med
ett og samme godkjente svar ble til «vakten forkaster alt». Et mål som bare har sett én
slags svar, sier ingenting om de andre. F6 måler derfor tre ulike godkjente svar.

## 5. Avledede tester (samlet)

| testRef | Formål | Hvordan | Evidens | Status |
|---|---|---|---|---|
| test.build | `purpose://quality.build-and-regression` | `swift build` gjennom køen (`HD/mac/cp-pin-verifiser-og-test-20260929.sh`) | `TESTRESULT.md#build` | venter |
| test.regression | `purpose://quality.build-and-regression` | `swift test`, hele mengden, før og etter. Antall før (227) og etter føres opp. Ingen test fjernet eller svekket | `TESTRESULT.md#regression` | før: grønn 18:33 UTC |
| test.vakt.innhold-uendret | F1 | XCTest, skal forkastes: beskrivelsen uten «mandler»; «Pane di campagna, focaccia e olio» delt med komma; «18» flyttet inn i listen; «Pizza Tartufo, Pizza Umami»; en rett tatt ut av de 18; et tegn som ikke er bokstav, tall eller vanlig tegnsetting | `TESTRESULT.md#innhold` | venter |
| test.vakt.trofast-godtas | F1, F2 | XCTest, skal godtas: «Vi har følgende pizzaer: …» (publisert 12:56 UTC) og «Vitello tonnato serveres som tynne skiver …» (publisert 18:35 UTC), begge ordrett | `TESTRESULT.md#trofast` | venter |
| test.vakt.ramme | F2 | XCTest, skal forkastes foran listen: «bare disse», «blant annet», «mange flere», «var», «ikke», «på tilbud», «Du har rett.», et spørsmålstegn, et tallord som ikke sto der | `TESTRESULT.md#ramme` | venter |
| test.vakt.sendes-ikke | F3 | XCTest: bestillingssvaret, et svar med «ikke», et med «må», og et med to retter gir null kall til stubben og uendret tekst | `TESTRESULT.md#sendes-ikke` | venter |
| test.vakt.publiserte-feil | F4 | XCTest: de fire svarene fra 2. oktober kl. 12:56 og setningen fra 1. oktober forkastes | `TESTRESULT.md#publiserte` | venter |
| test.vakt.roed-foerst | F4 | Kjøring: de nye «skal forkastes»-testene mot dagens vakt, før koden endres. Forventet: røde | `HD/maal/PINTEST-RUNDE2-ROED-<dato>.md`, `TESTRESULT.md#roed` | venter |
| test.vakt.uavhengig-forslag | F5 | Gjennomgang av forslaget før kode. Utført 2. oktober kl. 18:35–18:53 UTC: ni mekanismer i dagens vakt, sju som forslaget ikke stoppet | `HD/maal/VAKT-UAVHENGIG-FORSLAG-20261002.md` | utført |
| test.vakt.uavhengig-kode | F5 | Måling: en ny tråd får koden og skriver omskrivinger for å slippe gjennom og endre meningen. Hver kjøres gjennom vakten. Null godtas. Funn blir tester, og et nytt sett måles én gang etter frysing | `HD/maal/VAKT-UAVHENGIG-KODE-<dato>.md`, `TESTRESULT.md#uavhengig` | venter |
| test.vakt.grunn | F7 | XCTest: hvert utfall (publisert, forkastet med regel, ingen tekst) gir en navngitt grunn. Grunnen inneholder ikke spørsmålet | `TESTRESULT.md#grunn` | venter |
| test.commit.bare-mine-filer | `purpose://quality.build-and-regression` | Inspeksjon: commit-rapporten lister nøyaktig filene jeg har navngitt. `Deliverables/` og `Sites/` er urørt | `TESTRESULT.md#commit` | venter |
| test.deploy.claim-foer-vert | F6 | Inspeksjon: deploy-loggen viser `hd coord status` og egen claim før første kommando mot verten, og at nginx ikke ble rørt | `TESTRESULT.md#deploy` | venter |
| test.live.modellen-syns | F6 | Måling: fire kall hver på «Hvilke pizzaer har dere?», «Hva har dere på menyen?» og «Fortell om Vitello tonnato.» Minst seks er `route: model` med annen ordlyd. Skriptet kontrollerer at innholdet står uendret; jeg leser hvert svar | `HD/maal/SPOER-RUNDE2-<dato>.md`, `ACCEPT.md#live` | venter |
| test.live.grunn-i-loggen | F7 | Måling: utdrag fra containerens logg for de tolv kallene, lest på verten av ops | `HD/maal/VAKTLOGG-RUNDE2-<dato>.md`, `ACCEPT.md#logg` | venter |
| test.docs-updated | `purpose://quality.docs-in-same-change` | Inspeksjon: `HD/README.md`, kommentarene i koden og instruksen til modellen sier det samme som vakten gjør | `ACCEPT.md#docs` | venter |
| test.status-current | `purpose://quality.work-is-visible` | Inspeksjon: `STATUS.md` mot filene i mappen | `ACCEPT.md#status` | venter |
| test.cells.capability-audit | `purpose://cells.capabilities-declared-with-boundary` | Tabellene i §0 og §2 | `FORMAALSSPEC.md#audit` | venter |
| test.cells.dataflow-matches-contracts | `purpose://cells.dataflow-declared` | `dataflow.md` med de to punktene som endres | `PLAN.md#dataflow` | venter |
| test.cell.contract-fixtures, test.cell.auth-negative, test.cell.stub-scan | `pkg.std.cell-contract` | Ikke relevant: ingen kontrakt, autorisasjonsvei eller stubb endres | – | ikke relevant |
| test.handoff.dry-run | `purpose://handoff.runnable-without-guessing` | Skriptene i `HD/mac/` har ikke tørrkjøring. Rekkefølge og forventet utfall står i `HD/README.md` | `TESTRESULT.md#dry-run` | blocked: skriptene mangler `--dry-run`. Kjent hull, ikke rettet i denne runden |

## 6. Åpne spørsmål til Kjetil

1. **G1: er formålene i §1 og kontrakten i §3 det du vil ha?** Regelen er en annen enn den
   jeg beskrev da du valgte: «innholdet uendret, modellen skriver ordene rundt» i stedet
   for «samme ord, tåle bøyning». Målet er det samme: modellen syns, og vakten er strengere
   der den i dag er for slapp.
2. **Får modellen si «Vi har …»?** Det godkjente svaret sier «Pizzaene i
   kunnskapsgrunnlaget er: …». Modellens naturlige setning er «Vi har følgende pizzaer: …».
   Gjennomgangen peker på at det er en sterkere påstand: «vi har» mot «står i
   kunnskapsgrunnlaget». 2. oktober regnet jeg selv den setningen som trofast. Under hvert
   svar på siden står: «Svaret bygger på et datert kunnskapsgrunnlag. Dagens meny, priser
   og tilgjengelighet må bekreftes av Palazzo.»
   - **Ja (anbefalt):** «Vi har følgende pizzaer: …». Det en kelner ville sagt. Setningen
     legger ikke til en opplysning, og forbeholdet står i advarselen under svaret.
   - **Nei:** forbeholdet skal stå i setningen: «Dette er pizzaene i kunnskapsgrunnlaget:
     …». Modellen syns da bare i småord.
3. **Planen (G2).** Du kan si «auto», be om å se planen først, eller la meg bygge og teste
   i kveld og vente med deployen til du har sett resultatet.

Trenger ikke svar nå: **fritekstsvar uten kolon.** De finnes ikke på nett i dag, men
testene bruker ett («Vi har fem pizzaer på menyen. Margherita er den enkleste av dem.»), og
to av dem forventer at det omformuleres. Der kan en ordvakt ikke gi full garanti. Jeg lar
testene stå, strammer listen over frie ord, og fører grensen opp i `ACCEPT.md`. Vil du
heller at slike svar aldri sendes til modellen, må de to testene endres. Det gjør jeg bare
på ditt ord.

Én ting du bør vite før du svarer: med denne regelen er modellens bidrag en setning foran
listen eller et bindeledd etter et navn. Gjennomgangen spør om tre–fire setninger du selv
har godkjent, ville gjort samme nytte uten modell. Det er alternativ 3 fra forrige runde i
ny form. Jeg bygger det du valgte, og målingen mot nett viser hvor mye modellen faktisk
varierer, så du kan se det selv.

## 7. Revisjonslogg

| Iterasjon | Dato | Hva endret seg | Hvem |
|---|---|---|---|
| 0 | 2026-10-02 | Opprettet | Losen |
| 1 | 2026-10-02 | §0–§6 skrevet uten tilgang til Mac-en (kl. 18:18 UTC). Ikke sendt | Losen |
| 2 | 2026-10-02 | Skrevet om etter to prøver mot nett (kl. 18:32 og 18:35 UTC), ny lesing av vakten og malene, og en uavhengig gjennomgang (kl. 18:35–18:53 UTC). «Vakten forkaster alt» rettet. Regelen endret fra «samme ord, tåle bøyning» til «innholdet uendret, modellen skriver ordene rundt». Formålene gikk fra seks til sju: F1–F3 er nye i innhold, F7 (grunn i loggen) er ny. Sendt til Kjetil for G1 | Losen |
