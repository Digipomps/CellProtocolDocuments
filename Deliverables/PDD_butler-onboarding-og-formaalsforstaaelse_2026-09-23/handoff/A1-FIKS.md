STATUS: STOPPET — byggevakten avviser videre bygg ved 55,7 GiB ledig (exit 75); rød baseline fullført, produksjonskode uendret, ingen PR.

# Butler A1 — runde 3, 2026-09-29

Utfører: Codex. Integrator: Kjetil. Handoff til Losen.
Work ID: `butler-a1-onboarding-steg-20260929`.
Forrige rapporter er bevart i `A1-FIKS-runde1-20260929.md` og
`A1-FIKS-runde2-20260929.md`. Runde 1-arkivet er urørt; runde 2 er arkivert byte for byte.

## Faktisk fremdrift

- Arbeidstre: `CellScaffold/_wt-butler-a1-20260929` (HAVEN-relativt).
- Gren: `pdd/butler-a1-onboarding-steg`.
- HEAD/base: `adf48d4615d1ed143d5bdc190fcf63e266214c8f`.
- Hentet `origin/main`: `fdf1ce8e1713ac467ebca1e44707225175e72dc4`.
  Ingen forskjell i berørte produksjonsfiler eller pakkepinner mot basen.
- Alle 16 nye regresjonstester fra runde 1 og 2 er nå kompilert og kjørt røde
  mot uendret produksjonskode. Ingen testkode måtte rettes for å kompilere.
- Totalt 149 tester: 133 passerte, 16 feilet. XCTest teller 17 feilregistreringer
  fordi den nye chat-testen har to mislykkede asserts.
- Chat-testen med virkelig resolver og knappens eksakte payload gjenskaper
  `guided_onboarding_step_rejected — onboarding.start: notFound`.
- De to andre onboarding-testene og alle 13 søstercelletestene kaster `notFound`.
- Produksjonskode, CellProtocol/GeneralCell, Package.resolved, skips og exclusions
  er uendret. Ingen produksjonsretting, ettertest, commit, push, PR, CI, merge eller utrulling.

Detaljert og persondatafritt testbevis:
[råbaseline-sammendrag](../evidence/A1-runde3-red-summary.md).
Råloggen beholdes lokalt under filnavnet `butler-a1-runde3-red.log` i maskinens
midlertidige katalog, ikke i offentlig repo.

## Byggevakten — stoppgrunn

Første kjøring slapp gjennom med 62,9 GiB ledig, 52,9 GiB etter reserve (5 %).
Cache-eierskapsfeilen fra runde 1 kom ikke tilbake. Runneren brukte sin forvaltede
cache med standard jobbgrense og uendrede terskler.

Etter fullført rød kjøring ble kapasiteten kontrollert før videre arbeid:

```sh
scripts/check_build_capacity.sh .
```

Exit 75:

```text
Build capacity: 55.7 GiB free (6%); reserving 10 GiB leaves 45.7 GiB (4%).
ERROR: build blocked: projected free space must remain at or above 40 GiB and 5%.
```

Arbeidet stoppet her etter Kjetils uttrykkelige beskjed. Ingen omgåelse,
markørskriving, cachebytte, rydding eller avbrytelse av andre jobber.
Runneren rapporterte cachevekst på 6555052 KiB og 7600000 KiB mindre ledig plass
på filsystemet. Sistnevnte er en samlet filsystemmåling, ikke bevis for at alt
forbruket stammer fra denne jobben.

En senere ren `df`-avlesning viste 56,458 GiB; kapasiteten svinger. Minstegrensen
på dette filsystemet er cirka 56,315 GiB, inkludert reserven. Ingen ny vakt- eller
byggkjøring ble startet etter blokkeringen, og den senere avlesningen opphever
ikke stoppen. Ny runde trenger kapasitet med margin gjennom ordinær drift.

## Kontroller i runde 3

