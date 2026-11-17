# Chapter 36 — Agent Trust Package

Last verified against code: 2026-09-09

Status: WP1–WP10 er implementert i kandidatens lokale kode, med avgrensningene nedenfor. Dette er ikke en attest for deploy, Porthole-paritet eller full ende-til-ende-akseptanse.

`cell:///AgentTrustPackage` viser hva en eieravgrenset, lokal flåte faktisk har av annonserte Grants, verifiserbare Contracts og operative ceilings. Den viser modellrute og instruksjonsreferanse med digest når en lesbar kilde finnes. Pakken er **en projeksjon, aldri en kilde til rettigheter**. Formål, en korrekt pakke-digest og en gyldig godkjenning erstatter ikke målcellens tilgangskontroll.

Den maskinlesbare [v0-kontrakten](agent_trust_package_contract_v0.json) er en kopi av [PDD-kontrakten](../Deliverables/PDD_tillitspakke-agentflaate_2026-09-08/contract/agent_trust_package_contract_v0.json). `status` angir implementerte operasjoner og mangler; feltet `fixturesBasePath` angir hvor fixture-referansene skal løses fra, relativt til dokumentrepoets rot. Etter [lesson.planned-documented-as-implemented](haven_lessons_register_v0.json) bygger dette kapitlet på kode og de **siste** WP-sluttmeldingene i [TESTRESULT](../Deliverables/PDD_tillitspakke-agentflaate_2026-09-08/TESTRESULT.md), ikke på planens fremtidige oppførsel.

## 1. Kilder og rekkevidde

Cellen er registrert som `.identityUnique` og `.persistant`. Eieren velger inntil 64 forskjellige lokale celleendepunkter. Alle valgte celler må tilhøre requesteren. `fleet.set` og `regenerate` leser kildene gjennom den eksisterende resolver-/cellebanen; de installerer ikke Grants eller kjører flåtens effekter.

| Kilde | Implementert projeksjon og grense |
| --- | --- |
| Målcellens `agreementTemplate` | Eksakte keypaths og RWXS-flagg. En annonsert Grant er ikke alene bevis for requesterens tilgang. |
| Eieridentitetens EntityAnchor, `signedAgreementEntity` | Records og signerte lagringskvitteringer re-leses og kontrolleres med `AgreementProductionVerification.verifyEntityRecord`. Bare verifiserte, subject-bundne Contracts tas med. Manglende verifiserbar kilde gir tom Contract-liste og `verified=false` i raden; dette er ikke bevis for at ingen Contracts finnes. Den eksisterende verifierbanen er avgrenset til owner-snapshots. |
| PurposeBoundAIGateway, `ai.executionPolicy.ceiling` | Samme lagrede `CellExecutionPolicy` som invokasjonen bruker, med policy-, konfigurasjons- og taksonomidigester. |
| WebFetch, `webFetch.ceiling` | Faktiske hostmønstre, metoder og effektgrenser. Manglende ceiling vises som lukket; ugyldig kilde gir ingen avledet pakke. |
| Vanlig AIGateway, annonsert `state.draft` | Modellruten merkes som **utkast**. Base-URL og `state.draft.systemPrompt` bindes med separate digester; prompttekst og credential-alias kopieres ikke til pakken/state. |

PurposeBoundAIGateway har ingen lesbar gjeldende modellrute eller systeminstruksjon: disse følger invokasjonspayloaden. Pakken utelater derfor `modelRoute`/`instruction` der og viser fraværet. Det finnes heller ingen levert AIAssistantThread-/persona-kildebinding for denne projeksjonen. Vanlig/lokal gateway uten lesbar effekt-policy presenteres ikke som om den har en slik policy.

