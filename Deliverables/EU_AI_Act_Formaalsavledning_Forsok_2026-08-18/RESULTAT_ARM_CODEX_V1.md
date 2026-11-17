# Arm B3: blind erklæring ved Codex, etter rettelser

Dato: 2026-08-18

Status: kjørt forskningsresultat. Oppfølging av `RESULTAT_ARM_CODEX.md`.

Formål: måle om de fire rettelsene som ble diagnostisert i arm B2 faktisk virker,
eller bare hørtes rimelige ut.

## Rettelsene som ble gjort

Alle fire er **definisjonsrettelser**, ikke tuning. Ingen skjønnsverdi ble endret
fordi Codex var uenig med meg — bare feil i selve oppgaven ble rettet. Det
skillet er hele forskjellen mellom en rettelse og en tilpasning til testsettet.

| # | Rettelse | Begrunnelse fra B2 |
| --- | --- | --- |
| 1 | `systemKind` påkrevd og først (`capability` / `abstract` / `facet` / `governance-criterion` / `internal-test`). Bare `capability` klassifiseres. | 17 abstrakte grener ble erklært som kode. Feltet manglet i briefen — min utelatelse. |
| 2 | `aiInvolvement` **fjernet fra erklæringen**, avledes maskinelt. | Samsvar 0,579. Informasjonen finnes i implementasjonen, ikke i formålsteksten. |
| 3 | `allocatesTasksToPersons` → `supportsWorkAllocationOrMonitoring`, utvidet til å dekke å vise, spore eller *støtte* menneskelig fordeling. | Codex avviste flagget med «sporing er ikke det samme som automatisk oppgavefordeling» — forsvarlig lesning av et feil navn. |
| 4 | `confidence` brukes til å rute alt som ikke er `high` til menneskelig gjennomgang. | B2 viste at usikkerheten korrelerte med feilene. |

Reglene ble verifisert atferdsbevarende først: `score_arm_v1.mjs` reproduserer
takarmens 0,905 nøyaktig på referansefasettene før den ble brukt på Codex.

Ny brief: `BRIEF_v1.md`. Ny tråd, ingen kontekst fra B2.

## Resultat

| | B2 (v0-brief) | **B3 (v1-brief)** |
| --- | --- | --- |
| Presisjon | 1,000 | 0,923 |
| Dekning | 0,364 | **0,545** |
| F1 | 0,533 | **0,686** |
| Noder helt riktig | 46/57 | 48/57 |
| Falske negative | 14 | **10** |

Med `confidence`-ruting påslått:

| | B2 (anslag) | **B3 (målt)** |
| --- | --- | --- |
| Dekning med ruting | 0,727 | **0,909** |
| Noder rutet til menneske | — | 15 av 57 |
| Bommer gjenvunnet av ruting | — | 8 av 10 |
| **Restbommer på `high`** | 6 | **2** |

Restbommene er:

```
purpose://preference.owner-controlled   → art. 5(1)(c) grense
purpose://value-and-commons             → vedlegg III.5 grense
```

Begge er `boundary`. **Alt annet ble enten funnet eller riktig meldt som usikkert.**

Det er nøyaktig det utfallet jeg forutsa i B2-rapporten — «retter man flagget og
ruter medium/low til gjennomgang, står to bommer igjen, og begge er
grensetilfeller». Det er første gang i dette forsøket en prediksjon har blitt
bekreftet i stedet for falsifisert.

## Funn 1: rutingen er mekanismen, ikke reglene

Dette er armens viktigste resultat, og det er ikke det jeg ventet.

Rettelsene alene løftet dekningen fra 0,364 til 0,545 — en forbedring, men ikke
en løsning. Det som faktisk lukket gapet var at **Codex meldte usikkerhet på
nøyaktig de nodene den bommet på**.

Fire av de fem vedlegg III.4-nodene fikk fortsatt ikke flagget, med begrunnelser
som «ownership or assignees are not explicit». Men alle fire ble erklært `medium`.
De ble rutet, og dermed fanget.

Grunnen er verdt å merke seg: informasjonen flagget krever ligger i
**forelderen**, ikke i noden. `purpose://digital-work.coordinate` sier eksplisitt
«who is doing what» og fikk flagget med `high`. Barna sier bare «track tasks,
bugs, decisions» og fikk det ikke. En erklæring per node mister
arvet kontekst — men usikkerheten den skaper er ærlig rapportert.

**Konsekvens for design:** erklæringsverktøyet bør vise forelderens tekst når en
node erklæres. Og `confidence` er ikke pynt — det er den bærende
sikkerhetsmekanismen. Et skjema uten det feltet ville tapt 8 av 10 funn her.

## Funn 2: to uavhengige armer peker nå på en feil i min fasit

`purpose://content.review-before-publish` gir én falsk positiv i **begge** armer:
reglene sier art. 50(1), fasiten min sier bare 50(2) og 50(4).

Etter to uavhengige treff mener jeg fasiten er feil. Eieren som gjennomgår
modellgenerert innhold, *interagerer med et AI-system*, og art. 50(1) gjelder.

Fasiten er **ikke** rettet i etterkant. Å justere fasiten etter å ha sett
resultatene ville gjort begge målingene verdiløse. Rettelsen hører hjemme i en
fasit-v1 som skrives ned og dateres **før** neste arm kjøres, og som da må kjøres
mot alle tre armene på nytt. Reell presisjon i B3 er sannsynligvis 1,000.

