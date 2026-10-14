# Plan — Palazzo i Binding og samtykket møtedokumentasjon

Status: G1, G1-GUI med konkrete rammerettelser og G2 godkjent 2026-10-12. Planen beskriver godkjent arbeid; faktisk delvis implementering og åpne tester står i STATUS.md og TESTRESULT.md. Ingen G3-akseptanse.

## Opprinnelige portsteg (G1-GUI/G2 er nå besvart)

| Når | Hva Kjetil gjør | Hvorfor |
|---|---|---|
| Nå, uten tidsfrist | Se `index.html`, særlig «Ny deltaker», og godkjenn G1-GUI eller angi endringer. | Avtale synlige tilstander før produktkode endres. |
| Etter bildevalget, samme svar er mulig | Godkjenn G2 for denne planen eller angi endringer i de uttrykkelige standardvalgene nedenfor. | Avtale arbeid, behandlingsvilkår og målbare tester. |
| Når testbygget og testplanen er klare | Delta i ett fysisk testmøte med minst tre separate identiteter/enheter, og en fjerde som kommer til. Hver person godkjenner selv i appen. | Bevise ekte mikrofon, enheter, aktivt samtykke, stopp og mottak. Dato avtales senere. |
| Etter fremlagte testresultater | Vurder G3 mot bilder, brukerhandlinger og deltakerkvitteringer. | Godkjenne faktisk resultat. |

Ingen produktimplementering starter før G1-GUI og G2. Ingen tidsfrist gir automatisk godkjenning. Planen foreslår ikke produksjonsdeploy, distribusjon til reelle møtedeltakere eller mikrofonbruk i denne dokumentrunden.

## Valg som G2 skal ta stilling til

Anbefalt første leveranse er et fysisk møte med én valgt opptaksenhet, lokal transkribering på Apple-enheten og privat levering i HAVEN. Systemlyd fra Teams/Zoom og skjult skyfallback inngår ikke. Møteinngang fra Palazzo og Nearby åpner samme private møteinstans; offentlig Palazzo-/scannerflate får aldri lyd eller transkript.

Alle nåværende deltakere må aktivt godkjenne identisk planrevisjon. Ny deltaker, utmelding, ny opptaker eller endret formål, mottakerliste, språk/behandlingsrute eller lagringsvilkår stopper opptaket og krever ny godkjenning fra **alle**, også tidligere deltakere. Restart skjer bare ved et nytt eksplisitt starttrykk fra valgt opptaker etter siste ja. Avslag gir møtet uten opptak, uten automatisk gjentatt forespørsel.

Foreslåtte standardvilkår, synlige før hver godkjenning:

- Lokal Apple Speech, først norsk bokmål og engelsk der valgt enhet faktisk støtter lokal behandling. Ingen lovnad om språkstøtte før maskinvareprøven. Første varighetsmål: 60 minutter uten skjulte hull.
- Kryptert midlertidig rålyd, kun på opptaksenheten. Slett etter ferdig transkript, senest 24 timer etter segmentets slutt. Feil opphever ikke fristen; delvis transkript og eventuell datamangel vises. Rålyd deles ikke.
- Kryptert leveringskø i inntil 7 dager. Ikke levert innen fristen blir «utløpt», med tydelig varsel og eventuell ny eksplisitt delingsrunde. Mottatt pakke har foreslått 30 dagers oppbevaring på mottakerens enhet; forlengelse krever separat aktiv godkjenning fra alle i segmentets opprinnelige deltakersett. Eksport kan ikke tilbakekalles eller garanteres slettet hos andre.
- Automatisk levering av transkript og minimert tillitspakke etter stopp til **alle** i segmentets godkjente mottakerliste. Den som kommer senere, får bare senere segmenter. Eldre segmenter etterdeles bare med separat godkjenning fra berørte deltakere.
- Automatisk transkript merkes som usikkert/ikke godkjent referat. Ingen automatisk navngiving av talere. Rettelser lager ny versjon; opprinnelig tekst og uenighet kan spores.

Kjetil godkjente disse foreslåtte valgene i G2 2026-10-12. Hver faktisk møtedeltaker må likevel selv godkjenne den konkrete møteplanen; G2 er ikke deres opptakssamtykke. Bilder med kvittering eller sletting er syntetiske tilstander, ikke utførte handlinger.

