# Kontrakt — korpus, fasit og målerapport (løpet, v1)

## Korpus: `maaling/korpus/korpus-v<n>.jsonl`

Én JSON per linje:

| Felt | Type | Merknad |
|---|---|---|
| `id` | streng | stabil, `k<n>-<løpenummer>` |
| `text` | streng | meldingen slik en bruker ville skrevet den |
| `lang` | `nb` / `en` | Q2: bokmål og engelsk |
| `style` | `kort` / `lang` / `skrivefeil` / `indirekte` / `vet-ikke-navnet` / `negativ` | fordelingsakse |
| `intendedPurposeRef` | `purpose://…` eller `none` | det generatoren siktet mot; `none` for negativer |
| `split` | `trening` / `holdout` | settes ved frysing, deterministisk (hash av id), holdout ≈ 25 % |
| `generatedBy` | streng | f.eks. `losen-2026-09-23`; merket som generert, aldri ekte brukerdata |

## Fasit: `maaling/fasit/fasit-v<n>.jsonl`

`id`, `silverPurposeRef` (tolker), `agreement` (generator = tolker?), `goldPurposeRef` (Kjetil i Dommerbenken, bare for uenighet og stikkprøve), `decoy` (bool — blindt lagt inn for å avsløre alle-ja).

Regel: en dommerrunde der lokkeduene får «ja» teller ikke som gullfasit (`lesson.judgement-without-decoys-yields-all-yes`).

## Målerapport: `maaling/rapport/rapport-<dato>-<variant>.json`

Per id: `topK` (purposeRef + score, k=5), `unknown` (bool). Samlet per split: `top1`, `recallAt3`, `mrr`, `negativePrecision` (andel negativer som ble `unknown`), med bootstrap-intervall. Varianten (`dagens-rute`, `graf-v<n>`) står i filnavnet.
