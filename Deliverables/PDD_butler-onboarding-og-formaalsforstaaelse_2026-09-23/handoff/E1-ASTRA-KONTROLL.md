STATUS: LEVERT — anbefaling: ikke merge, 4 funn (3 blokkerer)

# Astra — E1-kontroll av kart, format og flytteplan

Kontrolldato: 2026-09-29. **E1-BYGG er STOPPET.** Denne rapporten vurderer derfor bare dokumentgrunnlaget, slik oppdraget bestemmer. Den er ikke en kodegodkjenning. Antallet i statuslinjen gjelder blokkeringer for E1-merge; E1-K4 er en separat port før registerflytting.

**Konklusjon:** Alternativ B er fortsatt en forsvarlig retning. Kartet og formatet har fjernet den foreslåtte regeltolkeren og bevart viktige semantiske skiller. Flytteplanen er prinsipielt i samsvar med CellProtocol og HAVENs samtykkekrav. Men ingen E1-celle eller semantisk differanse er levert, og planen mangler en fullstendig kontrakt for varig aktivering og oppdatering av leserne. Ett pekerbytte er en mulig avsluttende operasjon etter forberedelser; det er ikke en dokumentert egenskap ved dagens løsning.

## Lesegrunnlag og bevisgrense

Lest: hele E1-ASTRA-MOTSVAR, E1-DESIGN med v3-statuslinjen, E1-KART, JSON-skjemaet, E1-MIGRERING-TIL-REGISTER og E1-BYGG. Skjemaets definisjoner, parameterverdier og metadata er også lest strukturert med Python. Supplerende dokumentutdrag er angitt nedenfor.

E1-BYGG:1,5,24,58,72–81 oppgir kapasitetsstopp, avbrutt baselinebygg, ingen implementasjon, ingen kjørte E1-tester og ingen PR. Dermed finnes **ingen PR-head-SHA å kontrollere i denne leveransen**. `adf48d4615d1ed143d5bdc190fcf63e266214c8f` er kartets kildebaseline og byggforsøkets HEAD, ikke en levert E1-PR. `fdf1ce8e1713ac467ebca1e44707225175e72dc4` er den senere hentede main-revisjonen som byggnotatet omtaler.

**Ikke lest:** Swift-implementasjon, Swift-testkilder, PR-diff, CI eller staging i denne kontrollen; E1-BYGG peker ikke på noen E1-PR. Måleskriptet og byggloggene er heller ikke lest på nytt. Opplysninger om dem nedenfor tilskrives E1-BYGG, ikke egen kjøring. Ingen utsjekkede Swift-filer er brukt som kodebelegg. Eldre Swift-henvisninger i kart/motsvar er dokumentenes kildehenvisninger, ikke selvstendig reviderte linjer her.

Dokumentene er lokale versjoner, ikke påstått publisert main. SHA-256 ved kontrollen:

| Fil, relativt til denne PDD-mappen | SHA-256 av filbytes |
|---|---|
| `handoff/E1-ASTRA-MOTSVAR.md` | `56117a09aa047347540f467a504e0c6b9c0417e9fbc436c62a20cf4a54d328ca` |
| `handoff/E1-DESIGN.md` | `118c442ea2ce43c4e284aa12da6258123f23f5252305f4409990da650c09916c` |
| `handoff/E1-KART.md` | `a1e236305eaaebfc0a2b5062d84c4b66067a8e0bc6e7c5b7df8304c8c5fd4c6b` |
| `contract/butler_purpose_graph_v1.schema.json` | `03f26dbfbae1eb3c39b95fdd2587391ca989ce9595d5cbe5715bacce00080c57` |
| `handoff/E1-MIGRERING-TIL-REGISTER.md` | `22cde924c2ffdffbb47c874efbd7d2ec2883b204d43d5a01ae5458afd1f70a18` |
| `handoff/E1-BYGG.md` | `e16a1fbb1dd2e9ff84da0696d1993c6e0b344146a41d5cb8a7f33503d2356192` |

