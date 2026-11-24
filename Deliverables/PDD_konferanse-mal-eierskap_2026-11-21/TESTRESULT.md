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

Kjørt 2026-11-24 på Kjetils Mac (Remote Control, backupdisken, byggevindu v-kmecp-2), CellProtocol origin/main b5f467a5 (inneholder #103).

`swift test --filter EntityAnchorUnregisteredKeypathTests`: exit 0, 4 tester, 0 feil (testWriteEitherReadsBackOrFailsLoudly, testTemplateRootsAreStoredAndSurviveRestart, testTemplateRootsRefuseAnotherEntity, testTemplateRootsDoNotReopenAnchorRoots).

```
MÅLING CellApple | person.attributes.konferanseKontroll | lagret
MÅLING CellApple | event.ownedBy | lagret
MÅLING CellApple | project.milestones | lagret
MÅLING CellApple | conference.6f1c2d3e-0000-4000-8000-000000000001.role | lagret
MÅLING CellApple | groups.6f1c2d3e-0000-4000-8000-000000000002.name | lagret
MÅLING CellApple | template.ref | lagret
MÅLING CellVapor | person.attributes.konferanseKontroll | lagret
MÅLING CellVapor | event.ownedBy | lagret
MÅLING CellVapor | project.milestones | lagret
MÅLING CellVapor | conference.6f1c2d3e-0000-4000-8000-000000000001.role | lagret
MÅLING CellVapor | groups.6f1c2d3e-0000-4000-8000-000000000002.name | lagret
MÅLING CellVapor | template.ref | lagret
```

Målingen er tatt etter WP4, så den viser at malens røtter lagres. Før WP4 viser koden (lest 21.11) `KeyValueErrors.notFound` for de nye røttene; det ble ikke målt før endringen.

`swift test --filter EntityAnchor`: exit 0, 38 tester, 0 feil (AccessBoundary 10, Encryption 3, EnrollmentContract 4, FlowPlacement 3, Genesis 9, UnregisteredKeypath 4, og 5 tester i andre suiter som filteret traff).

## build

CellProtocol: Linux-CI grønn på #103 (regression, Persisted Cell file bounds, CellBase static Linux musl, Vapor identity vault strict storage, bounded synthetic runtime matrix). CellScaffold: «Focused control-plane gates» grønn på #498 (5d191e6a), etter at en feil som også var på main (ObjectStorageMultipartTests.swift:308) ble rettet i samme PR.

## regression

CellScaffold, Kjetils Mac 2026-11-24, origin/main 3d487b5d, CellProtocol-pin dc1de6f: `CELLPROTOCOL_PUBLISHED_API=1 swift test --filter ConferenceDefinitionOwnershipTests` → exit 0, 3/3. Hele testmengden i CellScaffold er ikke kjørt lokalt; CI-porten over bygger alle mål.
