# Uavhengig litteraturrevisjon — 2026-09-12

Rolle: kildeauditør og skeptiker under haven-panel-task-decomposition. Dette er et underlagsnotat; hovedkonklusjon om innføring avventer målinger og andre adjudikasjon. Ingen CellProtocol-kode er endret. HANDOFF.md, Vegar_svar_2026-09-09.md, deepresearch-prompten og den nåværende RelationalDecayPolicy.swift er faktisk lest.

## Brief audit

1. **F4 må korrigeres.** Usentrert input gir andre moment `E[xxᵀ] = Cov(x)+μμᵀ`, ikke generelt «retningen med størst rå gjennomsnitt». En alltid-aktiv kontekst er en mulig konfunder, men dominerer ikke nødvendigvis alle andre komponenter. Kildeankeret er Oja §3, s.269–270. Dette er en brief-feil som må få en synlig korreksjon: konklusjoner om sikker dominans faller; behovet for en målt kontroll står.
2. **Tilleggsforslaget er ikke hele Ojas regel.** Dagens suksessledd `a*x*(1−w)` pluss `−b*y²*w` er en hybrid. Ojas norm- og PCA-resultater kan ikke flyttes til den uten en egen utledning. Enhetsnorm er derfor et åpent målespørsmål for hybriden, ingen premiss.
3. **Hard clamp på y kan bryte normpåstanden**, også når resten av oppdateringen er ekte Oja. Et eksplisitt moteksempel er gitt nedenfor. «Svak ikke-linearitet» er ikke nok som implementasjonskontrakt når mange samtidige kanter gir raw > 1.
4. **Aktivitetsdrevet glemsel krever definert fravær.** Når et formål er aktivt og andre kanter driver y, må den fraværende kjente kanten inngå med x_i=0. Bare oppdatering av kanter i dagens eligibility-liste kan ikke realisere den foreslåtte konkurranseglemselen.
5. **F3 handler også om skåringens informasjonsødeleggelse.** En streng monoton transformasjon av raw kan fjerne clamp-ties uten at læring er forbedret. S6 og læringskandidaten må bedømmes separat; ikke bruk redusert metning som eneste evidens for bedre relasjonslæring.

## Faktisk hentede primærkilder og kildegrenser

### Oja 1982

