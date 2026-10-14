**Dom: Holder etter rettelsene under.** Den nye veien gir ingen utenforstående tilgang. Men et medlem som er fjernet, kan slippe inn igjen med den samme kontrakten. Det må stå i rapporten, og det blokkerer bolk 2 til det er løst.

Leser: Claude Opus (Fabel er uten kvote til 08.10 kl. 10:00Z), bestilt av korrespondanse-tråden.

Uavhengig kodelesing 07.10.2026 av en kopi i skyen, som er grunnlaget `68069b6` med `BOLK-1-ENDRING.patch` lagt på. bare `Contract.swift` og `GeneralCell.swift` er endret under `Sources`. Swift er ikke kjørt her. Alle stier under er relative til CellProtocol.

## MÅ

1. **Den nye veien undergraver tilbakekall.** Rapporten må si det, og bolk 2 må løse det før veien tas i bruk.
   - `removeMember(member:requester:)` og `removeMember(uuid:requester:)` (`GeneralCell.swift:2015-2041`) sletter medlemmet og kontraktene gjennom `GeneralAuditor.removeAuthorization` (`GeneralAuditor.swift:465-474`).
   - Ingenting husker hva som er fjernet. Det finnes ingen sperreliste og ingen «gyldig fra»-tid per subjekt. `acceptExternallySignedAgreement` (`GeneralCell.swift:1455-1505`) godtar derfor den samme kontrakten fra S på nytt, helt til den utløper. Det kan være opptil malens varighet, og høyst `Contract.maximumDuration`, ett år (`Contract.swift:23`).
   - På den gamle veien krevde hvert nytt innslipp eierens nøkkelbevis der og da (`GeneralCell.swift:1380-1406`). Der varte et tilbakekall.
   - Det finnes også et kappløp over `await`. Et `removeMember` kan gå ferdig mens `acceptExternallySignedAgreement` venter på `checkIdentityOrigin` eller på vilkårene (`GeneralCell.swift:1470-1494`). Deretter installerer `installAuthorization` (`GeneralCell.swift:1498-1503`) kontrakten likevel, og revisjonen øker, så fjerningen er tapt.
   - Rapportens punkt 5, avsnitt 6, linje «De fjerner medlemmet og alle autorisasjonskontrakter …», er riktig om koden, men gir et for sterkt inntrykk når den nye veien finnes. Setningen må få dette forbeholdet.
   - Bolk 2 trenger et varig, lagret tilbakekall som kontrolleres både i `acceptExternallySignedAgreement` og i `authorizationContracts(for:)`. Det kan være en liste over tilbakekalte `Contract.uuid` eller en «ikke før»-tid per subjekt, satt av eieren.

## BØR

1. **Hendelser ved avvisning.** Den nye veien registrerer ingen `recordContractRejected`-hendelser (`GeneralCell.swift:1462-1494`). Den gamle veien gjør det (`GeneralCell.swift:1363-1405`). Uten dem ser ingen forsøk med fremmede kontrakter på staging. Legg til grunnkoder for hver `guard`.
2. **Kodekommentaren lover for mye.** Kommentaren «Freeze all mutable Agreement/Identity references» (`GeneralCell.swift:1460`) gjelder ikke `identity`-parameteren, som fortsatt kan endres. Det gir ingen tilgang, fordi beviset kontrolleres mot den frosne `contract.subject` (`:1478`) og medlemmet hentes fra `contract.subject` (`:1500`). Men vilkårene (`:1488-1490`) evalueres mot den ufrosne `identity`. Kommentaren og rapportens «fryser … før await» bør presiseres.
3. **Ingen domeneseparasjon i signaturen.** Formatnavnet `issuer_only_subject_cell_bound_v2` utledes av feltene, men signeres ikke (`Contract.swift:38-40, 221-235`). Eierens nøkkel signerer også mange andre JSON-nyttelaster (mer enn 20 `sign(data:)`-steder under `Sources/`). Nå som hvem som helst kan legge fram en kontrakt, bør v2-nyttelasten få et signert felt for formål eller format. Jeg fant ingen konkret forveksling.
4. **Bindingen er bare så sterk som cellens UUID.** `uuid` er `public var` (`GeneralCell.swift:380`). Bindingen holder bare hvis UUID-en er unik og stabil, også etter gjenoppretting, kloning og reserve­kopi. Standarddomenet `"private"` (`:393`) er felles for mange celler. Bolk 2 bør si hvem som fastsetter UUID-en til relasjonscellene.
5. **`.signed` er misvisende som returverdi** (`GeneralCell.swift:1504`). Verten har ikke signert noe. Vurder en egen tilstand eller en egen hendelse.
6. **Testene, se svar 4:** kontroller hvilken feil som kastes ved avvisning, legg til en positiv kontroll for skriving, legg til en test der bindingen fjernes, og test filteret i den gamle veien.

