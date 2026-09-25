# Formålsspesifikasjon — scaffold admin delegering

Oppgavemappe: `PDD_scaffold-admin-delegering_2026-09-08` · Opprettet 2026-09-08 · Iterasjon 0 (ikke godkjent)

> Regel: ingen plan før G1 er godkjent av Kjetil. For GUI: ingen implementering før G1-GUI (rendret bilde) er godkjent.
> Et dokument om leveransen teller aldri som leveransen.

## 0. Intensjon (ordrett) og brief-audit
### Kjetils ord, ordrett

> Egentlig burde Digipomps entiteten være scaffold administrator som igjen burde
> delegere tilgangen til Vegar og meg. Skal vi være pirkete så bør vi da formelt
> innlemme vegar i Digipomps. Og så kan vi gjøre det samme med DiMy for de
> scaffoldene DiMy eier eller har ansvaret for. Vurder konsekvenser av dette og om
> dere kommer frem til at det er en god ide skal det implementeres og legges i
> deploykø.

Foranledning samme dag: «Gi publiseringstilgang i 7 dager» for brukernavn `vegar`
feilet med `Arendalsuka publisher access issuance requires owner proof or an
explicit publisherAccess.issue Agreement grant (agreement_or_proof_required)`.

### Brief-audit

| # | Påstand / antatt kapabilitet | Status | Kilde |
|---|---|---|---|
| A1 | En organisasjonsentitet kan i dag være scaffold-administrator | **contradicted** | `CellScaffold/Sources/ScaffoldKit/AdminMetricsSupport.swift:40-57` — `AdminRoleProfile` er observer/operator/nodeAgent/security, hver et bevis på keypath `identity.proofs.scaffold.roles.admin.*`, altså per **person-identitet**. `CellScaffold/Sources/App/Support/AdminEntityProofPersistenceSupport.swift:17-32` lagrer beviset i «the user's private EntityAnchor». Ingen organisasjonsentitet er innehaver noe sted. |
| A2 | Administrator kan delegere tilgang videre | **retrieved, men ikke via adminrollen** | `CellScaffold/Sources/App/Cells/Arendalsuka/ArendalsukaConfigurationPublisherCell.swift:80,225-234` — utstedelse krever `ownerProof` eller signert Agreement på `publisherAccess.issue`. Kildekommentaren sier: «Control-plane role labels are deliberately absent: the stored owner may act through owner proof, while every other identity needs the exact Agreement grant declared by this Cell.» Delegering finnes altså, men er celle-lokal og rolleuavhengig **med vilje**. |
| A3 | Vegar mangler publiseringstilgang nå | **retrieved** | Staging-datarot `/mnt/disk1/app/CellsContainer.staging-f76de5a`, fila `CellsContainer/7A741743-…/keypathstorage.json`: VC utstedt til `linkedIdentity.displayName = vegar` (uuid `8DCE5C5A-35E7-443E-A4A6-EDE781746CA4`), `issuanceDate 2026-09-02T08:06:06Z`, `validUntil 2026-09-04T08:06:06Z`. Utløpt. |
| A4 | Kjetil mangler utstedermyndighet nå | **retrieved** | Samme datarot: `grep -rl publisherAccess` gir **nøyaktig én** fil — VC-en over. Det finnes ingen lagret `publisherAccess.issue`-Agreement for noen. Kjetils nettleseridentitet løses altså verken til owner eller til avtalepart; avslaget kom i preflight, før utstedelse. |
| A5 | Adminpålogging virker | **retrieved** | Samme sesjon godkjente to correspondence-forespørsler på `/admin/funding` i dag. `admin.operator` fungerer; det er celle-myndigheten som mangler, ikke innlogging. |
| A6 | Staging og prod har hver sin autoritetsverden | **retrieved** | Datarøtter: staging `/mnt/disk1/app/CellsContainer.staging-f76de5a` (`.secrets` datert 19. aug), prod `/mnt/HC_Volume_104775511/haven-production/CellsContainer`. Ingen deling. |
| A7 | Det finnes en registrering av hvilke scaffolds DiMy eier eller har ansvaret for | **unavailable** | Ikke funnet i CellScaffold, CellProtocolDocuments eller på staging. Må komme fra Kjetil — se §6 Q1. |
| A8 | Vegar kan «formelt innlemmes i Digipomps» | **contradicted som formulert** | Digipomps er en stiftelse. En stiftelse har ingen medlemmer eller eiere å innlemmes i; tilknytning skjer som ansettelse, oppdragsavtale eller styre-/rolleoppnevning. Jeg er ikke jurist, og dette må bekreftes av en som er det. Poenget for oppgaven: den organisatoriske bindingen er en **avtale med en rolle**, ikke et medlemskap — og det er akkurat den formen Agreements allerede har. |
| A9 | Deploykøen tar imot en slik post | **retrieved** | `lesson.codex-sandbox-cannot-reach-docker` (2026-09-07): deploy-/image-steg planlegges aldri som Codex-slice, de registreres som HAVEN-Deploy-post med eier Kjetil. |

