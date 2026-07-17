# HAVEN offentlig nettsted – rådgiverpanel og beslutningsgrunnlag

**Dato:** 2026-07-15  
**Leveranse:** Første selvhostbare, norsk offentlig nettside for HAVEN  
**Omfang:** Innhold, påstandssikkerhet, grafisk retning og funksjonell kontroll. Publisering og DNS-endring er ikke utført.

## Formål og mål

### `purpose://root` – mennesket først

Digitale verktøy skal øke menneskers handlingsrom og evne til å samarbeide, uten å gjøre mennesker til produkter eller globale poengsummer.

| Mål | Målestokk | Resultat | Status |
|---|---|---|---|
| Gjøre HAVEN forståelig uten forkunnskaper | Tre tydelige innganger: kort forklaring, konkret eksempel og teknisk fordypning | Alle tre finnes på forsiden og i artikkelfilteret | Oppfylt |
| Forklare tillit uten skjult rangering | Teknisk og kontekstuell tillit skilles; global personscore avvises | Egne artikler og diagrammer, med eksplisitt avgrensning | Oppfylt |
| Bevare menneskelig verdighet i uttrykket | Ingen personscore, kryptosymbolikk eller «allvitende» teknologi i tekst eller grafikk | Kontrollert i tekstsøk og visuell gjennomgang | Oppfylt |

### `purpose://content.review-before-publish` – etterprøvbare påstander

| Mål | Målestokk | Resultat | Status |
|---|---|---|---|
| Skille dagens byggesteiner fra ambisjonene | Statusspråk for finnes, prøves og forskes på | Statusforklaring på kilde- og metodesiden; egne ærlighetsartikler | Oppfylt |
| Gi dekning for problem- og prinsippåstander | Primærkilder fra EU, OECD, NIST og W3C, med lesedato | Tolv kildekort og tydelig forklaring av hva kildene støtter | Oppfylt |
| Unngå overkrav | Ingen løfter om å løse ulikhet, reparere demokratiet eller skape global tillit | Slike formuleringer er eksplisitt avvist eller omskrevet som hypoteser | Oppfylt |

### `purpose://gui.quality.functional-accessible` – enkel og vennlig bruk

| Mål | Målestokk | Resultat | Status |
|---|---|---|---|
| Fungere på mobil og desktop | Ingen horisontal overflyt ved 390 px eller 1280 px; lesbar navigasjon | Kontrollert i ekte nettleser | Oppfylt |
| Gjøre fordypning valgfri | Filter for introduksjon, konkret og dypere nivå | Filteret viser korrekt delmengde av 14 artikler | Oppfylt |
| Være lett å drifte selv | Statisk nettsted uten eksterne skrifter, analyseverktøy eller tredjepartsressurser | HTML/CSS/JS, Caddy, Dockerfile og Compose følger leveransen | Oppfylt |

## Påstandsstruktur

### Rotpåstand A

**Påstand:** En statisk, selvhostet førsteversjon er riktig offentlig inngang nå.

- **Støtte:** Den gamle siden blander språk, tekniske og samfunnsmessige påstander og har utdatert innhold. En statisk side gir få driftsavhengigheter og en kort vei til versjonert, gjennomgått tekst.
- **Motargument:** Et dynamisk CellProtocol-basert publiseringssystem ville i prinsippet uttrykke arkitekturen bedre.
- **Vurdering:** Den generiske offentlige side-/bloggruteren er ikke ferdig nok til å være publiseringsgrunnlag. Statisk v1 er derfor valgt, mens en senere offentlig lesemodell kan bygges uten å love den nå.
- **Beslutning:** Godkjent for v1.

### Rotpåstand B

**Påstand:** HAVENs tillitsmodell kan forklares som to komplementære lag.

- **Teknisk tillit:** identitet, signerte bevis, tydelige tillatelser, avgrensede avtaler og etterprøvbare hendelser.
- **Kontekstuell tillit:** menneskers og miljøers vurdering av erfaring i en konkret sammenheng.
- **Motargument:** Ordet «omdømme» kan lett oppfattes som en global poengsum eller skjult profilering.
- **Vurdering:** Nettstedet bruker derfor «kontekstuell tillit», viser at uenighet kan finnes, og sier uttrykkelig at HAVEN ikke skal gi alle én global score.
- **Beslutning:** Godkjent med denne avgrensningen.

### Rotpåstand C

**Påstand:** HAVEN gir bedre demokrati og jevnere fordeling av verdi.

- **Støtte:** Mer innsyn, tydeligere fullmakter, sporbare beslutninger og dokumenterte bidrag er plausible mekanismer som kan prøves.
- **Motargument:** Verken kode, arkitektur eller prinsipper dokumenterer alene bedre demokratiske utfall eller jevnere fordeling.
- **Vurdering:** Påstanden er for sterk som nåtidsfaktum. Teksten beskriver dette som forsknings- og pilotretninger, med spørsmål som må måles og med vern mot overvåkning, falsk presisjon og pengeaktig internverdi.
- **Beslutning:** Avvist som resultatpåstand; godkjent som avgrenset hypotese.

