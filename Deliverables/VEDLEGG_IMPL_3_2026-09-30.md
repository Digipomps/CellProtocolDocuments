# Vedlegg i korrespondansen — implementasjon 3

Status: implementert og lokalt testet på egen gren. 24 nye tester bestått; kontrollert baseline-sammenligning har ingen nye feil. Parallell testustabilitet og adapterbegrensninger er eksplisitt rapportert nedenfor. Eierens bestilling 2026-09-30 og BESLUTNINGER_KJETIL_2026-09-28.md er autorisasjon for implementasjon/test/lokal commit. G3, main og deploy er ikke godkjent gjennom dette.

## Mål

Tre situasjonsvalgte moduser; signert binding til melding og avtale; eksplisitt henting; avsendereid lager; retensjon; navngitt og informert overdragelse bare etter henting i copy. Installer-/budsjettleveransene er separate formålsprøver med eieren.

## Arbeidsgrunnlag

- CellProtocol: 81601a6f835252aba7e99d43786fb5d67227c245.
- HavenAgentD: ea558ba1af63caa48cd76253ea1cb588f37aa084 (lokal origin/main, ikke den eldre og endrede hovedarbeidsmappen).
- Egen gren i alle tre repoer: codex/correspondence-attachments-20260930.
- Arbeidsmapper: _worktrees/{cellprotocol,havenagentd,documents}-attachments-impl3.
- Baseline startet før kodeendringer. CLANG_MODULE_CACHE_PATH og SWIFTPM_MODULECACHE_OVERRIDE peker til /private/tmp/haven-attachments-impl3-modulecache. swift test --disable-sandbox, fulle logger i VEDLEGG_IMPL_3_2026-09-30_evidence.

## Baseline — målt før kodeendringer

Første fulle kjøring brukte `swift test --disable-sandbox` i hver isolerte arbeidsmappe.
CellProtocol kjørte totalt 1326 XCTest-metoder: CellBase 1297, HavenCommons 26 og
CellNearby 3. CellBase hadde 9 hoppet over og de tre kjente feilene; de øvrige
bestod. Begge pakkene bygde. CellProtocols kommando ga exit 1.

| Rød baseline-test | Faktisk feil |
| --- | --- |
| `AppleIdentityVaultKeyStorageTests.testLegacyEmbeddedPrivateKeyMigratesToApplicationTagAndSigns` | CDSA-nøkkel: `EPERM`, OSStatus 100001. |
| `AppleIdentityVaultKeyStorageTests.testLegacyEmbeddedPrivateKeyStillSigns` | Samme CDSA-feil. |
| `AppleIdentityVaultKeyStorageTests.testScopedSecretDataStaysStableInUnsignedTestHost` | `unhandledError(status: -25291)`. |
| HavenAgentD: `decodedDefaultAgentCellsInstallBindingsOnceBeforeImmediateStateReads()` | `ownerProofUnavailable`. Denne feilen var **i tillegg** til de tre oppgitte. |

HavenAgentDs første baseline kjørte 326 Swift Testing-tester i sju testbunter,
med én feil og exit 1. Den brukte sin uendrede CP-pin `5609a9a…`.
[CP-logg](VEDLEGG_IMPL_3_2026-09-30_evidence/cellprotocol-baseline.log),
[HavenAgentD-logg](VEDLEGG_IMPL_3_2026-09-30_evidence/havenagentd-baseline.log).

## Verktøyflaten som er implementert

Alle verktøy krever eksplisitt `relationshipID`. Gamle fire-handlingsavtaler får
ikke nye rettigheter. En signert `withAttachments`-avtale må opptas av cellen.
Metadata og henting åpner og verifiserer meldingen gjennom
`CorrespondenceEnvelopeClient`. Byteoverføring bruker eksisterende Bridge og
Resolver, med én `AttachmentStreamV1`-chunk per kall.

