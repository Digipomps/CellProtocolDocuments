---
doc_id: manual-skeleton-redigering
title: Brukermanual – Endre en flate (skeleton-redigering)
repo: CellProtocolDocuments
owner: CellScaffold / Porthole
audience: human
status: draft
last_verified: 2026-10-22
source_code:
  - CellScaffold/Public/js/porthole-webo.js
  - CellScaffold/Sources/App/Controllers/PortholeWebSessionSupport.swift
  - CellScaffold/Sources/App/Controllers/PortholeWebEditorSupport.swift
  - CellScaffold/Sources/App/Cells/CellConfigurationStudio/CellConfigurationStudioCell.swift
  - CellScaffold/scripts/skeleton-iterate.js
  - CellProtocol/Sources/CellBase/Skeleton/SkeletonDescription.swift
interfaces:
  - editor.mode.set
  - editor.selection.set
  - editor.component.insert
  - editor.working.setSkeleton
  - editor.undo
  - editor.redo
  - editor.discard
  - editor.apply
  - cell:///CellConfigurationStudio
  - applyEditableCellConfiguration
  - resetEditableCellConfiguration
---

# Endre en flate

**Kort fortalt:** Alt du ser i HAVEN er en *flate*. Hver flate er beskrevet av en
oppskrift, en `CellConfiguration`, og selve utseendet ligger i oppskriftens
*skeleton*: en trestruktur av byggeklosser som tekst, knapper, lister og seksjoner.
Du kan endre en flate uten at noen må bygge appen på nytt.

Denne manualen er ordnet etter hva du vil få til, ikke etter knapper.

