# Reproduksjon

Les `RESULTAT.md` for avgrensning og resultat. Fra Documents-roten, med den pinnede
Qwen-modellen tilgjengelig og aliasene verifisert:

```bash
HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 \
  /private/tmp/haven-gemma-venv/bin/python -m mlx_vlm.server \
  --host 127.0.0.1 --port 8087 --model /private/tmp/haven-qwen35-9b \
  --max-tokens 512 --log-level INFO
```

I en annen terminal:

```bash
python3 Deliverables/Qwen35_Local_Dialogue_2026-10-13/run_qwen.py \
  --output /private/tmp/qwen35-new-run.jsonl
```

Runneren avviser eksisterende resultatfil og feil hash/modell-ID. Serveren krever
Metal-tilgang. Stopp bare serverprosessen du selv startet. Skillens Gemma-spesifikke
stoppskript eier ikke en Qwen-prosess.

Rå svar ligger i `evidence/run-01.jsonl`, manuelle vurderinger i `review-01.json`
og maskinlesbar sammenligning i `comparison.json` under samme evidence-mappe.
