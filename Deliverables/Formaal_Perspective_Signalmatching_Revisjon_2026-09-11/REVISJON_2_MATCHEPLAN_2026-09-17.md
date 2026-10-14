# Revisjon 2: matcheplanen sett gjennom formåls-/interessematching og de nye entitydataene

Dato: 2026-09-17 · Losen · Bestilt av Kjetil: «Gå igjennom planen for matching igjen og se det ut ifra perspektivet av endringer i formåls og interesse matching. Vi har også gjort endringer i entitydata som er relevant.»

Stier er relative til HAVEN-roten. Alt som står som tall eller kodeatferd er lest i kilden i denne økten; egne slutninger er merket `[vurdering]`. Ingenting er bygget, kjørt eller endret.

## Kort svar

Planen står — men den er ikke lenger den samme planen, fordi to av premissene har flyttet seg og ett ledd er dokumenterbart blindt.

Beslutningene fra 05.09 (D1–D5) holder alle. Det som har endret seg er *hva matching er*: etter entitydata-gjennomgangen 16.09 er formål og interesser ikke lenger lister ved siden av relasjonen — de **er** relasjonen, som vektede noder i én graf, og tillit måles i om formålet er oppfylt i stedet for å være et eget felt. Det gjør Palazzos egen signalmodell til den fjerde parallelle representasjonen på et tidspunkt der beslutningen er at det skal være **én**.

Og det umiddelbare: **Palazzos matcher ser ikke de postene Sicilia-arbeidet lager.** Trykker gjesten «Vil smake», blir det en `purpose`-post; matcheren plukker bare `interaction`-poster. Reaksjonsknappene bygger altså en profil huset kan *spørre* om, men som aldri kan gi et treff. Det var hele poenget med artiklene.

## 1. Hva planen var, og hva som faktisk står

Beslutningene 05.09 (`PalazzoComunaleScaffold/docs/Vurdering_Signalmatching_Familietilhorighet_2026-09-05.md` §9): matching kjører i gjestens entitet (D1); over grensen går dom + forklaring gjesten har godkjent + tillitspakke (D2); samtykke er signert Agreement, og en invaderende handling er et eget grant, altså to per treff (D3); rekkefølgen er brief v1 → «husk det jeg sa» → flerlags innholdssignaler (D4); Palazzo betaler planleggingskostnaden (D5).

Bygget siden, alt i `PalazzoScaffold` og alt bare lokalt: husk-laget (signaler, treff i gjestens entitet, to grants, tillitspakke, kelnerlinje), Sicilia-laget (artikler med godkjente tagger, reaksjoner som poster, `insight.avoid`, antiformålet om lesesporing) og bridgehead-publisering. 105 tester grønne ved siste kjøring 08.09.

Det som *ikke* er bygget er selve matcheren i noen annen forstand enn ett bevisst lite lag: `PalazzoOneLayerTagMatcher` gjør bokstavelig, case- og diakritikk-uavhengig overlapp mellom husets godkjente signaltagger og gjestens egne ord. Det var riktig for D4-steg 2, og det er fortsatt den ærligste mekanismen vi har: den kan alltid forklares med gjestens egne ord.

## 2. Endring A — formåls- og interessematching

Revisjonen 11.09 (`REVISJON.md`, samme mappe) står uendret i sine funn, og formålsregister-PDD-en har siden fått G1 (12.09) og G2 (15.09) med Kjetils låsninger: registeret bor i CellProtocol, dimensjoneres mot 100 000 noder, **én motor fra første dag uten overgangsperiode**, invarianskrav på kvalitetsporten, og kilden er resultatet av forsoningen.

Tre ting derfra treffer Palazzo direkte.

