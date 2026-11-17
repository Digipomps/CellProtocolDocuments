Brief audit
===========

Dato: 2026-10-05. Rolle: read-only rådgiver for WP0/WP9. Kjetils godkjenning av OIW-design og arbeidspakkene behandles som autorisasjon til hovedoppgaven; eldre «venter»-felt i separate dokumenter opphever ikke denne. Jeg har ikke implementert, bygget, kjørt tester, startet tjenester, hentet remote refs, flyttet arbeidstrær eller skrevet til produksjon. Bare denne rapporten er skrevet.

Viktig korreksjon fra oktober 2: den delte arbeidskopiens EventCells-stier er ikke dagens `origin/main`-struktur. De nyere konferansereparasjonene er derimot kommet inn i lokal `origin/main`. «Main» må derfor alltid presiseres som en bestemt ref og SHA. Ingen lokal ref eller køstatus alene beviser deploy.

## WP0: fersk baseline

| Observert sted/ref | SHA/status | Konsekvens |
|---|---|---|
| CellScaffold delt checkout, `codex/entitetsutvidelse-20260929` | `942965ca24e9a418b531f9514c1da75d6d529e30`; omfattende dirty state; `Sources/EventCells/` og `Tests/EventCellsTests/` er utrackede | Ikke bruk som ren implementerings-/testbaseline. `HEAD...origin/main`: 82 commits bare på HEAD-siden, 533 bare på origin-siden. |
| Lokal `main` | `e1f3e22f02239e44eacaf12a741d78b4066d0c35`, committerdato 2026-08-21 | Foreldet lokal gren. |
| Lokal `origin/main` og `origin/HEAD` | `e5c3434510884275cae4a732935ab4b55cf7fad9`, committerdato 2026-10-05 10:38:28 +0200 | Ferskeste lokalt kjente hovedlinje. Ingen fetch utført; nåværende GitHub-head er ikke uavhengig kontrollert. |
| Conference release-kandidat | `codex/conference-release-20260930` @ `683c1411ce1f941e89bdb66d2ca9b171a57520ad`; worktree låst i `/private/tmp/conference-release-integration` | Lokal origin/main inneholder merge `fdcfe7a5` for PR276. Bevar arbeidstreet og releasebevis; ikke anta uferdig kildeintegrasjon bare fordi gammel lås står. |
| Moduluttrekk | `codex/event-scaffold-structure` og remote-tracking gren @ `71babb2f7f602e7b47f58aa8b2afaeaf2780c9cb`; rent arbeidstre | Én unik ekstraksjonscommit, 97 commits på origin/main-siden siden felles ancestor. Ikke integrert i origin/main. |

Moduluttrekkets eksisterende arbeidstre er `/Users/kjetil/.codex/worktrees/event-scaffold-structure/CellScaffold`. Dets dokumentasjon sier uttrykkelig at dette er biblioteksgrenser i samme pakke, ikke et selvstendig EventScaffold: `Documentation/Operations/Scaffold_Structure_Implementation_2026-09-22.md:7–15`, `:19–40`, `:89–92` ved `71babb2f`.

Uttrekket flytter 57 kildefiler og tre testfiler, med EventCells, CellConfigurationKit og ScaffoldKit. Studio/Population/Playback/AdminShell blir fortsatt App-celler; modellen, klokke, flere hjelpeklasser og konferansefabrikker flyttes. `UserSimulationScaffoldCore` avhenger bare av CellBase og Vapor, både i origin/main (`Package.swift:249–255`) og den delte arbeidskopien (`:268–274`). Det finnes ingen App/EventCells-avhengighet for å utføre konferansedomenehandlinger direkte fra svermen.

Historisk verifikasjon må avgrenses: `Documentation/Operations/Scaffold_Structure_PR_Verification_2026-09-23.md` ved `71babb2f` rapporterer EventCells-build og strukturelle kontroller som bestått, men App-regresjonskjøring stoppet av kapasitetsvakt og CI ventet da. De 141 tidligere testene gjelder en annen arbeidskopi. Dette er dokumentert historikk, ikke nye kjøringer eller bevis for integrasjon mot `e5c34345`.

Anbefalt WP0-steg:

