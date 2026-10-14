# PLAN — E8: inntak først, så flaten

Til G2. Hører til `E8_G1-TILLEGG.md` (G1 og G1-GUI godkjent 2026-09-29).
Arbeidspakkene står 1:1 mot bladformålene E8.1–E8.7, i den rekkefølgen Kjetil satte:
**inntaket først.**

> «Først må HAVEN Agent ingeste jobber og ideer fra køer — og tråder i deg — Claude — og Codex.» (29.09)

Hver pakke står med fire linjer: **hva det innebærer**, **hva som finnes fra før**,
**hva du må gjøre**, **hvordan det måles**. Det som finnes fra før er målt, ikke antatt.

---

## WP0 — To ting blokkerer alt, og begge er utenfor koden

**0a · GitHub Actions starter ikke jobber.** Ordrett fra GitHub 29.09:
«The job was not started because recent account payments have failed or your spending
limit needs to be increased.» PR #26 (ikonet) og #27 (onComplete) er ferdige og grønne
lokalt, men kan ikke merges uten CI.
→ **Du må rette betalingen.** Ingen kode kan lande før det.

**0b · CellScaffold `main` er rød.** Målt 29.09 på `adf48d46`: bygget består, men
**45 av 2778 tester feiler** over 20 suiter, og CI på samme sha er `failure` siden
28.09 08:38Z (kjøring 36398574469, etter merge av #272).
→ **Trenger en eier.** Benken bor i CellScaffold; ingenting herfra kan landes grønt
mens main er rød. Forslag: egen jobb som finner hva #272 brøt, før WP2.

---

## WP1 — Inntaket (E8.1s forutsetning)

Målet: en jobb, en idé eller et spørsmål som oppstår i en kø eller i en tråd, finnes
etterpå i agenten — uten at noen må huske å fortelle det videre.

### 1a · MCP-en i drift i begge verter

- **Innebærer:** `haven-agentd`-MCP-en må faktisk svare i både Claude og Codex.
- **Finnes fra før:** binæren er installert i agentroten 25.09 og svarer
  (`initialize` → 21 verktøy). Codex-registreringen pekte på en pre-split-sti og er
  rettet. Claude-registreringen er lagt inn i `claude_desktop_config.json`.
- **Du må:** starte Claude-appen på nytt én gang, så den leser den nye registreringen.
- **Måles:** `agent.jobs.list` svarer fra begge verter.

### 1b · En registrering kan be om en handling

- **Innebærer:** `agent.jobs.register` leser `onComplete.actions` og validerer mot
  `AutomationPolicy`, fail closed.
- **Finnes fra før:** implementert i PR #27, 322 tester grønne lokalt. Venter på CI (WP0a).
- **Du må:** ingenting utover WP0a.
- **Måles:** en jobb registrert gjennom MCP med `losen-probe` utfører handlingen —
  samme kjede som ble bevist 25.09, men hele veien fra MCP-kallet.

### 1c · Køinntak

- **Innebærer:** hver jobb i `_losen-queue` (alle baner, `inbox*`, `running`, `done`)
  registreres som en AgentJob med status, bane, leveransesti og frist.
- **Finnes fra før:** `agent.jobs.import` tar en hel pakke (manifest + job-specs +
  work-items + køposisjoner) register-only med `executionAuthorized=false`. Men
  manifestskjemaet er låst til `haven.security-audit-import.v1` — mekanismen er
  bygget, navnet er for smalt.
- **Du må:** ingenting. Ett valg: skal historiske jobber i `done/` med (jeg foreslår
  de siste sju dagene, ikke alle 2600).
- **Måles:** antall jobber i køen = antall AgentJobs med kilde `losen-queue`, og en ny
  jobb dukker opp innen ett minutt.

### 1d · Tråder og ideer

- **Innebærer:** en tråd (Cowork, Claude Code, Codex) registrerer det den finner på —
  en jobb, en idé eller et spørsmål — med én verktøykall, uten å be deg om noe.
- **Finnes fra før:** `IdeaTaskWorkspaceCell` og `WorkItemCell` finnes i benken.
  Agentens side mangler et skille mellom *idé* og *jobb*: i dag er alt en jobb.
- **Du må:** ingenting.
- **Måles:** en idé registrert fra en tråd står i benken som idé, ikke som en jobb som
  later som den skal kjøres.

---

## WP2 — Portene kommer inn av seg selv (E8.1)

- **Innebærer:** HAVEN Agent leser portlinjene i `Deliverables/*/STATUS.md` lokalt og
  registrerer hver port med status `venter` som et spørsmål til deg. Kilden er filene,
  ikke en tråds hukommelse.
- **Finnes fra før:** formatet er fast (`- G1: …`, `- G3: venter`) i alle PDD-mapper.
  Ingenting leser dem i dag.
- **Du må:** ingenting.
- **Måles:** `test.e8.alle-ventende-vises` — antall rader = antall porter med `venter`.
  Måling 29.09 til sammenligning: seks PDD-er, seks ventende.

## WP3 — Raden sier hva du skal avgjøre (E8.2, E8.3)

- **Innebærer:** hver rad bærer avgjørelsesteksten og lenker til underlaget. En rad uten
  avgjørelsestekst vises ikke — det er bedre at den mangler enn at den er innholdsløs.
- **Du må:** se på det rendrede bildet igjen når første skive står, og si om teksten
  treffer. Det er den eneste GUI-runden i planen.
- **Måles:** `test.e8.rad-uten-avgjorelse-vises-ikke`, `test.e8.underlag-lenke-loeser`.

## WP4 — Du svarer fra raden (E8.4)

- **Innebærer:** listevalg og fritekst fra kortet. Anbefaling merket som anbefaling.
- **Du må:** ingenting.
- **Måles:** `test.e8.svar-listevalg`, `test.e8.svar-fritekst`, `test.e8.anbefaling-er-ikke-svar`.

## WP5 — Svaret føres inn og kan spores (E8.5)

- **Innebærer:** raden viser hva svaret ble ført inn i — fil, port, commit.
- **Du må:** svare på Q-E8-3: skal «ført inn» settes av tråden som fører det inn, eller
  skal benken utlede det? Jeg foreslår det første: benken skal ikke påstå noe den ikke vet.
- **Måles:** `test.e8.foert-inn-peker-paa-endring`.

## WP6 — Ingen spøkelser, og gjenåpning (E8.6, E8.7)

- **Innebærer:** en gitt port forsvinner ved neste oppdatering; et gjenåpnet spørsmål
  beholder historikken.
- **Måles:** `test.e8.ingen-spoekelser`, `test.e8.gjenaapning-bevarer-historikk`.

---

## Rekkefølgen, og hvorfor

WP0 er ikke arbeid, det er to stengsler. WP1 er din prioritering og gir verdi alene:
når inntaket virker, finnes jobbene og ideene ett sted selv før flaten er bygget.
WP2+WP3 er første skive som *når deg* — da er problemet du beskrev borte.
WP4–WP6 gjør sløyfen hel.

**Det du faktisk må gjøre:** rette betalingen (0a), finne en eier for rød main (0b),
starte Claude-appen én gang (1a), velge hvor langt tilbake køhistorikken skal med (1c),
se på bildet når første skive står (WP3), og svare på Q-E8-3 (WP5). Ingenting annet.
