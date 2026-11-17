# Bolk 1 — oppdrag til Codex: prøve av innslipp med en avtale signert utenfor cellens prosess

PDD `kryptert-korrespondanse-med-vedlegg-ut`, 07.10.2026. Skrevet av korrespondanse-tråden (Claude-tråden i prosjektet «HavenAgentD»).

**Status: GODKJENT 07.10.2026.** Kjetil, ordrett: «A ja, B ja, C ja Vegar har en m2 og victoria en intel». Spørsmål C var: «Kan Codex starte første ledd nå, før planen er godkjent? Det er en liten prøve, lokalt: en avtale signert på én maskin slipper inn et medlem i en celle som kjører på en annen. Bestillingen sier at ingenting skal til hovedgrenen.» Ordet hans står også i `STATUS.md` i oppgavemappen. Godkjenningen gjelder denne prøven og ingenting annet.

Oppgavemappen: `CellProtocolDocuments/Deliverables/PDD_kryptert-korrespondanse-med-vedlegg-ut_2026-10-06/`. Alle stier er fra HAVEN-mappen.

## Hva prøven er til

Kjetil eier relasjonscellene for korrespondanse og er selv part i dem. Cellene skal kjøre på staging, og nøklene hans skal ligge på Macen hans. Staging skal ikke ha noen nøkkel som kan slippe inn et medlem. Godkjent 07.10 (G1): `FORMAALSSPEC.md`, formålene A3, C2 og D3.

Prøven skal vise, med kjørende kode og rå utdata, om et medlem kan slippes inn i en celle når cellens prosess ikke har eierens private nøkkel, på grunnlag av noe eieren har signert et annet sted. Og hva som i så fall må endres i CellProtocol. Holder det ikke, går saken tilbake til Kjetil før noe annet bygges.

Dette er en prøve, ikke en leveranse. Den skal være liten.

## Det som er lest i koden

Lest av korrespondanse-tråden 07.10 på en kopi av CellProtocol-grenen med koden for vedlegg (`9420e7d`, som bygger på `81601a6`). En lesende jobb 06.10 viste at `GeneralCell.swift` var uendret fra `81601a6` til `origin/main` (`1ec56d5`). Målt 07.10 kl. 14:35Z (`HAVEN-Deploy/_handoff/KORR-UT/maal/G2-GRUNNLAG-20261007.md`): `origin/main` var da `1ec56d5`, med PR #53 (broen) inne. Kl. 15:04Z meldte kø-trådens jobb `c31` at PR #60 og #61 er merget, at `origin/main` er `68069b697a22246ffb4d8add5ecc42e3d0d5ba38`, og at den er tagget `2026.9.5` (`_losen-queue/done/c31-cp-merge-tag-2026.9.5.svar.md`). Etter kø-trådens innlegg i `_losen-queue/KOORDINERING.md` om PR #60 lar den `ensureRuntimeReady()` kaste når et oppsett er avslått, og `addAgreement` kaller `ensureRuntimeReady()` først. Kø-trådens jobb `a35` endrer samtidig rekkefølgen for avvisning i `get` og `set` i samme fil, på en egen gren. Det som står under, er altså lest på en eldre revisjon enn den du skal bygge på. Funksjonsnavnene er det som gjelder, ikke linjenumre. Les selv på `origin/main` før du bygger på noe av dette, og si fra i rapporten hvis noe ikke stemmer.

- `Sources/CellBase/Cells/GeneralCell/GeneralCell.swift`, `addAgreement(_:for:authorizedBy:)`: krever at den som ber, beviser nøkkelen sin (`checkIdentityOrigin`), utleder avtalen av cellens mal (`agreementDerivedFromTemplate`), spør `admissionPolicyAllows`, og signerer så med `Contract.signed(agreement:issuer:subject:domain:issuedAt:)`, der utstederen er identiteten `contractSigningOwner(preferredOwner:)` gir. Kontrakten installeres med `auditor.installAuthorization(contract:member:restoring:)`.
- Samme fil, `contractSigningOwner(preferredOwner:)`: gir en eieridentitet bare når eierens nøkkel kan bevises med `checkIdentityOrigin(owner, against: owner)`, eller for en eier hentet fra et nøkkellager cellen når (`locallyRestoredOwner`). Om det nøkkellageret kan ligge et annet sted enn i cellens prosess, er ikke lest.
- Samme fil, `admissionPolicyAllows`: med policyen `.ownerApprovalRequired` slipper bare et kall der eieren er autorisert, gjennom. Den policyen er standarden når en celle opprettes.
- Samme fil, `authorizationContracts(for:)`: ved hver tilgang kontrolleres de lagrede kontraktene med `verifyAuthorizationBinding(expectedIssuer: owner, expectedSubject:expectedDomain:now:)`, rettigheter og varighet holdes mot malen, og `checkIdentityOrigin(identity, against: currentContract.subject)` kreves.
- Samme fil, `checkIdentityOrigin(_:against:)`: henter en tilfeldig verdi fra identitetens eget nøkkellager (`identity.identityVault`), bygger en utfordring av den (`IdentitySigningChallenge.signingData`), lar identiteten signere utfordringen (`identity.sign`), og kontrollerer signaturen mot den offentlige nøkkelen til identiteten det sammenlignes med.
- `Sources/CellBase/Cells/Correspondence/CorrespondenceCell.swift`, `establishInitialMembership`: cellens eier legges alltid i medlemslista (lest 06.10).
- `Sources/CellBase/Agreement/Contract.swift`: formatet heter `issuer_only_subject_bound_v1`. `SigningPayload` har feltene `uuid`, `agreement`, `issuerUUID`, `issuerSigningKeyFingerprint`, `subjectUUID`, `subjectSigningKeyFingerprint`, `domain`, `issuedAt` og `expiresAt`. `verifyCryptographicSignature()` bruker utstederens offentlige nøkkel.

