STATUS: LEVERT — PR https://github.com/Digipomps/CellProtocol/pull/53, commit 283cc3fecedcbb94505501feb24fd886c6dac763, CI grønn (https://github.com/Digipomps/CellProtocol/actions/runs/36309197281)

Sluttført 2026-09-27. Se AP1-4-CP.md for full rapport og AP1-4-CP-CI.json for eksakt CI-evidens. Kilderevisjon 4132c45a372c217e9a770bd7bd6b1b5639b9d50e; etterfølgende HEAD er kun verified-SHA-dokumentasjon. Kode og docs er pushet; ingen merge/deploy.

Full macOS CI: Executed 1345 tests, with 2 tests skipped and 0 failures (0 unexpected) in 33.336 (33.780) seconds
TSAN tre kjøringer uten feil. Begge Linux-jobber, kapasitetsmatrise og notify-jobb grønn på samme head. Lokal fulltest har tre rapporterte Keychain-sandkassefeil; lokale bridge/Lightweight153/0. Ingen tester er deaktivert.

Neste eier: Kjetil avgjør merge etter AP9a. Losen/konsumentarbeid må komponere innløpsporten før celleoppslag, migrere ready-only/native/Admin/entity-ruter ved CP-pin, konfigurere proxy/kvoter/revokasjon og bevise staging/readiness/AD. Dette er ikke prod-godkjenning. Ingen videre CP-arbeid står åpent i denne leveransen.
