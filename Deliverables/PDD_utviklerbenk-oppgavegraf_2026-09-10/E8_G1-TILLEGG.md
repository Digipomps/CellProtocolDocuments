# E8 — G1-tillegg: eierens spørsmål og ventende porter har ett sted å bo

Oppgavemappe: `PDD_utviklerbenk-oppgavegraf_2026-09-10` · Tillegg opprettet 2026-09-29 · **Iterasjon 1 (G1 venter)**

Dette er det avgrensede G1-tillegget som E8 i FORMAALSSPEC §1 sier er neste steg.
G1 (14.09) og G1-GUI (15.09) dekker **ikke** dette. Ingen plan, ingen kode og ingen
GUI-implementering før G1 og G1-GUI er gitt på nettopp dette tillegget.

## 0. Intensjon (ordrett)

> **2026-09-29, Kjetil:** «Vi må ha dette opp i developer workbench så det ikke blir
> hengende på noe du har spurt om langt inne i loggen. Husk at funksjonalitet som ikke
> kommer ut til brukerene ikke eksisterer.»

> **2026-09-28, Kjetil:** «Spørsmålslister skal kunne vises og besvares i utviklerbenken.
> Formålet er at en beslutning tatt av eieren skal ha ett sted å bo, fra den stilles til
> den er ført inn i det den påvirker.»

> **2026-09-16, Kjetil, om raden «PR #242 hjelpertre — konflikten er løst, venter på push»:**
> «her burde det vært en knapp eller bedre forklaring på hva jeg skal gjøre.»

### Målingen som utløste tillegget (2026-09-29)

Seks PDD-er ble lest samme dag. **Alle seks har minst én port som venter på Kjetil, og
ingen av dem er synlig noe annet sted enn i en `STATUS.md`-fil eller i en chatlogg:**

| PDD | Hva som venter på ham |
|---|---|
| `scaffold-admin-delegering` | G3 — underlaget ble lagt fram 25.09, svar ikke gitt |
| `bro-paa-i-prod` | N07-metodevalg besvart 28.09; N12 venter på fysisk prøve med to iPhoner |
| `sindre-import-uten-bruker` | G3 |
| `palazzo-tolkning-og-vektjustering` | G3 |
| `palazzo-signalgraf` | G3 — og §3 er tom, så porten kan ikke gis som den står |
| `palazzo-raadgiverpanel-signalmatching` | G1 lå og ventet fra 26.09 til 29.09 |

Dette tillegget finnes fordi listen over er selve problemet, ikke et eksempel på det.
Bestillingen er ført inn fire ganger siden 14.09 uten at noe har nådd benken — det er
også en måling, og den hører hjemme her.

## 1. Formålstre — E8s blad

Forelder: `purpose://candidate.utviklerbenk.plangraf` · lokal kandidat:
`purpose://candidate.utviklerbenk.plangraf.sporsmallister` · status `candidate`.

**Rot for tillegget:** Eieren ser alt som venter på ham ett sted, vet hva han faktisk
skal avgjøre, og svarer der — uten å lete i en logg og uten at svaret må gjentas.

| Id | Blad | Observerbart mål | Verifier |
|---|---|---|---|
| **E8.1** | `…venter-paa-meg-er-synlig` | Hver port og hvert spørsmål som venter på eieren står som én rad i benken. Ingen rad krever at han har lest en tråd for å forstå hvorfor den er der. | `test.e8.alle-ventende-vises`: alle porter med status `venter` i PDD-mappene har nøyaktig én rad; antall rader = antall ventende porter |
| **E8.2** | `…raden-sier-hva-jeg-skal-avgjore` | Raden sier avgjørelsen, ikke bare at noe venter: hva som er levert, hva som ikke er det, og hva et ja betyr. En rad uten avgjørelsestekst vises ikke. | `test.e8.rad-uten-avgjorelse-vises-ikke` |
| **E8.3** | `…underlaget-er-ett-trykk-unna` | Raden peker på underlaget (ACCEPT.md, FORMAALSSPEC §3, bilde), og underlaget åpnes fra raden. | `test.e8.underlag-lenke-loeser` — hver lenke løser til en fil som finnes |
| **E8.4** | `…jeg-kan-svare-her` | Eieren svarer med listevalg **eller** fritekst når valgene ikke passer, fra raden. Anbefaling og eiersvar står tydelig atskilt; en anbefaling er aldri et avgitt svar. | `test.e8.svar-listevalg`, `test.e8.svar-fritekst`, `test.e8.anbefaling-er-ikke-svar` |
| **E8.5** | `…svaret-blir-foert-inn-og-kan-spores` | Et svar er ikke ferdig ved «besvart»: raden viser hva svaret ble ført inn i (hvilken fil, hvilken port, hvilken commit), og «ført inn» er en egen tilstand. | `test.e8.foert-inn-peker-paa-endring` |
| **E8.6** | `…listen-vedlikeholdes-ikke-for-haand` | Listen bygges fra kilden (portlinjene i `STATUS.md` og spørsmål registrert av tråder), ikke av at en tråd husker å oppdatere den. En gitt port forsvinner fra listen ved neste oppdatering. | `test.e8.ingen-spoekelser` — port satt til godkjent i kilden er borte fra listen etter oppdatering |
| **E8.7** | `…et-spoersmaal-kan-gjenaapnes` | Gjenåpning bevarer tidligere svar og viser at det er gjenåpnet. | `test.e8.gjenaapning-bevarer-historikk` |

