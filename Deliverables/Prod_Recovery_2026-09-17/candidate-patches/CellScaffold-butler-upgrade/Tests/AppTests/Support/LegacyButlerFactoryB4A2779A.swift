// SPDX-License-Identifier: Apache-2.0
// SPDX-FileCopyrightText: Copyright (c) 2026 Stiftelsen Digipomps and HAVEN contributors

@testable import App
import Foundation
@preconcurrency import CellBase

enum LegacyButlerFactoryB4A2779A {
    struct Descriptor {
        var configuration: CellConfiguration
        var metadata: PersonalCopilotConfigurationMetadata
        var sourceCellEndpoint: String
        var sourceCellName: String
        var purpose: String
        var purposeDescription: String
        var interests: [String]
        var menuSlots: [String]
        var surfaceFamily: String
        var presentationClass: String
        var executionScope: String
        var visibleActions: [String]
    }

    static func descriptors() -> [Descriptor] {
        cloudDescriptors() + localAndDeviceDescriptors()
    }

    static func catalogConfigurations() -> [CellConfiguration] {
        descriptors().map(\.configuration)
    }

    static func configuration(for endpoint: String) -> CellConfiguration? {
        descriptors().first { $0.sourceCellEndpoint == endpoint }?.configuration
    }

    static func catalogEntryObjects() -> [Object] {
        descriptors().map { descriptor in
            [
                "id": .string(entryID(for: descriptor.configuration)),
                "sourceCellEndpoint": .string(descriptor.sourceCellEndpoint),
                "sourceCellName": .string(descriptor.sourceCellName),
                "purpose": .string(descriptor.purpose),
                "purposeDescription": .string(descriptor.purposeDescription),
                "interests": .list(descriptor.interests.map(ValueType.string)),
                "menuSlots": .list(descriptor.menuSlots.map(ValueType.string)),
                "surfaceFamily": .string(descriptor.surfaceFamily),
                "presentationClass": .string(descriptor.presentationClass),
                "executionScope": .string(descriptor.executionScope),
                "visibleActions": .list(descriptor.visibleActions.map(ValueType.string)),
                "metadata": .object(metadataObject(for: descriptor)),
                "configuration": .cellConfiguration(descriptor.configuration)
            ]
        }
    }

    static func purposeGoal(for endpoint: String) -> ValueType {
        guard let descriptor = descriptors().first(where: { $0.sourceCellEndpoint == endpoint }) else {
            return .null
        }
        return .object([
            "id": .string(entryID(for: descriptor.configuration)),
            "sourceCellEndpoint": .string(descriptor.sourceCellEndpoint),
            "sourceCellName": .string(descriptor.sourceCellName),
            "purpose": .string(descriptor.purpose),
            "purposeDescription": .string(descriptor.purposeDescription),
            "interests": .list(descriptor.interests.map(ValueType.string)),
            "menuSlots": .list(descriptor.menuSlots.map(ValueType.string)),
            "surfaceFamily": .string(descriptor.surfaceFamily),
            "presentationClass": .string(descriptor.presentationClass),
            "executionScope": .string(descriptor.executionScope),
            "visibleActions": .list(descriptor.visibleActions.map(ValueType.string)),
            "metadata": .object(metadataObject(for: descriptor)),
            "goal": .cellConfiguration(descriptor.configuration),
            "configuration": .cellConfiguration(descriptor.configuration)
        ])
    }

    static func hasPersonalCopilotScope(_ configuration: CellConfiguration) -> Bool {
        configuration.discovery?.interests.contains(PersonalCopilotAppStoreV1Contract.appStoreScopeInterest) == true
    }

    private static func cloudDescriptors() -> [Descriptor] {
        [
            makeDescriptor(
                name: "Personal Page Publisher",
                endpoint: PersonalPagePublisherContract.endpoint,
                label: "pagePublisher",
                sourceCellName: "PersonalPagePublisherCell",
                purpose: "Create and manage public personal pages",
                purposeDescription: "Lag, forhåndsvis og publiser en offentlig side fra eksplisitt valgt tekst og private medieopplastinger. Medieinkludering, lagringskvote, directory-listing, hosting-policy og publisering er separate valg.",
                interests: [
                    "personal",
                    "profile",
                    "public-profile",
                    "public-presence",
                    "profile-page",
                    "personal-page",
                    "template-library",
                    "media-upload",
                    "storage-quota",
                    "hosting-policy",
                    "directory-opt-in",
                    "publish",
                    "identity",
                    "consent",
                    "purpose=template-preview-hosting-publish-unpublish-delete",
                    "purposeRef=personal.public-presence.publish",
                    "purposeRef=personal.profile.page.create",
                    "purposeRef=personal.profile.page.edit",
                    "purposeRef=personal.public-presence.template.choose",
                    "purposeRef=personal.public-presence.hosting.configure"
                ],
                menuSlots: ["upperMid"],
                metadata: PersonalCopilotConfigurationMetadata(
                    policyCategory: "public-presence-page",
                    requiresUserGeneratedContentModeration: true,
                    universalLink: stagingLink("personal/page/publish"),
                    reviewSummary: "Explicit page publishing adapter with template selection, hosting readiness and public-read-model guardrails."
                ),
                surfaceFamily: "identity",
                presentationClass: "form",
                executionScope: "cloud",
                visibleActions: [
                    "draft.pageTitle",
                    "draft.pageSummary",
                    "draft.templateID",
                    "draft.sourceProfileEndpoint",
                    "draft.sourceRefs",
                    "draft.hostingProvider",
                    "draft.costModel",
                    "draft.estimatedMonthlyCost",
                    "draft.deletionGuarantee",
                    "draft.directoryListed",
                    "uploadMedia",
                    "selectMedia",
                    "includeSelectedMedia",
                    "excludeSelectedMedia",
                    "deleteSelectedMedia",
                    "selectTemplate",
                    "selectPage",
                    "setActiveTab",
                    "refreshPreview",
                    "publishPage",
                    "unpublishPage",
                    "deletePage"
                ],
                skeleton: pagePublisherSkeleton()
            ),
            makeDescriptor(
                name: "Publish Public Profile",
                endpoint: PersonalProfilePublisherContract.endpoint,
                label: "profilePublisher",
                sourceCellName: "PersonalProfilePublisherCell",
                purpose: "Publish public profile",
                purposeDescription: "Publiser, avpubliser eller slett en offentlig profil bare når brukeren har skrevet eller valgt data for publisering og bekreftet samtykke.",
                interests: [
                    "personal",
                    "profile",
                    "public-profile",
                    "public-presence",
                    "profile-page",
                    "publish",
                    "identity",
                    "consent",
                    "purpose=publish-unpublish-delete",
                    "purposeRef=personal.public-presence.publish"
                ],
                menuSlots: ["upperMid"],
                metadata: PersonalCopilotConfigurationMetadata(
                    policyCategory: "profile-publish",
                    requiresUserGeneratedContentModeration: true,
                    universalLink: stagingLink("personal/profile/publish"),
                    reviewSummary: "Explicit user-controlled public profile publishing with unpublish and delete."
                ),
                surfaceFamily: "identity",
                presentationClass: "form",
                executionScope: "cloud",
                visibleActions: ["editPublicPayload", "publishProfile", "unpublishProfile", "deleteProfile", "profileStatus"],
                skeleton: profilePublisherSkeleton()
            ),
            makeDescriptor(
                name: "Public Profile Directory",
                endpoint: PublicProfileDirectoryContract.endpoint,
                label: "directory",
                sourceCellName: "PublicProfileDirectoryCell",
                purpose: "Search public profiles safely",
                purposeDescription: "Søk i publiserte profiler og la brukeren rapportere, skjule eller blokkere profiler fra samme flate.",
                interests: [
                    "personal",
                    "directory",
                    "search",
                    "profile",
                    "public-profile",
                    "public-presence",
                    "moderation",
                    "block",
                    "purpose=search-report-hide-block",
                    "purposeRef=personal.public-directory.search"
                ],
                menuSlots: ["upperLeft"],
                metadata: PersonalCopilotConfigurationMetadata(
                    policyCategory: "public-directory",
                    requiresUserGeneratedContentModeration: true,
                    universalLink: stagingLink("personal/directory"),
                    reviewSummary: "Searchable public profile read model with report, hide and block."
                ),
                surfaceFamily: "relationship",
                presentationClass: "list",
                executionScope: "cloud",
                visibleActions: ["searchProfiles", "profileDetail", "reportProfile", "hideProfile", "blockProfile"],
                skeleton: directorySkeleton()
            ),
            makeDescriptor(
                name: "Matches",
                endpoint: PersonalMatchmakingContract.endpoint,
                label: "matchmaking",
                sourceCellName: "PersonalMatchmakingCell",
                purpose: "Consent-based matching",
                purposeDescription: "Gi match-forslag basert på publiserte profiler og eksplisitte preferanser. Chat starter aldri automatisk.",
                interests: ["personal", "matchmaking", "recommendations", "consent", "social", "purpose=mutual-consent-no-auto-chat"],
                menuSlots: ["upperLeft", "lowerMid"],
                metadata: PersonalCopilotConfigurationMetadata(
                    policyCategory: "matching",
                    requiresUserGeneratedContentModeration: true,
                    universalLink: stagingLink("personal/matches"),
                    reviewSummary: "Consent-based matching; chat remains gated by explicit mutual approval."
                ),
                surfaceFamily: "relationship",
                presentationClass: "list",
                executionScope: "cloud",
                visibleActions: ["editPreferences", "refreshSuggestions", "requestMatchConsent", "acceptMatchConsent", "declineMatchConsent", "clearMatchSuggestion"],
                skeleton: matchmakingSkeleton()
            ),
            makeDescriptor(
                name: "Co-Pilot Chat",
                endpoint: PersonalChatHubContract.endpoint,
                label: "chatHub",
                sourceCellName: "PersonalChatHubCell",
                purpose: "Central purpose-driven co-pilot chat",
                purposeDescription: "Kompakt chat-first arbeidsflate som matcher brukerens naturlige språk mot synlige formål, interesser, CellConfigurations, tilgjengelige RAG-cases, trygge agent-action metadata og owner-scoped entity extension. Invitasjon, avstemning, work item/feilrapport, oppgave, prosjekt/idé, påminnelse, møtemetadata, eksplisitt RAG-query, tilgangsskann og signert agent-review er handlende workbench-moduler, men alle sideeffekter krever klikk og scope-godkjenning.",
                interests: [
                    "personal",
                    "chat",
                    "invite-only",
                    "moderation",
                    "block",
                    "ugc",
                    "chat-assistant",
                    "invite-person",
                    "external-collaboration-request",
                    "purpose-bound-share-link",
                    "guest-contribution-without-account",
                    "owner-controlled-reshare",
                    "poll",
                    "meeting-video-intent",
                    "schedule-meeting-intent",
                    "project-intent",
                    "todo-intent",
                    "reminder-intent",
                    "resource-router",
                    "rag-query",
                    "cell-scoped-ai-provider",
                    "provider-slot",
                    "best-fit-model-selection",
                    "provider-maintenance",
                    "local-agent-action",
                    "entity-extension",
                    "capability-map",
                    "owned-device",
                    "owned-service",
                    "signed-remote-intent",
                    "idea-capture",
                    "work-item",
                    "bug-report",
                    "work-item-capture",
                    "guided-onboarding",
                    "entity-enrichment",
                    "vault",
                    "component-motion",
                    "component-surface",
                    "spatial-map",
                    "spatial-discovery",
                    "location",
                    "nearby",
                    "requires-user-approval",
                    "purpose-interest-weighted",
                    "purpose=invite-accept-compose-report-block-assist-poll-rag-agent-action-provider-route",
                    "purposeRef=personal.chat.assist.invite",
                    "purposeRef=purpose://contact.introduction",
                    "purposeRef=purpose://digital-work.coordinate",
                    "purposeRef=purpose://project-work.share-selected-intent",
                    "purposeRef=purpose://access.audit.privacy",
                    "purposeRef=personal.chat.assist.poll",
                    "purposeRef=personal.chat.assist.resource-router",
                    "purposeRef=personal.chat.assist.rag-query",
                    "purposeRef=personal.chat.assist.provider-route",
                    "purposeRef=personal.ai.provider.select.best-fit",
                    "purposeRef=personal.ai.provider.maintain",
                    "purposeRef=personal.chat.assist.entity-extension",
                    "purposeRef=personal.chat.assist.meeting.video",
                    "purposeRef=personal.chat.assist.local-agent-action",
                    "purposeRef=personal.chat.assist.idea.capture",
                    "purposeRef=personal.chat.assist.work-item.capture",
                    "purposeRef=personal.chat.assist.guided-onboarding",
                    "purposeRef=personal.chat.assist.spatial-query",
                    "purposeRef=conference.participant.onboarding",
                    "purposeRef=personal.agent.local.gui.finder.close-windows",
                    "purposeRef=personal.agent.binding.wake",
                    "purposeRef=personal.agent.binding.absorb-cell",
                    "purposeRef=personal.agent.folder.changed-file",
                    "purposeRef=personal.agent.sprout.sync",
                    "purposeRef=personal.chat.assist.meeting.schedule",
                    "purposeRef=personal.chat.assist.project",
                    "purposeRef=personal.chat.assist.todo",
                    "purposeRef=personal.chat.assist.reminder",
                    "purposeRef=personal.chat.assist.moderation"
                ],
                menuSlots: ["upperLeft", "lowerLeft"],
                metadata: PersonalCopilotConfigurationMetadata(
                    policyCategory: "purpose-driven-chat",
                    requiresUserGeneratedContentModeration: true,
                    universalLink: stagingLink("personal/chat/copilot"),
                    reviewSummary: "Purpose-driven Butler Chat with invite-only human chat, report/block/filtering and no payment or external purchase CTA."
                ),
                surfaceFamily: "relationship",
                presentationClass: "detail",
                executionScope: "cloud",
                visibleActions: [
                    "invite",
                    "collaboration.prepareExternal",
                    "collaboration.revoke",
                    "collaboration.approveIdentityBinding",
                    "collaboration.rejectIdentityBinding",
                    "collaboration.revokeGrant",
                    "acceptInvite",
                    "declineInvite",
                    "setComposer",
                    "sendComposedMessage",
                    "clearComposer",
                    "reportMessage",
                    "blockUser",
                    "unblockUser",
                    "prompt.submit",
                    "assistant.analyzeDraft",
                    "assistant.acceptSuggestion",
                    "assistant.dismissSuggestion",
                    "assistant.queryResource",
                    "assistant.provider.register",
                    "assistant.provider.recommend",
                    "assistant.provider.invoke",
                    "assistant.setCandidateQuery",
                    "assistant.selectCandidate",
                    "entityExtension.scan",
                    "ui.openComponentSurface",
                    "ui.minimizeComponentSurface",
                    "ui.restoreComponentSurface",
                    "ui.dismissComponentSurface",
                    "ui.pinComponentSurface",
                    "absorbChat",
                    "releaseAbsorbedChat",
                    "setActiveAbsorbedChat",
                    "setCombinedChatView",
                    "poll.setQuestion",
                    "poll.setOptions",
                    "poll.create",
                    "poll.vote",
                    "poll.close",
                    "idea.title",
                    "idea.content",
                    "idea.capture",
                    "workItem.title",
                    "workItem.summary",
                    "workItem.kind",
                    "workItem.project",
                    "workItem.repo",
                    "workItem.cell",
                    "workItem.surface",
                    "workItem.severity",
                    "workItem.priority",
                    "workItem.currentBehavior",
                    "workItem.expectedBehavior",
                    "workItem.capture",
                    "todo.create",
                    "project.create",
                    "reminder.create",
                    "meeting.schedule",
                    "onboarding.start",
                    "onboarding.answer",
                    "onboarding.confirmStep",
                    "onboarding.skipStep",
                    "onboarding.editStep",
                    "onboarding.cancel",
                    "onboarding.resume",
                    "onboarding.complete",
                    "spatial.queryAround",
                    "spatial.explainFeature",
                    "spatial.draftArtifact",
                    "spatial.requestPresence",
                    "spatial.revokePresence",
                    "agent.review.create",
                    "agent.review.execute"
                ],
                additionalReferences: [
                    CellReference(endpoint: "cell:///AgreementWorkbench", subscribeFeed: false, label: "agreementWorkbench"),
                    CellReference(endpoint: SpatialProjectionContract.endpoint, subscribeFeed: false, label: "spatial"),
                    CellReference(endpoint: "cell:///Perspective", subscribeFeed: false, label: "perspective")
                ],
                skeleton: chatHubSkeleton()
            ),
            makeDescriptor(
                name: "HAVEN Teaching Group Chat",
                endpoint: "cell:///AIAssistantThread",
                label: "aiAssistantThread",
                sourceCellName: "AIAssistantThreadCell",
                purpose: "Run a HAVEN teaching group with ChatGPT, Claude and local Qwen",
                purposeDescription: "Start en CellProtocol-native gruppechat der ChatGPT 4o-mini og Claude kjører som lærere, mens den lokale Qwen-ruten deltar som liten læringsmodell. Diskusjonen vises som egne agentmeldinger i Co-Pilot-flaten.",
                interests: [
                    "personal",
                    "chat",
                    "chat-assistant",
                    "ai-assistant-thread",
                    "ai-gateway",
                    "agent-swarm",
                    "parallel-fan-out",
                    "parallel-ai-chat",
                    "parallel-local-borealis",
                    "chatgpt",
                    "openai",
                    "claude",
                    "anthropic",
                    "borealis",
                    "qwen",
                    "local-llm",
                    "local-model",
                    "cell-scoped-ai-provider",
                    "provider-route",
                    "component-surface",
                    "requires-user-approval",
                    "purpose=post-user-message-haven-teaching-swarm",
                    "purpose=post-user-message-parallel-local-borealis",
                    "purposeRef=personal.chat.assist.haven-teaching-swarm",
                    "purposeRef=personal.chat.assist.parallel-ai-chat",
                    "purposeRef=personal.chat.assist.private-local-model",
                    "purposeRef=personal.chat.assist.provider-route",
                    "purposeRef=personal.chat.assist.local-model"
                ],
                menuSlots: ["upperLeft", "lowerLeft"],
                metadata: PersonalCopilotConfigurationMetadata(
                    policyCategory: "purpose-driven-ai-group-chat",
                    requiresUserGeneratedContentModeration: true,
                    universalLink: stagingLink("personal/chat/haven-teaching-group"),
                    reviewSummary: "Co-Pilot surface for an AIAssistantThread teaching swarm using explicit provider routes and local model scope."
                ),
                surfaceFamily: "assistant",
                presentationClass: "detail",
                executionScope: "hybrid",
                visibleActions: [
                    "postUserMessage",
                    "messages",
                    "state",
                    "summary",
                    "runState",
                    "pendingRequests",
                    "refresh"
                ],
                subscribeFeed: true,
                skeleton: aiAssistantThreadSkeleton()
            ),
            makeDescriptor(
                name: "Executable Purpose Grounding",
                endpoint: ExecutablePurposeGroundingContract.endpoint,
                label: "executablePurposeGrounding",
                sourceCellName: "ExecutablePurposeGroundingCell",
                purpose: "Verify executable purpose plans",
                purposeDescription: "CellProtocol-native grounding layer that turns natural language into requester-scoped GroundedActionPlan data, verifies schemas/grants/risk and produces dry-runs before any helper or action can run.",
                interests: [
                    "personal",
                    "chat",
                    "grounded-action-plan",
                    "executable-language-grounding",
                    "xlang-like",
                    "schema-verification",
                    "dry-run",
                    "resource-router",
                    "rag-query",
                    "local-agent-review",
                    "cell-scoped-ai-provider",
                    "side-effect-free",
                    "requires-user-approval",
                    "purpose-interest-weighted",
                    "purposeRef=personal.chat.assist.executable-grounding",
                    "purposeRef=personal.chat.assist.resource-router",
                    "purposeRef=personal.chat.assist.rag-query",
                    "purposeRef=personal.chat.assist.local-agent-action"
                ],
                menuSlots: ["upperLeft", "lowerRight"],
                metadata: PersonalCopilotConfigurationMetadata(
                    policyCategory: "executable-purpose-grounding",
                    requiresUserGeneratedContentModeration: false,
                    universalLink: stagingLink("personal/chat/grounding"),
                    reviewSummary: "Verifier-owned grounding layer: providers may suggest plans, but schemas, grants and dry-runs decide what the UI may expose."
                ),
                surfaceFamily: "assistant",
                presentationClass: "inspector",
                executionScope: "cloud",
                visibleActions: [
                    "grounding.analyze",
                    "grounding.decompose",
                    "purpose.knowledge.resolve",
                    "purpose.context.pack",
                    "grounding.verify",
                    "grounding.dryRun",
                    "grounding.openHelper",
                    "grounding.dismiss"
                ],
                skeleton: executablePurposeGroundingSkeleton()
            ),
            makeDescriptor(
                name: "HAVENAgentD Capability Check",
                endpoint: HAVENAgentCapabilityBrokerContract.endpoint,
                label: "agentCapabilityBroker",
                sourceCellName: "HAVENAgentCapabilityBrokerCell",
                purpose: "Decide whether a registered local HAVENAgentD capability can help",
                purposeDescription: "Koble et deklarert formål til en kjent AgentD-handling, kontroller separat registreringsstatus, og eskaler til oppsettshjelp når agenten eller handlingen mangler. Matching gir aldri grant eller utførelsesrett.",
                interests: [
                    "personal",
                    "chat",
                    "local-agent",
                    "capability-resolution",
                    "purpose-escalation",
                    "registration-evidence",
                    "side-effect-free",
                    "requires-user-approval",
                    "purposeRef=purpose://capability.delivery",
                    "purposeRef=purpose://access.audit.privacy",
                    "purposeRef=personal.chat.assist.local-agent-action"
                ],
                menuSlots: ["lowerRight"],
                metadata: PersonalCopilotConfigurationMetadata(
                    policyCategory: "local-agent-capability-resolution",
                    requiresUserGeneratedContentModeration: false,
                    universalLink: stagingLink("personal/chat/agent-capability"),
                    reviewSummary: "Owner-scoped purpose-to-AgentD decision support with separate runtime evidence and explicit setup/review relations."
                ),
                surfaceFamily: "assistant",
                presentationClass: "inspector",
                executionScope: "local",
                visibleActions: [
                    HAVENAgentCapabilityBrokerContract.evaluateKeypath,
                    HAVENAgentCapabilityBrokerContract.reportRegistrationKeypath,
                    HAVENAgentCapabilityBrokerContract.clearRegistrationKeypath
                ],
                additionalReferences: [
                    CellReference(endpoint: HAVENAgentSetupContract.endpoint, subscribeFeed: false, label: "agentSetup")
                ],
                skeleton: havenAgentCapabilityBrokerSkeleton()
            ),
            makeDescriptor(
                name: "HAVENAgentD Setup",
                endpoint: HAVENAgentSetupContract.endpoint,
                label: "agentSetup",
                sourceCellName: "HAVENAgentSetupCell",
                purpose: "Explain, inspect and prepare a safe HAVENAgentD installation",
                purposeDescription: "Forklar hvorfor AgentD trengs for det valgte formålet, kontroller en lokal statusobservasjon uten token eller hemmeligheter, og lag en gjennomgåbar installasjonsplan med tillitspakke. Cellen kjører aldri installatøren selv.",
                interests: [
                    "personal",
                    "local-agent",
                    "onboarding",
                    "installation-guidance",
                    "trust-packet",
                    "loopback-only",
                    "explicit-confirmation",
                    "purposeRef=purpose://capability.delivery",
                    "purposeRef=purpose://access.audit.privacy",
                    "purposeRef=purpose://test.acceptance.purpose-decomposition"
                ],
                menuSlots: ["lowerRight"],
                metadata: PersonalCopilotConfigurationMetadata(
                    policyCategory: "local-agent-installation-guidance",
                    requiresUserGeneratedContentModeration: false,
                    universalLink: stagingLink("personal/chat/agent-setup"),
                    reviewSummary: "Side-effect-free AgentD setup guidance requiring artifact, hash, signing evidence, user review and local OS confirmation."
                ),
                surfaceFamily: "assistant",
                presentationClass: "form",
                executionScope: "local",
                visibleActions: [
                    HAVENAgentSetupContract.inspectKeypath,
                    HAVENAgentSetupContract.prepareInstallKeypath,
                    HAVENAgentSetupContract.clearKeypath
                ],
                skeleton: havenAgentSetupSkeleton()
            ),
            makeDescriptor(
                name: "Questionnaire Campaign",
                endpoint: QuestionnaireCampaignContract.endpoint,
                label: "questionnaireCampaign",
                sourceCellName: "QuestionnaireCampaignCell",
                purpose: "Run reusable questionnaire campaigns",
                purposeDescription: "Importer mottakere som EntityRepresentation-kompatible records, send tilgangslenker med access proof, og les samtykke-gatede spørreskjemasvar.",
                interests: [
                    "personal",
                    "questionnaire",
                    "campaign",
                    "recipient-import",
                    "entity-representation",
                    "bookproject",
                    "innovation-policy",
                    "access-proof",
                    "group-presence",
                    "purpose=import-preview-send-submit-export",
                    "purposeRef=purpose://questionnaire.response",
                    "purposeRef=purpose://bookproject.group-membership",
                    "purposeRef=purpose://bookproject.group-message"
                ],
                menuSlots: ["upperLeft", "lowerRight"],
                metadata: PersonalCopilotConfigurationMetadata(
                    policyCategory: "questionnaire-campaign",
                    requiresUserGeneratedContentModeration: true,
                    universalLink: stagingLink("personal/questionnaire/campaign"),
                    reviewSummary: "Reusable questionnaire campaign surface with access-only transport payloads, group membership read model and consent-gated person-linked responses."
                ),
                surfaceFamily: "relationship",
                presentationClass: "inspector",
                executionScope: "cloud",
                visibleActions: [
                    "campaign.createOrUpdate",
                    "campaign.updateSettings",
                    "campaign.title",
                    "campaign.contextText",
                    "campaign.questionsPerPage",
                    "campaign.endsAt",
                    "campaign.status",
                    "campaign.consentText",
                    "questions.replaceFromJSON",
                    "questions.upsert",
                    "questions.remove",
                    "recipients.importRows",
                    "recipients.selectForDelivery",
                    "recipients.selectGroupsForDelivery",
                    "delivery.emailSubject",
                    "delivery.emailBody",
                    "delivery.smsBody",
                    "delivery.preview",
                    "delivery.sendReady",
                    "delivery.recordFailure",
                    "respondent.openLink",
                    "respondent.saveDraft",
                    "respondent.submit",
                    "respondent.withdrawConsent",
                    "export.json",
                    "export.csv"
                ],
                skeleton: questionnaireCampaignSkeleton()
            ),
            makeDescriptor(
                name: "Meeting Intent",
                endpoint: PersonalMeetingCoordinatorContract.endpoint,
                label: "meetingCoordinator",
                sourceCellName: "PersonalMeetingCoordinatorCell",
                purpose: "Coordinate meeting intent safely",
                purposeDescription: "Foreslå møtetider og Jitsi-metadata som trygg placeholder uten native calendar, camera eller mic-permission.",
                interests: ["personal", "meeting", "jitsi", "intent", "safe-placeholder", "purpose=propose-accept-decline-no-native-permission"],
                menuSlots: ["upperRight", "lowerRight"],
                metadata: PersonalCopilotConfigurationMetadata(
                    policyCategory: "meeting-intent",
                    requiresUserGeneratedContentModeration: true,
                    universalLink: stagingLink("personal/meeting"),
                    reviewSummary: "MeetingBridge metadata only; Binding asks for native capability consent later."
                ),
                surfaceFamily: "relationship",
                presentationClass: "form",
                executionScope: "hybrid",
                visibleActions: ["editMeetingIntent", "proposeTimes", "acceptTime", "declineTime", "updateMeetingIntent", "clearMeetingIntent"],
                skeleton: meetingSkeleton()
            ),
            makeDescriptor(
                name: "Personal Co-Pilot Catalog",
                endpoint: PersonalCopilotAppStoreV1Contract.catalogEndpoint,
                label: "personalCatalog",
                sourceCellName: "PersonalCopilotConfigurationCatalogCell",
                purpose: "Personal Co-Pilot approved catalog",
                purposeDescription: "App Store-godkjent katalog som kun returnerer personal-copilot-v1-konfigurasjoner med policy, scope og execution metadata.",
                interests: ["personal", "catalog", "appstore", "configuration", "policy", "purpose=approved-personal-catalog"],
                menuSlots: ["lowerRight"],
                metadata: PersonalCopilotConfigurationMetadata(
                    policyCategory: "catalog",
                    requiresUserGeneratedContentModeration: false,
                    universalLink: stagingLink("personal/catalog"),
                    reviewSummary: "Catalog returns only Personal Co-Pilot V1 entries and excludes Conference/demo/admin surfaces."
                ),
                surfaceFamily: "catalog",
                presentationClass: "list",
                executionScope: "cloud",
                visibleActions: ["entries", "entries.allowed", "entries.unavailable", "entryDetail", "policySummary"],
                skeleton: catalogSkeleton()
            )
        ]
    }

