# TESTRESULT — implementeringsdel etter G2

## Siste status 2026-10-13 — appkoblet, signert Mac-kandidat

Evidensrot (HAVEN-relativ): `Binding/Implementation/PalazzoBinding-20261012/implementation/`.
`APP-INTEGRATION-20261013.md` og `meeting-app-provenance-20261013.json` beskriver sluttkilden;
`PHYSICAL-TEST-20261013.md` er den konkrete fysiske prøven.

- **79 passed, 0 failed, 0 skipped** mot sluttkilden (`meeting-app-tests-final.log`).
- Faktisk Binding-konfigurasjonslasting, signert Nearby-innmelding, autentisert privat Scanner/Bridge,
  kryptert AVAudioEngine-arkiv, lokal Speech-behandling og varig mottakerinnboks/kvittering er koblet inn.
- Ny deltaker ugyldiggjør alles ja og stopper opptak; alle må aktivt signere den nye planen før eksplisitt Start.
- Nye tester dekker opptaksarkiv med injisert ASR, faktisk signert innmelding, begge private bridge-roller,
  stor paget levering til kryptert innboks, feilisolasjon, faktisk godkjent syntetisk norsk Speech uten mikrofon
  og native rendering. De erstatter ikke fysisk radio/mikrofonprøve.
- `candidate-macos-arm64/HAVEN.app` og `HAVEN-meeting-macOS-arm64.zip`: signert macOS arm64 26.1+
  utviklingskandidat; kopiert signatur verifisert. Vanlig app åpnet og Kontroll → Entity Scanner →
  Mine transkripter klikket/readback. `candidate-nearby.png` og `candidate-inbox-empty.png` er skjermbevis.
- Første fysisk prøve kan kjøres på registrerte Mac-er. Profilen dekker to Mac-er. Ingen iOS-kandidat;
  full minst-tre-plus-sen-fjerde prøve trenger flere enheter/profiler. 60 minutter, kvalitet, retention,
  full Palazzo-paritet og G3 står åpne. Ikke installert i Applications, merget eller produksjonsdeployet.
- Arbeidsbenk: siste kommentar ble ikke skrevet; MCP bare state/query og utilgjengelig query,
  innlogget GUI uten kommentarfelt og Butler uten modell. Oppdateringen er bevart i
  `workbench-pending.json`. A/B/D/E/F/G sist verifisert in-progress, C ready, P done.

Teksten nedenfor er historikk og beskriver tidligere kilde-/testnivåer.

Full akseptanse er ikke nådd. G3 venter. Evidensroten nedenfor er
`Binding/Implementation/PalazzoBinding-20261012/implementation/` (HAVEN-relativt).

| testRef | Faktisk måling | Status mot hele testen |
|---|---|---|
| test.palazzo.coverage | Tidligere fem startkonfigurasjoner, ferske web-stikkprøver og autentisert Workbench med katalog110. Ingen full ny dynamisk enumerering. | Åpen |
| test.palazzo.appearance | Ett identisk møte-Skeleton og state gjennom web/Binding; fire tilstander x to bredder. Native breddekontekst og preview-ramme rettet. To overlay-regresjoner. Smale knapper synlige. Forskjeller i linjehøyde/tekstjustering finnes fortsatt. | Delbevis; alle Palazzo-flater og fysisk iOS gjenstår |
| test.palazzo.behavior | Møteprototypen: 14 native action-dispatches = 14 web callbacks med identisk komplett payload. Ingen native artikkel/kelner/hus mutation+reload-prøve. | Åpen |
| test.meeting.consent | 22 policytester, 3 celletester (separate signerte deltakeravtaler, ny deltaker, replay, første opprettelse/restore) og felles configuration-test. Ny deltaker, manglende ja, falsk nøkkel, utløp, lease, restart-replay og stoppretry dekket. | Lokal policy består; reell fordelt autorisasjon/mikrofon og målt stopptid gjenstår |
| test.meeting.audio | Read-only Apple Speech viser on-device støtte for nb-NO/en-US på denne Macen. Autorisasjon notDetermined. Ingen lyd innsamlet eller transkribert. | Åpen |
| test.meeting.delivery | Kildekontroll: Correspondence ackMessage er ikke individuell varig mottakerkvittering. | Åpen, ny adapter/kvitteringskontrakt trengs |
| test.meeting.nearby | Plan og Workbench-jobb registrert; ny møtekobling ikke implementert. | Åpen |

