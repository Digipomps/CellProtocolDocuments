# Formålsspesifikasjon — palazzo bordbestilling

Oppgavemappe: `PDD_palazzo-bordbestilling_2026-10-06` · Opprettet 2026-10-06 · Iterasjon 2 (ikke godkjent)

**Les dette først.** G1 er ikke gitt. Koden for cellene og rutene er likevel skrevet, natt til 7. oktober 2026,
på ordene dine fra kvelden før og på det jeg skrev til deg kl. 23:49 (21:49 UTC): «GastroPlanner-delen bygger jeg
på ditt ord fra i kveld, uten G1, og legger formålene og bildene fram i morgen sammen med det som er bygget.»
Ingen flate er bygget, ingenting er satt ut, og grenen er ikke pushet. Sier du nei til formålene her, er det
grenen som må endres eller kastes, ikke noe som er i bruk. Stier er relative til HAVEN-roten.

**Rettet 7. oktober, etter uavhengig kontroll.** Fem tråder som ikke hadde skrevet noe av dette, leste koden og
dokumentene samme natt. De fant tre alvorlige feil i koden, og at dokumentene sa mer enn koden gjorde. Feilene er
rettet i en andre commit, og teksten her er rettet der den var feil. Se `STATUS.md` og `TESTRESULT.md#kontroll`.

> Regel: ingen plan før G1 er godkjent av Kjetil. For GUI: ingen implementering før G1-GUI (rendret bilde) er godkjent.
> Et dokument om leveransen teller aldri som leveransen.

## 0. Intensjon (ordrett) og brief-audit

> «Om du slipper opp for ting å gjøre kan du impelmentere samme funksjonalitet som det er i GastroPlanner»

Kjetil, 6. oktober 2026 kl. 23:44 (21:44 UTC), i samtalen.

Det du har sagt om det samme før. Kilden skriver selv at ordene er forkortet:

> «3. Kan vi integrere oss mot GastroPlanner? Hva slags funksjonalitet har GastroPlanner — så vi kan vurdere å implementere det selv for mer sømløs interaksjon gjest/kelner/kjøkken/eier?»
>
> «5. Alle entiteter lagrer egne data i egen entitet. Restauranten lagrer IKKE allergiopplysninger, men sikrer seg tilgang til å spørre når det er nødvendig.»

`PalazzoComunaleScaffold/research/2026-09-02/contract.md`, linje 19–20 og 23–24, under overskriften «Oppdraget (Kjetils ord, 2026-09-02, forkortet)».

> «besøk, bookinger, interaksjoner, formål, interesser havner i alles private entitet»

`PalazzoComunaleScaffold/docs/Design_PalazzoScaffold_2026-09-02.md`, linje 25, kolonnen «Krav (ordrett)».

**Slik jeg har lest ordene.** «Samme funksjonalitet» er det GastroPlanner gjør i kjernen for en restaurant, bygget i Palazzos egne celler. Punkt 5 fra 2. september avgjør én ting GastroPlanner gjør som dette ikke skal gjøre: huset lagrer ikke opplysninger om gjesten. Du har ikke sagt at GastroPlanner skal erstattes, og jeg har ikke lest det slik. Importen fra GastroPlanner står urørt, conciergen viser fortsatt til GastroPlanner for bordbestilling, og ingenting er satt ut. Det valget er spørsmål 1 i §6.

**Vilkåret i ordene dine.** «Om du slipper opp for ting å gjøre» er et vilkår, ikke en bestilling. Jeg begynte på dette kl. 01:30 (23:30 UTC), da testen for avvik 4, lærdommene, planen og bildene for hovedoppgaven var skrevet. Ingen uavhengig tråd hadde lest dem ennå. Den kontrollen kom etterpå, og fant feil der også. Om vilkåret var oppfylt, er ditt å si.

### Brief-audit {#audit}

| Påstand i intensjonen / antatt kapabilitet | Audit (retrieved / recalled / unavailable / contradicted) | Kilde |
|---|---|---|
| GastroPlanner har bestilling på nett, bord med minste og største antall og område, bord som slås sammen, områder som åpnes og stenges, seteplaner, tak per tidspunkt, venteliste, walk-in, intern bestilling, oversikt med nøkkeltall, avbestilling med frist, kortgaranti, SMS og e-post, gjesteregister med notater og allergier, Reserve with Google og flere lokaler | retrieved 6. oktober 2026 av en lesetråd, fra GastroPlanners egne sider og researchen fra 2. september. Ikke prøvd i GastroPlanner selv; ingen av oss har en konto der | `HAVEN-Deploy/_handoff/HD-0077/maal/grunnlag-20261007/les/L1-GASTROPLANNER.md` |
| GastroPlanner har ingen offentlig dokumentasjon for utviklere | retrieved. Kilden sier «no public developer documentation», sjekket 2. september 2026. At det ikke finnes noe API, har ingen av oss slått fast | `PalazzoScaffold/Sources/App/Cells/PalazzoGastroPlannerCell.swift`, linje 9–20 |
| PalazzoScaffold har alt en celle for GastroPlanner | retrieved. Den er en import av en CSV-eksport med kolonnekobling og ett avledet svar. Den tar ikke imot bestillinger | samme fil, linje 28–343 |
| Kelnerflaten leser kommende bestillinger fra den cellen, og briefen leser feltet `guestCell` fra en bestilling for å finne gjestens entitet. Ingenting skrev det feltet | retrieved, på `31ce1ae7` | `PalazzoScaffold/Sources/App/Cells/PalazzoStaffShellCell.swift`, linje 310–324 og 378–403 |
| En celle kan slippe andre enn eieren til på navngitte nøkkelstier, uten avtale | retrieved, på CellProtocol-pinnen `81601a6f` | `CellProtocol/Sources/CellBase/Cells/GeneralCell/GeneralCell.swift`, `validateCellSpecificAccess`; brukt slik i `PalazzoScaffold/Sources/App/Cells/PalazzoHouseCell.swift`, linje 66–76 |
| Husets ansattliste avgjør hvem som er ansatt | retrieved | `PalazzoScaffold/Sources/App/Cells/PalazzoHouseCell.swift`, linje 356–362 |
| Gjestens entitet har posttypen `booking`. Poster kan legges til, ikke endres eller fjernes | retrieved | `PalazzoScaffold/Sources/App/Models/PalazzoEntityModels.swift`, linje 9–19; `PalazzoScaffold/Sources/App/Cells/PalazzoEntityCell.swift`, linje 460–475 |
| Huset har et regneark der integrasjonene legger radene sine, og huset kan spørre mot det | retrieved | `PalazzoScaffold/Sources/App/Cells/PalazzoSheetCell.swift`, linje 444–492 |
| Du har valgt mellom å erstatte GastroPlanner, kjøre ved siden av, eller bare vise dit | **unavailable**. Ingen slik beslutning er funnet. Det som finnes, er forslag fra tråder: «GastroPlanner forblir system of record», og «C (erstatte) tidligst 2027 og bare hvis A/B stenges» | `PalazzoComunaleScaffold/docs/Prosjektskisse_Palazzo_Comunale_2026-09-01.md`, linje 175; `PalazzoComunaleScaffold/docs/Design_Integrasjoner_og_Datastrategi_2026-09-02.md`, linje 110–113 |
| Swift kan bygges i Losens skyarbeidsområde | **contradicted**. Docker Hub og swift.org er sperret der. Alt er bygget og testet på Mac-en gjennom køen | målt 6. oktober 2026 |

## 1. Formålstre

| purposeRef | Tittel | Forelder | Goal (outcome) | Verifier | Status |
|---|---|---|---|---|---|
| purpose://candidate.palazzo-bordbestilling.root | Huset tar imot bord selv | ingen passende node i Book 23 | Huset kan ta imot og styre bordbestillinger i egne celler, med kjernen av det GastroPlanner gjør, uten å lagre opplysninger om gjesten | Alle bladformålene under er oppfylt | candidate |
| purpose://candidate.palazzo-bordbestilling.bordplan (B1) | Bordplan | root | Huset beskriver bordene (navn, minste og største antall, område, hvilke som kan slås sammen) og åpner og stenger områder. En plan med feil lagres ikke, og en plan kan ikke fjerne eller krympe et bord noen holder | Tester i §5: `test.b1.*` | candidate |
| purpose://candidate.palazzo-bordbestilling.seteplan (B2) | Seteplan | root | Huset bestemmer hvilke dager og tider det kan bestilles, hvor lenge et bord holdes, og hvor mange som kan komme samtidig | `test.b2.*` | candidate |
| purpose://candidate.palazzo-bordbestilling.ledighet (B3) | Ledighet | root | Den som spør, får bare tider som kan bestilles, og det samme bordet gis aldri til to selskaper i overlappende tid, heller ikke over midnatt | `test.b3.*` | candidate |
| purpose://candidate.palazzo-bordbestilling.bestilling (B4) | Bestille, endre, avbestille | root | En bestilling kan lages, endres og avbestilles. En endring som ikke får plass, lar bestillingen stå urørt. Krever seteplanen at huset bekrefter, må huset bekrefte på nytt når gjesten endrer | `test.b4.*` | candidate |
| purpose://candidate.palazzo-bordbestilling.walk-in (B5) | Walk-in | root | Huset setter et selskap nå, uten forhåndsbestilling | `test.b5.*` | candidate |
| purpose://candidate.palazzo-bordbestilling.venteliste (B6) | Venteliste | root | Når det er fullt, eller taket er nådd, kan gjesten stå på venteliste. Når noen avbestiller, ser huset hvem som nå får plass, den som ba først, først. Listen er et råd til huset: reglene holder ikke bordet av til den som står først (spørsmål 7 i §6) | `test.b6.*` | candidate |
| purpose://candidate.palazzo-bordbestilling.oversikt (B7) | Dagen | root | Huset ser dagens bestillinger, kuverter, bordliste og nøkkeltall for dagen før, dagen og de neste sju dagene | `test.b7.*` | candidate |
| purpose://candidate.palazzo-bordbestilling.ingen-gjestedata (B8) | Ingen gjestedata hos huset | root; nærmest `purpose://access.audit.privacy` i Book 23 | Det huset lagrer om en bestilling, har ikke felt for navn, telefon, e-post, notat eller allergi, og ingen fri tekst. For det gjesten bestiller selv, holder huset identiteten som bestilte og en peker til gjestens entitet, og gjesten kan se at huset har pekeren. Bestilling, endring, avbestilling og bord fra ventelisten føres i husets logg | `test.b8.*` | candidate |
| purpose://candidate.palazzo-bordbestilling.gjesten-selv (B9) | Gjesten bestiller selv | root | En gjest bestiller, ser, endrer og avbestiller sitt eget bord, og bestillingen ligger i gjestens egen entitet. Én identitet kan ikke bestille bort huset; grensen gjelder per identitet, ikke per person | `test.b9.*` | candidate |
| purpose://candidate.palazzo-bordbestilling.kelneren (B10) | Kelneren ser bestillingene | root | Kelnerflaten teller husets egne bestillinger sammen med de importerte, og briefen finner gjestens entitet fra referansen uten å lese noe gjesten ikke har delt | `test.b10.*` | candidate |
| purpose://candidate.palazzo-bordbestilling.tilgang (B11) | Tilgang følger nøkkelstien | root; `purpose://cell.authorization-honours-keypath` i pakken | Feil spørrer og feil nøkkelsti avvises: en gjest når ikke husets side, en `staff:`-påstand er ikke nok, og planen er husets alene | `test.cell.auth-negative`, `test.b11.*` | candidate |
| purpose://candidate.palazzo-bordbestilling.egne-tall (B12) | Huset spør sine egne tall | root | Bestillingene ligger i husets regneark, så huset kan spørre med spørring og formel | `test.b12.*` | candidate |