### Vurdering — er det en god idé?

**Ja i retning, med to forbehold som endrer utformingen.**

Argumentet for er sterkt, og dagens to feil er beviset. Både Arendalsuka-utstedelsen
og correspondence-godkjenningen henger i dag på at *én persons* nettleserbundne
identitet tilfeldigvis løser seg til celleeier i *én* datarot. Da staging fikk fersk
datarot 19. august forsvant den koblingen stille — ingen feilmelding, ingen
migrering, bare en knapp som slutter å virke uker senere. En organisasjonsentitet som
registrert administrator gjør myndigheten til noe som overlever personer, enheter,
nettleserøkter og datarot-bytter, og som kan trekkes tilbake ett sted.

Forbehold 1 — **adminrollen skal fortsatt ikke gi cellemyndighet.** Den fristende
snarveien er å la `admin.operator` bety «kan utstede». Det ville rive ned skillet
kilden kaller «deliberately absent», og gjøre HAVENs løfte om at rettigheter er
eksplisitte og formålsbundne til markedsføring. Digipomps-entiteten skal ikke få en
rolle som betyr alt; den skal kunne **utstede navngitte, tidsbegrensede,
tilbakekallbare Agreements per celle og keypath** — samme mekanisme som i dag, med en
organisasjon som utsteder i stedet for en tilfeldig person.

Forbehold 2 — **større blast radius krever terskel.** En entitet som kan delegere alt
er et bedre mål enn en person som kan delegere én ting. Digipomps har et styre på tre
([[profile]]: Kjetil, Petter Nielsen, Steinar Bjørlykke). Utstedelse av
*administratormandat* bør kreve mer enn én signatur, mens utstedelse av *dagligdags
celletilgang* under et allerede gitt mandat ikke bør det. Det er en beslutning for
Kjetil, ikke for meg — §6 Q3.

Bieffekt verdt å ta med: dette er nøyaktig mekanismen Kallimachos og tillitspakke-
ideen trenger senere — «hvilke fullmakter har denne agenten, fra hvem, hvor lenge, og
hvem kan trekke dem». Å bygge den nå på scaffold-administrasjon gir én mekanisme, ikke to.

## 1. Formålstre
Rot: `purpose://governance` (Book 23, active).

- **`purpose://candidate.scaffold-admin.org-is-registered-administrator`** — Hvert scaffold har en organisasjonsentitet registrert som administrator, og den registreringen er lesbar uten å kjenne noen persons identitet.
  - outcome: `cell:///ScaffoldSetup` (eller tilsvarende) svarer med administrator-entitet for scaffoldet.
  - successSignals: oppslag returnerer `entity:digipomps` for staging-scaffoldet; svaret inneholder ingen personidentitet.
  - verifier: `test.admin.registry-read`
- **`purpose://candidate.scaffold-admin.mandate-is-explicit-bounded-revocable`** — En person handler bare med et mandat som navngir celle, keypath, formål, varighet og tilbakekallsreferanse.
  - outcome: Et mandat er en signert Agreement utstedt av administrator-entiteten, aldri en rolleetikett.
  - successSignals: mandatet inneholder `resourceRefs`, `actionKeypaths`, `purposeRef`, `validUntil`, `revocationRef`; et mandat uten én av dem avvises.
  - verifier: `test.admin.mandate-shape`, `test.cell.auth-negative`
- **`purpose://candidate.scaffold-admin.role-label-grants-nothing`** — `admin.operator` og de andre rolleetikettene gir fortsatt null cellemyndighet.
  - outcome: Etter endringen feiler en utstedelse fra en admin uten mandat på nøyaktig samme måte som i dag.
  - successSignals: `agreement_or_proof_required` for admin uten mandat; ingen ny kodesti gir myndighet fra rolle.
  - verifier: `test.admin.role-is-not-authority`
  - lærdom: `lesson.purpose-never-grants-rights`
