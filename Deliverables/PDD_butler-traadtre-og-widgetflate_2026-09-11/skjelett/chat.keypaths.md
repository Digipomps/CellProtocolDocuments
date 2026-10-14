# Chat — data og bindinger

Dette er en strukturkandidat med dagens elementtyper og modifikatorfelter, **ikke en ferdig flate mot uendret PersonalChatHub**. Manglende kontrakter er merket nedenfor; markørene er aldri skrevet i skjelett-JSON. Ingen celledata er endret. Feltforslag er kontraktutkast, ikke implementerte keypaths.

Kildeversjoner, lest 2026-09-12: `git -C CellProtocol branch --show-current` → `pdd/tillitspakke-agentflaate`, HEAD `4096760fe2b47d93d65d143320acfb51b4d50ff7`. CellScaffold står også på `pdd/tillitspakke-agentflaate`; **alle fabrikk-/store-funn her er fra `git show origin/main:<sti>`**, ref `649255bb777b3a5135bd9c50512d3074bd23935b`. `origin/main` er den lokale remote-refen; den er ikke oppdatert over nett.

Kildehenvisningene F og C under er versjonskvalifiserte stier relativt HAVEN-roten:

- **F** = `CellScaffold/Sources/App/Cells/PersonalCopilot/PersonalCopilotConfigurationFactory.swift` på ovennevnte `origin/main`.
- **C** = `CellScaffold/Sources/App/Cells/PersonalCopilot/PersonalCopilotCloudStore.swift` på samme ref.
- **S** = `CellProtocol/Sources/CellBase/Skeleton/SkeletonDescription.swift` i den oppgitte arbeidskopien.

Descriptoren er `Co-Pilot Chat`, label `chatHub` (F:233–238); kilden er `cell:///PersonalChatHub` (`CellProtocol/Sources/CellBase/PersonalCopilot/PersonalCopilotContracts.swift:108–110`). Kandidaten er bare `SkeletonElement`, ikke en ny CellConfiguration. Den forutsetter descriptorens eksisterende cellReference.

## Bindinger som finnes

| Binding | Bruk i kandidaten | Kilde |
|---|---|---|
| `chatHub.state.ui.promptMessages` | Meldingslisten. Beholder dagens liste; hvert element har `id`, `role`, `speaker`, `body`, `status`, `statusText`, `kind`, `purposeRef`, `createdAt` og visse actionpayloads. | F:1394–1407; C:1227 og :1288–1341 |
| `speaker`, `body`, `role` i meldingsrad | Navn, tekst og valg av avatarfarge. Rolleverdiene må være user/assistant/system for de foreslåtte fargevariantene; ukjent rolle må få eksplisitt fallback før aksept. | C:1288–1317; fargekonvensjonen kommer fra mockup :63–65/:204 |
| `chatHub.state.ui.promptMessageCount` | Kilden for det foreslåtte `chatPanelRows[].count/countLabel`; ikke ny tellealgoritme i skjelettet. Ikke direkte Text-binding i kandidaten. | C:1228 |
| `chatHub.state.ui.showStarters` | **Gjenbrukt som datagrunnlag** for 0/1-projeksjonen `starterCards`, ikke som root-visibility. | F:3876–3885, særlig :3880; C:1234–1247 |
| `chatHub.state.ui.starterSuggestions` | Kandidatens startforslag binder direkte til den eksisterende listen. `title`, `summary`, `actionPayload` brukes uendret; `Prøv` sender eksisterende `chatHub.prompt.submit`. | F:1715–1741; C:1238–1247 |
| `chatHub.state.composer.body` | TextArea-lesing. | F:1704–1712 |
| `chatHub.setComposer` | Skriveutkast, ikke send. | F:1706; C:8391–8426 |
| `chatHub.prompt.submit` | Send-knapp, TextArea-submit og `Prøv` med `actionPayload`. | F:1723–1727 og :1758–1761 |

