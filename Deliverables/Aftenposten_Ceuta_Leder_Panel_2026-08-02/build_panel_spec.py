#!/usr/bin/env python3
"""Build the panel spec for the Aftenposten Ceuta editorial evaluation.

Reads article_source.md from this folder, embeds it in a shared brief together
with the independently retrieved factual background, and writes the spec to
Tools/ModelKnowledge/panels/aftenposten_ceuta_leder_2026-08-02.json.

Run:  python3 build_panel_spec.py
Then: NANOGPT_API_KEY=$(security find-generic-password -a nanogpt \
        -s com.digipomps.cellscaffold.aigateway -w) \
      python3 Tools/ModelKnowledge/run_advisory_panel.py --provider nanogpt \
        --spec Tools/ModelKnowledge/panels/aftenposten_ceuta_leder_2026-08-02.json
"""

from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SPEC_OUT = ROOT / "Tools" / "ModelKnowledge" / "panels" / "aftenposten_ceuta_leder_2026-08-02.json"

ARTICLE = (HERE / "article_source.md").read_text(encoding="utf-8")

BACKGROUND = """\
## Uavhengig hentet faktabakgrunn (hentet 2026-08-02, IKKE fra lederen)

Denne bakgrunnen er hentet av panelriggen via nettsøk, ikke av Aftenposten.
Bruk den til kildegransking. To regler:

- Der kilder spriker, ER SPRIKET funnet. Ikke velg ett tall og presenter det
  som fasit.
- Tidsstemplene er bindende. Lederens deadline er fredag 31.07.2026 kl. 21:44.

### FØR deadline (lederen kunne vite dette)

- Torsdag 30.07: migrasjonspresset mot Ceuta eksploderer. Spanske myndigheter
  oppga nær 50.000 migranter inn fra Marokko i løpet av ca. ett døgn; Ceutas
  regionale president anslo 60.000 fredag. Euronews meldte først «more than
  40,000», senere 31.07 «at least 60,000 ... in a single day».
- Torsdag 30.07: Meloni på Facebook om «ekstraordinære tiltak», herunder
  suspensjon av Schengen-samarbeidet med Spania.
- Dødstall gjennom 31.07 var SPRIKENDE og foreløpige: Al Jazeera og NPR minst
  18; Aftenposten og Forbes 34; politikilder 43 funnet; AP 41; Reuters minst 57.
  Flertallet druknet ved svømming rundt molene ved Tarajal og Benzú; noen omkom
  i trengsel ved grenseanlegget.
- Høyesterettsdommen (Tribunal Supremo) falt 29.06.2026: stanset summariske
  returer av migranter som ankommer Ceuta og Melilla sjøveien. Spansk
  innenriksdepartement pekte på den som utløsende faktor. Guardia Civil-
  talsperson: «It has been a slow trickle since the Supreme Court's ruling,
  but today has been an explosion.»
- 31.07: spanske myndigheter oppga at ca. 50.000 hadde returnert frivillig til
  Marokko. Militær utplassert i Ceuta. Sánchez omtalte hendelsen som «an attack,
  a violation of Spanish territorial sovereignty».
- Parallell uro i Bni Nsar på marokkansk side ved Melilla: sammenstøt med
  politi, steinkasting, påtenning av politibiler.
- Italia, Finland, Danmark og Tsjekkia hadde tatt til orde for å suspendere
  Spania fra Schengen. (Nøyaktig tidspunkt for de tre siste er ikke fastslått
  av riggen — behandle som usikkert plassert i tidslinjen, og si det.)

### ETTER deadline (lederen kunne IKKE vite dette — bruk kun til å vurdere
### hvordan analysen bar, aldri som kritikk av utelatelse)

- Italia gjeninnførte faktisk midlertidige, målrettede grensekontroller mot
  Spania i én måned, for tredjelandsborgere som ankommer fra Spania med fly
  eller sjøveien. Meloni kalte det en ekstraordinær nasjonal
  sikkerhetsforanstaltning. Merk at dette er noe ANNET enn «suspensjon av
  Schengen» — panelet skal selv avgjøre hvor mye den forskjellen betyr.
- 22 europeiske regjeringer (bl.a. Østerrike, Slovenia, Tyskland, Sverige,
  Belgia, Nederland, Polen, Hellas og flere sentral- og østeuropeiske land)
  undertegnet et felles brev om at hendelsene hadde svekket tilliten til EUs
  felles migrasjonspolitikk.
- Sánchez omtalte alliertes reaksjon som «selfish, polarizing and unlawful».
  Utenriksminister José Manuel Albares: det er umulig å reise fra eksklaven til
  det spanske fastlandet uten å passere politikontroll.
- Senere oppsummert dødstall: 67.

### Tidligere hendelser (til naturlig-eksperiment-testen)

Ceuta mai 2021 (~8.000–10.000 inn etter marokkansk grensesvikt, under
diplomatisk strid om Vest-Sahara/Ghali-saken); Melilla juni 2022 (dødelig
trengsel ved gjerdet, minst 18–23 døde, strid om spansk og marokkansk
politiopptreden); Hellas–Tyrkia ved Evros mars 2020; Polen/Litauen–Belarus
2021; EU–Tyrkia-avtalen 2016; EUs relokaliseringsordninger etter 2015.
Panelet skal selv vurdere om disse er strukturelt like eller bare overfladisk
like — riggen påstår ingen av delene.
"""