- **`purpose://candidate.scaffold-admin.threshold-matches-blast-radius`** — Terskelen for å utstede står i forhold til hvor mye mandatet åpner.
  - outcome: Påkrevd antall signaturer for administratormandat er en registrert verdi per scaffold, ikke en konstant i koden. Nåværende verdi er 1, med begrunnelse og dato.
  - successSignals: terskelen heves til 2 uten kodeendring; terskel under 2 gir `runtimeAdvisories`-linje som navngir scaffoldet og begrunnelsen; to signaturer fra samme identitet teller alltid som én.
  - verifier: `test.admin.threshold-is-policy`
  - kilde: Kjetils svar Q3 og presiseringen samme dag, 2026-09-08.
- **`purpose://candidate.scaffold-admin.authority-survives-or-fails-loudly`** — Et datarot-bytte skal enten bevare administrator-registreringen eller si fra ved oppstart.
  - outcome: Ny datarot uten administrator-registrering gir en synlig readiness-advarsel, ikke stille tap.
  - successSignals: `runtimeAdvisories` inneholder `scaffold_administrator_not_provisioned` når registreringen mangler.
  - verifier: `test.admin.fresh-root-advisory`
  - begrunnelse: dette er feilen fra 19. august, som traff A3/A4 seks uker senere.
- **`purpose://access.audit.privacy` → `purpose://candidate.scaffold-admin.audit-names-org-and-person`** — Revisjonssporet viser både hvilken organisasjon som ga mandatet og hvilken person som brukte det.
  - successSignals: hver utstedelse logger `mandateID`, administrator-entitet, handlende identitet og begrunnelse.
  - verifier: `test.admin.audit-pair`
- **`purpose://self-determination.data.recipients` → `purpose://candidate.scaffold-admin.delegation-is-visible-to-the-owner`** — Den som eier dataene kan se hvilke mandater som finnes på egne celler.
  - successSignals: en eier-lesbar liste over aktive mandater per celle.
  - verifier: `test.admin.owner-can-list-mandates`
- **`purpose://candidate.scaffold-admin.org-link-is-an-agreement-not-a-membership`** — Vegars tilknytning til Digipomps representeres som en rolleavtale med start, slutt og tilbakekall.
  - outcome: `entity:vegar` har en avtale utstedt av `entity:digipomps` med en navngitt rolle; ingen kode antar «medlemskap».
  - successSignals: avtalen kan trekkes tilbake uten å slette Vegars entitet eller hans data.
  - verifier: `test.admin.org-link-revocable`
  - merknad: den juridiske siden (A8) er Kjetils og en jurists, ikke denne oppgavens.

Blad uten eget formål er ikke tatt med. `purpose://candidate.*` er kandidater; ingen av
dem skrives til Book 23 uten Kjetil (Book 23 §8).

## 2. Avgrensning og avhengigheter
**Dette er ikke:**

- Ikke å gi Vegar publiseringstilgang i dag. Det er en egen, mye mindre oppgave som kan gjøres med dagens mekanisme så snart utstedermyndigheten finnes.
- Ikke en endring i prod. Prod har egen datarot (A6) og egen seremoni; den tas som eget punkt etter at staging er verifisert.
- Ikke en juridisk innlemmelse (A8).
- Ikke en ny adminflate. Om delegering skal ha en egen GUI-flate, utløser det G1-GUI som egen runde med rendret bilde.

**Avhengigheter, hver med verifier:**

| # | Avhengighet | Verifier | Status nå |
|---|---|---|---|
| D1 | Scaffoldets eierskaps-/oppsettsmodell (`Sources/App/Cells/Admin/ScaffoldSetupCell.swift`) tåler en administrator-registrering | lesing + kontraktvalidator | ikke undersøkt i detalj |
| D2 | EntityAnchor kan holde en organisasjonsentitet, ikke bare en person | `AdminEntityProofPersistenceSupport` + test | antatt, ikke verifisert |
| D3 | `entity:digipomps` og `entity:dimy` finnes eller kan opprettes på staging | oppslag mot staging | finnes ikke i dag (A1) |
| D4 | Liste over hvilke scaffolds DiMy eier | Kjetils svar (§6 Q1) | mangler |
| D5 | Deploykøen HAVEN-Deploy tar posten | `lesson.codex-sandbox-cannot-reach-docker` | gjelder |
| D6 | Staging er grønn før og etter | readiness-gaten i `cutover-invites-20260908.sh` | grønn i dag |

