# Glemmeterm i CellProtocols relasjonslæring

**Anbefaling: AVVIST som ny produksjonsregel nå. HD-0051 bør fikses separat ved å sortere på råskår og vise `raw/(1+raw)`.** Den additive glemmetermen kan gi raskere omstilling i de syntetiske driftsscenarioene, men taper også retningsbestemt rangering i sparse og tette scenarioer. Verken hybriden eller et L2-normtak løser skåringsmetningen. Dette er en anbefaling til Kjetil, ikke en registrert godkjenning av produksjonsendring.

144 syntetiske logger er kjørt med åtte regler, til sammen 1 152 kandidatkjøringer à 180 episoder. Dagens motor er kontrollert med 17 differensialfixtures og 1 063 binært identiske tall; tre ekstra Swift-fixtures måler migrasjonsfaren. De sju eksisterende motortestene passerer i en isolert bygging av uendret kildekode. Ingen CellProtocol-produksjonsfil er endret, og ingen melding er sendt til Vegar.

## Kildegrunnlag

Arbeidet gjelder lokal relasjonslæring og anbefalingsrangering. Det er ingen fysikkpåstand og ingen runde i UniverseSimulations v-serie. Målingene er gjort 12. september 2026, etter overleveringen fra 11. september. Kildecheckout: `CellProtocol` HEAD `4096760fe2b47d93d65d143320acfb51b4d50ff7`. Engine, Models, DecayPolicy og Cell er identiske med den lokale `origin/main`-referansen `c430a24c0d93d2cec9984149c4fb7546c6341bd3`; siste nettstatus for main er ikke påstått kontrollert. Eksakte filhasher ligger i [source_manifest.json](simulering/source_manifest.json).

