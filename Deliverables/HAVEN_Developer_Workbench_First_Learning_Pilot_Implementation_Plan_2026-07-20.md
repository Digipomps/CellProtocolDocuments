# HAVEN Developer Workbench — implementeringsplan frem til første læringspilot

Dato: 2026-07-20
Status: **blokkert og køklar**; implementasjon skal ikke starte før `ADMIN-GO`
Beslutningseier: Kjetil
Koordinerende oppgave: Codex-oppgaven «Evaluer admin-tjenesten» (`019f5bc3-a21e-7502-855d-6f1f3bd567e7`)
Tekniske eiere: må tildeles per repo ved oppstart
Dataklasse: intern prosjektplan; ingen API-nøkler, promptinnhold, kildekode eller pilotidentitet

## Utførende konklusjon

Arbeidet skal **ikke startes nå**. Adminoppgaven er 2026-07-20 aktiv i en alvorlig identitets-/recovery-hendelse, og skal ikke avbrytes eller få en ny implementasjonsgren blandet inn i dette arbeidet. En separat utviklingsstatusflate er merget, mens snapshotprodusenten ligger i draft-PR #36 med GitHub Actions blokkert før runnerstart av kontoens betalings-/spending-limit-status. Produsenten mangler dessuten upstream-adaptere, faktiske CellProtocol-grants og stagingakseptanse.

Dette hindrer ikke at planen legges i kø nå. Når `ADMIN-GO` er oppfylt, skal adminoppgaven starte en **egen Codex-oppgave i isolert worktree**, ikke implementere Developer Workbench inne i sin egen incident-/releasegren.

Første leveranse er en smal vertikal sløyfe:

> idé eller lite oppdrag → lokal prosjektmappe → lokal Codex/agent → typede endringer → bygg → browser-preview → feil tilbake til agenten → diff/snapshot

Providerpanel, egen API-nøkkel og mer avansert onboarding kommer etter første kjørende resultat. Phaser er første spillstack. Ingen spillmotor eller web-runtime bundtes i Binding.

## Autoritative innganger

- [Utviklermiljørapport](./Utviklermiljo_HAVEN_CellProtocol_Rapport_2026-07-20.md)
- [Rådgiverpanel for første læringspilot](./HAVEN_Developer_Workbench_First_Learning_Pilot_Advisory_2026-07-20.md)
- `Tools/ModelKnowledge/panels/dev_environment_first_pilot_2026-07-20.json`
- `Deliverables/Personlig_Butler_Onboarding_Plan_2026-07-20.md` — eksisterende, foreløpig untracket plan som overlapper `GuidedOnboardingCell`, profilfelter og Binding-paritet; må samordnes før kodearbeid
- CellScaffold draft-PR #36: `codex/development-status-snapshot-producer-20260720`, head `76883c364ab1502ea8aaa3c55d595b1143e37790`

Adminstatusen er tidsfølsom. Adminoppgaven skal lese status på nytt før `ADMIN-GO`; denne planen er ikke autoritet for senere PR-, CI-, staging- eller incidentstatus.

## Formål og mål frem til pilot

Planen arver formålene fra rådgiverleveransen og oppretter ingen nye `purpose://`-referanser.

| ID | Formål | Implementeringsmål | Bevis | Nåstatus |
|---|---|---|---|---|
| I1 | `purpose://project-work.overview-and-sharing` | Én eksplisitt Developer Workbench-flate gir prosjektstatus, progresjon, kjør/stopp, resultat og snapshot | Skeleton/Explore-validering, Porthole-preview, reload-test | Blokkert av `ADMIN-GO` |
| I2 | `purpose://access.audit.privacy` | Staging kan bare sende typede høynivå-intenter; lokal AgentD er autoritet og hemmeligheter forlater ikke maskinen | Negative autorisasjonstester og trafikkfangst | Blokkert av `ADMIN-GO` |
| I3 | `purpose://gui.quality.functional-accessible` | Første selvvalgte, avgrensede prosjekt kjører innen 60 min uten at foresatt overtar tastaturet | Clean-room og observert økt | Blokkert til funksjonen finnes |
| I4 | `purpose://test.acceptance.project-work` | ChatGPT/Codex-ruten og egen API-nøkkel/panel-ruten virker ende-til-ende | Funksjonelle artefakter, revoke/replay/denial-tester | Blokkert; adaptere mangler |
| I5 | `purpose://test.acceptance.project-work` | Ett Phaser-prosjekt kan opprettes, endres, bygges, kjøres og gjenopprettes uten motorbytes i Binding | 10 clean-room-scenarier og Release-størrelsesdelta | Blokkert til vertikal slice er bygget |
| I6 | `purpose://prompt.unknown` | Kandidat: «developer-learning pilot in HAVEN» er klar for menneskelig go/no-go | Samlet pilot-readiness-pakke signert av Kjetil | Blokkert til I1–I5 er tilfredsstilt |