| MCP-verktøy | Gjør | Autoriserer ikke |
| --- | --- | --- |
| `correspondence_list_inbox` | Lister konvolutter | Lese innhold, hente vedlegg, kvittere, sende eller kjøre noe. |
| `correspondence_read_message` | Leser/dekrypterer meldingen, viser signert vedleggsmetadata | Hente bytes, filkvittering, varig eksport eller overdragelse. |
| `correspondence_send_message` | Sender kryptert tekst | Vedlegg, kjøring eller maskinhandlinger. |
| `correspondence_ack_message` | Meldingskvittering | Filkvittering eller overdragelse. |
| `correspondence_send_attachment` | Sender melding med én `filePath` eller registrert `sourceID` | Fritt modusvalg, sletting av original, overdragelse, åpning/installasjon/kjøring. |
| `correspondence_attachment_metadata` | Navn/type/størrelse, modus/begrunnelse og tillatt neste steg | Bytehenting, filkvittering, eksport eller kjøring. Ingen innholdshash/nøkkel vises. |
| `correspondence_probe_attachment_source` | Mottaker prøver tilgang til eksplisitt delt referanse uten å lese innhold | Hente bytes, sende, opprette nye grants eller overdragelse. |
| `correspondence_fetch_attachment` | Verifisert, administrert nedlasting; i referansemodus returneres eksisterende fil med null kopierte bytes | Nytt varig eierskap, permanent eksport eller kjøring. |
| `correspondence_revoke_attachment` | Avsender tilbakekaller sin administrerte leveranse | Slette ekstern original eller overdratt mottakerfil. |
| `correspondence_transfer_attachment` | Avsender tilbyr navngitt overdragelse etter henting i `copy` | Aksept på mottakerens vegne eller skjult samtykke uten eierpolicy. |
| `correspondence_accept_attachment_transfer` | Mottaker aksepterer og eksporterer sin verifiserte fil | Overskrive eksisterende fil, installere eller kjøre. |

Ingen meldingstekst eller vedlegg gir utførelsesmyndighet. Ukjente argumenter,
inkludert et forsøk på å sende inn `mode`, avvises.

## Modusvalgets regel og lagringsansvar

1. **reference:** registrert kilde som avsender lagrer, eksplisitt delt referanse,
   og vellykket mottakerprobe siste fem minutter. Referansen må også nå samme
   registrerte fil hos avsender. Ingen strøm eller ny filkopi opprettes.
2. **fetchOnDemand:** registrert fil i avsenders celle, men ingen bekreftet felles
   referanse. Forsegling og henting starter først ved mottakerens hentehandling.
   Ukjent/utløpt nåbarhetsbelegg rapporteres som det, ikke som målt nettfeil.
3. **copy:** valgt lokal fil er utenfor cellens registrerte kilder, eller kildens
   lokalt fastsatte lagringspolicy ikke bærer fortsatt lagring. Avsender får ikke
   velge modus som et flagg.

Første referanseadapter gjelder fil-/delte filbaner. Andre navnerom, for eksempel
vilkårlige eksterne Cell-/skyreferanser, er ikke levert. En delt filbane må bety
samme kilde hos begge parter. Dette er en konkret begrensning i adapteren.

Lageret er en egen `CorrespondenceAttachmentCell` per avsender, med avsenderens
signeringsidentitet som eier og separat diskmappe. Cellene er fysisk vertet av
korrespondanseruntime i denne versjonen; dette betyr **ikke** at alle bytes
ligger på avsenders laptop. Alle ytre handlinger går gjennom relasjonscellens
avtalekontroll. Kopinøkkelen ligger i klienten og den krypterte meldingen, ikke i
serverens indeks. Filnavn/type/størrelse leveres før henting uten innholdshash.

Meldings-ID finnes før forsegling. Både indre signatur og konvoluttens autentiserte
kontekst binder melding og opprinnelig avtale. Gjenbruk av levende meldings-ID avvises.
Mottakerens nåværende rettighet kontrolleres i tillegg; en egen mottakerkontrakt
endrer ikke vedleggets opprinnelige avtale-ID.

## Overdragelsen og kostnaden for eieren

Bare `copy` viser overdragelse som tilgjengelig. Den krever fullført og
verifisert mottakerhenting; vanlig meldingskvittering teller ikke. Eier må svare
på den synlige konsekvensen, eller ha satt en uttrykkelig lokal policy:

