# HANDOFF — Lokalisering i HAVEN: grundig analyse av mest effektiv og fremtidsrettet implementering

Mappe: `CellProtocolDocuments/Deliverables/Lokalisering_Analyse_2026-09-07/`
Fra: Losen (Claude), 2026-09-07 → Til: Codex-økt (gjerne med «Astra» om Kjetil vil teste den) eller ny Claude-tråd.
Type: **analyse, ikke implementering.** Ingen kodeendringer. Resultatet er et beslutningsgrunnlag Kjetil kan si ja/nei til, og som deretter blir en PDD-mappe (`haven-purpose-driven-dev`).

Kjør: `./run_l.sh L1_ANALYSE` (Codex via launchctl, samme mekanikk som Forskningsagenda RundeB; se README i mappen). Prompten ligger i `L1_ANALYSE_prompt.md` og ber om at svaret skrives til `L1_ANALYSE.md` — **ikke** til `_svar.md`, som er Codex' `-o`-fil (lærdom 07.09: ellers overskrives notatet).

---

## §0 Intent (Kjetils ord, uendret, 2026-09-07)

> Vi har vel tidligere snakket om lokalisering - infosidene (og ikke minst butterpop studio) burde være tilgjengelige på engelsk samtidig som det hadde vært fint at det - av respekt for hjemlandet - er tilgjegelig på norsk også. Bør være styrt av egne preferanser om tilgjengelig eller inntilling i nettleser. Er det mye jobb å få på plass? Vi vil trenge det omtrent over alt når jeg tenker etter. Kan f.eks en interesse være språkuavhengig og ha lokaliserte labels?

> Ok lokalisering - og spesielt effektiv lokalisering må vi sette til en annen tråd - eller faktisk dette kan vi bruke Codex til - og da kanskje teste Astra på utfordrringen. Lag et handoff for en grundig analyse av hvordan vi mest mulig effektivt og fremtidsrettet kan imprlementere lokalisering. (Personlig liker jeg godt apple sin løsning men og du eller codex kommer på noe bedre er jeg lutter øre)

## §1 Formålet, dekomponert (analysen måles mot dette)

| ID | Delformål | Test på analysen |
|---|---|---|
| L1 | Alle flater og alt innhold kan vises på norsk (nb-NO) og engelsk (en-US), og flere språk senere uten ny arkitektur | Anbefalingen viser hvordan et tredje språk legges til uten kodeendring i celler eller renderere |
| L2 | Språk styres av brukerens egen preferanse (i entiteten) når den finnes, ellers nettleser/OS, ellers nb-NO | Én navngitt oppløsningsregel, samme i Swift, web-JS og Binding, med `resolved_locale` synlig i svar |
| L3 | Data (interesser, formål, taksonomi, kataloger) er språkuavhengige med lokaliserte labels | Konkret skjema for `Interest`/`Purpose` + migrering fra dagens `name`; dekningssjekk som test |
| L4 | **Effektivt**: minst mulig tekst-uttrekk og vedlikehold; oversettelse kan gjøres av språkmodell med menneskelig godkjenning | Anslag i timer per flate; verktøykjede for uttrekk → oversettelse → godkjenning → deploy |
| L5 | **Fremtidsrettet**: ett kildeformat som virker for Swift (Vapor + SwiftUI/Binding), web (vanilla JS/Leaf), statiske sider, og portene (Python, Go, Rust) | Formatet er lesbart uten Apple-verktøy; plural/kjønn/tall/dato dekkes; RTL vurdert |
| L6 | Skeleton-flater (CellConfiguration) lokaliseres uten spesialkode per flate — i tråd med kravet «alle skeletons rendres uten spesialkode» | Forslag til `label`-utvidelse i `SkeletonDescription` som er bakoverkompatibel |
| L7 | Kjetils preferanse for Apples løsning er vurdert på like vilkår med alternativene | Options-matrise med Apple String Catalogs som én av kandidatene, med ærlig for/imot for ikke-Apple-mål |

