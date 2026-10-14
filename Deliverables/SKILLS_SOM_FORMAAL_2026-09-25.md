# Skills som formål — 25.09.2026

Dokumentasjon og målskjema. **Besluttet, ikke implementert i Swift.**

## Mål

1. Fjerne hele `person.skills[]` fra den delte `PersonProfile` og håndheve at nøkkelen avvises.
2. Beskrive skills som vanlige formål i grafen, med påkrevd og målbart `goal`.
3. Undersøke eksisterende beviskobling uten å innføre et erstatningsfelt.
4. Bygge reproduserbart etter 23.09-steget, bevare tidligere kontroller og publisere bare avtalte dokumentasjonsstier til `origin/main`.

## Påstander og belegg

| Grep | Observert resultat |
|---|---|
| Nytt byggesteg | `apply_decisions_2026_09_25_skills.py` bygger 16.09 → 22.09 → 23.09 → undergrupper → skills som formål i minnet og validerer før skriving. Ingen skjemafil er håndredigert. |
| Skill-listen | Hele `$defs.PersonProfile.properties.skills` er fjernet, med `label`, `level`, `taxonomyRef` og `evidenceRefs`. Ingen avledet skill-liste beholdes. |
| Faktisk avvisning | `PersonProfile.additionalProperties` var `true`. Derfor avvises nøkkelen eksplisitt med `not: {required: [skills]}`. Urelatert profilutvidbarhet er bevart. |
| Samme grafmodell | Beskrivelsene ved `purposes`, `entityRepresentation` og de delte nodene sier at en skill er et formål brukeren hevder å kunne oppfylle. Ingen ny `Skill`-type eller `SearchPurpose`. |
| Villet friksjon | `Purpose.goal` er fortsatt påkrevd. Beskrivelsene sier uttrykkelig at en skill uten målbart resultat ikke kan uttrykkes i denne formen. Skjemaet kan kreve konfigurasjonen, men ikke bevise målbarheten. |
| Eksempel | Fiktiv eier med én vanlig Purpose-node i `entityRepresentation.purposes`: levere nøyaktig tre tilgjengelige nettsider, med null brutte interne lenker. Fast node-uuid `60000000-0000-4000-8000-000000000001`. Ingen ny målecelle er implementert. |
| Eksisterende eksempel | Ingen `skills`-oppføring fantes fra før; ingen finnes etterpå. Alle tidligere eksempeldata, inkludert bevis og grupper, er bevart. Uventede gamle skill-data stopper byggingen fremfor å slettes stille. |
| Bevis | `evidenceRefs` følger listen ut. `proofs.credentials` og `supports.keypaths` er uendret. Stabil adressering av én formålsnode er en målt, åpen sperre; se nedenfor. |
| Strenge grep | 35 slettede inngangsmål gir eksplisitt feil. Gjentatt anvendelse, ufullstendig gammel skill-post og uventede skill-data feiler høylytt. Kjørt med `python -O`; ingen avhengighet av avslåbare `assert`-setninger. |
| Avgrensning | Objektlikhet etter reversering av bare avtalte endringer viser at øvrig skjemakontrakt er bevart. Ingen Swift-fil er endret. |
| Dokumentasjon | Beslutningen, målformens forklaring, LES-MEG og bare Book-kapittel 37 er oppdatert. Kapittelets gamle åpne spørsmål om skills er fjernet. Book-inventaret er uendret. |

Beslutningsavsnittet fra 25.09 fantes i eierens opprinnelige, urene CellProtocol-arbeidstre,
men ikke på hentet `origin/main`. Den relevante eierbeslutningen er innarbeidet i
publiseringsversjonen med overskriften «Avklart 25.09.2026: konteksten bor i PerspectiveCell».
Tidligere publiserte bevis- og undergruppebeslutninger er bevart; den urene filen ble ikke
kopiert over main-versjonen. Sporform, grovhet og levetid er fortsatt uavklart.

## Hva som skjedde med evidenceRefs

Feltet er borte sammen med skill-listen i begge målskjemaene. Det er ikke flyttet til
`Purpose` og ikke erstattet av et oppfunnet felt. Bevis skal fortsatt bo i
`proofs.credentials`; `supports.entityRef` beskriver entiteten, og `supports.keypaths`
bærer påståtte nøkkelstier.

Kontrollen skiller mellom lagring av en streng og en løst referanse:

- Skjemaet godtar en forsøkt indekssti `entityRepresentation.purposes.0.value` og en
  forsøkt selektorsti som peker på `value.nodeIdentifier`, fordi det bare krever
  ikke-tomme strenger. Forsøkene er negative testdata, ingen ny syntakskontrakt.
