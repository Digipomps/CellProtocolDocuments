# Trinn 1 og 2: korrespondansevakten

Ett program, to oppgaver. `korrespondanse_vakt.py sjekk` ser etter ulest post. `korrespondanse_vakt.py frist` ser etter tilganger som snart går ut. Planleggeren som kjører i dag, starter dem som to faste programmer i policyen. Ingen ny agent trengs.

Ett program i stedet for to gir én fil og én sjekksum å kontrollere. `PLAN.md` runde 3 hadde to filer; det er endret her og i planen.

## Hvor ting ligger

| Hva | Sti |
|---|---|
| Kilden | `Scripts/scheduled/korrespondanse_vakt.py` i HavenAgentD |
| Installasjonen | `Scripts/install-scheduled-tasks.sh`, som starter `Scripts/scheduled/installer.py` |
| Installert | `~/Library/Application Support/HAVENAgent/bin/korrespondanse_vakt.py` |
| Markørene | `~/Library/Application Support/HAVENAgent/Inbox/CorrespondenceWaiting/` |
| Stempel og lås | `~/Library/Application Support/HAVENAgent/State/ScheduledTasks/` |
| Korrespondanseklienten | `~/Library/Application Support/HAVEN/AssistantCorrespondence/bin/haven-correspondence-mcp` |
| Klientens rot, med profilene | `~/Library/Application Support/HAVEN/AssistantCorrespondence/` (`<profil>/profile.json`) |

Alle stier gis som argumenter og må være absolutte, så policy-linjen viser nøyaktig hva programmet rører. Klienten får roten sin med `--root`, så den heller ikke leter selv. Programmet bruker ikke `HOME`, `PATH` eller gjeldende mappe. Det krever Python 3.9 og bare standardbiblioteket. At `/usr/bin/python3` på Macen er 3.9 eller nyere, måles av installasjonsskriptet før noe legges inn.

## Kravene som gjelder begge oppgavene

Planleggeren som kjører i dag, har ingen tidsgrense, leser utdata først når programmet er ferdig, og kjører én ting om gangen (`ScheduledEventService.swift` linje 224–226 og 238, `SubprocessRunner.swift` linje 61–63). Et program som henger, stanser derfor alt. Programmet må selv sørge for at det ikke skjer.

