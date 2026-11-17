# Fersk WP5/WP6-kildevurdering — 2026-10-05

## Brief audit

Kjetils godkjenning av designet og alle WP er opplyst av hovedtråden 2026-10-05 og legges til grunn. De leste PLAN/STATUS-filene fra 2. oktober sier fortsatt «forslag»/ingen godkjenning; de beskriver eldre dokumentstatus, ikke et nytt behov for å spørre brukeren. Ingen produktmutasjon, bygg, testkjøring, nettverk, prosessoppstart eller enhetstilgang i denne kontrollen. Bare denne rapporten er skrevet; læringsfangst hos hovedtråden.

Kildegrunnlaget har utviklet seg siden første rapport: en ekte personbundet to-prosess lesetest finnes allerede, og PR53s merge er tilgjengelig lokalt. Disse funnene må erstatte antakelser om fravær. Det som fortsatt ikke er dokumentert her, er hele AC5 med valgt konferansebidrag, riktig lagringsfullmakt, varig commit, tapt svar og read-back etter restart gjennom en felles produkt-ingress.

## Konkret anbefaling

**Implementer en avgrenset pull-reise:** Personlig runtime B henter ett valgt, godkjent WP2-bidrag fra konferanseruntime A som den virkelige deltakeren, og lagrer det hos seg selv under den personlige eierens fullmakt med eksisterende `EntityBatchPersistEnvelope` + `EntityAuthorityCommitRequest` + kvittering. Dette oppfyller retningen i F3/AC5 uten vilkårlig remote `entityData.set`, eieridentitetsbytte eller ny replikeringsprotokoll.

Enrollment er fortsatt relevant for teknisk innmelding og valg av betrodd scaffold, men er ikke alene samtykke til persondata eller selskapsrepresentasjon. Behold personens egen lagringsgodkjenning og kildebidragets `r`/`s`-omfang som egne autorisasjoner. Tapt svar etter commit avstemmes mot samme operasjons-ID/payload og eksisterende receipt; lag aldri en ny operasjon i en automatisk retry.

Første syntetiske fixture kan være én publisert eventopplysning eller ett manuelt godkjent notat. Endelig WP5-akseptanse bruker WP2s immutable bidragsversjon/proveniens og ikke et fritt valgt privat keypath.

## Eksakte kildebaser og status

Alle repo-relative ankere nedenfor er under HAVEN-roten. Absolutte checkouts er angitt fordi samme kilde finnes i flere varianter.

| Base | Eksakt ref og observert status | Bruk |
|---|---|---|
| `CellScaffold/.worktrees/oiw-conference-20261005` — `/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/.worktrees/oiw-conference-20261005` | `e5c3434510884275cae4a732935ab4b55cf7fad9`, ren ved kontroll | Foretrukket eksisterende OIW-integrasjonsbase. Lokal `origin/main` og `origin/release/2026.9.5` peker hit; ingen remote refresh gjort. |
| `/Users/kjetil/.codex/worktrees/entity-data-bridge/CellScaffold` | `fdcfe7a566ae4e73febbba464edb190e9e9cea08`, ren | Her ble Entity/enrollment/EventPlatform/prosesskilder lest. `git diff --quiet fdc… e5c…` for disse kildene og persist-helper returnerte 0. Linjeankrene gjelder derfor også e5c. |
| `/Users/kjetil/Build/Digipomps/HAVEN/_worktrees/cellscaffold-bridge-consumer-auth-20261005` | `e5c3434510884275cae4a732935ab4b55cf7fad9`, ren | Eget allerede opprettet Bridge consumer-spor. Koordiner kildeeierskap før felles ingress implementeres. Ingen endring ble funnet nå. |
| `/Users/kjetil/.codex/worktrees/bridge-pr53-integration/CellProtocol` | `14181968c8998c4543b42282c3559bc74ed6bddc`, ren; forelderlinje inkluderer merge `1ec56d59d13c20edb83b54687aaf393399ad0a15` | Kandidat med PR53-kanalbevis og ny scanner-følgeendring. Lokalt `origin/main` er 1ec56d5. Bruk eksakt felles pin etter WP0-gate. |
| `/Users/kjetil/.codex/worktrees/event-scaffold-structure/CellScaffold` | `71babb2f7f602e7b47f58aa8b2afaeaf2780c9cb`, ren, ikke ancestor av e5c | EventCells-ekstraksjon. Ikke kopier package-pathene herfra inn i e5 uten å velge/innlemme flyttingen. e5 bruker fortsatt `Sources/App/Cells/EventPlatform` og `Tests/AppTests`. |
| `/Users/kjetil/.codex/worktrees/credential-remote-use/CellScaffold` | base `fdcfe7a…`, dirty med endrede kilder og utrackede `AuthenticatedBridgeheadRoutes.swift`/tester | Felles kanalautentisert ingress finnes som skrevet kandidat. Status sier siste kilde ikke ferdig kompilert og AppTests ikke kjørt. Samordne og overfør avgrenset; ikke omtale som ferdig. |
| `/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold` | `942965ca24e9a418b531f9514c1da75d6d529e30`, omfattende dirty | Har en annen enrollment-implementasjon og utrackede EntityHomePolicy/DataRequest/DataAccess-filer. Disse finnes også i WIP-snapshot-ref `d3bc59ad89fcdaf87af957edd46ff64486adec69`, men er ikke valgt baseline. |
| `/Users/kjetil/Build/Digipomps/HAVEN/CellProtocol` | `253b4afe11af8b58bfcc433d9b7dc7393c761e24`, dirty på skeleton og utrackede audits | Skal ikke brukes som om den allerede var PR53-integrasjonen. |

