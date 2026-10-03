STATUS: LEVERT — flytteplan og lærdomskandidat for alternativ B; WP8-importkontrakt og runtime-prøver gjenstår

# Fra Butler-cellen til PurposeRegistry

Dokumentjobb 2026-09-29, Codex → Losen/b1a. Planen beskriver krav til kommende bygging, ikke en gjennomført migrering.

Kjetil 29.09, ordrett:

> Gjør B) Butler får grafen nå - men ta det som læring for hvordan flytte data så friksjonsløst som mulig - men selvfølgelig i overensstemmelse med cellprotocol og HAVEN - når det er klart.

Alternativ B betyr at Butler får et midlertidig, versjonert scaffold-lager. Registeret er det planlagte varige hjemmet. Kostnaden reduseres nå ved å bevare identitet, felt, rekkefølge og proveniens, og ved å avtale én flyttbar verdi og én felles kontrakttest. Kildebyttet skal ikke endre matcher, beslutninger eller rettigheter.

## 1. Hva vi vet, og hva vi ikke kan love ennå

Bindende grunnlag er [E1-DESIGN](E1-DESIGN.md), særlig v2-kravene som overstyrer den eldre §2-skissen, og [Astras motsvar](E1-ASTRA-MOTSVAR.md). Kjetils B-valg erstatter bare den åpne A/B-beslutningen. T0–T5 i [FORMAALSSPEC](../FORMAALSSPEC.md) og E1–E6 i [PLAN](../PLAN.md) gjelder fortsatt. Tillegget har ingen egen T4-overskrift i den leste filen; ingen ny regel er utledet av det.

Registerets [PLAN, WP8](../../PDD_formaalsregister-som-graf_2026-09-11/PLAN.md) plasserer `cell:///PurposeRegistry` i CellProtocol og navngir `registry.state`, `registry.resolve`, `registry.match` og `registry.taxonomyDigest`, med Explore-kontrakter og eier-scopede Grants. `contract/purpose_registry_contract_v0.json` finnes ikke ved denne kontrollen. Verken import-keypath, versjonslesing, kvittering, transaksjon eller skriverettigheter er dermed en ferdig kontrakt. `registry.state` skal ikke antas skrivbar bare fordi navnet finnes i planen.

[Ref/keypath-notatet](../../PDD_formaalsregister-som-graf_2026-09-11/contract/purposeref-og-keypath.md), særlig de senere svarene i §6, låser: identitet er ikke adresse; gamle punktumrefs står; nye refs bruker `/`; en ref er én komponent i klammeform. Den eldre «fortsatt åpent»-listen i §7 overstyrer ikke svarene. [Forsoningen](../../PDD_formaalsregister-som-graf_2026-09-11/contract/taksonomi-forsoning.md) låser kanter fra erklærte relasjoner, aldri ved splitting på punktum. INN-IA er besluttet som facet, men dens endelige maskinfeltnavn og WP8-importhåndheving er ikke spesifisert i disse filene. Vi finner ikke på et slikt felt i E1.

Book 23-kilden har 58 noder i den lokale dokumentversjonen som ble lest. Registreringsarbeidets historiske 57/78-tellinger er fra en annen kildetilstand. De skal ikke behandles som ferdig forsont innhold. Swift-grunnlaget er CellScaffold `origin/main` ved `adf48d4615d1ed143d5bdc190fcf63e266214c8f`, lest med `git show`. [Kartet](E1-KART.md) skiller uttrekk fra beholdt kode og utsatte områder.

### Lest kildegrunnlag, låst for b1a

Dokumentkildene er lokale dokumentversjoner, ikke påstått publisert main. Hashene under er SHA-256 av kildefilenes bytes; de er ikke grafens JCS-innholdshash.

