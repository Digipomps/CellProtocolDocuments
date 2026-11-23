# Agenter i CellProtocolDocuments

Dette repoet er dokumentasjonen for HAVEN og CellProtocol. Svar på norsk når brukeren skriver norsk.

## Slå opp i dokumentasjonen først

MCP-serveren `haven-docs` (HavenDocsMCP) starter av seg selv i Claude Code (`.mcp.json`) og i Codex (`.codex/config.toml`, bare i klarerte prosjekter). Den har fire verktøy:

- `haven_docs_search`: søk. Norske ord finner også engelske kapitler.
- `haven_docs_read`: les en hel seksjon fra et treff.
- `haven_docs_list`: list kapitlene i Book.
- `haven_docs_resolve`: finn et kapittel ut fra navn eller sti.

Bruk dem før du svarer på spørsmål om HAVEN, og vis til kapittel og overskrift du fant svaret i. Står ikke svaret der, si det i stedet for å gjette.

## Regler

- Serveren er skrivebeskyttet. Den sender ingenting ut av maskinen og trenger ingen konto.
- Les eller send aldri innloggingsdata for Claude, Codex eller andre modelltjenester (`~/.claude`, `~/.codex`, `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`).
- Tilgang til celler i HAVEN går bare gjennom vilkår i Agreement. Dokumentasjonen beskriver dette; den gir ingen tilgang.
- Endringer i HAVEN-kode går gjennom formålsdrevet utvikling (Book kapittel 35).

Veiledning for studenter: `Manuals/Student_Egen_agent.md`.
