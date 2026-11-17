# -*- coding: utf-8 -*-
"""Samtalen (arbeidspakke 5 og 6) skrevet utenfor Swift: hva det nye kallet svarer på en setning eller et valg,
gitt det som er notert. Følger contract/SAMTALE-UTSETTING-1.md steg for steg, og svarer til
PalazzoScaffold/Sources/App/Services/PalazzoSamtale.swift linje for linje.

Svar «som i dag» regnes ikke her: utfallet er da veien «som-i-dag» med grunnen. Henvisningen til personalet er
veien «henvist». Brukes til å lage referansen Swift-testene holdes mot (lag_samtalereferanse.py).

To ting leses utenfra og gis inn som funksjoner, så regningen her er den samme uansett hvor den kjøres:
  treffer_listen(tekst)   strakstiltakets ordliste (PalazzoAllergiHenvisning.treffer)
  roerer_vin(tekst)       ordene for allergener, vin og alkohol (PalazzoConciergePhrasing.touchesNeverRephrased)
"""
import unicodedata
import dekomp, husmatch_sim

LINJE_EN = "Beskrivelsen er ikke en ingrediensliste. Spør personalet om allergener før du bestiller."
LINJE_FLERE = "Beskrivelsene er ikke ingredienslister. Spør personalet om allergener før du bestiller."
LINJE_KORT = "Spør personalet om allergener før du bestiller."
LINJE_DATERT = "Svaret bygger på et datert kunnskapsgrunnlag. Dagens meny, priser og tilgjengelighet må bekreftes av Palazzo."
LINJE_KASTET = "Menyen er oppdatert siden du begynte. Det som var notert, er fjernet."

# Plass på menyen (korpusets kategori): spørsmålet i tilbudet, «når» i kvitteringen, og plassen i en liste.
PLASS = {
    "antipasti": ("Vil du ha det til forrett?", "til forrett", "forrett"),
    "primi": ("Vil du ha det som pastarett?", "som pastarett", "pastarett"),
    "secondi": ("Vil du ha det til hovedrett?", "til hovedrett", "hovedrett"),
    "dolce": ("Vil du ha det til dessert?", "til dessert", "dessert"),
    "pizze": ("Vil du ha den?", "", "pizza"),
    "non_alcoholic": ("Vil du ha det å drikke?", "å drikke", "drikke"),
}
NOTATSLAG = ["liker", "liker-ikke", "taaler-ikke", "spiser-ikke", "vil-ha"]
UNNGAAR = ("taaler-ikke", "spiser-ikke")
NEGATIVE = ("taaler-ikke", "spiser-ikke", "liker-ikke", "utelukker")
UKJENT = "ukjent"
UKJENT_MERKELAPP = "unngår noe conciergen ikke kjenner igjen"
MAKS_NOTERT = 24
TALLORD = {2: "to", 3: "tre", 4: "fire", 5: "fem", 6: "seks", 7: "sju", 8: "åtte", 9: "ni", 10: "ti", 11: "elleve", 12: "tolv"}
OVERSKRIFT = "Dette har vi som passer til det du skrev:"
VERB = {"liker": "liker", "liker-ikke": "liker ikke", "taaler-ikke": "tåler ikke", "spiser-ikke": "spiser ikke",
        "vil-ha": "vil ha", "spoer-om": "spør om", "nevner": "nevner", "utelukker": "vil ha noe annet enn"}
UTEN_INTERESSER = {"vite": "du spør om noe huset har.", "bord": "du spør om bord.", "aapningstid": "du spør om åpningstidene.",
                   "spise": "du vil ha noe å spise.", "drikke": "du vil ha noe å drikke.", "unngaa": "du vil unngå noe."}


# ── Poster og noder ────────────────────────────────────────────────────────────────────────────────

def post(g, pid):
    return g.retter.get(pid) or g.drikke.get(pid)

