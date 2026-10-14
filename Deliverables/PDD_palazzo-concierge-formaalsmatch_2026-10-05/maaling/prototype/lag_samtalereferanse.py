# -*- coding: utf-8 -*-
"""Skriver referansen for samtalen: en rekke samtaler, hver med stegene sine, og det samtale_sim.py gir for hvert steg.
Swift-testen PalazzoSamtaleReferanseTests krever at Swift-koden gir det samme, steg for steg.
Bruk: python3 -B lag_samtalereferanse.py <datafil> <ut.json> [vis]
Fra oppgavemappen på Mac-en: python3 -B maaling/prototype/lag_samtalereferanse.py graf/palazzo_husgraf-20261007.5.json <ut.json> vis"""
import json, sys, importlib.util
import husgraf, dekomp, samtale_sim as S

def ordliste():
    """Strakstiltakets ordliste, regnet utenfor Swift (HAVEN-Deploy/_handoff/HD-0077/maal/grunnlag-20261006/ordliste_strakstiltak.py,
    relativt til HAVEN-roten). PALAZZO_ORDLISTE overstyrer."""
    import os, stier
    sti = os.environ.get("PALAZZO_ORDLISTE", os.path.join(stier.HAVEN, "HAVEN-Deploy", "_handoff", "HD-0077", "maal", "grunnlag-20261006", "ordliste_strakstiltak.py"))
    spec = importlib.util.spec_from_file_location("ordliste_strakstiltak", sti)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return lambda tekst: bool(m.treff(tekst))