- Dagens `resolve_fixture_keypath` og `fixture_errors` kan ikke løse noen av dem.
  De håndterer objektstier, mens `purposes` er en liste av vektede `value`/`reference`-kanter.
- Stien til hele `entityRepresentation.purposes` kan løses, men gir listen, ikke den
  bestemte noden. Indeksadressering ville dessuten være ustabil ved omordning.
- Stabil nodeadressering, og oppførsel når en kant blir en `reference`, må avklares.
  Roten `purposes` har heller ikke en ferdig kontrakt for lagringsorganiseringen.

Dette står som **åpen sperre** i beslutningsdokumentet og i skjemaenes
`x-haven.deferredDecisions`. Det hevdes ikke at koblingen er løst. Eksempelet har ingen
ny skill-credential. Den eksisterende fiktive identitetsbeviskoblingen validerer fortsatt.
`supports` og bevisoppslaget er dessuten fortsatt ikke implementert i Swift.

## Kontrollresultater

[Maskinlesbart resultat](../../CellProtocol/Docs/EntityData-Review-2026-09-11/TARGET-VALIDATION-2026-09-25-SKILLS.json):
**208 kontroller bestått**, med **Ajv 8.17.1 + ajv-formats 3.0.1**.
Antallet inkluderer lokale skjemareferanser og mutasjonskontroller, ikke runtime-tester.

| Kontroll | Resultat |
|---|---|
| `person.skills`: tom liste, full gammel post, null, objekt, streng | Avvist |
| Delt `PersonProfile` i begge skjemaer og typet kontaktprofil | `skills` avvist |
| Eksempel, full EntityRepresentation og skill som vanlig Purpose | Validerer |
| Manglende eller null `goal` | Avvist |
| Målkonfigurasjon med bare navn | Godtas av skjemaet; målbart resultat er et semantisk krav, ikke bevist av schema |
| Begge skjemaer | Gyldig Draft 2020-12, alle lokale `$ref` løses |
| Ny bygging | Byte-identiske skjemaer, eksempel og manifest |
| Bevislager og supports, øvrige Purpose-felt, grupper og relasjoner | Uendret kontrakt |
| Tidligere identitetsbevis, relasjonsreferanser og gruppereferanser | Løses |
| Skill-bevisstier | Skjema godtar strengen; eksisterende referanseverktøy avviser — sperren er eksponert |
| Historiske 22.09-, 23.09- og undergruppesuiter | Uendret kjørt mot sine historiske målformer i midlertidig kopi: **235 / 301 / 217** bestått |
| Ugyldig bokprosjekt-form, gruppesykel og gruppe som medlem mot nytt mål | Fortsatt avvist på henholdsvis skjema- og referansenivå |
| Python-syntaks og `git diff --check` | Bestått |

De historiske suitene krever gamle byte og den tidligere skill-listen. De kjøres derfor
mot sine egne målformer, uten å overskrive dagens mål eller gamle resultatfiler.
Den nye suiten sammenligner hele kontrakten etter at bare tillatte endringer er reversert,
og kjører i tillegg regresjonsprøver mot den nye målformen.

### Ikke kjørt og gjenstående begrensninger

- **Visualiseringssjekkene: ikke kjørt.** Den historiske suiten leser utdaterte eksterne
  16.09/17.09-artefakter; oppdaterte 25.09-artefakter og kontroller mangler.
- **Swift/runtime, målecelle, ekte dekoding og migrering: ikke kjørt.** Oppgaven er
  dokumentasjon og målskjema. Ingen måling av en virkelig skill hevdes.
- **Python jsonschema-banen: ikke kjørt.** Den eksisterende lokale Ajv-banen er valgt
  eksplisitt. Ingen avhengigheter ble lastet ned.
- **Historisk 16.09-suite / validate_review.py: ikke kjørt.** Historiske kontrakter;
  16.09-suiten inkluderer de utdaterte visualiseringskravene.
- **GitHub Actions: ikke kjørt av denne jobben; ingen fjern-CI-suksess påstås.**
- **Beviskobling til én skill-node: ikke løst.** Dette er den etterspurte åpne sperren,
  ikke en utelatt implementasjonsoppgave. Ingen erstatningsfelt er innført.

## Reproduksjon

Fra `CellProtocol/Docs/EntityData-Review-2026-09-11`:

```sh
export ENTITYDATA_AJV_MODULE=/usr/local/lib/node_modules/@nestjs/cli/node_modules/ajv
export ENTITYDATA_AJV_FORMATS_MODULE=/usr/local/lib/node_modules/@nestjs/cli/node_modules/ajv-formats
python3 -B -O apply_decisions_2026_09_25_skills.py
python3 -B -O validate_decisions_2026_09_25_skills.py
```

