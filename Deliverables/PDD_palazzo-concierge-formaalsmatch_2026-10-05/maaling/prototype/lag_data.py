# -*- coding: utf-8 -*-
"""Bygger datafilen for husets graf og conciergens språk (utkast). Emnene og kantene er dem i graf/emner-v1.json.
Ordformene her er skrevet for hånd; hvilke treningsrader hver oppføring retter, regnes av endringslogg.py."""
import json, sys, os
# GRUNN=3 tar med rettelsene som kom etter versjon .2 (se graf/ENDRINGSLOGG.md). Uten den bygges .2 som før.
GRUNN = int(os.environ.get("GRUNN", "2"))
UTEN = set(x for x in os.environ.get("UTEN", "").split(",") if x)   # rettelser som holdes utenfor i en prøve
def med(navn): return GRUNN >= 3 and navn not in UTEN
import stier
e1 = json.load(open(stier.EMNER_V1, encoding="utf-8"))

formaal = [
 {"id": "spise", "maal": "Retten er servert til gjesten"},
 {"id": "drikke", "maal": "Drikken er servert til gjesten"},
 {"id": "vite", "maal": "Gjesten har fått svaret fra husets data"},
 {"id": "unngaa", "maal": "Gjesten har fått merkingen og beskrivelsen for det hun spør om, og er vist til personalet"},
 {"id": "bord", "maal": "Gjesten har fått vite hvordan hun bestiller bord"},
 {"id": "aapningstid", "maal": "Gjesten har fått åpningstiden, eller beskjed om at den må bekreftes"},
]

