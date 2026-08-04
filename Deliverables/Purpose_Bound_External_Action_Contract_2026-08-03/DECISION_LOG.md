# Beslutningslogg og A4-handoff

Dato: 2026-08-03  
Status: normative valg for A1; åpne runtime-spørsmål er ikke stilletiende
avgjort.

## Beslutninger

| ID | Beslutning | Begrunnelse | Konsekvens |
| --- | --- | --- | --- |
| D1 | Formål kan bare innsnevre authority. | Agreement er ikke grant og formål er ikke capability. | Ingen model/dekomponering kan mint'e access. |
| D2 | Én `PurposeBoundActionIntent` har nøyaktig én ytre effekt og ett primært formål. | Hindrer at en tilsynelatende ufarlig plan skjuler flere effekter. | Multi-step agentplaner splittes og reautoriseres. |
| D3 | Primary-purpose match er exact-only i v1. | Taxonomy-parent og semantisk likhet er for vide security-primitiver. | Parent/child-delegation er et fremtidig, versjonert valg. |
| D4 | Facets er non-authorizing. | Privacy/quality/validation er begrensninger, ikke permissions. | Facet treff kan aldri åpne action ceiling. |
| D5 | Config policy er ceiling, ikke grant. | Hindrer at AI-generert eller feilkonfigurert UI blir authority. | Contract/Grant/owner path må fortsatt valideres. |
| D6 | Owner path kan ikke bypass'e ekstern ceiling. | Egress krever ekstra vern selv når eier utfører handling. | Negativ test er implementert i CellBase og på AIGateway-banen. |
| D7 | Trust package/consent er evidens og condition-input, ikke capability. | Dokumentasjon uten enforcement er tillitsteater. | Receipt må angi authority path separat. |
| D8 | `s` og disclosure er uavhengige. | Retention og utlevering har forskjellig skadeflate. | To policy- og authority-kontroller kreves. |
| D9 | Digest-settet binder alle vesentlige deler. | Hindrer substitution og preview-to-execution drift. | Canonicalization er et nødvendig A4-delprosjekt. |
| D10 | `allowed` er ikke `executed`. | En policybeslutning beviser ikke transport/mottak. | Receipt har eget execution-statusfelt. |
| D11 | A1 var docs-ahead-of-code ved audit; A4 bruker fase-splitt fremfor purpose-Condition. | `Agreement` har nå policybinding, mens dynamiske action-fakta ligger i separate per-use-objekter. | Capability-påstanden gjelder bare den testede AIGateway-banen. |
| D12 | Provider-invocation-policyen isoleres i `PurposeBoundAIGatewayCell`, ikke i flere templates eller per-Grant-felt. | Minste løsning som fjerner Agreement-koblingen uten nytt wireformat. | Legacy AIGateway er ubundet; purpose-Cell har ett Grant og avviser mixed Agreements. |

## A4-v1-beslutninger og gjenværende Agreement-spørsmål

Implementasjonsstatus og testbevis står i
[A4-v1 implementasjonsrapport](A4_IMPLEMENTATION_REPORT.md).

1. **Condition-form og faser:** Dagens `Condition` kjører ved både admission
   og bruk, men kan ikke konsumere dynamisk purpose/action/digest uten en
   eksplisitt fase-splitt. Den gjelder dessuten Agreement-wide, ikke per
   Grant. A4 må velge hvilken del som er statisk avtalevalidering og hvilken
   som er per-action resolver-/gateway-validering; svaret må ikke lage en
   parallell, utestet autorisasjonsmodell.
2. **Agreement-binding — besluttet A4-v1-spor og tre alternativer:** A4-v1
   skal **ikke** innføre per-Grant purpose/action-constraints. Den skal starte
   med alternativ B og smale Agreements per verktøy-/action-familie. Per-Grant
   er en V2-beslutningsport som først åpnes dersom empirisk evidens viser at
   blandede scopes i samme Agreement er nødvendig.

   | Alternativ | Innhold | Fordel | Risiko / konsekvens |
   | --- | --- | --- | --- |
   | A. Ingen Agreement-endring | La en egresspolicy evaluere A1 separat. | Raskest, minst migrering. | Svak provenance: purpose/action-policy er ikke forpliktende knyttet til avtalen/granten. Ikke anbefalt som endelig modell. |
   | B. Agreement-level `authorizationPolicyBinding` digest | En signert/versjonert policy-binding registreres på Agreement-nivå; en fase-separert per-action context kontrollerer intent/digests ved bruk. | **Anbefalt A4-v1-hybrid:** synlig avtaleprovenance uten å late som en Agreement-wide Condition er en per-Grant action-condition. Smale Agreements begrenser scope ytterligere. | Krever nytt felt/migrering, canonicalization og tydelig vurderingstidspunkt. Bindingen er fortsatt ikke en Grant. |
   | C. Per-Grant purpose/action-constraints | Hver Grant bærer smale purpose/action/destination/data-constraints. | Mest presis minst-privilegium. | **Ikke A4-v1.** Størst migrering og kompatibilitetsrisiko; krever per-Grant condition/evaluator, lifecycle og revokasjonssemantikk. V2-port bare ved dokumentert behov for blandede scopes. |

   Alternativ B er implementert og testet. Smale Agreements er nå realisert
   ved en egen `PurposeBoundAIGatewayCell` med ett template-Grant; blandede
   requester-Agreements avvises av eksisterende subset-kontroll. Alternativ C
   er fortsatt en lukket V2-port. Se
   [isolasjonsbeslutningen](A4_AUTHORITY_ISOLATION_DECISION.md).
