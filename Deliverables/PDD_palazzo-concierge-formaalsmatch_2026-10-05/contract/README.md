# Kontrakt — conciergen med formålsmatch (forslag til G2)

Skrevet 7. oktober 2026 (natt til 7.), av Losen, og rettet samme natt etter en uavhengig kontroll (se «Rettet etter kontrollen» sist). Dette er et forslag. Ingenting av det er bygget. Stier er relative til HAVEN-roten; `PS` står for `PalazzoScaffold`, `HD` for `HAVEN-Deploy/_handoff/HD-0077`.

Grunnlaget er kontrakten slik koden er i dag, lest 6. oktober kl. 22:33–22:45 UTC av en lesetråd (`HD/maal/grunnlag-20261007/les/L2-CONCIERGEKONTRAKT.md`): hvert felt, hvert steg i `ask`, og hvilke committede tester som låser hva.

## Det som ikke endres

`POST /palazzo/api/ask`, `POST /palazzo/api/menu`, `POST /palazzo/api/beverages`, `GET /palazzo/api/state` og `GET /palazzo/api/configuration` står som de er, med konvolutten på 13 nøkler (`haven.palazzo.communale.guest-concierge.v1`). Det er grunnen til at det nye kommer som et eget kall:

- Sju committede tester krever nøyaktig de 13 nøklene (`PS/Tests/AppTests/PalazzoCommunaleFacadeTests.swift`, hjelperen `assertEnvelope`, og `PS/Tests/AppTests/PalazzoAllergiHenvisningTests.swift`, hjelperen `assertHenvisning`). Én krever nøyaktig de 13 nøklene i `state`.
- `testT6SpoersmaalUtenOrdFraListenFaarSammeSvartekstSomFoer` låser hele svarteksten for 182 målte kall, og `testDetFrosneAngrepetHolder` utfallet for 180.
- Flere tester krever nøyaktig null eller ett kall til modellen, ett oppslag i cellen per kall, og én logglinje per svar.

Et nytt felt i `ask`, en ny verdi for `route`, eller et steg foran oppslaget, ville gjort disse røde. En committet test endres ikke uten ditt ord. Med et eget kall trengs ingen slik endring.

## Det nye kallet: `POST /palazzo/api/samtale`

Bak samme mellomvare som `ask`: fartsgrensen (30 per 600 s per adresse), 4 kB, `application/json`, og de samme hodene. Kallet finnes bare når tjenesten er satt opp med det (en miljøvariabel, foreslått navn `PALAZZO_CONCIERGE_SAMTALE`). Er den av, svarer kallet 404, og siden bruker `ask` som i dag. Slik kan en utgave settes ut uten at noe endres for gjesten.

### Forespørselen

| Felt | Type | Regel |
|---|---|---|
| `query` | streng | Gjestens setning, 1–1200 tegn etter trimming. Enten `query` eller `choice`, aldri begge og aldri ingen |
| `choice` | objekt | Et trykk på en knapp i forrige svar: `{"kind": "offer", "answer": "ja"|"nei", "ref": "<postens id>"}`, `{"kind": "model", "answer": "denne-gangen"|"hele-samtalen"|"nei", "query": "<setningen som bommet>"}`, eller `{"kind": "remove", "node": "<node>"}` / `{"kind": "remove-all"}` |
| `noted` | liste, høyst 24 | Samtalens Perspective slik siden holder det. Hver post er `{"kind": …, "node": …}`. `kind` er én av `liker`, `liker-ikke`, `taaler-ikke`, `spiser-ikke`, `vil-ha`. `node` må finnes i husets graf. For `taaler-ikke` er det én av tre: en node for et allergen (`allergen:<kode>`, én per allergen i korpusets liste, laget av merkingen), et emne (når det gjesten ikke tåler, ikke er et av de 14, som løk), eller den faste noden `ukjent` når grafen ikke kjenner det igjen. Har det gjesten ikke tåler, samme navn som et allergen (`fisk`, `selleri`), peker posten på allergenet. For de andre slagene er det et emne, en rett eller en drikk. Ingen fritekst |
| `model_consent` | streng | `ikke-spurt`, `hele-samtalen` eller `nei`. Sier om gjesten har svart på spørsmålet om modellen for resten av samtalen |
| `graph_version` | streng | Versjonen av husets graf notatene ble laget mot. Er den en annen enn tjenestens, kastes notatene, og svaret sier det |

