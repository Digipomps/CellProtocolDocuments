#!/usr/bin/env python3
"""Modellprøve for tale til tekst på norsk (pc.stt.benchmark).

PDD: CellProtocolDocuments/Deliverables/PDD_palazzo-highend-mangler_2026-10-09

Hva den gjør:
1. Lager syntetisk norsk tale fra prøvesettet (proevesett.json) med en
   TTS-modell gjennom NanoGPT, og legger lyden i <out>/lyd/. Lyd som alt
   finnes lages ikke på nytt.
2. Tar også med egne opptak fra <out>/opptak/: <navn>.(m4a|mp3|wav) med
   fasit i <navn>.txt. Opptakene skal ikke inneholde personopplysninger.
3. Transkriberer hver fil med hver STT-modell gjennom NanoGPT, og med
   lokal whisper hvis mlx_whisper er installert.
4. Regner ut ordfeilrate (WER), tegnfeilrate (CER) og treff på kritiske
   ord (allergener, tall, navn), og skriver RESULTAT.md og resultater.json.

NanoGPT er en ekstern videreformidler. Den brukes bare til denne prøven,
med syntetisk tale. Ekte gjestelyd skal aldri sendes hit (FORMAALSSPEC §2).

Uten --go: tørrkjøring. Viser hva som ville skjedd og sjekker at nøkkel og
verktøy finnes, uten å sende noe.

Ren stdlib, Python 3.9+. Nøkkelen skrives aldri ut.
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
import unicodedata
import urllib.error
import urllib.request
import uuid
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
KEYCHAIN_SERVICE = "com.digipomps.cellscaffold.aigateway"
KEYCHAIN_ACCOUNT = "nanogpt"
BASE_URLS = ["https://nano-gpt.com/api/v1", "https://api.nano-gpt.com/api/v1"]

# Pris per minutt lyd, fra docs.nano-gpt.com/api-reference/speech-to-text (lest 2026-10-09).
STT_MODELS = {
    "Whisper-Large-V3": 0.0005,
    "Wizper": 0.01,
    "gpt-4o-mini-transcribe": 0.003,
    "Elevenlabs-STT": 0.03,
}
TTS_MODEL = "gpt-4o-mini-tts"
TTS_INSTRUCTIONS = "Snakk naturlig, i normalt tempo, som en person ved et restaurantbord."


def log(msg):
    print(msg, flush=True)


def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def get_key():
    key = os.environ.get("NANOGPT_API_KEY", "").strip()
    if key:
        return key, "miljøvariabel NANOGPT_API_KEY"
    if shutil.which("security"):
        try:
            out = subprocess.run(
                ["security", "find-generic-password", "-s", KEYCHAIN_SERVICE, "-a", KEYCHAIN_ACCOUNT, "-w"],
                capture_output=True, text=True, timeout=20,
            )
            if out.returncode == 0 and out.stdout.strip():
                return out.stdout.strip(), "nøkkelring %s / %s" % (KEYCHAIN_SERVICE, KEYCHAIN_ACCOUNT)
            return None, "nøkkelring svarte %d (finnes ikke eller ble nektet)" % out.returncode
        except subprocess.TimeoutExpired:
            return None, "nøkkelring svarte ikke innen 20 s (trolig en tilgangsdialog på skjermen)"
    return None, "ingen NANOGPT_API_KEY og ikke macOS-nøkkelring"


def http(url, key, data, headers, timeout=180):
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Authorization", "Bearer " + key)
    req.add_header("x-api-key", key)
    for k, v in headers.items():
        req.add_header(k, v)
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read()
            return resp.status, body, resp.headers.get("Content-Type", ""), time.time() - t0
    except urllib.error.HTTPError as e:
        return e.code, e.read(), e.headers.get("Content-Type", "") if e.headers else "", time.time() - t0


def scrub(text, key):
    return text.replace(key, "<nøkkel>") if key else text


def tts(base, key, text, voice, path):
    payload = json.dumps({
        "model": TTS_MODEL, "voice": voice, "input": text, "text": text,
        "response_format": "mp3", "instructions": TTS_INSTRUCTIONS,
    }).encode()
    status, body, ctype, secs = http(base + "/audio/speech", key, payload, {"Content-Type": "application/json"})
    if status == 200 and not ctype.startswith("application/json") and len(body) > 1000:
        with open(path, "wb") as f:
            f.write(body)
        return None, secs
    if status == 200 and ctype.startswith("application/json"):
        try:
            j = json.loads(body)
            url = j.get("audioUrl") or j.get("url")
            if url:
                with urllib.request.urlopen(url, timeout=120) as r, open(path, "wb") as f:
                    f.write(r.read())
                return None, secs
        except Exception as e:  # noqa: BLE001
            return "TTS-svar uten lyd: %s" % e, secs
    return "TTS HTTP %d: %s" % (status, scrub(body[:300].decode("utf-8", "replace"), key)), secs


def multipart(fields, file_field, file_path):
    boundary = "----stt" + uuid.uuid4().hex
    parts = []
    for name, value in fields.items():
        parts.append(("--%s\r\nContent-Disposition: form-data; name=\"%s\"\r\n\r\n%s\r\n" % (boundary, name, value)).encode())
    fname = os.path.basename(file_path)
    ext = fname.rsplit(".", 1)[-1].lower()
    mime = {"mp3": "audio/mpeg", "wav": "audio/wav", "m4a": "audio/mp4", "ogg": "audio/ogg", "aac": "audio/aac"}.get(ext, "application/octet-stream")
    with open(file_path, "rb") as f:
        data = f.read()
    parts.append(("--%s\r\nContent-Disposition: form-data; name=\"%s\"; filename=\"%s\"\r\nContent-Type: %s\r\n\r\n" % (boundary, file_field, fname, mime)).encode() + data + b"\r\n")
    parts.append(("--%s--\r\n" % boundary).encode())
    return b"".join(parts), "multipart/form-data; boundary=" + boundary


def stt_remote(base, key, model, path, lang):
    fields = {"model": model}
    if lang:
        fields["language"] = lang
    body, ctype = multipart(fields, "file", path)
    status, resp, rtype, secs = http(base + "/audio/transcriptions", key, body, {"Content-Type": ctype}, timeout=300)
    if status == 200:
        try:
            j = json.loads(resp)
            text = j.get("text")
            if text is None and isinstance(j.get("transcription"), str):
                text = j["transcription"]
            if text is None:
                return None, "svar uten text-felt: %s" % scrub(resp[:200].decode("utf-8", "replace"), key), secs
            return text, None, secs
        except ValueError:
            return resp.decode("utf-8", "replace"), None, secs
    return None, "HTTP %d: %s" % (status, scrub(resp[:300].decode("utf-8", "replace"), key)), secs


def stt_local_mlx(path, lang):
    exe = shutil.which("mlx_whisper")
    if not exe:
        return None, "ikke installert", 0.0
    outdir = os.path.join(os.path.dirname(path), "_mlx")
    os.makedirs(outdir, exist_ok=True)
    t0 = time.time()
    r = subprocess.run([exe, path, "--language", lang or "no", "--model", "mlx-community/whisper-large-v3-turbo",
                        "--output-format", "txt", "--output-dir", outdir], capture_output=True, text=True, timeout=600)
    secs = time.time() - t0
    txt = os.path.join(outdir, os.path.splitext(os.path.basename(path))[0] + ".txt")
    if r.returncode != 0 or not os.path.exists(txt):
        return None, "mlx_whisper feilet: %s" % r.stderr[-300:], secs
    with open(txt, encoding="utf-8") as f:
        return f.read(), None, secs



def normalize(text):
    text = unicodedata.normalize("NFC", text or "").lower()
    text = text.replace("-", " ")
    text = re.sub(r"[^\w\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def edit_distance(a, b):
    prev = list(range(len(b) + 1))
    for i, x in enumerate(a, 1):
        cur = [i] + [0] * len(b)
        for j, y in enumerate(b, 1):
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (x != y))
        prev = cur
    return prev[-1]


def wer(ref, hyp):
    r, h = normalize(ref).split(), normalize(hyp).split()
    return edit_distance(r, h) / max(1, len(r))


def cer(ref, hyp):
    r, h = normalize(ref).replace(" ", ""), normalize(hyp).replace(" ", "")
    return edit_distance(list(r), list(h)) / max(1, len(r))


def critical_hits(critical, hyp):
    h = normalize(hyp)
    hits = [c for c in critical if normalize(c) in h]
    return hits, [c for c in critical if c not in hits]


def audio_seconds(path):
    for tool in ("afinfo", "ffprobe"):
        exe = shutil.which(tool)
        if not exe:
            continue
        try:
            if tool == "afinfo":
                out = subprocess.run([exe, path], capture_output=True, text=True, timeout=20).stdout
                m = re.search(r"estimated duration:\s*([\d.]+)", out)
            else:
                out = subprocess.run([exe, "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", path],
                                     capture_output=True, text=True, timeout=20).stdout
                m = re.search(r"([\d.]+)", out)
            if m:
                return float(m.group(1))
        except Exception:  # noqa: BLE001
            pass
    return None


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def load_items(out):
    with open(os.path.join(HERE, "proevesett.json"), encoding="utf-8") as f:
        spec = json.load(f)
    items = []
    for c in spec["klipp"]:
        items.append({"id": c["id"], "kilde": "syntetisk", "tekst": c["tekst"], "stemme": c["stemme"],
                      "spraak": c.get("spraak", "no"), "kritiske": c.get("kritiske", []),
                      "fil": os.path.join(out, "lyd", c["id"] + ".mp3")})
    odir = os.path.join(out, "opptak")
    if os.path.isdir(odir):
        for name in sorted(os.listdir(odir)):
            stem, ext = os.path.splitext(name)
            if ext.lower() in (".m4a", ".mp3", ".wav") and os.path.exists(os.path.join(odir, stem + ".txt")):
                with open(os.path.join(odir, stem + ".txt"), encoding="utf-8") as f:
                    ref = f.read().strip()
                items.append({"id": "opptak-" + stem, "kilde": "opptak", "tekst": ref, "stemme": "-",
                              "spraak": "no", "kritiske": [], "fil": os.path.join(odir, name)})
    return items


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--go", action="store_true", help="Send forespørsler. Uten: tørrkjøring.")
    ap.add_argument("--models", default=",".join(STT_MODELS))
    args = ap.parse_args()
    out = os.path.abspath(args.out)
    os.makedirs(os.path.join(out, "lyd"), exist_ok=True)
    models = [m for m in args.models.split(",") if m]

    log("STT-prøve %s, ut: %s, modus: %s" % (now_iso(), out, "KJØR" if args.go else "TØRRKJØRING"))
    key, key_src = get_key()
    log("Nøkkel: %s (%s)" % ("funnet" if key else "MANGLER", key_src))
    log("Lokal mlx_whisper: %s" % (shutil.which("mlx_whisper") or "ikke installert"))
    log("whisper-cli (whisper.cpp): %s" % (shutil.which("whisper-cli") or "ikke installert"))
    try:
        log("macOS: %s" % subprocess.run(["sw_vers", "-productVersion"], capture_output=True, text=True).stdout.strip())
    except Exception:  # noqa: BLE001
        log("macOS: ukjent")
    items = load_items(out)
    log("Klipp: %d (%d syntetiske, %d opptak). Modeller: %s" % (
        len(items), sum(i["kilde"] == "syntetisk" for i in items), sum(i["kilde"] == "opptak" for i in items), ", ".join(models)))
    if not args.go:
        log("Tørrkjøring ferdig. Kjør med --go for å lage lyd og transkribere.")
        return 0
    if not key:
        log("STOPP: ingen nøkkel. Sett NANOGPT_API_KEY eller legg nøkkelen i nøkkelringen.")
        return 2

    base = BASE_URLS[0]
    runs = []
    for it in items:
        if it["kilde"] == "syntetisk" and not os.path.exists(it["fil"]):
            err, secs = tts(base, key, it["tekst"], it["stemme"], it["fil"])
            if err and "404" in err and base == BASE_URLS[0]:
                base = BASE_URLS[1]
                err, secs = tts(base, key, it["tekst"], it["stemme"], it["fil"])
            log("TTS %s: %s (%.1f s)" % (it["id"], err or "ok", secs))
            if err:
                it["feil"] = err
                continue
        it["sekunder_lyd"] = audio_seconds(it["fil"])
        it["sha256"] = sha256(it["fil"])
        for model in models:
            text, err, secs = stt_remote(base, key, model, it["fil"], it["spraak"])
            runs.append({"klipp": it["id"], "motor": "nanogpt:" + model, "tekst": text, "feil": err, "sekunder": round(secs, 2)})
            log("STT %-28s %-14s %s (%.1f s)" % (model, it["id"], "ok" if text is not None else err, secs))
        text, err, secs = stt_local_mlx(it["fil"], it["spraak"])
        if err != "ikke installert":
            runs.append({"klipp": it["id"], "motor": "lokal:mlx-whisper-large-v3-turbo", "tekst": text, "feil": err, "sekunder": round(secs, 2)})

    by_id = {i["id"]: i for i in items}
    for r in runs:
        if r["tekst"] is not None:
            it = by_id[r["klipp"]]
            r["wer"] = round(wer(it["tekst"], r["tekst"]), 4)
            r["cer"] = round(cer(it["tekst"], r["tekst"]), 4)
            hits, misses = critical_hits(it["kritiske"], r["tekst"])
            r["kritiske_treff"], r["kritiske_bom"] = len(hits), misses

    with open(os.path.join(out, "resultater.json"), "w", encoding="utf-8") as f:
        json.dump({"tid": now_iso(), "base": base, "tts": TTS_MODEL, "klipp": items, "kjoringer": runs}, f, ensure_ascii=False, indent=2)
    write_report(out, items, runs, base)
    log("Skrev %s og resultater.json" % os.path.join(out, "RESULTAT.md"))
    return 0


def write_report(out, items, runs, base):
    motors = sorted({r["motor"] for r in runs})
    total_min = sum((i.get("sekunder_lyd") or 0) for i in items) / 60.0
    lines = [
        "# Modellprøve: tale til tekst på norsk",
        "",
        "Kjørt %s av `tools/stt-benchmark/stt_proeve.py` (pc.stt.benchmark). API: `%s`." % (now_iso(), base),
        "",
        "**Forbehold:** de syntetiske klippene er laget med %s. Syntetisk tale er renere enn ekte tale ved et bord, så feilratene er trolig for lave. Ekte opptak legges i `opptak/` med fasit i `.txt` og tas med neste kjøring." % TTS_MODEL,
        "",
        "NanoGPT er en ekstern tjeneste og brukes bare til denne prøven. Ingen av motorene her er godkjent for gjestelyd.",
        "",
        "## Sammendrag per motor",
        "",
        "| Motor | Klipp ok | Snitt WER | Snitt CER | Kritiske ord truffet | Median tid (s) | Anslått pris for settet (USD) | Feil |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for m in motors:
        rs = [r for r in runs if r["motor"] == m]
        ok = [r for r in rs if r["tekst"] is not None]
        crit_total = sum(len([c for c in next(i for i in items if i["id"] == r["klipp"])["kritiske"]]) for r in ok)
        crit_hit = sum(r.get("kritiske_treff", 0) for r in ok)
        secs = sorted(r["sekunder"] for r in ok)
        med = secs[len(secs) // 2] if secs else 0
        price = STT_MODELS.get(m.split(":", 1)[1])
        cost = "%.4f" % (price * total_min) if price is not None else "0 (lokal)"
        avg = lambda k: ("%.1f %%" % (100 * sum(r[k] for r in ok) / len(ok))) if ok else "-"
        errs = "; ".join(sorted({(r["feil"] or "")[:80] for r in rs if r["feil"]}))
        lines.append("| %s | %d/%d | %s | %s | %d/%d | %.1f | %s | %s |" % (m, len(ok), len(rs), avg("wer"), avg("cer"), crit_hit, crit_total, med, cost, errs or "-"))
    lines += ["", "## Per klipp", ""]
    for it in items:
        lines += ["### %s (%s, stemme %s, %s s)" % (it["id"], it["kilde"], it["stemme"], ("%.1f" % it["sekunder_lyd"]) if it.get("sekunder_lyd") else "?"),
                  "", "Fasit: %s" % it["tekst"], ""]
        if it.get("feil"):
            lines += ["Lyd ble ikke laget: %s" % it["feil"], ""]
            continue
        lines += ["| Motor | WER | CER | Bom på kritiske ord | Transkripsjon |", "|---|---|---|---|---|"]
        for r in [r for r in runs if r["klipp"] == it["id"]]:
            if r["tekst"] is None:
                lines.append("| %s | - | - | - | FEIL: %s |" % (r["motor"], (r["feil"] or "")[:120]))
            else:
                lines.append("| %s | %.1f %% | %.1f %% | %s | %s |" % (r["motor"], 100 * r["wer"], 100 * r["cer"],
                             ", ".join(r.get("kritiske_bom", [])) or "-", r["tekst"].replace("|", "/").replace("\n", " ")))
        lines.append("")
    lines += ["## Lydfiler", "", "| Klipp | sha256 |", "|---|---|"]
    lines += ["| %s | `%s` |" % (i["id"], i.get("sha256", "-")) for i in items]
    with open(os.path.join(out, "RESULTAT.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    sys.exit(main())