# Hver samtale: navn, og stegene. Et steg er en setning (streng) eller et valg (liste).
SAMTALER = [
    ("ost-og-ja", ["Jeg liker ost", ["tilbud", True, "menu-formaggi-misti"]]),
    ("ost-og-nei", ["Jeg liker ost", ["tilbud", False, "menu-formaggi-misti"]]),
    ("tilbud-forrett", ["Jeg liker blekksprut"]),
    ("tilbud-hovedrett", ["Jeg liker lam"]),
    ("tilbud-pizza", ["Jeg liker trøffel"]),
    ("tilbud-drikke", ["Jeg liker eplemost"]),
    ("forteller-pistasj", ["Jeg liker pistasj"]),
    ("liker-ikke-ost", ["Jeg liker ikke ost", "Hva har dere til dessert?", "Har dere oster?"]),
    ("taaler-ikke-noetter", ["Jeg tåler ikke nøtter.", "Jeg liker ost", "Hva har dere til dessert?", ["tilbud", True, "menu-formaggi-misti"]]),
    ("spiser-ikke-kjoett", ["Jeg spiser ikke kjøtt", "Hvilke pizzaer har dere?", "Jeg liker ikke ost", "Jeg liker ikke kjøtt",
                            "Jeg spiser ikke fisk og liker ikke ost", "Jeg liker ost"]),
    ("vegetarianer", ["Jeg er vegetarianer", "Jeg liker ost"]),
    ("alkohol", ["Jeg liker øl", "Har dere alkoholfritt øl?", "Har dere alkoholfri vin?", "Jeg liker ost"]),
    ("lister", ["Hvilke pizzaer har dere?", "Hva har dere til dessert?", "Noe uten alkohol?", "Har dere brus?", "Har dere forretter?"]),
    ("navngitt", ["Fortell om Arancini", "Jeg vil ha Eplemost", "Jeg liker Arancini", "Fortell om Arancini og Vitello tonnato", "Jeg liker ikke Arancini", "Har dere Eplemost?"]),
    ("men", ["Jeg liker ikke ost, men jeg vil gjerne ha Pizza Tartufo", "Jeg liker ikke fisk, men gjerne pasta"]),
    ("bom", ["Hei", "Kan jeg bestille bord?", "Når åpner dere?", "Har dere noe sånt som risboller?", "Hva anbefaler du?", "Hva har dere som ikke er pizza?"]),
    ("klar-leder", ["Jeg liker sitron", "Jeg liker sjømat"]),
    ("notert-teller-med", ["Jeg liker ost", "Hva har dere til dessert?", "Jeg liker pistasj"]),
    ("fjern", ["Jeg liker pistasj", "Jeg liker ikke ost", "Jeg spiser ikke kjøtt", ["fjern", "emne:ost"], ["fjern-alt"]]),
    ("allergen-uten", ["uten gluten", "Jeg liker ost"]),
    ("spiser-ikke-fisk", ["Jeg spiser ikke fisk", "Jeg liker ost"]),
    ("ombestemmer-seg", ["Jeg liker ost", "Jeg liker ikke ost", "Jeg liker ost"]),
    ("det-strengeste-staar", ["Jeg spiser ikke kjøtt", "Jeg liker kjøtt", "Jeg tåler ikke løk", "Jeg liker løk"]),
    ("to-emner", ["Jeg liker ost og pistasj", "Jeg liker tomat og mozzarella"]),
    ("notert-bringer-ikke-inn", ["Jeg liker ost", "Jeg liker lam", "Jeg liker trøffel"]),
    ("ukjent", ["Jeg tåler ikke kanel", "Hva har dere til dessert?", ["fjern", "ukjent"], "Hva har dere til dessert?"]),
    ("liker-ikke-trekker-ned", ["Jeg liker ikke mozzarella", "Hvilke pizzaer har dere?"]),
    # Ord for allergener som grafen kjenner og strakstiltakets liste ikke har: samme svar som listens ord.
    ("allergenord-utenfor-listen", ["Jeg liker ikke nødder", "Har dere æg?", "Jeg liker pistasj"]),
    # Det samme for emner med samme ord som et allergen: «seleri» og «fesk» får samme svar som «selleri» og «fisk».
    ("allergenord-som-ogsaa-er-emner", ["Har dere seleri?", "Jeg liker ikke fesk", "uten seleri", "Jeg liker ost"]),
    ("fjern-to-ganger", ["Jeg liker ost", ["fjern", "emne:ost"], ["fjern", "emne:ost"]]),
    ("vil-ha-og-liker-ikke", ["Jeg vil ha Arancini", "Jeg liker ikke Arancini", ["fjern", "menu-arancini"]]),
    # Alkoholfritt øl, alkoholfri vin og alkoholfri gin tonic går som øl og vin, også ved navn.
    ("alkoholfritt-ved-navn", ["Har dere Carlsberg?", "Jeg vil ha en Carlsberg Free", "Har dere mocktail?", "Har dere juice?",
                               "Har dere alkoholfri gin tonic?", "Jeg liker Alkoholfri Gin Tonic"]),
    # Skrivemåter for alkoholfritt uten ordet alkohol: setningen når matchen. Listen har en overskrift som ikke sier
    # «uten», og verken øl eller vin, heller ikke de alkoholfrie.
    ("alkoholfritt-uten-ordet", ["Har dere alkofri?", "Jeg liker alkfri", "uten alk", "Har dere alc free?"]),
    # «Spiser ikke» om en drikk med alkohol ved siden av en henvisning: drikken noteres ikke, og det som står notert,
    # kan sendes tilbake. Uten dette fikk siden 422 på hvert kall etterpå (lest 7. oktober 2026).
    ("alkohol-ved-henvisning", ["Jeg tåler ikke nøtter. Jeg spiser ikke Peroni.", "Jeg liker ost", ["fjern-alt"], "Jeg liker ost"]),
    ("alkohol-spiser-ikke", ["Jeg drikker ikke Peroni.", "Jeg spiser ikke Carlsberg Free og tåler ikke egg.", "Hva har dere til dessert?",
                             ["fjern", "allergen:E"], "Jeg liker ost"]),
    # Det uavhengige angrepet 7. oktober 2026: et alkoholemne kan ikke stå notert, og allergi skrevet som helse får henvisningen.
    ("alkoholemne-noteres-ikke", ["Jeg tåler ikke nøtter og drikker ikke øl.", "Jeg liker ikke vin, men liker ost", "Jeg tåler ikke øl", "Jeg liker ost"]),
    ("allergi-som-helse", ["Mozzarella gjør meg syk. Hva har dere av pizza?", "Hva har dere til dessert?", "Pistasj kan drepe meg.",
                           "Tomat gir meg kvalme. Hva har dere av pizza?", ["fjern", "emne:mozzarella"], "Jeg liker ost"]),
    # Setningene i de avledede testene i FORMAALSSPEC.md §5 (F5 og F6).
    ("spek-liker", ["Jeg liker ost", "Hva anbefaler dere til dessert?"]),
    ("spek-liker-ikke", ["Jeg liker ikke ost", "Hva anbefaler dere til dessert?", "Har dere oster?"]),
    ("spek-formaal", ["Jeg vil ha noe med ost"]),
    ("spek-spoersmaal-noterer-ikke", ["Er det nøtter i ostekaken?"]),
    ("spek-vin", ["Hvilken vin passer til pasta vongole?"]),
    ("spek-egg", ["Jeg tåler ikke egg.", "Hva har dere av forretter?", "Jeg liker ost"]),
    ("spek-selleri", ["Jeg tåler ikke selleri.", "Hva har dere av forretter?"]),
    ("flere", ["Jeg vil ha en pizza", "Jeg vil ha pizza Margherita", "Har dere noe med trøffel?", "Noe søtt?", "Hva er Arancini?",
               "Jeg vil ha Solo og Arancini", "Jeg er sulten", "takk", "Hva har dere å drikke?", "Kan jeg få Tiramisu?"]),
]
# Valg som skal avvises (422).
AVVISTE_VALG = [
    ("ukjent-tilbud", [], ["tilbud", True, "menu-finnes-ikke"]),
    ("tilbud-med-alkohol", [], ["tilbud", True, "bev-peroni"]),
    ("tilbud-alkoholfritt-oel", [], ["tilbud", True, "bev-carlsberg-free"]),
    ("fjern-ukjent-node", [["liker", "emne:ost"]], ["fjern", "emne:finnes-ikke"]),
]

