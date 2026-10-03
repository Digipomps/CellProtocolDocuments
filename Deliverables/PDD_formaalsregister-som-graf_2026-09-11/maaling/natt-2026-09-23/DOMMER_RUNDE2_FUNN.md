# Dommerrunde 2 (chat) — funn, 28. september 2026

Dommer: Kjetil, i «Dommerbenken — chat» v2 (skriv først med egne ord, velg så blant fem formål pluss «Ingen av
disse» og «Uklart»). 30 saker, lagret 13:38–15:58 UTC. Rådata med dine svar, mine etiketter, hva som ble vist og
R4s svar: `dommer_runde2_chat.json`. Stier relative til `HAVEN/`.

Dette er en **etikettrevisjon** av utviklingssettet, ikke en generaliseringsmåling (NATT_RAPPORT §8).

## Det korte svaret

1. **Du og jeg er enige i 21 av 30.** De ni uenighetene er mine etikettfeil — det var avtalen.
2. **Friteksten sa mer enn valget.** I seks av tretti forklarte du hva du mente ved å vise til kontekst:
   noe du har jobbet med, noe som står i Perspective, noe som var her før. Det er det første menneskelige
   belegget for `kontekst-ved-tynn-tekst`, i dine ord.
3. **Matcheren tåler ikke dine ord.** På de 22 sakene der du valgte et formål, traff den frosne R4 9 med mine
   ytringer, men bare **4** med dine egne formuleringer av samme mening. Den er tilpasset måten jeg skriver på.
4. **Din dom kolliderer med en regel i Book 38** (butler-tråden): der er småprat og spørsmål om assistenten
   selv «riktige når ingenting foreslås». Du ga «hei», «nei» og «hvem er du» et formål. Det må du avgjøre.

## Tallene

| | |
|---|---|
| Saker dømt | 30 av 30 |
| Enig med min etikett | 21 |
| Du valgte et formål / «Ingen av disse» / «Uklart» | 22 / 7 / 1 |
| Fritekst skrevet | 30 av 30 (median 7 ord) |
| Tid, trinn 1 (skrive) / trinn 2 (velge), median | 34 s / 16,5 s |
| R4 enig med *min* etikett / med *din* | 18 / 14 av 30 |

Mine etiketter fikk altså R4 til å se fire saker bedre ut enn din dom gjør.

Ingen tegn til gjennomklikking: alle tretti har fritekst, og trinn 1 tok 14–66 s også blant de ti siste
(sak 1 sto åpen i 6 493 s og er utelatt fra tolkningen av tid).

## De ni uenighetene, og hva de betyr

| Ytring (flate) | Min etikett | Ditt valg | Din fritekst |
|---|---|---|---|
| «hei» (butler) | intet formål | `contact.introduction` | En introduksjon eller start på en forespørsel. |
| «nei» (hjelp) | intet formål | `test.acceptance.project-work` | ikke - som for eksempel ikke godta en påstand. |
| «ja» (onboarding) | intet formål | Ingen av disse ✓ | Ok - dette går vi for |
| «foreslå et forskningsspørsmål» (kallimachos) | `librarian.commons-growth` | Ingen av disse | Foreslå en problemstilling å forske på |
| «ønske: eksport til regneark» (butler) | `capability.request-new-functionality` | Ingen av disse | Jeg ønsker å eksportere og laste ned regnearkdata til et filformat |
| «noen må se på dette» (butler) | `capability.request-human-review` | Ingen av disse | Lag en oppgave og deleger |
| «personvern» (onboarding) | `access.audit.privacy` | `self-determination.data` | GDPR og privat eide data |
| «hvordan vet vi at det ikke er funnet på» (hjelp) | `test.acceptance.hallucination-evaluation` | `self-determination.data.verifiability` | Presenter bevis for påstanden |
| «hvem er du» (kallimachos) | `librarian.explain-haven` | `contact.introduction` | fortell meg hva du driver med, hvilken rolle du har og om du vil eller har - navnet ditt. |
| «send skjemaet til de påmeldte» (butler) | `questionnaire.delivery.consent` | Ingen av disse | se under |

(«ja» er tatt med fordi friteksten gir den mening, selv om valget ditt og min etikett er like.)

De faller i fem slag:

**A. Samtalehandlinger — «hei», «ja», «nei».** Jeg merket dem «intet formål». Du ga dem mening: å åpne en
forespørsel, å godta, å avvise. Registeret har ingen formål for dette, og *hva* et «ja» eller «nei» gjelder,
finnes bare i det som er aktivt i perspektivet. For «nei» valgte du «Project work acceptance tests». Ingen av de
fem var et avvisningsformål, og jeg tror ordet *acceptance* bar valget — det er min tolkning, ikke din.

**B. Formålet finnes ikke i registeret.** «Foreslå en problemstilling å forske på» og «eksportere til et
filformat». Den siste leste jeg feil: jeg tok «ønske:» som et funksjonsønske, du leste det som noe du vil gjøre.

**C. Formålet finnes, men ble ikke vist.** «Lag en oppgave og deleger» hører hjemme i `project-work.work-items`
eller `digital-work.coordinate`. Ingen av dem var blant de fem, så «Ingen av disse» var riktig svar på det du så.
R4 fant `work-items` på friteksten din (0,19).

**D. Du valgte naboen.** «Personvern» er `self-determination.data` for deg, ikke tilgangsrevisjon. «Hvordan vet
vi…» er etterprøvbarhet for eieren, ikke hallusinasjonstesting. «Hvem er du» er introduksjon — men se spørsmål 2
nederst.

