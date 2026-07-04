# Rapport til Jørn Erik: erfaringer med AI-agentbasert rådgiverpanel

Dato: 2026-06-15

Status: arbeidsrapport basert på lokale HAVEN/CellProtocol-notater, agentlogger,
modelltester og ekstern dokumentsjekk. Dette er ikke en produktspesifikasjon,
ikke juridisk rådgivning og ikke en påstand om at alle nevnte modeller eller
leverandørvalg er klare for produksjon.

## Kortversjon

Vi har i praksis satt opp et rådgiverpanel ved å gi ulike AI-assistenter og
modelltyper tydelige roller: Codex for repo-groundet implementering og
dokumentasjon, Claude for designkritikk og langhorisont-rådgivning, ChatGPT for
språklige og konseptuelle alternativer, NotebookLM for kildegroundet syntese,
Gemini for multimodal/design-til-struktur analyse, og lokale modeller for å
teste hva som kan kjøre nær brukeren uten eksterne modellkall.

Det viktigste funnet så langt er at panelet fungerer best når det ikke behandles
som en stemmemaskin. Verdien kommer fra forskjeller: en agent finner svakheter i
pitch, en annen lager implementerbar struktur, en tredje sjekker
claim-risiko, og lokale modeller avdekker hvilke oppgaver som må ha
deterministiske sperrer. Mennesket må fortsatt eie beslutningen.

Den andre læringen er at agenter blir rådgivere først når kontekst,
kildegrunnlag og begrensninger er eksplisitte. Uten kildepakker, promptlag,
CurrentState-filer, claim-canon, valideringsscript og benchmark-cases sklir
arbeidet fort over i plausible, men utestede svar.

## Hva vi mener med "rådgiverpanel"

Det finnes ikke per i dag en egen implementert `AdvisorPanelCell` eller et
formelt panelobjekt i runtime. Når vi sier rådgiverpanel her, mener vi en
arbeidsform:

1. Samme problemstilling sendes til flere AI-flater med forskjellige roller.
2. Hver flate får et avgrenset mandat og et kontrollert kildegrunnlag.
3. Output lagres som daterte notater, kildepakker, testlogger eller forslag.
4. Kritiske påstander klassifiseres mot claim-canon og modenhetsmatrise.
5. Tekniske forslag valideres med kode, schema, Explore-kontrakter, benchmarks
   eller manuell gjennomgang.

Dette ligner mer på et teknisk review board enn en chattrad. Panelet skal ikke
gi "fasit"; det skal gjøre antakelser, gap, risiko og alternativer synlige.

## Hvordan vi har satt det opp

### 1. Felles kontekst og minne

Vi har laget et lokalt prompt- og dokumentasjonslag i
`CellProtocolDocuments`. Det viktigste er:

- `Prompts/SystemPrompt-Codex.md`: tynn inngang som peker agenten til riktig
  leserekkefølge.
- `Prompts/CoreContext.md`: delt kjerneforståelse.
- `Prompts/CurrentState.md`: kort checkpoint for aktivt arbeid, slik at nye
  agentrunder ikke starter fra null.
- `Prompts/Architecture.md`: stabil oversikt over repoets rolle og struktur.
- `Book/13_Agent_Instructions.md`: eksplisitte instruksjoner for kodende
  agenter som skal lage Cells og Skeleton UI.

Dette har vært viktigere enn først antatt. En agent uten oppdatert
CurrentState kan gi teknisk imponerende, men feilprioriterte råd.

### 2. Rollefordeling mellom agentene

