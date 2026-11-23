# Dataflyt — egen agent mot HAVEN

```mermaid
sequenceDiagram
  participant S as Student (HAVEN i nettleser)
  participant C as Claude Code / Codex (studentens maskin)
  participant A as Adapter (pycell mcp / haven-mcp, stdio)
  participant B as /bridgehead/session (CellScaffold)
  participant O as cell:///OwnAgents
  participant X as Celle (f.eks. Mine dokumenter)
  participant P as Modelleverandør (Anthropic / OpenAI)

  A->>A: lager nøkkelpar (nøkkelring / fil 0600), viser fingeravtrykk
  A->>B: opptak: signert utfordring (bridge-channel.v1)
  A->>O: forespørsel (agentnøkkel, maskin, leverandør, celler) — gir ingen tilgang
  S->>O: ser forespørsel, sammenligner fingeravtrykk, godkjenner med passkey
  O->>O: lagrer AgentDelegation signert av studenten
  C->>A: verktøykall (MCP)
  A->>X: get/set som agentnøkkel
  X->>X: Agreement: DelegatedAgentCondition + RecipientCondition + resten av vilkårene
  X-->>A: svar, eller avvisning med kode
  X->>O: logghendelse (tid, verktøy, celle, utfall) — aldri innhold
  A-->>C: verktøysvar
  C->>P: sender verktøysvaret til modellen under studentens egen konto
  S->>O: Koble fra → neste kall avvises
```

Det som aldri går gjennom HAVEN eller adapteren: studentens Claude- eller ChatGPT-innlogging, OAuth-token eller API-nøkkel. Adapteren kaller aldri en modell selv.

Det som aldri går ut av HAVEN til modelleverandøren: innhold i celler uten `RecipientCondition` som tillater leverandøren, andres innslag uten deres tillatelse, forskningsdata over delegeringens N-nivå, privatnøkler.