Ukjente felt gir 400. En post i `noted` med ukjent `kind`, ukjent `node` eller ekstra felt gir 422 for hele forespørselen: tjenesten gjetter ikke på hva som var ment. Hverken `noted` eller noe annet i forespørselen velger identitet, celle, nøkkel eller publikum; fasaden kaller cellen som huset, som i dag.

### Svaret

De 13 nøklene fra v1 med samme mening, og disse i tillegg. `schema` er `haven.palazzo.communale.guest-concierge.v2`.

| Felt | Type | Innhold |
|---|---|---|
| `kind` | streng | Svartypen, fra en lukket liste: `answer` (som i dag), `offer` (tilbud), `tell` (forteller), `receipt` (kvittering), `marking-list` (liste med merking og beskrivelse), `ask-model` (spørsmålet til gjesten ved bom), `refused` (avvist eller henvist) |
| `understood` | objekt | Det dekomponeringen fant: `purpose` (`spise`, `drikke`, `vite`, `unngaa`, `bord`, `aapningstid` eller `null`), `interests` (hver med `node`, `label`, `sign` og ordene som traff, `matched`), og `text` (setningen siden viser etter «Slik forsto jeg deg:») |
| `offer` | objekt eller `null` | Ved `offer`: `ref` (postens id i korpuset), `name`, `when` (fra rettens kategori) og `choices` |
| `noted` | liste | Hele listen etter dette svaret, hver post med `kind`, `node` og `label`. Siden bytter sin kopi med denne |
| `match` | objekt | `route` (`match`, `model-behind` eller `none`), `graph_version`, `complete`, `threshold`, `miss_reason`, og `hits`: postene som nådde terskelen, hver med `ref`, `score` og `because` (nodene og ordene som ga treffet) |
| `model_question` | objekt | Bare ved `ask-model`: `choices` |
| `interpreted_by_model` | objekt eller `null` | Når modellen bak har pekt ut noder: `pointed` (id-ene som ble brukt), `offered_count` og `dropped` (antall id-er som ble kastet fordi de ikke var tilbudt) |

`route` beholder meningen fra v1: hvem som skrev teksten gjesten leser (`native` eller `model`). Hvordan nodene ble funnet, står i `match.route`. Et svar med `match.route == "model-behind"` har alltid `interpreted_by_model`, og siden viser merket «Tolket av en språkmodell».

`miss_reason` bruker kjernens egne navn (`MatchStrategyEscalationTrigger` i `CellProtocol/Sources/CellBase/PurposeAndInterest/MatchStrategyPlanner.swift`, pinnen `81601a6f`): `lowConfidence` (ingen node nådde terskelen), `ambiguousTopK` (flere noder like sterke, og ingen av dem klar), `missingPreconfiguredCoverage` (ingen ord i setningen traff grafen), `privacyOrCapabilityGate` (forhåndssjekken stoppet setningen), og i tillegg `incomplete` når kjernens kjøring ikke ble fullstendig. Et ufullstendig søk er en bom, aldri en rangering.

Nye verdier for `reason_code`: `offer`, `tell`, `noted`, `removed`, `marking-list`, `match-miss`, `model-declined`, `model-unavailable`, `precheck-blocked`. De gamle står.

### Regler svaret alltid følger

