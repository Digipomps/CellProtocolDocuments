# HAVEN: kvalitetsvurdering, modenhet og retning

Dato: 2026-08-09

Vurderer HAVEN som helhet: hva som faktisk er bygget, hvor god kvaliteten er,
hvor langt utviklingen er kommet, hvordan nivået plasserer seg mot løsninger en
fagperson kjenner fra før, og om formålene og argumentene holder.

## 1. Metode og forbehold

Alt i del 2 og 3 er målt på maskinen i dag, ikke hentet fra statusdokumenter.
Kjørt: `swift test` i CellProtocol, formålsevalueringen, `verify_app_entry.py`,
HTTP-kontroll mot alle fire verter, `gh run list` mot alle repoene, samt
opptelling av kode, tester, formål og fixtures.

Ikke kjørt: CellScaffolds Swift-suite og Playwright-suiten (de tar timer og
krever staging-miljø; jeg bruker rapporten fra i natt i stedet, med den kilden
navngitt), og Binding-testene, som ikke har noen kjørbar CI-flate.

Vurderingen er skrevet dagen før Arendalsuka og midt i en arbeidsordre med frist
15:00. Den er ikke en oppgaveliste for i dag.

## 2. Hva som faktisk finnes

| Repo | Kildelinjer | Testlinjer | Testfunksjoner | CI |
| --- | --- | --- | --- | --- |
| CellProtocol | 101 063 | 42 784 | 932 | Swift Linux, grønn på `main` 5. aug |
| CellScaffold | 315 637 | 114 879 | 1 960 | kun image-bygg, ingen testkjøring |
| Binding | ~138 000 totalt | i samme tre | 436 | ingen |
| PyCellProtocol | 4 646 | — | — | kun upstream-sync |
| GoCellProtocol | 5 661 | — | — | ingen |
| RustCellProtocol | 6 803 | — | — | ingen |

Dokumentasjon: 35 bokkapitler (10 336 linjer), 9 maskinlesbare kontrakter,
89 leveransedokumenter, 57 formål i kunnskapsbasen.

Levende flater, kontrollert i dag: `digipomps.org` 200, `haven.digipomps.org`
200 med `/health` `ok`, `staging.haven.digipomps.org` 200,
`new.haven.digipomps.org` 200.

Til sammen rundt 700 000 linjer Swift medregnet tester. Dette er ikke en
prototype. Det er en mellomstor plattform, bygget av én person med agenter.

## 3. Kvalitet, lag for lag

### Protokollkjernen — sterkest

`swift test` kjørte grønt i dag (exit 0) over 932 testfunksjoner, og
Linux-CI-en har vært grønn på `main`. At kjernen bygger og testes på Linux, ikke
bare macOS, er et reelt portabilitetsbevis og noe de fleste Swift-prosjekter i
denne størrelsen ikke har.

Håndhevingen sitter der den skal: `CellResolver` kaster
`CellAuthorizationError.denied` som utfall av en beslutning, ikke som en
if-setning spredt utover kallstedene. 19 wire-fixtures låser formatet.

### CellScaffold — størst, svakest verifisert

1 960 testfunksjoner og 115 000 linjer test er mye. Men det finnes ingen CI som
kjører dem. Den eneste workflowen bygger images. Siden 8. august har GitHub
Actions dessuten feilet av en grunn som ikke har noe med koden å gjøre:
«recent account payments have failed or your spending limit needs to be
increased». Kjørende betaling er altså i dag en del av verifikasjonskjeden.

Playwright-kjøringen mot staging i natt: **38 passert, 69 feilet, 12 ikke
kjørt**. Rapporten er uvanlig ærlig og metodisk sterk — den avviser først sine
egne skeleton-tester som bevis for staging, og bygger broen med
digest-sammenligning mot det som faktisk serveres, før den konkluderer. Det er
høyere bevisdisiplin enn det meste jeg ser i produksjonsteam.

To funn derfra er alvorlige:

- **Atomisitetsgarantien holder ikke.** En malformert skeleton erstatter en
  fungerende visning i stedet for å bli avvist. Den utrullede renderen er
  byte-identisk med repoets, så defekten er live. Dette treffer selve
  forutsetningen for at kjøretidsredigerbare konfigurasjoner er trygge.
- **61 av 69 feil har én rotårsak:** en førstegangsbruker får ikke
  `PersonalChatHub` provisjonert og møter en 422 i stedet for Co-Pilot Chat.
  Filen dekker 5 426 identiteter, hvorav 58 har hub. Førsteinntrykket er altså
  brutt for tilnærmet alle nye brukere.

Den andre er verre enn tallet antyder, fordi det er nøyaktig
utøvbarhetskriteriet fra brukerkontroll-settet: hvis en vanlig person ikke kommer
gjennom de første minuttene, faller kriteriet uansett hvor god resten er.

### Binding — ubevoktet

436 testfunksjoner, ingen CI, ingen lisensfil. Appen er den flaten et menneske
faktisk møter, og den er den minst kontinuerlig verifiserte delen av systemet.

