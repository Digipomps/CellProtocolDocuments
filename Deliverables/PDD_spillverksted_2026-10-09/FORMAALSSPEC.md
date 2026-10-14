# Formålsspesifikasjon — spillverksted

Oppgavemappe: `PDD_spillverksted_2026-10-09` · Opprettet 2026-10-09 · Iterasjon 1 (ikke godkjent)

> Regel: ingen plan før G1 er godkjent av Kjetil. For GUI: ingen implementering før G1-GUI (rendret bilde) er godkjent.
> Et dokument om leveransen teller aldri som leveransen.

Visuelt tre med godkjenning: se STATUS.md for lenken. Treet ligger også i Formålstrær-siden som `trees/spillverksted-2026-10-09`.

## 0. Intensjon (ordrett) og brief-audit

> «Jeg vil ha en arbeidsbenk for å lage spill slik at jeg kan lære Sverre - sønnen min - om programmering og ai orkestrering og hjelpe han til å lage spill han kan publisere via HAVEN. Vi trenger prosjektadministrasjon, valg av verktøy (hvilken spillmotor skal vi bruke) Vi skal koble på en språkmodell som kan diskutere med brukeren hva brukeren ønsker å lage og vise hvordan det blir. Vi skal bruke formål for å finne riktige verktøy og GUI elementer. Det betyr også å lage et bibliotek - eventuelt en RAG for hva som finnes av verktøy og hva de skal løse. Vurder om vi trenger et eget scaffold for dette. Denne chat-hjelperen er et mønster vi skal bruke i alle andre arbeidsbenker også. Så pass på å tenke nøye igjennom hvordan det skal lages generelt og være et nyttig og effektivt verktøy. Dette må dokumenteres som et eget område som vi kan lage instruksjoner og skills til. Gjør en grundig analyse av muligheter og behov, lag en plan som du viser meg i et visuelt tre av formål. (Formålenes detaljer - inkludert Goal kan vises som en popup på klikk). Jeg vil ha en godkjenn knapp og felt for eventuelle kommentarer som skal trigge neste fase i utviklingen.» (Kjetil, 2026-10-09 08:07Z)

Kildene er lest fra `origin/main` i CellScaffold (`8e282f8`, 2026-10-08) og fra CellProtocolDocuments på Kjetils Mac 2026-10-09. Ingenting er kjørt mot staging eller prod.

