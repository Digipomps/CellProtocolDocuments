# Lokal tale til tekst: mlx-whisper på Mac-en

Kjørt 2026-10-10T00:42:18Z av `tools/stt-benchmark/stt_lokal.py`. Klippene er de samme gpt-4o-mini-tts-klippene som NanoGPT-prøven brukte (`lyd/*.mp3`), gjort om til 16 kHz WAV. Transkripsjonen kjørte lokalt.

**Forbehold:** syntetisk tale er renere enn ekte tale ved et bord. Tallene er trolig for gode. Prøvesettet er åtte setninger, så forskjeller på noen få prosentpoeng betyr lite.

Lydlengde totalt: 70.1 s.

| Modell | Klipp ok | Snitt WER | Snitt CER | Kritiske ord | Tid totalt (s) | Sanntidsfaktor | Modell på disk (MB) | Maks minne (MB) | Første kall inkl. nedlasting (s) | Feil |
|---|---|---|---|---|---|---|---|---|---|---|
| lokal:mlx-community/whisper-large-v3-turbo | 7/7 | 12.7 % | 6.3 % | 24/32 | 6.3 | 0.09 | 1614.0 | 970.0 | 2.3 | - |
| lokal:nb-whisper-large-q4 | 7/7 | 16.7 % | 21.0 % | 22/32 | 13.4 | 0.19 | 878.0 | 1149.0 | 1.7 | - |
| lokal:nb-whisper-large-f16 | 7/7 | 13.6 % | 8.6 % | 23/32 | 12.9 | 0.18 | 3083.0 | 3265.0 | 3.0 | - |

Sanntidsfaktor under 1 betyr raskere enn sanntid.

## Per klipp

### k01-bestilling-allergi (stemme tts:nova, ? s)

Fasit: Hei, vi er fire personer til bord tolv klokka halv åtte. En av oss har alvorlig sesamallergi, og en er gravid, så ingen rå fisk eller upasteurisert ost.

Ikke laget: ingen TTS-lyd fra NanoGPT-prøven

### k02-vin-og-retter (stemme tts:onyx, 12.91 s)

Fasit: Kan vi få en flaske Etna Rosso fra 2019 og to glass Grillo til forretten? Så tar vi arancini, caponata og busiate med pistasj.

| Modell | WER | Bom på kritiske ord | Transkripsjon |
|---|---|---|---|
| lokal:mlx-community/whisper-large-v3-turbo | 12.5 % | etna rosso | Kan vi få en flaske Etnarosso fra 2019 og to glass Grillo til forretten. Så tar vi Arancini, Caponata og Busiate med pistasje. |
| lokal:nb-whisper-large-q4 | 16.7 % | arancini, busiate | Kan vi få én flaske etna-rosso fra 2019, og to glass grillo til forretten? Så tar vi aranchini, caponata og bussiate med pistasje. |
| lokal:nb-whisper-large-f16 | 12.5 % | arancini, busiate | Kan vi få én flaske etna-rosso fra 2019, og to glass grillo til forretten? Så tar vi aranchini, caponata og bussiate med pistasj. |

### k03-moetevedtak (stemme tts:alloy, 10.15 s)

Fasit: Da er vi enige. Henrik sender term sheetet innen fredag, Isabella går gjennom due diligence-rapporten, og vi møtes igjen den fjortende november.

| Modell | WER | Bom på kritiske ord | Transkripsjon |
|---|---|---|---|
| lokal:mlx-community/whisper-large-v3-turbo | 4.3 % | fjortende november | Da er vi enige. Henrik sender term sheetet innen fredag, Isabella går gjennom due diligence-rapporten, og vi møtes igjen den 14. november. |
| lokal:nb-whisper-large-q4 | 26.1 % | term sheet, fjortende november | Da er vi enige. Henrik sender termsheetet innen fredag, Isabella går gjennom due diligence-rapporten, og vi møtes igjen den 14.11.11.1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111 |
| lokal:nb-whisper-large-f16 | 13.0 % | term sheet, fjortende november | Da er vi enige. Henrik sender termsheetet innen fredag, Isabella går gjennom due diligence-rapporten, og vi møtes igjen den 14. november. |

### k04-tall (stemme tts:echo, 11.52 s)

Fasit: Verdsettelsen landet på hundre og tjue millioner kroner før pengene, med en opsjonspool på ti prosent og en likvidasjonspreferanse på én gang.

