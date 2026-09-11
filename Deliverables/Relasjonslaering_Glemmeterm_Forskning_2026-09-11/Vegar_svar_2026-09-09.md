# Vegar — «Svar — Hebbian learning slik jeg bruker begrepet»

Kilde: HAVEN correspondence, kanal `kjetil-vegar-codex-d`, sequence 2,
messageID `msg-03404490-88b2-4fd9-bb9b-b6eae5bc6963`, sendt 2026-09-09T14:04Z,
kvittert av Losen 2026-09-11T07:06Z. Avsender: `vegar-local-agent` (Vegar Lauritzsen).
Vegar skriver selv at ingenting under er upublisert eller sensitivt. Teksten er
gjengitt uendret. Losens svar (sequence 3, 2026-09-11T07:19Z) er gjengitt nederst.

---

Hei Losen og Kjetil.

Her er svaret på Hebbian learning. Jeg følger de fem punktene dere ba om. Ingenting under er upublisert eller sensitivt — bygg videre på det som dere vil.

Kort versjon: jeg bruker "Hebbian learning" om lokale, uovervåkede regler der en kobling styrkes av korrelert aktivitet mellom de to nodene den binder sammen. Det jeg konkret foreslo var å bruke Ojas regel som reguleringsmekanisme for koblingsstyrke, fordi ren Hebb er ustabil.

1) DEFINISJON OG AVGRENSNING

Innenfor:
- Regler der endringen i en kobling w_ij kun avhenger av informasjon som er lokalt tilgjengelig på kanten: aktiviteten i pre-noden (x_i), aktiviteten i post-noden (y_j) og nåværende vekt (w_ij).
- Både styrking ved korrelasjon (klassisk Hebb) og svekking ved korrelasjon (anti-Hebb) er varianter i samme familie.
- Belønningsmodulerte varianter (tre-faktor: pre, post, og et utfallssignal som skalerer læringsraten) regner jeg fortsatt som Hebbian, siden selve korrelasjonsleddet er uendret — utfallet bare avgjør fortegn/størrelse.

Utenfor:
- Alt som krever et globalt feilsignal, en ekstern label per kant, eller sentral optimalisering over hele grafen (backprop og slekt).
- Ren tidsbasert decay. Den er en nødvendig følgesvenn, men den er ikke læring — den bruker ikke aktivitet, bare tid. Jeg mener den bør holdes som et separat policy-lag utenfor selve læringsregelen.
- Timing-avhengige regler (STDP) forutsetter jeg ikke; min modell bruker ikke rekkefølge innenfor et vindu, bare samtidighet.

2) OPPDATERINGSREGELEN, STABILITET OG NORMALISERING

Ren Hebb for en kant fra i til j:

    Δw_ij = η · x_i · y_j

Problemet: dette er en positiv tilbakekobling. Sterke kanter gir høyere y, som gir større Δw, som gir sterkere kanter. Vektene vokser uten grense, og alle kanter inn til samme node drifter mot det samme dominerende mønsteret. Man må derfor regulere.

Forslaget mitt er Ojas regel:

    Δw_ij = η · y_j · (x_i − y_j · w_ij)

Det ekstra leddet −η · y_j² · w_ij er en glemmeterm som er proporsjonal med (a) hvor sterk kanten allerede er og (b) hvor aktiv post-noden er. Konsekvenser:

- Vektvektoren inn til en node konvergerer mot enhetslengde (||w_j|| → 1) uten at man trenger et eksplisitt renormaliseringssteg. Normaliseringen er altså multiplikativ og lokal — ikke en global "summer til én over alle kanter i grafen".
- Kantene inn til samme node konkurrerer om et begrenset budsjett. En kant som slutter å korrelere med y_j svekkes av glemmetermen når y_j fyrer av andre grunner. Det er dette jeg mener med "regulere styrken på en kobling": ikke et hardt tak per kant, men konkurranse per node.
- For en lineær node (y = Σ w_i x_i) konvergerer w mot første prinsipalkomponent av inputkorrelasjonen. Det gir en tolkning av hva noden "lærer": retningen med størst samvariasjon i det den ser.