G2 fra rådgiverrapporten — frivillig andel HAVEN-økter etter to uker — ligger **etter** første pilot og er ikke et før-pilot-kriterium.

## Påstandsdommer som styrer sekvensen

| ID | Påstand | Dom | Konsekvens |
|---|---|---|---|
| Q1 | Implementasjonen kan startes nå uten å komme i veien for adminarbeidet | Motsagt | Aktiv identitetsrecovery har høyere risiko og deler CellScaffold-/releasekontekst |
| Q2 | Adminoppgaven bør selv implementere Developer Workbench på sin aktive gren | Motsagt | Admin er koordinator og releasegate; implementasjon delegeres til egen oppgave/worktree |
| Q3 | Draft-PR #36 må være merget før noe pilotarbeid kan begynne | Motsagt i sterk form | PR #36 er nyttig for synlig kø, men ikke teknisk forutsetning for kontrakt/AgentD-arbeid; køen er dokument+oppgavemelding frem til live ingest finnes |
| Q4 | Den eksisterende butler-onboardingen kan gjenbrukes uten koordinering | Åpen | Den dekker verdi-først, providerstige og Binding-paritet, men deler filer og kontrakter; én felles eier må avklare forholdet før kode |
| Q5 | En generell in-app webpreview finnes allerede | Motsagt | Første pilot bruker ekstern systemnettleser; ny WebView/renderer krever egen beslutning |

## `ADMIN-GO`: hendelsesstyrt startport

Ingen kalenderdato settes nå. Adminoppgaven kan markere arbeidet `ready` og starte en egen oppgave først når **alle** punktene er sanne:

1. **Identitetshendelsen er terminal for gjeldende operasjon.** Ingen live recovery, vault-/database-/identitetsmutasjon, cutover eller rollback kjører. Den autentiserte brukerreisen er enten bevist frisk eller hendelsen er eksplisitt isolert med dokumentert restfare.
2. **Release/deploy-vinduet er rolig.** Ingen aktiv stagingdeploy, rollback, migrasjon eller primærgrenoperasjon berører samme CellScaffold-/Binding-/AgentD-flater.
3. **Arbeidskopi er isolert.** Ny oppgave får egen `codex/*`-gren og worktree fra verifisert base. Den skal ikke arve adminoppgavens incident-worktree eller skitten primærtretilstand.
4. **Filansvar er reservert.** Adminoppgaven kontrollerer aktive oppgaver/PR-er og registrerer én eier for hver delt fil eller modul før parallelle spor starter.
5. **Onboardingplanene er samordnet.** `Personlig_Butler_Onboarding_Plan_2026-07-20.md` og denne planen får én felles beslutning for `GuidedOnboardingCell`, `PersonalAssistantProfileCell`, providerstigen og Binding sync/paritet. Ingen dupliserte profilfelt eller parallelle scripts med samme ansvar.
6. **PR #36-status er registrert, ikke antatt.** Admin oppdaterer købeviset med aktuell merge-/CI-/stagingstatus. Manglende PR #36 kan gi manuell køstatus, men må ikke fremstilles som live adminstatus.
7. **Første arbeidspakke er avgrenset til M0.** Admin starter kontrakt-/trusselmodellpakken først. Kodepakker starter først etter M0-godkjenning.

Hvis ett punkt er falskt eller ukjent, forblir status `blocked`.

## Repo- og eierskapsgrenser

| Repo | Eier i denne leveransen | Skal inneholde | Skal ikke inneholde |
|---|---|---|---|
| CellProtocolDocuments | Kontrakt-/beslutningseier | Jobbkontrakt, threat model, ADR, testmatrise, pilotrunbook | Appspesifikk kode eller oppdiktede protocol-semantikker |
| Binding/HavenAgentD | Lokal runtime-eier | Typet jobbeksekvering, lokal prosjektrot, Codex-/provider-adapter, credential-bruk, loopback preview | Generell shell fra staging eller serverstyrt nøkkelinntasting |
| CellScaffold | Staging-/Workbench-eier | DeveloperWorkbenchCell/CellConfiguration, presenterende skeleton, typede intents og sanitert eventvisning | Lokal autoritet, lokale stier, secrets eller prosesskontroll |
| Binding | Native host/paritet | Rendre eksisterende portable skeleton; lokal status/samtykke dersom kontrakten ikke kan løses portabelt uten å lekke secrets | Bygge/installere/starte AgentD eller bundle spillmotor |
| CellProtocol | Bare hvis M0 avdekker ekte delt kontraktgap | Portabelt, appuavhengig kontraktarbeid med egne tester | Pilot-/Phaser-/Codex-spesifikk policy |