WP0-pakken er en reell avhengighet: e5c `Package.swift:126–128` og `Package.resolved:40–45` pinner CellProtocol **2026.9.4 → 81601a6f835252aba7e99d43786fb5d67227c245**, som er før PR53. Den eldre fdc-worktreen pinner 2026.9.3 → 9c60001. Lokale package overrides finnes (`Package.swift:102–121`) men er ikke en publisert release-pin.

N35 må ikke dobbelt-cherry-pickes: `990fffe` er ikke ancestor av 1418196 (ulik historikk), men `git diff 990fffe HEAD` for `Sources/CellVapor/CloudBridge/VaporBridgeTransport.swift`, `Sources/CellBase/Cells/Bridging/BridgeMultiplexing.swift` og `Tests/CellBaseTests/VaporWebSocketAdmissionTests.swift` var tom i CP-kandidaten. Dette beviser likhet i disse filene, ikke hele repoet eller en ny testkjøring.

## Dagens gjenbruk og grenser

### Entity/innmelding

På e5c/fdc:

- `CellScaffold/Sources/App/Cells/EntityScaffoldEnrollment/EntityDataGatewayCell.swift:7–56` bruker innrømt personbevis til å finne eksisterende eierinstans, men utfører faktisk query som den opprinnelige linked requesteren. Gatewayen eier ingen personstate og gir ikke service/person-ekvivalens.
- `EntityScaffoldEnrollmentCell.swift:664–698` revaliderer scaffold-link etter resolver/read/lifecycle-await og avviser beskyttede undertrær. `746–855` krever personlink, `linked_identity_proof`, riktig nøkkel/domene og separat evidence store; query gir `independent-reads`, `revisionVerified=false`, `retained=false`.
- Dette korrigerer den gamle generelle «ingen recheck etter await»-vurderingen for **lesing**. `Tests/AppTests/EntityScaffoldEnrollmentCellTests.swift:535–559,678–699` har konkrete read-/aggregate-revoke-tester. Ingen av dem ble kjørt her.
- **Legacy write er fortsatt feil utgangspunkt for AC5:** `EntityScaffoldEnrollmentCell.swift:704–731` kaller `anchor.set(...requester: authorization.ownerRequester)` og gjør nil-resultat til `.null` i en allowed-respons. `927–992` viser owner-signing mediation og godkjente scaffold-caps. Det er ikke signert receipt, end-to-end virkelig aktør eller atomisk write/revoke-fence. `Documentation/Entity_Data_Query_v1.md:92–96` sier eksplisitt at den siste grensen er åpen.
- `handleRevoke` (`597–616`) oppdaterer state og emitterer; denne kroppen inneholder ingen eksplisitt `persistCellSnapshot`-kvittering. Ikke påstå varig revokering etter restart bare fra responsen. Den andre dirty implementasjonen har eksplisitt snapshot-persist, men er en annen kildevariant.