## Publisering

Nye, isolerte utsjekkinger med lokal gren `main`, ren indeks og hentet `origin/main`:

- `_worktrees/skills-formaal-20260925/CellProtocol`
- `_worktrees/skills-formaal-20260925/CellProtocolDocuments`

Det tidligere CellProtocol-main-arbeidstreet fra 23.09 hadde staged Swift-endringer.
Derfor er de nye arbeidstrærne separate lokale kloner med delt Git-objektlager,
men egen indeks og egen `main`-referanse. `origin` peker til de opprinnelige GitHub-repoene.
Verken eksisterende staged arbeid, opprinnelige urene arbeidsgrener eller deres HEAD-er
brukes til publisering eller endres av jobben.

| Repo | Før: hentet origin/main | Etter: innholdscommit |
|---|---|---|
| CellProtocol | `63975cd4aeb79595f24cdf1d7f75b9713b9eeb13` | `a40ceeb8af05e1c06b111500b50427bf08bdf4e6` |
| CellProtocolDocuments | `af04ea5569841c68da598f14e3af98b46f217cf9` | `3e972c5bfc9572f4b1971b8f36fa8669915c3236` |

CellProtocol ble først committet som `16615c5ac82d5c5f62bea2fa74c75ab556e8d678`, med
nøyaktig eierens commit-melding. Første push ble avvist som non-fast-forward.
`git pull --rebase` lyktes; ett nytt push-forsøk lyktes med SHA-en i tabellen.
`git ls-remote --exit-code origin refs/heads/main` bekreftet
`a40ceeb8af05e1c06b111500b50427bf08bdf4e6`. Alle ti filer var byte-like med arbeidstreet,
og faktiske commit-stier var eksakt lik tillatelseslisten. Ingen force-push.
Rebasen endret ingen av de ti gjennomgåtte filene. Den tok inn
`5609a9a` (bridge-konkurrens og tilhørende tester/workflows); ingen inngangsfil til
skjemabyggingen eller skjemakontrollene ble endret. CellProtocol-arbeidstreet er rent.

CellProtocolDocuments: innholdscommit `3e972c5bfc9572f4b1971b8f36fa8669915c3236`
ble pushet på første forsøk, uten rebase. `git ls-remote` bekreftet samme SHA.
Begge publiserte filer var byte-like med arbeidstreet, og commit-stiene var eksakt
lik to-filslisten. Arbeidstreet var rent etter push.

Denne etterfølgende oppdateringen endrer bare rapporten for å dokumentere observerte
publiseringsresultater. Rapportens egen endelige commit-SHA kan ikke skrives inn i seg selv;
den finnes med `git log -1 --format=%H -- Deliverables/SKILLS_SOM_FORMAAL_2026-09-25.md`.
Etter hver push kontrolleres fjern-SHA og byte-likhet. Den endelige kvitteringen lagres
lokalt som `_worktrees/skills-formaal-20260925-evidence/CellProtocolDocuments-report-published.json`
og oppgis i leveringsmeldingen.

### Faktisk committede stier — CellProtocol (10 filer)

- `Docs/EntityData-Review-2026-09-11/BESLUTNING-UUID-OG-GRUPPER-2026-09-22.md`
- `Docs/EntityData-Review-2026-09-11/EntityData.v2.example.json`
- `Docs/EntityData-Review-2026-09-11/EntityData.v2.schema.json`
- `Docs/EntityData-Review-2026-09-11/EntityRepresentation.v2.schema.json`
- `Docs/EntityData-Review-2026-09-11/LES-MEG.md`
- `Docs/EntityData-Review-2026-09-11/TARGET-VALIDATION-2026-09-25-SKILLS.json`
- `Docs/EntityData-Review-2026-09-11/V2-BESLUTTET-FORM.md`
- `Docs/EntityData-Review-2026-09-11/apply_decisions_2026_09_25_skills.py`
- `Docs/EntityData-Review-2026-09-11/current-review.json`
- `Docs/EntityData-Review-2026-09-11/validate_decisions_2026_09_25_skills.py`

### Faktisk committede stier — CellProtocolDocuments (2 filer)

- `Book/37_EntityData.md`
- `Deliverables/SKILLS_SOM_FORMAAL_2026-09-25.md`

Før begge innholdscommitene ble `git diff --cached --name-only` kontrollert eksakt
mot den aktuelle listen: ti filer i CellProtocol, to i CellProtocolDocuments.
Faktiske commit-stier er også kontrollert. Rapportoppdateringen har en egen liste
med bare `Deliverables/SKILLS_SOM_FORMAAL_2026-09-25.md`, kontrollert på samme måte
før commit. Ingen andre stier stages i rapportoppdateringen.
`build_v2_schema.py` og `IdentityLink-fixture.patch` er uttrykkelig utelatt.
Ingen andre Book-filer eller kataloger inngår.