Forkortelser nedenfor: **M** = [E1-MIGRERING-TIL-REGISTER.md](E1-MIGRERING-TIL-REGISTER.md), **K** = [E1-KART.md](E1-KART.md), **S** = [butler_purpose_graph_v1.schema.json](../contract/butler_purpose_graph_v1.schema.json). Tall etter kolon er linjer i disse dokumentversjonene.

## 1. De sju kravene

Kravene er hentet fra E1-ASTRA-MOTSVAR:114–120. «Oppfylt på dokumentnivå» betyr at den tidligere designinnvendingen er besvart, ikke at implementasjonen er verifisert. Ingen av de sju er bevist i en levert celle.

| Krav | Vurdering og fil:linje | Ville testene fanget et brudd? |
|---|---|---|
| **1. Typede plasser og uendret kontrollflyt** | **Oppfylt på dokumentnivå for det avgrensede uttrekket.** K:19,85–111 kartlegger alle 17 funksjonene; 15 får plasser, mens `agentActionMatch` og signaladapteren står over samlet. K:326–358 bevarer kodekontrakter og krever før/etter-kallgraf. S:515–3184 har lukkede hjelperobjekter. | Ingen leverte E1-runtimeprøver. De planlagte overlappsprøvene i M:151 vil skille første treff fra maksimum og lokale fra globale veto. Kallgrafkontroll trengs i tillegg: fravær av literaler beviser ikke fravær av en ekstra matcher. |
| **2. Registereierskap, tapsfri fasett og refs** | **Besvart i tråd med Kjetils B-valg, med åpen WP8-port.** Midlertidig Butler-lager er nå autorisert; opprinnelig krav om registereierskap fra første dag skal ikke brukes til å omgjøre dette. K:23,57,61 og M:63–79 bevarer orden, endpoint/resource-skille, Book-struktur og miljøbinding uten adresser i grafen. M:37,107 krever mottakeraksept. | Formatreglene kan kontrollere feltskille og 27 unike entryID-er, men ikke bevise samme matching eller mottakeroppførsel. Felles import/read-back- og hashprøver i M:129–135 ville kontrollert dette når begge celler finnes. **WP8-paritet er ikke testet; E1-K4.** |
| **3. Særreglenes faktiske operasjoner** | **Oppfylt på dokumentnivå.** K:65–83 skiller S01–S11 fra P01/P02 og beholder exact/generic-grener, målflater, tillegg før gulv, tak og senere kontekstboost. S:3185–3793 har separate parametre, ikke ett globalt gulv/tak per formål. | Planlagt grenmatrise M:150,154 vil kunne fange feil fase, målflate og klamping. En skjematest av tallene alene ville ikke fanget feil operasjon. Ingen gjennomført grenprøve er levert. |
| **4. Ett snapshot og proveniens fra analysen** | **Spesifisert, ikke bevist.** K:364 og M:117–125,144,159 krever samme snapshot gjennom reruting og senere beregninger samt hash, regel-ID-er og evaluatorversjon fra forslagets opprettelse. Den konkrete resultat-/evaluator-kontrakten er ikke låst. | Bytte mellom kontrollerte await-punkter, samtidige analyser og svar på et eldre forslag etter nytt bytte er nødvendige prøver. M:139 angir samtidighet, men ingen testkilde er levert. Cachegarantien har dessuten hullet i **E1-K2**. |
| **5. Full semantisk differanse og lukket feilport** | **Godt spesifisert; ikke levert.** M:142–157 sammenligner hele beslutningen, fryser input og krever null avvik. K:358 avviser literal-grep som motorbevis. E1-BYGG:76,81 oppgir at differansen ikke er kjørt og at eksisterende måleskript fortsatt har åpne feilveier. | Den beskrevne porten ville kreve rødt for manglende rader, ukjente felt og analyse-/testfeil. At porten faktisk gjør dette er ikke bevist. Krev også negative prøver av selve sammenligneren; se **E1-K1**. |
| **6. Autoriserte, hashbundne overganger og CAS** | **Prinsippene er besvart; operasjonskontraktene er uferdige.** M:85–100,117–121 skiller rettighetene og binder gammel/ny post, rapport, runtime, katalog og miljø. Hele posten/revisjonen sammenlignes også ved lik hash og ulik kilde. Tilbakekalt versjon får ikke automatisk rollback-unntak. | M:136–140 dekker avslag, stale CAS, kandidatbytte og rollback i plan. Det er ingen bevis for kontroll ved faktisk commit, varig kvittering eller krasjatomisitet. **E1-K3.** |
| **7. E2/E6-grenser og gjenoppretting** | **Delvis på dokumentnivå.** M:159,163–169 skiller ren evaluator, viste forslag, utfall og eierdata. M:125 beskriver gjeninnlasting. Men versjonerte evaluator-/hendelses-/godkjenningsskjemaer, konkret ressursbudsjett og full gjenopprettingspolicy mangler. E6-kvalitetsport er uttrykkelig senere arbeid. | Ingen utførte prøver. Det trengs kontraktprøver for eksplisitte input, ingen sideeffekter, manglende kandidatutslag og eiergrenser, samt E1-K2/K3s feilinjeksjon. E1 trenger grensesnittene nå; selve E2/E6-funksjonaliteten trenger ikke bygges i E1. |

