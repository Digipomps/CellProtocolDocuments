# TESTRESULT — ordklasseramme i Swift

Oppgavemappe: `CellProtocolDocuments/Deliverables/PDD_ordklasseramme-swift_2026-10-13` · 14. oktober 2026

Kode: CellProtocol, grenen `losen/purpose-frame-matcher-20261013`, commit `2033ab7ac9c537c2c4d20b5ae4d8a9922ae845ee` (fra `origin/main` `34cecef`), arbeidstre `_worktrees/cellprotocol-purpose-frame-matcher`, pakke `commons/purpose-frame-matcher`. Ikke pushet.

Fasit: `HAVEN-Deploy/_handoff/ORDKLASSERAMME/fixtures.json` (2 095 rader fra Python R3 + ordklasseramme; DEV3, DEV4, DEV5, Butler v2 og 16 kanttilfeller). Bunt-sha256 `59ad83bf…`.

To kjøringer av `swift test` på macOS arm64, Apple Swift 6.4:

| Kjøring | Hvem | Når | Resultat | Bevis |
|---|---|---|---|---|
| A | Codex (pfm1), samme jobb som skrev koden | 13.10 22:48Z | 8 tester, 0 feil | `_losen-queue/done/pfm1-swiftpakke-20261013.svar.md`, `HAVEN-Deploy/_handoff/ORDKLASSERAMME/WP1-FERDIG` |
| B | Skriptjobb (pfm3), ikke Codex, egen byggemappe | 14.10 01:05–01:06Z | 8 tester, 0 feil, exit 0 | `HAVEN-Deploy/_handoff/ORDKLASSERAMME/RESULT-pfm3.md` |

Første forsøk på B (pfm2) stoppet på køens skrivetak på 2 GiB per fil (exit 153) før noen test kjørte. Skriptet kjører nå `swift test` via `HAVEN-Deploy/_handoff/LANDING/uten-skrivetak.sh`, slik andre Swift-bygg i køen gjør.

## #parity
`ParityTests.testAll2095Rows`: samme topp-3-refs, |Δscore| ≤ 1e-6 og samme svar for hver rad.
Utdata: `rader 2095 avvik 0 maks dscore 4.999999858590343e-10` (A). Kjøring B ga samme linje.

## #curve
`CurveTests.testDEV5SilverCurve` (DEV5, sølv), krav ≤ 1e-9:

| Falske forslag | Swift | Python |
|---|---|---|
| 0 % | 0.728538283062645 | 0.728538283062645 |
| 5 % | 0.765661252900232 | 0.765661252900232 |
| 10 % | 0.7958236658932715 | 0.7958236658932715 |
| 15 % | 0.802784222737819 | 0.802784222737819 |

## #pos
`PosTableTests`: 67 278 former; gikk→VERB, bøker→NOUN, oppgåver→NOUN, invitere→VERB, kva→PRON, hanne→PROPN. Grønn.

## #bundle
`BundleTests`: sha256 av bunten i pakken = `bundle_sha256` i fasiten (og to standardvektorer for hjelpefunksjonen). Grønn. Merk: sjekken skjer i testen, ikke når matcheren laster bunten (se ACCEPT, avvik 1).

## #fail-closed
`FailClosedTests`: tom melding, «   » og «🙂🙂» gir `purpose://prompt.unknown` på tre flater; alle 530 negativer med forventet unknown gir unknown (0 avvik); manglende bunt kaster feil. Grønn.

## #build
`swift build` og `swift test` med `--disable-sandbox` på macOS: grønne. Linux er ikke kjørt (ingen Linux-verktøykjede fra køen); koden bruker bare Foundation.
