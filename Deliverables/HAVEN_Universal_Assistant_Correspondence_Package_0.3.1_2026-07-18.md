# HAVEN Assistant Correspondence 0.3.1 universal2 — produkt- og verifikasjonsrapport

**Dato:** 18. juli 2026

**Beslutningseier:** Kjetil

**Mottakerpilot:** Victoria / Lille Robot

**Status:** Verifisert forhåndsvisning; formell mottakerleveranse blokkert av notarisering

## Kort dom

`HAVENAgentD-0.3.1-universal2.pkg` er bygget og Developer ID-signert. Alle tre
installerte binærer inneholder `arm64` og `x86_64`, har matchende
payload-hasher og gyldig Developer ID Application-signatur med hardened
runtime. Begge slicer er kjørt funksjonelt på en Apple M5 MacBook Pro: native
arm64 og Intel gjennom Rosetta. Begge kjørte også MCP-handshake og
staging-`doctor`; sistnevnte
returnerte HTTP 200 og `status: ok` for Kjetils eksisterende principal.

Pakken er ikke sendt til Apple for notarisering og har ingen staplet billett.
Gatekeeper avviser den derfor korrekt som `Unnotarized Developer ID`. Den er
ikke en formell Victoria-leveranse ennå.

## Formål og mål

| Formål | Mål | Resultat |
|---|---|---|
| `purpose://contact.communication` | Signert lokal korrespondanseklient kan nå den persistente staging-postkassen fra begge CPU-slicer | Bestått: `doctor` HTTP 200 på arm64 og x86_64 |
| `purpose://digital-work.coordinate` | Samme installasjonspakke kan brukes på Apple Silicon og Intel uten å gi korrespondanseflaten bredere myndighet | Bestått på M5 i native/Rosetta-prøve; fysisk M4- og Intel-installasjon gjenstår |
| `purpose://access.audit.privacy` | Pakken beholder fire-verktøygrensen, signerte binaries og identitetsbundet lokal profil | Bestått i MCP `tools/list`, kode-signatur og eksisterende Kjetil-profil |
| `purpose://test.acceptance` | Arkitektur, hashes, signaturer, MCP, staging og Gatekeeper-status skal ha eksplisitte bevis | Bestått for forhåndsvisning; notarisering/installasjon er åpen gate |

## Leveranseartefakt

Arbeidsmappe:

`/private/tmp/HAVEN-Assistant-Correspondence-Pilot-0.3.1-universal2-preview`

| Artefakt | SHA-256 |
|---|---|
| `HAVENAgentD-0.3.1-universal2.pkg` | `dc6bf8a5235235023be3636737a7ee79a77cbf90fa8ec3082c5c384d399a2b3a` |
| `haven-agentd` | `ef42a2e3f7d8f4bd021f0d8b2607b641e69e5d34e786c351bdc32d471380c8ff` |
| `haven-correspondence-mcp` | `827f4c117ce2348a98015ebe06e4ad88abac97891e30cc86d7fba1fe0d2ee949` |
| `sprout` | `648ac0fe08ce20b7bf111ba1263c26454bb3c95f5bb6b06c6a7006b14462efb9` |

Manifestet oppgir:

- versjon `0.3.1`;
- arkitektur `universal2` med `arm64` og `x86_64`;
- verktøykjedefingeravtrykk `50ff90ec92269ade`;
- Team ID `5UT5HQTCV9`;
- Sprout-revisjon `7d82016`;
- korrespondanse-MCP authority `messages-only`.

Distribution-kontrakten har
`hostArchitectures="arm64,x86_64"`.

## Verifikasjonsmatrise

| Lag | Kontroll | Resultat |
|---|---|---|
| Pakkeintegritet | `shasum -a 256 -c SHA256SUMS` | `OK` |
| Installer-signatur | `pkgutil --check-signature` | Developer ID Installer, gyldig Apple-kjede og tidsstempel 18. juli 2026 10:12:02 UTC |
| Payload-integritet | `shasum -a 256 -c PAYLOAD_SHA256SUMS` | 3 av 3 `OK` |
| Arkitektur | `lipo -archs` på alle tre binaries | `x86_64 arm64` på alle tre |
| Kode-signatur | `codesign --verify --strict --verbose=4` uten sandbox | 3 av 3 gyldige; Team ID `5UT5HQTCV9`; hardened runtime |
| Arm64-kjøring | MCP-bruk, `list-cell-blueprints`, Sprout units | Bestått |
| Rosetta-kjøring | Samme tre kontroller under `arch -x86_64` | Bestått; prosessen rapporterte `x86_64` |
| MCP-protokoll arm64 | `initialize`, `notifications/initialized`, `tools/list` | Bestått; nøyaktig fire korrespondanseverktøy |
| MCP-protokoll x86_64 | Samme handshake og liste | Bestått; samme fire verktøy |
| Live staging arm64 | Signert `doctor --profile kjetil` | HTTP 200, `status: ok`, tom inbox, `nextSequence: 0` |
| Live staging x86_64 | Samme `doctor` under Rosetta | HTTP 200, identisk resultat |
| Automatisert suite | `swift test --filter HavenCorrespondenceMCPTests` | 2 tester, 0 feil |
| Gatekeeper | `spctl -a -vv -t install` | Avvist som forventet: `Unnotarized Developer ID` |
| Stapling | `xcrun stapler validate` | Ingen billett, som forventet før notarisering |

