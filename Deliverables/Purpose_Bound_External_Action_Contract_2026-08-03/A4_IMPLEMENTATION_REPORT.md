# A4-v1 — implementasjonsrapport

Dato: 2026-08-03  
Status: **implementert og testet for én avgrenset provider-invocation-bane; ikke generell egressdekning**

## Resultat

Den anbefalte rekkefølgen er gjennomført uten per-Grant-utvidelse:

1. `Agreement.authorizationPolicyBinding` binder en statisk, versjonert
   policy-ceiling til issuer-signerte Contract-bytes.
2. Per-use formål, handling, destinasjon, datamanifest, plan, config, policy,
   taksonomi og faktisk payload holdes i separate action-objekter.
3. En ren, deterministisk evaluator krever både eksisterende Cell-authority og
   eksakt action-ceiling.
4. `PurposeBoundAIGatewayCell.ai.invokePurposeBound` håndhever én ekstern
   provider-effekt før credentialoppslag og provider-kall.
5. En egen Cell/Agreement-overflate isolerer policybindingen fra legacy
   AIGateway-grants uten flere templates eller per-Grant-utvidelse.

Dette er ikke en ny authority-modell. Evalueringsregelen er fortsatt:

```text
existing Cell authority
AND exact signed/installed policy ceiling
AND exact observed action facts
= allow for one effect
```

Formål, CellConfiguration-policy og tillitspakke kan bare gjøre resultatet
smalere. Ingen av dem kan gjøre en eksisterende denial til allow.

## Implementerte kontrakter

### Statisk Agreement-binding

`AuthorizationPolicyBinding` ligger på Agreement-nivå og inneholder:

- schema og canonicalization-versjon
- policy-ID og policyversjon
- SHA-256-binding til policy, resolved config-profil og taksonomi
- én action-familie

Bindingen er med i `Agreement`-kodingen, Contract-signaturens payload og
Contract-dedupliseringsnøkkelen. Eldre Agreement uten feltet dekodes med
`nil`. En Contract med manglende eller avvikende binding kan ikke brukes mot
en bundet template, og en endret template-binding gjør tidligere Contract
ubrukelig ved neste authorization check.

Bindingen er en ceiling-referanse, ikke en Grant.

### Dynamiske action-objekter

CellBase har runtime-modeller for alle fire wire-objektene:

- `PurposeBoundActionIntent`
- `CellExecutionPolicy`
- `PurposeAuthorizationContext`
- `ActionDecisionReceipt`

`PurposeBoundActionAuthorizer` er en ren funksjon. ID-er og tidspunkt kommer
inn som eksplisitte input, slik at identiske input gir identisk resultat.
Evalueringsresultatet skiller `decisionStatus` fra `executionStatus`.

Authority-evidens fra `CellAuthorizationDecision` kan nå peke på den eksakte
Agreement-, Contract- og Grant-referansen som faktisk matchet. En denial uten
authority bruker `authorityPath=none`; den oppdikter ikke en owner- eller
Contract-vei for å få et schema-valid objekt.

### Digestprofil

`PurposeBindingDigest` bruker SHA-256 med domene-separasjon og
lengdeprefiksede komponenter. Dermed kan for eksempel `['ab','c']` ikke
kollidere semantisk med `['a','bc']`, og samme bytes i purpose- og
payload-domenet får forskjellige bindinger.

AIGateway-profilen recomputerer observed bindings fra den faktiske requesten
før bruk:

| Binding | Faktisk input |
| --- | --- |
| purpose | fast, eksakt primary-purpose-ref |
| action | `provider_invocation` og eksakt action-ref |
| destination | provider, trusted endpointvalg, API-path og modell |
| data manifest | prompt og eventuell systeminstruksjon som eksplisitte dataklasser |
| plan | én route; ingen planning, fan-out, tools, metadata eller route-context |
| config | den kompilerte, resolved purpose-bound AIGateway-profilen |
| policy | policy-ID, versjon, invariants, ceilings og godkjente destinasjoner |
| taxonomy | purpose-, action-, data-class- og destination-refs |
| payload | AIGateways kanoniske requestrepresentasjon |

Receipts inneholder digests og reason codes, men ikke prompt, output eller
credentials.

## Avgrenset AIGateway-policy

Den nye banen er `cell:///PurposeBoundAIGateway` / `ai.invokePurposeBound` med:

- primary purpose: `purpose://ai.assistance.answer-user-prompt`
- action: `action://haven/aigateway/invoke-approved-provider`
- nøyaktig én hosted provider-route
- godkjente destinations: OpenAI, Anthropic eller Mistral gjennom eksisterende
  trusted HTTPS-egresspolicy
- data: user prompt og valgfri systeminstruksjon
- ingen planning, orchestration, fan-out, tools, metadata eller route-context

Clienten lager intent før kall. Runtime kontrollerer intentets synlige fakta,
recomputerer alle observed digests og kjører Cell-authorisasjon på
`ai.invokePurposeBound`. Først etter allow kan secret store leses.

