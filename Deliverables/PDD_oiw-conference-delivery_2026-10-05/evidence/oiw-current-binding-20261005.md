# WP7/WP8 — fersk kildekontroll 2026-10-05

**Brogrunnlaget har flyttet seg siden 2. oktober; møtekjeden er fortsatt en ny leveranse i den undersøkte koden.** CP53 finnes nå i lokal `origin/main`, med en ytterligere, ren scannerkandidat over denne. Sept30-paritetskandidatene er fortsatt rene og separate. De bør integreres selektivt, ikke erstattes med gamle kopier eller beskrives som installert funksjonalitet.

Kontrollen er lokal og read-only. Ingen fetch/nettverk, device-/GUI-test, bygg eller deploy. «Landet» nedenfor betyr tilgjengelig i den lokalt lagrede `origin/main`-historikken; aktiv produksjon og siste eksterne PR-status er ikke kontrollert. Referansekrav: `CellProtocolDocuments/Deliverables/Conference_OIW_2026-10-02/PLAN.md:29–30` (WP7/8), `:34` (to runtime-grenser), `:76–77` (ingen opptak i første pilot, web/macOS først).

## Faktisk nytt og nåværende baseline

| Del | Kontrollert tilstand | Betydning |
|---|---|---|
| Binding ordinært tre | HEAD fortsatt `775fc93db71397022733e8225827d92a9423c803`; 28 modifiserte og 53 utrackede Git-statusposter. Lokal `origin/main`: `8ce634f6533f5e63386229639c69c43aac25c31f` | Ingen ny hovedcommit i dette arbeidsområdet siden forrige audit. Dirty filer kan likevel ha endret seg; audit 2. oktober lagret ikke byte-hasher av alt WIP. |
| CP ordinært tre | HEAD/main fortsatt `253b4afe11af8b58bfcc433d9b7dc7393c761e24`; 2 staged endringer, 5 staged slettinger, 3 utrackede poster ved siste sjekk | Ikke et trygt sted å resette/pulle blindt. |
| CP lokal `origin/main` | **`1ec56d59d13c20edb83b54687aaf393399ad0a15`, 5. oktober: CP53** | Det gamle «CP53 open»-premisset er utdatert for denne lokale historikken. Git viser faktisk koden/committen, ikke bare en statusbeskrivelse. Dette er ikke samtidig bevis på oppdatert Binding-binær eller serverpin. |
| CP scanneroppfølging | **`14181968c8998c4543b42282c3559bc74ed6bddc`**, én ren commit over `1ec56d5`, branch `codex/bridge-scanner-instance-safety-20261005` | Ny kode krever beslutnings-ID for den beholdte invitasjonen/requesten, fryser detaljutvalget og skjermer cleanup mot gamle serviceinstanser. Ikke i lokal `origin/main` ennå. |
| CellScaffold ordinært tre | HEAD fortsatt `942965ca24e9a418b531f9514c1da75d6d529e30`; 154 modifiserte, 59 slettede, 136 utrackede statusposter ved siste sjekk | Store samtidige WIP-mengder. Tallene er statusposter, ikke rekursive filantall. |
| CellScaffold lokal `origin/main` | `e5c3434510884275cae4a732935ab4b55cf7fad9`; 5. oktober-merger #273/#277 for 2026.9.5 | Conference-release-commit `683c1411` er allerede ancestor av denne. Ikke reimplementer/gjeninnfør den pakken. `Package.swift:123–128` pin-er likevel CP **2026.9.4**; CP53s tilstedeværelse i CP main endrer ikke automatisk klientavhengigheten. |

Fersk kildeinspeksjon av `origin/main` og aktuelle arbeidsfiler viser fortsatt disse avgrensningene:

