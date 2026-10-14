# -*- coding: utf-8 -*-
"""R5: AI-løs formålsmatcher med brytere, så hver idé kan måles for seg. Ren stdlib.

Byggesteiner (hver kan slås av/på):
  norm     – normalisering: dialekt/nynorsk -> bokmål (generell tabell, skrevet før forseglet sett ble lest), emoji vekk
  stem     – lett norsk stemmer i stedet for 7-tegns avkutting
  split    – sammensatte ord splittes mot registerets vokabular
  bm25     – BM25 i stedet for TF-IDF/cosinus
  fuzzy    – skrivefeil: ukjente ord matches mot vokabular med trigramlikhet
  lex      – erklært leksikon (alias) per formål, med kilde (Fable-tolkning av treningsrader)
  desc_no  – norsk brukerbeskrivelse per formål (Fable, fra treningsrader)
  acts     – samtalehandlinger (hilse/godta/avvise/presenter deg) gjenkjennes på hele ytringen
  dekomp   – setningsdekomponering: handling (verb) og objekt slås opp hver for seg; formål med begge får bonus
  qword    – spørreords-prior, men BARE når uavhengig tekstbevis > 0 (Astras retting)
  scope    – multiplikativt flate-skop (som R4)
"""
from __future__ import annotations
import json, math, re
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
import natt_trening as T
import register_v1 as R
from natt_korpus import FLATE_SKOP

U = "purpose://prompt.unknown"
WORD = re.compile(r"[a-zæøåäöüéè0-9]+")

# Generell dialekt-/nynorsk-/andrespråkstabell. Skrevet fra allmenn kunnskap om norsk, ikke fra korpuset.
NORM = {
    "ikkje": "ikke", "itj": "ikke", "ikkj": "ikke", "kje": "ikke", "ente": "ikke", "ikk": "ikke",
    "kva": "hva", "ka": "hva", "kå": "hva", "hå": "hva", "va": "hva", "kvifor": "hvorfor", "kvifo": "hvorfor", "korfor": "hvorfor",
    "kofor": "hvorfor", "korleis": "hvordan", "kossen": "hvordan", "koss": "hvordan", "kordan": "hvordan", "åssen": "hvordan",
    "åsså": "hvordan", "kor": "hvor", "kvar": "hvor", "kem": "hvem", "kven": "hvem", "kæm": "hvem", "kåffer": "hvorfor",
    "kvifor": "hvorfor", "når": "når", "eg": "jeg", "e": "jeg", "æ": "jeg", "je": "jeg", "mæ": "meg", "meg": "meg", "me": "vi",
    "dokker": "dere", "dykk": "dere", "dokke": "dere", "dåkk": "dere", "ikkje": "ikke", "berre": "bare", "bærre": "bare",
    "noko": "noe", "nokon": "noen", "nåke": "noe", "nokre": "noen", "mykje": "mye", "mykkje": "mye", "kunne": "kunne",
    "heile": "hele", "alle": "alle", "korleis": "hvordan", "vere": "være", "vera": "være", "kome": "komme", "kjem": "kommer",
    "seie": "si", "seier": "sier", "eigen": "egen", "eigne": "egne", "eige": "eie", "eigar": "eier", "spørsmål": "spørsmål",
    "spurnad": "spørsmål", "skjema": "skjema", "lagra": "lagre", "lagrar": "lagrer", "sletta": "slette", "slettar": "sletter",
    "sende": "sende", "sendar": "sender", "ville": "ville", "vil": "vil", "treng": "trenger", "trenge": "trenge",
    "pls": "", "plz": "", "pliis": "", "takk": "takk", "tusen": "tusen", "lol": "", "idk": "vet ikke", "mtp": "med tanke på",
    "dkk": "dere", "dere": "dere", "hvor": "hvor", "ka": "hva", "kordan": "hvordan", "ka for": "hvilken",
    "mine": "mine", "mitt": "mitt", "dataa": "dataene", "data'n": "dataene", "frå": "fra", "fra": "fra", "fram": "frem",
    "framleis": "fortsatt", "enno": "ennå", "endå": "ennå", "veit": "vet", "vett": "vet", "trur": "tror", "skjønar": "skjønner",
}

STOP = set(("og i på til av for med en et ei det er som at kan du jeg vi de den dette om ikke skal vil har hva hvor hvem "
            "hvordan hvorfor når mine min mitt meg seg the a an of to in on for and or is are be it this that with my me you "
            "your så bare litt noe noen da nå var være blir ble få gjøre gjør hei please pls er det dere oss vår våre sin sitt "
            "sine også men eller hvis fra ut opp inn over etter før enn alle hele").split())

