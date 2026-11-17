# Formålsspesifikasjon — musikkstatistikk 20260904

Oppgavemappe: `PDD_musikkstatistikk-20260904_2026-09-05` · Opprettet 2026-09-05 · Iterasjon 0 (ikke godkjent)

> Regel: ingen plan før G1 er godkjent av Kjetil. For GUI: ingen implementering før G1-GUI (rendret bilde) er godkjent.
> Et dokument om leveransen teller aldri som leveransen.

## 0. Intensjon (ordrett) og brief-audit

> Vi maa ha et sted vi kan se paa statestikk paa nedlastede laater, om hele laata er spilt etc

Valg tatt av Kjetil 2026-09-05, før dekomponering:
- **Lagring:** per lytter, bak Agreement.
- **Måling:** både «levert» (byte) og «lyttet» (spillerrapportert), holdt fra hverandre.
- **Flate:** Butterpop Studio.

| Påstand i intensjonen / antatt kapabilitet | Audit | Kilde |
|---|---|---|
| Det finnes statistikk å se på i dag | **contradicted** — ingenting telles. `MusicDeliveryToken` har `tokenID, resourceID, storageKey, requesterUUID, issuedAt, expiresAt, credentialID, policyBased` og ingen leseregnskap | `Sources/App/Cells/MusicPublishing/MusicPublishingSupport.swift:444` |
| Serveren kan i det hele tatt vite hvor mye av en låt som er hentet | **retrieved** — hver lyd-lesning går gjennom ett punkt, `readTokenEnvelopeForSubject`, med `offset` og valgfri `length` samt `subjectIdentityUUID` | `Sources/App/Controllers/VaporButterpopStudio.swift:661–690` |
| «Nedlastet» og «spilt» er samme sak | **contradicted** — stream, preview og download er tre separate ressurser med hver sin `resourceID` | `Sources/App/Cells/MusicPublishing/MusicReleasePipeline.swift:475–479` |
| Byte-dekning beviser at noen hørte låta | **contradicted** — nettleseren kan hente hele fila uten at lytteren hører den. Range-håndteringen leverer det klienten ber om, ikke det lytteren konsumerer | `Sources/App/Controllers/VaporButterpopStudio.swift:512–527` |
| Studio har et fanemønster å henge en ny flate på | **retrieved** — `setActiveTab` med `tabIDs`, og fanene rendres av Tabs-bindingen | `Sources/App/Cells/MusicPublishing/MusicWorkspaceReviewCell.swift:644` |
| Agreement-maskineri finnes å feste samtykket i | **retrieved** — `agreementTemplate.addGrant(...)` per keypath, og `WorkspaceCapability` styrer hvem som får lese | `Sources/App/Cells/MusicPublishing/MusicWorkspaceReviewCell.swift:595` |
| Lytteren har en identitet å knytte historikk til | **retrieved** — `playbackIdentity(for:allowAnonymous:)` gir `(listener, cookie, subjectDomain)`; anonyme lyttere får en cookie-basert identitet | `Sources/App/Controllers/VaporButterpopStudio.swift:673` |

**Konsekvensen av «per lytter, bak Agreement», sagt tydelig:** en lytter uten
Agreement skal ikke bli en rad. Ikke en anonymisert rad heller — da er samtykket
pynt. Det betyr at tallene i flaten *systematisk* er lavere enn virkeligheten, og
at flaten må si hvor mye den ikke ser. Ellers leser artisten «12 avspillinger»
som «12 avspillinger totalt» når det kan være 12 av 300. Dette er
`purpose://candidate.musikkstatistikk-20260904.blind-flekk-vises` under, og det
er ikke en detalj som kan utsettes til seinere.

## 1. Formålstre

Rot: `purpose://candidate.musikkstatistikk-20260904.root` — *Artisten skal kunne se
hvordan de publiserte låtene faktisk blir brukt, uten at HAVEN bygger en lytterlogg
noen ikke har sagt ja til.*
Forelder i Book 23: `purpose://access.audit.privacy`.

**To spor, bestemt av Kjetil 2026-09-08.** Anonyme lyttere spørres ikke om noe og
lagres ikke; de bidrar bare til tellere på låta. Innloggede lyttere får en aktiv
samtykke-utfordring, og først da finnes det en rad om dem.

