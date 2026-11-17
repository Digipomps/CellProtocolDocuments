# Kjetils svar på de seks spørsmålene — 28.09.2026

Ordrett gjengitt, med det som følger av hvert svar. Dette er G1-svaret; implementasjonen skal
måles mot dette.

## 1. Hva er et vedlegg?

> «Alle tre må støttes. Er det ikke mulig for begge å nå referansen, må vi få den overlevert til
> brukeren på en annen måte for eksempel hente ved behov, men fil som kopieres indikerer at
> sender ikke vil ta kostnaden med å lagre det selv (Kanskje spørre om den skal slettes hos
> sender?) eller om det er en fil som er utenfor hva en celle kan få tak i.»

**Alle tre modusene støttes**, og valget mellom dem er ikke vilkårlig — det følger av hva som
faktisk er mulig:

| Modus | Når den gjelder |
|---|---|
| **referanse + grant** | begge parter når referansen. Førstevalget: ingen kopi, ingen duplisering |
| **hent ved behov** | referansen er ikke nåbar for mottaker, men filen bor hos avsender |
| **kopi** | filen er utenfor det en celle kan nå, eller avsender vil ikke bære lagringskostnaden |

Kopi er altså ikke en latskapsvei — den er svaret når de to andre ikke er mulige. Implementasjonen
skal velge modus ut fra nåbarhet, ikke la avsender velge fritt, og skal si hvilken modus som ble
valgt og hvorfor.

## 2. Hvem lagrer bytene?

**Avsenders celle. Mottaker henter.** Det gjør tilbakekall mulig.

## 3. Retensjon

**Vedlegget dør med meldingens `retentionSeconds`.** Mottakeren mister aldri noe han hadde.

## 4. Størrelsesgrense

**Ingen. Send det som chunks.** `AttachmentStreamV1` er allerede chunket med autentisert
avslutning.

## 5. Hva mottakeren ser før nedlasting

**Navn, type, størrelse.** Ikke hash — hash før nedlasting lekker at mottaker har akkurat den
filen.

## 6. Binding

**`messageID` + avtale-id, signert, verifisert ved henting.** En strøm skal ikke kunne flyttes
mellom kontekster.

## Avklart 29.09: sletting hos avsender gjelder bare kopimodus

Kjetil: «var tenkt bare om den sendes som kopi via vedlegg — vi kan ha funksjonaliteten og så
kan evt brukeren svare hver gang eller sette en policy.»

Altså:

- gjelder **bare** i modus `copy`. I `reference` og `fetchOnDemand` finnes ingen kopi å slette.
- funksjonaliteten skal finnes
- eieren svarer per sending, eller setter en policy som svarer for ham

### Hva det gjør med svar 2 og 3, og hvordan det håndteres

Sletter avsender sin kopi, er det ingen igjen hos avsender. Da gjelder ikke lenger «avsenders
celle lagrer» (svar 2) og heller ikke «dør med meldingen» (svar 3) — det finnes ikke noe igjen
å la dø.

Det er ikke en motsigelse, det er en **overdragelse**. Vedlegget slutter å være noe eieren kan
trekke tilbake, og blir mottakerens. Retensjonen gjaldt avsenders kopi, og den er borte.

Implementasjonen skal derfor:

- behandle sletting hos avsender som et eget, navngitt skritt: fra tilbakekallbart vedlegg til
  overdratt fil
- si det til eieren i de ordene, i øyeblikket han velger — ikke som «slett hos meg?», men som
  «da kan du ikke trekke den tilbake, og den dør ikke med meldingen»
- kreve at mottaker faktisk har hentet strømmen før avsenders kopi slettes. Sletting før
  henting er tap uten mottaker.
- la en policy sette standardsvaret, men aldri skjule overdragelsen for en eier som ikke har
  satt policy

Dette er Losens lesning av svarene, ikke et eget vedtak. Er overdragelsesrammen feil, si fra.

## Løst — tidligere åpent punkt

Kjetil reiste selv spørsmålet: «Kanskje spørre om den skal slettes hos sender?»

Det kolliderer med svar 2 og 3. Slettes kopien hos avsender, er det ingen igjen som lagrer den,
og modus «kopi» blir da i praksis «mottaker lagrer» — motsatt av svar 2. Og dør vedlegget med
meldingen etter at avsender har slettet sitt, er filen borte helt.

For en meldingsvedlegg kan det være riktig. For den eneste kopien av et budsjett er det et
datatap.

**Avklart 29.09.** Se avsnittet over.