## §2 Audit — hva som faktisk finnes (lest 2026-09-07, med sti)

| # | Funn | Status | Kilde |
|---|---|---|---|
| A1 | `CommonsTaxonomyCell` gjør allerede «språkuavhengig term + lokaliserte labels»: BCP-47-locale, default `nb-NO`, batch-oppslag med `requested_locale`/`resolved_locale`, og dekningsvarsel for `required_locales` (`nb-NO`, `en-US`) | **retrieved** — mønsteret finnes | `CellProtocol/Sources/CellBase/Cells/Commons/CommonsTaxonomyCell.swift:184–273, 330, 574–620` |
| A2 | `Interest` har `name: String` som både nøkkel og visningstekst; oppslag via `interestNameReferences[name]`; ingen labels | **retrieved** | `CellProtocol/Sources/CellBase/PurposeAndInterest/Interest.swift:13–40`; `PerspectiveNodeImpl` |
| A3 | Skeleton: `SkeletonButton.label: String` (+ `labelKeypath`), ingen locale-felt noe sted i `SkeletonDescription.swift` | **retrieved** | `CellProtocol/Sources/CellBase/Skeleton/SkeletonDescription.swift:1749–1793` |
| A4 | Porthole web: `Public/js/porthole-webo.js` er 9 884 linjer med norsk UI-tekst i JS-strenger; ingen i18n; `localeCompare(…, "nb")` på linje 1682 | **retrieved** | `CellScaffold/Public/js/porthole-webo.js` |
| A5 | Leaf-maler: 25 filer i `Resources/Views`; `butterpop_studio.leaf` (327 linjer) har `lang="no"` og norsk tekst; `base.leaf` har `lang="en"` | **retrieved** | `CellScaffold/Resources/Views/` |
| A6 | Butler/Co-Pilot: ~330 linjer norsk svartekst og intent-nøkkelord (både nb og en varianter, f.eks. «api nøkkel»/«api key») i Swift | **retrieved** | `CellScaffold/Sources/App/Cells/PersonalCopilot/PersonalCopilotCloudStore.swift` |
| A7 | Ingen `Accept-Language`/`preferredLanguage`-håndtering funnet i `CellScaffold/Sources`, `Public/js`, `Resources` | **retrieved (fravær)** | grep 07.09 |
| A8 | Binding (SwiftUI): ingen `.xcstrings`, `.lproj` eller `String(localized:)` funnet i `Binding/Binding` og `Binding/Cells` | **retrieved (fravær)** — Apples mekanisme er ikke tatt i bruk der den ville vært mest naturlig | find/grep 07.09 |
| A9 | digipomps.org: statisk HTML, nb-only, i `CellProtocolDocuments/Website/`; første en-side lagt 07.09 med `hreflang` (`en/artikler/from-the-2019-sketch-to-today/`) | **retrieved** | `Website/`, `Website/RELEASE_NOTE_2026-09-07.md` |
| A10 | Portene Python/Go/Rust har ingen skeleton-rendering og ingen i18n; de vil trenge å *lese* labels, ikke produsere dem | **retrieved (delvis)** | `PyCellProtocol/`, `GoCellProtocol/`, `RustCellProtocol/` |
| A11 | EntityAnchor-data har ingen `locale`-/språkpreferanse-post | **retrieved (fravær)** | `CellScaffold/Sources/App/Support/EntityAnchorDataV1Contract.swift` |
| A12 | Book 12 (Skeleton Spec) og Book 22 (Explore Contracts for Skeleton Authoring) er de normative dokumentene som må endres hvis skeleton får locale-støtte | **retrieved** | `CellProtocolDocuments/Book/12_*.md`, `22_*.md` |

Ingenting `recalled` er lastbærende.

## §3 Det analysen skal levere (`L1_ANALYSE.md`, norsk, PhD-nivå på kilder, alle eksterne fakta med URL + dato)

