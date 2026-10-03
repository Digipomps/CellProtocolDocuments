# Formål og Celler som styring av AI-agenter — vurdering mot leverandørenes begrensninger

Dato: 2026-09-08 · Forfatter: Losen (Claude), i diskusjon med Astra (gpt-6-astra via Codex) · Bestiller: Kjetil
Mappe: `CellProtocolDocuments/Deliverables/Formaal_Celler_Agentstyring_Vurdering_2026-09-08/`
Type: **analyse og beslutningsgrunnlag**, ikke implementering. Filer: `BRIEF.md` (formål, faktagrunnlag, spørsmål), `ASTRA_SVAR_KO.md` (Astra runde 1; `ASTRA_SVAR.md` er den avbrutte MCP-kjøringen, bare Q1), `RUNDE2_LOSEN.md` (mine motsvar), `ASTRA_SVAR_RUNDE2.md` (Astra runde 2), denne filen (samlet vurdering), `STATUS.md` (arbeidsmetode, hva som virket / ikke virket).

## 0. Formålet — og hvordan dokumentet måles mot det

Bestillingen (ordrett): *«Vurder hvor godt formål og Celler er for å styre og begrense AI agenter i forhold til de begrensningene AI selskapene bruker. Diskuter dette med Astra - og vurder hvor bra dette kan fungere i sin nåværende form og om det eventuelt er mer funksjonalitet vi bør legge til.»*

| ID | Delformål | Besvares i |
|---|---|---|
| F1 | Sammenligne det som er *implementert* i HAVEN i dag mot leverandørenes mekanismer slik de er i dag — ikke visjon mot visjon | §2, §3 |
| F2 | Finne hva som er *kategorisk* annerledes, og hva som er kjent teknikk med nytt navn | §3, §6 |
| F3 | Robusthet mot kjente angrep | §4 |
| F4 | Hvor bra fungerer det i nåværende form — dekning, håndheving, bevis, brukbarhet | §5 |
| F5 | Funksjonalitet som bør legges til, prioritert | §7 |
| F6 | Reelle motargumenter og den sterkeste innvendingen | §6, §9 |
| — | Diskusjonen med Astra: enighet, uenighet, hva som endret seg | §6 |
| — | Claim safety: hva vi kan si offentlig | §8 |

Merking: `[belagt: fil]` = observert i repoet 2026-09-08; `[vurdering]` = min eller Astras vurdering; `[Astra]` = punkt Astra reiste; `[usikker]` = ikke verifisert.

## 1. Kort svar

Formål og Celler er ikke en erstatning for leverandørenes begrensninger, men et **tredje lag** som leverandørene ikke har og ikke kan levere: en begrensning som *eies av dataeieren*, håndheves *ved dataene* (cellen) i stedet for i modellen, er *lik uansett leverandør*, og gir en strukturert beslutningspost per handling. Leverandørenes lag svarer på «hva får denne modellen gjøre for hvem som helst» (trening, klassifikatorer, Model Spec) og «hva får denne agenten gjøre i denne installasjonen» (permission modes, hooks, sandbox). HAVENs lag svarer på «hva får *denne handlingen* gjøre med *disse dataene* mot *denne destinasjonen* for *dette erklærte formålet* under *denne kontrakten* mellom *disse identitetene*». Det er en reell forskjell i *eierskap og plassering*, ikke i teknikk: mekanismene er kapabilitetsbasert tilgangskontroll med innsnevring (Macaroons/Biscuit/UCAN-familien), formålsbinding (GDPR-prinsippet gjort maskinsjekkbart) og attestasjon.

I nåværende form fungerer det **godt på én bane og ikke i det hele tatt på resten**. A4-v1 håndhever hele A1-regelsettet på `PurposeBoundAIGateway.ai.invokePurposeBound` `[belagt: AIGatewayPurposePolicy.swift]`, med fail-closed ved ukjent formål, exact match, ceiling-ikke-grant, owner-no-bypass og digest-binding. Men det finnes **ingen tool-løkke fra modell til celler** `[belagt: AIGatewayCell.swift, ingen tool_calls/tool_use i provider-adapterne]`; modellen er tekst inn / tekst ut. Dermed styrer formål og celler i dag *hva som sendes ut* (til leverandør) og *hva en ekstern agent får gjøre inn* (correspondence-MCP) — ikke hva en agent *gjør*. Det interessante handlingsrommet (Claude Code, Codex på Mac-en, HavenAgentD) ligger utenfor cellene og styres i dag av leverandørenes egne gates. Beslutningskvitteringen på A4-banen er dessuten **ikke signert** `[belagt: PurposeBoundExternalAction.swift:516, ingen signaturfelt; Astra]` — så «bevisbar» gjelder kontrollert scope, ikke autentisert beslutningsopphav. Og i correspondence — den ene banen der eksterne agenter faktisk *handler* inn i HAVEN — er «eksplisitt ja per melding» en regel Losen følger, **ikke** noe cellen håndhever: `correspondence_send_message` sender så snart relasjonen er aktiv, og `purposeRef` er en fri streng agenten setter selv `[belagt: CorrespondenceMCPService.swift:97–112, CorrespondenceClient.swift:382–412; Astra]`.

Konklusjon: tilnærmingen er riktig og *nødvendig* (leverandørene kan ikke levere ressurseierstyrt, datanær og leverandøruavhengig begrensning), men verdien står og faller med at **agentens foreslåtte handlinger går gjennom Contract + formål + ceiling før utførelse**, og med at dette blir *mindre* friksjon enn leverandørenes godkjenningsdialoger — ikke mer. Uten det er «formål styrer AI-agenter» en påstand om én provider-bane. Astra og jeg landet på samme anbefaling: **én pilot på correspondence send**, med en godkjenningsport hos avsenderen, målt mot en kompetent baseline med et snu-kriterium fastsatt på forhånd (§6.2, §10). §7 gir den prioriterte listen over funksjonalitet.

