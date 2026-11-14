# Lag din egen flate i HAVEN

En guide for masterstudenter som vil sette opp egne dashboards og flater, med hjelp fra en KI-assistent.

*Skrevet 14.11.2026 fra koden på CellScaffold `8e8f8e0` (det som kjører på staging) og CellProtocol `14fd9dc`. Stegene på staging er ikke gått gjennom med en ny konto ennå. Står du fast, si fra til Kjetil.*

## Kort fortalt

En flate i HAVEN er en **CellConfiguration**: en JSON-fil som sier hvilke celler flaten bruker (`cellReferences`) og hvordan den ser ut (`skeleton`). Den samme fila vises i nettleseren (Porthole) og i appen (Binding). Du trenger ikke kompilere noe for å lage en ny flate.

Arbeidsflyten i dag:

1. Du beskriver flaten for din egen KI-assistent (Claude Code, Codex eller en annen), som har fått skeleton-skillen fra CellProtocol.
2. Assistenten skriver en CellConfiguration-fil.
3. Du laster fila opp i **Cell Configuration Studio** på staging og ser en forhåndsvisning.
4. Du retter, laster opp på nytt, og lagrer en privat versjon når du er fornøyd.

HAVEN på staging har ennå ingen språkmodell som studenter kan bruke til dette. Det jobbes med, og guiden oppdateres når det er på plass. Til da gjør assistenten din jobben lokalt.

## 1. Gi assistenten din skeleton-skillen

Skillen er en instruks som sier hvilke elementer som finnes, hvordan data kobles inn, og hva den skal nekte å finne på. Den ligger i det offentlige CellProtocol-repoet:

```bash
git clone https://github.com/Digipomps/CellProtocol.git
ls CellProtocol/commons/skills/cellconfiguration-skeleton-authoring/
#   SKILL.md   references/schema-and-limits.md   references/examples.md
```

- **Claude Code:** kopier mappen til `~/.claude/skills/cellconfiguration-skeleton-authoring/`. Claude bruker den når du ber om en CellConfiguration eller et skeleton.
- **Codex og andre:** be assistenten lese `SKILL.md` og `references/schema-and-limits.md` før den skriver noe, eller pek på dem fra `AGENTS.md` i ditt eget repo.

Gi assistenten også CellProtocol-kildene, så den kan sjekke mot koden og ikke mot hukommelsen:

- `CellProtocol/Sources/CellBase/CellConfiguration/CellConfiguration.swift`
- `CellProtocol/Sources/CellBase/Skeleton/SkeletonDescription.swift`
- `CellProtocol/Sources/CellBase/Skeleton/SkeletonReachabilityAudit.swift`

Kjenn til to ting ved skillen slik den er nå:
- Den nevner stier på Kjetils maskin (`/Users/kjetil/...`) og kommandoen `npm run skeleton:iterate` fra den private CellScaffold. Du har ikke disse. Bruk Studio på staging i stedet (steg 3).
- Lista over elementer i `schema-and-limits.md` mangler noen som finnes i koden. Listen under er hentet fra koden.

## 2. Hva en flate kan inneholde

Elementene som finnes i `SkeletonElement` i dag:

| Gruppe | Elementer |
|---|---|
| Oppsett | `VStack`, `HStack`, `ZStack`, `Grid`, `ScrollView`, `Section`, `Tabs`, `NavigationBar`, `Spacer`, `Divider` |
| Tekst og bilde | `Text`, `Image` |
| Inndata | `TextField`, `TextArea`, `Toggle`, `Picker`, `Button`, `FileUpload` |
| Data | `List`, `Tree`, `Object`, `Reference`, `Visualization` |
| Annet | `Audio`, `AudioQueue`, `ComponentSurface`, `AttachmentField` (eldre) |

Finnes ikke: `Markdown`, `Chart` (bruk `Visualization`), `Video`, `Map`, `Table`, `WebView`, `DatePicker`. Ber du om noe som ikke finnes, skal assistenten si det, ikke finne på et element. Nye elementer krever endringer i renderen, og det avtales med Kjetil.

### Data inn og ut

- `cellReferences` kobler inn en celle og gir den et navn (`label`). Eksempel: `cell:///Todo` med `label: "todo"`.
- En `keypath` leser fra cellen: `todo.activeItems` er lista over aktive gjøremål.
- En `Button` med `keypath: "todo.toggleTodo"` skriver til cellen. Inne i en liste kan knappen ta verdien fra raden med `payloadKeypath: "id"`.
- Inne i en `List` leser `keypath` fra raden: `title` er tittelen på det gjøremålet raden viser.

