# k15 — vedlegg og produksjonens signeringskvote

Sluttrapport, 2026-10-13. Vertsloggvinduet og tidsstempler med `Z` er UTC.
Rå XCTest-utskrifter kan bruke maskinens lokale tid uten soneangivelse.
Ingen merge, tag, deploy, installerbygg eller vertsendring er utført.

## Påvist årsak og bevisgrense

En lokal reproduksjon med k13-r2-klienten viser at produksjonens signeringskvote
avviser et identitetsbevis inne i vedleggsautorisasjonen. Dette blir
`attachmentUnavailable`; neste oppryddingskall avvises i den ytre autorisasjonen
og blir `SetValueError`. Begge meldingene er reprodusert i samme kjøring.
Dette er en kode-/samspillsfeil, ikke en påvist manglende vertsinnstilling.

På staging-revisjonene CellScaffold `9ff06f84` og CellProtocol `b4100f57`:

| Kontroll | Kilde, relativt til repoet |
| --- | --- |
| Produksjon aktiverer `localProtection`; `.testing` bruker `monitorOnly` | CellScaffold `Sources/App/configure.swift:1174`; også `Sources/ScaffoldKit/AdminScaffoldRuntime.swift:859` |
| Standard er 12 signeringsforsøk per 60 sekunder | CellProtocol `Sources/CellBase/Security/CellSecurityContainment.swift:19` |
| Også utgående forespørsler om identitetsbevis treffer kvoten | CellProtocol `Sources/CellBase/Cells/Bridging/BridgeBase.swift:1140`, `:1269` |
| Feilet signering gjør at eier-/medlemsbeviset ikke kan verifiseres | CellProtocol `Sources/CellBase/Cells/GeneralCell/GeneralCell.swift:2477` |
| Den reproduserte upload-avvisningen skjer ved `decision.allowed` | CellProtocol `Sources/CellBase/Cells/Correspondence/CorrespondenceCell.swift:1225` |
| Handleren skjuler årsaken som `attachmentUnavailable` | samme fil, `:1255` |
| Ytre SET-feil blir `.error`, som klienten kaster som `SetValueError` | CellProtocol `Sources/CellBase/Cells/Bridging/BridgeBase.swift:1453`, `:910` |

Den lokale prøven med faktisk PR32-klient, Lightweight-transport og
`monitorOnly` var grønn. Med `localProtection` aktiv ble den samme feilkjeden
reprodusert på 0,201 sekunder. Sanitert lokalt diagnostikkutdrag:

```text
K15 security reason=signing_rate_limited
K15 security reason=owner_proof_failed
K15 attachment rejection action=attachments.upload type=CellBase.CorrespondenceAttachmentError
cleanup: CellBase.SetValueError error 4
```

Dette peker på autorisasjonen før `CorrespondenceAttachmentStorage.store`, ikke
på chunkstørrelse, bytegrense eller diskreserve i den reproduserte kjøringen.
Tekst-, historikk- og prepare-kall bruker allerede bevisbudsjett på forbindelsen.
Det forklarer hvorfor en opplasting kan nå grensen ved ulike chunkindekser.
Det nøyaktige historiske signeringsantallet for A og B er ikke tilgjengelig.

Vertsloggen ble lest via `HAVEN-Deploy/lib/vert.sh`, uten vertsmutasjon eller
lesing av relasjonsinnhold. Første avgrensede lesing fant 2867 logglinjer for
18:06–18:25:59Z, men ingen av de undersøkte faste feildiagnostikkene. En senere
lesing fant ingen beholdte linjer for samme vindu; containerens starttid var
uendret og restarttelleren null. Årsaken til bortfallet er ikke fastslått.
Loggen alene beviser derfor ikke hvilken kontroll de historiske enkeltkallene
traff. Den lokale reproduksjonen er det direkte kontrollbeviset.

Lesende konfigurasjonsprøver viste konfigurert lagringsrot på skrivbar mount,
tilgjengelige inoder og tilstrekkelig reserve ved målingen. De publiserer bare
predikater, ingen innstillingsverdier. Egen mount, faktisk reserve,
WebAuthn-origin-fallback og klientens bevisadapter var også grønne lokalt under
testpolicyen. Disse forskjellene forklarte ikke avvisningen.

## Kandidatretting

CellProtocol beholder signeringskvoten, vedleggsautorisasjonen, lagringskvotene og diskreserven. En uttrykkelig
signeringsbegrensning før operasjonens effekt får et avgrenset ventetidssignal.
Diagnostikken tilhører den enkelte forespørselens proxy. Den første eksplisitte autorisasjonsgrensen i den endelige CorrespondenceCell-klassen
binder signalet til nøyaktig mottakerobjekt og keypath; BridgeBase kontrollerer
at dette er toppnivåoperasjonen. Et barns avslag kan ikke godkjenne gjentakelse
av forelderen. De gjennomgåtte indre vedleggsgrensene kaster samme bundne avslag før lagring.
Bare BridgeBase lager wire-signalet etter bindingstesten; SET-returverdier
blir ikke tolket som gjenforsøkssignaler.
En sen autorisasjonsfeil, lagringsfeil eller ukjent utfall gjør det ikke.
Dette er avgrenset til disse korrespondansebanene, ikke en generell garanti for
alle Meddle-implementasjoner. Eldre svar uten tilleggsfelt kan fortsatt dekodes, og
eldre klienter behandler avslagene som feil.

