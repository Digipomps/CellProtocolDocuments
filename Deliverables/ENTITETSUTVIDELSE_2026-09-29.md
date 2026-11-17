# Entitetsutvidelse — 2026-09-29

**Status: IKKE LEVERT. Stoppet på en kompilatorfeil i kode skrevet i denne runden.**

Hele [kapittel 32](../Book/32_Cross_Scaffold_Entity_Enrollment.md) er lest og er
fortsatt spesifikasjonen. Kapittelet er ikke endret. Denne filen er en
arbeidsrapport, ikke en ny spesifikasjon.

## Mål

Eieren skal bruke samme entitetsdata fra staging, prod og andre eksplisitt
innrullerte scaffolds. Hver datadel skal ha ett kanonisk hjem. Tilgang krever
gjeldende eiergodkjent innrullering, avgrenset kapabilitet og identitetsbevis.
Cache og backup skal være navngitte unntak uten skriveautoritet.

Bestillingen er §9 punkt 1–5, med de seks testene i punkt 4. Grønt bygg og
grønne tester er ikke i seg selv godkjenning for main eller deploy.

## Påstander og belegg

| Påstand | Resultat / belegg |
| --- | --- |
| Byggemiljøet kan kompilere eksisterende CellScaffold. | **Påvist i dette arbeidsområdet:** grunnbygget fullførte med exit 0. Nett og skrivbar modulcache fungerte. Dette var ikke en ren HEAD-utsjekk. |
| Den nye implementasjonen bygger. | **Usant:** implementasjonsbygget feilet med exit 1. Feilen er beskrevet nedenfor. |
| De seks bestilte scenarioene virker. | **Ikke påvist:** testkode er skrevet, men ingen tester er kjørt eller testkompilert etter endringene. |
| Eierens én-sannhet-regel håndheves nå i staging og prod. | **Ikke påvist:** ingen utrulling, kjøring mot disse instansene eller funksjons-/formålsprøve. |
| Kodeutkastet er klarert for main. | **Nei.** Kildeendringene er uferdige og ikke committet som leverbar kode. |

## Hva som er skrevet, men ikke ferdig bygget

Arbeidskopien i `CellScaffold` har disse oppgavespesifikke endringene:

| Fil | Kildeutkastets innhold — ingen funksjonsgaranti |
| --- | --- |
| `Sources/App/Cells/EntityScaffoldEnrollment/EntityHomePolicy.swift` | Policystruktur og validering av ett hjem per datadel, eksplisitte lokale kopier, hosted kost-/region-/hosting-/transportgrenser og kontroll av deklarert plasseringsinventar. |
| `Sources/App/Cells/EntityScaffoldEnrollment/EntityScaffoldEnrollmentCell.swift` | Policykobling i datatilgangen, signerte operasjoner, kapabilitet/formål/audience, lenkegenerasjon og utløp, nonce-reservasjon, samordnet datatilgang/tilbakekalling/policyendring, skrivekvittering og metadata-FlowElement. **Denne filen har kompilatorfeilen.** |
| `Sources/App/Cells/EntityScaffoldEnrollment/EntityScaffoldDataRequest.swift` | Signert operasjonsformat, klientproxy, Explore-beskrivelser og en uforanderlig, dekryptert visningssnapshot som ikke er et autoritetsbevis. |
| `Sources/App/Cells/EntityScaffoldEnrollment/EntityScaffoldDataAccessCell.swift` | Scaffold-omfattende inngang for fjernkall. Eierens UUID brukes til ruting til eksisterende vault-identitet; den opprinnelige requester-identiteten sendes videre til innrulleringscellens autorisasjon. Ingen eiernøkkel sendes til fjernscaffoldet av denne koden. Sikkerheten i hele kjeden er ikke kjørt. |
| `Sources/App/Support/IdentityEntityPersistenceSupport.swift` | Utvidelse av eksisterende kvitterte batchlagring med valgt EntityAnchor-referanse. Proxykall skal kreve eksisterende røtter, slik at et avgrenset nøkkelfelt ikke blir til en implisitt erstatning av en hel rot. |
| `Sources/App/configure.swift` | Én registreringslinje for `EntityScaffoldDataAccess`. **Filen hadde mange eksisterende brukerendringer; bare denne linjen tilhører oppgaven.** |
| `Tests/AppTests/EntityScaffoldEnrollmentCellTests.swift` | Nye tester og tilpasning av eksisterende datatilgangstester til signerte operasjoner. Innrulleringens eksisterende tester for signert forespørsel/godkjenning/aktivering er beholdt. |

Ingen CellProtocol-kildekode eller vault-/SecretCredentialCell-implementasjon
er endret. Innrulleringslivssyklusen er beholdt; datatilgang, policy og
persistensintegrasjon er utvidet rundt den.

## EntityHomePolicy: plassering og begrunnelse

Policytilstanden blir **ved `EntityScaffoldEnrollment`**, med de eksisterende
keypathene `entityHomePolicy` og `entityHomePolicy.set`, og serialiseres sammen
med innrulleringscellen. Modellen og valideringskoden er flyttet til den lille
nabofilen `EntityHomePolicy.swift`; det er **ikke** opprettet en egen policycelle.

