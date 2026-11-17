# Regler for ordlistetrådene, runde 2 (7. oktober 2026)

Du skal foreslå ord. Restauranten Palazzo Communale (siciliansk, i Oslo) har en concierge på nettsiden som leser det gjesten skriver, uten språkmodell. Den kjenner ord igjen fra lister. Listene er gode på bokmål og nynorsk. De mangler mye av det folk faktisk skriver når de ikke skriver bokmål. Du foreslår det som mangler, ut fra det du vet om språk. Du får ikke se setninger gjester har skrevet, og skal ikke lete etter dem.

## Det denne runden gjelder

Skriv slik folk skriver i en chat, ikke slik det står i en ordbok:

- **Norsk talemål skrevet ned:** trøndersk («æ», «itj», «dokker», «te» for til, «nå» for noe, «mæ», «ka», «e» for er), nordnorsk, bergensk og vestlandsk («eg», «ikkje», «dokker», «kaffi»), sørlandsk, østlandsk («je», «itte»).
- **Svensk og dansk**, slik en gjest fra Sverige eller Danmark skriver til en norsk restaurant.
- **Engelsk slik turister skriver**, også muntlige vendinger («I'm in the mood for», «could go for», «not a big fan»).
- **Ungdom og chat:** forkortelser, bortfall («e» for er, «no» for noe, «d» for det), ord som «digg», «nice», «kjipt».

Tenk gjennom hver klasse for hvert av disse, ett om gangen.

## Hva som er et godt forslag

- Et ord eller uttrykk en gjest kunne skrevet.
- For emner og allergener: ordet må bety **nøyaktig samme ting** som emnet. Ikke noe videre og ikke noe smalere. «cola» er ikke «brus» (cola er én slags brus). «biff» er ikke «kjøtt». «sardeller» er «ansjos».
- For stikkord: uttrykket må nesten alltid bety det klassen sier. Et uttrykk som like ofte betyr noe annet, skal ikke med. Ta heller med et lengre uttrykk som er entydig («har løst på») enn et kort som er flertydig («løst»).
- Ett til fire ord, små bokstaver. Apostrof skrives som mellomrom («i m», «don t»). Ingen merkenavn.
- Vanlige bøyninger trenger du ikke føre opp når ordet bare får en endelse på opptil tre bokstaver (ost, oster, osten, ostene går av seg selv). Før opp former som endrer stammen (gulrot → gulrøtter) eller er et annet ord.
- Ikke gjenta det som står under `har`.

## Det du leverer

Ett JSON-objekt:

`{"forslag": {"<emne, allergenkode, klasse eller liste>": ["<ord>", …], …}, "usikre": {"<samme nøkler>": ["<ord du er i tvil om>", …]}, "merknad": "<kort, hvis noe i innfilen ser galt ut>"}`

Nøklene er navnene fra innfilen, uendret: for emner emnets navn, for allergener koden, for stikkord klassens navn, for ordlister listens navn, og `nektelser`. Heller få og sikre forslag enn mange usikre. Rundt 3–12 per nøkkel der det finnes noe å legge til; ingen der det ikke gjør det.
