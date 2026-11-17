# Natt 2026-10-07: AI-løs formålsforståelse, målt

Oppdrag (Kjetil 2026-10-07): «Kjør flere iterasjoner med rådgiverne om naturlige spørsmål, bruk Fables tolkning til å tune
formålsbeskrivelse og dekomponering … test med alle triks vi har. Få det målbart bedre.»

## Kort svar

Det ble målbart bedre på meldinger skrevet ut fra formålslista, men ikke nok på det uavhengige Butler-korpuset.

| Sett | Mål | R4 (frossen, 23.9) | R5 runde 3 (frossen i kveld) |
|---|---|---|---|
| Forseglet S1–S4 + NS, sølv (581 ekte / 70 neg) | top1 ved frossen terskel | 0.212 [0.177–0.244] | **0.749 [0.713–0.785]** |
| samme | negativer som fikk flateforslag | 22.9 % | 17.1 % (mål var ≤ 10 %) |
| samme | top1 når terskelen settes så negFA ≤ 10 % (kurve, rapport) | 0.165 | 0.683 |
| samme, alle rader (ikke bare der Fable var enig) | top1 | 0.206 | 0.735 |
| McNemar på forseglet sølv | R4 vant / R5 vant | 12 | 324 (p ≈ 5e-80) |
| Butler korpus v2 (uavhengig, etikett-kart v1.1) | top1 | 3/112 | **13/112** |
| samme | negFA | 12.5 % | 4.2 % |
| Kjetils egne vurderinger, ytring | top1 | 9/26 | 16/26 |
| Kjetils egne vurderinger, fritekst | top1 | 4/26 | 9/26 |

Forseglingen var intakt (sha256 kontrollert) og forseglet sett ble kjørt én gang, etter at variant og terskel var frosset
i `VALGT.json`.

## Hvordan

1. Rådgiverpersonaer skrev naturlige meldinger mot 77 mål (to per formål, kort og naturlig stil), 13 skribenter totalt.
   Negativer i fire typer (småprat, utenfor, spørreord-feller, uklart).
2. Fable tolket alle 3194 meldinger blindt med opake koder (vet ikke hvilket formål generatoren siktet mot). Sølv = der
   Fable og generatoren er enige.
3. Fable skrev norske erklæringer per formål: `beskrivelse_no`, `uttrykk`, `handlinger`, `objekter`, `sporsmaalsord`.
4. Fable skjerpet erklæringene to ganger fra målte feil (bom, for lav score, stjal fra andre, falske treff på negativer).
5. Hver runde ble målt på en NY skribentgruppe som ikke var brukt til tuning.

| Runde | Tunet på | Målt på (fersk) | top1 @ negFA ≤ 10 % |
|---|---|---|---|
| R4 frossen | — | DEV4 | 0.171 |
| Runde 1 (Fable fra register) | T1–T4 | DEV3 / DEV4 | 0.758 / 0.767 |
| Runde 2 (skjerpet) | T, D | DEV3 / DEV4 | 0.789 / 0.806 |
| Runde 3 (skjerpet igjen) | T, D, E | DEV4 | **0.820** |

Runde 3 mot runde 2 på DEV4 ved samme regel for terskel: 20 vunnet, 9 tapt, McNemar p = 0.06. Gevinsten per runde
flater ut (+4, +1.4 poeng). Runde 3 traff 0.952 på DEV3 som den var tunet på, mot 0.820 på fersk DEV4: resten er
generalisering, ikke flere ord.

## Hvilke triks bar (ablasjon på DEV3 med runde 2-erklæringer, top1 @ FA10, basis 0.789)

- Fable-`uttrykk` (frasetreff): 0.639 uten. Største enkeltbidrag.
- Dekningsregel (score × dekning², ord registeret ikke kjenner trekker ned): 0.730 uten. Løste avvisning av «HAVEN-klingende» irrelevante meldinger.
- Samtalehandlinger som egne formål som aldri foreslår flate (Kjetils avgjørelse 1): 0.761 uten.
- Verb + objekt slått opp hver for seg (Kjetils dekomponeringsregel, «frames»): 0.773 uten på DEV3, 0.786 uten på DEV4.
- Skop rangerer, men kan ikke alene løfte over terskel: 0.775 uten.
- Nøytralt (±1 poeng, innen støy): dialekt-normalisering, stemming, ordsplitt, trigram-fuzzy, spørreord-prior.
- Skadet og er slått av: setningsdekomponering (splitte i ledd og matche hver for seg), BM25, stemmet frasetreff,
  hints, automatisk utledet leksikon fra Fables bærende ord (overtilpasset).
