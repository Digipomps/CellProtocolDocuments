# PLAN — scaffold-administrator og delegering

G1 godkjent 2026-09-08. Arbeidspakker 1:1 mot bladformålene i FORMAALSSPEC §1.
Etter G2 teller bare artefaktene i §3 som fremdrift.

Regler som gjelder hele planen:

- Ingen arbeidspakke gir myndighet fra en rolleetikett (`lesson.purpose-never-grants-rights`).
- Deploy-/image-steg planlegges aldri som Codex-slice (`lesson.codex-sandbox-cannot-reach-docker`) — de blir HAVEN-Deploy-poster med eier Kjetil.
- Codex-jobber legges i `_losen-queue/inbox` som `<id>.job` + `<id>.prompt.md`, aldri som kommandoer Kjetil skal lime inn (`lesson.paste-command-instead-of-queue`).
- Testtall oppgis som «forventet ≈ N (fra kilde, dato)» og WP0 er en ekte kjøring (`lesson.baseline-count-from-report-not-run`).

## WP0 — Baseline

| | |
|---|---|
| purposeRef | `purpose://quality.build-and-regression` |
| utfører | Codex (kø-jobb) |
| gjør | Bygger CellScaffold på dagens hode og kjører hele testmengden **før** noen endring |
| tester | `test.build`, `test.regression` |
| artefakt | `TESTRESULT.md#build`, `#regression` med faktisk antall og faktiske røde |

Et rødt baseline stopper ikke arbeidet, men registreres som eget avvik med årsak.

## WP1 — Administrator-registrering per scaffold

| | |
|---|---|
| purposeRef | `purpose://candidate.scaffold-admin.org-is-registered-administrator` |
| utfører | Claude (kontrakt) + Codex (implementering) |
| gjør | Registrering av administrator-entitet per scaffold, lesbar uten å kjenne noen persons identitet. Administratorskifte er en egen handling med revisjonsspor. Digipomps for CellScaffold-staging; DiMy for Palazzo og senere Arendalsuka/konferanser |
| tester | `test.admin.registry-read` |
| artefakt | `contract/scaffold-administrator_v1.json` + fixtures, `dataflow.md` |

## WP2 — Mandatet som eneste myndighetsbærer

| | |
|---|---|
| purposeRef | `purpose://candidate.scaffold-admin.mandate-is-explicit-bounded-revocable` |
| utfører | Claude (kontrakt) + Codex (implementering) |
| gjør | Mandat = signert Agreement utstedt av administrator-entiteten, med `resourceRefs`, `actionKeypaths`, `purposeRef`, `validUntil`, `revocationRef`. Mangler ett felt: avvist. Ett ledd — et mandat som forsøker å gi utstederrett avvises (Kjetils Q2) |
| tester | `test.admin.mandate-shape`, `test.cell.auth-negative` |
| artefakt | `contract/scaffold-mandate_v1.json` + positive/negative fixtures |

## WP3 — Terskel som står i forhold til rekkevidde

| | |
|---|---|
| purposeRef | `purpose://candidate.scaffold-admin.threshold-matches-blast-radius` |
| utfører | Codex |
| gjør | Påkrevd signaturantall for administratormandat blir registrert policy per scaffold, ikke konstant. Settes til **1** nå (styreleder alene, utviklingsfase) med begrunnelse og dato, og gir en `runtimeAdvisories`-linje så lenge den er under 2. To signaturer fra samme identitet teller alltid som én. Heving til 2 skal skje uten kodeendring når prod er stabil |
| tester | `test.admin.threshold-is-policy` |
| artefakt | `TESTRESULT.md#threshold` |

## WP4 — Rolleetiketten gir fortsatt ingenting

| | |
|---|---|
| purposeRef | `purpose://candidate.scaffold-admin.role-label-grants-nothing` |
| utfører | Codex |
| gjør | Negativ test som låser dagens skille: `admin.operator` uten mandat får `agreement_or_proof_required`, nøyaktig som i dag. Ingen ny kodesti utleder myndighet fra rolle |
| tester | `test.admin.role-is-not-authority` |
| artefakt | `TESTRESULT.md#auth` |

