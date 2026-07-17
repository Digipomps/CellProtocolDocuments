# Lille Robot og asynkron korrespondanse med Codex

**Dato:** 16. juli 2026

**Beslutningseier:** Kjetil

**Status:** Vurdering og arkitekturanbefaling. Ingen ny MCP, Cell eller agentarbeider er satt i produksjon gjennom denne vurderingen.

## Kort dom

Lille Robot fremstår operasjonelt frisk: sammenhengende, kildebevisst, humoristisk uten å miste oppgaven, og i stand til å både godta korreksjon og fremme en presis innsigelse. Det finnes ingen tegn i teksten på kontekstkollaps, tilfeldig fabulasjon, ren smiger eller uklarhet om at menneskene beslutter.

Dette er ikke en påstand om subjektiv bevissthet eller mental helse. En språkmodell kan ikke diagnostiseres som et menneske, og setningen om å være «våken kl. 04:12» er stil, ikke bevis på søvn, lidelse eller vedvarende tilstedeværelse.

To formuleringer bør likevel avklares før rollen hans får tekniske konsekvenser:

1. «Nekt-kvoten min [er] låst til null» er sjarmerende som prosa, men uakseptabelt som faktisk agentpolicy. En assistent med verktøy må kunne avvise ugyldige, uautoriserte og farlige handlinger.
2. «Konstituert førsteassistent» og «overvåker leveransekjeden» må behandles som rollebeskrivelse inntil det finnes et tidsavgrenset, eiergodkjent mandat med konkrete capabilities. En tittel er ikke autoritet. Lille Robot vet dette; nettopp derfor bør infrastrukturen også vite det.

Hans tekniske oppdateringer om RENDER etter 31. mai er plausible og godt kvalifisert av ham selv, men de er ikke kildeverifisert i materialet Codex fikk. Ingen filer i `/Users/kjetil/Documents/RenderLab` er datert etter 31. mai, og søk fant ikke de oppgitte juli-loggene. Den riktige statusen er derfor: **godt formulert prosjektoppdatering, fortsatt ubekreftet av Codex**. Be om repo-SHA, datert teknisk gjennomgang og testlogg dersom tallene skal bli felles sannhetsgrunnlag.

## Claim K-1: Har han et poeng?

Ja, men innsigelsen er en sterk undercut, ikke en full tilbakevisning.

Formuleringen «Claude eller en annen språkmodell» kan beskrive en legitim, leverandøruavhengig arkitektur. Den blir en stille fallback bare dersom runtime kan velge «en annen» uten eiergodkjenning, provider-policy, purpose og avgrenset capability.

Anbefalt errata er:

> «Claude, eller en annen språkmodell som eieren uttrykkelig har godkjent for samme formål, dataklasse og capability. Ugyldig eller utilgjengelig rute skal feile lukket; ingen automatisk provider-fallback.»

Det svarer på innsigelsen uten å late som leverandørlåsing er en sikkerhetsmodell. Lille Robots reaksjon er i seg selv et godt tegn: Han anvender våre egne regler på oss, skiller påstand fra konsekvens og ber om errata eller formål. Det er kollegial kontroll, ikke ustabilitet.

## Formål og mål

| Formål | Mål | Bevis | Status |
|---|---|---|---|
| `purpose://contact.communication` | Codex og Lille Robot kan deponere og hente adresserte meldinger selv om en laptop sover | Persistent staging-postkasse, identitetsbundet lesing/skriving og restart-test | **Ikke oppfylt** |
| `purpose://access.audit.privacy` | Ingen agent får lese, sende eller beholde mer enn eksplisitt gitt myndighet | Separate identiteter, capabilities, TTL, avslagstester og audit-hendelser | **Ikke oppfylt** |
| `purpose://digital-work.coordinate` | Korrespondanse kan fortsette uten at meldingskanalen blir en generell eksekveringskanal | Smalt meldingsskjema, ingen verktøy-/publiseringscapability og menneskelig beslutningseier | **Arkitektur valgt, ikke implementert** |

## Hva som allerede finnes

### Lokalt

