# Lokalisering i HAVEN — L1-analyse

Dato: **2026-09-07**. Utført av Codex fra Claudes handoff i den eksisterende oppgaven. Status: **analyse levert; arkitektur og implementering avventer Kjetils beslutning**. Ingen kodeendringer, git-operasjoner, publisering eller modelloversettelse av prosjektinnhold er utført.

**Anbefaling:** én versjonert JSON-katalogmodell, med ICU MessageFormat 1 for dynamiske UI-meldinger, én felles regel for språkvalg, og stabile dataidentiteter med lokaliserte labels. Bruk Apples verktøy for Binding gjennom kontrollerte, genererte kataloger der konverteringen er tapsfri. Gjør MF2 til en konkret senere oppgradering av meldingsmotoren. En lokaliseringscelle er en mulig distribusjonskanal, ikke en forutsetning for å tegne en knapp.

Dette er et beslutningsgrunnlag, ikke en verifisert implementering. Timeanslag er mine planleggingsanslag. Eksterne kilder er primærkilder, åpnet **7. september 2026**; datoen gjelder alle W-lenker nedenfor. Dokumentert bibliotekstøtte betyr ikke at biblioteket er bygget eller testet med HAVEN. Kildekontroll og målemetode er bevart i [L1_KILDEKONTROLL.md](/Users/kjetil/Build/Digipomps/HAVEN/CellProtocolDocuments/Deliverables/Lokalisering_Analyse_2026-09-07/L1_KILDEKONTROLL.md).

## Premisskontroll før alternativvurderingen

Handoffet er nyttig, men noen fraværspåstander er allerede motsagt av koden. Rettelsene endrer anbefalingen: gjenbruk eksisterende kontrakter før nye felt og tjenester opprettes.

| Handoff | Kontrollert funn og konsekvens | Kilde, linjer |
|---|---|---|
| A1: taksonomiterm + labels finnes | Bekreftet. `CommonsTaxonomyCell` tilbyr batch og dekning; selve tekstvalget ligger i `LocalizationDefaults`. Dagens normalisering trimmer bare tekst; fallback prøver eksakt tag, hovedspråk, nb-NO/nb/en-US/en og til slutt alfabetisk første språk. Dette er ikke en komplett BCP 47-forhandling. | [CommonsTaxonomyCell.swift][R1], 184–273 og 342–420; [LocalizationContracts.swift][R2], 6–78 |
| A2: `name` er identitet | Delvis. Basisklassen har allerede `nodeIdentifier`; `reference` faller tilbake til `name`. Likhet sammenligner fortsatt navn. `Interest`/`Purpose` lagrer ikke dette identitetsfeltet i sine egne Codable-kontrakter. Migrering er derfor mer enn et nytt labels-felt. | [PerspectiveNode.swift][R3], 41–78 og 113–116; [Interest.swift][R4], 42–91; [Purpose.swift][R5], 41–108; [Perspective.swift][R6], 378–473 |
| A3: ingen lokalisering i skeleton | Strengkravet i selve elementene er bekreftet. Men `CellConfiguration.discovery.localizedText` finnes allerede, med `purposeRefs`/`interestRefs`. Discovery-lokalisering må inngå i arkitekturen. | [SkeletonDescription.swift][R7], 1752 og 1810; [CellConfiguration.swift][R8], 6–102 |
| A4–A6: norsk tekst i flater | Omfang bekreftet med nyanser: Porthole har både engelsk og norsk. 9 884 JS-linjer er ikke 9 884 oversettelser. Co-Pilot-filen har 15 190 linjer, hvorav 339 inneholder æ/ø/å; dette er en grov indikator, ikke 339 svarmaler. | [porthole-webo.js][R9], bl.a. 1682, 2209, 3311 og 4121; [PersonalCopilotCloudStore.swift][R12], 5321–5324 og 9620–9622 |
| A7: ingen `Accept-Language` | **Motsagt.** Identitetsfeilsiden har nb/en-valg og `Content-Language`/`Vary`. Den leser bare første språk og håndterer ikke q-vekter korrekt. Ingen felles resolver ble funnet i de undersøkte appkildene. | [VaporBrowserhead.swift][R13], 33–99 |
| A8: Binding bruker ikke Apple-kataloger | Ingen `.xcstrings`, `.strings`, `.stringsdict`, `.lproj` eller eksplisitte lokaliserings-API-er funnet under `Binding/Binding` og `Binding/Cells`. Det beviser ikke at alle SwiftUI-litteraler er uegnet for Apples automatiske uttrekk. | Avgrenset filsøk, 107 registrerte filer; se kildekontrollen |
| A9: nettstedet er nb-only | Det finnes én engelsk artikkel. Dens menyer går fortsatt til norske sider. Release-notatet sier uttrykkelig at `/en/` ikke er en engelsk utgave av nettstedet. Lokal kilde er verifisert; produksjonsstatus er ikke kontrollert her. | [RELEASE_NOTE_2026-09-07.md][R14], 3–8 og 32–35; [index.html][R15], 13–15, 27 og 37 |
| A10: portene har ingen i18n | Ingen UI-renderer er dokumentert der, men alle tre portene bevarer allerede lokaliserte discovery-data. Parsing, formattering og rendering er tre forskjellige krav. | [configuration.py][R16], 86–114; [configuration.go][R17], 108–136; [configuration.rs][R18], 16–54 |
| A11: EntityAnchor mangler preferanser | **Motsagt.** `person.preferences.locale`, `.timezone` og `.languageTags` er eksplisitte, eierprivate kontraktfelt. Ikke innfør konkurrerende `person.locale.preferred`. At feltene er beskrevet, beviser ikke at alle flater bruker dem. | [EntityAnchorDataV1Contract.swift][R19], 406–409 |
| A12: Book 12/22 må endres | Bekreftet for en senere schema-/rendererendring. Book 12 peker også på den faktiske Apple-rendereren i CellProtocol, ikke bare Binding-repoet. | [12_Skeleton_Spec.md][R20], 1–16; [22_Explore_Contracts_For_Skeleton_Authoring.md][R21], 179–214 |

Butterpop-estimatet må omfatte både den **327 linjer lange Leaf-malen** og **1 080 linjer JavaScript**. HTML-parsing fant 100 tekstnoder, 96 unike tekstverdier og 10 relevante attributter, 9 unike. Dette inkluderer merkevarer og mulige ikke-oversettbare verdier. Malen laster JS-filen eksplisitt. [butterpop_studio.leaf][R10], 325; [butterpop-studio.js][R11].

## 1. Alternativer for kildeformat og runtime

Tre beslutninger må skilles: **katalogformat**, **meldingsgrammatikk** og **tilgang til katalogen**. MF2 alene definerer ikke HAVENs godkjenninger eller namespace-organisering; en celle alene gir ingen pluralregler.

Tabellen vurderer L1 flere språk, L2 språkvalg, L3 stabile data, L4 effektivitet, L5 plattformer/grammatikk, L6 generelle skeletons og L7 Apple. «Felles arbeid» betyr at kandidaten ikke løser kravet automatisk.