1. **Options-matrise** for kildeformat og runtime, minst disse kandidatene, vurdert mot L1–L7:
   - Apple String Catalogs (`.xcstrings`, JSON) + `String(localized:)`/`LocalizedStringResource` + `Locale` — Kjetils preferanse; vurder også `.xcstrings` som *felles kildeformat* konsumert av web/Vapor/porter uten Xcode.
   - Unicode MessageFormat 2 (MF2, CLDR/ICU) — plural/kjønn/tall; status og biblioteker i Swift/JS/Python/Go/Rust.
   - Fluent (Mozilla, `.ftl`) — asymmetrisk lokalisering; biblioteker per språk.
   - gettext (`.po`) — det mest utbredte; verktøykjede; svakheter for JSON-first.
   - i18next / FormatJS (ICU MessageFormat) for web; Vapor `Lingo`/Leaf-tags for server.
   - «HAVEN-native»: en lokaliseringscelle (`cell:///Localization`) som eier katalogen som data i rotdata, med samme oppslagskontrakt som `CommonsTaxonomyCell`, og som renderere (web, Binding, Leaf) spør — vurder om dette er bedre enn eller komplementært til de andre.
2. **Anbefalt arkitektur** i tre lag (data / flater / innhold), med locale-oppløsningsregelen (L2), skjema for `Interest`/`Purpose` (L3), skeleton-utvidelse (L6, bakoverkompatibel: `label` streng *eller* `{key}`/`{nb-NO:…, en-US:…}`), og hvor katalogen bor (fil i repo? rotdata? celle-state?). Si eksplisitt hva som er *ett* kildeformat og hva som er generert.
3. **Effektivitet (L4):** hvordan trekke ut de ~9 900 linjene i `porthole-webo.js`, Leaf-malene og Butler-tekstene med minst mulig manuelt arbeid (AST-basert uttrekk? regex? LLM-assistert med diff-godkjenning?); hvordan språkmodell-oversettelse med menneskelig godkjenning kan gå inn i samme flyt som rettelsesloggen på nettstedet; anslag i timer per flate; hva som kan gjøres flate for flate uten «big bang».
4. **Fremtidsrettet (L5):** hva som skjer ved tredje språk; RTL; plural/kjønn i norsk vs engelsk; tall/dato/valuta (NOK/EUR) via CLDR; hvordan portene leser katalogen; hvordan agenter (Butler, Kallimachos) får språk fra samme regel som flatene.
5. **Migreringsplan** som arbeidspakker i PDD-form (én per løvformål, med test), i anbefalt rekkefølge — der Butterpop Studio og digipomps.org er første synlige resultat, og `Interest`-labels første datalagsresultat.
6. **Risiko og det som ikke bør gjøres**: f.eks. å oversette `name`-nøkler, å låse katalogen til Xcode-verktøy, å la modeller oversette uten godkjenning, å lokalisere før locale-regelen finnes.
7. **Ærlig dom om Apples løsning** for HAVENs faktiske mål (Vapor på Linux, vanilla JS, statisk HTML, tre porter): hva den gir gratis i Binding, og hva som må lages selv utenfor.

## §4 Regler for analysen
- Les kildene i §2 før du skriver; siter filsti og linje. Eksterne påstander om biblioteker/standarder: åpne URL, oppgi dato; merk «ikke verifisert» ellers.
- Ingen kodeendringer, ingen git. Skriv bare til denne mappen.
- Hold Kjetils preferanse og motargumentene like synlige; anbefal én ting, med hva som ville fått deg til å skifte mening.
- Maks ~6 000 ord + matriser. Norsk.

## §5 Etter analysen (Kjetil beslutter)
Q1 Standardspråk for anonyme: nb-NO alltid, eller nettleserens språk med nb-NO som fallback? · Q2 Skal katalogen være rotdata (signert, Ward) eller vanlig repo-fil? · Q3 Første flate: Butterpop Studio eller digipomps.org? · Q4 Kildeformat: det analysen anbefaler, eller Apples uansett?
