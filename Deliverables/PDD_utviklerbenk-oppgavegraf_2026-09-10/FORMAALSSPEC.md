# Formålsspesifikasjon — Utviklerbenken: idétre, oppgavegraf og stegvis arbeidsflyt

Oppgavemappe: `PDD_utviklerbenk-oppgavegraf_2026-09-10` · Opprettet 2026-09-10 · **Iterasjon 2 (G1 venter)**
Surfaces: `gui skeleton web binding cell scaffold codex` · Stier skrives `Repo::sti` (relativt til repoets rot).

> Regel: ingen plan før G1 er godkjent av Kjetil. For GUI: ingen implementering før G1-GUI (rendret bilde) er godkjent.
> Et dokument om leveransen teller aldri som leveransen.

## Formålet med denne runden

Kjetil skal (1) få en sann, kildebelagt status på utviklerbenken slik den står 2026-09-10, (2) se hvor grensen
mot prosjektstyring og admin workbench går, og (3) få ønskene sine fanget som et formålstre som er klassifisert
mot det som allerede finnes — så ingenting bygges to ganger og ingenting antas. Hvert steg under måles mot det:
en påstand uten kilde er ikke med; et ønske uten observerbart mål er ikke klart.

Leseforbehold for iterasjon 1 (2026-09-10): `device_bash` var nede hele økten. Alt er lest som filer (staging). **Ingen git-kommando er kjørt**,
så «merget»/«ikke merget» er utledet fra filinnhold og står merket som det.

Iterasjon 2 (2026-09-14) gjelder gren E: plangraf, detaljer, egne handlinger og forklaring ved siden av.
Ny kildeaudit i §0.2 presiserer historikken over. CellScaffold er lest med `git show origin/main:<sti>`
på lokal remote-ref `649255bb777b3a5135bd9c50512d3074bd23935b`; arbeidskopien står på
`pdd/tillitspakke-agentflaate` og brukes ikke som kodebevis. CellProtocol-kode er tilsvarende lest på
lokal `origin/main` `c430a24c0d93d2cec9984149c4fb7546c6341bd3`. Ingen fetch eller nett; revisjonene
er lokale observasjoner, ikke en kontroll av dagens GitHub eller staging. Nye mål er forslag, ikke levert funksjon.

---

## 0. Intensjon (ordrett) og brief-audit

> **2026-09-28, bestilling fra Kjetil (ordrette utdrag):** Spørsmålslister skal kunne **vises og besvares i utviklerbenken**.
>
> Formålet er at en beslutning tatt av eieren skal ha **ett sted å bo**, fra den stilles til den er ført inn i det den påvirker.
>
> Ikke bygg noe på min oppfordring — dette er en bestilling til benkens PDD-løp, ikke en spesifikasjon.

Registrert som **E8, P0-inntak**, nedenfor. E3/E5, Valgbenken og Dommerbenken dekker deler av behovet,
men ikke hele spørsmålets livsløp. Dekningskontroll, kilder og neste steg står i
[inntaksrapporten 28.09](../BENK_SPOERSMAALSLISTER_2026-09-28.md). Tidligere portvedtak gjelder sitt
opprinnelige omfang; denne bestillingen godkjenner ikke en E8-spesifikasjon eller implementering.

> **2026-09-13, tillegg (ordrett, fra Butler-tråden):** Vi må jobbe litt med forståeligheten til formålsforslagene. Kanskje en grafisk fremstilling i tillegg vil hjelpe. Og Plan f.eks der er det veldig vanskelig å forstå hva det innebærer og hva jeg skal gjøre. Det kan vi forbedre i oppgavehånderingen vår ved å implementere en mulighet for en AI Agent forklaring på hvert punkt jeg lurer på. Dt kan vises ved siden av eller et overlay eller floating vindov men ikke i seg selv legge til i chatloggen. Det blir fortuoversiktlig.

> **2026-09-14, tillegg (ordrett, fra Butler-tråden, om plangrafen `PDD_butler-traadtre-og-widgetflate_2026-09-11/images/plan-v1.png`):** Herlig oversikt over plan. Vi vil trenge dette i workbench funksjonaliteten, med mulighet for å gå inn og se detaljer og å utføre hva som er mine handlinger (så det ikke stopper opp på at jeg ikke finner hvor jeg skal gjøre det og så glemmer det)

> Hva er staus med developer workbench nå? (den sklir kanskje litt over mot prosjekt håndtering - og kanskje til og med admin workbench [om man som meg er HAVEN bidragsyter - og er admin i scaffoldet]) Jeg tror det er nevnt før men jeg vil i developer workbench ha mulighet til å ha en liste med løse ideer som jeg når jeg har lyst kan sette i jobbe køer. Tror vi kan trenge en liste med trestruktur for bedre å kunne fange idestruktur. (kan da også vises som grafnoder) Jeg tror også det er en god ide å ta utgangs punkt i oppgaven som skal gjøres. Oppgaven kan være en deloppgave i en større sammenheng. Oppgaven har referenser til kilder - f.eks kode i git repoer, ellerreferanser til ekstern kunnskap eller abonnement på Flow. vi bør ha muligheten til å representere alle avhengigheter i en graf slik at den som evaluerer hvordan oppgaven best kan løses vet hva oppgaven må forholde seg til. ut fra oppgaven kan man sette opp stegvis arbeidsflyt, men analyse, informasjoninnhenting, drøfting, implementering, testing, push, commit, CI og deploy

> **2026-09-14, tillegg (ordrett, fra formålsregister-tråden, om artefaktet «Dommerbenken»):** Funksjonaliteten i artifaktet var veldig bra - dette bør inn i developer workbench

> **2026-09-29, tillegg (ordrett, fra Butler-tråden, om artefaktet «Dommerbenken · Butler-korpus», 52 saker):** Har svart dommerbenken. (Dette er funksjonalitet vi skal ha inn i developer workbench)

> **2026-09-16, tillegg (ordrett, fra deploy-tråden, om artefaktet «HAVEN Valgbenk»):** Av og til er det litt uklart om jeg skal kjøre skript du legger inn med en gang eller ikke. Og kanskje vi burde ha et sted å legge inn en kommentar eller respons på terminal kommando.

