# Chat — handlinger og akseptansekontrakt

Omfang: bare logg-/kortpanelet. Formål `purpose://candidate.butler.surface-as-workbench`, A3/B1 og C1/C2. Ingen handling er utført. Tabellen er en kontrakt for senere reachability- og brukertest, ikke en attest på nåbarhet. Skopvalg i treet og slippmålets lagring tilhører de to andre delene.

**F** nedenfor er `CellScaffold/Sources/App/Cells/PersonalCopilot/PersonalCopilotConfigurationFactory.swift` lest med `git show origin/main:…`, ref `649255bb777b3a5135bd9c50512d3074bd23935b`. **M** er `HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html`. Alle navn merket KEYPATH-MANGLER er forslag, også når de står som action-keypath i kandidaten.

| Personen skal kunne | Action-keypath / status | Input fra personen eller cellen | Aksept for senere test | Kilde |
|---|---|---|---|---|
| Skrive og endre utkast | `chatHub.setComposer` — finnes | TextArea-tekst; avklart valgt mottaker. | Utkastet lagres uten sending. Samme tekst finnes ved gjenvisning. | F:1704–1712; M:323–326 |
| Sende utkast | `chatHub.prompt.submit` — finnes | Lagret/oppdatert tekst. Kandidaten har både eksplisitt Send og TextArea.submitActionKeypath. | Én sending, ingen dobbel melding; tekst og rutemottaker hører til samme handling. | F:1758–1761; `CellProtocol/Sources/CellBase/Skeleton/SkeletonDescription.swift:1151–1158` |
| Prøve et startforslag | `chatHub.prompt.submit` — finnes | `starterSuggestions[].actionPayload = {text: example}`. | Det valgte eksempelet sendes, ikke gammelt composerinnhold. Startkort forsvinner etter første loggmelding og vises ved reell tomtilstand. | F:1715–1741; `CellScaffold/Sources/App/Cells/PersonalCopilot/PersonalCopilotCloudStore.swift` @ origin/main:1234–1247 |
| Utvide ett loggkort | `KEYPATH-MANGLER:chatHub.ui.expandLogCard` | `expandPayload`, minst kort-ID, kilde-ID og presentasjonsmodus. | Det valgte kortet åpnes; loggens kort/kildereferanse bevares. Må ikke åpne en annen «aktiv hjelper». | M:278–283; KAPASITET_SKJELETT:20–21 |
| Skjule ett loggkort | `KEYPATH-MANGLER:chatHub.ui.hideLogCard` | `hidePayload` med samme kort-ID. | Bare kortets visning skjules; melding og kilde slettes ikke. Reversering og visningsregel må spesifiseres før implementering. | M:282; FORMAALSSPEC:79–87 |
| Se endringsdetaljer | `KEYPATH-MANGLER:chatHub.proposal.showDetails` | `detailsPayload`, forslag-ID og kildeobjekt. | Viser det samme rom-/kapasitetsforslaget som kortet. | M:311–317 |
| Bekrefte et forslag | `KEYPATH-MANGLER:chatHub.proposal.confirm` | `confirmPayload`: forslag-ID, målobjekt, forventet revisjon. | Endringen går til riktig celle én gang; kort og festet variant følger bekreftet kildeutfall. Avslag/konflikt vises og teller ikke som bekreftet. | M:311/:318; FORMAALSSPEC:85–87 |
| Endre et forslag | `KEYPATH-MANGLER:chatHub.proposal.edit` | `editPayload` med forslag-ID. | Personen kan endre utkastet før ny bekreftelse; ingen utilsiktet kildemutasjon. | M:318 |
| Avvise et forslag | `KEYPATH-MANGLER:chatHub.proposal.reject` | `rejectPayload` med forslag-ID. | Dette forslaget avvises; ingen romendring sendes. Dagens `assistant.dismissSuggestion` er ikke uten videre denne objektrettede operasjonen. | M:318; F:3545–3548 |
| Dra kortet til flaten | Modifierne `draggableRole`, `dragPayloadKeypath`, `dragPreviewRole`; **ingen kilde-action ved dragstart** | Rolleforslag `component-surface`, payload fra kortets `sourceDescriptor`, previewrolle `component-card`. | Riktig kort/kilde følger med; ghost viser kortet; avbrutt drag muterer ingenting. Mottaker må godta denne rollen og teste konkret drop-action; avtal keypath med flate-tråden. | `CellProtocol/Sources/CellBase/Skeleton/SkeletonDescription.swift:557–568`; `CellScaffold/Public/js/skeleton-runtime.js:4835–4863` |
| Åpne tilgangsvalg fra rutefallback | `KEYPATH-MANGLER:chatHub.routing.requestAccess` | `accessPayload`: routeID/messageID, avslått hjelper, målcelle, nødvendig operasjon. | Viser riktig tilgangsforespørsel for dette avslaget. Eventuell innvilgelse og retry må ha definert utfall før testen kan godkjennes. | M:294; FORMAALSSPEC:66–68 |
| Se ruten som faktisk ble brukt | `KEYPATH-MANGLER:chatHub.routing.showRoute` | `routePayload`: routeID/messageID. | Viser avslag, grunn, foreldreledd og bekreftet Butler-overtakelse; ikke bare en språkmodell-lane. | M:294; F:3555–3571 viser dagens annenartede route-action |
| Gjenåpne dokket chat | `KEYPATH-MANGLER:chatHub.ui.restoreChatPanel` | `restorePayload` fra panelraden. | Returnerer fra rail til utvidet chat med samme skop, utkast og loggposisjon. | M:259–263/:144–150 |

