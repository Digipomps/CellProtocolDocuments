# Entitetsutvidelse — 2026-09-28

**Status: blokkert før implementasjon. Oppgaven er ikke levert.**

Hele [kapittel 32](../Book/32_Cross_Scaffold_Entity_Enrollment.md) er lest.
Det er fortsatt spesifikasjonen; denne rapporten er ingen ny spesifikasjon.
Ingen kildekode eller tester er endret i denne runden. Grunnbygget kunne ikke
fullføres i kjøremiljøet. Eierens stoppregel ble derfor fulgt før implementasjon.

## Mål

Eieren skal kunne bruke samme entitetsdata fra staging, prod og andre eksplisitt
innrullerte scaffolds, med ett kanonisk hjem per datadel. Tilgang skal følge
aktiv innrullering og avgrenset kapabilitet. Cache og backup skal være navngitte,
kontrollerte unntak uten skriveautoritet. Bestillingen er §9 punkt 1–5.

## Påstand og belegg

| Påstand | Belegg / avgrensning |
| --- | --- |
| Entitetsutvidelsen virker etter denne runden. | **Ikke påvist.** Ingen ny implementasjon, vellykket bygg eller testkjøring. |
| Eksisterende kode går lenger enn implementasjonskartet i §8. | Kildeinspeksjon av innchecket `EntityScaffoldEnrollmentCell.swift` viser `EntityHomePolicy`, `entityHomePolicy.set`, `entityData.get` og `entityData.set`. Dette er eksisterende arbeid, ikke denne leveransen. |
| Eksisterende policy håndhever én-sannhet-regelen fullt ut. | **Ikke støttet av inspisert kode.** Datatilgangen leser ikke hjemme-policyen; modellen mangler plassering per datadel og eksplisitte cache-/backup-unntak. |
| De seks bestilte testene er grønne. | **Ikke påvist.** Alle seks er ukjørt i denne runden, se tabellen nedenfor. |

Kildegrunnlag: `CellScaffold` HEAD
`942965ca24e9a418b531f9514c1da75d6d529e30`. De to inspiserte filene
`Sources/App/Cells/EntityScaffoldEnrollment/EntityScaffoldEnrollmentCell.swift`
og `Tests/AppTests/EntityScaffoldEnrollmentCellTests.swift` hadde ingen lokale
endringer. Arbeidsområdet ellers hadde mange eksisterende endringer, inkludert
pakkeoppsett. Byggforsøkene gjelder dette arbeidsområdet, ikke en ren HEAD.

Konkrete observasjoner fra cellefilen:

- Linje 129: eksisterende `EntityHomePolicy` ligger i samme fil som enrollment.
- Linje 623: policy kan settes med eierkontroll og serialiseres med cellen.
- Linje 755: `entityDataAuthorization` kontrollerer blant annet lenkestatus,
  requester, offentlig nøkkel og kapabilitet. Den kontrollerer ikke
  hjemme-policy, formål/audience for dataoperasjonen eller et signert
  operasjonspayload med replay-vern for skriving.
- Linje 851: `ownerEntityAnchor` bruker payload/lenkereferanse og resolver med
  eieridentitet. Policyens valgte hjem styrer ikke denne avgjørelsen.
- Linje 674 og 1058: skriveveien kaller `emitLifecycle` etter skriving. At hvert
  fjernskrivekall gir korrekt observerbart FlowElement er ikke verifisert her.
- Linje 1520: policyparseren behandler overskridelse av oppgitt kosttak, men har
  ingen tilsvarende håndhevet region-/hostinggrense for personvern. Ukjent kost
  fører ikke i seg selv til krav om bekreftelse.

Dette er avgrensede kildefunn, ikke en full sikkerhetsrevisjon.

## EntityHomePolicy: plassering og begrunnelse

Valget for videre implementasjon er å beholde policytilstanden **nær
`EntityScaffoldEnrollment`**, som allerede har `entityHomePolicy` og
`entityHomePolicy.set`. Det er alternativet i §9 punkt 1 og bevarer den
eksisterende eier- og persistensgrensen. Policyen må kontrolleres sammen med
gjeldende lenke ved datatilgang; en ny søskencelle ville innført en ekstra
tilstandsgrense uten et påvist behov i denne oppgaven.

**Valget er ikke implementert videre i denne runden.** Plassering per datadel,
eksplisitte `cache`/`backup`-unntak og oppdagelse/avvisning av andre doble
plasseringer gjenstår. Eksisterende enrollment-livssyklus er urørt.

## Bygg og stoppårsak

Begge forsøk ble kjørt i `CellScaffold`, før kildeendringer.

1. `swift build --disable-sandbox` — **exit 1**, før kildekompilering.
   Swift kunne ikke skrive
   `/Users/kjetil/.cache/clang/ModuleCache/Swift-7JL1KBZ3A6V3.swiftmodule`:
   `Operation not permitted`; deretter `unable to load standard library`.
   [Full logg](ENTITETSUTVIDELSE_2026-09-28_evidence/baseline-build.log).
2. Miljøtilpasset forsøk, fortsatt med `--disable-sandbox`:

   ```sh
   env CLANG_MODULE_CACHE_PATH=/tmp/entitetsutvidelse-20260928-clang-cache \
       SWIFTPM_MODULECACHE_OVERRIDE=/tmp/entitetsutvidelse-20260928-swift-cache \
       swift build --disable-sandbox
   ```

   **Exit 1**, under avhengighetsoppsett. Modulcache-feilen ble passert, men
   SwiftPM kunne ikke hente `https://github.com/Digipomps/FileUtils-c.git`:
   `Could not resolve host: github.com`.
   [Full logg](ENTITETSUTVIDELSE_2026-09-28_evidence/baseline-build-cache.log).

