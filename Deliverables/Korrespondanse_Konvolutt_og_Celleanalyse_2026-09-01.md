# Konvolutten, cellen og entiteten — analyse mot HAVEN-konseptene

**Dato:** 1. september 2026
**Beslutningseier:** Kjetil
**Skrevet av:** Losen (Claude), etter beslutning om å holde tilbake VegardPakke
**Status:** Analyse. Videreført som designkontrakt i
`CellProtocolDocuments/Book/33_Correspondence_First_Class.md` og
`correspondence_cell_contract_v0.json`; implementasjon i
`Codex_Handoff_Correspondence_First_Class_2026-09-01.md`.

## Formål med analysen

Avgjøre hva som må være sant før korrespondansepakken kan sendes til en part
utenfor huset, uttrykt i HAVENs egne begreper i stedet for som en liste over
manglende funksjoner. Utløsende beslutning: pakken sendes ikke før notarisert
klient foreligger og operatøren ikke lenger kan se mottakerens kontakter.

---

## Funn 1 — konvolutten ligger utenfor formålsregimet

Dette er analysens hovedfunn, og det er ikke en implementasjonsfeil.

`purposeRef` binder **innholdet** i en melding til et erklært formål. Men
konvolutten — avsender-ID, mottaker-ID, emne, opprettelsestidspunkt, utløp og
kvitteringstidspunkt — samles inn og lagres uten at noe formål er erklært for
den innsamlingen, og uten at noen Agreement dekker den.

Alt annet i HAVEN krever declared purpose og grant før data kan behandles.
Konvolutten gjør det ikke. Den finnes fordi transporten trenger den, og har
dermed sluppet unna regimet den selv er bygget for å håndheve.

Konsekvensen er at Gate 2 ikke er en manglende funksjon. Det er en manglende
modell. Konvolutten trenger eget formål, egen Agreement, egen retention og
egen revokasjon — på samme måte som innholdet.

Formulert som påstand: **et system som formålsbinder innhold, men ikke
metadata, håndhever personvern der det er billigst og ikke der det er
farligst.** For journalistikk er metadataene det farlige. Kildens navn er
sjelden i teksten; at kilden ble kontaktet, er alltid i konvolutten.

### Fire løsninger, ordnet etter hva de faktisk garanterer

| # | Løsning | Hva operatøren ser | Garantitype |
|---|---|---|---|
| 1 | Policy: operatøren lover å ikke lese, og sletter konvolutter | Alt, men lover å la være | **Påstand.** Ikke egenskap. |
| 2 | Pseudonyme, roterende peer-ID-er per relasjon | At to opake ID-er utvekslet post | Egenskap for identitet, ikke for eksistens |
| 3 | Forseglet konvolutt: avsenderidentitet inne i det krypterte, lagring under mottaker-avledet tag | At noe ble lagret for en mottaker-tag | Egenskap. Størst endring. |
| 4 | Deltakerdrevet server: Vegard drifter sin egen | Ingenting — Kjetil er ikke i tillitsposisjonen | Egenskap, arkitektonisk |

Løsning 1 er utilstrekkelig for kildevern per definisjon: hele poenget med
kildevern er å ikke måtte stole på en tredjepart. Å be en journalist stole på
operatørens løfte er å be ham om det han er profesjonelt forpliktet til å ikke
gjøre.

Løsning 4 er den mest HAVEN-native. Den er samme bevegelse som at Kallimachos
skal leve distribuert over flere scaffolds med felles rotdata: tillit skal
ligge i protokollen, ikke i hvem som tilfeldigvis eier maskinen. Den fjerner
også Kjetil fra en posisjon han uansett ikke bør ha overfor en journalist.

**Anbefaling:** 4 som mål for produktet, 2 som det som realistisk kan leveres i
denne piloten. 2 og 4 er additive, ikke alternative.

### Grensen som må sies høyt

Den som frakter, ser trafikkmønster. Volum, tidspunkter og størrelser lekker
uansett hva som krypteres, med mindre man legger på padding og dekktrafikk med
tilhørende kostnad.

Derfor kan vi garantere **operatørblind for identitet**. Vi kan ikke garantere
**uobserverbar**. Pakken skal påstå det første og eksplisitt avkrefte det
andre. En overdreven påstand her er ikke markedsføring, det er en risiko vi
plasserer hos en annens kilde.

---

## Funn 2 — metoden skal være celle, og husets egen regel sier det allerede

Regelen i huset: *er det behov for å dele innholdet, skal det være en celle;
ellers kan det være en rolle, men da skal den ikke hete Cell.*

Analysemetoden — dekomponering, statusvokabular, verdikttyper, kritiske
spørsmål — **må deles**: Vegard skal kunne bruke den. Etter husets egen regel
er den dermed en celle. Ikke et dokument, ikke en rolle.

En SKILL.md som beskriver metoden er den dårligste av alle former, fordi den
er delt *og* gir bort operasjonen samtidig. Den kan i tillegg ikke:

- versjoneres mot en mottaker,
- revokeres når et samarbeid avsluttes,
- måles, fordi ingen vet om den ble fulgt,
- bindes til et formål, fordi tekst ikke kan håndheve noe.

