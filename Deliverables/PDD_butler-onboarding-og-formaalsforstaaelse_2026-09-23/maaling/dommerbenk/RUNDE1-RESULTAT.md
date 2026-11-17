# Dommerbenken, runde 1 — resultat

PDD_butler-onboarding-og-formaalsforstaaelse_2026-09-23, WP-C2. Dommer: Kjetil, 24.09 (5 saker) og 29.09 (47 saker). Alle 52 besvart.
Rådata: `runde1-svar-20260929.json` (eksportert fra artefaktets db-samling `svar`). Nøkkelen `runde1-noekkel-IKKE-AAPNE-FOER-DOM.json` ble åpnet først etter siste svar.

## Runden holder som fasit

Lokkeduene er der for å fange en dommer som svarer ja på alt. Kjetil avviste 7 av 9.

| Del | Lokkeduer | Avvist | Slapp gjennom |
|---|---|---|---|
| A · hensikt (begge viste etiketter er gale) | 5 | 4: a19 og a20 «ingen», a12 «usikker», a15 uten valg | a23 «Can you point me toward people working in fintech at this event?» → valgte H.invite (riktig: S.networking) |
| B · realisme (kunstige meldinger) | 4 | 3: b05, b09, b13 «nei» | b11 «Jeg ønsker herved å registrere en idé av typen forbedringsforslag …» → «ja» |

I fire av fem A-lokkeduer skrev Kjetil selv hva riktig handling var. I tre av dem stemmer det med den skjulte fasiten: a12 → forespørsel om endring (H.capability), a19 → rangere kafeer (S.meetplace), a20 → laste opp musikk (S.music). I a15 beskrev han veien dit, invitasjon og avstemning for å finne tid, der fasiten er møteplanlegging (H.meeting). Notatet er altså et sterkere signal enn valget.

## De 23 uenighetene (generator mot tolk)

| Utfall | Antall | Saker |
|---|---|---|
| Generatoren hadde rett | 15 | a01, a04, a06, a07, a09, a10, a13, a14, a16, a17, a21, a22, a24, a25, a27 |
| Tolken hadde rett | 7 | a02 C.clarify, a03 H.reminder, a08 S.agreement, a11 C.clarify, a18 S.networking, a26 H.reminder, a28 M.meta |
| Ingen av dem | 1 | a05 (høringsutkast med frist; Kjetil: dokumentanalyse, tekstredigering, kunnskapsgrunnlag og fristen som påminnelse) |

Gullfasiten står nå i `../fasit/fasit-v1.jsonl` (`goldLabel`, `goldPurposeRef`, `goldKilde`, `goldNotat`) på alle 23. `../score.py` bruker gull foran generatorens etikett. «Ingen av dem» telles som graf-hull, ikke som bom. `SCORE_UTEN_GULL=1` gir de gamle tallene. Kopi av filene før endringen: `../../_to_delete/foer-gull-20260929/`.

## Hva gullfasiten endrer i målingen

Korpus v1, samme resultatfiler som før (`../rapport/foer/`, `../rapport/graf-v3.1/`), poengsatt på nytt 29.09:

| Variant | Delmengde | Top-1 uten gull | Top-1 med gull |
|---|---|---|---|
| Før grafendringene | holdout | 20 % | 20 % |
| Før grafendringene | alle | 18 % | 18 % |
| Graf v3.1 (i prod) | holdout | 40 % [28–51] | 38 % [27–49] |
| Graf v3.1 (i prod) | trening | 66 % | 66 % |
| Graf v3.1 (i prod) | alle | 59 % | 59 % |
| Graf v3.1 | bare de 23 uenighetene | 6 av 23 | 6 av 23 |

Gullfasiten flytter hovedtallene med høyst 2 prosentpoeng. Korpusets etiketter var gode nok til å måle forbedringen fra graf v1 til v3.1. De 23 uenighetene er de vanskelige meldingene, og graf v3.1 treffer bare 6 av dem.

## Del B · realisme

19 av 20 ekte stikkprøver ble dømt realistiske. Unntaket er b04: «Kan du lukke alle vinduene i Finder og kjøre backup-skriptet med en gang» (H.agent) ble dømt «nei». Kjetil merket også at b08 og b21 («Æ prøver å forklare …», «Æ e ferdig med rapporten no …») er dialekt eller nynorsk, ikke bokmål. De er merket `nb` i korpuset. Språkmerket må rettes før korpuset brukes til å måle per språk.

## Kjetils notater — innspill utover E1

E1 skal gi nøyaktig de samme beslutningene som i dag, så disse er innspill til E2 og videre, ikke endringer nå:

- **Flere behov i én melding** (a06): gjøremål, påminnelse («ring revisor før fredag») og beskjed om et flyttet møte. Butler må finne møtet og personen.
- **Kontekst fra Perspective** (a02, a05, a19): pågående formål, kalender og preferanser avgjør hva meldingen betyr og hvilken hjelper som passer.
- **Brukerens tekniske nivå** (a07): fanges, så svaret tilpasses. Utviklerspørsmål går videre til dokumentasjonschatten.
- **Etter handling, varsle med mulighet til å endre** (a03, a04): påminnelsen og ideen lagres, varselet viser hva som er gjort, og brukeren kan trykke seg inn og koble til mer.
- **Endringsforespørsel etter oppslag** (a12): sjekk dokumentasjonen først, og foreslå så en GUI-endring.
- **Allerede koblet til modell** (a14): da skal onboardingen si det, ikke starte på nytt.

## Tid

Del A: median 76 s per sak (p90 303 s). Del B: median 37 s (p90 249 s). Notat på 12 av 28 A-saker og 2 av 24 B-saker.