> **2026-09-16, tillegg (ordrett, samme tråd, om raden «PR #242 hjelpertre — konflikten er løst, venter på push»):** her burde det vært en knapp eller bedre forklaring på hva jeg skal gjøre. Når vi får valgbenken ut i egen flate må vi kunne starte handlingen fra kortet, og om vi lurer på hva som skjer - kunne gå inn i hva som skjer når man trykker på knappen. Eventuelt kjøre tørrkjøring.

**Fire krav utledet av tilleggene 16.09, og hva prototypen gjør i dag (artefakt `UoPxUNqrfXtJbf6Cos3fVE`, v13).** Dette er kandidater til gren E, ikke vedtatt funksjonalitet.

| Krav | Hva prototypen gjør nå | Hva flaten må gjøre |
|---|---|---|
| K-E20 · Hver kommando sier når den skal kjøres | Merke over kommandoblokken: «Kjør nå» / «Kjør etter <vilkår>» / «Ikke kjør <grunn>». Feltet er obligatorisk i generatoren — en kommando uten det stopper byggingen. | Vilkåret må være en maskinlesbar tilstand (test grønn, post 0–2 grønne), ikke en setning, slik at kortet selv kan vise når vilkåret er oppfylt. |
| K-E21 · Kommandoen skal kunne limes rett inn | Generatoren avviser plassholdere (`<nr>`, `<sha>`) i kommandofeltet. Bakgrunn: en `gh pr update-branch <nr>` 16.09 ga `zsh: no such file or directory: nr`. | Verdier flaten allerede kjenner (PR-nummer, SHA) settes inn av flaten; verdier den ikke kjenner hører ikke i en kopierbar blokk. |
| K-E22 · Svar fra terminalen har et sted å gå | Fritekstfelt per kort («Lim inn svaret fra terminalen», også når det feilet) som lagres i kortets rad og leses av agenten. | Bør knyttes til kjøringen (kommando, tidspunkt, exit-kode) som en hendelse på oppgaven, ikke bare fritekst på kortet. |
| K-E23 · Handlingen startes fra kortet, med innsyn og tørrkjøring | «Hva skjer når du kjører dette?» lister stegene og hvordan det angres; der et ekte tørrkjøringsflagg finnes (`git push --dry-run`) står den som egen blokk. Statuskort som egentlig er en handling har knapp som hopper til kortet med kommandoen. | Selve kjøringen skal gå gjennom HAVEN Agent.app-broen (Q7), med forhåndsvisning av nøyaktig kommando, tørrkjøring der det finnes, og resultatet tilbake på oppgaven. Forklaringen er det samme overlayet som Q9 beskriver. |

**Hva «funksjonaliteten» er, målt mot artefaktet slik det står (`PDD_formaalsregister-som-graf_2026-09-11`, artefakt «Dommerbenken», db-samling `dommer`):** én oppgave om gangen med forrige/neste og prikkerad som viser tilstand per oppgave; kriteriet står synlig hele tiden; hver rad har tre knapper (ja / nei / usikker) som kan angres; full tekst per rad, ikke avkortet; ett valgfritt notatfelt per oppgave; framdrift som stolpe og telling; lagring per klikk uten sende-knapp, med synlig lagringsstatus; tid per oppgave målt automatisk. Kjetil brukte den i Safari, 15 oppgaver, 197 rader. Se `…/maaling/DOMMER_RUNDE1_FUNN.md` for hva runden avdekket — flaten virket, målingen bak den gjorde det ikke (ingen lokkeduer).

| Påstand / antatt kapabilitet | Audit | Kilde |
|---|---|---|
| Dette lar seg bygge som CellConfiguration-skeleton uten nye elementtyper | **retrieved, med to hull** — `List` med `flowElementSkeleton` (`Text` + tre `Button` med `keypath`/`payload`), `TextArea` for notat, `Text` for kriterium og framdrift, `Button` for forrige/neste. **Mangler:** ingen tidtaker-element (må være cellens jobb: tidsstempel på hver handling), og «trykket»-tilstand på knapp er bare `styleRole`-metadata, ikke garantert styling | `cellconfiguration-skeleton-authoring/references/schema-and-limits.md` |
| Lagring per klikk uten sende-knapp | **retrieved** — `Button` med `keypath` skriver til cellen; cellen eier dommene under eier-scopede Grants (`rwxs`). Ingen «send» trengs. Det som i artefaktet er en db-samling, er i HAVEN en celle | samme; A4 |
| En dom er en hendelse, ikke en tilstand | **stated** (Kjetil 2026-09-14: vekter skal justeres etter faktiske erfaringer) — dommen skal lagres som replaybar hendelse `(oppgave, kandidat, verdikt, sekunder, notat, tidsstempel)` i samme form som `RelationalWeightUpdateEvent`, slik at den kan flytte en vekt senere | `PDD_formaalsregister-som-graf_2026-09-11/FORMAALSSPEC.md` §6 Q8 |

> **2026-09-14, tillegg (ordrett):** Når vi bygger GUI for dette må det være lett å forstå både spørsmålet og hva eller hvordan man skal svare.

> **2026-09-15, tillegg (ordrett, fra statusgjennomgangen, om artefaktet «HAVEN Valgbenk»):** Funksjoneliteten i artefaktet for blokkert av mitt valg er veldig bra og noe vi må ha i workbench

Kontekst for auditen: «HAVEN Valgbenk» (Claude-artefakt, 2026-09-15) er en prototype av gren E3 (`…plangraf.mine-handlinger-utforbare`) og E4-mønsteret: tre baner (aktivt nå · venter på maskin/CI/Claude · blokkert av Kjetils valg), og per valg: spørsmål, alternativer med konsekvens, anbefaling fra Claude og/eller Astra (også når de er uenige), nøyaktig kommando (kopierbar), «Jeg har gjort dette» med bevisfelt. Valgene lagres i artefaktets database og leses av Claude, som handler på dem (samme dag: v-s1 → Codex-jobb; v-entity-core → HD-0079/80/81; v-formaal-g2 → G2 satt). Kilde for radene: Astras belagte gjennomgang (`HAVEN-Deploy/_handoff/STATUS/status-2026-09-15.json`) + Claudes GitHub-lesing. Det som mangler mot E3 er utføring på maskinen (Q7-broen) og at datakilden er `hd status` + PDD-filer direkte, ikke en JSON generert av en agent.

Dette er et **mål med verifier**, ikke et ønske. Den første dommerblanketten brøt nøyaktig dette — spørsmålet sto som statistikk («R+@10-forskjell på 0,15 … s_d=0,30») og svarformatet som notasjon (`1 3 ?4`, `3=u:sann-grunn`) — og Kjetil kunne ikke bruke den. Den omskrevne flaten satte kriteriet øverst i én setning og la svaret i knappeteksten («Ville endret noe» / «Nei» / «Usikker»), og han vurderte 197 rader uten instruksjon. Målet er altså allerede målt én gang i hver retning.

Goal-form for kandidatnoden (Book 23-skikk):
- **outcome:** en person som åpner flaten for første gang forstår spørsmålet og hvordan svaret gis, uten forklaring utenfor flaten.
- **successSignals:** (1) spørsmålet står i én setning, synlig hele tiden, og kan gjengis med egne ord av en førstegangsbruker; (2) svaralternativene *sier* svaret i klartekst — knappen heter det svaret betyr, ikke «ja»/«1»/«?»; (3) ingen notasjon, ingen kode og ingen statistikk i det dommeren ser; (4) første dom avgis innen ett minutt uten instruksjon.
- **verifier:** `test.gui.forstaa-uten-instruksjon` — en person som ikke har sett flaten før får den uten forklaring; måles: kan gjengi spørsmålet, avgir første svar, tid. Feiler hvis det trengs et spørsmål tilbake. Kjøres på hver ny vurderingsflate før den brukes til en runde.

Kandidat til §1 (ikke dekomponert; G1 venter): `purpose://candidate.utviklerbenk.dommerbenk` — en generell vurderingsflate der et menneske dømmer kandidater mot et synlig kriterium, én sak om gangen, og hver dom er en hendelse. Første bruk: fasit for formålsoppslag. Neste: G3-akseptanse rad for rad, og «ville denne lærdommen endret noe» ved P6.

### 0.1 Hva intensjonen består av

| # | Del | Type |
|---|---|---|
| S1 | Status på developer workbench nå | spørsmål |
| S2 | Grensen mot prosjekthåndtering og admin workbench, for en som er bidragsyter *og* scaffold-admin | spørsmål |
| I1 | Liste med løse idéer som kan settes i jobbkø *når Kjetil vil* | ønske |
| I2 | Idélisten som tre | ønske |
| I3 | Samme struktur vist som grafnoder | ønske |
| I4 | Oppgaven er utgangspunktet | ønske |
| I5 | Oppgaven kan være deloppgave i en større sammenheng | ønske |
| I6 | Oppgaven har kilder: kode i git, ekstern kunnskap, abonnement på Flow | ønske |
| I7 | Alle avhengigheter i en graf, for den som vurderer hvordan oppgaven best løses | ønske |
| I8 | Stegvis arbeidsflyt fra oppgaven: analyse, informasjonsinnhenting, drøfting, implementering, testing, commit/push, CI, deploy | ønske |

### 0.2 Audit av påstander og antatte kapabiliteter

| Påstand / antatt kapabilitet | Audit | Kilde |
|---|---|---|
| «Det er nevnt før» (idéer ned før de glemmes, køen startes når han vil) | **retrieved** — Kontrollrom-designet 25.08: «Masse ideer jeg må få ned før jeg glemmer dem», «Starte køen når jeg ønsker det»; tilstander `captured → drafting → frozen → queued → running → done`; frysing er menneskelig handling. Designforslag, ikke bygget | `CellScaffold::Documentation/ProjectControl/Kontrollrom_Design_2026-08-25.md` §1, §4, §5 |
| Det finnes én ting som heter «developer workbench» | **contradicted** — ingen flate eller celle har det navnet. Rollen er fordelt på fire ting: HAVEN Workbench 1.0 (prosjektceller), Admin workbench (skissen 04.09, operatør = «enhver som trenger utviklerverktøy»), arbeidskøen (HAVEN-Deploy + `_losen-queue`) og formålsmetoden (`purpose_dev.py`) | se §0.3 |
| En idéliste finnes | **retrieved, flat** — `IdeaTaskWorkspaceCell` holder idéer som Vault-notater med stadiet `inbox/project/review`, `captureIdea`, `promoteIdeaToTodo`, AI-analyse. Ingen forelder/barn | `CellScaffold::Sources/App/Cells/IdeaTaskWorkspace/IdeaTaskWorkspaceCell.swift` (nøkler `ideaWorkspace.*`, `stagePayload` ~l. 2174) |
| En tre-liste kan rendres | **retrieved (web), unavailable (Binding)** — `SkeletonList.childrenKeypath` + `expandedStateKeypath` (U2), utvid/kollaps lokalt uten rundtur. Finnes i et worktree laget fra main 09.09 sammen med beslutningsteksten fra doc-PR #229 → **utledet: merget i main**, ikke bekreftet mot GitHub; ukjent om i prod `3bdd622a`. Binding-renderer mangler | `CellScaffold::_wt-codex-ci-bolk-20260909/Public/js/skeleton-runtime.js` l. 1568, 6360–6563; `CellScaffold::Deliverables/PDD_admin-workbench_2026-09-04/TESTRESULT.md#u2u3` |
| Datamodellen kan holde et tre | **contradicted** — `WorkItemRecord` har ingen `parentRef`; deloppgaver er innebygde sjekklisteposter (`id, title, isDone, ownerRef`), ikke egne oppgaver | `CellScaffold::Sources/App/Cells/WorkItems/WorkItemCell.swift` l. 195–216, 317–356 |
| Noder kan vises som graf | **retrieved** — `GraphStoreCell`: `graph.import.workbench` (prosjekter, work items, idéer, todos → noder/kanter), `graph.subgraph`, `graph.subgraph.mermaid`, `graph.path.exists`, explorer med `radial-force`. Web-renderer: `Visualization kind: network|graph` | `CellScaffold::Sources/App/Cells/Graph/GraphStoreCell.swift` l. 1742–1780; `…/Public/js/skeleton-runtime.js` l. 2818, 3487 |
| GraphStoreCell tåler en kodegraf | **contradicted** — lagringen holder alt i minne og filtrerer lineært; greit for hundrevis av prosjektnoder, ikke for 25–50k symbolnoder. Egen backend er besluttet, ikke påbegynt | `CellProtocolDocuments::Deliverables/Kontekstgraf_For_Kodeagenter_Plan_2026-08-09.md` §2.2, §8 |
| En oppgave kan være deloppgave i en større sammenheng | **retrieved, delvis** — `WorkItemRecord.project`, `milestoneRef`, `relationships[]` (`depends-on`, `blocked-by`, `blocks`, `duplicate`, `related`). Ingen forelder. `HANDOFF-NODE` har `parentId` (design, ikke kode). HAVEN-Deploy-poster har `depends_on` (kode, i bruk) | `WorkItemCell.swift` l. 94–155; `CellScaffold::Documentation/ProjectControl/HANDOFF-NODE.md` §1; `HAVEN-Deploy::schema/task.schema.json` |
| Oppgaven kan referere kode i git | **retrieved, utypet** — `WorkItemRecord.repo` og `.cell` er enkeltstrenger; `evidence[].url` er fri. HAVEN-Deploy har `code_change {repo, branch, commit}` og typede `needs` (fil, skript, pin, secret, disk, image, koordinering, godkjenning). HANDOFF-NODE har `scope.repos/paths` og `inputs` med sha256 (design) | `WorkItemCell.swift` l. 317–340; `HAVEN-Deploy::queue/tasks/HD-0048.json`; `HANDOFF-NODE.md` §1 |
| Oppgaven kan referere ekstern kunnskap | **retrieved, utypet** — bare `evidence[].url` / `attachments[].url`. Kunnskapsceller finnes (`WebKnowledge`, `RAG`), men ingen oppgave peker på dem som kilde | `CellScaffold::Sources/App/Cells/{WebKnowledge,RAG}/` (katalog lest, innhold ikke) |
| Oppgaven kan ha «abonnement på Flow» som kilde | **unavailable** — ingen oppgavemodell har en flow-referanse. Flow finnes i CellProtocol; visionOS-PDD-en (i dag, G1 venter) foreslår `CellInteractionEvent` og `cell:///FlowTap`, som ville gjøre en slik referanse observerbar | `CellProtocolDocuments::Deliverables/PDD_haven-visionos_2026-09-10/FORMAALSSPEC.md` §1 (gren C) |
| Avhengighetsgraf per oppgave for den som vurderer | **unavailable** — delene finnes hver for seg (prosjektgraf, HAVEN-Deploy-indeks med `edges`, `Tools/CapabilityIndex/haven_capability_index.v1.json`), men ingenting slår dem sammen fra én oppgave. Kontekstgraf-planen §8b sier at repo-kontekst er påkrevd for kodeagenter | `HAVEN-Deploy::FORMAAL.md` F6; `CellScaffold::_wt-codex-ci-bolk-20260909/Tools/CapabilityIndex/` (fil finnes, ikke lest) |
| Stegvis arbeidsflyt kan uttrykkes | **retrieved, som metode og kø — ikke på oppgaven** — (a) Book 36 Formålssammensetning: `sequence` forbyr å *starte* et steg før forrige er målt grønt; kjøringslogg med `attempts`, `measurements`, `reports`; `purpose_dev.py gates` beregner en Composition-port. Status: «forslag, venter Kjetils ord»; commit-jobben er avvist to ganger. (b) HAVEN-Deploy: `PREPARING → PREFLIGHT_GREEN → DEPLOYING → COMMITTED_VERIFIED`, og F8-kjeden `implementert → origin/main → staging → prod`. (c) PDD-portene P0–P6 | `CellProtocolDocuments::Book/36_Purpose_Composition.md` §2–3; `…::Tools/PurposePackages/README.md`; `HAVEN-Deploy::FORMAAL.md` F1, F8 |
| Jobber kan settes i kø til Claude/Codex/celle | **retrieved, delvis i drift** — `_losen-queue` kjører Codex-jobber hver dag (fem vellykkede natt til 10.09). HAVEN-Deploy-arbeidskøen (dispatcher + utførere `codex`, `claude-local`, `cell`) er implementert, men G3 er **blocked**: alle tre ekte prøver feilet (HD-0013 EPERM, HD-0014 «Not logged in», HD-0015 lokal HTTP), og launchd-plisten er ikke installert (WP7, Kjetils) | `HAVEN::_losen-queue/logs/runner.log`; `CellProtocolDocuments::Deliverables/PDD_arbeidsko-ai-utforere_2026-09-07/{STATUS,ACCEPT}.md` |
| Rekkefølgen «push, commit» | **contradicted (git)** — commit må komme før push. Treet under bruker `commit → push` | — |
| «Admin i scaffoldet» gir tilgang til driftsverktøy | **retrieved, som vedtak** — admin workbench: operatør = enhver med Agreement, «ingen handling uten et klart definert grant» (05.09). Scaffold-admin-delegering: organisasjon er administrator per scaffold, delegerer i ett ledd (G1 08.09, G2 09.09, G3 venter). Grant-kontrakten er skrevet, koden ikke startet | `CellScaffold::Deliverables/PDD_admin-workbench_2026-09-04/contract/operator-grant.md`; `CellProtocolDocuments::Deliverables/PDD_scaffold-admin-delegering_2026-09-08/STATUS.md` |


**Tillegg til §0.2 — brief-audit for gren E, lest 2026-09-14.** `origin/main` nedenfor betyr de lokale revisjonene oppgitt over. Gamle auditrader og §0.3 er historikk fra 10.09; de er ikke ferske driftsmålinger. Dokumentkilder viser hva som er vedtatt eller rapportert, ikke at funksjonen kjører nå.

| ID / påstand | Audit | Kilde (repo-relativ sti:linje) |
|---|---|---|
| E-A1 · Referansen gir lanes, bokser, utførermerker og avhengighetspiler | **retrieved** — PNG-en er inspisert. HTML bruker faste posisjoner, fem lanes og manuelt skrevet kantliste; levert/kjører/din handling/senere er visuelle tilstander. Dette er en designreferanse, ingen levende PLAN-leser. PR-/portbokser må også få eksplisitt stegidentitet; de kan ikke utledes som nye oppgaver fra bildet. | `CellProtocolDocuments/Deliverables/PDD_butler-traadtre-og-widgetflate_2026-09-11/images/plan-v1.html:4`, `:21`, `:28`, `:57`, `:62`; samme mappes `images/plan-v1.png` |
| E-A2 · «Mine handlinger» har nødvendig kontekst | **retrieved** — tabellen sier når, hva, hvorfor bare Kjetil og hva som skjer etterpå; eksemplene er lokalt morgenskript, prod-ord og ja/nei til skjelettkapabiliteter. | `CellProtocolDocuments/Deliverables/PDD_butler-traadtre-og-widgetflate_2026-09-11/PLAN.md:11` og `:15` |
| E-A3 · Idéflate finnes i dagens kode | **retrieved** — konfigurasjonen heter **Idea Task Workspace**, kilde `cell:///IdeaTaskWorkspace` (`IdeaTaskWorkspaceCell`); bygger på Vault og Todo. Dette er konfigurasjons-/celleendepunkt, ingen påstått egen HTTP-side. | CellScaffold `origin/main`: `CellScaffold/Sources/App/Cells/ConfigurationCatalog/ConfigurationCatalogCell.swift:7513`; `CellScaffold/Sources/App/Cells/IdeaTaskWorkspace/IdeaTaskWorkspaceCell.swift:331`, `:644`, `:668` |
| E-A4 · Utviklerbenken har et konkret gjenbrukspunkt | **retrieved** — **HAVEN Workbench**, kilde `cell:///WorkItem`, integrerer **Agentkjøringer** med `cell:///AgentRun`. «Developer Workbench» er en betegnelse i kommentaren, ikke et eget katalog-/celleendepunkt. AgentRun-flaten er uttrykkelig lesende og mangler automatisk runtime-observer; den tilbyr ingen approve/dispatch. Den eldre påstanden «ingen utviklerbenk» er derfor for vid som nåbeskrivelse. | CellScaffold `origin/main`: `CellScaffold/Sources/App/Cells/ConfigurationCatalog/ConfigurationCatalogCell.swift:7872`, `:8194`; `CellScaffold/Sources/App/Cells/WorkItems/AgentRunWorkbenchConfiguration.swift:6`, `:54`, `:78`; `CellScaffold/Sources/App/Cells/WorkItems/AgentRunCell.swift:19` |
| E-A5 · Admin workbench er ett navngitt endepunkt | **contradicted** — koden har **Admin Control Plane Overview**, **Admin Operations Workspace**, **Admin Security & Access Workspace**, **Admin Product Administration**, **Admin Copilot Workspace**. Kildene er henholdsvis `AdminOverview`, `AdminHostMetrics`, `AdminSecurityPolicy`, `cell:///ConfigurationCatalog`, `AdminOverview`. Rutede navn blir `cell:///<navn>` lokalt eller `cell://<host[:port]>/<navn>` i remote-modus; vertsnavn er ikke målt. Navigasjonen har også `/admin/development`. Ikke funnet et separat katalogendepunkt kalt Admin Workbench i det avgrensede søket under `Sources/App/Cells`. | CellScaffold `origin/main`: `CellScaffold/Sources/App/Cells/Admin/AdminWorkspaceConfigurationFactory.swift:14`, `:30`, `:45`, `:123`, `:256`, `:355`, `:407`; `CellScaffold/Sources/ScaffoldKit/AdminControlPlaneRouting.swift:216` |
| E-A6 · hd vet oppgaveidentitet, eierskap, avhengigheter og status | **retrieved** — `hd.py` er inngang til `hdlib.cli`; oppgaveposten har `task_id`, fritekst-`purpose`, `owner`, `executed_by`, repo/branch/commit, `depends_on`, `needs`, `posts` og status. `task next` velger eldste tilgjengelige post med behov og avhengigheter kontrollert. Dette er ingen normalisert PDD-arbeidspakke med purposeRefs og tester per WP. | `HAVEN-Deploy/tools/hd.py:8`, `:15`; `HAVEN-Deploy/tools/hdlib/core.py:344`; `HAVEN-Deploy/tools/hdlib/cli.py:206`, `:223`; `HAVEN-Deploy/AGENTS.md:14` |
| E-A7 · hd-status er allerede en projeksjon med bevis | **retrieved** — status gir kø/forkastet/utført, eier, utfører, blokkeringer og bevisstier; utført uten bevis markeres. CLI nekter ny `COMMITTED_VERIFIED` uten `--evidence`, og arbeidsjobber kan bare startes/verifiseres av dispatcheren. Kontrollen av en oppgitt bevissti alene dokumenterer ikke at beviset gjelder riktig artefakt eller PDD-steg; E må gjenbruke C sitt strengere beviskrav. `ROLLED_BACK_VERIFIED` er avsluttet rollback, aldri grønn «levert». | `HAVEN-Deploy/tools/hdlib/status.py:74`, `:100`, `:147`; `HAVEN-Deploy/tools/hdlib/cli.py:63`, `:73`, `:102`; `HAVEN-Deploy/AGENTS.md:24`, `HAVEN-Deploy/AGENTS.md:31` |
| E-A8 · PLAN-formatet er ensartet | **contradicted** — Butler og correspondence bruker `### WP-*` med purposeRef/Utfører/Gjør/Tester/Leverer; agent-menylinje bruker tabell med forkortede bladnavn, «Hva den lager», test og utfører, med felles standardutfører. Alle har WP-identitet, arbeid, utfører, tester og rekkefølge, men avhengigheter er også ASCII/prosa, flere formål deler WP, og artefaktfelt mangler for noen tabellrader. Ikke én WP per blad i det faktiske materialet. | `CellProtocolDocuments/Deliverables/PDD_butler-traadtre-og-widgetflate_2026-09-11/PLAN.md:48`, `:62`, `:125`; `CellProtocolDocuments/Deliverables/PDD_correspondence-varsel-hendelsesbasert_2026-09-12/PLAN.md:54`, `:68`; `CellProtocolDocuments/Deliverables/PDD_agent-menylinje-og-varsler_2026-09-09/PLAN.md:8`, `:12`, `:27` |
| E-A9 · Status kan leses fra første statusord i PLAN | **contradicted** — correspondence-PLAN sier «G2 venter» mens STATUS-porten er godkjent; agent-menylinje-ACCEPT sier porter venter mens STATUS har Kjetils godkjenning. Butler mangler `TESTRESULT.md` ved denne lesningen (direkte mappeinventar); grafen må vise «bevis mangler», ikke gjøre grønt fra bilde/plan. | `CellProtocolDocuments/Deliverables/PDD_correspondence-varsel-hendelsesbasert_2026-09-12/PLAN.md:3` mot `STATUS.md:9`; `CellProtocolDocuments/Deliverables/PDD_agent-menylinje-og-varsler_2026-09-09/ACCEPT.md:3` mot `STATUS.md:7`; `CellProtocolDocuments/Deliverables/PDD_butler-traadtre-og-widgetflate_2026-09-11/PLAN.md:53` refererer fremtidig `TESTRESULT.md#build` |
| E-A10 · Skeleton har et grafuttrykk | **retrieved** — `SkeletonElement.Visualization` med fri `kind`, `spec: ValueType`, data-/state-keypath og én action-keypath finnes. Fri JSON betyr ikke at vilkårlige felt rendres. Oppgitt linje 1240 treffer nå `SkeletonHStack` i arbeidskopien; korrekt symbol på lest `origin/main` er linje 2655/2804. | CellProtocol `origin/main`: `CellProtocol/Sources/CellBase/Skeleton/SkeletonDescription.swift:2655`, `:2804`; arbeidskopiens samme sti `:1240` kun kontrollert for å forklare linjeforskyvningen |
| E-A11 · Dagens webgraf kan rendre referansen komplett | **contradicted** — `network`/`graph` går til grafutforskeren: piler, fargede prikker med noen etiketter, nodeklikk via felles actionKeypath; eksplisitte x/y-posisjoner finnes. Ingen lane-layout, arbeidskortmal med utfører/status/bevis eller separate Utfør/Forklar-knapper i hver node i denne rendererfunksjonen. Trenger dokumentert utvidelse av renderer-/skjelettkontrakten; ikke nødvendigvis ny elementtype. Oppgitt linje 3041 ligger nå i kalenderdelen. | CellScaffold `origin/main`: `CellScaffold/Public/js/skeleton-runtime.js:2165`, `:2784`, `:2861`, `:3045`, `:3530`, `:3617`, `:3660`, `:4336` |
| E-A12 · Samme plangraf er bevist i appen | **unavailable** — native kode har `network`/`graph` og node-action, men denne runden har ingen kjørende Binding-måling av lanes/arbeidskort/knapper. Paritet blir egen avhengighet og test; webstøtte er ikke appbevis. | CellProtocol `origin/main`: `CellProtocol/Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/Suggestion/SkeletonView.swift:2567` |
| E-A13 · HAVEN Agent.app-broen kan gjenbrukes til enhver maskinhandling nå | **unavailable** — menylinje-PDD beskriver kontrollbro og svar via den reelle ReviewCommandService. Lagret HTTP-prøve viser `accepted:false` for ukjent sak og for handling uten svarvei: dette beviser ruting/avvisning, ikke vellykket kjøring av vilkårlig skript. HD-0069 står `PREPARING`, med usatisferte behov for varselsamtykke/restart og en `pending` KJØR-SELV-post. Ingen målt vei plangraf → browser/app → godkjent lokal kjøring → bevis tilbake er funnet i disse kildene. | `CellProtocolDocuments/Deliverables/PDD_agent-menylinje-og-varsler_2026-09-09/PLAN.md:17`; samme mappes `TESTRESULT.md:193`, `:196`; `HAVEN-Deploy/queue/tasks/HD-0069.json:23`, `:29`, `:39`, `:43`, `:50` |
| E-A14 · HD-0069 leverer allerede hendelsesbro og faktisk varsel | **contradicted** — hendelsesbroen er beskrevet som WP-M0/M1/M2 med egen identitet og celle `agent/challenges`; correspondence-STATUS viser bare baseline og skrevet WP-S1, G3 venter. Menylinje-STATUS har G3 med forbehold, mens ACCEPT L6 fortsatt er «ikke verifisert». Verken port eller grønn enhetstest er bevis for dagens maskinbro. | `CellProtocolDocuments/Deliverables/PDD_correspondence-varsel-hendelsesbasert_2026-09-12/PLAN.md:82`, `:89`, `:96`; samme mappes `STATUS.md:10`, `:28`; `CellProtocolDocuments/Deliverables/PDD_agent-menylinje-og-varsler_2026-09-09/STATUS.md:10`; samme mappes `ACCEPT.md:21` |
| E-A15 · Å eie oppgaven gir grant til utførelse | **contradicted** — adminflatene erklærer at myndighet ligger i hver referert celles Agreement; hd skiller eier og utfører og reserverer vertskjøring for Kjetil. Den konkrete grant- og svarveien fra E-boksen er **unavailable** i auditkildene. Navnemerket «Kjetil» er aldri autorisasjon. | CellScaffold `origin/main`: `CellScaffold/Sources/App/Cells/Admin/AdminWorkspaceConfigurationFactory.swift:7`; `HAVEN-Deploy/tools/hdlib/core.py:350`; `HAVEN-Deploy/AGENTS.md:7` |
| E-A16 · Forklaring kan gjenbruke Butler B som ferdig funksjon | **retrieved** som mål/vedtak, **unavailable** som verifisert integrasjon — B definerer løsrivbart, levende og bruker-eid element i Portholens CellConfiguration. E bruker festingen, men forklaringskilden er valgt planpunkt og går aldri via chatlogg. Mønsteret er ingen dokumentasjon av ferdig forklarings-API. | `CellProtocolDocuments/Deliverables/PDD_butler-traadtre-og-widgetflate_2026-09-11/FORMAALSSPEC.md:77`, `:85`, `:88`; samme mappes `PLAN.md:125`, `:139`, `:174` |
| E-A17 · E skal flytte lokal hd-kø og utførelse til staging | **contradicted** — `HAVEN-Deploy/AGENTS.md` har et eldre absolutt forbud mot utviklerverktøy i server/HavenAgentD/HAVEN-appen. Senere Kjetil-retning ber om utviklerarbeidsflyt i adminflaten og her om web/app/staging. Denne bestillingen styrer E-visningen; lokal kø og utførelsesmyndighet blir fortsatt lokale. Verifisert tilgangsbegrenset projeksjon er avhengighet, ikke rå Mac-filer eller shell på staging. | `HAVEN-Deploy/AGENTS.md:7`; `CellProtocolDocuments/Deliverables/PDD_correspondence-varsel-hendelsesbasert_2026-09-12/STATUS.md:27`; Kjetils ordrette tillegg 14.09 i denne §0 |

Ingenting `recalled` er lastbærende.

### 0.3 Nåtilstand 2026-09-10 (svar på S1)

Kortversjon: **byggeklossene finnes og flere er gode, men det finnes ingen utviklerbenk å sitte ved.** Datacellene
er i main, tre-listen er levert på web, køen kjører Codex-jobber (fem vellykkede natt til 10.09), og formålsmetoden har fått sekvenser.
Det som mangler er det som binder dem: en oppgave som vet hvor den kom fra, hva den hviler på og hvor i
arbeidsflyten den er — og en flate som viser det.

| Lag | Hva | Status | Evidens |
|---|---|---|---|
| **Prosjektdata** (Workbench 1.0) | `WorkItemCell` skjema 0.5 (filter, eksplisitt Open, drawer, status/prioritet, relasjoner, evidens, aktivitet), `ProjectPortfolioCell`, `IdeaTaskWorkspaceCell`, `TodoCell`, `GraphStoreCell`, `GitHubWorkSyncCell` | i kode. 0.5-fiksen verifisert lokalt 30.08, «ikke deployet» da; om den er i prod nå: **ikke målt** | `CellScaffold::Documentation/ProjectControl/Work_Item_Tool_Functionality_Research_And_Purpose_2026-08-30.md` |
| | WO-1 MCP-bro (agenter skriver oppgaver via celler, ikke seed-JSON) | **ikke levert** — `.mcp.json` har bare `codex-local` og `haven-docs`, både i hovedtreet og i worktree fra 09.09 | `CellScaffold::.mcp.json` |
| | WO-2 GitHub som evidens | **ikke levert** — 0 treff på `URLSession`/`HTTPClient`/`api.github.com` i `GitHubWorkSyncCell` | `CellScaffold::Sources/App/Cells/WorkItems/GitHubWorkSyncCell.swift` |
| | WO-3/4/5/6 | ingen leveranse funnet; README står fortsatt READY/BLOCKED | `CellScaffold::Documentation/Operations/workbench-1.0/README.md` |
| **Operatørflaten** (admin workbench, skissen 04.09) | G1, G1-GUI, G2 godkjent 05.09 | godkjent | `…/PDD_admin-workbench_2026-09-04/STATUS.md` |
| | U2 tre-liste + U3 followTail (web + skjema) | levert (PR CP #34, CS #226, doc #229); **utledet merget** | se §0.2 |
| | Binding-renderer for U2/U3 | mangler | `…/TESTRESULT.md#u2u3` |
| | U1 `ConfigurationSlot` (verktøy lastet inn i fokusområdet) | ikke startet — krever barnesesjon på server og barnerenderer på klient | `…/TESTRESULT.md#u1` |
| | D1 operatør-grant | kontrakt skrevet, kode ikke startet | `…/contract/operator-grant.md` |
| | A1/A2 i HavenAgentD (avbryt + gate på `LocalTaskDefinition`) | Codex-jobben 08.09 leste kildene og døde uten kode | `CellScaffold::_pdd-admin-workbench-20260905/agentd/status.txt` |
| | Skallet P0–P7 | ikke startet | `…/PLAN.md` |
| **Kø og utførelse** | `_losen-queue` (launchd, `codex exec`, én jobb om gangen) | **i drift** — det som faktisk kjører | `HAVEN::_losen-queue/logs/runner.log` |
| | HAVEN-Deploy-arbeidskøen (dispatcher + `codex`/`claude-local`/`cell`) | implementert, 88 tester; **G3 blocked** (tre ekte prøver feilet, plist ikke installert) | `…/PDD_arbeidsko-ai-utforere_2026-09-07/ACCEPT.md` |
| | HAVEN-Deploy-køen som helhet (09.09 23:37Z) | 36 i kø, 5 utført, 6 forkastet; **109 endringspakker verken i main eller synlig avvist** (G8 blokkerer); staging = prod = `3bdd622a`, main `5e64c296` ikke ute | `HAVEN-Deploy::index/status.json` |
| | Menylinje-appen «hva venter på meg» (HavenAgentD) | implementert på gren, 227 tester, kjører på maskinen din; G1/G1-GUI/G3 venter på deg | `CellProtocolDocuments::Deliverables/PDD_agent-menylinje-og-varsler_2026-09-09/STATUS.md` |
| **Metoden som arbeidsflyt** | `purpose_dev.py` (lookup/new/validate/gates/lesson), 42 lærdommer (én lagt til i denne runden) | i drift | `CellProtocolDocuments::Tools/PurposePackages/` |
| | Book 36 sekvenser/porter | skrevet og implementert 09.09; **venter ditt ord**; commit avvist to ganger | `CellProtocolDocuments::Book/36_Purpose_Composition.md` |
| **Graf** | Prosjektgraf (`GraphStoreCell`) + web-grafvisning | i kode | se §0.2 |
| | Kontekstgraf for kodeagenter | omfang besluttet 09.08, ikke påbegynt | `CellProtocolDocuments::Deliverables/Kontekstgraf_For_Kodeagenter_Plan_2026-08-09.md` |

### 0.4 Grensen (svar på S2) — forslag: én benk, tre linser

Glidningen du kjenner er riktig, og den er ikke en feil i avgrensningen — det er samme arbeid sett fra tre høyder.
Forslaget er å slutte å skille dem som *flater* og i stedet skille dem som *linser* på samme valgte ting:

| Linse | Svarer på | Eier | Hvem ser den |
|---|---|---|---|
| **Prosjekt** | hva og hvorfor — idétre, oppgaver, formål, avhengigheter mellom oppgaver | Workbench (intensjon, prosjektmening, historikk) | alle med tilgang til prosjektet |
| **Utvikler** | hvordan — oppgavens kilder, avhengighetsgraf, stegvis arbeidsflyt, jobber i kø | Workbench (plan) + kø (utførelse) | bidragsytere |
| **Drift** | hvor og i hvilken tilstand — scaffold/repo/branch, prosesser, CI, deploy, logger | AgentD og HAVEN-Deploy (kjøring, policy) | den som har operatør-grant for scaffoldet |

Tre regler som allerede er vedtatt gjør dette mulig uten ny arkitektur:
- *Valgt kontekst binder alt* (admin workbench, vedtak 04.09).
- *Tilgang er grant, ikke rolle*: operatør = enhver med Agreement; ingen handling uten grant (04.09 og 05.09).
  Du som bidragsyter *og* scaffold-admin ser alle tre linsene; en bidragsyter uten admin-grant ser de to første.
- *AgentD eier kjøring, Workbench eier intensjon; ved konflikt vinner AgentD* (Workbench 1.0, 25.08).

### 0.5 Funn underveis (ikke en del av bestillingen, men de treffer den)

1. **Køen tok en halvskrevet jobb i dag.** `formaalskomposisjon-fullfor-commit-20260910-1020.job` ble skrevet
   10:18:25Z, runneren avviste den 10:18:38Z med «mangler promptfil», og promptfilen kom 10:18:40Z. Den ligger nå
   foreldreløs i `_losen-queue/inbox/`, og runneren ser den aldri igjen (den leser bare `*.job`). En tidligere
   versjon av jobben (`…-20260909-1330`) ble avvist 09.09 22:38Z for leveransesti utenfor cwd. Forebygging: skriv promptfilen først og `.job` sist —
   samme regel som `HavenAgentD::Docs/AgentJobs.md` har for `job.json`. Registrert som lærdom.
2. **109 endringspakker uten beslutning** er den største enkelthindringen for «deploy» som siste steg i en
   arbeidsflyt: en sekvens som ender i deploy blir aldri grønn så lenge main ikke kommer ut.

---

## 1. Formålstre

Klassifisert først: roten hører under `purpose://project-work.work-items` (Book 23, active), med
`purpose://digital-work.coordinate` som facett. Alle nye noder er `purpose://candidate.utviklerbenk.*`, navngitt her.
Sammensetning følger Book 36 (ingen default). Treet ligger også maskinlesbart i `PURPOSE_COMPOSITION.json`.

### Rot

| purposeRef | Tittel | Sammensetning | Goal (outcome) | Verifier |
|---|---|---|---|---|
| `…utviklerbenk.oppgaven-forst` | Oppgaven først: fra løs idé til levert endring uten å miste tråden | `allOf` (A, B, C, D, E) | For en vilkårlig oppgave kan Kjetil, fra én flate og uten å lese chat eller loggfiler: (1) se idéen den kom fra og hva den er del av, (2) se alt den må forholde seg til, (3) se hvor i arbeidsflyten den er og hvem som har neste steg, (4) sette neste steg i kø, (5) lese plangrafen, åpne en boks, starte egen tillatt handling og få forklaring ved siden av. | `test.benk.walkthrough-per-rolle` — simulert bruker per rolle (bidragsyter, bidragsyter + scaffold-admin, uten grant) gjør (1)–(4) og rapporterer hvor tilgang hindret, og om hindringen var riktig; `test.plangraf.staging-brukersti` dekker (5) |

### A — Idéer fanges og struktureres (I1, I2, I3)

| purposeRef | Tittel | Sammensetning | Goal (outcome) | Verifier | Gjenbruker |
|---|---|---|---|---|---|
| `…utviklerbenk.ideer` | Idéer i tre og graf | `allOf` | Alle blad under grønne | — | — |
| `…ideer.fangst` | Fangst uten beslutninger | blad | Fritekst + tidspunkt + opphav lagres med høyst to handlinger og null påkrevde felt; råteksten kan ikke overskrives etter lagring — berikelse er lag over | `test.idea.capture-two-actions`, `test.idea.raw-immutable` | Kontrollrom §4; `workItem.capture` |
| `…ideer.tre` | Idéer har struktur | blad | En idé kan få forelder, flyttes med hele undertreet og rendres som tre med utvid/kollaps; sykluser avvises; samme tre i web og Binding | `test.tree.move-keeps-subtree`, `test.tree.rejects-cycle`, paritetsrad U2 Binding | U2 `childrenKeypath` (web) |
| `…ideer.graf-er-samme-data` | Grafen er en annen visning, ikke en annen lagring | blad | Én grafnode per tre-node; valg i grafen er valg i treet og omvendt; kanter = forelder + relasjoner | `test.graph.node-count-equals-tree`, `test.graph.selection-shared` | `graph.import.workbench`, `Visualization kind: network` |
| `…ideer.frys-og-kø-er-kjetils` | Idé blir oppgave og går i kø når Kjetil vil | blad | «Frys» gjør idéen til oppgave uten kopi (samme node, ny tilstand, råteksten beholdes); «sett i kø» legger valgt steg i arbeidskøen. Begge krever operatørens handling; en agent-requester avvises | `test.idea.freeze-human-only`, `test.queue.enqueue-creates-post` | Kontrollrom `frozen`; `hd task new` |
| `…ideer.agentforslag-i-eget-lag` | *Skal ikke:* agenter skriver rett inn i treet Kjetil leser som sannhet | blad · prohibited | Agentskrevne noder vises i et forslagslag, teller ikke i tellere og blir først del av treet ved bekreftelse | `test.idea.agent-writes-are-proposals` | Kontrollrom felle 2 |

### B — Oppgaven kjenner sin sammenheng (I4, I5, I6, I7)

| purposeRef | Tittel | Sammensetning | Goal (outcome) | Verifier | Gjenbruker |
|---|---|---|---|---|---|
| `…utviklerbenk.oppgave-i-kontekst` | Oppgaven i sin sammenheng | `allOf` | Alle blad under grønne | — | — |
| `…oppgave.plass-i-helheten` | Deloppgave i en større sammenheng | blad | Hver oppgave har nøyaktig én forelder (idé, oppgave eller prosjekt) eller er rot; deloppgaver er egne oppgaver; dagens sjekkliste-`subtasks` migreres uten tap; `purposeRef` løses mot Book 23/pakker, ellers merket `candidate` | `test.task.single-parent`, `test.task.subtask-migration-lossless`, `test.task.purposeref-resolves` | `WorkItemRecord` 0.5 → 0.6 |
| `…oppgave.typede-kilder` | Kilder som typede referanser | blad | Kildene har type: `git {repo, ref, sti, symbol?, sha256?}`, `kunnskap {url \| Book-kapittel \| RAG-kilde, hentetAt}`, `flow {endpoint, topic}`, `celle {endpoint, keypath}`, `oppgave {id, relasjon}`, `behov` (HAVEN-Deploy `needs`). Hver har `lesbar: ja \| nei \| ukjent` med påkrevd grunn når den ikke er `ja`, sjekket maskinelt der det går | `test.source.types-validate`, `test.source.resolvability-honest` | `repo`/`cell`/`evidence` (strenger i dag); HD `needs`; HANDOFF-NODE `inputs` |
| `…oppgave.avhengighetsgraf` | Grafen den som vurderer trenger | blad | Fra en oppgave: kilder, blokkerende og avhengige oppgaver, celler og keypaths, flows, formål og lærdommer som matcher tagger, til valgt dybde. Uleselige noder vises som noder med tilstand, aldri som fravær. Samme utsnitt kan gis en agent som kontekst | `test.depgraph.complete-for-fixture`, `test.depgraph.unreadable-visible`, `test.depgraph.same-context-for-agent` | `graph.subgraph`; Kontekstgraf §8b; `purpose_dev.py lookup` |
| `…oppgave.graf-er-projeksjon` | Grafen kan bygges på nytt | blad | Grafen slettes og bygges fra oppgave- og kildedata med identisk resultat | `test.depgraph.rebuild-identical` | HAVEN-Deploy F6; AgentRunCell-regelen |
| `…oppgave.referanse-er-ikke-tilgang` | *Skal ikke:* en referanse gir innsyn | blad · prohibited | En kilde eller grafnode viser aldri innhold requester ikke har grant til; kryptert innhold vises som referanse | `test.cell.auth-negative` (på `graph.subgraph` og kildeoppslag) | lesson.purpose-never-grants-rights |

### C — Stegvis arbeidsflyt fra oppgaven (I8)

| purposeRef | Tittel | Sammensetning | Goal (outcome) | Verifier | Gjenbruker |
|---|---|---|---|---|---|
| `…utviklerbenk.arbeidsflyt` | Arbeidsflyten er en del av oppgaven | `allOf` | Alle blad under grønne | — | — |
| `…arbeidsflyt.sekvens` | Stegene er en sekvens, ikke en huskeliste | blad | Hver oppgave får en Book 36-`sequence` fra en mal (tabellen under). Et steg kan ikke *startes* før forrige er målt grønt; `purpose_dev.py gates` viser arbeidsflytens tilstand. Maler kan utelate steg (research slutter ved beslutning); en kjøring kan ikke hoppe over | `test.flow.sequence-enforced`, `test.flow.templates-validate` | Book 36 §3.2; `purpose_composition.py` |
| `…arbeidsflyt.steg-har-bevis` | Grønt krever bevis | blad | Hver måling har `evidenceRef` av riktig type for steget (tabellen); grønt uten bevis avvises | `test.flow.green-requires-evidence` | Book 36 kjøringslogg |
| `…arbeidsflyt.utforer-per-steg` | Riktig utfører per steg | blad | Hvert steg har utfører (`kjetil`, `claude-local`, `claude-cloud`, `codex`, `celle`, `ci`) og sandkasse; steg bare Kjetil kan gjøre er merket; deploy- og docker-steg har aldri `codex` | `test.flow.executor-rules` | HD G1.3; lesson.codex-sandbox-cannot-reach-docker |
| `…arbeidsflyt.en-ko` | Én kø, status tilbake på steget | blad | «Sett i kø» skriver til HAVEN-Deploy-arbeidskøen (vedtatt 07.09). `job.started`/`job.finished` oppdaterer stegets måling innen ett dispatcher-intervall + 60 s | `test.queue.round-trip` (ekte, én per utfører) | `tools/dispatch.py` |
| `…arbeidsflyt.menneskelige-porter` | Portene er Kjetils | blad | Beslutning, merge og prod-deploy krever signert handling fra operatør; ingen jobb kan åpne en port eller legge en jobb med videre sandkasse enn sin egen | `test.flow.gate-human-only`, `test.ko.no-escalation` | PDD-portene; arbeidskø `no-self-escalation` |
| `…arbeidsflyt.feil-blir-laerdom` | Gjentatt feil blir lærdom | blad | Samme fingeravtrykk to ganger på et steg → `HANDOFF_REQUIRED` + lærdom innen 48 t | `test.ko.lesson` | HAVEN-Deploy F7 |

**Standardmalen** (I8 i din rekkefølge; tre steg merket *lagt til* er forslag fra HAVEN-Deploy F8 og lærdommene — de trenger ditt ja):

| # | Steg | Grønt når | Bevis | Standard utfører |
|---|---|---|---|---|
| 1 | Analyse | formålet er skrevet og hver påstand i oppgaven er auditert | FORMAALSSPEC §0 | claude |
| 2 | Informasjonsinnhenting | alle kilder har `lesbar` satt, og avhengighetsgrafen er generert | graf-utsnitt + kildetabell | claude / codex (read-only) |
| 3 | Drøfting | hver rotpåstand har motargument behandlet; åpne spørsmål besvart eller parkert med grunn | påstandsregister | claude + rådgiverpanel |
| 3b | *Beslutning (lagt til)* | Kjetils ord på formål, og på bilde for GUI | STATUS.md G1/G1-GUI | **kjetil** |
| 4 | Implementering | endringen er skrevet i eget worktree fra målt revisjon og bygger — rapporteres «skrevet, ikke verifisert» | diff + byggelogg | codex / claude-local |
| 5 | Testing | bygg, nye tester og full regresjon mot målt baseline, i rent worktree | TESTRESULT.md | codex (detached) |
| 6 | Commit | branchen står på andre commits enn basen (`rev-parse branch ≠ base`) | commit-sha | codex |
| 7 | Push | origin har samme sha | `ls-remote` | codex |
| 8 | CI | kjøringen for sha er grønn, lest fra jobb-endepunktet | run-id | ci |
| 8b | *PR og merge (lagt til)* | squash-merget til main | merge-sha | **kjetil** |
| 9 | Deploy | staging, deretter prod, kjører main-sha ifølge `/health/build` | receipt.json | **kjetil** (verten) |
| 9b | *Verifisert i miljø (lagt til)* | brukerstien er klikket gjennom med ekte identitet | smoke-artefakt | claude / codex |

### D — Én benk, tre linser (S2)

| purposeRef | Tittel | Sammensetning | Goal (outcome) | Verifier | Gjenbruker |
|---|---|---|---|---|---|
| `…utviklerbenk.tre-linser` | Én benk, tre linser | `allOf` | Alle blad under grønne | — | — |
| `…linser.valgt-binder` | Valgt idé eller oppgave binder alle linser | blad | Bytte linse beholder valget; bytte valg oppdaterer alle linser | `test.gui.context-propagation` | admin workbench P0 |
| `…linser.tilgang-fra-grant` | Linsene åpnes av grants | blad | Hva som vises og kan gjøres kommer fra Agreement-grants; uten operatør-grant finnes ingen skrivende driftsverktøy i flaten, og tomt er et gyldig svar | `test.agreement.operator-scopes` + simulert bruker per rolle | `contract/operator-grant.md` |
| `…linser.netto-null-flater` | Ingen niende flate | blad | Benken erstatter overlappende innganger (idéfangst i IdeaTaskWorkspace, Todo, Work Item Tracker som egen inngang) som lagrede visninger; antall toppnivåinnganger for arbeid øker ikke | `test.catalog.entry-count-not-increased` | Kontrollrom felle 3 |

### E — Plangrafen er visning og handlingsflate over oppgaven (tillegg 13.–14.09)

Klassifisering: gjenbruk `purpose://project-work.work-items`, `purpose://project-work.current-status-and-outstanding`
og `purpose://gui.quality.functional-accessible` fra Book 23. Lokale blad under følger den eksisterende roten;
alle har status `candidate`. E innfører ingen planlagring eller kø: planen er oppgaven med arbeidsflyt fra C,
og grafen er projeksjonen fra B. Filkilde er anbefalt første leveranse (Q8), ikke vedtatt cellemigrering.

`purpose://candidate.utviklerbenk.plangraf` har forelder `…utviklerbenk.oppgaven-forst`, `composition.kind: allOf`.
Goal: `goal.candidate.utviklerbenk.plangraf`, lifecycle `continuous`; outcome: alle seks E-blad oppfylles fra den
samme valgte oppgaven. SuccessSignals: hver E-verifier er målt grønn med bevis. Verifier: §5 E-testene samlet.
Forkortelsen `…plangraf.*` nedenfor betyr `purpose://candidate.utviklerbenk.plangraf.*`.

Lesemerknad 28.09: «alle seks E-blad» er målgrunnlaget fra iterasjon 2, E1–E6. E7 og E8 nedenfor er
senere kandidatinntak. Samlet mål og testdekning må avstemmes i videre P1; innføring i treet utvider
ikke tidligere portgodkjenninger.

#### E1 · `…plangraf.visning` — Plangrafen viser planen i web og app

- Forelder: `…utviklerbenk.plangraf`; status: `candidate`.
- Goal: `goal.candidate.utviklerbenk.plangraf.visning`; lifecycle: `continuous`.
- Outcome: Kjetil ser planen som lanes per gren, én boks per arbeidspakke, navngitt utfører, status og piler for eksplisitte avhengigheter fra samme PDD-kildesett i web og Binding.
- SuccessSignals:
  - Samme normaliserte kildeversjon gir identiske WP-ID-er, lanes, utførere og kanter i web (1900×1100) og app (780×1688); appen kan panorere uten å miste innhold eller handlinger.
  - Levert, kjører, din handling og senere har både farge og tekst. Blokkert, feil og ukjent kilde er synlige med grunn. Manglende PLAN/TESTRESULT gir erklært fravær, aldri oppdiktede bokser eller grønt.
  - Mine handlinger er et filter på samme bokser; hver viser når, hva, hvorfor bare Kjetil og hva som skjer etterpå. Planlagt tidspunkt tolkes ikke som faktisk startet.
- Verifier: `test.plangraf.visning-paritet`, `test.plangraf.plan-normalisering` (hvordan og bevis i §5).
- Gjenbruk: `…oppgave.graf-er-projeksjon`, `…arbeidsflyt.utforer-per-steg`.

#### E2 · `…plangraf.drilldown` — En boks åpner arbeidets detaljer

- Forelder: `…utviklerbenk.plangraf`; status: `candidate`.
- Goal: `goal.candidate.utviklerbenk.plangraf.drilldown`; lifecycle: `continuous`.
- Outcome: Kjetil åpner en boks og forstår hva arbeidet gjelder, hvem som eier det og hvilket bevis statusen bygger på.
- SuccessSignals:
  - Detaljene viser WP-ID, purposeRef(s), gjør, tester, artefakter, avhengigheter, eier og utfører som separate felt, samt status med kildehenvisning og bevis.
  - Hver opplysning peker på fil:linje/anker og kildeversjon. Manglende eier eller tvetydig kort purposeRef vises som ukjent med grunn, ikke arvet fra utfører uten eksplisitt regel.
  - Tilbake til grafen beholder valgt boks og utsnitt i begge klienter; dokumentlenker og handlinger nås med tastatur.
- Verifier: `test.plangraf.drilldown-kilder` (hvordan og bevis i §5).
- Gjenbruk: `…oppgave.plass-i-helheten`, `…oppgave.typede-kilder`.

#### E3 · `…plangraf.mine-handlinger-utforbare` — Mine handlinger kan startes fra boksen

- Forelder: `…utviklerbenk.plangraf`; status: `candidate`.
- Goal: `goal.candidate.utviklerbenk.plangraf.mine-handlinger-utforbare`; lifecycle: `continuous`.
- Outcome: En boks med Kjetil som utfører tilbyr den konkrete handlingen, og trykk utfører eller starter den via en dokumentert svarvei med bevis tilbake til kilden.
- SuccessSignals:
  - Åpne PR åpner rett URL; det fullfører bare et eventuelt navigasjonssteg. Opprette PR eller registrere «godkjent» krever autentisert tjeneste, konkret mål/revisjon, grant og kvittering. Mangler svarvei, er knappen deaktivert med grunn.
  - KJØR-SELV-skript og deploy starter bare gjennom verifisert HAVEN Agent.app/AgentD-adapter på Kjetils maskin, med forhåndsdefinert handling, tillatt omfang og Kjetils eksplisitte handling. Nettleseren kjører ikke lokal shell, og staging overtar ikke kjøring.
  - Før trykk vises når/hva/hvorfor bare deg/etterpå, mål og sidevirkning; etter trykk vises startet med kjørings-ID, deretter levert med riktig artefaktbevis eller feil/blokkert med grunn. Dobbelttrykk gir høyst én kjøring; transportkvittering alene gjør ikke boksen grønn.
  - Feil requester, feil grant/keypath, endret kildeversjon, avslått godkjenning og utilgjengelig bro avvises uten kjøring eller grønn status. Portene forblir menneskelige. Q7 avgjør om manuell overgang med bevis kan godtas i første leveranse.
- Verifier: `test.plangraf.handling-web`, `test.plangraf.handling-maskin`, `test.plangraf.grant-og-porter` (hvordan og bevis i §5).
- Gjenbruk: `…arbeidsflyt.sekvens`, `…arbeidsflyt.utforer-per-steg`, `…arbeidsflyt.menneskelige-porter`, `…arbeidsflyt.steg-har-bevis`.

#### E4 · `…plangraf.forklaring-ved-siden-av` — Forklaringen kommer ved siden av punktet

- Forelder: `…utviklerbenk.plangraf`; status: `candidate`.
- Goal: `goal.candidate.utviklerbenk.plangraf.forklaring-ved-siden-av`; lifecycle: `continuous`.
- Outcome: Kjetil får AI-forklaring av valgt punkt i sidepanel, overlay eller flytende vindu og kan feste forklaringen uten å legge noe i chatloggen.
- SuccessSignals:
  - Forklar finnes på hver boks og ved formål, gjør, test, artefakt, status/bevis, avhengighet og handling i detaljene. Kontekst er valgt WP/felt, formål og lesbare kilder med versjon; svaret viser kildehenvisninger og skiller manglende informasjon fra forklaring.
  - Før/etter åpne, oppfølgingsspørsmål, feil, lukke, feste og gjenåpne er chatmeldings-ID-er og innhold uendret; ingen bruker-, assistent- eller verktøymelding skrives gjennom chatveien.
  - Feste bruker Butler B-mønsteret: bruker-eid element med kilde og valgt skop i Portholens CellConfiguration; ny økt beholder festet element. Endret kilde merker forklaringen utdatert og tilbyr ny forklaring. AI-feil gir synlig feiltilstand med prøv igjen.
  - Bare kilder requester kan lese sendes til forklareren; formålsmatching kan velge hjelper, men gir ingen tilgang og oppretter ingen chatmelding.
- Verifier: `test.plangraf.forklaring-uten-chat`, `test.plangraf.forklaring-festet` (hvordan og bevis i §5).
- Gjenbruk: `…oppgave.typede-kilder`, `…oppgave.referanse-er-ikke-tilgang`. Butler B `…detachable.live-binding` / `…detachable.owned-and-persisted` (§0.2 E-A16).

#### E5 · `…plangraf.aldri-utdatert` — Grafen viser samme sannhet som filene

- Forelder: `…utviklerbenk.plangraf`; status: `candidate`.
- Goal: `goal.candidate.utviklerbenk.plangraf.aldri-utdatert`; lifecycle: `continuous`.
- Outcome: Grafens status, detaljer og handlinger er en versjonert projeksjon av PLAN.md, STATUS.md og TESTRESULT.md, og påstår aldri å være fersk eller levert uten tilsvarende kildebevis.
- SuccessSignals:
  - Ved lesbar aktiv kilde slår endring i hver av de tre filene gjennom uten manuell omlasting innen 5 s i tre forsøk per klient. Kildeversjon og sist verifisert vises; eldre eller delvise oppdateringer kan ikke overskrive en nyere konsistent projeksjon.
  - Ved frakobling eller ulesbar kilde merkes siste snapshot som sist kjent/ukjent ferskhet, aldri dagens sannhet; utførelse er sperret til server og kildeeier har bekreftet versjonen på nytt. «Aldri» er denne sannhetsgrensen, ikke et løfte om null overføringstid.
  - PLAN eier beskrivelsen/avhengighetene, STATUS de uttrykkelige portene og daterte statusopplysningene, TESTRESULT testbeviset. Uenighet vises med begge kilder. Grønn WP krever alle relevante steg/tester og bevis for riktig forsøk og artefakt; en portgodkjenning alene er ikke leveranse.
  - Ingen separat grafstatus kan settes. Handling oppdaterer kildens arbeidsflyt/bevis og projiseres tilbake. Fjernet bevis, feil artefakt, rollback eller nyere rød måling trekker grønt tilbake; slettbar cache kan bygges identisk fra samme kildeversjon.
- Verifier: `test.plangraf.kildeendring`, `test.plangraf.bevis-og-konflikt` (hvordan og bevis i §5).
- Gjenbruk: `…oppgave.graf-er-projeksjon`, `…arbeidsflyt.steg-har-bevis`.

#### E6 · `…plangraf.ingen-niende-inngang` — Skal ikke: plangrafen blir en niende inngang

- Forelder: `…utviklerbenk.plangraf`; status: `candidate`; polarity: `prohibited`.
- Goal: `goal.candidate.utviklerbenk.plangraf.ingen-niende-inngang`; lifecycle: `continuous`.
- Outcome: Plangrafen inngår i den eksisterende benkens oppgavevalg og øker ikke antall toppnivåinnganger for arbeid.
- SuccessSignals:
  - Før/etter-inventar av faktisk servert navigasjon viser ingen ny toppnivåinngang for plangraf; Mine handlinger, detalj og Forklar åpnes fra samme valgte oppgave.
  - Bytte mellom prosjekt-, utvikler- og driftslinse beholder WP-valg og forklaringskontekst. En intern rute eller et festet element teller ikke som en ny app/benk og oppretter ingen ekstra oppgavelagring.
- Verifier: `test.plangraf.netto-null` (hvordan og bevis i §5).
- Gjenbruk: `…linser.netto-null-flater`, `…linser.valgt-binder`.

---

#### E7 · `…plangraf.celle-import` — Datakilden migrerer fra filer til celler, med importvei (lagt til 2026-09-14 av Kjetil, svar på Q8)

- Forelder: `…utviklerbenk.plangraf`; status: `candidate`.
- Goal: `goal.candidate.utviklerbenk.plangraf.celle-import`; lifecycle: `continuous`.
- Outcome: Kjetil ordrett: «Les fra filene, men da har vi cellene som vi representerer det med. Så vi får en elegant vei til Celler og import fra filer.» A-14 (filer først) er en bevisst overgang, ikke et endelig valg — E1/E5 leverer på filer nå; denne noden leverer senere en dokumentert, tapsfri importvei fra PLAN/STATUS/TESTRESULT-filene til cellerepresentasjon, uten at plangrafen må vente på den for å starte.
- Ikke dekomponert i egne suksesssignaler/tester ennå — egen G1-runde tas når E1/E5 er levert og importbehovet er konkret, ikke en forutsetning for E.
- Følgeforpliktelse (samme beslutning, ikke en egen node): når celle-import er fullt støttet, gjennomgås Claude- og Codex-trådene for viktige ting som er glemt, slik at de også kan importeres.

---

<a id="e8-sporsmallister"></a>

#### E8 · `…plangraf.sporsmallister` — Eierens spørsmål og svar har ett sted å bo

**P0-inntak 2026-09-28 — egen kandidatoppgave til benkens PDD-løp, ikke en ferdig spesifikasjon.**

- Forelder: `purpose://candidate.utviklerbenk.plangraf`; status: `candidate`.
- Lokal kandidat: `purpose://candidate.utviklerbenk.plangraf.sporsmallister`. Ingen innføring i Book 23 eller runtime.
- Beslutningseier: Kjetil. Neste ansvarlige løp: benkens P1-formålsarbeid.
- Goal: `goal.candidate.utviklerbenk.plangraf.sporsmallister`; lifecycle: `continuous`.
- Outcome: Eieren kan vise og besvare spørsmålslister i utviklerbenken, og hver beslutning har ett autoritativt sted fra spørsmålet stilles til svaret er ført inn i det det påvirker.

**Momenter fra bestillingen som P1 skal ivareta** (ønskede utfall, ikke vedtatt datamodell eller GUI):

1. Hvert spørsmål har synlig status: åpent, besvart eller ført inn. Dette er spørsmålets livsløp, ikke nye statuser for WorkItem.
2. Eieren kan svare med et listevalg eller fritekst når valgene ikke passer.
3. Anbefaling og eiersvar er tydelig atskilt; en anbefaling er aldri et avgitt svar.
4. Et besvart spørsmål kan spores til hva svaret endret. «Besvart» betyr ikke at endringen er ført inn.
5. Et spørsmål kan gjenåpnes, og gjenåpningen og tidligere svar må fortsatt være synlige.
6. Benk, dokumentasjon og eventuelle skjema viser samme beslutningsgrunnlag. Eieren skal slippe å gjenta svaret i chat eller få det kopiert manuelt mellom uavhengige originaler.

**Observerbart mål for videre formålsarbeid:** Eieren åpner en liste i benken, gir både et listevalg og
et fritekstsvar, finner svarene igjen, ser hva de er ført inn i og gjenåpner ett spørsmål uten at historikken
forsvinner. Ingen ubesvart anbefaling vises som eiersvar. Benkens P1 må avlede konkrete mål/tester og
beviskrav fra dette før G1; ingen funksjonstest eller produktleveranse er registrert nå.

**Gjenbruk og grense mot eksisterende elementer:** E3 eier handling/svarvei, E4 forklaring, E5 én sannhet
og bevis, E6 plasseringen i eksisterende benk. Dommerbenk-kandidaten i §0 bidrar med forståelige spørsmål
og svar; Valgbenken viser valg/anbefaling/bevis. E8 tilfører spørsmålslistens sammenhengende livsløp og
sporbar innføring, uten å opprette disse mekanismene på nytt. Book 23s
`purpose://project-work.work-items` og `purpose://digital-work.collect-structured-input` er eksisterende
forankringer. Om spørreskjemacellene kan gjenbrukes, og forholdet til E7s fil-/celleimport, skal undersøkes
i P1; de er ikke valgte løsninger eller nye harde avhengigheter her.

**Kilder til P1:** De seks hovedvalgene D1–D6 i
[vedleggs-PDD §2](../PDD_vedlegg-korrespondanse_2026-09-28/FORMAALSSPEC.md) er første konkrete tilfelle;
samme dokuments §6 har i tillegg D7–D8. EntityData-gjennomgangen og beslutningsregisteret er kildebelagt
i [inntaksrapporten](../BENK_SPOERSMAALSLISTER_2026-09-28.md). Svarene skal ikke kopieres til en ny
beslutningsliste i denne dokumentjobben.

**Neste steg:** Benkens P1 avklarer kildeeierskap, tilbakeføring og gjenåpning, undersøker gjenbruk og
legger E8 fram som et avgrenset G1-tillegg. G1/G1-GUI fra 14.–15.09 omfatter ikke denne nye bestillingen.
G2-plan, GUI, kontrakt, kode og commit følger deretter benkens eget løp; ingen av disse bestilles her.

---

## 2. Avgrensning og avhengigheter

Hva dette **ikke** er:
- Ikke et nytt tre-element i skeleton-formatet — U2 finnes. Å foreslå `Tree` ville vært å bygge samme ting to ganger.
- Ikke en ny kø — «sett i kø» skriver til HAVEN-Deploy-arbeidskøen (vedtatt 07.09). `_losen-queue` er det som kjører i dag.
- Ikke en kodesymbol-indeks — den eies av Kontekstgraf-planen. Første versjon av `git`-kilder er repo/ref/sti, ikke symboler.
- Ikke kjøring — AgentD og dispatcheren utfører; benken eier intensjon og historikk. E kan be om en tillatt handling via en bevist bro, men får ikke shell- eller deploymyndighet.
- Ikke Jira/Linear-bredde (Workbench 1.0 ikke-mål).
- Ikke visionOS-rommet — egen PDD i dag; tre- og grafdataene her skal kunne rendres der senere, uten at det er et krav nå.

| # | Avhengighet | Verifier | Eier | Må virke før |
|---|---|---|---|---|
| A-1 | U2 tre-liste er i main og i miljøet benken testes i | `childrenKeypath` i servert `skeleton-runtime.js` på staging | kjetil (deploy) | A `…ideer.tre` |
| A-2 | Binding-renderer for U2 | paritetsrad U2 grønn | codex | Binding-delen av `…ideer.tre` |
| A-3 | Arbeidskøens G3: ekte utførere (HD-0013 EPERM, HD-0014 Claude-innlogging, HD-0015 lokal HTTP) og WP7 plist installert | `test.ko.e2e` én jobb per utfører | **kjetil** (WP7, innlogging) + codex | C `…arbeidsflyt.en-ko` |
| A-4 | Operatør-grant i kode (admin workbench WP-D1) | `test.agreement.operator-scopes` | codex | D `…linser.tilgang-fra-grant`, C `…menneskelige-porter` |
| A-5 | Book 36: ditt ord + commit (avvist to ganger) | `purpose_dev.py gates` på fixture gir dokumenterte koder 0/1/2/3 fra committet kode | **kjetil** (ord) + kø | C `…arbeidsflyt.sekvens` |
| A-6 | WO-1 MCP-bro: agenter skriver via celler | serveren i `.mcp.json` + capture-test | codex | A `…agentforslag-i-eget-lag` |
| A-7 | WorkItem 0.5 er ute (Open-knapp, persistens-kvittering) | Work Item Tracker på staging viser Open og overlever restart | kjetil + claude | alt som bygger på WorkItem |
| A-8 | Flow som observerbar kilde | beslutning på §6 Q3; for live-varianten: `CellInteractionEvent`/FlowTap fra visionOS-PDD eller tilsvarende | kjetil | B `…typede-kilder` (`flow`) |
| A-9 | Beslutning på de 109 ubesluttede endringspakkene (HAVEN-Deploy G8) | `hd gap` = 0 | kjetil | at steg 9 «Deploy» kan bli grønt for noen oppgave |

**Avhengigheter for E (forslag, ingen er målt levert i denne runden):**

| # | Kapabilitet og kilde | Avgrensning / mangler | Verifier og bevis | Eier | Må virke før |
|---|---|---|---|---|---|
| A-10 | Normalisert PLAN-format; §0.2 E-A8/E-A9 og de tre PLAN-filene | WP-ID og full purposeRefs-liste, lane, eksplisitte avhengigheter, gjør, testRefs, artefaktRefs, eier, utfører, menneskehandling med når/hva/hvorfor/etterpå må kunne leses deterministisk. Flere purposeRefs per WP tillates. Ingen AI-gjetting av grafkanter eller «i morgen». | `test.plangraf.plan-normalisering` → `TESTRESULT.md#plangraf-plan-normalisering` | Claude (kontrakt), Codex (leser) | E1, E2, E5 |
| A-11 | Bro til Kjetils maskin; §0.2 E-A13/E-A14, HD-0069 og menylinje-PDD | Eksisterende challenge-svarvei er ikke generell skriptkjøring. Trenger app/AgentD-handling med identitet, tillatt handlings-ID, omfang, eksplisitt godkjenning, idempotens og resultatbevis. HD-0069 alene oppfyller ikke dette. Q7 avgjør om en manuell første variant godtas. | `test.plangraf.handling-maskin` → `TESTRESULT.md#plangraf-handling-maskin` (både ekte ufarlig lokal prøve og frakoblet/avvist); gjeldende brokontrakt i `contract/plangraf-actions.md` | Kjetil (maskin/ord), Codex (adapter) | E3 maskinhandling, aldri krav for bare å lese grafen |
| A-12 | Grant til å utføre og registrere menneskelig beslutning; §0.2 E-A15; gjenbruk A-4/C/D | Behandler må kontrollere faktisk identitet, presis handling/mål/revisjon og grant ved utførelse. Oppgaveeier, formålsmatch, farge eller knapp gir ingen rettighet. Filskriver/svarvei for webgodkjenning må bevises. | `test.plangraf.grant-og-porter`, `test.plangraf.handling-web` → `TESTRESULT.md#plangraf-grant-og-porter`, `#plangraf-handling-web` | Codex; Kjetil er beslutningseier | E3 alle skrivende handlinger |
| A-13 | Skjelettelementer og renderersemantikk for plangraf; §0.2 E-A10–E-A12 | `Visualization` gir grunnlag, men lanes, boksmal, utfører/status, separate knapper og komplett web/Binding-paritet mangler bevis. Først elementkart med eksisterende mulighet/gap; G1 er ikke i seg selv godkjenning av nye felt/cases. Eksakt utvidelse legges fram i G1-GUI-underlaget, uten oppdiktede JSON-felt. | `test.plangraf.renderer-kontrakt`, `test.plangraf.visning-paritet` → `TESTRESULT.md#plangraf-renderer-kontrakt`, `ACCEPT.md#plangraf-paritet` | Codex (web/skjema), Xcode/Binding | E1–E4 som full brukerflate |
| A-14 | Lesbar PDD-kilde og versjonert projeksjon til staging; §0.2 E-A6/E-A7/E-A17 | Filene forblir kilde; må ha eksplisitt leser/synk og tilbakevei til kildens arbeidsflyt ved handling. Staging får bare innhold requester har tilgang til. Ingen direkte stitraversering, ufiltrert Mac-mappecrawling eller lokal kjøring på serveren. Reell adapter/endepunkt er ikke funnet og må navngis i kontrakten. | `test.plangraf.kildeadgang`, `test.plangraf.kildeendring` → `TESTRESULT.md#plangraf-kildeadgang`, `#plangraf-kildeendring`; flyt i `dataflow.md` | Codex; Kjetil (kildetilgang) | E1/E2 med ekte filer, E3 status tilbake, E5/staging |
| A-15 | Forklarer og festet løsrivbart element; §0.2 E-A16 og Butler B | Leser valgt formål og kilder uten chat-skriving. Gjenbruk av B er en avhengighet, ingen ferdig integrasjon. Q9 avgjør hvem som eier innrammingen; matching kan være utskiftbar. | `test.plangraf.forklaring-uten-chat`, `test.plangraf.forklaring-festet` → `TESTRESULT.md#plangraf-forklaring-uten-chat`, `#plangraf-forklaring-festet` | Claude (kontrakt), Codex (integrasjon) | E4 |

**Normalisering og sannhetsregler for første filbaserte variant (Q8-forslag):**
PLAN.md bærer den strukturerte WP-beskrivelsen; STATUS.md bærer porter og daterte statusopplysninger;
TESTRESULT.md bærer testmåling/bevis. En avledet modell har stabile `PDD-sti + WP-ID`, eksplisitte
`purposeRefs[]`, `dependsOn[]`, kildepeker/versjon per felt og en deklarert handlingstype med mål og svarvei.
Dette er krav til `contract/plangraf-source.md`, ikke et nytt lagringsformat vedtatt eller implementert her.

Leseren må håndtere både WP-avsnitt og tabell. Forkortelser som agent-menylinjens `challenge-inbox`
løses mot akkurat den mappens FORMAALSSPEC; tvetydighet eller manglende metadata blir synlig diagnose.
Eier og utfører normaliseres separat; «Claude med Codex som byggearm» er ikke automatisk oppgaveeier.
Lanes/rekkefølge og avhengighetspiler må få eksplisitt opphav, ikke utledes av fritekstens nærhet eller HTML-posisjon.
Menneskehandlingen kan være et steg inni WP-boksen; den oppretter ikke en kopi av oppgaven.
Kildemapper som mangler PLAN eller TESTRESULT er gyldige før de aktuelle portene, men gir ingen konstruert plan
eller leveransebevis. Kildefeil stopper utførelse av berørte steg, ikke innsyn i en tydelig merket siste kjent visning.

Designpunkt å verifisere i P2, ikke et spørsmål: drøfting avdekker ofte manglende informasjon. Book 36 tillater nytt
forsøk med ny måling; det må bekreftes med `purpose_composition.py` at et nytt forsøk på steg 2 etter steg 3 er lovlig
og krever nye målinger av 3, uten at sekvensen regnes som brutt.

---

## 3. Forventningskontrakt — «Det du kommer til å se»

| Leveranse | Type | Hvor | Referanse | Godkjent |
|---|---|---|---|---|
| Denne spesifikasjonen, iterasjon 2 med forslag og åpne valg i §6 | fil | `FORMAALSSPEC.md` | G1 | nei |
| Idétreet, tom og fylt tilstand | bilde | `images/idetre-tom-v1.png`, `images/idetre-fylt-v1.png` | G1-GUI | nei |
| Samme utvalg som graf, med delt valg | bilde | `images/idegraf-v1.png` | G1-GUI | nei |
| Oppgave i fokus: plass i helheten, typede kilder med `lesbar`, avhengighetsgraf med én uleselig node | bilde | `images/oppgave-kontekst-v1.png` | G1-GUI | nei |
| Arbeidsflyten på oppgaven: sekvens, utfører per steg, ett steg i kø, ett blokkert, én port som venter på Kjetil | bilde | `images/arbeidsflyt-v1.png` | G1-GUI | nei |
| Samme flate for bidragsyter uten operatør-grant (driftslinsen borte, ikke tom) | bilde | `images/linser-uten-grant-v1.png` | G1-GUI | nei |
| Skeleton-JSON bildene er rendret fra (Porthole-preview der formatet tillater; ellers mockup med liste over hva skeleton ikke kan) | fil | `skeleton/` | G1-GUI | nei |
| Kontrakt `work-item` 0.6 (`parentRef`, `sources[]`) med positive og negative fixtures | fil | `contract/` | G2 | nei |
| Arbeidsflytmal som Book 36-JSON + to varianter (research, dokumentasjon) | fil | `contract/` | G2 | nei |
| Kjørende flate på staging med din egen identitet | kjørende flate | staging | G3 | nei |
| Simulert bruker per rolle: gjennomgang og hvor tilgang hindret | testutdata | `TESTRESULT.md#walkthrough` | G3 | nei |
| Utdata for hver rad i §5 | testutdata | `TESTRESULT.md` | G3 | nei |

### E — nye synlige leveranser

Bildene nedenfor skal lages **etter G1**, legges fram til G1-GUI og deretter brukes som referanse ved
akseptanse. Ingen av dem er laget i iterasjon 2. Web: 1900×1100; app/Binding: 780×1688.
Porthole-preview av gyldig skeleton brukes der det er mulig; ellers eksplisitt merket mockup med gapliste
for lanes/bokser/knapper og tilhørende appavvik. Mockup er ikke bevis på rendererfunksjon.

| Leveranse | Type | Hvor | Referanse | Godkjent |
|---|---|---|---|---|
| Plangraf med lanes, alle statustyper, piler og Mine handlinger — web og app | bilde | `images/plangraf-web-graf-fylt-v1.png`, `images/plangraf-app-graf-fylt-v1.png` | G1-GUI | nei |
| Tom plan med forklart fravær — web og app | bilde | `images/plangraf-web-graf-tom-v1.png`, `images/plangraf-app-graf-tom-v1.png` | G1-GUI | nei |
| Manglende/utdatert kilde og motstridende status — web og app | bilde | `images/plangraf-web-graf-kildefeil-v1.png`, `images/plangraf-app-graf-kildefeil-v1.png` | G1-GUI | nei |
| Åpen boks med purposeRefs, gjør, tester, artefakter, eier og bevis — web og app | bilde | `images/plangraf-web-drilldown-v1.png`, `images/plangraf-app-drilldown-v1.png` | G1-GUI | nei |
| Utfør før trykk, med mål, grant, når/hvorfor/etterpå — web og app | bilde | `images/plangraf-web-utfor-for-v1.png`, `images/plangraf-app-utfor-for-v1.png` | G1-GUI | nei |
| Startet handling med kjørings-ID, ennå ikke levert — web og app | bilde | `images/plangraf-web-utfor-kjorer-v1.png`, `images/plangraf-app-utfor-kjorer-v1.png` | G1-GUI | nei |
| Utfør etter kvittering, med status og artefaktbevis — web og app | bilde | `images/plangraf-web-utfor-etter-v1.png`, `images/plangraf-app-utfor-etter-v1.png` | G1-GUI | nei |
| Utfør avvist eller maskinbro borte, med reell grunn — web og app | bilde | `images/plangraf-web-utfor-blokkert-v1.png`, `images/plangraf-app-utfor-blokkert-v1.png` | G1-GUI | nei |
| Forklaringsoverlay ved valgt punkt, med kilder og oppfølgingsspørsmål — web og app | bilde | `images/plangraf-web-forklaring-v1.png`, `images/plangraf-app-forklaring-v1.png` | G1-GUI | nei |
| Forklarer utilgjengelig, med Prøv igjen — web og app | bilde | `images/plangraf-web-forklaring-feil-v1.png`, `images/plangraf-app-forklaring-feil-v1.png` | G1-GUI | nei |
| Forklaring festet ved siden av grafen, kilde endret — web og app | bilde | `images/plangraf-web-forklaring-festet-v1.png`, `images/plangraf-app-forklaring-festet-v1.png` | G1-GUI | nei |
| Elementkart, gap og beskrivelse av hvert referansebilde | fil | `images/README.md`, `contract/plangraf-renderer.md` | G1-GUI | nei |
| Én CellConfiguration/skeleton for begge klienter, og preview-scenarioer med identisk data | fil | `skeleton/plangraf.json`, `skeleton/plangraf-web.preview.json`, `skeleton/plangraf-app.preview.json` (etter at feltene er dokumentert støttet) | G1-GUI | nei |
| Normaliseringskontrakt med tre kildevarianter, bevisregler og manglende/konflikt-fixtures | fil | `contract/plangraf-source.md`, `contract/fixtures/plangraf/` | G2 | nei |
| Handlings- og forklaringskontrakt med reelle endepunkt/keypaths, grant, kildeversjon, svar og feilstater | fil | `contract/plangraf-actions.md`, `contract/plangraf-explanation.md`, `dataflow.md` | G2 | nei |
| Plangraf i eksisterende benk på staging: velg oppgave → graf → boks → egen handling → bevis, samt Forklar/Fest | kjørende flate | staging, konfigurasjonen **HAVEN Workbench** / kilde `cell:///WorkItem` som foreslått gjenbrukspunkt; faktisk rute, `/health/build` og kildeversjon logges i `TESTRESULT.md#plangraf-staging` | G3, ekte identitet i web og Binding | nei |
| Skjermbilder fra kjørende web/Binding og utdata per E-test | testutdata/bilde | `TESTRESULT.md#plangraf-staging`, `ACCEPT.md#plangraf-paritet`, `evidence/plangraf/` | G3 | nei |

---

## 4. Lærdommer som former treet

Fullt `purpose_dev.py lookup`-utdrag ligger i `LOOKUP.md`. Disse endret noe i treet:

| Lærdom | Hva den endret |
|---|---|
| `lesson.plan-instead-of-delivery` | §3 har bare artefakter; bildene er neste leveranse, ikke en ny plan |
| `lesson.text-ux-is-not-design` | fem bilder før G2, inkludert «uten grant»-tilstanden |
| `lesson.decomposition-is-classification` | rot under `project-work.work-items`; alle nye noder `candidate` |
| `lesson.purpose-never-grants-rights` | `…referanse-er-ikke-tilgang` som eget antiformål |
| `lesson.empty-list-must-not-look-like-calm` | `lesbar: ja/nei/ukjent` med grunn på hver kilde; uleselige grafnoder er noder |
| `lesson.paste-command-instead-of-queue` | `…arbeidsflyt.en-ko`: ingen kommandoer til Kjetil, bare kø |
| `lesson.codex-sandbox-cannot-reach-docker` | deploy har aldri `codex` som utfører |
| `lesson.syntax-check-reported-as-delivered` | steg 4 rapporteres «skrevet, ikke verifisert»; grønt først i steg 5 |
| `lesson.branch-is-empty-after-eight-work-packages` | steg 6 måles med `rev-parse branch ≠ base` |
| `lesson.main-does-not-build-without-unlanded-changes` | steg 5 kjøres i rent worktree fra revisjonen |
| `lesson.codex-workspace-write-cannot-build-cellscaffold` | steg 5 som detached jobb, ikke `workspace-write`-køjobb |
| `lesson.findability-is-not-usability` | flatetestene går mot `reachableActionKeypaths`, ikke mot beskrivelsen |
| Kontrollrom felle 1–3 (design 25.08) | fangst uten felt; agentforslag i eget lag; netto null flater |
| Butler Chat-PDD 08.09: «treet finnes alt» | ingen nytt tre-element; U2 gjenbrukes |


Iterasjon 2: både eksisterende lærdommer og nytt lookup er lest før E ble skrevet. Den bestilte kommandoen
med kommaseparerte argumenter ble kjørt ordrett; CLI tar lister med mellomrom (`purpose_dev.py:522`),
så den ga bare alwaysAttach-pakken. Supplerende kjøring med separate argumenter ga også GUI-pakken.
Begge resultater står i `LOOKUP.md`; eksisterende pakker beholdes. Ingen bygg-/kjøreinstruksjon i
lærdommene overstyrer denne rundens forbud mot bygg, nett eller git-mutasjon.

| Lærdom / audit | Konkret følge i E |
|---|---|
| `lesson.parity-was-correctness-not-decoration`, `lesson.text-ux-is-not-design` | Bildepar for web/app i §3 og faktisk knapp-/kildeparitet i `test.plangraf.visning-paritet`; ingen bilder før G1 |
| `lesson.empty-list-must-not-look-like-calm`, `lesson.planned-documented-as-implemented` | Kildefeil og manglende bevis er synlige; kildeendring og beviskonflikt har egne tester |
| `lesson.test-corpus-is-not-shipped-corpus`, `lesson.tested-a-different-path-than-production` | Staging-test starter i faktisk servert navigasjon og bruker produksjonens renderer/svarvei |
| `lesson.findability-is-not-usability`, `lesson.purpose-never-grants-rights` | Reelle handlinger og negative grantsjekker, ikke bare en synlig knapp |
| `lesson.paste-command-instead-of-queue` | Anbefal bro i Q7; manuell kopiering er kun Kjetils uttrykkelige alternativ med svakere første leveranse, aldri meldt som utførelse fra boksen |
| `lesson.local-main-is-not-main`, `lesson.baseline-measured-another-pdds-branch` | Audit leser lokal `origin/main`, oppgir SHA og har ingen påstand om oppdatert GitHub eller staging |

---

## 5. Avledede tester

| Test | Type | Hvordan | Evidens |
|---|---|---|---|
| `test.benk.walkthrough-per-rolle` | command | `Sources/UserSimulationScaffold` med tre roller mot staging; logger formålsoppnåelse og tilgangshindringer | `TESTRESULT.md#walkthrough` |
| `test.idea.capture-two-actions` | command | Playwright teller handlinger fra fokus til lagret idé | `#capture` |
| `test.idea.raw-immutable` | command | celletest: `update` på råtekst avvises, berikelse lagres som lag | `#capture` |
| `test.tree.move-keeps-subtree` / `rejects-cycle` | command | celletest på fixture med tre nivåer | `#tree` |
| paritetsrad U2 Binding | command | paritetskorpus-snapshot web ↔ Binding | `#parity` |
| `test.graph.node-count-equals-tree` / `selection-shared` | command | import av fixture; valg i graf leses i tre | `#graph` |
| `test.idea.freeze-human-only` | command | negativ: agent-requester får `denied` på frys og kø | `#auth` |
| `test.queue.enqueue-creates-post` | command | «sett i kø» → `hd validate` godtar ny post med `purposeRef` og `taskRef` | `#queue` |
| `test.idea.agent-writes-are-proposals` | command | agentskrevet node har `proposal: true` og telles ikke | `#auth` |
| `test.task.single-parent` / `subtask-migration-lossless` / `purposeref-resolves` | command | kontraktfixtures 0.6; migrering av 0.5-seed med subtasks gir samme antall og titler | `#contract` |
| `test.source.types-validate` / `resolvability-honest` | command | positive/negative fixtures; hvert feilutfall gir egen tilstand og grunn, aldri tom liste | `#sources` |
| `test.depgraph.complete-for-fixture` / `unreadable-visible` / `same-context-for-agent` / `rebuild-identical` | command | fixture med kjent graf; én kilde gjort uleselig; eksport sammenlignet kanonisk; slett og bygg | `#depgraph` |
| `test.cell.auth-negative` | command | feil requester / feil keypath / ukjent formål på `graph.subgraph` og kildeoppslag | `#auth` |
| `test.flow.sequence-enforced` / `templates-validate` / `green-requires-evidence` | command | `purpose_dev.py validate` + `gates` på mal og tre kjøringslogger (lovlig, for tidlig start, grønt uten bevis) | `#flow` |
| `test.flow.executor-rules` | command | mal med `codex` på deploy avvises | `#flow` |
| `test.queue.round-trip` | command | ekte jobb per utfører; stegets måling oppdateres | `#queue` |
| `test.flow.gate-human-only` / `test.ko.no-escalation` | command | jobb forsøker å åpne port / legge `workspace-write` → avvist | `#auth` |
| `test.ko.lesson` | command | eksisterende HAVEN-Deploy-test | `#queue` |
| `test.gui.context-propagation` | command | Playwright: velg A, les tre linser; velg B | `#gui` |
| `test.agreement.operator-scopes` | command | identitet uten grant → ingen driftslinse; med grant → nøyaktig skopene | `#auth` |
| `test.catalog.entry-count-not-increased` | command | tell toppnivåinnganger for arbeid før/etter | `#catalog` |
| `test.gui.reference-image-exists` / `test.gui.parity` / `test.skeleton.no-unreachable-elements` / `test.gui.load-time` | artifact / inspection / command / measurement | pakke `pkg.std.gui-surface` | `images/`, `ACCEPT.md#parity`, `#reachability`, `#load-time` |
| `test.build` / `test.regression` / `test.docs-updated` / `test.status-current` | command / inspection | pakke `pkg.std.everything-works` | `#build`, `#regression`, `ACCEPT.md` |

### E — tester for plangraf og avhengighetene

Alle radene under er **venter**. Dette er testkontrakten, ikke påstander om kjørte tester eller eksisterende
kommandoer. Ved gjennomføring legges råutdata, kilde-/buildversjoner og skjermbilder under `evidence/plangraf/`,
med lenker fra det navngitte ankeret. De eksisterende pakketestene over gjelder fortsatt.

| testRef | Formål | Type | Hvordan | Evidens | Status |
|---|---|---|---|---|---|
| `test.plangraf.plan-normalisering` | A-10, E1/E2/E5 | command | Kjør fremtidig normaliseringsleser mot kopier av de tre auditerte PLAN/STATUS/TESTRESULT-settene. Avstem alle WP-ID-er, fullstendige purposeRefs, artefakter og eksplisitte kanter mot gjennomlest fasit. Prøv tabell, avsnitt, flere purposeRefs, manglende eier/lane/TESTRESULT og tvetydig kortnavn; krev diagnose fremfor gjetting. Kommandolinjen fastsettes i PLAN etter G1/G2. | `TESTRESULT.md#plangraf-plan-normalisering` | venter |
| `test.plangraf.renderer-kontrakt` | A-13, E1–E4 | inspection | Gå elementkartet mot faktisk dekoder og begge renderere: lane, kort, statusmerke, piler, nodevalg, Utfør, Forklar, panel og Fest. Hvert felt/handling må ha kilde og keypath/kontrakt; gap hindrer godkjenning av implementeringsparitet. Kjør senere reachability-audit for det faktisk serverte skjelettet. | `TESTRESULT.md#plangraf-renderer-kontrakt` | venter |
| `test.plangraf.visning-paritet` | E1 | inspection | Åpne samme kildesnapshot i web 1900×1100 og Binding 780×1688. Tell lanes/bokser/kanter og sammenlign utfører, status og valg med fasit; inspiser panorering, tastatur, tekst og alle §3-bildepar mot godkjent referanse. Alle handlinger må være nåbare i begge klienter. | `ACCEPT.md#plangraf-paritet` | venter |
| `test.plangraf.drilldown-kilder` | E2 | inspection | Åpne én boks per lane og alle feiltilstander i begge klienter. Følg purposeRef, gjør, tester, artefakter og statusbevis til riktig kildeversjon/anker; kontroller eier separat fra utfører. Lukk/åpne og krev samme valg/utsnitt. Logg manglende kilde som avvik. | `TESTRESULT.md#plangraf-drilldown-kilder` | venter |
| `test.plangraf.handling-web` | E3 | inspection | Med tillatt testidentitet: Åpne PR går til eksakt PR; bare et navigasjonssteg kan kvitteres av dette. Registrer deretter en testgodkjenning fra boksen via faktisk skrivevei, les kildens beslutning/kvittering og grafens oppdatering. Prøv avbryt, serverfeil og dobbelttrykk; ingen falsk levert-status eller dobbel handling. Ingen ekte PR/port i denne runden. | `TESTRESULT.md#plangraf-handling-web` | venter |
| `test.plangraf.handling-maskin` | A-11, E3 | inspection | Etter at broen finnes: fra boks i web og app start samme forhåndsdefinerte ufarlige lokale prøve på Kjetils Mac. Bekreft handlings-ID, grant, én kjørings-ID og resultatbevis tilbake i kilde og graf; avbryt, koble fra og prøv uautorisert handlings-ID. Deploy må senere ha sin egen staging-kvittering; en ufarlig prøve beviser ikke deploy. Velges manuell Q7-variant, dokumenteres kopier/registrer-bevis særskilt og brokravet er fortsatt ikke målt grønt. | `TESTRESULT.md#plangraf-handling-maskin` | venter |
| `test.plangraf.grant-og-porter` | A-12, E3 | command | Mot handlingsbehandleren: feil requester, keypath, manglende/tilbakekalt grant, agent som prøver menneskeport, endret mål/revisjon og utgått forespørsel skal avvises før bivirkning. Tell kjøringer = 0 og uendret kildestatus. Positiv prøve krever Kjetils identitet/handling og riktig grant; gjenbruk C sine negative porttester. | `TESTRESULT.md#plangraf-grant-og-porter` | venter |
| `test.plangraf.forklaring-uten-chat` | A-15, E4 | inspection | Ta snapshot av chatmeldings-ID-er og innhold. Bruk Forklar på hvert feltslag i E4, still oppfølging, prøv AI-feil og lukk panelet i begge klienter. Inspiser forespørselens WP/felt/formål og tillatte kilder samt svarets referanser. Krev identisk chatinnhold og null chat-append-kall gjennom hele løpet, også ved feil; utilgjengelige kilder skal ikke sendes. | `TESTRESULT.md#plangraf-forklaring-uten-chat` | venter |
| `test.plangraf.forklaring-festet` | A-15, E4 | inspection | Fest et svar, lukk klienten og åpne igjen med samme identitet og valgt skop; kontroller at kildebindingen og festingen overlever i CellConfiguration. Endre kilden og krev merket utdatert forklaring og ny forklaring fra ny versjon. Chatlogg er identisk før/etter feste, gjenåpning og oppdatering. | `TESTRESULT.md#plangraf-forklaring-festet` | venter |
| `test.plangraf.kildeadgang` | A-14, E1/E2/E4/E5 | command | Gi to identiteter ulike PDD-kildesett. Be om den andres WP, artefakt og forklaringskontekst samt sti utenfor tillatt rot; krev avvisning uten innholdslekkasje. Tillatt identitet skal få fil:linje/anker, versjon og ferskhetsstatus. Reell synk-/tilbakevei skal være navngitt i dataflow og svare gjennom samme kontrakt som GUI bruker. | `TESTRESULT.md#plangraf-kildeadgang` | venter |
| `test.plangraf.kildeendring` | E5 | measurement | Endre PLAN, STATUS og TESTRESULT hver for seg i godkjent testkilde, tre forsøk per fil per klient, uten reload. Mål fra atomisk kildeendring til riktig synlig graf: ≤ 5 s. Send eldre snapshot etter nyere og bryt forbindelsen: eldre data kan ikke overskrive nyere, frakobling markeres, og handling må avvises hvis kilderevisjonen ikke kan bekreftes. Lagre tidsstempler og versjoner. | `TESTRESULT.md#plangraf-kildeendring` | venter |
| `test.plangraf.bevis-og-konflikt` | E5 | command | Fixture med PLAN G2 venter/STATUS godkjent skal vise kildespenning og kildenes roller. Prøv levert uten bevis, manglende bevisfil, feil artefakt/forsøk, nyere rød test og ROLLED_BACK_VERIFIED: ingen grønn levert-boks. Riktig bevis gir grønt; fjern det og krev tilbakekall. Forsøk direkte grafstatusskriving avvises. Bygg projeksjonen på nytt fra samme input og sammenlign kanonisk JSON. | `TESTRESULT.md#plangraf-bevis-og-konflikt` | venter |
| `test.plangraf.netto-null` | E6 | inspection | Ta før/etter-inventar av toppnivåinnganger fra faktisk servert meny og navigasjonsdestinasjoner i web og app (gjenbruk D-testen). Plangraf/Mine handlinger/drilldown/Forklar skal finnes i den eksisterende benken uten økning. Bytt linse og kontroller at valgt oppgave/boks bevares. | `TESTRESULT.md#plangraf-netto-null` | venter |
| `test.plangraf.staging-brukersti` | E1–E6 samlet | inspection | Fra levert meny med Kjetils testidentitet: velg oppgave, åpne graf/boks, utfør tillatt webhandling og separat lokal broprøve, les kildebevis, bruk Forklar/Fest. Gjenta i Binding og uten grant. Mål lastetid ≤ 5 s tre ganger; logg faktisk konfigurasjonsnavn/rute, build-SHA, kildeversjon, kjørings-ID-er og bilder. Mockup eller direkte API-prøve alene består ikke denne testen. | `TESTRESULT.md#plangraf-staging` | venter |

---

## 6. Åpne spørsmål (bare de som endrer treet)

| # | Spørsmål | Hva som endres | Forslag |
|---|---|---|---|
| Q1 | Er idé og oppgave **samme node** (idé = tilstand før frysing) eller **to typer** med lenke? | A `…frys-og-kø-er-kjetils`, B `…plass-i-helheten`, kontrakt 0.6 | Samme node: ett tre, én graf, frys er tilstandsendring og ikke kopi |
| Q2 | Bor arbeidsflytstegene **på oppgaven** (sekvens vist i fokus og graf) eller **som deloppgaver i treet**? | C `…arbeidsflyt.sekvens`, bildet `arbeidsflyt-v1` | På oppgaven: ellers drukner idétreet i ti steg per oppgave |
| Q3 | Betyr «abonnement på Flow» som kilde en **statisk avhengighet**, en **live strøm** som oppdaterer oppgaven, eller begge? | B `…typede-kilder`, avhengighet A-8 | Begge, statisk først |
| Q5 | Godkjenner du de tre stegene merket *lagt til* i standardmalen (beslutning, PR og merge, verifisert i miljø)? | C standardmal | ja |
| Q6 | Må Binding-paritet for **idétreet (A)** være med i første leveranse, eller holder web? | A-2 som hard eller myk avhengighet; E sin web/app-paritet er uttrykkelig bestilt og omfattes ikke av dette valget | web først for A, Binding som egen rad |
| Q7 | ~~Skal maskinhandlinger kjøres via HAVEN Agent.app-broen, eller er «kopier kommando + marker gjort med bevis» nok i første leveranse?~~ **Besvart 2026-09-14** | E3/A-11: direkte start med automatisk bevisretur kontra en avgrenset manuell overgang som ikke oppfyller full utførelse fra boksen | **Broen.** Ukjent/ikke levert bro vises blokkert. Manuell variant bare hvis Kjetil velger den uttrykkelig; ikke en knapp som later som den kjører. |
| Q8 | ~~Er PDD-mappen med filer datakilden, eller skal PLAN/STATUS bli celler først?~~ **Besvart 2026-09-14** | E1/E5/A-10/A-14: filleser og versjonert projeksjon kontra nødvendig cellemigrering før visningen | **Filer først**, som Book 35 §5: normalisert lesing og kontrollert tilbakeføring av beslutning/bevis; gjenbruk B/C og ingen dobbel lagring. |
| Q9 | ~~Eies forklaringsoverlayet av Butler med formålsmatching, eller av benken?~~ **Besvart 2026-09-14** | E4/A-15: Butler-ruting som obligatorisk avhengighet kontra benkens egen forklaringsflate med gjenbrukbar hjelper | **Benken eier åpning, kontekst og feste**; bruk Butler B-mønsteret og gjenbruk matcher/hjelper der det finnes, uten avhengighet til chatloggen. |

Kjetils svar 2026-09-14: **Q7 — HAVEN Agent.app-broen. Q8 — filer først. Q9 — benken eier åpning, kontekst og feste.** Tatt inn som avgrensning for E3 (bro er hard avhengighet; uten bro vises handlingen blokkert med grunn), E1/E5 (filkilde, normalisert projeksjon) og E4 (benkens overlay; Butler-hjelper gjenbrukes uten chatlogg).

Q1–Q3/Q5/Q6 er fortsatt åpne fra iterasjon 1. Q4 er flyttet ut av spørsmålslisten fordi den bare gjaldt
planrekkefølge; ingen beslutning er tatt på Kjetils vegne. Q7–Q9 er forslag som skal avklares ved G1,
ikke et vilkår for å fullføre denne spesifikasjonsrunden.

---

## 7. Revisjonslogg

| Iterasjon | Dato | Hva endret seg |
|---|---|---|
| 1 | 2026-09-10 | Første versjon: nåtilstand (§0.3), grense som tre linser (§0.4), tre med fire grener og standardmal for arbeidsflyt, ni avhengigheter, seks åpne spørsmål. Lest via staging; ingen git kjørt. |
| 2 | 2026-09-14 | Codex: gren E med seks nye blad (ett prohibited) og 14 nye tester; 17 kildebelagte auditrader, seks nye avhengigheter, web/app-bildepar og staging-leveranse, Q7–Q9 med forslag. A–D videreføres; Q4 om planrekkefølge tatt ut av §6. Lookup kjørt ordrett og med CLI-listesyntaks. Ingen G1/G1-GUI/G2/G3 satt; ingen bilder, plan eller implementering laget. |
| 3 | 2026-09-14 | Kjetil svarte Q7 (bro), Q8 (filer først), Q9 (benken eier) og godkjente G1. Formålstreet E rendret som bilde `images/formaalstre-E-v1.png`. Referansebildene av flaten (§3 E-rader) er ikke laget ennå — G1-GUI settes først når Kjetil har sett dem. |
| 4 · inntak | 2026-09-28 | E8 spørsmålslister registrert som én kandidatoppgave etter kontroll mot E3/E5, Valgbenken og Dommerbenken. Bestillingen og momenter til P1 er bevart; samme kandidat er ført i PURPOSE_COMPOSITION.json. Rapport: `../BENK_SPOERSMAALSLISTER_2026-09-28.md`. Ingen port, eiersvar, plan eller implementering endret. |
