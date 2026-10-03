# Butler A1 — rød baseline, runde 3

Kjørt 2026-09-29; avsluttet 14:34:06Z. Kun test- og dokumentendringer mot
CellScaffold `adf48d4615d1ed143d5bdc190fcf63e266214c8f`.
Produksjonskode og pakkepinner var uendret både før og etter kjøringen.

```sh
scripts/run_swift_bounded.sh test --disable-sandbox --filter 'GuidedOnboarding|PersonalCopilot'
```

- Exit 1 etter vellykket kompilering og fullført testkjøring.
- 149 tester: 133 passerte og alle 16 nye tester feilet.
- XCTest rapporterer 17 feil i 16 tester: chat-testen har to mislykkede asserts.
- GuidedOnboardingFailureReasonTests: 5 tester, 3 feilet, 4 feilregistreringer.
- PersonalCopilotRestorationTests: alle 13 feilet med `notFound` ved første gjenopprettede `purposeGoal`-lesing.
- GuidedOnboardingCellTests: 18 passerte. PersonalCopilotV1Tests: 76 passerte.
- Bygg: 1245,99 s. AppTests-testkjøring: 950,825 s.
- Ingen skip-argumenter eller exclusions brukt i denne kjøringen.

Maskert utdrag fra den nye chat-testen:

```text
guided onboarding onboarding.start failed: guided_onboarding_step_rejected — onboarding.start: notFound
```

De to andre nye onboarding-testene kastet `notFound`.
Eierkontrollen i den ferske direkte cellen passerte. Sikkerhetsassertene i
søstersuiten ligger etter den første gjenopprettede lesingen og ble derfor ikke
nådd; denne røde kjøringen er ikke bevis for at hele avvisningsregresjonen passerer.

## Feilende tester

- `GuidedOnboardingFailureReasonTests testChatOnboardingActionStartsRestoredCellWithExactConnectButtonPayload`
- `GuidedOnboardingFailureReasonTests testRestoredOnboardingRejectsSameOwnerUUIDWithDifferentSigningKey`
- `GuidedOnboardingFailureReasonTests testRestoredOnboardingStartsForProvedOwnerWithoutDefaultVault`
- `PersonalCopilotRestorationTests testRestoredAccountContinuityChatHub`
- `PersonalCopilotRestorationTests testRestoredAgentCapabilityBroker`
- `PersonalCopilotRestorationTests testRestoredAgentSetup`
- `PersonalCopilotRestorationTests testRestoredAssistantProfile`
- `PersonalCopilotRestorationTests testRestoredChatHub`
- `PersonalCopilotRestorationTests testRestoredConfigurationCatalog`
- `PersonalCopilotRestorationTests testRestoredExecutablePurposeGrounding`
- `PersonalCopilotRestorationTests testRestoredMatchmaking`
- `PersonalCopilotRestorationTests testRestoredMeetingCoordinator`
- `PersonalCopilotRestorationTests testRestoredPersonalPagePublisher`
- `PersonalCopilotRestorationTests testRestoredProfilePublisher`
- `PersonalCopilotRestorationTests testRestoredPublicProfileDirectory`
- `PersonalCopilotRestorationTests testRestoredQuestionnaireResponse`

## Proveniens

- Plattform: Darwin arm64, Apple Swift 6.4, target arm64-apple-macosx27.0.0.
- CellProtocol: `9c60001ac53abc35ba7ad6e2c0efa2a79ab2a366` (2026.9.3).
- DiMyMicropayments: `aa3d10d17b90f692e50343232961c3dfd8a66323` (2026.9.3).
- DiMyMint: `2dcefac5c21a0b54e4e8677452d591b6169c2057` (2026.9.3).
- Package.resolved SHA-256: `422c542703d177dc35b5c1a2672ed884078a580584351fab615a334a649cf183`.
- Lokal rålogg, filnavn `butler-a1-runde3-red.log`, SHA-256:
  `fed11d12c33c2c81c6db9fd7dfb840e8b61784866200bdc44b2b715c2c877471`.
  Råloggen beholdes lokalt i maskinens midlertidige katalog og publiseres ikke.

## Kapasitet

Start: 62,9 GiB ledig; uendret vakt godkjente kjøringen.
Runnerens sluttmåling: cache 9758396 KiB, cachevekst 6555052 KiB,
endring i ledig plass -7600000 KiB. Ingen håndskrevet markør eller alternativ cache.

Før videre arbeid avviste `scripts/check_build_capacity.sh .` med exit 75:

```text
Build capacity: 55.7 GiB free (6%); reserving 10 GiB leaves 45.7 GiB (4%).
ERROR: build blocked: projected free space must remain at or above 40 GiB and 5%.
```

En etterfølgende ren `df`-avlesning viste 56,458 GiB, som viser at kapasiteten
svinger. Vakten ble ikke forsøkt på nytt: Kjetils beskjed var å stoppe når den
blokkerer. Ingen produksjonsretting, ettertest, commit, push eller PR i runde 3.