1. Ingen svartype sier at en rett er trygg.
2. Har `noted` en post av slaget `taaler-ikke`, er `kind` aldri `offer`. Nevner svaret retter, er det `marking-list`: merkingen og beskrivelsen for hver rett, hva som er merket med eller nevner det gjesten ikke tåler, hvilke merkinger som ikke er bekreftet, og henvisningen til personalet. Det gjelder alle tre slag noder. For et allergen sier svaret hvilke retter som er merket med det, og hvilke som har allergenets eget ord i beskrivelsen (som «selleri» i «stangselleri»). Det vet ikke hvilke ingredienser som hører til et allergen: pistasj og mandler er ikke koblet til nøtter. For et emne sier svaret hvilke retter grafen har emnet på, enten det kommer fra beskrivelsen, en tagg, kategorien eller navnet. Beslektede emner regnes ikke med: «løk» treffer ikke `hvitløk`. For `ukjent` sier svaret at conciergen ikke kjenner det igjen. Ordet gjesten brukte, lagres ikke. I alle tre tilfellene viser svaret merkingen for hver rett det nevner, sier ikke at andre retter er uten, og viser til personalet.
3. Et `choice` med `ja` til et tilbud fører bare til en ny post i `noted` og en kvittering. Ingen bestillingsnøkkel kalles, og ingenting blir synlig for huset.
4. `offer.ref` peker aldri på en drikk med alkohol.
5. Hvert navn og hver beskrivelse i `answer` er postens felt ordrett. Teksten bygges av vakten, ikke av en modell.
6. Tekst fra modellen bak når aldri gjesten. Modellen svarer med id-er, og bare id-er den fikk tilbudt, brukes.
7. Et svar som nevner en rett eller en drikk, har linjen om allergener først blant advarslene, i de tre formene koden har i dag (regel 3 i strakstiltaket, `PS/Sources/App/Controllers/PalazzoCommunaleProjection.swift`, linje 17–19): én for én rett med beskrivelse, én for flere, og én for svar uten beskrivelse. Listene etter «tåler ikke» har sin egen linje. Regelen er smalere enn regel 3 på nett, som gjelder hvert publisert svar: kvitteringer som ikke nevner noen rett, og spørsmålet om modellen, har ikke linjen i forslaget. Vil du ha den på alle svar, sier du det.

Allergenene har ikke noder i forslaget til emner ennå (`graf/emner-v1.md`). De må inn før regel 2 kan bygges: emnene `selleri` og `fisk` er ord fra beskrivelser og tagger, og sier ikke hva en rett er merket med. Hva som skal skje når gjesten ikke tåler noe grafen ikke kjenner, er et forslag her (noden `ukjent`) og et spørsmål til deg.

### Hva modellen bak får, og hva som aldri sendes

Modellen bak spørres bare når matchen har bommet, gjesten har sagt ja (`choice` med `denne-gangen` eller `hele-samtalen`, eller `model_consent == "hele-samtalen"`), og forhåndssjekken slipper setningen gjennom.

- **Sendes:** gjestens setning, og listen over det huset kan tilby (id og navn for retter og drikke uten alkohol, og formålene). Ingen identitet, ingen adresse, ikke `noted`.
- **Sendes aldri:** en setning forhåndssjekken stopper. En setning sendes bare når hvert tegn er en bokstav, et mellomrom eller vanlig skilletegn (komma, spørsmålstegn, utropstegn, kolon, semikolon, bindestrek og anførselstegn), og et punktum bare sist i en setning. Et siffer, en «@», en parentes eller et punktum inne i et ord stopper den. Det som slipper gjennom, er det som er skrevet med bare bokstaver: et nummer eller en e-postadresse skrevet med ord, og navn og gatenavn. `contract/forhaandssjekk_regnet.py` har 23 setninger som skal stoppes: regelen stopper 20, og slipper gjennom de tre som er skrevet med ord (regnet i Python, ikke kjørt i Swift). De fem mønstrene Kallimachos har (`CellScaffold/_wt-butler-e1-20260929/Sources/App/Cells/AI/KallimachosAdvisorCell.swift`, linje 246–252), slipper 19 av de 23 gjennom. Gjesten har sagt ja til at setningen sendes. En setning med et ord fra listen i strakstiltaket (`PS/Sources/App/Services/PalazzoAllergiHenvisning.swift`) eller et ord for vin eller alkohol (`PS/Sources/App/Services/PalazzoConciergePhrasing.swift`, linje 87–95). De får det conciergen selv svarer.
- **Tilbake:** JSON med `nodes` (høyst tre id-er) og `purpose`. Alt annet kastes. En id som ikke ble tilbudt, kastes og telles i `dropped`. Ingen gyldig id gir avvisningen som i dag.

