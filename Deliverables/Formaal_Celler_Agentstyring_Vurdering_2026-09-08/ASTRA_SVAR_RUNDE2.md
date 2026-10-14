# Astra — runde 2

8. september 2026. Filstier er relative til HAVEN-roten. Kilder er lest; ingen tester, modellkjøringer eller sendinger er utført. Forslagene nedenfor er ikke levert funksjonalitet.

## M1. Dataeierens kontroll over andres agent

**Ja til en selvstendig tillitsgrense hos ressurseieren; nei til historisk ny sikkerhetsklasse eller ubetinget «uten å stole på operatøren».** Innsnevringen gjør produktargumentet vesentlig sterkere. Gjesten kan nekte Palazzo-agenten tilgang selv om Palazzo tillater handlingen. Men dette forutsetter at gjestens håndhevingsmiljø og nøkler faktisk er utenfor Palazzos kontroll. Datasubjekt, ressurseier og autorisasjonsutsteder er forskjellige roller; arkitekturen må etablere at gjesten har den siste rollen. [vurdering]

En direkte forgjenger er **User-Managed Access, UMA 2.0**. Standarden lar ressurseieren styre tilgang for selvstendige forespørrende parter gjennom en autorisasjonstjeneste, på tvers av tjenester og domener. [UMA, særlig §1.4](https://docs.kantarainitiative.org/uma/wg/rec-oauth-uma-federated-authz-2.0.html). Solid beskriver dessuten desentralisert tilgangskontroll på tvers av domener. [Solid WAC](https://solidproject.org/TR/wac). Jeg ville kalt HAVEN-egenskapen **ressurseierstyrt autorisasjon med håndheving ved ressursen**. Dette er et arkitekturvalg leverandørers lokale verktøysperrer ikke alene realiserer; eksisterende autorisasjonsinfrastruktur kan realisere det. [vurdering]

HAVEN har relevante byggesteiner: identitetsbundet Contract/Grant, bruksautorisasjon og en correspondence-adapter som fører eksterne operasjoner gjennom Resolver. Den lokale relasjonsposten inneholder en Contract, mens fjernsidens Resolver fortsatt avgjør operasjonen. Eierarkivets signerte snapshot må ikke forveksles med en bilateral avtale. [belagt: HavenAgentD/Sources/HavenCorrespondenceMCP/CorrespondenceContracts.swift:96; HavenAgentD/Sources/HavenCorrespondenceMCP/CorrespondenceCellTransport.swift:25; CellProtocolDocuments/Book/04_Agreements_Contracts.md:206]

Over scaffold-grenser må én konkret bane dokumentere autentisert requester og mottakertjeneste, korrekt domene-/ressursbinding, fersk autorisasjon, replayvern og identisk effektkontroll hos utføreren. Transporttilkobling alene er utilstrekkelig. Universell dekning er ikke dokumentert. [belagt: CellProtocolDocuments/Book/06_CellResolver.md:74] [usikker]

Den avgjørende grensen kommer ved utlevering: Palazzo kan kopiere klartekst som allerede er mottatt. Repoet sier dette uttrykkelig. Gi derfor helst et avgrenset svar fra gjestens celle fremfor hele historikken. Et kontrollspor kan dokumentere tillatt utlevering; det beviser ikke all senere bruk eller fravær av skjulte handlinger. Losens formulering «bevise etterpå at den holdt seg innenfor» er fortsatt for sterk. [belagt: CellProtocolDocuments/Book/04_Agreements_Contracts.md:86] [vurdering]

## M2. Fast formål og action→purpose

**Du har rett om dagens A4.** Profilen fastsetter primærformålet, og kontrollen krever samsvar mellom action, formål og bundet policy. Min etikettkritikk traff en mulig fremtidig utforming, men ble for lett lest som beskrivelse av denne implementasjonen. [belagt: CellScaffold/Sources/App/Cells/AI/AIGatewayPurposePolicy.swift:17; CellProtocol/Sources/CellBase/Agreement/PurposeBoundExternalAction.swift:671]

En beskyttet action→purpose-tabell fjerner modellens frie ommerking. Men velger modellen action, velger den indirekte tabellrad. Oppdraget må derfor på forhånd begrense hvilke actions og profiler modellen kan foreslå. Ellers kan den velge en tillatt «kundeservice»-action for et markedsføringsærend. Tabellforvalteren kontrollerer betydningen; agenten kan fortsatt misbruke tillatte operasjoner. [vurdering]

Formål gir en sikkerhetsgevinst når det tilfører **uavhengig godkjent oppgavekontekst**: samme mottaker, ressurs og operasjon kan være tillatt i ett oppdrag og avslås i et annet. Formål kan organisere dette konsekvent på tvers av celler. Gevinsten kan også uttrykkes med oppgave-ID og kontekstpolicy; den krever ingen ny sikkerhetsprimitiv. Er formålet bare en entydig omskriving av action, tilfører det ingen selvstendig informasjon til beslutningen. [vurdering]

Forklarbarhet, gjenbruk og sammenligning mellom parter kan likevel forsvare kostnaden, hvis piloten viser færre forståelses- eller konfigurasjonsfeil. Samme referanse og digest beviser enighet om representasjonen, ikke om motivet. Dessuten er `ownerConfirmed` i dagens konstruktør en standardverdi, ikke i seg selv et autentisert menneskelig godkjenningsbevis. [belagt: CellScaffold/Sources/App/Cells/AI/AIGatewayPurposePolicy.swift:139] [vurdering]

## M3. En konkret ramme og betrodde observasjoner

**Rammen bør være en versjonert oppgaveprofil som bindes til eksisterende autorisasjon.** Den bør angi utsteder, utføreridentitet, målressurser, tillatte actions, primærformål, databegrensninger, mottakere, budsjett/effektantall, gyldighet og tilbakekalling. Eierens godkjenning bindes til profilens digest. Hver effekt må tilfredsstille både gyldig Contract og profilens ceiling. Profilen er et forslag til sammensetting, ikke et eksisterende universelt objekt eller en ny kilde til rettigheter. [vurdering]

Innen rammen kan en betrodd adapter kontrollere eksakte argumenter, mottaker, policyversjon og aktuell fullmakt, samt reservere en effekt før utførelse. Dette krever ikke modellens vurdering. Numeriske budsjettsperrer må ligge i utføreren; dagens enkle Goal-verdipredikater er ikke en generell budsjettmotor. [belagt: CellProtocol/Sources/CellBase/PurposeAndInterest/GoalEvaluationEngine.swift:252] [vurdering]

Betrodd betyr her «autoritativ for denne bestemte opplysningen»:

- **Resolver/Cell:** kan avgjøre aktuell adgang ved den beskyttede operasjonen. Agentens gjenfortelling av beslutningen er ikke tilsvarende bevis. [belagt: CellProtocolDocuments/Book/06_CellResolver.md:74]
- **EntityAnchor:** den undersøkte commit-banen verifiserer Contract-binding, lagrer og leser tilbake record/kvittering. Det underbygger akkurat denne lagringen; det beviser ikke at innholdet er sant eller at et menneske godkjente meldingen. [belagt: CellProtocol/Sources/CellApple/Cells/EntityAnchorCell.swift:552]
- **Gatewayens kvotebane:** utfører reservasjon før modellkjøring når kvotemodusen krever det. Den er et grunnlag for kontroll av den aktuelle ressursbruken, ikke en universell oppgavekvote; kodebanen er betinget av `prepaidDimy`. [belagt: CellScaffold/Sources/App/Cells/AI/AIGatewayCell.swift:819]

Ingen av disse blir automatisk autentiserte Goal-observasjoner. Motoren mottar observasjoner som input. Modellgenererte `fresh`, `human-confirmation` eller GUI-/stedsetiketter må derfor ikke utløse autorisasjon uten en separat verifisert produsent. [belagt: CellProtocol/Sources/CellBase/PurposeAndInterest/GoalEvaluationEngine.swift:66] [vurdering]

Logg fra dag én **overflødige godkjenningsdialoger per fullført legitimt oppdrag**. Tell dialoger der samme effekt eller fortsatt gyldige ramme allerede er godkjent, uten relevante endringer. Logg oppgave-ID, effektdigest, profilversjon og spørregrunn fra porten. Målet er null. Dette måler unødvendige avbrudd, en praktisk indikator på tretthet; det måler ikke brukerens oppmerksomhet direkte. [vurdering]

## M4. Minste endring for et konkret «ja»

**Behold meldingsformatet, men legg en uomgjengelig godkjenningsport hos avsenderen.** Dette gir lokalt etterprøvbart godkjenningsbevis. Det oppfyller ikke automatisk det strengere ønsket om at fjerncellen selv kontrollerer menneskets ja. [vurdering]

Den indre signaturen dekker allerede innhold, emne, innholdstype, klientmelding-ID og avsenderidentitet. Transportens signatur dekker header og kryptert innhold; cellen kontrollerer denne og medlemsbindingen. `CorrespondenceSendRequest` inneholder ikke et menneskelig godkjenningsbevis, og den indre konvolutten er kryptert for serveren. Dagens avsendersignatur betyr derfor ikke «eieren har sett og godkjent». [belagt: CellProtocol/Sources/CellBase/Cells/Correspondence/CorrespondenceEnvelope.swift:95; CellProtocol/Sources/CellBase/Cells/Correspondence/CorrespondenceEnvelope.swift:132; CellProtocol/Sources/CellBase/Cells/Correspondence/CorrespondenceCell.swift:318]

Minste forsvarlige lokale utforming er følgende. [vurdering]

1. Porten fryser innhold, emne, klientmelding-ID og den ferdige krypterte forespørselen. En betrodd visning viser samme klartekst, mottakere, formål og lagringstid som porten binder.
2. Etter eierens ja i visningen signerer eierens separate godkjenningsnøkkel en domeneseparert, kanonisk post med innholdsdigest, digest av hele send-forespørselen, cellens identitet/endepunkt, relasjon/medlemsfingeravtrykk, avsender, profilversjon, engangs-ID og kort gyldighet. Dermed bindes også formål og lagringstid, som ikke inngår i den indre signaturen.
3. Porten verifiserer posten mot forhåndsregistrert eiernøkkel, gjentar aktuelle adgangssjekker og reserverer engangs-ID atomisk og varig før sending. Endring ugyldiggjør godkjenningen. Ukjent utfall etter timeout skal undersøkes før et nytt sendeforsøk; dagens celle oppretter ny meldings-ID ved hvert godtatt kall.
4. Agenten får verken godkjenningsnøkkelen, ubeskyttet sendetilgang eller en generell signeringsfunksjon. Den lokale signerte posten og sendestatusen knyttes sammen uten råtekst i auditloggen.

Ny ID per sending er synlig i implementasjonen; en klient-ID alene er ikke dokumentert deduplisering. [belagt: CellProtocol/Sources/CellBase/Cells/Correspondence/CorrespondenceCell.swift:356]

Hvis **fjerncellen** skal verifisere godkjenningen før lagring, må den få en verifiserbar godkjenningspost, enten separat registrert og oppslått gjennom forespørselsdigest eller gjennom en utvidet send-kontrakt. Konvoluttformatet kan beholdes, men autorisasjonssemantikken og bevisutvekslingen er nye. Jeg kan ikke belegge en eksisterende kanal som gjør dette ferdig i dag. Ikke skjul beviset i `purposeRef` eller `clientMessageID`. [usikker] [vurdering]

Innlesing og vanlig kvittering innen en uttrykkelig godkjent relasjon bør kunne kjøre automatisk. Kvitteringen er en synlig sideeffekt og må beskrives ved oppsett: dagens `ackMessage` setter én servertilstand til `acknowledged`. Den betyr ikke at mennesket har lest eller godtatt innholdet. [belagt: CellProtocol/Sources/CellBase/Cells/Correspondence/CorrespondenceCell.swift:390] [vurdering]

## M5. Velg correspondence, med en avgrenset beslutning

**Jeg velger (ii), correspondence send.** Her finnes en konkret effekt og en eksisterende kjede å forbedre. Palazzo legger til brukerflate og tolkning av gjestedata; arbeidskøen legger til en ny utfører. Correspondence kan først avgjøre om formålsbinding gir merverdi i en faktisk delegert handling. Den lokale varianten i M4 kan ikke alene bevise M1s uavhengighet fra agentoperatøren. [vurdering]

Minste løkke er: innlest testmelding → modellens strukturerte utkast → betrodd validering og profilvalg → konkret godkjenning → én sending → kontroll av mottakercellens lagrede konvolutt. JSON-tekst fra modellen er tilstrekkelig; native tool-calling eller en generell AIGateway-løkke er unødvendig. Kjør først med syntetiske relasjoner og isolerte mottakerceller. [vurdering]

Pilotens nødvendige P0 er: beskyttet policy og nøkkeltilgang; én tillatt sendebane gjennom M4-porten; konkrete mottaker-/payloadkontroller; ubetrodd meldingsinnhold adskilt fra kontrollfeltene; og avslag ved ukjent profil eller forsøk på utvidelse. Varig engangsreservasjon og håndtering av ukjent sendeutfall blir også inngangskrav. Generell scriptsandbox, per-Grant V2, universell celleattestasjon og distribuert revokasjon behøves ikke når disse mulighetene ikke åpnes. Agentprosessen må likevel være isolert fra alternative sendemidler. [vurdering]

Forhåndsregistrer **20 legitime og 20 adversarielle tilfeller**, i tre varianter: kompetent minst-privilegium med samme godkjenningsport; denne med forklarende formålstekst; og full oppgave-/formålsbinding. Hold modell, nøkkelisolasjon, godkjenningskrav og grunnleggende ressursgrenser like. Gi baselinen ordinær kontekstpolicy der oppgaven krever det. [vurdering]

Legitime tilfeller skal dekke utkast, avslag, innholdsendring før ja, relasjonsbytte med nytt ja, automatisk lesing/kvittering og ukjent sendeutfall. Angrep skal dekke falskt «eieren har godkjent», injisert verktøybeskrivelse, etterfølgende payload-/mottakerbytte, feil oppgaveprofil, utløpt godkjenning, replay, samtidige kall og direkte omgåelse. Tell faktiske lagringer/dekrypterte testmeldinger fra mottakersiden, ikke modellens suksesspåstand. [vurdering]

Krav: null uautoriserte eller doble effekter; minst 18 av 20 legitime oppgaver løst og ikke færre enn baseline; null overflødige dialoger. Mål dessuten operatørtid og om brukeren korrekt identifiserer mottaker og avslagets grunn. En uautorisert effekt stopper kjøringen straks for feilanalyse. **Snu-kriteriet** er at full binding etter høyst to avgrensede forbedringsrunder verken reduserer policy-/forståelsesfeil eller avbrudd, samtidig som operatørtiden overstiger baseline med over 20 prosent. Da beholdes autorisasjon og konkret godkjenning, mens formål forenkles til forklaring i denne arbeidsflyten. Tersklene er foreslåtte beslutningsregler, ikke forskningsresultater. [vurdering]

Kredittmangel hindrer ikke deterministiske angrepsforslag mot porten. Repoet har også en lokal modellprofil uten API-nøkkelkrav; en tilgjengelig lokal modell kan produsere utkast og injeksjonsforsøk. At modellen faktisk kjører nå, er ikke kontrollert. Lokal kjøring dokumenterer heller ikke A4-providerbanen, som uttrykkelig utelukker lokale modeller. [belagt: CellScaffold/Sources/App/Cells/AI/AIGatewayModels.swift:1071; CellScaffold/Sources/App/Cells/AI/AIGatewayCell.swift:2830] [usikker]

**Jeg endrer fra runde 1:** Jeg vektlegger ressurseierens uavhengige håndhevingsgrense sterkere, og korrigerer etikettkritikken for dagens fastlåste A4-profil. Jeg nedprioriterer en ny gateway-integrert tool-løkke: piloten kan bruke correspondence-kjeden med en ny godkjenningsport. Jeg fastholder at formål ikke er en ny sikkerhetsprimitiv, at etterfølgende databruk ikke er kontrollert, og at formålslagets praktiske merverdi er et åpent spørsmål piloten må avgjøre. [vurdering]

<!-- ASTRA RUNDE 2 FERDIG -->