| Påstand / antatt kapabilitet | Audit | Kilde |
|---|---|---|
| Små spill i HAVEN er utforsket før | contradicted: ingen spillkode i repoet, i gamle tråder eller i lokale mapper; det som finnes er «Sverres spillrom» laget 08.10 som Claude-side | søk 08.10 i CellScaffold, CellProtocolDocuments og prosjekttrådene; https://claude.ai/artifact/4qewDBuVf25GcAMC9sUTYb |
| Chat som sentralt grensesnitt er beskrevet | retrieved: Book 19 beskriver chat-arbeidsbenken, matchepipeline og ikke-forhandlbare grenser | `CellProtocolDocuments/Book/19_Chat_Workbench_Central_Interface.md` §1–§9 |
| Chatmotoren kan rute til hjelpere | retrieved, men hardkodet: `submitChatPrompt` ruter via en fast switch på hjelper-keypaths | CellScaffold `Sources/App/Cells/PersonalCopilot/PersonalCopilotCloudStore.swift:5023`, `:3920`, `~:5080` |
| Språkmodell kan kobles på | retrieved: `AIGatewayCell` med `ai.invoke` (OpenAI- og Anthropic-format); `ChatAIGatewayRequest`; eksempel i `ConferenceAIGatewayPreviewCell.swift:120-145` | `Sources/App/Cells/AI/AIGatewayCell.swift:361,462,3353`, `Sources/App/Support/ChatAIGatewayRequest.swift:9` |
| AIGateway kan kalle verktøy | contradicted, med vilje: AIGateway foreslår bare; Butler Chat ruter og har autoriteten (Kjetils beslutning 2026-09-02) | `Sources/App/Cells/AI/AIGatewayPurposePolicy.swift:12`; minne `butler-chat-arkitektur` |
| Forslag → bekreft → utfør finnes | retrieved: `GroundedActionPlan` med `requiresUserConfirmation`, `sideEffectFree`, tørrkjøring | `Sources/App/Support/ExecutablePurposeGrounding.swift:45`, `Sources/App/Cells/PersonalCopilot/ExecutablePurposeGroundingCell.swift:7-27` |
| Eskaleringstak for modellbruk finnes | retrieved: `never_external` / `ask_each_time` / `automatic_within_grant`, strengeste lag vinner | `Sources/App/Support/ChatInterpreterEscalationCeiling.swift:7,534,681` |
| Formål kan finne verktøy og GUI-elementer | delvis: koblingen er fritekst (`capabilityHints`, `CatalogEntry.purpose`, kapabilitetsindeksen med 48 lenker og 41 hengende refs); ingen typede kanter formål→celle/skjelett | `Sources/App/Support/PurposeKnowledgeBase.swift:7-17,101`, `Sources/App/Cells/ConfigurationCatalog/ConfigurationCatalogCell.swift:27,1425`, `Tools/CapabilityIndex/haven_capability_index.v1.json` |
| Det finnes ett formålsregister | contradicted: minst tre vokabularer (PurposeKnowledgeBase, PurposeCell-seed, `ChatPurposeResourceRouter.purposeLexicon`) | `Sources/App/Support/ChatPurposeResourceRouter.swift:2320`; `Documentation/Forskning/Fase2_Forutsetning_En_Formaalsnamespace_2026-08-30.md` |
| RAG med semantisk søk finnes | contradicted: alt søk er ordbasert; ingen vektorer | `Sources/ScaffoldKit/CommonsLibrarian/CommonsLibrarianCell.swift:264`; `Sources/App/Cells/RAG/` |
| Skjelett kan endres uten rekompilering | retrieved: Porthole-editorens `editor.working.setSkeleton` og `editor.apply` med revisjonssjekk | `Sources/App/Controllers/PortholeWebSessionSupport.swift:5733-6060,6064,6140` |
| Chat kan endre skjelett | unavailable: ingen kjede fra chat til `editor.working.setSkeleton` | samme fil; søk etter kallere |
| HAVEN kan vise eller publisere brukerlaget JS | contradicted: ingen iframe/srcdoc; alle CSP-er blokkerer brukerskript; Publication publiserer maler og medier | `Sources/App/Controllers/VaporButterpopStudio.swift:29`, `VaporPublication.swift:125,254` |
| Prosjektadministrasjon finnes | retrieved: `ProjectPortfolioCell`, `WorkItemCell`, Developer Workbench | `Sources/App/Cells/WorkItems/`, `DeveloperWorkbenchConfiguration.swift:9-30` |
| Barne- eller foresattkontoer finnes | contradicted: bare en 18+-dør | `Sources/App/Cells/Proofs/AgeProofDoorCell.swift:82,126` |
| Godkjenning i arbeidsbenken | unavailable i HAVEN i dag; spesifisert, ikke godkjent | `CellProtocolDocuments/Deliverables/PDD_godkjenninger-i-arbeidsbenken_2026-10-07/FORMAALSSPEC.md` |
| Regel for eget scaffold | retrieved: bare ved ulik risikoprofil eller deploytakt; ikke ett per cellefamilie | `Documentation/Scaffold_Product_Split_Plan_2026-07-10.md` §1–2 |
| KAPLAY og Phaser er åpne og aktive | retrieved fra nett 2026-10-09: Phaser 4.0.0 «Caladan» er stabil; KAPLAY publiseres på npm; lisenser ikke lest i fil ennå | phaser.io/download/stable, npmjs.com/package/kaplay |
| Scratch kan bygges inn | contradicted: Scratch gikk over til AGPL i 2024 | scratchfoundation.org/open-source-license |

## 1. Formålstre

Treet er klassifisert under `purpose://human-agency` i Book 23. Prosjektdelen gjenbruker `purpose://project-work.work-items`, og lærdomsfangsten gjenbruker `purpose://purpose-taxonomy.capture-and-place`. Alle nye noder er kandidater, navngitt her. Refs er engelske og ASCII, slik resten av Book 23 er; titlene er norske. Kombinator står i kolonnen «Sammensetning» (Book 36).

