# Ingen skeleton for denne flaten — og hvorfor

Artefaktkravet til G1-GUI er «CellConfiguration/skeleton-JSON som bildet er
rendret fra (når Porthole-preview er brukt)». Her er ingen brukt, og det er
med vilje.

Flaten er et **macOS-menylinjeikon, et adminvindu og varsler i macOS'
varslingsliste**. Ingen av delene tegnes av Porthole eller av
skeleton-rendereren. De tegnes av AppKit og SwiftUI (`MenuBarExtra`,
`Window`, `UNUserNotificationCenter`), utenfor CellProtocols rendererkjede.
Et skeleton-JSON her ville vært et dokument som later som om det styrer noe.

Referansebildene i `../images/` er derfor tegnet som HTML-mockup i riktig
størrelse, slik `haven-purpose-driven-dev` beskriver som fallback (2):
bilde per flate og per viktig tilstand, med en eksplisitt liste over hva som
ikke kan rendres.

| Bilde | Tilstand |
|---|---|
| `menu-ok-v1.png` | ingenting venter, alle kilder lest |
| `menu-attention-v1.png` | to saker venter, med kilde og alder |
| `menu-down-v1.png` | ingen kontakt — «vet ikke» som egen tilstand |
| `admin-window-v1.png` | adminvinduet, med en ulesbar kilde som egen rad |
| `notification-v1.png` | varslingslisten med handlingsknapper |

## Hva bildene ikke kan vise, og som derfor må sjekkes på skjerm

- Om macOS faktisk viser knappene kategorien ber om.
- Om varselet havner i varslingslisten når appen ikke har fokus.
- Om menylinjeikonet er lesbart i lys og mørk menylinje, og med redusert
  gjennomsiktighet.
- Om adminvinduet oppfører seg ved endring av vindusstørrelse.

Disse er ført som ikke verifisert i ACCEPT.md. Pariteten mot bildene måles
først når Kjetil har skjermen våken og har gitt varselsamtykke.
