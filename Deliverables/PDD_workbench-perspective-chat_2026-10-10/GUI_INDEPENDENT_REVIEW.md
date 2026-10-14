# Uavhengig GUI- og dokumentkontroll

2026-10-10 · kontrollør: Codex-underagent `workbench_spec_review`.
Skrivebeskyttet gjennomgang; kontrolløren startet ingen egne UI-/backendkjøringer.

## Første kontroll og rettinger

Fire P2-funn ble rettet i generator og bilder:

1. Historikk brukte konstant private/text og blandet private/delte eksempelrader.
   Den har nå separate fixtures/omfangstekst og en queryID til planlagt søkeutkast.
2. Egen pakke manglet formålsvalg, faktisk velgerbilde for skills/kontekst og
   forhåndsvisning av bestemt versjon/publikum. Disse kandidatene er nå rendret.
3. Ekstern modellbruk manglet mottaker/innhold/avslag. Egne bilder viser dette.
4. Uavklart køstatus tilbød bare Se krav. Les køstatus sender nå samme commandID.

Etterkontroll: PASS innenfor dette omfanget. Radstyrt knappetekst, keypath og
payload ble avstemt mot den eksporterte rendererens resolveButtonSpec.
Kontrolløren påpekte at draft-gapet også gjelder pakkelagring; dette ble målt
med egen skriv→Lagre-probe og dokumentert sammen med skriv→Send.

## Sluttkontroll

Kontrolløren bekreftet ved egen opptelling:

- 54 tilfeller, 926 ordinære kontrollhandlinger, 43 keypaths.
- Ingen registrerte JS-, komponent- eller unsupported-feil / horisontal overflyt.
- Laveste registrerte tekstkontrast 4,99:1 for elementene målefunksjonen undersøker.
- 54 bildehash/størrelser stemmer med manifest; totalt 4 711 943 PNG-bytes.
- Alle galleriets filreferanser finnes.
- Kanonisk generator, harness, CSS og rapport er like de etterkontrollerte kopiene.
- GUI_REVIEW.md, images/README.md og planlagt sluttsvar skiller design-/dispatch-
  bevis fra backendfunksjon og avgrenser Send/Lagre-gapet og kontrastmålingen.

Ett P3-funn i sluttkontrollen var en gammel G1-formulering i FORMAALSSPEC.md §6.
Den ble rettet. Kontrolløren leste seksjonen på nytt og bekreftet: G1 godkjent,
G1-GUI venter som neste beslutning. Ingen resterende funn innenfor kontrollomfanget.

## Avgrensning

Utvalgte bilder ble visuelt lest, inkludert nye lyse kontekst-, delings-, modell-
og delt-historikk-bilder. Kontrolløren så ikke visuelt gjennom alle 54 eller alle
nye mørke bilder. Root inspiserte i tillegg utvalgte lyse/mørke/smale bilder.
Native Binding, live Explore, faktisk sessionlagring/Flow/persistens, autorisasjon,
modell-/agentutføring, merge og deploy er ikke godkjent av denne kontrollen.
Dette er ingen G3-akseptanse og ingen brukergodkjenning av G1-GUI.
