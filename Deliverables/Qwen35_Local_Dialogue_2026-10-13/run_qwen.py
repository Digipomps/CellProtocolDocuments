#!/usr/bin/env python3
"""Run the unchanged Gemma baseline prompts/corpus with local Qwen3.5-9B."""
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
BASE=ROOT.parent/"Gemma_Local_Dialogue_2026-10-13"
pins=json.loads((ROOT/"evidence/baseline-inputs.json").read_text())
for name,digest in pins["sha256"].items():
    assert hashlib.sha256((BASE/name).read_bytes()).hexdigest()==digest, name
spec=importlib.util.spec_from_file_location("gemma_baseline", BASE/"run_dialogue.py")
baseline=importlib.util.module_from_spec(spec)
spec.loader.exec_module(baseline)
baseline.MODEL="/private/tmp/haven-qwen35-9b"
# Same loopback port, MLX/VLM server and request settings as the Gemma run.
if __name__=="__main__": baseline.main()
