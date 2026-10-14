# Kontrakt — PalazzoBooking

Skrevet 7. oktober 2026 av Losen, fra koden på commit `7eb404f1`, og rettet etter den uavhengige kontrollen. Det er en tabell, ikke en kontrakt-JSON med validator; testene gjennom rutene er det som holder den. Stier er relative til HAVEN-roten.

Cellen heter `PalazzoBooking`, er én for hele tjenesten, lagres, og eies av huset. Koden: `PalazzoScaffold/Sources/App/Cells/PalazzoBookingCell.swift`. Navnene: `PalazzoScaffold/Sources/App/Support/PalazzoScaffoldContract.swift`, `enum Booking`. Begge finnes bare på grenen `losen/palazzo-bordbestilling-20261007`; en kopi ligger i `HAVEN-Deploy/_handoff/HD-0077/bordbestilling/kilde/`.

Filen `noekkelstier.json` har de samme 16 nøkkelstiene, kanalene og kodene som en liste en maskin kan lese. `sjekk_noekkelstier.py` holder listen mot kildefilene og skriver ingenting:

```
python3 -B CellProtocolDocuments/Deliverables/PDD_palazzo-bordbestilling_2026-10-06/contract/sjekk_noekkelstier.py HAVEN-Deploy/_handoff/HD-0077/bordbestilling/kilde
```

## Nøkkelstiene

«Les» er en GET med tilgangen `r---`. «Skriv» er en SET med `-w--`; flere av dem endrer ingenting, men tar en forespørsel.

| Nøkkelsti | Slag | Hvem når den | Forespørsel | Svar |
|---|---|---|---|---|
| `booking.state` | les | huset, ansatt på husets liste | — | Om planen er lagt inn, tall, regler, hva cellen holder, hva den ikke gjør |
| `booking.plan` | les | huset, ansatt | — | Områder, bord, seteplaner med starttider, regler |
| `booking.plan.set` | skriv | bare huset | `areas`, `tables`, `seatings`, `cancelDeadlineHours`, `maxPartySizeForGuests`, `bookAheadDays`, `maxOpenBookingsPerGuest` | `stored` med planen, eller `error` med `problems` |
| `booking.area.set` | skriv | huset, ansatt | `area`, `open` | `opened` eller `closed`, og `bookingsStillThere` |
| `booking.availability` | skriv | enhver med bevist identitet | `date`, `partySize` | `slots` og `availableTimes`, eller `unavailable` med `reason` |
| `booking.request` | skriv | enhver med bevist identitet | `date`, `time`, `partySize`, `waitlistIfFull` | `booked` eller `waitlisted` med `bookingRef` og `booking`; ellers `refused` |
| `booking.mine` | les | enhver med bevist identitet | — | Egne bestillinger, hver med `linkedToYourEntity` |
| `booking.change` | skriv | den som eier bestillingen; huset; ansatt | `ref`, og minst én av `date`, `time`, `partySize`. Huset kan også sende `tables` | `changed`, eller `refused` |
| `booking.cancel` | skriv | den som eier bestillingen; huset; ansatt | `ref` | `cancelled`; huset får også `waitlistCandidates` |
| `booking.create` | skriv | huset, ansatt | `date`, `time`, `partySize`, `tables`, `channel`, `waitlistIfFull` | `booked` eller `waitlisted` |
| `booking.walkin` | skriv | huset, ansatt | `partySize`, `tables` | `seated` |
| `booking.mark` | skriv | huset, ansatt | `ref`, `state` | `marked` |
| `booking.promote` | skriv | huset, ansatt | `ref` | `promoted` |
| `booking.lookup` | skriv | huset, ansatt | `ref` | `found` med bestillingen og `guestCell`, eller `not_found` |
| `booking.overview` | skriv | huset, ansatt | `date` | Dagen: bestillinger, kuverter, bordliste, venteliste, nøkkeltall |
| `insight.bookings.upcoming` | les | huset; andre bare med avtale og husets samtykke | — | Kommende bestillinger uten peker til gjesten |

Ingen av nøkkelstiene under `booking.` kan gis bort med en avtale. Det en avtale kan gi, er `insight.bookings.upcoming` og `integration.state`. Avtalemalen er den integrasjonene bruker (`PalazzoAgreementTemplates.integration`), og begge krever i tillegg husets samtykke.