| Rolle | Typisk verktøy/modell | Hva den brukes til | Viktig begrensning |
| --- | --- | --- | --- |
| Repo-groundet implementor | Codex | lese filer, endre docs/kode, kjøre tester, lage leveranser | må få klare repo-regler og validering |
| Strategisk/designkritisk rådgiver | Claude | UX-kritikk, arkitekturkritikk, pitch- og produktvurdering | kan lage sterke narrativer som må faktsjekkes |
| Språklig/konseptuell sparringspartner | ChatGPT | alternative formuleringer, forklaring, struktur | må kildegroundes for prosjektspesifikke fakta |
| Kildegroundet syntese | NotebookLM | pitch- og beslutningsgrunnlag fra kuraterte kilder | kvaliteten avhenger av kildepakken |
| Multimodal/design-til-struktur rådgiver | Gemini | tolke designskisser, foreslå Skeleton JSON, finne renderer-gap | må ikke finne opp keypaths eller runtime-evner |
| Lokal modellkandidat | Qwen/Gemma m.fl. | teste lokal co-pilot, klassifisering, korte forklaringer | skal ikke eie policy, consent eller handlinger |

Rollefordelingen har også gjort det lettere å se når en modell ikke bør brukes.
Et eksempel: lokale små modeller kan være gode til korte forklaringer etter at
systemet allerede har valgt en trygg handling, men de skal ikke avgjøre om en
sponsor får kontaktdata.

### 3. Kildepakker og daterte leveranser

For eksterne eller semi-eksterne oppgaver har vi brukt kildepakker. Den mest
tydelige er `GrunderAcademy_3min_Pitch_NotebookLM_2026-06-01`, der NotebookLM
fikk en samlet pakke med pitchvarianter, markedsnotater, scenarioantakelser og
claim-vakter. Det gjorde at NotebookLM kunne brukes som en kildegroundet
syntesepartner, ikke som en fri fantasiassistent.

Vi har også brukt daterte leveranser til rådgivningsrunder:

- `Model_Toolbox_Advisory_2026-06-11.md`
- `CoPilot_Conference_Small_Model_Helper_Assessment_2026-06-11.md`
- `Local_Model_Availability_Test_Log_2026-06-11.md`
- `Gemma4_Local_Runtime_Test_Log_2026-06-12.md`
- `Gemini_Design_Sketch_To_Skeleton_Pack/`

Dette gir et revisjonsspor: hva vi trodde da, hva som var testet, og hva som
bare var forslag.

### 4. Guardrails rundt claims og modenhet

Vi har egen claim-canon og modenhetsmatrise i DiMy-dokumentasjonen. De sier
blant annet:

- ingen global reputation
- ingen global person-ID
- ingen skjult atferdsprofilering
- ingen transferable credits, cash-out eller P2P value i v0
- value redistribution er forsknings- og pilotretning, ikke ferdig økonomisk
  mekanisme

Dette har hatt direkte effekt på hvordan agentene får jobbe. De kan foreslå
story, pitch og produktmuligheter, men må merke hva som er trygt, hva som krever
caveat, og hva som ikke kan sies enda.

### 5. Teknisk validering for agent-output

For CellProtocol/Skeleton-arbeid har vi flyttet oss mot en Explore-first
arbeidsform. Agenter skal ikke bare generere UI JSON som ser riktig ut. De skal
validere skeleton-bindings mot Explore-kontrakter før de går til preview eller
runtime.

Samme prinsipp brukes i modelltester: lokale modeller benchmarkes mot konkrete
norske co-pilot-cases, ikke bare "virker den smart?".

## Konkrete erfaringer så langt

### 1. Panelet hjelper mest når agentene er uenige

Claude-varianten av pitcharbeidet ga mer kommersiell konflikt og bedre
fortelling. Codex-varianten var mer presis på systemlogikk og broen til HAVEN:
data, samtykke, tilgang og verdi som etterprøvbare hendelser. ChatGPT-varianten
var mer menneskelig og enkel i deltakeropplevelsen. Ingen av dem var komplett
alene.

For en teknisk venn er dette kanskje det mest interessante: "ensemblet" er ikke
mest nyttig fordi flere modeller konvergerer, men fordi de feiler forskjellig.
Det gir et bedre beslutningsrom.

### 2. Kildegrounding virker, men er ikke automatisk sannhet

NotebookLM-oppsettet bekrefter at kildepakker er kraftige. Når kildene er
kuraterte, kan modellen lage mer relevant syntese og bedre investor-/juryspørsmål.
Men Google beskriver selv NotebookLM som kildegroundet, ikke ufeilbarlig.
Responsene må fortsatt sjekkes mot originalkildene.