## 2. Faktagrunnlag

Fullt faktagrunnlag med filstier står i `BRIEF.md` §2 (tolv punkter). De bærende faktaene for vurderingen:

| # | Faktum | Status |
|---|---|---|
| a | Purpose er erklært, aldri utledet, og gir ingen myndighet i seg selv; kan være *betingelse* i Contracts | `[belagt: Book/09]` |
| b | Goals finnes som deterministiske predikater (state/event/location/time/network/contract-probe/gui-smoke/composite) med sideeffektfri motor og live celle | `[belagt: GoalDefinition.swift, GoalEvaluationEngine.swift, GoalEvaluationCell.swift]` |
| c | Autorisasjon er eksplisitt og kapabilitetsbasert: Agreement ≠ Contract; `rwxs`; storage ≠ disclosure; conditions; issuer-signert subject-bundet snapshot; TrustedIssuers-kvitteringer | `[belagt: Book/04]` |
| d | A1-regelsettet (formål innsnevrer, aldri utvider; exact match; facets ikke autoriserende; unknown fail-closed; config er ceiling; owner no bypass; alle digests bindes) er håndhevet på nøyaktig én bane | `[belagt: Purpose_Bound_External_Action_Contract_2026-08-03/, AIGatewayPurposePolicy.swift]` |
| e | Tool-policy i AIGateway: `denyAll` default; `denied` feiler lukket; *tillatte* verktøy håndheves som systemprompt-setning; ingen tool-løkke fra modell til celler | `[belagt: AIGatewayCell.swift ~2010/2104, AIGatewayModels.swift 69–135]` |
| f | `ActionDecisionReceipt` har bindinger, sjekker, decision-/executionStatus — men ingen signatur | `[belagt: PurposeBoundExternalAction.swift:516–545]` |
| g | Rådgiverpanel-celle besluttet, ikke levert; arbeidskø for AI-utførere er kandidat; celle-utfører får bare tekst inn/ut; ingen vilkårlig shell; ingen selv-eskalering | `[belagt: PDD_radgiverpanel…/STATUS.md, PDD_arbeidsko…/FORMAALSSPEC.md]` |
| h | Eksterne agenter (Losen, Lille Robot) handler inn i HAVEN via correspondence-MCP med avgrensede rettigheter (fire verktøy: list, read, send, ack); «sending krever eksplisitt ja» er Losens regel, ikke cellens — se j | `[belagt: CorrespondenceMCPService.swift; Book/33]` |
| i | Kallimachos-formålstre, Goals som prompts + uttrykk, distribuert fusjon, «bidra positivt» målbart, celle-autentisitet: visjon/under vurdering | ikke implementert |
| j | Correspondence-MCP: `send_message` krever aktiv relasjon og medlemskap, krypterer og kaller cellen — ingen payload-bundet godkjenning per melding; `purposeRef` er fri streng med default | `[belagt: CorrespondenceMCPService.swift:97, CorrespondenceClient.swift:382; Astra]` |
| k | Goal-verdipredikater dekker likhet/ulikhet/tekstinnhold, ikke generell numerisk/temporal logikk; `confidence` er 0,8 som default når observasjoner finnes, ikke et sannsynlighetsbevis | `[belagt: GoalEvaluationEngine.swift:252, :275; Astra]` |

Referanserammen (leverandørene, sept. 2026) står i `BRIEF.md` §3. Astra påpekte at septemberfaktaene (Model Spec 2026-08-18, «93 % godkjenning», EU-datoene) ikke er nettverifisert fra Codex-siden; jeg hentet dem fra åpne kilder 2026-09-08 (Model Spec-siden, bransjeoversikt, AI Act-oversikt) og de brukes som *mekanismebeskrivelse*, ikke som produktgaranti. `[usikker: eksakte tall]`

## 3. Sammenligning per dimensjon

