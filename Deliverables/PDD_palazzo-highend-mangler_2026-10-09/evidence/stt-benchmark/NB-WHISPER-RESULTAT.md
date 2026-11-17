# Lokal tale til tekst: mlx-whisper på Mac-en

Kjørt 2026-10-09T18:05:09Z av `tools/stt-benchmark/stt_lokal.py`. Klippene er laget med macOS sin egen stemme (`say`), så ingen lyd eller tekst forlot Mac-en.

**Forbehold:** syntetisk tale er renere enn ekte tale ved et bord. Tallene er trolig for gode. Prøvesettet er åtte setninger, så forskjeller på noen få prosentpoeng betyr lite.

Lydlengde totalt: 69.6 s.

| Modell | Klipp ok | Snitt WER | Snitt CER | Kritiske ord | Tid totalt (s) | Sanntidsfaktor | Modell på disk (MB) | Maks minne (MB) | Første kall inkl. nedlasting (s) | Feil |
|---|---|---|---|---|---|---|---|---|---|---|
| lokal:mlx-community/whisper-large-v3-turbo | 8/8 | 17.3 % | 8.5 % | 26/39 | 9.3 | 0.13 | 1614.0 | 1819.0 | 2.5 | - |
| lokal:nb-whisper-small-f16 | 8/8 | 23.3 % | 13.4 % | 21/39 | 3.7 | 0.05 | 481.0 | 697.0 | 1.0 | - |
| lokal:nb-whisper-medium-f16 | 8/8 | 17.3 % | 13.3 % | 26/39 | 9.9 | 0.14 | 1525.0 | 1737.0 | 2.2 | - |
| lokal:nb-whisper-large-f16 | 8/8 | 14.7 % | 10.2 % | 27/39 | 17.9 | 0.26 | 3083.0 | 2962.0 | 4.1 | - |
| lokal:nb-whisper-large-q4 | 8/8 | 15.2 % | 9.0 % | 27/39 | 14.1 | 0.20 | 878.0 | 1124.0 | 2.7 | - |
| lokal:nb-whisper-large-distil-turbo-beta-f16 | 8/8 | 25.7 % | 14.9 % | 24/39 | 8.8 | 0.13 | 1509.0 | 1724.0 | 1.8 | - |

Sanntidsfaktor under 1 betyr raskere enn sanntid.

## Per klipp

### k01-bestilling-allergi (stemme Nora (Norsk bokmål (Norge)), 10.5 s)

Fasit: Hei, vi er fire personer til bord tolv klokka halv åtte. En av oss har alvorlig sesamallergi, og en er gravid, så ingen rå fisk eller upasteurisert ost.

| Modell | WER | Bom på kritiske ord | Transkripsjon |
|---|---|---|---|
| lokal:mlx-community/whisper-large-v3-turbo | 7.1 % | tolv, upasteurisert | Hei, vi er fire personer til bord 12 klokka halv åtte. En av oss har alvorlig sesamallergi, og en er gravid, så ingen rå fisk eller upasterisert ost. |
| lokal:nb-whisper-small-f16 | 10.7 % | upasteurisert | Hei, vi har fire personer til bord tolv klokka halv åtte. En av oss har alvorlig sesamallergi, og en er gravid, så ingen rå fisk heller upastaurisert ost. |
| lokal:nb-whisper-medium-f16 | 7.1 % | tolv | Hei, vi er fire personer til bo 12 klokka halv åtte. En av oss har alvorlig sesamallergi, og en er gravid. Så ingen rå fisk eller upasteurisert ost. |
| lokal:nb-whisper-large-f16 | 0.0 % | - | Hei, vi er fire personer til bord tolv klokka halv åtte, en av oss har alvorlig sesamallergi, og en er gravid, så ingen rå fisk eller upasteurisert ost. |
| lokal:nb-whisper-large-q4 | 0.0 % | - | Hei, vi er fire personer til bord tolv klokka halv åtte, en av oss har alvorlig sesamallergi, og en er gravid, så ingen rå fisk eller upasteurisert ost. |
| lokal:nb-whisper-large-distil-turbo-beta-f16 | 0.0 % | - | Hei, vi er fire personer til bord tolv klokka halv åtte, en av oss har alvorlig sesamallergi, og en er gravid, så ingen rå fisk eller upasteurisert ost. |

