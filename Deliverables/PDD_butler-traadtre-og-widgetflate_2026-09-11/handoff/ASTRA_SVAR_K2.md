# Astra — uavhengig gjennomgang av WP-K2

Dato: 2026-09-18. Oppdrag: `handoff/ASTRA-K2.prompt.md`.
Arbeids-ID: `astra-k2-review-20260918`. Rapportstatus: `VERIFIED` (kildelesningen er gjennomført; **ikke** kode-, test- eller produktgodkjenning).
Goal-status: `satisfied` for gjennomgangen av de seks spørsmålene.
Verdikt om listen: **NEEDS_ONE_BOUNDED_CORRECTION**.

**Listen bør ikke godkjennes som en ferdig implementasjonskontrakt slik den står.** Den fanger mange reelle geometri- og paritetsgap, men bygger delvis på en eldre arbeidsgren, behandler et omstridt arkitekturvalg som en nødvendighet, og gir en misvisende enten/eller-beslutning om testrekkefølgen. Dette kan rettes i én avgrenset korrigering av K2; funnene gir ingen autorisasjon til implementering.

De viktigste rettelsene er:

1. Ta med eksisterende `List.childrenKeypath`/`expandedStateKeypath` før E1 vurderes. Web har allerede rekursiv visning og utbretting; Binding og den sterkere, cellebekreftede trekontrakten har fortsatt gap.
2. Gjør E2 til et begrunnet arkitekturalternativ. Dagens format kan beskrive de kjente widgetmalene og lagre materialiserte undertrær med `cellReferences`. Levende binding og riktig persistens krever fortsatt celle-/vertsarbeid, men følger ikke av en ny enum-case alene.
3. Utsett det brede M7 dersom målet kan nås med eksisterende synlighetsvarianter/materialisering. Duplisert visningsmal innebærer ikke nødvendigvis duplisert kilde eller instans.
4. Behold funksjons- og formålsbevis **før CellProtocol main**, og bruk en koordinert gren-preview. Verktøyene krever ikke staging eller main; en egnet preview-vert og testdata må riktignok bygges/etableres i implementasjonsarbeidet.
5. Rett feltopptellingen, slå sammen de to klippeforslagene, og gjør de gjenværende renderer- og testkravene eksplisitte.

## Kildegrunnlag og ferskhetskontroll

`OBSERVED` betyr lest i angitt kilde. `INFERRED` er en slutning fra disse kildene, ikke kjørt bevis. `PROPOSED` betyr anbefalt korrigering. `UNKNOWN` og `NOT_FOUND_UNDER_CHECKS` brukes der undersøkelsen ikke avgjør spørsmålet.

Alle tre gapkart, hele K2-listen og handoffprompten er lest. Oppfølgingslesningen er avgrenset til fem bevisområder: format/renderere, kartdekning, celle-/komponentgrensen, test/preview og utviklerbenkens gjenbruk. Ingen generell repo-audit er kjørt.

Ferskhet er kontrollert med `git rev-parse`, `git log`, `git show`, `git ls-tree` og statuslesning. Ingen fetch, checkout, worktree-oppretting, commit, push eller annen tilsiktet Git-mutasjon er utført. **`origin/main` nedenfor er lokale remote-tracking-ref-er, ikke en fersk avlesning fra GitHub.** Produksjon og staging er ikke kontaktet.

| Repo | Lokal HEAD ved gjennomgangen | Lokalt `origin/main` brukt som kilde |
|---|---|---|
| CellProtocol | `561d34a7ea785c087bd6036921f60debe6bace4a` | `b5b7282b495e96a7899a189087592581426f4bfb` |
| CellScaffold | `942965ca24e9a418b531f9514c1da75d6d529e30` | `87256f9ac643b27fa4667ec167023249f2a2a5e6` |
| CellProtocolDocuments | `1246fa1` på `codex/docs-cleanup-20260810` | PDD-dokumentenes lokale innhold er analysert; flere er usporede |

