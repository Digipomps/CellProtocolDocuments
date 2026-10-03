# ACCEPT — agent menylinje og varsler

Dato: 2026-09-10. **G3-underlag, ikke G3-godkjenning.** G1, G1-GUI og G3 venter alle på Kjetil.

Denne oppgaven ble bestilt sent på kvelden med «implementer det, test og vis meg
imorgen», og portene kunne ikke settes mens han sov. Formålene ligger derfor til
godkjenning **samtidig** som det finnes noe kjørende å se på. Blir §1 endret, er
koden det som viker — ikke omvendt.

## Forventningskontrakten, rad for rad

Radene speiler [FORMAALSSPEC §3](FORMAALSSPEC.md#3-forventningskontrakt--det-du-kommer-til-å-se).

| Rad | Forventning | Faktisk | Bevis |
| --- | --- | --- | --- |
| L1 | Formålsspesifikasjon | [FORMAALSSPEC.md](FORMAALSSPEC.md), 12 auditerte påstander. Auditen fanget to feil i min egen forståelse før noe ble bygget: jobbkøen finnes ikke på `main`, og verken menylinje eller varselkode fantes fra før. | §0-tabellen |
| L2 | Rendret bilde per tilstand + adminvindu | Fire bilder i [images/](images/): `menu-ok-v1`, `menu-attention-v1`, `menu-down-v1`, `admin-window-v1`, samt `notification-v1`. **Dette er tegnede referansebilder, ikke skjermbilder av den kjørende appen** — de er det G1-GUI skal godkjennes mot, og det `test.gui.parity` skal måles mot etterpå. | filene |
| L3 | Challenge-kontrakt med fixtures | [`Contracts/agent-challenge-v1.schema.json`](../../../HavenAgentD/Contracts/agent-challenge-v1.schema.json) i HavenAgentD, med tre fixturefiler; de negative har 8 poster som hver må avvises med sin egen grunn. | [#challenge](TESTRESULT.md#challenge) |
| L4 | Kode på egen gren, commit per bladformål | Gren `pdd/agent-menylinje-og-varsler` i `HavenAgentD`, fra `main` `ba14895`. Ti commits: én forutsetning, fem for arbeidet, fire for rettelser etter gjennomlesing, én for dokumentasjon. | [handoff/COMMIT_RAPPORT.md](handoff/COMMIT_RAPPORT.md), `COMMIT_RAPPORT_2.md` |
| L5 | Kjørende menylinjeitem med adminvindu | **Appen kjører på Kjetils maskin** (`HAVEN Agent.app`, ad-hoc signert, `io.digipomps.haven.agentmenu`). **Ikke fotografert:** `screencapture` ga svart bilde fordi skjermen sov. Bildet må tas når han logger inn. | [#app](TESTRESULT.md#app) |
| L6 | Faktisk varsel i macOS' varslingsliste | **Ikke verifisert.** Krever at et menneske svarer på samtykkedialogen. Logikken bak er testet (9 tester), leveringen er ikke. | [#notify](TESTRESULT.md#notify) |
| L7 | Testutdata for hver rad i §5 | [TESTRESULT.md](TESTRESULT.md) med ekte utdata, inkludert baseline, flakhetskontroll og HTTP-svar fra en faktisk kjørende agent. | hele filen |
| L8 | Akseptanse | Denne filen. | — |

## Avledede tester i §5

| Test | Status | Bevis |
| --- | --- | --- |
| `test.menu.three-states` | Grønn | [#menu](TESTRESULT.md#menu) |
| `test.menu.unknown-is-not-ok` | Grønn — alle fem feilutfall gir `unknown`, ikke-tom liste og egen overskrift | [#menu](TESTRESULT.md#menu) |
| `test.menu.admin-window-shows-report` | **Ikke kjørt.** Adminvinduet finnes i kode og bygger, men er ikke fotografert mot `haven-agentd status` | [#gjenstår](TESTRESULT.md#gjenstår) |
| `test.challenge.inbox-shape` | Grønn, 19 tester | [#challenge](TESTRESULT.md#challenge) |
| `test.challenge.sources` | Grønn, og bekreftet mot en faktisk agent over HTTP | [#e2e](TESTRESULT.md#e2e) |
| `test.challenge.answer-uses-real-path` | Grønn: `answeredVia: ReviewCommandService.approve` kom fra en ekte agent, og en sak flaten ikke kan besvare fikk `"ingen"` | [#e2e](TESTRESULT.md#e2e) |
| `test.notify.purpose-gate` | Grønn | [#notify](TESTRESULT.md#notify) |
| `test.notify.no-duplicates` | Grønn | [#notify](TESTRESULT.md#notify) |
| `test.notify.no-secrets` | Grønn, og etter rettelse også for kildelistens begrunnelser | [#review](TESTRESULT.md#review) |
| `test.notify.appears-in-center` | **Ikke kjørt** — sovende skjerm, manglende samtykke | [#gjenstår](TESTRESULT.md#gjenstår) |
| `test.build` | Grønn | [#build](TESTRESULT.md#build) |
| `test.regression` | Grønn: 165 → **227 tester, 62 nye, null nye feil**. De to røde er begge ustabile på ren base | [#regression](TESTRESULT.md#regression), [#review4](TESTRESULT.md#review4) |
| `test.branch-has-commits` | Grønn: grenen står på sju commits over `ba14895`, ikke på basen | [handoff/COMMIT_RAPPORT.md](handoff/COMMIT_RAPPORT.md) |
| `test.docs-updated` | Grønn: `HavenAgentD::Docs/AgentMenylinje.md` i samme endring, datert | commit 7 |
| `test.status-current` | Grønn | [STATUS.md](STATUS.md) |

## Det som er verdt å merke seg

**Rettet 2026-09-11: påstanden «`main` bygger ikke» var feil.** Den handlet om
`ba14895`, en commit som bare lå på den **lokale** main-grenen og aldri var
pushet, og som avhang av CellBase-kode som heller ikke var pushet.
`origin/main` var fire commits lenger fram og grønn hele tiden — verifisert med
en ren klone fra GitHub: bygg grønt, 179 tester, én ustabil rød fra før.

Feilen var min i to ledd. Først målte jeg en baseline i et lokalt utsjekk uten
å sjekke om det utsjekket var det samme som origin. Så svarte jeg på den røde
baselinen med `swift package edit` mot lokale søsterutsjekk, i stedet for å
spørre hvorfor den var rød. Da bygde alt — på én maskin — og jeg meldte det som
verifisert. Arbeidet er nå spilt av på nytt oppå den ekte main, og
forutsetnings-commiten er droppet fordi den aldri trengtes.
Se [#ekte-main](TESTRESULT.md#ekte-main).

**Fire runder kodegjennomgang fant tjuefire reelle feil** i kode som bygde grønt og
hadde grønne tester. To av dem var alvorlige: `AgentMenuModel.start()` ble
aldri kalt, så appen ville aldri hentet noe; og et samlevarsel husket bare sin
egen syntetiske ID, så appen ville laget et nytt samlevarsel hvert 20. sekund.
Ingen test fanget noen av dem. Alle tjuefire er rettet. Se [#review](TESTRESULT.md#review), [#review2](TESTRESULT.md#review2),
[#review3](TESTRESULT.md#review3) og [#review4](TESTRESULT.md#review4).

Dette er den klareste enkeltobservasjonen fra oppgaven: grønne tester på egen
kode sier lite. En annen leser som går gjennom diffen linje for linje fant
tjuefire ting testene ikke så.

**Flakhetskontrollen.** Den ene gangen mine endringer så ut til å innføre en ny
rød test, ble basen kjørt tre ganger uten mine endringer i et eget worktree.
Testen feilet 2 av 3 der. Uten den kontrollen ville jeg enten tatt på meg en
feil jeg ikke hadde laget, eller avfeid den uten grunnlag.

## Uttrykkelig ikke gjort

- **Bilde av den kjørende menyen og et faktisk varsel.** Skjermen sov. Appen
  kjører, og Kjetil ser den selv. Dette er de to radene som avgjør om oppgaven
  er løst, og de er ikke krysset av.
- **Den kjørende agenten på 43110 er forrige binær.** Den har ikke `/challenges`.
  Menyen vil derfor si «Agenten kjører en versjon uten challenge-innboks» til
  daemonen startes på nytt. Jeg har ikke restartet Kjetils produksjonsagent mens
  han sov — den kjører også korrespondansen.
- **Tilgang og påfyll med ekte data.** Kilden melder erklært fravær med
  begrunnelse, som er riktig oppførsel, men det er ikke det samme som at Vegars
  tilgangsforespørsel dukker opp i menyen.
- **De andre Apple-plattformene.** Kontrakten er plattformnøytral med vilje;
  kravlisten for iOS står i FORMAALSSPEC §2.
- **Signering, notarisering og LaunchAgent.** Appen er ad-hoc signert og startes
  manuelt. Gatekeeper vil klage hvis den flyttes.
- **Landet på den ekte main** 2026-09-11 etter at CI var grønn. Se STATUS.
- **`swift test` avslutter med 1 selv når alt er grønt** i dette repoet, fordi en
  tom XCTest-pakke ikke kan lastes. Det gjelder også på ren `main`. Se
  [#exitcode](TESTRESULT.md#exitcode) — et CI-oppsett her vil være rødt uansett.