| Kode | purposeRef | Tittel | Forelder | Sammensetning | Goal (outcome) | Verifier | Status | Fase |
|---|---|---|---|---|---|---|---|---|
| R | `purpose://candidate.game-workshop.root` | Sverre lærer programmering og AI-orkestrering ved å lage og publisere egne spill i HAVEN | — (under `purpose://human-agency`) | allOf | Sverre har laget og publisert minst ett spill han selv har bestemt innholdet i, og kan forklare med egne ord hva koden og AI-hjelperne gjorde. | T-R1: samtale med Sverre etter første publisering, notert i ACCEPT.md | candidate | Fase 1–3 |
| A | `purpose://candidate.game-workshop.learning` | Sverre forstår det han lager | R | allOf | Hvert steg i verkstedet lærer Sverre noe han kan vise, ikke bare noe AI har gjort for ham. | T-A: øktlogg med «dette lærte jeg» per økt | candidate | Fase 1 |
| A1 | `purpose://candidate.game-workshop.learning.progression-path` | Læringssti i fem nivåer | A | sequence | Verkstedet har fem nivåer som låses opp etter hvert: 1 Endre tall i et ferdig spill. 2 Bestille endringer fra hjelperen. 3 Lese og forklare koden hjelperen skrev. 4 Skrive egen kode som hjelperen ser over. 5 Dele et spill i oppgaver og fordele dem på flere AI-roller. | T-A1: gå gjennom nivå 1–2 med Sverre i prototypen | candidate | Fase 1 |
| A2 | `purpose://candidate.game-workshop.learning.explain-each-change` | Hjelperen forklarer hver endring | A | blad | Hver endring hjelperen foreslår kommer med en kort forklaring på barnespråk og en markering av hvilke linjer som endres. | T-A2: ti forslag i prototypen har forklaring og markerte linjer | candidate | Fase 1 |
| A3 | `purpose://candidate.game-workshop.learning.mentor-oversight` | Kjetil følger med og veileder | A | blad | Kjetil ser hva Sverre har bedt om, hva som ble godtatt og hvor han står i læringsstien, og kan legge igjen en kommentar. | T-A3: Kjetil finner forrige økt på under ett minutt | candidate | Fase 2 |
| B | `purpose://candidate.workbench-assistant.root` | Arbeidsbenk-assistenten (mønster for alle arbeidsbenker) | R | allOf | Det finnes én beskrevet og testet måte å lage en samtalehjelper for en arbeidsbenk på. Spillverkstedet er første bruker. | T-B: kontrakt og fixtures validerer; spillverkstedets profil lastes uten kodeendring i chatmotoren | candidate | Fase 1–2 |
| B1 | `purpose://candidate.workbench-assistant.understand-intent` | Forstår hva brukeren vil lage, som formål | B | blad | Det brukeren skriver blir klassifisert mot formålstreet først. Bare det som ikke passer, dekomponeres med modell. Hjelperen spør bare om det som endrer hva som lages. | T-B1: tjue barneformulerte ønsker gir riktig formål i minst femten, målt på et sett skrevet av noen som ikke har sett reglene | candidate | Fase 1 |
| B2 | `purpose://candidate.workbench-assistant.preview-before-change` | Viser hvordan det blir før noe endres | B | blad | Hvert forslag vises i en forhåndsvisning ved siden av samtalen før brukeren godtar det. Det som er godtatt og det som er foreslått, kan sammenlignes. | T-B2: måling av tid fra forslag til synlig forhåndsvisning, tre forsøk | candidate | Fase 1 |
| B3 | `purpose://candidate.workbench-assistant.select-tools-by-purpose` | Velger verktøy og GUI-elementer ut fra formål | B | blad | For hvert formål foreslår hjelperen verktøy og GUI-elementer fra biblioteket som er merket med det formålet, og sier hvorfor. | T-B3: alle forslag i en testsamtale kan spores til en bibliotekoppføring | candidate | Fase 2 |
| B4 | `purpose://candidate.workbench-assistant.propose-human-decides` | Foreslår, mennesket bestemmer | B | blad | Modellen foreslår bare. Alle endringer skjer etter et klikk fra brukeren, og målcellen sjekker tilgang på nytt. | T-B4: negative tester: endring uten klikk, feil bruker og ukjent formål blir avvist | candidate | Fase 2 |
| B5 | `purpose://candidate.workbench-assistant.reusable-profile` | Andre arbeidsbenker kan ta det i bruk med en profil | B | blad | En ny arbeidsbenk får sin hjelper ved å skrive en profil: formålsgren, bibliotek, forhåndsvisning, tillatte handlinger, tone og eskaleringstak. Ingen ny kode i chatmotoren. | T-B5: to profiler lastes av samme motor; kontraktvalidator grønn | candidate | Fase 2 |
| B6 | `purpose://candidate.workbench-assistant.child-safe-dialogue` | Trygg samtale for et barn | B | blad | Hjelperen svarer tilpasset alder, holder seg til verkstedet, ber ikke om personopplysninger, og bruker bare modeller Kjetil har valgt. | T-B6: et sett med vanskelige meldinger gir avvisning eller omdirigering, gjennomgått av Kjetil | candidate | Fase 1 |
| C | `purpose://candidate.tool-library.root` | Verktøybibliotek: hva som finnes og hva det løser | R | allOf | Biblioteket svarer på «hva kan jeg bruke til dette formålet?» med oppføringer som sier hva de løser, for hvem, og med hvilken lisens. | T-C: bibliotekoppslag for tjue formål gir minst én relevant oppføring per formål | candidate | Fase 1–2 |
| C1 | `purpose://candidate.tool-library.purpose-keyed-entries` | Hver oppføring er merket med formål | C | blad | Hver oppføring har purposeRefs, hva den løser, eksempler, lisens og alder. Den nøkles på purpose://-refs, ikke på fritekst. | T-C1: validator nekter oppføring uten purposeRef og lisens | candidate | Fase 1 |
| C2 | `purpose://candidate.tool-library.purpose-first-lookup` | Oppslag: formål først, tekstsøk etterpå | C | blad | Oppslag går først via formålsrefs, så via ordsøk. Tekst til modellen hentes etter oppslag, aldri i det skjulte. Semantisk søk (vektorer) legges til bare hvis målinger viser at ordsøk ikke holder. | T-C2: treffrate med og uten tekstsøk på et uavhengig sett | candidate | Fase 2 |
| C3 | `purpose://candidate.tool-library.derived-from-sources` | Biblioteket bygges fra kildene, ikke for hånd | C | blad | Oppføringer for celler og GUI-elementer lages fra cellenes Explore-kontrakter, CellConfiguration-discovery og kapabilitetsindeksen. En oppføring som ikke lenger finnes i kilden, faller ut. | T-C3: bygg biblioteket to ganger fra samme kilde gir samme resultat; fjernet celle forsvinner | candidate | Fase 2 |
| C4 | `purpose://candidate.tool-library.open-licensed-game-content` | Spillinnhold med åpne lisenser | C | blad | Biblioteket har maler (plattform, labyrint, huskespill, regnespill), figurer og lyder med kjent åpen lisens, slik at Sverre kan bruke dem i publiserte spill. | T-C4: lisensfeltet er fylt og kontrollert for hver ressurs | candidate | Fase 1 |
| D | `purpose://candidate.game-workshop.engine` | Spillmotor og sandkasse | R | allOf | Spillene lages med en motor valgt etter målte kriterier og kjører isolert fra resten av HAVEN. | T-D: motorvalgstabell med målinger i FORMAALSSPEC | candidate | Fase 1 |
| D1 | `purpose://candidate.game-workshop.engine.selection` | Motorvalg: KAPLAY først, Phaser når spillene vokser | D | blad | Første motor er KAPLAY (MIT, enkel og lesbar kode, kjører i nettleseren uten byggesteg). Phaser er neste trinn for større spill. Valget bekreftes ved at hjelperen lager fem fungerende småspill i hver. | T-D1: fem bestillinger per motor, tell spill som kjører uten retting | candidate | Fase 1 |
| D2 | `purpose://candidate.game-workshop.engine.sandbox-isolation` | Spillene kjører isolert fra HAVEN | D | blad | Et spill kjører i en sandkasse uten tilgang til HAVEN-økten, informasjonskapsler eller data: iframe med sandbox og uten allow-same-origin i forhåndsvisning, og CSP-direktivet sandbox på publiserte spill. | T-D2: et ondsinnet testspill prøver å lese økt og kalle API; alt blir avvist | candidate | Fase 2 |
| D3 | `purpose://candidate.game-workshop.engine.swappable-adapter` | Motoren kan byttes | D | blad | Arbeidsbenken snakker med motoren gjennom en liten adapter (mal, forhåndsvisning, eksport), så et nytt motorvalg ikke krever ny arbeidsbenk. | T-D3: samme spillprosjekt forhåndsvises med to adaptere | candidate | Fase 2 |
| E | `purpose://candidate.game-workshop.project` | Prosjektadministrasjon for spillene | R | allOf | Hvert spill er et prosjekt med oppgaver, versjoner og status som både Sverre og Kjetil ser. | T-E: et spill fra idé til publisert har sporbare oppgaver og versjoner | candidate | Fase 2 |
| E1 | `purpose://candidate.game-workshop.project.uses-haven-workbench` | Spillprosjekter bruker HAVEN Workbench | E | blad | Spillprosjekter lages med ProjectPortfolio og WorkItem som allerede finnes, ikke med et nytt prosjektsystem. | T-E1: inspeksjon av at spillprosjektet er WorkItem-poster under et ProjectPortfolio-prosjekt | gjenbruk | Fase 2 |
| E2 | `purpose://candidate.game-workshop.project.versioned-changes` | Hver godtatt endring er en versjon | E | blad | Hver endring Sverre godtar lagres som en versjon med hvem som ba om den, hva hjelperen foreslo og hva som ble godtatt. Han kan gå tilbake til en tidligere versjon. | T-E2: ti endringer, gå tilbake til nummer tre, spillet er likt versjon tre | candidate | Fase 2 |
| E3 | `purpose://candidate.game-workshop.project.child-readable-tasks` | Oppgaver Sverre forstår | E | blad | Hjelperen gjør ønsker om til korte oppgaver i barnespråk («Få helten til å hoppe») som vises som en liste Sverre kan krysse av. | T-E3: Sverre leser opp og forklarer tre oppgaver | candidate | Fase 2 |
| F | `purpose://candidate.game-workshop.publishing` | Publisering via HAVEN | R | sequence | Et ferdig spill kan publiseres til en fast adresse i HAVEN etter Kjetils godkjenning. | T-F: publiser et testspill og åpne det på en annen enhet | candidate | Fase 3 |
| F1 | `purpose://candidate.game-workshop.publishing.public-address` | Publisert spill har egen adresse | F | blad | Publiserte spill ligger under en egen rute (for eksempel /spill/navn) med CSP sandbox, ved siden av /pub. | T-F1: tre målinger av lastetid under fem sekunder | candidate | Fase 3 |
| F2 | `purpose://candidate.game-workshop.publishing.guardian-approval` | Kjetil godkjenner hver publisering | F | blad | Sverre kan be om publisering, men spillet blir offentlig først når Kjetil har godkjent den versjonen. Avpublisering kan begge gjøre. | T-F2: publisering uten godkjenning avvises; endret versjon etter godkjenning krever ny godkjenning | candidate | Fase 3 |
| F3 | `purpose://candidate.game-workshop.publishing.child-privacy` | Ingen persondata om Sverre i publiserte spill | F | blad | Publiserte spill viser bare et kunstnernavn Kjetil har godkjent. Spillene samler ikke inn data, og det finnes ingen chat med fremmede. | T-F3: inspeksjon av publisert spill og CSP connect-src | candidate | Fase 3 |
| G | `purpose://candidate.game-workshop.platform` | Eget scaffold? Ikke nå | R | allOf | Spillverkstedet bygges som celler og CellConfiguration i CellScaffold. Det skilles ut først når et målt kriterium slår til. | T-G: inspeksjon mot Scaffold_Product_Split_Plan_2026-07-10 | candidate | Fase 1 |
| G1 | `purpose://candidate.game-workshop.platform.no-new-scaffold-yet` | Ingen nytt scaffold nå, men egen sandkasse for spill | G | blad | Arbeidsbenken, hjelperen og biblioteket lever i CellScaffold. Det eneste med en annen risikoprofil er brukerlaget spillkode, og den isoleres med sandkasse (D2) i stedet for et eget scaffold. | T-G1: inspeksjon av at ingen ny Package-target er lagt til før kriteriet i G2 er målt | candidate | Fase 1 |
| G2 | `purpose://candidate.game-workshop.platform.split-out-criteria` | Kriterier for å skille ut en spillvert | G | blad | En egen spillvert (eget domene eller target) lages hvis ett av disse slår til: spill trenger lagring per spiller, trafikken fra spill påvirker resten av HAVEN, eller sandkassetesten T-D2 ikke kan bli grønn på samme domene. | T-G2: måling ved fase 3 | candidate | Fase 3 |
| H | `purpose://candidate.game-workshop.documentation` | Dokumentasjon, instruksjoner og skills | R | allOf | Arbeidsbenk-assistenten er et eget dokumentert område som Claude, Codex og mennesker kan bygge videre på. | T-H: lenkesjekk og inspeksjon | candidate | Fase 1 |
| H1 | `purpose://candidate.game-workshop.documentation.dedicated-area` | Eget område for arbeidsbenk-assistenten | H | blad | Documentation/Arbeidsbenkassistent/ i CellScaffold beskriver mønsteret, kontrakten og profilformatet, og et Book-kapittel i CellProtocolDocuments beskriver protokolldelen. | T-H1: hver påstand om implementert oppførsel har fil:linje | candidate | Fase 1 |
| H2 | `purpose://candidate.game-workshop.documentation.skills` | Skills for å bygge og bruke arbeidsbenker | H | blad | To skills: «workbench-assistant-authoring» for å lage en ny arbeidsbenkprofil, og «spillverksted-mentor» for Claude og Codex som hjelper Sverre. | T-H2: en ny tråd lager en profil for Developer Workbench bare ved hjelp av skillen | candidate | Fase 2 |
| H3 | `purpose://candidate.game-workshop.documentation.lesson-capture` | Lærdommer fanges underveis | H | blad | Avvik og funn i verkstedet blir lærdommer i registeret og endringer i skills. | T-H3: purpose_dev.py validate er grønn etter hver fase | gjenbruk | Alle faser |