| Kandidat | L1 / L2 / L3 | L4: uttrekk og vedlikehold | L5: plattformer og grammatikk | L6 / L7 | Dom |
|---|---|---|---|---|---|
| Apple `.xcstrings` som felles kilde | Nye språk som katalogdata; L2/L3 er felles arbeid | Svært god Xcode-redigering, status og uttrekk. Web/Leaf trenger egne uttrekkere og konvertering. | JSON er lesbart uten Xcode. Apples byggeprosess lager `.strings`/`.stringsdict`; dette er ikke en ferdig web-/Linux-runtime. Variasjoner må tolkes eller konverteres utenfor Apple. | Skeleton-adapter kreves. Best samsvar med Kjetils verktøypreferanse. | Reelt alternativ; sterkest hvis Apple blir hovedflaten. [Apple: String Catalogs][W1], [Apple: Xcode-lokalisering][W2] |
| MF2 i JSON | God utvidbarhet; L2/L3 er felles arbeid | Klar standardretning, men usikker Swift-integrasjonskostnad | Hentet UTS #35 del 9, v48.2, er stabil. ICU4C 78.3 dokumenterer fortsatt sitt MF2-API som teknologiforhåndsvisning. | Felles rendereradapter kreves; Apple-katalogmapping ikke automatisk. | Ikke velg uprøvd Swift-runtime som kritisk førstesteg. [Unicode MF2][W3], [ICU4C MF2-API][W4] |
| Fluent `.ftl` | Sterkt på lokale grammatiske forskjeller; L2/L3 er felles arbeid | Oversetter kan variere grammatikk uten endringer i kildespråket | Prosjektet har JS-, Python- og Rust-implementasjoner; moden Swift/Go-runtime ikke verifisert. Egnet ved mange grammatiske varianter. | Felles adapter; ingen direkte Apple-katalogflyt dokumentert her. | God utfordrer, særlig dersom Rust får UI-ansvar. [Project Fluent][W5] |
| gettext `.po` → `.mo` | Flere språk og kontekst/plural; L2/L3 er felles arbeid | Etablert PO-flyt, oppdatering og `fuzzy`-kontroll | Python har standardbibliotekstøtte. JSON-utveksling, sammensatte grammatikkvalg og formattering krever flere avtaler. Påstanden «mest utbredt» er ikke målt. | Egen skeleton-/Apple-adapter. | Solid, men lite gevinst av et formatbytte fra HAVENs JSON-data. [GNU gettext][W6], [Python gettext][W7] |
| i18next | Laste-/språkvalgsmekanismer; L2 må likevel følge HAVEN-regelen | Praktisk webøkosystem, kontekst, interpolering og plural | JavaScript-runtime. Standardformatet er ikke det samme som ICU MessageFormat. | Krever samme generelle skeletonarbeid; Apple krever adapter. | Mulig webhjelper; ikke la dens standardvalg definere hele kontrakten. [i18next][W8] |
| JSON + ICU MessageFormat 1, FormatJS på web | Nye språk med data; L2/L3 felles arbeid | Ett `t(key,args)` og eksisterende parser/formatter; uttrekksverktøy etter første merking | Plural, `select`, ordinale former og navngitte argumenter. ICU4C har stabilt API; Swift trenger en adapter. | Generell skeletonadapter; generert Apple-projeksjon for testet delmengde. | **Anbefalt nå.** Lavere dokumentert runtime-risiko enn MF2 for Swift. [FormatJS: ICU][W9], [ICU: meldinger][W10], [ICU4C MF1-API][W11] |
| Lingo + Lingo-Vapor/Leaf | Praktisk serveroppslag; L2/L3 må samordnes | JSON, interpolering og ferdige Leaf-tags | Egen syntaks; README beskriver begrensning ved flere uavhengige pluralvalg i én melding, og RFC 4647-fallback som videre arbeid. | Ikke en universell renderer-/Apple-løsning. | Ikke felles meldingsmotor; unngå enda en grammatikk. [Lingo][W12], [Lingo-Vapor][W13] |
| `cell:///Localization` | Kan eksponere locale, revisjon, oppslag og dekning | Kan støtte redigering og dynamiske kataloger | Format- og formattervalg gjenstår. Nettverksavhengighet må unngås. | Kan betjene alle renderere; ingen Apple-spesialbehandling nødvendig. | **Komplement**, senere ved påvist behov. Endpointet er et forslag. |

### Bibliotekstatus som faktisk er kontrollert

| Mål | MF2 | Fluent | Praktisk følge |
|---|---|---|---|
| Swift/macOS/Linux | Ingen ferdig Swift-native runtime verifisert. ICU4C har en C++-implementasjon med preview-markering. | Swift-runtime med aktuell konformitet ikke verifisert. | Ikke forveksle Foundation `Locale` med en MF2-/Fluent-parser. |
| JavaScript | `messageformat` dokumenterer parser/runtime/polyfill; Unicode-listen omtaler v4.0. Browserinnebygd `Intl.MessageFormat` er ikke dokumentert som allment tilgjengelig her. [messageformat][W14], [Unicode: implementasjoner][W15] | `@fluent/bundle` i prosjektets JS-repo. [Fluent JS][W16] | Begge kan evalueres i vanilla JS uten React. |
| Python | Full, aktuell MF2-runtime ikke verifisert i det avgrensede primærkildesøket. | Prosjektets `python-fluent` har runtime. [Fluent Python][W17] | HAVEN-porten kan først bevare katalogverdier uten formattering. |
| Go | `kaptinlin/messageformat-go` finnes; prosjektet beskriver testing mot en pinnet Unicode-testpakke. Egen konformitetskjøring ikke gjort. [MF2 for Go][W18] | Vedlikeholdt Go-runtime med dokumentert dekning ikke verifisert. | En README er ikke sertifisering av HAVEN-integrasjon. |
| Rust | `mf2-parser` er en parser; dette beviser ikke en full formatter. [Rust MF2-parser][W19] | Prosjektets `fluent-rs` har runtime. [Fluent Rust][W20] | For MF1 dokumenterer FormatJS også Rust-formatter og ICU4X-underlag. [FormatJS Rust][W21] |

Manglende verifikasjon betyr **ikke at et bibliotek ikke finnes**. Den gamle MF2-brukerveiledningen omtaler en eldre draft; standardstatus bygger derfor på den normative spesifikasjonen, og API-status på den nyere, versjonsmerkede API-siden. [Unicode MF2][W3], [ICU4C MF2-API][W4]

## 2. Anbefalt arkitektur: data, flater og innhold

### Én ressursmodell, én eier per tekst

Foreslå `haven.localization-catalog.v1`: UTF-8 JSON med namespace, revisjon, kilde-locale, ressurser, argumenttyper, oversetterkontekst og godkjenningsstatus. **Dette er nytt, foreslått format**, ikke et eksisterende CellProtocol-schema. Start med repo-filer: delte ressurser i CellProtocols `commons`-område, produktressurser i eierappen og nettstedstekster i dokumentrepoet. Ett kildeformat innebærer ikke én enorm fil eller ett sentralt eierskap.