ordformer = {
 "alkoholfri vin": ["alkoholfrie viner", "vin uten alkohol"],
 "alkoholfritt": ["alkoholfri", "alkoholfrie", "uten alkohol", "utan alkohol", "alcohol free", "non alcoholic", "nonalcoholic", "alkoholfreie", "alkoholfrei"],
 "alkoholfritt øl": ["alkoholfri øl", "øl uten alkohol", "alcohol free beer", "non alcoholic beer"],
 "ansjos": ["anchovy", "anchovies", "sardeller", "acciughe"],
 "arancini": ["arancino", "arancina", "riskrokett", "risbolle", "risball", "rice ball", "rice balls"],
 "asparges": ["asparagus", "sparris"],
 "aubergine": ["eggplant", "melanzane"],
 "basilikum": ["basil", "basilico"],
 "blekksprut": ["octopus"],
 "brissel": ["kalvebrissel", "sweetbread"],
 "brus": ["soda", "soft drink", "leskedrikk", "läsk", "sodavand"],
 "brød": ["bread", "landbrød"],
 "chili": ["chilli", "chile", "peperoncino"],
 "dessert": ["desert", "etterrett", "noe søtt", "noko søtt", "något sött", "something sweet", "dolce", "dolci", "efterrätt"],
 "eple": ["apple", "äpple", "æble"],
 "eplemost": ["eplesaft", "äppelmust"],
 "erter": ["ert", "peas", "ärtor"],
 "fava": ["bondebønner", "hestebønner", "broad beans"],
 "fisk": ["fish", "fesk", "fisch", "pesce", "fiskerett"],
 "forrett": ["starter", "antipasti", "antipasto", "appetizer", "appetiser", "förrätt"],
 "fritert": ["friterte", "frityrstekt", "deep fried"],
 "grønnsaker": ["grønnsak", "grønt", "grønsaker", "vegetable", "veggies", "grönsaker", "verdure"],
 "gulrot": ["gulrøtter", "carrot", "morot"],
 "havbrasme": ["sea bream", "seabream", "dorade", "brasme"],
 "hovedrett": ["hovudrett", "main course", "mains", "secondi", "secondo", "varmrett", "huvudrätt"],
 "hvitløk": ["kvitlauk", "garlic", "hvidløg", "vitlök", "aglio", "knoblauch"],
 "hvitvin": ["kvitvin", "white wine", "vitt vin", "vino bianco"],
 "italia": ["italiensk", "italienske", "italian", "italy", "italiano"],
 "kake": ["cake", "tårta", "kage"],
 "kalv": ["kalvekjøtt", "veal"],
 "kapers": ["capers", "capperi"],
 "karamell": ["caramel", "karamellisert"],
 "kjøtt": ["kjøt", "meat", "kött", "kød", "fleisch", "carne", "kjøttrett"],
 "krem": ["kräm"],
 "lam": ["lammekjøtt", "lammerett", "lamb", "lamm", "lammecarré", "lammenakke"],
 "linser": ["linse", "lentil", "lentils"],
 "løk": ["lauk", "onion", "lök", "løg", "zwiebel"],
 "majones": ["mayo", "mayonnaise", "majonnäs"],
 "mandler": ["mandel", "mandlene", "almond", "mandorle", "mandeln"],
 "mineralvann": ["sparkling water", "farris", "kullsyrevann", "vann med kullsyre"],
 "mocktail": ["alkoholfri drink", "alkoholfri cocktail"],
 "mozzarella": ["mozarella", "mozzarela"],
 "mynte": ["mint", "menta"],
 "okse": ["oksekjøtt", "biff", "storfe", "beef", "nötkött"],
 "oliven": ["olive", "olives", "oliver"],
 "olivenolje": ["olive oil"],
 "ost": ["cheese", "formaggio", "käse"],
 "ostekake": ["cheesecake", "cheese cake"],
 "pasta": ["pastarett"],
 "pistasj": ["pistasi", "pistachio", "pistacchio", "pistacchi", "pistasch", "pistazie"],
 "pizza": ["pizze"],
 "potet": ["potato", "potatis", "kartoffel"],
 "ragu": ["kjøttsaus"],
 "ris": ["rice", "riso"],
 "rødvin": ["raudvin", "red wine", "rött vin", "rotwein", "vino rosso", "a red"],
 "safran": ["saffron", "zafferano"],
 "salat": ["salad", "sallad", "insalata"],
 "salvie": ["=sage", "salvia"],
 "selleri": ["stangselleri", "celery", "sedano", "sellerie"],
 "sicilia": ["siciliansk", "sisiliansk", "sicilian", "sicily"],
 "sitron": ["lemon", "citron", "zitrone"],
 "sjømat": ["seafood", "frutti di mare", "fra havet"],
 "skjell": ["=skjel", "=skjela", "musling", "clam", "teppeskjell", "teppekjell"],
 "sorbet": ["sorbetto"],
 "sterk": ["sterkt", "sterke", "spicy", "=hot", "piccante", "piccant", "krydret", "scharf"],
 "tomat": ["tomato", "pomodoro"],
 "trøffel": ["truffle", "tryffel"],
 "tunfisk": ["tuna", "tonno", "thunfisch"],
 "urter": ["urt", "herbs", "krydderurter"],
 "vann": ["vatn", "water", "vatten", "acqua"],
 "vedfyrt": ["vedovn", "vedfyrt ovn", "wood fired", "wood oven", "steinovn"],
 "vin": ["viner", "wine", "wines", "vino", "wein", "hvitvin", "kvitvin", "rødvin", "raudvin", "rosévin", "white wine", "red wine", "vino bianco", "vino rosso", "rotwein", "rött vin", "vitt vin", "alkoholfri vin"],
 "øl": ["=ølet", "=øla", "=ølen", "=ølene", "pils", "pilsner", "halvliter", "beer", "bier", "birra"],
 "østers": ["oyster", "ostron"],
}

navneord = {
 "menu-carpaccio-polpo": ["blekksprutcarpaccio", "blekksprut carpaccio", "octopus carpaccio"],
 "menu-orata-forno": ["al forno a legna", "forno a legna"],
 "menu-crema-limone": ["sitronkrem", "citronkräm", "lemon cream"],
 "menu-pizza-margherita": ["margarita", "margerita", "margarhita"],
 "menu-pizza-siciliana": ["siciliana"],
 "menu-pizza-vulcano": ["vulkano"],
 "bev-frydenlund-05": ["frydenlund"],
 "bev-frydenlund-025": ["frydenlund"],
 "bev-italian-soda": ["italian soda", "italian sodas"],
 "bev-dagens-mocktail": ["mocktail of the day"],
 "bev-alkoholfri-vin": ["alcohol free wine", "non alcoholic wine"],
}

navnestopp = ["di", "e", "al", "a", "con", "la", "il", "alla", "del", "della", "olio", "salsa", "forno", "legna", "arrosto", "vino", "rosso",
              "bresato", "free", "max", "dagens", "italian", "sodas", "glutenfri", "pistacchio", "pistacchi", "alkoholfri", "vin"]