`createdAt` er dagens tidsfelt; et formatert klokkeslett «09:12» er ikke påvist i objektet. Kandidaten bruker derfor den foreslåtte `timeLabel`, ikke en uriktig påstand om at `createdAt` allerede har mockupens format (C:1297/:1316). `speaker` må projiseres som Butler for assistentrader der gammel tekst ikke følger navnekravet; ingen hardkodet personidentitet er lagt i kandidaten.

## Manglende toppdata og visningsprojeksjoner

| Markør | Kontraktforslag og kardinalitet | Begrunnelse/kilde |
|---|---|---|
| `KEYPATH-MANGLER:chatHub.state.ui.chatPanelRows` | Én rad `{mode, title, count, countLabel, scopeDescription, scopeChips, composerTargetLabel, restorePayload}`. `mode` er `expanded` eller `docked`; alle skjematiske betingelser ligger inni denne raden med `scope:item`. | Normal/full-valget kreves av mockup :144–150/:253–263. Ingen tilsvarende panelmodus eller dette radobjektet i C:1218–1264. |
| `KEYPATH-MANGLER:chatHub.state.ui.starterCards` | `showStarters == true ? [{}] : []`. Den ene raden inneholder **fabrikkens eksisterende startkortmønster**, overskrift + eksisterende `starterSuggestions` + `Prøv`. | C:1237 gjør allerede tomhetsavgjørelsen. Ikke lag ny katalog eller ny regel for når forslag skal vises. F:1715–1741/:3880. |
| `KEYPATH-MANGLER:chatHub.state.ui.chatPanelRows[].title` | Valgt nodes tittel. `Butler` i tom tilstand; `Program og sesjoner` i referansens fylte tilstand. | Mockup :254, tilstands-JS :378–388; C:1218–1264 har ikke dette skopfeltet. |
| `KEYPATH-MANGLER:chatHub.state.ui.chatPanelRows[].count/countLabel` | Heltall og ferdig tekst «34 meldinger · 2 grener i skop». Før skopmodellen finnes: projiser dagens `promptMessageCount` og si eksplisitt at det teller dagens liste. Senere må den samme filtrerte meldingsmengden gi både tall og logg. | C:1227–1228; FORMAALSSPEC:63–65; mockup :254. |
| `KEYPATH-MANGLER:chatHub.state.ui.chatPanelRows[].scopeDescription/scopeChips` | Ferdig forklaring + array `{id,label,branchKind}` for grenene i skop. Ikke en liste over alle hjelpere. `branchKind` a/b velger to faste CSS-farger, ikke skopsemantikk. | Mockup :60/:69–71/:255–258; KAPASITET_SKJELETT:14–15. |
| `KEYPATH-MANGLER:chatHub.state.ui.chatPanelRows[].composerTargetLabel` | Ferdig tekst «skriver til: …», fra samme valgte mottakernode som sendingen bruker. | Mockup :325; F:1704–1712 viser bare eksisterende composerbinding. |
| `KEYPATH-MANGLER:chatHub.state.ui.chatPanelRows[].restorePayload` | Stabil panel-ID og siste utvidede modus for `chatHub.ui.restoreChatPanel`. Ingen automatisk gjenbruk av component-surface restore. | Mockup :259–263; KAPASITET_SKJELETT:20 handler om et annet objekt. |

Den første mangelen betyr at kandidaten **ikke viser selve panelet mot dagens uendrede data**. Web vil dessuten vise sitt generiske tomlistesvar. Dette er oppført, ikke maskert med statisk eksempelhistorikk. Å klargjøre ovennevnte projeksjoner er cellearbeid som denne jobben ikke implementerer.

## Nye felt på dagens meldingsrader

Hvert felt nedenfor er et forslag på elementene i den **eksisterende** `chatHub.state.ui.promptMessages`. Fraværet er kontrollert mot feltlisten i C:1288–1341. Listene brukes som 0/1 eller 0/n, uten toppnivå-betingelse.