Hvis implementasjonen krever endret resolver-, identitets- eller capability-semantikk, stoppes sporet og går gjennom egen `cellprotocol-identity-capability-security`-/core-runtime-vurdering.

## Implementeringssteg

### M0 — kontraktfrys og konfliktaudit

Mål: gjøre grensene testbare før runtimekode.

Leveranser:

- `haven.developer-job.v1`: typet jobb-envelope med `jobID`, formål, dataklasse, prosjektref, tillatt handling, idempotensnøkkel, utløpstid og lokal samtykkestatus;
- eventkontrakt for `queued`, `awaitingLocalConsent`, `running`, `diagnostic`, `artifactReady`, `failed`, `cancelled`, `completed`;
- handlingallowlist: `createProject`, `applyPatch`, `build`, `runPreview`, `stop`, `snapshot`, `restoreSnapshot`, `openExternally`;
- eksplisitt forbud mot raw shell, vilkårlige paths, secrets og nettverksdestinasjoner fra staging;
- threat model for kompromittert staging, replay, symlink/path-flukt, prosessbarn, reconnect, stor output og providerkostnad;
- fil-/modulkonfliktkart mot aktive admin-, onboarding-, Binding- og AgentD-oppgaver;
- felles beslutning om hvordan developer-onboarding komponeres med butler-onboarding.

Port: kontrakten og negative krav er reviewet; ingen app/runtimekode før dette.

### M1 — lokal jobbkjerne i HAVENAgentD

Mål: bevise sikker lokal utførelse uten staging og uten ekte provider.

Implementer:

- lokalt mappevalg og kanonisk prosjektrot;
- symlink-/path traversal-forsvar per jobb;
- typet allowlist-dispatch uten kommandotekst fra nettverk;
- jobblås/idempotens, timeout, CPU-/minne-/outputgrenser og kansellering av prosess-tre;
- dependency-/nettverkssamtykke som egen lokal port;
- append-only, sanitert jobbhendelse med korte artefaktreferanser;
- fake executor og fake provider for deterministisk test.

Port: alle positive/negative tester passerer lokalt; restart/reconnect og dobbel levering gir ikke dobbel jobb.

### M2 — lokal Codex-rute for ChatGPT-abonnement

Mål: bruke Codex lokalt uten at HAVEN leser autentiseringsmateriale.

Implementer bak egen adapter:

- capability-detection og pinnet, testet Codex-versjon;
- kun status `signedIn`/`signedOut`; aldri token/cookie/cacheinnhold;
- lokal tråd/turn, progresjon, approvals, kansellering og avgrensede resultathendelser;
- adapter rundt `codex app-server` eller annen offisiell lokal Codex-flate, med kontrakttester fordi app-server er eksperimentell;
- alltid tilgjengelig «Åpne i Codex»-fallback.

Port: clean-room login/utlogging/avslag/restart; trafikkfangst viser at token ikke går til staging/AgentD-logg.

### M3 — lokal nøkkel- og rådgiverpanelrute

Mål: registrere og bruke egen API-nøkkel uten at staging eller Workbench-DOM ser den.

Først må renderer-/hostauditen avgjøre om lokal secure input finnes. Dagens søk fant ingen generell `SecureField`/`isSecure`-egenskap i portable skeletons. Hvis dette bekreftes, brukes en dedikert lokal native/AgentD-flate; det skal ikke simuleres med vanlig `TextField`.

Implementer:

- lokal registrering/rotasjon/revoke med fake key først;
- engangsautorisasjon bundet til provider, modell, formål, dataklasse, prompt-hash, jobb, kostnadsgrense og lokal godkjenning;
- håndheving av spendgrense og DPA/providerstatus, ikke bare lagring av metadata;
- lokal provider-adapter som bruker `SecretCredentialCell` uten å returnere rå nøkkel;
- `AdvisorPanelSpawnService` → lokal providerjobb → sanitert panelresultat;
- leverandør-/mottaker-/kostnads-/aldersinformasjon før første ekte kall.

