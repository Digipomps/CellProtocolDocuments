# Teststrategi for formålsmatching

Utført 11.–12. september 2026. Leveransen er en måleharness, et fasitskjema og
menneskeregistrering. **Vi har fortsatt ikke grunnlag for å kåre en matcher eller
hevde at matching forebygger feil.** Den sterkeste retrospektive fasiten gir
15 positive oppgave–lærdom-par fordelt på bare fire oppgaver. Ingen av disse
lærdommene er datert før oppgaven de oppsto i.

## Formål, mål og avgrensning

Forankring: `purpose://quality.build-and-regression` fra formålspakkene:
målingen skal gi etterprøvbare svar. Oppgavens brukerbestilling er mandatet for
denne avgrensede leveransen. Ingen G1/G2/G3-godkjenning i den overordnede
grafoppgaven er registrert av dette arbeidet.

| Mål denne runden | Baseline | Observerbar leveranse | Status |
|---|---|---|---|
| Relevans kan registreres uten fritekst per lærdom | Ingen fasit | Schema + `purpose_dev.py judge`; boolsk relevans, repeatOf og håndhevelse | Levert; menneskelig tidsmål ikke utprøvd |
| Retrospektiv evidens skilles etter styrke | Kilder og §4 finnes | Frosset korpus og sporbare positive par, uten oppdiktede negative | Levert |
| Kandidater sammenlignes med samme betingelser | Spredning uten fasit | Funksjonsgrensesnitt, tabeller, manglende dommer, parvis statistikk | Levert og testet |
| Utvalgsusikkerheten blir synlig | 19 oppgaver / 44 lærdommer | Bootstrap, eksakt permutasjon og eksplisitte utvalgsantakelser | Levert |

Ingen ny matcher, nye avhengigheter, byggkø eller Docker er brukt. Ingen commit,
push eller endring av branch er gjort. Eksisterende endringer i Book, kataloger,
andre leveranser og verktøy er bevart. Det overordnede grafregisteret er utenfor
denne leveransen.

## 1. Hva er et treff?

En lærdom er relevant ved G1 hvis forebyggingen, gitt oppgavens §0 og avgrensning,
ville endret **et konkret valg, en test eller en avgrensning**. Et felles ord eller
at rådet er fornuftig generelt er ikke tilstrekkelig. Personen som gjør G1-lesingen
avgjør. `false` betyr vurdert irrelevant; manglende rad betyr uvurdert.

Det fulle [JSON-skjemaet](../../../Tools/PurposePackages/matching_judgment.schema.json)
er Draft 2020-12. Hver dom har én av tre disjunkte former. Illustrasjonen bruker
fiktive referanser, ikke faktiske vurderinger:

```json
[
  {"lessonRef": "lesson.example-a", "relevant": false, "repeatOf": null},
  {"lessonRef": "lesson.example-b", "relevant": true,
   "repeatOf": "lesson.example-a", "preventedBy": "test.example"},
  {"lessonRef": "lesson.example-c", "relevant": true, "repeatOf": null,
   "unenforced": {"reason": "mangler-test"}}
]
```

- `repeatOf` peker på samme feilmekanisme og relevant forebygging i en tidligere
  lærdom. Tag-overlapp alene er ingen gjentakelse. `null` er menneskets eksplisitte
  «ingen identifisert gjentakelse». Validatoren avviser ukjente refs og samme eller
  senere dato. Registeret har bare dagoppløsning; sikre gjentakelser innen samme
  dag trenger bedre tidsdata før de kan registreres som ordnet her.
- For `relevant: true` kreves enten `preventedBy` eller `unenforced.reason`.
  Testref må finnes blant snapshotets `derivedTests` eller oppgavens §5.
  Pakketilknytning blir aldri automatisk en testkobling.
