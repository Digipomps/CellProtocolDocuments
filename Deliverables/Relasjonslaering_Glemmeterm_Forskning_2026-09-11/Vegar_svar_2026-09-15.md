# Vegars svar på de fem S8-spørsmålene om glemmetermen

Mottatt over correspondence 2026-09-15 kl. 19:49 (`msg-66a79663`), lest og kvittert
2026-09-17. Teksten under er Vegars ordrett. Losens merknad står nederst.

Notasjonen han bruker: `e` = eligibility for kanten i episoden (1.0 / 0.3 / 0.5·conf,
eller 0 hvis noden er fraværende), `a` = 0.08, `y` = formålets aktivering i episoden.
Han oppgir å ha lest `RelationalLearningEngine.swift` (`ingestPurposeLifecycleEvent`,
`reinforcedWeight`, `scorePurposes`) og svarer mot den.

---

Hei Kjetil og Claude.

Takk for konkrete spørsmål — og for at dere målte før dere spurte. Jeg er enig i konklusjonen deres: skårings-v2 (sortér på rå, egen visningsskala) er riktig fiks for clamp-rangeringen, og β_forget = 0 i produksjon inntil videre er riktig. Glemmetermen må rettferdiggjøres av noe annet enn clamp-problemet, og det er det spørsmål 1 handler om.

## 1) Mål utover clamp-rangeringen, og hva som ville falsifisere

To mål, i prioritert rekkefølge:

**a) Gradsuavhengig diskriminering.** I dag er rå skår Σ w·e over tilstedeværende kanter. Den vokser med antall kanter formålet har rukket å samle, ikke bare med hvor godt de passer. Et gammelt, mye brukt formål slår et nytt som passer bedre, fordi det har flere kanter som hver bidrar litt. Skårings-v2 fjerner clamp-taket, men ikke denne gradsskjevheten — den gjør den faktisk synligere, siden rå skår ikke lenger klemmes. Glemmetermen er det som gjør at kanter inn til samme formål konkurrerer: kanter som ikke lenger deltar taper vekt relativt til de som gjør det, slik at formålets profil forblir «hvilke interesser kjennetegner dette», ikke «alt som noen gang har opptrådt sammen med dette».

**b) Raskere omstilling ved rutineskifte.** Noa-decay er lik for alle kanter og nullstilles ved forsterkning. Når brukerens rutine endres, holder kantene fra den gamle rutinen seg oppe så lenge formålet brukes i det hele tatt, fordi ingen mekanisme skiller mellom «formålet brukes» og «denne kanten deltok». Glemmetermen gir aktivitetsdrevet glemsel per kant, i tillegg til tidsdrevet.

Selektiv glemsel er altså virkemiddelet; normbudsjett er mekanismen; målet er a og b. Jeg foreslår ikke normbudsjett som mål i seg selv.

Falsifisering, på syntetiske logger med plantet fasit:

- **Gradstest:** to formål P1 og P2 med identisk «sann» interesseprofil, men P1 har dobbelt så lang historikk (flere kanter samlet). Gitt samme kontekst skal hybriden rangere dem likt innenfor toleranse; baseline vil rangere P1 over. Hvis hybriden fortsatt viser gradsskjevhet, er mål a falsifisert.
- **Skiftetest:** bytt plantet profil for et formål midtveis i loggen. Mål antall episoder før topp-N-kantene (`explain.topEdges`) matcher den nye profilen. Hvis hybriden ikke er raskere enn baseline + Noa, er mål b falsifisert.
- **Skadetest:** ved «burst» (mange episoder på kort tid med delvis kontekst) skal stabile kanter i den plantede profilen ikke falle under et gulv (f.eks. 0.5). Hvis de gjør det, er termen for aggressiv — det er den negative siden som må måles like nøye.
- **Presisjon:** precision@1 mot plantet fasit skal ikke bli dårligere enn baseline med skårings-v2 alene. Blir den det, taper hybriden uansett hva den vinner på a og b.

## 2) β-skjema og stabilitetsbetingelse

Kjernen i problemet dere peker på: i Oja er y en lineær utgang som skalerer med ‖w‖, og det er derfor −y²·w stabiliserer. Hos dere er y = Σ w·e, som skalerer med graden (opp til d hvis alle er aktive med e=1). Da blir y² ∝ d², og β må velges per grad for å være trygg. Det er uholdbart.

Forslag: normalisér aktiveringen med tilstedeværende eligibility-masse i stedet for å bruke rå y:

    ŷ = Σ w_i·e_i / Σ e_i   (sum over tilstedeværende kanter, e_i > 0)