> I understand: the recipient owns this file; I cannot revoke it and it will not expire with the message.

Avsender tilbyr overdragelsen; mottakeren aksepterer deretter og velger sin
varige filbane. En varig overdragelsespost lagres **før** avsenders administrerte
kopi slettes. Ekstern original slettes ikke. Policyfeltet
`attachmentTransferPolicy` kan svare på det navngitte steget, men gir ikke
automatisk overdragelse ved sending, lesing eller henting.

Ved bortkommet akseptsvar kontrollerer klienten serverens varige status. Uavklart
utfall beholdes i karantene med en uttrykkelig ventende intensjon og feilsvar,
ikke som «overdratt». En slik uavklart intensjon kan beholdes utover TTL for å
unngå tap av en mulig overdratt fil; eksplisitt retry må avklare den. Dette
unntaket er synlig, og generell automatisk avstemming er ikke implementert.

## Full disk, avbrudd og retensjon

Ingen total filstørrelsesgrense er innført; chunks er 64 KiB. Testene sender
flere chunks, opptil 180037 bytes; svært store reelle filer er ikke målt her.

- Full disk under innlesing hos avsender: skrivefeil returneres, innførselen
  tilbakekalles og chunk-mappen fjernes. Uferdig kopi kan ikke publiseres.
- Full disk hos mottaker: feilsvar, midlertidig `.partial` slettes, ingen ferdig
  filbane publiseres. Eksport etter overdragelse bruker også midlertidig navn og
  atomisk navnebytte, uten overskriving.
- Feil ved lagring av overdragelsesstatus: tilstanden rulles tilbake i minnet;
  det rapporteres ikke overdragelse, og avsenders kopi beholdes.
- Oppryddingsfeil returneres særskilt. Testene injiserer reell `ENOSPC`-feilkode
  i skrivegrensen; maskinens disk ble ikke fysisk fylt opp.
- Mistet forbindelse etter første chunk: feilsvar, ingen hel-looking halvfil;
  ny eksplisitt henting kan fullføres. Autentisert slutt og signert størrelse
  må stemme før publisering.
- Ved publisering får lageret meldingens faktiske utløp fra `retentionSeconds`.
  Alle kall kontrollerer utløp. Timere rydder mens prosessen kjører; oppstart
  rydder forfalt innhold. Sovende/stoppet vert kan ikke fysisk rydde før den
  kjører igjen. Upubliserte innførsler har én times levetid.
- Referansen gir tilgang til en fil mottakeren allerede kunne nå. Utløp fjerner
  meldingskoblingen, ikke denne eksisterende filen. Administrerte hentedata dør
  med meldingen; uttrykkelig overdratte filer gjør det ikke.
- Tilbakekall stanser senere henting. Allerede lest klartekst, mottakerens egne
  kopier og sikkerhetskopier kan ikke kryptografisk trekkes tilbake/slettes.

Uferdig kildebasert strøm kan ikke fortsette etter prosessomstart: dens
engangsforsegler gjenopprettes ikke med samme nøkkel/nonce. Den feiler lukket og
krever en ny leveranse. Ferdige strømmer/kopier og overdragelsesposter overlever
lagring/gjeninnlasting. Dette er testet lokalt, ikke sertifisert mot strømbrudd.

## Regresjon og kjøringsmåte

En full kandidatkjøring med standardparallelisering bestod (`havenagentd-final2`,
334 tester; før den siste snapshot-testen ble lagt til). Neste kjøring, med
335 tester, fikk nye tidsavbrudd i tre **uendrede** jobbkjørertester:

- `appServerFailureBecomesDurableFailedCompletion()`
- `daemonRunsQueuedAppServerJobAndWritesDurableCompletion(kind:)`
- `failedStartPersistenceNeverLaunchesOrReplaysTheJob(kind:)`

