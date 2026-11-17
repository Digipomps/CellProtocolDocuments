# PLAN — ordklasseramme i Swift

Oppgavemappe: `CellProtocolDocuments/Deliverables/PDD_ordklasseramme-swift_2026-10-13` · Skrevet 13. oktober 2026 kl. 21:00 UTC, før noen kode er skrevet.

Stier er relative til HAVEN-roten. Formålene og testene er de i den godkjente spesifikasjonen (`FORMAALSSPEC.md`, iterasjon 1, G1 godkjent 13.10 med valget «Godkjent, egen pakke»). Planen legger ikke til og tar ikke bort noe der.

## Kort

```
 1 Fasiten på Mac-en   bunt, ordklassetabell, 2 095 fasitrader og referansen til HAVEN-Deploy/_handoff/ORDKLASSERAMME/
 2 Codex skriver pakken CellProtocol/commons/purpose-frame-matcher, eget arbeidstre og egen gren, bare Foundation
 3 Codex kjører testene swift test i pakken; paritet, kurve, ordklasser, bunt-hash, lukker ved tvil
        │  STOPP: en fasitrad avviker mer enn 1e-6, eller kurven avviker
 4 Uavhengig sjekk     en egen skriptjobb kjører swift test på nytt i samme tre og skriver rapporten
 5 Dokumentene         TESTRESULT.md og ACCEPT.md, holdt mot bevisfilene, så G3 hos Kjetil
```

**Hva Kjetil må gjøre.** Ingenting før G3, så lenge ingenting stopper. Ingen push, ingen merge, ingen utsetting i denne oppgaven.

**Sted.** Arbeidstre `_worktrees/cellprotocol-purpose-frame-matcher`, grenen `losen/purpose-frame-matcher-20261013` fra `origin/main` i CellProtocol. Byggemappe `/private/tmp/pfm-build-20261013` (slettes etterpå). Egen innboks i køen: `_losen-queue/inbox-pfm`. Pakken er liten og bygger uten avhengigheter; diskregelen i `KOORDINERING.md` sjekkes før bygg (70 GiB ledig lest 13.10 20:58Z).

## Arbeidspakker

| Pakke | Formål | Hva det innebærer | Test som skal bli grønn | Leveranse (§3) |
|---|---|---|---|---|
| WP1 Databunt | `….data-bundle` | `bundle.json` (skjema `haven.purpose-frame-matcher.bundle.v1`) legges i pakkens `Resources/`; sha256 sjekkes ved lasting | BundleTests | `TESTRESULT.md#bundle` |
| WP2 Ordklassetabell | `….pos-table` | `ordklasser.tsv` (UD, CC BY-SA 4.0, kilde i filhodet) lastes uten NLTagger | PosTableTests | `TESTRESULT.md#pos` |
| WP3 Matcheren | `….matcher-port` | Port av `ref_bundle.py` linje for linje: normalisering, stemming, ordsplitt, trigram-fuzzy, TF-IDF, frasetreff, samtalehandlinger, spørreord, skop, dekning. Unicode-skalarer og rekkefølgeregler som i referansen; ingen «forbedringer» | ParityTests: 2 095 rader, topp 3 lik, |Δscore| ≤ 1e-6 | `TESTRESULT.md#parity` |
| WP4 Ordklasserammen | `….pos-frame` | `pos_frame` oppå tekstscoren | CurveTests: DEV5-kurven lik Python innen 1e-9 (0.7285 / 0.7657 / 0.7958 / 0.8028) | `TESTRESULT.md#curve` |
| WP5 Lukker ved tvil | `….fail-closed` | Under terskel `purpose://prompt.unknown`; ukjent flate gir bare samtalehandlinger; manglende eller endret bunt gir feil, ikke svar | FailClosedTests | `TESTRESULT.md#fail-closed` |
| WP6 Alt virker | roten | README i pakken (kilde, lisens, hvordan bunten lages), TESTRESULT og ACCEPT holdt mot bevis av en egen sjekk | uavhengig `swift test` grønn | `ACCEPT.md` |

Alle seks går som én Codex-jobb, fordi fasiten er felles og pakkene ikke kan prøves hver for seg uten de andre. Jobben rapporterer «verifisert» bare når `swift test` faktisk har kjørt grønt; ellers «skrevet, ikke verifisert».

## Ikke med

Kobling inn i Butler eller `ChatPurposeResourceRouter`, engelske erklæringer, endring i Book 23, Linux-bygg (tas i CI ved neste port), push.
