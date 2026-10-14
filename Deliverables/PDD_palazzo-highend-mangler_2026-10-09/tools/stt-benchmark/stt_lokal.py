#!/usr/bin/env python3
"""Lokal tale til tekst med mlx-whisper på Mac-en (pc.stt.benchmark, lokal del).

PDD: CellProtocolDocuments/Deliverables/PDD_palazzo-highend-mangler_2026-10-09

Lager norske prøveklipp med macOS sin egen stemme (`say`, ingen nettverkstjeneste),
transkriberer dem med flere Whisper-størrelser i MLX, og skriver
<out>/LOKAL-RESULTAT.md og lokal-resultater.json.

Hver modell kjøres i en egen prosess, så minnetoppen per modell kan måles.
Lyden lastes med stdlib `wave` + numpy, så ffmpeg trengs ikke.

Kjøres av HAVEN-Deploy/_handoff/STT-PROEVE/kjor-stt-lokal.sh i en egen venv.
"""
import argparse
import json
import os
import resource
import shutil
import subprocess
import sys
import time
import wave
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import stt_proeve as sp  # noqa: E402  (wer, cer, critical_hits, normalize)

MODELS = [
    "mlx-community/whisper-tiny-mlx",
    "mlx-community/whisper-base-mlx",
    "mlx-community/whisper-small-mlx",
    "mlx-community/whisper-large-v3-turbo",
]
NB_VOICES = ["Nora", "Henrik"]
EN_VOICES = ["Samantha", "Daniel"]


def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def voices():
    out = subprocess.run(["say", "-v", "?"], capture_output=True, text=True).stdout
    found = {}
    rows = []
    for line in out.splitlines():
        # "Nora                nb_NO    # Hei! Jeg heter Nora."
        head = line.split("#")[0].rstrip()
        if not head:
            continue
        locale = head.split()[-1]
        name = head[: head.rfind(locale)].strip()
        rows.append((name, locale))
    for name, loc in rows:
        found.setdefault(loc, []).append(name)
    return found


def pick_voice(found, lang, idx):
    locs = ["nb_NO", "no_NO"] if lang == "no" else ["en_US", "en_GB"]
    pref = NB_VOICES if lang == "no" else EN_VOICES
    cands = [v for l in locs for v in found.get(l, [])]
    ordered = [v for v in pref if v in cands] + [v for v in cands if v not in pref]
    if not ordered:
        return None
    return ordered[idx % len(ordered)] if lang == "no" else ordered[0]


def make_clips(out):
    with open(os.path.join(HERE, "proevesett.json"), encoding="utf-8") as f:
        spec = json.load(f)
    found = voices()
    d = os.path.join(out, "lyd-say")
    os.makedirs(d, exist_ok=True)
    items = []
    for i, c in enumerate(spec["klipp"]):
        lang = c.get("spraak", "no")
        v = pick_voice(found, lang, i)
        wav = os.path.join(d, c["id"] + ".wav")
        item = {"id": c["id"], "tekst": c["tekst"], "spraak": lang, "kritiske": c.get("kritiske", []), "stemme": v, "fil": wav}
        if v is None:
            item["feil"] = "ingen macOS-stemme for %s" % lang
        elif not os.path.exists(wav):
            aiff = wav[:-4] + ".aiff"
            r1 = subprocess.run(["say", "-v", v, "-o", aiff, c["tekst"]], capture_output=True, text=True)
            r2 = subprocess.run(["afconvert", "-f", "WAVE", "-d", "LEI16@16000", "-c", "1", aiff, wav], capture_output=True, text=True)
            if r1.returncode or r2.returncode:
                item["feil"] = "say/afconvert feilet: %s %s" % (r1.stderr[-200:], r2.stderr[-200:])
            if os.path.exists(aiff):
                os.remove(aiff)
        if os.path.exists(wav):
            with wave.open(wav) as w:
                item["sekunder_lyd"] = round(w.getnframes() / float(w.getframerate()), 2)
            item["sha256"] = sp.sha256(wav)
        items.append(item)
    return items, found


