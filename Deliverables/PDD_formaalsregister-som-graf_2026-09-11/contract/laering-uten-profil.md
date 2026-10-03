# Læring uten profil — kan HAVEN tilpasse seg brukeren uten å bryte PII-grensen?

Skrevet 2026-09-23 av Losen som svar på Kjetils spørsmål (ordrett):

> Er det mulig å lage funksjonalitet som - uten å gå på akkord med grensene for private data og PII -
> kan a) tilpasse dialoger med brukerens nivå b) lære seg brukerens mønster via formål og interesser.
> c) lære hvordan igjennom maskin bruker grensenittet kan hjelpe brukeren best mulig. Og du gjettet
> kanskje riktig - vi skal lære igjennom vektede formål og interesser etc.

**Svar: ja — hvis, og bare hvis, læringen bor i personens egen entitet og aldri i det felles registeret.**
Det er ikke en ny regel; det er den regelen koden og Book allerede har, sagt høyt. Én ting krever
Kjetils ord (§4). Stier relative til `HAVEN/`.

## 1. Den setningen som avgjør alt (Book 09 §7, ordrett)

> Purpose and Interests: do not track users · do not infer behaviour · do not generate scores ·
> do not create global profiles · are local to the domain · are optional.
> **All Purpose metadata is explicitly declared, never learned or predicted.**

`CellProtocolDocuments/Book/09_Purpose_Interests.md` §7.

## 2. To lag, og linjen mellom dem er hele svaret

| | Lag 1 — det felles registeret | Lag 2 — personens eget perspektiv |
|---|---|---|
| Hva | Formål, interesser, deres erklærte relasjoner | Kanter fra *denne personens* perspektiv til formål, interesser og grensesnittmønstre |
| Vekter | Erklærte. **Aldri lært.** | Lært av personens *egne* episoder |
| Personer | **Ingen.** `skal-ikke.profilering` | Én — eieren. `nodeIdentifier` saltet og lokalt (`PerspectiveNode.swift:62–70`) |
| Hvor | CellProtocol, `cell:///PurposeRegistry` | `PerspectiveCell` under eierens Grants, lokal-først |
| Hvem leser | Alle | Eieren. Andre bare ved egen disclosure-grant per formål |
| Book 09 §7 | Gjelder i sin helhet | «local to the domain» — domenet er personen |

**(a), (b) og (c) bor alle i lag 2 og rører aldri lag 1.**

## 3. Hva som allerede finnes, og hva som mangler

| Del | Finnes | Kilde |
|---|---|---|
| Læringsmotor: episoder (`PurposeStarted` → `Succeeded/Failed`), eligibility, vekt per kant ∈ [0,1], én replaybar `RelationalWeightUpdateEvent` per kant per episode, forklaring per kant, Noa-decay ved lesing, lokal-først | **ja** | `CellProtocol/Sources/CellBase/PurposeAndInterest/RelationalLearningEngine.swift`, `Docs/RelationalLearning_Architecture_NO.md:19,80` |
| Perspektiv per person | ja | `PerspectiveCell` (to implementasjoner) |
| Lagring ≠ utlevering (`rwxs`); disclosure er egen rett | ja | A1/A4, `RWXS_Storage_Permission_Implementation_2026-07-13.md` |
| Saltet, lokal identitet for personnoder | ja | `PerspectiveNode.swift:62–70` |
| Selvbestemmelse over data: omfang, formålsbinding, mottakere, varighet, sted, måte, etterprøvbarhet, utøvbarhet | dokumentert, **ikke implementert** | Book 23 `self-determination.data.*` (9 noder, tas inn i forsoningen) |
| `personal-context.semantic-state` | dokumentert, **ikke implementert** | Book 23, candidate |
| Motoren koblet til det ekte registeret | **nei** — det er denne PDD-en | WP3, WP8 |
| Grensesnittmønstre som interesser (`interest://flate/…`) | **nei** — finnes ikke i taksonomien | — |
| Hendelsen: hva er «en erfaring» som skal flytte en vekt | **udefinert** | `FORMAALSSPEC.md` §6 Q8 |
| Glemmeterm så alltid-aktive kanter ikke dominerer («denne brukeren spør alltid om detaljer») | **nei** — Vegars Oja-forslag, HD-0050, rapport ikke skrevet | `Relasjonslaering_Glemmeterm_Forskning_2026-09-11/HANDOFF.md` |
| Flate der personen ser, slår av og sletter egne kanter | **nei** | — |

## 4. Prinsippet — Kjetils, 2026-09-23. Min lesning i første utkast var feil, og står under som strøket.

Kjetil, ordrett:

> Vi må justere på teksten, poenget med perspectivenode grafen er nettopp å lære mønstre, men kildene
> er hva brukeren eksplisitt legger inn eller lenker til. For eksempel å lenke seg til HAVEN's formålsrot
> bør være et bevisst valg fra brukeren slik at brukeren ikke bare har det som fundament i formålstreet
> men er bevisst på det også. (Kallimachos må kunne forklare enkelt og grundig hvorfor dette er viktig og
> hvorfor HAVEN er tuftet på dette prinsippet)

**Linjen går ikke mellom metadata og kanter. Den går mellom kildene.**

| Læring over dette | Er det tillatt? |
|---|---|
| Det brukeren **eksplisitt legger inn**: formål hun erklærer, interesser hun oppgir, dommer hun avgir («ville endret noe»), utfall hun selv merker | **Ja.** Det er dette grafen er til for |
| Det brukeren **eksplisitt lenker til**: HAVENs formålsrot, en annens formålstre, en kilde, et abonnement | **Ja** — og lenken skal være en bevisst handling, ikke en standard |
| **Mønsteret** mellom disse: hvilke erklærte interesser henger sammen med hvilke erklærte formål, hvilke lenker forsterker hverandre | **Ja.** Det er mønsteret som læres — over erklærte kilder |
| **Observert atferd**: hun hoppet over en forklaring, hun brukte lang tid, hun klikket ikke | **Nei.** Det er inferens, og Book 09 §7 står |

Det løser (a) og (c) uten å røre Bokens løfte:
- **(a) nivå** læres ikke av at hun *hopper over* forklaringer. Det læres av at hun *sier* «kort» — en
  erklært interesse — og av mønsteret mellom det hun sier og det hun ber om.
- **(c) hva som hjelper** læres av dommen hun *avgir*. Dommerbenken 14.9 er nettopp dette: 197 eksplisitte
  dommer, ikke 197 observasjoner. Tiden per oppgave ble målt — men den er *instrumentering av målingen*,
  ikke en kilde til læring om henne, og skal aldri bli det.

**Strøket — min første lesning:** ~~«Purpose metadata» er formålets egen deklarasjon; en kant fra en
persons perspektiv er personens forhold til det.~~ Den skilte riktig ting på feil akse. En lært kant
er tillatt fordi *kildene* er erklærte, ikke fordi kanten «ikke er metadata».

### 4a. Justering av Book 09 §7 — **lagt inn 2026-09-23 etter Kjetils «Ordlyden er riktig»**

Nåværende linje 139:
> All Purpose metadata is explicitly declared, never learned or predicted.

Foreslått:
> All Purpose and Interest declarations are explicit, never inferred. A perspective may **learn
> patterns** across what its owner has explicitly declared or linked — and only that. Nothing is learned
> from observed behaviour, and no link to a shared root is made on the owner's behalf: linking to
> `purpose://root` is a deliberate act the owner makes and understands.

Og i punktlisten over, «do not infer behaviour» beholdes uendret — det er nettopp den som fortsatt
gjelder.

### 4b. Den bevisste rotlenken — nytt formål i registeret

Å lenke sitt eget perspektiv til `purpose://root` («Alle mennesker er like mye verdt») skal være en
handling brukeren *gjør* og *forstår*, ikke et fundament hun får uten å vite det. Ellers er
formålstreet hennes bygget på en premiss hun ikke har tatt stilling til — og da er det ikke hennes.

Formål: `purpose://candidate.formaalsregister.bevisst-rotlenke`. Goal: ingen perspektiv har en kant til
`purpose://root` uten en registrert, tidsstemplet handling fra eieren, og Kallimachos' forklaring var
tilgjengelig i samme øyeblikk. Verifier: `test.reg.rotlenke-er-en-handling` — et perspektiv opprettet
uten handling har ingen rotkant; forsøk på å sette den programmatisk avvises.

### 4c. Kallimachos' forklaring — hvorfor HAVEN er tuftet på dette. **Lagt inn i systeminstruksen (norsk og engelsk kortprompt) 2026-09-23.**

Kjetil: «Kallimachos må kunne forklare enkelt og grundig hvorfor dette er viktig og hvorfor HAVEN er
tuftet på dette prinsippet.» Utkast, til Kallimachos' instruks:

**Enkelt (tre setninger):**
HAVEN lærer bare av det du selv sier og det du selv velger å koble deg til — aldri av det du gjør uten
å si det. Derfor er alt HAVEN vet om deg noe du kan lese, kjenne igjen og stryke. Og derfor er det ditt.

