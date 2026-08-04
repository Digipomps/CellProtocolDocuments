# A1 — Formålsbundet ekstern handling

Dato: 2026-08-03  
Status: **normativ A1-kontrakt; A4-v1 implementert for én avgrenset AIGateway-bane**  
Beslutningseier: menneskelig eier av den aktuelle CellConfiguration og Contract

## Formål

Denne leveransen definerer A1: en planlagt kontrakt for å la deklarerte
formål, mål og påstandsgrunnlag **innsnevre** utgående handlinger fra AI- og
script-celler. Den definerer ikke en ny kilde til myndighet.

Den normative grunnregelen er:

> Et formål kan innsnevre en eksisterende rettighet, men kan aldri opprette,
> utvide eller arve en rettighet.

Målet er at en bruker og en senere resolver-/egressimplementasjon kan svare
konkret på: *hva skal gjøres, hvorfor, mot hvem/hvor, med hvilke data, under
hvilken policy og med hvilken faktisk rettighet?*

## Mål og ferdigkriterier

| Formål | Mål | Målbar evidens | Status |
| --- | --- | --- | --- |
| `purpose://access.audit.privacy` | Gjøre hver foreslått ekstern handling inspeksjonsbar og avvisbar. | Alle A1-fixtures binder formål, handling, destinasjon, data, plan, konfigurasjon, policy, taksonomi og payload med digest. | satisfied for spesifikasjonen og den avgrensede A4-v1-banen. |
| `purpose://knowledge.explain-policy` | Forklare policyens begrunnelse uten å blande den med autorisasjon. | Claim-ledger, threat model og decision log skiller evidens, antagelser og normative valg. | satisfied for spesifikasjonen. |
| `purpose://test.acceptance.purpose-decomposition` | Fange feil formål, parent-/facet-escalation og bindingstap før A4. | Positiv og negativ golden-fixture-suite passerer den lokale semantiske kontrollen. | pending verification. |

Et formål med ukjent eller utestbar måltilstand skal ikke åpne en ekstern
handling. Det skal stå som `purpose://prompt.unknown`, blokkere utførelse og
be om menneskelig avklaring.

## Leveransen

- [Audited brief og claim ledger](AUDITED_BRIEF_AND_CLAIM_LEDGER.md)
- [Threat model](THREAT_MODEL.md)
- [Beslutningslogg og A4-spørsmål](DECISION_LOG.md)
- [A4-v1 implementasjonsrapport](A4_IMPLEMENTATION_REPORT.md)
- [A4-v1 beslutning om Agreement-isolasjon](A4_AUTHORITY_ISOLATION_DECISION.md)
- [Normative JSON Schema-kontrakter](schemas/)
- [Positive og negative golden fixtures](fixtures/)
- [Lokal, avhengighetsfri struktur-, semantikk- og lenkekontroll](checks/validate_contract.py)

## Normative semantiske låser

1. **Én konkret effekt, ett primært formål.** Ett `PurposeBoundActionIntent`
   beskriver nøyaktig én ytre effekt og nøyaktig én `primaryPurposeRef`.
   Flere handlinger må splittes i flere intents og beslutninger.
2. **Exact match som standard.** Et parent-formål impliserer ikke et child-
   formål, og et child-formål impliserer ikke parent-formålets videre scope,
   med mindre en fremtidig Contract uttrykkelig og testbart innfører en annen
   regel. A1 definerer ingen slik regel.
3. **Facets er ikke autoriserende.** Kvalitet, personvern, validering og andre
   kryssgående facets kan gi krav eller undercuts, men kan ikke matche en
   action ceiling.
4. **Ukjent feiler lukket.** `purpose://prompt.unknown` er alltid blokkert for
   ekstern utførelse. Confidence er kun beslutningsstøtte, aldri adgangsbevis.
5. **CellConfiguration er en ceiling, ikke en grant.** Den kan redusere hvilke
   effekter som er mulige. Den kan ikke erstatte identitet, Agreement,
   Contract/Grant, conditions eller resolver-kontroll.
6. **Trust package er evidens, ikke authority.** Pakken kan dokumentere
   dataløype, kilde-audit, retention, modell og brukerforståelse. Den kan ikke
   gi capability eller overstyre en denial.