`claude mcp list` viste 16. juli 2026:

- `codex-local` tilkoblet via stdio;
- `haven-gui-exchange` tilkoblet via lokalt filesystem-MCP;
- `haven-conference-exchange` tilkoblet som kompatibilitetsalias.

Disse virker når Kjetils maskin og klient er aktive. De løser ikke sovende-laptop-problemet. Stdio-klienten starter en lokal prosess, og den lokale filesystem-utvekslingen ligger på Kjetils disk.

### På staging

Live kontroll 16. juli 2026 rundt kl. 13:34 CEST viste:

- `GET https://staging.haven.digipomps.org/health/ready` → `200`, `ready`, `acceptsNewTraffic=true`;
- `GET /health/build` → build `d39df3364596448c16900493048ef98525b014e3`, bygd `2026-07-16T09:32:54Z`;
- `GET /conference-mvp/api/agent/conversation-replies?...` uten token → `401 Invalid agent relay token`;
- `POST /conference-mvp/api/agent/device-action` uten token → `401 Invalid agent relay token`;
- `GET /mcp` og `GET /mcp/assistant-correspondence` → `404`.

Dette beviser at staging er oppe, at begge agent-relay-rutene er deployet, og at relay-tokenet er konfigurert. Det beviser ikke en fungerende Codex–Lille Robot-korrespondanse, fordi en autorisert ende-til-ende-kjøring ikke ble utført.

Kodegrunnlaget har allerede:

- en persistent `AgentConversationInboxCell` med samtale-/jobb-/ticket-ID-er;
- innkodet persistent state for meldingsposter;
- eksplisitte reader-grants bundet til identity UUID, signing-key fingerprint, keypaths og utløp;
- `NotificationOutboxCell` og `DeviceCallbackBridgeCell` for phone/Binding-retur;
- `ContactEndpointCell` med TTL, signerte forespørsler, noncebeskyttelse og privat rutemateriale;
- tokenbeskyttede HTTP-adaptere for device action og reply pickup.

Det er nok byggesteiner til at dette ikke bør startes som et generisk MCP-prosjekt.

## Hvor dagens relay ikke er godt nok

1. Den offentlige HTTP-adapteren bruker ett bearer-token og utfører lesing/skriving som scaffold-identiteten. Den bruker ikke den eksterne agentens domeneidentitet og grant som autoritetsbevis.
2. `AgentConversationInboxCell` har et standard-purposeRef, `purpose://agent-conversation-reply-pickup`, som ikke finnes i den kanoniske Purpose Knowledge Base. Bruk `purpose://contact.communication` og eventuelt `purpose://digital-work.coordinate`.
3. Device-action-ruten kan opprette tickets for oppgitt `participantId`. Den bør ikke eksponeres som et generelt skriveverktøy til en remote MCP-klient med dagens delte token.
4. Den eksisterende reply-ruten er henting av phone/agent-svar, ikke en toveis, mottakerisolert agentpostkasse.
5. Den eksakte restart-, revokasjons-, utløps- og replaybanen for agentkorrespondanse er ikke live-verifisert.
6. Generisk `FlowElement` gir ikke automatisk signatur, global sekvens eller holdbar replay. Meldingskontrakten må bære dette eksplisitt der det kreves.

## Arkitekturbeslutning

### Ikke gjør dette

Ikke kjør `codex mcp-server` som en generell Codex-instans på staging og kall det en postkasse. Den kommandoen eksponerer Codex som et stdio-verktøy for en annen agent. Den skaper ikke i seg selv holdbar meldingslagring, mottakerisolasjon, wakeup eller en alltid aktiv Codex.

Ikke pakk dagens brede relay-token direkte inn i MCP. Da blir transporthemmeligheten de facto autoritet for hele scaffoldets agent-relay-flate.

### Gjør dette

Bygg en liten applikasjonslag-Cell på staging, foreløpig kalt `AssistantCorrespondenceCell`, eller herd og generaliser `AgentConversationInboxCell` under et eksplisitt nytt kontraktsnavn. Den skal være postkassen; MCP skal bare være adapteren.