### k02-vin-og-retter (stemme Nora (Norsk bokmål (Norge)), 9.68 s)

Fasit: Kan vi få en flaske Etna Rosso fra 2019 og to glass Grillo til forretten? Så tar vi arancini, caponata og busiate med pistasj.

| Modell | WER | Bom på kritiske ord | Transkripsjon |
|---|---|---|---|
| lokal:mlx-community/whisper-large-v3-turbo | 16.7 % | etna rosso | Kan vi få en flaske etnar også fra 2019 og to glassgrillo til forretten, så tar vi arancini, caponata og busiate med pistasj. |
| lokal:nb-whisper-small-f16 | 33.3 % | etna rosso, 2019, arancini, busiate, pistasj | Kan vi få en flaske etnar også fra 2000 og 1902 glass grillot til forretten, så tar vi Aranzini, Caponata og Buseate med Pistash. |
| lokal:nb-whisper-medium-f16 | 16.7 % | etna rosso, arancini, caponata | Kan vi få en flaske Etnar også fra 2019 og to glass grillo til forretten? Så tar vi aranzini, kaponata og busiate med pistasj. |
| lokal:nb-whisper-large-f16 | 4.2 % | busiate | Kan vi få en flaske Etna Rosso fra 2019 og to glass Grillo til forretten, så tar vi Arancini, Caponata og Buseate med pistasj. |
| lokal:nb-whisper-large-q4 | 12.5 % | etna rosso, busiate | Kan vi få en flaske etnarosso fra 2019 og to glass Grillo til forretten, så tar vi Arancini, Caponata og Buseate med pistasj. |
| lokal:nb-whisper-large-distil-turbo-beta-f16 | 25.0 % | etna rosso, 2019, arancini, busiate | Kan vi få en flaske Etna Roso fra 2 glass Grillo til forretten, så tar vi Aransini, Caponata og Buceate med pistasj. |

### k03-moetevedtak (stemme Nora (Norsk bokmål (Norge)), 9.91 s)

Fasit: Da er vi enige. Henrik sender term sheetet innen fredag, Isabella går gjennom due diligence-rapporten, og vi møtes igjen den fjortende november.

| Modell | WER | Bom på kritiske ord | Transkripsjon |
|---|---|---|---|
| lokal:mlx-community/whisper-large-v3-turbo | 26.1 % | term sheet, due diligence, fjortende november | Da er vi enige. Henrik sender tverm skjetet inn fredag, Isabella går gjennom Bue Dilijanser-rapporten, og vi møtes igjen den 14. november. |
| lokal:nb-whisper-small-f16 | 43.5 % | term sheet, due diligence, fjortende november | Da er vi enige. Henrik sender tjernskjeetet innfredag, Isabella går gjennom bue de Lichance-rapporten, og vi møtes igjen 14.11. |
| lokal:nb-whisper-medium-f16 | 30.4 % | term sheet, due diligence, fjortende november | Da er vi enige. Henrik sender tvermsetet innen fredag. Isabella går gjennom bue-delisjanse-rapporten, og vi møtes igjen 14.11. |
| lokal:nb-whisper-large-f16 | 26.1 % | term sheet, due diligence, fjortende november | Da er vi enige. Henrik sender fjern beskjed etter innen fredag, Isabella går gjennom Bue Dilisjanse-rapporten, og vi møtes igjen den 14. november. |
| lokal:nb-whisper-large-q4 | 30.4 % | term sheet, due diligence, fjortende november | Da er vi enige. Henrik sender fjern beskjed etter innen fredag, Isabella går gjennom Bue de Lisance-rapporten, og vi møtes igjen den 14. november. |
| lokal:nb-whisper-large-distil-turbo-beta-f16 | 30.4 % | term sheet, due diligence, fjortende november | Da er vi enige. Henrik sender fjerm skjehetet inne fredag, Isabella går gjennom Bue-dilisjanserapporten, og vi møtes igjen den 14. november. |

### k04-tall (stemme Nora (Norsk bokmål (Norge)), 9.66 s)