allergenord = {
 "HV": ["kveitemjøl", "kveitemel", "wheat", "hvetemel", "hvetemjøl", "=mel", "=melet", "flour", "glutin", "glutten", "weizen", "vetemjöl", "=vete"],
 "M": ["mjølk", "milk", "laktose", "lactose", "melkeprotein", "meieriprodukt", "dairy", "mjölk", "mælk", "milch"],
 "E": ["ägg", "=æg", "eggs"],
 "PE": ["peanøtt", "peanut", "jordnøtt", "erdnuss", "jordnötter"],
 "N": ["nøtt", "=nut", "=nuts", "tree nut", "tree nuts", "trenøtter", "nötter", "nødder", "nüsse", "=nuss", "hasselnøtt", "valnøtt"],
 "S": ["soja", "=soy", "soia"],
 "F": ["fish", "fesk", "fisch"],
 "SK": ["skaldyr", "shellfish", "krepsdyr", "skaldjur", "crustacean"],
 "BL": ["mollusk", "mollusc", "blötdjur"],
 "SE": ["celery", "stangselleri", "sellerie"],
 "SN": ["mustard", "senap", "senf"],
 "SF": ["sesam", "sesame"],
 "L": ["lupiner"],
 "SU": ["sulfitter", "sulfites", "sulphites", "sulfite", "sulfit", "sulphite"],
}
# ord som i seg selv sier at noe ikke tåles eller ikke spises
allergenutsagn = {
 "HV": {"taaler-ikke": ["cøliaki", "cøliaker", "celiaki", "celiac", "coeliac", "zöliakie"],
        "spiser-ikke": ["glutenfri", "glutenfritt", "glutenfrie", "gluten free", "glutenfrei", "glutenfria"]},
 "M": {"spiser-ikke": ["laktosefri", "laktosefritt", "laktosefrie", "melkefri", "melkefritt", "dairy free", "lactose free"]},
 "N": {"spiser-ikke": ["nøttefri", "nøttefritt", "nut free"]},
 "E": {"spiser-ikke": ["eggfri", "eggfritt", "egg free"]},
}

unntak = {
 "ris": ["ristet", "riste", "rista", "risiko", "risk"],
 "løk": ["lokal"],
 "lam": ["lampe"],
 "erter": ["desserter"],
 "vin": ["vinter", "vindu", "vinn", "vinge"],
 "kake": ["kaker"] and [],
}
unntak = {k: v for k, v in unntak.items() if v}

drikkeemner = ["alkoholfri vin", "alkoholfritt", "alkoholfritt øl", "brus", "eplemost", "juice", "mineralvann", "mocktail", "vann", "vin", "hvitvin", "rødvin", "øl"]

graf = {
 "terskel": 0.05,
 "formaal": formaal,
 "retter": e1["retter"], "drikke": e1["drikke"],
 "emner_uten_kant": ["vin"],
 "drikkeemner": drikkeemner,
 "stedsemner": ["italia", "sicilia", "bronte", "modica"],
 "ordformer": ordformer, "navneord": navneord, "navnestopp": navnestopp,
 "allergenord": allergenord, "allergenutsagn": allergenutsagn, "unntak": unntak,
}