| Kilde, faktisk hentet/lest | Betydning og kildegrense |
|---|---|
| [Oja 1982, *Simplified neuron model as a principal component analyzer*](https://neurophysics.ucsd.edu/courses/physics_171/Oja_1982.pdf), J. Math. Biology 15, 267–273, DOI 10.1007/BF00275687, s.268–270 | Førsteordensutledning og betinget lineær hovedkomponenttolkning. Fulltekst og ligningssider lest. Understøtter ikke en automatisk garanti for vår hybrid, hard clamp eller drift. |
| [Sanger 1989, *Optimal unsupervised learning in a single-layer linear feedforward neural network*](https://www.cs.cmu.edu/~bhiksha/courses/deeplearning/Fall.2016/pdfs/Sanger.pdf), Neural Networks 2, 459–473, særlig s.460–465 | GHA og flere komponenter med ortogonalisering; uavhengige Purpose-noder er ikke automatisk GHA. Hele PDF hentet, SHA-256 `3466afc26136cfe6f3d2f83ce8db2ec891baaa820c1f45905701106283666c3f`. |
| [Sanger 1988, *An Optimality Principle for Unsupervised Learning*](https://proceedings.neurips.cc/paper_files/paper/1988/file/e00da03b685a0dd18fb6a08af0923de0-Paper.pdf), s.12,14,18 | Skiller lineært konvergensresultat fra bestemte ikke-lineære forsøk. |
| [Vegar_svar_2026-09-09.md](Vegar_svar_2026-09-09.md), særlig pkt.2,5,6 | Forslaget som faktisk testes: glemmeterm lagt til dagens suksessregel. Ikke tolket som et krav om å erstatte hele motoren med Oja. |
| Engine linje 239–336, 429–503, 629–645; Models linje 455–520; DecayPolicy linje 98–132 | Gjeldende episode-, lærings- og skåringssemantikk. Full audit med linjeankre finnes i [MOTORREVISJON.md](underlag/MOTORREVISJON.md). |
| `Docs/RelationalLearning_Architecture_NO.md`, `Docs/RelationalLearning_Bruk_og_Drift_NO.md`, de to `commons/prompts/relational_learning_*prompt.md` | Rammer for determinisme, explainability, versjonering, lokale logger og additiv migrasjon. Dokumentene er eldre enn noen motoregenskaper; kildekoden er fasit. |
| [NIST, Exponential Distribution](https://www.itl.nist.gov/div898/handbook/eda/section3/eda3667.htm) og [Weibull Distribution](https://www.itl.nist.gov/div898/handbook/eda/section3/eda3668.htm) | Formelgrunnlag for den kvalitative decay-sammenligningen. Ingen empirisk påstand om menneskelig hukommelse følger av kurveformene. |

Ojas relevante resultat gjelder en lineær node og andre moment `C=E[xxᵀ]`; ved nullmiddel er dette kovarians. Diskrete steg og konstant læringsrate gir ikke i seg selv en eksakt norminvariant. Sangers utvidelse innfører ordnet fjerning av tidligere utgangers bidrag. Disse forutsetningene brukes som begrensninger, ikke som ferdig belegg for en produksjonsregel. Se den separate [litteraturrevisjonen](underlag/LITTERATURREVISJON.md) for sideankre og mislykkede kildehentinger.

### Korrigert brief

- F1 og F2 står: dagens suksess-/feilregel og Noa som eget leselag er korrekt beskrevet.
- F3 står for seks faktisk opprettede kanter etter én suksess: **raw=1.032, score=1**. Ukjente kanter som ikke er opprettet gir ingen skår. Ti lagrede 0.1-kanter summerer i Swift til **0.9999999999999999**, ikke eksakt 1; elleve gir 1.0999999999999999 og metning. Dette korrigerer både starttilstanden og eksakt flyttallspåstand.
- F4 må modereres: aktive traces er positive, mens fravær gir x=0 ved skåring. Usentrert læring påvirkes av `Cov(x)+μμᵀ`; alltid-aktive noder dominerer ikke nødvendigvis.
- F5 er et designvalg: formålet er semantisk post-node selv om kanten peker fra Purpose i datamodellen. Hele episoden stoppes også ved `contextConfidence<0.6`.
- F6 står, med et sterkere migrasjonsfunn: dagens journal kan inneholde kildehendelser som omberegnes med nåværende config. «Loggen finnes» er derfor utilstrekkelig som bakoverkompatibilitetsbevis.

## Formål og mål

Formål: Kjetil skal kunne avgjøre om aktivitetsdrevet konkurranse skal innføres uten å miste etterprøvbar læring eller rangering. Forankring: eksisterende `purpose://validation` og `purpose://source.methodology.current` fra Book 23. Målene og påstandene finnes også som typede strukturer i [MAL_OG_PASTANDER.json](MAL_OG_PASTANDER.json).

| Mål | Utgangspunkt → observerbart krav | Sluttstatus og bevis |
|---|---|---|
| G1 Instrumenter og dagens semantikk | F3 var bare utledet → målte null-/positivreferanser og Swift-paritet | Satisfied: referanser, 1 063 tall, originale 7 tester |
| G2 Samme-logg-sammenligning | Ingen målinger → alle seks scenarioer, grader 2/6/20, replay og fortegnsdiagnostikk | Satisfied: 144 logger, 1 152 kjøringer og rå-/aggregatfiler |
| G3 Beslutningsgrunnlag | Ingen adjudikasjon → S1–S8, én anbefaling og opptil fem spørsmål | Satisfied: denne rapporten og uavhengig gjennomgang |

Et målt nulltilfelle og et målt positivtilfelle finnes før metning, norm, tau, toppvalg, margin, vektendring, adaptasjon eller bitlikhet brukes som beslutningsgrunnlag. Alle-ties gir **udefinert tau-b**, ikke perfekt rangering. Referansene er instrumentkontroller, ikke en statistisk nullhypotese om brukere. Studien er eksplorativ og gir ikke bekreftende effektstørrelser for en brukerpopulasjon.

## S1 — Formell kartlegging og replay

La `w_i` være lagret vekt fra formål j til en interesse, entitet eller kontekstblokk; `x_i` er eligibility i avsluttet episode. Sett `r=Σ_i w_i x_i`. Beregn én frosset før-vektor og ett y per formål og episode. Nye, observerte kanter får dagens startvekt 0.1; eksisterende fraværende kanter inngår med x=0.

| Kandidat | Suksess før avsluttende clamp/projeksjon | Feil og preferanse |
|---|---|---|
| Dagens | `w+a*x*(1−w)`, a=.08 | Feil: `w−.05*x*w`; preferanse setter ønsket verdi, default .6 |
| Hybrid raw | `w+.08*x*(1−w)−β*r²*w` | Dagens feil/preferanse beholdes |
| Hybrid clamp | `w+.08*x*(1−w)−β*clamp01(r)²*w` | Som over |
| Oja-suksess | `w+η*y*x−η*y²*w`, y=r, η=.01 | Dagens feil/preferanse; dette gjør hele kandidaten forskjellig fra klassisk Oja |
| Sentrert/projisert | Samme Oja-steg med `z=x−mean(previous32)` og `y=Σwz`; projeksjon til [0,1] | Historikken bygges av godkjente suksessepisoder; dagens feil/preferanse |
| Budsjett | Først dagens suksess på observerte kanter, så `v/max(1,||v||₂)` over alle kjente kanter til formålet | Eksplisitt preferanse settes uendret; kan bryte normtaket frem til neste suksess |

**Hybriden er ikke Oja.** I den symmetriske, tette kontrollen x=1 gir egne likevektsutledninger følgende: ekte raw-Oja har `w=1/√n`; hybrid raw løser `.08(1−w)=β*n²*w³`; hybrid clamp i mettet regime har `w=.08/(.08+β)`. Slik ser vi direkte hvorfor Ojas enhetsnormteorem ikke følger med et tillegg til et annet forsterkningsledd. Dette er matematiske kontrolltilfeller, ikke et bevis på generell diskret stabilitet.

Konkurranseleddet er lokalt gitt `x_i,y_j,w_i` og en logget rate: y er et delt post-nodesignal. Aggregeringen skjer innen ett formål, ikke over alle menneskers graf. Budsjettvarianten krever i tillegg formålets norm og er formålslokal, men ikke samme tre-skalarlokalitet. Full konkurranse krever hendelser også for kjente kanter med x=0; bare dagens eligible-loop ville la dem stå urørt.

**Velg lagrede vekter til lærings-y.** Noa fortsetter å virke ved lesing. Et effektivt-y kan også være deterministisk dersom tidspunkt og policyvalg er del av kontrakten; problemet er koblingen til tidslaget, ikke tid i seg selv. Scoring uten et eksplisitt `at` bruker veggklokken i dagens API og kan ikke forventes byteidentisk mellom kjøringer.

Hvert kandidatsteg kan serialiseres som én vektoppdatering per berørt kant, med før/etter-verdi, policy og konkurranseforklaring. For et fast, ordnet kildeloggssett og fast policy er før-tilstanden identisk ved induksjon; sortert summering gir samme y og hver deterministisk funksjon gir samme neste tilstand. Dette argumentet forutsetter samme numeriske runtime, kanonisk rekkefølge og ingen flytting av cutover. Det erstatter ikke de målte testene og beviser ikke binær likhet på alle språk/plattformer.

## S2 — Simulering, metrikker og målinger

Hvert syntetisk datasett har tre formål A/B/C og n=2,6 eller 20 mulige kanter per formål. 180 episoder starter én time fra hverandre; hver avsluttes 30 sekunder senere. Motoren bruker dagens start/slutt-union, aktiv/passiv eligibility 1/.3, kontekst .5·confidence, confidence-gate .6, Noa og eksplisitt preferanse. Interesse-/entitetsidentiteter er delt mellom formål. Scenarioene varierer tetthet, drift, kontekst og utfallets sannsynlighet; syntetisk mål C har suksessrate .9 mot .3 for de andre. Drift/preference_change bytter til B ved steg 90. Dette er en definert simulatorfasit, ikke observerte menneskelige preferanser.

Primær metningsandel bruker bare lagrede kandidater. Toppmål bruker den faktiske kandidatlisten; tom liste har ingen korrekt topp. Den faste A/B/C-kohorten nullfylles kun i tau-, margin- og fortegnsdiagnostikk. Steg med skiftende kontekst gjør temporal tau til en blanding av kontekst- og læringsendring. L2-endringen beregnes over hele grafen per avsluttet episode, inklusive nyopprettede kanter; tabellen viser snitt av de siste 30 episodene. Lav endring alene er ikke kvalitet.

### Hovedresultater

Tallene under er likevektet gjennomsnitt over åtte seeds; alle per-seed-resultater og min/maks ligger i `aggregate.json` og `seed_metrics.json`. «Riktig topp» er treff på simulatorens deklarerte mål. Samme vekter brukes til begge kolonnene clamp og raw.

| Scenario, n=20 | Regel | Metning | Riktig topp, clamp | Riktig topp, raw | Raw mot dagens: vinn/tap/likt |
|---|---|---|---|---|---|
| sparse | Dagens | 28.00 % | 70.83 % | 90.69 % | 0/0/8 |
| sparse | Hybrid raw .02 | 20.87 % | 72.08 % | 86.81 % | 0/8/0 |
| sparse | L2-budsjett 1 | 14.02 % | 55.14 % | 62.08 % | 0/8/0 |
| dense | Dagens | 100.00 % | 0.00 % | 97.64 % | 0/0/8 |
| dense | Hybrid raw .02 | 100.00 % | 0.00 % | 82.15 % | 0/8/0 |
| dense | L2-budsjett 1 | 100.00 % | 0.00 % | 71.46 % | 0/8/0 |
| drift | Dagens | 97.53 % | 1.74 % | 89.72 % | 0/0/8 |
| drift | Hybrid raw .02 | 95.74 % | 3.75 % | 92.15 % | 7/1/0 |
| drift | L2-budsjett 1 | 95.83 % | 3.12 % | 90.21 % | 5/3/0 |
| preference_change | Dagens | 98.35 % | 0.83 % | 74.86 % | 0/0/8 |
| preference_change | Hybrid raw .02 | 98.18 % | 0.90 % | 78.26 % | 6/1/1 |
| preference_change | L2-budsjett 1 | 98.28 % | 0.90 % | 64.51 % | 0/8/0 |
| always_context | Dagens | 32.73 % | 74.38 % | 93.75 % | 0/0/8 |
| always_context | Hybrid raw .02 | 24.77 % | 76.67 % | 92.50 % | 0/7/1 |
| always_context | L2-budsjett 1 | 18.41 % | 64.72 % | 74.03 % | 0/8/0 |
| mixed | Dagens | 97.89 % | 1.04 % | 96.81 % | 0/0/8 |
| mixed | Hybrid raw .02 | 97.80 % | 1.04 % | 86.04 % | 0/8/0 |
| mixed | L2-budsjett 1 | 97.85 % | 1.04 % | 72.36 % | 0/8/0 |

**Det klareste skillet er tett n=20.** Dagens vekter gir 97.64 % riktig syntetisk topp ved raw-rangering og 0 % ved dagens clamp-rangering. Glemmeterm raw .02 gir også 0 % med clamp og 82.15 % med raw. Fiksen i skåring henter dermed tilbake informasjon som allerede finnes. Det er ikke evidens for at en ny læringsregel har lært mer.

Hybriden raw .02 forbedrer drift med n=20 fra 89.72 til 92.15 % raw-treff, men taper sparse fra 90.69 til 86.81 % og always_context fra 93.75 til 92.50 %. Seedvise fortegn viser at sparse tapte i 8/8 seeds, mens drift vant i 7 og tapte i 1. Slike blandede resultater skal stå ved siden av den vektede andelen; å velge bare drift ville gitt en misvisende generell anbefaling.

Den sterkeste pro-hybrid-armen er β=.005: ved n=20 steg raw-treff i drift fra **89.72 til 96.81 %** (7/0/1 seeds), og i preference_change fra **74.86 til 87.01 %** (8/0/0), med stabil byttemedian 17 episoder mot 40.5 og ingen sensurering. β=.02 ved n=6 preference_change steg fra **72.71 til 85.63 %** (8/0/0), med stabil median 25 mot 51.5, også uten sensurering. Dette er reelle retningsgevinster i de syntetiske loggene, ikke bare monotont reskalerte skårer.

β=.005 taper samtidig n=20 sparse 90.69→90.07 % (0/4/4) og dense 97.64→94.17 % (0/7/1). Den er derfor en sterk kandidat til en senere, målrettet driftstest, men ikke en generell dominans over dagens regel. Ingen vekting mellom omstilling, stabilitet og eksakte preferanser var gitt av produktmålet; denne studien finner ikke på en slik vekting for å kåre en vinner.

### Grader, norm og sparse-bevegelse

| Kanter | Regel | Metning, tett | Sluttnorm, tett | Endring L2, sparse |
|---|---|---|---|---|
| 2 | Dagens | 31.28 % | 0.8504 | 0.00946 |
| 2 | Hybrid raw .02 | 29.38 % | 0.7022 | 0.00914 |
| 2 | Oja-suksess .01 | 0.00 % | 0.1162 | 0.00078 |
| 2 | Sentrert/projisert .01 | 0.00 % | 0.0478 | 0.00075 |
| 2 | L2-budsjett 1 | 31.28 % | 0.7405 | 0.00946 |
| 6 | Dagens | 90.71 % | 1.3837 | 0.02175 |
| 6 | Hybrid raw .02 | 90.36 % | 0.8042 | 0.02151 |
| 6 | Oja-suksess .01 | 27.00 % | 0.3635 | 0.00198 |
| 6 | Sentrert/projisert .01 | 0.00 % | 0.0857 | 0.00162 |
| 6 | L2-budsjett 1 | 90.71 % | 0.8795 | 0.02195 |
| 20 | Dagens | 100.00 % | 2.5628 | 0.05237 |
| 20 | Hybrid raw .02 | 100.00 % | 0.8093 | 0.05697 |
| 20 | Oja-suksess .01 | 99.86 % | 0.7025 | 0.00666 |
| 20 | Sentrert/projisert .01 | 59.47 % | 0.1647 | 0.00372 |
| 20 | L2-budsjett 1 | 100.00 % | 0.9112 | 0.05726 |

Dagens tette n=20-rangering har temporal totalrekkefølge-tau **1.0**, samtidig med null treff på mål C: alt har score 1, og A vinner alfabetisk. Stabilitet er derfor ikke nok. Tau-b er udefinert når en sammenlignet skårvektor bare inneholder ties; to identiske vektorer med ulike skårer har derimot tau-b 1. Replay A/B gir identisk rekkefølge fordi tilstanden er identisk; det sier ingenting om hvor god rekkefølgen er.

### Adaptasjon etter bytte

Første topp er antall påfølgende episodeintervaller fra første spørrepunkt etter byttet, med 0 som umiddelbar topp. Stabil topp krever ti sammenhengende spørrepunkter. Perioden etter bytte inneholder 90 observasjoner. Medianer er bare for observerte bytter og må leses sammen med antall sensurerte kjøringer.

| Scenario n=20 | Regel | Første raw-topp, median observerte | Stabil raw-topp, median observerte | Stabil raw-topp sensurert /8 | Stabil clamp-topp sensurert /8 |
|---|---|---|---|---|---|
| drift | Dagens | 13.5 | 21.5 | 0 | 8 |
| drift | Hybrid raw .02 | 0.0 | 1.5 | 0 | 8 |
| drift | Oja-suksess .01 | 1.0 | 11.5 | 0 | 1 |
| drift | Sentrert/projisert .01 | 11.0 | 22.0 | 0 | 0 |
| drift | L2-budsjett 1 | 0.0 | 2.0 | 0 | 8 |
| preference_change | Dagens | 37.5 | 40.5 | 0 | 8 |
| preference_change | Hybrid raw .02 | 1.0 | 28.0 | 2 | 8 |
| preference_change | Oja-suksess .01 | 29.5 | 43.0 | 0 | 2 |
| preference_change | Sentrert/projisert .01 | 1.5 | 50.5 | 6 | 4 |
| preference_change | L2-budsjett 1 | 0.5 | 58 | 5 | 8 |

Preference_change bytter både suksessregime og én eksplisitt preferanse; latensen isolerer ikke preferanseeventens effekt. En separat kontroll i S3 måler hva en eksplisitt preferanse faktisk gjør med normen.

### Parametersjekk, n=20, uten vektet totalskår

| Regel | Sparse raw-topp | Tett raw-topp | Drift raw-topp | Alltid-kontekst raw-topp |
|---|---|---|---|---|
| Dagens | 90.69 % | 97.64 % | 89.72 % | 93.75 % |
| Hybrid raw .005 | 90.07 % | 94.17 % | 96.81 % | 93.54 % |
| Hybrid raw .02 | 86.81 % | 82.15 % | 92.15 % | 92.50 % |
| Hybrid raw .08 | 70.35 % | 48.61 % | 75.83 % | 80.35 % |
| Hybrid clamp .02 | 88.82 % | 97.64 % | 92.36 % | 93.19 % |
| Oja-suksess .01 | 89.79 % | 97.64 % | 94.72 % | 91.60 % |
| Sentrert/projisert .01 | 89.93 % | 97.85 % | 87.92 % | 91.39 % |
| L2-budsjett 1 | 62.08 % | 71.46 % | 90.21 % | 74.03 % |

Alle tre forhåndsvalgte β-verdier rapporteres. Treffandelene gjelder alle 180 episodene, ikke bare de 90 etter bytte. Ingen rate kåres til produksjonsvinner. Skåringsendringens invariant er målt separat: i **622080** parvise kohortsammenligninger endret soft-transformen **0** fortegn, mens clamp endret **162073**. Det er ingen ny retningsinformasjon fra soft-transformen. Flyttall kan likevel gi soft-ties utenfor disse parene; S6 beskriver kontrollen som avkrefter en universell garanti.

### Reproduksjon og råbevis

Kjør fra hvilken som helst mappe på denne Mac-en:

```bash
python3 /Users/kjetil/Build/Digipomps/HAVEN/CellProtocolDocuments/Deliverables/Relasjonslaering_Glemmeterm_Forskning_2026-09-11/simulering/run.py
```

På annen maskin: oppgi `--cellprotocol /absolutt/sti/CellProtocol`. Verktøyet nekter hvis de aktuelle kildefilene ikke matcher bevarte hasher. Swift-bygging skjer i en midlertidig mappe. `--out /absolutt/resultatmappe` velger resultatmappe. Python-standardbibliotek, Swift og Xcode/XCTest kreves; ingen pakker lastes ned.

- [synthetic_logs.json.gz](simulering/resultater/synthetic_logs.json.gz): de 144 rå loggene og spørringene, med scenario, seed og grad.
- [seed_metrics.json](simulering/resultater/seed_metrics.json) / [aggregate.json](simulering/resultater/aggregate.json): alle 1 152 målinger og 144 aggregatgrupper.
- [representative_histories.json.gz](simulering/resultater/representative_histories.json.gz): alle 180 tidspunkter, vektnormer og skårer for seed 0 i hver kombinasjon.
- [final_states.json.gz](simulering/resultater/final_states.json.gz): kanter og eventuell sentreringshistorikk for alle kombinasjoner.
- [controls.json](simulering/resultater/controls.json): tette likevektskontroller, fraværsablasjon, sentrering og preferanser.
- [instrument_references.json](simulering/resultater/instrument_references.json), [manifest.json](simulering/resultater/manifest.json), [swift_parity.json](simulering/resultater/swift_parity.json) og testlogger: instrumenter, hasher og verifiering.

Alle 1 152 kjøringer har identisk kant-/sentreringstilstand ved to kanoniske replay, også fra en omstokket kildeinputliste. Kantprojeksjonen er også lik ved rekonstruksjon fra simulatorens forskningsposter. Dette må **ikke** leses som bevis for en ferdig v2-journalimplementasjon: forskningspostene er ikke full `RelationalWeightUpdateEvent`, og full sesjons-/policy-/dedup-tilstand er ikke del av Python-snapshotet. Swift-testene dekker dagens faktiske replaykontrakt separat.

## S3 — Sentrering og normbudsjett

Ingen sentrering innebærer andre-momentlæring, med mulig bakgrunnsdominans. Kontrollen med to alternerende aktive interesser og én konstant kontekst (x=.5), etter 2 000 suksesser, gir følgende:

| Regel | Vekt a | Vekt b | Konstant kontekst | Norm |
|---|---:|---:|---:|---:|
| Oja-suksess raw | .575920 | .580229 | .578074 | 1.001259 |
| Sentrert/projisert | .933560 | 0 | .036522 | .934274 |
| L2-budsjett | .570459 | .587389 | .574065 | 1.000000 |

Konstant kontekst beholdes i den usentrerte kontrollen, men dominerer ikke entydig. Sentrering reduserer den konstante komponenten, samtidig som ikke-negativ projeksjon slår ut én av de to alternerende interessene. Det er ingen PCA-tolkning av dette resultatet. I helt konstant input blir z=0 etter innkjøring, og læringen stopper; lav bevegelse der er ikke demonstrert evne til å velge riktig formål.

**Blant de tre retningene anbefales en eksplisitt budsjettvariant som enkleste kontroll i eventuell videre forskning, uten PCA-påstand.** Den anbefales ikke innført nå: n=20 sparse tapte raw-treff i alle åtte seeds, og normtaket kolliderer med eksakte preferanser. Seks preferanser à .6 gir norm 1.469694. Ved neste budsjett-suksess reduseres en uobservert preferansekant fra .6 til .404573. Valget mellom hardt budsjett, reserverte preferanser og separate preferanse-/læringsvekter er et produktvalg som ikke er avgjort her.

Produksjonsanbefalingen er derfor foreløpig ingen sentreringstilstand og dagens læringsregel. En eventuell ny sentrering må spesifisere vindustype, størrelse, varmstart, fravær, hvilke utfall som oppdaterer gjennomsnittet og logget policyversjon. Sentrerte input er signerte og kan ikke ubemerket puttes inn i dagens [0,1]-eligibility-kontrakt.

## S4 — Samspill med Noa

Behold `effectiveWeight=weightStored*R(age)` og gjeldende Noa-parametre. Aktivitetsleddet virker på lagret vekt; det trenger ikke gjøre alder til en læringsvariabel.

Kontroll: to kanter har w=.6 ved t=0. Ved t=1 sekund lykkes formålet med bare den ene aktiv. Hybrid raw .02 får y=.6 og konkurranseledd `.02*.6²*.6=.00432`. Den fraværende kanten går fra .6 til **.59568**, med opprinnelig tidspunkt 0. Effektiv vekt er **.595679706** fordi R ennå er omtrent 1. Når kun eligible kanter oppdateres, blir vekten stående på **.6**. Denne ablasjonen viser hvorfor alle kjente kanter i det aktive formålet må besøkes.

Ved dag 30 er Noa-retensjonen **.099226173**. Konkurransevarianten gir effektiv vekt **.059107047** mot **.059535704** uten aktivitetsglemsel. Begge mekanismene virker på samme kant, men måler ulike ting: nylig aktivitet uten korrelasjon og tid siden støtte. Det kan være ønsket, men ønsket styrke må kalibreres; det er ikke automatisk «dobbel straff» eller automatisk riktig.

Ikke sett `lastReinforcedAt=now` ved ren konkurranse på en fraværende kant. Da ville aktiviteten fornyet tidslaget uten støtte. Dagens engine oppdaterer feltet også ved feil; dette er en eksisterende semantikk, ikke endret i simuleringen for observerte kanter. Eventuell v2 må navngi forskjellen mellom siste oppdatering og siste støtte.

### Tre alternative decayfamilier, kvalitativt

| Familie | Form og begrensning | Determinisme, forklaring og personvern |
|---|---|---|
| Eksisterende Noa | Normalisert produkt av to sigmoider + gulv .05. Parametre beholdes: 7d/30d, 1.2/.6 | Allerede logget, versjonert og lokalt beregnet |
| Stykkevis eksponentiell | `R=exp(−integrert hazard)`. Lav–høy–lav hazard kan konstrueres med eksplisitte segmenter | Replaybar med loggede knekkpunkter; enkle segmentforklaringer, flere parametre |
| Weibull | `R=exp(−(t/λ)^k)`. Ved k>1 kan absolutt fall først øke og så falle; hazard øker monotont | To parametre; definér om «sakte» gjelder absolutt fall eller relativ hazard |
| Forskjøvet potenslov | `R=(1+t/τ)^−p`; fallrate avtar for positive parametre | Lang hale og to parametre; ingen innledende akselerasjon uten ekstra struktur |

Disse kurvene kan alle være lokale og deterministiske. Ingen krever flere persondata bare på grunn av funksjonsformen. Tabellen er en matematisk sammenligning som oppfyller det eldre forskningsbriefets breddekrav; den inneholder ingen kalibrering mot menneskelige rutiner. Det finnes ikke belegg her for å bytte Noa.

## S5 — Forklarbarhet per kant

Dagens toppbidrag forklarer en skår, men ikke hele konkurransehistorikken. En additiv, foreslått oppdateringsforklaring bør inneholde:

| Felt | Hva det forklarer |
|---|---|
| `learningPolicyId/version`, kildeevent-ID og `inputStateHash` | Hvilken regel og før-tilstand som ga endringen |
| `eligibility`, `postActivation`, `activationBasis=stored` | Den lokale aktiviteten og betydningen av y |
| `reinforcementDelta`, `competitionDelta`, `projectionResidual` | Om endringen skyldtes støtte, konkurranse eller clamp/budsjett |
| `normBefore/normAfter`, evt. `budgetDivisor` | Hvor mye formålets samlede vektmasse påvirket kanten |
| `lastSupportedAt`/bevart `lastReinforcedAt` og separat `updatedAt` | Hvorfor en oppdatering ikke nødvendigvis fornyer Noa-alderen |

Feltene er et **forslag**, ikke eksisterende API. Nåværende event har ikke disse typed feltene, selv om noen tall kan serialiseres som metadata. Tallene bør beregnes ved hendelsen og versjoneres; forklaringen må ikke rekonstrueres med dagens nye policy og presenteres som historisk årsak.

Vis eksempelvis: «Vekten falt .00432 fordi andre forbindelser aktiverte formålet; denne forbindelsen var ikke aktiv. Tidsalderen ble beholdt.» Del ikke identiteter eller vekter for andre kanter utover mottakerens eksisterende rettigheter. Også y og norm kan avsløre aggregert aktivitet, så hold detaljene eierlokalt og gi avledet tekst/avrundede verdier innen samme tilgangsgrense. Ingen ny sentral logging foreslås.

## S6 — Skåringsnormalisering og HD-0051

Med `||w||₂=1` og `0≤x_i≤1` gir Cauchy–Schwarz `0≤raw≤||x||₂≤√n`. Enhetsnorm er derfor ikke det samme som raw≤1. Den tette kontrollen, med Noa satt til `.none` for å isolere læring, måler:

| Kanter | Regel | Raw etter 1500 suksesser | L2-norm | Score clamp |
|---|---|---|---|---|
| 2 | Dagens | 2.000000 | 1.414214 | 1 |
| 2 | Hybrid raw .02 | 1.364656 | 0.964957 | 1 |
| 2 | Hybrid clamp .02 | 1.600000 | 1.131371 | 1 |
| 2 | Oja-suksess .01 | 1.414214 | 1.000000 | 1 |
| 2 | L2-budsjett 1 | 1.414214 | 1.000000 | 1 |
| 2 | Oja clamp .01 | 1.999999 | 1.414213 | 1 |
| 6 | Dagens | 6.000000 | 2.449490 | 1 |
| 6 | Hybrid raw .02 | 2.426823 | 0.990746 | 1 |
| 6 | Hybrid clamp .02 | 4.800000 | 1.959592 | 1 |
| 6 | Oja-suksess .01 | 2.449490 | 1.000000 | 1 |
| 6 | L2-budsjett 1 | 2.449490 | 1.000000 | 1 |
| 6 | Oja clamp .01 | 5.999998 | 2.449489 | 1 |
| 20 | Dagens | 20.000000 | 4.472136 | 1 |
| 20 | Hybrid raw .02 | 4.000000 | 0.894427 | 1 |
| 20 | Hybrid clamp .02 | 16.000000 | 3.577709 | 1 |
| 20 | Oja-suksess .01 | 4.472136 | 1.000000 | 1 |
| 20 | L2-budsjett 1 | 4.472136 | 1.000000 | 1 |
| 20 | Oja clamp .01 | 19.999995 | 4.472135 | 1 |

**Avgjørelse for HD-0051: FIKS.** Bruk råskår som primær sorteringsnøkkel; purposeId bare når råskårene faktisk er like. Vis en avgrenset skår `f(raw)=raw/(s+raw)`, s=1 som eksplisitt, versjonert skala. Derivert er `s/(s+raw)²>0` i reell aritmetikk. Verdier som 1.032 og 3.44 får forskjellig visningsskår, uten at kantvektene endres.

Sorter likevel ikke bare på transformert Double. Kontrollen `4.0` og `nextafter(4,+∞)=4.000000000000001` gir begge soft=.8. Raw-sorteringen bevarer denne forskjellen. Resultatet «0 endrede fortegn» gjelder de målte parene, ikke alle representerbare flyttall.

Ingen normalisering behøves for selve rangeringen. Soft er et visnings-/API-valg, ikke en sannsynlighet. Normalisering med en formålsspesifikk grad eller inputnorm kan omrangere formål og krever et separat produktmål om størrelsesbias. Det er ikke nødvendig for å rette clamp-tapet. Eksisterende terskelforbrukere av `score` må identifiseres før endret skala settes som standard; denne studien har ikke auditert alle konsumenter.

HD-0051 er en anbefalt, spesifisert kodeoppgave. Den er **ikke implementert eller testet i produksjonskoden** av denne leveransen. Aksepten bør inkludere seks/tyve-kanters fixtures, eksakt raw-tie, den nærliggende flyttalls-tien, nullråskår, rangering på samme snapshot og oppdatert kontrakt for terskler.

## S7 — Versjonering og migrasjon

En ny `RelationalLearningConfig` alene er utilstrekkelig. Faktisk Swift-kjøring av gammel lifecycle-logg med alphaSuccess endret fra .08 til .2 ga aktive kanter **.28** i stedet for **.172**. Kun gamle vektoppdateringer ga .172; blandet lifecycle+vektlogg ga igjen .28 fordi kildehendelsen først genererte samme deterministiske vekt-ID og den historiske oppdateringen ble deduplisert bort. Bevis: de tre migrasjonsfixturene og [migration_summary.json](underlag/migration_summary.json).

En eventuell lærings-v2 bør bruke en egen uforanderlig `LearningPolicyUpdated` med ID, versjon, `effectiveFromTimestamp`, updateRule, β/η, y-grunnlag, fraværs-/tidsstempelsemantikk og eventuelle vinduparametre. Lokal config kan angi initiale defaults, men journalen må bevare hvilken policy som faktisk gjaldt. Gamle hendelser uten en ny læringspolicy må fortsatt få den opprinnelige v1-regelen og dens faktiske legacy-konfigurasjon; manglende data kan ikke repareres ved å gjette dagens standarder.

Foreslått migreringsrekkefølge:

1. Bevar en uendret v1-deriveringsbane med dagens event-ID og valider gamle kilder/vekter/blandinger mot golden fixtures. Synliggjør kilde-konfigurasjon der den finnes; marker ukjent proveniens.
2. Legg nye valgfrie felt til codec med `decodeIfPresent`/eksplisitte legacy-defaults. Swift-initializer-default alene gjør ikke syntetisert Codable bakoverkompatibel.
3. Logg policyen før cutover. Definér avgjørelse for policytidslikhet, sent ankomne hendelser, åpne episoder og tilbakevirkende policy. Bruk deterministisk avslutningstidspunkt i denne kandidaten; ikke veggklokke.
4. Beregn v2 fra en atomisk, sortert før-vektor. Nye v2-ID-er må inkludere policy-/regelidentitet, men en migrering må også ha én autoritativ strategi for blandede gamle/nye kilde- og vektposter, slik at versjonerte ID-er ikke skaper dobbelt anvendte oppdateringer.
5. Hvis sentrering prøves, replay eller snapshot også vinduet med policyhash og verifiserbart kildeområde. Vektposter alene gjenskaper ikke historikken.
6. Gjennomfør shadow-evaluering lokalt. Promotion krever Kjetils formåls-/målbeslutning, produksjonskontrakttester og målt nytte utover bare gjenopprettet raw-rangering. Rull tilbake med ny policy etter et nytt tidspunkt; ikke slett historikk.

Dagens `replayTransaction` sorterer etter tid, type, ID og payload; `restore` følger journalens sekvens. Swift-fixturen med start `z-start` og slutt `a-end` ved samme timestamp gir derfor forskjellig ankomst- og sortert replaytilstand, mens restore bevarer journalen. Det er en dokumentert kontraktgrense som må avklares før v2, ikke et nytt løfte om at enhver ankomstrekkefølge allerede er ekvivalent. To replay av samme kanoniske logg er en smalere egenskap.

**Anbefalt innføring nå er skårings-v2, ikke lærings-v2:** raw-sortering, visningsskala s=1, egen skåringsversjon/opt-in under migrasjon, uendrede lagrede vekter og Noa. β_forget=0 i produksjonen så lenge læringsforslaget er avvist. Derfor kreves ingen sentreringstilstand nå. Skåringsvalg må være eksplisitte dersom historiske presentasjoner skal kunne gjenskapes.

## S8 — Spørsmål til Vegar

Disse fem spørsmålene leveres til Losen/Kjetil. De er ikke sendt.

1. Hvilket mål skal tilleggsregelen oppfylle utover å rette clamp-rangeringen: et bestemt normbudsjett, selektiv glemsel eller raskere omstilling? Hvilket resultat ville falsifisere at hybriden gjør dette bedre enn dagens regel?
2. For `Δw=.08*x*(1−w)−β*y²*w`: hvilket β-skjema og hvilken stabilitetsbetingelse mener du er riktig når graden og aktivitetsnormen varierer? Våre tette kontroller har verken generell enhetsnorm eller raw≤1.
3. Skal eksplisitte brukerpreferanser inngå i samme konkurransebudsjett og kunne svekkes mens de er fraværende, eller bør de holdes adskilt fra den lærte vekten?
4. Er et ikke-negativt, forklarbart konkurransebudsjett tilstrekkelig for ditt formål, eller er signert, sentrert hovedkomponentlæring nødvendig? Hvilket konkret mål begrunner da den ekstra historikken og endrede vektsemantikken?
5. Skal fraværende kanter svekkes også ved et feilutfall, og i så fall med hvilken positiv konkurranserate? Negativ η i hele Oja snur glemmetermen; dagens feilregel er beholdt i våre forsøk.

## Anbefaling INN/AVVIST

**AVVIST som neste produksjonsregel nå.** Dette avviser ikke aktivitetsdrevet glemsel som forskningsretning. Den målte fordelen i drift står; den kan ikke oppheve tapene i sparse/tette scenarioer, preferansekonflikten og uavklarte preferanse-/legacy-semantikker. INN ville overdrevet hva de syntetiske dataene og den uimplementerte eventkontrakten viser.

Det konkrete neste arbeidet er HD-0051: bevar raw-rekkefølge, innfør en tydelig visningsskala og test konsumentkontrakten. Deretter kan lokal shadow-evaluering av en avgrenset budsjett-/konkurranseregel vurderes på nytt hvis et nytt mål krever den. Kjetil eier beslutningen om kodeendring; Losen/Kjetil eier eventuell oppfølging med Vegar. Ingen ekte journal ble etterspurt fordi syntetiske logger var tilstrekkelig for den avgrensede avvisningen og fordi ingen lokal brukerjournal var utpekt.

## Hva som ikke virket

- Full Oja-arv fra et hybridledd, generell alltid-aktiv dominans og «norm 1 løser score≤1» holdt ikke. Moteksemplene og støttende delresultater er beholdt.
- Sentrert/projisert kandidat reduserte konstant bakgrunn, men slo også ut en alternerende interesse og kunne stoppe læringen ved konstant input. Dette er ikke en demonstrasjon av ønsket PCA i dagens kontrakt.
- Lav norm, lite vektbevegelse og høy temporal tau var ikke pålitelige nytteindikatorer alene. En konstant alfabetisk feilrangering hadde tau 1.
- Første Python-summering og Noa-uttrykksrekkefølge matchet ikke Swift helt. Differensialkontrollen fant forskjellen; begge ble rettet før endelige tall. Set-iterasjon i en metric ble også sortert før leveransen.
- Full SwiftPM-bygging ble stoppet av nested sandbox-exec. De originale motortestene er i stedet kjørt uendret med direkte swiftc/XCTest og begrensede støtteklasser. **Full CellProtocol-pakke og CellApple-integrasjon er ikke verifisert.**
- Flere primærkildehentinger feilet før Sanger ble hentet fra CMU. Tilgjengelighet og faktisk leste kilder er skilt i underlaget.

[AVVIK_OG_FEIL.md](AVVIK_OG_FEIL.md) beskriver metodiske avvik, forsøksfeil og replaybegrensninger i detalj. Første sonderingskjøring og avbrutt kjøring er ikke brukt som sluttbevis. [PREREGISTRERING.md](PREREGISTRERING.md) er beholdt uendret med SHA-256 `fc0b9f5c22b3eac0657fef2b38a4e0402db1791a83e936211b0e5cb1b93ffd9f`.

## Påstandsregnskap og kvalitetskontroll

| ID | Hovedpåstand og evidens | Adjudikasjon |
|---|---|---|
| C1 | Dagens clamp skjuler forskjell mellom reelle råskårer >1; Swift F3 + matrisen | Supported |
| C2 | Additiv hybrid arver norm 1/PCA; motsagt av reglene og tette kontrolltilfeller | Contradicted som generell påstand |
| C3 | Norm 1 sikrer raw≤1; motsagt av √n-kontrollen | Contradicted |
| C4 | Alltid-aktive noder dominerer nødvendigvis; konstant kontroll viser nær like vekter | Contradicted som nødvendighet; bakgrunnsrisiko supported |
| C5 | Samme config/policy og kanonisk replay gir lik målt kanttilstand; 1 152 kjøringer | Supported innen presisert runtime/tilstand |
| C6 | Endret config bevarer gamle lifecycle-logger; native migrasjonsfixtures viser .172→.28 | Contradicted |
| C7 | Glemmeterm gir generell raw-rangeringsforbedring; blandede seedvise resultater | Contradicted innen denne scenariofamilien |
| C8 | Raw-sortering retter clamp-tapet uten vektendring; parvise tegn og dense-mål | Supported; brukernytte utenfor generatoren er ikke fastslått |

Den sterkeste støtten **for** videre konkurransearbeid er driftmålingen og Vegars konkrete fraværsmekanisme. Den sterkeste innvendingen mot å innføre nå er at det identifiserte skåringsproblemet kan løses uten konkurranse, mens konkurransen selv endrer nyttig raw-rekkefølge negativt i flere kontroller. At v2-koden ikke er skrevet er ikke et selvstendig avvisningsargument: dette oppdraget forbød produksjonsendringer. Anbefalingen avgjør implementering nå, ikke alle mulige fremtidige regler. C2, C3 og C7 er analytikerens eksplisitte arbeidshypoteser, ikke garantier sitert fra Vegar. Kilde-/simulatorrevisjon er dokumentert separat; andre adjudikator fikk denne eksplisitte motutfordringen før avslutning.

| Mål Q1–Q10 | Verdi og kontrollerbart grunnlag |
|---|---|
| Q1 Endringsspor | 6 brief-korrigeringer har navngitt kilde eller fixture; ingen korrigering begrunnes med enighet alene |
| Q2 Mot bestillingsretningen | Ingen målratio. Bestillingen belønner beslutningsgrunnlag; 4 positive arbeidshypoteser begrenses eller avkreftes (C2,C3,C4,C7), samtidig beholdes driftfordelen |
| Q3 Kildeaudit | 8/8 hovedpåstander har hentet kode, kjørte kontroller eller primærkilde; universell brukernytte hevdes ikke |
| Q4 Rammeuavhengighet | 8/8 tabellpåstander gjelder navngitt regel/data uavhengig av hvem som foreslo den; anbefalingen er et eksplisitt produktvalg |
| Q5 Falsifiserbarhet | 0 uflaggete «begge utfall støtter»-påstander; kontrollene inkluderer fravær, negative resultater og soft-tie |
| Q6 Kjørte motfaktiske armer | 8/8 regler kjørt på samme 144 logger; all-kant/kun-eligible og raw/clamp er faktisk kjørt |
| Q7 Motiver | Ikke relevant; ingen aktørmotiver eller personkarakteristikker evalueres |
| Q8 Avslutning | 8/8 hovedpåstander adjudikert; produksjonsnytte utenfor syntetiske logger står åpen med Kjetil som beslutningseier |
| Q9 Motstående kilde | Vegars pkt.6 er lest som sterkeste pro-hybrid-kilde; Oja/Sanger er kontrollert, ikke brukt som løs autoritet |
| Q10 Ubegrunnet konsesjon | 0 registrerte; endringene er sporbare til kode, måling eller matematisk moteksempel |

## Verifikasjon, registrering og avgrenset avslutning

De sju numeriske sluttartefaktene matchet manifestet og ble byte-identisk gjenskapt i en ny prosess med Python-hashseed 7841. Originale Swift-tester og differensialfixtures passerte mot de registrerte kildefilene. Tre mål og åtte påstander ble også dekodet med de uendrede Swift wire-typene. Den endelige kvitteringen ligger i [AVSLUTNING.md](AVSLUTNING.md), sammen med HD-hendelser, lessons, loggføring og eventuell git-commit.

Dette materialet hører til CellProtocolDocuments og de lokale HD-oppgavene. UniverseSimulation-arkivet og dets dedikerte RAG-korpus er ikke oppdatert: ingen UniverseSimulation-forskningsrunde er utført, og disse interne programdataene hører ikke i fysikkorpuset. Rapporten er ikke publisert til en ekstern side eller sendt til andre.
