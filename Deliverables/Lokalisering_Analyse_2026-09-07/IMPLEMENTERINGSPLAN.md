# Implementeringsplan: lokalisering gjennom HAVEN Skeleton

> Implementeringen er startet. Første del, testresultater og gjenstående arbeid er dokumentert i [IMPLEMENTERINGSSTATUS.md](IMPLEMENTERINGSSTATUS.md). S0-prøven ga et justert Apple-valg: samme FormatJS-pakke som web, kjørt via offentlig JavaScriptCore. ICU4C er foreløpig en separat Linux/macOS-probe. Planen under beholdes som oversikt over hele omfanget.

Dato: 2026-09-07. Status: **implementeringsforslag; ingen runtime- eller schemaendringer er utført**.

Planen følger Kjetils presisering: «Det felles formatet for GUI flater i HAVEN er skeleton så det må virke effektivt i skeleton sammenheng.» Den bygger på [analysen](/Users/kjetil/Build/Digipomps/HAVEN/CellProtocolDocuments/Deliverables/Lokalisering_Analyse_2026-09-07/L1_ANALYSE.md) og [kildekontrollen](/Users/kjetil/Build/Digipomps/HAVEN/CellProtocolDocuments/Deliverables/Lokalisering_Analyse_2026-09-07/L1_KILDEKONTROLL.md). Ved forskjell i anbefalt implementering gjelder denne planens mer konkrete skeleton-design. Bibliotekvalget er fortsatt betinget av den tekniske prøven i S0.

## Formål og første leveranse

En CellConfiguration skal kunne brukes på flere språk i både Porthole web og Binding med samme skeleton, samme datanøkler og samme handlinger. En ny flate skal få lokalisering ved å deklarere tekster og argumentbindinger; den skal ikke trenge egen språklogikk.

Første leveranse er **én fungerende lokaliserbar skeleton-flate i begge renderere**, med norsk og engelsk, dynamiske tekster, språkvalg og bevarte utkast. Deretter fullføres støtten for alle tekstposisjonene i dagens skeleton-elementer, før bred utrulling til produkter. Butterpop er første produktleveranse. Interesseetiketter følger som første datadomene, men migrering av hele Interest/Purpose-modellen skal ikke blokkere generell GUI-lokalisering.

| Mål | Målbart ferdigkriterium |
|---|---|
| G1: Felles GUI-kontrakt | Samme JSON-fixture gir riktig tekst og oppførsel i web og Apple-rendereren. Ingen språkgrener i cellen som eier flaten. |
| G2: Effektiv rendering | Språkbytte bruker lokale kataloger og oppdaterer tekstbindinger. Ingen Cell-oppslag per etikett, ny dekoding av skeleton eller montering av hele flaten. |
| G3: Brukerens språkvalg | Eksisterende eierpreferanser, eksplisitt språkvalg og nettleser/OS følger én testet regel. To samtidige brukere påvirker ikke hverandres språk. |
| G4: Enkel forfatterflyt | Uttrekk, oversettelsesforslag, godkjenning, validering og pakking er repeterbart. Et tredje språk i prøveflaten krever ressurser og språkdata, ikke celle- eller rendererendringer. |
| G5: Trygg videreføring | Gamle skeletons virker som før. Tekstlokalisering endrer ikke identifikatorer, keypaths, handlinger, feltverdier eller tilgangsregler. |

## 1. Arkitekturen som skal implementeres

Flyten skal være:

```text
CellConfiguration + uendret skeleton + datatilstand
                  │
                  ├── tekstdeklarasjoner med stabile ressursnøkler
                  ├── locale-kontekst fra verten
                  └── lokale, versjonerte katalogpakker
                                  │
                  felles tekstkontrakt og test-fixtures
                         ┌────────┴────────┐
                    web-adapter       Swift-adapter
                         │                 │
                 eksisterende DOM    eksisterende SwiftUI-flate
```