Port: fake provider komplett; deretter ett eksplisitt godkjent testkall med offentlig/syntetisk innhold, revoke/replay/expiry/overspend/DPA-negative tester.

### M4 — Developer Workbench i CellScaffold

Mål: en staging-servert presentasjonsflate som ikke blir lokal autoritet.

Implementer først som runtime `CellConfiguration`/skeleton-preview:

- valg: «Bygg min idé», «Remiks» eller 2–3 små oppdrag;
- prosjektmål: én scene, én mekanikk, ett suksesskriterium;
- tilkoblings-/samtykkestatus, progresjon, filer i relativ form, diagnostikk og artefakt;
- kjør/stopp, snapshot/angre og «åpne eksternt»;
- code block/copy bare der kode vises;
- ærlige tom/avslått/frakoblet/utdatert/feilet-tilstander.

UI binder bare til reelle Explore-keypaths. Preview/commit og reload testes før eventuell Swift factory-promotering. Ingen nytt skelettelement eller `webembed` i denne pakken.

Port: Porthole-preview, Explore-validering, reload, browserakseptanse og null secrets/absolutte stier i DOM/nettverkslogg.

### M5 — staging↔lokal integrasjon

Mål: koble M4 til M1–M3 uten å flytte autoritet til transporten.

Implementer:

- signert, kortlivet nonce og typet intent fra Workbench;
- Porthole som transport, ikke autoritet;
- lokal resolver/policy og lokal consent før utførelse;
- idempotent status/event-resume etter frakobling;
- bounded diagnostics, diff og artefaktreferanser tilbake;
- fail-closed ved tomt bridge-token, feil `Host`/`Origin`, utløpt/replayet intent eller ukjent handling.

Port: kompromittert-staging-testpakken klarer ikke å kjøre raw shell, forlate prosjektrot, hente secret eller omgå lokalt samtykke.

### M6 — første spillvertikal med Phaser

Mål: første synlige resultat uten Binding-bloat.

Implementer:

- én liten Phaser 3-mal i vanlig JavaScript, ferdige lokale assets og ingen package lifecycle-scripts i første økt;
- konkret Phaser-versjon velges etter 10-case clean-room-test, ikke før;
- AgentD loopback static server med tilfeldig sesjonstoken og validerte `Host`/`Origin`;
- preview i systemnettleser;
- bygg/run/error/snapshot gjennom samme jobbkontrakt.

Port:

- 10 kjente oppgaver fra ren maskin/prosjektbase;
- motor/runtime bundlet i Binding = 0 byte;
- ren Release-delta mål ≤1 MiB, hard stopp >5 MiB mot identisk baseline;
- Godot, WebView og flere motorer forblir utenfor.

### M7 — integrert første-60-minutters onboarding

Mål: komponere eksisterende onboarding, ikke bygge en konkurrerende motor.

Sekvens:

1. lokal datamodus og foresattflyt ved behov;
2. idé/remiks/oppdrag;
3. agent avgrenser første spillbare skive;
4. AgentD-health og lokalt mappe-/handlingssamtykke;
5. Codex-rute eller lokal demo/fake provider;
6. mal → endring → bygg → preview → én brukerbestemt endring;
7. diff, snapshot/angre og neste steg;
8. valgfritt API-nøkkel-/paneloppsett etter første suksess.

Samordning med personlig butler:

- gjenbruk `GuidedOnboardingCell`, verdi-først-prinsipp og capability/providerstige dersom den planen lander;
- developer-spesifikke steg får eget versjonert script og overtar ikke persona-/profilansvar;
- felles providerbeskrivelse/policy-port defineres én gang;
- samme skeleton må parity-testes i Porthole og Binding.

Port: intern clean-room med fake identitet/credentials; deretter observert test med nybegynner uten at voksen overtar tastaturet.

### M8 — samlet pilot-readiness

Mål: bevise at det er forsvarlig å invitere pilotbrukeren.

Obligatorisk evidens:

- alle to provider-veier: happy path, avslag, frakobling, restart, revoke og gjenopptakelse;
- trafikkfangst for nøkkel/token/absolutt sti;
- raw-shell/path/symlink/replay/expiry/network/resource/process-tree-negative tester;
- 10 Phaser-scenarier og Release-størrelse før/etter;
- staging funksjonsverifisering uten produksjonsdeploy;
- Porthole/Binding-paritetsmatrise;
- lokal innholdsfri måling, synlig sletting/eksport og ingen prompt/kode/minor-identitet;
- pilotrunbook, rollback og en énknapps «åpne i Codex»-fluktvei;
- foresatt-/leverandørvilkår og samtykke avklart før ekte ekstern provider.

