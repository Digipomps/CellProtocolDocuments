# Brief til Astra — formål og Celler som styring av AI-agenter, målt mot leverandørenes begrensninger

Dato: 2026-09-08 · Fra: Losen (Claude) · Til: Astra (gpt-6-astra via Codex) · Bestiller: Kjetil
Mappe: `CellProtocolDocuments/Deliverables/Formaal_Celler_Agentstyring_Vurdering_2026-09-08/`
Type: **analyse og diskusjon, ikke implementering.** Ingen kodeendringer. Du kan lese hele HAVEN-repoet (`/Users/kjetil/Build/Digipomps/HAVEN`), men skriv bare i denne mappen.

## 0. Bestillingen (ordrett, Kjetil 2026-09-08)

> Vurder hvor godt formål og Celler er for å styre og begrense AI agenter i forhold til de begrensningene AI selskapene bruker. Diskuter dette med Astra - og vurder hvor bra dette kan fungere i sin nåværende form og om det eventuelt er mer funksjonalitet vi bør legge til

## 1. Formålet med vurderingen (alt måles mot dette)

**Rot:** Avgjøre om — og hvor godt — *formål* (Purpose/Goals) og *Celler* (CellProtocol: Identity, Agreement/Contract/Grant med RWXS, Resolver, Explore-kontrakter, policy ceilings, signerte kvitteringer) egner seg til å styre og begrense AI-agenter, sammenlignet med begrensningene AI-selskapene bruker; og finne hvilken funksjonalitet som mangler.

| ID | Delformål | Test på svaret |
|---|---|---|
| F1 | Sammenligne *det som er implementert* i HAVEN i dag mot leverandørenes mekanismer *slik de er i dag* — ikke visjon mot visjon | Hver påstand om HAVEN er merket `[belagt: fil]`, `[vurdering]` eller `[usikker]`; visjon skilles eksplisitt fra runtime |
| F2 | Finne hva som er *kategorisk* annerledes (hvem eier begrensningen, hvor den håndheves, hva som er bevis) — og hva som bare er kjent teknikk med nytt navn | Svaret navngir minst én ting som er nytt og minst én ting som ikke er det |
| F3 | Vurdere robusthet mot kjente angrep (prompt injection, purpose laundering, confused deputy, tool hijacking, approval fatigue) | Hvert angrep får «løses strukturelt / løses bare i prompt / løses ikke» |
| F4 | Vurdere praktisk brukbarhet (kostnad, friksjon, kan en vanlig bruker eller en Palazzo-kelner faktisk forholde seg til det) | Svaret tar stilling til om dette kan drives uten Kjetil/Claude/Codex i løkka |
| F5 | Foreslå konkret funksjonalitet, prioritert, med hva hver løser og hva som fortsatt ikke løses | Liste med prioritet, løser/løser ikke, og anslått størrelse |
| F6 | Motargumenter: hvor er HAVEN-tilnærmingen svakere, overflødig eller feil | Minst tre reelle innvendinger, ikke stråmenn |

## 2. Faktagrunnlag — HAVEN slik det faktisk er i dag (hentet fra repoet 2026-09-08)

Verifiser gjerne selv; filstiene er relative til HAVEN-roten.

