# Brief til Astra (Codex, lesende) — Entity-utvidelse begge veier

Du er Astra. Arbeidskatalog er HAVEN-roten; stier relative til den. **Bare lesing i kode**; du skriver én fil: `CellProtocolDocuments/Deliverables/PDD_palazzo-entity-utvidelse-begge-veier_2026-09-14/handoff/ASTRA_ANALYSE.md`. Ingen git, ingen bygg, ingen kodeendringer.

Les først `…/FORMAALSSPEC.md` (§0 audit — fyll `unavailable`-radene, §1 utkast, §6 spørsmål).

## Oppdrag
1. **Kartlegg det som finnes**, med `[belagt: fil:linje]`:
   - CellProtocol: `IdentityLinkProtocolService` (request/approve/complete), `EntityAnchor.identityLinks`, IdentityVault/identityDomain-modellen, hvordan en identitet fra domene A brukes mot celler i domene B over bro (`RemoteBridgeheadAccess`, `VaporBridgeTransport`, hva som festes til presentert identitet — merk sikkerhetsnotatet i prosjektminnet: transporten fester lokal vault til presentert identitet uuid+fingerprint).
   - PalazzoScaffold: `PalazzoIdentityLinkCell` (`link.*`, `extendAccess`), `PalazzoAccessContractCell`, `PalazzoPrincipalGateway` (hvem blir requester over bro?), `PalazzoBridgehead` (hydrering av lokale identitetsdeskriptorer — hva betyr merknaden i praksis?).
   - Rollesimuleringen `PalazzoScaffold/Tests/Roles/` — hvilke formål dekker allerede lenking.
2. **Svar på §6 Q1–Q5** med anbefaling og motargument per spørsmål. Ta stilling.
3. **Hullene**: hva mangler for (a) HAVEN-identitet → Palazzo-entitet ved første kontakt, (b) Palazzo-gjest → HAVEN senere, (c) «tilby én gang, forklart, avvisbart». Angi for hvert hull om det hører i CellProtocol, PalazzoScaffold, CellScaffold/Porthole eller Binding, og størrelsesorden (timer/dager), med usikkerhet merket `[usikker]`.
4. **Foreslå deteksjonsøyeblikkene** som en tabell: situasjon → observerbart signal (hvilken celle/hendelse) → hvem tilbyr → hva tilbys → hva som skjer ved ja/nei/aldri.
5. Avslutt med en liste over hva Kjetil må avgjøre før G1 (maks 7 punkter, ett spørsmål per punkt).

Norsk, 1 500–3 000 ord. Avslutt filen med `<!-- ASTRA ANALYSE FERDIG -->`.

## Tillegg 2026-09-14 kveld — Kjetils svar og Q4′
Kjetil har svart på §6 (se FORMAALSSPEC §0, ordrett): D1–D5 er valgt; begge scaffolds kan tilby (den som først ser riktig tilstand); opplevelsen skal være trygg, ett trykk, forståelig; beviset «like sikkert eller sikrere enn Vipps»; deteksjonen er en celle. Seks mockups ligger i `images/` — vurder om tekstene på tilbudsflaten er sanne mot mekanismene du finner (særlig «Beviset lages av nøklene dine, her på telefonen» — stemmer det for custodial `guest:<id>`-identiteter i VaporIdentityVault? Hvis nøklene bor på serveren, si det, og foreslå hva flaten skal si i stedet).

6. **Q4′ — bevisstyrke mot Vipps.** Lag en eksplisitt sammenligning: hva IdentityLink-beviset faktisk beviser (nøkkelholder), hvor de private nøklene bor for hver identitetstype (custodial i scaffoldets vault / på enheten / i HAVEN-appen), angrepsflater (avspilling, MITM over bro — `VaporBridgeTransport` fester vault til presentert identitet uuid+fingerprint; kompromittert custodial nøkkel; ondsinnet scaffold), og hva Vipps-innlogging beviser (BankID-forankret person, enhetsbinding). Konkluder: er forslaget (a) koblingen ≥ Vipps på det den beviser + (b) personforankring via forankret identitet ved behov, holdbart? Hva må endres for at (a) skal være sant i dag? Merk alt `[belagt]`/`[vurdering]`/`[usikker]`.
7. **D2-signal (Q7):** foreslå den konkrete veien for «Palazzo-gjest får HAVEN senere» (kode/QR vist i Palazzo-flaten som HAVEN-appen skanner, eller annet) med hva som må finnes i hver ende.
