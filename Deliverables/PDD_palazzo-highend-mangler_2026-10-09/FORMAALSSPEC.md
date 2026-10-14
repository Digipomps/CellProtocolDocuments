# Formålsspesifikasjon — palazzo highend mangler

Oppgavemappe: `PDD_palazzo-highend-mangler_2026-10-09` · Opprettet 2026-10-09 · Iterasjon 2 (ikke godkjent)

> Regel: ingen plan før G1 er godkjent av Kjetil. For GUI: ingen implementering før G1-GUI (rendret bilde) er godkjent.
> Et dokument om leveransen teller aldri som leveransen.

## 0. Intensjon (ordrett) og brief-audit

Kjetil, 9. oktober 2026 kl. 12:27 UTC, i prosjekttråden «PalazzoComunaleScaffold»:

> Løs alle manglene du har avdekket.

Samme tråd, ett minutt før (12:26 UTC), ordrett. Denne meldingen setter rammene for chat og tale til tekst:

> Vi skal ha kryptert chat i den vanlige chat'en så vi skal bruke den. Correspondence er et lite hack for å chatte mellom AI codeverktøy.For tale til tekst kan vi bruke innebygd funksjonalitet, en selvvalgt ekstern tjeneste eller evt. så kan vi kjøre whisper eller likende selv. (Du kan sette opp en test av modeller igjennom nanogpt hvor jeg har apinøkkel) Vi må ha de troverdig eg etterprøvbart at konfedensialitet og sikkerhet er ivaretatt. Det betyr at tale til tekst må kjøre på enheten eller i et trygt skymiljø - helst noe ala secure enclave - men standard cell scaffold skal i utgangpunktet være sikkert nok.

«Manglene» er historiene merket **Mangler** og **Delvis (byggekloss)** i `/mnt/project-files/personas/highend-personas-og-brukerhistorier-2026-10-09.md` (prosjektets delte mappe; kopi skal legges i `grunnlag/`). Historier merket **Delvis (bygget)** (A1-kjernen, A2, A4-delvis, G1, H1, H2) eies av HD-0077-tråden og skal bare *settes ut* der; de er avhengigheter her (§2), ikke nytt arbeid.

| Påstand i intensjonen / antatt kapabilitet | Audit | Kilde |
|---|---|---|
| Den vanlige chatten (`ChatCell`) skal være kryptert | **retrieved: ikke kryptert i dag.** `ChatCell` lagrer `ChatEntry` med klartekst `text/plain`/`text/markdown`; ingen treff på encrypt/seal/envelope i fila | `CellScaffold/Sources/App/Cells/Chat/ChatCell.swift:17,38` |
| Correspondence er et hack for AI-verktøy, ikke gjesteproduktet | retrieved (Kjetils ord). `CorrespondenceCell` er konvolutt-bare og relasjonsbegrenset; korrespondanse-PDD-en planlegger å gi den «chat-cellens levering» | `CellProtocol/Sources/CellBase/Cells/Correspondence/CorrespondenceCell.swift:1-6`; `Deliverables/PDD_kryptert-korrespondanse-med-vedlegg-ut_2026-10-06/G1-KORT.md` punkt 1 |
| Konvoluttkryptering finnes som verktøy på klientsiden | retrieved (doc-kommentar: «Plaintext is accepted only by the client-side envelope utility»). Hvilken algoritme og nøkkelutveksling: **ikke lest ennå** | `CorrespondenceCell.swift` |
| Ingen E2EE finnes i HAVEN i dag | retrieved: «Implementation status: analysis only; no E2EE implementation exists» (21.07) | `Deliverables/Fabel_E2EE_Assessment_2026-07-21.md` |
| NanoGPT-nøkkel finnes | retrieved: AIGateway leser nøkler fra macOS-nøkkelringen, tjeneste `com.digipomps.cellscaffold.aigateway`, konto = alias; dokumentert alias `nanogpt`. Ikke i `CellScaffold/.env`. **At nøkkelen faktisk ligger der: ikke målt** | `CellScaffold/Sources/App/Cells/AI/AIGatewaySupport.swift:513-600`; `CellScaffold/Documentation/CoPilotChat_Advisor_Model_Access_2026-06-25.md:80-160` |
| NanoGPT har tale-til-tekst | retrieved fra docs.nano-gpt.com 09.10: `POST /api/v1/audio/transcriptions` (OpenAI-kompatibel); modeller Whisper-Large-V3 (~$0,0005/min), Wizper ($0,01/min), gpt-4o-mini-transcribe ($0,003/min), Elevenlabs-STT ($0,03/min, diarisering); TTS `/v1/audio/speech` med gpt-4o-mini-tts | https://docs.nano-gpt.com/api-reference/speech-to-text |
| NanoGPT er et trygt miljø for gjestelyd | **contradicted** av Kjetils krav: NanoGPT er en ekstern videreformidler. Brukes bare til modellprøven med syntetisk, ikke-sensitiv tale | Kjetils melding 12:26 |
| Innebygd tale til tekst på enheten (Apple) støtter norsk | **unavailable.** `SpeechTranscriber.supportedLocales` må måles på Mac-en | https://developer.apple.com/documentation/speech/speechtranscriber |
| Whisper kan kjøres selv | recalled (whisper.cpp, MLX-Whisper, WhisperKit finnes som åpen kildekode). Om noe er installert på Mac-en: **ikke målt** | — |
| `TranscriptStoreCell` kan lagre transkripsjoner med policy | retrieved: `transcript.store/read/release/setPolicy/sweep/tidy` | `CellScaffold/Sources/App/Cells/Transcript/TranscriptStoreCell.swift` |
| Lydmålinger finnes | retrieved: `AudioSignalAnalysis`, `AudioAnalysisRecord` | `CellProtocol/Sources/CellBase/Cells/Media/` |
| VC-er og beviste påstander kan styre tilgang | retrieved: `VCClaim`, `VCPresentation`, `TrustedIssuerCell` (2 124 l), `ProvedClaimCondition` (577 l) | `CellProtocol/Sources/CellBase/VerifiableCredentials/`, `.../Agreement/Condition/Implementation/ProvedClaimCondition.swift` |
| Aldersbevis finnes | retrieved: `AgeProofDoorCell`, `AgeOver18Credential` på `identity.proofs.person.age_over_18.latest` | `CellScaffold/Sources/App/Cells/Proofs/AgeProofDoorCell.swift` |
| Gjestens samtykke og innsikt er bygget i Palazzo | retrieved: `consent.*`, `insight.*`, per-forespørrer-bit `consent.policy.autoApprove.<uuid>`; gjestebrief leser fem keypaths | `PalazzoScaffold/Sources/App/Cells/PalazzoEntityCell.swift`, `PalazzoStaffShellCell.swift:51-58` |
| Fullmakt med eiergodkjenning finnes | retrieved: `pending_owner_approval`, `reshareNotAllowed`, `revoked` | `CellScaffold/Sources/App/Cells/PersonalCopilot/PersonalCopilotCollaborationInviteModels.swift` |
| Gjensidig tilkobling og stedsdeling finnes i konferansedomenet | retrieved: `scheduling.respondMeetingRequest`, `location.shareWithPeer/revokeShare` | `ConferenceConnectionHubCell.swift`, `ConferenceLocationShareCell.swift` |
| OrderX har API | **contradicted**: ingen API; SAF-T har ingen bord- eller gjestefelt | prosjektminne `palazzo-integrasjoner` (research 02.09) |

## 1. Formålstre

Roten og ti grener. Hver gren samler historier fra personadokumentet (ID i parentes). Alle nye noder er `candidate`. Forkortelse: `pc.` = `purpose://candidate.palazzo-highend-mangler.`