1. **Purpose er erklært intensjon, aldri utledet, og gir ingen myndighet i seg selv.** `CellProtocolDocuments/Book/09_Purpose_Interests.md`. Purpose kan brukes som *betingelse* i Contracts (f.eks. `purpose=moderation` før sletting).
2. **Goals finnes som deterministiske, sideeffektfrie predikater.** `GoalDefinition` med evaluator-typer `state-predicate`, `event-predicate`, `human-confirmation`, `semantic-location`, `semantic-time`, `network-ping`, `contract-probe`, `gui-smoke`, `composite`; `GoalEvaluationEngine` evaluerer bare eksplisitt innsendte observasjoner; `GoalEvaluationCell` er live `GeneralCell`. `CellProtocol/Sources/CellBase/PurposeAndInterest/GoalDefinition.swift`, `GoalEvaluationEngine.swift`, `CellProtocol/Sources/CellBase/Cells/Purpose/GoalEvaluationCell.swift`; `Deliverables/Purpose_Goal_Evaluation_Analysis_2026-06-11.md` (481 tester grønne 2026-06-11). Kobling til ekte GPS/klokke/GUI var *ikke* på plass da.
3. **Autorisasjon er eksplisitt og kapabilitetsbasert.** Agreement (ønske) ≠ Contract (beslutning). Grant i `rwxs`-form (read/write/execute/**storage**); Storage ≠ videresending/disclosure. Conditions (VC, endorsement, tid, domene, gruppeterskel, *caller må erklære matchende Purpose*). Issuer-signert, subject-bundet snapshot (ikke bilateral signering). `TrustedIssuers`-kvitteringer for VC. Resolver er håndhevingsgrense for støttede veier. `Book/04_Agreements_Contracts.md` (verifisert mot kode 2026-07-13).
4. **Formålsbundet ekstern handling (A1/A4-v1).** Normativ regel: *et formål kan innsnevre en rettighet, aldri opprette, utvide eller arve en.* Låser: én effekt = ett primærformål; exact match (parent impliserer ikke child); facets er ikke autoriserende; ukjent formål (`purpose://prompt.unknown`) feiler lukket; CellConfiguration er ceiling, ikke grant; trust package er evidens, ikke myndighet; owner path er ikke unntak; `s` ≠ disclosure; alle digests (purpose, action, destination, data-manifest, plan, config, policy, taxonomy, payload) bindes i intent/context/receipt. Receipt skiller `decisionStatus` fra `executionStatus`. **Håndhevet på nøyaktig én bane:** `cell:///PurposeBoundAIGateway` → `ai.invokePurposeBound` (én prompt + valgfri systemprompt til én godkjent leverandør openai/anthropic/mistral; ingen tools, planlegging, orkestrering, metadata). Ikke håndhevet på legacy `ai.invoke`, HavenAgentD, scriptceller eller transport. Trusselmodell T1–T15 med eksplisitte residualer. `Deliverables/Purpose_Bound_External_Action_Contract_2026-08-03/` (README, THREAT_MODEL, A4_*), `CellScaffold/Sources/App/Cells/AI/AIGatewayPurposePolicy.swift`.
5. **AIGatewayCell tool-policy:** default `denyAll`; en `toolPolicyDecision` som feiler lukket ved `denied`. Men for *tillatte* verktøy er håndhevingen en **systemprompt-setning** («Tool policy: declared tools for this agent are X. Do not use or claim any tool outside this set»). **Det finnes ingen tool-calling-løkke fra modell til celler i CellScaffold i dag** — ingen `tool_calls`/`tool_use`-håndtering i provider-adapterne; modellen er tekst inn / tekst ut. `CellScaffold/Sources/App/Cells/AI/AIGatewayCell.swift` (ca. linje 2010 og 2104), `AIGatewayModels.swift` linje 69–135. `AIAssistantThreadCell` bruker `toolPolicy: .denyAll`.
6. **Purpose Knowledge Base:** rot `purpose://root` = «Alle mennesker er like mye verdt», taksonomi med facets, `purpose://prompt.unknown`, hallusinasjons-evalueringsport (draft: ≤1 % hallusinerte refs, ≤3 % ubelagte påstander, ≥90 % «unknown» når evidens mangler, 0 sideeffektbrudd). `ExecutablePurposeGroundingCell` med sideeffektfri `purpose.knowledge.resolve` og `purpose.context.pack`. `Book/23_Purpose_Knowledge_Base.md`.
7. **Rådgiverpanel-celle** `cell:///AdvisorPanel`: besluttet 2026-09-05, ikke levert; skal nekte å kjøre uten en rådgiver med `stance: challenge`; persona i egen celle så profilinnhold aldri sendes til modell uten eksplisitt ja. `CellScaffold/Deliverables/PDD_radgiverpanel-og-persona_2026-09-05/STATUS.md`. Blokkert bl.a. av at ingen live modellkjøring er mulig nå (kreditt).
8. **Arbeidskø for AI-utførere** (kandidat, ikke levert): jobbpost bærer aldri en kommando; ingen vilkårlig shell; en jobb kan ikke gi seg selv videre sandkasse (`no-self-escalation`, polarity prohibited); celle-utfører får bare tekst inn / tekst ut. `Deliverables/PDD_arbeidsko-ai-utforere_2026-09-07/FORMAALSSPEC.md`. HAVEN-Deploy F5: rådgiveragent er read-only, hver påstand har bevis, målene G1–G7 er predikater som regnes deterministisk — «LLM-en forklarer og prioriterer, den finner ikke på fakta». `HAVEN-Deploy/FORMAAL.md`.
9. **HavenAgentD** (macOS-daemon): allowlistede Shortcuts/AppleScript-handlere, remote-intent-kø med audit og nonce, e-postutkast uten autosending, `SecretCredentialCell` med redigert metadata i cellestate og hemmelighet i Keychain. `HavenAgentD/README.md`.
10. **Correspondence-MCP** er grensesnittet der *eksterne* agenter (Claude «Losen», Victorias «Lille Robot») handler inn i HAVEN med klart definerte og begrensede rettigheter: agenten kvitterer selv på innkommende post; sending krever eksplisitt ja fra eier. Meldinger skal inn i HAVEN som first-class (`Book/33_Correspondence_First_Class.md`).
11. **Visjon, ikke implementert:** Kallimachos med formålstre (rot: menneskelikeverd og positivt bidrag), Goals som både prompts og matematiske uttrykk/event-predikater, distribuert over scaffolds med fusjon etter audit, undersøke egen bias, «bidra positivt» som målbart formål, formål om at miljøet må være stabilt nok til å bære prosjektets formål (rekursivt til Jorden). Celle-autentisitet (celler beviser egen identitet som Identity) er under vurdering, ikke bygget.
12. **Kjente hull som repoet selv oppgir:** A4 bare på én bane; ingen per-Grant purpose/action (V2-port lukket til use case finnes); eksisterende `Condition` kan ikke evaluere dynamisk formål/action/digest; sandbox for scriptceller ikke implementert (T6); JSON-schemaene er ikke i Explore; golden-digests er syntetiske; ingen fysisk kontroll etter at data er avslørt; ingen regulatorisk etterlevelse påstås. `Purpose_Bound_External_Action_Contract_2026-08-03/DECISION_LOG.md` («Eksplisitte current limitations»).

## 3. Referanseramme — leverandørenes begrensninger (status sept. 2026)

- **Treningstid (leverandøreid, ugjennomsiktig for bruker):** RLHF / constitutional AI / refusal-trening; OpenAI Model Spec (2026-08-18) med kommandokjede *root > system > developer > user > guideline*; sitert/verktøy-innhold er utrusted som standard og har ingen myndighet med mindre delegert; «agreed-upon scope of autonomy» (tillatte delmål, akseptable sideeffekter, når man skal spørre); bekreftelse ved irreversible handlinger; høyrisikohandlinger alltid forbudt uten eksplisitt autorisasjon.
- **Kjøretid, leverandøreid:** systemprompter, input/output-klassifikatorer (moderation, cyber/bio), bruksvilkår, rate limits.
- **Kjøretid, deployer-eid (infrastruktur, ikke prompt):** permission modes (Claude Code `default/acceptEdits/plan/bypass`), `PreToolUse`-hooks med allow/deny, tool-allowlister, OS-sandbox (Seatbelt/bubblewrap+seccomp), Codex `read-only/workspace-write/danger-full-access` + `approval-policy on-request/never` + managed `requirements.toml`, Agents SDK `require_approval` per verktøy, MCP OAuth med audience-bundne tokens, audit-logg, HITL interrupt/resume.
- **Regulatorisk:** EU AI Act art. 50 (transparens: bruker skal vite at det er AI) gjelder fra 2026-08-02; art. 12 (automatisk logging av hele handlingskjeden) og art. 14 (menneskelig tilsyn, «human-on-the-loop»: forhåndsdefinerte handlingsgrenser, kontinuerlig overvåking, rask inngripen) for høyrisiko fra 2027-12-02; deployer bærer ansvar også med tredjeparts modell.
- **Kjente svakheter i leverandørmodellen** (fra bransjelitteraturen): «The model is not a policy engine» — promptbaserte begrensninger omgås ved injection og manipulerte tool-resultater; approval fatigue (rapportert ~93 % godkjenning → tilsyn blir støy); brede tokens gir confused deputy; begrensningene er globale, ikke kontekstuelle; brukeren kan ikke definere egne formål; ingen delt, maskinlesbar intensjon mellom to parter; kvittering = logg, ikke bevis bundet til intensjon.

## 4. Sammenligningsdimensjoner (bruk disse)

| D | Dimensjon | Leverandør | HAVEN (i dag) |
|---|---|---|---|
| D1 | Hvem eier begrensningen | leverandør, dernest deployer | eier av entitet/celle; motpart via Contract |
| D2 | Hvor den håndheves | vekter → prompt → tool-gate → OS-sandbox | Resolver/Cell-grense + policy ceiling (én bane); ellers prompt |
| D3 | Hva som er bevis | logg | signert kvittering bundet til intent-digests (én bane); Contract-receipt |
| D4 | Granularitet | global / per app / per tool | per keypath × formål × destinasjon × dataklasse × payload-digest |
| D5 | Komposisjon over flere aktører | ingen delt intensjon | Agreement/Contract mellom identiteter; correspondence |
| D6 | Robusthet mot injection/laundering/confused deputy | prompt-avhengig unntatt tool-gate/sandbox | modelloutput er *proposal*; policy leser validerte wire-felt (én bane) |
| D7 | Kostnad | tokens + menneskelige godkjenninger | predikater er billige; taksonomi og Agreements koster oppsett |
| D8 | Ved ukjent | ofte fail open / spør | fail closed (`prompt.unknown`) |
| D9 | Dekning i dag | hele agentens handlingsrom (tool-gate) | én provider-bane + MCP-grensesnitt; ingen tool-løkke |

## 5. Spørsmål — svar på alle, i rekkefølge, med overskrift per spørsmål

**Q1.** Er premisset riktig — at formål + celler er en annen *klasse* av begrensning enn leverandørenes (eier-styrt, datanær, bevisbar) — eller er det capability-based access control + policy engine + attestasjon med nytt navn? Hva er faktisk nytt, og hva er kjent teknikk (nevn gjerne Macaroons, ZCAP-LD, UCAN, OPA/Cedar, Biscuit, SPIFFE, XACML purpose-binding, GDPR purpose limitation)?

**Q2.** Dekning: gitt at det ikke finnes noen tool-løkke fra modell til celler, styrer formål/celler i praksis bare (a) hva som sendes til leverandør og (b) hva en ekstern agent får gjøre via MCP/correspondence. Er «agenten kan bare foreslå, cellene bestemmer» en reell styrke, eller en illusjon av kontroll fordi det interessante handlingsrommet (Claude Code, Codex på Mac-en, HavenAgentD) ligger *utenfor* cellene?

**Q3.** Robusthet: gå gjennom T1–T15 i trusselmodellen pluss approval fatigue og tool hijacking via MCP. For hver: løses strukturelt av celle-modellen, løses bare i prompt, eller løses ikke. Vær konkret om hva som er avhengig av at *modellen* oppfører seg.

**Q4.** Goals som deterministiske uttrykk vs prompts: hvor stor andel av styringen av en agent kan realistisk gjøres med predikater (state/event/location/time/contract-probe), og hvor går grensen der det trengs en modell (og dermed en ny angrepsflate)? Er «Goal som prompt» i det hele tatt en begrensning, eller bare en instruks?

**Q5.** Sammenlign `PurposeBoundActionIntent` + kvitteringer med Model Spec sin «agreed-upon scope of autonomy» og med Claude Code permission modes / `PreToolUse`-hooks / Codex `requirements.toml`. Er HAVENs form *bedre* (og for hvem), eller et mer tungvint uttrykk for det samme? Hva kan HAVEN låne direkte?

**Q6.** Komplementaritet: bør HAVEN *forutsette* leverandørens begrensninger (defense in depth) — og hva må HAVEN da IKKE prøve å gjøre selv? Hvilke leverandørbegrensninger kan HAVEN ikke erstatte selv om det ville?

**Q7.** Hva mangler? Foreslå funksjonalitet, prioritert (P0–P3), med: hva den løser, hva den *ikke* løser, anslått størrelse (S/M/L), og hvilken eksisterende del av CellProtocol den bygger på. Ta stilling til minst disse kandidatene og legg til egne: (a) tool-løkke der modellens foreslåtte handling går gjennom Contract + formål + ceiling før utførelse; (b) per-Grant purpose/action (V2); (c) celle-autentisitet; (d) sandbox for scriptceller; (e) effect-receipts (`executionStatus` med transportbevis); (f) revokasjon/utløp distribuert; (g) design mot approval fatigue (hva skal *aldri* spørre, hva skal *alltid*); (h) injection-isolasjon (skille system/tool-input i wire-format); (i) taksonomi-governance for formål; (j) flerpartskontrakter; (k) «Skal ikke»-formål (prohibited polarity) som harde skranker; (l) måling av «bidra positivt»; (m) budsjett/kvote som Goal; (n) EU AI Act art. 12/14-logg og tilsyn som celle.

**Q8.** Claim safety: hvilke offentlige påstander om «AI-styring via formål» er belagt av det som finnes i dag, og hvilke er ikke? Gi tre formuleringer som er trygge, og tre som ville vært overclaims.

**Q9.** Den sterkeste innvendingen mot hele tilnærmingen — den som, hvis den er riktig, betyr at vi bør slutte eller snu. Og hva ville overbevise deg om at den er feil.

## 6. Format på svaret

- Skriv svaret til **`ASTRA_SVAR.md`** i denne mappen (ikke til `_svar.md`-filer; det er Codex sin `-o`-fil). Skriv underveis, seksjon for seksjon, så delvis svar er lesbart. Avslutt filen med linjen `<!-- ASTRA RUNDE 1 FERDIG -->` når du er ferdig.
- Norsk. Presist, to-the-point, ingen smiger. Motsi der du mener det.
- Merk påstander om HAVEN med `[belagt: <fil>]`, `[vurdering]` eller `[usikker]`. Ikke finn på keypaths, filer eller kapabiliteter; sjekk i repoet når du er i tvil.
- Ingen kodeendringer. Ingen andre filer enn `ASTRA_SVAR.md`.
- Hold svaret innenfor ca. 3 000–4 500 ord. Kvalitet foran bredde.
