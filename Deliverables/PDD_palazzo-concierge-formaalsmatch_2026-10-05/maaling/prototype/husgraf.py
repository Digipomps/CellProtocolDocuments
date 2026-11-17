# -*- coding: utf-8 -*-
"""Prototype: husets graf lest fra datafilen og korpuset, og leksikonet dekomponeringen slår opp i.
Speiler det Swift-koden skal gjøre. Navn, kategori og merking leses bare fra korpuset (test.graf.en-kilde)."""
import json
from ordtreff import normalize

from stier import KORPUS

class Term(object):
    """Én oppføring i leksikonet: ordene (normalisert), nodene den gir, typen og et eventuelt fast slag."""
    __slots__ = ("ord", "eksakt", "noder", "type", "slag", "tegn")
    def __init__(self, ord_, eksakt, noder, type_, slag=None):
        self.ord = ord_; self.eksakt = eksakt; self.noder = noder; self.type = type_; self.slag = slag
        self.tegn = sum(len(o) for o in ord_) + len(ord_) - 1

def les_term(tekst):
    """«=mel» er et ord som bare treffer nøyaktig; ellers gjelder bøyningsregelen."""
    eksakt = tekst.startswith("=")
    return normalize(tekst[1:] if eksakt else tekst).split(" "), eksakt

class Graf(object):
    def __init__(self, data, korpus):
        self.data = data
        g = data["graf"]
        self.versjon = data["versjon"]
        self.terskel = g["terskel"]
        self.formaal = {f["id"]: f["maal"] for f in g["formaal"]}
        self.retter = {m["id"]: m for m in korpus["menu_items"]}
        self.drikke = {b["id"]: b for b in korpus["beverage_items"]}
        self.allergener = {a["code"]: a for a in korpus["allergens"]}
        self.kanter = {}          # emne -> [(post-id, vekt)]
        for sek in ("retter", "drikke"):
            for pid, liste in g[sek].items():
                assert pid in self.retter or pid in self.drikke, pid
                for k in liste:
                    self.kanter.setdefault(k["emne"], []).append((pid, k["vekt"]))
        for e in g.get("emner_uten_kant", []):
            self.kanter.setdefault(e, [])
        self.drikkeemner = set(g.get("drikkeemner", []))
        for e in self.drikkeemner: assert e in self.kanter, e
        self.stedsemner = set(g.get("stedsemner", []))
        for e in self.stedsemner: assert e in self.kanter, e
        self.unntak = {}
        for k, v in g.get("unntak", {}).items():
            self.unntak.setdefault(normalize(k), set()).update(normalize(x) for x in v)
        self.navneord_i_navn = {}   # post-id -> ordene i navnet (til «retten sluker emnet»)
        self.termer = self._termer()

    def _legg(self, L, tekst, node, type_, slag=None):
        ord_, eksakt = les_term(tekst)
        if not ord_ or not ord_[0]: return
        L.append(Term(ord_, eksakt, [node], type_, slag))

    def _termer(self):
        g = self.data["graf"]; L = []
        emnetermer = set()
        for e in self.kanter:
            assert e not in self.allergener
            emnetermer.add(normalize(e))
            self._legg(L, e, "emne:" + e, "emne")
            for o in g.get("ordformer", {}).get(e, []):
                self._legg(L, o, "emne:" + e, "emne")
        for e in g.get("ordformer", {}): assert e in self.kanter, "ordformer for ukjent emne: " + e
        stopp = {normalize(x) for x in g.get("navnestopp", [])}
        def navn(poster, type_):
            teller = {}
            for pid, p in poster.items():
                for t in set(normalize(p["name"]).split()):
                    teller.setdefault(t, set()).add(pid)
            for pid, p in poster.items():
                n = normalize(p["name"]); tok = n.split()
                self.navneord_i_navn[pid] = set(tok)
                self._legg(L, "=" + p["name"], pid, type_)                 # hele navnet
                for t in tok:
                    if t in stopp or t.isdigit() or len(t) < 3: continue
                    if len(teller[t]) > 1: continue                         # ordet står i flere navn
                    if t in emnetermer and len(tok) > 1: continue           # et emne, ikke et navn
                    self._legg(L, t, pid, type_)
                for o in g.get("navneord", {}).get(pid, []):
                    self._legg(L, o, pid, type_)
        navn(self.retter, "rett"); navn(self.drikke, "drikk")
        for pid in g.get("navneord", {}): assert pid in self.retter or pid in self.drikke, pid
        for kode, a in self.allergener.items():
            for del_ in a["name_nb"].split("/"):
                self._legg(L, del_, "allergen:" + kode, "allergen")
            for o in g.get("allergenord", {}).get(kode, []):
                self._legg(L, o, "allergen:" + kode, "allergen")
            for slag, liste in g.get("allergenutsagn", {}).get(kode, {}).items():
                for o in liste:
                    self._legg(L, o, "allergen:" + kode, "allergen", slag)
        for kode in list(g.get("allergenord", {})) + list(g.get("allergenutsagn", {})): assert kode in self.allergener, kode
        # samme ord og samme type: én oppføring med flere noder («frydenlund» er to drikker)
        slaatt = {}; ut = []
        for t in L:
            n = (tuple(t.ord), t.eksakt, t.type, t.slag)
            if n in slaatt:
                for x in t.noder:
                    if x not in slaatt[n].noder: slaatt[n].noder.append(x)
            else:
                slaatt[n] = t; ut.append(t)
        return ut

