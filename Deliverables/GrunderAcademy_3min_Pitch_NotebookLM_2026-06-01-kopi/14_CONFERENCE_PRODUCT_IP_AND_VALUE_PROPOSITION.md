# DiMy konferanseprodukt: IP, verdiforslag og økosystemplassering

Oppdatert: 2026-05-13

Status: arbeidsnotat for kommunikasjon til Innovasjon Norge, investorer, arrangører og pilotkunder. Dette er ikke juridisk rådgivning, IPR-rådgivning eller regulatorisk konklusjon. Patentbarhet, freedom-to-operate, varemerke og avtaleverk må vurderes med kvalifisert rådgiver før ekstern pitch der eksklusivitet eller juridiske rettigheter vektlegges.

## Kort konklusjon

DiMy sin immaterielle verdi i konferanseproduktet er ikke at DiMy eier videomøte-teknologien. Jitsi/WebRTC er et utskiftbart media-lag. HAVEN/CellProtocol er det åpne og bruker-eide fundamentet. DiMy sin produkt-IP ligger i **kontrollplanet og verdilaget rundt konferansen**:

- samtykkebasert deltaker- og sponsorlogikk,
- kvalifisert lead vault med consent, qualification og unlock,
- entitlement- og gatekeeper-mekanikk for konferansetilgang,
- ressursmåling som knytter disk, CPU, minne, båndbredde, workers, AI og support til transparent pris,
- replaybar audit som gjør sponsorverdi og kostnader etterprøvbare,
- value-return-policy som kan simulere eller senere beregne ikke-overførbare fordeler til deltakere og commons,
- produktpakningen som gjør dette forståelig for arrangører, sponsorer og deltakere.

En trygg hovedsetning:

> DiMy gjør konferansen til en etterprøvbar verdiflyt: arrangøren kan skape og selge sponsorverdi uten å selge deltakernes tillit.

En mer teknisk setning:

> Konferanseproduktet er et HAVEN-basert kontrollplan for events der identitet, samtykke, adgang, ressursbruk, sponsor-unlock og audit uttrykkes som celler og replaybare verdihendelser.

## Kilder sjekket

Sjekket 2026-05-13:

- Innovasjon Norge beskriver tilskudd som virkemidler for bedrifter som skal starte, skalere, internasjonalisere og fornye, og sier finansiering skal bidra til innovasjon, konkurransekraft og bærekraftig vekst: [Tilskudd](https://www.innovasjonnorge.no/seksjon/tilskudd).
- Innovasjon Norge beskriver `Oppstartstilskudd 1` som rettet mot innovative oppstartsbedrifter med krevende teknologiutviklingsløp, betydelig markedspotensial og behov for å avklare betalingsvillig marked: [Oppstartstilskudd 1](https://www.innovasjonnorge.no/tjeneste/oppstartstilskudd-1).
- Innovasjon Norge beskriver `Oppstartstilskudd 2` som tekniske og forretningsmessige avklaringer for en lønnsom forretningsmodell: [Oppstartstilskudd 2](https://www.innovasjonnorge.no/tjeneste/oppstartstilskudd-2).
- Patentstyret skiller mellom immaterielle rettigheter og immaterielle verdier, der rettigheter gir juridisk kontroll, mens verdier kan være strategiske fordeler som kompetanse, relasjoner og omdømme: [Hva er immaterielle rettigheter og verdier?](https://www.patentstyret.no/immaterielle-rettigheter).
- Jitsi beskriver Jitsi Meet som en åpen videokonferanseløsning og Jitsi som en samling open-source prosjekter for videokonferanse: [Jitsi Meet](https://jitsi.org/jitsi-meet/) og [About Jitsi](https://jitsi.org/about/).

## IP-tese

DiMy bør kommunisere IP-en som en kombinasjon av beskyttbare og ikke-beskyttbare immaterielle verdier:

| Lag | Hva det er | Eierskapsfortelling | Kommuniserbar verdi |
| --- | --- | --- | --- |
| Tredjeparts media/infra | Jitsi, WebRTC, PSP, AI-provider, cloud | DiMy eier ikke dette; DiMy integrerer, drifter og bytter ved behov | lavere utviklingsrisiko, raskere pilot, mindre lock-in |
| HAVEN-fundament | CellProtocol, domain-scoped identity, agreements, grants, flow/audit, resource/value event standards | bør være felles/open/shared for tillit og portabilitet | gjør DiMy troverdig fordi verdiflyt kan etterprøves |
| DiMy produkt-IP | vertikal konferansepakke: gatekeeper, lead vault, exhibitor access, dashboards, policy, simulator, drift | DiMy eier implementasjon, design, playbooks, policy-maler, kundelæring og merkevare | gjør en generisk konferanse til et salgbart, auditerbart sponsorprodukt |
| DiMy operasjonell know-how | PSP/ledger-avstemming, pilotoppsett, arrangørprosess, sponsor onboarding, support, compliance evidence | forretningshemmeligheter, kontrakter, kundedata og dokumenterte prosesser | gjør produktet vanskeligere å kopiere enn bare en funksjonsliste |

Viktig nyanse: Hvis HAVEN skal være tillitsgrunnmur, bør ikke all event-/auditsemantikk låses proprietært. DiMy kan likevel ha sterk IP i produktisering, implementation details, UX, policy-pakker, dashboards, salgsmodell, kundedata, drift og vertikal know-how.

## Hva DiMy ikke bør påstå at det eier

- Generisk videomøte, skjermdeling eller chat.
- Jitsi/Videobridge/WebRTC-teknologien.
- Generisk CRM eller sponsor marketplace.
- Selve ideen om konferanseleads.
- HAVEN-protokollen som lukket DiMy-eiendom hvis strategien er at HAVEN skal være åpen, portabel og bruker-eid.
- Regulatorisk avklaring for credits, rebates, payouts eller e-money-lignende funksjoner.

## DiMy IP-aktiva

| Aktivum | IP-form | Hvor i dagens materiale | Hvorfor det er verdifullt |
| --- | --- | --- | --- |
| Consent-bound Lead Vault | opphavsrett i kode/UX, forretningshemmelighet i workflow, mulig kontraktsbeskyttelse | `ConferenceSponsorLeadAggregateCell`, `LeadVaultCell`, `ConsentReceiptCell`, `ExhibitorAccessCell`, conference fixture | gjør sponsorverdi målbar uten å gjøre deltakerdata til en svart boks |
| Resource-to-price stack | schema, policy, simulator, know-how | `ResourceUnitRegistry`, `ResourceMeterEvent`, `value_pool_simulator.mjs` | gjør påslag forklarbart og etterprøvbart, som er en tydelig differensiering |
| Conference gatekeeper | kode, arkitektur, sikkerhetsmodell | `JitsiConferenceGatekeeperCell`-plan, action/session-kontrakter | skiller kontrollplan fra media-plan og gir policy, roller og audit |
| ValueFlowViewer | produktdesign, rollemodell, audit UX | viewer-kontrakt og output-shape | gjør transparens til brukeropplevelse, ikke bare backend-logg |
| ValuePoolPolicy for konferanse | policy-maler, simulator, governance | conference synthetic fixture og policy v0 | viser hvordan sponsorverdi kan deles mellom operatør, commons og deltaker uten cash-out |
| Cross-cell eventmodell | schema, adapterkontrakter, test fixtures | `cell_event_adapter_contracts.v0.json` | gjør produktet repeterbart på flere eventdomener og senere vertikaler |
| Arrangør-/sponsor-/deltakerhistorien | merkevare, salgsmetodikk, pitch, onboarding | dette dokumentet og senere one-pagers | reduserer salgskompleksitet og gjør produktverdien lett å forstå |
| Pilotdata og benchmarks | konfidensiell kundedata, analyse, go-to-market learning | må samles i piloter | kan bli viktigste investor-IP fordi det viser betalingsvilje og defensibility |

Mulige patent-/designspørsmål som må vurderes senere, ikke påstås nå:

- Om en spesifikk metode for consent-bound lead unlock med ledger-backed entitlement, replaybar audit og value-return-policy er teknisk ny nok til patentvurdering.
- Om bestemte UI-/interaksjonsmønstre for value-flow viewer eller policy explainability kan designbeskyttes.
- Om navn som `DiMy Lead Vault`, `ValueFlowViewer`, `ProofDoor` eller konferanseproduktnavn bør varemerkeregistreres.

## Produktverdiforslag

Konferanseproduktet bør ikke pitches som "enda en videokonferanse". Det bør pitches som et event-tech produkt for **tillit, sponsorverdi og etterprøvbar økonomi**.

### For arrangør

Verdiløfte:

> Arrangøren får et konferanseprodukt som kan dokumentere deltakerflyt, sponsorverdi, samtykke og kostnader uten å miste tillit hos deltakerne.

Hva arrangøren kjøper:

- driftet konferanseworkspace,
- adgangs- og rollemodell,
- agenda/onboarding/matching,
- sponsor lead vault,
- rapportering og audit export,
- tydelig ressurs- og kostgrunnlag.

Hvor DiMy tjener penger:

- service package,
- deltaker-/eventkapasitet,
- sponsor lead unlock-pakker,
- AI/concierge usage,
- managed audit/support.

### For sponsor/exhibitor

Verdiløfte:

> Sponsor betaler ikke for en uklar logoeksponering alene, men for kvalifiserte, samtykkede relasjoner med audit trail.

Hva sponsor får:

- unlock av kvalifiserte leads,
- consent/qualification proof,
- role-scoped export,
- reversering/reclaim ved feil eller tilbakekalt samtykke,
- bedre grunnlag for ROI-dialog med arrangør.

### For deltaker

Verdiløfte:

> Deltakeren får kontroll over hva som deles, hvorfor det deles, og kan se når egen deltakelse skaper kommersiell verdi.

Hva deltaker får:

- eksplisitt consent,
- visibility scopes,
- egne receipts/proofs,
- mulig benefit i pilot som ikke-overførbar credit/rebate/grant,
- bedre matching og oppfølging uten global reputation.

### For HAVEN-økosystemet

Verdiløfte:

> Konferanseproduktet blir en konkret vertikal som viser hvorfor HAVEN trengs: portable contracts, replay, audit, resource events og value events.

Hva HAVEN får:

- praktisk testdomene for CellProtocol,
- dokumenterte standarder for value/resource metering,
- reusable eventkontrakter,
- bevis på at åpne protokoller kan støtte kommersiell drift uten å skjule verdiflyt.

## Kommunikasjon per publikum

| Publikum | Det de trenger å forstå | Første historie | Bevis som trengs |
| --- | --- | --- | --- |
| Innovasjon Norge | innovasjonshøyde, krevende utvikling, betalingsvillig marked, ansvarlig næringsliv | DiMy utvikler et ansvarlig event-tech kontrollplan som gjør sponsorverdi samtykkebasert og etterprøvbar | pilotkunde, teknisk roadmap, IP-strategi, bærekrafts-/ansvarlighetsvurdering, markedsintervjuer |
| Investorer | defensibility, timing, wedge, margin, skalerbarhet | DiMy starter med konferanser fordi hvert event har klare betalere, tydelige datapunkter og gjentakbar kommersiell flyt | ARR/pilotpipeline, sponsor WTP, marginmodell, switching cost, IP map, roadmap |
| Arrangører | mer inntekt, mindre manuelt arbeid, høyere tillit | Arrangøren kan tilby sponsorer bedre leads uten å miste deltakernes tillit | demo, pris, lead quality, rapporteksempel, personvern-/samtykkeflyt |
| Sponsorer | ROI og kvalitet | Betal for kvalifiserte relasjoner med samtykke, ikke bare synlighet | eksempelrapport, qualification criteria, export format, refund/reclaim-regler |
| Deltakere | kontroll og nytte | Du bestemmer hva som deles, og du kan se hva som skjer med det | klar consent UX, receipts, innsyn, revoke/reclaim |
| Tekniske partnere | integrerbarhet og kontrollgrenser | Jitsi/PSP/AI kan byttes; HAVEN eventkontrakter holder verdiflyten stabil | API-kontrakter, fixtures, replay tests, deployment plan |

## Historie-nivåer

### 20 sekunder

DiMy bygger ikke bare et konferanseverktøy. Vi bygger et tillits- og verdilag for konferanser, der sponsorverdi, deltakersamtykke, ressurskost og audit henger sammen. Arrangøren kan tjene mer på sponsorrelasjoner uten å gjøre deltakerdata utydelig eller ugjennomsiktig.

### 60 sekunder for arrangør

I vanlige konferanser er sponsorverdien ofte vanskelig å dokumentere: hvem møtte hvem, hvem samtykket, hva var faktisk kvalifisert, og hva kostet infrastrukturen? DiMy legger et HAVEN-basert kontrollplan rundt konferansen. Deltakere gir eksplisitt samtykke, leads kvalifiseres før sponsor-unlock, og alle kostnader og hendelser logges som rollebegrensede, etterprøvbare events. Resultatet er et produkt der arrangøren kan selge bedre sponsorverdi og samtidig vise deltakerne at tilliten er ivaretatt.

### 60 sekunder for Innovasjon Norge

DiMy adresserer ikke videomøter som råvare. Prosjektet utvikler et nytt kontroll- og verdilag for digitale og hybride konferanser, basert på HAVEN/CellProtocol. Målet er å gjøre tilgang, samtykke, lead-kvalifisering, ressursbruk, betaling og audit maskinlesbart og etterprøvbart. Første pilot avgrenser risiko ved å bruke PSP for betaling, ikke-overførbare entitlements og simulerbar value-return-policy. Det passer et utviklingsløp der både teknologi og betalingsvillig marked må avklares.

### 60 sekunder for investor

Konferanser er en god wedge fordi verdikjeden er tett: arrangører trenger inntekt, sponsorer trenger målbar ROI, deltakere trenger tillit, og alle hendelser er avgrenset i tid og domene. DiMy sin defensibility ligger i det vertikale kontrollplanet: consent-bound lead vault, resource-to-price metering, role-scoped audit og policybasert value return på HAVEN. Jitsi, PSP og AI-provider er utskiftbare underlag; DiMy eier produktlogikken, dataflyten, workflowene og pilotlæringen.

## Påstandsmatrise

| Påstand | Status | Trygg formulering |
| --- | --- | --- |
| DiMy eier hele videokonferanseteknologien | forbidden | DiMy integrerer og drifter videolaget, men produktverdien ligger i kontrollplan, audit og verdiflyt |
| DiMy gjør sponsorleads samtykkebaserte og etterprøvbare | safe med caveat | DiMy designer en flyt der sponsor-unlock krever consent, qualification og audit event; pilot må validere UX og juridisk grunnlag |
| DiMy kan dokumentere kostgrunnlag for konferansefunksjoner | safe med caveat | ResourceUnitRegistry og synthetic fixtures finnes; runtime-måling må kobles inn før produksjon |
| DiMy returnerer verdi til deltakere | aspirational for betalt pilot | V0 simulerer ikke-overførbar deltakerfordel; ekte fordel krever juridisk og regnskapsmessig vurdering |
| Dette er regulatorisk avklart | forbidden | Regulatoriske vurderinger må gjøres før ekte penger, cash-out, transferable credits eller ekstern aksept |
| Dette skaper et åpent HAVEN-økosystem | safe med caveat | HAVEN-delen bør holdes portabel og auditbar; DiMy tjener penger på drift, applikasjon og service |

## Produktverdi i én modell

```text
DiMy Conference Value Layer =
  conference control plane
+ consent/qualification/unlock workflow
+ resource-to-price metering
+ role-scoped audit/export
+ sponsor/organizer/attendee UX
+ operational playbooks and pilot data
+ HAVEN-compatible event contracts
```

Dette kan gi tre kommersielle pakker:

1. `Conference Workspace`: arrangør betaler for drift, roller, agenda, onboarding, møteflate og basisrapportering.
2. `Lead Vault`: sponsor/exhibitor betaler for kvalifiserte, samtykkede unlocks med audit.
3. `Value Transparency Pack`: arrangør/enterprise betaler for ressurskost, audit export, policyrapport og pilot-governance.

## Hva som må bevises neste

P0 før sterk ekstern pitch:

- én tydelig demo av arrangør-, sponsor- og deltakerflyten,
- pilotintervjuer med arrangører om betalingsvilje,
- sponsorintervjuer om betalingsvilje per kvalifisert lead/unlock,
- runtime-eksempel som produserer `ResourceMeterEvent` og `ValueFlowEvent`, ikke bare synthetic fixture,
- enkel rapport som viser gross, PSP/gebyr, ressurskost, DiMy allocation, HAVEN commons og eventuell deltakerbenefit,
- IP-strategi: hva holdes åpent i HAVEN, hva holdes proprietært i DiMy, hva vurderes som varemerke/forretningshemmelighet/patentkandidat,
- juridisk vurdering før ekte credits, rebates, payouts eller eksterne betalings-/wallet-lignende claims.

P1 for investorpakke:

- sammenligning mot status quo: vanlig konferanseplattform + CRM + sponsorrapportering,
- pilot KPI-er: consent rate, qualification rate, unlock conversion, sponsor satisfaction, organizer admin hours saved,
- marginmodell med ressurskost og supportkost,
- defensibility slide basert på IP-aktiva, ikke bare features.

## Diagrammer

- [conference_ip_stack.mmd](diagrams/conference_ip_stack.mmd)
- [conference_audience_story_map.mmd](diagrams/conference_audience_story_map.mmd)

