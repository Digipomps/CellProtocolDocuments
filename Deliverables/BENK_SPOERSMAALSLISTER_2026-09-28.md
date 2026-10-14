# Spørsmålslister i utviklerbenken — inntak 2026-09-28

**Delvis dekket fra før; ett nytt inntak er nødvendig for hele livsløpet.** Bestillingen er
registrert som **E8 — Eierens spørsmål og svar har ett sted å bo**, en kandidatoppgave til benkens
PDD-løp. Ingen løsning er bygget, ingen port er godkjent og ingen commit er laget.

## Hvor bestillingen er ført inn

| Sted | Hva er ført inn |
|---|---|
| [FORMAALSSPEC.md §0 og §1 E8](PDD_utviklerbenk-oppgavegraf_2026-09-10/FORMAALSSPEC.md#e8-sporsmallister) | Kjetils intensjon, formål, momenter til P1, dekningsgrense og neste steg. §7 har revisjonslogg. |
| [PURPOSE_COMPOSITION.json](PDD_utviklerbenk-oppgavegraf_2026-09-10/PURPOSE_COMPOSITION.json) | Én ny lokal kandidat: `purpose://candidate.utviklerbenk.plangraf.sporsmallister`, under `purpose://candidate.utviklerbenk.plangraf`. Ingen kjøring eller måling registrert. |
| [STATUS.md — Inntak 2026-09-28](PDD_utviklerbenk-oppgavegraf_2026-09-10/STATUS.md#inntak-2026-09-28--e8-spørsmålslister) | Inntaksstatus, beslutningseier og vei til P1/G1. Eksisterende porter er urørt. |

Dette er ett inntak med samme kandidat-ID i PDD-dokumentene, ikke flere oppgaver. Det er ikke skrevet
til en kjørende WorkItemCell, det globale formålsregisteret eller en ny spørsmålsdatabase.
Detaljdekomponering, testkontrakt, datamodell og GUI tilhører den videre PDD-runden.

## Hva som allerede dekker deler av behovet

Kontrollen gjelder den lokale [FORMAALSSPEC.md](PDD_utviklerbenk-oppgavegraf_2026-09-10/FORMAALSSPEC.md)
og tilhørende komposisjon og status, lest 28.09.2026. Den er ikke en test av benkens kjørende versjon.

| Eksisterende element | Dekker | Mangler mot denne bestillingen |
|---|---|---|
| E3 `…plangraf.mine-handlinger-utforbare` | Eierens konkrete handling, svarvei og bevis tilbake til kilden. | En liste med spørsmål, alternativer/fritekst og eget livsløp for svar og innføring. |
| E5 `…plangraf.aldri-utdatert` | Én versjonert sannhet, synlig kildekonflikt og status som krever bevis. | Skillet åpent/besvart/ført inn per spørsmål, og synlig gjenåpning med bevart historie. |
| Valgbenken, §0 tillegg 15.–16.09 | Spørsmål, alternativer med konsekvens, anbefalinger og eierrespons; prototype knyttet til E3/E4. | Et beskrevet, samlet livsløp i benken fram til svaret er innført. En artefaktdatabase er ikke bevis for dette. |
| Dommerbenken, §0, kandidat `…utviklerbenk.dommerbenk` | Forståelig spørsmål/svar, vurdering per rad, notat, lagring og hendelseshistorikk. | Generelle beslutningslister og sporbar innføring i det beslutningen påvirker. Kandidaten er ikke dekomponert. |
| E4, E6 og E7 | Henholdsvis forklaring, plass i eksisterende benk og senere fil-/celleimport. | Er støtte og mulig gjenbruk, ikke dekning av spørsmålslivsløpet. E7 er selv en kandidat for senere G1. |

Konklusjonen er derfor **ny kandidatoppgave for restbehovet, med gjenbruk av eksisterende elementer**.
Det er ikke opprettet nye kopier av E3/E5 eller en konkurrerende Dommerbenk.
Book 23 har også `purpose://project-work.work-items` og
`purpose://digital-work.collect-structured-input`, samt spørreskjemaformål for innsamling av svar
([lokalt register](../Book/haven_purpose_knowledge_base_v0.json)). Disse gir forankring og kandidater
til gjenbruk; registertekst alene beviser ikke støtte for beslutningsoppfølging i benken.

## Formål og kildekontroll

Formålet er at eierbeslutningen har **ett autoritativt sted fra spørsmålet stilles til svaret er ført
inn i det det påvirker**. E8 bevarer alle momentene: åpent/besvart/ført inn, listevalg eller fritekst,
klart skille mellom anbefaling og svar, spor til endringen, synlig gjenåpning og sammenheng med
dokumentasjon/skjema uten manuell kopiering mellom konkurrerende originaler.

| Premiss | Kontroll og kilde |
|---|---|
| Seks spørsmål om vedlegg | **Lest:** [vedleggs-PDD §2](PDD_vedlegg-korrespondanse_2026-09-28/FORMAALSSPEC.md) har seks hovedvalg D1–D6. §6 har også D7–D8; seks er derfor ikke hele antallet åpne eiervalg i dokumentet. Ingen av dem er besvart i denne jobben. |
| 45 kommentarer i beslutningsregisteret | **Telt:** [review-decisions-2026-09-16.json](../../CellProtocol/Docs/EntityData-Review-2026-09-11/review-decisions-2026-09-16.json) har 45 poster under `comments`, med kilde, ordrette kommentarer og status. |
| 46 elementbeslutninger og et HTML-artefakt med database | **Opplyst av Kjetil:** Det konkrete settet med 46 er ikke identifisert i denne avgrensede lesingen. [Gjennomgangsutskriften](../../CellProtocol/Docs/EntityData-Review-2026-09-11/GJENNOMGANG_KJETIL_2026-09-16.md) oppgir 253 elementer: 203 godkjent uten kommentar, 45 med kommentar og 5 uberørt. Settene skal ikke likestilles eller slås sammen uten kildeavklaring. Artefaktdatabasen er ikke inspisert. |
| Svar er ikke automatisk ført inn | **Lest:** [oppfølgingen 17.09](../../CellProtocol/Docs/EntityData-Review-2026-09-11/OPPDATERT-ETTER-GJENNOMGANG-2026-09-16.md) dokumenterer at gjennomgangen var publisert, mens skjema og grafikk fortsatt brukte grunnlaget fra 11.09. Senere innarbeiding retter dette; rapporten påstår ikke at avviket fortsatt består. |
| Dokumenter kan komme i utakt også i benkens eget løp | **Lest:** Benkens FORMAALSSPEC §6 sier at Q1–Q3/Q5/Q6 er åpne. STATUS-loggen 14.09 har Kjetils svar på de samme spørsmålene. STATUS har dessuten G1/G1-GUI godkjent 14.–15.09, mens spesifikasjonens topptekst fortsatt sier G1 venter. Avviket er dokumentert her; de historiske vedtakene er ikke tolket på nytt eller overskrevet. |

Kildegrunnlaget er lokale PDD-/gjennomgangsfiler og eierens bestilling. Ingen aktuell nett-,
staging- eller runtimekapabilitet er lagt til grunn uten måling.

## Hva som gjenstår før eieren kan besvare en liste i benken

1. **P1 og avgrenset G1-tillegg:** Benkens eget løp avleder mål og tester, kontrollerer gjenbruk og
   avklarer hva som eier spørsmål/svar, hvordan det føres inn i berørte kilder og hvordan gjenåpning
   beholder historikk. Filer først er allerede valgt for plangrafen; E8 velger ikke en ny database
   eller krever full E7-migrering. Svarregistrering må skilles fra tillatelse til å utføre endringen.
2. **GUI-grunnlag og G1-GUI for E8:** Vis forståelige spørsmål, alternativer, fritekst, anbefaling,
   faktisk svar og livsløp i benken. Eksisterende godkjenning av plangrafbildene v1 omfatter ikke
   automatisk denne nye flaten. Gjenbruk og eventuelle renderergap må dokumenteres.
3. **G2-plan og gjennomføring i benkens løp:** Avtal konkret arbeid og tilbakeføringsvei. Dokumenter
   hvordan mislykket innføring og kildekonflikter forblir synlige, slik at «besvart» ikke vises som
   «ført inn». Denne bestillingen gir ingen kode- eller commit-autorisasjon.
4. **Verifisert brukerforløp før G3:** Fra benkens vanlige inngang åpner eieren en liste, gir ett
   listevalg og ett fritekstsvar, finner dem igjen etter ny åpning, følger svaret til den faktiske
   endringen og gjenåpner et spørsmål med synlig historikk. Ubesvarte anbefalinger forblir ubesvart,
   og mislykket tilbakeføring blir ikke merket ført inn. De avtalte klientene må prøves i sitt
   faktiske miljø. Vedleggsvalgene D1–D6 er det første konkrete underlaget, med D7–D8 avklart som
   omfang i P1; eiersvar skal ikke oppdiktes for prøven.

Beslutningseier er Kjetil; neste ansvarlige løp er benkens P1. Frist og individuell utfører er ikke
satt. **Denne inntaksjobben er fullført når registreringen og rapporten er kontrollert; produktmålet
er fortsatt åpent.** Benkens STATUS har G2/G3 som venter og ingen PLAN.md finnes i den undersøkte
PDD-mappen. Dokumentregistreringen er ikke bevis for at listen nå kan besvares i benken.

## Dokumentkontroll

Kontrollert 28.09.2026:

- JSON kan leses. Nøyaktig én kandidat er lagt til, med eksisterende forelder og unik ID.
  Alle tidligere noder, tom kjøringslogg og portlinjene i STATUS er bevart uendret.
- Komposisjonskontrollen gir **0 feil**, med de samme 19 Book 23-advarslene som før.
- Alle 14 lokale lenker i rapporten og de nye inntaksavsnittene peker til eksisterende filer;
  de brukte ankerne finnes. Markdown og JSON dekker de samme seks momentene.
- Ingen PLAN.md, TESTRESULT.md eller ACCEPT.md finnes i den undersøkte benk-PDD-mappen.
  Ingen kode, GUI, funksjonstest, commit eller push er laget eller kjørt i denne jobben.

Den samlede kontrollen ble kjørt både før og etter endringen:

```sh
python3 CellProtocolDocuments/Tools/PurposePackages/purpose_dev.py validate CellProtocolDocuments/Deliverables/PDD_utviklerbenk-oppgavegraf_2026-09-10
```

**Exit 1 begge ganger, identisk utdata.** Fem eksisterende lærdommer viser til den uregistrerte
`purpose://candidate.testflyt-verktoycelle.haven-lenke-begge-veier`:
`lesson.sketch-assumed-a-renderer-it-did-not-have`, `lesson.maxwidthinfinity-also-stretches-height`,
`lesson.wrap-gives-each-item-its-ideal-width`, `lesson.empty-list-keeps-its-slot` og
`lesson.text-field-sends-a-string`. Feilene er ikke rettet som del av dette inntaket. Rapporten
hevder derfor ikke at hele PDD-validatoren er grønn; den nye registreringen tilfører ingen feil.
