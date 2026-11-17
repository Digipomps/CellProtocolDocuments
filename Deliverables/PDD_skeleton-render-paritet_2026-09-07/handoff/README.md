# Overlevering til Codex — skeleton-render-paritet

Til: Codex (ChatGPT 6 Astra), kjørt av Kjetil fra egen terminal
Fra: Losen, 2026-09-07
Formålsspesifikasjon: `../FORMAALSSPEC.md` — **les den først, den er kontrakten**

---

## Objektiv

Fem ting skal være sant for hver lokale flate i HAVEN:

1. alle elementer virker
2. dataene som vises er relevante
3. flaten oppfyller sitt erklærte formål
4. den rendrer effektivt
5. den ser lik ut i HAVEN-appen og i web-rendereren

Punkt 1, 3 og 4 har allerede maskineri. Punkt 5 har en matrise som ikke måler
native. Punkt 2 har ingenting. Det er der arbeidet ligger.

## Hva «likt» betyr — Kjetils ord, 2026-09-07

> «samme elementer, rekkefølge, tekst, tilstand og handlinger, med en nedskrevet
> toleranse for typografi og spacing — men det skal være lett gjenkjennelig at
> det er den samme flaten.»

Skrevet ut i **§3b** i spesifikasjonen som tre nivåer. Sammendraget her er ikke
kontrakten — §3b er:

- **Nivå 1, ingen toleranse:** elementsekvens, synlig tekst (trimmet; ingen
  JSON-hermetegn, rå keypath eller UUID), tilstand (tom/fylt/feil),
  `reachableActionKeypaths` som identiske mengder. Avvik her er en feil.
- **Nivå 2, toleranse:** skriftfamilie og absolutt skriftstørrelse kan avvike;
  **relativ typeskala innenfor ±10 %**; avstand **±25 % eller ±4 pt**, det
  største; linjebrytning fritt (antall linjer er ikke et avvik, innholdet er);
  farge etter rolle — eksakt verdi kan avvike bare der rollen **ikke** er i
  `agreedRoles`.
- **Nivå 3, gjenkjennelighet:** samme visuelle hierarki, gruppering og vekting av
  primærhandlingen. **Dette er ikke en toleranse — det er en kontrakt som ikke
  finnes ennå.** Les neste avsnitt før du planlegger noe rundt det.

Sammenligningen skjer på et skeleton normalisert med
`SkeletonStyleParity.normalizedForParity(...)`.

---

## Andre hovedfunn: normalisatoren skjuler et ekte avvik

`SkeletonStyleParity.agreedRoles` er **tom med vilje**. Men bildet rundt den er
ikke det filen tror:

| | Antall |
|---|---|
| Distinkte `styleRole` appens flater faktisk setter | **34** |
| Roller web styler via `.style-role-<navn>` i CSS | **61** |
| **Av appens roller: stylet av web, ikke av SwiftUI** | **5** |
| Av appens roller: tolket av SwiftUI, ikke av web | 2 |
| Av appens roller: ingen rendrer tolker | **27** |
| Av appens roller i `agreedRoles` | **0** |

`skeleton-runtime.js:4027` legger på `style-role-<navn>` som CSS-klasse for
**hver eneste** rolle, betingelsesløst. `SkeletonStyleParity.webOnlyRoles` kjenner
bare de tre JS-spesialbehandlede (`admin-page-heading`, `admin-section-heading`,
`admin-form-field`) — og de tre har ikke engang en CSS-regel. De 61 CSS-drevne
rollene er den fila ikke vet om.

Fem av appens roller er i denne gruppen: `chat-active-tool-chip`,
`chat-active-tool-chips`, `chat-helper-tabs`, `chat-helper-tabs-compact`,
`chat-prompt-log`. Web styler dem, SwiftUI ikke.

**Presist hva feilen var:** `classify` returnerer `nil` bare for roller i
`agreedRoles` — alt annet strykes fra JSON-en uansett `TokenKind`. Strykingen
var riktig. Feilen var **merkelappen**: de fem ble rapportert som `.unclaimed`,
«ingen rendrer tolker den». Funnstrømmen fra `normalizedForParity` — det eneste
stedet som sier hva som ble valgt bort fra sammenligningen — sa at forskjellen
ikke fantes.