def kontroller(g):
    """Det tekstene forutsetter om dataene. Feiler høyt i stedet for å gi en setning som ikke stemmer."""
    svar = g.data["graf"]["svar"]
    for pid, p in list(g.retter.items()) + list(g.drikke.items()):
        d = p.get("description_nb")
        if d: assert d.strip()[-1] in ".!?", "beskrivelsen til %s slutter ikke med punktum" % pid
        if pid in g.retter: assert d, "retten %s har ingen beskrivelse" % pid
    DRIKKEFORM = ("drikker", "slags brus", "mocktailer")
    for emne, form in svar["fortell"].items():
        poster = [pid for pid, _ in g.kanter[emne] if not S.alkoholnaer(g, pid)]
        drikke = [pid in g.drikke for pid in poster]
        assert all(drikke) or not any(drikke), "emnet %s fører til både retter og drikke; overskriften «%s» passer ikke" % (emne, form)
        assert form.startswith(DRIKKEFORM) == all(drikke), "overskriften «%s» for %s sier feil slag" % (form, emne)
    for emne, form in svar["fortell"].items():
        for ord in ("uten", "fri", "trygg", "sikker"):
            assert ord not in form, "overskriften «%s» for %s sier noe svarene ikke skal si" % (form, emne)
    for emne in svar["alkoholemner"]:
        # Et alkoholemne kan føre til en rett som har vin i beskrivelsen (valg 14), men aldri til en drikk uten alkohol.
        assert not any(pid in g.drikke and not S.alkohol(g, pid) for pid, _ in g.kanter[emne]), emne
    for pid in list(g.retter) + list(g.drikke):
        if not S.alkoholnaer(g, pid): assert S.kan_nevnes(g, pid), "posten %s kan ikke nevnes" % pid
    # Alkoholfrie utgaver av øl og vin er de to korpuset har i dag. Kommer det en til, skal det ses her.
    naer = sorted(pid for pid in g.drikke if S.alkoholnaer(g, pid) and not S.alkohol(g, pid))
    assert naer == ["bev-alkoholfri-gin-tonic", "bev-alkoholfri-vin", "bev-carlsberg-free"], naer
    # Et alkoholemne kan ikke stå notert, uansett slag (det uavhengige angrepet 7. oktober 2026).
    for emne in g.data["graf"]["svar"]["alkoholemner"]:
        for slag in ("liker", "liker-ikke", "spiser-ikke", "vil-ha", "taaler-ikke"):
            assert not S.gyldig_notat(g, slag, "emne:" + emne), (slag, emne)

def genererte(g):
    """Samtaler laget av grafen selv: hver rett og drikk ved navn, og hvert emne. De holder Swift-koden mot
    referansen på alt huset har, ikke bare på setningene noen har tenkt på."""
    ut = []
    for pid, p in list(g.retter.items()) + list(g.drikke.items()):
        ut.append(("post-" + pid, ["Jeg liker " + p["name"], "Fortell om " + p["name"], "Jeg vil ha " + p["name"]]))
    for emne in sorted(g.kanter):
        ut.append(("emne-" + emne, ["Jeg liker " + emne, "Har dere " + emne + "?"]))
    return ut

