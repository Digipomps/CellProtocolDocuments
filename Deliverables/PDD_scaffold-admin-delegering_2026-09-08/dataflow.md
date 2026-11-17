# Dataflyt — hvem utsteder hva til hvem

Kravet fra `pkg.std.cell-combination`: hver kant navngis med endepunkt eller event,
og hver kant skal finnes igjen i en kontrakt. Kontraktene er
`contract/scaffold-administrator_v1.json` og `contract/scaffold-mandate_v1.json`.

Last verified against code: 2026-09-09 — CellScaffold branch
`pdd/scaffold-admin-delegering`, worktree `CellScaffold/_wt-sad-20260909`.
WP9 har avstemt kantene mot kilde og eksisterende TESTRESULT, uten ny kjøring.
Dette er lokal implementasjons-/teststatus; organisasjonene og mandatene er ikke
provisjonert på staging.

## Aktører

| Aktør | Hva den er | Merknad |
|---|---|---|
| Scaffold-eier | Identiteten med eierbevis for scaffoldet | Eneste som kan registrere eller bytte administrator |
| Administrator-entitet | `entity:digipomps`, `entity:dimy` | Organisasjon, ikke person. Utsteder mandater |
| Styreidentitet | Person som signerer på vegne av organisasjonen | Teller mot terskelen. Samme identitet to ganger teller som én |
| Mandatinnehaver | Person eller agent som skal handle | Kjetil, Vegar, senere agenter |
| Målcelle | `cell:///ArendalsukaConfigurationPublisher`, `cell:///AssistantCorrespondence`, … | Beholder sin egen autorisasjon; mandatet er bare et nytt gyldig grunnlag |
| Celleeier | Den som eier dataene i målcellen | Skal kunne se hvilke mandater som finnes på egen celle |

## Kanter

| # | Fra | Til | Endepunkt / event | Kontrakt |
|---|---|---|---|---|
| K1 | Scaffold-eier | ScaffoldAdministratorRegistry | `administrator.register` | administrator §set |
| K2 | Scaffold-eier | ScaffoldAdministratorRegistry | `administrator.transfer` | administrator §set |
| K3 | Scaffold-eier | ScaffoldAdministratorRegistry | `administrator.thresholdPolicy.set` | administrator §set |
| K4 | Hvem som helst | ScaffoldAdministratorRegistry | `administrator.state` (les) | administrator §get |
| K5 | Scaffold ved oppstart | runtimeAdvisories | `scaffold_administrator_not_provisioned` | administrator §advisories |
| K6 | Scaffold ved oppstart | runtimeAdvisories | `scaffold_administrator_threshold_below_two` | administrator §advisories |
| K7 | Administrator-entitet (med N styresignaturer) | ScaffoldMandate | `mandate.issue` | mandat §set |
| K8 | ScaffoldMandate | Mandatinnehaverens EntityAnchor | mandatet lagres hos mottaker | mandat §mandateShape |
| K9 | Mandatinnehaver | Målcelle | handling på `actionKeypaths`, mandatet presenteres | målcellens egen kontrakt |
| K10 | Målcelle | ScaffoldMandate | intern `ScaffoldMandateProofSupport.authorize` → `ScaffoldMandateCell.authorize/validate`, bundet til posten bak `revocationRef` | mandat §implementation; ikke et offentlig GET på URL-en |
| K11 | Celleeier | ScaffoldMandate | `mandate.list` (les) | mandat §get |
| K12 | Utsteder eller scaffold-eier | ScaffoldMandate | `mandate.revoke` | mandat §set |
| K13 | Organisasjonsentitet | ScaffoldMandate | `orgLink.issue` / `orgLink.revoke` | mandat §set |
| K14 | Enhver utstedelse | revisjonsspor | mandatID + organisasjon + handlende identitet + begrunnelse | mandat §audit |

## Kanter som med vilje ikke finnes

| Fra | Til | Hvorfor ikke |
|---|---|---|
| Adminrolle (`admin.operator` o.l.) | Målcelle | Rolleetiketter gir null cellemyndighet. Dette er formålet `role-label-grants-nothing`, og WP4 er regresjonsvernet |
| Mandatinnehaver | ScaffoldMandate `mandate.issue` | Ett ledd. Et mandat gir rett til å handle, aldri til å utstede videre (Kjetils Q2) |
| ScaffoldAdministratorRegistry | Målcellens data | Registeret vet hvem som administrerer, aldri hva cellene inneholder |
| Administrator-entitet | Mandatinnehaverens øvrige entitetsdata | Mandatet lagres hos mottaker; utsteder får ingen leserett tilbake |

## Merknad om K9/K10

Målcellen beholder sin egen autorisasjon uendret. Mandatet legger til ett gyldig
grunnlag ved siden av eierbevis — det erstatter ikke `validateAccess`, og det gir
ingen tilgang cellen ikke allerede kjenner som en keypath. Et formål kan innsnevre
en rettighet, aldri opprette eller utvide en.

## Verifisert omfang og planlagte kanter

- K1–K6: register, separat revisjonsført administratorskifte, lagret terskel og
  advisories er grønne gjennom WP1; [bevis](TESTRESULT.md#registry).
- K7–K8 og K11–K14: dekkes av WP2s signerte utstedelse, EntityAnchor-indeks,
  avslag, lesing og tilbakekall; [bevis](TESTRESULT.md#auth),
  [mandatliste](TESTRESULT.md#mandates), [tilbakekall](TESTRESULT.md#revoke).
  Den handlende signataren må ha et separat eier-signert representant-Contract
  for organisasjonen og gjeldende registreringskvittering; organisasjonsnavnet,
  styrebetegnelsen og et mottatt mandat etablerer ikke denne retten.
- K9/K10 er kjørt grønt mot publisher-cellens
  `resetEditableCellConfiguration`, med avslag etter tilbakekall. Kobling til
  `applyEditableCellConfiguration` er sett i kilde; faktisk publisering gjennom
  den er ikke bevist av denne testen. `publisherAccess.issue` er
  `not-implemented` på branchen. `AssistantCorrespondence` og andre målceller
  i aktørtabellen er **planlagte integrasjoner**, ikke verifiserte kanter.
- Et administratormandat kan gi scaffoldets `mandate.list`-innsyn, men er aldri
  representantbevis for videre utstedelse. Mandatbasert innsyn i
  `administrator.history` er fortsatt `not-implemented`; eier eller et separat
  eiergodkjent Agreement for akkurat den nøkkelen kan lese historikken.

Se [avvik og stub-avstemming](ACCEPT.md#stubs). Ingen kant her dokumenterer en
gjennomført staginghandling eller gjenopprettet publiseringstilgang for Vegar.