Regler: velg fra Book 23 og pakkene først; nye noder får `purpose://candidate.…` og navngis her, aldri av en modell.
Hvert bladformål skal ha en test i §5. Et formål uten observerbart Goal er ikke klart til arbeid.

## 2. Avgrensning og avhengigheter

Hva dette IKKE er:
- Ikke en erstatning for GastroPlanner i drift. Importen står, og conciergen viser fortsatt dit. Valget er ditt (§6, spørsmål 1).
- Ikke en flate. Det er celler og ruter. Hverken gjestens bestillingsside eller husets bordbok er tegnet ferdig eller bygget. Skissene i `images/` er forslag.
- Ikke noe som sender beskjed. Ingen SMS, ingen e-post. Den som får bord fra ventelisten, får ikke vite det av seg selv.
- Ikke en kø. Ventelisten er en liste huset ser. Et bord som blir ledig, holdes ikke av til den som står først.
- Ikke betaling: ingen kortgaranti, intet forskudd.
- Ikke et gjesteregister, og ikke navn på en bestilling. Det følger av punkt 5 fra 2. september; se spørsmål 2 i §6.
- Ikke Reserve with Google, bordkart, flere lokaler eller synkronisering med GastroPlanner.
- Ikke satt ut, og ikke pushet. Linux-bygget i CI er ikke kjørt for grenen.

Kapabiliteter og avhengigheter oppgaven bygger på (hver med kilde og hva den ikke dekker):
| Kapabilitet | Kilde (fil) | Avgrensning | Må virke før test? |
|---|---|---|---|
| PalazzoScaffold bygger og testene er grønne på utgangspunktet `31ce1ae7` | Målt i eget arbeidstre 6. oktober kl. 23:31 UTC: 281 tester, 0 feil (`TESTRESULT.md#baseline`) | Mac, ikke Linux | Ja. Målt før første endring |
| En celle slipper andre enn eieren til på navngitte nøkkelstier (`validateCellSpecificAccess`) | `CellProtocol/Sources/CellBase/Cells/GeneralCell/GeneralCell.swift` på pinnen `81601a6f` | Avgjør bare om spørsmålet slipper fram. Hvem som eier en bestilling, avgjør reglene | Ja. Dekket av `test.cell.auth-negative` |
| Husets ansattliste (`house.staff`) | `PalazzoScaffold/Sources/App/Cells/PalazzoHouseCell.swift` | Listen settes av huset. Den sier ikke hvem som er på vakt | Ja. Brukes i testene |
| Gjestens entitet tar imot en post av slaget `booking` fra gjesten selv | `PalazzoScaffold/Sources/App/Cells/PalazzoEntityCell.swift` | Poster kan bare legges til. En avbestilt bestilling står derfor fortsatt som kommende i gjestens egen entitet | Ja |
| Registeret vet hvilken entitetscelle en identitet eier | `PalazzoScaffold/Sources/App/Cells/PalazzoAccessContractCell.swift`, `directoryCellUUID` | Bare for den som har brukt entiteten sin her | Ja |
| Husets regneark tar imot rader fra en celle huset eier | `PalazzoScaffold/Sources/App/Cells/PalazzoSheetCell.swift`, `replaceSheet` | Hele arket skrives på nytt ved hver endring | Ja |
| Husets logg tar imot en linje om en gjest | `PalazzoScaffold/Sources/App/Cells/PalazzoHouseCell.swift`, `house.ledger.append` | Bare huset kan skrive | Ja |

## 3. Forventningskontrakt — «Det du kommer til å se»

Én rad per leveranse. Dette er det eneste som teller som fremdrift etter G2.
**GUI-oppgave:** hver flate og hver viktig tilstand (tom, fylt, feil) må ha et rendret bilde i `images/` som Kjetil har godkjent før G1-GUI. Porthole-preview av skeleton-JSON når formatet tillater det; ellers mockup med eksplisitt liste over hva dagens skeleton ikke kan rendre.
| Leveranse | Type (bilde / fil / testutdata / kjørende flate) | Hvor | Referanse (images/…-v1.png osv.) | Godkjent |
|---|---|---|---|---|
| Koden for celle, regler og ruter, på en egen gren | fil (git-gren på Mac-en, ikke pushet) | Arbeidstreet `_worktrees/palazzoscaffold-bordbestilling`, grenen `losen/palazzo-bordbestilling-20261007`, commits `7976bb15c8ce525f343103e98ebbb2f82be48568` og `7eb404f1f8e3baf16e93f8a1b1447ed1c6f3b508` (rettinger etter kontrollen) | — | nei |
| Testene: reglene og rutene, grønne. 29 av de 47 nye er vist røde med vilje; 18 er ikke det | testutdata | `TESTRESULT.md` | — | nei |
| Beskrivelsen av rutene, hvem som når hva og hva som lagres hvor | fil | `PalazzoScaffold/docs/Bordbestilling_2026-10-07.md` på grenen; kopi i `HAVEN-Deploy/_handoff/HD-0077/bordbestilling/kilde/docs/Bordbestilling_2026-10-07.md` | — | nei |
| Hvor bestillingen ligger: hos huset, hos gjesten, og hva kelneren ser | bilde (tegning av det som er bygget) | `images/` | `images/tillegg-hvor-ligger-hva-v1.png` | nei |
| Husets bordbok: dagen | bilde (forslag, ikke bygget) | `images/` | `images/husflate-bordbok-dagen-v1.png` | nei |
| Gjesten bestiller bord | bilde (forslag, ikke bygget) | `images/` | `images/gjesteflate-bestill-bord-v1.png` | nei |
| Kelnerflatens «Bookinger» teller husets egne bestillinger | kjørende flate. Ikke satt ut, så det finnes ikke noe å se på nett ennå | Testen `testWaiterSeesOwnBookingsAndFindsTheGuestFromTheReference` leser de samme tallene flaten viser | — | nei |

## 4. Tilknyttede formålspakker og lærdommer (auto fra purpose_dev.py lookup)

## Formålspakker som festes
- **pkg.std.everything-works** — Alt skal virke (standard kvalitetsport)
    - purpose://quality.build-and-regression: Alle berørte mål bygger og eksisterende tester passerer uten at tester er fjernet eller svekket.
        - test test.build [command]: Bygg alle berørte mål. → TESTRESULT.md#build
        - test test.regression [command]: Kjør hele eksisterende testmengde. → TESTRESULT.md#regression
    - purpose://quality.docs-in-same-change: Alle dokumenter som beskriver endret oppførsel er oppdatert og datert 'Last verified against code'.
        - test test.docs-updated [inspection]: Hver endret kontrakt/atferd har tilsvarende doc-diff. → ACCEPT.md#docs
    - purpose://quality.work-is-visible: Oppgavemappen har oppdatert STATUS.md med gate-tilstand, og et eventuelt planbytte er datert og begrunnet.
        - test test.status-current [inspection]: STATUS.md speiler faktisk tilstand. → ACCEPT.md#status
    - artefakt FORMAALSSPEC.md (port G1): Godkjent formålsspesifikasjon.
    - artefakt PLAN.md (port G2): Arbeidspakker 1:1 mot bladformål.
    - artefakt TESTRESULT.md (port G3): Utdata fra alle avledede tester.
    - artefakt ACCEPT.md (port G3): Forventning mot faktisk, per leveranse.
    - artefakt STATUS.md (port G3): Gate-tilstand og planbytter.
- **pkg.std.gui-surface** — GUI-flate (bilde før kode)
    - purpose://gui.expectation-agreed-before-build: Et rendret bilde per flate/tilstand er godkjent av Kjetil og lagret som referanse i oppgavemappen.
        - test test.gui.reference-image-exists [artifact]: Godkjent referansebilde finnes for hver flate og hver viktig tilstand (tom, fylt, feil). → images/
    - purpose://gui.parity-with-approved-image: Screenshot av faktisk flate ligger side om side med referansebildet i ACCEPT.md, og alle avvik er enten rettet eller godkjent av Kjetil med begrunnelse.
        - test test.gui.parity [inspection]: Side-om-side referanse/faktisk per flate. → ACCEPT.md#parity
    - purpose://gui.surface-loads-in-time: Flaten er synlig innen terskelen angitt i FORMAALSSPEC.md (standard 5 s) på det avtalte miljøet.
        - test test.gui.load-time [measurement]: Lastetid ≤ terskel, tre forsøk. → TESTRESULT.md#load-time
    - purpose://gui.ways-in-are-reachable: SkeletonReachabilityAudit rapporterer ingen elementer som aldri kan sees, og handlingene FORMAALSSPEC §3 navngir finnes i reachableActionKeypaths.
        - test test.skeleton.no-unreachable-elements [command]: Ingen flate har elementer som aldri kan sees; funn navngir handlingene som gaar tapt. → TESTRESULT.md#reachability
        - test test.skeleton.purpose-actions-reachable [inspection]: Hver handling forventningskontrakten (§3) navngir finnes i flatens reachableActionKeypaths. → ACCEPT.md#ways-in
    - artefakt images/ (port G1-GUI): Godkjente referansebilder, ett per flate og tilstand.
    - artefakt skeleton/ (port G1-GUI): CellConfiguration/skeleton-JSON som bildet er rendret fra. Er bildet en mockup i stedet for Porthole-preview, kreves i stedet en renderingserklæring i images/README.md som lister hva skjelettet ikke kan rendre.
