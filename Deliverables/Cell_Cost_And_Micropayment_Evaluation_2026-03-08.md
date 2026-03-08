# Evaluering: kostmodell for celler, CloudBridge og micropayment-enheter

Dato: 2026-03-08

## Kort konklusjon

1. Selve cellen er billig. Instansiering, CPU, RAM og disk for en enkel `GeneralCell` er svært små kostnader.
2. Den største tekniske kostrisikoen er ikke cellen, men dagens outbound CloudBridge-design. `VaporBridgeTransport.setup(...)` oppretter i dag `MultiThreadedEventLoopGroup(numberOfThreads: 2)` per outbound forbindelse. Det gir en fast sesjonskost og dårlig skaleringsprofil.
3. Den største økonomiske kostbarrieren for ekte fiat-micropayments er heller ikke CPU eller disk, men betalingsrailene. Med Stripe Norge sin standard online-pris er faste gebyrer for høye til at man bør gjøre direkte kortbetaling per mikrohandling.
4. Anbefalt modell er å skille mellom:
   - oppgjørsenhet: `NOK` minor units / PSP-oppgjør
   - intern meteringsenhet: langt mindre enn `0.01 NOK`
5. Anbefalt intern enhet er:
   - `1 value_unit = 0.00001 NOK`
6. Hvis dere vil ha presis intern kostakkumulering før avrunding til `value_unit`, bør runtime i tillegg ha:
   - `1 cost_tick = 0.00000001 NOK`

Dette gir en praktisk modell for transparent verdiflyt i egne celler og i celler man får tilgang til via `Agreement`, uten å låse hele systemet til fiatens groveste enhet.

## Teknisk grunnlag i koden

### 1. En celle er ikke en tråd-per-instans-modell

`CellProtocol/Sources/CellBase/Cells/GeneralCell/GeneralCell.swift` viser at `GeneralCell` primært holder:

- schema-dictionaries
- `Agreement`
- `Identity`
- `PassthroughSubject`
- `Intercepts`-actor
- `GeneralAuditor`-actor

Det finnes ikke noe i denne klassen som tilsier én OS-tråd per celle.

### 2. Resolver har delte bakgrunnsoppgaver

`CellProtocol/Sources/CellBase/Cells/CellResolver/CellResolver.swift` viser at `CellResolver` har delte sweep-loops:

- `lifecycleSweepTask`
- `runtimeShadowTask`

Det betyr at livssyklusstyring er delt på resolver-nivå, ikke per celle.

### 3. Persistering er filbasert JSON per celle

`CellProtocol/Sources/CellVapor/FileSystemCreationSpaceStorage.swift` og `CellProtocol/Sources/CellApple/FileSystemCreationSpaceStorage.swift` lagrer celler som:

- `CellsContainer/<uuid>/typedCell.json`

`CellProtocol/Sources/CellBase/PersistingCells/CellPersistenceCrypto.swift` viser at lagring kan krypteres ved hvile via `ChaChaPoly`, styrt av `CellStorageWriteOptions.encryptedAtRestRequired`.

### 4. CloudBridge har i dag en fast outbound-sesjonskost

`CellProtocol/Sources/CellVapor/CloudBridge/VaporBridgeTransport.swift` oppretter i `setup(...)` en ny:

- `MultiThreadedEventLoopGroup(numberOfThreads: 2)`

per outbound WebSocket-forbindelse.

Det er den viktigste kostobservasjonen i hele gjennomgangen. Så lenge outbound bridge ikke deler event-loop-gruppe på tvers av forbindelser, er det misvisende å prise remote verdiutveksling bare per melding eller per CPU-ms. Kostbildet er sesjons- og kapasitetspreget.

## Lokale målinger

### 1. Instansiering av en enkel celle

Målt med en midlertidig Swift-benchmark mot `CellProtocol`:

- 1000 `GeneralCell` instansiert på `0.003507` sekunder
- ca. `285137` celler/sekund
- RSS-økning: `2244608` bytes
- nedre grense-estimat: `2244.6` bytes RAM per celle

Viktig:

- dette er en nedre grense for en enkel `GeneralCell`
- det er ikke et fullverdig mål for celler med tung state, subscriptions, bridge-tilkoblinger eller domenelogikk

### 2. Persistens av en enkel celle

Samme benchmark ga:

- 1000 persisteringer på `0.187575` sekunder
- ca. `5331` writes/sekund
- `1430000` bytes totalt
- ca. `1430` bytes per enkel persistert celle

### 3. Faktiske persisterte celler i live container

Lokal inspeksjon av eksisterende `typedCell.json`-filer ga:

- antall filer: `134`
- snittstørrelse: `3442` bytes
- minste: `2217` bytes
- største: `54765` bytes
- total størrelse: `461226` bytes

Videre:

- `~/CellsContainer` totalt: `728K`
- `CellScaffold/db.sqlite`: `266240` bytes, diskbruk `320K`

