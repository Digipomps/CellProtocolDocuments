# Lager graf/emner-v1.json og graf/emner-v1.md: første forslag til emner for de 18 rettene og 17 drikkene.
# Emnene er hentet fra rettens egen beskrivelse (norsk), korpusets tagger (engelske) og kategorien.
# Skriptet kontrollerer at hvert emne kan spores til en av de tre kildene, og regner eksemplene i planen.
import json, re, sys, collections
K = json.load(open("/mnt/user-data/uploads/PalazzoScaffold/Sources/App/Resources/RestaurantConcierge/palazzo_seed_corpus.json", encoding="utf-8"))

def norm(t):
    t = t.lower()
    for a, b in (("ø","o"),("æ","ae"),("å","a"),("ö","o"),("ä","a"),("ü","u"),("ë","e"),("é","e"),("è","e")): t = t.replace(a, b)
    return re.sub(r"[^a-z0-9]+", " ", t).strip()

KATEGORI = {"antipasti": "forrett", "primi": "pasta", "secondi": "hovedrett", "dolce": "dessert", "pizze": "pizza"}
NAAR = {"antipasti": "til forrett", "primi": "som pastarett", "secondi": "til hovedrett", "dolce": "til dessert", "pizze": None}

# emne -> (vekt, kilde, ordet i kilden). Kilde: B = beskrivelsen, T = tagg i korpuset, K = kategori, N = navnet.
# Vektklasser: 1.0 retten ER dette · 0.7 det retten bygger på · 0.4 nevnt som ingrediens · 0.5 kategori · 0.3 sted eller svak kobling
R = {
 "menu-pane-campagna": [("brød",1.0,"B","landbrød"),("focaccia",1.0,"B","focaccia"),("olivenolje",0.4,"B","olivenolje"),("forrett",0.5,"K","antipasti")],
 "menu-arancini": [("arancini",1.0,"N","arancini"),("ris",0.7,"B","riskroketter"),("ragu",0.4,"B","ragu"),("safran",0.4,"B","safran"),("ost",0.4,"B","ost"),("fritert",0.3,"B","friterte"),("sicilia",0.3,"T","sicily"),("forrett",0.5,"K","antipasti")],
 "menu-ostriche": [("østers",1.0,"B","østers"),("sjømat",0.5,"T","seafood"),("forrett",0.5,"K","antipasti")],
 "menu-carpaccio-polpo": [("blekksprut",1.0,"B","blekksprutcarpaccio"),("carpaccio",0.7,"B","blekksprutcarpaccio"),("potet",0.4,"B","potet"),("selleri",0.4,"B","stangselleri"),("olivenolje",0.4,"B","olivenolje"),("sitron",0.4,"B","sitron"),("sjømat",0.5,"T","seafood"),("forrett",0.5,"K","antipasti")],
 "menu-vitello-tonnato": [("kalv",1.0,"B","kalveroastbiff"),("tunfisk",0.7,"B","tunfiskmajones"),("majones",0.4,"B","tunfiskmajones"),("brissel",0.4,"B","kalvebrissel"),("asparges",0.4,"B","asparges"),("kjøtt",0.5,"B","kalveroastbiff"),("fisk",0.4,"T","fish"),("forrett",0.5,"K","antipasti")],
 "menu-busiate-primavera": [("pasta",1.0,"B","pasta"),("asparges",0.4,"B","asparges"),("erter",0.4,"B","erter"),("fava",0.4,"B","fava"),("mandler",0.4,"B","mandler"),("salvie",0.4,"B","salvie"),("mynte",0.4,"B","mynte"),("sitron",0.4,"B","sitron"),("grønnsaker",0.5,"T","vegetable"),("sicilia",0.3,"T","sicily")],
 "menu-pasta-vongole": [("pasta",1.0,"B","linguine"),("linguine",0.7,"B","linguine"),("skjell",0.7,"B","teppekjell"),("hvitvin",0.4,"B","hvitvin"),("sitron",0.4,"B","sitron"),("persille",0.4,"B","bladpersille"),("sjømat",0.5,"T","seafood")],
 "menu-orata-forno": [("havbrasme",1.0,"B","havbrasme"),("fisk",0.7,"T","fish"),("vedfyrt",0.4,"B","vedfyrt"),("urter",0.4,"B","urter"),("sitron",0.4,"B","sitron"),("potet",0.4,"B","poteter"),("kapers",0.4,"B","kapersmør"),("hovedrett",0.5,"K","secondi")],
 "menu-tagliata-cuvette": [("okse",1.0,"B","okse"),("linser",0.7,"B","linser"),("rødvin",0.4,"B","rødvinsbraiserte"),("salat",0.4,"B","salat"),("potet",0.4,"B","potet"),("kjøtt",0.5,"B","okse"),("modica",0.3,"B","modica"),("hovedrett",0.5,"K","secondi")],
 "menu-agnello-bronte": [("lam",1.0,"B","lammecarré"),("pistasj",0.7,"B","pistasj"),("gulrot",0.4,"B","gulrot"),("løk",0.4,"B","løk"),("kjøtt",0.5,"B","lammecarré"),("bronte",0.3,"B","brontë"),("sicilia",0.3,"T","sicily"),("hovedrett",0.5,"K","secondi")],
 "menu-torta-mascarpone-pistacchi": [("ostekake",1.0,"B","ostekake"),("kake",0.7,"B","ostekake"),("mascarpone",0.7,"B","mascarpone"),("pistasj",0.7,"B","pistasi"),("ost",0.3,"B","ostekake"),("bronte",0.3,"B","brontë"),("dessert",0.5,"K","dolce")],
 "menu-crema-limone": [("sitron",1.0,"B","sitronkrem"),("sorbet",0.7,"B","sitronsorbet"),("krem",0.7,"B","sitronkrem"),("karamell",0.4,"B","karamellisert"),("sicilia",0.3,"T","sicily"),("dessert",0.5,"K","dolce")],
 "menu-formaggi-misti": [("ost",1.0,"B","oster"),("italia",0.3,"B","italia"),("dessert",0.5,"K","dolce")],
 "menu-pizza-margherita": [("pizza",1.0,"K","pizze"),("tomat",0.4,"B","tomatsaus"),("mozzarella",0.4,"B","mozzarella"),("basilikum",0.4,"B","basilikum")],
 "menu-pizza-siciliana": [("pizza",1.0,"K","pizze"),("tomat",0.4,"B","tomatsaus"),("aubergine",0.4,"B","aubergine"),("oliven",0.4,"B","oliven"),("kapers",0.4,"B","kapers"),("caciocavallo",0.4,"B","caciocavallo"),("mozzarella",0.4,"B","mozzarella"),("sicilia",0.3,"T","sicily")],
 "menu-pizza-vulcano": [("pizza",1.0,"K","pizze"),("sterk",0.7,"B","piccant"),("salami",0.4,"B","chilisalami"),("nduja",0.4,"B","nduja"),("chili",0.4,"B","chilisalami"),("tomat",0.4,"B","tomatsaus"),("mozzarella",0.4,"B","mozzarella"),("kjøtt",0.5,"B","chilisalami")],
 "menu-pizza-tartufo-umami": [("pizza",1.0,"K","pizze"),("trøffel",0.7,"B","høsttrøffel"),("salami",0.4,"B","trøffelsalami"),("taleggio",0.4,"B","taleggio"),("mozzarella",0.4,"B","mozzarella"),("kjøtt",0.5,"B","trøffelsalami")],
 "menu-pizza-salina": [("pizza",1.0,"K","pizze"),("ansjos",0.7,"B","ansjos"),("tomat",0.4,"B","tomatsaus"),("hvitløk",0.4,"B","hvitløk"),("kapers",0.4,"B","kapers"),("fisk",0.4,"B","ansjos")],
}
# drikke: bare taggene og navnet finnes (ingen beskrivelse)
D = {
 "bev-frydenlund-05": [("øl",1.0,"T","beer")], "bev-frydenlund-025": [("øl",1.0,"T","beer")], "bev-peroni": [("øl",1.0,"T","beer")],
 "bev-poretti": [("øl",1.0,"T","beer")], "bev-peroni-glutenfri": [("øl",1.0,"T","beer")], "bev-brooklyn-ipa": [("øl",1.0,"T","beer")],
 "bev-carlsberg-free": [("alkoholfritt øl",1.0,"T","non alcoholic"),("alkoholfritt",0.5,"T","non alcoholic")],
 "bev-alkoholfri-vin": [("alkoholfri vin",1.0,"N","alkoholfri vin"),("alkoholfritt",0.5,"T","non alcoholic")],
 "bev-alkoholfri-gin-tonic": [("mocktail",1.0,"T","mocktail"),("alkoholfritt",0.5,"T","non alcoholic")],
 "bev-eplemost": [("eplemost",1.0,"N","eplemost"),("eple",0.7,"N","eplemost"),("juice",0.7,"T","apple juice"),("alkoholfritt",0.5,"T","non alcoholic")],
 "bev-grimstad-brusfabrikk": [("brus",1.0,"T","soda"),("alkoholfritt",0.5,"T","non alcoholic")],
 "bev-ferrarelle": [("vann",1.0,"T","water"),("mineralvann",0.7,"T","sparkling water"),("alkoholfritt",0.5,"T","non alcoholic")],
 "bev-pepsi-max": [("brus",1.0,"T","soda"),("alkoholfritt",0.5,"T","non alcoholic")], "bev-pepsi": [("brus",1.0,"T","soda"),("alkoholfritt",0.5,"T","non alcoholic")],
 "bev-solo": [("brus",1.0,"T","soda"),("alkoholfritt",0.5,"T","non alcoholic")],
 "bev-italian-soda": [("brus",1.0,"T","soda"),("alkoholfritt",0.5,"T","non alcoholic")],
 "bev-dagens-mocktail": [("mocktail",1.0,"T","mocktail"),("alkoholfritt",0.5,"T","non alcoholic")],
}
retter = {m["id"]: m for m in K["menu_items"]}; drikke = {b["id"]: b for b in K["beverage_items"]}
feil = 0
assert set(R) == set(retter), set(retter) ^ set(R)
assert set(D) == set(drikke), set(drikke) ^ set(D)
for rid, emner in R.items():
    m = retter[rid]; b = norm(m["description_nb"]); n = norm(m["name"]); tags = [t.lower() for t in m["tags"]]
    navn = [e[0] for e in emner]; assert len(navn) == len(set(navn)), (rid, navn)
    for emne, vekt, kilde, ord in emner:
        o = norm(ord)
        ok = (kilde == "B" and o in b) or (kilde == "T" and ord in tags) or (kilde == "K" and ord == m["category"]) or (kilde == "N" and o in n)
        if not ok: feil += 1; print("FEIL: kan ikke spores:", rid, emne, kilde, ord)
        assert vekt in (1.0, 0.7, 0.5, 0.4, 0.3)