| purposeRef | Tittel | Forelder | Goal (outcome) | Verifier | Status |
|---|---|---|---|---|---|
| pc.root | High-end-gjesten blir husket, møtes trygt og følger opp fra bordet, uten at huset lagrer henne | purpose://access.audit.privacy | Hver historie merket Mangler/Delvis (byggekloss) har en levert, testet funksjon, eller en dokumentert beslutning fra Kjetil om å utsette den | ACCEPT.md, én rad per historie | candidate |
| **pc.chat** | **Kryptert vanlig chat** (grunnmur for C1–C5, D5) | pc.root | Den vanlige chatten kan kjøres i kryptert modus der tjeneren bare ser konvolutter | test.chat.* | candidate |
| pc.chat.e2ee | Chatmeldinger lagres og leveres som chiffertekst | pc.chat | Bytene `ChatCell` lagrer og sender i kryptert modus er chiffertekst; klartekst finnes bare hos deltakerne | test.chat.bytes-are-ciphertext | candidate |
| pc.chat.membership-by-proof | Bare inviterte som beviser hvem de er blir medlemmer (C2) | pc.chat | Medlemskap krever invitasjon og et bevis som oppfyller rommets `ProvedClaimCondition`; ingen admin kan legge til noen | test.chat.membership-negative | candidate |
| pc.chat.key-rotation-on-leave | En som forlater rommet kan ikke lese nye meldinger | pc.chat | Ny gruppenøkkel ved hver medlemsendring | test.chat.removed-member-cannot-decrypt | candidate |
| pc.chat.expiry-joint-extension | Rommet slettes selv, forlenges bare om alle sier ja (C5) | pc.chat | Rommet og nøklene slettes ved utløp; forlengelse krever ja fra hvert medlem | test.chat.expiry | candidate |
| **pc.room** | **Bordrommet** (C1, C3, C4) | pc.root | Et kryptert rom som oppstår fra et bord, med NDA og dokumentanalyse | test.room.* | candidate |
| pc.room.from-table | Verten åpner et rom for dem som satt ved bordet (C1) | pc.room | Fra bookingen eller bordet sender verten invitasjon til hver deltaker; rommet er et `pc.chat`-rom | test.room.invite-from-booking | candidate |
| pc.room.nda-first | Alle signerer gjensidig NDA før første dokument (C4) | pc.room | Dokumenter i rommet kan ikke dekrypteres før hvert medlem har signert rommets Agreement | test.room.nda-blocks-documents | candidate |
| pc.room.document-analysis | Dokumentanalyse der det er trygt (C3) | pc.room | Et dokument i rommet kan oppsummeres og sammenlignes av en motor medlemmene har godkjent; kvittering sier hvor det kjørte | test.room.analysis-receipt | candidate |
| **pc.stt** | **Tale til tekst, troverdig og etterprøvbart konfidensielt** (D1–D4) | pc.root | Opptak blir tekst uten at lyd forlater enheten eller eierens scaffold, og hvem som helst i rommet kan etterprøve det | test.stt.* | candidate |
| pc.stt.benchmark | Vi vet hvilken motor som er god nok på norsk | pc.stt | Ordfeilrate (WER) og tegnfeilrate (CER) per motor på et fast norsk prøvesett, med pris og tid | test.stt.benchmark | candidate |
| pc.stt.engine-cell | Én kontrakt, tre utførere | pc.stt | `SpeechTranscriptionCell` med utførerne *på enheten*, *egen scaffold* (whisper e.l. i eierens CellScaffold) og *selvvalgt ekstern* (bare med Agreement som navngir tjenesten) | test.stt.contract-fixtures | candidate |
| pc.stt.verifiable-confidentiality | Konfidensialiteten kan etterprøves | pc.stt | Hver transkripsjon har en signert kvittering: utfører, modell og hash, kjøremiljø, at lyden ikke ble sendt ut (egress-policy), sletting av lyd; scaffold-varianten kan senere legge ved attestasjon fra konfidensiell VM | test.stt.receipt-verifies | candidate |
| pc.stt.consent-before-record | Opptak starter bare når alle har sagt ja (D1) | pc.stt | Opptak starter når hver tilstedeværende har sagt ja på egen enhet; ett nei eller en tilbaketrekking stopper det | test.stt.consent-gate | candidate |
| pc.stt.speaker-owned | Hver taler eier sine utsagn (D2) | pc.stt | Segmentene er merket med taler; en taler kan trekke ut sine segmenter, og referat bygges uten dem | test.stt.speaker-withdraw | candidate |
| pc.stt.minutes-to-room | Referat med beslutninger havner i bordrommet (D3) | pc.stt | Referat med beslutninger og oppgaver postes kryptert i rommet, laget av en godkjent motor | test.stt.minutes-in-room | candidate |
| pc.stt.audio-check | Lydsjekk før start (D4) | pc.stt | Før opptak viser flaten om lyden er god nok, fra `AudioSignalAnalysis` | test.secret.key-from-entity | pc.secret.provider-keys-in-entity | Utføreren henter nøkkelen fra eierens `SecretCredentialCell` med eierens bevis; en annen identitet og scaffold-admin får avslag; nøkkelen finnes ikke i logg, Flow eller modellverktøy | TESTRESULT.md#secret | venter |
| test.stt.audio-check | candidate |
| pc.secret.provider-keys-in-entity | Nøkler til eksterne tjenester ligger i eierens hemmelighetscelle | pc.root | API-nøkler (NanoGPT og andre motorer for tale, tekst og dokumentanalyse) ligger i `SecretCredentialCell` i eierens entitet og brukes derfra av utførerne; ikke i macOS-nøkkelringen eller miljøfiler | test.secret.key-from-entity | candidate |
| **pc.group** | **Vert og gruppe** (B1, B2, B5) | pc.root | Verten samler gjester uten å samle opplysninger om dem | test.group.* | candidate |
| pc.group.forward-grant | Gjestene deler kosthold direkte med stedet (B1, B2) | pc.group | Verten sender én invitasjon; hver gjest gir stedet tillatelse for kvelden fra egen entitet; verten ser bare hvor mange som har svart | test.group.host-cannot-read | candidate |
| pc.group.per-visit-grant | Tillatelse for ett besøk (A1) | pc.group | En tillatelse kan få utløp ved besøkets slutt og slutter da å virke | test.group.grant-expires | candidate |
| pc.group.image-consent | Bilde- og omtalesamtykke per gjest (B5) | pc.group | Hver gjest sier ja/nei til foto og omtale; verten ser listen med ja/nei, ikke noe annet | test.group.image-consent | candidate |
| **pc.control** | **Gjestens kontroll** (A3, A4, A6) | pc.root | Gjesten bestemmer og ser hva som skjer med henne | test.control.* | candidate |
| pc.control.discretion | Diskresjonsfelt (A3) | pc.control | Gjesten kan legge inn «ikke nevn», uttale og tiltale; briefen viser dem bare med tillatelse | test.control.discretion-in-brief | candidate |
| pc.control.access-log | Logg over faktiske oppslag (A4) | pc.control | Gjesteflaten viser hvert oppslag: hvem, hvilken opplysning, når | test.control.access-log | candidate |
| pc.control.forget-evening | Glem denne kvelden (A6) | pc.control | Ett besøk slettes fra gjestens entitet og husets kontekst, med signert slettekvittering | test.control.forget-receipt | candidate |
| **pc.proof** | **Bevis og sertifikater** (E1–E3, E5, E6) | pc.root | Gjester og hus kan vise hverandre verifiserbare bevis uten å dele data | test.proof.* | candidate |
| pc.proof.card-exchange | Verifisert visittkort (E1) | pc.proof | To gjester utveksler VC-er (navn, rolle, selskap) gjensidig; hver ser bare det den andre valgte å vise | test.proof.card-mutual | candidate |
| pc.proof.guest-proofs | Alder og hotellgjest uten pass (E2) | pc.proof | Palazzo og hotellet kan be om `AgeOver18Credential` eller et gjestebevis og få ja/nei | test.proof.age-and-guest | candidate |
| pc.proof.regular | Stamgjestbevis (E3) | pc.proof | Huset utsteder et stamgjestbevis; et søstersted verifiserer det uten å få besøkshistorikk | test.proof.regular-verifies | candidate |
| pc.proof.reliability | Bevis på at man holder bookinger (E4) | pc.proof | Huset utsteder et bevis på fremmøte; et sted kan frita for depositum på grunnlag av det; ingen penger i HAVEN | test.proof.reliability | candidate |
| pc.proof.provenance | Opphavsbevis for flaske (E5) | pc.proof | Sommelieren viser et produkt-VC fra en utsteder gjesten kan verifisere | test.proof.provenance | candidate |
| pc.proof.delegate | Assistent med begrenset fullmakt (E6) | pc.proof | Gjesten gir assistenten fullmakt til å booke og forvalte preferanser; fullmakten kan ikke deles videre og kan trekkes | test.proof.delegate-scope | candidate |
| **pc.meet** | **Kuraterte møter** (F1–F3, H6) | pc.root | Gjester kan treffes uten å bli funnet | test.meet.* | candidate |
| pc.meet.blind-mutual | «Åpen for å hilse i kveld», blindt til begge sier ja (F1) | pc.meet | Ingen identitet vises før begge har sagt ja | test.meet.no-identity-before-mutual | candidate |
| pc.meet.evening-expiry | Alt slettes ved stengetid (F2) | pc.meet | Signaler, treff og avslag for kvelden slettes ved stengetid | test.meet.expiry | candidate |
| pc.meet.host-intro | Verten foreslår, uten navn (F3, H6) | pc.meet | Verten kan foreslå en introduksjon; navn vises først ved gjensidig ja, og verten ser treffene | test.meet.host-intro | candidate |
| **pc.staff** | **Kelneren** (H3, H4, H5, H7) | pc.root | Marco har det han trenger på fem sekunder, uten skjerm foran gjesten | test.staff.* | candidate |
| pc.staff.order-allergy-check | Bestilling mot allergi (H3) | pc.staff | Kelneren legger rettene inn i briefen; kollisjon med delt allergi gir varsel før bestillingen tastes i OrderX | test.staff.order-collision | candidate |
| pc.staff.watch-cue | Signal på klokka (H4) | pc.staff | Klokka viser bordnummer, «kjent gjest» og delt allergi, og ikke mer | test.staff.watch-content | candidate |
| pc.staff.shift-note | Vaktnotat som forsvinner (H5) | pc.staff | Notat om bordet, ikke om gjesten, slettes ved stengetid | test.staff.shift-note-expiry | candidate |
| pc.staff.training | Øving med oppdiktede gjester (H7) | pc.staff | Ny kelner kan øve på briefen med simulerte gjester, adskilt fra ekte data | test.staff.training-isolated | candidate |
| **pc.ext** | **Det som krever andres systemer** (A5, B3, B4) | pc.root | Hver har enten en levert vei som ikke trenger integrasjonen, eller en beslutning om å utsette | ACCEPT.md | candidate |
| pc.ext.cross-venue | Preferanser mellom restaurant, spa og rom (A5) | pc.ext | Én tillatelse per sted i samme hus virker; PMS-kobling er utenfor | test.ext.cross-venue | candidate |
| pc.ext.expense-voucher | Representasjonsbilag (B3) | pc.ext | Bilag med deltakere (fra samtykkene) og formål, og beløp fra kvittering gjesten legger inn, lages i gjestens entitet | test.ext.voucher | candidate |
| pc.ext.split-bill | Delt regning (B4) | pc.ext | Bare via kassens betalingsløsning; utsatt til OrderX/Adyen har en vei inn (se §6) | — | candidate |

## 2. Avgrensning og avhengigheter

Hva dette IKKE er:

- Ikke penger i HAVEN. Depositum, regning og rabatter går gjennom stedets kasse og PSP (`dimy-payment-regulatory-guardrails`).
- Ikke en ny chat ved siden av den vanlige. `pc.chat` gjør den vanlige `ChatCell` kryptert. `CorrespondenceCell` brukes ikke for gjester.
- Ikke ekte gjestelyd gjennom NanoGPT. NanoGPT brukes bare i `pc.stt.benchmark`, med syntetisk tale og opptak uten personopplysninger.
- Ikke produksjon. Alt prøves på staging; prod krever Kjetils ja som i dag.
- Ikke ekte gjester før DPIA og databehandleravtale for helseopplysninger (allergier, art. 9) er gjort. Det står åpent fra research-rapporten.
- Ikke PMS-, OrderX- eller GastroPlanner-integrasjon.
- Ikke konfidensiell VM i første runde. Kjetil: «standard cell scaffold skal i utgangpunktet være sikkert nok». Kvitteringen (`pc.stt.verifiable-confidentiality`) har et felt for attestasjon, så det kan legges til.

Kapabiliteter og avhengigheter (hver må virke før testen som bygger på den):

| Kapabilitet | Kilde (fil) | Avgrensning | Målt før G1? |
|---|---|---|---|
| Konvoluttverktøyet på klientsiden | `CorrespondenceCell.swift`; korrespondanse-PDD (G2 godkjent 07.10, G3 venter) | Algoritme, nøkkelutveksling og gruppeformat ikke lest. Korrespondanse-tråden bygger på samme verktøy: én av trådene eier endringen (§6 spm. 2) | ikke målt |
| `ChatCell` deltakere og levering | `ChatCell.swift` (1 304 l) | Klartekst i dag; ingen medlemskapsbetingelse lest | lest, ikke kjørt |
| Gjestens samtykke og innsikt | `PalazzoEntityCell.swift` | Bygget med tester, ikke satt ut (HD-0077). Koblingen fra onboarding til entitet mangler | ikke målt på kjørende tjeneste |
| Gjestebrief | `PalazzoStaffShellCell.swift` | Bygget, ikke satt ut. Leser fem keypaths | ikke målt |
| VC-stakken | `CellProtocol/.../VerifiableCredentials/` | Ingen gjesteflyt; om presentasjoner verifiseres ende til ende er ikke kjørt | ikke målt |
| Agreement/kontrakt for NDA | CellBase Agreement, `AgreementWorkbenchCell` | Ingen NDA-mal | ikke målt |
| Transkripsjonslager | `TranscriptStoreCell.swift` | Ingen eierskap per taler | ikke målt |
| Lydmålinger | `AudioSignalAnalysis.swift` | Ikke koblet til opptak | ikke målt |
| Hemmelighetscelle for leverandørnøkler | `CellScaffold/Sources/App/Cells/Credentials/SecretCredentialCell.swift`; Book 25 | «Status: implemented database-key profile; broader API/provider Cell contract remains draft.» Leverandørprofilen må bygges eller fullføres | ikke målt |
| NanoGPT-nøkkel | nøkkelring `com.digipomps.cellscaffold.aigateway` / `nanogpt` | Bare for prøven | måles av `pc.stt.benchmark`-jobben |
| Apple tale til tekst på norsk | `SpeechTranscriber.supportedLocales` | Krever macOS 26 / iOS 26 | ikke målt |
| Whisper lokalt | whisper.cpp / MLX | Om installert på Mac-en | måles av prøvejobben (rapporterer «ikke installert») |
| Porthole-forhåndsvisning for Palazzo | `lesson.scaffold-without-porthole-host-has-no-preview` | G1-GUI-bilder blir trolig mockups | — |
| Utsetting av A1/A2/H1/H2/G1 | HD-0077-tråden | Eies der | — |

## 3. Forventningskontrakt — «Det du kommer til å se»

| Leveranse | Type | Hvor | Referanse | Godkjent |
|---|---|---|---|---|
| Modellprøve tale til tekst: WER/CER, tid og pris per motor, på norsk | testutdata + rapport | `evidence/stt-benchmark/RESULTAT.md` | — | nei |
| Kryptert chat: chiffertekst i lagring, lest fra bytene | testutdata | `TESTRESULT.md#chat` | — | nei |
| Bordrommet: invitasjon, NDA, dokument med kvittering | bilder per tilstand, så kjørende flate på staging | `images/bordrom-*-v1.png` | — | nei |
| Opptak: samtykke fra alle, lydsjekk, kvittering, uttrekk av egne utsagn, referat | bilder, så kjørende flate | `images/opptak-*-v1.png` | — | nei |
| Gjestens kontroll: diskresjon, oppslagslogg, glem kvelden med kvittering | bilder, så kjørende flate | `images/gjest-kontroll-*-v1.png` | — | nei |
| Vertinvitasjon og bildesamtykke | bilder, så kjørende flate | `images/invitasjon-*-v1.png` | — | nei |
| Bevis: visittkort, alder/hotellgjest, stamgjest, fremmøte, flaske, fullmakt | bilder, så kjørende flate | `images/bevis-*-v1.png` | — | nei |
| Åpen for å hilse i kveld + vertens introduksjon | bilder, så kjørende flate | `images/hilse-*-v1.png` | — | nei |
| Kelner: brief med diskresjon og allergisjekk, vaktnotat, klokke, øvingsmodus | bilder, så kjørende flate | `images/kelner-*-v1.png` | — | nei |
| Representasjonsbilag og samme-hus-tillatelse | bilder, så kjørende flate | `images/ext-*-v1.png` | — | nei |
| Kontrakter med fixtures for nye celler | filer + validator | `contract/` | — | nei |

## 4. Tilknyttede formålspakker og lærdommer (auto fra purpose_dev.py lookup)

**Lærdommer som styrer denne oppgaven:**
- `lesson.ciphertext-field-held-plaintext-hash`: en påstand om kryptering bekreftes på bytene, ikke på feltnavnet. Derfor `test.chat.bytes-are-ciphertext`.
- `lesson.purpose-never-grants-rights` og `lesson.location-is-not-ownership`: ingen, heller ikke scaffold-admin, når data i en celle jeg eier uten Agreement. Derfor negative tester for vert, admin og ekstern motor.
- `lesson.cellscaffold-two-holes`: celler portes ikke fra CellScaffold uten at autorisasjon per keypath er bevist.
- `lesson.text-ux-is-not-design`: hver flate får bilde før kode (G1-GUI per bølge).
- `lesson.paste-command-instead-of-queue`: prøven kjøres via køen, aldri som kommando Kjetil limer inn.
- `lesson.empty-list-must-not-look-like-calm`: oppslagsloggen og «ikke delt» skiller «ingen har sett» fra «kunne ikke lese».