Konklusjon:

- en virkelig persistert celle ligger fortsatt i kilobyte-klassen
- disk er ikke det som bestemmer minste økonomiske enhet

## Eksterne prisforutsetninger brukt i regnestykkene

Tallene under er brukt som utgangspunkt og bør oppdateres når dette notatet brukes på nytt:

- ECB referansekurser 2026-03-06:
  - `1 EUR = 1.1561 USD`
  - `1 EUR = 11.1725 NOK`
  - avledet `1 USD = 9.663956 NOK`
- Hetzner Cloud `CX23`:
  - `3.49 EUR/month`
  - `2 vCPU`
  - `4 GB RAM`
  - `40 GB SSD`
- Hetzner Volume Storage:
  - `0.044 EUR/GB/month`
- Cloudflare Workers paid:
  - `$0.30 / 1M requests`
  - `$0.02 / 1M CPU-ms`
- Cloudflare Durable Objects:
  - `$0.15 / 1M requests`
  - `$12.50 / 1M GB-seconds`
  - `$0.20 / GB-month`
- Stripe Norge online-betaling:
  - `2.4% + 2 NOK`

Kildelenker ligger nederst.

## Avledet kostmodell i NOK

### 1. CPU

Hvis man legger hele `CX23`-prisen lineært over `2 vCPU` og en 30-dagers måned:

- `1 vCPU-second ~= 0.000007521610 NOK`
- `1 vCPU-ms ~= 0.000000007522 NOK`

Dette betyr:

- rå CPU-kost er ekstremt liten
- enkel instansiering av en lett celle er langt under én hundredels øre

Nedre grense for instansiering av én benchmarket `GeneralCell` blir omtrent:

- `0.003507 / 1000 = 3.507e-6 sek`
- `3.507e-6 * 0.000007521610 NOK ~= 2.64e-11 NOK`

Det er så lite at det ikke gir mening som egen fiat-avregningsenhet.

### 2. RAM

Lineær RAM-kost fra `CX23`:

- `38.992025 NOK / 4 GB / month`

Brukt mot benchmarkens nedre grense på `2244.6` bytes per celle:

- `RAM-kost per cellemåned ~= 0.000020377760 NOK`

Det tilsvarer:

- ca. `2.04 value_units` hvis `1 value_unit = 0.00001 NOK`

Skalering:

- `100000` slike lette celler i RAM er ca. `214.06 MB`

Konklusjon:

- RAM er fortsatt billig nok til at dere kan ha mange celler i minnet
- men langvarig residency er mer økonomisk relevant enn selve instansieringen

### 3. Disk

Med Hetzner volume-pris:

- persistert virkelig celle på `3442` bytes:
  - `0.000001575847 NOK per cellemåned`
- benchmarket enkel celle på `1430` bytes:
  - `0.000000654695 NOK per cellemåned`

Skalering:

- `1000000` celler a `3442` bytes er ca. `3.2056 GB`

Konklusjon:

- disk er i praksis neglisjerbar som kostdriver for små celler
- det er ingen grunn til å la disk alene bestemme minste micropayment-enhet

### 4. Cloudflare som referanse for delt sky-runtime

Hvis deler av bridge-/edge-laget flyttes til Cloudflare-lignende drift:

- `1 Workers request ~= 0.000002899187 NOK`
- `1 Workers CPU-ms ~= 0.000000193279 NOK`
- `1 Durable Objects request ~= 0.000001449593 NOK`
- `1 aktiv Durable Object-sekund ved 128 MB ~= 0.000015099932 NOK`

Poenget her er ikke at dere må bruke Cloudflare, men at også sky-edge billing ligger langt under `0.01 NOK` per enkelthendelse. Det støtter behovet for en intern meteringsenhet som er mye finere enn fiat minor units.

### 5. CloudBridge i nåværende kodebase

Det går ikke an å gi én ærlig per-melding-pris for dagens outbound CloudBridge uten å være misvisende.

Årsak:

- dagens implementasjon oppretter to event-loop-tråder per outbound forbindelse
- kostnaden blir derfor dominert av sesjonsmodell, ressursreservering og skaleringsgrense
- ikke bare av bytes eller CPU brukt på én enkelt melding

Derfor bør dagens CloudBridge prises som en av disse:

1. fast kapasitet/sesjon
2. tidsbasert reservasjon
3. hybrid: sesjonsavgift + meterte meldinger

Ikke som ren "én melding = x øre".

## Betalingsrailer er mye grovere enn infra

Med Stripe Norge sin standard online-pris:

- fast del: `2 NOK`
- prosentdel: `2.4%`

Eksempler:

- `20 NOK` top-up -> gebyr `2.48 NOK`
- `50 NOK` top-up -> gebyr `3.20 NOK`
- `100 NOK` top-up -> gebyr `4.40 NOK`

Hvis den faste delen alene skal være under:

- `5%` må top-up være minst `40 NOK`
- `3%` må top-up være minst `66.67 NOK`
- `2%` må top-up være minst `100 NOK`

Konklusjon:

- ekte ekstern fiat-micropayment per celleoperasjon er lite realistisk på kortbetaling
- dere må batch'e oppgjør og la den transparente verdiflyten skje i interne enheter

## Hva dette betyr for transparent verdiflyt

### 1. Eide celler og egne runtime-miljøer

For celler man kontrollerer selv er:

- CPU nesten gratis på operasjonsnivå
- disk nesten gratis
- RAM liten, men ikke null over tid

Det betyr at intern verdiflyt bør uttrykke:

- residency over tid
- persistering
- bridge-reservasjon
- audit/replay-behov

ikke bare rå CPU-tid.

### 2. Agreement-tilknyttede celler

For celler man får tilgang til gjennom `Agreement` er verdiflyt naturlig å binde til:

- capabilities
- varighet
- persistenskrav
- bridge/sesjonstype
- eventuelt SLA eller trust-nivå

Det er en mer ærlig modell enn å late som én `Meddle` eller `Absorb` alltid har samme økonomiske kost.

### 3. Nåværende DiMy-modell er en produktpris, ikke en grunn-enhet

`DiMyMicropayments/docs/iterations/ITERATION-11-mvp-prepaid-entity-todo-chat-plan.md` bruker i dag:

- `0.1 NOK = 10 minor units`

Det er en helt grei produktpris for en inngangs-gate, men det er altfor grovt som intern meteringsenhet for transparent verdiflyt på infrastrukturnivå.

## Anbefalt enhetsmodell

### Modell A: anbefalt

- `settlement_minor_units`
  - PSP/fiat-lag
  - eksempel: `NOK`-øre
- `value_units`
  - bruker- og audit-synlig intern meteringsenhet
  - `1 value_unit = 0.00001 NOK`
- `cost_ticks`
  - intern runtime-akkumulator
  - `1 cost_tick = 0.00000001 NOK`
  - `1000 cost_ticks = 1 value_unit`

### Hvorfor `0.00001 NOK` er riktig nivå

1. Den er `1000x` finere enn `0.01 NOK`.
2. En celle som ligger i RAM en hel måned havner rundt `2 value_units`, altså målbart uten å bli absurd detaljert.
3. En persistert cellemåned havner under `1 value_unit`, men kan akkumulere naturlig.
4. En aktiv edge-/object-sekund i en sky-modell havner rundt `1.5 value_units`, altså også målbart.
5. Integer-regnskap holder seg fortsatt håndterbart:
   - `1 NOK = 100000 value_units`

### Hvorfor ikke låse alt til enda mindre synlige enheter

Hvis man gjør den synlige enheten like liten som rå CPU-ms-kost, blir tallene for store og lite lesbare. CPU alene er ikke riktig faktureringsobjekt uansett. Det riktige er:

- bruk fin intern akkumulering
- eksponer en litt grovere, men fortsatt mikrofin, synlig verdi-enhet

## Praktiske anbefalinger

1. Ikke bruk fiat minor units som intern `value_units`-semantikk.
2. Hold `value_units` og `settlement_minor_units` adskilt i modell og API.
3. Akkumuler rå kost i `cost_ticks`, og flush til `value_units` ved terskel eller ved avsluttet operasjon/sesjon.
4. Pris dagens outbound CloudBridge som kapasitet/sesjon, ikke bare som melding.
5. Behold produktpriser som `0.1 NOK` for MVP-gates hvis ønskelig, men forstå dem som produktpolicy, ikke som minste regnskapskorn.
6. For kort/PSP-top-ups bør dere tenke i størrelsesorden `50-100 NOK`, ikke i enkelthendelser på øre- eller sub-øre-nivå.

## Anbefalt neste beslutning

Jeg ville tatt denne beslutningen nå:

1. `value_units` frikobles fra fiat minor units.
2. `1 value_unit = 0.00001 NOK`.
3. `cost_ticks` innføres internt som `0.00000001 NOK`.
4. `0.1 NOK` i DiMy beholdes bare som første produktpris, ikke som universell metering-grunnmur.
5. CloudBridge får senere en egen refaktor hvor outbound forbindelser deler event-loop-gruppe; først da gir det mening å finjustere per-melding-pris.

## Kilder

- ECB reference rates 2026-03-06:
  - https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.pdf
- Hetzner Cloud pricing:
  - https://www.hetzner.com/cloud/
- Hetzner Storage Volumes:
  - https://www.hetzner.com/cloud/#volumes
- Cloudflare Workers pricing:
  - https://developers.cloudflare.com/workers/platform/pricing/
- Cloudflare Durable Objects pricing:
  - https://developers.cloudflare.com/durable-objects/platform/pricing/
- Stripe Norge pricing:
  - https://stripe.com/no/pricing