Dette er miljø-/avhengighetsblokkeringer, ikke kjørte tester som feiler.
Ingen `exit=64` ble observert, så vent-og-prøv-igjen-regelen for eierskapsvakten
ble ikke utløst. Ingen kodekompilering eller testresultater gir grunnlag for
grønn status. `swift test --disable-sandbox` ble ikke startet etter byggstopp.
Denne sesjonen har begrenset nettverk og ingen adgang til å eskalere
sandbox-tillatelser. Det er ikke mottatt en auto-review-avvisning.

## De seks testresultatene enkeltvis

| Test fra §9 punkt 4 | Resultat i denne runden | Eksisterende kilde / gap |
| --- | --- | --- |
| Eieren leser `entityRepresentation` fra to innrullerte scaffolds | **IKKE KJØRT / IKKE IMPLEMENTERT HER** | `testActiveScaffoldLinkReadsEntityRepresentationAfterEnrollmentCellRestart` dekker i koden én scaffoldidentitet og rekonstruert celle, ikke to kjørende scaffolds. |
| Ikke-innrullert scaffold nektes | **IKKE KJØRT** | Eksisterende `testEntityDataAccessDeniesForeignRequesterMissingCapabilityAndRevokedLink` inneholder avvisning av fremmed requester. |
| Tilbakekalt scaffold nektes | **IKKE KJØRT** | Samme eksisterende test inneholder tilbakekalling og avvisning. |
| Kapabilitet utenfor godkjent delmengde nektes | **IKKE KJØRT** | Samme eksisterende test inneholder manglende kapabilitet; enrollment har også `testApprovalRejectsCapabilityEscalation`. |
| Hosted plassering velges bare innenfor kost- og personvernpolicyen | **IKKE KJØRT / UFULLSTENDIG DEKNING** | `testHomePolicyRequiresOwnerConfirmationWhenHostedCostExceedsCap` sjekker status og gjenoppretting ved overskredet kosttak, ikke full plasseringshåndheving eller personvern. |
| Utdatert cache kan vises, men kan ikke autorisere skriving | **IKKE KJØRT / IKKE IMPLEMENTERT HER** | Ingen tilsvarende test i den inspiserte enrollment-testfilen. Ingen ny cachevei eller autoritetskontroll er lagt til. |

Ingen endringer er gjort ved vault- eller `SecretCredentialCell`-grensen.
Det er ikke lest eller kopiert private nøkler eller hemmeligheter. Det er heller
ikke kjørt nye tester som beviser §9 punkt 5.

## Hva som fortsatt ikke virker / ikke er påvist fra §8

- Full håndheving av `EntityHomePolicy` og den komplette grant-baserte
  fjernproxyen er fortsatt uferdig; eksisterende delimplementasjon er beskrevet
  ovenfor.
- Automatisk valg av hjemme-scaffold etter kost og tilgjengelighet er fortsatt
  utenfor oppgaven og ikke implementert her.
- Levende synk av `entityRepresentation` mellom instanser er fortsatt utenfor
  oppgaven og ikke implementert her.
- Konfliktløsning for krypterte cache/snapshots er fortsatt utenfor oppgaven og
  ikke implementert her.

**For eieren:** denne runden gir ingen ny brukbar kapabilitet. Det er ikke
grunnlag for å si at samme entitet nå kan brukes fra staging, prod og andre
scaffolds med håndhevet ett datasted. Ingen staging-/prod-instans er endret,
deployet eller funksjons-/formålsprøvd. Senere arbeid må fortsatt forholde seg
til manglende automatisk hjemmevalg, levende synk og konfliktløsning.

## Gren, commit og videre arbeid

- `CellScaffold`: `codex/entitetsutvidelse-20260928`, opprettet fra
  `942965ca24e9a418b531f9514c1da75d6d529e30`. Ingen ny kodecommit, siden
  implementasjonen stoppet før endringer.
- `CellProtocolDocuments`: rapportgrenen er
  `codex/entitetsutvidelse-rapport-20260928`, opprettet fra
  `c8029847502fe007833d1ebd371bcb5adc01c3ae`. Rapporten og de to byggloggene
  committes separat som `docs: record blocked entity enrollment build`.
  Committen lages i et separat, sparsomt utsjekket worktree:
  `HAVEN/_worktrees/entitetsutvidelse-docs-20260928`.
  Hovedarbeidsområdet fikk først grenen `codex/entitetsutvidelse-20260928`,
  men en allerede eksisterende `.git/index.lock` datert 25. september hindret
  staging der. Låsen er ikke fjernet. Rapport og logger finnes også på den
  bestilte stien i hovedarbeidsområdet, som ustagede filer.
- `CellProtocol`: urørt; inspisert HEAD
  `561d34a7ea785c087bd6036921f60debe6bace4a` med eksisterende lokale endringer.
- Ingen push, PR, merge eller deploy. Eksisterende endringer er ikke inkludert
  i rapportcommitten.

For å fortsette må byggeporten kunne passeres i et miljø med skrivbar Swift-cache
og tilgjengelige avhengigheter. Deretter fortsetter arbeidet fra §9 punkt 1 i
eierens angitte rekkefølge. Ingen ny spesifikasjon trengs.
