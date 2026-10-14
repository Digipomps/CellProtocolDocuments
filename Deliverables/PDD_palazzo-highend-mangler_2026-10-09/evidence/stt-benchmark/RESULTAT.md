# Modellprøve: tale til tekst på norsk

Kjørt 2026-10-10T00:40:49Z av `tools/stt-benchmark/stt_proeve.py` (pc.stt.benchmark). API: `https://nano-gpt.com/api/v1`.

**Forbehold:** de syntetiske klippene er laget med gpt-4o-mini-tts. Syntetisk tale er renere enn ekte tale ved et bord, så feilratene er trolig for lave. Ekte opptak legges i `opptak/` med fasit i `.txt` og tas med neste kjøring.

NanoGPT er en ekstern tjeneste og brukes bare til denne prøven. Ingen av motorene her er godkjent for gjestelyd.

## Sammendrag per motor

| Motor | Klipp ok | Snitt WER | Snitt CER | Kritiske ord truffet | Median tid (s) | Anslått pris for settet (USD) | Feil |
|---|---|---|---|---|---|---|---|
| nanogpt:Elevenlabs-STT | 0/7 | - | - | 0/0 | 0.0 | 0.0351 | HTTP 202: {"status":"pending","run_id":"01a1233e-2e71-7793-9910-e5d95e3b82f1","r; HTTP 202: {"status":"pending","run_id":"01a1233e-6faa-7661-822e-b5f9f76bb857","r; HTTP 202: {"status":"pending","run_id":"01a1233e-b77d-7de2-a371-0343cbf7b82c","r; HTTP 202: {"status":"pending","run_id":"01a1233e-fdef-7831-ad58-a33fd5669887","r; HTTP 202: {"status":"pending","run_id":"01a1233f-4115-7c83-8185-8f9a8e6b212e","r; HTTP 202: {"status":"pending","run_id":"01a1233f-ecb2-7882-a90e-2a0abacac1a8","r; HTTP 202: {"status":"pending","run_id":"01a12341-5eb5-7192-94f4-125e47a81e7e","r |
| nanogpt:Whisper-Large-V3 | 7/7 | 16.5 % | 8.1 % | 22/32 | 10.3 | 0.0006 | - |
| nanogpt:Wizper | 7/7 | 12.2 % | 7.4 % | 24/32 | 3.9 | 0.0117 | - |
| nanogpt:gpt-4o-mini-transcribe | 7/7 | 8.2 % | 4.2 % | 27/32 | 1.1 | 0.0035 | - |

## Per klipp

### k01-bestilling-allergi (syntetisk, stemme nova, ? s)

Fasit: Hei, vi er fire personer til bord tolv klokka halv åtte. En av oss har alvorlig sesamallergi, og en er gravid, så ingen rå fisk eller upasteurisert ost.

Lyd ble ikke laget: TTS HTTP 503: {"error":{"message":"Billing reservation failed","type":"server_error","param":null,"code":"async_billing_reservation_failed"}}

### k02-vin-og-retter (syntetisk, stemme onyx, 12.9 s)

Fasit: Kan vi få en flaske Etna Rosso fra 2019 og to glass Grillo til forretten? Så tar vi arancini, caponata og busiate med pistasj.

| Motor | WER | CER | Bom på kritiske ord | Transkripsjon |
|---|---|---|---|---|
| nanogpt:Whisper-Large-V3 | 20.8 % | 3.0 % | caponata |  Kan vi få en flaske Etna Rosso fra 2019?  og to glass Grillo til forretten.  så Tavi Arancini,  Kaponata, obusiate med pistasj. |
| nanogpt:Wizper | 4.2 % | 1.0 % | - | Kan vi få en flaske Etna Rosso fra 2019 og to glass Grillo til forretten. Så tar vi arancini, caponata og busiate med pistasje. |
| nanogpt:gpt-4o-mini-transcribe | 0.0 % | 0.0 % | - | Kan vi få en flaske Etna Rosso fra 2019 og to glass Grillo til forretten? Så tar vi arancini, caponata og busiate med pistasj. |
| nanogpt:Elevenlabs-STT | - | - | - | FEIL: HTTP 202: {"status":"pending","run_id":"01a1233e-2e71-7793-9910-e5d95e3b82f1","request_id":"01a1233e-2e71-7793-9910-e5d9 |

### k03-moetevedtak (syntetisk, stemme alloy, 10.2 s)

Fasit: Da er vi enige. Henrik sender term sheetet innen fredag, Isabella går gjennom due diligence-rapporten, og vi møtes igjen den fjortende november.

| Motor | WER | CER | Bom på kritiske ord | Transkripsjon |
|---|---|---|---|---|
| nanogpt:Whisper-Large-V3 | 13.0 % | 7.6 % | term sheet, fjortende november |  Da er vi enige.  Henrik sender termsheetet innen fredag, Isabella går gjennom due diligence rapporten, og vi møtes igjen.  Den 14. november. |
| nanogpt:Wizper | 4.3 % | 7.6 % | fjortende november | Da er vi enige. Henrik sender term sheetet innen fredag, Isabella går gjennom due diligence rapporten, og vi møtes igjen den 14. november. |
| nanogpt:gpt-4o-mini-transcribe | 13.0 % | 7.6 % | term sheet, fjortende november | Da er vi enige. Henrik sender termsheetet innen fredag, Isabella går gjennom due diligence-rapporten, og vi møtes igjen den 14. november. |
| nanogpt:Elevenlabs-STT | - | - | - | FEIL: HTTP 202: {"status":"pending","run_id":"01a1233e-6faa-7661-822e-b5f9f76bb857","request_id":"01a1233e-6faa-7661-822e-b5f9 |

### k04-tall (syntetisk, stemme echo, 11.5 s)

Fasit: Verdsettelsen landet på hundre og tjue millioner kroner før pengene, med en opsjonspool på ti prosent og en likvidasjonspreferanse på én gang.

| Motor | WER | CER | Bom på kritiske ord | Transkripsjon |
|---|---|---|---|---|
| nanogpt:Whisper-Large-V3 | 36.4 % | 21.0 % | hundre og tjue millioner, ti prosent, opsjonspool |  Verdsettelsen landet på 120 millioner kroner for pengene.  med en optionspool på 10%  og en likvidasjonspreferanse på en gang. |
| nanogpt:Wizper | 36.4 % | 21.0 % | hundre og tjue millioner, ti prosent, opsjonspool | Vedsetelsen landet på 120 millioner kroner før pengene, med en opsjonspol på 10% og en likvidasjonspreferanse på en gang. |
| nanogpt:gpt-4o-mini-transcribe | 13.6 % | 5.0 % | - | Verdsettes som lumnet på hundre og tjue millioner kroner før pengene, med en opsjonspool på ti prosent og en likvidasjonspreferanse på én gang. |
| nanogpt:Elevenlabs-STT | - | - | - | FEIL: HTTP 202: {"status":"pending","run_id":"01a1233e-b77d-7de2-a371-0343cbf7b82c","request_id":"01a1233e-b77d-7de2-a371-0343 |

### k05-engelsk-allergi (syntetisk, stemme shimmer, 7.0 s)

Fasit: I'm severely allergic to sesame and tree nuts. Could the kitchen please confirm that the sauce is safe for me?

| Motor | WER | CER | Bom på kritiske ord | Transkripsjon |
|---|---|---|---|---|
| nanogpt:Whisper-Large-V3 | 0.0 % | 0.0 % | - |  I'm severely allergic to sesame and tree nuts.  Could the kitchen please confirm that the sauce is safe for me? |
| nanogpt:Wizper | 0.0 % | 0.0 % | - | I'm severely allergic to sesame and tree nuts. Could the kitchen please confirm that the sauce is safe for me? |
| nanogpt:gpt-4o-mini-transcribe | 0.0 % | 0.0 % | - | I'm severely allergic to sesame and tree nuts. Could the kitchen please confirm that the sauce is safe for me? |
| nanogpt:Elevenlabs-STT | - | - | - | FEIL: HTTP 202: {"status":"pending","run_id":"01a1233e-fdef-7831-ad58-a33fd5669887","request_id":"01a1233e-fdef-7831-ad58-a33f |

### k06-vaktnotat (syntetisk, stemme fable, 10.5 s)

Fasit: Bord sju feirer forlovelse. Ikke nevn jobben hans, og husk at hun uttaler etternavnet Vessel, ikke Wessel.

| Motor | WER | CER | Bom på kritiske ord | Transkripsjon |
|---|---|---|---|---|
| nanogpt:Whisper-Large-V3 | 17.6 % | 5.8 % | bord sju |  Bor 7 feirer forlovelse.  Ikke nevn jobben hans, og husk at hun uttaler etternavnet Vessel.  Ikke Vessel. |
| nanogpt:Wizper | 17.6 % | 5.8 % | bord sju | Bor 7 feirer forlovelse. Ikke nevn jobben hans, og husk at hun uttaler etternavnet Vessel, ikke Vessel. |
| nanogpt:gpt-4o-mini-transcribe | 17.6 % | 5.8 % | bord sju, vessel | Bor, 7, feirer forlovelse. Ikke nevn jobben hans, og husk at hun uttaler etternavnet Wessel, ikke Wessel. |
| nanogpt:Elevenlabs-STT | - | - | - | FEIL: HTTP 202: {"status":"pending","run_id":"01a1233f-4115-7c83-8185-8f9a8e6b212e","request_id":"01a1233f-4115-7c83-8185-8f9a |

### k07-styreprotokoll (syntetisk, stemme nova, 8.4 s)

Fasit: Styret ber om at protokollen fra møtet trettiende oktober signeres elektronisk med BankID før generalforsamlingen.

| Motor | WER | CER | Bom på kritiske ord | Transkripsjon |
|---|---|---|---|---|
| nanogpt:Whisper-Large-V3 | 13.3 % | 11.1 % | trettiende oktober |  Styret ber om at protokollen fra møte 30. oktober signeres elektronisk med BankID før generalforsamlingen. |
| nanogpt:Wizper | 13.3 % | 11.1 % | trettiende oktober | Styret ber om at protokollen fra møte 30. oktober signeres elektronisk med BankID før generalforsamlingen. |
| nanogpt:gpt-4o-mini-transcribe | 13.3 % | 11.1 % | trettiende oktober | Styret ber om at protokollen fra møte 31. oktober signeres elektronisk med BankID før generalforsamlingen. |
| nanogpt:Elevenlabs-STT | - | - | - | FEIL: HTTP 202: {"status":"pending","run_id":"01a1233f-ecb2-7882-a90e-2a0abacac1a8","request_id":"01a1233f-ecb2-7882-a90e-2a0a |

### k08-idemoete (syntetisk, stemme onyx, 9.7 s)

Fasit: Hva om premieren starter i foajeen, og publikum følger skuespillerne opp trappen til Chambre, der middagen er en del av forestillingen?

| Motor | WER | CER | Bom på kritiske ord | Transkripsjon |
|---|---|---|---|---|
| nanogpt:Whisper-Large-V3 | 14.3 % | 8.0 % | foajeen, chambre |  Hva om premieren starter i forrige år?  og publikum følger skuespillerne opp trappen til sjambret.  der middagen er en del av forestillingen, |
| nanogpt:Wizper | 9.5 % | 5.4 % | foajeen, chambre | Hva om premieren starter i foyeren, og publikum følger skuespillerne opp trappen til sjambret, der middagen er en del av forestillingen? |
| nanogpt:gpt-4o-mini-transcribe | 0.0 % | 0.0 % | - | Hva om premieren starter i foajeen, og publikum følger skuespillerne opp trappen til Chambre, der middagen er en del av forestillingen? |
| nanogpt:Elevenlabs-STT | - | - | - | FEIL: HTTP 202: {"status":"pending","run_id":"01a12341-5eb5-7192-94f4-125e47a81e7e","request_id":"01a12341-5eb5-7192-94f4-125e |

## Lydfiler

| Klipp | sha256 |
|---|---|
| k01-bestilling-allergi | `-` |
| k02-vin-og-retter | `1e10483712f7f1bce2a4278280b4f65f05aece4194f18ef6dfec5c2a72fe2538` |
| k03-moetevedtak | `e4a3f22b623c55ae00b316a94b579dabafab8021e701da7da235b33d0fa884b1` |
| k04-tall | `61c8e7de5405f1ca00f87a5ec5fd41d565a305e5d8d4831dc56c5da8b2ba51a0` |
| k05-engelsk-allergi | `02bffabb4f6dcc7194a59bd56de204a49a4c4e7d16f43c410f03e5254fe6b8d6` |
| k06-vaktnotat | `44ff438bc6fe8c0a220bf9c3d4ddd9be520a65ed037ab88e6a8aacb5c16a92b7` |
| k07-styreprotokoll | `4dc508dbd86399b06030661b593563ced9e7c1b4ca8b6f6ac1e3288d08f97cc8` |
| k08-idemoete | `58ab9710ed815b992b522113be996c17c4f93de61a6b67a1f8b20db52b26c02c` |
