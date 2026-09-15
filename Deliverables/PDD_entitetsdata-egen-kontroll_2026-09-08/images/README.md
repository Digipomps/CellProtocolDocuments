# Referansebilder — G1-GUI

**Disse er mockups, ikke Porthole-preview.** Flatene bor i Swift-fabrikker i Binding, som ikke har
en preview-loop (`cellconfiguration-skeleton-authoring` → «Surfaces built in Binding Swift
factories»). Bildene er rendret fra HTML i samme bredde som flaten, for å avstemme forventningen
før kode. De er akseptansereferanse for `test.gui.parity` ved P5.

| Fil | Flate | Tilstand |
|---|---|---|
| `entitet-forsegling-v1.png` | Genesis | Forseglingsøyeblikket, utløst av at data må persisteres |
| `import-tom-v1.png` | Relasjoner | Tom — droppsone og to veier inn |
| `import-forhandsbilde-v1.png` | Relasjoner | Forhåndsbilde med kontekstnavn, kolonnetolkning og advarsel |
| `entitetsdata-editor-v1.png` | Entitetsdata | Generelt redigeringsverktøy, én verdi under endring |
| `forslag-venter-signatur-v1.png` | Forslag | Modellforslag som venter på eierens signatur |
| `keypath-chat-v1.png` | Chat | Oppslag av keypath, og en endring som blir et forslag |

## Dette kan dagens skeleton rendre

Kort, dropsone, felt, knapper, skillelinjer, lister med `flowElementSkeleton`, merkelapper,
fargede meldingsbokser og seksjonsoverskrifter — alt fra `FileUpload` (med `supportsDrop`),
`TextField`, `Button`, `Divider`, `List`, `Text`, `VStack`/`HStack`, og modifierne `background`,
`cornerRadius`, `borderColor`, `shadowRadius`, `foregroundColor`, `fontStyle`, `fontSize`,
`fontWeight`, `padding`.

## Dette forfalsker bildene — les før godkjenning

1. **Tabellene.** Det finnes ingen `Table`. Radene i kolonnetolkningen, entitetsdata-listen og
   forslagsdiffen er `List`-rader, altså `VStack` per rad. Kolonnejustering må gjøres med `HStack`
   og faste bredder, eller `Grid` med `fixed`-kolonner. Den rene kolonnejusteringen i bildene er
   ikke oppnåelig som vist — forvent rader som brytes, eller et strammere `Grid` med mindre
   kontroll over bredder.
2. **Monospace på keypaths.** `SkeletonModifiers` har `fontStyle`, `fontSize` og `fontWeight`, men
   ingen dokumentert skrifttypefamilie. Den blå monospacen er uverifisert; hvis rendereren ikke
   støtter den, blir keypaths vanlig tekst i en annen farge.
3. **Chat-boblene.** `cornerRadius` er én verdi — de asymmetriske hjørnene finnes ikke. Og
   maksbredde i prosent (76 % / 86 %) er ikke i modifier-listen; `width` og `maxWidthInfinity`
   finnes, prosent gjør det ikke.
4. **Understreket lenke inne i en setning** («eller *velg en fil*»). `Text` har `url`, men blandet
   styling inne i én streng finnes ikke. Blir enten hele setningen som lenke, eller en egen knapp.
5. **De nummererte stegene** i forseglingsbildet har en smal førstekolonne. Gjøres med `HStack` og
   fast bredde; justeringen blir omtrentlig.

## En regel bildene holder, og som må holdes i koden

**Ingen av tilstandene er laget med `visible(when:)` på rotnivå.** Tomme lister rendrer ingenting,
og tekst som ikke gjelder er tom fra cellen. Det er cellen som bestemmer hva som vises, ikke en
betingelse rendereren ikke kan slå opp. Dette er `lesson.unresolvable-condition-is-invisible`, og
det er grunnen til at Relasjoner-flaten sto tom i to uker. `test.skeleton.no-unreachable-elements`
må være grønn for hver av disse flatene.
