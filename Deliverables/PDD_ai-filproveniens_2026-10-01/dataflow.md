# Dataflyt — foreslått, ikke implementert

Registrert AgentD-jobb / bounded bygg / deploy-transaksjon
→ tillatt jobbområde + opprettelsesobservasjoner + kontrollinventar
→ lokal append-only metadatakø (eier, vert, sekvens, dekning)
→ autorisert projeksjonsimport (validering, deduplisering, rekkefølge)
→ eksisterende GraphStore (noder + relasjoner + atomisk checkpoint)
→ eierstyrt Workbench-oversikt og bevaringsvurdering
→ eksisterende ryddevakt ved separat godkjent ryddeoppgave.

| Kant | Kontrakt / bevis | Feiloppførsel |
|---|---|---|
| Jobb → hendelse | contract/provenance-event-draft.json | Ingen opphavsattribusjon uten bevis; registrer gap |
| Hendelse → lokal kø | Valider metadata, hold lokal eiergrense, varig kvittering | Full kø gir synlig manglende dekning, ikke falsk suksess |
| Lokal kø → GraphStore | Eksisterende graph.workbench.applyUpdates bak autorisert target | Manglende grant/offline beholder ventende data; ingen udokumentert sidekanal |
| GraphStore → GUI | Ny eksplisitt Explore-kontrakt til P5; preview.* er ikke produkt-API | Feil eier avvises; manglende/friskhet vises |
| Klassifisering → ryddevakt | Kandidat med stier, opphav, avhengigheter og måletid | Klassifisering gir ikke slettemakt |

Nåværende GraphStore-kilde returnerer delvis anvendelse via skippedCount; kvittering krever både validerte counts og readback. Jobbens eksisterende completion-status holdes adskilt fra innsamlingens/synkroniseringens helsetilstand.