## Funn 3: grensen står, nå etter tre armer

`boundary`-dekning: 0,25 i takarmen, 0,25 i B2, 0,25 i B3.

Tre uavhengige forsøk, samme tall, samme ene treff
(`personal-context.semantic-state`, som Codex flagget uoppfordret begge ganger),
samme tre bommer. Og etter rettelsene er grensetilfellene **det eneste** som
slipper gjennom.

Det er så nær et negativt resultat man kommer i et lite forsøk:

> Erklæring pluss regler pluss usikkerhetsruting løser plikter.
> Ingen av delene rører nærhet til et forbud.

`preference.owner-controlled` er det reneste eksempelet. Codex erklærte den med
`high` og skrev at oppgitte preferanser ikke er utledede egenskaper. Det er
**riktig**. Noden er likevel ett designvalg unna art. 5(1)(c). Ingen erklæring om
hva systemet *er* kan fange hva det *kunne bli*.

## Funn 4: `systemKind` virket, og gjorde noe uventet

Alle 57 fikk en fornuftig `systemKind`, og gatingen fjernet støyen fra B2.

Men Codex plasserte flere noder som `governance-criterion` enn jeg gjorde —
blant annet `purpose://root`, `purpose://human-agency`,
`purpose://skeleton.owner-entity-access` og `purpose://access.audit.privacy`.
Jeg hadde kalt de to første `abstract` og den tredje `capability`.

Codex' lesning er bedre enn min. `skeleton.owner-entity-access` *er* et krav om
hvordan systemet skal oppføre seg, ikke en funksjon. Det påvirket ikke skåringen
her, men det er en observasjon om selve formålstreet: flere noder som i dag ser
ut som formål, er egentlig kriterier. Det hører hjemme i en gjennomgang av Book 23,
ikke i dette forsøket.

## Samlet bilde etter fire kjøringer

| Arm | Metode | Presisjon | Dekning | F1 |
| --- | --- | --- | --- | --- |
| A | leksikalsk fra dagens formålstekst | 0,036 | 0,182 | 0,060 |
| B1 | tak: erklæring av samme annotatør som fasit | 0,950 | 0,864 | 0,905 |
| B2 | Codex blind, v0-brief | 1,000 | 0,364 | 0,533 |
| **B3** | **Codex blind, v1-brief** | 0,923 | 0,545 | **0,686** |
| **B3+ruting** | **B3 med `medium`/`low` til menneske** | — | **0,909** | — |

Konklusjonen etter fire kjøringer: **hypotesen holder, med to forbehold.**

Avledet AI Act-klassifisering fra formålserklæringer virker, forutsatt at
(a) erklæringen er strukturert og ikke fri tekst, (b) modellavhengigheten hentes
fra registeret og ikke fra et menneske, og (c) usikre erklæringer rutes til
gjennomgang. Da fanges 0,909 av pliktene, og restrisikoen er avgrenset til
grensetilfeller som uansett krever menneskelig vurdering.

## Hva som fortsatt ikke er vist

1. **`aiInvolvement` er ikke hentet fra et faktisk register.** Forsøket på å lese
   CellProtocol/CellScaffold/HavenAgentD via Codex 2026-08-18 nådde ikke gjennom
   innenfor MCP-kallets tidsgrense. Verdiene er foreløpig kopiert fra
   referansefasettene, altså fra samme annotatør som skrev fasiten. **B3-tallene
   er derfor et øvre tak betinget av at registerlesningen reproduserer de samme
   verdiene.** Dette står også i `aiinvolvement_registry_v0.json`, og må stå
   hvor enn tallene siteres.
2. **Rutingen antar at mennesket løser det.** 0,909 er et tak for
   ruteregelen, ikke en måling av menneskelig treffsikkerhet.
3. **Fasiten er fortsatt min, og har minst én kjent feil** (funn 2).
4. **n=1 per arm.** Ingen gjentakelse, ingen varians, én ekstern annotatør.
5. **Batch 2 ble sendt to ganger** etter en tidsavbrudd, i forkortet form. Samme
   innhold, men ikke identisk formulering. Seks noder er erklært fra den
   forkortede varianten.

## Neste steg

1. **Fasit-v1**, med `content.review-before-publish`-rettelsen, datert og skrevet
   før neste kjøring. Kjør alle armene på nytt mot den.
2. **Faktisk registerlesning** for `aiInvolvement`. Må gjøres som en filbasert
   Codex-oppgave, ikke over MCP, siden repo-grep sprenger tidsgrensen.
3. **Lokal arm.** Qwen3-8B eller Gemma 4 mot v1-briefen. Nå med et meningsfullt
   sammenligningsgrunnlag: klarer den lokale modellen 0,545 uten ruting og 0,909
   med, er regulatorisk selvklassifisering på egen maskin demonstrert.
4. **Grensesporet.** Fortsatt uløst etter tre armer. Trenger en fiendtlig agent
   som for hver node spør «hva er den minste designendringen som gjør dette
   forbudt?». Det er et annet eksperiment, og det bør ikke blandes inn i dette.

## Claim-regel, uendret

En grønn kjøring betyr at reglene dekker fasettene. Aldri «HAVEN etterlever
AI Act».
