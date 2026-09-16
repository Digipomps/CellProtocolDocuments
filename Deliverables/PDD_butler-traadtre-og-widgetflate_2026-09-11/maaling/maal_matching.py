import json, re, subprocess, itertools, os, pathlib
ROOT = pathlib.Path(".")
LESS = json.load(open("Book/haven_lessons_register_v0.json"))["lessons"]
by_ref = {l["lessonRef"]: l for l in LESS}

tasks = []
for d in sorted(ROOT.glob("Deliverables/PDD_*")):
    st = d / "STATUS.md"
    if not st.exists(): continue
    txt = st.read_text(errors="replace")
    def field(name):
        m = re.search(rf"^- {name}:\s*(.+)$", txt, re.M)
        return [x.strip() for x in m.group(1).split(",")] if m else []
    m = re.search(r"_(\d{4}-\d{2}-\d{2})$", d.name)
    tasks.append({"dir": d.name, "date": m.group(1) if m else "9999-99-99",
                  "tags": field("tags"), "surfaces": field("surfaces")})

def lookup(t):
    cmd = ["python3","Tools/PurposePackages/purpose_dev.py","lookup"]
    if t["tags"]: cmd += ["--tags"] + t["tags"]
    if t["surfaces"]: cmd += ["--surfaces"] + t["surfaces"]
    out = subprocess.run(cmd, capture_output=True, text=True).stdout
    return set(re.findall(r"(lesson\.[a-z0-9\-]+)", out))

print(f"{len(tasks)} PDD-oppgaver, {len(LESS)} lærdommer\n")
res = []
for t in tasks:
    got = lookup(t)
    # bare lærdommer som EKSISTERTE da oppgaven ble opprettet
    before = {r for r in got if by_ref.get(r,{}).get("date","0") < t["date"]}
    origin = {l["lessonRef"] for l in LESS if t["dir"] in str(l.get("source",""))}
    res.append({**t, "returnert": got, "returnert_foer": before, "oppsto_her": origin})
    print(f'{t["date"]} {t["dir"][:46]:46} tags={len(t["tags"])} -> returnert {len(got):2} (eksisterte da: {len(before):2})  nye lærdommer herfra: {len(origin)}')

print("\n--- 1. STOEY: hvor mange lærdommer maa leses per oppgave")
n = [len(r["returnert"]) for r in res]
print(f"   snitt {sum(n)/len(n):.1f}, min {min(n)}, maks {max(n)}, av {len(LESS)} totalt")

print("\n--- 2. DISKRIMINERING: skiller matcheren oppgaver fra hverandre?")
pairs = list(itertools.combinations(res, 2))
def jac(a,b):
    u = a|b
    return len(a&b)/len(u) if u else 1.0
js = [jac(a["returnert"], b["returnert"]) for a,b in pairs]
print(f"   Jaccard mellom oppgavepar: snitt {sum(js)/len(js):.2f}, min {min(js):.2f}, maks {max(js):.2f}")
print(f"   (1.00 = alle oppgaver faar samme sett, altsaa null informasjon i matchingen)")
alle = set.intersection(*[r["returnert"] for r in res]) if res else set()
print(f"   returnert til ALLE {len(res)} oppgaver: {len(alle)} lærdommer")

print("\n--- 3. DOEDVEKT: lærdommer ingen oppgave fikk se")
sett = set().union(*[r["returnert"] for r in res]) if res else set()
doed = sorted(set(by_ref) - sett)
print(f"   {len(doed)} av {len(LESS)} ble aldri returnert til noen av de {len(res)} oppgavene")
for r in doed[:8]: print("     -", r)

print("\n--- 4. GJENTAKELSE: ble en lærdom gjentatt selv om matcheren viste den?")
# to lærdommer 'gjentar' hverandre hvis de deler >=2 tags og en purposeRef
def like(a,b):
    return len(set(a["tags"]) & set(b["tags"])) >= 2 and set(a.get("purposeRefs",[])) & set(b.get("purposeRefs",[]))
gjentak = []
for a, b in itertools.combinations(sorted(LESS, key=lambda x: x["date"]), 2):
    if a["date"] < b["date"] and like(a,b): gjentak.append((a,b))
print(f"   {len(gjentak)} par der en senere lærdom gjentar moensteret fra en tidligere")
vist, ikke_vist = 0, 0
for tidlig, sen in gjentak:
    t = next((r for r in res if r["dir"] in str(sen.get("source",""))), None)
    if not t: continue
    if tidlig["lessonRef"] in t["returnert_foer"]: vist += 1
    else: ikke_vist += 1
print(f"   av de som kan spores til en PDD-oppgave: {vist} ble VIST paa forhaand og gjentok seg likevel,")
print(f"                                            {ikke_vist} ble IKKE vist")