def last(sti):
    return Graf(json.load(open(sti, encoding="utf-8")), json.load(open(KORPUS, encoding="utf-8")))


def valider(data, korpus=None):
    """Kontrollene Swift-leseren gjør, som ikke alt skjer når Graf bygges: en datafil som går gjennom her,
    skal også gå gjennom `PalazzoHusgraf.init`. Kaster ValueError med første feil."""
    import collections
    korpus = korpus or json.load(open(KORPUS, encoding="utf-8"))
    g = Graf(data, korpus); sp = data["spraak"]; G = data["graf"]
    def moenster(t):
        ut = []
        for del_ in t.split(" "):
            if not del_: continue
            st = del_.endswith("*")
            for bit in normalize(del_[:-1] if st else del_).split(" "):
                if bit: ut.append((bit, st))
        return tuple(ut)
    sett = {}
    KLASSER = {"LIKER", "LIKER_IKKE", "VIL", "SPISER", "SPISER_IKKE", "TAALER", "ALLERGI", "UNNGAAR", "UTEN", "UTELUKK", "SPOER", "HOEFLIG", "MED", "TOM"}
    for klasse in sorted(sp["stikk"]):
        if klasse not in KLASSER: raise ValueError("ukjent stikkordklasse «%s»" % klasse)
        for x in sp["stikk"][klasse]:
            m = moenster(x)
            if not m: raise ValueError("et tomt ord i stikkordene %s" % klasse)
            if m in sett: raise ValueError("stikkordet «%s» står i både %s og %s" % (x, sett[m], klasse))
            sett[m] = klasse
    for navn in ("bord", "aapningstid", "kosthold", "sulten", "torst", "drikkeord", "spiseord", "har_dere", "hus"):
        if navn not in sp["ordlister"]: raise ValueError("ordlisten «%s» mangler" % navn)
    for navn, liste in sp["ordlister"].items():
        for x in liste:
            if not moenster(x): raise ValueError("et tomt ord i ordlisten %s" % navn)
    for x in sp["nektelser"] + sp["engelske_nektelser"]:
        if not moenster(x): raise ValueError("et tomt ord i nektelsene")
    for sek in ("retter", "drikke"):
        for pid, liste in G[sek].items():
            emner = [k["emne"] for k in liste]
            if len(emner) != len(set(emner)): raise ValueError("%s har samme emne to ganger" % pid)
            for k in liste:
                if not (0 < k["vekt"] <= 1): raise ValueError("vekten på kanten %s → %s er ikke mellom 0 og 1" % (k["emne"], pid))
    for kode, u in G["allergenutsagn"].items():
        for slag in u:
            if slag not in ("taaler-ikke", "spiser-ikke"): raise ValueError("allergenutsagn for «%s» har slaget «%s»" % (kode, slag))
    if "svar" in G:
        sv = G["svar"]
        if not (sv["klar_leder"] > 1): raise ValueError("klar_leder må være større enn 1")
        for e in list(sv["alkoholemner"]) + list(sv["fortell"]):
            if e not in g.kanter: raise ValueError("«%s» i svar er ikke et emne i grafen" % e)
        utenalk = {b["id"] for b in g.drikke.values() if not b["category"].startswith("alcoholic")}
        avledet = sorted(e for e in g.drikkeemner if not any(p in utenalk for p, _ in g.kanter[e]))
        if sorted(sv["alkoholemner"]) != avledet: raise ValueError("alkoholemner er %s, men grafen gir %s" % (sorted(sv["alkoholemner"]), avledet))
        alk = {b["id"] for b in g.drikke.values() if b["category"].startswith("alcoholic")}
        for e, k in g.kanter.items():
            if k and all(p in alk for p, _ in k) and e not in sv["alkoholemner"]: raise ValueError("emnet «%s» fører bare til drikke med alkohol og står ikke i alkoholemner" % e)
        for e, tekst in sv["fortell"].items():
            if not tekst.strip(): raise ValueError("fortell for «%s» er tom" % e)
    return True
