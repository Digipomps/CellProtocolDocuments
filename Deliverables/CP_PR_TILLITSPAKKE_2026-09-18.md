# CellProtocol: draft-PR for tillitspakke-agentflaate — 2026-09-18

## Mål

Publisere `pdd/tillitspakke-agentflaate` uendret på `561d34a7ea785c087bd6036921f60debe6bace4a` som draft-PR mot `main`, måle lokalt bygg/test med SwiftPM-sandkassen deaktivert, og rapportere Linux-CI. Ingen merge, rebase, squash, nye commits eller endring av `main`.

## Påstander og evidensstatus

| Påstand | Målt status |
| --- | --- |
| Grenen er publisert uendret | Bekreftet: push exit `0`; fjern-SHA er nøyaktig `561d34a7ea785c087bd6036921f60debe6bace4a`. |
| PR mot `main` er opprettet som draft | Bekreftet: [PR #41](https://github.com/Digipomps/CellProtocol/pull/41), `OPEN`, `isDraft: true`. |
| Lokalt bygg fullfører | Bekreftet med `--disable-sandbox`, exit `0`. |
| Lokal testkjøring er grønn | Avkreftet i denne kjøringen: exit `1`, 1119 tester, 8 hoppet over, 14 feil. |
| Linux-CI er grønn | Ikke dokumentert. Manuell grenkjøring er fortsatt `in_progress`, uten konklusjon, ved siste kontroll 07:32:21 UTC. |
| PR-ens sammenslåing med `main` er verifisert | Ikke målt. GitHub rapporterer `CONFLICTING` / `DIRTY`; ingen automatisk `pull_request`-kjøring av Linux-workflowen er opprettet. |
| `main`, grenens commits og andre arbeidstrær er urørt | Bekreftet ved lokal før/etter-kontroll. Ingen merge er utført. |

## Opprydding og måleoppsett

`git worktree remove --force /private/tmp/cp-byggsjekk-20260917T204050Z` fullførte med exit `0`. Deretter ble `git worktree prune --verbose` kjørt; forhåndskontrollen viste ingen andre foreldreløse registreringer.

Bygg og test kjørte fra et nytt detached arbeidstre:
`/tmp/cp-pr-tillitspakke-20260918T071838Z/CellProtocol`.
HEAD var `561d34a7ea785c087bd6036921f60debe6bace4a`, og `git status --short` var tom før og etter kjøringen. Dette arbeidstreet ble deretter fjernet med vanlig `git worktree remove`. Alle andre registrerte arbeidstrær og deres HEAD-/grenopplysninger er identiske med før oppgaven.

Verktøykjede: Apple Swift 6.2.4 (`swiftlang-6.2.4.1.4`, `clang-1700.6.4.2`), target `arm64-apple-macosx28.0`.

## Lokalt bygg og tester

Begge kommandoene ble kjørt én gang fra det rene arbeidstreet:

```sh
Scripts/haven-swiftpm.sh -- build --disable-sandbox
Scripts/haven-swiftpm.sh -- test --disable-sandbox
```

| Måling | Bygg | Test |
| --- | --- | --- |
| Start, UTC | 2026-09-18 07:18:54 | 2026-09-18 07:22:56 |
| Slutt, UTC | 2026-09-18 07:22:36 | 2026-09-18 07:25:33 |
| Exit | `0` | `1` |
| Resultat | `Build complete! (217.24s)` | 1119 tester, 8 hoppet over, 14 feil (12 unexpected) |

Forrige forsøk stoppet før kompilering med manifest-sandkassefeilen som er dokumentert i [forrige rapport](CP_BYGG_561d34a_2026-09-17.md). Denne gangen kom bygg og testkompilering forbi manifestet. Det er derfor ikke korrekt å videreføre påstanden om at selve bygget fortsatt ikke lot seg fullføre.

Testfeilene fordeler seg slik:

- `AgentTrustPackageTests`: 9 feil ved lesing av fixture-filer fra det forventede søskenrepoet `CellProtocolDocuments`. Eksempel: `fleet-webfetch.package.json` / `fleet-webfetch.reach.json`, `NSCocoaErrorDomain Code=260`, under `Deliverables/PDD_tillitspakke-agentflaate_2026-09-08/contract/fixtures/`.
- `EntityRelationPerspectiveTests`: 1 feil ved lesing av fixture fra det samme forventede søskenrepoet (`Code=260`). Søskenrepoet var ikke kopiert eller lenket inn ved det isolerte arbeidstreet.
- `AppleIdentityVaultKeyStorageTests`: 3 feil. To rapporterer `failed to generate CDSA key` / `EPERM: Operation not permitted`; én rapporterer `unhandledError(status: -25291)`.
- `EntityScannerAgreementSurfaceTests.swift:75`: 1 assertion-feil: `EntityScannerCell.agreementTemplate` eksponerer nøklene `["radar", "select"]`, som testen ikke godtar. Dette er en konkret kontraktassertion og blir ikke forklart bort som sandkassefeil.

Ingen exit `64` forekom. Ingen retry var nødvendig etter cachevakten. `.haven-swiftpm-cache-v1` ble ikke fjernet manuelt. Ingen kildeendring eller testreparasjon er utført.

Fullstendig [bygglogg](CP_PR_TILLITSPAKKE_2026-09-18/build-attempt-1.log), [testlogg](CP_PR_TILLITSPAKKE_2026-09-18/test-attempt-1.log) og [uttrukne testfeil](CP_PR_TILLITSPAKKE_2026-09-18/test-errors.txt) er lagret sammen med rapporten. XCTest-oppsummeringen ovenfor gjelder hovedpakken; den etterfølgende Swift Testing-linjen om «0 tests» er ikke resultatet for de 1119 XCTest-testene.

## Push, PR og sammenligningsgrunnlag

Pushkommando:

```sh
git push origin refs/heads/pdd/tillitspakke-agentflaate:refs/heads/pdd/tillitspakke-agentflaate
```

Exit `0`; GitHub opprettet fjern-grenen. `git ls-remote` bekreftet SHA `561d34a7ea785c087bd6036921f60debe6bace4a`. Push skjedde mens testprosessen fortsatt kjørte; endelig testresultat forelå og var tatt inn før PR-en ble opprettet.

[PR #41](https://github.com/Digipomps/CellProtocol/pull/41) ble opprettet med `gh pr create --base main --head pdd/tillitspakke-agentflaate --draft`, exit `0`, kl. 07:26:29 UTC. Tittel:

> PDD tillitspakke-agentflaate: agent trust package, nearby proofs and node-model work

PR-body beskriver innhold, lokal måling og kravet om at PR-en forblir draft til Linux-CI er grønn. Den allerede installerte `/usr/local/bin/gh` kunne ikke kjøres (`bad CPU type in executable`, x86_64 på arm64). Offisiell `gh` 2.62.0 for macOS arm64 ble hentet fra `cli/cli` til oppgavens `/tmp`-mappe og kontrollert mot utgivelsens SHA-256-checksum. Ingen systeminstallasjon ble endret.

Oppgavens filantall måtte presiseres etter måling:

| Sammenligning | Resultat |
| --- | --- |
| Merge-base `f114ad6eb539c354dd6d88870166ae09a291dfa9` til grenen | **7 commits, 83 endrede filer**; 14698 innsettinger, 157 slettinger |
| Lokal `main` (`36372c5`) direkte mot grenen | **189 endrede filer** |
| `origin/main` (`b5b7282`) direkte mot grenen | **131 endrede filer** |

Tallet 189 er reprodusert, men gjelder ikke endringer fra merge-base. PR-en oppgir begge sammenligningsgrunnlagene eksplisitt.

## Linux-CI

GitHub rapporterer PR-en som `CONFLICTING` / `DIRTY`. Første oppslag etter PR-opprettelsen fant ingen `pull_request`-kjøring av `cellprotocol-swift-linux.yml`. Ifølge [GitHubs dokumentasjon](https://docs.github.com/en/actions/how-tos/troubleshoot-workflows) starter ikke `pull_request`-workflows når PR-en har merge-konflikt.

For å få Linux-måling uten å endre noen commits ble workflowens eksisterende `workflow_dispatch` brukt:

```sh
gh workflow run cellprotocol-swift-linux.yml --repo Digipomps/CellProtocol --ref pdd/tillitspakke-agentflaate
```

Dispatch fullførte med exit `0` kl. 07:27:27 UTC. [Kjøring 35319504345](https://github.com/Digipomps/CellProtocol/actions/runs/35319504345) har event `workflow_dispatch`, head `561d34a7ea785c087bd6036921f60debe6bace4a`, og status `in_progress` ved første kontroll kl. 07:27:46 UTC.

Dette er en Linux-måling av den publiserte grenen. Den verifiserer ikke en sammenslåing med dagens `main`. Workflowen kjører utvalgte Linux-kontrakttester og API-prober, ikke hele den lokale Apple-testpakken eller alle tillitspakketestene.

**Siste CI-status, 2026-09-18 kl. 07:32:21 UTC / 09:32:21 Europe/Oslo:** `in_progress`, tom `conclusion`. Både descriptor-testen og device-ingress-kompilering/-test har status `success`. Steget `Prove transport cannot invoke staged authority API` pågår; kontroll av uendret kilde/dependency-lock venter. Ingen samlet grønn CI-konklusjon foreligger ved overlevering.

En enkelt `gh run watch --exit-status --interval 15` ble observert i 180 sekunder. Bare den lokale watch-prosessen ble avsluttet ved tidsgrensen (`watch_exit: -15`); GitHub-kjøringen fortsetter. En siste `gh run view` ga statusen ovenfor. Se [CI-sluttmålingen](CP_PR_TILLITSPAKKE_2026-09-18/ci-final.json) og [watch-resultatet](CP_PR_TILLITSPAKKE_2026-09-18/ci-watch.json).

PR-kontrollen kl. 07:32:21 UTC bekreftet fortsatt `OPEN`, `isDraft: true`, riktig HEAD og `CONFLICTING`. PR-ens eneste rapporterte automatiske sjekk var `Notify PyCellProtocol`, `SUCCESS`; denne er ikke den etterspurte Linux-verifikasjonen. Den manuelle Linux-kjøringen og dens begrensning er også ført inn i PR-body.

## Ikke fullført og bevarte grenser

- Grønn samlet lokal testkjøring er ikke oppnådd; konkrete feil er oppgitt ovenfor.
- Endelig Linux-resultat forelå ikke innen observasjonsperioden. Kjøringen er overlatt til GitHub og er ikke kansellert; bruk kjøre-URL-en ovenfor for senere status.
- Automatisk PR-CI og verifikasjon mot sammenslått `main` er ikke oppnådd på grunn av merge-konflikt. Konflikten er ikke løst fordi grenen skulle publiseres uten nye commits eller omskriving.
- PR-en er fortsatt draft. Ingen merge, rebase, squash eller nye commits er utført.
- Lokal `main` står uendret på `36372c5b95a7b57fbef92ffa54dea13bdf75a9e6`; arbeidsgrenen står uendret på `561d34a7ea785c087bd6036921f60debe6bace4a`.
- CellProtocol hadde tre eksisterende untracked oppføringer (`Docs/EntityData-Review-2026-09-11/`, `LAZY_AUTH_REPORT.md`, `Losen_Administrert_Entitet_Design_2026-09-04.md`). Disse er urørt. Eksisterende endringer i CellProtocolDocuments er ikke staged, committet eller pushet; bare denne rapporten og dens evidensmappe er lagt til av oppgaven.

[Push-evidens](CP_PR_TILLITSPAKKE_2026-09-18/push.json), [PR-opprettelse](CP_PR_TILLITSPAKKE_2026-09-18/pr-create.json), [sammenligningsmåling](CP_PR_TILLITSPAKKE_2026-09-18/comparison.json) og [lokal sluttkontroll](CP_PR_TILLITSPAKKE_2026-09-18/final-local-state.json) er bevart for etterprøving.
