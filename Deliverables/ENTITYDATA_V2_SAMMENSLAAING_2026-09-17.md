# EntityData v2 — sammenslåing og publisering 2026-09-17

Begge dokumentasjonscommits er publisert på `origin/main`. Etter push bekreftet `git ls-remote --exit-code origin refs/heads/main` nøyaktig SHA-ene nedenfor. De leverte kildefilene ble kopiert og publisert uten innholdsendringer.

| Repo | `origin/main` før | `origin/main` etter | Push |
|---|---|---|---|
| CellProtocol | `261c6119607e74c018e8faf51bd658de7b4aeaed` | `36372c5b95a7b57fbef92ffa54dea13bdf75a9e6` | Bekreftet, første forsøk |
| CellProtocolDocuments | `d305ae41c4a6cb027c8cf64c340b2d6aa1af2dce` | `357f2cfa0b3f1587a751c29f36540ab19f24c4a1` | Bekreftet, første forsøk |

## Faktisk committede stier

CellProtocol: `36372c5b95a7b57fbef92ffa54dea13bdf75a9e6`, forelder `261c6119607e74c018e8faf51bd658de7b4aeaed`. Nøyaktig 14 stier:

| Endring | Sti |
|---|---|
| Endret | `Docs/EntityData-Review-2026-09-11/EntityData.v2.example.json` |
| Endret | `Docs/EntityData-Review-2026-09-11/EntityData.v2.schema.json` |
| Ny | `Docs/EntityData-Review-2026-09-11/EntityRepresentation.v2.schema.json` |
| Endret | `Docs/EntityData-Review-2026-09-11/LES-MEG.md` |
| Ny | `Docs/EntityData-Review-2026-09-11/OPPDATERT-ETTER-GJENNOMGANG-2026-09-16.md` |
| Ny | `Docs/EntityData-Review-2026-09-11/TARGET-VALIDATION-2026-09-17.json` |
| Slettet | `Docs/EntityData-Review-2026-09-11/V2-BESLUTTET-FORM.md` |
| Endret | `Docs/EntityData-Review-2026-09-11/WORK-IN-PROGRESS.md` |
| Ny | `Docs/EntityData-Review-2026-09-11/apply_decisions_2026_09_16.py` |
| Slettet | `Docs/EntityData-Review-2026-09-11/build_v2_schema.py` |
| Ny | `Docs/EntityData-Review-2026-09-11/current-review.json` |
| Ny | `Docs/EntityData-Review-2026-09-11/requirements-target.txt` |
| Ny | `Docs/EntityData-Review-2026-09-11/review-decisions-2026-09-16.json` |
| Ny | `Docs/EntityData-Review-2026-09-11/validate_decisions_2026_09_16.py` |

CellProtocolDocuments: `357f2cfa0b3f1587a751c29f36540ab19f24c4a1`, forelder `d305ae41c4a6cb027c8cf64c340b2d6aa1af2dce`. Kun én sti:

- `Book/37_EntityData.md` — endret.

## Commit-meldinger

CellProtocol:

```text
docs: replace EntityData v2 with the reconciled decision target

Two parallel passes produced target schemas from the same review. This
keeps the more complete one — reproducible builder, decision register,
graph schema and validator — and corrects it on one point the other pass
had right: signedAgreementEntity.records stays a list, per the owner's
accepted objection of 2026-09-16, because the record is an audit chain
where order must survive.

Decided, not implemented. The v1 files remain and still describe what the
code stores today.
```

CellProtocolDocuments:

```text
docs(book): point Chapter 37 §7 at the reconciled v2 package
```

## Isolering og publisering

Begge repoene ble hentet med `git fetch origin main`. Eksisterende lokal `main` var identisk med `origin/main`, uten egne commits foran. Separate, rene, midlertidige arbeidstrær ble opprettet på eksisterende `main`, som ved dokumentasjonsjobben `261c611`. Ingen ny gren ble opprettet, og ingen commit ble laget på de opprinnelige arbeidsgrenene.

Opprinnelige grener og HEAD er uendret før og etter:

- CellProtocol: `pdd/tillitspakke-agentflaate`, `561d34a7ea785c087bd6036921f60debe6bace4a`.

- CellProtocolDocuments: `codex/docs-cleanup-20260810`, `fb8dffd96b26a7721a631129710addeacd8ed7b8`.

