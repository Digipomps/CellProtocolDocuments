STATUS: STOPPET — HVELV-F5-F9.md er STOPPET; arbeidstreet har sporede endringer og usporede F1-utkast, head b658ef53e14dccdb12009991e78b1b44d47dac8a

Codex, 29.09.2026, for Kjetil og Losen. Arbeidsreferanse `PDD_sindre-import-uten-bruker_2026-09-25.F4`. Ingen implementering, bygg, testkjøring, commit, push eller merge utført. Forrige rapport er bevart byte-identisk som [HVELV-F4-runde1-20260928.md](HVELV-F4-runde1-20260928.md).

## Inngangskontroll

Forrige jobb, [HVELV-F5-F9.md](HVELV-F5-F9.md:1), har første linje `STATUS: STOPPET`, datert 29.09.2026. Brukerens uttrykkelige instruks er: «Er den STOPPET: stopp og rapporter.» Dette alene stopper F4. Forgjengerrapporten viser til STOPPET F1: uavhengig eierforankring fra Kjetils Mac mangler. Valget av eieranker er allerede avklart; denne jobben har ikke inspisert nøkkeloppsettet eller implementert tillitskjeden på nytt.

Arbeidstreet `CellScaffold/_wt-forvaltet-import-20260926` står på grenen `pdd/forvaltet-kunstnerimport`, lokal HEAD `b658ef53e14dccdb12009991e78b1b44d47dac8a`. Git-status er:

```text
 M Documentation/Operations/Managed_Artist_Import_2026-09-28.md
 M ci/test-filter.txt
?? Sources/App/Cells/ManagedArtistImport/ManagedArtistRecipientBinding.swift
?? Tests/AppTests/ManagedArtistRecipientBindingTests.swift
?? scripts/managed_artist_recipient.py
?? scripts/test_managed_artist_import.sh
?? scripts/tests/test_managed_artist_recipient.py
```

De sporede endringene utløser også regelen om rent arbeidstre. De usporede filene er dokumentert som F1-utkast i forrige rapport, ikke egne testrester. Ingen usporede testrester forelå i Git-statusen. Ingenting er flyttet til `_to_delete/`, slettet, stashet eller overskrevet i PR-arbeidstreet. `gh pr view 270 --json number,url,headRefName,headRefOid,state` bekreftet at [PR #270](https://github.com/Digipomps/CellScaffold/pull/270) er OPEN på samme gren og SHA som lokal HEAD.

## F4: ingen retting eller nytt testbevis levert

F4-kravene er lest i [ASTRA-HVELV.md](ASTRA-HVELV.md:50) og [ASTRA-HVELV-2.md](ASTRA-HVELV-2.md:129). Filankrene og testnavnene nedenfor er videreført fra forrige F4-rapport og Astra, på samme SHA. De er ikke nye kilde- eller runtimeverifikasjoner fra denne stoppede jobben.

| Del av F4 | Fil:linje | Eksisterende test / ville fanget den manglende dekningen? |
|---|---|---|
| Kald gjenstart av alle lagre ved mandatforbruk, utstedelse og eierskifte | `Tests/AppTests/ManagedArtistImportTests.swift:257`, `:393`; `Sources/App/Cells/ManagedArtistImport/ManagedArtistIssuanceVault.swift:506`, `:541`, `:609` | `testVaultReloadAndGenericIssuanceDenied` laster bare hvelvet på nytt. `testInterruptedClaimHidesBothCellsAndCanResumeSameClaimant` fortsetter med samme runtime og celleobjekter. Nei: de dekker ikke den etterspurte kalde gjenstarten. Ingen konkret original restartfeil er påvist, og ingen ny regresjons- eller mutationstest er kjørt. |
| Virkelig ekstern klient over planlagt transport og klientlokale private nøkler | `Tests/AppTests/ManagedArtistImportTests.swift:637`; `Documentation/Operations/Managed_Artist_Import_2026-09-28.md:46` (driftsanker fra Astra) | `ManagedArtistTestSigningBridge` er en fixture i testprosessen, ikke en ekstern klienttest. Nei: dette beviser ikke transportløypen eller eierens signering på egen enhet. Ingen ekstern test kjørt. |

Gjenstår etter at forgjengerjobben og inngangstilstanden er avklart:

- Ny prosess og reload av mandat, issuance-hvelv, Publication og ArtistSales ved alle lagringsgrensene i ASTRA-HVELV-2: etter mandatforbruk før issue, etter issue/under import, etter `transferring`, etter ArtistSales, etter Publication og før/etter terminalt snapshot.
- Skjulte flater under ufullført overføring; samme mottakers gjenopptakelse; avvist annen mottaker og replay; nøyaktig én utstedelse; varig key retirement/tombstone. Dokumenter tilfellet der mandatet er forbrukt uten issuance-record.
- Virkelig ekstern klient med testidentitet, faktisk planlagt transport, fingeravtrykk på begge enheter, eierens engangsbinding signert på egen enhet og fersk kunstnersignatur fra den bundne nøkkelen. Ingen privat eier- eller kunstnernøkkel på serveren.

## Ikke kjørt og videre overlevering

Ikke kjørt: isolert runtime, kald gjenstart, ekstern klient, privatnøkkelinspeksjon, `scripts/run_swift_bounded.sh … --disable-sandbox`, `HAVEN_PYTHON=/usr/bin/python3 ci/check-value-literals.sh`, `ci/test-suite-coverage.sh` eller CI-venting. Ingen skript er opprettet under `HAVEN-Deploy/_handoff/SINDRE/`: arbeidet stoppet ved den uttrykkelige forgjenger-/arbeidstregaten, før en eventuell sandkassebegrensning kunne undersøkes. Dette er ikke dokumentasjon på at en slik kjøring krever arbeid utenfor sandkassen.

ASTRA-rapportene, forgjengerrapporten, FORMAALSSPEC, PLAN og driftsnotatet er åpnet; forgjengerrapporten og F4-avsnittene i begge ASTRA-rapportene er lest særskilt. Full videre innlesing og implementeringsanalyse er utsatt på grunn av stoppregelen. Sentralhvelvets strict-oppførsel, avvisningstester, skips/exclusions og byggevakt er ikke endret av denne jobben. Ingen historisk grønn CI brukes som F4-bevis.

F1-utkastene må håndteres av deres eier, og F5–F9-jobben må avklares, før F4 tas opp igjen med ny kontroll av forgjengerrapport, rent arbeidstre og gjeldende PR-head. Rapporten gir ingen autorisasjon til å rydde bort utkastene.

Docs-repoet har omfattende eksisterende WIP, inkludert hele denne PDD-mappen som usporet. Bare denne rapporten og arkivkopien av forrige rapport er skrevet der; øvrig WIP er urørt. Rapporten er lokal og ikke committet/pushet. Læringsfangst registreres med `none`: dette er en kjent inngangsblokkering allerede dekket av brukerens stoppregel og eksisterende samarbeidsregler.
