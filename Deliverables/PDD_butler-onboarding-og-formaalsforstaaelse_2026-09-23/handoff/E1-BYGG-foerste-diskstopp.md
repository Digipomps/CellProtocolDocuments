STATUS: STOPPET — byggevakten avviste bygg med exit 75: 54,9 GiB ledig; etter 10 GiB reserve 44,9 GiB (4 %), under kravet om 5 %.

# E1 — byggforsøk 2026-09-29

Kjetils stoppregel er fulgt. Ingen celle, uttrekk, scorerendring eller nye tester er implementert. Ingen commit, push, PR, CI-kjøring, deploy eller merge er gjort. Semantisk differanse er **ikke målt**.

## Arbeidstre og kildegrunnlag

- `CellScaffold/_wt-butler-e1-20260929`, gren `pdd/butler-e1-formaalsgraf-celle`.
- Opprettet fra `origin/main` etter vellykket `git fetch origin main`.
- HEAD og baseline: `adf48d4615d1ed143d5bdc190fcf63e266214c8f`, samme kildecommit som E1-KART.
- Opprettet med `git worktree add --lock`; låst mot prune med begrunnelse om E1 og Kjetils gjennomgang.
- Arbeidstreet er rent. Andre arbeidstrær er ikke endret. Eksisterende lokale endringer i hovedutsjekkene er beholdt.
- E1-KART begynner med `STATUS: LEVERT`, så kartets stoppregel ble ikke utløst. E1-DESIGN v3 og Astras motsvar ble lest; migreringsplan, skjema og måleskript ble inspisert. Detaljert implementasjonskartlegging og full skjemavalidering er ikke gjennomført.

## Faktisk kjøring

Kjørt fra det nye arbeidstreet:

```sh
scripts/run_swift_bounded.sh test --disable-sandbox --filter ButlerGrafRoutingTests
```

Returkode: **75**. Faktisk utdata er bevart i [preflight.log](../maaling/rapport/e1-celle/preflight.log):

```text
Build capacity: 54.9 GiB free (5%); reserving 10 GiB leaves 44.9 GiB (4%).
ERROR: build blocked: projected free space must remain at or above 40 GiB and 5%.
```

`scripts/run_swift_bounded.sh:81` kaller kapasitetsvakten før SwiftPM-runneren. `scripts/check_build_capacity.sh:43` beregner prosentene som heltall; `:53` krever både minst 40 GiB og minst 5 % etter reserve, og `:55` returnerer 75. Disse filhenvisningene gjelder CellScaffold-baseline over. Ingen `HAVEN_BUILD_*`-overstyringer var satt. Ingen grense, cacheplassering eller runner ble endret. Swift-kompilering og tester startet ikke.

En etterfølgende `df -Pk` viste 971298980 KiB totalt og 57600000 KiB tilgjengelig. Dette er en separat måling etter avslaget, ikke bytepresis rekonstruksjon av vaktens måletidspunkt.

## Astras sju krav — status og manglende bevis

Ingen implementasjonsfil eller testmetode er opprettet. Derfor finnes ingen ærlige fil:linje-henvisninger til en E1-implementasjon. Test-ID-er nedenfor kommer fra bestillingen/designkontrakten; de er ikke påstått eksisterende Swift-metoder.

| Krav | Implementasjonsbelegg | Test/bevis som gjenstår |
|---|---|---|
| 1. Typede plasser, alle 17 funksjoner, uendret kontrollflyt | Ikke implementert | `test.reg.en-motor-i-kode` som uttrekkskontroll; grenprøver for første treff, lokale unntak og normalisering; før/etter-kallgraf |
| 2. Ordnet, tapsfri Butler-fasett og senere registerflytting | Ikke implementert | Hash-/read-back-kontrakt, endpoint/resource-skille og bevart rekkefølge; WP8 er fortsatt separat |
| 3. Særreglenes tillegg, gulv/tak, målflate og fase | Ikke implementert | Grenmatrise S01–S11 og P01/P02, generisk/eksakt og kontekstboost etter tak |
| 4. Ett snapshot per analyse og proveniens i forslag | Ikke implementert | Samtidige `analyzeDraft`, pekerbytte mellom await-punkter, grafhash og treffende plass-ID-er |
| 5. Full semantisk differanse og lukket port | Ikke implementert; måleskriptets avvik nedenfor | `test.lub.graf-i-celle-samme-tall`; v1, v2 og hele PromptPurposeLab; terskler, kontekst og historisk læring med læring av |
| 6. Hash-/rapportbundet CAS og egne rettigheter | Ikke implementert | `test.lub.dataendring-endrer-treff`, `test.lub.bytte-og-tilbakerull`; ikke-admin avvist separat for import, nominering, promotering og rollback; stale CAS og tilbakekalt hash |
| 7. E2/E6-grenser og gjenoppretting | Ikke implementert; ingen skygge lagt til | Snapshot-/evaluator-kontrakt, cache/hendelse/restart-prøver og proveniens fra vist forslag; senere skygge/utfall må ikke fremstilles som levert |

