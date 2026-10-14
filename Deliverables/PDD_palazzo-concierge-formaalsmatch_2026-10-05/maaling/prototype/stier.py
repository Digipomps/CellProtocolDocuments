# -*- coding: utf-8 -*-
"""Hvor filene ligger. Alt er relativt til denne mappen (maaling/prototype/ i oppgavemappen) og til HAVEN-roten.
Miljøvariablene HAVEN_ROOT og PALAZZO_MAALING overstyrer, for kjøring et annet sted."""
import os
HER = os.path.dirname(os.path.abspath(__file__))
MAALING = os.environ.get("PALAZZO_MAALING", os.path.dirname(HER))
HAVEN = os.environ.get("HAVEN_ROOT", os.path.abspath(os.path.join(HER, "..", "..", "..", "..", "..")))
KORPUS = os.path.join(HAVEN, "PalazzoScaffold", "Sources", "App", "Resources", "RestaurantConcierge", "palazzo_seed_corpus.json")
SETNINGER = os.path.join(MAALING, "korpus", "korpus-v1.jsonl")
FASIT = os.path.join(MAALING, "fasit", "solvfasit-v1.jsonl")
SETNINGER2 = os.path.join(MAALING, "korpus", "korpus-v2-tillegg.jsonl")
FASIT2 = os.path.join(MAALING, "fasit", "solvfasit-v2-tillegg.jsonl")
KATALOG = os.path.join(MAALING, "tolk", "inn", "katalog.json")
EMNER_V1 = os.path.join(os.path.dirname(MAALING), "graf", "emner-v1.json")
ORDLISTER = os.path.join(MAALING, "ordlister", "ut")
ORDLISTER2 = os.path.join(MAALING, "ordlister2", "ut")
ORDLISTER2_HAAND = os.path.join(MAALING, "ordlister2", "haand")
