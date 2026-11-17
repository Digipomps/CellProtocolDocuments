# Dataflyt — conciergen med formålsmatch (forslag til G2)

Skrevet 7. oktober 2026 (natt til 7.), av Losen, og rettet samme natt etter en uavhengig kontroll: steg 8 lovet mer enn mønstrene holdt (se `PLAN.md`, «Forhåndssjekken»). Viser kantene slik de blir med forslaget i `PLAN.md` og `contract/README.md`. Ingenting av det nye er bygget. Stier er relative til HAVEN-roten; `PS` står for `PalazzoScaffold`.

```
GJESTENS NETTLESER (siden /palazzo)                 PALAZZOS VERT (PalazzoScaffold i containeren)
 holder i minnet, ikke på disk:
   noted          det gjesten har sagt om seg selv
   model_consent  svaret på spørsmålet om modellen
        │
        │  POST /palazzo/api/samtale
        │  { query | choice, noted, model_consent, graph_version }
        ▼
                                                     FASADEN (PalazzoCommunaleFacade)
                                                      1  fartsgrense, størrelse, dekoding            som ask i dag
                                                      2  strakstiltaket: ord fra listen → henvisning  står til F8 er godkjent
                                                      3  DEKOMPONERINGEN                              ny, uten modell
                                                         setningen → formål + interesser med fortegn,
                                                         og ordene som traff
                                                      4  SAMTALENS PERSPECTIVE                        ny, bygges for dette kallet
                                                         noted + det setningen sier om gjesten;
                                                         kjernens typer (Interest, Purpose, Weight)
                                                      5  MATCHEN                                      ny, uten modell
                                                         interessene × HUSETS GRAF → poster over terskelen
                                                              ▲
                                                              │ lages én gang ved oppstart
                                                         HUSETS GRAF  (data med versjon: emner, ordformer,
                                                              │        vekter, terskel, formål med måltekst)
                                                              │ id, navn, beskrivelse, kategori, merking
                                                         KORPUSET (PalazzoConciergeCorpusCell)        som i dag, lest som huset
                                                      6a treff → VAKTEN bygger svaret av postens felt
                                                         (tilbud, forteller, liste med merking, kvittering)
                                                      6b bom  → spørsmålet til gjesten, eller avvisningen
                                                      7  loggen: én linje per svar (vei og grunn),
                                                         én linje per bom (grunn, grafversjon, antall noder)
        ◄─────────────────────────────────────────────  svar (v2): kind, understood, offer, noted, match …
 viser svaret, bytter noted med svarets

 [gjesten trykker «Denne gangen» eller «Hele samtalen»]
        │  POST /palazzo/api/samtale { choice: model … }
        ▼
                                                      8  FORHÅNDSSJEKKEN: bare bokstaver, mellomrom og
                                                         vanlig skilletegn slipper gjennom; ord om
                                                         allergi, trygghet, vin, alkohol → sendes ikke
                                                      9  MODELLEN BAK ──────────────────────────────►  EKSTERN SPRÅKMODELL
                                                         setningen + det huset kan tilby (id og navn)      (Anthropic, som i dag;
                                                         ◄── id-er ─────────────────────────────────       nøkkelen ligger bare på verten)
                                                     10  VALIDERINGEN: bare id-er som ble tilbudt
                                                         → tilbake til 5 med nodene; svaret merkes
```

## Hva som går hvor

| Data | Fra | Til | Lagres | Logges |
|---|---|---|---|---|
| Gjestens setning | siden | fasaden, hver gang | nei | nei |
| Gjestens setning | fasaden | den eksterne modellen, bare etter gjestens ja og forhåndssjekken | ikke av huset. Hva leverandøren beholder, er ikke undersøkt her | nei |
| `noted`: det gjesten har sagt om seg selv, som nodeid og slag | siden | fasaden, med hvert kall | bare i sidens minne | nei |
| `noted` | fasaden | modellen | sendes aldri | nei |
| Husets graf | datafil i pakken | fasaden, ved oppstart | i pakken, med versjon | versjonen står i `state` og i linjen per bom |
| Korpusets poster | cellen | fasaden, lest som huset | som i dag | nei |
| Det modellen peker på | modellen | fasaden | nei | antall, ikke hvilke |
| En bom | fasaden | loggen | loggen i containeren | grunn, grafversjon, antall noder |
| Et ja til et tilbud | siden | fasaden, som ny post i `noted` | bare i sidens minne | nei. Ingen i huset ser det |

## Det som er nytt mot i dag

- Gjestens setning kan forlate huset. I dag får modellen bare det ferdige svaret (`PS/Sources/App/Services/PalazzoAnthropicPhraser.swift`, linje 133). Det nye skjer bare etter gjestens ja. Forhåndssjekken slipper bare gjennom setninger av bokstaver og vanlig skilletegn. Et nummer eller en adresse skrevet med ord, og navn, stopper den ikke (`PLAN.md`, «Forhåndssjekken»).
- Tjenesten får vite hva gjesten har sagt om seg selv tidligere i samtalen, også hva hun ikke tåler, fordi siden sender det med. Det følger svaret ditt på valg D («Vakten, for samtalen»). Tjenesten beholder det ikke.
- Husets graf er en ny datakilde, laget av korpuset. Retter og drikke har fortsatt én kilde: grafen bærer postens id, og navn, beskrivelse, kategori og merking leses fra korpuset.

## Det som ikke endres

- Fasaden kaller cellen som huset. Gjesten får ingen identitet, og forespørselen velger aldri celle, nøkkel eller publikum.
- `ask`, `menu`, `beverages`, `state` og `configuration`.
- Modellen som formulerer, ser ikke gjestens spørsmål.
- Veien fra siden til gjestens egen entitet finnes ikke. Den hører til «Behold» (arbeidspakke 12) og onboarding-oppgaven.
