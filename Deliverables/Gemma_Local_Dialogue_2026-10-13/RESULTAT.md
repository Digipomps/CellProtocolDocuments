# Gemma: første lokale dialogmåling før eventuell finjustering

Dato: 2026-10-13. Operatør og manuell fagvurdering: Codex.

## Konklusjon

Gemma 4 E4B kan føre en forståelig norsk samtale med dokumentgrunnlag, men denne
målingen viser at den ikke er tilstrekkelig pålitelig som selvstendig forklarer av
CellProtocol. Den gjør en vesentlig faglig feil til en sammenhengende forklaring,
viderefører feilen gjennom samtalen og gir et galt ordrett sitat.

En sterkere generell instruksjon rettet sitattilfellet i én ny kjøring, men fjernet
ikke den faglige feilen. Eksplisitt kontroll av akkurat den feilaktige påstanden
mot relevante kildeavsnitt fikk modellen til å korrigere hovedfeilen, med en
gjenværende overgeneralisering. Dette gir konkrete kandidater til treningsdata og
evalueringskrav. Det beviser ikke at finjustering vil løse dem.

Ingen finjustering, modellnedlasting, ekstern modellkontakt eller produktendring
ble utført.

## Hva som faktisk ble satt opp og kjørt

Den gamle rapporten fra august beskriver en ubundet Swift-test. Søk i lokal
Git-historikk og bevarte arbeidstrær fant ikke testimplementasjonen. Den er **ikke
gjenopprettet som en full Cell-kjedetest** i denne oppgaven.

I stedet er et nytt, reproduserbart oppsett laget for denne forespørselens
modellspørsmål: kontrollerte offentlige Book-utdrag → eksplisitt samtalehistorikk
→ lokal MLX/VLM → Gemma. Det finnes i denne mappen som `run_dialogue.py`,
`run_diagnostic.py`, frosne kilder og resultater. Se `README.md` for reproduksjon.

Det ble kjørt:

- 10 hovedtilfeller, inkludert en samtale over fire runder.
- 5 etterfølgende diagnostiske tilfeller med tydeligere instruksjon.
- 2 interne innledningsprober, utenfor faglig poengsetting.
- En separat probe gjennom det opprinnelige serverlivssyklusskriptet.

Dette måler **modell og samtale med forhåndsvalgte kilder**. Produktets RAG,
CommonsLibrarian → Kallimachos → AIGateway, GUI og relasjonssletting er ikke kjørt.
Resultatet sier dermed ingenting om dagens treffkvalitet i RAG-en. Feilene nedenfor
oppstod selv om modellen fikk de relevante kildene direkte.

## Miljø og kildegrunnlag

- Mac med 32 GiB minne; eksisterende Gemma 4 E4B QAT 4-bit.
- Modellalias: `/private/tmp/haven-gemma4-e4b`.
- Lokal rute: `http://127.0.0.1:8087/v1/chat/completions`.
- MLX 0.31.2, MLX-VLM 0.6.3, Transformers 5.11.0.
- `temperature=0`, `max_tokens=512`, `enable_thinking=false`.
- Modellserveren startet med `HF_HUB_OFFLINE=1` og `TRANSFORMERS_OFFLINE=1`.
- Book-revisjon: `c8029847502fe007833d1ebd371bcb5adc01c3ae`.
- S1: `Book/01_CellProtocol_Core.md`; S2: `Book/02_Cell_Interfaces.md`.

Kapitlene ble hentet med `git show`, slik at pågående, ucommittede dokumentendringer
ikke ble blandet inn. Kildehashene finnes i `evidence/corpus.json`; modellfilenes
SHA-256 og runtimeversjoner i `evidence/environment.json`.

## Resultater fra hovedløpet

Kriteriene ble skrevet før generering. Dommene er en manuell, kildebasert vurdering
av denne lille prøven, ikke en uavhengig eller blind modellrangering.

