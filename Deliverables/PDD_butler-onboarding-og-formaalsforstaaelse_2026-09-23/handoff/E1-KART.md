STATUS: LEVERT — 371 plasser, 18 står i kode, 4 utsatt; SHA adf48d4615d1ed143d5bdc190fcf63e266214c8f

# E1-kart — alternativ B

Dokumentleveranse 2026-09-29 fra Codex til Losen/b1a. Ingen implementasjon, Butler-kjøring eller flytting er utført. WP8-kompatibilitet er et eksplisitt akseptansekrav, ikke en målt egenskap ved et register som ennå mangler importkontrakt.

## Telling og kildegrunnlag

Koden er lest med git show fra CellScaffold origin/main, SHA adf48d4615d1ed143d5bdc190fcf63e266214c8f. Dette er den lokale remote-refen ved kontrollen; ingen fetch. Ingen utsjekkede Swift-filer er brukt. Historiske linjer i E1-DESIGN/Astra kan avvike; linjene her gjelder SHA-en over.

En **plass** er ett navngitt parameterfelt (en liste teller én, også tokengrupper). Leksikonet har 27 × 7 = 189 plasser, øvrige felt 182. Alle er listet nedenfor og typet i skjemaet. entryID, fasett-ID og proveniens er kontraktmetadata, ikke uttrekte literaler. «18 står i kode» teller K01–K18, navngitte kodekontrakter; «4 utsatt» teller U01–U04, navngitte uttrekksområder. Tallene har ulike enheter og skal ikke summeres til antall funksjoner.

| Forkortelse | Fil i CellScaffold |
|---|---|
| R | Sources/App/Support/ChatPurposeResourceRouter.swift |
| C | Sources/App/Cells/PersonalCopilot/PersonalCopilotCloudStore.swift |
| K | Sources/App/Support/PurposeKnowledgeBase.swift |

R:2322 betyr filen R, linje 2322 på SHA-en over. Destinasjoner er under content.consumerFacets.butler. [Skjemaet](../contract/butler_purpose_graph_v1.schema.json) er lukket for Butler-felter. Det finnes ingen regel-AST, vilkårlig operator, regex, funksjonsnavn eller evalueringsrekkefølge som data. Dagens kodegren leser feltet direkte.

## 1. Alle 27 leksikonoppslag i kildeorden

For hver rad flyttes purposeRef, label, queryPhrases, requiredQueryTokenGroups, resourceHints, endpointHints og scoreBoost til typede felt i lexicon[]. Ingen lister sorteres, dedupliseres, oversettes eller normaliseres. Hele feltverdien fra det oppgitte kildeintervallet skal tas med; dette er et kart, ikke et nytt fraseutvalg. entryID er stabil selv om en godkjent kandidat endrer array-rekkefølge.

Kildelinjene står i rekkefølgen ref / label / fraser / tokengrupper / resource / endpoint / boost. K01–K03 beholder matching, rekkefølge og normalisering i kode for **hver** rad for å bevare beslutningene.

