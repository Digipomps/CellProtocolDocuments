#!/usr/bin/env python3
"""Round 2: adjudication with a CORRECTED timeline.

Round 1's shared brief contained a factual error: it told every panelist that
Italy's actual border-control measures came AFTER the editorial's deadline.
Retrieval on 2026-08-02 established they were formally approved Friday morning
31.07 and publicly reported by 18:24 CEST — over three hours BEFORE the
21:44 deadline. Every round-1 finding that leaned on that error must be
re-evaluated. This round hands the adjudicators the correction, the article,
and all round-1 output.
"""

from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SPEC_OUT = ROOT / "Tools" / "ModelKnowledge" / "panels" / "aftenposten_ceuta_leder_2026-08-02_round2.json"

ARTICLE = (HERE / "article_source.md").read_text(encoding="utf-8")

CORRECTION = """\
# KORRIGERT TIDSLINJE — leser opphever runde 1 der de er i strid

Runde 1 ble kjørt på en brief som inneholdt en FEIL: den plasserte Italias
faktiske grensekontroller ETTER lederens deadline. Det var galt. Alle
panelister i runde 1 arvet feilen. Der et runde 1-funn hviler på den, skal
funnet forkastes eller snus. Dette er den viktigste oppgaven din.

Lederens deadline: fredag 31.07.2026 kl. 21:44 CEST (Norge = Spania = Italia).

## FØR deadline — lederen kunne vite dette

- **Ons 29.07 og tidligere:** ca. 1.500 hadde kommet til Ceuta ved å svømme
  rundt molene siden 20.07. Tribunal Supremo-dommen falt 29.06.2026: stanser
  summarisk retur av sjøankomster til Ceuta/Melilla, krever individuell
  vurdering. Guardia Civil: «a slow trickle since the Supreme Court's ruling,
  but today has been an explosion.»
- **Tor 30.07 morgen:** flere tusen samler seg ved grensen; massegjennombruddet
  starter.
- **Tor 30.07:** Meloni advarer, etter samtale med innenriksminister Piantedosi,
  om «ekstraordinære tiltak», herunder «suspendere Schengen-avtalen med
  Spania». Utenriksminister Tajani støtter. Italias innenriksdepartement
  BEORDRER samme kveld midlertidig suspensjon av Schengen-samarbeidet med
  Spania.
- **Fre 31.07 morgen:** vedtaket FORMELT GODKJENT i møte i innenriksdepartementet
  ledet av Piantedosi (Komiteen for immigrasjonsanalyse og grensesikkerhet).
  Meloni kunngjør det sammen med Tajani og Salvini: regjeringen «has decided to
  temporarily suspend the free movement regime provided for by Schengen for sea
  and air connections with Spain, reintroducing border controls». Tiltaket er
  målrettet: én måned, tredjelandsborgere som ankommer fra Spania med fly eller
  sjøveien.
- **Fre 31.07 samme dag:** Frankrike (Macron) styrker grensekontrollene langs
  landegrensen mot Spania. Finlands innenriksminister Mari Rantanen starter
  forberedelser til gjeninnføring av grensekontroll.
- **Fre 31.07 kl. 18:24 CEST:** Euronews publiserer saken om Italias vedtak.
  Det vil si: 3 timer og 20 minutter FØR Aftenpostens deadline var Italias
  beslutning offentlig kjent og publisert av et stort europeisk medium.
- **Fre 31.07:** spansk regjering rapporterer ca. 49.000 inntrengninger på 24
  timer; Ceutas regionale president Juan Jesús Vivas oppgir 60.000.
- **Fre 31.07 formiddag/ettermiddag:** ca. 25.000 hadde returnert frivillig til
  Marokko. **Fre 31.07 kveld:** tallet steg til 48.300 (spansk
  innenriksdepartement, meldt av Reuters/AP/France24/Euronews samme dag).
- **Fre 31.07:** Sánchez omtaler hendelsen som «an attack, a violation of
  Spanish territorial sovereignty». Militær utplassert i Ceuta.
- Dødstallene var sprikende gjennom 31.07: Al Jazeera/NPR minst 18; Aftenposten
  og Forbes 34; politikilder 43; AP 41; Reuters minst 57.
- **Våren 2026 (kjent lenge før):** Spanias regulariseringsreform trådte i kraft
  20.04.2026. Opptil ca. 500.000 papirløse kan få ett års opphold- og
  arbeidstillatelse (krav: opphold i Spania før 31.12.2025, minst fem måneder,
  rent rulleblad). Over 1 million søknader per 30.06.2026. Funcas anslo 840.000
  uten lovlig opphold ved inngangen til 2025. Spanias sjette større
  regularisering. Ordningen var alt omtalt i europeisk presse som noe som
  «ryster Europa» med frykt for dominoeffekt for Schengen.
- EU-kommissær for migrasjon Magnus Brunner tilbød Frontex-støtte til
  overvåking, registrering og returer.

## ETTER deadline — kan IKKE brukes som kritikk av utelatelse

- **Lør 01.08:** brev fra 22 EU-ledere til kommisjonspresidenten, ledet av
  Italia og Danmark. Anklager Spania for å skape en «pull factor» og for en
  oppfatning av at «illegal entry into the EU is possible». Signatarer bl.a.
  Østerrike, Belgia, Bulgaria, Kroatia, Kypros, Tsjekkia, Estland, Finland,
  Hellas, Ungarn, Latvia, Litauen, Malta, Nederland, Polen, Romania, Slovakia,
  Slovenia, Sverige.
- **Lør 01.08:** Sánchez svarer og kaller alliertes reaksjon «selfish,
  polarizing and unlawful». Albares: umulig å reise fra eksklaven til fastlandet
  uten politikontroll; Spania har en av EUs minst porøse grenser.
- **01.08:** dødstall minst 67 bekreftet; Sky News melder 86 ifølge lokale
  myndigheter.
- Finland, Nederland, Danmark, Tsjekkia og Sverige slutter seg til Italias
  posisjon.

## Kildekonflikt du skal rapportere, ikke skjule

The Olive Press (01.08) daterer Italias kunngjøring til «fredag kveld 1.
august» — internt inkonsistent, siden 1. august var en lørdag. Euronews'
eget publiseringstidsstempel 31.07 kl. 18:24 CEST, med vedtaket omtalt som
allerede formelt godkjent fredag morgen, er sterkere evidens enn en
retrospektiv dagsangivelse. Behandle 18:24-tidsstemplet som det beste
tilgjengelige, men si at kildene spriker.
"""