| Kilde | SHA-256 |
|---|---|
| CellScaffold/Sources/App/Support/ChatPurposeResourceRouter.swift på kode-SHA over | 49ac835408ef6f3ddd5c4f4dec775462f42358726114b98cce6a8d5aefbd746b |
| CellScaffold/Sources/App/Cells/PersonalCopilot/PersonalCopilotCloudStore.swift på kode-SHA over | 7f93ae3f6f89188ea7c577248c236d0c5f2018d525a307d4eb52f6750a92d222 |
| CellScaffold/Sources/App/Support/PurposeKnowledgeBase.swift på kode-SHA over | f707b7865d5dbd8d58cdc496146fce838c3e11cb45c7eb5da3206e362f5f90ae |
| CellProtocolDocuments/Book/haven_purpose_knowledge_base_v0.json | 85ffe284123ae312c3a50e3867be081f8ff4c2b73bc7197fb406a0024b177037 |
| CellProtocolDocuments/Book/haven_purpose_composition_v0.schema.json | 2844650be82fb29b5d1987f80f6d8517d6c2288022eb02dc65816a5583384804 |

b1a må kontrollere disse før uttrekk og dokumentere kildeendringer som ny baseline. Skjemaet beholder de brukte node-/komposisjonsdefinisjonene fra Book-skjemaet. Lokale endringer i en navngitt kildefil skal ikke stilltiende bli del av startgrafen.

**Grensen for løftet:** Formatet her er et konkret forslag som b1a kan bygge Butler mot. WP8 må vedta og bestå samme kontrakt før registeret kan overta. Vi har ikke fått eller målt en ferdig registerimplementasjons aksept. Hvis WP8 ikke kan lagre og returnere verdien uendret, stopper flyttingen. Det innføres ikke en skjult konverterer for å få grønn status.

## 2. Den flyttbare verdien

[JSON-skjemaet](../contract/butler_purpose_graph_v1.schema.json) definerer denne konvolutten:

```text
schema = haven.butler-purpose-graph.v1
contentHash = sha256:<64 små heksadesimale tegn>
content
  knowledgeBase                 hele Book/register-snapshotet
    schema = haven.purpose-knowledge-base.v0
    rootPurposeRef, nodes, sourceRefs, øvrige Book-felt
  consumerFacets
    butler                      navngitt konsumentfasett
      facetID = haven.butler-routing.v1
      runtimeContract
      lexicon                   ordnet, stabile entryID-er
      router.specialRules       faste, typede felt
      helpers                   faste, typede felt
      thresholds, baseWeights, scoring
  provenance
    sourceCommit
    sourceArtifacts             relative stier og kildefilhash
```

`knowledgeBase` beholder Book-feltene på deres faktiske plass: `purposeRef`, `parentRef`, `title`, `summary`, `status`, `goal.goalRef/lifecycle/outcome/successSignals/verifier`, `matchingHints.aliases/tokens`, eventuelle `aliases`, `interests`, `capabilityHints`, `facetRefs`, `composition` og `childOrder`. `sourceRefs` beholder `id`, `path` eller `url`, `domain` når oppgitt, `status`, `checkedAt` og `appliesTo`. Historisk kontrolltid er kildeproveniens, ikke importtid. Relativ `path` tolkes i sitt dokumenterte kilde-repo; den omskrives ikke ved overføring. Importkvitteringen oppgir kilde-repo separat.

Nodene kan gis direkte til registerets node-leser fordi objektet ikke flates ut eller får nye feltnavn. WP8 må bevare Book-utvidelser og versjonere tolkningen av dem. Den komplette Book-konvolutten bevares også, inklusive `schemaRef`, `facets`, `compatibility`, `nodeDefaults` og øvrige kildemetadata. Indeksbygging på mottakersiden er tillatt; indeksen er avledet og inngår ikke i overført innhold eller innholdshash.

Butler-fasetten er adskilt fra semantiske `facetRefs`. Ruterfraser er ikke Book-aliaser; endpointHints og resourceHints er ikke én capabilityHints-liste. De 27 ruterrefs bevares, også de eldre strengene uten `purpose://`. De er konsument-ID-er under Butler-fasetten, ikke automatisk nye registernoder. Ingen omdøping eller «smart» kobling mellom dem og Book 23 skjer i E1. Manglende kanoniske noder er forsoningsarbeid, ikke en anledning til å finne opp parentRef eller Goal.

Skjemaets faste navn definerer dataspor, ikke en regeltolker. Operasjon, målflate, fase, første treff og normalisering står i kode. Nye plasser krever ny avtalt skjema-/runtimekontrakt; nye fraser og tall i eksisterende plasser krever ny innholdshash, evaluering og godkjenning. `examples` i skjemaet angir startverdier fra kildekoden og fylles ikke inn som runtime-defaults.