## 1b. Analyse: muligheter og behov

### Hva som allerede finnes og kan gjenbrukes
- **Chatmotoren** i Personal Co-Pilot / Butler Chat: ruting, forslagskort, bekreftelse, eskaleringstak og arbeidsbenkoppsettet med tråder, chat og sidepanel (`PersonalCopilotConfigurationFactory+Workbench.swift:33`).
- **Formålsforankring**: `PurposeDecomposition` og `ExecutablePurposeGroundingCell` (analyser, dekomponer, verifiser, tørrkjør).
- **AIGateway** som forslagsmotor, med leverandørvalg per chat-scope (`ChatScopedAIProviderRouter`).
- **Porthole-editoren** som forhåndsvisning og lagring av skjelett uten rekompilering.
- **Workbench-cellene** for prosjekt og oppgaver.
- **Formålstrær-siden** og PDD-verktøyene for å vise og godkjenne formål.

### Hull som spillverkstedet må tette
1. Hjelpere er hardkodet i chatmotoren. Mønsteret krever deklarativ registrering (B5).
2. Ingen kjede fra chat til forhåndsvisning. Spill trenger sin egen forhåndsvisning (sandkasse-iframe), skjelettflater trenger `editor.working.setSkeleton` gjort tilgjengelig som en celle-handling (B2).
3. Formål er ikke koblet typet til verktøy og GUI-elementer, og det finnes tre vokabularer (B3, C1).
4. Ingen sandkasse eller publiseringsvei for brukerlaget kode (D2, F1).
5. Ingen modell for barn og foresatte (F2, F3).

