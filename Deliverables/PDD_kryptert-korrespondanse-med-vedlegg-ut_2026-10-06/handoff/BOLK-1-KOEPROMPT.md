# Bolk 1 — forslag til køprompt for Codex-jobben (korrespondansen: prøve av innslipp med en avtale signert utenfor cellens prosess)

Skrevet 07.10.2026 av korrespondanse-tråden (Claude-tråden i prosjektet «HavenAgentD») til kø-tråden, som legger Codex-jobber i kø. Teksten under streken kan brukes som promptfil slik den står. Rett det som ikke passer med banepolitikken eller køen akkurat nå. Forslag til jobbfil: tom linje 1 (HAVEN-roten), `workspace-write` på linje 2 (jobben trenger ikke nett: ingen fetch, ingen push), leveransestien under på linje 3, og 240 på linje 4.

Leveransesti: `CellProtocolDocuments/Deliverables/PDD_kryptert-korrespondanse-med-vedlegg-ut_2026-10-06/handoff/BOLK-1-RAPPORT.md`

---

# Korrespondansen: prøve av innslipp med en avtale signert utenfor cellens prosess (bolk 1)

Codex-jobb bestilt av Claude-tråden i prosjektet «HavenAgentD» (korrespondanse-tråden).

## Kjetils ord (07.10.2026, ordrett)

«A ja, B ja, C ja Vegar har en m2 og victoria en intel». Spørsmål C var: «Kan Codex starte første ledd nå, før planen er godkjent? Det er en liten prøve, lokalt: en avtale signert på én maskin slipper inn et medlem i en celle som kjører på en annen. Bestillingen sier at ingenting skal til hovedgrenen. Holder ikke prøven, kommer jeg tilbake til deg før noe annet bygges.»

Samme dag: «Jeg synes det ikke er noe poeng å teste den gamle versjonen. Få ut den nye.»

## Oppdraget

Les `CellProtocolDocuments/Deliverables/PDD_kryptert-korrespondanse-med-vedlegg-ut_2026-10-06/handoff/BOLK-1-OPPDRAG.md` og utfør det. Den fila er hele oppdraget: hva prøven er til, det som er lest i koden, de seks tingene prøven skal svare på, rammene og leveransen. Står noe her i strid med den fila, gjelder fila.

Dette er en prøve og skal være liten. Den skal svare med tester og rå utdata, ikke med resonnement, og den skal ikke anbefale arkitektur.

## Slik gjøres det på denne Macen

- Arbeidstre `_worktrees/cp-korr-innslipp-proeve-20261007`, gren `codex/korr-innslipp-proeve-20261007` fra `origin/main` i CellProtocol slik den er lokalt (`68069b697a22246ffb4d8add5ecc42e3d0d5ba38`, taggen `2026.9.5`). Ingen fetch trengs. Lås arbeidstreet mot prune.
- Ikke rør hovedarbeidstreet i `CellProtocol` (det har andres endringer) eller andre arbeidstrær. Jobben `a35` arbeider i `_worktrees/cp-avvis-foer-readiness-20261007`, på en annen gren i samme repo.
- Bygg og tester kjøres som skriptjobber etter banepolitikken i `_losen-queue/KOORDINERING.md` (kø-trådens innlegg 07.10 kl. 15:09Z): avgrensede kjøringer av den nye testfila som kortjobber, og hele testmengden med `HAVEN-Deploy/_handoff/GRUNNMUR/wp-cellprotocol-grunnmur.sh <gren>`. Et eget skript for den avgrensede kjøringen legges under `HAVEN-Deploy/_handoff/KORR-UT/`, etter mønsteret i `HAVEN-Deploy/_handoff/GRUNNMUR/wp-cp-refusal-focused.sh`. Promptfil først, så jobbfil via `.tmp` og `mv`. Se etter i `done/`, `running/` og innboksen før et jobbnummer brukes.
- Følg regel 1–3 i `_losen-queue/KOORDINERING.md` (diskplass, avgrenset bygg, eget arbeidstre) og punkt 11 i `_losen-queue/LES_MEG.md` (filtaket ved Swift-bygg).
- Ingen push, ingen PR, ingen merge, ingen tag. Commit lokalt på grenen. Forskjellen mot `origin/main` legges i `CellProtocolDocuments/Deliverables/PDD_kryptert-korrespondanse-med-vedlegg-ut_2026-10-06/handoff/BOLK-1-ENDRING.patch`.

## Avslutning

- Rapporten skrives til leveransestien, i formen oppdraget sier. Øverst en tabell: | Steg | Utfall | Bevis (kommando, exit-kode, antall tester) |.
- Skill mellom **kjørt** og **lest i kode**. Skriv «vet ikke» der det er sant.
- Kjør `CellScaffold/scripts/haven_learn.py` for det som er gjenbrukbart, eller `none --reason`.

## Regler

- Bare CellProtocol. Ingen endring i kildekoden i HavenAgentD, CellScaffold eller Binding (læringsregisteret under `CellScaffold/Documentation/Learnings/` er unntatt). Ingen pinnendring, ingen deploy, ingen vert, ingen staging.
- Ingen debug-bypass. Private nøkler bare i testenes egne nøkkellagre. Ingen nøkler, tokener, IP-adresser eller brukerstier i rapport, commit eller patch. Stier relative til repoet.
- Ingen eksisterende test fjernes eller svekkes.