| D | Dimensjon | Leverandørene | HAVEN i dag | Vurdering |
|---|---|---|---|---|
| D1 | Hvem eier begrensningen | Leverandør (trening, klassifikatorer, Model Spec) → deployer (permission modes, hooks) | Eier av entitet/celle; motpart via Contract | **Reell forskjell i eierskap** — *ressurseierstyrt autorisasjon med håndheving ved ressursen* (Astras navn; forgjengere UMA 2.0, Solid WAC). Leverandøren kan ikke gi datasubjektet eierskap til begrensningen; HAVEN kan ikke gi leverandørens. De må leve sammen. Forutsetter at eierens nøkler og håndheving ligger utenfor operatørens kontroll. |
| D2 | Hvor den håndheves | Vekter → prompt → tool-gate → OS-sandbox | Resolver/Cell-grense + policy ceiling (én bane); ellers prompt | **Lik teknikk, ulik plassering.** Leverandørens tool-gate står ved *agenten*; HAVENs står ved *dataene*. Det er poenget: en celle nekter selv om agenten er kompromittert. Men i dag dekker den bare egress. |
| D3 | Hva som er bevis | Logg (og audit-hooks) | `ActionDecisionReceipt` med digests og sjekkresultater — usignert; signerte Contracts og TrustedIssuer-kvitteringer for autorisasjonen | **Overdrevet i briefen** `[Astra]`. HAVEN har *strukturert* bevis for scope, ikke autentisert bevis for beslutningen. Lett å rette (P1). |
| D4 | Granularitet | Global / per app / per verktøy (+ path-mønstre i hooks) | Keypath × formål × destinasjon × dataklasse × payload-digest | HAVEN er finere *på aksene den har*. Dataklassene er grove (`user-prompt`, `system-instruction`) — den ser ikke persondata *inne i* teksten `[Astra]`. |
| D5 | Komposisjon over flere aktører | Ingen delt intensjon mellom parter; hver deployer har sin policy | Agreement/Contract mellom identiteter; correspondence; samme vokabular hos begge | **Reelt i praksis**, ikke historisk nytt: to parter kan sammenligne formål mot tilbud mot faktisk handling med samme vokabular. Bilateral signering finnes ikke ennå. |
| D6 | Robusthet mot injection/laundering/confused deputy | Prompt-avhengig, unntatt tool-gate og sandbox | Modelloutput er *proposal*; policy leser validerte wire-felt (én bane) | Strukturelt sterkt der det gjelder; se §4. |
| D7 | Kostnad | Tokens + menneskelige godkjenninger (approval fatigue) | Predikater er nesten gratis; taksonomi + Agreements koster oppsett | HAVENs *potensielle* fordel: predikater kan auto-godkjenne det leverandøren må spørre om. Ikke realisert. |
| D8 | Ved ukjent | Spør, eller fail open i praksis | Fail closed (`purpose://prompt.unknown`) | HAVEN er strengere. Strengt uten god fallback = friksjon. |
| D9 | Dekning i dag | Hele agentens handlingsrom (verktøy, filer, nett) | Én provider-bane + MCP-inngang; ingen tool-løkke | **Leverandørene vinner klart i dag.** |

Det som skiller HAVEN er D1 og D5 (eierskap og delt intensjon) og delvis D2 (plassering ved dataene) — en arkitekturretning leverandørenes lokale gates ikke realiserer alene, men som eksisterende autorisasjonsinfrastruktur (UMA, Solid) også kan realisere. D3, D4, D6 og D8 er kjent teknikk anvendt konsekvent. D7 er en fordel som ennå ikke er hentet ut. D9 er hullet.

## 4. Robusthet — angrep for angrep

Vurderingen gjelder A4-banen (`ai.invokePurposeBound`) der den er håndhevet, og «utenfor» for resten. «Strukturelt» = løses uten at modellen må oppføre seg.

| Angrep | På A4-banen | Utenfor A4-banen | Kommentar |
|---|---|---|---|
| T1 Purpose laundering («hjelp brukeren» som dør til disclosure) | Strukturelt: exact match, ett formål per effekt, destinasjon/data-ceiling | Ikke løst | Avhenger av taksonomi-governance: hvem bestemmer hva `purpose://ai.assistance.answer-user-prompt` dekker? |
| T2 Prompt injection | Strukturelt *for autorisasjon*: modelloutput gir aldri myndighet; policy leser wire-felt. **Ikke** løst for *innhold*: en injisert instruks kan få modellen til å legge feil data i den tillatte prompten til den tillatte destinasjonen | Bare i prompt (Model Spec «tool output untrusted») + leverandørens klassifikatorer | Ceiling begrenser *skaden*, fjerner ikke feilen. Injection-isolasjon i wire-format (P0) mangler. |
| T3 Parent escalation | Strukturelt | — | |
| T4 Facet escalation | Strukturelt | — | |
| T5 Confused deputy | Strukturelt: egen celle, ett Grant, owner-no-bypass | Ikke løst: HavenAgentD, scriptceller, Codex på Mac-en har brede rettigheter | Dette er hovedhullet. |
| T6 Direkte script-egress | Ikke implementert (sandbox mangler) | Leverandørens sandbox (Seatbelt/bubblewrap) gjør jobben *for* oss i dag | HAVEN bør *forutsette* OS-sandbox, ikke bygge egen. |
| T7/T8 Config-/payload-substitusjon | Strukturelt (digests) | — | Krever kanonisering + signering for å være bevis, ikke bare kontroll. |
| T9 Storage → disclosure | Strukturelt (`s` ≠ disclosure) | Ikke løst nedstrøms (logger, backups) | |
| T10 Trust theater | Strukturelt (trust package non-authorizing) | — | |
| T11 Stale evidence | Delvis: utløpt evidens avvises, men gatewayen tar evidensstatus fra *requesten*; `current` er en etikett, ikke en ferskhetskontroll; `trustPackageEvidence` kan være `notRequired` `[belagt: AIGatewayCell.swift:1089; Astra]` | Revokasjonsdistribusjon mangler | |
| T12 Owner bypass | Strukturelt (negativt testet) | Ikke løst i andre adaptere | |
| T13 Receipt overclaim | Strukturelt (decision ≠ execution) | Effect-receipt med transportbevis mangler | |
| T14 Audit-log leakage | Delvis (bare digests i receipt) | Logger/telemetri utestet | |
| T15 Doc-to-runtime gap | Håndtert med claim ledger | Risiko: «HAVEN styrer agenter» sies om én bane | Se §8. |
| Tool hijacking via MCP | Ikke relevant (ingen tool-løkke) | Correspondence-MCP: rettigheter avgrenset per verktøy; «sending krever ja» håndheves hos Losen, ikke i cellen (§2 j); `purposeRef` kan settes av injisert tekst | Når tool-løkke kommer, må hvert verktøy være en celle-action under Contract, og formålet komme fra profil, ikke fra agent. |
| Approval fatigue | Ikke adressert. `requires_human_approval` uten «aldri spør / alltid spør»-design vil gi det samme som leverandørene | — | HAVENs mulige fortrinn (predikater auto-godkjenner) er ikke tatt ut. |