«Felles» betyr samme JSON, betydning og akseptansetester. Web og Swift trenger hver sin formatteradapter. Lokalisering blir en generell del av rendererens bindinger, på samme måte som den allerede binder felt til data. Porthole og Binding leverer konteksten; cellene leverer språkuavhengige data.

### 1.1 Additiv utvidelse av skeleton

**Anbefalt justering fra analysen:** behold dagens `text`, `label`, `placeholder` og øvrige tekstfelt som strenger. Legg til én valgfri `modifiers.localization`, med en deklarasjon per tillatt tekstposisjon. Dette gir samme mekanisme på tvers av elementtyper og mindre endring i eksisterende Swift-initialiserere og JSON-forfattere enn å gjøre alle strengfeltene til unioner.

Dette er en ny, foreslått kontrakt. Den finnes ikke i dagens runtime. Valget passer eksisterende `SkeletonModifiers`, som allerede rommer både visning, tilgjengelighet og presentasjonsatferd. Dagens `SkeletonButton.label` dekodes som `String`, og web-valideringen krever også streng. [SkeletonDescription.swift](/Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellBase/Skeleton/SkeletonDescription.swift:519), [button-dekoding](/Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellBase/Skeleton/SkeletonDescription.swift:1810), [web-validering](/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Public/js/skeleton-runtime.js:360).

Foreslåtte byggesteiner:

| Byggestein | Ansvar |
|---|---|
| `CellConfiguration.localization` | Versjon, kilde-locale og katalogavhengigheter med revisjon. Kan også inneholde private/lokale katalogressurser i samme ressursformat, slik at en konfigurasjon kan være selvstendig. |
| `SkeletonModifiers.localization` | Oppslag fra godkjent tekstposisjon til en `SkeletonLocalizedText`-deklarasjon. Uten feltet gjelder dagens atferd. |
| `SkeletonLocalizedText` | Enten katalogreferanse med typede argumentbindinger, eller eksplisitt binding til en lokalisert dataverdi. Formene skal være entydige. |
| `LocalizationContext` | Ønsket og valgt UI-locale, tidssone, retning, kilde til språkvalget og aktiv kataloggenerasjon. Eies av den aktuelle flaten/forespørselen. |
| `ResolvedText` | Ferdig tekst, faktisk tekst-locale, eventuell fallback-årsak og ressursrevisjon. Brukes internt og i diagnostikk. |

Eksemplet under er **foreslått JSON for en testkonfigurasjon**, ikke en allerede støttet flate. S2 skal definere testens Explore-data med `demo.trackCount` som heltall.

```json
{
  "name": "LocalizationDemo",
  "localization": {
    "version": 1,
    "sourceLocale": "nb-NO",
    "catalogs": [
      { "namespace": "demo", "revision": "1" }
    ]
  },
  "skeleton": {
    "Text": {
      "text": "Spor",
      "modifiers": {
        "localization": {
          "text": {
            "namespace": "demo",
            "key": "trackCount",
            "arguments": {
              "count": { "scope": "root", "keypath": "demo.trackCount" }
            }
          }
        }
      }
    }
  }
}
```

Katalogmeldingen kan ha norsk `{count, plural, one {# spor} other {# spor}}` og engelsk `{count, plural, one {# track} other {# tracks}}`. En eldre klient viser den kontrollerte reserveteksten «Spor». En oppdatert klient binder `count` til data og viser korrekt melding. Bare språkbytte eller endring av `count` skal utløse ny formatering av denne teksten.

`namespace + key` er den stabile tekstidentiteten. Oversettelsesnøkler skal aldri bygges fra visningsteksten, elementets posisjon eller tilfeldig runtime-UUID. For eksempel serialiseres ikke `SkeletonText.id` i dagens CodingKeys. Det er dermed uegnet som varig oversettelsesnøkkel. [SkeletonText](/Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellBase/Skeleton/SkeletonDescription.swift:794).

### 1.2 Dynamiske labels og hva som faktisk lokaliseres

