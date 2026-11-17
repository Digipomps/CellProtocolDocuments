# Commitrapport 4 — tredje runde gjennomgangsrettelser

Én lokal commit med nøyaktig de sju bestilte filene er opprettet. **Ingen push er utført.** Kritisk gjennomlesing fant fire restfeil. Den bestilte committeksten er beholdt, men påstanden om reservasjon før levering stemmer ikke med produksjonskoden; avviket er presisert nedenfor. Ingen kildefiler er endret av denne jobben.

Dato: 2026-09-10.
Arbeidstre: `/Users/kjetil/Build/Digipomps/HAVEN/HavenAgentD/.worktrees/menylinje-20260909`.
Branch før og etter: `pdd/agent-menylinje-og-varsler`.
HEAD før: `ed0a821bebf095eedceb242e65bb43dcafcf14c6`.
HEAD etter / commit-SHA: `4d3bc677a823c66d29437208663070992309ef3a`.
Førstelinje: `Rett seks funn fra tredje gjennomlesing av menylinjen`.
Filantall: **7**, med **187 tillegg og 13 slettinger**.

```text
Sources/HavenAgentMenu/AgentMenuModel.swift
Sources/HavenAgentMenu/ChallengeNotifier.swift
Sources/HavenAgentMenuCore/ChallengeNotifierCategory.swift
Sources/HavenAgentMenuCore/NotificationDecider.swift
Sources/HavenAgentRuntime/AgentChallenge.swift
Packaging/menu-app/demo.sh
Tests/HavenAgentMenuCoreTests/NotificationDeciderTests.swift
```

## Etterkontroll og sluttstatus

De tre bestilte kommandoene er kjørt etter commit.

`git rev-parse HEAD`:

```text
4d3bc677a823c66d29437208663070992309ef3a
```

`git log --oneline ba1489554bdf8b27f10ef0fdc8fa727689fa0c98..HEAD`:

```text
4d3bc67 Rett seks funn fra tredje gjennomlesing av menylinjen
ed0a821 Rett seks funn til fra gjennomlesingen av menylinjen
129e271 Beskriv menylinjen og legg ved en demo uten sideeffekter
592bc48 Rett åtte funn fra kodegjennomgangen av menylinjen
7168001 Legg til menylinjeappen og pakk den som en app-bundle
d61d533 Skill mellom ro, oppmerksomhet og «vet ikke» i menylinjekjernen
2815d90 La kontrollbroen vise ventende saker og ta imot svar
f750d1d Samle alt som venter på et menneske i challenge-innboksen
a2623d8 Ta inn identitetslasting som forutsetning for bygg
```

`git status --porcelain`:

```text
 M Package.resolved
```

Indeksen har ingen staged endringer. `Package.resolved` er verken staget eller committet. Forelder, branch, nøyaktig én ny commit, nøyaktig filsett og hele commitmeldingen er kontrollert. Meldingen har de seks bestilte punktene, merknaden om den snudde testen og de pålagte sluttlinjene.

SHA-256 og filmodus for de sju commitfilene og `Package.resolved` er identiske før staging og etter commit. De stagede blobene og de ferdige commitblobene er også sammenlignet med fingeravtrykkene. `git diff --check`, `git diff --cached --check` og kontroll av den ferdige commitdiffen ga ingen treff. `bash -n Packaging/menu-app/demo.sh` ga ingen syntaksfeil.

Ingen relevante låser fantes under `HavenAgentD/.git/worktrees/menylinje-20260909/` ved oppstart eller rett før staging og commit: verken `index.lock`, `HEAD.lock` eller `refs/**/*.lock`. Den delte `HavenAgentD/.git/index.lock` er ikke brukt som stoppgrunn, fjernet eller endret. Ingen aktive Git-hooks ble funnet. Ingen checkout, switch, rebase, merge, reset eller stash er utført. Ingen filer i det delte HavenAgentD-arbeidstreet eller `.worktrees/menylinje-base-20260909` er skrevet.

## Testgrunnlag og begrensninger

Ingen `swift build` eller `swift test` er kjørt. Appen, varselsenteret og den komplette demoen er heller ikke startet.

Eksisterende oppsummeringer ble lest fra `HavenAgentD/.build/menylinje-baseline/`; de finnes ikke relativt til det avtalte arbeidstreet. `wp13.summary.txt`, datert `2026-09-10T00:41:56Z`, oppgir `EXIT_BUILD=0`, `EXIT_TEST=1` og **224 tester i 43 suiter med 2 issues**:

- `decodedDefaultAgentCellsInstallBindingsOnceBeforeImmediateStateReads`: `ownerProofUnavailable`.
- `hostedAgentIdentityProvesRemoteBridgeControl`: `requesterAuthorityUnavailable`.

`base.summary.txt` viser 165 tester i 33 suiter: begge feil forekommer i basekjøring 1 og 3, mens bare den første forekommer i kjøring 2. Dermed er begge wp13-feilene bekreftet også på ren base. Oppsummeringene er tidligere kjøringer; denne jobben har ikke bevist at den ferdige commiten er uten regresjoner.