**Én motor gjelder også Palazzo.** WP4b i planen fjerner to håndrullede matcheveier (`PerspectiveCell.swift:684` og `PurposeKnowledgeBase.resolvePrompt:551`) uansett hvem som vinner motorvalget. `PalazzoOneLayerTagMatcher` er en tredje håndrullet vei. Den står oppført i revisjonens punkt 4 — «adapter `PalazzoSignal*` til CellProtocols `Signal`, eller skriv ned hvorfor den skal være separat» — og er eksplisitt satt **utenfor** formålsregister-planen («Palazzo-adapteren og ny kvalitetsevaluering»). Den har altså ingen eier i dag. `[vurdering]` Det er planens tydeligste hull: en beslutning om «én motor uten overgangsperiode» med et unntak ingen har ansvar for, er ikke én motor.

**Kostnad er ikke lenger et argument for å beholde noe eget.** KSM-målingene 02.–03.09: matching 32–267 µs kompilert mot 445–2970 µs naivt, konfigurering 4,66 ms ved 170 noder og 7,94 ms ved 2 420, planlegging konstant 0,24 ms mens grafen tidobles, N* mellom 0,4 og 3,6. Palazzos hele signalmengde er i dag titalls noder. Å bruke den ordentlige motoren koster ikke noe som er målbart for en gjest.

**Kvalitet er derimot fortsatt uavklart, og det skjerper D2 i stedet for å svekke den.** Målingene 12.09: graf med 1–3 hopp og lærte vekter er ikke målbart bedre enn TF-IDF (R+@10 0,476 mot 0,476; lærte vekter vinner på trening, 0,917, og taper på holdout, 0,357). Dommerrunde 1 ga «ja» på alle 197 rader og kan derfor ikke skille motorene; runde 2 ble publisert 15.09 og har ingen avgitte dommer per 16.09. Flaskehalsen er fasit, ikke algoritme. `[vurdering]` For Palazzo betyr det at vi ikke kan love Andre bedre *treffkvalitet* fra en tyngre matcher. Verdien ligger et annet sted — i at treffet kan forklares og bevises — og det er nettopp D2. Planen bør derfor slutte å behandle «flerlags signalmatching» som et kvalitetsløft og begynne å behandle det som en *forklarings- og bevismekanisme*.

**Taksonomidivergensen blokkerer fortsatt eksakt match:** 44 refs i runtime mot 57 i Book 23, 31 felles, 26 dokumenterte som ikke kan løses opp og 13 udokumenterte som lever i drift. Palazzo bruker ikke `purpose://`-refs i matchingen i dag, og er derfor ikke rammet ennå — men får Palazzo-posten et `purposeRef` (se §4), arver den problemet.

## 3. Endring B — entitydataene

Book 37 (`CellProtocolDocuments/Book/37_EntityData.md`) med Kjetils gjennomgang av alle 253 elementene 16.09. Fem av beslutningene endrer matcheplanen. Ingen av dem er implementert i kode ennå.

| Beslutning | Hva den gjør med matcheplanen |
|---|---|
| `EntityRelationInterests` erstattes av Interest/Purpose, og `purposeRefs` av grafen | Gjestens interesser er ikke lenger en liste å slå opp i, men noder med kanter. Palazzos `insight.interests`/`insight.purposes` blir projeksjoner av grafen — og «avoid» blir en kant med retning, ikke et attributt `polarity: "negative"` |
| `EntityRelationStanding` erstattes av at **status og tillit måles i om relasjonens uttalte formål er oppfylt, vektet** | Dette er den største. Familiefølelse har ikke lenger bare en spørreundersøkelse som mål — den kan måles som oppfyllelsesgrad på uttalte formål i relasjonen gjest↔hus. D5 (hvem betaler) og Andres «gir dette mer omsetning?» får et felles, ikke-personidentifiserende måltall |
| `EntityRelationEvidence` erstattes av `proofs` med keypaths, og `proofs.index.byKeypath` gjør at **ett enkelt felt** kan være bevist | Tillitspakken i D2 bør ikke være en egen pakkestruktur, men `proofs` over de keypathene dommen bygger på. Da er «verifiserbar uten å vise profilen» en eksisterende mekanisme, ikke en Palazzo-oppfinnelse |
| `EntityRepresentation` er *min* representasjon av en annen entitet, ikke den andres data | Bekrefter D1 og gir kelnerbriefen et riktig hjem: husets bilde av gjesten er husets egen node, som lever av det gjesten har delt, og forsvinner ikke når gjesten trekker tilbake — men mister da sitt belegg |
| `person.attributes[]` er sandkassen, med kilde, konfidens, bevis og livsløp `proposed`→`active`→`promoted`→`deprecated` | Her hører tagger avledet av artikkelreaksjoner hjemme før de er kanoniske. Det løser problemet husk-arbeidet parkerte: tagger avledes maskinelt, men skal ikke bli sannhet før noen har gått god for dem |

