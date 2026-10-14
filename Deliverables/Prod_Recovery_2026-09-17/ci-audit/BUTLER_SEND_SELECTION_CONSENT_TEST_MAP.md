# Butler Send: eksisterende UI-kontrakt og gjenbrukbare tester

Leserevisjon 2026-09-18. Kandidat `/private/tmp/haven-prod-20260917/CellScaffold`. Ingen kildefiler, Git, bygg, tester, secrets eller modellaktivering berørt. Bare rapporten er skrevet. Kildeanker gjelder den observerte kandidaten; root arbeider samtidig.

## Konklusjon

Backend-kontraktene for eksplisitt providerkall og samtykke finnes. Det finnes **ikke** et lagret bruker-valgt providerID eller tilhørende consentID i Butler UI-state, og ingen fullført samtykke-UI foran vanlig Send. «Velg beste provider» rangerer; «Spør valgt modell» sender tom payload og velger første kallbare kandidat. AIGateway-draft er et eget valg av leverandør/modell, men er ikke koblet til dette chatvalget. Ikke presenter disse tre som én eksisterende fungerende kontrakt.

## Det som kan gjenbrukes uten ny rendererfunksjonalitet

| Eksisterende kontrakt | Kildeanker | Viktig egenskap |
|---|---|---|
| `chatHub.prompt.submit` | PersonalCopilotCells.swift:1419; CloudStore:4876 | Normal Send; ruter Porthole-/hjelperhandlinger først. payloadWithModelRouteContext:844 bevarer alle eksisterende objectfelter. |
| `chatHub.assistant.provider.invoke` | PersonalCopilotCells.swift:1533; CloudStore:6519 | Tar prompt, providerID, purposeRef, dataCategories og consentID; kjører gate med requireConsent:true ved6646. |
| `chatHub.assistant.provider.recommend` | CloudStore:6458 | Lagrer rangerte matches, ikke eksplisitt valg. |
| `assistantProfile.profile.setProviderPolicy` | PersonalAssistantProfileCell.swift:382 | localOnly eller askBeforeExternal; sistnevnte er tillatelse til å spørre, ikke til å sende. |
| `assistantProfile.profile.registerProviderTrustPacket` | samme fil:404 | Krever confirm:true og validert pakke. Ingen providerkall. |
| `assistantProfile.profile.grantProviderConsent` | samme fil:440 | Krever confirm:true, eksisterende gyldig pakke, provider/modell/formål/datakategorier. |
| `assistantProfile.profile.revokeProviderConsent` | samme fil:480 | Eksplisitt tilbakekalling. |
| List-valg og dynamisk knappepayload | ConfigurationFactory:1316–1324,1428–1445,1737–1743 | Eksisterende SkeletonList.selectionActionKeypath/selectionPayloadMode og Button.payloadKeypath er nok. |

Profil-state lagrer `providerTrustPackets` og `providerConsents` som objekter (PersonalAssistantProfileCell:44–70,105–108). Samtykkeskjema finnes i PersonalAIProviderPolicy:127–157. Minimal payload til grant-handlingen, med verdier som faktisk er valgt og vist:

```json
{
  "confirm": true,
  "consentID": "<ny identifikator for denne bekreftelsen>",
  "providerID": "<chat-descriptorens id, ikke vilkårlig provider-navn>",
  "modelID": "<valgt modell>",
  "purposeRef": "<vist formål>",
  "dataCategories": ["<faktisk kategori for innholdet>"],
  "trustPacketRef": "<eksisterende validert pakke>",
  "useScope": "singleUse",
  "expiresAt": "<kort, vist utløp>"
}
```

Grant-handlingen støtter også untilExpiry, men singleUse er den minste eksplisitte sendingen. Utelatt utløp gir nå 15 minutter. Vis mottaker/modell, hvilke data som sendes, formål og pakkens faktiske lagrings-/trenings-/kostopplysninger før bekreftelse. Ingen ekte kildeverifisert pakke ble funnet eller opprettet av denne revisjonen. Testenes example.invalid/source_audited-fixtures er ikke produksjonsgrunnlag.

## Små, men nødvendige appkoblinger

1. `PersonalCopilotChatUIState` (CloudStore:967–1000) mangler valg og samtykkereferanse. `chatAssistantStateObject` (11180–11230) eksponerer bare matches, første recommendation, tidligere invocation og receipts. Legg et eksplisitt valg i riktig requester/tråd-scope, med rute/modellbinding; ikke bruk matches.first eller forrige invocation som brukerens valg. En smal ny selection-action er nødvendig hvis valget skal overleve mellom klikk og Send; det finnes ingen slik action å koble listen til i dag. `assistant.selectCandidate` gjelder personer, ikke modeller.
2. `selectedInvokableProvider` (9518–9528) faller tilbake til første provider også når et eksplisitt requestedID ikke finnes. Ukjent/stale eksplisitt ID skal avvises uten fallback. Valget skal valideres mot fersk eier-scoped descriptor/rute før samtykke og igjen ved sending.
3. Koble valgt consentID til den valgte ruten, og gjenbruk `invokeChatAssistantProvider` fra normal `submitChatPrompt` etter eksisterende global/hjelper-routing. Profile gate skal fortsatt validere policy, providerID/modelID, formål, datakategorier, trustPacketRef, expiry, revocation og singleUse (Policy:374–415). Ikke kjør tolknings-grantbanen i tillegg til samme samtalekall. En ny consent-knapp kan kalle eksisterende profilhandling, men må ikke gi samtykke som følge av anbefaling/nøkkellagring.
4. Butler-konfigurasjonen har ikke `assistantProfile`-cellreference: additionalReferences:402–405 inneholder AgreementWorkbench, Spatial og Perspective. Profilens eksisterende policyknapper:2899–2900 er i den separate «Personal Assistant Profile»-flaten, descriptor:700. En direkte profilknapp inne i Butler trenger den faktiske cellreferansen; alternativt en smal chat-wrapper som kaller den eksisterende profilen med samme requester.
5. Send-knappen (Factory:1775) sender `{}`. Enter (Public/js/porthole-webo.js:8805–8823) lager bare draft/body/text, mens vanlig Send payload-resolver:8927–8932 bevarer ekstra objectfelter. Bare payloadKeypath på knappen løser derfor ikke Enter. Serverlagret eksplisitt valg/samtykkereferanse gjør begge innganger konsistente; begge skal revalidere før kall. Bevar én synlig Send og eksisterende composerdata.