## Det prøven skal svare på

Hvert svar er en test med rå utdata. Et resonnement uten test teller ikke som svar. Kan noe ikke vises i en test, står det under «Ikke vist» med grunnen.

1. **Kan det gjøres?** Oppsett: kontekst B huser en celle og har bare eierens offentlige identitet, ikke nøkkellageret hans. Kontekst A har eierens nøkkellager. Et subjekt S skal bli medlem på grunnlag av noe A har signert, uten at B noen gang har eierens private nøkkel. Hvordan det signerte når cellen, og hvem som legger det fram, er en del av svaret. Etterpå skal en handling S har rett til etter malen, lykkes, og en handling utenfor malen bli avvist. Bruk adskilte nøkkellagre i testen, slik at B beviselig ikke kan signere som eieren.
2. **Hva må endres, om noe?** Den minste endringen i CellProtocol som gjør punkt 1 mulig. Oppgi filer, funksjoner og linjetall for endringen.
3. **Hva skal fortsatt avvises?** Én test per tilfelle, rød før endringen der det gir mening, grønn etter:
   - a) noe signert med en annen nøkkel enn eierens;
   - b) noe eieren har signert for en **annen celle** han eier, med samme mal og samme domene, lagt fram for denne cellen. Si i rapporten hva som binder det signerte til én celle, eller at ingenting gjør det;
   - c) noe som er utløpt, og noe som ikke gjelder ennå;
   - d) et subjekt som ikke kan bevise nøkkelen sin;
   - e) noe som gir mer enn malen: en rettighet utenfor malen, og en varighet over malens;
   - f) en tredje identitet prøver å få tilgang med noe som er signert for subjektet S;
   - g) det samme lagt fram to ganger: medlemslista og kontraktlista skal ikke vokse;
   - h) kontekst B prøver selv å slippe inn S med `addAgreement`, uten eierens nøkkel: skal avvises som i dag.
4. **Subjektets bevis over en forbindelse.** `checkIdentityOrigin` går gjennom `identity.identityVault`. Når S sitter i en annen prosess enn cellen: hva gir cellen et slikt bevis i dag, og mangler noe? Les og oppgi fil og funksjon. Vis det i en test hvis det lar seg gjøre uten ny ruting. Ellers står det under «Ikke vist».
5. **Tilbakekall.** Ikke bygg noe. Oppgi bare hva som finnes for å fjerne et medlem og en kontrakt, og hvem som kan kalle det.
6. **Eierens to bruk av nøkler.** Eieren skal gjøre to ting: slippe inn medlemmer, som skal kreve Touch ID eller passord hver gang, og lese og sende gjennom agenten sin, som ikke skal det. Hver handling i cellen krever at identiteten signerer en utfordring (`checkIdentityOrigin`). Les og oppgi hva koden krever og avviser når identiteten som signerer for innslipp (cellens eier), og identiteten eieren leser og sender med, er (a) samme identitet og (b) to ulike identiteter, der den andre er sluppet inn av den første. Vis hvert tilfelle i en test hvis det er lite arbeid. Ellers står det under «Ikke vist». Ikke anbefal det ene framfor det andre.

## Rammer

- Gren: `codex/korr-innslipp-proeve-20261007`, laget fra `origin/main` i CellProtocol (`68069b6`, taggen `2026.9.5`), i et eget arbeidstre. Hovedutsjekken røres ikke.
- **Ingenting til `main`.** Ingen PR, ingen merge, ingen tag. Commit på grenen, lokalt. Grenen skyves ikke. Legg forskjellen mot `origin/main` som fil i oppgavemappen, `handoff/BOLK-1-ENDRING.patch`, slik at arbeidet finnes mer enn ett sted.
- Bare CellProtocol. Ingen endring i kildekoden i HavenAgentD, CellScaffold eller Binding. Ingen staging, ingen ekte nøkler, ingen nettverk i testene.
- Policyen `.ownerApprovalRequired` endres ikke. `CellBase.debugValidateAccessForEverything` skal være av i testene, og testene skal feile hvis den er på.
- Ingen eksisterende test fjernes eller svekkes. Kjør hele testmengden for pakken etterpå og oppgi tallene.
- Nye tester legges i én ny fil under `Tests/CellBaseTests/`. Testnavnene sier hva som avvises.
- Skriv ingen nøkler, ingen UUID-er fra ekte identiteter og ingen tokener i rapporten.
- Kom ikke med anbefaling om arkitektur ut over det prøven viser. Det avgjør Kjetil.

## Leveranse

Én rapport: `CellProtocolDocuments/Deliverables/PDD_kryptert-korrespondanse-med-vedlegg-ut_2026-10-06/handoff/BOLK-1-RAPPORT.md`, med:

1. Commit og gren, og `origin/main` den ble laget fra.
2. Endrede filer, med `git diff --stat` mot `origin/main`, og at `handoff/BOLK-1-ENDRING.patch` er skrevet.
3. For hvert av punktene 1–6 over: testnavn, og rå utdata fra kjøringen (rødt før, grønt etter, der det gjelder). Utdata limes inn uendret.
4. Hele testmengden: kommandoen, antall tester og antall feil. På macOS avslutter `swift test` med tomme omslagslinjer; tell linjene «Test Case … passed/failed».
5. «Ikke vist»: det prøven ikke kunne vise, og hvorfor.
6. «Avvik fra det som er lest»: det i avsnittet «Det som er lest i koden» som ikke stemte på `origin/main`.

Rapporten gjennomgås av korrespondanse-tråden og av en uavhengig leser før noe sies til Kjetil.