- `Binding/Binding/BindingVoiceInputTranscriber.swift:102–150` er on-device mikrofon→Speech med OS-tillatelser; `:206–220` stopper audio. Filen er byteidentisk med lokal Binding `origin/main`.
- `Binding/Binding/ChatWorkbenchParityCells.swift` ved **origin/main** `:4586–4594` eier transkriberen i `BindingPersonalChatHubCell`; `:6740–6755` beskriver personlig chat-taleinput med composer/analyzeDraft som mål. Det er ikke en felles møtesesjon.
- `CellScaffold/Sources/App/Cells/Transcript/TranscriptStoreCell.swift:188–241` bruker fortsatt `rw--`; `:59–63` har `keepUntilReleased`, automatisk utløpssletting av. Den er byteidentisk med lokal `origin/main`, likeså `ConferenceSessionThreadCell.swift`, hvis handlinger ved `:21–38` fortsatt er melding/draft/invitasjon/medlemskap.
- `Binding/Binding/NearbyScannerSurfaceView.swift` er også byteidentisk med lokal `origin/main`, selv om filen er untracked i den gamle ordinære checkoutens indeks. Dens private-vault requester (`:29–38`) og nil/ukjent respons som suksess (`:55–65`) må ikke bli møtemodellens autorisasjons-/kvitteringsmønster.
- Navnesøk i source-trær og `git grep` i lokal `origin/main` fant ingen møtesesjons-/capture-plan-aggregate (`MeetingSession`, `MeetingCapture`, `CapturePlan`, `RecordingConsent`, `recordingPlan`, `participantApprovals`, `meeting.state/capture/plan`). De direkte primitivekontraktene over ble også lest. Dette er et avgrenset «ikke funnet», ikke et bevis på fravær i alle andre grener eller et gammelt statusnotat brukt som bevis.

## Eksisterende kandidater og arbeid som må gjenbrukes

**WP7, alle tre rene ved kontroll:**

| Arbeidsområde under HAVEN-roten | Commit |
|---|---|
| `Binding/Implementation/SurfaceParityRepair-20260930/workspaces/Binding` | `b18e267d6e103c2bcb2ebda9f91215fc435861f2` |
| `Binding/Implementation/SurfaceParityRepair-20260930/workspaces/CellProtocol` | `41139185b00e2abb7b6c28c212fc64140e60d083` |
| `Binding/Implementation/SurfaceParityRepair-20260930/workspaces/CellScaffold` | `bdc9f8302691d8af7ee16e7f0fa659dddf500fac` |

Ingen av disse tre head-committene er ancestor av sin lokale `origin/main`; direkte tre-differanser viser også gjenværende paritetsfiler. Gjenbruk Binding `BindingSkeletonMountedActionSupport.swift`, `SkeletonPresentationOverlayView.swift` og tilhørende renderer-/snapshot-/mounted-action-tester. Gjenbruk CPs host-theme/control/List/Reference-reparasjoner og native regresjoner. Gjenbruk webendringer i `Public/js/{porthole-webo,skeleton-runtime}.js`, `Public/css/porthole-webo.css` og list/overflow-testene. `VaporSkeletonParity.swift` har ingen differanse mot kandidat i kontrollen; kopier ikke gamle serverendringer ukritisk.

**Integrasjonskollisjon:** CP-paritetsgrenen har merge-base `81601a6` med ny main. Main har etter dette endret `CellListView.swift`, `CellTreeView.swift`, `SkeletonListTree.swift`, `SkeletonDescription.swift`; paritetsarbeidet berører overlappende filer. Bevar både main sin Tree/List-kontrakt og kandidatens rad-/rotkontekst. Ren gammel kandidat er ikke riktig full erstatningsbaseline.

Kandidatens `Binding/SkeletonPresentationOverlayView.swift:52–55` sier i faktisk kode at lyst Porthole-tema velges, mens mørkt beholder native standard. **Conference/mørk paritet i AC7 er dermed fortsatt egen implementasjon/akseptanse**, ikke gitt av tidligere lyse tester. Binding `origin/main:Binding/ContentView.swift:8624–8657` har fortsatt native scanner-substitusjon/foranstilt native radar; test dette separat fra portable skeleton.

**Scannerkandidaten:** `/Users/kjetil/.codex/worktrees/bridge-pr53-integration/CellProtocol`, clean `1418196`. Konkrete grenser: `Sources/CellApple/EntityRadar/EntityScannerCell.swift:418–427` krever `invitationID`; `:662` og `:1566` krever `decisionID`; `:1506–1574` fryser og innsnevrer detaljreferanser; `ScannerService.swift:838–842` matcher beholdt invitasjon. Publiserte UI-handlinger må bevare hele payloaden, ikke bygges om fra bare remoteUUID. Nye kildebaserte regresjoner finnes bl.a. i `ScannerServiceInvitationTests.swift:282`, `EntityScannerConsumerSecurityTests.swift:550,591,663`, `ScannerRetainedStateTests.swift:186,207`. Ikke kjørt i denne vurderingen.

Andre registrerte områder: `_worktrees/binding-cp-253b4af` er clean `cf666783`, men bare en gammel CP-pin-endring, ikke sept30-paritet. `/private/tmp/conference-release-integration` finnes, men mangler `.git`; Git-kommandoer feiler der. Bruk allerede landet commit i ny baseline fremfor å anta at registrert worktree fortsatt er brukbart. Clean `_worktrees/binding-butterpop-knapp` står på Binding origin/main og tilhører annet arbeid; ikke overta det.

