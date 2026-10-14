# Bolk 3 og 5 — stoppet ved klientens broabonnement

Oppdragets §3 krever stopp dersom klientens abonnement over broen ikke virker. c150 etablerte autentisert socket og hentet initial state, men Flow-prøven fikk manglende signert data / mislykket eierskapsbevis og tidsavbrudd før noen push-konvolutt ble åpnet. Den påkrevde formålsprøven er derfor ikke grønn. Ingen installer er bygget. Ingen merge, deploy eller sending er gjort.

Kandidaten ligger i eget låst arbeidstre `_worktrees/havenagentd-korr-klient-20261007`, gren `codex/korr-klient-20261007`, fra `origin/main` ea558ba. Endringene er ucommittet; ingen ny commit, push eller PR er laget fordi kandidaten ikke er CI-klar og har kjente åpne feil. Tidligere arbeid er bevart. Ingen andres arbeidstre eller jobb er endret.

CellProtocol er pinnet til det senere publiserte PR63-hodet `b95a0886f730cf9001af69a9b82c9b5eef93aaa8`, etter beslutningen om ny innmeldingskontrakt. P3 har rapportert 77 fokuserte prøver, fullport 1629 bestått + 5 hoppet over + 0 feil og fire CI-kontroller med SUCCESS på eksakt hode. Dette er protokollens bevis, ikke klientens fullport. CP-TAG-KORR.txt manglet ved siste kontroll; ingen tag/merge er gjort.

| Krav | Test | Utfall | Bevis |
|---|---|---|---|
| A1: samme klient for eier og invitert, tekst og vedlegg | Funksjonell lokal red/grønn; fixture-kopi 1 100 037 byte begge veier | Lokal klientfunksjon bestod; autentisert to-profil formålsprøve ikke fullført | `evidence/bolk3-owner-privacy-red-green.txt` |
| A5: håndtrykk og abonnement over autentisert bro | c150, faktisk lokal Vapor/WebSocket, separat vertsvault, ordinær klientforbindelse | Initial state grønn; abonnement/push rød med timeout. Oppdragets stoppregel utløst | `evidence/bolk3-formaalsproeve.txt` |
| A7: direkte Flow, state og manglende historikk | Lokale sequence-0-, recovery-, direkte-push- og dedup-prøver | Lokale prøver bestod; aktuelle socketabonnementet feilet. Ingen automatisk reconnect i kandidaten | `evidence/bolk3-owner-privacy-red-green.txt`; `handoff/K1-REUSABLE-NOTES.md` |
| C2/D3: native signering, fersk autentisering og testnøkkelgrense | Samme sju NativeCorrespondenceApprovalSignerTests, injisert fixture-autentisering | c149: 6 bestått, 1 forventet funksjonell feil; c150 etter retting: 7 bestått, 0 issues. Ekte Touch ID/passord ikke prøvd | `evidence/bolk3-native-red-green.txt` |
| C2: opprettelse, lenke, kode og kort under Trenger deg | Native link/session/store/views-utkast, separat compile-only | Ikke integrert i adminvinduet. b149 stoppet ved actor-isolert requester i en profile-refresh-test; ingen prototypetester kjørt | `handoff/BOLK-3-INTEGRASJON.md` |
| C3: eier fornyer etter utløp og trekker tilbake | Kildegjennomgang og integrasjonshandoff | Ikke vist. join.decide/result mangler levert eierstyrt fornyelsesflyt; signeringstest erstatter ikke nettlevering. Signerte ekstra vilkår må fortsatt avvises ved native fornyelse | `handoff/BOLK-3-INTEGRASJON.md`; `handoff/K1-REUSABLE-NOTES.md` |
| C1: mottaker fra lenke/kode, høyst to håndgrep | Onboarding, agentregistrering, aktiv agent og GUI | Ikke implementert/verifisert som samlet flyt | Ingen GUI-bevis |
| D4: verdier ute av logg | Åtte feil-canaryer røde før statiske feilmeldinger, grønn etter; kildegjennomgang | Avgrensede canaryer bestod. Komplett Mac-app-/produktloggport ikke vist | `evidence/bolk3-owner-privacy-red-green.txt` |
| Bufret kanal må være bundet til opprinnelig vault | To negative forespørsler i c150 | Begge fikk uventet state: 2 issues. Gjennomgåtte rettingspatches forblir unapplied etter stopp | `evidence/bolk3-formaalsproeve.txt` |
| Nedkobling, sen factory, EOF og cache-retirement | Negative lifetime-prøver etter positivt Flow | Ikke nådd; ingen grønn lifetime-port hevdes | `evidence/bolk3-formaalsproeve.txt` |
| Alle eksisterende tester og daemon smoke | Full syv-bundle-port etter broprøven | Ikke nådd i c150. Tidligere c136 nådde 339 tester med 2 feil; ingen grønn fullport | `evidence/bolk3-formaalsproeve.txt` |
| CI-helper og pakkeressurser | Åtte Python-prøver; positiv staging og negative bundle/symlink-prøver | Bestod i b130; dette er ikke klientens Swift-fullport eller installer | b130s køresultat |
| Lokal full formålsprøve | Invitasjon, godkjenning, tekst/vedlegg over 1 MB begge veier, Flow, eierfornyelse, tilbakekall | Ikke fullført; annen vertsgrens positive native prøve teller ikke som klientbevis | `evidence/bolk3-formaalsproeve.txt` |
| Godkjente bilder og faktiske Mac-skjermbilder side ved side | Ekte admin-/mottakerflate | Ikke vist; ingen skjermbilder fra en fungerende produktflyt | Ingen GUI-bevis |
| Bolk 5: ren eksport, universal, Developer ID, notarisation, staple | Bare tillatt etter alle grønne porter | Ikke bygget; forutsetningen er ikke oppfylt | Ingen pakke-, SHA-, spctl- eller lipo-bevis |

