# Evidens, avgrensning og adjudikasjon

Dato: 2026-10-02. Repo-relative kildeankere nedenfor er fra HAVEN-roten. Linjer er øyeblikksbilder og kan flyttes. `source-manifest.json` fryser hashes for et utvalg av de bærende kildefilene, ikke hele repos eller bygg.

## Kildeidentitet og metode

| Arbeidskopi | HEAD ved audit | Begrensning |
|---|---|---|
| CellScaffold | 942965ca24e9a418b531f9514c1da75d6d529e30 | Stor dirty arbeidskopi; EventCells og deler av test-/workbencharbeidet utrackede ved flytting. HEAD alene er utilstrekkelig |
| CellProtocol | 253b4afe11af8b58bfcc433d9b7dc7393c761e24 | Dirty Skeleton og andre endringer; undersøk faktisk filhash |
| Binding | 775fc93db71397022733e8225827d92a9423c803 | Endret ContentView og utrackede nearby-filer/tester |
| CellProtocolDocuments | c8029847502fe007833d1ebd371bcb5adc01c3ae | Andre dokumentendringer finnes; denne leveransen committer dem ikke |

Tre rådgivere undersøkte kildeområdene konferanse/Swarm, Binding/møte og gruppe-Entity. De leverte brief-audit, bevis og motargumenter. Hovedagenten sammenholdt dette med offentlige primærkilder og utfordret en annen adjudikator på den mest forsiktige anbefalingen. Dette var samarbeidsagenter med kildeinnsyn, **ikke en test av en kjørende DiMy-rådgivertjeneste**.

Ingen runtimebygg, Swift-tester, virkelig radio, mikrofon, produksjonsbesøk, deploy eller faktisk Swarm-domene-kjøring inngår. Nettlesertesten gjelder bare den nye interaktive skissen. Tidligere testresultater er eksplisitt historiske.

## Bærende interne kilder

