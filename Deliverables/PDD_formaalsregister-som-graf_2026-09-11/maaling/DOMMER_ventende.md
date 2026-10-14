<!-- GENERATED; no judgments entered -->
# Ventende dommer: 15 oppgaver

Dette er en tom arbeidsblankett, ikke fasit. Fjern GENERATED-kommentaren før du skriver svar, slik at ny målekjøring ikke overskriver dem.
Kandidat 6 = tekst/perspektiv/skop (0,50/0,25/0,25); kandidat 1 = uendret TF-IDF. K=10, frosset 44-korpus.
Samme lærdom har samme nummer i begge kolonner. Unionen kan ha opptil 20 rader. Kolonnene er synlige etter bestilling; dette er ikke blind merking.

Et treff: ville forebyggingen endret et konkret valg, en test eller en avgrensning i oppgaven? Generelt gode råd er ikke nok.
Etter vanlig G1-lesing: svar 1) `1 3 ?4` (1,3 relevant; 4 uvurdert; resten i unionen irrelevant), eller `-` for ingen relevante. 2) `3=lesson.tidligere`, eller `-` når du ikke identifiserer gjentakelse. 3) `1=test.ref 3=u:sann-grunn`, eller `u:sann-grunn` for alle relevante. Ingen standardgrunn fylles inn. Lærdommer utenfor unionen er alltid uvurderte.
Oppgi `sekunder=…`; mål median <60 sekunder på første fem etter G1-lesingen, også andel uvurderte. Tidsmålet er ikke mennesketestet.
Å lese alt fra bunnen av er ikke lovet å ta under ett minutt. Utvid «Full tekst» ved behov (tilsvarer `v n` i judge). Svarene må valideres mot samme snapshot før import til purpose_dev.py judge-format; denne filen skriver ingen dom automatisk. Topp-10-pool gir dekning av poolens positive; ekte total R krever vurdering av alle 44 eller separat revisjonsutvalg.
Korpus: `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/korpus_44.json`; snapshotHash: `1437e34b2faa23210156cc71ef981e20cdd57ec18a0c2739a49e1d06ab26f00f`.

For en absolutt R+@10-forskjell på 0,15: ved antatt paret s_d=0,30 er normalanslaget 16 og t-intervallanslaget 18 vurderte, uavhengige oppgaver; planlegging med 80 % styrke gir 32 nye oppgaver. Ved s_d=0,50 gir det henholdsvis 43, 46 og 88. Ingen garanti for bootstrap-CI. De 15 nedenfor utvider utviklingsgrunnlaget; de er ikke 15 uavhengige bekreftende tester. Dagens fire source-oppgaver erstatter ikke menneskedommer.

## PDD_arbeidsko-ai-utforere_2026-09-07

**Simulert perspektiv:** Én arbeidskø, tre utførere, ingen postbud; Ett jobbformat = HAVEN-Deploy-task; Dispatcher på Mac-en. **Skop:** simulated-scope://deploy.
Oppgave: `CellProtocolDocuments/Deliverables/PDD_arbeidsko-ai-utforere_2026-09-07/FORMAALSSPEC.md` (§0/§1).

