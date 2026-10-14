# Stikonvensjon for HAVEN — 2026-09-09

**Forslag til håndheving: repo-ID + repo-relativ sti i versjonerte artefakter; én lokal JSON-fil erklærer maskinens plasseringer.** Oppslagsverktøyet, jobbformatet og migreringen nedenfor er forslag, ikke levert funksjonalitet. [vurdering]

Dette håndhever en eksisterende dokumentasjonsregel: `DEVELOPERS.md` sier allerede at lokale absolutte stier skal unngås og at Markdown skal bruke repo-relative stier. [belagt: CellProtocolDocuments::DEVELOPERS.md:31]

Kildeankre bruker `repo-ID::fil:linje`. `device.workspace::fil:linje` betegner undersøkte filer i den nåværende samlemappen, uten å gjøre denne mappen til et repo eller fastsette dens plassering. Det er en kildeadresse, ikke en streng som kan gis direkte til `cd`. Merkingen på et innledende avsnitt til en kodeblokk gjelder hele eksemplet; `[vurdering]` på en migreringsrad gjelder den foreslåtte endringen og verifiseringen. [vurdering]

## 1. Kontrollerte funn og mønster

| Funn | Grunnlag og konsekvens |
|---|---|
| Personlig rot og antatt VM-mount i worktree-verktøyet | `ROOT` er hardkodet; neste linje prøver én bestemt mappe under VM-brukerens hjemmekatalog. Repoet bygges senere som `ROOT/repo_rel`, og en kontroll avviser andre plasseringer. [belagt: device.workspace::_worktrees/agent-worktree.sh:23] [belagt: device.workspace::_worktrees/agent-worktree.sh:43] |
| Personlige installasjonsstier i køen | Både `PATH`, `ROOT` og `CODEX` inneholder maskinens personlige plasseringer. [belagt: device.workspace::_losen-queue/runner.sh:5] |
| Samlemappen er del av jobbkontrakten | Linje 1 og 3 i en jobb tolkes relativt til `ROOT`; tom arbeidskatalog blir samlemappen. Utdata sjekkes igjen ved å sette `ROOT` foran stien. Dette krever endring av både format, preflight og sluttkontroll. [belagt: device.workspace::_losen-queue/runner.sh:26] [belagt: device.workspace::_losen-queue/runner.sh:66] [vurdering] |
| Palazzo-planen har to plasseringavhengigheter | `cd PalazzoScaffold/Tests/Roles` forutsetter start i samlemappen; `--out ../../../CellProtocolDocuments/...` forutsetter søskenplassering. Begge må avledes fra hvert sitt repooppslag. [belagt: CellProtocolDocuments::Deliverables/PDD_palazzo-rollesimulering_2026-09-08/PLAN.md:34] [belagt: CellProtocolDocuments::Deliverables/PDD_palazzo-rollesimulering_2026-09-08/PLAN.md:40] [vurdering] |
| Skills instruerer eksplisitt om å tolerere personlige stier | Dokumentasjonsferdigheten kaller dem «local anchors» og følger opp med absolutte lesestier. Panel-ferdigheten bruker samtidig `CellProtocolDocuments/Book/...` og kaller dette repo-relativt fra CellProtocolDocuments. Dette blander to forskjellige startpunkter. [belagt: CellProtocolDocuments::.claude/skills/cellprotocol-docs-and-rag-maintenance/SKILL.md:42] [belagt: CellProtocolDocuments::.claude/skills/cellprotocol-docs-and-rag-maintenance/SKILL.md:48] [belagt: CellProtocolDocuments::.claude/skills/haven-panel-task-decomposition/SKILL.md:23] [belagt: CellProtocolDocuments::.claude/skills/haven-panel-task-decomposition/SKILL.md:36] [vurdering] |
| Mønsteret kopieres til arbeidspakker | Arbeidskø-planen bruker `HAVEN/HAVEN-Deploy`; Sicilia-handoff bruker `HAVEN/CellProtocol` og `HAVEN/CellScaffold`; agentflåtens promptmal erklærer HAVEN-roten som `cwd`. Det er derfor utilstrekkelig å rette bare Palazzo-kommandoen. [belagt: CellProtocolDocuments::Deliverables/PDD_arbeidsko-ai-utforere_2026-09-07/PLAN.md:3] [belagt: CellProtocolDocuments::Deliverables/PDD_palazzo-sicilia-artikler_2026-09-07/handoff/GUI.md:11] [belagt: CellProtocolDocuments::Deliverables/PDD_palazzo-sicilia-artikler_2026-09-07/handoff/GUI.md:25] [belagt: CellProtocolDocuments::Deliverables/PDD_tillitspakke-agentflaate_2026-09-08/handoff/prompts/wp01.prompt.md:1] [vurdering] |
| Plist og veiledning vil ellers gjeninnføre feilen | Køens plist hardkoder skript og logger; installeringskommandoen i `LES_MEG.md` fastsetter samlemappens plassering. [belagt: device.workspace::_losen-queue/org.digipomps.losen-queue.plist:9] [belagt: device.workspace::_losen-queue/org.digipomps.losen-queue.plist:13] [belagt: device.workspace::_losen-queue/LES_MEG.md:8] |
| Det finnes korrekt intern avledning | `purpose_dev.py` finner sin egen reporot fra skriptets plassering og bygger `Book/` og `Deliverables/` under den. Slik avledning av egen, fast reposstruktur trenger ikke et oppslag av andre repoer. [belagt: CellProtocolDocuments::Tools/PurposePackages/purpose_dev.py:28] [vurdering] |
| Problemet finnes også i kode uten personnavn | Palazzo velger miljøvariabel, deretter søskenrepo, deretter GitHub; CellScaffold har tilsvarende søskenavledning. Å fjerne bare personlige absolutte stier oppfyller derfor ikke regelen. [belagt: PalazzoScaffold::Package.swift:20] [belagt: PalazzoScaffold::Package.swift:30] [belagt: CellScaffold::Package.swift:32] [belagt: CellScaffold::Package.swift:61] [vurdering] |

Gjennomgangen omfatter de navngitte skriptene, deres veiledninger/plist, PDD-trærne under `CellProtocolDocuments::Deliverables/`, dokumentasjonsrepoets prompts og skills, repo-lagrede skills i CellScaffold, samt installerte Codex-/Claude-kopier som sammenligningsgrunnlag. Dette er en mønsteranalyse med konkret migreringsliste, ikke en påstand om at all kode, alle historiske worktrees og alle eksterne maskiner er fullstendig revidert. [vurdering]

Et rent søk etter `HAVEN/` er for upresist: ferdighetsbeskrivelsen «HAVEN/CellProtocol/Binding/Palazzo» navngir produkter, mens `HAVEN/CellProtocol/Sources/...` i en leseinstruks er en sti. Også relative Markdown-lenker til `../images/` innen samme repo kan være riktige. Klassifiser treff før endring. [belagt: CellProtocolDocuments::.claude/skills/haven-purpose-driven-dev/SKILL.md:3] [belagt: CellProtocolDocuments::Deliverables/PDD_palazzo-sicilia-artikler_2026-09-07/handoff/GUI.md:4] [belagt: CellProtocolDocuments::Deliverables/PDD_palazzo-sicilia-artikler_2026-09-07/handoff/GUI.md:11] [vurdering]

## 2. Den presise konvensjonen

**Repo-relativt betyr relativt til roten av ett navngitt repo, ikke relativt til samlemappen og ikke automatisk relativt til prosessens `cwd`.** Den portable adressen er paret `{repo, path}`, eksempelvis `{repo: "PalazzoScaffold", path: "Tests/Roles/"}`. I prosa skrives dette `PalazzoScaffold::Tests/Roles/`, eller «repo PalazzoScaffold, sti `Tests/Roles/`». [vurdering]

Repo-ID er en stabil logisk identifikator med fast skrivemåte, uavhengig av katalogens navn, plassering og valgt worktree. `HAVEN` betegner prosjektfellesskapet; det er ingen implisitt reporot. Et repo kan fysisk ligge som søsken, under en annen mappe eller alene. Det er device-konfigurasjonen som kobler ID til riktig utsjekk. [vurdering]

