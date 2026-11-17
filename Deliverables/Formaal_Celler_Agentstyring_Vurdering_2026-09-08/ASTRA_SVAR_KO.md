# Astra — formål og Celler som styring av AI-agenter

8. september 2026. Analyse, ingen implementering.

**Hovedvurdering:** Fortsett med en avgrenset, målt pilot. HAVEN har en reell mekanisme for å begrense bestemte handlinger, men har ikke dokumentert generell agentkontroll eller noen ny sikkerhetsprimitiv. Verdien ligger i sammenhengen mellom erklært formål, konkret myndighet, kontrollert utførelse og etterprøvbar dokumentasjon. Den sammenhengen er foreløpig ufullstendig. [vurdering]

**Brief audit.** Fire premisser må korrigeres eller innsnevres:

1. En signert Contract er ikke en signert handlingskvittering. `ActionDecisionReceipt` inneholder statuser og digester, men ingen egen signatur; returfunksjonen legger ved objektet uten signering. Briefens D3 er derfor for sterkt formulert. [belagt: CellProtocol/Sources/CellBase/Agreement/PurposeBoundExternalAction.swift:516; CellScaffold/Sources/App/Cells/AI/AIGatewayCell.swift:1129]
2. Leverandørenes mekanismer er også kontekstuelle og deployer-styrte. «Bare logg», «ingen delt intensjon» og «ofte fail open» er ikke holdbare generelle kategorier. Se kildene og D1–D9 i Q5. [vurdering]
3. «Goals som matematiske uttrykk» overdriver dagens evaluator: verdipredikatet støtter likhet, ulikhet og tekstinnhold, ikke generell numerisk eller temporal logikk. [belagt: CellProtocol/Sources/CellBase/PurposeAndInterest/GoalEvaluationEngine.swift:252]
4. Tallet «93 % godkjenning» mangler etterprøvbar kilde i briefen og brukes ikke som evidens her. [usikker]

**Avgrensning:** Filstier nedenfor er relative til `/Users/kjetil/Build/Digipomps/HAVEN`. Kode, tester og dokumentasjon er undersøkt målrettet i CellProtocol, CellScaffold, HavenAgentD, HAVEN-Deploy og CellProtocolDocuments. Søkene omfattet autorisasjon, kvitteringer, modellverktøy, Goals og correspondence; bygg/cache var utenfor evidensgrunnlaget. Ingen tester eller live handlinger er kjørt. Historiske testresultater betegnes som rapporterte, ikke bekreftet på nytt. Nettkilder er offisielle sider hentet denne dagen. Merkingene skiller filbelegg, min vurdering/forslag og uavklart kunnskap.

## Q1. Annen klasse av begrensning, eller kjent teknikk?

**Annen klasse enn en promptinstruks, samme hovedklasse som kapabiliteter og eksternt håndhevet policy.** Å sammenligne HAVENs autorisasjonskode med leverandørens modelltrening alene ville gi HAVEN en kunstig fordel. Riktig sammenligning er hele kjeden: modell, verktøysperre, tjenesteautorisasjon og operativsystem. [vurdering]

