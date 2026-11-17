# -*- coding: utf-8 -*-
"""Lager innfilene til en ny runde med ordlistetråder av en datafil og innfilene fra forrige runde
(forklaringene og delingen av emner i A og B beholdes; «har» er det datafilen har nå).
Bruk: lag_leksinn.py <datafil> <forrige inn-mappe> <ny inn-mappe>"""
import json, sys, os
data = json.load(open(sys.argv[1], encoding="utf-8")); forrige, ny = sys.argv[2], sys.argv[3]
g, sp = data["graf"], data["spraak"]
os.makedirs(ny, exist_ok=True)
for navn in ("emner-A.json", "emner-B.json"):
    inn = json.load(open(os.path.join(forrige, navn), encoding="utf-8"))
    for e in inn["emner"]:
        e["har"] = list(g["ordformer"].get(e["emne"], []))
    for a in inn.get("allergener", []):
        kode = a["kode"]
        har = list(g["allergenord"].get(kode, []))
        for slag, ord_ in g["allergenutsagn"].get(kode, {}).items(): har += ord_
        a["har"] = har
    json.dump(inn, open(os.path.join(ny, navn), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(navn, "emner:", len(inn["emner"]), "allergener:", len(inn.get("allergener", [])))
st = json.load(open(os.path.join(forrige, "stikk.json"), encoding="utf-8"))
kjente = {x["klasse"] for x in st["stikk"]}
for x in st["stikk"]: x["har"] = list(sp["stikk"][x["klasse"]])
if "HOEFLIG" not in kjente:
    st["stikk"].append({"klasse": "HOEFLIG", "forklaring": "Ord som gjør det gjesten nettopp nevnte, til en bestilling, uten verb («en pizza, takk», «a beer please»). Også uttrykk som sier hvem det er til eller når det skal komme, når de bare brukes i bestillinger («til meg», «først», «etterpå»).", "har": list(sp["stikk"]["HOEFLIG"])})
st["nektelser"]["har"] = list(sp["nektelser"])
for x in st["ordlister"]: x["har"] = list(sp["ordlister"][x["liste"]])
json.dump(st, open(os.path.join(ny, "stikk.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("stikk.json klasser:", [(x["klasse"], len(x["har"])) for x in st["stikk"]], "| nektelser:", len(st["nektelser"]["har"]), "| ordlister:", [(x["liste"], len(x["har"])) for x in st["ordlister"]])