### Innholdshash

Den normative hash-inputen er nøyaktig objektet `{"schema": document.schema, "content": document.content}`. Det serialiseres med JCS, kodes i UTF-8 uten BOM eller avsluttende linjeskift og hashes med SHA-256. Resultatet skrives `sha256:` + 64 små heksadesimale tegn. Objektfelter sorteres etter JCS; array-rekkefølge og Unicode-strenger bevares. Dupliserte feltnavn, ugyldig Unicode, NaN og uendelig avvises. Numerisk serialisering følger JCS' binary64-regler, ikke plattformens tilfeldige JSON-format. Ingen normalisering, defaultinnsetting eller sortering av leksikon/tokengrupper skjer før hashing. [RFC 8785 §§3.1–3.2](https://www.rfc-editor.org/rfc/rfc8785).

Alt under `content` inngår: alle noder og deres proveniens, konsumentparametre, alle ordnede lister, kildecommit og predicate/evaluator/catalog-kontraktversjon. Bare rotfeltet `contentHash` utelates. Det gir ingen selvrefererende hash. Skjemafilen og dens dependencies låses med egne filhasher i målemanifestet; `sourceArtifacts` skal vise kildedata og kode, ikke hash av dokumentet som inneholder listen selv.

Pekere, miljøets løste endepunkter, godkjenninger, målerapporter, importkvitteringer, tidsmålinger og revisjonslogg ligger **utenfor** dette uforanderlige dokumentet. De bindes til dokumentets hash. Flytting mellom celler eller miljøer endrer derfor ikke grafhashen; miljøets autorisasjon og historikk blir ikke kopiert med den. Endret node eller kommentar-/proveniensfelt inne i `content` er derimot nytt innhold og får ny hash.

Registerets `registry.taxonomyDigest` er ikke uten videre denne hashen: WP8 kan definere en digest av bare taksonomien. Da må mottaket i tillegg eksponere og kvittere den uendrede **grafens** contentHash. Lik taksonomidigest alene beviser ikke lik Butler-fasett.

## 3. Explore-kontrakter før transport

Alle keypaths i tabellen som begynner med `graph.` eller `source.` er **foreslåtte b1a-kontrakter**, ikke observerte API-er. Endelige register-keypaths velges av WP8 og oppdages/verifiseres via Explore. Ingen keypath gjøres skrivbar gjennom dette dokumentet.

| Operasjon | Foreslått kontrakt / krav | Rettighet og resultat |
|---|---|---|
| Les Butler-versjon | GET `graph.versions[<contentHash>]`, returnerer hele konvolutten uendret; GET `graph.state` for tilgjengelige versjoner | Requester-scoped lesing; hash som én opak komponent. Ikke les intern database eller eksportfil. |
| Legg inn Butler-versjon | SET `graph.versions.import`, input eksakt konvolutt | Egen opplastingsrett; validering, hashkontroll, uforanderlig lagring og kvittering. Idempotent ved samme hash/innhold. |
| Nominer kandidat | SET `graph.candidate.compareAndSwap` | Egen nomineringsrett; identifisert ny hash, forventet kandidatpeker/revisjon; aktiverer ingenting. |
| Evaluer | Eksplisitt snapshot inn i ren evaluator, resultat bundet til inputmanifest | Egen evalueringsrett der det kreves lesing; ingen skriverett følger av den. |
| Importer til register | WP8s egen Explore-annonserte SET-kontrakt, input samme konvolutt | Eier-scopet Grant for nøyaktig mottaker, keypath, metode og dataklasse; staging/validering før publisering som uforanderlig versjon. |
| Les tilbake fra register | WP8s kontrakt for hashadressert versjonslesing | Hele samme innhold, ikke bare count, sammendrag eller taxonomyDigest. |
| Bytt aktiv kilde | SET `source.compareAndSwap` på stabilt eierstyrt kontrollpunkt | Egen promoteringsrett + godkjenning og rapportbinding; se §5. |
| Rull tilbake | Egen rollback-overgang over samme kildepeker | Bare identifisert tidligere godkjent, ikke tilbakekalt hash/kilde med kompatibel runtime. |