| Markør | Form / betydning |
|---|---|
| `KEYPATH-MANGLER:chatHub.state.ui.promptMessages[].avatarInitials` | Presentasjonsinitialer, fra avsenderen; Butler kan bruke B. Ingen avledning av identitet i rendereren. |
| `KEYPATH-MANGLER:chatHub.state.ui.promptMessages[].timeLabel` | Lokalisert `HH:mm`; `createdAt` bevares som tidskilde og sorteringsgrunnlag. |
| `KEYPATH-MANGLER:chatHub.state.ui.promptMessages[].branchChips` | 0/1 rad `{id,label,branchKind}` for opphavsgren. En modellbane/lane er ikke en gren. |
| `KEYPATH-MANGLER:chatHub.state.ui.promptMessages[].branchStarts` | 0/1 rad `{eventID, label}` før meldingen som starter en gren. `label` inkluderer «gren startet · …». Skal ikke telles som en ekstra menneskemelding. |
| `KEYPATH-MANGLER:chatHub.state.ui.promptMessages[].componentCards` | 0/n kortobjekter; se under. Program- og endringskort bruker samme kandidatmal; innhold og hvilke handlinger som finnes kommer fra data. |
| `KEYPATH-MANGLER:chatHub.state.ui.promptMessages[].routingFallbacks` | 0/1 rad etter den tilknyttede meldingen med dokumentert avslag og overtakelse. Se A3-kontrakten under. |

En feil kan oppstå flere ganger i en rute. 0/1 her gjelder **oppsummeringen for meldingen**; hele ruten inneholder alle forsøk. Ved selvstendige eventer mellom meldinger må cellen levere en samlet, sortert loggprojeksjon; det løses ikke av List-filter eller SkeletonCondition. Kandidaten plasserer grenstart før og fallback etter tilknyttet melding; endelig eventmodell er utenfor chatkartet (FORMAALSSPEC:54–68; KAPASITET_SKJELETT:14–15).

## Kortobjektet — alle felter under componentCards er foreslått

`KEYPATH-MANGLER:chatHub.state.ui.promptMessages[].componentCards[].{id,title,sourceDescriptor,rows,toolRows,detailRows,footerRows,actionRows}`.

- `id`: stabil kortidentitet, separat fra meldingens ID.
- `sourceDescriptor`: versjonert, dataorientert kildereferanse, minst `{version, componentID, sourceCellEndpoint, sourceElementID, dataKeypath, configurationID, configurationRevision, originMessageID}`. Den identifiserer innholdet i både logg og mottakende flate. Verken serialisert DOM, et bilde eller bare tittelen gir denne identiteten. Detaljene må avtales med flate-tråden. KAPASITET_SKJELETT:18–23; S:557–568.
- `rows`: array `{id,text,muted,stateKind,stateText}`; `stateKind` = ok/warn/idle. Dette er allerede ferdige etiketter, ikke rom-/kapasitetsberegning i rendereren. Kandidaten følger CSSs tre kolonner (mockup :85–91/:284–289/:314–317).
- `toolRows`: 0/1 rad `{expandPayload,hidePayload}` for Utvid/Skjul.
- `detailRows`: 0/1 rad `{detailsPayload}` for Detaljer.
- `footerRows`: 0/1 rad `{sourceChip,summary}`; for eksempel «celle: arendalsuka.program» og «4 av 11 sesjoner». Etiketten er ikke en dokumentert faktisk celleadresse (mockup :290).
- `actionRows`: 0/1 rad `{confirmPayload,editPayload,rejectPayload}`. Payloadene må identifisere samme forslag, kildeobjekt og forventet revisjon; de må ikke ende opp med å godkjenne «siste aktive forslag» ved et uhell (mockup :311–318).

Kortmalen i kandidaten er en vanlig VStack. Gjenbruk ved å kopiere JSON er mulig, men innlasting av én felles definisjon og fortsatt kildeoppdatering er ikke gitt av VStack, Object eller dagens Reference. Det nye `ComponentSurface`-forslaget er bare beskrevet i rapporten, aldri brukt i kandidat-JSON (S:1675–1744/:2747–2771; `CellScaffold/Public/js/skeleton-runtime.js:1511–1537`). Dra-payloadens feltstruktur over er et forslag; kun selve modifierfeltene finnes i dag.

