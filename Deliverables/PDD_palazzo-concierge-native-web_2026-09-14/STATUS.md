# STATUS — palazzo concierge native web

- surfaces: cell, codex, scaffold, web
- tags: concierge, palazzo, scaffold, web
- HAVEN-Deploy: HD-0076 (feilen), HD-0077 (deploy)

## Porter
- G1: godkjent 2026-09-14 (Kjetil: «1. Gjør B»)
- G1-GUI: godkjent 2026-09-14 (referansen er dagens produksjonsflate haven.digipomps.org/palazzo — `images/palazzo-leaf-prod-v1.jpg`; flaten flyttes, ikke tegnes om)
- G2: godkjent 2026-09-14 (auto — «Kjør i gang Codex astra på dette så ser vi hvor langt vi kommer»)
- G3: venter        (test.standalone og test.gui.parity er Kjetils)

Sett en port til `godkjent <dato>` kun når Kjetil har sagt det. `purpose_dev.py validate <mappe>` nekter porter uten artefakter.

## Planbytter (dato — hvorfor)
-

## Logg
- 2026-09-14: opprettet etter målt 503 på prod/staging (HD-0076) og B2 = B. Codex-jobb `pz2-concierge-native-web-20260914` lagt i _losen-queue etter pz1.
- 2026-09-14 (Astra/Codex): WP0–WP4 skrevet, verifisert med full regresjon. Native arm64-bygg grønt; full `swift test --disable-sandbox --triple x86_64-apple-macosx13.0 --disable-swift-testing` med offlineflagg: 116 XCTest-tester, 0 feil, exit 0. Baseline målt 105; native standard-testkommando fortsatt blocked av arm64/x86_64-lastermiks, gjentatt og dokumentert. Ingen tester/korpus/gateway endret; ingen git/nettverk. TESTRESULT/ACCEPT, rålogger, svar og SHA-256-manifest er skrevet; KJOR-SELV-build.sh tørrkjørt. G3/WP5 standalone/parity venter fortsatt på Kjetil. Webmetadata på configuration og ekstern HAVEN-lenke er dokumenterte tilpasninger; korpus-reingest og WP6 er utenfor.
