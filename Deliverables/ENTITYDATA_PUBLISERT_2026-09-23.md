# EntityData: UUID-håndheving og publisering, 23.09.2026

## Mål

1. Håndheve UUID-nøkler i `relations.records` gjennom byggesteget, med faste,
   oppdiktede UUID-er og sammenhengende referanser i eksempel og validatorfixtures.
2. Publisere de avgrensede 22.09/23.09-filsettene til `origin/main` i begge repoer,
   først etter grønne kontroller, uten Swift-endringer eller andre tråders arbeid.
3. Bekrefte fjern-SHA-er og byte-likhet mellom hver committet fil og arbeidsfilene.

## Påstander og evidens

- **UUID-kravet er håndhevet i målskjemaet.** `relations.records.propertyNames`
  bruker samme UUID-mønster som entitets- og identitetskartene, samt
  `maxLength: 36` for å avvise avsluttende linjeskift. Det tidligere unntaket
  er fjernet fra målskjemaets `deferredDecisions`.
- **Omskrivingen er reproduserbar og referansene henger sammen.** Grepet ligger
  i `apply_decisions_2026_09_23.py`. Begge skjemaer, eksempel og manifest er
  bygget av kjeden 16.09 → 22.09 → 23.09. Ingen skjemafil er håndredigert.
  Byggesteget kontrollerer inngangsform, kollisjoner og lokale stier før skriving.
- **Begge publiseringene er bekreftet.** Push lyktes på første forsøk i begge
  repoer. `git ls-remote --exit-code origin refs/heads/main` ga etter-SHA-ene
  nedenfor. Ingen rebase eller force-push var nødvendig.
- **Publiseringsomfanget er nøyaktig kontrollert.** `git diff --cached --name-only`
  var identisk med tillatelseslisten: 16 filer i CellProtocol og tre i
  CellProtocolDocuments. `git diff-tree` bekreftet de samme stiene etter commit.
- **Alle 19 filer er byte-like.** Etter push ble Git-blobben for hver fil
  sammenlignet med både filen i det opprinnelige arbeidstreet og filen i det
  rene publiseringsarbeidstreet. Alle sammenligninger passerte.
- **Dette er vedtatt målform, ikke Swift-implementasjon.** Historisk
  `EntityData.review.schema.json` er uendret. Kontrollene beviser målstruktur
  og de konkrete fiktive referansene, ikke runtime-dekoding eller wire-atferd.

## UUID-omskrivingen og hva den traff

| Gammel nøkkel | Fast, fiktiv UUID | Bruk |
|---|---|---|
| `relation-demo` | `40000000-0000-4000-8000-000000000001` | Publisert eksempel og validatorfixture |
| `rellea` | `40000000-0000-4000-8000-000000000002` | Validatorfixture for den andre kjente gamle nøkkelen |

I `EntityData.v2.example.json` ble seks forekomster omskrevet samlet:

1. Kartnøkkelen i `relations.records`.
2. Relasjonspostens `relationID`.
3. Den fiktive adressen `cell:///DemoContact/<relation-id>/1`.
4. `subject.validatedContactRef` sin sti til kontaktposten.
5. Kartnøkkelen i `relations.validatedContacts`.
6. Kontaktpostens `relationID`.

Eksempelets `supports.keypaths` peker til identitetens `domain` og nevnte ingen
av de gamle relasjonsnøklene. Eksempelet har ingen persistert `proofs.index`.
Begge bevissti-tilfellene ble derfor også prøvd i en egen validatorfixture:
`supports.keypaths` og nøklene i `proofs.index.byKeypath` ble omskrevet for
både `relation-demo` og `rellea`; bevis-UUID-referansene ble beholdt. Alle
stiene løses før og etter omskriving, og indeksen samsvarer med oppslaget
som kan bygges fra bevispostene.

Ingen gammel relasjons-ID gjenstår noe sted i det omskrevne eksempelet eller
den omskrevne positive fixturen. Hele dokumentene validerer, inkludert alle
kart der skjemaet krever UUID-nøkler. Gamle navn forekommer med hensikt som
inngangsdata til omskriving og som negative testdata som skal avvises.
Historiske runtime-fixtures er ikke omskrevet til en kontrakt de ikke bruker.

Ukjente forekomster av gamle ID-er, ukjent celleadresse med gammel ID,
kollisjoner, mismatchet `relationID`, manglende kontakt, uoppløselig bevissti
og ikke støttet escaping/selektorform gir eksplisitt feil. Ingen slik
uavklart referanse ble funnet i leveranseeksempelet. Celleadressen er et
fiktivt format-eksempel; ingen levende celle ble kontaktet.

