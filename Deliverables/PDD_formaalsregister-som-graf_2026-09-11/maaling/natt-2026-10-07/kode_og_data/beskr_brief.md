# Tune formålsbeskrivelser for en matcher UTEN språkmodell

HAVEN har et formålsregister. En regelbasert matcher (BM25 over formålstekst + fraseoppslag + setningsdekomponering)
skal finne riktig formål for korte norske chatmeldinger. Den forstår bare ord den finner i formålets tekst. I dag er
beskrivelsene engelske og tekniske, så matcheren bommer på hvordan folk faktisk skriver.

Du får en fil med formål. For hvert formål: tittel, teknisk beskrivelse, forelder, eksisterende alias, noen
TRENINGSMELDINGER folk skrev for dette formålet (med din egen tidligere tolkning: handling, objekt, bærende ord), og
hvilke andre formål matcheren forveksler det med.

Skriv for hvert formål en erklæring som gjør det lettere å treffe riktig på NYE meldinger fra ANDRE mennesker:
- `beskrivelse_no`: 2–4 setninger på vanlig bokmål, i brukerens språk: hva vil folk som ønsker dette, og hva er det IKKE
  (skill det fra formålene det forveksles med).
- `uttrykk`: 12–30 korte, generelle fraser (2–5 ord) folk bruker om dette, på bokmål og nynorsk. Ikke kopier navn,
  steder, organisasjoner eller detaljer fra treningsmeldingene — generaliser («flytte styremøtet» → «flytte møtet»).
  Fraser som like gjerne kan bety et nabotformål, skal IKKE med.
- `handlinger`: 4–12 verb i infinitiv (bokmål og nynorsk) som typisk bærer dette formålet («slette», «sletta»).
  Bare verb som skiller dette formålet fra naboene; ikke «lage», «få», «gjøre» alene.
- `objekter`: 4–15 substantiv (grunnform og bestemt form der vanlig) som handlingen typisk gjelder.
- `sporsmaalsord`: spørreformer som peker hit når de står sammen med et objekt herfra («hvor lenge» + «lagret»). Kan være tom.

Ikke skriv noe for formål du ikke forstår — sett `usikker: true`.

Returner JSON (Write) til filen i oppdraget: `[{"ref":"purpose://…","beskrivelse_no":"…","uttrykk":[…],"handlinger":[…],"objekter":[…],"sporsmaalsord":[…],"usikker":false}, …]`, én rad per formål i inndata. Les tilbake og kontroller gyldig JSON. Bare Read/Write. Ikke kall mcp__hearthbot__-verktøy. Svar kun med antall rader.