def make_clips_tts(out):
    """Samme lyd som NanoGPT-prøven (lyd/<id>.mp3 fra gpt-4o-mini-tts), gjort om til 16 kHz WAV, så motorene kan sammenlignes på lik lyd."""
    with open(os.path.join(HERE, "proevesett.json"), encoding="utf-8") as f:
        spec = json.load(f)
    src, d = os.path.join(out, "lyd"), os.path.join(out, "lyd-tts-wav")
    os.makedirs(d, exist_ok=True)
    items = []
    for c in spec["klipp"]:
        mp3, wav = os.path.join(src, c["id"] + ".mp3"), os.path.join(d, c["id"] + ".wav")
        item = {"id": c["id"], "tekst": c["tekst"], "spraak": c.get("spraak", "no"), "kritiske": c.get("kritiske", []), "stemme": "tts:" + c.get("stemme", "?"), "fil": wav}
        if not os.path.exists(mp3):
            item["feil"] = "ingen TTS-lyd fra NanoGPT-prøven"
        elif not os.path.exists(wav):
            r = subprocess.run(["afconvert", "-f", "WAVE", "-d", "LEI16@16000", "-c", "1", mp3, wav], capture_output=True, text=True)
            if r.returncode:
                item["feil"] = "afconvert feilet: %s" % r.stderr[-200:]
        if os.path.exists(wav):
            with wave.open(wav) as w:
                item["sekunder_lyd"] = round(w.getnframes() / float(w.getframerate()), 2)
            item["sha256"] = sp.sha256(wav)
        items.append(item)
    return items, {}


def load_wav(path):
    import numpy as np
    with wave.open(path) as w:
        frames = w.readframes(w.getnframes())
        assert w.getsampwidth() == 2 and w.getframerate() == 16000 and w.getnchannels() == 1
    return np.frombuffer(frames, dtype=np.int16).astype(np.float32) / 32768.0


def hf_cache_size(repo):
    root = repo if os.path.isdir(repo) else os.path.expanduser("~/.cache/huggingface/hub/models--" + repo.replace("/", "--"))
    total = 0
    for dp, _, fns in os.walk(root):
        for fn in fns:
            p = os.path.join(dp, fn)
            if not os.path.islink(p):
                total += os.path.getsize(p)
    return total


def worker(model, items_path, result_path):
    import mlx_whisper
    with open(items_path, encoding="utf-8") as f:
        items = [i for i in json.load(f) if not i.get("feil")]
    res = {"motor": "lokal:" + (model.rstrip("/").split("/")[-1] if os.path.isdir(model) else model), "klipp": []}
    t0 = time.time()
    try:
        mlx_whisper.transcribe(load_wav(items[0]["fil"]), path_or_hf_repo=model, language=items[0]["spraak"])
    except Exception as e:  # noqa: BLE001
        res["feil"] = "lasting feilet: %s" % e
        json.dump(res, open(result_path, "w"), ensure_ascii=False)
        return
    res["sekunder_forste_inkl_nedlasting"] = round(time.time() - t0, 1)
    for it in items:
        t = time.time()
        try:
            out = mlx_whisper.transcribe(load_wav(it["fil"]), path_or_hf_repo=model, language=it["spraak"])
            text, err = out.get("text", "").strip(), None
        except Exception as e:  # noqa: BLE001
            text, err = None, str(e)[:200]
        res["klipp"].append({"klipp": it["id"], "tekst": text, "feil": err, "sekunder": round(time.time() - t, 2)})
    res["maks_minne_mb"] = round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e6, 0)  # macOS: bytes
    res["modellstorrelse_mb"] = round(hf_cache_size(model) / 1e6, 0)
    json.dump(res, open(result_path, "w"), ensure_ascii=False, indent=2)


KILDE = "say"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--worker")
    ap.add_argument("--items")
    ap.add_argument("--result")
    ap.add_argument("--models", default=",".join(MODELS), help="Kommaliste: HF-repo eller lokal MLX-mappe")
    ap.add_argument("--rapport", default="LOKAL-RESULTAT.md")
    ap.add_argument("--kilde", choices=["say", "tts"], default="say", help="say: macOS-stemme; tts: lyden fra NanoGPT-prøven (lyd/*.mp3)")
    a = ap.parse_args()
    if a.worker:
        worker(a.worker, a.items, a.result)
        return 0
    out = os.path.abspath(a.out)
    os.makedirs(out, exist_ok=True)
    print("Lokal STT-prøve %s, ut: %s" % (now_iso(), out), flush=True)
    items, found = make_clips_tts(out) if a.kilde == "tts" else make_clips(out)
    global KILDE
    KILDE = a.kilde
    print("Norske stemmer: %s" % (found.get("nb_NO") or found.get("no_NO") or "ingen"), flush=True)
    for it in items:
        print("Klipp %s: %s %s" % (it["id"], it.get("stemme"), it.get("feil") or "%.1f s" % it.get("sekunder_lyd", 0)), flush=True)
    items_path = os.path.join(out, "lokal-klipp.json")
    json.dump(items, open(items_path, "w"), ensure_ascii=False, indent=2)
    results = []
    models = [m for m in a.models.split(",") if m]
    stem = os.path.splitext(a.rapport)[0].lower()
    for m in models:
        rp = os.path.join(out, "_" + stem + "-" + m.rstrip("/").split("/")[-1] + ".json")
        t = time.time()
        r = subprocess.run([sys.executable, os.path.abspath(__file__), "--out", out, "--worker", m, "--items", items_path, "--result", rp],
                           capture_output=True, text=True, timeout=3000)
        if os.path.exists(rp):
            res = json.load(open(rp))
        else:
            res = {"motor": "lokal:" + m, "klipp": [], "feil": "arbeider feilet: %s" % r.stderr[-400:]}
        by = {i["id"]: i for i in items}
        for k in res["klipp"]:
            if k["tekst"] is not None:
                ref = by[k["klipp"]]
                k["wer"], k["cer"] = round(sp.wer(ref["tekst"], k["tekst"]), 4), round(sp.cer(ref["tekst"], k["tekst"]), 4)
                hits, miss = sp.critical_hits(ref["kritiske"], k["tekst"])
                k["kritiske_treff"], k["kritiske_bom"], k["kritiske_totalt"] = len(hits), miss, len(ref["kritiske"])
        results.append(res)
        print("Modell %s: %s (%.0f s)" % (m, res.get("feil") or "%d klipp" % len(res["klipp"]), time.time() - t), flush=True)
    json.dump({"tid": now_iso(), "klipp": items, "modeller": results}, open(os.path.join(out, stem + "-resultater.json"), "w"), ensure_ascii=False, indent=2)
    report(out, items, results, a.rapport)
    print("Skrev " + a.rapport, flush=True)
    return 0


