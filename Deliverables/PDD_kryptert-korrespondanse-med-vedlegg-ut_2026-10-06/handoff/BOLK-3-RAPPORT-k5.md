# Bolk 3 og 5 — k5: diskvakt passert, klientrettinger testet, fullport rød

Oppdraget er ikke fullført. Diskvakten ble kontrollert hvert tiende minutt fra 12:03Z til 16:53Z, 30 målinger over 4 timer og 50 minutter. Første grønne måling: 61,0 GiB ledig; 51,0 GiB og 5 prosent etter 10 GiB reserve. Ingen diskrydding, terskelendring eller leaseoverstyring ble utført. Managed-cache GC ble kjørt i dry-run under bygg, slik at den bare rapporterte kandidater. Testenes ordinære opprydding av syntetiske testfiler er ikke diskrydding.

K3-rapporten ble kopiert byte-identisk til BOLK-3-RAPPORT-k3.md før denne rapporten ble skrevet; SHA-256 e5dc27f68864486f74c3e5179e866d84b7505bab60470a3a0fd45626241f5621. K2-kopi og native-utkastet fra k3 er bevart. Faktisk SwiftPM-checkout ble kontrollert mot pålagt p5-hode 36959ae4a114503b08ff85785e0d73f865d4758e.

| Krav | Test | Utfall | Bevis |
|---|---|---|---|
| Vent på uendret diskvakt, høyst seks timer | Timinuttersmonitor | Vakt passert etter 4t50m; monitor avsluttet | k5-capacity-monitor.log |
| Baseline mot faktisk p5-avhengighet | Bane c, managed build med fjernresolusjon | Bygg grønt. Seks tidligere bundles: 324 tester grønne. Korrespondansebundle: 45 tester, seks issues; fullkjeden exit1 | k5-baseline-private.log; k5-baseline-queue-output.md |
| Bevar privat filnavn i signert kryptert vedleggsmetadata | Eksisterende copyThroughMCPMetadataFetchTransferAndRetainedExport | Grønn etter klientretting: bruk lokale request-metadata, ikke host-planens redigerte filnavn | k5-client-fixes-focused-private.log; samme test grønn i ny fullport |
| Reconnect med samme cache, uten å svekke låsen | Eksisterende admissionTextLargeCopyFlowRenewalAndRevocation; ny shutdownRetiresCacheWithoutDeletingFilesOrReacquiringItsLock | Begge grønne. Eksplisitt client.shutdown frigir gammel cacheeier. Gammel cacheeier kan ikke ta låsen tilbake; beholdte bytes uendret | k5-client-fixes-focused-private.log; k5-fullport-after-fixes-private.log |
| Full port etter rettinger | Ny bane c-kjøring; gamle assertions beholdt | Fortsatt rød: 46 korrespondansetester, fem issues. Native admin ikke integrert | k5-fullport-after-fixes-private.log |
| Uventet closed i broprøven | Isolert bane b-gjenprøve med uendret assertion | Rød igjen: én test, én issue. Baselinen passerte denne testen; årsak ikke fastslått | k5-bridge-recheck-private.log |
| C1/C2/C3: join, kort, profiloppdatering, automatisk fornyelse etter utløp | K3-utkast bevart utenfor produktkoden | Ikke fullført eller vist. Ingen GUI-/LAContext-akseptanse | k3-native-draft/; BOLK-3-RAPPORT-k3.md |
| Samlet formålsprøve mot faktisk PR #286-vert og tre vaults | Krever videre integrasjon og grønne porter | Ikke kjørt. Socket-fixturen er ikke faktisk PR #286-vert | Ingen ny slik evidens |
| Commit, push, kladd-PR, CI | Krever grønn fullport | Ikke utført | Ingen commit/push/ny PR/CI |
| Bolk 5: ren eksport, universal2, Developer ID, notarisation, staple | Krever alt ovenfor grønt | Ikke bygget. Ingen ny pakke eller installerhash | Ingen pakke |

Bevisfilene med k5-prefiks ligger under `HAVEN-Deploy/_handoff/KORR-UT/bolk3/`. `k5-verification-summary.json` registrerer kildehashene og resultatene; `k5-client-changes.diff` bevarer den nåværende klientdiffen, inkludert arvet arbeid. Bare to k5-produktrettinger er gjort: filmetadata og cacheavslutning; den eksisterende reconnect-fixturen er oppdatert til å avslutte gammel klient, og en ny cachelivsløpsprøve er lagt til. Native-utkastet er ikke lagt inn i produktets Sources/Tests.

