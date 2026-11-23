# PLAN — Egen Claude og Codex mot HAVEN (MCP-adapter)

Oppgavemappe: `PDD_egen-agent-mcp_2026-11-20` · Skrevet 2026-11-23 · G2 godkjent 2026-11-23
Bygger på FORMAALSSPEC.md iterasjon 1 (G1 2026-11-21) og bildene i `images/` (G1-GUI 2026-11-23).

## Fakta planen bygger på (lest 23.11 i kode)

| Fakta | Kilde |
|---|---|
| CellScaffold har en autentisert bridgehead: `GET /bridgehead/:pubId/:bridgeId` og `/bridgehead/session` (multiplex, maks 64 kanaler). Opptaket beviser at klienten eier en nøkkel; det gir ingen celletilgang. | CellScaffold main `af7f375`, `Sources/App/Services/ScaffoldBridgeRuntime.swift:44–75`, `Sources/ScaffoldKit/AuthenticatedBridgeIngress.swift` |
| Den gamle uautentiserte bridgeheaden er fjernet. | `Sources/App/Controllers/VaporBridgehead.swift:13–14` |
| Python-klienten snakker samme opptak (`org.haven.bridge-channel.v1`). | PyCellProtocol `README.md`, `src/cellprotocol/interop/channel.py` |
| **En lenke «samme entitet» gir eiermakt over alle celler i domenet.** `GeneralCell.authorizationEvidence` setter `ownerReferenceMatches: true, ownerProofValid: true` når spørreren har en verifisert lenke; `approvedScopes` på lenken brukes ikke i den avgjørelsen. | CellProtocol `669850b`, `Sources/CellBase/Cells/GeneralCell/GeneralCell.swift:2339–2350, 2163–2173`; `Sources/CellBase/Identity/IdentityLinkingModels.swift` (`IdentityLinkRecord.approvedScopes`) |
| CellBase har ingen vilkårstype for delegering til en agent og ingen for tillatte mottakere. Vilkårene som finnes: Grant, Lookup, Login, ProvedClaim, ColdStorage, ConditionalEngagement, LifecycleAlertAccess, LifecycleFunding, ReplayGuarantee. | `Sources/CellBase/Agreement/Condition/Implementation/` |
| `EntityScaffoldEnrollment` i CellScaffold har en signert forespørsel → godkjenning → fullføring → tilbaketrekking for et scaffold som kobler seg til en person, med `requestedCapabilities` og en tillatt liste av nøkkelstier. | `Sources/App/Cells/EntityScaffoldEnrollment/EntityScaffoldEnrollmentCell.swift` |
| HavenDocsMCP: 19/19 tester grønne 20.11. | `Tools/HavenDocsMCP/tests` |

### Hva funnet om lenker betyr for F2

FORMAALSSPEC F2 sier at agenten er «en godkjent utvidelse av studentens entitet». Hvis det bygges som en lenke «samme entitet», får agenten alt studenten har, i hele domenet. Det bryter F3 (bare godkjente celler), F3b (bare utkast) og F4 (mottaker sjekkes). Planen bygger derfor utvidelsen som en **delegering i Agreement**: studenten signerer et `AgentDelegation`-dokument for agentens nøkkel, og cellene slipper agenten inn bare gjennom et nytt vilkår, `DelegatedAgentCondition`, i sitt Agreement. Slik følger agenten regelen «tilgang bare via Agreement-vilkår». Flaten og ordene i bildene endres ikke. Ingen eksisterende lenke eller eierregel endres.

## Endring i oppførsel du bør vite om

- Celler uten vilkåret `RecipientCondition` er stengt for agenter (ditt valg i §6.3). Etter at koden er ute, ser agenten bare HAVEN-dokumentasjonen til vi legger vilkåret på cellene studentene bruker. WP8 gjør det for «Mine dokumenter»; resten tas celle for celle.
- Ingen eksisterende Agreement endres. Et Agreement uten `DelegatedAgentCondition` slipper aldri inn en agent.

## Arbeidspakker

Utfører: **Claude** skriver kode og tester i skyen og lager PR; **Mac** betyr bygg og tester på Macen din (Remote Control, arbeidstre under `/Volumes/Backup/build`) før en PR tas ut av utkast; **Kjetil** er dine valg og det du må gjøre selv.