K1-kartene oppgir selv CellProtocol HEAD `4096760…` og CellScaffold `origin/main` `649255bb…` (T:11, C:26, F:7). De er derfor ikke tilstrekkelige som beskrivelse av dagens lokale main-ref-er. Historikken viser at CP `cde2e0a` (#34, 2026-09-09) la til tre-List, og `f114588` (#26, 2026-09-05) la til itembundne modifikatorer. Begge finnes i den leste CP-mainen. CellScaffold-main pinner CP `533b42d5dc25cf1453cbe5ad08f523d47d5d32e9`; også denne bloben har tre-List og fargebindingene (PK:126–128; kontrollert med `git show 533b42d:Sources/CellBase/Skeleton/SkeletonDescription.swift`). Dette er ikke bare funksjoner på en fremtidig CP-gren.

Ingen eksisterende `ASTRA_SVAR_K2.md` eller historikk for denne svarfilen ble funnet. Søket i CP/CS-historikken etter WP-K2, ComponentSurface og layoutVariants ga ingen dokumentert ferdig K2-leveranse. Dette er `NOT_FOUND_UNDER_CHECKS`, ikke en påstand om alle andre oppgaver eller servere.

### Kildenøkler

Alle stier er relative til `/Users/kjetil/Build/Digipomps/HAVEN/`. `Nøkkel:linje` angir den presise kildeversjonen i tabellen. CP-/CS-kilder er lest som Git-blober på ref-ene ovenfor; linjene kan avvike fra arbeidskopien.

| Nøkkel | Sti / versjon |
|---|---|
| K | `CellProtocolDocuments/Deliverables/PDD_butler-traadtre-og-widgetflate_2026-09-11/handoff/SKJELETT_ELEMENTER.md`, lokal fil |
| T | Samme PDD, `handoff/SKJELETT_GAP_tre.md`, lokal fil |
| C | Samme PDD, `handoff/SKJELETT_GAP_chat.md`, lokal fil |
| F | Samme PDD, `handoff/SKJELETT_GAP_flate.md`, lokal fil |
| P | Samme PDD, `FORMAALSSPEC.md`, lokal fil |
| PL | Samme PDD, `PLAN.md`, lokal fil |
| U | `CellProtocolDocuments/Deliverables/PDD_utviklerbenk-oppgavegraf_2026-09-10/FORMAALSSPEC.md`, lokal fil |
| UC | Samme utviklerbenk-PDD, `contract/plangraf-renderer.md`, lokal fil |
| S | `CellProtocol/Sources/CellBase/Skeleton/SkeletonDescription.swift`, CP-main |
| A | `CellProtocol/Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/Suggestion/SkeletonView.swift`, CP-main |
| L | `CellProtocol/Sources/CellApple/Cells/Porthole/Utility Views/CellListView.swift`, CP-main |
| G | `CellProtocol/Sources/CellApple/Cells/Porthole/Utility Views/CellGridView.swift`, CP-main |
| Q | `CellProtocol/Sources/CellBase/CellConfiguration/CellConfiguration.swift`, CP-main |
| RA | `CellProtocol/Sources/CellBase/Skeleton/SkeletonReachabilityAudit.swift`, CP-main |
| PR | `CellProtocol/Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/SkeletonParityRenderer.swift`, CP-main |
| W | `CellScaffold/Public/js/skeleton-runtime.js`, CS-main |
| CSS | `CellScaffold/Public/css/porthole-webo.css`, CS-main |
| PK | `CellScaffold/Package.swift`, CS-main |
| IT | `CellScaffold/scripts/skeleton-iterate.js`, CS-main |
| CAT | `CellScaffold/playwright/skeleton-element-catalog.spec.js`, CS-main |
| WS | `CellScaffold/Sources/App/Controllers/PortholeWebSessionSupport.swift`, CS-main |
| WC | `CellScaffold/Sources/App/Cells/PersonalCopilot/PersonalCopilotCloudStore+WidgetCanvas.swift`, CS-main |
| WF | `CellScaffold/Sources/App/Cells/PersonalCopilot/PersonalCopilotConfigurationFactory+WidgetCanvas.swift`, CS-main |
| M | `HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html`, lokal fil |

## 1. Er E1, E2 eller M1–M11 unødvendige?

«Kan beskrives med dagens format» betyr ikke «virker allerede i begge klienter». Følgende skiller uttrykksevne, implementert rendereratferd og faktisk verifikasjon.

| Forslag | Vurdering mot dagens format og mindre vei |
|---|---|
| **E1 Tree** | **Ikke begrunnet som nødvendig for all trevisning.** `List.childrenKeypath`, `expandedStateKeypath`, `selectionValueKeypath`, `selectionStateKeypath` og `selectionActionKeypath` finnes (S:1424–1448). Web traverserer barn rekursivt med samme radmal, har ID-oppslag, utbrettknapp med `aria-expanded`, og stopper klikkpropagering ved utbretting (W:6491–6625). Påstanden om bare eksplisitt kodede, endelige nivåer gjelder den eldre nestede komposisjonen, ikke denne List-kontrakten. **Gapet er fortsatt reelt:** U2 beregner `hasChildren` fra lastede barn, utbretting er renderer-lokal, og den undersøkte native `CellListView` konsumerer ikke U2-feltene (S:1438–1445; W:6555–6557; L:172–193). E1s cellebekreftede utbretting, komplette tastaturmodell, tilgjengelighet og separate semantiske nivå/innrykk er ikke dermed levert. `PROPOSED`: sammenlign en utvidelse av U2 med ny Tree-case, med eksplisitt kompatibilitets- og eiermodell. Ingen kilde viser at akkurat en ny case er eneste løsning. |
| **E2 ComponentSurface** | **Ikke nødvendiggjort for de to kjente innholdsmalene.** `CellConfiguration.skeleton` og `cellReferences` kan holde materialiserte, instansspesifikke undertrær med levende keypath-bindinger; kildeverdier behøver ikke lagres som tekstkopier (Q:116–128,147–162; F:50–72). Dette er en representerbar løsning, ikke en ferdig livefunksjon. Monteringsregister for ukjente komponentdefinisjoner kan legitimt begrunne E2, men det er et videre krav som må skilles fra B2/B2b/B3. C:94–106 og F:72 trekker forskjellige konklusjoner; K2 har ikke adjudikert dem. Behold R3 uansett. |
| **M1 paddingInsets** | **Nytt, nyttig direkte felt; ikke bevist uunnværlig for hvert asymmetrisk mellomrom.** Dagens `padding`, `width`/`height`, stacks og spacing kan beskrive ekstra plass med indre/ytre beholdere og tomme, faste flater. T:49 bruker allerede slik komposisjon (5+3/11/27). For 11/13 kan en konstruksjon legge 11 rundt innholdet og ytterligere 2 horisontalt innen samme ytre dekorasjon. Det er `INFERRED` uttrykksevne, ikke pikselbevis; native intrinsisk størrelse/boksrekkefølge må fortsatt avstemmes (S:519–527; A:722–745; M:32). M1 reduserer kompleksitet og gjør vilkårlige logiske kanter direkte uttrykkbare. Erstatt «umulig uten» med denne begrunnelsen. |
| **M2 typografi** | **Reelt gap for de eksakte, vilkårlige typografiverdiene.** `fontStyle`, `fontSize`, `fontWeight` finnes, men ingen generell fontfamilieliste, tracking eller tabularvariant i modifiers (S:554–562). Webens `fontStyle:"body"` har allerede 1.45 linjehøyde, men det er en typografirolle og ingen garanti om identisk native linjeboks eller referansefont (W:4568–4578; A:33–45). De fire foreslåtte feltene er relevante for presis kontroll; faktisk fonttilgjengelighet er `UNKNOWN`. Tre-kartets absolutte 15-piksel linjeboks kan uttrykkes med forholdet `15/11` ved fontSize 11, hvis multiplumkontrakten faktisk gjelder linjeboksen (T:37; M:50). Ingen separat absolutt lineHeight er nødvendigvis glemt. |
| **M3 List-radskall** | **Betinget nødvendig.** For data uten Lists innebygde valg/aktivering finnes en mindre vei: énkolonne `Grid(columns:[flexible(min:0)], keypath:…, itemSkeleton:…, spacing:…)`, eventuelt materialiserte VStack-barn. Grid har spacing og repeterbar vilkårlig itemmal, og native bruker `LazyVGrid` uten CellListViews radpadding og ScrollView (S:2347–2379; W:1854–1881; G:83–119). Det løser ikke relativt dataoppslag eller identitetsbevaring automatisk: native `getItems()` får fortsatt ikke row-context her (G:100). Hvis List-valg og aktivering skal beholdes, er justerbart skall/gap reelt arbeid. M3 alene løser ikke scroll- og tomlisteproblemene i kartet. |
| **M4 størrelser/fylling/klipp** | **Delvis reelle nye kapabiliteter, delvis rendereravklaring og duplikat.** Numerisk minHeight/maxHeight/minWidth mangler generelt; fast height er ikke en maksimumshøyde (S:519–579; F:39). `Spacer` og Grid flexible-spor kan løse deler av plassfordelingen (A:852–855; G:7–17), mens webens `maxHeightInfinity` bare setter max-height 100 %, og native utvider begge akser når én infinity-ramme brukes (W:4671–4672; A:736–737). Avklar eksisterende fyllingssemantikk før alt tilskrives nytt flexGrow. **Slå sammen `clipsToBounds` med M6 `contentClip`**, eller definer en faktisk forskjell; begge er foreslått for klipping innen avrundet ramme (F:81; C:116). |
| **M5 kontrollstil/navn** | **Skill to behov.** En synlig `Button.label` kan allerede gi en lesbar knapp, men oppfyller ikke referansen med bare ⤢/✕ og et annet tilgjengelig navn (F:22; WF:65–68). `SkeletonPresentation.accessibilityLabel` navngir presentasjonen; det er ikke et generelt navn på en vanlig knapp (S:86–99). Det spesifikke navngapet er derfor reelt. `controlStyle:plain` er et mulig eksplisitt stilvalg, men nullstilling av feilaktig kant/hover og konsistent grunnstil kan også være rendererarbeid. `borderWidth:0` blir ignorert av webens >0-vakt (W:4758–4764). Ikke gjør et nytt stilfelt til forutsetning for å rette den feilen. |
| **M6 kant/skygge/klipp** | **Delvis.** Header-/footerkanter kan komponeres som egen tynn flate/Divider; begge kart nevner dette (T:20; C:39,64; F:24). `borderEdges` er dermed en forenkling, ikke eneste uttrykksvei. Eksakt stiplet kant og spread-ring med null blur mangler direkte portable felt; gjeldende web støtter bare solid kant og skygge med radius >0 (W:4758–4770; M:133,193). Dagens radius gjør ikke samme klipping på web og native (W:4718–4719; A:745). Behold én klippekontrakt, ikke to nesten like booleans. |
| **M7 layoutVariants** | **Ikke nødvendig for å oppnå full/kompakt med samme datainstans.** Eksisterende `visibility.when` kan velge to Grid-undertrær i itemkontekst; begge binder samme instans-ID og kilde. Alternativt materialiserer vert/celle valgt layout med dagens Grid/ScrollView-felt. F:88 sier allerede dette; C:133 bruker itemvariant for dokket/utvidet panel. Dette krever eksplisitt layouttilstand og bevaring av utkast/fokus/scroll, men ikke nødvendigvis nytt JSON-format (S:132–170,224–234,2347–2354). `layoutVariants` unngår dupliserte maler; det er en vedlikeholdsgevinst, ikke bevis for at B3 ellers er umulig. Se eget avsnitt nedenfor. |
| **M8 interactionStyles** | **Reelt gap for forfatterstyrt hover/focus/drag-stil.** Statisk background/opacity og itemfargebindinger beskriver ikke pekerhover eller fokus (S:519–579; W:4712–4735). Standard hover/fokus kan implementeres i rendereren uten et nytt felt; nye felter trengs dersom vilkårlige, portable per-elementverdier skal kunne angis. Presiser dessuten hvem `dragging` gjelder: kilden selv, etterkommere eller andre flater. `.msgs` og `.composer` dimmes ved en drag et annet sted i treet; selv-dragging alene dekker ikke det (M:134–135; K:122). |
| **M9 tekstdekor/transform/rotasjon** | **Delvis nødvendig.** `textTransform` kan utsettes for den faste starteroverskriften: lever korrekt ferdig tekst, slik C:120 allerede beskriver. Understrek på en ekte action og rotert railtekst er ikke direkte modifikatorer i dagens feltliste (S:519–579; C:78,84). Behold eventuelt textDecoration/textRotationDegrees for referansen, men understrek alene gir ikke inline tekstflyt rundt to knapper. `Text.url` må ikke omtolkes til en action. |
| **M10 leadingMarker** | **Begrunnet for eksakt dynamisk markør, ikke for selve skopfunksjonen.** Dagens HStack/ZStack kan tegne en stripe; den inspiserte kontrakten har ikke negativ leading-offset med top/bottom-insets uten layoutbidrag (S:519–579; W:1836–1851; T:28). K2-feltet gir en direkte vei til M:47. A2s valg og loggfiltrering kan likevel oppfylles uten denne markørgeometrien; det er det visuelle skillet i referansen som avhenger av løsningen (P:63–65). |
| **M11 paddingLeadingKeypath** | **Kan utsettes med E1; vurder også eksisterende U2.** U2-web har allerede innrykk basert på treets dybde, men ingen valgfri, itemlest leading-padding i schemaet (W:6541–6567,6650–6653; CSS:3258–3261; S:519–579). M11 har verdi hvis nøyaktig innrykk skal komme fra data uten egen Tree. Avgrensede statiske varianter finnes (T:49). K2s forslag om å utsette det når E1 har leadingInsetKeypath er fornuftig (K:125). Itembundne farger finnes nå, men de er ikke en geometribinding. |

### Mindre vei for M7

`PROPOSED`: Skill **layoutvalg** fra **nye formatfelter**. Et avgrenset panelitem kan ha for eksempel kompakt/full-modus, og eksisterende item-visibility velger en ferdig tre- eller firekolonnemal. Kildelesninger og actionpayloads beholder samme widget-ID. Verten velger et passende layoutoppsett og eier plasseringen av chat/flate. Det er allerede behov for denne vertskontrakten i R5; M7 fjerner ikke det arbeidet (K:141; F:88).

Dette er ikke en gratis løsning: lokal kontrolltilstand kan tapes ved remontering, native radoppslag må virke, og bare én relevant handlingsflate skal være aktiv. Test at full → kompakt bevarer instans, skop, utkast, valgt rad og kildeabonnement. Alternativet med `Visualization(kind:"table")` kan endre kolonner via spec, men har en annen visuell kontrakt og er ikke i seg selv pikselparitet (S:2670–2705; F:86).

Hvis én fysisk layoutmal uten duplisering blir et eksplisitt krav, kan et **smalere, navngitt variantvalg for Grid.columns** vurderes. Det er fortsatt et nytt, separat forslag; ikke en eksisterende keypath-funksjon. K2s kombinasjon av viewportClass, presentationMode, dragActive, akse, kolonner, størrelser og tilstandsbaserte farger trenger vesentlig mer semantikk enn en kolonnevariant. Dessuten er `web/app` en klientkategori, ikke automatisk en breddeklasse: en smal webflate og en bred native flate må ikke få feil layout bare på grunn av rendererens navn (M:166–185; C:125).

### E2 og hva som faktisk finnes etter #243

`OBSERVED`: Den nåværende main-koden lagrer et `sourceDescriptor` i `PersonalCopilotPinnedWidget`, men sier eksplisitt at dette er requester-/tråd-UI-tilstand, **ikke en source-backed CellConfiguration override** (WC:7–12). Program- og statradene settes til tomme lister, og footeren sier «lagret kort, uten løpende oppdatering» (WC:100–110). B2 er altså fortsatt et reelt gap. Samtidig er det misvisende å omtale B2b i denne implementasjonen som full oppfyllelse av P:88–90, som krever Portholens CellConfiguration.

Den mindre E2-veien er ikke «sett subscribeFeed og ferdig»: webverten omskriver abonnementer og bevarer bare en avgrenset mengde endpoints/labels (WS:5171–5190). R3 må levere og bevise abonnementsvei, eierskap, persistens, siste kjente verdi og feil. Hvis E2 beholdes, må dessuten **kildeidentitet skilles fra instansidentitet**: F:60 krever at to instanser fra samme kilde kan skilles; K:91 oppgir componentID, men ingen egen eksplisitt instanceID-kontrakt. Det må spesifiseres hvor instans-ID-en lever, og hvordan audit får se handlingene i den monterte definisjonen.

## 2. Mangler rader eller felt i syntesen?

**Ingen rad merket «ny modifikator» eller «nytt element» er helt uten en navngitt motpart.** Det er likevel forskjell på å nevne et felt og å dekke hele radens avvik. Følgende gir full sporbarhet for disse 37 radene: 10+12+12 modifikatorrader og 2+1+0 elementrader. De to tre-elementradene peker på samme foreslåtte Tree.

| Kart og linje | Rad / rader | Motpart i K2 |
|---|---|---|
| T:20 | `.panel.rail > header` | M1; kantkomposisjon/M6 |
| T:21 | `.panel.rail h2` | M2, R1 |
| T:23,34 | `.tree`, `.node .tw` | E1; alternativ U2 må nå med |
| T:25 | `.node:hover` | M8 |
| T:28 | `.node.sel::before` | M10 |
| T:32–33 | `.node.d1`, `.node.d2` | E1.leadingInsetKeypath eller M11 |
| T:36 | `.node .label` | M4; avkorting/innholdsbredden må også spesifiseres |
| T:37 | `.node .kind` | M1 og M2.lineHeightMultiple, med definert 15/11-konvertering |
| T:38 | `.node .count` | M2.numericVariant |
| T:40 | `.tree-foot .chip` | M1; native naturlig bredde er fortsatt semantikk |
| C:39,56,67,69,79 | panelheader, kortheader, kortfooter, actions, composer | M1/M6; klipp på kortheader og bunnplassering på composer trenger også riktig containersemantikk |
| C:40,52,74 | paneltittel, meldingsbody, starterh4 | M2; M9.textTransform er valgfritt for starterh4 |
| C:43 | `.scope-line .chip` | M1; nowrap/intrinsisk størrelse er ikke dekket bare av insets |
| C:54 | `.card` | E2 som arkitekturalternativ; motsigelsen mot F:72 må avgjøres |
| C:59 | `.card .tools button` | M8 og M5/R8 |
| C:78 | `.errline a` | M9.textDecoration; **inline tekstflyt står fortsatt uavklart** |
| C:84 | `.railview .pill` | M9.textRotationDegrees |
| F:16,17 | canvasheader/tittel | M1/M2/R1 |
| F:19,24 | canvasbody og radseparatorer | M3/M4 og M1 |
| F:22 | `.widget .tools` | M5/M1 og grunnstil |
| F:27 | `.widget .stat b` | M2.numericVariant/R1 |
| F:29 | `.placeholder` | M6.borderStyle og R4/innsettingsanker |
| F:32 | `.emptyhint` | M4.minHeight, M6.borderStyle, layoutvalg |
| F:35 | full `.row` / `.fullonly-cell` | M7 eller eksisterende Grid-varianter |
| F:36 | full `.rows` / skjult annen widget | M4 og layout-/synlighetsvalg |
| F:37 | app canvasbody | M7/M3 eller separat horisontal komposisjon |
| F:39 | app canvas-høyde under drag | M4.maxHeight og valgt layout-/dragtilstand |

**Materielle hull i dekningspåstanden:**

- **List uten tomtekst og eget rullefelt.** C:45,60,73,76 og C:135 beskriver ekstra ScrollView og «Ingen elementer» i 0/1-lister. M3s tre felt regulerer gap/insets/dekor, ikke eksplisitt tomlisteatferd eller hvem som eier scrolling. R2 gjelder dataoppslag, ikke dette. Avtal at en valgt komposisjon/repeteringsmodus ikke lager disse tilleggene. Ikke anta at `rowDecoration:none` også betyr «ingen ScrollView/tomtekst».
- **Intrinsisk størrelse og tekstflyt.** C:43 krever nowrap og innholdsstørrelse; C:78 krever actionlenker i tekstflyt. A:869–886 gir stacks full bredde, mens R7 bare navngir baseline. M4/M9 løser ikke automatisk disse kravene. Ingen ny type er dermed påkrevd, men en eksplisitt semantikk-/akseptrad mangler.
- **TextArea-dekorasjon og dragpreview.** C:80 beskriver dobbel dekorasjon; dette er ikke navngitt blant R1–R8. C:55,72 krever et faktisk kortpreview, mens R4 primært beskriver målmarkering. Hvis E2 utsettes, må kravene til eksisterende `dragPreviewRole` fortsatt ha en eier. M8 må også skille kilde-drag fra global dragtilstand (M:134–141).
- **Treoppdatering og fokus.** T:75–77 krever avklart loading/error ved forsinkede barn og fokus til forelder når et fokusert barn skjules. K:67–74 viderefører bare deler av denne kontrakten. Dette er atferd som må spesifiseres, ikke automatisk flere modifiers.

**Opptellingen er feil:** K:33 sier 12 nye modifikatorfelt. K:115–125 lister **26 forskjellige toppnivåfeltnavn**, fordelt 1+4+3+5+2+4+1+1+3+1+1 over M1–M11. Etter sammenslåing av clipsToBounds/contentClip blir det 25, før andre reduksjoner. Nested typefelter er ikke telt. «2 elementer, 11 modifikatorforslag, 26 feltnavn før deduplisering» beskriver det foreliggende forslaget presist.

## 3. Holder avgrensningene i §5?

| Avgrensning | Konklusjon |
|---|---|
| Ingen generell uttrykksmotor | **Behold.** Innrykk, skop og datavalg kan beregnes i cellen. Men setningen «ingen … betingelser … i JSON» er feil: M7 bruker eksplisitt `when: SkeletonCondition`, og formatet har allerede equals/allOf/anyOf/not (K:121,183–185; S:224–234). Skriv «ingen ny generell evaluerings-, regne- eller traverseringsmotor; avgrensede eksisterende betingelser kan gjenbrukes». |
| Ingen Card-case | **Behold.** Stacks/Grid/Button beskriver kortet, slik begge kart sier (C:92; F:5). Ikke bruk dette som indirekte bevis for at E2 likevel er obligatorisk. |
| Ingen Error-case | **Behold.** Feildata og actions kan komponeres; samtidig må 0/1-repetisjon og inline layout faktisk virke (C:76,78,129,135). |
| Ingen Disclosure-case | **Behold for denne oppgaven**, men rett begrunnelsen: utbrettingen kan høre til eksisterende U2-List eller en godkjent Tree. Det følger ikke at ny E1 må velges (S:1438–1445; W:6606–6625). |
| Ikke legg `full` til SkeletonPresentationKind | **Behold.** Enum/presentasjonsfeltene beskriver presentasjon, ikke Grid-kolonner eller parentens dokking (S:45–99; M:144–163). Eksisterende layoutvarianter ved komposisjon er også et alternativ til M7. |
| Ikke gjett breakpoint | **Behold.** Mockupen velger eksplisitt `data-viewport=app` (M:166–185). Dette beviser et behov for en avtalt layoutinngang; det beviser ikke at en ny viewportClass må inn i det portable formatet. |

App-DnD kan fortsatt være en navngitt, separat leveranse i henhold til avgrensningen (K:195–196; PL:167–172). En slik avgrensning må imidlertid være en eksplisitt unntaksrad fra akseptomfanget; den kan ikke samtidig telles som bestått T-F3 for native drag/drop.

## 4. Holder testkontrakten, og finnes preview før main?

**Retningen er riktig, men kontrakten er ikke konsistent nok til å brukes som merge-gate ennå.** K:150–154 krever fem grønne porter før CP-main; K:168–171 åpner for å merge først. Å velge sistnevnte opphever det gjengitte brukerkravet. Konflikten kommer fra den valgte stagingrekkefølgen i PL:78 og PL:181–185, ikke fra en teknisk nødvendighet om at formatet må være på main før det kan testes.

### Kildebelagte testveier før main

1. **Isolert rendererbevis på gren:** `skeleton-element-catalog.spec.js` svarer selv på nettleserforespørsler med grenens lokale runtime/CSS og fixturedata; onAction samles opp (CAT:11–47,60–86). Dette kan understøtte webfunksjons- og visuelle tester uten staging. Det beviser ikke automatisk en virkelig cellerute eller liveabonnement.
2. **Reell lokal Porthole-preview:** `Package.swift` tillater `CELLPROTOCOL_LOCAL_PACKAGE_PATH` og en navngitt lokal pakke, med publisert pin som alternativ (PK:102–128). En separat testvert kan derfor bygges med CP-kandidaten før merge. `skeleton-iterate.js` har `--base-url`, og `preview` setter working skeleton uten `editor.apply` (IT:183–201,858–862,888–899). Den inspeksjonen viser ingen main-gate. **Ny renderer/schema-kode må være bygget og lastet i verten**; å sende ny JSON til gammel staging installerer ikke WP-R.
3. **Native bevis:** samme kandidat og data må kjøres med CP-grenens native renderer i en passende Binding-/testvert. `SkeletonParityRenderer.renderPNG` bygger en ny `PortholeViewModel` og har ingen parameter for nodeliste eller action-driver; PNG-metoden alene beviser ikke T-F3 (PR:86–121).

`PROPOSED` kjøreform for senere implementasjonsverifikasjon, fra en isolert CellScaffold-testkopi **etter at en godkjent lokal vert faktisk er startet på adressen**:

```sh
node scripts/skeleton-iterate.js --mode preview \
  --base-url http://127.0.0.1:9089 \
  --scenario ../CellProtocolDocuments/Deliverables/PDD_butler-traadtre-og-widgetflate_2026-09-11/skjelett/flate.preview.json \
  --output-dir /tmp/wp-k2-flate-preview
```

Kommandoen er ikke kjørt, og adressen er ikke kontrollert som en kjørende vert. Den viser den eksisterende grensesnittmuligheten. Bruk en separat testidentitet/arbeidstilstand: preview forkaster tidligere working state før den setter kandidaten (IT:183–195). Manglende celldata må etableres på forhånd; scriptet evaluerer expects **før** actions (IT:199–201). De tre leverte scenarioene har `actions:[]`, og kartene sier at bare fylt-basisscenario er skrevet (C:155–181; F:102–123; T:112). De sertifiserer ikke tom/feil/dra/full eller chatnåbarhet av seg selv.

### Nødvendige presiseringer per port

| Port | Korrigering før kontrakten brukes |
|---|---|
| **T-F1** | Definer streng validering av nye felter: type, endelige tall, gyldige intervaller/enumerasjoner, default og negative fixtures. Dagens modifiers bruker lossy decode, og elementdekoderen kan konvertere en feil til `Unsupported` i stedet for å kaste (S:633–697,2911–2921). Test «ingen uventede Unsupported og ingen tapte obligatoriske felt», ikke bare vellykket JSONDecoder. Kravet om at også gammel `padding` må kaste ved feil vil endre dagens kompatibilitetsatferd; navngi dette som en separat endring, ikke som allerede gjeldende regel. |
| **T-F2** | Utvid audit både med barne-/radkontekst og egne actions. For E2 må materialisert/oppløst definisjon inngå i audit; sourceKeypath alene avslører ingen actions. Dagens audit går gjennom kjente undertrær og leser f.eks. Button.keypath, ikke et komponentregister eller faktisk chatadgang (RA:225–248,315–335). Negative tester må vise at utelatt action/feil kontekst faktisk oppdages. |
| **T-F3** | Kjør virkelige interaksjoner i begge renderere: payload, bekreftet tilstand, fokus/utbretting, tastatur, tilgjengelig navn og kildeoppdatering der relevant. En PNG og en henvisning til SkeletonView er ikke en kjørbar native funksjonstest (PR:86–121). Test også at skjulte varianter ikke eksponerer doble handlinger. |
| **T-P1** | Krev navngitt formål og et målbart signal, men ikke et pikselflytt for **hvert** felt. accessibilityLabel, stabile ID-er, utbrettingsaction og levende binding kan forbedre formålet uten å endre et statisk referansebilde (K:52–57,119; P:85–100). Visuelle felt må fortsatt måles mot referansen, med samme data, panelmål, skala og font. Grønn «nærmere» per felt er ikke i seg selv ferdig samlet GUI-paritet. |
| **T-P2** | Bevis en faktisk alternativ inngang fra samtalen med riktig instans/payload og effekt. `reachableActionKeypaths` over GUI-skjelettet sier ikke at samtalen kan utløse den samme handlingen (RA:79–82,198–213). B4 omfatter alle widgethandlinger, også ved komposisjon og gjennom drop-modifiers, ikke bare nye E1/E2-elementer (P:98–100). Behold testen dersom E2 utsettes. |

**Anbefalt rekkefølge:** godkjent redusert kontrakt → CP-/web-/native-kandidater med registrerte revisjoner → T-F1/T-F2 → grenens web- og nativefunksjon → T-P1/T-P2 mot isolert testvert med nødvendige cellehandlinger → først deretter CP-main. CellScaffold-PR-en kan bære integrasjonsbeviset uten å være merget først. Etter merge/deploy kjøres vanlig miljøverifikasjon i tillegg; det erstatter ikke pre-main-kravet. Det er `PROPOSED` testrekkefølge, ikke autorisasjon til å bygge, starte vert eller deploye i dette oppdraget.

## 5. Kan Tree brukes i utviklerbenkens oppgavetre?

**Ja som visnings-/valgprimitive for en projisert oppgavehierarki; nei som en komplett kontrakt for hele den bestilte benken.**

`OBSERVED`: Benkens hierarki krever én forelder eller rot, mens avhengighetsgrafen er et separat utsnitt med flere relasjonstyper (U:221–225). Tree trenger derfor ikke `parentIDs` for denne trebruken, og heller ikke en generell grafkantmodell. Node-ID, parentID, level, leadingInset, hasChildren, expanded, selected-ID og rowSkeleton kan projiseres fra oppgavene. Radmalen kan vise navn, status og kildereferanser. Delt valg mellom graf og tre kan lese/skrive samme celleverdi (U:211–212; K:49–59). Dette er `INFERRED` kompatibilitet; ingen slik fixture er implementert eller kjørt her.

**Den konkrete mangelen er flyttekontrakten.** U:211 krever at en idé kan få forelder og flyttes med hele undertreet, med syklusavvisning. E1-feltlisten har bare valg og utbretting; ingen navngitt flytteoperasjon/payload.

Dette trenger **ikke nødvendigvis et nytt Tree-felt**. En `Button` i rowSkeleton kan kalle cellens flyttehandling, eller eksisterende rowModifiers kan koble generisk dra-/slipp til den (S:568–579; K:58–59). Det som må spesifiseres i gjenbrukseksemplet er minst `move/reparent(nodeID, newParentID)` og eventuelt et innsettingsanker dersom søskenrekkefølge skal styres; sykluskontroll og faktisk flytting eies av cellen. Navnene her er `PROPOSED`, ikke eksisterende keypaths. Hvis E1 skal tilby innebygd direkte omforeldring, mangler et eksplisitt `moveActionKeypath`/tilsvarende kontraktvalg, men benkens tekst krever ikke at akkurat Tree må eie dette.

C2 ber om et dokumentert mønster og minst én annen bruk, ikke et bevis for at hele utviklerbenken dermed er levert (P:108–110). Rett derfor K:81 til: «egnet kandidat for utviklerbenkens projiserte hierarki; flyttehandling, delt valg og native paritet må konkretiseres». Lanes, grafpiler, drilldown, Utfør/Forklar og hele arbeidsflyten dekkes ikke av Tree og har egne gap (UC:31–51; U:221–236).

Hvis E1 skal vente på cellebekreftet utbretting, må gjenbruksteksten også forklare forskjellen fra benkens eksisterende U2, der utbretting er lokal (U:96; S:1438–1445). Dette er et kontraktvalg som nå er skjult av formuleringen «samme kontrakt bærer».

## 6. Overdrivelser og konkrete rettelser

| Alvor / sted | Setningen eller påstanden | Hva kilden faktisk bærer / korrigert ordlyd |
|---|---|---|
| **blocking — K:61–65,206** | «Nei betyr … nestede List i endelig dybde … utbretting … ikke kan leveres.» | U2-List har rekursiv barnelesing og webutbretting allerede (S:1438–1445; W:6541–6625). Skriv at full E1-atferd/native paritet mangler, og vurder utvidelse av eksisterende kontrakt. |
| **blocking — K:104,207** | «Nei betyr at en festet widget forblir et bilde … B2/B2b/B3 kan ikke oppfylles.» | F:50–72 beskriver eksisterende format + ny cellekontrakt som alternativ. Manglende liveimplementasjon i WC:100–110 beviser ikke at E2 er nødvendig. Gjør valget betinget av behovet for generisk definisjonsmontering. |
| **blocking — K:168–171,213** | «T-P1 og T-P2 krever staging … altså etter merge.» | IT støtter base-url/working preview; PK støtter lokal CP-pakke, og CAT laster lokale assets (IT:183–201,861,893; PK:102–128; CAT:11–47). Krever riktig kandidatvert og data, ikke main som sådan. |
| **material — K:22–31** | Listen er «det som skal til» for at flaten ser ut og oppfører seg som mockupen. | Listen alene leverer ikke A3/A4, B2c, liveabonnement/persistens, manglende scenariodata eller alle renderersemantikkene. P:66–100 og PL:83–165 skiller disse arbeidspakkene. Skriv «foreslåtte format- og rendererbidrag; øvrige celle-/vertsavhengigheter gjenstår». |
| **material — K:33–34** | «12 nye modifikatorfelt … 8 rendereravklaringer uten formatendring.» | Tabellen har 26 feltnavn. R3 er eksplisitt cellearbeid, R5 er vertsintegrasjon, og R8 omtaler det nye feltet shadowSpread (K:139,141,144). Skriv 11 grupper/26 felt før deduplisering, og «8 arbeidspunkter på tvers av renderer, vert og celle», med avhengighet til M6 i R8. |
| **material — K:81,174–177** | Samme Tree-kontrakt «bærer utviklerbenkens oppgavetre». | Visning og delt valg er plausible; flytting med undertre og syklusavvisning krever en navngitt cellehandling (U:211–212). Ikke legg til et schemafelt uten å vurdere eksisterende Button/drop-binding. |
| **material — K:208** | Uten M1/M2 er pikselparitet umulig «uansett hva annet som bygges». | Flere insets kan beskrives med komposisjon (T:49); M2 har reelle typografibegrensninger, men font og native pikselutfall er umålt (K:224–226). Begrunn hvert behov konkret, uten en universell umulighetspåstand. |
| **material — K:119,124** | M5 stopper B4; M10 stopper A2. | B4 gjelder inngang fra chat, A2 gjelder loggutvalg/skop (P:63–65,98–100). Tilgjengelig knappnavn og markørstripe tjener andre nødvendige visnings-/tilgjengelighetssignaler, men er ikke hver for seg bevis for at disse domeneformålene stopper. |
| **material — K:183–185** | «Ingen … betingelser … i JSON.» | M7 inkluderer betingelser, og formatet har dem allerede (K:121; S:224–234). Avgrensningen må gjelde en ny generell uttrykksmotor. |
| **material — K:15–16,29** | «Ingenting her er implementert» og «prod … B0+B2b+B1». | De konkret nye feltnavnene/casene ble ikke funnet i den leste schema-listen, men deler av kapasiteten finnes: U2 og itemfargebindinger. #243 ligger i lokal CS-main, mens WC:7–12 begrenser lagringen til tråd-UI-state. Prod er ikke målt her. Skriv nøyaktig hva som er kode, hva som oppfyller PDD, og hva som faktisk er miljøverifisert. |
| **editorial — K:36,233–234** | Flate-kartet har én «eksakt» rad, men «ingen rad … kan kalles eksakt». | F:11,30 avgrenser sin ene eksakt-rad til at en dropzone utelates/skjules. Det er ikke visuell runtimeparitet. Oppgi dette unntaket i stedet for motstridende generelle påstander. |

I tillegg må videre bruk av K1-kartene merke følgende historiske funn: T:7/C:110/F:86 er ikke en oppdatert totalbeskrivelse av dagens bindings-/rendererstøtte. CP-main har `hAlignmentKeypath`, `backgroundKeypath`, `foregroundColorKeypath` (S:528–556); web konsumerer dem og har wrap-håndtering (W:4674–4725). Det gjør ikke padding/fontSize dynamiske, gjør ikke List til en full Tree, og gir ikke automatisk kolonnebytte. Presise delpåstander må erstattes, ikke hele gapanalysen forkastes.

## Leveranse, dekning og begrensninger

Alle seks bestilte spørsmål er besvart, alle E1/E2/M1–M11 er vurdert, og alle 37 rader med de to etterspurte gapstatusene er koblet til K2. Ferskhetskontrollen har avdekket eksisterende trestøtte på lokale main-ref-er som syntesen må ta hensyn til. Den sterkeste støttede konklusjonen er at **arbeidet bør reduseres og presiseres før godkjenning; det er ikke vist at to nye elementer og hele M7 er nødvendig**.

Den viktigste gjenværende usikkerheten er om de mindre komposisjonsalternativene oppfyller nøyaktig geometri og tilstandsbevaring i begge faktiske klienter. Det krever implementasjons-/previewbevis, ikke mer sikker ordlyd i denne rapporten. Det er heller ikke etablert en kjørende preview-vert eller nye native funksjonstester her.

Denne gjennomgangen kjørte **ingen bygg, produkttester, nettleser, nettverkskall, deploy eller Git-mutasjon**. Referanse-HTML/CSS er lest; referansebilder er ikke målt på nytt. Ingen runtime-/piksel-/tilgjengelighetsstandard er sertifisert. Ingen eksisterende kildekode, kandidat-JSON, K2-liste, PLAN eller STATUS er endret. Eksisterende dirty arbeid i repoene er beholdt. Bare denne svarrapporten er leveransen.

Neste avgrensede handling er å korrigere K2-listen mot funnene over før Kjetil velger formatendringer. Gjennomgangen autoriserer ingen implementering.