7. **Owner path er ikke et unntak for egress.** En owner path kan være en
   akseptert grunnleggende autorisasjonsvei i eksisterende CellProtocol, men
   A1 krever fortsatt den ytre action ceiling. Eierstatus er ikke blankofullmakt
   til publisering, provider-kall, filutskrift eller andre eksterne effekter.
8. **`s` er separat fra disclosure.** Storage krever egen `s`-rettighet.
   Disclosure, forwarding og publisering krever en annen, eksplisitt
   capability og mottakerbinding. Ingen av dem følger av den andre.
9. **Alle beslutningsrelevante deler bindes.** Purpose-, action-, destination-,
   data-manifest-, plan-, config-, policy-, taxonomy- og payload-digest skal
   følge intent, authorization context og receipt.

## Autorisasjonsformel

Dette er en normativ evalueringsregel, ikke nåværende runtime-kode:

```text
allow(effect) =
  valid domain-scoped identity/proof
  AND valid explicit authority path (Contract/Grant, or supported owner path)
  AND config policy ceiling matches the exact external effect
  AND exact primary-purpose match
  AND all binding digests match
  AND destination/data/plan constraints match
  AND storage and disclosure each have their own required authority
  AND any required trust-package evidence and human approval are current
```

Hvis et ledd er ukjent, mangler, er utløpt eller er inkonsistent, er resultatet
`denied` eller `requires_human_approval`; aldri en stille fallback til egress.

## Nåværende avgrensning

A1-kontrakten er nå håndhevet på den nye, smale
`PurposeBoundAIGatewayCell.ai.invokePurposeBound`-banen. Den er ikke håndhevet på legacy
`ai.invoke`, HAVENAgentD, scriptceller, øvrig transport eller andre
CellConfigurations. Se [A4-v1 implementasjonsrapport](A4_IMPLEMENTATION_REPORT.md)
for nøyaktig runtime-scope, Agreement-konsekvens og testbevis.

Lokale kilder for bakgrunnen:

- [Book 23 — Purpose Knowledge Base](../../Book/23_Purpose_Knowledge_Base.md)
  dokumenterer sideeffektfri purpose-resolving og `purpose://prompt.unknown`.
- [Book 04 — Agreements and Contracts](../../Book/04_Agreements_Contracts.md)
  skiller Agreement-intensjon fra Contract-myndighet og skiller `s` fra
  forwarding.
- [Book 06 — CellResolver](../../Book/06_CellResolver.md) angir Resolver som
  håndhevingsgrense for støttede veier, med begrensninger for direkte kall og
  nedstrøms kopiering.
- Den lokale metoden `personal-data-trust-package` er brukt som
  arbeidsgrunnlag: en tillitspakke er evidens/proposal, ikke authority.
  Metodekilden er ikke lenket fordi den ligger utenfor repositoryet og ikke er
  en portabel produktreferanse.

Et tidligere kilde-audit fant at `Agreement.swift` manglet policybinding,
`ConditionType` manglet formålsvariant og `ConnectContext` manglet per-action-
kontekst. A4-v1 løser dette med en fase-splitt: statisk
`authorizationPolicyBinding` på Agreement og separate per-use action-objekter,
uten å introdusere en purpose-Condition eller endre Grant-wireformatet.

## Ikke-mål

- Ingen generell A4-dekning utenfor den dokumenterte AIGateway-keypathen.
- Ingen per-Grant purpose/action-utvidelse eller endring av Grant-wireformatet.
- Ingen påstand om at eksisterende `Condition` kan evaluere dynamisk formål,
  action eller digest ved admission eller bruk.
- Ingen ny global identitet eller personscoresystem.
- Ingen automatisk promotering av formålskandidater til taksonomien.
- Ingen faktisk ekstern handling, modellkall, kredentiallesing, lagring,
  publisering eller disclosure.
- Ingen påstand om regulatorisk etterlevelse, sikker deploy eller at en
  kryptografisk receipt alene gir tillit til en person eller mottaker.

## Kontroll

Kjør fra denne mappen eller repository root:

```bash
python3 Deliverables/Purpose_Bound_External_Action_Contract_2026-08-03/checks/validate_contract.py
```

Kontrollen er avhengighetsfri og validerer JSON-parse, påkrevde wire-felter,
digestform, positive/negative semantiske cases og relative Markdown-lenker i
denne leveransen. Den er **ikke** en full JSON-Schema 2020-12 validator; se
[Decision log](DECISION_LOG.md) for A4-kravet om en full validator i CI.