SUFFIX = ["ene", "ane", "ene", "ers", "ens", "ets", "het", "ing", "inga", "ingar", "inger", "ingen", "else", "elser", "elsen",
          "ende", "erte", "ert", "ere", "er", "en", "et", "ar", "ne", "te", "de", "a", "e", "s"]
SUFFIX = sorted(set(SUFFIX), key=len, reverse=True)


def stem(w):
    if len(w) <= 4: return w
    for s in SUFFIX:
        if w.endswith(s) and len(w) - len(s) >= 4:
            return w[:-len(s)]
    return w


def trigrams(w):
    w = f"#{w}#"; return {w[i:i + 3] for i in range(len(w) - 2)}


class Matcher:
    def __init__(self, flags=None, lexicon=None, desc_no=None, acts=None, verbs=None, overlays=(), nodes=None, bg=None, bg_w=0.3,
                 frames=None, dk_both=0.8, dk_one=0.15, cov_alpha=0.0):
        self.f = dict(norm=True, stem=True, split=True, bm25=False, frames=True, fuzzy=True, lex=True, desc_no=True, acts=True,
                      dekomp=True, qword=True, scope=True, hints=True, signals=True)
        self.f.update(flags or {})
        self.nodes = nodes or R.load_register(overlays)
        self.ch = T.children_map(self.nodes)
        self.lexicon = lexicon or {}      # ref -> [fraser]
        self.desc_no = desc_no or {}      # ref -> norsk beskrivelse
        self.acts = acts or {}            # ref -> [hele ytringer / startfraser]
        self.verbs = verbs or {}          # verb-lemma -> {ref: vekt}
        self.frames = frames or {}        # ref -> {"handlinger": set(stem), "objekter": set(stem)}  (verb -> formål, objekt -> formål)
        self.dk_both, self.dk_one = dk_both, dk_one
        self.cov_alpha = cov_alpha   # dekning: andel av meldingens innholdsord registeret kjenner, opphøyd i alpha
        self.bg = bg or set(); self.bg_w = bg_w  # bakgrunnsord (fra treningsnegativer): vektes ned
        self.cands = [r for r, n in self.nodes.items() if not n["facetOnly"] and r not in (U, "purpose://root")
                      and not r.startswith("purpose://conversation")]   # samtalehandlinger bare via act()
        self._build()

    # ------------------------------------------------ tekst
    def words(self, text):
        t = text.lower().replace("’", "'")
        ws = WORD.findall(t)
        if self.f["norm"]:
            out = []
            for w in ws:
                m = NORM.get(w, w)
                out += m.split() if m else []
            ws = out
        return ws

    def toks(self, text, for_doc=False):
        out = []
        for w in self.words(text):
            if w in STOP or len(w) < 2: continue
            parts = [w]
            if self.f["split"] and not for_doc and len(w) >= 8 and w not in self.vocab_raw:
                parts = self._split(w) or [w]
            for p in parts:
                s = stem(p) if self.f["stem"] else (p[:7] if len(p) > 7 else p)
                if not self.f["stem"] and len(p) >= 6: out.append("~" + p[:5])
                out.append(s)
        return out

    def _split(self, w):
        # grådig to-delt splitt mot registerets vokabular (rå ord), med fuge-s/e
        best = None
        for i in range(3, len(w) - 2):
            a, b = w[:i], w[i:]
            for aa in (a, a[:-1] if a.endswith(("s", "e")) else None):
                if aa and len(aa) >= 3 and aa in self.vocab_raw and (b in self.vocab_raw or stem(b) in self.vocab_stem):
                    cand = [aa, b]
                    if best is None or len(aa) > len(best[0]): best = cand
        return best

    def node_doc(self, r):
        n = self.nodes[r]
        parts = [n["title"], n["desc"]]
        if self.f["hints"]: parts += n["aliases"] + n["tokens"]
        if self.f["signals"]: parts += n["signals"] + [n["outcome"]]
        if self.f["lex"]: parts += self.lexicon.get(r, [])
        if self.f["desc_no"] and self.desc_no.get(r): parts.append(self.desc_no[r])
        return " ".join(p for p in parts if p)

    def _build(self):
        self.vocab_raw = set()
        for r in self.cands:
            for w in WORD.findall(self.node_doc(r).lower()): self.vocab_raw.add(w)
        self.vocab_stem = {stem(w) for w in self.vocab_raw}
        self.tf = {r: Counter(self.toks(self.node_doc(r), for_doc=True)) for r in self.cands}
        df = Counter()
        for c in self.tf.values(): df.update(c.keys())
        self.N = len(self.cands); self.df = df
        self.avgdl = sum(sum(c.values()) for c in self.tf.values()) / max(1, self.N)
        self.idf = {w: math.log((self.N - d + 0.5) / (d + 0.5) + 1) * (self.bg_w if w in self.bg else 1.0) for w, d in df.items()}
        self.vocab_tok = set(df)
        self.tri = defaultdict(set)
        for w in self.vocab_tok:
            if len(w) >= 4:
                for g in trigrams(w): self.tri[g].add(w)
        # tf-idf-vektorer (når bm25 er av)
        self.vec = {}
        for r, c in self.tf.items():
            v = {w: (1 + math.log(f)) * self.idf[w] for w, f in c.items()}
            nrm = math.sqrt(sum(x * x for x in v.values())) or 1.0
            self.vec[r] = {w: x / nrm for w, x in v.items()}
        # fraseindeks for alias/leksikon
        self.phrases = []
        for r in self.cands:
            n = self.nodes[r]
            ph = (n["aliases"] if self.f["hints"] else []) + (self.lexicon.get(r, []) if self.f["lex"] else [])
            for a in ph:
                a2 = " ".join(self.words(a))
                if len(a2) < 3: continue
                st = tuple(stem(w) for w in a2.split() if w not in STOP)
                self.phrases.append((r, a2, st if len(st) >= 2 else None))

    def _fuzzy(self, w):
        if w in self.vocab_tok or len(w) < 4: return w
        g = trigrams(w); cnt = Counter()
        for x in g:
            for v in self.tri.get(x, ()): cnt[v] += 1
        best, bs = None, 0.0
        for v, c in cnt.items():
            j = c / (len(g) + len(trigrams(v)) - c)
            if j > bs: best, bs = v, j
        return best if bs >= 0.5 else w

    def coverage(self, text):
        q = self.qtoks(text)
        if not q: return 0.0
        return sum(1 for w in q if w in self.vocab_tok) / len(q)

    def qtoks(self, text):
        ts = self.toks(text)
        if self.f["fuzzy"]: ts = [self._fuzzy(w) for w in ts]
        return ts

    # ------------------------------------------------ scoring
    def text_score(self, text):
        q = Counter(self.qtoks(text))
        if not q: return {}
        sc = {}
        if self.f["bm25"]:
            k1, b = 1.2, 0.75
            for r, c in self.tf.items():
                dl = sum(c.values()); s = 0.0
                for w, qf in q.items():
                    f = c.get(w, 0)
                    if f: s += self.idf[w] * f * (k1 + 1) / (f + k1 * (1 - b + b * dl / self.avgdl))
                if s > 0: sc[r] = s
            # normaliser til ~[0,1] med maks mulig for spørringen
            invoc = [w for w in q if w in self.idf]
            mx = (sum(self.idf[w] * (k1 + 1) for w in invoc) * (len(invoc) / len(q)) ** 0.5 / max(1, len(invoc)) ** 0.5) or 1.0
            sc = {r: s / mx for r, s in sc.items()}
        else:
            qv = {w: (1 + math.log(f)) * self.idf.get(w, 0.0) for w, f in q.items()}
            nrm = math.sqrt(sum(x * x for x in qv.values())) or 1.0
            for r, v in self.vec.items():
                s = sum(qv[w] / nrm * v.get(w, 0.0) for w in qv)
                if s > 0: sc[r] = s
        low = " " + " ".join(self.words(text)) + " "
        S = None
        if self.f.get("phrase_stem", True):
            st = [stem(w) for w in self.words(text) if w not in STOP]
            if self.f["fuzzy"]: st = [x if x in self.vocab_tok else self._fuzzy(x) for x in st]
            S = " " + " ".join(st) + " "
        bonus = self.f.get("phrase_bonus", 0.5)
        got = {}
        for r, a, st in self.phrases:
            if f" {a} " in low or (len(a) >= 6 and a in low): got[r] = max(got.get(r, 0), bonus)
            elif S and st and f" {' '.join(st)} " in S: got[r] = max(got.get(r, 0), bonus * self.f.get("stem_phrase_w", 0.7))
        for r, b in got.items(): sc[r] = sc.get(r, 0.0) + b
        return sc

    def act(self, text):
        """Samtalehandling bare når HELE ytringen er handlingen (eller en hilsen åpner en kort ytring)."""
        if not self.f["acts"]: return None
        low = " ".join(self.words(text)).strip()
        if not low: return None
        ntok = len(low.split())
        if self.f.get("yesno", True) and ntok <= 5:
            first = low.split()[0]
            if first in ("nei", "nope", "nah", "no", "neida", "niks") and "purpose://conversation.reject" in self.acts:
                return "purpose://conversation.reject"
            if first in ("ja", "jo", "jepp", "yes", "ok", "okei", "okay", "greit", "jada") and "purpose://conversation.accept" in self.acts:
                return "purpose://conversation.accept"
        best = None
        for r, pats in self.acts.items():
            for p in pats:
                p2 = " ".join(self.words(p))
                if not p2: continue
                ok = low == p2
                if not ok and r.endswith(".open") and ntok <= 6 and low.startswith(p2 + " "): ok = True
                if not ok and ntok <= 4 and low.startswith(p2 + " ") and len(p2.split()) >= 2: ok = True
                if ok and (best is None or len(p2) > best[1]): best = (r, len(p2))
        return best[0] if best else None

    def dekomp(self, text, sc):
        """Verb -> formål, objekt -> formål, to oppslag. Formål som får støtte fra både handling og objekt løftes."""
        if not self.f["dekomp"] or not self.verbs: return sc
        ws = self.words(text)
        vhit = Counter()
        for i, w in enumerate(ws):
            for form in (w, stem(w)):
                if form in self.verbs:
                    for r, wt in self.verbs[form].items(): vhit[r] = max(vhit[r], wt)
        if not vhit: return sc
        out = dict(sc)
        for r, wt in vhit.items():
            if r in out and out[r] > 0:
                out[r] = out[r] * (1 + 0.6 * wt)      # handling bekrefter objektets formål
        return out

    def frame(self, text, sc):
        """Kjetils regel «verbet gir formålet, argumentene slås opp for seg»: handling og objekt slås opp hver for seg
        mot formålets erklærte handlinger/objekter. Begge treffer -> sterkt løft; bare én -> lite. Skaper aldri score
        alene for et formål uten tekstbevis, med mindre begge treffer (da ER det tekstbevis)."""
        if not self.f["frames"] or not self.frames: return sc
        st = [stem(w) for w in self.words(text)]
        st = st + ([self._fuzzy(w) for w in st] if self.f["fuzzy"] else [])
        sset = set(st)
        out = dict(sc)
        for r, fr in self.frames.items():
            if r not in self.cands: continue
            hv = bool(fr["handlinger"] & sset); ho = bool(fr["objekter"] & sset)
            if hv and ho: out[r] = out.get(r, 0.0) * (1 + self.dk_both) + 0.15
            elif (hv or ho) and out.get(r, 0) > 0: out[r] = out[r] * (1 + self.dk_one)
        return out

    def qword(self, text, sc):
        if not self.f["qword"]: return sc
        if not any(s > 0 for s in sc.values()): return sc    # aldri bevis av spørreord alene
        pri = T.qword_prior_specific(" ".join(self.words(text)))
        out = dict(sc)
        for r, v in pri.items():
            if r in out and out[r] > 0: out[r] += v
        return out

    def scope(self, flate, text, sc):
        if not self.f["scope"]: return sc
        inscope = T.subtree(self.nodes, FLATE_SKOP.get(flate, []), self.ch)
        inscope |= {r for r in self.nodes if r.startswith("purpose://conversation")}
        ntok = len(self.toks(text)); w = 1.0 - min(1.0, ntok / 6.0)
        return {r: (s * (1 + w * 3.0) if r in inscope else s) for r, s in sc.items()}

    CLAUSE = re.compile(r"[.;!?:\n]+|,\s|\s(?:og|men|så|fordi|for|siden|slik at|sånn at|ettersom|but|and|because)\s", re.I)

    def __call__(self, flate, text):
        a = self.act(text)
        if a: return [(a, 1.0)]
        if self.f.get("clauses"):
            parts = [p.strip() for p in self.CLAUSE.split(text) if p and len(self.toks(p)) >= 1]
            if len(parts) > 1:
                best = {}
                for p in parts + [text]:
                    for r, s in self._one(flate, p):
                        if s > best.get(r, 0): best[r] = s
                if self.f.get("clauses") == "rank":
                    whole = dict(self._one(flate, text))
                    order = sorted(best.items(), key=lambda x: (-x[1], x[0]))
                    return [(r, whole.get(r, 0.0)) for r, _ in order if whole.get(r, 0.0) > 0]
                return sorted(best.items(), key=lambda x: (-x[1], x[0]))
        return self._one(flate, text)

    def _one(self, flate, text):
        sc = self.text_score(text)
        sc = self.dekomp(text, sc)
        sc = self.frame(text, sc)
        sc = self.qword(text, sc)
        if self.f.get("scope_rank_only", True):
            # skop rangerer, men terskelen gjelder tekstbeviset: rapportert score = tekstscore for vinneren
            sc2 = self.scope(flate, text, sc)
            items = [(r, s) for r, s in sc2.items() if s > 0 and r in self.cands]
            items.sort(key=lambda x: (-x[1], x[0]))
            cov = self.coverage(text) ** self.cov_alpha if self.cov_alpha else 1.0
            return [(r, sc[r] * cov) for r, _ in items]
        sc = self.scope(flate, text, sc)
        items = [(r, s) for r, s in sc.items() if s > 0 and not self.nodes[r]["facetOnly"] and r in self.cands]
        return sorted(items, key=lambda x: (-x[1], x[0]))