| Orden / plass-ID | purposeRef uendret | R:kildelinjer | scoreBoost | Endpoint-kilde |
|---|---|---|---|---|
| 0 / lex.01 | conference.demo.story.run | 2322 / 2323 / 2324 / 2355 / 2359 / 2373 / 2374 | 0.46 | ["cell:///ConferenceDemoStory"] |
| 1 / lex.02 | admin.cell-lifecycle.cleanup-review | 2377 / 2378 / 2379 / 2401 / 2405 / 2418 / 2419 | 0.44 | [AdminControlPlaneRouting.current.endpoint(for: "AdminOverview")] |
| 2 / lex.03 | admin.identity.vc.request | 2422 / 2423 / 2424 / 2444 / 2448 / 2462 / 2463 | 0.46 | ["cell:///AccessRequirementPrompt", AdminControlPlaneRouting.current.endpoint(for: "AdminEntry")] |
| 3 / lex.04 | admin.scaffold-operations.observe | 2466 / 2467 / 2468 / 2515 / 2519 / 2534 / 2535 | 0.45 | [AdminControlPlaneRouting.current.endpoint(for: "AdminOverview")] |
| 4 / lex.05 | conference.agenda.view | 2538 / 2539 / 2540 / 2590 / 2594 / 2605 / 2611 | 0.40 | [ "cell:///ConferenceParticipantPreviewShell", "cell:///ConferenceParticipantShell", ArendalsukaConfigurationPublisherContract.endpoint, "cell:///ArendalsukaParticipantProgram" ] |
| 5 / lex.06 | arendalsuka.companion.introduce | 2614 / 2615 / 2616 / 2645 / 2649 / 2664 / 2668 | 0.43 | [ ArendalsukaConfigurationPublisherContract.endpoint, "cell:///ArendalsukaEventAtlas" ] |
| 6 / lex.07 | purpose://arendalsuka.configuration.draft-preview | 2671 / 2672 / 2673 / 2685 / 2690 / 2691 / 2692 | 0.50 | ["cell:///ConfigurationCatalog", "cell:///CellConfigurationStudio"] |
| 7 / lex.08 | purpose://arendalsuka.configuration.official-publish | 2695 / 2696 / 2697 / 2706 / 2711 / 2712 / 2713 | 0.54 | ["cell:///ConfigurationCatalog"] |
| 8 / lex.09 | purpose://event.meeting-place.agree | 2716 / 2717 / 2718 / 2744 / 2748 / 2760 / 2767 | 0.42 | [ ArendalsukaConfigurationPublisherContract.endpoint, "cell:///ConferenceParticipantPreviewShell", "cell:///ConferenceConnectionHub", "cell:///ConferenceLocationShare", "cell:///ArendalsukaEventAtlas" ] |
| 9 / lex.10 | purpose://event.group-chat.vote | 2770 / 2771 / 2772 / 2792 / 2796 / 2807 / 2812 | 0.43 | [ ArendalsukaConfigurationPublisherContract.endpoint, "cell:///ConferenceChatLaunch", "cell:///ConferenceParticipantPreviewShell" ] |
| 10 / lex.11 | purpose://democracy.vote.participate | 2815 / 2816 / 2817 / 2836 / 2840 / 2850 / 2855 | 0.41 | [ ArendalsukaConfigurationPublisherContract.endpoint, "cell:///ArendalsukaEventAtlas", "cell:///ConferenceParticipantPreviewShell" ] |
| 11 / lex.12 | arendalsuka.local-commerce.discover | 2858 / 2859 / 2860 / 2878 / 2882 / 2894 / 2898 | 0.42 | [ ArendalsukaConfigurationPublisherContract.endpoint, "cell:///ArendalsukaEventAtlas" ] |
| 12 / lex.13 | arendalsuka.social-networking.meet | 2901 / 2902 / 2903 / 2937 / 2941 / 2951 / 2956 | 0.42 | ["cell:///PersonalMatchmaking", "cell:///PublicProfileDirectory", ArendalsukaConfigurationPublisherContract.endpoint, "cell:///ConferenceEntityDiscovery", "cell:///ConferenceChatLaunch" ] |
| 13 / lex.14 | purpose://agreement.terms.put-in-writing | 2961 / 2962 / 2963 / 2982 / 2986 / 2993 / 2994 | 0.34 | ["cell:///AgreementWorkbench"] |
| 14 / lex.15 | personal.diagram.mermaid.render | 2997 / 2998 / 2999 / 3032 / 3036 / 3045 / 3046 | 0.34 | ["cell:///MermaidRenderer"] |
| 15 / lex.16 | personal.chat.assist.spatial-query | 3049 / 3050 / 3051 / 3087 / 3091 / 3102 / 3103 | 0.40 | ["cell:///SpatialProjection"] |
| 16 / lex.17 | personal.ai.gateway.configure | 3106 / 3107 / 3108 / 3188 / 3192 / 3218 / 3219 | 0.38 | ["cell:///AIGateway"] |
| 17 / lex.18 | purpose://personal-entity.activity-dashboard.view | 3222 / 3223 / 3224 / 3245 / 3250 / 3257 / 3258 | 0.56 | [] |
| 18 / lex.19 | purpose://capability.construct-cellconfiguration | 3261 / 3262 / 3263 / 3317 / 3321 / 3335 / 3336 | 0.44 | ["cell:///ConfigurationCatalog", "cell:///AIGateway"] |
| 19 / lex.20 | purpose://capability.request-new-functionality | 3339 / 3340 / 3341 / 3358 / 3362 / 3375 / 3376 | 0.40 | ["cell:///WorkItem", "cell:///ProjectPortfolio", "cell:///IdeaTaskWorkspace"] |
| 20 / lex.21 | cellprotocol.docs.lookup | 3379 / 3380 / 3381 / 3409 / 3413 / 3426 / 3427 | 0.36 | ["cell:///MarkdownRenderer"] |
| 21 / lex.22 | personal.music.publish | 3430 / 3431 / 3432 / 3468 / 3472 / 3484 / 3485 | 0.34 | ["cell:///MusicPublishingConsole"] |
| 22 / lex.23 | personal.profile.page.create | 3488 / 3489 / 3490 / 3524 / 3528 / 3537 / 3538 | 0.42 | ["cell:///PersonalPagePublisher"] |
| 23 / lex.24 | personal.public-presence.publish | 3541 / 3542 / 3543 / 3605 / 3609 / 3633 / 3634 | 0.44 | ["cell:///PersonalPagePublisher", "cell:///PersonalProfilePublisher"] |
| 24 / lex.25 | personal.entity.relations.manage | 3637 / 3638 / 3639 / 3677 / 3681 / 3694 / 3695 | 0.38 | ["cell:///EntityStudio"] |
| 25 / lex.26 | haven.work.board.view | 3698 / 3699 / 3700 / 3715 / 3719 / 3730 / 3731 | 0.38 | ["cell:///WorkItem"] |
| 26 / lex.27 | knowledge.demo.kallimachos | 3741 / 3742 / 3743 / 3801 / 3810 / 3820 / 3821 | 0.36 | [KallimachosAdvisorContract.endpoint] |

Det er **indeksen blant matchede oppføringer**, ikke absolutt plass blant alle 27, som gir fratrekk 0,04 i understand (R:1040–1046) og låserang 1000 − indeks (R:2293–2303). Kilderekkefølgen avgjør dermed rekkefølgen etter filtrering. endpointHints bruker case-insensitiv helstrengslikhet (R:924–926); resourceHints bruker substring i normalisert metadata (R:914–921). De blir ikke slått sammen til capabilityHints.

**Konstantkilder på samme SHA:** draft/publish-ref: Sources/App/Cells/Arendalsuka/ArendalsukaConfigurationPublisherCell.swift:21–22; publisher-endpoint: samme fil :9. Dashboard-ref og eksakt navn: Sources/App/Cells/PersonalEntityActivity/PersonalEntityActivityDashboardConfigurationFactory.swift:10,14. Kallimachos-endpoint: Sources/App/Cells/AI/KallimachosAdvisorCell.swift:19. Rene konstanter materialiseres som de samme strengene.

**Miljøbinding:** AdminControlPlaneRouting.current.endpoint(for:) er miljøavhengig (Sources/ScaffoldKit/AdminControlPlaneRouting.swift:216–222). endpointHints bruker to lukkede objekter med binding=adminOverview eller binding=adminEntry for disse eksisterende kallene; ingen dynamisk funksjonsoppløsning. Vert/adresse/hemmeligheter lagres ikke i grafen. Det løste endepunktet festes sammen med analyseinput og bindes i målerapportens miljøgrunnlag. Baseline bygger dette i et static let-leksikon (R:2320): b1a må bevare samme init-fase og levetid for løst miljøbinding, og feste dette miljøsnapshotet til analysen. Å lese en endret AdminControlPlaneRouting.current på nytt per analyse kan endre oppførsel og er ikke del av E1. Prøv også endret miljøbinding etter første leksikontilgang.

## 2. Elleve særregler og to etter sløyfen

S01–S11 kjøres i kildeorden inne i exactPurposeMatch OR exactEndpointMatch etter score += scoreBoost (R:1560–1561). Generiske metadata-treff bruker egen gren (R:1647–1649) og får ingen av disse særreglene. Målflate, formålslikhet, sammenligningsmåte, fase og operasjon er kode. Hvert navngitte tall er en egen plass; ingen global floor/cap per formål.