To presiseringer fra Astras audit 16.09 som planen må ta med seg. For det første: `Purpose.goal` er **ikke** påkrevet i koden (`goal` er `CellConfiguration?`, initialiseres til `nil`, dekodes med `decodeIfPresent`, og bare `getGoal()` kaster). Kapittelets «påkrevet» er en semantisk beslutning, ikke en eksisterende invariant. For det andre: kapittelet gjengir avtalepost-beslutningen motsatt av referatet — kapittelet sier liste, referatet sier dictionary, og begge ankre skriver i dag dictionary. Det berører D3, siden samtykket lagres som signert Agreement. `[vurdering]` Dette må avklares før Palazzo bygger videre på avtalebanen.

## 4. Funnet: matcheren ser ikke reaksjonene

Dette er kontrollert i kilden, ikke utledet.

`PalazzoOneLayerTagMatcher.match` (`PalazzoScaffold/Sources/App/Models/PalazzoMatchModels.swift:93`) starter med å filtrere kandidatmengden:

```swift
let eligible = records.filter { $0.kind == .interaction && $0.source == "self" }
```

Sicilia-reaksjonene skriver (`PalazzoEntityCell.swift:246`) `wantToTaste` → `.purpose`, `interesting` og `notForMe` → `.interest` (sistnevnte med `attributes.polarity = "negative"`), og bare en fritekstkommentar → `.interaction`.

Konsekvensen, presist: gjesten som trykker «Vil smake» på pistasjartikkelen får en `purpose`-post med taggene *pistasj, Bronte, Etna*. Publiserer huset senere en rett tagget *pistasj*, blir det **ikke** noe treff — posten er filtrert bort før sammenligningen. Bare gjester som har *skrevet* noe med egne ord kan få et treffkort.

Det som *virker* er spørrebanen: `insight.interests` og `insight.purposes` leverer reaksjonene, med negative som `avoid`, når samtykkepolicyen er aktiv. Det er testet. Sicilia-oppgavens rot-formål er altså halvt innfridd — huset kan spørre, men gjesten kan ikke bli overrasket av det hun har reagert på.

To ting til i samme kodevei. `PalazzoMatch.Verdict` har `positive`, `negative` og `undecided`, men søk i hele `Sources/` gir null forekomster av at `negative` eller `undecided` noen gang produseres — matcheren setter alltid `.positive`. Vurderingen fra 05.09 sa at verdien for tillit er **størst på negativ polaritet** (allergen, «ikke for meg»); den delen er ikke bygget, bare modellert. Og den ene stedet polaritet faktisk brukes er `insight`-spørringen, ikke matchingen.

Til slutt en ting som er riktig og bør bli stående: stående grants er bevisst begrenset til `menuChangeKind` (`PalazzoEntityCell.swift:912`), så et artikkeltreff aldri kan glippe gjennom på et «alltid» gjesten ga for menyendringer. Det er nøyaktig den innsnevringen D3 krever.

## 5. Hva som står, endres og faller bort

**Står:** D1 (matching i gjestens entitet) — styrket av at `EntityRepresentation` nå eksplisitt er min representasjon av den andre. D3 (to grants, signert Agreement) — uendret, med forbehold om avtalepostformen. D5 (Palazzo betaler) — og målingene viser at beløpet er mikrosekunder per match.

