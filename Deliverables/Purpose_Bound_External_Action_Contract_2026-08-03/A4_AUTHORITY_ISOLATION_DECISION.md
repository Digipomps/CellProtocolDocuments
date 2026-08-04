# A4-v1 — beslutning om Agreement-isolasjon

Dato: 2026-08-03  
Beslutningseier: Kjetil  
Status: implementert og testet; per-Grant V2-port fortsatt lukket

## Briefgransking

Faktaene nedenfor er hentet fra lokal kode og er ikke erklært autoritative bare
fordi de står i briefen.

| Faktum | Auditstatus | Lokal evidens |
| --- | --- | --- |
| `GeneralCell` persisterer én `agreementTemplate`. | retrieved-local | `GeneralCell.swift` og `Book/04_Agreements_Contracts.md` |
| A4-profilen lå først i en AIGateway-template med både invocation-, state- og setup-Grants. | retrieved-local | `AIGatewayCell.swift` før isolasjonsendringen; `A4_IMPLEMENTATION_REPORT.md` |
| Flere navngitte templates ville kreve valg av template ved admission, signering, persistens og use-time matching. | inferred-from-local-code | `GeneralCell.agreementDerivedFromTemplate`, Contract-verifikasjon og kodingsflaten |
| Provider-, cache-, quota-, credential- og receipt-motoren kan deles mellom konkrete Cell-typer. | retrieved-local | `AIGatewayCell.swift`; samme motor brukes av den nye subtypen i test |

## Formål og Goals

| purposeRef | Intent | Målbar Goal | Sluttstatus |
| --- | --- | --- | --- |
| `purpose://access.audit.privacy` | Hindre at en Agreement-policy for provider-egress binder eller autoriserer uvedkommende AIGateway-funksjoner. | Purpose-bound Cell har nøyaktig ett Grant og eksakt policybinding; legacy AIGateway har ingen slik binding eller keypath. | satisfied |
| `purpose://test.acceptance.purpose-decomposition` | Bevise at scope-isolasjonen overlever requester-input og persistens. | Smalt Agreement godtas; blandet Agreement avvises; begge Cell-profiler normaliseres korrekt etter encode/decode. | satisfied |

## Påstandsledger og adjudikasjon

| ID | Påstand | Type | Støtte / motargument | Dom |
| --- | --- | --- | --- | --- |
| C-ISO-01 | En egen Cell-type er mindre protokollflate enn flere Agreement-templates i `GeneralCell`. | normative, moderated | Krever ingen nye Agreement-/Contract-wirefelt. Motargument: subtyping kan lekke overflate. Det testes ved eksakt Explore-keysett og typebestemt profil. | supported for dette tilfellet |
| C-ISO-02 | En typebestemt autorisasjonsflate kan dele provider-motor uten at requesten får velge myndighetsprofil. | project_capability | Profilen bestemmes av konkret Swift-type; requesten har ikke profile-felt. Legacy direkte purpose-kall feiler før credentials. | supported |
| C-ISO-03 | Ett template-Grant er tilstrekkelig til å avvise blandede requester-Agreements uten per-Grant constraints. | project_capability | `GeneralCell` krever at alle requested Grants er subset av template. Positiv og negativ test er implementert. | supported |
| C-ISO-04 | En per-Grant V2-utvidelse er ikke nødvendig nå. | normative, moderated | Det eneste implementerte action-scope-et er isolert i egen Cell. Motargumentet — flere policyfamilier i ett Contract — har ingen konkret nødvendig use case i denne leveransen. | supported; gjenåpnes ved evidens |

Root-komposisjon:

```text
Velg dedikert Cell
  allOf(C-ISO-01, C-ISO-02, C-ISO-03)
  undercut by: subtyping kan dele for mye overflate
  svar: eksakt ett registrert keypath, eksakt ett Grant, reload-test

Ikke innfør per-Grant V2 nå
  allOf(C-ISO-03, C-ISO-04)
```

## Beslutning

`PurposeBoundAIGatewayCell` registreres som `cell:///PurposeBoundAIGateway`.
Den gjenbruker AIGatewayens modne provider-motor, men dens konkrete type låser:

- Agreement-template til ett `rw--`-Grant på `ai.invokePurposeBound`;
- én `authorizationPolicyBinding` for `provider_invocation`;
- Explore-/Meddle-overflaten til samme ene keypath.

Legacy `cell:///AIGateway` fjerner den purpose-bound keypathen og
policybindingen. Ved reload kanoniseres begge profiler, slik at en eldre blandet
template ikke videreføres. Dette er en app-/Cell-isolasjon, ikke en ny
CellProtocol-wirekapabilitet.

Cell-endepunktet og action-keypathen er del av policyens config-digest.
Bindingen er derfor versjonert `1.1.0`; tidligere `1.0.0`-signerte
Agreements/Contracts må utstedes og signeres på nytt. In-place mutasjon ville
brutt signatur- og provenance-egenskapene.

## Åpen beslutningsport

Per-Grant V2 vurderes først når en konkret use case krever minst to ulike,
uavhengige policy-/purpose-scopes i samme Contract og denne samlokaliseringen
ikke kan løses med separate Cells eller templates. Da må precedence,
signaturcanonicalization, revokasjon, legacy decode og use-time evaluering
spesifiseres samlet.

## Rapportkvalitetsdiagnostikk

| Metrikk | Resultat og evidens |
| --- | --- |
| Q1 Position-change traceability | Ingen posisjon ble endret etter beslutningen; alternativene ble vurdert før implementasjon. |
| Q2 Mixed-ledger ratio | Ledgeren har både valgt løsning og et eksplisitt inheritance-undercut; ingen normativ måltall brukes. |
| Q3 Audit-status honesty | Alle bærende faktapåstander er `retrieved-local` eller tydelig merket inferred; ingen ekstern støtte påstås. |
| Q4 Narrative independence | Valget følger minst protokollflate og testet isolasjon, ikke ønsket om å få per-Grant eller en ny kjernefeature. |
| Q5 Falsifiability audit | Påstandene kan falsifiseres av ekstra annonserte keys/Grants, godkjent mixed Agreement eller feil etter reload. Ingen slik test feilet. |
| Q6 Natural-experiment identification | Den valgte Cell-isolasjonen er faktisk implementert og kjørt; flere-template-alternativet er ikke forsøkt og omtales ikke som empirisk dårligere. |
| Q7 Revealed-preference test | Ikke relevant; analysen gjelder kodearkitektur, ikke aktørmotiv. |
| Q8 Terminal adjudication rate | 4 av 4 root-/delpåstander er adjudikert; V2 er en navngitt beslutningsport med eier. |
| Q9 Steelman sourcing | Ingen ekstern motsatt kilde finnes; sterkeste motargument er utledet fra subtype-/delingsegenskapene og testet direkte. |
| Q10 Concession asymmetry | Ingen konklusjon er endret uten ny evidens. |