### Varig personlig lagring

I CP1418196:

- `Sources/CellBase/PersistingCells/EntityBatchPersistEnvelope.swift:42–59` har allerede metadata og valgfri `commitRequest`.
- `Sources/CellBase/PersistingCells/EntityAuthorityCommit.swift:80–97,131–186` har mutation ID, epoch, forventet revisjon/head, payload-hash, virkelig requesternøkkel, formål, capability og signatur.
- `Sources/CellVapor/Cells/EntityAnchorCell.swift:862–940` krever eierbevis og kjent formål; journalgrenen skriver authority journal og returnerer receipt/idempotentReplay. Snapshot uten commitRequest er en annen svakere gren.
- `Tests/CellBaseTests/EntityAuthorityCommitTests.swift:25–76` uttrykker signert/idempotent kvittering, samme mutation-ID og ett journalinnslag. `:232` tester gjenoppbygging etter avbrutt snapshot. Kvitteringen er uttrykkelig **local_authority_only**, ikke distribuert quorum.
- Dagens `CellScaffold/Sources/App/Support/IdentityEntityPersistenceSupport.swift:26–79` returnerer Void og lager envelope uten commitRequest. Ikke kall denne helperen et fullstendig kvitterings-API. Legg en liten typed receipt-variant i eksisterende hjelpeflate eller en avgrenset personlig import-Cell; gjenbruk CPs modell og returner faktisk verifisert receipt.

### Bridge og testadaptere

- `CellScaffold/Tests/AppTests/EntityPersonBridgeProcessTests.swift:18–20,29–34,63–105` starter ekte andre XCTest-prosess og holder linked klientnøkkel i klientprosessen. `:133–169` gjør ekte Bridge/query/read; `:171–188` avviser annen service og lesing etter tilbakekalling på samme forbindelse. Dette er en sterk gjenbrukbar prosessramme, ikke bare en mock.
- Samme fil `:240–245` registrerer testceller som ephemeral; den beviser ikke AC5s varige mottakerrestart. `authenticatedRoute=true` bruker den eldre personspesifikke HTTP discovery/WS-ruten, som ikke skal kopieres som produktløsning når kravet er felles Bridge. `false` er en test-only listener. Behold prosess/fixture/logg-harness, erstatt bare inngangen med felles autorisert route og legg til mottakerlagring/restart.
- `CellProtocol/Tests/CellBaseTests/BridgeChannelProcessTests.swift:10–50,55–105` gir en annen ekte prosessharness: `BridgeChannelTransport` + `VaporBridgeTransport` + `BridgeBase`, server-signing-trap og eksplisitte proof-scopes. Den bruker en liten mock resolver/probe-cell; nyttig kanalbevis, ikke ferdig Entity-produktreise.
- `CellScaffold/Sources/App/Controllers/AuthenticatedBridgeheadRoutes.swift:37–79` i **credential-remote-use**-kandidaten komponerer `/bridgehead/session` mux og `/bridgehead/:publisher` med kanalbevist requester. Tester `AuthenticatedBridgeheadTests.swift:19,23` er skrevet for metadata, linked requester og revokering. Kandidatens `Deliverables/Remote_use_2026-10-03/STATUS.md` sier at de nye AppTests ikke er kjørt. Dagens felles produkt-ingress må derfor integreres én gang, ikke parallelt i WP5 og credential-sporet.
- `RemoteBridgeheadAccess.swift:48–70` er host/port-scopet bearer-routehjelp, ikke person-/medlemsfullmakt. Ikke send en operatørbearer til deltakere for å løse AC5.
- CP1418196 `CellResolver.swift:2238–2258,2329–2338` lager BridgeBase uten eksplisitte child proof-scopes. `Entity_Data_Query_v1.md:66–73` beskriver den eksakte gateway/query/anchor-scopegrensen. Et direkte smalt bidragspublisher-endepunkt kan redusere antallet scopes, men scopevalg må fortsatt være innrømt lokalt og verifisert; aldri wildcard signing. Setup over felles Bridge og senere Meddle/Flow er to separate bevis.

