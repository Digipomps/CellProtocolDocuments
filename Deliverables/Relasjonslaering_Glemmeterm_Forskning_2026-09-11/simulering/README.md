# Lokal reproduksjon

Fra leveransemappen: `python3 simulering/run.py`.
På en annen maskin: oppgi `--cellprotocol /absolutt/CellProtocol` og eventuelt `--out /absolutt/resultater`.

Forutsetninger: Python 3.13.2 og Swift 6.2.4/Xcode ble brukt. Standardbibliotek, Foundation og CryptoKit; ingen tredjepartsinstallasjon. Referansefilene i CellProtocol må ha nøyaktig de bevarte hashene. Numerisk bitlikhet på andre plattformer/versjoner er ikke lovet.

Kommandoen kjører 144 kildelogger mot åtte kandidater, 8 forskningskontrakttester, de originale 7 Swift-motortestene og 20 differensial-/migrasjonsfixtures. Bygging skjer i en midlertidig mappe; CellProtocol-checkouten leses, men endres ikke. Resultater skrives bare til valgt resultatmappe. Ingen nettverk eller eksterne API-er brukes.

`oracle/Support.swift` erstatter kun nødvendige Object/ValueType/FlowElement/FlowHasher-avhengigheter med plain-JSON/CryptoKit-støtte. Det er ingen full pakke- eller CellApple-integrasjonstest. Se rapportens avviksavsnitt.

`study.py` følger gjeldende standardverdier og gyldige syntetiske source-events. Produksjonens genererte-event-ID-deduplisering for mixed source+weight-logger, full metadata-serialisering og journalstørrelsesavvisning er ikke portert. `edge_event_replay_equal` er bare rekonstruksjon av kantprojeksjonen fra forskningsposter. De tre mixed/config-fixturene kjøres derfor i faktisk Swift.

Deterministiske tallfiler ligger i `resultater/manifest.json`. Testlogger har veggklokketid og inngår ikke i de sju numeriske reproduksjonsfilene. En separat kjøring med `PYTHONHASHSEED=7841` ga identiske sju filer; kvittering i `../underlag/REPRODUKSJON.json`.

Ekstra skjema-verifikasjon: `SchemaCheck.swift` dekodet de 3 GoalDefinition- og 8 ClaimDefinition-verdiene mot aktuelle Swift wire-typer, separat fra modellkjøringen. Det er en dataformatkontroll, ikke en full kompilering av runtime-prosjektet.
