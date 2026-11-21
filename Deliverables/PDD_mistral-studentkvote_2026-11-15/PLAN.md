# PLAN — DiMy-modeller med mikrobetaling, Mistral-kvote for studentene

Oppgavemappe: `/Users/kjetil/Build/Digipomps/HAVEN/CellProtocolDocuments/Deliverables/PDD_mistral-studentkvote_2026-11-15/` · Skrevet 2026-11-21 · G1 godkjent 20.11, G1-GUI godkjent 20.11 · **G2 godkjent 2026-11-21**

Målt mot CellScaffold `272580b` (main 20.11). Fakta planen bygger på:
- `FirstPartyAIProvider.swift:31` har fast `https://api.openai.com/v1/responses`. `FirstPartyAIConfiguration.swift:69` godtar bare nøkler som starter med `sk-`.
- `ModelCatalogModel` har `priceUSDPerMTok` (listepris, Double) og `status`, men ikke `offeredByDiMy`, `region` eller en tariff i NOK.
- Kallimachos «kapabel» er `claude-opus-5-5` på operatørens nøkkel (#487, merget 20.11).
- `ModelSourceEligibility.swift` finnes (kildevelgeren, #454).
- Butler har sitt eget målespor på main med 16 `Butler*`-tjenester (#435 og senere), blant annet `ButlerInvocationService`, `ButlerBYOKUsageLimiter` og `ButlerTopUpPolicy`.
- Rolle-VC-en fra Informasjonssystemer (CellProtocolDocuments #46) er ikke merget.
- CellScaffold #493 (utkast 20.11, tråden «Gjør Sara klar til å utforske HAVEN») gir alle kontoer på staging uten egen nøkkel Opus 5.5 i Kallimachos og Architect, på operatørens nøkkel (`AI_GATEWAY_OPERATOR_FALLBACK_*`). Den har et eget tak på 2 USD per konto per døgn og 50 USD per måned, og en egen ledger på disk i USD, utenom PaymentGate.

## Arbeidspakker (1:1 mot bladformål)

| WP | purposeRef | Hva | Utfører | Test(er) som skal bli grønne | Artefakter |
|---|---|---|---|---|---|
| 0 | — | Baseline: `swift build --build-tests` og `ci/run-tests.sh` på main, med testtall | Claude (Linux-CI på et utkast) + Mac via Remote Control | test.build, test.regression | TESTRESULT.md#baseline |
| 1 | dimy-liste | Nye felt i `ModelCatalogModel`: `offeredByDiMy`, `servingClass`, `region`, `pricePerMTokInput`/`Output` (NOK, desimalstreng), `tariffEffectiveDate`. Ny nøkkel `catalog.offered`. Mistral small merkes som tilbudt i data, men av til drift slår den på. `check_catalog.py` utvides | Claude | T-LISTE | kontrakt-JSON + fixtures |
| 2 | mikrobetaling | Førstepartstjenesten gjøres leverandøruavhengig: tariff og endepunkt hentes fra den tilbudte katalogoppføringen, med én adapter per API-stil (OpenAI responses, OpenAI-kompatibel chat completions, Anthropic messages) og en forseglet nøkkel per leverandør. Reservasjon, avregning, kvittering og avstemming er uendret | Claude | T-MIKRO | — |
| 3 | mistral | Mistral-adapter: fast EU-URL, ingen omdirigering, ingen fallback, brukstall fra `usage`. Live-kallet venter på ditt ja og nøkkelen | Claude, så Kjetil | T-MISTRAL, T-MISTRAL-LIVE | fixture fra ekte svar |
| 4 | dagsgrense | Grense per student per døgn (Europe/Oslo) i tillegg til det samlede døgnbudsjettet. Avvises før reservasjon | Claude | T-DAG | — |
| 5 | tak | Semesterkvote: «Gi kvote til kullet» på driftssiden kaller `issuePrepaid` for hver student med rollen. Uten kvote blir svaret `payment_required`, som oversettes til `student_quota_exhausted_term` | Claude | T-TAK | — |
| 6 | hvem | Vilkår: ProvedClaimCondition på `InformasjonssystemerRoleCredential` (student, MasterHAVEN26) med TrustedIssuer. `role_status_unknown` får egen kode. Mens #46 er åpen, testes det mot en fixture-utsteder, og ekte kobling skjer når #46 lander | Claude | T-HVEM, test.cell.auth-negative | — |
| 7 | en-port + svarform | Én Swift-port, `HostedModelAccess.resolve(requester:, purpose:)` → kilde eller avslag med `quota`-objekt og kode. Alle studentverktøy kaller den | Claude | T-EN-PORT, T-SVARFORM | dataflow.md |
| 8 | betaler-velger | Kallimachos' faste rute på operatørens nøkkel (`capable` uten valg) erstattes av porten: DiMy-hostet (kvote), egen nøkkel (#433-sporet) eller ingen. **#493 rives ikke.** Den er mellomløsningen til porten virker, og flyttes deretter inn: Opus 5.5 blir en DiMy-tilbudt modell i katalogen, #493-ledgeren erstattes av målesporet, og taket på 2 USD per døgn blir dagsgrensen for Opus. Hvem fallbacken gjelder for («alle uten egen nøkkel» eller studentrollen), avgjør du | Claude | T-BETALER, og #493-testene (`AIGatewayOperatorFallbackTests`) grønne til de er erstattet | migreringsnotat |
| 9 | kallimachos-modell + lokal-forst | Kildevelgeren «Hvem skal svare?» i Kallimachos-skeletonet (som bildet), koblet til `ModelSourceEligibility`. Lokal modell brukes først når den svarer | Claude | T-KALLIMACHOS-KILDE, T-LOKAL | skeleton-JSON |
| 10 | synlig | Kvotekort, avslagskort og «Svart av …» i Kallimachos, likt på web og i Binding (Swift) | Claude; Binding på Mac via Remote Control | T-SYNLIG, test.gui.parity, test.gui.load-time, test.skeleton.* | skjermbilder ved siden av bildene |
| 11 | drift | `/admin/ai-usage` utvides som bildet: modeller DiMy tilbyr (på/av, pris), grenser og forbruk per student. Leverandørmodus krever bekreftelse. Siden er fortsatt Leaf-HTML | Claude | T-DRIFT | skjermbilde |
| 12 | mikrobetaling (samling) | Butler flyttes over på samme målespor. Overlevering til Codex etter WP2 (pkg.std.codex-handoff), uten at Claude rører `Butler*` | Codex | Butler-suitene grønne og T-MIKRO for Butler | handoff/README.md |
| 13 | — | Dokumentasjon (ModelCatalog.md, Kallimachos, FirstPartyAI), TESTRESULT, ACCEPT, FORESPOERSEL til HAVEN-Deploy | Claude | test.docs-updated, test.status-current | FORESPOERSEL-fil |

## Levering

| PR | WP | Repo | Avhenger av |
|---|---|---|---|
| A | 1–5, 7 | CellScaffold | ingenting |
| B | 6 | CellScaffold | at #46 lander for ekte kobling (fixture før det) |
| C | 8–10 | CellScaffold | A, og at #493 er merget (C bygger på den) |
| D | 11 | CellScaffold | A |
| E | 12 | CellScaffold (Codex) | A |

Hver PR er et utkast til Linux-CI er grønn og Binding er sjekket på Mac. Claude merger, tagger og deployer ikke. Staging går via FORESPOERSEL til HAVEN-Deploy etter verifisert bygg.

## Det som krever ditt ja underveis

0. **Forholdet til #493:** avgjort 20.11 23:17Z, «Begge, i samme målespor». Mistral er standard i studentkvoten med 3 kr per dag. Opus er et eget valg med 2 USD per dag fra #493. Begge flyttes inn i målesporet i WP8.

1. Mistral-nøkkelen og at leverandørmodus slås på (WP3 live, WP11). Inntil da kjører alt i simulert modus.
2. Prisen (tariffen) for Mistral small, med kilde og dato.
3. Å slå på Claude Haiku 5.5 og en OpenAI-modell senere, hver med pris.

## Dataflyt (kort)

Student → Kallimachos (persona) → `HostedModelAccess.resolve` (rolle-VC → døgngrense → tjenestebudsjett) → kildevelger → FirstPartyAIService (reserver i PaymentGate → adapter → mål tokens → avregn → kvittering) → svar med `quota` og «Svart av …». Avslag stopper før reservasjon og transport.