| Regel / typed record | Fil:linje | Betingelse, målflate, fase og operasjon som blir kode |
|---|---|---|
| S01 / router.specialRules.profilePublish | R:1562–1565 | Exact purpose/endpoint; personal.profile.page.create OR personal.public-presence.publish; max(score, floor). |
| S02 / router.specialRules.conferenceAgenda | R:1566–1571 | Exact purpose/endpoint; conference.agenda.view; max(score, floor). |
| S03 / router.specialRules.configurationAuthoring | R:1572–1579 | Exact; purpose://capability.construct-cellconfiguration; normalized name cell configuration architect: max(score + add, floor); else ai agent workspace: min(score, workspaceCap). |
| S04 / router.specialRules.activityDashboard | R:1580–1583 | Exact; dashboard routing purpose AND exact combinedConfigurationName; max(score + add, floor). |
| S05 / router.specialRules.adminOperations | R:1584–1592 | Exact; admin.scaffold-operations.observe; admin control plane overview: add then floor; else admin copilot workspace OR admin cell dashboard: cap. |
| S06 / router.specialRules.adminCleanup | R:1593–1600 | Exact; admin.cell-lifecycle.cleanup-review; admin cell dashboard: add then floor; else admin copilot workspace: cap. |
| S07 / router.specialRules.aiGateway | R:1601–1607 | Exact; personal.ai.gateway.configure; normalized name ai agent workspace OR normalized endpoint contains cell aigateway; add then floor. |
| S08 / router.specialRules.kallimachosAdvisor | R:1608–1618 | Exact; knowledge.demo.kallimachos; endpoint equals KallimachosAdvisorContract.endpoint case-insensitively; add then floor. |
| S09 / router.specialRules.adminCredential | R:1619–1625 | Exact; admin.identity.vc.request; normalized name access requirement prompt OR endpoint contains cell accessrequirementprompt; add then floor. |
| S10 / router.specialRules.arendalsukaIntroduction | R:1626–1633 | Exact; arendalsuka.companion.introduce; publisher endpoint: add then floor; else EventAtlas: cap. |
| S11 / router.specialRules.arendalsukaParticipant | R:1634–1643 | Exact; text contains arendalsuka AND isArendalsukaParticipantPurpose; publisher: add then floor; else EventAtlas AND !mentionsArendalsukaAtlasMaintenance: cap. May follow S10. |
| P01 / router.specialRules.dashboardAfterLexicon | R:1653–1664 | After loop if dashboard intent matched; exact combinedConfigurationName: floor; else architect: cap. Not inside S04. |
| P02 / router.specialRules.artistSalesAfterLexicon | R:1666–1680 | After P01; exact ArtistSales endpoint; artTerms substring in normalized prompt: floor, otherwise cap. Context boost follows. |

P01/P02 er tillegg til de elleve. Etter dem kommer refs-deduplisering, purposeContext.matchBoost og sluttklamping (R:1681–1688). Et tidligere tak er derfor **ikke** et tak på ferdig score. Operasjonsrekkefølgen må ikke flyttes.

## 3. Alle 17 hjelpefunksjoner

13 entallsfunksjoner …IntentScore + én flertallsadapter butlerSignalIntentScores + tre andre funksjoner = 17. 15 får typede plasser; kontrollflyt, første retur og standardretur beholdes (K04–K10). Tabellen beskriver eksakte grener; alle feltverdier finnes som examples i skjemaet og kildehenvisninger i §4.

| Funksjon → typed record | Fil:linje | Kodekontrakt som bevares |
|---|---|---|
| isInviteIntent → helpers.invite | C:14714–14733 | lowercased; negation first; listExclusions only affect addPhrases. Original-text regex and boolean returns remain code. |
| isPollIntent → helpers.poll | C:14735–14768 | lowercased; negation and two global exclusions; groupChoice OR (cannotAgree AND alternative); exact token/prefix fallback. |
| videoMeetingIntentScore → helpers.videoMeeting | C:14770–14793 | lowercased; negation then direct, expanded, call AND immediate, device; first return, otherwise zero. |
| scheduleMeetingIntentScore → helpers.scheduleMeeting | C:14795–14812 | lowercased; negation; meeting AND scheduling before explicit phrase. schedule meeting remains 0.84, never max over branches. |
| projectIntentScore → helpers.project | C:14814–14847 | lowercased; negation and publish exclusions stop all; project AND work, general project, workspace in that order. |
| ideaCaptureIntentScore → helpers.ideaCapture | C:14849–14869 | nb_NO folding/lowercase; negation then capture, note, token fallback with local no-idea exclusion. |
| todoIntentScore → helpers.todo | C:14871–14902 | lowercased; AI exclusion before negation. generic, list, remember, delegate; todo list stays 0.78. |
| reminderIntentScore → helpers.reminder | C:14904–14919 | lowercased; negation, direct, then (notify OR loseTrack) AND mentionsClockTime. notify wins overlap; clock predicate stays code. |
| guidedOnboardingIntentScore → helpers.guidedOnboarding | C:14929–15112 | normalizedAssistantText; negation then gateway AND explicitSetup AND (!status OR strongSetup), questionnaire AND setup, modelNotConnected AND !status, gettingStarted AND !otherSurface, onboarding AND conference, onboarding. All exception scopes and order stay code. |
| capabilityDiscoveryOnboardingIntentScore → helpers.capabilityDiscoveryOnboarding | C:15114–15133 | normalizedAssistantText; one phrases list for suppression markers and positive match; score or zero. |
| advisoryReportIntentScore → helpers.advisoryReport | C:15245–15320 | normalizedAssistantText; negation, panel, short assessment phrase/prefix, advisor AND (assessment OR report), advisor, assessment AND report, assessment. First return; prefix remains anchored. |
| uncertainGoalClarificationIntentScore → helpers.uncertainGoalClarification | C:15351–15454 | normalizedAssistantText; negation, strong phrases, uncertainty AND goal words; otherwise zero. |
| capabilityGapIntentScore → helpers.capabilityGap | C:15545–15584 | lowercased; negation, explicit gap, other gap phrases, desire AND product; otherwise zero. |
| workItemIntentScore → helpers.workItem | C:15586–15683 | normalizedAssistantText; negation, capture, product AND failure, fix phrases with product-dependent score. All order remains code. |
| moderationIntentScore → helpers.moderation | C:15685–15703 | lowercased; phrase match or zero. Baseline has no negation guard; E1 must not add one. |
| agentActionMatch → U01 | C:15710–15744; C:13728 | **UTSATT:** descriptor, handlingsvalg, tabeller og råscore blir kode samlet i første runde. |
| butlerSignalIntentScores → U02 | C:12748–12770; C:13720–13737 | **UTSATT:** matcher-/katalogadapter og dens parametre blir kode samlet. |