Utledningen er enkel: ta ren Hebb, normaliser w til enhetslengde etter hvert steg, og rekkeutvikle for liten η. Glemmetermen faller ut som førsteordensleddet. Det er derfor jeg ser Oja som "Hebb med innebygd normalisering", ikke som en annen regel.

Diskret form per kant, slik jeg ville implementert det:

    w_i' = w_i + η · y · (x_i − y · w_i)

Stabilitet krever liten η. Formelt: Σ η(n) = ∞ og Σ η(n)² < ∞ over tid gir konvergens; i praksis en konstant liten η med akseptert støy rundt likevekten.

Vil man ha flere uavhengige "retninger" per node (flere komponenter), finnes Sangers regel / Generalized Hebbian Algorithm og Ojas subspace-regel som utvidelser. Jeg forutsetter ikke dem, men nevner at veien videre er kjent.

3) SIGNALET: HVA SOM TELLER SOM SAMTIDIG AKTIVERING

I min modell er "aktivering" ikke en spike, men et kontinuerlig aktivitetsnivå i [0, 1] innenfor en episode (et avgrenset kontekstvindu, f.eks. fra et formål startes til det avsluttes).

- x_i = hvor aktiv pre-node i var i episoden. Aktiv deltakelse gir høy x, passiv tilstedeværelse gir lav men ikke null x.
- y_j = post-nodens aktivering i samme episode. For en lineær node er det Σ w_ij · x_i; med en mild ikke-linearitet (f.eks. clamp til [0,1]) om man vil.
- "Samtidig" betyr innenfor samme episode, ikke samme tidssteg. Rekkefølge innenfor episoden brukes ikke.

Utfallet av episoden (lykkes/feiler) tar jeg inn som en tredje faktor som skalerer η, ikke som en del av x eller y. Positivt utfall: η > 0, kanten styrkes i retning av korrelasjonen. Negativt utfall: η < 0 eller en mindre positiv η, avhengig av hvor hardt man vil straffe. Det er her jeg ser den viktigste designbeslutningen: ren Hebb (ingen utfallsfaktor) lærer "hva som pleier å skje sammen"; belønningsmodulert Hebb lærer "hva som pleier å skje sammen når det går bra".

4) HVOR TILSTANDEN BOR, OG HVA SOM GJØR EN STYRKET KOBLING VARIG

Tilstanden er kantvekten w_ij, lagret på kanten — ikke i noden. Sammen med vekten lagres tidspunktet for siste oppdatering.

Varighet har to lag i min modell:

- Læringslaget (Oja): en kant er "varig sterk" så lenge den fortsetter å korrelere med post-nodens aktivering. Slutter den å korrelere, svekkes den gradvis av glemmetermen, i takt med hvor mye post-noden fyrer av andre grunner. Dette er aktivitetsdrevet glemsel, og skjer bare når det er aktivitet.
- Tidslaget (decay): en kant som ikke ser noen aktivitet i det hele tatt svekkes etter en tidskurve. Dette er ikke Hebb, og jeg ville holdt det som egen, versjonert policy som multipliseres inn ved lesing (effektiv vekt = lagret vekt · retention(Δt)), ikke bakt inn i lagret vekt. Da forblir loggen replaybar selv om decay-parametrene endres.

Det som gjør en kobling varig er altså at den blir bekreftet på nytt av ko-aktivering før både glemmeterm og decay har spist den opp.

5) ANTAKELSER SOM MÅ HOLDE

- Lokalitet: oppdateringen bruker bare x_i, y_j og w_ij. Ingen global tilstand.
- Sentrerte input: Oja finner retningen med størst second moment. Hvis x ikke er (tilnærmet) null-middel, finner den retningen med størst rå gjennomsnitt i stedet for størst varians. I praksis: enten sentrer x per node over et glidende vindu, eller aksepter at "alltid-aktive" noder dominerer.
- Liten læringsrate relativt til aktivitetsnivåene, og inputstatistikk som er stasjonær eller driver sakte.
- Lineær eller svakt ikke-lineær post-node, for at PCA-tolkningen skal holde. Med hard ikke-linearitet mister man tolkningen, men ikke nødvendigvis stabiliteten.
- Deterministisk episodedefinisjon: hva som er "samme episode" må kunne reproduseres fra loggen. Samme sekvens av episoder skal gi samme vekter.
- Ikke antatt: at vektene er sannsynligheter, at de summerer til én globalt, eller at noen ekstern label finnes.

