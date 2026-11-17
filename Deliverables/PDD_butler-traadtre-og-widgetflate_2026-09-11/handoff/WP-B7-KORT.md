STATUS: VENTER PÅ G1-GUI — bildene av kortene må godkjennes av Kjetil før implementering

# WP-B7 — Kortene i chatten og widgetene på Flaten rundt (vei B)

Kjetils valg 2026-09-20: neste steg mot mockupen er kortene i chatten og på Flaten rundt, som
`ComponentSurface` per rad (`instanceIDKeypath`), fylt av kildecellen. Kilder: **begge** —
deltakerens Arendalsuka-program først, deretter sponsoroppfølgingen, med samme kontrakt.

## Hva bildene viser (G1-GUI)

Rendret uten server i Chromium med web-rendereren slik den står etter WP-F1 web og WP-B6, Butler-
skjelettet fra fabrikken (WP-B5) med de to malene byttet ut, og temaet `Co-Pilot Chat.css`.

| Bilde | Innhold |
|---|---|
| `images/kort/web-kort-v1.png` (2000 × 1250) | Agendakortet i loggen (med Fest), endringskortet på Butlers siste svar (Avvis i hodet, «Legg til i agenda» inne i kortet), to widgets på Flaten rundt: «Min agenda — Arendalsuka» og «Sponsoroppfølging». |
| `images/kort/web-kort-bekreftet-v1.png` (2000 × 1250) | Etter «Legg til i agenda»: endringskortet viser «✓ Lagt til i min agenda», og **begge** agendakortene (i loggen og på Flaten rundt) har fått den nye raden fordi de leser samme kilde. «oppdatert 09:27». |
| `images/kort/web-kort-1440-v1.png` (1440 × 900) | Samme som det første, på en vanlig bærbar skjerm. |

Kandidaten er bygget av `HAVEN-Deploy/_handoff/WP-R/b7/bygg-kort.py`; skjelett og tilstand ligger
i `skeleton/kort.skeleton.json`, `skeleton/kort.state.json` og `skeleton/kort-bekreftet.state.json`.

## Hvem eier hva

- **Butler (verten)** eier rammen rundt hvert kort: tittel, grep (⠿), Fest, Avvis, ⤢, ✕ og
  «Fra: … oppdatert HH:MM». Dette er vertens handlinger og står utenfor definisjonen.
- **Kildecellen** eier innholdet: definisjonen (`skeleton`, likt for alle instanser, med
  `componentID` og `revision`) og dataene (`item`) for hver instans. Knappene inne i kortet går til
  kildecellen med brukerens egen identitet (ruten fra WP-R2c), aldri via Butler.

Monteringen per rad (SKJELETT_ELEMENTER.md §2.2):
`{componentID, revision, sourceCellEndpoint, skeleton, item}` på radens `mount`, og radens
`id`/`instanceID` er instansidentiteten (`instanceIDKeypath`).

| Kort | Kildecelle | Definisjon (`componentID`) | Kildehandling i kortet |
|---|---|---|---|
| Min agenda | `cell:///ArendalsukaParticipantProgram` | `arendalsuka.agenda-card` | ingen |
| Endring — min agenda | `cell:///ArendalsukaParticipantProgram` | `arendalsuka.agenda-change` | `participant.toggleSavedSession {sessionID}` |
| Sponsoroppfølging | `cell:///ConferenceSponsorPreviewShell` | `conference.sponsor-followup` | ingen i første omgang |

Begge kildecellene er `identityUnique`: hver bruker har sin egen instans og er eier av den, så
Butler kan lese med brukerens identitet uten ny avtale.

## Avvik fra mockupen (bevisst, etter Kjetils valg av kilder)

- Mockupen viser en arrangørvisning (rom og innledere per sesjon). Den finnes ikke i noen celle.
  Kortet viser i stedet deltakerens egen agenda (tittel, tid, sted).
- Mockupens «Sponsorstatus» (Signert / Venter på svar / Scenetid) er en arrangørvisning av
  sponsorer. Kilden som finnes er sponsorens egen oppfølging av leads: hentet opp, kvalifisert,
  kontakt låst opp. Tallene i bildet er eksempeltall.
- Endringskortet har «Legg til i agenda» og Avvis, ikke Bekreft / Endre / Avvis: programcellen har
  ingen «endre»-handling for et arrangement.

## Hva som bygges etter G1-GUI (forslag til plan)

1. Kildecellene leverer definisjon og data: `component.agendaCard`, `component.agendaChange`
   (for et foreslått arrangement) og `component.followUp`.
2. Butler legger `mount` på radene (widgetene og kortene i loggen) ved projeksjon, lest fra
   kildecellen med brukerens identitet; siste kjente `item` og feilteksten vises hvis kilden ikke
   svarer. Skjelettet får de to malene i bildet.
3. Tester avledet av formålene: kildehandlingen i kortet endrer programcellen og går ikke via
   Butler; begge agendakortene viser den nye raden uten ny innlasting (B2); Avvis og Fest går til
   Butler; auditen ser de oppløste definisjonene (B4); T-P2 mot lokal testvert med skjermbilder.