`AgentTrustReach` avleder kanter fra verifiserte, u-utløpte subject-bundne Contract-Grants og kjente, annonserte CellConfiguration-kall som består målcellens `validateAccess`. En referanse alene gir ingen kant. Grant-keypath må finnes eksakt i mål-templaten; en adresse uten mål må være entydig i flåten, eller bruke `cell:///Target#keypath`. Contract-flagg bevares som evidens, uten å bli gjort til runtime-autorisasjon.

For hver agent beregnes enkle stier på høyst fire kanter. RWXS summeres med snitt langs samme sti; separate stier beholdes. Over 4096 stier per agent avvises hele projeksjonen. Celler uten påvist sti får «Ingen vei. Ingen Grant.». `credentials=true` krever en påvist sti med r/x-Grant til `ScopedCredential.credentials` eller en eksakt annonsert under-keypath; flagget er forskjellig fra WebFetchs `allowCredentials`. Grafen dekker kjente deklarerte kall, ikke vilkårlige Swift-kall eller fremtidige modellhandlinger.

## 2. Keypaths og Grants

Alle operasjonene i tabellen har implementerte handlere og Explore-kontrakter. `r/w/x/s` betyr read/write/execute/storage; `s` i `rw-s` betyr **lagring**, ikke signering. Signeringen er en separat kontroll i godkjenningshandleren. Alle operasjoner krever eksakt keypath-tilgang. I tillegg er de eieravgrenset, unntatt `trustPackage.packageSchema`, som bruker vanlig tilgangskontroll for admitted requester. Det finnes ingen bred `trustPackage`-Grant.

| Metode | Keypath | Grant | Resultat eller payload |
| --- | --- | --- | --- |
| GET | `trustPackage.state` | `r---` | Labels, `fleet.cells[]`, `reach[]`, `adjust.*`, `hasChangesSinceApproval`, `deniedAttempts`, `audit.*`. |
| GET | `trustPackage.package` | `r---` | Kanonisk pakke-JSON som streng, eller `package_not_derived`. |
| GET | `trustPackage.packageSchema` | `r---` | JSON Schema for pakkemodellen. |
| GET | `trustPackage.approved` | `r---` | Re-verifisert record/receipt, digest, `approvedAt`, bevart `packageSnapshot`, policy-digester og eventuell `revokedAt`. |
| GET | `trustPackage.state.audit` | `r---` | Etterprøvingsstatus, avvik og kvitteringsrader. |
| GET | `trustPackage.audit.receipts` | `r---` | Originale kvitteringsmetadata indeksert med innholdsdigest. |
| GET | `configuration` / `configuration.audit` | `r---` | Henholdsvis før- og etter-konfigurasjonen. |
| SET | `trustPackage.fleet.set` | `rw--` | `{cellEndpoints: [...]}` velger flåte og regenererer. |
| SET | `trustPackage.regenerate` | `rw--` | `{}` leser kildene på nytt. |
| SET | `trustPackage.adjust.whitelist` | `rw--` | `{text: "ett mønster per linje"}`. |
| SET | `trustPackage.adjust.credentials` | `rw--` | `{isOn: false}`; `true` avvises i v0. |
| SET | `trustPackage.adjust.webfetchWrite` | `rw--` | `{isOn: false}`; `true` avvises i v0. |
| SET | `trustPackage.approve` | `rw-s` | `{packageDigest: "sha256:…"}`. |
| SET | `trustPackage.fleet.stop` | `rw--` | `{}` tilbakekaller aktiv godkjenning. |
| SET | `trustPackage.open.instruction` | `r---` | `{cellID: "…"}` → navigasjonsreferanse, hvis kilden finnes. |
| SET | `trustPackage.open.receipt` | `r---` | `{receiptID: "…"}` → referanse til arkivets originalkvittering. |
| SET | `trustPackage.open.package` | `r---` | `{}` → `cell:///AgentTrustPackage#configuration`. |

