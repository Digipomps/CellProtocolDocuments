#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Kontrollerer at eksemplene i denne mappen holder kontraktene.

Kjør fra mappen: python3 kontroller_kontrakt.py
Krever pakken jsonschema. Skriver resultatet til skjermen; siste linje sier hvor mange kontroller som holdt.

Reglene som er portert fra Swift, står med kilden ved siden av. `referanse/agent-challenge-v1.schema.json`
er en kopi av `Contracts/agent-challenge-v1.schema.json` på `origin/main` (ea558ba, 02.10.2026).
"""
import glob
import hashlib
import json
import os
import sys

import jsonschema

from cron_reference import main as cron_main

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
results = []


def check(name, ok, detail=""):
    results.append((name, bool(ok), detail))
    print(("ok    " if ok else "FEIL  ") + name + (f" — {detail}" if detail and not ok else ""))


def load(path):
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


# --- portert fra AgentChallengeTextSafety.looksLikeSecret (AgentChallenge.swift) ---
TRIM = ".,;:()[]{}«»\"'"


def secret_like_word(word):
    if len(word) < 24:
        return False
    has_letter = has_digit = False
    all_hex = True
    for ch in word:
        if ("A" <= ch <= "Z") or ("a" <= ch <= "z"):
            has_letter = True
            if ch.lower() not in "abcdef":
                all_hex = False
        elif "0" <= ch <= "9":
            has_digit = True
        elif ch in "_-":
            all_hex = False
        else:
            return False
    if all_hex and len(word) >= 32:
        return True
    return has_letter and has_digit


def looks_like_secret(text):
    for word in text.replace("\n", " ").replace("\t", " ").split(" "):
        if word and secret_like_word(word.strip(TRIM)):
            return True
    return "-----BEGIN" in text


# --- portert fra CorrespondenceWaitingStore.isFileSafe og CorrespondenceWaitingItem.validate ---
def file_safe(identifier):
    if not identifier or len(identifier) > 120 or identifier.startswith("."):
        return False
    return all(("a" <= c <= "z") or ("A" <= c <= "Z") or ("0" <= c <= "9") or c in "-_." for c in identifier)


def marker_problem(item):
    if item.get("schema") != "haven.correspondence-waiting.v1":
        return "feil skjema"
    if not file_safe(item.get("id", "")):
        return "id er ikke filtrygg"
    summary = item.get("summary", "")
    if not summary or len(summary) > 200:
        return f"sammendraget er {len(summary)} tegn"
    if looks_like_secret(summary):
        return "sammendraget likner en hemmelighet"
    sender = item.get("from")
    if sender is not None and looks_like_secret(sender):
        return "avsenderen likner en hemmelighet"
    if sender is not None and len(sender) > 56:
        return f"avsenderen er {len(sender)} tegn"
    title = f"Post fra {sender} venter på svar" if sender else "Post venter på svar"
    if len(title) > 80:
        return f"tittelen blir {len(title)} tegn"
    return None


# 1. Markørene programmene skriver
for path in sorted(glob.glob("fixtures/markor-*.json")):
    item = load(path)
    problem = marker_problem(item)
    check(f"markør {os.path.basename(path)}", problem is None, problem or "")
    check(f"markør {os.path.basename(path)}: markedBy er programmets eget",
          item.get("markedBy") in ("agent-korrespondansesjekk", "agent-korrespondansefrist"))

# 2. Tekst som skal nektes
bad = load("fixtures/ugyldig-tekst.json")
for case in bad["tilfeller"]:
    value, field = case["verdi"], case["felt"]
    if field == "from":
        caught = looks_like_secret(value) or len(value) > 56
    elif field == "summary":
        caught = looks_like_secret(value)
    else:
        caught = not file_safe(value)
    check(f"utrygg {field}: {case['hvorfor']}", caught)
    replacement = case["skrives"]
    if field == "id" and not replacement.startswith("("):
        check(f"erstatningen for id er filtrygg: {replacement}", file_safe(replacement))
for value in bad["trygt"]:
    check(f"trygg tekst slipper gjennom: {value[:40]}", not looks_like_secret(value))

# 3. Skjema mot eksempel
JOBS = "fixtures/ScheduledJobs"
PAIRS = [
    ("scheduled-task-stamp-v1.schema.json", ["fixtures/stempel-korrespondanse-sjekk.json", "fixtures/stempel-korrespondanse-frist.json"]),
    ("scheduled-job-v1.schema.json", [JOBS + "/post-oftere-under-fornyelsen.spec.json", JOBS + "/regresjon-havenagentd.spec.json"]),
    ("scheduled-job-control-v1.schema.json", [JOBS + "/regresjon-havenagentd.control.json"]),
    ("scheduled-job-approval-v1.schema.json", [JOBS + "/regresjon-havenagentd.approval.json"]),
    ("scheduled-job-runtime-v1.schema.json", [JOBS + "/regresjon-havenagentd.runtime.json"]),
    ("scheduled-job-ack-v1.schema.json", [JOBS + "/regresjon-havenagentd.ack.json"]),
    ("scheduled-jobs-status-v1.schema.json", ["fixtures/status.example.json"]),
    ("referanse/agent-challenge-v1.schema.json", ["saker-job.example.json"]),
]
for schema_path, examples in PAIRS:
    schema = load(schema_path)
    try:
        jsonschema.Draft202012Validator.check_schema(schema)
        check(f"skjemaet er gyldig: {schema_path}", True)
    except jsonschema.SchemaError as error:
        check(f"skjemaet er gyldig: {schema_path}", False, str(error)[:200])
        continue
    validator = jsonschema.Draft202012Validator(schema)
    for example in examples:
        errors = sorted(validator.iter_errors(load(example)), key=lambda e: list(e.path))
        check(f"{example} følger {schema_path}", not errors, "; ".join(e.message[:120] for e in errors[:3]))

# 4. Sakene: reglene Swift-koden håndhever i tillegg til skjemaet (AgentChallenge.validate, AgentChallengeInbox.validate)
inbox = load("saker-job.example.json")
ids = [c["id"] for c in inbox["challenges"]]
check("sakene har ulike id-er", len(ids) == len(set(ids)))
sources = [s["source"] for s in inbox["sources"]]
check("alle seks kildene står nøyaktig én gang",
      sorted(sources) == sorted(["intent-review", "scaffold-queue", "agent-health", "job", "correspondence", "tool-link"]))
for challenge in inbox["challenges"]:
    cid = challenge["id"]
    check(f"sak {cid}: tittel høyst 80 tegn", len(challenge["title"]) <= 80, str(len(challenge["title"])))
    check(f"sak {cid}: detalj høyst 400 tegn", len(challenge.get("detail") or "") <= 400, str(len(challenge.get("detail") or "")))
    check(f"sak {cid}: «Gjelder» høyst 200 tegn", len(challenge.get("subject") or "") <= 200)
    texts = [challenge["title"], challenge.get("detail") or "", challenge.get("subject") or "",
             (challenge.get("handleAt") or {}).get("reason", "")]
    texts += [r["label"] for r in challenge["responses"]]
    check(f"sak {cid}: ingen tekst likner en hemmelighet", not any(looks_like_secret(t) for t in texts))
    check(f"sak {cid}: kilden er job", challenge["source"] == "job")
    allowed = {"approve", "reject", "open", "dismiss-today"}
    check(f"sak {cid}: bare svar som finnes i kontrakten", {r["id"] for r in challenge["responses"]} <= allowed)
for status in inbox["sources"]:
    if status["state"] != "read":
        check(f"kilde {status['source']}: grunnen likner ikke en hemmelighet", not looks_like_secret(status.get("reason") or ""))

# 4b. Saker om faste hendelser har bare «Kvitter» og «Åpne», og titler holder seg innenfor 80 tegn
fixed_ids = {e["id"] for e in load("config-tillegg-trinn1-2.json")["scheduledEvents"]}
for challenge in inbox["challenges"]:
    parts = challenge["id"].split(":")
    if len(parts) == 4 and parts[:2] == ["job", "scheduled"] and parts[3] == "attention":
        reject = [r for r in challenge["responses"] if r["id"] == "reject"]
        labels = [r["label"] for r in challenge["responses"]]
        if parts[2] in fixed_ids:
            check(f"sak {challenge['id']}: en fast hendelse har bare «Kvitter» og «Åpne»", labels == ["Kvitter", "Åpne"] and not reject)
            check(f"sak {challenge['id']}: begrunnelsen lover verken stopp eller pause",
                  "stopp" not in challenge["handleAt"]["reason"] and "pause" not in challenge["handleAt"]["reason"])
        else:
            check(f"sak {challenge['id']}: en jobb som er bedt om, har «Stopp jobben»", [r["label"] for r in reject] == ["Stopp jobben"])

MAX_TITLE = 80


def case_title(prefix, name):
    """Slik agenten avkorter: 79 tegn og «…» (som CorrespondenceWaitingItem.asChallenge)."""
    title = prefix + name
    return title if len(title) <= MAX_TITLE else title[:MAX_TITLE - 1] + "…"


worst_approval = "En assistent ber om en planlagt jobb: «" + "x" * 40 + "»"
check("lengste godkjenningstittel (lengste navn, tittel på 40 tegn) er høyst 80 tegn", len(worst_approval) <= MAX_TITLE, str(len(worst_approval)))
for prefix in ("Planlagt jobb kan ikke kjøres: ", "Planlagt jobb ble passert: ", "Planlagt jobb feilet: "):
    shown = case_title(prefix, "a" * 60)
    check(f"«{prefix.strip()}» med en id på 60 tegn avkortes til 80", len(shown) == MAX_TITLE and shown.endswith("…"))
    check(f"«{prefix.strip()}» med en tittel på 40 tegn avkortes ikke", case_title(prefix, "x" * 40) == prefix + "x" * 40)

# 5. Sjekksummene henger sammen
def digest(path):
    with open(path, "rb") as handle:
        return "sha256:" + hashlib.sha256(handle.read()).hexdigest()

spec = load(JOBS + "/regresjon-havenagentd.spec.json")
spec_digest = digest(JOBS + "/regresjon-havenagentd.spec.json")
check("godkjenningen peker på spec-filas sjekksum", load(JOBS + "/regresjon-havenagentd.approval.json")["specDigest"] == spec_digest)
check("kjøretilstanden peker på spec-filas sjekksum", load(JOBS + "/regresjon-havenagentd.runtime.json")["specDigest"] == spec_digest)
template_digest = spec["action"]["templateDigest"]
template_path = JOBS + "/regresjon-havenagentd." + template_digest[len("sha256:"):][:12] + ".spool.json"
check("jobbmalen ligger under navnet sjekksummen gir", os.path.exists(template_path))
check("spec-fila peker på jobbmalens sjekksum", os.path.exists(template_path) and template_digest == digest(template_path))
approval_case = next(c for c in inbox["challenges"] if ":approval:" in c["id"])
check("sakens id bærer de tolv første tegnene i sjekksummen", approval_case["id"].endswith(":" + spec_digest[len("sha256:"):][:12]))
check("kvitteringen gjelder tidspunktet saken gjaldt",
      load(JOBS + "/regresjon-havenagentd.ack.json")["throughOccurrence"]
      == load(JOBS + "/regresjon-havenagentd.runtime.json")["attention"]["occurrence"])
check("godkjenningssaken setter tittelen fra bestillingen i anførselstegn", "«" + spec["title"] + "»" in approval_case["title"])

# 5b. Køfilas navn går gjennom køens eget mønster (JOB_ID_RE i .agent-tools/agent_job_runner.py linje 40)
import re
JOB_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,120}$")
runtime = load(JOBS + "/regresjon-havenagentd.runtime.json")
occurrence = runtime["lastRun"]["occurrence"].replace("-", "").replace(":", "")
spool_name = f"{spec['id']}-{occurrence}"
check(f"køfilas navn tas av køen: {spool_name}.json", bool(JOB_ID_RE.match(spool_name)))
check("et tidspunkt med kolon ville blitt avvist av køen", not JOB_ID_RE.match(f"{spec['id']}-{runtime['lastRun']['occurrence']}"))
check("lengste id pluss tidspunkt får plass i køens mønster", bool(JOB_ID_RE.match("a" * 64 + "-" + occurrence)))

status_example = load("fixtures/status.example.json")
check("faste hendelser i statuslista kan ikke stoppes",
      all(item["canStop"] is False for item in status_example["items"] if item["origin"] == "config"))

# 6. Eksempelmalen bruker bare programmer og underkommandoer som står på køens tillatt-liste.
#    Dette er en kontroll av eksempelet, ikke en regel agenten håndhever: køen håndhever sin egen liste
#    (check_command i .agent-tools/agent_job_runner.py, som også har forbudte flagg og vernede utsjekker).
ALLOWED = {
    "scripts/run_swift_bounded.sh": None,
    "swift": {"build", "test", "package"},
    "git": {"status", "diff", "log", "show", "rev-parse", "branch", "fetch", "add", "commit", "push", "checkout",
            "switch", "restore", "stash", "worktree", "remote", "describe", "ls-files"},
    "gh": {"pr", "repo", "run", "api"},
    ".agent-tools/disk_report.py": None,
    "CellScaffold/scripts/haven_learn.py": None,
    "CellScaffold/scripts/sync_claude_desktop_skills.py": None,
}
template = load(template_path)
for step in template["steps"]:
    cmd = step["cmd"]
    ok = cmd[0] in ALLOWED and (ALLOWED[cmd[0]] is None or (len(cmd) > 1 and cmd[1] in ALLOWED[cmd[0]]))
    check(f"steget «{' '.join(cmd)}» står på køens tillatt-liste", ok)

# 6b. Formkontrollen agenten gjør når en køjobb bes om (trinn4, bestillingen punkt 4)
def template_problem(candidate):
    cwd = candidate.get("cwd")
    if not isinstance(cwd, str) or cwd.startswith("/") or ".." in cwd.split("/"):
        return "cwd"
    steps = candidate.get("steps")
    if not isinstance(steps, list) or not steps:
        return "steps"
    for step in steps:
        cmd = step.get("cmd") if isinstance(step, dict) else None
        if not isinstance(cmd, list) or not cmd or not all(isinstance(part, str) for part in cmd):
            return "cmd"
        timeout = step.get("timeoutSeconds")
        if timeout is not None and (isinstance(timeout, bool) or not isinstance(timeout, int) or not 1 <= timeout <= 10800):
            return "timeoutSeconds"
        if "name" in step and not isinstance(step["name"], str):
            return "name"
    if "stopOnFailure" in candidate and not isinstance(candidate["stopOnFailure"], bool):
        return "stopOnFailure"
    env = candidate.get("env")
    if env is not None:
        if not isinstance(env, dict):
            return "env"
        if any(not key.startswith("HAVEN_") or not isinstance(value, str) for key, value in env.items()):
            return "env"
    return None


check("eksempelmalen holder formkontrollen", template_problem(template) is None)
for name, bad in (
    ("env med en nøkkel utenom HAVEN_", dict(template, env={"PATH": "/tmp"})),
    ("env som ikke er et objekt", dict(template, env=["HAVEN_X=1"])),
    ("en mal uten steg", dict(template, steps=[])),
    ("et steg uten ledd", dict(template, steps=[{"name": "tom", "cmd": []}])),
    ("tekst i timeoutSeconds", dict(template, steps=[{"name": "x", "cmd": ["git", "status"], "timeoutSeconds": "60"}])),
    ("timeoutSeconds over køens tak", dict(template, steps=[{"name": "x", "cmd": ["git", "status"], "timeoutSeconds": 10801}])),
    ("name som ikke er tekst", dict(template, steps=[{"name": 7, "cmd": ["git", "status"]}])),
    ("stopOnFailure som tekst", dict(template, stopOnFailure="nei")),
    ("cwd med ..", dict(template, cwd="../utenfor")),
    ("absolutt cwd", dict(template, cwd="/tmp")),
):
    check(f"formkontrollen avviser {name}", template_problem(bad) is not None)
check("formkontrollen slipper env med HAVEN_-nøkler", template_problem(dict(template, env={"HAVEN_SWIFT_JOBS": "2"})) is None)

# 7. Tillegget i config.json
addition = load("config-tillegg-trinn1-2.json")
task_ids = set()
for task in addition["automationPolicy.localTasks"]:
    task_ids.add(task["id"])
    check(f"fast program {task['id']}: nøyaktig feltene LocalTaskDefinition har",
          set(task) == {"id", "description", "executablePath", "arguments", "requiresUserSession"})
    check(f"fast program {task['id']}: absolutt sti og argumenter på én linje",
          task["executablePath"].startswith("/") and all("\n" not in a for a in task["arguments"]))
    check(f"fast program {task['id']}: alle stier i argumentene er absolutte",
          all(a.startswith("/") for a in task["arguments"] if "/" in a and "=" not in a))
for event in addition["scheduledEvents"]:
    check(f"hendelse {event['id']}: id-en er høyst 40 tegn, så sakstittelen får plass uten title", len(event["id"]) <= 40)
    check(f"hendelse {event['id']}: peker på et fast program i tillegget", event["action"]["id"] in task_ids and event["action"]["kind"] == "localTask")
    check(f"hendelse {event['id']}: gjentas til den stoppes, med intervall",
          event["repeatMode"] == "untilStopped" and event["intervalSeconds"] > 0)
check("korrespondanse-sjekk står før korrespondanse-frist", [e["id"] for e in addition["scheduledEvents"]] == ["korrespondanse-sjekk", "korrespondanse-frist"])

# 8. MCP-verktøyene
tools = load("mcp-verktoy.json")["verktoy"]
names = [t["name"] for t in tools]
check("verktøynavnene er ulike og begynner med agent.schedule.", len(names) == len(set(names)) and all(n.startswith("agent.schedule.") for n in names))
check("ingen verktøy godkjenner eller kvitterer", not any(w in n for n in names for w in ("approve", "ack", "decide")))
check("verktøyene som styrer, sier at faste hendelser avvises",
      all("fixed-event" in t.get("errors", []) for t in tools if t["name"].split(".")[-1] in ("pause", "resume", "stop", "remove")))
for tool in tools:
    try:
        jsonschema.Draft202012Validator.check_schema(tool["inputSchema"])
        check(f"{tool['name']}: inputSchema er gyldig", True)
    except jsonschema.SchemaError as error:
        check(f"{tool['name']}: inputSchema er gyldig", False, str(error)[:160])
codes = load("mcp-verktoy.json")["feilkoder"]
check("spool-not-enabled nevner begge nøklene", "spoolInbox" in codes["spool-not-enabled"] and "spoolOutbox" in codes["spool-not-enabled"])
check("invalid-job nevner env og HAVEN_", "env" in codes["invalid-job"] and "HAVEN_" in codes["invalid-job"])
example_result = tools[0]["result"]
check("eksempelsvaret fra agent.schedule.request peker på samme sak som i innboksen", example_result["challengeId"] == approval_case["id"])
check("eksempelsvaret viser samme tittel som saken", example_result["shown"]["title"] == approval_case["title"])

# 9. Cron-fasiten
print("--- cron")
cron_rc = cron_main(["cron_reference.py", "kontroller", "fixtures/cron-forventninger.json"])
check("cron-referansen gir fasiten", cron_rc == 0)

failed = [r for r in results if not r[1]]
print(f"\n{len(results) - len(failed)} av {len(results)} kontroller holdt")
sys.exit(1 if failed else 0)