Ett angrep briefen ikke hadde med, og som gjelder *alle* Goal-baserte kontroller: **egenrapporterte observasjoner**. `GoalEvaluationCell` evaluerer det som sendes inn. Hvis samme agent både utfører oppgaven og sender inn `human-confirmation`-hendelsen, får vi deterministisk godkjenning av en løgn `[Astra; belagt: GoalEvaluationCell.swift:6]`. Observasjonskilden er en sikkerhetsgrense og må ha autentisert produsent, ferskhet og binding til handlingen — det er viktigere enn flere evaluator-typer.

Det som er *avhengig av at modellen oppfører seg* på A4-banen: at prompten den foreslår er riktig og minimert (innhold), og at modellen ikke «later som» den brukte verktøy (tool-policy for tillatte verktøy er en setning i systemprompten). Alt annet på banen er strukturelt.

## 5. Hvor godt fungerer det i nåværende form

| Område | Vurdering | Begrunnelse |
|---|---|---|
| Håndheving der den finnes | **Sterk** | A1-låsene er implementert og negativt testet på A4-banen; fail-closed; owner-no-bypass `[belagt]` |
| Dekning | **Svak** | Én bane. Ingen tool-løkke. Legacy `ai.invoke`, HavenAgentD, scriptceller, arbeidskø utenfor. Rådgiverpanel ikke levert. Ingen live modellkjøring mulig nå (kreditt) `[belagt: PDD_radgiverpanel STATUS]` |
| Bevis | **Middels** | Signerte Contracts og TrustedIssuer-kvitteringer for *autorisasjon*; usignert `ActionDecisionReceipt` for *beslutning*; ingen effect-receipt for *utførelse* |
| Goals som styring | **Riktig grunnlag, ikke koblet** | Motoren finnes og er testet; den evaluerer bare innsendte observasjoner; ikke koblet til AIGateway, kvoter, correspondence eller GUI `[belagt: Purpose_Goal_Evaluation_Analysis]` |
| Brukbarhet uten Kjetil/Claude/Codex i løkka | **Ikke i dag** | A4-profilen er kompilert Swift-policy, ikke konfigurasjon en celleeier setter selv `[Astra]`; Agreement Workbench finnes, men formålsbinding krever kode |
| Leverandøruavhengighet | **God, med ett hull** | Samme policy for openai/anthropic/mistral. A4-banen utelukker lokale modeller `[belagt: AIGatewayCell.swift:2830; Astra]`; lokal modell går bare via legacy-banen uten formålsbinding |

Samlet: **fungerer som *bevis på konsept* og som *egress-kontroll*; fungerer ikke ennå som *agentstyring***. Det er ikke en svakhet ved ideen, men ved dekningen.

## 6. Diskusjonen med Astra

Astra (gpt-6-astra) fikk `BRIEF.md` med formål, faktagrunnlag, referanseramme og ni spørsmål, og svarte i `ASTRA_SVAR_KO.md` (runde 1, 3 900 ord, filbelagt med linjenumre). Jeg svarte med fem motsvar i `RUNDE2_LOSEN.md`; Astras runde 2 står i `ASTRA_SVAR_RUNDE2.md`.

### 6.1 Runde 1 — hva Astra rettet, og hva vi er enige om

Astra reviderte briefen på fire punkter, alle verifisert av meg i koden etterpå, og alle tatt inn over:

| Briefen sa | Astra viste | Konsekvens |
|---|---|---|
| D3: «signert kvittering bundet til intent-digests» | `ActionDecisionReceipt` har ingen signatur; gatewayen setter status uten signering | «Bevisbar» = kontrollert scope, ikke autentisert beslutning. P1-tiltak, lite. |
| «Goals som matematiske uttrykk» | Verdipredikat = likhet/ulikhet/tekst; ingen numerikk/temporal logikk; confidence 0,8 default | Visjonen om «uttrykk billigere enn tokens» er riktig i prinsipp, men motoren må utvides før den bærer budsjett/tid |
| Correspondence: «sending krever eksplisitt ja» | Ingen payload-bundet godkjenning i kjeden; `purposeRef` er fri streng | Regelen bor i Losen, ikke i cellen. Må inn i cellen før piloten kan kalles «HAVEN-styrt» |
| Leverandørsiden for kategorisk («bare logg», «ofte fail open») | Deployer-gates er også kontekstuelle og konfigurerbare | Tatt inn i §3-tabellen |

Enighet: A1/A4 er reell håndheving på én bane; formål gir ikke myndighet; tool-policy for tillatte verktøy er prompt; OS-sandbox skal *forutsettes*, ikke bygges i Swift; «agenten foreslår, cellene bestemmer» er sant bare der cellen er en uomgjengelig grense; observasjonskilden er en sikkerhetsgrense; approval fatigue løses ikke av flere detaljer; ingen offentlig påstand om generell agentstyring er belagt.

### 6.2 Runde 2 — uenighetene, og hvor de landet