def alkohol(g, pid):
    p = post(g, pid)
    return p is not None and p.get("category", "").startswith("alcoholic")

def alkoholemne(g, emne):
    """Emnet er et alkoholemne, eller en alkoholfri utgave av ett («alkoholfritt øl», «alkoholfri vin»)."""
    alk = g.data["graf"]["svar"]["alkoholemner"]
    return emne in alk or any(o in alk for o in emne.split(" "))

def alkoholnaer(g, pid):
    """En drikk med alkohol, eller en alkoholfri utgave av en: et emne den nås fra er et alkoholemne eller en alkoholfri
    utgave av ett («alkoholfritt øl»), eller navnet har et ord for alkohol («Alkoholfri Gin Tonic»), med samme ordliste
    som holder setninger unna modellen. Den går samme vei som drikke med alkohol: oppslaget svarer, og den står aldri i
    et tilbud eller en liste fra matchen. En rett med vin i beskrivelsen er ikke en drikk og regnes ikke hit."""
    if pid not in g.drikke: return False
    if alkohol(g, pid): return True
    if roerer_vin(g.drikke[pid]["name"]): return True
    return any(alkoholemne(g, e) for e, kanter in g.kanter.items() if any(p == pid for p, _ in kanter))

def kan_nevnes(g, pid):
    """Posten kan stå i et svar vakten bygger: den har en plass på menyen, er bekreftet og har kilde og dato."""
    p = post(g, pid)
    if p is None or p.get("category") not in PLASS: return False
    if alkoholnaer(g, pid): return False
    if p.get("human_verified") is not True or p.get("needs_human_review") is True: return False
    if pid in g.drikke and p.get("availability_verified") is not True: return False
    return bool(p.get("source_ids")) and bool(p.get("last_verified"))

def nodenavn(g, node):
    if node == UKJENT: return "noe conciergen ikke kjenner igjen"
    if node.startswith("emne:"): return node[5:]
    if node.startswith("allergen:"): return g.allergener[node[9:]]["name_nb"].lower()
    return post(g, node)["name"]

def nodetype(g, node):
    if node == UKJENT: return "ukjent"
    if node.startswith("emne:"): return "emne" if node[5:] in g.kanter else None
    if node.startswith("allergen:"): return "allergen" if node[9:] in g.allergener else None
    if node in g.retter: return "rett"
    if node in g.drikke: return "drikk"
    return None

def gyldig_notat(g, slag, node):
    """Kontraktens regel for en post i noted. En drikk med alkohol, eller en alkoholfri utgave av øl eller vin, kan ikke stå notert,
    og heller ikke et alkoholemne («øl», «vin»): det uavhengige angrepet 7. oktober 2026 fikk «vil ha øl» tilbake med vil-ha på emne:øl."""
    t = nodetype(g, node)
    if t == "emne" and alkoholemne(g, node[5:]): return False
    if slag == "taaler-ikke": return t in ("allergen", "emne", "ukjent")
    if slag in ("liker", "liker-ikke", "spiser-ikke", "vil-ha"):
        if t == "drikk" and alkoholnaer(g, node): return False
        return t in ("emne", "rett", "drikk")
    return False

def merkelapp(g, slag, node):
    if node == UKJENT: return UKJENT_MERKELAPP
    if slag == "vil-ha" and nodetype(g, node) in ("rett", "drikk"):
        naar = PLASS.get(post(g, node).get("category"), ("", "", ""))[1]
        return ("vil ha " + nodenavn(g, node) + " " + naar).strip()
    return VERB[slag] + " " + nodenavn(g, node)

def ramse(navn):
    navn = list(navn)
    if len(navn) <= 1: return "".join(navn)
    return ", ".join(navn[:-1]) + " og " + navn[-1]


# ── Det som er notert ──────────────────────────────────────────────────────────────────────────────

