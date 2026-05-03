# Conference Design Handoff · 2026-04-30

## Purpose

Samle ferske skjermdumper av konferanseflatene i `Binding` og
`CellScaffold`, slik at Claude eller en annen modell kan foreslaa et bedre og
mer helhetlig designsystem for konferanseproduktet.

Dette dokumentet beskriver:

- hva som faktisk ble capturet
- hvor artefaktene ligger
- hva som fortsatt er auth-gated eller ikke sendt videre
- hvor neste modellrespons skal dokumenteres

## Artifact Pack

Den samlede handoff-pakken ligger her:

- `/tmp/conference-design-handoff-20260430`

Viktigste filer:

- `/tmp/conference-design-handoff-20260430/README.md`
- `/tmp/conference-design-handoff-20260430/CLAUDE_PROMPT.md`
- `/tmp/conference-design-handoff-20260430/CLAUDE_RESPONSE.md`

## Binding Captures

Kilde:

- `/tmp/binding-conference-smoke-20260430`

Generert via:

- `Binding/Scripts/run_conference_demo_smoke.sh`

Captured surfaces:

1. `01-launcher.png`
2. `02-participant-portal.png`
3. `03-participant-portal-chat-ready.png`
4. `04-chat-workbench.png`
5. `05-public-surface.png`
6. `06-control-tower.png`
7. `07-ai-assistant.png`
8. `08-identity-link.png`

Kjørselsrapport:

- `/tmp/binding-conference-smoke-20260430/report.md`

## CellScaffold Captures

Kilde:

- `/tmp/cellscaffold-conference-captures-20260430`

Lokal server ble startet mot:

- `http://127.0.0.1:8081`

### Route viewport captures

Disse viser web-rutene slik de presenterer konferansefamilien:

1. `viewport-routes/01-conference-public.png`
2. `viewport-routes/02-conference-participant-preview.png`
3. `viewport-routes/03-conference-ai-preview.png`
4. `viewport-routes/04-conference-public-profile-preview.png`
5. `viewport-routes/05-conference-public-profile-editor-preview.png`
6. `viewport-routes/06-conference-admin-preview.png`

### Surface viewport captures

Disse er scrollt ned til selve flaten og er de viktigste designreferansene:

1. `surface-viewports/01-conference-public-surface.png`
2. `surface-viewports/02-conference-participant-surface.png`
3. `surface-viewports/03-conference-ai-surface.png`
4. `surface-viewports/04-conference-public-profile-surface.png`
5. `surface-viewports/05-conference-public-profile-editor-surface.png`
6. `surface-viewports/06-conference-admin-surface.png`

## Skeleton Clarification

Det som vises i toppen av web-rutene er ikke alltid den kanoniske
skeleton-flaten alene. `CellScaffold` legger en preview-/route-kappe over den
egentlige flaten.

Praktisk leseregel:

- `viewport-routes/` = route-wrapper + preview shell
- `surface-viewports/` = den delen som faktisk bør leses som selve
  skeleton-uttrykket

Hvis målet er å vurdere om "all GUI skal uttrykkes i skeleton", er det
`surface-viewports/` som skal vektes tyngst.

## Observed Gaps

- `CellScaffold` sponsor follow-up-ruten er fortsatt auth-gated.
- Legacy `conference-mvp`-ruten er fortsatt admin-gated.
- `CellScaffold` Porthole-deeplinks landet på innlogging uten en autentisert
  web-økt.
- For å unngaa aa opprette eller sende en ny browser-brukerøkt uten eksplisitt
  action-time bekreftelse ble auth-gated webflater ikke tvangskjørt videre i
  denne pakken.

## Claude Delivery Status

Claude desktop ble faktisk brukt i denne kjøringen.

Fordi Claude desktop ikke kunne lese lokale `/tmp`- eller repo-stier direkte,
ble pakken oversatt til tre faktiske kontaktark-bilder og limt inn i chatten
sammen med prompten:

- `binding-sheet.png`
- `cellscaffold-surface-sheet.png`
- `cellscaffold-route-sheet.png`

Det ble også sendt en eksplisitt presisering om at:

- `surface-viewports/` er kanonisk skeleton-GUI
- `route-viewports/` bare viser wrapper-/preview-kontekst

Claude-responsen ble deretter hentet ut automatisk fra lokal Claude-cache og
lagret som:

- `/tmp/conference-design-handoff-20260430/CLAUDE_RESPONSE.md`
- `Deliverables/Conference_Claude_Redesign_Direction_2026-04-30.md`

## Recommended Next Step

Bruk:

- `/tmp/conference-design-handoff-20260430/CLAUDE_PROMPT.md`
- `/tmp/conference-design-handoff-20260430/CLAUDE_RESPONSE.md`

sammen med skjermdumpene i samme mappe hvis pakken skal sammenlignes mot eller
mates inn i en annen modell.

## Documentation Follow-up

Claude-svaret er nå dokumentert i:

- `Deliverables/Conference_Design_Response_2026-04-30.md`

Den oppfølgingsfilen inneholder:

- valgt modell og faktisk sendeform
- hvilke bilder som ble sendt
- modellens hovedforslag
- hvilke forslag som ser sterke ut for HAVEN
- hvilke forslag som må valideres mot arkitekturen
- anbefalt implementeringsrekkefølge i `Binding`, `CellScaffold`, og eventuelt
  `CellProtocol`