for did, emner in D.items():
    d = drikke[did]; n = norm(d["name"]); tags = [t.lower() for t in d["tags"]]
    for emne, vekt, kilde, ord in emner:
        ok = (kilde == "T" and ord in tags) or (kilde == "N" and norm(ord) in n)
        if not ok: feil += 1; print("FEIL: kan ikke spores:", did, emne, kilde, ord)
    alk = d["category"] != "non_alcoholic"
    assert alk == (emner[0][0] == "øl"), did

# ---- to regninger for eksemplene i planen
def gjesteflaten(interesser, emner, negskala=1.0):   # vekt på gjestens side × andel av rettens emner som treffes (enhetsvekt på kantene), som PalazzoSignalGraph.contributions
    navn = {e[0] for e in emner}; s = 0.0
    for i, w in interesser.items():
        if i in navn: s += w * 1.0 / len(navn) * (negskala if w < 0 else 1.0)
    return s
def gjesteflaten_vektgrenen(interesser, emner): return gjesteflaten(interesser, emner, 0.5)
def kjernen(interesser, emner):        # sum av gjestens vekt × kantens vekt, som InterestPurposeWeightedSum
    v = {e[0]: e[1] for e in emner}; return sum(w * v[i] for i, w in interesser.items() if i in v)
def forslaget(interesser, emner, negskala=1.0):   # planens forslag: gjesteflatens regning med vekt på kanten.
    # Andelen er summen av vektene på emnene som treffes, delt på summen av alle rettens vekter. Med enhetsvekt er den lik gjesteflaten().
    v = {e[0]: e[1] for e in emner}; alt = sum(v.values()); s = 0.0
    for i, w in interesser.items():
        if i in v: s += w * v[i] / alt * (negskala if w < 0 else 1.0)
    return s