## Svar på spørsmålene

**1. Kan den nye veien gi tilgang den ikke skal?** Nei, ikke ut over MÅ 1. Kontrollene ligger på disse stedene:

| Kontroll | Hvor |
|---|---|
| Utstederen er eieren, med nøkkelens fingeravtrykk | `verifyAuthorizationBinding(expectedIssuer: owner …)`, `GeneralCell.swift:1471`. `identitiesReferenceSame` krever lik UUID og likt fingeravtrykk (`Contract.swift:248-255`). Fingeravtrykket regnes ut av selve nøkkelen (`IdentitySigningChallenge.swift:218-230`), og signaturen kontrolleres mot den samme nøkkelen (`IdentityPublicKeySignatureVerifier.swift:14-38`). Det samme gjelder `agreement.owner` og underskriverne (`Contract.swift:209-218`). |
| `targetCellUUID` er denne cellen og er signert | `GeneralCell.swift:1470` krever eksakt likhet, så `nil` avvises. Feltet er med i `SigningPayload` (`Contract.swift:88, 232`). |
| Den som legger fram, beviser nøkkelen sin | `expectedSubject: identity` (`:1474`) og `checkIdentityOrigin(identity, against: contract.subject)` (`:1478`). Utfordringen er bundet til ressurs og domene (`:2355-2363`). |
| Innenfor malen | `agreementDerivedFromTemplate` (`:1486`, `:1542-1570`) kontrollerer eier, varighet, rettigheter, policybinding og vilkår. Det kontrolleres på nytt ved hver tilgang (`:2268-2275`). Kontrakten som installeres, er den signerte, ikke den avledede, og det er riktig. |
| Tidsvindu | `verifySignature(now:)` gjennom bindingen, og `temporalStatus == .active` (`:1492`). Varigheten er låst: `expiresAt − issuedAt` må være lik `agreement.duration` (`Contract.swift:149`). Godtatt klokkeavvik er 300 s. |
| Samme kontrakt to ganger | `addContract` fjerner dubletter på `uuid` og på dublettnøkkel, `addMember` på UUID (`GeneralAuditor.swift:431-436, 510-515`). Gjentatt framlegging fornyer også innslippet, se MÅ 1. |
| Tredjepart legger fram S sin kontrakt | Avvises på grunn av subjektets fingeravtrykk og nøkkelbevis. |
| Endring under `await` | Ufarlig for innslipp, med to unntak: kappløpet i MÅ 1 og vilkårene i BØR 2. |
| `debugValidateAccessForEverything` | Er flagget på, avvises alt (`:1462`). |

Den nye veien hopper over `admissionPolicyAllows`. Det er greit, fordi alle tre policyene slipper gjennom når eieren har autorisert (`:1511-1513`). Eierens signatur står her for eierens godkjenning.

