# -*- coding: utf-8 -*-
"""Prototype av dekomponeringen (F1), utgave 2: setning -> formål og interesser med fortegn, uten modell.

Dette er et verksted for å måle raskt mot sølvfasiten. Tallene som rapporteres til Kjetil, kommer fra
Swift-koden. Koden er skrevet med lister og løkker slik at den kan portes linje for linje.

Gangen:
 1. Teksten renses (NFC, usynlige tegn bort, bokstaver som bare ligner, byttes) og deles i setninger
    ved . ! ? ; og linjeskift.
 2. Hver setning deles i ledd ved «men» og lignende, så en nektelse ikke rekker over.
 3. I hvert ledd finnes treff i husets leksikon (Butlers bøyningsregel), stikkord og nektelser.
    Lengste term vinner der to dekker samme ord.
 4. Leddet leses fra venstre: et stikkord styrer treffene etter seg, en nektelse snur det, og et komma
    avslutter det som styrer, hvis det ikke er en oppramsing. Et treff uten stikkord foran kan styres
    av et stikkord rett etter («Hvitløk spiser jeg aldri»).
 5. Formålet settes av det som ble funnet, i fast rekkefølge."""
import unicodedata
from ordtreff import normalize, term_matches_token

STOPPTEGN = ".!?;\n"
KOMMATEGN = ",():–—"
# Bokstaver fra andre alfabeter som ser ut som latinske. En gjest som skriver «аllergi» med kyrillisk a,
# mener allergi.
LIKNER = {u"а": "a", u"е": "e", u"о": "o", u"р": "p", u"с": "c", u"х": "x", u"у": "y",
          u"і": "i", u"ѕ": "s", u"ј": "j", u"һ": "h", u"ԁ": "d", u"ԛ": "q", u"ԝ": "w",
          u"А": "A", u"В": "B", u"Е": "E", u"К": "K", u"М": "M", u"Н": "H", u"О": "O",
          u"Р": "P", u"С": "C", u"Т": "T", u"Х": "X", u"ο": "o", u"α": "a", u"ν": "v",
          u"Α": "A", u"Β": "B", u"Ε": "E", u"Ο": "O"}

NEGATIVE = ("taaler-ikke", "spiser-ikke", "liker-ikke", "utelukker")
RANG = ["taaler-ikke", "spiser-ikke", "liker-ikke", "utelukker", "vil-ha", "liker", "spoer-om", "nevner"]
VERBALE = ("LIKER", "VIL", "SPISER", "TAALER", "SPOER")
ETTERSTILTE = ("LIKER", "LIKER_IKKE", "VIL", "SPISER", "SPISER_IKKE", "TAALER", "ALLERGI", "UNNGAAR")
STERKE = ("ALLERGI", "UNNGAAR", "SPISER_IKKE")

class Spraak(object):
    """Stikkordene, lest fra datafilen. Et mønster er en liste ord; et ord med stjerne sist følger bøyningsregelen."""
    def __init__(self, data):
        sp = data["spraak"]
        self.stikk = []                       # (klasse, [(ord, stamme)])
        for klasse in sorted(sp["stikk"]):
            for m in sp["stikk"][klasse]:
                self.stikk.append((klasse, self.moenster(m)))
        sett = {}
        for klasse, mo in self.stikk:
            n = tuple(mo)
            assert n not in sett, "stikkordet står to steder: %s (%s og %s)" % (mo, sett.get(n), klasse)
            sett[n] = klasse
        self.nektelser = [self.moenster(m) for m in sp["nektelser"]]
        self.engelske_nektelser = [self.moenster(m) for m in sp["engelske_nektelser"]]
        self.engelske_tegn = set(normalize(x) for x in sp["engelske_tegn"])
        self.skiller = set(normalize(x) for x in sp["leddskiller"])
        self.skiller_etter_komma = set(normalize(x) for x in sp["leddskiller_etter_komma"])
        self.spoerreord = set(normalize(x) for x in sp["spoerreord"])
        self.bindeord = set(normalize(x) for x in sp["bindeord"])
        self.kopula = set(normalize(x) for x in sp["kopula"])
        self.sammensatt = [normalize(x) for x in sp["sammensatt"]]
        self.ordlister = {}
        for navn in sorted(sp["ordlister"]):
            self.ordlister[navn] = [self.moenster(m) for m in sp["ordlister"][navn]]

    @staticmethod
    def moenster(tekst):
        ut = []
        for o in tekst.split(" "):
            stamme = o.endswith("*")
            n = normalize(o[:-1] if stamme else o)
            if n:
                for d in n.split(" "): ut.append((d, stamme))
        return ut