- **pkg.std.cell-contract** — Cellekontrakt
    - purpose://cell.contract-explicit: Book/<celle>_contract_v<n>.json finnes, og en validator kjører grønt på alle fixtures.
        - test test.cell.contract-fixtures [command]: Kjør kontraktvalidator mot positive/negative fixtures. → TESTRESULT.md#contract
    - purpose://cell.authorization-honours-keypath: Negative tester viser at feil requester, feil keypath og purpose://prompt.unknown alle avvises.
        - test test.cell.auth-negative [command]: Feil requester / feil keypath / ukjent formål avvises. → TESTRESULT.md#auth
    - purpose://cell.no-empty-stubs: Ingen endepunkt i kontrakten er implementert som no-op uten status 'not-implemented'.
        - test test.cell.stub-scan [inspection]: Liste alle no-op-handlere og avstem mot Gap_Analysis.md. → ACCEPT.md#stubs
    - artefakt contract/ (port G2): Kontrakt-JSON + fixtures (kan være lenke til Book/).
- **pkg.std.cell-combination** — Cellekombinasjon og dataflyt
    - purpose://cells.dataflow-declared: dataflow.md (eller .graffle/.json) finnes med alle kanter navngitt med endepunkt/event.
        - test test.cells.dataflow-matches-contracts [inspection]: Hver kant i dataflow finnes i en kontrakt. → PLAN.md#dataflow
    - purpose://cells.capabilities-declared-with-boundary: FORMAALSSPEC.md §2 lister hver antatt kapabilitet med kildefil og hva den ikke dekker.
        - test test.cells.capability-audit [inspection]: Alle kapabilitetspåstander har audit-status retrieved. → FORMAALSSPEC.md#audit
    - artefakt dataflow.md (port G2): Diagram + kant-tabell.

## Lærdommer du må lese før dekomponering
- **lesson.text-ux-is-not-design** (2026-05-06, major): Kjetil forventet en helt annen flate enn den som ble vist; den tekstlige UX-beskrivelsen var godkjent, bildet var det ikke.
    - forebygging: Rendret bilde (Porthole-preview eller mockup) godkjennes før implementering; bildet er akseptansereferanse.
- **lesson.parity-was-correctness-not-decoration** (2026-05-06, major): Parity-audit mellom Porthole og Binding viste at problemet ikke var manglende dekorasjon, men produktkorrekthet (feil oppførsel).
    - forebygging: Akseptanse sammenligner både bilde og oppførsel (knapper trigger keypaths, felt tar input) — begge i ACCEPT.md.
- **lesson.surface-load-alias-miss** (2026-08-24, blocker): Flatelasting tok 46 541 ms (klientens 45 s-timeout) ved bom, 5 000 ms ved treff; målingen 10.08 målte en mislykket lasting.
    - forebygging: Mål lastetid tre ganger og sjekk logg for navnebom før en flate erklæres ferdig; aliaser må løses server-side eller ikke brukes.
- **lesson.plan-instead-of-delivery** (2026-08-21, major): Kjetil ba om en leveranse flere ganger og fikk planer/dokumenter om leveransen i stedet.
    - forebygging: G1 godkjenner formål, ikke arbeid; etter G2 telles bare artefakter listet i §3 'Det du kommer til å se' som fremdrift. Et dokument om leveransen teller aldri som leveransen.
- **lesson.undocumented-plan-switch** (2026-08-24, major): Tre produktive døgn (22.–24.08) så tomme ut i alle statusdokumenter fordi planbyttet fra bølge 1–3 til deploy-seremonien aldri ble skrevet ned.
    - forebygging: STATUS.md i oppgavemappen oppdateres ved hvert planbytte med dato og hvorfor; sjekkes i test.status-current.
- **lesson.planned-documented-as-implemented** (2026-08-24, major): Book/05_Flows_Lifecycle.md beskrev sekvensnummer, signatur og replay som ikke finnes i structen.
    - forebygging: Docs-diff i samme endring, med 'Last verified against code'-dato; planlagt oppførsel merkes eksplisitt.
- **lesson.bridge-inferred-architecture-from-one-use** (2026-08-09, major): En kodeassistent sluttet fra én observert bruksmåte av bridge til en egenskap ved arkitekturen og konkluderte feil.
    - forebygging: Erklær hver kapabilitet oppgaven bygger på som eget formål med kilde og Avgrensning (pkg.std.cell-combination).
- **lesson.cellscaffold-two-holes** (2026-09-01, blocker): CellScaffold har tomme booking-/concierge-stubber og autorisasjon som kaster nøkkelstien og bare sjekker eierskap.
    - forebygging: Ikke porter celler fra CellScaffold til PalazzoScaffold uten å lukke begge hullene; test.cell.auth-negative og test.cell.stub-scan må være grønne.
- **lesson.purpose-never-grants-rights** (2026-08-03, blocker): Risiko for at formålsmatch tolkes som tilgang.
    - forebygging: Et formål kan innsnevre en rettighet, aldri opprette, utvide eller arve en; exact match; purpose://prompt.unknown feiler lukket.
- **lesson.corr-approval-surfaces-timed-out** (2026-08-30, major): Corr-godkjenningen (Vegar) er utestet fordi flater/godkjenninger timet ut før testing rakk å skje.
    - forebygging: FORMAALSSPEC.md §2 lister avhengigheter som egne formål med verifier; pkg.std.everything-works og gui.surface-loads-in-time må være grønne før den egentlige testen kjøres.
- **lesson.unresolvable-condition-is-invisible** (2026-09-05, blocker): Relasjoner-flaten viste tittel og ingen vei inn: ingen filopplasting, ingen knapper. Alle tester gronne.
    - forebygging: SkeletonReachabilityAudit kjores over hver flate; test.skeleton.no-unreachable-elements feiler med elementene som aldri kan sees og handlingene som gaar tapt med dem. Betingelser hoerer hjemme inne i List/Grid/Reference-rader, der radens verdi sendes videre; ellers skal cellen avgjore og innhold bindes.
- **lesson.test-corpus-is-not-shipped-corpus** (2026-09-05, major): Rot-probe-testen, lastetidstesten og finnbarhetsauditen var gronne i to uker mens Relasjoner-flaten var tom.
    - forebygging: Enhver flate-test skal bygge korpuset fra det som faktisk sendes ut (menykonfigurasjoner + navigasjonsdestinasjoner + verifiseringshjelperen), dedupliseres, og feile hvis korpuset er mindre enn appens egen meny.
- **lesson.tested-a-different-path-than-production** (2026-09-05, major): Rot-probene leste relations.state.* gjennom porthole.get og var gronne, mens rendereren aldri fikk de samme dataene.
    - forebygging: Naar en test skal si noe om hva brukeren ser, maa den bruke produksjonens egen kodevei - helst produksjonens egen funksjon med produksjonens egne inndata (SkeletonReachabilityAudit kaller condition.evaluate(root: nil, ...) nettopp derfor).
- **lesson.findability-is-not-usability** (2026-09-05, major): Flatene ble kalt validert fordi de bestod en beskrivelsesaudit; de var samtidig ubrukelige.
    - forebygging: En formaalssjekk maa navngi handlingene eieren skal kunne utfore, og testes mot SkeletonReachabilityAudit.reachableActionKeypaths - ikke mot hvor godt formaalet er formulert.
- **lesson.paste-command-instead-of-queue** (2026-09-07, major): Kjetil fikk et innlimingsskript for å starte Codex; flagget --full-auto finnes ikke på `codex exec`, og kjøringen feilet ved første linje.
    - forebygging: Før enhver Codex-kjøring fra Cowork: `ls HAVEN/_losen-queue/inbox running; tail logs/runner.log`, legg jobben som <id>.job + <id>.prompt.md. Aldri gi Kjetil kommandoer å lime inn. Gyldige `codex exec`-flagg: --sandbox, --skip-git-repo-check, -C.
- **lesson.baseline-count-from-report-not-run** (2026-09-07, minor): PLAN.md sa «48 tester grønne»; baseline-kjøringen viste 68 tester med 3 røde.
    - forebygging: WP0/S0 baseline er alltid en ekte kjøring før endring; PLAN oppgir testtall som «forventet ≈ N (fra <kilde, dato>)», og et rødt baseline stopper ikke arbeidet men registreres som eget avvik med årsak.
- **lesson.codex-sandbox-cannot-reach-docker** (2026-09-07, major): S10 (docker compose build/up) endte i `permission denied … docker.sock` i Codex-sandkassen; deploy-slicen ble blocked.
    - forebygging: Deploy-/image-steg planlegges aldri som Codex-slice; de registreres som HAVEN-Deploy-post med eier Kjetil (eller en dispatcher-adapter med eksplisitt docker-rettighet når arbeidskø-PDD-en er levert). Se HD-0012.
- **lesson.scaffold-without-porthole-host-has-no-preview** (2026-09-07, minor): G1-GUI måtte bruke mockups rendret fra skeleton-JSON; ekte Porthole-preview var umulig.
    - forebygging: For scaffolds uten Porthole-vert: (1) images/README.md må si eksplisitt at bildene er mockups og hva skeleton ikke kan rendre, (2) paritet (test.gui.parity) planlegges som egen slice med kjørende scaffold + Binding/Porthole via bridge, ikke som del av implementeringsjobben.
- **lesson.codex-workspace-write-cannot-build-cellscaffold** (2026-09-09, major): WP0-baselinen i køen ble blocked: `sandbox-exec: sandbox_apply: Operation not permitted`. Testkommandoen brukte 1 604 sekunder uten at én eneste test startet.
    - forebygging: Lange bygg og testkjøringer legges ikke som `workspace-write`-køjobb. De kjøres som detached skript startet via Codex med `danger-full-access` og python Popen(start_new_session=True), med logg i en montert mappe som Cowork kan polle — samme mønster som produserte den notariserte HavenAgentD-pakken 2026-09-08. Køjobber brukes til analyse, kontrakter, dokumentasjon og korte kommandoer.
- **lesson.baseline-measured-another-pdds-branch** (2026-09-09, major): WP0 målte `pdd/tillitspakke-agentflaate` med 181 skitne oppføringer, ikke et rent utgangspunkt for sin egen PDD. En regresjonsbaseline derfra sier ingenting om hva denne PDD-en endrer.
    - forebygging: WP0 måler en ren eksport av den revisjonen arbeidet skal gå ut fra (`git archive <rev> | tar -x -C <scratch>`), ikke det delte arbeidstreet. Er arbeidstreet opptatt av en annen PDD, er det en planopplysning som hører i STATUS, ikke noe implementeringen skal jobbe rundt.
