# Plan og akseptanse — konferanse med OIW som modell

Dato: 2026-10-02. Alle arbeidspakker nedenfor er forslag. Ingen av dem er markert implementert av denne analysen. Tidsestimat settes etter en låst, byggbar baseline; antall arbeidspakker er ikke et tidsestimat.

## Formål som kan prøves

| Bladformål | Foreslått observerbart mål | Tegn på at vi må endre retning |
|---|---|---|
| F1: Gjøre felles kunnskap mer nyttig | Deltaker finner kildeforankret svar, ser usikkerhet og kan rette en konkret feil; sammenlignes med samme kilder i en enkel kuratert samling | Flere poster og AI-sammendrag, men ingen bedre svar eller nyttige rettelser |
| F2: Gjøre relevante bidrag og møter mulige | En ny arrangør publiserer formål/tilbud/behov/tid; en relevant deltaker finner hvorfor det passer og foreslår et mulig møte | Faste demoaktører, tvungen publisering av kalender eller uforklarlige treff |
| F3: Bevare hver aktørs kontroll ved utvidelse av Entity | Valgt bidrag kommer til egen Entity på annet scaffold med riktig proveniens og kvittering; privat materiale forblir privat | En sentral konto må få alle data eller avsender bruker vertens eieridentitet |
| F4: Gjøre felles møteminne frivillig og etterprøvbart | Begge velger deltakelse/opptaksplan; etterpå godkjennes eksakt utdrag og publikum; avslag og stopp virker | Nearby, mikrofontillatelse eller ett samtykke brukes som godkjenning av hele kjeden |
| F5: Gjøre selskapsdeltakelse tydelig | Person kan handle som seg selv eller innenfor et konkret publisher-mandat; ingen privat Entity blir selskapets eiendom | Jobbtittel, organisasjonsnummer eller medlemskap gir alle fullmakter |
| F6: Prøve systemet før reelle deltakere | Swarm utfører domenehandlinger og sammenholder forventet/faktisk resultat med run-spor og isolerte testdata | Grønne socketmålinger omtales som bevis på samtykke, meningsfulle treff eller kunnskapsverdi |

Disse produktmålene er fremtidige akseptansekriterier. Analysens tre mål i `analysis-contracts.json` er et annet lag: kartlegging, vurderbart design og handlingsklar plan.

## Arbeidspakker

