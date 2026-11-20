# UX-vurdering av Studio-flaten (G1-GUI runde 2, 2026-11-18)

Kjetil, 18.11: «GUI-et ser helt forferdelig ut. Det må være enkelt og forståelig for brukeren og se elegant ut. Alle elementer skal ha et formål. Evaluer UX prinsipper.»

Runde 1 (`images/*-v1.png`) er vurdert mot prinsippene under. Runde 2 (`images/v2/`) er laget fra vurderingen.

## Prinsippene og hva runde 1 brøt

| Prinsipp | Runde 1 | Runde 2 |
|---|---|---|
| **Én oppgave, én hovedhandling per steg** | Seks knapper med lik vekt, og «Forkast» like tydelig som «Lag utkast». | Hvert steg har én blå hovedknapp: «Lag forslag», «Lagre», «Inviter» eller «Hent den nyeste versjonen». Alt annet er hvitt og sekundært. I konflikt er «Lagre» borte til du har hentet den nyeste versjonen. |
| **Brukerens språk, ikke systemets** | `cell:///Todo`, `todo.toggleTodo`, «revisjon 4», «nåbarhet». | Klartekst: «Henter fra gjøremålene dine», «Knappen Ferdig krysser av gjøremålet». Keypaths står bare under fanen «Slik er den bygget», for den som vil se. |
| **Vis status, ikke data** | Sjekken var en egen seksjon med en lang setning, også når alt var bra. | Ett merke, «Klar» (grønn) eller «Må rettes» (gul), og én overskrift. Detaljene ligger bak fanen. |
| **Gradvis avsløring** | Invitasjonsfelt, revisjonstekst og redaktørliste var alltid synlige. | «Del» åpner delingskortet. Konflikt-, resultat- og lagrelinjen vises bare når de gjelder. |
| **Resultatet er det viktigste** | Forhåndsvisningen lå tredje nederst, mellom sjekk og redaktører. | Forhåndsvisningen er hovedinnholdet i resultatkortet, i en egen ramme, og er standardfanen. |
| **Feil: si hva som skjedde, hva som er trygt, og hva du kan gjøre** | Tekniske funn, ingen vei videre. | «Én del av forslaget ville aldri vist seg», «Forslaget er ikke tatt i bruk» og én knapp: «Lag nytt forslag som retter dette». |
| **Ingen blindvei uten modell** | Tekst om manglende modell, uten noe å gjøre. | Samme kort gir opplasting av egen fil i stedet, med lenke til guiden. |
| **Samarbeid uten overraskelser** | «Revisjon 4 · sist lagret av Ola». | Topplinjen sier «Med Ola». Konflikten sier hvem og hva, og at teksten din ikke er tapt. |
| **Ro i uttrykket** | Mørkt tekstfelt på hvitt, liten tittel, like grå seksjoner. | Lyst lerret, hvite kort med 14 px hjørner, én blåfarge, tydelig tittel, dempet hjelpetekst. |
| **Mobil først** | Rader brøt ord midt i («morg-en»). | Tittel og frist står over hverandre, og knappen står til høyre. Merket brytes ikke. |

## Hvert element og formålet det tjener

| Element | Formål (§1) | Hvorfor det finnes |
|---|---|---|
| Tittel «Ny flate» og statuslinje | root | Hva dette er, og om det er lagret |
| «Med Ola» og «Del» | co-edit-draft | Hvem som er med, og én vei til å invitere |
| Konfliktkort (bare ved konflikt) | co-edit-draft | Ingen lagring overskrives uten at du ser det |
| Delingskort (bare etter «Del») | co-edit-draft, discuss-draft | Inviter en navngitt person, eller del lenke i samtale |
| «Hva skal flaten gjøre?» med tekstfelt | model-draft | Beskriv med egne ord |
| Modellinje «Mistral Small · EU» | model-route | Hvem som lager forslaget, og hvor |
| «Lag forslag» | model-draft | Hovedhandlingen i steget |
| Opplasting (bare uten modell) | model-route, guide | Vei videre uten modell |
| Merke og overskrift | studio-audit | Virker forslaget eller ikke |
| «Lag nytt forslag som retter dette» (bare ved funn) | studio-audit, model-draft | Én handling ut av feilen |
| Fanen «Forhåndsvisning» | model-draft | Se resultatet før du lagrer |
| Fanen «Slik er den bygget» | public-skill-current, studio-audit | Data og handlinger for den som vil lære formatet |
| «Forkast» og «Lagre» (bare med ulagret utkast) | root | Avslutt steget |

Fjernet fra runde 1, fordi de ikke tjente et formål for brukeren: Studio-navnet som tittel, revisjonsnummeret, den alltid synlige sjekkseksjonen, den alltid synlige invitasjonen, «Utkast laget»-meldingen og den doble forklaringen av forslaget.

## Hva som er web, og hva som virker i appen

- Farger, hjørner, kanter, skrift og avstand ligger som modifikatorer i skjelettet (`skeleton/studio-hjelp-v2.skeleton.json`). Dette er CellBase-felt, så CellApple (Binding) leser de samme verdiene. Det er **ikke sett i Binding ennå**.
- `theme/Cell Configuration Studio.css` gjelder bare vertsrammen og webklassene (fanelisten, standardknapper, seksjoner), samme mønster som `themes/Questionnaire Campaign.css`. Flaten skal virke uten den.
- Rader som kommer og går, er lister med null eller én rad som cellen fyller, ikke betingelser på toppnivå.
- Forhåndsvisningen er tegnet rett inn i resultatkortet. Den ekte innbyggingen skal gjøres i WP5.

## Nytt funn

Eksempelutkastet hadde rader som brøt ord på mobil. Det er rettet i utkastet og i studentguiden. Modellprompten i WP5 skal be om rader der tekst står over hverandre og knappen til høyre.