Alle traff `waitUntil(timeout: 2)` i `JobCompletionServiceTests.swift:745`.
Følgeassertene leste derfor uferdig jobbstatus. Dette er observert tidsfølsomhet;
rotårsaken til den enkelte forsinkelsen er ikke bevist. Ingen tidsfrist eller
produksjonskode i jobbkjøreren ble endret for å få grønt.
[Hele feilloggen](VEDLEGG_IMPL_3_2026-09-30_evidence/havenagentd-final3.log)
er beholdt. Dette omtales ikke som en usvikelig grønn parallell suite.

Derfor ble en **ny ren baseline** sjekket ut ved samme `ea558ba…` og kjørt med
`swift test --disable-sandbox --no-parallel`, uten samtidige bygg fra denne
jobben. Deretter ble kandidaten kjørt med samme eksplisitte modus. Den rene
baselinen bestod alle 326 tester, inkludert den opprinnelige `ownerProofUnavailable`-
feilen. Dispensasjon for en ny rød test ble ikke antatt.

Swift Testings parallelle standard er forskjellig fra XTests standard, selv om
CLI-hjelpen kan angi `--no-parallel` som standard. Den eksplisitte bryteren er
beskrevet i [Swift Testings egen dokumenterte kode](https://github.com/swiftlang/swift-testing/blob/main/Sources/Testing/Traits/ParallelizationTrait.swift),
og den misvisende hjelpeteksten er registrert i
[SwiftPMs problemrapport](https://github.com/swiftlang/swift-package-manager/issues/8174).
Rapportens akseptgrunnlag skiller derfor mellom standardkjøringen og den
kontrollerte serielle sammenligningen.

Explore-kildeaudit: baseline og kandidat har begge 7 eksisterende feil og 20
advarsler; ingen nye funn. Nye vedleggshandlinger har registrerte Explore-kontrakter,
kontrollert også gjennom runtime i snapshot-testen.
[Baseline](VEDLEGG_IMPL_3_2026-09-30_evidence/explore-baseline.json),
[kandidat](VEDLEGG_IMPL_3_2026-09-30_evidence/explore-final.json).

## Dokumentasjon og videre formålsprøve

Løpende implementasjonsdokumentasjon:
[CellProtocol-kontrakten](VEDLEGG_IMPL_3_2026-09-30_evidence/CellProtocol-CorrespondenceAttachments.md)
og [MCP-verktøy og myndighetsgrenser](VEDLEGG_IMPL_3_2026-09-30_evidence/HavenAgentD-CorrespondenceAttachments.md).
Bokstoffet hører hjemme i kapittel 04 (avtaler), 05 (livsløp/retensjon),
08 (chunket transport) og 21 (kontakt/korrespondanse). Boka er ikke endret.

Målene om **installerpakken til Vegar/LilleRobot** og **bruk av riktig budsjett**
er ikke bevist av syntetiske byte-/MCP-tester. Ingen operative profiler,
virkelige meldinger, installasjoner eller mottakerhandlinger er brukt her.
Eieren avgjør G3/formålsaksept. Pakkejobben må publisere de parede revisjonene,
bygge/utrulle dem og provisionere de nye signerte avtalene og lagringen før
operative mottakertester.

Gjenstående begrensninger: andre referanseadaptere enn fil/delt filbane,
automatisk avstemming av uavklarte overdragelser, gjenopptak av uferdige
kildestrømmer etter omstart, reell svært stor filbelastning, fysisk ENOSPC,
strømbrudd, Linux/iOS og en funksjonsprøve mellom to virkelige maskiner.
Standardparallelle jobbkjørertester har den dokumenterte tidsfølsomheten;
den er ikke reparert som del av vedleggsjobben.

## Læringsfangst

`L-2026-09-30-ved-baselinebasert-aksept-skal-full-uendret` er fanget og anvendt i
`CellScaffold/.claude/skills/cellprotocol-contract-testing/SKILL.md`.
Tidligere endringer i filen er beholdt. Synkronisering ble forsøkt, men
skriving til `~/.claude/skills` ble avvist med `Operation not permitted`.
Læringen er **anvendt, ikke distribuert**, og er ikke markert som synket.
[Synklogg](VEDLEGG_IMPL_3_2026-09-30_evidence/learning-sync.log).


## Mål og påstander — holdt adskilt

| Mål | Målt påstand / belegg | Grense |
| --- | --- | --- |
| F1: levere en navngitt fil i korrespondansen | Tre situasjoner har hver sin valgte modus; faktisk MCP/Resolver-rundtur og bytekontroll består. | Fil/delt filbane som referanseadapter; lokalt testmiljø. |
| F4/F7: kilde, melding og avtale hører sammen | Signert innermanifest og AAD; bytte av melding/avtale avvises; vedleggscellens avsendereier bevares ved gjeninnlasting. | Ingen ekstern kryptografisk revisjon. |
| F5: kontrollert lagring og utløp | TTL, diskfeil, avbrudd, sen sluttchunk, omstart og overdragelsesfeil er prøvd. | Fysisk sletting på stoppet vert og backup/egne kopier kan ikke garanteres. |
| F6: informert valg | Metadata uten bytes/hash; eget overdragelsessteg, klar konsekvens, eksplisitt policy og separat mottakeraksept er prøvd. | Ingen GUI-flate eller brukertest med eier er påstått. |
| F2/F3: installer/budsjett faktisk brukt | **Ikke prøvd.** | Eierstyrt formålsprøve og pakkejobb gjenstår. |

Det er altså grunnlag for å hevde lokal funksjon i den beskrevne adapteren,
ikke at produksjonsleveransene er gjennomført eller at eieren har akseptert G3.


## Sluttresultat — baseline før og etter

| Pakke/kjøring | Før | Etter | Nye feil i sammenligningen |
| --- | --- | --- | --- |
| CellProtocol, full standardkjøring | 1326 tester totalt; 3 feil, 9 hoppet over; exit 1 | 1340 totalt; samme 3 feil, samme 9 hoppet over; exit 1 | 0. CellBase alene: 1297 → 1311. |
| HavenAgentD, eksplisitt seriell fullkjøring | 326 tester, 0 feil; exit 0 | 336 tester, 0 feil; exit 0 | 0. Alle sju testbunter fullførte. |

Alle **24 nye tester** bestod (14 CellProtocol + 10 HavenAgentD). Den ekstra
HavenAgentD-feilen i første baseline og de tre tidsfølsomme metodene i én
parallell kandidatkjøring er beskrevet ovenfor; de er ikke fjernet fra beleggene.
[Maskinell sammenligning](VEDLEGG_IMPL_3_2026-09-30_evidence/comparison.json).

Sluttkommandoer, begge med de skrivbare modulcachevariablene fra arbeidsgrunnlaget:

```sh
# CellProtocol, fra egen arbeidsmappe
swift test --disable-sandbox
# HavenAgentD, fra egen arbeidsmappe, med den parede CellProtocol-kilden
export HAVEN_ATTACHMENT_CELLPROTOCOL_PATH=../cellprotocol-attachments-impl3
swift test --disable-sandbox --no-parallel
```

Den ekstra rene HavenAgentD-baselinen lå i
`_worktrees/havenagentd-attachments-baseline3`, uendret ved `ea558ba…` og med
original CP-pin. Den brukte `--scratch-path ../havenagentd-attachments-impl3/.build`
for å gjenbruke byggelageret sekvensielt. Ingen av de to prosessene brukte det
lageret samtidig.

[CP sluttlogg](VEDLEGG_IMPL_3_2026-09-30_evidence/cellprotocol-final-verified.log),
[seriell baseline](VEDLEGG_IMPL_3_2026-09-30_evidence/havenagentd-baseline-serial.log),
[seriell kandidat](VEDLEGG_IMPL_3_2026-09-30_evidence/havenagentd-final-serial.log).

## Hver ny test med resultat

CellProtocol (`CorrespondenceAttachmentTests`):

| Test | Resultat |
| --- | --- |
| `testCopySelectionAndRecipientByteExactRoundTrip` | Bestått |
| `testExpiredAttachmentIsUnavailableAndStoredBytesArePurged` | Bestått |
| `testFailedTransferStateWriteDoesNotClaimOwnershipOrDeleteSenderCopy` | Bestått |
| `testFullDestinationDiskReturnsErrorAndRemovesPartialFile` | Bestått |
| `testFullSenderDiskRevokesAndRemovesPartialImport` | Bestått |
| `testInterruptedOrTamperedStreamNeverPublishesHalfFile` | Bestått |
| `testMetadataHasNoHashKeyOrChunksAndDoesNotFetch` | Bestått |
| `testMissingFinalChunkCannotPublishAndRestartKeepsCompleteCopy` | Bestått |
| `testNonRetainingSourcePolicySelectsCopy` | Bestått |
| `testReceiverRejectsExtraChunkAndWrongSignedSize` | Bestått |
| `testReferenceAndFetchOnDemandAreChosenByObservedReachabilityWithoutSendTimeBytes` | Bestått |
| `testTransferRequiresDownloadAndExplicitOwnerConsequenceThenSurvivesExpiry` | Bestått |
| `testUnfinishedSourceStreamAfterRestartFailsClosedAndStaleProbeDoesNotSelectReference` | Bestått |
| `testWrongMessageAndAgreementCannotFetchStream` | Bestått |

HavenAgentD, faktisk MCP-service → transportadapter → isolert Resolver →
CorrespondenceCell (ingen mock av avtaleavgjørelsen):

| Test | Resultat |
| --- | --- |
| `copyThroughMCPMetadataFetchTransferAndRetainedExport()` | Bestått |
| `sourceModesAreObservedAndNeverOfferTransfer()` | Bestått |
| `legacyAgreementCannotUseAttachmentActions()` | Bestått |
| `signedEnvelopeRejectsMessageAndAgreementSubstitution()` | Bestått |
| `expiryUsesActualMessageTTLAndDeletesManagedDownload()` | Bestått |
| `interruptedTransportReportsErrorWithoutFinalOrPartialFileThenCanRetry()` | Bestått |
| `ownerConfiguredPolicySuppliesOnlyTheNamedTransferAnswer()` | Bestått |
| `managedCacheStartupCleansOrphanAndRejectsConcurrentWriter()` | Bestått |
| `senderOwnedCellAndSignedAgreementSurviveSnapshotReload()` | Bestått |
| `finalChunkArrivingAfterExpiryCannotPublishOrphanFile()` | Bestått |

Avsenderdisk, mottakerdisk og diskfeil ved overdragelsescommit testes med injisert
ENOSPC; avbrudd og sent sluttchunk testes gjennom transportgrensen. Gamle
strøm-/konvoluttester inngår i fullkjøringene. Nye rettigheter er også negativt
testet med gammel avtale direkte gjennom Resolver.

## Grener og commits

Alle tre oppdragsgrenene heter `codex/correspondence-attachments-20260930`.

| Repository | Commit / leveranse |
| --- | --- |
| CellProtocol | `9420e7dbd6790be8608dc9045a9c793c841b9195` |
| HavenAgentD | `a6bd16394781de2ebe20ec6f68d4a6eea22dae2d` |
| CellProtocolDocuments | Denne rapporten og hele beleggsmappen committes på samme oppdragsgren, med commitmelding `Record third correspondence attachment implementation and baseline evidence`. |

HavenAgentDs manifest og låsefil peker på den parede CP-commiten. Den er bare
lokal: remote-avhengigheten kan først hentes når pakkejobben har publisert
revisjonen. Den eksplisitte lokale pakkeoverstyringen ovenfor er bygget/testet.
Låsefilens manifestfingeravtrykk oppdateres av SwiftPM når den publiserte
remote-pakken løses. Ingen kildeendring trengs for det.

Ingen push, main-merge eller deploy er gjort. Eksisterende endringer i vanlige
arbeidsmapper er bevart. Læringsendringen ligger lokalt i den allerede endrede
kanoniske ferdighetsfilen og læringsloggen; den ble ikke blandet inn i noen
kodecommit. Rapport/belegg finnes både på den bestilte vanlige stien og i
`_worktrees/documents-attachments-impl3` sin dokumentgren.