Underfelt i state/audit og enkeltkvitteringer leses gjennom den autoriserte rotoperasjonen. `open.*` returnerer bare `{status: "navigate", endpoint, keypath}`, aldri målinnhold. Ukjent/tvetydig receipt-ID avvises; manglende instruksjon gir `instruction_reference_missing`. SET med `r---` er den implementerte navigasjonskontrakten, ikke en feilaktig skrive-Grant.

Målcellene har også følgende implementerte operasjoner, med eierkontroll på administrasjon og kvitteringslesing:

| Celle | GET (`r---`) | SET (`rw--`) |
| --- | --- | --- |
| WebFetch | `webFetch.ceiling`, `webFetch.fleetBinding`, `webFetch.receipts` | `webFetch.ceiling.set`, `webFetch.fleetBinding` |
| PurposeBoundAIGateway | `ai.executionPolicy.ceiling`, `ai.fleetBinding`, `ai.receipts` | `ai.executionPolicy.ceiling.set`, `ai.fleetBinding` |

`webFetch.ceiling`-GET bruker ordinær `r---`-tilgang og kan også leses av en admitted requester med den retten; eierkravet gjelder ceiling-SET. Gatewayens ceiling-GET krever i tillegg eierskap.

## 3. Pakke-digest og kanonisk koding

`AgentTrustPackage` bruker schema `haven.agent-trust-package.v0`. `AgentTrustPackageCanonicalEncoder` koder sorterte objektnøkler, uten strukturell whitespace eller slash-escaping; array-rekkefølgen bevares. Manglende valgfrie cellefelt utelates. `generatedAt` og Contract-`expiresAt` normaliseres til RFC3339 UTC med bevarte brøkdelssekunder uten avsluttende nuller. Ugyldige datoer, ukjent offset `-00:00` og ukjent pakkeschema avvises ved koding.

La `B` være disse kanoniske UTF-8-bytene etter at **bare toppnivåets `packageDigest`** er fjernet. Den implementerte domeneseparasjonen er:

```text
packageDigest = "sha256:" + hexLower(SHA256(
  UTF8("haven.agent-trust-package.v0") || 0x00 || UInt64BE(B.count) || B
))
```

Også `generatedAt`, `edges` og `reach` inngår. Cellen beholder samme genereringsepoke gjennom regenerering/reload, slik at uendrede kilder gir samme digest. En endret projisert Grant eller ceiling gir ny digest. Modellens eldre fixtureform `"see fleet-webfetch.reach.json"` bevares ved round-trip, men binder bare referanseteksten; runtime produserer listeformen.

Den rekursive kodingsvakten avviser feltnavn med `key`, `secret`, `token`, `password` eller `prompt`, med unntak for `keypath`, samt nøkkellignende verdier. Den er konservativ mønstergjenkjenning, ikke et bevis for at vilkårlig tekst er hemmelighetsfri. Pakken har ingen prompttekstfelt. Et innlagt `package`-felt i cellens lagrede snapshot settes i karantene: «Ikke avledet», `approve → package_not_derived`. Råpakken beholdes ikke; bare vellykket eksplisitt eierregenerering/flåtevalg fjerner markøren.

## 4. Justering som bare innsnevrer

De tre `adjust.*`-handlingene krever eierens signeringsbevis og skriver data til målcellens ceiling, aldri til `agreementTemplate` eller en ny Contract. Hele flåten og alle mønstre valideres før første skriving. Vanlig avslag, blant annet `expansion_not_allowed` eller `invalid_pattern`, beholder ceiling og pakke-digest.

Whitelist trimmes per linje, normaliseres til små bokstaver og dedupliseres. Tom tekst eller blanke linjer avvises. **Førstegangsregelen:** en første ikke-tom liste ved manglende/aldri-initialisert tom WebFetch-ceiling kan settes innenfor templatens HTTPS-tak. Dette åpner den tidligere deny-all-listen innenfor eksisterende myndighet. Deretter må hvert mønster være en host-/port-delmengde av gjeldende liste. Et historikkflagg i WebFetch-snapshotet hindrer at tømming, reload eller en ny pakkecelle gjenåpner førstegangsregelen. Direkte eieradministrasjon via `webFetch.ceiling.set` er en separat operasjon; monotoni gjelder pakkens justeringsbane.