3. **Capability-form:** Hvilke eksisterende eller nye konkrete capabilities
   representerer disclosure, provider-invocation, file-write og script-exec?
   Navn må være smale, operasjonsnære og ikke wildcard-baserte.
4. **Authority-path binding:** Hvordan bindes Agreement, Contract, Grant,
   condition evaluation og domain-scoped identity til samme canonical digest
   set og correlation ID?
5. **Kontraktsignatur, reissue og gamle dekodere:** Krever en ny
   `authorizationPolicyBinding` resignering/reissue av Contract eller
   Agreement, og hvordan bevises det at gamle dekodere ikke ignorerer et nytt
   condition-/binding-felt? Ukjent security-relevant condition må feile lukket,
   ikke falle tilbake til tidligere allow-semantikk.
6. **Canonicalization — delvis besluttet:** A4-v1 bruker domene-separert,
   lengdeprefikset SHA-256 over eksplisitte semantiske komponenter og
   AIGateways eksisterende sorterte requestrepresentasjon. En generell
   canonical JSON/CBOR-profil på tvers av alle runtimes er fortsatt åpen.
7. **Config provenance:** Hvem kan publisere eller endre en CellExecutionPolicy,
   og hvordan knyttes config/policy-digest til den faktisk resolved Cell?
8. **Egresscoverage:** Hvilken adapter eier faktisk nettverk, subprocess,
   script, fil, bridge og provider-kall? A4 må ha en komplett route-matrise.
9. **Storage/disclosure:** Hvordan uttrykkes recipient-bound disclosure
   capability, retention TTL, deletion receipt og downstream begrensninger?
10. **Approval UX:** Når er per-handling, tidsavgrenset eller policy-vedtatt
   approval tillatt? Hvilken målgruppe kan forstå forskjellen mellom lokal og
   ekstern revokasjon?
11. **Replay:** Hvilke beslutningsfakta kan replays, og hvilke eksterne effekter
   må aldri replays? En receipt kan ikke føre til et nytt provider-kall.
12. **Taxonomy governance:** Hvordan kan formålsrefs promoteres og tilbakekalles
    uten at klienter kan bruke frie strings som security-scope?

## A4-akseptansekriterier

A4 kan først beskrives som implementert for en avgrenset action-familie når:

- runtime bruker alle fire A1-objektene på den faktiske egressveien
- en Resolver-/gateway-grense avviser alle negative golden cases
- faktisk payload, destinasjon og config/policy er digest-bundet ved execute
- authority, storage og disclosure er separate kontroller
- owner path uten ceiling er testet negativt
- direkte adapter-/script-bypass er fraværende eller teknisk blokkert
- allow/deny og execution result har separate, secret-safe receipts
- revokasjon/expiry og feiltilstander er testet med positiv og negativ evidens

## Eksplisitte current limitations

- A4-v1 har additive runtimefelt og legacy-dekoding; eksisterende, ubundne
  Contract blir med hensikt ugyldige mot en template som nå krever binding.
- JSON Schema-filene er normative wire-beskrivelser; de er ikke eksponert i
  Explore eller brukt av en Cell i dag.
- Den lokale validatoren er med hensikt smal og avhengighetsfri; den erstatter
  ikke en standardsamsvarende JSON Schema-validering i CI.
- Golden-digestene er syntetiske testverdier, ikke hashes av ekte brukerdata,
  secrets eller eksterne requests.
- Dette etablerer ikke fysisk kontroll hos en mottaker etter at data er
  avslørt, og etablerer ikke regulatorisk etterlevelse.