**U01, gren for gren:** nektelse C:15713; Finder + lukke-/ryddeord :15716–15718; desktopPlace + desktopMess :15721–15724 gir også mac.finder.close-all-windows; Binding + wake :15726–15728 gir shortcut.binding.wake; Binding + absorb :15730–15732 gir binding.absorb.cell-input; watch AND (folder OR folder-watch-frase) :15734–15737 gir folder-watch.changed-input; sprout + sync :15739–15741 gir sprout.sync.local-agent; ellers nil. Første katalogoppslag returnerer direkte, også når valgt descriptor mangler. v1Actions, risiko, interesser, refs og actionID bevares. Råscore 0,88 legges på senere (C:13728).

**U02, gren for gren:** specificity ≥ 3 og ikke isNoActionStatement (C:12757–12758); matcher med minimum 0,62 (:12760); hasActionSignal, capability-oppslag, intentKindRawValue, enum-dekoding og supportedInChatV1 (:12761–12765); per-kind maksimum med 0,70 (:12768); ordbok ut. C:13721–13737 kombinerer bare eksplisitt utvalgte scorer med max; video, moderation og agent beholder egne spor. ButlerSignalMatcher/ButlerCapabilityCatalog er ikke erklært uttrekt.

## 4. Alle øvrige parameterplasser

De 182 radene her og de 189 leksikonfeltene er statuslinjens 371 plasser. Fraselister er ordnet [String]; tall er endelige Double i [0,1]. examples er kildeuttrekk til byggingen, ikke skjemadefaults. Runtime skal avvise manglende felt. Hvor linjen inneholder to lister/scorer, er skillet navngitt eksplisitt.

