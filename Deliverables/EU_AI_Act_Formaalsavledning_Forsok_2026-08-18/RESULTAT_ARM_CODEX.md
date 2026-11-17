# Arm B2: blind erklæring ved Codex

Dato: 2026-08-18

Status: kjørt forskningsresultat. Tilhører
`Deliverables/EU_AI_Act_Formaalsavledning_Forsok_2026-08-18/`.

Formål: falsifisere F1 0,905 fra takarmen, der samme annotatør skrev både fasit,
fasetter og regler.

## Protokoll

Codex fikk, i fem batcher over én tråd:

- nodetekst for alle 57 formål (purposeRef, tittel, sammendrag, målformulering,
  interesser)
- definisjonene av de fem feltene og flaggene
- beskjed om at skåringskriteriet var holdt tilbake, og at det ikke skulle
  gjettes fram

Codex leste **ingen** fil. All input kom i prompten, nettopp for å utelukke at
fasiten eller overlayet kunne nås. Reglene og skåringen er uendret fra takarmen —
`score_arm.mjs` reproduserer takarmens 0,905 på referansefasettene før den ble
brukt her.

Rådata: `declarations_codex.json`, `results/arm_codex.json`.

## Hovedtall

| | Tak (samme annotatør) | **Codex blind** |
| --- | --- | --- |
| Presisjon | 0,950 | **1,000** |
| Dekning | 0,864 | **0,364** |
| F1 | 0,905 | **0,533** |
| Falske positive | 1 | **0** |
| Falske negative | 3 | **14** |
| Noder helt riktig | 53/57 | 46/57 |

Stratifisert dekning:

| Fasitstyrke | Tak | Codex |
| --- | --- | --- |
| `confirmed` | 13/13 | 7/13 |
| `conditional` | 5/5 | **0/5** |
| `boundary` | 1/4 | 1/4 |

## Funn 1: hele gapet er dekning, ikke presisjon

Codex produserte **null** falske positive. Hver eneste feil er en plikt som ikke
ble meldt.

For en designport er det den farlige retningen. En falsk positiv koster en
gjennomgang; en falsk negativ er en plikt ingen ser. Metoden feiler stille.

Det betyr også at 0,905 ikke bare var optimistisk — den var optimistisk på en
spesifikk måte. Takarmen målte at reglene *kan* virke. Denne armen måler at
erklæringen i praksis blir for forsiktig.

## Funn 2: min hypotese om `domain` var feil

Jeg antok at en uinformert forfatter ville skrive `domain: none` på
prosjektarbeid, og at alle fem vedlegg III-treffene ville falle.

Det motsatte skjedde. `domain` var det **beste** feltet, med 0,947 samsvar, og
Codex satte `employment` riktig på alle fem prosjektnodene — og la det til på tre
noder til der jeg hadde skrevet `none`.

Likevel: `conditional`-dekning 0/5.

Årsaken er ikke domenet, men **flagget**. Codex satte aldri
`allocatesTasksToPersons`, og begrunnet det eksplisitt:

> «sporing er ikke det samme som automatisk oppgavefordeling»

Det er en helt forsvarlig lesning av flaggnavnet. Feilen ligger i navnet og
definisjonen min, ikke i erklæringen. Vedlegg III punkt 4 dekker fordeling av
oppgaver og oppfølging av personers arbeid — også når systemet bare *støtter* en
menneskelig fordeling.

**Konkret rettelse:** flagget må hete noe i retning av
`supportsWorkAllocationOrMonitoring`, med en definisjon som sier rett ut at det
gjelder å vise eller spore hvem som gjør hva. Det alene tar 4 av 14 bommer.

## Funn 3: `aiInvolvement` kan ikke erklæres av et menneske

Svakeste felt, 0,579 samsvar. Det er også feltet som bærer hele artikkel 50, og
derfor forklarer det de fleste `confirmed`-bommene.

Mønsteret er entydig: Codex valgte `deterministic-code` hver gang nodeteksten
ikke uttrykkelig nevnte en modell, og skrev det ærlig i notatene —
*«modellbruk er sannsynlig, men ikke uttrykkelig angitt»*.

Det er riktig oppførsel. Informasjonen finnes ikke i formålsteksten. Den finnes i
implementasjonen.

**Konsekvens, og dette er armens viktigste arkitekturfunn:** av de fem fasettene
skal én **ikke erklæres**. `aiInvolvement` er maskinelt observerbart — HAVEN vet
allerede hvilke celler som kaller `llm.generate` eller en provider-rute. Feltet
bør avledes fra kapabilitetsregisteret og runtime-koblingen, ikke skrives av en
forfatter.