- Uten Fable-erklæringer i det hele tatt: 0.053. Nesten alt kommer fra erklæringene, ikke fra matcheren.

## Det som ikke holdt

1. **Terskelen holdt ikke på forseglede negativer** (17 % mot mål 10 %). Spørreord-feller (28 %) og uklare
   («det der som vi snakka om, ordne det», 22 %) er verst. «Hvem har tilgang til garderoben på treningssenter» ga
   tilgangsformålet med høy score (0.78). Spørreord + ett domeneord er fortsatt for sterkt.
2. **Samtalehandlinger bommer når de er lange.** «Nei, det vil jeg ikke. Ikke gjør det» og «Ja det høres bra ut, bare
   gjør sånn» ga ukjent (score 0.07–0.14): de faller under terskelen fordi dekningsregelen straffer resten av setningen.
   17 av 146 forseglede bom er samtalehandlinger. Forslag (ikke målt): egen terskel for samtalehandlinger, siden de
   aldri foreslår flate. Må måles på dev før det tas i bruk.
3. **Butler v2 er fortsatt svakt (13/112).** Halvparten er engelsk, erklæringene er bare norske. Og hverdagsønskene
   («sett på lista mi», «få Hanne inn i denne tråden», «lag en avstemning», «sett opp styremøte tirsdag») har ikke et
   presist formål: kartet sender dem til nærmeste (koble to personer, utkast til møteforespørsel), og 117 andre meldinger i
   korpuset ber om noe registeret ikke har formål for. Det genererte korpuset ble skrevet ut fra formålslista, så det måler hvor godt
   vi forstår formål vi har; Butler v2 måler hva folk faktisk ber om. Avstanden er det viktigste funnet.

## Forbehold

- Alle tall unntatt Butler v2 og Kjetils sett bygger på genererte meldinger (Sonnet/Opus i persona). Én generator (G2)
  skrev med et skript og ble formelpreget («asså typ 🙂»); beholdt, men merket.
- Fable er både tolk (sølv) og forfatter av erklæringene. Tolkningen var blind (opake koder), men samme modell kan dele
  blindsoner. Kjetils 26 vurderinger og Butler v2 er de eneste helt uavhengige målene.
- 70 forseglede negativer gir vid usikkerhet på negFA (±9 poeng).
- Book 38-regler fulgt: delinger etter skribent, forhåndsbestemt valgmål, forseglet kjørt én gang, sølv og alle rader rapportert.

## Forslag til Kjetil (ingenting er skrevet inn i Book 23)

- `ERKLAERINGSFORSLAG_runde3.json`: Fables norske erklæringer for 86 formål, 3258 uttrykk, med kilde. Kandidat til
  erklært kilde for AI-løs matching. Dommen er din.
- Register v1-kandidater (fra avgjørelsene dine i dag): `conversation.open/accept/reject/introduce-self` (aldri flate),
  `librarian.propose-research-question`, `digital-work.export-to-file`, og `librarian.explain-haven` delt slik at
  presentasjon av AI-figuren er eget formål. Se `register_v1.py`.
- Nye kandidatformål som Butler v2 viser at mangler: legg til på oppgavelista, inviter person til tråd/prosjekt,
  lag avstemning, sett opp møte (ikke bare utkast). Ikke laget, bare foreslått.

## Neste steg jeg anbefaler

1. Erklæringer på engelsk for de samme formålene (Butler v2 er halvt engelsk).
2. Egen terskel for samtalehandlinger, målt på dev.
3. Hverdagsformålene over inn i registeret, så måle Butler v2 på nytt med nytt kart.
4. Spørreord-feller: krev at spørreordet står sammen med et HAVEN-objekt, ikke bare et domeneord.

## Filer

`maaling/natt-2026-10-07/kode_og_data/` (utpakket): `r5.py` (matcher), `abl4.py` (bygging), `eval7.py`/`curve.py` (måling),
`slutt.py` + `SLUTT_resultat.json` (forseglet kjøring), `VALGT.json` (frosset variant og terskel), `beskr_ut`,
`beskr2_ut`, `beskr3_ut` (erklæringer per runde), `gen/` (korpus), `tolk/fable.json` (Fables tolkning),
`FORSEGLET_sha256.txt`.