## Ikke kjørt

- Swift-bygg og alle Swift-tester, inklusive `ButlerGrafRoutingTests`, `ChatPurposeResourceRouterTests`, `ButlerSignalMatcherTests` og `PersonalChatPromptEvaluationTests`.
- `HAVEN_PYTHON=/usr/bin/python3 ci/check-value-literals.sh` og `ci/test-suite-coverage.sh`.
- `wp-butler-maaling-v3.sh` mot baseline eller celle; ingen resultatfiler eller sammenligningsrapport er produsert.
- Korpus v1 (396 linjer), v2 (264 linjer) og eksisterende `fixtures-v1.jsonl` (101 linjer). Linjetellingene er kun inventar, ikke validerte/målte saker; fixtureuttrekket er ikke full PromptPurposeLab-dekning.
- Alle nye import-, rettighets-, persistens-, CAS-, rollback-, samtidighets-, terskel-, lærings- og grenprøver.
- Uttrekks-/grep-test, staging-helse og CI.

## Statisk funn i måleskriptet — må håndteres før gjenopptakelse

Den leste `HAVEN-Deploy/_handoff/WP-R/wp-butler-maaling-v3.sh` oppfyller ikke denne bestillingens kjøregrenser uendret:

- `:17` binder et annet eksisterende arbeidstre; `:33` sjekker ut `Sources` der. Det kan ikke kjøres slik under «rør ikke andre arbeidstrær».
- `:39` legger til en testeksklusjon, og `:53` utelater PromptPurposeLab-saker med setup. Dette strider mot «ingen skips/exclusions» og full beslutningsdekning.
- `:61` kaller `swift build` direkte; `:65`, `:71` og `:86` kaller `swift test` direkte. Det går utenom pålagt bounded runner og kapasitetsvakt.
- `:25` returnerer exit 0 fra `stopp`; sluttgrenen for lukket port gjør også dette. `:71` lagrer ikke korpuskallets exitstatus, og `:66` gjør manglende katalog til rapporttekst. Prosesskode 0 eller en eksisterende rapport kan derfor ikke være bevis for bestått E1-port.

Dette er kildeinspeksjon, ikke en kjørt feilinjeksjon. Skriptet er ikke endret eller startet. Ved gjenopptakelse må måleløpet få eksplisitte, isolerte kilder, bounded kjøring, full fixturedekning og håndhevet feilstatus før det kan brukes som E1-bevis. [Kapittel 38](../../../Book/38_Measuring_Purpose_Understanding_Without_A_Model.md) er oppdatert med denne begrensningen gjennom læringsfangst.

## Gjenopptakelse og opprydding

Først må diskforutsetningen oppfylle den uendrede byggevakten. Deretter kan oppgaven fortsette i det låste arbeidstreet, etter kontroll av kilde- og arbeidsstatus. Ingen ny beslutning om alternativ A/B eller PDD-godkjenning er nødvendig for den allerede bestilte E1-implementasjonen.

Ingen egne midlertidige kataloger under `/private/tmp` ble opprettet; det er ingenting fra dette forsøket å slette der. Ingen annen tråds cache eller arbeidstre er ryddet. Læringsfangsten gjelder måleverktøyets observerte begrensninger; dataflytting mellom celler er ikke implementert eller verifisert.

Læring `L-2026-09-29-wp-butler-maaling-v3-sh-er-ikke-en-tilstrekkelig` er fanget, anvendt i kapittel 38 og behandlet med `sync` (dokumenter distribueres med Git; ingen dokumentpublisering er gjort her). Den globale `haven_learn.py check --strict` returnerte 1 på grunn av to andre læringsposter: én åpen om tmp-rydding og én ikke distribuert om scanner-tester. Disse postene er ikke endret av E1. Rapportens lokale lenker, fravær av brukersti/IP/e-post og rent E1-arbeidstre er kontrollert.