`credentials:true` og `webfetchWrite:true` avvises alltid i WebFetch v0. `false` beholder henholdsvis `allowCredentials=false` og `methods=[GET]`. En ScopedCredential-celle i flåten eller et `w`-flagg på fetch gir ingen HTTP POST- eller credential-rett. PurposeBoundAIGateways lagrede policy kan bare innsnevres mot både gjeldende policy og templatens maksimum; øvrige authority-/purpose-/provenance-felt kan ikke endres.

Godtatt endring re-leses og regenererer pakken. Identiske verdier beholder digest. En innsnevret AI-policy bindes i pakken med digest over hele den effektive policyen. Skriving til flere celler er ingen distribuert transaksjon: teknisk feil etter påbegynt skriving trekker projeksjonen tilbake til «Ikke avledet». `deniedAttempts` teller eieravviste `adjust.*`-kall uten rå forslag eller hemmeligheter; den er ikke en signert effektjournal.

## 5. Eiergodkjenning og flåteport

`approve` regenererer kildene, sammenligner den innsendte digesten og lager et kanonisk snapshot med `{schema, fleetID, packageDigest, approvedAt, policyDigests}`. Hele snapshotet ligger i `Agreement.name`, inne i bytes signert av `Contract.ownerSignedSnapshot`. Agreement har **ingen Grants og ingen conditions**; issuer og subject er eieren. Dette er eier-/issuer-signering, ikke flerpartssignering.

`signedAgreementEntity.commit` må returnere `persisted`, og både record og signert lagringskvittering må verifiseres. Kildene kontrolleres igjen etter commit før godkjenningen aktiveres. `trustPackage.approved` re-verifiserer signaturene ved GET; et lagret `signatureValid=true` er ikke bevis. Den egne godkjenningsrecorden utelates fra Contract-projeksjonen for å unngå at den endrer sin egen pakke-digest.

`policyDigests` binder celleinstansens UUID, type, eiernøkkel-fingerprint, eksakte template-keypaths med begge permission-gruppene og hele den operative policyen. Dermed bindes også WebFetchs `maxBytes` og `followRedirects`, selv om den kompakte pakkeprojeksjonen ikke har disse feltene. Bare endret bytegrense kan derfor stenge porten uten at `packageDigest` endres.

Flåtevalg/godkjenning oppretter ikke automatisk bindinger. Eieren setter separat `webFetch.fleetBinding` eller `ai.fleetBinding` til `{fleetID: "pakkecellens UUID", endpoint: "cell:///AgentTrustPackage"}`. `null` fjerner bindingen bevisst. Ugyldig lagret binding feiler dekoding; feilet persistent unbind rulles tilbake.

På **bundne** `WebFetch.web.fetch` og `PurposeBoundAIGateway.ai.invokePurposeBound` leser porten godkjenningen med målcellens verifiserte runtime-eier. Den kontrollerer flåte/eier/instans, signatur, gjeldende pakke og fulle policy-digester før credential-, cache- og nettverksbanen. Den feiler lukket med `package_not_approved`, `package_digest_mismatch`, `package_unavailable` eller `package_approval_invalid`. Requesteren trenger fortsatt sin ordinære tilgang. Ubundne celler følger eksisterende autorisasjon og ceiling; øvrige celletyper får ingen slik port av å stå i pakken.

`fleet.stop` beholder recorden og setter `revokedAt`; ny godkjenning beholder eldre records i historikken. Stopp nekter nye opptak, men avbryter ikke allerede innslupne effekter. Ceiling, bindinger og cellehistorikk bruker eksisterende Codable/resolver-snapshots; approval-recorden bruker EntityAnchor-commit. Lagringsfeil gir ikke en garanti om varig godkjenning eller tilbakekalling.

