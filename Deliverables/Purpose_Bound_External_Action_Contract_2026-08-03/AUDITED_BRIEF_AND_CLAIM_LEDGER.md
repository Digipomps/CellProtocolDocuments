# Audited brief og claim ledger

Dato: 2026-08-03  
Status: arbeidsgrunnlag auditet mot lokale HAVEN-kilder; ingen eksterne kilder
er hentet i denne A1-leveransen.

## Brief-integritet

| Brief-faktum | Status | Kilde / kontroll | Begrensning |
| --- | --- | --- | --- |
| Purpose-resolveren er sideeffektfri og faller tilbake til `purpose://prompt.unknown`. | retrieved-local | `Book/23_Purpose_Knowledge_Base.md`, avsnitt 9–10. | Dokumentert runtime-bridge er ikke en generell egress-policy. |
| Agreement uttrykker ønsket tilgang; Contract/Grant definerer tillatt tilgang. | retrieved-local | `Book/04_Agreements_Contracts.md`, avsnitt 1–3 og 12. | Hver konkret path krever egen positiv/negativ runtime-evidens. |
| Resolver er beskrevet som håndhevingsgrense for støttede resolver-medierte handlinger. | retrieved-local documentation | `Book/06_CellResolver.md`, avsnitt 3. | Dette beviser ikke at dagens runtime kan binde dynamisk formål til en konkret ekstern handling. |
| Agreement-/runtime-modellen har en formålsbundet per-action hook. | supported for bounded A4-v1 path | `Agreement.authorizationPolicyBinding`, de fire action-modellene og `PurposeBoundActionAuthorizer` er implementert; `PurposeBoundAIGatewayCell` bruker dem på `ai.invokePurposeBound`. | Ikke en Condition/ConnectContext-utvidelse og ikke generell egressdekning. |
| `s` gir storage/retention, ikke disclosure/forwarding. | retrieved-local | `Book/04_Agreements_Contracts.md`, avsnitt 2.2–2.3. | Protokollen kan ikke fysisk hindre en uærlig mottaker som allerede har fått data. |
| TrustPacket-matching gir ikke tilgang. | retrieved-local | `CellProtocol/Sources/CellBase/Cells/TrustPacket/TrustPacketCell.swift`, `evaluateAgainstPerspective`. | TrustPacket er ikke en erstatning for Contract-revokasjon. |
| AIGateway er dekket av denne A1-policyen. | supported only for bounded path | Den dedikerte `PurposeBoundAIGatewayCell.ai.invokePurposeBound` recomputerer observed bindings og autoriserer før credentialoppslag/provider-kall. | Legacy `AIGatewayCell`, draft, planning, fan-out, tools og lokale modeller er ikke dekket. |

Briefet er ikke autoritativt fordi det står i denne leveransen. Det er et
sporingsgrunnlag for påstandene nedenfor.

## Formål–påstandsgrense

- **Formål** angir ønsket retning og målbar effekt.
- **Påstand** sier noe om hva som er sant, mulig eller nødvendig.
- **Policyforslag** er et normativt designvalg, ikke påstand om nåværende
  runtime.

## Root claim

**C-A1-root** — *En formålsbundet action-kontrakt kan gjøre ekstern
AI-/script-adferd mer begripelig og strammere avgrenset, dersom formål bare
innsnevrer eksisterende authority og faktisk egress blir kontrollert av en
støttet håndhevingsgrense.*

Type: `normative`  
Styrke: `moderated`  
Formål: `purpose://access.audit.privacy`  
Mål: `goal.a1.external-action-contract` (lokalt leveransemål; ikke en
taksonomi-ref)

### Støttestruktur

```text
C-A1-root
  allOf
  ├── C-A1-01: Formålsresolving kan være sideeffektfri og ukjent kan feile lukket.
  ├── C-A1-02: Contract/Grant, ikke Agreement eller purpose-tekst, er authority.
  ├── C-A1-03: Resolver kan være en fremtidig håndhevingsgrense på støttede paths.
  ├── C-A1-04: Hver effekt kan bindes til konkrete digests og policy ceiling.
  └── C-A1-05: Storage og disclosure kan kontrolleres separat.

  countered by
  ├── U-A1-01: Promptklassifisering kan påvirkes eller være feil.
  ├── U-A1-02: Script/direct calls kan omgå Resolver.
  ├── U-A1-03: En tillitspakke kan bli tillitsteater uten enforcement.
  └── U-A1-04: Parent- og facet-matching kan bli scope-escalation.
```

