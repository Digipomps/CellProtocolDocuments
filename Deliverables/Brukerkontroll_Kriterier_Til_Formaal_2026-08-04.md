# Brukerkontroll: fra gammel kriterieskisse til formål

Dato: 2026-08-04

Status: analyse og begrunnelse for kandidatgrenen
`purpose://self-determination.data` i `Book/haven_purpose_knowledge_base_v0.json`.
Grenen er lagt inn med status `candidate` og endrer ikke kjøretidstaksonomien.

## Kilde

En gammel håndskisse med målet «Alle brukere har rett til å bestemme over egne
data», dekomponert i kolonnene *Impliserer*, *Krever*, *Hvorfor*, *Trenger*,
*Områder* og en tom *Løsninger*-kolonne. Skissen er vurdert som kriteriesett og
omskrevet til formål med målbare Goals.

## Vurdering av skissen

### Det som holder

- Firedelingen *hva / hvilke / hvor / hvordan* er en reell dekomponering av
  kontroll og treffer formålsbinding, minimering, lokalitet og behandlingsmåte.
- «Hvorfor»-kolonnen er den sterkeste delen: autonomi, hindre nedkjøling,
  valgbar identifiserbarhet og synliggjort påvirkning er fortsatt gyldige
  begrunnelser.
- At «Trenger»-kolonnen handler om organisasjonen og ikke bare teknikken, er
  riktig instinkt: brukerkontroll er en institusjonell garanti, ikke bare en
  teknisk egenskap.

### Det som ikke holder som kriterier

1. **Ingen av boksene er testbare.** Ingen har observerbart suksesskriterium
   eller verifikator. I HAVEN-termer: formål uten Goal. «Gjennomsiktighet»,
   «tillit til løsning» og «enkelt for bruker» kan verken bestås eller avvises.
2. **To dimensjoner mangler.** *Hvem* finnes bare indirekte («uvedkomne»,
   «delegere»), og *hvor lenge / angre* mangler helt. Kontroll som ikke
   overlever at data har forlatt eier, er ikke kontroll: tilbaketrekking,
   sletting, nedstrøms forplantning og eksport står ingen steder.
3. **Lagblanding i «Impliserer».** *Globalt tilgjengelig* og *alltid
   tilgjengelig* er tjenesteegenskaper, ikke rettigheter, og følger ikke av
   målet. De står dessuten i direkte motsetning til *hvor egne data skal
   brukes*. En tjeneste kan ha 100 % oppetid og null kontrollerbarhet.
4. **Samtykkeabsolutisme.** «All datautveksling må godkjennes via bruker» er
   både juridisk upresist (samtykke er ett av flere behandlingsgrunnlag) og
   praktisk selvundergravende: per-hendelse-godkjenning gir klikketretthet, som
   produserer det motsatte av kontroll. Riktig form er stående, lesbar,
   oppsigelig avtale, som er der HAVENs avtalemodell faktisk landet (Book 04).
5. **«Tillit til organisasjon» som krav er en selvmotsigelse.** Et design som
   krever at eier stoler på drifteren, har flyttet kontrollen, ikke gitt den.
   Den viktigste enkeltoppgraderingen er å bytte *tillit* mot
   *etterprøvbarhet*; da betyr organisatorisk stabilitet mindre.
6. **«Ingen adgang for uvedkomne» er sirkulært.** «Uvedkomne» er nettopp det
   kriteriet skulle definere. Erstattes av default deny og eksplisitt
   kapabilitet.
7. **Uanerkjent spenning.** *Normalisering av data* gir interoperabilitet og
   koblingsrisiko samtidig, og står imot notatet nederst i skissen om dataenes
   usikkerhetsrelasjon. *Deltagelse i verdiskapningen* følger ikke av kontroll i
   det hele tatt; det krever en verdiretur-mekanisme
   (`purpose://value-and-commons`).
8. **«Løsninger» er tom og «Områder» er ukoblet.** Skissen stopper rett før den
   ble nyttig: hvert kriterium trenger et ansvarslag, fordi de fleste svikter
   hvis de bare implementeres teknisk.

**Konklusjon:** som problemforståelse holder skissen seg bedre enn de fleste fra
sin tid. Som kriteriesett er den ikke brukbar: den mangler målbarhet, mangler
tid og tilbaketrekking, og ber om tillit der den burde krevd bevis.

## Formålsgrenen

Kunnskapsbasen hadde ingen gren for selvbestemmelse over data. Nærmeste var
`purpose://access.audit.privacy` og `purpose://preference.owner-controlled`
under governance, som begge handler om hvordan systemet oppfører seg, ikke om
eierens rett til å bestemme.