## 3. Forventningskontrakt — «Det du kommer til å se»
| # | Leveranse | Type | Hvor | Referanse |
|---|---|---|---|---|
| L1 | Denne formålsspesifikasjonen | fil | `Deliverables/PDD_scaffold-admin-delegering_2026-09-08/FORMAALSSPEC.md` | — |
| L2 | Kontrakt for administrator-registrering og mandat | fil (JSON + fixtures) | `contract/` i denne mappen, speilet i `Book/` | `pkg.std.cell-contract` |
| L3 | Dataflyt: hvem utsteder hva til hvem | fil | `dataflow.md` | `pkg.std.cell-combination` |
| L4 | Kodeendring i CellScaffold | kode | egen gren, ett commit per bladformål | §1 |
| L5 | Testutdata for hver rad i §5 | testutdata | `TESTRESULT.md` | — |
| L6 | Akseptanse: forventning mot faktisk | fil | `ACCEPT.md` | — |
| L7 | Deploykø-post | post | `HAVEN-Deploy`, eier Kjetil | D5 |

Etter G2 teller bare radene her som fremdrift (`lesson.plan-instead-of-delivery`).

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
    - artefakt skeleton/ (port G1-GUI): CellConfiguration/skeleton-JSON som bildet er rendret fra (når Porthole-preview er brukt).
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

## Book 23-noder som kan være forelder/gjenbruk (leksikalsk forslag, verifiser)
- purpose://governance [active] — Governance
- purpose://self-determination.data.recipients [candidate] — Recipients and delegation

## 5. Avledede tester (samlet)
| Test | Type | Hvordan | Bevis lander i |
|---|---|---|---|
| `test.admin.registry-read` | command | Les administrator-entitet for staging-scaffoldet gjennom produksjonens egen kodesti, ikke en testhjelper | `TESTRESULT.md#registry` |
| `test.admin.mandate-shape` | command | Positive/negative fixtures: mandat uten `validUntil`, uten `revocationRef`, uten `actionKeypaths`, med feil `purposeRef` — alle avvist | `TESTRESULT.md#contract` |
| `test.admin.role-is-not-authority` | command | Admin med `admin.operator` og uten mandat forsøker utstedelse → `agreement_or_proof_required` | `TESTRESULT.md#auth` |
| `test.cell.auth-negative` | command | Feil requester, feil keypath, `purpose://prompt.unknown` avvises | `TESTRESULT.md#auth` |
| `test.admin.threshold-is-policy` | command | Terskel 1: én signatur godtas og advisory-linja finnes. Terskel 2 satt uten kodeendring: én signatur avvises, to distinkte godtas, to fra samme identitet avvises | `TESTRESULT.md#threshold` |
| `test.admin.fresh-root-advisory` | command | Start scaffold mot tom datarot → `runtimeAdvisories` inneholder mangelen | `TESTRESULT.md#advisory` |
| `test.admin.audit-pair` | inspection | Utstedelseslogg viser mandatID, administrator-entitet, handlende identitet, begrunnelse | `ACCEPT.md#audit` |
| `test.admin.owner-can-list-mandates` | command | Eier lister aktive mandater på egen celle; ikke-eier får avslag | `TESTRESULT.md#mandates` |
| `test.admin.org-link-revocable` | command | Trekk tilbake Vegars rolleavtale → mandater under den slutter å virke, entiteten og dataene består | `TESTRESULT.md#revoke` |
| `test.cell.stub-scan` | inspection | Ingen no-op-handler uten `not-implemented` | `ACCEPT.md#stubs` |
| `test.build` / `test.regression` | command | Ekte baseline-kjøring før endring (`lesson.baseline-count-from-report-not-run`), så etter | `TESTRESULT.md#build`, `#regression` |
| `test.docs-updated` | inspection | Kapittel om autorisasjon oppdatert i samme endring | `ACCEPT.md#docs` |
| `test.status-current` | inspection | STATUS.md speiler faktisk tilstand | `ACCEPT.md#status` |

## 6. Åpne spørsmål til Kjetil
Bare spørsmål som endrer treet.

**Q1.** Hvilke scaffolds eier eller har DiMy ansvaret for? Jeg finner ingen registrering
noe sted (A7). Uten listen kan jeg ikke skille «Digipomps-scaffolds» fra
«DiMy-scaffolds», og §1 får ikke riktig antall administrator-entiteter.

**Q2.** Skal administrator-entiteten kunne utstede *mandat til å utstede videre*
(delegering i to ledd), eller bare mandat til å handle? To ledd er mer fleksibelt og
langt vanskeligere å trekke tilbake riktig. Jeg anbefaler å starte med ett ledd.