| Mitt motsvar | Astras svar | Hvor det landet |
|---|---|---|
| **M1 «Ny klasse», innsnevret:** dataeieren kan begrense en agent *noen andre* kjører, uten å stole på operatøren | Ja til *en selvstendig tillitsgrense hos ressurseieren*; nei til «historisk ny» og nei til «uten å stole på operatøren» ubetinget. Forgjengere: UMA 2.0 (ressurseierstyrt autorisasjon på tvers av domener), Solid WAC. Navn: **ressurseierstyrt autorisasjon med håndheving ved ressursen**. Forutsetter at gjestens håndhevingsmiljø og nøkler faktisk er utenfor Palazzos kontroll; datasubjekt, ressurseier og autorisasjonsutsteder er tre roller, og arkitekturen må gi gjesten den siste. Grensen går ved utlevering: mottatt klartekst kan kopieres `[belagt: Book/04:86]`; «bevise etterpå at den holdt seg innenfor» er for sterkt. | **Enige om den innsnevrede påstanden med Astras navn og forbehold.** Det er dette HAVEN skal si det er. Over scaffold-grenser må én bane dokumentere autentisert requester + mottaker, ressursbinding, fersk autorisasjon, replayvern og lik effektkontroll hos utføreren `[usikker]`. |
| **M2 Formål er nøkkel, ikke etikett** (fast i A4; i tool-løkke valgt av eier eller action→purpose-tabell) | «Du har rett om dagens A4» — etikettkritikken traff en mulig fremtidig utforming. Men: velger modellen *action*, velger den indirekte tabellrad; oppdraget må på forhånd begrense hvilke actions/profiler modellen kan foreslå. Formål gir sikkerhetsgevinst bare når det tilfører *uavhengig godkjent oppgavekontekst* (samme mottaker+operasjon tillatt i ett oppdrag, avslått i et annet); er det en entydig omskriving av action, tilfører det ingenting til beslutningen. `ownerConfirmed` er en standardverdi i konstruktøren, ikke et godkjenningsbevis `[belagt: AIGatewayPurposePolicy.swift:139]`. | **Astra ga seg på A4, jeg gir meg på gevinsten:** formålet forsvarer kostnaden sin gjennom *oppgavekontekst på tvers av celler*, forklarbarhet og sammenligning mellom parter — ikke som egen sikkerhetsprimitiv. Piloten må vise færre forståelses-/konfigurasjonsfeil, ellers er formål forklaring. |
| **M3 Godkjenning uten tretthet — konkret** | Rammen = versjonert **oppgaveprofil** (utsteder, utfører, målressurser, tillatte actions, primærformål, databegrensninger, mottakere, budsjett/effektantall, gyldighet, tilbakekalling); eierens ja bindes til profilens digest; hver effekt må tilfredsstille både Contract og profilens ceiling. Betrodde produsenter i dag: Resolver/Cell (adgang ved operasjonen), EntityAnchor commit-banen (denne lagringen), gatewayens kvotereservasjon (betinget av `prepaidDimy`) — ingen av dem blir automatisk Goal-observasjoner. Metrikk fra dag én: **overflødige godkjenningsdialoger per fullført legitimt oppdrag**, mål null. | **Tatt inn i §7 som P0 «ramme-objekt» og P1 «betrodde observasjoner».** Numeriske budsjettsperrer må ligge i utføreren, ikke i dagens Goal-predikater. |
| **M4 Correspondence — minste endring for ja per melding** | Behold formatet; legg en **uomgjengelig godkjenningsport hos avsenderen**: porten fryser innhold + hele send-forespørselen; betrodd visning viser samme klartekst/mottakere/formål/lagringstid; eierens *separate* godkjenningsnøkkel signerer en kanonisk post (innholdsdigest, forespørselsdigest, celle, relasjon/medlemsfingeravtrykk, avsender, profilversjon, engangs-ID, kort gyldighet); porten verifiserer, gjentar adgangssjekker, reserverer engangs-ID atomisk før sending; agenten får aldri nøkkelen. Fjerncellen kan ikke verifisere dette uten ny bevisutveksling `[usikker]`. Lesing og kvittering innenfor godkjent relasjon kan gå automatisk — men `ackMessage` betyr ikke «lest av menneske». | **Tatt inn som P1 med konkret design.** Dagens indre signatur beviser avsender, ikke «eieren har sett og godkjent» `[belagt: CorrespondenceEnvelope.swift:95/132, CorrespondenceCell.swift:318]`. Ny meldings-ID per godtatt kall → ukjent utfall etter timeout må undersøkes før nytt forsøk `[belagt: CorrespondenceCell.swift:356]`. |
| **M5 Pilot** | **(ii) correspondence send.** Minste løkke: testmelding → modellens strukturerte utkast (JSON-tekst er nok; ingen native tool-calling) → betrodd validering + profilvalg → konkret ja → én sending → kontroll av mottakercellens lagrede konvolutt. Nødvendig P0: beskyttet policy/nøkler; én sendebane gjennom M4-porten; mottaker-/payloadkontroll; utrusted innhold adskilt fra kontrollfelt; avslag ved ukjent profil/utvidelse; varig engangsreservasjon; håndtering av ukjent sendeutfall. *Ikke* nødvendig: generell sandbox, per-Grant V2, celleattestasjon, distribuert revokasjon. 20 legitime + 20 adversarielle tilfeller, tre varianter. Krav: null uautoriserte/doble effekter; ≥ 18/20 legitime og ikke færre enn baseline; null overflødige dialoger. **Snu-kriterium:** etter høyst to forbedringsrunder gir full binding verken færre policy-/forståelsesfeil eller færre avbrudd, og operatørtid > baseline + 20 %. Lokal modell kan lage utkast og injeksjonsforsøk, men dokumenterer ikke A4-providerbanen (som utelukker lokale modeller `[belagt: AIGatewayCell.swift:2830]`). | **Enig. Dette er anbefalingen i §10.** Piloten treffer også Vegar/Victoria-piloten direkte. |

Astra endret fra runde 1: vektlegger ressurseierens uavhengige håndhevingsgrense sterkere; korrigerer etikettkritikken for dagens A4; **nedprioriterer en ny gateway-integrert tool-løkke** (piloten kan bruke correspondence-kjeden med godkjenningsport). Fastholder: formål er ikke en ny sikkerhetsprimitiv; etterfølgende databruk er ikke kontrollert; formålslagets praktiske merverdi er et åpent spørsmål piloten må avgjøre.

