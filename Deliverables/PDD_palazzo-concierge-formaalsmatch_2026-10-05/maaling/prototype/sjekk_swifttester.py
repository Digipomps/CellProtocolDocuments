# -*- coding: utf-8 -*-
"""Holder forventningene i Swift-testene (radene i krev([...])) mot prototypen, før de sendes til bygg."""
import re, json, sys
import husgraf, dekomp
data = json.load(open(sys.argv[1], encoding="utf-8"))
g = husgraf.Graf(data, json.load(open(husgraf.KORPUS, encoding="utf-8"))); sp = dekomp.Spraak(data)
kilde = open(sys.argv[2], encoding="utf-8").read()
def avswift(s):
    s = re.sub(r"\\u\{([0-9A-Fa-f]+)\}", lambda m: chr(int(m.group(1), 16)), s)
    return s.replace("\\t", "\t").replace("\\n", "\n").replace('\\"', '"')
feil = 0; n = 0
for m in re.finditer(r'\("((?:[^"\\]|\\.)*)", (\.\w+|nil), \[([^\]]*)\]\)', kilde):
    tekst = avswift(m.group(1)); formaal = None if m.group(2) == "nil" else m.group(2)[1:]
    noder = sorted(re.findall(r'"([^"]+)"', m.group(3)))
    d = dekomp.dekomponer(tekst, g, sp)
    fikk = sorted(("-" if x["slag"] in dekomp.NEGATIVE else "+") + x["node"] for x in d["noder"])
    n += 1
    if d["formaal"] != formaal or fikk != noder:
        feil += 1
        print("AVVIK «%s»: prototypen gir %s %s, testen venter %s %s   %s" % (tekst, d["formaal"], fikk, formaal, noder, d["klasser"]))
print(n, "rader,", feil, "avvik")
