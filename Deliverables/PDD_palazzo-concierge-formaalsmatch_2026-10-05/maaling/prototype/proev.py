# -*- coding: utf-8 -*-
"""Tilfellene fra spesifikasjonen (§5) og planen (arbeidspakke 3), kjørt i prototypen."""
import json, sys
import husgraf, dekomp
data = json.load(open(sys.argv[1], encoding="utf-8"))
g = husgraf.Graf(data, json.load(open(husgraf.KORPUS, encoding="utf-8"))); sp = dekomp.Spraak(data)
def t(tekst):
    d = dekomp.dekomponer(tekst, g, sp)
    return d["formaal"], sorted(("-" if x["slag"] in dekomp.NEGATIVE else "+") + x["node"] for x in d["noder"]), d
feil = 0
def krev(tekst, formaal, noder, merk=""):
    global feil
    f, n, d = t(tekst)
    ok = (formaal == "*" or f == formaal) and (noder is None or n == sorted(noder))
    if not ok: feil += 1
    print("%s %-55s -> %-8s %s %s" % ("ok  " if ok else "FEIL", tekst[:55], f, " ".join(n), ("   (ventet %s %s)" % (formaal, noder)) if not ok else ""))
# test.dekomp.ordformer
krev("ost", "vite", ["+emne:ost"]); krev("oster", "vite", ["+emne:ost"]); krev("osten", "vite", ["+emne:ost"])
krev("pizza", "vite", ["+emne:pizza"]); krev("pizzaer", "vite", ["+emne:pizza"])
krev("Pizza Tartufo", "vite", ["+menu-pizza-tartufo-umami"])
krev("hvitvin", "*", ["+emne:hvitvin", "+emne:vin"]); krev("rødvinsbraiserte", "*", ["+emne:rødvin", "+emne:vin"])
krev("pistasi", "*", ["+emne:pistasj"]); krev("pistasj", "*", ["+emne:pistasj"])
# test.dekomp.nektelse
krev("jeg liker ikke ost", None, ["-emne:ost"]); krev("uten kjøtt", "unngaa", ["-emne:kjøtt"])
krev("jeg liker ikke ost, men jeg liker pistasj", None, ["-emne:ost", "+emne:pistasj"])
# test.dekomp.formaal
krev("Jeg vil ha noe med ost", "spise", ["+emne:ost"]); krev("Har dere eplemost?", "drikke", ["+bev-eplemost"])
krev("Hva er Arancini?", "vite", ["+menu-arancini"]); krev("Jeg tåler ikke nøtter", "unngaa", ["-allergen:N"])
krev("Kan jeg bestille bord?", "bord", []); krev("Når åpner dere?", "aapningstid", [])
krev("Jeg liker ost", None, ["+emne:ost"])
# planen, arbeidspakke 3
krev("Jeg liker østers", None, ["+emne:østers"])
krev("Har dere dessert uten nøtter?", "unngaa", ["+emne:dessert", "-allergen:N"])
krev("Jeg er ikke så glad i fisk", None, ["-emne:fisk"])
# flere veier med «ikke»
krev("Jeg spiser ikke kjøtt", "unngaa", ["-emne:kjøtt"]); krev("Jeg er allergisk mot egg", "unngaa", ["-allergen:E"])
krev("Jeg har nøtteallergi", "unngaa", ["-allergen:N"]); krev("Hvitløk spiser jeg aldri", "unngaa", ["-emne:hvitløk"])
krev("Ost er ikke noe for meg", None, ["-emne:ost"]); krev("ingen nøtter, takk", "unngaa", ["-allergen:N"])
krev("Jeg vil ikke ha fisk", "unngaa", ["-emne:fisk"]); krev("Jeg tåler ikke fisk", "unngaa", ["-allergen:F"])
krev("Jeg tåler ikke løk", "unngaa", ["-emne:løk"]); krev("Jeg tåler ikke koffein", "unngaa", ["-ukjent"])
krev("Tingen er at jeg liker pizza", None, ["+emne:pizza"]); krev("Hva er allergenene i Ostriche?", "vite", ["+menu-ostriche"])
krev("Jeg liker ikke ost. Har dere pizza?", "vite", ["-emne:ost", "+emne:pizza"])
krev("Takk for maten!", None, []); krev("Hei", None, [])
krev("Er det nøtter i Agnello arrosto?", "vite", ["+allergen:N", "+menu-agnello-bronte"])
krev("lokale råvarer", None, []); krev("Hva er risikoen?", None, []); krev("Har dere desserter?", "vite", ["+emne:dessert"])
krev("Jeg vil ha ølet", "drikke", ["+emne:øl"]); krev("en lampe", None, [])
print("feil:", feil)