```
purpose://self-determination.data — Selvbestemmelse over egne data
├── .use-purpose      Hva egne data skal brukes til
├── .scope            Hvilke egne data skal brukes
├── .locality         Hvor egne data skal brukes
├── .manner           Hvordan egne data skal brukes
├── .recipients       Hvem som får bruke dem            (ny dimensjon)
├── .duration         Hvor lenge — og retten til å ombestemme seg (ny)
├── .verifiability    Etterprøvbarhet framfor tillit    (ny)
└── .exercisability   Kontroll som faktisk kan utøves
```

Hvert formål har Goal med `outcome`, `successSignals` og `verifier` skrevet mot
eksisterende testflater: resolver-policytester, avtalelivsløp, audit-assertions
og brukerstitester.

## Språk og matching

Nodene er skrevet på engelsk i kunnskapsbasen, som resten av basen. Det er ikke
kosmetikk: `derive_purpose_index.mjs` indekserer `title`, `summary`,
`goal.outcome` og `successSignals`. Første utkast hadde norsk brødtekst, og da
falt `evaluate_purpose_cases.mjs` fra 56/56 til 53/56 — kandidatgrenen kapret
norske prompt fra `purpose://gui.quality.functional-accessible` og
`purpose://governance` på generiske ord som «alle», «tilgang», «samtykke» og
«profilering». Med engelsk brødtekst og bare distinktive norske aliaser
(«selvbestemmelse over egne data», «datasuverenitet») er suiten tilbake på
56/56.

Konsekvensen er bevisst: grenen treffer i dag på engelske formuleringer og på de
distinktive norske frasene, ikke på vanlige norske personvern-prompt. Når grenen
eventuelt løftes fra `candidate` til `active`, må norske aliaser legges inn
sammen med nye fixtures — og eierskapet til de generiske ordene avklares mot
governance-grenen.

## Kartlegging fra skissen

### Beholdt

| Boks i skissen | Formål |
| --- | --- |
| Hva egne data skal brukes til | `.use-purpose` |
| Hvilke egne data skal brukes | `.scope` |
| Hvor egne data skal brukes | `.locality` |
| Hvordan egne data skal brukes | `.manner` |
| Avtaler / samtykker | bærende mekanisme for hele grenen, ikke eget kriterium |
| Ingen adgang for uvedkomne | `.recipients`, omformulert til default deny |
| Delegere rettigheter | `.recipients` |
| All datautveksling må godkjennes via bruker | `.recipients` + `.use-purpose`, svekket fra per-hendelse-godkjenning til stående, lesbar, oppsigelig avtale |
| Velge grad av identifiserbarhet | `.scope` |
| Gjennomsiktighet | `.verifiability` |
| Enkelt for bruker | `.exercisability` |
| Data usikkerhetsrelasjon | `.scope`, som åpent spørsmål, ikke løst kriterium |

### Flyttet til mekanisme, strategi eller governance

| Boks | Plassering |
| --- | --- |
| Sikker autentisering | mekanisme, Book 03 Identity |
| Sikker tilgang | mekanisme, Book 06 CellResolver |
| Sikker lagring | mekanisme, lagringskontrakt |
| Personlig datalager | løsningsvalg, ikke kriterium; kriteriet er kontroll, ikke plassering |
| Gode integrasjonsmuligheter | strategi; nødvendig for utbredelse, ikke for kontroll |
| Dannelse av økosystem | strategi |
| Må kunne brukes mot alle tjenester | ambisjon; måles ikke som kontrollkriterium |
| Normalisering av data | mekanisme med motsetning; hører under `.scope` som avveining |
| Kompetent fagmiljø, stabil organisasjon, ikke bindinger til annen interesse | institusjonell forutsetning under governance |

### Forkastet som kriterium

| Boks | Begrunnelse |
| --- | --- |
| Globalt tilgjengelig | tjenesteegenskap i direkte spenning med `.locality`; kan ikke stå som implikasjon av målet |
| Alltid tilgjengelig | oppetidsløfte, ikke kontroll |
| Tillit til organisasjon | erstattet av `.verifiability` |
| Tillit til løsning | samme; tillit er ønsket effekt, ikke kriterium |

### «Hvorfor»-kolonnen

Beholdt som begrunnelse, ikke som kriterier: autonomi, hindre nedkjøling,
deltakelse i verdiskapingen, likere muligheter, valgbar identifiserbarhet,
distribuert AI-modell, synliggjøre påvirkning.

## Åpne spørsmål

1. Dataenes usikkerhetsrelasjon: hvor grovt må et datasett være før identitet
   ikke kan avledes, og hvordan uttrykkes den grensen maskinlesbart i `.scope`?
2. Hvem er motstanderen? Kriteriene peker på minst tre — driftsoperatøren,
   tredjepartstjenester og treningspipelines — med delvis motstridende
   mottiltak.
3. Er modellvekter trent på mine data fortsatt «mine data»? `.manner` antar ja
   for avledning, men grensen er ikke satt.
4. Områdene juridisk / organisasjon / teknisk fra skissen er ennå ikke tildelt
   per kriterium. De fleste kriteriene svikter hvis de bare implementeres
   teknisk.