**Endres:** D2. Tillitspakken bør realiseres som `proofs` med keypath-binding i stedet for en egen struktur, og dommen må kunne bære polaritet. D4s rekkefølge er innhentet av virkeligheten: lag 3 (innholdssignaler) er bygget på datasiden før lag 2s matcher kunne se dataene. Rekkefølgen bør derfor snus til å fullføre lag 2 mot de nye postetypene før mer innhold lages.

**Faller bort:** antakelsen om at en tyngre matcher gir bedre treff. Den er målt, og den holder ikke ennå. `[vurdering]` Planen bør bygge flerlags matching for forklarbarhet, bevis og polaritet — ikke for rangeringskvalitet — inntil dommergrunnlaget sier noe annet.

## 6. Revidert rekkefølge

1. **Rett blindheten** (liten, Palazzo, ingen avhengigheter): la matcheren se `.purpose` og `.interest` fra `source == "self"`, og la `notForMe` gi `negative` dom. Krever ett valg fra Kjetil om hva en negativ dom *gjør* (§7, valg 2).
2. **Skriv Palazzo-adapterens skjebne ned** (liten, men blokkerer): enten adapter mot CellProtocols `Signal`, eller en skrevet begrunnelse for at Palazzo er unntaket fra «én motor». Uten dette er beslutningen fra 12.09 ikke gjennomført.
3. **Tillitspakke → `proofs`** (middels): når entitydata-beslutningene implementeres, ikke før — men designet bør låses nå så husk-laget ikke må bygges om to ganger.
4. **Formålsregisteret går sin gang** (WP0 venter fortsatt på en baseline kjørt på Mac-en; WP4b er ikke blokkert). Palazzo kobler seg på når `cell:///PurposeRegistry` finnes, ikke før.
5. **Ny kvalitetsevaluering** (revisjonens punkt 5) — evalueringen er fra 09.08 og dekker ikke dagens tre.

## 7. Valg som er Kjetils

Disse fem kan ingen ta for ham. De ligger også som klikkbare kort i «Matchebenken» (artefakt, 17.09) med alternativer, konsekvens og anbefaling.

1. **Palazzo-matcheren mot én-motor-beslutningen.** Adapter nå, adapter når registeret står, eller skriv ned unntaket? Anbefaling: skriv ned unntaket nå og adapter når registeret står — men skriv det ned, ellers står beslutningen fra 12.09 uten dekning.
2. **Hva en negativ dom gjør.** «Ikke for meg» kan (a) skjule retten på gjestens egen flate uten at huset får vite noe, (b) merke den, eller (c) bare telle i `avoid` som i dag. Vurderingen 05.09 kalte (a) det sterkeste tillitsbeviset. Anbefaling: (a), fordi den aldri krysser grensen.
3. **Purpose uten mål.** Palazzos «Vil smake» blir en `purpose`-post uten `goal`. Skal Palazzo-poster få et målbart mål, eller skal de være `interest` med constraint? Anbefaling: `interest` med constraint — «vil smake» er en interesse med en betingelse om anledning, ikke et formål med måloppnåelse.
4. **Avtalepostformen.** Liste eller dictionary? Kapittel 37 og referatet sier hver sin ting, koden sier dictionary. Dette blokkerer D3-arbeid.
5. **Familiefølelse som oppfylt formål.** Skal Palazzo måle tilhørighet som vektet formålsoppfyllelse i relasjonen, slik `EntityRelationStanding`-beslutningen legger opp til? Anbefaling: ja, og la det være måltallet Andre får se — det måler forholdet, ikke personen.

## 8. Hva jeg ikke har kontrollert

`CellProtocol` og `CellScaffold` er ikke tilgjengelige fra denne økten; alle påstander om dem er sitert fra revisjonen 11.09 og Astras audit 16.09, ikke lest på nytt i kilden i dag. Ingen tester er kjørt — de 105 i `PalazzoScaffold` er fra kjøringen 08.09. Dommerrunde 2 er ikke kontrollert for nye svar etter 16.09 05:00Z. Entitydata-beslutningene er lest som beslutninger; ingen av dem er implementert, og jeg har ikke vurdert migreringskostnaden for eksisterende Palazzo-data.