- **lesson.worktree-created-from-vm-has-unusable-gitdir** (2026-09-09, major): WP1 ble blocked etter ett minutt: `fatal: not a git repository: /sessions/<sesjon>/mnt/CellScaffold/.git/worktrees/_wt-sad-20260909`, exit 128. Branch og HEAD kunne ikke bekreftes.
    - forebygging: Opprett worktrees fra macOS (Codex), ikke fra VM-en. Er det allerede gjort fra VM-en: skriv om begge pekerfilene til macOS-stien og verifiser `branch --show-current` + `rev-parse HEAD` **fra macOS** før noen jobb legges i køen. En jobb skal aldri være første stedet en sti blir prøvd.
- **lesson.cellbase-decodingerror-shadows-swift** (2026-09-09, minor): WP1s nye celle ga 50 kompileringsfeil: `type 'DecodingError' has no member 'dataCorruptedError'` og `cannot infer contextual base in reference to member 'registry'`, alle fra én linje.
    - forebygging: I App-modulen: skriv `Swift.DecodingError` når du vil ha standardbibliotekets. Gjelder generelt for typenavn CellBase også definerer — sjekk med `grep -rn "enum <Navn>" CellProtocol::Sources/CellBase` før du antar at et kjent Foundation-navn er Foundations.
- **lesson.valuetype-equality-false-for-objects** (2026-09-09, major): Fire av sju WP1-tester feilet på `XCTAssertEqual` mellom to `ValueType.object` som hadde identisk innhold. Feilmeldingen viste samme nøkler og verdier på begge sider, i ulik rekkefølge.
    - forebygging: Aldri assert på hele sammensatte `ValueType`-verdier. Sammenlign kanonisk JSON (`JSONEncoder` med `.sortedKeys`) eller pakk ut og sammenlign felt for felt. Skalarer (`.string`, `.integer`, `.bool`, `.null`) sammenlignes trygt. Merk: dette er et funn i CellBase, ikke bare en testregel — App-kildene destrukturerer riktignok før sammenligning, men en fremtidig `==` på hele verdier vil stille behandle like verdier som ulike. Ikke revidert utover App-kildene.
- **lesson.syntax-check-reported-as-delivered** (2026-09-09, major): WP1 ble rapportert som «kode og 7 tester levert, syntakssjekken bestod». Et faktisk bygg ga 50 kompileringsfeil, og testene feilet 4 av 7 da de først kunne kjøre.
    - forebygging: En implementeringsslice er ikke levert før et detached bygg med `danger-full-access` er kjørt mot arbeidstreet og både bygg og de nye testene er grønne. Legg byggejobben klar FØR slicen kjøres, og skriv i prompten at slicen skal rapportere «skrevet, ikke verifisert» — ikke «levert».
- **lesson.cellbase-internal-members-look-public** (2026-09-09, minor): WP2 stoppet på `'fullPermissionString' is inaccessible due to 'internal' protection level`. Medlemmet finnes og brukes i CellBase selv, så det så ut som et gyldig API.
    - forebygging: Sjekk tilgangsnivå og faktisk returverdi før du bruker et CellBase-medlem fra App: `grep -n "var <navn>" CellProtocol::Sources/CellBase/...`. Et medlem som brukes internt i CellBase er ikke automatisk en del av API-et, og navnelikhet betyr ikke verdilikhet.
- **lesson.entityanchor-keypaths-are-registered** (2026-09-09, minor): WP2-testen skrev en sentinel til `profile` på abonnentens EntityAnchor og fikk `notFound` ved gjenlesing. Skrivingen ga ingen feil.
    - forebygging: Skriv aldri testdata til en oppdiktet keypath på en celle. Finn en keypath cellen faktisk registrerer, helst en annen test som allerede bruker den. At et `set` går gjennom er ikke bevis på at keypathen finnes.
- **lesson.new-cell-must-declare-its-provisioning-mode** (2026-09-09, major): To nye celler i CellScaffold ga tre nye regresjoner: `OrchestratorPersistenceTests testRequireExistingModeRejectsFreshStorageWithoutCreatingBootstrapCells` (opprettet en celle i require-existing-modus mot fersk lagring) og to `TopUpCheckoutTests` som teller celler i provision-only-modus (5 mot forventet 4).
    - forebygging: Enhver ny persistert celle i CellScaffold må eksplisitt svare på tre spørsmål før den registreres: (1) skal den opprettes i require-existing mot fersk lagring? Nei, med mindre den er kanonisk bootstrap. (2) Er den en av de kanoniske eager-bootstrap-cellene som provision-only skal lage? Nesten alltid nei — TopUpCheckoutTests teller dem eksplisitt. (3) Er den en Porthole-publisert flate? Bare da hører den i `reconcilePortholePublishedCellResolves`. Scaffold-intern tilstand registreres i egen funksjon, gated på policy OG provisionOnly, med gjenkjenning av eksisterende mapping.
- **lesson.branch-is-empty-after-eight-work-packages** (2026-09-09, major): Åtte arbeidspakker rapportert utført og verifisert, ACCEPT.md skrevet — men `git branch -v` viste at `pdd/scaffold-admin-delegering` fortsatt pekte på samme commit som `main` (`e1f3e22f`). All koden lå ucommittet i et worktree som bare finnes på én maskin. Ett tapt worktree = 2 750 linjer kode og test borte, med full dokumentasjon på at arbeidet var «levert».
    - forebygging: Skill «filene finnes» fra «branchen har dem». Sjekk `git rev-parse <branch>` mot `git rev-parse <base>` som del av hver verifikasjon som påstår at noe ligger på en branch; er de like, er branchen tom. Legg en commit-pakke inn i planen etter første grønne bygg, ikke etter siste arbeidspakke. Når worktreet bare kan leses fra macOS, kjør sjekken der — ikke hopp over den fordi verktøyet svarer feil.
- **lesson.ciphertext-field-held-plaintext-hash** (2026-09-10, blocker): Losen fortalte Kjetil at lyd allerede var kryptert i lagring. Det var feil: filene i prod begynner med ID3 og er vanlig MP3. To ting forte dit. (1) Krypteringskoden som ble lest tilhorer MusicIngestCell paa /mvp/ingest/local, mens Butterpop publiserer gjennom MusicAssetStoreCell.storeLocalAsset, som skriver bytene slik de kommer. (2) storeLocalAsset setter ciphertextSHA256 = plaintextSHA256 = sha256(data), saa manifestet ser kryptert ut selv naar encryptionPolicy er none.
    - forebygging: En paastand om at noe er kryptert, signert eller verifisert skal bekreftes paa artefaktet - les bytene, ikke feltet. Et felt som heter ciphertext* skal ikke settes naar encryptionPolicy er none; enten utelates det, eller navnet sier hva det er. Kan bli derivedTest: manifest med encryptionPolicy none har ingen ciphertext-verdi.
- **lesson.local-main-is-not-main** (2026-09-11, major): WP0-baselinen var rød og ble meldt som «main bygger ikke». Det var feil. Den commiten baselinen ble målt mot, `ba14895`, lå bare på den LOKALE main-grenen og var aldri pushet; den avhang av CellBase-kode som heller ikke var pushet. origin/main lå fire commits lenger fram, pinnet CellProtocol til en revisjon som ER på CellProtocol sin main, og hadde grønn CI hele tiden. Et helt døgns arbeid ble bygget oppå den lokale commiten.
    - forebygging: Før du måler en baseline eller sier at main er rød: `git fetch origin main` og sammenlign. Er lokal main foran origin/main, er de commitene ikke main for andre — bygg aldri videre på dem. Se på CI for origin/main før du konkluderer. `swift package edit` skal aldri være på når noe måles eller meldes verifisert. Og den eneste sjekken som virkelig avgjør: klon fra GitHub til en tom katalog og bygg der. HavenAgentD::Scripts/preflight_before_landing.sh stiller alle fire spørsmålene.
- **lesson.a-new-red-test-needs-a-repeated-baseline** (2026-09-10, minor): Første fulle kjøring med nye endringer viste to røde i stedet for baselinens én, og den nye lå i en fil jeg hadde endret. Det så ut som en regresjon jeg hadde innført.
    - forebygging: Når en ny rød dukker opp: kjør basen på nytt, i et eget rent worktree, **flere ganger** (tre holder som regel), før du enten tar på deg feilen eller avfeier den. Skriv resultatet av gjentakelsen i TESTRESULT — «2 av 3 på ren base» er et svar, «den er nok flaky» er ikke. Det koster ti minutter og avgjør om du bruker natten på å jage din egen feil eller andres.
- **lesson.swift-test-exit-code-lies-in-havenagentd** (2026-09-10, minor): `swift test` i HavenAgentD avslutter med 1 selv når samtlige 212 tester passerer. Et skript som leser `$?` melder rødt på et helt grønt tre.
    - forebygging: Les resultatet fra linjen `Test run with N tests in M suites passed/failed`, ikke fra exitkoden, i alle skript og køjobber for dette repoet. Og fjern det tomme XCTest-målet, eller bygg det for riktig arkitektur, før noen setter opp CI her — ellers vil CI være rød uansett hva som gjøres.
- **lesson.pin-must-be-on-their-main** (2026-09-11, major): En revisjonspin i Package.swift pekte på en CellProtocol-revisjon som ikke lå på CellProtocol sin main. Koden bygde bare på den ene maskinen som hadde revisjonen liggende lokalt.
    - forebygging: Å pinne er riktig — det er det som gjør bygget reproduserbart. Kravet er at revisjonen er en forfar av avhengighetens egen main. Da er «bygg fra andres main» og «reproduserbart bygg» samme krav. HavenAgentD::Scripts/assert_dependencies_are_on_their_main.sh håndhever det, og CI kjører den. Lander du en klient før cellen den bruker er på den andres main, har du laget et repo som bare bygger hos deg.
- **lesson.a-red-baseline-is-a-question-not-an-answer** (2026-09-11, major): En rød baseline ble behandlet som en opplysning om prosjektet, og arbeidet gikk videre med et tiltak som gjorde den grønn. Tiltaket skjulte årsaken i stedet for å fjerne den.
    - forebygging: Svar på tre spørsmål før du gjør noe med en rød baseline: er utsjekket mitt likt origin? er CI grønn på origin/main? hvilken commit gjorde den rød, og hvem eier den? Først når svaret er «prosjektet er faktisk rødt» er det riktig å jobbe rundt det — og da som en egen, navngitt sak, ikke som en stille lokal omgåelse.
- **lesson.a-conditional-artifact-must-still-cost-something** (2026-09-18, minor): purpose_dev.py validate ble rød på PDD_entitetsdata-egen-kontroll fordi artefaktet 'skeleton/' manglet, selv om G1-GUI var godkjent på bilder Kjetil faktisk hadde sett. Pakken beskrev artefaktet som påkrevd «når Porthole-preview er brukt»; validatoren krevde det alltid.
    - forebygging: Et betinget krav oppfylles av et *annet krav*, aldri av et fravær. Feltet 'satisfiedByDeclaration' peker på en fil og en overskrift og krever minst ett punkt under den: enten viser du skjelett-JSON-en bildet er rendret fra, eller du skriver ned hva skjelettet ikke kan rendre. Begge tvinger frem spørsmålet «kan flaten dette?». Feilmeldingen navngir begge veier ut. Sjekket begge veier: rød uten erklæring, grønn med.