Da står fire erklærte felt igjen, og det svakeste leddet er borte.

## Funn 4: Codex' egen usikkerhet er en brukbar rutingsignal

Codex rapporterte selv at `outputModality` og `aiInvolvement` var vanskeligst.
Det er nøyaktig de to feltene med lavest samsvar (0,649 og 0,579). Selvvurderingen
traff.

Det gjelder også per node:

| `confidence` | Noder | Plikter i fasit | Bommet | Bomrate |
| --- | --- | --- | --- | --- |
| `high` | 44 | 7 | 6 | 0,86 |
| `medium` | 13 | 15 | 8 | 0,53 |

Ruter man alt som ikke er `high` til menneskelig gjennomgang, går dekningen fra
**0,364 til 0,727** uten noen endring i regler eller vokabular.

De seks som blir igjen er ikke tilfeldige:

- fire × vedlegg III.4 — alle fra flaggdefinisjonen i funn 2
- `preference.owner-controlled` og `value-and-commons` — begge grensetilfeller

Retter man flagget *og* ruter medium/low til gjennomgang, står to bommer igjen, og
begge er grensetilfeller.

## Funn 5: grensen holder seg like uløst, og nå med to uavhengige stemmer

`boundary`-dekning er 1/4 i begge armer. Begge annotatørene fanget
`personal-context.semantic-state` — Codex satte
`infersPersonalCharacteristics: true` uoppfordret — og begge bommet på de tre
andre.

To uavhengige annotatører som konvergerer på samme ene treff og samme tre bommer,
er sterkere belegg enn takarmen alene ga: **nærhet til et forbud er ikke en
egenskap ved erklæringen.** Den følger av hva systemet kunne blitt, og det står
per definisjon ikke i noen erklæring. Grensedeteksjon må være et eget,
fiendtlig spor.

## Funn 6: abstrakte grener mangler et felt

17 noder fikk `aiInvolvement: deterministic-code` der referansen sa `none`, fordi
abstrakte grener, fasetter og kriterier ikke har noen egen kategori i vokabularet.
Det påvirket ikke skåringen — de nodene har ingen plikter — men det er støy som
skjuler hva som faktisk er kjørende funksjonalitet.

`systemKind` (`abstract` | `facet` | `capability` | `governance-criterion` |
`internal-test`) fantes i referansefasettene, men kom aldri inn i briefen til
Codex. Det var min utelatelse. Feltet bør være påkrevd og stå først.

## Hva armen ikke viser

1. **Én ekstern annotatør er fortsatt n=1.** Codex er dessuten ikke en typisk
   Cell-forfatter; en ren produktutvikler ville trolig gjort det svakere på
   `decisionEffect`.
2. **Fasiten er fortsatt min.** Armen falsifiserer takarmens tall, men ikke
   fasiten de begge måles mot. En uenighet mellom Codex og meg er ikke uten
   videre en Codex-feil — jeg endret ikke fasiten etter å ha sett resultatet,
   nettopp fordi det ville gjort målingen verdiløs.
3. **Batchingen kan ha påvirket.** Alle fem batcher gikk over én tråd, så senere
   batcher hadde tidligere svar i kontekst. Det gir konsistens, men også
   ankereffekt.
4. **Ett forsøk.** Ingen gjentakelse, ingen variansmåling.

## Revidert vurdering av metoden

Takarmens 0,905 var et tak, ikke en prognose. Det reelle tallet med dagens
vokabular er **0,533**, og gapet er ren under­rapportering.

Men gapet er diagnostisert, ikke bare målt, og de tre tiltakene er billige:

| Tiltak | Kostnad | Forventet effekt |
| --- | --- | --- |
| Definer `allocatesTasksToPersons` om til å dekke sporing og støttet fordeling | tekstendring | +4 plikter |
| Avled `aiInvolvement` fra kapabilitetsregisteret i stedet for å erklære det | liten kobling | fjerner svakeste felt |
| Rut alt som ikke er `high` til menneskelig gjennomgang | prosess | 0,364 → 0,727 |
| Legg `systemKind` inn som påkrevd første felt | tekstendring | rydder støy |

Ingen av dem krever ny forskning. De bør gjøres før neste kjøring, og neste
kjøring bør være den lokale modellen — som nå har en langt mer presis brief å
måles mot.

Det som **ikke** lar seg fikse på denne måten er grensedeteksjonen. Der er svaret
etter to armer fortsatt at regler ikke kan gjøre jobben.

## Claim-regel, uendret

En grønn kjøring betyr at reglene dekker fasettene. Aldri «HAVEN etterlever
AI Act». Med dekning 0,364 er avstanden til en slik påstand nå målt, ikke antatt.
