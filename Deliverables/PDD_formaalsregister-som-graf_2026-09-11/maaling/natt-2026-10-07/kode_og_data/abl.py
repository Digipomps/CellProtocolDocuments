import sys, eval7 as E, r5
silver = "--silver" in sys.argv
tr=E.train_rows(silver); dv=E.dev_rows(silver)
fn,nodes,tau=E.make_r4_frozen()
def show(name, m, tau=None):
    t = tau if tau is not None else E.choose_tau(m, dv)
    a=E.run(m,tr,t); b=E.run(m,dv,t)
    print(f"{name:34s} tau={t!s:5s} TR {E.fmt(E.summary(a))} | DEV {E.fmt(E.summary(b),E.ci(b))}")
    return b
if __name__=="__main__":
    show("R4 frossen",fn,tau)
    base=dict(lex=False,desc_no=False,acts=False,dekomp=False)
    show("R5 bare",r5.Matcher(flags=base))
    for k in ["norm","stem","split","bm25","fuzzy","qword","scope","hints","signals"]:
        show(f"R5 bare -{k}", r5.Matcher(flags=dict(base,**{k:False})))