def rangering(interesser, regn, bare=None):
    ut = []
    for rid, emner in R.items():
        if bare and retter[rid]["category"] != bare: continue
        s = regn(interesser, emner)
        if s != 0: ut.append((round(s, 3), retter[rid]["name"]))
    return sorted(ut, key=lambda x: (-x[0], x[1]))
EKS = [("«Jeg liker ost»", {"ost": 1.0}, None), ("«Jeg liker pistasj»", {"pistasj": 1.0}, None), ("«Jeg liker blekksprut»", {"blekksprut": 1.0}, None),
       ("«Jeg liker lam»", {"lam": 1.0}, None), ("«Jeg liker trøffel»", {"trøffel": 1.0}, None), ("«Jeg liker sitron»", {"sitron": 1.0}, None),
       ("«Jeg liker ikke ost», og så desserter", {"ost": -1.0, "dessert": 1.0}, "dolce"), ("«Jeg liker ost», og så desserter", {"ost": 1.0, "dessert": 1.0}, "dolce"),
       ("«Jeg spiser ikke kjøtt», pizzaene", {"kjøtt": -1.0}, "pizze")]
linjer = []
for tittel, i, bare in EKS:
    linjer.append((tittel, rangering(i, gjesteflaten, bare), rangering(i, kjernen, bare)))