Kjetil tar go/no-go. Adminoppgaven kan vise readiness og manglende bevis, men skal ikke selv erklære produktsikkerhet uten evidensen.

### M9 — første pilot

Dette er første handling **etter** implementeringsplanen:

- kjør én observert økt med tidslinje og hjelpenivå;
- stopp ved secret-/identity-/stagingavvik eller manglende lokal consent;
- registrer usability- og integrasjonsfeil, ikke «produktvalidering»;
- etter retting kan to ukers frivillig G2-måling starte;
- generalisering krever senere minst to ubeslektede nybegynnere.

## Parallellisering uten kollisjon

Etter M0 kan admin starte maksimalt disse to parallelle sporene:

- Spor A, `Binding/HavenAgentD`: M1 og deretter M2/M3.
- Spor B, `CellScaffold`: M4 som runtime skeleton/kontrakt med fake events.

M5 starter først når begge har stabile, testede kontrakter. M7 starter ikke parallelt med personlig-butler-arbeid i delte onboarding-/profil-/Binding-filer uten eksplisitt, filnivå-eierskap. M6 kan bygges etter M1 i AgentD-sporet, men må ikke legge motoravhengighet i Binding.

CellProtocol-kjerneendringer, stagingdeploy, identitetsarbeid og admin/releasearbeid skal aldri «tas med» som sideeffekt i disse sporene.

## Køpost for fremtidig WorkItemCell

Fordi ingen skrivbar WorkItemCell-runtime var tilgjengelig i denne oppgaven, er denne filen den varige køposten. Adminoppgaven kan senere registrere samme innhold via `workItems.capture` uten å endre semantikken.

```json
{
  "title": "Bygg HAVEN Developer Workbench frem til første læringspilot",
  "kind": "feature",
  "status": "blocked",
  "confidence": "needs-verification",
  "project": "HAVEN Developer Workbench",
  "source": "codex",
  "labels": ["developer-workbench", "learning-pilot", "admin-coordinated", "local-first"],
  "summary": "Implementer en smal staging→lokal læringssløyfe med lokal AgentD-autoritet, Codex-abonnementsrute, valgfri lokal API-nøkkel/panelrute og Phaser browser-preview uten Binding-bloat.",
  "nextAction": "Adminoppgaven re-evaluerer ADMIN-GO og starter M0 i en egen isolert Codex-oppgave når alle startporter er sanne.",
  "doneWhen": "M0–M8 har grønn, sanitert evidens og Kjetil har tatt eksplisitt go/no-go for første pilot.",
  "blockedBy": [
    {
      "targetRef": "codex-thread:019f5bc3-a21e-7502-855d-6f1f3bd567e7",
      "summary": "Aktiv identitets-/recovery-hendelse og releasekoordinering må være terminal før ny implementasjon startes."
    },
    {
      "targetRef": "decision:onboarding-shared-ownership",
      "summary": "Developer- og personlig-butler-onboarding må få én eier for delte celler, profilfelt og Binding-paritet."
    }
  ],
  "evidence": [
    {
      "type": "note",
      "source": "Deliverables/HAVEN_Developer_Workbench_First_Learning_Pilot_Advisory_2026-07-20.md",
      "summary": "Rådgiverdommer, sikkerhetsarkitektur og pilotscope."
    },
    {
      "type": "note",
      "source": "Deliverables/HAVEN_Developer_Workbench_First_Learning_Pilot_Implementation_Plan_2026-07-20.md",
      "summary": "Implementeringsrekkefølge, startporter, repoansvar og pilot-readiness."
    }
  ]
}
```

## Admininstruks ved avblokkering

Når `ADMIN-GO` er sann:

1. Oppdater køstatus fra `blocked` til `ready` med konkret evidens, ikke bare en vurdering.
2. Start en ny Codex-oppgave med M0 og lenker til begge rapportene og denne planen.
3. Bruk isolert worktree og avtal filansvar før parallelle spor.
4. Be den nye oppgaven rapportere tilbake commit/PR/testbevis og blockers til adminoppgaven.
5. Ikke deploy, merge eller gå til M1 før M0-kontrakten er godkjent.

Hvis adminoppgaven ikke har WorkItem-ingest i drift, er en oppgavemelding med denne commitens SHA og eksplisitt status `blocked` tilstrekkelig købevis.
