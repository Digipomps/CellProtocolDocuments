# Valget om rekkefølgen på staging

Fakta, målt 02.10:

- Staging kjører `415ea3d2`: 2026.9.3 pluss fornyelse av utløpte tilganger. Det er live-testet 30.09.
- Køens plan, etter din beskjed «Be Codex utføre», er å sette ut 2026.9.4 (`fdcfe7a5`) på staging når HD-0141 er frigitt, vertens rot har 40 GiB ledig og HD-0150 er håndtert. 2026.9.4 har ikke fornyelseskoden.
- PR #277 har fornyelseskoden, og i tillegg fornyelse de siste sju dagene før fristen. Merge-sjekken er grønn. Sjudagersvinduet har bare enhetstester; det er ikke prøvd live.
- Enhver fornyelse krever at en ny invitasjonsliste legges i stagings miljø. Det er en omstart av containeren, og den krever et eget claimvindu (HD-0006).
- PR #277 kan merges nå uten å røre 2026.9.4, som er bundet til tagg og SHA.

| Valg | Hva som skjer | Vegar (ute 08.10) | Victoria (ute nå) | Hva det koster | Hva du gjør |
|---|---|---|---|---|---|
| D. 2026.9.4 som bestilt, og fornyelsen rett etter (anbefalt) | 2026.9.4 settes ut slik du har bestilt. Rett etter at den er verifisert, settes en liten utgivelse med bare PR #277 oppå ut, og invitasjonene legges inn i samme vindu. | Kan fornyes før 08.10 hvis begge utsettingene rekkes før da. Ellers rett etter. | Fornyes når enhets-ID-en hennes er her og den lille utgivelsen er ute. | To image-bygg og to vinduer. Staging skifter mens spørsmålet om prod for 2026.9.4 er åpent, og det fraviker køens regel. | Sier ja til merge av PR #277, og ja til at kø-tråden legger den lille utgivelsen rett etter 2026.9.4. |
| A. Ta fornyelsen med i neste utsetting | PR #277 merges, og en utgivelse med både konferanseendringene og fornyelsen settes ut i stedet for 2026.9.4. | Som D, med én utsetting å vente på. | Som D. | Setter bestillingen din til Codex til side. 2026.9.4 blir aldri verifisert som egen utgivelse, og spørsmålet om prod flytter til den nye. | Sier ja til merge, og ber kø-tråden bytte 2026.9.4 mot den nye utgivelsen på staging. |
| B. 2026.9.4 som planlagt, fornyelsen når køen kommer til den | 2026.9.4 settes ut. Fornyelsen forsvinner fra staging til en utgivelse med PR #277 er ute. Køens vilkår for neste utgivelse er mange, så ventetiden er åpen. | Uten tilgang fra 08.10 til den utgivelsen er ute. | Uten tilgang til den utgivelsen er ute. | Ingen endring i køens plan. | Sier ja til merge. |
| C. Forny på det som står nå, før 2026.9.4 | Invitasjonene legges inn på `415ea3d2` så snart HD-0141 er frigitt eller gir et vindu. 2026.9.4 venter til begge er fornyet. | Kan først fornyes etter 08.10. Det som står nå, fornyer bare utløpte tilganger. | Fornyes når enhets-ID-en hennes er her. | 2026.9.4 venter på staging til etter 08.10. | Ber kø-tråden holde 2026.9.4 tilbake. |

Alle fire venter på det samme: at HD-0141 slipper `cellscaffold-app-1`, eller at eieren gir et vindu.

Uansett valg gjør denne tråden ingen vertsendring selv. Rekkefølgen på utgivelsene eies av kø-tråden. Merge, tagg, image og utsetting avgjør du, og du avgjør hvem som utfører.
