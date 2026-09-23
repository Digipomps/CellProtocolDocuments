# EntityData: UUID og grupper, 22.09.2026

**Historisk rapport.** Målingene nedenfor gjelder 22.09-mellomsteget.
Ved publiseringen 23.09 ble `relations.records` sitt UUID-unntak opphevet,
og eksempelets nøkler og referanser omskrevet. Validatoren er videreført som
regresjonskontroll mot 23.09-målet; den lenkede resultatfilen er kjørt på nytt
og angir `targetDecisionsAsOf`. Opprinnelige målinger nedenfor er ikke en
påstand om dagens skjemabyte eller dagens antall kontroller.

Arbeidet ligger i arbeidstreet. Ingen commit, push, merge, Swift-endring eller
migrering av ekte brukerdata er utført. Fasit er
[beslutningen 22.09](../../CellProtocol/Docs/EntityData-Review-2026-09-11/BESLUTNING-UUID-OG-GRUPPER-2026-09-22.md).

## Mål

1. Innarbeide de utførbare 22.09-beslutningene i det ene gjeldende målskjemaet,
   med de samme tre filnavnene, etter 16.09-transformasjonen.
2. Uttrykke grupper som uvektede medlemslister over entiteter, og fjerne
   eierdefinerte lister under `relations`.
3. Uttrykke UUID-nøkling i de fire angitte kartene, med det uttrykkelig tillatte
   beskrivelsesunntaket der eksisterende eksempler ellers brytes.
4. Persistere bare entitet → identitet og relasjon → entitet for de to angitte kantene.
5. Erstatte bokprosjektets separate gruppeform dersom synlige data gir tilstrekkelig
   grunnlag; ellers bevare den og identifisere manglende grunnlag.
6. Bevare runtime-grunnlaget og `proofs.index.byKeypath` uten endring.
7. Levere reproduserbar bygging, positive og negative strukturkontroller,
   SHA-256 før/etter og et tydelig skille mot uprøvd runtime og visualisering.

## Påstander og observerte resultater

| Grep | Traff? | Hva som faktisk er skrevet eller bevart |
|---|---|---|
| Egen `groups`-rot | Ja | Objekt nøklet på gruppe-UUID. Hver gruppe krever `name` og `members` og tillater ingen andre felt. Medlemmene er UUID-strenger til `relations.entities`. Beskrivelsene skiller uvektede grupper fra relasjonenes vektede perspektivgraf. Røttene er fortsatt valgfrie i en delvis EntityData. |
| Eierdefinerte relasjonslister ut | Ja | `relations.additionalProperties` endres fra listeschema til `false`. Alle ti eksisterende reserverte nøkler er bevart. |
| `relations.records` nøklet på UUID | Beskrivelse, ikke håndheving | Eksisterende kompakte eksempel bruker `relation-demo`; visualiseringsvalidatoren bruker `rellea`. `propertyNames.pattern` ville avvist dem. UUID-kravet og dette unntaket står eksplisitt i `description` og metadata. Ingen nøkler eller bevisstier er omskrevet. |
| `relations.entities` nøklet på UUID | Ja | `propertyNames.pattern` for UUID. Det gamle kompakte eksempelet hadde ikke dette kartet; det nye har to UUID-nøklede entitetsposter. |
| `relations.identities` nøklet på UUID | Ja | Samme UUID-mønster. Eksempelet har én UUID-nøklet identitetspost. |
| `groups` nøklet på UUID | Ja | Samme UUID-mønster; eksempelet har to UUID-nøklede grupper. |
| Fjern `relations.identities.*.entityRefs` | Ja | Feltdefinisjonen er fjernet, og et eksplisitt `not`-krav avviser feltet også i et ellers åpent objekt. `relations.entities.*.identityRefs` beholdes og beskriver at bakveien bygges ved dekoding, i minnet. |
| Fjern `relations.entities.*.relationRefs` | Ja | Samme eksplisitte avvisning. `relations.records.*.subject.entityRef` beholdes og beskriver dekoding av bakveien i minnet. Den overordnede Subject-beskrivelsen skiller den lagrede kanten fra mulige avledede sammendrag. |
| Bokprosjektgrupper inn i ny rot | Nei, utsatt etter oppgavens unntak | Hele `relations.bokprosjekt` er identisk med før, inkludert `members[].relation.groupRefs` og `group`. Manglende grunnlag er konkretisert nedenfor. |
| Eksempel | Ja | Venner har to entitetsreferanser; Samarbeidspartnere har én av de samme. Én relasjon peker på den felles entiteten, og entiteten peker på en identitet. Alle nye referanser løses mot eksempelets faktiske kart. |
| `proofs.index.byKeypath` | Urørt | Både struktur og beskrivelse er bevart; hele `proofs`-skjemaet og eksempelets `proofs` er identiske med 16.09-resultatet. |
| Samme mål og reproduksjon | Ja | De tre målfilnavnene og deres eksisterende schema-ID-er er beholdt. 16.09 → 22.09 kjøres i minnet før målfilene og manifestet skrives. Ingen datert konkurrerende målskjemafil er opprettet. |