| Jeg vil …                                   | Gå til |
|---------------------------------------------|--------|
| se hvordan en flate er bygget               | [1](#1-se-hvordan-en-flate-er-bygget) |
| endre en tekst, etikett, farge eller avstand | [2](#2-endre-tekst-farge-og-avstand) |
| legge en ferdig del inn i en flate          | [3](#3-legge-en-ferdig-del-inn-i-flaten) |
| fjerne noe                                  | [4](#4-fjerne-noe) |
| prøve meg fram uten å ødelegge              | [5](#5-prøve-trygt-angre-gjør-om-forkast) |
| lagre slik at endringen varer               | [6](#6-lagre-slik-at-endringen-varer) |
| gjøre større endringer eller lage en ny flate | [7](#7-større-endringer-cell-configuration-studio) |
| la en agent prøve ut endringer (utvikler)   | [8](#8-for-utviklere-iterere-med-agent-uten-ny-bygg) |
| sjekke at flaten faktisk virker             | [9](#9-sjekke-at-flaten-virker) |

> **Hvor:** Redigering gjøres i **Porthole i nettleseren** (web). HAVEN-appen på
> iPhone/Mac (Binding) viser flatene, men har ingen redigeringsmodus i dag.

---

## Ord du trenger

| Ord | Betyr |
|-----|-------|
| **Flate** | Én skjerm eller ett arbeidsområde, for eksempel «Samtaler» eller «Offentlig profil». |
| **Konfigurasjon** (`CellConfiguration`) | Oppskriften for en flate: navn, hvilke celler den henter data fra, og skeleton. |
| **Skeleton** | Byggeklossene flaten består av, ordnet som et tre. |
| **Element / node** | Én byggekloss i skeleton, for eksempel en tekst eller en knapp. |
| **Komponent** | En ferdig sammensatt del (for eksempel «Chat») som kan legges inn i en flate. |
| **Kilde-celle / eiercelle** | Cellen som eier flaten og lagrer den varige versjonen. |
| **Kladd** | Endringene dine før du trykker **Bruk**. Ingen andre ser dem. |
| **Keypath** | Adressen til en verdi eller handling i en celle, for eksempel `chat.state.title`. |

---

## 1. Se hvordan en flate er bygget

**Formål:** Forstå hva flaten består av før du endrer den.

1. Åpne Porthole og trykk **Bibliotek** øverst til høyre.
2. Søk etter flaten (navn, formål eller endepunkt) og trykk **Last inn**.
3. Trykk **Rediger**. Tre paneler dukker opp:
   - **Components** (komponenter) – ferdige deler du kan legge inn.
   - **Elements** (elementer) – treet av byggeklosser. Innrykket viser hva som ligger inni hva.
   - **Inspector** (inspektør) – detaljene for elementet du har valgt.
4. Klikk et element i lerretet eller i **Elements**. Det får en ramme, og
   **Inspector** viser type, plassering (`Path`, for eksempel `root.2.0`) og feltene.

Panelene kan dras, kollapses og skjules. **Mer → Vis detaljer → Tilbakestill
paneler** setter dem tilbake.

> **Kun lesing?** Står det «Kun lesing» i et banner, har du ikke rett til å endre
> denne flaten. Du kan se, men ikke lagre. Be eieren om en avtale (Agreement) som
> gir skrivetilgang, eller åpne Porthole som eier.

---

## 2. Endre tekst, farge og avstand

**Formål:** Små justeringer av noe som allerede finnes.

1. I **Rediger**, velg elementet.
2. I **Inspector → Parameters** endrer du innholdet, for eksempel `text` på en
   tekst eller `label` på en knapp.
3. I **Inspector → Modifiers** endrer du utseende: `padding`, `background`,
   `cornerRadius`, `fontSize`, `foregroundColor`, `opacity` og lignende.
4. Felt som ikke finnes ennå, legges til fra listen under feltene.
5. Endringen vises med en gang i lerretet, men er bare en kladd til du trykker
   **Bruk** (se [6](#6-lagre-slik-at-endringen-varer)).

**Dette kan inspektøren ikke endre i dag:** lister og regler, som hvilke deler et
område tar imot (`acceptedDragRoles`), når noe skal vises (`visibility`) og
stilklasser. Slike endringer må gjøres i Studio (se [7](#7-større-endringer-cell-configuration-studio)).

> **Pass på keypath:** Feltene `keypath`, `actionKeypath` og lignende kobler
> elementet til data og handlinger i en celle. Endrer du dem til noe som ikke
> finnes, blir teksten tom eller knappen gjør ingenting, uten feilmelding.

---

## 3. Legge en ferdig del inn i flaten

**Formål:** Gi flaten ny funksjon, for eksempel en chat, uten å bygge den selv.

**Med dra og slipp:**

1. Trykk **Rediger**, og åpne **Bibliotek**.
2. Under **Components** finner du ferdige deler (Chat, AI Agent, Todo Planner,
   RAG Assistant, m.fl.). Også hele konfigurasjoner med skeleton kan dras inn.
3. Dra delen inn i lerretet. Områder som tar imot, lyser opp med
   **Legg til her** (eller **Legg til i rotnivå**).
4. Slipp. Delen legges inn, og eventuelle celler den trenger kobles til flaten
   automatisk (navnene får nytt suffiks om de kolliderer).

**Uten mus:** Trykk **Plasser** på delen, og klikk deretter **Legg til her** der den
skal stå. **Avbryt** i det gule banneret angrer valget.

**Hvor kan jeg slippe?** Flaten bestemmer selv. Hvis et område i flaten er merket
som slippsone for komponenter, er det *bare* disse områdene som lyser opp. Er ingen
områder merket, kan du slippe i alle beholdere (stabler, seksjoner, lister, faner).

**Dette går ikke i dag:** legge inn én enkelt tekst, knapp eller felt fra
paletten, eller flytte et element til et annet sted. Paletten har bare ferdige,
sammensatte deler.

---

## 4. Fjerne noe

1. Velg elementet.
2. Trykk **Slett valgt node** i **Inspector**. Roten kan ikke slettes.
3. Angre med **Angre** hvis det var feil.

---

## 5. Prøve trygt: Angre, Gjør om, Forkast

**Formål:** Eksperimentere uten risiko.

- **Angre** og **Gjør om** finnes under **Mer** (og under **Vis detaljer**).
  Historikken gjelder fram til du trykker **Bruk** eller **Forkast**.
- **Forkast endringer** kaster hele kladden og viser flaten slik den sist ble lagret.

> ⚠️ **Viktig: «Vis» lagrer.** Trykker du **Vis** mens du har ulagrede endringer,
> blir de lagret automatisk, akkurat som **Bruk**. Vil du *ikke* beholde
> endringene, trykk **Forkast endringer** først, og deretter **Vis**.

---

## 6. Lagre slik at endringen varer

**Formål:** Gjøre endringen synlig for deg selv neste gang, eller for andre.

Trykk **Bruk** i verktøylinjen. Hva som skjer, avhenger av flaten:

| Hvis du ser … | Så betyr «Bruk» … |
|---------------|-------------------|
| Banner **«Kildebasert redigering»** | Endringen lagres i eiercellen og overlever ny innlogging og omstart. |
| Banner **«Kun lesing»** | Du kan ikke lagre. |
| Ingen banner | Endringen gjelder **bare denne visningen** (denne Porthole-økten). Laster du en annen flate eller logger ut, er den borte. Bruk Studio (se 7) for å lagre en egen versjon. |

**Hvis noen andre har lagret i mellomtiden** får du en feil om utdatert revisjon.
Last flaten på nytt, og gjør endringen igjen.

**Tilbake til originalen:** Flater fra biblioteket beholder originalen. Det finnes
foreløpig ingen knapp i Porthole for å tilbakestille til originalen; be en utvikler
om å kjøre tilbakestilling på eiercellen.

Flater som er kildebaserte i dag, er blant annet konferanseflatene (deltaker,
admin, sponsor, offentlig profil og profilredigering, konferansechat), Chat,
Publication og Arendalsuka-publiseringen.

---

## 7. Større endringer: Cell Configuration Studio

**Formål:** Endre mye på en gang, lage en ny flate, eller ta vare på versjoner.

Studio er en egen flate i biblioteket («Cell Configuration Studio», og som del av
«Cell Configuration Architect»).

1. **Velg flate** i listen *Konfigurasjoner*.
2. **Hent oppskriften:** I Porthole, **Rediger → Inspector → Kopier working
   CellConfiguration**. Lim inn i en tekstfil og gjør endringene der (eller be en
   AI-assistent om hjelp, se under).
3. **Last opp utkastet** under *Privat utkast* (én JSON-fil, maks 512 KB, må ha
   skeleton). Du ser en forhåndsvisning.
4. **Lagre ny privat versjon** for å ta vare på et punkt du kan gå tilbake til
   (*Versjonshistorikk*).
5. **Publiser til valgt eiercelle** når utkastet er riktig. Det krever at du har
   skrivetilgang til eiercellen. Studio gir deg aldri tilgang til andres data.
6. **Forkast lokale endringer**, **Angre** og **Gjør om** fungerer som i Porthole.

**Få hjelp av AI:** I «Cell Configuration Architect» finnes knappen
**Load architect prompt**. Den gir AI-assistenten oppskriften på hva skeleton
faktisk støtter, slik at utkastet ikke bruker byggeklosser som ikke finnes.

**Byggeklosser som finnes i dag:** `VStack`, `HStack`, `ZStack`, `ScrollView`,
`Section`, `Tabs`, `Grid`, `List`, `Tree`, `Object`, `Reference`,
`ComponentSurface`, `NavigationBar`, `Text`, `Image`, `Divider`, `Spacer`,
`Button`, `Toggle`, `Picker`, `TextField`, `TextArea`, `FileUpload`,
`AttachmentField` (eldre) og `Visualization`. Finnes ikke det du trenger i denne
listen, er det en ny funksjon, og den må avtales med Kjetil før noen bygger den.

---

## 8. For utviklere: iterere med agent uten ny bygg

**Formål:** La en agent (Claude/Codex) prøve ut en skeleton-endring mot kjørende
Porthole, med skjermbilder, før noe lagres.

Fra `CellScaffold`:

```bash
# Forhåndsvis uten å lagre (trygt standardvalg)
npm run skeleton:iterate -- --mode preview \
  --configurationName "Conference Participant Chat" \
  --sourceCellEndpoint cell:///ConferenceChatLaunch \
  --skeletonFile /tmp/kandidat.skeleton.json

# Eller med et ferdig scenario
npm run skeleton:iterate -- --scenario playwright/skeleton-scenarios/conference-participant-chat.preview.json
```

| Modus | Hva skjer |
|-------|-----------|
| `preview` | Laster flaten, setter kladden, tester og tar skjermbilder. Lagrer ingenting. |
| `commit-runtime` | Som preview, men trykker **Bruk** og sjekker at endringen overlever en ny økt. Krever kildebasert flate. |
| `review` | Som preview, og lager en pakke for vurdering: kandidat-JSON, diff, skjermbilder, DOM-tekst, konsoll og feil. |

Resultatene ligger i `test-results/skeleton-iterate/…`. Å gjøre endringen
permanent i Swift-koden (fabrikken) er et eget, bevisst steg etter at
runtime-resultatet er godkjent.

Agenten skal ikke bytte til **Vis** under forhåndsvisning (det lagrer, se 5).

---

## 9. Sjekke at flaten virker

**Formål:** Vite at det du lagret faktisk fungerer for den som bruker flaten.

- **Inspector → Dokument** viser *Struktur OK*, eller advarsler som
  «Bindings uten matchende reference» (et element peker på en celle flaten ikke
  har koblet til) og «Ubrukte references».
- *Struktur OK* betyr at oppskriften henger sammen. Det betyr **ikke** at alle
  knapper kan nås. En seksjon som er skjult bak en betingelse som aldri blir sann,
  vises aldri, og det kommer ingen feilmelding.
- Test derfor selv: trykk hver knapp, fyll hvert felt, og sjekk på mobilbredde.
- Utviklere kjører `SkeletonReachabilityAudit` (CellBase) for å finne elementer og
  handlinger som aldri kan nås.

---

## Vanlige problemer

| Problem | Årsak | Løsning |
|---------|-------|---------|
| **Rediger** gir feilmelding | Flaten er «Kun lesing» for deg. | Be eieren om skrivetilgang. |
| **Bruk** er grå | Ingen endringer i kladden. | – |
| Endringen forsvant etter at jeg byttet flate | Flaten var ikke kildebasert; endringen gjaldt bare økten. | Lagre via Studio (7). |
| Endringen ble lagret selv om jeg ikke ville | Du trykket **Vis** med ulagrede endringer. | Forkast før du trykker Vis. Angre ved å redigere tilbake. |
| Teksten er tom / knappen gjør ingenting | Feil `keypath`, eller cellen er ikke koblet til flaten. | Sjekk advarslene i **Inspector → Dokument**. |
| Ingen «Legg til her» dukker opp | Delen passer ikke i områdene flaten tilbyr. | Prøv rotnivå, eller be eieren åpne en slippsone. |
| «Editable configuration revision is stale …» | Noen lagret samtidig. | Last på nytt og gjør endringen igjen. |

---

## Kjente begrensninger (22.10.2026)

- Redigering finnes bare i Porthole på web, ikke i HAVEN-appen.
- Paletten har bare sammensatte komponenter; enkeltelementer og flytting mangler.
- Inspektøren endrer bare enkle verdier (tekst, tall, av/på).
- **Vis** lagrer ulagrede endringer.
- Ingen knapp for å tilbakestille til bibliotekets original.
- CellConfiguration-JSON i Porthole kan bare leses og kopieres, ikke redigeres der.

Forslag til forbedringer ligger i [Skeleton_Redigering_Forslag.md](Skeleton_Redigering_Forslag.md).

## Se også

- [README.md](README.md) – alle brukermanualer
- `CellScaffold/Documentation/Skeleton_Runtime_Iteration_Workflow.md`
- `CellScaffold/Documentation/CellConfiguration_Library_and_Variant_Architecture.md`
- `Book/12_Skeleton_Spec.md` og `Book/22_Explore_Contracts_For_Skeleton_Authoring.md`