> **Dette er allerede rettet.** Kjetil ba om det utenfor porten 2026-09-07.
> Endringen ligger i `../patch/` med `apply.sh` som lager worktrees fra
> origin/main, kopierer inn, bygger og tester. **Den er ikke kompilert** — det
> finnes ingen Swift-verktøykjede i Cowork-VM-en. Kjør `apply.sh --apply` og se
> hva som faller ut før du bygger videre på den.

**Rollene som bærer flatene** — alle i gruppen «ingen rendrer tolker»:
`personal-list-row` (35 bruk), `personal-key-value-block` (7),
`personal-audit-row` (5), `personal-hero` (4), `personal-card` (4),
`personal-section-header` (3), `tabstrip` (2).

Nivå 3 er ikke oppnåelig ved å måle piksler. **Kjetil har besluttet første
pulje** (2026-09-07): `personal-list-row`, `personal-key-value-block`,
`personal-hero`, `personal-card`, `personal-section-header`, `tabstrip`.

Regelen som følger med: en rolle føres inn i `agreedRoles` **og** implementeres
i både `skeleton-runtime.js` og `SkeletonView.swift` i samme endring. Legger du
den inn uten implementasjon gjør du det motsatte av hensikten — da slutter
`normalizedForParity` å stryke rollen, og målingen begynner å sammenligne noe
bare den ene rendreren tolker. Dette er P3, bak G2.

---

## Portene — ikke hopp over dem

Dette er en GUI-oppgave, så:

- **G1** — Kjetil godkjenner FORMAALSSPEC.md. Ingen plan før det.
- **G1-GUI** — Kjetil godkjenner et *rendret bilde* per flate og tilstand. Ingen
  implementering før det. En tekstlig beskrivelse teller ikke
  (`lesson.text-ux-is-not-design`).
- **G2** — Kjetil godkjenner PLAN.md.
- **G3** — akseptanse mot §3.

`python3 Tools/PurposePackages/purpose_dev.py gates <mappe>` viser tilstanden.
Sett aldri en port på Kjetils vegne.

§6: fire spørsmål er besvart av Kjetil 2026-09-07 — hva «likt» betyr, at **web
slik den er i dag er fasit**, hvilke seks roller som blir normative, og at
`SkeletonStyleParity` skulle rettes med én gang. Tre står åpne (ytelsesterskel,
hvem som dømmer datarelevans, rekkefølgen på de seks rollene). Ingen av dem
blokkerer G1.

---

## Første hovedfunn: paritetspåstanden er kildeinspeksjon, ikke rendering

`CellScaffold/Tests/fixtures/SkeletonElementParityMatrix.v1.json` har 24 caser.
Den leses av:

- `CellScaffold/Tests/AppTests/SkeletonElementParityMatrixTests.swift`
- `CellScaffold/playwright/skeleton-element-catalog.spec.js`
- `CellScaffold/playwright/skeleton-real-configuration-corpus.spec.js`

**Ingen fil i Binding refererer den.** Native-siden av hver case står som
`"binding": "source-inspected-explicit-switch"` — altså: noen har lest Bindings
switch-setning fra CellScaffold og konkludert. Det er nøyaktig
`lesson.tested-a-different-path-than-production`: en test som sier noe om hva
brukeren ser, må gå gjennom produksjonens egen kodevei.

Første konkrete leveranse er derfor `test.parity.matrix-native`: en XCTest i
Binding som leser den samme fixturen og rendrer hver case gjennom
`BindingSkeletonView`. Da måler begge sider det samme, fra samme kilde.

---

## Tilstand du kan stole på (verifisert, med kilde)