**E. «Send skjemaet til de påmeldte» — en dekomponering, ikke et valg.** Du skrev, ordrett: «send (verb ->
formål) skjemaet (hva som skal sendes - noe man aktivt har jobbet med eller er i Perspective av en annen grunn.)
til de påmeldte -> målgruppen, bør også kunne finnes i perspective i relasjon til skjemaet.» Og du valgte bort
`questionnaire.delivery.consent`. Slik jeg leser det: *verbet* gir formålet, mens *objektet* og *mottakeren* er
entiteter som slås opp i perspektivet. Det er to oppslag, ikke ett — formål i registeret, argumentene i
perspektivet — og det passer rett inn i keypath-formen vi valgte (`purposes[…].interests[…]`, entiteter ved
siden av).

## Friteksten: seks av tretti peker på kontekst

| Sak | Hva du skrev |
|---|---|
| send skjemaet til de påmeldte | «noe man aktivt har jobbet med eller er i Perspective» |
| hva er klokka | «i tidssonen jeg er i nå» |
| feltet er borte | «feltet jeg mente var her før» |
| bygg en konfigurasjon for menyen | «en meny jeg har nevnt eller jobbet med» |
| hvordan virker dette | «dette - som trenger kontekst» |
| hvor gjør jeg det | «som oppfyller "det"» |

I tillegg har sju av ytringene et pronomen som bare kontekst kan løse (*den, det, dette*). Det er dette 12.9-
målingen pekte på (0,111 → 0,404 med skop, n = 4, simulert). Nå sier en menneskedom det samme. Det er fortsatt
ikke målt at kontekst *hjelper matcheren* på ekte data — bare at du bruker den når du tolker.

## Matcheren på dine ord

| 22 saker der du valgte et formål | Mine ytringer | Dine fritekster |
|---|---:|---:|
| R4 treffer ditt formål | 9 | **4** |

| 8 saker uten formål | Mine ytringer | Dine fritekster |
|---|---:|---:|
| R4 avviser riktig | 5 | 5 |

Forbehold: friteksten din er forklaringer, lengre enn chatmeldinger, og skopvekten i R4 avtar med lengden. Det
er ikke en ren sammenligning, og n = 22. Men retningen er den samme som butler-tråden målte med nye skribenter
(Book 38 §4: +20 prosentpoeng på holdout ble +8 på et uavhengig korpus), og den samme som Astra advarte om.
R4 skal ikke brukes videre som den er.

Én node skiller seg ut: **`skeleton.owner-entity-access` vant fire av dine fritekster** (hvor lenge lagres det,
jeg kan ikke trykke på den, bygg en konfigurasjon, hvilke kilder) uten å høre hjemme i noen av dem. Det er samme
fenomen som `cellbase-decodingerror` i runde 1: en node som svarer på alt, bærer ingen informasjon. Vekten dens
bør synke — det er Oja-leddet (HD-0050).

## Feil i målingen som er mine

1. **Plassholderen lekket.** Eksempelet i skrivefeltet var «status på prosjektet». Du skrev nøyaktig det for
   «hvor står vi nå på prosjektet» og «hva står igjen». Eksempelet kom fra settet. Det kan ha ledet deg, og de to
   sakene teller derfor svakere. Neste gang: eksempler som ikke ligner noen sak.
2. **Utfylte alternativer ble valgt to ganger** («hei», «nei»), begge der ingen av de fem var et godt treff. For
   «hei» støtter friteksten valget; for «nei» tror jeg ordet bar det.
3. **Dette er utviklingssettet.** Alt over er etikettrevisjon og en indikasjon, ikke generalisering.

## Hva jeg har gjort

- Dine valg står som fasit for disse tretti (`gold_kjetil` i `dommer_runde2_chat.json`), mine etiketter ved siden.
- R4 er fortsatt frosset. Ingenting er justert på dine svar.
- Lærdom: `lesson.placeholder-example-leaks-into-judgement`. Mønsteret for Dommerbenken er oppdatert med det
  runde 2 lærte (`handoff/DOMMERBENK_MONSTER.md`).

## Hva du skal avgjøre

1. **Samtalehandlinger.** Skal «åpne», «godta», «avvise» og «presenter deg» være formål i registeret, der *hva*
   de gjelder hentes fra det som er aktivt i perspektivet? Book 38 regel 5 sier i dag at de er riktige når
   ingenting foreslås. Mitt forslag forener begge: de *er* formål (de har mening), men de foreslår aldri en flate
   — samme mekanisme som facet-only.
2. **«Hvem er du».** Friteksten din — «hva du driver med, hvilken rolle du har … navnet ditt» — passer ordrett med
   andre halvdel av `librarian.explain-haven` («explain the AI figure itself»), men tittelen begynner med
   «Explain HAVEN». Mente du introduksjon, eller lurte tittelen deg? Lurte den, er det det første konkrete
   argumentet for granularitet: én node som bærer to formål taper mot naboen fordi tittelen bare nevner det ene.
3. **Nye kandidatformål fra friteksten:** «foreslå en problemstilling», «eksportere til filformat», og regelen
   «verbet gir formålet, argumentene hentes fra perspektivet». Legge dem inn som kandidater?
4. **Uavhengig test av R4.** Butler-tråden har allerede et uavhengig korpus (264 meldinger, fire nye skribenter,
   `Deliverables/PDD_butler-onboarding-og-formaalsforstaaelse_2026-09-23/maaling/korpus/`). Det kan være den
   uavhengige testen Astra ba om — men etikettene er butlerens, så det trengs et etikett-kart (Book 38 regel 10).
