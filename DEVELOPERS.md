# DEVELOPERS

Inngang for utviklere og AI-assistenter til praktiske rutiner i HAVEN-dokumentasjonen.

## 1. Start Here

- Les dokumentindeks: `README-CellProtocol.md`
- Les utviklerkapitler først:
  - `Book/10_Quickstart.md`
  - `Book/11_Developer_Guide_Cell.md`
  - `Book/12_Skeleton_Spec.md`
  - `Book/13_Agent_Instructions.md`
  - `Book/14_Perspective_Runtime_Matching.md`
  - `Book/15_Documentation_Discovery_and_RAG.md`
  - `Book/16_Book_Reference_Workspace.md`

## 2. Operasjonelle Playbooks

- SSH/package-resolve: `SSH_SETUP.md`
- Prompt policy og systemprompts: `Prompts/SystemPrompts.md`
- Dokumentasjonsgap: `Gap_Analysis.md`
- Cross-repo audit: `Deliverables/Documentation_Audit_2026-03-05.md`

## 3. Endringspolicy for dokumentasjon

- Oppdater dokumentasjon i samme PR/commit som funksjonell kodeendring.
- For kontrakter/endepunkter: oppdater både brukerrettet doc og agentrettet doc.
- For bakoverkompatibilitet: dokumenter eksplisitt om legacy format fortsatt støttes.
- Unngå absolute lokale paths; bruk repo-relative paths i markdown.

## 4. RAG-vennlig dokumentasjonspraksis

- Hvert doc må ha tydelig formål, scope og målgruppe i toppseksjon.
- Inkluder konkrete keypaths/endepunkter som egne listepunkter.
- Hold en stabil canonical path per tema for å unngå duplikat sannheter.
- Legg inn `Last verified against code` med dato når kontrakt/endepunkt beskrives.
- Bruk `Book/book_catalog.json` som maskinlesbar doc-tree for vault, web-rendering og RAG-oppkobling.