CellProtocol ble pushet først, deretter CellProtocolDocuments. Begge brukte `git push origin refs/heads/main:refs/heads/main`. Begge lyktes på første forsøk. Ingen push ble avvist fordi fjerngrenen hadde flyttet seg; `git pull --rebase` og et nytt forsøk var derfor ikke nødvendig. Ingen force-push ble brukt.

Begge midlertidige arbeidstrær var rene etter commit og ble fjernet etter bekreftet publisering med vanlig `git worktree remove`, uten force. Lokal `main` og `origin/main` peker på de publiserte commitene.

## Slettede lokale duplikater

Etter at begge pushene var bekreftet, ble disse tre filene kontrollert som usporede og slettet fra det opprinnelige CellProtocol-arbeidstreet:

- `Docs/EntityData-Review-2026-09-11/EntityData.decisions-2026-09-16.schema.json`
- `Docs/EntityData-Review-2026-09-11/EntityData.decisions-2026-09-16.example.json`
- `Docs/EntityData-Review-2026-09-11/EntityRepresentation.decisions-2026-09-16.schema.json`

Før slettingen ble `shasum -a 256` kjørt på alle tre parene. Grafskjemaene ble i tillegg sammenlignet byte-for-byte.

| Filpar | SHA-256, gammelt navn | SHA-256, v2-navn | Resultat |
|---|---|---|---|
| `EntityRepresentation.decisions-2026-09-16.schema.json` / `EntityRepresentation.v2.schema.json` | `0f398b1f59c4e1f25f4d690ad10dbba3fc12ca3c080348bbd3c9fdf5f86d20e2` | `0f398b1f59c4e1f25f4d690ad10dbba3fc12ca3c080348bbd3c9fdf5f86d20e2` | Like |
| `EntityData.decisions-2026-09-16.schema.json` / `EntityData.v2.schema.json` | `3052706f897db5b5fb6a89f1eba8a444d759df3588525bd5e991e9fcdaae7bd4` | `a5fdf62f074e3cd1b3494009b69dee5ae28504eece0e838d35cc65607587ee15` | Ulike |
| `EntityData.decisions-2026-09-16.example.json` / `EntityData.v2.example.json` | `b576632448a881236014271d81a0c992aee45b88bc9f3c242003e258b3993e60` | `b576632448a881236014271d81a0c992aee45b88bc9f3c242003e258b3993e60` | Like |

Avvik fra forventningen i bestillingen: det gamle EntityData-eksemplet var allerede byte-likt v2-eksemplet. EntityData-skjemaene var ulike, og grafskjemaene var like som påkrevd. Alle tre gamle navn ble slettet som uttrykkelig bestilt.

## Kontroller og avgrensning

- Før commit inneholdt `git diff --cached --name-only` nøyaktig de 14 bestilte CellProtocol-stiene og kun den ene bestilte Book-stien. De faktiske commitene ble kontrollert med `git diff-tree --no-commit-id --no-renames --name-only -r HEAD`; filsettene stemte.

- SHA-256 for alle 13 kildefiler ble sammenlignet med kopiene, staged Git-blobber og committede Git-blobber. Alt var identisk. Originalfilenes innhold var fortsatt uendret etter publisering og opprydding.

- Commit-meldingene ble sammenlignet med de bestilte tekstene. `git diff --cached --check` passerte i begge repoer.

- Opprinnelige arbeidstrærs gren, HEAD, index-oppføringer og tracked diff var uendret. Full Git-status var uendret før duplikatslettingen, og etter slettingen var de tre autoriserte usporede filene den eneste forskjellen før denne rapporten ble skrevet.

- Ingen andre filer ble tatt med i commitene. v1-filene er uendret på main. `Book/book_catalog.json`, andre Book-filer, eksisterende kode og andre tråders arbeid ble ikke endret eller stagert.

- Ingen kodeendringer, bygg, tester, installasjoner eller kjøring av pakkens bygge- og valideringsskript ble utført. De to bestilte Python-filene ble kun kopiert og publisert. Eksisterende valideringsresultater ble videreført uendret, ikke kjørt på nytt.

- Ingen bestilte publiserings- eller oppryddingssteg gjenstår.

Denne rapporten er skrevet lokalt til `CellProtocolDocuments/Deliverables/ENTITYDATA_V2_SAMMENSLAAING_2026-09-17.md`. Den er ikke stagert, committet eller pushet, slik at commitene inneholder nøyaktig de bestilte stiene. Originalfilene kan fortsatt vises som usporede på arbeidsgrenene selv om innholdet er publisert på `origin/main`.
