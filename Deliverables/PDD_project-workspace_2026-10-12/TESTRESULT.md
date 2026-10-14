# Designkontroll — 2026-10-12

Lokal HTML-kandidat med syntetiske data. Ingen produktakseptanse, Swift-, CI-, native- eller utførertest for nytt prosjektarbeidsrom.

## Målt i Chrome gjennom CUA

- JS-syntaks: `node --check preview/app.js` exit 0 etter siste kildeendring.
- Lys/mørk oversikt og graf rendret ved normal desktopbredde 1512. Grafens kontrollerte bredde hadde ingen horisontal overflow.
- Arbeidsflyt → I kø viste fire eksempler. Teste prosjektisolasjon → detaljer viste riktig prosjekt, oppgave og utfører. Start jobb beholdt jobbtittel i handlingsforhåndsvisningen. Ingen forespørsel ble sendt.
- Legg til i prosjektet viste Ny idé, Ny oppgave og Knytt til eksisterende. Separat prosjektoppretting finnes under Alle prosjekter (kildekontroll).
- Tomflate rendret. Offline/viewer: Rediger prosjekt og Legg til er begge isEnabled=false. Dette beviser GUI-tilstand, ikke autorisasjon.
- Åpne idé viste IDÉ, forklarte at idéen beholdes og tilbød Lag oppgave fra idé. Faktisk type beholdes i kommandokonteksten (kilde).
- Graf: 7 noder/7 kanter; valgt oppgave gav riktig detalj med 3 direkte relasjoner og endelig transform translate(450,255). Forrige fokus gjenopprettet prosjektet; Liste beholdt valgt objekt. Enter på grafnode oppdaterte detaljer.
- Kilden interpolerer noder, kanter og kanttekst i samme SVG over 420 ms. `prefers-reduced-motion` hopper til sluttposisjon. OS-innstillingen er ikke endret eller kjørt; ingen full animasjonssertifisering.
- Etter P2-retting går prosjekt→entitet rundt oppgaven med synlig «bruker», visuelt kontrollert i begge temaer av uavhengig leser.
- 390×844: liste som inngang; Alle prosjekter og privat-/tilgangsmerking isVisible=true. Målt dokumentbredde 390. Viewport tilbakeført etter opptak.
- Console-inspeksjon returnerte ingen error/warn på kontrollert kandidatsteg; ikke kontinuerlig instrumentering av hele testen.

## Korrigerte kontroller

En tastaturprobe søkte grafnode mens Liste var aktiv. En senere opptaksprobe fant også Liste, uten grafnode. Aktiv visning ble inspisert; Graf valgt eksplisitt. Responsivt visningsvalg skjer nå ved inngang, ikke gjennom resize-handler. Endelig valgt-nodeposisjon kontrollert før referansebilder.
En mobilprobe brukte desktopnavn med skjult ikon. Faktisk mobilnavn ble lest og brukt i ny kontroll. Tre reelle P2-designfunn ble rettet og uavhengig etterkontrollert. Feilbilder erstattet før manifestet ble skrevet.

## Gjenstår

Alle seks produkttestene i FORMAALSSPEC §5 står venter: faktisk navigasjon/prosjektisolasjon, tallavstemming, autorisert utføring/bekreftet stopp, fullstendige objektdestinasjoner, privacy, Flow/reconnect. Native, full GUI-paritet, kontrastmåling og tre lastetidsmålinger gjenstår etter implementering.

Hjelpechatens separate manifestlåste testjobb er ferdig: 15/17 testmetoder pass, 2 legacy-journal-konfliktprober fail, exit 1. Rød stoppregel gjelder. Den tester ikke denne designkandidaten. Se nabomappens W1_TEST_RESULT_20261012.md.

## Læring

L-2026-10-12-et-korrekt-projectportfolio-select-svar-er-ikke er applied/synced til haven-gui-testing. Kanon/Codex/Claude oppdatert, Desktop-store og ZIP skrevet av synkverktøyet. Allerede opplastede Cowork-plugin-kopier er ikke oppdatert. Global PDD-/læringskontroll er ikke gjentatt eller erklært grønn.


## 2026-10-13 — testinfrastruktur, fortsatt ingen prosjektakseptanse