TASK = """\
# Oppgave: strukturert evaluering av en lederartikkel

Du er ett medlem av et rådgiverpanel. Flere modeller får akkurat denne
briefen med ulike roller. Du skal IKKE forsøke å gjøre alles jobb — gjør din
rolle grundig, og la de andre gjøre sine. Uenighet mellom roller er signal,
ikke støy.

Objektet som evalueres er Aftenpostens lederartikkel gjengitt nedenfor.
Evalueringen gjelder SAKEN og TEKSTEN — aldri personer. Ingen rangering av
mennesker, ingen omdømmescore, ingen karakteristikker av redaktører.

## Kritiske begrensninger du må respektere

**Lederteksten er komplett.** Du har hele brødteksten verbatim. En påstand du
tilskriver lederen MÅ derfor ha et verbatim `quoteAnchor`. Har den ikke det, er
den `isInferred=true` og kan ikke telle som støtte for hva lederen mener.

**Deadline-disiplin — den viktigste rettferdighetsregelen her.** Lederen ble
publisert fredag 31.07.2026 kl. 21:44. Faktabakgrunnen nedenfor inneholder
hendelser fra ETTER det tidspunktet. Du skal:

1. Merke hver bakgrunnsopplysning som før eller etter deadline før du bruker
   den. Det står i tidslinjen.
2. ALDRI kritisere lederen for ikke å nevne noe som skjedde etter 31.07 21:44.
   Det er etterpåklokskap forkledd som kildekritikk.
3. Skille skarpt mellom to helt ulike funn: (a) lederen sa noe som var galt
   ut fra det som var kjent ved deadline — ekte feil; (b) lederen sa noe som
   senere utviklet seg annerledes — ikke en feil, men relevant for hvor godt
   analysen bar.
4. Et tredje og legitimt funn: lederen valgte en ramme som gjorde den sårbar
   for en utvikling som allerede var i emning ved deadline. Det krever at du
   viser hva som var i emning FØR 21:44.

Skriv eksplisitt hvilken av kategoriene (a), (b) eller (c) hvert av dine funn
tilhører.

## Hva du skal levere

Bruk HAVENs claim-/argumentmodell (Book 29) og paneldekomponering (Book 30).

Uttrykk hver bærende påstand som en claim-node med:
- `claimID`, `text`, `claimType` (factual | causal | normative | predictive |
  statistical | project_capability), `strength` (assertive | moderated |
  speculative), `quoteAnchor` (verbatim, eller null), `isInferred` (bool).

Komponer per rot-claim med `allOf` (lenkede premisser — svakeste ledd
bestemmer), `anyOf` (uavhengige alternativer), `atLeast` (kvorum), og
`countered` med `rebuts` (påstår at claimen er usann) eller `undercuts`
(påstår at støtten ikke etablerer claimen).

Legg ved støttenoder: evidence, assumption, qualifier, counterargument.

Kildegransking er ærlig eller ikke i det hele tatt: en kilde du husker fra
trening er ALDRI «audited». Statuser: `retrieved` (navngitt kilde i briefen
over), `recalled` (fra hukommelse — gir INGEN støtte), `unavailable`,
`contradicted`.

## Analytiske tester panelet er forpliktet på

Disse er målt til å gi høyest utbytte. Kjør dem der de biter:

- **Naturlig eksperiment (høyest utbytte):** for hvert kontrafaktisk utsagn —
  «hvis Europa i stedet hadde …» — spør FØRST: har dette faktisk skjedd før?
  En scenario som allerede er prøvd har evidens, ikke odds. Ikke gi
  sannsynlighetsbånd til noe som har en virkelig instans.
- **Avslørt preferanse:** sammenlign aktørers uttalte motiv med deres faktiske
  handlinger — for Spania, for de 22 regjeringene, for Marokko, og for
  Aftenposten selv.
- **Falsifiserbarhet:** finn påstander konstruert slik at både bekreftelse og
  avkreftelse støtter dem. Navngi strukturen når den opptrer — også hvis den
  opptrer i lederens egen ramme.
- **Rammeuavhengighet:** ville funnet ditt stå seg under spansk ramme, under
  italiensk/dansk ramme, under marokkansk ramme, og under en migrants ramme?
  Marker funn som er rammeavhengige som nettopp det.

## Format

Lever i denne rekkefølgen, med overskrifter:

1. `## Rollesammendrag` — maks 8 setninger.
2. `## Claim-ledger` — JSON-blokk med claim-nodene og komposisjonene dine.
3. `## Analyse` — prosa, der du viser arbeidet bak ledgeren.
4. `## Testene` — naturlig eksperiment, avslørt preferanse, falsifiserbarhet,
   rammeuavhengighet. Skriv «ikke anvendelig fordi …» der de ikke biter.
5. `## Det jeg ikke kan avgjøre` — eksplisitt liste, med hva som ville avgjort
   det. En tom seksjon her leses som at du ikke har lett godt nok.

Skriv på norsk (bokmål).
"""


