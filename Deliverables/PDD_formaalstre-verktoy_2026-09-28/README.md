# Formålstrær — visuelt verktøy for formålstrær

Kjetil 2026-09-28: «Når du presenterer formål kan vi lage det som et tre hvor vi ser avlange felter med formålets navn, underformål som barn festet med en linje (gjerne kurver), kanskje tematisk fargevalg, klikk for å se detaljer, kollapsbare barn og mulighet for å se hvor i et høyere scoped formålstre de hører hjemme. La det bli et visuelt verktøy for å redigere formålstrær. Med mulighet til å fjerne, muligens redigere og legge til nye. Husk å ha auto complete med oppslag av formål + fallback til formålsdekomponering av fri tekst og matching med eksisterende.»

Kjetils valg samme dag:
- «Side i Claude nå, HAVEN senere».
- «Oppgavens tre, forslag til Book 23».

## Hvor

- **Siden:** https://claude.ai/artifact/DAXLyDGAwej65jb7fnfVJS. Den er privat for Kjetil til han deler den.
- **Kilden:** `formaalstre.html` i denne mappen. Siden oppdateres fra samme fil.
- **Kapabiliteter:**
  - `db` lagrer trær og forslag;
  - `sample` lar Claude dekomponere fri tekst;
  - `user` viser om du er eier, og bare eieren kan godkjenne forslag.

## Datamodell i sidens database

| Sti | Innhold | Hvem skriver |
|---|---|---|
| `kb/book23` | Kopi av `Book/haven_purpose_knowledge_base_v0.json` i kort form (`ref, parentRef, title, summary, status, outcome, signals, verifier, aliases, interests`), pluss `sourceSHA256` og `syncedAt` | Losen, fra `seed/kb-book23.json` |
| `trees/<id>` | Ett PDD-tre: `title, pdd, source, anchorRef` (hvor treet hører hjemme i Book 23), `rootRef` og `nodes[]` (`ref, parentRef, title, code, outcome, verifier, status, reused`) | Siden, når noen redigerer. Losen når et tre hentes fra en FORMAALSSPEC. |
| `proposals/<id>` | Forslag til Book 23: `kind` (`add`, `edit` eller `remove`), `targetRef, parentRef, node, before, why`, og `status` (`venter`, så `godkjent` eller `avvist`, så `innført`) | Siden. Eieren godkjenner. Losen setter `innført`. |

## Slik henger det sammen med filene (Losen)

1. **Nytt tre fra en PDD.** Parse FORMAALSSPEC §1 slik `seed/tree-palazzo-tolkning.json` ble laget (se loggen), og skriv det med `ArtifactData set trees/<id>`.
2. **Endringer i et tre tilbake til PDD-en.** Les `trees/<id>` med `ArtifactData get`, og oppdater FORMAALSSPEC §1 og revisjonsloggen §7. Det gjøres når Kjetil ber om det eller før en gate. Treet i siden erstatter aldri en godkjent G1 i det stille.
3. **Forslag til Book 23.**
   1. Les `proposals` der `status == "godkjent"`.
   2. Før dem inn i `Book/haven_purpose_knowledge_base_v0.json` med Book 23 §8, fangstprosessen.
   3. Kjør `purpose_dev.py validate`.
   4. Sett `status: "innført"` med `innførtAt`.
   5. Skriv `kb/book23` på nytt fra fila.
   - Book 23 endres aldri fra siden direkte.
4. **Book 23 endret i repoet.** Bygg `seed/kb-book23.json` på nytt og skriv `kb/book23`.

## Slik virker siden

- **Tegning.** Treet tegnes fra venstre mot høyre. Hvert formål er et avlangt felt, og barna er koblet med kurver. Hver gren under roten har sin egen farge, og fargeforklaringen står nede til høyre.
- **Skjule og åpne.** Sirkelen på høyre kant skjuler eller åpner barna og viser hvor mange som er skjult. «Åpne alle» viser alle igjen. Hva som er skjult, huskes i nettleseren.
- **Høyere tre.** «Vis i høyere tre» tegner kjeden i Book 23 fram til `anchorRef` som stiplede felt til venstre for roten. Trykk på et av dem for å åpne Book 23-visningen der.
- **Redigere.** Trykk på et formål for å redigere tittel, kode, status, mål og verifisering. Du kan også legge til underformål eller fjerne formålet med alle barna, med en bekreftelse på siden.
- **Autocomplete.** Søket slår opp i Book 23 og i treet, på tittel, alias, interesser, sammendrag og ref.
  - «Legg til som nytt formål» lager en kandidat.
  - «Dekomponer … med Claude» deler fri tekst i formål med mål og verifisering, og matcher hvert mot eksisterende ref.
  - Refs som ikke finnes i listene, forkastes.
  - Du krysser av hva som skal inn, og om en match skal gjenbrukes.
- **Book 23-visningen.** Den er skrivebeskyttet. Endringer blir forslag, og ventende forslag vises stiplet eller overstrøket.

## Kjent i versjon 1

- **Flytte formål.** Du kan ikke flytte et formål til en annen forelder i treet. I dag fjerner du det og legger det til på nytt.
- **Tester.** Siden har ingen automatiske tester. Den ble sett på én gang med testdata før publisering.
- **Tilbake til PDD-en.** Endringer i treet synkes ikke automatisk tilbake til FORMAALSSPEC. Det gjør Losen, se punkt 2 over.
- **HAVEN-flaten.** Den kommer senere. Denne siden er spesifikasjonen og prototypen for den.