def noter(notert, slag, node):
    """Legger én post til listen. Det strengeste står, og om det hun liker, gjelder det siste hun sa."""
    notert = list(notert)
    if (slag, node) in notert: return notert
    if slag in ("liker", "liker-ikke"):
        if any(n == node and s in UNNGAAR for s, n in notert): return notert
        notert = [(s, n) for s, n in notert if not (n == node and s in ("liker", "liker-ikke"))]
    elif slag == "spiser-ikke":
        if ("taaler-ikke", node) in notert: return notert
        notert = [(s, n) for s, n in notert if not (n == node and s in ("liker", "liker-ikke"))]
    elif slag == "taaler-ikke":
        notert = [(s, n) for s, n in notert if not (n == node and s in ("liker", "liker-ikke", "spiser-ikke"))]
    if len(notert) >= MAKS_NOTERT:
        # Listen er full. Det eldste som ikke er noe hun unngår, går ut. Er alt noe hun unngår, står listen.
        for i, (s, n) in enumerate(notert):
            if s not in UNNGAAR:
                del notert[i]
                break
        else:
            return notert
    return notert + [(slag, node)]

def unngaar_notat(g, x):
    """Posten et «tåler ikke» eller «spiser ikke» i setningen gir. Et allergen er alltid «tåler ikke». «Spiser ikke» om en
    drikk med alkohol, eller en alkoholfri utgave av en, gir ingen post (None): en slik drikk kan ikke stå notert
    (gyldig_notat), og vakten nevner den aldri. Uten dette noterte steg 2 «spiser ikke Peroni» ved siden av en henvisning,
    og siden fikk 422 på hvert kall etterpå (lest 7. oktober 2026)."""
    node, t = x["node"], nodetype(g, x["node"])
    if t == "allergen": return ("taaler-ikke", node)
    if t == "ukjent" or t is None: return ("taaler-ikke", UKJENT)
    # Et alkoholemne går som en drikk med alkohol: «tåler ikke øl» blir ukjent, «drikker ikke øl» noteres ikke.
    if t == "emne" and alkoholemne(g, node[5:]):
        return ("taaler-ikke", UKJENT) if x["slag"] == "taaler-ikke" else None
    if x["slag"] == "taaler-ikke":
        return ("taaler-ikke", node) if t == "emne" else ("taaler-ikke", UKJENT)
    if t == "drikk" and alkoholnaer(g, node): return None
    return ("spiser-ikke", node)


# ── Det conciergen forsto ──────────────────────────────────────────────────────────────────────────

def forstaatt(g, d):
    interesser = []
    for x in d["noder"]:
        interesser.append({"node": x["node"], "label": nodenavn(g, x["node"]), "sign": -1 if x["slag"] in NEGATIVE else 1,
                           "matched": [x["ord"]] if x.get("ord") else []})
    deler, forrige = [], None
    for x in d["noder"]:
        slag = (unngaar_notat(g, x) or (x["slag"],))[0] if x["slag"] in UNNGAAR else x["slag"]
        if slag == forrige:
            deler[-1][1].append(nodenavn(g, x["node"]))
        else:
            deler.append((slag, [nodenavn(g, x["node"])]))
            forrige = slag
    if deler:
        tekst = "du " + ramse(VERB[s] + " " + ramse(n) for s, n in deler) + "."
    else:
        tekst = UTEN_INTERESSER.get(d["formaal"], "")
    return {"purpose": d["formaal"], "interests": interesser, "text": tekst}


# ── Tekstene ───────────────────────────────────────────────────────────────────────────────────────

def linje_for(g, poster):
    med = sum(1 for pid in poster if post(g, pid).get("description_nb"))
    return LINJE_KORT if med == 0 else (LINJE_EN if med == 1 else LINJE_FLERE)

def tilbudstekst(g, pid):
    p = post(g, pid)
    spoersmaal = PLASS[p["category"]][0]
    if p.get("description_nb"):
        return "Vi har %s: %s %s" % (p["name"], p["description_nb"], spoersmaal)
    return "Vi har %s. %s" % (p["name"], spoersmaal)