Hvilke keypaths en celle har, finner du i **Cell Configuration Architect** under katalogkontraktene, eller i cellens kildekode.

## 3. Forhåndsvis i Cell Configuration Studio

1. Logg inn på `https://staging.haven.digipomps.org`.
2. Åpne **Cell Configuration Architect** (eller **Cell Configuration Studio**) fra biblioteket.
3. Under «Last opp privat CellConfiguration-utkast» drar du fila inn eller velger den. JSON, maks 512 KB.
4. Studio viser utkastet og en forhåndsvisning.
5. Trykk «Lagre ny privat versjon» når du vil ta vare på det. Du kan gå tilbake til en tidligere versjon.

Utkastet er ditt og privat. Det publiseres ikke, og ingen andre ser det.

Vil du heller endre en flate som finnes, direkte i Porthole, står det i manualen [Endre en flate](Skeleton_Redigering.md).

Forhåndsvisningen kjører ikke `setKeysAndValues` og abonnementer. Knapper og felt treffer cellene for alvor, og cellene sjekker tilgangen din som vanlig.

## 4. Et eksempel: mitt gjøremålspanel

Ber du assistenten om «et panel som viser gjøremålene mine og lar meg krysse dem av», bør du få noe slikt:

```json
{
  "name": "Mitt gjøremålspanel",
  "cellReferences": [
    { "endpoint": "cell:///Todo", "label": "todo", "subscribeFeed": true, "subscriptions": [], "setKeysAndValues": [] }
  ],
  "skeleton": {
    "VStack": [
      { "Text": { "text": "Mine gjøremål" } },
      { "List": {
          "keypath": "todo.activeItems",
          "flowElementSkeleton": {
            "HStack": [
              { "Text": { "keypath": "title" } },
              { "Text": { "keypath": "dueText" } },
              { "Button": { "keypath": "todo.toggleTodo", "label": "Ferdig", "payloadKeypath": "id" } }
            ]
          }
      } },
      { "Section": {
          "header": { "Text": { "text": "Fullført" } },
          "content": [
            { "List": { "keypath": "todo.completedItems",
                        "flowElementSkeleton": { "Text": { "keypath": "title" } } } }
          ]
      } }
    ]
  }
}
```

`Todo` er din egen celle (én per identitet), så panelet viser bare dine gjøremål. Eksempelet er laget fra koden og ikke prøvd på staging ennå.

## 5. Feller du bør kjenne

- **En seksjon som er skjult med en betingelse på toppnivå, vises aldri.** `modifiers.visibility` på toppnivå har ingen data å sjekke mot, og blir usann. Flaten ser ferdig ut, men knappene der er borte. Legg innhold som skal komme og gå inne i en `List`: en tom liste viser ingenting.
- **Sjekk at alle handlingene du trenger, faktisk kan nås.** `SkeletonReachabilityAudit.reachableActionKeypaths(_:)` i CellBase lister dem. Mangler en handling flaten er laget for, er flaten ikke ferdig, selv om JSON-en er gyldig. Studio kjører ikke denne sjekken ennå.
- **`styleRole` og `styleClasses` er hint, ikke stil.** Flaten må virke uten dem.
- **En knapp gir ingen rettigheter.** Hver handling sjekkes av cellen mot Agreement-en din. Får du «denied», er det tilgang, ikke JSON.
- **En `TextField` med `targetKeypath` kan sende mens du skriver.** Pek den på et utkast-felt, og la en knapp sende, i stedet for å peke den rett på en handling som lager noe.

## 6. Samarbeid

HAVEN er laget for samarbeid, men Studio-utkast er private i dag. Til dette er på plass kan dere:

- dele JSON-fila (for eksempel i en gruppesamtale på staging, eller i et felles repo) og laste den opp hver for dere
- snakke om flaten i samtalen dere har med veileder

Deling av utkast med navngitte personer, og å vise et delt utkast fra en samtale, er planlagt.

## 7. Hva som er på vei

| Hva | Status 14.11.2026 |
|---|---|
| Studio sier fra når en flate skjuler sine egne knapper | Planlagt |
| «Beskriv flaten» i Studio: modellen lager utkastet for deg | Planlagt, venter på at studentene får modelltilgang |
| Workbench-hjelperen svarer på flate-bestillinger i stedet for «forsto ikke» | Planlagt |
| `skeleton-check`: sjekk en fil lokalt med CellBase | Foreslått |
| Del et utkast med en medstudent, og vis det fra chat | Planlagt |
| Oppdatert offentlig skeleton-skill med alle elementer | Planlagt |

Spør Kjetil om status før du bygger oppgaven din på noe i denne tabellen.