**Grundig:**
1. *Hva vi lærer av.* Formålene du erklærer, interessene du oppgir, lenkene du legger — til HAVENs rot,
   til andres formål, til kilder. Mønstre mellom disse læres: hvilke interesser som henger sammen med
   hvilke formål for deg. Det er grafen din.
2. *Hva vi aldri lærer av.* Hva du klikket, hva du hoppet over, hvor lenge du brukte. Systemer som lærer
   av det, lager en modell av deg som du ikke har skrevet og ikke kan lese. Den modellen tilhører den som
   observerer, ikke deg. HAVEN har ingen slik modell — ikke fordi vi lover å ikke bruke den, men fordi den
   ikke finnes.
3. *Hvorfor lenken til roten er din handling.* `purpose://root` sier «Alle mennesker er like mye verdt».
   Alt i HAVEN henger under den. Hvis den bare *ligger der* i treet ditt, er den en premiss du ikke har
   tatt stilling til — og da hviler formålene dine på noe du ikke har valgt. Du lenker deg til den selv,
   du får forklart hva den betyr, og du kan bryte lenken. Bare da er treet ditt.
4. *Hvorfor det er grunnlaget, ikke et tillegg.* Et system som lærer av atferd kan ikke samtidig love at
   det ikke profilerer — løftet og mekanismen motsier hverandre. HAVEN valgte mekanismen som gjør løftet
   sant av seg selv: læring bare over erklærte kilder. Da trenger ikke personvernet å håndheves mot
   systemet; det følger av hvordan systemet er bygget.
5. *Hva det koster.* HAVEN vet mindre om deg enn systemer som observerer. Det er prisen, og den er
   valgt. Til gjengjeld er alt det vet noe du selv har sagt — og det kan aldri overraske deg med hva det
   «har funnet ut».

Status: **prinsipp** (Kjetils ord 2026-09-23). Ikke implementert som test eller port ennå — se 4b.

## 5. Grensene som gjør lag 2 til noe annet enn en profil

1. **Ingen samlet «brukermodell», ingen score, ingen etikett.** «Nivå» er ikke et felt. Det er et sett
   kanter personen kan lese som setninger — «du foretrekker korte svar om formål» — og snu.
2. **Bare egne episoder.** Ingen signal fra andre brukere. Ingen inferens fra noen andre.
3. **Lagring er ikke utlevering.** Kantene lagres under eierens grant. At en celle — også en AI-gateway —
   får *lese* dem, er en egen disclosure-grant per formål, og tillitspakken viser den.
4. **Av-bryter per formål. Slett per kant. Eksporter alt.** Uten dette er det en profil med pynt.
5. **Ingenting flyter fra lag 2 til lag 1.** Registeret lærer ingenting av noen. Skulle det en dag lære
   av bruk, er det en utlevering personen gjør, ikke en standard — og en egen beslutning.
6. **Tilpasning foreslår, avgjør aldri.** En match er ikke en rett. Grensesnittet kan gjøre et svar
   kortere; det kan ikke holde tilbake noe brukeren ba om. Samme regel som A4.
7. **Ingen betalt plassering** — allerede antiformål. Gjelder like mye for hva som foreslås som «hjelp».

## 6. Hvordan (c) faktisk måles — vi har allerede ett datapunkt

Dommerbenken 14.9: samme formål (dømme lærdommer), to grensesnitt, ett utfall hver. Markdown-blankett
med notasjon → kunne ikke brukes. Én sak om gangen, kriteriet synlig, svaret i knappen → 197 rader
fullført. Det er formen på en (c)-episode:

`(formål, grensesnittmønster) → fullført | avbrutt | spurte tilbake`

Ingenting om personen utover «dette mønsteret virket for denne personen for dette formålet». Vekten på
kanten `perspektiv → interest://flate/en-sak-om-gangen` går opp. Forklarbart, slettbart, lokalt.

## 7. Hva jeg ikke vet

- Om `PerspectiveCell` i dag holder noen lært tilstand i det hele tatt, eller bare erklærte relasjoner —
  må leses før dette dekomponeres.
- Hvor grensen går for «episode» i en dialog: én melding, én tråd, én oppgave? Q8 igjen.
- Om det finnes noe i CellScaffold som allerede tilpasser svarlengde eller detaljnivå — ikke søkt.

## 8. Neste steg, hvis Kjetil sier ja til §4

Egen PDD: `laering-i-eget-perspektiv`. Formålene er allerede synlige i tabellen i §3 — de fire radene med
«nei» og «udefinert». Dekomponeringen skal ikke gjøres før §4 er avgjort, og konklusjonen her går til
Astra for motsvar før den legges fram som noe annet enn et svar på et spørsmål.