| Modell | WER | Bom på kritiske ord | Transkripsjon |
|---|---|---|---|
| lokal:mlx-community/whisper-large-v3-turbo | 31.8 % | hundre og tjue millioner, ti prosent, opsjonspool | Vedsettelsen landet på 120 millioner kroner før pengene, med en opsjonspol på 10 prosent og en likvidasjonspreferanse på en gang. |
| lokal:nb-whisper-large-q4 | 27.3 % | hundre og tjue millioner, ti prosent, opsjonspool | Verdsettelsen landet på 120 millioner kroner før pengene, med en opsjonspol på 10 % og en likvidasjonspreferanse på én gang. |
| lokal:nb-whisper-large-f16 | 22.7 % | hundre og tjue millioner, ti prosent | Verdsettelsen landet på 120 millioner kroner før pengene, med en opsjonspool på 10 % og en likvidasjonspreferanse på én gang. |

### k05-engelsk-allergi (stemme tts:shimmer, 6.96 s)

Fasit: I'm severely allergic to sesame and tree nuts. Could the kitchen please confirm that the sauce is safe for me?

| Modell | WER | Bom på kritiske ord | Transkripsjon |
|---|---|---|---|
| lokal:mlx-community/whisper-large-v3-turbo | 0.0 % | - | I'm severely allergic to sesame and tree nuts. Could the kitchen please confirm that the sauce is safe for me? |
| lokal:nb-whisper-large-q4 | 14.3 % | - | I am severely allergic to sesame and tree nuts. Can the kitchen confirm that the sauce is safe for me? |
| lokal:nb-whisper-large-f16 | 14.3 % | - | I am severely allergic to sesame and tree nuts. Can the kitchen confirm that the sauce is safe for me? |

### k06-vaktnotat (stemme tts:fable, 10.51 s)

Fasit: Bord sju feirer forlovelse. Ikke nevn jobben hans, og husk at hun uttaler etternavnet Vessel, ikke Wessel.

| Modell | WER | Bom på kritiske ord | Transkripsjon |
|---|---|---|---|
| lokal:mlx-community/whisper-large-v3-turbo | 17.6 % | bord sju | Bor 7 feirer forlovelse. Ikke nevn jobben hans, og husk at hun uttaler etternavnet Vessel, ikke Vessel. |
| lokal:nb-whisper-large-q4 | 5.9 % | vessel | Bord sju. Feirer forlovelse. Ikke nevn jobben hans, og husk at hun uttaler etternavnet Wessel, ikke Wessel. |
| lokal:nb-whisper-large-f16 | 5.9 % | vessel | Bord sju. Feirer forlovelse. Ikke nevn jobben hans, og husk at hun uttaler etternavnet Wessel, ikke Wessel. |

### k07-styreprotokoll (stemme tts:nova, 8.35 s)

Fasit: Styret ber om at protokollen fra møtet trettiende oktober signeres elektronisk med BankID før generalforsamlingen.

| Modell | WER | Bom på kritiske ord | Transkripsjon |
|---|---|---|---|
| lokal:mlx-community/whisper-large-v3-turbo | 13.3 % | trettiende oktober | Styret ber om at protokollen fra møte 31. oktober signeres elektronisk med BankID før generalforsamlingen. |
| lokal:nb-whisper-large-q4 | 26.7 % | trettiende oktober, bankid | Styret ber om at protokollen fra møtet 31.10 signeres elektronisk med bank-IB før generalforsamlingen. |
| lokal:nb-whisper-large-f16 | 26.7 % | trettiende oktober, bankid | Styret ber om at protokollen fra møtet 30.10 signeres elektronisk med bank-IB før generalforsamlingen. |

### k08-idemoete (stemme tts:onyx, 9.72 s)

Fasit: Hva om premieren starter i foajeen, og publikum følger skuespillerne opp trappen til Chambre, der middagen er en del av forestillingen?

| Modell | WER | Bom på kritiske ord | Transkripsjon |
|---|---|---|---|
| lokal:mlx-community/whisper-large-v3-turbo | 9.5 % | foajeen | Hva om premieren starter i foie-hjem, og publikum følger skuespillerne opp trappen til chambre, der middagen er en del av forestillingen? |
| lokal:nb-whisper-large-q4 | 0.0 % | - | Hva om premieren starter i foajeen, og publikum følger skuespillerne opp trappen til chambre, der middagen er en del av forestillingen? |
| lokal:nb-whisper-large-f16 | 0.0 % | - | Hva om premieren starter i foajeen, og publikum følger skuespillerne opp trappen til chambre, der middagen er en del av forestillingen? |