## Konkrete eiergrenser for WP8

Følgende nye filnavn er **forslag til implementering**, ikke eksisterende funksjoner:

| Eier | Filer / ansvar |
|---|---|
| Portable domenemodell i CP CellBase | Nye `Sources/CellBase/Cells/Meeting/MeetingSessionModels.swift` og `MeetingSessionCell.swift`, med `Tests/CellBaseTests/MeetingSessionCellTests.swift`. Eie deltakersett, plan/version/hash, opptaksfase/epoch, review-manifest, samtykkebevis og kvitteringer. Normal requester/Resolver/Agreement-policy. Host-eier får ikke godkjenne for deltaker B. Ingen mikrofon/OS-import her. |
| Conference-komposisjon i CellScaffold | Ny `Sources/App/Cells/ConferenceMVP/ConferenceMeetingConfigurationFactory.swift` og minimal registrering/løsning av møtesesjonen. Felles originale skeleton/data for WP7. WP2 eier kilde-/versjonsbundet publisering; WP5 eier faktisk overføring/varig read-back på annen vert. En `TranscriptStore.release`-retur er ikke fjernkvittering. |
| Native Binding | Ny `Binding/BindingMeetingCaptureAdapter.swift` med egen livssyklus, og `BindingTests/MeetingCaptureAdapterTests.swift`. Gjenbruk lavnivå Speech/audio fra `BindingVoiceInputTranscriber.swift`; ikke del ChatHub-instansen. OS-tillatelse, microphone/start/stop, avbrudd og faktisk status her. Ingen tildeling av møtemyndighet eller automatisk publisering. |
| Portable renderer | Gjenbruk kandidatens `BindingSkeletonMountedActionSupport.swift:63,79–101`: aktiv `executionRequesterIdentity`, normal Resolver, manglende SET-kvittering = ukjent, ingen retry. Den støtter bare lokale cell-kilder (`:104–116`); remote WP5 krever egen bevist integrasjon, ikke privat identitetsfallback. |

Viktig native race: `BindingVoiceInputTranscriber.start` venter på tillatelse ved `:106`, og starter tap/engine ved `:145–150`. Adapteren må revalidere gjeldende plan, deltakersett, grant og capture-epoch **etter** denne ventingen og rett før effekten. Et gammelt «ready»-flagg før en tillatelsesdialog er utilstrekkelig. Skill prepare/permission fra et autorisert startpunkt, eller legg en eksplisitt admission-kontroll ved dette startpunktet.

## Liten implementerbar første del

**Lever en portabel møtenotat-/capture-kontrakt med syntetisk adapter og én felles skeleton, uten ekte mikrofon.** Dette lar WP8-modellen gi WP7 et konkret testkorpus mens full transport/device-akseptanse arbeides videre med.

1. To reelle syntetiske testidentiteter i ett isolert runtime, en tredjepart for denial. `invited → joined/noCapture → planPending → ready → syntheticCapturing → stopped → review → approvedSelection`; avslag lar møtet fortsette uten capture.
2. Signert plan bundet til session/domain, deltakersett, exact plan digest, processor, publikum, formål og retention. Bare to gyldige godkjenninger + ferske grants gir synthetic start. Bruk injisert klokke og holdbarriere ved den faktiske adaptereffekten; stop/revoke/deltaker- eller planbytte før frigivelse skal gi null start.
3. Manuelt/syntetisk transkript gir immutable review-versjon og et eksakt utdragsmanifest. Endret tekst/publikum opphever den relevante godkjenningen. Gi separate resultat-/leveringsstatuser, men ikke kall lokal kvittering varig fjernlevering.
4. Én vanlig skeleton viser deltakere, planversjon, status, Stop og review-utvalg i web og faktisk Binding-host. Web `nearby=false`, `microphone=false`; syntetisk adapter merkes tydelig. Korpus dekker compact/wide, lyst/mørkt, stale refresh og denied/unknown outcome. Full AC7/AC8 forblir åpne inntil originale conference-stiler, riktig ny baseline, to fysiske enheter og WP5-grensen er bevist.

Dette er en gjennomførbar første del av de allerede autoriserte arbeidspakkene, ikke en ny godkjenningsforespørsel. Parent håndterer læringsfangst; denne rådgiverslicen endrer ingen kanoniske kilder.