## 2. Regelmotor og semantisk differanse

**Ingen femte matchevei er innført i det leste formatforslaget.** Butler-fasetten inneholder faste felt som eksisterende grener skal lese. Den inneholder ikke en brukerdefinert AST, operatorrekkefølge eller dynamisk predikatdispatch. `x-function` og regelbeskrivelser er skjemametadata; implementasjonen må ikke gjøre dem til instruksjoner. Book-delen har allerede komposisjonsbegrepene `allOf`, `sequence`, `firstOf` osv. i S:24–162. Bevaring av disse som registerdata er ikke tillatelse til å lage en ny Butler-tolker.

E1-DESIGN:41–47 er den gamle skissen. V2-tabellen på :71–81 og M:15 overstyrer den. Kartet sier uttrykkelig at U01–U04 står igjen og at WP4/WP19 ikke er løst (K:349–358). Derfor er både «alle frasetabeller er flyttet» og «én motor er etablert» fortsatt uriktige leveransepåstander. Antall reelle produksjonsmatchere er **ikke kontrollert i kode** her.

Den semantiske differansen er **ekte som krav, ikke som måleresultat**. M:142 tar med alle kandidater i orden, uavrundede scorer, bidrag, vern, tilgjengelighet, endelig valg, handlings-ID, mål, risiko og komplette utkast. M:144 håndterer flyktige ID-er og ny proveniens separat. M:146–157 fryser oppsettet og avviser ufullstendig måling. Dette retter de konkrete svakhetene i det første designet. En bestått fremtidig prøve vil likevel bare bevise likhet innenfor det låste prøvesettet og de supplerende grensetilfellene, ikke for enhver mulig melding.