stikk = {
 "LIKER": ["liker", "likar", "likte", "elsk*", "digger", "diggar", "foretrekker", "føretrekkjer", "glad i", "gla i", "glade i", "fan av", "svak for", "svakhet for",
           "sans for", "begeistret for", "setter pris på", "set pris på", "setter stor pris på", "love", "loves", "loved", "adore", "enjoy", "fond of", "prefer", "favoritt*", "favourite", "favorite",
           "beste jeg vet", "beste eg veit", "noe for meg", "noko for meg", "min greie", "mi greie", "min stil", "orker", "orkar", "i like", "we like", "i really like"],
 "LIKER_IKKE": ["hater", "hatar", "avskyr", "misliker", "mislikar", "kan ikke fordra", "ikke er så glad i", "ikke er glad i", "ikkje er så glad i",
                "ikke helt for meg", "ikke for meg", "ikkje for meg", "skummelt", "ekkelt", "ekkel"],
 "VIL": ["vil ha", "vil gjerne ha", "vil gjerne", "vil prøve", "har lyst på", "lyst på", "kan jeg få", "kan eg få", "kan vi få", "kan me få", "kan jeg ta", "kan jeg prøve", "kan jeg bestille",
         "kunne jeg få", "kunne jeg fått", "kunne vi få", "får jeg", "jeg tar", "eg tek", "vi tar", "me tek", "tar gjerne", "tek gjerne", "tar en", "tar ei", "tar et", "tek ein", "tek eit",
         "ønsker", "ynskjer", "gi meg", "gje meg", "gi oss", "gje oss", "noe med", "noko med", "sugen på", "kunne tenke meg", "kunne tenkt meg", "kunne jeg tenke meg", "kunne eg tenke meg", "kunne godt tenke meg",
         "kunne jeg godt tenke meg", "ville passe", "ville passet", "tenker på", "tenkjer på", "trenger", "treng", "skal ha", "må ha",
         "bestille", "i d like", "id like", "i would like", "we would like", "i ll have", "i will have", "can i have", "can i get", "could i have", "could i get", "may i have",
         "i want", "we want", "something with", "something", "anbefal*", "tilrå*", "recommend*", "foreslå*", "forslag", "suggest*", "passer", "passar",
         "hva kan jeg spise", "hva kan jeg drikke", "hva kan jeg få", "kva kan eg få", "what can i eat", "what can i have", "what can i order", "what can i drink",
         "kan dere", "kan de", "kan dokke", "kan dokker", "can you", "could you", "hadde vært digg", "hadde vært godt", "hadde smakt", "frister"],
 "SPISER": ["spiser", "spis", "spise", "eter", "ete", "eta", "eat", "eats", "drikker", "kan ha", "få i seg", "får i seg"],
 "SPISER_IKKE": ["et ikkje", "et ikke", "et aldri", "drikk ikkje", "drikk ikke", "kan ikke ha", "kan ikkje ha", "can t have", "cant have", "cannot have", "can t eat", "cant eat", "cannot eat",
                 "don t eat", "dont eat", "do not eat", "doesn t eat", "doesnt eat"],
 "TAALER": ["tåler", "tåle", "tålte", "toler", "tolerer*", "tolerate*", "vertrage"],
 "ALLERGI": ["allerg*", "alerg*", "intoleran*", "overfølsom*", "anafyla*", "anaphyla*", "reagerer på", "reagerer kraftig på", "reagerer", "reager på", "blir dårlig av", "blir sjuk av", "blir syk av",
             "blir jättedålig av", "får vondt av", "får utslett av", "trigger", "triggers", "can t tolerate", "cant tolerate", "cannot tolerate",
             "tåler dårlig", "toler dårleg", "tåler dårleg", "krise for", "migrene", "klør", "kløe", "oppustet", "oppblåst", "hjertebank", "legevakt*", "vondt i magen", "hevelse", "svulm*", "utslett"],
 "UNNGAAR": ["unngår", "unngå", "holder meg unna", "held meg unna", "halde meg unna", "holde meg unna", "holde seg unna", "styre unna", "styrer unna", "ligge unna", "ligg unna",
             "avoid", "avoids", "avoiding", "skal ikke ha", "skal ikkje ha", "vil ikke ha", "vil ikkje ha", "ikke noe med", "ikkje noko med", "ingenting med", "nothing with",
             "droppe", "dropper", "sløyfe", "sløyfes", "utelate", "leave out", "hold the", "kutte ut", "fri for", "free from", "free of", "nei til",
             "skal ikkje ha noko med", "skal ikke ha noe med", "vil ikke ha noe med", "vil ikkje ha noko med", "uaktuelt", "uaktuell", "utelukket", "ikke aktuelt"],
 "UTEN": ["uten", "utan", "without", "uden", "ohne"],
 "UTELUKK": ["som ikke er", "som ikkje er", "annet enn", "anna enn", "andre enn", "other than", "bortsett fra", "utenom", "except", "except for", "apart from"],
 "SPOER": ["hva er", "kva er", "hva betyr", "kva betyr", "fortell", "fortel", "beskriv", "forklar", "har dere", "har de", "har du", "har dokke", "har dokker", "har ni", "hvilke", "hvilken", "hvilket",
           "kva for", "kva slags", "ka slags", "hva slags", "er det", "er d", "e det", "finnes det", "fins det", "finst det", "finns det", "hva inneholder", "hva har", "kva har",
           "what is", "what s", "whats", "tell me", "describe", "do you have", "is there", "are there", "does the", "does it", "hvor mye", "hva koster", "kva kostar", "how much",
           "hvordan", "korleis", "which", "what kind", "kan du si", "kan dere si", "kan du fortelle", "kan dere fortelle", "could you tell me", "can you tell me",
           "kan jeg ta med", "kan eg ta med", "kan vi ta med", "kan dere bekrefte", "kan dere garantere", "kan kjøkkenet garantere", "can you guarantee", "can you confirm", "lurer på", "inneholder", "contain*", "er den", "er dei", "er de",
           "is the", "are the", "is it", "stekes", "lages", "serveres"],
 "HOEFLIG": ["takk", "please", "plz", "til meg", "for me"],
 "MED": ["med", "with"],
 "TOM": ["allergen*", "uten at", "uten å", "utan å", "utan at", "without being"],
}

