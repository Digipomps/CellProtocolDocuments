# Commitrapport 2 — menylinje og varsler

To lokale commits er opprettet med avtalt filfordeling. **Ingen push er utført.** Gjennomgangen fant gjenværende problemer; commitene innebærer ingen endring av portstatusene nederst i rapporten.

Dato: 2026-09-10.
Arbeidstre: `/Users/kjetil/Build/Digipomps/HAVEN/HavenAgentD/.worktrees/menylinje-20260909`.
Branch før og etter: `pdd/agent-menylinje-og-varsler`.
HEAD før: `7168001bf7a18d20a9153367f7883569ff108ec0`.
HEAD etter: `129e2719c3c2c257602381f190eecb71de202856`.

| Nr. | SHA | Førstelinje | Filantall |
| --- | --- | --- | ---: |
| 1 | `592bc4875eb0610fff41c40419ca3a76669a105d` | Rett åtte funn fra kodegjennomgangen av menylinjen | 11 |
| 2 | `129e2719c3c2c257602381f190eecb71de202856` | Beskriv menylinjen og legg ved en demo uten sideeffekter | 2 |

Commit 1 omfatter nøyaktig disse filene, med 324 tillegg og 39 slettinger:

```text
Sources/HavenAgentMenu/HavenAgentMenuApp.swift
Sources/HavenAgentMenu/AgentMenuModel.swift
Sources/HavenAgentMenu/ChallengeNotifier.swift
Sources/HavenAgentMenuCore/MenuPresentation.swift
Sources/HavenAgentMenuCore/NotificationDecider.swift
Sources/HavenAgentRuntime/AgentChallenge.swift
Sources/HavenAgentRuntime/ChallengeInboxService.swift
Sources/HavenAgentCellRuntime/AgentControlBridgeServer.swift
Contracts/agent-challenge-v1.schema.json
Tests/HavenAgentMenuCoreTests/MenuPresentationTests.swift
Tests/HavenAgentMenuCoreTests/NotificationDeciderTests.swift
```

Commit 2 omfatter `Docs/AgentMenylinje.md` og `Packaging/menu-app/demo.sh`, med 165 tillegg. Skriptet er registrert som kjørbart i Git (`100755`).

Etter siste commit ga `git log --oneline ba1489554bdf8b27f10ef0fdc8fa727689fa0c98..HEAD`:

```text
129e271 Beskriv menylinjen og legg ved en demo uten sideeffekter
592bc48 Rett åtte funn fra kodegjennomgangen av menylinjen
7168001 Legg til menylinjeappen og pakk den som en app-bundle
d61d533 Skill mellom ro, oppmerksomhet og «vet ikke» i menylinjekjernen
2815d90 La kontrollbroen vise ventende saker og ta imot svar
f750d1d Samle alt som venter på et menneske i challenge-innboksen
a2623d8 Ta inn identitetslasting som forutsetning for bygg
```

Sluttstatus fra `git status --porcelain`:

```text
 M Package.resolved
```

Indeksen er tom. `Package.resolved` er verken staget eller committet. Endringen var til stede ved oppstart og skyldes ifølge oppgaven `swift package edit`. Filen er uendret av denne jobben.

SHA-256 og filmodus ble sammenlignet før staging og etter begge commits for alle 14 berørte filer: de 13 avtalte commitfilene og `Package.resolved`. Alle er identiske. Ingen kildefil, testfil, eksisterende dokumentasjon eller demoskript er redigert av denne jobben. Filfordeling og begge commitmeldinger er kontrollert mot de forberedte meldingene; begge har nøyaktig de pålagte PDD- og portlinjene. `git diff --check` for endringene og begge staged sett ga ingen treff. Skjemaet kunne leses som JSON, og `bash -n Packaging/menu-app/demo.sh` rapporterte ingen syntaksfeil.