Jeg endret: «bevisbar» → «strukturert, usignert» inntil P1; «sending krever ja» → regel hos Losen, ikke i cellen; tool-løkke gjennom AIGateway er P0 for en *generell* effektbane, men ikke for piloten; formålets forsvar er oppgavekontekst + forklarbarhet + sammenligning, ikke sikkerhet i seg selv.

## 7. Funksjonalitet som bør legges til — prioritert

Sammenslått fra min liste og Astras Q7. P0 = må finnes før en effektbane åpnes for en agent; P1 = før begrenset ordinær drift; P2 = ved dokumentert behov; P3 = forskning. S/M/L er relativ størrelse, ikke tid. «Bygger på» peker på det som allerede finnes i CellProtocol/CellScaffold.

| Pri | Tiltak | Løser | Løser ikke | Størrelse | Bygger på |
|---|---|---|---|---|---|
| **P0** (for en generell effektbane; *ikke* for piloten) | **Tool-løkke gjennom celler.** Modellen foreslår *typede argumenter* (JSON-tekst er nok) til én celle-action; betrodd adapter beregner intent-fakta; `PurposeBoundActionAuthorizer` sjekker Contract + ceiling + formål + digests *før* utførelse; kvittering etterpå. Én action, ikke fan-out, ikke shell. Formålet velges **aldri** av modellen: eier-bekreftet i oppgaveprofil eller avledet av action→purpose-tabell — og oppdraget må på forhånd begrense hvilke actions modellen kan foreslå (Astra M2). | Koblingen modellforslag → håndheving; gjør «formål styrer agenter» sann for den ene banen | Agentens direkte vertstilgang (Claude Code/Codex/HavenAgentD) | M | Explore, Contract, `PurposeBoundExternalAction.swift`, A4-profilen. Piloten (M5) klarer seg med correspondence-kjeden + M4-porten |
| **P0** | **Dekningskontrakt.** Kartlegg alle effektveier per utfører (legacy `ai.invoke`, credentials, policyfiler, scriptceller, MCP-servere) og sperr eller dokumenter hver. | Omgåelse av den valgte grensen; T15 | Dårlige handlinger innenfor tillatt scope | M | Resolver, A4, `PDD_arbeidsko` no-arbitrary-shell |
| **P0** | **Injection-isolasjon i wire-format.** Separate roller/felter for system, bruker, verktøydata; policy leser aldri modelltekst for myndighet (allerede normen — gjør det testbart); `purposeRef` i correspondence slutter å være fri streng fra agenten. | Instruksjons-/datablanding; T2 for myndighet | Semantisk påvirkning av modellens *innhold* | M | `AIGatewayInvokeRequest`, Explore-kontrakter, correspondence-kontrakten |
| **P0** | **Godkjenning bundet til effekt («ramme»-objekt).** Signert oppgaveprofil = ceiling + budsjett + gyldighet + mottakere. Aldri spør om harde forbud (avvis); aldri gjenta innenfor godkjent ramme; alltid spør ved myndighetsutvidelse, ny sensitiv utlevering, irreversibel effekt utenfor rammen. Logg godkjenningsrate fra dag én. | Approval fatigue; «ja» som ikke er bundet til handling | Kan ikke bevise at brukeren forstod | M | Intent, ceiling, Agreement Workbench, HavenAgentD review-mønster |
| **P0** | **«Skal ikke» som deny-regler med forrang**, utilgjengelige for agentens endringer. En `prohibited`-etikett i formålstreet gjør ingenting alene. | Eksplisitte forbud som observerbare regler | — | S | A4-invariantene, `no-self-escalation` |
| **P0** | **Sandbox for script-/utfører-baner** — bruk OS-isolasjon (Seatbelt/bubblewrap) med eksplisitt fil-, nett- og prosesspolicy; hold banen stengt til den finnes. | T6 | Skade mot uttrykkelig tillatte ressurser | L (sperring: S) | Codex/Claude Code-sandbox som forbilde; `PDD_arbeidsko` |
| **P0 for piloten** | **Correspondence: godkjenningsport hos avsender** (M4-design): frys innhold + forespørsel, betrodd visning, eierens separate godkjenningsnøkkel signerer kanonisk post, porten verifiserer + reserverer engangs-ID før sending; agenten får aldri nøkkelen; `purposeRef` fra profil, ikke fra agent. | Regelen «ja per melding» flyttes fra Losen til koden; replay; payload-bytte etter ja | Fjerncellens verifikasjon av menneskets ja (krever ny bevisutveksling) | S–M | `CorrespondenceEnvelope`, `CorrespondenceClient.sendMessage`, Contract |
| **P1** | **Betrodde observasjoner.** `GoalObservation` får kildeidentitet, tidspunkt, hendelses-ID og handlingsbinding; utfører ≠ kontrollør. | Egenrapportert måloppnåelse | Feil sensor, feil definert mål | M | `GoalEvaluationCell`, EntityAnchor-kvitteringer |
| **P1** | **Signert beslutnings- og effektkvittering.** Signer `ActionDecisionReceipt`; skill beslutning, sendeforsøk, providerrespons, bekreftet mottak. | Autentisk kontrollspor; T13 | Mottakerens videre bruk | M | `ActionDecisionReceipt`, identitetssignering |
| **P1** | **Replayvern og atomisk utførelse.** Revalider før effekt; idempotens; ukjent status ved timeout. | Dobbeltutførelse ved retry | «Exactly once» mot ekstern tjeneste | M | Intent-ID, kvotereservasjon, HavenAgentD nonce |
| **P1** | **Utvid Goal-motoren** med numeriske og temporale predikater + budsjett/kvote som hard reservasjon *før* effekt (ikke bare overvåking etterpå). | Overskridelse før neste effekt; billig auto-godkjenning | Verdi/rimelighet | M | `GoalEvaluationEngine`, gatewayens kvotereservasjon |
| **P1** | **Distribuert utløp/revokasjon.** Kortlevde fullmakter, ferskhetsgrenser, revokasjonskanal, oppførsel ved nettbrudd. | Bruk etter tilbakekalling; T11 | Øyeblikkelig revokasjon + offline samtidig | L | Contract-gyldighet, policyversjoner |
| **P1** | **Autentisert celle-/adapteridentitet** (nøkkel + endepunkt + forventet kontrakt). Full attestasjon av hver celleprosess: P2/L. | Tjenesteforveksling, identitetsbytte over bridge | Feil i autentisk kode | M | Identity, Contract |
| **P1** | **Taksonomi-governance.** Versjonert betydning, navngitt forvalter, endringshistorikk, eksempler, migrering; brukbar avklaringsvei for `prompt.unknown`. | T1 stille betydningsendring | Oppriktighet i erklært formål | M | Purpose Knowledge Base, taxonomy-digest |
| **P2** | Per-Grant purpose/action (V2) — bare når smale Agreements gir målt problem. | Presisjon i flerfunksjonsavtale | Bypass, taksonomi, sandbox | L | Agreement-policybinding |
| **P2** | Logg og tilsyn som celleflate (avvik, stopp, ansvarlig, gjenopptakelse) — støtte for AI Act art. 12/14, ikke samsvarserklæring. | Operatørinnsyn og inngripen | Etterlevelse i seg selv | M–L | Kvitteringer, Goals, audit-hendelser |
| **P3** | Flerpartskontrakter (signaturer, quorum, endring, revokasjon). | Flere selvstendige godkjennere | Semantisk enighet | L | Agreement/Contract |
| **P3** | Måling av «bidra positivt» — avgrensede forsøk med nytte, skade, baseline, etterkontroll; utsteder aldri rettigheter. | Læring om virkning | Universell sammenveiing | L | Goals, claim/evidence-modellen |

