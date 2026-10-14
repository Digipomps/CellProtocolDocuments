# images/ — referansebilder for G1-GUI (PDD_palazzo-husk-det-jeg-sa)

Alle bilder er 390×844 @2x, rendret **fra skeleton-JSON i `skeleton/`** av en minimal HTML-renderer
(`render.html`, samme mappe i leveransen) med Palazzo-temaets tokens (oliven #556b3f, offwhite #f8f5f2,
kaldt kort #e6eaf0/marine #213963, terracotta #832c03). Fonter: Playfair Display/Georgia for Noe Display,
system-sans for Futura — fontene er ikke identiske med Porthole-temaet.

**Dette er mockups (skill-preferanse 2), ikke Porthole-preview (preferanse 1).** Grunn: PalazzoScaffold har
ingen Porthole-vert (Public/ inneholder bare README), og bridgehead er av som standard; en ekte preview krever at
Codex kjører PalazzoScaffold + Porthole lokalt. Det gjøres i P5 (`test.gui.parity`), ikke før G1-GUI.

| Bilde | Skeleton | Tilstand |
|---|---|---|
| gjest-treffkort-fylt-v1.png | gjest-treffkort.json | ett treff i `entity.match.pending` |
| gjest-treffkort-tom-v1.png | (ingen — seksjonen skjules) | ingen treff; flaten er identisk med i dag |
| gjest-treffkort-feil-v1.png | gjest-treffkort-feil.json | signal utløpt før svar (`entity.match.expired`) |
| gjest-samtykke-to-grants-v1.png | gjest-samtykke-to-grants.json | modal/sheet med innsyn + handling |
| gjest-delt-v1.png | gjest-delt.json | én utstedt pakke, «Trekk tilbake» |
| hus-tagger-v1.png | hus-tagger.json | én ny rett med foreslåtte tagger |
| kelner-husker-v1.png | kelner-husker.json | «Husker»-seksjon i staff-konsollen |

## Hva dagens skeleton IKKE kan rendre (og hva mockupen derfor viser annerledes)

1. **Chips/tagg-piller** finnes ikke — tagger vises som kommaseparert tekst i et TextField.
2. **Betinget rad-visning** (samme List, ulik rad for pending/expired) finnes ikke — cellen leverer to lister
   (`match.pending`, `match.expired`), hver med egen List. Bildet «feil» viser expired-listen.
3. **Knappefarger** (primær/sekundær/fare) er ikke skeleton — de er `styleClasses`-metadata som temaet kan
   plukke opp; uten tema er alle knapper like.
4. **Venstre kantstripe på kortet** og dobbeltlinje under seksjonstittel er tema-CSS (pz-*), ikke skeleton.
5. **Sheet-presentasjon fra bunnen** er `SkeletonPresentation.mobileFallback(kind: .sheet)` — finnes i
   konsentfabrikken i dag, men rendering av *to* knapperader i én modal er ikke verifisert.

## Må verifiseres i Porthole før P5 (står også i hver JSON under `_verify_in_porthole`)

- `Button` inne i `List`-rad med payload som bærer radens id. Fallback: `selectionMode: single` +
  `selectionActionKeypath` + `selectionPayloadMode: item_id`.
- `TextField` i rad med `targetKeypath` utenfor raden (hus-tagger): trolig må godkjenn-payloaden bære teksten.
- `$matchID`/`$id` i payload er fabrikk-substitusjon ved bygging (som `requestID` i dag), ikke runtime.