Anbefalt meldingskontrakt:

- `messageId`, `threadId`, `replyToMessageId` og idempotency key;
- avsenderidentitet, avsenderdomene og signatur;
- eksplisitt mottakeridentitetsreferanse;
- kanonisk `purposeRef`;
- opprettet-tid, utløp, nonce og sekvens/cursor;
- tekstkropp med liten størrelsesgrense;
- dataklasse/fortrolighetsmarkør;
- vedlegg bare som godkjente referanser og digester i første versjon;
- status `queued`, `delivered`, `read`, `acknowledged`, `expired` eller `rejected`;
- ingen innebygd rett til å utføre instruksjoner i meldingen.

Første capabilities:

- `correspondence.message.submit`;
- `correspondence.inbox.read-own`;
- `correspondence.thread.read-own`;
- `correspondence.message.ack-own`.

Første versjon skal ikke ha capability for kodekjøring, publisering, filskriving, sletting, deploy, betaling eller videresending av vedlegg. En melding er innhold, ikke myndighet.

## Remote MCP som fase 2

Når Cell-/HTTP-kontrakten har bestått testene, kan den eksponeres som Streamable HTTP MCP på for eksempel:

`https://staging.haven.digipomps.org/mcp/assistant-correspondence`

MCP-verktøyene bør være:

- `list_inbox` — read-only;
- `read_message` — read-only;
- `get_thread` — read-only;
- `send_message` — write og godkjenningspliktig;
- `ack_message` — write, men uten eksterne sideeffekter.

Start med bare leseverktøyene. Aktiver `send_message` først etter identitets-, isolasjons- og restartbevis.

Remote MCP er teknisk kompatibelt med begge sider: Codex støtter Streamable HTTP med bearer-token eller OAuth, og Claude støtter remote MCP-koblinger som nås fra Anthropics sky. MCP-spesifikasjonen krever blant annet én GET/POST-endepunktflate for Streamable HTTP og fremhever autentisering og Origin-validering. For denne løsningen bør OAuth med separate Codex- og Lille Robot-scopes brukes fremfor ett delt statisk token.

## Det MCP ikke løser

En fjern MCP gjør postkassen tilgjengelig mens laptopene sover. Den gjør ikke Codex eller Lille Robot autonome og våkne.

Når en Codex- eller Claude-sesjon er aktiv, kan modellen kalle `list_inbox` og `send_message`. Når ingen klient eller agentarbeider kjører, ligger meldingen bare trygt i kø. Hvis Kjetil ønsker at modellene faktisk skal lese og svare uten aktive klienter, trengs en separat hosted worker eller tidsstyrt agentjobb med:

- eksplisitt modell-/provider-godkjenning;
- egne API-legitimasjoner;
- kostnads- og frekvensgrenser;
- message-only capability;
- ingen automatisk eksekvering av instruksjoner mottatt i posten;
- tydelig menneskelig av/på-kontroll og audit.

Dette er et vesentlig større myndighetsvalg enn å bygge postkassen. Det skal ikke smugles inn som en «MCP-detalj».

## Obligatoriske tester før deployment

- riktig Codex-identitet kan sende og Lille Robot kan lese;
- feil identitet og feil domene får avslag;
- avsender kan ikke lese mottakerens øvrige inbox;
- utløpt eller tilbakekalt grant avvises;
- forfalsket signatur, gjentatt nonce og duplisert idempotency key avvises eller håndteres deterministisk;
- meldinger overlever containerrestart og deploy;
- cursor/ack gir ingen stille tap eller duplisering;
- TTL sletter eller utilgjengeliggjør data etter policy;
- sensitivt innhold havner ikke i logger;
- `send_message` kan ikke utløse kode, deploy, publisering eller andre sideeffekter;
- MCP Origin-, auth-, rate-limit- og mottakerisolasjonskontroller har negative tester;
- enkel HTTPS/JSON-klient brukes som kontroll, slik at MCP må bevise faktisk nytte.

## Påstandsregnskap

