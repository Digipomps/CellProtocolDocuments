# Akseptanse — uferdig implementeringskandidat

G3: venter. Ingen arbeidspakke er akseptert som ferdig. Godkjent design og implementeringsmandat gjelder fortsatt alle WP0–WP10.

Tall og kildeversjon nedenfor er generert fra `evidence/candidate-manifest.json` og `evidence/first-build.log`. Kodebeskrivelsene bygger på statisk lesing; de er ikke funksjonsbevis. Ingen bruker-/pilotutfall finnes. Påstander om at denne tråden ikke har deployet eller sendt invitasjoner kommer fra trådens handlingshistorikk, ikke fra en separat ekstern audit.

| Pakke | Godkjent forventning | Faktisk nå | Gjenstår før aksept |
|---|---|---|---|
| WP0 | Sporbar, byggbar baseline og kald oppstart | Isolert låst worktree; første bygg stoppet før tester. | Ny bygging, regresjon, faktisk runtime-/vertsversjon og kald oppstart. |
| WP1 | Selvstendige arrangører og kontrollert paraplytilknytning | Kandidatmodell, registry-oppslag, Cell og konfigurasjon for paraply/tilknytning. | Reelle requester-/HTTP-reiser, utkastisolasjon, varig lagring og siste-admin-vernet. |
| WP2 | Kildebundet innsikt, rettelse og frivillig deling | Private/versjonerte bidrag, modell for rettelse, tilbaketrekking og separat kopivalg. | Full kilde/påstand/motargument-reise, GUI for rettelser, eksplisitt publikumspolicy og negative runtime-prøver. |
| WP3 | Forklarbar matching fra virkelige aktører og kapasitet | Ny intention-projeksjon med opt-in, tilbud/behov, tidsvinduer og topersoners reservasjon. | Erstatte eksisterende faste recommendation-kandidater; publiserte arrangementer i matching; kapasitet og samtidige runtime-prøver. |
| WP4 | DiMy-råd med kilde/usikkerhet og aktivt valg | Eksisterende formålsmodell og nødvendige provider-grenser kartlagt. | Koble faktisk rådgiver, use grant, datavei, kostnadsgrense og akseptprøve. Ingen provider kjørt. |
| WP5 | Varig Entity-utvidelse mellom to selvstendige runtime-instanser | Kopitillatelse i lokal modell; eksisterende Bridge-integrasjon kartlagt. | Reell transport, mottaker-eid commit, restart/read-back, tapt svar/idempotens og revokering under venting. |
| WP6 | Avgrenset selskapsrepresentasjon og tilbakekalling | Additive nøkkel-/utløpsfelt, streng leseevaluering og nøkkelbinding ved ny publisher. | Representasjonsvalg, trygg grant/revoke-skriver, legacy-migrering, monoton revisjon og varig/race-sikker revokering. |
| WP7 | Samme konferanseflate på web og faktisk Binding-host | Felles Skeleton-kandidat med seks faner, katalog og route. | Runtime-preview, fungerende handlinger, web/native-paritet i kompakt/bredt og lys/mørk; ingen nye skjermbilder tatt. |
| WP8 | Gjensidig godkjent møte og kontrollert opptak | Modell for plan/review-versjoner, to godkjenninger, stopp/revokering og syntetisk capture. | Native adapter, to fysiske enheter, fersk autoritet etter await, kontakt-lease og bakgrunnssletting. Ingen mikrofon eksponert. |
| WP9 | Swarm med semantiske forventet/faktisk-resultater | Eksisterende Swarm/admin kartlagt; syntetisk pilot-fixture spesifisert. | Domeneadapter, faktisk run, receipts/assertions, isolert namespace og dokumentert opprydding. |
| WP10 | Kontrollert pilot med observerte menneskelige utfall | Pilot-runbook og syntetisk fixture skrevet. | Tekniske inngangskrav, navngitte ansvarlige, rekruttering og faktisk gjennomføring. Ingen invitasjoner sendt. |

## Bevis og grenser

- Baseline: `e5c3434510884275cae4a732935ab4b55cf7fad9`; gren `codex/oiw-conference-20261005`. Kandidaten er ikke committet.
- 21 nye testmetoder er skrevet; 0 kjørt. Første bygg endte med status 1 før teststart. Den konkrete namespace-feilen er rettet i kildekoden; rettelsen er ikke bygd på nytt.
- `TESTRESULT.md` er den detaljerte kjørestatusen. `evidence/candidate-manifest.json` identifiserer den nyere, utestede kildekandidaten.
- Godkjent HTML: `../Conference_OIW_2026-10-02/design/oiw-felles-forstaelse.html`. Ingen faktisk runtime-screenshot finnes for sammenligning, og GUI-paritet er ikke påvist.
- Rådgiverrapportene i `evidence/oiw-*-20261005.md` beskriver kildefunn og integrasjonsgrenser. Rettelser etter disse rapportene er ikke selvstendig funksjonsverifisert.

Dokumentene sendes til en avgrenset uavhengig beviskontroll. Resultatet legges i `evidence/document-review.md`; eventuelle etterfølgende endringer må identifiseres separat.
