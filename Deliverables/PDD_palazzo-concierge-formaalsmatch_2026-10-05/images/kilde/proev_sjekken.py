# Prøver at sjekk_tekster.js blir rød når rammene endres på seks måter. Endrer ingen fil her: kopierer til en midlertidig mappe.
# Bruk: python3 proev_sjekken.py   (fra mappen der tilstander.js og sjekk_tekster.js ligger)
import os, shutil, subprocess, sys, tempfile
her = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(her, "tilstander.js"), encoding="utf-8").read()
MUT = [("sidens merkelapp tilbake på bilde 1", 'kind: "offer", intro: INTRO_NY, understood: "du liker ost.", hideBadge: true,', 'kind: "offer", intro: INTRO_NY, understood: "du liker ost.", viserSidensMerkelapp: true,'),
       ("et tilbud med andre ord etter «tåler ikke»", '"Formaggi misti.\\nMerket med: melk.\\nBeskrivelse: Utvalg av oster fra små utvalgte gårder i Italia med tilbehør.",\n          { confidence: "medium", warnings: [LINJE_PERSONAL, LINJE_DATERT] })', '"Formaggi misti.\\nMerket med: melk.\\nBeskrivelse: Utvalg av oster fra små utvalgte gårder i Italia med tilbehør.\\n\\nJeg anbefaler sitronkremen.",\n          { confidence: "medium", warnings: [LINJE_PERSONAL, LINJE_DATERT] })'),
       ("«er uten nøtter» i listen", '"Crema di limone Siciliana.\\nMerket med: hvete/gluten.', '"Crema di limone Siciliana er uten nøtter.\\nMerket med: hvete/gluten.'),
       ("et feilstavet rettnavn i listen", '"Crema di limone Siciliana.\\nMerket med: hvete/gluten.', '"Crema di limone Sicilana.\\nMerket med: hvete/gluten.'),
       ("advarselen skjult i et tilbud", 'understood: "du liker lam.", actions: JA_NEI, note: JA_NOTE, hideSources: true, hideBadge: true }', 'understood: "du liker lam.", actions: JA_NEI, note: JA_NOTE, hideSources: true, hideWarning: true, hideBadge: true }'),
       ("en skrivefeil i en beskrivelse", 'Blekksprutcarpaccio med kokt potet, stangselleri, olivenolje og sitron.",\n  agnello', 'Blekksprutcarpaccio med kokt potet, selleri, olivenolje og sitron.",\n  agnello')]
gikk_gjennom = 0
with tempfile.TemporaryDirectory() as tmp:
    shutil.copy(os.path.join(her, "sjekk_tekster.js"), tmp)
    r = subprocess.run(["node", "sjekk_tekster.js", os.path.join(her, "tilstander.js")], cwd=tmp, capture_output=True, text=True)
    print("uendret: rc=%d, %s" % (r.returncode, r.stdout.strip().split("\n")[-1]))
    for navn, a, b in MUT:
        if src.count(a) != 1:
            print("ENDRINGEN TRAFF %d GANGER: %s" % (src.count(a), navn)); gikk_gjennom += 1; continue
        open(os.path.join(tmp, "t.js"), "w", encoding="utf-8").write(src.replace(a, b))
        r = subprocess.run(["node", "sjekk_tekster.js", "t.js"], cwd=tmp, capture_output=True, text=True)
        feil = [l for l in r.stdout.split("\n") if l.startswith("FEIL")]
        slag = "; ".join(sorted({l.split("]")[0][6:] for l in feil}))
        print("%-44s rc=%d, %d feil: %s" % (navn, r.returncode, len(feil), slag or "ingen"))
        if r.returncode == 0: gikk_gjennom += 1
print("endringer sjekken ikke så:", gikk_gjennom)
sys.exit(1 if gikk_gjennom else 0)