def listelinje(g, pid):
    p = post(g, pid)
    plass = PLASS[p["category"]][2]
    if p.get("description_nb"):
        return "%s (%s): %s" % (p["name"], plass, p["description_nb"])
    return "%s (%s)." % (p["name"], plass)

def fortelltekst(g, poster, emne=None):
    svar = g.data["graf"]["svar"]
    hva = svar["fortell"].get(emne) if emne else None
    antall = TALLORD.get(len(poster), str(len(poster)))
    overskrift = ("Vi har %s %s:" % (antall, hva)) if hva else OVERSKRIFT
    return overskrift + "\n\n" + "\n\n".join(listelinje(g, pid) for pid in poster)

def en_post_tekst(g, pid):
    p = post(g, pid)
    if p.get("description_nb"): return "%s: %s" % (p["name"], p["description_nb"])
    return tilbudstekst(g, pid)

def ja_tekst(g, poster):
    def ett(pid):
        naar = PLASS[post(g, pid)["category"]][1]
        return (post(g, pid)["name"] + " " + naar).strip()
    return "Notert: du vil ha %s. Jeg kan ikke bestille for deg, og kelneren ser ikke dette. Si det til kelneren når du bestiller." % ramse(ett(p) for p in poster)

def liker_ikke_tekst(navn):
    return "Notert: du liker ikke %s. Jeg foreslår helst andre retter. Spør du om %s, får du svar likevel." % (ramse(navn), ramse(navn))

def spiser_ikke_tekst(navn):
    return "Notert: du spiser ikke %s. Jeg foreslår derfor ingen retter selv. Spør personalet om hva som passer." % ramse(navn)

def notert_tekst(merkelapper):
    return "Notert: du %s." % ramse(merkelapper)

NEI_TEKST = "Greit. Da noterer jeg ingenting."
IKKE_NOTERT = "Det står ingenting notert om dette."
ALT_FJERNET = "Alt er fjernet. Jeg husker ingenting av det du har sagt om deg selv."

def fjernet_tekst(merkelapper):
    return "Fjernet: %s. Jeg regner ikke lenger med det." % ramse("«%s»" % m for m in merkelapper)


# ── Matchen ────────────────────────────────────────────────────────────────────────────────────────

def match(g, interesser, negskala=1.0):
    """interesser: [(emne, ord, negativ)]. Samme regning som PalazzoHusmatcher.match, med samme rekkefølge."""
    poster = {}
    for del_ in ("retter", "drikke"):
        for pid, kanter in g.data["graf"][del_].items():
            poster[pid] = [(k["emne"], k["vekt"]) for k in kanter]
    emner = [(e, n) for e, _, n in interesser if e in g.kanter]
    if not emner:
        return {"treff": [], "fullstendig": True, "bom": "missingPreconfiguredCoverage"}
    raa = husmatch_sim.match(poster, g.terskel, emner, negskala=negskala)
    ordene = {}
    for e, o, n in interesser: ordene.setdefault((e, n), o)
    treff = []
    for pid, s, bidrag in raa:
        kant = dict(poster[pid])
        treff.append({"post": pid, "sum": s,
                      "fordi": [{"node": "emne:" + e, "ord": ordene.get((e, n), ""), "emne": e, "kantvekt": kant.get(e, 0), "bidrag": b, "negativ": n}
                                for e, b, n in bidrag]})
    treff.sort(key=lambda t: (-round(t["sum"] * 1e9), any(f["negativ"] for f in t["fordi"]), t["post"]))
    return {"treff": treff, "fullstendig": True, "bom": None if treff else "lowConfidence"}


# ── Svaret på en setning ───────────────────────────────────────────────────────────────────────────

def _utfall(vei, **felt):
    ut = {"vei": vei, "kind": None, "tekst": None, "linjer": [], "poster": [], "tilbud": None, "grunn": None, "bom": None, "treff": []}
    ut.update(felt)
    return ut