## Hva er bevist nå?

| Grunnlag | Faktisk status | Konsekvens |
|---|---|---|
| Historisk paritetsfangst | Fem Palazzo/concierge-konfigurasjoner × to bredder; ti native action-filer er tomme | Ingen full funksjonell godkjenning. Dynamiske flater og handlinger må med. |
| Installert Binding | Offline bibliotek, bridge reconnect og venting på katalogautentisering observert | Velg sporbar kandidat og gjenopprett faktisk requester-/transportbane før UI-test. Ikke konkluder med manglende brukerrettighet. |
| Palazzo web | Gjest, kelner og hus åpnet. Fersk artikkelhandling ga HTTP 200 uten artikkeltekst | Artikkelens datakjede må undersøkes; webfeilen skal ikke kopieres som ønsket Binding-oppførsel. |
| Ny møteflate | 13 syntetiske tilstander i to bredder via eksisterende web-renderer | Designbevis; ingen native-kompilering, mikrofon, autorisasjon eller levering bevist. |

Grunnlag og avgrensninger: `Binding/Implementation/PalazzoBinding-20261012/REPORT.md`, `parity-matrix.csv`, `evidence/` og denne oppgavens `KONTROLL.md`. Rendererens kildeversjon og hash finnes i `assets/provenance.json`; knappetrykk i `render-evidence.json`.

## Arbeidspakker — én per bladformål

Alle purposeRefs nedenfor har prefiks `purpose://candidate.palazzo-binding-og-samtykket-tale.`. Utfører er Codex på lokal Mac; Xcode bygger/kjører native tester. Kjetils menneskelige teststeg er bare dem i tabellen øverst. Pakkene utføres i rekkefølgen A → B → C, deretter D → E → F → G. Innsikt fra A kan brukes til D, men sikkerhetsprøver må være grønne før E får bruke mikrofon.