Policy-evaluerte avslag gir authorization context og decision receipt med
`executionStatus=not_attempted`. En strukturelt ugyldig forespørsel som
avvises av API-preflight før det finnes et schema-valid intent, gir vanlig
diagnostikk og ingen oppdiktet context eller receipt.

En aktuell tillitspakke kan legges ved som evidensref. Den har alltid
`confersAuthority=false`. En outsider med en «current» tillitspakke blir
fortsatt avvist før credentialoppslag.

Cache lagrer ikke authorization context eller receipt. Ved cache hit lages en
ny beslutning for aktuell requester/intent, og execution står som
`not_executed`.

## Agreement-konsekvens og valgt isolasjon

Dette var den viktigste arkitekturkonsekvensen av Agreement-level binding:

`GeneralCell` har én `agreementTemplate` per Cell. Den første A4-versjonen la
bindingen i den blandede AIGateway-template-en og koblet dermed invocation-,
state- og setup-grants til samme policyversjon.

Dette er nå løst med den minste komplette isolasjonen:

- `cell:///AIGateway` er igjen ubundet og annonserer ikke purpose-keypathen
- `cell:///PurposeBoundAIGateway` har nøyaktig ett Grant på
  `ai.invokePurposeBound` og eksakt policybinding
- et requester-Agreement som blander inn `state` eller en annen grant-familie
  avvises av eksisterende template-subset-kontroll
- begge profiler kanoniseres ved reload; eldre blandede persisted templates
  videreføres ikke
- policybindingen er løftet til `1.1.0` fordi Cell-endepunkt og action-keypath
  nå inngår i digest-en; eventuelle `1.0.0`-signerte Agreements/Contracts må
  utstedes og signeres på nytt, ikke muteres på plass

Provider-motoren deles, men autorisasjonsprofilen bestemmes av konkret Cell-type
og kan ikke velges i requesten. Flere Agreement-templates ville krevd ny
protokollflate for admission, signering, persistens og use-time matching og ble
derfor ikke valgt. Se
[beslutningen om Agreement-isolasjon](A4_AUTHORITY_ISOLATION_DECISION.md).

Per-Grant V2 er fortsatt lukket til en konkret use case krever flere
forskjellige policy-scopes i samme Contract.

## Testevidens

CellProtocol:

- Agreement round-trip med og uten binding
- ukjent felt og ukjent binding-schema avvises
- Contract-signatur og deduplisering endres ved binding-tampering
- mismatch ved Agreement-utstedelse avvises
- policyendring tilbakekaller tidligere utstedt Contract
- deterministisk allow og separat execution-status
- trust package uten authority avvises
- owner kan ikke omgå destination/binding-ceiling
- Contract-path krever Agreement-, Contract- og Grant-ref samt eksakt binding
- ukjent purpose og facet-only treff feiler lukket
- digest framing er domene-separert og entydig
- Unicode-tegn avvises der kontrakten krever ASCII digest- og purpose-tokens

CellScaffold/AIGateway:

- positivt provider-kall returnerer eligible context og completed receipt
- payload-endring etter intent gir denial før credentialoppslag
- current trust package kan ikke autorisere outsider
- flere routes avvises før credentialoppslag
- cache gjenbruker ikke en tidligere receipt
- dedikert Cell har eksakt ett Grant og ett Explore-keypath
- mixed-grant Agreement avvises, mens smalt Agreement godtas
- legacy og purpose-bound templates normaliseres korrekt etter persistens
- direkte kryssbruk av authority-flater avvises før credential- og providerbruk
- eksisterende 39 AIGateway-regresjonstester er beholdt; Explore-manifestene
  verifiseres separat for legacy- og purpose-bound-flaten

Verifikasjonsstatus 2026-08-03:

- 31 målrettede Agreement-, GeneralCell- og purpose-bound tester: bestått
- 47 AIGateway-tester: bestått
- full CellProtocol-suite: 875 av 876 tester bestått; eneste feil er den
  separat reproduserbare
  `ChatCellTests.testAudienceGroupPresentationIsViewerRelativeBoundedAndDeterministic`
  i allerede modifiserte Chat-filer utenfor A4-endringsflaten
- schema-, fixture-, semantikk- og Markdown-linkvalidering: bestått

## Restscope og påstandsgrense

Følgende er uttrykkelig **ikke** dekket av A4-v1:

- legacy `ai.invoke`, `invokeAI` og `invokeDraft`
- multi-route, voting, swarm, adjudication og planner/executor
- lokale modeller
- script/subprocess, filer, bridges og andre nettverksadaptere
- full JSON Schema 2020-12-validering i runtime
- kryptografisk signert, separat policy-publication utenfor Contract-bindingen
- retention/deletion-kontroll hos en provider etter disclosure
- generell replaybeskyttelse for eksterne effekter

Derfor er den korrekte påstanden: *HAVEN har nå en testet, formålsbundet
provider-invocation-profil for én AIGateway-keypath.* Det er ikke korrekt å si
at all AI-egress eller alle AI-verktøy er formålsbundet.