HavenAgentD venter og prøver bare slike uttrykkelige avslag på nytt, med høyst
tre gjenforsøk og høyst 120 sekunders ventetid per avslag. Opaque
`attachmentUnavailable`, generisk `SetValueError`, timeout og lagringsfeil blir
ikke automatisk gjentatt. Avbrudd stopper gjenforsøk. Shutdown hindrer neste innsending, men vekker ikke
en allerede pågående kvoteventing; kallet kan vente ut resten av perioden
(opptil 120 sekunder) før det feiler.

Den første lange prøven avdekket dessuten kanalens ordinære femminuttersutløp.
Grensen er beholdt. Klienten reautentiserer før en ny operasjon når den gamle
kanalen er utløpt. Den native signeringskvoten følger nå verifisert identitet,
endepunkt og logisk publisher/consumer på tvers av forbindelser. Et kanalbytte
nullstiller dermed ikke kvoten. Dette er kontrollert separat i protokolltesten og i første lange nettverkstest.
Den overførte 1 100 037 byte begge veier, sammenlignet mottatte bytes,
tilbakekalte vedlegg og kontrollerte avvisning etter tilbakekalling. Den tok
1327,803 sekunder (22 minutter og 8 sekunder). Stor overføring er altså treg med
dagens kvote; rettingen endrer ikke dette budsjettet. Endelig klientfulltest med publisert protokollpinne er også grønn etter de siste
innstrammingene fra gjennomgangen: nettverksprøven tok 1330,598 sekunder
(22 minutter og 11 sekunder).

