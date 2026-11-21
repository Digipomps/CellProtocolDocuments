# Testresultat — konferanse mal og eierskap

## contract

Kjørt 2026-11-21 av Losen i skyøkten, Python 3.13.16. Kommando: `python3 checks/validate_contract.py` fra oppgavemappen.

```
OK  01-arrangor-gyldig.json [test.kme.arrangor-fixture]
OK  02-arrangor-admin-ikke-medlem.json [test.kme.arrangor-negativ]
OK  03-arrangor-sykel.json [test.kme.arrangor-negativ]
OK  04-arrangement-med-eier.json [test.kme.eierskap-fixture]
OK  05-arrangement-uten-eier.json [test.kme.eierskap-fixture]
OK  06-to-arrangementer-samme-eier.json [test.kme.eierskap-bakvei]
OK  07-folger-malen-med-reserverte.json [test.kme.mal-validator]
OK  08-mal-feil-versjon-og-mangler.json [test.kme.mal-validator]
OK  09-en-utvidelse-er-gyldig.json [test.kme.utvidelse-gyldig]
OK  10-to-bruker-samme-utvidelse.json [test.kme.utvidelse-forslag]
OK  11-deltaker-to-konferanser.json [test.kme.deltakerpost-to]
OK  12-deltaker-innebygd-representasjon.json [test.kme.deltakerpost-ingen-kopi]
OK  13-deltaker-unoklet-post.json [test.kme.deltakerpost-to]
13/13 fixtures stemmer
```

Sjekk av at validatoren kan bli rød: to fixtures ble endret i en kopi (forventning fjernet i 12, administrator gjort til medlem i 02). Begge ble FEIL, 11/13.

## lagring

Ikke kjørt. Testen er `EntityAnchorUnregisteredKeypathTests` i CellProtocol PR #103 og kjøres i køen på Macen etter «Slipp inn». Lest i koden 2026-11-21 (CellProtocol 669850b): set-intercepts bare for person, proofs, relations, identityLinks, signedAgreementEntity.commit; andre røtter gir `KeyValueErrors.notFound` i `GeneralCell.set` (Sources/CellBase/Cells/GeneralCell/GeneralCell.swift). Forventet måling: kontrollen lagres, de nye røttene avvises.

## build

Venter (WP3).

## regression

Venter (WP3).
