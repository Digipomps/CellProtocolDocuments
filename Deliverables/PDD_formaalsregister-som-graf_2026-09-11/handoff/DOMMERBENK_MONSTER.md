# Dommerbenken — mønsteret, så det kan bygges i HAVEN

Skrevet 2026-09-14 av Losen, samme økt som Kjetil sa «dette bør inn i developer workbench».
Artefaktet selv er HTML på claude.ai (db-samling `dommer`). Dette notatet er det som skal overleve
artefaktet. Stier relative til `HAVEN/`.

## Hva det er

En **vurderingsflate**: et menneske dømmer kandidater mot ett synlig kriterium, én sak om gangen, og
hver dom lagres i det den avgis. Ingen sende-knapp, ingen notasjon, ingen statistikk i skjemaet.

## De sju egenskapene som gjorde at den virket

| # | Egenskap | Hvorfor den betyr noe |
|---|---|---|
| 1 | Kriteriet står synlig hele tiden, over radene | Dommeren skal aldri måtte huske hva spørsmålet var |
| 2 | Én sak om gangen, med forrige/neste og prikkerad for tilstand | Femten saker på én side dreper dommen etter den sjuende (målt: 7 094 s → 25 s) |
| 3 | Tre knapper per rad — ja / nei / usikker — som kan angres | «Usikker» er et ærlig svar; uten den blir det ja |
| 4 | Full tekst per rad, aldri avkortet | Avkortet tekst gir dom på overskrift |
| 5 | Ett valgfritt notatfelt per sak | Det var her det ekte signalet kom («nevnt før») |
| 6 | Lagring per klikk, med synlig status | Ingen «send», ingenting å miste |
| 7 | Tid per sak målt automatisk | Feltet «sekunder=…» forsvant; tallet ble bedre |

## Grunnregelen (Kjetil 2026-09-14, ordrett)

> Når vi bygger GUI for dette må det være lett å forstå både spørsmålet og hva eller hvordan man skal svare.

Konkret, og testbart:

| Krav | Hvordan det ser ut | Hvordan det brytes |
|---|---|---|
| Spørsmålet er én setning, synlig hele tiden | «Ville forebyggingen endret et konkret valg, en test eller en avgrensning i *denne* oppgaven?» øverst, aldri rullet bort | Spørsmålet står i en innledning tre skjermer opp, eller som statistikk |
| Svaret står i knappen | «Ville endret noe» · «Nei» · «Usikker» | «Ja» · «1» · «?» · `3=u:sann-grunn` |
| Ingen notasjon, kode eller tall i det dommeren ser | Full tekst, klartekst | `R+@10`, `s_d=0,30`, snapshotHash i skjemaet |
| Første dom uten instruksjon, innen ett minutt | Åpne → lese → klikke | Må spørre tilbake hva som menes |

Verifier: `test.gui.forstaa-uten-instruksjon` — en førstegangsbruker får flaten uten forklaring og skal
kunne gjengi spørsmålet og avgi første dom. Ett spørsmål tilbake = rød. Kjøres før hver runde på en ny
flate. Runde 1 målte begge utfall: den første blanketten feilet, den omskrevne besto.

## Det som IKKE virket, og som mønsteret må ta med seg

- **Uten lokkeduer blir alt ja.** Kandidatene må blandes blindt med rader hentet utenfor treffmengden,
  ellers har «nei» ingenting å feste seg til. Dette er ikke en egenskap ved flaten, men ved *utvalget*
  som legges i den — og flaten må kunne ta imot merkede lokkeduer uten å vise merket.
- **Kriteriet «ville endret noe» er for løst.** Neste versjon: «nevn hvilket valg, hvilken test eller
  hvilken avgrensning». Et navn, ellers nei.
- **Maks fem saker per økt.** Tidskurven bestemmer det, ikke smak.

## Det runde 2 (chat, 2026-09-28) lærte

Flaten: «Dommerbenken — chat» v2, 30 saker. Funn: `maaling/natt-2026-09-23/DOMMER_RUNDE2_FUNN.md`.

- **Skriv først, velg så.** Kjetil skrev med egne ord hva han mente *før* alternativene ble vist, i alle 30
  sakene (median 7 ord, 34 s). Friteksten ga mer enn valget: dekomponeringer («verb → formål, objektet i
  Perspective»), kontekstreferanser i seks saker, og forklaringen på hver uenighet. Ingen gjennomklikking.
  Tretti saker gikk bra med to trinn; fem-per-økt-regelen gjaldt ja/nei-rader og står for dem.
- **Alltid like mange alternativer.** Fylles opp (gold-søsken, skopnoder, øvrige), stokkes, gold alltid med.
  Et alternativ som står alene, er en etikett, ikke et valg.
- **«Uklart — trenger kontekst» er et eget svar**, adskilt fra «Ingen av disse». Brukt én gang, men det skiller
  «intet formål» fra «kan ikke avgjøres».
- **Plassholder og eksempler må ikke ligne noen sak.** Eksempelet «status på prosjektet» ble ordrett svaret i to
  saker (`lesson.placeholder-example-leaks-into-judgement`).