Hver operasjon må ha metode, input, returns, permissions, navngitte feil og flowEffects i Explore. En legacy methodless schemaDescription beviser ikke både GET og SET. Kontraktene følger [Book 22](../../../Book/22_Explore_Contracts_For_Skeleton_Authoring.md); JSON Schema alene er ikke en Explore-kontrakt og gir ingen tilgang.

Skriving og persistens kontrolleres gjennom registerets egne keypaths og Grants med requesterens faktiske bevis. Et rollenavn eller `entity:digipomps` i en streng er ikke autorisasjon. Lesing, lagring og eventuell utlevering er separate rettigheter; ikke utled videresendingsrett fra lagringsrett. Match/resolve-resultater gir aldri en Grant.

En autorisert migreringskoordinator binder en versjonslesing fra Butler til registerets importoperasjon gjennom CellProtocol-resolveren. Den kan videreføre den typede verdien i minne/flow, men skal ikke ha en filkopi, direkte databasevei eller annen sidekanal som alternativ. Bridge/transport frakter verdien; cellene eier semantikk og adgangskontroll. Explore er oppdagelse av kontrakt, ikke bevis på at requester har lov til å kalle den.

## 4. Flyttetrinn og feiltilfeller

1. **Lås kontrakten.** b1a og WP8 bruker samme skjema, hash-regel og fixture-pakke. Kartets SHA, nodekildens filhash, predikat-/evaluatorversjon, katalogbinding, miljø og skjemadependencies bindes i manifestet. Ukjent versjon eller uløst INN-IA-/komposisjonssemantikk avvises før import/aktivering.
2. **Fest kilde.** Les gjeldende kildepeker og revisjon; hent nøyaktig hashversjon fra Butler via Explore-kontraktert GET. Verifiser hash lokalt. En endret aktiv/kandidatpeker endrer ikke verdien som allerede er festet.
3. **Importer som uforanderlig versjon.** Kall registerets egen import-keypath med samme konvolutt. Registeret verifiserer hash og alle felt før versjonen blir lesbar. Delvis mottak eller avbrudd må aldri bli en aktiv graf. Retry med samme hash er idempotent; påstått lik hash med ulikt innhold avvises.
4. **Bevar identitet uten sammenslåing.** Registeret beholder `purposeRef`, nodeobjekter, rekkefølger, kildeproveniens og konsumentfasett uendret. Kollisjon med eksisterende kanonisk nodeinnhold løses ikke med overwrite/merge. WP8 må kunne holde denne uforanderlige registerversjonen isolert frem til godkjent valg. Kan det ikke det, er porten rød. En senere forsoning er en egen innholdsendring med ny hash og egen beslutning.
5. **Les tilbake og mål før bytte.** Hent samme hash fra registeret gjennom dets lesekontrakt. Krev samme kanoniske innhold, samme ID-er og samme grafhash. Kjør felles kontrakttest og full semantisk differanse over Butler-snapshot og register-snapshot med identiske eksplisitte input. Registerets interne indeks er ikke bevis nok.
6. **Bytt én peker.** Etter grønn rapport og gyldig godkjenning utføres compare-and-swap på kontrollpunktet i §5. Ingen kodeutrulling eller midlertidig global kandidatinstallasjon skal være nødvendig for kildebyttet.
7. **Mål etter bytte.** Nye analyser skal rapportere ny kildepekerrevisjon og samme forventede grafhash; pågående analyser fullfører sitt gamle festede snapshot. Kjør samme semantiske prøve mot den faktiske leserveien etter byttet. Avvik eller manglende rader gir rød port og autorisert rollback, ikke «ingen treff».
8. **Avslutt midlertidig eierskap.** Registeret er etter overtakelsen eneste aktive skriver for nye grafversjoner. Butler-beholdningen beholdes uforanderlig og lesbar så lenge godkjent rollback krever det, uten toveis synk eller to konkurrerende aktive grafer. Sletting/retensjon avgjøres separat etter verifisert overtakelse; denne jobben autoriserer ingen sletting.

WP8 trenger en definert atomisk import-/publiseringsgrense. Det er ikke dokumentert at en slik finnes nå. Ved timeout må koordinatoren kunne spørre etter hash/kvittering og fastslå om importen ble fullført før nytt forsøk. Ingen distribuert transaksjon antas: først uforanderlig import, deretter verifisering, så ett CAS-bytte er nok når hvert trinn er idempotent og feiler lukket.

