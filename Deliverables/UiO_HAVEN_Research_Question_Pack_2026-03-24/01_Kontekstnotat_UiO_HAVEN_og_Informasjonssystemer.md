# Kontekstnotat: UiO, HAVEN og informasjonssystemer

## Formål

Dette notatet gir et felles utgangspunkt for veileder, student og ChatGPT Deep Research når målet er å utvikle gode forskningsspørsmål rundt HAVEN.

## Arbeidslesning av UiO Information Systems-konteksten

En arkivert tekst signert Petter Nielsen som leder for Information Systems-gruppen ved Universitetet i Oslo beskriver gruppen som opptatt av:

- forholdet mellom digitale plattformer, helse og bredere utviklingsprosesser
- governance, deltakende design og systemimplementering
- interventionistiske metoder og action research
- effekter av digitale intervensjoner på praksis, politikk og samfunn
- en sosioteknisk og fortolkende forskningstradisjon

Dette bør leses som en indikativ ramme, ikke som en fullstendig eller bindende beskrivelse av gruppens eksakte prioriteringer i 2026.

Kilde:

- <https://lists.aisnet.org/pipermail/iris_lists.aisnet.org/2021-May/000063.html>

## Hvorfor HAVEN er interessant i en informasjonssystemramme

HAVEN er ikke bare et teknisk system. Det er også et forslag til hvordan digital infrastruktur kan organiseres annerledes. Det gjør HAVEN interessant for informasjonssystemforskning fordi systemet berører:

- hvordan tilgang gis og begrunnes
- hvordan data deles uten global identitet eller skjult profilering
- hvordan verdiskaping og verdifordeling kan synliggjøres
- hvordan styring og legitimitet kan bygges uten sentralisert plattformmakt
- hvordan brukere, fellesskap og institusjoner kan samhandle gjennom eksplisitte regler

HAVEN passer derfor godt som et objekt for sosioteknisk analyse, ikke bare som et implementeringsprosjekt.

## Sentrale HAVEN-begreper som er forskningsmessig viktige

### 1. CellProtocol som minimal og deterministisk modell

HAVEN beskriver en privacy-first, replaybar og kontraktsbasert modell for distribuerte systemer. Dette gjør det mulig å studere hvordan teknisk arkitektur kan bakes sammen med normative idealer som transparens, revisjonsspor og brukerautonomi.

### 2. Domain-scoped identity

Identitet i HAVEN er eksplisitt, kryptografisk og domenespesifikk. Systemet avviser ideen om en global konto som følger brukeren på tvers av sammenhenger. Dette åpner for forskning på balansen mellom personvern, koordinering og ansvarlighet.

### 3. Agreements og Contracts

Tilgang i HAVEN er ikke implisitt. Den må forespørres, vurderes og gis eksplisitt. Dette gjør HAVEN relevant for forskning på governance, autorisasjon, legitimitet og institusjonelt design.

### 4. Flows, replay og audit

All observerbar adferd uttrykkes som replaybare hendelsesstrømmer. Dette gjør HAVEN interessant for forskning på gjennomsiktighet, revisjon, forklarbarhet og sporbarhet i digitale infrastrukturer.

### 5. Purpose og Interests

HAVEN legger opp til at intensjon og formål kan deklareres eksplisitt, i stedet for å utledes gjennom overvåking, scoring eller atferdsprofilering. Dette er viktig for forskning på tillit, koordinering, demokratisk styring og alternative plattformlogikker.

### 6. Local-first og transportuavhengighet

HAVEN er tenkt som en bruker-eid og semantisk stabil infrastruktur som kan fungere lokalt, distribuert, peer-to-peer og på tvers av broer og transportsjikt. Dette inviterer til forskning på digital allmenning, robusthet, lokalt eierskap og institusjonell forankring.

## Problemrom denne pakken retter seg mot

Denne pakken prioriterer fem overlappende problemrom:

- gjennomsiktighet i verdiflyt
- verdigenerering som starter fra individet
- data som del av en digital allmenning
- HAVEN som demokratisk plattform
- forskyvning av verdi og makt fra selskaper til brukerne som eiere

## Hvordan problemrommene kan oversettes til informasjonssystemforskning

### Transparent verdiflyt

Spørsmålet er ikke bare om verdiflyt kan måles teknisk, men hvordan den blir sosialt begripelig, legitim og styrbar for brukere, fellesskap og institusjoner.

### Individ-først verdiskaping

Her er kjernespørsmålet om systemer kan designes slik at verdi først oppstår hos, eller tilskrives, brukeren og brukerens relasjoner, heller enn at plattformen samler og ekstrakterer verdi sentralt.

### Den digitale allmenningen

Her blir HAVEN interessant som et mulig rammeverk for datadeling, databruk og datastyring der data ikke automatisk blir privat plattformkapital, men heller forvaltes gjennom regler, samtykke, kontrakter og fellesskapsmekanismer.

### Demokratisk plattform

Dette problemrommet handler om hvordan beslutninger, moderering, deltakelse og ansvar kan organiseres på en måte som er etterprøvbar, personvernbevarende og mindre avhengig av opaque plattformlogikk.

### Maktforskyvning

Dette er et politisk-økonomisk spørsmål: Hva skjer med verdikjeder, lock-in, forhandlingsmakt og institusjonelle roller dersom brukerne selv eier infrastrukturelle byggesteiner?

## Forskningstilnærminger som passer godt

Følgende tilnærminger er spesielt relevante:

- fortolkende case-studier
- komparative plattformstudier
- design science og prototypeevaluering
- participatory design
- governance- og policyanalyse
- interventionistiske eller workshop-baserte opplegg

## Viktige forsiktighetsmomenter

1. Ikke anta at teknisk transparens automatisk gir sosial legitimitet.
2. Ikke anta at bruker-eierskap automatisk gir rettferdighet eller fravær av konflikt.
3. Skill mellom hva HAVEN hevder normativt og hva som kan vises empirisk.
4. Hvis empirien rundt HAVEN er begrenset, bruk HAVEN som designforslag, analytisk kontrast eller prototypisk case.
5. Formuler oppgaver slik at de kan gjennomføres innenfor en masterstudents tids- og datarammer.

## HAVEN-dokumenter som bør behandles som kjernegrunnlag

- `Book/01_CellProtocol_Core.md`
- `Book/03_Identity_Model.md`
- `Book/04_Agreements_Contracts.md`
- `Book/05_Flows_Lifecycle.md`
- `Book/06_CellResolver.md`
- `Book/08_Bridging_Transport.md`
- `Book/09_Purpose_Interests.md`

## Kort oppsummering

HAVEN er spesielt interessant som forskningsobjekt dersom dere vil utvikle oppgaver som kombinerer:

- teknisk arkitektur
- styring og institusjoner
- brukerautonomi
- datadeling og personvern
- demokratisk koordinering
- alternativ plattformokonomi

Det mest lovende grepet er ofte å bruke HAVEN som et gjennomtenkt designforslag for å stille bedre informasjonssystemspørsmål, ikke bare som et system som skal beskrives teknisk.
