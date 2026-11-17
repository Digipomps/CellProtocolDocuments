# -*- coding: utf-8 -*-
"""Butlers treffregel, portet linje for linje fra
CellScaffold/_wt-butler-e1-20260929/Sources/App/Support/ButlerSignalMatcher.swift (normalize,
termMatchesToken, isNegated, containsWholeMarker). Dette er en prototype i Python for å kunne
måle raskt mot sølvfasiten. Tallene som rapporteres, kommer fra Swift-koden, ikke herfra."""
import unicodedata

def normalize(text):
    mapped = text.lower()
    for a, b in (("ø", "o"), ("æ", "ae"), ("å", "a"), ("ö", "o"), ("ä", "a"), ("ü", "u")):
        mapped = mapped.replace(a, b)
    # .diacriticInsensitive: fjern kombinerende tegn etter dekomponering
    folded = "".join(c for c in unicodedata.normalize("NFD", mapped) if unicodedata.category(c) != "Mn").lower()
    out = []; last_space = True
    for ch in folded:
        if ch.isalpha() or ch.isnumeric():
            out.append(ch); last_space = False
        elif not last_space:
            out.append(" "); last_space = True
    return "".join(out).strip()

def tokens(text):
    return normalize(text).split(" ") if normalize(text) else []

def term_matches_token(term, token, allow_compound=True):
    if token == term:
        return True
    allowed_tail = 7 if len(term) >= 5 else 3
    if len(term) >= 3 and token.startswith(term) and len(token) <= len(term) + allowed_tail:
        return True
    if allow_compound and len(term) >= 5 and term in token:
        return True
    return False

NEGATION_MARKERS = ["ikke", "ikkje", "ingen", "inga", "aldri", "slutt a", "slutte a", "uten a", "trenger ikke",
                    "trengs ikke", "ikke behov", "bare til info", "til info", "fyi", "do not", "dont", "no need",
                    "already", "allerede"]

def contains_whole_marker(haystack, marker):
    return bool(marker) and (" %s " % marker) in (" %s " % haystack)

def is_negated(index, normalized, window=34):
    if index <= 0:
        return False
    lower = max(0, index - window)
    if lower > 0:
        while lower < index and normalized[lower] != " ":
            lower += 1
    if lower >= index:
        return False
    prefix = normalized[lower:index]
    return any(contains_whole_marker(prefix, m) for m in NEGATION_MARKERS)

if __name__ == "__main__":
    assert normalize("Møte på Café?") == "mote pa cafe"
    assert normalize("  ÆØÅ, æøå!  ") == "aeoa aeoa"
    assert normalize("work-item #42") == "work item 42"
    assert term_matches_token("analyse", "analysere") and term_matches_token("ide", "ideene") and not term_matches_token("ide", "identitet")
    assert term_matches_token("ost", "osters") and term_matches_token("lok", "lokale")
    print("ok")