    private static func localAndDeviceDescriptors() -> [Descriptor] {
        [
            makeDescriptor(
                name: "Personal Assistant Profile",
                endpoint: PersonalAssistantProfileContract.endpoint,
                label: "assistantProfile",
                sourceCellName: "PersonalAssistantProfileCell",
                purpose: "Configure an owner-scoped personal Co-Pilot",
                purposeDescription: "Gi Co-Piloten navn, eksplisitt formål, nødvendig innhold og interesser. Passiv adferdslæring er av, lokale modeller er standard og ekstern provider krever et separat valg med tillitspakke.",
                interests: [
                    "personal",
                    "assistant",
                    "copilot",
                    "privacy",
                    "owner-control",
                    "local-model-default",
                    "purposeRef=personal.chat.assist.guided-onboarding"
                ],
                menuSlots: ["upperLeft"],
                metadata: PersonalCopilotConfigurationMetadata(
                    policyCategory: "personal-assistant-profile",
                    requiresLogin: false,
                    requiresUserGeneratedContentModeration: false,
                    universalLink: stagingLink("personal/copilot/profile"),
                    reviewSummary: "Owner-scoped assistant preferences with explicit learning and provider policy. No provider invocation in this surface."
                ),
                surfaceFamily: "identity",
                presentationClass: "form",
                executionScope: "owner-scoped",
                visibleActions: [
                    PersonalAssistantProfileContract.setDisplayNameKeypath,
                    PersonalAssistantProfileContract.setDeclaredPurposeKeypath,
                    PersonalAssistantProfileContract.setNecessaryContentKeypath,
                    PersonalAssistantProfileContract.setDeclaredInterestsKeypath,
                    PersonalAssistantProfileContract.setInteractionStyleKeypath,
                    PersonalAssistantProfileContract.setLearningPolicyKeypath,
                    PersonalAssistantProfileContract.setProviderPolicyKeypath,
                    PersonalAssistantProfileContract.resetKeypath
                ],
                skeleton: personalAssistantProfileSkeleton()
            ),
            localDescriptor(
                name: "Personal Home",
                endpoint: "cell:///PersonalIdentity",
                label: "identity",
                sourceCellName: "PersonalIdentityCell",
                purpose: "Personal Co-Pilot startside",
                purposeDescription: "Lokal inngang til requester, public/private identity, samtykker, eksport og sletting uten sky-publisering.",
                interests: ["personal", "identity", "privacy", "account", "export", "delete"],
                menuSlots: ["upperLeft"],
                policyCategory: "identity-and-account",
                surfaceFamily: "identity",
                presentationClass: "hero",
                executionScope: "local",
                visibleActions: ["viewIdentity", "exportAccount", "deleteAccount"]
            ),
            localDescriptor(
                name: "My Profile",
                endpoint: "cell:///PersonalProfileDraft",
                label: "profileDraft",
                sourceCellName: "PersonalProfileDraftCell",
                purpose: "Private profile draft",
                purposeDescription: "Holder arbeidsutkast, preview og publiseringssamtykke lokalt for profilen sendes til CellScaffold.",
                interests: ["personal", "profile", "draft", "consent", "public-profile"],
                menuSlots: ["upperMid"],
                policyCategory: "profile-draft",
                surfaceFamily: "identity",
                presentationClass: "form",
                executionScope: "local",
                requiresUserGeneratedContentModeration: true,
                visibleActions: ["editDraft", "previewPublicProfile", "recordPublishConsent", "resetDraft"]
            ),
            localDescriptor(
                name: "Vault / Ideas",
                endpoint: "cell:///Vault",
                label: "vault",
                sourceCellName: "VaultCell",
                purpose: "Personal vault for ideas",
                purposeDescription: "Organiser ideer, prosjekter og notater lokalt. Remote flater får ikke vault-tilgang uten eksplisitt eksport eller deling.",
                interests: ["personal", "vault", "ideas", "projects", "notes", "markdown"],
                menuSlots: ["upperRight", "lowerRight"],
                policyCategory: "local-vault",
                surfaceFamily: "content",
                presentationClass: "detail",
                executionScope: "local",
                nativePermissionRequests: ["vault-on-explicit-action"],
                visibleActions: ["createNote", "editNote", "shareExplicitExport"]
            ),
            localDescriptor(
                name: "Privacy Audit",
                endpoint: "cell:///PersonalPrivacyAudit",
                label: "privacyAudit",
                sourceCellName: "PersonalPrivacyAuditCell",
                purpose: "Local privacy audit",
                purposeDescription: "Lokal logg som forklarer hva som ble publisert, rapportert, blokkert, slettet eller delt.",
                interests: ["personal", "privacy", "audit", "consent", "permissions", "remote-config"],
                menuSlots: ["lowerLeft"],
                policyCategory: "privacy-audit",
                surfaceFamily: "governance",
                presentationClass: "list",
                executionScope: "local",
                visibleActions: ["viewAuditEvents", "filterAuditEvents"]
            ),
            localDescriptor(
                name: "Apple Intelligence",
                endpoint: "cell:///AppleIntelligence",
                label: "appleIntelligence",
                sourceCellName: "AppleIntelligenceCell",
                purpose: "Device intelligence for Personal Co-Pilot",
                purposeDescription: "Lokale forslag og semantisk hjelp bak eksplisitt brukerhandling. Remote configs kan bare beskrive intent.",
                interests: ["personal", "assistant", "apple-intelligence", "semantic-matching"],
                menuSlots: ["upperMid"],
                policyCategory: "apple-intelligence",
                surfaceFamily: "intelligence",
                presentationClass: "detail",
                executionScope: "device",
                nativePermissionRequests: ["apple-intelligence-on-explicit-action"],
                visibleActions: ["requestLocalSuggestion", "applyUserApprovedSuggestion"]
            ),
            localDescriptor(
                name: "Entity Scanner",
                endpoint: "cell:///EntityScanner",
                label: "entityScanner",
                sourceCellName: "EntityScannerCell",
                purpose: "Entity Scanner for personal contact discovery",
                purposeDescription: "Oppdag naerliggende enheter med tydelige permissions. Remote cells mottar bare bruker-godkjente resultatsammendrag.",
                interests: ["personal", "scanner", "nearby", "identity", "peer", "proofs"],
                menuSlots: ["lowerLeft"],
                policyCategory: "hardware-scanner",
                surfaceFamily: "intelligence",
                presentationClass: "detail",
                executionScope: "device",
                nativePermissionRequests: ["nearby-on-explicit-action", "bluetooth-on-explicit-action"],
                visibleActions: ["requestScanPermission", "selectDiscoveredEntity", "shareApprovedProof"]
            ),
            localDescriptor(
                name: "Workflow Studio",
                endpoint: "cell:///WorkflowStudio",
                label: "workflowStudio",
                sourceCellName: "WorkflowStudioCell",
                purpose: "Workflow Studio for Personal Co-Pilot",
                purposeDescription: "Bygg og test personlige arbeidsflyter uten å eksponere skjulte remote features eller generell plugin-marketplace.",
                interests: ["personal", "workflow", "automation", "studio", "personal-productivity"],
                menuSlots: ["upperMid", "lowerMid"],
                policyCategory: "workflow-studio",
                surfaceFamily: "content",
                presentationClass: "detail",
                executionScope: "local",
                visibleActions: ["createWorkflow", "testWorkflow", "disableWorkflow"]
            )
        ]
    }

    private static func makeDescriptor(
        name: String,
        endpoint: String,
        label: String,
        sourceCellName: String,
        purpose: String,
        purposeDescription: String,
        interests: [String],
        menuSlots: [String],
        metadata: PersonalCopilotConfigurationMetadata,
        surfaceFamily: String,
        presentationClass: String,
        executionScope: String,
        visibleActions: [String],
        subscribeFeed: Bool = false,
        additionalReferences: [CellReference] = [],
        skeleton: SkeletonElement
    ) -> Descriptor {
        var configuration = CellConfiguration(name: name)
        configuration.description = purposeDescription
        let purposeInterests = interests + metadata.discoveryInterests + [
            "surfaceFamily=\(surfaceFamily)",
            "presentationClass=\(presentationClass)",
            "executionScope=\(executionScope)"
        ] + visibleActions.map { "visibleAction=\($0)" }
        configuration.discovery = CellConfigurationDiscovery(
            sourceCellEndpoint: endpoint,
            sourceCellName: sourceCellName,
            purpose: purpose,
            purposeDescription: purposeDescription,
            interests: PersonalCopilotValue.normalize(purposeInterests),
            menuSlots: menuSlots
        )
        configuration.cellReferences = [CellReference(endpoint: endpoint, subscribeFeed: subscribeFeed, label: label)] + additionalReferences
        configuration.skeleton = skeleton
        return Descriptor(
            configuration: configuration,
            metadata: metadata,
            sourceCellEndpoint: endpoint,
            sourceCellName: sourceCellName,
            purpose: purpose,
            purposeDescription: purposeDescription,
            interests: configuration.discovery?.interests ?? [],
            menuSlots: menuSlots,
            surfaceFamily: surfaceFamily,
            presentationClass: presentationClass,
            executionScope: executionScope,
            visibleActions: visibleActions
        )
    }

    private static func localDescriptor(
        name: String,
        endpoint: String,
        label: String,
        sourceCellName: String,
        purpose: String,
        purposeDescription: String,
        interests: [String],
        menuSlots: [String],
        policyCategory: String,
        surfaceFamily: String,
        presentationClass: String,
        executionScope: String,
        requiresUserGeneratedContentModeration: Bool = false,
        nativePermissionRequests: [String] = [],
        visibleActions: [String]
    ) -> Descriptor {
        makeDescriptor(
            name: name,
            endpoint: endpoint,
            label: label,
            sourceCellName: sourceCellName,
            purpose: purpose,
            purposeDescription: purposeDescription,
            interests: interests + ["purpose=\(visibleActions.joined(separator: "+"))"],
            menuSlots: menuSlots,
            metadata: PersonalCopilotConfigurationMetadata(
                policyCategory: policyCategory,
                requiresLogin: false,
                requiresUserGeneratedContentModeration: requiresUserGeneratedContentModeration,
                nativePermissionRequests: nativePermissionRequests,
                universalLink: stagingLink("personal/\(slug(name))"),
                reviewSummary: "Binding-owned \(executionScope) Personal Co-Pilot surface: \(purpose)."
            ),
            surfaceFamily: surfaceFamily,
            presentationClass: presentationClass,
            executionScope: executionScope,
            visibleActions: visibleActions,
            skeleton: localSurfaceSkeleton(
                title: name,
                purpose: purpose,
                purposeDescription: purposeDescription,
                executionScope: executionScope,
                visibleActions: visibleActions,
                nativePermissionRequests: nativePermissionRequests
            )
        )
    }

    private static func metadataObject(for descriptor: Descriptor) -> Object {
        var object = descriptor.metadata.objectValue()
        object["surfaceFamily"] = .string(descriptor.surfaceFamily)
        object["presentationClass"] = .string(descriptor.presentationClass)
        object["executionScope"] = .string(descriptor.executionScope)
        object["visibleActions"] = .list(descriptor.visibleActions.map(ValueType.string))
        return object
    }

    private static func entryID(for configuration: CellConfiguration) -> String {
        slug(configuration.name)
    }

    private static func stagingLink(_ path: String) -> String {
        "https://staging.haven.digipomps.org/app/\(path)"
    }

    private static func slug(_ value: String) -> String {
        value
            .lowercased()
            .replacingOccurrences(of: " / ", with: "-")
            .replacingOccurrences(of: " ", with: "-")
            .replacingOccurrences(of: "·", with: "-")
    }

