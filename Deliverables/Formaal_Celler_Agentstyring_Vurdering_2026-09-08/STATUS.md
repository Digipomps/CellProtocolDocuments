# STATUS — Formål og Celler som agentstyring (vurdering)

Mappe: `CellProtocolDocuments/Deliverables/Formaal_Celler_Agentstyring_Vurdering_2026-09-08/`

## Logg

- 2026-09-08 07:1x: Formålet skrevet ned først (BRIEF §1, VURDERING §0). Faktagrunnlag hentet fra repoet: Book 04/09/13/23, A1/A4-kontrakten, `AIGatewayPurposePolicy.swift`, `AIGatewayCell.swift` (tool-policy), `GoalDefinition.swift`, PDD rådgiverpanel, PDD arbeidskø, HAVEN-Deploy FORMAAL, HavenAgentD README.
- 2026-09-08 07:32: Astra startet via `codex-local` (MCP), `gpt-6-astra`, `workspace-write`, cwd = denne mappen, reasoning high. Broen timet ut etter 60 s som ventet; Codex fortsatte og skrev Q1 til `ASTRA_SVAR.md` 07:35. Deretter ingen skriving på 15+ min.
- 2026-09-08 07:50: Samme oppdrag lagt i `_losen-queue` som sikring (id `astra-formaal-agentstyring-20260908-0752`, svar til `ASTRA_SVAR_KO.md`, med sjekk mot dobbeltarbeid). Runneren tok jobben 07:50:57.

## Hva som virket

- `codex-local` MCP aksepterer nå `gpt-6-astra` (trivielt kall svarte «klar» på < 60 s). Blokkeringen fra 04.09 (`Codex_blokkert_20260904.md`) er borte.
- `workspace-write` via MCP ble **ikke** avvist av klassifisereren for denne (rene analyse-) jobben, i motsetning til lærdom 07.09 for skrivende implementasjonsjobber. Skillet ser ut til å gå på hva prompten ber om, ikke på sandbox-flagget alene.
- Codex-prosessen overlever bro-timeouten i minst to minutter (Q1 ble skrevet etter timeouten).
- `_losen-queue` er i drift og tar jobber innen ett minutt; jobbformatet (tre linjer + prompt) fungerer fra Cowork-VM-en uten at Kjetil gjør noe.

## Hva som ikke virket / er usikkert

- Etter Q1 stoppet skrivingen i MCP-økten. Uvisst om økten ble avbrutt da klienten kansellerte (MCP-semantikk), eller om Codex bare skriver én gang til slutt. **Regel:** ikke stol på MCP-ruten for jobber > 1 min; bruk køen. MCP-ruten er fin for trivielle kall og for å sjekke at modellen svarer.
- Astra fikk ikke nettverifisert septemberfakta fra Codex-siden (nettoppslag avvist av godkjenningskontroll; DNS-feil). Nåtidsfakta må hentes av Losen og legges i briefen som fakta med kilde, ikke som oppgave til Codex.
- Dobbeltkjøring: to Astra-instanser på samme oppdrag koster dobbelt. Sjekken «hvis ASTRA_SVAR.md slutter med FERDIG, ikke gjør noe» i kø-prompten er det som gjør det trygt.

## Logg (forts.)

- 2026-09-08 08:03: Kø-jobben ferdig etter 13 min: `ASTRA_SVAR_KO.md`, 3 900 ord, Q1–Q9, med fil:linje-belegg. MCP-økten skrev aldri mer enn Q1 (`ASTRA_SVAR.md`, 440 ord) — regnes som avbrutt.
- 2026-09-08 08:05–08:13: Runde 2 via køen (`astra-formaal-runde2-20260908-0808`): `RUNDE2_LOSEN.md` (fem motsvar M1–M5) → `ASTRA_SVAR_RUNDE2.md` (1 600 ord). Astra endret standpunkt på M2 (A4 låser formålet), ga navn og forgjengere til M1 (ressurseierstyrt autorisasjon; UMA 2.0, Solid WAC), valgte correspondence-piloten i M5 med snu-kriterium.
- 2026-09-08 08:2x: `VURDERING.md` ferdig (ca. 4 700 ord), målt mot F1–F6 i §0.

## Lærdommer (til gjenbruk)

1. **Astra-diskusjon fra Cowork: bruk `_losen-queue`, ikke `codex-local`, for alt som tar > 1 min.** MCP-ruten svarer på trivielle kall og beviser at modellen er tilgjengelig; en 60-sekunders-timeout på broen ser ut til å avbryte økten (Q1 ble skrevet, så stopp). Køen tok jobben på < 1 min og leverte hele svaret. Kostnad: én dobbeltkjøring (~440 ord), unngått verre av «hvis ferdig-markør finnes, gjør ingenting»-sjekken i kø-prompten.
2. **Runde-basert diskusjon virker med filer som tråd:** BRIEF → svar → motsvar-fil → svar. Hver runde er en ny kø-jobb som leser forrige filer. Ingen behov for `threadId`.
3. **Be Astra om `[belagt: fil:linje]`.** Det ga fire korreksjoner av briefen (usignert receipt, verdipredikater, correspondence-ja, `ownerConfirmed` som default) som jeg kunne verifisere i koden på minutter. Uten linjenumre hadde det tatt lengre og vært lettere å avfeie.
4. **Nåtidsfakta må Losen hente og legge i briefen med kilde.** Codex' nettoppslag ble avvist av godkjenningskontroll; Astra markerte dem `[usikker]` og brukte dem ikke som evidens. Det var riktig av Astra — og betyr at briefen bør skille «mekanisme» fra «tall/dato».
5. **Skriv egen vurdering parallelt, før Astras svar.** Det gjorde at diskusjonen ble en diskusjon (fem reelle uenigheter), ikke en gjenfortelling.
6. **Verifiser Astras funn i koden før de tas inn.** Alle fire ble bekreftet; tid: ~5 min. Regelen står uansett.
