# Undergrupper via partOf — 23.09.2026

Dokumentasjon og målskjema. **Besluttet, ikke implementert i Swift.**

## Mål

1. Valgfri gruppeforelder på barnet med `partOf`; ingen persistert barneliste.
2. Beholde påkrevd `name` og `members`, med bare entitets-uuid-er i `members`.
3. Ta `relations.bokprosjekt` ut av målskjemaet og erstatte det med `groups`-roten.
4. Vise prosjekt, kapittel og to arbeidsgrupper med fiktive navn og faste UUID-er.
5. Bygge som et strengt nytt steg etter 23.09, kontrollere positivt og negativt,
   og publisere bare avtalte dokumentasjonsfiler fra rene `main`-arbeidstrær.

## Påstander og belegg

| Grep | Observert resultat |
|---|---|
| Nytt steg `apply_decisions_2026_09_23_groups.py` | Bygger 16.09 → 22.09 → 23.09 → undergrupper i minnet; validerer før skriving. Ingen skjemafil er håndredigert. |
| Gruppeobjektet | Bare `name`, `members` og `partOf` tillates. `name` og `members` er påkrevd; `partOf` er valgfri UUID-streng med maks 36 tegn. |
| Retning | Beskrivelsene sier barnet → foreldregruppen. Barnelisten persisteres ikke og bygges ved dekoding som øvrige bakveier. |
| Medlemskap | Beskrivelsene krever entitets-uuid-er. Separate Python-referansekontroller avviser gruppe-uuid-er, relasjons-uuid-er og ukjente entiteter i `members`. Ingen type utledes fra UUID-prefiks. |
| Gammel bokprosjekt-form | Hele `relations.bokprosjekt` er fjernet; `relations.additionalProperties: false` avviser den gamle formen. Beslutningsdokumentet navngir `groups` som erstatning. |
| Eksempel | Fire nye grupper: rot `…0003`, kapittel `…0004`, arbeidsgrupper `…0005`/`…0006`. Begge arbeidsgruppene peker til samme kapittel; hver har én eksisterende fiktiv entitet som medlem. Eksisterende eksempeldata er bevart. |
| Manifest og grafskjema | Manifestet peker til siste bygge-/kontrollsteg. Grafskjemaet speiler oppdatert beslutningsmetadata; alle delte `$defs` og `$id` er uendret. |
| Dokumentasjon | Beslutningen, målformens forklaring, LES-MEG og bare Book-kapittel 37 er oppdatert. Book-inventaret er uendret, så katalogen er ikke endret. |
| Manglende mål | 36 slettede skjemamål, eksempelmål og manifest-/grafmål gir eksplisitt feil. Gjentatt anvendelse av skjemasteget eller eksempelsteget feiler. Kjørt med `python -O`. |
| Uendret runtime | `EntityData.review.schema.json` har fortsatt SHA-256 `c62ca8f329d229101775158c61fdfce0b0874b0e00211820bea6fb10500c5e2f`. Ingen Swift-endringer eller ekte datamigrering. |

### Kontrollresultater

[Maskinlesbart resultat](../../CellProtocol/Docs/EntityData-Review-2026-09-11/TARGET-VALIDATION-2026-09-23-GROUPS.json):
**217 kontroller bestått**, med **Ajv 8.17.1 + ajv-formats 3.0.1**.
Antallet inkluderer lokale `$ref`-oppslag og mutasjonskontroller; det er ikke 217 runtime-tester.

| Kontroll | Resultat og nivå |
|---|---|
| `partOf` til eksisterende gruppe-uuid | Bestått: schema og referansekontroll |
| Rot uten `partOf` | Bestått: schema og referansekontroll |
| Ikke-uuid, null, liste eller avsluttende linjeskift i `partOf` | Avvist av JSON Schema |
| Manglende `name` eller `members` | Avvist av JSON Schema |
| Gruppe-uuid i `members` | Avvist av separat referansekontroll; skjemaet alene godtar UUID-syntaksen |
| Gruppe-uuid med vilkårlig prefiks og ulik bokstavstørrelse | Avvist av referansekontrollen, også hvis samme UUID finnes i entitetskartet |
| `children`, `parts`, `subgroups` eller `groups` som persistert felt på en gruppe | Avvist av JSON Schema |
| `relations.bokprosjekt` | Avvist av JSON Schema |
| Ukjent forelder eller entitets-uuid i `partOf` | Avvist av referansekontroll |
| Selvsykel og sykel gjennom tre nivåer | Avvist av referansekontroll; skjemaet alene godtar begge |
| Eksempelet, alle referanser og eksisterende beviskoblinger | Bestått |
| Begge skjemaer gyldig Draft 2020-12; lokale `$ref` løses | Bestått |
| Ny bygging gir byte-like skjemaer, eksempel og manifest | Bestått |
| Hele kontrakten utenfor avtalte endringer bevart | Bestått: objektlikhet mot foregående byggesteg |
| Uendrede 22.09-/23.09-suiter mot deres målform i isolert midlertidig kopi | 235 / 301 kontroller bestått |