| Kontroll | Resultat |
|---|---|
| `scripts/run_swift_bounded.sh test --disable-sandbox --filter 'GuidedOnboarding\|PersonalCopilot'` | Exit 1 etter vellykket kompilering; 149 tester, alle 16 nye røde, øvrige 133 grønne |
| `HAVEN_PYTHON=/usr/bin/python3 ci/check-value-literals.sh` | Exit 0; selvtester grønne, 22 eksisterende literaler dekket av baseline |
| `ci/test-suite-coverage.sh` | Exit 0; 343 suiter, 323 dekket av filter, eksisterende unntak uendret |
| `git diff --check` | Exit 0 |
| Produksjonskode, manifest og låsfil mot HEAD | Ingen diff |
| `scripts/check_build_capacity.sh .` etter rød kjøring | Exit 75; 55,7 GiB ledig |

Dekningskontrollen teller filterdekning. Det fulle lokale CI-filteret er ennå
ikke kjørt. Det ble ikke brukt skip-argumenter i den røde kjøringen.
Søstersuitens negative tilgangsasserts kommer etter første gjenopprettede lesing
og ble ikke nådd; disse må faktisk bli grønne etter rettingen.

## Rettingen — gjenstår

Den dokumenterte feilen er nå reprodusert lokalt. Dette beviser ikke alene
livssyklusen til den tidligere prodinstansen. Kildekjeden fra runde 1 består:
dekodet eier uten hvelv → setup uten runtime-installasjonstoken → manglende
handler → `notFound` ved bruk med bevist eier.

CellProtocol-pinnen har allerede `installCellRuntimeBindingsForAccess`,
instansbundet installasjonstoken og serialisert readiness. `PublicationCell`
bruker dette mønsteret i CellScaffold. Det er fortsatt grunnlag for en lokal
retting uten endring i GeneralCell, men selve rettingen er ikke implementert.

Neste utfører:

1. Bevar eget WIP og arbeidstreet. Sørg for kapasitet gjennom godkjent drift;
   vakten, jobbgrensen og cachevalget skal ikke omgås.
2. Den røde baselinen finnes nå i bevisfilen. Kontroller at produksjonskoden og
   testene fortsatt matcher før den brukes som før-bevis.
3. Flytt handlerinstallasjonen i GuidedOnboarding og de persisterte søstercellene
   til eksisterende runtime-hook i CellScaffold. Bruk lagret eierbeskrivelse kun
   under den autoriserte installasjonen; behold eierbevis og tilgangskontroll ved bruk.
4. Gjenopprettingstesten omfatter allerede 13 søstertyper, inkludert den arvede
   `purposeGoal`-veien i AccountContinuityPersonalChatHubCell. Behold de negative
   testene, og utvid handling/persistens der det er nødvendig.
5. Følg lokal AGENTS-regel dersom PersonalPagePublisherCell endres: dens
   eksisterende literal på 21 felt må deles opp og baseline senkes.
6. Kjør fokuserte grønne tester, hele avtalt lokalt CI-filter, literalvakt,
   testdekning og diff-kontroll uten nye skips/exclusions. Ingen CellProtocol-endring
   i denne jobben; stopp med begrunnelse hvis den kreves.
7. Etter lokal verifikasjon: commit med `PDD_butler-onboarding-og-formaalsforstaaelse_2026-09-23`
   og A1 samt de to Claude-trailerne fra Kjetils prompt; push, ordinær PR mot main,
   vent på CI maks 60 min. Kjetil merger selv. Oppdater første linje med PR, head og CI-run.

## Eget WIP og læring

Testene og CI-filteret fra runde 2 er uendret. Kun dokumentnotatet i
`Documentation/PersonalCopilotV1_PurposeEvaluationAndPlan.md` er oppdatert med
målt rød baseline og ny stoppgrunn. Læringen følger dette dokumentmålet og
bevisfilen; ingen produksjonsatferd omtales som rettet.

Læringspost `L-2026-09-29-butler-a1-har-na-kjort-rod-baseline-med-ekte` er
markert applied; sync er kjørt og angir Git som distribusjonsvei for dokumentet.
Dette er fortsatt lokal WIP, ikke publisering. `check --strict` returnerte exit 1
på to andre åpne læringer og seks andre poster som venter på distribusjon.
Disse postene og målene deres er ikke endret i denne jobben. Nytt rapportinnhold
og dokumenttillegg er kontrollert for brukerstier, IP-er, e-post, konkrete
identitetsverdier og kjente nøkkelmarkører uten treff.