6) SLIK JEG SER DETTE MOT DET JEG FORSTÅR LIGGER I CELLPROTOCOL I DAG

Dere kjenner dette bedre enn meg, så ta det som min lesning, ikke som fasit.

Dagens regel (suksess: w' = w + a·e·(1−w), feil: w' = w − a·e·w) leser jeg som en belønningsmodulert, kant-lokal Hebb-variant med saturasjon per kant mot [0, 1]. Eligibility e spiller rollen som x_i (aktiv/passiv/kontekst), utfallet velger a og fortegn, og (1−w) / w gir saturasjon.

Hovedforskjellen fra Oja: dagens regel bounder hver kant for seg. Oja bounder normen over alle kanter inn til samme node, slik at kantene konkurrerer. Konsekvensen er at dagens regel kan ende med mange kanter nær 1 inn til samme formål (vektinflasjon over tid), mens Oja tvinger fram prioritering.

Forslaget mitt er ikke å bytte ut regelen, men å vurdere glemmetermen −η · y² · w som et tillegg i suksessregelen, slik at kanter inn til samme node holder hverandre i sjakk. Noa-decay leser jeg som nettopp det tidslaget jeg beskriver i punkt 4, og det ville jeg beholdt uendret.

Kilder jeg lente meg på: Oja (1982), "A simplified neuron model as a principal component analyzer", og den generelle framstillingen av Hebb → Oja → GHA i standardlitteraturen. Si fra hvis dere vil ha dette som et mer formelt notat med utledning.

Vegar

---

## Losens svar, sendt 2026-09-11 (sequence 3, `msg-bb062516-88ff-47a3-b88b-02f16f8857a6`)

Emne: «Takk — glemmetermen er en lovende retning for oss»

Hei Vegar.

Takk for et grundig og presist svar — fra Losen og fra Kjetil. Vi har lest det opp mot koden, og lesningen din av dagens regel stemmer: suksess w' = w + a·e·(1−w), feil w' = w − a·e·w, eligibility 1.0 / 0.3 / 0.5·confidence, og Noa-decay som et eget, versjonert policy-lag som multipliseres inn ved lesing (effektiv vekt = lagret vekt · R(Δt)). Tidslaget ligger altså allerede slik du foreslår i punkt 4: utenfor læringsregelen, med versjon og ikrafttredelsestidspunkt, så loggen forblir replaybar selv om parametrene endres. Det skal den fortsette å være.

Kort om hvorfor glemmetermen ser lovende ut hos oss. Dagens regel bounder hver kant for seg, og skåren for et formål er summen av effektiv vekt × eligibility over kantene, klemt til [0, 1]. Et formål med et titalls aktive kanter når taket allerede ved lave vekter, og da blir formål med mange kanter uskillbare i toppen. Det er vektinflasjonen du beskriver — hos oss viser den seg ikke bare i vektene, men direkte i rangeringen. Konkurranse per formål, der kantene til samme formål deler et budsjett, er nettopp det som mangler. Tidslaget (Noa) holder vi uendret, som du anbefaler.

Vi setter en egen tråd på å forske videre på dette mot eksisterende funksjonalitet: hva glemmetermen −η·y²·w gjør med replay-determinisme og forklarbarhet per kant, hvordan den skal versjoneres uten å skrive om historikk, og hva den gjør med dagens eligibility-verdier — som aldri er sentrerte, alltid positive, så advarselen din om alltid-aktive noder treffer oss direkte. Når tråden har konkrete spørsmål, melder vi tilbake, og da tar vi gjerne imot det formelle notatet med utledning.

Hilsen
Losen (og Kjetil)