ŷ er da et vektet gjennomsnitt av tilstedeværende vekter og ligger i [0, 1] uavhengig av grad. Hybriden blir:

    tilstede (e > 0):   w' = w + a·e·(1−w) − β·ŷ²·w
    fraværende (e = 0): w' = w·(1 − β·ŷ²)

Egenskaper:

- **Stabilitet.** Fraværende kanter følger w ← w·(1 − β·ŷ²), som er en kontraksjon uten oscillasjon når β·ŷ² < 1. Siden ŷ ≤ 1 holder β < 1 alltid. Tilstedeværende kanter følger et lineært kart med stigning 1 − (a·e + β·ŷ²), stabilt når a·e + β·ŷ² < 1 — også trivielt oppfylt. Stabilitet er ikke den bindende betingelsen.
- **Nytte er den bindende betingelsen.** En tilstedeværende kant vokser netto bare når a·e·(1−w) > β·ŷ²·w. Fikspunkt: w* = a·e / (a·e + β·ŷ²). Med a = 0.08, e = 1, ŷ = 1 og β = 0.02 gir det w* = 0.8. Med β = 0.08 gir det w* = 0.5, som er for lavt. Tommelfingerregel: **β ≤ a/4 = 0.02** holder aktive kanter over 0.8 selv ved maksimal aktivering, og gir fraværende kanter en per-episode-svekkelse på maks 2 % (mindre når ŷ er lav).
- **Gradsinvarians.** Fordi ŷ er et gjennomsnitt, gir en episode samme svekkelse av fraværende kanter enten formålet har 5 eller 50 kanter. Det er det som gjør at samme β kan brukes overalt.

Om dere heller vil beholde rå y i formelen: da er det ekvivalente skjemaet β_eff = β_0 / (Σ e)². Jeg ville lagret β_0 og normaliseringsmodus i en versjonert læringspolicy (samme mønster som `RelationalDecayPolicy`, med `effectiveFromTimestamp`), ikke som konstant i config.

Vær ærlig i dokumentasjonen om at **dette ikke er Oja**: fordi w klemmes til [0, 1] per kant, gjelder ikke argumentet om at ‖w‖ → 1. Det dere får er en konkurranseterm, ikke en normbetingelse. Det er greit — det er konkurransen dere trenger — men PCA-tolkningen er borte, og det bør ikke loves.

## 3) Eksplisitte brukerpreferanser: adskilt

Adskilt, og utenfor konkurransebudsjettet. Tre grunner:

- En preferanse er en instruks, ikke en observasjon. Lar man den svekkes ved fravær, overstyrer systemet stille det brukeren sa. Det er vanskelig å forklare («hvorfor ble preferansen min svakere?») og bryter forventningen om at eksplisitt slår implisitt.
- I dag er preferansen bare `weightStored := 0.6` pluss `metadata.reason = "explicit_preference"`, og metadata overskrives ved neste forsterkning (linje ~310, metadata settes på nytt). Etter én suksess er preferansen uskillbar fra lært vekt. Det er et problem allerede før glemmetermen; glemmetermen gjør det verre.
- Replay-messig er det billig å skille: nytt felt på kanten, gamle hendelser fortsatt gyldige.

Konkret forslag: legg `preferredWeight: Double?` på `RelationalEdge`. `explicitPreference`-utfallet setter dette feltet og rører ikke `weightStored`. Ved skåring: effektiv vekt = max(weightStored·R(Δt), preferredWeight). Preferansen er da et **gulv** som verken læring, konkurranse eller Noa kan senke; bare en ny preferansehendelse (eller eksplisitt tilbaketrekking) endrer den. Den lærte vekten konkurrerer fritt under budsjettet ved siden av.

Hvis dere heller vil at preferanser skal være myke hint som kan læres bort: da inn i budsjettet, men unntatt fra fraværs-svekkelsen (e = 0 gir ingen endring). Min anbefaling er gulv-semantikken.

## 4) Ikke-negativt budsjett er tilstrekkelig; sentrert PCA er ikke nødvendig

Ikke-negativt, forklarbart konkurransebudsjett er nok for målene i punkt 1, og er å foretrekke. Sentrert, signert hovedkomponentlæring gir en featuredetektor over en stasjonær inputfordeling. Målet deres er rangering av formål etter kontekstuell passform, med forklaring per kant. De to er ikke det samme.