### Dokumentasjonen — prosjektets nest sterkeste aktivum

35 kapitler med maskinlesbare kontrakter ved siden av, en formålsgraf med
`goal.outcome`, `successSignals` og navngitt verifikator per node, og en
evalueringssuite som kjørte 56/56 i dag. PyCellProtocols README har et eget
avsnitt om hva som *ikke* er implementert og feiler lukket. Den typen
selvbegrensning er sjelden og er i seg selv et kvalitetstegn.

### Drift — over forventet nivå

Immutable images, egen rollback-container per cutover, readiness-gate,
fingeravtrykkskontroll gjennom start og restart, restore-proofs, diskvakt i
byggeskriptet, og arbeidsordrer med eksplisitte forbud mot å slakke tester eller
sette bypass-flagg. Dette er driftsdisiplin på et nivå de fleste selskaper med
femti ansatte ikke har.

Motstykket: disken lå på 87 %, det finnes ni fulltrekopier og seks
retry-artefakter på verten, og produksjon kjører en annen commit enn staging.
Disiplinen finnes i prosedyrene, ikke ennå i automatikken.

## 4. Kalibrering mot kjente løsninger

For noen som kjenner feltet, er dette de sammenligningene som betyr noe:

**Mot Solid.** HAVENs autorisasjonsmodell er vesentlig rikere enn WAC/ACP:
formålsbinding, avtaler med livsløp, betingelser, evidence og kvitteringer mot
Solids ressurs- og agentbaserte tilgang. Solid har til gjengjeld det HAVEN ikke
har: en spesifikasjon med flere uavhengige serverimplementasjoner, en
konformanssuite, og en offentlig utrulling mot 6,5 millioner innbyggere i
Flandern. HAVEN har mer *produkt* per begrep. Solid har mer *protokoll*.

**Mot AT Protocol.** Bluesky har en lexicon-modell med uavhengige
implementasjoner og over 1 000 tredjepartsapper. HAVENs bokkapitler og
JSON-kontrakter er sammenlignbare i ambisjon, men wire-formatet er ikke
uavhengig implementert av noen. Forskjellen er ikke dokumentkvalitet; den er
antall parter som har måttet lese dokumentet for å få noe til å virke.

**Mot IDS/Gaia-X og Eclipse Dataspace Components.** Dette er den nærmeste
mekaniske slektningen — ODRL-policyer håndhevet hos mottakeren. EDC har titalls
bedriftsbidragsytere og interop-tester på tvers av connectorer. HAVEN har én
implementasjon, men et genuint annet veddemål: eieren er en person, ikke en
virksomhet. Det er en reell posisjon, ikke en svakere versjon av EDC.

**Mot MCP.** MCP nådde over 10 000 servere på omtrent et år fordi det løste ett
smalt problem med en triviell spesifikasjon. HAVENs begrepsflate er
størrelsesordener større. I distribusjonssammenheng er det en ulempe, ikke en
styrke, og det er verdt å si høyt.

**Plassering.** Teknisk: sen alfa til tidlig beta, med én normativ
implementasjon. Drift: produksjonsklar for én operatør. Dokumentasjon: over
nivået til de fleste prosjekter i denne fasen. Økosystem: før-adopsjon.

Det siste er det harde tallet: **null stjerner, null forks og null eksterne
bidragsytere** på alle de offentlige repoene. Og lisenssituasjonen forklarer en
del av det — `Binding`, `CellProtocolDocuments` og `PyCellProtocol` ligger
offentlig **uten lisensfil**, som juridisk betyr at ingen har lov til å bruke
dem. `CellScaffold` og `RustCellProtocol` er private.

## 5. Formål og argumenter

Formålsgrafen er prosjektets mest originale bidrag. At hvert formål har et Goal
med observerbare suksessignaler og en navngitt verifikator, er en disiplin jeg
ikke kjenner fra noen av sammenligningsprosjektene. Den gjør «brukerkontroll» til
noe som kan bestås eller strykes, i stedet for noe man erklærer.

Men grafen har en systematisk skjevhet, og den er lett å se når man teller: av
25 grener modellerer nesten alle **eieren og systemet**. Ingen gren modellerer
**motparten** — tjenesten, utvikleren eller virksomheten som må si ja for at noe
som helst skal skje. Det finnes ikke noe `purpose://adoption`, ingen
integrasjonsgevinst, ingen kostnad ved å slutte seg til.

Det er ikke en akademisk mangel. Det er nøyaktig hullet fra
produktivitetsanalysen, nå synlig som en strukturell tomhet i taksonomien:
formålene beskriver et system uten den parten hvis ja avgjør om systemet finnes.

To andre huller, i fallende alvorlighet:

- **Kontinuitet.** Ingen formål dekker hva som skjer hvis operatøren forsvinner.
  `.verifiability` fjerner behovet for å stole på drifteren mens drifteren lever.
  Det er ikke det samme som at dataene overlever at Digipomps slutter.