| Påstand | Bevis |
|---|---|
| Korpuset er eierens egne flater, ikke hjelperens liste | `BindingTests/CellConfigurationVerifierXCTest.swift:436–454`, feiler hvis korpuset < appens meny |
| Uoppnåelige elementer fanges | `testNoLocalSurfaceHidesItsOwnWaysIn` + `SkeletonReachabilityAudit` (`CellProtocol/Sources/CellBase/Skeleton/SkeletonReachabilityAudit.swift:65`) |
| Lastetid er målt | 74 av 77 lokale flater < 100 ms; sum 4 430 ms; median 1 ms (`Binding/_audit-skeleton-render-20260828/reports/surface-audit-20260902T214435Z.json`) |
| Tre flater bruker fortsatt ~1400 ms | `Trusted Issuers Registry`, `Identities Access Control`, `Cloud Bridge Transport` — `subscribeFeed: true`, men feeden blir aldri aktiv |
| Render er **ikke** målt i produksjonens vei | tallene (median 178 ms) kommer fra NSHostingView + PNG-snapshot i testharnessen |
| 26 røde flater er fjernvert, ikke renderer | manglende bro-rute, eget spor (`Binding/Documentation/HAVEN_Bro_Forensikk_og_Status_2026-09-02.md`) |
| 5 flater tilbys uten at cellen finnes | `SkeletonParityTextFixture`, `DiMyWallet`, `DiMyAccess`, `DiMyPricingPolicy`, `agent/network/sentinel` |

## Verktøy som finnes — bruk dem, ikke lag nye

- `BindingTests/CellConfigurationVerifierXCTest.swift` — korpus, reachability,
  lastetid, statisk strukturaudit.
- `BindingTests/RemoteSurfaceRenderAuditXCTest.swift` — fasene
  `local|bridge|http|load`, JSON- og Markdown-rapport. Kjøres med
  `zsh Binding/_audit-skeleton-render-20260828/run_surface_audit.sh`.
  **Merk:** dette verktøyet er mitt, og det bruker `CellConfigurationVerifier`,
  ikke produksjonens rendersti. Målingene fra det duger til lastetid og
  regresjon, men **ikke** som bevis på hva brukeren ser. Bruk det til å finne
  kandidater, ikke til å erklære paritet.
- `CellScaffold/scripts/skeleton-iterate.js` — endre en skeleton i runtime uten
  å bygge om. `--mode export` er read-only. Krever `--base-url`; uten den
  treffer den en levende server.

---

## Miljø — dette har kostet tid før

| Ting | Tilstand 2026-09-07 | Konsekvens |
|---|---|---|
| `codex-local` MCP | **Astra virker i ChatGPT-appen** (bekreftet med skjermdump 2026-09-07), men MCP-serveren avviser `gpt-6-astra` med «requires a newer version of Codex». Kontoen aksepterer ingen andre modeller (`gpt-5.2-codex` og `gpt-5.1-codex` avvises som «not supported with a ChatGPT account»), saa MCP-veien er stengt. Codex ligger inne i ChatGPT.app og naas via symlinken `~/.local/bin/codex` - en oppgradering kan la den peke paa forrige bundle | Kjoer Codex fra appen eller `codex exec`. Skal MCP-veien tilbake: `ls -l ~/.local/bin/codex; ~/.local/bin/codex --version; find /Applications/ChatGPT.app -type f -name codex` - er versjonen eldre enn appens, er symlinken foreldet |
| Playwright fra Codex' sandkasse | virker ikke — `MachPortRendezvousServer … Permission denied` | web-screenshots tas av Kjetil eller i CI |
| git fra Cowork-mounten | ødelegger — etterlater `.lock` mounten ikke får slettet | all git fra macOS-terminalen |
| `swift build` i CellScaffold | går via `haven-swiftpm.sh` | dør med exit 64 hvis cache-katalogen mangler markørfila `.haven-swiftpm-cache-v1` (innhold: `haven-swiftpm-cache-v1`) |
| Hovedtreet i CellScaffold | 226 commits bak origin/main | lag worktree fra `origin/main`, les aldri hovedtreet som «det som kjører» |
| Test-målet i AppTests | brekker på nye `SkeletonElement`-caser | `swift test --filter X` som ikke finner noe ser ut som suksess — sjekk at målet kompilerer |

