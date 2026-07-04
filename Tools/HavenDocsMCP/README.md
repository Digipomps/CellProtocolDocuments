# HAVEN Docs MCP

Read-only Model Context Protocol server for `CellProtocolDocuments`.

The server exposes canonical HAVEN documentation as MCP resources, read-only
tools, and static reading-path prompts. It does not write files, call staging,
mutate Vault/Todo state, publish RAG chunks, adapt prompts for target models, or
invoke language models.

## Run

```bash
python3 Tools/HavenDocsMCP/haven_docs_mcp.py
```

The server speaks line-delimited JSON-RPC over stdio, which is the normal local
MCP transport shape. Point an MCP client at the command above with this repo as
the working directory.

## Where To Run It

Default recommendation: each developer runs this MCP locally from their own
`CellProtocolDocuments` checkout.

That is the best fit for Kjetil, Vegar, and other collaborators because:

- stdio MCP is designed to be launched by the local MCP client
- citations point at the same files the developer can inspect and edit
- freshness follows the developer's current branch/submodule revision
- no extra LAN service, firewall rule, TLS, or shared auth boundary is needed

For a colleague such as Vegar:

1. Clone or update `CellProtocolDocuments` locally.
2. Configure the MCP client to launch:
   `python3 Tools/HavenDocsMCP/haven_docs_mcp.py`
3. Keep the repo synced through normal Git/submodule workflow.

Acceptable shared variant:

- Use an SSH or VPN command transport to start the same stdio server on a known
  host, for example a read-only office machine, when both people trust the host
  and the repo revision is pinned or visible.
- Do not expose this stdio MCP as an unauthenticated TCP service on the LAN or
  public internet.

If the team needs always-on shared access from office and home, prefer a proper
authenticated docs/RAG gateway or CellScaffold workbench endpoint. Keep this
MCP as the local lookup adapter and let RAG/RAGPromptTransformerCell own shared
retrieval and model-specific prompt packaging.

Useful local checks:

```bash
python3 Tools/HavenDocsMCP/haven_docs_mcp.py --list-tools
python3 Tools/HavenDocsMCP/haven_docs_mcp.py --list-resources
python3 Tools/HavenDocsMCP/haven_docs_mcp.py --search "RAG citations"
python3 -m unittest discover Tools/HavenDocsMCP/tests
```

## Resources

- `haven-docs://catalog/book`
- `haven-docs://book/{doc_id}`
- `haven-docs://book/{doc_id}#{heading_anchor}`

Resources read from canonical repo files only:

- `Book/book_catalog.json`
- `Book/*.md` entries listed in the catalog
- `README-CellProtocol.md`
- `DEVELOPERS.md`
- `Gap_Analysis.md`

## Tools

- `haven_docs_list` lists catalog records with optional `status`, `group`, and
  `audience` filters.
- `haven_docs_search` runs deterministic lexical search over heading sections
  and returns canonical citations.
- `haven_docs_read` reads a full document or heading section by `doc_id`, slug,
  path, or resource URI.
- `haven_docs_resolve` resolves a path, slug, symbol, endpoint, or topic to the
  best matching canonical docs.

Tool responses include `structuredContent` with citations and a short text
summary for clients that only display text content.

## Prompts

- `haven_docs_lookup_before_answering`
- `cellprotocol_implement_cell`
- `cellprotocol_author_skeleton_from_explore`

These prompts encode the current recommended reading paths for future agents.
They are not model-adaptive RAG prompts. Use `RAGPromptTransformerCell` and
`Tools/RAGPromptTransformer` when retrieved RAG chunks must be packaged for a
specific target model.

## Current Limits

- Search is lexical and local, not vector RAG.
- It does not proxy `/rag-mvp` or authenticated staging services.
- It does not generate final answer prompts for target models; that belongs to
  RAG or a Cell that consumes RAG output.
- Heading anchors are normalized locally and should be treated as best-effort
  until shared renderer anchor normalization is imported.
- It does not watch files or emit list-changed notifications.
- Write flows for Vault/Todo are intentionally excluded from this read-only
  first version.