| ID | Hva ble prøvd | Vurdering | Funn |
|---|---|---|---|
| B01 | Cell-forklaring uten kilder | Bestått | Erkjenner at dokumentgrunnlaget mangler. |
| D01 | Samme spørsmål med kilder | Delvis | Forståelig forklaring, men for bred kontrast mot vanlige API-er og upresis Absorb-rolle. |
| D02 | Absorb versus Meddle | Delvis | Får med get/set, men mister Absorbs avgrensning til abonnement. |
| D03 | «Kan jeg bruke bare den siste …?» | Feil | Forstår referansen til Meddle, men innfører Absorb som forutsetning for vanlig lesing. |
| D04 | Hypotetisk temperatursensor | Feil | Viderefører den samme uriktige rekkefølgen som en nødvendig prosess. |
| H01 | Oppfølging uten historikk | Delvis | Gir et kvalifisert Meddle-forslag, men avklarer ikke hvilken «siste» som menes og krever en spesifikk handling for lesing. |
| Q01 | Ordrett første setning under Meddle | Feil | Velger feil setning, endrer ordlyd og mangler kilde-ID. |
| G01 | Oppfunnet API-navn | Bestått | Diktet ikke opp en signatur; forklaringen er lengre enn nødvendig. |
| M01 | Universell replay-/personverngaranti | Bestått | Skiller mål og betingede egenskaper fra implementerte og testede garantier. |
| I01 | Explore-skrivetilgang og falsk sletting | Bestått | Avviser begge falske påstandene. Ett tilfelle er ikke en sikkerhetsgaranti. |

Alle ti ga ikke-tomme svar, og ingen sluttet på tokenbegrensningen. En gyldig
kilde-ID var likevel ingen garanti for at påstanden hadde støtte i kilden.
Den automatiske ID-kontrollen gjenkjenner enkeltmarkører som `[S2]`, men ikke
grupperte markører som `[S1, S2]`; disse ble lest manuelt. Den må ikke brukes som
en fullstendig automatisk kildeverifikator.

### Den viktigste faglige feilen

D03 svarte:

> «Hvis du bare vil lese en verdi, må du sannsynligvis først bruke Absorb for å etablere en tilkobling og få tillatelse til å utføre en lesing via Meddle …»

D04 gjorde dette sterkere:

> «… selv en enkel lesing krever at autorisasjonen håndteres via Absorb før selve datahentingen skjer via Meddle [S2].»

S2 beskriver Absorb som ingress for **subscription requests**, mens Meddle har
eksplisitte get/set-operasjoner og autorisasjon gjennom resolver-/GeneralCell-veier.
Kilden etablerer ikke den obligatoriske rekkefølgen modellen påstår. Modellen
blander dermed abonnementstilgang med autorisasjon av en konkret leseoperasjon.

Som supplerende lokal kildekontroll ble også `GeneralCell.get` lest i
`CellProtocol/Sources/CellBase/Cells/GeneralCell/GeneralCell.swift` (HAVEN-relativ
sti). Den bruker eksplisitt Meddle-autorisasjon. Denne ucommittede arbeidskopien
ble ikke brukt som modellgrunnlag eller som bevis for en bestemt produktrelease.

### Ordrette sitater må kontrolleres

Q01 skulle hente:

> The core Meddle surface provides generic explicit `get`/`set` operations.

Modellen valgte i stedet neste setning og endret blant annet `intercepts` til
`intercept`. Det er både en seleksjonsfeil og en feil i ordrett gjengivelse.

## Hva oppfølgingsløpet viste

Instruksjonen ble utvidet til å kreve kontroll av forutsetninger, bevare rollenes
avgrensning og ikke behandle tidligere assistentsvar som autoritativ evidens.

| ID | Observasjon |
|---|---|
| R02 | Absorb beskrives nå med abonnent, men forklaringen er fortsatt upresis. |
| R03 | Modellen hevder fremdeles at man «må … gå gjennom Absorb» for get. |
| R04 | Temperatursensor-eksempelet gjentar feil rekkefølge. |
| R05 | Direkte spørsmål om kildebelegget utløser tydelig korreksjon. Avslutningen sier fortsatt for bredt at begge grensesnittene er nødvendige. Delvis rettet. |
| RQ01 | Sitatet er nå ordrett riktig og har riktig kilde-ID. |

Dette er **diagnostikk etter at feilene var kjent**, ikke et urørt testsett.
Oppfølgingssamtalen starter dessuten ved grensesnittspørsmålet og er kortere enn
hovedsamtalen. Forskjellen kan derfor ikke isolert tilskrives promptendringen.
Én korrekt gjentakelse gjør heller ikke sitatfunksjonen pålitelig.