def paa_setning(tekst, notert, g, sp, treffer_listen, roerer_vin, negskala=1.0):
    """Returnerer (utfall, notert etterpå, forstått). `notert` er en liste av (slag, node)."""
    notert = list(notert)
    d = dekomp.dekomponer(tekst, g, sp)
    I = d["noder"]
    f = forstaatt(g, d)
    svar = g.data["graf"]["svar"]

    # Steg 2: strakstiltaket, og det dekomponeringen leser som noe gjesten ikke tåler.
    unngaar = [x for x in I if x["slag"] in UNNGAAR]
    strengt = [x for x in unngaar if (unngaar_notat(g, x) or ("",))[0] == "taaler-ikke"]
    uten_node = d["formaal"] == "unngaa" and not unngaar
    liste = treffer_listen(tekst)
    # `allergi`: setningen sier at noen ikke tåler noe, har et ord for allergi, eller nevner et allergen.
    # Grafen kjenner flere ord for allergener enn listen gjør. De får samme svar som listens ord. Det gjelder også
    # et emne med samme ord som et allergen («fisk», «selleri»): «fesk» og «seleri» får samme svar som «fisk» og «selleri».
    tvilling = any(x.get("allergen") for x in I)
    if liste or d["allergi"] or tvilling or strengt or uten_node:
        for x in unngaar:
            n = unngaar_notat(g, x)
            if n: notert = noter(notert, *n)
        if uten_node:
            notert = noter(notert, "taaler-ikke", UKJENT)
        return _utfall("henvist", kind="refused", grunn="ordliste" if liste else "dekomponering"), notert, f

    # Steg 4: vin og alkohol går til oppslaget, og ingenting noteres.
    def alkoholnode(x):
        t = nodetype(g, x["node"])
        if t == "drikk": return alkoholnaer(g, x["node"])
        if t == "emne": return alkoholemne(g, x["node"][5:])
        return False
    if roerer_vin(tekst) or any(alkoholnode(x) for x in I):
        return _utfall("som-i-dag", grunn="alkohol"), notert, f

    # Steg 5: det setningen sier om gjesten selv, noteres.
    for x in I:
        t = nodetype(g, x["node"])
        if x["slag"] in ("liker", "liker-ikke") and t in ("emne", "rett", "drikk"):
            notert = noter(notert, x["slag"], x["node"])
        elif x["slag"] == "spiser-ikke":
            n = unngaar_notat(g, x)
            if n: notert = noter(notert, *n)

    # Steg 6: står det noe hun ikke tåler eller ikke spiser, kommer verken tilbud eller liste fra matchen.
    if any(s in UNNGAAR for s, n in notert):
        if I and all(x["slag"] == "spiser-ikke" for x in I):
            return _utfall("kvittering", kind="receipt", tekst=spiser_ikke_tekst([nodenavn(g, x["node"]) for x in I]),
                           linjer=[LINJE_KORT], grunn="noted"), notert, f
        if I and all(x["slag"] in ("spiser-ikke", "liker-ikke") for x in I):
            # Kvitteringen sier det som står notert om det hun nevnte. Det strengeste står, så «liker ikke kjøtt»
            # etter «spiser ikke kjøtt» gir «spiser ikke kjøtt».
            nevnt = [x["node"] for x in I]
            staar = [(s, n) for s, n in notert if n in nevnt and s in ("taaler-ikke", "spiser-ikke", "liker-ikke")]
            if staar:
                return _utfall("kvittering", kind="receipt", tekst=notert_tekst([merkelapp(g, s, n) for s, n in staar]),
                               linjer=[LINJE_KORT], grunn="noted"), notert, f
        return _utfall("som-i-dag", grunn="notert-unngaar"), notert, f

    # Bord og åpningstid svarer oppslaget på, også når setningen nevner noe huset har.
    if d["formaal"] in ("bord", "aapningstid"):
        return _utfall("som-i-dag", grunn="formaal"), notert, f

    # Steg 7: setningen sier bare noe gjesten ikke liker.
    if I and all(x["slag"] == "liker-ikke" for x in I):
        return _utfall("kvittering", kind="receipt", tekst=liker_ikke_tekst([nodenavn(g, x["node"]) for x in I]),
                       linjer=[LINJE_KORT], grunn="noted"), notert, f

    # Steg 8: en rett eller en drikk uten alkohol ved navn.
    navngitte = [x for x in I if nodetype(g, x["node"]) in ("rett", "drikk") and x["slag"] not in NEGATIVE and kan_nevnes(g, x["node"])]
    if navngitte:
        vil = [x["node"] for x in navngitte if x["slag"] == "vil-ha"]
        if vil:
            for pid in vil: notert = noter(notert, "vil-ha", pid)
            return _utfall("kvittering", kind="receipt", tekst=ja_tekst(g, vil), linjer=[LINJE_KORT, LINJE_DATERT],
                           poster=vil, grunn="noted"), notert, f
        poster = [x["node"] for x in navngitte]
        if len(poster) == 1:
            pid = poster[0]
            liker = navngitte[0]["slag"] == "liker"
            if liker or not post(g, pid).get("description_nb"):
                return _tilbud(g, pid), notert, f
            return _utfall("match", kind="tell", tekst=en_post_tekst(g, pid), linjer=[linje_for(g, poster), LINJE_DATERT],
                           poster=poster, grunn="tell"), notert, f
        return _utfall("match", kind="tell", tekst=fortelltekst(g, poster), linjer=[linje_for(g, poster), LINJE_DATERT],
                       poster=poster, grunn="tell"), notert, f

    # Steg 9: emnene i setningen, og det som er notert.
    positive = [x for x in I if nodetype(g, x["node"]) == "emne" and x["slag"] in ("liker", "vil-ha", "spoer-om", "nevner")]
    if positive:
        interesser, sett = [], set()
        for x in positive:
            e = x["node"][5:]
            if e not in sett:
                sett.add(e); interesser.append((e, x.get("ord", ""), False))
        for x in I:
            e = x["node"][5:] if nodetype(g, x["node"]) == "emne" else None
            if e and x["slag"] in ("liker-ikke", "utelukker") and e not in sett:
                sett.add(e); interesser.append((e, x.get("ord", ""), True))
        for s, n in notert:
            e = n[5:] if nodetype(g, n) == "emne" else None
            if e and e not in sett and s in ("liker", "liker-ikke"):
                sett.add(e); interesser.append((e, "", s == "liker-ikke"))
        m = match(g, interesser, negskala=negskala)
        spurt = set(x["node"][5:] for x in positive)
        treff = [t for t in m["treff"] if not alkohol(g, t["post"]) and kan_nevnes(g, t["post"])
                 and any(r["emne"] in spurt and not r["negativ"] for r in t["fordi"])]
        if not m["fullstendig"]:
            return _utfall("som-i-dag", grunn="bom", bom="incomplete"), notert, f
        if not treff:
            return _utfall("som-i-dag", grunn="bom", bom=m["bom"] or "lowConfidence"), notert, f
        if len(treff) == 1 or treff[0]["sum"] >= svar["klar_leder"] * treff[1]["sum"]:
            u = _tilbud(g, treff[0]["post"])
            u["treff"] = treff
            return u, notert, f
        poster = [t["post"] for t in treff]
        emne = sorted(spurt)[0] if len(spurt) == 1 else None
        if emne and not all(any(r["emne"] == emne and not r["negativ"] for r in t["fordi"]) for t in treff):
            emne = None
        return _utfall("match", kind="tell", tekst=fortelltekst(g, poster, emne), linjer=[linje_for(g, poster), LINJE_DATERT],
                       poster=poster, grunn="tell", treff=treff), notert, f

    # Steg 10: bom, eller ingenting huset har.
    return _utfall("som-i-dag", grunn="bom", bom="lowConfidence" if I else "missingPreconfiguredCoverage"), notert, f