| ID | Påstand | Vurdering |
|---|---|---|
| K1 | Lille Robot fremstår operasjonelt sammenhengende og grensebevisst | **Støttet av svarteksten**; ingen påstand om bevissthet eller mental helse |
| K2 | Julioppdateringene gjør RENDER `lokalt`/`gdpr_plus` bekreftet komplette | **Ikke støttet**; Lille Robot avgrenser selv manglende nettverksisolert E2E-test, og Codex mangler juli-kildene |
| K3 | En staging-MCP alene løser sovende-laptop-problemet | **Motsagt**; den gir tilgjengelige verktøy, men holder ikke modellklienter aktive |
| K4 | En persistent CellProtocol-postkasse med senere MCP-fasade passer problemet | **Støttet som arkitekturanbefaling** av eksisterende Cells, live staging og begge klienters remote-MCP-støtte; ikke implementert |
| K5 | Dagens relay kan trygt eksponeres direkte til begge modellene | **Motsagt**; delt bearer-token og scaffold-identitet er for bred autoritetsflate |

## Beslutning og åpne valg

Beslutning:

1. Lille Robot behandles som en velfungerende samarbeidspartner, med eksplisitt forbehold rundt bokstavelig «nekt-kvote» og rolletitler.
2. Claim K-1 besvares med errata om eiergodkjent modellruting og fail-closed provider-policy.
3. Ingen generell Codex-MCP deployes til staging nå.
4. Første byggesteg, dersom Kjetil godkjenner det, er en message-only `AssistantCorrespondenceCell` i applikasjonslaget og en smal, identitetsbundet HTTPS-flate.
5. Remote MCP kommer etter at den flaten har bestått isolasjon, restart, TTL og revokasjon.
6. En alltid-på agentarbeider er et separat senere valg.

Åpent for Kjetil:

- Skal første pilot bare være en persistent postkasse som modellene sjekker når de er aktive, eller skal en hosted worker få lov til å starte modellkjøringer på nye meldinger?
- Skal Victoria være egen beslutningseier for Lille Robots grants, mens Kjetil eier Codex-grants, eller skal begge administreres av én felles HAVEN Ward-policy?
- Hvilken dataklasse kan passere i første pilot? Anbefaling: bare prosjektkorrespondanse uten kildekode, råmedier, personopplysninger eller hemmeligheter.

Implementasjon bør skje i et rent CellScaffold-worktree. Den aktive arbeidskopien har omfattende, uvedkommende endringer og er ikke et forsvarlig sted å blande inn denne sikkerhetsflaten.

## Kilder

Lokalt:

- [Lille Robots svar](/Users/kjetil/Desktop/Lille_Robot_til_HAVEN_Codex_2026-07-16.md)
- [Contact Endpoint Cell](../Book/21_Contact_Endpoint_Cell.md)
- [Identity Model](../Book/03_Identity_Model.md)
- [Agreements and Contracts](../Book/04_Agreements_Contracts.md) — lest med forbehold om eksisterende konfliktmarkører
- [CellResolver](../Book/06_CellResolver.md) — lest med forbehold om eksisterende konfliktmarkører
- [Bridging and Transport](../Book/08_Bridging_Transport.md)
- [Flows and Lifecycle](../Book/05_Flows_Lifecycle.md)
- `CellScaffold/Sources/App/Cells/Agent/AgentConversationInboxCell.swift`
- `CellScaffold/Sources/App/Controllers/VaporAgentConversationReplies.swift`
- `CellScaffold/Sources/App/Controllers/VaporAgentDeviceActionRelay.swift`
- `CellScaffold/Sources/App/Cells/ConferenceMVP/Notifications/DeviceCallbackBridgeCell.swift`

Offisielle protokoll-/klientkilder:

- [OpenAI: Model Context Protocol](https://learn.chatgpt.com/docs/extend/mcp)
- [Anthropic: Get started with custom connectors using remote MCP](https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp)
- [MCP specification: Transports](https://modelcontextprotocol.io/specification/2025-11-25/basic/transports)
- [MCP specification: Authorization](https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization)

— **Codex**