Praktisk læring: kildepakken er en del av produktet. Hvis kildene er utdaterte,
for brede eller blander hypotese og fakta, blir rådgiverens output tilsvarende
uklar.

### 3. Agenter trenger negative regler, ikke bare mål

Noe av det mest nyttige i dette arbeidet er "ikke finn opp"-delen:

- Gemini-pakken sier eksplisitt at modellen ikke skal finne opp unsupported
  stack-properties, renderer-evner eller keypaths.
- Agentinstruksjonene sier at skeleton-bindings skal valideres mot Explore.
- Claim-canon sier hvilke claims som er forbudt inntil dokumentert.
- Modelltoolbox-notatet sier at ingen chatflate skal kjøre rå shell eller
  device actions uten signert review-intent.

Dette reduserer ikke bare risiko. Det gjør også output bedre, fordi agenten
blir tvunget til å skille mellom designønske, runtime-status og neste steg.

### 4. Lokale modeller er lovende, men ikke autoritet

De lokale testene ga mer nyanserte svar enn "lokalt er bra" eller "lokalt er
for svakt".

Representative funn:

- `Qwen3-8B-Q4_K_M` var beste lokale tekstbaseline i 8-case testen, med
  `38/48`.
- `Gemma 4 E4B QAT MLX/VLM` var beste Gemma-kandidat, med `36/48`, og er mer
  strategisk interessant for multimodal bruk på Apple Silicon.
- `Qwen3-1.7B` og mindre modeller er nyttige som baseline eller smale
  bakgrunnshjelpere, men ikke gode nok for deltakerrettet normalspråk eller
  policyavgjørelser.
- Sikkerhetsscore og "must mention" var fortsatt svakt nok til at
  deterministiske regler må ligge utenfor modellen.

Dette peker mot en arkitektur der modellen formulerer, forklarer og lager utkast,
mens regler, grants, consent, publisering, sletting og sponsor-data avgjøres av
deterministiske kontrakter.

### 5. Sandkassen avslørte en viktig runtime-grense

De første lokale modelltestene ble hindret av Codex-sandkassen: Metal/MLX var
ikke tilgjengelig der. Fra en usandboxed lokal prosess på M5 fungerte MLX/Metal.

Dette er en nyttig arkitekturleksjon: produksjonslignende lokal AI bør ikke
baseres på ad hoc kjøring inne i en coding-agent. Den bør ligge bak en
supervisert lokal prosess, for eksempel HAVENAgentD, med stabile provider-id-er,
loopback-grense, audit og prompt/resultat-policy.

### 6. "AI-agent" må bety reviewbar intensjon, ikke fri handling

I Chat Workbench- og Model Toolbox-notatene er retningen tydelig: ingen skjult
RAG, ingen skjulte eksterne modellkall, ingen skjult agenthandling. Agent bridge
skal være signert, reviewbar intent med allowlist, dry-run og eksplisitt
godkjenning for irreversible handlinger.

Det gjør panelet mindre flashy, men mer robust. Vi får agenter som hjelper til
med å strukturere handlinger, ikke agenter som stikker av med brukerens
rettigheter.

## Hva vi ikke har bevist enda

1. Vi har ikke en ferdig, runtime-implementert rådgiverpanelcelle.
2. Vi har ikke full produksjonsmodell for AgentD + lokale modeller + audit.
3. Vi har ikke full 40-case benchmark for alle lokale modellkandidater.
4. Vi har ikke validert markedsfunn statistisk; de er hypotesedannende.
5. Vi har ikke juridisk avklart value-return, credits, cash-out eller e-money
   grenser.
6. Vi har ikke bevist at syntetiske personaer predikerer ekte kunder. De er
   nyttige til story-kritikk, ikke markedssannhet.
7. Vi har ikke kryptografisk bevis for enkelte CLI-modellalias; lokale tester
   kan vise at aliaset virker, ikke garantere backend-identitet.

Dette er viktige forbehold. Rapporten bør ikke selge rådgiverpanelet som mer
modent enn det er.

## Foreløpig arbeidsmodell

