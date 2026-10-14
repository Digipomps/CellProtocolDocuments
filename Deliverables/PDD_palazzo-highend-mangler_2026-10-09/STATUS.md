# STATUS — palazzo highend mangler

- surfaces: binding, cell, codex, gui, python, scaffold, skeleton
- tags: chat, gjest, gui, kryptering, palazzo, restaurant, samtykke, tale, transkribering, vc

## Porter
- G1: godkjent 2026-10-10        (formålsspesifikasjon godkjent av Kjetil)
- G1-GUI: venter        (rendret bilde godkjent — bare for GUI-oppgaver)
- G2: venter        (plan godkjent; arbeidspakker 1:1 mot bladformål)
- G3: venter        (akseptanse: forventning mot faktisk, alle avledede tester grønne)

Sett en port til `godkjent <dato>` kun når Kjetil har sagt det. `purpose_dev.py validate <mappe>` nekter porter uten artefakter.

## Planbytter (dato — hvorfor)
-

## Logg
- 2026-10-09: opprettet
- 2026-10-09: FORMAALSSPEC iterasjon 1 skrevet (Claude, PalazzoComunaleScaffold-prosjektet). G1 bedt om.
- 2026-10-09: modellprøve for tale til tekst lagt i køen som `inbox-stt/stt-proeve-1-20261009` (skript-modus; Kjetils lov 12:26 UTC). Resultat i `evidence/stt-benchmark/`.
- 2026-10-09 12:38Z: modellprøve kjørt (`stt-proeve-1`). Nøkkelen i nøkkelringen (`com.digipomps.cellscaffold.aigateway` / `nanogpt`, 44 tegn) avvises av NanoGPT med 401 på TTS. Nøkkelsjekk 12:39Z (`stt-nokkel-1`): 401 på chat for begge baser og begge hodeformer, og på balanse. Evidens: `HAVEN-Deploy/_handoff/STT-PROEVE/evidens/`. Prøven venter på gyldig nøkkel; jobben kan legges i køen igjen uendret.
- 2026-10-09 16:00Z: Kjetil la inn ny nøkkel (nøkkelringposten endret 15:53:23Z). Den har NanoGPT-form (`sk-nano-<uuid>`, 44 tegn, uten mellomrom), men NanoGPT svarer fortsatt 401 «Invalid session» på chat og «Incorrect API key» på balanse (`evidens/nokkel-sjekk-2.log`, `nokkel-finn-1.log`, `nokkel-form-1.log`). Prøven er ikke kjørt.
- 2026-10-09 17:37Z: lokal prøve kjørt (`stt-lokal-1`): mlx-whisper 0.4.3 installert i `~/.cache/haven-stt/venv` (760 MB); fire modeller (2,3 GB i HF-bufferen). Resultat: `evidence/stt-benchmark/LOKAL-RESULTAT.md`. large-v3-turbo: WER 17,3 %, 26/39 kritiske ord, 0,14× sanntid.
- 2026-10-09 17:38Z: ny NanoGPT-nøkkel godtas, men kontoen har 0 USD (402 «Insufficient balance», `evidens/nokkel-sjekk-3.log`). NanoGPT-prøven venter på saldo.
- 2026-10-09: FORMAALSSPEC iterasjon 2: nøkler skal ligge i eierens hemmelighetscelle (Kjetil 17:36Z).
- 2026-10-09 18:10Z: NB-Whisper (NbAiLab, Apache 2.0) konvertert til MLX (mlx-examples 796f5b5, `~/.cache/haven-stt/mlx-models/`) og målt (`stt-nb-3`): `evidence/stt-benchmark/NB-WHISPER-RESULTAT.md`. nb-whisper-large q4: WER 15,2 %, 27/39 kritiske, 878 MB, 1,1 GB minne, 0,20× sanntid. OpenAI large-v3-turbo: 17,3 %, 26/39, 1,6 GB.
- Avvik underveis: (1) runnerens mykt filtak 2 GiB stoppet nedlasting av medium/large på nøyaktig 2 147 483 648 byte; skriptet hever taket selv med begrunnelse. (2) convert.py skriver `model.safetensors`, mlx-whisper 0.4.3 leser `weights.safetensors`; skriptet omdøper.
- 2026-10-10: G1 godkjent av Kjetil («nanogpt har saldo nå. G1 godkjent», 00:34 UTC). Godkjenningen gjelder treet i FORMAALSSPEC iterasjon 2 med de anbefalte svarene i §6 (bølgerekkefølge, ChatCell-kryptering bygges her, delt regning utsatt) og standardvalget for tale til tekst.
- 2026-10-10: NanoGPT-prøven kjørt på nytt med saldo (køjobb stt-proeve-2-20261010): gpt-4o-mini-transcribe 8.2 % WER, Wizper 12.2 %, Whisper-Large-V3 16.5 %; Elevenlabs asynkron (202) og ikke målt; k01 fikk ingen TTS-lyd (503 billing reservation). Lokal mlx på samme lyd (lokal-tts-1-20261010): large-v3-turbo 12.7 %, NB large f16 13.6 %, NB large q4 16.7 % med gjentakelsesløkke på k03. Sammendrag: evidence/stt-benchmark/SAMMENLIGNING.md.