Deklarasjonsformen for en dataeid etikett foreslås som `{ "valueKeypath": "localizedLabel", "scope": "item" }`. Den skal lese et eksplisitt `LocalizedTextMap`-kompatibelt objekt med `values` og eventuell `fallbackLocale`, eller et versjonert objekt med allerede oppløst tekst og språkproveniens. Vanlige strenger skal fortsatt være vanlige strenger. Eksisterende `LocalizedTextMap` er et nyttig utgangspunkt, men dagens resolverregel må ikke antas å være identisk med den nye UI-policyen. [LocalizationContracts.swift](/Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/commons/schemas/haven.core/Sources/HavenCoreSchemas/LocalizationContracts.swift:112).

Prioritet for en tekstposisjon blir: gyldig eksplisitt lokaliseringsdeklarasjon → eksisterende dynamiske label-/tekstbinding som reserve → eksisterende statisk reservetekst. Uten deklarasjon gjelder uendret legacy-prioritet. Manglende argument, ugyldig type eller manglende katalog skal gi en kontrollert reserve og en diagnostikkpost, aldri rå ICU-syntaks eller en blank knapp. CI avviser slike feil i en konfigurasjon som publiseres som ferdig lokalisert.

| Område | Hva den felles mekanismen må dekke |
|---|---|
| Text og statiske kontrolltekster | `text`, knapp-/toggle-/navigasjonsetiketter, picker-label og placeholder. Section får tekst gjennom sine eksisterende header/footer-elementer. |
| Redigerbare felt | Placeholder og hjelpe-/kontrolltekster. `TextField.text`, `TextArea.text`, kildeverdien og utkastet er brukerdata. Språkbytte skal ikke oversette eller skrive om disse. |
| Lister, grid og referanser | Item-skeleton bruker samme tekstmekanisme og binding med eksplisitt `root`, `item` eller `context`. Ingen fjernoppslag for hver rad. |
| Tabs, Picker og autocomplete | Faste tekstposisjoner som `tabLabel` og `optionLabel`; `item` betyr her den aktuelle fanen eller kandidaten. ID, valgt verdi og handlingspayload bevares. |
| FileUpload og legacy AttachmentField | Title, subtitle, helperText, emptyTitle og emptyMessage. Knapp-, status- og feiltekster som rendereren produserer, kommer fra rendererens systemkatalog. Filnavn er data. |
| Presentasjon og tilgjengelighet | Dialogens tilgjengelighetsnavn, drag/drop-etiketter og kontrollenes oppløste navn. Etiketten lest av skjermleser skal følge den synlige, dynamiske etiketten når de skal være like. |
| Visualization | Rendererens kontrolltekster og eksplisitt deklarerte tekstfelt i støttede visualiseringskontrakter. Kart-/tabell-/diagramdata må kartlegges per faktisk kontrakt; ingen rekursiv oversettelse av vilkårlige strenger i `spec`. |
| Vert og konfigurasjonskatalog | Konfigurasjonens visningstittel/beskrivelse får deklarerte visningsreferanser. `CellConfiguration.name` bevares for eksisterende oppslag. Discovery-metadata og visningstekster må ikke få to uavhengige oversettelsesregistre. |

S1 lager en uttømmende tabell fra dagens Swift-typer og begge renderere. Den tabellen blir testgrunnlag og en versjonert liste over tillatte tekstposisjoner. `presentationAccessibilityLabel` kan for eksempel mappe til det bestemte presentasjonsfeltet; nøkkelen er ikke en fri JSON-sti. Ukjente posisjoner skal rapporteres av valideringen. Nye widgets eller manglende rendererfunksjoner inngår ikke automatisk i lokaliseringsstøtte.

`CellReference.label`, keypaths, actions, payloads, URL-er, ikonnavn, taksonomi-ID-er og profil-/fritekst skal ikke omfattes av automatisk tekstuttrekk eller oversettelse. `label` i en cellereferanse er et bindingsnavn, selv om feltet heter det samme som en knappetekst. [CellConfiguration.swift](/Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellBase/CellConfiguration/CellConfiguration.swift:110).

## 2. Rendering og effektivitet

### Last én gang, formater lokalt

