# Dataflyt — foreslått

```mermaid
sequenceDiagram
 participant I as Palazzo / Nearby
 participant M as Privat møtecelle
 participant P as Hver deltaker
 participant A as Opptaksenhet
 participant Q as Privat leveringskø
 participant R as Hver mottakers innboks
 I->>M: Åpne / inviter (ingen lyd)
 M->>P: Samme plan, deltakerliste og hash
 P->>M: Aktivt ja fra hver autentisert identitet
 A->>M: Eksplisitt start, gjeldende revisjon
 M->>A: Kort tillatelse når ALLE vilkår holder
 A->>A: Mikrofon → kryptert midlertidig lyd → lokal ASR
 Note over M,A: Rosterendring/revokering: stopp innsamling først
 M->>P: Ny revisjon, null ja; alle godkjenner igjen
 A->>A: Finaliser tidligere godkjent segment
 A->>Q: Transkript + minimert tillitspakke, mottakerbundet
 Q->>R: Idempotent levering, kun segmentets mottakere
 R->>Q: Autentisert kvittering med hash og versjon
 Q->>M: Individuell status; alle mottatt først etter alle receipts
```

Autoritet: eksisterende resolver/capability + møtecellens planbundne samtykkekrav + recorderens lokale gate. Transport flytter data, skaper ikke samtykke. Tillitspakken dokumenterer hendelser, gir ikke myndighet. Nearby/lobby/Palazzo offentlig flate inneholder bare møteinngang; ingen lyd, transkript eller personpakker.