G2 godkjent. Prosjektbaseline på main3a668044 er forberedt med eksakt inventar
på 112 eksisterende metoder, men har ikke kjørt. P1–P6 står fortsatt venter.
Ny CP-fortsettelse er uaktivert og avventer brukerord etter det brukte forsøket.
Original CP8: 8 bestått/null feil/Swift exit0; runner stopped på falsk loggtreff,
CS17 ikke kjørt. Original rødt resultat er bevart, ikke ommerket.

Parserens første offline-utkast hadde Python IndexError på regex-gruppeslicing;
rettet til groups() uten å endre tester. Endelig pakke gjenbruker revidert parser
for parvise testkvitteringer/sammenflettet stdout. Alle 19 parser- og 5 prosess-
kontrollmetoder bestod lokalt og uavhengig; kjørt i begge Mac-localer.
Begge pakkers check-modus, bash-syntaks og Python-syntaks bestod. PRECHECK.json
og rålogger finnes i de navngitte pakkene under HAVEN-Deploy/_handoff/ARBEIDSBENK/.
Uavhengig rapport: evidence/test-packets-independent-review-20261013.md.
Ingen Swift-/produkt-/native-/GUI-/CI-/deploybevis er produsert av disse fixturetestene.


## 2026-10-13 15:13Z — lokal prosjektbaseline rød

112 avtalte tester kjørt: 111 besto, én feilet (PortholeConfigurationLoadingTests, linje 1806). Den gamle testen forventer approve-knappen som ble erstattet av request/recheck i commit 21219a834. Se BASELINE-REPAIR-20261013.md og evidence/baseline-failure-20261013.json. Forslag til avgrenset committed-testrettelse ligger som patch; ikke anvendt. Ny engangskjøring foreslås med 116 tester (112 + fire eksisterende AdminAccessBannerTests), og deretter ukjørte CP8→CS17 bare ved grønt. Krever godkjenning av testendring og ny kjøring etter rødt; eksisterende G2 er uendret. Ingen prosjektkode, CI eller deploy.

## 2026-10-13T22:01:29.256750+00:00 — R1 verified green; CP continuation awaits owner activation

R1 completed21:40:13Z with116/116 exact named tests passed, no skips/failures, both exit codes0, source3a668044 and remote CellProtocolb4100f57. Frozen test/script hashes, source status, before/after/current pins and actual managed-cache dependency match. Queue .done and terminal receipt exist. Evidence: `evidence/baseline-r1-reconciled-20261013.json`. This verifies the repaired baseline, not CP8 or CS17.

At22:00Z running/ was empty and CP8→CS17 still had no ADMISSION/attempt/result. Attempt to contact the same Claude queue owner through the authorized native GUI was blocked because the Mac is locked. No message was sent in that attempt, and no alternative executor/admission was created. A scoped handoff is appended to _losen-queue/KOORDINERING.md; saving it does not prove the owner was awakened or acknowledged it. Existing CP8→CS17 approval remains valid and unused. Manual unlock is required for direct follow-up through this GUI.

## 2026-10-14 — CP8 grønn; CS17 stoppet før tester, ny pakke sperret

Dette erstatter forrige status om at CP8→CS17 ikke hadde startet. Eier aktiverte
2026-10-13T22:06:28Z. Eksakt CP8/8 er avstemt mot råloggen, kildehashene og
gjenopprettede pins. CS17 stoppet22:12:47Z i SwiftPM-oppsett før tester fordi
DiMyMicropayments ikke gjenkjente CP-kandidatens mappenavn. Se
`evidence/cp8-cs17-reconciled-20261014.json`. Baseline116 er fortsatt grønn.

Engangsforsøket er brukt. Ingen test eller produktkode er endret. Ny kildeidentisk
detached CP-kopi med mappeblad CellProtocol og CS17-only pakke er klargjort og
kontrollert uten Swift. Manifest102f027723dee2aab2fb2bd639978c4c8db39094bdf8d1be203d08a1e36157d5; AUTHORIZATION=false, ingen ADMISSION eller
attempt. Les `CS17-SETUP-REPAIR-20261014.md` før ny godkjenning/aktivering.
Oppfølgingen forblir PAUSED ved stopp i egen kjede. Ikke gjenta116/8; ikke aktiver
CS17 uten nytt eksplisitt ja og køeiers ferske admission. Ingen CI/push/deploy.
Prosjektimplementeringen venter på grønn testkjede; Butler-kravet beholdes.