spraak = {
 "nektelser": ["ikke", "ikkje", "itj", "itte", "ingen", "inga", "intet", "ingenting", "aldri", "neppe", "verken", "hverken", "korkje", "not", "never", "don t", "dont", "do not", "doesn t", "doesnt",
               "nicht", "kein", "keine", "inte", "aldrig"],
 "engelske_nektelser": ["no"],
 "engelske_tegn": ["the", "please", "my", "we", "you", "with", "and", "are", "any", "im", "of", "it", "this", "that", "what", "which", "does", "do", "for"],
 "leddskiller": ["men", "but", "likevel", "derimot", "however", "though", "although", "aber", "mais"],
 "leddskiller_etter_komma": ["så", "so", "derfor", "da"],
 "spoerreord": ["hva", "kva", "ka", "hvem", "hvor", "kor", "hvordan", "korleis", "hvorfor", "hvilken", "hvilke", "hvilket", "kan", "kunne", "har", "finnes", "fins", "er", "what", "who", "where",
                "how", "why", "which", "can", "could", "does", "do", "is", "are", "when", "når", "tar", "vet", "veit"],
 "sammensatt": ["allerg", "intoleran", "overfølsom"],
 "bindeord": ["og", "eller", "samt", "and", "or", "och", "und", "oder"],
 "kopula": ["er", "e", "is", "är", "are"],
 "stikk": stikk,
 "ordlister": {
  "bord": ["bord til", "bord for", "et bord", "eit bord", "ledig bord", "ledige bord", "bestille bord", "bestiller bord", "bestiller jeg bord", "bestille et bord", "booke", "booker", "=book", "boka", "boka bord",
           "reserver*", "reservasjon*", "reservation*", "tinga bord", "table for", "a table", "tisch", "har dere plass", "ledig plass", "ledig kapasitet", "avbestill*", "kortgaranti", "bryllupsmiddag"],
  "aapningstid": ["åpningstid*", "opningstid*", "åpent", "åpen", "ope", "öppet", "når åpner", "når opnar", "opnar", "åpner", "stenger", "stengjer", "stengt", "close", "closes", "opening hours", "open", "holder åpent"],
  "kosthold": ["vegetar*", "vegan*", "halal", "kosher", "keto", "lavkarbo", "fodmap", "lavfodmap", "pescetar*", "diabet*", "gravid", "pregnan*", "cellegift", "chemo"],
  "sulten": ["sult*", "skrubbsult*", "svolten", "hungry", "starving"],
  "torst": ["tørst", "tørste", "thirsty"],
  "drikkeord": ["drikke", "drikk", "drink", "drinks", "å drikke", "glass", "glas", "flaske", "bottle", "cola", "kaffe", "kaffen", "coffee", "te", "cappuccino", "espresso", "bobler", "prosecco", "champagne", "saft"],
  "spiseord": ["spise", "eta", "ete", "mat", "maten", "middag", "lunsj", "eat", "food", "rett", "retter", "rettene", "dishes", "dish"],
  "har_dere": ["har dere", "har de", "har du", "har dokke", "har dokker", "har ni", "do you have", "hva har dere av", "which", "hvilke", "hvilken"],
  "hus": ["har dere", "har de", "har dokke", "har dokker", "har ni", "tar dere", "tar dokker", "do you have", "do you take", "do you sell", "do you do", "kan dere", "kan man", "kan vi", "kan jeg", "kan eg",
          "meny*", "barnemeny", "kjøkken*", "restauranten", "palazzo", "hos dere", "pris*", "koster", "kostar", "betale", "vipps", "parkering", "parkere", "take away", "takeaway", "heis", "barnestol", "rullestol*",
          "ligger dere", "hvor ligger", "adresse*", "til dere", "til dykk", "to you", "bill", "regning*", "=tip", "service", "mattilsynet", "smilefjes", "servers", "servitør*", "bordet",
          "uteservering*", "terrasse", "dresscode", "hunden", "barnevogn"],
 },
}
# Rettelser i grunnlaget etter versjon .2 (GRUNN=3). Hver har et navn, så den kan holdes utenfor i en prøve (UTEN=navn).
if med("menta"):       # «dokumentasjon» traff mynte gjennom «menta»
    graf["ordformer"]["mynte"] = ["=menta" if x == "menta" else x for x in graf["ordformer"]["mynte"]]
