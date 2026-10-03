# EntityData: bevismønster, 23.09.2026

**Historisk delrapport før UUID-omskriving og publisering.** Målingene og
SHA-256-tabellen nedenfor gjelder den opprinnelige bevisleveransen.
23.09-steget håndhever nå også UUID-nøkler i `relations.records`, og
referansene er omskrevet samlet. De lenkede validatorresultatene er kjørt
på nytt: 301 kontroller i 23.09-suiten og 235 i 22.09-regresjonssuiten,
med Ajv 8.17.1 + ajv-formats 3.0.1. Visualiseringssjekkene er **ikke kjørt**.

Dokumentasjon og målskjema er oppdatert i arbeidstreet. Ingen Swift-endringer,
commit, push, merge, staging eller migrering av ekte data er utført.

Fasit er [«Løst 23.09.2026: følg entityRepresentation-mønsteret»](../../CellProtocol/Docs/EntityData-Review-2026-09-11/BESLUTNING-UUID-OG-GRUPPER-2026-09-22.md#løst-23092026-følg-entityrepresentation-mønsteret).
[22.09-rapporten](ENTITYDATA_UUID_GRUPPER_2026-09-22.md) og dens kontrollresultater
står urørt som historisk evidens. De lot bevis stå urørt med vilje.

## Mål

1. Ett persistert, flatt bevislager i `proofs.credentials`, nøklet på bevis-uuid.
2. Hver bevispost bærer en påstand om hva den understøtter: entitets-uuid og
   eierens nøkkelstier. Beskriv bare de seks etterspurte VCClaim-feltene og dette tillegget.
3. Dokumenter `proofs.index.byKeypath` som avledet ved dekoding, uten å fjerne
   oppslagsformen eller gjøre den til en andre kilde.
4. Beskriv alle bevisrettede `proofRefs`/`evidenceRefs` som uuid-referanser inn
   i lageret, uten formendring.
5. Viderefør 22.09-resultatet med et nytt, strengt byggesteg, et gyldig eksempel,
   positive/negative kontroller og etterprøvbare filsummer.

## Påstander og observerte resultater

| Grep | Traff? | Resultat og belegg |
|---|---|---|
| `proofs.credentials` | Ja | `propertyNames.pattern` og `maxLength: 36` krever UUID-form, også uten avsluttende linjeskift. Beskrivelsen sier ett persistert, flatt lager og ett sted der bevispostene bor. Fire prøver med ikke-uuid-nøkler avvises. |
| Bevispostens felter | Ja | `uuid`, `type`, `issuer`, `issuanceDate`, `credentialSubject`, `proof`, samt nytt `supports`. Alle sju kreves; andre toppfelter avvises. Felttypene følger de seks etterspurte Swift-feltene. Ingen nye verifikasjons-, status- eller tillitsfelter er lagt på bevisposten. |
| `supports` | Ja | Påkrevd objekt med `entityRef` (entitets-uuid) og `keypaths` (minst én unik, ikke-tom nøkkelstistreng i eierens EntityData). Ingen andre underfelter. Navnet og beskrivelsen er en påstand om understøttelse, ikke gyldighet. Merket som ikke implementert i Swift. |
| Grense for oppslag | Ja | Beskrivelsen sier uttrykkelig at oppslag ikke fastslår sannhet, gyldighet, utstedertillit eller samtykke. Gjelder `supports`, bevisposten, `byKeypath` og referansebeskrivelsene. |
| `proofs.index.byKeypath` | Ja | Formen nøkkelsti → liste av bevisreferanser er bevart. Beskrivelsen sier at den bygges fra `supports.keypaths` ved dekoding, med entitetskontekst på posten, og forklarer parallellen til `entityRepresentationNameReferences`/`name`. Ingen persistert sannhet eller andre kilde. |
| Indeksmetadata | Ja | `index`, `byKeypath` og verdi-listene har `derived: true`, `persisted: false`, `storageDomain: memory`, `mutability: read-only`, `runtimeImplemented: false`. Kilden er `proofs.credentials`. Dette er målmetadata, ikke implementert lagringsatferd. |
| `relations.identities.*.proofRefs` | Ja | Beskrivelsen peker inn i `proofs.credentials` på bevis-uuid. Hele definisjonen utenom `description` er byte-/verdimessig uendret. |
| `$defs.PersonProfile.affiliations[].proofRefs` | Ja | Samme referanseavklaring, uendret form. |
| `$defs.PersonProfile.skills[].evidenceRefs` | Ja | Samme referanseavklaring, uendret form. |
| `$defs.PersonProfile.attributes[].proofRefs` | Ja | Samme referanseavklaring, uendret form. |
| Fiktivt eksempel | Ja | Bevis `50000000-0000-4000-8000-000000000001` ligger i lageret, bærer `supports` og refereres av identitetspostens `proofRefs`. Entitet, identitet, nøkkelsti og bevisreferanse finnes i eksempelet. Ingen persistert indeks. |
| Nytt byggesteg | Ja | `apply_decisions_2026_09_23.py` tar hele resultatet fra 22.09-steget videre i minnet. 16.09 → 22.09 → 23.09 valideres før skriving. Skjemaene og eksempelet er generert, ikke håndredigert. |
| Manglende mål gir feil | Ja | 58 faktisk brukte skjemamål er fjernet enkeltvis; hvert tilfelle stopper med eksplisitt feil. Tre manglende eksempelmål og elleve manglende manifest-/grafmål stopper også. Gjentatt anvendelse og uventede eksisterende kontraktfelter avvises. Kontrollene virker med `python -O`. |
| Grafskjema og manifest | Ja | Grafskjemaet får identiske delte `$defs`, inkludert de tre PersonProfile-beskrivelsene. Filnavn og `$id` er beholdt. `current-review.json` peker på 23.09-kommandoene og hele kjeden. Den gamle bevis-sperren i `deferredDecisions` erstattes av eksplisitt uimplementert runtime-status. |
| Dokumentasjonsinnganger | Ja | `V2-BESLUTTET-FORM.md`, innledningen til `LES-MEG.md` og bevisomtalen i `Book/37_EntityData.md` viser gjeldende mål og skiller det fra Swift. Ingen Book-inventarendring; katalogen er urørt. |
| Avgrensning mot tidligere arbeid | Ja | Helhetssammenligning viser at øvrig datakontrakt fra 22.09 er uendret, inkludert grupper, relasjoner og bokprosjekt. Runtime-grunnlag, gamle byggesteg, historiske rapporter/resultater og beslutningskilden er urørt. |

### Det konkrete eksempelet

Beviset gjelder entiteten `10000000-0000-4000-8000-000000000001` og nøkkelstien
`relations.identities.20000000-0000-4000-8000-000000000001.domain`.
Entitetens `identityRefs` peker til denne identiteten. Identitetens `proofRefs`
peker til bevisets uuid. `credentialSubject` har en fiktiv påstand om domenet.
`proof: {}` er bare et objekt i et struktureksempel, ingen gyldig signatur.

Den separate eksempelsjekken bygger oppslaget utelukkende fra bevispostene og
får `{ "<nøkkelstien over>": ["50000000-0000-4000-8000-000000000001"] }`.
Den ignorerer også en tilført, utdatert indeks. Dette viser at eksempelet bærer
tilfredsstillende oppslagsdata; det er **ikke** en implementasjonstest av Swift-dekoding.

## Kontroller

[Maskinlesbart resultat](../../CellProtocol/Docs/EntityData-Review-2026-09-11/TARGET-VALIDATION-2026-09-23.json):
**270 strukturkontroller bestått**, kjørt med **Ajv 8.17.1 + ajv-formats 3.0.1**.
Antallet omfatter blant annet lokale `$ref`-oppslag og mutasjonskontroller;
det er ikke 270 uavhengige runtime-tester.

| Kontroll | Resultat |
|---|---|
| EntityData og EntityRepresentation er gyldige Draft 2020-12-skjemaer | Grønn |
| Alle lokale skjemareferanser kan slås opp | Grønn |
| Det oppdaterte eksempelet validerer | Grønn |
| Tomt lager og delvis EntityData `{}` tillates fortsatt | Grønn |
| Ikke-uuid som bevisnøkkel avvises | Grønn |
| Bevis uten `supports` avvises | Grønn |
| Manglende øvrige påkrevde bevisfelter avvises | Grønn |
| Manglende entitet/nøkkelstier, ugyldig entitets-uuid, tom eller gjentatt nøkkelsti avvises | Grønn |
| Feil VCClaim-felttype og ugyldig `issuanceDate` avvises; objekt-utsteder og flere stier tillates | Grønn |
| Ingen formendring av de fire referansefeltene eller indeksformen | Grønn |
| Alle nye eksempelreferanser løses; feil uuid-likhet, ukjent entitet, sti og bevisref oppdages separat | Grønn |
| Rekonstruksjon fra lageret uten indeks; tilført gammel indeks ignoreres | Grønn, kun fiktiv eksempelsjekk |
| Ny bygging gir identiske byte for begge skjemaer, eksempel og manifest | Grønn |
| Uventede/manglende mål og gjentatt transformasjon feiler høylytt | Grønn, også med `-O` |
| Øvrig 22.09-kontrakt og historisk runtime-grunnlag er bevart | Grønn |

Første kjøring av den nye testsuiten fant en feil i testhjelperen: en tom
rotsti ble behandlet som et slettbart felt. Testhjelperen ble rettet til å
mutere faktiske mål; den endelige kjøringen ovenfor passerte. Ingen skjemakrav
ble svekket for å få kontrollene grønne. Sluttkontrollen la til maksimal lengde
36 for de nye UUID-feltene og tre negative linjeskiftprøver: regexens `$` alene
kan slippe gjennom et avsluttende linjeskift. Det delte UUID-mønsteret er bevart.

### Ikke kjørt

- **Visualiseringssjekkene: ikke kjørt.** Den historiske suiten leser
  `/Users/kjetil/.codex/visualizations/2026/09/11/01a090eb-528a-76d3-87d1-41a0b84f4d47`,
  utenfor repoet. Artefaktene er utdaterte fra 16.09/17.09; ingen oppdaterte
  23.09-artefakter er levert. De er ikke endret eller brukt som bestått evidens.
- **Swift/runtime, ekte dekoding og migrering: ikke kjørt.** Oppgaven er
  dokumentasjon og skjema; det nye feltet og bevisindeksens dekoding er ikke
  implementert i Swift.
- **Python jsonschema-banen: ikke kjørt.** `import jsonschema` ga
  `ModuleNotFoundError`. Den eksisterende eksplisitte, lokale Ajv-banen ble
  brukt i stedet. Ingen avhengigheter ble lastet ned.
- **Den historiske 22.09-validatoren mot 23.09-målet: ikke kjørt.** Den krever
  med vilje urørt `proofs` og 22.09-byte. Den nye suiten sammenligner resten av
  datakontrakten mot 22.09-resultatet; gammel evidens er bevart som historisk.

## Kildegrunnlag og begrensninger

[VCClaim.swift](../../CellProtocol/Sources/CellBase/VerifiableCredentials/VCClaim.swift)
er lest: de seks etterspurte feltene har de beskrevne typene; `IssuerType` er
strengreferanse eller innebygd objekt. `supports` finnes ikke der. Dette
målskjemaet gjengir det etterspurte feltutvalget, ikke hele dagens Swift-wireformat.
Ingen interne `VCProof`-felter eller valideringsresultater er oppfunnet.

[Perspective.swift](../../CellProtocol/Sources/CellBase/PurposeAndInterest/Perspective.swift)
er lest: `InterestsAndPurposesContainer` enkoder de flate postene, dekodingen
registrerer dem i Facilitator, og Perspective har oppslagskartene som beskrives
i fasiten. Dette underbygger mønsteret; det beviser ikke en ny bevisimplementasjon.

JSON Schema håndhever struktur og det valgte UUID-mønsteret, ikke referanse-
oppløsning, entitetslikhet, at kartnøkkel og `uuid` er samme verdi, eller at en
nøkkelsti finnes. Eksempelsjekken dekker konkrete referanser og enkle stier,
ikke generell escaping/selektorlogikk. De historisk åpne listeelementene i
`proofRefs`/`evidenceRefs` og `byKeypath` er fortsatt åpne, som pålagt.

`x-haven.persisted=false` er dokumentasjonsmetadata; det forbyr ikke indeksen
via JSON Schema. Formen er med for lesbarhet, og fremtidig runtime må bygge
indeksen og utelate den ved lagring. Signatur, sannhet, gyldighet,
utstedertillit og samtykke avgjøres ikke av disse kontrollene.

`relations.records` sitt utsatte UUID-mønster, bokprosjekt-migreringen og
øvrige spesialiserte `proofs`-undertrær er urørt. Dette arbeidet hevder ikke
at disse eldre strukturene er migrert til det nye lageret.

## Reproduksjon

Fra `CellProtocol/Docs/EntityData-Review-2026-09-11` i dette miljøet:

```sh
export ENTITYDATA_AJV_MODULE=/usr/local/lib/node_modules/@nestjs/cli/node_modules/ajv
export ENTITYDATA_AJV_FORMATS_MODULE=/usr/local/lib/node_modules/@nestjs/cli/node_modules/ajv-formats
python3 -B -O apply_decisions_2026_09_23.py
python3 -B -O validate_decisions_2026_09_23.py
```

Den nye validatoren bruker eksisterende `target_validation.py`, som er urørt.
Kjør siste byggesteg; de gamle byggeskriptene alene skriver historiske mellomsteg.
Alle transformasjoner og skjemakontroller skjer før målfilene skrives.

Etter sluttkjøringen ble 51 lokale Markdown-lenker i de berørte dokumentene
kontrollert; alle peker til eksisterende filer. De leverte filene har ingen
avsluttende blanktegn. Sammenligning av 425 oppstartsfiler fant ingen uventede
endringer. SHA-256-kontrollfilen er verifisert med alle elleve oppføringer grønne.

## SHA-256 før og etter

Før betyr faktiske arbeidsfiler ved oppstart, ikke Git HEAD. Nye filer har
ingen før-SHA. Begge repoer var allerede urene, og gjennomgangsmappen var
allerede usporet; eksisterende arbeid er bevart. De sju endrede eksisterende
filene og tre nye bygg-/kontrollartefaktene er listet nedenfor.

| Fil | Før SHA-256 | Etter SHA-256 |
|---|---|---|
| [apply_decisions_2026_09_23.py](../../CellProtocol/Docs/EntityData-Review-2026-09-11/apply_decisions_2026_09_23.py) | — (ny fil) | `7b7a09f7e0e1db7fb889ac3a20c92e1bbc53b3a376ef36fa1cbe2d2f7f49d74d` |
| [validate_decisions_2026_09_23.py](../../CellProtocol/Docs/EntityData-Review-2026-09-11/validate_decisions_2026_09_23.py) | — (ny fil) | `873c048b3b035edcad2361780d6b2b8ae81e5991084435100d1f32aab6b596e0` |
| [EntityData.v2.schema.json](../../CellProtocol/Docs/EntityData-Review-2026-09-11/EntityData.v2.schema.json) | `b7211f3dd361c5f39c5bcfa499b09ca9b3bbf54e4e43fcd098fe88b6cbb0d9f4` | `cd033cc187ba1e1b580df6cfe378d117db71080f405062b7af7854cc0d2329b0` |
| [EntityRepresentation.v2.schema.json](../../CellProtocol/Docs/EntityData-Review-2026-09-11/EntityRepresentation.v2.schema.json) | `7720d80e07035d87e3518c61ea20f73ee62787a0aded6743fee41eafdf67a65d` | `991fe543967e1f1910677fad304e45766ba6d0da58d1dd3a0dd9fad165f63032` |
| [EntityData.v2.example.json](../../CellProtocol/Docs/EntityData-Review-2026-09-11/EntityData.v2.example.json) | `cc4df57f7647869838685652415daab4122296069c6c5f70255550fada5b643b` | `6c478126b255198be7fd4afd90bcd41e699b7b4ebddef72bad626987acaca79f` |
| [current-review.json](../../CellProtocol/Docs/EntityData-Review-2026-09-11/current-review.json) | `fc38bc87c2a5577c15ccb0da28fb37996066a5a67556764ac6480e7b04c335ee` | `c81a66067c3d8cb10b88661e31dba2c7377bfb8bf95f3c8e2c788d5d9aef4c00` |
| [TARGET-VALIDATION-2026-09-23.json](../../CellProtocol/Docs/EntityData-Review-2026-09-11/TARGET-VALIDATION-2026-09-23.json) | — (ny fil) | `8a4dd0f45efd8839f6facb44e6ee137cda32f25098216caa96c509c9f614cbb0` |
| [V2-BESLUTTET-FORM.md](../../CellProtocol/Docs/EntityData-Review-2026-09-11/V2-BESLUTTET-FORM.md) | `2b0c9068c996fa78f98eac2dd52d91a2a269d2a8222b1df1874e6aabed3ddbaa` | `2e37f5e08c39d92e55ba6f034b0787275314f6b4dc04986ceabdd999cace93ef` |
| [LES-MEG.md](../../CellProtocol/Docs/EntityData-Review-2026-09-11/LES-MEG.md) | `c271954b0cc67dda9f2ac4c75968d2feb039375937310a9cd768312770ab1deb` | `90add0472f5c837a9df5f43e761f181b679d6e96eb05c2f49cb6e8651e076b3a` |
| [37_EntityData.md](../Book/37_EntityData.md) | `5e3e745837caf2b992725046f5abc60bd54b028e4f3944b38988e167b78fb33c` | `284b76f9a613c6b7083ca85bc7b11c010056404d5eb75bd32b3e1f98b273c74e` |

Rapporten var ny ved den opprinnelige leveransen (ingen før-SHA).
Den daværende lokale kontrollfilen `ENTITYDATA_BEVIS_2026-09-23.sha256`
tilhører det historiske arbeidsøyeblikket og publiseres ikke. Den er ikke
en kontroll av UUID-omskrivingen eller den publiserte versjonen.

Beslutningskilden er urørt med SHA-256
`abae5b92cd86e33130c45570046b1a993990e6faff0ad39c3051a0f7b3a7a2a6`.
Runtime-grunnlaget er urørt med SHA-256
`c62ca8f329d229101775158c61fdfce0b0874b0e00211820bea6fb10500c5e2f`.
Sammenligning mot oppstartssummer fant ingen endring i de 387 kontrollerte
Swift-filene (inkludert `Package.swift`). Historiske steg og 22.09-rapporten
har også samme innhold som ved oppstart. Ingenting er staged eller publisert.