## Kontrollresultater

| Kontroll | Resultat |
|---|---|
| Opprinnelig 23.09-suite før omskriving | 270 kontroller bestått |
| Oppdatert `validate_decisions_2026_09_23.py` | 301 kontroller bestått |
| Oppdatert `validate_decisions_2026_09_22.py` mot 23.09-målet | 235 kontroller bestått |
| Begge suiter i rent `main`-arbeidstre, med `python3 -B -O` | Samme grønne resultater |
| Begge Draft 2020-12-skjemaer og alle lokale skjemareferanser | Bestått |
| Eksempel og omskrevne positive fixtures; negative UUID- og referansetilfeller | Bestått |
| Ny bygging sammenlignet med leverte skjemaer, eksempel og manifest | Identiske byte |
| Lokale Markdown-filhenvisninger i publiseringssettet | 72 kontrollert, ingen manglende filer |
| `git diff --cached --check` i begge repoer | Bestått |
| Staged- og commit-stier mot nøyaktig tillatelsesliste | 16/16 og 3/3, ingen avvik |
| Etter push: Git-blob mot begge arbeidstrær | 19/19 byte-like |
| Visualiseringssjekkene | **Ikke kjørt** — utdaterte eksterne 16.09/17.09-artefakter |
| Swift/runtime, ekte dekoding og datamigrering | **Ikke kjørt** — utenfor oppgaven |
| Python jsonschema-banen | **Ikke kjørt** — modulen er ikke installert |
| Historisk 16.09-suite og `validate_review.py` | **Ikke kjørt** — historiske kontrakter; 16.09-suiten inkluderer utdaterte visualiseringskrav |
| GitHub Actions / fjern-CI | **Ikke kontrollert** — ingen CI-suksess påstås |

Faktisk validator var **Ajv 8.17.1 + ajv-formats 3.0.1**, via den eksisterende,
eksplisitte lokale adapteren. Ingen avhengigheter ble lastet ned.
Kontrollantall omfatter også skjemareferanser og mutasjonskontroller; de er
ikke antall uavhengige runtime-tester.

22.09-validatoren er videreført som regresjonssuite for den løpende modellen.
Den bevarer gruppe-/retningskontrollene og godtar de uttrykkelige
23.09-endringene i bevisformen. Gamle påstander om utsatt `records`-krav er
byttet til avvisningsprøver. Resultatfilen oppgir `targetDecisionsAsOf: 2026-09-23`.
De to historiske leveranserapportene er merket som historiske slik at gamle
SHA-er, kontrollantall og publiseringsstatus ikke fremstår som dagens målinger.
Den historiske bevisrapportens lenke til en upublisert `.sha256`-fil er
omgjort til en forklaring uten lenke.

Reproduksjon fra `CellProtocol/Docs/EntityData-Review-2026-09-11` i dette miljøet:

```sh
export ENTITYDATA_AJV_MODULE=/usr/local/lib/node_modules/@nestjs/cli/node_modules/ajv
export ENTITYDATA_AJV_FORMATS_MODULE=/usr/local/lib/node_modules/@nestjs/cli/node_modules/ajv-formats
python3 -B -O apply_decisions_2026_09_23.py
python3 -B -O validate_decisions_2026_09_22.py
python3 -B -O validate_decisions_2026_09_23.py
```

## Git-SHA-er før og etter

Før er hentet `origin/main` før publisering. Etter er både lokal commit og
fjernverdien fra `git ls-remote --exit-code origin refs/heads/main` etter push.

| Repo | Før `origin/main` | Etter `origin/main` |
|---|---|---|
| CellProtocol | `473357cf4efee831cb3b55ae87bc921d4bb63c10` | `7f9bdcffbf2f886238d8bfdf4f5f41937d5c00c7` |
| CellProtocolDocuments | `357f2cfa0b3f1587a751c29f36540ab19f24c4a1` | `b814a8187e3d35310d26824992412e2dab7a1b0b` |

De opprinnelige arbeidstrærne beholdt gren og HEAD:

| Repo | Gren | Uendret HEAD |
|---|---|---|
| CellProtocol | `pdd/tillitspakke-agentflaate` | `561d34a7ea785c087bd6036921f60debe6bace4a` |
| CellProtocolDocuments | `codex/docs-cleanup-20260810` | `c8029847502fe007833d1ebd371bcb5adc01c3ae` |

