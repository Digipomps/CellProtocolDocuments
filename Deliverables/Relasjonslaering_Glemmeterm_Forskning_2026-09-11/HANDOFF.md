# HANDOFF — Glemmeterm (Ojas regel) mot dagens relasjonslæring i CellProtocol

Dato: 2026-09-11. Fra: Losen (Claude, Cowork-tråd i HAVEN-Deploy). Til: neste tråd (Claude eller Codex) som forsker videre.
Kø-poster: **HD-0050** (denne forskningen, eier claude) og **HD-0051** (clamp-funnet, avhenger av HD-0050). Kommandoer: `python3 tools/hd.py task show HD-0050` fra `HAVEN-Deploy/`.
Stier i dette dokumentet er relative til HAVEN-mappen (repo-navn først). Hvor HAVEN ligger på maskinen er en enhetsinnstilling.

## 0. Formål (mål hvert steg mot dette)

Kjetil skal kunne avgjøre, på målt grunnlag, om en aktivitetsdrevet glemmeterm (Ojas regel, foreslått av Vegar 9.9.2026) skal inn i CellProtocols relasjonslæring som v2 av oppdateringsregelen — uten at replaybarhet fra eventlogg, determinisme, forklarbarhet per kant eller lokal-først brytes.

**Måles ved:** `RAPPORT.md` i denne mappen som (a) besvarer S1–S8 under med belegg, (b) inneholder målinger fra replay-simulering der samme logg kjøres med dagens regel og med glemmeterm, (c) ender i én anbefaling — INN (med parameterforslag og migrasjonsplan) eller AVVIST (med begrunnelse) — og (d) lister spørsmålene som skal tilbake til Vegar.

Et dokument som beskriver hvordan dette *kunne* undersøkes, oppfyller ikke formålet. Målinger gjør det.

## 1. Hva som utløste dette

- 9.9.2026 sendte Losen Vegar et spørsmål om «Hebbian learning slik han bruker begrepet» (fem punkter). Svaret kom samme dag (kanal `kjetil-vegar-codex-d`, sequence 2), ble kvittert 11.9 og besvart 11.9 (sequence 3). Fullteksten av begge ligger i `Vegar_svar_2026-09-09.md` her. Vegar sier eksplisitt at ingenting i svaret er upublisert eller sensitivt.
- Svaret til Vegar lover at «en egen tråd forsker videre på dette mot eksisterende funksjonalitet», og at vi melder tilbake med konkrete spørsmål før vi ber om hans formelle notat med utledning. Denne tråden er det løftet.

## 2. Vegars forslag i kortform (les kildefilen før du siterer ham)

- Hebbian = lokale, uovervåkede regler der en kobling styrkes av korrelert aktivitet mellom de to nodene den binder; belønningsmodulerte (tre-faktor) varianter hører med. Globalt feilsignal, ekstern label og ren tidsdecay hører ikke med.
- Ren Hebb (Δw = η·x·y) er positiv tilbakekobling og ustabil. Forslaget er Ojas regel: **Δw_ij = η·y_j·(x_i − y_j·w_ij)**, der leddet −η·y_j²·w_ij er en glemmeterm proporsjonal med kantens styrke og post-nodens aktivitet. Vektvektoren inn til en node konvergerer mot norm 1; kantene inn til samme node konkurrerer om et budsjett. For lineær node lærer vekten første prinsipalkomponent av inputkorrelasjonen.
- Aktivering er et kontinuerlig nivå i [0,1] innenfor en episode (fra et formål startes til det avsluttes); «samtidig» = samme episode. Utfallet (lykkes/feiler) skalerer η, ikke x eller y.
- Tilstanden bor på kanten (vekt + tidspunkt). Tidsbasert decay holdes som eget, versjonert policy-lag multiplisert inn ved lesing, ikke bakt inn i lagret vekt.
- Antakelser som må holde: lokalitet; (tilnærmet) sentrerte input — ellers dominerer alltid-aktive noder; liten η; lineær/svakt ikke-lineær post-node for PCA-tolkningen; deterministisk episodedefinisjon.
- Mot CellProtocol: dagens regel bounder hver kant for seg → mange kanter nær 1 inn til samme formål (vektinflasjon). Forslaget er ikke å bytte regel, men å vurdere glemmetermen som tillegg i suksessregelen. Noa-decay beholdes uendret.

## 3. Dagens funksjonalitet — verifisert 11.9.2026 mot kode

Lest i checkouten av `CellProtocol` (gren `pdd/tillitspakke-agentflaate`, HEAD 4096760). De fire filene under er identiske med `origin/main` (c430a24, 2026-09-10), sjekket med `git diff --quiet origin/main -- <fil>`. **Verifiser på nytt i din økt** — ikke stol på dette avsnittet alene (R-A2).