if med("te"):          # «te» er trøndersk for «til» («bord te fire», «te mæ»); tre ordlistetråder pekte på det
    spraak["ordlister"]["drikkeord"] = [x for x in spraak["ordlister"]["drikkeord"] if x != "te"]
if med("forskjell"):   # «forskjellen» traff skjell
    graf["unntak"]["skjell"] = ["forskjell"]
if med("bestille"):    # «bestille» alene er oftere bord enn mat
    spraak["stikk"]["VIL"] = [x for x in spraak["stikk"]["VIL"] if x != "bestille"]
if med("sedano"):      # emnet selleri hadde ordet, allergenet ikke
    graf["allergenord"]["SE"].append("sedano")
if med("utsagn"):      # ord som i seg selv sier «uten» eller «tåler ikke», foreslått som vanlige ord av trådene i runde 2
    u = graf["allergenutsagn"]
    u["HV"]["taaler-ikke"] += ["søliaki", "coeliaki"]; u["HV"]["spiser-ikke"] += ["gluten fri"]
    u["M"]["spiser-ikke"] += ["milk free", "non dairy"]
    u["E"]["spiser-ikke"] += ["eggefri", "æggefri"]
    u["N"]["spiser-ikke"] += ["nøddefri", "nötfri", "nutfree", "nussfrei"]
    u["F"] = {"spiser-ikke": ["fiskefri"]}
if GRUNN >= 3:
    # Det svarene trenger av data (arbeidspakke 5): når én post «leder klart», hvilke emner som gjelder alkohol,
    # og hva en liste over flere poster for ett emne heter («Vi har tre desserter:»).
    graf["svar"] = {
     "klar_leder": 2.5,
     "alkoholemner": ["hvitvin", "rødvin", "vin", "øl"],
     "fortell": {
      "ost": "retter med ost", "sitron": "retter med sitron", "sjømat": "retter med sjømat", "dessert": "desserter",
      "mozzarella": "retter med mozzarella", "pizza": "pizzaer", "tomat": "retter med tomat", "olivenolje": "retter med olivenolje",
      "forrett": "forretter", "fisk": "retter med fisk", "salami": "retter med salami", "kjøtt": "retter med kjøtt",
      "pasta": "pastaretter", "kapers": "retter med kapers", "asparges": "retter med asparges", "hovedrett": "hovedretter",
      "pistasj": "retter med pistasj", "potet": "retter med potet",
      "alkoholfritt": "drikker uten alkohol", "brus": "slags brus", "mocktail": "mocktailer",
     },
    }
# tillegg fra ordlistetrådene (flett_leks.py og flett_leks2.py): tredje argument og utover, i rekkefølge
for tilleggsfil in sys.argv[3:]:
    t = json.load(open(tilleggsfil, encoding="utf-8"))
    def flett(maal, kilde):
        for k, v in kilde.items():
            har = maal.setdefault(k, [])
            for x in v:
                if x not in har: har.append(x)
    flett(graf["ordformer"], t["ordformer"]); flett(graf["allergenord"], t["allergenord"])
    flett(spraak["stikk"], t["stikk"]); flett(spraak["ordlister"], t["ordlister"])
    for x in t["nektelser"]:
        if x not in spraak["nektelser"]: spraak["nektelser"].append(x)
ut = {"schema": "palazzo.husgraf.v1", "versjon": sys.argv[2] if len(sys.argv) > 2 else "husgraf-utkast",
      "kilde": "palazzo_seed_corpus.json; emner og kanter fra graf/emner-v1.json", "graf": graf, "spraak": spraak}
json.dump(ut, open(sys.argv[1], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("skrevet", sys.argv[1], "emner:", len(set(k["emne"] for sek in ("retter", "drikke") for l in graf[sek].values() for k in l)) + len(graf["emner_uten_kant"]))