| Navngitt plass | Fil:linje | Type | Startverdi / kildeomfang |
|---|---|---|---|
| helpers.invite.suppressionMarkers | C:14716 | [String] | 5 strenger, hele oppgitte intervallet |
| helpers.invite.listExclusions | C:14720–14721 | [String] | 16 strenger, hele oppgitte intervallet |
| helpers.invite.explicitPhrases | C:14722 | [String] | 2 strenger, hele oppgitte intervallet |
| helpers.invite.addPhrases | C:14725 | [String] | 3 strenger, hele oppgitte intervallet |
| helpers.invite.conversationPhrases | C:14729 | [String] | 9 strenger, hele oppgitte intervallet |
| helpers.poll.suppressionMarkers | C:14737 | [String] | 5 strenger, hele oppgitte intervallet |
| helpers.poll.civicExclusions | C:14741 | [String] | 10 strenger, hele oppgitte intervallet |
| helpers.poll.meetingPlaceExclusions | C:14746 | [String] | 9 strenger, hele oppgitte intervallet |
| helpers.poll.groupChoicePhrases | C:14749 | [String] | 8 strenger, hele oppgitte intervallet |
| helpers.poll.cannotAgreePhrases | C:14750 | [String] | 10 strenger, hele oppgitte intervallet |
| helpers.poll.alternativePhrases | C:14751 | [String] | 7 strenger, hele oppgitte intervallet |
| helpers.poll.exactTokens | C:14759–14763 | [String] | 5 strenger, hele oppgitte intervallet |
| helpers.poll.tokenPrefixes | C:14764–14766 | [String] | 3 strenger, hele oppgitte intervallet |
| helpers.videoMeeting.suppressionMarkers | C:14775 | [String] | 6 strenger, hele oppgitte intervallet |
| helpers.videoMeeting.directPhrases | C:14778 | [String] | 5 strenger, hele oppgitte intervallet |
| helpers.videoMeeting.directScore | C:14779 | Double | 0.84 |
| helpers.videoMeeting.expandedPhrases | C:14782 | [String] | 12 strenger, hele oppgitte intervallet |
| helpers.videoMeeting.expandedScore | C:14783 | Double | 0.84 |
| helpers.videoMeeting.callWords | C:14785 | [String] | 3 strenger, hele oppgitte intervallet |
| helpers.videoMeeting.immediateWords | C:14786 | [String] | 6 strenger, hele oppgitte intervallet |
| helpers.videoMeeting.immediateScore | C:14787 | Double | 0.8 |
| helpers.videoMeeting.deviceWords | C:14789 | [String] | 4 strenger, hele oppgitte intervallet |
| helpers.videoMeeting.deviceScore | C:14790 | Double | 0.76 |
| helpers.scheduleMeeting.suppressionMarkers | C:14798 | [String] | 6 strenger, hele oppgitte intervallet |
| helpers.scheduleMeeting.meetingWords | C:14802 | [String] | 11 strenger, hele oppgitte intervallet |
| helpers.scheduleMeeting.schedulingWords | C:14803–14804 | [String] | 26 strenger, hele oppgitte intervallet |
| helpers.scheduleMeeting.combinedScore | C:14806 | Double | 0.84 |
| helpers.scheduleMeeting.explicitPhrases | C:14808 | [String] | 2 strenger, hele oppgitte intervallet |
| helpers.scheduleMeeting.explicitScore | C:14809 | Double | 0.86 |
| helpers.project.suppressionMarkers | C:14816 | [String] | 5 strenger, hele oppgitte intervallet |
| helpers.project.publishExclusions | C:14820 | [String] | 6 strenger, hele oppgitte intervallet |
| helpers.project.workSignals | C:14823–14833 | [String] | 9 strenger, hele oppgitte intervallet |
| helpers.project.projectWords | C:14834 | [String] | 2 strenger, hele oppgitte intervallet |
| helpers.project.workScore | C:14836 | Double | 0.88 |
| helpers.project.generalPhrases | C:14838 | [String] | 5 strenger, hele oppgitte intervallet |
| helpers.project.generalScore | C:14839 | Double | 0.78 |
| helpers.project.workspacePhrases | C:14842–14843 | [String] | 16 strenger, hele oppgitte intervallet |
| helpers.project.workspaceScore | C:14844 | Double | 0.8 |
| helpers.ideaCapture.suppressionMarkers | C:14853 | [String] | 5 strenger, hele oppgitte intervallet |
| helpers.ideaCapture.capturePhrases | C:14856 | [String] | 6 strenger, hele oppgitte intervallet |
| helpers.ideaCapture.captureScore | C:14857 | Double | 0.86 |
| helpers.ideaCapture.notePhrases | C:14860 | [String] | 18 strenger, hele oppgitte intervallet |
| helpers.ideaCapture.noteScore | C:14861 | Double | 0.86 |
| helpers.ideaCapture.fallbackTokens | C:14865 | [String] | 2 strenger, hele oppgitte intervallet |
| helpers.ideaCapture.fallbackExclusions | C:14865 | [String] | 1 strenger, hele oppgitte intervallet |
| helpers.ideaCapture.fallbackScore | C:14866 | Double | 0.7 |
| helpers.todo.aiExclusions | C:14873–14882 | [String] | 8 strenger, hele oppgitte intervallet |
| helpers.todo.suppressionMarkers | C:14885 | [String] | 6 strenger, hele oppgitte intervallet |
| helpers.todo.genericPhrases | C:14888 | [String] | 6 strenger, hele oppgitte intervallet |
| helpers.todo.genericScore | C:14889 | Double | 0.78 |
| helpers.todo.listPhrases | C:14892 | [String] | 11 strenger, hele oppgitte intervallet |
| helpers.todo.listScore | C:14893 | Double | 0.84 |
| helpers.todo.rememberPhrases | C:14895 | [String] | 3 strenger, hele oppgitte intervallet |
| helpers.todo.rememberScore | C:14896 | Double | 0.8 |
| helpers.todo.delegatePhrases | C:14898 | [String] | 2 strenger, hele oppgitte intervallet |
| helpers.todo.delegateScore | C:14899 | Double | 0.74 |
| helpers.reminder.suppressionMarkers | C:14906 | [String] | 4 strenger, hele oppgitte intervallet |
| helpers.reminder.directPhrases | C:14909 | [String] | 6 strenger, hele oppgitte intervallet |
| helpers.reminder.directScore | C:14910 | Double | 0.82 |
| helpers.reminder.notifyWords | C:14913 | [String] | 12 strenger, hele oppgitte intervallet |
| helpers.reminder.loseTrackWords | C:14914 | [String] | 5 strenger, hele oppgitte intervallet |
| helpers.reminder.notifyScore | C:14916 | Double | 0.82 |
| helpers.reminder.loseTrackScore | C:14916 | Double | 0.8 |
| helpers.guidedOnboarding.suppressionMarkers | C:14931–14961 | [String] | 29 strenger, hele oppgitte intervallet |
| helpers.guidedOnboarding.gatewayWords | C:14965–14987 | [String] | 21 strenger, hele oppgitte intervallet |
| helpers.guidedOnboarding.statusWords | C:14988–14997 | [String] | 8 strenger, hele oppgitte intervallet |
| helpers.guidedOnboarding.setupWords | C:14998–15019 | [String] | 20 strenger, hele oppgitte intervallet |
| helpers.guidedOnboarding.strongSetupWords | C:15020–15036 | [String] | 15 strenger, hele oppgitte intervallet |
| helpers.guidedOnboarding.gatewayScore | C:15038 | Double | 0.91 |
| helpers.guidedOnboarding.questionnaireWords | C:15040–15055 | [String] | 14 strenger, hele oppgitte intervallet |
| helpers.guidedOnboarding.questionnaireSetupWords | C:15056–15069 | [String] | 12 strenger, hele oppgitte intervallet |
| helpers.guidedOnboarding.questionnaireScore | C:15071 | Double | 0.86 |
| helpers.guidedOnboarding.modelNotConnectedPhrases | C:15074–15080 | [String] | 23 strenger, hele oppgitte intervallet |
| helpers.guidedOnboarding.gettingStartedPhrases | C:15081 | [String] | 8 strenger, hele oppgitte intervallet |
| helpers.guidedOnboarding.modelScore | C:15085 | Double | 0.92 |
| helpers.guidedOnboarding.otherSurfaceWords | C:15089 | [String] | 5 strenger, hele oppgitte intervallet |
| helpers.guidedOnboarding.gettingStartedScore | C:15091 | Double | 0.8 |
| helpers.guidedOnboarding.onboardingWords | C:15093–15103 | [String] | 9 strenger, hele oppgitte intervallet |
| helpers.guidedOnboarding.conferenceWords | C:15104 | [String] | 2 strenger, hele oppgitte intervallet |
| helpers.guidedOnboarding.conferenceScore | C:15106 | Double | 0.9 |
| helpers.guidedOnboarding.onboardingScore | C:15109 | Double | 0.74 |
| helpers.capabilityDiscoveryOnboarding.phrases | C:15116–15128 | [String] | 11 strenger, hele oppgitte intervallet |
| helpers.capabilityDiscoveryOnboarding.score | C:15132 | Double | 0.92 |
| helpers.advisoryReport.suppressionMarkers | C:15247–15261 | [String] | 13 strenger, hele oppgitte intervallet |
| helpers.advisoryReport.advisorPhrases | C:15265–15278 | [String] | 12 strenger, hele oppgitte intervallet |
| helpers.advisoryReport.reportWords | C:15279–15285 | [String] | 5 strenger, hele oppgitte intervallet |
| helpers.advisoryReport.panelPhrases | C:15287 | [String] | 12 strenger, hele oppgitte intervallet |
| helpers.advisoryReport.panelScore | C:15289 | Double | 0.84 |
| helpers.advisoryReport.shortAssessmentPhrases | C:15291 | [String] | 1 strenger, hele oppgitte intervallet |
| helpers.advisoryReport.shortAssessmentPrefixes | C:15291 | [String] | 1 strenger, hele oppgitte intervallet |
| helpers.advisoryReport.shortAssessmentScore | C:15292 | Double | 0.8 |
| helpers.advisoryReport.assessmentPhrases | C:15294–15306 | [String] | 11 strenger, hele oppgitte intervallet |
| helpers.advisoryReport.advisorCombinedScore | C:15308 | Double | 0.92 |
| helpers.advisoryReport.advisorScore | C:15311 | Double | 0.86 |
| helpers.advisoryReport.assessmentReportScore | C:15314 | Double | 0.84 |
| helpers.advisoryReport.assessmentScore | C:15317 | Double | 0.76 |
| helpers.uncertainGoalClarification.suppressionMarkers | C:15353–15375 | [String] | 21 strenger, hele oppgitte intervallet |
| helpers.uncertainGoalClarification.strongPhrases | C:15380–15407 | [String] | 26 strenger, hele oppgitte intervallet |
| helpers.uncertainGoalClarification.strongScore | C:15409 | Double | 0.9 |
| helpers.uncertainGoalClarification.uncertaintyWords | C:15412–15420 | [String] | 7 strenger, hele oppgitte intervallet |
| helpers.uncertainGoalClarification.goalWords | C:15421–15447 | [String] | 25 strenger, hele oppgitte intervallet |
| helpers.uncertainGoalClarification.combinedScore | C:15450 | Double | 0.78 |
| helpers.capabilityGap.suppressionMarkers | C:15547 | [String] | 7 strenger, hele oppgitte intervallet |
| helpers.capabilityGap.explicitPhrases | C:15550–15567 | [String] | 16 strenger, hele oppgitte intervallet |
| helpers.capabilityGap.explicitScore | C:15569 | Double | 0.88 |
| helpers.capabilityGap.gapPhrases | C:15572–15574 | [String] | 20 strenger, hele oppgitte intervallet |
| helpers.capabilityGap.gapScore | C:15576 | Double | 0.8 |
| helpers.capabilityGap.desireWords | C:15578 | [String] | 8 strenger, hele oppgitte intervallet |
| helpers.capabilityGap.productWords | C:15579 | [String] | 12 strenger, hele oppgitte intervallet |
| helpers.capabilityGap.combinedScore | C:15581 | Double | 0.76 |
| helpers.workItem.suppressionMarkers | C:15588 | [String] | 8 strenger, hele oppgitte intervallet |
| helpers.workItem.capturePhrases | C:15591–15617 | [String] | 24 strenger, hele oppgitte intervallet |
| helpers.workItem.captureScore | C:15619 | Double | 0.9 |
| helpers.workItem.productWords | C:15622–15645 | [String] | 21 strenger, hele oppgitte intervallet |
| helpers.workItem.failureWords | C:15646–15675 | [String] | 27 strenger, hele oppgitte intervallet |
| helpers.workItem.failureScore | C:15677 | Double | 0.84 |
| helpers.workItem.fixPhrases | C:15679 | [String] | 3 strenger, hele oppgitte intervallet |
| helpers.workItem.fixWithProductScore | C:15680 | Double | 0.78 |
| helpers.workItem.fixWithoutProductScore | C:15680 | Double | 0.62 |
| helpers.moderation.phrases | C:15687–15698 | [String] | 10 strenger, hele oppgitte intervallet |
| helpers.moderation.score | C:15700 | Double | 0.9 |
| router.specialRules.profilePublish.floor | R:1564 | Double | 0.78 |
| router.specialRules.conferenceAgenda.floor | R:1570 | Double | 0.6 |
| router.specialRules.configurationAuthoring.add | R:1575 | Double | 0.18 |
| router.specialRules.configurationAuthoring.floor | R:1575 | Double | 0.86 |
| router.specialRules.configurationAuthoring.workspaceCap | R:1577 | Double | 0.56 |
| router.specialRules.activityDashboard.add | R:1582 | Double | 0.18 |
| router.specialRules.activityDashboard.floor | R:1582 | Double | 0.94 |
| router.specialRules.adminOperations.add | R:1587 | Double | 0.18 |
| router.specialRules.adminOperations.floor | R:1587 | Double | 0.86 |
| router.specialRules.adminOperations.otherAdminCap | R:1590 | Double | 0.72 |
| router.specialRules.adminCleanup.add | R:1596 | Double | 0.18 |
| router.specialRules.adminCleanup.floor | R:1596 | Double | 0.86 |
| router.specialRules.adminCleanup.workspaceCap | R:1598 | Double | 0.72 |
| router.specialRules.aiGateway.add | R:1605 | Double | 0.2 |
| router.specialRules.aiGateway.floor | R:1605 | Double | 0.88 |
| router.specialRules.kallimachosAdvisor.add | R:1616 | Double | 0.2 |
| router.specialRules.kallimachosAdvisor.floor | R:1616 | Double | 0.88 |
| router.specialRules.adminCredential.add | R:1623 | Double | 0.2 |
| router.specialRules.adminCredential.floor | R:1623 | Double | 0.88 |
| router.specialRules.arendalsukaIntroduction.add | R:1629 | Double | 0.2 |
| router.specialRules.arendalsukaIntroduction.floor | R:1629 | Double | 0.92 |
| router.specialRules.arendalsukaIntroduction.atlasCap | R:1631 | Double | 0.84 |
| router.specialRules.arendalsukaParticipant.add | R:1638 | Double | 0.18 |
| router.specialRules.arendalsukaParticipant.floor | R:1638 | Double | 0.9 |
| router.specialRules.arendalsukaParticipant.atlasCap | R:1641 | Double | 0.84 |
| router.specialRules.dashboardAfterLexicon.floor | R:1657 | Double | 0.96 |
| router.specialRules.dashboardAfterLexicon.architectCap | R:1662 | Double | 0.88 |
| router.specialRules.artistSalesAfterLexicon.artTerms | R:1667–1670 | [String] | 10 strenger, hele oppgitte intervallet |
| router.specialRules.artistSalesAfterLexicon.floor | R:1672 | Double | 0.9 |
| router.specialRules.artistSalesAfterLexicon.cap | R:1678 | Double | 0.74 |
| thresholds.render | C:1862 | Double | 0.6 |
| thresholds.suggest | C:1863 | Double | 0.72 |
| thresholds.autofill | C:1864 | Double | 0.85 |
| thresholds.directResource | C:5377 | Double | 0.82 |
| thresholds.candidateMinimum | C:13746 | Double | 0.5 |
| thresholds.candidateTieTolerance | C:13765 | Double | 0.02 |
| baseWeights.invite | C:14289 | Double | 0.78 |
| baseWeights.poll | C:14291 | Double | 0.76 |
| baseWeights.resourceRouter | C:14293 | Double | 0.72 |
| baseWeights.meetingVideo | C:14295 | Double | 0.62 |
| baseWeights.agentAction | C:14297 | Double | 0.64 |
| baseWeights.scheduleMeeting | C:14299 | Double | 0.62 |
| baseWeights.guidedOnboarding | C:14301 | Double | 0.74 |
| baseWeights.advisoryReport | C:14303 | Double | 0.72 |
| baseWeights.personalAgentPrefix | C:14305 | Double | 0.64 |
| baseWeights.ideaCapture | C:14307 | Double | 0.7 |
| baseWeights.workItem | C:14309 | Double | 0.72 |
| baseWeights.projectTodoReminder | C:14311 | Double | 0.58 |
| baseWeights.capabilityRequest | C:14313 | Double | 0.58 |
| baseWeights.moderation | C:14315 | Double | 1.0 |
| baseWeights.fallback | C:14317 | Double | 0.5 |
| scoring.successIncrement | C:11665 | Double | 0.05 |
| scoring.failureDecrement | C:11665 | Double | 0.04 |
| scoring.rawScaleBase | C:13745 | Double | 0.75 |
| scoring.personalWeightScale | C:13745 | Double | 0.25 |
| scoring.inviteRawScore | C:13729 | Double | 0.86 |
| scoring.pollRawScore | C:13730 | Double | 0.86 |
| scoring.purposeCandidateBase | R:1044 | Double | 0.72 |
| scoring.matchedOrdinalPenalty | R:1044 | Double | 0.04 |
| scoring.genericResourceCap | R:1648 | Double | 0.08 |
| scoring.genericResourceScale | R:1648 | Double | 0.2 |

