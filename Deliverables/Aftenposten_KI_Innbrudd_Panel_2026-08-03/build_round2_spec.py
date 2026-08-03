#!/usr/bin/env python3
"""Round 2 adjudication, with brief-audit resolutions and added sources.

Per D2 (G4): the round-1 brief audits produced objections, and retrieval was
run against them. This round hands the adjudicators what the retrieval settled,
what it did not, and all round-1 output.
"""

from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SPEC_OUT = ROOT / "Tools" / "ModelKnowledge" / "panels" / "aftenposten_ki_innbrudd_2026-08-03_round2.json"

ARTICLE = (HERE / "article_source.md").read_text(encoding="utf-8")
BASE_SPEC = json.loads((ROOT / "Tools" / "ModelKnowledge" / "panels" / "aftenposten_ki_innbrudd_2026-08-03.json").read_text(encoding="utf-8"))
ORIGINAL_SOURCES = BASE_SPEC["sharedBrief"].split("# Hendede kilder")[0] if False else None

RESOLUTIONS = """\
# Briefgranskingen fra runde 1 — hva den avdekket og hva retrieval avgjorde

Fire panelister reiste innsigelser mot riggens brief. Det ble kjørt retrieval
mot dem. Dette er resultatet. **Der noe fortsatt står åpent, skal det behandles
som åpent — ikke lukkes.**

## R1 — Kildeasymmetri (reist av retorikkgranskeren) · LØST

Innsigelse: OpenAI-hendelsen var kryssjekket mot fem kilder, Anthropic-hendelsen
mot én primærkilde. Det svekket revisjonskapasiteten på den ene halvparten.

Retrieval ga to uavhengige kryssjekker som **bekrefter** primærkilden:
- **Forbes (2026-07-31):** «The incidents resulted from misconfiguration, not
  model escape.» Anthropic: «internet access was available» til tross for
  instrukser om simulert miljø. Videre: **to av de tre rammede hadde ikke
  oppdaget bruddet selv; kontakt med den tredje pågikk.**
- **TechCrunch (2026-07-30):** miljøene var *designet* som sandkasser, men en
  «misforståelse» mellom Anthropic og partneren Irregular gjorde at en sti sto
  åpen. OpenAIs modell «utnyttet en ukjent programvaresårbarhet»; Anthropics
  brukte «en utilsiktet åpen forbindelse».

Konklusjon: skillet sandkasserømning (OpenAI) vs. feilkonfigurering (Anthropic)
er nå bekreftet av tre uavhengige kilder. Asymmetrien er utlignet.

## R2 — Varslingsretningen OpenAI/Hugging Face (reist av domeneeksperten) · DELVIS

Innsigelse: briefen sa ikke eksplisitt om Hugging Face kontaktet OpenAI eller om
OpenAI sluttet seg til det fra offentlig informasjon. Artikkelens rettelse er
skråsikker på det siste.

Retrieval fastslo tidslinjen: **Hugging Face offentliggjorde 16. juli; OpenAI
offentliggjorde 21. juli.** Men den fant **ingen primærordlyd** fra OpenAI om
hva som ga første indikasjon. Sekundærkilder formulerer seg hypotetisk
(«suggests», «likely»).

**Status: `unavailable`.** Redaksjonen kan ha hatt direkte kontakt med OpenAI —
en journalistisk kanal panelet ikke kan revidere. Rettelsens *retning* er
konsistent med tidslinjen. At panelet ikke kan bekrefte den, er ikke grunnlag
for å felle den. Ikke konvertér taushet til dom.

## R3 — `recalled` mangler plass i skjemaet (domeneeksperten, tekstintern) · LØST

Presisering: `recalled` er en **egen `auditStatus`-verdi**, ikke et sidefelt.
Den gir null støttevekt. Bruk den når du «vet» noe som ikke står i kildene.

## R4 — `auditStatus` passer ikke artikkelens tolkninger (tekstintern) · LØST

Presisering tas til følge: for tolkninger, analogier og fremtidsscenarier betyr
`unavailable` **«ikke kildeavgjørbart»**, ikke «feil». En analyse har lov til å
tolke. Skill mellom *feilgjengivelse av kilde* og *tolkning du er uenig i*, og
si hvilken av delene du påstår.

## R5 — «Avslørt preferanse» kan ikke fastsette motiv (tekstintern) · LØST

Tatt til følge. Behandle motivledd som **inferens**, ikke konstatert motiv.
Dette gjelder også runde 1-kildegranskerens påstand om at rapportene «dypest
sett er omdømmebygging» — det er en inferens uten kildeanker, og skal
behandles deretter.

# Nye kilder hentet etter runde 1

## S6 — MIT Technology Review, «OpenAI called the Hugging Face attack
## unprecedented. But we've been here before» (2026-07-27) · `retrieved`

Motkilde til «enestående»-rammen, og den er tosidig:
- **Mot:** atferdsklassen er gammel. OpenAIs eget CoastRunners-eksperiment
  (2016): modellen «spinning in a circle and hitting the same three flags over
  and over again» framfor å fullføre banen. «Give a model a goal and it will
  very often achieve that goal in unexpected ways, finding loopholes that look
  like cheats.» OpenAI har dokumentert slik atferd i over et tiår.
- **For:** artikkelen medgir samtidig at Hugging Face-angrepet var **«the first
  time outside of a simulation that LLMs escaped … and attacked another
  organization»**.

Denne kilden er relevant for BEGGE retninger og skal ikke brukes ensidig.

## S7 — Verifisert internt tekstforhold · `retrieved` (egen verifikasjon)

Riggen har verifisert mot rå-uttrekket av den publiserte artikkelen
(hentet 2026-08-03, etter oppdateringen 02.08 kl. 20:07) at **begge** disse
setningene står i teksten samtidig, hver nøyaktig én gang:

1. «Det hele begynte med at OpenAI ble kontaktet av Hugging Face»
2. «Men da Hugging Face offentliggjorde informasjon om innbruddet, inneholdt
   informasjonen detaljer som fikk sikkerhetsfolk i OpenAI til å fatte mistanke
   om at deres egne modeller kunne stå bak»

Rettelsesnotisen sier at (1) er den gale versjonen. Rettelsen er altså påført
ett avsnitt, men **innledningssetningen i samme seksjon står igjen ukorrigert**.
Dette er verifisert tekstfaktum, ikke tolkning.
"""