| Krav | Hvordan |
|---|---|
| Ferdig på 60 sekunder | `signal.alarm(55)` med en behandler som kaster et unntak. Hovedløpet fanger det, regner profilene som ikke ble ferdige som feilet, beholder en lesing som alt var ferdig, og skriver markører og stempel som vanlig. Alarmen slås av når lesingene er over, så den aldri avbryter skrivingen. En vakttråd slår inn etter 60 sekunder uansett: den dreper klientens prosessgruppe, skriver stempelet med kode 3, og kaller så `os._exit(3)`. En siste tidtaker avslutter prosessen fem sekunder senere uten å røre noe, i tilfelle vakttråden selv står fast. Har hovedløpet skrevet linjene sine når vakttråden kommer, rører vakttråden ingenting. |
| Henger ikke på barneprosesser | Klienten startes med egne rør og i egen prosessgruppe (`start_new_session=True`). Gruppen får SIGTERM og så SIGKILL i `finally`. Klientens stderr går til en midlertidig fil i tilstandsmappen, ikke til et rør. De siste 2000 tegnene leses, også når klienten ikke svarte i tide, og fila fjernes; teksten havner bare i stempelet. |
| Lite utdata | Nøyaktig én linje på stdout, og høyst én på stderr, begge under 4 KiB. Mer enn rørbufferen ville hengt planleggeren. |
| Lar seg stoppe, og stopper ordnet | Planleggeren overser SIGTERM og SIGINT i sin egen prosess, og det arves av programmene den starter. Programmet tar derfor over SIGTERM så lenge en kjøring varer: ved SIGTERM dreper det klienten, slipper låsen, skriver én linje på stderr og avslutter med kode 143, uten å røre stempel eller markører. Klienten det starter, får dermed vanlig behandling av SIGTERM. SIGINT behandles likt når det ikke er oversett; et SIGINT som er arvet som oversett, blir stående slik, så en planlegger som får Ctrl-C i en terminal, lar kjøringen bli ferdig. SIGHUP røres ikke. Var SIGTERM arvet som oversett, står «startet med SIGTERM oversett» i stempelets `note`, så det kan leses av på Macen hva planleggeren gir videre. |
| Ingen dialoger | Ingen kall som kan åpne et vindu. Klienten kjøres bare med `serve`. |
| To kjøringer går ikke samtidig | Låsfila `<tilstand>/<oppgave>.lock`, opprettet med `O_EXCL`, med pid og tidspunkt. En lås eldre enn ti minutter regnes som forlatt og byttes. Er låsen tatt, skriver programmet «`<oppgave>`: kjører allerede», avslutter med kode 0, og rører verken markører eller stempel. |
| Markører byttes på plass | Nye og endrede markører skrives før gamle fjernes. Skriv til `.<id>.tmp-<pid>-<tråd>` i markørmappen og `os.replace` til `<id>.json`. En midlertidig fil som blir liggende fordi en kjøring døde midt i en skriving, fjernes av en senere kjøring når den er ti minutter gammel. Agenten hopper over skjulte filer og filer som ikke ender på `.json` (`CorrespondenceWaiting.swift` linje 152 og 156). |
| Rører bare sine egne markører | En markør endres eller fjernes bare når `markedBy` er oppgavens eget navn. Finnes en fil med samme navn og annen `markedBy`, skrives ingenting, og kjøringen regnes som feilet. |
| Teksten er trygg | `from` og `summary` kontrolleres mot samme regel som agenten bruker (se under) før de skrives. |
| Etterlater et stempel | `<tilstand>/<oppgave>.stamp.json`, etter `scheduled-task-stamp-v1.schema.json`. `firstRunAt` og `runCount` føres videre fra forrige stempel. |

Avslutningskoder: 0 når alt ble lest, 1 når noe ikke kunne leses (markører og stempel er likevel skrevet), 2 ved feil i argumentene, 3 når vakttråden slo inn, og 143 eller 130 når kjøringen ble stoppet med SIGTERM eller SIGINT (da skrives ikke stempel). Slår vakttråden inn, er det den som avslutter: hovedløpet skriver da verken stempel, markører eller utdata.

Feil i argumentene er også: et profilnavn som ikke følger `[A-Za-z0-9][A-Za-z0-9._-]{0,35}` (høyst 36 tegn, så «tilgangsfristen for `<profil>`» får plass i avsenderfeltet), eller som likner en ID; et visningsnavn i `--navn` som er over 56 tegn eller likner en ID; samme profil to ganger; og en sti som ikke er absolutt. Da kan ingen tekst programmet lager fra argumentene, bli avvist av agenten. Planleggeren legger koden, hele kommandolinjen og stderr-linjen i `lastError` i `State/scheduled-events.json`, og går videre uansett.

Stdout-linjen havner i `lastOutput`, og fra trinn 5 i lista «Planlagte jobber». Formen er fast: «korrespondanse-sjekk: 2 profiler lest, 1 avsender med ulest post» eller «korrespondanse-frist: 2 profiler lest, nærmeste frist om 27 dager». Ble ikke alt lest, står det «1 av 2 profiler lest». Ingen navn, ingen ID-er. Stderr-linjen navngir profilen og den faste grunnen: «korrespondanse-sjekk: kjetil-d ble ikke lest (klienten svarte ikke i tide)».

### Tidspunkter