UUID-mønsteret er
`^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$`.
Mønsteret kontrollerer representasjonsform, ikke global unikhet, referanseoppløsning
eller identitetslikhet. En UUID som bare finnes som relasjonsnøkkel kan derfor
passere strengskjemaet, men avvises av den separate referansekontrollen for
fixturet. Dette skillet er testet eksplisitt.

## Hvorfor bokprosjektet står urørt

Det kompakte repoeksempelet inneholder ingen `relations.bokprosjekt`-data.
Schemafeltet `groupRefs` har bare `type: array` og tekst om Excel-kolonnen Gruppe,
uten kontrakt for elementer eller kobling til en entitets-UUID.

Følgende kildekode ble lest, uten endringer:

- [EntityAnchorDataV1Contract.swift](../../CellScaffold/Sources/App/Support/EntityAnchorDataV1Contract.swift):501
  beskriver gruppereferansene som avledet fra Excel-kolonnen.
- [BookProjectEntityPresenceSupport.swift](../../CellScaffold/Sources/App/Support/BookProjectEntityPresenceSupport.swift):61–94
  skriver `recipientID`, `group` og `groupRefs` fra `recipient.groupMemberships[].id`.
  Samme fil har et eget `relations.bokprosjekt.groups`-uttrekk.
- [QuestionnaireCampaignCell.swift](../../CellScaffold/Sources/App/Cells/QuestionnaireCampaign/QuestionnaireCampaignCell.swift):1775–1797
  grupperer på medlemskapets eksisterende ID og skriver `label` og `memberRecipientIDs`.

For en tapsfri omlegging mangler konkret:

1. Autoritativ kobling fra hver eksisterende `recipientID`/medlemspost til
   entitets-UUID i `relations.entities`.
2. Autoritativ kobling fra hver eksisterende gruppe-ID og label til én stabil
   gruppe-UUID og gruppens navn i `groups`.
3. De faktiske gruppene og medlemskapene, eller et representativt fixture med
   disse koblingene, slik at refs og sammenslåing med eventuelle eksisterende
   grupper kan kontrolleres uten å gjette.

De nye fiktive UUID-ene i det generelle eksempelet er ikke slike koblinger for
bokprosjektet. Å bare omdøpe `groupRefs` eller la dem peke til nye grupper ville
heller ikke i seg selv flytte medlemskapet til én lagret retning. Den gamle
sideformen er derfor et dokumentert, gjenstående migreringsunntak, ikke påstått avviklet.

## SHA-256 for de tre målfilene

Før-verdiene ble målt fra arbeidstreet før noen endring, ikke fra `HEAD`.
Review-mappen var allerede usporet ved oppstart.

| Fil | Før | Etter |
|---|---|---|
| `EntityData.v2.schema.json` | `a5fdf62f074e3cd1b3494009b69dee5ae28504eece0e838d35cc65607587ee15` | `b7211f3dd361c5f39c5bcfa499b09ca9b3bbf54e4e43fcd098fe88b6cbb0d9f4` |
| `EntityData.v2.example.json` | `b576632448a881236014271d81a0c992aee45b88bc9f3c242003e258b3993e60` | `cc4df57f7647869838685652415daab4122296069c6c5f70255550fada5b643b` |
| `EntityRepresentation.v2.schema.json` | `0f398b1f59c4e1f25f4d690ad10dbba3fc12ca3c080348bbd3c9fdf5f86d20e2` | `7720d80e07035d87e3518c61ea20f73ee62787a0aded6743fee41eafdf67a65d` |

