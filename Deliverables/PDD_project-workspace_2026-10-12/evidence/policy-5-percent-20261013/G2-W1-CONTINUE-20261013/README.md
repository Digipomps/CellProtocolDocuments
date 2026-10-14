# Workbench Entity — avgrenset fortsettelse

Forberedt 2026-10-13. **Venter på eksplisitt godkjenning av nytt forsøk og køeiers admission. Ikke kjørt.**

Den forrige pakken beholdes uendret. CP8 var grønn (0 feil, prosesskode 0);
parseren feiltolket forventede journal-avvisninger som testfeil og stoppet før CS17.
Denne pakken kjører de samme 8 + 17 testmetodene mot identiske kildebytes og pins.
Den endrer ingen test eller produktkode og verifiserer alle manifester før/etter.

Rettet parser krever eksakt startet/bestått metodeinventar, avsluttede suiter,
null feil i alle sammendrag og prosesskode 0. Applikasjonens forventede
avvisningslogger er ikke XCTest-verdict. Avvisninger, manglende resultat,
duplikater, compilerfeil, signal og feil antall dekkes av offline-fixtures.

Samme administrerte cachefamilier, to Swift-jobber, 10 GiB reserve, 40 GiB/10 %.
GC er report-only etter den dokumenterte kollisjonen i korrespondansejobben k17.
Ingen sletting av byggcacher eller ny scratch. Bevarer eget og andre arbeidstrær. Package.resolved
kan bare få den forventede lokale CP-pin-fjerningen og gjenopprettes byte for byte.
Prosesskontrollen gjenbruker de reviderte OwnedPopen/child_exec-primitivene og
signalbarrierene fra AUDIT-CP-20261012-R1; pins gjenopprettes først etter tom gruppe.
SIGKILL, strømbrudd og prosesser som lager ny session er ikke dekket av dette beviset.

Aktivering: Køeier skriver fersk ADMISSION.json (jobID, coordinator,
exclusiveBuildWindow=true, expiresAt) og aktiverer én gang i inbox-g2, etter at
AUTHORIZATION.json binder Kjetils uttrykkelige ord til manifestSHA256. Den nyeste
G2-godkjenningen gjelder prosjektflaten; den registreres ikke som et nytt CP-ja.
Et rødt resultat stopper kjeden uten automatisk omkjøring. Ingen betalt CI/PR/deploy.

Forberedelseskontroll: bash wp-g2-w1-continue.sh check. Dette kjører ingen Swift,
tar ikke et byggvindu og forbruker ikke forsøket.