**Q3.** Skal utstedelse av administratormandat kreve mer enn én signatur fra styret?
Digipomps har tre i styret. Jeg anbefaler: mandat til *å administrere* krever to
signaturer, mandat til *å bruke* en enkelt celle krever én. Dette er din beslutning.

**Q4.** Skal Vegar ha publiseringstilgangen med en gang som en midlertidig utstedelse
under dagens mekanisme, eller skal han vente til denne oppgaven er ferdig? Dagens
mekanisme krever at noen med owner-proof gjør det én gang — det er timer, ikke dager.

### Kjetils svar 2026-09-08

- **Q1 — besvart 2026-09-08.** DiMy skal være administrator for Palazzo, og for Arendalsuka/konferanser når de flyttes til eget scaffold. Flere kommer. Digipomps er administrator for resten, inkludert dagens CellScaffold-staging. Konsekvens for §1: administrator-registreringen må være **per scaffold**, ikke global, og må tåle at et scaffold skifter administrator når ansvaret flyttes. Nytt suksesssignal på `org-is-registered-administrator`: oppslag mot to forskjellige scaffolds gir to forskjellige administrator-entiteter, og et administratorskifte er en egen, revisjonsspor-førende handling.
- **Q2 — ett ledd.** Administrator-entiteten utsteder mandat direkte til den som skal handle. Ingen videredelegering i første versjon. Formålet `purpose://candidate.scaffold-admin.mandate-is-explicit-bounded-revocable` får derfor et eksplisitt suksesssignal: et mandat som forsøker å gi utstederrett avvises.
- **Q3 — revidert samme dag: én signatur inntil videre.** Kjetil presiserte: styreleder holder terskelen alene inntil prod er stabil og dette ikke lenger de facto er et utviklingsprosjekt — de øvrige styremedlemmene svarer sent, og å kreve to signaturer nå ville bare bremse arbeidet.

Konsekvensen for formålet er ikke å fjerne terskelen, men å gjøre den til **registrert policy per scaffold med synlig unntak**. Ellers gjentar vi feilen fra 19. august i ny form: en sikkerhetsegenskap som forsvinner stille og som ingen oppdager før den mangler. `purpose://candidate.scaffold-admin.threshold-matches-blast-radius` får derfor: outcome — påkrevd antall signaturer for administratormandat er en registrert verdi per scaffold, ikke en konstant i koden; nåværende verdi er 1 med begrunnelse «utviklingsfase, styreleder alene» og en dato. successSignals — terskelen kan heves til 2 uten kodeendring; en terskel under 2 gir en `runtimeAdvisories`-linje som navngir scaffoldet og begrunnelsen; to signaturer fra samme identitet teller alltid som én, uansett terskel. verifier: `test.admin.threshold-is-policy`.
- **Q4 — Vegars publiseringstilgang fikses nå med dagens mekanisme.** Egen, liten oppgave utenfor denne PDD-en. Forutsetningen er at noen med owner-proof for `cell:///ArendalsukaConfigurationPublisher` utsteder én gang; hvem det er i praksis på staging er **ikke** verifisert ennå (se A4 — det finnes ingen lagret Agreement, så det må være owner-veien). Undersøkes før noe loves.

## 7. Revisjonslogg

- 2026-09-08 v4 — Q3 revidert av Kjetil: én signatur (styreleder) inntil prod er stabil. Terskelen blir registrert policy per scaffold med synlig advarsel når den er under 2, i stedet for en konstant. Test omdøpt til `test.admin.threshold-is-policy`.
- 2026-09-08 v3 — G1 godkjent av Kjetil. Q1 besvart: DiMy administrerer Palazzo og (etter flytting) Arendalsuka/konferanser; Digipomps resten. Administrator-registrering er per scaffold og må tåle administratorskifte.
- 2026-09-08 v2 — Q2/Q3/Q4 besvart av Kjetil; nytt bladformål `threshold-matches-blast-radius` og ny test `test.admin.threshold-two-of-three`. Q1 (DiMys scaffolds) står fortsatt åpen og er første inndata i P2.
- 2026-09-08 v1 — P0+P1 skrevet i én runde: intensjon ordrett, brief-audit med ni påstander (to contradicted, én unavailable), formålstre under `purpose://governance`, avgrensning, forventningskontrakt, avledede tester, fire åpne spørsmål. Venter på G1.

| Iterasjon | Dato | Hva endret seg | Hvem |
|---|---|---|---|
| 0 | 2026-09-08 | Opprettet | Losen |