---

**Artefakt:** «Matchebenken» (claude.ai-artefakt, 17.09) — funnet, tallene og de fem valgene som klikkbare kort med lagring. Valgene leses tilbake derfra.
**Køposter:** HD-0098 (matcheren ser ikke purpose/interest-poster) · HD-0099 (Palazzo-adapteren mot én-motor-beslutningen). Begge har eier `kjetil` og venter på valg 2 og valg 1.

## 9. Kjetils svar 21.09, og en retting av §2

Alle fem valgene er avgitt i Matchebenken (lest fra artefaktets lager 21.09).

| Valg | Svar | Kjetils begrunnelse, ordrett der den finnes |
|---|---|---|
| 1 Palazzo-adapteren | **adapter nå** (mot min anbefaling) | «Matching av formål og interesser er en viktig ting i HAVEN … å finne hva vi vil ha uten nødvendigvis å vite navnet. Vi skal bruke det som å insentivere positiv adferd ved å ha muligheten publisere at en annen entitet leverte på de formålene den hevdet den ville levere på … både selskaper og personer — og i tillegg prosesser. … Signalmatching en gjennomgående funksjonalitet i hele CellProtocol. Det behøver nødvendigvis ikke å være store matchinger men kommer til å brukes over alt.» |
| 2 Negativ dom | **skjuler retten på gjestens egen flate** | — |
| 3 «Vil smake» | **ingen av de tre** — nytt skille | «Purpose er en interest's *executive branch*. Jeg vil smake — det kan være en interesse — men jeg har som hensikt å gjennomføre det — er et formål. Når det har blitt et formål skal formålet ha et Goal — da skal den spises.» |
| 4 Avtalepostform | **liste**, med presisering | «Der avtalene lagres rått kan det være dictionary. Listen med revisjonskjede er referanser til spesifikke avtaler.» |
| 5 Tilhørighet som oppfylt formål | **ja** | — |

Valg 3 og 4 er ikke valg fra menyen min, men presiseringer som oppløser begge spørsmålene:

**Valg 3.** Skillet er *hensikt*, ikke datatype. «Vil smake» er en `Interest` så lenge det er en tilbøyelighet. I det gjesten har til hensikt å gjennomføre — bestiller, sier ja til treffet — blir det et `Purpose` med et Goal som er oppfylt når retten er spist. Det gjør det påkrevde målet uproblematisk: et formål oppstår først når det *finnes* noe målbart. Palazzo må da skrive reaksjonen som `interest` og først forfremme til `purpose` ved hensikt. `[vurdering]` Det er også svaret på hvorfor `Purpose.goal` kan være påkrevet i modellen uten at alt brukeren liker må ha et mål.

**Valg 4.** Begge former, på hvert sitt nivå: rå lagring av avtalen kan være dictionary nøklet på UUID, mens `signedAgreementEntity.records` er en ordnet liste av *referanser* inn i den. Rekkefølgen bevares der revisjonskjeden er, oppslag er raskt der avtalen er. Motsetningen mellom kapittel 37 og referatet var tilsynelatende.

### Retting: TF-IDF-sammenligningen sier mindre enn §2 lot den si

Jeg skrev i §2 at antakelsen om at en tyngre matcher gir bedre treff «faller», og anbefalte å bygge for forklarbarhet i stedet for rangering. Det første er riktig, men rammen var for trang, og Kjetil har rett i innvendingen.

Tre presiseringer.

**Målingen sa ikke «likestilt», den sa «kan ikke avgjøres».** R+@10 var 0,476 mot 0,476, men MRR+ var 0,642 for TF-IDF mot 0,531–0,544 for grafen, og fasiten dekket 4 av 19 oppgaver. Ingen av kandidatene er statistisk bedre enn noen annen. Riktig konklusjon er at målingen ikke gir grunn til å foretrekke noen av dem — ikke at de er like gode.

