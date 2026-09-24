# Formålsspesifikasjon (FORMAALSSPEC.md) — mal og regler

`python3 Tools/PurposePackages/purpose_dev.py new <slug> --intent "…" --tags … --surfaces …`
lager malen ferdig utfylt med pakker, lærdommer og avledede tester. Dette dokumentet
forklarer hva hver seksjon skal inneholde og hva som gjør den godkjennbar.

Grunnregel: **Kjetil godkjenner formålet (G1) og bildet (G1-GUI) før noen planlegger
eller bygger.** Iterer så mange runder som trengs; hver runde er en rad i §7.

## §0 Intensjon (ordrett) og brief-audit

Kjetils tekst limes inn uendret. Under den: én rad per faktapåstand og per
kapabilitet oppgaven forutsetter, med audit-status `retrieved` (lest fra fil denne
økten, sti oppgitt) / `recalled` / `unavailable` / `contradicted`. Bare `retrieved`
kan bære planen.

## §1 Formålstre

| purposeRef | Tittel | Forelder | Goal (outcome) | Verifier | Status |

- Velg først fra `Book/haven_purpose_knowledge_base_v0.json` og pakkene. Nye noder heter
  `purpose://candidate.<slug>.<navn>` og navngis av Losen — aldri av en modell.
- Goal skal ha observerbart utfall, suksessignaler og en verifier (Book 23-krav). Kan
  ikke suksess observeres, skriv det rett ut i §6 i stedet for å pynte.
- Hvert bladformål har minst én test i §5. Antiformål (`polarity: prohibited`) er lov
  og skrives som «skal ikke …» med egen test.
- Dybde: så grunt som mulig. Tre nivåer holder nesten alltid.

## §2 Avgrensning og avhengigheter

Først «hva dette IKKE er» (3–6 linjer). Så tabellen over kapabiliteter og avhengigheter
oppgaven bygger på, hver med kildefil, hva den ikke dekker, og om den må virke før
testene kan kjøres. Dette er der `lesson.bridge-inferred-architecture-from-one-use`
og `lesson.corr-approval-surfaces-timed-out` skal fanges.

## §3 Forventningskontrakt — «Det du kommer til å se»

| Leveranse | Type | Hvor | Referanse | Godkjent |

Én rad per ting Kjetil faktisk får: bilde, fil, testutdata, kjørende flate. Etter G2
er dette tabellen fremdrift måles mot. For GUI: hver flate × tilstand (tom, fylt,
feil) har en `images/<flate>-<tilstand>-v<n>.png`, laget med Porthole-preview av
skeleton-JSON når formatet tillater det, ellers mockup med eksplisitt liste over hva
dagens skeleton ikke kan rendre. Tekst teller ikke som bilde.

## §4 Tilknyttede formålspakker og lærdommer

Auto-generert av `lookup`. Ikke slett noe her; kommenter heller «ikke relevant fordi …»
hvis en pakke ikke passer. Lærdommene skal *leses* av begge før §1 skrives.

## §5 Avledede tester

| testRef | Formål | Hvordan | Evidens | Status |

Pakketestene kommer inn automatisk. Legg til én rad per bladformål i §1 og én per
antiformål. `Hvordan` er en kommando eller en inspeksjonsprosedyre; `Evidens` er en
fil/anker der utdata skal ligge (TESTRESULT.md#…, ACCEPT.md#…, images/…).
Status: venter / grønn / rød / blocked (+ grunn).

## §6 Åpne spørsmål

Bare spørsmål som endrer treet. Still dem som valg når Kjetil er til stede.

## §7 Revisjonslogg

| Iterasjon | Dato | Hva endret seg | Hvem |

## Etter G1: de andre filene i mappen

- `PLAN.md` — én arbeidspakke per bladformål, i avhengighetsrekkefølge, med purposeRef,
  utfører (Claude / Codex / Xcode / Kjetil), testene den skal gjøre grønne og
  artefaktene den leverer til §3. Handoff til Codex/terminal følger `pkg.std.codex-handoff`.
- `TESTRESULT.md` — ekte utdata under ankrene testene navngir.
- `ACCEPT.md` — §3 rad for rad: forventet → faktisk, med evidenslenke; GUI side om side.
- `STATUS.md` — porter, planbytter med dato og hvorfor, logg.
- `images/`, `skeleton/`, `contract/`, `dataflow.md`, `handoff/` — etter hvilke pakker som er festet.

`purpose_dev.py gates <mappe>` viser hva som mangler for hver port.