### Arbeidsbenk-assistenten som mønster
Mønsteret er en løkke med sju steg, der modellen bare deltar i steg 1 og 3:
1. **Forstå**: klassifiser ønsket mot formålstreet; dekomponer bare resten.
2. **Avklar**: spør bare om det som endrer treet.
3. **Foreslå**: en `GroundedActionPlan` med verktøy og GUI-elementer fra biblioteket, og en forklaring.
4. **Vis**: forhåndsvisning ved siden av samtalen.
5. **Bestem**: brukeren godtar, endrer eller forkaster med et klikk.
6. **Utfør**: målcellen sjekker tilgang på nytt og lagrer en versjon.
7. **Lær**: avvik blir lærdommer.

En arbeidsbenk tar mønsteret i bruk med en **profil**: formålsgren (`anchorRef`), bibliotek, forhåndsvisningsadapter, tillatte handlinger, tone og alder, eskaleringstak og måletall. Måletallene er felles for alle arbeidsbenker: andel forslag godtatt uten endring, tid fra ønske til første forhåndsvisning, og antall avklaringsspørsmål per ønske.

### Motorvalg

| Kriterium | KAPLAY | Phaser 4 | Godot (web-eksport) | Scratch | MakeCode Arcade |
|---|---|---|---|---|---|
| Kjører i nettleseren uten byggesteg | ja | ja | nei, eksport kreves | ja | ja, via makecode.com |
| Lesbar kode for et barn | best | middels | GDScript, eget verktøy | blokker | blokker, JS og Python |
| Modeller skriver riktig kode | antatt god, ikke målt | risiko: modellene kjenner mest Phaser 3 | middels | ikke aktuelt | ikke målt |
| Kan bygges inn i HAVEN | ja (MIT, ikke lest i fil) | ja (MIT, ikke lest i fil) | tungt (store WASM-filer) | nei, AGPL siden 2024 | ikke sjekket |
| Vokser med eleven | til mellomstore spill | store spill | fullverdig motor | begrenset | begrenset |

