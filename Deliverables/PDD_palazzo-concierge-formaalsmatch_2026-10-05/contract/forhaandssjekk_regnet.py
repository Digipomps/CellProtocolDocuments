# Regner forhåndssjekken på eksempelsetninger, på tre måter:
#   1. de fem mønstrene Kallimachos har
#      (CellScaffold/_wt-butler-e1-20260929/Sources/App/Cells/AI/KallimachosAdvisorCell.swift, linje 246–252),
#   2. en liste over det som stoppes: «@», «(at)» eller «[at]» i setningen, eller seks sifre eller flere i alt,
#   3. planens forslag, en liste over det som slipper gjennom: setningen sendes bare når hvert tegn er en bokstav,
#      et mellomrom eller vanlig skilletegn (, ? ! ' " « » : ; - –), og et punktum bare sist i en setning.
# Regnet i Python, ikke kjørt i Swift. Bruk: python3 forhaandssjekk_regnet.py
import re
KALLIMACHOS = [("e-postadresse", r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"),
               ("personnummer", r"(?<![0-9])[0-9]{6}[ ]?[0-9]{5}(?![0-9])"),
               ("kortnummer", r"(?<![0-9])[0-9]{13,19}(?![0-9])"),
               ("IBAN", r"(?<![A-Za-z0-9])[A-Z]{2}[0-9]{2}[A-Z0-9]{10,30}(?![A-Za-z0-9])"),
               ("telefon med landkode", r"\+[0-9]{2}[ ]?[0-9]{6,12}")]
# (setningen, skal den stoppes?)
SETNINGER = [("Ring meg på 912 34 567", True), ("Ring 91234567", True), ("Nummeret er +47 912 34 567", True),
             ("Nummeret er +4791234567", True), ("Ring 0047 91234567", True), ("Ring meg på 555 1234", True),
             ("Kortet er 4111 1111 1111 1111", True), ("Kortet er 4111-1111-1111-1111", True), ("Kortet er 4111111111111111", True),
             ("Fødselsnummeret er 010190 12345", True), ("Kontoen er NO93 8601 1117 947", True),
             ("Skriv til kari@example.org", True), ("Skriv til kari @ example.org", True), ("Skriv til kari(at)example.org", True),
             ("Skriv til kari[at]example.org", True), ("Skriv til kari(a)example.org", True), ("Skriv til kari at example.org", True),
             ("Nummeret er 9123", True), ("og så 4567", True), ("Ring meg på 912 34 fem seks sju", True),
             ("Skriv til kari krøllalfa example punktum org", True), ("Ring meg på ni en to tre fire fem seks sju", True),
             ("Jeg heter Kari Nordmann og bor i Storgata", True),
             ("Har dere bord til 4 den 12.10.2026 kl. 19:00?", False), ("To pizzaer og 3 øl", False), ("Noe f.eks. med fisk?", False),
             ("Har dere noe sånt som risboller?", False), ("Jeg vil ha noe søtt.", False)]
def kallimachos(s):
    return [navn for navn, m in KALLIMACHOS if re.search(m, s)]
def stoppliste(s):
    grunner = []
    if "@" in s or re.search(r"[\(\[]\s*at\s*[\)\]]", s, re.I): grunner.append("«@», «(at)» eller «[at]»")
    if sum(c.isdigit() for c in s) >= 6: grunner.append("seks sifre eller flere")
    return grunner
TILLATT = re.compile(r"(?:[^\W\d_]|[ ,?!'\"«»:;\-–]|\.(?=\s|$))+")
def slippliste(s):
    if TILLATT.fullmatch(s): return []
    grunner = []
    if any(c.isdigit() for c in s): grunner.append("et siffer")
    if re.search(r"\.(?!\s|$)", s): grunner.append("punktum inne i et ord")
    annet = sorted({c for c in s if not re.fullmatch(r"[^\W\d_]|[ ,?!'\"«»:;\-–.]", c) and not c.isdigit()})
    if annet: grunner.append("tegnet " + " ".join("«%s»" % c for c in annet))
    return grunner or ["et tegn som ikke er tillatt"]
def celle(grunner):
    return "stopper (" + ", ".join(grunner) + ")" if grunner else "slipper gjennom"
print("| Setning | Skal stoppes | Kallimachos' fem mønstre | Liste over det som stoppes | Forslaget: liste over det som slipper gjennom |\n|---|---|---|---|---|")
gjennom = [0, 0, 0]; uskyldige = [0, 0, 0]
for s, skal in SETNINGER:
    r = [kallimachos(s), stoppliste(s), slippliste(s)]
    for i in range(3):
        if skal and not r[i]: gjennom[i] += 1
        if not skal and r[i]: uskyldige[i] += 1
    print("| «%s» | %s | %s | %s | %s |" % (s, "ja" if skal else "nei", celle(r[0]), celle(r[1]), celle(r[2])))
n_skal = sum(1 for _, x in SETNINGER if x); n_ikke = len(SETNINGER) - n_skal
print("\nAv %d setninger som skal stoppes, slipper Kallimachos' mønstre %d gjennom, listen over det som stoppes %d, og forslaget %d. Av %d som ikke trenger å stoppes, stopper de %d, %d og %d." % (n_skal, gjennom[0], gjennom[1], gjennom[2], n_ikke, uskyldige[0], uskyldige[1], uskyldige[2]))