def passer(moenster, ord_, i, komma):
    """Sant når mønsteret står i ordlisten fra plass i, uten komma inni."""
    m = len(moenster)
    if i + m > len(ord_): return False
    for j in range(m):
        if j > 0 and (i + j) in komma: return False
        o, stamme = moenster[j]; t = ord_[i + j]
        if t == o: continue
        if stamme and term_matches_token(o, t, False): continue
        return False
    return True

def finnes(moenstre, ord_, komma):
    for m in moenstre:
        for i in range(len(ord_)):
            if passer(m, ord_, i, komma): return True
    return False

def rens(tekst):
    t = unicodedata.normalize("NFC", tekst)
    return "".join(LIKNER.get(c, c) for c in t if unicodedata.category(c) not in ("Cf", "Mn", "Me"))

def setninger(tekst, sp):
    """[[spørsmålstegn, ord, komma, delt]] der komma er plassene et komma står rett foran, og delt er plassene
    til siste halvdel av en sammensetning som ble delt («allergi» i «eggallergi»)."""
    t = rens(tekst)
    ut = []; ord_ = []; komma = set(); delte = set(); buf = []
    def toem():
        s = normalize("".join(buf)); del buf[:]
        if not s: return
        for o in s.split(" "):
            delt = False
            for st in sp.sammensatt:              # «eggallergi» -> «egg», «allergi»
                p = o.find(st)
                if p >= 3:
                    ord_.append(o[:p]); delte.add(len(ord_)); ord_.append(o[p:]); delt = True; break
            if not delt: ord_.append(o)
    n = len(t)
    for i in range(n):
        c = t[i]
        if c in STOPPTEGN:
            if c == "." and 0 < i < n - 1 and t[i - 1].isalnum() and t[i + 1].isalnum():
                buf.append(" "); continue          # «0.5», «f.eks»
            toem()
            if ord_:
                ut.append([c == "?", ord_, komma, delte]); ord_ = []; komma = set(); delte = set()
            elif c == "?" and ut:
                ut[-1][0] = True
        elif c in KOMMATEGN:
            toem()
            if ord_: komma.add(len(ord_))
        else:
            buf.append(c)
    toem()
    if ord_: ut.append([False, ord_, komma, delte])
    return ut

def ledd_av(ord_, komma, delte, sp):
    """Del en setning i ledd ved «men» og lignende, og ved komma fulgt av «så». Gir (ord, komma, delt, plass i setningen)."""
    ut = []; start = 0
    for i in range(len(ord_)):
        if ord_[i] in sp.skiller or (i in komma and ord_[i] in sp.skiller_etter_komma):
            if i > start:
                ut.append((ord_[start:i], set(k - start for k in komma if start < k < i), set(k - start for k in delte if start <= k < i), start))
            start = i + 1
    if start < len(ord_):
        ut.append((ord_[start:], set(k - start for k in komma if start < k < len(ord_)), set(k - start for k in delte if start <= k < len(ord_)), start))
    return ut

class Spenn(object):
    __slots__ = ("start", "slutt", "hva", "termer", "klasse", "tegn", "eksakt")
    def __init__(self, start, slutt, hva, tegn, eksakt, termer=None, klasse=None):
        self.start = start; self.slutt = slutt; self.hva = hva; self.tegn = tegn; self.eksakt = eksakt
        self.termer = termer or []; self.klasse = klasse

