STATUS: IKKE KJØRT — iOS-kompilering/simulatortester og fysisk NI/UWB må utføres på angitt PR-head

# N12 — operatørprosedyre

Stier er relative til HAVEN-roten. Ikke merge eller endre produksjonspinner som del av prøven.
Registrer dato, full CP-head, Xcode-versjon, app-head, iPhone-modell og iOS-versjon i
`handoff/CP53-N12-evidence/ios-<dato>/`. Bruk testidentiteter i lokale vaults.

## 1. Pakken: iOS-bygg og tester uten NI-maskinvare

1. I Terminal/den godkjente `skript`-modusen, fra HAVEN-roten, kjør:

   ```sh
   CP53_EXPECTED_HEAD="$(git -C CellProtocol/_wt-bro-kanal-auth-20260927 rev-parse HEAD)" \
     bash HAVEN-Deploy/_handoff/BRO/wp-cp53-ios-bygg.sh
   ```

   Sammenlign SHA-en med N12-rapporten før kjøring. Skriptet krever rent arbeidstre,
   kjører eksisterende kapasitetsvakt uten overstyring, og velger en installert iPhone-
   simulator. Det bygger `CellApple` og tester NI-uavhengige tilfeller gjennom
   `CellProtocol-Package` / `CellBaseTests`. Testutvalget er målrettet iOS-verifikasjon;
   det erstatter ikke full macOS-suite. Ingen test blir markert skipped.
2. Mangler iOS-runtime, installer/velg runtime i Xcode før ny kjøring. Ingen simulator
   betyr ikke bestått. Mangler forventet scheme, stopp og bevar `schemes.json`.
3. Bestått: `** BUILD SUCCEEDED **`, `** TEST SUCCEEDED **`, seks NI-assosiasjonstester,
   iOS-testen `testPlatformTokenDecoderRejectsMalformedArchiveWithoutNIHardware` og
   de to DiscoveryToken-testene er faktisk kjørt og grønne. Bevar begge `.xcresult`,
   `head.txt` og `operator.log`; endre ikke Package.resolved for å få grønt.

Codex-forsøkene nådde ikke kompilering: CoreSimulatorService var utilgjengelig,
pakkeinngangen ble avvist, og eksplisitt `.swiftpm/xcode/package.xcworkspace` ble
avvist som «not a workspace file». Scriptet er syntakskontrollert, men **ikke kjørt
utenfor sandkassen**. Ingen påstand om at alle øvrige iOS-kilder allerede bygger.

## 2. App, target og enheter

- App: `Binding/Binding.xcodeproj`, **target/scheme HAVEN**, Debug, to fysiske iPhones.
  Kildegrunnlaget viser iPhone-støtte og minimum iOS 18 i dette app-prosjektet.
- Bruk to UWB-støttede iPhones der `NISession.deviceCapabilities.supportsPreciseDistanceMeasurement`
  er true; simulator, Mac eller bare Bluetooth-discovery er ikke en NI-prøve.
  Installer samme app/CP-revisjon på begge. Start med telefonene omtrent 1 meter fra
  hverandre, skjermene aktive og appen i forgrunnen, uten skjermlåsing.
- I et separat lokalt test-workspace legg til `Binding/Binding.xcodeproj` og den
  lokale pakken `CellProtocol/_wt-bro-kanal-auth-20260927` som package override.
  Kontroller Build Log at **ScannerNearbyInteraction.swift fra dette arbeidstreet**
  faktisk kompileres. Ikke stol bare på et produktnavn eller en gammel appinstallasjon.
  Ikke commit/push endringer i Binding eller dets dependency-pin.
- Bruk appens normale Development Team/signering for enhetene. Prosjektet har
  `NSNearbyInteractionUsageDescription`, `NSLocalNetworkUsageDescription` og
  Bonjour `_haven-radar._tcp`/`_haven-radar._udp`. Godta lokalnett- og NI-tillatelse
  på begge telefonene. Bevar eventuell feiltekst hvis tillatelse/hardware mangler.

Appbygget og navigasjonen er kildeinspisert, ikke kjørt av Codex. Target finnes;
hele appens nåværende integrasjon med CP-headen er en egen, uprøvd forutsetning.

## 3. Etablering og målinger