### Basisvektenes kodebinding

Switch-ordenen i `assistantBaseWeight` beholdes (C:14286–14319). Plassnavnene velger ikke funksjon eller wildcard; koblingen nedenfor står i koden. C:1848–1861 binder konstantnavnene til strengene.

| Plass under baseWeights | Eksisterende purposeRef/predikat |
|---|---|
| invite | personal.chat.assist.invite |
| poll | personal.chat.assist.poll |
| resourceRouter | personal.chat.assist.resource-router |
| meetingVideo | personal.chat.assist.meeting.video |
| agentAction | personal.chat.assist.local-agent-action |
| scheduleMeeting | personal.chat.assist.meeting.schedule |
| guidedOnboarding | personal.chat.assist.guided-onboarding eller conference.participant.onboarding |
| advisoryReport | personal.chat.assist.advisory-report |
| personalAgentPrefix | hasPrefix("personal.agent."), etter foregående grener |
| ideaCapture | personal.chat.assist.idea.capture |
| workItem | personal.chat.assist.work-item.capture |
| projectTodoReminder | personal.chat.assist.project, personal.chat.assist.todo, personal.chat.assist.reminder; tre eksakte refs |
| capabilityRequest | personal.chat.assist.capability-request |
| moderation | personal.chat.assist.moderation |
| fallback | switch default |