```json
{
  "schema": "haven.localization-catalog.v1",
  "namespace": "butterpop.ui",
  "revision": 1,
  "source_locale": "nb-NO",
  "messages": {
    "release.count": {
      "format": "icu-mf1",
      "arguments": {"count": "integer"},
      "context": "Antall utgivelser i oversikten",
      "translations": {
        "nb-NO": {
          "value": "{count, plural, one {# utgivelse} other {# utgivelser}}",
          "state": "draft"
        },
        "en-US": {
          "value": "{count, plural, one {# release} other {# releases}}",
          "state": "draft"
        }
      }
    }
  }
}
```

Tillatte verdiarter: `literal` for labels, `icu-mf1` for dynamiske meldinger og `markdown` for redaksjonelt innhold. Markdown er innholdssyntaks inne i JSON-ressursen, ikke en konkurrerende oversettelseskatalog. Redaktørverktøyet bør vise lange tekstfelt som dokumenter, ikke som escaped JSON. Før en slik flyt finnes, behold dagens HTML som eksplisitt **umigrert kilde**; ikke opprett to redigerbare kopier av samme side.

Godkjent revisjon genererer namespace-/locale-pakker, eventuell formatter-AST, nettstedets HTML og en testet `.xcstrings`-projeksjon. Genererte filer redigeres ikke. Importerte oversettelser er endringsforslag til den kanoniske ressursen. Dataeide labels har datanoden/taksonomipakken som autoritet; de skal ikke vedlikeholdes samtidig i en UI-katalog. Samme ressurskonvolutt kan brukes til eksport/review uten å flytte eierskapet.

**Runtime:** FormatJS `intl-messageformat` på web; én delt Swift-adapter over ICU4Cs stabile MF1-API for Vapor og generiske Apple-skeletons. Navngitte argumenter krever riktig C++-overload; ikke antagelser om en enkel varargs-C-funksjon. Pakk en kontrollert ICU-avhengighet og test Linux/macOS; ikke bygg på udokumenterte Apple-systemsymboler. Dette adapterarbeidet er ikke ferdig. [FormatJS: ICU][W9], [ICU4C MF1-API][W11]

Den første kontraktprøven må vise de samme meldingene med omordnede argumenter, nestet `select`/plural, apostrofer, tall og dato på begge Swift-mål og JS. Godta ingen stille nedgradering av syntaks. Profilen tillater navngitte argumenter, `select`, `plural`, `selectordinal`, eksakte tallvalg og avtalte formatteringsstiler. Den avviser rå HTML, formatterfunksjoner fra katalogen, `choice` og utestede plattformspesifikke stiler. Dette er en kontrollert delmengde av en eksisterende grammatikk; ikke en egen grammatikkmotor. [FormatJS: ICU][W9], [ICU: meldinger][W10]

### Felles språkregel: `HAVEN Locale Resolution v1`

For en **UI-forespørsel**, prøv disse kildene i rekkefølge og velg første støttede språk innen kilden:

1. Eierens `person.preferences.locale`, deretter ordnet `person.preferences.languageTags`.
2. Eksplisitt valg på flaten eller tidligere lagret anonymt valg.
3. Ordnet `Accept-Language` på server, `navigator.languages` på web eller OS-preferanser i Binding.
4. `nb-NO`.

Ved et innlogget språkbytte oppdateres eierpreferansen som en vanlig eierstyrt innstilling før ny oppløsning. En eldre entitetsverdi må ikke gjøre velgeren virkningsløs. Vis lagringsfeil; ikke lat som en vedvarende endring lyktes. I frakoblet modus må den lokale, eksplisitte endringen være en køet eierendring med konfliktbehandling. Bruk eksisterende felt [EntityAnchorDataV1Contract.swift][R19], ikke profilens språkferdighet som skjult UI-preferanse.

Kanoniser tags med en avtalt BCP 47-policy; la manifestet beskrive støttede språk og standardvariant per språk. Eksempler: `nb` og legacy `no` → `nb-NO`, `en` → `en-US`, `en-GB` kan velge `en-US` som tilgjengelig engelsk variant. `no`-mapping er HAVENs kompatibilitetspolicy, ikke en regel om at norsk og bokmål er identiske. `nn` skal ikke kanoniseres til `nb`. Bevar script: `zh-Hant` må ikke bli vilkårlig `zh-Hans`. RFC 4647 beskriver matching, men valg av tilgjengelig variant må være deterministisk hos HAVEN. [RFC 4647][W22]

For HTTP sorteres q-vekter synkende, med original rekkefølge som stabil tie-break. `q=0` utelukkes fra headerforhandling. Ugyldige verdier ignoreres med diagnostikk; wildcard velger manifestets standard blant akseptable kandidater. Når ingen kandidat er akseptabel, brukes produktets nb-NO-fallback med årsak `default_no_match`; dette er et eksplisitt valg om å ignorere headerpreferansen fremfor 406, slik HTTP tillater. En eksplisitt eierpreferanse har høyere prioritet enn headeren. [RFC 9110][W23]

**Tekstfallback er et eget trinn:** valgt katalog-locale → dens avtalte foreldre/variant → nb-NO → en-US → eksplisitt legacy-tekst eller kontrollert «mangler oversettelse». Fjern ikke dagens fallback-semantikk lydløst: gi den nye regelen versjon og tester. Ikke velg alfabetisk første tilfeldige språk i en offentlig UI. Bruk locale for den teksten som faktisk ble valgt når plural og grammatikk beregnes.

```json
{
  "locale_policy": "haven.locale-resolution.v1",
  "requested_locale": "en-GB",
  "ui_locale": "en-US",
  "resolved_locale": "nb-NO",
  "locale_source": "entity",
  "fallback_reason": "message_missing",
  "catalog_revision": "butterpop.ui@1",
  "value": "Utgivelser"
}
```

Dette er et **foreslått lokaliseringssvar**. Hver lokalisert verdi/batchpost har sannferdig `resolved_locale`; et toppfelt alene kan ikke beskrive en blanding av språk. Umerket historisk tekst kan ha `resolved_locale: null`, aldri en oppdiktet språkproveniens. Legg tilsvarende metadata i bootstrap/visningssvar og `Content-Language` der dette passer. Ikke endre alle `FlowElement` eller domenedata for å oppfylle formuleringen «hvert svar».

Server bestemmer første renderings kontekst og sender den til web. Nettleseren skal ikke umiddelbart overstyre den under hydrering. Cache må skille katalogrevisjon og locale; bruk også eierscope for private data. Ikke lagre én prosessglobal «current locale» i Vapor. HTTP-cache må variere etter faktisk språkvalg; innloggede personlige svar kan ikke deles som anonyme offentlige sider. [RFC 9110][W23]

### Datalaget: interesser og formål

Språkuavhengighet betyr at navneendring aldri endrer identitet eller matching. Det krever ikke at historiske identifikatorer slutter å ligne norske eller engelske ord.

Foreslått **lokaliseringsprojeksjon**, ikke komplett erstatning for dagens graf-JSON:

```json
{
  "id": "example.interest.italian-food",
  "kind": "interest",
  "legacyName": "Italian food",
  "labels": {"nb-NO": "Italiensk mat", "en-US": "Italian food"},
  "aliases": {"nb-NO": ["italiensk mat"], "en-US": ["Italian cuisine"]},
  "labelSource": {"type": "owned"},
  "revision": 1
}
```