**Anbefaling:** KAPLAY i fase 1, Phaser som neste trinn, motoren bak en adapter (D3). Valget bekreftes med testen T-D1 før G2.

### Eget scaffold?
**Nei, ikke nå.** Arbeidsbenken, hjelperen og biblioteket har samme risikoprofil og deploytakt som resten av CellScaffold. Det som skiller seg ut er brukerlaget spillkode. Den isoleres med sandkasse: iframe uten `allow-same-origin` i forhåndsvisning, og CSP-direktivet `sandbox allow-scripts` på publiserte spill. Begge gir spillet et ugjennomsiktig opphav uten tilgang til HAVEN-økten. Kriteriene for å skille ut en egen spillvert står i G2.

### Bibliotek eller RAG
Biblioteket er først en **katalog nøklet på formål**, bygget fra kildene (C1, C3). Oppslag går via formål, deretter ordsøk. Modellen får tekst fra biblioteket først etter oppslaget, aldri i det skjulte. Semantisk søk (vektorer) legges til bare hvis T-C2 viser at ordsøk ikke holder. Det følger lærdommene om utviklingssett og uavhengig måling.

## 2. Avgrensning og avhengigheter

Hva dette IKKE er:
- Ikke en generell barneplattform eller et sosialt nettverk for spill. Ingen chat mellom spillere.
- Ikke en endring av AIGatewayPurposePolicy. AIGateway forblir uten verktøy.
- Ikke et nytt prosjektsystem. Workbench-cellene gjenbrukes.
- Ikke et nytt scaffold i fase 1–2.
- Ikke en kanonisk endring av Book 23. Nye formål er kandidater til Kjetil godkjenner dem.