    private static func pagePublisherSkeleton() -> SkeletonElement {
        var templateList = SkeletonList(
            topic: nil,
            keypath: "pagePublisher.state.templates",
            flowElementSkeleton: row([
                styledKeyText("title", role: "publisher-card-title"),
                styledKeyText("summary", role: "publisher-card-copy"),
                styledKeyText("status", role: "publisher-status-chip")
            ])
        )
        templateList.selectionMode = .single
        templateList.selectionValueKeypath = "id"
        templateList.selectionActionKeypath = "pagePublisher.selectTemplate"
        templateList.selectionPayloadMode = .itemID
        templateList.modifiers = publisherListModifiers(role: "publisher-template-list")

        var mediaList = SkeletonList(
            topic: nil,
            keypath: "pagePublisher.state.media",
            flowElementSkeleton: row([
                hstack([
                    styledKeyText("kind", role: "publisher-media-kind"),
                    styledKeyText("inclusionStatus", role: "publisher-status-chip")
                ], role: "publisher-media-meta"),
                styledKeyText("displayName", role: "publisher-card-title"),
                hstack([
                    styledKeyText("mimeType", role: "publisher-card-copy"),
                    styledKeyText("sizeLabel", role: "publisher-card-copy")
                ], role: "publisher-media-meta"),
                styledKeyText("moderationStatus", role: "publisher-card-copy")
            ])
        )
        mediaList.selectionMode = .single
        mediaList.selectionValueKeypath = "id"
        mediaList.selectionActionKeypath = "pagePublisher.selectMedia"
        mediaList.selectionPayloadMode = .itemID
        mediaList.modifiers = publisherListModifiers(role: "publisher-media-list")

        var publishedPages = SkeletonList(
            topic: nil,
            keypath: "pagePublisher.state.pages",
            flowElementSkeleton: row([
                styledKeyText("title", role: "publisher-card-title"),
                hstack([
                    styledKeyText("publishStatus", role: "publisher-status-chip"),
                    styledKeyText("mediaCount", role: "publisher-card-copy")
                ], role: "publisher-media-meta")
            ])
        )
        publishedPages.selectionMode = .single
        publishedPages.selectionValueKeypath = "id"
        publishedPages.selectionActionKeypath = "pagePublisher.selectPage"
        publishedPages.selectionPayloadMode = .itemID
        publishedPages.modifiers = publisherListModifiers(role: "publisher-page-list")

        var upload = SkeletonFileUpload(
            title: "Slipp media her",
            subtitle: "Bilder, video, lyd eller PDF",
            helperText: "Maks 25 MB per fil. Opplastingen er privat til du velger den inn på siden og publiserer.",
            valueKeypath: "pagePublisher.state.selectedMediaAssetID",
            stateKeypath: "pagePublisher.state.media",
            actionKeypath: "pagePublisher.uploadMedia",
            acceptedContentTypes: ["image/*", "audio/*", "video/*", "application/pdf"],
            allowsMultiple: false,
            supportsDrop: true,
            maxSizeBytes: PersonalPagePublisherCell.maximumUploadBytes,
            uploadMode: "chunked",
            submitOnSelection: true
        )
        upload.modifiers = publisherUploadModifiers()

        let draftPanel = adaptiveGrid([
            section("Innhold", [
                subtleText("Skriv det publikum faktisk skal møte. Private profilutkast og vault-data leses aldri automatisk."),
                textField("pagePublisher.state.draft.pageTitle", "pagePublisher.draft.pageTitle", "Navn på siden"),
                textArea("pagePublisher.state.draft.pageSummary", "pagePublisher.draft.pageSummary", "Fortell kort hvem du er og hva folk finner her", minLines: 5),
                hstack([
                    button("pagePublisher.refreshPreview", "Oppdater preview", payload: .object([:]), style: .secondary),
                    button("pagePublisher.publishPage", "Publiser side", payload: .object(["explicitPublishIntent": .bool(true)]), style: .primary)
                ], role: "publisher-actions")
            ], footer: "Publisering krever et eksplisitt klikk. Katalogføring er et eget valg.", modifiers: publisherSectionModifiers(role: "publisher-editor-card")),
            section("Live preview", [
                styledKeyText("pagePublisher.state.preview.title", role: "publisher-preview-title"),
                styledKeyText("pagePublisher.state.preview.summary", role: "publisher-preview-copy"),
                valueRow("Design", "pagePublisher.state.preview.templateID"),
                valueRow("Medier", "pagePublisher.state.preview.mediaCount"),
                styledKeyText("pagePublisher.state.readiness.humanSummary", role: "publisher-readiness"),
                subtleText("Siste handling"),
                keyText("pagePublisher.state.lastActionSummary")
            ], modifiers: publisherSectionModifiers(role: "publisher-preview-card"))
        ], minColumnWidth: 320, role: "publisher-editor-grid")

        let mediaPanel = adaptiveGrid([
            section("Last opp", [
                .FileUpload(upload),
                hstack([
                    button("pagePublisher.includeSelectedMedia", "Ta med på siden", payload: .object(["explicitMediaPublishIntent": .bool(true)]), style: .primary),
                    button("pagePublisher.excludeSelectedMedia", "Gjør privat", payload: .object([:]), style: .secondary),
                    button("pagePublisher.deleteSelectedMedia", "Slett", payload: .object(["explicitDeleteIntent": .bool(true)]), style: .secondary)
                ], role: "publisher-actions"),
                subtleText("Eierattestert V1-media kan publiseres på en side som ikke er katalogført. Offentlig medielevering og moderering må kobles før katalogpromotering.")
            ], modifiers: publisherSectionModifiers(role: "publisher-upload-card")),
            section("Lagringsplass", [
                styledKeyText("pagePublisher.state.storage.usedLabel", role: "publisher-storage-number"),
                valueRow("Inkludert", "pagePublisher.state.storage.includedQuotaLabel"),
                valueRow("Ledig", "pagePublisher.state.storage.remainingLabel"),
                valueRow("Maks per fil", "pagePublisher.state.storage.maximumUploadLabel"),
                keyText("pagePublisher.state.storage.billingSummary"),
                styledKeyText("pagePublisher.state.storage.pricingStatus", role: "publisher-status-chip")
            ], footer: "Mer lagring er en ikke-overførbar brukskvote. Ingen pris eller checkout vises før det faktisk er koblet.", modifiers: publisherSectionModifiers(role: "publisher-storage-card")),
            section("Dine medier", [
                .List(mediaList)
            ], footer: "Velg en rad for å styre om mediet skal være privat, med på siden eller slettes.", modifiers: publisherSectionModifiers(role: "publisher-library-card"))
        ], minColumnWidth: 300, role: "publisher-media-grid")

        let hostingPanel = stack([
            section(
                "Hosting, kostnad og sletting",
                [
                    subtleText("Før publisering må det være tydelig hvor siden ligger, hvilken kostnadsmodell som gjelder og hvem som kan slette den."),
                    textField("pagePublisher.state.draft.hostingPolicy.provider", "pagePublisher.draft.hostingProvider", "Hosting-provider, f.eks. dimy-hosted eller self-hosted"),
                    textField("pagePublisher.state.draft.hostingPolicy.costModel", "pagePublisher.draft.costModel", "included, self-hosted eller owner-paid"),
                    textField("pagePublisher.state.draft.hostingPolicy.estimatedMonthlyCost", "pagePublisher.draft.estimatedMonthlyCost", "Estimert månedskostnad"),
                    textField("pagePublisher.state.draft.hostingPolicy.deletionGuarantee", "pagePublisher.draft.deletionGuarantee", "Slettegaranti, f.eks. user-controlled"),
                    hstack([
                        button("pagePublisher.draft.directoryListed", "List i katalog", payload: .bool(true)),
                        button("pagePublisher.draft.directoryListed", "Skjul fra katalog", payload: .bool(false))
                    ], role: "publisher-actions"),
                    valueRow("Hosting avklart", "pagePublisher.state.draft.hostingPolicy.publishable"),
                    keyText("pagePublisher.state.readiness.humanSummary")
                ],
                footer: "Katalog er ikke det samme som offentlig side. Katalogføring velges eksplisitt og krever modererte medier.",
                modifiers: publisherSectionModifiers(role: "publisher-hosting-card")
            )
        ])

        let templatesPanel = stack([
            section(
                "Velg uttrykk",
                [
                    subtleText("Velg en rad. Creator portfolio støtter eksplisitt valgte medier; mer spesialiserte musikk- og tjenesteflater kobles til egne celler."),
                    .List(templateList)
                ],
                modifiers: publisherSectionModifiers(role: "publisher-design-card")
            )
        ])

        let publishedPanel = stack([
            section(
                "Publiserte sider",
                [
                    .List(publishedPages),
                    valueRow("Tittel", "pagePublisher.state.publicReadModel.title"),
                    valueRow("Offentlig URL", "pagePublisher.state.publicReadModel.publicURL"),
                    valueRow("Levering", "pagePublisher.state.publicReadModel.publicURLStatus"),
                    valueRow("Medier", "pagePublisher.state.publicReadModel.mediaCount"),
                    valueRow("Medielevering", "pagePublisher.state.publicReadModel.mediaDeliveryStatus"),
                    hstack([
                        button("pagePublisher.unpublishPage", "Avpubliser valgt", payload: .object([:])),
                        button("pagePublisher.deletePage", "Slett valgt", payload: .object(["explicitDeleteIntent": .bool(true)]))
                    ], role: "publisher-actions")
                ],
                footer: "Avpublisering gjør publicReadModel null. Sletting av siden sletter ikke private mediefiler; de styres i Media-fanen.",
                modifiers: publisherSectionModifiers(role: "publisher-published-card")
            )
        ])

        let safetyPanel = stack([
            section(
                "Personvern og begrensninger",
                [
                    text("Mediefiler lagres privat ved opplasting. Bare eksplisitt valgte manifest blir kopiert inn i public read model når du publiserer siden."),
                    text("Katalogføring blokkeres for eierattestert V1-media til moderering er koblet. En ukatalogisert side kan publiseres med samme tydelige V1-status."),
                    text("Slug og endelig public URL krever hosting-infrastruktur. Feltet publicURL er derfor bevisst 'not-assigned-yet' inntil hosting er koblet på."),
                    text("Lagringskvoten er tilgang til lagringskapasitet, ikke penger, saldo eller en overførbar verdi. Pris og betalingsflyt er ikke koblet i V1."),
                    text("Hvis en AI-assistent hjelper med teksten, skal forslaget alltid forhåndsvises og publiseres med eksplisitt klikk fra brukeren.")
                ],
                modifiers: publisherSectionModifiers(role: "publisher-safety-card")
            )
        ])

        return stack([
            section("", [
                styledKeyText("pagePublisher.state.publishStatus", role: "publisher-hero-eyebrow"),
                text("Din side. Ditt uttrykk."),
                subtleText("Bygg en offentlig flate med tekst og media – med private utkast, tydelige kostnadsgrenser og eksplisitt publisering."),
                hstack([
                    styledKeyText("pagePublisher.state.readiness.humanSummary", role: "publisher-hero-status"),
                    styledKeyText("pagePublisher.state.storage.remainingLabel", role: "publisher-hero-storage")
                ], role: "publisher-hero-meta")
            ], modifiers: publisherHeroModifiers()),
            .Tabs(SkeletonTabs(
                tabsKeypath: "pagePublisher.state.tabs",
                activeTabStateKeypath: "pagePublisher.state.activeTab",
                selectionActionKeypath: "pagePublisher.setActiveTab",
                panels: [
                    SkeletonTabPanel(id: "draft", content: [draftPanel]),
                    SkeletonTabPanel(id: "media", content: [mediaPanel]),
                    SkeletonTabPanel(id: "templates", content: [templatesPanel]),
                    SkeletonTabPanel(id: "hosting", content: [hostingPanel]),
                    SkeletonTabPanel(id: "published", content: [publishedPanel]),
                    SkeletonTabPanel(id: "safety", content: [safetyPanel])
                ]
            ))
        ], role: "personal-page-publisher")
    }

    private static func profilePublisherSkeleton() -> SkeletonElement {
        stack([
            text("Publish Public Profile"),
            text("Skriv bare data som skal kunne publiseres offentlig. Publish krever eksplisitt samtykke."),
            keyText("profilePublisher.state.publishStatus"),
            keyText("profilePublisher.state.visibility"),
            .TextField(SkeletonTextField(
                sourceKeypath: "profilePublisher.state.publishDraft.displayName",
                targetKeypath: "profilePublisher.publishDraft.displayName",
                placeholder: "Public display name"
            )),
            .TextField(SkeletonTextField(
                sourceKeypath: "profilePublisher.state.publishDraft.headline",
                targetKeypath: "profilePublisher.publishDraft.headline",
                placeholder: "Public headline"
            )),
            .TextArea(SkeletonTextArea(
                sourceKeypath: "profilePublisher.state.publishDraft.summary",
                targetKeypath: "profilePublisher.publishDraft.summary",
                placeholder: "Public summary",
                minLines: 3,
                maxLines: 7,
                submitOnEnter: false,
                editorMode: .plain
            )),
            .TextField(SkeletonTextField(
                sourceKeypath: "profilePublisher.state.publishDraft.interestsText",
                targetKeypath: "profilePublisher.publishDraft.interestsText",
                placeholder: "Public interests, comma separated"
            )),
            .HStack(SkeletonHStack(elements: [
                button("profilePublisher.publishProfile", "Publish with consent", payload: .object(["explicitPublishIntent": .bool(true)])),
                button("profilePublisher.unpublishProfile", "Unpublish", payload: .object([:])),
                button("profilePublisher.deleteProfile", "Delete", payload: .object([:]))
            ], spacing: 8)),
            keyText("profilePublisher.state.publicReadModel.displayName"),
            keyText("profilePublisher.state.publicReadModel.summary")
        ])
    }

    private static func directorySkeleton() -> SkeletonElement {
        var directoryResultRow = row([
            keyText("displayName"),
            keyText("headline"),
            keyText("summary"),
            keyText("moderationStatus")
        ])
        directoryResultRow.modifiers = personDragModifiers(payloadKeypath: "publicSafeDragPayload")

        var results = SkeletonList(
            topic: nil,
            keypath: "directory.state.lastSearch.results",
            flowElementSkeleton: directoryResultRow
        )
        results.selectionMode = .single
        results.selectionValueKeypath = "id"
        return stack([
            text("Public Profile Directory"),
            text("Søk i profiler brukere har publisert. Report, hide og block virker på valgt eller første synlige resultat."),
            keyText("directory.state.moderationStatus"),
            .TextField(SkeletonTextField(
                sourceKeypath: "directory.state.query",
                targetKeypath: "directory.query",
                placeholder: "Search public profiles"
            )),
            .HStack(SkeletonHStack(elements: [
                button("directory.searchProfiles", "Search", payload: .object([:])),
                button("directory.reportProfile", "Report result", payload: .object(["reason": .string("user_reported_from_directory")])),
                button("directory.hideProfile", "Hide result", payload: .object([:])),
                button("directory.blockProfile", "Block result", payload: .object([:]))
            ], spacing: 8)),
            .List(results),
            keyText("directory.state.blockedProfileCount")
        ])
    }

    private static func matchmakingSkeleton() -> SkeletonElement {
        var suggestions = SkeletonList(
            topic: nil,
            keypath: "matchmaking.state.matchSuggestions",
            flowElementSkeleton: row([
                keyText("profile.displayName"),
                keyText("profile.headline"),
                keyText("reasons"),
                keyText("chatEligible")
            ])
        )
        suggestions.selectionMode = .single
        suggestions.selectionValueKeypath = "profile.id"
        return stack([
            text("Matches"),
            text("Forslag kan be om samtykke, men starter aldri chat automatisk."),
            keyText("matchmaking.state.requiresMutualApprovalForChat"),
            .TextField(SkeletonTextField(
                sourceKeypath: "matchmaking.state.preferencesText",
                targetKeypath: "matchmaking.preferencesText",
                placeholder: "Preferences, comma separated"
            )),
            .HStack(SkeletonHStack(elements: [
                button("matchmaking.refreshSuggestions", "Refresh suggestions", payload: .object([:])),
                button("matchmaking.requestMatchConsent", "Request consent", payload: .object([:])),
                button("matchmaking.acceptMatchConsent", "Accept match", payload: .object([:])),
                button("matchmaking.declineMatchConsent", "Decline match", payload: .object([:])),
                button("matchmaking.clearMatchSuggestion", "Clear suggestion", payload: .object([:]))
            ], spacing: 8)),
            .List(suggestions),
            keyText("matchmaking.state.matchConsentStatus")
        ])
    }