Konfigurasjonen deklarerer katalogavhengighetene. Vertens bootstrap laster valgte språk og nødvendige fallback-ressurser samlet, eventuelt fra innebygde pakker. Katalogoppslag og meldingsformatering er synkrone operasjoner mot lokal tilstand etter innlasting. En senere LocalizationCell kan distribuere katalogversjoner; den skal ikke ligge i løkken som tegner hvert element.

Kataloger caches etter namespace, revisjon og locale. Ferdig kompilerte meldinger caches også etter formatterversjon og aktuelle formateringsvalg. Argumentverdier og ferdig formattert privat tekst skal ikke legges i en global delt katalogcache. Private kataloger og data har eierscope. Cacher må være begrenset og ryddes ved avmontering, eierskifte og versjonsbytte.

Katalogreferanser identifiserer registrerte ressurser. Skeleton-deklarasjoner skal ikke føre til vilkårlige HTTP-kall. Ved manglende nettverk fungerer allerede lastede eller medleverte språk; ellers vises den erklærte reserven.

### Oppdater bindinger, behold flaten

Ved første montering lages en oversikt over tekstbindinger og deres argumentavhengigheter. Ved dataendring formateres bare berørte meldinger. Ved språkbytte oppdateres eksisterende tekstnoder, etiketter, tilgjengelighetstekster og relevante formaterte visningsverdier.

På web tilføyes et eget inngangspunkt, foreslått `setLocalization(context, catalogs)`, på rendererinstansen. Det må ikke gå gjennom en omskriving av `configuration.skeleton`. I dag sammenligner Porthole `JSON.stringify(renderedSkeleton)` før den oppretter ny renderer; en oversatt kopi av skeleton ville derfor utløse utskifting. `update(nextData)` kjører dessuten en bred bindingoppdatering som også omfatter lister og felt. Språkoppdateringen skal ha en egen, avgrenset vei. [porthole-webo.js](/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Public/js/porthole-webo.js:7941), [skeleton-runtime.js](/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Public/js/skeleton-runtime.js:113), [flushDynamicBindings](/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Public/js/skeleton-runtime.js:5352).

I SwiftUI injiseres en observerbar lokaliseringskontekst via den generelle skeleton-verten. Endring av konteksten skal ikke sette `currentSkeleton` på nytt eller dekode JSON. SwiftUI kan beregne berørte views på nytt, men deres identitet og felt-/fokus-/valgt-fane-tilstand skal bevares. [PortholeBindingViewModel.swift](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/Suggestion/PortholeBindingViewModel.swift:9>).

Ved rask veksling nb → en → nb må en sen katalogrespons for en ikke overstyre siste valg. Ny kontekst og dens kataloggenerasjon publiseres samlet. Fallback per melding er tillatt og skal ha riktig provenance; ufullstendige kataloger må ikke presenteres som full språkdekning. Argumentbindinger bruker eksisterende godkjente datatilstand og gir ingen nye Cell-leserettigheter.

### Målekrav

Disse er foreslåtte akseptansekrav, ikke målte egenskaper ved dagens kode:

- Varmt språkbytte utløser **0 nye Cell-/nettverksoppslag** når alle deklarerte ressurser og data finnes lokalt. Eksplisitt lagring av en ny brukerpreferanse måles separat.
- Kald lasting skalerer med unike katalogpakker, ikke antall etiketter eller rader; samtidige forespørsler etter samme pakke slås sammen.
- En fixture med 1 000 dataelementer og en egen med 200 monterte tekstbindinger måler oppslag, formatterkompileringer, DOM/view-identitet og tidsbruk. Dette kravet forutsetter ikke at dagens listekomponenter allerede er virtualiserte.
- Meldinger kompileres høyst én gang per aktiv cache-nøkkel. Listeetiketter bruker lokale kart eller et deduplisert batchresultat.
- Foreløpig mål: p95 for varmt språkbytte på 200 monterte tekster under 50 ms i begge målrenderere på dokumentert referansemaskin, uten nettverk. Mål både bindingsarbeid og tid til oppdatert flate, med layout målt separat. S0 etablerer baseline og S3 kontrollerer om målet er realistisk; et avvik skal forklares, ikke skjules ved å flytte målegrensen.
- Fokus, caret/markering, IME-komposisjon, utkast, valgt fane, listevalg og opplastingsstatus beholdes. Komposisjonstesten må også kjøres manuelt hvis automatiseringsverktøyet ikke kan reprodusere den.