---

## Arbeidsrekkefølge

**Stopp etter hvert punkt som har en port.**

1. Les `../FORMAALSSPEC.md` — hele, den er kontrakten. §6 er besvart; det som
   gjenstår er Kjetils ord på at spesifikasjonen som helhet er godkjent. → **G1**
2. Ta web-referansebilder for hver lokale flate og hver viktig tilstand
   (tom, fylt, feil) i én fast viewport. Legg i `../images/` som
   `<flate>-<tilstand>-web-v1.png`. → **G1-GUI**
3. Skriv PLAN.md, én arbeidspakke per bladformål i §1, hver med sin test fra §5
   og en navngitt utfører. → **G2**
4. Implementer, i denne rekkefølgen fordi hver bygger på forrige:
   a. `test.parity.style-parity-knows-web-css` — **skrevet, ikke kompilert.**
      Ligger i `../patch/`. Kjør `bash ../patch/apply.sh --apply` først; retter
      den seg ikke, er alt som måles etterpå målt med feil instrument.
   b. `test.parity.matrix-native` — Binding leser paritetsmatrisen og rendrer
      hver av de 24 casene. Dette er den som gjør resten målbar.
   c. `test.parity.real-corpus` — utvid matrisen til elementtypene som faktisk
      forekommer i eierens flater; feil hvis en type mangler case.
   d. `test.elements.execute` — hver statisk knapp gjennom rendererens egen
      eksekveringsvei; ikke `notFound`, ikke `denied`.
   e. `test.purpose.actions-exist` — `discovery.purpose` → navngitte handlinger →
      finnes i `reachableActionKeypaths` og gjør noe.
   f. `test.data.relevance` — den automatiserbare halvdelen: ingen synlig verdi
      er tom, teknisk eller et JSON-sitat. Dommen per flate er Kjetils.
   g. De tre flatene på ~1400 ms.
5. TESTRESULT.md med ekte utdata under hver anker. En test som ikke kunne kjøres
   er `blocked` med grunn — aldri stilltiende utelatt.
6. ACCEPT.md: forventning mot faktisk, per rad i §3. GUI side om side. → **G3**
7. Lærdommer inn i registeret: `purpose_dev.py lesson add <mappe>`.

## Regler

- Ingen ny elementtype og ingen nye felter i skeleton-formatet uten at Kjetil har
  sagt ja. Treffer du grensen: stopp og legg det fram.
- Ikke fjern eller svekk en eksisterende test for å få noe grønt.
- Skriver du en test som skal si noe om hva brukeren ser: bruk produksjonens
  egen funksjon med produksjonens egne inndata.
- Et dokument om leveransen er aldri leveransen.
- Fjerner du en egenskap for ytelse: skriv en post i
  `CellScaffold/Documentation/ProjectControl/VIRKER_OG_VIRKER_IKKE.md`, ikke bare
  en kodekommentar. Det har skjedd to ganger.

## Åpne spørsmål jeg ikke har svart på

- Er `SkeletonElementParityMatrix.v1.json` riktig sted for et delt korpus, eller
  bør det flyttes til CellProtocol så begge klientene eier det likt? Den bor i
  CellScaffold i dag, som gjør web til implisitt fasit.
- De 24 casene er syntetiske fixtures. Hvor mange av elementtypene i eierens
  faktiske flater er dekket? Det er ikke talt.
- 56 roller styles av web uten at appen noen gang setter dem (`publisher-*`,
  `resource-match-*`, `admin-*`). Er det en web-only-flatefamilie som aldri skal
  finnes i appen, eller er det etterslep? Det avgjør om de skal med i
  `webOnlyRoles` eller ryddes bort.
- Er `personal-card` og `personal-list-row` med `role:`-overstyring egentlig én
  rolle med varianter? 31 av de 35 `personal-list-row`-bruken kommer fra
  `listCard(role:)`. Hvis varianter er meningen, må `agreedRoles` håndtere det —
  i dag er den en flat mengde strenger.