[Oja, A Simplified Neuron Model as a Principal Component Analyzer](https://neurophysics.ucsd.edu/courses/physics_171/Oja_1982.pdf), Journal of Mathematical Biology 15, 267–273; DOI 10.1007/BF00275687. Status: **retrieved**, alle syv PDF-sider tilgjengelig via web-verktøyets fulltekst; ligningssidene 268 og 270 også åpnet som skjermbilder. Lokal curl-kopi feilet på DNS; ingen PDF-hash hevdes.

Kildesammendrag: S.268, lign.(2–3), utleder Oja som førsteordensapproksimasjon til normalisert Hebb for liten læringsrate. S.269, lign.(4–8), bruker lineær y og C=E[xxᵀ]. S.270 skiller maksimal varians ved nullmiddel fra maksimalt kvadratisk middel ved ikke-nullmiddel. Teoremet gjelder den gjennomsnittlige differensialligningen med enkel største egenverdi og initial projeksjon; den stokastiske koblingen forutsetter egne regularitets- og rateskjema-antakelser. Konstant liten rate beskrives som approksimasjon når fluktuasjoner neglisjeres. S.269 sier norm nær én, ikke eksakt én etter hvert diskret steg. Dette gir ingen generell garanti for hard-clamp, per-kant [0,1]-projeksjon, negativ reward-rate, drift eller vår hybrid.

### Sanger 1989 / GHA

[Sanger, Optimal Unsupervised Learning in a Single-Layer Linear Feedforward Neural Network](https://www.cs.cmu.edu/~bhiksha/courses/deeplearning/Fall.2016/pdfs/Sanger.pdf), Neural Networks 2(6), 459–473. [Utgiver/DOI](https://doi.org/10.1016/0893-6080(89)90044-0). Status: **retrieved**, full PDF lastet via curl og tekstuttrukket med pypdf; særlig §§1–5 lest, s.460–461 visuelt kontrollert. Nettleserhenting hadde timeout; utgiverens direkte side ga 403. Det er ikke en fulltekstblokkering etter at CMU-kopien lyktes. Lokal PDF `/tmp/Sanger_1989.pdf`; SHA-256 `3466afc26136cfe6f3d2f83ce8db2ec891baaa820c1f45905701106283666c3f`. Tekst `/tmp/Sanger_1989.txt`.

Kildesammendrag: S.460 lign.(1–2) gir GHA `ΔC=η(yxᵀ−LT[yyᵀ]C)`, lineær y=Cx og stasjonær inputprosess. S.461–463 behandler betinget konvergens og bruker blant annet avtakende positiv rate, bounded input og en stabil differensialligning. S.463 §3 forutsetter nullmiddel for rekonstruksjons/PCA-tolkningen. S.464–465 forklarer utvidelsen med ortogonalisering; lokal realisering på s.465 lign.(13–14) bruker input modifisert av tidligere utganger. Uavhengige formål med hver sin Oja-oppdatering er derfor ingen GHA-implementasjon eller garanti for ulike komponenter.

### Supplerende primærkilde om ikke-linearitet

[Sanger, An Optimality Principle for Unsupervised Learning, NeurIPS 1988, s.11–19](https://proceedings.neurips.cc/paper_files/paper/1988/file/e00da03b685a0dd18fb6a08af0923de0-Paper.pdf). Status **retrieved**, fulltekst ni sider. S.12 lign.(1) gjengir lineær GHA. S.14 lign.(2) diskuterer bestemte ikke-lineariteter, og s.18 sier konvergens bare er bevist for det lineære tilfellet; erfaringene gjelder bestemte eksempler. Dette støtter forsiktighet, ikke et generelt negativt resultat for enhver ikke-linearitet.

## Egne matematiske kontroller (ikke empiriske brukerresultater)

Notasjon: `r=Σ_i w_i x_i`, `y=r` eller `clamp01(r)`. Beregn alle endringer fra **samme pre-episode-vektor** og samme y, før noen vekt muteres.

| Regel | Suksessoppdatering før eventuell kantclamp | Hva som faktisk er regulert |
|---|---|---|
| Dagens | `w_i+a*x_i*(1−w_i)` | Hver kant nærmer seg 1 separat |
| Foreslått hybrid | `w_i+a*x_i*(1−w_i)−b*y²*w_i` | Må måles; ikke Ojas invariant |
| Ekte Oja som referanse | `w_i+η*y*(x_i−y*w_i)` | Betinget Oja-approksimasjon ved lineær y |
| Budsjettkontroll | Først dagens steg, deretter eksempelvis `w←w/max(1,||w||₂/B)` | Eksplisitt normtak B; ingen PCA-påstand |

For n identiske kontinuerlig aktive input, x_i=1 og symmetriske vekter w_i=w:

- Ekte Oja, raw: den positive likevekten løser `1−n*w²=0`; `w=1/√n`, norm 1, men **raw=√n**. Enhetsnorm kan altså fortsatt mette score-clamp. Cauchy–Schwarz gir generelt `r≤||w||₂||x||₂≤√n` når norm 1 og x_i∈[0,1]. Dette er en øvre grense, ikke en sammenlignbar kalibrering mellom alle formål.
- Ekte Oja, clamped y=1: `Δw=η(1−w)`; w→1, norm→√n, raw→n. Et enkelt konkret moteksempel mot at output-clamp bevarer enhetsnorm.
- Hybrid, clamped y=1: `Δw=a(1−w)−bw`; positiv likevekt `w*=a/(a+b)`, raw*=n*a/(a+b), forutsatt at den ligger i clamp-regimet.
- Hybrid, raw: likevekten løser `a(1−w)=b*n²*w³`. Ingen generell norm 1; en målt bounded vektsekvens etablerer heller ikke en universell stabilitetspåstand.
- Hele x=0 gir raw y=0 og intet aktivitetsledd. Bare x_i=0 mens y>0 gir `w'_i=(1−b*y²)w_i` for hybriden. For å unngå fortegnsflipp før kantclamp trengs `b*y²≤1` for en fraværende kant; dette er ikke i seg selv et tilstrekkelig globalt stabilitetskriterium.
- Negativ η i hele Oja snur også glemmetermen: en fraværende kant kan vokse ved negativt utfall. En feilregel må derfor defineres eksplisitt og ikke arve en positiv-rate-konvergenspåstand.

`raw/(s+raw)` med s>0 har derivert `s/(s+raw)²>0` og bevarer matematisk raw-rekkefølge. Den gir ingen ny rangeringsevidens sammenlignet med raw; finite precision kan fortsatt produsere ties ved ekstreme verdier. Rank på raw, transformer for visning. Per-formål nevner som avhenger av grad eller inputnorm kan endre rekkefølgen og er et annet produktvalg.

## Sentrering og aktivitet

En positiv inputvektor som aldri sentreres kan fremdeles være nyttig for anbefaling; det er PCA-tolkningen og risikoen for bakgrunnsretninger som må skilles fra produktmålet. Kjør ingen-sentrering og kontroll med en alltid-aktiv node. Glidende gjennomsnitt må være deterministisk og replaybart, med window/version, warmup, fraværsdefinisjon og oppdateringsrekkefølge. Sentrerte x kan bli negative. Å bruke dem i dagens positive eligibility-kontrakt og samtidig tvinge vekter til [0,1] er ikke klassisk Oja; det er enda en modifisert algoritme. Budsjettvarianten er derfor en enklere avgrenset produktkontroll, men har ikke automatisk best anbefalingskvalitet.

Velg lagrede vekter til lærings-y hvis formålet er å holde aktivitets- og tidslaget atskilt. Effektive vekter kan også være deterministiske hvis tidspunkt og policy er logget og entydig; «tid inngår» betyr ikke automatisk ikke-determinisme. Kostnaden er tettere kobling mellom policyer.

Ved ren konkurransesvekkelse på fraværende kanter bør `lastReinforcedAt` bevares. Hvis den nullstilles ved slike steg, fornyer aktivitet uten støtte Noa-retensjonen og kan motvirke glemselen. Dette er en nødvendig eksplisitt v2-semantikk, ikke noe litteraturen avgjør for CellProtocol.

## Decayfamilier — kvalitativ sammenligning, Noa beholdes

Felles vurdering: Alle fire kan beregnes lokalt og deterministisk fra logget policy, timestamp og kanttid. Ingen trenger mer persondata bare på grunn av kurveformen. Det er inputlogging og explain-felt som bestemmer personvernet. Ingen kilder eller syntetiske scenarier her fastslår hvilken kurve som best beskriver menneskelig rutinekontekst.

| Familie | Slow → fast → slow og begrensning | Explain/replay | Beslutning nå |
|---|---|---|---|
| Eksisterende Noa dobbel sigmoid | Produkt av to normaliserte sigmoider, pluss gulv. Flere tidsskalaer; form bestemmes av parametre. Navnet alene beviser ikke et bestemt forløp. | Allerede versjonert i kode. Fem parametre må forklares som policyvalg. | Behold uendret for isolering av læringsspørsmålet. |
| Stykkevis eksponentiell | Egne positive hazards per tidssegment kan konstruere lav–høy–lav relativ reduksjon. Kontinuitet krever akkumulert hazard, ikke restart av vekten ved hvert knekkpunkt. | Enkle segmentforklaringer, men flere knekkpunkter å versjonere. | Alternativ for senere kalibrering; ikke innført. |
| Weibull | `R=exp(−(t/λ)^k)`. For k>1 kan absolutt fallrate begynne nær null, øke, og falle mot null; hazard stiger monotont. Derfor må «slow» defineres: absolutt fall eller relativ hazard. | To parametre, glatt og deterministisk. | Ingen empirisk grunn her for å bytte. |
| Forskjøvet potenslov | `R=(1+t/τ)^−p`. Absolutt og relativ fallrate synker for positive τ,p. Gir lang hale, men ingen innledende akselerasjon uten ekstra struktur. | To parametre; lang hale må forklares. | Kvalitativ kontroll, ikke påstand om menneskelig glemsel. |

Formelgrunnlag: [NIST/SEMATECH, Exponential Distribution §1.3.6.6.7](https://www.itl.nist.gov/div898/handbook/eda/section3/eda3667.htm) angir survival `exp(−t/β)` og konstant hazard; stykkevis-utvidelsen over er vårt designresonnement. [NIST/SEMATECH, Weibull Distribution §1.3.6.6.8](https://www.itl.nist.gov/div898/handbook/eda/section3/eda3668.htm) angir survival og hazard; forskjellen mellom absolutt helning og hazard ovenfor er matematisk utledet. Begge sider er faktisk hentet. Potenslovraden er direkte matematisk funksjonsanalyse, uten empirisk hukommelsespåstand. Noa-raden bygger på lokalt lest implementasjon, ikke en ekstern psykologisk kilde.

## Hva som ikke virket og hva som står åpent

- CMU PDF via web.open ga timeout to ganger, men samme offentlige URL lyktes via curl (15 sider). Dette er løst; ikke rapporter Sanger som ulest.
- Utgiverens Sanger-side ga 403 ved direkte åpning; bare søkeresultatets abstract var tilgjengelig der. CMU-kopien er den faktiske fulltekstkilden.
- En annen Sanger-avhandlingskopi ga 502; den ble ikke brukt.
- `pdftotext` var ikke installert i standardshell. Bundlet Python/pypdf ga tekst, og pdfplumber ga visuelt kontrollerte ligningssider. Ingen pakker installert.
- Lokal Oja-PDF-kopi feilet på DNS; web-fulltekst ble lest. Ingen oppdiktet lokal source-hash.
- Ingen målinger av reelle brukerpreferanser eller langsiktig produktnytte foreligger i dette delnotatet. Null- og positivreferanser må komme fra simulatoren før gate, og endelig anbefaling må avgrenses til det målingene støtter.

## Foreløpig adjudikasjon

- Påstand «additiv glemmeterm arver Ojas enhetsnorm/PCA»: **kontradiktert som generell påstand**, med regelulikhet og konkrete likevekter.
- Påstand «positivt gjennomsnitt kan prege usentrert læring»: **støttet**, men universell alltid-aktiv dominans er **ikke støttet**.
- Påstand «Noa og aktivitetsglemsel kan holdes atskilt og replaybare»: **plausibel designpåstand**, må kontrolleres mot event-kontrakt og målt replay; litteraturen beviser ikke programsemantikken.
- Påstand «hybriden bør inn i produktet»: **åpen**, eier hovedtråden/Kjetil; avventer samme-logg-målinger og eksplisitt andre-adjudikasjon.