CellProtocols lokale `main` sto først på
`36372c5b95a7b57fbef92ffa54dea13bdf75a9e6` og ble fast-forwardet til hentet
`origin/main` i det nye arbeidstreet før filene ble kopiert inn. Ingen av
utgangsgrenenes øvrige commits eller uncommittede kode ble tatt med.

## Stier som faktisk ble committet

### CellProtocol — 16 filer

Commit-melding:

```text
docs: uuid keying, groups as their own root, and the proof store pattern

Owner decisions of 2026-09-22 and 2026-09-23 applied to the running target
schema. Data lives keyed by uuid; groups are unweighted member lists over
entities and get their own root; each edge is persisted in one direction and
the back edge is built at decode; proofs.credentials is the store and
byKeypath is derived from it.

Decided, not implemented. EntityData.review.schema.json is untouched and
still describes what the code stores today.
```

- `Docs/EntityData-Review-2026-09-11/BESLUTNING-UUID-OG-GRUPPER-2026-09-22.md`
- `Docs/EntityData-Review-2026-09-11/EntityData.v2.example.json`
- `Docs/EntityData-Review-2026-09-11/EntityData.v2.schema.json`
- `Docs/EntityData-Review-2026-09-11/EntityRepresentation.v2.schema.json`
- `Docs/EntityData-Review-2026-09-11/LES-MEG.md`
- `Docs/EntityData-Review-2026-09-11/OPPDATERT-ETTER-GJENNOMGANG-2026-09-16.md`
- `Docs/EntityData-Review-2026-09-11/TARGET-VALIDATION-2026-09-22.json`
- `Docs/EntityData-Review-2026-09-11/TARGET-VALIDATION-2026-09-23.json`
- `Docs/EntityData-Review-2026-09-11/V2-BESLUTTET-FORM.md`
- `Docs/EntityData-Review-2026-09-11/apply_decisions_2026_09_16.py`
- `Docs/EntityData-Review-2026-09-11/apply_decisions_2026_09_22.py`
- `Docs/EntityData-Review-2026-09-11/apply_decisions_2026_09_23.py`
- `Docs/EntityData-Review-2026-09-11/current-review.json`
- `Docs/EntityData-Review-2026-09-11/target_validation.py`
- `Docs/EntityData-Review-2026-09-11/validate_decisions_2026_09_22.py`
- `Docs/EntityData-Review-2026-09-11/validate_decisions_2026_09_23.py`

### CellProtocolDocuments — tre filer

Commit-melding: `docs(book): chapter 37 follows the 2026-09-22/23 target decisions`

- `Book/37_EntityData.md`
- `Deliverables/ENTITYDATA_BEVIS_2026-09-23.md`
- `Deliverables/ENTITYDATA_UUID_GRUPPER_2026-09-22.md`

## Avgrensninger og lokalt sluttresultat

- Ingen Swift-fil ble endret av denne oppgaven. SHA-256-sammenligning mot
  oppstart fant 554 uendrede Swift-filer i CellProtocol og 29 i dokumentrepoet.
  Alle øvrige kontrollerte filer utenfor publiseringslisten var også uendret:
  763 i CellProtocol og 3176 i dokumentrepoet, inkludert Swift-filene.
- `EntityData.review.schema.json` har fortsatt SHA-256
  `c62ca8f329d229101775158c61fdfce0b0874b0e00211820bea6fb10500c5e2f`.
- `build_v2_schema.py` og `IdentityLink-fixture.patch` er bekreftet fraværende
  i publisert CellProtocol-commit. Lokale levn er ikke slettet.
- Katalog, øvrige Book-kapitler, kunnskapsbase og alle andre tråders endringer
  er ikke staged eller publisert. Bokprosjekt-migrering er fortsatt utsatt.
- Denne sluttrapporten er **lokal og ikke committet**: dokumentrepoets
  uttrykkelige publiseringsliste tillot bare de tre filene over.
- Ingen generell escaped-nøkkelstioppløser, ekstern endpoint-verifikasjon,
  signaturvalidering, identitetslikhet eller brukerdata-migrering er implementert.

Begge rene `main`-arbeidstrær er beholdt og har ren Git-status:

- `_worktrees/entitydata-publish-20260923/CellProtocol`
- `_worktrees/entitydata-publish-20260923/CellProtocolDocuments`

Lokalt revisjonsgrunnlag, med filsummer per committet sti, tillatelsesliste,
oppstartsstatus og SHA-kontroller, ligger i
`_worktrees/entitydata-publish-20260923-evidence/` under HAVEN-roten.
