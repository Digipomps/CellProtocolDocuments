# Regler for ordlistetrådene (7. oktober 2026)

Du skal foreslå ord. Restauranten Palazzo Communale (siciliansk, i Oslo) har en concierge på nettsiden som leser det gjesten skriver, uten språkmodell. Den kjenner ord igjen fra lister. Listene mangler mange vanlige skrivemåter. Du foreslår det som mangler, ut fra det du vet om språk. Du får ikke se setninger gjester har skrevet, og skal ikke lete etter dem.

## Tilgang

Les BARE denne regelfilen og den ene innfilen oppgaven din navngir. Les ingenting annet under `/home/claude` eller `/mnt`, og søk ikke etter andre filer. Bruk ikke nettet. Du trenger bare Read, Write og Bash (bare for `date -u`).

## Hva som er et godt forslag

- Et ord eller uttrykk en gjest kunne skrevet: bokmål, nynorsk, vanlig dialekt og muntlig stavemåte («æ», «itj», «dokker»), svensk, dansk, engelsk og tysk. Også vanlige skrivefeil.
- For emner og allergener: ordet må bety **nøyaktig samme ting** som emnet. Ikke noe videre og ikke noe smalere. «cola» er ikke «brus» (cola er én slags brus). «biff» er ikke «kjøtt». «sardeller» er «ansjos».
- For stikkord: uttrykket må nesten alltid bety det klassen sier. Et uttrykk som like ofte betyr noe annet, skal ikke med.
- Ett til fire ord, små bokstaver. Ingen merkenavn.
- Vanlige bøyninger trenger du ikke føre opp når ordet bare får en endelse på opptil tre bokstaver (ost, oster, osten, ostene går av seg selv). Før opp former som endrer stammen (gulrot → gulrøtter) eller er et annet ord.
- Ikke gjenta det som står under `har`.

## Det du leverer

Én JSON-fil, skrevet med Write til stien oppgaven din navngir:

`{"forslag": {"<emne, allergenkode, klasse eller liste>": ["<ord>", …], …}, "usikre": {"<samme nøkler>": ["<ord du er i tvil om>", …]}, "merknad": "<kort, hvis noe i innfilen ser galt ut>"}`

Nøklene er navnene fra innfilen, uendret. Heller få og sikre forslag enn mange usikre. Rundt 3–10 per nøkkel der det finnes noe å legge til; ingen der det ikke gjør det.

## Tid

TIDEN ER HARD: 8 minutter. Kjør `date -u` når du starter og før du leverer. Rekker du ikke alt, leverer du det du har. Svaret ditt til meg er kort: stien til filen, antall nøkler med forslag, antall forslag i alt, og start- og sluttid (UTC).
