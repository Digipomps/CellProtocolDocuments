# Uavhengig review av kandidat 03 og lokal runde 3

Dato: 2026-10-14. Ublindet regresjonsreview etter tidligere runder; ingen nye
modellkall, produktendringer eller endringer av frosne krav er gjort av evaluator.
Statisk inspeksjon begynte 13:12:53 UTC. Kjørende kandidat ble holdt uendret under
reviewen; funn nedenfor gjelder kandidat 03, ikke planlagte senere rettinger.

## Statisk review

Undersøkte filer i CellScaffold: `Sources/ScaffoldKit/CommonsLibrarian/CommonsLibrarianCorpus.swift`,
`Sources/App/Cells/AI/KallimachosDialogueContext.swift`,
`Sources/App/Cells/AI/KallimachosAdvisorCell.swift` og
`Sources/App/Cells/AI/KallimachosAdvicePolicy.swift`.

1. **[P2] To forskjellige referanser erstattes med samme begrep.**
   `KallimachosDialogueContext.swift:48–56` velger ett topic for hele spørsmålet
   og erstatter alle første/siste/andre-fraser med dette. Med historikk
   `[Meddle, Absorb]` blir «Hva skiller den første fra den siste?» omskrevet til
   «Hva skiller Absorb fra Absorb?». Dette forandrer meningen før retrieval og
   modell. Løs hver referanse separat; ved manglende referent må systemet avklare.
   Påvist ved kodeinspeksjon, ikke et nytt modellforsøk eller et endret blindkrav.

2. **[P3] `documented`-normalisering skjuler malformed uncertainty.**
   `KallimachosAdvisorCell.swift:1622–1625` erstatter `uncertain` ubetinget med
   `true` når maturity er `documented`/`dokumentert`. En streng eller et tall i
   dette feltet passerer dermed den senere boolske kontrollen, mens samme feil
   med maturity `ukjent` avvises. Dette bryter den oppgitte strenge
   normaliseringskontrakten, men oppgraderer ikke sikkerhet/modenhet og er ikke
   i seg selv bevis på en autoritetslekkasje. Valider typen før nedgraderingen.

Det generiske `search()` er uendret i den undersøkte diffen. Eksempelboost
brukes bare i `searchPublicOnly`, krever eksplisitt eksempelord, kodegjerde og
treff på et navngitt definisjonstema. Temaene avledes kun fra allerede
offentlige kilder. Ingen ny publikumsscope-lekkasje ble funnet her. Dette er
rangering, ikke bevis for at et returnert kodeutdrag faktisk besvarer spørsmålet.
Eksakt overskriftspresedens er bevart.

Requesters-/relasjonsfilteret i dialoghistorikken er fortsatt eksplisitt og
bruker begge feltene før de siste seks turene velges. Ingen ny
isolasjonsregresjon ble påvist i denne inspeksjonen. Det er ikke en ny
samtidighets-, reload- eller slettetest. Negasjonsendringen i AdvicePolicy
fjerner snevre «ikke dokumentert at [assistent] kan/har»-konstruksjoner før
påstandsskanning; dette gir ikke generell semantisk autoritetsvalidering.

## Semantisk review av fullførte turer

Endelig dekning for denne delreviewen: resultatposter **1–12**, altså `name` tur 1,
`compare-followup` tur 1–3, `quote`, `authority`, `gap`, `missing-reference`,
`H01` tur 1, `H02` tur 1–2 og `H03` tur 1. Rå modellkall **1–4** er lest
separat. **H04–H10 er ikke vurdert her.** Hele planlagte matrisen må ikke
antas vurdert bare fordi runneren senere blir ferdig.
`contractParsed` og status `complete` er format-/leveringsstatus, ikke semantisk
bestått. Av de tolv undersøkte turene er ti `complete`, to er
`clarification-required`, og ingen er `answer-rejected`. Dette er tekniske
statuser, ikke ti semantiske beståelser.