## Formålspakker som festes
- **pkg.std.everything-works** — Alt skal virke (standard kvalitetsport)
    - purpose://quality.build-and-regression: Alle berørte mål bygger og eksisterende tester passerer uten at tester er fjernet eller svekket.
        - test test.build [command]: Bygg alle berørte mål. → TESTRESULT.md#build
        - test test.regression [command]: Kjør hele eksisterende testmengde. → TESTRESULT.md#regression
    - purpose://quality.docs-in-same-change: Alle dokumenter som beskriver endret oppførsel er oppdatert og datert 'Last verified against code'.
        - test test.docs-updated [inspection]: Hver endret kontrakt/atferd har tilsvarende doc-diff. → ACCEPT.md#docs
    - purpose://quality.work-is-visible: Oppgavemappen har oppdatert STATUS.md med gate-tilstand, og et eventuelt planbytte er datert og begrunnet.
        - test test.status-current [inspection]: STATUS.md speiler faktisk tilstand. → ACCEPT.md#status
    - artefakt FORMAALSSPEC.md (port G1): Godkjent formålsspesifikasjon.
    - artefakt PLAN.md (port G2): Arbeidspakker 1:1 mot bladformål.
    - artefakt TESTRESULT.md (port G3): Utdata fra alle avledede tester.
    - artefakt ACCEPT.md (port G3): Forventning mot faktisk, per leveranse.
    - artefakt STATUS.md (port G3): Gate-tilstand og planbytter.
- **pkg.std.gui-surface** — GUI-flate (bilde før kode)
    - purpose://gui.expectation-agreed-before-build: Et rendret bilde per flate/tilstand er godkjent av Kjetil og lagret som referanse i oppgavemappen.
        - test test.gui.reference-image-exists [artifact]: Godkjent referansebilde finnes for hver flate og hver viktig tilstand (tom, fylt, feil). → images/
    - purpose://gui.parity-with-approved-image: Screenshot av faktisk flate ligger side om side med referansebildet i ACCEPT.md, og alle avvik er enten rettet eller godkjent av Kjetil med begrunnelse.
        - test test.gui.parity [inspection]: Side-om-side referanse/faktisk per flate. → ACCEPT.md#parity
    - purpose://gui.surface-loads-in-time: Flaten er synlig innen terskelen angitt i FORMAALSSPEC.md (standard 5 s) på det avtalte miljøet.
        - test test.gui.load-time [measurement]: Lastetid ≤ terskel, tre forsøk. → TESTRESULT.md#load-time
    - purpose://gui.ways-in-are-reachable: SkeletonReachabilityAudit rapporterer ingen elementer som aldri kan sees, og handlingene FORMAALSSPEC §3 navngir finnes i reachableActionKeypaths.
        - test test.skeleton.no-unreachable-elements [command]: Ingen flate har elementer som aldri kan sees; funn navngir handlingene som gaar tapt. → TESTRESULT.md#reachability
        - test test.skeleton.purpose-actions-reachable [inspection]: Hver handling forventningskontrakten (§3) navngir finnes i flatens reachableActionKeypaths. → ACCEPT.md#ways-in
    - artefakt images/ (port G1-GUI): Godkjente referansebilder, ett per flate og tilstand.
    - artefakt skeleton/ (port G1-GUI): CellConfiguration/skeleton-JSON som bildet er rendret fra. Er bildet en mockup i stedet for Porthole-preview, kreves i stedet en renderingserklæring i images/README.md som lister hva skjelettet ikke kan rendre.
- **pkg.std.cell-contract** — Cellekontrakt
    - purpose://cell.contract-explicit: Book/<celle>_contract_v<n>.json finnes, og en validator kjører grønt på alle fixtures.
        - test test.cell.contract-fixtures [command]: Kjør kontraktvalidator mot positive/negative fixtures. → TESTRESULT.md#contract
    - purpose://cell.authorization-honours-keypath: Negative tester viser at feil requester, feil keypath og purpose://prompt.unknown alle avvises.
        - test test.cell.auth-negative [command]: Feil requester / feil keypath / ukjent formål avvises. → TESTRESULT.md#auth
    - purpose://cell.no-empty-stubs: Ingen endepunkt i kontrakten er implementert som no-op uten status 'not-implemented'.
        - test test.cell.stub-scan [inspection]: Liste alle no-op-handlere og avstem mot Gap_Analysis.md. → ACCEPT.md#stubs
    - artefakt contract/ (port G2): Kontrakt-JSON + fixtures (kan være lenke til Book/).
- **pkg.std.cell-combination** — Cellekombinasjon og dataflyt
    - purpose://cells.dataflow-declared: dataflow.md (eller .graffle/.json) finnes med alle kanter navngitt med endepunkt/event.
        - test test.cells.dataflow-matches-contracts [inspection]: Hver kant i dataflow finnes i en kontrakt. → PLAN.md#dataflow
    - purpose://cells.capabilities-declared-with-boundary: FORMAALSSPEC.md §2 lister hver antatt kapabilitet med kildefil og hva den ikke dekker.
        - test test.cells.capability-audit [inspection]: Alle kapabilitetspåstander har audit-status retrieved. → FORMAALSSPEC.md#audit
    - artefakt dataflow.md (port G2): Diagram + kant-tabell.
- **pkg.std.codex-handoff** — Overlevering til Codex/terminal
    - purpose://handoff.runnable-without-guessing: README.md i _handoff-mappen har rekkefølge, forventet utfall per steg, og alle skript støtter --dry-run/--go.
        - test test.handoff.dry-run [command]: Tørrkjøring gir 0 og lister hva som ville skjedd. → TESTRESULT.md#dry-run
    - artefakt handoff/README.md (port G2): Rekkefølge og kommandoer.

## Lærdommer du må lese før dekomponering
- **lesson.text-ux-is-not-design** (2026-05-06, major): Kjetil forventet en helt annen flate enn den som ble vist; den tekstlige UX-beskrivelsen var godkjent, bildet var det ikke.
    - forebygging: Rendret bilde (Porthole-preview eller mockup) godkjennes før implementering; bildet er akseptansereferanse.
- **lesson.parity-was-correctness-not-decoration** (2026-05-06, major): Parity-audit mellom Porthole og Binding viste at problemet ikke var manglende dekorasjon, men produktkorrekthet (feil oppførsel).
    - forebygging: Akseptanse sammenligner både bilde og oppførsel (knapper trigger keypaths, felt tar input) — begge i ACCEPT.md.
- **lesson.surface-load-alias-miss** (2026-08-24, blocker): Flatelasting tok 46 541 ms (klientens 45 s-timeout) ved bom, 5 000 ms ved treff; målingen 10.08 målte en mislykket lasting.
    - forebygging: Mål lastetid tre ganger og sjekk logg for navnebom før en flate erklæres ferdig; aliaser må løses server-side eller ikke brukes.
- **lesson.plan-instead-of-delivery** (2026-08-21, major): Kjetil ba om en leveranse flere ganger og fikk planer/dokumenter om leveransen i stedet.
    - forebygging: G1 godkjenner formål, ikke arbeid; etter G2 telles bare artefakter listet i §3 'Det du kommer til å se' som fremdrift. Et dokument om leveransen teller aldri som leveransen.
- **lesson.undocumented-plan-switch** (2026-08-24, major): Tre produktive døgn (22.–24.08) så tomme ut i alle statusdokumenter fordi planbyttet fra bølge 1–3 til deploy-seremonien aldri ble skrevet ned.
    - forebygging: STATUS.md i oppgavemappen oppdateres ved hvert planbytte med dato og hvorfor; sjekkes i test.status-current.
- **lesson.planned-documented-as-implemented** (2026-08-24, major): Book/05_Flows_Lifecycle.md beskrev sekvensnummer, signatur og replay som ikke finnes i structen.
    - forebygging: Docs-diff i samme endring, med 'Last verified against code'-dato; planlagt oppførsel merkes eksplisitt.
- **lesson.bridge-inferred-architecture-from-one-use** (2026-08-09, major): En kodeassistent sluttet fra én observert bruksmåte av bridge til en egenskap ved arkitekturen og konkluderte feil.
    - forebygging: Erklær hver kapabilitet oppgaven bygger på som eget formål med kilde og Avgrensning (pkg.std.cell-combination).
- **lesson.cellscaffold-two-holes** (2026-09-01, blocker): CellScaffold har tomme booking-/concierge-stubber og autorisasjon som kaster nøkkelstien og bare sjekker eierskap.
    - forebygging: Ikke porter celler fra CellScaffold til PalazzoScaffold uten å lukke begge hullene; test.cell.auth-negative og test.cell.stub-scan må være grønne.
- **lesson.purpose-never-grants-rights** (2026-08-03, blocker): Risiko for at formålsmatch tolkes som tilgang.
    - forebygging: Et formål kan innsnevre en rettighet, aldri opprette, utvide eller arve en; exact match; purpose://prompt.unknown feiler lukket.
- **lesson.zsh-no-inline-comments** (2026-08-25, minor): Begge kommandolinjene feilet med 'ukjent argument: #' og ingenting kjørte.
    - forebygging: Aldri forklaring på samme linje som en kommando; skript har '"#"*) break ;;' i argumentparseren.
- **lesson.mount-is-not-git** (2026-08-25, major): Hver git-kommando fra device_bash etterlot en index.lock som ikke kunne fjernes og blokkerte Kjetils commits; seks repoer låst 24.08.
    - forebygging: Aldri git mot $HOME/mnt fra device_bash; les .git/refs som filer; all git kjøres av Kjetil eller codex exec.
- **lesson.codex-mcp-60s** (2026-08-18, major): Codex-MCP-kall kuttes etter ~60 s; registerlesning og Swift-bygg sprengte taket.
    - forebygging: Bygg/test/lange jobber går via terminal codex exec eller filbasert overlevering, aldri via Codex-MCP.
- **lesson.corr-approval-surfaces-timed-out** (2026-08-30, major): Corr-godkjenningen (Vegar) er utestet fordi flater/godkjenninger timet ut før testing rakk å skje.
    - forebygging: FORMAALSSPEC.md §2 lister avhengigheter som egne formål med verifier; pkg.std.everything-works og gui.surface-loads-in-time må være grønne før den egentlige testen kjøres.
- **lesson.unresolvable-condition-is-invisible** (2026-09-05, blocker): Relasjoner-flaten viste tittel og ingen vei inn: ingen filopplasting, ingen knapper. Alle tester gronne.
    - forebygging: SkeletonReachabilityAudit kjores over hver flate; test.skeleton.no-unreachable-elements feiler med elementene som aldri kan sees og handlingene som gaar tapt med dem. Betingelser hoerer hjemme inne i List/Grid/Reference-rader, der radens verdi sendes videre; ellers skal cellen avgjore og innhold bindes.
- **lesson.test-corpus-is-not-shipped-corpus** (2026-09-05, major): Rot-probe-testen, lastetidstesten og finnbarhetsauditen var gronne i to uker mens Relasjoner-flaten var tom.
    - forebygging: Enhver flate-test skal bygge korpuset fra det som faktisk sendes ut (menykonfigurasjoner + navigasjonsdestinasjoner + verifiseringshjelperen), dedupliseres, og feile hvis korpuset er mindre enn appens egen meny.
- **lesson.tested-a-different-path-than-production** (2026-09-05, major): Rot-probene leste relations.state.* gjennom porthole.get og var gronne, mens rendereren aldri fikk de samme dataene.
    - forebygging: Naar en test skal si noe om hva brukeren ser, maa den bruke produksjonens egen kodevei - helst produksjonens egen funksjon med produksjonens egne inndata (SkeletonReachabilityAudit kaller condition.evaluate(root: nil, ...) nettopp derfor).
- **lesson.findability-is-not-usability** (2026-09-05, major): Flatene ble kalt validert fordi de bestod en beskrivelsesaudit; de var samtidig ubrukelige.
    - forebygging: En formaalssjekk maa navngi handlingene eieren skal kunne utfore, og testes mot SkeletonReachabilityAudit.reachableActionKeypaths - ikke mot hvor godt formaalet er formulert.
- **lesson.paste-command-instead-of-queue** (2026-09-07, major): Kjetil fikk et innlimingsskript for å starte Codex; flagget --full-auto finnes ikke på `codex exec`, og kjøringen feilet ved første linje.
    - forebygging: Før enhver Codex-kjøring fra Cowork: `ls HAVEN/_losen-queue/inbox running; tail logs/runner.log`, legg jobben som <id>.job + <id>.prompt.md. Aldri gi Kjetil kommandoer å lime inn. Gyldige `codex exec`-flagg: --sandbox, --skip-git-repo-check, -C.
