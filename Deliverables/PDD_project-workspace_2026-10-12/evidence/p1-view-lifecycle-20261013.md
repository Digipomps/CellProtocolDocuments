# P1 — visningslevetid før implementering

Kildeinspeksjon av Codex root 2026-10-13 på CS 3a668044. Dette er et
implementeringsnotat innen godkjent P1/P2/P3, ikke implementert oppførsel,
testresultat eller en ny godkjenningsport. Original PLAN og GUI-referanser er urørt.
Leste områder og hele filenes hasher: p1-view-lifecycle-source-manifest-20261013.json.

## Nytt funn: en transient Orchestrator har fortsatt vertsbivirkninger

`CellScaffold/Sources/App/Cells/SimpleProjectManager/OrchestratorCell.swift`
236-255 oppretter menygrants, forsøker sidecar-lasting og installerer runtime.
`installRuntimeInterceptors` 307-319 kaller
`NativeLocalModelBridgeRegistry.shared.attach(responderUUID: owner.uuid, ...)`.
I `CellScaffold/Sources/App/Support/NativeLocalModelBridge.swift` 123-128
erstatter attach send-callbacken for alle aktive broer med samme responderUUID.
Dermed kan naiv oppretting av én Orchestrator per fane overta modellruting fra
identitetsverten. Dette er utledet fra de leste kallene; det er ikke kjørt en
runtime-reproduksjon.

`saveCellConfiguration` 1253-1258 skriver dessuten CellConfiguration.json før
`persistCurrentConfigurationSnapshot` sjekker persistancy. Å sette en celle til
ephemeral alene er derfor ikke bevis for en visning uten sidecar-skriving.
`loadCellConfiguration` 1055-1126 bytter abonnementer/konfigurasjon og kaller
den samme lagringen. Både vanlige og requester-spesifikke lastebaner må dekkes.

## Konkrete implementeringskrav

1. Skill identitetsvertens oppgaver fra transient visningsruntime før en
   per-view Orchestrator brukes. Visningsrollen skal være bestemt før
   initialisering, ikke settes etter at modellcallbacken allerede er erstattet.
   Den beholder autorisert referanselasting og visnings-Flow, men skal ikke
   re-registrere identitetsvertens native modellkanal eller skrive sidecar.
2. Behold den autentiserte HTTP-sessionen. Legg til et separat view-register
   bundet til bevist requester, session og view/mount. Et view-ID alene er
   ikke rettigheter. Send samme kontekst gjennom HTTP bootstrap/action og WS.
3. Reserver initialisering i registeret før await, slik at samtidige bootstrap
   ikke oppretter to verter for samme visning. Publiser først etter ny
   autoritetskontroll. En generasjon fra før revoke/navigasjon må ikke vinne.
4. Visningens prosjektprojeksjon leser konkret portfolio og eksakt prosjekt-ID
   på requesterens vegne. Skeleton skal ikke få bred portfolio-state og
   filtrere den i nettleseren. Eksisterende portfolio-grants er ikke P5-jobbgrants.
5. Ved logout, utløp og erstatning av visning: trekk tilbake kontekst og
   abonnementer, tøm projeksjon/klientminne og avvis sene hendelser. En enkelt
   WS-reconnect må ikke kaste en fortsatt aktiv HTTP-visning. Ikke innfør en
   periodisk fullskanning av prosjekter som oppdateringsmekanisme.
6. Gjenopprettingsdata i nettleseren er ruteinformasjon. Ny fane må få egen
   runtime-instans også når nettleseren kopierer sessionStorage ved duplisering;
   reload kan gjenåpne den eksplisitte prosjektrefen med ny autorisasjon.

## Avledede kontroller som skal skrives etter grønn baseline

| Scenario | Påkrevd observasjon |
|---|---|
| To views åpner ulike prosjekt-ID-er samtidig | Ulike aktive konfigurasjoner/projeksjoner; legacy selectedProjectID, kildeversjon og bytes uendret |
| To bootstrap for samme view mens kildeoppslag venter | Én runtime; begge svar til riktig requester og prosjekt |
| Opprett view mens lokal modell har aktiv callback | Identitetsvertens modellmelding når samme opprinnelige mottaker |
| Vanlig og requester-spesifikk konfigurering i transient view | Ingen sidecar eller resolver-snapshot-skriving fra navigasjon |
| View-ID/mount-ID gjenbrukt av annen requester | Ingen tilgang til første requesters projeksjon, labels eller tellinger |
| Tilgang trekkes tilbake mens get venter | Intet gammelt snapshot publiseres; ny klientstate er tom/avvist |
| To faner, duplisert fane, reload og tilbake | Prosjektref gjenåpnes eksplisitt uten delt sist-valgt-prosjekt |
| WebSocket kobler til på nytt | Riktig view og prosjekt, kontrollert avstemming; ingen ekstra modellregistrering |

Disse kontrollene er ikke skrevet eller kjørt. Ingen committed tester endres.
Den frosne 112-testbaselinen må foreligge før produktendringer etter PLAN.

## Separat målt avhengighet

AgentD MCP `agent_state_refresh` returnerte siste persisterte runtime-snapshot
med heartbeat 2026-10-13T14:01:11Z: daemon og lokal kontrollbro running,
Porthole failed, bootstrapfeil expired, retryCount 1100 og activeWatchIDs tom.
Dette beviser ikke et nytt live kall mot staging. Det er heller ikke bevis for
prosjektbundet jobbkontroll. Ingen nøkkel, pairing eller bootstrap er endret.
P5 må avstemmes med AgentD-eieren før denne forbindelsen kan regnes operativ.