## Gjenbrukbar testkode og eksakte hull

- **Chat gjennom resolver og faktisk gateway:** `PersonalCopilotV1Tests.testChatAssistantInvokesExplicitScopedProviderAfterUserAction`:4056. Bruk samme owner, PersonalChatHubCell, resolverregistrering og encodedValue-helper. Den eksisterende testen sender allerede en typed request via providerPayload:4101–4118, men omgår feilbanen der chat selv skal bygge fra state.draft. Erstatt i en ny test med konfigurert gateway-draft og bare vanlig prompt.submit/valgt ID. NB: eksisterende testprovider er deklarert local kun som syntetisk fixture; en ekstern samtykketest må bruke external og faktisk profilpakke/samtykke-fixture.
- **Chat-stub:** `PersonalCopilotAIGatewayProviderStub`:5218 i samme fil registrerer callCount/lastPrompt. Den er file-private. Legg eventuelt til lastRoute/lastRequest og kontrollert error der for ende-til-ende assertions; ikke flytt produksjonskoden inn i testen. `registerResolveIfNeeded`:2857 gir identityUnique/ephemeral testregistrering.
- **Rik gateway-stub:** `AIGatewayCellTests.StubProvider`:2742 har outputs, outputSequences, .success/.failure, callCount, lastRoute, lastSecret, promptsByProvider og systemPromptsByProvider. File-private; nye tester i samme fil kan gjenbruke den direkte. `CountingSecretStore`:2818 kan bevise null credentialoppslag før avvisning; StubQuotaAuthorizer:2832 har prepare/commit/rollback-tellere. setUp/tearDown:24–41 resetter factories.
- **Draftbevis:** AIGatewayCellTests:914 (`testInvokeDraftCarriesLocalTimeoutToProviderRoute`),2119 (`testInvokeDraftUsesSessionCredentialAndUpdatesSetupState`) og2161 (`testInvokeUsesOwnerScopedCredentialCellSecret`). Gjenbruk `configureDraftForTesting`:AIGatewayCell3400, `stateValueForTesting` og syntetisk owner store. Ny chat-test skal assert aktuell prompt (ikke gammel draft.prompt), providerID, model, baseURL, apiPath, apiStyle, alias, timeout og én rute; konfigurer avvikende miljø-default/fallback og assert at de aldri brukes.
- **Samtykke:** `PersonalAssistantProfileCellTests.testOwnerRegistersAuditedTrustPacketAndCanGrantThenRevokeConsent`:162 er faktisk profil-action-fixture. `PersonalAIProviderPolicyTests`:38,69,101 tester match/utløp/singleUse/revocation; provider/trustPacket/consent/profile-helperne ligger130–205. Kombiner disse med chat-stub i ny ekstern normal-Send-test: før bekreftelse null kall, etter ett gyldig singleUse-samtykke ett kall, neste sending null nye kall. Policy default/private avvisning finnes også i PersonalCopilotV1Tests:4143.
- **Feilmapping:** AIGatewayCellTests:2036 (`testFailureRedactsSecretAndRollsBackQuota`),2405 (`testQuotaExceededUpdatesQuotaStatusAndSetupState`) og1542 (`testSettlementFailureFailsClosedAfterProviderSuccess`). AIGateway.failureResponse:3044 setter outputText=nil og diagnostics.errors, men ingen generisk success=false. Chat6813–6830 merker i dag alle ikke-nil resultater invoked. Ny chat-test må bevise failure/timeout/quota/missing credential gir success=false, redigert feilmelding og ingen falsk modelsvarrad; bare gyldig output gir invoked. Ikke behandle diagnostics.errors eller denial-string som et modelsvar.
- **UI-innganger:** `playwright/skeleton-textarea-submit.spec.js` dekker generell Enter, og `playwright/arendalsuka-onboarding-matching.smoke.spec.js:435` har clickAndReadPortholeAction for chatHub.prompt.submit. Legg én konkret Send/Enter-likhetstest på den samme eksplisitte selection/consent-scopen, pluss eksisterende helper-routingtester (PersonalCopilotV1Tests:1494,1573,2595).

Dette er en plan og et testkart, ikke resultat av utførte tester eller en bekreftelse på at noen produksjonsmodell er tilgjengelig.
