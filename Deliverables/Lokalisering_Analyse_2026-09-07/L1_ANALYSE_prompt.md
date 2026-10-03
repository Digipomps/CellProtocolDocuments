# L1_ANALYSE — Lokalisering i HAVEN: mest effektiv og fremtidsrettet implementering

Du er en senior arkitekt med dyp erfaring fra internasjonalisering på tvers av Apple-plattformer (String Catalogs, Foundation), web (ICU MessageFormat, i18next/FormatJS, Fluent), server (Vapor/Leaf, gettext) og Unicode/CLDR (MessageFormat 2). Du har websøk. Skriv svaret til **`L1_ANALYSE.md` i denne mappen** (ikke til `L1_ANALYSE_svar.md`), på norsk, PhD-nivå på kilder: alle eksterne fakta med URL du har åpnet og dato; «ikke verifisert» ellers. Ingen kodeendringer, ingen git.

## Les først, i denne rekkefølgen
1. `HANDOFF.md` i denne mappen — §0 (Kjetils ord), §1 (formål L1–L7 som analysen måles mot), §2 (audit med filstier), §3 (leveransen), §4 (regler).
2. `/Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellBase/Cells/Commons/CommonsTaxonomyCell.swift` — det eksisterende mønsteret for term + lokaliserte labels.
3. `/Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellBase/PurposeAndInterest/Interest.swift` og `PerspectiveNodeImpl` — dagens `name`-nøkkel.
4. `/Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellBase/Skeleton/SkeletonDescription.swift` — `label`/`labelKeypath`; og `CellProtocolDocuments/Book/12_Skeleton_Spec.md`, `22_Explore_Contracts_For_Skeleton_Authoring.md`.
5. `/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Public/js/porthole-webo.js` (9 884 linjer — mål omfanget av UI-strenger, ikke les alt), `CellScaffold/Resources/Views/butterpop_studio.leaf`, og `CellScaffold/Sources/App/Cells/PersonalCopilot/PersonalCopilotCloudStore.swift` (svartekster og intent-nøkkelord).
6. `/Users/kjetil/Build/Digipomps/HAVEN/Binding/` — bekreft at ingen `.xcstrings`/`String(localized:)` er i bruk.
7. `/Users/kjetil/Build/Digipomps/HAVEN/CellProtocolDocuments/Website/` — statisk nb-only nettsted; `en/artikler/from-the-2019-sketch-to-today/` er første en-side; `RELEASE_NOTE_2026-09-07.md`.
8. `/Users/kjetil/Build/Digipomps/HAVEN/Kallimachos/Verdifordeling/Sachs_2026-09-07/Nettside/LOKALISERING_Vurdering_2026-09-07.md` — Losens foreløpige vurdering (utfordre den der du er uenig).

## Lever nøyaktig det HANDOFF §3 ber om, punkt 1–7, i den rekkefølgen
Krav som er lette å glemme:
- Options-matrisen skal ha Apple String Catalogs som én rad, vurdert også som *felles kildeformat* (`.xcstrings` er JSON) for web/Vapor/porter uten Xcode — Kjetil liker Apples løsning, og fortjener et ærlig svar på om den bærer utenfor Apple.
- Ta stilling til en «HAVEN-native» lokaliseringscelle med samme oppslagskontrakt som `CommonsTaxonomyCell` — er det bedre, verre eller komplementært?
- Locale-oppløsning: én regel (egen preferanse i entiteten → valg på flaten → `Accept-Language`/OS → nb-NO) med `resolved_locale` i hvert svar. Foreslå hvor preferansen bor i EntityAnchor-data.
- Skeleton: utvidelsen må være bakoverkompatibel med alle eksisterende CellConfiguration-JSON (streng-`label` skal fortsatt virke).
- Effektivitet: gi timeanslag per flate og en konkret uttrekksmetode for `porthole-webo.js`; foreslå hvordan LLM-oversettelse med menneskelig godkjenning kan gå inn i samme flyt som rettelsesloggen.
- Migreringsplan som PDD-arbeidspakker (én per løvformål, hver med test og executor).
- Avslutt med: din ene anbefaling; hva som ville fått deg til å skifte mening; og svar på Q1–Q4 i HANDOFF §5 slik du ville rådet Kjetil.

Maks ~6 000 ord pluss matriser.