Personlig vekt er fortsatt `clamp01(base + successCount × successIncrement − failureCount × failureDecrement)`. Hendelser filtreres på eksakt purposeRef og, når tråd er gitt, samme tråd eller hendelse uten tråd (C:11652–11677). Råscore vektes som `clamp01(raw × (rawScaleBase + personalWeight × personalWeightScale))` før minimum og sortering (C:13740–13768). Hendelsene og beregnede personvekter er **ikke** grafdata. `learningEnabled` stanser nye hendelser (C:13809), men gamle vekter leses fortsatt (C:14445–14454).

## 5. De 18 kodekontraktene som beholdes

| ID | Fil:linje | Beholdt semantikk og grunn |
|---|---|---|
| K01 | R:914–926, 2279–2303 | Leksikonfilter, phrase-OR / all-token-groups, endpointlikhet, metadata-substring og første formålslås. Ingen tolker. |
| K02 | R:1999–2056, 2256–2267 | Normalisering, camel case, Locale.current, stavekorreksjoner, stoppliste og semantiske tokenaliaser. Beholder tekstsemantikken. |
| K03 | R:1040–1046, 1551–1688 | Filtrert rekkefølge, enumerering, særregelgrener, operasjonsrekkefølge, post-regler, kontekst og sluttklamping. Tall leses fra navngitte plasser. |
| K04 | C:14714–14919, 14929–15133, 15245–15320, 15351–15454, 15545–15703 | De 15 hjelpernes if/guard/ternær, AND/OR, første retur og 0/false. Ingen maks-aggregator eller globalisering av lokale unntak. |
| K05 | C:14732 | Invitasjonsregex på originaltekst med stor forbokstav; regextekst og options blir kode. |
| K06 | C:14754–14767, 14864–14866, 15916–15921 | Poll-tokenisering vs intentTokens; lengde ≥ 3 og stoppliste bare i sistnevnte. Ide-unntaket gjelder bare fallback. |
| K07 | C:14922–14927 | mentionsClockTime med tre regexer og tidfraser blir predikatkode, med uendret input. |
| K08 | C:13544–13548, 14850–14852 | normalizedAssistantText/ide bruker nb_NO-folding; andre hjelpere bare lowercase. Ingen felles normalisering innføres. |
| K09 | C:15705–15708, 15746–15789 | suppressesIntent: idiomer fjernes, globale/historiske stopp, første markørforekomst og 36 tegns prefiksvindu med ordtest. Hjelpermarkører flyttes; predikatets egne tabeller beholdes. |
| K10 | C:14988–15038, 15070–15111 | Status og oppstart er kodepredikater med lokale unntak. Ingen dataevaluert predicate-name. |
| K11 | C:13715–13768, 14408–14442 | Kandidatkobling, utvalgt max med signaladapter, støttet intent, moderation-prioritet og intentPriority: 100/80/75/72/70/65/64/64/63/62/61/60/55/50/30/0 i switch-orden. Toleransefelt flyttes; sammenligningen < beholdes. |
| K12 | C:11652–11677, 14286–14319, 14445–14454 | Vektformel, switch, trådfiltrering, klamping og lesing av gamle hendelser; persondata blir hos eieren. |
| K13 | C:13801–13822 | Registreringsbryter og eierscope. E1 gjør ikke observerte klikk eller taushet til nytt læringsgrunnlag. |
| K14 | C:5377, 5434–5566, 7825 | Terskelbruk, endelig valg, avklaringsantall og autofyll. Tall flyttes, ikke betingelser eller handlingstilgang. |
| K15 | R:514–528, 1682–1687 | Perspective: ready/empty/unavailable, formål eksakt 0,16/token 0,05, interesse eksakt 0,07/token 0,03, tak 0,24. Beholdt i kode, ikke nye grafparametre i første runde. |
| K16 | R:1444–1469, 1573–1641 | Målflatenavn, endpointkonstanter, isArendalsukaParticipantPurpose og Atlas-vedlikeholdsfraser. Targetvalget og operasjonene er kode. |
| K17 | Sources/ScaffoldKit/AdminControlPlaneRouting.swift:216–222 | To lukkede miljøbindinger løses med eksisterende funksjon. Dekoder kan ikke slå opp vilkårlig kode eller godta en ny adresse som binding. |
| K18 | C:14321–14350, 13742–13758; R:1690–1698 | Handlings-keypaths, descriptor, risiko og tilgjengelighet er fortsatt kode/kontrakter. En score, import eller purposeRef gir aldri en Grant. |