| Pakke / purposeRef | Konkret arbeid og avhengighet | Test som skal bestås | Leveranse og evidens |
|---|---|---|---|
| A · `coverage` | Inventer faktisk katalog, fabrikkreturer, navigasjon og alle rolle-/dataavhengige varianter. Velg isolerte checkouts fra dokumentert kandidat; kartlegg eksisterende endringer før integrasjon. Verifiser autentisert appbane, transport og identitet. | `test.palazzo.coverage`: hver inventert flate åpner i Binding, med teller prøvd/total/ukjent; direkte `cellConfiguration`, `configuration`, `helperCellConfiguration` fungerer. | Maskinlesbart manifest med konfigurering/state-hash, rolle, requester, app/CP/Palazzo-SHA, inngang og handlinger; skjermbilde per rad. |
| B · `appearance` | Sammenlign samme payload, data, tema og bredde i faktisk Palazzo-web, Porthole og ekte Binding-host. Rett minste dokumenterte renderer-/tema-/skallavvik. Bevar styleRole/styleClasses, tilgjengelighet, scroll, tilbakevei og kontroller. | `test.palazzo.appearance`: 390/1280, tom/fylt/feil der tilstanden finnes; macOS og iOS skilles. Synlige avvik må rettes eller særskilt legges frem. | Side-ved-side-bilder per inventarrad, avviksliste og nye native bilder med sporbar binær. Historiske bilder teller ikke som ny kandidat. |
| C · `behavior` | Følg artikkelreferansen og missing reaction-read før årsak plasseres i renderer. Test legitim staff-rute. Rett nødvendige kildefeil. Kjør reaksjon, kommentar, treff/samtykke, kelnerbrief, tilbakekalling og husutkast/publisering i isolert testmiljø. | `test.palazzo.behavior`: handling → celle/bridge → faktisk resultat → tilbake → reload. Både nøstet og direkte konfigurasjonsretur. HTTP 200 eller vellykket klikk alene er ikke nok. | Handlingsspor, observerte state-endringer, persistens etter reload og feil/tilbakeveier i `TESTRESULT.md`. |
| D · `consent` | Implementer additiv privat MeetingSessionCell med Explore-kontrakt, revisjoner, deltakeridentitet, eksplisitte ja/nei og opptakstillatelse. Bruk eksisterende resolver-autorisasjon. Atomisk start/stopp mot revisjonsendring, ingen tillit til UI-skjuling. | `test.meeting.consent`: N=2,3,4; ett manglende/nei/utløpt/forfalsket ja; vert forsøker overstyring; samtidig start og ny deltaker; alle tidligere ja ugyldige; offline, revokering, restart, rekkefølge og gamle callbacks. Null lyd før siste gyldige ja. | `contract/meeting-v1.md` realisert i additive celler og tester; ingen core/protokollendring uten eget dokumentert behov. Persistens og autoritet bevises. |
| E · `audio` | Ny møteadapter for mikrofon, kryptert rålyd, lokal ASR, segmenter og sluttranskript. Gjenbruk dokumenterte deler av chat-diktering, ikke chat-komponistflyten. Ikke tilby lokal rute på enhet som mangler lokal støtte. | `test.meeting.audio`: syntetisk lyd og fysisk samtykket møte; 60 min, ingen umerkede hull/duplikater; norsk/engelsk der støttet, mål WER og segmenttid. Foreslått aksept WER ≤20 % på fast rolig testkorpus, separat støymåling. Tillatelser, diskfeil, avbrudd, sletting og restart. | Faktisk mikrofonbevis, enhet/OS/språk/rute, referansetekst, målinger og bekreftet slettehistorikk. Nytt testkorpus legges frem før terskelen brukes. |
| F · `delivery` | Versjoner/hash transkript + minimert tillitspakke; mottakerbundet kryptert outbox/inbox, deduplisering, retry, receipts og oppbevaring. `release` og lokal `sent`-receipt erstatter ikke levering. | `test.meeting.delivery`: hver deltaker åpner samme hash/versjon etter reload; en offline, dobbel avslutning, restart, feil mottaker, sen deltaker, utløpt kø, rettelse og slettefrister. To og ≥3 selvstendige identiteter. | Per mottaker: planlagt/forsøkt/mottatt/lagret/utløpt. Pakke, receipts og autorisasjonsavslag; intet «alle mottatt» før alle har kvittert. |
| G · `nearby` | Legg møteinngangen til eksisterende NearbyScannerSurfaceView og Palazzo-flate. Discovery/invitasjon fører til samme private møte; ingen automatisk opptaksstart. Prøv faktisk radio, bortfall og gjenforening. | `test.meeting.nearby`: to fysiske enheter for discovery, deretter N-personers møte med sen deltaker; privat identitet, manglende tilgang, ingen lyd/transkript i advertisement/lobby. End-to-end til mottak. | Skjermopptak/handlingsspor av begge innganger, fysisk discovery separat fra injiserte fixtures; samlet `ACCEPT.md` mot G1 og godkjente bilder. |

Ingen «alle flater» godkjennes med fast forhåndstalt utvalg. Startlisten er gjest, kelner, hus, concierge-komponent/-flate, artikkel (inkludert tom/feil), samtykke (vanlig/treff/uten treff), husets artikkelutkast og gjest uten artikler. A skal utvide listen når flere finnes. Onboarding, menyinnganger og tilbakeveier inventeres, ikke antas dekket.

## Komponenter og ansvar

Forslag til nye additive modeller og MeetingSessionCell under `CellProtocol/Sources/CellBase/Cells/Meeting/`. Binding eier enhetsadapter, mikrofontillatelser og tydelig opptaksstatus. Konfigurasjonsfabrikk og eventuell tjenesteadapter plasseres i CellScaffold; Palazzo monterer samme private møte. Eksakt persistens-/leveringsadapter avgjøres ved prøve mot eksisterende autorisert entitets-/transportbane, ikke ved å gi en offentlig server ny myndighet.

Leste kilder og navngitte lesere står i `SOURCE-REVIEW.md`. Ikke hele mapper eller hele kjernen er gjennomlest. Modellen er en implementeringsanbefaling fra kildegrunnlaget, ikke bevis på en eksisterende møtecelle.

## Sikker stopp og kjent fysisk grense