- **lesson.baseline-count-from-report-not-run** (2026-09-07, minor): PLAN.md sa «48 tester grønne»; baseline-kjøringen viste 68 tester med 3 røde.
    - forebygging: WP0/S0 baseline er alltid en ekte kjøring før endring; PLAN oppgir testtall som «forventet ≈ N (fra <kilde, dato>)», og et rødt baseline stopper ikke arbeidet men registreres som eget avvik med årsak.
- **lesson.codex-sandbox-cannot-reach-docker** (2026-09-07, major): S10 (docker compose build/up) endte i `permission denied … docker.sock` i Codex-sandkassen; deploy-slicen ble blocked.
    - forebygging: Deploy-/image-steg planlegges aldri som Codex-slice; de registreres som HAVEN-Deploy-post med eier Kjetil (eller en dispatcher-adapter med eksplisitt docker-rettighet når arbeidskø-PDD-en er levert). Se HD-0012.
- **lesson.scaffold-without-porthole-host-has-no-preview** (2026-09-07, minor): G1-GUI måtte bruke mockups rendret fra skeleton-JSON; ekte Porthole-preview var umulig.
    - forebygging: For scaffolds uten Porthole-vert: (1) images/README.md må si eksplisitt at bildene er mockups og hva skeleton ikke kan rendre, (2) paritet (test.gui.parity) planlegges som egen slice med kjørende scaffold + Binding/Porthole via bridge, ikke som del av implementeringsjobben.
- **lesson.codex-workspace-write-cannot-build-cellscaffold** (2026-09-09, major): WP0-baselinen i køen ble blocked: `sandbox-exec: sandbox_apply: Operation not permitted`. Testkommandoen brukte 1 604 sekunder uten at én eneste test startet.
    - forebygging: Lange bygg og testkjøringer legges ikke som `workspace-write`-køjobb. De kjøres som detached skript startet via Codex med `danger-full-access` og python Popen(start_new_session=True), med logg i en montert mappe som Cowork kan polle — samme mønster som produserte den notariserte HavenAgentD-pakken 2026-09-08. Køjobber brukes til analyse, kontrakter, dokumentasjon og korte kommandoer.
- **lesson.baseline-measured-another-pdds-branch** (2026-09-09, major): WP0 målte `pdd/tillitspakke-agentflaate` med 181 skitne oppføringer, ikke et rent utgangspunkt for sin egen PDD. En regresjonsbaseline derfra sier ingenting om hva denne PDD-en endrer.
    - forebygging: WP0 måler en ren eksport av den revisjonen arbeidet skal gå ut fra (`git archive <rev> | tar -x -C <scratch>`), ikke det delte arbeidstreet. Er arbeidstreet opptatt av en annen PDD, er det en planopplysning som hører i STATUS, ikke noe implementeringen skal jobbe rundt.
- **lesson.worktree-created-from-vm-has-unusable-gitdir** (2026-09-09, major): WP1 ble blocked etter ett minutt: `fatal: not a git repository: /sessions/<sesjon>/mnt/CellScaffold/.git/worktrees/_wt-sad-20260909`, exit 128. Branch og HEAD kunne ikke bekreftes.
    - forebygging: Opprett worktrees fra macOS (Codex), ikke fra VM-en. Er det allerede gjort fra VM-en: skriv om begge pekerfilene til macOS-stien og verifiser `branch --show-current` + `rev-parse HEAD` **fra macOS** før noen jobb legges i køen. En jobb skal aldri være første stedet en sti blir prøvd.
- **lesson.cellbase-decodingerror-shadows-swift** (2026-09-09, minor): WP1s nye celle ga 50 kompileringsfeil: `type 'DecodingError' has no member 'dataCorruptedError'` og `cannot infer contextual base in reference to member 'registry'`, alle fra én linje.
    - forebygging: I App-modulen: skriv `Swift.DecodingError` når du vil ha standardbibliotekets. Gjelder generelt for typenavn CellBase også definerer — sjekk med `grep -rn "enum <Navn>" CellProtocol::Sources/CellBase` før du antar at et kjent Foundation-navn er Foundations.
- **lesson.valuetype-equality-false-for-objects** (2026-09-09, major): Fire av sju WP1-tester feilet på `XCTAssertEqual` mellom to `ValueType.object` som hadde identisk innhold. Feilmeldingen viste samme nøkler og verdier på begge sider, i ulik rekkefølge.
    - forebygging: Aldri assert på hele sammensatte `ValueType`-verdier. Sammenlign kanonisk JSON (`JSONEncoder` med `.sortedKeys`) eller pakk ut og sammenlign felt for felt. Skalarer (`.string`, `.integer`, `.bool`, `.null`) sammenlignes trygt. Merk: dette er et funn i CellBase, ikke bare en testregel — App-kildene destrukturerer riktignok før sammenligning, men en fremtidig `==` på hele verdier vil stille behandle like verdier som ulike. Ikke revidert utover App-kildene.
- **lesson.syntax-check-reported-as-delivered** (2026-09-09, major): WP1 ble rapportert som «kode og 7 tester levert, syntakssjekken bestod». Et faktisk bygg ga 50 kompileringsfeil, og testene feilet 4 av 7 da de først kunne kjøre.
    - forebygging: En implementeringsslice er ikke levert før et detached bygg med `danger-full-access` er kjørt mot arbeidstreet og både bygg og de nye testene er grønne. Legg byggejobben klar FØR slicen kjøres, og skriv i prompten at slicen skal rapportere «skrevet, ikke verifisert» — ikke «levert».
- **lesson.cellbase-internal-members-look-public** (2026-09-09, minor): WP2 stoppet på `'fullPermissionString' is inaccessible due to 'internal' protection level`. Medlemmet finnes og brukes i CellBase selv, så det så ut som et gyldig API.
    - forebygging: Sjekk tilgangsnivå og faktisk returverdi før du bruker et CellBase-medlem fra App: `grep -n "var <navn>" CellProtocol::Sources/CellBase/...`. Et medlem som brukes internt i CellBase er ikke automatisk en del av API-et, og navnelikhet betyr ikke verdilikhet.
- **lesson.entityanchor-keypaths-are-registered** (2026-09-09, minor): WP2-testen skrev en sentinel til `profile` på abonnentens EntityAnchor og fikk `notFound` ved gjenlesing. Skrivingen ga ingen feil.
    - forebygging: Skriv aldri testdata til en oppdiktet keypath på en celle. Finn en keypath cellen faktisk registrerer, helst en annen test som allerede bruker den. At et `set` går gjennom er ikke bevis på at keypathen finnes.
- **lesson.new-cell-must-declare-its-provisioning-mode** (2026-09-09, major): To nye celler i CellScaffold ga tre nye regresjoner: `OrchestratorPersistenceTests testRequireExistingModeRejectsFreshStorageWithoutCreatingBootstrapCells` (opprettet en celle i require-existing-modus mot fersk lagring) og to `TopUpCheckoutTests` som teller celler i provision-only-modus (5 mot forventet 4).
    - forebygging: Enhver ny persistert celle i CellScaffold må eksplisitt svare på tre spørsmål før den registreres: (1) skal den opprettes i require-existing mot fersk lagring? Nei, med mindre den er kanonisk bootstrap. (2) Er den en av de kanoniske eager-bootstrap-cellene som provision-only skal lage? Nesten alltid nei — TopUpCheckoutTests teller dem eksplisitt. (3) Er den en Porthole-publisert flate? Bare da hører den i `reconcilePortholePublishedCellResolves`. Scaffold-intern tilstand registreres i egen funksjon, gated på policy OG provisionOnly, med gjenkjenning av eksisterende mapping.
- **lesson.branch-is-empty-after-eight-work-packages** (2026-09-09, major): Åtte arbeidspakker rapportert utført og verifisert, ACCEPT.md skrevet — men `git branch -v` viste at `pdd/scaffold-admin-delegering` fortsatt pekte på samme commit som `main` (`e1f3e22f`). All koden lå ucommittet i et worktree som bare finnes på én maskin. Ett tapt worktree = 2 750 linjer kode og test borte, med full dokumentasjon på at arbeidet var «levert».
    - forebygging: Skill «filene finnes» fra «branchen har dem». Sjekk `git rev-parse <branch>` mot `git rev-parse <base>` som del av hver verifikasjon som påstår at noe ligger på en branch; er de like, er branchen tom. Legg en commit-pakke inn i planen etter første grønne bygg, ikke etter siste arbeidspakke. Når worktreet bare kan leses fra macOS, kjør sjekken der — ikke hopp over den fordi verktøyet svarer feil.
- **lesson.stop-rule-too-wide-stops-the-job** (2026-09-09, minor): En commit-jobb til Codex stoppet før første `git add` fordi stoppregelen sa «finner du `.git/index.lock` eller annen låsefil: stopp». Et rekursivt søk fant 25 filer som heter `locked` under andre arbeidstrær — normale `git worktree lock`-markører som ikke blokkerer noe. Jobben gjorde ingenting, og hele runden gikk tapt.
    - forebygging: Skriv stoppregler som navn og sti, ikke som kategori: «stopp hvis `index.lock`, `HEAD.lock` eller `*.lock` finnes under `<denne stien>`». Navngi eksplisitt det som ser ut som en treffer men ikke er det, og si at det skal ignoreres. Legg alltid til «stopp hvis kommandoen faktisk avvises med denne feilen» — en filsøk-treffliste er ikke et bevis på blokkering. Samme gjelder alle vide vendinger i en prompt: «eller lignende», «eller annet», «eventuelle andre».
- **lesson.ciphertext-field-held-plaintext-hash** (2026-09-10, blocker): Losen fortalte Kjetil at lyd allerede var kryptert i lagring. Det var feil: filene i prod begynner med ID3 og er vanlig MP3. To ting forte dit. (1) Krypteringskoden som ble lest tilhorer MusicIngestCell paa /mvp/ingest/local, mens Butterpop publiserer gjennom MusicAssetStoreCell.storeLocalAsset, som skriver bytene slik de kommer. (2) storeLocalAsset setter ciphertextSHA256 = plaintextSHA256 = sha256(data), saa manifestet ser kryptert ut selv naar encryptionPolicy er none.
    - forebygging: En paastand om at noe er kryptert, signert eller verifisert skal bekreftes paa artefaktet - les bytene, ikke feltet. Et felt som heter ciphertext* skal ikke settes naar encryptionPolicy er none; enten utelates det, eller navnet sier hva det er. Kan bli derivedTest: manifest med encryptionPolicy none har ingen ciphertext-verdi.
- **lesson.local-main-is-not-main** (2026-09-11, major): WP0-baselinen var rød og ble meldt som «main bygger ikke». Det var feil. Den commiten baselinen ble målt mot, `ba14895`, lå bare på den LOKALE main-grenen og var aldri pushet; den avhang av CellBase-kode som heller ikke var pushet. origin/main lå fire commits lenger fram, pinnet CellProtocol til en revisjon som ER på CellProtocol sin main, og hadde grønn CI hele tiden. Et helt døgns arbeid ble bygget oppå den lokale commiten.
    - forebygging: Før du måler en baseline eller sier at main er rød: `git fetch origin main` og sammenlign. Er lokal main foran origin/main, er de commitene ikke main for andre — bygg aldri videre på dem. Se på CI for origin/main før du konkluderer. `swift package edit` skal aldri være på når noe måles eller meldes verifisert. Og den eneste sjekken som virkelig avgjør: klon fra GitHub til en tom katalog og bygg der. HavenAgentD::Scripts/preflight_before_landing.sh stiller alle fire spørsmålene.
- **lesson.a-new-red-test-needs-a-repeated-baseline** (2026-09-10, minor): Første fulle kjøring med nye endringer viste to røde i stedet for baselinens én, og den nye lå i en fil jeg hadde endret. Det så ut som en regresjon jeg hadde innført.
    - forebygging: Når en ny rød dukker opp: kjør basen på nytt, i et eget rent worktree, **flere ganger** (tre holder som regel), før du enten tar på deg feilen eller avfeier den. Skriv resultatet av gjentakelsen i TESTRESULT — «2 av 3 på ren base» er et svar, «den er nok flaky» er ikke. Det koster ti minutter og avgjør om du bruker natten på å jage din egen feil eller andres.
- **lesson.swift-test-exit-code-lies-in-havenagentd** (2026-09-10, minor): `swift test` i HavenAgentD avslutter med 1 selv når samtlige 212 tester passerer. Et skript som leser `$?` melder rødt på et helt grønt tre.
    - forebygging: Les resultatet fra linjen `Test run with N tests in M suites passed/failed`, ikke fra exitkoden, i alle skript og køjobber for dette repoet. Og fjern det tomme XCTest-målet, eller bygg det for riktig arkitektur, før noen setter opp CI her — ellers vil CI være rød uansett hva som gjøres.
