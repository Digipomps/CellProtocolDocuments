Brief audit
===========

Andre adjudikator, OIW 2026-10-02. Leste de to andre rapportene og etterprøvde publisher-ACL i fem kilde-/testfiler. Ingen produktendringer, tester, bygg eller tjenestekall. Bare denne rapporten er skrevet. Alle kildehenvisninger er relative til HAVEN-roten `<HAVEN_ROOT>`.

1. Første anbefaling blander **lokal fleradministratorstøtte** med **full selskapsgovernance**. Dette må korrigeres før anbefalingen brukes: publisher-runtime har allerede flere medlemsoppføringer, eksplisitte rettigheter og vern av siste medlemsadministrator.
2. «Første pilot trenger to vertsinstanser» må knyttes til hva piloten skal bevise. En lokal kunnskaps-/UX-test kan kjøres tidligere. Brukerens ønskede kommunikasjon mellom scaffolds er først demonstrert med minst to selvstendige kjørende instanser og reell transport; én resolver med to identiteter er utilstrekkelig. To fysiske maskiner er ikke automatisk nødvendig for den første transporttesten. Binding/radio krever egen fysisk enhetstest når det inngår.
3. «Eksplisitt publiseringsmandat» må ikke bli et krav om en ny godkjenningsdialog for hvert vanlig event-edit. Eksisterende publisher-ACL er et konkret mandat innenfor sitt nåværende ressursomfang. Den gir ikke automatisk mandat til å publisere ansattes private data, felles møtetranskript eller en OIW-tilknytning.
4. Rådgiverrapportene er kildekontroller, ikke ferske testresultater. CellScaffold-base er `942965ca24e9a418b531f9514c1da75d6d529e30`; EventPlatformModels, EventPublisherAccessSupport, EventPublisherRegistryCell og registertesten er utrackede i et omfattende dirty checkout. Referansen alene gjenskaper ikke den undersøkte koden.

## Avgjørelse: behold retningen, korriger begrunnelsen og milepælene

Anbefalingen om en liten frivillig kunnskapsallmenning er en rimelig **første leveransehypotese**, men er ikke empirisk bevist best. Den må ikke erstatte brukerens eksplisitte mål om kommunikasjon mellom scaffolds. Planlegg lokal produktverdi og den smale integrasjonsbevisføringen som to synlige milepæler i samme arbeid.

Motargumentet vinner på to punkter: Vi bør **gjenbruke lokal fleradministrator-/publisher-ACL allerede i piloten**, og **ikke bygge en ny generell mandatmotor der dagens autorisasjon dekker handlingen**. Motargumentet taper der det vil slutte fra disse lokale rettighetene til ferdig selskapsidentitet, portabel delegering, sikker recovery, delt møtesamtykke eller faktisk federation.

| Omstridt punkt | Kildebasert avgjørelse |
|---|---|
| «Fleradministrator kan utsettes» | For grovt. `CellScaffold/Sources/EventCells/EventPlatform/EventPublisherRegistryCell.swift:430–469` legger til/oppdaterer flere medlemmer; 461–462 krever at minst én beholder `manageMembers`. `EventPlatformModels.swift:19–50` gir admin alle rettigheter. Dette er implementert lokal administrasjon som bør brukes, ikke bygges på nytt. Quorum, tapte nøkler, eierskifte og recovery er fortsatt egne ubekreftede kontrakter. |
| «Roller er bare etiketter» | Feil for publisher-runtime. `EventPlatformModels.swift:73–88` lagrer eksplisitte permissions og avleder rollen. `EventPublisherAccessSupport.swift:54–62,65–99` matcher medlem og nødvendig permission. `Tests/EventCellsTests/EventPublisherRegistryCellTests.swift:204–246` uttrykker publishEvent uten editEvent og forventer nektet redigering. Testen er lest, ikke kjørt. GeneralCell/GroupProtocol er en annen, mer generell medlemsmekanisme. |
| «Owner-proof løser selskapsrepresentasjon» | Ikke etablert. `CellScaffold/Sources/App/Controllers/VaporEventPlatform.swift:292–307` sjekker aktiv vault, signing key og domenebinding. Det beviser requester-binding i denne innloggede veien. Registeret oppretter selv en publisher med requester som admin (`EventPublisherRegistryCell.swift:246–279`); det beviser ikke at en navngitt virksomhet har godkjent vedkommende som representant. |
| «Nytt publiseringsmandat kreves for alt» | Avvises. Eventpublisering sjekker `.publishEvent`, validerer og lager en publisert snapshot (`EventPublisherRegistryCell.swift:648–681`). Gjenbruk dette for egne publiserbare eventdata. Utvid bare for nytt materiale/ny myndighet: deltakerbidrag, felles møter, tredjepartsdata eller paraplytilknytning. |
| «Lokal federation er tilstrekkelig» | Avvises som bevis for kommunikasjon mellom scaffolds. `EventPublisherRegistryCell.swift:721–735` bygger søkedokumenter fra lokale snapshots; `EventFederationBrokerCell.swift:108–125` filtrerer dette registeret. Komponenten er nyttig, men navnet utvider ikke implementasjonen. |
| «Eksisterende Swarm kan validere piloten direkte» | Delvis. Den andre kildekontrollen viser reell coordinator/worker/transport/runtime og administrativt API, men generiske handlinger, ikke konferansens semantiske brukerreiser. Gjenbruk infrastrukturen; legg til smale domenehandlinger og forventet/faktisk-resultatkontroll. Sockets og metrics beviser ikke publiseringsmyndighet eller kunnskapsverdi. |