PANELISTS = [
    {
        "name": "Tekstintern analytiker",
        "modelID": "openai/gpt-5.6-terra-pro",
        "role": "tekstintern analytiker",
        "roleInstructions": (
            "Du normaliserer lederens egen argumentasjon til en claim-ledger. "
            "Du gjør INGEN kildegransking og feller INGEN dom om lederen har "
            "rett. Du kartlegger: hva hevder teksten, med hvilken styrke, på "
            "hvilke premisser — inkludert premisser den forutsetter uten å si. "
            "Vær særlig nøye med de usagte leddene: tittelens hjelp/trussel-"
            "dikotomi, hva 'allierte' i flertall dekker når brødteksten bare "
            "dokumenterer Meloni, og hva som må være sant for at avslutningen "
            "('grenseløst mye bedre') skal følge av premissene. Marker hvert "
            "slikt ledd `isInferred=true`."
        ),
    },
    {
        "name": "Kildegransker",
        "modelID": "google/gemini-3.1-pro-preview-high",
        "role": "kildegransker (source auditor)",
        "roleInstructions": (
            "Du reviderer lederens faktapåstander mot faktabakgrunnen i briefen. "
            "Gi hver påstand en ærlig status: retrieved / recalled / unavailable "
            "/ contradicted. Recalled gir INGEN støtte — skriv det eksplisitt. "
            "Vær særlig presis på tallene: lederen skriver 60.000 og minst 34 "
            "døde. Vurder om tallvalget er dekket, hvor spriket i kildene ligger, "
            "hva et 21:44-deadline rimeligvis kunne vite, og om lederen markerer "
            "usikkerhet i tråd med det den kunne vite. Skille mellom å ta feil og "
            "å rapportere et foreløpig tall uten forbehold."
        ),
    },
    {
        "name": "Skeptiker",
        "modelID": "anthropic/claude-opus-4.8:thinking",
        "role": "skeptiker",
        "roleInstructions": (
            "Du leverer motargumenter som formelle komposisjoner: `rebuts` "
            "(claimen er usann) eller `undercuts` (støtten etablerer den ikke) — "
            "aldri løse innvendinger. Angrip lederens faktiske argument, ikke en "
            "svakere versjon av det, og sitatforankre det du angriper. Test "
            "særlig: er hjelp/trussel-dikotomien i tittelen uttømmende, eller "
            "skjuler den et tredje alternativ? Følger 'treffer hverken årsaken "
            "eller løsningen' av premissene, eller forutsetter det at Melonis "
            "tiltak bare kan ha ett formål? Og: lederen innrømmer kritikk mot "
            "Spania i to avsnitt før den avviser Meloni — er innrømmelsen "
            "bærende for konklusjonen, eller er den retorisk avlastning?"
        ),
    },
    {
        "name": "Steelman og rimelighetsgransker",
        "modelID": "deepseek/deepseek-v4-pro:thinking",
        "role": "steelman og rimelighetsgransker",
        "roleInstructions": (
            "Du bygger lederens posisjon i dens sterkeste form. Hent forsvaret "
            "fra kilder som FAKTISK argumenterer for den posisjonen (spansk "
            "regjering, EU-solidaritetsargumentet, folkerettslige innvendinger "
            "mot summariske returer) — et selvforfattet steelman er svak evidens, "
            "så navngi hvem argumentet tilhører. Kontroller deretter om panelets "
            "øvrige kritikk treffer det virkelige argumentet eller en stråmann. "
            "Du er ikke lederens advokat: si det klart hvis den sterkeste "
            "versjonen fortsatt ikke holder."
        ),
    },
    {
        "name": "Domeneekspert europeisk migrasjons- og sikkerhetspolitikk",
        "modelID": "x-ai/grok-4.5",
        "role": "domeneekspert i europeisk migrasjons- og sikkerhetspolitikk",
        "roleInstructions": (
            "Du leverer domeneevidens og graver frem skjulte premisser: "
            "Schengen-grensekodeksens faktiske hjemler for midlertidig "
            "grensekontroll og hva 'suspensjon fra Schengen' rettslig sett "
            "innebærer (finnes mekanismen?), Dublin/pakten om migrasjon og asyl, "
            "Ceutas særstilling utenfor Schengens ytre grense for personkontroll, "
            "og Marokkos historiske bruk av grensekontroll som diplomatisk "
            "pressmiddel. Skill juridisk umulig fra politisk usannsynlig fra "
            "faktisk gjennomført. Marker eksplisitt der du er usikker på "
            "rettstilstanden per 2026."
        ),
    },
    {
        "name": "Naturlig-eksperiment-gransker",
        "modelID": "moonshotai/kimi-k2.6:thinking",
        "role": "gransker av kontrafaktiske utsagn og naturlige eksperimenter",
        "roleInstructions": (
            "Du har panelets høyest verdsatte oppgave. For hvert kontrafaktisk "
            "eller prediktivt utsagn i lederen eller i panelets ramme — 'hjelp "
            "ville virket', 'trusler vil ikke virke', 'dette svekker europeisk "
            "samhold' — finn en virkelig instans der det allerede er prøvd: "
            "Ceuta 2021, Melilla 2022, Evros 2020, Belarus-grensen 2021, "
            "EU-Tyrkia-avtalen 2016, relokaliseringsordningene etter 2015. "
            "Hva skjedde faktisk? Ingen sannsynlighetsbånd før den sjekken er "
            "gjort. Der ingen instans finnes, si det — da er utsagnet reelt "
            "åpent, og det er også et funn. Vurder også om analogiene faktisk "
            "er strukturelt like eller bare overfladisk like."
        ),
    },
]


def main() -> int:
    shared_brief = "\n\n".join([TASK, BACKGROUND, "# Lederartikkelen\n\n" + ARTICLE])
    spec = {
        "panelID": "aftenposten_ceuta_leder_2026-08-02",
        "purposeRef": "purpose://prompt.unknown",
        "purposeCandidate": "purpose://knowledge.evaluate-published-argument",
        "dataClass": "public",
        "temperature": 0.2,
        "maxTokens": 8000,
        "sharedBrief": shared_brief,
        "panelists": PANELISTS,
    }
    SPEC_OUT.parent.mkdir(parents=True, exist_ok=True)
    SPEC_OUT.write_text(json.dumps(spec, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {SPEC_OUT}")
    print(f"  shared brief: {len(shared_brief)} chars, {len(PANELISTS)} panelists")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
