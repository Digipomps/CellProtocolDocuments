# Ordliste for invitasjon → samtale

Formål Q: flaten bruker ingen ord mottakeren må slå opp. Dette er forbudtlisten, og hva som står i
stedet. `test.invite.one-primary-action-per-screen` sjekker hvert bilde mot venstre kolonne.

| Forbudt i flaten | Bruk i stedet | Hvorfor |
|---|---|---|
| scaffold | «tjenesten Kjetil bruker», «hos deg», «her» | Ingen utenfor prosjektet vet hva et scaffold er. Det som betyr noe for mottakeren er *hvem sin* tjeneste det er. |
| entitet, entitetsdata | «deg», «det som er ditt», «det du har» | Entiteten *er* personen sett fra HAVEN. Si personen. |
| anchor, EntityAnchor | — (nevnes aldri) | Intern struktur. |
| identitet (som teknisk ord) | «den du er her», «privat-deg» — eller utelat | I rute 1 hos mottaker med HAVEN sier vi «identiteten du bruker privat» én gang, fordi valget er reelt. Ellers utelat. |
| keypath, aksjon, contract | — | Intern. |
| celle, ChatCell, InvitationCell | «samtalen», «invitasjonen» | Si tingen, ikke beholderen. |
| envelope, batchPersist, konvolutt | «lagret hos hver av dere» | Rute 3 hos mottaker med HAVEN: «en avtale dere begge signerer, lagret hos hver av dere». |
| genesis, forsegling | — (aldri for nykommer) | Nykommeren skal ikke vite at noe ble forseglet; de skal oppleve at det som er deres er deres. |
| artefakt, proof, signatur (som substantiv) | «signert» (som adjektiv, én gang per bilde) | «Valget ditt sendes signert til Kjetil» er nok. |
| billett, ticket, token | «invitasjonen», «lenken» | |
| landing, landingsside | «lenken», «invitasjonssiden» | |
| register, matching | — (ikke i denne flyten) | Hører til oppdagelse, ikke til invitasjon. |
| relasjon (som teknisk ord) | «kontakten Kjetil», «dere to» | |
| chronicle, spor, logg | — | Vises ikke for bruker i denne flyten. |
| purpose://, formål (som teknisk ord) | — | |
| HAVEN-konto | «konto» — helst «ingen konto trengs» | Vi har ingen konto; si det bare når vi sier at det ikke trengs. |
| butler (mot mottaker) | «hjelp», «spør» | Butleren er avsenderens. Mottakeren møter en hjelp, ikke noens butler. |

## Faste formuleringer

Disse gjentas ordrett, slik at de blir gjenkjennelige:

- **«Hvem ser dette: …»** — nederst på hvert bilde, alltid med hvem, aldri med hva systemet gjør.
- **«Besvart — ikke nå»** — det eneste avsender ser ved nei, uansett hvilket nei.
- **«Sendes én gang. Ingen purring.»** — på forhåndsvisningen og på «sendt».
- **«Hans egne notater — ikke bekreftet av deg»** — over feltene mottakeren ser.
- **«Ja, la oss snakke» / «Ikke nå» / «Aldri — ikke inviter meg igjen»** — de tre svarene, i den rekkefølgen.