    private static func chatHubSkeleton() -> SkeletonElement {
        var candidateRow = row([
            keyText("displayName"),
            keyText("headline"),
            valueRow("Kontakt-endepunkt", "contactEndpoint.endpointID")
        ])
        candidateRow.modifiers = personDragModifiers(payloadKeypath: "publicSafeDragPayload")

        var candidates = SkeletonList(
            topic: nil,
            keypath: "chatHub.state.assistant.latestSuggestion.candidates",
            flowElementSkeleton: candidateRow
        )
        candidates.selectionMode = .single
        candidates.selectionValueKeypath = "id"
        candidates.selectionActionKeypath = "chatHub.assistant.selectCandidate"
        candidates.selectionPayloadMode = .itemID

        let intentCandidates = SkeletonList(
            topic: nil,
            keypath: "chatHub.state.assistant.intentCandidates",
            flowElementSkeleton: row([
                keyText("kind"),
                valueRow("Purpose", "purposeRef"),
                valueRow("Score", "weightedScore"),
                valueRow("Tilgjengelig", "availability")
            ])
        )

        var resourceMatches = SkeletonList(
            topic: nil,
            keypath: "chatHub.state.assistant.resourceMatches",
            flowElementSkeleton: resourceMatchCardRow()
        )
        resourceMatches.selectionMode = .single
        resourceMatches.selectionValueKeypath = "id"
        resourceMatches.selectionActionKeypath = "chatHub.ui.openMatchedResourceLibrary"
        resourceMatches.selectionPayloadMode = .itemID
        resourceMatches.modifiers = resourceMatchListModifiers()

        var docsRAGDocumentationMatches = SkeletonList(
            topic: nil,
            keypath: "chatHub.state.docsRAG.documentationMatches",
            flowElementSkeleton: row([
                keyText("title"),
                keyText("summary")
            ])
        )
        docsRAGDocumentationMatches.selectionMode = .single
        docsRAGDocumentationMatches.selectionValueKeypath = "id"
        docsRAGDocumentationMatches.selectionActionKeypath = "chatHub.docsRAG.openTopDocument"
        docsRAGDocumentationMatches.selectionPayloadMode = .itemID

        var docsRAGRAGMatches = SkeletonList(
            topic: nil,
            keypath: "chatHub.state.docsRAG.ragMatches",
            flowElementSkeleton: row([
                keyText("title"),
                keyText("summary")
            ])
        )
        docsRAGRAGMatches.selectionMode = .single
        docsRAGRAGMatches.selectionValueKeypath = "id"
        docsRAGRAGMatches.selectionActionKeypath = "chatHub.docsRAG.askRAG"
        docsRAGRAGMatches.selectionPayloadMode = .itemID

        let entityExtensions = SkeletonList(
            topic: nil,
            keypath: "chatHub.state.entityExtension.extensions",
            flowElementSkeleton: row([
                keyText("title"),
                valueRow("Type", "kind"),
                valueRow("Tilgang", "grantStatus")
            ])
        )

        let providerMatches = SkeletonList(
            topic: nil,
            keypath: "chatHub.state.assistant.assistantProviders",
            flowElementSkeleton: row([
                keyText("title"),
                valueRow("Type", "kind"),
                valueRow("Tilgang", "availability")
            ])
        )

        var messages = SkeletonList(
            topic: nil,
            keypath: "chatHub.state.messages",
            flowElementSkeleton: row([
                keyText("authorDisplayName"),
                keyText("body")
            ])
        )
        var messageListModifiers = SkeletonModifiers()
        messageListModifiers.styleRole = "chat-message-list"
        messageListModifiers.styleClasses = ["chat-message-list"]
        messages.modifiers = messageListModifiers

        var promptLog = SkeletonList(
            topic: nil,
            keypath: "chatHub.state.ui.promptMessages",
            flowElementSkeleton: row([
                keyText("speaker"),
                keyText("body"),
                keyText("statusText"),
                assistantResponseActions(),
                widgetSourceCards(modifiers: componentSurfaceCardModifiers())
            ])
        )
        var promptLogModifiers = SkeletonModifiers()
        promptLogModifiers.styleRole = "chat-prompt-log"
        promptLogModifiers.styleClasses = ["chat-prompt-log"]
        promptLog.modifiers = promptLogModifiers

        var clarificationOptionRow = row([
            keyText("title"),
            keyText("summary"),
            hstack([
                button(
                    "chatHub.assistant.answerClarification",
                    "Velg",
                    payload: nil,
                    style: .primary,
                    payloadKeypath: "actionPayload"
                )
            ])
        ])
        clarificationOptionRow.modifiers = clarificationOptionCardModifiers()
        var clarificationOptions = SkeletonList(
            topic: nil,
            keypath: "chatHub.state.assistant.clarification.options",
            flowElementSkeleton: clarificationOptionRow
        )
        clarificationOptions.activationActionKeypath = "chatHub.assistant.answerClarification"
        clarificationOptions.selectionValueKeypath = "id"
        clarificationOptions.selectionPayloadMode = .item
        clarificationOptions.modifiers = clarificationOptionListModifiers()

        var clarificationCard = SkeletonVStack(elements: [
            keyText("chatHub.state.assistant.clarification.question"),
            .List(clarificationOptions)
        ], spacing: 8)
        clarificationCard.modifiers = clarificationCardModifiers()

        var routeExplanationCard = SkeletonVStack(elements: [
            keyText("chatHub.state.assistant.routeExplanation.summary"),
            keyText("chatHub.state.assistant.routeExplanation.detailText"),
            hstack([
                // Denne veien finnes bare naar en ekstern lane faktisk kan spoerres.
                // Uten vilkaaret svarte knappen alltid «ikke tilgjengelig i V1».
                visibleButton(
                    "chatHub.assistant.reinterpretDraft",
                    "Tolk med sterkere modell",
                    payload: .object([:]),
                    style: .secondary,
                    visibleWhen: "chatHub.state.ui.automaticEscalation.canAskStrongerModelThisTime"
                )
            ])
        ], spacing: 8)
        routeExplanationCard.modifiers = routeExplanationCardModifiers()

        let automaticEscalationControls = section(
            "Automatisk tolkning",
            [
                hstack([
                    valueRow("Tak", "chatHub.state.ui.automaticEscalation.interpreterCeilingModeLabel"),
                    valueRow("Kvote", "chatHub.state.ui.automaticEscalation.quotaSummary")
                ], role: "chat-escalation-meter"),
                styledKeyText("chatHub.state.ui.automaticEscalation.lastDecisionExplanation", role: "chat-escalation-meter"),
                hstack([
                    automaticEscalationPauseButton(paused: true),
                    automaticEscalationPauseButton(paused: false)
                ], role: "chat-escalation-pause")
            ],
            modifiers: automaticEscalationMeterModifiers()
        )

        let automaticEscalationConsent = section(
            "Samtykke for ekstern tolkning",
            [
                styledKeyText("chatHub.state.ui.automaticEscalation.lastDecisionExplanation", role: "chat-escalation-consent-summary"),
                hstack([
                    button("chatHub.ui.dismissComponentSurface", "Avbryt", payload: .object([:]), style: .secondary),
                    button(
                        "chatHub.assistant.issueEscalationGrant",
                        "Tillat 7 dager",
                        payload: .object([
                            "durationOption": .string("7d"),
                            "providerKind": .string("api_gateway"),
                            "modelClass": .string("external_api_gateway"),
                            "allowedDataClasses": .list([.string("public_text")]),
                            "maximumAutomaticInterpretations": .integer(5),
                            "maximumEstimatedCostMicros": .integer(0),
                            "currency": .string("USD")
                        ]),
                        style: .primary
                    )
                ], role: "chat-escalation-consent-actions"),
                hstack([
                    button(
                        "chatHub.assistant.issueEscalationGrant",
                        "Tillat 24 timer",
                        payload: .object([
                            "durationOption": .string("24h"),
                            "providerKind": .string("api_gateway"),
                            "modelClass": .string("external_api_gateway"),
                            "allowedDataClasses": .list([.string("public_text")]),
                            "maximumAutomaticInterpretations": .integer(5),
                            "maximumEstimatedCostMicros": .integer(0),
                            "currency": .string("USD")
                        ]),
                        style: .secondary
                    )
                ], role: "chat-escalation-consent-duration")
            ],
            modifiers: automaticEscalationConsentModifiers()
        )

        // «Sjekk sterkere modell» kalte `assistant.reinterpretDraft`, som alltid
        // svarer `no_stronger_lane_available` (CloudStore). Knappen lovet altsaa
        // noe den aldri kunne levere, og den viste seg nettopp naar taket sto paa
        // «spoer hver gang». Kortet forklarer i stedet hva som gjelder, og peker
        // paa modellvalget som faktisk finnes under Mer → AI.
        // Knappen kaller `assistant.reinterpretDraft`, som ikke kjoerer en ny
        // tolkning: veien til en sterkere modell er ikke bygget, og skal ikke
        // bygges uten en beslutning om samtykke per tur. Svaret navngir naa den
        // faktiske grunnen (CloudStore), og linja under sier hvor modellvalget
        // som finnes faktisk ligger. Da lover flaten ikke mer enn den holder.
        var askThisTimeCard = SkeletonVStack(elements: [
            styledKeyText("chatHub.state.ui.automaticEscalation.lastDecisionExplanation", role: "chat-ask-this-time"),
            text("Ekstern tolkning skjer bare innenfor et samtykke du har gitt. Modellvalg og status ligger under Mer → AI."),
            hstack([
                button("chatHub.assistant.reinterpretDraft", "Sjekk sterkere modell", payload: .object([:]), style: .secondary)
            ], role: "chat-ask-this-time")
        ], spacing: 8)
        askThisTimeCard.modifiers = askThisTimeCardModifiers()

        let threads = SkeletonList(
            topic: nil,
            keypath: "chatHub.state.threads",
            flowElementSkeleton: row([
                keyText("title"),
                valueRow("Status", "moderationStatus")
            ])
        )

        let invites = SkeletonList(
            topic: nil,
            keypath: "chatHub.state.invites",
            flowElementSkeleton: row([
                keyText("title"),
                valueRow("Status", "invitationStatus")
            ])
        )

        var inlinePollOptionRow = row([
            hstack([
                button(
                    "chatHub.poll.vote",
                    "Stem",
                    payload: nil,
                    style: .secondary,
                    labelKeypath: "label",
                    payloadKeypath: "votePayload"
                ),
                styledKeyText("voteSummary", role: "chat-inline-poll-count"),
                styledKeyText("selectedSummary", role: "chat-inline-poll-selected")
            ], role: "chat-inline-poll-option")
        ])
        inlinePollOptionRow.modifiers = inlinePollOptionModifiers()
        var inlinePollOptions = SkeletonList(
            topic: nil,
            keypath: "options",
            flowElementSkeleton: inlinePollOptionRow
        )
        inlinePollOptions.modifiers = inlinePollOptionsModifiers()

        var inlinePollRow = row([
            hstack([
                styledKeyText("typeLabel", role: "chat-inline-poll-badge"),
                styledKeyText("summary", role: "chat-inline-poll-summary")
            ], role: "chat-inline-poll-header"),
            styledKeyText("question", role: "chat-inline-poll-question"),
            .List(inlinePollOptions),
            hstack([
                button(
                    "chatHub.poll.close",
                    "Lukk",
                    payload: nil,
                    style: .secondary,
                    payloadKeypath: "closePayload"
                )
            ], role: "chat-inline-poll-actions")
        ])
        inlinePollRow.modifiers = inlinePollCardModifiers()
        var polls = SkeletonList(
            topic: nil,
            keypath: "chatHub.state.polls",
            flowElementSkeleton: inlinePollRow
        )
        polls.modifiers = inlinePollListModifiers()

        let workbenchModules = SkeletonList(
            topic: nil,
            keypath: "chatHub.state.workbench.modules",
            flowElementSkeleton: row([
                keyText("title"),
                valueRow("Type", "kind"),
                valueRow("Status", "status")
            ])
        )

        let capabilityRequests = SkeletonList(
            topic: nil,
            keypath: "chatHub.state.capabilityRequests",
            flowElementSkeleton: row([
                keyText("title"),
                valueRow("Til", "destination"),
                valueRow("Status", "status")
            ])
        )

        var pinnedComponentChipRow = row([
            hstack([
                keyText("title"),
                button("chatHub.ui.dismissComponentSurface", "×", payload: .object([:]), style: .secondary)
            ])
        ])
        pinnedComponentChipRow.modifiers = pinnedComponentChipModifiers()
        var pinnedComponentSurfaces = SkeletonList(
            topic: nil,
            keypath: "chatHub.state.ui.pinnedComponentSurfaces",
            flowElementSkeleton: pinnedComponentChipRow
        )
        pinnedComponentSurfaces.activationActionKeypath = "chatHub.ui.restoreComponentSurface"
        pinnedComponentSurfaces.selectionValueKeypath = "id"
        pinnedComponentSurfaces.selectionPayloadMode = .itemID
        pinnedComponentSurfaces.modifiers = pinnedComponentChipListModifiers()

        var advancedComponentSurfaceRow = row([
                keyText("title"),
                keyText("summary"),
                valueRow("Fra prompt", "sourcePromptPreview"),
                hstack([
                    button("chatHub.ui.restoreComponentSurface", "Åpne", payload: .object([:]), style: .secondary),
                    button("chatHub.ui.minimizeComponentSurface", "−", payload: .object([:]), style: .secondary),
                    button("chatHub.ui.pinComponentSurface", "Fest", payload: .object([:]), style: .secondary),
                    button("chatHub.ui.dismissComponentSurface", "×", payload: .object([:]), style: .secondary)
                ])
        ])
        advancedComponentSurfaceRow.modifiers = componentSurfaceCardModifiers()
        let advancedComponentSurfaces = SkeletonList(
            topic: nil,
            keypath: "chatHub.state.ui.componentSurfaces",
            flowElementSkeleton: advancedComponentSurfaceRow
        )

        var activeToolChipRow = row([
            hstack([
                keyText("title"),
                button("chatHub.ui.dismissComponentSurface", "×", payload: .object([:]), style: .secondary)
            ])
        ])
        activeToolChipRow.modifiers = activeToolChipModifiers()
        var activeToolChips = SkeletonList(
            topic: nil,
            keypath: "chatHub.state.ui.activeToolChips",
            flowElementSkeleton: activeToolChipRow
        )
        activeToolChips.activationActionKeypath = "chatHub.ui.restoreComponentSurface"
        activeToolChips.selectionValueKeypath = "id"
        activeToolChips.selectionPayloadMode = .itemID
        activeToolChips.modifiers = activeToolChipListModifiers()

        var minimizedComponentSurfaces = SkeletonList(
            topic: nil,
            keypath: "chatHub.state.ui.minimizedComponentSurfaces",
            flowElementSkeleton: row([
                hstack([
                    keyText("title"),
                    button("chatHub.ui.dismissComponentSurface", "×", payload: .object([:]), style: .secondary)
                ])
            ])
        )
        minimizedComponentSurfaces.activationActionKeypath = "chatHub.ui.restoreComponentSurface"
        minimizedComponentSurfaces.selectionValueKeypath = "id"
        minimizedComponentSurfaces.selectionPayloadMode = .itemID
        minimizedComponentSurfaces.modifiers = minimizedComponentChipListModifiers()

        let absorbedChats = SkeletonList(
            topic: nil,
            keypath: "chatHub.state.ui.absorbedChats",
            flowElementSkeleton: row([
                keyText("sourceBadge"),
                keyText("summary"),
                valueRow("Tilgang", "grantStatus")
            ])
        )

        let promptParticipants = SkeletonList(
            topic: nil,
            keypath: "chatHub.state.ui.promptParticipants",
            flowElementSkeleton: row([
                keyText("badge"),
                keyText("title"),
                keyText("summary")
            ])
        )

        let composer = SkeletonTextArea(
            sourceKeypath: "chatHub.state.composer.body",
            targetKeypath: "chatHub.setComposer",
            placeholder: "F.eks. \"start Arendalsuka-onboarding\", \"vis meg programmet\", \"inviter Anna\" eller \"vi trenger avstemning\"",
            minLines: 3,
            maxLines: 8,
            submitOnEnter: true,
            editorMode: .plain,
            modifiers: composerModifiers()
        )

        // Startforslag: repertoaret som ett klikk. Vises bare i en tom samtale,
        // saa flaten ikke maser naar brukeren allerede er i gang. Uten dette
        // moeter en ny bruker et tomt felt og maa gjette hva Butler kan.
        var starterRow = row([
            keyText("title"),
            keyText("summary"),
            hstack([
                button(
                    "chatHub.prompt.submit",
                    "Prøv",
                    payload: nil,
                    style: .secondary,
                    payloadKeypath: "actionPayload"
                )
            ])
        ])
        starterRow.modifiers = starterRowModifiers()
        let starterList = SkeletonList(
            topic: nil,
            keypath: "chatHub.state.ui.starterSuggestions",
            flowElementSkeleton: starterRow
        )
        var starterCard = SkeletonVStack(elements: [
            text("Slik kan jeg hjelpe deg i gang"),
            .List(starterList)
        ], spacing: 8)
        starterCard.modifiers = starterCardModifiers()

        // Hjelpelinja: det co-piloten allerede regnet ut naar den ikke fant en
        // hjelper, men som ingen flate viste foer naa.
        var promptHelpLine = SkeletonVStack(elements: [
            styledKeyText("chatHub.state.ui.promptHelpSummary", role: "chat-help-line-text")
        ], spacing: 4)
        promptHelpLine.modifiers = promptHelpLineModifiers()

        let composerDock = stack(
            [
                text("Hva vil du få gjort?"),
                .VStack(starterCard),
                .VStack(promptHelpLine),
                .List(activeToolChips),
                .List(pinnedComponentSurfaces),
                .List(minimizedComponentSurfaces),
                .TextArea(composer),
                hstack([
                    button("chatHub.prompt.submit", "Send", payload: .object([:]), style: .primary),
                    button("chatHub.clearComposer", "Rydd utkast", payload: .object([:]), style: .secondary)
                ])
            ],
            role: "chat-composer-dock"
        )

        // Kortene hoerer hjemme INNE i rulleomraadet, ikke som soesken av det.
        // Som soesken ble de egne rader i seksjonens rutenett, og fire synlige
        // kort spiste hele hoeyden: loggraden ble 0 px og det nederste kortet
        // havnet utenfor rammen uten noe aa rulle i. Inne i rullefeltet foelger
        // de samtalen, og det nyeste ligger nederst der leseren ser det.
        let promptScroll = scrollView(
            [
                .List(promptLog),
                .VStack(clarificationCard),
                .VStack(routeExplanationCard),
                automaticEscalationControls,
                automaticEscalationConsent,
                .VStack(askThisTimeCard)
            ],
            role: "chat-prompt-scroll"
        )

        let conversation = section(
            "Butler Chat",
            [
                promptScroll,
                composerDock
            ],
            modifiers: chatConversationModifiers()
        )

        let active = stack([
            hstack([
                button("chatHub.ui.setActiveTab", "Til samtale", payload: .object(["activeTab": .string("samtale")]), style: .secondary)
            ]),
            section(
                "Demo story",
                [
                    subtleText("Rollebasert konferansefortelling. Co-piloten starter historien, mens eksisterende conference-celler viser dataene."),
                    valueRow("Status", "chatHub.state.demoStory.storyBar.status"),
                    valueRow("Rolle", "chatHub.state.demoStory.storyBar.role"),
                    valueRow("Simulert tid", "chatHub.state.demoStory.storyBar.simulatedTime"),
                    keyText("chatHub.state.demoStory.storyBar.currentStep"),
                    keyText("chatHub.state.demoStory.storyBar.nextStep"),
                    hstack([
                        button("chatHub.demoStory.activate", "Deltaker", payload: .object(["role": .string("participant")])),
                        button("chatHub.demoStory.activate", "Sponsor", payload: .object(["role": .string("sponsor")])),
                        button("chatHub.demoStory.activate", "Utstiller", payload: .object(["role": .string("exhibitor")])),
                        button("chatHub.demoStory.activate", "Arrangør", payload: .object(["role": .string("organizer")]))
                    ]),
                    hstack([
                        button("chatHub.demoStory.previousStep", "Forrige", payload: .object([:])),
                        button("chatHub.demoStory.nextStep", "Neste steg", payload: .object([:]), style: .primary),
                        button("chatHub.demoStory.prepareSimulationPopulation", "Seed demo-folk", payload: .object(["count": .integer(24)])),
                        button("chatHub.demoStory.reset", "Stopp", payload: .object([:]))
                    ]),
                    .List(SkeletonList(
                        topic: nil,
                        keypath: "chatHub.state.demoStory.sidePanelCards",
                        flowElementSkeleton: row([
                            keyText("title"),
                            keyText("subtitle"),
                            keyText("detail")
                        ])
                    )),
                    .List(SkeletonList(
                        topic: nil,
                        keypath: "chatHub.state.demoStory.missingData",
                        flowElementSkeleton: row([
                            keyText("title"),
                            valueRow("Status", "status"),
                            keyText("detail")
                        ])
                    ))
                ]
            ),
            section(
                "Minimerte hjelpere",
                [
                    .List(minimizedComponentSurfaces)
                ],
                modifiers: motionSurfaceModifiers(role: "minimized-helper-pill", hint: .restore, sourceRole: "component-surface")
            ),
            section(
                "Chatter med mennesker",
                [
                    .List(messages),
                    text("Avstemninger"),
                    .List(polls),
                    hstack([
                        button("chatHub.sendComposedMessage", "Send melding", payload: .object([:]), style: .primary),
                        button("chatHub.clearComposer", "Rydd utkast", payload: .object([:]), style: .secondary)
                    ]),
                    .List(absorbedChats),
                    hstack([
                        button("chatHub.setCombinedChatView", "Kombinert med badges", payload: .bool(true)),
                        button("chatHub.setCombinedChatView", "En chat om gangen", payload: .bool(false)),
                        button("chatHub.releaseAbsorbedChat", "Slipp aktiv chat", payload: .object([:]))
                    ])
                ]
            ),
            section(
                "Invitasjoner",
                [
                    text("Invitasjoner"),
                    .List(invites),
                    hstack([
                        button("chatHub.acceptInvite", "Godta invitasjon", payload: .object([:])),
                    button("chatHub.declineInvite", "Avslå invitasjon", payload: .object([:]))
                    ])
                ]
            ),
            section(
                "Opprettet fra chat",
                [
                    valueRow("Antall", "chatHub.state.workbench.moduleCount"),
                    .List(workbenchModules)
                ]
            ),
            section(
                "Meldte behov",
                [
                    .List(capabilityRequests)
                ]
            )
        ])

        let aiPanel = stack([
            section(
                "AI",
                [
                    valueRow("Anbefalt", "chatHub.state.assistant.providerRecommendation.title"),
                    keyText("chatHub.state.assistant.providerRecommendation.reason"),
                    hstack([
                        button("chatHub.assistant.provider.recommend", "Velg beste provider", payload: .object([:]), style: .primary),
                        button("chatHub.assistant.provider.status", "Sjekk bruk og nøkler", payload: .object([:])),
                        button("chatHub.assistant.provider.invoke", "Spør valgt modell", payload: .object([:])),
                        button("chatHub.ui.openComponentSurface", "Åpne docs/RAG", payload: .object(["kind": .string("docs-rag")])),
                        button("chatHub.docsRAG.askRAG", "Spør tilgjengelig RAG", payload: .object([:]))
                    ]),
                    valueRow("Gateway", "chatHub.state.assistant.providerUsageStatus.providerLabel"),
                    valueRow("Nøkkel", "chatHub.state.assistant.providerUsageStatus.activeCredentialSource"),
                    valueRow("Kvote", "chatHub.state.assistant.providerUsageStatus.lastQuotaStatus"),
                    keyText("chatHub.state.assistant.providerUsageStatus.answer"),
                    valueRow("Tokens", "chatHub.state.assistant.providerUsageStatus.lastUsage.totalTokens"),
                    valueRow("Kost", "chatHub.state.assistant.providerUsageStatus.lastPricingEstimate.priceMinorUnits"),
                    valueRow("Modellstatus", "chatHub.state.assistant.providerInvocation.status"),
                    keyText("chatHub.state.assistant.providerInvocation.answer"),
                    valueRow("RAG-svar", "chatHub.state.assistant.resourceQuery.answer")
                ]
            )
        ])

        let accessPanel = stack([
            section(
                "Tilgang",
                [
                    valueRow("Status", "chatHub.state.entityExtension.status"),
                    valueRow("Antall", "chatHub.state.entityExtension.extensionCount"),
                    keyText("chatHub.state.entityExtension.summary"),
                    hstack([
                        button("chatHub.entityExtension.scan", "Skann tilgang", payload: .object(["query": .string("hva har jeg tilgang til på enhetene mine og i skyen?")]), style: .primary),
                        button("chatHub.assistant.provider.recommend", "Velg provider", payload: .object([:]))
                    ]),
                    .List(entityExtensions)
                ]
            )
        ])

        var approveIdentityBinding = SkeletonButton(
            keypath: "chatHub.collaboration.approveIdentityBinding",
            label: "Godkjenn tilgang",
            payload: .object([:]),
            payloadKeypath: "identityBinding.approvalPayload"
        )
        approveIdentityBinding.modifiers = primaryButtonModifiers()
        approveIdentityBinding.modifiers?.visibility = SkeletonVisibilityRule(when: SkeletonCondition(
            scope: .item,
            keypath: "identityBinding.canApprove",
            equals: .bool(true)
        ))
        var rejectIdentityBinding = SkeletonButton(
            keypath: "chatHub.collaboration.rejectIdentityBinding",
            label: "Avslå",
            payload: .object([:]),
            payloadKeypath: "identityBinding.rejectionPayload"
        )
        rejectIdentityBinding.modifiers = secondaryButtonModifiers()
        rejectIdentityBinding.modifiers?.visibility = SkeletonVisibilityRule(when: SkeletonCondition(
            scope: .item,
            keypath: "identityBinding.canReject",
            equals: .bool(true)
        ))
        var revokeCollaborationGrant = SkeletonButton(
            keypath: "chatHub.collaboration.revokeGrant",
            label: "Trekk tilgang",
            payload: .object([:]),
            payloadKeypath: "identityBinding.revocationPayload"
        )
        revokeCollaborationGrant.modifiers = secondaryButtonModifiers()
        revokeCollaborationGrant.modifiers?.visibility = SkeletonVisibilityRule(when: SkeletonCondition(
            scope: .item,
            keypath: "identityBinding.canRevoke",
            equals: .bool(true)
        ))

        let collaborationInvites = SkeletonList(
            topic: nil,
            keypath: "chatHub.state.collaborationInvites",
            flowElementSkeleton: row([
                keyText("title"),
                keyText("purposeText"),
                valueRow("Status", "statusSummary"),
                keyText("responseSummary"),
                valueRow("HAVEN-identitet", "identityBindingSummary"),
                hstack([
                    .Button(approveIdentityBinding),
                    .Button(rejectIdentityBinding),
                    .Button(revokeCollaborationGrant)
                ])
            ])
        )

        let invite = section(
            "Inviter",
            [
                subtleText("Få et konkret bidrag først. Bekjente uten HAVEN kan lese bare dette formålet og svare uten konto; chat- og prosjekttilgang krever fortsatt egen godkjenning."),
                keyText("chatHub.state.assistant.latestSuggestion.explanation"),
                .TextField(SkeletonTextField(
                    sourceKeypath: "chatHub.state.assistant.candidateQuery",
                    targetKeypath: "chatHub.assistant.setCandidateQuery",
                    placeholder: "Søk etter person eller alias"
                )),
                .List(candidates),
                .TextField(SkeletonTextField(
                    sourceKeypath: "chatHub.state.inviteDraft.profileID",
                    targetKeypath: "chatHub.inviteDraft.profileID",
                    placeholder: "Profil-ID hvis du kjenner den"
                )),
                .TextField(SkeletonTextField(
                    sourceKeypath: "chatHub.state.inviteDraft.title",
                    targetKeypath: "chatHub.inviteDraft.title",
                    placeholder: "Kort tittel på samarbeidet"
                )),
                .TextArea(SkeletonTextArea(
                    sourceKeypath: "chatHub.state.inviteDraft.purposeText",
                    targetKeypath: "chatHub.inviteDraft.purposeText",
                    placeholder: "Hva vil dere få til sammen? Vær konkret.",
                    minLines: 2,
                    maxLines: 5,
                    submitOnEnter: false,
                    editorMode: .plain
                )),
                .TextArea(SkeletonTextArea(
                    sourceKeypath: "chatHub.state.inviteDraft.contextText",
                    targetKeypath: "chatHub.inviteDraft.contextText",
                    placeholder: "Hva trenger mottakeren å vite for å kunne bidra?",
                    minLines: 2,
                    maxLines: 6,
                    submitOnEnter: false,
                    editorMode: .plain
                )),
                keyText("chatHub.state.drop.summary"),
                keyText("chatHub.state.inviteDraft.deliverySummary"),
                hstack([
                    button("chatHub.invite", "Send i HAVEN", payload: .object([:]), style: .primary),
                    button("chatHub.collaboration.prepareExternal", "Del med en bekjent", payload: .object([:]), style: .secondary),
                    button(
                        "chatHub.ui.openMatchedResourceLibrary",
                        "Last inn Entity Studio",
                        payload: .object([
                            "configurationName": .string("Entity Studio"),
                            "sourceCellEndpoint": .string("cell:///EntityStudio"),
                            "autoOpen": .bool(true)
                        ])
                    )
                ]),
                valueRow("Eksterne invitasjoner", "chatHub.state.collaborationInviteCount"),
                valueRow("Mottatte bidrag", "chatHub.state.collaborationResponseCount"),
                keyText("chatHub.state.collaborationPrivacySummary"),
                .List(collaborationInvites),
                button("chatHub.collaboration.revoke", "Trekk tilbake siste lenke", payload: .object([:]))
            ],
            modifiers: chatInviteDropModifiers()
        )

        let poll = section(
            "Avstemning",
            [
                valueRow("Krav", "chatHub.state.assistant.pollPrerequisite"),
                .TextField(SkeletonTextField(
                    sourceKeypath: "chatHub.state.pollDraft.question",
                    targetKeypath: "chatHub.poll.setQuestion",
                    placeholder: "Spørsmål"
                )),
                .TextArea(SkeletonTextArea(
                    sourceKeypath: "chatHub.state.pollDraft.optionsText",
                    targetKeypath: "chatHub.poll.setOptions",
                    placeholder: "Alternativer, ett per linje",
                    minLines: 2,
                    maxLines: 6,
                    submitOnEnter: false,
                    editorMode: .plain
                )),
                hstack([
                    button("chatHub.poll.create", "Publiser avstemning", payload: .object([:]), style: .primary),
                    button("chatHub.poll.vote", "Stem første", payload: .object(["optionID": .string("option-1")])),
                    button("chatHub.poll.close", "Lukk avstemning", payload: .object([:]))
                ])
            ]
        )

        let ideaCapture = section(
            "Idé",
            [
                .TextArea(SkeletonTextArea(
                    sourceKeypath: "chatHub.state.workbench.ideaDraft.content",
                    targetKeypath: "chatHub.idea.content",
                    placeholder: "Hva tenker du på?",
                    minLines: 4,
                    maxLines: 8,
                    submitOnEnter: false,
                    editorMode: .plain
                )),
                .TextField(SkeletonTextField(
                    sourceKeypath: "chatHub.state.workbench.ideaDraft.title",
                    targetKeypath: "chatHub.idea.title",
                    placeholder: "Tittel (valgfritt)"
                )),
                hstack([
                    button("chatHub.idea.capture", "Lagre idé", payload: .object([:]), style: .primary),
                    button(
                        "chatHub.ui.openMatchedResourceLibrary",
                        "Last inn idéflate",
                        payload: .object([
                            "configurationName": .string("Idea Task Workspace"),
                            "sourceCellEndpoint": .string("cell:///IdeaTaskWorkspace"),
                            "autoOpen": .bool(true)
                        ])
                    ),
                    button("chatHub.ui.minimizeComponentSurface", "−", payload: .object([:]))
                ])
            ],
            modifiers: motionSurfaceModifiers(role: "component-surface", hint: .expand, sourceRole: "suggestion-card")
        )

        let workItem = section(
            "Feil / work item",
            [
                .TextField(SkeletonTextField(
                    sourceKeypath: "chatHub.state.workbench.workItemDraft.title",
                    targetKeypath: "chatHub.workItem.title",
                    placeholder: "Kort tittel"
                )),
                .TextArea(SkeletonTextArea(
                    sourceKeypath: "chatHub.state.workbench.workItemDraft.summary",
                    targetKeypath: "chatHub.workItem.summary",
                    placeholder: "Hva skjer, hvor skjer det, og hvorfor betyr det noe?",
                    minLines: 3,
                    maxLines: 8,
                    submitOnEnter: false,
                    editorMode: .plain
                )),
                .TextField(SkeletonTextField(
                    sourceKeypath: "chatHub.state.workbench.workItemDraft.kind",
                    targetKeypath: "chatHub.workItem.kind",
                    placeholder: "bug, feature, docs, chore ..."
                )),
                hstack([
                    .TextField(SkeletonTextField(
                        sourceKeypath: "chatHub.state.workbench.workItemDraft.project",
                        targetKeypath: "chatHub.workItem.project",
                        placeholder: "Prosjekt"
                    )),
                    .TextField(SkeletonTextField(
                        sourceKeypath: "chatHub.state.workbench.workItemDraft.repo",
                        targetKeypath: "chatHub.workItem.repo",
                        placeholder: "Repo"
                    ))
                ]),
                hstack([
                    .TextField(SkeletonTextField(
                        sourceKeypath: "chatHub.state.workbench.workItemDraft.cell",
                        targetKeypath: "chatHub.workItem.cell",
                        placeholder: "Cell / komponent"
                    )),
                    .TextField(SkeletonTextField(
                        sourceKeypath: "chatHub.state.workbench.workItemDraft.surface",
                        targetKeypath: "chatHub.workItem.surface",
                        placeholder: "Flate"
                    ))
                ]),
                hstack([
                    .TextField(SkeletonTextField(
                        sourceKeypath: "chatHub.state.workbench.workItemDraft.severity",
                        targetKeypath: "chatHub.workItem.severity",
                        placeholder: "Severity"
                    )),
                    .TextField(SkeletonTextField(
                        sourceKeypath: "chatHub.state.workbench.workItemDraft.priority",
                        targetKeypath: "chatHub.workItem.priority",
                        placeholder: "Priority"
                    ))
                ]),
                .TextArea(SkeletonTextArea(
                    sourceKeypath: "chatHub.state.workbench.workItemDraft.currentBehavior",
                    targetKeypath: "chatHub.workItem.currentBehavior",
                    placeholder: "Observerte symptomer / repro",
                    minLines: 2,
                    maxLines: 6,
                    submitOnEnter: false,
                    editorMode: .plain
                )),
                .TextArea(SkeletonTextArea(
                    sourceKeypath: "chatHub.state.workbench.workItemDraft.expectedBehavior",
                    targetKeypath: "chatHub.workItem.expectedBehavior",
                    placeholder: "Forventet oppførsel",
                    minLines: 2,
                    maxLines: 5,
                    submitOnEnter: false,
                    editorMode: .plain
                )),
                hstack([
                    button("chatHub.ui.openComponentSurface", "Åpne feilflate", payload: .object(["kind": .string("work-item")])),
                    button("chatHub.workItem.capture", "Registrer feil", payload: .object([:]), style: .primary),
                    button("chatHub.ui.minimizeComponentSurface", "−", payload: .object([:]))
                ])
            ],
            modifiers: motionSurfaceModifiers(role: "component-surface", hint: .expand, sourceRole: "assistant-response-bubble")
        )

        let todo = section(
            "Oppgave",
            [
                .TextField(SkeletonTextField(
                    sourceKeypath: "chatHub.state.workbench.todoDraft.title",
                    targetKeypath: "chatHub.todo.title",
                    placeholder: "Hva skal gjøres?"
                )),
                .TextField(SkeletonTextField(
                    sourceKeypath: "chatHub.state.workbench.todoDraft.dueAtText",
                    targetKeypath: "chatHub.todo.dueAtText",
                    placeholder: "Frist (valgfritt)"
                )),
                .TextArea(SkeletonTextArea(
                    sourceKeypath: "chatHub.state.workbench.todoDraft.note",
                    targetKeypath: "chatHub.todo.note",
                    placeholder: "Detaljer (valgfritt)",
                    minLines: 2,
                    maxLines: 5,
                    submitOnEnter: false,
                    editorMode: .plain
                )),
                hstack([
                    button("chatHub.todo.create", "Legg til oppgave", payload: .object([:]), style: .primary),
                    button(
                        "chatHub.ui.openMatchedResourceLibrary",
                        "Last inn oppgaveliste",
                        payload: .object([
                            "configurationName": .string("Personlig Todo"),
                            "sourceCellEndpoint": .string("cell:///Todo"),
                            "autoOpen": .bool(true)
                        ])
                    )
                ])
            ]
        )

        let project = section(
            "Prosjekt / idé",
            [
                .TextField(SkeletonTextField(
                    sourceKeypath: "chatHub.state.workbench.projectDraft.title",
                    targetKeypath: "chatHub.project.title",
                    placeholder: "Tittel"
                )),
                .TextArea(SkeletonTextArea(
                    sourceKeypath: "chatHub.state.workbench.projectDraft.description",
                    targetKeypath: "chatHub.project.description",
                    placeholder: "Hva skal vi lage?",
                    minLines: 3,
                    maxLines: 7,
                    submitOnEnter: false,
                    editorMode: .plain
                )),
                .TextField(SkeletonTextField(
                    sourceKeypath: "chatHub.state.workbench.projectDraft.membersText",
                    targetKeypath: "chatHub.project.membersText",
                    placeholder: "Medlemmer, ett navn per linje"
                )),
                button("chatHub.project.create", "Opprett idé", payload: .object([:]), style: .primary)
            ]
        )

        let reminder = section(
            "Påminnelse",
            [
                .TextField(SkeletonTextField(
                    sourceKeypath: "chatHub.state.workbench.reminderDraft.title",
                    targetKeypath: "chatHub.reminder.title",
                    placeholder: "Hva skal huskes?"
                )),
                .TextField(SkeletonTextField(
                    sourceKeypath: "chatHub.state.workbench.reminderDraft.scheduledAtText",
                    targetKeypath: "chatHub.reminder.scheduledAtText",
                    placeholder: "Tidspunkt"
                )),
                .TextField(SkeletonTextField(
                    sourceKeypath: "chatHub.state.workbench.reminderDraft.scope",
                    targetKeypath: "chatHub.reminder.scope",
                    placeholder: "me eller thread"
                )),
                button("chatHub.reminder.create", "Lagre påminnelse", payload: .object([:]), style: .primary)
            ]
        )

        let meeting = section(
            "Møte / video",
            [
                .TextField(SkeletonTextField(
                    sourceKeypath: "chatHub.state.workbench.meetingDraft.title",
                    targetKeypath: "chatHub.meeting.title",
                    placeholder: "Møtetittel"
                )),
                .TextField(SkeletonTextField(
                    sourceKeypath: "chatHub.state.workbench.meetingDraft.targetProfileID",
                    targetKeypath: "chatHub.meeting.targetProfileID",
                    placeholder: "Profil-ID (valgfritt)"
                )),
                .TextField(SkeletonTextField(
                    sourceKeypath: "chatHub.state.workbench.meetingDraft.proposedTimesText",
                    targetKeypath: "chatHub.meeting.proposedTimesText",
                    placeholder: "Tider, kommaseparert"
                )),
                button("chatHub.meeting.schedule", "Foreslå møte", payload: .object([:]), style: .primary)
            ]
        )

        let onboardingMissingFields = SkeletonList(
            topic: nil,
            keypath: "chatHub.state.onboarding.missingFields",
            flowElementSkeleton: row([
                keyText("title"),
                keyText("prompt"),
                valueRow("Påkrevd", "required")
            ])
        )

        let onboardingCurrentStepOptions = SkeletonList(
            topic: nil,
            keypath: "chatHub.state.onboarding.currentStep.options",
            flowElementSkeleton: row([
                button(
                    "chatHub.onboarding.answer",
                    "",
                    payload: nil,
                    labelKeypath: "label",
                    payloadKeypath: "selectPayload"
                )
            ])
        )

        // Onboarding-panelet er tilstandsstyrt. Foer ble alle sju start-knappene,
        // Lagre/Hopp over/Fullfoer og fem tomme oppsummeringsrader vist samtidig
        // uansett hvor brukeren var i loepet — en vegg med 13 knapper etter at
        // brukeren hadde bedt om EN ting. Naa styrer chatHub.state.onboarding.status
        // hva som vises: velg loep foer start, ett steg om gangen underveis, og
        // en avslutning naar alt paakrevd er fylt. Feil fra cella (utilgjengelig
        // runtime) vises som tekst i stedet for aa forsvinne stille.
        let onboardingStatusKeypath = "chatHub.state.onboarding.status"
        let onboardingHiddenChooserStatuses: [ValueType] = [.string("active"), .string("complete_ready"), .string("unavailable")]

        let whenChoosing = SkeletonCondition(not: SkeletonCondition(scope: .root, keypath: onboardingStatusKeypath, inValues: onboardingHiddenChooserStatuses))
        let whenActive = SkeletonCondition(scope: .root, keypath: onboardingStatusKeypath, equals: .string("active"))
        let whenCompleteReady = SkeletonCondition(scope: .root, keypath: onboardingStatusKeypath, equals: .string("complete_ready"))
        let whenUnavailable = SkeletonCondition(scope: .root, keypath: onboardingStatusKeypath, equals: .string("unavailable"))
        // Forslaget hoerer ikke hjemme inne i den aktive gruppen: cella setter
        // status til "complete_ready" i samme svar som lager det siste
        // dry_run-forslaget, saa et forslag nestet under "active" ville vises og
        // forsvinne i samme oeyeblikk — med et ulagret svar igjen.
        //
        // Betingelsen kan derimot ikke vaere «det finnes et ubekreftet forslag».
        // GuidedOnboardingCell svarer `status: "dry_run_ready"` i selve
        // handlingssvaret, mens tilstandsprojeksjonen som mater
        // chatHub.state.onboarding bare kjenner session.status ("active",
        // "complete_ready", "cancelled", "completed") — og lastDryRun er ikke
        // paalitelig satt der naar synligheten evalueres. Maalt 09.09: smoken
        // passerte toContainText("Forslag før lagring") (som leser textContent og
        // ikke krever synlighet) og feilet paa toBeVisible for «Lagre dette
        // steget» — gruppen var rendret, men skjult.
        //
        // Forsoek to bandt gruppen til status i {active, complete_ready}. Det
        // flyttet feilen ett steg fram — foerste bekreftelse virket, den andre
        // ikke (spec-linje 203 -> 220) — saa status holder seg ikke i det settet
        // gjennom loepet slik antatt. Regelen er derfor gitt opp: radene og
        // «Lagre dette steget» staar ubetinget, som foer denne endringen.
        // AAPENT: skal knappen skjules naar det ikke finnes et ubekreftet
        // forslag, maa GuidedOnboardingCell projisere et felt for det. Cella
        // svarer "dry_run_ready" bare i handlingssvaret, ikke i tilstanden.
        // Det er en celleendring, ikke en skjelettendring.

        let onboardingUnavailable = visibleGroup([
            text("Onboarding er ikke tilgjengelig akkurat nå."),
            keyText("chatHub.state.onboarding.summary")
        ], when: whenUnavailable)

        let onboardingChooser = visibleGroup([
            text("Hva vil du sette opp?"),
            hstack([
                button("chatHub.onboarding.start", "Start Arendalsuka-onboarding", payload: .object(["scriptID": .string("arendalsuka-participant-v1")]), style: .primary),
                button("chatHub.onboarding.start", "Start konferanse-onboarding", payload: .object(["scriptID": .string("conference-participant-v1")]), style: .secondary)
            ]),
            subtleText("Oppsett og hjelp"),
            hstack([
                button("chatHub.onboarding.start", "Bli kjent med HAVEN", payload: .object(["scriptID": .string("haven-foundation-v1")])),
                button("chatHub.onboarding.start", "Tilpass Co-Pilot", payload: .object(["scriptID": .string("personal-copilot-foundation-v1")])),
                button("chatHub.onboarding.start", "Hjelp med Co-Pilot", payload: .object(["scriptID": .string("personal-copilot-foundation-v1"), "mode": .string("help")])),
                button("chatHub.onboarding.start", "Start AIGateway-oppsett", payload: .object(["scriptID": .string("ai-gateway-provider-setup-v1")])),
                button("chatHub.onboarding.start", "Start spørreskjema", payload: .object(["scriptID": .string("user-research-questionnaire-v1")]))
            ])
        ], when: whenChoosing)

        let onboardingDryRun = visibleGroup([
            text("Forslag før lagring"),
            valueRow("Hva jeg forstod", "chatHub.state.onboarding.lastDryRun.understoodSummary"),
            valueRow("Hvor lagres", "chatHub.state.onboarding.lastDryRun.storageSummary"),
            valueRow("Hvem kan lese", "chatHub.state.onboarding.lastDryRun.readerSummary"),
            valueRow("Hva skjer ikke ennå", "chatHub.state.onboarding.lastDryRun.notYetSummary"),
            button("chatHub.onboarding.confirmStep", "Lagre dette steget", payload: .object([:]), style: .primary)
        ])

        let onboardingActive = visibleGroup([
            hstack([
                subtleText("Fullført"),
                keyText("chatHub.state.onboarding.progress.completedRequired"),
                subtleText("av"),
                keyText("chatHub.state.onboarding.progress.totalRequired")
            ]),
            styledKeyText("chatHub.state.onboarding.currentStep.title", role: "onboarding-step-title"),
            keyText("chatHub.state.onboarding.currentStep.prompt"),
            .TextArea(SkeletonTextArea(
                sourceKeypath: "chatHub.state.onboarding.answerDraft",
                targetKeypath: "chatHub.onboarding.answer",
                placeholder: "Svar naturlig her. Co-piloten lager et lagringsforslag før noe skrives.",
                minLines: 3,
                maxLines: 6,
                submitOnEnter: false,
                editorMode: .plain
            )),
            .List(onboardingCurrentStepOptions),
            hstack([
                button("chatHub.onboarding.skipStep", "Hopp over", payload: .object([:])),
                button("chatHub.onboarding.cancel", "Avbryt", payload: .object([:]))
            ]),
            subtleText("Mangler som fortsatt må fylles:"),
            .List(onboardingMissingFields)
        ], when: whenActive)

        let onboardingComplete = visibleGroup([
            text("Alt som trengs er fylt ut."),
            hstack([
                button("chatHub.onboarding.complete", "Fullfør", payload: .object([:]), style: .primary),
                button("chatHub.onboarding.cancel", "Avbryt", payload: .object([:]))
            ])
        ], when: whenCompleteReady)

        let onboarding = section(
            "Onboarding",
            [
                onboardingUnavailable,
                onboardingChooser,
                onboardingActive,
                onboardingDryRun,
                onboardingComplete,
                hstack([
                    button("chatHub.ui.minimizeComponentSurface", "−", payload: .object([:]))
                ])
            ],
            modifiers: motionSurfaceModifiers(role: "component-surface", hint: .expand, sourceRole: "assistant-response-bubble")
        )

        let agentReview = section(
            "Agent-review",
            [
                .TextField(SkeletonTextField(
                    sourceKeypath: "chatHub.state.workbench.agentReviewDraft.actionID",
                    targetKeypath: "chatHub.agent.review.actionID",
                    placeholder: "Action ID"
                )),
                .TextArea(SkeletonTextArea(
                    sourceKeypath: "chatHub.state.workbench.agentReviewDraft.reason",
                    targetKeypath: "chatHub.agent.review.reason",
                    placeholder: "Hvorfor skal agenten foreslås?",
                    minLines: 2,
                    maxLines: 5,
                    submitOnEnter: false,
                    editorMode: .plain
                )),
                .TextArea(SkeletonTextArea(
                    sourceKeypath: "chatHub.state.workbench.agentReviewDraft.argumentsText",
                    targetKeypath: "chatHub.agent.review.argumentsText",
                    placeholder: "Argumenter som JSON",
                    minLines: 2,
                    maxLines: 5,
                    submitOnEnter: false,
                    editorMode: .plain
                )),
                .TextField(SkeletonTextField(
                    sourceKeypath: "chatHub.state.workbench.agentReviewDraft.signatureBase64",
                    targetKeypath: "chatHub.agent.review.signatureBase64",
                    placeholder: "Signatur fra lokal issuer"
                )),
                hstack([
                    button("chatHub.agent.review.create", "Lag review", payload: .object([:]), style: .primary),
                    button("chatHub.agent.review.execute", "Send til lokal review", payload: .object([:]))
                ])
            ]
        )

        let compactAgentReview = section(
            "Agent-review",
            [
                valueRow("Forslag", "chatHub.state.workbench.agentReviewDraft.actionID"),
                valueRow("Hvorfor", "chatHub.state.workbench.agentReviewDraft.reason"),
                hstack([
                    button("chatHub.ui.setActiveTab", "Åpne verktøy", payload: .object(["activeTab": .string("mer")])),
                    button("chatHub.ui.minimizeComponentSurface", "−", payload: .object([:]))
                ])
            ]
        )

        let advisorReport = section(
            "Rådgiver-rapport",
            [
                .TextField(SkeletonTextField(
                    sourceKeypath: "chatHub.state.workbench.advisorReportDraft.subject",
                    targetKeypath: "chatHub.advisorReport.subject",
                    placeholder: "Hva skal vurderes?"
                )),
                .TextArea(SkeletonTextArea(
                    sourceKeypath: "chatHub.state.workbench.advisorReportDraft.markdown",
                    targetKeypath: "chatHub.advisorReport.markdown",
                    placeholder: "# Rapport\n\nSkriv eller rediger markdown her.",
                    minLines: 8,
                    maxLines: 18,
                    submitOnEnter: false,
                    editorMode: .plain
                )),
                styledKeyText("chatHub.state.workbench.advisorReportDraft.markdown", role: "markdown"),
                valueRow("Eksport", "chatHub.state.workbench.advisorReportDraft.exportStatus"),
                hstack([
                    button("chatHub.advisorReport.prepare", "Oppdater rapport", payload: .object([:]), style: .primary),
                    button("chatHub.advisorReport.exportMarkdown", "Eksporter MD", payload: .object([:])),
                    button("chatHub.advisorReport.exportPDF", "Eksporter PDF", payload: .object([:])),
                    button("chatHub.ui.minimizeComponentSurface", "−", payload: .object([:])),
                    button("chatHub.ui.dismissComponentSurface", "×", payload: .object([:]), style: .secondary)
                ])
            ],
            modifiers: motionSurfaceModifiers(role: "component-surface", hint: .expand, sourceRole: "assistant-response-bubble")
        )

        let capabilityRequest = section(
            "Meld behov",
            [
                valueRow("Behovsradar", "chatHub.state.ui.capabilityDiscoveryEnabled"),
                .TextField(SkeletonTextField(
                    sourceKeypath: "chatHub.state.workbench.capabilityRequestDraft.title",
                    targetKeypath: "chatHub.capabilityRequest.title",
                    placeholder: "Kort tittel"
                )),
                .TextArea(SkeletonTextArea(
                    sourceKeypath: "chatHub.state.workbench.capabilityRequestDraft.summary",
                    targetKeypath: "chatHub.capabilityRequest.summary",
                    placeholder: "Hva prøvde du å få til?",
                    minLines: 3,
                    maxLines: 7,
                    submitOnEnter: false,
                    editorMode: .plain
                )),
                .TextField(SkeletonTextField(
                    sourceKeypath: "chatHub.state.workbench.capabilityRequestDraft.destination",
                    targetKeypath: "chatHub.capabilityRequest.destination",
                    placeholder: "kjetil, digipomps eller dimy"
                )),
                .TextField(SkeletonTextField(
                    sourceKeypath: "chatHub.state.workbench.capabilityRequestDraft.category",
                    targetKeypath: "chatHub.capabilityRequest.category",
                    placeholder: "cellprotocol, scaffold, dimy-commercial ..."
                )),
                hstack([
                    button("chatHub.ui.openComponentSurface", "Åpne behovsflate", payload: .object(["kind": .string("capability-request")])),
                    button("chatHub.capabilityRequest.submit", "Send behov", payload: .object([:]), style: .primary),
                    button("chatHub.ui.minimizeComponentSurface", "−", payload: .object([:]))
                ])
            ],
            modifiers: motionSurfaceModifiers(role: "component-surface", hint: .expand, sourceRole: "suggestion-card")
        )

        let resourceRouter = section(
            "Finn verktøy",
            [
                valueRow("Beste treff", "chatHub.state.assistant.latestSuggestion.targetPhrase"),
                .List(resourceMatches),
                hstack([
                    button("chatHub.ui.openMatchedResourceLibrary", "Last inn beste treff", payload: .object(["autoOpen": .bool(true)]), style: .secondary),
                    button("chatHub.ui.openMatchedResourceLibrary", "Velg selv i Library", payload: .object(["autoOpen": .bool(false)])),
                    button("chatHub.entityExtension.scan", "Skann tilgang", payload: .object([:])),
                    button("chatHub.ui.minimizeComponentSurface", "−", payload: .object([:]))
                ])
            ],
            modifiers: motionSurfaceModifiers(role: "component-surface", hint: .expand, sourceRole: "suggestion-card")
        )

        let compactResourceRouter = section(
            "Finn verktøy",
            [
                valueRow("Beste treff", "chatHub.state.assistant.latestSuggestion.targetPhrase"),
                .List(resourceMatches),
                hstack([
                    button("chatHub.ui.openMatchedResourceLibrary", "Last inn beste treff", payload: .object(["autoOpen": .bool(true)]), style: .secondary),
                    button("chatHub.ui.openMatchedResourceLibrary", "Velg selv", payload: .object(["autoOpen": .bool(false)])),
                    button("chatHub.ui.minimizeComponentSurface", "−", payload: .object([:]))
                ])
            ],
            modifiers: motionSurfaceModifiers(role: "component-surface", hint: .expand, sourceRole: "suggestion-card")
        )

        var docsRAGDocumentationMatchesVisible = docsRAGDocumentationMatches
        docsRAGDocumentationMatchesVisible.modifiers = visibleWhenBool("chatHub.state.docsRAG.canOpenDocument")
        var docsRAGRAGMatchesVisible = docsRAGRAGMatches
        docsRAGRAGMatchesVisible.modifiers = visibleWhenBool("chatHub.state.docsRAG.canAskRAG")

        let docsRAG = section(
            "Spør docs/RAG",
            [
                .TextArea(SkeletonTextArea(
                    sourceKeypath: "chatHub.state.docsRAG.query",
                    targetKeypath: "chatHub.docsRAG.setQuery",
                    placeholder: "Spør om dokumentasjon, arkitektur, skeleton, formål/interesser eller et RAG-case",
                    minLines: 3,
                    maxLines: 7,
                    submitOnEnter: false,
                    editorMode: .plain
                )),
                hstack([
                    button("chatHub.docsRAG.search", "Finn kilder", payload: .object([:]), style: .primary),
                    visibleButton("chatHub.docsRAG.openTopDocument", "Åpne dokument", payload: .object([:]), visibleWhen: "chatHub.state.docsRAG.canOpenDocument"),
                    visibleButton("chatHub.docsRAG.askRAG", "Spør RAG", payload: .object([:]), visibleWhen: "chatHub.state.docsRAG.canAskRAG"),
                    button("chatHub.ui.minimizeComponentSurface", "−", payload: .object([:])),
                    button("chatHub.ui.dismissComponentSurface", "×", payload: .object([:]), style: .secondary)
                ]),
                .List(docsRAGDocumentationMatchesVisible),
                .List(docsRAGRAGMatchesVisible),
                visibleKeyText("chatHub.state.docsRAG.answer")
            ],
            modifiers: motionSurfaceModifiers(role: "component-surface", hint: .expand, sourceRole: "assistant-response-bubble")
        )

        let agreementHelper = section(
            "Avtalehjelper",
            AgreementWorkbenchConfigurationFactory.compactHelperElements(includeWorkbenchNavigationButtons: false) + [
                button(
                    "chatHub.ui.openMatchedResourceLibrary",
                    "Åpne full avtale-flate",
                    payload: .object([
                        "configurationName": .string("Agreement Workbench"),
                        "autoOpen": .bool(true)
                    ]),
                    style: .secondary
                ),
                hstack([
                    button("chatHub.ui.minimizeComponentSurface", "−", payload: .object([:])),
                    button("chatHub.ui.dismissComponentSurface", "×", payload: .object([:]), style: .secondary)
                ])
            ],
            modifiers: motionSurfaceModifiers(role: "component-surface", hint: .expand, sourceRole: "assistant-response-bubble")
        )

        let spatialQueryPayload: ValueType = .object([
            "purpose": .string("personal.chat.assist.spatial-query"),
            "interestRefs": .list([.string("nearby"), .string("spatial-discovery")])
        ])

        let spatialMap = section(
            "Kart",
            [
                .Visualization(SkeletonVisualization(
                    kind: "map",
                    keypath: "spatial.state.map",
                    stateKeypath: "spatial.state.selection",
                    actionKeypath: "spatial.spatial.selectFeature"
                )),
                valueRow("Valgt", "spatial.state.selection.label"),
                hstack([
                    button("spatial.spatial.queryAround", "Hent rundt meg", payload: spatialQueryPayload, style: .primary),
                    button("spatial.spatial.explainFeature", "Forklar valgt", payload: spatialQueryPayload),
                    button("spatial.spatial.draftArtifact", "Lag utkast", payload: spatialQueryPayload),
                    button("spatial.spatial.requestPresence", "Forbered presence", payload: spatialQueryPayload),
                    button("spatial.spatial.revokePresence", "Trekk presence", payload: .object([:]))
                ])
            ],
            modifiers: motionSurfaceModifiers(role: "component-surface", hint: .expand, sourceRole: "suggestion-card")
        )

        func helperTabs(compact: Bool = false, activeOnly: Bool = false) -> SkeletonTabs {
            var modifiers = SkeletonModifiers()
            modifiers.styleClasses = compact
                ? ["chat-helper-tabs", "chat-helper-tabs-compact"]
                : ["chat-helper-tabs"]
            return SkeletonTabs(
                tabsKeypath: activeOnly ? "chatHub.state.ui.activeHelpers" : "chatHub.state.ui.helpers",
                activeTabStateKeypath: "chatHub.state.ui.activeHelper",
                selectionActionKeypath: "chatHub.ui.setActiveHelper",
                idKeypath: "id",
                labelKeypath: "title",
                panels: [
                    SkeletonTabPanel(id: "invite", content: [invite]),
                    SkeletonTabPanel(id: "poll", content: [poll]),
                    SkeletonTabPanel(id: "resource-router", content: [compact ? compactResourceRouter : resourceRouter]),
                    SkeletonTabPanel(id: "docs-rag", content: [docsRAG]),
                    SkeletonTabPanel(id: "agreement", content: [agreementHelper]),
                    SkeletonTabPanel(id: "spatial-map", content: [spatialMap]),
                    SkeletonTabPanel(id: "idea-capture", content: [ideaCapture]),
                    SkeletonTabPanel(id: "work-item", content: [workItem]),
                    SkeletonTabPanel(id: "todo", content: [todo]),
                    SkeletonTabPanel(id: "project", content: [project]),
                    SkeletonTabPanel(id: "reminder", content: [reminder]),
                    SkeletonTabPanel(id: "meeting", content: [meeting]),
                    SkeletonTabPanel(id: "onboarding", content: [onboarding]),
                    SkeletonTabPanel(id: "agent-review", content: [compact ? compactAgentReview : agentReview]),
                    SkeletonTabPanel(id: "advisor-report", content: [advisorReport]),
                    SkeletonTabPanel(id: "capability-request", content: [capabilityRequest])
                ],
                modifiers: modifiers
            )
        }

        let toolsPanel = stack([
            .Tabs(helperTabs())
        ])

        let moderationPanel = stack([
            section(
                "Moderering",
                [
                    .List(threads),
                    hstack([
                        button("chatHub.reportMessage", "Rapporter siste", payload: .object(["reason": .string("user_reported_from_chat")])),
                        button("chatHub.blockUser", "Blokker deltaker", payload: .object([:])),
                        button("chatHub.unblockUser", "Opphev blokk", payload: .object([:]))
                    ]),
                    valueRow("Blokkerte", "chatHub.state.blockedUsers")
                ],
                footer: "Rapportering og blokkering overstyrer alltid assistentforslag."
            )
        ])

        let privacyPanel = stack([
            section(
                "Personvern",
                [
                    text("Co-piloten leser kun utkastet ditt når du ber om forslag."),
                    text("RAG spørres bare når du klikker."),
                    text("Agenten kjører ingenting før lokal review."),
                    text("Forslagslæring er av som standard. Hvis du slår den på, lagres bare bekreftede formål/interesser og om forslaget lyktes – ikke meldingsteksten."),
                    .List(promptParticipants),
                    valueRow("Forslagslæring", "chatHub.state.ui.learningStatus"),
                    valueRow("Behovsradar", "chatHub.state.ui.capabilityDiscoveryStatus"),
                    hstack([
                        button("chatHub.ui.setLearningEnabled", "Stopp forslagslæring", payload: .bool(false)),
                        button("chatHub.ui.setLearningEnabled", "Tillat forslagslæring", payload: .bool(true)),
                        button("chatHub.ui.setCapabilityDiscoveryEnabled", "Skru på behovsradar", payload: .bool(true)),
                        button("chatHub.ui.setCapabilityDiscoveryEnabled", "Skru av behovsradar", payload: .bool(false)),
                        button("chatHub.ui.setShowAdvanced", "Vis avansert", payload: .bool(true))
                    ])
                ],
                footer: "Forslagslæring og behovsradar er per bruker og per tråd; de påvirker ikke andre brukere."
            )
        ])

        let advancedPanel = stack([
            section(
                "Avansert",
                [
                    valueRow("assistant.status", "chatHub.state.assistant.status"),
                    valueRow("latest.kind", "chatHub.state.assistant.latestSuggestion.kind"),
                    valueRow("confidence", "chatHub.state.assistant.latestSuggestion.confidence"),
                    valueRow("purposeRef", "chatHub.state.assistant.latestSuggestion.purposeRef"),
                    valueRow("executionScope", "chatHub.state.assistant.providerRecommendation.executionScope"),
                    valueRow("lastMotion", "chatHub.state.ui.lastMotionEvent.hint"),
                    valueRow("activeSurface", "chatHub.state.ui.activeComponentSurfaceID"),
                    valueRow("combinedChatView", "chatHub.state.ui.combinedChatView"),
                    valueRow("capabilityDiscovery", "chatHub.state.ui.capabilityDiscoveryEnabled"),
                    valueRow("signatureBase64", "chatHub.state.workbench.agentReviewDraft.signatureBase64"),
                    valueRow("invite.userUUID", "chatHub.state.inviteDraft.userUUID"),
                    valueRow("invite.contactEndpoint", "chatHub.state.inviteDraft.contactEndpoint.endpointID"),
                    valueRow("drop.validationState", "chatHub.state.drop.validationState"),
                    keyText("chatHub.state.assistant.whySummary"),
                    .List(advancedComponentSurfaces),
                    .List(intentCandidates),
                    .List(resourceMatches),
                    .List(providerMatches)
                ],
                footer: "Tekniske felt vises bare her, slik at Samtale forblir brukerflate."
            )
        ])

        let more = stack([
            section(
                "Tilbake",
                [
                    button("chatHub.ui.setActiveTab", "Til samtale", payload: .object(["activeTab": .string("samtale")]), style: .primary)
                ]
            ),
            section(
                "Rydd",
                [
                    hstack([
                        button("chatHub.ui.clearPromptHistory", "Rydd historikk", payload: .object([:]), style: .secondary),
                        button("chatHub.ui.clearComponentSurfaces", "Rydd hjelpere", payload: .object([:]), style: .secondary)
                    ])
                ]
            ),
            .Tabs(SkeletonTabs(
                tabsKeypath: "chatHub.state.ui.moreTabs",
                activeTabStateKeypath: "chatHub.state.ui.activeMoreTab",
                selectionActionKeypath: "chatHub.ui.setActiveMoreTab",
                idKeypath: "id",
                labelKeypath: "title",
                panels: [
                    SkeletonTabPanel(id: "verktoy", content: [toolsPanel]),
                    SkeletonTabPanel(id: "ai", content: [aiPanel]),
                    SkeletonTabPanel(id: "tilgang", content: [accessPanel]),
                    SkeletonTabPanel(id: "moderering", content: [moderationPanel]),
                    SkeletonTabPanel(id: "personvern", content: [privacyPanel]),
                    SkeletonTabPanel(id: "avansert", content: [advancedPanel])
                ]
            ))
        ])

        let componentPanel = section(
            "Aktiv hjelper",
                [
                    keyText("chatHub.state.ui.activeHelperSummary"),
                    scrollView(
                        [.Tabs(helperTabs(compact: true, activeOnly: true))],
                        role: "component-panel-scroll"
                    ),
                    hstack([
                        button("chatHub.ui.minimizeComponentSurface", "−", payload: .object([:])),
                        button("chatHub.ui.restoreComponentSurface", "Hent", payload: .object([:])),
                        button("chatHub.ui.dismissComponentSurface", "×", payload: .object([:]), style: .secondary),
                        button("chatHub.ui.clearComponentSurfaces", "Rydd alle", payload: .object([:]))
                ])
            ],
            modifiers: activeComponentPanelModifiers()
        )

        let conversationWorkbench = widgetCanvasWorkbench(conversation: conversation, componentPanel: componentPanel)

        return .Tabs(SkeletonTabs(
            tabsKeypath: "chatHub.state.ui.tabs",
            activeTabStateKeypath: "chatHub.state.ui.activeTab",
            selectionActionKeypath: "chatHub.ui.setActiveTab",
            idKeypath: "id",
            labelKeypath: "title",
            panels: [
                SkeletonTabPanel(id: "samtale", content: [conversationWorkbench]),
                SkeletonTabPanel(id: "aktivt", content: [active]),
                SkeletonTabPanel(id: "mer", content: [more])
            ]
        ))
    }

