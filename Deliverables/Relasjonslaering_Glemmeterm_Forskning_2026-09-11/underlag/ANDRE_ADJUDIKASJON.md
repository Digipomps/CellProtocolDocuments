# Andre adjudikasjon — utfordret avvisning av glemmeterm

Dato: 2026-09-12. Rolle: uavhengig kildeauditør og utfordret adjudikator B. Ingen rapport- eller kodefiler endret. Lest: `/tmp/relational-study/RAPPORT.md`, `PREREGISTRERING.md`, `underlag/SIMULATORREVISJON.md`, `aggregate.json`, aktuelle `seed_metrics.json` og de relevante måle-/aggregeringsfunksjonene i `study.py`. Primærkildene Oja/Sanger og Vegars pkt.6 var lest i første audit. Alle syv datafilhasher i resultatmanifestet stemte ved denne kontrollen. Dette notatet innebærer ikke en ny full matrise-, Swift- eller deploykjøring.

## Brief audit

1. Utfordringen gjengir drift-, sparse- og dense-tallene korrekt. n=6 preference_change er også korrekt: raw-treff .7270833→.8562500 ved hybrid raw .02, og 8/8 seeds vinner. Dette positive resultatet mangler foreløpig i rapportens hovedtekst, som konsentrerer trefftabellene om n=20.
2. Det sterkeste positive parameterargumentet er enda bedre enn utfordringen: β=.005 gir n=20 drift .8972222→.9680556 (7 seire, 0 tap, 1 likt), og preference_change .7486111→.8701389 (8 seire, 0 tap). Dette reduserer ikke avvisningen til feil, men hindrer at β=.02 brukes som stand-in for hele familien.
3. «Manglende produksjonsmigrasjon» må ikke bety manglende implementasjon som selvstendig avvisningsgrunn. Oppdraget forbød produksjonskodeendring; INN skulle være en forskningsanbefaling med parametre og migreringsplan. Det relevante åpne problemet er uavklart historisk policy-/legacy-konfigurasjon og produktsemantikk, ikke at denne avgrensede oppgaven lot være å implementere planen.
4. Tidligere brief-korreksjoner er synlige og saklige: ikke-eksisterende kanter skårer ikke; sum av ti 0.1 i Swift er ikke eksakt 1; andre moment er ikke bare middel; hybriden arver ikke Ojas invariant. Ingen av disse korreksjonene fjerner den påviste clamp-feilen for faktisk opprettede kanter.

## Eksplisitt avgjørelse av utfordringen

**AVVIST SOM GENERELL PRODUKSJONSSTANDARD NÅ er forsvarlig, med presiseringene nedenfor. En generell avvisning av aktivitetsdrevet konkurranse ville ikke være forsvarlig.**

Motargumentet vinner på ett viktig punkt: det finnes **reelle retningsendringer utover monoton omskalering**, og noen er gunstige etter simulatorens fasit. Ved n=20 drift går β=.02 fra 89.72 til 92.15 % raw-treff; stabil ny topp går fra median 21.5 til 1.5 intervaller, med null sensurering i begge grupper. Ved n=6 preference_change går raw-treff fra 72.71 til 85.63 %, åtte av åtte seeds vinner, og stabil median faller fra 51.5 til 25.0, også med null sensurering. Dette er ikke bare en lavere norm eller en transformert skår. Vegars pkt.6 gir dessuten et konkret, riktig representert mekanisk argument for selektiv glemsel når andre kanter aktiverer formålet. Fraværsablasjonen støtter at denne mekanismen faktisk er implementert i forsøket.

Avvisningen står fordi dette ikke avgjør avveiningen for en **felles standard**: samme β=.02 taper raw-treff i samtlige seeds i n=20 sparse (90.69→86.81 %) og dense (97.64→82.15 %), og flere scenarioer har motgående effekter. Den mildere β=.005 har bedre driftgevinst, men fortsatt små sparse-tap (90.69→90.07; 0/4/4) og dense-tap (97.64→94.17; 0/7/1). Rapporten definerer ingen dokumentert bruker- eller produktfordeling som begrunner at disse tapene skal kjøpes for driftgevinsten. Ingen av disse fortegnene er et estimat av en faktisk brukerpopulasjon.

Det er dermed rimelig å rette den målte clamp-feilen separat og beholde konkurranse som en åpen, målrettet kandidat. Det ville være urimelig å skrive at manglende generell dominans beviser at gevinsten er verdiløs, eller at enhver avgrenset driftspolicy må avvises. Adjudikasjonen er en konservativ produktanbefaling under de deklarerte målene, ikke et statistisk teorem om at dagens regel er best.

## Tidligere konklusjoner: faller, står, eller begrenses

