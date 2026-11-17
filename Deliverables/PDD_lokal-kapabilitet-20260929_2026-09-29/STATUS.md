# STATUS - lokal kapabilitet 20260929

- surfaces: binding, cell, gui, web, native
- tags: capability, live, audio, routing, grant, vision, agent

## Porter
- G1: **venter paa Kjetil** (FORMAALSSPEC.md, iterasjon 1)
- G1-GUI: ikke aktuelt enda - ingen flate er foreslaatt
- G2: ikke startet
- G3: ikke startet

## Ingen kode er skrevet
Dette er P0-P1.

## Det viktigste funnet
`HAVENAgentCapabilityBrokerCell`, `HAVENAgentSetup`, `KallimachosCapabilityIndex`
og `CapabilityInvitationProofSupport` finnes allerede. Mekanismen Kjetil beskriver
ser ut til aa vaere en utvidelse av noe som er der, ikke noe nytt. Lest i
kontrakter og doc-kommentarer - **ikke i implementasjonen**. Maa etterproeves foer
det legges til grunn.

## Den viktigste risikoen
R1: synkronisering. Per-hendelse fjernstyring over nett kan ikke gi
beat-noeyaktighet. Arkitekturen maa trolig vaere at HAVEN sender planen paa
forhaand og maskinen eier klokka. Losens paastand - boer valideres uavhengig
(Fabel eller Astra) foer den legges til grunn.