**Målingen testet ikke det signalmatching er til for.** Oppgaven var å rangere dokumenter etter tekstlikhet — TF-IDFs hjemmebane. Og grafen som ble målt var ikke den ekte: revisjon 1 slo fast at HAVENs formål ikke finnes i grafen i det hele tatt; testgrafen ble bygget av et leksikon utledet av den samme teksten. Det var altså TF-IDF mot en grafformet gjengivelse av TF-IDFs eget inndata. Uavgjort under de vilkårene er svakt bevis mot grafen, og heller mildt oppmuntrende. `[vurdering]`

**Fleksibiliteten er en forskjell i art, ikke i grad.** Dette er det bærende argumentet, og det er ikke et ytelsesargument. TF-IDF kan strukturelt ikke uttrykke: en dom som er **nei** (lav score er ikke det samme som avslag — allergenet som skjuler retten er et nei); «ikke avgjort fordi budsjettet tok slutt» som noe annet enn nei; lokale variabler som bæres fra lag 1 til lag 2 så lag 2 avgjør noe lag 1 ikke kunne, uten modellkall; betingelser som ferskhet, pris, størrelse, farge (Kjetils beslutning 13.09 om at formål skal normalisere produkter); proveniens per kant — hvilken node, hvilken kant, hvilken vekt — som er nettopp det D2 krever og som en cosinus ikke kan levere; og fusjon av nye mønstre uten å replanlegge de urørte.

Og det Kjetil selv peker på, som er det avgjørende: **leverte entiteten på de formålene den hevdet?** Det er et spørsmål om kanter over tid mellom et uttalt formål og bevis for oppfyllelse. Tekstlikhet har ingenting å si om det. Det er også samme mekanisme som valg 5 (tilhørighet som vektet formålsoppfyllelse) og som `EntityRelationStanding`-beslutningen — altså ikke en Palazzo-funksjon, men den generelle.

**Hva optimaliserbarheten faktisk er verdt.** Målt: kompilert matching er 5–30× raskere enn naiv, planlegging er konstant mens grafen tidobles, og det finnes strategier for indeksert signal, sparsom vektorfiltrering, parallell og GPU, samt hash-consing. TF-IDF er også optimaliserbar, men er en moden teknikk nær sitt tak; oppgraderingen er embeddings, som koster en modell. Signalmatchingens tak er **ukjent** — det er en svakere påstand enn «høyere», og bør ikke overselges. Den holder likevel asymmetrien: den ene har en kjent grense, den andre har ikke målt sin.

**Den reelle risikoen, som står.** Kvalitet kan bli *dårligere* og vanskeligere å feilsøke: de lærte vektene gikk fra 0,917 på trening til 0,357 på holdout. En håndvektet graf kan tape mot TF-IDF, og feilene er ugjennomsiktige uten fasit. Motgiften er allerede i planen og må ikke droppes: frossen fasit før sammenligning (WP12), invarianskravet (WP14), og at ukjent feiler lukket og differensiert etter polaritet (WP17).

**Konklusjon.** Signalmatching velges — ikke fordi den vant målingen, men fordi den kan uttrykke det HAVEN faktisk trenger: polaritet, betingelser, proveniens, lagvis avgjørelse og oppfylt-formål over tid. Valget skal skrives ned som et formålsbegrunnet valg, aldri som en ytelses- eller kvalitetspåstand, til fasiten finnes.

Det dette valget **ikke** avgjør: hvilken av de to Swift-motorene som blir den ene (KSM-porten eller CellProtocols egen). Det er måling X i WP4a, og står fortsatt åpent.

Der tekst er inndata og ingen node finnes ennå, må noe fortsatt gjøre tekst om til kandidatnoder — leksikon, TF-IDF eller en modell. Det er *inngangen*, ikke avgjørelsen. Signalmatching er avgjørelses- og forklaringslaget. De to er ikke rivaler på samme trinn.
