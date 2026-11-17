# Lokal tale til tekst: mlx-whisper på Mac-en

Kjørt 2026-10-09T17:36:58Z av `tools/stt-benchmark/stt_lokal.py`. Klippene er laget med macOS sin egen stemme (`say`), så ingen lyd eller tekst forlot Mac-en.

**Forbehold:** syntetisk tale er renere enn ekte tale ved et bord. Tallene er trolig for gode. Prøvesettet er åtte setninger, så forskjeller på noen få prosentpoeng betyr lite.

Lydlengde totalt: 69.6 s.

| Modell | Klipp ok | Snitt WER | Snitt CER | Kritiske ord | Tid totalt (s) | Sanntidsfaktor | Modell på disk (MB) | Maks minne (MB) | Første kall inkl. nedlasting (s) | Feil |
|---|---|---|---|---|---|---|---|---|---|---|
| lokal:mlx-community/whisper-tiny-mlx | 8/8 | 74.0 % | 28.8 % | 3/39 | 5.0 | 0.07 | 74.0 | 433.0 | 9.1 | - |
| lokal:mlx-community/whisper-base-mlx | 8/8 | 52.9 % | 16.6 % | 11/39 | 2.7 | 0.04 | 144.0 | 509.0 | 12.1 | - |
| lokal:mlx-community/whisper-small-mlx | 8/8 | 32.6 % | 13.5 % | 15/39 | 4.5 | 0.07 | 481.0 | 816.0 | 20.1 | - |
| lokal:mlx-community/whisper-large-v3-turbo | 8/8 | 17.3 % | 8.5 % | 26/39 | 10.1 | 0.14 | 1614.0 | 1361.0 | 59.6 | - |

Sanntidsfaktor under 1 betyr raskere enn sanntid.

## Per klipp

### k01-bestilling-allergi (stemme Nora, 10.5 s)

Fasit: Hei, vi er fire personer til bord tolv klokka halv åtte. En av oss har alvorlig sesamallergi, og en er gravid, så ingen rå fisk eller upasteurisert ost.

| Modell | WER | Bom på kritiske ord | Transkripsjon |
|---|---|---|---|
| lokal:mlx-community/whisper-tiny-mlx | 71.4 % | fire, tolv, halv åtte, sesamallergi, rå fisk, upasteurisert | Hei, vi har fyrepåsundet i bult hokloka halvrotte, en av oss har albo olisessamalerg i, og en aggravid, så ingen rofisk eller røpast av risert oss. |
| lokal:mlx-community/whisper-base-mlx | 57.1 % | tolv, halv åtte, sesamallergi, rå fisk, upasteurisert | Hej, vi har fire personer til buthold klocka halvåttet, en av oss har albollige sesamalergi, og en agravid, så ingen råfiskeller vi pasta i setost. |
| lokal:mlx-community/whisper-small-mlx | 32.1 % | tolv, halv åtte, sesamallergi, upasteurisert | Hei, vi er fire personer tilbord hva hva hva halvåte. En av oss har alvorlig sesam allergi, og en er gravid, så ingen rå fisk eller upasteriseret ost. |
| lokal:mlx-community/whisper-large-v3-turbo | 7.1 % | tolv, upasteurisert | Hei, vi er fire personer til bord 12 klokka halv åtte. En av oss har alvorlig sesamallergi, og en er gravid, så ingen rå fisk eller upasterisert ost. |

### k02-vin-og-retter (stemme Nora, 9.68 s)

Fasit: Kan vi få en flaske Etna Rosso fra 2019 og to glass Grillo til forretten? Så tar vi arancini, caponata og busiate med pistasj.

| Modell | WER | Bom på kritiske ord | Transkripsjon |
|---|---|---|---|
| lokal:mlx-community/whisper-tiny-mlx | 75.0 % | etna rosso, 2019, grillo, arancini, caponata, busiate, pistasj | Kan vi få en flasket er enn arosofrat 2021 og nitten opp på glaske rilotiforetten? Så tar vi er ansinier, kabel natar og busig at det med pistas. |
| lokal:mlx-community/whisper-base-mlx | 62.5 % | etna rosso, 2019, grillo, arancini, caponata, busiate, pistasj | Kan vi få en flaske ettena i rossoffra 2000 og 1982 glaske i Lotte i Foretten, så tar vi Aransini, Kaponata og Busi Atemepistas. |
| lokal:mlx-community/whisper-small-mlx | 29.2 % | etna rosso, grillo, arancini, busiate | Kan vi få en flaske etnar også fra 2019 og to glass, relativt for etten? Så tar vi Aransini, Caponata og Busiata med pistasj. |
| lokal:mlx-community/whisper-large-v3-turbo | 16.7 % | etna rosso | Kan vi få en flaske etnar også fra 2019 og to glassgrillo til forretten, så tar vi arancini, caponata og busiate med pistasj. |