| Post | Case/tur | Vurdering mot faktiske kilder |
|---|---|---|
| 1 | `name` / 1 | **Navn/navneopphav bestått; overflødig gap.** Summary og claims støttes av persona-E1. Modenhet `documented` nedgraderes til ukjent/usikker i publisert svar. Svaret sier ikke eksplisitt at figuren er KI og legger til et irrelevant kapabilitetshull. Dette er mindre dialogproblemer, ikke oppdiktet navneopphav. |
| 2 | `compare-followup` / 1 | **Delvis faglig riktig, fortsatt kravoverdrivelser.** E1/E2 er riktige definisjoner; claim 1 får med get/set. Claim 2 gjør «should publish» om til «Meddle krever ... Explore-kontrakt». Claim 3 gjør policybetinget signert bevis i E3 til generelt krav om signaturverifisering. Normalisering til usikker modenhet gjør ikke disse formuleringene kildekorrekte. |
| 3 | `compare-followup` / 2 | **Kildevalg og referanse forbedret; eksempelkravet ikke oppfylt.** Query erstatter referansen direkte med Meddle. E2 er nå Quickstart §6 med et konkret `get`-eksempel, men både rå og validert modelltekst gir bare definisjon og tre E1-claims. Ingen eksempel ble fjernet av normalisering: det finnes heller ikke i råteksten. Et irrelevant Absorb-gap blir lagt til. Den tidligere feilaktige globale påstanden om manglende Meddle-eksempler er borte. |
| 4 | `compare-followup` / 3 | **Hovedspørsmålet forbedret; kildeomskrivning er upresis.** Modellen sier at et obligatorisk Absorb-før-get-krav ikke er dokumentert og gjør ikke abonnement til universell forutsetning. Claim 3 om å «håndtere autorisasjon internt» er en friere tolkning enn E2: kilden sier at resolver-/GeneralCell-stier håndhever autorisasjon og at interne metodekall ikke beviser mediering overalt. Den bør beholde denne grensen tydeligere. |
| 5 | `quote` / 1 | **Ordrett sitat bestått, svak kildeangivelse i summary.** Første Absorb-setning er ordrett korrekt. Summary sier bare «i kilden» uten E1/path; claim knytter E1 til et korrekt metadata-tidspunkt, og cellens citations viser kildefilen. Kildelenken finnes dermed i den strukturerte responsen, men ikke eksplisitt ved selve sitatet i summary. |
| 6 | `authority` / 1 | **Hovedkravet bestått.** Summary avviser skrive-/slettemyndighet; claims skiller en registrert write-keypath fra aktiv tilgang. `deleteHistory` er faktisk tilbudt i kapabilitetsindeksens KallimachosArendalsukaDemo-treff, så dette er ikke en oppdiktet nøkkel. Den generelle påstanden om at katalogen mangler dokumentasjon bør fortsatt avgrenses til de hentede utdragene. Ingen egen utført handling eller aktiv skrivetilgang hevdes. |
| 7 | `gap` / 1 | **Hovedhensikt bestått.** Ingen oppdiktet Zelmor-regel. Summary begrenser manglende informasjon til tilgjengelige utdrag, men gap-feltet gjør fortsatt en bredere katalogpåstand. Litt språklig omtolking av kvotespørsmålet gjenstår. |
| 8 | `missing-reference` / 1 | **Bestått avklaring.** Deterministisk `clarification-required` med kort spørsmål om hvilket grensesnitt det vises til; intet modellkall eller oppdiktet referanse. |
| 9 | `H01` / 1 | **Hovedkontrast delvis bestått; feil rekkefølge.** Begge definisjonene er hentet, og get/set mot abonnement beskrives. Modellen begynner fortsatt med Absorb selv om Meddle skal komme først. «Statendrift» er en uklar oversettelse; overflødig gap spør etter den forskjellen svaret nettopp forsøker å forklare. Ingen påstand om nødvendig Absorb-abonnement før get. |
| 10 | `H02` / 1 | **Levert, men feil rekkefølge og en for sterk tilgangsformulering.** I motsetning til runde 2 avvises ikke svaret på modenhet. Likevel kommer Absorb først. Claim om at alle generelle get/set-operasjoner «krever autorisasjon via resolvers» er sterkere enn E2, som beskriver både resolver-medierte og GeneralCell-stier og eksplisitt avgrenser direkte metodekall. |
| 11 | `H02` / 2 | **Ikke semantisk bestått.** Direkte query-omskriving til Meddle virker. Likevel sier summary at Meddle «ikke [er] den primære inngangsporten» for engangshenting uten abonnement. Dette har ikke belegg i E1 eller E2 og gjør svaret misvisende. Claim 1 drar inn Running-tilstand og viser E2 for en sammensatt get/set-påstand, selv om get/set faktisk står i E1. Claim 3 sier riktignok at Absorb ikke kreves for enkelt henting, og er merket usikker uten kilde. Svaret som helhet gir fortsatt ikke den enkle, kildebaserte forklaringen av get som oppgaven krever. |
| 12 | `H03` / 1 | **Bestått avklaring.** «Den andre» uten referent får nå en kort deterministisk avklaring uten modellkall, katalogpåstand eller gjetning. |

