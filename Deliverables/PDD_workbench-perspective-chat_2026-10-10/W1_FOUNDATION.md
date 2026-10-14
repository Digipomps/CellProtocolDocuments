# W1 — internt journalgrunnlag, 2026-10-12

Status: uferdig, ukompilert og uten runtime-kobling. G2 er godkjent; W1 og G3 er ikke fullført.
Kildebase: CellScaffold 9ff06f8446b6331da49272f5fd72b947b4092ece, gren codex/workbench-perspective-chat-20261012. Filhashene ligger i evidence/w1-preflight-20261012.json.

## Det som er skrevet

To interne Swift-typer er lagt til: WorkbenchSessionJournal og WorkbenchSessionCommitBoundary.
Journalen har sesjonsrevisjon, stabil kommando-/hendelsesidentitet, payload-hash,
sekvenskontroll, begrenset historikklesing og ren rekonstruksjon uten eksterne callbacks.
Commit-grensen serialiserer callback-forsøk, holder ubekreftet kandidat utenfor synlig
tilstand, krever identisk tilbakelevert journal, og lar usikre forsøk avstemmes uten nytt skriv.
Tretten nye XCTest-metoder er skrevet. Ingen av dem er kjørt.

Disse typene er interne byggesteiner, ikke publisert wire-kontrakt eller sikkerhetsbevis.
Kommandoformatet er foreløpig smalere enn contract/workbench-v1.json; innpakking av
input, aggregateID/type/payloadRef, full receipt og immutable turn/effektforsøk gjenstår.
Ingen nye Meddle-/Explore-/GUI-innganger er aktivert. WorkbenchHelperCell er identisk
med kildebasen. Ingen eksisterende test er endret. De tre filene er fortsatt ucommittet.

## Hvorfor den første snapshot-koblingen ble tatt ut

Uavhengig kildelesing av det første utkastet avdekket to P2-funn:
1. Arvet GeneralCell.flow godtar også en gyldig delegert feed-grant. Eierkrav på snapshot
   beskytter ikke private sessionID/cursor/revision/operation som sendes på en slik feed.
2. Hvis vanlig Cell.encode inneholder pending journal, kan resolverens senere autosave
   eller eviction skrive kandidaten uten ny autorisasjon/retention-kontroll. Bare å encode
   committed er heller ikke tilstrekkelig: et eldre snapshot kan overskrive et nyere skriv.

Den foreløpige runtime-koblingen og de seks tilhørende, ukjørte integrasjonstestutkastene
er fjernet. Core-grensen gir kandidat kun til den eksplisitte store-callbacken. Den er
ikke lagt i noen Cell Codable-/autosave-flyt. Dermed har denne endringen ingen
produksjonssti som kan utløse de to funnene; dette betyr ikke at en ferdig adapter er levert.

Kildespor:
- CellProtocol/Sources/CellBase/Cells/CellResolver/CellResolver.swift:
  evictCellFromMemory, persistCellSnapshot, persistCellIfPossible.
- CellProtocol/Sources/CellBase/PersistingCells/TypedCellsUtility.swift:
  storeAsTypedCell fanger lagringsfeil; resolverens Bool er ikke en varig kvittering.
- CellProtocol/Sources/CellBase/Cells/GeneralCell/GeneralCell.swift:
  flow(requester:) og runtime-eid emitter.
- CellScaffold/Sources/ScaffoldKit/DistributedEntityData/EncryptedEntityAuthorityReplicaPersistence.swift:
  eksisterende kryptert, admission-bundet replikaadapter.
- CellProtocol/Sources/CellBase/PersistingCells/EntityAuthorityReplicaStore.swift:
  eksisterende admission-, journal- og readback-kontroll. Den krever reell authority/
  replica-binding og kan ikke erstattes med en oppfunnet tillatelse.

Dette er kildeanalyse, ikke utført crash-/race-/angrepsprøve.

Etterkontrollen fant også at en ny kommando B kunne avstemme pending A med Bs
admission-callback. Intern grense er endret til å returnere unknown(A) før readback
når ID-ene er ulike; bare A kan avstemmes med As admission. En trettende test er
skrevet for dette. Endringen er statisk kontrollert, ikke runtime-testet.

## Må leveres før W1 kan godkjennes

- Velge og verifisere konkret Entity-/journalgrense som alle skrivere følger; ingen
  vanlig autosave som kan omgå admission eller overskrive autoritativ historikk.
- Verifisert eier- og retention-binding før innsamling, samt W2 før-inventar/migrering.
- Varig outbox eller journalavledet at-least-once-levering. Den interne publish-callbacken
  er ikke en slik outbox. Tap mellom store og publish er fortsatt et integrasjonsgap.
- Eieravgrenset Flow med legitim, delegert feed-grant som negativ prøve, faktisk
  emitterbevis, revokasjon under await og avstemming subscribe→snapshot→eventsSince.
- Faktiske crash-/restart-/autosave- og samtidighetstester mot valgt lagring;
  modell-, perspektiv-, forslag-, kvittering- og feilhendelser må deretter kobles.
- Bounded bygg, relevante tester og full regresjon; uavhengig kontroll av samlet bevis før CI.

## Kø og kjørbarhet

Claude-køeier har reservert inbox-g2. Avstemmingen er i referansen i evidence-filen.
Ved denne avlesningen var d235.done ikke til stede og relaterte jobber aktive.
Mac hadde 101.11 GiB tilgjengelig; etter 10 GiB reserve var
det 91.11 GiB, under 10-prosentkravet
92.63 GiB. Dette er df-beregning;
kapasitetsgaten er ikke startet. Ingen bygg eller betalt CI er brukt av denne oppgaven.
Prod-hold står. G2 er ikke et nytt prod-mandat.