| purposeRef | Tittel | Forelder | Goal (outcome) | Verifier | Status |
|---|---|---|---|---|---|
| `…root` | Bruk synlig, uten overvåking | `purpose://access.audit.privacy` | Artisten kan svare «hvor mye av denne låta blir faktisk hørt» og «hvor mange lastet den ned», og vet hva tallet ikke dekker | Flaten viser begge mål, begge spor og blindflekken | candidate |
| `…anonym-telles-uten-spor` | Anonym: teller, ikke logg | `…root` | En anonym avspilling øker en teller på låta og etterlater **ingen** rad om lytteren — verken identitet, cookie-id, token eller tidsstempel som kan knyttes til én person | Spill av anonymt; dump cellens state og let etter enhver verdi som stammer fra forespørselen → ingen treff | candidate |
| `…anonym-gjennomspilling-uten-pii` | Anonym gjennomspilling, hvis det går rent | `…anonym-telles-uten-spor` | «Spilt gjennom» telles anonymt ved at klienten melder én hendelse ved slutten og serveren øker en andre teller. Korrelasjonen skjer i nettleseren, ikke i lagringen | Spill til slutt anonymt → gjennomspillingstelleren øker; state inneholder fortsatt ingen forespørselsverdier | candidate |
| `…anonyme-tall-er-usikrede` | Anonyme tall merkes som usikrede | `…anonym-gjennomspilling-uten-pii` | Flaten sier at anonyme tellere ikke er autentisert og kan pumpes opp av et skript; de står aldri side om side med innloggede tall uten den merkingen | Inspeksjon: merkingen finnes der tallet står, ikke i en fotnote | candidate |
| `…innlogget-krever-aktivt-ja` | Innlogget: aktivt ja, ellers ingenting | `purpose://questionnaire.delivery.consent` | En innlogget lytter uten signert samtykke behandles nøyaktig som anonym. Samtykket gis ved en aktiv handling i et overlay — ikke forhåndshuket, ikke utledet av at man fortsetter å lytte | Logg inn, avslå, spill av → ingen rad; signer, spill av → rad finnes | candidate |
| `…samtykket-er-en-signert-avtale` | Samtykket lever i en signert Agreement | `…innlogget-krever-aktivt-ja` | Samtykket er en egen, signert Agreement med egne grants — ikke et flagg på brukeren og ikke et valgfritt vilkår i lytteavtalen | Les avtalen: den finnes som eget objekt med signatory og grants; trekkes den, faller radene bort | candidate |
| `…levert-maales-paa-server` | «Levert» måles der bytene går | `…root` | For hver økt vet cellen hvilke byte-områder som er levert, og dermed dekningsgrad 0–100 % | Kjent Range-sekvens → forventet dekning | candidate |
| `…lyttet-rapporteres-av-spilleren` | «Lyttet» rapporteres av spilleren | `…root` | Spilleren melder faktisk avspilt tid og `ended`, lagret som egen størrelse | Spill til slutt → `listenedSeconds` ≈ lengde, `completed=true` | candidate |
| `…to-tall-blandes-aldri` | To mål, aldri slått sammen | `…root` | «Levert» og «lyttet» står hver for seg med sin egen forklaring; ingen avledet «avspillinger» som skjuler kilden | Test som feiler hvis et felt slår dem sammen | candidate |
| `…blind-flekk-vises` | Flaten sier hva den ikke ser | `…root` | Flaten oppgir hvor mange avspillinger som ikke har detaljdata fordi lytteren ikke er innlogget eller ikke har samtykket | 3 med samtykke + 5 uten → «3 med detaljer, 5 bare talt» | candidate |
| `…artisten-ser-bare-fordelinger` | Artisten ser fordelinger, aldri personer | `…root` | Ingen flate, ingen API-respons og ingen eksport gir artisten en enkelt lytters identitet eller historikk — bare aggregater og fordelinger | Negativ test: be om detaljdata som artist → avvist; skann API-responsen for identitetsfelt → ingen | candidate |
| `…nedlasting-er-overfoering` | Nedlasting telles som overføring | `…root` | Nedlastinger telles for seg, merket «filen er hentet» — aldri som lytting | Last ned → nedlastingstelleren øker, lyttetallene står stille | candidate |
| `…lytteren-ser-og-kan-trekke` | Lytteren eier sin egen historikk | `purpose://access.audit.privacy` | Den som har signert kan se hva som er lagret om ham og få det slettet | Trekk samtykke → radene forsvinner, aggregatet justeres | candidate |

## 2. Avgrensning og avhengigheter

Hva dette IKKE er:
- Ikke en anonym besøkslogg. Uten samtykke lagres ingenting om lytteren; anonym bruk blir bare tellere på låta (Kjetil 2026-09-08 og 2026-09-24).
- Ikke en påstand om at noen *hørte* låta når bare byte er levert.
- Ikke geografi, enhet, referrer eller noe annet som ikke er spurt om.
- Ikke en betalingsrapport. Tallene her er bruk, ikke oppgjør.
- Ikke statistikk for private mikser i denne omgangen — kun publiserte låter.
- Ikke anonym *identifisering*: den anonyme telleren skal aldri kunne brukes til
  å skille én lytter fra en annen, heller ikke indirekte.