Dette bevarer den eksisterende eier- og persistensgrensen. Gjeldende lenke og
gjeldende policy må avgjøre samme dataoperasjon. En separat policycelle ville
tilført en ekstra tilstandsgrense uten et påvist behov i denne oppgaven.

Datadelene i kildeutkastet er `entityRepresentation`, `relations`,
`agreements`, `purposes` og `chronicle`. Duplikate hjem avvises i policyen.
`cache` og `backup` er uttrykkelige, navngitte, krypterte og skrivebeskyttede
kopiunntak. `index` og `uiState` kan ikke deklareres som kopier med entitetsverdier.
`entityHomePolicy.validatePlacements` er skrevet for å avvise uautoriserte
deklarerte kopier.

**Bevisgrense:** Dette kontrollerer policy og deklarert inventar; det skanner
ikke andre serveres disker. Det beviser heller ikke at alle eksisterende
direkte EntityAnchor-skriveveier i resten av systemet følger denne policyen.
Ingen av disse kontrollene er kjørt. Full håndheving av eierens regel kan
derfor ikke påstås fra denne leveransen.

## Bygg og faktisk stoppårsak

Miljø: Apple Swift 6.4, arm64 macOS. Begge forsøk brukte:

```sh
export CLANG_MODULE_CACHE_PATH=/private/tmp/haven-modulecache-48166
export SWIFTPM_MODULECACHE_OVERRIDE="$CLANG_MODULE_CACHE_PATH"
```

1. **Grunnbygg, før kildeendringer:** `swift build --disable-sandbox` i
   `CellScaffold` — **exit 0**, `Build complete! (248,43 sek)`.
   [Logg](ENTITETSUTVIDELSE_2026-09-29_evidence/baseline-build.log),
   [exit og cacheinnstillinger](ENTITETSUTVIDELSE_2026-09-29_evidence/baseline-build-exit.txt).
   SwiftPM hentet avhengigheter fra GitHub. Advarsler om global manifestcache
   hindret ikke dette bygget.
2. **Implementasjonsbygg:** `swift build --disable-sandbox --package-path CellScaffold`
   fra HAVEN-roten — **exit 1**.
   [Logg](ENTITETSUTVIDELSE_2026-09-29_evidence/implementation-build.log),
   [exit](ENTITETSUTVIDELSE_2026-09-29_evidence/implementation-build-exit.txt).

Den konkrete kompilatorfeilen:

```text
Sources/App/Cells/EntityScaffoldEnrollment/EntityScaffoldEnrollmentCell.swift:749:83:
error: value of type 'any CellResolverProtocol' has no member 'persistCellSnapshot'
```

Kallet ble lagt til i denne runden. `CellBase.defaultCellResolver` er deklarert
gjennom `CellResolverProtocol`; `persistCellSnapshot(_:) async -> Bool` finnes
på den konkrete `CellResolver`-klassen. Dette er **en implementasjonsfeil fra
denne runden**, ikke nettverksfeilen eller modulcache-feilen fra forrige forsøk.

Eierens regel «Rødt bygg eller røde tester: stopp» ble fulgt ved dette
resultatet: ingen videre kildeendring, nytt byggforsøk eller testkjøring.
Ingen `exit=64` ble observert, så vent-og-prøv-igjen-regelen ble ikke utløst.
`swift test --disable-sandbox` ble ikke startet etter byggstopp.

## De seks testresultatene enkeltvis

Alle navn nedenfor finnes i testkildeutkastet. **Ingen av testene er kjørt.**

| Test fra §9 punkt 4 | Testnavn | Resultat |
| --- | --- | --- |
| Eieren leser `entityRepresentation` fra to innrullerte scaffolds | `testOwnerReadsOneCanonicalRepresentationFromTwoEnrolledScaffoldsThroughResolver` | **IKKE KJØRT.** Skrevet med to scaffoldidentiteter/vaults og resolverinngangen i én lokal prosess; ikke to kjørende serverinstanser. |
| Ikke-innrullert scaffold nektes | `testNonEnrolledScaffoldIsDeniedByResolverIngress` | **IKKE KJØRT.** |
| Tilbakekalt scaffold nektes | `testRevokedScaffoldIsDeniedForReadAndWrite` | **IKKE KJØRT.** |
| Kapabilitet utenfor godkjent delmengde nektes | `testCapabilityOutsideApprovedSubsetIsDeniedForWrite` | **IKKE KJØRT.** |
| Hosted plassering bare innenfor kost- og personvernpolicy | `testHostedPlacementOnlyWithinOwnerCostAndPrivacyPolicy` | **IKKE KJØRT.** Tester skrevet for eksplisitt eiervalg, kostoverskridelse, ukjent kost, region, hostinggrense og transport; ikke automatisk hjemmevalg. |
| Utdatert cache kan vises, men ikke autorisere skriving | `testStaleCacheRendersButCannotAuthorizeWriteEvenAfterRevocation` | **IKKE KJØRT.** Skriver både forsøk med cache-revisjon og signert skriveforsøk etter tilbakekalling, med kontroll av uendret hjemmedata. |