For `Purpose` brukes samme identitets-/labelstruktur og `descriptions` per språk; dagens `goal`, `helperCells`, `composition`, vekter og relasjoner bevares. `labelSource` er enten eierdata **eller** en taksonomireferanse `{namespace, term_id, revision}`. Ingen udefinert blanding der en lokal kopi tilfeldig vinner. Eksempelets ID er illustrasjon, ikke en registrert taksonomiterm.

Migrering:

1. Registrer eksisterende referanser, språk og kollisjoner per datadomene. Ikke flytt alle `name` til `labels.nb-NO`: repoet inneholder også engelske navn. Ukjent opprinnelsesspråk må avklares.
2. Gjenbruk `nodeIdentifier` som stabil intern identitet og inkluder den i `Interest`/`Purpose`-koding. Gamle objekter uten feltet beholder gamle referanser; migreringsmapping må være deterministisk og lagret, ikke ny UUID ved hver lesing.
3. Legg til labels uten å overskrive `name`. `name` er frosset legacy-oppslag i overgangsperioden. Bygg separat ID-indeks og språkspesifikke aliasindekser; like labels kan peke til ulike ID-er.
4. Flytt referanser, likhet, deduplisering og matching samlet etter verifisert kartlegging. Gamle navn kan returnere flere treff; ikke slå sammen homonymer automatisk. Oversatte aliaser er søkeinnganger, ikke nye konsepter.
5. Kjør begge lesemodeller i en avtalt overgang. Bekreft at serialisering/rundtur og grafresultater er uendret av valgt UI-språk. Bevar rollback-data før eventuell senere utfasing.

Dekningstesten må telle **egne godkjente oversettelser**, ikke vellykket fallback: alle aktive, publiserbare noder skal ha nb-NO og en-US fra autoritativ labelkilde. Eksisterende taksonomidekning er et utgangspunkt, men advarsler må gjøres til en release-grense for den migrerte delmengden. Private brukerlagde interesser uten oversettelse kan vises på originalspråket og merkes som udekket; L1 kan ikke ærlig love oversettelse av alt brukergenerert innhold uten slikt arbeid. [CommonsTaxonomyCell.swift][R1], [LocalizationContracts.swift][R2]

### Flatelaget: generell skeleton-støtte

**Støttet nå:** literal `label` og enkelte `labelKeypath`-/tekstbindinger kan vise allerede lokaliserte data. **Ikke støttet nå:** objekt i `SkeletonButton.label`; Swift dekoder `String`, og webvalideringen krever streng. [SkeletonDescription.swift][R7], 1810; [skeleton-runtime.js][R22], 360–365.

Foreslå én gjenbrukbar `LocalizedText`-union for presentasjonstekst:

```json
[
  {"label": "Lagre"},
  {"label": {"key": "common.save"}},
  {"label": {"nb-NO": "Lagre", "en-US": "Save"}}
]
```

Dette er tre **foreslåtte feltformer**, ikke gyldige ferdige CellConfigurations i dagens runtime. Inline-kart tillater bare literal tekst; komplekse meldinger bruker katalog-ID med typede argumentbindinger. Objektet skal entydig være nøkkelreferanse eller locale-kart. En manglende nøkkel er en valideringsfeil, ikke en anledning til å tolke teksten som en keypath.

Ny dekoder må lese alle gamle strenger. Det gjør den bakoverkompatibel med eksisterende dokumenter, men **gamle klienter kan fortsatt ikke lese nye objektlabels**. Rull derfor først ut nye lesere. Send nye former bare til klienter med avtalt kapabilitet; lever ellers en generell, lokalisert v1-projeksjon med strengverdier. Ukjent klient behandles som v1. En gammel klient som viderelagrer v1-projeksjonen må ikke overskrive den rikere kilden.

Samme oppløser må dekke `Text.text`, felt-placeholder, knapper, toggles, picker, tabtitler, upload-hjelpetekst, tilgjengelighetsnavn og discovery-tekster. `cellReferences.label`, action-keypaths, payload-koder, ID-er og enum-verdier er **bindingsdata**, selv om feltnavnet inneholder «label»; de oversettes ikke. Eksisterende `labelKeypath`-prioritet bevares; nye lokaliseringsbindinger valideres mot Explore med riktig item-/root-scope.

Samle alle katalognøkler i en konfigurasjon og last én pakke/batch før rendering. Unngå cellekall per widget. Språkbytte skal oppdatere tekst og tilgjengelighetsnavn samtidig uten å miste felter, fokus, valgte ID-er eller action-bindinger. Apple-rendereren setter i dag en knappes accessibility-label fra den opprinnelige labelen; akkurat dette må testes når synlig tekst blir dynamisk. [SkeletonView.swift][R23], 1805–1813.

### Innholdslaget og lokaliseringscellen

Gi artikler en stabil innholds-ID, språkversjoner, originalspråk, kilde-revisjon og separat godkjenning. Behold dagens norske URL-er og bygg engelske under `/en/`; ingen generell URL-flytting trengs. En eksplisitt `/en/artikler/...` identifiserer en engelsk innholdsressurs og skal ikke automatisk omdirigeres bort på grunn av profilpreferansen. UI-språk og innholdsspråk kan derfor være forskjellige. Ved nøytral inngang brukes den felles preferanseregelen til et språkforslag/valg. Språklenker går mellom oversettelser av samme innhold.

Generer korrekt `lang`, gjensidige `hreflang`, selv-canonical og språkvarianter i sitemap. Google beskriver krav til gjensidige alternativer og eventuell `x-default`; dette gjør sidene oppdagbare, uten å garantere rangering. Ikke merk norske sider som engelske bare fordi menyen er oversatt. [Google: språkversjoner][W24]

En senere `LocalizationCell` kan tilby foreslåtte `localization.resolve.batch`, `.catalog`, `.coverage` og revisjonsmetadata etter taksonomimønsteret. Start med filbacket tjeneste og lokale, uforanderlige snapshots i web/Binding. Cellen kan senere distribuere godkjente endringer og private overlegg. Rotdata/Ward-signering bør bare innføres når proveniens, distribusjon eller redigeringsbehov begrunner det; ikke bygg en ny autoritets- og synkroniseringsflyt bare for tekstutskifting.

## 3. Effektivitet: uttrekk, oversettelse og vedlikehold

### Konkret uttrekk for Porthole, Leaf og Swift

**Førstegangsuttrekk og løpende uttrekk er ulike jobber.** En parser finner strenglitteraler; den vet ikke at «Save» er en knapp og «save» en action-kode. FormatJS' dokumenterte uttrekk tar allerede deklarerte meldinger; det er ikke dokumentasjon på automatisk forståelse av hele `porthole-webo.js`. [FormatJS: uttrekk][W25]