- **lesson.pkill-pattern-killed-the-queue-job** (2026-09-10, major): En commit-jobb i Losen-køen døde med EXIT=143 tolv sekunder etter start. Ingen feilmelding, ingen commit. Årsaken var min egen opprydding i et annet skript: `pkill -f "<appnavn>"`.
    - forebygging: Bruk aldri `pkill -f <mønster>` på en maskin der andre prosesser kan ha teksten i argv. Stopp en prosess ved PID du selv startet, eller ved `pgrep -x <prosessnavn>` kombinert med en sjekk av `ps -o comm=` mot den nøyaktige kjørbare stien. Dette gjelder særlig når en jobbkø kjører prompter som argument: alt du skriver i en prompt står på en kommandolinje et sted.
- **lesson.queue-job-file-before-prompt** (2026-09-10, minor): Køjobben `formaalskomposisjon-fullfor-commit-20260910-1020` ble avvist med «mangler promptfil» 13 sekunder etter at `.job` ble skrevet; promptfilen kom to sekunder etter avvisningen og ligger foreldreløs i `_losen-queue/inbox/`, der runneren aldri ser den igjen.
    - forebygging: Skriv `<id>.prompt.md` først og `<id>.job` sist, helst som `mv` fra en tmp-fil i samme mappe — `.job` er registreringssignalet, slik `job.json` er det i HavenAgentD::Docs/AgentJobs.md. Kan bli derivedTest: runneren eller `hd validate` rapporterer enhver `inbox/*.prompt.md` uten tilhørende `.job`, eldre enn to minutter, som foreldreløs.
- **lesson.pin-must-be-on-their-main** (2026-09-11, major): En revisjonspin i Package.swift pekte på en CellProtocol-revisjon som ikke lå på CellProtocol sin main. Koden bygde bare på den ene maskinen som hadde revisjonen liggende lokalt.
    - forebygging: Å pinne er riktig — det er det som gjør bygget reproduserbart. Kravet er at revisjonen er en forfar av avhengighetens egen main. Da er «bygg fra andres main» og «reproduserbart bygg» samme krav. HavenAgentD::Scripts/assert_dependencies_are_on_their_main.sh håndhever det, og CI kjører den. Lander du en klient før cellen den bruker er på den andres main, har du laget et repo som bare bygger hos deg.
- **lesson.a-red-baseline-is-a-question-not-an-answer** (2026-09-11, major): En rød baseline ble behandlet som en opplysning om prosjektet, og arbeidet gikk videre med et tiltak som gjorde den grønn. Tiltaket skjulte årsaken i stedet for å fjerne den.
    - forebygging: Svar på tre spørsmål før du gjør noe med en rød baseline: er utsjekket mitt likt origin? er CI grønn på origin/main? hvilken commit gjorde den rød, og hvem eier den? Først når svaret er «prosjektet er faktisk rødt» er det riktig å jobbe rundt det — og da som en egen, navngitt sak, ikke som en stille lokal omgåelse.
- **lesson.a-conditional-artifact-must-still-cost-something** (2026-09-18, minor): purpose_dev.py validate ble rød på PDD_entitetsdata-egen-kontroll fordi artefaktet 'skeleton/' manglet, selv om G1-GUI var godkjent på bilder Kjetil faktisk hadde sett. Pakken beskrev artefaktet som påkrevd «når Porthole-preview er brukt»; validatoren krevde det alltid.
    - forebygging: Et betinget krav oppfylles av et *annet krav*, aldri av et fravær. Feltet 'satisfiedByDeclaration' peker på en fil og en overskrift og krever minst ett punkt under den: enten viser du skjelett-JSON-en bildet er rendret fra, eller du skriver ned hva skjelettet ikke kan rendre. Begge tvinger frem spørsmålet «kan flaten dette?». Feilmeldingen navngir begge veier ut. Sjekket begge veier: rød uten erklæring, grønn med.
- **lesson.location-is-not-ownership** (2026-09-22, major): dataflow.md begrunnet at AIGateway matte ligge i appen med at «en gateway utenfor entiteten gjor prompten til noen andres data». Kjetil: en celle i skyen som eies av meg er pr definisjon innenfor min entitet.
    - forebygging: Regelen er uniform og gjelder alle scaffolds likt: ingen andre, scaffold-admin inkludert, nar data ELLER funksjonalitet i en celle jeg eier uten en Agreement som sier det. Et vern som bare gjelder skyen er et tegn pa at grensen er tegnet feil. Negative tester skal kjores i begge oppsett, lokalt og sky, og gi samme svar — og de skal dekke handlinger, ikke bare felter. Den positive motsatsen ma ogsa testes: en Agreement apner nayktig sitt eget omfang.