## Latest2026-10-14: R1 authorized elsewhere, stopped at cache guard

# CS17-R2: cachekollisjon avklart, ny kjøring venter

Status2026-10-14: baseline116/116 ogCP8/8 er grønne. CS17 har fortsatt null teststarter.
Kjetil sa «Ja, kjør» i Claude-køtråden07:58:26Z (registrert approvalMessage
cmsg_013NgqC72PRtRb8tu7xHs7YT4Jc3BYVJvG59qXWHAmRv9s). Køeieren bandt ja-et
til endeligR1-manifest102f0277…157d5 og startet08:00:04Z. R1 stoppet08:01:31Z,
faseexit75, før Swift fikk cachelåsen. Diskgrensen besto:122,9GiB/13prosent etter reserve.

Rålogg: `HAVEN-Deploy/_handoff/ARBEIDSBENK/G2-W1-CS17-R1-20261014/cs-tests.log`.
Cache28516ddea851 hadde en levende lease:PID14793,start09:46:50lokal,
kommando `haven-swiftpm.sh ... test --jobs 2 --filter CommonsLibrarianCellTests|KallimachosAdvisorCellTests`.
Lesende ps bekreftet prosessen og lsof viste aktive Swift-filer i sammecache.
Tom kø var dermed ikke et ledig byggvindu. Ingen prosesser/låser ble fjernet.

## Konkret ny pakke

`HAVEN-Deploy/_handoff/ARBEIDSBENK/G2-W1-CS17-R2-20261014/`.
Manifest `66a86e662bd3f77617df76ef2bf504bf87fff5f6a5416ea25fa4b4dd92153364`. Samme968-fil CP-kopi med korrekt mappenavnCellProtocol,
sammeCS-kilde og17tester, ingen produkt-/testendring. Gamle pakker bevares.
Ny tidlig lesende cachekontroll stopper før attempt-started når en lease finnes.
Den ordinære runneren beholder atomisk låsing og open-file-kontroll; forhåndskontrollen
er ikke i seg selv eksklusivitet og hindrer ikke en ny konkurrent fra å starte senere.
Køeieren må derfor avstemme også bygg utenfor køen før ferskADMISSION.
Queue-konvolutt har eksplisitt tom cwd-linje før run-argumentet.

Kontrollert i begge locale: check grønn, cache-check avviser aktivlease førforsøk,
run avviser manglendegodkjenning. Ingen Swift, ingenADMISSION/attempt/result iR2.
ForrigeR1 er konsumert; ingen automatisk rerun. Nytt eksplisitt ja gjelder énR2-kjøring
av bare17tester etter frigittcache og køeiers ferske eksklusivevindu. 40GiB OG5prosent
etter10GiBreserve,2jobber, sammeadministrertecache. Ingen CI/push/deploy.
Ved grønt fortsetter alleredeG2-godkjent prosjektflate, inkludert Butler fraalleflater.
Oppfølgingen erPAUSED inntil gyldig videreautorisasjon. Pakkeidentitetsrettelsen er
fortsatt ikke runtime-verifisert fordi cachevakten stoppet før Swift.


## 2026-10-14T13:46:48.557729+00:00 — R2 terminal stopped; oppfølging PAUSED

R2 startet 2026-10-14T13:40:33.694561+00:00 og stoppet 2026-10-14T13:41:24.413950+00:00 (exit1), med null av17 teststarter. SwiftPM avviser versjonslåst DiMyMicropayments med lokal CellProtocol-avhengighet. Ikke cachefeil. Begge pins gjenopprettet byteidentisk; frosne kilder og tidligere116+8 fortsatt verifisert. Se CS17-R2-RESULT-20261014.md og evidence/cs17-r2-reconciled-20261014.json. Engangsforsøket er brukt; ingen rerun/committed testendring. Oppfølging PAUSED bekreftet av automation-verktøyet. Produktimplementering venter på grønt. Ingen CI/push/deploy.
