# Språkmodeller og samtykke

Status: batch 1 · godkjent av Kjetil 2026-10-16 · kildegrunnlag: snapshot 2026-10-07, ankre kontrollert ordrett 2026-10-15 · godkjenner: Kjetil (per batch)

## Er Kallimachos et menneske?

**[kan sies] HF-04-01.** Nei. Kallimachos er en KI-figur, bibliotekaren i HAVEN.

Kilder:
- `CellScaffold/Sources/App/Cells/AI/KallimachosAdvisorCell.swift` linje 972: «"kindLabel": .string("KI-figur")»

## Sendes spørsmålet mitt til en ekstern språkmodell?

**[kan sies] HF-04-02.** Ja, i dag som standard. Når rådgiveren Kallimachos svarer, brukes en kapabel ekstern modell (OpenAI eller Anthropic) med mindre noen aktivt har valgt noe annet. Spørsmålet og de utvalgte offentlige utdragene forlater da maskinen. At ekstern behandling skjer, opplyses i svaret.

*Begrensning:* Gjelder koden per 2026-10-07. Rådgiverne anbefaler å gjøre svar uten modell til standard (beslutning B1), men det er ikke bygget.

Kilder:
- `CellScaffold/Sources/App/Cells/AI/KallimachosAdvisorCell.swift` linje 296: «var modelTier = KallimachosModelTier.capable.rawValue»
- `CellScaffold/Sources/App/Cells/AI/KallimachosAdvisorCell.swift` linje 114: «the question and the selected public excerpts leave this machine»
- `CellScaffold/Tests/AppTests/KallimachosAdvisorCellTests.swift` linje 251: «testCapableRoutePlanUsesApprovedRemoteEndpointAndDisclosesExternalProcessing»

## Blir jeg spurt om samtykke før noe sendes til modellen?

**[med forbehold] HF-04-03.** Nei, ikke i dag. Det opplyses at en ekstern modell brukes, men du blir ikke bedt om samtykke før spørsmålet sendes.

*Forbehold:* Fraværet av et samtykkesteg er rapportert av rådgiversvermen etter kodelesing (R6), ikke vist med en egen test. Samtykke før sending er foreslått i bølge 0.

Kilder:
- `RAPPORT_Kallimachos_raadgiversverm_2026-10-07.md` linje 15 (intern rådgiverrapport, ikke offentlig kilde): «og uten samtykke før sending (R6).»

## Hva får modellen se og gjøre?

**[kan sies] HF-04-04.** Modellen får bare formulere over det som har sluppet gjennom evidensporten, og porten slipper bare gjennom offentlig Book-materiale og den versjonerte personaressursen. Modellen kan ikke bruke verktøy.

Kilder:
- `CellScaffold/Sources/App/Cells/AI/KallimachosAdvisorCell.swift` linje 903: «Deterministisk bibliotekar og kapabilitetsindeks først; modellen formulerer bare over det som slapp gjennom evidensporten.»
- `CellScaffold/Sources/App/Cells/AI/KallimachosAdvisorCell.swift` linje 934: «"allowedSources": .string("Book/** og bundle://commons_librarian_persona.v1.json")»
- `CellScaffold/Sources/App/Cells/AI/KallimachosAdvisorCell.swift` linje 921: «"toolPolicy": .string("deny-all")»
- `CellScaffold/Tests/AppTests/KallimachosAdvisorCellTests.swift` linje 120: «testNonPublicLibrarianEvidenceBlocksTheProviderCall»

## Blir modellsvaret kontrollert mot kildene?

**[kan sies] HF-04-05.** Ikke ennå. Påstandene i modellsvaret kontrolleres ikke mot kildene som ble sendt, og hvis modellsvaret ikke kan leses som forventet, kan den rå modellteksten vises. Les derfor modellteksten som en formulering, og sjekk sitatene.

*Begrensning:* Retting er foreslått som bølge 0 (vis aldri rå modelltekst, valider påstander).

Kilder:
- `CellScaffold/Sources/App/Cells/AI/KallimachosAdvisorCell.swift` linje 894: «let summary = Self.nonEmptyString(adviceBody["summary"]) ?? persistedState.adviceRaw»
- `raadgivere/O2_konsistens.md` linje 131 (intern rådgiverrapport, ikke offentlig kilde): «'projectedClaims' sjekker ikke 'evidenceIds' mot E1…En»

## Er modellleverandørene godkjent for personopplysninger?

**[kan sies] HF-04-06.** Nei. Book sier uttrykkelig at ingen leverandør er godkjent for produksjon med personopplysninger.

Kilder:
- `Book/24_Model_Providers_Credentials_And_Selection.md` linje 9: «claim that any provider is production-approved for personal data.»

## Finnes det en lokal modell?

**[med forbehold] HF-04-07.** Det finnes en lokal modellrute i koden (Qwen3-8B på samme maskin), men den er ikke standard, og du kan ikke velge den selv i dag.

*Forbehold:* Lokal rute er satt per celle av den som drifter tjenesten, ikke av sluttbrukeren.

Kilder:
- `CellScaffold/Sources/App/Cells/AI/KallimachosAdvisorCell.swift` linje 48: «static let localModel = "Qwen3-8B-Q4_K_M.gguf"»
- `raadgivere/O1_opponent.md` linje 30 (intern rådgiverrapport, ikke offentlig kilde): «Tieren settes per celle med 'advisor.setModelTier'.»

## Kan jeg velge språkmodell eller bruke min egen nøkkel?

**[ikke ennå] ARG-L5.** Ikke ennå. Som sluttbruker kan du i dag ikke velge modell eller koble til din egen nøkkel i Kallimachos. Modellkatalogen i Book er et utkast fra juni og inneholder ikke rutene Kallimachos faktisk bruker.

*Skal ikke sies:* «Du kan velge språkmodell.» · «Du kan bruke din egen API-nøkkel i Kallimachos.»

Kilder:
- `raadgivere/O1_opponent.md` linje 30 (intern rådgiverrapport, ikke offentlig kilde): «Påstanden er feil for sluttbrukeren i dag.»
- `Book/24_Model_Providers_Credentials_And_Selection.md` linje 3: «Status: draft operational contract.»