1. Åpne den lokale **Entity Scanner**-konfigurasjonen på begge enheter (katalogfunksjon
   `ConfigurationCatalogCell.entityScannerWorkbenchConfiguration()`, endpoint
   `cell:///EntityScanner`). Start scanner på begge. Bruk `invite` på funnet peer og
   godta invitasjonen på den andre med `respondToInvitation` / `accept=true`.
   «I nærheten» alene/discovery alene er ikke en autentisert NI-oppkobling.
   Hvis konfigurert UI ikke tilbyr disse handlingene, åpne **Scanner Test Helper** /
   **Pairing Checklist** for samme lokale celle; ikke omgå celleeierkontrollen.
2. Sett kildebreakpoints i arbeidstreets `ScannerNearbyInteraction.swift`:
   etter arkivering i `AppleScannerNISession.init`, etter `decodeToken` i `run`, og
   i `session(_:didUpdate:)`. Sett dessuten breakpoint før `proximityChanged` i
   `ScannerService.enqueueNearbyMeasurement` og i `AppleScannerNISession.invalidate`.
3. Ved arkivering: kontroller at `localToken.count > 0` og at
   `try AppleScannerNISession.decodeToken(localToken) == session.discoveryToken`
   evaluerer til true i samme Swift-debuggerscope. Dette er det vellykkede native
   secure-archive/decode-beviset som macOS-falsken ikke kan gi. Ikke skriv tokenbytes
   eller nøkkelmateriale til logg.
4. Ved `run`: kontroller at én session får én motparttoken; ingen gjentatt `init`
   ved ordinære måleoppdateringer. Ved publisering noter bare testens remoteUUID,
   `entry.context.generation` og `entry.generation`; bekreft at remoteUUID er den
   andre telefonens sessionUUID, og at context.identity er den beviste motparten.
5. Fortsett uten pausepunkter, og flytt den andre telefonen fra omtrent 1 til 3 meter
   og tilbake. Observer `scanner.proximity` / `distanceMeters` for riktig remoteUUID
   med minst ti oppdateringer. Avstand skal endres i forventet retning; retning kan
   være nil når Apple ikke leverer den. Ren discovery-status er ikke et resultat.
6. Sett appen kort i bakgrunnen og tilbake. Observer suspend/resume. Eventuell restart
   skal bruke samme sesjon/token; ingen måling publiseres mens NI er suspendert.
   Plattformens terminale invalidation krever ny kanal, ikke automatisk ny NI-instans.

## 4. Stop, revoke og reconnect

1. Trykk **Stopp** på A. Bekreft `invalidate` for As NI-driver og at ingen ny
   `scanner.proximity` publiseres fra gammel entry etter stop. En verdi som allerede
   vises i et historisk UI er ikke et nytt event; vurder eventstrømmen/breakpointet.
2. Start begge på nytt og opprett ny invitasjon. Krev ny shared setupID, kanal- og
   NI-generasjon samt ny NISession. Gjenta avstandsprøven og bekreft ny remoteUUID-
   mapping. Gammel token/callback-injeksjon dekkes separat av deterministiske tester.
3. Revokasjon: ved publiseringsbreakpointet på A (etter liveness-kontrollen og uten
   session-låsen holdt), kjør `expr -l Swift -- entry.context.session.revoke()` i
   debuggeren og fortsett. Kontroller at driveren invalideres, kanal lukkes og ingen
   senere måling fra samme entry publiseres. Den allerede innslupne callbacken kan
   fullføre. Ny kanal må etableres eksplisitt for ny NI-måling.
4. Gjenta med B som inviter. Etablering, native archive/decode, oppdateringer og stop
   skal bestå i begge retninger. Marker et uteblitt resultat som IKKE BESTÅTT/
   IKKE KJØRT med faktisk årsak; ikke erstatt NI med syntetisk avstand.

**Bestått fysisk totelefonprøve:** punktene 3 og 4 er gjennomført i begge retninger,
med rett peer i alle målte events og invalidation ved stop/revoke. Registrer antall
oppdateringer, avstandsendring, generasjonsskifte, og ev. feil — uten tokenbytes.

Samtidig fysisk A/B/C krever **en tredje UWB-telefon**, og er ikke bevist av to
telefoner. Dersom den finnes: koble A til både B og C; hold B stille, flytt C, og
krev separate sesjoner og bare Cs endrede målinger. Revoker B og krev fortsatt C-
måling. Denne utvidelsen er også **IKKE KJØRT**; macOS B/C-testene er deterministisk
assosiasjonsbevis, ikke en påstått treradioprøve.