- Ved G1 betyr `preventedBy` **utpekt vern som skal håndheve forebyggingen**.
  Det betyr ikke at testen er kjørt, at en feil faktisk ble hindret eller at
  utfallet er kausalt bevist. Slike påstander krever senere kjøringsbevis.

Omslaget lagrer oppgave, G1-stadium, tidspunkt, full lærdomstekst, kandidatlistenes
rekkefølge, presentert union, testrefs, dommer og registreringstid. `snapshotHash`
sporer hele datagrunnlaget; `corpusHash` fryser lærdommer og pakker; `taskHash`
fryser denne oppgavens query, dato, tags og surfaces. Å legge til andre oppgaver
ugyldiggjør ikke gamle dommer. Endrede lærdommer, pakker eller oppgaveinput gjør det.

### Billig menneskeflyt

Etter den vanlige G1-lesingen: én kompakt, nummerert liste, tre svar:

1. `1 3 ?4`: 1 og 3 relevante; 4 uvurdert; resten eksplisitt irrelevant.
   `-` betyr ingen relevante. `v 4` viser hele symptom/forebygging før svaret.
2. `3=lesson.tidligere`: registrer eventuell gjentakelse; `-` betyr ingen.
3. `1=test.known 3=u:mangler-test`, eller `u:mangler-test` for alle treff.
   `?` viser testrefs. Grunn kan også være eksempelvis `manuell-kontroll` eller
   `ikke-automatiserbart`; bruk en sann grunn, ikke en forhåndsvalgt standard.

Normalrunden har to svar hvis ingen lærdom er relevant. Ingen standardverdi gjetter
menneskets relevans eller håndhevelse. Ukjente rader kan tas senere. Filen lagres
atomisk etter en komplett svarrunde. `q`, EOF eller Ctrl-C bevarer tidligere
lagrede runder. `--batch-size 10` gir delrunder hvis hele listen er for stor.
Gjentatt kjøring fortsetter med uvurderte rader og avviser en annen kjøring over
den eksisterende filen.

**Under ett minutt er et mål for ekstra registrering etter G1-lesingen.** Antall
normale svar er konstant også ved 35 lærdommer. Det er ikke en påstand om at et
menneske kan lese 70 avsnitt og avgjøre relevans på ett minutt. Syntetiske CLI-tester
viser at flyten lagrer gyldig JSON; de måler ikke menneskelig brukbarhet.
`annotationSeconds` inkluderer tiden fra den kompakte listen vises til svarene er
ferdige, også eventuell utvidet lesing med `v`. Første fem reelle oppgaver skal
måle total registreringstid per oppgave; mål median <60 sekunder, og rapporter
også maksimal tid og andel uvurderte. Ikke reduser tiden ved å tvinge ukjente til nei.
Menneskelig tidsmål er foreløpig **åpent**, med oppgaveeier som evaluator.

### Kjøring

Fra `CellProtocolDocuments/`:

```sh
MEAS=Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling
python3 "$MEAS/evaluer.py" snapshot --out /tmp/g1-korpus.json
python3 "$MEAS/evaluer.py" pool --snapshot /tmp/g1-korpus.json --task PDD_formaalsregister-som-graf_2026-09-11 --matcher tag --matcher tfidf --k 10 --out /tmp/g1-run.json
python3 Tools/PurposePackages/purpose_dev.py judge Deliverables/PDD_formaalsregister-som-graf_2026-09-11 --run /tmp/g1-run.json
python3 Tools/PurposePackages/purpose_dev.py judge Deliverables/PDD_formaalsregister-som-graf_2026-09-11
```

Dette er en oppskrift, ikke utførte menneskevurderinger. Eksempelet bruker den
kjente oppgavemappen; bruk ny oppgave ved fremtidig G1. Verktøyet godkjenner ingen
port. For ett faktisk oppslag brukes bare matcheren som leverte listen, og `--k`
settes til antall lærdommer som faktisk ble vist. En sammenligningspool er unionen
av alle kandidatens topp-k, deduplisert og deterministisk blandet. Mennesket ser
ikke kandidatnavn eller kandidatens rangering under merkingen. Poolen kan inneholde
opptil `antall kandidater × k` lærdommer; antallet skjules ikke. Kjør `--k 44` hvis
hele dette korpuset skal vurderes for ekte dekning, og budsjetter mer lesetid.