## Testbevis

- Sluttkjøring V13 `native-tests-v13-summary.json`:48 passed,0failed,0skipped. Avslag bevares ved omstart; positive ja gjenopprettes aldri. Ugyldige numeriske lokale planvilkår lukker også lydgaten.

- V11 `native-tests-v11-summary.json`: 47 passed, 0 failed, 0 skipped. 25 møte-/Cell-/configuration-tester og 22 eksisterende renderer/overlay-regresjoner.
- V7 `native-tests-summary.json`: historiske 40 passed,0failed,0skipped før V11-utvidelsen.
- `native-actions-summary.json`: snapshot-testen består; `shared-native-actions-final/summary.json` viser 10 rendringer, 0 feil.
- `action-comparison.json`: åtte par,14 native/14 web, alle keypath+payload identiske. Testhandler uten domeneskriv.
- `shared-web-final/evidence.json`: ingen horisontal overflow ved 1280 eller 390 px.
- `comparison.html`: bildepar, syntetiske data, ekte web- og native renderere.
- `provenance.json`: base-revisjoner og kilde-/fixture-hasher. Kandidaten er ikke den installerte appen.
- `INDEPENDENT-REVIEW.md`: kildegrunnlag, rettelser og åpne integrasjonsgrenser.
- `workbench-readback.txt` og `workbench.png`: åtte faktisk registrerte poster og deres status.

V3-bildene underkjennes visuelt selv om en svak OCR-kontroll var grønn. De beholdes som feilbevis.
Ingen tidsmål for last, 250ms stopp, 60min lyd, WER, varig levering eller sletting er bestått med disse testene.

V11 utvider operationID-vern til plan/approve/decline og retter eksakte deltakergrants.
Kildeaudit Explore: 7/7 kontrakter,0feil. Se implementation/STATUS.md og INDEPENDENT-REVIEW.md
under evidensroten; dette er fortsatt runtime-only og ikke varig distribuert møte.

## Oppdatering 2026-10-13 — visuelle møteknapper

Kjetils nye krav er tatt inn i isolert kildekandidat: mindre tekst, ikonknapper,
deltakerkort og Hjelp i chat, samme Skeleton i web/Binding. Alle tidligere ja blir
fortsatt ugyldige når en ny deltaker kommer. Chatknappen bruker eksisterende
Co-Pilot Chat-konfigurasjon uten automatisk overføring av møtedata.
48 relevante tester bestod. 8 idle-renderinger per plattform, 8 native
handlingsrenderinger og 22 identiske handlingspayloads per plattform er kontrollert.
Ingen reell lyd, levering eller chatsamtale er bevist. G3 er ikke klar.
Konkrete bevis og gjenstående forskjeller:
`Binding/Implementation/PalazzoBinding-20261012/implementation/COMPACT-UI-20261013.md`.
Oppdatert sammenligning:
`Binding/Implementation/PalazzoBinding-20261012/design/comparison/index.html`.
Arbeidsbenk B er lest som in-progress, men Åpne gir Something went wrong; pending
oppdatering er lagret på eksisterende jobb i workbench-pending.json, uten duplikat.

## 2026-10-13 — chat og audio: nyeste målte status

Kjetil godkjente det kompakte uttrykket og ba om faktisk chatprøve, opptak og
transkribering, med alles nye ja også ved Nearby-innmelding.
63/0/0 målrettede macOS-tester består. Binding-kandidaten eksporterer full
chatkonfigurasjon, prøvd gjennom faktisk Porthole med autorisasjon på. Installert
Binding ga ikke nyttig hjelpesvar; staging web viste ingen tilkoblet modell.
Ingen godkjent chatsamtale på begge klienter hevdes.

