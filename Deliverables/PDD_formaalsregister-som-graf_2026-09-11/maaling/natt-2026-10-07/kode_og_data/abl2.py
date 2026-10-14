import json, sys, eval7 as E, r5, utled
from abl import show
tr=E.train_rows(True); dv=E.dev_rows(True)
def mk(ms=2, mp=0.6, ml=4, **flags):
    lex, verbs, acts, bg = utled.derive(ms, mp, ml)
    L={r:[x['frase'] for x in v] for r,v in lex.items()}
    return r5.Matcher(flags=dict(desc_no=False, **flags), lexicon=L, verbs=verbs, acts=acts), (lex,verbs,acts,bg)
if __name__=="__main__":
    fn,nodes,tau=E.make_r4_frozen()
    show("R4 frossen", fn, tau); show("R4 tau@FA10", fn)
    show("R5 bare", r5.Matcher(flags=dict(lex=False,desc_no=False,acts=False,dekomp=False)))
    for ms in (1,2):
        for mp in (0.5,0.7,0.9):
            m,_=mk(ms,mp); show(f"R5 lex ms{ms} mp{mp} +acts+dekomp", m)
    m,_=mk(1,0.7,dekomp=False); show("ms1 mp.7 -dekomp", m)
    m,_=mk(1,0.7,acts=False); show("ms1 mp.7 -acts", m)
    m,_=mk(1,0.7,lex=False); show("ms1 mp.7 -lex", m)