def _tilbud(g, pid):
    p = post(g, pid)
    return _utfall("match", kind="offer", tekst=tilbudstekst(g, pid), linjer=[linje_for(g, [pid]), LINJE_DATERT], poster=[pid], grunn="offer",
                   tilbud={"ref": pid, "name": p["name"], "when": PLASS[p["category"]][1], "choices": ["ja", "nei"]})


# ── Svaret på et valg ──────────────────────────────────────────────────────────────────────────────

def paa_valg(valg, notert, g):
    """valg: ("tilbud", ja, ref) | ("fjern", node) | ("fjern-alt",). Returnerer (utfall, notert) eller kaster ValueError (422)."""
    notert = list(notert)
    if valg[0] == "tilbud":
        _, ja, ref = valg
        if nodetype(g, ref) not in ("rett", "drikk") or alkohol(g, ref) or not kan_nevnes(g, ref):
            raise ValueError("ukjent tilbud")
        if not ja:
            return _utfall("kvittering", kind="receipt", tekst=NEI_TEKST, linjer=[LINJE_KORT], grunn="answered"), notert
        if any(s in UNNGAAR for s, n in notert):
            return _utfall("henvist", kind="refused", grunn="notert-unngaar"), notert
        notert = noter(notert, "vil-ha", ref)
        return _utfall("kvittering", kind="receipt", tekst=ja_tekst(g, [ref]), linjer=[LINJE_KORT, LINJE_DATERT], poster=[ref], grunn="noted"), notert
    if valg[0] == "fjern":
        node = valg[1]
        if nodetype(g, node) is None: raise ValueError("ukjent node")
        borte = [(s, n) for s, n in notert if n == node]
        if not borte:
            # Det står ingenting notert om noden (fjernet fra før, eller menyen er oppdatert). Svaret sier det,
            # og siden får listen slik den er.
            return _utfall("kvittering", kind="receipt", tekst=IKKE_NOTERT, linjer=[LINJE_KORT], grunn="answered"), notert
        notert = [(s, n) for s, n in notert if n != node]
        return _utfall("kvittering", kind="receipt", tekst=fjernet_tekst([merkelapp(g, s, n) for s, n in borte]), linjer=[LINJE_KORT], grunn="removed"), notert
    if valg[0] == "fjern-alt":
        return _utfall("kvittering", kind="receipt", tekst=ALT_FJERNET, linjer=[LINJE_KORT], grunn="removed"), []
    raise ValueError("ukjent valg")


# ── Ordene for allergener, vin og alkohol (PalazzoConciergePhrasing.touchesNeverRephrased) ─────────

ALDRI_BITER = ["allergen", "allergi", "gluten", "melk", "nott", "nøtt", "notter", "nøtter", "krysskontakt", "crosscontact", "trygg", "wine", "alkohol", "alcohol"]
ALDRI_ORD = ["egg", "vin", "øl", "ol", "nøtt", "nott"]

def brett(tekst):
    for a, b in (("æ", "ae"), ("Æ", "ae"), ("ø", "o"), ("Ø", "o"), ("å", "a"), ("Å", "a")):
        tekst = tekst.replace(a, b)
    tekst = unicodedata.normalize("NFD", tekst)
    return "".join(c for c in tekst if unicodedata.category(c) != "Mn").lower()

def roerer_vin(tekst):
    b = brett(tekst)
    if any(brett(x) in b for x in ALDRI_BITER): return True
    ord_, naa = set(), ""
    for c in b:
        if c.isalpha() or c.isdigit(): naa += c
        else:
            if naa: ord_.add(naa)
            naa = ""
    if naa: ord_.add(naa)
    return any(brett(x) in ord_ for x in ALDRI_ORD)