- Kode: `CellProtocol/Sources/CellBase/PurposeAndInterest/RelationalLearningEngine.swift` (966 linjer, siste commit d9d9514 2026-07-14), `RelationalLearningModels.swift`, `RelationalDecayPolicy.swift` i samme mappe. Celleintegrasjon: `CellProtocol/Sources/CellApple/PurposeAndInterest/Cells/RelationalLearningCell.swift`.
- Dokumentasjon: `CellProtocol/Docs/RelationalLearning_Architecture_NO.md` (sist oppdatert 2026-03-02) og `CellProtocol/Docs/RelationalLearning_Bruk_og_Drift_NO.md`.
- Tester: `CellProtocol/Tests/CellBaseTests/RelationalLearningEngineTests.swift` (7 tester: replay-determinisme, Noa-monotoni, policy-cutover, journal-restore, avvisning av ugyldig replay/for stor journal/feil kantform) og `RelationalLearningCellContractTests.swift`. Kjøres på Mac: `swift test --filter RelationalLearningEngineTests` — ikke i Cowork-VM-en.
- Eksisterende forskningsramme: `CellProtocol/commons/prompts/relational_learning_deepresearch_prompt.md`. Spørsmål 1 der («alternativer til dagens update-regel som gir bedre stabilitet ved sparse data uten å bryte replaybarhet») er nøyaktig det Vegars forslag svarer på. Leveranseformatet og avgrensningene i den prompten gjelder fortsatt. `relational_learning_code_assistant_prompt.md` gir de ikke-forhandlingsbare kravene til en eventuell implementering (additivt API, alt replaybart, ingen skjulte mutasjoner, explainability, lokal-først, versjonert decay).
- Modell: `RelationalEdge(fromNode: purpose, relationType, toNode: interest | entityRepresentation | contextBlock, weightStored ∈ [0,1], lastReinforcedAt, decayProfileId, decayParamsVersion, metadata)`. `purposePurpose` finnes i modellen, men brukes ikke i læringsregelen (kjent grense, Docs §10).
- Episode: `RelationalPurposeSession` opprettes ved `PurposeStarted`; ved `Succeeded/Failed` bygges eligibility-traces fra aktive/passive interesser, aktive/passive entiteter og aktive kontekstblokker (kontekst krever confidence ≥ 0.6, skaleres 0.5·confidence). Engine linje 239–336.
- Regel (`reinforcedWeight`, linje 629–645): suksess `w' = clamp01(w + a·e·(1−w))`, feil `w' = clamp01(w − a·e·w)`. Eksplisitt preferanse setter `w' = 0.6`. Standard (`RelationalLearningDefaults`): unknownWeight 0.1, alphaSuccess 0.08, alphaFail 0.05, eligibility aktiv 1.0 / passiv 0.3 / kontekst 0.5·confidence.
- Hver vektendring er én `RelationalWeightUpdateEvent` per kant per episode, idempotent på event-ID, med deterministisk replayrekkefølge (`emittedAt`, `eventType`, `eventId`, kanonisk payload).
- Tidslag: ved skåring `effectiveWeight = clamp01(weightStored · R(Δt))` med `RelationalDecayPolicy` (profil `noa`, `version`, `effectiveFromTimestamp`, dobbel sigmoid t1=7d, t2=30d, k1=1.2, k2=0.6, rMin=0.05; `kind` kan også være `none`). Policy byttes ved cutover uten å skrive om historikk.
- Skåring (`scorePurposes`, linje 429–503): per formål `raw = Σ effectiveWeight · eligibility` over kanter med eligibility > 0 i kontekstøyeblikket; `score = RelationalMath.normalizedScore(raw)` som er **`clamp01(raw)`** (`RelationalLearningModels.swift` linje 518–520). Explain per kant: effectiveWeight, contribution, policy-id/versjon/parametre. Sortering: score synkende, tie-break på `purposeId`.

## 4. Funn gjort i denne økten (start her — verifiser F3 først)