**Anti-formål.** (a) Listen skal ikke bli enda et sted å vedlikeholde for hånd — da har
vi flyttet problemet. (b) Den skal ikke opprette nye statuser på `WorkItem`; spørsmålets
livsløp er sitt eget. (c) Den skal ikke kopiere svar til en ny beslutningsliste ved siden
av originalen — én sannhet, jf. E5. (d) Ingen rad skal vises som ikke faktisk venter på ham.

## 2. Avgrensning

Ikke i dette tillegget: plangrafen (E1–E6, egne porter fra 14.–15.09), tørrkjøring og
kommandokjøring fra kortet (K-E20–K-E23), fil-/celleimport (E7), og spørsmål som ikke
venter på **eieren** (andre tråders interne avklaringer).

Grense mot det som finnes: E3 eier handling og svarvei, E4 forklaring, E5 én sannhet og
bevis, E6 plasseringen i benken. Valgbenken viser valg, anbefaling og bevis; Dommerbenken
gir forståelige spørsmål og svar. E8 tilfører **livsløpet** og **sporbar innføring** — og
oppretter ingen av de andre mekanismene på nytt.

## 3. Forventningskontrakt — «Det du kommer til å se»

Én rad per leveranse. Etter G2 teller bare disse som fremdrift.

| Leveranse | Type | Hvor | Referanse | Godkjent |
|---|---|---|---|---|
| Rendret bilde: seksjonen «Venter på deg» i Developer Workbench, med én rad utvidet | bilde | `images/benk-venter-paa-deg-v1.png` | G1-GUI | nei |
| **Første skive, i drift:** hver ventende port fra PDD-mappene står som en rad i benken med avgjørelsestekst og lenke til underlaget | kjørende flate | Developer Workbench | E8.1–E8.3 | nei |
| Svar fra raden: listevalg og fritekst, med anbefaling atskilt | kjørende flate | samme | E8.4 | nei |
| «Ført inn»-tilstanden med peker til hva svaret endret | kjørende flate + testutdata | `TESTRESULT.md#foert-inn` | E8.5 | nei |
| Oppdatering fra kilden, uten håndarbeid, og uten spøkelsesrader | testutdata | `TESTRESULT.md#kilde` | E8.6 | nei |
| Akseptanse: forventning mot faktisk | fil | `ACCEPT.md` | — | nei |

**Første skive er valgt slik at den når deg før resten er ferdig.** E8.1–E8.3 alene
fjerner problemet du beskrev: at et spørsmål blir hengende langt inne i en logg.
E8.4–E8.7 følger etter, i samme benk.

## 4. Åpne spørsmål — de som endrer treet

- **Q-E8-1 · Hvor bor spørsmålet?** Forslag: som et `WorkItem` eid av Kjetil, med
  spørsmålets livsløp som egne felter — benken har allerede celle, flate og tilgang.
  Alternativet er en egen celle. Valget avgjør hvor mye som må bygges.
- **Q-E8-2 · Hvordan kommer portene inn?** `STATUS.md` ligger i CellProtocolDocuments på
  din maskin, ikke i scaffoldet som kjører i prod. Forslag: HAVEN Agent leser portlinjene
  lokalt og registrerer dem gjennom broen — samme vei som andre agentjobber. Alternativet
  er at tråder registrerer spørsmålet direkte når de stiller det.
- **Q-E8-3 · Er «ført inn» automatisk eller bekreftet?** Forslag: tråden som fører svaret
  inn markerer raden og oppgir hva den endret; benken viser det, men påstår ikke selv at
  noe er ført inn.

## Porter for dette tillegget

- **G1: godkjent 2026-09-29** (Kjetil, ordrett: «G1 og G1-GUI på tillegget er godkjent.»)
- **G1-GUI: godkjent 2026-09-29** — referanse `images/benk-venter-paa-deg-v1.png`
- **G2: godkjent 2026-10-01** (Kjetil, ordrett: «G2 på PLAN-E8.md er godkjent») — planen er
  `/Users/kjetil/Build/Digipomps/HAVEN/CellProtocolDocuments/Deliverables/PDD_utviklerbenk-oppgavegraf_2026-09-10/PLAN-E8.md`
- G3: venter

### Eiersvar på de åpne spørsmålene (2026-09-29)

- **Q-E8-1 og Q-E8-2 — «Vi trenger støtte for begge deler.»** Begge inntaksveiene skal
  finnes: HAVEN Agent leser portlinjene fra `STATUS.md` lokalt og registrerer dem gjennom
  broen, **og** en tråd kan registrere et spørsmål direkte når det stilles. De er ikke
  alternativer; en port som ingen tråd har registrert skal fortsatt komme fram.
- **Rekkefølge, ordrett:** «Først må HAVEN Agent ingeste jobber og ideer fra køer — og
  tråder i deg — Claude — og Codex.» Inntaket er derfor WP1, før flaten. Kilder som skal
  dekkes: Losen-køen (`_losen-queue`), Claude-tråder (Cowork og Claude Code) og
  Codex-tråder. Ideer teller som inntak på linje med jobber og spørsmål.
- Q-E8-3 (er «ført inn» automatisk eller bekreftet) er ikke besvart; planen skal legge
  den fram som et valg, ikke avgjøre den.

## 5. Avledede tester

`test.e8.alle-ventende-vises`, `test.e8.rad-uten-avgjorelse-vises-ikke`,
`test.e8.underlag-lenke-loeser`, `test.e8.svar-listevalg`, `test.e8.svar-fritekst`,
`test.e8.anbefaling-er-ikke-svar`, `test.e8.foert-inn-peker-paa-endring`,
`test.e8.ingen-spoekelser`, `test.e8.gjenaapning-bevarer-historikk`, pluss standardpakken
`test.build`, `test.regression`, `test.gui.parity`, `test.skeleton.no-unreachable-elements`,
`test.docs-updated`, `test.status-current`.