def spenn_i(ord_, komma, graf, sp):
    """Alle treff, stikkord og nektelser i leddet. Lengste vinner der to overlapper."""
    K = []
    n = len(ord_)
    for term in graf.termer:
        m = len(term.ord)
        for i in range(n - m + 1):
            ok = True; eks = True
            for j in range(m):
                if j > 0 and (i + j) in komma: ok = False; break
                t = ord_[i + j]; o = term.ord[j]
                if t == o: continue
                if term.eksakt or j < m - 1: ok = False; break
                if m == 1 and any(term_matches_token(u, t, False) for u in graf.unntak.get(o, ())): ok = False; break
                if term_matches_token(o, t, m == 1): eks = False
                else: ok = False; break
            if ok: K.append(Spenn(i, i + m, "treff", term.tegn, eks, [term]))
    for klasse, mo in sp.stikk:
        for i in range(n):
            if passer(mo, ord_, i, komma):
                K.append(Spenn(i, i + len(mo), "stikk", sum(len(o) for o, _ in mo) + len(mo) - 1, True, None, klasse))
    engelsk = any(t in sp.engelske_tegn for t in ord_)
    for mo in sp.nektelser + (sp.engelske_nektelser if engelsk else []):
        for i in range(n):
            if passer(mo, ord_, i, komma):
                K.append(Spenn(i, i + len(mo), "nekt", sum(len(o) for o, _ in mo) + len(mo) - 1, True))
    prio = {"treff": 0, "stikk": 1, "nekt": 2}
    K.sort(key=lambda s: (-(s.slutt - s.start), -s.tegn, not s.eksakt, prio[s.hva], s.start))
    valgt = []
    for s in K:
        lik = None
        for v in valgt:
            if v.hva == "treff" and s.hva == "treff" and v.start == s.start and v.slutt == s.slutt and v.tegn == s.tegn and v.eksakt == s.eksakt:
                lik = v; break
        if lik is not None:
            lik.termer.extend(s.termer); continue     # samme ord, flere noder
        if any(not (s.slutt <= v.start or s.start >= v.slutt) for v in valgt): continue
        valgt.append(s)
    valgt.sort(key=lambda s: s.start)
    return valgt

def effektivt(klasse, nekt):
    if klasse == "LIKER": return "liker-ikke" if nekt else "liker"
    if klasse == "LIKER_IKKE": return "liker-ikke"
    if klasse == "VIL": return "spiser-ikke" if nekt else "vil-ha"
    if klasse == "SPISER": return "spiser-ikke" if nekt else None
    if klasse == "SPISER_IKKE": return "spiser-ikke"
    if klasse == "TAALER": return "taaler-ikke" if nekt else None
    if klasse == "ALLERGI": return "taaler-ikke"
    if klasse in ("UNNGAAR", "UTEN"): return "spiser-ikke"
    if klasse == "UTELUKK": return "utelukker"
    if klasse == "SPOER": return "spoer-om"
    return None

def noder_for(termer, slag):
    """Velg noder for et treff ut fra hva som sies om det. Tom liste: ordet gir ingen node her."""
    navn = [t for t in termer if t.type in ("rett", "drikk")]
    if navn:
        return [(n, t.type) for t in navn for n in t.noder]
    emner = [t for t in termer if t.type == "emne"]
    allerg = [t for t in termer if t.type == "allergen"]
    if allerg and (slag == "taaler-ikke" or not emner):
        if slag in ("taaler-ikke", "spiser-ikke", "utelukker", "spoer-om", "liker-ikke"):
            return [(n, "allergen") for t in allerg for n in t.noder]
        return []
    return [(n, "emne") for t in emner for n in t.noder]

