# Trådadministrasjon og egen kontekst — vurdering

2026-11-17, Losen i skyen. Svar på Kjetils spørsmål samme dag: hvor ofte skal en tråd pensjoneres, og hva trenger vi for å holde konteksten selv, uten å brenne tokens og uten å henge på én leverandør.

Grunnlaget er denne trådens egen historie og det som ligger i repoene. Ingen tokentall er målt; der jeg anslår, står det.

## Kort svar

1. **Pensjoner etter gjøremål, ikke etter kalender.** Én tråd per PDD eller gjøremål. Tråden avsluttes når G3 er gitt eller PR-en er merget.
2. **Sett et tak i tillegg:** tre arbeidsdager, eller første gang konteksten blir komprimert, det som kommer først. Da skrives en overlevering og en ny tråd tar over.
3. **Nytt tema er alltid ny tråd.** Hver dag er for ofte: en CI-runde tar en time, og en PDD går gjennom tre porter med venting på deg.
4. **Konteksten skal bo i repoet og i entiteten din, ikke i tråden.** Tråden er en arbeidsflate som kan kastes.

## Det denne tråden viser

| Observasjon | Kilde |
|---|---|
| Tråden startet 2026-10-09 med formålstreet, fikk AI-hjelperen samme dag, og modellvalg 2026-11-17. Tre gjøremål i én tråd. | trådens historie |
| Konteksten er komprimert minst én gang. Etter det måtte testfilen og cellen leses på nytt før CI-feilene kunne rettes. | sammendraget i økten |
| Det som overlevde uten tap var det som sto i filer: `STATUS.md` med dine ord ordrett, `PLAN.md`, minnefilen om CI-fellene. | `Deliverables/PDD_workbench-ai-helper_2026-10-09/STATUS.md` |
| Det som gikk tapt eller måtte gjenoppdages var det som bare sto i samtalen: hvorfor et valg ble tatt underveis, og hva som var lest. | inferert |
| Hver vekking laster hele verktøy- og skill-listen på nytt. I en lang tråd er det mye som betales for hver gang. | inferert, ikke målt |

## Regler jeg foreslår

| Når | Hva skjer |
|---|---|
| Nytt gjøremål | Ny tråd. Den starter fra oppgavemappen, ikke fra en gammel samtale. |
| G3 gitt eller PR merget | Tråden lukkes. Lærdommer føres (P6). |
| Tre arbeidsdager, eller første komprimering | Overlevering skrives, ny tråd tar over samme oppgavemappe. |
| Tråden venter på deg i mer enn en uke | Overlevering skrives, tråden lukkes. Svaret ditt starter en ny. |
| Vakt på en PR (CI, review) | Kan leve lenger, men gjør ikke annet arbeid. |

## Det vi trenger for å holde konteksten selv

Mye finnes. Det som mangler er de tre siste radene.

| Funksjon | Finnes? | Hva det er |
|---|---|---|
| Oppgavemappe som sannhet | ja | `FORMAALSSPEC.md`, `STATUS.md`, `PLAN.md` per PDD. Porter med dine ord ordrett. |
| Lærdomsregister og læringsledger | ja | `Book/haven_lessons_register_v0.json`, `haven_learn.py`. |
| Arbeidselementer med status | ja | `WorkItem` i Developer Workbench. |
| **Overlevering** | nei | En fast fil, `OVERLEVERING.md`, i oppgavemappen: hvor formålet står, beslutninger med sitat, åpne spørsmål, neste steg, og pekere (filer, commits, PR-er). Skrives av tråden som går av, og kontrolleres mot `STATUS.md` av et skript. |
| **Startpakke** | nei | Et verktøy som setter sammen det en ny tråd trenger, med et tak (forslag: 4 000 tokens): formålene, portene, siste overlevering, lærdommene `lookup` gir. Resten hentes ved behov fra docs-RAG. Ren tekst, så den kan gis til hvilken som helst modell. |
| **Tråd som celle** | nei | Et arbeidselement i Workbench for hver tråd: hvilken oppgavemappe, hvilken modell, startet, sist aktiv, tokenbruk fra usage-meteret, og knappen «Pensjoner» som krever en overlevering. Da ser du alle tråder ett sted, uansett leverandør. |

## Mindre tokens

- Startpakken erstatter «les deg opp i repoet». Det er den største enkeltposten jeg ser, men den er ikke målt.
- Søk og lesing gjøres av en billig modell som bare leverer konklusjonen. «Mine modeller» gjør det mulig å velge.
- Måling først: læringsloggen i denne PDD-en og usage-meteret gir tokens per gjøremål. Uten tallene er taket på tre dager et skjønn.

## Mindre avhengig av én leverandør

- Alt som må overleve ligger som markdown og JSON i git og i entiteten din. Minnet i Claude-prosjektet er en kopi, ikke en kilde.
- Startpakken og overleveringen er ren tekst og kan gis til Codex, en lokal modell eller en annen leverandør.
- Skills ligger i repoet og synkes ut. Det gjør de alt.
- Det som fortsatt binder: selve trådflaten, vekking på PR-hendelser og verktøykoblingene. Det er grunnen til «tråd som celle».

## Forslag til videre arbeid

Overlevering og startpakke hører ikke hjemme i modellvalg-PDD-en. Jeg foreslår en egen, liten PDD («trådadministrasjon»), og at regelen «nytt gjøremål er ny tråd» gjelder fra nå. Denne tråden fullfører modellvalg og lukkes da.