Opptakerens lokale stopphandling skal stanse bufferaksept straks i samme serialiserte autoritetsløp; foreslått målt øvre grense er 250 ms fra mottatt stopp på opptaksenheten til siste aksepterte buffer. Fjernendring må nå opptakeren; foreslått kort opptakslease er maksimalt 3 s, med heartbeat hvert sekund. Tidsgrensene er mål som skal testes, ikke målte garantier. Ved frakobling kan en fjernhendelse ikke få øyeblikkelig virkning; denne grensen må være synlig i akseptansen, og opptak stopper når leasen ikke kan fornyes.

Ny person som melder seg i møteflyten må ikke bli aktiv deltaker før opptakeren har bekreftet stopp. Ny person som fysisk kommer inn, kan ikke garanteres oppdaget av scanner. Synlig «Ny deltaker – stopp først», bekreftet fysisk deltakerliste og stopp hos alle er derfor påkrevd. Produktet må ikke love at teknologi oppdager alle hørbare mennesker. Hvis kravet er null lyd av enhver uregistrert forbipasserende, kan det ikke garanteres av denne løsningen; møtesituasjonen må kontrolleres av deltakerne.

## Gjennomføring og bevis

- Isoler produktendringer; primærarbeidstrærne inneholder mye annet arbeid. Ingen eksisterende endringer slettes eller tas inn automatisk.
- Les relevante AGENTS-/skill-instruksjoner ved implementering. Ingen endring av eksisterende committed testkrav for å få grønt uten å legge endringen frem.
- Ta grunnlinje én gang per valgt revisjon/state. Kjør målrettede tester per pakke; ny bred kjøring bare etter endringer som berører den.
- Feil autorisasjon, faktisk lekkasje før samtykke, uventet ekstern behandling eller feil mottaker stanser berørt test/implementeringsbane. Sikre bevis og rett årsaken før ny prøve. Ikke trekk tilbake urelaterte godkjente leveranser.
- Dokumenter `TESTRESULT.md` og `ACCEPT.md` med hver test som bestått/feilet/blokkert, faktisk revisjon og lenke til råbevis. Uavhengig kontroll leser siste tall, bilder og overleveringsmelding før G3.
- Build, installasjon og fysisk test avtales med konkret kandidat når nødvendig. Merge og produksjonsdeploy inngår ikke i denne portgodkjenningen.

## Bilder, brukersteg og begrensninger

`index.html` viser alle 26 kandidatbilder og fem faktiske grunnlinjebilder. Nye møtebilder bruker 13 konkrete Skeleton-konfigurasjoner med syntetiske data, ikke et implementert møte. UI-handlingene blir registrert lokalt; de godkjenner ingen virkelig plan, åpner ingen mikrofon og leverer ingen pakke. Knappenes fixture-operationID må erstattes med nye idempotensnøkler per faktisk handling; identitet kommer fra autentisert kontekst, aldri fra displaynavn.

Fra vist Nearby-utvalg har møteleder ett invitertrykk, deretter ett trykk for komplett deltakerliste; hver deltaker leser og godkjenner (ett trykk hver), så opptakeren starter (ett trykk). Invitasjonsaksept, innlogging og førstegangs OS-tillatelser kommer i tillegg og er ikke ferdig utformet her. Ny deltaker: stopp/legg til, oppdatert liste/plan, ett nytt aktivt ja fra hver og ett nytt starttrykk. Ingen påstand om et målt totalantall brukeroperasjoner.

Native variant, invitasjonsaksept, redigering av plan/deltakerliste, detaljert tillitspakke, rettelsesdialog og alle Palazzo-sammenligninger får egne bilder før deres visuelle implementering. G1-GUI i denne runden gjelder de viste møtetilstandene og Nearby-inngangen; det er ikke forhåndsgodkjenning av usette flater.

## Ekstern dokumentasjon

Kontrollert 2026-10-12: Apple dokumenterer at lokal behandling krever både `supportsOnDeviceRecognition` og `requiresOnDeviceRecognition`. Dette støtter fail-closed rutevalget, men beviser ikke kvalitet eller lang møtestøtte på målmaskinen: [lokal støtte](https://developer.apple.com/documentation/speech/sfspeechrecognizer/supportsondevicerecognition), [krav om lokal behandling](https://developer.apple.com/documentation/speech/sfspeechrecognitionrequest/requiresondevicerecognition).