Fasit: Verdsettelsen landet på hundre og tjue millioner kroner før pengene, med en opsjonspool på ti prosent og en likvidasjonspreferanse på én gang.

| Modell | WER | Bom på kritiske ord | Transkripsjon |
|---|---|---|---|
| lokal:mlx-community/whisper-large-v3-turbo | 36.4 % | hundre og tjue millioner, ti prosent, opsjonspool | Verbskjettelsen landet på 120 millioner kroner før pengene, med en opsjonspul på 10% og en likvidasjonspreferanse på en gang. |
| lokal:nb-whisper-small-f16 | 31.8 % | hundre og tjue millioner, ti prosent, opsjonspool | Verbsettelsen landet på 120 millioner kroner før pengene, med en opsjonsbul på 10 % og en likvidasjonspreferanse på én gang. |
| lokal:nb-whisper-medium-f16 | 36.4 % | hundre og tjue millioner, ti prosent, opsjonspool | Verdsettelsen landet på 120 mill. kr før pengene, med en opsjonsbol på 10 % og en likvidasjonspreferanse på én gang. |
| lokal:nb-whisper-large-f16 | 27.3 % | hundre og tjue millioner, ti prosent, opsjonspool | Verdsettelsen landet på 120 millioner kroner før pengene, med en opsjonsbul på 10 % og en likvidasjonspreferanse på én gang. |
| lokal:nb-whisper-large-q4 | 18.2 % | hundre og tjue millioner, opsjonspool | Verdsettelsen landet på 120 millioner kroner før pengene, med en aksjonsbul på ti prosent og en likvidasjonspreferanse på én gang. |
| lokal:nb-whisper-large-distil-turbo-beta-f16 | 31.8 % | hundre og tjue millioner, ti prosent, opsjonspool | Verbsettelsen landet på 120 millioner kroner før pengene, med en opsjonsbul på 10 %, og en likvidasjonspreferanse på én gang. |

### k05-engelsk-allergi (stemme Daniel, 6.01 s)

Fasit: I'm severely allergic to sesame and tree nuts. Could the kitchen please confirm that the sauce is safe for me?

| Modell | WER | Bom på kritiske ord | Transkripsjon |
|---|---|---|---|
| lokal:mlx-community/whisper-large-v3-turbo | 0.0 % | - | I'm severely allergic to sesame and tree nuts. Could the kitchen please confirm that the sauce is safe for me? |
| lokal:nb-whisper-small-f16 | 28.6 % | sesame, tree nuts | I am allergic to sesami and tree knots. Can the kitchen confirm that the sauce is safe for me? |
| lokal:nb-whisper-medium-f16 | 28.6 % | tree nuts | I am allergic to sesame and seeds. Can the kitchen confirm that the sauce is safe for me? |
| lokal:nb-whisper-large-f16 | 28.6 % | tree nuts | I am highly allergic to sesame and cloves. Can the kitchen confirm that the sauce is safe for me? |
| lokal:nb-whisper-large-q4 | 28.6 % | tree nuts | I am highly allergic to sesame and knubs. Can the kitchen confirm that the sauce is safe for me? |
| lokal:nb-whisper-large-distil-turbo-beta-f16 | 95.2 % | sesame, tree nuts, sauce | Jeg er ute allergisk til sesami og trenutter. Kan kjøkkenet beføre at saus er tatt for meg? |

### k06-vaktnotat (stemme Nora (Norsk bokmål (Norge)), 7.1 s)

Fasit: Bord sju feirer forlovelse. Ikke nevn jobben hans, og husk at hun uttaler etternavnet Vessel, ikke Wessel.