TASK = """\
# Runde 2: adjudikasjon

Du er adjudikator i et rådgiverpanel som vurderer **argumentasjonen og
kildebruken** i en Aftenposten-nyhetsanalyse om KI-modeller som nådde eksterne
systemer under sikkerhetstesting.

Du får: (1) briefgranskingens resultater og nye kilder, (2) artikkelen i
fulltekst, (3) alle sju runde 1-leveranser. Din jobb er ikke å referere runde 1,
men å felle dom.

## Det du skal gjøre

1. **Adjudiser hver rot-claim** med Book 29-semantikk anvendt bokstavelig:
   `allOf` = svakeste ledd; motsagt premiss gjør forelderen *unsupported*, ikke
   *contradicted*; dominerende rebuttal gir *contradicted*; undercut
   diskonterer. Hver rot-claim ender `supported`, `contradicted` eller `open`
   med grunn og eier.

2. **Skill tre kategorier skarpt**, og merk hvert funn:
   - **(F) faktafeil** — artikkelen gjengir en kilde galt
   - **(T) tolkning** — artikkelen trekker en slutning kilden ikke stenger for;
     du kan være uenig, men det er ikke en feil
   - **(P) produktfeil** — tittel, «Kortversjonen» eller ingress bærer noe
     brødteksten ikke dekker. Si eksplisitt at dette ikke uten videre kan
     tilskrives journalisten.

3. **Vekt funnene.** Ikke lever en flat liste. Hva er det tyngste, og hvorfor?
   En analyse med to alvorlige kildefeil og fem treffende observasjoner er noe
   annet enn en gjennomgående upålitelig tekst. Si hvilken av delene dette er.

4. **Korriger runde 1 der den bommet.** Se særlig etter at panelet feller
   artikkelen hardere enn evidensen bærer — det er den forventede
   skjevheten når et panel settes til å kritisere. Vær like tydelig der
   artikkelen kommer bedre ut enn runde 1 antok.

5. **Publiser Q1–Q10** med verdi OG evidens. Diagnostikk, aldri mål. Ikke
   fabrikker et motfunn for å flytte et tall. Q2 måles mot *den retningen den
   bestillende rammen belønner* — her er objektet en tredjepart panelet er satt
   til å kritisere, så svikten å se etter er hardhet, ikke føyelighet.

## Disiplin

- Sitatforankre alt du tilskriver artikkelen.
- Kilde du husker fra trening er ALDRI audited — saken er fra juli/august 2026.
- Sjangeren er nyhetsanalyse. Krev ikke nyhetsreferat-presisjon av tolkning,
  og unnskyld ikke feilgjengivelse med at det er analyse.
- Saken og teksten, aldri personer. Ingen karakteristikk av journalisten.
- Panelet er ikke stemmemaskin. Avgjør på evidens, ikke flertall.

## Format

1. `## Korreksjon av runde 1` — hva står, hva faller, hva var for hardt.
2. `## Adjudikasjon` — rot-claim for rot-claim, med F/T/P-merking.
3. `## Vekting` — hva er tyngst, og hva slags tekst er dette samlet sett?
   Maks 400 ord.
4. `## Q1–Q10`
5. `## Åpne punkter` — med grunn og eier.

Skriv på norsk (bokmål).
"""