Klienten og profilene skriver tid som `2026-10-01T00:02:36.280Z`. Python 3.9 sin `fromisoformat` leser ikke det. Programmet tolker derfor formen `ÅÅÅÅ-MM-DDTtt:mm:ss`, med eller uten desimaler, og med `Z` til slutt, og skriver alltid `2026-10-01T00:02:36Z`. Tekst til mennesker («2.10. kl. 02:02») er i Macens egen tidssone. Årstall utenfor 2000–2999 regnes som et tidspunkt som ikke kan tolkes: i `createdAt` føres det bare i stempelet, i `expiresAt` gir det `frist-feilet-<profil>`.

### Regelen for trygg tekst

Portert fra `AgentChallengeTextSafety.looksLikeSecret` (`AgentChallenge.swift` linje 178–208). Teksten deles på mellomrom, linjeskift og tabulator. Tegnene `.,;:()[]{}«»"'` fjernes fra endene av hvert ord. Et ord er utrygt når det har minst 24 tegn, bare består av `A–Z`, `a–z`, `0–9`, `_` og `-`, og enten har både bokstav og siffer, eller er minst 32 tegn rene heksadesimale tegn. Tekst som inneholder `-----BEGIN`, er alltid utrygg.

Er `from` utrygg eller lengre enn 56 tegn, skrives «en ukjent avsender». Grensen på 56 er kontraktens egen: da får hele tittelen plass på 80 tegn. Er `summary` utrygg, skrives den faste teksten for markørtypen uten de variable delene. `fixtures/ugyldig-tekst.json` har tilfellene testen skal dekke.

Meldingens emne og innhold tas aldri med, og heller ikke enhets-ID, meldings-ID eller rå feiltekst fra klienten.

## `sjekk`: ulest post

```
korrespondanse_vakt.py sjekk
    --profil NAVN                 (én eller flere)
    --navn PRINCIPAL=VISNINGSNAVN (null eller flere)
    --klient STI  --klientrot STI  --markorer STI  --tilstand STI
    [--frist-maks-timer 48]
```

Profilene tas i en rekkefølge som flyttes ett hakk for hver kjøring (`runCount` i stempelet), så den samme profilen ikke alltid kommer sist. Tidsbudsjettet er 50 sekunder delt på antall profiler, og høyst 25 per profil. Hvert forsøk får høyst 12 sekunder, og aldri mer enn det som er igjen av profilens tid. Flere enn fire profiler avvises som feil i argumentene (kode 2): da ville ingen profil fått tid til et helt forsøk.

For hver profil:

1. Start `<klient> serve --profile <profil> --root <klientrot>`. Protokollen er JSON-RPC 2.0 med én melding per linje.
2. Send `initialize`, så `notifications/initialized`, så `tools/list`.
3. Finn verktøyet som heter `correspondence_list_inbox` eller `correspondence.list_inbox`. Klienten har en annen kontrakt enn ventet når `tools/list` gir feil eller tom liste, når verktøyet mangler, eller når verktøyets `inputSchema.required` finnes og ikke er tom (den nye klienten på `main` krever `relationshipID`). Da leses ingenting.
4. Kall verktøyet med `afterSequence: 0` og `limit: 100`. Svaret er JSON i `result.content[0].text`. Neste side hentes med `afterSequence` lik den største `sequence` på siden. Blaingen stopper når en side er tom, ikke når den er kort: tjeneren kan gi færre meldinger per side enn det ble bedt om, og da ville de nyeste, de som oftest er uleste, aldri blitt sett. Etter 20 sider regnes profilen som feilet.
5. En melding er ulest når `acknowledgedAt` mangler eller er `null`. Tell per `senderID`, og husk den eldste `createdAt`.
6. Lukk klientens stdin, vent to sekunder, og drep prosessgruppen. Etter et forsøk som feilet, ventes det ikke: gruppen drepes straks, så ventetiden ikke går av tiden til neste forsøk.

Et `createdAt` som ikke kan tolkes, stopper ikke lesingen. Programmet bruker da kjøringens eget tidspunkt for den meldingen, og fører antallet i stempelet.