| Pakke / foreslått fagansvar | Leveranse og gjenbruk | Akseptanse | Avhengig av |
|---|---|---|---|
| WP0 / integrasjon og release | Lås kilde-/pakke-/konfigurasjonsrevisjoner. Avklar utrackede EventCells, eksisterende conference-release-repair og separat SurfaceParityRepair-kandidat. Lag støtteoversikt over kjørende scaffolds og deres ingress/auth/store | AC0: ny prosess og kald browser/native start; faktisk binær og vertsversjon kan spores. Eksisterende PR/status kontrolleres ferskt, ikke antatt deployet fra septembernotat | Ingen |
| WP1 / konferanseprodukt | Gjenbruk EventPlatform CRUD, snapshots og publisher-ACL. Legg til paraply, tilknytning som egen status, tilbud/behov/formål og tidsrom. Alle autentiserte aktører kan etablere egen arrangør innenfor publiseringspolicy | AC1: A oppretter/publiserer; B kan ikke endre A; utkastlekkasje avvises; tilknytning ikke «bekreftet» før riktig paraplymyndighet har godkjent; siste admin kan ikke fjernes ved vanlig rettighetsendring | WP0 |
| WP2 / kunnskapsprodukt | Frivillig kilde-/versjonsbundet bidrag med publikum, hjemmel, rettelse og dissens. Bruk vanlige publisher-rettigheter for arrangørens egne eventdata. Møtebidrag har egen eksakt godkjenning | AC2: spørsmål → kilde → påstand/motargument → rettelse; privat notat vises aldri i felles søk; avslag på deling hindrer ikke deltakelse; rettelse beholdes og publiseres med proveniens | WP1 |
| WP3 / matching | Erstatt faste kandidater med rettighetsfiltrert projeksjon av faktisk publiserte aktører/arrangementer. Tilgjengelighet, tidssone, overlapping, kapasitet og ønsket møtelengde | AC3: forklarbart treff og ekte nulltreff; endret tilgjengelighet/utløpt tilbud fjerner treff; to samtidige bekreftelser kan ikke dobbeltbooke samme reserverte kapasitet; rangering gir aldri leserett | WP1 |
| WP4 / DiMy og argumentanalyse | Koble eksisterende formåls-/mål-/påstandsmodeller til to oppgaver: dekomponer formål; prøv påstand mot kilder og motargumenter. Klargjør modellrute, kostnadsgrense og data som sendes | AC4: rådgiver finner en plantet usikker antakelse, viser kilde/ukjent og lar bruker godta/redigere/avvise; ingen foreslått interesse blir automatisk personlig fakta eller felles formål | WP2; WP3 for matchbruk |
| WP5 / Entity og transport | Én smal end-to-end-reise mellom to selvstendige runtime-instaser med egen autoritets- og lagringsgrense. Gjenbruk enrollment, owner-proof, EntityAnchor og eksisterende Bridge/Resolver | AC5: forespørsel med virkelig aktør → avgrenset grant → transport → varig lagring → read-back etter restart. Kryssdomene, utløpt grant, feil actor og tilbakekalling under venting avvises; tapt svar avstemmes uten duplikat | WP0, WP2 |
| WP6 / gruppe og selskap | Gjenbruk lokale publisher-medlemmer og rettigheter. Tydelig representasjonsvalg. Skill selvdeklarert organisasjon fra verifisert representasjon. Finn/bygg korrekt medlemsfjerning og kontrollert utløp der nødvendig | AC6: publish-only kan publisere tillatt event, men ikke redigere eller publisere private møtedata; inaktivt/tilbakekalt mandat kan ikke brukes; feil selskap/domene avvises; personens private noter består ved utmelding | WP1; WP5 for portabilitet |
| WP7 / Binding og renderer | Integrer eller avklar sept30-kandidaten uten å overskrive andres WIP. Samme originale konferansekonfigurasjon og identitetsskopede data på faktisk Binding-host og Porthole | AC7: status, feilmeldinger, valgt deltaker, review-versjon og faktiske knapper virker på kompakt/bred web og macOS, lys/mørk. iOS egen akseptanse hvis inkludert. Web viser capability-fravær; native radar testes separat | WP0; møtemodell fra WP8 |
| WP8 / møte og capture | Implementer portable møtetilstander og native adapter: deltakelse → eksakt opptaksplan → opptak/stopp → kontroll → godkjent utdrag → separate leveringer. Gjenbruk taleinput/TranscriptStore som deler | AC8: to godkjenninger og ferske rettigheter før effekt; ny deltaker/plan/processor/publikum ugyldiggjør relevante godkjenninger; alle kan stoppe; tap av kontakt pauser innen avtalt lease. To fysiske enheter og reell radio/transport kreves for nearby-løftet | WP2, WP5, WP7; synthetic adapter kan utvikles før fysiske tester |
| WP9 / Swarm og QA | Utvid eksisterende Swarm Workbench-plan med OIW-scenariobygger, adaptere og forventning/faktisk-resultat. Gjenbruk coordinator, workers, API og metrics | AC9: seed + fixtureversjon + identitetsmateriale/testklokke + binærrefs gir en etterprøvbar kjøring; scenariofeil synlig selv ved HTTP/socket-suksess; alle testdata isoleres og rester kontrolleres etterpå | WP0; domeneadaptere følger WP1–WP8 |
| WP10 / pilotansvarlig | Liten invitert pilot med kjente aktører, moderator og støtteansvarlig, først med manuelle bidrag. Mål forståelse og kontroll fremfor aktivitet | AC10: oppgavene under gjennomføres, feil registreres, avslag/privat bruk virker, oppfølging og slette-/rettingsønske har navngitt ansvar | AC0–AC6 og relevant AC9; AC7/AC8 bare hvis nearby/opptak er med |

WP2 kan prøves lokalt mens WP5 arbeides frem. WP5 forblir et nødvendig fullføringskrav for brukerens mål om kommunikasjon mellom scaffolds. En lokal resolver med to identiteter er ikke tilstrekkelig som det beviset.

## Liten menneskepilot

Foreslått oppsett: én paraply, to arrangementer, to arrangører, 6–8 inviterte deltakere og 1–2 selskaper. Dette er dimensjonering for læring, ikke avtalt rekruttering eller statistisk effekttest.

1. En arrangør oppretter et arrangement og beskriver formål, hva den tilbyr/trenger, tid og tilgjengelighet. En annen arrangørs tilgang prøves negativt.
2. Deltaker velger selv hva som kan finnes i matchingen, finner et relevant arrangement og forklarer tilbake hvorfor treffet ble foreslått. En deltaker uten treff skal få et ærlig tomt resultat.
3. To deltakere gjennomfører et møte. Første pilot kan bruke manuelt skrevet og godkjent møtenotat. De deler ett felles utdrag og beholder resten privat; én reise avslås uten tap av øvrig funksjon.
4. En tredje deltaker finner utdraget, følger kilden og utfordrer en påstand. Rettelse og dissens blir synlige uten å overskrive historikken.
5. En deltaker lagrer valgt innsikt i egen Entity på den andre verten. Restart/read-back og ett avbrutt/tilbakekalt forsøk prøves med syntetisk innhold først.
6. En selskapsrepresentant publiserer et tillatt selskapsbidrag, prøver en ikke-tillatt handling og viser at egne private notater ikke følger med.
7. Deltakerne sammenligner ett kunnskapssøk med en enkel kuratert kildeoversikt. Registrer hvilke spørsmål som ble løst, hvor kilder manglet, nyttige rettelser og frivillig vurdert verdi. Det lille utvalget kan ikke bevise generell effekt.