## 6. WebFetch-ceiling og matcheregler

`WebFetchCeiling` (`haven.webfetch-ceiling.v0`) lagres per instans. Gyldig v0 krever HTTPS, nøyaktig `[GET]`, ingen body, `allowCredentials=false`, `followRedirects=false` og `maxBytes` mellom 1 og 256000. Manglende/ugyldig ceiling og tom hostliste nekter fetch. Request-felter kan ikke overstyre taket.

| Mønster | Matcher | Matcher ikke |
| --- | --- | --- |
| `example.org` | Bare `example.org`, standardport 443 | `a.example.org` eller port 8443 |
| `*.example.org` | `a.example.org` og dypere subdomener, port 443 | Selve `example.org`, `evil-example.org` eller `example.org.evil` |
| `example.org:8443` | Bare eksakt vert og port 8443 | Samme vert på 443 |

Host sammenlignes uten forskjell på store/små bokstaver. Eksplisitt port må være 1–65535; uten port brukes 443. Parseren godtar ASCII-hostetiketter, med wildcard bare som innledende `*.`. Scheme, path, query, userinfo, tomme etiketter og vilkårlige glob-uttrykk er ikke hostmønstre.

Credential-alias, URL-userinfo eller header-payload avvises med `credential_not_granted` før noe credential-oppslag eller nettverkskall. v0 kan ikke åpne credentials, heller ikke for eieren. Sessionen har ingen cookie-, credential- eller URL-cache. Forhåndsavslag skjer uten nettverk; redirect-avslag krever at første respons er mottatt.

Alle automatiske redirects stoppes. Ved 3xx kontrolleres `Location` med samme ceiling: utenfor listen, ugyldig eller manglende mål gir `redirect_outside_whitelist`. Tillatt mål gir `redirect_not_followed`. Ingen av tilfellene starter en ny request. Buffermottaket begrenses og kanselleres ved bytegrensen; en allerede mottatt chunk kan være større. Responsens beholdte `byteCount` er derfor forskjellig fra kvitteringens samlede mottatte `bytes`.

## 7. Signerte kvitteringer

`ActionDecisionReceipt` og `EffectReceipt` bruker `signed(by:)` og `verify(against:)`, med `ReceiptSignature {signerRef, algorithm, value, signedAt}`. Eksisterende Identity-API signerer kompakt, sortert JSON uten signaturfeltet. P256-ECDSA-SHA256 og Ed25519 støttes. Verifisering bruker forventet, fastlagt offentlig identitet, ikke en identitet valgt fra kvitteringens påstand. Legacy uten signatur dekodes som `unsigned`; audit viser «usignert/ugyldig». `signedAt` må være lik kanonisk `createdAt` og er utstederens oppgitte tid, ikke et uavhengig tidsstempel.

WebFetch utsteder én `EffectReceipt` per håndtert kall når eierens signering er tilgjengelig, også ved avslag, redirect og transportfeil. Den inneholder bare vert, metode, mottatte bytes, `credentialsUsed`, beslutning/utførelse, årsakskode og tilgjengelige ceiling-/pakkedigester. Den binder admission-snapshotet også hvis ceiling endres under overføringen. `credentialsUsed=false` følger v0-forbudet. Pakke-digest utelates hvis ingen godkjenning kan verifiseres. Ingen sti/query, port, redirect-mål, alias, headers eller response-body lagres i kvitteringen; dette utsagnet gjelder ikke WebFetchs separate innholdsresultat.

PurposeBoundAIGateway signerer beslutningskvitteringen etter endelig execution-status, også ved cache-treff og tidlige avslag med observerbare bindings. Helt udekodbar input eller manglende intent kan gi eksisterende feilretur uten kvittering. `ai.receipts` gjelder PurposeBoundAIGateway; vanlig AIGateway/LocalLLMGateway er ikke tilsvarende kvitteringskilder for flåteaudit.

