# Kontraktskisse v0 — ikke implementert eller maskinvalidert

Dette er planens operasjonsliste. WP1 leverer JSON Schema, positive/negative fixtures, versjonerte returskjema og en validator før klient/handlerimplementasjon.

| Celle | Metode/keypath | Input | Output |
|---|---|---|---|
| Dataset | set dataset.load | intakeId, metadata-ID, requestId | datasetId, inputSha256, validation |
| Dataset | get datasets.<id>.metadata | UUID i keypath | kilde, enheter, n, hashes |
| Analysis | set fit.start | requestId, runId, datasetId, methodId, parameters | jobId, status |
| Analysis | get jobs.<id>.state | UUID i keypath | status, stage, artifactIds, error |
| Figure | set figure.render | requestId, runId, datasetId, analysisArtifactId | jobId, status |
| Figure | get jobs.<id>.state | UUID i keypath | status, artifactIds, error |
| Experiment | set run.start | requestId, intakeId, metadataId, methodId, parameters | runId, status |
| Experiment | set run.cancel | runId | status; terminal cancelled først etter at worker er høstet |
| Experiment | get runs.<id>.state | UUID i keypath | status, stage, lastSequence, artifactIds, error |
| Experiment | get runs.<id>.events | UUID i keypath | alle stadiehendelser, begrenset til maks 64 per v1-run |
| Experiment | get runs.<id>.result | UUID i keypath | manifest/artefaktmetadata; tydelig NOT_READY før completed |
| Alle | keys/type_for_key/description | eksisterende Explore-flate | kun statiske, sideeffektfrie beskrivelser |

Kall krever lokal eieridentitet med kontrollbevis; en UUID-string gir ingen tilgang. Default GeneralCell fallback på ukjent keypath må ikke slippe gjennom. UUID-er parsevalideres, og eventuelle suffikser avvises. Feilmetode og ukjente inputfelt avvises. Gjennomslipp av vilkårlige stier, eval, shell og pickle er ikke kontrakt.

Metodebeskrivelse skal inkludere inndata, enheter, parametergrenser, forventet output, forutsetninger og metodeversjon. Ingen ny wire-type er nødvendig: manifest, metadata og hendelser bruker eksisterende objektverdier. NumPy-skalare konverteres til vanlige endelige Python-tall; NaN/Inf kan ikke serialiseres som faglig resultat.

Progresjon bruker eksisterende FlowElement med applikasjonsfelt runId/jobId, sequence, status, stage, artifactIds og error. Endelig schema presiserer feltenes required/null-regler. Positive og negative fixtures skal blant annet dekke feil eier, ukjent keypath, ugyldig datasett, duplisert requestId, konflikt, cancelled og write-failure.

Deljobbenes runId må finnes og tilhøre samme autoriserte eier/kjøringskontekst som inndataartefaktene. Supervisoren lagrer runId→jobId før oppstart, og avbrytelse treffer bare jobber i den aktuelle kjøringen. Cross-run/cross-owner referanser får egne negative fixtures.