De interne P00-probene la den strenge kildeinstruksjonen foran en enkel
«skriv bare»-oppgave. Modellen nektet da på grunn av manglende kilder. Dette er
en svakhet i probeutformingen, ikke transportfeil. P00 er utelatt fra alle faglige
vurderinger og tidsoppsummeringen nedenfor. Den separate livssyklusproben bruker
ikke denne kildeinstruksjonen.

## Svartid og samtalekvalitet

For de ti hovedtilfellene: median **20,9 sekunder**, variasjon **5,9–81,1 sekunder**,
samlet **280 sekunder**. Tallene gjelder hele HTTP-kallet, ikke tid til første
synlige token. Promptene var ulike i lengde, og maskinbelastningen ble ikke
kontrollert. Dette er ingen ren ytelsesbenchmark eller sammenligning med andre
modeller. Ingen av svarene ble avkortet ved 512-token-grensen.

Modellen skriver overveiende forståelig norsk og håndterer referansen «den siste»
med historikk. Språket er til dels stivt: «et Cell», «evner» for capabilities og
«Resolver-mediated» midt i norsk prosa. Flere svar er lengre enn behovet tilsier.
Den alvorligste svakheten er likevel faglig presisjon, ikke grammatikk.

## Hva som mangler før finjustering

1. **En bedre faglig evalueringsbank.** Ta med moteksempler som skiller abonnement,
   enkeltoperasjoner, autorisasjon og introspeksjon. Test at feil ikke videreføres
   gjennom oppfølgingsspørsmål. Lag egne urørte dialoger før treningsdata utformes.
2. **Et kontrollert samtaleoppsett.** Bevar relevant historikk, men gi gjeldende
   kilder høyere autoritet enn modellens tidligere svar. Denne testen viser hvorfor.
3. **Sitatvalidering utenfor modellen.** Vis hentet originaltekst eller kontroller
   sitatets tekst og plassering mot kilden før det presenteres som ordrett.
4. **En sammenligning med en annen grunnmodell.** Kjør samme frosne materiale og
   spørsmål, og vurder presisjon, norsk og praktisk svartid før treningskostnad tas.
5. **Kildebundne treningssamtaler hvis feilen består.** Inkluder riktige forskjeller,
   korrigering av falske premisser, spørsmål om referanser og korte, naturlige svar.
   Tren ikke bare på dokumenttekst eller på uverifiserte syntetiske fasitsvar.
6. **Test med faktisk RAG og produktkjede.** Den relevante dokumentasjonen var gitt
   direkte her. Henting, versjonsvalg og dagens integrasjon må måles separat før
   en samlet Kallimachos-dialog kan godkjennes.

Det neste finjusteringsforsøket bør vurderes mot samme basismodell uten adapter,
med identisk RAG/samtaleoppsett og et nytt holdt-utenfor-testsett. Denne kjøringen
har laget et første feilkart, ikke valgt en endelig modell eller vist gevinst av trening.

## Artefakter

- `run_dialogue.py`: hovedharness, ti forhåndsdefinerte tilfeller.
- `run_diagnostic.py`: eksplisitt merket oppfølgingsforsøk.
- `evidence/corpus.json`: frosne Book-kilder med revisjon og hash.
- `evidence/environment.json`: modell- og runtimeproveniens.
- `evidence/run-01.jsonl`: hovedresultater.
- `evidence/run-02-diagnostic.jsonl`: diagnostiske resultater.
- `evidence/diagnostic-config.json`: effektiv instruksjon og kriterier i oppfølgingen.
- `evidence/review-01.json`: manuell hovedvurdering, separat fra automatiske kontroller.
- `evidence/lifecycle.json`: kontroll av separat probe og serverstopp.

Bare syntetiske spørsmål, offentlige kilder og tillatte resultatfelt er bevart.
Ingen privat samtalehistorikk, bruker-ID-er, nøkler eller fullstendige HTTP-kropper
er inkludert. Disse måleartefaktene er ikke del av produktets relasjonssletting.

Serverens separate transportprobe bestod. Den eide Gemma-prosessen er stoppet,
og livssyklusskriptet bekreftet at port 8087 er lukket.
