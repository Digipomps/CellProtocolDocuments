"""Human G1 judgments. Standard library only; never infers a human answer."""
from __future__ import annotations

import datetime as dt
import json
from pathlib import Path
import re
import time


SCHEMA = Path(__file__).with_name("matching_judgment.schema.json")


def validate_schema(value, schema=None, root=None):
    """Validate the subset used by our schema, not arbitrary JSON Schema."""
    schema = schema if schema is not None else json.loads(SCHEMA.read_text())
    root = root or schema
    if "$ref" in schema:
        return validate_schema(value, root["$defs"][schema["$ref"].split("/")[-1]], root)
    if "oneOf" in schema:
        valid = 0
        for branch in schema["oneOf"]:
            try:
                validate_schema(value, branch, root)
                valid += 1
            except ValueError:
                pass
        if valid != 1:
            raise ValueError("oneOf: nøyaktig én gyldig variant kreves")
    types = {"object": lambda v: isinstance(v, dict), "array": lambda v: isinstance(v, list),
             "string": lambda v: isinstance(v, str), "boolean": lambda v: type(v) is bool,
             "number": lambda v: type(v) in (int, float), "null": lambda v: v is None}
    if "type" in schema:
        allowed = schema["type"] if isinstance(schema["type"], list) else [schema["type"]]
        if not any(types[t](value) for t in allowed):
            raise ValueError(f"feil datatype, ventet {allowed}")
    if "const" in schema and (type(value) is not type(schema["const"]) or value != schema["const"]):
        raise ValueError("feil konstant")
    if "enum" in schema and value not in schema["enum"]:
        raise ValueError("ugyldig enum")
    if isinstance(value, dict):
        if set(schema.get("required", [])) - value.keys():
            raise ValueError("mangler påkrevd felt")
        props = schema.get("properties", {})
        for key, item in value.items():
            child = props.get(key, schema.get("additionalProperties", {}))
            if child is False:
                raise ValueError(f"ukjent felt: {key}")
            validate_schema(item, child, root)
    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            raise ValueError("for få elementer")
        if schema.get("uniqueItems") and len({json.dumps(v, sort_keys=True) for v in value}) != len(value):
            raise ValueError("duplikat")
        for item in value:
            validate_schema(item, schema.get("items", {}), root)
    if isinstance(value, str):
        if len(value.strip()) < schema.get("minLength", 0) or ("pattern" in schema and not re.search(schema["pattern"], value)):
            raise ValueError("tom/ugyldig tekst eller referanse")
    if type(value) in (int, float) and value < schema.get("minimum", float("-inf")):
        raise ValueError("for lav verdi")


def validate_record(record):
    validate_schema(record)
    lessons = {x["lessonRef"]: x for x in record["lessons"]}
    if len(lessons) != len(record["lessons"]):
        raise ValueError("duplisert lærdom i snapshot")
    shown = set(record["presented"])
    if not shown <= lessons.keys():
        raise ValueError("vist lærdom mangler i snapshot")
    for refs in record["rankings"].values():
        if not set(refs) <= lessons.keys():
            raise ValueError("rangering peker utenfor snapshot")
    judged = set()
    for row in record["judgments"]:
        ref = row["lessonRef"]
        if ref not in shown or ref in judged:
            raise ValueError("dom må gjelde én unik vist lærdom")
        judged.add(ref)
        prior = row["repeatOf"]
        if prior is not None:
            if prior not in lessons or lessons[prior]["date"] >= lessons[ref]["date"]:
                raise ValueError("repeatOf må peke på en kjent, strengt tidligere lærdom (dato)")
        if "preventedBy" in row and row["preventedBy"] not in record["tests"]:
            raise ValueError("preventedBy finnes ikke blant snapshotets derivedTests")
    return record


def save_record(path, record):
    validate_record(record)
    path = Path(path)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)


def _indices(text, size):
    out = set()
    if text.strip() == "-":
        return out
    for part in text.replace(",", " ").split():
        if not part.isdigit() or not 1 <= int(part) <= size:
            raise ValueError("bruk nummer fra listen, eller - for ingen")
        out.add(int(part))
    if not out:
        raise ValueError("tomt svar er ikke en vurdering")
    return out