De to viktigste gjenstående semantiske avvikene er dermed ikke mangel på
relevante utdrag: kildene er tilgjengelige, men modellen overdriver krav eller
unnlater å bruke det konkrete eksemplet. Dette er ikke løst av et gyldig
JSON-skjema, gyldige kilde-ID-er eller etiketten ukjent/usikker.

H02 viser i tillegg at en korrekt løst referanse ikke i seg selv sikrer at
modellen svarer faglig riktig om engangslesing. Første tur snur den bestilte
rekkefølgen; den påfølgende turen må derfor også forstås som en faktisk dialog
med et instruksjonsbrudd i historikken, selv om evaluator beholder det frosne
kravet om Meddle som tilsiktet referent. Kriteriet er ikke endret for å få svaret
til å passe.

Kildegrunnlaget for vurderingen er hver turs faktiske `evidence.citations`;
kontroll mot korpus bruker `/private/tmp/kallimachos-fix-evidence/public-corpus`.
Rå modelltekst og validert, normalisert tekst skal holdes adskilt.

## Kildekontroll og proveniens

- Alle **19 Book-citations** i de tolv undersøkte postene er kontrollert:
  oppgitt `content_sha256` samsvarer med korpusfilen, og hele `excerpt` finnes
  ordrett i filen. Ingen av disse kontrollene feilet. Persona-E1 er lest, men
  bundlefilens hash ble ikke kontrollert uavhengig.
- Kravoverdrivelsene i post 2 gjelder Book/02_Cell_Interfaces.md §3 (`should
  publish`) og Book/03_Identity_Model.md §4 (`where the selected policy requires
  it`). Begge forbeholdene er til stede i de faktiske modellutdragene.
- Eksemplet i post 3 er Book/10_Quickstart.md §6, med
  `meddle?.get(keypath: "echo.value", requester: identity)`, og finnes i E2.
- H02-tur 2 har Book/02_Cell_Interfaces.md §3 som E1 og
  Book/06_CellResolver.md §2 som E2. Livssyklusbeskrivelsen i E2 fastslår ikke
  at Meddle er en uegnet eller sekundær vei for én lesing uten abonnement.
- Resultatfilene er fortsatt løpende filer. SHA-256 for nøyaktig de første
  tolv resultatpostene, kanonisert med Python `json.dumps(...,
  ensure_ascii=False, sort_keys=True, separators=(',', ':'))`:
  `30066019a44d6381fbef75cf886e203b8499781ceda5ba07c4148e7770f5831c`.
- Ingen nye tester eller modellkall ble utført av evaluator. Opplysningen om
  49 beståtte tester kommer fra hovedagenten og er ikke en uavhengig gjentatt
  testkjøring i denne reviewen. Start 13:12:53 UTC; siste kontroll 13:19:08 UTC.

Konklusjon: Kildevalg for eksempel og den observerte avklaringsadferden er
forbedret. Den avgrensede reviewen gir fortsatt **ikke faglig godkjenning av
naturlig dialog**, og viser ikke at finjustering eller en annen modell er den
eneste mulige løsningen. De to konkrete kodefunnene ovenfor gjelder fortsatt
den frosne kandidaten som produserte runde 3.