## Den avgjørende porten

c149 viste reell funksjonell red for kombinert manipulering av usignerte X25519-deskriptorer. De andre seks native prøvene bestod. Bindingrettingen ble brukt, deretter måtte en Swift 6-kompilatorfeil rettes med immutable Data-basert historisk verifikasjon. Kompilatorfeilen teller ikke som funksjonell red. c150 bygde og kjørte de samme sju prøvene grønt. Disse prøvene bruker kun fixture-autentisering; de viser ikke ekte LocalAuthentication eller ferdig Mac-kort.

c150s socketprøve kjørte én test som feilet med tre issues: to uventet tillatte vault-cacheforespørsler og ett tidsavbrudd ved push. Etter initial state kom diagnostikken «Got no signed data» og mislykket owner proof. Observasjonen lokaliserer feilen til videre operasjon/Flow etter kanalåpning; den beviser ikke hvilken side som er rotårsaken. Ingen skjult fallback eller alternativ transport er brukt.

Positive push-kriteriet og de forventede seks lifetime-issues ble ikke oppfylt. Rettingspatchene for authority/shutdown ble derfor ikke brukt; fullport, produktsnapshot og smoke ble ikke nådd. Historisk liten CP7f87-probe var grønn, men erstatter ikke prøven av nåværende adapter/pinne. Alle bygg og tester gikk via skriptjobber i bane b/c med egne cacher.

## PR #28 og #30

**#28:** åpen kladd på inventarert `5cf3531`, tidligere grønn CI. Anbefaling: ta bare CI-fasevakten og direkte Swift Testing-kjøreren inn via denne grenen når den er grønn, og del ut/rebase den separate provenance-funksjonen. Ikke merge hele PR28 ukritisk som en duplikat av de samme helperendringene. Seks helperfiler er allerede tatt inn i arbeidskandidaten; åtte helperprøver bestod. Provenance-funksjonen er ikke tatt inn. Ingen merge eller lukking er utført.

**#30:** åpen på inventarert `653fb87`, CI-kjøring 37330064662 feilet ved ytre 25-minuttersgrense. Siste utskrift var FourthReviewFixTests, uten at dette beviser feilårsaken. Anbefaling: rebase på de verifiserte fasehelperne og kjør ny full CI før merge. Ikke lukk PR-en som unødvendig på dette beviset. Ingen endring, merge eller lukking er utført.

Denne grenen gjør ikke main grønn i CI ennå: egen Swift-fullport er rød, ny CI er ikke kjørt og ingen CI-klar kladd-PR er åpnet.

## Installeropplysninger

Pakke: ikke bygget; derfor intet filnavn eller SHA-256. spctl og lipo: ikke kjørt. Developer ID-signering, notarisation, staple og manifest etter staple: ikke kjørt. Ingen release-dist er levert. macOS 13 er lest som minimum i dagens manifest; det er ikke et testet universal-release-minimum. Intel, Tahoe og eldre støttede systemer er ikke prøvd. Dagens pakkeoppskrift inkluderer ikke det nye native Menu.app-oppsettet; URL-handler og agentregistrering trenger fortsatt implementering og prøver før pakking.

## Ikke vist og nødvendig neste arbeid

Fungerende aktuelt broabonnement; full klientport; ekte invitasjon/godkjenning og vedlegg begge veier over den aktuelle broen; automatisk gjenkobling; owner-fornyelse etter utløp; signerte conditions/policy-negativer; shutdown/EOF; idempotent native setup og oppdatering av eksisterende klientprofil; agentdiscovery uten ekstra omstart; ekte userPresence; GUI-akseptanse og skjermbilder; CI; universal installasjon.

Senere beslutning §4 utsetter separat nøkkelgruppe og bruker dagens nøkkellagring med fersk LAContext i adminappen. Dette er ikke Keychain-håndhevet userPresence-isolasjon: en prosess med samme brukers nøkkeltilgang kan omgå en appkontroll. Det er den oppgitte beslutningsgrensen, ikke en sikkerhetsgaranti som klienttesten har vist. Ingen produksjons-debug-bypass er lagt til.

Native utkast, unapplied authority-patches og siste kildestatus er bevart under `HAVEN-Deploy/_handoff/KORR-UT/bolk3/` og det egne arbeidstreet. De er uferdige og skal ikke tas rett inn i en installer. Kildebaserte gjenbrukbare funn er bevart i `handoff/K1-REUSABLE-NOTES.md` og fanget med haven_learn.

STATUS: STOPPET — aktuelt klientabonnement over autentisert bro feiler; oppdragets §3 krever stopp, og installerporten er ikke grønn.