1. Bruk Babel-parser til AST med posisjoner. Samle strenglitteraler og template-litteraler med fil, linje, funksjon, parameteruttrykk og syntaktisk kontekst. Spor synker som `textContent`, notice/toast, feilmeldinger og HTML-malbygging. [Babel-parser][W26]
2. Parse HTML-fragmentene i template-litteraler separat, med bevarte markører for `${...}`. Hent tekstnoder og `aria-label`, `title`, `alt`, `placeholder`; aldri oversett ID, klasse, URL eller `data-action`. Ikke evaluer JS for å hente tekst.
3. Del kandidatene i visningstekst, tekniske verdier, domeneinnhold og uavklart. La modellen foreslå hele meldinger, argumentnavn og semantiske nøkler. Mennesket godkjenner diff per funksjon/flate. Like ord med ulik betydning får ulike nøkler.
4. Gjør små AST-baserte omskrivinger til `t("namespace.key", {args})`. For dynamisk HTML må tekst og attributter escapes på riktig sted; oversatte katalogverdier skal ikke bli kjørbar markup.
5. Etter innføringen brukes en deterministisk extractor/linter for merkede meldinger, ukjente nøkler, manglende oversettelser og nye umerkede synker. Regex brukes til kontrollsøk, ikke masseomskriving.

Semantiske nøkler er mitt bevisste valg for delte kontrakter. FormatJS anbefaler normalt genererte innholdshasher for å unngå kollisjoner; HAVEN bør i stedet forebygge kollisjoner med namespace/validering og bruke **teksthash for oversettelsesferskhet**, slik at en språkrettelse ikke endrer kontrakts-ID. [FormatJS: uttrekk][W25]

Leaf får en strukturbevarende uttrekker som respekterer Leaf-direktiver. Injiser ferdig lokaliserte verdier eller én generisk tag med request-kontekst. Swift får SwiftSyntax-besøk av brukerrettede litteraler/interpoleringer og typekontroll etter omskriving. SwiftSyntax gir parser-/transformasjonsgrunnlaget, ikke automatisk klassifisering av hvilke tekster brukeren ser. [SwiftSyntax][W27]

Butler-tekster, intent-ord og modellinstruksjoner holdes adskilt: oversett svarmaler, bevar maskinelle intent-ID-er og vedlikehold flerspråklige søke-/intenteksempler separat. En engelsk UI skal fortsatt kunne forstå et norsk spørsmål. Ikke oversett eierens meldinger, navn eller fakta som del av kodeuttrekket.

### Modelloversettelse og rettelseslogg

Flyt: uttrekk → kontekst/ordliste → modellutkast → automatisk strukturkontroll → menneskelig språkgodkjenning → visuell og funksjonell kontroll → godkjent katalogrevisjon → ordinær release.

Hver godkjenning bindes til teksthash, mål-locale og ressurs-ID. Endres originalen, blir tidligere oversettelser `needs_review`. Deploy bruker bare `approved`-verdier for språk som annonseres som dekket. Modellen kan ikke godkjenne sitt eget resultat. Kontroller variabler, tall, lenker, produktnavn, forbehold og hele meldingsvarianter. Dette krever ingen ekstern oversettelsestjeneste som obligatorisk avhengighet.

Koble meningsendrende rettelser til nettstedets eksisterende rettelseslogg: hva som var galt, hvilke språk og sider som berøres, kildegrunnlag, hvem som godkjente, og publisert revisjon. Typografiske rettelser kan ligge i den ordinære endringshistorikken. Den nåværende loggen dokumenterer både endringer og avviste overpåstander; samme styrke på forbehold må beholdes i engelsk tekst. [index.html][R24], 23–45.

### Timeanslag og avgrensning

Arbeidstimer for en erfaren utvikler med agentstøtte, inkludert teknisk review og målrettet verifikasjon. **Ingen faktisk uttrekks-/oversettelsespilot er tidsmålt.** Estimatene gjelder undersøkte flater, ikke hele HAVEN, alle kundedata eller alle fremtidige språk.

| Arbeidspakke/flate | Timer | Forutsetning og avgrensning |
|---|---:|---|
| Formatprøve og bibliotekvalg | 12–20 | JS + Swift på macOS/Linux, samme 12 representative meldinger |
| Locale-regel, EntityAnchor-tilkobling, bootstrap | 12–20 | Eksisterende preferansefelt; testet vedvarende og anonymt valg |
| Katalog, uttrekksgrunnlag, validering/release | 16–28 | Første repeterbare kjede og metadata; ikke fullt oversetterprodukt |
| Butterpop | 12–24 | Leaf + 1 080 JS-linjer, relevante feil-/tomtilstander |
| digipomps.org, første sammenhengende engelsk inngang | 10–18 | Forside, navigasjon, om/status og kobling til eksisterende artikkel |
| Interest + Purpose, første datadomene | 16–32 | Persistens, referanser, labels og migreringsfixture; ingen masseoversettelse av ukjent data |
| Generell skeleton-støtte, web + Apple | 24–40 | Union, v1-projeksjon, Explore, docs, språkbytte og tilgjengelighet |
| Porthole-shell | 28–48 | 9 884 linjer JS; resten av skeleton-runtime ligger i forrige rad |
| Øvrige Leaf-maler | 16–28 | Inntil 24 andre maler; prioriter faktiske brukerflater |
| Butler-maler + agentkontekst | 16–28 | Avgrensede intent-/svarsett; ikke evaluering av alle mulige modellutsagn |
| Binding-shell, pakking og Apple-katalogprojeksjon | 16–28 | Ut over felles skeletonadapter; faktisk omfang må inventeres |
| Porter: bevaring og labeloppslag | 8–16 | Ingen ny UI-renderer eller full formatter i hver port |
| Tredje språk-prøve, RTL og samlet releasekontroll | 12–20 | Representative flater og testoversettelser |
| **Sum undersøkt innføring** | **198–350** | Før oversettelse av hele artikkelarkivet og ukjent celleinnhold |

Første tekniske Butterpop-resultat: **52–92 timer** inkludert de tre første grunnpakkene. Deretter første engelsk nettinngang: **10–18 timer ekstra**. Interest er første dataleveranse og kan følge som egen pakke uten å forsinke de synlige flatene.

Menneskelig språkredigering bør budsjetteres separat: grovt **0,5–1,5 timer per 100 korte meldinger**, **1–3 timer per vanlig artikkel**, mer for faglig krevende tekst. Dette er anslag, ikke bransjemålinger. Revider etter første 50 meldinger og én artikkel. Et tredje språk krever oversettelse, review og layoutkontroll selv om kodeendringer uteblir.

## 4. Flere språk, grammatikk, formatering og agenter

**Tredje språk:** legg til locale/retning/variantpolicy i manifestet, oversett ressursene, generer pakker og kjør dekning-/paritetstester. Velg for eksempel polsk i prøvepakken for mer krevende plural og arabisk som egen RTL-test. Ingen celler eller renderere skal ha `if language == ...`. Bibliotekenes locale-data må også følge med distribusjonen; «ingen cellekodeendring» betyr ikke «ingen ny pakke/release».

**Norsk og engelsk:** begge har kardinalkategoriene `one`/`other`, men CLDR-reglene er forskjellige: bokmål har `n = 1`, engelsk `i = 1 and v = 0`. Synlig desimalpresisjon kan derfor påvirke engelsk. Engelsk har også ordinale `one`/`two`/`few`/`other`, mens bokmål har `other`. Test tallene 0, 1, 2, 11, 21 og desimaler, med eksplisitt avrunding. Grammatisk kjønn håndteres gjennom oversetterstyrte `select`-varianter; ikke utled personers kjønn fra navn. Oversett hele setninger, ikke sammensatte ordfragmenter. [CLDR: pluralregler][W28], [ICU: meldinger][W10]