    private static func personalAssistantProfileSkeleton() -> SkeletonElement {
        stack([
            section(
                "Din Co-Pilot",
                [
                    valueRow("Status", "assistantProfile.state.status"),
                    .TextField(SkeletonTextField(
                        sourceKeypath: "assistantProfile.state.displayName",
                        targetKeypath: "assistantProfile.profile.setDisplayName",
                        placeholder: "Navn på assistenten"
                    )),
                    .TextArea(SkeletonTextArea(
                        sourceKeypath: "assistantProfile.state.declaredPurpose",
                        targetKeypath: "assistantProfile.profile.setDeclaredPurpose",
                        placeholder: "Hva vil du at assistenten skal hjelpe deg med?",
                        minLines: 3,
                        maxLines: 8,
                        submitOnEnter: false,
                        editorMode: .plain
                    )),
                    .TextArea(SkeletonTextArea(
                        sourceKeypath: "assistantProfile.state.necessaryContent",
                        targetKeypath: "assistantProfile.profile.setNecessaryContent",
                        placeholder: "Hvilket innhold eller hvilke kilder trengs? Ikke legg inn hemmeligheter.",
                        minLines: 3,
                        maxLines: 8,
                        submitOnEnter: false,
                        editorMode: .plain
                    )),
                    .TextField(SkeletonTextField(
                        sourceKeypath: "assistantProfile.state.declaredInterestsText",
                        targetKeypath: "assistantProfile.profile.setDeclaredInterests",
                        placeholder: "Interesser, kommaseparert"
                    )),
                    valueRow("Samhandlingsstil", "assistantProfile.state.interactionStyle"),
                    valueRow("Læring fra adferd", "assistantProfile.state.behaviorLearning"),
                    valueRow("Læring fra formål", "assistantProfile.state.purposeLearning"),
                    valueRow("Providerpolicy", "assistantProfile.state.providerPolicy")
                ],
                footer: "Navn og stil gir ikke assistenten ny autoritet. Profilen sender ikke innhold til en modell."
            ),
            section(
                "Personvern og modeller",
                [
                    keyText("assistantProfile.state.privacySummary"),
                    keyText("assistantProfile.state.providerSummary"),
                    hstack([
                        button("assistantProfile.profile.setProviderPolicy", "Bare lokale modeller", payload: .string("localOnly"), style: .primary),
                        button("assistantProfile.profile.setProviderPolicy", "Spør før ekstern modell", payload: .string("askBeforeExternal")),
                        button(
                            "assistantProfile.profile.setLearningPolicy",
                            "Bruk bare eksplisitte formål",
                            payload: .object([
                                "behaviorLearning": .string("off"),
                                "purposeLearning": .string("explicitConfirmedOnly")
                            ])
                        )
                    ])
                ],
                footer: "Ekstern provider krever separat samtykke og tillitspakke; denne flaten aktiverer ingen provider."
            ),
            section(
                "Slett profilinnhold",
                [
                    button(
                        "assistantProfile.profile.reset",
                        "Tilbakestill Co-Pilot-profil",
                        payload: .object(["confirm": .bool(true)]),
                        style: .secondary
                    )
                ],
                footer: "Tilbakestilling gjenoppretter private standardvalg og fjerner formål, innhold, interesser og bekreftelser."
            )
        ])
    }

