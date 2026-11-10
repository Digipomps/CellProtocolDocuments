# Foreslått dataflyt — ikke implementert

Alle kanter er lokale, resolver-medierte cellekall. Referanser er applikasjonskontrakter, ikke nye protokolltyper.

| Fra → til | Handling/data | Fullføring |
|---|---|---|
| CLI → ExperimentCell | run.start: requestId, intakeId, metadataId, methodId, parameters | Kvittering med runId; Flow run.status |
| ExperimentCell → DatasetCell | dataset.load: intakeId + metadata | dataset-ID, SHA-256, validering |
| ExperimentCell → AnalysisCell | fit.start: requestId, runId, dataset-ID, metode/versjon | job-ID; Flow analysis.completed med artefakt-ID |
| ExperimentCell → FigureCell | figure.render: requestId, runId, dataset-ID + analyseartefakt | job-ID; Flow figure.completed med PNG/SVG-ID |
| ExperimentCell → ArtifactStore | Rapport, miljø, hendelseshistorikk og manifest | Atomisk publisert run-mappe; run.completed |
| CLI → ExperimentCell | runs.<id>.state og runs.<id>.events ved start/reconnect | Snapshot med siste sekvens og avgrenset historikk |

En intern fullførings-future kan brukes i supervisoren; den erstatter ikke Flow-flaten til klientene. Ingen timer re-leser jobbstatus.