`webFetch.receipts` og `ai.receipts` er append-only via celle-API-et, med eierbeskyttet GET og uten SET/reset/trim. `web.clear` sletter ikke kvitteringene. Manglende signering feiler eksplisitt; persistensfeil rapporteres separat og beholder kvitteringen i minnet. Snapshot/reload er testet, men dette er ingen slettesikker eller kryptografisk kjedet journal.

## 8. Etterprøvingsdiff

Audit bruker bevart `packageSnapshot`, hvis digest må stemme med den signerte godkjenningen. Senere justering, tomt flåtevalg og stopp erstatter ikke dette sammenligningsgrunnlaget. En eldre WP7-godkjenning uten snapshot kan bare suppleres fra gjeldende kilder når de fortsatt gir den samme signerte digesten.

Ved GET samles kvitteringer fra det **godkjente** flåteutvalgets WebFetch/PurposeBoundAIGateway siden `approvedAt`. Signatur, eier og kildeinstans kontrolleres. Flåtearkivet bevarer originalmetadata under innholdsdigest; gjentatt GET dedupliserer. Endret innhold med samme receipt-ID bevarer begge versjoner og markerer avvik. Ugyldig signatur kan ikke skjules ved å flytte tidspunktet før godkjenning.

| `ViolationKind` | Implementert evidens |
| --- | --- |
| `new_destination` | Host utenfor godkjent liste eller signert årsakskode for destinasjon/scheme/redirect-avslag. Redirect-mål rekonstrueres ikke. |
| `credential_resolved` | `credentialsUsed` utenfor ceiling eller `credential_not_granted`; sistnevnte er et nektet forsøk, ikke bevis for oppløst credential. |
| `data_class_outside` | Signert dataklasseavslag eller datamanifest-digest utenfor de støttede AI-manifestene i godkjent ceiling. |
| `provider_tools_on` | Avvik fra gatewayens kjente `no-tools`-plan-digest eller `plan_not_allowed`; ikke uavhengig observasjon av leverandørens interne verktøy. |
| `unknown_policy_version` | Ugyldig/usignert kvittering, ukjent kilde, binding-/policyavvik, uavklart kontroll eller kolliderende receipt-ID. |

`trustPackage.state.audit` har `statusLabel`, `summaryLabel`, `approvedDigestLabel`, `violationsLabel`, `violations[]` og `receipts[]`. Både nektede forsøk og registrerte effekter kan gi avvik; én effekt kan ha flere avvik. «Innenfor» teller effekter uten påviste avvik. Manglende godkjenning, snapshot, kilde eller vellykket arkivlagring gir ufullstendig status, aldri «Overholdt».

AI-kvittering v1 inneholder digester og signerte kontrollresultater, ingen lesbar route/destinasjon eller verktøyliste. Audit rekonstruerer ikke AI-kallet. Innsnevret effektiv policy kan avvike fra receiptens template-digest og vises konservativt som `unknown_policy_version`. WebFetch-kvitteringen identifiserer kildecellen, ikke caller-agenten. Innhold fjernet fra kilden før første innsamling kan ikke oppdages av dette arkivet.

WP10s signerte, syntetiske fixture gir 7 effekter, 5 innenfor og 2 avvik. Det er testdata, ikke en kjørt flåtes hendelsesrapport. WP4 verifiserer at produksjonens provider-bodyer utelater verktøyfelter, og at body-endringer endrer hash; receiptens normaliserte request-digest er ikke en hash av HTTP-bytene. Ingen av disse kontrollene beviser leverandørens interne oppførsel. WP10 observerte dessuten et eksisterende Anthropic-avslag fordi core-autorisatoren velger første ceiling før destinasjon kontrolleres; feilen er ikke rettet, og positiv produksjonskontroll brukte OpenAI.