**2. Gamle kontrakter og bindingen.**
- Både `Contract` og `SigningPayload` bruker syntetisert `Codable`, og det finnes ingen egne utvidelser. Et valgfritt felt med verdien `nil` kodes da med `encodeIfPresent`, slik at nøkkelen utelates. Bytene som signeres for en kontrakt med `nil`, blir derfor de samme som før (`Contract.swift:66-89, 221-235`). Testen `testRejectsUnboundLegacyContractWhileKeepingItsSignatureValid` viser det.
- Fjernes eller endres bindingen, endres de signerte bytene, og signaturen feiler.
- Den nye veien godtar ikke `nil` (`:1470`).
- På den gamle veien kan ingen legge fram en kontrakt. Filteret på `:2257` hopper over kontrakter som er bundet til en annen celle.
- En eldre binær som dekoder og lagrer en v2-kontrakt på nytt, mister feltet. Da feiler signaturen, så feilen lukker tilgangen.
- Det som var før, gjelder fortsatt: en kontrakt med `nil` er bare bundet til eier og domene, ikke til cellen.

**3. Endrer `authorizationContracts(for:)` noe for lokale kontrakter?** Nei. Den eneste endringen er `guard` på `GeneralCell.swift:2257`, og den slipper alltid gjennom `nil`. `addAgreement` signerer fortsatt uten binding (`:1418-1424`).

**4. Testene** (`Tests/CellBaseTests/ExternalAgreementAdmissionTests.swift`).
- Nøkkellagrene er virkelig adskilt. `EphemeralIdentityVault` er en `actor` med lagring per instans (`EphemeralIdentityVault.swift:11-17`), og A, B og S er tre instanser (testlinje 51-54).
- `setUp` krever at flagget er av. Produksjonskoden avviser også når det er på.
- Avvisningstestene starter fra autentisk signerte byte (hjelperen bekrefter signaturen) og skiller seg fra den gyldige kontrakten på ett punkt. De er ikke tautologiske. Svakheter:
  - **a)** `testRejectsChangedCellBindingAfterWireRoundTrip` kontrollerer bare `verifyCryptographicSignature`. Den legger ikke kontrakten fram for cellen, og den prøver ikke å fjerne bindingen helt.
  - **b)** Filteret i den gamle veien (`:2257`) er ikke testet.
  - **c)** Skriving og tredjepartens lesing avvises med en tom `catch {}`. Det finnes ingen positiv kontroll som viser at eieren kan skrive. «Write rejected» kan derfor skyldes en annen feil enn manglende tilgang.
  - **d)** `testRejectsHostAddAgreementWithoutOwnerPrivateKey` stopper på policyen (`:1396`) før `contractSigningOwner`. Den sjekker ikke at medlemslista er tom, og den består også på grunnlaget. Det stemmer med «som i dag».
  - **e)** `testPublicRemoteSubjectWithoutSigningProxyCannotProveControl` viser bare at en identitet uten nøkkellager ikke kan signere. Navnet sier «Remote» uten at noe er fjernt.
  - **f)** Ingen test dekker tilbakekall fulgt av ny framlegging (MÅ 1).

**5. Stemmer rapporten med koden?** For det meste. Linjehenvisningene stemmer innenfor et par linjer: `permit` står på `BridgeIdentityProofAuthorization.swift:77`, ikke `:75`. Rapporten er ærlig om at grunnlinjen ga grønt for avvisningstestene bare fordi en testadapter alltid avviste. Disse påstandene er sterkere enn koden:
- Punkt 5, tilbakekall: se MÅ 1.
- «fryser framlagt Contract … før await»: se BØR 2.
- Punkt 4 i rapporten: den eneste testen som er kjørt, er tautologisk. Rapporten sier selv at fjernbeviset ikke er vist.
- Tallene for hele testmengden (1577/0/5) kan jeg ikke kontrollere her.

**6. Hva blokkerer bolk 2?**
- Tilbakekall (MÅ 1).
- En rute for å legge fram kontrakten over broen, med subjektets bevis. `permit` krever i dag `action == "checkIdentityOrigin"` og `audience == "GeneralCell"` (`BridgeIdentityProofAuthorization.swift:77-86`), og utfordringen bruker de samme verdiene (`GeneralCell.swift:2359-2361`). Den eksisterende bevisflyten kan altså trolig brukes, men bare med en lokal lease hos S. Det er ikke testet.
- Ellers BØR 1, 3 og 4.

Jeg fant ikke noe annet i bolk 1 som stenger veien.