    private static func aiAssistantThreadSkeleton() -> SkeletonElement {
        var messages = SkeletonList(
            topic: nil,
            keypath: "aiAssistantThread.messages",
            flowElementSkeleton: row([
                keyText("author.displayName"),
                keyText("kind"),
                keyText("text")
            ])
        )
        var messageListModifiers = SkeletonModifiers()
        messageListModifiers.styleRole = "chat-message-list"
        messageListModifiers.styleClasses = ["chat-message-list"]
        messages.modifiers = messageListModifiers

        let localStartPayload: ValueType = .object([
            "text": .string("Start en lokal M5 HAVEN-undervisningsrunde der lokale lærerroller forklarer HAVEN til den lille Qwen-modellen."),
            "invokeAssistant": .bool(true),
            "assistantMode": .string("haven-local-teaching-swarm")
        ])
        let hostedStartPayload: ValueType = .object([
            "text": .string("Start en HAVEN-undervisningsrunde der ChatGPT og Claude lærer opp den lokale Qwen-modellen."),
            "invokeAssistant": .bool(true),
            "assistantMode": .string("haven-teaching-swarm")
        ])
        let borealisParallelPayload: ValueType = .object([
            "text": .string("Svar parallelt med tre lokale Borealis-perspektiver: kort svar, arkitektur og personvern/Agreement."),
            "invokeAssistant": .bool(true),
            "assistantMode": .string("parallel-local-borealis"),
            "maxParallelInvocations": .integer(3)
        ])

        return stack([
            section(
                "HAVEN Teaching Group Chat",
                [
                    valueRow("Status", "aiAssistantThread.runState.status"),
                    valueRow("Provider", "aiAssistantThread.runState.providerId"),
                    valueRow("Model", "aiAssistantThread.runState.model"),
                    valueRow("Meldinger", "aiAssistantThread.state.messageCount"),
                    hstack([
                        button("aiAssistantThread.postUserMessage", "Start lokal M5-runde", payload: localStartPayload, style: .primary),
                        button("aiAssistantThread.postUserMessage", "Start Borealis parallell", payload: borealisParallelPayload, style: .secondary),
                        button("aiAssistantThread.postUserMessage", "Start GPT/Claude-runde", payload: hostedStartPayload, style: .secondary),
                        button("aiAssistantThread.refresh", "Oppdater", payload: .object([:]), style: .secondary)
                    ])
                ],
                footer: "Lokal runde bruker M5-ruter uten API-nøkkel. Borealis parallell bruker én lokal backend med flere route-kontekster. GPT/Claude-runden bruker hosted teacher-ruter og lokal Qwen."
            ),
            section(
                "Diskusjon",
                [
                    scrollView([.List(messages)], role: "chat-prompt-scroll")
                ]
            ),
            section(
                "Oppsett",
                [
                    text("Lokal: LOCAL_LLM_BASE_URL, LOCAL_LLM_API_PATH og LOCAL_LLM_DEFAULT_MODEL."),
                    text("Borealis parallell: BOREALIS_BASE_URL/LOCAL_BOREALIS_BASE_URL peker som default til http://127.0.0.1:8082."),
                    text("Hosted: alias openai/anthropic eller OPENAI_API_KEY/ANTHROPIC_API_KEY.")
                ],
                footer: "AIAssistantThread viser hver vellykkede provider-kandidat som egen agentmelding."
            )
        ])
    }

    private static func meetingSkeleton() -> SkeletonElement {
        stack([
            text("Meeting Intent"),
            text("Foreslå tider og vis Jitsi som metadata. Kamera, mikrofon og kalender bes ikke om her."),
            .TextField(SkeletonTextField(
                sourceKeypath: "meetingCoordinator.state.draft.title",
                targetKeypath: "meetingCoordinator.draft.title",
                placeholder: "Meeting title"
            )),
            .TextField(SkeletonTextField(
                sourceKeypath: "meetingCoordinator.state.draft.targetProfileID",
                targetKeypath: "meetingCoordinator.draft.targetProfileID",
                placeholder: "Optional target profile ID"
            )),
            .TextField(SkeletonTextField(
                sourceKeypath: "meetingCoordinator.state.draft.proposedTimesText",
                targetKeypath: "meetingCoordinator.draft.proposedTimesText",
                placeholder: "Proposed times, comma separated ISO-8601"
            )),
            .HStack(SkeletonHStack(elements: [
                button("meetingCoordinator.proposeTimes", "Propose times", payload: .object([:])),
                button("meetingCoordinator.acceptTime", "Accept first time", payload: .object([:])),
                button("meetingCoordinator.declineTime", "Decline first time", payload: .object([:])),
                button("meetingCoordinator.clearMeetingIntent", "Clear intent", payload: .object([:]))
            ], spacing: 8)),
            keyText("meetingCoordinator.state.coordinationStatus"),
            keyText("meetingCoordinator.state.meetingBridge.provider"),
            keyText("meetingCoordinator.state.meetingBridge.joinURL"),
            keyText("meetingCoordinator.state.meetingBridge.requiresCameraMicrophoneConsent"),
            keyText("meetingCoordinator.state.nativePermissionRequests")
        ])
    }

    private static func executablePurposeGroundingSkeleton() -> SkeletonElement {
        .Tabs(SkeletonTabs(
            tabsKeypath: "",
            activeTabStateKeypath: "",
            selectionActionKeypath: nil,
            idKeypath: "id",
            labelKeypath: "title",
            panels: [
                SkeletonTabPanel(id: "plan", content: [
                    stack([
                        section("Siste GroundedActionPlan", [
                            valueRow("Status", "executablePurposeGrounding.state.status"),
                            valueRow("Intent", "executablePurposeGrounding.lastPlan.intentKind"),
                            valueRow("Formål", "executablePurposeGrounding.lastPlan.purposeRefs"),
                            valueRow("Målflate", "executablePurposeGrounding.lastPlan.target.configurationName"),
                            valueRow("Endpoint", "executablePurposeGrounding.lastPlan.target.sourceCellEndpoint"),
                            valueRow("Handling", "executablePurposeGrounding.lastPlan.target.actionKeypath"),
                            valueRow("Risiko", "executablePurposeGrounding.lastPlan.riskLevel"),
                            valueRow("Forklaring", "executablePurposeGrounding.lastPlan.explanation")
                        ]),
                        section("HAVENAgentD", [
                            valueRow("Avgjørelse", "executablePurposeGrounding.state.agentCapabilityDecision.status"),
                            valueRow("Begrunnelse", "executablePurposeGrounding.state.agentCapabilityDecision.reason"),
                            valueRow("Registrering", "executablePurposeGrounding.state.agentCapabilityDecision.registration.status"),
                            valueRow("Neste relasjon", "executablePurposeGrounding.state.agentCapabilityDecision.nextRelation.relationship")
                        ], footer: "Et formålstreff gir ikke agenten grant. Manglende registrering peker til HAVENAgentD Setup."),
                        hstack([
                            button("executablePurposeGrounding.grounding.verify", "Verifiser", payload: .object([:]), style: .primary),
                            button("executablePurposeGrounding.grounding.dryRun", "Dry-run", payload: .object([:]), style: .secondary),
                            button("executablePurposeGrounding.grounding.openHelper", "Åpne forslag", payload: .object([:]), style: .secondary),
                            button("executablePurposeGrounding.grounding.dismiss", "Rydd", payload: .object([:]), style: .secondary)
                        ])
                    ])
                ]),
                SkeletonTabPanel(id: "verify", content: [
                    stack([
                        section("Sjekkresultat", [
                            valueRow("Status", "executablePurposeGrounding.lastVerification.status"),
                            valueRow("Blokkeringer", "executablePurposeGrounding.lastVerification.blockers"),
                            valueRow("Varsler", "executablePurposeGrounding.lastVerification.warnings"),
                            valueRow("Grants sjekket", "executablePurposeGrounding.lastVerification.checkedGrants"),
                            valueRow("Forklaring", "executablePurposeGrounding.lastVerification.explanation")
                        ]),
                        section("Dry-run", [
                            valueRow("Oppsummering", "executablePurposeGrounding.lastDryRun.summary"),
                            valueRow("Leser", "executablePurposeGrounding.lastDryRun.reads"),
                            valueRow("Skriver etter klikk", "executablePurposeGrounding.lastDryRun.writes"),
                            valueRow("Brukerklikk kreves", "executablePurposeGrounding.lastDryRun.userClickRequired")
                        ])
                    ])
                ]),
                SkeletonTabPanel(id: "decompose", content: [
                    stack([
                        section("Formålstre", [
                            valueRow("Schema", "executablePurposeGrounding.lastDecomposition.schema"),
                            valueRow("Status", "executablePurposeGrounding.lastDecomposition.status"),
                            valueRow("Rotformål", "executablePurposeGrounding.lastDecomposition.rootPurposeRef"),
                            valueRow("Dekning", "executablePurposeGrounding.lastDecomposition.coverage.status"),
                            valueRow("Mangler", "executablePurposeGrounding.lastDecomposition.missing"),
                            valueRow("Sideeffektfri", "executablePurposeGrounding.lastDecomposition.sideEffectFree")
                        ]),
                        section("Kilde- og preferansepolicy", [
                            valueRow("Kildepolicy", "executablePurposeGrounding.lastDecomposition.sourcePolicy.policy"),
                            valueRow("Sjekket", "executablePurposeGrounding.lastDecomposition.sourcePolicy.checkedAt"),
                            valueRow("Preferansepolicy", "executablePurposeGrounding.lastDecomposition.preferenceModel.policy"),
                            valueRow("Ingen stille profilmutasjon", "executablePurposeGrounding.lastDecomposition.preferenceModel.noSilentProfileMutation")
                        ])
                    ])
                ]),
                SkeletonTabPanel(id: "schemas", content: [
                    stack([
                        text("Synlige capabilities som grounding kan bruke. Private Perspective/Entity-data brukes kun lokalt i ranking og publiseres ikke som katalog."),
                        .List(SkeletonList(
                            topic: nil,
                            keypath: "executablePurposeGrounding.availableSchemas",
                            flowElementSkeleton: row([
                                keyText("title"),
                                keyText("kind"),
                                keyText("sourceCellEndpoint"),
                                keyText("actionKeypath"),
                                keyText("riskLevel")
                            ])
                        ))
                    ])
                ])
            ]
        ))
    }

