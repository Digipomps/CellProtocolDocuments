# Formålssammensetning i purpose_dev

Implementerer Book 36 for kunnskapsbasen, formålene i pakkene og lokale oppgaver.
Kjør fra en vilkårlig arbeidsmappe med Python 3.9 eller nyere; verktøy og tester
bruker bare standardbiblioteket. Behold `purpose_dev.py` og
`purpose_composition.py` i samme mappe når verktøyet kopieres til Cowork-VM-en.

```sh
python3 Tools/PurposePackages/purpose_dev.py validate
python3 Tools/PurposePackages/purpose_dev.py validate /sti/til/oppgave
python3 Tools/PurposePackages/purpose_dev.py gates /sti/til/oppgave
python3 -m unittest discover -s Tools/PurposePackages/tests -v
```

`validate` gir inntil videre **advarsel** for hver ikke-løvnode uten
`composition`, med samlet antall og antall Book 23-noder. Feltet får ingen
default, og en slik samling kan ikke bli verifisert grønn. Eksisterende
kanoniske noder migreres i en egen leveranse. Regel 2–6 gir feil. Ugyldig type,
ukjente kombinatorer, tvetydige referanser/tidspunkt og sykluser gir også feil.

`gates` beholder visningen og artefaktkontrollen av G1/G1-GUI/G2/G3 og viser en
separat `Composition-port`. Den beregnes for samlinger i oppgavens noder,
tilknyttede pakkeformål, arvede formålsreferanser, rapporterte formål og deres
forfedre med eksplisitt composition. Dette registrerer ingen menneskelig
portgodkjenning. Undersamlinger vises, men deres forelder avgjør om en rød
eller ikke-verifisert alternativ gren hindrer helheten. Returkoder fra `gates`:

| Kode | Tilstand | Betydning |
|---|---|---|
| 0 | `green` | De øverste samlingene i omfanget er verifisert grønne, uten valideringsfeil. |
| 1 | `red` | Brudd eller valideringsfeil. |
| 2 | `blocked` | Minst én samling er blokkert; årsaken vises. Andre feil vises fortsatt. |
| 3 | `unverified` | Manglende sammensetning, gren, målinger eller forsøk; også uten definerte samlinger. |

`blocked` bevares også når `anyOf` allerede har nok grønne alternativer, eller
et annet barn er rødt. `validate` skiller fortsatt mellom gyldig data (0) og
feil (1); en gyldig logg med blokkering er ikke i seg selv en valideringsfeil.

## Format

JSON-schemaene ligger i `Book/haven_purpose_*_v0.schema.json`. KB- og
pakkefilene peker på sine schemaer med `schemaRef`. Schemaene deler definisjoner
av `composition`, noder og kjøringslogg. Kryssreferanser, antall barn og
historiske tilstander kontrolleres av Python-verktøyet; det bruker ingen
JSON Schema-avhengighet og er ikke en generell JSON Schema-validator.

Oppgavens valgfrie `PURPOSE_COMPOSITION.json` inneholder `nodes` og `execution`.
Nodene utvider KB- og pakketreet; en eksisterende `purposeRef` kan ikke
overskrives. Egne trær kan ha `parentRef: null`. Referanser i loggen kan også
peke på eksisterende KB- eller pakkeformål. Både KB- og pakkedokumentene kan
ha `execution` på toppnivå; kjøringsloggen for en konkret oppgave bør ligge i
oppgavens fil. `validate` undersøker hele det kombinerte datasettet.

Barn bestemmes av `parentRef`. For `sequence` og `firstOf` skal forelderen ha
`childOrder`, med hvert direkte barn nøyaktig én gang. Arrayrekkefølgen i
`nodes` eller mellom pakker er ikke en implisitt kontrollrekkefølge.
`allOf` har ingen rekkefølge; `anyOf.min` er et positivt heltall, default 1.
`invariant.over` må peke på en annen samling i samme sammenhengende tre.
Plasser invarianten som en egen gren ved siden av en ordnet samling, slik at
betingelsene ikke blir steg i samlingens `childOrder`.

Kjøringsloggen holder tre slags påstand atskilt:

- `measurements`: observasjoner av bladformål, med `measuredAt`, `state` og
  `evidenceRef`. `blocked` krever `reason`. En samlings grønne status er en
  slutning og kan ikke skrives som måling.
- `reports`: rapporterte slutninger, med `reportedAt`, `state` og
  `purposeRef`. Grønne rapporter kontrolleres mot evidensen som forelå da.
  `firstOf` registrerer valgt direkte barn i `branchRef` her.
- `opinions`: meninger, med `purposeRef` og `text`. De brukes aldri som
  verifikasjonsevidens.

`attempts` registrerer hendelser, med unik `attemptRef`, `purposeRef`,
`attemptedAt` og eventuelt `finishedAt`. Tidspunkter er ISO 8601 med tidssone.
Poster sorteres etter tidspunkt; motstridende eller doble målinger/rapporter
på samme tidspunkt avvises. Logg alle forsøk og behold historikken i samme
kjøring. Et nytt forsøk krever en ny måling; en gammel grønn måling blir ikke
automatisk videreført. Verktøyet leser loggen og endrer den ikke.