## 5. Én kildepeker, én analyseversjon, reversibelt bytte

Butler skal lese gjennom ett stabilt kontrollpunkt. Aktiv kilde er **én atomisk post** med `sourceCellRef`, `readContractRef`, `contentHash` og monotont `revision`. ReadContractRef identifiserer den Explore-verifiserte lesekontrakten; celleref velger kilde, hash velger uforanderlig innhold. Før flytting peker posten på Butler-cellen, etterpå på `cell:///PurposeRegistry`. Ingen andre kodeveier skal følge en skjult «active» hos hver kilde. Kandidatpekeren er separat og kan ikke påvirke aktive analyser.

CAS må sammenligne hele forventet gammel post/revisjon, ikke bare hash: under selve flyttingen er gammel og ny **innholdshash lik**, men kilden er forskjellig. Ellers oppdages ikke konkurrerende kildebytter eller ABA. Ved vanlig grafpromotering endres også hashen. Godkjenningen binder gammel og ny post, rapporthash, runtime, katalog og miljø. «Aktiver nåværende kandidat» er ikke en gyldig godkjenningsbinding.

Tilbakerulling er ett CAS-bytte til en eksplisitt tidligere godkjent kilde/hash som ikke er tilbakekalt og som fortsatt kan leses med gyldige Grants. Rollback peker til identifisert historikkpost, ikke vekselvis «forrige aktiv» som kan peke tilbake til feilen. Det har egen rettighet og revisjonskvittering. At en gammel hash har vært aktiv, gjør den ikke automatisk gyldig igjen.

Hele analyzeDraft fester posten og det validerte snapshotet før første await. Alle ruter-/hjelperkall, rerutinger og forslag bruker dette samme objektet; ingen getter leser global active på nytt midt i analysen. Nye analyser ser ny revisjon etter byttet. Et bevisst festet gammelt snapshot fullfører lovlig; blanding av to versjoner i ett forslag er feil.

Pekerhendelser har revisjon og forventet hash; de er varsling om varig tilstand. Klienten tåler duplikater, forsinkelse og feil rekkefølge, laster kontrollpunktet ved oppstart/gjenkobling og ved revisjonsgap, og validerer innhold før cache installeres atomisk. «Ingen polling» er ikke et argument for manglende gjenoppretting. Ved utilgjengelig ny kilde blir aktiveringen ikke halvveis gjeldende: behold dokumentert siste gyldige snapshot etter fastsatt policy eller returner eksplisitt utilgjengelig; ingen stille fallback til innebygde literaler.

## 6. Én felles kontrakttest og semantisk port

Foreslått felles fixture-kontrakt: `test.butler-purpose-graph.transfer-v1`. b1a implementerer den én gang med kontraktadaptere; Butler-cellen og WP8-registeret kjører **samme** fixture-pakke og forventede resultater. Det er testadaptere for samme celleoperasjoner, ikke ekstra produksjonsmatchere. Før WP8 finnes kan bare Butler-siden kjøres; det gir ingen påstand om registerparitet.

| Prøve | Krav til begge celler / måleport |
|---|---|
| Import → read-back | Uendret nodeobjekt og proveniens, ordnet leksikon og identisk contentHash; samme ref er samme identitet. Mottakers indeks må ikke omskrive payload. |
| Hashvektorer | Låste JCS-bytes og forventet SHA-256 for representativ graf; objektfelters inputrekkefølge påvirker ikke hash; endret listeorden, score, kildecommit eller predikatversjon gjør det. Unicode og tallgrensevektorer inngår. |
| Import avvist | Manglende/duplisert entryID, tom tokengruppe eller frase, ukjent plass/binding, ugyldig/ikke-endelig tall, feil hash, ukjent runtimeversjon og ødelagte nodekanter. Ingen halvversjon blir synlig. |
| Rettigheter | Uautorisert import, nominering, evaluering med private input, promotering og rollback avvises separat. Lesetilgang er ikke skriverett. Match/facet kan ikke brukes som autorisasjon. |
| Retry/kollisjon | Samme hash og innhold er idempotent; annen verdi under samme påståtte hash og motstridende kanonisk node avvises. Timeout/restart kan avklares via varig kvittering. |
| CAS | Gammel revisjon, gammel kilde eller gammel hash som ikke stemmer, avvises. Rapport for A kan ikke brukes etter at kandidat er byttet til B. Lik hash med annet sourceCellRef omfattes også. |
| Samtidighet og cache | Bytte mellom await-punkter gir aldri blandet snapshot; konkurrerende kandidat/aktiv-bytte, duplisert/tapt hendelse, forsinket cache og omstart er prøvd. |
| Rollback | Tidligere godkjent identifisert hash/kilde virker; tilbakekalt eller inkompatibel versjon avvises; rettigheter og rapportbinding bevares. |