Rekkefølgen er styrt av ett prinsipp: **ingen agent får en effektbane før P0 for den banen er på plass**, og første bane skal være så smal at P0 er M, ikke L.

## 8. Claim safety — hva vi kan si offentlig

Trygt (med den avgrensningen som står):

1. «HAVEN har implementert en avgrenset gateway-bane som kontrollerer erklært formål, eksisterende celle-myndighet og bundne handlingsfakta før én forespørsel sendes til en godkjent AI-leverandør» — kode og målrettede tester finnes; ingen produksjonsverifikasjon påstås.
2. «I HAVEN kan et formål innsnevre en rettighet, men aldri opprette den» — for runtime-påstander må banen navngis.
3. «HAVEN kan evaluere eksplisitte mål deterministisk mot innsendte observasjoner» — lover verken sanne observasjoner eller signerte effektbevis.

Overclaims som skal avvises: «HAVEN hindrer prompt injection / garanterer at agenter handler i brukerens interesse»; «alle AI-handlinger har signerte kvitteringer som beviser samtykke og utførelse»; «formålsceller sikrer positivt samfunnsbidrag og gjør løsningen AI Act-kompatibel»; og — inntil P0 er levert — «HAVEN styrer AI-agenter».

Faktakorreksjon til briefen fra Astra: AI Act-tidslinjen har også 2. august 2028 for systemer integrert i regulerte produkter; art. 12 krever logging *tilpasset* risikoen, ikke «hele handlingskjeden» som generell regel. `[usikker: ikke selv verifisert mot lovteksten]`

## 9. Den sterkeste innvendingen

Astras formulering: *formålslaget gir ingen beslutningsrelevant sikkerhetsgevinst utover vanlig minst-privilegium, men gjør systemet vanskeligere å forstå og revidere.* Hvis de virkelige sperrene alltid er mottaker, ressurs, handling og kvote, mens formålet bare er en riktig stavet etikett agenten velger, ender HAVEN med kostbar hensiktsdokumentasjon og større falsk trygghet.

Min formulering: verdien avhenger av at agentens handlinger går *gjennom* celler, men agenter er mest nyttige akkurat der de har brede verktøy (kode, filer, nett). Blir tool-løkken tregere eller mer friksjonsfylt enn leverandørens egne godkjenninger, går brukerne utenom, og HAVEN blir tillatelsesteater på den minst interessante banen.

De to henger sammen, og begge er empiriske. Det som ville motbevise dem (Astra Q9, som jeg slutter meg til): én smal arbeidsflyt målt mot en kompetent baseline (samme modell, sandbox, verktøy, minste rettigheter) i tre varianter — eksisterende policy, samme policy med formålstekst, full HAVEN-binding — med oppgavesett som inkluderer legitim ombestemmelse, nye mottakere, injiserte meldinger, feil formålsmerking, policyendring, retry, utløp og alternative utganger. Kriterier fastsatt før forsøket: null uautoriserte effekter i angrepssettet, minst like god legitim løsning som baseline, færre unødige godkjenninger, forståelige avslag, og at vanlige brukere klarer flyten uten ekspert. Stoppkriteriet: hvis full HAVEN-binding ikke stopper noe baseline slipper gjennom, *eller* krever flere godkjenninger for samme oppgave, skal formål brukes som forklaring — ikke som kontroll.

