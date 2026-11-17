# Bolk 3 og 5 — k6: tre vedleggsfunn rettet; broens nøkkelbevis stopper fullporten

STATUS: STOPPET VED CP-GRENSEN. Ingen commit, push, kladd-PR, ny CI, pakke,
merge, deploy eller sending. CellProtocol er fortsatt pinnet til
`36959ae4a114503b08ff85785e0d73f865d4758e`, også i faktisk managed-checkout.
CP-arbeidstreet er uendret. Ingen diskrydding, fil-/cache-sletting,
vaktendring eller leaseoverstyring er utført. Ordinær eksisterende testopprydding
av syntetiske testfiler er beholdt.

K5-rapporten er bevart byte-identisk i `BOLK-3-RAPPORT-k5.md` før denne
rapporten ble skrevet. SHA-256: `9d54165a7ef1f4506932be7cbdefe84f30e7b2d29f9336b04fad1f9819a6dfd4`.

## Rettet og prøvd

| Funn | Endring | Målt resultat |
|---|---|---|
| sourceModesAreObservedAndNeverOfferTransfer | Beholdt prøven; kommentar til godkjent S1. Registrert sourceID og probe krever MCP isError, status error og allowlistet code attachmentUnavailable; samme klienter må deretter sende og hente en riktig kopi. Begge reachability-fixturer beholdt. MCP gir nå maskinlesbar feilkategori uten å vise peer-feiltekst. Verktøybeskrivelsene sier bare kopi i første pakke. | Grønn |
| senderOwnedCellAndSignedAgreementSurviveSnapshotReload | Gjenopprettet celle binder samme betrodde host-root med configureTrustedHostAttachmentStorage før bruk av Resolver. Ingen CP-endring. | Grønn; beholdt byte- og kontraktkontroll |
| legacyAgreementCannotUseAttachmentActions | Faktisk Resolver-resultat er objekt med status error og message attachmentUnavailable, ikke exception. Testen krever begge feltene. MCP-avslag og fravær av transporthandling beholdt. | Grønn |

Den første fokuserte kjøringen prøvde også en feilaktig antakelse om Resolver
status denied; det forsøket er bevart. Faktisk error-status ble klassifisert og
prøven rettet til den typede refusjonen som CP returnerer. Ingen legacy-suksess
ble gjort om til et forventet avslag.

## Brofeilen: observert spor og påvist mekanisme

K5-baselinen passerte samme broprøve, mens k5-fullport/gjenprøve og k6-fullport
feilet. Dette er ikke kalt flaky. K6-fullport viser `Got no signed data` og
at eieren ikke beviser nøkkelkontroll før `.closed`.

Den opprinnelige Vapor-topologien ble beholdt. Alle opprinnelige assertions er
beholdt, inkludert én innmeldt kanal, push uten polling og at vertsvaulten ikke
har deltakerens nøkkel. Prøven er utvidet til gjentakelser og feilbegrenset
buffering av brodiagnostikk og security events; ingen skip, automatisk retry
som skjuler et feiltilfelle, autentiseringsomgåelse eller sleep-retting.

Feilsporet i `k6-buffered-private.log`, linje 73–94:

1. FEED cid2 starter og første nøkkelbevis cid4 får signert svar.
2. SET cid3 starter; nøkkelbevis cid5 og cid6 får signert svar.
3. Nytt nøkkelbevis cid7 kommer inn og signeringshåndteringen starter.
4. Svaret på SET cid3 kommer inn før signert svar på cid7.
5. Nøkkelbeviset feiler og kanalen lukker med `.closed`.

Pinnet CP-kilde forklarer en konkret mekanisme som passer sporet:

- `BridgeIdentityProofAuthorization.permit` tar dictionaryens første aktive
  lease for samme identitet/opprinnelses-scope. Det kan være den kortvarige
  SET-leasen selv om FEED fortsatt lever.
- `BridgeBase.consumeResponse` avslutter SET-leasen når svaret kommer.
- `BridgeBase.validateOriginSigning` krever at akkurat den valgte leasen
  fortsatt finnes, og kaster closed dersom SET-leasen er borte.
- Den kastede feilen kan lukke kanalen gjennom `BridgeChannelTransport`.