Ingen relevante låser fantes under `HavenAgentD/.git/worktrees/menylinje-20260909/` ved oppstart eller før Git-skrivingene: verken `index.lock`, `HEAD.lock` eller `refs/**/*.lock`. Den delte `HavenAgentD/.git/index.lock` ble ikke brukt som stoppgrunn og er ikke endret eller fjernet. Ingen filer i det delte arbeidstreet eller `.worktrees/menylinje-base-20260909` er endret. Ingen checkout, switch, rebase, merge, reset eller stash er utført.

Bygg og tester er ikke kjørt i denne jobben. Appen og demoen er heller ikke startet. Tidligere resultater er kontrollert ved lesing av eksisterende logger:

- Oppgitt `.build/menylinje-baseline/wp9.summary.txt` finnes under hovedrepoet `HavenAgentD`, ikke relativt til dette arbeidstreet.
- Oppsummeringen, datert `2026-09-10T00:03:58Z`, oppgir `EXIT_BUILD=0`, `EXIT_TEST=1` og 212 beståtte Swift Testing-tester i 41 suiter, uten registrerte feilende tester.
- `HavenAgentD/.build/menylinje-baseline/wp9.test.log:15` viser at XCTest-pakken ikke kunne lastes. Linje 16 angir `have 'arm64', need 'x86_64'` og peker på testpakken i det avtalte arbeidstreet. Linje 585 bekrefter de 212 beståtte Swift Testing-testene. Dette forklarer avviket mellom beståtte tester og testkommandoens feilkode; kjøringen kan ikke beskrives som en testkommando med exit 0.

Det er to bevisste presiseringer i commitmeldingenes brødtekst sammenlignet med bestillingen. Commit 1 omtaler åtte nye regresjonstester, men påstår ikke én test per rettelse, siden diffen ikke dokumenterer dette. Commit 2 beskriver separat rot, port og miljøvariabler, men nevner også at skriptets `pkill` stopper eksisterende menylinjeapper. De to ønskede førstelinjene er beholdt ordrett. Ingen fil er holdt utenfor den avtalte fordelingen på grunn av disse funnene.

Følgende gjenværende problemer ble funnet ved lesing av kildekoden. Dette er statiske observasjoner, ikke nye test- eller GUI-resultater. Referansene gjelder filene i arbeidstreet ved HEAD etter commitene:

1. **Varselkvitteringen bekrefter ikke varselsenterets resultat.** `Sources/HavenAgentMenu/ChallengeNotifier.swift:98` kaller `center.add` uten completion-handler og returnerer umiddelbart `true` på linje 101. `AgentMenuModel.swift:74` markerer dermed saken som varslet selv om registreringen senere feiler. Apple dokumenterer at resultat og eventuell feil kommer gjennom completion-handleren eller `async throws`; dagens returverdi leser ingen av dem. Se [Apples dokumentasjon for add(_:withCompletionHandler:)](https://developer.apple.com/documentation/usernotifications/unusernotificationcenter/add%28_%3Awithcompletionhandler%3A%29?changes=_9). Testen `aNotificationThatNeverArrivedStaysPending` simulerer fravær av kvittering i kjernen og kaller ikke `ChallengeNotifier.post`.

2. **Samlevarsler husker ikke de underliggende sakene i produksjonsveien.** Ved mer enn tre nye saker lager `Sources/HavenAgentMenuCore/NotificationDecider.swift:66` en syntetisk ID basert på `generatedAt`. `AgentMenuModel.swift:75` markerer bare denne ID-en, mens kandidatfilteret på `NotificationDecider.swift:61` sjekker de opprinnelige saks-ID-ene. Neste oppdatering kan derfor lage et nytt samlevarsel for de samme sakene, normalt hvert 20. sekund. `forgetIdentifiersMissing` fjerner dessuten den syntetiske ID-en siden den ikke finnes i innboksen. Testen `collapsedSummaryStillRemembersEveryUnderlyingChallenge` bruker `decide`, som har en egen løkke for underliggende saker; appen bruker `pending` og `markNotified` og får ikke denne oppførselen. «Ignorer i dag» på samlevarselet demper også bare den syntetiske ID-en.

3. **Døgnskiftet frigir ikke en sak som allerede er varslet.** `Sources/HavenAgentMenuCore/NotificationDecider.swift:111` registrerer dagens demping, men fjerner ikke saken fra `notifiedIdentifiers`. Forløpet `markNotified(id)`, `dismissForNow(id)`, neste dag lar derfor kandidatfilteret fortsatt utelate saken så lenge den finnes i innboksen. Testen `dismissForNowExpiresWithTheDay` starter med en sak som aldri er markert som varslet, og dekker ikke det vanlige forløpet fra en varselknapp.

4. **Varselknappene følger fortsatt to faste kategorier.** `Sources/HavenAgentMenu/ChallengeNotifier.swift:104` sjekker bare om `.approve` finnes. Kategorien på linje 64 tilbyr da alltid approve/reject/open; alle andre saker får open/dismissToday. En sak med bare approve får dermed ekstra svar, og en sak med reject uten approve mister reject-knappen. Helsesakene i `Sources/HavenAgentD/AgentChallengeWiring.swift` oppgir bare open, men får også dismissToday i varslet. Menyradene bruker nå sakens egne alternativer; denne gjenværende forskjellen gjelder varselsenteret.

5. **Demoen har sideeffekter og svak oppstartskontroll.** `Packaging/menu-app/demo.sh:42` bruker `pkill -f "HAVEN Agent"`, som ikke er avgrenset til en prosess startet av demoen. Det stopper eksisterende menylinjeapper og kan treffe andre prosesser med samme tekst i kommandolinjen. Porten på linje 15 er fast som standard, og helsesjekken på linje 33 bekrefter ikke at svareren er den nyopprettede prosessen. Etter 30 mislykkede forsøk går skriptet likevel videre til teksten om at agenten svarer. Ved opptatt port kan det lese en eksisterende tjeneste. Den midlertidige roten opprettes også før appkontrollen, mens cleanup-trap først installeres etter kontrollen; manglende app etterlater derfor roten. Skriptet er ikke kjørt i denne jobben.

6. **Åtte nye tester betyr ikke dekning av alle åtte rettelser.** Diffen har to tester for menyraders svaralternativer, fire for varslingskjernen, én for kildebegrunnelsens filter og én for kontraktsversjon. Ingen av de nye testene kaller appens `start()`, åpner et vindu, prøver varselsenterets kategorier/feilresultat eller sender en ugyldig innboks gjennom broens HTTP-rute. Filtertesten validerer innboksen direkte; den tester ikke rutens nye avvisning. Samlevarseltesten bruker dessuten en annen kvitteringsvei enn appen, som beskrevet over.

Et eget GUI-spørsmål står åpent: `Sources/HavenAgentMenu/HavenAgentMenuApp.swift:29` observerer `requestedAdminWindow` inne i innholdet til selve adminvinduet. «Åpne» fra et varsel bør derfor prøves fra en appøkt der vinduet aldri har vært åpnet, og etter at vinduet er lukket. Koden alene dokumenterer ikke at observatøren er aktiv i disse situasjonene; ingen konkret GUI-feil påstås som reprodusert her.

Verktøyavvik: `rg` var ikke installert, så avgrensede filsøk brukte Python. Det første forsøket på å lese byggoppsummeringen i arbeidstreet fant ikke filen; den eksisterende filen ble deretter funnet og lest i hovedrepoets `.build`. Apples dokumentasjon ble kontrollert på nett for varselsenterets completion-handler.

Denne rapporten er eneste nye prosjektfil skrevet av jobben og er ikke committet. Ingen tredje commit er opprettet. `CellProtocolDocuments` står på branch `codex/docs-cleanup-20260810`, HEAD `f6aa54460d82ae52ede8a7475c4dff133175d4a7`; repoets eksisterende endringer er latt stå. Ingen push er utført.

PDD: CellProtocolDocuments::Deliverables/PDD_agent-menylinje-og-varsler_2026-09-09/
G1: venter · G1-GUI: venter · G3: venter