**Kjent begrensning:** Draft 2020-12 kontrollerer form og UUID-syntaks, ikke
oppslag av referansetype i dokumentets dynamiske kart eller sykler i `partOf`.
Referansekontrollen er dokumentasjonsverktøy for komplette lokale kart.
Dekoderen må fortsatt implementere avvisningene og bygge barnelistene i minnet.
Kontrollene hevder ikke at denne Swift-atferden allerede finnes.
Se [spesifikasjonens valideringsmodell](https://json-schema.org/draft/2020-12/json-schema-validation#section-3).

### Ikke kjørt

- **Visualiseringssjekkene: ikke kjørt.** Den historiske suiten leser eksterne,
  utdaterte 16.09/17.09-artefakter fra
  `/Users/kjetil/.codex/visualizations/2026/09/11/01a090eb-528a-76d3-87d1-41a0b84f4d47`.
  Oppdaterte undergruppeartefakter og en oppdatert suite mangler.
- **Swift/runtime, ekte dekoding og migrering: ikke kjørt.** Oppgaven er
  dokumentasjon og skjema. Den nye dekoderen er ikke implementert.
- **Python jsonschema-banen: ikke kjørt.** Import ga `ModuleNotFoundError`.
  Den eksisterende lokale Ajv-banen ble brukt eksplisitt; ingen pakker ble lastet ned.
- **De gamle validatorene direkte mot ny målform: ikke kjørt.** De krever den
  gamle gruppeformen og byte fra tidligere byggesteg. I stedet kjørte de uendret
  mot sitt historiske mål i en midlertidig kopi; historiske resultatfiler er urørt.
- **GitHub Actions: ikke kjørt av denne jobben.** Resultatene over er lokale
  dokumentasjons-/skjemakontroller, ingen påstand om CI eller runtime-dekning.

## Reproduksjon

Fra `CellProtocol/Docs/EntityData-Review-2026-09-11`:

```sh
export ENTITYDATA_AJV_MODULE=/usr/local/lib/node_modules/@nestjs/cli/node_modules/ajv
export ENTITYDATA_AJV_FORMATS_MODULE=/usr/local/lib/node_modules/@nestjs/cli/node_modules/ajv-formats
python3 -B -O apply_decisions_2026_09_23_groups.py
python3 -B -O validate_decisions_2026_09_23_groups.py
```

## Publisering og SHA-er

De separate `main`-arbeidstrærne fra forrige publisering ble gjenbrukt etter
kontroll av ren status, `git fetch origin main` og `git merge --ff-only origin/main`:

- `_worktrees/entitydata-publish-20260923/CellProtocol`
- `_worktrees/entitydata-publish-20260923/CellProtocolDocuments`

Den nye jobben startet på `03d173881e8d6c662b402f716c985572b91d3183` og
`cdfa43513ab887a4be466b8ddd93b5c5867ce3e2`. Disse har senere arbeid enn
`7f9bdcf`/`b814a81`; det eksisterende arbeidet er beholdt.
De opprinnelige urene arbeidsgrenene er ikke brukt til staging eller publisering.

| Repo | Før (hentet `origin/main`) | Etter innholdscommit |
|---|---|---|
| CellProtocol | `03d173881e8d6c662b402f716c985572b91d3183` | `a785dc71aadc2ea4e0468faae4dbfe9388952275` |
| CellProtocolDocuments | `cdfa43513ab887a4be466b8ddd93b5c5867ce3e2` | Rapporteres etter publisering |

CellProtocol: push til `origin/main` gikk gjennom på første forsøk.
`git ls-remote --exit-code origin refs/heads/main` bekreftet nøyaktig samme SHA.
Alle ti committede filer er sammenlignet byte for byte med det rene arbeidstreet.
Ingen rebase eller tvunget push var nødvendig.
Dokumentrepoets publisering bekreftes i en etterfølgende rapportcommit.

Sluttkontroll før staging: 37 lokale Markdown-lenker finnes, ingen avsluttende
blanktegn, Python-syntaks leses, og `git diff --check` er grønn i begge repoer.
842 øvrige sporede filer i CellProtocol og 592 i dokumentrepoet er byte-uendret
fra oppstart, inkludert henholdsvis 593 og 2 Swift-filer.
Stilisten i CellProtocol ble kontrollert eksakt mot `git diff --cached --name-only`
før commit; dokumentrepoet bruker den samme kontrollen med de to stiene under.

### Stier i CellProtocol — 10 filer

- `Docs/EntityData-Review-2026-09-11/BESLUTNING-UUID-OG-GRUPPER-2026-09-22.md`
- `Docs/EntityData-Review-2026-09-11/EntityData.v2.example.json`
- `Docs/EntityData-Review-2026-09-11/EntityData.v2.schema.json`
- `Docs/EntityData-Review-2026-09-11/EntityRepresentation.v2.schema.json`
- `Docs/EntityData-Review-2026-09-11/LES-MEG.md`
- `Docs/EntityData-Review-2026-09-11/TARGET-VALIDATION-2026-09-23-GROUPS.json`
- `Docs/EntityData-Review-2026-09-11/V2-BESLUTTET-FORM.md`
- `Docs/EntityData-Review-2026-09-11/apply_decisions_2026_09_23_groups.py`
- `Docs/EntityData-Review-2026-09-11/current-review.json`
- `Docs/EntityData-Review-2026-09-11/validate_decisions_2026_09_23_groups.py`

### Stier i CellProtocolDocuments — 2 filer

- `Book/37_EntityData.md`
- `Deliverables/GRUPPER_PARTOF_2026-09-23.md`

Uttrykkelige tillatelseslister ligger i den lokale evidensmappen
`_worktrees/grupper-partof-20260923-evidence/`. `git diff --cached --name-only`
skal være eksakt lik listen før hver commit. `build_v2_schema.py` og
`IdentityLink-fixture.patch` er ikke med. Ingen andre Book-filer er med.

CellProtocol-commit bruker nøyaktig meldingen eieren ba om:

```text
docs: subgroups via partOf, and the bokprosjekt tree retired

Groups can point at a parent group with partOf; the child list is built at
decode like every other back edge. relations.bokprosjekt carried its own
member and group form and is replaced by the groups root.

Decided, not implemented.
```

## Filsummer før og etter

Før er rene `main` etter fast-forward; etter er filene som skal publiseres.
Filnavnene nedenfor er under `Docs/EntityData-Review-2026-09-11/`.

| Fil | SHA-256 før | SHA-256 etter |
|---|---|---|
| `BESLUTNING-UUID-OG-GRUPPER-2026-09-22.md` | `abae5b92cd86e33130c45570046b1a993990e6faff0ad39c3051a0f7b3a7a2a6` | `7662c7934b9365bbe33a5da383c23cd460664b4f5fc43933e6195c5af406cb17` |
| `EntityData.v2.example.json` | `5d8140c1902f2b99a9e4eb4fd8d4cf24c23bcfd3c5b442e2ecf35aa447db18c1` | `b4ccf189eb242fa41c6ba10ac61b3faab388eb9f01aa5548d9190e3494327ca2` |
| `EntityData.v2.schema.json` | `3d778a2e6c964548c553696020b793292762605bfaf9a07fa0cca5f39ae793cc` | `fd72be5b91471a7fec4f5e55bffb78bf40ea738f19ec3f1f864621cd6a9e943a` |
| `EntityRepresentation.v2.schema.json` | `86ccbe52bdfe40e62eedc91fe68c33c161182ff6b437d6de66b8298f518b5fd4` | `5a2f1df727db99ee45269293744c82422bdc7097e0bdf9de2c94c74f5580e9a8` |
| `LES-MEG.md` | `cd0b5b73e8e94856e0448a448b623ed702f0713bc105eafa459930ed0746f17d` | `8688c28f0ce9b570c319a280b6b47ac73e2d35fdf4d455883f8c0dd2dd17f39d` |
| `TARGET-VALIDATION-2026-09-23-GROUPS.json` | `ny fil` | `99581b3b6de80ed2b596f83a66c66ad1e9f3ec921b4f61d48c006a4bd4b642a7` |
| `V2-BESLUTTET-FORM.md` | `a43c66ed41768ccbba317de8dcc7742a730baa2d233a06c76f7052ec4451ed0b` | `12db425075d718987c96e62aa9da656b635d4099ea24cade6dd8b4b00f1a3dbe` |
| `apply_decisions_2026_09_23_groups.py` | `ny fil` | `15ef2acc3a6823d82f40cc0f620c34cddafbf9b43aeee8aaf0a96029a78016bb` |
| `current-review.json` | `c81a66067c3d8cb10b88661e31dba2c7377bfb8bf95f3c8e2c788d5d9aef4c00` | `acbff7858317709ded570d4fc89ca1c5addf62a75a47fe63041fa3e305a5ae62` |
| `validate_decisions_2026_09_23_groups.py` | `ny fil` | `a7882d9a26fe6d988f3c3ce3454bb93b9100f5d0479ddbdadd5956e486056de7` |