    private static func havenAgentCapabilityBrokerSkeleton() -> SkeletonElement {
        stack([
            section(
                "Formål → lokal agentkapabilitet",
                [
                    valueRow("Avgjørelse", "agentCapabilityBroker.state.status"),
                    valueRow("Registrering", "agentCapabilityBroker.state.registration.status"),
                    valueRow("Evidens", "agentCapabilityBroker.state.registration.evidenceKind"),
                    valueRow("Handling", "agentCapabilityBroker.state.lastDecision.matchedActionID"),
                    valueRow("Begrunnelse", "agentCapabilityBroker.state.lastDecision.reason"),
                    valueRow("Neste relasjon", "agentCapabilityBroker.state.lastDecision.nextRelation.relationship")
                ],
                footer: "Formålstreff og runtime-status er beslutningsstøtte. De gir aldri grant, installasjonsrett eller utførelsesrett."
            ),
            section(
                "Manuell statusobservasjon",
                [
                    text("Normal bruk rapporterer fersk status fra haven-agentd status --json eller den token-gatede loopback-broen. Disse knappene kan registrere at agenten mangler eller ikke kjører; de kan ikke påstå at agenten er klar."),
                    hstack([
                        button(
                            "agentCapabilityBroker.registration.report",
                            "AgentD er ikke installert",
                            payload: .object([
                                "status": .string("not_installed"),
                                "evidenceKind": .string("owner-report")
                            ]),
                            style: .secondary
                        ),
                        button(
                            "agentCapabilityBroker.registration.report",
                            "Installert, ikke i gang",
                            payload: .object([
                                "status": .string("installed_not_running"),
                                "evidenceKind": .string("owner-report")
                            ]),
                            style: .secondary
                        ),
                        button("agentCapabilityBroker.registration.clear", "Fjern observasjon", payload: .object([:]), style: .secondary)
                    ])
                ],
                footer: "Access token, private nøkler og credentials avvises og skal aldri limes inn i denne cellen."
            ),
            section(
                "Oppsettshjelp",
                [
                    valueRow("Status", "agentSetup.state.status"),
                    keyText("agentSetup.state.guidance.summary"),
                    valueRow("Personverngrense", "agentSetup.state.privacyBoundary")
                ],
                footer: "Når agent eller action mangler, peker avgjørelsen eksplisitt til cell:///HAVENAgentSetup."
            )
        ])
    }

    private static func havenAgentSetupSkeleton() -> SkeletonElement {
        stack([
            section(
                "HAVENAgentD-oppsett",
                [
                    valueRow("Status", "agentSetup.state.status"),
                    keyText("agentSetup.state.guidance.summary"),
                    valueRow("Statuskommando", "agentSetup.state.guidance.statusCommand"),
                    valueRow("Forventet lokal bro", "agentSetup.state.guidance.expectedBridge"),
                    valueRow("Kjører installatør", "agentSetup.state.installerExecutionAvailable")
                ],
                footer: "Oppsettshjelpen forklarer og verifiserer grunnlag. Installasjon krever et separat lokalt bruker- og OS-samtykke."
            ),
            section(
                "Tillitspakke for installasjonsartefakten",
                [
                    textField(
                        "agentSetup.state.installDraft.artifactReference",
                        "agentSetup.setup.draft.artifactReference",
                        "Verifiserbar referanse til signert installasjonspakke"
                    ),
                    textField(
                        "agentSetup.state.installDraft.sha256",
                        "agentSetup.setup.draft.sha256",
                        "SHA-256"
                    ),
                    textArea(
                        "agentSetup.state.installDraft.signingEvidence",
                        "agentSetup.setup.draft.signingEvidence",
                        "Utgiver, signatur og notarisering",
                        minLines: 3
                    ),
                    button(
                        "agentSetup.setup.install.prepare",
                        "Lag gjennomgåbar installasjonsplan",
                        payload: .object(["explicitConfirmation": .bool(true)]),
                        style: .primary
                    )
                ],
                footer: "Knappen installerer ingenting. Den kontrollerer om artefaktreferanse, hash og signeringsevidens er oppgitt."
            ),
            section(
                "Siste plan",
                [
                    valueRow("Status", "agentSetup.state.lastInstallPlan.status"),
                    valueRow("Blokkeringer", "agentSetup.state.lastInstallPlan.blockers"),
                    valueRow("Krever lokal OS-bekreftelse", "agentSetup.state.lastInstallPlan.requiresLocalOSConfirmation"),
                    valueRow("Sideeffektfri", "agentSetup.state.lastInstallPlan.sideEffectFree"),
                    button("agentSetup.setup.clear", "Rydd oppsett", payload: .object([:]), style: .secondary)
                ]
            )
        ])
    }

    private static func questionnaireCampaignSkeleton() -> SkeletonElement {
        var groupList = SkeletonList(
            topic: nil,
            keypath: "questionnaireCampaign.state.primaryCampaign.recipientGroups",
            flowElementSkeleton: row([
                keyText("label"),
                valueRow("Medlemmer", "memberCount"),
                valueRow("Audience", "messagingAudienceRef"),
                valueRow("Cell", "readiness.cellReadyCount"),
                valueRow("E-post", "readiness.emailReadyCount"),
                valueRow("SMS", "readiness.smsReadyCount")
            ])
        )
        groupList.selectionMode = .multiple
        groupList.selectionValueKeypath = "id"
        groupList.selectionActionKeypath = "questionnaireCampaign.recipients.selectGroupsForDelivery"
        groupList.selectionPayloadMode = .selectedIDs
        groupList.allowsEmptySelection = true

        var recipientList = SkeletonList(
            topic: nil,
            keypath: "questionnaireCampaign.state.primaryCampaign.recipients",
            flowElementSkeleton: row([
                keyText("displayName"),
                keyText("organization"),
                valueRow("Gruppe", "group"),
                valueRow("Readiness", "readiness.status"),
                valueRow("Levering", "delivery.status"),
                valueRow("Svar", "response.status")
            ])
        )
        recipientList.selectionMode = .multiple
        recipientList.selectionValueKeypath = "id"
        recipientList.selectionActionKeypath = "questionnaireCampaign.recipients.selectForDelivery"
        recipientList.selectionPayloadMode = .selectedIDs
        recipientList.allowsEmptySelection = true

        var questionList = SkeletonList(
            topic: nil,
            keypath: "questionnaireCampaign.state.primaryCampaign.config.questions",
            flowElementSkeleton: row([
                keyText("title"),
                keyText("prompt"),
                valueRow("Type", "type"),
                valueRow("Obligatorisk", "required")
            ])
        )
        questionList.selectionMode = .single
        questionList.selectionValueKeypath = "id"

        return .Tabs(SkeletonTabs(
            tabsKeypath: "",
            activeTabStateKeypath: "",
            selectionActionKeypath: nil,
            idKeypath: "id",
            labelKeypath: "title",
            panels: [
                SkeletonTabPanel(id: "overview", content: [
                    stack([
                        section("Oversikt", [
                            valueRow("Tittel", "questionnaireCampaign.state.primaryCampaign.title"),
                            valueRow("Status", "questionnaireCampaign.state.primaryCampaign.lifecycle.status"),
                            valueRow("Avsluttes", "questionnaireCampaign.state.primaryCampaign.lifecycle.endsAt"),
                            valueRow("Spørsmål", "questionnaireCampaign.state.primaryCampaign.questionCount"),
                            valueRow("Spørsmål per side", "questionnaireCampaign.state.primaryCampaign.questionsPerPage"),
                            valueRow("Sider", "questionnaireCampaign.state.primaryCampaign.pageCount"),
                            valueRow("Mottakere", "questionnaireCampaign.state.primaryCampaign.recipientCount"),
                            valueRow("Klare", "questionnaireCampaign.state.primaryCampaign.readiness.readyCount"),
                            valueRow("Blokkert", "questionnaireCampaign.state.primaryCampaign.readiness.blockedCount"),
                            valueRow("Sendt", "questionnaireCampaign.state.primaryCampaign.deliverySummary.sentCount"),
                            valueRow("Besvart", "questionnaireCampaign.state.primaryCampaign.responseSummary.answeredCount")
                        ]),
                        section("Siste handling", [
                            valueRow("Status", "questionnaireCampaign.state.primaryCampaign.lastActionResult.status"),
                            valueRow("Klare", "questionnaireCampaign.state.primaryCampaign.lastActionResult.readyCount"),
                            valueRow("Blokkert", "questionnaireCampaign.state.primaryCampaign.lastActionResult.blockedCount"),
                            valueRow("Provider gate", "questionnaireCampaign.state.primaryCampaign.lastActionResult.providerGate")
                        ]),
                        hstack([
                            button("questionnaireCampaign.delivery.preview", "Forhåndsvis", payload: .object([:]), style: .secondary),
                            button("questionnaireCampaign.delivery.sendReady", "Send klare mottakere", payload: .object([:]), style: .primary),
                            button("questionnaireCampaign.export.json", "JSON", payload: .object([:]), style: .secondary),
                            button("questionnaireCampaign.export.csv", "CSV", payload: .object([:]), style: .secondary)
                        ])
                    ])
                ]),
                SkeletonTabPanel(id: "edit", content: [
                    stack([
                        section("Kampanjeoppsett", [
                            text("Tittel"),
                            textField("questionnaireCampaign.state.primaryCampaign.config.title", "questionnaireCampaign.campaign.title", "Tittel"),
                            text("Formål og kontekst"),
                            textArea("questionnaireCampaign.state.primaryCampaign.config.contextText", "questionnaireCampaign.campaign.contextText", "Kontekst deltageren ser før samtykke", minLines: 4),
                            text("Spørsmål per side"),
                            textField("questionnaireCampaign.state.primaryCampaign.config.questionsPerPage", "questionnaireCampaign.campaign.questionsPerPage", "1"),
                            text("Avslutningsdato, ISO8601. La stå tom for ingen frist."),
                            textField("questionnaireCampaign.state.primaryCampaign.config.lifecycle.endsAt", "questionnaireCampaign.campaign.endsAt", "2026-07-01T12:00:00Z"),
                            text("Status: draft, active eller closed"),
                            textField("questionnaireCampaign.state.primaryCampaign.config.lifecycle.status", "questionnaireCampaign.campaign.status", "active")
                        ]),
                        section("Samtykke", [
                            textArea("questionnaireCampaign.state.primaryCampaign.config.consentText", "questionnaireCampaign.campaign.consentText", "Samtykketekst", minLines: 5)
                        ]),
                        section("Spørsmål", [
                            text("Rediger spørsmål som JSON. Feltene er id, title, prompt, type, required, category og maxLength."),
                            textArea("questionnaireCampaign.state.primaryCampaign.questionEditorJSON", "questionnaireCampaign.questions.replaceFromJSON", "[]", minLines: 12),
                            .List(questionList)
                        ])
                    ])
                ]),
                SkeletonTabPanel(id: "send", content: [
                    stack([
                        section("Mottakerutvalg", [
                            valueRow("Valgte mottakere", "questionnaireCampaign.state.primaryCampaign.deliverySelection.effectiveRecipientCount"),
                            valueRow("Utvalgsmodus", "questionnaireCampaign.state.primaryCampaign.deliverySelection.mode"),
                            text("Velg grupper eller deltakere i listene. Tomt utvalg betyr alle klare mottakere."),
                            .List(groupList),
                            .List(recipientList)
                        ]),
                        section("Invitasjon", [
                            text("E-postemne"),
                            textField("questionnaireCampaign.state.primaryCampaign.config.deliveryPolicy.invitation.emailSubject", "questionnaireCampaign.delivery.emailSubject", "E-postemne"),
                            text("E-posttekst. Bruk {{link}}, {{expiresAt}}, {{accessProofID}} og {{recipientName}}."),
                            textArea("questionnaireCampaign.state.primaryCampaign.config.deliveryPolicy.invitation.emailBody", "questionnaireCampaign.delivery.emailBody", "E-posttekst", minLines: 7),
                            text("SMS-tekst"),
                            textArea("questionnaireCampaign.state.primaryCampaign.config.deliveryPolicy.invitation.smsBody", "questionnaireCampaign.delivery.smsBody", "SMS-tekst", minLines: 3),
                            valueRow("Transportpolicy", "questionnaireCampaign.state.primaryCampaign.config.deliveryPolicy.transportPayloadPolicy.purpose")
                        ]),
                        hstack([
                            button("questionnaireCampaign.delivery.preview", "Forhåndsvis invitasjoner", payload: .object([:]), style: .secondary),
                            button("questionnaireCampaign.delivery.sendReady", "Send til gjeldende utvalg", payload: .object([:]), style: .primary)
                        ])
                    ])
                ]),
                SkeletonTabPanel(id: "recipients", content: [
                    stack([
                        section("Deltakere", [
                            valueRow("Totalt", "questionnaireCampaign.state.primaryCampaign.recipientCount"),
                            valueRow("Cell", "questionnaireCampaign.state.primaryCampaign.readiness.cellReadyCount"),
                            valueRow("E-post", "questionnaireCampaign.state.primaryCampaign.readiness.emailReadyCount"),
                            valueRow("SMS", "questionnaireCampaign.state.primaryCampaign.readiness.smsReadyCount"),
                            valueRow("Blokkert", "questionnaireCampaign.state.primaryCampaign.readiness.blockedCount"),
                            .List(recipientList)
                        ]),
                        section("Grupper", [
                            .List(groupList)
                        ])
                    ])
                ]),
                SkeletonTabPanel(id: "responses", content: [
                    stack([
                        section("Følg opp", [
                            valueRow("Sendt", "questionnaireCampaign.state.primaryCampaign.deliverySummary.sentCount"),
                            valueRow("Besvart", "questionnaireCampaign.state.primaryCampaign.responseSummary.answeredCount"),
                            valueRow("Utkast", "questionnaireCampaign.state.primaryCampaign.responseSummary.draftCount"),
                            valueRow("Leveringsstatuser", "questionnaireCampaign.state.primaryCampaign.deliverySummary.byStatus"),
                            valueRow("Svarstatuser", "questionnaireCampaign.state.primaryCampaign.responseSummary.byStatus")
                        ]),
                        section("Eksport", [
                            text("Eksport viser bare personkoblede svar der samtykke er aktivt."),
                            hstack([
                                button("questionnaireCampaign.export.json", "Eksporter JSON", payload: .object([:]), style: .secondary),
                                button("questionnaireCampaign.export.csv", "Eksporter CSV", payload: .object([:]), style: .secondary)
                            ])
                        ])
                    ])
                ]),
                SkeletonTabPanel(id: "privacy", content: [
                    stack([
                        section("Personvern", [
                            valueRow("Oppsummering", "questionnaireCampaign.privacy.0.summary"),
                            valueRow("Synlighet", "questionnaireCampaign.privacy.0.visibility"),
                            valueRow("Samtykke", "questionnaireCampaign.privacy.0.consentText"),
                            valueRow("Status før samtykke", "questionnaireCampaign.privacy.0.adminMaySeeStatusBeforeConsent"),
                            valueRow("Svar før samtykke", "questionnaireCampaign.privacy.0.adminMaySeePersonLinkedAnswersBeforeConsent"),
                            valueRow("Søk", "questionnaireCampaign.privacy.0.allowFullTextSearch"),
                            valueRow("Auto-oppsummering", "questionnaireCampaign.privacy.0.allowAutoLLMSummary"),
                            valueRow("Kilder", "questionnaireCampaign.privacy.0.privacySourceURLs"),
                            valueRow("Transport", "questionnaireCampaign.privacy.0.transportPayloadPolicy.purpose")
                        ]),
                        section("Svar", [
                            valueRow("Svarstatus", "questionnaireCampaign.state.primaryCampaign.responseSummary.byStatus"),
                            valueRow("Personkoblede svar krever samtykke", "questionnaireCampaign.state.primaryCampaign.privacyGate.requiresExplicitConsentBeforePersonLinkedAnswers")
                        ])
                    ])
                ])
            ]
        ))
    }

    private static func catalogSkeleton() -> SkeletonElement {
        var entries = SkeletonList(
            topic: nil,
            keypath: "personalCatalog.catalogEntries",
            flowElementSkeleton: row([
                keyText("configuration.name"),
                keyText("metadata.policyCategory"),
                keyText("metadata.surfaceFamily"),
                keyText("metadata.executionScope"),
                keyText("metadata.reviewSummary")
            ])
        )
        entries.selectionMode = SkeletonListSelectionMode.none
        return stack([
            text("Personal Co-Pilot Catalog"),
            text("Katalogen viser bare App Store-godkjente Personal Co-Pilot V1-flater."),
            keyText("personalCatalog.state.appStoreScope"),
            keyText("personalCatalog.state.configurationCount"),
            keyText("personalCatalog.state.policySummary"),
            .List(entries)
        ])
    }

    private static func localSurfaceSkeleton(
        title: String,
        purpose: String,
        purposeDescription: String,
        executionScope: String,
        visibleActions: [String],
        nativePermissionRequests: [String]
    ) -> SkeletonElement {
        stack([
            text(title),
            text(purpose),
            text(purposeDescription),
            text("Execution scope: \(executionScope)"),
            text("Native permissions: \(nativePermissionRequests.isEmpty ? "none by default" : nativePermissionRequests.joined(separator: ", "))"),
            text("Supported actions: \(visibleActions.joined(separator: ", "))")
        ])
    }

    private static func stack(_ elements: SkeletonElementList) -> SkeletonElement {
        .VStack(SkeletonVStack(elements: elements, spacing: 10))
    }

    private static func stack(_ elements: SkeletonElementList, role: String) -> SkeletonElement {
        var modifiers = SkeletonModifiers()
        modifiers.styleRole = role
        modifiers.styleClasses = [role]
        return .VStack(SkeletonVStack(elements: elements, spacing: 10, modifiers: modifiers))
    }

    private static func scrollView(_ elements: SkeletonElementList, role: String) -> SkeletonElement {
        var modifiers = SkeletonModifiers()
        modifiers.styleRole = role
        modifiers.styleClasses = [role]
        var scrollView = SkeletonScrollView(axis: "vertical", elements: elements)
        scrollView.modifiers = modifiers
        return .ScrollView(scrollView)
    }

    private static func row(_ elements: SkeletonElementList) -> SkeletonVStack {
        SkeletonVStack(elements: elements, spacing: 4)
    }

    private static func resourceMatchCardRow() -> SkeletonVStack {
        SkeletonVStack(
            elements: [
                resourceMatchMetaRow(),
                styledKeyText("title", role: "resource-match-title"),
                styledKeyText("summary", role: "resource-match-summary"),
                resourceMatchFooterRow()
            ],
            spacing: 8,
            modifiers: resourceMatchCardModifiers()
        )
    }

    private static func resourceMatchMetaRow() -> SkeletonElement {
        hstack(
            [
                styledKeyText("matchBadge", role: "resource-match-badge"),
                styledKeyText("kindLabel", role: "resource-match-kind")
            ],
            role: "resource-match-meta"
        )
    }

    private static func resourceMatchFooterRow() -> SkeletonElement {
        hstack(
            [
                styledKeyText("openHint", role: "resource-match-hint"),
                button(
                    "chatHub.ui.openMatchedResourceLibrary",
                    "Åpne",
                    payload: .object(["autoOpen": .bool(true)]),
                    style: .primary,
                    keypathKeypath: "openActionKeypath",
                    labelKeypath: "openLabel",
                    payloadKeypath: "openPayload"
                )
            ],
            role: "resource-match-footer"
        )
    }

    private static func hstack(_ elements: SkeletonElementList) -> SkeletonElement {
        .HStack(SkeletonHStack(elements: elements, spacing: 8))
    }

    private static func hstack(_ elements: SkeletonElementList, role: String) -> SkeletonElement {
        var modifiers = SkeletonModifiers()
        modifiers.styleRole = role
        modifiers.styleClasses = [role]
        return .HStack(SkeletonHStack(elements: elements, spacing: 8, modifiers: modifiers))
    }

    private static func adaptiveGrid(
        _ elements: SkeletonElementList,
        minColumnWidth: Double,
        role: String
    ) -> SkeletonElement {
        var modifiers = SkeletonModifiers()
        modifiers.styleRole = role
        modifiers.styleClasses = [role]
        return .Grid(SkeletonGrid(
            columns: [.adaptive(min: minColumnWidth)],
            spacing: 12,
            elements: elements,
            modifiers: modifiers
        ))
    }

    private static func assistantResponseActions() -> SkeletonElement {
        var modifiers = SkeletonModifiers()
        modifiers.styleRole = "assistant-response-actions"
        modifiers.styleClasses = ["assistant-response-actions"]
        return .HStack(SkeletonHStack(
            elements: [
                laneChipButton(),
                button("chatHub.ui.openSuggestedHelper", "Åpne hjelper", payload: .object([:]), style: .primary, labelKeypath: "helperActionLabel", payloadKeypath: "helperActionPayload"),
                button("chatHub.ui.openMatchedResourceLibrary", "Last inn flate", payload: .object(["autoOpen": .bool(true)]), style: .secondary, labelKeypath: "surfaceActionLabel", payloadKeypath: "surfaceActionPayload"),
                button("chatHub.assistant.dismissSuggestion", "Avvis", payload: .object([:]), style: .secondary, labelKeypath: "dismissActionLabel")
            ],
            spacing: 8,
            modifiers: modifiers
        ))
    }

