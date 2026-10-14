# STATUS - innholdsvern lyd 20260909

- surfaces: binding, cell, gui, web
- tags: agreement, delivery, drm, encryption, grant, hls, music, rights

## Porter
- G1: **GODKJENT av Kjetil 2026-09-21** (FORMAALSSPEC.md, iterasjon 2)
- G2: **GODKJENT av Kjetil 2026-09-21**, med forbehold om vernnivaaene (se D2)
- G1-GUI: **GODKJENT av Kjetil 2026-09-28** - «Vern valg v1 er godkjent som en
  god start». `images/vern-valg-v1.png`, tre posisjoner, default beskyttet.
  «God start» er ikke «ferdig»: flaten kan endre seg naar den generelle
  musikkpubliseringen faar form. Mekanismebildet `vern-mekanisme-v1.png` er en
  forklaring av mekanismen, ikke GUI-et.

## Retning fra Kjetil 2026-09-28 (ikke avgjort, mer kommer)
- Musikkpublisering skal vaere **generell funksjonalitet** som andre artister
  kan bruke - ikke en Butterpop-spesifikk loesning.
- Det skal gaa an aa **knytte profilside eller blogg** til musikkpubliseringen.
- Kan trenge funksjonalitet fra **arrangementer** (vernissage, slippfest).
- Aapent: flytte musikk, profilsider og artistportefoelje til **eget scaffold**,
  eller bare et **eget target i CellScaffold**.

Konsekvens for denne PDD-en: AP2-AP6 maa ikke bygges slik at de forutsetter at
Butterpop er eneste utgiver. Foerste maaling av hvor ille det staar er gjort -
se under.

### Maaling: hvor Butterpop-bundet er musikkpubliseringen i dag (2026-09-28)
Rent navnetelling i `Sources/App`, ikke en revisjon:
- `Controllers/VaporButterpopStudio.swift` - 13 treff
- `Cells/MusicPublishing/MusicWorkspaceReviewCell.swift` - 5
- `Cells/MusicPublishing/MusicPublishingConfigurationFactory.swift` - 2
- De oevrige seks cellene i `Cells/MusicPublishing/` - **null treff**

Det peker mot at delingen allerede stort sett finnes: generelle celler, med
Butterpop-merkingen samlet i HTTP-flaten. `MusicArtistProfileCell` finnes ogsaa
fra foer. Men dette er en telling av navn, ikke et svar paa om eierskap og
tilgang faktisk er per artist. Det maa etterproeves foer noen flytter noe.
- G3: ikke startet

## Avgjoerelser (begge tatt 2026-09-24)
- **D1: JA** - `hls.js` skal inn i webspilleren. Vernet skal virke i Chrome og
  Firefox, ikke bare Safari.
- **D2: lesning A** - tre nivaaer, der mellomnivaaet er et trinn i *vern*, ikke
  i tillatelse:
  1. **beskyttet** - kryptert HLS, noekkel bak samme doer. `cellManaged` + `[.hls]`
  2. **aapen** - ukryptert, men leveres bare til den som er autorisert. Ingen fri
     adresse. `none` + `[.progressive]`
  3. **nedlastbar** - fritt hentbar adresse, merket nedlastbar.
     `none` + `[.progressive, .download]`

  Default er **beskyttet**.

## D2 - tre nivaaer, ikke to (Kjetil 2026-09-21)
Kjetil: «Naar det gjelder fritt hentbar URL maa vi ha et nivaa til - vi er noedt
til aa foelge protokollen og markere den som nedlastbar.»

Funn: protokollen har allerede ordet. `MusicDeliveryMode` har `.download` ved
siden av `.preview`, `.progressive` og `.hls`. Det skal ikke lages noe nytt.

Videre funn, som Kjetil boer vite: `MusicAssetManifest.asObject()` bruker i dag
`deliveryModes ?? [.progressive, .download]`. **Nedlastbar er default naar
ingen sier noe annet.** Butterpops publiseringsloype setter riktignok
`[.progressive]` eksplisitt, saa de publiserte laatene er ikke merket
nedlastbare - men grunnlinja i modellen er det motsatte av det Kjetil har bedt
om, og det maa snus i AP2.

To lesninger av korreksjonen. Losen er i reell tvil og spoer.

**Lesning A (Losens anbefaling)**
1. beskyttet - kryptert HLS, noekkel bak samme doer. `cellManaged` + `[.hls]`
2. aapen - ukryptert, men fortsatt bak den autoriserte doera. `none` +
   `[.progressive]`. Ingen fri adresse.
3. nedlastbar - fritt hentbar adresse, merket `.download`. `none` +
   `[.progressive, .download]`

**Lesning B**
1. beskyttet - som over
2. fritt hentbar URL - ukryptert paa fri adresse, merket `.download`
3. helt aapen fil - som 2, men lytteren faar i tillegg `store`-grant gjennom
   avtalen

Argumentet for A: i B er 2 og 3 teknisk identiske. Forskjellen ligger bare i
hva avtalen sier, og avtale er allerede en egen akse. Da blir det ikke et
vernnivaa, men en avtalevariant forkledd som et vernnivaa. I A er alle tre
faktisk forskjellige i hva som skjer med lyden.

## RETTELSE 2026-09-10 - iterasjon 0 var delvis feil, og feilen var Losens
Jeg fortalte Kjetil at lyd allerede var kryptert i lagring. **Det stemte ikke.**

