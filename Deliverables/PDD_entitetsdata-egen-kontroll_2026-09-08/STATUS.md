# STATUS — entitetsdata egen kontroll

- surfaces: binding, cell, gui, skeleton
- tags: ai, autorisasjon, eierskap, entitet, tillit

## Porter
- G1: godkjent 2026-09-15, delta godkjent 2026-09-19    (formålsspesifikasjon iterasjon 5)
- G1-GUI: godkjent 2026-09-15    (seks rendrede tilstander godkjent av Kjetil)
- G2: godkjent 2026-09-22    (Kjetil: «Ok - du implementerer som i PLAN §0.1.»)
- G3: venter        (akseptanse: forventning mot faktisk, alle avledede tester grønne)

Sett en port til `godkjent <dato>` kun når Kjetil har sagt det. `purpose_dev.py validate <mappe>` nekter porter uten artefakter.

## Planbytter (dato — hvorfor)
-

## Logg
- 2026-09-08: opprettet
- 2026-09-15: G1 godkjent av Kjetil. Samtidig fire klargjøringer som gjør treet enklere, ikke større:
  entitetsankeret opprettes i det øyeblikket entiteten trenger å persistere entitydata; adressebok-import
  for å invitere noen uten HAVEN-representasjon *er* en slik hendelse; VC-bevis hører også hjemme i
  entitydata; betaling via Palazzos egen PSP kommer senere og avhenger av at DiMyMint og
  DiMyMicropayments hentes inn. Konsekvens: §6.1 og §6.2 bortfaller — importen og genesis er samme flyt,
  ikke to runder. Neste port er G1-GUI.
- 2026-09-15: G1-GUI godkjent. Kjetil ba samtidig om at manglene i images/README.md legges fram
  som vurderbare utvidelsesforslag for skjelettet (SKELETON_UTVIDELSER_2026-09-15.md), og om at
  invitasjonsopplevelsen tas opp som egen formalsoppgave.
- 2026-09-19: G1 hel igjen. Kjetil godkjente de to bladene som kom til i iterasjon 5
  (owner-brings-their-own-model, every-model-path-is-declared). Neste port: G2 / PLAN.md.
- 2026-09-21: PLAN.md skrevet, venter på G2. 15 arbeidspakker 1:1 mot bladformålene, i seks
  leveringsrunder. dataflow.md, contract/ (tre skjemaer, tolv fixturer, check_fixtures.py — 0 avvik)
  og handoff/README.md er på plass. §5 supplert med de åtte testene §1 navngav men tabellen manglet.
  WP11 (Apple Intelligence-veiene) er blokkert på §6.5 til jeg har lest Apples dokumentasjon.
- 2026-09-22: Kjetil rettet en feil i dataflow.md. Entiteten er en eierskapsgrense, ikke en
  maskingrense: en celle i skyen som eies av meg er innenfor min entitet. Regelen er uniform, og
  Agreement er eneste dør — for data og for funksjonalitet. §2A.4 skrevet, testen skjerpet til å
  dekke handlinger, ny test for at en Agreement gir nøyaktig sitt omfang, og begrunnelsen for
  gateway i appen skrevet om (rekkevidde til lokale modeller + tilgjengelighet uten scaffold).
- 2026-09-22: G2 godkjent. Runde 1 (WP1 genesis + WP2 autorisasjon via IdentityLink) skrevet som
  patch med tester og lagt i handoff/runde1/. 1 283 linjer: to nye CellBase-filer med logikken,
  én ny autorisasjonssti (.linkedIdentity) med linkRef, identiske grep i Vapor- og Apple-ankeret,
  og 25 tester i tre filer. Ingenting kompilert — Kjetil kjører preflight/apply/verify med Codex.
  Forsegling ved første batchPersist er med i koden, men UTESTET til runde 2 har flow-harness.
- 2026-09-22 (kveld): Runde 1 kjørt på Mac-en gjennom Finder → runde1.command (patch mot
  origin/main i eget worktree, ingen berøring av Kjetils utsjekk). CellProtocol: bygger, 1244/1244
  tester grønne, commit ebb0b7f på pdd/entitetsdata-egen-kontroll (ikke pushet). WP2 viste seg i
  hovedsak å være landet på main av en annen oppgave — min parallelle resolver forkastet, to
  herdinger beholdt (binding må være localEntityAnchor; genesis-lenke gjelder bare med gyldig segl).
  Nedstrøms: CellScaffold og Binding er røde mot CellProtocol main uavhengig av patchen
  (swift-crypto-konflikt via DiMyMint; skjeletteditor mangler Tree/ComponentSurface). Se TESTRESULT.
  Ny lærdom: lesson.read-origin-main-before-writing-a-mechanism.