## 6. Fire uttrekksområder som står over i første runde

| ID | Område | Grunn og videre avhengighet |
|---|---|---|
| U01 | agentActionMatch, alle tabeller og råscore 0,88 | Descriptor og katalogvalg må kartlegges samlet før uttrekk; alle grener er listet i §3. |
| U02 | butlerSignalIntentScores, minimum 0,62, løft 0,70, specificity 3 og underliggende matcher/katalog | Annen returtype og egen datakilde; eksisterende adapter beholdes. Krever egen avgrenset kartlegging. |
| U03 | PurposeKnowledgeBase runtime-noder, aliasindeks og matcher | K:7–31, 92 ff., 588–648, 997–1016. Book bruker goal.goalRef og matchingHints; runtime har flatere felt og egne tekster/tokens. Å lagre Book-snapshot bytter ikke runtime-forbruker eller løser WP1/WP2/WP4/WP19. |
| U04 | Øvrige ruter-/ressurstabeller og parametre utenfor uttrekket | R:1208–1438 låste flater (0,88/0,86/0,87/0,89/0,93); R:1494–1545 lexicalScore, eksakt identifier +0,32/gulv0,86, flate/RAG +0,10, Arendalsuka +0,75/−0,20, docs-tak0,26, entity +0,34/+0,08. Resten av ressursruting/-rangering i R:1700–1998 beholdes også. Senere uttrekk krever eget kart. |

Startversjonen er et avgrenset uttrekk. b1a må ikke rapportere at «alle frasetabeller» er borte eller at én motor er etablert. Før/etter-kallgraf skal vise de samme aktive matchveiene. Literal-søk viser bare hvilke plasser som faktisk ble flyttet.

## 7. Noder, proveniens og byggføringer

Nodedelen er `content.knowledgeBase`, med Book 23-objektet bevart. Den er ikke en syntese av leksikonet: mange ruterrefs mangler `purpose://`, og flere prefiksede refs finnes ikke i Book-snapshotet. `lexicon[].purposeRef` bevarer konsument-ID-ene; ingen automatisk prefiksing, alias, parentRef eller Goal. Nye registernoder går gjennom registerets forsoning. Butler-parametre bor i `consumerFacets.butler`, ikke i nodenes semantiske `facetRefs`.

b1a låser SHA og filhasher, kopierer råverdier tapsfritt, fjerner akkurat de flyttede literalene og gir hvert analyzeDraft ett festet snapshot før første await. Samme snapshot følger reruting og senere beregninger. Forslaget får contentHash, evaluator-/predikatversjon og stabile regel-ID-er, eksempelvis `lex.05`, `S02` og `helper.scheduleMeeting.combined`. Trace-ID-ene bestemmes av kodegrenen, ikke dynamisk funksjonsoppslag. Utsatte veier får også kodeproveniens.

Importvalidering, semantisk differanse, tilgangsporter og WP8-forutsetninger står i [flytteplanen](E1-MIGRERING-TIL-REGISTER.md). Manglende registerkontrakt stopper kildebyttet, ikke denne dokumentleveransen eller det avgrensede Butler-uttrekket.

## 8. Innspill til E2+

Dommerbenken a02 (Perspective-kontekst og setningsdekomponering), a05 (sjekke hvilke formål brukeren forfølger) og a06 (flere behov i én melding) føres videre som innspill til E2+ og senere forståelsesarbeid. De endrer ikke E1. Eksisterende Perspective-bruk bevares; E1 skal gi identiske beslutninger.

## 9. Verifikasjon av dokumentleveransen

Utført 2026-09-29:

- 27 leksikonoppslag og 7 felt hver kontrollert gjennom uttrekk fra git-objektet; alle 182 øvrige parameterverdier sammenlignet med eksakte kildeintervaller. Sum 371 plasser.
- JSON Schema Draft 2020-12 metaschema og kompilering godkjent med lokalt tilgjengelig Ajv 8.17.1. En komplett testverdi bygget i minne fra de 27 kildeoppslagene, parameterverdiene og Book-kildens 58 noder validerte.
- 10 negative formatprøver avvist: ukjent hjelper, tom tokengruppeliste, tom tokengruppe, duplisert entryID, ukjent endpointbinding, sammenblandede hintfelter, blank frase, score utenfor intervallet, ugyldig hashformat og flat goalRef i stedet for Book-goal. To positive prøver godtatt: omordnet leksikon og tom endpointHints. Omordningen krever fortsatt ny hash og semantisk evaluering.
- Alle lokale skjemareferanser og relative dokumentlenker løst; de tre nye filene skannet uten funn av IP-adresser, e-postadresser, konkrete personidentifikatorer eller brukerstier.
- E1-DESIGN er byteidentisk etter første linje; SHA-256 for den bevarte delen: d9aa9746651d30972e60fedc3d0e875232bd4dc3edf1aafaa8672ced7b897bcd.

Formatprøven brukte en plassholderhash og verifiserte bare hashens format. Ingen JCS-implementasjon, runtime-paritet, ekte celleoperasjon eller migrering er testet i denne dokumentjobben. Den felles kontrakttesten i flytteplanen er fortsatt et krav til b1a/WP8. Ingen kodeendring, commit, push eller PR er gjort.