## 3. Katalog, formatter og språkpolicy

Behold analysens forslag om `haven.localization-catalog.v1` som kildeformat, med namespace, revisjon, kilde-locale, format, argumenttyper, oversetterkontekst, kildehash og godkjente oversettelser. Ressurser kan eies av en app, delt pakke eller privat konfigurasjon. Samme ressursformat brukes også når en konfigurasjon inneholder ressursene selv. Et alternativt lokalt språk-kart skal ikke bygges inn i hvert statiske GUI-felt.

Start med en eksplisitt testet profil av ICU MessageFormat 1: literal tekst, navngitte argumenter, plural/select, tall, dato og klokkeslett. FormatJS dokumenterer disse mekanismene, men støtter ikke alle ICU-datomønstre. ICU4C tilbyr et stabilt MessageFormat-API med navngitte argumenter. Derfor må **felles støttet delmengde verifiseres**, ikke bare parsernes produktnavn. [FormatJS ICU syntax](https://formatjs.github.io/docs/core-concepts/icu-syntax/), [ICU4C MessageFormat](https://unicode-org.github.io/icu-docs/apidoc/released/icu4c/classicu_1_1MessageFormat.html), åpnet 2026-09-07.

Web bruker `intl-messageformat`; Swift får en avgrenset adapter over kontrollert pakket ICU4C, testet på macOS og Linux. Den skal ikke bruke udokumenterte Apple-systemsymboler. S0 må avklare pakking, størrelse, vedlikehold, navngitte argumenter, apostrofregler, tidssone, escaping og forskjeller i CLDR-data. Pinned testmiljøer kan kreve identisk tekst; støttede nettlesere testes i tillegg mot eksplisitt dokumenterte tillatte formateringsforskjeller. Ingen generell normalisering som skjuler feil i tall, dato eller grammatikk.

Meldingsverdier er ren tekst i første versjon. FormatJS-spesifikk riktekst og kjørbare markup-/HTML-utvidelser inngår ikke. Tall sendes som tall, tidspunkt med avtalt wire-representasjon og tidssone separat; cellen skal ikke forhåndsformatere UI-argumenter til norsk. Pengebeløp beholder valuta og presisjon fra data; lokalisering konverterer ikke valuta. Markdown-/artikkelinnhold behandles i en egen innholdsadapter med samme katalogeierskap.

Apples String Catalogs kan senere være et generert format for native menyer og andre skalltekster. De skal ikke være en ekstra manuelt vedlikeholdt kilde for dynamiske skeleton-tekster. MF2 vurderes senere gjennom en ny formatteradapter og migrering av ressurser; det skal ikke kreve en ny måte å deklarere GUI-tekster på.

Språkvalget følger analysens `HAVEN Locale Resolution v1`: eierens `person.preferences.locale` / `languageTags` → eksplisitt flate-/anonymt valg → nettleser/OS → `nb-NO`. Feltene finnes allerede i EntityAnchor-kontrakten. [EntityAnchorDataV1Contract.swift](/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Sources/App/Support/EntityAnchorDataV1Contract.swift:406).

Et innlogget språkbytte er en eksplisitt oppdatering av preferansen. Den lokale flaten kan vise det nye valget straks med synlig lagringsstatus; en eldre lagret verdi må ikke overstyre det på neste render. Ved feil vises at valget ikke er lagret. Offline synk bruker eksisterende eier-/synkmekanisme og skal ikke late som en ny, fungerende synkprotokoll følger med lokalisering.

Tekstfallback er separat fra valg av UI-locale og må være deterministisk. Bruk locale for teksten som faktisk ble valgt når plural/formatering utføres; rapporter faktisk `resolved_locale` per verdi når språkene blandes. Tidssone kommer fra egen preferanse/kontekst. Ikke innfør prosessglobal locale i Vapor. Ved innlasting i nettleseren brukes serverens første kontekst til bruker eller preferansedata faktisk endrer valget.

## 4. Arbeidspakker og rekkefølge

Hver pakke leverer en konkret endring med fixture, målrettet verifikasjon og kort statusnotat. Estimatene er grove utviklertimer inkludert teknisk review, før menneskelig språkredigering. Ingen pilot er tidsmålt. Etter S0 og den første flaten skal resten reestimeres.

| Pakke | Arbeid og hovedplassering | Avhengighet | Ferdig når | Timer |
|---|---|---|---|---:|
| S0 — teknisk prøve | Felles meldings-fixture; web-formatter og Swift/macOS/Linux-prøve i isolert testkode. Baseline for tekstoppdatering. | Ingen | Minst 12 representative meldinger består profilprøven; pakking og støttet syntaks er dokumentert. Eventuell blokkering gir et konkret revidert formattervalg før produksjonsintegrasjon. | 12–20 |
| S1 — kontrakt og locale | Nye lokaliseringsmodeller i CellBase; additive felter i `SkeletonDescription.swift` og `CellConfiguration.swift`; uttømmende tekstposisjonstabell, locale-policy og tests. | S0 | Kanoniske encode/decode-fixtures, legacy-dekoding og prioritet for data/literal/fallback er entydige; ukjente posisjoner avvises i authoring. | 12–20 |
| S2 — ressurser og vert | Katalogvalidator/pakker, formatteradapter ferdigstilles, bootstrap-kontekst i CellScaffold og Apple-verten; eksisterende preferansefelt kobles inn. | S1 | Begge verter laster samme katalogrevisjon, får korrekt språk og virker med lokal/offline pakke. To eiere er isolert. Feil ved lagring av språkvalg er synlig. | 16–28 |
| S3 — første gjennomgående skeleton | Generell tekstresolver i web `skeleton-runtime.js` og Apple `SkeletonView.swift`; Text, Button, TextField-placeholder, dynamisk listeetikett og plural. En testcelle leverer reelle Explore-data/handlinger. | S2 | Samme konfigurasjon virker i begge renderere. Endret data og språk gir riktige tekster; klikk og feltverdier bevares. Varmt språkbytte henter ikke tekster fra nettet. | 24–40 |
| S4 — full dekning og authoring | Resterende tekstposisjoner, systemmeldinger, Tabs/Picker/autocomplete, upload, tilgjengelighet og visualiseringskontrakter; validator, uttrekk, editor preview/commit og bevaring. | S3 | Hele S1-tabellen har eksplisitt støtte-/gapstatus i begge renderere. Alle støttede tekstposisjoner er testet; lagring og kloning mister ikke deklarasjoner/ressurser. Book 12/22 oppdateres til faktisk levert støtte. | 24–40 |
| S5 — effektivitet og releaseprøve | Måling, cache-/race-tester, langtekst, norsk/engelsk, tredje språk og representativ RTL; reelle UI-stier på web og Binding. | S4 | G1–G5 består for den avgrensede referanseflaten, resultatene og eventuelle plattformgap er lagret, og rollback er prøvd. | 12–20 |
| S6 — Butterpop | Oversett og integrer første produkts relevante normal-, tom-, feil- og spiller-/opplastingsflater gjennom samme katalog/runtime. | S3; full lansering etter S5 | Brukeren kan velge norsk/engelsk, arbeide videre i eksisterende utkast og fullføre de valgte handlingene. Dekning kontrolleres på mobil/desktop. | 12–24* |

**S0–S5: 100–168 timer. Med avgrenset Butterpop-lokalisering: 112–192 timer.** Dette er et mer detaljert og bredere anslag for generell skeleton-støtte enn analysens første anslag på 24–40 timer for den enkeltposten. S3–S5 inkluderer nå eksplisitt alle tekstposisjoner, authoring, dynamisk oppdatering, ytelse og reell rendererparitet. Tallene er ikke kalenderløfter eller et anslag for hele HAVEN.

\* Butterpop er i dag Leaf + egen JavaScript, ikke dokumentert som en ren skeleton-flate. S6-estimatet gjelder lokalisering av dagens avgrensede flate med den samme ressurs-/formatteradapteren. Å bygge hele Studio om til skeleton er et eget produktarbeid som må kartlegges og estimeres. Den generelle skeleton-leveransen skal uansett være demonstrert først. [butterpop_studio.leaf](/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Resources/Views/butterpop_studio.leaf:325).

Etter S3 kan produktmigrering utvikles mot den etablerte kontrakten. Utgivelse som «lokalisert skeleton-støtte» krever S4–S5. Kontrakt, formatter og UI-oppdatering bør ikke flettes sammen til én stor endring.

### Videre innføring som egne pakker

| Pakke | Konkret innhold og akseptanse |
|---|---|
| D1 — Interest/Purpose | Stabile ID-er og separate lokaliserte labels; migreringsfixture for eksisterende navn, referanser og likhet/oppslag. Samme item-binding brukes i skeleton. Eksisterende navn blir legacy-alias, og ukjent kildespråk merkes ukjent. Ingen sammenslåing av ulike interesser fordi oversettelsen blir lik. |
| D2 — Python/Go/Rust | Lesing og rundturbevaring av de nye konfigurasjonsfeltene uten metadata-/ressurstap; samme locale-/label-fixtures. Ingen nye GUI-renderere eller full meldingsmotor medregnet. Klienter som skriver konfigurasjoner må kvalifiseres før de får lagre ny metadata. |
| D3 — Porthole- og Binding-skall | Menyer, editor, dialoger og diagnostikk som ligger utenfor skeleton, bruker samme kataloger og kontekst. Apple-generering bare for testet delmengde der det gir nytte. |
| D4 — Infosider og øvrige Leaf-flater | Første sammenhengende norsk/engelsk inngang på digipomps.org, deretter andre maler. Artikkelvarianter, navigasjon, språklenker og manglende oversettelser håndteres eksplisitt. |
| D5 — Butler og andre agenter | Deterministiske svar/feil får meldingsnøkler; genererte svar får samme språk-/tidssonekontekst. Kilder og sitater beholder proveniens. Språkstyring og dialogkvalitet evalueres separat. |

Disse pakkene inngår i det opprinnelige handoffets bredere mål, men er ikke inkludert i S0–S6-estimatet. D1 behøver ingen egen oversettelsesmekanisme for GUI: dataeide labels leses av den generelle skeleton-bindingen. Ved manglende lokale termdata kan en delt vert/adapter hente unike ID-er i batch; en enkelt etikett skal ikke initiere nettverk. Bygg på eksisterende [CommonsTaxonomyCell](/Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellBase/Cells/Commons/CommonsTaxonomyCell.swift:184).

## 5. Forfatter- og oversettelsesflyt

1. Forfatteren lager tekst med stabil nøkkel og kontekst, enten via Swift-hjelpere eller editoren. Rene legacy-skeletons krever ingen migrering for å virke.
2. En schema-bevisst traversering trekker ut deklarerte tekstposisjoner fra JSON. For eksisterende umerkede tekster foreslås nøkler; skillet mellom UI-tekst og brukerdata må gjennomgås. Duplikat tekst betyr ikke nødvendigvis samme mening.
3. Kildekatalogen er autoritet. For selvstendige konfigurasjoner er den innebygde katalogen autoritet. Reservestrenger for gamle klienter genereres fra kilden; meldinger med argumenter kan ha en eksplisitt, enkel `legacy_fallback`. De skal ikke vedlikeholdes separat for hver renderer.
4. Oversettelser kommer inn som forslag. Godkjenning er knyttet til ressurs-ID, mål-locale og kildehash. Endret kilde gjør tidligere oversettelse klar for nytt review. Katalogvalidator sjekker argumentnavn/-typer og nødvendig grammatikkstruktur.
5. Preview viser flere språk, lange teststrenger, fallback og manglende tekster. Språkbytte i preview endrer bare visningen. Commit lagrer kildekonfigurasjon og deklarasjoner, aldri en oversatt kopi som ny kilde.
6. Godkjente ressurser pakkes per namespace/locale. CI verifiserer faktisk mål-språkdekning og kjører de delte fixture-testene. Bare godkjente revisjoner inngår i en produktrelease som erklæres dekket.

For dynamisk forfattede skeletons skal tekstdeklarasjoner og katalogressurser kunne previewes uten Swift-rekompilering. Nye schemafunksjoner krever først rendereroppdatering; etter det skal vanlig tekst-/språkarbeid være dataarbeid.

## 6. Kompatibilitet, validering og utgivelse

En additiv metadatautvidelse reduserer risikoen for at gamle lesere avviser et `label`-objekt, men er ikke i seg selv bevis på full bakoverkompatibilitet. Følgende skal testes:

- Ny Swift/web leser eksisterende konfigurasjoner og beholder handlinger, legacy-fallback og feltbindinger.
- Reelle eldre lesere viser eksisterende strengfelt. Der ukjente felter avvises, leverer verten en eksplisitt legacy-projeksjon uten ny metadata.
- Eldre skrivere kan miste ukjente felt ved decode/encode. Preview, lagring, eksport, duplisering og import må bevaringstestes. En klient som ikke bevarer kontrakten, får legacy-visning uten adgang til å overskrive den kanoniske lokaliserte konfigurasjonen.
- Katalogmanifest, konfigurasjon og rendererfunksjon kobles gjennom deklarert versjonsstøtte. Ustøttet versjon gir kontrollert reserve og diagnostikk; det skal ikke tolkes som støttet lokalisering.
- Roller, skjuling og synlighetsregler evalueres uendret. Lokaliserte tekster skal aldri bli tilgangsregler eller gi nye dataoppslag.
- Før aktivering verifiseres fungerende funksjonsbryter/rollback til eksisterende strenger. Kanoniske nøkler og oversettelser beholdes, så de ikke må rekonstrueres etter rollback.

Foretrukne testankre er [SkeletonTests.swift](/Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Tests/CellBaseTests/SkeletonTests.swift), dagens [Explore-validator](/Users/kjetil/Build/Digipomps/HAVEN/CellProtocolDocuments/Tools/Explore/skeleton_explore_validator.py) og CellScaffolds [Playwright-korpus](/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/playwright/skeleton-real-configuration-corpus.spec.js). Utvid eksisterende navigasjons-, felt-, upload-, tab- og atomic-swap-tester med språkbytte der det faktisk kan endre atferd. Suppler med felles JSON-fixtures og faktisk Binding-kjøring; en bestått formattertest beviser ikke at en SwiftUI-kontroll viser den oppløste teksten.

Minstekorpus skal dekke norsk/engelsk, 0/1/2 og større mengder, select, tall/dato/tidssone, manglende/utdaterte ressurser, ugyldige bindinger, en dataeid etikett, fallbacks med ulikt faktisk språk, q-verdier/regionvalg og to samtidige brukere. Legg til polsk som pluralprøve og en representativ RTL-prøve. Lang tekst og RTL krever kontroll av layout, tekstretning, input og retningsbestemte ikoner; bestått prøve betyr ikke at hele HAVEN er oversatt til disse språkene.

Ved overlevering skal det ligge en kort status med støttede schema-/katalogversjoner, ferdige tekstposisjoner per renderer, kjørte tester med miljø, målte ytelsestall, kjente gap og neste konkrete pakke. Normative Book 12/22 og agentveiledning oppdateres i takt med implementeringen. Denne planen skal inntil da forbli et forslag i Deliverables.

**Anbefalt oppstart:** S0 etterfulgt av S1–S3 som første sammenhengende implementeringsløp. Det avgjørende demonstrasjonskriteriet er én og samme skeleton som bytter norsk/engelsk i både web og Binding mens brukeren fortsetter å arbeide i flaten.