**Tall, dato og valuta:** lagre tall, valuta-ID og tidspunkt som strukturerte verdier. Norsk grensesnitt endrer ikke NOK til EUR eller omvendt. Formatering er ikke valutaveksling. Skill språk, regionpreferanse og tidssone; gjenbruk `.timezone`. Bruk avtalte stiler over `Intl.NumberFormat`/`DateTimeFormat` på web og Foundation/ICU i Swift. Tidssone for et arrangement følger arrangementet når dette er produktets regel. [ECMA-402][W29], [Unicode: datoer][W30]

For å unngå variasjon mellom motorer kan navngitte formatteringsprofiler produsere typede presentasjonsargumenter før meldingsformatering; rå count beholdes separat til pluralvalg. Del tester for semantikk og for eksakt tekst. ICU-/CLDR-/OS-versjoner kan gi forskjellige mellomrom og datoformater; krev lik beslutning/grammatikk, og dokumenter avtalte visningsforskjeller. Bevisførsel og protokollidentitet baseres aldri på lokaliserte strenger. [Unicode MF2][W3], [ECMA-402][W29]

**RTL:** språkmanifestet angir retning, HTML får `dir`, og layout bruker logical properties/leading/trailing. Variabler med fremmed retning isoleres (`bdi`/tilsvarende mekanisme), URL-er og kode beholdes lesbare. Test menyer, modaler, opplasting, tekstfelt, piltaster og ikoner som faktisk skal speiles. Ikke speil merkevarer og mediekontroller ukritisk. Språkstøtte er ikke ferdig før fokus, tilgjengelighetsnavn og synlig rekkefølge er kontrollert. [W3C: RTL][W31]

**Portene:** bevar unioner, locale-tags, nøkler, kilde-revisjon og ukjente fremtidige metadata ved rundtur. Lokal labeloppløsning kan bruke samme policy-fixture uten en full meldingsmotor. Når en port faktisk skal produsere brukerrettede meldinger, kvalifiser dens formatter mot samme pakke; ikke anta at JSON-parsing innebærer MF-støtte. Dette bygger videre på dagens discovery-kontrakter. [configuration.py][R16], [configuration.go][R17], [configuration.rs][R18]

**Butler/Kallimachos:** forespørsler får samme oppløste språk-/tidssonekontekst fra verten, med eksplisitt samtalevalg håndtert som brukerinnstilling. Skill ønsket svar-locale fra språket i innhentede kilder. Bevar sitater i originalspråk; merk oversettelser og bevar kildelenker. Deterministiske feilmeldinger bruker katalogen; genererte svar instrueres og evalueres for språk, kildebevaring og forbehold. Modellen bestemmer ikke autoritativ UI-locale. Full Kallimachos-dialogtesting er en senere akseptansejobb, ikke utført i denne analysen.

## 5. Migreringsplan som PDD-arbeidspakker

Dette er en **PDD-kladd**, ikke opprettede eller autoriserte implementeringsoppgaver. L1–L7 er brukerens krav; arbeidspakkene under er deres konkrete løvformål. Hver pakke får ett målbart mål. Executor er foreslått rolle, ingen agent er startet. Kjetil er beslutningseier; den implementerende oppgaven er integrator.

| Pakke / løvformål | Mål og akseptansetest | Avhengighet / executor |
|---|---|---|
| P0 — velge bærende format (L5/L7) | 12 meldinger med literal, omordning, plural, nestet select, apostrof, tall/dato gir avtalt resultat i JS og Swift/macOS/Linux. Mål faktisk bygge-, pakkings- og vedlikeholdskostnad. Apple-projeksjon har tapsfri test eller eksplisitt avslag. | Før katalogformat fryses; plattformutvikler |
| P1 — språk følger eieren (L2) | Samme policy-fixture består i Swift/web/Binding: eier → flate → OS/header → nb-NO; q=0, q-rekkefølge, region, nn, ugyldig tag, manglende tekst og isolerte samtidige brukere. `resolved_locale` stemmer. | P0; scaffold-/Binding-utvikler |
| P2 — vedlikeholdbar katalog (L4/L5) | Første 50 meldinger går gjennom uttrekk, modellutkast som draft, menneskelig godkjenning og lokal bygging. Endret kildehash ugyldiggjør godkjenning; manglende variabel stopper build. Generering er repeterbar. | P0; verktøyutvikler + språkredaktør |
| P3 — Butterpop på nb/en (L1/L4) | Første synlige resultat: normal-, tom-, feil-, modererings- og spillerflate er dekket. Språkbytte bevarer innhold og utkast; begge locale-er viser riktige tilgjengelighetsnavn på mobil/desktop. | P1/P2; produktutvikler + Kjetil |
| P4 — engelsk nettinngang (L1/L4) | Sammenhengende forside/navigasjon/om/status, fungerende språklenker, lang/hreflang/canonical/sitemap og godkjent ordbruk. Eksisterende norsk URL-oppførsel består. | P1/P2, synlig etter P3; nettstedredaktør/-utvikler |
| P5 — språkfrie Interest/Purpose-identiteter (L3) | Første dataleveranse: gammel fixture migreres og kjøres på nytt uten nye ID-er; grafresultat og referanser er like ved språkbytte; kollisjoner bevares; aktiv publiserbar delmengde har 100 % godkjent nb/en-dekning. | P1/P2; CellBase-/datamigreringsutvikler |
| P6 — alle skeleton-tekster via felles mekanisme (L6) | Gammelt JSON-korpus dekoder uendret; nye label-former består web/Apple-paritet. Gamle klienter får lesbar v1-projeksjon uten å kunne overskrive originalen. Bok 12/22 og Explore-eksempler følger implementeringen. | P1/P2/P5; schema- og rendererutvikler |
| P7 — Porthole-shell (L1/L4) | Migrert shell har ingen uavklarte synlige strenger i uttrekksregisteret; navigation, notices og errors består brukerflyter i nb/en; eksisterende handlinger/ID-er er bevart. | P6; webutvikler |
| P8 — øvrige Leaf-flater (L1/L4) | Hver prioritert mal har deklarert dekning; lokaliserte feil-/tomtilstander og korrekt første render testes. Umigrerte maler listes eksplisitt. | P3; Vapor-/webutvikler |
| P9 — Butler/Kallimachos (L1/L2) | Samme spørsmål og relevante intent-uttrykk på nb/en gir riktig svartspråk, samme handling og bevarte kilde-/usikkerhetsgrenser. | P1/P2; agentintegrasjonsutvikler + fagredaktør |
| P10 — Binding-shell (L1/L7) | Shell-tekster, native katalogprojeksjon og generisk skeleton bruker samme effektive preferanse, også frakoblet. Ingen synlig etikett er ulik sitt tilgjengelighetsnavn. | P6; Binding-utvikler |
| P11 — porter (L5) | Python/Go/Rust leser og rundturbevarer nye ressurser og discovery uten datatap. Felles label-/locale-fixture gir samme resultat. | P5/P6; portutvikler |
| P12 — tredje språk og RTL (L1/L5) | Tilfør språk og locale-data kun i katalog/manifest. Ingen celle-/renderer-kodeendring. Test plural, lange strenger og RTL; merk resten av produktet som udekket. | P3–P11; integrator + språkredaktør |