1. Lås en ren implementeringsbaseline fra en ferskt bekreftet hovedlinje; den lokalt observerte kandidaten er `e5c34345`. Lås også companion-pakker, runtimekonfigurasjon og datarot.
2. Avklar EventCells-uttrekket eksplisitt før store endringer i flyttede modeller/fabrikker. Gjenbruk `71babb2f` som flyttemanifest og reviewbart kildegrunnlag; oppdater det mot valgt baseline uten å overskrive nyere konferanse-/identitetsreparasjoner. Et ukritisk kopi/cherry-pick av den delte arbeidskopiens utrackede mappe vil miste denne kontrollen.
3. La Run være overgangsvert slik uttrekket dokumenterer. Et nytt EventScaffold er et eget vertsarbeid, ikke noe WP9 trenger å late som eksisterer.
4. Bevar nyere `ConferenceConnectionHubCell` fra origin/main. Den har kommet videre enn den gamle delte arbeidskopien, med blant annet deltakerformål og eieravgrenset lagringsfeil/rollback (`Sources/App/Cells/ConferenceMVP/Cells/ConferenceConnectionHubCell.swift:914–934` ved origin/main). Dette beviser fortsatt ikke atomisk kapasitetsreservasjon eller bilaterale kontrakter.

## Dagens Swarm Workbench og kjøreflate

Kilden i `Sources/UserSimulationScaffoldCore/` og `Sources/UserSimulationScaffold/` er byte-lik mellom delt HEAD og lokal origin/main (`git diff --quiet` ga 0), og målrettet status viste ingen arbeidskopiendringer der. Det ble ikke funnet en ny SwarmWorkbench-celle eller -factory i de undersøkte Sources-stiene, og ingen aktuell workbench-gren i refnavnene. Dette er en avgrenset negativ observasjon, ikke inventar over alle andre maskiner/oppgaver.

`Deliverables/PDD_swarm-workbench_2026-09-29/STATUS.md:6–10,20–26` har fortsatt bare grafisk skissegodkjenning 2026-09-30. Dokumentet viser ingen etterfølgende runtimeimplementering. Det er separat fra dagens autoriserte OIW-WP9 og kan utvides under hovedoppgavens godkjenning.

| Lag | Implementert kildegrunnlag | Mangler for WP9 |
|---|---|---|
| Run API | `SimulationRoutes.swift:44–141`: opprett/hent run, pause/fortsett/stopp, users, reconnect/feilinjisering og JSON/Prometheus-metrics; shard/worker-ruter følger i samme fil | Semantisk scenario/forventning/faktisk-resultat er ikke en del av dagens request/resultat. |
| Worker | `SimulationWorker.swift:35–76`: deterministisk brukertildeling, VirtualUserConfiguration, metrics og artifact writer | Injiserbar domeneutfører og kontekst for ekte aktør-/publisher-/Entity-grenser. |
| Atferd | `SimulationModels.swift:49–55`, `VirtualUser.swift:285–310`: lurker, reader, requester, generic AI-conversation, reconnectingMobile, slowSubscriber | Ingen create-event, approve-affiliation, purpose/availability, meeting, shared knowledge, private note eller expected/actual-steg. |
| Scenario | `SimulationModels.swift:128–160`: runId, userCount, shardCount, seed, targets, ramp, mix, topics, bridge | Fixtureversjon/hash, aktørroller, identitetsmanifest, testklokke, forutsetninger, semantiske steg, policy, assert- og cleanupplan. |
| Reproduserbarhet | `SimulationModels.swift:442–469`: stabil identitetskontekst men ny Curve25519-nøkkel | Persistér eller injiser særskilt testidentitetsmateriale; seed alene er ikke nøkkelreplay. |
| Bevis | `VirtualUser.swift:39–74`: events.jsonl, metrics.jsonl, summary.json | Domeneeffektkvitteringer, semantiske assertions, innhold-/fixturehash, kilde-/binærrefs og restkontroll. |
| UI | Eksisterende konferanseadmin og godkjente Swarm Workbench-skisser | Ekte binding fra admin Cell til run API og resultater. Statisk `/swarm/cells`-katalog må ikke brukes som livstegn. |

## Konferanseadmin kan gjenbrukes konkret

Alle følgende referanser gjelder **origin/main `e5c34345`**, slik at det ikke er tvil om gammel kontra flyttet sti:

- `Sources/App/Controllers/VaporConferenceMVP.swift:135–141`: `/conference-admin` → `cell:///ConferenceAdminShell`, `adminOnly`.
- `Sources/App/configure.swift:1735–1763`: Clock, Studio, Population, Playback registreres `identityUnique` og persistent; AdminShell ved `:1842–1846`.
- `Sources/App/Cells/ConferenceMVP/Cells/ConferenceAdminShellCell.swift:783–791`: henter Studio, erstatter dets population/playback-placeholder med reelle celledata.
- Samme fil `:1824–1859`: videresender population- og playback-handlinger til de konkrete cellene; øvrige simuleringshandlinger går til Studio.
- `Sources/App/Cells/ConferenceMVP/Skeleton/ConferenceShellConfigurationFactory.swift:1906`: «Simulation Studio»-seksjonen. `:2033–2056`: start/pause/fortsett/seek/reset, antall deltakere og spawn/reset population; `:2058–2090`: Lists for roller/samtykker/deltakere og Picker/Button for snapshots.
- `Sources/App/Cells/ConferenceMVP/Cells/ConferenceSimulationPopulationCell.swift:293–334`: eksisterende ekte profil/snapshot/samtykkehandlinger gjennom ConferenceOnboarding per syntetisk identitet. `:248–254`: reset sletter bare arbeidssett, ikke lagrede Entities/aggregater.
- `Sources/App/Cells/ConferenceMVP/Cells/ConferenceRecommendationCell.swift:321–325,943`: fortsatt faste directoryCandidates i anbefalingsløpet. En ny dynamisk OIW-fixture alene gjør ikke denne projeksjonen levende.

Forslag til minste admin-skeleton-integrasjon, **ikke implementert i denne runden**:

1. Behold det fungerende admin-referanse-/state-/dispatch-mønsteret. Lag en egen adaptercelle som eier OIW-run-konfigurasjon og autentisert kontakt med eksisterende simulator. Den må ha eksplisitt Explore for konfigurere, validere, starte, pause, fortsette, stoppe og hente resultater.
2. Vis fire tydelige områder med eksisterende Tabs/Picker/TextField/Button/List-byggesteiner: scenario/revisjoner, aktører/rettigheter, kjøring/trinn, bevis/opprydding. Ingen ny skeleton-type er nødvendig for første versjon.
3. Skill `conferenceAdminShell.simulation.start` (konferanseklokke i dag) fra start av et ekte Swarm-run. Ikke gi den gamle knappen ny, skjult effekt. Adapterens egne nøkkelstier må defineres og kontrakttestes før bindende skeleton legges til.
4. Vis forventet/faktisk resultat per semantisk steg, ikke bare grønt transportstatus. En ukjent/ikke-observert celleforbindelse vises som ukjent. Oppgi run-ID, observert tidspunkt og bevisdekning.
5. HTTP-token/proof og target-allowlist ligger på serversiden. Skeleton synlighet brukes bare til presentasjon, ikke autorisasjon. Preview først, deretter varig factory etter verifisert rendering, i samsvar med skeleton-ferdigheten; dagens godkjenning gjør ikke preview til runtimebevis.

Ved senere moduluttrekk flyttes bare factory/import-stien; eksisterende celleendepunkter og data-/eierkontrakter skal bestå. Gjenbruk fra den godkjente Workbench-designen er visuell og informasjonsmessig; ikke dupliser en parallell kjørekoordinator.

## Konkret semantisk gjenbruksvei

Anbefalt vertssplitt: hold `UserSimulationScaffoldCore` fri for App-avhengighet. Innfør en smal, testbar domeneutfører ved worker/VirtualUser-grensen og en versjonert OIW-scenariodefinisjon. På konferanseverten oversetter en adapter et fast sett tillatte domeneoperasjoner til eksisterende resolver-/cell-kall som riktig syntetisk requester. Ikke eksponer vilkårlig endpoint/keypath/principal valgt av browseren.

Bygg først en liten semantisk snitt-test: to publishers, én paraply, to arrangementer, seks syntetiske personer, én avvist rettighet, én deltaker uten treff. Kjør create/publish/read/update-draft, negativ publisher-ACL, ubekreftet/avvist paraplytilknytning og ett ekte nulltreff. Utvid etter hvert til den godkjente fullscenariets 12 personer/3 grupper/4 arrangementer og de to første scaffold-vertene i `CellProtocolDocuments/Deliverables/Conference_OIW_2026-10-02/PLAN.md:50–66`.

Gjenbruk:

- EventPublisherRegistry `publishers.create`, `events.create/update/publish/archive` og publikasjonssnapshots, på origin/main fortsatt `Sources/App/Cells/EventPlatform/EventPublisherRegistryCell.swift:75–87`.
- ConferencePopulation-mønsteret for ekte onboarding-calls, men innfør run-avgrenset fixture og eksplisitt identitetsbinding fremfor å kalle eksisterende demo-reset en opprydding.
- Coordinator/Worker for fordeling, stopp, metrics og failure injection. Domeneassertionens feil må slå ut separat selv om transporten svarte HTTP 200.
- Faktisk eieravgrenset resolver på konferanseverten for publisher/Entity. Ikke la swarm-administrator være stedfortreder for alle deltakere; run-admin og domeneaktør har ulike roller.

Adaptere som må leveres i WP9 eller WP1–WP8:

| Adapter | Minimumskontrakt og avhengighet |
|---|---|
| Fixture/compiler | Låst scenario + fixturehash → run-namespace, aktører, publishers, events og kildereferanser. WP1 paraplymodell kreves for affiliation. |
| Identity/authority | Syntetisk aktør → faktisk requester, vault/proof/mandat og tillatte vertsruter. Versjonert nøkkelmateriale kun for isolert testmodus. |
| Domain executor | Fast operasjonsliste med korrekt requester, correlation/idempotency-ID, resultat og effektkvittering. Ingen provider-/GUI-snarvei. |
| Live matching | Tilkobling til WP3 sin faktiske projeksjon og tid/kapasitet, med samtykke- og rettighetsfiltrering. Dagens faste kandidater må ikke brukes som forventet sannhet. |
| Evidence/assertion | Expected/actual + observerbar effekt/read-back + kildeversjon; negatives for feil publisher/requester, draft-lekkasje og genuine nullresultat. |
| Test clock/isolation | Kontrollert tid og barriers for revokering/konkurranse. Dedikert datarot og namespace; ingen delte demoaggregater. |
| Cleanup/restart | Inventory før/etter, kvittert cleanup og verifisert read-back etter restart. Run-stop betyr bare stop, ikke rollback. |
| Admin bridge | Server-side tilgang til dagens run API; Explore-kontrakter og kontrollflate som viser faktisk semantisk resultat. |

WP5-test må fortsatt krysse to selvstendige prosesser/lagringsgrenser. En lokal Swift-test med to identiteter er nyttig kontrakttest, men er ikke dette transportbeviset. Mikrofon/radio og AI-kvalitet har egne akseptanser og skal ikke simuleres bort av en grønn WP9-status.

## Lokale køer, låser og overlapp

Kun lokale filer inspisert, ingen koordinator/remote claim hentet og ingen claim opprettet:

- `HAVEN-Deploy/queue/tasks/HD-0143.json`: PREPARING, owner codex, konferanseflater.
- `HD-0144.json`: PREPARING, owner codex, konferansemigrering/Workbench-kobling.
- `HD-0145.json`: PREPARING, owner codex, manglende selvstendig ConferenceScaffold; oppdatert 2026-09-29 13:20:28Z.
- `HD-0146.json`: PREPARING, owner codex, samlet staging-/produksjonskvittering; oppdatert 2026-10-05 08:53:32Z. Status alene sier ikke at PR276 er umerget; origin/main viser merge.
- `HD-0164.json`: COMMITTED_VERIFIED, owner codex, release 2026.9.5; oppdatert 2026-10-05 13:10:34Z. Ingen remote deploysertifisering i denne rapporten.
- `HAVEN-Deploy/queue/locks/` hadde ingen filer ved lesingen. Det er ikke bevis for at alle andre claim-systemer er tomme.
- `.agent-spool/inbox/` hadde ingen JSON-jobber. `.agent-spool/running/planlagte-jobber-s3-bygg-20261005.json` lå der med cwd `HavenAgentD/.worktrees/planlagte-jobber-20261002`; dette er kjøringskøstatus, ikke et nytt Swarm Workbench-arbeid.
- Git-låser inkluderer conference-release-integration/HD-0146 og et ferskt bridge-consumer-auth-arbeidstre/HD-0166. Bevar dem. Ingen fersk Swarm Workbench-runtimegren ble identifisert i lokal refnavnesøk.

Køstatus kan være nyere/eldre enn faktisk operasjon; sjekk ansvarlig koordinator før nytt arbeid som overlapper disse filene. Hovedoppgaven har autorisasjon til å koordinere, men denne read-only rådgiveren har ikke sendt meldinger til eksterne oppgaver.

## Ruling

WP0 er konkret gjennomførbar: baseline må løses rundt nyere origin/main og den separat reviewbare EventCells-kandidaten, med companion-/konfigurasjonsrefs og bevarte releasebevis. WP9 har betydelig gjenbruk i scheduler, API, metrics, conference admin-skeleton og onboarding-fixtures. Den semantiske runneren, faktisk domeneprojeksjon, identitetsreplay, expected/actual og cleanupkontrakten må fremdeles bygges. Det finnes ingen kildegrunn til å hevde at en OIW-sverm allerede kan kjøres fra de godkjente skissene.

Parent håndterer integrasjon og sentral læringsfangst. Nyttig læring: alltid skill delt dirty EventCells-uttrekk, ren ekstraksjonskandidat og nyere origin/main; ConferenceAdminShell sin eksisterende simulation-knapp styrer klokke og celler, ikke UserSimulationScaffold-run.