## Feltene i en bestilling

Det er to former. «Raden» er den som står i regnearket `house_bookings` og i `insight.bookings.upcoming`. «Bestillingen» er den huset og eieren får i svarene fra `booking.*`.

| Felt | Innhold | I raden | I bestillingen |
|---|---|---|---|
| `booking_ref` | Referansen, `PC-` og seks tegn | ja | ja |
| `booking_date`, `booking_time` | `åååå-mm-dd`, `tt:mm` | ja | ja |
| `party_size` | Antall gjester | ja | ja |
| `status` | Tilstanden på norsk: Bekreftet, Ubekreftet, Venteliste, Ankommet, Ferdig, Avbestilt, Ikke møtt | ja | ja |
| `table` | Bordene som én tekst | ja | ja |
| `service_mode` | Seteplanens navn | ja | ja |
| `source` | Kanalen, ett av sju faste ord | ja | ja |
| `created_at` | Når bestillingen ble laget | ja | ja |
| `state`, `stateLabel` | Tilstanden som kode og på norsk | nei | ja |
| `tables` | Bordene som liste | nei | ja |
| `updatedAt` | Når den sist ble endret | nei | ja |
| `durationMinutes` | Hvor lenge bordet holdes | nei | ja |
| `bookedByGuest` | Om en gjest bestilte selv | nei | ja |
| `linkedToYourEntity` | Om huset har pekeren til gjestens entitet | nei | bare i `booking.mine` |
| `guestCell` | Pekeren til gjestens entitet | nei | bare til huset og ansatte: i `booking.lookup`, og i svaret når huset selv endrer, avbestiller, fører eller gir bord |

Identiteten som bestilte, er lagret i cellen og kommer aldri ut i noe svar. Den står som den det gjelder i linjene cellen fører i husets logg.

## Kanalene

| Kanal | Hvem setter den |
|---|---|
| `nett` | Cellen, når gjesten bestiller selv |
| `telefon`, `e-post`, `oppmøte`, `intern`, `annet` | Huset, i `channel` på `booking.create`. `telefon` når feltet mangler |
| `walk-in` | Cellen, på `booking.walkin` |

Alt annet i `channel` gir `invalid_channel` og HTTP 400.

## Avslag

`refused` gir HTTP 409 og har `reason` og `message`. Feil formet forespørsel gir `error` og HTTP 400, med koden i `errorCode`. `booking.availability` svarer annerledes: spørsmålet er besvart, så det som ville vært 409 ved en bestilling, kommer som HTTP 200 med `unavailable` og `reason`, eller som `reason` på hver tid som ikke er ledig.

| `reason` eller `errorCode` | HTTP | Betyr |
|---|---|---|
| `plan_not_configured` | 409 | Huset har ikke lagt inn bord og seteplaner |
| `in_the_past`, `too_far_ahead` | 409 | Tidspunktet har vært eller har begynt, eller er lenger fram enn planen tillater |
| `closed_that_day`, `not_a_bookable_time` | 409 | Ingen seteplan den dagen, eller klokkeslettet er ikke en starttid |
| `party_too_large` | 409 | Større selskap enn gjesten kan bestille selv |
| `too_many_open_bookings` | 409 | Gjesten har alt så mange bestillinger som kan stå samtidig |
| `start_is_full`, `no_table` | 409 | Taket for klokkeslettet er nådd, eller ingen bord passer |
| `unknown_booking` | 409 | Referansen finnes ikke for den som spør |
| `past_deadline`, `not_changeable` | 409 | Fristen er ute, eller bestillingen er avsluttet |
| `table_taken`, `table_too_small` | 409 | Bordet huset pekte ut, er opptatt eller for lite |
| `invalid_date`, `invalid_time`, `invalid_party_size`, `unknown_table`, `invalid_state`, `invalid_channel`, `invalid_payload`, `invalid_plan`, `unknown_area` | 400 | Forespørselen er feil formet |
| `duplicate_reference` | 400 | Finnes i reglene. Kommer ikke ut gjennom rutene, for cellen lager referansen selv |

## Det som ikke finnes

Ingen eksempler fanget fra en kjøring ligger her. Svarene over er lest fra koden, og formene er de testene i `PalazzoScaffold/Tests/AppTests/PalazzoBookingCellTests.swift` krever.
