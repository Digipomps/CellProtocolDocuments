# Digipomps.org innholdsrevisjon

Dato: 2026-06-02

Status: redaksjonell anbefaling for oppdatering av `https://digipomps.org`. Nettstedet skal kun handle om HAVEN og Digipomps. Produktspor, kommersielle case og navn som ikke hører til HAVEN/Digipomps bør holdes utenfor denne publiseringsflaten.

## Kort konklusjon

Digipomps.org bør ryddes om fra en eldre fortelling om en stor global persondataplattform til en mer presis fortelling om:

1. Digipomps som ideell forvalter og offentlig stemme for et menneskeorientert digitalt fundament.
2. HAVEN som et arbeid for digital autonomi, samtykke, portable relasjoner, privacy og etterprøvbarhet.
3. CellProtocol som det tekniske protokoll- og runtime-grunnlaget: Cells, flows, domain-scoped identity, explicit contracts, capabilities, replay og audit.
4. Purpose/Interests som et context-local semantisk lag, ikke global reputation eller global person-ID.

Trygg hovedsetning:

> Digipomps utvikler HAVEN og CellProtocol for å gjøre digital samhandling mer eksplisitt, etterprøvbar, samtykkebasert og menneskeorientert.

## Avgrensning

Dette nettstedet bør ikke presentere separate produktspor, betalingsmodeller, konferansecase, sponsorcase eller verdiomfordelingsmekanismer. Slike spor kan være relevante i andre sammenhenger, men `digipomps.org` bør være den rene, prinsipielle og tekniske HAVEN/Digipomps-flaten.

Det betyr:

- Ingen produktnavn utenfor HAVEN/Digipomps på hovedsidene.
- Ingen konferansepilot som egen nettsideseksjon.
- Ingen sponsor-, lead-, payout-, credit- eller revenue-fortelling.
- Ingen claims om regulatorisk avklart økonomisk mekanisme.
- Ingen global reputation.

## Kildegrunnlag

Offentlig nettsted gjennomgått:

- `https://digipomps.org/`
- `https://digipomps.org/om-oss/`
- `https://digipomps.org/tjenester/`
- `https://digipomps.org/cellprotocol-explained/`
- `https://digipomps.org/purpose-framework-explainer/`
- `https://digipomps.org/bidra/`
- `https://digipomps.org/opprop/`
- `https://digipomps.org/vanlige-sporsmal/`
- offentlige WordPress REST-/sitemap-endepunkter for sider og innlegg

Lokale HAVEN-/CellProtocol-kilder brukt:

- `Book/00_Book_Home.md`
- `Book/01_CellProtocol_Core.md`
- `Book/02_Cell_Interfaces.md`
- `Book/03_Identity_Model.md`
- `Book/04_Agreements_Contracts.md`
- `Book/06_CellResolver.md`
- `Book/07_Scaffold_Runtime.md`
- `Book/09_Purpose_Interests.md`
- `Book/12_Skeleton_Spec.md`
- `Book/15_Documentation_Discovery_and_RAG.md`
- `Book/16_Book_Reference_Workspace.md`
- `Book/22_Explore_Contracts_For_Skeleton_Authoring.md`

Eksterne kilder som bør styre offentlig språk:

- European Commission, GDPR rights for individuals: `https://commission.europa.eu/law/law-topic/data-protection/what-are-my-rights_en`

Hvis donation/payment-funksjonalitet beholdes på nettstedet, bør også betalingsflyt og relevant regelverk sjekkes særskilt før publisering.

## Nåværende innhold og anbefaling