Rekkefølge: P0 → P1/P2 → **P3 Butterpop → P4 nettsted**, med **P5 som første dataresultat**; deretter P6–P12. Nettstedets øvrige artikler og flere cellekataloger tas i små etterfølgende pakker med samme mal. Ingen «big bang» eller samlet migrering av private data er nødvendig.

Analysemålene L1–L7 er behandlet med anbefaling, begrensninger og testbare pakker. **Produktmålene er ikke oppnådd ennå.** P0 kan avkrefte gjennomførbarheten til anbefalt Swift-adapter innen anslaget; da må formatvalget vurderes på nytt før masseuttrekk.

## 6. Risiko og valg som bør unngås

| Risiko | Konkret styring |
|---|---|
| Oversettelse endrer identitet | Frosne gamle referanser, separate labels og eksplisitt migreringsmapping; navn er ikke oversettelsesnøkler som kan omskrives fritt. |
| Falsk bakoverkompatibilitet | Test både ny-leser/gammelt-data og gammel-leser/ny-projeksjon. Ny union er ikke automatisk lesbar for gamle klienter. |
| Fallback skjuler mangler | Dekning teller godkjent originalt mål-locale, ikke antall oppslag som ga en streng. |
| Doble kataloger | Én redigerbar autoritet per ressurs; `.xcstrings`, runtimepakker og HTML merkes generert etter migrering. |
| Egen halvt implementert pluralmotor | Bruk testet standardparser/formatter; avvis ikke-støttet profil i CI. |
| Fremmed tekst blir kode | Kataloger inneholder data. Escaping skjer ved DOM-/Leaf-grensen; oversettelser får ikke endre handlinger eller utføre kode. |
| En lokaliseringscelle blir global flaskehals | Lokale snapshots, batch, revisjonspinning og cache. Brukerens språkvalg må ikke kreve nettverk ved hver rendering. |
| Modell endrer løfter eller kilder | Menneskelig godkjenning knyttet til revisjon, særlig ved påstander og brukerrettet handlingsinformasjon. |
| Anslag blir lest som full HAVEN-dekning | Før eget register for umigrerte flater, cellefactory-tekster, artikler, grafetiketter og brukergenerert innhold. |

Unngå også å gjøre et felt som heter `locale` til en ny protokollidentitet eller autorisasjonsregel. Lokalisering er presentasjon og eksplisitte brukerpreferanser. Endringer i core, schema, tilgang eller dataflyt må behandles som de respektive implementeringspakkene når Kjetil har valgt retning.

## 7. Dom om Apple, anbefaling og beslutninger

**Apple er det beste ferdige forfatterverktøyet blant kandidatene for en Xcode-/SwiftUI-arbeidsflyt.** Det er min vurdering av samsvaret med HAVENs Binding-flate, ikke en målt universell rangering. Apple dokumenterer automatisk uttrekk, oversetterkontekst og genererte, typede `LocalizedStringResource`-symboler i Xcode 26. Dette gir god ergonomi når meldinger deklareres slik verktøyet kan oppdage dem. [Apple: Xcode-lokalisering][W2]

Utenfor Apple kan `.xcstrings` leses som JSON. Å avvise det som et lukket binærformat ville vært feil. Men HAVEN må da eie tolkning av variasjoner, argumentmapping, fallback, uttrekk fra JS/Leaf og Linux-bygging. Apples dokumenterte katalogbygging retter seg mot Xcode og genererer Apple-ressurser. Vi har ikke verifisert en komplett, tapsfri ferdigløsning som gjør dette til HAVENs felles runtime. [Apple: String Catalogs][W1]

Kompromisset har også en kostnad: velges ICU-katalogen, får ikke alle dynamiske skeleton-tekster Apples automatiske uttrekk gratis. De kommer fra data og løses av den generelle adapteren. `.xcstrings`-generatoren bør først håndtere literal/enkle typede meldinger og bare pluralvarianter med bevist lik semantikk. Sammensatte ICU-uttrykk skal bruke felles formatter, ikke feilaktig konverteres. En redigering gjennom Apples verktøy kan senere importeres som kandidat til kanonisk katalog; toveis tapsfri import er ikke lovet.

**Min ene anbefaling:** velg repo-eide JSON-ressurser med ICU MessageFormat 1 nå, gjenbruk eksisterende locale-/taksonomifelter, og bygg én adapter per runtime. Bruk Apples løsninger der de gir konkret nytte gjennom genererte ressurser. Utsett den dynamiske lokaliseringscellen til behovet er vist. Bevar stabile nøkler og et versjonert `format`-felt så MF2 kan innføres med katalogkonvertering og paritetstester senere; MF1 og MF2 har forskjellig syntaks, og migreringen er ikke automatisk kostnadsfri. Prosjektet `messageformat` dokumenterer en MF1→MF2-bro, men HAVEN må teste sitt faktiske innhold. [Unicode MF2][W3], [messageformat][W14]

Jeg ville skifte til **MF2 som kanonisk meldingsformat** dersom en støttet Swift/macOS/Linux-runtime består HAVEN-prøven uten større vedlikeholds-/pakkingskostnad enn MF1-adapteren. Jeg ville skifte til **`.xcstrings` som kanonisk kilde** dersom en konkret kryssplattformkonverter demonstrerer alle nødvendige grammatikk-/argumenttilfeller, og målt tidsbruk på samme Butterpop-prøve er lavere — eller Kjetil prioriterer Apples forfatterverktøy høyere enn denne portabilitetskostnaden. Flere stjerner eller at et format er JSON er ikke tilstrekkelig bevis.

| Beslutning | Mitt råd |
|---|---|
| Q1: anonymt standardspråk | Bruk lagret eksplisitt valg, ellers nettleser/OS; nb-NO ved manglende treff. Norsk tilgjengelighet krever ikke norsk for alle. |
| Q2: rotdata eller repo | Repo-filer først, lokale genererte snapshots ved kjøring. Senere celle-/rotdata-distribusjon ved dokumentert behov. |
| Q3: første flate | Butterpop først; sammenhengende engelsk inngang på digipomps.org rett etter. Interest først i datalaget. |
| Q4: kildeformat | JSON + ICU MessageFormat 1, med Apples kataloger som kontrollert projeksjon. Bekreft formatbeslutningen gjennom P0 før stort uttrekk. |

Neste handling etter Kjetils valg er å opprette PDD-mappen og spesifisere P0–P5 med faktiske filer, målinger og godkjenningsgrenser. Denne analysen autoriserer ikke implementering eller publisering.