## Konkret kontraktgrense i p5

Den bevarte `sourceModesAreObservedAndNeverOfferTransfer` krever vellykket registrert-sourceID med fetchOnDemand/reference. Den pinnede `CorrespondenceCell` har derimot uttrykkelig:

- `attachments.probe`: kaster unavailable; ingen kildeprobe på denne wire-flaten.
- `attachments.prepare`: krever sourceID == nil; ellers contextMismatch.

Dermed kan ikke disse eksisterende success-forventningene bli grønne gjennom en HavenAgentD-adapterretting som beholder samme protokollrute og semantikk. Å endre CP, fjerne prøven eller gjøre forventet kildeleveranse til forventet avslag er utenfor denne videreføringens grense. Ingen slik endring er gjort. Upstream må avklare/implementere kildemoduskontrakten, eller oppdragseier må avgrense den uttrykkelig før fullport og pakking kan bli grønne. Det er ikke hevdet at copy-overføring er blokkert; den er vist begge veier i socket-fixturen.

To andre vedleggsissues må vurderes hver for seg, ikke oppgis som påviste CP-produktfeil:

- legacyAgreementCannotUseAttachmentActions forventer en kastet feil fra Resolver, men får ingen exception. MCP-avslaget passerer; den returnerte Resolver-verdien er ikke klassifisert i k5.
- senderOwnedCellAndSignedAgreementSurviveSnapshotReload får attachmentUnavailable. Fixturen rebinder ikke den gjenopprettede cellens betrodde vedleggsrot; beslutningens lokale host-binding må brukes og prøves før man krever CP-endring.

I tillegg feiler authenticatedVaporBridgeDeliversEnvelopeWithoutPolling med closed i ny fullport og isolert gjenprøve. Cachepositive og avslag for detached/foreign vault blir observert først; push-konvolutten blir ikke vist i disse to kjøringene. Årsaken er uavklart. De to klientrettingene berører ikke broadapteren; dette er ikke tilstrekkelig til å kalle utfallet flaky eller frikjenne klienten.

## Kapasitet og leveransegrense

Etter første bygg falt ledig plass til 56,1 GiB og vakten blokkerte en frisk kontroll. Neste fokuserte jobb passerte igjen på 56,4 GiB; ingen vakt ble overstyrt. Managed-cachetotalen ble omtrent 14,3 GiB, over eksisterende 12 GiB-cap; runneren rapporterte en GC-kandidat, men slettet den ikke. Cap og retensjon er ikke endret. Dette er fortsatt en kapasitetsbegrensning for videre arbeid, ikke en ryddefullmakt.

K5 stopper ved den påviste CP-kildemodusgrensen og den røde fullporten. Ingen merge, deploy eller sending til noen; prøvene brukte syntetiske identiteter og lokale testverter. Ingen påstand om at native admin, etter-utløp-fornyelse eller pakking er ferdig. K3s øvrige sikkerhetsfunn gjelder fortsatt. Eierens eksisterende nøkkel er ikke isolert fra andre prosesser som samme OS-bruker; egen nøkkelgruppe og ekte LAContext er fortsatt ikke vist.

## PR #28 og #30

K2s anbefaling beholdes som historisk vurdering: #28s CI-fasevakt/direkte Swift Testing-kjører er i det arvede arbeidet; provenance-funksjonen skilles ut/rebases. #30 rebases på verifiserte fasehelpere og krever ny full CI før merge. Ingen ny GitHub-statuskontroll, merge eller lukking i k5.

## Læringsfangst

L-2026-10-08-klientbaseline-mot-cp-36959ae-avviser-registrert er captured/applied; dokumentmål `CellProtocolDocuments/Book/33_Correspondence_First_Class.md` er oppdatert. Sync markerer dokumentmål som git-distribusjon; dokumentet er ikke committet/pushet i denne jobben. Global strict-check er fortsatt rød på eldre andres poster; egen post er applied/synced i verktøyets dokumentforstand.

STATUS: STOPPET — p5 avviser kildemodusene som bevarte tester krever; fullport fortsatt rød, broens closed uavklart; ingen PR eller pakke.