Tilføy nye oppgaver med samme frosne kandidatverden:

```sh
python3 "$MEAS/evaluer.py" snapshot --corpus-from /tmp/g1-korpus.json --out /tmp/g1-utvidet.json
```

Dette gjenbruker lærdommer/pakker fra det gamle snapshotet og leser oppgaver på
nytt. Oppdaterte §0/tags/surfaces krever ny vurdering av den berørte oppgaven.

## 2. Retrospektiv fasit og brief-audit

[MAALT_UTGANGSPUNKT.md](../maaling/MAALT_UTGANGSPUNKT.md) ble lest først.
Originalskriptene ble også kjørt før endringer. De fant 19 oppgaver og 44 lærdommer:
tag-listen hadde snitt 35,0, Jaccard 0,81 og 23 felles lærdommer; den eksisterende
TF-IDF-spikens topp-10 hadde Jaccard 0,20 og null felles. Dette er forenlig med
utgangspunktets avrundede spredningstall, men den opprinnelige 18-oppgavelisten er
ikke lagret der. Vi påstår derfor ikke å ha rekonstruert akkurat de samme 18.

**Samtidig endring:** mellom innledende lesing og snapshot kom
`lesson.unavailable-was-a-repo-scoped-search` inn som lærdom nr. 45.
[korpus.json](../maaling/korpus.json) bevarer dette observerte 19/45-snapshotet.
[korpus_44.json](../maaling/korpus_44.json) utelukker uttrykkelig bare denne nye
refen og peker på foreldresnapshotets hash. Primærtallene nedenfor gjelder 19/44.
Dette er en avgrenset kohort av det frosne innholdet, ikke en påstand om at alle
filbytes er de samme som da det tidligere notatet ble skrevet.

Alle 19 oppgaver har nå spec og status. De 18 andre oppgavene kan avgrenses med
`subset --exclude-task PDD_formaalsregister-som-graf_2026-09-11`; ingen av de 15
source-positive parene forsvinner da. Slike avgrensninger må oppgis før sammenligning.

Fasitutledningen er i [retrospektiv_fasit.json](../maaling/retrospektiv_fasit.json).
`judgments` inneholder bare de 15 `relevant: true` med `basis: source`.
`rows` bevarer øvrig evidens. Ingen kilde gir automatiske negative dommer.

| Evidens i 44-kohorten | Par | Hva det støtter |
|---|---:|---|
| `source` inneholder hele oppgavemappens navn | 15 i 4 oppgaver | Sikker tilknytning/relevans til oppgaven retrospektivt |
| Eksplisitt ref i §4 uten gjenkjent auto-seksjon | 26 i 3 oppgaver | Svakt, sannsynlig redaksjonelt utvalg; ikke en menneskelig fasit |
| Eksplisitt ref i en gjenkjent auto-seksjon | 269 | Eksponering, ikke relevans |
| Minst 50 % felles normaliserte femordssekvenser | 259 | Tekstlig gjenbruk; **alle 259** finnes i auto-seksjoner |
| §4-ref som ikke finnes i 44-registeret | 2 forekomster | Datagap; beholdes som varsel, ingen oppfunnet alias |

Overlapptallet er andelen av lærdommens unike femordssekvenser fra symptom og
forebygging som finnes i §4. Terskelen 0,50 er en synlig diagnoseheuristikk, ikke
en validert relevansterskel eller en del av matcheren. Den håndterer ordrett
gjenbruk, men overser parafraser og kan treffe generisk tekst. Auto-deteksjonen
bruker de eksisterende lookup-overskriftene; fravær av overskriften beviser ikke
at en seksjon er menneskeskrevet. Derfor forblir `curated_ref` svak evidens.

