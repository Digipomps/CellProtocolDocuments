import sys, eval7 as E, r5, utled, curve, fablelex
dv=E.dev_rows(True)
def C(name, m, rows=dv):
    c=curve.curve(m,rows); print(f"{name:52s} top1@FA0/5/10/15 = " + " / ".join(f"{v:.3f}" for v in c.values()), flush=True); return c
KW = ("cov_alpha", "dk_both", "dk_one", "bg", "bg_w")
def build(desc=True, uttr=True, frames=True, acts_f=True, lexT=False, verbsT=False, d='beskr_ut', **flags):
    kw = {k: flags.pop(k) for k in list(flags) if k in KW}
    D,L,F,rows=fablelex.load(d=d)
    lex={}
    if uttr:
        for r,v in L.items():
            if not r.startswith("purpose://conversation"): lex.setdefault(r,[]).extend(v)
    acts={r:v for r,v in L.items() if r.startswith("purpose://conversation")} if acts_f else {}
    verbs={}
    if lexT or verbsT:
        l2,v2,a2,bg=utled.derive(1,0.7,4)
        if lexT:
            for r,v in l2.items():
                if not r.startswith("purpose://conversation"): lex.setdefault(r,[]).extend(x['frase'] for x in v)
        if verbsT: verbs=v2
    return r5.Matcher(flags=dict(dict(desc_no=desc, frames=frames, dekomp=bool(verbs), lex=bool(lex), acts=bool(acts)), **flags),
                      lexicon=lex, desc_no=D if desc else {}, frames=F if frames else {}, acts=acts, verbs=verbs, **kw)
if __name__=="__main__":
    fn,_,_=E.make_r4_frozen(); C("R4 frossen", fn)
    C("R5 bare", r5.Matcher(flags=dict(lex=False,desc_no=False,acts=False,dekomp=False,frames=False)))
    C("F: desc+uttrykk+frames+acts", build())
    C("F: -desc", build(desc=False)); C("F: -uttrykk", build(uttr=False)); C("F: -frames", build(frames=False)); C("F: -acts", build(acts_f=False))
    C("F + treningsfraser (Fable bærende ord)", build(lexT=True))
    C("F + treningsverb (dekomp v1)", build(verbsT=True))
    for k in ["norm","stem","split","fuzzy","qword","scope","hints","signals","scope_rank_only"]:
        C(f"F: -{k}", build(**{k:False}))