## 10. Anbefaling til Kjetil

1. **Behold retningen, avgrens påstanden.** Den innsnevrede påstanden som kan forsvares: dataeieren kan begrense en agent som noen andre kjører, uten å stole på operatøren, og få en strukturert post om hva som skjedde. Det er noe leverandørene ikke leverer. Alt annet er kjent teknikk — si det høyt, det styrker troverdigheten.
2. **Én pilot: correspondence send** (Astra M5, jeg er enig). Minste løkke: testmelding → modellutkast som JSON-tekst → betrodd validering + oppgaveprofil → konkret ja gjennom M4-porten → én sending → kontroll i mottakercellen. 20 legitime + 20 adversarielle tilfeller i tre varianter mot en kompetent baseline; krav og snu-kriterium som i §6.2. Kan starte med lokal modell og syntetiske relasjoner nå, uten kreditt. Ingen generell tool-løkke, sandbox eller V2 før piloten har svart.
3. **Flytt to regler fra Losen til koden nå:** eksplisitt ja per melding i correspondence (payload-bundet, M4-porten), og `purposeRef` bestemt av oppgaveprofil, ikke av agenten. Det er små endringer og fjerner to påstander som i dag bare er sanne fordi jeg oppfører meg. Det er også inngangskravet til piloten — og til at pakken til Vegar kan kalles HAVEN-styrt.
4. **Fiks bevisstyrken før den brukes i tillitspakker:** signer `ActionDecisionReceipt`; ellers må tillitspakken si «strukturert, usignert».
5. **Ikke bygg** egen innholdsmoderator, egen sandbox i Swift, eller universell «positivt bidrag»-score. Forutsett leverandørens lag og OS-isolasjon; bruk HAVEN på det bare HAVEN kan.

## 11. Tillegg 2026-09-08: tillitspakke *før* og *etter* en agentflåte (Kjetils forslag)

Kjetil (etter §1–10): *generere en tillitspakke brukeren kan se gjennom før en eller en flåte av AI-agenter settes opp — hvilke modeller, lenker til instruksjoner, liste over Grants cellene har — så brukeren kan gjøre seg opp en mening, justere, og verifisere etterpå at pakken ble overholdt. Eks.: en AIGatewayCell har rett til å bruke en fetch-celle, med eller uten credentials, bare lese, evt. på en whitelist av sider — begrensninger modellen inne i cellen ikke kan gå utenfor.*

**Vurdering: ja — og det er den manglende brukerflaten for §7 P0 «ramme-objekt».** Astras «oppgaveprofil» (M3) er maskinobjektet; tillitspakken er den menneskelesbare projeksjonen av det samme. Fire regler gjør den til kontroll og ikke tillitsteater (T10):

1. **Generert, ikke skrevet.** Pakken avledes fra de faktiske objektene — Grants (`rwxs` per keypath), `CellExecutionPolicy.effectCeilings` (destinasjoner, dataklasser, execute/storage/disclosure), `AuthorizationPolicyBinding`, modellrute fra `model_provider_catalog`, instruksjons-digest — og bærer én pakke-digest over alt. Det brukeren leser *er* det som håndheves. En pakke som skrives ved siden av policyen er nettopp det A1 kaller «evidens, ikke myndighet».
2. **Transitiv rekkevidde, ikke bare liste.** For en flåte må pakken vise grafen: hvem kan kalle hvem med hvilke rettigheter, og hva det summerer til («AIGateway → fetch-celle (r---, uten credentials) → 5 domener»). Det er confused-deputy-linsen (T5) gjort synlig for et menneske.
3. **Håndhevet i cellen, ikke i modellen.** Fetch-eksempelet er den sterke formen: lese-bare, whitelist og credentials-eller-ikke ligger som Grant + condition i *fetch-cellen*; modellen holder aldri en credential (`credentials-after-authorization` finnes allerede som config-streng i A4-profilen). Whitelist = samme form som `allowedDestinationRefs` for leverandører.
4. **Etterpå = kvitteringer mot pakke-digest.** Verifikasjon er en diff «planlagt vs. observert»: hver `ActionDecisionReceipt`/effekt-kvittering bærer bindings-digestene; avvik fra pakken (ny destinasjon, credential løst opp, dataklasse utenfor, leverandørverktøy aktivert) vises som brudd. Krever P1 signert kvittering for at «overholdt» skal bety noe utad.

**Presisering av parentesen («om ikke modellen tillater det der den kjører — den må instrueres — eller vi kjører modellen selv»).** En hostet modell når verden bare gjennom celler — *unntatt* leverandørens innebygde verktøy (web search, kodekjøring, computer use) som kjører hos leverandøren. Instruksjon er den svake spaken. Den sterke er at AIGateway-forespørselen aldri slår på leverandørverktøy (A4s `no-tools` ligger allerede i `planDigest`), og at pakken viser «leverandørverktøy: av» som en linje kvitteringen kan bekrefte via payload-digest. Egen kjøring fjerner kanalen helt; hostet modell + digest-bundet forespørsel er beviset ellers.

**Bygger på:** `PersonalDataTrustPackageCell` (data-siden: `externalRequests` med method/url/purpose, retention, disclosure — samme mønster), `CellExecutionPolicy`, Explore-kontrakter, Agreement Workbench, `ActionDecisionReceipt`, Book 24 (modellkatalog). **Størrelse:** M for projeksjon + digest + «før»-flate; L med fetch-celle-ceilings, flåtegraf og «etter»-diff. **Løser ikke:** dårlig innhold innenfor tillatt scope; hva leverandøren beholder; at instruksjoner utover ceilingen ble fulgt.