| ID | Kildeanker | Hva det støtter / begrenser |
|---|---|---|
| S1 | `CellScaffold/Sources/EventCells/EventPlatform/EventPublisherRegistryCell.swift:246`, `:430`, `:648`; `EventPlatformModels.swift:19`, `:73`; `EventPublisherAccessSupport.swift:43` | Reell publisher-onboarding, medlems-/publiserings-ACL og snapshots; ikke portabel representasjonsfullmakt |
| S2 | `CellScaffold/Sources/EventCells/EventPlatform/EventFederationBrokerCell.swift:108`; registry `:721` | Søk i lokale publiserte dokumenter, ikke demonstrert remote federation |
| S3 | `CellScaffold/Sources/App/Cells/ConferenceMVP/Cells/ConferenceRecommendationCell.swift:943`; `ConferenceSchedulingCell.swift:162` | Faste anbefalingskandidater og separat tilgjengelighet; ikke levende felles aktørmatching |
| S4 | `Binding/Binding/ContentView.swift:8529`; `NearbyScannerSurfaceView.swift:29`, `:55`; `Binding/Documentation/NearbyConversationConsentAndTrust_2026-09-11.md:3` | Native scannersubstitusjon, requester-/nil-resultatfallgruver og eksplisitt ikke implementert felles opptaksforslag |
| S5 | `Binding/Implementation/SurfaceParityRepair-20260930/STATUS.md:26`; `REPORT.md:15` | Historisk paritetskandidat i separate workspaces. Binding b18e267d6e103c2bcb2ebda9f91215fc435861f2, CP 41139185b00e2abb7b6c28c212fc64140e60d083, CS bdc9f8302691d8af7ee16e7f0fa659dddf500fac er ikke ancestors til de vanlige checkoutenes HEAD; ikke installed-build-bevis |
| S6 | `Binding/Binding/BindingVoiceInputTranscriber.swift:68`; `CellScaffold/Sources/App/Cells/Transcript/TranscriptStoreCell.swift:59`, `:366`, `:446` | Taleinput og transkriptlager finnes. Expiry er ikke automatisk sletting; release til caller er ikke fjern leveringskvittering |
| S7 | `CellProtocol/Sources/CellBase/PersistingCells/EntityRelationRecordV1.swift:19`; `GeneralCell.swift:1912`; `CellScaffold/Sources/EventCells/ConferenceMVP/Models/ConferenceDomainModels.swift:102` | Generiske relasjoner/medlemskap og enkel Organization-type; ikke ferdig generell selskapsgovernance |
| S8 | `CellScaffold/Sources/App/Cells/EntityScaffoldEnrollment/EntityScaffoldEnrollmentCell.swift:642`; `CellProtocol/Sources/CellVapor/Cells/EntityAnchorCell.swift:364`; `CellScaffold/Sources/ScaffoldKit/DistributedEntityData/EntityOperationReplicaV0.swift:92` | Signert innmelding, owner-proof og lokal persistens; referanse-replika i minnet er ikke produksjonsklar multi-master |
| S9 | `CellScaffold/Sources/UserSimulationScaffoldCore/SimulationRoutes.swift:44`; `SwarmToolCells.swift:44`; `SimulationModels.swift:49`, `:463`; `VirtualUser.swift:277` | Run-API og generiske scriptatferder; catalogdescriptors ikke en ferdig UI, seed ikke alene identitetsreplay |
| S10 | `CellScaffold/Sources/App/Cells/ConferenceMVP/Cells/ConferenceAdminShellCell.swift:783`; `ConferenceSimulationPopulationCell.swift:248`; `ConferenceSimulationPlaybackCell.swift:134`; `CellScaffold/Deliverables/PDD_swarm-workbench_2026-09-29/STATUS.md:6` | Egen konferansesimulering/admin; reset ikke full opprydding. Workbench-design godkjent, øvrige porter åpne |
| S11 | `CellProtocol/Sources/CellBase/Cells/Purpose/GoalEvaluationCell.swift:6`; `PurposeAndInterest/ClaimComposition.swift:189`; `CellScaffold/Sources/App/Cells/PersonalCopilot/ExecutablePurposeGroundingCell.swift` | Reelle formåls-/mål-/påstandsbyggesteiner. Ingen påvist full panelorkestrering for OIW |
| S12 | `CellProtocolDocuments/Deliverables/PDD_conference-release-repair_2026-09-29/STATUS.md` | Tidligere reparasjonsspor/PR276 og tester; notatet dokumenterer ikke en fullført release |

Rådgivervedleggene inneholder flere og mer presise ankre. Hvis kildeflytting har endret et anker, bruk manifest og filnavnsøk fremfor å anta at funksjonen mangler.

## Eksterne primærkilder

Alle lest 2026-10-02. Ingen private deltaker-/selskapsopplysninger ble hentet.

