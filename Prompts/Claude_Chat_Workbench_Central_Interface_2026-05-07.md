# Claude Round - Chat Workbench Central Interface

Date: 2026-05-07

## Prompt

Du designer HAVEN/CellProtocol sin sentrale chat-komponent. Svar paa norsk,
praktisk og kritisk.

Ground truth fra repoene:

- Chat skal vaere primaer GUI-komponent i HAVEN/Binding/Porthole, men maa ogsaa
  kunne embeddes kompakt.
- Hovedmekanismen er natural language -> Purpose/Interest -> match mot
  tilgjengelige CellConfigurations, RAG-cases, agent-actions og cell-scoped AI
  providers.
- Brukerens lokale Purpose/Interest-kontekst ligger i PerspectiveCell.
  Implementerte keypaths: GET `advertisedPurpose`, `activePurpose`,
  `perspective.state`. SET `addPurpose`, `matchPurpose`,
  `perspective.query.activePurposes`,
  `perspective.query.interestsFromActivePurposes`, `perspective.query.match`.
  Payloads har `portablePurposeRef`/`portableInterestRef`, weights og
  `supportingPurposes`.
- `PersonalChatHubCell` finnes og har chat-first Invite Chat med Tabs:
  `Samtale`, `Aktivt`, `Mer`. Actions: set/send/clear composer,
  `analyzeDraft`, `openSuggestedHelper` side-effektfritt, accept/dismiss
  suggestion, invite/accept/decline, poll create/vote/close,
  todo/project/reminder/meeting metadata, report/block/unblock,
  `queryResource`, `provider.register/recommend`, `agent.review.create/execute`.
- `ChatPurposeResourceRouter` matcher draft mot CellConfigurations, RAG-cases og
  `AgentActionCapabilityDescriptor`. Metadata eksponeres, ikke data. RAG query
  krever eksplisitt klikk.
- `ChatScopedAIProviderRouter` velger kun providers i chat/cell-scope:
  `localRules`, `appleIntelligence`, `subscription`, `apiGateway`,
  `ragGateway`, `agentBridge`, `custom`. Ingen global AI-provider. Prioritet
  boer vaere tryggest/billigst: local deterministic -> Apple
  Intelligence/on-device -> RAG/owner scoped -> subscription/API naar
  noedvendig.
- Apple Intelligence finnes som CellProtocol `AppleIntelligenceCell` bak
  `canImport(FoundationModels)`, med `ai.sendPrompt`/`ensurePurpose`/`discover`/
  `rank`; Apple Foundation Models er on-device, supports structured generation
  and tool calling, but requires Apple Intelligence enabled.
- AgentD bridge: chat kan bare lage signert/reviewbar intent til
  RemoteIntentInbox/Review; ingen raw shell/AppleScript, ingen lokale filer
  eller Entity values i autocomplete.
- Konferansefunksjoner finnes: `ConferenceUIRouterCell` med
  `screenMap`/`state`/`navigate`/`dispatchAction`, `ConferenceOnboarding`,
  `Scheduling`, `ConnectionHub`, `Recommendation`, `EntityDiscovery`,
  `ChatLaunch`, `ProofChatLaunch`, `SessionThread`, `SessionPolling`,
  `BroadcastStudio`, `Sponsor`, `PublishedContent`, Admin/Participant/Public
  shells. `ConferenceUIRouter` kan `dispatchAction` til onboarding,
  recommendation og scheduling keypaths. `ConferenceEntityDiscovery` kan starte
  chat via `ConferenceChatLaunch`. Notifications/broadcast kan vekke enheter.
- Skeleton-primitives tilgjengelig naa: `Text`, `TextField`, `TextArea`,
  `Image`, `Spacer`, `HStack`, `VStack`, `ZStack`, `List`, `Object`,
  `Reference`, `Button`, `Grid`, `ScrollView`, `Section`, `Divider`, `Picker`,
  `Toggle`, `Tabs`, `FileUpload`. Ikke anta `Sheet`, `DateTimePicker`,
  `ComponentSlot` eller sticky composer.

Oppgave:

1. Foreslaa IA/UX for en universell Chat Workbench som kan brukes full-screen,
   embedded og conference context.
2. Beskriv hvordan Purpose/Interest + PerspectiveCell skal paavirke matching og
   provider/tool-valg uten datalekkasjer.
3. Beskriv hvordan Apple Intelligence-integrasjonen boer gjoeres nyttig nok til
   aa unngaa stoerre modell som default.
4. Beskriv hvordan chatten skal hente frem alle konferansefunksjoner som trygge
   verktøy/helper cards, med konkrete examples: agenda, people matching, start
   chat, meeting request, session thread/poll, broadcast, public content edit,
   sponsor lead, device wake.
5. Skill mellom V1 med dagens skeleton og V2 som krever nye primitives.
6. Gi en kort, implementerbar dokumentasjonsstruktur for CellProtocolDocuments
   og DiMyDocuments.

Ikke foreslaa global AI-provider. Ikke foreslaa fake buttons eller raa debug i
default UI. All sideeffekt krever eksplisitt klikk og riktig CellProtocol-grant.

## Claude Response Summary

Claude recommended:

- one component model with full-screen, embedded and conference modes
- a context bar as the visible truth source for cell scope and active purpose
- composer-first interaction, with helper cards appearing after explicit draft
  analysis
- metadata-only Purpose/Interest matching through `ChatPurposeResourceRouter`
  and `PerspectiveCell`
- provider ranking that starts with local rules, then on-device Apple
  Intelligence, then scoped RAG/provider/API only after explicit user action
- conference capabilities exposed as role-gated helper cards through
  `ConferenceUIRouterCell` and related conference cells
- V1 using current skeleton primitives, with V2 priority on Sheet,
  sticky composer/section, DateTimePicker and ComponentSlot
- CellProtocolDocuments for protocol contracts and DiMyDocuments for product,
  commercial, privacy and roadmap documentation

See `Book/19_Chat_Workbench_Central_Interface.md` for the normalized design
record that incorporates this response with repo ground truth.