`EntityData.review.schema.json`, SHA-256 før **og** etter:
`c62ca8f329d229101775158c61fdfce0b0874b0e00211820bea6fb10500c5e2f`.

Som ekstra kontroll er `proofs.index.byKeypath` sammenlignet som JSON-tre,
inkludert beskrivelse. Begge sider har kanonisk JSON-SHA-256
`eb1e0fbf152f78f19b1590eb6b372ed47227b4fdcbf9605c29b87dc4b08b85da`
(sorterte nøkler, UTF-8, kompakte separatorer). Dette er hash av undertreet,
ikke av en egen schemafil.

## Kontroller som er grønne

[Det maskinlesbare resultatet](../../CellProtocol/Docs/EntityData-Review-2026-09-11/TARGET-VALIDATION-2026-09-22.json)
oppgir **234 beståtte strukturkontroller**, med **Ajv 8.17.1 + ajv-formats 3.0.1**.
Kjøringen ble også gjort med `python3 -B -O`; kontrollene av manglende
transformasjonsmål bruker eksplisitte feil og blir ikke slått av av `-O`.

- Begge schemafilene er gyldige Draft 2020-12; alle lokale `$ref` løses.
- Kompakt eksempel og dets EntityRepresentation validerer mot sine målskjemaer.
- Grupperot finnes; minst to medlemmer i én gruppe og en entitet i to grupper.
- Gruppe uten navn, uten medlemsliste, med tomt navn, med gruppevekt,
  med vektet medlem, med innebygd entitet og med ikke-UUID-medlem avvises.
- Eierdefinert liste og objekt under `relations` avvises.
- Ugyldige nøkler avvises i de tre UUID-stramme kartene; gyldige nøkler godtas.
  Det eksplisitte `records`-unntaket og det gamle eksempel-ID-et godtas.
- Begge fjernede ref-felt avvises med tom liste, fylt liste og `null`.
- Nye medlems-, identitets- og subject-referanser i eksempelet har eksisterende mål.
  En relasjons-UUID og en ukjent entitets-UUID avvises som gruppemedlem av
  fixturets referansekontroll. Ugyldig date-time avvises av formatkontrollen.
- Tolv konkrete manglende transformasjonsmål gir høylytt feil. Dobbelt anvendt
  steg og eksempel uten den forventede relasjonsposten avvises også.
- Reproduserte byte er identiske for begge skjemaer, eksempel og manifest.
  En ny full bygging ga uendrede etter-SHA-er.
- Runtime-baseline, hele `proofs`, hele `bokprosjekt`, øvrige røtter og alle
  øvrige delte definisjoner er bevart fra 16.09-steget. Reserverte nøkler beholdes.
- Python-syntaks er kontrollert. Tracked Swift-/Package-diffene i de to
  berørte repoene er identiske med oppstart. Eksisterende Swift-arbeid er ikke endret.

Dette er strukturell evidens for målmodellen. Det er ikke bevis for at en decoder
bygger bakveier, at grafen er looptrygg i runtime, at identiteter er ekvivalente,
eller at autorisasjon, signaturer eller distribuert lagring virker.

## Kontroller som ikke er kjørt