## Claim ledger

| ID | Påstand | Type / status | Støtte | Undergravende forhold / beslutning |
| --- | --- | --- | --- | --- |
| C-A1-01 | Ukjent formål kan håndteres uten å finne på en ref eller utføre sideeffekt. | project_capability / supported locally | Book 23 beskriver `purpose://prompt.unknown` og sideeffektfri resolver. | Formålsresolveren gir ikke selv egresskontroll. Brukes bare som innsnevrende input. |
| C-A1-02 | Formål alene er ikke authority. | factual / supported locally | Book 04: Agreement uttrykker intensjon; Contract definerer tillatelse. | Ingen. Dette er en hard A1-invariant. |
| C-A1-03 | Et Contract kan binde en statisk authorization policy ceiling som kontrolleres ved konkret bruk. | project_capability / supported for A4-v1 | Agreement-bindingen inngår i Contract-signaturen; runtimebeslutningen eksponerer eksakte Agreement/Contract/Grant-refs; dedikert Cell isolerer action-familien. | Agreement-level, ikke per-Grant; flere scopes i samme Contract er ikke støttet. |
| C-A1-04 | Exact purpose/action/destination/data-digest-binding reduserer confused-deputy- og substitution-risiko. | project_capability / supported for bounded A4-v1 | Ren evaluator og AIGateway-tester av payload-drift, destination, owner-no-bypass og authority. | Ikke bevist for andre adapters eller for en generell cross-runtime canonicalization. |
| C-A1-05 | `s` og disclosure må ha separate beslutninger. | factual / supported locally | Book 04 og 06. | Kan ikke fysisk trekke tilbake en allerede kopiert ekstern verdi. |
| C-A1-06 | CellConfiguration bør fungere som ceiling, ikke grant. | normative / proposed | Forenlig med Book 04/06-skille mellom eksplisitt Contract og operasjonsgrense. | Det er ikke verifisert som et eksisterende first-class CellConfiguration-felt. |
| C-A1-07 | En trust package gir forklaring/evidens, ikke adgang. | factual / supported locally | Trust-package-kontrakten og TrustPacket-implementasjonens begrensninger. | En pakke uten gateway-enforcement er bare dokumentasjon. |

## Antagelser som A4 må enten bevise eller avvise

1. Alle ytre effekter fra en målrettet AI-/scriptcelle kan routes gjennom en
   kontrollert egressadapter eller Resolver-mediert action.
2. Den konkrete adapteren kan nekte rå nettverk, shell, filskriving og
   credential-eksport når det ikke foreligger en tillatt action ceiling.
3. Digestene kan kanoniseres stabilt, bindes til den faktiske payloaden og
   sammenlignes uten typeforvirring eller replay.
4. Exact purpose-match kan evalueres mot en versjonert taxonomi uten at en
   modell eller klient får velge ny semantikk ved runtime.
5. Den bruker som godkjenner en ekstern effekt forstår destinasjon, dataklasse,
   varighet og hvilken revokasjon som faktisk er mulig.

## Adjudikasjon

**C-A1-root: implementert og testet for én avgrenset provider-invocation-
bane; fortsatt docs-ahead-of-code for øvrige egressflater.**

Det er forsvarlig å bruke denne leveransen som kravgrunnlag for A4. Det er ikke
forsvarlig å si at HAVEN allerede hindrer formålsdrift, script-egress eller
uautoriserte provider-kall på tvers av alle paths.

## Åpne evidensoppgaver

- Velg en fase-splitt mellom Agreement-admission og per-action bruk, siden
  dagens `Condition` kjøres ved admission og bruk men ikke har dynamisk
  per-action formål/digest som input. En Agreement-wide condition er heller
  ikke i seg selv en per-Grant-begrensning.
- Kartlegg alle egressflater i AIGateway, HAVENAgentD, bridge-adaptere og
  script-/subprocess-vertsmiljøer.
- Velg og test canonical JSON-/digestprofil, inkludert unicode, rekkefølge,
  numerisk normalisering, redigering og secrets.
- Gjennomfør brukertest av den menneskelesbare action-previewen; en korrekt
  schema er ikke bevis på forståelse.