- **lesson.location-is-not-ownership** (2026-09-22, major): dataflow.md begrunnet at AIGateway matte ligge i appen med at «en gateway utenfor entiteten gjor prompten til noen andres data». Kjetil: en celle i skyen som eies av meg er pr definisjon innenfor min entitet.
    - forebygging: Regelen er uniform og gjelder alle scaffolds likt: ingen andre, scaffold-admin inkludert, nar data ELLER funksjonalitet i en celle jeg eier uten en Agreement som sier det. Et vern som bare gjelder skyen er et tegn pa at grensen er tegnet feil. Negative tester skal kjores i begge oppsett, lokalt og sky, og gi samme svar — og de skal dekke handlinger, ikke bare felter. Den positive motsatsen ma ogsa testes: en Agreement apner nayktig sitt eget omfang.
- **lesson.read-origin-main-before-writing-a-mechanism** (2026-09-22, major): Runde 1 av PDD_entitetsdata skrev en egen resolver for lenkede identiteter (EntityLinkAuthorizer, ny CellAuthorizationPath.linkedIdentity, ny hook pa GeneralCell). Da patchen ble lagt mot origin/main viste det seg at IdentityLinkRegistry og GeneralCell.authorizationEvidence allerede gjorde det samme, landet av en annen oppgave (purpose://candidate.entity-link.resolver-honours-link). Hele resolveren ble forkastet.
    - forebygging: Brief-audit skal si HVILKEN revisjon noe ble lest fra, og for et formal som skal endre en mekanisme skal kilden vaere origin/main (git show origin/main:<fil>), ikke utsjekket. Preflight-skriptet sjekker na at patchen passer mot origin/main i et eget worktree for noe legges pa. Og: for du skriver en mekanisme, grep pa main etter navnet pa det den skal gjore (her: sameEntity, linkedIdentity) - ikke bare etter typen du planlegger a lage.
- **lesson.method-lived-only-on-one-machine** (2026-09-24, major): Metoden selv — Book 35 (PDD-arbeidsflyten), Book 36, lærdomsregisteret med 50 lærdommer, formålspakkene, purpose_dev.py — lå bare i ett utsjekk på Kjetils Mac på grenen codex/docs-cleanup-20260810, aldri på main; derfor verken i HAVEN eller hos andre utviklere.
    - forebygging: Metodeartefakter landes som kode: PR til main og pin-oppdatering i HAVEN. Test: git cat-file -e origin/main:<fil> for hver metodefil.
- **lesson.downstream-pin-must-come-from-the-consumer** (2026-09-24, major): Nedstrøms-baselinen for CellScaffold var rød 22.09 («cellprotocol krever swift-crypto 4.5.2, dimymint krever 3.x») og ble rapportert som prosjektets blokkering. CellScaffold main pinnet DiMyMint af41630, som løser swift-crypto 4.x; skriptet hadde hardkodet en eldre revisjon (1718fda).
    - forebygging: Et nedstrøms-skript leser alle transitive pinner fra forbrukerens egen Package.swift/Package.resolved på origin/main ved kjøring, og logger dem. En rød avhengighetsoppløsning i et skript med hardkodede pinner er ikke et funn før pinnene er bekreftet mot forbrukerens resolved.
- **lesson.disposable-worktree-must-be-reset-before-checkout** (2026-09-24, minor): pdd-check/Binding ble stående på 72f6a6c9 i to kjøringer selv om skriptet ba om origin/main: «Your local changes to project.pbxproj would be overwritten by checkout». Baselinen målte feil Binding-revisjon uten å si fra.
    - forebygging: Engangs-worktrees resettes hardt (`git reset --hard` + fjern Package.resolved) før hver utsjekk, og skriptet skriver ut revisjonen den faktisk står på — en avvikende revisjon skal stoppe kjøringen, ikke logges forbi.
- **lesson.report-the-commit-you-pushed-not-the-one-you-planned** (2026-09-24, minor): TESTRESULT og PLAN sa «commit ebb0b7f». Branchen sto på e66b7f1 — commit.sh hadde laget en ny hash — og var ikke pushet. Push-skriptets EXPECT måtte rettes før det kunne kjøre.
    - forebygging: Etter hver commit/push: les `git rev-parse --short HEAD` og `git ls-remote --heads origin <branch>` og lim inn utdataene i STATUS/TESTRESULT. Sjekk også for remote-tracking ref før du sier «pushet» (lesson.branch-is-empty-after-eight-work-packages, samme familie).
- **lesson.lookup-again-when-a-surface-is-added** (2026-09-24, major): De nye seksjonene i «Utvid entiteten» (B10) var portet på synlighet med rot-scope, og listen med verktøyets forespørsel forsvant — samme feil som lesson.unresolvable-condition-is-invisible fra 05.09.
    - forebygging: For hver ny eller endret skjelettflate: kjør `purpose_dev.py lookup --tags skeleton gui` før utformingen, og `BindingTests/CellConfigurationVerifierXCTest/testNoLocalSurfaceHidesItsOwnWaysIn` + `testPersonalCopilotLocalSurfacesLoadWithoutReferenceFailures` før flaten vises eller committes.
- **lesson.picker-state-keypath-is-read-and-written** (2026-09-24, minor): Velgeren «Verktøy» i «Gi tilgang» sto på «Velg verktøy» selv om cellen hadde valgt verktøyet.
    - forebygging: `selectionStateKeypath` skal være en nøkkel cellen både leser (`{selected}`) og skriver; test rundturen (`pickerSelectionRoundTrips`).
- **lesson.pairing-can-outlive-the-identity** (2026-09-24, major): Agenten var paret med en HAVEN-identitet fra 4. mai («Binding Local Session», nøkkel 13BF…), mens HAVEN brukte en annen privat identitet (D362…, identitetsfilen skrevet 18.09). Svar fra HAVEN ville blitt avvist; ingen test i noen av endene kunne se det.
    - forebygging: En flate som ber eieren signere for agenten sammenligner egen nøkkel med agentens forankring og viser forskjellen før signering, med vei til ny paring (test: `offerIsRefusedHereWhenThisHavenHoldsAnotherKey`, `theOwnerNeverSignsWhatFailedTheCheck`). Sjekk nøkkelkontinuitet før live-test av noe som signeres.
- **lesson.screencapture-from-runner-can-fail** (2026-09-24, minor): `screencapture -l <vindu>` fra jobbløperen ga «could not create image from window» for HAVEN-vinduet, med samme vindus-ID som computer use så.
    - forebygging: Ta bilder av flater med computer use (eller be Kjetil), og ikke planlegg bevis som avhenger av `screencapture` fra løperen før det er målt at det virker den dagen.
- **lesson.sketch-assumed-a-renderer-it-did-not-have** (2026-09-25, major): Skissen v2 (HTML) var venstrestilt, men «Utvid entiteten» i HAVEN viste all tekst sentrert, også etter at hAlignment «leading» var satt.
    - forebygging: Før en skisse godkjennes: finn CellProtocol-committen HAVEN-bygget bruker, les hvordan Text/VStack/HStack rendres der, og list i §3 hva den ikke kan (her: venstrestilt tekst). Et HTML-bilde er ikke bevis for at rendreren kan det samme.
- **lesson.maxwidthinfinity-also-stretches-height** (2026-09-25, minor): En tekst i en listerad ble kuttet med «…» etter fem linjer når en HStack med wrap og maxWidthInfinity sto i samme rad; uten maxWidthInfinity ble teksten hel.
    - forebygging: Ikke sett maxWidthInfinity på elementer i listerader. Se etter «…» i skjermbildet av hver rad med lang tekst, i et smalt vindu.
- **lesson.wrap-gives-each-item-its-ideal-width** (2026-09-25, minor): Knappen «Par agenten med denne HAVEN-en» gikk ut over kortet og ble klippet i et smalt vindu.
    - forebygging: Knapper i vanlig HStack, som kan krympe og bryte teksten; wrap bare for korte merkelapper. Se på flaten i et smalt vindu før den vises fram.
- **lesson.empty-list-keeps-its-slot** (2026-09-25, minor): Tomme lister og tomme tekster ga store hull i «Utvid entiteten».
    - forebygging: Én liste per kort, der cellen bestemmer radene (`kind`) og en rad med en kort linje står der det ellers ville vært tomt. Ingen faste høyder på lister, og ingen tekst på toppnivå som kan bli tom.
- **lesson.pgrep-pattern-must-allow-arguments** (2026-09-25, minor): Byggejobben avsluttet ikke HAVEN, og `open` hentet bare fram det gamle bygget (startet 24.09 17:29) i stedet for å starte det nye.
    - forebygging: Bruk 'HAVEN( |$)' i mønsteret, og skriv ut prosessens starttid etter omstart og sammenlign den med byggetiden før noe vises fram.
- **lesson.computer-use-image-is-not-a-file** (2026-09-25, minor): Skjermbildene av den nye flaten kunne ikke sendes til Kjetil som fil; vinduet var i tillegg på et annet skrivebord og kunne ikke gjøres større i bakgrunnen.
    - forebygging: Planlegg bildebeviset med en vei som gir en fil (Kjetils eget skjermbilde, eller skjermopptakstilgang for løperen), og si det før arbeidet, ikke etter.
- **lesson.text-field-sends-a-string** (2026-09-25, major): Adressefeltet i «Utvid entiteten» kunne aldri starte en forespørsel: Enter ga alltid «Si hvilket scaffold dette gjelder — `audience` …».
    - forebygging: For hvert tekstfelt: en kontraktstest som sender feltets egen payload (.string) til targetKeypath og venter et svar som ikke er feil.
- **lesson.green-gate-must-read-the-last-summary-line** (2026-09-26, major): runde2.sh committet og pushet 399f6d2 med 4 røde tester. Porten grep'et «Executed … with 0 failures» i hele loggen og traff en grønn suites linje lenger opp; siste linje sa «1262 tests, with 2 tests skipped and 8 failures».
    - forebygging: En grønn-port leser bare den siste «Executed»-linjen (tail -1) og krever « 0 failures (0 unexpected)». Sammenligningen gjøres uten pipe (POSIX case), fordi `echo | grep -q` under pipefail kan gi rødt på grønt (SIGPIPE). Porten skriver ut nøyaktig hva den sammenlignet.
- **lesson.module-and-type-share-a-name-in-cellprotocol** (2026-09-26, minor): `CellApple.EntityAnchorCell` og `CellVapor.EntityAnchorCell` kompilerte ikke: «type 'CellApple' has no member 'EntityAnchorCell'». Begge modulene har en type med samme navn som modulen.
    - forebygging: Én fil per modul som importerer bare den ene og gir typen et unikt typealias (TestSupport/AppleEntityAnchorAlias.swift, VaporEntityAnchorAlias.swift). Testfilen importerer ingen av modulene direkte.
- **lesson.placeholder-example-leaks-into-judgement** (2026-09-28, minor): I «Dommerbenken — chat» v2 var plassholderen i fritekstfeltet «f.eks. «status på prosjektet»». Kjetil skrev nøyaktig «status på prosjektet» som sin egen tolkning i to av tretti saker («hvor står vi nå på prosjektet», «hva står igjen»). Eksempelet var hentet fra meningen til en sak i settet.
    - forebygging: Eksempler, plassholdere og hjelpetekst i en dommerflate skal hentes fra et domene som ikke finnes i settet, og testes: ingen sak i settet skal ha gold hvis tittel eller alias overlapper eksempelteksten. Rapporter saker der dommerens fritekst er lik eksempelet som svakere.
- **lesson.host-mutation-without-reading-the-coordination-file** (2026-10-02, major): 30.09 satte en Claude-tråd ut en gren-commit på staging og byttet invitasjonene, med Kjetils ja, men uten claim. En Codex-tråd hadde claim på samme container (HD-0141), staging var reservert for 2026.9.4, og deploykøen trodde i to døgn at staging kjørte forrige utgivelse.
    - forebygging: Før enhver vertsmutasjon: les `_losen-queue/KOORDINERING.md`, kjør `hd coord status`, ta egen claim på en HD-oppgave, og før utsettingen inn i køen etterpå. Test: jobbloggen for utsettingen viser `hd coord status` uten annen claim på samme tjeneste, og egen claim, før første kommando mot verten. Eierens ja til å sette ut erstatter ikke sjekken.
- **lesson.remembered-install-state-is-not-measured** (2026-10-02, minor): En plan sa at agenten på Macen var bygget fra en bestemt gren, og bygde grenvalg og et åpent spørsmål til eieren på det. Agenten var installert på nytt fra `main` av en annen tråd seks dager tidligere.
    - forebygging: Hva som er installert, måles før en plan bygger på det: dato og navn på binærene og sikkerhetskopiene i `bin/`, `launchctl print`, og om commiten er på `origin/main`. Test: påstandstabellen merker installasjonstilstand som hentet med måletidspunkt, aldri som husket.
- **lesson.vocabulary-guard-admits-new-claims** (2026-10-03, major): En vakt som godtok enhver setning bygd av tillatte ord, også i bøyd form, slapp 38 av 45 angrepsomskrivinger gjennom («Det har vi:», «Dette er menyen vår:», «Du har rett:»).
    - forebygging: Det en vakt publiserer i en modells navn, er en tekst vakten selv kan bygge av lukkede lister med hele setninger; modellens tekst velger bare hvilken. Test: et sett omskrivinger skrevet av en som ikke har skrevet reglene, gir null publiserte tekster utenfor den mengden.
- **lesson.guard-must-see-the-question-the-model-does-not** (2026-10-03, major): «Vi har følgende pizzaer: …» etter spørsmålet «Hvilke pizzaer har dere uten kjøtt?» leses som fem pizzaer uten kjøtt; to av dem har salami.
    - forebygging: For hver svartype som kan omformuleres, finnes en lukket liste med hele spørsmål; alt annet gir det godkjente svaret ordrett. Et ord som tas ut av svaret, tas også ut av spørsmålene. Test: hvert spørsmål utenfor listen gir null kall til modellen.
- **lesson.own-committed-tests-changed-without-asking** (2026-10-03, major): Ti tester tråden selv hadde committet tidligere samme dag, ble endret uten å spørre: tretten endringer, og sju av dem snudde eller fjernet noe en test krevde godtatt.
    - forebygging: En committet test er eksisterende, uansett hvem som skrev den og når. Før hver commit leses testendringene rett fra git; en endring i en committet test er et spørsmål til eieren. Test: skriptet som lister testendringer fra git, viser ingen endring i en committet test uten en godkjenning ført i STATUS.md.
- **lesson.accept-written-from-memory-had-27-errors** (2026-10-03, major): Første utkast til ACCEPT.md og TESTRESULT.md hadde 27 feil da en uavhengig tråd holdt det mot bevisfilene; ett av dem var påstanden om at hver frosset utgave ble angrepet etter at den var satt ut.
    - forebygging: Tall, klokkeslett, commit-numre og sitater i ACCEPT.md og TESTRESULT.md fylles inn fra bevisfilene av kode, og en uavhengig tråd holder hver påstand mot bevisene før eieren får dokumentene. Test: rapporten fra kontrollen ligger blant bevisene, med en dom per påstand.
- **lesson.red-first-claimed-for-tests-that-were-not** (2026-10-04, minor): TESTRESULT.md sa at hver ny eller endret test var kjørt rød først. Tolv endringer i tester som alt fantes, og ti av de 24 nye i første runde, kom inn sammen med koden og var aldri kjørt røde.
    - forebygging: En påstand om alle tester føres per test: «rød først» listes med hvilke tester som fantes i den røde kjøringen, og hvilke som kom til etterpå. Test: antall tester i den røde og i den grønne kjøringen står i TESTRESULT.md, og differansen er forklart.
- **lesson.estimate-assumed-one-attack-round** (2026-10-04, minor): Planen sa «rundt tre og en halv time etter G1». Den siste utgaven var målt på nett 34 timer og 50 minutter etter.
    - forebygging: Et anslag for arbeid som skal angripes av en uavhengig tråd, oppgis per runde, og sier at antall runder er ukjent til første angrep er målt. Test: planen har tid per runde, ikke en sluttid.
- **lesson.full-path-rule-broken-in-short-references** (2026-10-05, major): Kjetil måtte for tredje gang si at filer skal stå med hele stien («Du må legge med hele banen til filer som dette: ACCEPT.md»): meldingene og spørsmålene ved G3 hadde bare filnavnet.
    - forebygging: Hver melding til eieren kontrolleres maskinelt før den sendes: et ord som ender på en filendelse og ikke begynner med en rot, stopper sendingen. Det gjelder hver gang en fil nevnes, også i spørsmål. Test: skriptet som kontrollerer meldinger, gir null funn på hver melding som ber om en port.
- **lesson.file-copied-to-the-mac-was-the-previous-version** (2026-10-05, major): En commit gikk ut med testen, men uten endringen den prøvde: filkopien fra skyøkten til Macen meldte «written», og fila på Macen var forrige utgave. To skript mistet dessuten kjørbar-biten på veien.
    - forebygging: Hver utgave som skal til Macen, legges under et nytt filnavn i utdatamappen. Sjekksummen på Macen sammenlignes med den i skyen i et eget steg, og neste steg (commit eller køjobb) startes ikke i samme kommando. Test: commit-jobben viser «git diff --cached --stat --summary» før commit, og lista over filer og moduser sammenlignes med det som skulle med.
- **lesson.pr-opened-without-reading-the-base-branch-ci** (2026-10-05, minor): PR #30 ble opprettet uten at CI-tilstanden på main var lest: løpet sto til tidsgrensen på 25 minutter av en grunn som hadde stått på main i seks dager, og den første lesningen av loggen, at det stoppet før PR-ens tester hadde startet, ble felt av den uavhengige kontrollen.
    - forebygging: Før en PR opprettes, listes løpene for basisgrenen; har hodet ikke noe grønt løp med samme testskript, rettes det først, eller rettelsen tas med. Før en årsak skrives ned for et rødt løp, leses avsnittet om CI i skillen, og siste linje i en logg kalles ikke stedet det stoppet. Test: skriptet som oppretter en PR, viser siste løp på basisgrenen og stopper når det er rødt.
- **lesson.status-message-sent-before-the-documents-were-checked** (2026-10-06, minor): Dokumentene og meldingen til eieren 06.10 om kvelden skrev slutninger som målinger («haven-deploy ville blitt kjørt med umask 077», «skallet ventet fem sekunder: målt»), gjenga kontrollenes merknader som «en feil» og «alle rettet», utelot ett av fire svar der en vakt ble beskrevet, og ga et klokkeslett for når en kjøring ville være ferdig, uten grunnlag. Meldingen var sendt et kvarter før kontrollen av dokumentene.
    - forebygging: Dokumenter, LES-MEG ved siden av et skript og meldingen til eieren kontrolleres mot kildene av en som ikke har skrevet dem, før meldingen sendes. Ved hver påstand står det om den er målt, lest eller sluttet, og et tidsanslag gis som et spenn med grunnlaget. Test: kontrollrapporten er eldre enn meldingen, og rettelser gjort etter kontrollen er merket som ukontrollert.
- **lesson.commit-file-built-on-a-stale-copy-and-the-check-got-the-same-copy** (2026-10-06, major): README.md i commiten `c5058f49` fikk 172 endrede linjer (104 ut, 68 inn) der rundt 50 nye var ventet: tekst fra tre tidligere commiter falt ut.
    - forebygging: Hver fil i en commit-pakke bygges på git-objektet i foreldercommiten, og skriptet som committer, krever ventet antall linjer inn og ut per fil og stopper ellers. Kontrolltråden får commiten og finner grunnlaget selv. Test: skriptet stopper når forskjellen mot forelderen ikke er den ventede.
- **lesson.brake-file-written-after-the-chain-had-passed-the-brake** (2026-10-06, minor): Bremsefilen ble lagt 13 sekunder etter at kjedeskriptet hadde passert bremsesjekken foran pushen, så en commit med en kjent feil ble pushet.
    - forebygging: Et tall et menneske må lese før neste steg som ikke kan angres, deler kjeden i to jobber, eller skriptet krever tallet selv. Test: kjeden stopper foran pushen når commitens linjetall avviker fra det ventede.
- **lesson.check-ran-before-the-last-numbers-and-did-not-read-the-message** (2026-10-06, minor): Kontrollen av akseptdokumentet ble gjort før de 27 siste kallene var målt, og meldingen til eieren var ikke med. En ny kontroll rett før sending fant åtte ting, blant annet at meldingen la en svakhet til angrepet alene der råsvarene fra nett viste det samme.
    - forebygging: Den siste uavhengige kontrollen kommer etter at siste tall er ført inn, regner tallene på nytt fra råfilene og leser meldingen eieren får. Test: kontrollrapporten er yngre enn siste bevisfil og eldre enn meldingen.
- **lesson.approved-image-had-no-way-to-be-photographed-on-the-live-page** (2026-10-06, minor): Telefonbildet som ble godkjent ved G1-GUI, kunne ikke få et skjermbilde fra nett ved siden av seg ved G3: nettleserverktøyet holder vinduet på 1280 punkter, og siden nekter å bli vist i en ramme.
    - forebygging: Ved G1-GUI står det for hvert bilde hvordan motstykket på nett skal tas ved G3, og veien er prøvd én gang mot siden slik den står. Kan et bilde ikke tas, sies det ved G1-GUI. Test: hvert godkjent bilde har en navngitt opptaksvei som har gitt en fil.
- **lesson.early-return-rule-changed-what-happens-when-the-lookup-is-down** (2026-10-06, minor): Et spørsmål med et ord fra ordlisten får henvisningen (HTTP 200) også når oppslaget ikke kan nås, der andre spørsmål får 503 eller 403. Det sto verken i spesifikasjonen eller i en test.
    - forebygging: For hver regel som svarer før en avhengighet spørres, sier spesifikasjonen hva som skjer når avhengigheten er nede, og en test holder det fast. Test: en test der avhengigheten er tatt bort, med ventet svar for begge grener.
- **lesson.way-back-was-called-a-way-back-after-dry-runs-only** (2026-10-06, minor): Veien tilbake fra utsettingen er tørrkjørt to ganger, men selve byttet tilbake er aldri kjørt, der spesifikasjonen krever en vei som virker også når siden er nede.
    - forebygging: En vei tilbake er vist når byttet er kjørt, for eksempel mot en egen container med samme image. Ellers står den som «ikke vist» i planen eieren godkjenner. Test: bevis for et gjennomført bytte, eller linjen «ikke vist» i planen.
- **lesson.order-of-steps-changed-to-keep-a-promised-time** (2026-10-06, minor): Utgaven ble satt ut før rettelsen av README.md var committet, mot planen, fordi kontrollen av rettelsen tok 28 minutter der 15 var ventet.
    - forebygging: Planen sier hvilke steg som kan bytte plass når noe tar lengre tid, og kontroller får en hard tidsgrense. Test: hvert planbytte har en linje i STATUS.md med hva som tapes.
- **lesson.correction-to-a-list-removed-words-it-already-caught** (2026-10-06, minor): To rettelser i ordlisten ga nye hull: et unntak som ble sammenlignet etter at ø var brettet til o, tok bort «nøtte», og en innsnevring tok bort «tolererer».
    - forebygging: Hver utgave av en liste kjøres mot alle tidligere eksempler, både ord som skal treffe og ord som ikke skal, og eksemplene ligger som fikstur. Test: en fikstur med ett eksempelord per oppføring og en liste med ord som ikke skal treffe.
- **lesson.rewritten-draft-got-new-errors-where-it-was-rewritten** (2026-10-06, minor): Seks utkast til spesifikasjonen ble lest i fem kontrollrunder som fant 110 ting til sammen. Hver runde fant feil i det som var skrevet om etter den forrige.
    - forebygging: Etter en omskriving kontrolleres det omskrevne på nytt, og eieren får vite når siste utgave ikke er kontrollert. Tall fylles inn av kode. Test: dokumentet sier hvilken utgave kontrollen leste.
- **lesson.known-pitfall-repeated-in-a-small-follow-up-without-lookup** (2026-10-06, minor): Testen for avvik 4 sammenlignet to like svarkonvolutter med `XCTAssertEqual` og var rød mot riktig kode. Den grønne kjøringen fanget det før commit.
    - forebygging: `lookup` kjøres for hvert steg som skriver kode eller tester, også små oppfølginger, og oppgaven til kontrolltråden ber den holde testen mot lærdommene for taggene. Test: commit-trinnet stopper uten grønt bevis for nettopp filene som committes.
- **lesson.full-path-rule-passed-the-checker-in-descriptions-and-file-cards** (2026-10-06, minor): Meldingen som ba om G3, gikk gjennom kontrollskriptet for hele banen, men fem filer ble sendt som kort uten bane i sendingen, og dokumenter ble nevnt med en beskrivelse («akseptdokumentet») før banen sto.
    - forebygging: Hver fil som leveres i samtalen, står med hele banen i meldingen som følger med, og en beskrivelse av en fil får banen ved første nevning. Test: antall leverte filer er lik antall baner i meldingen.

## Book 23-noder som kan være forelder/gjenbruk (leksikalsk forslag, verifiser)
- purpose://contact.communication [draft] — Contact and communication
- purpose://event.participation [draft] — Event participation
- purpose://event.privacy-preserving-networking [draft] — Privacy-preserving event networking
- purpose://skeleton.owner-entity-access [draft] — Owner entity access affordance
- purpose://governance [active] — Governance
- purpose://access.audit.privacy [active] — Access, audit and privacy
- purpose://questionnaire.access.audit [active] — Questionnaire access audit
- purpose://access.audit.privacy.database-key-custody [candidate] — Eierstyrt kryptering og nøkkellagring for celledata

## 5. Avledede tester (samlet)

| testRef | Formål | Hvordan | Evidens | Status |
|---|---|---|---|---|
| test.build | purpose://quality.build-and-regression | Prosjektets byggkommando (xcodebuild / swift build / pytest) — angis i PLAN.md. | TESTRESULT.md#build | venter |
| test.regression | purpose://quality.build-and-regression | Prosjektets testkommando; sammenlign antall tester før/etter. | TESTRESULT.md#regression | venter |
| test.docs-updated | purpose://quality.docs-in-same-change | Les diff; kryss av i ACCEPT.md. | ACCEPT.md#docs | venter |
| test.status-current | purpose://quality.work-is-visible | Sammenlign STATUS.md med filene i mappen. | ACCEPT.md#status | venter |
| test.gui.reference-image-exists | purpose://gui.expectation-agreed-before-build | purpose_dev.py validate sjekker images/ mot FORMAALSSPEC.md §3. | images/ | venter |
| test.gui.parity | purpose://gui.parity-with-approved-image | Screenshot fra Porthole/Binding i samme viewport som referansen; lim inn i ACCEPT.md. | ACCEPT.md#parity | venter |
| test.gui.load-time | purpose://gui.surface-loads-in-time | Stoppeklokke/logg-tidsstempel; noter alle tre tider. | TESTRESULT.md#load-time | venter |
| test.skeleton.no-unreachable-elements | purpose://gui.ways-in-are-reachable | xcodebuild -only-testing:BindingTests/CellConfigurationVerifierXCTest/testNoLocalSurfaceHidesItsOwnWaysIn | TESTRESULT.md#reachability | venter |
| test.skeleton.purpose-actions-reachable | purpose://gui.ways-in-are-reachable | Sammenlign §3-radene mot SkeletonReachabilityAudit.reachableActionKeypaths(skeleton). | ACCEPT.md#ways-in | venter |
| test.cell.contract-fixtures | purpose://cell.contract-explicit | python3 checks/validate_contract.py | TESTRESULT.md#contract | venter |
| test.cell.auth-negative | purpose://cell.authorization-honours-keypath | Tre enhetstester navngitt etter tilfellet. | TESTRESULT.md#auth | venter |
| test.cell.stub-scan | purpose://cell.no-empty-stubs | Søk i berørte filer; skriv listen i ACCEPT.md. | ACCEPT.md#stubs | venter |
| test.cells.dataflow-matches-contracts | purpose://cells.dataflow-declared | Tabell kant→kontrakt i PLAN.md. | PLAN.md#dataflow | venter |
| test.cells.capability-audit | purpose://cells.capabilities-declared-with-boundary | Tabell i FORMAALSSPEC.md §0. | FORMAALSSPEC.md#audit | gjort |
| test.b1.plan-problems | B1 | `PalazzoTableBookingEngineTests.testPlanProblemsAreNamedOneByOne`: en plan med 16 feil gir 16 navngitte problemer; en gyldig plan gir ingen | TESTRESULT.md#regler | grønn; ikke vist rød |
| test.b1.plan-route | B1 | `PalazzoBookingCellTests.testHouseSetsThePlanAndABrokenPlanIsRefusedWithEveryProblem`: en plan med feil gir 400 og listen; den gyldige planen står | TESTRESULT.md#ruter | grønn; ikke vist rød |
| test.b1.held-table | B1 | `PalazzoBookingCellTests.testPlanCannotRemoveATableSomeoneHolds` | TESTRESULT.md#ruter | grønn; ikke vist rød |
| test.b1.area | B1 | `PalazzoTableBookingEngineTests.testClosingAnAreaTakesItsTablesOutOfAvailability` og `PalazzoBookingCellTests.testAnAreaCanBeClosedAndOpenedAgain` | TESTRESULT.md#regler, #ruter | grønn; ikke vist rød |
| test.b2.start-times | B2 | `testStartTimesFollowTheSeatingAndTheWeekday` | TESTRESULT.md#regler | grønn; ikke vist rød |
| test.b2.caps | B2 | `testCapsPerStartApplyToGuestsAndNotToTheHouse` | TESTRESULT.md#regler | grønn; ikke vist rød |
| test.b3.no-double-booking | B3 | `testSmallestFittingTableIsChosenAndNeverGivenTwice`, `testTablesAreJoinedOnlyWhenNoSingleTableFits`, `testAHoldEndsWhenTheDurationIsOver`. Hver avslutter med en kontroll av at ingen to bestillinger i overlappende tid deler bord | TESTRESULT.md#regler | grønn; vist rød med vilje (d138) |
| test.b3.route | B3 | `PalazzoBookingCellTests.testTheSameTableIsNeverGivenTwiceAndAFullHouseMeansTheWaitingList` | TESTRESULT.md#ruter | grønn; ikke vist rød |
| test.b4.guest-rules | B4 | `testGuestMustHitABookableTimeAndStayUnderTheHouseLimit` | TESTRESULT.md#regler | grønn; ikke vist rød |
| test.b4.cancel | B4 | `testCancellingFreesTheTableAndObeysTheDeadlineForGuests`, `PalazzoBookingCellTests.testGuestCannotCancelAfterTheDeadlineButTheHouseCan` | TESTRESULT.md#regler, #ruter | grønn; celletesten vist rød med vilje (d141), regeltesten ikke |
| test.b4.change-atomic | B4 | `testAChangeThatDoesNotFitLeavesTheBookingUntouched` | TESTRESULT.md#regler | grønn; vist rød med vilje (d138) |
| test.b4.states | B4 | `testMarkingFollowsTheAllowedTransitions` | TESTRESULT.md#regler | grønn; ikke vist rød |
| test.b5.walk-in | B5 | `testWalkInTakesATableNowOrIsRefused`, `PalazzoBookingCellTests.testStaffCreatesSeatsWalkInsMarksAndSeesTheDay` | TESTRESULT.md#regler, #ruter | grønn; regeltesten vist rød med vilje (d138), celletesten ikke |
| test.b6.waitlist | B6 | `testWaitlistHoldsNoTableAndCandidatesAppearAfterACancellation` | TESTRESULT.md#regler | grønn; vist rød med vilje (d138) |
| test.b7.overview | B7 | `testOverviewCountsCoversTablesAndKeyFigures` | TESTRESULT.md#regler | grønn; ikke vist rød |
| test.b8.no-field | B8 | `testABookingHasNoFieldForGuestDetails`: nøklene i det som lagres, er nøyaktig de fjorten som står i testen. Et nytt felt gjør testen rød | TESTRESULT.md#regler | grønn; ikke vist rød |
| test.b8.refused | B8 | `PalazzoBookingCellTests.testGuestBooksAndTheBookingLandsInTheirOwnEntityWhileTheHouseKeepsNoDetails`: navn, telefon, allergier og notat i forespørselen kommer tilbake som avvist, og finnes ikke i svaret, regnearket, oppslaget, kommende bestillinger eller tilstanden | TESTRESULT.md#ruter | grønn; vist rød med vilje (d141) |
| test.b9.own-entity | B9 | Samme test: gjestens entitet har én post mer, og `insight.bookings.upcoming` i gjestens egen entitet viser bestillingen | TESTRESULT.md#ruter | grønn; testen er vist rød (d141), men på påstandene om avviste felt, ikke på denne |
| test.b9.only-holder | B9 | `PalazzoBookingCellTests.testOnlyTheHolderOrTheHouseCanChangeOrCancel`: en annen gjest får samme svar som for en referanse som ikke finnes | TESTRESULT.md#ruter | grønn; vist rød med vilje (d141) |
| test.b9.limit | B9 | `testAGuestCannotHoldMoreOpenBookingsThanTheHouseAllows`, `PalazzoBookingCellTests.testOneGuestCannotBookOutTheHouse` | TESTRESULT.md#regler, #ruter | grønn; ikke vist rød |
| test.b9.instant | B9 | `testTheGuestsOwnRecordCarriesTheInstantAndNothingAboutTheTable` | TESTRESULT.md#regler | grønn; ikke vist rød |
| test.b10.waiter | B10 | `PalazzoBookingCellTests.testWaiterSeesOwnBookingsAndFindsTheGuestFromTheReference`: «Bookinger» teller bestillingen, briefen finner gjestens entitet, og ingenting gjesten ikke har delt, står i briefen | TESTRESULT.md#ruter | grønn; vist rød med vilje (d141) |
| test.b10.unchanged | B10 | `PalazzoBookingCellTests.testMergedBookingsLeaveTheImportAloneWhenTheHouseHasNoneOfItsOwn`: uten egne bestillinger er svaret importens svar, tegn for tegn | TESTRESULT.md#ruter | grønn; vist rød med vilje (d141) |
| test.b11.house-side | B11 | `PalazzoBookingCellTests.testGuestsAndUnrosteredStaffCannotReachTheHouseSide`: en gjest og en `staff:`-påstand uten plass på husets liste får 403 på ti ruter, og på planen gjennom den generiske celleflaten | TESTRESULT.md#auth | grønn; vist rød med vilje (d141) |
| test.b12.sheet | B12 | `PalazzoBookingCellTests.testTheHouseCanAskItsOwnNumbersInTheSheet` | TESTRESULT.md#ruter | grønn; vist rød med vilje (d141) |
| test.b0.calendar | grunnlaget for B2–B4 | `testCalendarKnowsRealDatesWeekdaysAndTimes`: datoer som finnes, ukedager, klokkeslett | TESTRESULT.md#regler | grønn; ikke vist rød |
| test.b1.shrink | B1 | `testAPlanCannotRemoveOrShrinkATableSomeoneHolds` og `PalazzoBookingCellTests.testThePlanCannotShrinkATableSomeoneHolds`: en plan kan ikke fjerne eller krympe et bord noen holder | TESTRESULT.md#regler, #ruter | grønn; vist rød med vilje (d146) |
| test.b1.areas-kept | B1 | `PalazzoBookingCellTests.testAPlanSentWithoutAreasKeepsAClosedAreaClosed`: et område planen ikke nevner, står som før, også når det er stengt | TESTRESULT.md#ruter | grønn; vist rød med vilje (d146, d149) |
| test.b3.midnight | B3 | `testATableHeldPastMidnightIsNotGivenAgainTheNextDay`: et bord som holdes over midnatt, gis ikke på nytt dagen etter | TESTRESULT.md#regler | grønn; vist rød med vilje (d146, d149) |
| test.b3.concurrent | B3 | `PalazzoBookingCellTests.testGuestsAskingAtTheSameMomentNeverShareATable`: tolv samtidige bestillinger om to bord gir to bord og ti avslag | TESTRESULT.md#roed | grønn; vist rød med vilje (d147) |
| test.b4.reconfirm | B4 | `testAGuestsChangeNeedsANewConfirmationWhenTheHouseConfirmsItself`: gjestens endring må bekreftes på nytt når seteplanen krever det, også utenom seteplanen; en endring uten innhold lar bekreftelsen stå | TESTRESULT.md#regler | grønn; vist rød med vilje (d146, d149) |
| test.b4.house-tables | B4 | `testTheHouseKeepsTheTablesItPointedOutWhenItChangesABooking`: huset beholder bordene, eller peker dem ut på nytt | TESTRESULT.md#regler | grønn; vist rød med vilje (d146, d149) |
| test.b4.party-off-grid | B4 | `testAGuestCanChangeThePartySizeOfABookingTheHouseMovedOffTheGrid` | TESTRESULT.md#regler | grønn; vist rød med vilje (d146) |
| test.b6.cap-waitlist | B6 | `testAGuestStoppedByACapCanStandOnTheWaitingList`: venteliste også når taket er nådd; et selskap større enn taket får nei | TESTRESULT.md#regler | grønn; vist rød med vilje (d146, d149) |
| test.b6.started | B6 | `testAGuestOnTheWaitingListCannotTakeATableAfterTheTimeHasStarted` | TESTRESULT.md#regler | grønn; vist rød med vilje (d149) |
| test.b8.channel | B8 | `testAChannelIsOneOfAClosedListAndNeverFreeText` og `PalazzoBookingCellTests.testTheHouseCannotWriteGuestDetailsIntoTheChannel`: kanalen er ett av sju faste ord; fri tekst fra huset avvises og lagres ikke | TESTRESULT.md#regler, #ruter | grønn; vist rød med vilje (d146, d149) |
| test.b8.guest-sees | B8, B9 | `PalazzoBookingCellTests.testTheGuestSeesThatTheHouseHoldsThePointerAndUnreadFieldsAreNamedOnAChange`: gjesten ser at huset har pekeren; felt som ikke leses, navngis ved endring og avbestilling | TESTRESULT.md#ruter | grønn; vist rød med vilje (d146, d149) |
| test.b10.refusal | B10 | `PalazzoBookingCellTests.testMergedBookingsSayWhenTheHousesOwnCameBackWithoutAList` | TESTRESULT.md#ruter | grønn; vist rød med vilje (d146) |
| test.root.stored-state | rotformålet | `testStoredStateThatCannotBeReadIsAnErrorAndNotAnEmptyHouse` og `PalazzoBookingCellTests.testTheCellRefusesToStartFromStoredBookingsItCannotRead`: lagret tilstand som ikke lar seg lese, gir feil og ikke et tomt hus | TESTRESULT.md#regler, #ruter | grønn; vist rød med vilje (d146, d149) |

## 6. Åpne spørsmål til Kjetil

1. **Hva skal dette være for Palazzo?** Tre veier: (a) det blir liggende på grenen som en mulighet, og GastroPlanner brukes som i dag; (b) det settes ut og prøves ved siden av GastroPlanner, for eksempel bare for walk-in og husets egen oversikt; (c) det er ment å erstatte GastroPlanner. To systemer som begge tar imot bestillinger for de samme bordene, gir dobbeltbestillinger. Velger du (b) eller (c), må det avgjøres hvilket som gjelder for hvilke bord. Jeg anbefaler (a) til du og Andre har sett på det.
2. **Navn på en bestilling.** Når en gjest ringer, har huset i dag ingenting annet enn referansen å gå etter. Punkt 5 fra 2. september sier at huset ikke lagrer allergiopplysninger; det sier ikke noe om navn. Skal huset kunne skrive et navn på en bestilling det fører selv? Jeg har ikke lagt inn feltet, fordi det er lettere å legge til enn å ta bort.
3. **Beskjed til gjesten.** Uten SMS eller e-post får ikke gjesten bekreftelse utenfor siden, og den som får bord fra ventelisten, får ikke vite det. Hvilken kanal, og hvem eier adressen: gjestens entitet, eller huset?
4. **Flatene.** Skal jeg tegne ferdig gjestens bestillingsside og husets bordbok for godkjenning (G1-GUI)? Skissene i `images/` viser retningen. Skjelettformatet har ikke kalender- eller bordelementer i dag; skissene er HTML.
5. **Linux-bygget.** Grenen er bare på Mac-en. Pusher jeg den som `pdd/…`, bygger og tester CI den på Linux, og publiserer samtidig et image som ikke settes ut. Vil du det?
6. **Gjestens egen post ved avbestilling.** Poster i entiteten kan bare legges til. Skal en avbestilling føres som en ny post («avbestilt»), eller skal entiteten kunne trekke en post tilbake? Det siste er en endring i entitetscellen.
7. **Ventelisten.** I dag er ventelisten en liste huset ser, og rekkefølgen er et råd. Et bord som blir ledig, kan bestilles av hvem som helst til huset har gitt det bort. Skal bordet holdes av til den som står først? Da må reglene endres, og gjesten må kunne få beskjed (spørsmål 3).

## 7. Revisjonslogg

| Iterasjon | Dato | Hva endret seg | Hvem |
|---|---|---|---|
| 0 | 2026-10-06 | Opprettet | Losen |
| 1 | 2026-10-07 | §0–§3, §5 og §6 fylt ut. Skrevet samme natt som koden, ikke før. Testene i §5 er de som faktisk er skrevet og kjørt | Losen |
| 2 | 2026-10-07 | Rettet etter uavhengig kontroll (K1, K2 og K5): §0 (vilkåret i ordene, to gjengivelser som ikke var ordrette), §1 (B1, B3, B4, B6, B8, B9), §2 (ikke en kø), §3 (to commits), §5 (hvilke tester som er vist røde, og 14 nye rader for 16 nye tester), §6 (spørsmål 7) | Losen |