| WP | purposeRef (blad) | Hva | Filer | Test(er) som skal bli grønne | Utfører |
|---|---|---|---|---|---|
| 0 | quality.build-and-regression | Baseline: CellProtocol main (`swift test`), PyCellProtocol (`pytest`), GoCellProtocol (`go test ./...`), CellScaffold CI på main, HavenDocsMCP. Tallene i TESTRESULT.md før første endring. I tillegg måling: kobler en Python-klient med egen nøkkel seg til `/bridgehead/session` på staging, og hva svarer en celle uten Agreement? | — | test.build, test.regression (baseline); §2-raden «Staging-vertens Agreement-sjekk» målt | Mac (Swift, staging-måling), Claude (Py, Go, CI) |
| 1 | docs-without-account | `.mcp.json`, `AGENTS.md`, `CLAUDE.md` i roten av CellProtocolDocuments som starter HavenDocsMCP; norsk søk ved å kopiere begrepsbroen (`commons_librarian_term_bridges.v1.json` fra CellScaffold #446) inn i HavenDocsMCP; kort veiledning `MasterHAVEN26/EGEN_AGENT.md` | CellProtocolDocuments | test.egen-agent.docs-config, test.egen-agent.docs-norsk | Claude; klienttesten i WP13 |
| 2 | swift-python-parity | Kontrakt: verktøyliste, JSON inn og ut, avvisningskoder, `AgentDelegation` og de to vilkårene. Swift lager gylne fixtures | `contract/egen-agent-mcp-tools.v1.json` (utkast i denne mappen), CellProtocol `fixtures/interop/agent-delegation-v1/` | test.egen-agent.parity (fixtures finnes) | Claude |
| 3 | connect-entity, declare-provider | CellBase: `AgentDelegation` (signert av studenten: agentens offentlige nøkkel, maskinnavn, leverandør, celler og tillatelser, gyldig til, tilbaketrekkingsreferanse) og `DelegatedAgentCondition` (spørreren er agentnøkkelen, delegeringen er gyldig og ikke trukket, rektor oppfyller resten av Agreementet, tillatelsen ligger innenfor både delegeringen og Agreementet) | CellProtocol `Sources/CellBase/Agreement/AgentDelegation.swift`, `Condition/Implementation/DelegatedAgentCondition.swift` + tester | test.egen-agent.connect, test.egen-agent.auth-negative (Swift) | Claude, Mac |
| 4 | provider-recipient, others-consent | CellBase: `RecipientCondition` (tillatte mottakere: `local`, `anthropic`, `openai`, region). Mangler vilkåret, får en agent nei (`recipient_not_allowed`). For celler med innhold fra flere (chat): hvert innslag gis bare når forfatterens vilkår tillater mottakeren | CellProtocol `Condition/Implementation/RecipientCondition.swift` + tester | test.egen-agent.recipient, test.egen-agent.others-consent (enhet) | Claude, Mac |
| 5 | swift-python-parity | Samme `AgentDelegation`, `DelegatedAgentCondition` og `RecipientCondition` i PyCellProtocol og GoCellProtocol, testet på fixturene fra WP2. Go får bare vilkårene, ikke adapteren | PyCellProtocol `src/cellprotocol/agreement/`, GoCellProtocol | test.egen-agent.parity (vilkår), test.egen-agent.auth-negative (Py, Go) | Claude |
| 6 | approve-revoke | Vertscelle `cell:///OwnAgents` i CellScaffold: tar imot signert forespørsel fra agenten over bridge (lagres som ventende, gir ingen tilgang), godkjenning med passkey (fersk innlogging som i `IdentityLinkFreshAuthEvidence`), lagrer delegeringen, «Koble fra» trekker den fra neste kall, utløp. Koder `extension_revoked`, `extension_expired` | CellScaffold `Sources/App/Cells/OwnAgents/*`, registrering | test.egen-agent.approve, test.egen-agent.revoke | Claude; Mac/CI bygg |
| 7 | visibility | Logg per agent hos studentens entitet: tid, verktøy, celle, utfall og kode. FlowElement `haven.own-agents.call.v1`, aldri innhold eller prompt | `OwnAgents` + `OwnAgentsLog.swift` | test.egen-agent.log | Claude |
| 8 | approve-revoke (flate), read-documents, write-back | Flaten «Egne agenter» som skjelett etter de godkjente bildene; «Mine dokumenter» får `DelegatedAgentCondition` + `RecipientCondition` (studentens eget valg ved godkjenning); verktøyene les, søk, lagre utkast. Lagre utkast lager en ny `DocumentInstance` som utkast og deler ingenting | `PersonalCopilotConfigurationFactory` (ny seksjon), RichDocument/DocumentInstance-vilkår | test.egen-agent.read, test.egen-agent.write, test.gui.parity mot `images/` | Claude; Mac for Binding-paritet |
| 9 | research-data-level | Verktøyet `research_data_get` med N-nivå fra Agreement. Til PDD «Forskningsdata» har landet, svarer verktøyet `not_available` | `OwnAgents` + forskningsdata-cellene | test.egen-agent.research-level | Claude; venter på PDD Forskningsdata |
| 10 | device-key, tools-by-agreement | Python-adapter `pycell mcp` i PyCellProtocol: stdio MCP, nøkkel i systemets nøkkellager eller fil med 0600, skriver fingeravtrykket i terminalen, sender forespørselen, kobler til `/bridgehead/session`, viser bare verktøy for celler med gyldig delegering, merker skrivende verktøy | PyCellProtocol `src/cellprotocol_mcp/` + `pycell mcp` i CLI | test.egen-agent.device-key, test.egen-agent.agreement-only | Claude |
| 11 | device-key, swift-python-parity | Swift-adapter `haven-mcp` som eget produkt i CellProtocol (macOS: nøkkelring; Linux: fil 0600). Samme verktøy og svar som Python | CellProtocol `Sources/HavenMCP/` (kjørbart mål, avhenger bare av CellBase) | test.egen-agent.device-key, test.egen-agent.parity | Claude, Mac |
| 12 | no-model-credentials | Statisk sjekk i CI for begge adaptere: ingen lesing av `~/.claude`, `~/.codex`, `ANTHROPIC_API_KEY`, `OPENAI_API_KEY` eller nøkkelringoppføringer for dem; ingen vertsnavn api.anthropic.com/api.openai.com. Nettverkslogg under WP13 | `ci/no-model-credentials.sh` i begge repo | test.egen-agent.no-credentials | Claude |
| 13 | real-clients | Ekte Claude Code og Codex CLI på Macen mot lokal CellScaffold: docs-config, connect, read, write, revoke. Så Linux i skyen med Python-adapteren mot lokal vert (uten modellklient). Versjoner noteres | `TESTRESULT.md#real-clients`, skjermbilder `images/klient-*.png` | test.egen-agent.real-clients, test.egen-agent.docs-config | Mac; du logger inn i Claude Code og installerer Codex |
| 14 | root | Staging: FORESPOERSEL til HAVEN-Deploy etter grønt bygg på main; så e2e med en studentkonto og Claude Code på Macen | `/Users/kjetil/Build/Digipomps/HAVEN/HAVEN-Deploy/_handoff/RELEASE/FORESPOERSEL-egen-agent-<dato>.md` | test.egen-agent.e2e | Claude skriver forespørselen; du fletter og slipper |
| 15 | real-clients | Pilot med to eller tre studenter etter veiledningen, uten hjelp | `PILOT.md` | test.egen-agent.pilot | Kjetil (inviterer), Claude (skriver opp) |
| 16 | everything-works | Book-kapittel om egne agenter («Last verified against code»), TESTRESULT og ACCEPT bygget fra bevisfilene og sjekket av en uavhengig tråd | CellProtocolDocuments `Book/` | test.build, test.regression, test.docs-updated, test.status-current | Claude |

## Leveranse i PR-er

1. CellProtocolDocuments (denne PR-en, #56): WP1, kontrakten fra WP2, veiledningen.
2. CellProtocol: WP2-fixtures, WP3, WP4, WP11. Utkast til Mac-kjøring er grønn.
3. PyCellProtocol: WP5 (Python) og WP10.
4. GoCellProtocol: WP5 (Go, bare vilkårene).
5. CellScaffold: WP6–WP9, etter at CellProtocol-PR-en er flettet og pinnet.
6. FORESPOERSEL til HAVEN-Deploy (WP14).

## Dataflyt

Se `dataflow.md`.

## Avhengigheter som må virke

| Avhengighet | Status 23.11 | Hva som skjer uten den |
|---|---|---|
| Autentisert bridgehead på staging | Kode på main; om staging-utgaven har den, er ikke målt (WP0) | Adapteren kan ikke koble til staging; WP13 kjøres mot lokal vert |
| PDD «Dele dokumenter» (delte dokumenter) | G2 spurt 20.11, i arbeid | F3a gjelder bare egne dokumenter |
| PDD «Forskningsdata» | G1 venter | F3c svarer `not_available` |
| Samtaler på ChatCell (CellScaffold #495) | utkast | F4b testes bare på enhetsnivå, ikke i ekte felles chat |
| Begrepsbroen fra CellScaffold #446 | flettet (sjekket 23.11) | — |

## Ikke i denne planen

- Go-adapter (bare vilkårene i Go).
- Agenten deler, publiserer eller sletter.
- Studentens agent som modellkilde for andre (regelen står i modellkilde-PDD-en, WP18).
- Endring av lenker «samme entitet» i GeneralCell. Funnet over meldes til deg, men endres ikke her.
- HavenAgentD.

## Risiko

- **CellScaffold-baselinen er rød** (39 kjente røde AppTests 22.11 i en annen tråd). WP0 skriver lista, og «ingen nye røde» og «grønn» rapporteres hver for seg.
- **Nye vilkår i CellBase** må gi samme utfall i Swift, Python og Go. Fixtures fra Swift først, så portene.
- **Passkey-godkjenning** gjenbruker fersk innlogging fra lenkeflyten; om den kan kalles fra en ny celle uten endring i CellBase, er ikke målt.
- **Tid:** CellProtocol-PR-en må flettes og pinnes i CellScaffold før WP6. Hver Swift-kjøring går på Macen.