TASK = """\
# Runde 2: adjudikasjon

Du er adjudikator i et rådgiverpanel som evaluerer Aftenpostens lederartikkel
«Spania trenger hjelp, ikke trusler fra allierte» (31.07.2026 21:44).

Du får: (1) den korrigerte tidslinjen, (2) lederen i fulltekst, (3) alle seks
runde 1-leveranser. Runde 1 ble kjørt på en feilaktig tidslinje. Din jobb er
IKKE å referere runde 1, men å felle dom.

## Det du skal gjøre

1. **Kjør korreksjonen først.** Gå gjennom runde 1-funnene og identifiser hvert
   funn som hviler på den feilaktige premissen om at Italias tiltak var
   etter-deadline. For hvert: står funnet, snus det, eller faller det? Vær
   konkret om hvilket funn og hvilken panelist.

2. **Adjudiser hver rot-claim** med Book 29-semantikk, anvendt som skrevet:
   `allOf` = svakeste ledd; en motsagt premiss gjør forelderen *unsupported*,
   ikke *contradicted*; dominerende rebuttal gir *contradicted*; undercut
   diskonterer. Ikke øyemål poeng. Hver rot-claim ender `supported`,
   `contradicted`, eller `open` med grunn og eier.

3. **Klassifiser hvert funn** som (a) feil ut fra det som var kjent ved
   deadline, (b) senere utvikling — ikke en feil, eller (c) rammevalg som var
   sårbart for noe som alt var i emning.

4. **Publiser metrikkblokken Q1–Q10** med verdi OG evidensen bak. Dette er
   diagnostikk, aldri mål. Ikke fabrikker et motfunn for å flytte et tall.
   Q1 sporbarhet i posisjonsendring; Q2 blandet ledger (INGEN målverdi —
   evidensen bestemmer); Q3 revisjonsærlighet; Q4 rammeuavhengighet;
   Q5 falsifiserbarhet; Q6 naturlig eksperiment; Q7 avslørt preferanse;
   Q8 terminal adjudikasjonsrate; Q9 steelman fra motpartskilder;
   Q10 innrømmelser uten nytt evidensanker.

## Disiplin

- Sitatforankre alt du tilskriver lederen. Ellers `isInferred=true`.
- En kilde du husker fra trening er ALDRI «audited». Bare den korrigerte
  tidslinjen og lederteksten er hentet materiale her.
- Ikke kritiser lederen for 01.08-hendelser.
- Saken og teksten, aldri personer. Ingen karakteristikk av redaktører.
- Panelet er ikke stemmemaskin. Der runde 1-panelistene er uenige, avgjør du
  på evidens og sier hvorfor — ikke ved flertall.
- Du skal ikke være snill mot verken lederen eller panelet. Hvis runde 1
  overdrev, si det. Hvis lederen kommer bedre ut etter korreksjonen enn runde 1
  antok, si DET like tydelig.

## Format

1. `## Korreksjonen` — hva faller, hva snus, hva står.
2. `## Adjudikasjon` — rot-claim for rot-claim, med Book 29-begrunnelse.
3. `## Samlet vurdering av lederen` — hva den får rett, hva den får galt, hva
   som er rammeavhengig. Maks 400 ord.
4. `## Q1–Q10` — tabell med verdi og evidens.
5. `## Åpne punkter` — med grunn og hvem som eier dem.

Skriv på norsk (bokmål).
"""