<!-- Lokale kildeankre: linjene gjelder leste arbeidskopier 2026-09-07. -->
[R1]: /Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellBase/Cells/Commons/CommonsTaxonomyCell.swift:184
[R2]: /Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/commons/schemas/haven.core/Sources/HavenCoreSchemas/LocalizationContracts.swift:6
[R3]: /Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellBase/PurposeAndInterest/PerspectiveNode.swift:41
[R4]: /Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellBase/PurposeAndInterest/Interest.swift:42
[R5]: /Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellBase/PurposeAndInterest/Purpose.swift:41
[R6]: /Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellBase/PurposeAndInterest/Perspective.swift:378
[R7]: /Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellBase/Skeleton/SkeletonDescription.swift:1752
[R8]: /Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellBase/CellConfiguration/CellConfiguration.swift:6
[R9]: /Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Public/js/porthole-webo.js:1682
[R10]: /Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Resources/Views/butterpop_studio.leaf:2
[R11]: /Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Public/js/butterpop-studio.js:1
[R12]: /Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Sources/App/Cells/PersonalCopilot/PersonalCopilotCloudStore.swift:5321
[R13]: /Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Sources/App/Controllers/VaporBrowserhead.swift:33
[R14]: /Users/kjetil/Build/Digipomps/HAVEN/CellProtocolDocuments/Website/RELEASE_NOTE_2026-09-07.md:3
[R15]: /Users/kjetil/Build/Digipomps/HAVEN/CellProtocolDocuments/Website/en/artikler/from-the-2019-sketch-to-today/index.html:13
[R16]: /Users/kjetil/Build/Digipomps/HAVEN/PyCellProtocol/src/cellprotocol/configuration.py:86
[R17]: /Users/kjetil/Build/Digipomps/HAVEN/GoCellProtocol/configuration.go:108
[R18]: /Users/kjetil/Build/Digipomps/HAVEN/RustCellProtocol/src/configuration.rs:16
[R19]: /Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Sources/App/Support/EntityAnchorDataV1Contract.swift:406
[R20]: /Users/kjetil/Build/Digipomps/HAVEN/CellProtocolDocuments/Book/12_Skeleton_Spec.md:1
[R21]: /Users/kjetil/Build/Digipomps/HAVEN/CellProtocolDocuments/Book/22_Explore_Contracts_For_Skeleton_Authoring.md:179
[R22]: /Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Public/js/skeleton-runtime.js:360
[R23]: </Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/Suggestion/SkeletonView.swift:1805>
[R24]: /Users/kjetil/Build/Digipomps/HAVEN/CellProtocolDocuments/Website/rettelser/index.html:23

<!-- Eksterne primærkilder; alle åpnet 2026-09-07. -->
[W1]: https://developer.apple.com/videos/play/wwdc2023/10155/ "Apple: Discover String Catalogs; åpnet 2026-09-07"
[W2]: https://developer.apple.com/videos/play/wwdc2025/225/ "Apple: Explore localization with Xcode; åpnet 2026-09-07"
[W3]: https://www.unicode.org/reports/tr35/tr35-messageFormat.html "Unicode UTS #35 del 9, hentet v48.2; åpnet 2026-09-07"
[W4]: https://unicode-org.github.io/icu-docs/apidoc/released/icu4c/classicu_1_1message2_1_1MessageFormatter.html "ICU4C 78.3 MessageFormatter, Technical Preview; åpnet 2026-09-07"
[W5]: https://projectfluent.org/ "Project Fluent: grammatikk og plattformer; åpnet 2026-09-07"
[W6]: https://www.gnu.org/software/gettext/manual/html_node/Workflow-flags.html "GNU gettext: Workflow flags; åpnet 2026-09-07"
[W7]: https://docs.python.org/3/library/gettext.html "Python: gettext; åpnet 2026-09-07"
[W8]: https://github.com/i18next/i18next "i18next: prosjektets README; åpnet 2026-09-07"
[W9]: https://formatjs.github.io/docs/core-concepts/icu-syntax/ "FormatJS: ICU-syntaks; åpnet 2026-09-07"
[W10]: https://unicode-org.github.io/icu/userguide/format_parse/messages/ "ICU: Formatting Messages; åpnet 2026-09-07"
[W11]: https://unicode-org.github.io/icu-docs/apidoc/released/icu4c/classicu_1_1MessageFormat.html "ICU4C: stabil MessageFormat, navngitte argumenter; åpnet 2026-09-07"
[W12]: https://github.com/miroslavkovac/Lingo "Lingo: JSON-syntaks og dokumenterte begrensninger; åpnet 2026-09-07"
[W13]: https://github.com/vapor-community/Lingo-Vapor "Lingo-Vapor: Leaf-tags; åpnet 2026-09-07"
[W14]: https://github.com/messageformat/messageformat "messageformat: MF1, MF2 og konverteringspakker; åpnet 2026-09-07"
[W15]: https://github.com/unicode-org/message-format-wg/blob/main/spec/README.md "Unicode MFWG: ikke-normativ implementasjonsliste; åpnet 2026-09-07"
[W16]: https://github.com/projectfluent/fluent.js "Project Fluent: JS-implementasjon; åpnet 2026-09-07"
[W17]: https://github.com/projectfluent/python-fluent "Project Fluent: Python-implementasjon; åpnet 2026-09-07"
[W18]: https://github.com/kaptinlin/messageformat-go "MessageFormat Go: egen dokumentasjon, ikke uavhengig konformitetsbevis; åpnet 2026-09-07"
[W19]: https://github.com/sajikix/mf2-parser "Rust MF2-parser, ikke bevis for formatter; åpnet 2026-09-07"
[W20]: https://github.com/projectfluent/fluent-rs "Project Fluent: Rust-implementasjon; åpnet 2026-09-07"
[W21]: https://formatjs.github.io/docs/rust/ "FormatJS: Rust og ICU4X-underlag; åpnet 2026-09-07"
[W22]: https://www.rfc-editor.org/rfc/rfc4647.html "RFC 4647: Matching of Language Tags; åpnet 2026-09-07"
[W23]: https://www.rfc-editor.org/rfc/rfc9110.html "RFC 9110: Accept-Language, Content-Language, Vary; åpnet 2026-09-07"
[W24]: https://developers.google.com/search/docs/specialty/international/localized-versions "Google Search Central: localized versions; åpnet 2026-09-07"
[W25]: https://formatjs.github.io/docs/getting-started/message-extraction/ "FormatJS: uttrekk av deklarerte meldinger; åpnet 2026-09-07"
[W26]: https://babeljs.io/docs/babel-parser "Babel-parser; åpnet 2026-09-07"
[W27]: https://github.com/swiftlang/swift-syntax "SwiftSyntax: parsing og transformasjon; åpnet 2026-09-07"
[W28]: https://www.unicode.org/cldr/charts/48/supplemental/language_plural_rules.html "CLDR 48: språkspesifikke pluralregler; åpnet 2026-09-07"
[W29]: https://tc39.es/ecma402/ "ECMA-402 redaktørutgave: Intl-formatering; ikke garanti for browserutrulling; åpnet 2026-09-07"
[W30]: https://www.unicode.org/reports/tr35/tr35-dates.html "Unicode LDML: datoer og tidssoner; åpnet 2026-09-07"
[W31]: https://www.w3.org/International/questions/qa-html-dir "W3C: strukturell RTL-markup; åpnet 2026-09-07"