Feiler et forsøk, prøves profilen én gang til etter tre sekunder når grunnen er «klienten svarte ikke i tide», «klienten meldte feil» eller «svaret kunne ikke leses», og det er minst åtte sekunder igjen av profilens tid. Det dekker sekundene etter at Macen har våknet. De andre grunnene gir ikke nytt forsøk.

### Markører

| Markør | Når | `id` | `from` | `summary` |
|---|---|---|---|---|
| Ulest post | En avsender har minst én ulest melding i en profil som ble lest | `ulest-<profil>-<avsender>` | visningsnavnet fra `--navn`, ellers «en ukjent avsender» | «1 ulest melding, fra 2.10. kl. 02:02.» eller «3 uleste meldinger. Den eldste er fra 2.10. kl. 02:02.» |
| Sjekken feilet | Profilen kunne ikke leses i to kjøringer på rad | `sjekk-feilet-<profil>` | «sjekken av `<profil>`» | «Innboksen for `<profil>` kunne ikke leses to ganger på rad. Grunn: `<fast grunn>`. Ulest post kan ligge der uten å vises.» |
| Fristvarselet står | Se regelen under | `sjekk-stoppet-korrespondanse-frist` | «fristvarselet (det har stoppet)» | «Fristvarselet har ikke kjørt siden 30.9. kl. 09:00. Planleggeren kan stå.» |

`profile` er profilnavnet. `markedAt` er den eldste uleste meldingens `createdAt`. For de to andre markørene er det tidspunktet tilstanden først ble sett. `markedBy` er `agent-korrespondansesjekk`. `<avsender>` er `senderID` der alt utenom `A–Z a–z 0–9 . _ -` er byttet med `_`. Blir id-en lengre enn 120 tegn, kuttes den der.

De faste grunnene er: «klienten startet ikke», «klienten svarte ikke i tide», «klienten har en annen kontrakt enn ventet», «klienten meldte feil», «svaret kunne ikke leses», «innboksen har for mange sider». En klient som avslutter før den har svart på noe, er «klienten startet ikke»; avslutter den senere, er det «klienten meldte feil». Den rå feilteksten legges i stempelet, avkortet til 500 tegn. Der kan den leses, men den vises aldri.

Når markørene fjernes:

- **Ulest post:** når avsenderen ikke lenger har ulest post **og profilen ble lest**. Ble profilen ikke lest, står markørene som de var: ukjent er ikke null.
- **Sjekken feilet:** første gang profilen leses igjen.
- **Profiler som er tatt ut:** oppgavens egne markører med en `profile` som ikke lenger står i `--profil`, fjernes ved hver kjøring.

**Fristvarselet står.** Markøren skrives når alt dette holder: sjekkens eget forrige stempel er ferskere enn 60 minutter (Macen har vært våken, og planleggeren går), og fristvarselets stempel er eldre enn 48 timer, eller det mangler og sjekkens første kjøring er mer enn 48 timer gammel. Markøren fjernes når fristvarselets stempel igjen er ferskere enn 48 timer. Ellers står den som den var. Har fristvarselet aldri kjørt, sier teksten «Fristvarselet har ikke kjørt siden det ble lagt inn.» Uten kravet til eget stempel ville markøren kommet hver gang Macen hadde vært av i to døgn, sekunder før fristvarselet kjørte. Søskenvakten tas ut av programmet når trinn 4 er installert, for da viser agenten selv «Planleggeren går ikke».

### Hva saken blir i menyen

Agenten som kjører, lager tittelen selv: «Post fra `<from>` venter på svar», avkortet til 80 tegn (`CorrespondenceWaiting.swift` linje 105–110). Undertittelen er `<from> · correspondence · <profil>`. Knappene er «Åpne» og «Ignorer i dag».