def valg_ut(v):
    """Valget slik referansen skriver det: et objekt, så Swift-testen kan lese det med faste felt."""
    if v[0] == "tilbud": return {"slag": "tilbud", "ja": bool(v[1]), "ref": v[2]}
    if v[0] == "fjern": return {"slag": "fjern", "node": v[1]}
    if v[0] == "fjern-alt": return {"slag": "fjern-alt"}
    raise ValueError(v)

def kjoer(datafil):
    data = json.load(open(datafil, encoding="utf-8"))
    g = husgraf.Graf(data, json.load(open(husgraf.KORPUS, encoding="utf-8"))); sp = dekomp.Spraak(data)
    treffer = ordliste()
    kontroller(g)
    ut = {"schema": "palazzo.samtale-referanse.v1", "versjon": data["versjon"], "terskel": g.terskel, "klar_leder": data["graf"]["svar"]["klar_leder"],
          "skrevne": len(SAMTALER), "samtaler": [], "avviste_valg": []}
    for navn, steg in SAMTALER + genererte(g):
        notert = []
        rader = []
        for s in steg:
            foer = [{"kind": a, "node": b} for a, b in notert]
            if isinstance(s, str):
                u, notert, f = S.paa_setning(s, notert, g, sp, treffer, S.roerer_vin)
                rad = {"setning": s}
            else:
                u, notert = S.paa_valg(tuple(s), notert, g)
                f = None
                rad = {"valg": valg_ut(s)}
            # Alt som står notert, må kunne sendes tilbake: tjeneren avviser (422) en post gyldig_notat ikke godtar.
            for s2, n in notert:
                assert S.gyldig_notat(g, s2, n), "steget «%s» i %s noterte (%s, %s), som ikke kan sendes tilbake" % (s, navn, s2, n)
            rad.update({
                "notert_foer": foer, "vei": u["vei"], "kind": u["kind"], "grunn": u["grunn"], "bom": u["bom"], "tekst": u["tekst"], "linjer": u["linjer"],
                "poster": u["poster"], "tilbud": u["tilbud"],
                "treff": [{"ref": t["post"], "score": round(t["sum"], 3), "because": [{"node": r["node"], "word": r["ord"], "negative": r["negativ"]} for r in t["fordi"]]} for t in u["treff"]],
                "notert": [{"kind": s2, "node": n, "label": S.merkelapp(g, s2, n)} for s2, n in notert],
                "forstaatt": f,
            })
            rader.append(rad)
        ut["samtaler"].append({"navn": navn, "steg": rader})
    for navn, notert, valg in AVVISTE_VALG:
        try:
            S.paa_valg(tuple(valg), [tuple(x) for x in notert], g)
            raise SystemExit("valget %s skulle vært avvist" % navn)
        except ValueError as e:
            ut["avviste_valg"].append({"navn": navn, "notert": [{"kind": a, "node": b} for a, b in notert], "valg": valg_ut(valg)})
    return ut, g

if __name__ == "__main__":
    ut, g = kjoer(sys.argv[1])
    json.dump(ut, open(sys.argv[2], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    n = sum(len(s["steg"]) for s in ut["samtaler"])
    print("skrevet", sys.argv[2], "samtaler:", len(ut["samtaler"]), "steg:", n, "avviste valg:", len(ut["avviste_valg"]))
    if len(sys.argv) > 3:
        for s in ut["samtaler"]:
            print("\n== " + s["navn"])
            for r in s["steg"]:
                inn = r.get("setning") or json.dumps(r.get("valg"), ensure_ascii=False, sort_keys=True)
                print("  > %s" % inn)
                print("    %s/%s grunn=%s bom=%s%s" % (r["vei"], r["kind"], r["grunn"], r["bom"], ("  forstått: " + r["forstaatt"]["text"]) if r["forstaatt"] else ""))
                if r["tekst"]: print("    " + r["tekst"].replace("\n", "\n    "))
                if r["linjer"]: print("    advarsler: " + " | ".join(x[:44] for x in r["linjer"]))
                if r["treff"]: print("    treff: " + ", ".join("%s %.3f" % (t["ref"], t["score"]) for t in r["treff"]))
                print("    notert: " + (", ".join(x["label"] for x in r["notert"]) or "(ingenting)"))
