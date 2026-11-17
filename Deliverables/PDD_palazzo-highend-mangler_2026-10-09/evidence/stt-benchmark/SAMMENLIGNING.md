# Tale til tekst: NanoGPT mot lokal Whisper på lik lyd

Dato: 2026-10-10. Lyd: sju syntetiske klipp laget med gpt-4o-mini-tts (k02–k08, 70 s). k01 fikk ingen lyd fordi NanoGPT svarte «Billing reservation failed» på TTS-kallet. Detaljer: `RESULTAT.md` (NanoGPT) og `LOKAL-TTS-RESULTAT.md` (lokalt).

| Motor | Hvor | WER | CER | Kritiske ord | Median/totaltid | Størrelse | Pris for settet |
|---|---|---|---|---|---|---|---|
| gpt-4o-mini-transcribe | NanoGPT (ekstern) | 8.2 % | 4.2 % | 27/32 | 1.1 s per klipp | - | 0.0035 USD |
| Wizper | NanoGPT (ekstern) | 12.2 % | 7.4 % | 24/32 | 3.9 s per klipp | - | 0.0117 USD |
| whisper-large-v3-turbo (mlx) | Mac-en | 12.7 % | 6.3 % | 24/32 | 6.3 s totalt (RTF 0.09) | 1614 MB | 0 |
| nb-whisper-large f16 (mlx) | Mac-en | 13.6 % | 8.6 % | 23/32 | 12.9 s totalt (RTF 0.18) | 3083 MB | 0 |
| Whisper-Large-V3 | NanoGPT (ekstern) | 16.5 % | 8.1 % | 22/32 | 10.3 s per klipp | - | 0.0006 USD |
| nb-whisper-large q4 (mlx) | Mac-en | 16.7 % | 21.0 % | 22/32 | 13.4 s totalt (RTF 0.19) | 878 MB | 0 |
| Elevenlabs-STT | NanoGPT (ekstern) | - | - | - | svarer asynkront (HTTP 202), skriptet henter ikke resultatet | - | - |

## Hva tallene sier

- gpt-4o-mini-transcribe er klart best, særlig på tall skrevet som ord og på låneord (Chambre, foajeen).
- Lokalt er whisper-large-v3-turbo og nb-whisper-large like gode på denne lyden. På `say`-lyden i går var NB best (15.2 % mot 17.3 %). Med sju korte klipp er forskjellene innenfor støyen.
- nb-whisper-large q4 hang seg opp i en gjentakelsesløkke på k03 («14.11.11.111…»). Det forklarer den høye CER-en. Kjent Whisper-feil; motvirkes med `condition_on_previous_text=False`, temperaturfallback og kompresjonsgrense. Må fikses før q4 blir nedlastbar ressurs.
- Felles feil for alle: tall normaliseres til sifre («14. november», «10 %»), og «bord sju» blir «Bor 7». Dette er normalisering, ikke hørselsfeil, men kritiske ord som allergi og bordnummer må sjekkes i begge former.

## Konsekvens for pc.stt

Standard forblir lokal kjøring i eierens CellScaffold. En ekstern motor som gpt-4o-mini-transcribe kan tilbys bare som brukerens eget valg med en Agreement, som §1 sier. Ingen ekte gjestelyd har gått til NanoGPT.