| Kapabilitet / avhengighet | Kilde (fil) | Avgrensning | Må virke før test? |
|---|---|---|---|
| AIGateway svarer med en modell Kjetil har valgt | `AIGatewayCell.swift:361,462` | ikke målt på staging i denne oppgaven | ja, før T-B1 og T-B2 (måles i fase 1) |
| Chatmotoren kan få en ny hjelper uten kodeendring | `PersonalCopilotCloudStore.swift:~5080` | ikke mulig i dag; krever B5 | ja, før T-B5 |
| Porthole-editoren kan lagre skjelett | `PortholeWebSessionSupport.swift:6064` | sesjonsbundet kontrollerkode, ikke en celle | ja, før skjelettflater i B2 |
| Sandkasse-iframe og CSP sandbox | ingen kode i dag | nettleserstøtte er standard; HAVEN-rute må lages | ja, før T-D2 og F1 |
| Godkjenning i arbeidsbenken | `PDD_godkjenninger-i-arbeidsbenken_2026-10-07` | ikke godkjent; F2 bygger på den | ja, før T-F2 |
| Formålsregister med én navnerom | `Fase2_Forutsetning_En_Formaalsnamespace_2026-08-30.md` | tre vokabularer i dag | ja, før T-B3 og T-C1 |
| Godkjenningsknappen på formålssiden | Claude-side med database og varsling til denne tråden | midlertidig til F2/godkjenninger finnes i HAVEN | nei |

## 3. Forventningskontrakt — «Det du kommer til å se»

| Leveranse | Type | Hvor | Referanse | Godkjent |
|---|---|---|---|---|
| Formålstre med detaljer og godkjenning | kjørende side | Claude-side, lenke i STATUS.md | denne spesifikasjonen §1 | nei |
| Bilder av arbeidsbenken: samtale, forhåndsvisning, prosjekt, bibliotek (tom, fylt, feil) | bilde | `images/` | `images/<flate>-<tilstand>-v1.png` | nei (fase 1, G1-GUI) |
| Klikkbar prototype Sverre kan prøve: chat med Claude, KAPLAY-spill i sandkasse, angre | kjørende side | Claude-side | T-A1, T-B2, T-D1 | nei (fase 1) |
| Profilformat og kontrakt for arbeidsbenk-assistenten | fil | `contract/` og CellScaffold `Documentation/Arbeidsbenkassistent/` | T-B, T-B5 | nei (fase 1) |
| Bibliotek v0 for spill (maler, motorer, GUI-elementer) med formål og lisens | fil | `contract/game-tool-library.v0.json` | T-C1, T-C4 | nei (fase 1) |
| Motorvalgsmåling, fem spill per motor | testutdata | `TESTRESULT.md#motor` | T-D1 | nei (fase 1) |

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

## Book 23-noder som kan være forelder/gjenbruk (leksikalsk forslag, verifiser)
- purpose://digital-work.collect-structured-input [active] — Collect structured input
- purpose://questionnaire.campaign.complete [active] — Complete questionnaire campaign
- purpose://gui.quality.functional-accessible [active] — Functional accessible GUI
- purpose://skeleton.owner-entity-access [draft] — Owner entity access affordance
- purpose://questionnaire.access.audit [active] — Questionnaire access audit
- purpose://test.acceptance.questionnaire [active] — Questionnaire acceptance tests
- purpose://knowledge.explain-policy [draft] — Explain policy or rules
- purpose://value-and-commons [candidate] — Value and commons
- purpose://self-determination.data.manner [candidate] — Manner of processing and derived data
- purpose://access.audit.privacy.database-key-custody [candidate] — Eierstyrt kryptering og nøkkellagring for celledata