En sandboxet `codesign --verify` ga falskt «modified»-resultat på de utpakkede
binærene. Den samme kontrollen uten sandbox verifiserte alle tre med gyldig
Developer ID-kjede, tidsstempel og Designated Requirement. Dette er registrert
som en testmiljøbegrensning; payload-hashene var identiske i begge miljøer.

## Byggefunn og korrigering

Første universalbygg gjenbrukte Swift/Clang-modulcache etter Xcode/SDK-skifte og
feilet sent med motstridende `NSThread`-definisjoner. Feilen oppstod før
signering, slik fail-closed-gaten skulle.

Korrigeringen består av:

1. separate SwiftPM scratch paths per arkitektur;
2. namespace beregnet fra Swift-, Xcode- og macOS SDK-fingeravtrykk;
3. separat kryssbygging av hvert produkt før `lipo`;
4. eksplisitt arkitekturgate før stripping og signering;
5. valgfri prebuilt-bane for CI/sandbox, der `haven-agentd` og
   `haven-correspondence-mcp` må leveres sammen og alle tre binaries fortsatt
   må bestå arkitekturgaten;
6. egne checksums for distribusjonspakken og den installerte payloaden.

De endelige HAVEN-slicene ble bygget i samme begrensede miljø mot den samme
fastlåste CellProtocol-revisjonen `0ef84bcfbb81d2e112e961719821ed218cf95169`.
Signering og pakkebygging brukte deretter de ferdige universalbinærene uten å
gi SwiftPM-byggingen nøkkelringmiljøets bredere filesystem-syn.

## Påstandsregnskap

| ID | Påstand | Dom | Begrunnelse / restusikkerhet |
|---|---|---|---|
| U1 | Pakken er universal for Apple Silicon og Intel | **Støttet med resttest** | Alle tre binaries har begge slices, og begge kjører på M5 via native/Rosetta. Fysisk installasjon på Victorias M4 og på separat Intel-Mac er ikke utført. |
| U2 | M4 Mac mini er egnet første pilotvert | **Støttet som lavrisiko plan, ikke målmaskinbevis** | M4 er Apple Silicon og pakken har en fungerende arm64-slice, men den konkrete M4-maskinen og dens Keychain-innrullering er ikke testet. |
| U3 | Samme Victoria-principal kan uten videre kopieres mellom flere maskiner | **Motsagt** | v0.3.1 binder principal til én device/identity/public key. Hver maskin trenger egen nøkkel og grant, eller en ny fler-enhetskontrakt. |
| U4 | Victoria eier hele grant-livsløpet i v0.3.1 | **Ikke støttet** | Hun eier lokal nøkkel og beslutninger på sin side; staging-operatøren forvalter issuer-, tillatelses- og revokasjonsmekanismen. |
| U5 | Pakken er klar for formell ekstern overlevering | **Motsagt foreløpig** | Notarisering, stapling, ny Gatekeeper-prøve, invitasjon og mottaker-`LES_MEG.md` mangler. |
| U6 | Postkassen kan levere mens laptopene sover | **Støttet for lagring, ikke autonom respons** | Staging er tilgjengelig og inbox leses etter oppvåkning. Ingen hosted modellarbeider blir vekket av dette. |
| U7 | Lille Robot kan bruke postkassen mellom egne maskiner i neste pilot | **Støttet som hypotese/plan** | Krever separat principal/grant per maskin og eksplisitt peer-policy; ikke testet ennå. |

## Foreslått fler-maskinpilot

1. Installer notarisert 0.3.1 på Victorias M4 Mac mini.
2. Opprett lokal Ed25519-identitet og send adgangsforespørsel.
3. Kjetil mottar varsel og utsteder eller avslår beviset.
4. Kjør `doctor`, MCP-handshake og en melding fra Kjetil.
5. Opprett senere en separat Intel-principal med egen nøkkel og grant.
6. Test M4 → staging → sovende Intel → henting etter oppvåkning.
7. Test avslag for kopiert nøkkel, feil device-binding, feil peer og tilbakekalt grant.

## Kandidatfunksjoner for Lille Robots vurdering

Lokalt:

- varsling uten hosted agent;
- kryptert lokal søkeindeks og arkiv;
- outbox retry/status og hemmelighetsfri `doctor`-eksport;
- maskin-/profiloversikt, nøkkelrotasjon og revokasjonsforespørsel;
- Claude-konfigurasjonsinstallasjon/validering;
- vedleggsreferanser med digest.

På staging:

- tråder, reply-referanser og leveringskvitteringer;
- fler-enhetsruting under samme Entity;
- ende-til-ende-krypterte konvolutter;
- eierstyrt retention, eksport og sletting;
- `ArtifactReceiptCell` for verifiserbar metadata;
- `TimebaseMapCell` for medie-/transkript-/eksporttidsbaser;
- claim/evidence-register med eksplisitt evidensstatus.

Forslagene er ikke implementert og skal prioriteres etter formål, dataklasse,
capability, feilmodus og akseptansetest.

## Beslutningsgate

Formell mottakerleveranse krever fortsatt:

1. Kjetils eksplisitte godkjenning til å sende den eksakte pakken til Apples
   notariseringstjeneste;
2. `Accepted` notary-resultat;
3. staplet billett og bestått Gatekeeper-kontroll;
4. Victorias personlige invitasjon og et `LES_MEG.md` med hash og
   installasjons-/innrulleringssteg;
5. fysisk installasjon og `doctor` på Victorias M4 Mac mini.

Før denne gaten er passert, er dommen **CONDITIONAL GO for pilot preview** og
**NO-GO for formell ekstern installasjon**.

— **Codex**