De sikre positive parene fordeler seg slik:

| Oppgave | Source-positive lærdommer |
|---|---:|
| agent-menylinje-og-varsler | 7 |
| scaffold-admin-delegering | 4 |
| palazzo-husk-det-jeg-sa | 3 |
| utviklerbenk-oppgavegraf | 1 |

Alle 15 er datert samme dag som eller senere enn oppgaven. `--before-task-date`
utelukker dem alle. Dato er dessuten hendelses-/lærdomsdato, ikke bevist
registreringstid; dagens query/pakker kan være revidert. Datofilteret er bare en
konservativ følsomhetskontroll, **ikke historisk G1-replay**.

Den ukjente refen er `lesson.main-does-not-build-without-unlanded-changes`, sitert
i visionOS- og utviklerbenkoppgaven. Den kobles ikke automatisk til andre
main/baseline-lærdommer. Heller ikke gjentakelser eller faktisk håndhevelse kan
utledes sikkert av eksisterende tags, pakketilknytning eller manglende feilrapport.

**Bruksgrense:** source-fasiten kan grovsortere retrospektiv gjenfinning av kjente
problemer. Den overrepresenterer oppgaver som faktisk produserte registrerte feil,
mangler negative dommer og overser relevante råd som aldri ble en registrert
hendelse. Den kan ikke estimere reell presisjon, all relevant dekning eller nytte.
Mer resampling reparerer ingen av disse skjevhetene.

## 3. Metrikker og sammenligningskontrakt

For oppgave `q`: `Lq` er kandidatens ordnede liste, `Rq` alle relevante lærdommer
i det frosne universet, `Hq(k) = |Lq[:k] ∩ Rq|`.

- **Presisjon@k:** `Hq(k)/k`. En kort liste får tomme, ikke-relevante plasser opp
  til k; den får ikke kunstig perfekt presisjon ved å returnere ett eneste treff.
- **Dekning@k:** `Hq(k)/|Rq|`. Oppgaver med `Rq = ∅` har udefinert dekning og
  utelates med synlig antall; de får ikke automatisk 0 eller 1.
- **MRR:** gjennomsnitt av `1/rang_første_treff`, eller 0 hvis listen ikke har
  treff. Hele returnerte rangeringen brukes. `MRR@k` setter dette til 0 når første
  treff er etter k, og bør brukes ved vurdering av et fast lesebudsjett.
- **Lesebelastning:** antall avsnitt i symptom + forebygging for topp-k, med
  blanklinjer som deling innen hvert felt. Hvert av de 44 objektene gir to
  avsnitt i denne visningskontrakten. Urelevante avsnitt er støy. Ordantall og
  faktisk lesetid kan supplere senere; avsnittene er ikke antatte minutter.

