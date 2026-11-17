# patch — SkeletonStyleParity kjenner ikke web-stilarket

Rettet 2026-09-07 på Kjetils ord, utenfor porten, fordi det er en defekt i
eksisterende kode som gjør enhver paritetspåstand mindre verdt så lenge den står.

## Hva som var galt

`applyElementModifiers` i `CellScaffold/Public/js/skeleton-runtime.js:4027`
legger på klassen `style-role-<navn>` for **hver eneste** rolle, betingelsesløst.
Web styler derfor en rolle så snart det finnes en `.style-role-<navn>`-regel —
uten at noen har skrevet spesialkode for den. Det er 61 slike regler i
`Public/css/porthole-webo.css` og `Public/css/conference-mvp.css`.

`SkeletonStyleParity.webOnlyRoles` inneholdt bare tre roller: de JS-spesial-
behandlede `admin-page-heading`, `admin-section-heading`, `admin-form-field` —
som ikke engang har en CSS-regel. De 61 var fila ukjent.

Fem av dem er i bruk i appens egne flater: `chat-active-tool-chip`,
`chat-active-tool-chips`, `chat-helper-tabs`, `chat-helper-tabs-compact`,
`chat-prompt-log`. Web styler dem, SwiftUI ikke.

**Presist hva konsekvensen var.** `classify` returnerer `nil` bare for roller i
`agreedRoles`; alt annet strykes fra JSON-en uansett `TokenKind`. Strykingen var
altså riktig. Feilen var **merkelappen**: de fem ble rapportert som `.unclaimed`,
hvis egen dokumentasjon sier «ingen rendrer tolker den». Funnstrømmen — det
eneste stedet som forteller hva som ble valgt bort fra sammenligningen — sa at
forskjellen ikke fantes.

## Hva som er endret

| Fil | Endring |
|---|---|
| `CellProtocol/Sources/CellBase/Skeleton/SkeletonStyleParity.swift` | `webOnlyRoles` splittet i `webJavaScriptRoles` (3, JS-spesialbehandlet) og `webStylesheetRoles` (61, generert fra CSS-en). `webOnlyRoles` er nå unionen. `.unclaimed`-dokumentasjonen retter påstanden om at CSS-treff bare *kan* skje |
| `CellScaffold/Tests/AppTests/SkeletonStyleParityCSSDriftTests.swift` | Ny. Skanner `Public/**/*.{css,html,js}` og feiler med differansen mot `webStylesheetRoles`, med filnavn per rolle. Lista bor i ett repo og reglene i et annet — uten denne driver de fra hverandre |

`SkeletonStyleParity.BASE.swift` er fila slik den var, for diffing.

## Kjør

```
bash apply.sh            # tørrkjøring, endrer ingenting
bash apply.sh --apply    # worktrees fra origin/main, kopier, bygg, test
```

Skriptet stopper med exit 65 hvis `SkeletonStyleParity.swift` på origin/main
ikke lenger er fila endringen ble laget mot — endringen erstatter hele fila.

## Ikke verifisert herfra

Det finnes ingen Swift-verktøykjede i Cowork-VM-en. **Endringen er ikke
kompilert og testene er ikke kjørt.** Verifisert er bare:

- de 61 rollene er identiske i hovedtreet og i et worktree fra 5. september
- ingen kollisjon mellom `webStylesheetRoles` og `nativeOnlyRoles`, så den
  eksisterende `isDisjoint`-invarianten i `SkeletonStyleParityTests` holder
- `agreedRoles` er tom, så `agreedRoles.isDisjoint(...)` holder trivielt
- klammebalanse og at konstanten har 61 oppføringer
- `SkeletonStyleParity.swift` er byte-identisk med origin/main før endringen

`apply.sh` er det som avgjør om den kompilerer.

## Ikke gjort her

De seks rollene Kjetil godkjente — `personal-list-row`,
`personal-key-value-block`, `personal-hero`, `personal-card`,
`personal-section-header`, `tabstrip` — er **ikke** lagt inn i `agreedRoles`.
Det er med vilje. En rolle føres inn der *og* implementeres i begge rendrerne i
samme endring; legger man den inn uten implementasjon slutter
`normalizedForParity` å stryke den, og målingen begynner å sammenligne noe bare
web tolker. Det er P3-arbeid bak G2.