def les_ledd(ord_, komma, delte, spm, graf, sp):
    """Les ett ledd fra venstre. Gir treffene med slag, hva slags stikkord som sto der, og om noe ukjent ikke tåles."""
    spenn = spenn_i(ord_, komma, graf, sp)
    ut = []            # {"termer","slag","ord","start","slutt"}
    klasser = []; ukjent = [False]
    klasse = None      # stikkordet som styrer treffene som kommer
    nekt = False       # om det er nektet
    foer_uten = None   # det som styrte før et «uten»
    siste_nekt = None  # slutten på en nektelse som ikke har fått noe etter seg ennå
    venter = []        # treff uten slag, som et stikkord rett etter kan styre
    aapen = None       # [klasse, har fått et treff, er nektet, plass i klasser]: stikkord som trenger noe å gjelde
    forrige_slutt = 0
    def lukk():
        if aapen is not None and not aapen[1]:
            if aapen[0] == "ALLERGI" or (aapen[0] == "TAALER" and aapen[2]): ukjent[0] = True
    for idx in range(len(spenn)):
        s = spenn[idx]
        # et komma avslutter det som styrer, hvis ikke det som kommer er neste ledd i en oppramsing
        if klasse is not None:
            siste_komma = None
            for c in komma:
                if forrige_slutt <= c <= s.start and (siste_komma is None or c > siste_komma): siste_komma = c
            if siste_komma is not None:
                fortsetter = False
                if s.hva == "treff" and s.start - siste_komma <= 2: fortsetter = True
                if s.hva == "nekt" and idx + 1 < len(spenn) and spenn[idx + 1].hva == "treff" and spenn[idx + 1].start - siste_komma <= 3: fortsetter = True
                if not fortsetter:
                    lukk(); aapen = None
                    klasse = None; nekt = False; siste_nekt = None
        forrige_slutt = s.slutt
        if s.hva == "nekt":
            nekt = True; siste_nekt = s.slutt
            if aapen is not None: aapen[2] = True
            continue
        if s.hva == "stikk":
            k = s.klasse
            if k == "TOM":                # «uten at», «allergener»: ord som ligner et stikkord, og ikke er det
                continue
            if k == "HOEFLIG":            # «takk», «please»: det som ble nevnt foran, er et ønske
                for v in venter:
                    if v["slag"] is None: v["slag"] = "vil-ha"
                klasser.append(k)
                continue
            if k == "MED":                # «uten ost med ekstra tomat»: «uten» slutter å gjelde
                if klasse == "UTEN": klasse = foer_uten; nekt = False
                continue
            if k == "SPISER" and (klasse in STERKE or (klasse == "TAALER" and nekt)):
                continue                  # «allergisk ... får i seg egg»: det sterke stikkordet står
            if k in VERBALE: nekt = siste_nekt is not None and s.start - siste_nekt <= 3
            elif k != "UTEN": nekt = False
            fikk = False
            if k in ETTERSTILTE:          # «Hvitløk spiser jeg aldri», «Ost er ikke noe for meg»
                etter = False
                if idx + 1 < len(spenn):
                    x = spenn[idx + 1]
                    if x.hva == "nekt" and x.start - s.slutt <= 3 and not any(s.slutt <= c <= x.start for c in komma):
                        etter = True
                grense = s.start; rekkevidde = 4
                for vi in range(len(venter) - 1, -1, -1):
                    v = venter[vi]
                    if v["slag"] is not None: break
                    if grense - v["slutt"] > rekkevidde: break
                    if grense == s.start and any(v["slutt"] <= c <= s.start for c in komma): break
                    if grense != s.start:
                        mellom_ord = ord_[v["slutt"]:grense]      # «salami og lagrede oster»: ett bindeord og høyst ett ord til
                        if len(mellom_ord) > 2 or (mellom_ord and not any(o in sp.bindeord for o in mellom_ord)): break
                    mellom = False
                    for x in spenn:
                        if x.hva == "nekt" and v["slutt"] <= x.start and x.slutt <= s.start: mellom = True
                    e = effektivt(k, nekt or mellom or etter)
                    if e is None: break
                    v["slag"] = e; fikk = True
                    grense = v["start"]; rekkevidde = 3      # videre bakover i en oppramsing
            lukk()
            klasser.append(k + ("+nekt" if nekt else ""))
            if s.start in delte and not fikk:
                if effektivt(k, nekt) == "taaler-ikke": ukjent[0] = True     # «soppallergi»: noe grafen ikke kjenner
                fikk = True
            if fikk:
                # stikkordet har fått det det gjelder, foran seg; det styrer ikke det som kommer etter
                klasse = None; nekt = False; siste_nekt = None; aapen = None
                continue
            if k == "UTEN" and klasse != "UTEN": foer_uten = klasse
            klasse = k; siste_nekt = None
            aapen = [k, False, nekt, len(klasser) - 1]
            continue
        # et treff
        fast = None                   # ord som selv sier slaget («cøliaki», «glutenfri»); det strengeste gjelder
        for t in s.termer:
            if t.slag and (fast is None or RANG.index(t.slag) < RANG.index(fast)): fast = t.slag
        if fast is not None:
            e = fast
            if fast == "spiser-ikke" and ut and ord_[0] in sp.kopula:
                e = "spoer-om"            # «Er Pizza Margherita glutenfri?» spør om retten har det
        elif klasse is None:
            # uten stikkord foran: en nektelse rett foran gjør det til noe gjesten ikke vil ha («ingen nøtter»)
            e = "spiser-ikke" if (nekt and siste_nekt is not None and s.start - siste_nekt <= 1) else None
        else:
            e = effektivt(klasse, nekt)
        v = {"termer": s.termer, "slag": e, "ord": " ".join(ord_[s.start:s.slutt]), "start": s.start, "slutt": s.slutt}
        ut.append(v)
        if e is None: venter.append(v)
        if aapen is not None: aapen[1] = True
        # en oppramsing fortsetter: «ingen nøtter eller egg»
        if klasse is None and e == "spiser-ikke": siste_nekt = s.slutt
        elif klasse is None: siste_nekt = None; nekt = False
        else: siste_nekt = None
    lukk()
    if aapen is not None and aapen[2] and aapen[0] in ("SPISER", "TAALER") and not klasser[aapen[3]].endswith("+nekt"):
        klasser[aapen[3]] = klasser[aapen[3]] + "+nekt"      # «tåler det ikke»: nektelsen kom etter stikkordet
    for v in ut:                       # det som står igjen: spørsmål eller bare nevnt
        if v["slag"] is None: v["slag"] = "spoer-om" if spm else "nevner"
    return ut, klasser, ukjent[0]

