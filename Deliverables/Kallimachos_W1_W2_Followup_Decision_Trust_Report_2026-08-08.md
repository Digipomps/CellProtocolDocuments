# Kallimachos W1/W2 — oppfølgings-, beslutnings- og tillitsrapport

- Dato: 2026-08-08
- Beslutningseier: Kjetil
- Omfang: svarene gitt etter W1/W2-leveransen
- Status: implementert og fokusert verifisert; eksakte commit-SHA-er rapporteres ved overlevering

## Formål

| Formål | Begrunnelse |
| --- | --- |
| `purpose://knowledge` | Kallimachos skal være en delt, kildebevisst bibliotekarimplementasjon med deterministisk trinn 0–1. |
| `purpose://access.audit.privacy` | Requesteren skal kunne eksportere og slette egen rå spørre- og svarhistorikk uten tilgang til andres historikk. |
| `purpose://grounding.local-model-assisted-decomposition` | De lokalt testede Qwen3/Gemma-rutene skal ha stabile AgentD-identifikatorer uten å gjøre modellen til policyautoritet. |

## Goals

| Goal | Målbar terminaltilstand | Status | Evidens |
| --- | --- | --- | --- |
| G1 | `CommonsLibrarianCell` eies av ScaffoldKit; `relation_id` er obligatorisk for katalogspørring; relasjonsavgrenset eksport og bekreftet sletting har komplette Explore-kontrakter og fokuserte tester. | complete | `swift test --disable-sandbox --skip-update --filter CommonsLibrarianCellTests`: 11 tester, 0 feil. |
| G2 | HAVENAgentD kjenner stabile Qwen3-8B- og Gemma 4 E4B-profiler; profilvalg, provider-ID, loopback-port, lokal path-override og unikhet testes. | complete | `swift test --package-path HavenAgentD --disable-sandbox --skip-update --filter AgentCellsTests`: 23 tester i 3 suites, 0 feil. |
| G3 | Manifestbeslutningen og de to kanoniske Kallimachos-dokumentene er committet sammen med denne rapporten; ingen uavklarte spørsmål skjules. | complete | Tre Deliverables inngår i dokumentasjonscommitten som inneholder denne rapporten; eksakt SHA rapporteres ved overlevering. |

## Bindende beslutninger fra Kjetil

| ID | Beslutning | Implementert konsekvens |
| --- | --- | --- |
| D1 | Include/exclude-manifestet godkjennes, og panelartefakter forblir ekskludert. | `reviewStatus` settes til `approved`; eksisterende panel-/handoff-eksklusjoner beholdes; `reviewQuestions` tømmes. |
| D2 | Wire lokale modeller nå. | To kjente AgentD-profiler legges til med stabile profil- og provider-ID-er; begge forblir merket eksperimentelle for produktbruk. |
| D3 | Flytt `CommonsLibrarianCell` til ScaffoldKit. | Swift-kode og versjonerte ressurser flyttes til ScaffoldKit-target; App beholder bare resolver-registreringen. |
| D4 | Eksport og sletting av spørrehistorikk skal implementeres. | `librarian.audit.export` og `librarian.audit.delete` legges til som requester- og relasjonsavgrensede SET-handlinger. |
| D5 | `relation_id` er obligatorisk. | Explore-skjema og runtime avviser katalogspørring uten ikke-tom `relation_id`; avvist spørring lagres ikke. |

## Claim graph summary

### C1 — delt implementasjon

- Claim: `CommonsLibrarianCell` bør eies av ScaffoldKit.
- Type: project capability / normative, assertive.
- Premisser: App er allerede avhengig av ScaffoldKit; resolverregistrering trenger bare en offentlig celletype og kontrakt; ressursene kan eies av ScaffoldKit-bundlen.
- Counterargument: flyttingen øker ScaffoldKit-targetens omfang og gjør admin-plane-eksporten avhengig av bibliotekarressursene.
- Steelman: en egen mindre pakke kunne gitt skarpere avhengighetsgrense enn ScaffoldKit.
- Adjudication: beslutningen er bindende. Begge Package.swift-manifestene får eksplisitte ressurser slik at ingen host får en skjult Bundle-feil.
- Støtter: G1.

