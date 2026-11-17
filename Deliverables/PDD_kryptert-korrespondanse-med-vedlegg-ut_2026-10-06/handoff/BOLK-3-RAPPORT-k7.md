# Bolk 3 og 5 — k7: broretting pinnet og 100 brotilfeller grønne; fullport blokkert av diskvakten

CP-HODE: 7ebb4f5f76cdcda39a2abc2e42c8743a62a703b0
Klientgren: `codex/korr-klient-20261007`. Videreført ucommittet k6-arbeid.

## Krav, prøve og resultat

| Krav | Test | Utfall | Bevis |
| --- | --- | --- | --- |
| Vent på p6 og grønn CP-CI | Ferdigmarkør; PR63-BRO-LEASE-RAPPORT; direkte GitHub-kontroll på eksakt hode | LEVERT; 5/5 SUCCESS, PR63 fortsatt åpen kladd | p6/ci.json og p6-rapporten |
| Bevar k6 før overskriving | Bytekopi og SHA-256 | BOLK-3-RAPPORT-k6.md bevart; hash nedenfor | Backup og k7-verification-summary.json |
| Pinne klienten til brorettet CP | Manifest, lockfile og faktisk managed-checkout HEAD | Alle peker på CP-HODE; andre dependencyrevisjoner bevart | Package.swift, Package.resolved, checkout-kontroll |
| 100 authenticatedVaporBridgeDeliversEnvelopeWithoutPolling | Opprinnelig Vapor-topologi, k6-buffering, alle assertions beholdt; 0..<100 | 100/100 tilfeller, 0 issues, exit 0; 21,717 s testtid | k7-buffered-private.log og køjobb b-k7-buffered-20261009 |
| Full lokal port før commit/push | Ny kontroll med uendret check_build_capacity | BLOKKERT, exit 75; fullport ikke startet | k7-full-capacity.log |
| Commit, push, kladd-PR og klient-CI | Krever grønn fullport | Ikke utført; ingen PR på klientgrenen ved GitHub-kontroll | Ingen ny commit/PR/CI hevdes |
| Ren eksport, Developer ID, universal2, notarisering, staple, sha256 | Krever grønn klient-CI | Ikke utført; ingen ny installer eller installerhash | Ingen pakkebevis |
| Native admin fra k3 | Krever grønn produkt- og GUI-akseptanse | Ikke tatt inn som levert admin; se begrensninger | Ingen ny native GUI-akseptanse |

Alle k7-bevis ligger under `HAVEN-Deploy/_handoff/KORR-UT/bolk3/`.
Backupens SHA-256: `d068bc0f4ce94899cc5932782831286e432f3c1f1f1c80e0d0c082ccdef347df`.

## Hva broprøven viser

Prøven bruker samme lokale Vapor-socket som k6-buffered, med autentisert kanal,
Flow-push uten polling og kontroll på at vertsvaulten ikke har deltakerens
private nøkkel. Også negative vault-cache-, shutdown- og factorytilfeller er
beholdt. Antall argumenttilfeller er økt fra 20 til 100; ingen assertion er
slettet eller svekket. Dette er ikke en automatisk retry av mislykkede tilfeller.
Separat k6-lease-diagnostikk forblir under `Evidence/k6/`, utenfor produktkode
og akseptansetarget. CP-arbeidstreet er rent og uendret av k7.

## Stoppgrunn og videreføring

Før brobygget viste uendret vakt 58,3 GiB ledig; etter 10 GiB reserve var både
40 GiB- og 5 %-kravet oppfylt. Etter kompileringen viser ny vakt 54,2 GiB ledig,
44,2 GiB etter reserve og bare 4 % prosjektert ledigandel. Derfor exit 75.
Den delte cachen rapporterte 14 932 188 KiB mot eksisterende cap 12 582 912 KiB.
GC-adapteren var fortsatt dry-run; ingen cache eller annen fil er slettet.

Det må være nok ledig plass til den eksisterende vakten før neste bygg. K7
endrer ikke vakt, reserve, cap eller leie. Fullportskriptene er forberedt, men
ikke lagt i kø eller kjørt: `wp-k7-full.sh` og `wp-k7-swift-and-tests.sh` under
samme KORR-UT-handoff. De beholder bounded-runneren og legger til helperprøver
og daemon smoke i fullporten. Shellsyntaks og diff-hygiene er grønne; dette er
ikke fullportevidens. En direkte Python-helperprøve inne i sandbox feilet på
nektet `/bin/ps`; fire prebuilt-helperprøver bestod. Ingen produktfeil utledes
av sandbox-nektelsen, og helperporten på verten er fortsatt ikke kjørt i k7.

Videre rekkefølge: uendret diskvakt grønn, full klientport grønn, avgrenset
commit med ønsket co-author, push og kladd-PR, eksakt klient-CI grønn, så ren
eksport og signert/notarisert/staplet universal2-pakke med hash etter staple.

## PR28 og PR30

Ny GitHub-inventar viser begge fortsatt åpne: PR28 kladd på `5cf3531`, PR30 på
`653fb87`. K1-anbefalingen beholdes: CI-fasevakten og direkte Swift Testing-
løperen er videreført i kandidaten; PR28s separate provenance-funksjon bør
skilles ut/rebases. PR30 bør rebases på verifiserte helpere og få ny full CI før
merge. Main-historikken viser røde kjøringer på `ea558ba`; dette er ikke ny
klient-CI. Ingen merge, lukking eller endring av disse PR-ene er utført.

## Ikke vist eller levert

- Fullport mot ny pinne, klientcommit, kladd-PR og grønn klient-CI.
- Ny universal2-installer, signering, notarisering, staple eller installer-SHA-256.
- Native adminvindu, ekte LAContext, innmelding/fornyelse etter utløp og GUI-akseptanse.
- Samlet formålsprøve mot faktisk PR286-vert og tre adskilte vaults.
- Intel-kjøring og oppsett på en ren mottaker-Mac.
- Isolasjon av nøkkellager mot andre prosesser med samme OS-bruker.

Ingen CP-endring, sletting, diskvaktendring, merge, deploy eller sending.
Læringsfangst er registrert som none: eksisterende dokumenterte grenser og
arbeidsmåter ble brukt; kandidatens testresultater er bevart som evidens.

STATUS: STOPPET — uendret diskvakt blokkerer fullport; broprøven 100/100 er grønn.
