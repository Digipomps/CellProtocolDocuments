# CS17-R2: cachekollisjon avklart, ny kjøring venter

Status2026-10-14: baseline116/116 ogCP8/8 er grønne. CS17 har fortsatt null teststarter.
Kjetil sa «Ja, kjør» i Claude-køtråden07:58:26Z (registrert approvalMessage
cmsg_013NgqC72PRtRb8tu7xHs7YT4Jc3BYVJvG59qXWHAmRv9s). Køeieren bandt ja-et
til endeligR1-manifest102f0277…157d5 og startet08:00:04Z. R1 stoppet08:01:31Z,
faseexit75, før Swift fikk cachelåsen. Diskgrensen besto:122,9GiB/13prosent etter reserve.

Rålogg: `HAVEN-Deploy/_handoff/ARBEIDSBENK/G2-W1-CS17-R1-20261014/cs-tests.log`.
Cache28516ddea851 hadde en levende lease:PID14793,start09:46:50lokal,
kommando `haven-swiftpm.sh ... test --jobs 2 --filter CommonsLibrarianCellTests|KallimachosAdvisorCellTests`.
Lesende ps bekreftet prosessen og lsof viste aktive Swift-filer i sammecache.
Tom kø var dermed ikke et ledig byggvindu. Ingen prosesser/låser ble fjernet.

## Konkret ny pakke

`HAVEN-Deploy/_handoff/ARBEIDSBENK/G2-W1-CS17-R2-20261014/`.
Manifest `66a86e662bd3f77617df76ef2bf504bf87fff5f6a5416ea25fa4b4dd92153364`. Samme968-fil CP-kopi med korrekt mappenavnCellProtocol,
sammeCS-kilde og17tester, ingen produkt-/testendring. Gamle pakker bevares.
Ny tidlig lesende cachekontroll stopper før attempt-started når en lease finnes.
Den ordinære runneren beholder atomisk låsing og open-file-kontroll; forhåndskontrollen
er ikke i seg selv eksklusivitet og hindrer ikke en ny konkurrent fra å starte senere.
Køeieren må derfor avstemme også bygg utenfor køen før ferskADMISSION.
Queue-konvolutt har eksplisitt tom cwd-linje før run-argumentet.

Kontrollert i begge locale: check grønn, cache-check avviser aktivlease førforsøk,
run avviser manglendegodkjenning. Ingen Swift, ingenADMISSION/attempt/result iR2.
ForrigeR1 er konsumert; ingen automatisk rerun. Nytt eksplisitt ja gjelder énR2-kjøring
av bare17tester etter frigittcache og køeiers ferske eksklusivevindu. 40GiB OG5prosent
etter10GiBreserve,2jobber, sammeadministrertecache. Ingen CI/push/deploy.
Ved grønt fortsetter alleredeG2-godkjent prosjektflate, inkludert Butler fraalleflater.
Oppfølgingen erPAUSED inntil gyldig videreautorisasjon. Pakkeidentitetsrettelsen er
fortsatt ikke runtime-verifisert fordi cachevakten stoppet før Swift.
