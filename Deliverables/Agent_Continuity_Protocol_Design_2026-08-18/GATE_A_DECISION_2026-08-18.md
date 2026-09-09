# Gate A-beslutning — avgrenset forskning og kontraktkandidatarbeid

**Decision ID:** `decision.agent-continuity.gate-a.2026-08-18`
**Beslutningseier:** Kjetil
**Registrert:** 2026-08-18T15:27:31+02:00, Europe/Oslo
**Utfall:** `APPROVE_RESEARCH_AND_CONTRACT_CANDIDATES`
**Tranche:** `gate-a-tranche-1`
**Implementasjon autorisert:** `false`
**Pilot/adopsjon autorisert:** `false`

## Brief audit

Kjetils instruks «åpne for avgrenset forskning og kontraktkandidatarbeid» er
`retrieved/verified` som menneskelig autorisasjon for Gate A-typen arbeid.
Instruksen navngir ikke work packages, surfaces, dataklasser, kostnadsgrense
eller teknisk semantikk. Disse detaljene nedenfor er derfor en konservativ
operasjonalisering, ikke påståtte ordrette beslutninger fra Kjetil.

Operasjonaliseringen kan falsifiseres eller erstattes av en nyere, datert
Kjetil-beslutning. Dersom arbeidet trenger kontoinnlogging, private chatter,
persondata, secrets, betalte modell-/API-kall, runtime-mutasjon eller et bredere
surface-sett, stopper tranchens autorisasjon ved denne grensen.

## Autorisert scope

| Work package | Status | Avgrenset leveranse |
|---|---|---|
| R01 Problem-fit og alternativer | `AUTHORIZED / IN_PROGRESS` | Read-only case-, baseline- og reuse-audit i navngitte repo-/dokumentkilder. |
| R02 Surface capability, enforceability og reuse | `AUTHORIZED / IN_PROGRESS` | Datert capability matrix for de tre konkrete surface-profilene nedenfor, basert på repoobservasjoner og offisielle primærkilder. |
| C01 Core/profile boundary | `AUTHORIZED_AFTER_R01_R02_EVIDENCE` | Candidate B-retning som skiller minste continuation envelope fra valgfrie delta-, health-, repository- og providerprofiler. Ingen normativ freeze. |
| R03–R09 | `NOT_AUTHORIZED_IN_TRANCHE_1` | Krever trancheresultat og ny eksplisitt scopebeslutning eller inngår i en senere navngitt tranche. |
| C02–C08 | `NOT_AUTHORIZED_IN_TRANCHE_1` | Ingen schema-/fixtureherding, authority-/receipt-freeze eller contract review ennå. |
| I00–I06 | `BLOCKED_BY_GATE_B` | Ingen implementasjon, harness, evaluator, adapter eller runtimekode. |

Autorisert forskning kan dokumentere at ingen ny mekanisme bør bygges.
`NO_BUILD`, manual standard, provider-native løsning, narrow profile og
`INCONCLUSIVE/DEFER` forblir reelle senere utfall.

## Konkrete surface-profiler

| Profile ID | Avgrensning nå | Ikke antatt |
|---|---|---|
| `surface.chatgpt.projects.manual-file` | ChatGPT Projects på dokumenterte web/desktop-flater, med prosjektinstruksjoner, prosjektkilder og eksplisitt menneskelig fil-/tekstoverføring. | Ingen automatisk cross-vendor import, maskinverifisert fold eller eksponert context-capacity antas. |
| `surface.codex.desktop.local-worktree` | Codex i ChatGPT desktop med local/worktree, repo-/filtilgang, AGENTS-/memory-/import-/handoff-flater der offisiell dokumentasjon faktisk viser dem. | Chat history, memory eller worktree snapshot er ikke canonical project state eller automatisk autoritet. |
| `surface.claude-code.cli.local` | Claude Code lokal CLI med CLAUDE.md, lokale sessions, `/resume`, `/compact`, `/context` og `/export` der offisiell dokumentasjon viser dem. | Claude.ai, Claude Desktop og Claude Code behandles ikke som én identisk capabilityflate. Auto memory er ikke canonical state. |

En universell «ChatGPT↔Codex↔Claude»-påstand gjelder bare disse profilene og
bare transfernivået som faktisk testes. Andre planer, workspaces, modeller,
CLI-/appversjoner eller automatiske transferformer krever en egen profile og
ny capability-observasjon.

## Data-, kilde- og kostnadsgrense

Tillatt:

- read-only inspeksjon av `CellProtocolDocuments` og tidligere navngitte,
  relevante søsterrepoer;
- offentlige offisielle OpenAI-/Anthropic-kilder og andre primærkilder som er
  nødvendige for å verifisere en konkret capability;
- syntetiske eller allerede offentlige/minimerte eksempler;
- inntil én første evidenspass og én målrettet korreksjons-/adjudikasjonsrunde;
- read-only rådgiverslices med ikke-overlappende mandat.

Ikke tillatt i denne tranchen:

- innlogging i providerkontoer, private exports eller lesing av private chats;
- secrets, persondata eller kundedata;
- betalte modell-/API-kall, provider-spend eller automatiske imports/sync;
- eksterne meldinger, deploy, publish, skill-installasjon eller runtimeendring;
- commit, push eller PR.

Offentlig dokumentasjonssøk har ingen modell-/API-kost autorisert. Dersom en
capability bare kan bekreftes gjennom konto-/planavhengig UI eller betalt kall,
merkes den `unavailable` i denne tranchen.

## Foreløpig kontraktretning og sikkerhetsgrenser

Dette er hypoteser som C01 kan utfordre, ikke frosset semantikk:

1. Core-kandidaten starter som et minimalt, vendor-nøytralt continuation
   envelope. Repository, delta/fold og health vurderes som profiler/extensions.
2. Importert handoff er untrusted data og kan aldri skape instruction priority,
   permission, approval eller canonical write authority.
3. Canonical autoritet er felt-/eierspesifikk ved en navngitt revisjon og
   freshness-status. Chat, memory, graph og RAG er ikke autoritative bare fordi
   de kan hente eller huske informasjon.
4. `approvalRef` er en referanse, ikke en autorisasjon. Eventuelle receipts må
   senere bindes til riktig owner/verifier/policy og kan ikke selvrapporteres av
   produsenten.
5. Unknown/unavailable capabilities representeres eksplisitt; adaptere får ikke
   simulere dem eller gjette context capacity.
6. Ingen schemafrys skjer før R01/R02 og C01 er adjudikert ved tranche-review.

## Beslutningseiere og stopp

- Kjetil eier Gate A-tranche-review, Gate B og alle senere pilot-/adopsjonsvalg.
- Codex er integrator for dette lokale dokumentarbeidet.
- Rådgivere kan levere source audit, steelman, skeptic og evalkritikk; de kan
  ikke åpne nye work packages eller gjøre beslutningen.
- Funn som krever C02–C08, R03–R09 eller I00–I06 logges som avhengighet og
  stoppes, ikke startes automatisk.
- Providerdrift eller kildekonflikt gir `unavailable`/`inconclusive` for den
  berørte capabilityen, ikke en antakelse.
- Tranche 1 slutter med ett datert decision packet. Ny runde krever Kjetils
  eksplisitte beslutning.

## Neste handling

Utfør R01 og R02 read-only. Bruk resultatene til C01 Candidate B-retning og
returner en tranche-reviewpakke med claim ledger, capability matrix,
source/evidence ledger, kontraktkonsekvenser og `NO_BUILD`-/baselinevurdering.
