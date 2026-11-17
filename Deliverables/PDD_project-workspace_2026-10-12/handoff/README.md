# Handoff ved godkjent G2

Avstem HEADs og AgentD-eier med Deploy prosjekt køadministrasjon. Isoler arbeidstrær og bevar andres endringer. P1–P6 i plan.json er oppgavene. Hver leverer diff, måltestlogg, inputmanifest og status. Oppgi nøyaktig leste filer, ikke hele mapper.

CP-retesten er separat godkjent og ligger under HAVEN-Deploy/_handoff/ARBEIDSBENK/G2-W1-RETEST-20261012. Den beviser journalgrensen, ikke prosjektflaten.

Bygg koordineres i inbox-g2. Nye scripts har check/dry-run som standard. Prompt først, .job atomisk sist. Stdout-mottaker skilles fra egne rapportfiler. Følg kapasitet, to-jobbsgrense og engangskvitteringer. Rødt stopper; ingen rerun uten Kjetils ord. Ingen betalt CI før grønn lokal kontroll. Ingen deploy uten separat køeier og eksisterende godkjenninger.