- **F1.** Vegars lesning av dagens regel stemmer med koden. Bekreftet ham dette 11.9.
- **F2.** Tidslaget ligger allerede som eget, versjonert policy-lag multiplisert inn ved lesing — hans punkt 4 er oppfylt i dag. Glemmetermen er et tillegg til *læringslaget*, ikke en erstatning for Noa. Ikke bygg tidslaget på nytt.
- **F3. Skåren metter.** `normalizedScore = clamp01(raw)`. Ti aktive kanter på unknownWeight 0.1 gir raw 1.0 før noe er lært; seks kanter etter én suksess (0.1 + 0.08·1·0.9 = 0.172 hver) gir 1.03 → 1.0. Formål med mange kanter blir uskillbare i toppen, og rekkefølgen faller tilbake på `purposeId` alfabetisk. Dette er Vegars «vektinflasjon», synlig direkte i rangeringen. Registrert som **HD-0051**. Regnestykket er utledet fra defaultverdiene, ikke kjørt — **skriv en test som viser det før du bygger videre.**
- **F4.** Eligibility er aldri sentrert (1.0 / 0.3 / 0.5·c, alltid > 0). Vegars antakelse «sentrerte input» holder ikke hos oss uten tiltak: Oja finner da retningen med størst rå gjennomsnitt, og alltid-aktive noder (f.eks. en kontekstblokk som alltid er til stede) dominerer.
- **F5.** Kartlegging til Oja: post-node = formålet, y = raw-skåren (Σ w·x) eller clamp av den, x_i = eligibility per kant i episoden, w_ij = weightStored. Vegars episode = vår `RelationalPurposeSession`; utfallet velger allerede a og fortegn (belønningsmodulert). Merk: kantene peker *fra* formålet i datamodellen, men formålet er semantisk post-noden som aggregerer.
- **F6.** Ingen event- eller modellfelt for en glemmeterm finnes. En v2 må være additiv: nye parametre i `RelationalLearningConfig` og/eller egen versjonert policy à la `RelationalDecayPolicy` med `effectiveFromTimestamp`, slik at gammel logg replayer likt som før cutover.

## 5. Forskningsspørsmål — besvar alle, hvert svar med belegg

- **S1 Formell kartlegging.** Skriv Ojas regel i vår notasjon og vis hva −η·y²·w blir per kant når y er raw-skåren (lineær) og når y er clamp01(raw). Vis at oppdateringen fortsatt er lokal (bare x_i, y_j, w_ij) og kan uttrykkes som én `RelationalWeightUpdateEvent` per kant. Avgjør om y skal beregnes fra lagret vekt eller effektiv vekt (med Noa) — tid inngår i det siste, og det påvirker replay-determinisme. *Måles ved:* tabell med dagens regel og v2 side om side, og et argument for at replay av samme logg gir identisk tilstand.
- **S2 Simulering.** Syntetiske episodelogger: sparse, tett, med drift, med preferanseendring, med en alltid-aktiv kontekstnode, med formål som har 2, 6 og 20 kanter. Kjør dagens regel og v2 på samme logg. Mål: andel formål med score = 1.0 (metning); rangeringskonsistens (f.eks. Kendall τ over tid og mellom kjøringer); episoder til ny topp etter preferanseendring; stabilitet ved sparse data; vektnorm per formål over tid; bit-likhet ved replay av samme logg to ganger. *Måles ved:* tall i rapporten og én kommando som reproduserer dem.
- **S3 Sentrering.** Hva gjør Oja med våre positive eligibility-verdier (F4)? Sammenlign: ingen sentrering; sentrering per formål over glidende vindu (kostnad: ny tilstand som selv må være event-sourced); en ren «budsjett»-variant (normaliser vektnormen per formål) uten PCA-tolkning. Anbefal én.
- **S4 Samspill med Noa.** Glemmeterm = aktivitetsdrevet, Noa = tidsdrevet. Skal glemmetermen virke på `weightStored` mens Noa fortsatt bare multipliseres ved lesing? Vis et tilfelle der en kant som ikke lenger korrelerer svekkes av glemmetermen selv om den nylig var forsterket (R≈1), og et tilfelle der begge virker samtidig — er det dobbel glemsel, og er det ønsket?
- **S5 Forklarbarhet.** I dag forklares en skåre ved kantbidrag. Med konkurranse blir «hvorfor sank denne kanten» avhengig av andre kanter i samme formål. Foreslå explain-felt (f.eks. konkurranseledd per oppdatering, eller formålets vektnorm) som gjør det synlig uten å lekke mer data enn i dag.
- **S6 Skåringsnormalisering (HD-0051).** Er `clamp01(raw)` fortsatt riktig med v2? Hvis ‖w‖ → 1 per formål, hva blir raw-skårens verdiområde, og trengs normalisering i det hele tatt? Foreslå en normalisering som bevarer rekkefølge (ikke metning), og gi HD-0051 sin avgjørelse: fiks (hvilken) eller avvis (hvorfor).
- **S7 Versjonering og migrasjon.** Hvor bor η_forget og eventuell sentreringstilstand — `RelationalLearningConfig` eller egen policy? Additivt API, `effectiveFromTimestamp`-cutover, bakoverkompatibel replay av gammel logg. Tester avledes av målene i dette dokumentet, ikke av implementasjonen.
- **S8 Spørsmål til Vegar.** Maks fem presise spørsmål rapporten ikke kunne avgjøre selv (f.eks. valg av y: lineær vs clamp; sentrering i praksis; η-skjema Σ η = ∞, Σ η² < ∞ i diskret episodetid; om glemmetermen også skal virke ved feilutfall). Disse sendes av Losen/Kjetil, ikke av denne tråden.