## Foreslått smal implementasjonsgrense for WP5

**I valgt e5c-worktree, produktkode:**

1. Ett lite adapter-/Cell-lag for «lagre valgt konferansebidrag hos meg», på eksisterende konferanse-/personlig Cell-flate. Input binder immutable WP2 artifact ID/version/hash, kildeorigin+cell-ref, faktisk aktør, mottakerens lokale Entity og eksisterende `r`/`s` authority. Ingen vilkårlig host/keypath fra ubetrodd tekst. Navn/keypaths besluttes med WP2; ingen ny protokoll antas eksisterende.
2. En typed kvitteringsvei rundt eksisterende EntityAnchor batch/authority commit i `Sources/App/Support/IdentityEntityPersistenceSupport.swift` eller den nye lille import-Cellen: samme mutation ID, forventet epoch/revisjon, signert payload, receipt-verifikasjon og read-back. Oppbevar nøyaktig request til utfallet er avklart; timeout/nil gir unknown/pending.
3. Gjenbruk felles ingress-arbeidet fra bridge-consumer/credential-spor; avgrens eventuell overføring til controller, route-registrering og deres autentiseringstester. Ikke ta med credentials/UI/provider-kode bare for å få Bridge.
4. Ny smal `Tests/AppTests`-prosessreise, bygget av den eksisterende EntityPersonBridgeProcess-harnessen. To egne prosesser, to isolerte datarøtter/vaults, faktisk nettverkskanal og kontrollerte stopp/restart. Bruk syntetiske identiteter og eksakt pin; ingen fysiske enheter nødvendig for denne WP5-reisen.

**AC5-sekvens:** A publiserer én immutable valgt bidragsversjon med riktig grant → B beviser sin egen actor over felles Bridge → A returnerer bare den versjonen innenfor current authority → B sjekker egen lagringsbeslutning og mottaker → B committer lokalt med eksisterende signert EntityAuthority-modell → behold receipt og proveniens → stopp/start B → samme kildehash og personlig data leses tilbake → simuler tapt kvitteringssvar, avstem samme mutation ID og bevis ett journalinnslag. Gjenta med feil actor/domene, utløpt grant, revokering ved deterministisk barriere, endret versjon og tilbaketrukket personlig lagringstillatelse.

Revokering må ha et presist lineariseringstidspunkt. Legg admission/reservasjon ved den endelige effekten i den aktuelle app-Cellen og hold den gjennom commit; en sjekk før `await` eller å skjule et sent svar er utilstrekkelig. En allerede lovlig hentet artefakt med eksplisitt lagringsrett er ikke automatisk «ulovlig lagret» fordi fremtidig kildeaccess senere trekkes tilbake; avtal lease-/revokeringssemantikken i WP2-manifestet og test begge sider av grensen. Dette er ikke en distribuert transaksjon.

## WP6: konkret gjenbruk og faktisk hull

På e5c brukes `Sources/App/Cells/EventPlatform/`:

- `EventPlatformModels.swift:19–50,73–88`: detaljerte permissions; admin er preset/avledet label; assignment har requesterUUID, permissions, addedByUUID, updatedAt. Ingen medlemsstatus, expiry eller principal fingerprint/domain i dette formatet.
- `EventPublisherRegistryCell.swift:430–469`: flere medlemmer/adminer, endring av permissions og vern av siste `manageMembers`. Tom permission-liste avvises (437–438). Bounded søk av register/model/test fant ingen separat medlemsfjerning/revoke/expiry-operasjon. Nedgradering til viewer er ikke full utmelding.
- `EventPublisherAccessSupport.swift:43–62,65–99`: oppslag er normalisert UUID og permissions; ingen expiry-/revocation-filter eller bound requester-key i denne funksjonen. Dette er et presist gjenbrukshull for AC6, ikke bevis for en generell sårbarhet i eksisterende controller.

