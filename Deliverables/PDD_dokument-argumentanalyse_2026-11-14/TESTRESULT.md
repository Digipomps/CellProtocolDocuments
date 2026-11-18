# TESTRESULT – dokument- og argumentanalyse

Faktiske kjøringer. Ingenting her er meldt levert før bygget det gjelder er grønt.

## #graf (WP1, WP2)

- **CellBase `ArgumentMapVisualizationTests`**: 6/6 grønne, 2026-11-18, Docker `swift:6.1-noble`, rigg som avhenger av CellProtocol-grenen `claude/argumentmap-visualization` (b133369) gjennom produktet CellBase. Felles layoutvektorer: `Tests/CellBaseTests/Fixtures/ArgumentMapLayoutVectors.v1.json` (mobilforbud, syklus, uten kanter, hengende/selv-kanter fjernes, barysenter-rekkefølge).
- **Web `playwright/argumentmap-visualization.spec.js`**: 4/4 grønne, 2026-11-18, Chromium, CellScaffold-grenen `claude/tekstanalyse` (6a6acba). Samme vektorfil som CellBase, så web og Swift plasserer hver påstand i samme rad og posisjon.
- **CellApple-renderer (WP3)**: skrevet, ikke bygget. Venter på Mac-kjøring.

## #paritet (WP4, T-PARITET, T-SITAT, T-KILDE)

- **`TextReliabilityAnalyzerParityTests`**: 5/5 grønne, 2026-11-18, Docker `swift:6.1-noble`. Fire fixtures (markdown_struktur, mobilforbud, add2entity_capture, project_description) gir sortert JSON lik Python-verktøyet for seksjoner, påstander, kildereferanser, retorikk og argument_map.
- **Rødsjekk**: ett felt endret i en golden-fil gjorde testen rød som forventet; filen er satt tilbake.
- Ikke portert (bevisst): klynger, matrise, graf, produktivitet og pålitelighetsdimensjoner. Rommet bruker argumentkartet i stedet for den gamle grafen.

## #inntak, #samarbeid, #auth, #eksport (WP5, WP7)

- **`TextAnalysisRoomCellTests`**: 13/13 grønne, 2026-11-18, Docker `swift:6.1-noble`, rigg `/home/user/room-rig` (CellScaffold-kildene symlenket, CellBase fra CellProtocol-grenen). Tilgang er ekte: `debugValidateAccessForEverything = false`, hver identitet signerer med egen nøkkel.
  - T-INNTAK: innliming og .txt/.md-opplasting (base64 og biter) lagrer tittel, kilde, forfatter-uuid og tid; for stor fil, binærfil, ugyldig UTF-8, PDF og feil MIME-type avvises med grunn.
  - T-SAMARBEID: eier og invitert gjest markerer, kommenterer og chatter; begge ser begges navn og markeringer; Flow `analysis.change` sendes for inntak, markering, kommentar og chat.
  - T-TILGANG: fremmed får ikke kontrakt og leser/skriver ingenting; medlem kan ikke bruke eierens nøkler eller utvide avtalen; tilbakekalt medlem mister rom og chat; gjenopprettet rom beholder tekst, markeringer og medlemskap.
  - T-EKSPORT: alle 18 felt fra `requiredOutputFields` finnes; felt Swift-porten ikke beregner er tomme og navngitt i `audit_log`; Mermaid tegner antatte koblinger stiplet.
- **Rødsjekk**: et medlemsvilkår som alltid svarer ja gjør tre tilgangstester røde. Satt tilbake.
- Ikke testet ennå: `purpose://prompt.unknown` (hører til modellforslagene, WP6).

## #parity (WP8)

- Skjelettet (`skeleton/analyserom-skeleton.v2.js`, eksportert til JSON og bygget inn i `TextAnalysisRoomConfigurationFactory`) dekodes av Swift `SkeletonElement` uten å miste felt. Testen fant to felt Swift ikke har (`title` på fanepanel, `fontFamily`); de er fjernet.
- Hver handling skjelettet sender er en medlemsnøkkel i rommet, og hver `analyse.state.*`-sti det leser finnes i tilstanden.
- Bilder: `images/analyserom-*-v2.png`, rendret med `skeleton/render-v2.js` og ekte web-renderer fra tilstander rommet selv laget (`skeleton/states-v2/`). Bildene avslørte at et `label`-felt i påstandsradene overstyrte knappetekstene; feltet er fjernet og testen sjekker det nå.
- Åpent: invitasjon fra flaten (eier velger deltakere) finnes ikke ennå. Rommet støtter invitasjonsbevis fra CellBase-chatten, men flaten har ingen knapp for det.
