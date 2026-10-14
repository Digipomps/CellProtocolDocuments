# Regner Butlers treffregel (CellScaffold/_wt-butler-e1-20260929/Sources/App/Support/ButlerSignalMatcher.swift,
# linje 32–57 og 78–90) i Python på emnenavnene i graf/emner-v1.json. Regnet, ikke kjørt i Swift.
# Bruk: python3 kollisjoner_regnet.py <graf/emner-v1.json> [ord ...]
import json, re, sys
def norm(t):
    t = t.lower()
    for a, b in (("ø", "o"), ("æ", "ae"), ("å", "a"), ("ö", "o"), ("ä", "a"), ("ü", "u"), ("é", "e"), ("è", "e"), ("ë", "e")): t = t.replace(a, b)
    return re.sub(r"[^a-z0-9]+", " ", t).strip()
def treffer(term, token, sammensetning=True):
    if token == term: return True
    hale = 7 if len(term) >= 5 else 3
    if len(term) >= 3 and token.startswith(term) and len(token) <= len(term) + hale: return True
    if sammensetning and len(term) >= 5 and term in token: return True
    return False
d = json.load(open(sys.argv[1], encoding="utf-8"))
emner = sorted({e["emne"] for v in list(d["retter"].values()) + list(d["drikke"].values()) for e in v})
ordene = sys.argv[2:] or ["østers", "lokale", "lokalt", "risiko", "lampe", "desserter", "øl", "ølet", "pistasj", "pistasi", "Har dere noe sånt som risboller?"]
print(len(emner), "emner")
for o in ordene:
    treff = sorted({e for t in norm(o).split() for e in emner if " " not in e and treffer(norm(e), t)})
    print("%-34s treffer: %s" % (o, ", ".join(treff) or "ingen"))