def judge(taskdir, run_path=None, batch_size=0, input_fn=input):
    """One short recording round after the G1 reading. Save partial work, resume."""
    path = Path(taskdir) / "MATCHING_FASIT.json"
    if batch_size < 0:
        raise ValueError("batch-size må være minst 0 (0 = alle)")
    if path.exists():
        record = validate_record(json.loads(path.read_text()))
        if run_path:
            supplied = validate_record(json.loads(Path(run_path).read_text()))
            immutable = set(record) - {"judgments", "annotationSeconds", "updatedAt"}
            if any(record[k] != supplied[k] for k in immutable):
                raise ValueError("eksisterende fasit tilhører en annen kjøring; skriv den ikke over")
    elif run_path:
        record = validate_record(json.loads(Path(run_path).read_text()))
    else:
        raise ValueError("første runde krever --run fra evaluer.py pool")
    if record["taskRef"] != Path(taskdir).resolve().name:
        raise ValueError("oppgavemappen stemmer ikke med kjøringen")
    done = {j["lessonRef"] for j in record["judgments"]}
    pending = [r for r in record["presented"] if r not in done]
    if not pending:
        if not path.exists():
            save_record(path, record)
        print("Alle viste lærdommer er allerede vurdert.")
        return 0
    batch = pending[:batch_size] if batch_size else pending
    lessons = {l["lessonRef"]: l for l in record["lessons"]}
    print("G1: Ville lærdommen endret et konkret valg, en test eller en avgrensning?")
    print("Registrer etter lesingen. Ukjent blir stående uvurdert; ingen automatisk nei.")
    start = time.monotonic()
    for i, ref in enumerate(batch, 1):
        hint = " ".join(lessons[ref]["symptom"].split())
        print(f"{i}. {ref} — {hint[:100]}{'…' if len(hint) > 100 else ''}")
    print("v 1 2 viser full symptom/forebygging for disse numrene.")
    print("\nSkriv relevante nummer; andre blir eksplisitt nei. ? foran nummer = uvurdert.")
    try:
        while True:
            try:
                answer = input_fn("Treff (f.eks. 1 3 ?4; - = ingen; q = avbryt): ").strip()
                if answer == "q":
                    return 1
                if answer.startswith("v "):
                    for i in sorted(_indices(answer[2:], len(batch))):
                        lesson = lessons[batch[i-1]]
                        print(f"{i}. {lesson['symptom']}\nForebygging: {lesson['prevention']}")
                    continue
                parts = answer.replace(",", " ").split()
                unknown = _indices(" ".join(p[1:] for p in parts if p.startswith("?")) or "-", len(batch))
                positive = _indices(" ".join(p for p in parts if not p.startswith("?")) or ("-" if unknown else ""), len(batch))
                if unknown & positive:
                    raise ValueError("samme nummer kan ikke være treff og ukjent")
                break
            except ValueError as exc:
                print(exc)
        rows = {i: {"lessonRef": ref, "relevant": i in positive, "repeatOf": None}
                for i, ref in enumerate(batch, 1) if i not in unknown}
        print("Gjentakelse betyr samme feilmekanisme, ikke bare samme tema.")
        while True:
            try:
                answer = input_fn("Gjentakelser som nr=lesson.ref, eller - (ingen): ").strip()
                if not answer:
                    raise ValueError("svar eksplisitt; - betyr ingen gjentakelse")
                repeats = {}
                if answer != "-":
                    for part in answer.split():
                        idx, ref = part.split("=", 1)
                        i = int(idx)
                        if i not in rows or ref not in lessons or lessons[ref]["date"] >= lessons[rows[i]["lessonRef"]]["date"]:
                            raise ValueError("repeatOf må være kjent og strengt tidligere; nummeret må være vurdert")
                        repeats[i] = ref
                for i, ref in repeats.items():
                    rows[i]["repeatOf"] = ref
                break
            except (ValueError, KeyError):
                print("Ugyldig gjentakelsesreferanse; ingen endringer lagret.")
        if positive:
            print("Håndhevelse for hvert treff: nr=test.ref eller nr=u:grunn (f.eks. 1=u:mangler-test).")
            print("u:grunn alene gjelder alle treff; ? viser kjente derivedTests.")
            print("En testref er planlagt vern, ikke bevis for effekt.")
            while True:
                try:
                    answer = input_fn("Håndhevelse: ").strip()
                    if answer == "?":
                        print(", ".join(record["tests"]))
                        continue
                    assignments = ({i: answer for i in positive} if answer.startswith("u:") else
                                   {int(p.split("=", 1)[0]): p.split("=", 1)[1] for p in answer.split()})
                    if set(assignments) != positive:
                        raise ValueError("gi håndhevelse for hvert treff")
                    for i, val in assignments.items():
                        if val.startswith("u:") and val[2:].strip():
                            rows[i]["unenforced"] = {"reason": val[2:]}
                        elif val in record["tests"]:
                            rows[i]["preventedBy"] = val
                        else:
                            raise ValueError("ukjent derivedTest eller tom grunn")
                    break
                except (ValueError, IndexError):
                    for row in rows.values():
                        row.pop("preventedBy", None)
                        row.pop("unenforced", None)
                    print("Ugyldig håndhevelse; bruk kjent testref eller u:grunn.")
    except (EOFError, KeyboardInterrupt):
        print("\nAvbrutt; tidligere lagrede runder er bevart.")
        return 1
    record["judgments"].extend(rows.values())
    elapsed = time.monotonic() - start
    record["annotationSeconds"] += round(elapsed, 3)
    record["updatedAt"] = dt.datetime.now(dt.timezone.utc).isoformat()
    save_record(path, record)
    remaining = len(record["presented"]) - len(record["judgments"])
    print(f"Lagret {len(rows)} dommer på {elapsed:.1f} s. {remaining} uvurderte. {path}")
    return 0
