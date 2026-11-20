# PLAN — språkmodell som deltaker i felles chat

Oppgavemappe: `PDD_modell-i-felles-chat_2026-11-15` · Skrevet 2026-11-20 · G1 og G1-GUI godkjent 2026-11-20 · G2 bedt om

Grunnlag: FORMAALSSPEC.md iterasjon 2 (§6: 1a, 2a, 3a, 4a) og de seks godkjente bildene i `images/`. Kode lest denne økten: CellProtocol `669850b` (main 20.11), CellScaffold `272580b` (main 20.11).

## Hva planen bygger på (lest i kode 20.11)

- **Mønsteret finnes allerede.** `CellScaffold/Sources/App/Cells/TextAnalysis/TextAnalysisRoomCell.swift:162–186` (analyserommet, PR #465) eier en CellBase `ChatCell`, setter adgangsvilkåret `member` på den, og bruker chattens medlemsliste som rommets. Samtaler gjør det samme: hver samtale eier sin `ChatCell`.
- **Modellkall med testleverandør finnes.** `TextAnalysisModelProposals.swift:26` (`protocol TextAnalysisModelClient`) og `TextAnalysisAIGatewayClient.swift` (kall via `cell:///AIGateway`, `toolPolicy: denyAll`). Modellen i chatten får en egen klient etter samme mønster, med en falsk klient i testene.
- **Feiltekster for modell som ikke svarer finnes.** `ScaffoldKit/AIGateway/ModelRouteUnavailability.swift` (PR #445, flettet 19.11) klassifiserer feilene fra gatewayen. Chatten bruker den, ikke egne tekster.
- **Den felles adgangsdelen fra dokumentdeling (`InvitationAdmission`) finnes ikke på CellProtocol main.** Planen bygger derfor på `ChatCell` slik den er, og legger `modelConsent` der. Lander `InvitationAdmission` først, flyttes vilkåret dit i samme PR (se planbytter).

## Arbeidspakker

Utfører: **Claude** = denne tråden i skyen (CellBase og ScaffoldKit bygges i Docker `swift:6.1-noble`, Python og Go direkte). **Mac** = samme tråd via Remote Control på din Mac (lange kjøringer, CellScaffold App, Binding og Xcode), slik du valgte 18.11. **Kjetil** = fletting og staging. Ingen pakke går til Codex.

| WP | purposeRef | Hva | Utfører | Tester som skal bli grønne | Leveranse (§3) |
|---|---|---|---|---|---|
| WP0 | purpose://quality.build-and-regression | Baseline: full testkjøring av CellProtocol, CellScaffold, Binding, PyCellProtocol og GoCellProtocol på main, fra rene kloner. Kjente røde skrives ned, så «ny feil» er alt utenfor den listen | Mac + Claude | test.build, test.regression (baseline) | TESTRESULT.md#baseline |
| WP1 | purpose://candidate.modell-i-felles-chat.model-is-participant | CellBase `ChatCell`: deltakere får `kind` (`person`/`model`), meldinger får `authorKind`, `askedBy`, `model`, `contextCount`. Gamle meldinger leses som `person` | Claude | test.modellchat.deltaker-merket | CellProtocol PR |
| WP2 | purpose://candidate.modell-i-felles-chat.admission-condition | `ChatAdmissionCondition.modelConsent` og et samtykkeregister i `ChatCell`: foreslå, si ja, si nei, trekke ja, fjerne modellen. Vilkåret holder bare når alle nåværende menneskelige medlemmer har sagt ja. Sjekkes ved hvert kall | Claude | test.modellchat.alle-maa-si-ja, test.modellchat.fjern, test.cell.auth-negative | CellProtocol PR |
| WP3 | purpose://candidate.modell-i-felles-chat.external-opt-in | Eget samtykke for ekstern modell (§6 spm. 3a): `externalModelConsent` i samme register, eget vilkår for Mistral | Claude | test.modellchat.ekstern-krever-ja | CellProtocol PR |
| WP4 | purpose://candidate.modell-i-felles-chat.cross-language | Swift skriver interop-fixtures for WP1–WP3 (sant, usant, trukket, ny deltaker, ekstern av/på) i `fixtures/interop/v1` | Claude | test.modellchat.vilkaar-fixtures (Swift-siden) | CellProtocol PR |
| WP5 | purpose://candidate.modell-i-felles-chat.cross-language | Python: samme vilkår, register og meldingskontrakt i `cells/chat.py`, og en innplugget modelleverandør med falsk leverandør i testene (§6 spm. 4a) | Claude | test.modellchat.vilkaar-fixtures, test.modellchat.interop | PyCellProtocol PR |
| WP6 | purpose://candidate.modell-i-felles-chat.cross-language | Go: det samme i `chat.go` | Claude | test.modellchat.vilkaar-fixtures, test.modellchat.interop | GoCellProtocol PR |
| WP7 | purpose://candidate.modell-i-felles-chat.chat-on-agreement | CellScaffold: hver Samtaler-tråd eier en CellBase `ChatCell` (mønster fra analyserommet). Invitasjon og invitasjonslenke gir medlemskap via chattens invitasjonsbevis, ikke via lagret deltakerliste. Co-Pilot-lageret holder bare oversikten over hvilke samtaler du har | Claude (bygg) + Mac (App-tester) | test.modellchat.samtale-er-chatcell, test.cell.auth-negative | CellScaffold PR |
| WP8 | purpose://candidate.modell-i-felles-chat.chat-on-agreement | Flytting av lagrede samtaler: tråder i dagens format flyttes til `ChatCell` med samme deltakere, meldinger og rekkefølge. Kjøres én gang ved oppstart og kan kjøres igjen uten skade | Claude + Mac | test.modellchat.migrering | CellScaffold PR |
| WP9 | purpose://candidate.modell-i-felles-chat.addressed-only, .bounded-context | Modelldeltakeren: reagerer bare på «Spør modellen» eller `@modell`, henter spørsmålet og høyst 20 meldinger etter at modellen kom inn, og poster svaret som modellen gjennom sin egen kontrakt | Claude | test.modellchat.bare-naar-spurt, test.modellchat.kontekstgrense | CellScaffold PR |
| WP10 | purpose://candidate.modell-i-felles-chat.asker-route | Rutevalg per spørrer: Qwen lokalt som standard, Mistral gjennom kvoten fra tråden «Gi studentene Mistral med dagsgrense». Requester mot gatewayen er den som spør. Til kvoten finnes, er Mistral-knappen der, men gir «ikke tilgjengelig ennå» | Claude | test.modellchat.rute-er-spørrerens | CellScaffold PR |
| WP11 | purpose://candidate.modell-i-felles-chat.untrusted-output | Svaret renses til ren tekst, kortes til 4 000 tegn, går gjennom samme moderering som andre meldinger, og kan ikke utløse handlinger (`toolPolicy: denyAll`) | Claude | test.modellchat.svar-er-ren-tekst | CellScaffold PR |
| WP12 | purpose://candidate.modell-i-felles-chat.honest-failure | Feil til den som spurte: `ModelRouteUnavailability` og kvotens avslagskoder blir kortet «Modellen svarte ikke», bare for den som spurte, med «Prøv med Mistral» når det går | Claude | test.modellchat.feil-til-spørrer | CellScaffold PR |
| WP13 | purpose://candidate.modell-i-felles-chat.swift-native, purpose://gui.ways-in-are-reachable | Samtaler-skjelettet i `PersonalCopilotConfigurationFactory` får elementene fra de godkjente bildene. Playwright-fixturen oppdateres fra Swift. Lagrede Samtaler-skjeletter oppgraderes som for modellkilde-panelene (#454) | Claude | test.skeleton.purpose-actions-reachable, test.skeleton.no-unreachable-elements | CellScaffold PR + skjermbilder web |
| WP14 | purpose://candidate.modell-i-felles-chat.swift-native | Binding: CellProtocol-pinnen løftes i begge filene, Samtaler åpnes i Binding, og skjermbildene legges ved siden av de godkjente | Mac (Xcode) | test.gui.parity (Binding) | Binding PR + skjermbilder |
| WP15 | purpose://quality.build-and-regression | Full bygg og regresjon på Mac for alle fem repoene mot grenene. Ingen ny rød utenfor baselinen fra WP0 | Mac | test.build, test.regression | TESTRESULT.md#build, #regression |
| WP16 | purpose://candidate.modell-i-felles-chat.root | Når du har flettet, og bygget er grønt: FORESPOERSEL til HAVEN-Deploy. Deretter to nye kontoer på staging gjennom hele flyten | Claude (forespørsel), Kjetil (fletting, staging) | test.modellchat.e2e-to-studenter, test.gui.load-time | Kjørende flate på staging |
| WP17 | pkg.std.everything-works | ACCEPT.md og TESTRESULT.md bygges fra bevisfilene og kontrolleres av en uavhengig tråd. Lærdommer føres | Claude | test.status-current, test.docs-updated, test.gui.parity | ACCEPT.md |

## Rekkefølge og fletting

1. WP0, så WP1–WP4 i én CellProtocol-PR. Den må flettes av deg før noe som bruker den kan lande, fordi en pin skal peke på CellProtocol main.
2. WP5 og WP6 parallelt med CellScaffold-arbeidet, i hver sin PR.
3. WP7–WP13 i én CellScaffold-PR (utkast mens CellProtocol-PR-en venter). Draft-PR-ens Linux-CI er byggesjekken underveis. App-testene kjøres på Macen.
4. WP14 og WP15 på Macen når alle PR-ene er grønne.
5. WP16 etter at du har flettet. Jeg fletter, tagger og deployer ikke selv.

## Avhengigheter som kan stoppe roten (fra §2)

| Avhengighet | Hva skjer hvis den ikke er klar |
|---|---|
| Lokal Qwen på staging (tråd A) | Alt bygges og testes med falsk leverandør. E2E på staging venter, eller kjøres med Mistral alene |
| Mistral-kvoten (PR #42, G1 venter fortsatt) | WP10 bygges mot kontrakten i PR #42 (`quota`-objektet og avslagskodene). Mistral-knappen sier «ikke tilgjengelig ennå» til kvoten er levert |
| Opus 5.5 med dagsgrense per student (tråden «Gjør Sara klar til å utforske HAVEN», besluttet 20.11, nøkkelalias `anthropic` fra CellScaffold #446) | Mulig tredje rute ved siden av Qwen og Mistral. Den er ekstern, så den går under samme gruppe-ja som Mistral (§6 spm. 3a). Den tas bare med i WP10 hvis Kjetil sier ja ved G2 |
| Studentrollen (Informasjonssystemer, PR #46) | Påvirker bare hvem som får Mistral-kvote, ikke denne PDD-en |

## Avledede tester mot pakker

Alle rader i FORMAALSSPEC §5 er dekket av minst én pakke over. Testene av Agreement-adgang sammenligner sortert-nøkkel-JSON, ikke `ValueType` direkte (`lesson.valuetype-equality-false-for-objects`). Nye testklasser i CellScaffold føres i `ci/test-filter.txt`.

## Dataflyt

    Student A trykker «Spør modellen»
      → Samtaler (CellScaffold) sjekker at A er medlem (ChatCell member) og at modelConsent holder
      → modelldeltakeren henter spørsmålet + ≤ 20 meldinger etter at modellen kom inn
      → AIGateway invokeAI, requester = A, rute = A sitt valg (Qwen lokalt / Mistral med A sin kvote)
      → svar renses (ren tekst, ≤ 4 000 tegn, ingen verktøy)
      → ChatCell sendMessage som modellen, med authorKind=model, askedBy=A, model, contextCount
      → alle medlemmer ser svaret; ved feil ser bare A kortet «Modellen svarte ikke»