Den separate diagnostikken `transientCommandRetiresChosenPermitDespiteActiveFeed`
ble kompilert og kjørt mot den uendrede pinnede dependencyen gjennom testable-API:
valgt SET-permit var gyldig før SET-complete, ugyldig etterpå; et nytt permit
kunne fortsatt velge FEED. Dette viser mekanismen direkte. Første diagnostikk
brukte bare faste cid1/cid2 og fant ikke kortvarig valg; den er bevart som et
mislykket diagnostikkforsøk. R2 varierer kommando-ID-er siden dictionaryrekkefølgen
avhenger av hash, og passerte. Diagnostikkilden ligger bevart under
`Evidence/k6/CorrespondenceBridgeLeaseDiagnosticTests.swift` i klientarbeidstreet;
den er ikke lagt inn som en produktakseptanseprøve som krever at CP-feilen finnes.

**Evidensgrense:** live-sporet eksponerer ikke valgt permit-ID. Koblingen fra
dette konkrete socket-feiltilfellet til lease-mekanismen er derfor en
kildebegrunnet diagnose, ikke en direkte måling av valget i live-kanalen.
Flere diagnostikkjøringer passerte; det beviser ingen retting. En sikker
klientretting innen samme kanal og samme nøkkelbeviskontroller er ikke funnet.
Å rette denne autorisasjonslivssyklusen eller pinne et nytt CP-hode går utenfor
k6-grensen. Arbeidet stopper her; valideringen er ikke svekket for å få grønt.

## Kjøringer og bevis

Alle bevis ligger i `HAVEN-Deploy/_handoff/KORR-UT/bolk3/`.
`k6-verification-summary.json` registrerer sluttilstandens kilde- og bevishasher.
Sluttkompilering/vedleggsgate er kjørt etter siste kildeendring; ingen fullport
er kjørt på nytt etter arkivering av den separate lease-diagnostikken. Den
reproduserte brofeilen er urettet.

| Bevis | Resultat |
|---|---|
| k6-focused-private.log | Kilde- og snapshotprøve grønne; legacy status-antakelse rød; bro passerte én gang |
| k6-full-private.log | Eldre bundles grønne; vedleggssuite grønn; 46 korrespondansetester, én issue i broprøven; exit1 |
| k6-diagnostic-private.log | Instrumentert fullkjede exit0; dette frikjenner ikke den reproduserte brofeilen |
| k6-reproduce-private.log | 20 brotilfeller, første rød med closed, resten grønne |
| k6-capture-full-private.log | Instrumentert fullkjede passerte med 20 brotilfeller; ingen broretting gjort |
| k6-trace-private.log / k6-trace100-private.log / k6-rawtrace-private.log | 20/100/100 brotilfeller passerte med testtransport-instrumentering; denne instrumenteringen er tatt ut av sluttilstanden |
| k6-buffered-private.log | 100 brotilfeller i opprinnelig Vapor-topologi, første rød med closed, 99 grønne; detaljspor over |
| k6-lease-private.log | Første lease-diagnostikk fant ikke kortvarig valg med faste ID-er; exit1 |
| k6-lease-r2-private.log | Isolert lease-mekanisme vist; én diagnostikkprøve grønn |
| k6-final-attachments-private.log | Sluttkompilering grønn; hele vedleggssuiten 11 tester / 0 issues, exit0 |

Direkte kjøring inne i sandbox feilet ved manifestets sandbox-exec. Ingen
sikkerhetsinnstilling ble endret; de ordinære avgrensede Mac-skriptjobbene kjørte
via samme købane som k5. Kapasitetsvakten ble kontrollert uendret før hvert bygg;
GC-adapteren beholdt dry-run og rapporterte bare kandidater over eksisterende cap.

## Ikke levert eller vist

- Grønn fullport etter en faktisk broretting; dermed ingen commit/push/kladd-PR/CI.
- Bolk 5: ingen ren eksport, universal2-pakke, Developer ID-signering,
  notarisering eller staple. Ingen installer eller installer-SHA-256 finnes.
- Native admin fra k3 er fortsatt utenfor produktkode; vindu, ekte LAContext,
  innmelding/fornyelse etter utløp og GUI-akseptanse er ikke vist grønt.
- Samlet formålsprøve mot faktisk PR #286-vert og tre vaults er ikke kjørt her.
- Dagens nøkkellager er ikke isolert mot andre prosesser med samme OS-bruker;
  egen nøkkelgruppe krever fortsatt riktig provisioningprofil.

## Læringsfangst

`L-2026-10-08-pinned-correspondence-bridge-proofs-can-choose-a` er captured/applied
og synced i verktøyets dokumentforstand. `Book/33_Correspondence_First_Class.md`
har den påviste lease-mekanismen og evidensgrensen. Dokumentet er ikke committet
eller pushet. Global strict-check er rød på eldre andres åpne/usynkede poster;
egen post er applied/synced.