## 5. Avledede tester

| Test | Type | Hvordan | Bevis havner |
|---|---|---|---|
| T-R1 | inspeksjon | samtale med Sverre etter første publisering | ACCEPT.md#rot |
| T-A | inspeksjon | øktlogg med «dette lærte jeg» | ACCEPT.md#laering |
| T-A1 | artefakt | nivå 1–2 gjennomført i prototypen | ACCEPT.md#laeringssti |
| T-A2 | inspeksjon | ti forslag har forklaring og markerte linjer | TESTRESULT.md#forklaring |
| T-A3 | måling | Kjetil finner forrige økt på under ett minutt | TESTRESULT.md#mentor |
| T-B / T-B5 | kommando | kontraktvalidator; to profiler lastes av samme motor | TESTRESULT.md#profil |
| T-B1 | måling | tjue barneformulerte ønsker fra en uavhengig skribent | TESTRESULT.md#forsta |
| T-B2 | måling | tid fra forslag til forhåndsvisning, tre forsøk | TESTRESULT.md#forhandsvisning |
| T-B3 | inspeksjon | hvert forslag sporbart til bibliotekoppføring | ACCEPT.md#verktoyvalg |
| T-B4 | kommando | negative tester: uten klikk, feil bruker, ukjent formål | TESTRESULT.md#auth |
| T-B6 | inspeksjon | vanskelige meldinger, gjennomgått av Kjetil | ACCEPT.md#trygg |
| T-C | måling | oppslag for tjue formål | TESTRESULT.md#bibliotek |
| T-C1 | kommando | validator nekter oppføring uten purposeRef og lisens | TESTRESULT.md#bibliotek-validator |
| T-C2 | måling | treffrate med og uten tekstsøk, uavhengig sett | TESTRESULT.md#oppslag |
| T-C3 | kommando | bygg to ganger; fjernet celle forsvinner | TESTRESULT.md#utledet |
| T-C4 | inspeksjon | lisens og kilde per ressurs | ACCEPT.md#lisens |
| T-D1 | måling | fem bestillinger per motor | TESTRESULT.md#motor |
| T-D2 | kommando | ondsinnet testspill avvises | TESTRESULT.md#sandkasse |
| T-D3 | inspeksjon | samme prosjekt i to adaptere | ACCEPT.md#adapter |
| T-E / T-E1 | inspeksjon | spillprosjekt er WorkItem-poster | ACCEPT.md#prosjekt |
| T-E2 | kommando | ti endringer, tilbake til nummer tre | TESTRESULT.md#versjoner |
| T-E3 | inspeksjon | Sverre forklarer tre oppgaver | ACCEPT.md#oppgaver |
| T-F / T-F1 | måling | publisert spill på annen enhet, lastetid tre ganger | TESTRESULT.md#publisering |
| T-F2 | kommando | publisering uten godkjenning avvises | TESTRESULT.md#godkjenning |
| T-F3 | inspeksjon | ingen nettverkskall utenfor egen adresse | ACCEPT.md#personvern |
| T-G / T-G1 / T-G2 | inspeksjon | mot Scaffold_Product_Split_Plan; måling ved fase 3 | ACCEPT.md#scaffold |
| T-H / T-H1 | inspeksjon | fil:linje for hver påstand om implementert oppførsel | ACCEPT.md#docs |
| T-H2 | artefakt | ny tråd lager profil for Developer Workbench med skillen | ACCEPT.md#skills |
| T-H3 | kommando | `purpose_dev.py validate` grønn | TESTRESULT.md#validate |

## 6. Åpne spørsmål (bare de som endrer treet)
1. Hvor gammel er Sverre, og leser han godt? Det avgjør om nivå 1–2 skal ha blokker i stedet for tekst.
2. Hvilken enhet bruker han mest (iPad, PC eller Mac)? Det avgjør om prototypen må være laget for berøring først.
3. Hvilken modell skal hjelperen bruke for ham: Claude via AIGateway, eller en lokal modell?
4. Skal publiserte spill være åpne for alle, eller bare for familie og venner med lenke?

## 7. Revisjonslogg
| Dato | Iterasjon | Endring |
|---|---|---|
| 2026-10-09 | 1 | Første versjon: analyse, tre med 8 grener og 27 blad, motorvalg, scaffoldvurdering. |
| 2026-10-09 | 1.1 | Refs omdøpt til engelsk etter Kjetils innspill (titler fortsatt norske). Ingen formål endret. G1 godkjent 08:56Z. |