- «Åpne» i menyen åpner adminvinduet, der `summary` står (`HavenAgentMenuApp.swift` linje 85–86). Fra et varsel og inne i adminvinduet åpner knappen ingenting; den viser linjen «Denne skrives i samtalen med Losen» (`ChallengeOpenPlan.swift` linje 47–48).
- «Ignorer i dag» demper varselet ut dagen. Saken står.
- En ny sak varsles én gang. Kommer det mer post fra samme avsender mens saken står, endres teksten, men det kommer ikke nytt varsel. Kommer det mer enn tre nye saker på én gang, samles de i ett varsel (`NotificationDecider.swift` linje 72–91).

Tittelformen kan ikke endres uten ny agent. Derfor blir en feil til «Post fra sjekken av kjetil-vegar-d venter på svar». Det rettes i trinn 5 (AP13).

## `frist`: tilganger som snart går ut

```
korrespondanse_vakt.py frist
    --profil NAVN (én eller flere)
    --klientrot STI  --markorer STI  --tilstand STI
    [--dager 7] [--sjekk-maks-minutter 60]
```

For hver profil leses `accessCredential.payload.expiresAt` i `<klientrot>/<profil>/profile.json`. Programmet bruker ikke nettet og starter ikke klienten.

**Terskelen.** Programmet regner hele døgn igjen, rundet ned. Markøren skrives når tallet er `--dager` eller mindre. Med `--dager 7` betyr det: under åtte døgn igjen. Åtte døgn og null timer gir ingen markør, sju døgn og 23 timer gir markør, og en frist som er passert, gir markøren «gikk ut».

| Markør | Når | `id` | `from` | `summary` |
|---|---|---|---|---|
| Frist | Hele døgn igjen er `--dager` eller mindre | `frist-<profil>` | «tilgangsfristen for `<profil>`» | «Tilgangsbeviset for `<profil>` går ut 30.10. kl. 20:00, om 7 dager. Etter det kan Losen verken lese eller sende post der.» Under ett døgn: «om under ett døgn». Etter fristen: «Tilgangsbeviset for `<profil>` gikk ut 30.10. kl. 20:00. Losen kan verken lese eller sende post der.» |
| Uten bevis | Profilen har ikke `accessCredential` | `frist-<profil>` | som over | «Profilen `<profil>` har ikke noe tilgangsbevis nå. Losen kan verken lese eller sende post der.» |
| Kan ikke leses | `profile.json` mangler eller kan ikke tolkes | `frist-feilet-<profil>` | «fristvarselet for `<profil>`» | «Fikk ikke lest tilgangsbeviset for `<profil>`. Fristen er ukjent.» |
| Sjekken står | Se regelen under | `sjekk-stoppet-korrespondanse-sjekk` | «korrespondansesjekken (den har stoppet)» | «Korrespondansesjekken har ikke kjørt siden 2.10. kl. 14:30. Planleggeren kan stå.» |

`markedBy` er `agent-korrespondansefrist`.

Når markørene fjernes:

- **Frist:** når hele døgn igjen er flere enn `--dager`, altså når tilgangen er fornyet. Kan `profile.json` ikke leses, står `frist-<profil>` som den var, og `frist-feilet-<profil>` skrives i tillegg.
- **Kan ikke leses:** første gang fila leses igjen.
- **Profiler som er tatt ut:** som for `sjekk`.

**Sjekken står.** Markøren skrives når fristvarselets eget forrige stempel er ferskere enn 48 timer, og korrespondansesjekkens stempel mangler eller er eldre enn 60 minutter. Den fjernes når sjekkens stempel igjen er ferskere enn 60 minutter. Etter søvn kjører planleggeren sjekken først, fordi den står først i `config.json`, så stempelet er ferskt når fristvarselet ser etter det.

## `selvtest`

`korrespondanse_vakt.py selvtest` kjører programmets egne kontroller mot prøvedata i en midlertidig mappe, med en liten klient programmet selv skriver. Den bruker ikke nettet og rører ikke de ekte mappene. Den dekker:

- markør skrives og fjernes; ulest post med `acknowledgedAt: null` og uten feltet;
- feil telles og gir markør andre gang; markørene for ulest post står urørt når profilen ikke ble lest;
- annen kontrakt (verktøyet mangler, `tools/list` er tom, verktøyet krever `relationshipID`) gir feil, ikke tom liste;
- blaing over tre sider, og stopp etter 20;
- en klient som henger, blir drept innen tidsgrensen, og vakttråden etterlater stempel med kode 3;
- alarmen avbryter lesingene ordnet, og kaster ikke en lesing som var ferdig da den kom;
- en tjener som gir 50 meldinger per side, skjuler ikke den nyeste;
- en uventet feil gir én linje og kode 1, ikke en traceback;
- en klient som skriver 200 KiB, henger ikke programmet;
- tidspunkter med og uten millisekunder;
- utrygg tekst skrives ikke (`fixtures/ugyldig-tekst.json`); fremmede markører røres ikke;
- markører for en profil som er tatt ut av `--profil`, fjernes;
- søskenvakten: ingen markør når eget forrige stempel er gammelt, markør når det er ferskt og søskenets er gammelt;
- tre profiler deler tidsbudsjettet, og fem avvises;
- fristen: 8 døgn 0 timer gir ingen markør, 7 døgn 23 timer gir markør, passert frist gir «gikk ut», manglende bevis gir «uten bevis»;
- signalene, slik planleggeren gir dem videre: programmet startes gjennom `/bin/sh` med SIGTERM og SIGINT oversett og `exec`. SIGTERM midt i en kjøring gir kode 143, tom stdout, én linje på stderr, låsen sluppet, intet stempel og klienten drept. En vanlig kjøring gjennom samme omslag fører «startet med SIGTERM oversett» i stempelet. Selvtesten er det installasjonen kjører på Macen, så dette er første gang macOS' `/bin/sh` og Python 3.9 måles på det.

Siste linje er `SELVTEST OK <antall> kontroller`, og koden er 0. Programmet slik det står 03.10, har 126 kontroller og bruker omtrent fjorten sekunder. Installasjonsskriptet kjører selvtesten med `/usr/bin/python3` før noe legges inn (T8 og T9 med prøvedata; testene står i `../FORMAALSSPEC.md` §5).

## Kjente grenser

- Planleggeren laster hendelser og policy bare ved start. Den må derfor startes på nytt etter at `config.json` er endret (`handoff/README.md`).
- Etter en kjøring settes neste tidspunkt til «nå pluss intervall» (`ScheduledEventService.swift` linje 271–274). Etter søvn kjøres hendelsen straks, én gang.
- En hendelse som peker på et fast program som ikke finnes i policyen, oppdages ikke av `validate-config` eller `schedule-list`. Den feiler først når den kjøres. Installasjonsskriptet kontrollerer derfor selv at hver hendelse peker på et program i policyen.
- Agenten leser markørmappen samtidig som programmet skriver. Fjernes en markør i samme øyeblikk som mappen leses, kan kilden ett øyeblikk stå som ulesbar, og du kan få varselet «Får ikke lest correspondence». Det er sjeldent, går over ved neste lesing (20 sekunder), og rettes i agenten i trinn 5.
- Står hele planleggeren, kjører ingen av oppgavene, og ingen markør skrives. Det synes først fra trinn 4.
- Hele innboksen listes ved hver kjøring, høyst 20 sider. Passerer en innboks mellom ett og to tusen meldinger, etter hvor mange tjeneren gir per side, feiler sjekken synlig med «innboksen har for mange sider». Da må programmet få huske hvor det slapp. Innboksene har 15 og 12 meldinger 02.10.
- Om binæren fra 16.08 kaller verktøyet `correspondence_list_inbox` eller `correspondence.list_inbox`, og om den tar `--root`, måles av installasjonsskriptet. Programmet godtar begge navn. Tar klienten ikke `--root`, stopper `toerr`, og ingenting legges inn: programmet har ingen utgave uten `--root`.