| Rang | Kandidat 6 | Kandidat 1 — TF-IDF |
|---:|---|---|
| 1 | **1** `lesson.paste-command-instead-of-queue` — Før enhver Codex-kjøring fra Cowork: ls HAVEN/_losen-queue/inbox running; tail logs/runner.log, legg jobben som <id>.job + <id>.prompt.md. A… | **1** `lesson.paste-command-instead-of-queue` — Før enhver Codex-kjøring fra Cowork: ls HAVEN/_losen-queue/inbox running; tail logs/runner.log, legg jobben som <id>.job + <id>.prompt.md. A… |
| 2 | **2** `lesson.codex-sandbox-cannot-reach-docker` — Deploy-/image-steg planlegges aldri som Codex-slice; de registreres som HAVEN-Deploy-post med eier Kjetil (eller en dispatcher-adapter med e… | **2** `lesson.codex-sandbox-cannot-reach-docker` — Deploy-/image-steg planlegges aldri som Codex-slice; de registreres som HAVEN-Deploy-post med eier Kjetil (eller en dispatcher-adapter med e… |
| 3 | **3** `lesson.codex-workspace-write-cannot-build-cellscaffold` — Lange bygg og testkjøringer legges ikke som workspace-write-køjobb. De kjøres som detached skript startet via Codex med danger-full-access o… | **3** `lesson.codex-workspace-write-cannot-build-cellscaffold` — Lange bygg og testkjøringer legges ikke som workspace-write-køjobb. De kjøres som detached skript startet via Codex med danger-full-access o… |
| 4 | **4** `lesson.a-new-red-test-needs-a-repeated-baseline` — Når en ny rød dukker opp: kjør basen på nytt, i et eget rent worktree, flere ganger (tre holder som regel), før du enten tar på deg feilen e… | **6** `lesson.queue-job-file-before-prompt` — Skriv <id>.prompt.md først og <id>.job sist, helst som mv fra en tmp-fil i samme mappe — .job er registreringssignalet, slik job.json er det… |
| 5 | **5** `lesson.pin-must-be-on-their-main` — Å pinne er riktig — det er det som gjør bygget reproduserbart. Kravet er at revisjonen er en forfar av avhengighetens egen main. Da er «bygg… | **11** `lesson.stop-rule-too-wide-stops-the-job` — Skriv stoppregler som navn og sti, ikke som kategori: «stopp hvis index.lock, HEAD.lock eller .lock finnes under <denne stien>». Navngi eksp… |
| 6 | **6** `lesson.queue-job-file-before-prompt` — Skriv <id>.prompt.md først og <id>.job sist, helst som mv fra en tmp-fil i samme mappe — .job er registreringssignalet, slik job.json er det… | **12** `lesson.codex-mcp-60s` — Bygg/test/lange jobber går via terminal codex exec eller filbasert overlevering, aldri via Codex-MCP. |
| 7 | **7** `lesson.swift-test-exit-code-lies-in-havenagentd` — Les resultatet fra linjen Test run with N tests in M suites passed/failed, ikke fra exitkoden, i alle skript og køjobber for dette repoet. O… | **13** `lesson.pkill-pattern-killed-the-queue-job` — Bruk aldri pkill -f <mønster> på en maskin der andre prosesser kan ha teksten i argv. Stopp en prosess ved PID du selv startet, eller ved pg… |
| 8 | **8** `lesson.baseline-measured-another-pdds-branch` — WP0 måler en ren eksport av den revisjonen arbeidet skal gå ut fra (git archive <rev> \| tar -x -C <scratch>), ikke det delte arbeidstreet. … | **14** `lesson.zsh-no-inline-comments` — Aldri forklaring på samme linje som en kommando; skript har '"#") break ;;' i argumentparseren. |
| 9 | **9** `lesson.syntax-check-reported-as-delivered` — En implementeringsslice er ikke levert før et detached bygg med danger-full-access er kjørt mot arbeidstreet og både bygg og de nye testene … | **15** `lesson.worktree-created-from-vm-has-unusable-gitdir` — Opprett worktrees fra macOS (Codex), ikke fra VM-en. Er det allerede gjort fra VM-en: skriv om begge pekerfilene til macOS-stien og verifise… |
| 10 | **10** `lesson.a-red-baseline-is-a-question-not-an-answer` — Svar på tre spørsmål før du gjør noe med en rød baseline: er utsjekket mitt likt origin? er CI grønn på origin/main? hvilken commit gjorde d… | **16** `lesson.entityanchor-keypaths-are-registered` — Skriv aldri testdata til en oppdiktet keypath på en celle. Finn en keypath cellen faktisk registrerer, helst en annen test som allerede bruk… |

Union: 16 lærdommer; øvrige 28 uvurderte.
- Relevans: 
- Gjentakelser: 
- Håndhevelse / sann grunn: 
- Sekunder: 

<details><summary>Full tekst og testreferanser</summary>

**1 — lesson.paste-command-instead-of-queue**

Symptom: Kjetil fikk et innlimingsskript for å starte Codex; flagget --full-auto finnes ikke på `codex exec`, og kjøringen feilet ved første linje.

Forebygging: Før enhver Codex-kjøring fra Cowork: `ls HAVEN/_losen-queue/inbox running; tail logs/runner.log`, legg jobben som <id>.job + <id>.prompt.md. Aldri gi Kjetil kommandoer å lime inn. Gyldige `codex exec`-flagg: --sandbox, --skip-git-repo-check, -C.

**2 — lesson.codex-sandbox-cannot-reach-docker**

Symptom: S10 (docker compose build/up) endte i `permission denied … docker.sock` i Codex-sandkassen; deploy-slicen ble blocked.

Forebygging: Deploy-/image-steg planlegges aldri som Codex-slice; de registreres som HAVEN-Deploy-post med eier Kjetil (eller en dispatcher-adapter med eksplisitt docker-rettighet når arbeidskø-PDD-en er levert). Se HD-0012.

**3 — lesson.codex-workspace-write-cannot-build-cellscaffold**

Symptom: WP0-baselinen i køen ble blocked: `sandbox-exec: sandbox_apply: Operation not permitted`. Testkommandoen brukte 1 604 sekunder uten at én eneste test startet.

Forebygging: Lange bygg og testkjøringer legges ikke som `workspace-write`-køjobb. De kjøres som detached skript startet via Codex med `danger-full-access` og python Popen(start_new_session=True), med logg i en montert mappe som Cowork kan polle — samme mønster som produserte den notariserte HavenAgentD-pakken 2026-09-08. Køjobber brukes til analyse, kontrakter, dokumentasjon og korte kommandoer.

**4 — lesson.a-new-red-test-needs-a-repeated-baseline**

Symptom: Første fulle kjøring med nye endringer viste to røde i stedet for baselinens én, og den nye lå i en fil jeg hadde endret. Det så ut som en regresjon jeg hadde innført.

Forebygging: Når en ny rød dukker opp: kjør basen på nytt, i et eget rent worktree, **flere ganger** (tre holder som regel), før du enten tar på deg feilen eller avfeier den. Skriv resultatet av gjentakelsen i TESTRESULT — «2 av 3 på ren base» er et svar, «den er nok flaky» er ikke. Det koster ti minutter og avgjør om du bruker natten på å jage din egen feil eller andres.

**5 — lesson.pin-must-be-on-their-main**

Symptom: En revisjonspin i Package.swift pekte på en CellProtocol-revisjon som ikke lå på CellProtocol sin main. Koden bygde bare på den ene maskinen som hadde revisjonen liggende lokalt.

Forebygging: Å pinne er riktig — det er det som gjør bygget reproduserbart. Kravet er at revisjonen er en forfar av avhengighetens egen main. Da er «bygg fra andres main» og «reproduserbart bygg» samme krav. HavenAgentD::Scripts/assert_dependencies_are_on_their_main.sh håndhever det, og CI kjører den. Lander du en klient før cellen den bruker er på den andres main, har du laget et repo som bare bygger hos deg.

**6 — lesson.queue-job-file-before-prompt**

Symptom: Køjobben `formaalskomposisjon-fullfor-commit-20260910-1020` ble avvist med «mangler promptfil» 13 sekunder etter at `.job` ble skrevet; promptfilen kom to sekunder etter avvisningen og ligger foreldreløs i `_losen-queue/inbox/`, der runneren aldri ser den igjen.

Forebygging: Skriv `<id>.prompt.md` først og `<id>.job` sist, helst som `mv` fra en tmp-fil i samme mappe — `.job` er registreringssignalet, slik `job.json` er det i HavenAgentD::Docs/AgentJobs.md. Kan bli derivedTest: runneren eller `hd validate` rapporterer enhver `inbox/*.prompt.md` uten tilhørende `.job`, eldre enn to minutter, som foreldreløs.

**7 — lesson.swift-test-exit-code-lies-in-havenagentd**

Symptom: `swift test` i HavenAgentD avslutter med 1 selv når samtlige 212 tester passerer. Et skript som leser `$?` melder rødt på et helt grønt tre.

Forebygging: Les resultatet fra linjen `Test run with N tests in M suites passed/failed`, ikke fra exitkoden, i alle skript og køjobber for dette repoet. Og fjern det tomme XCTest-målet, eller bygg det for riktig arkitektur, før noen setter opp CI her — ellers vil CI være rød uansett hva som gjøres.

**8 — lesson.baseline-measured-another-pdds-branch**

Symptom: WP0 målte `pdd/tillitspakke-agentflaate` med 181 skitne oppføringer, ikke et rent utgangspunkt for sin egen PDD. En regresjonsbaseline derfra sier ingenting om hva denne PDD-en endrer.

Forebygging: WP0 måler en ren eksport av den revisjonen arbeidet skal gå ut fra (`git archive <rev> | tar -x -C <scratch>`), ikke det delte arbeidstreet. Er arbeidstreet opptatt av en annen PDD, er det en planopplysning som hører i STATUS, ikke noe implementeringen skal jobbe rundt.

**9 — lesson.syntax-check-reported-as-delivered**

Symptom: WP1 ble rapportert som «kode og 7 tester levert, syntakssjekken bestod». Et faktisk bygg ga 50 kompileringsfeil, og testene feilet 4 av 7 da de først kunne kjøre.

Forebygging: En implementeringsslice er ikke levert før et detached bygg med `danger-full-access` er kjørt mot arbeidstreet og både bygg og de nye testene er grønne. Legg byggejobben klar FØR slicen kjøres, og skriv i prompten at slicen skal rapportere «skrevet, ikke verifisert» — ikke «levert».

**10 — lesson.a-red-baseline-is-a-question-not-an-answer**

Symptom: En rød baseline ble behandlet som en opplysning om prosjektet, og arbeidet gikk videre med et tiltak som gjorde den grønn. Tiltaket skjulte årsaken i stedet for å fjerne den.

Forebygging: Svar på tre spørsmål før du gjør noe med en rød baseline: er utsjekket mitt likt origin? er CI grønn på origin/main? hvilken commit gjorde den rød, og hvem eier den? Først når svaret er «prosjektet er faktisk rødt» er det riktig å jobbe rundt det — og da som en egen, navngitt sak, ikke som en stille lokal omgåelse.

**11 — lesson.stop-rule-too-wide-stops-the-job**

Symptom: En commit-jobb til Codex stoppet før første `git add` fordi stoppregelen sa «finner du `.git/index.lock` eller annen låsefil: stopp». Et rekursivt søk fant 25 filer som heter `locked` under andre arbeidstrær — normale `git worktree lock`-markører som ikke blokkerer noe. Jobben gjorde ingenting, og hele runden gikk tapt.

Forebygging: Skriv stoppregler som navn og sti, ikke som kategori: «stopp hvis `index.lock`, `HEAD.lock` eller `*.lock` finnes under `<denne stien>`». Navngi eksplisitt det som ser ut som en treffer men ikke er det, og si at det skal ignoreres. Legg alltid til «stopp hvis kommandoen faktisk avvises med denne feilen» — en filsøk-treffliste er ikke et bevis på blokkering. Samme gjelder alle vide vendinger i en prompt: «eller lignende», «eller annet», «eventuelle andre».

**12 — lesson.codex-mcp-60s**

Symptom: Codex-MCP-kall kuttes etter ~60 s; registerlesning og Swift-bygg sprengte taket.

Forebygging: Bygg/test/lange jobber går via terminal codex exec eller filbasert overlevering, aldri via Codex-MCP.

**13 — lesson.pkill-pattern-killed-the-queue-job**

Symptom: En commit-jobb i Losen-køen døde med EXIT=143 tolv sekunder etter start. Ingen feilmelding, ingen commit. Årsaken var min egen opprydding i et annet skript: `pkill -f "<appnavn>"`.

Forebygging: Bruk aldri `pkill -f <mønster>` på en maskin der andre prosesser kan ha teksten i argv. Stopp en prosess ved PID du selv startet, eller ved `pgrep -x <prosessnavn>` kombinert med en sjekk av `ps -o comm=` mot den nøyaktige kjørbare stien. Dette gjelder særlig når en jobbkø kjører prompter som argument: alt du skriver i en prompt står på en kommandolinje et sted.

**14 — lesson.zsh-no-inline-comments**

Symptom: Begge kommandolinjene feilet med 'ukjent argument: #' og ingenting kjørte.

Forebygging: Aldri forklaring på samme linje som en kommando; skript har '"#"*) break ;;' i argumentparseren.

**15 — lesson.worktree-created-from-vm-has-unusable-gitdir**

Symptom: WP1 ble blocked etter ett minutt: `fatal: not a git repository: /sessions/<sesjon>/mnt/CellScaffold/.git/worktrees/_wt-sad-20260909`, exit 128. Branch og HEAD kunne ikke bekreftes.

Forebygging: Opprett worktrees fra macOS (Codex), ikke fra VM-en. Er det allerede gjort fra VM-en: skriv om begge pekerfilene til macOS-stien og verifiser `branch --show-current` + `rev-parse HEAD` **fra macOS** før noen jobb legges i køen. En jobb skal aldri være første stedet en sti blir prøvd.

**16 — lesson.entityanchor-keypaths-are-registered**

Symptom: WP2-testen skrev en sentinel til `profile` på abonnentens EntityAnchor og fikk `notFound` ved gjenlesing. Skrivingen ga ingen feil.

Forebygging: Skriv aldri testdata til en oppdiktet keypath på en celle. Finn en keypath cellen faktisk registrerer, helst en annen test som allerede bruker den. At et `set` går gjennom er ikke bevis på at keypathen finnes.

Kjente testrefs (eksistens i snapshot er ikke bevis for at testen er kjørt): `test.build`, `test.cell.auth-negative`, `test.cell.contract-fixtures`, `test.cell.stub-scan`, `test.cells.capability-audit`, `test.cells.dataflow-matches-contracts`, `test.docs-updated`, `test.gui.load-time`, `test.gui.parity`, `test.gui.reference-image-exists`, `test.handoff.dry-run`, `test.ko.board`, `test.ko.cell`, `test.ko.claude`, `test.ko.codex`, `test.ko.dispatch`, `test.ko.e2e`, `test.ko.from-cowork`, `test.ko.lesson`, `test.ko.no-escalation`, `test.ko.no-shell`, `test.ko.schema`, `test.regression`, `test.skeleton.no-unreachable-elements`, `test.skeleton.purpose-actions-reachable`, `test.status-current`

</details>

## PDD_bridge-fase2-handshake_2026-09-04

**Simulert perspektiv:** Multipleks uten svekket grense; Handshake-scope er eksplisitt; Autorisasjon per kanalåpning. **Skop:** simulated-scope://bridge.
Oppgave: `CellProtocolDocuments/Deliverables/PDD_bridge-fase2-handshake_2026-09-04/FORMAALSSPEC.md` (§0/§1).

| Rang | Kandidat 6 | Kandidat 1 — TF-IDF |
|---:|---|---|
| 1 | **1** `lesson.cellscaffold-two-holes` — Ikke porter celler fra CellScaffold til PalazzoScaffold uten å lukke begge hullene; og må være grønne. | **8** `lesson.cellbase-decodingerror-shadows-swift` — I App-modulen: skriv Swift.DecodingError når du vil ha standardbibliotekets. Gjelder generelt for typenavn CellBase også definerer — sjekk m… |
| 2 | **2** `lesson.entityanchor-keypaths-are-registered` — Skriv aldri testdata til en oppdiktet keypath på en celle. Finn en keypath cellen faktisk registrerer, helst en annen test som allerede bruk… | **3** `lesson.codex-workspace-write-cannot-build-cellscaffold` — Lange bygg og testkjøringer legges ikke som workspace-write-køjobb. De kjøres som detached skript startet via Codex med danger-full-access o… |
| 3 | **3** `lesson.codex-workspace-write-cannot-build-cellscaffold` — Lange bygg og testkjøringer legges ikke som workspace-write-køjobb. De kjøres som detached skript startet via Codex med danger-full-access o… | **10** `lesson.local-main-is-not-main` — Før du måler en baseline eller sier at main er rød: git fetch origin main og sammenlign. Er lokal main foran origin/main, er de commitene ik… |
| 4 | **4** `lesson.worktree-created-from-vm-has-unusable-gitdir` — Opprett worktrees fra macOS (Codex), ikke fra VM-en. Er det allerede gjort fra VM-en: skriv om begge pekerfilene til macOS-stien og verifise… | **4** `lesson.worktree-created-from-vm-has-unusable-gitdir` — Opprett worktrees fra macOS (Codex), ikke fra VM-en. Er det allerede gjort fra VM-en: skriv om begge pekerfilene til macOS-stien og verifise… |
| 5 | **5** `lesson.ciphertext-field-held-plaintext-hash` — En paastand om at noe er kryptert, signert eller verifisert skal bekreftes paa artefaktet - les bytene, ikke feltet. Et felt som heter ciphe… | **11** `lesson.pin-must-be-on-their-main` — Å pinne er riktig — det er det som gjør bygget reproduserbart. Kravet er at revisjonen er en forfar av avhengighetens egen main. Da er «bygg… |
| 6 | **6** `lesson.undocumented-plan-switch` — STATUS.md i oppgavemappen oppdateres ved hvert planbytte med dato og hvorfor; sjekkes i | **1** `lesson.cellscaffold-two-holes` — Ikke porter celler fra CellScaffold til PalazzoScaffold uten å lukke begge hullene; og må være grønne. |
| 7 | **7** `lesson.test-the-representation-not-the-issuance-flow` — Skille to spørsmål: «hvordan får noen rollen» og «hva gir rollen». Tester du det andre, installer rollen på husets etablerte måte og test vi… | **7** `lesson.test-the-representation-not-the-issuance-flow` — Skille to spørsmål: «hvordan får noen rollen» og «hva gir rollen». Tester du det andre, installer rollen på husets etablerte måte og test vi… |
| 8 | **8** `lesson.cellbase-decodingerror-shadows-swift` — I App-modulen: skriv Swift.DecodingError når du vil ha standardbibliotekets. Gjelder generelt for typenavn CellBase også definerer — sjekk m… | **12** `lesson.scaffold-without-porthole-host-has-no-preview` — For scaffolds uten Porthole-vert: (1) images/README.md må si eksplisitt at bildene er mockups og hva skeleton ikke kan rendre, (2) paritet (… |
| 9 | **9** `lesson.valuetype-equality-false-for-objects` — Aldri assert på hele sammensatte ValueType-verdier. Sammenlign kanonisk JSON (JSONEncoder med .sortedKeys) eller pakk ut og sammenlign felt … | **2** `lesson.entityanchor-keypaths-are-registered` — Skriv aldri testdata til en oppdiktet keypath på en celle. Finn en keypath cellen faktisk registrerer, helst en annen test som allerede bruk… |
| 10 | **10** `lesson.local-main-is-not-main` — Før du måler en baseline eller sier at main er rød: git fetch origin main og sammenlign. Er lokal main foran origin/main, er de commitene ik… | **13** `lesson.bridge-inferred-architecture-from-one-use` — Erklær hver kapabilitet oppgaven bygger på som eget formål med kilde og Avgrensning (pkg.std.cell-combination). |

Union: 13 lærdommer; øvrige 31 uvurderte.
- Relevans: 
- Gjentakelser: 
- Håndhevelse / sann grunn: 
- Sekunder: 

<details><summary>Full tekst og testreferanser</summary>

**1 — lesson.cellscaffold-two-holes**

Symptom: CellScaffold har tomme booking-/concierge-stubber og autorisasjon som kaster nøkkelstien og bare sjekker eierskap.

Forebygging: Ikke porter celler fra CellScaffold til PalazzoScaffold uten å lukke begge hullene; test.cell.auth-negative og test.cell.stub-scan må være grønne.

**2 — lesson.entityanchor-keypaths-are-registered**

Symptom: WP2-testen skrev en sentinel til `profile` på abonnentens EntityAnchor og fikk `notFound` ved gjenlesing. Skrivingen ga ingen feil.

Forebygging: Skriv aldri testdata til en oppdiktet keypath på en celle. Finn en keypath cellen faktisk registrerer, helst en annen test som allerede bruker den. At et `set` går gjennom er ikke bevis på at keypathen finnes.

**3 — lesson.codex-workspace-write-cannot-build-cellscaffold**

Symptom: WP0-baselinen i køen ble blocked: `sandbox-exec: sandbox_apply: Operation not permitted`. Testkommandoen brukte 1 604 sekunder uten at én eneste test startet.

Forebygging: Lange bygg og testkjøringer legges ikke som `workspace-write`-køjobb. De kjøres som detached skript startet via Codex med `danger-full-access` og python Popen(start_new_session=True), med logg i en montert mappe som Cowork kan polle — samme mønster som produserte den notariserte HavenAgentD-pakken 2026-09-08. Køjobber brukes til analyse, kontrakter, dokumentasjon og korte kommandoer.

**4 — lesson.worktree-created-from-vm-has-unusable-gitdir**

Symptom: WP1 ble blocked etter ett minutt: `fatal: not a git repository: /sessions/<sesjon>/mnt/CellScaffold/.git/worktrees/_wt-sad-20260909`, exit 128. Branch og HEAD kunne ikke bekreftes.

Forebygging: Opprett worktrees fra macOS (Codex), ikke fra VM-en. Er det allerede gjort fra VM-en: skriv om begge pekerfilene til macOS-stien og verifiser `branch --show-current` + `rev-parse HEAD` **fra macOS** før noen jobb legges i køen. En jobb skal aldri være første stedet en sti blir prøvd.

**5 — lesson.ciphertext-field-held-plaintext-hash**

Symptom: Losen fortalte Kjetil at lyd allerede var kryptert i lagring. Det var feil: filene i prod begynner med ID3 og er vanlig MP3. To ting forte dit. (1) Krypteringskoden som ble lest tilhorer MusicIngestCell paa /mvp/ingest/local, mens Butterpop publiserer gjennom MusicAssetStoreCell.storeLocalAsset, som skriver bytene slik de kommer. (2) storeLocalAsset setter ciphertextSHA256 = plaintextSHA256 = sha256(data), saa manifestet ser kryptert ut selv naar encryptionPolicy er none.

Forebygging: En paastand om at noe er kryptert, signert eller verifisert skal bekreftes paa artefaktet - les bytene, ikke feltet. Et felt som heter ciphertext* skal ikke settes naar encryptionPolicy er none; enten utelates det, eller navnet sier hva det er. Kan bli derivedTest: manifest med encryptionPolicy none har ingen ciphertext-verdi.

**6 — lesson.undocumented-plan-switch**

Symptom: Tre produktive døgn (22.–24.08) så tomme ut i alle statusdokumenter fordi planbyttet fra bølge 1–3 til deploy-seremonien aldri ble skrevet ned.

Forebygging: STATUS.md i oppgavemappen oppdateres ved hvert planbytte med dato og hvorfor; sjekkes i test.status-current.

**7 — lesson.test-the-representation-not-the-issuance-flow**

Symptom: Alle fire WP4-rolletestene feilet i oppsettet, ikke i det de skulle teste: `deniedNoGrant` på `requestEntry` mot `cell:///AdminEntry`. Testen fikk aldri gitt identiteten rollen.

Forebygging: Skille to spørsmål: «hvordan får noen rollen» og «hva gir rollen». Tester du det andre, installer rollen på husets etablerte måte og test virkningen. Let alltid etter en eksisterende `*TestSupport`-hjelper før du bygger oppsettet selv — `grep -rn "TestSupport" CellScaffold::Tests` — og se hvilke argumenter de andre testene gir den.

**8 — lesson.cellbase-decodingerror-shadows-swift**

Symptom: WP1s nye celle ga 50 kompileringsfeil: `type 'DecodingError' has no member 'dataCorruptedError'` og `cannot infer contextual base in reference to member 'registry'`, alle fra én linje.

Forebygging: I App-modulen: skriv `Swift.DecodingError` når du vil ha standardbibliotekets. Gjelder generelt for typenavn CellBase også definerer — sjekk med `grep -rn "enum <Navn>" CellProtocol::Sources/CellBase` før du antar at et kjent Foundation-navn er Foundations.

**9 — lesson.valuetype-equality-false-for-objects**

Symptom: Fire av sju WP1-tester feilet på `XCTAssertEqual` mellom to `ValueType.object` som hadde identisk innhold. Feilmeldingen viste samme nøkler og verdier på begge sider, i ulik rekkefølge.

Forebygging: Aldri assert på hele sammensatte `ValueType`-verdier. Sammenlign kanonisk JSON (`JSONEncoder` med `.sortedKeys`) eller pakk ut og sammenlign felt for felt. Skalarer (`.string`, `.integer`, `.bool`, `.null`) sammenlignes trygt. Merk: dette er et funn i CellBase, ikke bare en testregel — App-kildene destrukturerer riktignok før sammenligning, men en fremtidig `==` på hele verdier vil stille behandle like verdier som ulike. Ikke revidert utover App-kildene.

**10 — lesson.local-main-is-not-main**

Symptom: WP0-baselinen var rød og ble meldt som «main bygger ikke». Det var feil. Den commiten baselinen ble målt mot, `ba14895`, lå bare på den LOKALE main-grenen og var aldri pushet; den avhang av CellBase-kode som heller ikke var pushet. origin/main lå fire commits lenger fram, pinnet CellProtocol til en revisjon som ER på CellProtocol sin main, og hadde grønn CI hele tiden. Et helt døgns arbeid ble bygget oppå den lokale commiten.

Forebygging: Før du måler en baseline eller sier at main er rød: `git fetch origin main` og sammenlign. Er lokal main foran origin/main, er de commitene ikke main for andre — bygg aldri videre på dem. Se på CI for origin/main før du konkluderer. `swift package edit` skal aldri være på når noe måles eller meldes verifisert. Og den eneste sjekken som virkelig avgjør: klon fra GitHub til en tom katalog og bygg der. HavenAgentD::Scripts/preflight_before_landing.sh stiller alle fire spørsmålene.

**11 — lesson.pin-must-be-on-their-main**

Symptom: En revisjonspin i Package.swift pekte på en CellProtocol-revisjon som ikke lå på CellProtocol sin main. Koden bygde bare på den ene maskinen som hadde revisjonen liggende lokalt.

Forebygging: Å pinne er riktig — det er det som gjør bygget reproduserbart. Kravet er at revisjonen er en forfar av avhengighetens egen main. Da er «bygg fra andres main» og «reproduserbart bygg» samme krav. HavenAgentD::Scripts/assert_dependencies_are_on_their_main.sh håndhever det, og CI kjører den. Lander du en klient før cellen den bruker er på den andres main, har du laget et repo som bare bygger hos deg.

**12 — lesson.scaffold-without-porthole-host-has-no-preview**

Symptom: G1-GUI måtte bruke mockups rendret fra skeleton-JSON; ekte Porthole-preview var umulig.

Forebygging: For scaffolds uten Porthole-vert: (1) images/README.md må si eksplisitt at bildene er mockups og hva skeleton ikke kan rendre, (2) paritet (test.gui.parity) planlegges som egen slice med kjørende scaffold + Binding/Porthole via bridge, ikke som del av implementeringsjobben.

**13 — lesson.bridge-inferred-architecture-from-one-use**

Symptom: En kodeassistent sluttet fra én observert bruksmåte av bridge til en egenskap ved arkitekturen og konkluderte feil.

Forebygging: Erklær hver kapabilitet oppgaven bygger på som eget formål med kilde og Avgrensning (pkg.std.cell-combination).

Kjente testrefs (eksistens i snapshot er ikke bevis for at testen er kjørt): `test.bridge.channel-cap`, `test.bridge.channel-open-authz`, `test.bridge.contract-fixtures`, `test.bridge.session-scope-negative`, `test.bridge.setup-error-fanout`, `test.bridge.socket-loss`, `test.bridge.upgrade-parity`, `test.build`, `test.cell.auth-negative`, `test.cell.contract-fixtures`, `test.cell.stub-scan`, `test.cells.capability-audit`, `test.cells.dataflow-matches-contracts`, `test.docs-updated`, `test.gui.load-time`, `test.gui.parity`, `test.gui.reference-image-exists`, `test.handoff.dry-run`, `test.regression`, `test.skeleton.no-unreachable-elements`, `test.skeleton.purpose-actions-reachable`, `test.status-current`

</details>

## PDD_butler-traadtre-og-widgetflate_2026-09-11

**Simulert perspektiv:** Rot —; ### A. Hjelpertre med ruting og skop —; ### B. Dra element ut av en flate og feste det —. **Skop:** simulated-scope://arbeid.
Oppgave: `CellProtocolDocuments/Deliverables/PDD_butler-traadtre-og-widgetflate_2026-09-11/FORMAALSSPEC.md` (§0/§1).

| Rang | Kandidat 6 | Kandidat 1 — TF-IDF |
|---:|---|---|
| 1 | **1** `lesson.stop-rule-too-wide-stops-the-job` — Skriv stoppregler som navn og sti, ikke som kategori: «stopp hvis index.lock, HEAD.lock eller .lock finnes under <denne stien>». Navngi eksp… | **5** `lesson.branch-is-empty-after-eight-work-packages` — Skill «filene finnes» fra «branchen har dem». Sjekk git rev-parse <branch> mot git rev-parse <base> som del av hver verifikasjon som påstår … |
| 2 | **2** `lesson.cellbase-decodingerror-shadows-swift` — I App-modulen: skriv Swift.DecodingError når du vil ha standardbibliotekets. Gjelder generelt for typenavn CellBase også definerer — sjekk m… | **1** `lesson.stop-rule-too-wide-stops-the-job` — Skriv stoppregler som navn og sti, ikke som kategori: «stopp hvis index.lock, HEAD.lock eller .lock finnes under <denne stien>». Navngi eksp… |
| 3 | **3** `lesson.codex-workspace-write-cannot-build-cellscaffold` — Lange bygg og testkjøringer legges ikke som workspace-write-køjobb. De kjøres som detached skript startet via Codex med danger-full-access o… | **6** `lesson.local-main-is-not-main` — Før du måler en baseline eller sier at main er rød: git fetch origin main og sammenlign. Er lokal main foran origin/main, er de commitene ik… |
| 4 | **4** `lesson.pkill-pattern-killed-the-queue-job` — Bruk aldri pkill -f <mønster> på en maskin der andre prosesser kan ha teksten i argv. Stopp en prosess ved PID du selv startet, eller ved pg… | **7** `lesson.unresolvable-condition-is-invisible` — SkeletonReachabilityAudit kjores over hver flate; feiler med elementene som aldri kan sees og handlingene som gaar tapt med dem. Betingelser… |
| 5 | **5** `lesson.branch-is-empty-after-eight-work-packages` — Skill «filene finnes» fra «branchen har dem». Sjekk git rev-parse <branch> mot git rev-parse <base> som del av hver verifikasjon som påstår … | **11** `lesson.scaffold-without-porthole-host-has-no-preview` — For scaffolds uten Porthole-vert: (1) images/README.md må si eksplisitt at bildene er mockups og hva skeleton ikke kan rendre, (2) paritet (… |
| 6 | **6** `lesson.local-main-is-not-main` — Før du måler en baseline eller sier at main er rød: git fetch origin main og sammenlign. Er lokal main foran origin/main, er de commitene ik… | **12** `lesson.pin-must-be-on-their-main` — Å pinne er riktig — det er det som gjør bygget reproduserbart. Kravet er at revisjonen er en forfar av avhengighetens egen main. Da er «bygg… |
| 7 | **7** `lesson.unresolvable-condition-is-invisible` — SkeletonReachabilityAudit kjores over hver flate; feiler med elementene som aldri kan sees og handlingene som gaar tapt med dem. Betingelser… | **10** `lesson.text-ux-is-not-design` — Rendret bilde (Porthole-preview eller mockup) godkjennes før implementering; bildet er akseptansereferanse. |
| 8 | **8** `lesson.plan-instead-of-delivery` — G1 godkjenner formål, ikke arbeid; etter G2 telles bare artefakter listet i §3 'Det du kommer til å se' som fremdrift. Et dokument om levera… | **2** `lesson.cellbase-decodingerror-shadows-swift` — I App-modulen: skriv Swift.DecodingError når du vil ha standardbibliotekets. Gjelder generelt for typenavn CellBase også definerer — sjekk m… |
| 9 | **9** `lesson.surface-load-alias-miss` — Mål lastetid tre ganger og sjekk logg for navnebom før en flate erklæres ferdig; aliaser må løses server-side eller ikke brukes. | **3** `lesson.codex-workspace-write-cannot-build-cellscaffold` — Lange bygg og testkjøringer legges ikke som workspace-write-køjobb. De kjøres som detached skript startet via Codex med danger-full-access o… |
| 10 | **10** `lesson.text-ux-is-not-design` — Rendret bilde (Porthole-preview eller mockup) godkjennes før implementering; bildet er akseptansereferanse. | **13** `lesson.tested-a-different-path-than-production` — Naar en test skal si noe om hva brukeren ser, maa den bruke produksjonens egen kodevei - helst produksjonens egen funksjon med produksjonens… |

Union: 13 lærdommer; øvrige 31 uvurderte.
- Relevans: 
- Gjentakelser: 
- Håndhevelse / sann grunn: 
- Sekunder: 

<details><summary>Full tekst og testreferanser</summary>

**1 — lesson.stop-rule-too-wide-stops-the-job**

Symptom: En commit-jobb til Codex stoppet før første `git add` fordi stoppregelen sa «finner du `.git/index.lock` eller annen låsefil: stopp». Et rekursivt søk fant 25 filer som heter `locked` under andre arbeidstrær — normale `git worktree lock`-markører som ikke blokkerer noe. Jobben gjorde ingenting, og hele runden gikk tapt.

Forebygging: Skriv stoppregler som navn og sti, ikke som kategori: «stopp hvis `index.lock`, `HEAD.lock` eller `*.lock` finnes under `<denne stien>`». Navngi eksplisitt det som ser ut som en treffer men ikke er det, og si at det skal ignoreres. Legg alltid til «stopp hvis kommandoen faktisk avvises med denne feilen» — en filsøk-treffliste er ikke et bevis på blokkering. Samme gjelder alle vide vendinger i en prompt: «eller lignende», «eller annet», «eventuelle andre».

**2 — lesson.cellbase-decodingerror-shadows-swift**

Symptom: WP1s nye celle ga 50 kompileringsfeil: `type 'DecodingError' has no member 'dataCorruptedError'` og `cannot infer contextual base in reference to member 'registry'`, alle fra én linje.

Forebygging: I App-modulen: skriv `Swift.DecodingError` når du vil ha standardbibliotekets. Gjelder generelt for typenavn CellBase også definerer — sjekk med `grep -rn "enum <Navn>" CellProtocol::Sources/CellBase` før du antar at et kjent Foundation-navn er Foundations.

**3 — lesson.codex-workspace-write-cannot-build-cellscaffold**

Symptom: WP0-baselinen i køen ble blocked: `sandbox-exec: sandbox_apply: Operation not permitted`. Testkommandoen brukte 1 604 sekunder uten at én eneste test startet.

Forebygging: Lange bygg og testkjøringer legges ikke som `workspace-write`-køjobb. De kjøres som detached skript startet via Codex med `danger-full-access` og python Popen(start_new_session=True), med logg i en montert mappe som Cowork kan polle — samme mønster som produserte den notariserte HavenAgentD-pakken 2026-09-08. Køjobber brukes til analyse, kontrakter, dokumentasjon og korte kommandoer.

**4 — lesson.pkill-pattern-killed-the-queue-job**

Symptom: En commit-jobb i Losen-køen døde med EXIT=143 tolv sekunder etter start. Ingen feilmelding, ingen commit. Årsaken var min egen opprydding i et annet skript: `pkill -f "<appnavn>"`.

Forebygging: Bruk aldri `pkill -f <mønster>` på en maskin der andre prosesser kan ha teksten i argv. Stopp en prosess ved PID du selv startet, eller ved `pgrep -x <prosessnavn>` kombinert med en sjekk av `ps -o comm=` mot den nøyaktige kjørbare stien. Dette gjelder særlig når en jobbkø kjører prompter som argument: alt du skriver i en prompt står på en kommandolinje et sted.

**5 — lesson.branch-is-empty-after-eight-work-packages**

Symptom: Åtte arbeidspakker rapportert utført og verifisert, ACCEPT.md skrevet — men `git branch -v` viste at `pdd/scaffold-admin-delegering` fortsatt pekte på samme commit som `main` (`e1f3e22f`). All koden lå ucommittet i et worktree som bare finnes på én maskin. Ett tapt worktree = 2 750 linjer kode og test borte, med full dokumentasjon på at arbeidet var «levert».

Forebygging: Skill «filene finnes» fra «branchen har dem». Sjekk `git rev-parse <branch>` mot `git rev-parse <base>` som del av hver verifikasjon som påstår at noe ligger på en branch; er de like, er branchen tom. Legg en commit-pakke inn i planen etter første grønne bygg, ikke etter siste arbeidspakke. Når worktreet bare kan leses fra macOS, kjør sjekken der — ikke hopp over den fordi verktøyet svarer feil.

**6 — lesson.local-main-is-not-main**

Symptom: WP0-baselinen var rød og ble meldt som «main bygger ikke». Det var feil. Den commiten baselinen ble målt mot, `ba14895`, lå bare på den LOKALE main-grenen og var aldri pushet; den avhang av CellBase-kode som heller ikke var pushet. origin/main lå fire commits lenger fram, pinnet CellProtocol til en revisjon som ER på CellProtocol sin main, og hadde grønn CI hele tiden. Et helt døgns arbeid ble bygget oppå den lokale commiten.

Forebygging: Før du måler en baseline eller sier at main er rød: `git fetch origin main` og sammenlign. Er lokal main foran origin/main, er de commitene ikke main for andre — bygg aldri videre på dem. Se på CI for origin/main før du konkluderer. `swift package edit` skal aldri være på når noe måles eller meldes verifisert. Og den eneste sjekken som virkelig avgjør: klon fra GitHub til en tom katalog og bygg der. HavenAgentD::Scripts/preflight_before_landing.sh stiller alle fire spørsmålene.

**7 — lesson.unresolvable-condition-is-invisible**

Symptom: Relasjoner-flaten viste tittel og ingen vei inn: ingen filopplasting, ingen knapper. Alle tester gronne.

Forebygging: SkeletonReachabilityAudit kjores over hver flate; test.skeleton.no-unreachable-elements feiler med elementene som aldri kan sees og handlingene som gaar tapt med dem. Betingelser hoerer hjemme inne i List/Grid/Reference-rader, der radens verdi sendes videre; ellers skal cellen avgjore og innhold bindes.

**8 — lesson.plan-instead-of-delivery**

Symptom: Kjetil ba om en leveranse flere ganger og fikk planer/dokumenter om leveransen i stedet.

Forebygging: G1 godkjenner formål, ikke arbeid; etter G2 telles bare artefakter listet i §3 'Det du kommer til å se' som fremdrift. Et dokument om leveransen teller aldri som leveransen.

**9 — lesson.surface-load-alias-miss**

Symptom: Flatelasting tok 46 541 ms (klientens 45 s-timeout) ved bom, 5 000 ms ved treff; målingen 10.08 målte en mislykket lasting.

Forebygging: Mål lastetid tre ganger og sjekk logg for navnebom før en flate erklæres ferdig; aliaser må løses server-side eller ikke brukes.

**10 — lesson.text-ux-is-not-design**

Symptom: Kjetil forventet en helt annen flate enn den som ble vist; den tekstlige UX-beskrivelsen var godkjent, bildet var det ikke.

Forebygging: Rendret bilde (Porthole-preview eller mockup) godkjennes før implementering; bildet er akseptansereferanse.

**11 — lesson.scaffold-without-porthole-host-has-no-preview**

Symptom: G1-GUI måtte bruke mockups rendret fra skeleton-JSON; ekte Porthole-preview var umulig.

Forebygging: For scaffolds uten Porthole-vert: (1) images/README.md må si eksplisitt at bildene er mockups og hva skeleton ikke kan rendre, (2) paritet (test.gui.parity) planlegges som egen slice med kjørende scaffold + Binding/Porthole via bridge, ikke som del av implementeringsjobben.

**12 — lesson.pin-must-be-on-their-main**

Symptom: En revisjonspin i Package.swift pekte på en CellProtocol-revisjon som ikke lå på CellProtocol sin main. Koden bygde bare på den ene maskinen som hadde revisjonen liggende lokalt.

Forebygging: Å pinne er riktig — det er det som gjør bygget reproduserbart. Kravet er at revisjonen er en forfar av avhengighetens egen main. Da er «bygg fra andres main» og «reproduserbart bygg» samme krav. HavenAgentD::Scripts/assert_dependencies_are_on_their_main.sh håndhever det, og CI kjører den. Lander du en klient før cellen den bruker er på den andres main, har du laget et repo som bare bygger hos deg.

**13 — lesson.tested-a-different-path-than-production**

Symptom: Rot-probene leste relations.state.* gjennom porthole.get og var gronne, mens rendereren aldri fikk de samme dataene.

Forebygging: Naar en test skal si noe om hva brukeren ser, maa den bruke produksjonens egen kodevei - helst produksjonens egen funksjon med produksjonens egne inndata (SkeletonReachabilityAudit kaller condition.evaluate(root: nil, ...) nettopp derfor).

Kjente testrefs (eksistens i snapshot er ikke bevis for at testen er kjørt): `test.build`, `test.cell.auth-negative`, `test.cell.contract-fixtures`, `test.cell.stub-scan`, `test.cells.capability-audit`, `test.cells.dataflow-matches-contracts`, `test.dnd.attach`, `test.docs-updated`, `test.gui.load-time`, `test.gui.parity`, `test.gui.reference-image-exists`, `test.handoff.dry-run`, `test.migration`, `test.regression`, `test.scope.switch`, `test.skeleton.no-unreachable-elements`, `test.skeleton.purpose-actions-reachable`, `test.status-current`, `test.tree-model`, `test.widget.live`

</details>

## PDD_correspondence-vedlegg_2026-09-04

**Simulert perspektiv:** Melding kan bære ikke-tekstlig innhold; Vedlegg refereres, ikke inlines; Manifestet ligger i det indre konvoluttet. **Skop:** simulated-scope://correspondence.
Oppgave: `CellProtocolDocuments/Deliverables/PDD_correspondence-vedlegg_2026-09-04/FORMAALSSPEC.md` (§0/§1).

| Rang | Kandidat 6 | Kandidat 1 — TF-IDF |
|---:|---|---|
| 1 | **1** `lesson.ciphertext-field-held-plaintext-hash` — En paastand om at noe er kryptert, signert eller verifisert skal bekreftes paa artefaktet - les bytene, ikke feltet. Et felt som heter ciphe… | **2** `lesson.cellbase-decodingerror-shadows-swift` — I App-modulen: skriv Swift.DecodingError når du vil ha standardbibliotekets. Gjelder generelt for typenavn CellBase også definerer — sjekk m… |
| 2 | **2** `lesson.cellbase-decodingerror-shadows-swift` — I App-modulen: skriv Swift.DecodingError når du vil ha standardbibliotekets. Gjelder generelt for typenavn CellBase også definerer — sjekk m… | **1** `lesson.ciphertext-field-held-plaintext-hash` — En paastand om at noe er kryptert, signert eller verifisert skal bekreftes paa artefaktet - les bytene, ikke feltet. Et felt som heter ciphe… |
| 3 | **3** `lesson.valuetype-equality-false-for-objects` — Aldri assert på hele sammensatte ValueType-verdier. Sammenlign kanonisk JSON (JSONEncoder med .sortedKeys) eller pakk ut og sammenlign felt … | **3** `lesson.valuetype-equality-false-for-objects` — Aldri assert på hele sammensatte ValueType-verdier. Sammenlign kanonisk JSON (JSONEncoder med .sortedKeys) eller pakk ut og sammenlign felt … |
| 4 | **4** `lesson.decomposition-is-classification` — Dekomponering velger fra Book 23 + pakker først; nye noder merkes 'candidate' og navngis av Claude, aldri implisitt av en modell. | **7** `lesson.cellbase-internal-members-look-public` — Sjekk tilgangsnivå og faktisk returverdi før du bruker et CellBase-medlem fra App: grep -n "var <navn>" CellProtocol::Sources/CellBase/.... … |
| 5 | **5** `lesson.entityanchor-keypaths-are-registered` — Skriv aldri testdata til en oppdiktet keypath på en celle. Finn en keypath cellen faktisk registrerer, helst en annen test som allerede bruk… | **8** `lesson.corr-approval-surfaces-timed-out` — FORMAALSSPEC.md §2 lister avhengigheter som egne formål med verifier; pkg.std.everything-works og gui.surface-loads-in-time må være grønne f… |
| 6 | **6** `lesson.queue-job-file-before-prompt` — Skriv <id>.prompt.md først og <id>.job sist, helst som mv fra en tmp-fil i samme mappe — .job er registreringssignalet, slik job.json er det… | **4** `lesson.decomposition-is-classification` — Dekomponering velger fra Book 23 + pakker først; nye noder merkes 'candidate' og navngis av Claude, aldri implisitt av en modell. |
| 7 | **7** `lesson.cellbase-internal-members-look-public` — Sjekk tilgangsnivå og faktisk returverdi før du bruker et CellBase-medlem fra App: grep -n "var <navn>" CellProtocol::Sources/CellBase/.... … | **9** `lesson.codex-workspace-write-cannot-build-cellscaffold` — Lange bygg og testkjøringer legges ikke som workspace-write-køjobb. De kjøres som detached skript startet via Codex med danger-full-access o… |
| 8 | **8** `lesson.corr-approval-surfaces-timed-out` — FORMAALSSPEC.md §2 lister avhengigheter som egne formål med verifier; pkg.std.everything-works og gui.surface-loads-in-time må være grønne f… | **5** `lesson.entityanchor-keypaths-are-registered` — Skriv aldri testdata til en oppdiktet keypath på en celle. Finn en keypath cellen faktisk registrerer, helst en annen test som allerede bruk… |
| 9 | **9** `lesson.codex-workspace-write-cannot-build-cellscaffold` — Lange bygg og testkjøringer legges ikke som workspace-write-køjobb. De kjøres som detached skript startet via Codex med danger-full-access o… | **11** `lesson.zsh-no-inline-comments` — Aldri forklaring på samme linje som en kommando; skript har '"#") break ;;' i argumentparseren. |
| 10 | **10** `lesson.branch-is-empty-after-eight-work-packages` — Skill «filene finnes» fra «branchen har dem». Sjekk git rev-parse <branch> mot git rev-parse <base> som del av hver verifikasjon som påstår … | **12** `lesson.mount-is-not-git` — Aldri git mot $HOME/mnt fra device_bash; les .git/refs som filer; all git kjøres av Kjetil eller codex exec. |

Union: 12 lærdommer; øvrige 32 uvurderte.
- Relevans: 
- Gjentakelser: 
- Håndhevelse / sann grunn: 
- Sekunder: 

<details><summary>Full tekst og testreferanser</summary>

**1 — lesson.ciphertext-field-held-plaintext-hash**

Symptom: Losen fortalte Kjetil at lyd allerede var kryptert i lagring. Det var feil: filene i prod begynner med ID3 og er vanlig MP3. To ting forte dit. (1) Krypteringskoden som ble lest tilhorer MusicIngestCell paa /mvp/ingest/local, mens Butterpop publiserer gjennom MusicAssetStoreCell.storeLocalAsset, som skriver bytene slik de kommer. (2) storeLocalAsset setter ciphertextSHA256 = plaintextSHA256 = sha256(data), saa manifestet ser kryptert ut selv naar encryptionPolicy er none.

Forebygging: En paastand om at noe er kryptert, signert eller verifisert skal bekreftes paa artefaktet - les bytene, ikke feltet. Et felt som heter ciphertext* skal ikke settes naar encryptionPolicy er none; enten utelates det, eller navnet sier hva det er. Kan bli derivedTest: manifest med encryptionPolicy none har ingen ciphertext-verdi.

**2 — lesson.cellbase-decodingerror-shadows-swift**

Symptom: WP1s nye celle ga 50 kompileringsfeil: `type 'DecodingError' has no member 'dataCorruptedError'` og `cannot infer contextual base in reference to member 'registry'`, alle fra én linje.

Forebygging: I App-modulen: skriv `Swift.DecodingError` når du vil ha standardbibliotekets. Gjelder generelt for typenavn CellBase også definerer — sjekk med `grep -rn "enum <Navn>" CellProtocol::Sources/CellBase` før du antar at et kjent Foundation-navn er Foundations.

**3 — lesson.valuetype-equality-false-for-objects**

Symptom: Fire av sju WP1-tester feilet på `XCTAssertEqual` mellom to `ValueType.object` som hadde identisk innhold. Feilmeldingen viste samme nøkler og verdier på begge sider, i ulik rekkefølge.

Forebygging: Aldri assert på hele sammensatte `ValueType`-verdier. Sammenlign kanonisk JSON (`JSONEncoder` med `.sortedKeys`) eller pakk ut og sammenlign felt for felt. Skalarer (`.string`, `.integer`, `.bool`, `.null`) sammenlignes trygt. Merk: dette er et funn i CellBase, ikke bare en testregel — App-kildene destrukturerer riktignok før sammenligning, men en fremtidig `==` på hele verdier vil stille behandle like verdier som ulike. Ikke revidert utover App-kildene.

**4 — lesson.decomposition-is-classification**

Symptom: Modeller som genererte purpose://-refs fritt hallusinerte referanser.

Forebygging: Dekomponering velger fra Book 23 + pakker først; nye noder merkes 'candidate' og navngis av Claude, aldri implisitt av en modell.

**5 — lesson.entityanchor-keypaths-are-registered**

Symptom: WP2-testen skrev en sentinel til `profile` på abonnentens EntityAnchor og fikk `notFound` ved gjenlesing. Skrivingen ga ingen feil.

Forebygging: Skriv aldri testdata til en oppdiktet keypath på en celle. Finn en keypath cellen faktisk registrerer, helst en annen test som allerede bruker den. At et `set` går gjennom er ikke bevis på at keypathen finnes.

**6 — lesson.queue-job-file-before-prompt**

Symptom: Køjobben `formaalskomposisjon-fullfor-commit-20260910-1020` ble avvist med «mangler promptfil» 13 sekunder etter at `.job` ble skrevet; promptfilen kom to sekunder etter avvisningen og ligger foreldreløs i `_losen-queue/inbox/`, der runneren aldri ser den igjen.

Forebygging: Skriv `<id>.prompt.md` først og `<id>.job` sist, helst som `mv` fra en tmp-fil i samme mappe — `.job` er registreringssignalet, slik `job.json` er det i HavenAgentD::Docs/AgentJobs.md. Kan bli derivedTest: runneren eller `hd validate` rapporterer enhver `inbox/*.prompt.md` uten tilhørende `.job`, eldre enn to minutter, som foreldreløs.

**7 — lesson.cellbase-internal-members-look-public**

Symptom: WP2 stoppet på `'fullPermissionString' is inaccessible due to 'internal' protection level`. Medlemmet finnes og brukes i CellBase selv, så det så ut som et gyldig API.

Forebygging: Sjekk tilgangsnivå og faktisk returverdi før du bruker et CellBase-medlem fra App: `grep -n "var <navn>" CellProtocol::Sources/CellBase/...`. Et medlem som brukes internt i CellBase er ikke automatisk en del av API-et, og navnelikhet betyr ikke verdilikhet.

**8 — lesson.corr-approval-surfaces-timed-out**

Symptom: Corr-godkjenningen (Vegar) er utestet fordi flater/godkjenninger timet ut før testing rakk å skje.

Forebygging: FORMAALSSPEC.md §2 lister avhengigheter som egne formål med verifier; pkg.std.everything-works og gui.surface-loads-in-time må være grønne før den egentlige testen kjøres.

**9 — lesson.codex-workspace-write-cannot-build-cellscaffold**

Symptom: WP0-baselinen i køen ble blocked: `sandbox-exec: sandbox_apply: Operation not permitted`. Testkommandoen brukte 1 604 sekunder uten at én eneste test startet.

Forebygging: Lange bygg og testkjøringer legges ikke som `workspace-write`-køjobb. De kjøres som detached skript startet via Codex med `danger-full-access` og python Popen(start_new_session=True), med logg i en montert mappe som Cowork kan polle — samme mønster som produserte den notariserte HavenAgentD-pakken 2026-09-08. Køjobber brukes til analyse, kontrakter, dokumentasjon og korte kommandoer.

**10 — lesson.branch-is-empty-after-eight-work-packages**

Symptom: Åtte arbeidspakker rapportert utført og verifisert, ACCEPT.md skrevet — men `git branch -v` viste at `pdd/scaffold-admin-delegering` fortsatt pekte på samme commit som `main` (`e1f3e22f`). All koden lå ucommittet i et worktree som bare finnes på én maskin. Ett tapt worktree = 2 750 linjer kode og test borte, med full dokumentasjon på at arbeidet var «levert».

Forebygging: Skill «filene finnes» fra «branchen har dem». Sjekk `git rev-parse <branch>` mot `git rev-parse <base>` som del av hver verifikasjon som påstår at noe ligger på en branch; er de like, er branchen tom. Legg en commit-pakke inn i planen etter første grønne bygg, ikke etter siste arbeidspakke. Når worktreet bare kan leses fra macOS, kjør sjekken der — ikke hopp over den fordi verktøyet svarer feil.

**11 — lesson.zsh-no-inline-comments**

Symptom: Begge kommandolinjene feilet med 'ukjent argument: #' og ingenting kjørte.

Forebygging: Aldri forklaring på samme linje som en kommando; skript har '"#"*) break ;;' i argumentparseren.

**12 — lesson.mount-is-not-git**

Symptom: Hver git-kommando fra device_bash etterlot en index.lock som ikke kunne fjernes og blokkerte Kjetils commits; seks repoer låst 24.08.

Forebygging: Aldri git mot $HOME/mnt fra device_bash; les .git/refs som filer; all git kjøres av Kjetil eller codex exec.

Kjente testrefs (eksistens i snapshot er ikke bevis for at testen er kjørt): `test.att.claim-scan`, `test.att.close-kills-fetch`, `test.att.constant-memory`, `test.att.dump-opaque`, `test.att.e2e`, `test.att.expiry-together`, `test.att.fetch-only-addressed`, `test.att.gated-on-s5`, `test.att.grants-exactly-two`, `test.att.manifest-only`, `test.att.no-fs-right`, `test.att.no-host-in-outer`, `test.att.no-new-cell`, `test.att.one-message-only`, `test.att.resume`, `test.att.suite-no-size-cap`, `test.att.suite-roundtrip`, `test.att.suite-tamper`, `test.att.transport-keyless`, `test.att.ttfb`, `test.build`, `test.cell.auth-negative`, `test.cell.contract-fixtures`, `test.cell.stub-scan`, `test.cells.capability-audit`, `test.cells.dataflow-matches-contracts`, `test.docs-updated`, `test.gui.load-time`, `test.gui.parity`, `test.gui.reference-image-exists`, `test.handoff.dry-run`, `test.regression`, `test.skeleton.no-unreachable-elements`, `test.skeleton.purpose-actions-reachable`, `test.status-current`

</details>

## PDD_entitetsdata-egen-kontroll_2026-09-08

**Simulert perspektiv:** Data self-determination; Første kjøring forsegler entiteten til den som startet den; Lesing krever bevis, ikke bare mutasjon. **Skop:** simulated-scope://egne-data.
Oppgave: `CellProtocolDocuments/Deliverables/PDD_entitetsdata-egen-kontroll_2026-09-08/FORMAALSSPEC.md` (§0/§1).

| Rang | Kandidat 6 | Kandidat 1 — TF-IDF |
|---:|---|---|
| 1 | **1** `lesson.entityanchor-keypaths-are-registered` — Skriv aldri testdata til en oppdiktet keypath på en celle. Finn en keypath cellen faktisk registrerer, helst en annen test som allerede bruk… | **1** `lesson.entityanchor-keypaths-are-registered` — Skriv aldri testdata til en oppdiktet keypath på en celle. Finn en keypath cellen faktisk registrerer, helst en annen test som allerede bruk… |
| 2 | **2** `lesson.unresolvable-condition-is-invisible` — SkeletonReachabilityAudit kjores over hver flate; feiler med elementene som aldri kan sees og handlingene som gaar tapt med dem. Betingelser… | **5** `lesson.cellbase-decodingerror-shadows-swift` — I App-modulen: skriv Swift.DecodingError når du vil ha standardbibliotekets. Gjelder generelt for typenavn CellBase også definerer — sjekk m… |
| 3 | **3** `lesson.cellbase-internal-members-look-public` — Sjekk tilgangsnivå og faktisk returverdi før du bruker et CellBase-medlem fra App: grep -n "var <navn>" CellProtocol::Sources/CellBase/.... … | **6** `lesson.new-cell-must-declare-its-provisioning-mode` — Enhver ny persistert celle i CellScaffold må eksplisitt svare på tre spørsmål før den registreres: (1) skal den opprettes i require-existing… |
| 4 | **4** `lesson.a-new-red-test-needs-a-repeated-baseline` — Når en ny rød dukker opp: kjør basen på nytt, i et eget rent worktree, flere ganger (tre holder som regel), før du enten tar på deg feilen e… | **3** `lesson.cellbase-internal-members-look-public` — Sjekk tilgangsnivå og faktisk returverdi før du bruker et CellBase-medlem fra App: grep -n "var <navn>" CellProtocol::Sources/CellBase/.... … |
| 5 | **5** `lesson.cellbase-decodingerror-shadows-swift` — I App-modulen: skriv Swift.DecodingError når du vil ha standardbibliotekets. Gjelder generelt for typenavn CellBase også definerer — sjekk m… | **2** `lesson.unresolvable-condition-is-invisible` — SkeletonReachabilityAudit kjores over hver flate; feiler med elementene som aldri kan sees og handlingene som gaar tapt med dem. Betingelser… |
| 6 | **6** `lesson.new-cell-must-declare-its-provisioning-mode` — Enhver ny persistert celle i CellScaffold må eksplisitt svare på tre spørsmål før den registreres: (1) skal den opprettes i require-existing… | **9** `lesson.test-the-representation-not-the-issuance-flow` — Skille to spørsmål: «hvordan får noen rollen» og «hva gir rollen». Tester du det andre, installer rollen på husets etablerte måte og test vi… |
| 7 | **7** `lesson.parity-was-correctness-not-decoration` — Akseptanse sammenligner både bilde og oppførsel (knapper trigger keypaths, felt tar input) — begge i ACCEPT.md. | **11** `lesson.cellscaffold-two-holes` — Ikke porter celler fra CellScaffold til PalazzoScaffold uten å lukke begge hullene; og må være grønne. |
| 8 | **8** `lesson.scaffold-without-porthole-host-has-no-preview` — For scaffolds uten Porthole-vert: (1) images/README.md må si eksplisitt at bildene er mockups og hva skeleton ikke kan rendre, (2) paritet (… | **12** `lesson.valuetype-equality-false-for-objects` — Aldri assert på hele sammensatte ValueType-verdier. Sammenlign kanonisk JSON (JSONEncoder med .sortedKeys) eller pakk ut og sammenlign felt … |
| 9 | **9** `lesson.test-the-representation-not-the-issuance-flow` — Skille to spørsmål: «hvordan får noen rollen» og «hva gir rollen». Tester du det andre, installer rollen på husets etablerte måte og test vi… | **4** `lesson.a-new-red-test-needs-a-repeated-baseline` — Når en ny rød dukker opp: kjør basen på nytt, i et eget rent worktree, flere ganger (tre holder som regel), før du enten tar på deg feilen e… |
| 10 | **10** `lesson.test-corpus-is-not-shipped-corpus` — Enhver flate-test skal bygge korpuset fra det som faktisk sendes ut (menykonfigurasjoner + navigasjonsdestinasjoner + verifiseringshjelperen… | **13** `lesson.pin-must-be-on-their-main` — Å pinne er riktig — det er det som gjør bygget reproduserbart. Kravet er at revisjonen er en forfar av avhengighetens egen main. Da er «bygg… |

Union: 13 lærdommer; øvrige 31 uvurderte.
- Relevans: 
- Gjentakelser: 
- Håndhevelse / sann grunn: 
- Sekunder: 

<details><summary>Full tekst og testreferanser</summary>

**1 — lesson.entityanchor-keypaths-are-registered**

Symptom: WP2-testen skrev en sentinel til `profile` på abonnentens EntityAnchor og fikk `notFound` ved gjenlesing. Skrivingen ga ingen feil.

Forebygging: Skriv aldri testdata til en oppdiktet keypath på en celle. Finn en keypath cellen faktisk registrerer, helst en annen test som allerede bruker den. At et `set` går gjennom er ikke bevis på at keypathen finnes.

**2 — lesson.unresolvable-condition-is-invisible**

Symptom: Relasjoner-flaten viste tittel og ingen vei inn: ingen filopplasting, ingen knapper. Alle tester gronne.

Forebygging: SkeletonReachabilityAudit kjores over hver flate; test.skeleton.no-unreachable-elements feiler med elementene som aldri kan sees og handlingene som gaar tapt med dem. Betingelser hoerer hjemme inne i List/Grid/Reference-rader, der radens verdi sendes videre; ellers skal cellen avgjore og innhold bindes.

**3 — lesson.cellbase-internal-members-look-public**

Symptom: WP2 stoppet på `'fullPermissionString' is inaccessible due to 'internal' protection level`. Medlemmet finnes og brukes i CellBase selv, så det så ut som et gyldig API.

Forebygging: Sjekk tilgangsnivå og faktisk returverdi før du bruker et CellBase-medlem fra App: `grep -n "var <navn>" CellProtocol::Sources/CellBase/...`. Et medlem som brukes internt i CellBase er ikke automatisk en del av API-et, og navnelikhet betyr ikke verdilikhet.

**4 — lesson.a-new-red-test-needs-a-repeated-baseline**

Symptom: Første fulle kjøring med nye endringer viste to røde i stedet for baselinens én, og den nye lå i en fil jeg hadde endret. Det så ut som en regresjon jeg hadde innført.

Forebygging: Når en ny rød dukker opp: kjør basen på nytt, i et eget rent worktree, **flere ganger** (tre holder som regel), før du enten tar på deg feilen eller avfeier den. Skriv resultatet av gjentakelsen i TESTRESULT — «2 av 3 på ren base» er et svar, «den er nok flaky» er ikke. Det koster ti minutter og avgjør om du bruker natten på å jage din egen feil eller andres.

**5 — lesson.cellbase-decodingerror-shadows-swift**

Symptom: WP1s nye celle ga 50 kompileringsfeil: `type 'DecodingError' has no member 'dataCorruptedError'` og `cannot infer contextual base in reference to member 'registry'`, alle fra én linje.

Forebygging: I App-modulen: skriv `Swift.DecodingError` når du vil ha standardbibliotekets. Gjelder generelt for typenavn CellBase også definerer — sjekk med `grep -rn "enum <Navn>" CellProtocol::Sources/CellBase` før du antar at et kjent Foundation-navn er Foundations.

**6 — lesson.new-cell-must-declare-its-provisioning-mode**

Symptom: To nye celler i CellScaffold ga tre nye regresjoner: `OrchestratorPersistenceTests testRequireExistingModeRejectsFreshStorageWithoutCreatingBootstrapCells` (opprettet en celle i require-existing-modus mot fersk lagring) og to `TopUpCheckoutTests` som teller celler i provision-only-modus (5 mot forventet 4).

Forebygging: Enhver ny persistert celle i CellScaffold må eksplisitt svare på tre spørsmål før den registreres: (1) skal den opprettes i require-existing mot fersk lagring? Nei, med mindre den er kanonisk bootstrap. (2) Er den en av de kanoniske eager-bootstrap-cellene som provision-only skal lage? Nesten alltid nei — TopUpCheckoutTests teller dem eksplisitt. (3) Er den en Porthole-publisert flate? Bare da hører den i `reconcilePortholePublishedCellResolves`. Scaffold-intern tilstand registreres i egen funksjon, gated på policy OG provisionOnly, med gjenkjenning av eksisterende mapping.

**7 — lesson.parity-was-correctness-not-decoration**

Symptom: Parity-audit mellom Porthole og Binding viste at problemet ikke var manglende dekorasjon, men produktkorrekthet (feil oppførsel).

Forebygging: Akseptanse sammenligner både bilde og oppførsel (knapper trigger keypaths, felt tar input) — begge i ACCEPT.md.

**8 — lesson.scaffold-without-porthole-host-has-no-preview**

Symptom: G1-GUI måtte bruke mockups rendret fra skeleton-JSON; ekte Porthole-preview var umulig.

Forebygging: For scaffolds uten Porthole-vert: (1) images/README.md må si eksplisitt at bildene er mockups og hva skeleton ikke kan rendre, (2) paritet (test.gui.parity) planlegges som egen slice med kjørende scaffold + Binding/Porthole via bridge, ikke som del av implementeringsjobben.

**9 — lesson.test-the-representation-not-the-issuance-flow**

Symptom: Alle fire WP4-rolletestene feilet i oppsettet, ikke i det de skulle teste: `deniedNoGrant` på `requestEntry` mot `cell:///AdminEntry`. Testen fikk aldri gitt identiteten rollen.

Forebygging: Skille to spørsmål: «hvordan får noen rollen» og «hva gir rollen». Tester du det andre, installer rollen på husets etablerte måte og test virkningen. Let alltid etter en eksisterende `*TestSupport`-hjelper før du bygger oppsettet selv — `grep -rn "TestSupport" CellScaffold::Tests` — og se hvilke argumenter de andre testene gir den.

**10 — lesson.test-corpus-is-not-shipped-corpus**

Symptom: Rot-probe-testen, lastetidstesten og finnbarhetsauditen var gronne i to uker mens Relasjoner-flaten var tom.

Forebygging: Enhver flate-test skal bygge korpuset fra det som faktisk sendes ut (menykonfigurasjoner + navigasjonsdestinasjoner + verifiseringshjelperen), dedupliseres, og feile hvis korpuset er mindre enn appens egen meny.

**11 — lesson.cellscaffold-two-holes**

Symptom: CellScaffold har tomme booking-/concierge-stubber og autorisasjon som kaster nøkkelstien og bare sjekker eierskap.

Forebygging: Ikke porter celler fra CellScaffold til PalazzoScaffold uten å lukke begge hullene; test.cell.auth-negative og test.cell.stub-scan må være grønne.

**12 — lesson.valuetype-equality-false-for-objects**

Symptom: Fire av sju WP1-tester feilet på `XCTAssertEqual` mellom to `ValueType.object` som hadde identisk innhold. Feilmeldingen viste samme nøkler og verdier på begge sider, i ulik rekkefølge.

Forebygging: Aldri assert på hele sammensatte `ValueType`-verdier. Sammenlign kanonisk JSON (`JSONEncoder` med `.sortedKeys`) eller pakk ut og sammenlign felt for felt. Skalarer (`.string`, `.integer`, `.bool`, `.null`) sammenlignes trygt. Merk: dette er et funn i CellBase, ikke bare en testregel — App-kildene destrukturerer riktignok før sammenligning, men en fremtidig `==` på hele verdier vil stille behandle like verdier som ulike. Ikke revidert utover App-kildene.

**13 — lesson.pin-must-be-on-their-main**

Symptom: En revisjonspin i Package.swift pekte på en CellProtocol-revisjon som ikke lå på CellProtocol sin main. Koden bygde bare på den ene maskinen som hadde revisjonen liggende lokalt.

Forebygging: Å pinne er riktig — det er det som gjør bygget reproduserbart. Kravet er at revisjonen er en forfar av avhengighetens egen main. Da er «bygg fra andres main» og «reproduserbart bygg» samme krav. HavenAgentD::Scripts/assert_dependencies_are_on_their_main.sh håndhever det, og CI kjører den. Lander du en klient før cellen den bruker er på den andres main, har du laget et repo som bare bygger hos deg.

Kjente testrefs (eksistens i snapshot er ikke bevis for at testen er kjørt): `test.build`, `test.cell.auth-negative`, `test.cell.contract-fixtures`, `test.cell.stub-scan`, `test.cells.capability-audit`, `test.cells.dataflow-matches-contracts`, `test.docs-updated`, `test.entitet.auth-negative`, `test.entitet.direct-edit`, `test.entitet.file-roundtrip`, `test.entitet.gateway-owned`, `test.entitet.trace`, `test.entitet.unsigned-proposal-refused`, `test.entitet.untrusted-model-refused`, `test.gui.load-time`, `test.gui.parity`, `test.gui.reference-image-exists`, `test.handoff.dry-run`, `test.regression`, `test.skeleton.no-unreachable-elements`, `test.skeleton.purpose-actions-reachable`, `test.status-current`

</details>

## PDD_entitetsnokler_2026-09-04

**Simulert perspektiv:** En nøkkel hører til entiteten som bruker den; Hemmeligheten ligger i cellens egen persisterte tilstand; Kryptert på hvile. **Skop:** simulated-scope://egne-data.
Oppgave: `CellProtocolDocuments/Deliverables/PDD_entitetsnokler_2026-09-04/FORMAALSSPEC.md` (§0/§1).

| Rang | Kandidat 6 | Kandidat 1 — TF-IDF |
|---:|---|---|
| 1 | **1** `lesson.new-cell-must-declare-its-provisioning-mode` — Enhver ny persistert celle i CellScaffold må eksplisitt svare på tre spørsmål før den registreres: (1) skal den opprettes i require-existing… | **1** `lesson.new-cell-must-declare-its-provisioning-mode` — Enhver ny persistert celle i CellScaffold må eksplisitt svare på tre spørsmål før den registreres: (1) skal den opprettes i require-existing… |
| 2 | **2** `lesson.entityanchor-keypaths-are-registered` — Skriv aldri testdata til en oppdiktet keypath på en celle. Finn en keypath cellen faktisk registrerer, helst en annen test som allerede bruk… | **7** `lesson.valuetype-equality-false-for-objects` — Aldri assert på hele sammensatte ValueType-verdier. Sammenlign kanonisk JSON (JSONEncoder med .sortedKeys) eller pakk ut og sammenlign felt … |
| 3 | **3** `lesson.cellbase-decodingerror-shadows-swift` — I App-modulen: skriv Swift.DecodingError når du vil ha standardbibliotekets. Gjelder generelt for typenavn CellBase også definerer — sjekk m… | **5** `lesson.cellscaffold-two-holes` — Ikke porter celler fra CellScaffold til PalazzoScaffold uten å lukke begge hullene; og må være grønne. |
| 4 | **4** `lesson.test-the-representation-not-the-issuance-flow` — Skille to spørsmål: «hvordan får noen rollen» og «hva gir rollen». Tester du det andre, installer rollen på husets etablerte måte og test vi… | **2** `lesson.entityanchor-keypaths-are-registered` — Skriv aldri testdata til en oppdiktet keypath på en celle. Finn en keypath cellen faktisk registrerer, helst en annen test som allerede bruk… |
| 5 | **5** `lesson.cellscaffold-two-holes` — Ikke porter celler fra CellScaffold til PalazzoScaffold uten å lukke begge hullene; og må være grønne. | **3** `lesson.cellbase-decodingerror-shadows-swift` — I App-modulen: skriv Swift.DecodingError når du vil ha standardbibliotekets. Gjelder generelt for typenavn CellBase også definerer — sjekk m… |
| 6 | **6** `lesson.scaffold-without-porthole-host-has-no-preview` — For scaffolds uten Porthole-vert: (1) images/README.md må si eksplisitt at bildene er mockups og hva skeleton ikke kan rendre, (2) paritet (… | **4** `lesson.test-the-representation-not-the-issuance-flow` — Skille to spørsmål: «hvordan får noen rollen» og «hva gir rollen». Tester du det andre, installer rollen på husets etablerte måte og test vi… |
| 7 | **7** `lesson.valuetype-equality-false-for-objects` — Aldri assert på hele sammensatte ValueType-verdier. Sammenlign kanonisk JSON (JSONEncoder med .sortedKeys) eller pakk ut og sammenlign felt … | **9** `lesson.branch-is-empty-after-eight-work-packages` — Skill «filene finnes» fra «branchen har dem». Sjekk git rev-parse <branch> mot git rev-parse <base> som del av hver verifikasjon som påstår … |
| 8 | **8** `lesson.ciphertext-field-held-plaintext-hash` — En paastand om at noe er kryptert, signert eller verifisert skal bekreftes paa artefaktet - les bytene, ikke feltet. Et felt som heter ciphe… | **11** `lesson.planned-documented-as-implemented` — Docs-diff i samme endring, med 'Last verified against code'-dato; planlagt oppførsel merkes eksplisitt. |
| 9 | **9** `lesson.branch-is-empty-after-eight-work-packages` — Skill «filene finnes» fra «branchen har dem». Sjekk git rev-parse <branch> mot git rev-parse <base> som del av hver verifikasjon som påstår … | **10** `lesson.cellbase-internal-members-look-public` — Sjekk tilgangsnivå og faktisk returverdi før du bruker et CellBase-medlem fra App: grep -n "var <navn>" CellProtocol::Sources/CellBase/.... … |
| 10 | **10** `lesson.cellbase-internal-members-look-public` — Sjekk tilgangsnivå og faktisk returverdi før du bruker et CellBase-medlem fra App: grep -n "var <navn>" CellProtocol::Sources/CellBase/.... … | **12** `lesson.baseline-count-from-report-not-run` — WP0/S0 baseline er alltid en ekte kjøring før endring; PLAN oppgir testtall som «forventet ≈ N (fra <kilde, dato>)», og et rødt baseline sto… |

Union: 12 lærdommer; øvrige 32 uvurderte.
- Relevans: 
- Gjentakelser: 
- Håndhevelse / sann grunn: 
- Sekunder: 

<details><summary>Full tekst og testreferanser</summary>

**1 — lesson.new-cell-must-declare-its-provisioning-mode**

Symptom: To nye celler i CellScaffold ga tre nye regresjoner: `OrchestratorPersistenceTests testRequireExistingModeRejectsFreshStorageWithoutCreatingBootstrapCells` (opprettet en celle i require-existing-modus mot fersk lagring) og to `TopUpCheckoutTests` som teller celler i provision-only-modus (5 mot forventet 4).

Forebygging: Enhver ny persistert celle i CellScaffold må eksplisitt svare på tre spørsmål før den registreres: (1) skal den opprettes i require-existing mot fersk lagring? Nei, med mindre den er kanonisk bootstrap. (2) Er den en av de kanoniske eager-bootstrap-cellene som provision-only skal lage? Nesten alltid nei — TopUpCheckoutTests teller dem eksplisitt. (3) Er den en Porthole-publisert flate? Bare da hører den i `reconcilePortholePublishedCellResolves`. Scaffold-intern tilstand registreres i egen funksjon, gated på policy OG provisionOnly, med gjenkjenning av eksisterende mapping.

**2 — lesson.entityanchor-keypaths-are-registered**

Symptom: WP2-testen skrev en sentinel til `profile` på abonnentens EntityAnchor og fikk `notFound` ved gjenlesing. Skrivingen ga ingen feil.

Forebygging: Skriv aldri testdata til en oppdiktet keypath på en celle. Finn en keypath cellen faktisk registrerer, helst en annen test som allerede bruker den. At et `set` går gjennom er ikke bevis på at keypathen finnes.

**3 — lesson.cellbase-decodingerror-shadows-swift**

Symptom: WP1s nye celle ga 50 kompileringsfeil: `type 'DecodingError' has no member 'dataCorruptedError'` og `cannot infer contextual base in reference to member 'registry'`, alle fra én linje.

Forebygging: I App-modulen: skriv `Swift.DecodingError` når du vil ha standardbibliotekets. Gjelder generelt for typenavn CellBase også definerer — sjekk med `grep -rn "enum <Navn>" CellProtocol::Sources/CellBase` før du antar at et kjent Foundation-navn er Foundations.

**4 — lesson.test-the-representation-not-the-issuance-flow**

Symptom: Alle fire WP4-rolletestene feilet i oppsettet, ikke i det de skulle teste: `deniedNoGrant` på `requestEntry` mot `cell:///AdminEntry`. Testen fikk aldri gitt identiteten rollen.

Forebygging: Skille to spørsmål: «hvordan får noen rollen» og «hva gir rollen». Tester du det andre, installer rollen på husets etablerte måte og test virkningen. Let alltid etter en eksisterende `*TestSupport`-hjelper før du bygger oppsettet selv — `grep -rn "TestSupport" CellScaffold::Tests` — og se hvilke argumenter de andre testene gir den.

**5 — lesson.cellscaffold-two-holes**

Symptom: CellScaffold har tomme booking-/concierge-stubber og autorisasjon som kaster nøkkelstien og bare sjekker eierskap.

Forebygging: Ikke porter celler fra CellScaffold til PalazzoScaffold uten å lukke begge hullene; test.cell.auth-negative og test.cell.stub-scan må være grønne.

**6 — lesson.scaffold-without-porthole-host-has-no-preview**

Symptom: G1-GUI måtte bruke mockups rendret fra skeleton-JSON; ekte Porthole-preview var umulig.

Forebygging: For scaffolds uten Porthole-vert: (1) images/README.md må si eksplisitt at bildene er mockups og hva skeleton ikke kan rendre, (2) paritet (test.gui.parity) planlegges som egen slice med kjørende scaffold + Binding/Porthole via bridge, ikke som del av implementeringsjobben.

**7 — lesson.valuetype-equality-false-for-objects**

Symptom: Fire av sju WP1-tester feilet på `XCTAssertEqual` mellom to `ValueType.object` som hadde identisk innhold. Feilmeldingen viste samme nøkler og verdier på begge sider, i ulik rekkefølge.

Forebygging: Aldri assert på hele sammensatte `ValueType`-verdier. Sammenlign kanonisk JSON (`JSONEncoder` med `.sortedKeys`) eller pakk ut og sammenlign felt for felt. Skalarer (`.string`, `.integer`, `.bool`, `.null`) sammenlignes trygt. Merk: dette er et funn i CellBase, ikke bare en testregel — App-kildene destrukturerer riktignok før sammenligning, men en fremtidig `==` på hele verdier vil stille behandle like verdier som ulike. Ikke revidert utover App-kildene.

**8 — lesson.ciphertext-field-held-plaintext-hash**

Symptom: Losen fortalte Kjetil at lyd allerede var kryptert i lagring. Det var feil: filene i prod begynner med ID3 og er vanlig MP3. To ting forte dit. (1) Krypteringskoden som ble lest tilhorer MusicIngestCell paa /mvp/ingest/local, mens Butterpop publiserer gjennom MusicAssetStoreCell.storeLocalAsset, som skriver bytene slik de kommer. (2) storeLocalAsset setter ciphertextSHA256 = plaintextSHA256 = sha256(data), saa manifestet ser kryptert ut selv naar encryptionPolicy er none.

Forebygging: En paastand om at noe er kryptert, signert eller verifisert skal bekreftes paa artefaktet - les bytene, ikke feltet. Et felt som heter ciphertext* skal ikke settes naar encryptionPolicy er none; enten utelates det, eller navnet sier hva det er. Kan bli derivedTest: manifest med encryptionPolicy none har ingen ciphertext-verdi.

**9 — lesson.branch-is-empty-after-eight-work-packages**

Symptom: Åtte arbeidspakker rapportert utført og verifisert, ACCEPT.md skrevet — men `git branch -v` viste at `pdd/scaffold-admin-delegering` fortsatt pekte på samme commit som `main` (`e1f3e22f`). All koden lå ucommittet i et worktree som bare finnes på én maskin. Ett tapt worktree = 2 750 linjer kode og test borte, med full dokumentasjon på at arbeidet var «levert».

Forebygging: Skill «filene finnes» fra «branchen har dem». Sjekk `git rev-parse <branch>` mot `git rev-parse <base>` som del av hver verifikasjon som påstår at noe ligger på en branch; er de like, er branchen tom. Legg en commit-pakke inn i planen etter første grønne bygg, ikke etter siste arbeidspakke. Når worktreet bare kan leses fra macOS, kjør sjekken der — ikke hopp over den fordi verktøyet svarer feil.

**10 — lesson.cellbase-internal-members-look-public**

Symptom: WP2 stoppet på `'fullPermissionString' is inaccessible due to 'internal' protection level`. Medlemmet finnes og brukes i CellBase selv, så det så ut som et gyldig API.

Forebygging: Sjekk tilgangsnivå og faktisk returverdi før du bruker et CellBase-medlem fra App: `grep -n "var <navn>" CellProtocol::Sources/CellBase/...`. Et medlem som brukes internt i CellBase er ikke automatisk en del av API-et, og navnelikhet betyr ikke verdilikhet.

**11 — lesson.planned-documented-as-implemented**

Symptom: Book/05_Flows_Lifecycle.md beskrev sekvensnummer, signatur og replay som ikke finnes i structen.

Forebygging: Docs-diff i samme endring, med 'Last verified against code'-dato; planlagt oppførsel merkes eksplisitt.

**12 — lesson.baseline-count-from-report-not-run**

Symptom: PLAN.md sa «48 tester grønne»; baseline-kjøringen viste 68 tester med 3 røde.

Forebygging: WP0/S0 baseline er alltid en ekte kjøring før endring; PLAN oppgir testtall som «forventet ≈ N (fra <kilde, dato>)», og et rødt baseline stopper ikke arbeidet men registreres som eget avvik med årsak.

Kjente testrefs (eksistens i snapshot er ikke bevis for at testen er kjørt): `test.build`, `test.cell.auth-negative`, `test.cell.contract-fixtures`, `test.cell.stub-scan`, `test.cells.capability-audit`, `test.cells.dataflow-matches-contracts`, `test.docs-updated`, `test.gui.load-time`, `test.gui.parity`, `test.gui.reference-image-exists`, `test.handoff.dry-run`, `test.regression`, `test.skeleton.no-unreachable-elements`, `test.skeleton.purpose-actions-reachable`, `test.status-current`

</details>

## PDD_formaalsregister-som-graf_2026-09-11

**Simulert perspektiv:** Formålsregisteret er én graf signalmatching kan kjøre på; Én taksonomi, én sannhet; De 39 avvikende nodene er avgjort, ikke slettet. **Skop:** simulated-scope://kunnskap.
Oppgave: `CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/FORMAALSSPEC.md` (§0/§1).

| Rang | Kandidat 6 | Kandidat 1 — TF-IDF |
|---:|---|---|
| 1 | **1** `lesson.decomposition-is-classification` — Dekomponering velger fra Book 23 + pakker først; nye noder merkes 'candidate' og navngis av Claude, aldri implisitt av en modell. | **4** `lesson.cellbase-decodingerror-shadows-swift` — I App-modulen: skriv Swift.DecodingError når du vil ha standardbibliotekets. Gjelder generelt for typenavn CellBase også definerer — sjekk m… |
| 2 | **2** `lesson.local-main-is-not-main` — Før du måler en baseline eller sier at main er rød: git fetch origin main og sammenlign. Er lokal main foran origin/main, er de commitene ik… | **2** `lesson.local-main-is-not-main` — Før du måler en baseline eller sier at main er rød: git fetch origin main og sammenlign. Er lokal main foran origin/main, er de commitene ik… |
| 3 | **3** `lesson.bridge-inferred-architecture-from-one-use` — Erklær hver kapabilitet oppgaven bygger på som eget formål med kilde og Avgrensning (pkg.std.cell-combination). | **10** `lesson.pin-must-be-on-their-main` — Å pinne er riktig — det er det som gjør bygget reproduserbart. Kravet er at revisjonen er en forfar av avhengighetens egen main. Da er «bygg… |
| 4 | **4** `lesson.cellbase-decodingerror-shadows-swift` — I App-modulen: skriv Swift.DecodingError når du vil ha standardbibliotekets. Gjelder generelt for typenavn CellBase også definerer — sjekk m… | **1** `lesson.decomposition-is-classification` — Dekomponering velger fra Book 23 + pakker først; nye noder merkes 'candidate' og navngis av Claude, aldri implisitt av en modell. |
| 5 | **5** `lesson.purpose-never-grants-rights` — Et formål kan innsnevre en rettighet, aldri opprette, utvide eller arve en; exact match; feiler lukket. | **11** `lesson.cellbase-internal-members-look-public` — Sjekk tilgangsnivå og faktisk returverdi før du bruker et CellBase-medlem fra App: grep -n "var <navn>" CellProtocol::Sources/CellBase/.... … |
| 6 | **6** `lesson.free-text-is-not-a-declaration` — Formålsnoder skal ha strukturerte felt (goal, verifier, avgrensning, surfaces) — ikke bare summary; usikre noder rutes til Kjetil med confid… | **12** `lesson.codex-workspace-write-cannot-build-cellscaffold` — Lange bygg og testkjøringer legges ikke som workspace-write-køjobb. De kjøres som detached skript startet via Codex med danger-full-access o… |
| 7 | **7** `lesson.entityanchor-keypaths-are-registered` — Skriv aldri testdata til en oppdiktet keypath på en celle. Finn en keypath cellen faktisk registrerer, helst en annen test som allerede bruk… | **13** `lesson.valuetype-equality-false-for-objects` — Aldri assert på hele sammensatte ValueType-verdier. Sammenlign kanonisk JSON (JSONEncoder med .sortedKeys) eller pakk ut og sammenlign felt … |
| 8 | **8** `lesson.ciphertext-field-held-plaintext-hash` — En paastand om at noe er kryptert, signert eller verifisert skal bekreftes paa artefaktet - les bytene, ikke feltet. Et felt som heter ciphe… | **5** `lesson.purpose-never-grants-rights` — Et formål kan innsnevre en rettighet, aldri opprette, utvide eller arve en; exact match; feiler lukket. |
| 9 | **9** `lesson.planned-documented-as-implemented` — Docs-diff i samme endring, med 'Last verified against code'-dato; planlagt oppførsel merkes eksplisitt. | **14** `lesson.tested-a-different-path-than-production` — Naar en test skal si noe om hva brukeren ser, maa den bruke produksjonens egen kodevei - helst produksjonens egen funksjon med produksjonens… |
| 10 | **10** `lesson.pin-must-be-on-their-main` — Å pinne er riktig — det er det som gjør bygget reproduserbart. Kravet er at revisjonen er en forfar av avhengighetens egen main. Da er «bygg… | **15** `lesson.a-new-red-test-needs-a-repeated-baseline` — Når en ny rød dukker opp: kjør basen på nytt, i et eget rent worktree, flere ganger (tre holder som regel), før du enten tar på deg feilen e… |

Union: 15 lærdommer; øvrige 29 uvurderte.
- Relevans: 
- Gjentakelser: 
- Håndhevelse / sann grunn: 
- Sekunder: 

<details><summary>Full tekst og testreferanser</summary>

**1 — lesson.decomposition-is-classification**

Symptom: Modeller som genererte purpose://-refs fritt hallusinerte referanser.

Forebygging: Dekomponering velger fra Book 23 + pakker først; nye noder merkes 'candidate' og navngis av Claude, aldri implisitt av en modell.

**2 — lesson.local-main-is-not-main**

Symptom: WP0-baselinen var rød og ble meldt som «main bygger ikke». Det var feil. Den commiten baselinen ble målt mot, `ba14895`, lå bare på den LOKALE main-grenen og var aldri pushet; den avhang av CellBase-kode som heller ikke var pushet. origin/main lå fire commits lenger fram, pinnet CellProtocol til en revisjon som ER på CellProtocol sin main, og hadde grønn CI hele tiden. Et helt døgns arbeid ble bygget oppå den lokale commiten.

Forebygging: Før du måler en baseline eller sier at main er rød: `git fetch origin main` og sammenlign. Er lokal main foran origin/main, er de commitene ikke main for andre — bygg aldri videre på dem. Se på CI for origin/main før du konkluderer. `swift package edit` skal aldri være på når noe måles eller meldes verifisert. Og den eneste sjekken som virkelig avgjør: klon fra GitHub til en tom katalog og bygg der. HavenAgentD::Scripts/preflight_before_landing.sh stiller alle fire spørsmålene.

**3 — lesson.bridge-inferred-architecture-from-one-use**

Symptom: En kodeassistent sluttet fra én observert bruksmåte av bridge til en egenskap ved arkitekturen og konkluderte feil.

Forebygging: Erklær hver kapabilitet oppgaven bygger på som eget formål med kilde og Avgrensning (pkg.std.cell-combination).

**4 — lesson.cellbase-decodingerror-shadows-swift**

Symptom: WP1s nye celle ga 50 kompileringsfeil: `type 'DecodingError' has no member 'dataCorruptedError'` og `cannot infer contextual base in reference to member 'registry'`, alle fra én linje.

Forebygging: I App-modulen: skriv `Swift.DecodingError` når du vil ha standardbibliotekets. Gjelder generelt for typenavn CellBase også definerer — sjekk med `grep -rn "enum <Navn>" CellProtocol::Sources/CellBase` før du antar at et kjent Foundation-navn er Foundations.

**5 — lesson.purpose-never-grants-rights**

Symptom: Risiko for at formålsmatch tolkes som tilgang.

Forebygging: Et formål kan innsnevre en rettighet, aldri opprette, utvide eller arve en; exact match; purpose://prompt.unknown feiler lukket.

**6 — lesson.free-text-is-not-a-declaration**

Symptom: Leksikalsk avledning fra fri formålstekst ga F1 0,060; strukturerte erklæringer ga 0,686 og 0,909 med ruting til menneske.

Forebygging: Formålsnoder skal ha strukturerte felt (goal, verifier, avgrensning, surfaces) — ikke bare summary; usikre noder rutes til Kjetil med confidence.

**7 — lesson.entityanchor-keypaths-are-registered**

Symptom: WP2-testen skrev en sentinel til `profile` på abonnentens EntityAnchor og fikk `notFound` ved gjenlesing. Skrivingen ga ingen feil.

Forebygging: Skriv aldri testdata til en oppdiktet keypath på en celle. Finn en keypath cellen faktisk registrerer, helst en annen test som allerede bruker den. At et `set` går gjennom er ikke bevis på at keypathen finnes.

**8 — lesson.ciphertext-field-held-plaintext-hash**

Symptom: Losen fortalte Kjetil at lyd allerede var kryptert i lagring. Det var feil: filene i prod begynner med ID3 og er vanlig MP3. To ting forte dit. (1) Krypteringskoden som ble lest tilhorer MusicIngestCell paa /mvp/ingest/local, mens Butterpop publiserer gjennom MusicAssetStoreCell.storeLocalAsset, som skriver bytene slik de kommer. (2) storeLocalAsset setter ciphertextSHA256 = plaintextSHA256 = sha256(data), saa manifestet ser kryptert ut selv naar encryptionPolicy er none.

Forebygging: En paastand om at noe er kryptert, signert eller verifisert skal bekreftes paa artefaktet - les bytene, ikke feltet. Et felt som heter ciphertext* skal ikke settes naar encryptionPolicy er none; enten utelates det, eller navnet sier hva det er. Kan bli derivedTest: manifest med encryptionPolicy none har ingen ciphertext-verdi.

**9 — lesson.planned-documented-as-implemented**

Symptom: Book/05_Flows_Lifecycle.md beskrev sekvensnummer, signatur og replay som ikke finnes i structen.

Forebygging: Docs-diff i samme endring, med 'Last verified against code'-dato; planlagt oppførsel merkes eksplisitt.

**10 — lesson.pin-must-be-on-their-main**

Symptom: En revisjonspin i Package.swift pekte på en CellProtocol-revisjon som ikke lå på CellProtocol sin main. Koden bygde bare på den ene maskinen som hadde revisjonen liggende lokalt.

Forebygging: Å pinne er riktig — det er det som gjør bygget reproduserbart. Kravet er at revisjonen er en forfar av avhengighetens egen main. Da er «bygg fra andres main» og «reproduserbart bygg» samme krav. HavenAgentD::Scripts/assert_dependencies_are_on_their_main.sh håndhever det, og CI kjører den. Lander du en klient før cellen den bruker er på den andres main, har du laget et repo som bare bygger hos deg.

**11 — lesson.cellbase-internal-members-look-public**

Symptom: WP2 stoppet på `'fullPermissionString' is inaccessible due to 'internal' protection level`. Medlemmet finnes og brukes i CellBase selv, så det så ut som et gyldig API.

Forebygging: Sjekk tilgangsnivå og faktisk returverdi før du bruker et CellBase-medlem fra App: `grep -n "var <navn>" CellProtocol::Sources/CellBase/...`. Et medlem som brukes internt i CellBase er ikke automatisk en del av API-et, og navnelikhet betyr ikke verdilikhet.

**12 — lesson.codex-workspace-write-cannot-build-cellscaffold**

Symptom: WP0-baselinen i køen ble blocked: `sandbox-exec: sandbox_apply: Operation not permitted`. Testkommandoen brukte 1 604 sekunder uten at én eneste test startet.

Forebygging: Lange bygg og testkjøringer legges ikke som `workspace-write`-køjobb. De kjøres som detached skript startet via Codex med `danger-full-access` og python Popen(start_new_session=True), med logg i en montert mappe som Cowork kan polle — samme mønster som produserte den notariserte HavenAgentD-pakken 2026-09-08. Køjobber brukes til analyse, kontrakter, dokumentasjon og korte kommandoer.

**13 — lesson.valuetype-equality-false-for-objects**

Symptom: Fire av sju WP1-tester feilet på `XCTAssertEqual` mellom to `ValueType.object` som hadde identisk innhold. Feilmeldingen viste samme nøkler og verdier på begge sider, i ulik rekkefølge.

Forebygging: Aldri assert på hele sammensatte `ValueType`-verdier. Sammenlign kanonisk JSON (`JSONEncoder` med `.sortedKeys`) eller pakk ut og sammenlign felt for felt. Skalarer (`.string`, `.integer`, `.bool`, `.null`) sammenlignes trygt. Merk: dette er et funn i CellBase, ikke bare en testregel — App-kildene destrukturerer riktignok før sammenligning, men en fremtidig `==` på hele verdier vil stille behandle like verdier som ulike. Ikke revidert utover App-kildene.

**14 — lesson.tested-a-different-path-than-production**

Symptom: Rot-probene leste relations.state.* gjennom porthole.get og var gronne, mens rendereren aldri fikk de samme dataene.

Forebygging: Naar en test skal si noe om hva brukeren ser, maa den bruke produksjonens egen kodevei - helst produksjonens egen funksjon med produksjonens egne inndata (SkeletonReachabilityAudit kaller condition.evaluate(root: nil, ...) nettopp derfor).

**15 — lesson.a-new-red-test-needs-a-repeated-baseline**

Symptom: Første fulle kjøring med nye endringer viste to røde i stedet for baselinens én, og den nye lå i en fil jeg hadde endret. Det så ut som en regresjon jeg hadde innført.

Forebygging: Når en ny rød dukker opp: kjør basen på nytt, i et eget rent worktree, **flere ganger** (tre holder som regel), før du enten tar på deg feilen eller avfeier den. Skriv resultatet av gjentakelsen i TESTRESULT — «2 av 3 på ren base» er et svar, «den er nok flaky» er ikke. Det koster ti minutter og avgjør om du bruker natten på å jage din egen feil eller andres.

Kjente testrefs (eksistens i snapshot er ikke bevis for at testen er kjørt): `test.build`, `test.cell.auth-negative`, `test.cell.contract-fixtures`, `test.cell.stub-scan`, `test.cells.capability-audit`, `test.cells.dataflow-matches-contracts`, `test.docs-updated`, `test.gui.load-time`, `test.gui.parity`, `test.gui.reference-image-exists`, `test.handoff.dry-run`, `test.reg.adjacency-vs-signal`, `test.reg.backend-konformans`, `test.reg.book09-loftet`, `test.reg.bro-dekning`, `test.reg.budsjett-rapporterer-for-lavt`, `test.reg.divergens`, `test.reg.e2e`, `test.reg.evaluering-lokal`, `test.reg.fasit-finnes`, `test.reg.forsoning-komplett`, `test.reg.generert-er-fersk`, `test.reg.goal-uten-tokens`, `test.reg.goal-uttrykk-dekning`, `test.reg.hash-cons-dedup`, `test.reg.ingen-person-noder`, `test.reg.ingen-stille-avvik`, `test.reg.konformans`, `test.reg.konsumenter`, `test.reg.kostnadsprofil`, `test.reg.lagvis-lokale-variabler`, `test.reg.match-gir-ikke-rett`, `test.reg.null-og-positiv`, `test.reg.signal-naar-roten`, `test.reg.token-andel`, `test.reg.unknown-lukket`, `test.regression`, `test.skeleton.no-unreachable-elements`, `test.skeleton.purpose-actions-reachable`, `test.status-current`

</details>

## PDD_haven-visionos_2026-09-10

**Simulert perspektiv:** HAVEN i rommet; Flere Portholes samtidig; Porthole er instansierbar. **Skop:** simulated-scope://gui.
Oppgave: `CellProtocolDocuments/Deliverables/PDD_haven-visionos_2026-09-10/FORMAALSSPEC.md` (§0/§1).

| Rang | Kandidat 6 | Kandidat 1 — TF-IDF |
|---:|---|---|
| 1 | **1** `lesson.scaffold-without-porthole-host-has-no-preview` — For scaffolds uten Porthole-vert: (1) images/README.md må si eksplisitt at bildene er mockups og hva skeleton ikke kan rendre, (2) paritet (… | **8** `lesson.cellbase-decodingerror-shadows-swift` — I App-modulen: skriv Swift.DecodingError når du vil ha standardbibliotekets. Gjelder generelt for typenavn CellBase også definerer — sjekk m… |
| 2 | **2** `lesson.text-ux-is-not-design` — Rendret bilde (Porthole-preview eller mockup) godkjennes før implementering; bildet er akseptansereferanse. | **1** `lesson.scaffold-without-porthole-host-has-no-preview` — For scaffolds uten Porthole-vert: (1) images/README.md må si eksplisitt at bildene er mockups og hva skeleton ikke kan rendre, (2) paritet (… |
| 3 | **3** `lesson.findability-is-not-usability` — En formaalssjekk maa navngi handlingene eieren skal kunne utfore, og testes mot SkeletonReachabilityAudit.reachableActionKeypaths - ikke mot… | **11** `lesson.cellbase-internal-members-look-public` — Sjekk tilgangsnivå og faktisk returverdi før du bruker et CellBase-medlem fra App: grep -n "var <navn>" CellProtocol::Sources/CellBase/.... … |
| 4 | **4** `lesson.tested-a-different-path-than-production` — Naar en test skal si noe om hva brukeren ser, maa den bruke produksjonens egen kodevei - helst produksjonens egen funksjon med produksjonens… | **5** `lesson.unresolvable-condition-is-invisible` — SkeletonReachabilityAudit kjores over hver flate; feiler med elementene som aldri kan sees og handlingene som gaar tapt med dem. Betingelser… |
| 5 | **5** `lesson.unresolvable-condition-is-invisible` — SkeletonReachabilityAudit kjores over hver flate; feiler med elementene som aldri kan sees og handlingene som gaar tapt med dem. Betingelser… | **12** `lesson.valuetype-equality-false-for-objects` — Aldri assert på hele sammensatte ValueType-verdier. Sammenlign kanonisk JSON (JSONEncoder med .sortedKeys) eller pakk ut og sammenlign felt … |
| 6 | **6** `lesson.parity-was-correctness-not-decoration` — Akseptanse sammenligner både bilde og oppførsel (knapper trigger keypaths, felt tar input) — begge i ACCEPT.md. | **4** `lesson.tested-a-different-path-than-production` — Naar en test skal si noe om hva brukeren ser, maa den bruke produksjonens egen kodevei - helst produksjonens egen funksjon med produksjonens… |
| 7 | **7** `lesson.new-cell-must-declare-its-provisioning-mode` — Enhver ny persistert celle i CellScaffold må eksplisitt svare på tre spørsmål før den registreres: (1) skal den opprettes i require-existing… | **6** `lesson.parity-was-correctness-not-decoration` — Akseptanse sammenligner både bilde og oppførsel (knapper trigger keypaths, felt tar input) — begge i ACCEPT.md. |
| 8 | **8** `lesson.cellbase-decodingerror-shadows-swift` — I App-modulen: skriv Swift.DecodingError når du vil ha standardbibliotekets. Gjelder generelt for typenavn CellBase også definerer — sjekk m… | **13** `lesson.syntax-check-reported-as-delivered` — En implementeringsslice er ikke levert før et detached bygg med danger-full-access er kjørt mot arbeidstreet og både bygg og de nye testene … |
| 9 | **9** `lesson.surface-load-alias-miss` — Mål lastetid tre ganger og sjekk logg for navnebom før en flate erklæres ferdig; aliaser må løses server-side eller ikke brukes. | **14** `lesson.local-main-is-not-main` — Før du måler en baseline eller sier at main er rød: git fetch origin main og sammenlign. Er lokal main foran origin/main, er de commitene ik… |
| 10 | **10** `lesson.empty-list-must-not-look-like-calm` — Modeller fravær eksplisitt: én rad per kjent kilde, alltid med, med tilstand read / unreadable / not-configured, og en påkrevd grunn når den… | **3** `lesson.findability-is-not-usability` — En formaalssjekk maa navngi handlingene eieren skal kunne utfore, og testes mot SkeletonReachabilityAudit.reachableActionKeypaths - ikke mot… |

Union: 14 lærdommer; øvrige 30 uvurderte.
- Relevans: 
- Gjentakelser: 
- Håndhevelse / sann grunn: 
- Sekunder: 

<details><summary>Full tekst og testreferanser</summary>

**1 — lesson.scaffold-without-porthole-host-has-no-preview**

Symptom: G1-GUI måtte bruke mockups rendret fra skeleton-JSON; ekte Porthole-preview var umulig.

Forebygging: For scaffolds uten Porthole-vert: (1) images/README.md må si eksplisitt at bildene er mockups og hva skeleton ikke kan rendre, (2) paritet (test.gui.parity) planlegges som egen slice med kjørende scaffold + Binding/Porthole via bridge, ikke som del av implementeringsjobben.

**2 — lesson.text-ux-is-not-design**

Symptom: Kjetil forventet en helt annen flate enn den som ble vist; den tekstlige UX-beskrivelsen var godkjent, bildet var det ikke.

Forebygging: Rendret bilde (Porthole-preview eller mockup) godkjennes før implementering; bildet er akseptansereferanse.

**3 — lesson.findability-is-not-usability**

Symptom: Flatene ble kalt validert fordi de bestod en beskrivelsesaudit; de var samtidig ubrukelige.

Forebygging: En formaalssjekk maa navngi handlingene eieren skal kunne utfore, og testes mot SkeletonReachabilityAudit.reachableActionKeypaths - ikke mot hvor godt formaalet er formulert.

**4 — lesson.tested-a-different-path-than-production**

Symptom: Rot-probene leste relations.state.* gjennom porthole.get og var gronne, mens rendereren aldri fikk de samme dataene.

Forebygging: Naar en test skal si noe om hva brukeren ser, maa den bruke produksjonens egen kodevei - helst produksjonens egen funksjon med produksjonens egne inndata (SkeletonReachabilityAudit kaller condition.evaluate(root: nil, ...) nettopp derfor).

**5 — lesson.unresolvable-condition-is-invisible**

Symptom: Relasjoner-flaten viste tittel og ingen vei inn: ingen filopplasting, ingen knapper. Alle tester gronne.

Forebygging: SkeletonReachabilityAudit kjores over hver flate; test.skeleton.no-unreachable-elements feiler med elementene som aldri kan sees og handlingene som gaar tapt med dem. Betingelser hoerer hjemme inne i List/Grid/Reference-rader, der radens verdi sendes videre; ellers skal cellen avgjore og innhold bindes.

**6 — lesson.parity-was-correctness-not-decoration**

Symptom: Parity-audit mellom Porthole og Binding viste at problemet ikke var manglende dekorasjon, men produktkorrekthet (feil oppførsel).

Forebygging: Akseptanse sammenligner både bilde og oppførsel (knapper trigger keypaths, felt tar input) — begge i ACCEPT.md.

**7 — lesson.new-cell-must-declare-its-provisioning-mode**

Symptom: To nye celler i CellScaffold ga tre nye regresjoner: `OrchestratorPersistenceTests testRequireExistingModeRejectsFreshStorageWithoutCreatingBootstrapCells` (opprettet en celle i require-existing-modus mot fersk lagring) og to `TopUpCheckoutTests` som teller celler i provision-only-modus (5 mot forventet 4).

Forebygging: Enhver ny persistert celle i CellScaffold må eksplisitt svare på tre spørsmål før den registreres: (1) skal den opprettes i require-existing mot fersk lagring? Nei, med mindre den er kanonisk bootstrap. (2) Er den en av de kanoniske eager-bootstrap-cellene som provision-only skal lage? Nesten alltid nei — TopUpCheckoutTests teller dem eksplisitt. (3) Er den en Porthole-publisert flate? Bare da hører den i `reconcilePortholePublishedCellResolves`. Scaffold-intern tilstand registreres i egen funksjon, gated på policy OG provisionOnly, med gjenkjenning av eksisterende mapping.

**8 — lesson.cellbase-decodingerror-shadows-swift**

Symptom: WP1s nye celle ga 50 kompileringsfeil: `type 'DecodingError' has no member 'dataCorruptedError'` og `cannot infer contextual base in reference to member 'registry'`, alle fra én linje.

Forebygging: I App-modulen: skriv `Swift.DecodingError` når du vil ha standardbibliotekets. Gjelder generelt for typenavn CellBase også definerer — sjekk med `grep -rn "enum <Navn>" CellProtocol::Sources/CellBase` før du antar at et kjent Foundation-navn er Foundations.

**9 — lesson.surface-load-alias-miss**

Symptom: Flatelasting tok 46 541 ms (klientens 45 s-timeout) ved bom, 5 000 ms ved treff; målingen 10.08 målte en mislykket lasting.

Forebygging: Mål lastetid tre ganger og sjekk logg for navnebom før en flate erklæres ferdig; aliaser må løses server-side eller ikke brukes.

**10 — lesson.empty-list-must-not-look-like-calm**

Symptom: En flate som samler «hva venter på meg» ser roligere ut jo mindre den får lest. En kilde som svarer 403, et token som er feil, en agent som ikke svarer — alle tre gir en tom liste, og en tom liste ser ut som at ingenting venter.

Forebygging: Modeller fravær eksplisitt: én rad per kjent kilde, alltid med, med tilstand `read` / `unreadable` / `not-configured`, og en påkrevd grunn når den ikke er lest. Skill erklært fravær (vi vet at den ikke er koblet til) fra ukjent fravær (vi fikk ikke spurt) — bare det første får se rolig ut. Ha én boolsk verdi i visningsmodellen (`claimsAllClear`) som er sann på nøyaktig ett sted, og en test som går over **alle** feilutfall og krever at den er falsk og at listen ikke er tom. Gi hvert feilutfall sin egen overskrift: «det virker ikke» hjelper ingen, «token avvist» og «ingen kontakt» krever hver sin handling.

**11 — lesson.cellbase-internal-members-look-public**

Symptom: WP2 stoppet på `'fullPermissionString' is inaccessible due to 'internal' protection level`. Medlemmet finnes og brukes i CellBase selv, så det så ut som et gyldig API.

Forebygging: Sjekk tilgangsnivå og faktisk returverdi før du bruker et CellBase-medlem fra App: `grep -n "var <navn>" CellProtocol::Sources/CellBase/...`. Et medlem som brukes internt i CellBase er ikke automatisk en del av API-et, og navnelikhet betyr ikke verdilikhet.

**12 — lesson.valuetype-equality-false-for-objects**

Symptom: Fire av sju WP1-tester feilet på `XCTAssertEqual` mellom to `ValueType.object` som hadde identisk innhold. Feilmeldingen viste samme nøkler og verdier på begge sider, i ulik rekkefølge.

Forebygging: Aldri assert på hele sammensatte `ValueType`-verdier. Sammenlign kanonisk JSON (`JSONEncoder` med `.sortedKeys`) eller pakk ut og sammenlign felt for felt. Skalarer (`.string`, `.integer`, `.bool`, `.null`) sammenlignes trygt. Merk: dette er et funn i CellBase, ikke bare en testregel — App-kildene destrukturerer riktignok før sammenligning, men en fremtidig `==` på hele verdier vil stille behandle like verdier som ulike. Ikke revidert utover App-kildene.

**13 — lesson.syntax-check-reported-as-delivered**

Symptom: WP1 ble rapportert som «kode og 7 tester levert, syntakssjekken bestod». Et faktisk bygg ga 50 kompileringsfeil, og testene feilet 4 av 7 da de først kunne kjøre.

Forebygging: En implementeringsslice er ikke levert før et detached bygg med `danger-full-access` er kjørt mot arbeidstreet og både bygg og de nye testene er grønne. Legg byggejobben klar FØR slicen kjøres, og skriv i prompten at slicen skal rapportere «skrevet, ikke verifisert» — ikke «levert».

**14 — lesson.local-main-is-not-main**

Symptom: WP0-baselinen var rød og ble meldt som «main bygger ikke». Det var feil. Den commiten baselinen ble målt mot, `ba14895`, lå bare på den LOKALE main-grenen og var aldri pushet; den avhang av CellBase-kode som heller ikke var pushet. origin/main lå fire commits lenger fram, pinnet CellProtocol til en revisjon som ER på CellProtocol sin main, og hadde grønn CI hele tiden. Et helt døgns arbeid ble bygget oppå den lokale commiten.

Forebygging: Før du måler en baseline eller sier at main er rød: `git fetch origin main` og sammenlign. Er lokal main foran origin/main, er de commitene ikke main for andre — bygg aldri videre på dem. Se på CI for origin/main før du konkluderer. `swift package edit` skal aldri være på når noe måles eller meldes verifisert. Og den eneste sjekken som virkelig avgjør: klon fra GitHub til en tom katalog og bygg der. HavenAgentD::Scripts/preflight_before_landing.sh stiller alle fire spørsmålene.

Kjente testrefs (eksistens i snapshot er ikke bevis for at testen er kjørt): `test.backside.absence-states`, `test.backside.four-zones`, `test.build`, `test.cell.auth-negative`, `test.cell.contract-fixtures`, `test.cell.stub-scan`, `test.cells.capability-audit`, `test.cells.dataflow-matches-contracts`, `test.docs-updated`, `test.events.emitted`, `test.events.no-payload`, `test.gui.load-time`, `test.gui.parity`, `test.gui.reference-image-exists`, `test.h1.compile-probe`, `test.handoff.dry-run`, `test.host.capability-profile`, `test.host.current-is-known`, `test.host.deck`, `test.host.multiwindow`, `test.host.no-appkit-in-else`, `test.lint.platform-conditionals`, `test.porthole.instances`, `test.porthole.restore`, `test.pressure.aggregate-complete`, `test.pressure.h11`, `test.radar.no-precision-state`, `test.regression`, `test.room.hig-checks`, `test.skeleton.base-context`, `test.skeleton.no-unreachable-elements`, `test.skeleton.purpose-actions-reachable`, `test.status-current`, `test.styles.hex-count`, `test.tap.no-plaintext-without-key`, `test.tap.records-metadata-only-by-default`, `test.tap.transparent`, `test.tap.valve-changes-traffic`

</details>

## PDD_innholdsvern-lyd-20260909_2026-09-10

**Simulert perspektiv:** Åndsverket forlater ikke huset som fil; Klartekst forlater aldri serveren; Nøkkelen går samme vei som lyden. **Skop:** simulated-scope://musikk.
Oppgave: `CellProtocolDocuments/Deliverables/PDD_innholdsvern-lyd-20260909_2026-09-10/FORMAALSSPEC.md` (§0/§1).

| Rang | Kandidat 6 | Kandidat 1 — TF-IDF |
|---:|---|---|
| 1 | **1** `lesson.ciphertext-field-held-plaintext-hash` — En paastand om at noe er kryptert, signert eller verifisert skal bekreftes paa artefaktet - les bytene, ikke feltet. Et felt som heter ciphe… | **1** `lesson.ciphertext-field-held-plaintext-hash` — En paastand om at noe er kryptert, signert eller verifisert skal bekreftes paa artefaktet - les bytene, ikke feltet. Et felt som heter ciphe… |
| 2 | **2** `lesson.cellscaffold-two-holes` — Ikke porter celler fra CellScaffold til PalazzoScaffold uten å lukke begge hullene; og må være grønne. | **10** `lesson.cellbase-internal-members-look-public` — Sjekk tilgangsnivå og faktisk returverdi før du bruker et CellBase-medlem fra App: grep -n "var <navn>" CellProtocol::Sources/CellBase/.... … |
| 3 | **3** `lesson.entityanchor-keypaths-are-registered` — Skriv aldri testdata til en oppdiktet keypath på en celle. Finn en keypath cellen faktisk registrerer, helst en annen test som allerede bruk… | **11** `lesson.branch-is-empty-after-eight-work-packages` — Skill «filene finnes» fra «branchen har dem». Sjekk git rev-parse <branch> mot git rev-parse <base> som del av hver verifikasjon som påstår … |
| 4 | **4** `lesson.purpose-never-grants-rights` — Et formål kan innsnevre en rettighet, aldri opprette, utvide eller arve en; exact match; feiler lukket. | **12** `lesson.swift-test-exit-code-lies-in-havenagentd` — Les resultatet fra linjen Test run with N tests in M suites passed/failed, ikke fra exitkoden, i alle skript og køjobber for dette repoet. O… |
| 5 | **5** `lesson.empty-list-must-not-look-like-calm` — Modeller fravær eksplisitt: én rad per kjent kilde, alltid med, med tilstand read / unreadable / not-configured, og en påkrevd grunn når den… | **5** `lesson.empty-list-must-not-look-like-calm` — Modeller fravær eksplisitt: én rad per kjent kilde, alltid med, med tilstand read / unreadable / not-configured, og en påkrevd grunn når den… |
| 6 | **6** `lesson.tested-a-different-path-than-production` — Naar en test skal si noe om hva brukeren ser, maa den bruke produksjonens egen kodevei - helst produksjonens egen funksjon med produksjonens… | **3** `lesson.entityanchor-keypaths-are-registered` — Skriv aldri testdata til en oppdiktet keypath på en celle. Finn en keypath cellen faktisk registrerer, helst en annen test som allerede bruk… |
| 7 | **7** `lesson.pkill-pattern-killed-the-queue-job` — Bruk aldri pkill -f <mønster> på en maskin der andre prosesser kan ha teksten i argv. Stopp en prosess ved PID du selv startet, eller ved pg… | **13** `lesson.valuetype-equality-false-for-objects` — Aldri assert på hele sammensatte ValueType-verdier. Sammenlign kanonisk JSON (JSONEncoder med .sortedKeys) eller pakk ut og sammenlign felt … |
| 8 | **8** `lesson.test-the-representation-not-the-issuance-flow` — Skille to spørsmål: «hvordan får noen rollen» og «hva gir rollen». Tester du det andre, installer rollen på husets etablerte måte og test vi… | **14** `lesson.planned-documented-as-implemented` — Docs-diff i samme endring, med 'Last verified against code'-dato; planlagt oppførsel merkes eksplisitt. |
| 9 | **9** `lesson.unresolvable-condition-is-invisible` — SkeletonReachabilityAudit kjores over hver flate; feiler med elementene som aldri kan sees og handlingene som gaar tapt med dem. Betingelser… | **15** `lesson.cellbase-decodingerror-shadows-swift` — I App-modulen: skriv Swift.DecodingError når du vil ha standardbibliotekets. Gjelder generelt for typenavn CellBase også definerer — sjekk m… |
| 10 | **10** `lesson.cellbase-internal-members-look-public` — Sjekk tilgangsnivå og faktisk returverdi før du bruker et CellBase-medlem fra App: grep -n "var <navn>" CellProtocol::Sources/CellBase/.... … | **16** `lesson.bridge-inferred-architecture-from-one-use` — Erklær hver kapabilitet oppgaven bygger på som eget formål med kilde og Avgrensning (pkg.std.cell-combination). |

Union: 16 lærdommer; øvrige 28 uvurderte.
- Relevans: 
- Gjentakelser: 
- Håndhevelse / sann grunn: 
- Sekunder: 

<details><summary>Full tekst og testreferanser</summary>

**1 — lesson.ciphertext-field-held-plaintext-hash**

Symptom: Losen fortalte Kjetil at lyd allerede var kryptert i lagring. Det var feil: filene i prod begynner med ID3 og er vanlig MP3. To ting forte dit. (1) Krypteringskoden som ble lest tilhorer MusicIngestCell paa /mvp/ingest/local, mens Butterpop publiserer gjennom MusicAssetStoreCell.storeLocalAsset, som skriver bytene slik de kommer. (2) storeLocalAsset setter ciphertextSHA256 = plaintextSHA256 = sha256(data), saa manifestet ser kryptert ut selv naar encryptionPolicy er none.

Forebygging: En paastand om at noe er kryptert, signert eller verifisert skal bekreftes paa artefaktet - les bytene, ikke feltet. Et felt som heter ciphertext* skal ikke settes naar encryptionPolicy er none; enten utelates det, eller navnet sier hva det er. Kan bli derivedTest: manifest med encryptionPolicy none har ingen ciphertext-verdi.

**2 — lesson.cellscaffold-two-holes**

Symptom: CellScaffold har tomme booking-/concierge-stubber og autorisasjon som kaster nøkkelstien og bare sjekker eierskap.

Forebygging: Ikke porter celler fra CellScaffold til PalazzoScaffold uten å lukke begge hullene; test.cell.auth-negative og test.cell.stub-scan må være grønne.

**3 — lesson.entityanchor-keypaths-are-registered**

Symptom: WP2-testen skrev en sentinel til `profile` på abonnentens EntityAnchor og fikk `notFound` ved gjenlesing. Skrivingen ga ingen feil.

Forebygging: Skriv aldri testdata til en oppdiktet keypath på en celle. Finn en keypath cellen faktisk registrerer, helst en annen test som allerede bruker den. At et `set` går gjennom er ikke bevis på at keypathen finnes.

**4 — lesson.purpose-never-grants-rights**

Symptom: Risiko for at formålsmatch tolkes som tilgang.

Forebygging: Et formål kan innsnevre en rettighet, aldri opprette, utvide eller arve en; exact match; purpose://prompt.unknown feiler lukket.

**5 — lesson.empty-list-must-not-look-like-calm**

Symptom: En flate som samler «hva venter på meg» ser roligere ut jo mindre den får lest. En kilde som svarer 403, et token som er feil, en agent som ikke svarer — alle tre gir en tom liste, og en tom liste ser ut som at ingenting venter.

Forebygging: Modeller fravær eksplisitt: én rad per kjent kilde, alltid med, med tilstand `read` / `unreadable` / `not-configured`, og en påkrevd grunn når den ikke er lest. Skill erklært fravær (vi vet at den ikke er koblet til) fra ukjent fravær (vi fikk ikke spurt) — bare det første får se rolig ut. Ha én boolsk verdi i visningsmodellen (`claimsAllClear`) som er sann på nøyaktig ett sted, og en test som går over **alle** feilutfall og krever at den er falsk og at listen ikke er tom. Gi hvert feilutfall sin egen overskrift: «det virker ikke» hjelper ingen, «token avvist» og «ingen kontakt» krever hver sin handling.

**6 — lesson.tested-a-different-path-than-production**

Symptom: Rot-probene leste relations.state.* gjennom porthole.get og var gronne, mens rendereren aldri fikk de samme dataene.

Forebygging: Naar en test skal si noe om hva brukeren ser, maa den bruke produksjonens egen kodevei - helst produksjonens egen funksjon med produksjonens egne inndata (SkeletonReachabilityAudit kaller condition.evaluate(root: nil, ...) nettopp derfor).

**7 — lesson.pkill-pattern-killed-the-queue-job**

Symptom: En commit-jobb i Losen-køen døde med EXIT=143 tolv sekunder etter start. Ingen feilmelding, ingen commit. Årsaken var min egen opprydding i et annet skript: `pkill -f "<appnavn>"`.

Forebygging: Bruk aldri `pkill -f <mønster>` på en maskin der andre prosesser kan ha teksten i argv. Stopp en prosess ved PID du selv startet, eller ved `pgrep -x <prosessnavn>` kombinert med en sjekk av `ps -o comm=` mot den nøyaktige kjørbare stien. Dette gjelder særlig når en jobbkø kjører prompter som argument: alt du skriver i en prompt står på en kommandolinje et sted.

**8 — lesson.test-the-representation-not-the-issuance-flow**

Symptom: Alle fire WP4-rolletestene feilet i oppsettet, ikke i det de skulle teste: `deniedNoGrant` på `requestEntry` mot `cell:///AdminEntry`. Testen fikk aldri gitt identiteten rollen.

Forebygging: Skille to spørsmål: «hvordan får noen rollen» og «hva gir rollen». Tester du det andre, installer rollen på husets etablerte måte og test virkningen. Let alltid etter en eksisterende `*TestSupport`-hjelper før du bygger oppsettet selv — `grep -rn "TestSupport" CellScaffold::Tests` — og se hvilke argumenter de andre testene gir den.

**9 — lesson.unresolvable-condition-is-invisible**

Symptom: Relasjoner-flaten viste tittel og ingen vei inn: ingen filopplasting, ingen knapper. Alle tester gronne.

Forebygging: SkeletonReachabilityAudit kjores over hver flate; test.skeleton.no-unreachable-elements feiler med elementene som aldri kan sees og handlingene som gaar tapt med dem. Betingelser hoerer hjemme inne i List/Grid/Reference-rader, der radens verdi sendes videre; ellers skal cellen avgjore og innhold bindes.

**10 — lesson.cellbase-internal-members-look-public**

Symptom: WP2 stoppet på `'fullPermissionString' is inaccessible due to 'internal' protection level`. Medlemmet finnes og brukes i CellBase selv, så det så ut som et gyldig API.

Forebygging: Sjekk tilgangsnivå og faktisk returverdi før du bruker et CellBase-medlem fra App: `grep -n "var <navn>" CellProtocol::Sources/CellBase/...`. Et medlem som brukes internt i CellBase er ikke automatisk en del av API-et, og navnelikhet betyr ikke verdilikhet.

**11 — lesson.branch-is-empty-after-eight-work-packages**

Symptom: Åtte arbeidspakker rapportert utført og verifisert, ACCEPT.md skrevet — men `git branch -v` viste at `pdd/scaffold-admin-delegering` fortsatt pekte på samme commit som `main` (`e1f3e22f`). All koden lå ucommittet i et worktree som bare finnes på én maskin. Ett tapt worktree = 2 750 linjer kode og test borte, med full dokumentasjon på at arbeidet var «levert».

Forebygging: Skill «filene finnes» fra «branchen har dem». Sjekk `git rev-parse <branch>` mot `git rev-parse <base>` som del av hver verifikasjon som påstår at noe ligger på en branch; er de like, er branchen tom. Legg en commit-pakke inn i planen etter første grønne bygg, ikke etter siste arbeidspakke. Når worktreet bare kan leses fra macOS, kjør sjekken der — ikke hopp over den fordi verktøyet svarer feil.

**12 — lesson.swift-test-exit-code-lies-in-havenagentd**

Symptom: `swift test` i HavenAgentD avslutter med 1 selv når samtlige 212 tester passerer. Et skript som leser `$?` melder rødt på et helt grønt tre.

Forebygging: Les resultatet fra linjen `Test run with N tests in M suites passed/failed`, ikke fra exitkoden, i alle skript og køjobber for dette repoet. Og fjern det tomme XCTest-målet, eller bygg det for riktig arkitektur, før noen setter opp CI her — ellers vil CI være rød uansett hva som gjøres.

**13 — lesson.valuetype-equality-false-for-objects**

Symptom: Fire av sju WP1-tester feilet på `XCTAssertEqual` mellom to `ValueType.object` som hadde identisk innhold. Feilmeldingen viste samme nøkler og verdier på begge sider, i ulik rekkefølge.

Forebygging: Aldri assert på hele sammensatte `ValueType`-verdier. Sammenlign kanonisk JSON (`JSONEncoder` med `.sortedKeys`) eller pakk ut og sammenlign felt for felt. Skalarer (`.string`, `.integer`, `.bool`, `.null`) sammenlignes trygt. Merk: dette er et funn i CellBase, ikke bare en testregel — App-kildene destrukturerer riktignok før sammenligning, men en fremtidig `==` på hele verdier vil stille behandle like verdier som ulike. Ikke revidert utover App-kildene.

**14 — lesson.planned-documented-as-implemented**

Symptom: Book/05_Flows_Lifecycle.md beskrev sekvensnummer, signatur og replay som ikke finnes i structen.

Forebygging: Docs-diff i samme endring, med 'Last verified against code'-dato; planlagt oppførsel merkes eksplisitt.

**15 — lesson.cellbase-decodingerror-shadows-swift**

Symptom: WP1s nye celle ga 50 kompileringsfeil: `type 'DecodingError' has no member 'dataCorruptedError'` og `cannot infer contextual base in reference to member 'registry'`, alle fra én linje.

Forebygging: I App-modulen: skriv `Swift.DecodingError` når du vil ha standardbibliotekets. Gjelder generelt for typenavn CellBase også definerer — sjekk med `grep -rn "enum <Navn>" CellProtocol::Sources/CellBase` før du antar at et kjent Foundation-navn er Foundations.

**16 — lesson.bridge-inferred-architecture-from-one-use**

Symptom: En kodeassistent sluttet fra én observert bruksmåte av bridge til en egenskap ved arkitekturen og konkluderte feil.

Forebygging: Erklær hver kapabilitet oppgaven bygger på som eget formål med kilde og Avgrensning (pkg.std.cell-combination).

Kjente testrefs (eksistens i snapshot er ikke bevis for at testen er kjørt): `test.binding.samme-terskel`, `test.build`, `test.cell.auth-negative`, `test.cell.contract-fixtures`, `test.cell.stub-scan`, `test.cells.capability-audit`, `test.cells.dataflow-matches-contracts`, `test.docs-updated`, `test.grant.read-gir-ikke-fil`, `test.grant.read-og-store-gir-fil`, `test.gui.load-time`, `test.gui.parity`, `test.gui.reference-image-exists`, `test.handoff.dry-run`, `test.nivaa.endrer-levering`, `test.noekkel.levetid`, `test.noekkel.uten-token-avvist`, `test.regression`, `test.skeleton.no-unreachable-elements`, `test.skeleton.purpose-actions-reachable`, `test.status-current`, `test.tekst.ingen-overslag`, `test.uttrekk.ingen-spillbar-fil`, `test.uttrekk.produksjonsstien`

</details>

## PDD_musikkstatistikk-20260904_2026-09-05

**Simulert perspektiv:** Bruk synlig, uten overvåking; Anonym: teller, ikke logg; Anonym gjennomspilling, hvis det går rent. **Skop:** simulated-scope://musikk.
Oppgave: `CellProtocolDocuments/Deliverables/PDD_musikkstatistikk-20260904_2026-09-05/FORMAALSSPEC.md` (§0/§1).

| Rang | Kandidat 6 | Kandidat 1 — TF-IDF |
|---:|---|---|
| 1 | **1** `lesson.empty-list-must-not-look-like-calm` — Modeller fravær eksplisitt: én rad per kjent kilde, alltid med, med tilstand read / unreadable / not-configured, og en påkrevd grunn når den… | **1** `lesson.empty-list-must-not-look-like-calm` — Modeller fravær eksplisitt: én rad per kjent kilde, alltid med, med tilstand read / unreadable / not-configured, og en påkrevd grunn når den… |
| 2 | **2** `lesson.entityanchor-keypaths-are-registered` — Skriv aldri testdata til en oppdiktet keypath på en celle. Finn en keypath cellen faktisk registrerer, helst en annen test som allerede bruk… | **3** `lesson.ciphertext-field-held-plaintext-hash` — En paastand om at noe er kryptert, signert eller verifisert skal bekreftes paa artefaktet - les bytene, ikke feltet. Et felt som heter ciphe… |
| 3 | **3** `lesson.ciphertext-field-held-plaintext-hash` — En paastand om at noe er kryptert, signert eller verifisert skal bekreftes paa artefaktet - les bytene, ikke feltet. Et felt som heter ciphe… | **8** `lesson.cellbase-internal-members-look-public` — Sjekk tilgangsnivå og faktisk returverdi før du bruker et CellBase-medlem fra App: grep -n "var <navn>" CellProtocol::Sources/CellBase/.... … |
| 4 | **4** `lesson.plan-instead-of-delivery` — G1 godkjenner formål, ikke arbeid; etter G2 telles bare artefakter listet i §3 'Det du kommer til å se' som fremdrift. Et dokument om levera… | **7** `lesson.test-the-representation-not-the-issuance-flow` — Skille to spørsmål: «hvordan får noen rollen» og «hva gir rollen». Tester du det andre, installer rollen på husets etablerte måte og test vi… |
| 5 | **5** `lesson.surface-load-alias-miss` — Mål lastetid tre ganger og sjekk logg for navnebom før en flate erklæres ferdig; aliaser må løses server-side eller ikke brukes. | **2** `lesson.entityanchor-keypaths-are-registered` — Skriv aldri testdata til en oppdiktet keypath på en celle. Finn en keypath cellen faktisk registrerer, helst en annen test som allerede bruk… |
| 6 | **6** `lesson.new-cell-must-declare-its-provisioning-mode` — Enhver ny persistert celle i CellScaffold må eksplisitt svare på tre spørsmål før den registreres: (1) skal den opprettes i require-existing… | **11** `lesson.unresolvable-condition-is-invisible` — SkeletonReachabilityAudit kjores over hver flate; feiler med elementene som aldri kan sees og handlingene som gaar tapt med dem. Betingelser… |
| 7 | **7** `lesson.test-the-representation-not-the-issuance-flow` — Skille to spørsmål: «hvordan får noen rollen» og «hva gir rollen». Tester du det andre, installer rollen på husets etablerte måte og test vi… | **9** `lesson.valuetype-equality-false-for-objects` — Aldri assert på hele sammensatte ValueType-verdier. Sammenlign kanonisk JSON (JSONEncoder med .sortedKeys) eller pakk ut og sammenlign felt … |
| 8 | **8** `lesson.cellbase-internal-members-look-public` — Sjekk tilgangsnivå og faktisk returverdi før du bruker et CellBase-medlem fra App: grep -n "var <navn>" CellProtocol::Sources/CellBase/.... … | **10** `lesson.swift-test-exit-code-lies-in-havenagentd` — Les resultatet fra linjen Test run with N tests in M suites passed/failed, ikke fra exitkoden, i alle skript og køjobber for dette repoet. O… |
| 9 | **9** `lesson.valuetype-equality-false-for-objects` — Aldri assert på hele sammensatte ValueType-verdier. Sammenlign kanonisk JSON (JSONEncoder med .sortedKeys) eller pakk ut og sammenlign felt … | **12** `lesson.cellbase-decodingerror-shadows-swift` — I App-modulen: skriv Swift.DecodingError når du vil ha standardbibliotekets. Gjelder generelt for typenavn CellBase også definerer — sjekk m… |
| 10 | **10** `lesson.swift-test-exit-code-lies-in-havenagentd` — Les resultatet fra linjen Test run with N tests in M suites passed/failed, ikke fra exitkoden, i alle skript og køjobber for dette repoet. O… | **4** `lesson.plan-instead-of-delivery` — G1 godkjenner formål, ikke arbeid; etter G2 telles bare artefakter listet i §3 'Det du kommer til å se' som fremdrift. Et dokument om levera… |

Union: 12 lærdommer; øvrige 32 uvurderte.
- Relevans: 
- Gjentakelser: 
- Håndhevelse / sann grunn: 
- Sekunder: 

<details><summary>Full tekst og testreferanser</summary>

**1 — lesson.empty-list-must-not-look-like-calm**

Symptom: En flate som samler «hva venter på meg» ser roligere ut jo mindre den får lest. En kilde som svarer 403, et token som er feil, en agent som ikke svarer — alle tre gir en tom liste, og en tom liste ser ut som at ingenting venter.

Forebygging: Modeller fravær eksplisitt: én rad per kjent kilde, alltid med, med tilstand `read` / `unreadable` / `not-configured`, og en påkrevd grunn når den ikke er lest. Skill erklært fravær (vi vet at den ikke er koblet til) fra ukjent fravær (vi fikk ikke spurt) — bare det første får se rolig ut. Ha én boolsk verdi i visningsmodellen (`claimsAllClear`) som er sann på nøyaktig ett sted, og en test som går over **alle** feilutfall og krever at den er falsk og at listen ikke er tom. Gi hvert feilutfall sin egen overskrift: «det virker ikke» hjelper ingen, «token avvist» og «ingen kontakt» krever hver sin handling.

**2 — lesson.entityanchor-keypaths-are-registered**

Symptom: WP2-testen skrev en sentinel til `profile` på abonnentens EntityAnchor og fikk `notFound` ved gjenlesing. Skrivingen ga ingen feil.

Forebygging: Skriv aldri testdata til en oppdiktet keypath på en celle. Finn en keypath cellen faktisk registrerer, helst en annen test som allerede bruker den. At et `set` går gjennom er ikke bevis på at keypathen finnes.

**3 — lesson.ciphertext-field-held-plaintext-hash**

Symptom: Losen fortalte Kjetil at lyd allerede var kryptert i lagring. Det var feil: filene i prod begynner med ID3 og er vanlig MP3. To ting forte dit. (1) Krypteringskoden som ble lest tilhorer MusicIngestCell paa /mvp/ingest/local, mens Butterpop publiserer gjennom MusicAssetStoreCell.storeLocalAsset, som skriver bytene slik de kommer. (2) storeLocalAsset setter ciphertextSHA256 = plaintextSHA256 = sha256(data), saa manifestet ser kryptert ut selv naar encryptionPolicy er none.

Forebygging: En paastand om at noe er kryptert, signert eller verifisert skal bekreftes paa artefaktet - les bytene, ikke feltet. Et felt som heter ciphertext* skal ikke settes naar encryptionPolicy er none; enten utelates det, eller navnet sier hva det er. Kan bli derivedTest: manifest med encryptionPolicy none har ingen ciphertext-verdi.

**4 — lesson.plan-instead-of-delivery**

Symptom: Kjetil ba om en leveranse flere ganger og fikk planer/dokumenter om leveransen i stedet.

Forebygging: G1 godkjenner formål, ikke arbeid; etter G2 telles bare artefakter listet i §3 'Det du kommer til å se' som fremdrift. Et dokument om leveransen teller aldri som leveransen.

**5 — lesson.surface-load-alias-miss**

Symptom: Flatelasting tok 46 541 ms (klientens 45 s-timeout) ved bom, 5 000 ms ved treff; målingen 10.08 målte en mislykket lasting.

Forebygging: Mål lastetid tre ganger og sjekk logg for navnebom før en flate erklæres ferdig; aliaser må løses server-side eller ikke brukes.

**6 — lesson.new-cell-must-declare-its-provisioning-mode**

Symptom: To nye celler i CellScaffold ga tre nye regresjoner: `OrchestratorPersistenceTests testRequireExistingModeRejectsFreshStorageWithoutCreatingBootstrapCells` (opprettet en celle i require-existing-modus mot fersk lagring) og to `TopUpCheckoutTests` som teller celler i provision-only-modus (5 mot forventet 4).

Forebygging: Enhver ny persistert celle i CellScaffold må eksplisitt svare på tre spørsmål før den registreres: (1) skal den opprettes i require-existing mot fersk lagring? Nei, med mindre den er kanonisk bootstrap. (2) Er den en av de kanoniske eager-bootstrap-cellene som provision-only skal lage? Nesten alltid nei — TopUpCheckoutTests teller dem eksplisitt. (3) Er den en Porthole-publisert flate? Bare da hører den i `reconcilePortholePublishedCellResolves`. Scaffold-intern tilstand registreres i egen funksjon, gated på policy OG provisionOnly, med gjenkjenning av eksisterende mapping.

**7 — lesson.test-the-representation-not-the-issuance-flow**

Symptom: Alle fire WP4-rolletestene feilet i oppsettet, ikke i det de skulle teste: `deniedNoGrant` på `requestEntry` mot `cell:///AdminEntry`. Testen fikk aldri gitt identiteten rollen.

Forebygging: Skille to spørsmål: «hvordan får noen rollen» og «hva gir rollen». Tester du det andre, installer rollen på husets etablerte måte og test virkningen. Let alltid etter en eksisterende `*TestSupport`-hjelper før du bygger oppsettet selv — `grep -rn "TestSupport" CellScaffold::Tests` — og se hvilke argumenter de andre testene gir den.

**8 — lesson.cellbase-internal-members-look-public**

Symptom: WP2 stoppet på `'fullPermissionString' is inaccessible due to 'internal' protection level`. Medlemmet finnes og brukes i CellBase selv, så det så ut som et gyldig API.

Forebygging: Sjekk tilgangsnivå og faktisk returverdi før du bruker et CellBase-medlem fra App: `grep -n "var <navn>" CellProtocol::Sources/CellBase/...`. Et medlem som brukes internt i CellBase er ikke automatisk en del av API-et, og navnelikhet betyr ikke verdilikhet.

**9 — lesson.valuetype-equality-false-for-objects**

Symptom: Fire av sju WP1-tester feilet på `XCTAssertEqual` mellom to `ValueType.object` som hadde identisk innhold. Feilmeldingen viste samme nøkler og verdier på begge sider, i ulik rekkefølge.

Forebygging: Aldri assert på hele sammensatte `ValueType`-verdier. Sammenlign kanonisk JSON (`JSONEncoder` med `.sortedKeys`) eller pakk ut og sammenlign felt for felt. Skalarer (`.string`, `.integer`, `.bool`, `.null`) sammenlignes trygt. Merk: dette er et funn i CellBase, ikke bare en testregel — App-kildene destrukturerer riktignok før sammenligning, men en fremtidig `==` på hele verdier vil stille behandle like verdier som ulike. Ikke revidert utover App-kildene.

**10 — lesson.swift-test-exit-code-lies-in-havenagentd**

Symptom: `swift test` i HavenAgentD avslutter med 1 selv når samtlige 212 tester passerer. Et skript som leser `$?` melder rødt på et helt grønt tre.

Forebygging: Les resultatet fra linjen `Test run with N tests in M suites passed/failed`, ikke fra exitkoden, i alle skript og køjobber for dette repoet. Og fjern det tomme XCTest-målet, eller bygg det for riktig arkitektur, før noen setter opp CI her — ellers vil CI være rød uansett hva som gjøres.

**11 — lesson.unresolvable-condition-is-invisible**

Symptom: Relasjoner-flaten viste tittel og ingen vei inn: ingen filopplasting, ingen knapper. Alle tester gronne.

Forebygging: SkeletonReachabilityAudit kjores over hver flate; test.skeleton.no-unreachable-elements feiler med elementene som aldri kan sees og handlingene som gaar tapt med dem. Betingelser hoerer hjemme inne i List/Grid/Reference-rader, der radens verdi sendes videre; ellers skal cellen avgjore og innhold bindes.

**12 — lesson.cellbase-decodingerror-shadows-swift**

Symptom: WP1s nye celle ga 50 kompileringsfeil: `type 'DecodingError' has no member 'dataCorruptedError'` og `cannot infer contextual base in reference to member 'registry'`, alle fra én linje.

Forebygging: I App-modulen: skriv `Swift.DecodingError` når du vil ha standardbibliotekets. Gjelder generelt for typenavn CellBase også definerer — sjekk med `grep -rn "enum <Navn>" CellProtocol::Sources/CellBase` før du antar at et kjent Foundation-navn er Foundations.

Kjente testrefs (eksistens i snapshot er ikke bevis for at testen er kjørt): `test.build`, `test.cell.auth-negative`, `test.cell.contract-fixtures`, `test.cell.stub-scan`, `test.cells.capability-audit`, `test.cells.dataflow-matches-contracts`, `test.docs-updated`, `test.gui.load-time`, `test.gui.parity`, `test.gui.reference-image-exists`, `test.handoff.dry-run`, `test.levert.dekning-stemmer`, `test.levert.overlapp-telles-en-gang`, `test.lyttet.fullfoert-settes`, `test.lyttet.klienten-kan-ikke-lyve-fritt`, `test.nedlasting.teller-for-seg`, `test.regression`, `test.samtykke.ingen-rad-uten-avtale`, `test.samtykke.trukket-sletter`, `test.skeleton.no-unreachable-elements`, `test.skeleton.purpose-actions-reachable`, `test.status-current`, `test.visning.blindflekk`, `test.visning.to-kolonner`

</details>

## PDD_palazzo-gjestebestilling_2026-09-03

**Simulert perspektiv:** ukjent; ukjent. **Skop:** simulated-scope://palazzo.
Oppgave: `CellProtocolDocuments/Deliverables/PDD_palazzo-gjestebestilling_2026-09-03/FORMAALSSPEC.md` (§0/§1).

| Rang | Kandidat 6 | Kandidat 1 — TF-IDF |
|---:|---|---|
| 1 | **1** `lesson.bridge-inferred-architecture-from-one-use` — Erklær hver kapabilitet oppgaven bygger på som eget formål med kilde og Avgrensning (pkg.std.cell-combination). | **1** `lesson.bridge-inferred-architecture-from-one-use` — Erklær hver kapabilitet oppgaven bygger på som eget formål med kilde og Avgrensning (pkg.std.cell-combination). |
| 2 | **2** `lesson.empty-list-must-not-look-like-calm` — Modeller fravær eksplisitt: én rad per kjent kilde, alltid med, med tilstand read / unreadable / not-configured, og en påkrevd grunn når den… | **2** `lesson.empty-list-must-not-look-like-calm` — Modeller fravær eksplisitt: én rad per kjent kilde, alltid med, med tilstand read / unreadable / not-configured, og en påkrevd grunn når den… |
| 3 | **3** `lesson.unresolvable-condition-is-invisible` — SkeletonReachabilityAudit kjores over hver flate; feiler med elementene som aldri kan sees og handlingene som gaar tapt med dem. Betingelser… | **5** `lesson.scaffold-without-porthole-host-has-no-preview` — For scaffolds uten Porthole-vert: (1) images/README.md må si eksplisitt at bildene er mockups og hva skeleton ikke kan rendre, (2) paritet (… |
| 4 | **4** `lesson.decomposition-is-classification` — Dekomponering velger fra Book 23 + pakker først; nye noder merkes 'candidate' og navngis av Claude, aldri implisitt av en modell. | **3** `lesson.unresolvable-condition-is-invisible` — SkeletonReachabilityAudit kjores over hver flate; feiler med elementene som aldri kan sees og handlingene som gaar tapt med dem. Betingelser… |
| 5 | **5** `lesson.scaffold-without-porthole-host-has-no-preview` — For scaffolds uten Porthole-vert: (1) images/README.md må si eksplisitt at bildene er mockups og hva skeleton ikke kan rendre, (2) paritet (… | **10** `lesson.syntax-check-reported-as-delivered` — En implementeringsslice er ikke levert før et detached bygg med danger-full-access er kjørt mot arbeidstreet og både bygg og de nye testene … |
| 6 | **6** `lesson.purpose-never-grants-rights` — Et formål kan innsnevre en rettighet, aldri opprette, utvide eller arve en; exact match; feiler lukket. | **11** `lesson.findability-is-not-usability` — En formaalssjekk maa navngi handlingene eieren skal kunne utfore, og testes mot SkeletonReachabilityAudit.reachableActionKeypaths - ikke mot… |
| 7 | **7** `lesson.test-the-representation-not-the-issuance-flow` — Skille to spørsmål: «hvordan får noen rollen» og «hva gir rollen». Tester du det andre, installer rollen på husets etablerte måte og test vi… | **12** `lesson.text-ux-is-not-design` — Rendret bilde (Porthole-preview eller mockup) godkjennes før implementering; bildet er akseptansereferanse. |
| 8 | **8** `lesson.baseline-measured-another-pdds-branch` — WP0 måler en ren eksport av den revisjonen arbeidet skal gå ut fra (git archive <rev> \| tar -x -C <scratch>), ikke det delte arbeidstreet. … | **6** `lesson.purpose-never-grants-rights` — Et formål kan innsnevre en rettighet, aldri opprette, utvide eller arve en; exact match; feiler lukket. |
| 9 | **9** `lesson.a-red-baseline-is-a-question-not-an-answer` — Svar på tre spørsmål før du gjør noe med en rød baseline: er utsjekket mitt likt origin? er CI grønn på origin/main? hvilken commit gjorde d… | **13** `lesson.free-text-is-not-a-declaration` — Formålsnoder skal ha strukturerte felt (goal, verifier, avgrensning, surfaces) — ikke bare summary; usikre noder rutes til Kjetil med confid… |
| 10 | **10** `lesson.syntax-check-reported-as-delivered` — En implementeringsslice er ikke levert før et detached bygg med danger-full-access er kjørt mot arbeidstreet og både bygg og de nye testene … | **14** `lesson.corr-approval-surfaces-timed-out` — FORMAALSSPEC.md §2 lister avhengigheter som egne formål med verifier; pkg.std.everything-works og gui.surface-loads-in-time må være grønne f… |

Union: 14 lærdommer; øvrige 30 uvurderte.
- Relevans: 
- Gjentakelser: 
- Håndhevelse / sann grunn: 
- Sekunder: 

<details><summary>Full tekst og testreferanser</summary>

**1 — lesson.bridge-inferred-architecture-from-one-use**

Symptom: En kodeassistent sluttet fra én observert bruksmåte av bridge til en egenskap ved arkitekturen og konkluderte feil.

Forebygging: Erklær hver kapabilitet oppgaven bygger på som eget formål med kilde og Avgrensning (pkg.std.cell-combination).

**2 — lesson.empty-list-must-not-look-like-calm**

Symptom: En flate som samler «hva venter på meg» ser roligere ut jo mindre den får lest. En kilde som svarer 403, et token som er feil, en agent som ikke svarer — alle tre gir en tom liste, og en tom liste ser ut som at ingenting venter.

Forebygging: Modeller fravær eksplisitt: én rad per kjent kilde, alltid med, med tilstand `read` / `unreadable` / `not-configured`, og en påkrevd grunn når den ikke er lest. Skill erklært fravær (vi vet at den ikke er koblet til) fra ukjent fravær (vi fikk ikke spurt) — bare det første får se rolig ut. Ha én boolsk verdi i visningsmodellen (`claimsAllClear`) som er sann på nøyaktig ett sted, og en test som går over **alle** feilutfall og krever at den er falsk og at listen ikke er tom. Gi hvert feilutfall sin egen overskrift: «det virker ikke» hjelper ingen, «token avvist» og «ingen kontakt» krever hver sin handling.

**3 — lesson.unresolvable-condition-is-invisible**

Symptom: Relasjoner-flaten viste tittel og ingen vei inn: ingen filopplasting, ingen knapper. Alle tester gronne.

Forebygging: SkeletonReachabilityAudit kjores over hver flate; test.skeleton.no-unreachable-elements feiler med elementene som aldri kan sees og handlingene som gaar tapt med dem. Betingelser hoerer hjemme inne i List/Grid/Reference-rader, der radens verdi sendes videre; ellers skal cellen avgjore og innhold bindes.

**4 — lesson.decomposition-is-classification**

Symptom: Modeller som genererte purpose://-refs fritt hallusinerte referanser.

Forebygging: Dekomponering velger fra Book 23 + pakker først; nye noder merkes 'candidate' og navngis av Claude, aldri implisitt av en modell.

**5 — lesson.scaffold-without-porthole-host-has-no-preview**

Symptom: G1-GUI måtte bruke mockups rendret fra skeleton-JSON; ekte Porthole-preview var umulig.

Forebygging: For scaffolds uten Porthole-vert: (1) images/README.md må si eksplisitt at bildene er mockups og hva skeleton ikke kan rendre, (2) paritet (test.gui.parity) planlegges som egen slice med kjørende scaffold + Binding/Porthole via bridge, ikke som del av implementeringsjobben.

**6 — lesson.purpose-never-grants-rights**

Symptom: Risiko for at formålsmatch tolkes som tilgang.

Forebygging: Et formål kan innsnevre en rettighet, aldri opprette, utvide eller arve en; exact match; purpose://prompt.unknown feiler lukket.

**7 — lesson.test-the-representation-not-the-issuance-flow**

Symptom: Alle fire WP4-rolletestene feilet i oppsettet, ikke i det de skulle teste: `deniedNoGrant` på `requestEntry` mot `cell:///AdminEntry`. Testen fikk aldri gitt identiteten rollen.

Forebygging: Skille to spørsmål: «hvordan får noen rollen» og «hva gir rollen». Tester du det andre, installer rollen på husets etablerte måte og test virkningen. Let alltid etter en eksisterende `*TestSupport`-hjelper før du bygger oppsettet selv — `grep -rn "TestSupport" CellScaffold::Tests` — og se hvilke argumenter de andre testene gir den.

**8 — lesson.baseline-measured-another-pdds-branch**

Symptom: WP0 målte `pdd/tillitspakke-agentflaate` med 181 skitne oppføringer, ikke et rent utgangspunkt for sin egen PDD. En regresjonsbaseline derfra sier ingenting om hva denne PDD-en endrer.

Forebygging: WP0 måler en ren eksport av den revisjonen arbeidet skal gå ut fra (`git archive <rev> | tar -x -C <scratch>`), ikke det delte arbeidstreet. Er arbeidstreet opptatt av en annen PDD, er det en planopplysning som hører i STATUS, ikke noe implementeringen skal jobbe rundt.

**9 — lesson.a-red-baseline-is-a-question-not-an-answer**

Symptom: En rød baseline ble behandlet som en opplysning om prosjektet, og arbeidet gikk videre med et tiltak som gjorde den grønn. Tiltaket skjulte årsaken i stedet for å fjerne den.

Forebygging: Svar på tre spørsmål før du gjør noe med en rød baseline: er utsjekket mitt likt origin? er CI grønn på origin/main? hvilken commit gjorde den rød, og hvem eier den? Først når svaret er «prosjektet er faktisk rødt» er det riktig å jobbe rundt det — og da som en egen, navngitt sak, ikke som en stille lokal omgåelse.

**10 — lesson.syntax-check-reported-as-delivered**

Symptom: WP1 ble rapportert som «kode og 7 tester levert, syntakssjekken bestod». Et faktisk bygg ga 50 kompileringsfeil, og testene feilet 4 av 7 da de først kunne kjøre.

Forebygging: En implementeringsslice er ikke levert før et detached bygg med `danger-full-access` er kjørt mot arbeidstreet og både bygg og de nye testene er grønne. Legg byggejobben klar FØR slicen kjøres, og skriv i prompten at slicen skal rapportere «skrevet, ikke verifisert» — ikke «levert».

**11 — lesson.findability-is-not-usability**

Symptom: Flatene ble kalt validert fordi de bestod en beskrivelsesaudit; de var samtidig ubrukelige.

Forebygging: En formaalssjekk maa navngi handlingene eieren skal kunne utfore, og testes mot SkeletonReachabilityAudit.reachableActionKeypaths - ikke mot hvor godt formaalet er formulert.

**12 — lesson.text-ux-is-not-design**

Symptom: Kjetil forventet en helt annen flate enn den som ble vist; den tekstlige UX-beskrivelsen var godkjent, bildet var det ikke.

Forebygging: Rendret bilde (Porthole-preview eller mockup) godkjennes før implementering; bildet er akseptansereferanse.

**13 — lesson.free-text-is-not-a-declaration**

Symptom: Leksikalsk avledning fra fri formålstekst ga F1 0,060; strukturerte erklæringer ga 0,686 og 0,909 med ruting til menneske.

Forebygging: Formålsnoder skal ha strukturerte felt (goal, verifier, avgrensning, surfaces) — ikke bare summary; usikre noder rutes til Kjetil med confidence.

**14 — lesson.corr-approval-surfaces-timed-out**

Symptom: Corr-godkjenningen (Vegar) er utestet fordi flater/godkjenninger timet ut før testing rakk å skje.

Forebygging: FORMAALSSPEC.md §2 lister avhengigheter som egne formål med verifier; pkg.std.everything-works og gui.surface-loads-in-time må være grønne før den egentlige testen kjøres.

Kjente testrefs (eksistens i snapshot er ikke bevis for at testen er kjørt): `test.build`, `test.cell.auth-negative`, `test.cell.contract-fixtures`, `test.cell.stub-scan`, `test.cells.capability-audit`, `test.cells.dataflow-matches-contracts`, `test.docs-updated`, `test.gui.load-time`, `test.gui.parity`, `test.gui.reference-image-exists`, `test.handoff.dry-run`, `test.regression`, `test.skeleton.no-unreachable-elements`, `test.skeleton.purpose-actions-reachable`, `test.status-current`

</details>

## PDD_palazzo-rollesimulering_2026-09-08

**Simulert perspektiv:** Hver rolle når sine formål, og hvert stopp er begrunnet; Rollene har nedskrevne formål med observerbart utfall; Simulert aktør går produksjonens vei. **Skop:** simulated-scope://palazzo.
Oppgave: `CellProtocolDocuments/Deliverables/PDD_palazzo-rollesimulering_2026-09-08/FORMAALSSPEC.md` (§0/§1).

| Rang | Kandidat 6 | Kandidat 1 — TF-IDF |
|---:|---|---|
| 1 | **1** `lesson.decomposition-is-classification` — Dekomponering velger fra Book 23 + pakker først; nye noder merkes 'candidate' og navngis av Claude, aldri implisitt av en modell. | **8** `lesson.cellscaffold-two-holes` — Ikke porter celler fra CellScaffold til PalazzoScaffold uten å lukke begge hullene; og må være grønne. |
| 2 | **2** `lesson.entityanchor-keypaths-are-registered` — Skriv aldri testdata til en oppdiktet keypath på en celle. Finn en keypath cellen faktisk registrerer, helst en annen test som allerede bruk… | **6** `lesson.scaffold-without-porthole-host-has-no-preview` — For scaffolds uten Porthole-vert: (1) images/README.md må si eksplisitt at bildene er mockups og hva skeleton ikke kan rendre, (2) paritet (… |
| 3 | **3** `lesson.test-the-representation-not-the-issuance-flow` — Skille to spørsmål: «hvordan får noen rollen» og «hva gir rollen». Tester du det andre, installer rollen på husets etablerte måte og test vi… | **3** `lesson.test-the-representation-not-the-issuance-flow` — Skille to spørsmål: «hvordan får noen rollen» og «hva gir rollen». Tester du det andre, installer rollen på husets etablerte måte og test vi… |
| 4 | **4** `lesson.empty-list-must-not-look-like-calm` — Modeller fravær eksplisitt: én rad per kjent kilde, alltid med, med tilstand read / unreadable / not-configured, og en påkrevd grunn når den… | **2** `lesson.entityanchor-keypaths-are-registered` — Skriv aldri testdata til en oppdiktet keypath på en celle. Finn en keypath cellen faktisk registrerer, helst en annen test som allerede bruk… |
| 5 | **5** `lesson.purpose-never-grants-rights` — Et formål kan innsnevre en rettighet, aldri opprette, utvide eller arve en; exact match; feiler lukket. | **5** `lesson.purpose-never-grants-rights` — Et formål kan innsnevre en rettighet, aldri opprette, utvide eller arve en; exact match; feiler lukket. |
| 6 | **6** `lesson.scaffold-without-porthole-host-has-no-preview` — For scaffolds uten Porthole-vert: (1) images/README.md må si eksplisitt at bildene er mockups og hva skeleton ikke kan rendre, (2) paritet (… | **7** `lesson.queue-job-file-before-prompt` — Skriv <id>.prompt.md først og <id>.job sist, helst som mv fra en tmp-fil i samme mappe — .job er registreringssignalet, slik job.json er det… |
| 7 | **7** `lesson.queue-job-file-before-prompt` — Skriv <id>.prompt.md først og <id>.job sist, helst som mv fra en tmp-fil i samme mappe — .job er registreringssignalet, slik job.json er det… | **4** `lesson.empty-list-must-not-look-like-calm` — Modeller fravær eksplisitt: én rad per kjent kilde, alltid med, med tilstand read / unreadable / not-configured, og en påkrevd grunn når den… |
| 8 | **8** `lesson.cellscaffold-two-holes` — Ikke porter celler fra CellScaffold til PalazzoScaffold uten å lukke begge hullene; og må være grønne. | **9** `lesson.bridge-inferred-architecture-from-one-use` — Erklær hver kapabilitet oppgaven bygger på som eget formål med kilde og Avgrensning (pkg.std.cell-combination). |
| 9 | **9** `lesson.bridge-inferred-architecture-from-one-use` — Erklær hver kapabilitet oppgaven bygger på som eget formål med kilde og Avgrensning (pkg.std.cell-combination). | **11** `lesson.corr-approval-surfaces-timed-out` — FORMAALSSPEC.md §2 lister avhengigheter som egne formål med verifier; pkg.std.everything-works og gui.surface-loads-in-time må være grønne f… |
| 10 | **10** `lesson.tested-a-different-path-than-production` — Naar en test skal si noe om hva brukeren ser, maa den bruke produksjonens egen kodevei - helst produksjonens egen funksjon med produksjonens… | **10** `lesson.tested-a-different-path-than-production` — Naar en test skal si noe om hva brukeren ser, maa den bruke produksjonens egen kodevei - helst produksjonens egen funksjon med produksjonens… |

Union: 11 lærdommer; øvrige 33 uvurderte.
- Relevans: 
- Gjentakelser: 
- Håndhevelse / sann grunn: 
- Sekunder: 

<details><summary>Full tekst og testreferanser</summary>

**1 — lesson.decomposition-is-classification**

Symptom: Modeller som genererte purpose://-refs fritt hallusinerte referanser.

Forebygging: Dekomponering velger fra Book 23 + pakker først; nye noder merkes 'candidate' og navngis av Claude, aldri implisitt av en modell.

**2 — lesson.entityanchor-keypaths-are-registered**

Symptom: WP2-testen skrev en sentinel til `profile` på abonnentens EntityAnchor og fikk `notFound` ved gjenlesing. Skrivingen ga ingen feil.

Forebygging: Skriv aldri testdata til en oppdiktet keypath på en celle. Finn en keypath cellen faktisk registrerer, helst en annen test som allerede bruker den. At et `set` går gjennom er ikke bevis på at keypathen finnes.

**3 — lesson.test-the-representation-not-the-issuance-flow**

Symptom: Alle fire WP4-rolletestene feilet i oppsettet, ikke i det de skulle teste: `deniedNoGrant` på `requestEntry` mot `cell:///AdminEntry`. Testen fikk aldri gitt identiteten rollen.

Forebygging: Skille to spørsmål: «hvordan får noen rollen» og «hva gir rollen». Tester du det andre, installer rollen på husets etablerte måte og test virkningen. Let alltid etter en eksisterende `*TestSupport`-hjelper før du bygger oppsettet selv — `grep -rn "TestSupport" CellScaffold::Tests` — og se hvilke argumenter de andre testene gir den.

**4 — lesson.empty-list-must-not-look-like-calm**

Symptom: En flate som samler «hva venter på meg» ser roligere ut jo mindre den får lest. En kilde som svarer 403, et token som er feil, en agent som ikke svarer — alle tre gir en tom liste, og en tom liste ser ut som at ingenting venter.

Forebygging: Modeller fravær eksplisitt: én rad per kjent kilde, alltid med, med tilstand `read` / `unreadable` / `not-configured`, og en påkrevd grunn når den ikke er lest. Skill erklært fravær (vi vet at den ikke er koblet til) fra ukjent fravær (vi fikk ikke spurt) — bare det første får se rolig ut. Ha én boolsk verdi i visningsmodellen (`claimsAllClear`) som er sann på nøyaktig ett sted, og en test som går over **alle** feilutfall og krever at den er falsk og at listen ikke er tom. Gi hvert feilutfall sin egen overskrift: «det virker ikke» hjelper ingen, «token avvist» og «ingen kontakt» krever hver sin handling.

**5 — lesson.purpose-never-grants-rights**

Symptom: Risiko for at formålsmatch tolkes som tilgang.

Forebygging: Et formål kan innsnevre en rettighet, aldri opprette, utvide eller arve en; exact match; purpose://prompt.unknown feiler lukket.

**6 — lesson.scaffold-without-porthole-host-has-no-preview**

Symptom: G1-GUI måtte bruke mockups rendret fra skeleton-JSON; ekte Porthole-preview var umulig.

Forebygging: For scaffolds uten Porthole-vert: (1) images/README.md må si eksplisitt at bildene er mockups og hva skeleton ikke kan rendre, (2) paritet (test.gui.parity) planlegges som egen slice med kjørende scaffold + Binding/Porthole via bridge, ikke som del av implementeringsjobben.

**7 — lesson.queue-job-file-before-prompt**

Symptom: Køjobben `formaalskomposisjon-fullfor-commit-20260910-1020` ble avvist med «mangler promptfil» 13 sekunder etter at `.job` ble skrevet; promptfilen kom to sekunder etter avvisningen og ligger foreldreløs i `_losen-queue/inbox/`, der runneren aldri ser den igjen.

Forebygging: Skriv `<id>.prompt.md` først og `<id>.job` sist, helst som `mv` fra en tmp-fil i samme mappe — `.job` er registreringssignalet, slik `job.json` er det i HavenAgentD::Docs/AgentJobs.md. Kan bli derivedTest: runneren eller `hd validate` rapporterer enhver `inbox/*.prompt.md` uten tilhørende `.job`, eldre enn to minutter, som foreldreløs.

**8 — lesson.cellscaffold-two-holes**

Symptom: CellScaffold har tomme booking-/concierge-stubber og autorisasjon som kaster nøkkelstien og bare sjekker eierskap.

Forebygging: Ikke porter celler fra CellScaffold til PalazzoScaffold uten å lukke begge hullene; test.cell.auth-negative og test.cell.stub-scan må være grønne.

**9 — lesson.bridge-inferred-architecture-from-one-use**

Symptom: En kodeassistent sluttet fra én observert bruksmåte av bridge til en egenskap ved arkitekturen og konkluderte feil.

Forebygging: Erklær hver kapabilitet oppgaven bygger på som eget formål med kilde og Avgrensning (pkg.std.cell-combination).

**10 — lesson.tested-a-different-path-than-production**

Symptom: Rot-probene leste relations.state.* gjennom porthole.get og var gronne, mens rendereren aldri fikk de samme dataene.

Forebygging: Naar en test skal si noe om hva brukeren ser, maa den bruke produksjonens egen kodevei - helst produksjonens egen funksjon med produksjonens egne inndata (SkeletonReachabilityAudit kaller condition.evaluate(root: nil, ...) nettopp derfor).

**11 — lesson.corr-approval-surfaces-timed-out**

Symptom: Corr-godkjenningen (Vegar) er utestet fordi flater/godkjenninger timet ut før testing rakk å skje.

Forebygging: FORMAALSSPEC.md §2 lister avhengigheter som egne formål med verifier; pkg.std.everything-works og gui.surface-loads-in-time må være grønne før den egentlige testen kjøres.

Kjente testrefs (eksistens i snapshot er ikke bevis for at testen er kjørt): `test.build`, `test.cell.auth-negative`, `test.cell.contract-fixtures`, `test.cell.stub-scan`, `test.cells.capability-audit`, `test.cells.dataflow-matches-contracts`, `test.docs-updated`, `test.gui.load-time`, `test.gui.parity`, `test.gui.reference-image-exists`, `test.handoff.dry-run`, `test.regression`, `test.roles.agent`, `test.roles.calibration`, `test.roles.cross-privacy`, `test.roles.no-unevaluated-success`, `test.roles.null-principal`, `test.roles.production-path`, `test.roles.reachable`, `test.roles.report`, `test.roles.schema`, `test.roles.unclassified-fails`, `test.skeleton.no-unreachable-elements`, `test.skeleton.purpose-actions-reachable`, `test.status-current`

</details>

## PDD_palazzo-sicilia-artikler_2026-09-07

**Simulert perspektiv:** Artikler som bygger formål og interesser; Artikler publiseres med godkjente tagger; Reaksjon blir post i gjestens entitet. **Skop:** simulated-scope://palazzo.
Oppgave: `CellProtocolDocuments/Deliverables/PDD_palazzo-sicilia-artikler_2026-09-07/FORMAALSSPEC.md` (§0/§1).

| Rang | Kandidat 6 | Kandidat 1 — TF-IDF |
|---:|---|---|
| 1 | **1** `lesson.entityanchor-keypaths-are-registered` — Skriv aldri testdata til en oppdiktet keypath på en celle. Finn en keypath cellen faktisk registrerer, helst en annen test som allerede bruk… | **2** `lesson.cellscaffold-two-holes` — Ikke porter celler fra CellScaffold til PalazzoScaffold uten å lukke begge hullene; og må være grønne. |
| 2 | **2** `lesson.cellscaffold-two-holes` — Ikke porter celler fra CellScaffold til PalazzoScaffold uten å lukke begge hullene; og må være grønne. | **1** `lesson.entityanchor-keypaths-are-registered` — Skriv aldri testdata til en oppdiktet keypath på en celle. Finn en keypath cellen faktisk registrerer, helst en annen test som allerede bruk… |
| 3 | **3** `lesson.scaffold-without-porthole-host-has-no-preview` — For scaffolds uten Porthole-vert: (1) images/README.md må si eksplisitt at bildene er mockups og hva skeleton ikke kan rendre, (2) paritet (… | **4** `lesson.bridge-inferred-architecture-from-one-use` — Erklær hver kapabilitet oppgaven bygger på som eget formål med kilde og Avgrensning (pkg.std.cell-combination). |
| 4 | **4** `lesson.bridge-inferred-architecture-from-one-use` — Erklær hver kapabilitet oppgaven bygger på som eget formål med kilde og Avgrensning (pkg.std.cell-combination). | **3** `lesson.scaffold-without-porthole-host-has-no-preview` — For scaffolds uten Porthole-vert: (1) images/README.md må si eksplisitt at bildene er mockups og hva skeleton ikke kan rendre, (2) paritet (… |
| 5 | **5** `lesson.purpose-never-grants-rights` — Et formål kan innsnevre en rettighet, aldri opprette, utvide eller arve en; exact match; feiler lukket. | **5** `lesson.purpose-never-grants-rights` — Et formål kan innsnevre en rettighet, aldri opprette, utvide eller arve en; exact match; feiler lukket. |
| 6 | **6** `lesson.cellbase-decodingerror-shadows-swift` — I App-modulen: skriv Swift.DecodingError når du vil ha standardbibliotekets. Gjelder generelt for typenavn CellBase også definerer — sjekk m… | **6** `lesson.cellbase-decodingerror-shadows-swift` — I App-modulen: skriv Swift.DecodingError når du vil ha standardbibliotekets. Gjelder generelt for typenavn CellBase også definerer — sjekk m… |
| 7 | **7** `lesson.cellbase-internal-members-look-public` — Sjekk tilgangsnivå og faktisk returverdi før du bruker et CellBase-medlem fra App: grep -n "var <navn>" CellProtocol::Sources/CellBase/.... … | **7** `lesson.cellbase-internal-members-look-public` — Sjekk tilgangsnivå og faktisk returverdi før du bruker et CellBase-medlem fra App: grep -n "var <navn>" CellProtocol::Sources/CellBase/.... … |
| 8 | **8** `lesson.unresolvable-condition-is-invisible` — SkeletonReachabilityAudit kjores over hver flate; feiler med elementene som aldri kan sees og handlingene som gaar tapt med dem. Betingelser… | **11** `lesson.codex-workspace-write-cannot-build-cellscaffold` — Lange bygg og testkjøringer legges ikke som workspace-write-køjobb. De kjøres som detached skript startet via Codex med danger-full-access o… |
| 9 | **9** `lesson.test-the-representation-not-the-issuance-flow` — Skille to spørsmål: «hvordan får noen rollen» og «hva gir rollen». Tester du det andre, installer rollen på husets etablerte måte og test vi… | **12** `lesson.baseline-measured-another-pdds-branch` — WP0 måler en ren eksport av den revisjonen arbeidet skal gå ut fra (git archive <rev> \| tar -x -C <scratch>), ikke det delte arbeidstreet. … |
| 10 | **10** `lesson.decomposition-is-classification` — Dekomponering velger fra Book 23 + pakker først; nye noder merkes 'candidate' og navngis av Claude, aldri implisitt av en modell. | **9** `lesson.test-the-representation-not-the-issuance-flow` — Skille to spørsmål: «hvordan får noen rollen» og «hva gir rollen». Tester du det andre, installer rollen på husets etablerte måte og test vi… |

Union: 12 lærdommer; øvrige 32 uvurderte.
- Relevans: 
- Gjentakelser: 
- Håndhevelse / sann grunn: 
- Sekunder: 

<details><summary>Full tekst og testreferanser</summary>

**1 — lesson.entityanchor-keypaths-are-registered**

Symptom: WP2-testen skrev en sentinel til `profile` på abonnentens EntityAnchor og fikk `notFound` ved gjenlesing. Skrivingen ga ingen feil.

Forebygging: Skriv aldri testdata til en oppdiktet keypath på en celle. Finn en keypath cellen faktisk registrerer, helst en annen test som allerede bruker den. At et `set` går gjennom er ikke bevis på at keypathen finnes.

**2 — lesson.cellscaffold-two-holes**

Symptom: CellScaffold har tomme booking-/concierge-stubber og autorisasjon som kaster nøkkelstien og bare sjekker eierskap.

Forebygging: Ikke porter celler fra CellScaffold til PalazzoScaffold uten å lukke begge hullene; test.cell.auth-negative og test.cell.stub-scan må være grønne.

**3 — lesson.scaffold-without-porthole-host-has-no-preview**

Symptom: G1-GUI måtte bruke mockups rendret fra skeleton-JSON; ekte Porthole-preview var umulig.

Forebygging: For scaffolds uten Porthole-vert: (1) images/README.md må si eksplisitt at bildene er mockups og hva skeleton ikke kan rendre, (2) paritet (test.gui.parity) planlegges som egen slice med kjørende scaffold + Binding/Porthole via bridge, ikke som del av implementeringsjobben.

**4 — lesson.bridge-inferred-architecture-from-one-use**

Symptom: En kodeassistent sluttet fra én observert bruksmåte av bridge til en egenskap ved arkitekturen og konkluderte feil.

Forebygging: Erklær hver kapabilitet oppgaven bygger på som eget formål med kilde og Avgrensning (pkg.std.cell-combination).

**5 — lesson.purpose-never-grants-rights**

Symptom: Risiko for at formålsmatch tolkes som tilgang.

Forebygging: Et formål kan innsnevre en rettighet, aldri opprette, utvide eller arve en; exact match; purpose://prompt.unknown feiler lukket.

**6 — lesson.cellbase-decodingerror-shadows-swift**

Symptom: WP1s nye celle ga 50 kompileringsfeil: `type 'DecodingError' has no member 'dataCorruptedError'` og `cannot infer contextual base in reference to member 'registry'`, alle fra én linje.

Forebygging: I App-modulen: skriv `Swift.DecodingError` når du vil ha standardbibliotekets. Gjelder generelt for typenavn CellBase også definerer — sjekk med `grep -rn "enum <Navn>" CellProtocol::Sources/CellBase` før du antar at et kjent Foundation-navn er Foundations.

**7 — lesson.cellbase-internal-members-look-public**

Symptom: WP2 stoppet på `'fullPermissionString' is inaccessible due to 'internal' protection level`. Medlemmet finnes og brukes i CellBase selv, så det så ut som et gyldig API.

Forebygging: Sjekk tilgangsnivå og faktisk returverdi før du bruker et CellBase-medlem fra App: `grep -n "var <navn>" CellProtocol::Sources/CellBase/...`. Et medlem som brukes internt i CellBase er ikke automatisk en del av API-et, og navnelikhet betyr ikke verdilikhet.

**8 — lesson.unresolvable-condition-is-invisible**

Symptom: Relasjoner-flaten viste tittel og ingen vei inn: ingen filopplasting, ingen knapper. Alle tester gronne.

Forebygging: SkeletonReachabilityAudit kjores over hver flate; test.skeleton.no-unreachable-elements feiler med elementene som aldri kan sees og handlingene som gaar tapt med dem. Betingelser hoerer hjemme inne i List/Grid/Reference-rader, der radens verdi sendes videre; ellers skal cellen avgjore og innhold bindes.

**9 — lesson.test-the-representation-not-the-issuance-flow**

Symptom: Alle fire WP4-rolletestene feilet i oppsettet, ikke i det de skulle teste: `deniedNoGrant` på `requestEntry` mot `cell:///AdminEntry`. Testen fikk aldri gitt identiteten rollen.

Forebygging: Skille to spørsmål: «hvordan får noen rollen» og «hva gir rollen». Tester du det andre, installer rollen på husets etablerte måte og test virkningen. Let alltid etter en eksisterende `*TestSupport`-hjelper før du bygger oppsettet selv — `grep -rn "TestSupport" CellScaffold::Tests` — og se hvilke argumenter de andre testene gir den.

**10 — lesson.decomposition-is-classification**

Symptom: Modeller som genererte purpose://-refs fritt hallusinerte referanser.

Forebygging: Dekomponering velger fra Book 23 + pakker først; nye noder merkes 'candidate' og navngis av Claude, aldri implisitt av en modell.

**11 — lesson.codex-workspace-write-cannot-build-cellscaffold**

Symptom: WP0-baselinen i køen ble blocked: `sandbox-exec: sandbox_apply: Operation not permitted`. Testkommandoen brukte 1 604 sekunder uten at én eneste test startet.

Forebygging: Lange bygg og testkjøringer legges ikke som `workspace-write`-køjobb. De kjøres som detached skript startet via Codex med `danger-full-access` og python Popen(start_new_session=True), med logg i en montert mappe som Cowork kan polle — samme mønster som produserte den notariserte HavenAgentD-pakken 2026-09-08. Køjobber brukes til analyse, kontrakter, dokumentasjon og korte kommandoer.

**12 — lesson.baseline-measured-another-pdds-branch**

Symptom: WP0 målte `pdd/tillitspakke-agentflaate` med 181 skitne oppføringer, ikke et rent utgangspunkt for sin egen PDD. En regresjonsbaseline derfra sier ingenting om hva denne PDD-en endrer.

Forebygging: WP0 måler en ren eksport av den revisjonen arbeidet skal gå ut fra (`git archive <rev> | tar -x -C <scratch>`), ikke det delte arbeidstreet. Er arbeidstreet opptatt av en annen PDD, er det en planopplysning som hører i STATUS, ikke noe implementeringen skal jobbe rundt.

Kjente testrefs (eksistens i snapshot er ikke bevis for at testen er kjørt): `test.build`, `test.cell.auth-negative`, `test.cell.contract-fixtures`, `test.cell.stub-scan`, `test.cells.capability-audit`, `test.cells.dataflow-matches-contracts`, `test.docs-updated`, `test.gui.load-time`, `test.gui.parity`, `test.gui.reference-image-exists`, `test.handoff.dry-run`, `test.regression`, `test.sicilia.articles`, `test.sicilia.e2e`, `test.sicilia.no-tracking`, `test.sicilia.persist`, `test.sicilia.query`, `test.sicilia.reaction`, `test.sicilia.signal`, `test.skeleton.no-unreachable-elements`, `test.skeleton.purpose-actions-reachable`, `test.status-current`

</details>

## PDD_skeleton-render-paritet_2026-09-07

**Simulert perspektiv:** Eieren ser samme flate uansett klient; Veiene inn finnes; Elementene virker, ikke bare vises. **Skop:** simulated-scope://gui.
Oppgave: `CellProtocolDocuments/Deliverables/PDD_skeleton-render-paritet_2026-09-07/FORMAALSSPEC.md` (§0/§1).

| Rang | Kandidat 6 | Kandidat 1 — TF-IDF |
|---:|---|---|
| 1 | **1** `lesson.unresolvable-condition-is-invisible` — SkeletonReachabilityAudit kjores over hver flate; feiler med elementene som aldri kan sees og handlingene som gaar tapt med dem. Betingelser… | **9** `lesson.test-corpus-is-not-shipped-corpus` — Enhver flate-test skal bygge korpuset fra det som faktisk sendes ut (menykonfigurasjoner + navigasjonsdestinasjoner + verifiseringshjelperen… |
| 2 | **2** `lesson.scaffold-without-porthole-host-has-no-preview` — For scaffolds uten Porthole-vert: (1) images/README.md må si eksplisitt at bildene er mockups og hva skeleton ikke kan rendre, (2) paritet (… | **1** `lesson.unresolvable-condition-is-invisible` — SkeletonReachabilityAudit kjores over hver flate; feiler med elementene som aldri kan sees og handlingene som gaar tapt med dem. Betingelser… |
| 3 | **3** `lesson.findability-is-not-usability` — En formaalssjekk maa navngi handlingene eieren skal kunne utfore, og testes mot SkeletonReachabilityAudit.reachableActionKeypaths - ikke mot… | **2** `lesson.scaffold-without-porthole-host-has-no-preview` — For scaffolds uten Porthole-vert: (1) images/README.md må si eksplisitt at bildene er mockups og hva skeleton ikke kan rendre, (2) paritet (… |
| 4 | **4** `lesson.parity-was-correctness-not-decoration` — Akseptanse sammenligner både bilde og oppførsel (knapper trigger keypaths, felt tar input) — begge i ACCEPT.md. | **5** `lesson.tested-a-different-path-than-production` — Naar en test skal si noe om hva brukeren ser, maa den bruke produksjonens egen kodevei - helst produksjonens egen funksjon med produksjonens… |
| 5 | **5** `lesson.tested-a-different-path-than-production` — Naar en test skal si noe om hva brukeren ser, maa den bruke produksjonens egen kodevei - helst produksjonens egen funksjon med produksjonens… | **8** `lesson.corr-approval-surfaces-timed-out` — FORMAALSSPEC.md §2 lister avhengigheter som egne formål med verifier; pkg.std.everything-works og gui.surface-loads-in-time må være grønne f… |
| 6 | **6** `lesson.text-ux-is-not-design` — Rendret bilde (Porthole-preview eller mockup) godkjennes før implementering; bildet er akseptansereferanse. | **3** `lesson.findability-is-not-usability` — En formaalssjekk maa navngi handlingene eieren skal kunne utfore, og testes mot SkeletonReachabilityAudit.reachableActionKeypaths - ikke mot… |
| 7 | **7** `lesson.empty-list-must-not-look-like-calm` — Modeller fravær eksplisitt: én rad per kjent kilde, alltid med, med tilstand read / unreadable / not-configured, og en påkrevd grunn når den… | **11** `lesson.bridge-inferred-architecture-from-one-use` — Erklær hver kapabilitet oppgaven bygger på som eget formål med kilde og Avgrensning (pkg.std.cell-combination). |
| 8 | **8** `lesson.corr-approval-surfaces-timed-out` — FORMAALSSPEC.md §2 lister avhengigheter som egne formål med verifier; pkg.std.everything-works og gui.surface-loads-in-time må være grønne f… | **12** `lesson.local-main-is-not-main` — Før du måler en baseline eller sier at main er rød: git fetch origin main og sammenlign. Er lokal main foran origin/main, er de commitene ik… |
| 9 | **9** `lesson.test-corpus-is-not-shipped-corpus` — Enhver flate-test skal bygge korpuset fra det som faktisk sendes ut (menykonfigurasjoner + navigasjonsdestinasjoner + verifiseringshjelperen… | **6** `lesson.text-ux-is-not-design` — Rendret bilde (Porthole-preview eller mockup) godkjennes før implementering; bildet er akseptansereferanse. |
| 10 | **10** `lesson.surface-load-alias-miss` — Mål lastetid tre ganger og sjekk logg for navnebom før en flate erklæres ferdig; aliaser må løses server-side eller ikke brukes. | **4** `lesson.parity-was-correctness-not-decoration` — Akseptanse sammenligner både bilde og oppførsel (knapper trigger keypaths, felt tar input) — begge i ACCEPT.md. |

Union: 12 lærdommer; øvrige 32 uvurderte.
- Relevans: 
- Gjentakelser: 
- Håndhevelse / sann grunn: 
- Sekunder: 

<details><summary>Full tekst og testreferanser</summary>

**1 — lesson.unresolvable-condition-is-invisible**

Symptom: Relasjoner-flaten viste tittel og ingen vei inn: ingen filopplasting, ingen knapper. Alle tester gronne.

Forebygging: SkeletonReachabilityAudit kjores over hver flate; test.skeleton.no-unreachable-elements feiler med elementene som aldri kan sees og handlingene som gaar tapt med dem. Betingelser hoerer hjemme inne i List/Grid/Reference-rader, der radens verdi sendes videre; ellers skal cellen avgjore og innhold bindes.

**2 — lesson.scaffold-without-porthole-host-has-no-preview**

Symptom: G1-GUI måtte bruke mockups rendret fra skeleton-JSON; ekte Porthole-preview var umulig.

Forebygging: For scaffolds uten Porthole-vert: (1) images/README.md må si eksplisitt at bildene er mockups og hva skeleton ikke kan rendre, (2) paritet (test.gui.parity) planlegges som egen slice med kjørende scaffold + Binding/Porthole via bridge, ikke som del av implementeringsjobben.

**3 — lesson.findability-is-not-usability**

Symptom: Flatene ble kalt validert fordi de bestod en beskrivelsesaudit; de var samtidig ubrukelige.

Forebygging: En formaalssjekk maa navngi handlingene eieren skal kunne utfore, og testes mot SkeletonReachabilityAudit.reachableActionKeypaths - ikke mot hvor godt formaalet er formulert.

**4 — lesson.parity-was-correctness-not-decoration**

Symptom: Parity-audit mellom Porthole og Binding viste at problemet ikke var manglende dekorasjon, men produktkorrekthet (feil oppførsel).

Forebygging: Akseptanse sammenligner både bilde og oppførsel (knapper trigger keypaths, felt tar input) — begge i ACCEPT.md.

**5 — lesson.tested-a-different-path-than-production**

Symptom: Rot-probene leste relations.state.* gjennom porthole.get og var gronne, mens rendereren aldri fikk de samme dataene.

Forebygging: Naar en test skal si noe om hva brukeren ser, maa den bruke produksjonens egen kodevei - helst produksjonens egen funksjon med produksjonens egne inndata (SkeletonReachabilityAudit kaller condition.evaluate(root: nil, ...) nettopp derfor).

**6 — lesson.text-ux-is-not-design**

Symptom: Kjetil forventet en helt annen flate enn den som ble vist; den tekstlige UX-beskrivelsen var godkjent, bildet var det ikke.

Forebygging: Rendret bilde (Porthole-preview eller mockup) godkjennes før implementering; bildet er akseptansereferanse.

**7 — lesson.empty-list-must-not-look-like-calm**

Symptom: En flate som samler «hva venter på meg» ser roligere ut jo mindre den får lest. En kilde som svarer 403, et token som er feil, en agent som ikke svarer — alle tre gir en tom liste, og en tom liste ser ut som at ingenting venter.

Forebygging: Modeller fravær eksplisitt: én rad per kjent kilde, alltid med, med tilstand `read` / `unreadable` / `not-configured`, og en påkrevd grunn når den ikke er lest. Skill erklært fravær (vi vet at den ikke er koblet til) fra ukjent fravær (vi fikk ikke spurt) — bare det første får se rolig ut. Ha én boolsk verdi i visningsmodellen (`claimsAllClear`) som er sann på nøyaktig ett sted, og en test som går over **alle** feilutfall og krever at den er falsk og at listen ikke er tom. Gi hvert feilutfall sin egen overskrift: «det virker ikke» hjelper ingen, «token avvist» og «ingen kontakt» krever hver sin handling.

**8 — lesson.corr-approval-surfaces-timed-out**

Symptom: Corr-godkjenningen (Vegar) er utestet fordi flater/godkjenninger timet ut før testing rakk å skje.

Forebygging: FORMAALSSPEC.md §2 lister avhengigheter som egne formål med verifier; pkg.std.everything-works og gui.surface-loads-in-time må være grønne før den egentlige testen kjøres.

**9 — lesson.test-corpus-is-not-shipped-corpus**

Symptom: Rot-probe-testen, lastetidstesten og finnbarhetsauditen var gronne i to uker mens Relasjoner-flaten var tom.

Forebygging: Enhver flate-test skal bygge korpuset fra det som faktisk sendes ut (menykonfigurasjoner + navigasjonsdestinasjoner + verifiseringshjelperen), dedupliseres, og feile hvis korpuset er mindre enn appens egen meny.

**10 — lesson.surface-load-alias-miss**

Symptom: Flatelasting tok 46 541 ms (klientens 45 s-timeout) ved bom, 5 000 ms ved treff; målingen 10.08 målte en mislykket lasting.

Forebygging: Mål lastetid tre ganger og sjekk logg for navnebom før en flate erklæres ferdig; aliaser må løses server-side eller ikke brukes.

**11 — lesson.bridge-inferred-architecture-from-one-use**

Symptom: En kodeassistent sluttet fra én observert bruksmåte av bridge til en egenskap ved arkitekturen og konkluderte feil.

Forebygging: Erklær hver kapabilitet oppgaven bygger på som eget formål med kilde og Avgrensning (pkg.std.cell-combination).

**12 — lesson.local-main-is-not-main**

Symptom: WP0-baselinen var rød og ble meldt som «main bygger ikke». Det var feil. Den commiten baselinen ble målt mot, `ba14895`, lå bare på den LOKALE main-grenen og var aldri pushet; den avhang av CellBase-kode som heller ikke var pushet. origin/main lå fire commits lenger fram, pinnet CellProtocol til en revisjon som ER på CellProtocol sin main, og hadde grønn CI hele tiden. Et helt døgns arbeid ble bygget oppå den lokale commiten.

Forebygging: Før du måler en baseline eller sier at main er rød: `git fetch origin main` og sammenlign. Er lokal main foran origin/main, er de commitene ikke main for andre — bygg aldri videre på dem. Se på CI for origin/main før du konkluderer. `swift package edit` skal aldri være på når noe måles eller meldes verifisert. Og den eneste sjekken som virkelig avgjør: klon fra GitHub til en tom katalog og bygg der. HavenAgentD::Scripts/preflight_before_landing.sh stiller alle fire spørsmålene.

Kjente testrefs (eksistens i snapshot er ikke bevis for at testen er kjørt): `test.build`, `test.cell.auth-negative`, `test.cell.contract-fixtures`, `test.cell.stub-scan`, `test.cells.capability-audit`, `test.cells.dataflow-matches-contracts`, `test.data.relevance`, `test.docs-updated`, `test.elements.execute`, `test.gui.load-time`, `test.gui.parity`, `test.gui.reference-image-exists`, `test.handoff.dry-run`, `test.parity.agreed-roles-cover-surfaces`, `test.parity.matrix-native`, `test.parity.real-corpus`, `test.parity.style-parity-knows-web-css`, `test.purpose.actions-exist`, `test.regression`, `test.skeleton.no-unreachable-elements`, `test.skeleton.purpose-actions-reachable`, `test.status-current`

</details>

## PDD_tillitspakke-agentflaate_2026-09-08

**Simulert perspektiv:** Brukeren ser, justerer og etterprøver agentflåtens myndighet; Pakken er en projeksjon av det som håndheves; Transitiv rekkevidde er synlig. **Skop:** simulated-scope://administrasjon.
Oppgave: `CellProtocolDocuments/Deliverables/PDD_tillitspakke-agentflaate_2026-09-08/FORMAALSSPEC.md` (§0/§1).

| Rang | Kandidat 6 | Kandidat 1 — TF-IDF |
|---:|---|---|
| 1 | **1** `lesson.entityanchor-keypaths-are-registered` — Skriv aldri testdata til en oppdiktet keypath på en celle. Finn en keypath cellen faktisk registrerer, helst en annen test som allerede bruk… | **2** `lesson.decomposition-is-classification` — Dekomponering velger fra Book 23 + pakker først; nye noder merkes 'candidate' og navngis av Claude, aldri implisitt av en modell. |
| 2 | **2** `lesson.decomposition-is-classification` — Dekomponering velger fra Book 23 + pakker først; nye noder merkes 'candidate' og navngis av Claude, aldri implisitt av en modell. | **1** `lesson.entityanchor-keypaths-are-registered` — Skriv aldri testdata til en oppdiktet keypath på en celle. Finn en keypath cellen faktisk registrerer, helst en annen test som allerede bruk… |
| 3 | **3** `lesson.purpose-never-grants-rights` — Et formål kan innsnevre en rettighet, aldri opprette, utvide eller arve en; exact match; feiler lukket. | **5** `lesson.new-cell-must-declare-its-provisioning-mode` — Enhver ny persistert celle i CellScaffold må eksplisitt svare på tre spørsmål før den registreres: (1) skal den opprettes i require-existing… |
| 4 | **4** `lesson.cellscaffold-two-holes` — Ikke porter celler fra CellScaffold til PalazzoScaffold uten å lukke begge hullene; og må være grønne. | **10** `lesson.branch-is-empty-after-eight-work-packages` — Skill «filene finnes» fra «branchen har dem». Sjekk git rev-parse <branch> mot git rev-parse <base> som del av hver verifikasjon som påstår … |
| 5 | **5** `lesson.new-cell-must-declare-its-provisioning-mode` — Enhver ny persistert celle i CellScaffold må eksplisitt svare på tre spørsmål før den registreres: (1) skal den opprettes i require-existing… | **11** `lesson.undocumented-plan-switch` — STATUS.md i oppgavemappen oppdateres ved hvert planbytte med dato og hvorfor; sjekkes i |
| 6 | **6** `lesson.cellbase-internal-members-look-public` — Sjekk tilgangsnivå og faktisk returverdi før du bruker et CellBase-medlem fra App: grep -n "var <navn>" CellProtocol::Sources/CellBase/.... … | **8** `lesson.syntax-check-reported-as-delivered` — En implementeringsslice er ikke levert før et detached bygg med danger-full-access er kjørt mot arbeidstreet og både bygg og de nye testene … |
| 7 | **7** `lesson.test-the-representation-not-the-issuance-flow` — Skille to spørsmål: «hvordan får noen rollen» og «hva gir rollen». Tester du det andre, installer rollen på husets etablerte måte og test vi… | **9** `lesson.cellbase-decodingerror-shadows-swift` — I App-modulen: skriv Swift.DecodingError når du vil ha standardbibliotekets. Gjelder generelt for typenavn CellBase også definerer — sjekk m… |
| 8 | **8** `lesson.syntax-check-reported-as-delivered` — En implementeringsslice er ikke levert før et detached bygg med danger-full-access er kjørt mot arbeidstreet og både bygg og de nye testene … | **12** `lesson.baseline-measured-another-pdds-branch` — WP0 måler en ren eksport av den revisjonen arbeidet skal gå ut fra (git archive <rev> \| tar -x -C <scratch>), ikke det delte arbeidstreet. … |
| 9 | **9** `lesson.cellbase-decodingerror-shadows-swift` — I App-modulen: skriv Swift.DecodingError når du vil ha standardbibliotekets. Gjelder generelt for typenavn CellBase også definerer — sjekk m… | **3** `lesson.purpose-never-grants-rights` — Et formål kan innsnevre en rettighet, aldri opprette, utvide eller arve en; exact match; feiler lukket. |
| 10 | **10** `lesson.branch-is-empty-after-eight-work-packages` — Skill «filene finnes» fra «branchen har dem». Sjekk git rev-parse <branch> mot git rev-parse <base> som del av hver verifikasjon som påstår … | **6** `lesson.cellbase-internal-members-look-public` — Sjekk tilgangsnivå og faktisk returverdi før du bruker et CellBase-medlem fra App: grep -n "var <navn>" CellProtocol::Sources/CellBase/.... … |

Union: 12 lærdommer; øvrige 32 uvurderte.
- Relevans: 
- Gjentakelser: 
- Håndhevelse / sann grunn: 
- Sekunder: 

<details><summary>Full tekst og testreferanser</summary>

**1 — lesson.entityanchor-keypaths-are-registered**

Symptom: WP2-testen skrev en sentinel til `profile` på abonnentens EntityAnchor og fikk `notFound` ved gjenlesing. Skrivingen ga ingen feil.

Forebygging: Skriv aldri testdata til en oppdiktet keypath på en celle. Finn en keypath cellen faktisk registrerer, helst en annen test som allerede bruker den. At et `set` går gjennom er ikke bevis på at keypathen finnes.

**2 — lesson.decomposition-is-classification**

Symptom: Modeller som genererte purpose://-refs fritt hallusinerte referanser.

Forebygging: Dekomponering velger fra Book 23 + pakker først; nye noder merkes 'candidate' og navngis av Claude, aldri implisitt av en modell.

**3 — lesson.purpose-never-grants-rights**

Symptom: Risiko for at formålsmatch tolkes som tilgang.

Forebygging: Et formål kan innsnevre en rettighet, aldri opprette, utvide eller arve en; exact match; purpose://prompt.unknown feiler lukket.

**4 — lesson.cellscaffold-two-holes**

Symptom: CellScaffold har tomme booking-/concierge-stubber og autorisasjon som kaster nøkkelstien og bare sjekker eierskap.

Forebygging: Ikke porter celler fra CellScaffold til PalazzoScaffold uten å lukke begge hullene; test.cell.auth-negative og test.cell.stub-scan må være grønne.

**5 — lesson.new-cell-must-declare-its-provisioning-mode**

Symptom: To nye celler i CellScaffold ga tre nye regresjoner: `OrchestratorPersistenceTests testRequireExistingModeRejectsFreshStorageWithoutCreatingBootstrapCells` (opprettet en celle i require-existing-modus mot fersk lagring) og to `TopUpCheckoutTests` som teller celler i provision-only-modus (5 mot forventet 4).

Forebygging: Enhver ny persistert celle i CellScaffold må eksplisitt svare på tre spørsmål før den registreres: (1) skal den opprettes i require-existing mot fersk lagring? Nei, med mindre den er kanonisk bootstrap. (2) Er den en av de kanoniske eager-bootstrap-cellene som provision-only skal lage? Nesten alltid nei — TopUpCheckoutTests teller dem eksplisitt. (3) Er den en Porthole-publisert flate? Bare da hører den i `reconcilePortholePublishedCellResolves`. Scaffold-intern tilstand registreres i egen funksjon, gated på policy OG provisionOnly, med gjenkjenning av eksisterende mapping.

**6 — lesson.cellbase-internal-members-look-public**

Symptom: WP2 stoppet på `'fullPermissionString' is inaccessible due to 'internal' protection level`. Medlemmet finnes og brukes i CellBase selv, så det så ut som et gyldig API.

Forebygging: Sjekk tilgangsnivå og faktisk returverdi før du bruker et CellBase-medlem fra App: `grep -n "var <navn>" CellProtocol::Sources/CellBase/...`. Et medlem som brukes internt i CellBase er ikke automatisk en del av API-et, og navnelikhet betyr ikke verdilikhet.

**7 — lesson.test-the-representation-not-the-issuance-flow**

Symptom: Alle fire WP4-rolletestene feilet i oppsettet, ikke i det de skulle teste: `deniedNoGrant` på `requestEntry` mot `cell:///AdminEntry`. Testen fikk aldri gitt identiteten rollen.

Forebygging: Skille to spørsmål: «hvordan får noen rollen» og «hva gir rollen». Tester du det andre, installer rollen på husets etablerte måte og test virkningen. Let alltid etter en eksisterende `*TestSupport`-hjelper før du bygger oppsettet selv — `grep -rn "TestSupport" CellScaffold::Tests` — og se hvilke argumenter de andre testene gir den.

**8 — lesson.syntax-check-reported-as-delivered**

Symptom: WP1 ble rapportert som «kode og 7 tester levert, syntakssjekken bestod». Et faktisk bygg ga 50 kompileringsfeil, og testene feilet 4 av 7 da de først kunne kjøre.

Forebygging: En implementeringsslice er ikke levert før et detached bygg med `danger-full-access` er kjørt mot arbeidstreet og både bygg og de nye testene er grønne. Legg byggejobben klar FØR slicen kjøres, og skriv i prompten at slicen skal rapportere «skrevet, ikke verifisert» — ikke «levert».

**9 — lesson.cellbase-decodingerror-shadows-swift**

Symptom: WP1s nye celle ga 50 kompileringsfeil: `type 'DecodingError' has no member 'dataCorruptedError'` og `cannot infer contextual base in reference to member 'registry'`, alle fra én linje.

Forebygging: I App-modulen: skriv `Swift.DecodingError` når du vil ha standardbibliotekets. Gjelder generelt for typenavn CellBase også definerer — sjekk med `grep -rn "enum <Navn>" CellProtocol::Sources/CellBase` før du antar at et kjent Foundation-navn er Foundations.

**10 — lesson.branch-is-empty-after-eight-work-packages**

Symptom: Åtte arbeidspakker rapportert utført og verifisert, ACCEPT.md skrevet — men `git branch -v` viste at `pdd/scaffold-admin-delegering` fortsatt pekte på samme commit som `main` (`e1f3e22f`). All koden lå ucommittet i et worktree som bare finnes på én maskin. Ett tapt worktree = 2 750 linjer kode og test borte, med full dokumentasjon på at arbeidet var «levert».

Forebygging: Skill «filene finnes» fra «branchen har dem». Sjekk `git rev-parse <branch>` mot `git rev-parse <base>` som del av hver verifikasjon som påstår at noe ligger på en branch; er de like, er branchen tom. Legg en commit-pakke inn i planen etter første grønne bygg, ikke etter siste arbeidspakke. Når worktreet bare kan leses fra macOS, kjør sjekken der — ikke hopp over den fordi verktøyet svarer feil.

**11 — lesson.undocumented-plan-switch**

Symptom: Tre produktive døgn (22.–24.08) så tomme ut i alle statusdokumenter fordi planbyttet fra bølge 1–3 til deploy-seremonien aldri ble skrevet ned.

Forebygging: STATUS.md i oppgavemappen oppdateres ved hvert planbytte med dato og hvorfor; sjekkes i test.status-current.

**12 — lesson.baseline-measured-another-pdds-branch**

Symptom: WP0 målte `pdd/tillitspakke-agentflaate` med 181 skitne oppføringer, ikke et rent utgangspunkt for sin egen PDD. En regresjonsbaseline derfra sier ingenting om hva denne PDD-en endrer.

Forebygging: WP0 måler en ren eksport av den revisjonen arbeidet skal gå ut fra (`git archive <rev> | tar -x -C <scratch>`), ikke det delte arbeidstreet. Er arbeidstreet opptatt av en annen PDD, er det en planopplysning som hører i STATUS, ikke noe implementeringen skal jobbe rundt.

Kjente testrefs (eksistens i snapshot er ikke bevis for at testen er kjørt): `test.build`, `test.cell.auth-negative`, `test.cell.contract-fixtures`, `test.cell.stub-scan`, `test.cells.capability-audit`, `test.cells.dataflow-matches-contracts`, `test.docs-updated`, `test.gui.load-time`, `test.gui.parity`, `test.gui.reference-image-exists`, `test.handoff.dry-run`, `test.regression`, `test.skeleton.no-unreachable-elements`, `test.skeleton.purpose-actions-reachable`, `test.status-current`, `test.tp.diff-viser-brudd`, `test.tp.e2e`, `test.tp.ingen-hemmeligheter`, `test.tp.injeksjon-endrer-ingenting`, `test.tp.justering-innsnevrer`, `test.tp.justering-kan-ikke-utvide`, `test.tp.pakke-uten-contract-nektes`, `test.tp.projeksjon-deterministisk`, `test.tp.provider-tools-off`, `test.tp.receipt-signatur`, `test.tp.rekkevidde-matcher-kontrakter`, `test.tp.start-uten-godkjent-digest-nektes`, `test.tp.webfetch-credential-negativ`, `test.tp.webfetch-monster-kanttilfeller`, `test.tp.webfetch-redirect-negativ`, `test.tp.webfetch-whitelist-negativ`

</details>