## Sekvens, grenvalg og invarianter

For `sequence` må forgjengeren være verifisert grønn **før** `attemptedAt`,
med registrert forsøk også for første barn. Samme tidspunkt er ikke «før».
Kontrollen beregner også sammensatte forgjengeres historiske tilstand. Et
for tidlig forsøk blir ikke reparert av senere grønne målinger eller et nytt
forsøk i samme logg. Barnet selv kan heller ikke rapporteres grønt etter et
slikt brudd.

For `firstOf` prøves barn i `childOrder`. Tidligere grener må være verifisert
røde før neste forsøkes. Første grønne gren avslutter kjøringen; nye forsøk
etter suksess avvises, også om suksessen senere trekkes tilbake. Den valgte
grenen må registreres i `reports[].branchRef`. Manglende gren gir
`unverified`; en eksplisitt grønn rapport uten gren avvises av regel 4.

For `invariant` har hver måling av en betingelse også `attemptRef` til steget
i `over`, samt `phase: "before"` eller `"after"`. Hvert utført steg trenger
`attemptedAt`, `finishedAt` og grønne målinger av hver betingelse på begge
sider av steget. En etter-måling kan ikke utsettes til neste steg har startet;
en før-måling kan ikke gjenbrukes fra før et tidligere steg ble ferdig.
Uforsøkte alternativer i en disjunksjon trenger ingen måling.

Et rødt invariantfunn forblir et brudd selv om en senere måling er grønn.
Forsøk etter bruddet rapporteres særskilt. Invarianten begrenser `over`
uavhengig av hvor den ligger i treet, så en grønn alternativ gren i `anyOf`
kan ikke omgå bruddet. CLI-en kontrollerer registrert arbeid; den er ikke en
prosesskjører og kan ikke stoppe en ekstern prosess. Porten kan bare regnes som
verifisert grønn på returkode 0. Ingen automatisk rollback utføres.

## Minimal sekvens

Lagre dette som `PURPOSE_COMPOSITION.json` i en oppgavemappe. Tidspunktene og
referansene er et syntetisk eksempel; reelle kjøringer skal registrere sine
egne faktiske forsøk og observasjoner.

```json
{
  "schema": "haven.purpose-composition-run.v0",
  "nodes": [
    {"purposeRef": "purpose://example", "parentRef": null,
     "composition": {"kind": "sequence"},
     "childOrder": ["purpose://example.a", "purpose://example.b"]},
    {"purposeRef": "purpose://example.a", "parentRef": "purpose://example"},
    {"purposeRef": "purpose://example.b", "parentRef": "purpose://example"}
  ],
  "execution": {
    "attempts": [
      {"attemptRef": "a-1", "purposeRef": "purpose://example.a",
       "attemptedAt": "2026-09-09T10:00:00Z"},
      {"attemptRef": "b-1", "purposeRef": "purpose://example.b",
       "attemptedAt": "2026-09-09T10:00:02Z"}
    ],
    "measurements": [
      {"purposeRef": "purpose://example.a", "state": "green",
       "measuredAt": "2026-09-09T10:00:01Z", "evidenceRef": "TESTRESULT.md#a"},
      {"purposeRef": "purpose://example.b", "state": "green",
       "measuredAt": "2026-09-09T10:00:03Z", "evidenceRef": "TESTRESULT.md#b"}
    ],
    "reports": [
      {"purposeRef": "purpose://example", "state": "green",
       "reportedAt": "2026-09-09T10:00:04Z"}
    ],
    "opinions": []
  }
}
```

Verktøyet kontrollerer loggens form, referanser og sammensetningssemantikk.
Det beviser ikke at oppgitte tidspunkter eller observasjoner er sanne, eller at
verifikatoren måler riktig egenskap; `evidenceRef` er en sporbar referanse,
ikke en automatisk inspeksjon av artefaktens innhold (Book 36 §6).

## G1-fasit for formålsmatching

`purpose_dev.py judge TASKDIR --run RUN.json` registrerer menneskets vurdering av
en frosset liste i `TASKDIR/MATCHING_FASIT.json`. Normalrunden har tre svar:
relevante nummer, eventuelle gjentakelser, og testref eller eksplisitt grunn til
manglende håndhevelse. `?nummer` står uvurdert; tomt svar betyr aldri nei.
Fortsett med `judge TASKDIR`, eventuelt `--batch-size 10` for delrunder.
Dette setter ingen port til godkjent og endrer ikke lærdomsregisteret.

Kjøringen lages med `evaluer.py pool`. Schema, CLI-flyt, avgrensninger og
reproduserbare målinger er beskrevet i
[teststrategien](../../Deliverables/PDD_formaalsregister-som-graf_2026-09-11/handoff/TESTSTRATEGI_MATCHING.md).
`matching_judgment.schema.json` er JSON Schema 2020-12. Den lokale
`purpose_judgments.py`-validatoren støtter bare delmengden dette schemaet bruker,
pluss kontroll av referanser, duplikater og rekkefølge for `repeatOf`.
Ta med begge filene hvis `judge` skal kjøres fra en kopi av verktøymappen.
