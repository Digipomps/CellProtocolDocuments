#!/usr/bin/env python3
"""Holder contract/noekkelstier.json mot kildefilene for PalazzoBooking.

    python3 -B sjekk_noekkelstier.py <kilde-rot>

<kilde-rot> er en mappe med Sources/App/... slik den står i PalazzoScaffold, for
eksempel HAVEN-Deploy/_handoff/HD-0077/bordbestilling/kilde. Skriver ingenting.
Avslutter med 0 når alt stemmer, ellers 1.
"""
import json
import os
import re
import sys

ROT = sys.argv[1]
HER = os.path.dirname(os.path.abspath(__file__))


def les(sti):
    with open(os.path.join(ROT, sti), encoding="utf-8") as fil:
        return fil.read()


liste = json.load(open(os.path.join(HER, "noekkelstier.json"), encoding="utf-8"))
kontrakt = les("Sources/App/Support/PalazzoScaffoldContract.swift")
celle = les("Sources/App/Cells/PalazzoBookingCell.swift")
regler = les("Sources/App/Models/PalazzoTableBookingModels.swift")
ruter = les("Sources/App/routes.swift")

feil = []
ok = 0


def krev(sant, tekst):
    global ok
    if sant:
        ok += 1
    else:
        feil.append(tekst)


# 1. Navnene i `enum Booking` er nøyaktig de i listen.
blokk = re.search(r"enum Booking \{(.*?)\n    \}", kontrakt, re.S)
krev(blokk is not None, "fant ikke `enum Booking` i kontrakten")
i_kode = {}
if blokk:
    for navn, verdi in re.findall(r'static let (\w+) = ("[^"]+"|[\w.]+)', blokk.group(1)):
        i_kode[navn] = verdi.strip('"')
    if i_kode.get("upcoming") == "Integration.bookingsUpcoming":
        treff = re.search(r'static let bookingsUpcoming = "([^"]+)"', kontrakt)
        i_kode["upcoming"] = treff.group(1) if treff else "?"
i_liste = {rad["constant"]: rad["keypath"] for rad in liste["keypaths"]}
krev(i_kode == i_liste, f"navnene i koden og i listen er ulike: kode {sorted(i_kode.items())}, liste {sorted(i_liste.items())}")
krev(len(liste["keypaths"]) == 16, f"listen har {len(liste['keypaths'])} nøkkelstier, ventet 16")

# 2. Hver nøkkelsti er registrert i cellen, med riktig slag og riktig gruppe.
for rad in liste["keypaths"]:
    navn = rad["constant"]
    ref = f"PalazzoScaffoldContract.Booking.{navn}"
    if rad["who"] == "contract":
        krev(re.search(r"registerDerivedAnswer\(\s*key: " + re.escape(ref) + r"\b", celle) is not None,
             f"{rad['keypath']}: ikke registrert som avledet svar")
        continue
    slag = "registerGet" if rad["kind"] == "get" else "registerSet"
    krev(re.search(slag + r"\(\s*key: " + re.escape(ref) + r"\b", celle) is not None,
         f"{rad['keypath']}: ikke registrert med {slag}")
    oppslag = f'"{rad["access"]} \\({ref})"'
    gjest = re.search(r"static let guestOperations: Set<String> = \[(.*?)\]", celle, re.S).group(1)
    ansatt = re.search(r"static let staffOperations: Set<String> = \[(.*?)\]", celle, re.S).group(1)
    if rad["who"] == "guest":
        krev(oppslag in gjest and oppslag not in ansatt, f"{rad['keypath']}: står ikke (bare) i guestOperations")
    elif rad["who"] == "staff":
        krev(oppslag in ansatt and oppslag not in gjest, f"{rad['keypath']}: står ikke (bare) i staffOperations")
    else:
        krev(oppslag not in gjest and oppslag not in ansatt, f"{rad['keypath']}: skal ikke stå i noen av gruppene")

# 3. Rutene.
for rad in liste["keypaths"]:
    metode, sti = rad["route"].split(" ")
    siste = sti.rsplit("/", 1)[1]
    par = f'("{siste}", PalazzoScaffoldContract.Booking.{rad["constant"]})'
    egen = f'app.post("api", "booking", "{siste}")'
    krev(par in ruter or (metode == "POST" and egen in ruter), f"{rad['route']}: fant ikke ruten")

# 4. Kanalene.
hus = re.search(r"static let houseChannels: \[String\] = \[(.*?)\]", regler).group(1)
krev(re.findall(r'"([^"]+)"', hus) == liste["channels"]["house"], "husets kanaler er ulike i koden og i listen")
krev(f'static let guestChannel = "{liste["channels"]["guest"]}"' in regler, "gjestens kanal er en annen i koden")
krev(f'static let walkInChannel = "{liste["channels"]["walk_in"]}"' in regler, "kanalen for walk-in er en annen i koden")

# 5. Kodene.
alle = dict(re.findall(r'case (\w+) = "([a-z_]+)"', re.search(r"enum PalazzoBookingRefusal.*?var message", regler, re.S).group(0)))
inn = re.search(r"inputRefusals: Set<PalazzoBookingRefusal> = \[(.*?)\]", celle, re.S).group(1)
inn_navn = set(re.findall(r"\.(\w+)", inn))
fra_regler_400 = sorted(alle[n] for n in inn_navn)
fra_regler_409 = sorted(v for n, v in alle.items() if n not in inn_navn)
krev(fra_regler_400 == sorted(liste["error_400_from_rules"]), f"400-kodene fra reglene er ulike: kode {fra_regler_400}")
krev(fra_regler_409 == sorted(liste["refused_409"]), f"409-kodene er ulike: kode {fra_regler_409}")
for kode in liste["error_400_from_cell"]:
    krev(f'"{kode}"' in celle, f"{kode}: finnes ikke i cellen")

for linje in feil:
    print("AVVIK:", linje)
print(f"{ok} kontroller stemmer, {len(feil)} avvik")
sys.exit(1 if feil else 0)
