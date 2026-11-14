# Text Reliability Analysis Report

- Schema: `haven.text_reliability.analysis.v1`
- Analysis ID: `analysis-ce1a7de6a9579b79`
- Generated at: `2026-11-14T11:59:24Z`
- Source mode: `verifying`

## Inputs
- `text-file:eksempeltekst.md:eb3219fe73584902`: Mobilforbud i skolen virker (86 words)

## Markdown Structure
- Sections: `1`
- Tables: `0`

## Claims
- `claim-0001` `cluster-0001` `factual` `assertive` `source_cue_without_anchor`: "Ifølge en rapport fra Utdanningsdirektoratet har 70 % av skolene innført en form for mobilforbud."
- `claim-0002` `cluster-0001` `causal` `assertive` `source_missing`: "Elevene konsentrerer seg bedre når telefonen ligger i skapet, fordi varslene ikke avbryter undervisningen."
- `claim-0003` `cluster-0001` `factual` `assertive` `source_missing`: "Alle vet at sosiale medier gir mer mobbing."
- `claim-0004` `cluster-0001` `factual` `assertive` `needs_external_source_audit`: "En studie fra Norges handelshøyskole fant at karakterene i matematikk økte etter forbudet, se https://www.nhh.no/forskning/mobilforbud."
- `claim-0005` `cluster-0001` `factual` `assertive` `source_missing`: "Kritikerne mener at forbudet tar fra elevene et viktig læringsverktøy."
- `claim-0006` `cluster-0001` `factual` `moderated` `source_missing`: "Men lærerne kan fortsatt bruke nettbrett i timene."
- `claim-0007` `cluster-0001` `causal` `assertive` `source_missing`: "Derfor bør alle skoler innføre et nasjonalt mobilforbud fra neste skoleår."

## Claim Clusters
| Cluster | Title | Claims | Source audit statuses | Representative claims |
| --- | --- | ---: | --- | --- |
| `cluster-0001` | Mobilforbud i skolen virker | 7 | source_cue_without_anchor:1, source_missing:5, needs_external_source_audit:1 | claim-0001 / claim-0002 / claim-0003 |

## Claim Source Matrix
| Claim | Cluster | Section | Type | Audit status | Evidence grade | Sources | Quote |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `claim-0001` | `cluster-0001` | Mobilforbud i skolen virker | factual | `source_cue_without_anchor` | source_named_but_not_anchorable | Ifølge | Ifølge en rapport fra Utdanningsdirektoratet har 70 % av skolene innført en form for mobilforbud. |
| `claim-0002` | `cluster-0001` | Mobilforbud i skolen virker | causal | `source_missing` | no_source_anchor |  | Elevene konsentrerer seg bedre når telefonen ligger i skapet, fordi varslene ikke avbryter undervisningen. |
| `claim-0003` | `cluster-0001` | Mobilforbud i skolen virker | factual | `source_missing` | no_source_anchor |  | Alle vet at sosiale medier gir mer mobbing. |
| `claim-0004` | `cluster-0001` | Mobilforbud i skolen virker | factual | `needs_external_source_audit` | source_named_unverified | https://www.nhh.no/forskning/mobilforbud. | En studie fra Norges handelshøyskole fant at karakterene i matematikk økte etter forbudet, se https://www.nhh.no/fors... |
| `claim-0005` | `cluster-0001` | Mobilforbud i skolen virker | factual | `source_missing` | no_source_anchor |  | Kritikerne mener at forbudet tar fra elevene et viktig læringsverktøy. |
| `claim-0006` | `cluster-0001` | Mobilforbud i skolen virker | factual | `source_missing` | no_source_anchor |  | Men lærerne kan fortsatt bruke nettbrett i timene. |
| `claim-0007` | `cluster-0001` | Mobilforbud i skolen virker | causal | `source_missing` | no_source_anchor |  | Derfor bør alle skoler innføre et nasjonalt mobilforbud fra neste skoleår. |

## Source Checks
- `claim-0001`: `source_missing` / `source_cue_without_anchor` - source_cue_found_without_url_or_retrievable_anchor
- `claim-0002`: `source_missing` / `source_missing` - no_source_reference_found_near_claim
- `claim-0003`: `source_missing` / `source_missing` - no_source_reference_found_near_claim
- `claim-0004`: `not_checkable` / `needs_external_source_audit` - local_v1_does_not_fetch_or_verify_sources
- `claim-0005`: `source_missing` / `source_missing` - no_source_reference_found_near_claim
- `claim-0006`: `source_missing` / `source_missing` - no_source_reference_found_near_claim
- `claim-0007`: `source_missing` / `source_missing` - no_source_reference_found_near_claim

## Argument Graph
- Nodes: `1`
- Edges: `0`

```mermaid
flowchart TD
    n001["Mobilforbud i skolen virker (7 claim(s))"]
```

## Quantitative Models
- No quantitative model inputs found.

## Rhetoric
- `authority_appeal`: "Ifølge en rapport fra Utdanningsdirektoratet har 70 % av skolene innført en form for mobilforbud."
- `certainty_inflation`: "Alle vet at sosiale medier gir mer mobbing."
- `contrast`: "Men lærerne kan fortsatt bruke nettbrett i timene."

## Reliability Dimensions
- `source_grounding`: `weak` - 6 claim(s) lack nearby source references.
- `logical_coherence`: `mixed` - Heuristic argument links found.
- `transparency`: `mixed` - The local tool exposes quote spans and source-status limitations.
- `rhetorical_pressure`: `moderate` - 1 rhetoric finding(s) may substitute for evidence.
- `uncertainty_handling`: `weak` - Unverified or missing source support remains.
- `fact_checkability`: `mixed` - Claims are sentence anchored; external verification is a separate step.

## Boundaries
- The local v1 tool does not verify external sources.
- Deep argument reconstruction requires model or human review.
- Quantitative productivity models are sizing models unless a source-auditor validates inputs and an empirical model validates attribution.