- **Når ingen alternativer passer, velges noen ganger det nærmeste ordet** («nei» → *acceptance*). Utfylte
  lokkeduer bør derfor også omfatte noder med *ordlikhet* til ytringen, så slike valg kan oppdages.

## Det runde 3 (Butler-korpus, 24.–29.09) lærte

Flaten: «Dommerbenken · Butler-korpus», 52 saker i to deler og elleve økter à fem. Resultat:
`PDD_butler-onboarding-og-formaalsforstaaelse_2026-09-23/maaling/dommerbenk/RUNDE1-RESULTAT.md`.

- **To svartyper i samme flate virket.** Del A: velg blant to etiketter, «Ingen av dem» eller «Usikker». Del B: ja, nei eller usikker. 47 saker gikk på én dag. Median 76 s per sak i del A og 37 s i del B.
- **Lokkeduene holdt: 7 av 9 ble avvist.** De to som slapp, lærer noe. (1) Nærmeste ord: «point me toward people» ble H.invite der fasiten er nettverk — samme mønster som i runde 2. (2) Formell norsk («Jeg ønsker herved å registrere en idé …») ble dømt realistisk. En realisme-lokkedue må være kunstig på en måte som ikke også er ekte, formell norsk.
- **Notat uten valg er et svar.** Én sak fikk bare notat. Flaten bør ha det som eget valg («Beskrevet i notatet»), ellers står saken halvt besvart.
- **Notatet traff fasiten der valgene ikke gjorde det.** I fire av fem lokkeduer skrev dommeren selv riktig handling. Notatfeltet er hovedsignalet, ikke et tillegg.
- **Dommeren ser feil i metadata.** Meldinger med «Æ» var merket bokmål; dommeren skrev at det er nynorsk eller dialekt. Flaten bør vise metadata (språk, stil) og ha et eget felt for å flagge det.
- **Notatene går utover etikettsettet** (flere behov i én melding, kontekst fra Perspective, brukerens tekniske nivå). Flaten bør la dommeren foreslå et nytt formål, som blir en kandidat i formålsregisteret, ikke bare fritekst.
- **Fra dom til fasit var håndarbeid.** Db-eksport, kobling mot nøkkelen og skriving til `fasit-v1.jsonl` ble gjort med skript i en Claude-økt. I HAVEN skal lukking av runden skrive gullfasiten som hendelser direkte, og nøkkelen skal holdes av cellen til runden er lukket. Her ble den åpnet først etter svar 52 av 52.

## Slik bygges det i HAVEN

**Skeleton** (innenfor dagens format, jf. `cellconfiguration-skeleton-authoring/references/schema-and-limits.md`):

- `Text` for kriteriet (øverst, `styleRole` framhevet)
- `Text` for framdrift («12 av 197 vurdert») — det finnes ingen stolpe-element; tekst holder
- `List` over kandidater med `flowElementSkeleton` = `VStack` av `Text` (ref), `Text` (forebygging),
  `Text` (symptom), og `HStack` med tre `Button` som hver har `keypath` mot cellen og `payload`
  `{ "kandidat": "<ref>", "verdikt": "ja" | "nei" | "usikker" }`
- `TextArea` for notat, `targetKeypath` mot cellen
- To `Button` for forrige/neste, `keypath` mot cellen

**To hull i skeleton-formatet, som ikke skal improviseres:**

1. Ingen tidtaker-element. Tiden måles av **cellen**: tidsstempel på hver mottatt dom, differanse til
   forrige handling i samme sak. Ikke i flaten.
2. «Trykket»-tilstand på en knapp er bare `styleRole`/`styleClasses` — metadata, ikke garantert
   styling. Skal vises som tekst i tillegg («valgt: ja») til rendereren støtter det.

**Cellen** (`cell:///Dommerbenk`, eller en del av workbench-cellen):

- Eier dommene under eier-scopede Grants (`rwxs`). Bare dommeren skriver; den som satte opp runden
  leser. Ingen dom er tilgjengelig for den som laget kandidatlisten før runden er lukket — ellers
  lekker fasiten inn i metoden som skal måles mot den.
- **En dom er en hendelse, ikke en tilstand:** `(runde, sak, kandidat, verdikt, sekunder, notat,
  tidsstempel, dommer)`, append-only, replaybar, i samme form som `RelationalWeightUpdateEvent`.
  Det er dette som gjør at en dom senere kan flytte en vekt — jf. `FORMAALSSPEC.md` §6 Q8.
- Lukking av en runde er én handling, og først da får den som bestilte runden lese.

**Første bruk:** fasit for formålsoppslag (denne PDD-en, WP12).
**Neste:** G3-akseptanse rad for rad (forventet → faktisk, godkjent/avvik/grunn), og «ville denne
lærdommen endret noe» ved P6 — som er hendelsen som skal justere lærdommers vekt over tid.

## Hvor det er registrert

- Kjetils ord ordrett i `PDD_utviklerbenk-oppgavegraf_2026-09-10/FORMAALSSPEC.md` §0, med tre
  auditrader. Kandidatnode `purpose://candidate.utviklerbenk.dommerbenk`. Ikke dekomponert — den
  PDD-en venter på G1.
- Rådata fra runde 1: `maaling/dommer_runde1.json`. Funn: `maaling/DOMMER_RUNDE1_FUNN.md`.