Verifisert paa serveren, ikke i koden:
```
/app/Database/MusicAssets/assets/music-full-8fc856d23050cb844d96.bin
0000000   I   D   3 002  \0  \0  \0  \0 037   v   T   S
```
`ID3` = vanlig MP3. 16 filer i katalogen, alle publiserte laater ligger i klartekst.

To ting forte til feilen:
1. Krypteringskoden jeg leste (chachaPoly, cellManaged, perTrack) tilhorer
   `MusicIngestCell.ingest` paa `/mvp/ingest/local` - en annen celle paa en annen
   sti. Butterpop publiserer gjennom `MusicAssetStoreCell.storeLocalAsset`, som
   skriver bytene slik de kommer og lar `encryptionPolicy` falle til `.none`.
2. `storeLocalAsset` setter `ciphertextSHA256 = plaintextSHA256 = sha256(data)`.
   Et felt som heter «ciphertext» inneholder hashen av klartekst. Manifestet ser
   kryptert ut selv naar ingenting er kryptert.

Registrert som `lesson.ciphertext-field-held-plaintext-hash` (blocker).

## Valg (Kjetil, 2026-09-10)
- Trinn: segmentert HLS med AES-128, nokkel gjennom samme autorisasjon som lyden.
- To nivaaer: **beskyttet** (kryptert) eller **aapent**. Ikke en matrise.
- Allerede publiserte laater skal krypteres og pakkes om, uten stans og uten aa
  brekke noe. Det skal verifiseres at laatene faktisk spilles.
- Opptak av lyd er akseptert som mulig.

## Konsekvens for omfanget
Jobben er stoerre enn den saa ut. Det er ikke ompakking av allerede krypterte
filer - det er forstegangs kryptering av 16 filer som i dag ligger i klartekst,
mens tjenesten gaar.

## Ingen kode er skrevet
Dette er P0-P1.

## Logg (Losen, natt 24./25.09)
- AP1 (`ddd03491`, lå lokalt fra 21.09) cherry-plukket på main, testet lokalt (grønn med endringen, rød uten; `HAVEN-Deploy/_handoff/VERK/AP1-LOKALTEST.md`), CI grønn, merget som CellScaffold PR #261 01:36Z. I image for main `e6277af1` sammen med musikkstatistikk skive 1. AP2–AP9 ikke rørt.
- 2026-09-25 04:57Z: **I prod.** Main `e6277af1` (metodikk + Butterpop AP1 #261 + musikkstatistikk skive 1 #262): image 36083749837 publisert 04:46Z, staging COMMITTED_VERIFIED 04:48:53Z, prod 04:49:20Z, `/health/build` bekreftet. Kapittel 38 i prod-containeren (9 276 byte). Butterpop 200; `/butterpop/api/workspace/statistics` anonymt 401. Staging lagt tilbake til PR #254-imaget `4dd70c52` 04:57Z (hentesteget feilet fordi imaget bare finnes lokalt; lagt tilbake uten det). Bevis: `HAVEN-Deploy/_handoff/NATT/NATT-B2-UT.md`, `STAGING-TILBAKE.md`.

## RETTELSE 2026-10-06 - AP1 er merget, og Losen sa to ganger at den ikke var det

**Fakta, lest i git 2026-10-06:**
- AP1 ble merget til main **2026-09-25 i PR #261** (`pdd/innholdsvern-ap1-manifest-uten-loegn`,
  commit `2c4004d26`, merget av kjetilh). En annen traad pushet grenen.
- `origin/main` @ `e5c34345` har `ciphertextSHA256: String?` og testen
  `testStoreLocalAssetManifestTellsTheTruthAboutEncryption`.

**Hva Losen sa, og hvorfor det var feil:**
- 2026-10-01: «aldri kompilert, aldri merget, aldri deployet». Lest mot en lokal
  `origin/main` fra 18.09. Losen sa fra om at refen var gammel, men paastod likevel
  «aldri merget» som et faktum. Det var merget seks dager foer.
- 2026-10-05: «kontrollerte paastandene paa nytt mot nye main, og de holder».
  Kontrollen av AP1 var én opptelling - `ciphertextSHA256` ga 6 treff - som Losen
  leste som «ikke merget» uten aa sammenligne med det kjente tallet foer (5) og
  etter (6). Seks treff betydde at den VAR merget. Det var en verifisering som
  ikke verifiserte noe, rapportert som om den gjorde det.

**Det som faktisk staar igjen for AP1:**
- `MusicPublishingCellsTests` staar i `ci/test-exclusions.txt` (hele suiten, siden
  2026-09-01, paa grunn av én test). **AP1-testen har derfor aldri kjoert i CI** -
  bare blitt kompilert. Den har heller aldri kjoert lokalt.
- Negativ kontroll (at testen feiler uten fiksen) er ikke gjort.
- Begge deler ligger i Losen-koeen: `_losen-jobber/jobber/01-musikk-bygg-og-test`.

**Uendret, og naa lest direkte paa main:** ingenting krypterer. `storeLocalAsset`
skriver bytene som de kommer, publiseringsloypa sender ingen `encryptionPolicy`,
det finnes ingen rute for HLS/segmenter/noekkel og ingen `hls.js`. AP2-AP9 er ikke
skrevet.

**Ogsaa merget 25.09 av en annen traad, uten at denne traaden visste det:**
musikkstatistikk skive 1 (PR #262) og fanen Statistikk i Studio (PR #263).
