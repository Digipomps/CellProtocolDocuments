# Formålsspesifikasjon — Signert medlemsbevis i en gruppeentitet

Oppgavemappe: `PDD_medlemsbevis-gruppe_2026-11-24` · Opprettet 2026-11-24 · Iterasjon 2 (G1 godkjent 2026-11-25)

> Regel: ingen plan før G1 er godkjent av Kjetil. For GUI: ingen implementering før G1-GUI (rendret bilde) er godkjent.
> Et dokument om leveransen teller aldri som leveransen.

## 0. Intensjon (ordrett) og brief-audit

Kjetil, 2026-11-24 12:35Z (svar i tråden om kapittel 09 «Unik representasjon»):

> Godkjent. Men lag funksjonalitet for å at medlemmer kan få et signert bevis for at de er godtatt som en entitet i gruppen. Dette kan styres av en moderator eller gjennom bevis på at man eier fødselsnummeret sitt. (Kan brukes som eksempel for studentene på en løsning som fungerer ganske godt i norge - skjønt ikke 100% - men andre steder i varden er ikke dette en opsjon. F.eks ved dobbelt statsborgerskap får man to identifikatorer)

Sammenheng fra prosjektet (ikke Kjetils ord): bygger på gruppeentiteten Informasjonssystemer
(`PDD_informasjonssystemer-gruppeentitet_2026-11-17`, CPD #46, WP1–10 tagget i CellProtocol 2026.9.18) og
er et konkret eksempel for Saras Tema A (unik representasjon). Kapittel 09 (CPD #52, godkjent 24.11) sier at
HAVEN i dag **ikke** har sybil-motstand. Denne PDD-en skal ikke endre det utsagnet til mer enn det koden viser.

Kodestand som er lest: CellProtocol `12fa8bf` (main 24.11), PyCellProtocol `826db6a` (main), GoCellProtocol
`c0274c2` (main), CellScaffold `6e2f667` (main 24.11), CellProtocolDocuments main 24.11 + PR #52.

| Påstand i intensjonen / antatt kapabilitet | Audit | Kilde |
|---|---|---|
| En gruppe kan signere bevis for sine medlemmer | **retrieved.** Gruppen utsteder rollebevis (`OrganizationRoleCredential`) signert av hvelvets egen nøkkel, aldri en eiers personlige nøkkel; feltene som avgjør tilgang ligger i `credentialSubject`, som beviset dekker | `CellProtocol/Sources/CellBase/Organization/OrganizationRoles.swift:10–75` |
| Bevis kan trekkes tilbake | **retrieved.** Signert statusliste (`OrganizationRoleStatusList`), speilet lokalt i `CredentialStatusRegistry`; manglende eller for gammelt speil gir `unknown` og feiler lukket (10 min) | `OrganizationRoles.swift:78–204` |
| Det finnes «medlem» som begrep i gruppa | **contradicted.** `OrganizationRole` har `owner, chair, boardMember, ceo, procurist`; rollebevisene i Informasjonssystemer er student/forsker/veileder. Ingen `member`-rolle, ingen «godtatt som entitet» | `GovernancePolicy.swift:22–33`; `OwnershipAgreement.swift:15–26` |
| Det finnes en moderator-rolle | **contradicted.** Ingen `moderator` i `OrganizationRole`. Handlingsklassene er `role.issue`, `role.revoke`, `role.status.publish`, `policy.amend`. En moderator med `role.issue` ville kunne utstede *alle* roller, også forsker; det må skilles ut | `OwnershipAgreement.swift:15–26` |
| Tilgang kan kreve et slikt bevis via Agreement | **retrieved i Swift, Python og Go.** Swift `ProvedClaimCondition` (VC, subjekt = requester, gyldig bevis, utsteder godkjent av TrustedIssuer). Py/Go har organisasjonsmodellen og rollebevis/statusliste-sjekk i `interop/organization.*`, med felles fixtures (`org.role.valid`, `org.role.tampered`, `org.status.*`, `org.access-matrix`) | `CellProtocol/Sources/CellBase/Agreement/Condition/Implementation/ProvedClaimCondition.swift`; `PyCellProtocol/src/cellprotocol/interop/organization.py`; `GoCellProtocol/interop/organization.go`; `PyCellProtocol/tests/fixtures/interop/v1/` |
| HAVEN kan verifisere at noen eier et fødselsnummer | **retrieved, delvis** (rettet i iterasjon 2; iterasjon 1 sa «contradicted» etter å bare ha lest CellProtocol). CellScaffold har en eID-kobling via ID-porten direkte eller en OIDC-megler (`Sources/App/EID/`). Den kobler eID til en *eksisterende* innlogget entitet, gir ingen tilgang, og har **ingen leverandøravtale eller klientregistrering**; alle tester bruker en falsk IdP. I CellProtocol finnes ingen eID-kode; OpenID4VP er delvis, SD-JWT VC og mdoc (EUDI-PID) mangler | `CellScaffold/Documentation/EID.md:1–6`; `CellScaffold/Sources/App/EID/VaporEID.swift`; `CellProtocol/Docs/VerifiableCredentials_EUDI_Gap_Checklist.md` |
| eID-koblingen kan oppdage at samme person kommer to ganger | **contradicted, med vilje.** Pseudonymet er HMAC over eier/entitet/utsteder/subjekt **pluss et ferskt tilfeldig salt** for hver kobling, så samme nummer gir nytt pseudonym hver gang. Unikhet i en gruppe krever et nytt, *stabilt* pseudonym per gruppe; den som har gruppas nøkkel (driftsoperatøren) kan regne det ut. Oppbevaring og rotasjon av hash-nøkkelen er ikke avgjort | `CellScaffold/Documentation/EID.md:75–80, 89–91` |
| HAVEN kan i dag hindre at én person blir medlem to ganger | **contradicted.** Kapittel 09 HF-09-06 [ikke ennå]: ingen sybil-motstand, ingen nullifiers, ingen anonyme medlemsbevis | `CellProtocolDocuments` PR #52 `Book/40_HAVEN_Forklart/09_unik_representasjon.md` |
| Fødselsnummer gir én identifikator per person i Norge «ganske godt, ikke 100 %» | **recalled** (ikke målt her). Kjente brudd: D-nummer som senere blir fødselsnummer, nytt fødselsnummer ved endret juridisk kjønn, ny nummerstruktur fra 2032, personer uten norsk eID, lånt/delt BankID. Dobbelt statsborgerskap gir to nasjonale identifikatorer (Kjetils eksempel). Skal verifiseres mot Skatteetaten/Digdir før teksten til studentene skrives | — (åpen kilde i WP for studentteksten) |
| Fødselsnummer er personopplysning som krever særskilt vern | **recalled.** Personopplysningsloven § 12: fødselsnummer kan bare behandles når det er saklig behov for sikker identifisering. Gruppa trenger *unikhet*, ikke selve nummeret, så nummeret skal ikke lagres | — (verifiseres i WP for personvern) |

## 1. Formålstre

Rot: **`purpose://candidate.medlemsbevis-gruppe.root`** — Et medlem kan vise et bevis, signert av gruppa, for at
gruppa har godtatt det som én entitet i gruppa; andre celler kan kreve beviset gjennom en Agreement-betingelse;
og det står ærlig hva beviset ikke garanterer. Forelder: `purpose://governance`.

| # | Formål (`purpose://candidate.medlemsbevis-gruppe.*`) | Mål (outcome) | Suksesssignaler | Verifier |
|---|---|---|---|---|
| 1 | `credential` — medlemsbeviset | Gruppa utsteder `GroupMembershipCredential`: en `OrganizationRoleCredential` med rolle `member`, signert av hvelvets nøkkel, subjekt = medlemmets domene-identitet. Feltet `admittedVia` (`moderator` eller `national-id:NO`) og `validUntil` ligger i `credentialSubject` | Bevis verifiseres i Swift, Python og Go fra samme fixture; endret `admittedVia` gir ugyldig bevis | test.cred.roundtrip, test.cred.tampered |
| 2 | `moderator-admits` — moderator godtar | En moderator (ny rolle i `GovernancePolicy`) kan godta eller avvise en søknad. Moderator kan *bare* utstede og trekke tilbake `member`, aldri andre roller (ny handlingsklasse `membership.admit` / `membership.revoke`, adskilt fra `role.issue`) | Moderator-godkjent søknad gir bevis; moderator som prøver å utstede `researcher` avvises; moderator kan ikke godta seg selv | test.mod.admit, test.mod.scope-negative, test.mod.self-negative |
| 3 | `national-id-admits` — fødselsnummer-veien | Et medlem som beviser at det eier et norsk fødselsnummer/D-nummer gjennom en eID-utsteder gruppa stoler på (TrustedIssuer), får beviset uten moderator. Gruppa lagrer **aldri** nummeret | Gyldig eID-attest gir bevis automatisk; attest fra ukjent utsteder avvises; fødselsnummeret finnes ikke i noen lagret tilstand eller logg | test.nid.admit, test.nid.untrusted-issuer, test.nid.no-plaintext |
| 3a | `national-id-admits.one-per-number` — én gang per nummer | Gruppa holder et register med en gruppe-spesifikk pseudonym (HMAC med gruppas hemmelige nøkkel over `NO:` + nummer). Samme nummer kan ha bare ett gyldig medlemsbevis i gruppa | Andre forsøk med samme nummer fra en annen identitet gir «allerede medlem» (eller flytting, se §6 q2); pseudonymet kan ikke regnes tilbake uten gruppas nøkkel; to grupper får ulike pseudonymer for samme person | test.nid.duplicate, test.nid.unlinkable |
| 3b | `national-id-admits.eid-source` — hvor beviset kommer fra | v1 gjenbruker CellScaffolds eID-kobling (ID-porten/OIDC-megler) med den falske IdP-en i testene og en test-IdP på staging med syntetiske numre. I tillegg til dagens saltede bevis regner gruppa sitt stabile pseudonym i samme kall, slik at subjektet aldri forlater eID-kallet. Ekte eID krever leverandøravtale, klientregistrering og personvernvurdering (se §2) | Test-IdP godtas bare på staging; prod-konfigurasjon uten ekte leverandør avviser eID-veien | test.nid.test-issuer-staging-only, test.nid.same-call |
| 4 | `agreement-gates` — beviset gir tilgang bare via Agreement | En gruppecelle (f.eks. en avstemming eller felles chat) kan kreve «gyldig medlemsbevis fra gruppa» som Agreement-betingelse, og kan i tillegg kreve `admittedVia = national-id:NO` | Samme tilgangsmatrise (gyldig/endret/trukket/ukjent status/feil utsteder) gir samme svar i Swift, Python og Go; ingen språkspesifikk snarvei | test.access.matrix (felles fixture) |
| 5 | `revoke-and-leave` — tilbaketrekking | Moderator kan trekke tilbake; medlemmet kan melde seg ut; pseudonymet **slettes** da straks (ikke bare frigjøres) | Trukket bevis gir `revoked` innen ett statuslisteintervall; pseudonymet finnes ikke lenger i lagret tilstand; utmeldt nummer kan melde seg inn igjen | test.revoke.status, test.revoke.free-pseudonym |
| 5a | `privacy` — samtykke og hva beviset bærer | Søkeren ser og godtar hva som lagres (pseudonym, tidspunkt) før eID-veien. Selve medlemsbeviset inneholder **ikke** pseudonymet, så den som sjekker beviset kan ikke koble det til andre grupper | Beviset som sendes ut har ikke pseudonymfeltet; samtykke er lagret før pseudonymet | test.priv.no-pseudonym-in-credential, test.priv.consent-first |
| 6 | `surfaces` — flatene | Medlem: «Medlemsbevis» (søk via moderator / bevis med eID, venter, godtatt, avvist, allerede medlem). Moderator: kø med søknader, godta/avvis. Vises i web og Binding (Swift) | Godkjente G1-GUI-bilder; flatene har alle handlinger nåbare | test.gui.parity, test.skeleton.purpose-actions-reachable |
| 8 | `one-vote-example` — én stemme per bevis (eksempel, avhenger av §6 q6) | En avstemming i en gruppecelle kan kreve medlemsbevis og telle én stemme per aktivt bevis, ikke per identitetsnøkkel (i dag: per nøkkel, `LiveInteractionCell.swift:1711`) | To identiteter med samme pseudonym gir én stemme; to moderator-godtatte identiteter for samme person gir fortsatt to (og det står i studentteksten) | test.vote.one-per-credential |
| 7 | `limits-stated` — det beviset ikke garanterer | Kapittel 09 får et nytt avsnitt [med forbehold] som sier nøyaktig hva medlemsbeviset gir, og en liste over der det ikke holder; et studentark bruker dette som eksempel | Ingen tekst sier «én person, én stemme»; hver begrensning har kilde; Kjetil har godkjent teksten | test.docs.claims (claims.json), test.docs.no-overclaim |

Begrensningene formål 7 skal skrive ned (utkast, til verifisering):

- **Moderator-veien gir ingen unikhet.** Den hviler på moderatorens skjønn. Én person kan få to bevis fra to identiteter om moderatoren ikke ser det.
- **Fødselsnummer-veien gir unikhet bare innenfor «personer med norsk nummer».** Dobbelt statsborgerskap: godtar gruppa også et annet lands eID, kan samme person bli medlem to ganger med to nasjonale identifikatorer; godtar den bare norsk, er alle uten norsk nummer utestengt fra den veien.
- **Samme person kan få nytt nummer:** D-nummer som blir fødselsnummer, nytt nummer ved endret juridisk kjønn. Uten oppslag i Folkeregisteret ser gruppa to ulike personer.
- **eID kan lånes.** Beviset viser at noen med tilgang til eID-en var med, ikke hvem som sitter ved tastaturet senere.
- **Tillit flyttes til staten og eID-leverandøren.** Leverandøren kan se at du logger inn mot gruppa.
- **Driftsoperatøren kan regne ut pseudonymet**, fordi den holder gruppas nøkkel. Det er ikke anonymt overfor den som drifter noden.
- **Pseudonymet er bare trygt så lenge gruppas nøkkel er hemmelig.** Fødselsnumre er få nok til å prøves ut; en vanlig hash uten hemmelig nøkkel kan regnes tilbake.
- **Det er ikke anonymt.** Gruppa vet hvilken identitet som er medlem; den vet ikke nummeret. Anonyme medlemsbevis og nullifiers (Tema A) er fortsatt [ikke ennå].
- **Andre steder i verden finnes ikke et slikt nummer**, eller det er ikke knyttet til en eID.

## 2. Avgrensning og avhengigheter

**Dette er ikke:** anonym stemmegivning, nullifiers eller sybil-motstand i generell forstand; integrasjon med ekte
ID-porten/BankID i v1; lagring eller visning av fødselsnummer; en endring i hvem som eier gruppa.

| Avhengighet | Status | Verifier |
|---|---|---|
| Gruppeentitet med hvelv som signerer rollebevis (Swift) | tagget CellProtocol 2026.9.18 | `OrganizationRoles.swift`, org-tester grønne (TESTRESULT i informasjonssystemer-PDD) |
| Hvelvet overlever omstart (persist/restore) | **ikke landet**: branch `claude/organization-vault-restore`, ingen PR | må være på CellProtocol main før moderator-veien kan virke på staging |
| Gruppa finnes på staging (WP11–13 i informasjonssystemer-PDD) | **ikke landet**: CellScaffold-branch `claude/informasjonssystemer-gruppeentitet`, ingen PR | flaten kan ikke måles på staging før dette er der; G1-GUI bruker web-rendereren |
| Rollebevis og statusliste i Python og Go | på main (Py `826db6a`, Go `c0274c2`) | felles fixtures `tests/fixtures/interop/v1/org.*` |
| eID-attest for fødselsnummer | **finnes ikke** | v1 bruker test-utsteder (3b); ekte eID er åpent spørsmål q1 |
| Rettslig grunnlag og personvernvurdering (DPIA) for å behandle fødselsnummer, også flyktig | **finnes ikke** (ingen DPIA funnet; `EID.md:89–91` sier oppbevaring må avgjøres før ekte innrulling) | Kjetils ansvar; til det finnes bygges og testes eID-veien bare med falsk IdP / syntetiske numre |
| CellScaffolds eID-kobling (falsk IdP i tester) | på main `6e2f667` | `CellScaffold/Sources/App/EID/`, eID-testene |
| Medlemsopptak etter regel i gruppeeid celle (`PDD_gruppeeid-celle`, G1 19.11, G2 venter) | egen tråd | ord og flyt koordineres med den; ikke to ulike opptaksmodeller |
| Gruppeflaten (Informasjonssystemer på staging) | **finnes ikke ennå** | WP11–13 i informasjonssystemer-PDD |

## 3. Forventningskontrakt — «Det du kommer til å se»

| Leveranse | Type | Hvor | Referanse |
|---|---|---|---|
| Bilder av medlemsflaten (tom, venter, godtatt, avvist, allerede medlem) og moderatorkøen, laptop + iPhone | bilde | `images/` | G1-GUI |
| `GroupMembershipCredential`, moderatorrolle og `membership.*`-handlingsklasser i CellBase (Swift) med tester | testutdata | `TESTRESULT.md#swift` | formål 1, 2, 5 |
| Fødselsnummer-veien med pseudonymregister og test-utsteder (Swift) | testutdata | `TESTRESULT.md#nid` | formål 3, 3a, 3b |
| Felles tilgangsmatrise grønn i Swift, Python og Go | testutdata | `TESTRESULT.md#parity` | formål 4 |
| Flatene kjørende på staging, i web og Binding | kjørende flate + skjermbilder | staging | formål 6, `test.gui.parity` |
| Nytt avsnitt i kapittel 09 og et studentark «Medlemsbevis som eksempel på unik representasjon» | fil | `Book/40_HAVEN_Forklart/09_unik_representasjon.md`, `Manuals/` | formål 7 |


## 4. Tilknyttede formålspakker og lærdommer (auto fra purpose_dev.py lookup)

Lærdommer som former treet:
- `lesson.purpose-never-grants-rights`: medlemsbeviset gir ingen tilgang alene; bare en Agreement-betingelse som krever det (formål 4).
- `lesson.planned-documented-as-implemented`: kapittel 09 får bare påstander koden viser; v1 med test-utsteder skal ikke beskrives som «BankID-verifisert» (formål 7).
- `lesson.ciphertext-field-held-plaintext-hash`: «nummeret lagres ikke» sjekkes på bytene i lagret tilstand og logger, ikke på feltnavn (test.nid.no-plaintext).
- `lesson.text-ux-is-not-design`: flatene godkjennes som bilder før kode (formål 6).
- `lesson.location-is-not-ownership`: samme regler lokalt og i skyen; Swift, Python og Go gir samme svar (formål 4).

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
- **lesson.stand-in-shared-the-callers-assumption** (2026-10-05, major): Første tørrkjøring på Macen stoppet fordi korrespondanseklienten svarte «No enrolled correspondence profile exists», mens 42 tester og 126 selvkontroller var grønne i skyen.
    - forebygging: Før kode skrives mot et eksternt program, måles kontrakten der programmet kjører: argumentene, avslutningskodene og den ordrette teksten når det nekter. Stedfortrederen i testene skal nekte på samme måte. Test: én test kjører stedfortrederen med inndataene det ekte programmet nektet, og krever samme kode og tekst; og når det gamle kallet settes tilbake i en kopi, blir testene røde.
- **lesson.file-copied-to-the-mac-was-the-previous-version** (2026-10-05, major): En commit gikk ut med testen, men uten endringen den prøvde: filkopien fra skyøkten til Macen meldte «written», og fila på Macen var forrige utgave. To skript mistet dessuten kjørbar-biten på veien.
    - forebygging: Hver utgave som skal til Macen, legges under et nytt filnavn i utdatamappen. Sjekksummen på Macen sammenlignes med den i skyen i et eget steg, og neste steg (commit eller køjobb) startes ikke i samme kommando. Test: commit-jobben viser «git diff --cached --stat --summary» før commit, og lista over filer og moduser sammenlignes med det som skulle med.
- **lesson.pr-opened-without-reading-the-base-branch-ci** (2026-10-05, minor): PR #30 ble opprettet uten at CI-tilstanden på main var lest: løpet sto til tidsgrensen på 25 minutter av en grunn som hadde stått på main i seks dager, og den første lesningen av loggen, at det stoppet før PR-ens tester hadde startet, ble felt av den uavhengige kontrollen.
    - forebygging: Før en PR opprettes, listes løpene for basisgrenen; har hodet ikke noe grønt løp med samme testskript, rettes det først, eller rettelsen tas med. Før en årsak skrives ned for et rødt løp, leses avsnittet om CI i skillen, og siste linje i en logg kalles ikke stedet det stoppet. Test: skriptet som oppretter en PR, viser siste løp på basisgrenen og stopper når det er rødt.
- **lesson.the-scripts-own-python-was-newer-in-the-tests-than-on-the-mac** (2026-10-06, minor): Testene av bytteskriptet kjørte skriptets egne Python-blokker med 3.11, mens Macen har 3.9.6, som avviser datoformer 3.11 tar.
    - forebygging: Testene bytter stien til tolken, i kopien av skriptet de kjører, til utgaven målmaskinen har, og én test krever at ingen annen tolk står igjen i kopien. Datoer tolkes uten funksjoner som oppfører seg ulikt mellom utgavene.
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
- **lesson.status-did-not-say-status-or-what-to-do** (2026-10-06, major): Eieren 06.10 om statusen han fikk: «Dette sier meg ingenting om hva status er eller hva jeg skal gjøre.» Han skrev selv formålet og spurte hva som gjensto for å få prøvd med de to mottakerne.
    - forebygging: En statusmelding åpner med hvor formålet står for dem det gjelder, så det eieren skal gjøre i nummererte punkter, så leddene som gjenstår. Arbeid på et sidespor kalles et sidespor. Test: kontrolløren får eierens ord fra §0 og svarer på om første avsnitt sier hva mottakerne har fått.
- **lesson.few-steps-was-counted-for-the-recipient-and-not-for-the-owner** (2026-10-07, minor): Utkastet til G1 talte tre håndgrep for mottakeren og skrev «én gang per person» for eieren («ett trykk» i spesifikasjonen bak). Bildet viste to Touch ID per person og en kode å sammenligne, og rekkefølgen på eierens steg sto feil. Kontrollen før framlegget fant det.
    - forebygging: Der «få håndgrep» er et formål, telles håndgrepene for hver part, eieren først, per person og per runde, fra bildene og i rekkefølgen de skjer. Et steg som følger av et forslag, merkes som forslag. Test: et opptak på en ren maskin der håndgrepene er telt.
- **lesson.a-second-safeguard-hid-that-the-first-had-no-test** (2026-10-06, major): Én av 145 innsatte feil, kalt nr. 100 i filnavnene for omkjøringen («fila legges tilbake mens haven-deploy kanskje går»), ble ikke fanget, og alle 133 testene var grønne med den.
    - forebygging: To vern foran samme handling får hver sin test der det andre ikke kan svare. En innsatt feil som ingen test fanger, leses i utskriften før den regnes som ufarlig. Test: for hvert vern finnes et tilfelle der bare det vernet står mellom skriptet og handlingen.
- **lesson.deadline-request-left-out-what-follows-when-it-passes** (2026-10-06, minor): Utkastet til meldingen etter byttet ba eieren godkjenne to forespørsler innen 24 timer, uten å si at invitasjonen da er brukt opp og at en ny trengs (etter kontrollørens lesning: nytt bytte og ny omstart av staging), og uten steget etter: hans godkjenning av mottakernes egne forespørsler. Kontrollen før sending fant det.
    - forebygging: En forespørsel med frist sier hva som skjer når fristen går ut, og nevner hvert senere steg som er eierens. Test: kontrolløren spør for hver frist i meldingen «hva følger hvis den ikke holdes?» og «hva er hans neste steg etter dette?».
- **lesson.question-used-the-repos-words-and-came-back-as-a-question** (2026-10-07, minor): To av fem nummererte punkter til eieren kom tilbake som spørsmål: «Hva gjør assistentidentiteten?» og «Hva mener du med at vedlegg kan gå til main? Vi skal ikke lagre vedlegg i git så forklar hva du mener.»
    - forebygging: Et spørsmål til eieren bruker hans ord og sier hva en ting gjør før det spør om den. Test: kontrolløren leser hvert spørsmål, slik det blir sendt, som en som ikke kjenner repoet, og sier hvilke ord som må forklares.
- **lesson.render-candidate-skeleton-with-the-web-renderer-before-g1-gui** (2026-10-02, major): G1-GUI-bilder har vært mockups (butler-PDD-en) eller krevd en kjørende CellScaffold med Porthole-preview. Begge gir enten feil piksler eller en byggerunde før Kjetil får se noe.
    - forebygging: For en ny flate: eksporter de to filene fra CellScaffold origin/main (md5 i images/README.md), rendre kandidat-skjelett-JSON med eksempeldata i Playwright/Chromium (images/render.js i PDD_lister), lagre bildene som G1-GUI-referanse og mål oppførsel (onAction-payloads) i samme kjøring. Etter implementering: en test som krever at Swift-fabrikken gir kanonisk byte-lik JSON som fixturen bildet ble rendret fra, og en ny render fra cellens ekte state med pikseldiff mot referansen. PDD_lister: 0 piksler avvik på tre flater.
- **lesson.shared-swiftpm-cache-lost-its-ownership-marker** (2026-10-08, minor): Første bygg i et nytt CellProtocol-arbeidstre stoppet etter 4 s: haven-swiftpm.sh exit 64, «existing cache lacks the required ownership marker: …/T/haven-swiftpm-bounded/caches/90c10549…».
    - forebygging: Byggeskript for en PDD setter HAVEN_SWIFTPM_CACHE_KEY=<pdd-slug> (egen cache) i stedet for å reparere den delte; koster ett kaldt bygg (6 min for CellProtocol). Test: skriptet skriver cache-key i rapporten.
- **lesson.xctest-stdout-export-interleaves-with-its-own-log** (2026-10-08, minor): En test printet 49 kB JSON til stdout mellom markører for at byggeskriptet skulle klippe den ut; fila ble ugyldig ved byte 49156 — XCTests egen «Test Case '…' passed»-linje lå midt inne i JSON-en.
    - forebygging: En test som skal levere data til et skript, skriver til en fil (NSTemporaryDirectory()) og printer bare stien; skriptet validerer JSON før det kopierer. Og: /usr/local/bin/python3 på Kjetils Mac er en x86-binær («Bad CPU type in executable») under launchd — bruk /usr/bin/python3 eller node i skript.
- **lesson.textfield-cannot-carry-instance-identity-in-a-mount** (2026-10-08, major): Inne i en ComponentSurface-montering kan Button si hvilken liste den gjelder (payload fra raden), men TextField sender bare en string til en fast targetKeypath — «Legg til …» i montering nr. 2 ville havnet i aktiv liste.
    - forebygging: Kjetil valgte A (2026-10-08): SkeletonComponentActionContext (struct + @TaskLocal) i CellBase; cellen leser mount.instanceID; CellScaffold bytter ScaffoldKit-typen til en typealias i integrasjonspakken. Regel for nye komponenter: alt som skal vite instansen går via Button-payload eller monteringskonteksten — aldri via aktiv-tilstand i cellen. Test: ListsCellTests.testMountedComponentContextTargetsTheMountedListNotTheActiveOne.
- **lesson.capability-based-layout-variant-replaces-client-checks** (2026-10-08, minor): Flytting av punkter trengte piler i appen og dra-og-slipp på web, uten to skjeletter eller klientnavn.
    - forebygging: layoutVariants: [{requiresCapability: [drag], hidden: true}] på pilene: web erklærer drag (porthole-webo.js), Binding erklærer pointer/hover/keyboard eller touch (PortholeView.swift) — pilene forsvinner av seg selv den dagen appen får drag-adapteren. Test: layoutVariant(in:) med begge kapabilitetssett (ListsConfigurationTests) + web-harness variants (render-report-wp5.json).
- **lesson.explore-requiredkeys-match-codable** (2026-10-12, major): Schema-gyldig konfigurasjon kunne mangle felt som Codable krever.
    - forebygging: Sammenlign requiredKeys med avvisning ved fjerning av hvert required felt; ta med nested visibility/privacy og recursive kind/all/any.
- **lesson.context-startup-independent-task-cycle** (2026-10-12, major): TaskLocal vernet samme kallkjede, men kildekontroll fant mulig motsatt gate-rekkefølge for to oppstarts-Tasks.
    - forebygging: Serialiser uavhengige røtter før lokale gates og bevar nested scope; test to samtidige røtter i en allerede syklisk fixture.
- **lesson.shared-cellresolver-fixture-unique-names** (2026-10-12, minor): Integrasjon kunne treffe en tidligere emitter selv om nytt registerkall ikke kastet.
    - forebygging: Bruk unike registreringsnavn i sharedInstance-fixtures, og mål actual loadCell/flow mot den nye cellen.
- **lesson.gui-image-number-from-another-source** (2026-11-17, minor): G1-GUI-bildet for dekningsvisningen sa «21 elementer»; den bygde flaten sa 19. Oppdaget i ACCEPT (parity), ikke før.
    - forebygging: Hvert tall i et G1-GUI-bilde regnes av samme kode og samme data som flaten kommer til å bruke, eller merkes som plassholder i §3 med kilden oppgitt. Sammenlign tallene i bildet mot datakilden før bildet sendes til godkjenning.
- **lesson.placeholder-text-in-approved-image** (2026-11-17, minor): Dialogen i det godkjente bildet viste rapportnavnet «coverage/spillverksted-2026-11-09.json»; den bygde flaten viser kjørerens ekte reportRef «playwright/purpose-driver». Avviket måtte godkjennes i ettertid.
    - forebygging: Ingen oppdiktede strenger i et G1-GUI-bilde: bruk den verdien kjøreren faktisk skriver, eller sett «eksempel» synlig i bildet og list strengen i §3 som noe som vil endre seg.
- **lesson.denied-is-thrown-not-returned** (2026-11-17, minor): Negativ test ventet `{"error": "not_authorized"}` fra cellen når en fremmed identitet skrev; testen falt med «caught error: denied(...)» fra GeneralCell.
    - forebygging: Negative tilgangstester bruker do/catch, godtar både kastet `denied` og svarobjekt, og leser tilstanden etterpå for å vise at ingenting endret seg.

## Book 23-noder som kan være forelder/gjenbruk (leksikalsk forslag, verifiser)
- purpose://contact.communication [draft] — Contact and communication
- purpose://event.participation [draft] — Event participation
- purpose://event.privacy-preserving-networking [draft] — Privacy-preserving event networking
- purpose://governance [active] — Governance
- purpose://access.audit.privacy [active] — Access, audit and privacy
- purpose://questionnaire.access.audit [active] — Questionnaire access audit
- purpose://access.audit.privacy.database-key-custody [candidate] — Eierstyrt kryptering og nøkkellagring for celledata

## 5. Avledede tester (samlet)

| Test | Type | Hvordan | Bevis havner |
|---|---|---|---|
| test.cred.roundtrip | command | Utsted medlemsbevis i Swift, verifiser i Swift, Python og Go fra samme fixture | TESTRESULT.md#parity |
| test.cred.tampered | command | Endre `admittedVia`/`validUntil` i fixture; alle tre språk avviser | TESTRESULT.md#parity |
| test.mod.admit | command | Moderator godtar søknad → hvelvet signerer → bevis gyldig | TESTRESULT.md#swift |
| test.mod.scope-negative | command | Moderator prøver `role.issue` for `researcher` → avvist av policy-evaluatoren | TESTRESULT.md#auth |
| test.mod.self-negative | command | Moderator godtar egen søknad → avvist | TESTRESULT.md#auth |
| test.nid.admit | command | Gyldig test-eID-attest → bevis med `admittedVia = national-id:NO` uten moderator | TESTRESULT.md#nid |
| test.nid.untrusted-issuer | command | Attest fra utsteder utenfor TrustedIssuer → avvist | TESTRESULT.md#auth |
| test.nid.no-plaintext | inspection + command | Grep lagret tilstand, logger og journal etter testnummeret etter en kjøring: 0 treff | TESTRESULT.md#nid |
| test.nid.duplicate | command | Samme testnummer fra ny identitet → «allerede medlem» (eller flytting, avhengig av q2) | TESTRESULT.md#nid |
| test.nid.unlinkable | command | Samme nummer i to grupper gir ulike pseudonymer | TESTRESULT.md#nid |
| test.nid.test-issuer-staging-only | command | Prod-konfigurasjon avviser test-utstederen | TESTRESULT.md#auth |
| test.access.matrix | command | Felles fixture `org.membership.access-matrix.json` kjørt i Swift, Python og Go; Swift rapporteres først | TESTRESULT.md#parity |
| test.revoke.status | command | Tilbaketrukket bevis → `revoked` etter ny statusliste | TESTRESULT.md#swift |
| test.revoke.free-pseudonym | command | Etter utmelding: pseudonymet finnes ikke i lagret tilstand; samme nummer kan melde seg inn igjen | TESTRESULT.md#nid |
| test.nid.same-call | inspection + command | Gruppepseudonymet regnes i eID-kallet; subjekt/pid finnes ikke i noe som returneres derfra | TESTRESULT.md#nid |
| test.priv.no-pseudonym-in-credential | command | Utstedt medlemsbevis har ikke pseudonymet | TESTRESULT.md#nid |
| test.priv.consent-first | command | Uten samtykke lagres ingen pseudonym | TESTRESULT.md#nid |
| test.vote.one-per-credential | command | Avstemmingscelle: to identiteter, samme pseudonym → én stemme (bare hvis ja på q6) | TESTRESULT.md#vote |
| test.gui.reference-image-exists | artifact | Bilder per flate og tilstand | images/ |
| test.gui.parity | inspection | Staging-skjermbilde (web + Binding) ved siden av godkjent bilde | ACCEPT.md#parity |
| test.skeleton.purpose-actions-reachable | inspection | `søk`, `godta`, `avvis`, `meld ut`, `trekk tilbake` finnes i reachableActionKeypaths | ACCEPT.md#ways-in |
| test.docs.claims | command | claims.json validerer; nye påstander har kilde med linje | TESTRESULT.md#docs |
| test.docs.no-overclaim | inspection | Ingen tekst sier «én person, én stemme» eller «sybil-sikker» | ACCEPT.md#docs |
| test.build / test.regression | command | Full `swift test` i CellProtocol på Kjetils Mac; Py/Go-suitene | TESTRESULT.md#build |

## 6. Åpne spørsmål til Kjetil

1. **Hvor kommer fødselsnummer-beviset fra i første versjon?** Forslag: CellScaffolds eID-kobling med falsk IdP / test-IdP på staging nå, ekte ID-porten (eller OIDC-megler) når leverandøravtale, klientregistrering og personvernvurdering finnes. Det betyr også et nytt valg: et *stabilt* pseudonym per gruppe ved siden av dagens saltede, som driftsoperatøren kan regne ut. Alternativ: vente på EUDI-lommeboka (OpenID4VP finnes delvis, PID-formatene mangler).
2. **Hva skjer når et nummer som allerede er medlem kommer fra en ny identitet?** Forslag: flytting. Det gamle beviset trekkes tilbake og det nye utstedes, etter fersk eID, og moderator får beskjed. Det dekker tapt telefon. Alternativ: avvis og send til moderator.
3. **Skal beviset si hvilken vei medlemmet kom inn?** Forslag: ja (`admittedVia`), slik at en avstemming kan kreve fødselsnummer-veien mens en chat godtar begge.
4. **Hvem er moderator i Informasjonssystemer?** Forslag: du alene nå, Petter når han er med. Moderatorrollen gis av én eier (samme regel som andre roller).
5. **Skal andre lands eID godtas nå?** Forslag: nei i v1, men nummeret lagres i pseudonymet med landskode (`NO:`), slik at dobbelt statsborgerskap blir en synlig, dokumentert svakhet og ikke en skjult en.
6. **Skal en avstemming telle én stemme per medlemsbevis, som eksempel for studentene (formål 8)?** Forslag: ja, i én avstemmingscelle på staging, med teksten om at moderator-veien fortsatt kan gi to stemmer.

## 7. Revisjonslogg

| Iterasjon | Dato | Hva endret seg |
|---|---|---|
| 1 | 2026-11-24 | Første utkast fra Kjetils melding 12:35Z |
| 2 | 2026-11-24 | Rettet audit: CellScaffold har eID-kobling (falsk IdP, saltet pseudonym, ingen leverandør). 3b gjenbruker den; nye formål 5a (personvern, beviset bærer ikke pseudonymet) og 8 (én stemme per bevis, q6); pseudonym slettes ved utmelding; DPIA, gruppeeid-celle-PDD og manglende gruppeflate lagt i §2; driftsoperatør kan regne pseudonymet lagt i begrensningene. Innspill fra et parallelt utkast (`claude/pdd-gruppebevis-unik-entitet-20261124`), verifisert mot CellScaffold `6e2f667` |
| — | 2026-11-25 | G1 godkjent av Kjetil (08:40Z, «G1 godkjent»). Han svarte ikke på §6 enkeltvis; forslagene i §6 (q1 falsk/test-IdP nå, q2 flytting med beskjed til moderator, q3 `admittedVia`, q4 Kjetil alene som moderator, q5 bare norsk eID med landskode, q6 én stemme per bevis) legges til grunn og kan endres ved G1-GUI |