Andre nye, **ukjørte** tester gjelder FlowElement og replay etter gjenoppretting,
duplikatplassering og navngitte kopiunntak, endret signert payload,
formål/audience/mål, utløp, eiergodkjenning av skriving og syntetisk
`privateKey`-materiale. Eksisterende avvisningstester er heller ikke kjørt på nytt.
Testfilen er ikke kompilert i denne runden; flere feil kan derfor gjenstå.

## Hva som fortsatt ikke virker eller ikke er påvist fra §8

- Ny hjemme-policy og komplett fjernproxy er **uferdige kildeutkast**, ikke
  verifiserte kapabiliteter.
- Automatisk hjemmevalg etter kost og tilgjengelighet er fortsatt ikke
  implementert; bare validering av et eksplisitt eiervalg er skrevet.
- Levende synk av `entityRepresentation` er fortsatt ikke implementert. Den
  tiltenkte proxyen leser på nytt fra hjemmet ved hvert kall.
- Konfliktløsning for krypterte snapshots er fortsatt ikke implementert.
- Ingen varig kryptert cachemotor eller datamigrering ved hjemmebytte er bygget
  i denne runden. Cachetesten gjelder en dekryptert snapshot i minnet.

**For eieren etter denne runden:** ingen ny brukbar kapabilitet er levert.
Det er ikke grunnlag for å bruke utkastet i staging eller prod. Ingen instans
er deployet eller funksjons-/formålsprøvd. Selv etter senere vellykket
ferdigstilling vil automatisk hjemmevalg, levende synk og snapshot-konfliktløsning
fortsatt være utenfor den bestilte delen. Hjemmet må velges/provisjoneres
eksplisitt, og ferske autorisasjoner og skriving må nå det kanoniske hjemmet.

## Gren, bevaring og commit

- `CellScaffold`: **`codex/entitetsutvidelse-20260929`**, fra
  `942965ca24e9a418b531f9514c1da75d6d529e30`.
  Kildeendringene er **ukommittert WIP** på denne grenen. Det røde bygget
  stopper kodeleveransen; det er ikke laget en kildekodecommit som om dette
  var ferdig bygget.
- En avgrenset
  [WIP-patch](ENTITETSUTVIDELSE_2026-09-29_evidence/UNBUILT_WORK_IN_PROGRESS.patch)
  og [manifest med kildehash](ENTITETSUTVIDELSE_2026-09-29_evidence/work-in-progress-manifest.json)
  bevarer forsøket. Patchen inneholder bare oppgavens endringer, inkludert bare
  registreringslinjen fra `configure.swift`. Den skal ikke anvendes blindt over
  eksisterende endringer.
- `CellProtocolDocuments`: rapport og byggbevis lagres som en egen dokumentasjonscommit på
  **`codex/entitetsutvidelse-rapport-20260929`**, fra
  `c8029847502fe007833d1ebd371bcb5adc01c3ae`, i worktree
  `_worktrees/entitetsutvidelse-docs-20260929` under HAVEN-roten.
  Den eksisterende `CellProtocolDocuments/.git/index.lock` fra 25. september
  er urørt. Rapporten finnes også på den bestilte stien i hovedarbeidsområdet.
- Mange eksisterende lokale endringer fantes ved oppstart. Ingen av disse er
  lagt i rapportcommitten. CellProtocol-kilden er urørt av denne oppgaven.
- **Ingen push, PR, merge eller deploy.** Eier avgjør videre arbeid og senere
  funksjons-/formålsgodkjenning.

## Læringsfangst

API-fallgruven er fanget som
`L-2026-09-29-persistcellsnapshot-is-a-concrete-cellresolver`, rutet til og
faktisk skrevet inn i
`CellScaffold/.claude/skills/cellprotocol-scaffold-integration/SKILL.md`.
`applied` godkjente endringen. `sync` bygget Desktop-ZIP, men feilet med
`Operation not permitted` ved skriving til hjemmekatalogens `.claude/skills`.
Læringen er derfor **oppdatert i kanon, men ikke distribuert**.
En separat Git-fallgruve ble også fanget og anvendt i `haven-git-workflow`:
`L-2026-09-29-a-fresh-git-worktree-created-with-no-checkout`. Et nytt
`--no-checkout`-worktree måtte få indeks fra HEAD før den sparsomme rapporten
kunne stages; kontroll av staged paths fanget utilsiktede slettemarkeringer
før commit. Bare det nye rapport-worktreets indeks ble initialisert; ingen
brukerfiler ble slettet. Også denne skill-distribusjonen feilet på tilgang til
hjemmekatalogen.

`check --strict` må leses sammen med distribusjonstelleren: null uoppdaterte
mål betyr ikke at skills er synket. Begge nye læringer er anvendt i kanon,
men udistribuert.
