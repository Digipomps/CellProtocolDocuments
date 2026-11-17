# Bokprosjektet – regenerering 2026-09-25

**Status: ikke ferdig.** Gruppeforutsetningen er bekreftet på GitHub, ny lokal
generator er skrevet, og gammel automatisk relasjons-/presence-import er tatt
ut av arbeidskopien. Resultatdata er **ikke skrevet**: målskjemaet mangler en
fastlagt råverdiform for e-post og telefon i endpoints. Avklaring er sendt til
eieren; ingen fallback er godkjent eller brukt på deltakerdata.

## Kontroll av forutsetningen

GitHub API viste `Digipomps/CellProtocol/main` på
`63975cd4aeb79595f24cdf1d7f75b9713b9eeb13`. Sammenligningen mot
`a785dc71aadc2ea4e0468faae4dbfe9388952275` ga `ahead`, to commits foran,
null bak, og samme merge-base som `a785dc7`. Dette er en fersk kontroll mot
GitHub, ikke tillit til oppgaveteksten eller den lokale arbeidskopien.

Det eksakte skjemaet ble hentet fra denne main-committen:

[EntityData.v2.schema.json på kontrollert main](https://github.com/Digipomps/CellProtocol/blob/63975cd4aeb79595f24cdf1d7f75b9713b9eeb13/Docs/EntityData-Review-2026-09-11/EntityData.v2.schema.json).

| Forutsetning | Resultat |
| --- | --- |
| `groups.<uuid>.partOf` | Finnes som UUID-peker til foreldregruppe. |
| `relations.bokprosjekt` | Fjernet fra tillatte properties; `relations.additionalProperties` er `false`. |
| Skjemaets SHA-256 | `fd72be5b91471a7fec4f5e55bffb78bf40ea738f19ec3f1f864621cd6a9e943a` |

Nedlastet valideringsgrunnlag:
`/private/tmp/bokprosjekt-origin-main-20260925.schema.json`.
Den lokale `origin/main`-pekeren og CellProtocol-arbeidskopien ble ikke endret.

## Det nye kontraktgapet

`$defs.ContactEndpoint` beskriver bare `endpointId`, `purposes`,
`cellReference` og `label`. Beskrivelsen sier uttrykkelig at råverdier,
ruting, status og bevis ennå ikke har fastlagte skjemaer. `cellReference`
beskrives som en foreslått cellereferanse. Å putte rå e-post/telefon der eller
finne på `value`/`kind` ville være en egen kontrakt, selv om åpne objekter
teknisk kunne passert JSON Schema.

Generatoren stopper derfor som standard med:
`STOP: raw email/phone endpoint contract is unresolved`.

Eieren er bedt om å velge mellom å bevare råkontakt i eksisterende
`person.attributes` og rapportere endpoint-delen som uferdig, eller å vente
på en avklart endpoint-kontrakt. Den eksplisitte generatorinnstillingen
`--contact-mode preserve-attributes` er bare testet med oppdiktede data.
Den er ikke kjørt mot deltakerdata. Stillhet er ikke behandlet som godkjenning.

## Kilde og antall

Kilde: `Binding/.sprout/import/HAVEN_import_bokprosjekt.xlsx`,
arket `Deltakerliste`. 189 rader har navn; åtte av disse mangler `Gruppe`.
Det finnes elleve ikke-tomme gruppeverdier. Ingen av de importerte
kildekolonnene inneholder formler. Kontaktkolonnene inneholder 188 ikke-tomme
e-postceller og 189 telefonceller; disse tallene sier ingenting om gyldighet
eller tilgjengelighet.

| Type | Beregnet fra kilden / klargjort generator | Skrevet som resultatdata |
| --- | ---: | ---: |
| Entiteter | 189 | 0 |
| Rotgrupper, nivå 1 | 1 | 0 |
| Kapittelgrupper, nivå 2 | 9 | 0 |
| Arbeidsgrupper, nivå 3 | 4 | 0 |
| Grupper totalt | 14 | 0 |
| Direkte medlemskap | 189 | 0 |
| Relasjonsposter | 0 | 0 |

Planlagt fordeling av direkte medlemskap, kontrollert mot kilden:

| Gruppe | Nivå | Direkte medlemmer |
| --- | ---: | ---: |
| Bokprosjektet | 1 | 8 |
| KI og tillit | 2 | 20 |
| KI | 2 | 18 |
| Krise og beredskap | 2 | 0 |
| Krise og beredskap (gruppe 1) | 3 | 16 |
| Krise og beredskap (gruppe 2) | 3 | 15 |
| Kultur | 2 | 15 |
| Innovasjonspolitikk og virkemidler | 2 | 18 |
| Innovasjon og alder (65+) | 2 | 18 |
| Bærekraft | 2 | 13 |
| Trender og kreativ destruksjon | 2 | 16 |
| Medici-effekten | 2 | 0 |
| Medici-effekten (gruppe 1) | 3 | 16 |
| Medici-effekten (gruppe 2) | 3 | 16 |
| Sum | | 189 |

Generatoren lager tilfeldig UUIDv4 for hver entitet og gruppe, aldri
navne-/adresseavledede nøkler. Bare mest spesifikke gruppe får direkte
medlemskap. Roten har ikke `partOf`; undergrupper peker oppover. Ingen
bakreferanser, fiktiv «Ikke tildelt gruppe», `relations.records` eller
`scaffoldPresence` inngår i den nye formen.

Navn beholdes samlet i `person.displayName`, firma i
`person.work.organizationName`, stilling i `person.work.role`, og
interessecellen som én ufortolket verdi i `person.profile.interestTags`.
Oppgave og det tvetydige bosted/jobb-feltet bevares med kildehenvisning i
`person.attributes`. Det utledes ikke by, arbeidsgiverkobling, identitet,
samtykke, kontakttillatelse eller relasjon fra disse feltene.

## Filer, lagring og sletting

Ny generator og tester i CellScaffolds vanlige kildekodetre:

- `scripts/bokprosjekt-regenerate.py`
- `scripts/bokprosjekt-requirements.txt`
- `scripts/tests/test_bokprosjekt_regenerate.py`

Den gamle builderen i
`Sources/App/Support/BookProjectEntityPresenceSupport.swift` er erstattet
med verdifri utfasingsstatus. `QuestionnaireCampaignCell` oppretter ikke
lenger den gamle batchen eller registrerer gamle mounts ved import.
`EntityPresenceRegistryCell` avviser den gamle importen og leser/skriver
ikke de gamle `registryState`/`relationRootsByPrefix`-snapshotfeltene.
Kompatibilitetsendepunktet gir bare utfasingsstatus.

`QuestionnaireCampaignSupport.recipientGroups` og den tilhørende
`groupMemberships` ble lest før implementeringen. De laget flate grupper
og en syntetisk gruppe for tom kildeverdi. Den nye generatoren bruker ikke
denne utledningen; spørreskjemaverktøyets egne mottakerlister er ikke
omdefinert til EntityData-grupper.

**Ingen gamle persondata eller kildefiler ble slettet.** Under
`Binding/.sprout/import/` fant denne kjøringen bare kilderegnearket og
ingen gammel generert resultatfil. `CellScaffold/.sprout/` inneholdt bare
auditlogg. Logger er ikke slettet. Eksisterende EntityAnchor-data,
spørreskjemakampanjer, historikk, sikkerhetskopier og stagingdata er ikke
ryddet eller migrert. Kodeendringen er ikke deployet.

Reservert, men fortsatt ikke opprettet, resultatsti:

`/Users/kjetil/Build/Digipomps/HAVEN/Binding/.sprout/import/bokprosjekt-2026-09-25/EntityData.json`

`git check-ignore -v` bekreftet både kilden og denne stien med
`Binding/.gitignore:1:.sprout/`. Generatoren kontrollerer dette på nytt
før skriving, avviser symlinker og eksisterende resultatmapper, og bruker
mappe-/filrettigheter `0700`/`0600` med atomisk flytting og lesing tilbake.
Et ferdig lokalt JSON-resultat ville fortsatt ikke være bevis på
resolverautorisert Entity-lagring, runtime-migrering eller replikering.

## Kontroller

| Kontroll | Resultat |
| --- | --- |
| Kildens navngitte rader | 189, kontrollert direkte fra regnearket. |
| Kildens medlemsfordeling | 189 totalt, åtte direkte i roten; ingen gruppe gjettes. |
| Virkelig kilde, uten kontaktkolonnene, bare i minnet | 189 entiteter, 1/9/4 grupper og 189 unike medlemskap validerte mot main-skjemaet. Alle andre kildekolonner og riktig gruppe per rad ble avstemt. Kandidaten ble ikke lagret. |
| Generator-/skjematester | 11 tester bestått med oppdiktede deltakere mot det nedlastede main-skjemaet. |
| UUIDv4, duplikatnavn, nye kjøringer | Bestått i tester. |
| Foreldrereferanser, entitet som forelder, egen-/flergruppesyklus | Gyldig form godtas; ugyldige tilfeller avvises i tester. |
| Manglende/doble medlemskap, gruppe som medlem | Avvises i tester. |
| Medlemskap i mest spesifikke kildegruppe | Egen radavstemming; feil plassering avvises i tester. |
| JSON Schema | Testdata validerer; hver nestet person valideres også særskilt fordi entitetspostene er åpne i målskjemaet. |
| Ingen `relations.records` | Generatoren skriver bare `relations.entities`; selv en tom `records` avvises av importkontrollen. |
| Gitignore, tilgangsmodus, lesing tilbake, overskrivingsvern | Bestått med oppdiktet testresultat i midlertidig Git-repo. |
| Virkelig importforsøk | Exit 1 ved kontaktgapet, før skriving. Fravær av resultatmappen kontrollert etterpå. |
| Swift-syntaks | `swiftc -frontend -parse` bestått for de fire endrede Swift-filene. |
| Fullt Swift-bygg | `swift build --disable-sandbox --skip-update --disable-automatic-resolution`: bestått, exit 0, ca. 263 sekunder. Ingen exit 64. |
| Swift-integrasjonstest | `QuestionnaireCampaignCellTests/testBookProjectImportDoesNotPublishLegacyRelationsOrPresence`: 1 test bestått, 0 feil, exit 0. Kontrollerer uendret EntityAnchor, avvist registrering, tomme mounts og at gamle snapshotfelt ikke kodes på nytt. |
| `git diff --check` | Bestått. |
| Persondatakontroll av rapport og ny generator/testkode | Ingen treff på kildens navn, e-post- eller telefonverdier på minst fem tegn. |

Testkommando fra `CellScaffold`:

```sh
PYTHONDONTWRITEBYTECODE=1 \
BOKPROSJEKT_SCHEMA=/private/tmp/bokprosjekt-origin-main-20260925.schema.json \
/private/tmp/bokprosjekt-validation-20260925/bin/python -m unittest discover \
  -s scripts/tests -p test_bokprosjekt_regenerate.py -v
```

Swift-integrasjonstesten ble kjørt med
`swift test --disable-sandbox --skip-update --disable-automatic-resolution --filter QuestionnaireCampaignCellTests/testBookProjectImportDoesNotPublishLegacyRelationsOrPresence`.
Lokal testlogg: `/private/tmp/bokprosjekt-swift-test-20260925.log`.
Bygg/test ga eksisterende kompilator- og cacheadvarsler, men fullførte med
exit 0. Hele Swift-testsuiten er ikke kjørt.

## Persondata og eksterne kall

Ingen deltakerverdier er skrevet i rapport, kode, fixtures, testlogger eller
nye resultatfiler. Kildedata ble bare behandlet lokalt i minnet. Eksisterende
kilderegneark beholdes på den opprinnelige gitignorerte stien.

Eksterne lesekall: GitHub API for main-SHA, commit-sammenligning og skjema
ved SHA, med eksisterende GitHub CLI-autentisering. Ingen deltakerdata
ble sendt. Valideringsverktøyet `jsonschema==4.25.1` med avhengigheter ble
hentet fra PyPI til `/private/tmp/bokprosjekt-validation-20260925`, uten
nedlastingscache. `openpyxl==3.1.5` fantes allerede lokalt. SwiftPM hentet
pakkekode fra lokal cache under bygget. Midlertidig skjema og Python-miljø
inneholder ingen deltakerdata og er beholdt for gjenopptakelse.

## Gjenstår og Git-status

- Avklare råkontaktformen før resultatdata kan skrives. Et attributtbasert
  delresultat krever svar på det sendte valget; det oppfyller ikke kravet om
  ferdige endpoints.
- Generere og validere hele det virkelige resultatet, med 189 entiteter og
  14 grupper, og kontrollere filen etter lagring.
- Eventuell opprydding av gamle data i konkrete kjørende EntityAnchor- og
  registrylagre er ikke utført. Ingen slike lagre er valgt eller endret av
  denne kjøringen.
- Eventuell runtime-innlasting og deploy. Fullbygget og den avgrensede
  integrasjonstesten er bestått lokalt, ikke kjørt i CI.

Ingen staging, commit eller push er utført, verken av kode eller data.
Generator og tester ligger som nye, ikke-gitignorerte kildefiler, men er
ennå ikke lagt til i Git-indeksen. De fire endrede Swift-filene var rene
ved oppstart. Omfattende andre eksisterende endringer i arbeidskopiene
er ikke tatt med. Ingen commit planlegges i denne kjøringen.