    private static func laneChipButton() -> SkeletonElement {
        var button = SkeletonButton(
            keypath: "chatHub.assistant.explainRoute",
            label: "Hvorfor?",
            payload: nil,
            labelKeypath: "laneLabel",
            payloadKeypath: "laneDetailPayload"
        )
        var modifiers = secondaryButtonModifiers()
        modifiers.styleRole = "chat-lane-chip"
        modifiers.styleClasses = ["chat-lane-chip"]
        modifiers.visibility = SkeletonVisibilityRule(when: SkeletonCondition(
            scope: .item,
            keypath: "laneLabel",
            exists: true
        ))
        button.modifiers = modifiers
        return .Button(button)
    }

    private static func automaticEscalationPauseButton(paused: Bool) -> SkeletonElement {
        var button = SkeletonButton(
            keypath: "chatHub.assistant.pauseAutomaticEscalation",
            label: paused ? "Gjenoppta" : "Pause",
            payload: .object(["paused": .bool(paused == false)])
        )
        var modifiers = secondaryButtonModifiers()
        modifiers.styleRole = "chat-escalation-pause"
        modifiers.styleClasses = ["chat-escalation-pause"]
        modifiers.visibility = SkeletonVisibilityRule(when: SkeletonCondition(
            scope: .root,
            keypath: "chatHub.state.ui.automaticEscalation.pauseAutomaticEscalation",
            equals: .bool(paused)
        ))
        button.modifiers = modifiers
        return .Button(button)
    }

    private static func section(_ title: String, _ elements: SkeletonElementList, footer: String? = nil, modifiers: SkeletonModifiers? = nil) -> SkeletonElement {
        var section = SkeletonSection(
            header: titleText(title),
            footer: footer.map { text($0) },
            content: elements
        )
        section.modifiers = modifiers ?? surfaceModifiers()
        return .Section(section)
    }

    private static func text(_ value: String) -> SkeletonElement {
        var text = SkeletonText(text: value)
        text.modifiers = bodyTextModifiers()
        return .Text(text)
    }

    private static func subtleText(_ value: String) -> SkeletonElement {
        var text = SkeletonText(text: value)
        text.modifiers = subtleTextModifiers()
        return .Text(text)
    }

    private static func titleText(_ value: String) -> SkeletonElement {
        var text = SkeletonText(text: value)
        text.modifiers = textModifiers(size: 20, weight: "semibold")
        return .Text(text)
    }

    private static func keyText(_ keypath: String) -> SkeletonElement {
        var text = SkeletonText(keypath: keypath)
        text.modifiers = bodyTextModifiers()
        return .Text(text)
    }

    private static func styledKeyText(_ keypath: String, role: String) -> SkeletonElement {
        var modifiers = bodyTextModifiers()
        modifiers.styleRole = role
        modifiers.styleClasses = [role]
        var text = SkeletonText(keypath: keypath)
        text.modifiers = modifiers
        return .Text(text)
    }

    private static func visibleKeyText(_ keypath: String) -> SkeletonElement {
        var text = SkeletonText(keypath: keypath)
        text.modifiers = visibleWhenExists(keypath)
        return .Text(text)
    }

    private static func textField(_ sourceKeypath: String, _ targetKeypath: String, _ placeholder: String) -> SkeletonElement {
        var field = SkeletonTextField(
            sourceKeypath: sourceKeypath,
            targetKeypath: targetKeypath,
            placeholder: placeholder
        )
        field.modifiers = surfaceInputModifiers()
        return .TextField(field)
    }

    private static func textArea(_ sourceKeypath: String, _ targetKeypath: String, _ placeholder: String, minLines: Int) -> SkeletonElement {
        var area = SkeletonTextArea(
            sourceKeypath: sourceKeypath,
            targetKeypath: targetKeypath,
            placeholder: placeholder,
            minLines: minLines,
            maxLines: max(minLines, minLines + 8),
            submitOnEnter: false,
            editorMode: .plain
        )
        area.modifiers = surfaceInputModifiers()
        return .TextArea(area)
    }

    private static func valueRow(_ label: String, _ keypath: String) -> SkeletonElement {
        hstack([
            text(label),
            keyText(keypath)
        ])
    }

    private enum ButtonStyle {
        case normal
        case primary
        case secondary
    }

    private enum MotionHint: String {
        case appear
        case expand
        case collapse
        case minimize
        case restore
        case replace
        case emphasize
    }

    private static func button(
        _ keypath: String,
        _ label: String,
        payload: ValueType?,
        style: ButtonStyle = .normal,
        keypathKeypath: String? = nil,
        labelKeypath: String? = nil,
        payloadKeypath: String? = nil
    ) -> SkeletonElement {
        var button = SkeletonButton(
            keypath: keypath,
            label: label,
            payload: payload,
            keypathKeypath: keypathKeypath,
            labelKeypath: labelKeypath,
            payloadKeypath: payloadKeypath
        )
        if style == .primary {
            button.modifiers = primaryButtonModifiers()
        } else if style == .secondary {
            button.modifiers = secondaryButtonModifiers()
        }
        return .Button(button)
    }

    private static func visibleButton(
        _ keypath: String,
        _ label: String,
        payload: ValueType?,
        style: ButtonStyle = .normal,
        visibleWhen keypathForVisibility: String
    ) -> SkeletonElement {
        var button = SkeletonButton(keypath: keypath, label: label, payload: payload)
        var modifiers: SkeletonModifiers
        if style == .primary {
            modifiers = primaryButtonModifiers()
        } else if style == .secondary {
            modifiers = secondaryButtonModifiers()
        } else {
            modifiers = SkeletonModifiers()
        }
        modifiers.visibility = SkeletonVisibilityRule(when: SkeletonCondition(
            scope: .root,
            keypath: keypathForVisibility,
            equals: .bool(true)
        ))
        button.modifiers = modifiers
        return .Button(button)
    }

    private static func surfaceModifiers() -> SkeletonModifiers {
        var modifiers = SkeletonModifiers()
        modifiers.padding = 14
        modifiers.background = "#FFFFFF"
        modifiers.foregroundColor = "#172033"
        modifiers.borderColor = "#D7DCE2"
        modifiers.borderWidth = 1
        modifiers.cornerRadius = 8
        return modifiers
    }

    private static func publisherHeroModifiers() -> SkeletonModifiers {
        var modifiers = surfaceModifiers()
        modifiers.padding = 24
        modifiers.background = "#E9FFF5"
        modifiers.borderColor = "#A7E8CE"
        modifiers.cornerRadius = 20
        modifiers.styleRole = "publisher-hero"
        modifiers.styleClasses = ["publisher-hero"]
        return modifiers
    }

    private static func publisherSectionModifiers(role: String) -> SkeletonModifiers {
        var modifiers = surfaceModifiers()
        modifiers.padding = 18
        modifiers.cornerRadius = 16
        modifiers.styleRole = role
        modifiers.styleClasses = [role, "publisher-card"]
        return modifiers
    }

    private static func publisherListModifiers(role: String) -> SkeletonModifiers {
        var modifiers = SkeletonModifiers()
        modifiers.styleRole = role
        modifiers.styleClasses = [role, "publisher-list"]
        return modifiers
    }

    private static func publisherUploadModifiers() -> SkeletonModifiers {
        var modifiers = SkeletonModifiers()
        modifiers.padding = 18
        modifiers.background = "#F4FBF8"
        modifiers.borderColor = "#8DD7BB"
        modifiers.borderWidth = 1
        modifiers.cornerRadius = 14
        modifiers.styleRole = "publisher-media-upload"
        modifiers.styleClasses = ["publisher-media-upload"]
        return modifiers
    }

    private static func surfaceInputModifiers() -> SkeletonModifiers {
        var modifiers = SkeletonModifiers()
        modifiers.padding = 10
        modifiers.background = "#FFFFFF"
        modifiers.foregroundColor = "#172033"
        modifiers.borderColor = "#D7DCE2"
        modifiers.borderWidth = 1
        modifiers.cornerRadius = 6
        return modifiers
    }

    private static func chatConversationModifiers() -> SkeletonModifiers {
        var modifiers = surfaceModifiers()
        modifiers.styleRole = "chat-conversation"
        modifiers.styleClasses = ["chat-conversation"]
        return modifiers
    }

    private static func inlinePollListModifiers() -> SkeletonModifiers {
        var modifiers = SkeletonModifiers()
        modifiers.styleRole = "chat-inline-polls"
        modifiers.styleClasses = ["chat-inline-polls"]
        return modifiers
    }

    private static func inlinePollCardModifiers() -> SkeletonModifiers {
        var modifiers = surfaceModifiers()
        modifiers.styleRole = "chat-inline-poll-card"
        modifiers.styleClasses = ["chat-inline-poll-card"]
        modifiers.background = "#F8FBFF"
        modifiers.borderColor = "#BFD8FF"
        modifiers.padding = 12
        return modifiers
    }

    private static func inlinePollOptionsModifiers() -> SkeletonModifiers {
        var modifiers = SkeletonModifiers()
        modifiers.styleRole = "chat-inline-poll-options"
        modifiers.styleClasses = ["chat-inline-poll-options"]
        return modifiers
    }

    private static func inlinePollOptionModifiers() -> SkeletonModifiers {
        var modifiers = SkeletonModifiers()
        modifiers.styleRole = "chat-inline-poll-option-card"
        modifiers.styleClasses = ["chat-inline-poll-option-card"]
        modifiers.padding = 6
        modifiers.borderColor = "#D7E6FF"
        modifiers.borderWidth = 1
        modifiers.cornerRadius = 6
        return modifiers
    }

    private static func motionSurfaceModifiers(role: String, hint: MotionHint, sourceRole: String? = nil) -> SkeletonModifiers {
        var modifiers = surfaceModifiers()
        modifiers.styleRole = role
        modifiers.motionHint = SkeletonMotionHint(rawValue: hint.rawValue)
        modifiers.motionSourceRole = sourceRole
        var classes = ["motion-\(hint.rawValue)"]
        if let sourceRole {
            classes.append("motion-source-\(sourceRole)")
        }
        modifiers.styleClasses = classes
        return modifiers
    }

    private static func activeComponentPanelModifiers() -> SkeletonModifiers {
        var modifiers = motionSurfaceModifiers(role: "component-panel", hint: .expand, sourceRole: "assistant-response-bubble")
        modifiers.visibility = SkeletonVisibilityRule(when: SkeletonCondition(
            scope: .root,
            keypath: "chatHub.state.ui.hasActiveHelperSurface",
            equals: .bool(true)
        ))
        return modifiers
    }

    private static func pinnedComponentDockModifiers() -> SkeletonModifiers {
        var modifiers = motionSurfaceModifiers(role: "pinned-component-dock", hint: .restore, sourceRole: "component-surface")
        modifiers.visibility = SkeletonVisibilityRule(when: SkeletonCondition(
            scope: .root,
            keypath: "chatHub.state.ui.hasPinnedComponentSurfaces",
            equals: .bool(true)
        ))
        modifiers.styleClasses = ["pinned-component-dock", "snap-grid", "motion-restore", "motion-source-component-surface"]
        return modifiers
    }

    private static func starterCardModifiers() -> SkeletonModifiers {
        var modifiers = surfaceModifiers()
        modifiers.visibility = SkeletonVisibilityRule(when: SkeletonCondition(
            scope: .root,
            keypath: "chatHub.state.ui.showStarters",
            equals: .bool(true)
        ))
        modifiers.styleRole = "chat-starter-card"
        modifiers.styleClasses = ["chat-starter-card"]
        return modifiers
    }

    private static func starterRowModifiers() -> SkeletonModifiers {
        var modifiers = SkeletonModifiers()
        modifiers.styleRole = "chat-starter-row"
        modifiers.styleClasses = ["chat-starter-row"]
        return modifiers
    }

    private static func promptHelpLineModifiers() -> SkeletonModifiers {
        var modifiers = SkeletonModifiers()
        modifiers.visibility = SkeletonVisibilityRule(when: SkeletonCondition(
            scope: .root,
            keypath: "chatHub.state.ui.hasPromptHelp",
            equals: .bool(true)
        ))
        modifiers.styleRole = "chat-help-line"
        modifiers.styleClasses = ["chat-help-line"]
        return modifiers
    }

    private static func clarificationCardModifiers() -> SkeletonModifiers {
        var modifiers = motionSurfaceModifiers(role: "chat-clarification-card", hint: .appear, sourceRole: "assistant-response-bubble")
        modifiers.visibility = SkeletonVisibilityRule(when: SkeletonCondition(
            scope: .root,
            keypath: "chatHub.state.assistant.clarification",
            exists: true
        ))
        modifiers.styleClasses = ["chat-clarification-card", "motion-appear", "motion-source-assistant-response-bubble"]
        return modifiers
    }

    private static func routeExplanationCardModifiers() -> SkeletonModifiers {
        var modifiers = motionSurfaceModifiers(role: "chat-route-explanation-card", hint: .appear, sourceRole: "chat-lane-chip")
        modifiers.visibility = SkeletonVisibilityRule(when: SkeletonCondition(
            scope: .root,
            keypath: "chatHub.state.assistant.routeExplanation",
            exists: true
        ))
        modifiers.styleClasses = ["chat-route-explanation-card", "motion-appear", "motion-source-chat-lane-chip"]
        return modifiers
    }

    private static func automaticEscalationMeterModifiers() -> SkeletonModifiers {
        var modifiers = surfaceModifiers()
        modifiers.visibility = SkeletonVisibilityRule(when: SkeletonCondition(
            scope: .root,
            keypath: "chatHub.state.ui.automaticEscalation.showMeter",
            equals: .bool(true)
        ))
        modifiers.styleRole = "chat-escalation-meter"
        modifiers.styleClasses = ["chat-escalation-meter"]
        return modifiers
    }

    private static func automaticEscalationConsentModifiers() -> SkeletonModifiers {
        var modifiers = surfaceModifiers()
        modifiers.visibility = SkeletonVisibilityRule(when: SkeletonCondition(
            scope: .root,
            keypath: "chatHub.state.ui.automaticEscalation.lastDecisionReason",
            equals: .string(ChatInterpreterEscalationDecisionReason.missingAutomaticGrant.rawValue)
        ))
        modifiers.styleRole = "chat-escalation-consent"
        modifiers.styleClasses = ["chat-escalation-consent"]
        return modifiers
    }

    private static func askThisTimeCardModifiers() -> SkeletonModifiers {
        var modifiers = motionSurfaceModifiers(role: "chat-ask-this-time", hint: .appear, sourceRole: "chat-escalation-meter")
        modifiers.visibility = SkeletonVisibilityRule(when: SkeletonCondition(
            scope: .root,
            keypath: "chatHub.state.ui.automaticEscalation.canAskStrongerModelThisTime",
            equals: .bool(true)
        ))
        modifiers.styleClasses = ["chat-ask-this-time", "motion-appear", "motion-source-chat-escalation-meter"]
        return modifiers
    }

    private static func clarificationOptionListModifiers() -> SkeletonModifiers {
        var modifiers = SkeletonModifiers()
        modifiers.styleRole = "chat-clarification-options"
        modifiers.styleClasses = ["chat-clarification-options"]
        return modifiers
    }

    private static func clarificationOptionCardModifiers() -> SkeletonModifiers {
        var modifiers = surfaceModifiers()
        modifiers.styleRole = "chat-clarification-option"
        modifiers.styleClasses = ["chat-clarification-option"]
        return modifiers
    }

    private static func componentSurfaceCardModifiers() -> SkeletonModifiers {
        var modifiers = surfaceModifiers()
        modifiers.styleRole = "component-surface-card"
        modifiers.styleClasses = ["component-surface-card"]
        return modifiers
    }

    private static func pinnedComponentCardModifiers() -> SkeletonModifiers {
        var modifiers = surfaceModifiers()
        modifiers.styleRole = "pinned-component-card"
        modifiers.styleClasses = ["pinned-component-card", "snap-grid-item"]
        return modifiers
    }

    private static func pinnedComponentChipListModifiers() -> SkeletonModifiers {
        var modifiers = SkeletonModifiers()
        modifiers.styleRole = "pinned-component-dock"
        modifiers.styleClasses = ["pinned-component-dock", "snap-grid"]
        return modifiers
    }

    private static func pinnedComponentChipModifiers() -> SkeletonModifiers {
        var modifiers = SkeletonModifiers()
        modifiers.styleRole = "pinned-component-chip"
        modifiers.styleClasses = ["pinned-component-chip", "snap-grid-item"]
        return modifiers
    }

    private static func minimizedComponentChipListModifiers() -> SkeletonModifiers {
        var modifiers = SkeletonModifiers()
        modifiers.styleRole = "minimized-component-chip-list"
        modifiers.styleClasses = ["minimized-component-chip-list", "snap-grid"]
        return modifiers
    }

    private static func personDragModifiers(payloadKeypath: String) -> SkeletonModifiers {
        var modifiers = surfaceModifiers()
        modifiers.draggableRole = "person"
        modifiers.dragPayloadKeypath = payloadKeypath
        modifiers.dragPreviewRole = "person-chip"
        modifiers.accessibilityDragLabel = "Dra person inn i chat"
        modifiers.styleRole = "person-drag-source"
        modifiers.styleClasses = ["person-drag-source"]
        return modifiers
    }

    private static func chatInviteDropModifiers() -> SkeletonModifiers {
        var modifiers = surfaceModifiers()
        modifiers.dropTargetRole = "chat-invite-slot"
        modifiers.acceptedDragRoles = ["person"]
        modifiers.dropActionKeypath = "chatHub.drop.receive"
        modifiers.dropIntents = ["add"]
        modifiers.dropValidationStateKeypath = "chatHub.state.drop.validationState"
        modifiers.dropDeniedReasonKeypath = "chatHub.state.drop.deniedReason"
        modifiers.accessibilityDropLabel = "Slipp en person her for å fylle invitasjonsutkastet"
        modifiers.styleRole = "chat-invite-drop-target"
        modifiers.styleClasses = ["chat-invite-drop-target"]
        return modifiers
    }

    private static func textModifiers(size: Double, weight: String) -> SkeletonModifiers {
        var modifiers = SkeletonModifiers()
        modifiers.foregroundColor = "#172033"
        modifiers.fontSize = size
        modifiers.fontWeight = weight
        return modifiers
    }

    private static func bodyTextModifiers() -> SkeletonModifiers {
        var modifiers = SkeletonModifiers()
        modifiers.foregroundColor = "#172033"
        return modifiers
    }

    /// En gruppe uten synlighetsregel. Holder beslektede elementer samlet i
    /// panelet uten aa si noe om naar de vises.
    private static func visibleGroup(_ elements: SkeletonElementList) -> SkeletonElement {
        return .VStack(SkeletonVStack(elements: elements, spacing: 8))
    }

    /// En gruppe som bare vises naar betingelsen holder. Brukes for aa la
    /// ett panel vise ulike deler etter tilstand i stedet for alt paa en gang.
    private static func visibleGroup(_ elements: SkeletonElementList, when condition: SkeletonCondition) -> SkeletonElement {
        var stack = SkeletonVStack(elements: elements, spacing: 8)
        var modifiers = SkeletonModifiers()
        modifiers.visibility = SkeletonVisibilityRule(when: condition)
        stack.modifiers = modifiers
        return .VStack(stack)
    }

    private static func visibleWhenBool(_ keypath: String) -> SkeletonModifiers {
        var modifiers = bodyTextModifiers()
        modifiers.visibility = SkeletonVisibilityRule(when: SkeletonCondition(
            scope: .root,
            keypath: keypath,
            equals: .bool(true)
        ))
        return modifiers
    }

    private static func visibleWhenExists(_ keypath: String, scope: SkeletonVisibilityScope = .root) -> SkeletonModifiers {
        var modifiers = bodyTextModifiers()
        modifiers.visibility = SkeletonVisibilityRule(when: SkeletonCondition(
            scope: scope,
            keypath: keypath,
            exists: true
        ))
        return modifiers
    }

    private static func subtleTextModifiers() -> SkeletonModifiers {
        var modifiers = SkeletonModifiers()
        modifiers.foregroundColor = "#475569"
        modifiers.fontSize = 14
        modifiers.styleRole = "secondary-text"
        return modifiers
    }

    private static func composerModifiers() -> SkeletonModifiers {
        var modifiers = SkeletonModifiers()
        modifiers.background = "#FFFFFF"
        modifiers.foregroundColor = "#111827"
        modifiers.borderColor = "#CBD5E1"
        modifiers.borderWidth = 1
        modifiers.cornerRadius = 8
        modifiers.padding = 10
        modifiers.styleRole = "chat-composer"
        return modifiers
    }

    private static func activeToolChipListModifiers() -> SkeletonModifiers {
        var modifiers = SkeletonModifiers()
        modifiers.styleRole = "chat-active-tool-chips"
        modifiers.styleClasses = ["chat-active-tool-chips"]
        return modifiers
    }

    private static func activeToolChipModifiers() -> SkeletonModifiers {
        var modifiers = SkeletonModifiers()
        modifiers.styleRole = "chat-active-tool-chip"
        modifiers.styleClasses = ["chat-active-tool-chip"]
        return modifiers
    }

    private static func resourceMatchListModifiers() -> SkeletonModifiers {
        var modifiers = SkeletonModifiers()
        modifiers.styleRole = "resource-match-list"
        modifiers.styleClasses = ["resource-match-list"]
        return modifiers
    }

    private static func resourceMatchCardModifiers() -> SkeletonModifiers {
        var modifiers = SkeletonModifiers()
        modifiers.styleRole = "resource-match-card"
        modifiers.styleClasses = ["resource-match-card"]
        return modifiers
    }

    private static func primaryButtonModifiers() -> SkeletonModifiers {
        var modifiers = SkeletonModifiers()
        modifiers.background = "#1D4ED8"
        modifiers.foregroundColor = "#FFFFFF"
        modifiers.cornerRadius = 6
        return modifiers
    }

    private static func secondaryButtonModifiers() -> SkeletonModifiers {
        var modifiers = SkeletonModifiers()
        modifiers.background = "#FFFFFF"
        modifiers.foregroundColor = "#334155"
        modifiers.borderColor = "#CBD5E1"
        modifiers.borderWidth = 1
        modifiers.cornerRadius = 6
        return modifiers
    }
}
