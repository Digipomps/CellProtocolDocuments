# Bilder

To bilder til G1-GUI. Kjetil godkjente dem 07.10.2026, ordrett: «4. Bildene er godkjent.» De viser forslaget om en kode på seks sifre.

| Fil | Viser | Formål i `FORMAALSSPEC.md` §1 |
|---|---|---|
| `godkjenning-paa-macen-v1.png` | Kortet under «Trenger deg» i adminvinduet til HAVEN Agent: en forespørsel som venter, lenken som lages, og tilstandene godkjent, avslått og feil | C2, C3, D3 |
| `mottaker-oppsett-v1.png` | Det mottakeren gjør: installere pakken, gi agenten sin lenken, sende koden. Og tilstanden «lenken er brukt eller utløpt» | C1 |

Kildene ligger i `kilde/` (`godkjenning.html`, `mottaker.html`).

## RENDERINGSERKLÆRING

Ingen av de to flatene er et HAVEN-skjelett. Kortet hører hjemme i adminvinduet til HAVEN Agent, som er en native macOS-app (appmålet `HavenAgentMenu`, planlagt slik i `Deliverables/PDD_agent-menylinje-og-varsler_2026-09-09/PLAN.md`, WP4 og WP5). Mottakerens oppsett er macOS' eget installasjonsvindu og en samtale med mottakerens egen agent. Det finnes derfor ingen `CellConfiguration` å rendre i Porthole, og mappen `skeleton/` brukes ikke. Bildene er tegnet som HTML og rendret til PNG i Chromium. Begge sier selv at de er skisser, ikke skjermbilder.

- Skrift, avstander, farger og vindusramme er tilnærmet. De er ikke målt mot macOS, og ikke mot adminvinduet slik det er i dag.
- Menyen til venstre i adminvinduet (Status, Identitet, Korrespondanse, Kontrollbro, Logg) er ikke holdt mot koden.
- Det er ikke lest om adminvinduet fra grenen `pdd/agent-menylinje-og-varsler` kan bære kortet, og hva som gjenstår for å få den grenen til `main`. Det står under «Det jeg ikke vet» i `FORMAALSSPEC.md` §6.
- Dialogen for Touch ID er macOS' egen og er ikke tegnet. Bildet viser bare knappene som utløser den («Lag lenke med Touch ID», «Godkjenn med Touch ID»).
- I mottakerbildet kommer teksten i boblene fra klienten. Hvordan mottakerens agent gjengir den, styrer ikke pakken.
- Koden `483 920`, navnet «Vegar», datoene, lenken og filnavnet med størrelse er eksempler.
- Bare disse tilstandene er tegnet. Hos eieren: forespørsel som venter, lenke laget, godkjent, avslått, og feil uten kontakt med cellen. Hos mottakeren: pakken installert, lenken gitt, post lest, og lenken brukt eller utløpt. Fornyelse, utløpt avtale og dialogen bak «Trekk tilgangen…» er ikke tegnet.
- Varsel på skjermen ved ny post er ikke med i første pakke og er ikke tegnet. I mottakerbildet spør mottakeren selv agenten om det er kommet post.