| Side/innlegg | Status | Anbefaling |
| --- | --- | --- |
| `Velkommen` / home | Gammel missiontekst med bredt løfte om global plattform og personlig datalager. | Skriv helt ny forside. Behold stiftelsesformål, men led med HAVEN, CellProtocol og digital autonomi. |
| `Om oss` | Relevant stiftelsesfortelling, men bygger på gammel PDS-/plattformlogikk og for bastante påstander om kommersielle aktører. | Omskriv. Gjør Digipomps til ideell forvalter/steward for HAVEN-prinsippene og åpent protokollarbeid. |
| `Plattform` / `tjenester` | Utdatert tekst om global autentisering/autorisering/anonymisering/persondata. For bredt og for sikkert. | Erstatt med ny `HAVEN`-side. Flytt gammel tekst til arkiv om ønskelig. |
| `CellProtocol explained` | Viktig, men utdatert: "proposal", nano services, gamle interface-beskrivelser, eksempel som ikke matcher siste dokumentasjon fullt ut. | Omskriv som teknisk, presis side: Cells, flows, contracts/capabilities, domain-scoped identity, replay/audit, transport independence, Skeleton/CellConfiguration. |
| `Purpose Framework explainer` | Verdifull idéhistorie, men "web-of-trust" og trustworthiness kan leses som global reputation. | Omskriv til `Purpose og Interests` med eksplisitt caveat: context-local, ingen global score. |
| `Trust` | Nyere og tematisk relevant, men for generell for produktside. | Behold som essay. Lenke fra ny side om "Hvorfor HAVEN trengs". |
| `We can't regulate ourselves...` | Relevant tese om nye digitale strukturer, men bruker collapse/singularity-språk som er for bastant for hovednavigasjon. | Arkiver eller omskriv kraftig før den brukes i navigasjon. Ikke bruk på forside. |
| `Bidra` / `Help` | Gammel donation-flow og emosjonell tekst. Mulig betalings-/pluginteknisk risiko hvis skjemaet er gammelt. | Ta ut av hovedmeny inntil donation-flow er verifisert. Lag heller `Bidra til HAVEN` med faglig, organisatorisk og eventuelt økonomisk bidrag tydelig skilt. |
| `Opprop` / `Petition` | Eldre personvernopprop. Relevant historisk, men ikke dagens presise HAVEN-fortelling. | Flytt til arkiv eller essayseksjon. |
| `Vanlige spørsmål` | Utdatert, uformelt og for bredt. | Omskriv FAQ fra bunnen: hva er Digipomps, hva er HAVEN, hva er CellProtocol, hva finnes nå, hva er ikke ferdig. |
| `Use cases` | Eldre retailer/persondata-eksempler som kan virke datainnsamlingsorienterte. | Avpubliser eller arkiver. Erstatt med prinsippielle HAVEN-scenarier: identitet, consent, portable context, audit og developer/runtime. |
| `Portefølje` | Templatetekst. | Avpubliser/slett fra meny. |
| `Galleri`, `Blogg`, `Store`, donor-system-sider | Tomt, plugin-/malpreget eller internt. | Skjul fra meny og søk hvis ikke aktivt i bruk. |
| `Broken Blockchain` | Eldre, kildetungt og delvis datert. | Arkiv. Ikke bruk som hovedargument. |
| `Krise for Digital Identitet` | Historisk COVID/Smittestopp-kontekst. | Arkiv. |
| `The pains of our digital future`, `Paradox of progress`, `Public goods...` | Idéessays. | Behold i arkiv/essay, men ikke som primær navigasjon. |

## Foreslått ny navigasjon

Minimal første versjon:

- Hjem
- HAVEN
- CellProtocol
- Purpose og Interests
- Artikler
- Om Digipomps
- Kontakt

Hvis vi vil ha en litt mer forklarende struktur:

- Hjem
- Hvorfor HAVEN
- HAVEN
- CellProtocol
- For utviklere
- Artikler
- Om Digipomps
- Kontakt

## Ny forside - anbefalt struktur

### Hero

Tittel:

> HAVEN: et åpent fundament for menneskeorientert digital samhandling

Ingress:

> Digipomps utvikler HAVEN og CellProtocol for å gjøre digitale relasjoner mer eksplisitte, etterprøvbare og samtykkebaserte. Målet er et digitalt fundament der mennesker kan opptre med mer autonomi, bedre privacy og tydeligere kontroll over hvilken tilgang de gir til andre.

Call to action:

- `Les om HAVEN`
- `Les om CellProtocol`
- `Ta kontakt`

### Seksjon: Hva er HAVEN?

> HAVEN er Digipomps sitt arbeid for et digitalt fundament der identitet, tilgang, formål, samtykke og audit er eksplisitt. Det handler ikke om én lukket plattformkonto som følger deg overalt, men om domain-scoped identitet, avgrensede contracts og etterprøvbare hendelser.

### Seksjon: Hva er nytt?

> Arbeidet har gått fra overordnet idé til et mer konkret protokoll- og runtime-grunnlag. CellProtocol beskriver nå Cells, flows, explicit contracts, capability-grants, domain-scoped identity, replay og audit. I tillegg finnes det dokumenterte spor for Skeleton/CellConfiguration, CellResolver, Scaffold/runtime, Book/RAG og Explore-kontrakter for å gjøre utvikling og testing mer etterprøvbar.

### Seksjon: Hvorfor dette trengs

> Digitale tjenester bygges ofte rundt skjult state, implisitt tilgang og datamodeller som er vanskelige for mennesker å forstå eller kontrollere. HAVEN snur retningen: tilgang, formål og dataflyt skal være synlig, avgrenset og mulig å etterprøve.

### Seksjon: Hva HAVEN ikke er

> HAVEN er ikke et globalt reputation-system, ikke en global person-ID og ikke en ferdig verdensplattform. Arbeidet bør presenteres som et åpent protokoll-, runtime- og governance-spor under utvikling.

## Ny `HAVEN`-side

Foreslått ingress:

> HAVEN er et forsøk på å gi digital samhandling et annet utgangspunkt: individets autonomi, tydelige avtaler, avgrenset identitet og etterprøvbar dataflyt. I stedet for at hver tjeneste skjuler sine egne regler i lukkede systemer, skal HAVEN gjøre relasjoner og tilgang eksplisitte nok til at de kan forstås, kontrolleres og replays.

Hovedpunkter:

- Domain-scoped identity, ikke global person-ID.
- Explicit agreements/contracts før tilgang.
- Capability-grenset state og handlinger.
- Purpose/Interests som semantisk lag uten global score.
- Replay og audit som grunnprinsipp.
- Transportuavhengighet: reglene skal ikke endre seg fordi noe flyttes mellom lokal runtime, bridge eller nettverk.
- Commons-/public-good-retning for protokollgrunnlaget.

## Ny `CellProtocol`-side

Foreslått ingress:

> CellProtocol er språket HAVEN bruker for å gjøre digital funksjonalitet eksplisitt. En Cell har avgrenset ansvar, publiserer hendelser, tar imot hendelser og endrer state på en måte som kan replays og auditeres. Når Cells kobles sammen, skal tilgang, formål og capabilities være synlige i kontrakten - ikke gjemt i en API eller en plattformkonto.

Hovedpoeng:

- Cell: deterministisk komponent med avgrenset state og handlinger.
- Flow: hendelsesstrøm som gjør oppførsel observerbar.
- Identity: kryptografisk og domain-scoped.
- Agreement/Contract: forespørsel og faktisk tildelt autoritet.
- Capability: konkret tillatelse, ikke generell tilgang.
- Resolver: håndhever identitet, contracts og capabilities når celler kobles.
- Scaffold/runtime: hoster celler, storage, replay og supervision uten å eie protokollsemantikken.
- Skeleton/CellConfiguration: gjør UI-/runtimeflater mer portable og testbare.

## Ny `Purpose og Interests`-side

Foreslått ingress:

> Purpose og Interests er HAVENs semantiske lag for å uttrykke hva en aktør prøver å få til, og hvilke typer kontekst som er relevante. Dette skal være context-local og eksplisitt. Det skal ikke bli en global reputation-score eller skjult profilering.

Hovedpoeng:

- Purpose beskriver intensjon/formål.
- Interests beskriver semantiske kategorier.
- Matching må være avgrenset til kontekst og avtale.
- Trust bør bygges med evidence og receipts der det er relevant.
- Ingen global reputation, ingen skjult atferdsscore.

## Ny FAQ

Forslag til spørsmål:

1. Hva er Digipomps?
2. Hva er HAVEN?
3. Hva er CellProtocol?
4. Hvorfor trengs HAVEN?
5. Er HAVEN en ferdig plattform?
6. Hva er en Cell?
7. Hva betyr domain-scoped identity?
8. Hva er agreements, contracts og capabilities?
9. Hva betyr replay og audit?
10. Hva er Purpose og Interests?
11. Er dette et globalt identitets- eller reputation-system?
12. Hvordan kan jeg bidra?

Kort svar på nr. 5:

> Nei. HAVEN bør presenteres som et protokoll-, runtime- og governance-arbeid under utvikling, med dokumenterte byggesteiner og prototyper, ikke som en ferdig global plattform.

Kort svar på nr. 11:

> Nei. Dagens retning er domain-scoped identity og context-local trust. HAVEN skal ikke innføre global person-ID eller global reputation.

## Redaksjonelle claim-regler

Ikke skriv:

- "Ferdig global plattform."
- "Global reputation."
- "Global person-ID."
- "Dette løser digital identitet."
- "Dette løser ulikhet."
- "Dette er regulatorisk avklart."
- "Dette hindrer kollaps."
- "Vi har bevist at modellen skalerer globalt."

Skriv heller:

- "HAVEN undersøker..."
- "Arbeidet bygger på..."
- "Målet er..."
- "Dagens retning er..."
- "Dette er dokumentert/prototypet, men må valideres videre..."
- "Context-local trust, ikke global score."
- "Domain-scoped identity, ikke global ID."

## Anbefalt publiseringsrekkefølge

1. Skjul åpenbare mal-/tomme sider: `Portefølje`, `Galleri`, `Store`, `Blogginnlegg-tittel`.
2. Ta `Bidra` ut av hovedmenyen til donation-flow er verifisert og teksten er skrevet om.
3. Erstatt forsiden.
4. Erstatt `Plattform` med ny `HAVEN`-side.
5. Erstatt eller oppdater `CellProtocol explained`.
6. Opprett eller omskriv `Purpose og Interests`.
7. Omskriv `Om oss`.
8. Omskriv FAQ.
9. Flytt eldre tekster til `Artikler / arkiv` med dato og kontekst.
10. Lag engelsk versjon etter at norsk struktur er godkjent.

## WordPress-tilgang

Codex kan ikke automatisk arve Safari-innloggingen fra shell/web-verktøyene. Mulige veier:

1. Bruke en kontrollerbar nettleser der innlogging er tilgjengelig.
2. Bruke WordPress Application Password / admin-API.
3. Bruke Safari GUI-automatisering med eksplisitt godkjenning, men dette er tregere og mer risikabelt for publisering.
4. Lage ferdige WordPress-klare tekstutkast lokalt, og lime dem inn manuelt.

Anbefaling: først godkjenn HAVEN/Digipomps-strukturen og norsk tekst, deretter publiser via WordPress med enten admin/API-tilgang eller kontrollert nettleserøkt.
