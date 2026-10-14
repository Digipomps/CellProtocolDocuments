# Runde 2: skjerp formålsbeskrivelsene etter målte feil

Du skrev i runde 1 norske erklæringer for formålene i HAVENs register (beskrivelse_no, uttrykk, handlinger, objekter,
sporsmaalsord). En regelbasert matcher uten språkmodell bruker dem: TF-IDF over formålstekst + nøyaktig frasetreff på
`uttrykk` + løft når både et verb fra `handlinger` og et ord fra `objekter` står i meldingen + en dekningsregel (meldinger
med mange ord registeret ikke kjenner, får lav score) + terskel.

Nå er erklæringene målt på meldinger fra sju skribenter og et sett med irrelevante meldinger. For hvert formål får du:
- `naa`: erklæringen slik den står
- `riktig_truffet`: meldinger som traff riktig (ikke ødelegg disse)
- `bom_ble_til`: meldinger som HØRTE til formålet, men matcheren valgte et annet
- `for_lav_score`: riktig formål, men under terskelen (mangler ord)
- `stjal_fra_andre`: meldinger som hørte til et ANNET formål, men matcheren valgte dette (erklæringen er for vid)
- `falske_treff_paa_irrelevante`: irrelevante meldinger som feilaktig traff dette (erklæringen har for generelle ord)

Skriv en forbedret erklæring per formål. Regler:
- Generaliser. Ikke kopier navn, steder eller detaljer fra meldingene, og ikke lim inn hele meldinger som uttrykk.
  Målet er at NYE mennesker som skriver annerledes skal treffes.
- Legg til ord og fraser som manglet i `bom_ble_til`/`for_lav_score`, når de er typiske for formålet og ikke for naboen.
- Fjern eller gjør mer spesifikke de uttrykkene/ordene som forklarer `stjal_fra_andre` og `falske_treff_paa_irrelevante`.
  Enkeltord som «regler», «kilder», «data», «dele», «tilgang» er farlige alene; foretrekk fraser med HAVEN-kontekst.
- `beskrivelse_no` skal skille formålet fra naboene den forveksles med, med de ordene brukerne faktisk bruker.
- Bokmål og nynorsk. 12–35 uttrykk, 4–12 handlinger, 4–15 objekter.

Returner JSON (Write) til filen i oppdraget, samme skjema som runde 1:
`[{"ref":"…","beskrivelse_no":"…","uttrykk":[…],"handlinger":[…],"objekter":[…],"sporsmaalsord":[…],"usikker":false,"endret":"én setning om hva du endret og hvorfor"}, …]`
Én rad per formål. Les tilbake og kontroller gyldig JSON. Bare Read/Write. Ikke kall mcp__hearthbot__-verktøy. Svar kun med antall rader.