- **Kostnad.** Ingen formål har en pris. `.exercisability` krever «uten kostnad
  for personen», men ingenting sier hvem som betaler, eller hva kontrollen koster
  per bruker.

`self-determination` og `value-and-commons` står begge som `candidate`. De to
grenene som bærer hele fortellingen, er altså ikke aktive i kjøretidstaksonomien.

## 6. Er det komplett?

Nei, og det er heller ikke rimelig å vente. Det som betyr noe er *hvilke* deler
som mangler, og der er svaret ubehagelig presist: det som mangler, er ikke
kjernen. Det er tre ting som alle ligger utenfor kompilatorens rekkevidde.

1. **Én implementasjon.** Py-portens `fixtures/golden` er tom, og hverken Go- eller
   Rust-porten kjører mot Swift-fixturene. Uten en uavhengig implementasjon som
   må passere de samme 19 fixturene, er dette et bibliotek med god dokumentasjon,
   ikke ennå en protokoll. Dette er den enkeltforskjellen som skiller HAVEN fra
   Solid og AT Protocol, og den kan lukkes uten tillatelse fra noen.
2. **Ingen mottakerside.** De fire kontrollkriteriene som skiller HAVEN fra Solid
   — formål, måte, varighet, etterprøvbarhet — kan bare håndheves hos en mottaker
   som kjører noe HAVEN-aktig. Antall slike mottakere er i dag null.
3. **Lisenshullet.** Tre offentlige repoer uten lisens er en teknisk banal, men
   praktisk avgjørende, sperre mot at noen i det hele tatt kan prøve.

## 7. Er retningen fornuftig?

Ja, med ett vesentlig forbehold.

Det som gjør retningen fornuftig, er at analysen bak den er ærligere enn feltets.
Prosjektet har selv identifisert at samtykkeabsolutisme produserer klikketretthet,
at «tillit til organisasjon» som krav er en selvmotsigelse, at kontroll uten
tilbaketrekking ikke er kontroll, og at brukerkontroll uten en verdiretur ikke
gir deltakelse i verdiskapingen. Det er fire innsikter som store deler av
personvernfeltet fortsatt ikke har tatt inn over seg. Kombinasjonen av dem med
en kjøretid som faktisk finnes, er sjelden.

Forbeholdet er tempo mot flate. Prosjektet utvider begrepsflaten raskere enn det
lukker den. 57 formål, 35 kapitler, seks runtimes påbegynt, konferanse, chat,
kunnskapspanel, agentdaemon, mikrobetalinger og et regulatorisk spor — mens
førstegangsbrukeren ikke kommer inn i chatten og en malformert konfigurasjon kan
slå ut en fungerende visning. Bredden er prosjektets største risiko, og den er
selvpålagt.

Den sterkeste innvendingen mot hele retningen, ærlig gjengitt: et
kontrollag som krever at mottakeren kjører det, har historisk aldri vunnet uten
et mandat i ryggen. Solid fikk sitt gjennombrudd i Flandern gjennom det
offentlige, ikke gjennom markedet. Britisk open banking kom av et pålegg. Hvis
den observasjonen holder, er den viktigste strategiske variabelen ikke
kodekvalitet i det hele tatt, men om HAVEN kobles til en forpliktelse noen andre
allerede har — EUDI-tilslutning, offentlig sektor, eller et regulatorisk krav
som gjør formålsbundet tilgang billigere enn alternativet.

Det motargumentet svekker ikke retningen. Det flytter tyngdepunktet fra å bygge
mer til å skaffe den første mottakeren.

## 8. Hva jeg ville gjort først

I rekkefølge, og bevisst kort:

1. Provisjonering av hub for førstegangsbrukere, og atomisk swap. De to
   defektene er henholdsvis utøvbarhetskriteriet og integritetsgarantien, uttrykt
   som feilende tester. Begge står allerede i arbeidsordren.
2. Lisensfil på `Binding`, `CellProtocolDocuments` og `PyCellProtocol`. Koster
   en time og fjerner en juridisk sperre mot all ekstern bruk.
3. Én CI som kjører CellScaffold-testene, og en betalingsordning som ikke
   stopper verifikasjonen. 1 960 tester uten kontinuerlig kjøring er
   dokumentasjon, ikke vern.
4. Fyll `PyCellProtocol/fixtures/golden` fra Swift-fixturene og la Python-suiten
   feile på avvik. Det er den billigste veien fra bibliotek til protokoll.
5. Legg inn en formålsgren for motparten, med Goal og verifikator. Uten den kan
   ikke resten av grafen svare på hvorfor noen andre skulle bli med.

## Grunnlag

Målt 2026-08-09 på denne maskinen. Playwright-tallene er hentet fra
`CellScaffold/Documentation/Operations/Staging_Surface_Test_Report_2026-08-09.md`,
ikke kjørt på nytt. Sammenligningsgrunnlaget mot Solid, AT Protocol, dataspaces
og MCP er dokumentert i
`Beslektede_Prosjekter_Brukerkontroll_Sammenligning_2026-08-09.md`.