To avgrensede Python-kontroller bekreftet identisk tekst før kategorihashing og tilstandsfølgen ved demping under levering. De er modeller av de leste uttrykkene, ikke kjøring av Swift-implementasjonen. Tre isolerte Bash-kontroller brukte `keep_log` og `cleanup` hentet uendret fra skriptet, syntetiske logger i egne midlertidige mapper og stubber for feilende `curl`, `wait` eller `cp`. Ingen agent, app eller nettverkskall ble startet; ingen eksisterende demologg ble skrevet. Resultatene er beskrevet under funn 4.

## Avvik mellom bestilt committekst og kode

`AgentMenuModel.swift:68` hindrer nå overlappende `refresh()`-kall. Dette lukker den tidligere beskrevne dupliseringsveien mellom to oppdateringer av samme modell.

Men produksjonsløkken på `AgentMenuModel.swift:77` gjør fremdeles `await notifier.post(decision)` først og `decider.markNotified(decision)` etter vellykket levering, på linje 84. Den reserverer ikke før levering og kaller aldri den nye `forget(_:)` ved feil. `NotificationDecider.forget(_:)` på linje 109 brukes bare av de to nye reservasjonstestene. Commitmeldingens første punkt beskriver derfor mer enn det som er koblet inn i appen. Dette er et dokumentasjons- og integrasjonsavvik, ikke i seg selv bevis for at den gamle dupliseringsfeilen mellom oppdateringer fortsatt finnes. Den separate dempingsfeilen nedenfor viser derimot en gjenværende følge av leveringsrekkefølgen.

Den eldre testen er **snudd, ikke fjernet**: `theSameResponseSetIsAlwaysTheSameCategory` krevde at rekkefølgen ikke påvirket kategorien. Den heter nå `theSameResponseShapeIsAlwaysTheSameCategory` og sammenligner identisk form. Den nye `orderOfActionsIsPartOfTheCategory` krever ulike kategorier når rekkefølgen er ulik. De sju nye testene dekker to reservasjonstilstander, tre kategorisammenligninger og to knappetekstvalideringer. Ingen av dem kjører modellens faktiske leveringsløkke, varselsenterets handlinger eller demoens feilutganger.

## Fire restfeil fra ny kritisk gjennomlesing

«Nye» betyr oppdaget i denne gjennomgangen. Ikke alle er innført av denne commiten. Kodehenvisningene gjelder `4d3bc677a823c66d29437208663070992309ef3a` i det avtalte arbeidstreet. Ingen av funnene er rettet her.

### 1. P2 — To forskjellige knappesett kan fortsatt få samme kategori

`Sources/HavenAgentMenuCore/ChallengeNotifierCategory.swift:23` bygger en streng med `=`, `|` og `;` uten å escape eller lengdeprefikse knappetekstene. Disse tegnene er tillatt i `label`, både av Swift-valideringen og JSON-skjemaet. Følgende to forskjellige sett får identisk tekst før hashing:

```text
A: [open(label: "Åpne|-;approve=Godkjenn", destructive: false)]
B: [open(label: "Åpne", destructive: false),
    approve(label: "Godkjenn", destructive: false)]

Begge blir: open=Åpne|-;approve=Godkjenn|-
```

Dette er en deterministisk kollisjon i serialiseringen, uavhengig av hashfunksjonens kollisjonssannsynlighet. Etikettene er under skjemaets 40-tegnsgrense og inneholder ingen tekst som filteret avviser. Den avgrensede Python-kontrollen ga `DIFFERENT_SHAPES_SAME_INPUT: True`.

`ChallengeNotifier.swift:47` gjenbruker en registrert kategori utelukkende etter ID. Hvis B er registrert først, vil en senere sak av form A gjenbruke kategorien med en ekstra «Godkjenn»-knapp; motsatt rekkefølge mister B knappen. Dette er utledet fra kode og gyldige inndata, ikke observert i macOS eller hos dagens produsenter. Bruk en entydig representasjon av svaralternativene før hashing, og dekk eksempelet med en regresjonstest.

### 2. P2 — Demping under levering kan bli til varig taushet i samme appøkt

`AgentMenuModel.swift:77` beregner alle beslutningene før leveringsløkken. `isRefreshing` sperrer bare nye oppdateringer; `answer(..., response: .dismissToday)` på linje 108 kan fremdeles kjøres mens `post` venter. Dette er mulig ved Swifts dokumenterte suspensjonspunkter. Se [Swift: Concurrency](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/concurrency/).

Et konkret forløp er at innboksen med sak A og B vises, leveringen av A venter, og brukeren velger «Ignorer i dag» for B fra menyen. Dempingen fjerner B fra `notifiedIdentifiers` og lagrer dagens dato (`NotificationDecider.swift:139`). Deretter fortsetter den allerede beregnede løkken, leverer B uten å kontrollere dempingen på nytt og legger B tilbake i `notifiedIdentifiers` ved kvittering på modellens linje 84. Det samme problemet kan oppstå ved demping mens leveringen av selve B venter.