## 6. Avgrensninger

- Ingen endring i CellProtocol-kode i denne oppgaven. Simulering skjer i egen kode under `simulering/` i denne mappen (Python eller Swift-skript) — ikke i `Sources/`. Implementering krever formålsdrevet utvikling med formålstre godkjent av Kjetil (G1) — se skill `haven-purpose-driven-dev`.
- Ingen git-mutasjon fra Cowork-VM-mount; commits gjøres av Codex eller Kjetil på Mac.
- Lokal-først: ikke bruk ekte brukerlogger utenfor maskinen. Syntetiske logger er standard; ekte journal bare om Kjetil peker på én.
- Ingen sentral profilering, ingen black-box-modell uten edge-nivå explainability, ingenting som bryter event-sourcing (avgrensningene i deepresearch-prompten gjelder).
- Ikke send noe til Vegar fra denne tråden. Spørsmål til ham leveres i rapporten.

## 7. Leveranse

- `RAPPORT.md` i denne mappen med seksjonene: Kildegrunnlag (primærkilder, minst Oja 1982 og GHA/Sanger), S1–S8, Målinger, Anbefaling INN/AVVIST, Spørsmål til Vegar, Hva som ikke virket.
- `simulering/` med reproduserbar kjøring (én kommando) og resultatfiler.
- HD-0050: målinger som `python3 tools/hd.py event emit --task HD-0050 --kind note --phase PREPARING --status OK --message '<målt resultat>' --evidence <sti>` (gyldige kinds står i `HAVEN-Deploy/tools/hdlib/core.py`, `KINDS`; `research.*` finnes ikke — Losen prøvde). HD-0051: avgjørelse fra S6. Merk HD-0045: tilstandsmaskinen har ennå ingen ferdig-tilstand for en oppgave som ikke er en deploy, så «ferdig» meldes som note + i loggen inntil den er løst.
- Loggfør i `Losen/logg/Losen_Hendelseslogg.md` under dagens overskrift — bruk den loggen, ikke lag en ny. Alt som ikke virket: `hd lesson new`.

## 8. Slik starter du

1. Les denne filen, `Vegar_svar_2026-09-09.md`, Docs §5–7, engine-linjene nevnt i §3, og deepresearch-prompten.
2. Verifiser F3 med en test (eller et eksplisitt regnestykke kjørt i kode) før du bygger videre på det.
3. Bygg simuleringen på engine-semantikken (samme defaultverdier, samme episode- og eligibility-regler), ikke på en forenkling. Dokumenter hvert avvik.
4. Skriv rapporten underveis, ikke til slutt; det som ikke virket, skrives ned i samme økt.

## 9. Åpne spørsmål til Kjetil (avgjøres før eller under tråden)

- Skal tråden bruke Codex (`codex exec` på Mac) for Swift-simulering mot selve motoren, eller holde seg til Python med reimplementert regel?
- Finnes det en ekte, lokal journal (`RelationalLearningPersistedJournal`) som kan replayes, eller er syntetiske logger nok for avgjørelsen?
- Skal vi be Vegar om det formelle notatet nå, eller etter rapporten (slik svaret 11.9 lovet)?

## 10. Kilder lest i denne økten

- `CellProtocol/Docs/RelationalLearning_Architecture_NO.md` (hele)
- `CellProtocol/Sources/CellBase/PurposeAndInterest/RelationalLearningEngine.swift` (linje 239–300, 429–505, 629–645, funksjonsliste)
- `CellProtocol/Sources/CellBase/PurposeAndInterest/RelationalLearningModels.swift` (linje 459–475, 518–520)
- `CellProtocol/Sources/CellBase/PurposeAndInterest/RelationalDecayPolicy.swift` (typer og `retention`)
- `CellProtocol/commons/prompts/relational_learning_deepresearch_prompt.md` (hele), `relational_learning_code_assistant_prompt.md` (linje 1–40)
- `CellProtocol/Tests/CellBaseTests/RelationalLearningEngineTests.swift` (testnavn)
- HAVEN correspondence, kanal `kjetil-vegar-codex-d`, sequence 2 og 3
