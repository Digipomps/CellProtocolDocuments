# Bruk din egen Claude eller Codex med HAVEN-dokumentasjonen

For studenter. Du trenger ingen HAVEN-konto for dette steget, og HAVEN ser aldri innloggingen din hos Anthropic eller OpenAI.

## Det du trenger

- Python 3.10 eller nyere (`python3 --version`).
- Git.
- Enten Claude Code (med ditt eget Claude-abonnement eller API-nøkkel) eller Codex CLI (med din egen ChatGPT-konto). Du logger inn i verktøyet selv, slik verktøyet beskriver.

## Steg

1. Klon dokumentasjonen:
   `git clone https://github.com/Digipomps/CellProtocolDocuments.git` og gå inn i mappen: `cd CellProtocolDocuments`
2. Start agenten i mappen.
   - **Claude Code:** skriv `claude`. Første gang spør den om du vil bruke MCP-serveren `haven-docs` fra `.mcp.json`. Svar ja.
   - **Codex:** skriv `codex`. Svar ja når den spør om du stoler på prosjektet; da leser den `.codex/config.toml` og starter `haven-docs`.
3. Sjekk at det virker: skriv `/mcp` i Claude Code eller Codex. Du skal se `haven-docs` med fire verktøy (`haven_docs_search`, `haven_docs_read`, `haven_docs_list`, `haven_docs_resolve`).
4. Spør på norsk, for eksempel: «Hva er en celle i CellProtocol, og hvordan gir en avtale tilgang?» Agenten søker i dokumentasjonen og viser hvilket kapittel svaret kommer fra.

## Hva dette er og ikke er

- Serveren leser bare filene i mappen du klonet. Den sender ingenting videre og trenger ingen nøkkel.
- Spørsmålene og svarene går mellom deg og Anthropic eller OpenAI, etter vilkårene i ditt eget abonnement.
- Å koble agenten til dine egne data i HAVEN (dokumenter, notater) er neste steg. Det kommer som «Egne agenter» i HAVEN, der du godkjenner og kan koble fra agenten selv.

## Hvis noe ikke virker

- `haven-docs` vises ikke: sjekk at du startet agenten i rotmappen til repoet, og at `python3 Tools/HavenDocsMCP/haven_docs_mcp.py --list-tools` virker.
- Codex viser ikke serveren: prosjektet er ikke merket som klarert. Start `codex` på nytt i mappen og svar ja.