Når dagen skifter, er dempingen utløpt, men B ligger fortsatt i `notifiedIdentifiers`, og `pending` på linje 67 holder saken ute. Så lenge B forblir i innboksen og appøkten fortsetter, blir «Ignorer i dag» dermed lengre enn én dag. Den avgrensede tilstandsmodellen bekreftet at B fortsatt ikke er aktuell dagen etter. Dagens `ChallengeInboxService.swift:129` produserer faktisk alternativet «Ignorer i dag».

Den eksisterende testen `aDismissedChallengeCanNotifyAgainTheNextDay` demper først etter at `markNotified` er ferdig og dekker ikke denne rekkefølgen. Levering og kvittering må bevare demping som skjer under ventingen; hver ventende beslutning må også revurderes før den sendes. Dette er en statisk påvist mulig kjøresekvens, ikke en fremprovosert GUI-hendelse.

### 3. P3 — Destruktiv-flagget påvirker kategorinøkkelen, men ikke varselknappen

Den nye nøkkelen inkluderer `option.destructive`, men `Sources/HavenAgentMenu/ChallengeNotifier.swift:65` velger fortsatt handlingsopsjoner utelukkende fra `option.id`. For eksempel gir `.approve` med `destructive: true` bare `.authenticationRequired`, mens `.reject` alltid får `.destructive`, også ved eksplisitt `false`.

Dermed kan to kategorier få forskjellige ID-er på grunn av flagget, men like varselknapper. Flaten gjengir ikke flagget som kontrakten tilbyr. Apple beskriver at [destructive gir særskilt markering av en destruktiv handling](https://developer.apple.com/documentation/usernotifications/unnotificationactionoptions/destructive?changes=la). Autentiseringskravene fjernes ikke av dette avviket. Det er et eksisterende hull i gjengivelsen, synlig ved gjennomlesing av den nye kategoriformen; ingen konkret feilmarkering hos dagens produsenter eller i macOS er observert. Avklar standarden når flagget mangler, og la eksplisitte verdier styre markeringen.

### 4. P3 — Loggen forsvinner fortsatt ved feil etter helsesjekken, og kopieringsfeil skjules

`Packaging/menu-app/demo.sh:59` og linje 62 bevarer nå loggen ved de to uttrykkelige oppstartsfeilene. Men statuskallet på linje 65 kan nå avslutte med timeout etter fem sekunder. Med `set -e` på linje 11 går skriptet da rett til EXIT-opprydding uten `keep_log`; linje 47 sletter originalen. En agent som avslutter med feil etter vellykket oppstart gir samme problem gjennom `wait "$AGENT"` på linje 75. Dette stemmer med [Bashs dokumentasjon av errexit](https://www.gnu.org/s/bash/manual/html_node/The-Set-Builtin.html).

Isolerte kontroller med de faktiske oppryddingsfunksjonene og feilende stubber ga henholdsvis exit 28 og exit 1. I begge tilfeller var originalloggen borte etterpå, og ingen bevaringsmelding ble skrevet. Hele demoen ble ikke kjørt.

I tillegg svelger `keep_log` kopieringsfeil på linje 40 med `|| true`, men hevder alltid på linje 41 at loggen er tatt vare på. En tredje kontroll med feilende `cp` bekreftet denne meldingen samtidig som oppryddingen slettet originalen. Det faste loggmålet ble ikke skrevet i kontrollen. Bevar loggen ved alle relevante feilutganger, og bekreft vellykket bevaring før originalen slettes eller en lagringskvittering vises.

## Rapport og avgrensning

Denne rapporten er eneste nye prosjektfil skrevet av jobben og er ikke committet. Ingen ekstra commit er opprettet. `CellProtocolDocuments` hadde mange eksisterende endringer og står på branch `codex/docs-cleanup-20260810`, HEAD `f6aa54460d82ae52ede8a7475c4dff133175d4a7`; de øvrige filene er latt stå.

Midlertidige kontrollartefakter ligger i `/private/tmp/menylinje-commit-round3-before.json`, `/private/tmp/menylinje-commit-round3-after.json`, `/private/tmp/menylinje-commit-round3-review-checks.json` og `/private/tmp/menylinje-commit-round3-message.txt`. De er ikke committet.

`rg` var utilgjengelig, så avgrensede filsøk brukte Python. Enkelte direkte nettlesinger av dokumentasjon feilet eller viste bare JavaScript-sider; de siterte opplysningene ble deretter kontrollert i indekserte primærkilder fra Swift, Apple og GNU. Ingen verktøyavvik endret commitomfanget eller krevde kildeendringer.

PDD: CellProtocolDocuments::Deliverables/PDD_agent-menylinje-og-varsler_2026-09-09/
G1: venter · G1-GUI: venter · G3: venter