| Modell | WER | Bom på kritiske ord | Transkripsjon |
|---|---|---|---|
| lokal:mlx-community/whisper-large-v3-turbo | 29.4 % | bord sju | Bo Sy feirer forlovelse, ikke nevn jobben hans, og husk at hun uttaler etter nagne Vessel, ikke Vessel. |
| lokal:nb-whisper-small-f16 | 11.8 % | bord sju, vessel | Bor Sju feirer forlovelse, ikke nevn jobben hans. Og husk at hun uttaler etternavnet Wessel, ikke Wessel. |
| lokal:nb-whisper-medium-f16 | 5.9 % | vessel | Bord sju feirer forlovelse. Ikke nevn jobben hans. Og husk at hun uttaler etternavnet Wessel, ikke Wessel. |
| lokal:nb-whisper-large-f16 | 11.8 % | bord sju, vessel | Bod sju feirer forlovelse, ikke nevn jobben hans, og husk at hun uttaler etternavnet Wessel, ikke Wessel. |
| lokal:nb-whisper-large-q4 | 11.8 % | bord sju, vessel | Bod sju feirer forlovelse, ikke nevn jobben hans, og husk at hun uttaler etternavnet Wessel, ikke Wessel. |
| lokal:nb-whisper-large-distil-turbo-beta-f16 | 11.8 % | - | Bord sju feirer forlovelse, ikke nevn jobben hans, og husk at hun uttaler etternavnet Vesel, ikke Vessel. |

### k07-styreprotokoll (stemme Nora (Norsk bokmål (Norge)), 7.96 s)

Fasit: Styret ber om at protokollen fra møtet trettiende oktober signeres elektronisk med BankID før generalforsamlingen.

| Modell | WER | Bom på kritiske ord | Transkripsjon |
|---|---|---|---|
| lokal:mlx-community/whisper-large-v3-turbo | 13.3 % | trettiende oktober | Styret ber om at protokollen fra møte 30. oktober signeres elektronisk med BankID før generalforsamlingen. |
| lokal:nb-whisper-small-f16 | 26.7 % | trettiende oktober, bankid | Styret ber om at protokollen fra møtet signeres elektronisk med bank ID før generalforsamlingen. |
| lokal:nb-whisper-medium-f16 | 13.3 % | trettiende oktober | Styret ber om at protokollen fra møtet 13.10. signeres elektronisk med BankID før generalforsamlingen. |
| lokal:nb-whisper-large-f16 | 20.0 % | trettiende oktober, bankid | Styret ber om at protokollen fra møtet 13. oktober signeres elektronisk med bank ID før generalforsamlingen. |
| lokal:nb-whisper-large-q4 | 20.0 % | trettiende oktober, bankid | Styret ber om at protokollen fra møtet 13. oktober signeres elektronisk med bank ID før generalforsamlingen. |
| lokal:nb-whisper-large-distil-turbo-beta-f16 | 6.7 % | trettiende oktober | Styret ber om at protokollen fra møtet 13. oktober signeres elektronisk med bankID før generalforsamlingen. |

### k08-idemoete (stemme Nora (Norsk bokmål (Norge)), 8.74 s)

Fasit: Hva om premieren starter i foajeen, og publikum følger skuespillerne opp trappen til Chambre, der middagen er en del av forestillingen?

| Modell | WER | Bom på kritiske ord | Transkripsjon |
|---|---|---|---|
| lokal:mlx-community/whisper-large-v3-turbo | 9.5 % | foajeen, chambre | Hva om premieren starter i foieen, og publikum følger skuespillerne opp trappen til sjambre, der middagen er en del av forestillingen. |
| lokal:nb-whisper-small-f16 | 0.0 % | - | Hva om premieren starter i foajeen, og publikum følger skuespillerne opp trappen til Chambre der middagen er en del av forestillingen. |
| lokal:nb-whisper-medium-f16 | 0.0 % | - | Hva om premieren starter i foajeen og publikum følger skuespillerne opp trappen til Chambre, der middagen er en del av forestillingen. |
| lokal:nb-whisper-large-f16 | 0.0 % | - | Hva om premieren starter i foajeen, og publikum følger skuespillerne opp trappen til chambre, der middagen er en del av forestillingen? |
| lokal:nb-whisper-large-q4 | 0.0 % | - | Hva om premieren starter i foajeen og publikum følger skuespillerne opp trappen til Chambre, der middagen er en del av forestillingen? |
| lokal:nb-whisper-large-distil-turbo-beta-f16 | 4.8 % | chambre | Hva om premieren starter i foajeen og publikum følger skuespillerne opp trappen til Shambre, der middagen er en del av forestillingen. |

