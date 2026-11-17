STATUS: LEVERT — anbefaling: merge etter 2 rettinger, 4 funn (2 blokkerer)

Astra / Codex, 28.09.2026. Lese- og vurderingsjobb. Ingen kodeendring, testendring, commit, push, merge, utrulling eller produksjonsimport er utført. Denne rapporten er eneste leveransefil.

Vurdert [CellScaffold PR #270](https://github.com/Digipomps/CellScaffold/pull/270), head `9209ce100446866c9869550ca53273665fde4304`, mot base `feec23725321320ab00f0e7f7bf728b775869ec7`. GitHub bekreftet åpen PR med disse SHA-ene. Kode og linjenumre nedenfor er fra `git show`/`git diff` på head, aldri fra det skitne arbeidstreet. CellProtocol-pinnen er uendret: `2026.9.3`, SHA `9c60001ac53abc35ba7ad6e2c0efa2a79ab2a366`.

Utstedelsesstien og skillet mellom kunstnernøkkel og Digipomps-nøkkel er i hovedsak godt avgrenset. Jeg anbefaler likevel ikke merge av dagens head: første overtakelse binder ikke mottakernøkkelen til den navngitte kunstneren, og lagringsvernet aksepterer en katalogkjede som kan tillate utskifting av hvelvets navnerom. Grønn CI endrer ikke disse kildefunnene.

«Blokkerer» i første linje betyr merge-blokkerende. F3–F4 er avgrensninger i verifikasjonen som må lukkes før AP6; de er ikke påståtte, reproduserte produktfeil.

| Funn | Prioritet | Merge | Før AP6 |
|---|---|---|---|
| F1: Token + selvvalgt ekstern nøkkel kan overta som kunstner | P1 | Blokkerer | Rett og test mottakerbinding |
| F2: Katalogkjede/ACL og binding til lease-navnet er ikke sikret | P1 | Blokkerer | Rett, test og kontroller produksjonsroten |
| F3: Grønn CI dekker ikke de to røde manifestskriver-testene | P2 | Blokkerer ikke alene | Avklar og kjør relevante manifest-/lagringstester |
| F4: Full gjenstart under overtakelse og virkelig ekstern klient er ikke bevist | P2 | Blokkerer ikke alene | Dokumenter gjenstart og klientløype |

**F1 — Korrekt nøkkelkontroll beviser ikke at mottakeren er den navngitte kunstneren.**

Hovedanker: [Sources/App/Cells/ManagedArtistImport/ManagedArtistIssuanceVault.swift:433](https://github.com/Digipomps/CellScaffold/blob/9209ce100446866c9869550ca53273665fde4304/Sources/App/Cells/ManagedArtistImport/ManagedArtistIssuanceVault.swift#L433), særlig 438–444. Før første claim er `claimedIdentity` nil; sammenligningen på linje 439 tillater da enhver requester som består de øvrige kontrollene. `prove` bruker requester selv som `trustedIdentity` ved linje 380. `ManagedArtistImportScope` har slug, navn, samtykke og brukstall, men ingen mottakernøkkel eller uavhengig overtakelsesmyndighet (`ManagedArtistImportTypes.swift:24–35`).

Konkret forløp: Den autoriserte importøren velger/sender `claimToken` ved execute (`ManagedArtistIssuanceVault.swift:468–492`) og kjenner derfor tokenet. Etter import kan samme person bruke en ny UUID og sin egen eksterne signeringsnøkkel gjennom `BridgeIdentityVault`, sende tokenet og begge attestasjonene som true, og signere de friske utfordringene. Kollisjonskontrollene på linje 449–455 avviser eldre UUID-myndighet; de avviser ikke en ny identitet. Deretter flyttes eierskapet, og `ArtistSalesChannelCell.swift:1807–1810` setter `artistAttestedAt`. Offentlig projeksjon blir `rightsOwnershipAttested=true` og `attestation=artist` (`ArtistSalesSupport.swift:244–245`).

Dette krever verken serverkompromiss, en stjålet kunstnernøkkel eller brudd på signaturkontrollen. Det er en autorisasjonsmangel før første nøkkelbinding. Også en uvedkommende som får tokenet, kan skaffe den øvrige nødvendige «faktoren» selv. Administratorens direkte redigeringsnekt og UUID-vernet løser ikke dette.

Evidensgrense: Forløpet er utledet fra hele claim-/proof-stien, ikke kjørt som et nytt angrep i denne jobben. De eksisterende positive testene bruker nettopp en ny, tilfeldig UUID og en ny nøkkel uten kunstnerbinding (`ManagedArtistImportTests.swift:561–565, 622–631`); alle 23 tester passerer i CI. Testen som avviser `runtime.importer` ved linje 334 prøver en lokal vault-identitet, ikke importøren med en ny ekstern identitet.

Rett før merge: Bind overtakelsen til en mottakernøkkel som er godkjent gjennom en separat, dokumentert verifikasjon av den navngitte kunstneren. Når kunstneren ennå ikke har identitet ved import, må bindingen etableres senere, før endelig claim og attestasjon. Den som bare har importmandatet/tokenet, må ikke alene kunne opprette denne bindingen. Behold den friske signeringsutfordringen og bind den til den godkjente nøkkelen. En kontroll av displayName, eller bare avvisning av importørens gamle UUID, er utilstrekkelig. Legg til negativ test med riktig token + ny importørstyrt ekstern nøkkel og positiv test med godkjent kunstnernøkkel.

Hvis tilsiktet produktpolicy faktisk er at enhver tokeninnehaver får velge kunstneridentiteten, må den tillitsgrensen avklares eksplisitt. Dagens kilde støtter da en tokenstyrt overdragelse, men ikke påstanden om at bare kunstneren kan bekrefte og overta. Denne gjennomgangen legger kravet om kunstnerens egen bekreftelse til grunn.

**F2 — Filmodus og `O_NOFOLLOW` beskytter ikke hele navnerommet som leasen skal gjelde.**

Hovedanker: [Sources/App/Cells/ManagedArtistImport/ManagedArtistIssuanceVault.swift:27](https://github.com/Digipomps/CellScaffold/blob/9209ce100446866c9869550ca53273665fde4304/Sources/App/Cells/ManagedArtistImport/ManagedArtistIssuanceVault.swift#L27). Linje 31–38 åpner hvert ledd uten symlink-følging, men kontrollerer ikke eier, gruppe-/andre-skriverettigheter eller ACL på root/forfedrene. Bare den siste hvelvkatalogens UID og modus kontrolleres ved linje 43–45. Heller ikke den katalogen eller filene får ACL-kontroll. Senere driftkontroll leser `vault.crypt` relativt til det allerede åpne katalogdeskriptoret; den verifiserer ikke at den konfigurerte stien fortsatt peker dit, eller at `.lease` fortsatt er samme inode (`:61–63, 91–118`).

Konkret betingelse: En eksplisitt, absolutt rot under en katalog der en annen konto kan omdøpe oppføringer, aksepteres. Den andre kontoen kan flytte hvelvkatalogen uten å lese innholdet i dens 0700-katalog. Første prosess fortsetter da mot sitt åpne katalogdeskriptor og gamle lease. En senere legitim oppstart kan opprette en ny 0700-katalog og ny `.lease` på den opprinnelige stien og få en annen lås. Dermed gjelder «én lagringssti / én skriver» ikke lenger det samme navnerommet. Dette er betinget av utrygge katalogrettigheter; jeg har ikke påstått at produksjonsroten har dem. Det er svakere enn bare den dokumenterte resttrusselen «OS-konto kompromittert».

OS-semantikken støtter vurderingen: `flock` er knyttet til den åpne filbeskrivelsen, og omdøping styres av katalogrettigheter. Se [Linux flock(2)](https://man7.org/linux/man-pages/man2/flock.2.html) og [rename(2)](https://man7.org/linux/man-pages/man2/rename.2.html). Apple beskriver dessuten hvorfor låsing alene ikke beskytter mot uvedkommendes filendringer i [Race Conditions and Secure File Operations](https://developer.apple.com/library/archive/documentation/Security/Conceptual/SecureCodingGuide/Articles/RaceConditions.html). Angrepsforløpet er en kilde-/OS-basert vurdering; ingen slik manipulasjon er utført på brukerens filer.

Rett før merge: Håndhev en uttrykkelig betrodd katalogkjede med effektive tilgangsrettigheter, inkludert ACL, og avvis uvedkommendes mulighet til å bytte katalog/lease. Kontroller nødvendig sti-/inode-kontinuitet ved drift. Gjenbruk etablerte sikkerhetsprinsipper uten å svekke sentralhvelvet; eksempelvis har `Sources/App/Support/SecureRuntimeIdentityManifestFile.swift:80–86` eksplisitt ACL-kontroll. Legg til negative tester for skrivbar forelder, ACL, omdøpt katalog/utskiftet lease, hardlink og feil modus/eier. Dagens test ved `ManagedArtistImportTests.swift:276–291` dekker andre skriver i samme prosess, en rot-symlink, feil nøkkel og endrede ciphertext-bytes, men ikke disse tilfellene.

**F3 — Manifestskriverens kjente røde tester er ikke avklart av grønn Linux-CI.**

Hovedanker: [ci/test-filter.txt:40](https://github.com/Digipomps/CellScaffold/blob/9209ce100446866c9869550ca53273665fde4304/ci/test-filter.txt#L40). Linje 40–47 velger åtte enkeltmetoder fra `CellScaffoldRuntimeIdentityProvisionerTests`. `testWriterRejectsExtendedAttributesOnExistingManifest` og `testWriterRejectsOverwriteWithoutExactOldDigestAndUses0600` er ikke blant dem. `SecureRuntimeIdentityManifestFileTests` er dessuten allerede unntatt ved `ci/test-exclusions.txt:25`. Dette er uendret fra basen, ikke en ny exclusion i PR-en.

Jeg har lest feillinjer i `evidence-runde3/final-tests.log`, de tre `clean-base-N.log` og `clean-base-canonical-tmp.log`. Begge navngitte tester feiler med `manifestWritePreconditionFailed` også i alle tre baselogger. Handoff knytter basen til `feec2372`; disse kjøringene er ikke gjentatt av meg. Kilde-diffen viser uendrede writer-/provisioner-filer og tester. Det er dermed ikke grunnlag her for å tilskrive feilene PR #270. Det er heller ikke grunnlag for å si at akkurat disse testene er grønne på Linux.

Før AP6: Kjør de relevante writer-/ACL-/rettighetstestene med en gyldig, beskyttet testrot og dokumenter resultatet, særlig siden nytt eier-signert manifest må provisjoneres. Bevar avvisningsreglene. Rapporter eventuell videre baseline-feil med egen årsak; ikke bruk hele suitenavnet eller grønn workflow som erstatning for metodene som mangler.

**F4 — Gjenstart og ekstern brukerflyt har smalere testbevis enn en produksjonsklar AP7-kjede.**

Hovedanker: [Tests/AppTests/ManagedArtistImportTests.swift:373](https://github.com/Digipomps/CellScaffold/blob/9209ce100446866c9869550ca53273665fde4304/Tests/AppTests/ManagedArtistImportTests.swift#L373). Avbruddstesten kaster etter ArtistSales-overføring og prøver igjen i samme prosess med samme celleobjekter. Hvelv-reload-testen ved `:257–273` gjenoppretter hvelvet i `active`, ikke hele runtime med begge postlagrene i `transferring`. Peer-fixturen ved `:622–631` signerer ekte utfordringer, men er en testklasse i testprosessen.

Ingen konkret gjenstartsfeil er påvist. Koden har en fornuftig mellomfase, men testene beviser ikke en kald gjenstart ved alle lagringsgrenser, tap av strøm, eller overtakelse fra en virkelig Binding-/annen ekstern klient. `ManagedArtistIssuanceVault.swift:559–567` verifiserer serialisert readback av cellene; dette er ikke i seg selv bevis for en atomisk transaksjon over mandat, hvelv, Publication og ArtistSales.

Før AP6: Stopp/start en isolert runtime ved mandatforbruk, etter utstedelse og ved begge eierskiftelagringene; last alle lagre på nytt. Verifiser skjulte flater mens overføring pågår, samme mottakers gjenopptakelse, avvist annen mottaker/replay og varig key retirement/tombstone. Kjør deretter virkelig ekstern signering over den planlagte transporten, med kunstnernøkkelen kun på klienten. Dette kan gjøres med testidentitet; Sindres produksjonsovertakelse skal ikke brukes som første test.

**1. Trusselflate og utstedelse.**

På den leste headen finnes én faktisk opprettelsesmetode og ett kallested: `ManagedArtistIssuanceVault.issue(consumed:seedDigest:tokenHash:)` er `fileprivate` ved linje 201, og kalles bare fra coordinator ved linje 492. Kallestedet følger `consumeArtistImport` ved linje 491. Søk i hele `Sources` på head fant ingen annen opprettelsesinngang til dette hvelvet.

Myndighetskjeden er: eksisterende eier-signert representantmyndighet → signert `artistImport`-mandat → bevist mandatmottaker → lagret forbruk → utstedelse. `ScaffoldMandate.swift:104–115` krever eksakt ressurs, action, purpose, 24 timer og scope med én bruk. Signaturgrunnlaget ved `:140–147` inkluderer hele mandatet unntatt signatur-arrayet, altså også samtykket. `ScaffoldMandateCell.swift:249–266, 362–384` kontrollerer representant, signaturer, requesterens nøkkelbinding, gyldighet, revokering, eventuell orgLink og den lagrede proof-kopien. Generisk mandatbruk avviser typen (`:336`).

`ScaffoldMandateCell.swift:657–669` bruker mandatcellens mutation gate, setter `consumedAt` og `consumedSeedDigest`, og persisterer før retur. Persistensen leses tilbake og sammenlignes før `state` byttes (`:545–553`). Coordinatorens egen gate beholdes over async-operasjonene (`ManagedArtistIssuanceVault.swift:351–365, 388–394`), hvelvets tilstand beskyttes av `NSLock`, og issue nekter både samme mandat-ID og samme artistSlug (`:203–207`). Replay/parallelle execute-kall har derfor reelt vern i den normale, intakte lagringen. Testene ved `ManagedArtistImportTests.swift:66–77, 294–303` dekker gjenbruk og to samtidige kall.

Viktig presisering: Argumentet `consumed` er fortsatt et vanlig `ScaffoldMandate`; utstederen verifiserer ikke selv en kryptografisk forbrukskvittering. «Bare forbrukt, signert mandat» er en invariant i det ene private kallforløpet, ikke en selvstendig HSM-/tjenestegrense. Jeg fant ingen annen nåværende Cell-/resolverinngang som bryter den. `addIdentity`/`saveIdentity` gjør ingenting, og create-on-lookup returnerer nil (`:248–255`).

Det finnes én ny registerpolicy og ett nytt inventarført kallested: `managedArtistImport` / `managed-artist-import.consumed-mandate`, med `separateIssuanceVault`, `ownerApprovedIssuance`, `externalVaultOnly` (`Sources/App/Support/CellScaffoldRuntimeIdentityRegistry.swift:885–892, 1005`). Registeret beskriver/validerer inventaret; selve mandatkontrollen ligger i koden ovenfor.

Det finnes én fast snapshot-sti per konfigurert rot: `CELL_VAULT_DOCUMENT_ROOT/DigipompsManagedArtistIssuance/vault.crypt`; i tillegg `.lease` og kortvarige `.pending-<UUID>` i samme katalog (`ManagedArtistIssuanceVault.swift:23, 39, 47, 67`). Ingen seed-, slug- eller tokenverdi velger filsti. **Antallet innganger/policyer/snapshot-stier stemmer; F2 begrenser sikkerheten i selve sti-/lease-bindingen.**

Lagringsvern som faktisk finnes: `openat`/`O_NOFOLLOW` gjennom stien; 0700 på hvelvkatalog; 0600, eier-UID, regulær fil og `st_nlink == 1` på lease/snapshot; maksimal snapshotstørrelse; AES-GCM med fast schema-AAD; eksklusiv midlertidig fil, `fsync`, `renameat`, katalog-`fsync` og readback (`:27–118, 150–169, 237–243`). `assertCurrent` avviser avvik fra sist lastede bytes. Et autentisert eldre snapshot ved ny oppstart har derimot ingen ekstern monoton forankring. Driftsnotatets forbehold om backup/rollback er reelt.

**Krypteringsnøkkelen:** Dagens API leser `MANAGED_ARTIST_ISSUANCE_KEY_B64` fra CellScaffold-prosessens miljø (`:305–315`). Den må altså være tilgjengelig i klartekst for denne serverprosessen; den beskytter Digipomps' midlertidige signeringsnøkler på disk. Dette er adskillelse fra sentral-/brukerhvelv i kode og lagring, ikke en separat OS-prosess eller HSM. En kompromittert appprosess/vertskonto med tilgang til miljø eller minne kan også nå denne nøkkelen. Kunstnerens egen private nøkkel er en annen nøkkel og skal forbli på klienten.

Drift må oppbevare/provisjonere en separat tilfeldig 32-byte hemmelighet og injisere den i den tiltenkte runtime; aldri legge den i repo, image, seed, rapport eller vanlig logg. Headen har ingen `..._KEY_PATH`-leser for denne nøkkelen og ingen deploy-wiring for navnet: søk på head fant bare runtime-leseren og driftsnotatet. Bare å legge variabelen i verts-shell eller Compose `.env` er derfor ikke dokumentert ende-til-ende provisjonering. Eksisterende `docker-compose.yml:131–139` viser eksplisitt miljøoppsett for sentralhvelvet, ikke denne nøkkelen. Ingen virkelige hemmeligheter eller container-miljøer er lest i gjennomgangen.

Manglende variabel, ugyldig base64, feil lengde eller ikke-absolutt rot gir `unavailable`; feil 32-byte nøkkel mot eksisterende snapshot feiler GCM-dekryptering. Ingen automatisk krypteringsnøkkelgenerering eller fallback finnes. `visible`/`editable` returnerer false når hvelvet ikke kan åpnes/leses (`:321–344`). Kontrollen er lazy: hele appoppstarten er ikke nødvendigvis rød; import og administrerte offentlige data stenges. Et allerede cachet hvelv beholder nøkkelen i minnet, så endring av miljøverdien alene roterer ikke nøkkelen. På et tomt hvelv kan koden naturligvis ikke vite at en ellers gyldig 32-byte nøkkel er operasjonelt «feil».

**2. Sentral strict runtime og registerdiff.**

`Sources/App/configure.swift`, runtime-manifest, provisioner og `SecureRuntimeIdentityManifestFile.swift` er byte-uendret mellom base og head. Det samme gjelder manifest-/provisioner-/secure-file-testfilene, `Package.swift` og `Package.resolved`. Strict-aktivering og revisjons-/bindingstallkontroll står fortsatt ved `configure.swift:546–558`. Pinnet CellProtocol avviser ukjent dynamisk opprettelse i strict ved `Sources/CellVapor/VaporIdentityVault.swift:2245–2249` og varig `addIdentity` ved `:2269–2271`.

Registerdiffen er begrenset til consumer/context-enumerasjoner, én dynamisk policy og ett kallested. Testdiffen oppdaterer 18→19 policyer, 20→21 kallesteder, kildeevidens og digest-golden. Antallet sentrale bindinger er fortsatt 28. Ingen strict-denial-assertion er fjernet eller svekket. Den nye profildigesten i golden-testen er `sha256:A8BXBMIAHkiiTiVJXqNLQ9FxRsgeb7di3qaYtwmVcUQ` (`CellScaffoldRuntimeIdentityRegistryTests.swift:589–593`); produksjonsmanifestet må utstedes for sin faktiske kompilerte profil, ikke kopiere en testverdi ukritisk.

Ny test `ManagedArtistImportTests.swift:115–140` aktiverer strict før import/claim, sammenligner sentralfilens bytes, revisjon og bindingstall, og prøver avvist opprettelse før/etter. Den passerer i CI. **Ja: de leste strict-reglene og relevante eksisterende tester er uendret; register-/digest-endringene er nødvendige for den nye policyen.** F3 beskriver hva CI ikke dekker.

**3. AP7: nøkkelkontroll, mellomfase, sletting, fjerning og frist.**

Nøkkelkontroll: `prove` genererer 64-byte nonce, bruker strukturert challenge med domene/resource/action/audience og verifiserer signaturen mot offentlig nøkkel (`ManagedArtistIssuanceVault.swift:367–385`). Claim krever `BridgeIdentityVault`, korrekt tokenhash, eksplisitte attestasjoner og en ekstra challenge bundet til import-ID, seed-digest og tokenhash (`:433–445`). Pinnet `CellProtocol/Sources/CellBase/Identity/BridgeIdentityVault.swift:58–75` har ingen lokal opprettelse eller nøkkelimport; den sender signering til eksisterende bridge. Dette beviser kontroll over presentert nøkkel. F1 gjelder hvem nøkkelen representerer.

Kunstnerens private nøkkel: Claim-payloadens tillatte felter inneholder ingen nøkkelfelt; ukjente felter avvises (`:400–407`). Persistensen bruker `publicIdentitySnapshot`, og ingen kunstnernøkkel føres inn i sentral-/utstedelseshvelvet. Testen ved `ManagedArtistImportTests.swift:339–369` dekrypterer issuance-snapshot og inspiserer serialiserte celler for fixturens private bytes/base64. Dette støtter nøkkelgrensen i den leste API-stien. Det er ikke en audit av alle transportlogger, andre innloggingsruter eller en virkelig klient. BrowserClientIdentityVault skal fortsatt ikke brukes til denne overtakelsen.

Token: Serveren krever dekodet lengde 32 bytes og lagrer SHA-256 (`:570–572, 215–217`). Serveren kan ikke måle klientens tilfeldighet; sikker generering er et klient-/driftskrav. Tokenet kommer nødvendigvis inn som requestverdi, men lagres ikke i de leste importrecord-/receipt-/Flow-stiene. Generisk `GeneralCell.set` er også lest ved den pinnede CellProtocol-revisjonen (`:1781–1871`); den lagrer ikke automatisk hele setter-payloaden. Øvrig transport-/observability-pipeline: **ikke lest fullstendig**.

Mellomfase: `transferring` persisteres før ArtistSales og Publication endres, begge celler persisteres/readback-kontrolleres, så settes `claimed` (`:456–462, 559–567`). Public delivery og ordinær redigering av administrert innhold er stengt i `transferring` (`:321–333`). Gjenopptakelse krever samme allerede registrerte nøkkel, token og nye signaturer. Post-ID-er og mediereferanser beholdes (`ArtistSalesChannelCell.swift:1793–1817`, `PublicationCell.swift:1750–1772`). F4 avgrenser restartbeviset.

Forvaltet nøkkel: Signering er bare tillatt i `importing` (`:275–280`). Etter ferdig import i `active` beholdes nøkkelen kryptert, men kan ikke brukes gjennom vault-API-et. Ved `claimed` eller `removed` settes `privateSigningKey` og `tokenHash` til nil i neste persisterte snapshot (`:224–243`). Den forvaltede nøkkelen overføres aldri til kunstneren. Sletting gjelder gjeldende snapshot; koden gir ikke bevis for nullstilling av all RAM, sletting av gamle filsystemblokker, snapshots eller backups. Ved bare 30-dagersutløp slettes heller ikke nøkkelen; fristen styrer synlighet.

«Fjern alt»: Bevist registrert claimant eller gjeldende administratorrepresentant kan sette terminal `removed` (`:421–431`; `ScaffoldMandateCell.swift:673–677`). Det avpubliserer varig via hvelvets fase, også direkte previews; det sletter ikke verk/media/historikk. Det samsvarer med formålets uttrykkelige avpublisering. `reason` valideres, men lagres ikke som egen fjerningsårsak i recorden; kvitterings-Flow inneholder bare operasjonsnavn. Dette er en begrensning i etterprøvbarhet, ikke et femte merge-funn.

30 dager: Lesekontrollen er `now < createdAt + 30*24*60*60` for `active`; nøyaktig på fristen skjules data (`:321–325`; `ManagedArtistImportTypes.swift:114`). Publication-katalog, side/media og verk-/preview-stiene har vern (`PublicationCell.swift:1453–1457, 1476–1487, 1559–1600, 1608–1618`), og ArtistSales bruker `isPublic` på relevante publiserte lesinger (`ArtistSalesChannelCell.swift:668–691, 1164–1172, 1484–1501`). Sen claim er tillatt; fristen er ikke tokenutløp. `removed` kan ikke gjenåpnes med claim. Allerede nedlastede kopier kan ikke trekkes tilbake av dette API-et.

**4. AP2: samtykke og rettighetsbekreftelse.**

Importveien setter `portfolioOnly=true`, pris 0, tomme lisensvilkår og ingen lisenscredential (`ArtistSalesChannelCell.swift:839–865`). `publishWork` med importsamtykke setter `artistAttestedAt=nil`, `consent_unconfirmed` og `licenseOfferCredential=nil`, også om noen skulle sende true-attestasjoner under selve importfasen (`:976–986`). Dermed blir offentlig `rightsOwnershipAttested=false`, `attestation=consent`. `purchaseWork` nekter portfolio-only før lisens-/betalingsbehandling (`:1069–1078`). Claim endrer ikke portfolio-only til salg.

**Samtykkeobjektet blir ikke automatisk til en rettighetsbekreftelse eller salgslisens.** Rettsbekreftelsen kommer først fra claim/kunstnerhandling. Men F1 gjør at feil person kan levere denne handlingen og få false→true: skillet i datafeltene er riktig, mens person-/mottakerbindingen er utilstrekkelig. Jeg fant ingen sti som genererer salgslisens fra importsamtykket. Dette er kodevurdering av lisensutstedelse, ikke en juridisk vurdering av de faktiske rettighetene eller samtykkets bevisverdi.

**5. CI-status og hva som faktisk ble kontrollert.**

GitHub lest 28.09.2026. [Run 36359156197](https://github.com/Digipomps/CellScaffold/actions/runs/36359156197) er `completed / success`, knyttet til head `9209ce100446866c9869550ca53273665fde4304`. Start `2026-09-27T23:34:32Z`, sist oppdatert `2026-09-28T00:24:58Z` (02:24:58 norsk tid). Liste over kjøringer på denne committen returnerte denne ene kjøringen; ingen senere kjøring ble funnet ved kontrollen.

Jeg leste jobb-/stegstatus og filtrerte den faktiske [jobbloggen 108732726341](https://github.com/Digipomps/CellScaffold/actions/runs/36359156197/job/108732726341). Resultat:

| Kontroll | Observert resultat |
|---|---|
| Focused control-plane gates | success |
| Bygg alle mål, literals, testdekning og fokuserte Swift-gates | success |
| ManagedArtistImportTests | 23 tester, 0 feil; 23 pass-linjer i loggen |
| RuntimeIdentityRegistryTests | 21 tester, 0 feil |
| RuntimeIdentityProvisionerTests | 8 valgte tester, 0 feil; se F3 |
| RuntimeIdentityManifestTests | 15 tester, 0 feil |
| Gjentatte bridge-tester, shell/package-kontroll, tilgjengelighet/responsivitet | success |
| Thursday-demo og document live collaboration proof | success |
| Publish signed-source image pair | skipped; CI-resultatet er ikke bevis på publisert image/utrulling |

Workflowen er PR-CI. `actions/checkout` har ingen eksplisitt head-ref i `.github/workflows/admin-scaffold-image.yml:40–41`; derfor skiller jeg mellom kjøring tilknyttet head og en påstand om et separat, direkte head-bygg. Kildereviewet i denne rapporten bruker uansett den oppgitte SHA-en eksakt.

Det er ingen rød CI å feilattribuere for denne headen. De to røde lokale testene er beskrevet under F3 og finnes også i de oppgitte baseloggene. PR-en legger `ManagedArtistImportTests` til filteret ved `ci/test-filter.txt:468`; den legger ikke til exclusions eller skips. Hele eksisterende testsuiten er ikke dermed sertifisert grønn.

**6. Merge og AP6.**

Anbefalingen er **merge etter to rettinger: F1 og F2**, med relevante negative tester og ny grønn CI på korrigert head. Sentral strict-policy og eksisterende avvisningstester skal beholdes. Jeg har ikke gjort disse rettingene eller gitt merge-/deploy-autorisasjon.

Før faktisk import i produksjon må følgende være dokumentert:

1. Rettet mottakerbinding og lagringsvern fra F1/F2; avklart manifesttest-evidens fra F3 og gjenstarts-/ekstern-klientbevis fra F4.
2. Separat issuance-krypteringsnøkkel provisjonert til riktig prosess, med verifisert håndtering ved restart, tilgang, backup, tap og eventuell rotasjon. Kontroller fravær, feil lengde og feil nøkkel mot eksisterende lagring uten å eksponere hemmeligheten. Ingen fallback til bruker- eller sentralhvelvet.
3. Eier-signert runtime-manifest for faktisk ny profil, fortsatt strict, og bevist at sentralhvelvets bindingsinventar ikke utvides av importen.
4. Beskyttet, kanonisk rot på et filsystem med de nødvendige lås-/rename-/fsync-egenskapene. Én aktiv skriver per hvelv. Faktisk produksjonstopologi, UID/ACL, mount og hemmelighetsdistribusjon er **ikke lest/verifisert** her.
5. Samordnet backup/gjenoppretting av mandatforbruk, issuance-faser/tombstones, Publication, ArtistSales og tilhørende media. Et eldre komplett snapshot kan gjeninnføre tidligere tilstand; gjenoppretting må ikke stille gjenåpne brukt token eller fjernet innhold. Driftsnotatet `:32–34` beskriver deler av denne risikoen; en prøvd restore-prosedyre er fortsatt nødvendig.
6. Staging med testidentitet: import én gang, replay-/feil-requester-nekt, faktisk ekstern overtakelse, privatnøkkelgrense, avpublisering, direkte preview og 30-dagersgrense. Kjør fra den reelle klient-/transportveien. AP7-HTML/GUI er utenfor PR-en; dagens test-fixture erstatter ikke en brukbar overtakelsesvei.
7. Først deretter Kjetils uttrykkelige produksjonsmandat for navngitt kunstner, én bruk, 24 timer og korrekt samtykke. Bruk de godkjente seed-/bildekildene, behold manglende Batikk-preview som manglende, og kontroller `/pub` samt faktisk verk-side før/etter. Ingen slik produksjonshandling er utført i denne jobben.

**Lese- og verifikasjonsomfang.**

Lest: `handoff/AP2-7.md` (runde 3), `handoff/AP2-7-runde2-20260927.md`, `FORMAALSSPEC.md`, `PLAN.md`, PR-metadata og driftsnotatet på head. Kjetils krav 27.09 fra oppdraget går foran eldre tekst om «Sindres egen» serverforvaltede identitet. Hele de to nye produksjonsfilene og hele `ManagedArtistImportTests.swift` er lest. Hele PR-diffen er gjennomgått, med målrettet utvidet lesing av mandatvalidering/persistens, Publication/ArtistSales, strict-startup og testfilter. Relevante utdrag av pinnet CellProtocol er lest for strict, bridge-signering, challenge, setter-dispatch og snapshot/readback. Eksisterende skitne arbeidstrær er urørt.

Ikke lest: hele kodebasene, alle eksisterende testkropper, hele CI-loggen linje for linje, alle lokale evidenslogger i sin helhet, faktiske hemmeligheter, produksjons-/staginglagring, hele deployment-/backup-systemet, alle transport-/telemetriveier, levende kunstneridentitet eller klientens vault. Bilder/skjermbilder er ikke vurdert visuelt i denne sikkerhetsgjennomgangen. Ingen nye Swift-bygg, testkjøringer, manipulasjonsforsøk eller nettleserprøver er kjørt av Astra. Testresultater ovenfor er hentet fra CI og uttrykkelig navngitte eksisterende logger; nye funn er statisk kildevurdering med angitte forutsetninger.

Kravet «ingen hackbare svake ledd» kan ikke sertifiseres absolutt av en PR-gjennomgang. Denne rapporten identifiserer to konkrete grenser som bør rettes og skiller dem fra hva den leste koden og de eksisterende testene faktisk viser.