### Rotpåstand D

**Påstand:** Vi bør starte med mennesket.

- **Støtte:** Dette er et normativt valg for HAVEN, i samsvar med europeiske prinsipper om menneskesentrert digital omstilling, kontroll over data og digital deltakelse.
- **Motargument:** «Mennesket først» kan bli tomt dersom det ikke gir konkrete produktgrenser.
- **Vurdering:** Nettstedet knytter prinsippet til forståelige tillatelser, dataminimering, lokal kontroll, reverserbare valg, innsyn og fravær av global personscore.
- **Beslutning:** Godkjent som rotformål og produktregel.

## Rådgivernes vurderinger

### Publikums- og språkrådgiver

- Åpne med setningen «Digitale verktøy bør arbeide for mennesker».
- La leseren velge mellom et hverdagslig eksempel, hovedideen og en teknisk forklaring.
- Bruk korte artikler med én idé om gangen og en varm lærer-stemme.
- Behold ideen om et digitalt fristed, men fjern absolutte løfter og selvhøytidelig språk.

### Påstands- og risikorådgiver

- Beskriv HAVEN som et økosystem under utvikling med konkrete byggesteiner, avgrensede forsøk og tydelige forskningsretninger.
- Skill teknisk tillit fra menneskelig, kontekstuell tillit.
- Forby global omdømmescore, global personidentitet og skjult adferdsprofilering.
- Beskriv demokrati og verdifordeling som hypoteser som krever reelle piloter og målbare utfall.
- Ikke bruk de lokalt konfliktmerkede Book-kapitlene som offentlig sannhetsgrunnlag.

### Visuell rådgiver

- Bruk varm redaksjonell illustrasjon: papir, blekk, dempet grønt og leirefarger.
- Vis mennesker som likeverdige og teknologien som støttende infrastruktur.
- Unngå neon, glassflater, kryptosymboler, globale nettverkskloder og tall over mennesker.
- Bruk enkle, kodebaserte diagrammer som kan leses og vedlikeholdes uten designverktøy.

## Leveransebeslutninger

1. Norsk først, med enkel setningsbygning og få fremmedord.
2. Én forside, 14 korte artikler og én kilde-/metodeside.
3. Tre lesedybder: introduksjon, konkret og gå dypere.
4. Teknisk tillit, kontekstuell tillit og verdiflyt får egne SVG-diagrammer.
5. Én menneskesentrert redaksjonell heroillustrasjon; ingen eksterne bilde- eller skriftavhengigheter.
6. Caddy-baserte omdirigeringer bevarer sentrale adresser fra WordPress-siden.
7. Ingen publisering, DNS-endring eller sletting av gammel side før menneskelig innholdsgodkjenning og eksplisitt deploybeslutning.

## Verifikasjon

- Ekte nettleserpass på forside, artikler og kilder ved desktop- og mobilbredde.
- Mobilmeny og artikkelfilter aktivert og kontrollert.
- Ingen horisontal overflyt eller ødelagte bilder i de kontrollerte sidene.
- Én hovedoverskrift per side og beskrivende alternativtekst på innholdsbilder.
- SVG- og sitemap-XML validert.
- Docker Compose-konfigurasjonen validert syntaktisk.
- Deterministisk tekstanalyse kjørt på den ferdige teksten; analyse-id: `analysis-6c19f8432a79169c`. Verktøyet analyserte tekst uten egen kildekobling, så kildekvalitet og påstandsgrenser ble i tillegg kontrollert manuelt mot kildesiden.

## Åpne punkter før offentlig bytte

| Punkt | Eier | Terminal tilstand |
|---|---|---|
| Godkjenne offentlig ordlyd, kontaktinformasjon og avsender | Menneskelig produkteier | Eksplisitt godkjent eller returnert med konkrete endringer |
| Bestemme server og DNS-vindu | Driftsansvarlig | Vert, backup og reverseringsplan dokumentert |
| Kjøre Caddy-container og omdirigeringer mot midlertidig vertsnavn | Implementasjon/drift | HTTPS, sikkerhetsheadere, 404 og gamle lenker verifisert |
| Arkivere gammel WordPress-side | Driftsansvarlig | Lesbar backup bekreftet før DNS-bytte |
| Måle samfunnspåstander i avgrensede piloter | Pilotansvarlige | Hypotese, baseline, vern, måling og publiserbart resultat dokumentert |

Alle mål i dette leveranseomfanget er terminale. Offentlig publisering er bevisst holdt utenfor omfanget og krever en eksplisitt menneskelig beslutning.