Hash-inputen er entydig definert i M:73–79 og S:4869–4876. Kravet om bevart array-orden/Unicode og JCS-serialisering er forenlig med [RFC 8785 §§3.1–3.2](https://www.rfc-editor.org/rfc/rfc8785). Det finnes derimot ingen kontrollert JCS-kjøring gjennom en E1-celle. Skjemaets `examples` og `x-semanticValidation` er ikke eksekverbare bevis; `examples` er en annotasjon i [JSON Schema 2020-12 §9.5](https://json-schema.org/draft/2020-12/json-schema-validation#section-9.5). Hash, nodekanter, kompatibilitet, terskelrelasjoner og persondatakontroll krever egne implementerte validatorer som planen også forlanger.

## 3. Funn

### E1-K1 — Ingen implementasjon eller akseptansebevis å merge

**Blokkerer E1-merge. Leveransemangel, ikke påvist kodefeil.** E1-BYGG:5,24,58,72–81 sier at baselinebygg ble avbrutt, E1 ikke ble implementert, ingen tester ble kjørt og ingen PR ble opprettet. Notatet rapporterer dessuten fortsatt måleskript med setup-utelatelse og stoppveier med exit 0. Det siste er dokumentbelegg fra byggjobben, ikke et skript jeg har revidert på nytt.

**Konsekvens:** Det finnes ikke grunnlag for å godkjenne runtime-paritet, tilgang, bytte, rollback eller omstart. En grønn skjemaprøve eller ferdig flytteplan kan ikke erstatte disse bevisene.

**Lukking:** Lever implementasjon fra rent, identifisert PR-head og kjør de avtalte testene etter at byggevakten tillater det. Frys baseline og målemanifest. Prøv selve sammenligneren med en endring i kandidat nummer seks, et dypt handlingsfelt, et nytt ukjent felt, en manglende korpusrad og en simulert analyse-/regresjonsfeil. Alle må gi rød port; en kontroll med bare tillatte flyktige forskjeller skal fortsatt bestå. Disse er foreslåtte kontrollprøver, ikke utført mutasjonstesting. M:142–157 ville kreve avslaget, men det finnes ingen implementert test å kreditere.

### E1-K2 — Tap av siste hendelse har ingen definert oppdagelsesvei

**Blokkerer E1-merge til leserkontrakten er presisert og prøvd. Designfunn.** M:123 lover at nye analyser ser ny revisjon etter byttet. M:125 baserer gjeninnlasting på oppstart, gjenkobling og revisjonsgap, samtidig som normal drift bruker hendelser.

**Konkret feilsekvens:** Leseren har revisjon 7. CAS lagrer revisjon 8, men hendelsen går tapt. Forbindelsen består, og det kommer ingen revisjon 9. Leseren ser da verken et gap eller en gjenkobling og kan fortsette å starte analyser på 7. At et allerede startet kall får fullføre på 7, løser ikke dette. En forsinket hendelse gir dessuten et tidsrom der løftet om nye analyser på 8 trenger en presis gyldighetsgrense.

**Lukking:** Velg en faktisk garanti: eksempelvis synkron installasjon i den autoritative leseren før aktivering kvitteres, eller en varig strøm med kvittering/relevering og definert ferskhetsgrense. Hvis gamle snapshot kan brukes ved utilgjengelig kilde, må maksimal varighet, rapportert revisjon og forholdet til tilbakekalling angis. «Siste gyldige etter fastsatt policy» på M:125 er foreløpig en henvisning til en policy som ikke er fastsatt her.

**Test:** Dropp den siste hendelsen uten flere bytter eller gjenkobling; start nye analyser og krev den valgte ferskhets-/utilgjengelighetsgarantien. Gjør også bytte mellom innledende lesing og etablering av abonnement. M:139 nevner tapt hendelse, men beskriver ikke disse sekvensene. Generell omstarts- eller gaptest ville ikke nødvendigvis fanget dem. Ingen slik test er levert.

### E1-K3 — Varig kontrollpunkt og autorisasjon mangler en samlet commit-kontrakt

**Blokkerer E1-merge; valg som planen selv lar b1a gjøre.** M:83 merker API-ene som forslag, M:117–121 angir riktig atomisk post og rollback-prinsipp, og M:203 sier eksplisitt at eiercelle og varig CAS-mekanisme fortsatt må velges. Det er ikke definert hvilke varige oppdateringer som utgjør én fullført aktivering, eller når klienten kan stole på kvitteringen.

En `scaffoldUnique`, persistent celle er ikke i seg selv bevis for dette. Den leste [Book 06](../../../Book/06_CellResolver.md):50–66,168–182 skiller snapshotlagring fra commit-, strømbrudd- og krasjgarantier. [Book 04](../../../Book/04_Agreements_Contracts.md):63–112,179–206 skiller lesing, lagring og utlevering, og krever gyldig autorisasjon ved bruk.

**Lukking før akseptanse:** Lås eiercellens versjonerte Explore-kontrakter for import, kandidat, aktivering, rollback og status/kvittering. Angi atomisitetsgrensen for peker, revisjon, godkjennings-/rapportbinding og revisjonshistorikk; hendelser må kunne gjenskapes etter commit. Bind kontrollen av requester, scope, gjeldende godkjenning og tilbakekalling til den faktiske mutasjonen, også når arbeidet inneholder await. Definer entydig resultat ved krasj og timeout, retry og oppstart uten et lesbart gyldig snapshot. Lås samtidig E1s evaluator-/resultatgrensesnitt slik at E2/E3 ikke senere må gjette graf- og forslagstilhørighet.

**Test:** To samtidige CAS med samme forventede revisjon skal gi høyst én suksess. Krasj før/etter varig commit og før/etter kvittering skal gi én konsistent historikk etter omstart. Retry etter tapt svar må kunne avklares mot varig kvittering. Tilbakekall godkjenning/Grant mens en operasjon venter og kontroller avslag ved effekten. Prøv importør uten promoteringsrett, leser uten lagrings-/utleveringsrett og rollback til tilbakekalt/inkompatibel hash. M:136–140 krever mye av dette i overskriftsform; ingen levert test beviser håndheving eller krasjgrenser.

### E1-K4 — Registerkompatibilitet og ett pekerbytte er fortsatt betinget

**Blokkerer den senere registerflyttingen, ikke det autoriserte Butler-uttrekket i E1.** M:17,37,200–204 er korrekt forbeholdne. Jeg kontrollerte at den navngitte `contract/purpose_registry_contract_v0.json` fortsatt mangler i register-PDD-en. Dens [PLAN](../../PDD_formaalsregister-som-graf_2026-09-11/PLAN.md):39 navngir state/resolve/match/taxonomyDigest, men leverer ikke import, hashadressert read-back eller varig kvittering.

**Konsekvens:** Samme Book-feltnavn og grafhash er nødvendig, men utilstrekkelig. WP8 må kunne bevare hele konvolutten, inklusive Butler-fasetten, og holde den isolert fra sin forsonte aktive taksonomi. Den faste `knowledgeBase`-versjonen og lukkede `consumerFacets` i S:365–395,4822–4838 er en konkret versjonert importavtale som WP8 må akseptere; de er ikke et universelt registerformat. Lagring av dette snapshotet løser ikke forsoning eller motorvalg.

**Lukking:** WP8 adopterer kontrakten, avklarer node-/facetsemantikk, grenser og eierskap, og begge virkelige cellegrenser består samme fixture-pakke. Produksjonsleseren må allerede kunne lese begge kilder gjennom den stabile kontrakten; ellers kreves en kodeendring i tillegg til pekerbyttet. Tidligere godkjent graf og nødvendige leserettigheter må beholdes gjennom rollback-perioden. M:111s avslutning av Butler som aktiv skriver trenger også en konkret håndhevet overgang.

**Test:** M:133–140,155 gir riktige føringer for import/read-back, hash, retry, rettigheter og faktisk etterprøve. De ville kunne fange omskriving, tapt fasett og feil kilde, men ingen prøve mot WP8 finnes. Testene må også vise at gammel skriver ikke kan overta aktiv kilde etter overtakelsen.

## 4. CellProtocol, HAVEN og friksjon i flyttingen

Planen følger de riktige grensene: metodebevisste Explore-operasjoner, resolvermediert tilgang med faktisk requesterbevis, adskilt grafidentitet og lagringsadresse, separate lagrings- og utleveringsrettigheter og ingen autorisasjon avledet fra et treff (M:85–100). Dette stemmer med den leste [Book 03](../../../Book/03_Identity_Model.md):20–84,107–127 og [Book 22](../../../Book/22_Explore_Contracts_For_Skeleton_Authoring.md):70–173. De konkrete Grants og håndhevingen gjenstår; prinsipielt samsvar er ikke verifisert tilgangssikkerhet.

HAVEN-grensen er også riktig: scaffold-grafen flyttes, mens personlige vekter, meldinger, utfall og Perspective-kanter blir hos entiteten. Administratoren samtykker ikke for andre, og flytting oppretter ikke automatisk en personlig rotlenke. Nivå 0/1/2 og tilbaketrekking i M:163–171 samsvarer med [FORMAALSSPEC](../FORMAALSSPEC.md):255–279 og [læring-uten-profil](../../PDD_formaalsregister-som-graf_2026-09-11/contract/laering-uten-profil.md):51–75. Ingen ny samtykkerunde per bruker er nødvendig for en ren flytting av scaffold-data. Dersom personlige input brukes i migreringsmålingen, må evaluator, rapport og eksport fortsatt respektere hver entitets eksisterende scope; rå input eller personavledede tellinger kan ikke følge en felles flytterapport uten nødvendig samtykke.

Fritekst og åpne Book-utvidelser betyr at payloaden ikke automatisk er fri for persondata. M:171 og S:4884 erkjenner dette og krever innholdskontroll utover formatvalidering. Det er en riktig forutsetning, ikke en levert kontroll.

For at **selve overtakelsen** skal bli ett pekerbytte, må følgende allerede være ferdig:

1. Ett varig, eierstyrt kontrollpunkt brukes av alle Butler-analyser fra første E1-versjon; ingen konkurrerende aktive pekere eller skjulte literal-fallbacker.
2. Begge kilder har kompatibel, tilgjengelig og autorisert hashadressert lesing. Registerets import/read-back bevarer hele verdien uten omforming.
3. Grafen er forhåndsimportert og lest tilbake; JCS/hash, full semantisk prøve, rettigheter og rollback-grunnlag er verifisert og bundet til en konkret rapport/godkjenning.
4. CAS flytter hele kildeposten med ny revisjon; tilhørende historikk/kvittering er varig, og E1-K2s lesergaranti er oppfylt.
5. Pågående analyser beholder sitt snapshot, nye analyser følger den definerte aktiveringsgrensen, etterprøven bekrefter dette, og gammel aktiv skrivevei er avviklet uten å ødelegge rollback.

Dette kan gi liten friksjon ved selve byttet. Første etablering krever fortsatt kontraktarbeid, mottakerstøtte, autorisasjon og prøver. Planen er ærlig om dette; det finnes ingen målt tids-, ytelses- eller friksjonsgevinst ennå.

## 5. Utført kontroll og anbefaling

Utført i denne jobben, uten kodeendringer eller bygg:

- JSON-parsing og strukturelle assertions: 47 definisjoner, 258 lokale skjemareferanser som løser, 15 hjelperobjekter og 13 særregelobjekter. Alle 182 øvrige parameterfelt er påkrevd i lukkede objekter; sammen med 27 × 7 leksikonfelt blir dette 371 plasser. De 27 entryID-kravene er entydige.
- Filhashene for Book-snapshot og komposisjonsskjema stemmer med M:32–33. Dette er bytekontroll, ikke ny semantisk gjennomgang av hele Book-snapshotet.
- WP8-kontraktfilens fravær er kontrollert. RFC 8785 og JSON Schema 2020-12 er kontrollert mot offisielle nettkilder.

**Ikke utført:** full JSON Schema-validering med Ajv i denne jobben, negative runtime-importer, JCS/hashvektorer, semantisk differanse, Swift-tester, mutasjonstesting, CAS/krasjprøver, migrering eller staging. K:376–382 rapporterer tidligere formatprøver; de er ikke kjørt om her og beviser heller ikke runtime-paritet.

**Anbefaling: ikke merge nå.** E1-K1–K3 må lukkes før E1 kan godkjennes. Fortsett det allerede valgte B-arbeidet når byggforutsetningene er oppfylt; manglende WP8 skal ikke alene stanse det avgrensede Butler-uttrekket. Registerflytting må i tillegg vente på E1-K4. Ny kodekontroll skal gjøres på den da leverte PR-headens eksakte SHA.

**Læring innenfor denne leveransen:** En hendelsesplan må teste tap av *siste* hendelse uten senere aktivitet; revisjonsgap alene gir ikke gjenoppretting. Et atomisk objekt i minne er heller ikke et bevis for varig, autorisert aktivering. Dette er designlæring, ikke erfaring fra en utført migrering. Læringsruting er kjørt. Oppdragets grense på én rapportfil er fulgt: ingen læringsledger, skill eller distribusjonsartefakt er endret, og capture/sync er ikke påstått utført.
