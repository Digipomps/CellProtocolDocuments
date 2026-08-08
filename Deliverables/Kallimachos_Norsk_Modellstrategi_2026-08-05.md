# Kallimachos: norsk modellstrategi — oversettelseslag eller annen modell?

- Dato: 2026-08-05
- Status: vurdering med anbefaling; grunnlag for Kallimachos v1
- Spørsmål fra Kjetil: skal vi legge inn et smart ekstra lag som oversetter
  slik at Apple Foundation Models kan brukes godt, eller er det bedre å få
  inn en annen modell?
- Beslutningseier: Kjetil

## Konklusjon (anbefaling)

**Ikke bygg et generelt oversettelseslag. Ruter etter oppgave i stedet:**

1. **Trinn 0–1 (deterministisk katalog, gap-lister, ferskhet): ingen modell.**
   Dette er mesteparten av bibliotekarens verdi og kan skipes raskt — viktig
   siden Kallimachos v1 skal komme fort.
2. **Apple FM beholdes der den er bevist god**: avgrensede seleksjons-
   mikrooppgaver med engelsk-innpakning og deterministisk gate (E3: 96 %
   seleksjon-kun, 85 % gated på holdt-ut test). Det er nøyaktig formen på
   formålsrutingen som *påkaller* Kallimachos. Pluss rene engelskspråklige
   økter ende til ende.
3. **Norsk friform-prosa (trinn 2–3): egen lokal modell via HAVENAgentD**,
   bak den stabile provider-id-kontrakten (à la
   `local.gemma4.e4b.qat.mlx-vlm`). Kandidatvalget (Qwen3-8B vs Gemma 4 E4B
   QAT) avgjøres av det allerede planlagte 40-cases norsk-benchmarket +
   bibliotekar-caser; Kallimachos binder seg til AgentD-kontrakten, ikke til
   én modell.

Et generelt oversettelseslag er den dårligste av de tre veiene for en
bibliotekar, av grunnene under. Det smale, gode «oversettelseslaget» finnes
allerede og skal beholdes: engelsk-innpakning for *avgrensede valg*, ikke for
prosa.

## Repo-sannhet (verifisert i dag)

| Fakta | Kilde |
| --- | --- |
| Apple FM tilgjengelig lokalt, `@Generable` bekreftet; norsk er ikke støttet språk | `Codex_Handoff_E3b_Norwegian_LoRA_Adapter_2026-07-13.md` |
| E3-baseline (norsk prompt, engelske kandidatbeskrivelser): seleksjon-kun 96 %, naiv strict 52 % (overselektjon 87 % JA-rate), med deterministisk resolver-gate 85 % på holdt-ut test | samme + `Small_Model_Purpose_Decomposition_Research_2026-07-11.md` |
| E3b (norsk LoRA-adapter for Apple FM): **ikke utført** — kun probe (`e3b_adapter_probe.swift`); adaptere må retrenes per basismodellversjon | `Tools/PurposeKnowledge/` + handoff-dokumentet |
| Norsk 8-cases lokalbenchmark: Qwen3-8B Q4 38/48 (79,2 %, best tekst); Gemma 4 E4B QAT MLX 36/48 (75 %, 8–11 s/case, multimodal vei, anbefalt strategisk kandidat) | `Gemma4_Local_Runtime_Test_Log_2026-06-12.md` |
| HAVENAgentD anbefalt som lokal modellgrense med stabil provider-id; deterministisk policy utenfor modellen | samme |
| Distribusjonsvei for lokal modell finnes (HAVENAgentD signert/notarisert pkg, Victoria-pilot) | `havenagentd-distribution`-sporet |

## Vurdering av oversettelseslaget (alternativ A)

Idéen: norsk spørsmål → oversett til engelsk → Apple FM svarer → oversett
tilbake. Fire problemer, i fallende alvorlighet:

1. **Kildetro brytes (formål F3).** Bibliotekarens kjerneløfte er ordrette
   sitater med kilde og ferskhet. Korpuset er i stor grad norsk; et
   RAG-svar krever da at *hentede tekstutdrag* også oversettes til engelsk
   for modellen, og svaret tilbake til norsk. Sitater som har vært gjennom
   to oversettelser er ikke lenger sitater. Å unnta sitatene fra
   oversettelse gir en modell som resonnerer på engelsk over tekst den ikke
   forstår kontraktsmessig — begge varianter underminerer svarkonvolutten
   (`citations`, `confidence`).
2. **Laget trenger sin egen modell uansett.** Apples oversettelsesrammeverk
   har ikke verifisert norsk-støtte (må ev. sjekkes mot gjeldende OS-versjon
   før noen satser på det). Da må det smarte laget selv skipe en
   MT-modell lokalt — og hvis vi først skiper en modell, gir en generativ
   norskkapabel modell mer verdi per gigabyte enn en ren
   oversettelsesmodell foran en engelsk 3B-modell.
3. **Latens og feilkomponering.** Tre modellpass (inn-oversettelse,
   generering, ut-oversettelse) på lokale hastigheter der ett Gemma-pass
   alt tar 8–11 s/case. Feil komponerer multiplikativt gjennom passene.