def dekomponer(tekst, graf, sp):
    alle = []; klasser = []; ukjent = False; spm_noe = False; spm_tegn = False
    setn = []
    for nr, (tegn, ord_, komma, delte) in enumerate(setninger(tekst, sp)):
        spm = tegn or (ord_[0] in sp.spoerreord)
        spm_noe = spm_noe or spm; spm_tegn = spm_tegn or tegn
        setn.append((ord_, komma, spm))
        for l_ord, l_komma, l_delte, plass in ledd_av(ord_, komma, delte, sp):
            ut, kl, uk = les_ledd(l_ord, l_komma, l_delte, spm, graf, sp)
            klasser += kl
            ledd_noder = []
            for v in ut:
                alt = sorted(n for t in v["termer"] if t.type == "allergen" for n in t.noder)
                for node, type_ in noder_for(v["termer"], v["slag"]):
                    ledd_noder.append({"node": node, "type": type_, "slag": v["slag"], "ord": v["ord"], "setning": nr, "plass": plass + v["start"],
                                       "allergen": alt[0] if (alt and type_ == "emne") else None})
            # retten sluker emnet som står i navnet («Pizza Tartufo» er pizzaen, ikke pizzalisten)
            navn = set()
            for x in ledd_noder:
                if x["type"] in ("rett", "drikk"): navn |= graf.navneord_i_navn[x["node"]]
            for x in ledd_noder:
                if x["type"] == "emne":
                    ordene = [o for o in normalize(x["node"][5:]).split(" ") if o]
                    if ordene and all(o in navn for o in ordene): continue
                alle.append(x)
            if uk:
                # «…, da jeg reagerer på den»: det gjelder det siste som ble nevnt som noe å unngå, eller
                # det siste allergenet det ble spurt om. Finnes ingen av delene, er det noe grafen ikke kjenner.
                funnet = None
                for x in reversed(alle):
                    if x["slag"] in ("spiser-ikke", "taaler-ikke"): funnet = x; break
                if funnet is None:
                    for x in reversed(alle):
                        if x["type"] == "allergen": funnet = x; break
                if funnet is not None:
                    funnet["slag"] = "taaler-ikke"
                    if funnet["type"] == "emne" and funnet.get("allergen"):
                        # det hun ikke tåler, har samme navn som et allergen: noden er allergenet
                        funnet["node"] = funnet["allergen"]; funnet["type"] = "allergen"; funnet["allergen"] = None
                else: ukjent = True
    if ukjent: alle.append({"node": "ukjent", "type": "ukjent", "slag": "taaler-ikke", "ord": "", "setning": -1, "plass": -1})
    # like noder slås sammen; det strengeste slaget vinner
    beste = {}; rekke = []
    for x in alle:
        if x["node"] not in beste: beste[x["node"]] = x; rekke.append(x["node"])
        elif RANG.index(x["slag"]) < RANG.index(beste[x["node"]]["slag"]): beste[x["node"]] = x
    noder = [beste[n] for n in rekke]
    slagene = set(x["slag"] for x in noder)

    def liste(navn, bare_utsagn=False):
        for o, k, spm in setn:
            if bare_utsagn and spm: continue
            if finnes(sp.ordlister[navn], o, k): return True
        return False
    def foerste_tegn():
        """Det første i teksten som sier mat eller drikke: 'D', 'F' eller None."""
        for nr in range(len(setn)):
            o, k, _ = setn[nr]
            for i in range(len(o)):
                for m in sp.ordlister["drikkeord"]:
                    if passer(m, o, i, k): return "D"
                for m in sp.ordlister["spiseord"]:
                    if passer(m, o, i, k): return "F"
                for x in alle:
                    if x["setning"] == nr and x["plass"] == i:
                        if x["type"] == "drikk": return "D"
                        if x["type"] == "rett": return "F"
                        if x["type"] == "emne":
                            e = x["node"][5:]
                            if e in graf.drikkeemner: return "D"
                            if e not in graf.stedsemner: return "F"
        return None

    like = set(["liker", "liker-ikke"])
    unngaa = bool(slagene & set(["taaler-ikke", "spiser-ikke"])) or any(
        k in ("ALLERGI", "UNNGAAR", "SPISER_IKKE", "UTEN", "SPISER+nekt", "TAALER+nekt") for k in klasser)
    vil = "vil-ha" in slagene or "VIL" in klasser or liste("sulten") or liste("torst")
    if unngaa: formaal = "unngaa"
    elif liste("bord"): formaal = "bord"
    elif liste("aapningstid"): formaal = "aapningstid"
    elif liste("kosthold", True): formaal = "unngaa"
    elif vil:
        tegn = "D" if liste("torst") else foerste_tegn()
        formaal = "drikke" if tegn == "D" else "spise"
    elif slagene and not (slagene - like) and not spm_tegn: formaal = None      # bare det hun liker eller ikke liker
    elif spm_noe:
        if liste("har_dere") and foerste_tegn() == "D": formaal = "drikke"
        elif noder or liste("hus"): formaal = "vite"
        else: formaal = None
    elif "SPOER" in klasser and (noder or liste("hus")): formaal = "vite"
    elif noder and sum(len(o) for o, _, _ in setn) <= 4: formaal = "vite"       # bare et navn: fortell om det
    else: formaal = None
    allergi = "taaler-ikke" in slagene or "ALLERGI" in klasser or any(x["type"] == "allergen" for x in noder)
    return {"formaal": formaal, "noder": noder, "allergi": bool(allergi), "klasser": klasser}

def merkelapp(d):
    """Formålet slik sølvfasiten skriver det: uten formål er 'selv' når gjesten sier noe om seg selv, ellers 'ingen'."""
    if d["formaal"] is not None: return d["formaal"]
    if any(x["node"] != "ukjent" for x in d["noder"]): return "selv"
    if any(k.startswith("LIKER") for k in d["klasser"]): return "selv"
    return "ingen"
