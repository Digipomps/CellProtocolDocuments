# Oppgave: skriv meldinger som IKKE skal utløse noe formål i HAVEN

HAVEN er en norsk plattform fra stiftelsen Digipomps der folk har sine egne data og får hjelp av assistenter i chat
(Butler: prosjekter/oppgaver/kontakter/møter/spørreundersøkelser; Kallimachos: bibliotekar, kilder, allmenningen;
Onboarding: personvern, egne data, regler; Hjelpechat: når noe ikke virker).

Vi tester at en regelbasert assistent IKKE foreslår noe når meldingen ikke hører hjemme der. Skriv som personaen under.

Skriv 72 meldinger, 18 av hver type, fordelt jevnt på flatene butler, kallimachos, onboarding, hjelp:
- `smaaprat`: takk, kommentarer, opplysninger uten forespørsel, «bare tenker høyt», «ikke gjør noe med det ennå».
  IKKE hilsener (hei), IKKE ja/nei/ok, IKKE «hvem er du» — det er egne formål.
- `utenfor`: reelle ønsker som ligger helt utenfor HAVEN (vær, pizza, oversette bok, aksjetips, oppskrift, sportsresultat).
- `spoerreord`: spørsmål som bruker typiske spørreord og ord fra HAVENs verden, men i et irrelevant domene. Eksempelvis
  «hvor lenge» om matlaging, «hvem har tilgang» om et treningssenter, «kan jeg slette» om en app i en butikk, «hva er
  reglene» i fotball, «hvor lagres» om poteter i kjelleren. Lag dine egne, varier spørreordene.
- `uklart`: genuint underbestemt uten kontekst: «fiks det», «den greia fra i går», «samme som sist».

Format, skrevet med Write til filen i oppdraget:
`[{"type": "smaaprat"|"utenfor"|"spoerreord"|"uklart", "flate": "...", "tekst": "..."}, ...]`
Les filen tilbake og sjekk at den er gyldig JSON. Svar bare med antall. Ikke kall mcp__hearthbot__-verktøy.