## Kandidatens avvik fra personens klikkflate

Startkortet gjenbruker fabrikkens **Prøv-knapp**, mens mockupen gjør hele raden klikkbar (F:1722–1729; M:197–199). `List.activationActionKeypath` er en mulig del av en senere løsning, men web legger til en egen «Open»-knapp og tolker payload som rad/utvalg; det er ikke samme klikkgeometri eller automatisk samme actionPayload (`CellScaffold/Public/js/skeleton-runtime.js:5867–5877`). Ingen ny starter-action er nødvendig.

Send-knappen er beholdt som en funksjonell vei inn og avviker fra mockupens rene tekstboks. `submitOnEnter` alene er ikke garanti for sending: web bruker `submitActionKeypath || targetKeypath` og her krever feltkoblingen Meta/Ctrl+Enter (`CellScaffold/Public/js/skeleton-runtime.js:899–924`). Tastaturforløp, IME, linjeskift og appens tastatur må testes; kandidaten lover ikke Enter-paritet.

Programkortets Utvid/Skjul og endringskortets Detaljer/Bekreft/Endre/Avvis skilles av 0/1-listene `toolRows`, `detailRows` og `actionRows`. Felles kandidatmal viser et grep på alle kort; mockupen viser grep og draggable bare på programkortet (M:278–283/:312–318). Før godkjenning må samme kildekontrakt angi hvilke kort som kan dras og hvordan et kort uten drag vises. Den foreløpige kandidatmalen er ikke et slikt ferdig policyvalg.

Header, teller, skopchips, tidsstempel, kildechip og grenstart er informasjon i denne delen. Mockupen angir ikke egne klikkhandlinger på dem (M:254–262/:290/:295/:298). De må ikke få oppdiktede action-keypaths. «Alt widgetene kan gjøre, kan du be om her» er foreløpig en **akseptansepåstand**: kortenes og flate-trådens actionsett må sammenholdes med samtaleruting før den kan regnes som oppfylt (FORMAALSSPEC:98–100).

## Reachability: hva som skal kontrolleres

`SkeletonReachabilityAudit.reachableActionKeypaths` finnes ved `CellProtocol/Sources/CellBase/Skeleton/SkeletonReachabilityAudit.swift:79`. Den statiske samleren tar Button.keypath og TextArea.targetKeypath, men **ikke TextArea.submitActionKeypath eller drag/drop-actions** (:315–337). Derfor sikrer Send-knappen at `chatHub.prompt.submit` kan komme med i det statiske settet. En drakilde uten Button har ingen egen action å samle; den må prøves som gest sammen med mottakeren.

Kandidaten har bare item-betingelser inne i List-rader. Det unngår root-feilen beskrevet i samme audit :142–169, men audit gir automatisk radkontekststatus til alle List-maler (:243–245). Den beviser ikke at 0/1-raden finnes, at native binder den, eller at en handling lykkes. Sammenlign derfor:

1. Dekodet/auditert actionsett mot alle deklarerte kandidatknapper, med konkrete payload-ID-er.
2. Synlige knapper per tilstand: tom, fylt, feil, dokket; logg- og kortlister må faktisk inneholde rader.
3. Handling gjennom ekte web- og Binding-renderer mot samme isolerte data: særlig en startknapp som sender sitt eget eksempel, én proposal.confirm som treffer korrekt revisjon, to ulike fallback-ruter og avbrutt drag.
4. Modellens komplette handlinger mot chatens mulighet til å be om dem. Ingen formålsmessig nåbarhet er bevist bare av et sett strenger.

`skjelett/chat.validation.json` inneholder en **enkel statisk uttrekking**, ikke en kjøring av Swift-auditen. Swift-audit, dynamiske klikk og dra/slipp er ikke kjørt: ingen bygg eller nettverk var tillatt.

Henvisninger til FORMAALSSPEC og KAPASITET_SKJELETT gjelder henholdsvis `CellProtocolDocuments/Deliverables/PDD_butler-traadtre-og-widgetflate_2026-09-11/FORMAALSSPEC.md` og `CellProtocolDocuments/Deliverables/PDD_butler-traadtre-og-widgetflate_2026-09-11/handoff/KAPASITET_SKJELETT.md` med angitte linjenumre.