### Tilstand

Tjenesten holder ingenting om samtalen. `noted` og `model_consent` ligger på siden, i minnet, og sendes med hvert kall. Lukkes eller lastes siden på nytt, er de borte. Ingenting skrives til disk, verken på siden (ingen informasjonskapsel, ikke `localStorage`) eller i tjenesten. Planen sier hvorfor dette er valgt framfor et lager i tjenesten.

### Loggen

Én linje per svar, samme logger som i dag, med ny verdi for handlingen: `concierge-formulering handling=samtale utfall=<vei>:<grunn>`. Veien er `match`, `modell-bak`, `kvittering`, `avvist` eller `henvist`. Grunnen er en verdi fra de lukkede listene over. I tillegg én linje per bom: `concierge-bom grunn=<miss_reason> graf=<versjon> noder=<antall modellen pekte på>`. Aldri gjestens ord, aldri `noted`, aldri nøkkelen.

## Eksemplene

I `contract/eksempler/`. Tallene i `match.hits` er regnet av `graf/lag_emner.py` med gjesteflatens regning og enhetsvekter, ikke av programkoden, og terskelen 0,05 er den som står på grenen i dag, ikke et valg. `graph_version` er versjonen datafilen har nå, `emner-v1-forslag-20261007`.

| Fil | Viser |
|---|---|
| `gyldig-01-tilbud.foresporsel.json`, `gyldig-01-tilbud.svar.json` | «Jeg liker ost» gir et tilbud |
| `gyldig-02-ja.foresporsel.json` | Trykk på «Ja, det vil jeg» |
| `gyldig-03-bom.svar.json` | En bom: spørsmålet til gjesten. Ingen ord i setningen traff grafen (`missingPreconfiguredCoverage`), som i bilde 8 |
| `ugyldig-01-baade-setning-og-valg.foresporsel.json` | Både `query` og `choice`: 400 |
| `ugyldig-02-fritekst-i-notert.foresporsel.json` | Fritekst, ukjent slag og ukjent node i `noted`: 422 |

## Siden

`PS/Public/js/palazzo-communale.js` leser i dag bare navngitte felt og hopper over resten. Når kallet finnes, sender siden setningene til `samtale` i stedet for `ask`, holder `noted` og `model_consent` i minnet, og tegner etter `kind`. De to snarveiene «Hva står på menyen?» og «Hva kan jeg drikke?» går til `menu` og `beverages` som i dag.

## Rettet etter kontrollen (7. oktober 2026)

Kontrolltråden K4 leste kontrakten mot kildene (`HAVEN-Deploy/_handoff/HD-0077/maal/grunnlag-20261007/kontroll/K4-HOVEDOPPGAVEN.md`). Det som er endret her:

- **Forhåndssjekken.** Første utgave lovet at en setning med telefonnummer eller kortnummer aldri sendes, og viste til Kallimachos' fem mønstre. De slipper vanlige skrivemåter gjennom. Mitt første forslag til egne regler sa at de «dekker» telefonnumre og e-postadresser; den neste kontrollen (K7) fant setninger som slapp gjennom, og kontrollen etter den (K8) fant flere. Nå er regelen snudd til en liste over det som slipper gjennom, og det som går ut da, er bare det som er skrevet med ord.
- **Regel 2** sier nå hva svaret ser på for et allergen og for et emne, og hva det ikke vet (K8).
- **«Tåler ikke».** Første retting snevret det inn til de 14 allergenene. K7 fant at «Jeg tåler ikke løk» da sto uten regel. Nå er det tre slag noder, og regel 2 gjelder alle.
- **Regel 7** er ny: linjen om allergener under hvert svar som nevner en rett eller en drikk, i formene koden på nett har. Den er smalere enn regel 3 på nett, som gjelder hvert publisert svar.
- **Nodene for allergener** er sagt som en mangel i forslaget til emner.
- **Eksemplene** har versjonen datafilen har. `contract/forhaandssjekk_regnet.py` er ny.
