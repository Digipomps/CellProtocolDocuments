# Panel-test av Walton-skjemaer: diskusjon, empiri og adjudikering

Dato: 2026-07-11. Adjudikator: Claude (final adjudicator per Book 27/30).
Beslutningseier: Kjetil (D1 under er hans, ikke panelets).

Feature under test: `haven.claim-scheme.v0` (CellProtocol `97df6bc`, Book 29 §6)
— Walton-skjemaer med kritiske spørsmål lagt oppå claim-modellen.

Metode: to rådgivere med motsatte mandater analyserte samme testcase
(Jørn Eriks hosted-only-forslag) mot de to ferdige pre-skjema-kjøringene fra
benchmarken 2026-07-06 (te2/c2, begge armer, komplette leveranser). Proponenten
bygde skjema-instanser og merket hvert kritisk spørsmål ærlig som
ALREADY-IN-BASELINE eller NET-NEW; skeptikeren klassifiserte alle anvendbare
kritiske spørsmål som REDUNDANT / CEREMONY / GENUINE-ADD. Artefaktene ligger i
denne mappen (`proponent_scheme_instances.json`, `skeptic_review.md`).

## Rot-claim som ble adjudikert

> «Walton-skjemaene forbedrer panelets argumentanalyse vesentlig.»
> (normativ/prediktiv, moderert styrke)

## Empirisk tally — begge rådgivere konvergerer

| Kilde | Netto-nytt innhold | Av totalt |
| --- | --- | --- |
| Proponent (ærlig merking) | 1 helt ny (sign.alternatives → konfundere i S1), 1 delvis ny (counterbalance → verdijustert TCO), 1 ny som *diagnose* (ekvivokasjon på «GDPR-compliant») | 7 instansierte CQ-er |
| Skeptiker | 1 GENUINE-ADD (vendor-lock-in/prisrisiko i TCO-premisset), 1 strukturell skjerping (feasibility-klassifisering) | 16 anvendbare CQ-er |

Konvergent funn: **på en veldokumentert case med kapabel analytiker reproduserer
den skjemaløse metoden nesten alt innholdet selv** — samme regime-funn som den
rene benchmarken 2026-07-06 ga for selve skillen. Skjemaenes netto-bidrag på
denne casen: 1–2 reelle innholdshull (viktigst: kommersiell innlåsing som
manglende motvekt i kostnadspremisset) pluss skarpere *diagnoser* (navngitt
ekvivokasjon; feasibility-hard-stop), ingen endret dom.

## Adjudikering

- **Rot-claimen SOM FORMULERT: ikke støttet** i regimet «kapabel modell +
  repo-tilgang». Undercut av begge rådgiveres empiri (15/16 redundante CQ-er;
  dommen på testcasen uendret).
- **Innsnevret claim: støttet.** «Skjemaene gir dekningsgaranti, deterministisk
  revisjonsspor og Pollock-korrekt undercut-bro, og gir reelt innsiktsløft for
  svakere modeller, ukjente argumenttyper, governance/etterviselighet og
  mange-claims-batcher.» Begge rådgivere konsederer dette eksplisitt.
- **Kostnadssiden er reell:** manuell instansiering (~20 CQ-statuser per case),
  `completeness`-brøken kan feilleses som kvalitetsmål, og naiv instansiering
  eksploderer deloppgave-listen (18–24 vs baselinens 3–4) hvis CQ-er ikke
  triageres først.
- **Semantikk-sjekk (proponentens RISK):** en skjema-undercut kan aldri nedgradere
  en direkte motsigelse — verifisert mot koden: `countered()` bevarer basens
  `contradicted`-status når effektiv score ikke reduseres under basens (score 0
  forblir 0, status propageres). Ingen kodeendring nødvendig.

## Vedtatte guards (anvendt i skill + Book 29/30, revert enkelt)

1. **Gated instansiering:** ikke instansier skjema på claims en kapabel analytiker
   alt har adjudikert ferdig; bruk dem der et kritisk spørsmål ventes å bli
   *challenged* eller reelt er *unexamined* — og alltid ved svak analytiker,
   ukjent argumenttype eller governance-krav.
2. **Triage før deduksjon:** sett CQ-er til `answered`/`not-applicable` FØR
   `deducedSubtasks()` kjøres, så løkken aldri emitterer alt-besvarbart arbeid.
3. **`completeness` er bokføring:** aldri presentér brøken som målt
   argumentkvalitet.

## Beslutningslogg

- D1 (BESLUTTET — Kjetil, 2026-07-11): guards 1–3 er varig policy. Panelets
  anbefaling fulgt; guidance-endringene i skill + Book 29/30 står.
- Avvist av adjudikator: å fjerne skjemalaget (skeptikerens konsesjoner + de
  innsnevrede regimene gir klar netto verdi til lav kost når guardene står).

## Åpne punkter

- Auto-deteksjon av skjematype fra claim-tekst er fortsatt ugjort (Book 29 §7).
- Regime-hypotesen ble empirisk testet 2026-07-11 (se `regime_test_results.md`
  i denne mappen): ikke bekreftet i enkel form — liten positiv delta på alle
  nivåer, omvendt U (mellomsjiktet tjener mest), og den reelle effekten er
  per-spørsmål-garanti (definisjonskritikk og konfunder-jakt leveres 3/3 med
  stillas mot 0–1/3 uten). Sjekkliste-tunnelsyn observert — bekrefter guard 1.