# ---- skriv ut
alle = collections.defaultdict(list)
for rid, emner in list(R.items()) + list(D.items()):
    for e in emner: alle[e[0]].append(rid)
ut = {"schema": "palazzo.husgraf.emner.v1", "versjon": "emner-v1-forslag-20261007", "kilde": "palazzo_seed_corpus.json (concierge-knowledge-v0.1, oppdatert 2026-06-03)",
      "vektklasser": {"1.0": "retten er dette", "0.7": "det retten bygger på", "0.5": "kategori", "0.4": "nevnt som ingrediens", "0.3": "sted eller svak kobling"},
      "retter": {rid: [{"emne": e[0], "vekt": e[1], "kilde": {"B": "beskrivelsen", "T": "tagg", "K": "kategori", "N": "navnet"}[e[2]], "ord": e[3]} for e in emner] for rid, emner in R.items()},
      "drikke": {did: [{"emne": e[0], "vekt": e[1], "kilde": {"T": "tagg", "N": "navnet"}[e[2]], "ord": e[3]} for e in emner] for did, emner in D.items()}}
json.dump(ut, open("emner-v1.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
alle_navn_forelopig = set(alle)
md = []
md.append("# Emner for retter og drikke, første forslag (`graf/emner-v1.md`)\n")
md.append("Laget 7. oktober 2026 av Losen med `graf/lag_emner.py`. Dette er data til husets graf (F7), ikke kode, og ingenting er bygget på det ennå. Teksten er rettet samme natt etter de uavhengige kontrollene (K4 og K7): avsnittet om allergener under og regnestykket for «liker ikke» sist er nye. Emnene, koblingene og vektene er de samme, og `graf/emner-v1.json` er uendret.\n")
md.append("Hvert emne er hentet fra én av fire kilder i korpuset (`PalazzoScaffold/Sources/App/Resources/RestaurantConcierge/palazzo_seed_corpus.json`): rettens norske beskrivelse (B), en engelsk tagg (T), kategorien (K) eller navnet (N). Skriptet kontrollerer at hvert emne kan spores til kilden det oppgir; %d emnekoblinger er kontrollert, %d feil.\n" % (sum(len(v) for v in R.values()) + sum(len(v) for v in D.values()), feil))
md.append("Vektene er et første forslag i fem klasser, satt av meg og ikke målt: 1,0 retten er dette · 0,7 det retten bygger på · 0,5 kategori · 0,4 nevnt som ingrediens · 0,3 sted eller svak kobling. Det er disse revisoren (F4) skal foreslå endringer i, og tallene settes ikke fast før første måling.\n")
md.append("Tre ting er holdt utenfor med vilje:\n")
md.append("- **Ingen kant fra ingrediens til allergen.** Majones til egg og smør til melk sier noe om hva retten inneholder, og må komme fra huset. Allergener leses fra merkingen.")
md.append("- **Mozzarella, taleggio og caciocavallo er ikke koblet til «ost».** «Jeg liker ost» ville da gitt fire av fem pizzaer. Koblingen er et spørsmål for målingen.")
md.append("- **Ragu er ikke koblet til «kjøtt».** Beskrivelsen av Arancini sier «ragu», ikke hva raguen er laget av. Det må huset si.\n")
samme = sorted(set(alle_navn_forelopig) & {a["name_nb"] for a in K["allergens"]})
md.append("**Allergenene er ikke emner, og forslaget mangler noder for dem.** " + ("%d emner har samme navn som et allergen i korpusets liste: %s. " % (len(samme), " og ".join("`%s`" % x for x in samme))) + "De er hentet fra ord i beskrivelsene og fra tagger (`selleri` fra «stangselleri» i beskrivelsen av Carpaccio di polpo, som ikke er merket med selleri; `fisk` fra taggen `fish` og fra «ansjos» i beskrivelsen av Pizza Salina), og sier hva kilden nevner, ikke hva retten er merket med. Ingen emner heter nøtter, egg eller melk. Forslaget sier derfor ikke hvilken node «tåler ikke nøtter» skal peke på. Det må inn i datafilen før den nye allergenveien (F8) bygges: én node per allergen i korpusets liste (%d), laget av merkingen og ikke av beskrivelsene. Det gjesten ikke tåler, kan også være et vanlig emne, som løk, eller noe grafen ikke kjenner. Kontrakten sier hva som skjer i hvert av de tre tilfellene (`contract/README.md`, feltet `noted` og regel 2).\n" % len(K["allergens"]))
md.append("## Rettene\n")
md.append("| Rett | Kategori | Emner (vekt, kilde: ordet i kilden) |\n|---|---|---|")
for rid, emner in R.items():
    m = retter[rid]
    md.append("| %s | %s | %s |" % (m["name"], m["category"], "; ".join("%s (%s, %s: %s)" % (e[0], str(e[1]).replace(".", ","), e[2], e[3]) for e in emner)))
md.append("\n## Drikkene\n")
md.append("Drikkene har ingen beskrivelse i korpuset, bare navn og tagger. De seks ølene tilbys aldri (regel 4); de står i grafen så et spørsmål om øl kan kjennes igjen.\n")
md.append("| Drikk | Kategori | Emner |\n|---|---|---|")
for did, emner in D.items():
    d = drikke[did]
    md.append("| %s | %s | %s |" % (d["name"], d["category"], "; ".join("%s (%s, %s: %s)" % (e[0], str(e[1]).replace(".", ","), e[2], e[3]) for e in emner)))
md.append("\n## Emnene, og hvilke retter og drikker de når\n")
md.append("| Emne | Antall | Når |\n|---|---|---|")
for emne in sorted(alle, key=lambda x: (-len(alle[x]), x)):
    md.append("| %s | %d | %s |" % (emne, len(alle[emne]), ", ".join((retter.get(i) or drikke.get(i))["name"] for i in alle[emne])))
md.append("\n## Formålene, første liste\n")
md.append("| Formål | Måltekst (forslag) | Former som gir det (eksempler, ikke hele listen) |\n|---|---|---|")
for f, maal, former in [("spise", "Retten er servert til gjesten (samme måltekst som gjesteflaten har i dag)", "«jeg vil ha …», «jeg har lyst på …», «kan jeg få …», «noe med …»"),
                        ("drikke", "Drikken er servert til gjesten", "«noe å drikke», «har dere eplemost», «hva kan jeg drikke»"),
                        ("vite", "Gjesten har fått svaret fra husets data", "«hva er …», «fortell om …», «hvilke … har dere», «har dere …»"),
                        ("unngå", "Gjesten har fått merkingen og beskrivelsen for det hun spør om, og er vist til personalet", "«jeg tåler ikke …», «jeg er allergisk mot …», «jeg spiser ikke …», «uten …»"),
                        ("bord", "Gjesten har fått vite hvordan hun bestiller bord", "«bestille bord», «booke», «reservere»"),
                        ("åpningstid", "Gjesten har fått åpningstiden, eller beskjed om at den må bekreftes", "«når åpner dere», «åpningstider», «har dere åpent»")]:
    md.append("| %s | %s | %s |" % (f, maal, former))
md.append("\n«Jeg liker …» og «jeg liker ikke …» er ikke formål, men interesser med fortegn.\n")
md.append("## To måter å regne på, med samme emner\n")
md.append("Gjesteflaten regner i dag slik (`PalazzoScaffold/Sources/App/Models/PalazzoSignalGraph.swift`, linje 234–246): gjestens vekt ganger andelen av rettens emner som treffes. Kjernen har en annen ferdig regning (`CellProtocol/Sources/CellBase/PurposeAndInterest/InterestPurposeWeightedSum.swift` på pinnen `81601a6f`): gjestens vekt ganger vekten på kanten, summert. Tabellen viser hva de gir med emnene over. Tallene er regnet av skriptet, ikke av programkoden.\n")
md.append("| Setning | Gjesteflatens regning (enhetsvekt på kantene) | Kjernens regning (vektene over) |\n|---|---|---|")
for tittel, a, b in linjer:
    f = lambda xs: "<br>".join("%s %s" % (str(s).replace(".", ","), n) for s, n in xs) or "ingen"
    md.append("| %s | %s | %s |" % (tittel, f(a), f(b)))
neg = rangering({"ost": -1.0, "dessert": 1.0}, gjesteflaten_vektgrenen, "dolce")
md.append("\nGjesteflatens regning er her regnet med `negativeScale` 1,0, som på grenen som står på nett. Vektene du valgte 2. oktober har `negativeScale` 0,5 (grenen `codex/palazzo-vekter-20260928`). Da blir raden «Jeg liker ikke ost», og så desserter: " + ", ".join("%s %s" % (str(x).replace(".", ","), n) for x, n in neg) + ". Med 1,0 faller osteretten og ostekaken til null; med 0,5 er osteretten fortsatt med. En rett med sum null er utelatt i tabellen; en negativ sum betyr at retten trekkes ned.")
md.append("\nDet tabellen viser: med gjesteflatens regning avgjør antall emner på retten. Formaggi misti har tre emner og Arancini åtte, så «ost» gir osteretten først uten at noen vekt er satt. Med kjernens regning avgjør vekten på kanten. Begge gir osteretten først for «Jeg liker ost» og begge gir to retter for «Jeg liker pistasj». De skiller seg når en rett har mange emner: da taper den i gjesteflatens regning selv om emnet er det retten er.\n")
# ---- «liker ikke», regnet på fire måter (rettet etter kontrollen K4)
md.append("## Et «liker ikke», regnet på fire måter\n")
md.append("Gjesten har sagt «Jeg liker ikke ost», og spør så etter desserter. Testen i spesifikasjonen (`test.samtale.liker-ikke`) krever at osteretten ikke står først, og at den ikke er stengt ute. Tabellen viser alle tre dessertene, også når summen er null. Tallene er regnet av skriptet, ikke av programkoden.\n")
MAATER = [("Gjesteflatens regning, `negativeScale` 1,0 (på nett i dag)", lambda i, e: gjesteflaten(i, e, 1.0)),
          ("Gjesteflatens regning, `negativeScale` 0,5 (vektene du valgte 2. oktober)", lambda i, e: gjesteflaten(i, e, 0.5)),
          ("Planens forslag (vekt på kanten), `negativeScale` 1,0", lambda i, e: forslaget(i, e, 1.0)),
          ("Planens forslag (vekt på kanten), `negativeScale` 0,5", lambda i, e: forslaget(i, e, 0.5))]
DESS = [rid for rid in R if retter[rid]["category"] == "dolce"]
ONSKE = {"ost": -1.0, "dessert": 1.0}
md.append("| Regning | " + " | ".join(retter[r]["name"] for r in DESS) + " | Øverst |\n|---|" + "---|" * (len(DESS) + 1))
for navn, regn in MAATER:
    tall = {r: round(regn(ONSKE, R[r]), 3) for r in DESS}
    best = max(tall.values())
    topp = [retter[r]["name"] for r in DESS if tall[r] == best]
    ost = tall["menu-formaggi-misti"]
    if len(topp) > 1: sier = "likt øverst: " + " og ".join(topp)
    else: sier = topp[0]
    if ost == 0: sier += ". Osteretten har null og faller ut"
    md.append("| %s | %s | %s |" % (navn, " | ".join(str(tall[r]).replace(".", ",") for r in DESS), sier))
    print("liker ikke ost, desserter:", navn, tall, "->", sier)
md.append("\nDet tabellen viser: med vektene du valgte 2. oktober (0,5) og gjesteflatens regning står osteretten likt med sitronkremen øverst, og da avgjør rekkefølgen ved likt tall om testen holder. I de tre andre regningene står sitronkremen alene øverst. Osteretten får null i to av dem og en negativ sum i én, og er da ute av det conciergen foreslår selv for dette spørsmålet. Spesifikasjonen åpner for det (F5: «det kan falle under terskelen for det conciergen foreslår selv, men spør gjesten om det, får hun svar»). Planen foreslår en regel for likt tall (valg 19 i `PLAN.md`), så testen ikke henger på rekkefølgen to like tall får.\n")
open("emner-v1.md", "w", encoding="utf-8").write("\n".join(md) + "\n")
print("emner:", len(alle), "| koblinger:", sum(len(v) for v in R.values()) + sum(len(v) for v in D.values()), "| feil:", feil)
for tittel, a, b in linjer: print(tittel, "\n   gjesteflaten:", a[:4], "\n   kjernen:     ", b[:4])
sys.exit(1 if feil else 0)