Klientgrenen er opprettet fra `main` og inkluderer de fem nødvendige commitene
fra fortsatt åpne [HavenAgentD PR32](https://github.com/Digipomps/HavenAgentD/pull/32).
CellProtocol er publisert som [kladd-PR #67](https://github.com/Digipomps/CellProtocol/pull/67),
commit `fee5cbacd254be97d5775b819b4f2f907373724e`. Klientcommit
`538e8187d9476fdf50806b0cfefe54a65fd64895` bruker denne offentlige Git-pinnen;
låsefilen er regenerert, og ingen andre avhengighetspinner er endret.
Klienten er publisert som [kladd-PR #36](https://github.com/Digipomps/HavenAgentD/pull/36)
etter full lokal port. CellProtocol CI er grønn; klientens CI stoppet før bygg på kravet om avhengighetspinner på `main`. Kladdene skal ikke merges eller deployes som del av dette oppdraget.

Kildeankere for rettingen (repo-relative, ved commitene oppgitt over):

| Del | Fil:linje |
| --- | --- |
| Bundet avslag fra korrespondansens første autorisasjonsgrense | CellProtocol `Sources/CellBase/Cells/Correspondence/CorrespondenceCell.swift:432` |
| Bundet avslag før publisering og vedleggslagring | samme fil `:777`, `:1269` |
| Mottaker-/keypath-binding og kontroll før wire-svar | CellProtocol `Sources/CellBase/Cells/Bridging/BridgeSigningBackpressure.swift:56`; `BridgeBase.swift:1473`, `:1524` i samme katalog |
| Kvotebudsjett over native kanalfornyelse | CellProtocol `Sources/CellBase/Cells/Bridging/BridgeBase.swift:1274` |
| Klientens avgrensede venting/gjenforsøk | HavenAgentD `Sources/HavenCorrespondenceMCP/CorrespondenceSigningRetry.swift:12` |
| Kanalutløp og kontroll av gjeldende cache-generasjon | HavenAgentD `Sources/HavenCorrespondenceMCP/CorrespondenceCellTransport.swift:113`, `:191` |

## Teststatus

| Prøve | Resultat |
| --- | --- |
| Staging-lik lokal lagrings-/origin-/transportprøve | Grønn, to tester |
| Faktisk PR32-klient med testpolicy | Grønn, én test |
| Samme klient med produksjonspolicy på staging-koden | Rød; upload og cleanup-feil reprodusert |
| Endelige fire protokollregresjoner på staging-koden | Rød, fem forventede assertionsfeil; identiske testmetoder verifisert med hash |
| Effekt → sent autorisasjonsavslag før retting | Rød, én test/én assertionsfeil |
| Foreldreeffekt → indre upload-avslag fra barn før retting | Rød, én test/én assertionsfeil |
| Siste berørte protokollport | Grønn, 409 tester, én utelatt, null feil |
| Full lokal protokollport på publisert `fee5cbacd` | Grønn, 1697 tester, fem utelatt, null feil; rent tre før/etter |
| Første lange klientprøve med ordinær kvote/kanalutløp | Grønn, fem tester; nettverkstesten tok 1327,803 sekunder |
| Endelig klientfulltest på offentlig protokollpinne | Grønn, 369 tester i alle sju testtargets; nettverksprøven 1330,598 sekunder; rent tre før/etter |
| Daemon-smoke og pakkekontroll | Grønn; fire CI-fasetester, fire testkjørertester og ressurskontroller inkludert negative prøver |
| CP kladd-PR/CI | #67; alle kontroller grønne. macOS: 1697 tester/fem utelatt/null feil, samt Thread Sanitizer-port. Linux-port: 174 tester/null feil, inkludert alle åtte nye regresjoner. Linux identitetslager og runtime-matrise grønne |
| Klient kladd-PR/CI | #36; rød før bygg: CP-pinnen finnes på kladd-PR #67, men ikke på `main`. Lokal fulltest er grønn |

Ikke summer fokuserte og fulle kjøringer; de dekker overlappende tester.
Protokollfulltesten består av CellBase 1668 tester (fem utelatt), HavenCommons
26 og CellNearby tre. Første klientnettverkstest er tidligere enn siste
mottakerbinding og er derfor oppført separat fra den endelige fulltesten.
Klientens sju fulltestrunder rapporterte 5 + 51 + 190 + 60 + 25 + 31 + 7 = 369
tester. Ingen fokuserte tester er lagt til dette antallet.

Saniterte bevis i `HAVEN-Deploy/_handoff/KORR-UT/k15/`:
`diagnosis-evidence.json`, `red-green-test-identity.json`, `cp-final-red-result.json`,
`cp-full-final-result.json`, `cp-linux-ci-result.json`, `cp-macos-ci-result.json`,
`client-full-final-result.json`, `client-smoke-final-result.json` og `client-ci-result.json`.
Fulltestbevisene peker på skriptenes revisjons-/rent-tre-kontroller og køens
`EXIT=0`-kvitteringer; rødbeviset inneholder terminaloppsummeringen.
Linux-resultatet viser de åtte nye testenes faktiske terminalresultater.
Lesende vertspredikater: `HAVEN-Deploy/_handoff/KORR-UT/k15/staging-read-only.json`
og `staging-log-generation.json` i samme bevismappe. Alle klientidentiteter og
filinnhold i nye prøver er syntetiske.

## CI-lenker

CellProtocol, head `fee5cbacd254be97d5775b819b4f2f907373724e`:

- [macOS og Thread Sanitizer](https://github.com/Digipomps/CellProtocol/actions/runs/38314991550) — grønn.
- [Linux, inkludert de nye signeringsregresjonene](https://github.com/Digipomps/CellProtocol/actions/runs/38314991546) — grønn.
- [Linux identitetslager](https://github.com/Digipomps/CellProtocol/actions/runs/38314991578) — grønn.
- [Avgrenset runtime-matrise](https://github.com/Digipomps/CellProtocol/actions/runs/38314991548) — grønn.

Klient, head `538e8187d9476fdf50806b0cfefe54a65fd64895`: [CI](https://github.com/Digipomps/HavenAgentD/actions/runs/38317573852) — rød før bygg.
Steget `Assert every pinned dependency is on its own main` avviste CP-pinnen:

```text
FEIL  cellprotocol: fee5cbacd254 ligger IKKE på main i https://github.com/Digipomps/CellProtocol.git.
Process completed with exit code 1.
```

Kontrollen finnes i HavenAgentD `.github/workflows/ci.yml:200` og
`Scripts/assert_dependencies_are_on_their_main.sh:47`. Kandidaten er publisert
og lokalt testet via offentlig Git-pinne, men ligger fortsatt på kladd-PR #67.
Kontrollen er beholdt. Ingen omkjøring kan gjøre denne pinnen til del av `main`
uten en senere, særskilt autorisert landing. Klientens bygg og tester ble ikke
startet i CI; den grønne lokale fulltesten erstatter ikke dette CI-resultatet.

## Ikke vist

- Grønn klient-CI: avhengighetskontrollen stopper kjøringen før bygg.

- Ingen ny funksjonell prøve eller retting på staging; verten er ikke endret.
- Historisk, entydig feildiagnostikk for hvert A/B-kall fra k13-r2 mangler.
- Full Linux-app-test: Docker avviste opprettelse før teststart. Den avgrensede
  Linux/macOS-codecprøven var grønn for 8192 syntetiske utfordringer. CPs Linux-CI
  er også grønn, inkludert nye regresjoner; dette er komponenttester, ikke en
  Linux-akseptanse av hele CellScaffold-tjenesten.
- Gjenoppretting av aktive Flow-abonnementer over kanalutløp er ikke målet for
  den nye vedleggstesten. Eksisterende Flow-tester må rapporteres separat.
- Faktisk `Task.cancel()`/shutdown mens kvoteventing pågår er ikke særskilt
  testet. Den raske avbruddstesten injiserer `CancellationError` fra ventefunksjonen.
- Ingen merge, tag, deploy eller nye installerere i dette oppdraget.

STATUS: LEVERT
