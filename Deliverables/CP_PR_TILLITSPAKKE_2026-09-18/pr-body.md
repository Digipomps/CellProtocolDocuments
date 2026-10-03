Publiserer grenen uendret på `561d34a7ea785c087bd6036921f60debe6bace4a`: agent trust package og effektkvitteringer, nearby proofs/radar, node-/relasjonsmodell, CorrespondenceCell, attachmentStreamV1, lokalisering og tilhørende tester/dokumentasjon. Ingen rebase, squash eller nye commits.

Grenen har **7 commits og 83 endrede filer fra merge-base** `f114ad6`. Oppgavens tall på **189 filer** gjelder direkte sammenligning mellom lokal `main` (`36372c5`) og grenens HEAD, ikke merge-base. Direkte sammenligning mot dagens `origin/main` (`b5b7282`) gir 131 filer.

Forrige lokale bygg lot seg ikke fullføre i agent-sandkassen: SwiftPM stoppet før kompilering med `Invalid manifest` / `sandbox-exec: sandbox_apply: Operation not permitted`. Ny måling 2026-09-18 fra rent arbeidstre på samme SHA:

- `Scripts/haven-swiftpm.sh -- build --disable-sandbox`: **exit 0**, bygg fullført (SwiftPM: 217,24 sekunder).
- `Scripts/haven-swiftpm.sh -- test --disable-sandbox`: **exit 1**; 1119 tester, 8 hoppet over, 14 feil (12 unexpected). Ti feil gjelder manglende fixture-filer i forventet `CellProtocolDocuments`-søskenrepo; tre gjelder Apple-nøkkellagring (`EPERM` / status `-25291`). Én assertion i `EntityScannerAgreementSurfaceTests.swift:75` avviser de eksponerte nøklene `radar` og `select`.
- Ingen exit 64; ingen retry eller manuell fjerning av cachemarkøren.

`cellprotocol-swift-linux.yml` på Linux er den gjeldende CI-verifikasjonen. **PR-en skal forbli draft til denne CI-en er grønn.** Det er foreløpig ingen påstand om grønn CI eller grønn samlet testkjøring. Ingen merge eller endring av `main` er utført.

CI-status 2026-09-18 kl. 07:32:21 UTC: GitHub rapporterer `CONFLICTING` / `DIRTY`, og ingen automatisk `pull_request`-kjøring av Linux-workflowen er opprettet. [GitHub kjører ikke slike workflows ved merge-konflikt](https://docs.github.com/en/actions/how-tos/troubleshoot-workflows). Samme workflow er derfor startet manuelt på uendret gren/SHA: [Linux-kjøring 35319504345](https://github.com/Digipomps/CellProtocol/actions/runs/35319504345), event `workflow_dispatch`, fortsatt **in_progress** uten samlet konklusjon. Descriptor- og device-ingress-teststeg har bestått; API-proben pågår. Kjøringen fortsetter. Dette måler grenens Linux-kontrakter, ikke en sammenslåing med dagens `main` eller hele Apple-/tillitspakketestpakken. Konflikten er ikke løst fordi grenen skal bevares uten nye commits eller omskriving.
