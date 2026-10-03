# ACCEPT — PZ1, 2026-09-14

**Skrevet, verifisert med avgrenset test.** Dette er forventning mot faktisk resultat, ikke Kjetils G3-godkjenning. Full Palazzo-integrasjon og G5/parity er ikke verifisert. Én eksisterende regresjonsfeil står igjen.

| § / krav | Forventning | Faktisk | Status / evidens |
|---|---|---|---|
| §0 / WP0 | Baseline på treet før endring; gjenta ny rød test | To kjøringer, begge 121 tester / 2 hoppet over / samme ene feil | Målt, rød baseline. [baseline](TESTRESULT.md#baseline) |
| §1 remote-lookup / WP1 | Valgfri keypath, eksisterende lokale oppslag beholdes | Direkte/nestet decoding, bevarer case for fjern celle og keypath; lokale oppslag normaliseres som før | Pass, [remote-lookup](TESTRESULT.md#remote-lookup), [rewrite](TESTRESULT.md#rewrite) |
| §1 remote-lookup / WP2 | Oppslag over bridgehead gir 200 og aktiv «Palazzo Gjest» | Produksjonens *kode* (Porthole-action, ekte resolver/BridgeBase) gir 200 med eksportfixture i en **in-memory-test** (XCTVapor, testtransport, ingen nettverk); dynamisk lesing gjennom lastet konfigurasjon treffer probe-publisisten | Avgrenset pass; **Palazzo-app-integrasjon ikke verifisert**. Presisert 2026-09-28: dette er ikke en prøve mot staging/prod, verken over PalazzoBridgehead eller CellScaffolds `/bridgehead` — den siste har vært avregistrert i staging og prod siden 13.07 (se `PDD_bro-paa-i-prod_2026-09-26`). [remote-lookup](TESTRESULT.md#remote-lookup) |
| §1 trust-boundary | Ukjent vert / manglende keypath gir 400 uten resolver-kall | Spy viser null kall, også ved aktiv UUID-match. Feil port, token, userinfo, query og localhost dekkes | Pass, [trust](TESTRESULT.md#trust) |
| §1 reference-rewrite / WP3a | Lokale kilde-/cellereferanser blir fjerne; øvrig innhold uendret | Original Palazzo-eksport sammenlignes i kanonisk JSON. Lokal last, IPv6 og eksisterende fjerne referanser dekkes | Pass, [rewrite](TESTRESULT.md#rewrite) |
| §1 published-allowlist / WP3b | Lokal kjent / ukjent / fjern godkjent / fjern avvist | Matrisen og token/port-grensene passerer. Statisk liste er byte-identisk; kontrollplanets særregel beholdes | Pass, [allowlist](TESTRESULT.md#allowlist) |
| §1 preview-tool / WP4 | CLI/scenario sender keypath, input.json viser det | Produksjonsfunksjoner testet offline med faktisk G5-argv. CLI-prioritet og gammel payload dekkes | Pass innen offline-kontrakt, [preview-tool](TESTRESULT.md#preview-tool) |
| §3 liste | Preview bruker `guest.configuration` | Pålagt listekommando oppdatert; input.json kontrollert | Skrevet og offline-verifisert |
| §3 artikkel | Preview bruker `guest.article.configuration` og art-pistasj-bronte | Argument lagt til; eksisterende eksporterte skeleton/binding er beholdt og kontrollert | Skrevet og offline-verifisert |
| §3 hus | Preview bruker `content.configuration` | Pålagt huskommando oppdatert; input.json kontrollert | Skrevet og offline-verifisert; husautorisasjon krever virkelig husidentitet |
| §2 / grensene | Ingen CellProtocol-endring, cellekopiering, ny trust-env eller endret lokal liste | Kun scaffold-oppslag/policy, JS/bash og testfixture endret. Originale tester er uendret | Pass, [files](TESTRESULT.md#files), [scope-kontroll](evidence/scope-check.json) |
| §5 test.build / WP5 | Bygg med isolert runner | Testbygget passerer; siste bygg 23,58 s | Pass, [build](TESTRESULT.md#build) |
| §5 test.regression / WP5 | Samme avgrensede filter før/etter | 129 tester etter, 2 hoppet over, samme ene eksisterende feil; 8/8 nye passerer | Rød som baseline, ingen nye feil observert. [regression](TESTRESULT.md#regression) |
| §5 test.docs-updated | Datert avsnitt om endret oppførsel | «Flater fra eksternt scaffold», datert 2026-09-14, beskriver lookup, trust, omskriving og preview | Pass, se docs nedenfor |
| §5 test.status-current | STATUS speiler faktisk tilstand | G3 venter; logg og WP-status har testgrenser og eksisterende feil | Pass, se status nedenfor |

## docs

`CellScaffold/Documentation/Skeleton_Runtime_Iteration_Workflow.md` har avsnittet
«Flater fra eksternt scaffold» med `Last verified against code: 2026-09-14`.
Beskrivelsen skiller kodeoppførsel og lokal test fra virkelig Palazzo/G5-kjøring.
Det står også at valgfri tomtilstands-preview er uendret og mangler keypath.

## status

[STATUS.md](STATUS.md) og [PLAN.md](PLAN.md) er oppdatert. WP0–WP4 har artefakter;
WP5 har avgrenset verifikasjon, eksisterende regresjonsfeil og gjenstående
Palazzo-integrasjon. G1/G2 er beholdt som godkjent av Kjetil; G3 er fortsatt
ventende. WP6/G5 og WP7/commit er ikke kjørt.

## Avgrensede krav fra formålspakkene

Denne slicen endrer ikke skeleton-innhold eller cellekontrakter. Nye
Binding-/reachability-kjøringer, kontraktvalidator, full testcase-mengde og
lastetidsmåling tre ganger er ikke utført. Rekkefølge/ruting og kapabilitetsgrunnlag
følger FORMAALSSPEC og den eksisterende resolver-/bridgehead-koden; in-memory-
testen bekrefter denne kodeveien for den avtalte loopback-adressen. Den bekrefter
ikke Palazzo-appens egne tilgangsvurderinger eller en ekte socket-handshake.

Ingen ny KJOR-SELV-build-handoff var nødvendig: bygging i den foreskrevne
runneren var mulig. Dermed gjelder ikke test.handoff.dry-run for et nytt byggeskript.
For gjenkjøring finnes den eksakte testkommandoen i TESTRESULT.md#baseline.