## A3 — rutefallback som celledata

`KEYPATH-MANGLER:chatHub.state.ui.promptMessages[].routingFallbacks[].{messageID,routeID,attemptedNodeID,declinedBy,reasonCode,reasonText,route,takenOverBy,status,detailText,accessPayload,routePayload}`.

Cellen må levere:

1. Kobling til melding og stabil rute-ID, valgt mottaker/skop og kronologisk rute: hvert ledd med hjelper-ID, utfall, avvisningsgrunn og neste hjelper.
2. Hvem som avslo og hvorfor, eksempelvis hjelperen Pressemelding / manglende tilgang til Arendalsuka-cellen. `reasonCode` skal være maskinlesbar, `reasonText` egnet for personen.
3. Bekreftet overtakelse: `takenOverBy = Butler`, og status som skiller ventende ruting fra at Butler faktisk har tatt over. Ikke vis «Rutet til Butler» bare fordi lokal visning feilet.
4. `detailText`, `accessPayload` og `routePayload`. De to payloadene må identifisere denne ruten/meldingen; tilgangshandlingen må i tillegg identifisere den avslåtte hjelperen, målcellen og nødvendig operasjon. «Gi tilgang» åpner et konkret tilgangsvalg; den generiske knappen er ikke i seg selv en innvilgelse.

Dette er utledet kontraktbehov fra FORMAALSSPEC:66–68 og mockup :206–207/:294, ikke eksisterende felter. Dagens `laneLabel`, `routeCorrelationId` og `laneDetailPayload` (C:1299–1334) samt `chatHub.assistant.explainRoute` (F:3555–3571) handler om forklaring av modellruting. De dokumenterer ikke avslag i et hjelpertre; de omdøpes derfor ikke til A3-handlingene.

Uten feil: `routingFallbacks: []`. Med avslag og bekreftet overtakelse: én rad. **Webs tomliste er likevel ikke usynlig**: `CellScaffold/Public/js/skeleton-runtime.js:5753–5759` genererer «Ingen elementer». Native List har egen ScrollView og henter via resolver i stedet for å slå opp den relative listen i gjeldende rad: `CellProtocol/Sources/CellApple/Cells/Porthole/Utility Views/CellListView.swift:172–193`; S:1491–1507. Derfor kreves rendererarbeid selv etter at cellen leverer disse dataene. Å bruke CSS-rollen for Arendalsukas valgfrie lister ville bare gi en webspesifikk omvei (`CellScaffold/Public/css/porthole-webo.css:3171–3174`); kandidaten låner ikke den rollen.

## Explore og ukjente kontrakter

Ingen runtime-Explore-manifest er hentet eller fabrikkert. Eksistens i fabrikk/store er dokumentert, men alle foreslåtte felt/actions mangler bekreftet Explore-kontrakt og faktisk kjørebevis. `CellProtocolDocuments/Tools/Explore/skeleton_explore_validator.py` er en bindingsvalidator, ikke SkeletonElement-dekoderen; se `CellProtocolDocuments/Book/22_Explore_Contracts_For_Skeleton_Authoring.md:289–320`. Neste tråd må hente manifest for den faktiske testkilden, verifisere lesing/skriving og gjøre de foreslåtte projeksjonene konkrete før visuell aksept. Ikke presenter et grønt JSON-strukturresultat som en fungerende samtale.

Henvisninger til FORMAALSSPEC og KAPASITET_SKJELETT utvider til `CellProtocolDocuments/Deliverables/PDD_butler-traadtre-og-widgetflate_2026-09-11/FORMAALSSPEC.md` og `CellProtocolDocuments/Deliverables/PDD_butler-traadtre-og-widgetflate_2026-09-11/handoff/KAPASITET_SKJELETT.md`; «mockup» utvider til `HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html`. Linjenumrene følger etter kolon.