**Smal WP6-endring:** utvid eksisterende assignment/ACL og setMember-flate med eksplisitt aktiv/tilbakekalt eller fjerning/tombstone samt controlled expiry. Bevar tidligere audit/proveniens. Siste-administratorregelen må telle **aktive, ikke-utløpte** `manageMembers`, også ved fjerning/utløp. AccessSupport bruker samme current-policy-filter for alle relevante handlinger. Publiseringskontroll og rettighetsendring bør bruke samme serialiserte registergren og skje før state-effekt; async fremtidig lagring må ikke åpne et hull mellom sjekk og commit.

For remote selskapsbruk må assignment knyttes til innrømt requester-principal/domene/nøkkel, ikke bare tekst-UUID-normalisering. Bevar kompatibel lokal migrering, men ikke la en gammel ubundet assignment bli portabel autoritet automatisk. Representasjonsvalget i UI velger bare hvilket eksisterende mandat som brukes; det skaper ingen rettighet. `publishEvent` skal fortsatt ikke gi privat møtedataaccess. Behold personlige notater i personens egen Entity og test uendret kontroll ved utmelding.

Foreslått kildegrense: `EventPlatformModels.swift`, `EventPublisherAccessSupport.swift`, `EventPublisherRegistryCell.swift`, eksisterende tilhørende testfil og nødvendig medlemsskjema/skeleton-binding. Ikke opprett ny CompanyCell/GroupProtocol eller endre generelle identity-/grant-semantikker for denne skiven. Hvis WP1 velger EventCells-ekstraksjonen, følger de samme filene sin nye sti og package-level tilgjengelighet; dette må besluttes én gang i WP0/WP1.

## Reelle avhengigheter og avslutningsbevis

1. **WP0: en koordinert package-graf.** Nåværende release-pin er før PR53. Den dirty remote-use-statusen dokumenterer SwiftPM stable/unstable-konflikt ved blanding av lokal CP og publiserte DiMy-pakker; bruk de eksisterende tre LOCAL_PACKAGE_PATH-valgene til en kontrollert integrasjonsgraf og behold release-pinnen ærlig. Disk-/buildgrenser følger eksisterende bounded runner; ingen bygg forsøkt her.
2. **Felles Bridge ingress og route/proof-scope-kompatibilitet.** Eget consumer-spor og credential-kandidat finnes allerede. Avklar kildeeier, exact API-revisjon og om første reise bruker én dedicated publisher-kanal eller mux. En test-only listener alene sertifiserer ikke app-ruten.
3. **WP2-manifest/grant.** Immutable bidrag, source-origin, version/hash, publikum, `r`/`s`, korrigering og withdrawal-semantikk må være definert. Ingen behov for generell personquery eller multi-master for den første reisen.
4. **Personlig eierkontroll.** B har egen ekte signer/vault; A får ikke B-nøkkelen. Hvis UI sitter på A og B er headless, må en allerede autorisert personlig importtjeneste på B håndtere jobben under B-eierens scoped fullmakt. Dette er et ekstra adapterbehov, ikke lov til å erstatte aktøren med A-eier.
5. **WP6 local-first og separat portabilitet.** Full revokering/expiry kan implementeres og testes i eksisterende lokale register nå. Portabel company-principal og grant må følge WP5-boundary før cross-scaffold representasjon påstås.
6. **Fresh test evidence.** Eksisterende testkilder er konkrete gjenbruksadaptere, men ingen kjøring her. Historiske docs skal ikke telle som AC5/AC6. Krev exact ref/config, to PIDer/datagrensene, receipts, restart/read-back og negative handlinger med zero forbidden effect.

Konklusjon: Implementeringsarbeidet kan være et lite produktlag over eksisterende Bridge og EntityAuthority, pluss en smal utvidelse av publisher-ACL. Den vesentlige usikkerheten er kobling og endelig autorisasjon/persistens, ikke fravær av en transport- eller Entity-protokoll. Ikke gjeninnfør personspesifikk HTTP/WS eller påstå at legacy writes allerede gir AC5-kvitteringer.