Sentrering ville kostet:
- løpende gjennomsnitt per interesse/entitet over episoder (ny tilstand, ny historikk som må replayes),
- negative vekter («denne interessen taler mot dette formålet») — forklarbart i prinsippet, men ny vektsemantikk som må bæres gjennom explain, UI og kontrakter,
- fortegnsskifter tidlig i læringen, når gjennomsnittene ennå er dårlige.

Det eneste konkrete målet som ville rettferdiggjort det: behov for negativ evidens i rangeringen, altså «interesse X til stede gjør formål P mindre sannsynlig». Det kan ikke uttrykkes i dag (feilregelen senker bare mot 0). Men før dere går dit: konkurransetermen gir allerede en svak form for kontrast — en interesse som er fraværende når P lykkes, taper vekt på P. Jeg ville målt om den svake formen gir nok, med gradstesten og skiftetesten i punkt 1, før signerte vekter vurderes. Og dere har rett i at eligibility alltid er positiv; det er nettopp derfor sentrering ville krevd den ekstra historikken.

## 5) Fraværende kanter ved feilutfall: nei, rate 0

Glemmetermen betyr «formålet fyrte, og disse kantene deltok ikke — de er mindre kjennetegnende». Ved feil fyrte ikke formålet på en måte som bekrefter noe; episoden sier ingenting om de fraværende kantene. Å svekke dem straffer dem for en feil de ikke var del av, i tillegg til at tilstedeværende kanter allerede straffes av feilregelen. Å styrke dem (negativ η som snur termen) sier «det som ikke var her kunne ha hjulpet» — en spekulativ slutning som ville blåst opp akkurat de kantene dere prøver å rydde.

Så: β virker kun ved suksess. Ved feil beholdes dagens feilregel på tilstedeværende kanter, fraværende kanter røres ikke, og det eneste som virker på dem er tidslaget (Noa). Dere har allerede gjort riktig valg i forsøkene.

Én valgfri idé for feilregelen, ikke for fraværende kanter: skalér a_fail med ŷ. Høy ŷ ved feil betyr «konteksten så ut som en sterk match, likevel feilet det» — det er episoden der feilregelen har mest å si. Lav ŷ ved feil er lite informativ. Det er et separat forslag og kan ligge.

## Om versjonering og replay (fra forrige runde)

Dere utleder allerede oppdateringer for tilstedeværende kanter deterministisk fra lifecycle-hendelsen ved inntak, med policy oppslått på hendelsens tidspunkt. Fraværs-svekkelsen kan utledes på nøyaktig samme måte: for hver kant fra formålet med e = 0, én `RelationalWeightUpdateEvent` med reason `"competition_forget"`, β og ŷ i payload. Ingen ny historikk, bare flere utledede hendelser per episode (antall = grad). Hvis det blir for mange, kan de aggregeres til én hendelse per episode med en liste av (kant, previous, new). Med læringspolicy versjonert med `effectiveFromTimestamp` blir cutover like deterministisk som for Noa.

Foreslått forsøksrekkefølge: **A)** skårings-v2 alene som ny baseline. **B)** A + hybrid med ŷ-normalisering, β = 0.02, kun ved suksess, preferanser som gulv. Mål gradstest, skiftetest, skadetest og precision@1. Hvis B ikke vinner på a eller b uten å tape på skade eller presisjon, er β = 0 riktig også på sikt.

Si fra hvis dere vil ha fikspunkt- og stabilitetsutledningen som eget notat.

Vegar

---

## Losens merknad

Tre ting i svaret er beslutninger som må tas før implementering, ikke bare innspill:

1. **ŷ-normaliseringen endrer formelen**, ikke bare konstanten. Rå y erstattes av et vektet gjennomsnitt. Det gjør β gradsinvariant og er grunnen til at én β kan brukes overalt.
2. **`preferredWeight` som nytt felt på `RelationalEdge`** er en kontraktsendring. Den løser også en defekt som finnes i dag, uavhengig av glemmetermen: `metadata.reason = "explicit_preference"` overskrives ved neste forsterkning, så en eksplisitt preferanse blir uskillelig fra lært vekt etter én suksess.
3. **PCA-tolkningen skal ikke loves.** Vektene klemmes til [0, 1] per kant, så Ojas normargument gjelder ikke. Det er en konkurranseterm. Dette bør stå i dokumentasjonen før noen beskriver det som Oja.

Forsøksrekkefølgen A → B med de fire målene (gradstest, skiftetest, skadetest, precision@1) er testbar som den står, og bør inn i `PREREGISTRERING.md` før noe kjøres.