Før ekte opptak: konkret ansvarlig for behandlingen, informasjon til deltakere, behandlingsgrunnlag, data-/processorvei, lagringstid og rettighets-/slettehåndtering avklares. Gjensidig godkjenning er et produktkrav her, ikke en påstand om at samtykke er eneste lovlige grunnlag i enhver situasjon. Kilder: Datatilsynet i EVIDENCE.md.

## Swarm-scenario som gjenbruker eksisterende løsning

Foreslått domeneoppsett: 12 syntetiske personer, tre gruppeentiteter, fire arrangementer, én paraply og tre separate scaffold-instaser. Start med to verter for den minste brotesten. Roller: arrangør, bidragsyter, kritiker, deltaker som bare leser, person som avviser opptak, publisher med begrensede rettigheter og tredjepart uten tilgang. Ingen virkelige persondata.

Scenariovarianter:

- Normal: publiser → match → avtal → felles notat → godkjent deling → individuelt read-back.
- Avslag: avvis deling/opptak; resten av konferansen skal fortsatt kunne brukes.
- Endring: rediger utdrag eller publikum etter godkjenning; gammel godkjenning kan ikke gjenbrukes.
- Revokering: stopp mens en autorisert handling venter; ingen forbudt effekt etter frigivelse av testbarrieren.
- Frakobling: mottaker offline, tapt kvittering etter vellykket lagring, reconnect/replay; ingen falsk suksess eller duplikat.
- Isolasjon: feil requester, selskap, domene, gruppe og vert; ingen data-/rettighetslekkasje.
- Uenighet: to motstridende påstander og en feil AI-utledning; kilde, motargument og korrigering beholdes.

Nødvendige adaptere: scenario → domene-fixtures; testidentiteter til reelle requester/proof-paths; domenehandlinger; levende matchingprojeksjon; paraplymedlemskap; kontrollert klokke/evidens; isolasjon/opprydding. Den eksisterende seed alene gir ikke nøyaktig identitetsreplay fordi nøkler genereres på nytt; håndter dette eksplisitt i testmodus.

Operatørflaten skal vise kjøringskonfigurasjon og revisjoner, syntetiske aktører og roller, hvilken handling som feilet, forventet/faktisk resultat, kvitteringer og rester. Pause/fortsett/stopp gjenbruker dagens run-API. Ikke kall eksisterende conference-reset en global rollback. Bruk tomt, dedikert testnamespace og kontroller faktisk vedvarende innhold etter kjøringen.

## Åpne beslutninger og eiere

| Beslutning / bevis | Eier (rolle, ikke tildelt jobb) | Anbefalt foreløpig valg |
|---|---|---|
| OIW-referanse eller faktisk oktoberpilot/arrangøravtale | Kjetil / produktansvarlig | Referansemodell inntil eksplisitt avklart; ikke lov offisiell tilknytning |
| Første verts-/scaffold-par og operasjon | Arkitektur/integrasjon | Konferansevert og én eksisterende personlig Entity-vert; valgt kunnskapsbidrag med kvittering, ikke vilkårlig remote skriving |
| Selskapsnivå i pilot | Produkt og governance | Delt publisher-arbeidsrom med kjente rettighetshavere; verifisert selskapsrepresentasjon kun når autoritetskilden er avklart |
| Moderator, rapportering av misbruk og korreksjoner | Pilotansvarlig | Navngitt moderator; kilde-/rettighetskontroll, ikke popularitetsbasert sannhet |
| Opptaksrute og bevaring | Produkt / personvernansvarlig / Binding | Først ingen opptak. For separat opptakspilot: lokal behandling, kort avtalt bevaring, valg om lagring av lyd som egen beslutning |
| Plattformomfang | Produkt / Binding | Web + faktisk macOS-host først; iOS eksplisitt ekstra akseptanse |
| Ressursbruk og modellbudsjett | Drift / DiMy | Avgrenset syntetisk kjøring, fast grense; ingen ubegrenset AI-/swarm-last |

Full multi-master Entity-replikering, avansert quorum/recovery og automatisk offentlig transkriptpublisering inngår ikke i den foreslåtte første piloten. De to første er egne fremtidige designoppgaver; den siste krever fortsatt et eksplisitt publiseringsvalg.