### C2 — relasjonsavgrenset personvernhandling

- Claim: eksport og sletting må kreve eksplisitt relasjon og aldri bruke requesterens identitet som stille standard.
- Type: privacy/design, assertive.
- Premisser: historikken inneholder rå spørsmål; navnehistorikk og auditposter er allerede knyttet til `relationID`; D5 gjør relasjon eksplisitt.
- Counterargument: en «eksporter alt»-handling er enklere for dataportabilitet.
- Steelman: komplett requester-eksport kan være nødvendig senere, men bør være en separat, tydelig reviewet bulkhandling.
- Adjudication: v1 eksporterer/sletter én eksplisitt relasjon. Sletting krever i tillegg `confirm: true`, regenererer gap-tellere fra gjenværende poster og returnerer kvittering.
- Støtter: G1 og `purpose://access.audit.privacy`.

### C3 — stabil rute, eksperimentell modell

- Claim: stabil AgentD-identitet kan wires uten å hevde at modellen er stabil produktpolicy.
- Type: architecture/project capability, moderated.
- Premisser: W2 kjørte begge lokale runtimes, men ikke AgentD; AgentD støtter allerede profiler, loopback-gate og miljøoverstyring; Gemma-serveren krever maskinlokal modellsti.
- Counterargument: en profil som trenger miljøoverstyring er ikke fullstendig nullkonfigurasjon.
- Steelman: AgentD kunne senere eie en installasjons-/modellsti-resolver, men det er utenfor denne endringen.
- Adjudication: profil/provider-ID og porter er stabile; `isExperimental` beholdes; Gemma-sti leveres gjennom eksisterende miljøvariabel og committes ikke.
- Støtter: G2.

## Brief audit

### Verifiserte fakta

- W1-committen registrerer `CommonsLibrarianCell` i to resolver-oppsett i `Sources/App/configure.swift`.
- ScaffoldKit er et target og produkt i samme CellScaffold-pakke; App er direkte avhengig av targetet.
- Historikk lagres i `CommonsLibrarianPersistedState.auditRecordsByRequester`, avgrenset med requester-UUID og maksimalt 500 poster per requester.
- Eksisterende AgentD-kode avviser ikke-loopback backend som standard og tillater eksplisitt miljøoverstyring av profil, provider, URL og modell.
- W2-rapporten dokumenterer direkte lokale runtimes: Qwen3 53/72 og Gemma 56/72; rapporten sier eksplisitt at AgentD ikke ble brukt.

### Bindende regler

- D1–D5 over er beslutninger fra Kjetil, ikke utledede fakta.
- Ingen modell skal eie kildevalg, gap-policy, sletting, autorisasjon eller annen deterministisk policy.
- Ingen modellsti, modellvekt, venv, credential eller generert korpusindeks committes.

### Vurderinger og begrensninger

- Requester-avgrensningen er applikasjonslogikk i tillegg til resolverens Agreement-sjekk; testen bruker en annen requester under tillatt direkte testtilgang for å bevise at lagringsnøkkelen ikke lekker.
- «Stabil profil» betyr stabil ruteidentitet, ikke produksjonsgodkjent modellkvalitet.
- Sletting dekker rå auditposter, avledede gap-tellere og relasjonens navnenarrasjonstilstand. Den skriver ikke en ekstern eller Entity-basert kvittering.

## Personal-data trust package

### Data og formål

- Datakategori: rå katalogspørsmål, relasjons-ID, deterministiske svar, citations og avledede gap-tellere.
- Formål: etterprøvbar katalogdialog og requesterens egen eksport/sletting.
- Requester/decision basis: Kjetil har godkjent funksjonen; hver konkret sletting krever fortsatt callerens uttrykkelige `confirm: true`.