Dette er regresjonsvernet mot den fristende snarveien. Den skal feile rødt hvis noen senere kobler rolle til myndighet.

## WP5 — Datarot-bytte skal si fra

| | |
|---|---|
| purposeRef | `purpose://candidate.scaffold-admin.authority-survives-or-fails-loudly` |
| utfører | Codex |
| gjør | Mangler administrator-registrering ved oppstart, legges `scaffold_administrator_not_provisioned` i `runtimeAdvisories` |
| tester | `test.admin.fresh-root-advisory` |
| artefakt | `TESTRESULT.md#advisory` |

Begrunnelse i én linje: staging fikk fersk datarot 19. august, myndigheten forsvant stille, og vi oppdaget det 8. september på en knapp som ikke virket.

## WP6 — Revisjonsspor navngir både organisasjon og person

| | |
|---|---|
| purposeRef | `purpose://candidate.scaffold-admin.audit-names-org-and-person` |
| utfører | Codex |
| gjør | Hver utstedelse logger mandatID, administrator-entitet, handlende identitet og begrunnelse |
| tester | `test.admin.audit-pair` |
| artefakt | `ACCEPT.md#audit` |

## WP7 — Eieren ser hvilke mandater som finnes

| | |
|---|---|
| purposeRef | `purpose://candidate.scaffold-admin.delegation-is-visible-to-the-owner` |
| utfører | Codex |
| gjør | Eier-lesbar liste over aktive mandater per celle; ikke-eier får avslag |
| tester | `test.admin.owner-can-list-mandates` |
| artefakt | `TESTRESULT.md#mandates` |

Merk: hvis dette skal ha en egen flate, utløser det G1-GUI som egen runde med rendret bilde før implementering. Denne pakken leverer først lesetilgangen, ikke flaten.

## WP8 — Organisasjonstilknytning som avtale

| | |
|---|---|
| purposeRef | `purpose://candidate.scaffold-admin.org-link-is-an-agreement-not-a-membership` |
| utfører | Claude (kontrakt) + Codex |
| gjør | `entity:vegar` får en rolleavtale utstedt av `entity:digipomps`, med start, slutt og tilbakekall. Ingen kode antar medlemskap. Tilbakekall slutter mandatene under avtalen uten å slette entiteten eller dataene |
| tester | `test.admin.org-link-revocable` |
| artefakt | `TESTRESULT.md#revoke` |

Den juridiske siden er Kjetils og en jurists. Denne pakken leverer formen, ikke avtalen.

## WP9 — Dokumentasjon i samme endring

| | |
|---|---|
| purposeRef | `purpose://quality.docs-in-same-change` |
| utfører | Claude |
| gjør | Kapittelet om autorisasjon oppdateres med administrator/mandat-modellen, datert «Last verified against code» |
| tester | `test.docs-updated`, `test.cell.stub-scan`, `test.status-current` |
| artefakt | `ACCEPT.md#docs`, `#stubs`, `#status` |

## WP10 — Deploykø

| | |
|---|---|
| utfører | **Kjetil** (eier), forberedt av Claude |
| gjør | HAVEN-Deploy-post: bygg image fra godkjent commit, transaksjonell cutover på staging med `cutover-invites-20260908.sh`-mønsteret (fingeravtrykk-vakt, rollback-container, readiness-gate), registrer `entity:digipomps` som administrator for staging-scaffoldet, verifiser `test.admin.registry-read` mot kjørende tjeneste |
| gate | Ingen prod før staging er verifisert. Prod har egen datarot og egen seremoni |

## Rekkefølge

WP0 → WP1 → WP2 → (WP3, WP4, WP5 parallelt) → WP6 → WP7 → WP8 → WP9 → WP10.

WP4 kjøres bevisst tidlig: den skal være grønn både før og etter endringen.

## Utenfor denne planen

- Vegars publiseringstilgang nå (Kjetils Q4) — egen liten oppgave med dagens mekanisme. Forutsetningen er at noen med owner-proof for `cell:///ArendalsukaConfigurationPublisher` utsteder én gang; hvem det er i praksis på staging er ikke verifisert.
- DiMy-utstedte VC-er fra Vipps-innlogging — egen PDD, egne regulatoriske porter.