Mikrofon-/Speech-adapter, opptakskoordinator og segmentvis tilbakekalling er
bygget i isolert kandidat. En fjernet deltaker beholder rett til å tilbakekalle
behandling av sitt opprinnelige segment. Sen enhetsfeil påvirker bare egen epoch.
Testsuiten bruker falsk opptaker og syntetisk PCM, ikke fysisk mikrofon.
SpeechTranscriber mangler nb-NO på denne Macen; kort lokal SFSpeech-bane er
bygget. Syntetisk norsk lydfil (7,439 s) er klar; OS-tillatelse er etterspurt,
selve ASR-prøven er ikke kjørt.

Workbench E er verifisert endret til in-progress gjennom autentisert Chrome.
A/B/D/E pågår, C/F/G ready og P done. B-beskrivelsesoppdateringen er fortsatt
forberedt lokalt, ikke bekreftet skrevet. Ingen duplikat opprettet.

Varig møtevert, individuell samtykkedokumentasjon, reell lease-fornyelse,
kryptert lagring/sletting, mottakerlevering og fysisk Nearby-innmelding gjenstår.
Ingen installasjon, merge, deploy eller virkelig opptak. G3 er ikke klar.
Detaljer, logger, kildepatcher og proveniens:
`Binding/Implementation/PalazzoBinding-20261012/implementation/CHAT-AUDIO-20261013.md`.

## Norsk syntetisk Speech-prøve bestått — 2026-10-13 kl. 16:57

Kjetil svarte «Ja, tillat den lokale testen». Opt-in-prøven er nå kjørt og
bestått: 7,439 sekunder syntetisk norsk lyd, nb-NO og
requiresOnDeviceRecognition=true, uten mikrofon. Transkriptet inneholder alle
17 ordene, med deltager i stedet for deltaker og uten referansens tegnsetting.
Ordredigeringsavstand 1/17 etter normalisering; dette er ett syntetisk eksempel,
ikke en generell WER-/60-minutters godkjenning. 1/1 Speech-test bestått i tillegg
til de 63 regresjonstestene. Ingen produktkode endret i denne prøven.
Evidens: `Binding/Implementation/PalazzoBinding-20261012/implementation/synthetic-speech-result-20261013.json`
og `meeting-synthetic-speech-20261013.log` i samme mappe.
Den besvarte OS-forespørselen er fjernet fra forespoersler.json.
Møtevert, mikrofonintegrasjon, Nearby og mottakerlevering er fortsatt uferdig;
E skal fortsatt stå in-progress og G3 er ikke klar.

## Møteflyt 2026-10-13 — isolert kandidat V3

74 lokale tester bestod, 0 feil/0 hoppet over. Kryptert journal og fail-closed
omstart, signerte samtykker med absolutt utløp, eksplisitt start med installert
adapter, opprinnelig mottakergruppe, individuell kryptert innboks og signert
lagringskvittering er implementert/prøvd med syntetiske data. To faktiske
klientobjekter går gjennom autoriserte Cell get/set. Ny deltaker gir fysisk
stop-kall til mock-adapter og null gyldige ja. Sen deltaker får ikke gammel pakke.
17-pakkeprøven sikrer at kvitterte/revokerte segmenter ikke blokkerer resten.

Nearby-invitasjon er koblet til verifisert scanner peer-context, bygget men ikke
radioprøvd. Oppstart/montering i Binding og Palazzo, invitasjonsaksept og
medlemsavtale, samlet audio/ASR/arkiv/sletting og fysisk fler-enhetsprøve gjenstår.
Ingen mikrofon brukt. Ingen installasjon, merge, deploy eller G3.

F/G er endret ready→in-progress på arbeidsbenken, eksakt tittel/status lest tilbake.
P er fortsatt done; ingen implementeringspost er feilaktig lukket.

Detaljer, rålogg, SHA256-proveniens og patcher:
`Binding/Implementation/PalazzoBinding-20261012/implementation/MEETING-FLOW-20261013.md`.
Læring om samtykke gjennom await og mottakerkvittering er anvendt og distribuert
i `cellprotocol-identity-capability-security`.
