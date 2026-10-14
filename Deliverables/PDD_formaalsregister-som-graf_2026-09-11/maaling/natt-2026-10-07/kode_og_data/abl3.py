import eval7 as E, r5, utled, curve
dv=E.dev_rows(True); tr=E.train_rows(True)
def C(name, m):
    c=curve.curve(m,dv); print(f"{name:40s} DEV top1@FA0/5/10/15 = " + " / ".join(f"{v:.3f}" for v in c.values()))
fn,_,_=E.make_r4_frozen(); C("R4 frossen", fn)
lex,verbs,acts,bg=utled.derive(1,0.7,4); L={r:[x['frase'] for x in v] for r,v in lex.items()}
for bm in (True, False):
  for sro in (True, False):
    C(f"R5 bare bm25={bm} skopRangOnly={sro}", r5.Matcher(flags=dict(lex=False,desc_no=False,acts=False,dekomp=False,bm25=bm,scope_rank_only=sro)))
    C(f"R5 lex bm25={bm} skopRangOnly={sro}", r5.Matcher(flags=dict(desc_no=False,bm25=bm,scope_rank_only=sro),lexicon=L,verbs=verbs,acts=acts))