## 9. Ikke implementert

- **Porthole-paritet:** ikke levert/verifisert i dette dokumentasjonsgrunnlaget. Før-/etter-skeleton og referansesvar finnes, men visuell paritet, faktisk navigasjon i Porthole/Binding, payload-substitusjon og lastetid er ikke dokumentert som fungerende.
- **Per-Grant V2:** ikke implementert; dagens eieravgrensede v0-ceilings og grafprojeksjon er ikke en per-Grant V2-autorisasjonsmodell.
- **Flerpartssignering:** ikke implementert; godkjenningen er ett eier-/issuer-signert snapshot.
- **Distribuert revokasjon:** ikke implementert; lokal `fleet.stop` gir verken distribuert konsensus eller kansellering av innslupne effekter.
- **Lesbar gjeldende modellrute/instruksjon for PurposeBoundAIGateway og AIAssistantThread-/persona-projeksjon:** ikke implementert. Det lesbare AIGateway-utkastet fyller ikke denne mangelen.
- **Full rekonstruksjon av AI-effekter og slettesikker journal:** ikke implementert. Full vertsomstart med varig disk-I/O er heller ikke verifisert av snapshot-testene.

WP11-paritet og WP13 ende-til-ende-/sluttakseptanse inngår ikke i WP12. Siste WP10-helkjøring har samme 46 røde CellScaffold-testnavn som baseline; den er ikke grønn full regresjon. Direkte XCTest-resultatene dekker ikke Swift Testing.

## 10. Kodeankere

- Pakkemodell/koding: [AgentTrustPackage.swift](../../CellProtocol/Sources/CellBase/Agreement/AgentTrustPackage.swift), [PurposeBindingDigest og ActionDecisionReceipt](../../CellProtocol/Sources/CellBase/Agreement/PurposeBoundExternalAction.swift).
- Celle, kontrakt og graf: [AgentTrustPackageCell.swift](../../CellScaffold/Sources/App/Cells/AgentTrustPackage/AgentTrustPackageCell.swift), [AgentTrustPackageContract.swift](../../CellScaffold/Sources/App/Cells/AgentTrustPackage/AgentTrustPackageContract.swift), [AgentTrustReach.swift](../../CellScaffold/Sources/App/Cells/AgentTrustPackage/AgentTrustReach.swift).
- Justering/port: [AgentTrustPackageAdjustment.swift](../../CellScaffold/Sources/App/Cells/AgentTrustPackage/AgentTrustPackageAdjustment.swift), [AgentTrustPackageApproval.swift](../../CellScaffold/Sources/App/Cells/AgentTrustPackage/AgentTrustPackageApproval.swift), [WebKnowledgeCells.swift](../../CellScaffold/Sources/App/Cells/WebKnowledge/WebKnowledgeCells.swift), [AIGatewayCell.swift](../../CellScaffold/Sources/App/Cells/AI/AIGatewayCell.swift).
- Kvitteringer/audit: [ReceiptSignature.swift](../../CellProtocol/Sources/CellBase/Agreement/ReceiptSignature.swift), [EffectReceipt.swift](../../CellProtocol/Sources/CellBase/Agreement/EffectReceipt.swift), [SignedCellReceiptStore.swift](../../CellScaffold/Sources/App/Cells/SignedCellReceiptStore.swift), [AgentTrustPackageAudit.swift](../../CellScaffold/Sources/App/Cells/AgentTrustPackage/AgentTrustPackageAudit.swift).
- Flatekonfigurasjoner: [AgentTrustPackageConfigurationFactory.swift](../../CellScaffold/Sources/App/Cells/AgentTrustPackage/AgentTrustPackageConfigurationFactory.swift). Capture av kandidat-formål følger [kapittel 23 §8](23_Purpose_Knowledge_Base.md#8-new-purpose-capture); denne leveransen promoterer ingen taksonominoder.