- Ikke et forsøk på å gjøre anonyme tall pålitelige. De er usikrede, og det står i flaten.
- **Ikke innholdsvern.** Kjetil tok opp 2026-09-09 at det bør være så vanskelig som
  mulig å hente en ukryptert lydfil uten grant på read *og* store. Det er et eget
  formål med egen kjede (levering, nøkler, klient) og skal ha sin egen oppgavemappe.
  Statistikken hverken styrker eller svekker vernet, og de to må ikke slås sammen
  bare fordi begge handler om avspilling.
- **Ikke album.** Album er avklart som metadata med felles cover, der en avtale skal
  kunne dekke settet slik at det kan selges som pakke (Kjetil 2026-09-09). Egen sak.

| Kapabilitet | Kilde | Avgrensning | Må virke før test? |
|---|---|---|---|
| Ett lesepunkt for lyd med offset/length | `VaporButterpopStudio.swift:661–690` | Dekker stream og preview; nedlasting går en annen vei og må håndteres eget | ja |
| Lytteridentitet finnes ved avspilling | `VaporButterpopStudio.swift:673` | Anonyme får cookie-identitet — den er *ikke* et samtykke | ja |
| Agreement per keypath | `MusicWorkspaceReviewCell.swift:595` | Gir tilgang til å lese; samtykke fra lytteren er en annen avtale enn workspace-tilgang | ja |
| Fanemønster i Studio | `MusicWorkspaceReviewCell.swift:644` | Ny fane krever både `tabIDs`, panel og skeleton | ja |
| Persistens for musikk-celler | `MusicPublishingPersistence.persist` | Uten eksplisitt persist overlever ingenting omstart (lærdom fra `revoke` 03.09) | ja |

## 3. Forventningskontrakt — «Det du kommer til å se»

| Leveranse | Type | Hvor | Referanse | Godkjent |
|---|---|---|---|---|
| Fanen «Statistikk» i Butterpop Studio, med låtliste og de to kolonnene | bilde, så kjørende flate | `/butterpop` → fanen Statistikk | `images/statistikk-fylt-v1.png` | nei |
| Samme fane uten data ennå | bilde | — | `images/statistikk-tom-v1.png` | nei |
| Samme fane når mesteparten er utenfor samtykke | bilde | — | `images/statistikk-blindflekk-v1.png` | nei |
| Detalj for én låt: fordeling av hvor langt folk kommer | bilde | — | `images/statistikk-detalj-v1.png` | nei |
| Fanen med alle avspillinger (usikret) øverst, før samtykke-sporet finnes | bilde | `/butterpop` → Statistikk | `images/statistikk-skive1-v2.png` | **ja, Kjetil 2026-09-25 («Ok»)** |
| Samme fane ferdig, med samtykke-delen | bilde | — | `images/statistikk-fylt-v2.png` | **ja, Kjetil 2026-09-25** |
| `MusicListeningStatsCell` med kontrakt og fixtures | fil | `Sources/App/Cells/MusicPublishing/` + `contract/` | — | nei |
| Testutdata for alle rader i §5 | testutdata | `TESTRESULT.md` | — | nei |

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

## Book 23-noder som kan være forelder/gjenbruk (leksikalsk forslag, verifiser)
- purpose://contact.communication [draft] — Contact and communication
- purpose://event.participation [draft] — Event participation
- purpose://event.privacy-preserving-networking [draft] — Privacy-preserving event networking
- purpose://project-work.share-selected-intent [active] — Share selected project intent
- purpose://questionnaire.delivery.consent [active] — Questionnaire delivery and consent
- purpose://governance [active] — Governance
- purpose://access.audit.privacy [active] — Access, audit and privacy
- purpose://questionnaire.access.audit [active] — Questionnaire access audit
## 5. Avledede tester