| Flate | Konvensjon og eksempel |
|---|---|
| Kode i eget repo | Bruk repo-relative ressurser med eksplisitt base, eller stier avledet fra modulens/skriptets faste plass i repoet. Et nakent `open("Book/x.json")` krever en dokumentert arbeidskatalog; ellers må basen følge koden. [vurdering] |
| Kode som bruker et annet repo | Slå opp repo-ID, og legg til den repo-relative stien: `root = resolve_repo("CellProtocolDocuments")`, deretter `root / "Book" / "book_catalog.json"`. Ingen antakelse om `../CellProtocolDocuments`. Funksjonsnavnet er foreslått API. [vurdering] |
| Skill og prompt | Oppgi repo-ID ved hver gruppe lesestier, samt hvordan oppslagsverktøyet brukes. En installert skill kan ikke anta at dens egen installasjonsmappe er et checkout. Eksempel: «Repo CellProtocolDocuments; les `Book/23_Purpose_Knowledge_Base.md`; avled roten med `haven-path repo CellProtocolDocuments`.» [vurdering] |
| PDD-dokument | Oppgi dokumentrepo, oppgavemappe relativt til dette repoet, utførelsesrepo og kommandoens arbeidskatalog. Et kortnavn som `P` må bindes eksplisitt, for eksempel `P = CellProtocolDocuments::Deliverables/PDD_palazzo-rollesimulering_2026-09-08/`. [vurdering] |
| Kø-jobb | Lagre repo-ID og repo-relativ sti separat for `cwd`, prompt, leserepoer og leveranse. Jobben skal ikke inneholde avsenderens ferdig utledede maskinstier. Utføreren gjør oppslaget på maskinen som faktisk kjører jobben. [vurdering] |
| Markdown-lenker | Vanlige dokumentrelative lenker er tillatt når målet ligger innen samme repo og lenkens base er Markdown-filen. Kryssrepo-referanser skrives som repo-ID + repo-relativ sti; en leser kan gjøre dem klikkbare etter lokalt oppslag. `repo::path` er referansenotasjon, ikke en eksisterende URI-handler. [vurdering] |
| Device-oppsett og genererte filer | Lokale konfigurasjoner, prosessargumenter og installert plist må kunne inneholde avledede absolutte stier. Versjoner en mal og generator, ikke den personlige konfigurasjonen eller den ferdig genererte installasjonen. [vurdering] |
| Chat | Chat inngår ikke i standarden for repo-lagrede artefakter. Innhold som kopieres inn i et repo, følger konvensjonen for mottakerartefaktet. [vurdering] |

Portable `path`-felt skal være relative, bruke `/`, og ikke inneholde `..`, hjemmekataloguttrykk, miljøvariabler eller absolutte prefikser. `.` er tillatt for repoets rot. Mellomrom i filnavn er tillatt; shellvariabler skal siteres, og programkall skal bruke separate argumenter. En symlink må ikke føre et slikt felt ut av det navngitte repoet. Dette gjelder filadresser, ikke eksempelvis `cell://`-adresser eller eksterne HTTPS-lenker. [vurdering]

Et faktisk submodule eller en vendoret mappe i et repo kan adresseres som en intern sti når man uttrykkelig mener den pinnede kopien. Den skal ikke erstattes av et annet lokalt checkout uten en egen beslutning om avhengigheten. Reglene om plassering endrer ikke revisjoner eller kildevalg. [vurdering]

## 3. Ett oppslag: lokal `repos.json`

### Vurderte alternativer

| Alternativ | Styrke | Avgjørelse |
|---|---|---|
| En lokal fil, normalt `~/.haven/repos.json` | Kan navngi alle repoer, uavhengige plasseringer, forventede markører og lokale infrastrukturmapper i ett inspeksjonsbart dokument. [vurdering] | **Velges.** Filen er eneste manuelt vedlikeholdte kilde til repo-plassering. [vurdering] |
| `HAVEN_ROOT` med overstyring per repo | Lett i et interaktivt shell, men hver prosess må få riktig miljø og riktig navnesett. Uavhengige overstyringer kan gjøre terminal, scheduler og agent uenige. [vurdering] | Velges ikke. Ingen egen fallback til `HAVEN_ROOT`, `PALAZZO_ROOT` eller tilsvarende. Miljøvariabler som et byggeverktøy krever, kan bare være avledede adapterverdier fra filen. [vurdering] |
| Søk oppover etter markørfil | Praktisk for å identifisere eget, allerede åpnet repo. Gir ikke alene plasseringen til et annet repo utenfor dette treet og gjør resultatet avhengig av startkatalogen. [vurdering] | Velges ikke som maskinens repooppslag. Markører brukes til å teste det erklærte målet, ikke til å lete etter alternativer. Fast intern avledning fra egen skriptfil er fortsatt tillatt. [vurdering] |

### Filformat og avledning

Eksemplet nedenfor er en **mal for en lokal device-fil**. Vinkelparentesene må fylles med reelle verdier før validering; de er ikke fungerende installasjonsstier. `commonRoot` er valgfri. `repos` er en eksplisitt liste, ikke «alle mapper som tilfeldigvis finnes under commonRoot». [vurdering]

```json
{
  "schema": "haven.repo-locations.v1",
  "commonRoot": "<absolutt sti til valgfri fellesmappe>",
  "repos": {
    "CellProtocolDocuments": {
      "path": "CellProtocolDocuments",
      "marker": {
        "path": "README-CellProtocol.md",
        "contains": "# CellProtocol Documentation Index"
      }
    },
    "CellProtocol": {
      "path": "CellProtocol",
      "marker": {
        "path": "Package.swift",
        "contains": "name: \"CellProtocol\""
      }
    },
    "PalazzoScaffold": {
      "path": "<absolutt sti til PalazzoScaffold utenfor fellesmappen>",
      "marker": {
        "path": "Package.swift",
        "contains": "name: \"PalazzoScaffold\""
      }
    }
  },
  "locations": {
    "queue": "_losen-queue",
    "worktrees": "_worktrees"
  },
  "tools": {
    "codex": "~/.local/bin/codex"
  }
}
```

De tre markørverdiene over er hentet fra filene som faktisk finnes i de undersøkte kildetrærne. Slik unngår første migrering å kreve nye markørfiler i alle repoer. [belagt: CellProtocolDocuments::README-CellProtocol.md:1] [belagt: CellProtocol::Package.swift:10] [belagt: PalazzoScaffold::Package.swift:42]

Avledningskontrakten er følgende; dette er hele prioriteringsregelen, uten søk eller stille fallback. [vurdering]

1. Les én fil: eksplisitt `--config FIL` når kjøreverten har valgt den, ellers `$HOME/.haven/repos.json`. `--config` velger bare hvilken fil som leses; det er ikke en alternativ deklarasjon av repo-plasseringer. Avvis ukjent skjemaversjon, dupliserte nøkler, ugyldige typer og tom `repos`. [vurdering]
2. Slå opp eksakt repo-ID. Mangler den, returner `repo_not_declared` med den etterspurte ID-en. Ikke gjett fra katalognavn, Git-remotes eller `cwd`. [vurdering]
3. En absolutt `repos[ID].path` brukes direkte. `~/...` utvides bare med den kjørende brukerens hjemmekatalog. En relativ verdi legges under eksplisitt `commonRoot`; manglende `commonRoot` er feil for akkurat dette repoet. `commonRoot` må selv være absolutt eller begynne med `~/`. Ingen `$VAR`-substitusjon, `eval`, `~annenbruker` eller `..` i relative plasseringsfelt. [vurdering]
4. Normaliser den valgte roten ved å følge symlinker og sjekk at den er en tilgjengelig katalog. At en eksplisitt valgt rot ligger utenfor fellesmappen, er tillatt; en symlink til slik plassering testes som den faktisk løste roten. [vurdering]
5. `marker.path` er relativ til denne roten. Kontroller at den normaliserte markørstien fortsatt ligger i repoet, at filen kan leses, og at den inneholder den ikke-tomme `marker.contains`-verdien. Markøren er en enkel identitetssjekk, ikke et bevis på korrekt branch, revisjon eller ubesudlet kildekode. [vurdering]
6. `locations` avledes etter samme plasseringsregel, men er eksplisitt lokale driftsmapper, ikke repoer. `tools` inneholder absolutte eller `~/`-baserte programstier som skal finnes og være kjørbare. Ingen plassering er i seg selv en skrivetillatelse. [vurdering]

Foreslått CLI er `haven-path repo ID`, `haven-path file ID RELATIV_STI`, `haven-path location NAVN`, `haven-path tool NAVN` og `haven-path check --all`. `file` kontrollerer repoet og at målet holder seg i det; selve målfilen kan være en ny leveranse. `repo`, `file`, `location` og `tool` skriver bare resultatstien til stdout ved suksess; feil og diagnose går til stderr med ikke-null exitkode. Ingen av disse kommandoene oppretter mapper. [vurdering]

Implementer CLI og validering som én liten Python-standardbibliotekpakke i `CellProtocolDocuments::Tools/RepoPaths/`. Installer en kjørbar kopi med nødvendige ressurser som `$HOME/.local/bin/haven-path`. Dette er en avtalt installasjonsadresse for verktøyet, ikke et nytt sted å erklære repoer. Første installasjon kjøres fra det eksplisitt valgte dokumentasjonscheckoutet; etterpå trenger verktøyet ikke finne sitt eget kilderepo for å slå opp andre. Python-tilgjengelighet skal sjekkes under installasjon. [vurdering]