def main() -> int:
    r1 = HERE / "round1"
    parts = []
    for p in sorted(r1.glob("*.md")):
        parts.append(p.read_text(encoding="utf-8"))
    round1 = "\n\n---\n\n".join(parts)

    shared_brief = "\n\n".join(
        [
            TASK,
            CORRECTION,
            "# Lederartikkelen\n\n" + ARTICLE,
            "# Runde 1 — alle seks leveranser\n\n" + round1,
        ]
    )
    spec = {
        "panelID": "aftenposten_ceuta_leder_2026-08-02_round2",
        "purposeRef": "purpose://prompt.unknown",
        "dataClass": "public",
        "temperature": 0.15,
        "maxTokens": 20000,
        "sharedBrief": shared_brief,
        "panelists": [
            {
                "name": "Adjudikator A",
                "modelID": "openai/gpt-5.6-terra-pro",
                "role": "adjudikator",
                "roleInstructions": (
                    "Du feller dom med Book 29-semantikk anvendt bokstavelig. "
                    "Vær hard på runde 1 der den overdrev, og like hard på "
                    "lederen der den svikter. Prioriter korreksjonsarbeidet."
                ),
            },
            {
                "name": "Adjudikator B",
                "modelID": "anthropic/claude-opus-5",
                "role": "adjudikator",
                "roleInstructions": (
                    "Du feller dom uavhengig av Adjudikator A. Legg særlig vekt "
                    "på Q2 og Q10: let aktivt etter steder der panelet har vært "
                    "føyelig mot oppdragsgiverens implisitte forventning om at "
                    "lederen skal felles, og steder der det motsatte skjedde."
                ),
            },
        ],
    }
    SPEC_OUT.parent.mkdir(parents=True, exist_ok=True)
    SPEC_OUT.write_text(json.dumps(spec, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {SPEC_OUT}")
    print(f"  shared brief: {len(shared_brief)} chars")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