4. **E3 har allerede funnet lagets riktige størrelse.** Engelsk-innpakning
   virker godt når *modellens output er et avgrenset valg* (yes/no/unsure
   per kandidat) og en deterministisk gate står bak. Det generaliserer ikke
   til fri norsk prosa — det er nettopp overselektjons-/kvalitetsgapet E3
   dokumenterte.

**Delkonklusjon:** oversettelseslag som hovedstrategi avvises. Behold
engelsk-innpakningen for seleksjonsoppgaver; tillat i høyden en tydelig
merket oversettelses-fallback for visning, aldri for sitater.

## Vurdering av egen norskkapabel modell (alternativ B)

- **Kvalitet:** Qwen3-8B (79,2 %) og Gemma 4 E4B QAT (75 %) løser allerede
  norsk hverdagsspråk målbart på benchmarket; begge ligger langt over det
  Apple FM kan levere på norsk prosa (ustøttet språk, 52 % naiv strict på
  selv den enklere seleksjonsoppgaven).
- **Infrastruktur finnes:** MLX/GGUF-runtimes verifisert på M5;
  HAVENAgentD-grensen er anbefalt design; distribusjonsvei (signert pkg) er
  løst i Victoria-sporet. Bibliotekarens trinn 2–3 kobles på som ordinær
  lokal provider — ingen ny mekanikk.
- **Kostnader:** 4–7 GiB distribusjon per modell, minnetrykk på
  brukermaskiner, 8–11 s/case latens lokalt, og grammatikk-/skjemabegrenset
  dekoding må erstatte `@Generable` for strukturert output. Akseptabelt for
  trinn 2–3 (som uansett er opt-in kapabilitet), og trinn 4 (ekstern med
  samtykke) finnes for dyp kvalitet.
- **Modellvalg utsettes riktig:** Kallimachos binder seg til
  AgentD-provider-kontrakten. Qwen3-8B er beste tekstscore i dag; Gemma 4
  E4B er strategisk kandidat (multimodal, M5-akselerasjon, 128K kontekst).
  Det planlagte 40-cases-benchmarket + bibliotekar-caser avgjør.

## E3b-adapteren (norsk LoRA for Apple FM)

Beholdes som **parallelt eksperiment, ikke v1-avhengighet**:

- Oppsiden er avgrenset til seleksjons-mikrooppgavene (heve 85 % gated), ikke
  norsk prosa — en rank-32-adapter gjør ikke en 3B-modell med ustøttet språk
  til norsk skribent.
- Vedlikeholdskostnaden er reell: retrening per basismodellversjon, dvs. per
  OS-oppdatering.
- Om E3b lander godt, oppgraderer den påkallingsrutingen gratis — fint, men
  Kallimachos v1 venter ikke på den.

## Konsekvens for Kallimachos v1 (rask leveranse)

| Trinn | Modell | Status |
| --- | --- | --- |
| 0–1: katalogoppslag, oversikt, gap, ferskhet, audit | Ingen (deterministisk) | Kan bygges nå; ingen modellavhengighet |
| Påkalling/formålsruting | Apple FM, engelsk-innpakning + deterministisk gate | Mønster bevist (E3); gjenbrukes |
| 2–3: norsk oppsummering/friform med ordrette sitater | Lokal modell via HAVENAgentD (Qwen3-8B eller Gemma 4 E4B QAT) | Runtime verifisert; benchmark avgjør valg |
| Engelske økter | Apple FM kan bære mer, ellers samme ruting | — |
| 4: dyp resonnering | Ekstern frontier via tillitspakke | Som designet |

## Målingsplan før endelig modellvalg

1. Utvid det norske benchmarket med bibliotekar-caser: oppsummer-med-ordrett-
   sitat, hull-svar («det har jeg ikke i katalogen»), invitasjonsformulering
   (F4-tonen), avslagsrespekt.
2. Kjør Qwen3-8B og Gemma 4 E4B QAT gjennom AgentD-grensen på samme caser og
   scoringskontrakt som 8-cases-loggen.
3. Akseptansekrav med claim-review-blikk: sitatfelt skal være eksakt
   tekstmatch mot kilde (automatisk sjekk); «må ikke nevne»-dimensjonen
   dekker overpåstander.
4. Beslutning tas på tallene; taperen beholdes som dokumentert alternativ i
   provider-katalogen.

## Claim ledger

| ID | Påstand | Type/styrke | Vurdering |
| --- | --- | --- | --- |
| M1 | Generelt oversettelseslag underminerer sitatfidelitet og gir netto dårligere bibliotekar enn norskkapabel lokal modell. | design/causal, moderated | Støttet av E3-tallene (prosa-gapet) og F3-kravet; motargument (null ekstra distribusjon) faller fordi laget selv trenger en MT-modell. |
| M2 | Engelsk-innpakning + deterministisk gate er fortsatt riktig bruk av Apple FM for påkallingsruting. | project capability, assertive | Målt: 96/85 % på holdt-ut test; ingen ny mekanikk. |
| M3 | Lokal norskkapabel modell via AgentD dekker trinn 2–3 godt nok for v1. | predictive, moderated | 75–79 % på generelt norsk-benchmark; bibliotekar-casene i målingsplanen verifiserer domenet før endelig valg. |
| M4 | E3b-adapteren endrer ikke denne konklusjonen uansett utfall. | scoping, assertive | Adapteren adresserer seleksjon, ikke prosa; vedlikehold per OS-versjon gjør den uegnet som v1-avhengighet. |
