# TESTRESULT — egen-agent-mcp

## Baseline (WP0, 2026-11-23, sky)

| Repo | Commit | Kommando | Resultat |
|---|---|---|---|
| PyCellProtocol | `7f5c0fc` (main) | `python -m pytest -q` | 327 bestått, 1 hoppet over |
| GoCellProtocol | `c0274c2` (main) | `go test ./...` | ok (rotpakke og interop) |
| CellProtocolDocuments HavenDocsMCP | `a57751c` (før WP1) | `pytest Tools/HavenDocsMCP/tests` | 19/19 |
| CellProtocol (Swift) | — | `swift test` | venter: kjøres på Macen |
| CellScaffold CI på main | — | — | venter: kjøres på Macen / CI; 39 kjente røde AppTests 22.11 fra annen tråd |
| Staging: Python-klient med egen nøkkel mot `/bridgehead/session` | — | — | venter: måles på Macen |

## docs-norsk

`Tools/HavenDocsMCP/tests/fixtures/student-questions.v1.json` (kopi fra Kallimachos-målingen 16.11; 31 av 35 spørsmål har forventede kilder). Treff = minst én forventet kilde blant de fem første i `haven_docs_search`.

| Variant | Treff i topp 5 |
|---|---|
| Uten begrepsbro (`a57751c`) | 13/31 |
| Med begrepsbro fra CellScaffold #446 (WP1) | 19/31 |

Ingen spørsmål som traff før, faller ut. Bommer fortsatt: S02, S06, S07, S08, S12, S15, S16, S17, S20, S21, S26, S29. Testen `test_student_questions_top5_floor` holder gulvet på 19.

Merknad: målet i FORMAALSSPEC er «norsk ≥ engelsk». Settet finnes bare på norsk; en engelsk utgave må oversettes før den sammenligningen kan gjøres.

## docs-config

Filsiden er testet (`test_client_configs_start_this_server`): `.mcp.json` (Claude Code) og `.codex/config.toml` (Codex, bare i klarerte prosjekter) starter `Tools/HavenDocsMCP/haven_docs_mcp.py`; stdio-svar på `initialize` og `tools/list` gir de fire `haven_docs_*`-verktøyene. Ekte klienter: venter på WP13 (Macen).

## WP3 + WP4 (CellBase, Swift på Linux, 2026-11-23)

CellProtocol PR #114 (utkast), commit `1320a34`, grein `claude/egen-agent-avgrenset-lenke` fra main `b5f467a`.

| Hva | Resultat |
|---|---|
| `ScopedIdentityLinkTests` (8 nye: test.egen-agent.connect, auth-negative, recipient) | 8/8 grønne |
| `IdentityLinkRegistryTests` (hel lenke uendret) | 4/4 grønne |
| 190 CellBaseTests-filer uten CellApple/CellVapor, Docker `swift:6.1-noble` | 1489 tester, 27 røde; samme 27 røde på main uten endringen → ingen nye røde |
| Full `swift test` på macOS | venter: Macen var offline |