42 lokale Markdown-lenker og deres ankere er kontrollert; alle finnes.
`git diff --check` er grønn i begge repoer.

Bytekontrollen før første publiseringsforsøk bekrefter at **848** øvrige sporede CellProtocol-filer
(inkludert **596 Swift-filer**) og **610** øvrige dokumentrepo-filer (inkludert **2 Swift-filer**)
er uendret. Runtime-grunnlaget `EntityData.review.schema.json` har fortsatt SHA-256
`c62ca8f329d229101775158c61fdfce0b0874b0e00211820bea6fb10500c5e2f`.

Eksplisitte tillatelseslister, oppstartsstatus, SHA-256-snapshots og publiseringskvitteringer
ligger lokalt under `_worktrees/skills-formaal-20260925-evidence/`.

## Filsummer før og etter

Før er hentet `main`; etter er arbeidsfilene som publiseres. Rapporten selv er utelatt
fra tabellen fordi den ikke kan inneholde sin egen endelige hash.

| Fil | SHA-256 før | SHA-256 etter |
|---|---|---|
| `CellProtocol/Docs/EntityData-Review-2026-09-11/BESLUTNING-UUID-OG-GRUPPER-2026-09-22.md` | `7662c7934b9365bbe33a5da383c23cd460664b4f5fc43933e6195c5af406cb17` | `c4f5357f2892ee81c8b1a48a92d9a14935812cefbcbf24180df06a75fb67da26` |
| `CellProtocol/Docs/EntityData-Review-2026-09-11/EntityData.v2.example.json` | `b4ccf189eb242fa41c6ba10ac61b3faab388eb9f01aa5548d9190e3494327ca2` | `b084cba2336068a949b7e89cd23fe569327a811408785c20fde176c5e15a18da` |
| `CellProtocol/Docs/EntityData-Review-2026-09-11/EntityData.v2.schema.json` | `fd72be5b91471a7fec4f5e55bffb78bf40ea738f19ec3f1f864621cd6a9e943a` | `598f7462270a766b8c15a03d6220b8e5a81c19912fd89bafe1f5ab9e373dc576` |
| `CellProtocol/Docs/EntityData-Review-2026-09-11/EntityRepresentation.v2.schema.json` | `5a2f1df727db99ee45269293744c82422bdc7097e0bdf9de2c94c74f5580e9a8` | `cad7e2e989d1214d66feb38fc15f182a1d13f00a842e89435039668542a131bd` |
| `CellProtocol/Docs/EntityData-Review-2026-09-11/LES-MEG.md` | `8688c28f0ce9b570c319a280b6b47ac73e2d35fdf4d455883f8c0dd2dd17f39d` | `b06cd7ec9f571aec45b307a07a1a1c08ea0fcdfc163d60cf31ec0ea604eaf72b` |
| `CellProtocol/Docs/EntityData-Review-2026-09-11/TARGET-VALIDATION-2026-09-25-SKILLS.json` | `ny fil` | `b8259e7504b67d06aac2f9df26337fd2c3caa7d9b2e72aa2762e4e449c36dca6` |
| `CellProtocol/Docs/EntityData-Review-2026-09-11/V2-BESLUTTET-FORM.md` | `12db425075d718987c96e62aa9da656b635d4099ea24cade6dd8b4b00f1a3dbe` | `1b8db009ae7a35f1de67249b766fd951cceed142a78cd358a772c5ebe5f36056` |
| `CellProtocol/Docs/EntityData-Review-2026-09-11/apply_decisions_2026_09_25_skills.py` | `ny fil` | `48832de6f03b13047ccf101d94accc954cb5cfc76d110ab4aaa94021d86e8001` |
| `CellProtocol/Docs/EntityData-Review-2026-09-11/current-review.json` | `acbff7858317709ded570d4fc89ca1c5addf62a75a47fe63041fa3e305a5ae62` | `50b4a7d2d27a42e809467a7fbb297878f9c7e9b9891ef7fd5e3b5940aeb2f7ab` |
| `CellProtocol/Docs/EntityData-Review-2026-09-11/validate_decisions_2026_09_25_skills.py` | `ny fil` | `866a0e43c42f7ad3debb34d98ce4e39fce2c06b6cdc0c542e3b3dbce13904157` |
| `CellProtocolDocuments/Book/37_EntityData.md` | `740e6328902ebeb79cee4fda6fc3dbcd967f892883c238c69e2d4371d9fb8791` | `4a7a1598b41db2fd1642c0b8b12fa7e2b0c09cce5621bebd92f8bb3a3614217d` |