Bruk normaliserte filsystemstier og komponentbasert kontroll av tilhørighet; ikke strengprefikser som kan godta en katalog med samme navnebegynnelse. Bruk `stat()` og faktisk lesing av markøren til å skille manglende fil fra manglende tilgang; `exists()` alene er utilstrekkelig for den feildiagnosen. Utformingen bygger på operasjonene i den offisielle [pathlib-dokumentasjonen](https://docs.python.org/3/library/pathlib.html#pathlib.Path.stat). [vurdering]

### Kjøreflater og worktrees

| Flate | Oppsett og verifisering |
|---|---|
| macOS-skall | Maskinens bruker fyller filen med sine plasseringer. Kjør CLI fra minst to ulike arbeidskataloger og få samme reporesultater. Bruk den avtalte CLI-installasjonsadressen i scheduler-skript; ikke stol på interaktiv shellprofil. [vurdering] |
| Codex-sandkasse | Den valgte filen og CLI må være lesbare/kjørbare, og erklærte leserepoer må være tilgjengelige. Start jobben med avledet `cwd` i leveranserepoet og med bare nødvendige, tillatte ekstra røtter. Hvis en administrert profil ikke gir nødvendig tilgang, rapporter repo-ID og `repo_inaccessible`/skriveblokkering; ikke bytt til en annen utsjekk. At skriverettigheter utenfor godkjente røtter er begrenset, er også dokumentert i den lokale kapabilitetsmatrisen. [vurdering] [belagt: CellScaffold::.claude/skills/haven-functional-service-verification/references/sandbox-capability-matrix.md:29] |
| Cowork-VM | VM-en er et eget filsystemmiljø og har sin egen device-fil. Oppsettet fyller `commonRoot` med den faktisk monterte `$HOME/mnt/<mappe>`-plasseringen, eller fyller individuelle repooppføringer. I JSON skrives en konkret absolutt verdi eller `~/mnt/<faktisk mappenavn>`; den bokstavelige teksten `$HOME` ekspanderes ikke. En Mac-sti skal ikke oversettes ved tekstutskifting. [vurdering] |
| Jobb fra Cowork til Mac | Avsender sender `{repo, path}`. Mac-runneren bruker Mac-filens oppslag. VM-ens plasseringer overføres ikke som Mac-arbeidskatalog. [vurdering] |
| CI | Checkout-steget bestemmer kjøringens faktiske kataloger og skriver samme JSON-format til en midlertidig fil. Alle oppslag får eksplisitt `--config` til denne filen. En generert CI-fil er device-oppsett for den kjøringen, ikke en ny oppslagsalgoritme; erklær bare repoer som sjekkes ut for jobben, og feile hvis et påkrevd repo mangler. GitHub Actions gir et eksplisitt checkout-`path` som kan brukes av generatoren, se [actions/checkout](https://github.com/actions/checkout#checkout-multiple-repos-side-by-side). [vurdering] |
| Aktiv worktree | Skriptet finner basisrepo via filen, men arbeidsoppgaven må deretter bruke sin valgte worktree konsekvent for lesing og skriving. Runneren lager en lokal, avledet konfigurasjon for kjøringen med samme skjema og den valgte worktree-roten for repo-ID-en; den endrer ikke maskinens basisfil. Alle CLI-kall i denne kjøringen får samme `--config`, også i agentens genererte kjørekontekst. Jobbprompten kan ikke selv velge en vilkårlig config-fil. [vurdering] |

En avledet kjøringsfil er et låst bilde av device-innstillingen med runnerens eksplisitte worktree-tildeling, ikke en konkurrerende manuelt vedlikeholdt oversikt. Ta bildet én gang før preflight, behold det gjennom jobben, og noter konfigurasjonsdigest i den lokale kvitteringen. En endring i brukerens basisfil skal ikke sende halvparten av en jobb til et annet checkout. [vurdering]

Den nåværende worktree-veiledningen sier at skriptets absolutte stdout kan legges direkte i jobbens første linje, mens runneren alltid setter `ROOT` foran denne linjen. Denne kombinasjonen er inkonsistent og må dekkes i migreringstesten. [belagt: device.workspace::_worktrees/README.md:46] [belagt: device.workspace::_worktrees/agent-worktree.sh:12] [belagt: device.workspace::_losen-queue/runner.sh:33] [vurdering]

Repooppslaget reparerer ikke Git-worktree-metadata mellom Mac- og VM-stier. Verifiser Git-operasjoner på verten der worktree-et er opprettet; ikke utled at lesbare kildefiler betyr at samme worktree kan administreres fra begge flater. Dette skillet støttes av [Git-dokumentasjonen om worktree-detaljer](https://git-scm.com/docs/git-worktree#_details) og den eksisterende lokale advarselen om mount-stier. [vurdering] [belagt: device.workspace::.agent-tools/README.md:116]

Fungerende oppslag i en virkelig Cowork-VM og en virkelig CI-jobb er ikke verifisert i denne leveransen. Det er også uavklart hvilke ekstra skriverøtter hver fremtidig administrert agentprofil vil tillate. Disse punktene må passere miljøtestene før migreringen kan kalles driftsklar. [usikker]

## 4. Formålet og den avledede testen

Book 23 krever observerbare mål; kunnskapsbasens `goal` har feltene `outcome`, `successSignals` og `verifier`. `purpose://digital-work.coordinate` finnes allerede. Blokken under bruker denne eksisterende overordnede referansen og definerer et lokalt mål for oppslaget; den registrerer ingen ny kanonisk purpose-node. [belagt: CellProtocolDocuments::Book/23_Purpose_Knowledge_Base.md:122] [belagt: CellProtocolDocuments::Book/haven_purpose_knowledge_base_v0.json:35] [belagt: CellProtocolDocuments::Book/haven_purpose_knowledge_base_v0.json:458] [vurdering]

Foreslått formålsbinding i Book 23-form: [vurdering]

```json
{
  "purposeRef": "purpose://digital-work.coordinate",
  "title": "Finn erklærte repoer uavhengig av lokal plassering",
  "goal": {
    "goalRef": "goal.repo-placement.resolvable",
    "lifecycle": "continuous",
    "outcome": "Hver kjøreflate finner riktig kildekatalog for hvert erklært repo fra sin device-innstilling, uten endring i repoets kode, skills eller prompts.",
    "successSignals": [
      "Hvert erklært repo gir en eksisterende og tilgjengelig katalog med forventet markør.",
      "Samme repo-ID og repo-relative filadresse virker etter flytting når bare device-filen endres.",
      "Et repo utenfor commonRoot virker på samme måte som et repo innenfor.",
      "Et oppslagsavvik navngir repoet og årsaken og gir ikke-null exitkode."
    ],
    "verifier": "haven-path check --all med kjøreflatens valgte JSON-fil, samt flytte- og negativtilfellene i testmatrisen nedenfor."
  }
}
```

**Minste test er akkurat: for hvert erklærte repo, avled roten og sjekk at katalogen og den forventede markøren finnes.** Innholdssjekken gir litt sterkere identifikasjon enn bare en generisk fil som `Package.swift`. Testen skal bruke produksjonsoppslaget, ikke en egen kopi av algoritmen som kan være uenig med runneren. Foreslått pseudokode: [vurdering]

```text
config = les_og_valider_valgt_device_fil()
feil = []
for repo_id in sortert(config.repos):
    try:
        root = resolve_repo(config, repo_id)
        krev_tilgjengelig_katalog(root)
        marker = normalisert_sti_innenfor(root, config.repos[repo_id].marker.path)
        krev_lesbar_fil(marker)
        krev_innhold(marker, config.repos[repo_id].marker.contains)
        skriv_resultat(repo_id, "PASS")
    except Oppslagsfeil as error:
        feil.append((repo_id, error.reason))
        skriv_resultat(repo_id, "FAIL", error.reason)
exit(1 if feil else 0)
```

Fortsett gjennom alle erklærte repoer etter en repo-spesifikk feil. Hele filens syntaks-/skjemafeil skal gi `config_invalid` og filidentifikasjon; oppgi berørt repo-ID når den lar seg lese, men ikke finn på et repo-navn ved uleselig JSON. En tom deklarasjon skal feile, ikke gi en meningsløs grønn test. En jobb som krever et repo som ikke er erklært, skal dessuten feile under preflight med akkurat denne ID-en. [vurdering]

Eksempler på feilformat, ikke resultater fra en kjøring: [vurdering]

```text
FAIL repo=PalazzoScaffold reason=common_root_missing
FAIL repo=CellProtocol reason=repo_missing
FAIL repo=Binding reason=repo_inaccessible
FAIL repo=CellProtocolDocuments reason=marker_mismatch marker=README-CellProtocol.md
FAIL repo=UniverseSimulation reason=repo_not_declared
```

Den lokale feilloggen kan i tillegg vise forsøkt absolutt sti og hvilken config som ble brukt. En rapport som lagres i et repo bruker repo-ID, relativ markørsti og årsak; den private maskinstien er ikke et gjenbrukbart instruksjonsfelt. [vurdering]

| Test | Forventning før neste migreringssteg |
|---|---|
| T1 — alle erklærte repoer | Hver oppføring gir eksisterende katalog og lesbar markør med forventet innhold; ingen utelatte oppføringer. [vurdering] |
| T2 — uavhengig plassering | Flytt et lite fixture-repo utenfor fellesmappen og oppdater bare JSON; samme `{repo, path}` virker. Gjenta uten `commonRoot`, med alle plasseringer eksplisitte. [vurdering] |
| T3 — feil repo og mangler | Feil mappe, manglende markør, feil markørinnhold, ukjent repo og manglende `commonRoot` gir hver sin navngitte feil og ikke-null exit. Ingen fallback til en annen kopi. [vurdering] |
| T4 — filsystemgrense | Mellomrom virker; `..`, absolutt relativfelt, symlink ut av repoet og utilgjengelig katalog avvises/rapporteres. Test også at `repo-extra` ikke godtas som barn av `repo`. [vurdering] |
| T5 — miljø | Kjør T1 fra macOS-skall, faktisk Codex-profil, faktisk Cowork-VM og CI med hver sin valgte fil. Simulerte VM-stier erstatter ikke den virkelige mount-testen. [vurdering] |
| T6 — worktree | Et midlertidig Git-repo med worktree bruker valgt utsjekk for både kilde, `cwd` og leveranse, mens basisconfig er uendret. En `.git`-fil må ikke forveksles med manglende Git-repo. [vurdering] |
| T7 — kø | En falsk utfører registrerer mottatt argv og `cwd`; sjekk riktig repo, quoting, leveransesti og tilgangspolicy uten et modellkall. Deretter én ekte, liten fil-leveranse i det nye formatet. [vurdering] |

De undersøkte markørfilene for CellProtocolDocuments, CellProtocol, PalazzoScaffold og HavenAgentD var lesbare og inneholdt forventede overskrifter/pakkenavn. Dette er et kildegrunnlag for markørvalget, ikke en bestått test av det foreslåtte `haven-path`. [belagt: CellProtocolDocuments::README-CellProtocol.md:1] [belagt: CellProtocol::Package.swift:10] [belagt: PalazzoScaffold::Package.swift:42] [belagt: HavenAgentD::Package.swift:5] [vurdering]

Leveransemålet her er dokumentasjon; driftsmålet over står **ikke verifisert** til oppslagsverktøyet er implementert og T1–T7 har relevante resultater. [vurdering]

## 5. Konkrete erstatninger

### Palazzo-kommandoen

I `PalazzoScaffold::Tests/Roles/` skal `run_roles.py` fortsatt kjøres med samme testparametre. Bytt bare avledning av arbeidskatalog og rapportmål i planen. Følgende viser de nye stidelene; `ALLE_EKSISTERENDE_TESTARGUMENTER` er en plassholder for de uendrede argumentene i dagens plan. Eksemplet bruker basisconfig; ved en tildelt worktree får hvert CLI-kall den samme eksplisitte `--config` for kjøringen. [belagt: CellProtocolDocuments::Deliverables/PDD_palazzo-rollesimulering_2026-09-08/PLAN.md:35] [vurdering]

```bash
hp="$HOME/.local/bin/haven-path"
roles_dir=$("$hp" file PalazzoScaffold Tests/Roles) || exit 1
report_dir=$("$hp" file CellProtocolDocuments \
  Deliverables/PDD_palazzo-rollesimulering_2026-09-08) || exit 1
cd "$roles_dir" || exit 1
python3 run_roles.py ALLE_EKSISTERENDE_TESTARGUMENTER \
  --out "$report_dir/RAPPORT_$(date +%F).md"
```

Planens innledning endres til «Repo PalazzoScaffold, testmappe `Tests/Roles/`. Rapport: repo CellProtocolDocuments, `Deliverables/PDD_palazzo-rollesimulering_2026-09-08/`.» Det er ikke nødvendig å starte Palazzo-serveren for å verifisere denne stirettingen: slå opp begge mapper og kontroller `Tests/Roles/run_roles.py`; funksjonell rolletesting er en annen verifikasjon. [vurdering]

### Køformat og driftsstier

Foreslå et versjonert JSON-format for nye `.job`-filer. Dette eksempeloppdraget skriver bare dokumentasjonsrepoet; øvrige repoer er lesekilder. `prompt` peker på en kildefil for en fremtidig gjenkjøring og påstår ikke at denne filen allerede finnes. Runneren kan ta en kopi til sin lokale spool før kjøring. [vurdering]

```json
{
  "schema": "haven.losen-job.v2",
  "id": "repo-path-convention",
  "cwd": {"repo": "CellProtocolDocuments", "path": "."},
  "prompt": {
    "repo": "CellProtocolDocuments",
    "path": "Prompts/Repo_Path_Audit.md"
  },
  "readRepos": ["CellProtocolDocuments", "CellProtocol", "CellScaffold", "PalazzoScaffold", "HavenAgentD"],
  "sandbox": "workspace-write",
  "output": {
    "repo": "CellProtocolDocuments",
    "path": "Deliverables/Repo_Path_Konvensjon_2026-09-09.md"
  },
  "completionMarker": "FERDIG-MARKØR"
}
```

Dette er et konkret formateksempel, ikke en ferdig jobb for hele denne revisjonen: lesing av de gamle skriptene utenfor repoene må i tillegg tillates som eksplisitt lokal infrastrukturscope i runnerens policy. Slike driftsressurser slås opp via `locations`; de skal ikke kamufleres som repoer eller gi generell tilgang til samlemappen. [vurdering]

For første versjon av den nye runneren skal `output.repo` være lik `cwd.repo`, og normalisert leveranse må ligge under normalisert `cwd`. `readRepos` angir behov, men gir ikke rettigheter alene. Jobber som skriver flere repoer, må splittes eller senere få et eget eksplisitt format med avgrensede skriverøtter. Å sette `cwd` til samlemappen skal ikke brukes som løsning. [vurdering]

Den eksisterende preflighten bruker strengbasert kontroll av leveranseforelder før `mkdir`, og sluttkontrollen bygger stien på nytt fra `ROOT`. Erstatt begge med én normalisert, validert leveransesti som beholdes gjennom kjøringen. Ved nye undermapper må nærmeste eksisterende forelder kontrolleres for symlinker før opprettelse og kontrolleres igjen før bruk. [belagt: device.workspace::_losen-queue/runner.sh:39] [belagt: device.workspace::_losen-queue/runner.sh:46] [belagt: device.workspace::_losen-queue/runner.sh:51] [belagt: device.workspace::_losen-queue/runner.sh:66] [vurdering]

I worktree-skriptet erstattes argumentet `repo-rel-path` av `repo-ID`, `ROOT/repo_rel` av `haven-path repo ID`, og `ROOT/_worktrees` av `haven-path location worktrees`. Fjern antakelsen om at basisrepoet ligger under samlemappen; behold Git-kontroll, låsing og kontroll av valgt utsjekk. Kontroller at en gjenbrukt målkatalog faktisk er et worktree av det valgte repoet, ikke bare at `.git` finnes. [belagt: device.workspace::_worktrees/agent-worktree.sh:16] [belagt: device.workspace::_worktrees/agent-worktree.sh:43] [belagt: device.workspace::_worktrees/agent-worktree.sh:56] [vurdering]

I runneren erstattes `ROOT`/`Q`-konstruksjonen av `haven-path location queue`, og `CODEX` av `haven-path tool codex`. Avtal nødvendig system-`PATH` ved installasjon; brukerens Codex-binær velges fra config, ikke fra en personlig streng i `PATH`. Config-/verktøyfeil før `Q` er kjent skal gå til stderr og den installerte scheduler-loggen, ikke til en uavledet `$Q`. [belagt: device.workspace::_losen-queue/runner.sh:5] [belagt: device.workspace::_losen-queue/runner.sh:9] [vurdering]

## 6. Migrering med stoppunkt mellom hvert steg

**Ingen av stegene i denne listen skal utføres som del av dokumentleveransen.** Hvert steg krever bestått verifisering før neste; live runner, dens jobbformat og en aktiv worktree skal ikke byttes under pågående arbeid. Køens intervall på 60 sekunder står i plist, og eksisterende worktree-veiledning sier allerede at runner-endring utsettes til køen er tom. [vurdering] [belagt: device.workspace::_losen-queue/org.digipomps.losen-queue.plist:11] [belagt: device.workspace::_worktrees/README.md:58]

| Rekkefølge | Filer og konkret endring | Verifisering før neste steg |
|---|---|---|
| M1 — kontrakt og implementasjon isolert | Opprett `CellProtocolDocuments::Tools/RepoPaths/repos.schema.json`, `haven_path.py`, `test_repo_paths.py`, `README.md` og `install.py`. Implementer §3–4 og en installerbar CLI uten nye repooppslagskilder. [vurdering] | T1–T4 på midlertidige fixtures, ugyldig JSON, dupliserte nøkler og CLI installert utenfor kilderepoet. Ingen endring i eksisterende skript. [vurdering] |
| M2 — device-oppsett | Opprett brukerens `~/.haven/repos.json`, eller vertens eksplisitt valgte fil, og installer CLI på hver nødvendig kjøreflate. Fyll alle repoer som migrerte forbrukere bruker, samt `locations.queue`, `locations.worktrees` og nødvendige `tools`. Ikke legg personlige verdier i Git. [vurdering] | T1 og T5; sjekk også at kømapper finnes og programmet er kjørbart. Manglende miljøtest blir et åpent stoppunkt, ikke en grønn antakelse. [vurdering] |
| M3 — dokumentasjonsregler og generator | Oppdater `CellProtocolDocuments::DEVELOPERS.md:31`, `Book/13_Agent_Instructions.md:102`, `Prompts/Purpose_Driven_Dev_Spec.md:3`, `Tools/PurposePackages/purpose_dev.py:249`, `Tools/PurposePackages/SKILL_haven-purpose-driven-dev.md` og `.claude/skills/haven-purpose-driven-dev/SKILL.md:19`. Innfør `{repo,path}`, navngi dokumentrepoet i leselistene og la ny PDD-mal skrive `Repo: CellProtocolDocuments; oppgavemappe: Deliverables/{dirname}/`. [vurdering] | Generer én PDD-fixture i midlertidig område. Kontroller at alle lesestier har repo/base, at interne lenker virker, og at ingen personlig sti eller samlemappen som `cwd` er generert. Behold den korrekte egenrepo-avledningen i `purpose_dev.py:28`. [vurdering] |
| M4 — skills og gjenbrukbare PDD-instrukser | Endre de konkrete filene i §7 til §2-format. Fjern «local anchors»-unntaket. Normaliser prosa og kjøreinstrukser; håndter historisk evidens etter §7. Installer/synkroniser deretter tilsvarende personlige skill-kopier og eventuelle pakker fra rettet kilde. [vurdering] | Slå opp refererte filer fra en annen mappe og med ett repo utenfor fellesmappen. Sammenlign installert skill med valgt kilde og åpne én fersk agentøkt. Ingen antakelse om at en allerede kjørende økt har lastet nye skills. [vurdering] |
| M5 — worktree-verktøy | Lag først en kandidatkopi av `device.workspace::_worktrees/agent-worktree.sh`, og korriger `device.workspace::_worktrees/README.md` etter §5. Gamle absolute-output-til-jobblinje-instrukser fjernes. [vurdering] | Kjør T6 i et lite, midlertidig Git-repo, inkludert repo utenfor fellesmappen, eksisterende branch/worktree og feil gjenbruksmål. `--dry-run` og `bash -n` er tillegg; de erstatter ikke worktree-testen. Bytt skript først etter at aktiv bruker er ferdig; ikke flytt eller reparer den aktive worktree-en som del av byttet. [vurdering] |
| M6 — køkandidat og installasjonsmal | Lag kandidat av `device.workspace::_losen-queue/runner.sh`, ny formatvalidering og en mal/generator for `org.digipomps.losen-queue.plist`. Korriger `LES_MEG.md` til repo-ID-format, avledet `cwd` og generert installasjon. Plist-generatoren fyller skript-, verktøy- og loggstier fra valgt config; den installerte plisten har konkrete absolutte verdier. [vurdering] | T7 mot separat testspool med falsk Codex-binær, så én liten ekte canary. Test ukjent repo, skriveavslag, markør allerede til stede, ikke-null utførerexit og manglende leveranse. Den gamle køen fortsetter uendret. [vurdering] |
| M7 — kontrollert købytte | Stans nye innleveringer, la `running` bli tom og avklar gamle `inbox`-jobber. Konverter bare ventende jobber til repo-ID-format mens ingen runner plukker dem opp; arkiver originalen. Installer den testede runneren og genererte plisten, og oppdater produsentene i §7 samtidig. [vurdering] | Dokumenter at ingen gammel prosess kjører før bytte. Start med én canary og kontroller argv/`cwd`, leveranse og ferdigmarkør før vanlig kø åpnes. Behold gammel versjon og plist for tilbakeføring; v2-jobber må holdes unna gammel runner ved tilbakeføring. Historiske `done/`-jobber omskrives ikke. [vurdering] |
| M8 — øvrige forbrukere og varig kontroll | Migrer de navngitte kode-/infrastrukturfunnene i §8 i egne verifiserbare endringer. Legg sti-lint for nye/endret operative instrukser i `CellProtocolDocuments::Tools/RepoPaths/check_path_convention.py` og kall den fra relevant CI. [vurdering] | Skann personlige hjemmestier, VM-mount-antakelser, kjørbare `HAVEN/...`-stier og kryssrepo-`../`. Test fra flyttet fixture-oppsett. Linten må skille interne lenker, eksterne URL-er og historiske kildeutdrag fra operative instrukser. [vurdering] |

## 7. Filinventar for M3–M4 og jobbprodusentene i M7

### Skills

Disse filene er konkrete første rettemål i dokumentasjonsrepoet og samlemappens skill-kilde. Erstatning: navngitt repo + repo-relativ lesesti + §3-oppslag; behold standard installasjonsadresser som installasjonskontrakt, ikke som repo-plassering. [vurdering]

| Fil/funn | Endring |
|---|---|
| `CellProtocolDocuments::.claude/skills/cellprotocol-docs-and-rag-maintenance/SKILL.md` [belagt: CellProtocolDocuments::.claude/skills/cellprotocol-docs-and-rag-maintenance/SKILL.md:42] | Fjern lokale-ankre-unntaket; leselisten blir `README-CellProtocol.md`, `Book/...`, `Tools/...`, `Gap_Analysis.md`, med `CellProtocolDocuments` som eksplisitt repo. [vurdering] |
| `CellProtocolDocuments::.claude/skills/haven-panel-task-decomposition/SKILL.md` [belagt: CellProtocolDocuments::.claude/skills/haven-panel-task-decomposition/SKILL.md:23] | Fjern det dupliserte repo-prefikset fra stifeltene og legg til oppslagskommandoen før leselisten. [vurdering] |
| `device.workspace::.agents/skills/cell-attachment-surface/SKILL.md` [belagt: device.workspace::.agents/skills/cell-attachment-surface/SKILL.md:23] [belagt: device.workspace::.agents/skills/cell-attachment-surface/SKILL.md:40] | Skill-kilden ligger her uten en deklarert repoeier. Avklar kildeeier ved migrering, erstatt personlige kildestier med navngitte repoer og synkroniser derfra. [vurdering] |

Følgende repo-lagrede CellScaffold-filer har personlige absolutte kilde-/arbeidsstier. **Hver rad er en fil som må gjennom samme konvertering**, inkludert `references/`-filer som en rettet hovedskill ellers ville sendt leseren videre til. Verifikasjonen er at hvert nytt `{repo,path}` peker på samme tilsiktede kildefil etter flytting, ikke bare at en tekststreng er fjernet. [vurdering]

| Fil under `CellScaffold::.claude/skills/` | Kildeanker |
|---|---|
| `binding-skeleton-parity-testing/SKILL.md` | [belagt: CellScaffold::.claude/skills/binding-skeleton-parity-testing/SKILL.md:16] |
| `binding-skeleton-parity-testing/references/parity-workflows.md` | [belagt: CellScaffold::.claude/skills/binding-skeleton-parity-testing/references/parity-workflows.md:6] |
| `cellconfiguration-skeleton-authoring/SKILL.md` | [belagt: CellScaffold::.claude/skills/cellconfiguration-skeleton-authoring/SKILL.md:59] |
| `cellprotocol-cell-authoring/SKILL.md` | [belagt: CellScaffold::.claude/skills/cellprotocol-cell-authoring/SKILL.md:46] |
| `cellprotocol-contract-testing/SKILL.md` | [belagt: CellScaffold::.claude/skills/cellprotocol-contract-testing/SKILL.md:28] |
| `cellprotocol-core-runtime-implementation/SKILL.md` | [belagt: CellScaffold::.claude/skills/cellprotocol-core-runtime-implementation/SKILL.md:29] |
| `cellprotocol-cross-language-porting/SKILL.md` | [belagt: CellScaffold::.claude/skills/cellprotocol-cross-language-porting/SKILL.md:37] |
| `cellprotocol-docs-and-rag-maintenance/SKILL.md` | [belagt: CellScaffold::.claude/skills/cellprotocol-docs-and-rag-maintenance/SKILL.md:42] |
| `cellprotocol-identity-capability-security/SKILL.md` | [belagt: CellScaffold::.claude/skills/cellprotocol-identity-capability-security/SKILL.md:28] |
| `cellprotocol-scaffold-integration/SKILL.md` | [belagt: CellScaffold::.claude/skills/cellprotocol-scaffold-integration/SKILL.md:27] |
| `cellprotocol-skeleton-renderer-porting/SKILL.md` | [belagt: CellScaffold::.claude/skills/cellprotocol-skeleton-renderer-porting/SKILL.md:35] |
| `cellprotocol-transport-bridging/SKILL.md` | [belagt: CellScaffold::.claude/skills/cellprotocol-transport-bridging/SKILL.md:25] |
| `codex-collaboration/SKILL.md` | [belagt: CellScaffold::.claude/skills/codex-collaboration/SKILL.md:14] |
| `dimy-payment-regulatory-guardrails/SKILL.md` | [belagt: CellScaffold::.claude/skills/dimy-payment-regulatory-guardrails/SKILL.md:12] |
| `dimy-value-redistribution/SKILL.md` | [belagt: CellScaffold::.claude/skills/dimy-value-redistribution/SKILL.md:12] |
| `dimy-value-redistribution/references/workflow.md` | [belagt: CellScaffold::.claude/skills/dimy-value-redistribution/references/workflow.md:13] |
| `haven-claim-review/SKILL.md` | [belagt: CellScaffold::.claude/skills/haven-claim-review/SKILL.md:12] |
| `haven-disk-and-machine-health/SKILL.md` | [belagt: CellScaffold::.claude/skills/haven-disk-and-machine-health/SKILL.md:28] |
| `haven-functional-service-verification/references/porthole-demo-testing.md` | [belagt: CellScaffold::.claude/skills/haven-functional-service-verification/references/porthole-demo-testing.md:97] |
| `haven-functional-service-verification/references/sandbox-capability-matrix.md` | [belagt: CellScaffold::.claude/skills/haven-functional-service-verification/references/sandbox-capability-matrix.md:22] |
| `haven-functional-service-verification/references/staging-verification.md` | [belagt: CellScaffold::.claude/skills/haven-functional-service-verification/references/staging-verification.md:34] |
| `haven-git-workflow/SKILL.md` | [belagt: CellScaffold::.claude/skills/haven-git-workflow/SKILL.md:31] |
| `haven-gui-testing/references/playwright-runner-patterns.md` | [belagt: CellScaffold::.claude/skills/haven-gui-testing/references/playwright-runner-patterns.md:6] |
| `haven-prompt-purpose-testing/SKILL.md` | [belagt: CellScaffold::.claude/skills/haven-prompt-purpose-testing/SKILL.md:16] |
| `haven-work-intake/SKILL.md` | [belagt: CellScaffold::.claude/skills/haven-work-intake/SKILL.md:17] |
| `haven-work-intake/references/github-work-sync-schema.md` | [belagt: CellScaffold::.claude/skills/haven-work-intake/references/github-work-sync-schema.md:8] |
| `haven-work-intake/references/project-portfolio-schema.md` | [belagt: CellScaffold::.claude/skills/haven-work-intake/references/project-portfolio-schema.md:7] |
| `haven-work-intake/references/work-item-schema.md` | [belagt: CellScaffold::.claude/skills/haven-work-intake/references/work-item-schema.md:8] |
| `haven-xcode-workspace-recovery/SKILL.md` | [belagt: CellScaffold::.claude/skills/haven-xcode-workspace-recovery/SKILL.md:21] |
| `omnigraffle-illustrations/SKILL.md` | [belagt: CellScaffold::.claude/skills/omnigraffle-illustrations/SKILL.md:43] |

I den undersøkte ekstra utsjekken med lokalt navn `CellScaffold-corr-deploy` finnes også `.claude/skills/haven-local-dev-environment-setup/SKILL.md` og `.claude/skills/haven-copilot-onboarding-dialogue-authoring-workspace/iteration-1/benchmark.json` med en annen utviklers personlige stier. Skillen må skille repo-kilder fra lokale datasett og slå datasettene opp som navngitte device-ressurser; benchmarkens skill-adresse må bli repo + relativ sti, og historisk målekontekst merkes ved normalisering. Kildeankrene bruker her `device.workspace` for å identifisere den faktisk undersøkte utsjekken, uten å innføre katalognavnet som repo-ID. [belagt: device.workspace::CellScaffold-corr-deploy/.claude/skills/haven-local-dev-environment-setup/SKILL.md:92] [belagt: device.workspace::CellScaffold-corr-deploy/.claude/skills/haven-copilot-onboarding-dialogue-authoring-workspace/iteration-1/benchmark.json:4] [vurdering]

Installerte kopier under `~/.codex/skills/<skill>/` og `~/.claude/skills/<skill>/` skal synkroniseres fra rettet kilde, ikke vedlikeholdes som konkurrerende varianter. Repo-kopier i et annet aktivt checkout må tas inn via det checkoutets normale endringsflyt; ikke masseoverskriv worktrees. Dokumentasjonsferdigheten beskriver allerede de tre installasjons-/pakkeflatene. [belagt: CellProtocolDocuments::.claude/skills/cellprotocol-docs-and-rag-maintenance/SKILL.md:30] [vurdering]

### PDD-er, prompts og resultatreferanser

Alle filadresser i tabellen nedenfor tilhører repoet `CellProtocolDocuments`. Endringer i operative kommandoer følger §5; kryssrepo-kildereferanser blir `repo::path`. For en oppgavespesifikk kortform `P` skal bindingen stå før første bruk. [vurdering]

| Fil | Konkret behandling |
|---|---|
| `Deliverables/PDD_arbeidsko-ai-utforere_2026-09-07/FORMAALSSPEC.md` [belagt: CellProtocolDocuments::Deliverables/PDD_arbeidsko-ai-utforere_2026-09-07/FORMAALSSPEC.md:12] | Navngi HAVEN-Deploy som repo; erstatt lokale programstier med `tools`-oppslag og samlemappens jobbmodell med versjonert repo-adresse ved købyttet. [vurdering] |
| `Deliverables/PDD_arbeidsko-ai-utforere_2026-09-07/PLAN.md` [belagt: CellProtocolDocuments::Deliverables/PDD_arbeidsko-ai-utforere_2026-09-07/PLAN.md:3] | Navngi HAVEN-Deploy som repo; erstatt lokale programstier med `tools`-oppslag og samlemappens jobbmodell med versjonert repo-adresse ved købyttet. [vurdering] |
| `Deliverables/PDD_arbeidsko-ai-utforere_2026-09-07/handoff/README.md` [belagt: CellProtocolDocuments::Deliverables/PDD_arbeidsko-ai-utforere_2026-09-07/handoff/README.md:3] | Navngi HAVEN-Deploy som repo; erstatt lokale programstier med `tools`-oppslag og samlemappens jobbmodell med versjonert repo-adresse ved købyttet. [vurdering] |
| `Deliverables/PDD_bridge-fase2-handshake_2026-09-04/FORMAALSSPEC.md` [belagt: CellProtocolDocuments::Deliverables/PDD_bridge-fase2-handshake_2026-09-04/FORMAALSSPEC.md:28] | Erstatt operative/kilderefererende repo-prefikser med navngitt repo + relativ sti, og angi eksplisitt base for korte filnavn. [vurdering] |
| `Deliverables/PDD_bridge-fase2-handshake_2026-09-04/contract/bridge_session_handshake_contract_v1.json` [belagt: CellProtocolDocuments::Deliverables/PDD_bridge-fase2-handshake_2026-09-04/contract/bridge_session_handshake_contract_v1.json:5] | Splitt den dokumenterende kryssrepo-kildereferansen i repo-ID og relativ sti; endre ikke kontraktsemantikken som bieffekt. [vurdering] |
| `Deliverables/PDD_bridge-fase2-handshake_2026-09-04/handoff/README.md` [belagt: CellProtocolDocuments::Deliverables/PDD_bridge-fase2-handshake_2026-09-04/handoff/README.md:7] | Bind `P` til dokumentrepo + oppgavemappe; navngi utførelsesrepo og erstatt kryssrepo-/HAVEN-stier med oppslag. Køprodusentregler byttes først ved M7. [vurdering] |
| `Deliverables/PDD_correspondence-vedlegg_2026-09-04/FORMAALSSPEC.md` [belagt: CellProtocolDocuments::Deliverables/PDD_correspondence-vedlegg_2026-09-04/FORMAALSSPEC.md:15] | Erstatt operative/kilderefererende repo-prefikser med navngitt repo + relativ sti, og angi eksplisitt base for korte filnavn. [vurdering] |
| `Deliverables/PDD_entitetsdata-egen-kontroll_2026-09-08/FORMAALSSPEC.md` [belagt: CellProtocolDocuments::Deliverables/PDD_entitetsdata-egen-kontroll_2026-09-08/FORMAALSSPEC.md:24] | Erstatt operative/kilderefererende repo-prefikser med navngitt repo + relativ sti, og angi eksplisitt base for korte filnavn. [vurdering] |
| `Deliverables/PDD_palazzo-husk-det-jeg-sa_2026-09-05/FORMAALSSPEC.md` [belagt: CellProtocolDocuments::Deliverables/PDD_palazzo-husk-det-jeg-sa_2026-09-05/FORMAALSSPEC.md:17] | Erstatt operative/kilderefererende repo-prefikser med navngitt repo + relativ sti, og angi eksplisitt base for korte filnavn. [vurdering] |
| `Deliverables/PDD_palazzo-husk-det-jeg-sa_2026-09-05/PLAN.md` [belagt: CellProtocolDocuments::Deliverables/PDD_palazzo-husk-det-jeg-sa_2026-09-05/PLAN.md:5] | Erstatt operative/kilderefererende repo-prefikser med navngitt repo + relativ sti, og angi eksplisitt base for korte filnavn. [vurdering] |
| `Deliverables/PDD_palazzo-husk-det-jeg-sa_2026-09-05/TESTRESULT.md` [belagt: CellProtocolDocuments::Deliverables/PDD_palazzo-husk-det-jeg-sa_2026-09-05/TESTRESULT.md:130] | Rett kryssrepo-lenker og gjenkjøringsoppskrifter; merk eventuell normalisering av historisk evidens etter regelen nedenfor. [vurdering] |
| `Deliverables/PDD_palazzo-husk-det-jeg-sa_2026-09-05/handoff/README.md` [belagt: CellProtocolDocuments::Deliverables/PDD_palazzo-husk-det-jeg-sa_2026-09-05/handoff/README.md:6] | Bind `P` til dokumentrepo + oppgavemappe; navngi utførelsesrepo og erstatt kryssrepo-/HAVEN-stier med oppslag. Køprodusentregler byttes først ved M7. [vurdering] |
| `Deliverables/PDD_palazzo-husk-det-jeg-sa_2026-09-05/handoff/run_codex_husk.sh` [belagt: CellProtocolDocuments::Deliverables/PDD_palazzo-husk-det-jeg-sa_2026-09-05/handoff/run_codex_husk.sh:3] | Avled PDD-mappe, utførelsesrepo og Codex-verktøy; fjern samlemappen som felles `cwd`. Avklar eksplisitte skriverøtter for den konkrete slicen. [vurdering] |
| `Deliverables/PDD_palazzo-rollesimulering_2026-09-08/FORMAALSSPEC.md` [belagt: CellProtocolDocuments::Deliverables/PDD_palazzo-rollesimulering_2026-09-08/FORMAALSSPEC.md:125] | Erstatt operative/kilderefererende repo-prefikser med navngitt repo + relativ sti, og angi eksplisitt base for korte filnavn. [vurdering] |
| `Deliverables/PDD_palazzo-rollesimulering_2026-09-08/PLAN.md` [belagt: CellProtocolDocuments::Deliverables/PDD_palazzo-rollesimulering_2026-09-08/PLAN.md:6] | Erstatt både `cd` og `--out` som vist i §5. [vurdering] |
| `Deliverables/PDD_palazzo-rollesimulering_2026-09-08/STATUS.md` [belagt: CellProtocolDocuments::Deliverables/PDD_palazzo-rollesimulering_2026-09-08/STATUS.md:19] | Erstatt operative/kilderefererende repo-prefikser med navngitt repo + relativ sti, og angi eksplisitt base for korte filnavn. [vurdering] |
| `Deliverables/PDD_palazzo-rollesimulering_2026-09-08/TESTRESULT.md` [belagt: CellProtocolDocuments::Deliverables/PDD_palazzo-rollesimulering_2026-09-08/TESTRESULT.md:9] | Rett kryssrepo-lenker og gjenkjøringsoppskrifter; merk eventuell normalisering av historisk evidens etter regelen nedenfor. [vurdering] |
| `Deliverables/PDD_palazzo-sicilia-artikler_2026-09-07/FORMAALSSPEC.md` [belagt: CellProtocolDocuments::Deliverables/PDD_palazzo-sicilia-artikler_2026-09-07/FORMAALSSPEC.md:16] | Erstatt operative/kilderefererende repo-prefikser med navngitt repo + relativ sti, og angi eksplisitt base for korte filnavn. [vurdering] |
| `Deliverables/PDD_palazzo-sicilia-artikler_2026-09-07/PLAN.md` [belagt: CellProtocolDocuments::Deliverables/PDD_palazzo-sicilia-artikler_2026-09-07/PLAN.md:4] | Erstatt operative/kilderefererende repo-prefikser med navngitt repo + relativ sti, og angi eksplisitt base for korte filnavn. [vurdering] |
| `Deliverables/PDD_palazzo-sicilia-artikler_2026-09-07/TESTRESULT.md` [belagt: CellProtocolDocuments::Deliverables/PDD_palazzo-sicilia-artikler_2026-09-07/TESTRESULT.md:5] | Rett kryssrepo-lenker og gjenkjøringsoppskrifter; merk eventuell normalisering av historisk evidens etter regelen nedenfor. [vurdering] |
| `Deliverables/PDD_palazzo-sicilia-artikler_2026-09-07/handoff/GUI.md` [belagt: CellProtocolDocuments::Deliverables/PDD_palazzo-sicilia-artikler_2026-09-07/handoff/GUI.md:11] | Bind `P` til dokumentrepo + oppgavemappe; navngi utførelsesrepo og erstatt kryssrepo-/HAVEN-stier med oppslag. Køprodusentregler byttes først ved M7. [vurdering] |
| `Deliverables/PDD_palazzo-sicilia-artikler_2026-09-07/images/verify/AVVIK.md` [belagt: CellProtocolDocuments::Deliverables/PDD_palazzo-sicilia-artikler_2026-09-07/images/verify/AVVIK.md:18] | Rett kryssrepo-lenker og gjenkjøringsoppskrifter; merk eventuell normalisering av historisk evidens etter regelen nedenfor. [vurdering] |
| `Deliverables/PDD_palazzo-sicilia-artikler_2026-09-07/images/verify/NATIVE.md` [belagt: CellProtocolDocuments::Deliverables/PDD_palazzo-sicilia-artikler_2026-09-07/images/verify/NATIVE.md:12] | Rett kryssrepo-lenker og gjenkjøringsoppskrifter; merk eventuell normalisering av historisk evidens etter regelen nedenfor. [vurdering] |
| `Deliverables/PDD_scaffold-admin-delegering_2026-09-08/FORMAALSSPEC.md` [belagt: CellProtocolDocuments::Deliverables/PDD_scaffold-admin-delegering_2026-09-08/FORMAALSSPEC.md:26] | Erstatt operative/kilderefererende repo-prefikser med navngitt repo + relativ sti, og angi eksplisitt base for korte filnavn. [vurdering] |
| `Deliverables/PDD_scaffold-admin-delegering_2026-09-08/STATUS.md` [belagt: CellProtocolDocuments::Deliverables/PDD_scaffold-admin-delegering_2026-09-08/STATUS.md:25] | Erstatt operative/kilderefererende repo-prefikser med navngitt repo + relativ sti, og angi eksplisitt base for korte filnavn. [vurdering] |
| `Deliverables/PDD_scaffold-admin-delegering_2026-09-08/TESTRESULT.md` [belagt: CellProtocolDocuments::Deliverables/PDD_scaffold-admin-delegering_2026-09-08/TESTRESULT.md:64] | Rett kryssrepo-lenker og gjenkjøringsoppskrifter; merk eventuell normalisering av historisk evidens etter regelen nedenfor. [vurdering] |
| `Deliverables/PDD_scaffold-admin-delegering_2026-09-08/handoff/README.md` [belagt: CellProtocolDocuments::Deliverables/PDD_scaffold-admin-delegering_2026-09-08/handoff/README.md:3] | Bind `P` til dokumentrepo + oppgavemappe; navngi utførelsesrepo og erstatt kryssrepo-/HAVEN-stier med oppslag. Køprodusentregler byttes først ved M7. [vurdering] |
| `Deliverables/PDD_skeleton-render-paritet_2026-09-07/FORMAALSSPEC.md` [belagt: CellProtocolDocuments::Deliverables/PDD_skeleton-render-paritet_2026-09-07/FORMAALSSPEC.md:15] | Erstatt operative/kilderefererende repo-prefikser med navngitt repo + relativ sti, og angi eksplisitt base for korte filnavn. [vurdering] |
| `Deliverables/PDD_skeleton-render-paritet_2026-09-07/handoff/README.md` [belagt: CellProtocolDocuments::Deliverables/PDD_skeleton-render-paritet_2026-09-07/handoff/README.md:126] | Bind `P` til dokumentrepo + oppgavemappe; navngi utførelsesrepo og erstatt kryssrepo-/HAVEN-stier med oppslag. Køprodusentregler byttes først ved M7. [vurdering] |
| `Deliverables/PDD_skeleton-render-paritet_2026-09-07/patch/README.md` [belagt: CellProtocolDocuments::Deliverables/PDD_skeleton-render-paritet_2026-09-07/patch/README.md:33] | Erstatt operative/kilderefererende repo-prefikser med navngitt repo + relativ sti, og angi eksplisitt base for korte filnavn. [vurdering] |
| `Deliverables/PDD_tillitspakke-agentflaate_2026-09-08/FORMAALSSPEC.md` [belagt: CellProtocolDocuments::Deliverables/PDD_tillitspakke-agentflaate_2026-09-08/FORMAALSSPEC.md:18] | Erstatt operative/kilderefererende repo-prefikser med navngitt repo + relativ sti, og angi eksplisitt base for korte filnavn. [vurdering] |
| `Deliverables/PDD_tillitspakke-agentflaate_2026-09-08/PLAN.md` [belagt: CellProtocolDocuments::Deliverables/PDD_tillitspakke-agentflaate_2026-09-08/PLAN.md:5] | Erstatt operative/kilderefererende repo-prefikser med navngitt repo + relativ sti, og angi eksplisitt base for korte filnavn. [vurdering] |
| `Deliverables/PDD_tillitspakke-agentflaate_2026-09-08/STATUS.md` [belagt: CellProtocolDocuments::Deliverables/PDD_tillitspakke-agentflaate_2026-09-08/STATUS.md:77] | Erstatt operative/kilderefererende repo-prefikser med navngitt repo + relativ sti, og angi eksplisitt base for korte filnavn. [vurdering] |
| `Deliverables/PDD_tillitspakke-agentflaate_2026-09-08/TESTRESULT.md` [belagt: CellProtocolDocuments::Deliverables/PDD_tillitspakke-agentflaate_2026-09-08/TESTRESULT.md:44] | Rett kryssrepo-lenker og gjenkjøringsoppskrifter; merk eventuell normalisering av historisk evidens etter regelen nedenfor. [vurdering] |
| `Deliverables/PDD_tillitspakke-agentflaate_2026-09-08/evidence/wp11/precheck.json` [belagt: CellProtocolDocuments::Deliverables/PDD_tillitspakke-agentflaate_2026-09-08/evidence/wp11/precheck.json:5] | Rett kryssrepo-lenker og gjenkjøringsoppskrifter; merk eventuell normalisering av historisk evidens etter regelen nedenfor. [vurdering] |
| `Deliverables/PDD_tillitspakke-agentflaate_2026-09-08/evidence/wp13/run-context.json` [belagt: CellProtocolDocuments::Deliverables/PDD_tillitspakke-agentflaate_2026-09-08/evidence/wp13/run-context.json:2] | Rett kryssrepo-lenker og gjenkjøringsoppskrifter; merk eventuell normalisering av historisk evidens etter regelen nedenfor. [vurdering] |
| `Deliverables/PDD_tillitspakke-agentflaate_2026-09-08/handoff/README.md` [belagt: CellProtocolDocuments::Deliverables/PDD_tillitspakke-agentflaate_2026-09-08/handoff/README.md:3] | Bind `P` til dokumentrepo + oppgavemappe; navngi utførelsesrepo og erstatt kryssrepo-/HAVEN-stier med oppslag. Køprodusentregler byttes først ved M7. [vurdering] |

Agentflåtens handoff har en sammenhengende familie av prompts som erklærer HAVEN-roten som `cwd`. Rett **hver** av `Deliverables/PDD_tillitspakke-agentflaate_2026-09-08/handoff/prompts/post0-gren.prompt.md`, `post0b-gjenoppretting.prompt.md`, `wp01.prompt.md`, `wp02.prompt.md`, `wp03.prompt.md`, `wp04.prompt.md`, `wp05.prompt.md`, `wp06.prompt.md`, `wp07.prompt.md`, `wp08.prompt.md`, `wp09.prompt.md`, `wp09b.prompt.md`, `wp10.prompt.md`, `wp11.prompt.md`, `wp12.prompt.md` og `wp13.prompt.md`. Sett eksplisitt dokumentrepo/`P`, utførelsesrepo og oppslag for hver kryssrepo-fil; ikke gjør global `cd HAVEN` til felles regel. [belagt: CellProtocolDocuments::Deliverables/PDD_tillitspakke-agentflaate_2026-09-08/handoff/prompts/post0-gren.prompt.md:1] [belagt: CellProtocolDocuments::Deliverables/PDD_tillitspakke-agentflaate_2026-09-08/handoff/prompts/wp01.prompt.md:1] [belagt: CellProtocolDocuments::Deliverables/PDD_tillitspakke-agentflaate_2026-09-08/handoff/prompts/wp13.prompt.md:1] [vurdering]

`Deliverables/PDD_scaffold-admin-delegering_2026-09-08/handoff/queue-ready/sad-wp1-registry-20260909.job` har tom første linje, `workspace-write` og en samlemappereferanse på tredje linje. Konverter denne ventende jobbmalen sammen med den tilhørende `.prompt.md` ved M7; ikke få gammel runner til å gjette at nytt innhold er det gamle linjeformatet. [belagt: CellProtocolDocuments::Deliverables/PDD_scaffold-admin-delegering_2026-09-08/handoff/queue-ready/sad-wp1-registry-20260909.job:2] [belagt: CellProtocolDocuments::Deliverables/PDD_scaffold-admin-delegering_2026-09-08/handoff/queue-ready/sad-wp1-registry-20260909.prompt.md:1] [vurdering]

Historiske testutdata må behandles annerledes enn gjenbrukbare kjøreinstrukser. Agentflåtens handoff krever ekte råutdata, og Sicilia-resultatet inneholder både historiske logger og kryssrepo-lenker. Ved migrering: rett referanser og oppskrifter; hvis personlige stier i innlimte råutdata normaliseres i en repo-publisert kopi, merk eksplisitt at kopien er stinormalisert og bevar originalens hash og lokal evidensreferanse. Ikke fremstille omskrevet tekst som byteidentisk råutdata eller som en ny testkjøring. Fremtidige rålogger holdes lokalt, mens portable rapporter bruker repo-adresser. [belagt: CellProtocolDocuments::Deliverables/PDD_tillitspakke-agentflaate_2026-09-08/handoff/README.md:13] [belagt: CellProtocolDocuments::Deliverables/PDD_palazzo-sicilia-artikler_2026-09-07/TESTRESULT.md:11] [belagt: CellProtocolDocuments::Deliverables/PDD_palazzo-sicilia-artikler_2026-09-07/TESTRESULT.md:17] [vurdering]

## 8. Videre navngitte forbrukere og åpne grenser

| Fil | Funn, erstatning og verifisering |
|---|---|
| `PalazzoScaffold::Package.swift` | Miljøvariabel og søskenoppslag velger lokal CellProtocol. Migrer lokal utviklingsmodus til en adapter som får CellProtocol-stien utelukkende fra valgt JSON, og fjern automatisk søskenoppdagelse. Behold eksplisitt valgt fjernavhengighet for bygg som skal bruke den; ikke endre revisjon som bieffekt. Verifiser lokal avhengighetsadresse med et repo utenfor fellesmappen og en separat fjernmodus. [belagt: PalazzoScaffold::Package.swift:20] [belagt: PalazzoScaffold::Package.swift:30] [vurdering] |
| `CellScaffold::Package.swift` | `coordinatedLocalPackagePath` avleder også søsken fra andre miljøvariabler og egen pakke. Erstatt den lokale plasseringspolitikken med samme adapterkontrakt; avledede miljøverdier kan være transport til SwiftPM, men ikke en manuelt vedlikeholdt andre oversikt. Verifiser alle berørte lokale avhengigheter og riktig revisjonsvalg før normal byggtest. [belagt: CellScaffold::Package.swift:44] [belagt: CellScaffold::Package.swift:52] [belagt: CellScaffold::Package.swift:61] [vurdering] |
| `device.workspace::.agent-tools/agent_job_runner.py` og `.agent-tools/README.md` | Runneren avleder hele HAVEN-treet fra sin egen fil og avviser `cwd` utenfor dette treet. Den unngår personnavn, men støtter fortsatt ikke vilkårlig repo-plassering. Migrer jobbadresser og policy separat fra `_losen-queue`; behold kommandobegrensningene. Test eksplisitt tillatt repo utenfor fellesmappen og avvist uregistrert mål med en falsk utfører. [belagt: device.workspace::.agent-tools/agent_job_runner.py:30] [belagt: device.workspace::.agent-tools/agent_job_runner.py:107] [belagt: device.workspace::.agent-tools/README.md:51] [vurdering] |
| `HavenAgentD::Contracts/agent-job-v1.schema.json` | `workspacePath` er i dag beskrevet som absolutt. En portabel innsendingskontrakt må ha repo-ID/relativt mål og separat vertslokal utledning; behold et avledet absolutt runtime-felt hvis utføreren trenger det. Dette krever versjonert kontrakt og verifikasjon av produsent/forbruker, ikke bare omskriving av schema-beskrivelsen. [belagt: HavenAgentD::Contracts/agent-job-v1.schema.json:40] [vurdering] |

Det er ikke avgjort her hvilken fysisk kilde/installasjon som skal eie alle nåværende samlemappeskript eller alle historiske skill-kopier. Ved implementering må eieren navngis før distribusjon, og endrede referanser må testes mot valgt checkout. Dette er et avgrenset åpent migreringspunkt, ikke grunn til å gjeninnføre maskinstier i repoer. [usikker] [vurdering]

HAVENAgentD-køen måtte kunne motta portable repo-adresser, avlede dem på utførerens device, håndheve lesing/skriving og isolasjon, og kvittere med verifisert leveranse og idempotent ferdigmarkør for at denne oppgaven naturlig skulle ligge der. [vurdering]

FERDIG-MARKØR