### Dataflyt

```text
requester -> resolver/Agreement -> CommonsLibrarianCell
          -> requester UUID + relation_id -> persistent Cell state
          -> export response tilbake til samme autoriserte requester
          -> delete muterer bare samme requester + relation og gir receipt
```

- Runtime gjør ingen modell- eller nettverkskall i trinn 0–1.
- Export returnerer data i Cell-responsen; den skriver ingen fil og gjør ingen ekstern disclosure.
- Flow-hendelsen for katalogsvar inneholder ikke rå query- eller answer-tekst.

### Lagring og retention

- Lagringssted: persistent Cell state, ikke Entity og ikke ekstern tjeneste.
- Grense: 500 auditposter og 200 gap-emner per requester.
- TTL: ingen tidsbasert TTL er implementert.
- Eksport: én requester + én eksplisitt relasjon; rå spørsmål og registrerte svar følger med.
- Sletting: én requester + én eksplisitt relasjon; gap-tellere bygges på nytt fra gjenværende poster.

### Autorisasjon og isolasjon

- Leseflater krever `r---`; handlinger krever `-w--`.
- Alle handlere kaller `validateAccess` før tilstand leses eller muteres.
- Ingen eksport- eller slettepayload kan velge en annen requester-ID.
- En annen requester med samme `relation_id` får null poster og kan ikke slette eierens poster.

### Kvittering og disclosure

- Sletting returnerer `haven.commons-librarian-deletion-receipt.v1` med relasjon, antall slettede/gjenværende poster, narrasjonstilstand og SHA-256.
- `external_disclosure=false` inngår i eksportmetadata og slettekvittering.
- Ingen ekstern recipient, jurisdiksjon, DPA eller provider er involvert i runtime-operasjonene.

## Decision log

| Dato | Beslutning/handling | Eier | Resultat |
| --- | --- | --- | --- |
| 2026-08-05 | W1/W2-handoff og opprinnelige constraints. | Kjetil | W1/W2 levert i separate commits. |
| 2026-08-08 | D1–D5 bekreftet. | Kjetil | Oppfølgingsimplementasjon startet i tre rene worktrees. |
| 2026-08-08 | Personvernminimum for destructive action. | Implementasjon under Kjetils D4/D5 | Relasjonsscope + `confirm: true` + deterministisk receipt. |
| 2026-08-08 | Fokusert CellScaffold-verifikasjon. | Codex | 11/11 `CommonsLibrarianCellTests` bestått. |
| 2026-08-08 | Fokusert AgentD-verifikasjon. | Codex | 23/23 `AgentCellsTests` bestått; ingen modellserver eller modellvekter startet. |

## Åpne spørsmål til Kjetil

1. Qwen3-profilen bruker foreløpig port `8083` for å unngå eksisterende `8080` (Qwen-test), `8081` (staging-app), `8082` (Borealis) og `8094` (Gemma). Skal `8083` være den kanoniske standardporten?
2. Skal en senere, separat bulkhandling kunne eksportere alle relasjoner for requesteren, eller skal eksport forbli én relasjon per eksplisitt kall?
3. Skal audit-historikken få en tidsbasert TTL i tillegg til 500-postgrensen? Ingen TTL er antatt eller implementert her.
4. Skal de to Kallimachos Deliverables senere få egne poster i `Book/book_catalog.json`, eller skal de forbli søkbare Deliverables uten Book-identitet?
5. Skal live AgentD-smoke mot kjørende Qwen/Gemma-servere tas som et eget spor? Denne endringen verifiserer profilkontrakt og konfigurasjon, men starter ikke modellservere og kjører ikke modellvekter.

Disse spørsmålene blokkerer ikke D1–D5. De er avgrensede viderevalg og er ikke behandlet som stille prosjektfakta.