def report(out, items, results, name="LOKAL-RESULTAT.md"):
    tot = sum(i.get("sekunder_lyd", 0) for i in items if not i.get("feil"))
    L = ["# Lokal tale til tekst: mlx-whisper på Mac-en", "",
         "Kjørt %s av `tools/stt-benchmark/stt_lokal.py`." % now_iso() + (" Klippene er laget med macOS sin egen stemme (`say`), så ingen lyd eller tekst forlot Mac-en." if KILDE == "say" else " Klippene er de samme gpt-4o-mini-tts-klippene som NanoGPT-prøven brukte (`lyd/*.mp3`), gjort om til 16 kHz WAV. Transkripsjonen kjørte lokalt."), "",
         "**Forbehold:** syntetisk tale er renere enn ekte tale ved et bord. Tallene er trolig for gode. Prøvesettet er åtte setninger, så forskjeller på noen få prosentpoeng betyr lite.", "",
         "Lydlengde totalt: %.1f s." % tot, "",
         "| Modell | Klipp ok | Snitt WER | Snitt CER | Kritiske ord | Tid totalt (s) | Sanntidsfaktor | Modell på disk (MB) | Maks minne (MB) | Første kall inkl. nedlasting (s) | Feil |",
         "|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in results:
        ok = [k for k in r["klipp"] if k["tekst"] is not None]
        if not ok:
            L.append("| %s | 0 | - | - | - | - | - | - | - | - | %s |" % (r["motor"], (r.get("feil") or "")[:120]))
            continue
        secs = sum(k["sekunder"] for k in ok)
        L.append("| %s | %d/%d | %.1f %% | %.1f %% | %d/%d | %.1f | %.2f | %s | %s | %s | %s |" % (
            r["motor"], len(ok), len(r["klipp"]), 100 * sum(k["wer"] for k in ok) / len(ok), 100 * sum(k["cer"] for k in ok) / len(ok),
            sum(k["kritiske_treff"] for k in ok), sum(k["kritiske_totalt"] for k in ok), secs, secs / tot if tot else 0,
            r.get("modellstorrelse_mb", "?"), r.get("maks_minne_mb", "?"), r.get("sekunder_forste_inkl_nedlasting", "?"),
            "; ".join(sorted({k["feil"][:60] for k in r["klipp"] if k["feil"]})) or "-"))
    L += ["", "Sanntidsfaktor under 1 betyr raskere enn sanntid.", "", "## Per klipp", ""]
    for it in items:
        L += ["### %s (stemme %s, %s s)" % (it["id"], it.get("stemme"), it.get("sekunder_lyd", "?")), "", "Fasit: %s" % it["tekst"], ""]
        if it.get("feil"):
            L += ["Ikke laget: %s" % it["feil"], ""]
            continue
        L += ["| Modell | WER | Bom på kritiske ord | Transkripsjon |", "|---|---|---|---|"]
        for r in results:
            k = next((k for k in r["klipp"] if k["klipp"] == it["id"]), None)
            if k is None:
                continue
            if k["tekst"] is None:
                L.append("| %s | - | - | FEIL: %s |" % (r["motor"], k["feil"]))
            else:
                L.append("| %s | %.1f %% | %s | %s |" % (r["motor"], 100 * k["wer"], ", ".join(k["kritiske_bom"]) or "-", k["tekst"].replace("|", "/")))
        L.append("")
    open(os.path.join(out, name), "w", encoding="utf-8").write("\n".join(L) + "\n")


if __name__ == "__main__":
    sys.exit(main())
