# Leser Fables erklæringskandidater (beskr_ut/*.json) til matcherens format.
import json
from pathlib import Path
import r5
HERE=Path(__file__).resolve().parent
def load(include=("desc","uttrykk","frames","qord"), d="beskr_ut"):
    rows=[]
    for f in sorted((HERE/d).glob("*.json")): rows+=json.load(open(f))
    desc={}; lex={}; frames={}
    m=r5.Matcher(flags=dict(lex=False,desc_no=False,acts=False,dekomp=False,frames=False))
    for r in rows:
        if r.get('usikker'): continue
        ref=r['ref']
        if "desc" in include: desc[ref]=r.get('beskrivelse_no','')
        if "uttrykk" in include: lex[ref]=list(r.get('uttrykk') or [])
        if "frames" in include:
            hv={r5.stem(w) for v in r.get('handlinger') or [] for w in m.words(v) if w not in r5.STOP}
            ob={r5.stem(w) for v in r.get('objekter') or [] for w in m.words(v) if w not in r5.STOP}
            frames[ref]={"handlinger":hv,"objekter":ob}
    return desc, lex, frames, rows