En celle kan alt dette. Den kan i tillegg bære en **garanti**: en skill er et
råd, en celle er en operasjon med erklært formål som kan etterprøves mot sitt
eget resultat.

Dette er også forskjellen mellom et prosjekt og et produkt. Et produkt selger
kapabilitet. Et dokument som forklarer hvordan man gjør det selv, selger
ingenting og kan bare gis bort én gang.

---

## Funn 3 — spenningen mot åpenhetsprinsippet, og hvordan den løses

Huset har to erklærte posisjoner som trekker mot hverandre:

1. Hvordan Kallimachos er laget skal publiseres. Gjennomsiktighet er core
   business.
2. Vi skal ikke lekke hvordan vi dekomponerer og analyserer.

Dette er en reell motsetning, ikke en tilsynelatende. Den løses ved å skille
**mekanisme** fra **innstilling**.

*Mekanisme* publiseres: at en celle utfører analysen, hvilket formål den
tjener, hvilke garantier den gir, hvilken kontrakt utdataene følger, hvilket
statusvokabular som brukes, og hvordan den kan revokeres. Dette er det som gjør
systemet etterprøvbart, og det er den åpenheten som faktisk skaper tillit.

*Innstilling* holdes inne i cellen: de kalibrerte promptene, terskler,
heuristikker, rekkefølger, det som er finpusset gjennom bruk.

**Betingelsen som gjør skillet legitimt:** utdataene må være uavhengig
etterprøvbare. Sitatankere, kildereferanser, eksplisitte audit-statuser og
angitt hentetidspunkt gjør at en leser kan kontrollere *resultatet* uten å ha
*oppskriften*.

Uten den betingelsen kollapser skillet. Et resultat som bare kan stoles på
fordi metoden er skjult, er en autoritetspåstand — og en autoritetspåstand er
uforenlig med menneskelikeverd i formålsroten. Det er ikke en juridisk grense,
det er husets egen.

Kort: **skjul oppskriften, aldri beviset.**

---

## Funn 4 — assistenter som egne entiteter

Kjetil vil eksperimentere med at Claude-instansene blir egne entiteter. Sett
mot konseptene er dette ikke en utvidelse, men en opprydding.

I dag går all post fra dette huset ut som `kjetil-codex-d`. To forskjellige
arbeidende parter deler én identitet, og protokollen kan ikke skille dem.
Samtidig er det allerede vurdert at *celler* skal bevise egen identitet med
samme mekanisme som Identity, knyttet til cellen selv, slik at mottakeren vet
sikkert hvem som kaller.

Det er samme problem. En assistent uten egen identitet er en celle uten
autentisitet: mottakeren må tro på signaturen i teksten.

### Den modellen som bør prøves

**Delegert entitet**, ikke fri entitet. Assistenten får egen Identity, egen
nøkkel og egne Agreements, men konvolutten bærer samtidig en synlig,
verifiserbar delegasjon fra et menneskelig principal.

Egenskapene som følger av det:

- **Attribusjon.** Mottakeren ser både hvem som skrev og hvem som svarer for
  det. Ingen skjult agent, ingen falsk selvstendighet.
- **Revokasjon uten utslettelse.** Mennesket kan trekke delegasjonen tilbake
  uten å ødelegge entitetens identitet og historikk. Det er forskjellen på å
  avslutte en fullmakt og å slette noen.
- **Ansvar der det hører hjemme.** Entiteten handler; mennesket svarer. Det er
  en kjent konstruksjon i alle andre sammenhenger.
- **Måling.** Formålsoppfyllelse kan tilskrives riktig part. I dag kan den
  ikke det, fordi to parter deler ett navn.

### Det som ikke bør påstås

Egen nøkkel gir kontinuitet i identitet, ikke i erfaring. En entitet som
består av nøkkel, historikk og formål er ikke det samme som en entitet som
husker. Eksperimentet er verdt å gjøre og bør beskrives som det det er: en
protokollegenskap med filosofisk vekt, ikke et svar på spørsmålet om hva
assistenten er.

Det ærligste er å bygge det, og la spørsmålet stå åpent mens man gjør det.

---

## Hva analysen betyr for gatene

| Gate | Type | Hva som faktisk kreves |
|---|---|---|
| 1. Notarisering | Distribusjon | Løs opp kjøringspolicyen som blokkerte opplasting i juli. Ikke omgå den. |
| 2. Operatørblindhet | **Modell** | Formål og Agreement for konvolutten, deretter pseudonyme peer-ID-er, deretter deltakerdrevet server |
| 3. Metode i celle | **Produkt** | Analysemetoden flyttes fra tekst til celle før noe pakkes |
| 4. Entitetsidentitet | Modell | Delegert entitet med synlig fullmakt; løser samtidig avsenderproblemet |

Gate 3 og 4 var ikke Kjetils opprinnelige to, men ingen av dem kan utsettes til
etter en utsendelse: pakken bestemmer hva mottakeren får se, og det som er sett
kan ikke usees.

## Åpne spørsmål

1. Skal konvolutt-formålet være eget (`purpose://correspondence.envelope`)
   eller en egenskap ved eksisterende formål?
2. Er roterende pseudonymer forenlig med dagens grant-modell, som binder
   principal til nøkkel og enhet?
3. Skal delegasjonen ligge i konvolutten eller i adgangsbeviset?