**Semantisk projeksjon, ikke fillikhet:** sammenlign hele beslutningsstrukturen: alle ressurs- og intent-kandidater i rekkefølge, purposeRefs, rå- og vektede scorer uten avrunding, scorebidrag, terskel-/vernutfall, actionability/speechAct, støttet status, tilgjengelighet, endelig valg/avklaring, stabile actionID-er, mål-endepunkt og keypath, risiko, forklaring og komplette utkast med alle beslutningsrelevante felt. Ingen top-5-avkorting eller erstatning av dype objekter med størrelser. Ukjente utdatafelt gir rød port til projeksjonen er vurdert.

Utelat bare dokumenterte flyktige felter: tilfeldig genererte analyse-/forslagsidentifikatorer, tidsstempler og målt kjøretid. Kryssreferanser til flyktige identifikatorer erstattes konsistent med fixture-lokale navn; stabile handlings-/ressurs-ID-er bevares. Kildepekerrevisjon og fysisk lageradresse verifiseres som forventet migreringsproveniens, men skal ikke gi falsk beslutningsdifferanse. Ved literal→celle får E1 nytt hash-/regelspor som baseline ikke har: sammenlign gammel beslutning uendret og valider det nye sporet separat. Ved celle→register skal både grafhash og treffende regel-ID-er være like.

Porten fryser før målingen: baseline-commit, eventuell patchhash, datahash, skjema/dependencies, predikat-/evaluatorversjon, katalog og requester-synlige ressurser, locale/miljøbindinger, kontekst, trådtilstand, personlige inputvekter, harness, korpus/fasit og beslutningsregel. Et visningsnavn som «graf v3.1» erstatter ikke dette. For E1/flytting er regelen **null semantiske avvik**, ikke bare samme aggregate treffprosent.

Prøvesettet omfatter korpus v1/v2 og PromptPurposeLab, også setup-/kontekstsaker, samt:

- Grenmatrise S01–S11 og P01/P02: eksakt vs generisk, konkurrerende flater, tillegg før gulv, tak, samme melding med flere treff, og kontekstboost etter tak.
- Hjelperoverlapp: schedule meeting, todo list, ideens lokale no-idea-unntak, invitasjonsregex på originaltekst, poll som helt token, onboardings lokale veto, agentkatalogens manglende descriptor og moderation uten nytt vern.
- Læring av/på med gamle hendelser, samme/annen/ingen tråd, null historikk og klamping. Læring av betyr ikke nødvendigvis basisvekt.
- Tersklene eksakt og på hver side, inkludert toleransen 0,02 med dens strenge `<`, kandidatminimum 0,50 og direkte ressursgrense 0,82.
- Tom/ready/utilgjengelig Perspective-projeksjon, eksakte refs og tokenoverlapp, null/ulike vekter, requester uten tilgang og negative utsagn.
- Samtidighets- og gjenopprettingsprøvene i tabellen over, før og etter det faktiske pekerbyttet.

Porten feiler lukket ved tomt testsett, hoppet over eller ugyldig korpusrad, mismatch i forventet antall, analysefeil, timeout, feil kilde/hash/katalog, røde regresjoner, ukjent beslutningsfelt eller manglende etterprøve. Rapporteksistens alene gir aldri grønt. Lås kriteriene før tall sees, slik [kapittel 38](../../../Book/38_Measuring_Purpose_Understanding_Without_A_Model.md) krever. Den gamle målejobbens «LEVERT» ved røde tester kan ikke brukes som akseptansebevis.