- **lesson.read-origin-main-before-writing-a-mechanism** (2026-09-22, major): Runde 1 av PDD_entitetsdata skrev en egen resolver for lenkede identiteter (EntityLinkAuthorizer, ny CellAuthorizationPath.linkedIdentity, ny hook pa GeneralCell). Da patchen ble lagt mot origin/main viste det seg at IdentityLinkRegistry og GeneralCell.authorizationEvidence allerede gjorde det samme, landet av en annen oppgave (purpose://candidate.entity-link.resolver-honours-link). Hele resolveren ble forkastet.
    - forebygging: Brief-audit skal si HVILKEN revisjon noe ble lest fra, og for et formal som skal endre en mekanisme skal kilden vaere origin/main (git show origin/main:<fil>), ikke utsjekket. Preflight-skriptet sjekker na at patchen passer mot origin/main i et eget worktree for noe legges pa. Og: for du skriver en mekanisme, grep pa main etter navnet pa det den skal gjore (her: sameEntity, linkedIdentity) - ikke bare etter typen du planlegger a lage.
- **lesson.method-lived-only-on-one-machine** (2026-09-24, major): Metoden selv — Book 35 (PDD-arbeidsflyten), Book 36, lærdomsregisteret med 50 lærdommer, formålspakkene, purpose_dev.py — lå bare i ett utsjekk på Kjetils Mac på grenen codex/docs-cleanup-20260810, aldri på main; derfor verken i HAVEN eller hos andre utviklere.
    - forebygging: Metodeartefakter landes som kode: PR til main og pin-oppdatering i HAVEN. Test: git cat-file -e origin/main:<fil> for hver metodefil.
- **lesson.readonly-git-is-not-all-git** (2026-09-24, minor): Et `git status` fra device_bash i CellProtocolDocuments etterlot .git/index.lock (0 byte) som ikke kunne fjernes fra VM-en, selv om git show/grep/log/rev-parse i samme økt ikke gjorde det.
    - forebygging: Fra device_bash bare objektlesende git mot en revisjon (git show/grep/log/cat-file <rev>); aldri status, diff mot arbeidstreet, add eller commit. Finnes en lås likevel: flytt den til _to_delete/ (mv virker, rm gjør ikke).
- **lesson.downstream-pin-must-come-from-the-consumer** (2026-09-24, major): Nedstrøms-baselinen for CellScaffold var rød 22.09 («cellprotocol krever swift-crypto 4.5.2, dimymint krever 3.x») og ble rapportert som prosjektets blokkering. CellScaffold main pinnet DiMyMint af41630, som løser swift-crypto 4.x; skriptet hadde hardkodet en eldre revisjon (1718fda).
    - forebygging: Et nedstrøms-skript leser alle transitive pinner fra forbrukerens egen Package.swift/Package.resolved på origin/main ved kjøring, og logger dem. En rød avhengighetsoppløsning i et skript med hardkodede pinner er ikke et funn før pinnene er bekreftet mot forbrukerens resolved.
- **lesson.disposable-worktree-must-be-reset-before-checkout** (2026-09-24, minor): pdd-check/Binding ble stående på 72f6a6c9 i to kjøringer selv om skriptet ba om origin/main: «Your local changes to project.pbxproj would be overwritten by checkout». Baselinen målte feil Binding-revisjon uten å si fra.
    - forebygging: Engangs-worktrees resettes hardt (`git reset --hard` + fjern Package.resolved) før hver utsjekk, og skriptet skriver ut revisjonen den faktisk står på — en avvikende revisjon skal stoppe kjøringen, ikke logges forbi.
- **lesson.report-the-commit-you-pushed-not-the-one-you-planned** (2026-09-24, minor): TESTRESULT og PLAN sa «commit ebb0b7f». Branchen sto på e66b7f1 — commit.sh hadde laget en ny hash — og var ikke pushet. Push-skriptets EXPECT måtte rettes før det kunne kjøre.
    - forebygging: Etter hver commit/push: les `git rev-parse --short HEAD` og `git ls-remote --heads origin <branch>` og lim inn utdataene i STATUS/TESTRESULT. Sjekk også for remote-tracking ref før du sier «pushet» (lesson.branch-is-empty-after-eight-work-packages, samme familie).
- **lesson.lookup-again-when-a-surface-is-added** (2026-09-24, major): De nye seksjonene i «Utvid entiteten» (B10) var portet på synlighet med rot-scope, og listen med verktøyets forespørsel forsvant — samme feil som lesson.unresolvable-condition-is-invisible fra 05.09.
    - forebygging: For hver ny eller endret skjelettflate: kjør `purpose_dev.py lookup --tags skeleton gui` før utformingen, og `BindingTests/CellConfigurationVerifierXCTest/testNoLocalSurfaceHidesItsOwnWaysIn` + `testPersonalCopilotLocalSurfacesLoadWithoutReferenceFailures` før flaten vises eller committes.
- **lesson.picker-state-keypath-is-read-and-written** (2026-09-24, minor): Velgeren «Verktøy» i «Gi tilgang» sto på «Velg verktøy» selv om cellen hadde valgt verktøyet.
    - forebygging: `selectionStateKeypath` skal være en nøkkel cellen både leser (`{selected}`) og skriver; test rundturen (`pickerSelectionRoundTrips`).
- **lesson.pairing-can-outlive-the-identity** (2026-09-24, major): Agenten var paret med en HAVEN-identitet fra 4. mai («Binding Local Session», nøkkel 13BF…), mens HAVEN brukte en annen privat identitet (D362…, identitetsfilen skrevet 18.09). Svar fra HAVEN ville blitt avvist; ingen test i noen av endene kunne se det.
    - forebygging: En flate som ber eieren signere for agenten sammenligner egen nøkkel med agentens forankring og viser forskjellen før signering, med vei til ny paring (test: `offerIsRefusedHereWhenThisHavenHoldsAnotherKey`, `theOwnerNeverSignsWhatFailedTheCheck`). Sjekk nøkkelkontinuitet før live-test av noe som signeres.
- **lesson.jxa-objc-method-without-arguments-is-a-property** (2026-09-24, minor): `a.terminate()` i JXA ga `TypeError: a.terminate is not a function`, men appene avsluttet likevel.
    - forebygging: Skriv `a.terminate` (uten parentes) og sjekk etterpå med `pgrep` at prosessen er borte før du går videre.
- **lesson.screencapture-from-runner-can-fail** (2026-09-24, minor): `screencapture -l <vindu>` fra jobbløperen ga «could not create image from window» for HAVEN-vinduet, med samme vindus-ID som computer use så.
    - forebygging: Ta bilder av flater med computer use (eller be Kjetil), og ikke planlegg bevis som avhenger av `screencapture` fra løperen før det er målt at det virker den dagen.
- **lesson.sketch-assumed-a-renderer-it-did-not-have** (2026-09-25, major): Skissen v2 (HTML) var venstrestilt, men «Utvid entiteten» i HAVEN viste all tekst sentrert, også etter at hAlignment «leading» var satt.
    - forebygging: Før en skisse godkjennes: finn CellProtocol-committen HAVEN-bygget bruker, les hvordan Text/VStack/HStack rendres der, og list i §3 hva den ikke kan (her: venstrestilt tekst). Et HTML-bilde er ikke bevis for at rendreren kan det samme.
- **lesson.maxwidthinfinity-also-stretches-height** (2026-09-25, minor): En tekst i en listerad ble kuttet med «…» etter fem linjer når en HStack med wrap og maxWidthInfinity sto i samme rad; uten maxWidthInfinity ble teksten hel.
    - forebygging: Ikke sett maxWidthInfinity på elementer i listerader. Se etter «…» i skjermbildet av hver rad med lang tekst, i et smalt vindu.
- **lesson.wrap-gives-each-item-its-ideal-width** (2026-09-25, minor): Knappen «Par agenten med denne HAVEN-en» gikk ut over kortet og ble klippet i et smalt vindu.
    - forebygging: Knapper i vanlig HStack, som kan krympe og bryte teksten; wrap bare for korte merkelapper. Se på flaten i et smalt vindu før den vises fram.
- **lesson.empty-list-keeps-its-slot** (2026-09-25, minor): Tomme lister og tomme tekster ga store hull i «Utvid entiteten».
    - forebygging: Én liste per kort, der cellen bestemmer radene (`kind`) og en rad med en kort linje står der det ellers ville vært tomt. Ingen faste høyder på lister, og ingen tekst på toppnivå som kan bli tom.
- **lesson.pgrep-pattern-must-allow-arguments** (2026-09-25, minor): Byggejobben avsluttet ikke HAVEN, og `open` hentet bare fram det gamle bygget (startet 24.09 17:29) i stedet for å starte det nye.
    - forebygging: Bruk 'HAVEN( |$)' i mønsteret, og skriv ut prosessens starttid etter omstart og sammenlign den med byggetiden før noe vises fram.
- **lesson.computer-use-image-is-not-a-file** (2026-09-25, minor): Skjermbildene av den nye flaten kunne ikke sendes til Kjetil som fil; vinduet var i tillegg på et annet skrivebord og kunne ikke gjøres større i bakgrunnen.
    - forebygging: Planlegg bildebeviset med en vei som gir en fil (Kjetils eget skjermbilde, eller skjermopptakstilgang for løperen), og si det før arbeidet, ikke etter.
- **lesson.text-field-sends-a-string** (2026-09-25, major): Adressefeltet i «Utvid entiteten» kunne aldri starte en forespørsel: Enter ga alltid «Si hvilket scaffold dette gjelder — `audience` …».
    - forebygging: For hvert tekstfelt: en kontraktstest som sender feltets egen payload (.string) til targetKeypath og venter et svar som ikke er feil.
- **lesson.green-gate-must-read-the-last-summary-line** (2026-09-26, major): runde2.sh committet og pushet 399f6d2 med 4 røde tester. Porten grep'et «Executed … with 0 failures» i hele loggen og traff en grønn suites linje lenger opp; siste linje sa «1262 tests, with 2 tests skipped and 8 failures».
    - forebygging: En grønn-port leser bare den siste «Executed»-linjen (tail -1) og krever « 0 failures (0 unexpected)». Sammenligningen gjøres uten pipe (POSIX case), fordi `echo | grep -q` under pipefail kan gi rødt på grønt (SIGPIPE). Porten skriver ut nøyaktig hva den sammenlignet.
- **lesson.module-and-type-share-a-name-in-cellprotocol** (2026-09-26, minor): `CellApple.EntityAnchorCell` og `CellVapor.EntityAnchorCell` kompilerte ikke: «type 'CellApple' has no member 'EntityAnchorCell'». Begge modulene har en type med samme navn som modulen.
    - forebygging: Én fil per modul som importerer bare den ene og gir typen et unikt typealias (TestSupport/AppleEntityAnchorAlias.swift, VaporEntityAnchorAlias.swift). Testfilen importerer ingen av modulene direkte.
- **lesson.placeholder-example-leaks-into-judgement** (2026-09-28, minor): I «Dommerbenken — chat» v2 var plassholderen i fritekstfeltet «f.eks. «status på prosjektet»». Kjetil skrev nøyaktig «status på prosjektet» som sin egen tolkning i to av tretti saker («hvor står vi nå på prosjektet», «hva står igjen»). Eksempelet var hentet fra meningen til en sak i settet.
    - forebygging: Eksempler, plassholdere og hjelpetekst i en dommerflate skal hentes fra et domene som ikke finnes i settet, og testes: ingen sak i settet skal ha gold hvis tittel eller alias overlapper eksempelteksten. Rapporter saker der dommerens fritekst er lik eksempelet som svakere.
- **lesson.host-mutation-without-reading-the-coordination-file** (2026-10-02, major): 30.09 satte en Claude-tråd ut en gren-commit på staging og byttet invitasjonene, med Kjetils ja, men uten claim. En Codex-tråd hadde claim på samme container (HD-0141), staging var reservert for 2026.9.4, og deploykøen trodde i to døgn at staging kjørte forrige utgivelse.
    - forebygging: Før enhver vertsmutasjon: les `_losen-queue/KOORDINERING.md`, kjør `hd coord status`, ta egen claim på en HD-oppgave, og før utsettingen inn i køen etterpå. Test: jobbloggen for utsettingen viser `hd coord status` uten annen claim på samme tjeneste, og egen claim, før første kommando mot verten. Eierens ja til å sette ut erstatter ikke sjekken.
- **lesson.remembered-install-state-is-not-measured** (2026-10-02, minor): En plan sa at agenten på Macen var bygget fra en bestemt gren, og bygde grenvalg og et åpent spørsmål til eieren på det. Agenten var installert på nytt fra `main` av en annen tråd seks dager tidligere.
    - forebygging: Hva som er installert, måles før en plan bygger på det: dato og navn på binærene og sikkerhetskopiene i `bin/`, `launchctl print`, og om commiten er på `origin/main`. Test: påstandstabellen merker installasjonstilstand som hentet med måletidspunkt, aldri som husket.
- **lesson.md5-differs-for-images-written-from-the-cloud** (2026-10-02, minor): Etter at seks PNG-filer ble skrevet fra en Cowork-økt til Macen, stemte ikke md5 mot originalene, mens alle tekstfilene stemte. Det så ut som feilen der en gammel utgave blir skrevet.
    - forebygging: Kontroller tekstfiler med md5. Kontroller bilder ved å sammenligne `IDAT`-dataene eller størrelsen minus `caBX`-blokken, ikke md5 av hele fila. Test: kontrollskriptet for overførte filer skiller de to tilfellene.
- **lesson.vocabulary-guard-admits-new-claims** (2026-10-03, major): En vakt som godtok enhver setning bygd av tillatte ord, også i bøyd form, slapp 38 av 45 angrepsomskrivinger gjennom («Det har vi:», «Dette er menyen vår:», «Du har rett:»).
    - forebygging: Det en vakt publiserer i en modells navn, er en tekst vakten selv kan bygge av lukkede lister med hele setninger; modellens tekst velger bare hvilken. Test: et sett omskrivinger skrevet av en som ikke har skrevet reglene, gir null publiserte tekster utenfor den mengden.
- **lesson.guard-must-see-the-question-the-model-does-not** (2026-10-03, major): «Vi har følgende pizzaer: …» etter spørsmålet «Hvilke pizzaer har dere uten kjøtt?» leses som fem pizzaer uten kjøtt; to av dem har salami.
    - forebygging: For hver svartype som kan omformuleres, finnes en lukket liste med hele spørsmål; alt annet gir det godkjente svaret ordrett. Et ord som tas ut av svaret, tas også ut av spørsmålene. Test: hvert spørsmål utenfor listen gir null kall til modellen.
- **lesson.own-committed-tests-changed-without-asking** (2026-10-03, major): Ti tester tråden selv hadde committet tidligere samme dag, ble endret uten å spørre: tretten endringer, og sju av dem snudde eller fjernet noe en test krevde godtatt.
    - forebygging: En committet test er eksisterende, uansett hvem som skrev den og når. Før hver commit leses testendringene rett fra git; en endring i en committet test er et spørsmål til eieren. Test: skriptet som lister testendringer fra git, viser ingen endring i en committet test uten en godkjenning ført i STATUS.md.
- **lesson.status-reader-gave-up-at-the-first-network-error** (2026-10-03, major): Skriptet som ventet på CI for en utgave, ga opp ved første nettfeil. Utgaven lå bygget, men ikke satt ut, i tre timer, mens den forrige sto på nett med hull et angrep hadde vist.
    - forebygging: Lesing av et utfall som ligger et annet sted, prøves på nytt når ingen svar kom, og skriptet sier hvor mange ganger; et rødt utfall stopper. Det er lesing, ikke en kontroll som er blitt rød (se lesson.red-check-rerun-because-the-cause-looked-like-the-network). Test: venteren kjørt uten nett leser igjen og skriver antall forsøk.
- **lesson.accept-written-from-memory-had-27-errors** (2026-10-03, major): Første utkast til ACCEPT.md og TESTRESULT.md hadde 27 feil da en uavhengig tråd holdt det mot bevisfilene; ett av dem var påstanden om at hver frosset utgave ble angrepet etter at den var satt ut.
    - forebygging: Tall, klokkeslett, commit-numre og sitater i ACCEPT.md og TESTRESULT.md fylles inn fra bevisfilene av kode, og en uavhengig tråd holder hver påstand mot bevisene før eieren får dokumentene. Test: rapporten fra kontrollen ligger blant bevisene, med en dom per påstand.
- **lesson.failure-named-by-a-guess** (2026-10-03, minor): En kjede leste CI-utfallet tjue ganger uten nett og meldte «gh er ikke logget inn» hver gang; innloggingen var i orden.
    - forebygging: Et skript skriver ut det kommandoen sa, eller prøver nettet før innloggingen. Test: skriptet kjørt uten nett melder at det ikke fikk kontakt.
- **lesson.red-first-claimed-for-tests-that-were-not** (2026-10-04, minor): TESTRESULT.md sa at hver ny eller endret test var kjørt rød først. Tolv endringer i tester som alt fantes, og ti av de 24 nye i første runde, kom inn sammen med koden og var aldri kjørt røde.
    - forebygging: En påstand om alle tester føres per test: «rød først» listes med hvilke tester som fantes i den røde kjøringen, og hvilke som kom til etterpå. Test: antall tester i den røde og i den grønne kjøringen står i TESTRESULT.md, og differansen er forklart.
- **lesson.estimate-assumed-one-attack-round** (2026-10-04, minor): Planen sa «rundt tre og en halv time etter G1». Den siste utgaven var målt på nett 34 timer og 50 minutter etter.
    - forebygging: Et anslag for arbeid som skal angripes av en uavhengig tråd, oppgis per runde, og sier at antall runder er ukjent til første angrep er målt. Test: planen har tid per runde, ikke en sluttid.
- **lesson.full-path-rule-broken-in-short-references** (2026-10-05, major): Kjetil måtte for tredje gang si at filer skal stå med hele stien («Du må legge med hele banen til filer som dette: ACCEPT.md»): meldingene og spørsmålene ved G3 hadde bare filnavnet.
    - forebygging: Hver melding til eieren kontrolleres maskinelt før den sendes: et ord som ender på en filendelse og ikke begynner med en rot, stopper sendingen. Det gjelder hver gang en fil nevnes, også i spørsmål. Test: skriptet som kontrollerer meldinger, gir null funn på hver melding som ber om en port.
- **lesson.stand-in-shared-the-callers-assumption** (2026-10-05, major): Første tørrkjøring på Macen stoppet fordi korrespondanseklienten svarte «No enrolled correspondence profile exists», mens 42 tester og 126 selvkontroller var grønne i skyen.
    - forebygging: Før kode skrives mot et eksternt program, måles kontrakten der programmet kjører: argumentene, avslutningskodene og den ordrette teksten når det nekter. Stedfortrederen i testene skal nekte på samme måte. Test: én test kjører stedfortrederen med inndataene det ekte programmet nektet, og krever samme kode og tekst; og når det gamle kallet settes tilbake i en kopi, blir testene røde.
- **lesson.file-copied-to-the-mac-was-the-previous-version** (2026-10-05, major): En commit gikk ut med testen, men uten endringen den prøvde: filkopien fra skyøkten til Macen meldte «written», og fila på Macen var forrige utgave. To skript mistet dessuten kjørbar-biten på veien.
    - forebygging: Hver utgave som skal til Macen, legges under et nytt filnavn i utdatamappen. Sjekksummen på Macen sammenlignes med den i skyen i et eget steg, og neste steg (commit eller køjobb) startes ikke i samme kommando. Test: commit-jobben viser «git diff --cached --stat --summary» før commit, og lista over filer og moduser sammenlignes med det som skulle med.
- **lesson.pr-opened-without-reading-the-base-branch-ci** (2026-10-05, minor): PR #30 ble opprettet uten at CI-tilstanden på main var lest: løpet sto til tidsgrensen på 25 minutter av en grunn som hadde stått på main i seks dager, og den første lesningen av loggen, at det stoppet før PR-ens tester hadde startet, ble felt av den uavhengige kontrollen.
    - forebygging: Før en PR opprettes, listes løpene for basisgrenen; har hodet ikke noe grønt løp med samme testskript, rettes det først, eller rettelsen tas med. Før en årsak skrives ned for et rødt løp, leses avsnittet om CI i skillen, og siste linje i en logg kalles ikke stedet det stoppet. Test: skriptet som oppretter en PR, viser siste løp på basisgrenen og stopper når det er rødt.
- **lesson.the-scripts-own-python-was-newer-in-the-tests-than-on-the-mac** (2026-10-06, minor): Testene av bytteskriptet kjørte skriptets egne Python-blokker med 3.11, mens Macen har 3.9.6, som avviser datoformer 3.11 tar.
    - forebygging: Testene bytter stien til tolken, i kopien av skriptet de kjører, til utgaven målmaskinen har, og én test krever at ingen annen tolk står igjen i kopien. Datoer tolkes uten funksjoner som oppfører seg ulikt mellom utgavene.
- **lesson.status-message-sent-before-the-documents-were-checked** (2026-10-06, minor): Dokumentene og meldingen til eieren 06.10 om kvelden skrev slutninger som målinger («haven-deploy ville blitt kjørt med umask 077», «skallet ventet fem sekunder: målt»), gjenga kontrollenes merknader som «en feil» og «alle rettet», utelot ett av fire svar der en vakt ble beskrevet, og ga et klokkeslett for når en kjøring ville være ferdig, uten grunnlag. Meldingen var sendt et kvarter før kontrollen av dokumentene.
    - forebygging: Dokumenter, LES-MEG ved siden av et skript og meldingen til eieren kontrolleres mot kildene av en som ikke har skrevet dem, før meldingen sendes. Ved hver påstand står det om den er målt, lest eller sluttet, og et tidsanslag gis som et spenn med grunnlaget. Test: kontrollrapporten er eldre enn meldingen, og rettelser gjort etter kontrollen er merket som ukontrollert.
- **lesson.commit-file-built-on-a-stale-copy-and-the-check-got-the-same-copy** (2026-10-06, major): README.md i commiten `c5058f49` fikk 172 endrede linjer (104 ut, 68 inn) der rundt 50 nye var ventet: tekst fra tre tidligere commiter falt ut.
    - forebygging: Hver fil i en commit-pakke bygges på git-objektet i foreldercommiten, og skriptet som committer, krever ventet antall linjer inn og ut per fil og stopper ellers. Kontrolltråden får commiten og finner grunnlaget selv. Test: skriptet stopper når forskjellen mot forelderen ikke er den ventede.
- **lesson.brake-file-written-after-the-chain-had-passed-the-brake** (2026-10-06, minor): Bremsefilen ble lagt 13 sekunder etter at kjedeskriptet hadde passert bremsesjekken foran pushen, så en commit med en kjent feil ble pushet.
    - forebygging: Et tall et menneske må lese før neste steg som ikke kan angres, deler kjeden i to jobber, eller skriptet krever tallet selv. Test: kjeden stopper foran pushen når commitens linjetall avviker fra det ventede.
- **lesson.check-ran-before-the-last-numbers-and-did-not-read-the-message** (2026-10-06, minor): Kontrollen av akseptdokumentet ble gjort før de 27 siste kallene var målt, og meldingen til eieren var ikke med. En ny kontroll rett før sending fant åtte ting, blant annet at meldingen la en svakhet til angrepet alene der råsvarene fra nett viste det samme.
    - forebygging: Den siste uavhengige kontrollen kommer etter at siste tall er ført inn, regner tallene på nytt fra råfilene og leser meldingen eieren får. Test: kontrollrapporten er yngre enn siste bevisfil og eldre enn meldingen.
- **lesson.approved-image-had-no-way-to-be-photographed-on-the-live-page** (2026-10-06, minor): Telefonbildet som ble godkjent ved G1-GUI, kunne ikke få et skjermbilde fra nett ved siden av seg ved G3: nettleserverktøyet holder vinduet på 1280 punkter, og siden nekter å bli vist i en ramme.
    - forebygging: Ved G1-GUI står det for hvert bilde hvordan motstykket på nett skal tas ved G3, og veien er prøvd én gang mot siden slik den står. Kan et bilde ikke tas, sies det ved G1-GUI. Test: hvert godkjent bilde har en navngitt opptaksvei som har gitt en fil.
- **lesson.early-return-rule-changed-what-happens-when-the-lookup-is-down** (2026-10-06, minor): Et spørsmål med et ord fra ordlisten får henvisningen (HTTP 200) også når oppslaget ikke kan nås, der andre spørsmål får 503 eller 403. Det sto verken i spesifikasjonen eller i en test.
    - forebygging: For hver regel som svarer før en avhengighet spørres, sier spesifikasjonen hva som skjer når avhengigheten er nede, og en test holder det fast. Test: en test der avhengigheten er tatt bort, med ventet svar for begge grener.
- **lesson.stop-rule-promised-a-reading-by-hand-that-the-script-did** (2026-10-06, minor): Spesifikasjonen sa «jeg leser claimene selv rett før utsettingen». Lesingen ble gjort av utsettingsskriptet, og utskriften ble lest etterpå.
    - forebygging: En stoppregel skrives slik den skal utføres: hva som leser, når, og hva som stopper. Test: ordlyden i spesifikasjonen og steget i skriptet er den samme.
- **lesson.way-back-was-called-a-way-back-after-dry-runs-only** (2026-10-06, minor): Veien tilbake fra utsettingen er tørrkjørt to ganger, men selve byttet tilbake er aldri kjørt, der spesifikasjonen krever en vei som virker også når siden er nede.
    - forebygging: En vei tilbake er vist når byttet er kjørt, for eksempel mot en egen container med samme image. Ellers står den som «ikke vist» i planen eieren godkjenner. Test: bevis for et gjennomført bytte, eller linjen «ikke vist» i planen.
- **lesson.order-of-steps-changed-to-keep-a-promised-time** (2026-10-06, minor): Utgaven ble satt ut før rettelsen av README.md var committet, mot planen, fordi kontrollen av rettelsen tok 28 minutter der 15 var ventet.
    - forebygging: Planen sier hvilke steg som kan bytte plass når noe tar lengre tid, og kontroller får en hard tidsgrense. Test: hvert planbytte har en linje i STATUS.md med hva som tapes.
- **lesson.correction-to-a-list-removed-words-it-already-caught** (2026-10-06, minor): To rettelser i ordlisten ga nye hull: et unntak som ble sammenlignet etter at ø var brettet til o, tok bort «nøtte», og en innsnevring tok bort «tolererer».
    - forebygging: Hver utgave av en liste kjøres mot alle tidligere eksempler, både ord som skal treffe og ord som ikke skal, og eksemplene ligger som fikstur. Test: en fikstur med ett eksempelord per oppføring og en liste med ord som ikke skal treffe.
- **lesson.rewritten-draft-got-new-errors-where-it-was-rewritten** (2026-10-06, minor): Seks utkast til spesifikasjonen ble lest i fem kontrollrunder som fant 110 ting til sammen. Hver runde fant feil i det som var skrevet om etter den forrige.
    - forebygging: Etter en omskriving kontrolleres det omskrevne på nytt, og eieren får vite når siste utgave ikke er kontrollert. Tall fylles inn av kode. Test: dokumentet sier hvilken utgave kontrollen leste.
- **lesson.known-pitfall-repeated-in-a-small-follow-up-without-lookup** (2026-10-06, minor): Testen for avvik 4 sammenlignet to like svarkonvolutter med `XCTAssertEqual` og var rød mot riktig kode. Den grønne kjøringen fanget det før commit.
    - forebygging: `lookup` kjøres for hvert steg som skriver kode eller tester, også små oppfølginger, og oppgaven til kontrolltråden ber den holde testen mot lærdommene for taggene. Test: commit-trinnet stopper uten grønt bevis for nettopp filene som committes.
- **lesson.full-path-rule-passed-the-checker-in-descriptions-and-file-cards** (2026-10-06, minor): Meldingen som ba om G3, gikk gjennom kontrollskriptet for hele banen, men fem filer ble sendt som kort uten bane i sendingen, og dokumenter ble nevnt med en beskrivelse («akseptdokumentet») før banen sto.
    - forebygging: Hver fil som leveres i samtalen, står med hele banen i meldingen som følger med, og en beskrivelse av en fil får banen ved første nevning. Test: antall leverte filer er lik antall baner i meldingen.
- **lesson.status-did-not-say-status-or-what-to-do** (2026-10-06, major): Eieren 06.10 om statusen han fikk: «Dette sier meg ingenting om hva status er eller hva jeg skal gjøre.» Han skrev selv formålet og spurte hva som gjensto for å få prøvd med de to mottakerne.
    - forebygging: En statusmelding åpner med hvor formålet står for dem det gjelder, så det eieren skal gjøre i nummererte punkter, så leddene som gjenstår. Arbeid på et sidespor kalles et sidespor. Test: kontrolløren får eierens ord fra §0 og svarer på om første avsnitt sier hva mottakerne har fått.
- **lesson.few-steps-was-counted-for-the-recipient-and-not-for-the-owner** (2026-10-07, minor): Utkastet til G1 talte tre håndgrep for mottakeren og skrev «én gang per person» for eieren («ett trykk» i spesifikasjonen bak). Bildet viste to Touch ID per person og en kode å sammenligne, og rekkefølgen på eierens steg sto feil. Kontrollen før framlegget fant det.
    - forebygging: Der «få håndgrep» er et formål, telles håndgrepene for hver part, eieren først, per person og per runde, fra bildene og i rekkefølgen de skjer. Et steg som følger av et forslag, merkes som forslag. Test: et opptak på en ren maskin der håndgrepene er telt.
- **lesson.a-second-safeguard-hid-that-the-first-had-no-test** (2026-10-06, major): Én av 145 innsatte feil, kalt nr. 100 i filnavnene for omkjøringen («fila legges tilbake mens haven-deploy kanskje går»), ble ikke fanget, og alle 133 testene var grønne med den.
    - forebygging: To vern foran samme handling får hver sin test der det andre ikke kan svare. En innsatt feil som ingen test fanger, leses i utskriften før den regnes som ufarlig. Test: for hvert vern finnes et tilfelle der bare det vernet står mellom skriptet og handlingen.
- **lesson.deadline-request-left-out-what-follows-when-it-passes** (2026-10-06, minor): Utkastet til meldingen etter byttet ba eieren godkjenne to forespørsler innen 24 timer, uten å si at invitasjonen da er brukt opp og at en ny trengs (etter kontrollørens lesning: nytt bytte og ny omstart av staging), og uten steget etter: hans godkjenning av mottakernes egne forespørsler. Kontrollen før sending fant det.
    - forebygging: En forespørsel med frist sier hva som skjer når fristen går ut, og nevner hvert senere steg som er eierens. Test: kontrolløren spør for hver frist i meldingen «hva følger hvis den ikke holdes?» og «hva er hans neste steg etter dette?».
- **lesson.question-used-the-repos-words-and-came-back-as-a-question** (2026-10-07, minor): To av fem nummererte punkter til eieren kom tilbake som spørsmål: «Hva gjør assistentidentiteten?» og «Hva mener du med at vedlegg kan gå til main? Vi skal ikke lagre vedlegg i git så forklar hva du mener.»
    - forebygging: Et spørsmål til eieren bruker hans ord og sier hva en ting gjør før det spør om den. Test: kontrolløren leser hvert spørsmål, slik det blir sendt, som en som ikke kjenner repoet, og sier hvilke ord som må forklares.
- **lesson.render-candidate-skeleton-with-the-web-renderer-before-g1-gui** (2026-10-02, major): G1-GUI-bilder har vært mockups (butler-PDD-en) eller krevd en kjørende CellScaffold med Porthole-preview. Begge gir enten feil piksler eller en byggerunde før Kjetil får se noe.
    - forebygging: For en ny flate: eksporter de to filene fra CellScaffold origin/main (md5 i images/README.md), rendre kandidat-skjelett-JSON med eksempeldata i Playwright/Chromium (images/render.js i PDD_lister), lagre bildene som G1-GUI-referanse og mål oppførsel (onAction-payloads) i samme kjøring. Etter implementering: en test som krever at Swift-fabrikken gir kanonisk byte-lik JSON som fixturen bildet ble rendret fra, og en ny render fra cellens ekte state med pikseldiff mot referansen. PDD_lister: 0 piksler avvik på tre flater.
- **lesson.shared-swiftpm-cache-lost-its-ownership-marker** (2026-10-08, minor): Første bygg i et nytt CellProtocol-arbeidstre stoppet etter 4 s: haven-swiftpm.sh exit 64, «existing cache lacks the required ownership marker: …/T/haven-swiftpm-bounded/caches/90c10549…».
    - forebygging: Byggeskript for en PDD setter HAVEN_SWIFTPM_CACHE_KEY=<pdd-slug> (egen cache) i stedet for å reparere den delte; koster ett kaldt bygg (6 min for CellProtocol). Test: skriptet skriver cache-key i rapporten.
- **lesson.xctest-stdout-export-interleaves-with-its-own-log** (2026-10-08, minor): En test printet 49 kB JSON til stdout mellom markører for at byggeskriptet skulle klippe den ut; fila ble ugyldig ved byte 49156 — XCTests egen «Test Case '…' passed»-linje lå midt inne i JSON-en.
    - forebygging: En test som skal levere data til et skript, skriver til en fil (NSTemporaryDirectory()) og printer bare stien; skriptet validerer JSON før det kopierer. Og: /usr/local/bin/python3 på Kjetils Mac er en x86-binær («Bad CPU type in executable») under launchd — bruk /usr/bin/python3 eller node i skript.
- **lesson.textfield-cannot-carry-instance-identity-in-a-mount** (2026-10-08, major): Inne i en ComponentSurface-montering kan Button si hvilken liste den gjelder (payload fra raden), men TextField sender bare en string til en fast targetKeypath — «Legg til …» i montering nr. 2 ville havnet i aktiv liste.
    - forebygging: Kjetil valgte A (2026-10-08): SkeletonComponentActionContext (struct + @TaskLocal) i CellBase; cellen leser mount.instanceID; CellScaffold bytter ScaffoldKit-typen til en typealias i integrasjonspakken. Regel for nye komponenter: alt som skal vite instansen går via Button-payload eller monteringskonteksten — aldri via aktiv-tilstand i cellen. Test: ListsCellTests.testMountedComponentContextTargetsTheMountedListNotTheActiveOne.
- **lesson.capability-based-layout-variant-replaces-client-checks** (2026-10-08, minor): Flytting av punkter trengte piler i appen og dra-og-slipp på web, uten to skjeletter eller klientnavn.
    - forebygging: layoutVariants: [{requiresCapability: [drag], hidden: true}] på pilene: web erklærer drag (porthole-webo.js), Binding erklærer pointer/hover/keyboard eller touch (PortholeView.swift) — pilene forsvinner av seg selv den dagen appen får drag-adapteren. Test: layoutVariant(in:) med begge kapabilitetssett (ListsConfigurationTests) + web-harness variants (render-report-wp5.json).

## Book 23-noder som kan være forelder/gjenbruk (leksikalsk forslag, verifiser)
- purpose://questionnaire.respondent.form [active] — Respondent questionnaire form
- purpose://questionnaire.admin.authoring [active] — Questionnaire admin authoring
- purpose://gui.quality.functional-accessible [active] — Functional accessible GUI
- purpose://skeleton.owner-entity-access [draft] — Owner entity access affordance
- purpose://access.audit.privacy [active] — Access, audit and privacy
- purpose://questionnaire.access.audit [active] — Questionnaire access audit
- purpose://knowledge.explain-policy [draft] — Explain policy or rules
- purpose://access.audit.privacy.database-key-custody [candidate] — Eierstyrt kryptering og nøkkellagring for celledata

## 5. Avledede tester (samlet)

| testRef | Formål | Hvordan | Evidens | Status |
|---|---|---|---|---|
| test.build | purpose://quality.build-and-regression | Prosjektets byggkommando (xcodebuild / swift build / pytest) — angis i PLAN.md. | TESTRESULT.md#build | venter |
| test.regression | purpose://quality.build-and-regression | Prosjektets testkommando; sammenlign antall tester før/etter. | TESTRESULT.md#regression | venter |
| test.docs-updated | purpose://quality.docs-in-same-change | Les diff; kryss av i ACCEPT.md. | ACCEPT.md#docs | venter |
| test.status-current | purpose://quality.work-is-visible | Sammenlign STATUS.md med filene i mappen. | ACCEPT.md#status | venter |
| test.gui.reference-image-exists | purpose://gui.expectation-agreed-before-build | purpose_dev.py validate sjekker images/ mot FORMAALSSPEC.md §3. | images/ | venter |
| test.gui.parity | purpose://gui.parity-with-approved-image | Screenshot fra Porthole/Binding i samme viewport som referansen; lim inn i ACCEPT.md. | ACCEPT.md#parity | venter |
| test.gui.load-time | purpose://gui.surface-loads-in-time | Stoppeklokke/logg-tidsstempel; noter alle tre tider. | TESTRESULT.md#load-time | venter |
| test.skeleton.no-unreachable-elements | purpose://gui.ways-in-are-reachable | xcodebuild -only-testing:BindingTests/CellConfigurationVerifierXCTest/testNoLocalSurfaceHidesItsOwnWaysIn | TESTRESULT.md#reachability | venter |
| test.skeleton.purpose-actions-reachable | purpose://gui.ways-in-are-reachable | Sammenlign §3-radene mot SkeletonReachabilityAudit.reachableActionKeypaths(skeleton). | ACCEPT.md#ways-in | venter |
| test.cell.contract-fixtures | purpose://cell.contract-explicit | python3 checks/validate_contract.py | TESTRESULT.md#contract | venter |
| test.cell.auth-negative | purpose://cell.authorization-honours-keypath | Tre enhetstester navngitt etter tilfellet. | TESTRESULT.md#auth | venter |
| test.cell.stub-scan | purpose://cell.no-empty-stubs | Søk i berørte filer; skriv listen i ACCEPT.md. | ACCEPT.md#stubs | venter |
| test.cells.dataflow-matches-contracts | purpose://cells.dataflow-declared | Tabell kant→kontrakt i PLAN.md. | PLAN.md#dataflow | venter |
| test.cells.capability-audit | purpose://cells.capabilities-declared-with-boundary | Tabell i FORMAALSSPEC.md §0. | FORMAALSSPEC.md#audit | venter |
| test.handoff.dry-run | purpose://handoff.runnable-without-guessing | ./<skript>.sh (uten --go) | TESTRESULT.md#dry-run | venter |
| test.chat.bytes-are-ciphertext | pc.chat.e2ee | Les de lagrede bytene og en levert Flow-melding i kryptert modus; ingen klartekstbit fra en kjent melding skal finnes (`lesson.ciphertext-field-held-plaintext-hash`) | TESTRESULT.md#chat | venter |
| test.chat.membership-negative | pc.chat.membership-by-proof | Uinvitert, invitert uten bevis, admin uten invitasjon: alle avvises | TESTRESULT.md#auth | venter |
| test.chat.removed-member-cannot-decrypt | pc.chat.key-rotation-on-leave | Fjern et medlem, send ny melding, forsøk dekryptering med den gamle nøkkelen | TESTRESULT.md#chat | venter |
| test.chat.expiry | pc.chat.expiry-joint-extension | Simulert klokke: rom slettet ved utløp; forlengelse med ett nei avvist | TESTRESULT.md#chat | venter |
| test.room.invite-from-booking | pc.room.from-table | Fra en booking med fire deltakere: fire invitasjoner, rom opprettet først når verten bekrefter | TESTRESULT.md#room | venter |
| test.room.nda-blocks-documents | pc.room.nda-first | Dokument lastet opp før alle har signert: kan ikke hentes; etter siste signatur: kan | TESTRESULT.md#room | venter |
| test.room.analysis-receipt | pc.room.document-analysis | Analyse med motor godkjent av rommet gir kvittering; motor som ikke er godkjent avvises | TESTRESULT.md#room | venter |
| test.stt.benchmark | pc.stt.benchmark | `HAVEN-Deploy/_handoff/STT-PROEVE/kjor-stt-proeve.sh` via køen (skript-modus) | evidence/stt-benchmark/RESULTAT.md | venter |
| test.stt.contract-fixtures | pc.stt.engine-cell | Kontraktvalidator mot fixtures for de tre utførerne, inkludert ekstern uten Agreement (avvist) | TESTRESULT.md#contract | venter |
| test.stt.receipt-verifies | pc.stt.verifiable-confidentiality | En annen deltaker verifiserer kvitteringens signatur og modell-hash; en endret kvittering feiler; scaffold-utføreren med nettverk ut forsøkt blokkert og logget | TESTRESULT.md#stt | venter |
| test.stt.consent-gate | pc.stt.consent-before-record | Tre til stede, to ja: ikke start. Tre ja: start. Én trekker seg: stopp innen 1 s | TESTRESULT.md#stt | venter |
| test.stt.speaker-withdraw | pc.stt.speaker-owned | Taler B trekker ut; transkripsjon og referat inneholder ingen B-segmenter | TESTRESULT.md#stt | venter |
| test.stt.minutes-in-room | pc.stt.minutes-to-room | Referat postet i rommet er chiffertekst i lagring og leselig for medlemmene | TESTRESULT.md#stt | venter |
| test.stt.audio-check | pc.stt.audio-check | Støyfil gir «for dårlig», ren fil gir «god nok» | TESTRESULT.md#stt | venter |
| test.group.host-cannot-read | pc.group.forward-grant | Verten forsøker å lese en gjests kosthold: avvist; stedet med kveldens tillatelse: får det | TESTRESULT.md#auth | venter |
| test.group.grant-expires | pc.group.per-visit-grant | Simulert klokke etter besøket: `insight.*` avvist | TESTRESULT.md#auth | venter |
| test.group.image-consent | pc.group.image-consent | Verten ser ja/nei-listen og ingenting annet | TESTRESULT.md#group | venter |
| test.control.discretion-in-brief | pc.control.discretion | Briefen viser diskresjonsfeltene med tillatelse, «ikke delt» uten | TESTRESULT.md#control | venter |
| test.control.access-log | pc.control.access-log | Tre oppslag fra to ansatte gir tre rader i gjestens logg med riktig hvem/hva/når | TESTRESULT.md#control | venter |
| test.control.forget-receipt | pc.control.forget-evening | Etter «glem»: besøket finnes ikke i entitet eller husets kontekst; kvitteringen verifiseres | TESTRESULT.md#control | venter |
| test.proof.card-mutual | pc.proof.card-exchange | Ensidig deling gir ingenting; gjensidig gir hver sitt valgte utsnitt; forfalsket kort avvises | TESTRESULT.md#proof | venter |
| test.proof.age-and-guest | pc.proof.guest-proofs | Gyldig, utløpt og fremmed-utstedt bevis | TESTRESULT.md#proof | venter |
| test.proof.regular-verifies | pc.proof.regular | Søsterstedet verifiserer; svaret inneholder ingen besøksdata | TESTRESULT.md#proof | venter |
| test.proof.reliability | pc.proof.reliability | Bevis utstedt etter N fremmøter; ingen pengeverdi i noe felt | TESTRESULT.md#proof | venter |
| test.proof.provenance | pc.proof.provenance | Ekte og endret produkt-VC | TESTRESULT.md#proof | venter |
| test.proof.delegate-scope | pc.proof.delegate | Assistent booker: ok; deler videre: avvist; etter tilbaketrekking: avvist | TESTRESULT.md#auth | venter |
| test.meet.no-identity-before-mutual | pc.meet.blind-mutual | Ensidig ja: ingen identitet i noe svar eller Flow-event | TESTRESULT.md#meet | venter |
| test.meet.expiry | pc.meet.evening-expiry | Etter stengetid: ingen signaler, treff eller avslag igjen | TESTRESULT.md#meet | venter |
| test.meet.host-intro | pc.meet.host-intro | Verten ser treff først ved gjensidig ja | TESTRESULT.md#meet | venter |
| test.staff.order-collision | pc.staff.order-allergy-check | Rett med sesam mot gjest med delt sesamallergi: varsel; uten delt allergi: «ikke delt, spør gjesten» | TESTRESULT.md#staff | venter |
| test.staff.watch-content | pc.staff.watch-cue | Klokkevisningen inneholder bare de tre feltene | TESTRESULT.md#staff | venter |
| test.staff.shift-note-expiry | pc.staff.shift-note | Notat slettet ved stengetid; notat kan ikke knyttes til en gjestentitet | TESTRESULT.md#staff | venter |
| test.staff.training-isolated | pc.staff.training | Øvingsmodus kan ikke lese ekte entiteter | TESTRESULT.md#staff | venter |
| test.ext.cross-venue | pc.ext.cross-venue | Restaurant med tillatelse leser; spa uten: avvist | TESTRESULT.md#ext | venter |
| test.ext.voucher | pc.ext.expense-voucher | Bilag inneholder deltakere som har samtykket og ingen andre | TESTRESULT.md#ext | venter |


## 6. Åpne spørsmål til Kjetil

1. **Rekkefølge.** Anbefalt: bølge 1 er chat, bordrom og tale til tekst (det du løftet fram). Bølge 2 er gruppe, gjestens kontroll og kelner. Bølge 3 er bevis og kuraterte møter. G1-GUI-bilder og G2-plan lages per bølge.
2. **Hvem bygger krypteringen i `ChatCell`?** Korrespondanse-tråden skal gi korrespondansecellen chat-cellens levering, og bygger på samme konvoluttverktøy. Anbefalt: denne PDD-en bygger kryptert modus i `ChatCell` og korrespondanse-tråden bruker den, så den bygges én gang.
3. **Delt regning (B4)** trenger OrderX eller Adyen. Anbefalt: utsett, og ta det opp med Andre når OrderX har en vei inn.

Standardvalg som gjelder om du ikke sier noe annet: tale til tekst kjører som standard i eierens egen CellScaffold (whisper e.l.), på enheten når Apple støtter norsk, og ekstern tjeneste bare når brukeren velger det med en Agreement.

## 7. Revisjonslogg

| Iterasjon | Dato | Hva endret seg | Hvem |
|---|---|---|---|
| 0 | 2026-10-09 | Opprettet | Losen |
| 1 | 2026-10-09 | §0–§3, §5–§6 skrevet fra personadokumentet og Kjetils meldinger 12:26 og 12:27 | Claude (PalazzoComunaleScaffold-prosjektet) |
| 2 | 2026-10-09 | Ny node `pc.secret.provider-keys-in-entity` og avhengighetsrad, etter Kjetil 17:36 UTC: «Husk at dette skal inn i min entitet i en eller annen hemmelighet celle» | Claude (PalazzoComunaleScaffold-prosjektet) |