Hvert mål aggregeres som **makrosnitt over oppgaver**, ikke over 19×44 uavhengige
par. Rangering og målinger per oppgave finnes i resultat-JSON. Dette følger vanlig
rangert gjenfinningsmåling; konvensjonene for kort liste og tom relevantmengde er
spesifisert over. [Stanford, *Evaluation of ranked retrieval results*](https://nlp.stanford.edu/IR-book/html/htmledition/evaluation-of-ranked-retrieval-results-1.html).

Med ufullstendig fasit oppgis følgende i stedet for oppdiktet eksakthet:

- P@k har nedre grense `kjente treff/k` og øvre grense
  `(kjente treff + uvurderte returnerte)/k`.
- MRR har nedre grense fra første kjente positive og øvre grense fra første
  positive **eller uvurderte**. En kandidatfeil hopper ikke over en vanskelig
  oppgave; ukjente/dupliserte refs gir eksplisitt feil.
- `R+@k` har bare **kjente** positiver i nevneren. Den er ikke ekte dekning og
  heller ikke generelt en nedre/øvre grense for ekte dekning. `MRR+` rapporteres
  på samme oppgaveutvalg som R+, mens MRR-grensene omfatter alle evaluerte oppgaver.
- Støyens nedre grense teller eksplisitt irrelevante avsnitt; øvre grense teller
  også uvurderte avsnitt. Lesebelastningen kan måles uten fasit.
- `n / n+ / fullt` viser totalt antall oppgaver, antall med kjent positiv og
  antall der hele universet er vurdert. Vurdert@k viser domsdekningen i resultatlisten.

En menneskevurdert topp-k-union gjør presisjon og MRR@k sammenlignbare for de
inkluderte kandidatene. Dekning blir fortsatt **dekning av poolens kjente
positiver**. En ny kandidat kan returnere uvurderte lærdommer; utvid da poolen
og merk dem blindt før sammenligning. Ekte dekning krever hele universet vurdert
eller et separat, representativt revisjonsutvalg med en eksplisitt estimeringsmetode.

### Funksjonsgrensesnitt

`evaluate({"navn": matcher_fn, ...}, data, labels, k=10)` tar funksjoner direkte.
Fra CLI: `--matcher navn=/sti/adapter.py:funksjon`, gjentatt for alle kandidater.

```python
def matcher(query, lessons, context):
    # Delegér til eksisterende kandidat. Returnér ordnede, unike lessonRef-er.
    # context: tags, surfaces, packages. Ingen fasit eller oppgavemappenavn.
    return existing_matcher(query, lessons, context)
```

Kandidatene får kopier av identiske input. §4, source, menneskedommer og oppgave-ID
sendes ikke til matcherfunksjonen. Den lokale importen er ikke en sikkerhetssandbox;
en adapter må følge kontrakten og kan ikke lese fasiten fra disk. Tidligere
læring/tuning på disse 19 oppgavene må oppgis; dette er utviklingsdata, ikke et
skjult testsett. Tags/surfaces er eksisterende oppgaveannotasjoner, ikke bevist
førstegangsinput fra G1.

`tag` bruker de faktiske funksjonene i `purpose_dev.py lookup`, i registerets
rekkefølge. Topp-k betyr de k første som leseren ville møtt, **ikke en ny
rangering av tag-treff**. `tfidf` gjenbruker tokenizer, vekting og cosine direkte
fra den eksisterende spikens funksjoner; ingen matcher er forbedret her. Adapteren
eksponerer hele rangeringen for MRR, der spiken bare viste topp-10.

Alle primærkjøringer bruker nøyaktig den nummererte §0 frem til neste nummererte
seksjon. Spikens gamle «inntil 2500 tegn etter §0» tar med senere seksjoner i fire
oppgaver og avkorter §0 i 14. `--legacy-query` bevarer den gamle ekstraksjonen som
en separat yardstick-kjøring. Primær og legacy må ikke blandes som én metode.

## 4. Tall fra denne harnessen

Korpus: 19 oppgaver, 44 lærdommer. Fast k=10. Ingen menneskedommer er laget i denne
leveransen. Tabellen under bruker bare source-positive par. [Full tabell](../maaling/resultat_source.txt),
[alle rangeringer og statistikk](../maaling/resultat_source.json).

| Kandidat | P@10 grenser, n=19 | R+@10, n=4 | MRR+, n=4 | MRR+@10, n=4 | Avsnitt@10 |
|---|---:|---:|---:|---:|---:|
| tag, opprinnelig rekkefølge | 0,000–1,000 | 0,000 | 0,050 | 0,000 | 20 |
| eksisterende TF-IDF | 0,032–1,000 | 0,476 | 0,642 | 0,625 | 20 |

Dette viser bare gjenfinning av de registrerte kildepositive lærdommene ved
avskjæring. Det er ikke et estimat av sann presisjon. Den uavkortede tag-listen
har snitt 35 lærdommer / 70 avsnitt; TF-IDF-visningen i spiken har 10 / 20.
Resultatfeltet `paragraphs_all=88` for TF-IDF gjelder dens **hele rangering på 44**,
ikke antall avsnitt som ble vist i spiken. Uavkortet tag-Jaccard er 0,809 med
23 felles lærdommer; topp-10-Jaccard måler et annet utsnitt.

| Fasit-/inputvariant | n med positiv | R+@10 tag | R+@10 TF-IDF | Tosidig p for parvis forskjell |
|---|---:|---:|---:|---:|
| Source, streng §0 | 4 | 0,000 | 0,476 | 0,250 |
| Source + utvalgte §4-refs | 5 | 0,204 | 0,334 | 0,250 |
| Også tekstoverlapp, bevisst kontaminert | 18 | 0,610 | 0,279 | 0,000412 |
| Source, bare lærdommer datert før oppgaven | 0 | NA | NA | NA |
| Source, gammel 2500-tegn-query | 4 | 0,000 | 0,289 | 0,250 |

Evidens: [curated](../maaling/resultat_curated.json),
[overlap](../maaling/resultat_overlap.json), [datofilter](../maaling/resultat_temporal.json),
[legacy](../maaling/resultat_legacy.json). Source + curated gir 41 positive par;
med overlap blir det 300. Den tilsynelatende sterke p-verdien i overlap-raden
kommer fra en fasit som gjenbruker dagens matcherutdata. **Statistisk tydelighet
gjør ikke en sirkulær fasit gyldig.**

For source-fasiten er R+@1 henholdsvis 0,000 / 0,286 og R+@5 0,000 / 0,476.
[k=1](../maaling/resultat_k1.json), [k=5](../maaling/resultat_k5.json).
Dette er følsomhetskontroller, ikke grunnlag for å velge beste k på testsettet.

Reproduser fra `CellProtocolDocuments/`:

```sh
MEAS=Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling
python3 "$MEAS/evaluer.py" retro --snapshot "$MEAS/korpus_44.json" --out /tmp/retrospektiv.json
python3 "$MEAS/evaluer.py" evaluate --snapshot "$MEAS/korpus_44.json" --truth source --k 10 --out /tmp/matching-source.json
python3 "$MEAS/evaluer.py" evaluate --snapshot "$MEAS/korpus_44.json" --truth curated --k 10
python3 "$MEAS/evaluer.py" evaluate --snapshot "$MEAS/korpus_44.json" --truth overlap --k 10
python3 "$MEAS/evaluer.py" evaluate --snapshot "$MEAS/korpus_44.json" --before-task-date
python3 "$MEAS/evaluer.py" evaluate --snapshot "$MEAS/korpus_44.json" --legacy-query
python3 "$MEAS/evaluer.py" power
```

For ekte dommer: `--truth human --human /sti/MATCHING_FASIT.json`, med `--human`
gjentatt for hver oppgave. Manglende menneskefasit fylles aldri med silver.
Motstridende menneskedommer avvises. Samme snapshot, dommer, kode og seed gir
samme tall; `elapsedSeconds` er naturligvis ikke deterministisk. Filhasher,
kodehasher, labelhash, seed og kandidatspesifikasjoner følger resultatet.

## 5. Statistisk edruelighet og antall oppgaver

Måleenheten er **oppgaven**, ikke lærdommen. De 44 lærdommene gir ikke 44
uavhengige forsøk; heller ikke 19×44. For hvert par kandidater beregnes
`d_q = metrikk(B,q) − metrikk(A,q)` på nøyaktig samme vurderte oppgaver.
Dette er en paret sammenligning. [NIST, *Analysis of paired observations*](https://www.itl.nist.gov/div898/handbook/prc/section3/prc311.htm).

Implementert:

- 10 000 bootstrap-utvalg av hele oppgaveforskjeller med tilbakelegging;
  2,5- og 97,5-persentilene gir et diagnostisk 95 %-intervall.
- Tosidig fortegnspermutasjon innen hvert par: eksakt for opptil 19 ikke-null
  forskjeller; ellers Monte Carlo med `(ekstreme+1)/(trekninger+1)`. Seed 20260911.
  Under nullhypotesen må kandidatetikettene kunne byttes innen oppgaven.
  [SciPy-dokumentasjonens beskrivelse av paret «samples»-permutasjon](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.permutation_test.html)
  beskriver metoden; implementeringen her bruker ingen SciPy-avhengighet.
- Eksakte P/MRR-sammenligninger bruker bare oppgaver der begge kandidaters
  relevansgrenser sammenfaller. R+ rapporteres separat som proxy. Både rå p og
  Bonferroni-justert p over testene med definert p i denne kjøringen lagres.
  Dette korrigerer ikke for gjentatte kjøringer, terskelvalg eller modellutvelgelse.

I source-kjøringen: **n=4**, tre ikke-null forskjeller, ΔR+=0,476,
standardavvik for forskjellene 0,421, bootstrapintervall [0,143; 0,833],
men **eksakt p=0,250**. Et positivt bootstrapintervall fra fire observerte oppgaver
er ikke tilstrekkelig evidens. Selv om alle fire hadde bedret seg, ville minste
mulige tosidige fortegns-p vært `2/2^4 = 0,125`. Med seks ensrettede forskjeller
kan p bli 0,03125; seks er en matematisk minimumsmulighet, ikke et forsvarlig
utvalgsråd eller en garanti om styrke.

### Hvor stor forskjell kan 19 oppgaver oppdage?

Det finnes ingen absolutt prosentgrense uten spredningen i de parede forskjellene,
effektmålet og ønsket styrke. Som **planleggingsscenario**, ved tosidig α=0,05 og
80 % styrke:

`n ≈ ((1,960 + 0,842) × s_d / δ)^2`

Dette er en normaltilnærming for forskjellene, ikke et løfte om permutasjonstestens
styrke. Ukjent varians og små utvalg trenger mer forsiktig planlegging og senere
styrkesimulering. [NIST, *Sample sizes required*](https://www.itl.nist.gov/div898/handbook/prc/section2/prc222.htm).

Tallene genereres av `evaluer.py power`; δ måles i **absolutte prosentpoeng**, ikke
relativ forbedring:

| Antatt s_d | Minste omtrentlige utslag ved n=19 / 80 % styrke | n for +5 pp | n for +10 pp |
|---|---:|---:|---:|
| 0,10 | 6,4 pp | 32 | 8 |
| 0,20 | 12,9 pp | 126 | 32 |
| 0,30 | 19,3 pp | 283 | 71 |
| 0,50 | 32,1 pp | 785 | 197 |

Særlig de små n-tallene er grove normalanslag, ikke presise minimumskrav.
Med n=19 er den omtrentlige detekterbare effekten `0,643 × s_d`; en vanlig
95 %-t-grense rundt en observert middelforskjell er omtrent `0,482 × s_d`.
Den siste er en signifikansgrense, **ikke 80 % styrke**. Med observert source-s_d
ville +10 pp tilsi omtrent 139 oppgaver, men et variansanslag fra fire skjeve
oppgaver er altfor ustabilt til å være bestillingsgrunnlaget.

**For moderate utslag trenger vi flere oppgaver enn vi har.** Et praktisk opplegg:

1. Velg primærmål og minste nyttige utslag før nye resultater: eksempelvis
   menneskevurdert P@10, +10 pp, med uendret avsnittsbudsjett og separat kontroll
   av tapte alvorlige treff. Lås kandidatene før bekreftende evaluering.
2. Bruk 20 nye pilotoppgaver til tidsbruk, relevanskriterium og variansanslag.
   De 19 eksisterende er utviklingsdata. Ikke velg kandidat og bekreft den på
   samme merkede materiale. Gjennomgå uenighet på et lite dobbeltvurdert utvalg.
3. Planlegg deretter **omtrent 100 nye, tilstrekkelig uavhengige oppgaver** for
   +10 pp hvis s_d≈0,30. Er s_d≈0,50, trengs omtrent 200. For +5 pp ved s_d≈0,30
   er størrelsesordenen 300. Dette er betingede anslag; pilotdata skal bestemme
   et fast endelig utvalg før testen fortsetter.
4. Beslektede oppgaver fra samme leveranse/prosjekt er korrelerte. Bruk ett
   forhåndsvalgt tilfelle per uavhengig oppgavefamilie, eller implementer
   blokkbootstrap/-permutasjon på familier. Dagens harness trekker oppgaver,
   **ikke prosjektblokker**. Dersom alle oppgavene kommer fra få familier,
   kreves flere oppgaver/familier enn tabellen antyder.

Gjennomfør ikke «test til p<0,05». Flere hundre like, feilmerkede oppgaver blir
heller ikke en god fasit. Relevansmålet er nærmere nytte enn Jaccard, men faktisk
forebygging krever neste trinn: logg ved G1 hvilke råd som ble vist, og ved senere
læring hvilken ny feil som er `repeatOf` hvilken tidligere feil, hvilken test som
var aktiv, og kjøringsbevis. Ikke tell en oppgave uten rapportert feil som bevist
forebygget. Et kontrollert fremtidig sammenligningsopplegg trengs for kausal nytte.

## 6. Verifikasjon og gjenværende usikkerhet

**20 harnesstester og 29 eksisterende PurposePackages-tester passerte.** Faktiske
utdata er lagret i [TESTUTDATA.txt](../maaling/TESTUTDATA.txt). Sju evalueringsvarianter
ble kjørt med samme frosne 44-kohort og kodehasher.

Kjøringer fra repo-roten:

```sh
python3 -m unittest discover -s Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling -p 'test_*.py' -v
python3 -m unittest discover -s Tools/PurposePackages/tests -v
```

Harnesstestene dekker håndregnet P/dekning/MRR, ufullstendig fasit, tomme og korte
lister, lesebelastning, eksakt liten permutasjon, kildegrenser, auto-sitater,
datofilter, query-avgrensning, hashdrift, isolerte matcherinput, duplikater,
CLI-registrering, gjenopptakelse og avbrudd. Det uendrede TF-IDF-skriptet kjøres
dessuten mot midlertidige kopier av de frosne inputene; alle 19 hele rangeringer må
stemme med adapteren i legacy-modus. Eksisterende PurposePackages-tester kontrollerer
at underkommandoen ikke bryter tidligere verktøyatferd.
Tomme eller helt uvurderte kjøringer som leveres til evalueringen beholdes i
oppgaveutvalget; vanskelige oppgaver forsvinner ikke fordi de mangler treff/dom.

Åpent med eier:

- Oppgaveeier/menneskelig G1-leser: registreringstid <60 s og relevanskalibrering
  er ikke målt hos mennesker. Ingen reelle G1-dommer er oppfunnet.
- Senere evalueringsrunde: representativ negativ/positiv fasit, prosjektgrupper,
  faktisk registreringstid for lærdommer og målt forebygging mangler.
- Matcherens effekt på nytte: påstanden står **åpen**, fordi verken proxyfasiten
  eller utvalget gir støtte til en konklusjon om hvilken matcher som er best.

Arbeidets bærende påstander er knyttet til filene/tallene over. Tidsmålet er
merket uprøvd, utvalgsanslagene er merket scenarioer, og auto-sitatforklaringen har
en konkret falsifikasjonskontroll gjennom den kontaminerte overlap-kjøringen.
Dette er en lokal metodeleveranse, ikke en panelavstemning eller offentlig
kapabilitetspåstand.