For nye rådgiverpanelrunder bør vi bruke en enkel protokoll:

1. Definer beslutningen: hva skal faktisk avgjøres?
2. Lag kildepakke: hvilke filer, notater, data og eksterne kilder er lovlige
   for runden?
3. Velg roller: kritiker, implementor, kildeoppsummerer, claim reviewer,
   lokalmodell-tester, design reviewer.
4. Be hver agent levere i samme format:
   - anbefaling
   - antakelser
   - risiko
   - hva som må valideres
   - hvilke claims som er trygge/risikable/aspirerende
5. Sammenlign uenigheter, ikke bare konklusjoner.
6. Lag et menneskelig beslutningsnotat.
7. Flytt bare stabile ting inn i Book/spec; behold midlertidig rådgivning som
   datert leveranse.

## Anbefaling til neste fase

Jeg ville ikke bygget en egen `AdvisorPanelCell` først. Først bør vi kjøre
flere manuelle rådgivningsrunder med samme mal og se hvilke felt som faktisk
gjenbrukes.

Neste praktiske steg:

1. Lag en fast `AdvisoryRound` markdown/JSON-mal.
2. Kjør den på tre konkrete beslutninger: konferanse-pitch, AgentD local
   provider boundary, og sponsor/consent-reporting.
3. La minst to ulike modeller kritisere samme beslutningsnotat.
4. Kjør claim-review etter hver runde.
5. Når mønsteret er stabilt, vurder egne Celler:
   `AdvisoryRoundCell`, `ClaimSafetyReviewCell`, `EvidenceNeedCell` og
   senere `StoryScenarioRunnerCell`.

For Jørn Erik spesielt: det mest interessante å diskutere teknisk er kanskje
ikke modellvalget, men kontrollsløyfen. HAVEN-retningen er at AI-agenten kan
skrive, forklare, foreslå og validere, men autoritet ligger i contracts,
capabilities, ledger/audit, deterministic validators og eksplisitt menneskelig
review.

## Kildegrunnlag brukt i denne rapporten

Lokale kilder:

- `Prompts/SystemPrompt-Codex.md`
- `Prompts/Architecture.md`
- `Prompts/CurrentState.md`
- `Book/13_Agent_Instructions.md`
- `Deliverables/Model_Toolbox_Advisory_2026-06-11.md`
- `Deliverables/CoPilot_Conference_Small_Model_Helper_Assessment_2026-06-11.md`
- `Deliverables/Local_Model_Availability_Test_Log_2026-06-11.md`
- `Deliverables/Gemma4_Local_Runtime_Test_Log_2026-06-12.md`
- `Tools/CoPilotChatLanguageBenchmark/results/Benchmark_Run_Summary_2026-06-11.md`
- `Deliverables/Gemini_Design_Sketch_To_Skeleton_Pack/README.md`
- `Deliverables/GrunderAcademy_3min_Pitch_NotebookLM_2026-06-01/KILDEPAKKE.md`
- `Deliverables/GrunderAcademy_3min_Pitch_NotebookLM_2026-06-01/sources/dimy_value_redistribution/17_CONFERENCE_PERSONAS_AND_STORY_SIMULATION.md`
- `/Users/kjetil/Build/Digipomps/HAVEN/DiMyDocuments/ValueRedistribution/01_TERMINOLOGY_AND_CLAIMS_CANON.md`
- `/Users/kjetil/Build/Digipomps/HAVEN/DiMyDocuments/ValueRedistribution/05_ASSURANCE_MATURITY_MATRIX.md`

Eksterne kilder sjekket 2026-06-15:

- OpenAI Help Center: "Using Codex with your ChatGPT plan":
  https://help.openai.com/en/articles/11369540-getting-started-with-codex
- Anthropic Claude Code docs, "Overview":
  https://code.claude.com/docs/en/overview
- Google Blog, "Introducing NotebookLM":
  https://blog.google/innovation-and-ai/technology/ai/notebooklm-google-ai/
- Google AI for Developers, "Function calling with the Gemini API":
  https://ai.google.dev/gemini-api/docs/function-calling