| Tidlig konklusjon | Avgjørelse etter korrigert brief og målte data |
|---|---|
| Usentrert Oja finner bare retningen med størst middel; alltid-aktiv node må dominere | **Faller som generell påstand.** Andre moment er korrekt mål; risikoen for bakgrunnskomponenter står. |
| Seks opprettede kanter etter én suksess gir clamp-metning | **Står.** F3 er runtimebekreftet. Påstanden om ti ikke-opprettede/lagrede .1-kanter som eksakt startmetning faller i de presiserte tilfellene. |
| Additiv glemmeterm arver Ojas norm/PCA | **Faller.** Regelulikhet og kontrollikevekter gir motbelegg. |
| Norm 1 løser raw≤1 | **Faller.** √n-kontrollen står. |
| Konkurranse på fraværende kanter kan svekke dem ved aktivitet i andre kanter | **Står innen implementert kontroll.** Krever at fraværende kjente kanter besøkes og at alderen ikke fornyes ved konkurranse alene. |
| Hybrid gir ingen læringsfordel utover skåringsfiks | **Ville falle.** Den påstanden bør ikke forekomme: drift- og preferansescenarioene viser retningsgevinster. Rapporten erkjenner allerede driftgevinsten; synliggjør også den sterkeste preferansegevinsten. |
| Hybrid bør bli generell standard nå | **Ikke etablert.** Målte fordeler og ulemper krever produktavveining; anbefaling AVVIST nå står. |

## Kun handlingsrettede rettelser før levering

1. **Legg inn de sterkeste pro-resultatene i hovedteksten.** Etter S2-resultatavsnittet: n=6 preference_change β=.02, 72.71→85.63 %, 8/8 seier, stabil median 51.5→25.0 og 0/8 sensurering. Nevn også n=20 β=.005 drift 96.81 % og preference_change 87.01 % mot henholdsvis 89.72/74.86 baseline. Dette krever ingen ny kjøring; tallene finnes i bevarte aggregater. Ikke gi alle positive funn bare som datafil som få lesere vil åpne.
2. **Bytt avvisningsgrunn fra «uimplementert» til «uavklart».** I anbefalingsavsnittet og S7: si at ingen felles nytteavveining eller ferdig fastlagt legacy-/preferansekontrakt er besluttet. Ikke argumenter med at oppdraget ikke implementerte kode. Skillet mellom en forskningsanbefaling INN og faktisk produksjonspromotion må stå klart. Behold at ekte brukernytte ennå ikke er fastslått.
3. **Presiser utvalget og nevnerne.** S2 «Parametersjekk»-tabellen gjelder n=20; skriv det i tittelen. Raw-treffandelene gjelder alle 180 spørringer, ikke bare de 90 etter byttet. Stable latency er starten på første blokk med ti riktige topper og er retrospektivt bekreftet av de ni neste observasjonene. Ikke presenter den som tid til bekreftet stabilitet uten dette skillet.
4. **Presiser sensurkolonnene og tau-formuleringen.** «Raw sensurert /8» og «Clamp sensurert /8» er sensurering for **stabil** topp. Rename slik; første topp har egen observasjonsmengde. Særlig preference_change n=20 β=.02 har to stabile bytter som aldri observeres; 28.0 observerte mot 40.5 med ingen sensurerte er ikke alene en ubetinget medianforbedring. Tau-/margin-/fortegns-nullfylling er allerede eksplisitt dokumentert og trenger ingen ny analyse. Bytt «Tau-b for en helt lik skårvektor» til «Tau-b er udefinert når en sammenlignet skårvektor bare inneholder ties» for å unngå forveksling med to identiske, ikke-konstante vektorer som har tau 1.
5. **Bevar kandidatskillet i betegnelsene.** «Oja-suksess» er riktig brukt i resultatdelen og begrensningen er tydelig. «Ekte raw-Oja» ved den analytiske success-only-kontrollen i S1 er akseptabelt fordi det gjelder selve ligningen. Den uendrede preregistreringen kan beholde sitt opprinnelige «ekte Oja raw», men avviksnotatet bør markere at den hele kandidaten også har baseline-feil, preferanser, featurevekst og [0,1]-projeksjon. Ingen endring i låst preregistrering.
6. **Lukk leveransestatus med faktisk kvittering.** `AVSLUTNING.md` eksisterte ikke ved denne revisjonen, selv om siste avsnitt lenker til den. Før sluttmelding må kvitteringen finnes og presist skille forskningsfiler, verifisering, HD-noter/lessons, logg og eventuell commit/push med status. Eierskapet i CellProtocolDocuments, ikke bare fravær av fysikkpåstander, er begrunnelsen for at denne leveransen ikke er en UniverseSimulation-arkiv/RAG-runde. Ikke skriv at alle avslutningsledd er utført før dette er dokumentert.

## Kilde- og omfangskontroll uten nye rettingskrav

Oja/Sanger brukes med konkrete sider og forutsetninger; de bærer ikke simulatorens nyttepåstander. Egne likevektsutledninger er navngitt som egne matematiske kontroller. Ingen lengre tekstsitat eller full artikkelkopi finnes blant rapportvedleggene jeg så; Sanger-PDF ligger bare som lokal kildekopi i /tmp. Kildeutlegningen er kort, mens rapportens lengde kommer fra egen kode, data og designvurdering. Ingen korrigerbar kilde-/sitatoverskridelse identifisert i denne gjennomgangen.

Tau-padding og høyresensurering er synliggjort og svekker ikke den usensurerte driftutfordringen. Python-replay beskrives som kant-/sentreringstilstand og kantprojeksjon, ikke som ferdig v2-event-sourcing. Swift-paritetens og direkte byggingens begrensninger er tydelige. Disse forbeholdene skal beholdes; en bestått datafilhashkontroll er ikke bevis for de utestede produksjonskontraktene.