| Kontroll | Status og konkret grunn |
|---|---|
| Den gamle visualiseringssuiten | **Ikke kjørt for 22.09.** Den avhenger av `/Users/kjetil/.codex/visualizations/2026/09/11/01a090eb-528a-76d3-87d1-41a0b84f4d47`, utenfor repoet. En lesende forhåndskontroll viste at mappen finnes, men snapshot oppgir beslutningsdato 16.09, oppdateringsdato 17.09 og 13 røtter. Snapshot og payload bruker SHA `3052706f897db5b5fb6a89f1eba8a444d759df3588525bd5e991e9fcdaae7bd4`, som ikke er etter-SHA for målskjemaet. Ingen ekstern visualisering er oppdatert. Full mock-/variant-/deknings-/grafkontroll er ikke bokført som bestått. |
| Python-motoren `jsonschema` og den uendrede 16.09-validatoren | **Ikke kjørt.** System-Python og et isolert Python 3.11-miljø manglet `jsonschema`. Installasjon fra `requirements-target.txt` feilet ved DNS/nettverkstilgang til PyPI. Lokale Python 3.13-binærer var av feil CPU-type. Struktursjekkene ble i stedet faktisk kjørt med den oppgitte lokale Ajv-motoren. Den historiske validatoren forutsetter dessuten at egne relasjonslister godtas og at hele målet er lik bare 16.09-steget. |
| Swift-bygg, Swift-tester og faktisk dekoding | **Ikke kjørt.** Oppgaven gjelder bare dokumentasjon og skjema; det finnes ingen Swift-endring å verifisere her. |
| Bokprosjektmigrering og ekte brukerdata | **Ikke kjørt.** Koblingsgrunnlaget over mangler, og ekte datamigrering er utenfor oppgaven. |
| UI/staging, signaturer, autorisasjon, identitetslikhet og replikering | **Ikke kjørt.** Ingen påstand om runtime-funksjon eller distribuerte garantier inngår i leveransen. |

For fornyede visualiseringsartefakter støtter den nye validatoren
`--visual-dir <mappe>`. Feil eller manglende data gir feil; de hoppes ikke over.
Det gamle `TARGET-VALIDATION-2026-09-17.json` er urørt og er historisk evidens.

## Bygging og berørte filer

Fra `CellProtocol/Docs/EntityData-Review-2026-09-11`:

```sh
export ENTITYDATA_AJV_MODULE=/usr/local/lib/node_modules/@nestjs/cli/node_modules/ajv
export ENTITYDATA_AJV_FORMATS_MODULE=/usr/local/lib/node_modules/@nestjs/cli/node_modules/ajv-formats
python3 -B -O apply_decisions_2026_09_22.py
python3 -B -O validate_decisions_2026_09_22.py
```

Med Python-avhengighetene installert kan miljøvariablene utelates; da brukes
`jsonschema` og `FormatChecker`. Dette alternativet er tilgjengelig i skriptene,
men ble ikke kjørt i denne økten.

Ny [apply_decisions_2026_09_22.py](../../CellProtocol/Docs/EntityData-Review-2026-09-11/apply_decisions_2026_09_22.py)
kaller 16.09-transformasjonene og transformerer resultatet videre. Alle grep
krever eksisterende mål; nye felt krever at de ikke allerede finnes. Kontroller
og validering skjer før filskriving. 16.09-skriptets transformasjonslogikk er
uendret: bare `jsonschema`-importen er flyttet inn i `main()`, slik at rene
transformasjonsfunksjoner kan importeres med en annen tilgjengelig validator.

Ny [validate_decisions_2026_09_22.py](../../CellProtocol/Docs/EntityData-Review-2026-09-11/validate_decisions_2026_09_22.py)
og [target_validation.py](../../CellProtocol/Docs/EntityData-Review-2026-09-11/target_validation.py)
gir kontrollene og det eksplisitte motorvalget. Ingen validatorlastinger laster
ned pakker eller skifter motor i det stille.

`current-review.json` er generert på nytt. `V2-BESLUTTET-FORM.md` er oppdatert
til én gjeldende forklaring, `LES-MEG.md` peker dit, og 16.09-notatet er merket
som historisk mellomsteg. Det tidligere V2-notatet beskrev et annet historisk
byggeskript; det er ikke videreført som en konkurrerende fasit.

Urørt: beslutningsdokumentet 22.09, runtime-schema og runtime-eksempel,
16.09-beslutningsregisteret, historiske kontrollresultater, Swift-kode,
`proofs.index.byKeypath`, bokprosjektets undertre og øvrig eksisterende WIP.
Ingen arbeidstreet-filer er staged eller committed.

Arbeidsgrener ved oppstart: CellProtocol `pdd/tillitspakke-agentflaate`,
CellProtocolDocuments `codex/docs-cleanup-20260810`. Begge repoene var allerede
urene; denne oppgaven endrer bare de navngitte dokumentasjons-/schemaartefaktene.