### k03-moetevedtak (stemme Nora, 9.91 s)

Fasit: Da er vi enige. Henrik sender term sheetet innen fredag, Isabella går gjennom due diligence-rapporten, og vi møtes igjen den fjortende november.

| Modell | WER | Bom på kritiske ord | Transkripsjon |
|---|---|---|---|
| lokal:mlx-community/whisper-tiny-mlx | 91.3 % | henrik, term sheet, fredag, isabella, due diligence, fjortende november | Da vi er nere, hendrig senet færmersjeetet hinsredag, i så belag går jeg noen byld i lisjonser rapporten, og vi møte sig gjennens jotenen noen vember. |
| lokal:mlx-community/whisper-base-mlx | 65.2 % | term sheet, isabella, due diligence, fjortende november | Da er vi enige, Henrik Sennertfarmskjætet innfredag, i Sabelagår i en ombyen i Lyshanserapotten, og vi möte seg jenden 14 november. |
| lokal:mlx-community/whisper-small-mlx | 43.5 % | term sheet, due diligence, fjortende november | Da er vi igjen, ja. Henrik Senert-Ferm skjetet inn fredag, Isabella går gjennom duet dele chanserapporten, og vi møtes igjen den 14. november. |
| lokal:mlx-community/whisper-large-v3-turbo | 26.1 % | term sheet, due diligence, fjortende november | Da er vi enige. Henrik sender tverm skjetet inn fredag, Isabella går gjennom Bue Dilijanser-rapporten, og vi møtes igjen den 14. november. |

### k04-tall (stemme Nora, 9.66 s)

Fasit: Verdsettelsen landet på hundre og tjue millioner kroner før pengene, med en opsjonspool på ti prosent og en likvidasjonspreferanse på én gang.

| Modell | WER | Bom på kritiske ord | Transkripsjon |
|---|---|---|---|
| lokal:mlx-community/whisper-tiny-mlx | 68.2 % | hundre og tjue millioner, ti prosent, opsjonspool, likvidasjonspreferanse | Verbjetelsen langet på føndre 7.000 kr. f. h. men en options spul på ti prusent og en likvidationspreferangse på en gang. |
| lokal:mlx-community/whisper-base-mlx | 45.5 % | hundre og tjue millioner, ti prosent, opsjonspool, likvidasjonspreferanse | Verbsjettelsen landet på 120 millioner kroner før pengene, med en optionspul på 10 % og en likvidarsjons preferanse på en gang. |
| lokal:mlx-community/whisper-small-mlx | 31.8 % | hundre og tjue millioner, ti prosent, opsjonspool | Verbskjettelsen landet på 120 millioner kroner før pengene, med en opjonsbull på 10% og en likvidasjonspreferanse på én gang. |
| lokal:mlx-community/whisper-large-v3-turbo | 36.4 % | hundre og tjue millioner, ti prosent, opsjonspool | Verbskjettelsen landet på 120 millioner kroner før pengene, med en opsjonspul på 10% og en likvidasjonspreferanse på en gang. |

### k05-engelsk-allergi (stemme Samantha, 6.01 s)

Fasit: I'm severely allergic to sesame and tree nuts. Could the kitchen please confirm that the sauce is safe for me?

| Modell | WER | Bom på kritiske ord | Transkripsjon |
|---|---|---|---|
| lokal:mlx-community/whisper-tiny-mlx | 4.8 % | tree nuts | I'm severely allergic to sesame and tree knots. Could the kitchen please confirm that the sauce is safe for me? |
| lokal:mlx-community/whisper-base-mlx | 0.0 % | - | I'm severely allergic to sesame and tree nuts. Could the kitchen please confirm that the sauce is safe for me? |
| lokal:mlx-community/whisper-small-mlx | 0.0 % | - | I'm severely allergic to sesame and tree nuts. Could the kitchen please confirm that the sauce is safe for me? |
| lokal:mlx-community/whisper-large-v3-turbo | 0.0 % | - | I'm severely allergic to sesame and tree nuts. Could the kitchen please confirm that the sauce is safe for me? |