| test | type | Formål | Hvordan | Hvor havner beviset |
|---|---|---|---|---|
| `test.samtykke.ingen-rad-uten-avtale` | command | `…samtykke-er-porten` | Spill av som lytter uten samtykke; les cellens state | `TESTRESULT.md#samtykke` |
| `test.samtykke.trukket-sletter` | command | `…lytteren-ser-og-kan-trekke` | Samtykk, spill av, trekk samtykke; radene skal være borte | `TESTRESULT.md#samtykke` |
| `test.levert.dekning-stemmer` | command | `…levert-maales-paa-server` | Kjent Range-sekvens → forventet dekningsgrad | `TESTRESULT.md#levert` |
| `test.levert.overlapp-telles-en-gang` | command | `…levert-maales-paa-server` | Be om samme byte-område to ganger → dekning øker ikke | `TESTRESULT.md#levert` |
| `test.lyttet.fullfoert-settes` | command | `…lyttet-rapporteres-av-spilleren` | Spill til `ended` i Playwright → `completed=true` | `TESTRESULT.md#lyttet` |
| `test.lyttet.klienten-kan-ikke-lyve-fritt` | command | `…lyttet-rapporteres-av-spilleren` | Rapporter mer lyttet tid enn låta er lang → avvist | `TESTRESULT.md#lyttet` |
| `test.visning.to-kolonner` | inspection | `…to-tall-blandes-aldri` | Flaten har separate felt; ingen sammenslått «avspillinger» | `ACCEPT.md#parity` |
| `test.visning.blindflekk` | command | `…blind-flekk-vises` | 3 med samtykke + 5 uten → flaten sier 3 talt, 5 utenfor | `TESTRESULT.md#blindflekk` |
| `test.nedlasting.teller-for-seg` | command | `…nedlasting-er-overfoering` | Last ned → nedlastingstall øker, lyttetall står stille | `TESTRESULT.md#nedlasting` |
| `test.gui.parity` | inspection | `pkg.std.gui-surface` | Godkjent bilde mot faktisk skjermbilde | `ACCEPT.md#parity` |
| `test.build` / `test.regression` | command | `pkg.std.everything-works` | `swift build --target App`, full suite | `TESTRESULT.md#build` |

## 6. Åpne spørsmål (bare de som endrer treet)

Besvart av Kjetil 2026-09-08: anonyme spørres ikke og lagres ikke; innloggede får
en aktiv samtykke-utfordring i overlay; artisten ser bare fordelinger.

Igjen å avklare:

1. **Besvart av Kjetil 2026-09-25: 90 dager rådata, deretter bare aggregat** («90 dager ok»). Opprinnelig spørsmål: **Oppbevaringstid for de innloggede radene.** Uten en grense vokser loggen uten
   slutt, og «lytteren kan trekke samtykket» blir det eneste som noen gang sletter
   noe. Forslag: rådata 90 dager, deretter bare aggregat. Endrer
   `…lytteren-ser-og-kan-trekke`.
2. **Besvart av Kjetil 2026-09-24: ja** («Jeg vil fortsatt ha musikk statistikk. Også fra ikke innlogget bruk.») — både start og gjennomspilling telles anonymt, merket usikret. Opprinnelig spørsmål: **Skal den anonyme gjennomspillingstelleren i det hele tatt bygges?** Den kan
   ikke sikres, og et tall som kan pumpes opp av et skript kan gjøre mer skade enn
   nytte når det står ved siden av et ekte tall. Alternativet er å telle bare
   *start* anonymt, og la gjennomspilling være noe bare innloggede bidrar til.
   Endrer `…anonym-gjennomspilling-uten-pii` og `…anonyme-tall-er-usikrede`.

## 7. Iterasjoner

| # | Dato | Hva endret seg |
|---|---|---|
| 0 | 2026-09-05 | Første dekomponering, etter tre valg fra Kjetil (lagring / måling / flate) |
| 1 | 2026-09-08 | Kjetil delte lagringen i to spor: anonyme telles uten å lagres, innloggede får aktiv samtykke-utfordring i overlay, samtykket lever som egen signert Agreement. Artisten ser bare fordelinger. Nye formål: `…anonym-telles-uten-spor`, `…anonym-gjennomspilling-uten-pii`, `…anonyme-tall-er-usikrede`, `…innlogget-krever-aktivt-ja`, `…samtykket-er-en-signert-avtale`, `…artisten-ser-bare-fordelinger`. G1 og G1-GUI godkjent samme dag. |
| 2 | 2026-09-24 | Kjetil: fortsatt ønsket, også fra ikke innlogget bruk → §6.2 ja (anonym start og gjennomspilling telles, merket usikret). Rettet selvmotsigelse i §2 («uten samtykke telles ingenting»). §6.1 (oppbevaringstid) fortsatt åpen. |
| 3 | 2026-09-25 | Kjetil godkjente bilde v2 (G1-GUI for fanen, med anonyme tall merket usikret) og 90 dager oppbevaring (§6.1). Skive 1c (fanen) settes i gang; skive 2 trenger et bilde av samtykke-spørsmålet til lytteren (G1-GUI). |