E2 bruker en **ren evaluator** med eksplisitte input og tidsbudsjett. Ingen modellkall, handling, chatlogg, læring eller annen lagring; kandidatfeil rapporteres som manglende måling. To kall til analyzeDraft er ikke skygge. E1 må fra forslaget blir laget bære grafhash, regel-ID-er og evaluatorversjon. E3 skiller vist forslag, alternativer og utfall. Kandidaten er ikke vist, og får derfor ikke et oppdiktet aksept-/avvisningsutfall. E6 definerer senere kvalitetsport; E1s likhetsprøve beviser ingen kvalitetsforbedring.

## 7. Eierskap og samtykke følger dataene

Grafens erklærte noder, leksikon, basisvekter og koeffisienter er scaffold-data. Personlige vekter, utfall, læringshendelser, meldinger og Perspective-kanter tilhører entiteten og er ikke med i grafpayload eller flytterapport. En scaffold-administrator kan ikke samtykke på andre entiteters vegne. Dette gjelder også tellinger eller «anonymiserte» data.

T-reglene gir nivå 0 som standard for utlevering: ingenting forlater entiteten. Nivå 1 gjelder samtykkede tellinger per formål/versjon, uten tekst. Nivå 2 gjelder i tillegg vaskede meldinger som eieren har sett og godkjent. Tilbaketrekking stopper neste eksport. Grafmigreringen hverken oppretter, utvider eller flytter et slikt samtykke. En eventuell flytting av entitetens eget lager krever separat, formålsbundet samtykke og Grants for kilde, mottaker, omfang og sletting; den er ikke del av E1.

[Læring uten profil §4](../../PDD_formaalsregister-som-graf_2026-09-11/contract/laering-uten-profil.md) presiserer at læring bygger på det eieren eksplisitt erklærer eller lenker til. Passiv tid, klikkfravær og taushet blir ikke læringsbelegg. En rotlenke er eierens bevisste handling; å importere `purpose://root` som scaffold-node oppretter ingen lenke i noe personlig perspektiv.

T0 sier skygge på egne data på som standard, med av-bryter; det er ikke samtykke til utlevering og ikke tillatelse til atferdsprofilering. De planlagte utfallene «annet valg», «skrev om» og «intet svar» må i E2/E3 avklares mot §4 før de brukes til læring. Eksponering kan registreres for evaluering under eierens regler; inferert hensikt skal ikke fremstilles som eksplisitt dom. E1 bevarer dagens beslutninger og lager ikke en ny slik læringsmekanisme.

Registeret tar over scaffold-grafen, ikke private læringsdata eller brukerprofiler. Schema-validering beviser ikke at fritekst er fri for persondata; importpublisering trenger en separat innholdskontroll. Offentlige fixtures bruker bare syntetisk, ikke personidentifiserende materiale.

## 8. Hva som gjøres nå, og hva som venter

| Nå, i b1a | Venter på WP8 / senere arbeid |
|---|---|
| Implementer skjemaet og 371 typede plasser etter kartet; behold K01–K18 og merk U01–U04. | Registerets faktiske import-/read-back-keypaths, Explore-kontrakter, Grants og atomisk persistens. |
| Bruk uendrede Book-noder og kildeproveniens som snapshot; behold Butler-fasett separat. | WP1/WP2-forsoning, endelig INN-IA-felt og håndheving; ingen automatisk oppgradering av snapshot til ny kanonisk taksonomi. |
| Innfør JCS/hash, uforanderlige versjoner, schema/runtime-binding og én festet analyseversjon. | Felles fixture-pakke kjørt mot ekte register; endelig avtale om hele grafens hash vs taxonomyDigest. |
| Bygg én kildepeker med CAS og egne rettigheter; start med Butler som kilde. | Verifisert flytting, godkjent kildebytte og rollback mellom begge celler. |
| Skriv felles kontrakttest, hashvektorer, semantisk projeksjon, negative importer og likhetsport. | Registerets del av testene, krysscellefeil og omstart; ingen påstand om bestått WP8 før dette. |
| Bær versjons-/regelproveniens fra forslaget blir laget; design evaluator som ren funksjon. | E2/E3 hendelser/skygge, E4 samtykke og E6 godkjent kvalitetsport. |