Minst-privilegium og formålsinnsnevring er kjent teknikk. Allerede Macaroons beskrev delegerbare rettigheter med vilkår som begrenser blant annet kontekst og formål. Cedar skiller hvem, handling, ressurs og kontekst; OPA skiller policybeslutningen fra applikasjonens håndheving. SPIFFE gir identitet til kjørende programvare. Dette er relevante sammenligningsgrunnlag, ikke funksjoner HAVEN kan regne som oppfunnet her. [Macaroons](https://research.google/pubs/macaroons-cookies-with-contextual-caveats-for-decentralized-authorization-in-the-cloud/), [Cedar](https://docs.cedarpolicy.com/), [OPA](https://www.openpolicyagent.org/docs), [SPIFFE](https://spiffe.io/docs/latest/spiffe-about/overview/).

HAVENs konkrete bidrag er integrasjonen: samme cellemodell knytter oppdagbare handlinger, identitet og Agreement/Contract til en statisk policybinding og dynamiske handlingsfakta. I A4 kontrolleres eksisterende myndighet **og** eksakt ceiling **og** samsvar med den faktiske forespørselen. Formål kan ikke opprette myndighet. Dette er en ny funksjon i HAVEN og en mulig særpreget produktkombinasjon; internasjonal originalitet er ikke påvist. [belagt: CellProtocolDocuments/Deliverables/Purpose_Bound_External_Action_Contract_2026-08-03/A4_IMPLEMENTATION_REPORT.md:8] [vurdering]

Den interessante forskjellen er hvem som kan uttrykke en begrensning, og om begrensningen følger data og handling på tvers av modellbytte. Men dagens A4-policy er en kompilert profil med ett fast primærformål og tre godkjente leverandørdestinasjoner. «Eier-styrt» beskriver derfor arkitekturretningen bedre enn en ferdig selvbetjent policyfunksjon. [belagt: CellScaffold/Sources/App/Cells/AI/AIGatewayPurposePolicy.swift:12] [vurdering]

En digest beviser samsvar mellom representasjoner; den beviser ikke at hensikten er oppriktig, innholdet nødvendig eller utførelsen moralsk riktig. Et system som oppfører seg konsistent etter feil policy, er fortsatt feil. Formålet «Alle mennesker er like mye verdt» er en normativ forankring, ikke et beregnbart sikkerhetsbevis. [belagt: CellProtocolDocuments/Book/23_Purpose_Knowledge_Base.md:30] [vurdering]

## Q2. Hva styres faktisk når modellen ikke har en tool-løkke?

Briefens avgrensning er riktig for **A4**, men for snever som beskrivelse av **alle Celler**. Celler begrenser også eksisterende lokale tjenester og correspondence-operasjoner uavhengig av hvem som kaller. HavenAgentD dokumenterer egne celler, signerte remote intents, nonce-kontroll, gjennomgang og allowlistede handlinger. Det er reell kontroll, men ikke samme A4-kontrakt eller generell kontroll over Mac-en. [belagt: HavenAgentD/README.md:129] [vurdering]

I den undersøkte AIGateway-koden finnes ingen modellstyrt verktøyutførelse. Den deklarerte verktøypolicyen kan avvise en forespørsel; ved tillatelse formuleres begrensningen til modellen som systemtekst. Tekstlig verktøybruk eller påstander om utførte handlinger forblir avhengige av modellens oppførsel. Fravær av utfører gjør faktisk verktøyutførelse umulig på denne banen, men demonstrerer ikke sikker kontroll over en agent som kan handle. [belagt: CellScaffold/Sources/App/Cells/AI/AIGatewayCell.swift:1805; CellScaffold/Sources/App/Cells/AI/AIGatewayCell.swift:2104] [vurdering]

«Agenten foreslår, cellene bestemmer» er sant når cellen er en uomgjengelig utførelsesgrense. Har samme agent direkte shell, nettverk, brukerens nøkler eller andre MCP-servere, gjelder utsagnet bare cellens tjenester. Agenten kan omgå arbeidsflyten gjennom andre fullmakter. De fullmaktene må begrenses av vertsmiljøet; flere formålsnoder løser ikke dette. [vurdering]

Correspondence viser et viktig skille. Verktøyet mottar relasjon, innhold og formålsreferanse og kaller `sendMessage`. Klienten sjekker aktiv relasjon og medlemskap, krypterer meldingen og påkaller cellen. Jeg finner ikke et payload-bundet menneskelig godkjenningsbevis i denne kallekjeden. At eier har godkjent relasjonen, beviser ikke godkjenning av hver melding. Kravet om eksplisitt ja før sending må derfor ikke presenteres som dokumentert per-melding-håndheving; en eventuell separat klientsperre er ikke verifisert. [belagt: HavenAgentD/Sources/HavenCorrespondenceMCP/CorrespondenceMCPService.swift:97; HavenAgentD/Sources/HavenCorrespondenceMCP/CorrespondenceClient.swift:382] [usikker]

A4 beskytter dessuten forespørselens struktur bedre enn innholdets mening. Dataklassene er «user-prompt» og «system-instruction». En hemmelighet limt inn i en ellers tillatt prompt blir ikke nødvendigvis avvist: samme tekst kan være korrekt digest-bundet og fortsatt uegnet for utlevering. [belagt: CellScaffold/Sources/App/Cells/AI/AIGatewayPurposePolicy.swift:31] [vurdering]

**Praktisk dom:** Dette er et anvendelig utviklingsgrunnlag, men drift uten Kjetil/Claude/Codex er ikke dokumentert. Palazzo-kelneren bør se «lag et svarutkast til denne gjesten» og forstå mottaker, data og konsekvens. Hvis vedkommende må velge taksonomireferanser, tolke digester eller reparere Agreements, er produktet ikke klart. Oppsett, nøkkellivsløp, avslag og gjenoppretting må kunne håndteres gjennom ferdige oppgaveprofiler. [vurdering]

## Q3. T1–T15, approval fatigue og MCP-hijacking

Klassifikasjonen gjelder implementasjonen nå. «Løses strukturelt» betyr at kode håndhever den angitte, avgrensede egenskapen selv om modellen oppfører seg feil; det betyr ikke at hele angrepsfamilien er eliminert. Grunnlag: trusselmodellen, autorisasjonsmotoren, gatewaybindingen og de negative testene. [belagt: CellProtocolDocuments/Deliverables/Purpose_Bound_External_Action_Contract_2026-08-03/THREAT_MODEL.md:31; CellProtocol/Sources/CellBase/Agreement/PurposeBoundExternalAction.swift:619; CellProtocol/Tests/CellBaseTests/PurposeBoundExternalActionTests.swift:8]

| Trussel | Klassifikasjon og konkret grense [vurdering] |
|---|---|
| **T1 Purpose laundering** | **Løses ikke semantisk.** Exact match blokkerer brede eller feil referanser strukturelt. Men noen kan velge riktig referanse for en upassende handling. Fast «answer-user-prompt» kontrollerer ikke nødvendighet eller faktisk hensikt. |
| **T2 Prompt injection** | **Løses strukturelt for endring av A4-myndighet/destinasjon; løses bare i prompt for modellens innholdsatferd.** Injisert tekst kan ikke omskrive installert policy, men kan forurense svar og få modellen til å foreslå en dårlig handling innenfor tillatt scope. |
| **T3 Parent escalation** | **Løses strukturelt i A4.** Foreldrematch gir ingen rett til barnets handling. Avhenger ikke av modellens tolkning av treet. |
| **T4 Facet escalation** | **Løses strukturelt i A4.** Facets gir ingen myndighet; misvisende presentasjon kan fortsatt lure brukeren. |
| **T5 Confused deputy** | **Løses strukturelt for A4s avgrensede delegasjon; løses ikke generelt.** Requester-autorisasjon og smal policy kontrolleres før credentialbruk. Andre tjenester med brede fullmakter krever egne grenser. |
| **T6 Direkte script-egress** | **Løses ikke av A4.** Scripts og vertsprosesser må sperres eller isoleres utenfor modellen. En instruks om å bruke Celler er utilstrekkelig. |
| **T7 Config/policy substitution** | **Løses strukturelt i A4 for bundne komponenter.** Installert profil og observerte digester må samsvare. Kompromittert runtime eller policyutgiver ligger utenfor garantien. |
| **T8 Payload substitution** | **Løses strukturelt for bytte av den kanoniske gatewayforespørselen.** Dette er ikke uavhengig bevis for alle bytes som til slutt passerer transporten; adapteren inngår i tillitsbasen. |
| **T9 Storage → disclosure** | **Løses strukturelt som skillet mellom lagringsrett og den smale utleveringshandlingen.** Gatewayen setter disclosure-evidens fra godkjent action-autorisasjon. Dette er ingen generell informasjonsflytsporing; kopiering etter mottak løses ikke. |
| **T10 Trust theater** | **Løses strukturelt mot at en tillitspakke alene gir A4-tilgang.** Tillitsteater i brukergrensesnitt eller offentlig omtale løses ikke av formatet. |
| **T11 Stale evidence** | **Løses ikke ende til ende.** Merket utløpt evidens avvises, men gatewayen tar evidensstatus fra requesten; en `current`-etikett er ingen selvstendig ferskhetskontroll. Contract-gyldighet er en separat kontroll. |
| **T12 Owner bypass** | **Løses strukturelt i A4.** Owner må også tilfredsstille ceiling. Andre adaptere er ikke dermed dekket. |
| **T13 Receipt overclaim** | **Løses strukturelt som statusskille; faktisk eksternt effektbevis løses ikke.** `completed` settes av gatewayen. Verken mottakersignatur eller egen kvitteringssignatur følger automatisk. |
| **T14 Audit-log leakage** | **Løses strukturelt for utelatelse av rå prompt/output i dette kvitteringsformatet; øvrig logging løses ikke generelt.** Også digester og referanser kan lekke sammenhenger eller avsløre laventropidata gjennom gjetting. |
| **T15 Dokumentasjon/runtime-gap** | **Løses ikke strukturelt.** God dokumentasjon og tester reduserer feilpåstander, men briefens egen signaturpåstand demonstrerer residualen. |
| **Approval fatigue** | **Løses ikke av cellemodellen.** Flere detaljer og flere dialoger kan forverre problemet. Relasjonstillatelse må skilles fra samtykke til en bestemt effekt. |
| **MCP tool hijacking** | **Løses ikke generelt.** En kompromittert server, endret verktøybeskrivelse eller injisert resultat kan villede agenten. Celleautorisasjon begrenser bare handlinger som faktisk går gjennom den kontrollerte adapteren. |

For T9, T11 og T13 er detaljene særlig synlige i gatewayens evidensbygging og kvitteringsretur. `trustPackageEvidence` kan utelates som `notRequired`; klientens `current` kontrolleres ikke mot en ekstern attestutsteder her. [belagt: CellScaffold/Sources/App/Cells/AI/AIGatewayCell.swift:1089; CellProtocol/Sources/CellBase/Agreement/PurposeBoundExternalAction.swift:740]

MCPs HTTP-autorisasjon krever mottakerspesifikke tokens og validering av tiltenkt ressurs. Det reduserer tokenmisbruk; det gjør ikke verktøybeskrivelsen sann eller serverens implementasjon trygg. Lokal stdio har dessuten en annen autentiseringsmodell. HAVEN bør kombinere disse grensene med kontrollerte serveridentiteter og smale handlinger. [MCP-autorisasjon](https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization). [vurdering]

## Q4. Deterministiske Goals og grensen mot modellvurdering

**En høy andel av tillatelseskontrollene kan være deterministiske; ingen forsvarlig prosentandel av «agentstyringen» kan angis uten en konkret oppgavemengde.** Adgang, ressurs, mottaker, gyldighetstid og effektantall er gode maskinelle grenser. Å avgjøre hva som er nyttig, rettferdig eller et godt svar er en annen oppgave. [vurdering]

Dagens motor evaluerer eksplisitte observasjoner med boolske kombinasjoner, etiketter, hendelser, enkle strengpredikater og nettverksfeilstatus. Testen for semantisk sted/tid blir tilfredsstilt når innsendte etiketter matcher. Dette er deterministisk evaluering av representerte fakta, ikke måling av verden. Evaluatortypene alene dokumenterer verken GPS-integrasjon, sikker klokke eller en autonom GUI-tester. [belagt: CellProtocol/Sources/CellBase/PurposeAndInterest/GoalEvaluationEngine.swift:68; CellProtocol/Tests/CellBaseTests/GoalEvaluationEngineTests.swift:8]

Observasjonskilden blir derfor en sikkerhetsgrense. Hvis agenten både utfører oppgaven og leverer hendelsen «human-confirmation», får vi deterministisk godkjenning av en mulig løgn. En følsom kontroll trenger autentisert produsent, aktualitet og binding til riktig handling. Motorens `confidence` er heller ikke sannsynlighetsbevis: uten innsendte konfidensverdier returnerer den normalt 0,8 når observasjoner finnes. [belagt: CellProtocol/Sources/CellBase/PurposeAndInterest/GoalEvaluationEngine.swift:275] [vurdering]

Skill tre ting: mål for ønsket sluttresultat, sikkerhetsinvarianter som alltid må holde, og stoppregler for videre arbeid. Et «satisfied»-resultat stanser ikke en utfører av seg selv. `GoalEvaluationCell` er en adapter for definisjoner, observasjoner og evaluering; en sikkerhetskritisk konsekvens må kobles eksplisitt til handlingsgrensen. [belagt: CellProtocol/Sources/CellBase/Cells/Purpose/GoalEvaluationCell.swift:6] [vurdering]

«Goal som prompt» er en instruks, ikke en hard begrensning. En modell kan foreslå klassifikasjon og delmål, men forslaget må ikke produsere egen myndighet eller egen godkjenningsobservasjon. Bruk modeller der semantisk vurdering trengs; la uavhengige kontroller begrense konsekvensen av feil. For «bidra positivt» trengs avgrenset nytte, skadeindikatorer og menneskelig vurdering, ikke én universell score. [vurdering]

## Q5. Intent/kvittering mot autonomiramme, hooks og managed policy

Model Spec beskriver en avtalt autonomiramme: tillatte delmål, akseptable sideeffekter og når agenten skal stoppe eller spørre. Den omtaler også risikoen ved så mange bekreftelser at brukeren godkjenner automatisk. Det er en eksplisitt intensjonsmodell, men en normativ atferdsspesifikasjon er ikke bevis for perfekt etterlevelse. [Model Spec, 18. august 2026](https://model-spec.openai.com/2026-08-18.html#act-within-an-agreed-upon-scope-of-autonomy).

Claude Codes permission-regler og `PreToolUse` kan blokkere faktiske verktøykall. Codex `requirements.toml` kan begrense tillatte sandkasse- og godkjenningsvalg; dagens dokumentasjon omfatter også administrerte tillatelsesprofiler. Dette er reelle sperrer utenfor den handlende modellen. [Claude Code permissions](https://code.claude.com/docs/en/permissions), [Codex managed configuration](https://learn.chatgpt.com/docs/enterprise/managed-configuration).

Tabellen korrigerer briefens motsetninger. HAVEN-kolonnen bygger på A4-koden, Contract-kapitlet og avgrensningene ovenfor; sammenligningene er vurderinger, ikke målte konkurransefortrinn. [belagt: CellScaffold/Sources/App/Cells/AI/AIGatewayPurposePolicy.swift:75; CellProtocolDocuments/Book/04_Agreements_Contracts.md:206] [vurdering]

| Dimensjon | Leverandør/deployer | HAVEN nå |
|---|---|---|
| **D1 Eier** | Leverandørens grunnregler; deployers lokale policy. | Cellemyndighet og utsteders Contract; A4-profilen er utviklerinstallert. |
| **D2 Håndheving** | Modell, tool-gate og vertssandbox. | Resolver/Cell og ekstra A4-gate; ingen generell vertssandbox. |
| **D3 Bevis** | Logger og produktspesifikke kontrollspor. | Signert Contract-binding; strukturert A4-kvittering uten egen signatur. |
| **D4 Granularitet** | Verktøy, argumenter, stier, domener og kontekst. | Konkret keypath og bundne handlingsfakta; svært smal A4-profil. |
| **D5 Flere aktører** | Identitets-, OAuth- og applikasjonspolicy kan komponeres. | Felles cellekontrakter er lovende; dagens snapshot er ikke flerpartssignert. |
| **D6 Angrep** | Hard gate tåler modellfeil innen eget scope. | Samme prinsipp; kvaliteten på fakta og komplett mediering avgjør. |
| **D7 Kostnad** | Oppsett, kontrollregler, avklaringer og modellbruk. | I tillegg formålstaksonomi, avtalevedlikehold og digester; ingen sammenlignende måling. |
| **D8 Ukjent** | Avslag eller avklaring er konfigurerbart. | Ukjent formål avvises i A4; ikke dokumentert universell egenskap. |
| **D9 Dekning** | Bred verktøydekning i klienten, med produkt-/modusavhengige unntak. | Én A4-providerbane, pluss andre lokale autorisasjonsgrenser. |

HAVENs form kan være bedre for en dataeier eller tjenesteoperatør som trenger samme etterprøvbare ramme på tvers av assistenter. For én utvikler med ett repo kan eksisterende sandbox og hooks gi mindre friksjon og større faktisk dekning. [vurdering]

Lån direkte: administrert policy som agenten ikke kan endre, deny-first-regler, eksplisitt kontroll før utførelse, minst-privilegium per oppgave og gjenopptakelse etter avklaring. Bruk hooks som integrasjon til cellekontrollen, men normaliser handlingen før kontroll; et shell-kommandoprefiks er ikke en full beskrivelse av effekten. [vurdering]

## Q6. Komplementaritet og hva HAVEN ikke bør erstatte

HAVEN bør kreve en dokumentert minsteprofil av vertsbegrensninger, og beholde leverandørens sikkerhetslag når en slik modell brukes. Autorisasjonen bør samtidig tåle at modellen følger en ondsinnet instruks: et gyldig modellforslag er fortsatt bare input til kontrollen. «Defense in depth» betyr uavhengige feilbarrierer, ikke at hver barriere antar at den andre allerede har godkjent. [vurdering]

HAVEN kan ikke med formål og Grants erstatte modellens trening, interne risikokontroller, leverandørens tjenestevilkår eller faktisk kontroll over leverandørens infrastruktur. En tillatt forespørsel kan fortsatt gi farlig eller feil innhold. En lokal modell fjerner heller ikke behovet for innholdsevaluering; da flyttes ansvaret for slike kontroller til operatøren. [vurdering]

Operativsystemisolasjon er også en egen oppgave. Codex bruker blant annet Seatbelt på macOS og bubblewrap på Linux. Dette er relevant eksisterende infrastruktur HAVEN kan bygge på, fremfor å forsøke å oppnå prosessisolasjon gjennom Swift-objektgrenser eller prompts. [Codex sandbox](https://learn.chatgpt.com/docs/sandboxing). [vurdering]

HAVEN bør ikke bygge en egen generell innholdsmoderator, en universell moralberegner eller en komplett agentplattform bare for å få én beskyttet arbeidsflyt. Bruk eksisterende modeller, sandkasser og autorisasjonsstandarder; konsentrer eget arbeid om data-/handlingstilpasset delegasjon, etterprøvbar utførelse og forståelig brukerinteraksjon. [vurdering]

Leverandøren skal likevel ikke få definere brukerens lokale forretningsmyndighet: at modellen vil utføre en handling, gir ingen tilgang til HAVEN-data. Omvendt kan ikke en gyldig HAVEN-Contract oppheve leverandørens tjenestebegrensninger. [vurdering]

## Q7. Hva mangler, og hva bør prioriteres?

Alle tiltakene nedenfor er **forslag**, ikke nye påstander om levert funksjonalitet. P0 betyr nødvendig før den aktuelle effektbanen åpnes; P1 før begrenset ordinær drift; P2 ved dokumentert bruksbehov; P3 forskning eller utsatt utvidelse. S er en lokal endring, M en integrasjon med målrettet verifikasjon, L arbeid på tvers av runtime/protokoll/operasjon. Dette er relative størrelser, ikke tidsestimater. [vurdering]

| Pri./størrelse | Funksjonalitet og eksisterende grunnlag | Løser / løser ikke [vurdering] |
|---|---|---|
| **P0 / M** | **Dekningskontrakt og beskyttet policy.** Bygg på Resolver, A4-profilen og vertsrestriksjoner. Kartlegg og sperr alternative effektveier, også legacy-aliaser, direkte credentials og policyfiler. | Løser omgåelse av den valgte grensen. Løser ikke innholdsmessig dårlige handlinger innen tillatt scope. Dokumenter nøyaktig hvilken utfører som har hvilke utganger. |
| **P0 / M** | **(a) Minimal tool-løkke.** Bygg på Explore, Contract og `PurposeBoundActionAuthorizer`; start med én konkret cellehandling. Modellen foreslår typed argumenter; betrodd adapter beregner fakta; kontroll skjer før utførelse. | Løser manglende sammenkobling mellom modellforslag og håndheving. Løser ikke agentens direkte vertstilgang. Ikke bygg fan-out eller generell shell-utførelse først. |
| **P0 / L; sperring S** | **(d) Sandbox for scriptceller.** Bygg på eksisterende host-/adaptergrenser og bruk OS-isolasjon med eksplisitt fil-, nettverks- og prosesspolicy. Hold scriptbanen stengt inntil dette finnes. | Løser direkte script-egress innen definert isolasjon. Løser ikke skade mot uttrykkelig tillatte ressurser eller kompromittert vert. |
| **P0 / M** | **(g) Godkjenning med forståelig effekt.** Bygg på intent, ceiling og eksisterende review-mønster. Bind nødvendig godkjenning til innhold, mottaker, frist og myndighetsendring. | Løser manglende forbindelse mellom «ja» og faktisk handling. Reduserer gjentakelser; kan ikke bevise at brukeren forstod. |
| **P0 / M** | **(h) Injection-isolasjon.** Bygg på gatewayens requesttyper og Explore-kontrakter: separate roller, utrusted tool-data, validerte argumenter og forbud mot at datainnhold endrer policy. | Løser en del instruksjons-/datablanding. Løser ikke semantisk påvirkning av modellen. JSON alene er ingen injection-beskyttelse. |
| **P0 / M** | **(k) «Skal ikke» som deny-regler.** Bygg på A4-invariantene og køforslagets no-self-escalation. Negative skranker må ha prioritet og være utilgjengelige for agentens endringer. | Løser eksplisitte forbud som observerbare handlingsregler. En `prohibited`-etikett i et formålstre løser ingenting alene; ikke påstå generell runtime-støtte for polaritet nå. |
| **P1 / M** | **Betrodde observasjoner.** Bygg på `GoalObservation` og `GoalEvaluationCell`. Knytt kildeidentitet, tidspunkt, hendelses-ID og handling til observasjonen; skill utfører fra kontrollør. | Løser egenrapportert måloppnåelse som eneste bevis. Løser ikke feil sensor eller feildefinert mål. Dette er viktigere enn flere evaluatornavn. |
| **P1 / M** | **(e) Signerte beslutnings- og effektkvitteringer.** Bygg på `ActionDecisionReceipt`, digestprofil og eksisterende identitetssignering. Skill beslutning, sendeforsøk, providerrespons og bekreftet mottak. | Løser autentisitet og presis bevisstyrke i kontrollsporet. Transportkvittering beviser ikke mottakerens videre bruk, sletting eller god effekt. |
| **P1 / M** | **Replayvern og atomisk utførelse.** Bygg på intent-ID, gatewayens kvotereservasjon og HavenAgentDs nonce-mønster. Revalider før effekt; bruk idempotens og behold ukjent status ved timeout. | Løser dobbeltutførelse ved retry og deler av kontroll/utførelse-racet. Kan ikke garantere «exactly once» mot enhver ekstern tjeneste uten dens samarbeid. |
| **P1 / L** | **(f) Distribuert utløp og revokasjon.** Bygg på Contract-gyldighet og policyversjoner. Definer kortlevde fullmakter, ferskhetsgrenser, revokasjonskanal og oppførsel ved nettverksbrudd. | Løser videre bruk etter observerbar tilbakekalling. Øyeblikkelig revokasjon og fortsatt frakoblet tilgjengelighet kan ikke loves samtidig. |
| **P1 / M** | **(c) Autentisert tjeneste-/adapteridentitet.** Bygg på Identity og Contract: bind nøkkel, endepunkt og forventet handlingskontrakt. Full attestasjon av hver celleprosess utsettes til **P2 / L**. | Løser forveksling av tjeneste og uoppdaget identitetsbytte. Beviser ikke at autentisk kode er feilfri; et selvoppgitt cellenavn er utilstrekkelig. |
| **P1 / M** | **(i) Taksonomi-governance.** Bygg på Purpose Knowledge Base og A4s taxonomy-digest. Versjoner betydning, ha navngitt forvalter, endringshistorikk, oppgaveeksempler og migreringskontroll. | Løser stille betydningsendringer og ukontrollert promovering. Løser ikke verdikonflikter eller oppriktigheten i erklært formål. Ukjent formål må ha en brukbar avklaringsvei. |
| **P1 / M** | **(m) Budsjett/kvote med hard reservasjon.** Bygg på eksisterende gatewayreservasjon og Goals for status. Ta med samtidighet, antall effekter, maksimal kjøretid og samlet oppgavekostnad. | Løser overskridelse før neste effekt. Et Goal som oppdager overskridelse etterpå er bare overvåking. Kostnadsgrense beviser ikke verdi eller rimelig pris. |
| **P2 / L, behovsport** | **(b) Per-Grant purpose/action, V2.** Bygg på Agreement-policybinding. Åpne først når smale Agreements faktisk gir et målt problem for blandede scopes. | Løser presisjon innen én flerfunksjonsavtale. Løser ikke bypass, feil taksonomi eller manglende sandbox. Behold den eksisterende beslutningsporten. |
| **P2 / M–L** | **(n) Logg og tilsyn som celleflate.** Bygg på kvitteringer, Goals, review-celler og audit-hendelser. Vis avvik, stopptilstand, ansvarlig operatør og sikker gjenopptakelse. | Løser operatørens innsyn og inngripen i dekkede baner. Gir ikke alene AI Act-etterlevelse eller komplette logger hos tredjepart. |
| **P3 / L** | **(j) Flerpartskontrakter.** Bygg på Agreement/Contract, men spesifiser signaturer, quorum, endring og revokasjon før ny wire-kontrakt. | Løser behov for flere selvstendige godkjennere når et konkret samarbeid krever det. Løser ikke semantisk enighet eller utførelse hos uavhengige parter. |
| **P3 / L** | **(l) Måling av «bidra positivt».** Bygg på Goals og claim/evidence-modellen; gjør avgrensede forsøk med nytte, skade, baseline og etterkontroll. | Løser læring om konkrete virkninger. Løser ikke universell sammenveiing av menneskeverd, miljø og samfunn; bør aldri utstede nye rettigheter. |

Grunnlaget er allerede delvis til stede: gatewayen reserverer kvote før kjøring; HavenAgentD har nonce- og review-mønstre; per-Grant V2 er uttrykkelig utsatt. Køens negative formål står som kandidatkrav, ikke levert håndheving. [belagt: CellScaffold/Sources/App/Cells/AI/AIGatewayCell.swift:819; HavenAgentD/README.md:133; CellProtocolDocuments/Deliverables/Purpose_Bound_External_Action_Contract_2026-08-03/DECISION_LOG.md:35; CellProtocolDocuments/Deliverables/PDD_arbeidsko-ai-utforere_2026-09-07/FORMAALSSPEC.md:42]

**Godkjenningsregelen:** Aldri spør om et hardt forbud kan omgås; avvis og forklar. Aldri gjenta spørsmål om ordinære handlinger innen en allerede godkjent, avgrenset oppgave. Alltid krev menneskelig beslutning ved utvidelse av myndighet, ny sensitiv utlevering utenfor rammen eller en irreversibel effekt som rammen ikke dekker. Forhåndsgodkjente effekter skal følge den vedtatte policyen, ikke utløse ritualer ved hver teknisk operasjon. [vurdering]

**Regelverket:** Artikkel 12 gjelder logging tilpasset høyrisikosystemets risiko og sporbarhetsbehov; «hele handlingskjeden» er briefens forenkling. Artikkel 14 gjelder effektivt menneskelig tilsyn, forståelse av begrensninger, risiko for overdreven tillit og mulighet for inngripen. En tilsynscelle kan støtte dette, men er ikke en samsvarserklæring. [Artikkel 12](https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-12), [artikkel 14](https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-14).

Kommisjonens tidslinje bekrefter transparensregler fra august 2026 og 2. desember 2027 for bestemte høyrisikoområder, men angir 2. august 2028 for systemer integrert i regulerte produkter. Briefens ene høyrisikodato er derfor ufullstendig. Konkret produktklassifikasjon og eventuell norsk gjennomføring er ikke vurdert her. [Kommisjonens AI Act-tidslinje](https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai).

## Q8. Hvilke offentlige påstander tåler kontroll?

Tre trygge formuleringer, med nødvendig avgrensning:

1. **«HAVEN har implementert en avgrenset gatewaybane som kontrollerer eksplisitt formål, eksisterende cellemyndighet og bundne handlingsfakta før én forespørsel sendes til en godkjent AI-leverandør.»** Koden og målrettede tester støtter dette; det er ingen påstand om produksjonsverifikasjon i dag. [belagt: CellScaffold/Sources/App/Cells/AI/AIGatewayCell.swift:730; CellProtocol/Tests/CellBaseTests/PurposeBoundExternalActionTests.swift:8]
2. **«HAVEN skiller erklært formål fra rettigheter: formålet kan innsnevre en tillatelse, men kan ikke opprette den.»** For runtimepåstander må den dokumenterte håndhevingsbanen navngis. [belagt: CellProtocol/Sources/CellBase/Agreement/PurposeBoundExternalAction.swift:694]
3. **«HAVEN kan evaluere uttrykkelige mål deterministisk mot innsendte observasjoner og returnere strukturert beslutningsinformasjon for den formålsbundne gatewaybanen.»** Dette lover verken sanne observasjoner eller signerte effektbevis. [belagt: CellProtocol/Sources/CellBase/PurposeAndInterest/GoalEvaluationEngine.swift:68; CellProtocol/Sources/CellBase/Agreement/PurposeBoundExternalAction.swift:516]

Tre overclaims som bør avvises:

1. **«HAVEN hindrer prompt injection og garanterer at agenter bare handler i brukerens interesse.»** Semantisk laundering og udekkede effektveier gjenstår. [vurdering]
2. **«Alle AI-handlinger har signerte kvitteringer som beviser samtykke og utførelse.»** Dagens A4-kvitteringsformat, dekning og godkjenningskjede støtter ikke dette. [belagt: CellProtocol/Sources/CellBase/Agreement/PurposeBoundExternalAction.swift:516] [vurdering]
3. **«Formålsceller sikrer positivt samfunnsbidrag og gjør løsningen AI Act-kompatibel.»** Verken samfunnseffekt eller regulatorisk samsvar følger av kontrollmodellen. [belagt: CellProtocolDocuments/Deliverables/Purpose_Bound_External_Action_Contract_2026-08-03/DECISION_LOG.md:94] [vurdering]

## Q9. Den sterkeste innvendingen, og hva som kan motbevise den

**Den sterkeste innvendingen er at formålslaget ikke gir beslutningsrelevant sikkerhetsgevinst utover vanlig minst-privilegium, men gjør systemet vanskeligere å forstå og revidere.** Hvis de virkelige sperrene alltid er mottaker, ressurs, handling og kvote, mens formål bare er en korrekt stavet etikett agenten velger, kan HAVEN ende med kostbar hensiktsdokumentasjon og større falsk trygghet. Da bør prosjektet snu mot enklere autorisasjon og bruke formål som forklaring. [vurdering]

Tre andre innvendinger står uavhengig av dette: Egen policy- og kryptografiintegrasjon øker vedlikeholds- og feilflaten; exact match og mange avtaler kan gjøre legitime oppgaver unødvendig skjøre; taksonomiforvalteren kan i praksis overta styringen som angivelig skulle ligge hos brukeren. Dette er reelle kostnader, ikke argumenter for å fjerne alle sikkerhetsgrenser. [vurdering]

Jeg ville la én smal arbeidsflyt konkurrere mot en kompetent baseline: samme modell, sandbox, verktøy og minste rettigheter. Sammenlign tre varianter: eksisterende policy, samme policy med formålstekst, og full HAVEN-binding med kontrollerbar utførelse. Oppgavene må inkludere legitim ombestemmelse, nye mottakere, injiserte meldinger, feil formålsmerking, policyendring, retry, utløp og forsøk på alternative utganger. En uavhengig observatør må telle de faktiske effektene. [vurdering]

Fastsett kriteriene før forsøket: ingen uautoriserte effekter i angrepssettet, minst like god legitim oppgaveløsning som baseline, færre unødige godkjenninger og forståelig forklaring av avslag. Registrer også oppsettid, operatørinngrep og feil ved endringer. Et endelig antall vellykkede tester er evidens for denne piloten, aldri et universelt sikkerhetsbevis. [vurdering]

Det som ville overbevise meg, er at vanlige brukere gjennomfører arbeidsflyten uten ekspertbistand, samtidig som HAVEN stopper dokumenterte angrep eller misforståelser baseline slipper gjennom. Rådgiverpanelet er foreløpig ikke en slik demonstrasjon: statusfilen oppgir uferdig gjennomføring og blokkerte live avhengigheter. [belagt: CellScaffold/Deliverables/PDD_radgiverpanel-og-persona_2026-09-05/STATUS.md:5] [vurdering]

Rekursive støtteformål som «miljøet må være stabilt nok» må dessuten aldri utvide agentens handlingsrom. Ellers gjeninnføres nettopp den selvautorisasjonen A4 forsøker å fjerne. Behold verdiforankringen, men bind hver effekt til en konkret fullmakt. Min anbefaling til Kjetil er derfor en pilot med tydelig stoppkriterium før bred plattformutvidelse. [vurdering]

**Sluttstatus:** F1–F6 er behandlet og Q1–Q9 besvart. Påstanden om en ny sikkerhetsklasse forkastes i sterk form; avgrenset runtimekontroll er belagt; generell agentdekning, selvbetjent brukbarhet og merverdi mot baseline er åpne spørsmål for Kjetils pilotbeslutning. Ingen kode er endret, og denne vurderingen er eneste leveranse.

<!-- ASTRA RUNDE 1 FERDIG -->