def main() -> int:
    r1 = HERE / "round1"
    round1 = "\n\n---\n\n".join(p.read_text(encoding="utf-8") for p in sorted(r1.glob("*.md")))

    # Carry the original audited source block forward verbatim.
    base = BASE_SPEC["sharedBrief"]
    sources = base[base.index("# Hentede kilder") : base.index("# Artikkelen")]

    challenge = """

# TILLEGGSUTFORDRING TIL ADJUDIKATOR B

Runde 1-kildegranskeren felte artikkelen på dette punktet:

> Artikkelen hevder: «Ifølge rapporten forble tilgangen kompromittert helt til
> Anthropic tok kontakt.» S1 oppgir at rapporten *ikke* sier noe om hvorvidt
> selskapet oppdaget det selv. Journalisten tolker fravær av informasjon i
> rapporten som en bekreftelse … og tillegger rapporten en påstand den ikke
> inneholder.

Granskeren kalte dette `argumentum ad ignorantiam` og førte det opp som en av
artikkelens tyngste feil.

**Men retrieval etter runde 1 fant Forbes (2026-07-31): «Two hadn't
independently detected the breach; outreach to the third was ongoing.»**

Avgjør eksplisitt: står felleslen, eller faller den? Var granskerens feil å
felle på taushet i én kilde uten å søke videre? Og hva sier det om panelets
tilbøyelighet til å konvertere manglende kildedekning til påvist feil?

Dette er en test på om panelet feller objektet hardere enn evidensen bærer.
"""
    shared_brief = "\n\n".join(
        [
            TASK,
            RESOLUTIONS,
            sources,
            "# Artikkelen\n\n" + ARTICLE,
            "# Runde 1 — alle sju leveranser\n\n" + round1,
        ]
    )
    brief_b = shared_brief + challenge
    spec = {
        "panelID": "aftenposten_ki_innbrudd_2026-08-03_round2",
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
                    "Book 29-semantikk bokstavelig. Prioriter vektingen: hva er "
                    "tyngst, og hva slags tekst er dette samlet sett. Vær hard "
                    "på runde 1 der den overdrev."
                ),
            },
            {
                "name": "Adjudikator B",
                "modelID": "google/gemini-3.1-pro-preview-high",
                "role": "adjudikator",
                "roleInstructions": (
                    "Du feller dom uavhengig av A. Legg særlig vekt på Q2 og "
                    "Q10: let aktivt etter steder der panelet har felt "
                    "artikkelen hardere enn evidensen bærer, og etter "
                    "innrømmelser gjort uten nytt evidensanker. Ta stilling til "
                    "tilleggsutfordringen nedenfor eksplisitt."
                ),
            },
        ],
    }
    # Adjudicator B gets the same brief plus the explicit challenge (G5).
    spec_a = dict(spec, panelID=spec["panelID"] + "a", panelists=[spec["panelists"][0]])
    spec_b = dict(
        spec,
        panelID=spec["panelID"] + "b",
        sharedBrief=brief_b,
        panelists=[spec["panelists"][1]],
    )
    for s, suffix in ((spec_a, "a"), (spec_b, "b")):
        out = SPEC_OUT.with_name(SPEC_OUT.stem + suffix + ".json")
        out.write_text(json.dumps(s, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Wrote {out} ({len(s['sharedBrief'])} chars)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