### k06-vaktnotat (stemme Nora, 7.1 s)

Fasit: Bord sju feirer forlovelse. Ikke nevn jobben hans, og husk at hun uttaler etternavnet Vessel, ikke Wessel.

| Modell | WER | Bom på kritiske ord | Transkripsjon |
|---|---|---|---|
| lokal:mlx-community/whisper-tiny-mlx | 82.3 % | bord sju, forlovelse, vessel | Borsiøfairer for lovelse, ikkende vi jobben hans, og husk og tunn utal er etter navnne vesul, ikke vesul. |
| lokal:mlx-community/whisper-base-mlx | 76.5 % | bord sju, forlovelse | Borsju feire for lovelse, ikke nøvn jobbenhands, og huskat hun utaler etter navne vessel, ikke vessel. |
| lokal:mlx-community/whisper-small-mlx | 47.1 % | bord sju, forlovelse, vessel | bor sju feire for lovelse, ikke nevn i jobben hans, og husk at hun uttaler etternagende vesul, ikke vesul. |
| lokal:mlx-community/whisper-large-v3-turbo | 29.4 % | bord sju | Bo Sy feirer forlovelse, ikke nevn jobben hans, og husk at hun uttaler etter nagne Vessel, ikke Vessel. |

### k07-styreprotokoll (stemme Nora, 7.96 s)

Fasit: Styret ber om at protokollen fra møtet trettiende oktober signeres elektronisk med BankID før generalforsamlingen.

| Modell | WER | Bom på kritiske ord | Transkripsjon |
|---|---|---|---|
| lokal:mlx-community/whisper-tiny-mlx | 113.3 % | protokollen, trettiende oktober, bankid, generalforsamlingen | Styrbebern At Fro'tokolen fra Møte everyday nakento å berce nieres elektronisk med banke edel fungeren everyday for fungerningen. |
| lokal:mlx-community/whisper-base-mlx | 73.3 % | trettiende oktober, generalforsamlingen | Styrer beroen at protokollen framøter 30 og 2 ber singnere selektronisk med bankID før generalforskampningen. |
| lokal:mlx-community/whisper-small-mlx | 53.3 % | trettiende oktober, bankid, generalforsamlingen | Styrer Bæron at protokollen fra møte 13. oktober signeres elektronisk med bank IDFørgjeneralforsamlingen. |
| lokal:mlx-community/whisper-large-v3-turbo | 13.3 % | trettiende oktober | Styret ber om at protokollen fra møte 30. oktober signeres elektronisk med BankID før generalforsamlingen. |

### k08-idemoete (stemme Nora, 8.74 s)

Fasit: Hva om premieren starter i foajeen, og publikum følger skuespillerne opp trappen til Chambre, der middagen er en del av forestillingen?

| Modell | WER | Bom på kritiske ord | Transkripsjon |
|---|---|---|---|
| lokal:mlx-community/whisper-tiny-mlx | 85.7 % | premieren, foajeen, skuespillerne, chambre, forestillingen | Bå om primi anstorter i fvaien, opplikken føler skøsbilene opptropen til Schambra, da er med doggen her endel av forstillingen. |
| lokal:mlx-community/whisper-base-mlx | 42.9 % | premieren, foajeen, skuespillerne, chambre | Hva om premieen starter i fjelene, og publikum føler skjuspillene opptrappen til Shambra, der midagen her en del av forestillingen? |
| lokal:mlx-community/whisper-small-mlx | 23.8 % | premieren, foajeen, skuespillerne, chambre | Hva om Premiand starter i få Aegeen, og publikum følger skuspillende opp trappen til Sjambre, der middagen er en del av forestillingen? |
| lokal:mlx-community/whisper-large-v3-turbo | 9.5 % | foajeen, chambre | Hva om premieren starter i foieen, og publikum følger skuespillerne opp trappen til sjambre, der middagen er en del av forestillingen. |