b1a kan gjøre uttrekket billig uten å velge ny motor. Ingen DSL innføres og ingen WP4-/WP19-leveranse erklæres ferdig ved å skifte lager. Registerarbeidet trenger denne konvolutten og fixture-kontrakten før det låser WP8; Losen er integrasjonspunktet for den avtalen.

## 9. Slik flytter vi data mellom celler

**Lærdomskandidat for METODE.md — foreslått metode, ennå ikke bekreftet av en gjennomført E1-flytting:** Avtal den minste uforanderlige verdien som begge celler kan lese uten omforming. Skill dens identitet og innholdshash fra hvor den lagres, hvem som får lese den og hvilken versjon som er aktiv. Bevar de opprinnelige feltene, ID-ene og proveniensen; legg forbrukerspesifikke data i navngitte fasetter. Gjør import gjennom mottakerens egne Explore-kontrakter og Grants, og les tilbake gjennom de samme offentlige cellegrensene. En direkte fil-/databasekopi er ikke bevis på en fungerende cellekontrakt.

La begge cellene bestå samme kontrakttest. Flytt først en uforanderlig versjon, bevis samme hash og semantikk, og bytt deretter én versjonert kildepeker med compare-and-swap. Hold godkjenning, rapport og tilbakerulling bundet til eksakt innhold, gammel/ny peker og miljø. Gjenoppretting etter timeout, tapte hendelser og omstart er en del av flyttingen. Persondata følger sitt eierskap og samtykke, aldri bare den tekniske pakken.

Er det nødvendig å endre dataformen, er dette en egen dataversjon og transformasjon som må vurderes og testes før kildebytte. Ikke kall den samme flyttingen eller behold gammel hash. I E1 er fravær av transformasjon et krav: en inkompatibel mottaker gir stopp, ikke en adapter som skjuler forskjellen.

**Verifisert læring fra kartleggingen:** (1) en liste kan ha semantisk orden selv uten et order-felt; her påvirker filtrert orden både score og formålslås; (2) kildekoden inneholder miljøavhengige endepunktkall som ikke kan fryses til portable adressestrenger; (3) like feltbegreper i Book og runtime er ikke samme struktur eller normalisering. Dette er statiske funn, ikke målt migreringsgevinst.

Læringsruting ble kjørt med `CellScaffold/scripts/haven_learn.py route` og pekte blant annet på PDD-, samarbeids- og kontrakttest-skillene. Lærdommen er plassert her, i dokumentet b1a/WP8 skal lese, innenfor oppdragets uttrykkelige grense «bare dokumenter i PDD-mappen». Ingen felles ledger, skill, METODE.md eller distribusjonsartefakt utenfor de fire leveransene er endret; capture/sync er ikke rapportert som utført. Losen kan etter reell migrering føre validert metode videre gjennom vanlig læringsfangst. Unngå å registrere denne planen som implementert praksis.

## 10. Åpne usikkerheter og stoppunkter

- WP8s endelige JSON-kontrakt finnes ikke. Nodelesing uten feltomforming er et designkrav, ikke bekreftet runtime-kompatibilitet. Registeret må uttrykkelig adoptere konsumentfasetten og hashbevarende read-back.
- Forsont kilde og dagens Book/runtime er ulike. Det er uavklart når registeret kan godkjenne denne Book-versjonen som aktiv taksonomi. Arkivering av uendret snapshot er ikke stille kanonisering.
- INN-IA-feltets maskinform og registerets behandling av ukjente Book-utvidelser må låses. Skjemaet bevarer felt, men avgjør ikke deres autorisasjonssemantikk.
- Den konkrete kildepekerens eiercelle og varige CAS-mekanisme må velges i b1a. Det må være ett kontrollpunkt som overlever flyttingen, ikke pekere i begge lagre som konkurrerer.
- Ytelse, størrelsesgrenser, importbudsjett og cachehendelser er ikke målt. Begge cellene må vedta samme grenser før testene fryses; for lavt budsjett gir eksplisitt feil, ikke ufullstendig graf.
- Gamle læringsvekter brukes selv med læring av. Endring av dette eller tolkningen av observerte utfall er separat arbeid; en «forbedring» under migreringen ville bryte likhetskravet.
- a02/a05/a06 er E2+-innspill som beskrevet i kartet. Kildebyttet gir ikke ny setningsdekomponering eller håndtering av flere behov.
