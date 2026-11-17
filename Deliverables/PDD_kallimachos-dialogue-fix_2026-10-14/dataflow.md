# Faktisk dataflyt som testes

`setDraftQuestion` + `setRelationID` → Advisor `ask` → scope-avgrenset kontekst/referanseavklaring → CommonsLibrarian `catalogQuery` (public-only) → evidensport → tillatt lokal rute → AIGateway `invokeAI` med denyAll → loopback `/v1/chat/completions` → validering → svar eller `answer-rejected` med deterministisk grunnlag.

Bare validerte svar lagres som kontekst. `deleteHistory(confirm: true)` → CommonsLibrarian `auditDelete` for samme requester/relation → kvittering → fjern samme dialogscope. Ingen modell kan kalle dette verktøyet.