- [OIW FAQ](https://www.oiw.no/faq): paraply, 19.–22. oktober 2026, hoved-/sideprogram, arrangøransvar, separat påmelding og publisert frist 13. september. Dette er fakta om OIW, ikke tillatelse til vår integrasjon.
- [OIW](https://www.oiw.no/): offentlig arrangementsramme. Mockupens arrangementer, personer og selskaper er fiktive, ikke kopiert fra programmet.
- [Datatilsynet: lydopptak](https://www.datatilsynet.no/personvern-pa-ulike-omrader/overvaking-og-sporing/lydopptak/?print=true): lydopptak innebærer behandling av personopplysninger; begrunner at opptak/lagring/bruk trenger konkret vurdering før reell pilot.
- [Datatilsynet: samtykke](https://www.datatilsynet.no/rettigheter-og-plikter/virksomhetenes-plikter/om-behandlingsgrunnlag/samtykke/): støtte for frivillighet og avgrensede valg. Produktets gjensidige godkjenning er ikke et generelt juridisk utsagn om alle opptakssituasjoner.
- [Brønnøysundregistrenes API-dokumentasjon](https://data.brreg.no/enhetsregisteret/api/dokumentasjon/no/index.html): enhets- og rolleoppslag som mulig kilde for virksomhetsbekreftelse. Slutningen om at requester-fullmakt må bevises separat er vår arkitekturvurdering.

## Adjudikasjon og korrigert vurdering

Den sterkeste utfordringen var: «Hvorfor utsette gruppefunksjoner når eksisterende GroupProtocol, publisher-ACL, medlemskap og owner-proof allerede gjør mye?» Andre adjudikator etterprøvde fem kilde-/testfiler og korrigerte første rapport:

1. **Lokal fleradministratorstøtte og siste-admin-vern finnes.** S1 og `Tests/EventCellsTests/EventPublisherRegistryCellTests.swift:204` støtter gjenbruk av publish-only-rollen og medlemsadministrasjon. Første rapport var for grov hvis den ble lest som at dette manglet helt. Den delen av begrunnelsen er forkastet; plan WP1/WP6 bruker eksisterende ACL.
2. **To verter er krav for integrasjonsbevis, ikke for all lokal brukerprøving.** S8 og S2 avgrenser hva én runtime beviser. Planen skiller lokal kunnskapsprøve fra AC5, og beholder AC5 som fullføringskrav.

Vurderingen om manglende portabel selskapsrepresentasjon, full opptaksreise og verifisert universell federation står. Den er ikke et argument for å bygge alt på nytt. Se `advisers/second-adjudication.md` for eksplisitt dom og første rapport for hvilke formuleringer som ble presisert.

Påstandsgrafen i `analysis-contracts.json` har 11 røtter. Tre er åpne med eier: all-scaffold-readiness, bedre verdi fra fellesførst og kjørende DiMy-tjeneste. Øvrige er lukket med avgrenset støtte eller motsagt av de leste kildene. Fellesførst er en produktføring; at det gir bedre effekt enn en enkel kuratert kildeoversikt er en separat, uprøvd hypotese.

## Kvalitetsdiagnostikk

Disse målingene gjelder analysen, ikke løsningens kvalitet eller en sannsynlighetsscore.

| Metrikk | Observasjon og grunnlag |
|---|---|
| Q1 sporbar endring | 2/2 endringer ovenfor har eksplisitt begrunnelse og kilde; én er nytt direkte kildebevis, én er korrigert avgrensning av hva beviset krever |
| Q2 mot bestillingsretningen | Ingen entydig «ønsket dom» er lagt til grunn: bestillingen ber om kartlegging/design. Ingen ratio konstrueres. Funnene både støtter gjenbruk og avviser ferdig-påstander |
| Q3 ærlige auditstatuser | 9 faktuelle/kapabilitetsrøtter har navngitte hentede kilder; 2 røtter gjelder brukerens normative føring/hypotese. Hentet kode brukes ikke som ferskt driftsbevis |
| Q4 uavhengighet av fortelling | De 9 kildebaserte kapabilitets-/faktarøttene står også om man velger personlig nytte som første skjerm. C1 er brukerføring; C10 er åpen verdihypotese |
| Q5 falsifiserbarhet | Ingen uflagget «uansett resultat bekrefter hypotesen»-struktur identifisert. AC1–AC10 kan feile; negativ baseline-sammenligning svekker C10 |
| Q6 naturlig eksperiment | 0 reelle piloter eller sammenligninger undersøkt. Historiske renderer-/unitresultater er ikke sosialt effektbevis; ingen sannsynlighet er satt |
| Q7 motiv mot atferd | Ikke relevant: ingen motivpåstander om faktiske deltakere eller selskaper. Syntetiske roller er testoppsett |
| Q8 terminal håndtering | 11/11 røtter er støttet/motsagt eller åpne med grunn og eier; åpne produktbevis er ikke kalt ferdige |
| Q9 kildebasert steelman | 1 hovedmotargument etterprøvd direkte i publisher-ACL og tillatelsestester; utfallet korrigerte vår for forsiktige formulering |
| Q10 konsesjon uten bevis | 0 substansielle konsesjoner uten ny kilde eller eksplisitt avgrensningsbegrunnelse; korrigeringen er ikke en avstemning |

Tellingene er manuelle diagnoser av disse 11 røttene, ikke uttømmende måling av alle setninger eller uavhengige ekspertstemmer.
