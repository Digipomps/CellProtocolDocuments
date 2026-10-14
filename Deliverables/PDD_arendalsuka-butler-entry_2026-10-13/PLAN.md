# Arendalsuka Butler-inngang

Mandat: Kjetil ba 13.10.2026 om fullført integrasjon, deploy og web/native-test. Ingen nye G1/G2-godkjenninger påstås; direkte gjennomføringsmandat brukes. Ingen endring av tilgangsgrenser eller implisitt samtykke.

## Forventet brukerreise

Ny deltaker åpner Arendalsuka og møter Butler-dialogen for formål, interesser og matching-samtykke. Svar er forslag til brukeren bekrefter. Reload gjenopptar bekreftet framdrift; avbrutt/fullført dialog forblir lukket ved automatisk inngang. «Start Arendalsuka-onboarding» eller «hjelp meg i gang med Arendalsuka» åpner korrekt dialog, også for eksisterende deltaker. Samme CellConfiguration og celle brukes via Porthole og HAVEN/Bridge.

## Arbeid og bevis

1. Felles inngangskontrakt i GuidedOnboarding, idempotent og requester-skopet. Bare bekreftede steg og lukket-status skal bevares, ingen ubekreftede svar eller modellnøkler serialiseres. Test første/ny/gjentatt inngang, avbrudd, fullført, gjenåpning, decode/reload, feil målcelle og annen requester.
2. Native-kompatibelt skeleton-panel i Arendalsuka-konfigurasjonen; oppstart gjennom eksplisitt initial action, aldri profilskriving fra GET. Test faktiske referanser, init-actions og action/state-runden. Publisert anonymt atlas skal fortsatt være lesende.
3. Butler-ruting fra innsendt forespørsel, mens utkastanalyse forblir uten aktivering. Test direkte forespørsel, negasjon, programspørsmål og generell konferanse.
4. Kunnskapsbase: mål konfig og tilgjengelig datakilde før aktivering. Foreløpig målt: ingen ARENDALSUKA_KNOWLEDGE-flagg og ingen database på standardstien i staging/prod; offentlige kunnskapsruter503. Ikke skru på et tomt lager eller publiser private eksportdata. Onboardingens lokale taksonomi og profilflyt er separat.
5. Lokale målrettede regresjoner, preflight og Linux-bygg før CI. Eksisterende reserverte byggevindu respekteres. Deploy HD-0224 med eksakt image, rollback og nye helsemålinger. Web og HAVEN testes med faktisk ny testidentitet; nåværende personprofiler overskrives ikke.

## Kilder lest av Codex

CellScaffold staging9ff06f84: GuidedOnboardingCell (utvalgte kontrakt-, state-, start-, confirm-, complete- og scriptdeler); PersonalCopilotCloudStore (ruting og akseptering av forslag); ArendalsukaEventAtlasConfigurationFactory (deltakerkonfig og skeleton); ArendalsukaParticipantProgramCell (state/konfig); ArendalsukaProfileCell; ArendalsukaConnectionHubCell; ArendalsukaKnowledgeSQLiteStore (runtime/schema); VaporConferenceMVP (offentlig rute); GuidedOnboardingCellTests og PersonalCopilotV1Tests (relevante testmetoder). Native lasting og publisher-overstyringer gjennomgås uavhengig; ikke ferdig verifisert.

## Lærdommer anvendt

- Testet kode er ikke nødvendigvis kjørende kode: arbeidsbase er live stagingcommit.
- Plan er ikke leveranse: bare faktisk runtime-akseptanse lukker oppdraget.
- Test brukerens faktiske vei: innsendt Butler-tekst og bibliotekinngang, ikke bare celle-GET.
- Grønn kildekode/testliste er ikke kjørt test: rapporter faktiske exitkoder og artefakter.