## Sterkeste motargument, vurdert på sitt beste

«Det er unødvendig å vente på en full selskapsstandard. Vi har uavhengige publishers, identitetsbinding, egne medlemsrettigheter, begrenset publisher-tilgang, snapshots, EntityAnchor og scaffold-innmelding. En gruppe kan samarbeide og publisere gjennom eksisterende mekanismer. En liten eksplisitt kobling mellom dette og kunnskapsartefakter kan være tilstrekkelig.»

**Jeg er enig innenfor en avgrenset, ærlig produktkontrakt.** Kall det et delt publisher-/organisasjonsarbeidsrom med navngitte rettighetshavere. La flere administratorer bruke eksisterende ACL. Opplys om selvdeklarert eller verifisert tilknytning separat. Ikke krev full legal/verifisert selskapsidentitet for uformelle grupper.

Begrensningen er konkret: medlemsoppslaget sammenlikner normalisert requester-UUID (`EventPublisherAccessSupport.swift:43–62`) og selve assignment-formatet har UUID, permissions, hvem som la til og tid (`EventPlatformModels.swift:73–85`). Det er ikke i seg selv et signert, utløpende, portabelt delegasjonsbevis bundet til et selskaps kontrollmyndighet. Den lokale controllerens gode identitetskontroller må ikke antas å følge med over en ny remote ingress. Test den faktiske requester/proof-pathen før samme ACL brukes fra en annen scaffold. Dette er en integrasjonsgrense, ikke en påvist utnyttelse.

## Korrigert første leveranse

1. Gjenbruk event-register, publiserte snapshots og den eksisterende permission-baserte medlemsadministrasjonen. En liten kunnskapsartefaktmodell legger til kilde, forfatter/representasjonsrolle, versjon, publikum, rettighetshjemmel, rettelse og dissens. Private notater og personlig enrichment er tilgjengelige uten plikt til å bidra.
2. For organiserens egne eventdata: eksisterende publisher-rettigheter. For deltakerbidrag/felles møtedata: eksakt innholds-/versjons- og mottakerfullmakt før publisering. Ingen generell utvidelse fra `publishEvent` til andre menneskers data.
3. Første lokale prøve demonstrerer innhold, korrekt autorisasjon og nyttig kunnskapsgjenfinning. Den rapporteres som lokal. Parallelt eller neste smale milepæl demonstrerer to selvstendige scaffold-instaser med separate tilstands-/autoritetsgrenser: kjent requester → eksplisitt grant → faktisk transport → varig kvittering → read-back → tilbakekalling/nektet tilgang. Først da er den delen av brukerens opprinnelige mål oppfylt.
4. Full kontrollskifte-/quorum-/recovery-governance kan utsettes dersom piloten ikke lover det eller håndterer irreversibel selskapskontroll. Eksisterende flere administratorer og siste-administratorvern bør ikke utsettes eller erstattes. Tap av tilgang må ha en kjent, ærlig operativ håndtering før reelle organisasjoner er avhengige av piloten.
5. Delte opptak/transkripter holdes som egen akseptansereise. Binding-rapportens lokale taleinput, nearby-invitasjon og TranscriptStore er gjenbrukbare deler; de er ikke samlet deltakergodkjenning eller publiseringsgodkjenning. Ingen opptaksmodul er nødvendig for å teste den første kunnskapsallmenningen med manuelt godkjente artefakter.

## Åpne beslutninger og evidens

- **Produktansvarlig/Kjetil:** Er første leveranse et publisher-arbeidsrom for kjente inviterte deltakere, eller skal den allerede hevde formell selskapsrepresentasjon? Det siste krever en tydelig myndighetskilde og kontrollmodell.
- **Arkitektur/integrasjon:** Velg konkret kilde- og mottakerscaffold, requester-domener, eksisterende grant-path og persistent namespace. Bestem om piloten demonstrerer remote lesing, bidragsinnsending eller remote skriving; én veldefinert reise er tilstrekkelig som første bevis.
- **Kunnskapsprodukt:** Definer hvilken forbedring som skal måles mot en enkel kuratert samling. Flere lagrede poster er ingen verdiindikator alene. Bruk kildeforankrede svar, nyttige rettelser og frivillig deltakervurdering; ikke personscore eller aktivitetsrangering.
- **Governance:** Undersøk faktisk medlemsfjerning/utløp, restart og fullmaktsendring under en pågående operasjon. `setMemberAccess` krever en ikke-tom permission-liste (436–438); kildeutdraget beviser nedgradering, ikke fullstendig revokering av alle rettigheter. Ikke lov den siste egenskapen uten riktig path/test.
- **Leveranse:** Alle ferske godkjente/avviste scenarier er åpne fordi ingen test ble kjørt. Lås fungerende kilde-/konfigurasjonsversjon før readiness-påstander.

## Korrigering av første rådgiverrapport

Behold første rapports skille mellom person, bedrift, medlemskap og representasjonsfullmakt. **Presiser utsagnene om manglende fleradministratorstøtte og siste-administratorvern:** de mangler som demonstrert generell selskapsgovernance, men finnes i den lokale publisher-modellen som denne andre runden nå har lest. Korrigeringen skyldes nye kildeankere ovenfor, ikke enighetspress. Generell federation og selskapsrepresentasjon er fortsatt åpne. Samlet anbefaling: **gjenbruk mer konkret, hevde mindre enn det som ikke er vist, og gjør to-instans-beviset til et synlig fullføringskrav for brukerens integrasjonsmål.**
