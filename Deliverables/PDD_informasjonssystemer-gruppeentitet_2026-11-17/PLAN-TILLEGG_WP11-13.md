# Tillegg til planen: WP11–13 i CellScaffold

Dato 2026-11-24. Status: venter på Kjetils godkjenning (G2-tillegg).

CellProtocol 2026.9.18 inneholder organisasjonsmodellen (WP1–10). Før cellene og flatene bygges i CellScaffold har jeg lest koden på begge sider. Sju ting i planen holder ikke som skrevet. Hver har et forslag under.

## Det som må avgjøres

| Nr | Funn | Forslag |
|---|---|---|
| 1 | **Hvelvet husker ingenting over en omstart.** `OrganizationVault` kan bare startes fra forseglingen. Etter en omstart er utstedte roller borte, statuslisten begynner på sekvens 1 igjen (noder som har speilet en nyere liste avviser den), og vernet mot gjenbrukte nonce-verdier er nullstilt. | Legge til lagring og gjenoppretting i `OrganizationVault` i CellProtocol, med tester, i en egen PR. Det krever en ny tag (2026.9.19) før CellScaffold kan bruke det. |
| 2 | **En eier er én nøkkel.** Policyen kjenner en eier som én identitet. På web signerer du med web-identiteten din, i Binding med enhetsnøkkelen. Er begge medlemmer, teller du som to personer, og «begge eiere må godkjenne» kan oppfylles av én. | På staging er eieren web-identiteten din. Godkjenning fra Binding (WP14) løses for seg, og jeg kommer med et eget forslag da. Jeg legger ikke inn to nøkler for samme person. |
| 3 | **Passkey kreves ikke av modellen.** Malene setter ikke `requiresFreshAuth`, og hvelvet sjekker ikke beviset. En godkjenning uten passkey ville blitt tatt imot. | Gruppecellen krever det selv: web-ruten verifiserer passkey-signaturen over forslagets hash før godkjenningen lages. Policy-formatet og fixturene i Swift, Python og Go røres ikke. |
| 4 | **Knappene i de godkjente skjelettene vet ikke hvilken rad de gjelder.** «Godkjenn», «Avvis» og «Trekk tilbake» har tom payload, velgerne sender ikke valget til serveren, og «Gi rolle» har ingen vei til Gi rolle-flaten. | Legge til rad-id i payload, `selectionActionKeypath` på velgerne og navigasjon på «Gi rolle». Ingenting av dette endrer hvordan flatene ser ut. Føres som avvik i `images/README.md`. |
| 5 | **Ingen kan logge inn som gruppa.** Gruppas identitet har ingen innlogging, så eierbevis slik andre celler bruker det, går ikke. Planen sier også at scaffold-eieren skal kunne stoppe cellen, men det finnes ingen mekanisme for det. | Rett til å foreslå og godkjenne følger av medlemskap i policyen pluss signert godkjenning. Én nøkkel, `group.operate.stop`, gis bare til scaffold-eieren og setter cellen i stoppet tilstand. |
| 6 | **Hvelvet journalfører bare det som blir signert.** Avviste forslag, ventende forslag og enkeltgodkjenninger står ikke i journalen. | Gruppecellen fører sin egen logg over forslag, godkjenninger og avvisninger. Hvelvets journal står som den er. |
| 7 | **Gruppas identitet må finnes på staging før deploy.** Med dagens oppstart hoppes registreringen stille over hvis identiteten ikke er lagt inn, og flaten blir tom uten at CI merker det. | Føres som eget steg i forespørselen til HAVEN-Deploy. Jeg legger også inn en test som feiler hvis cellen ikke er registrert. |

## Ærlig om testnøkkelen

Gruppas nøkkel på staging er en programvarenøkkel i scaffoldens hvelv (ditt valg 18.11). Den som eier scaffolden kan derfor teknisk sett signere som gruppa. Flaten sier dette i klartekst («testnøkkel»), og `keyIsExportable` står som sann.

## Mindre ting jeg gjør uten å spørre

- Nøkkelen heter `role.issue` i koden. Planens `roles.issue` var en skrivefeil.
- Ventende forslag som blir ugyldige fordi policyen eller statuslisten har endret seg i mellomtiden, merkes «utløpt».
- Cellen fornyer speilet av statuslisten jevnlig, ellers ser «Mine roller» ukjent status etter 600 sekunder.
- `test.ge.owns-cells` kjøres i Swift. Hvelvet finnes ikke i Python og Go, så «Py + Go» i testlisten faller bort for denne testen.
- Kontraktsfilene for de to cellene (`contract/`) skrives sammen med cellene.

## Rekkefølge

1. CellProtocol: lagring og gjenoppretting i hvelvet (punkt 1), verifisert på Mac-en, så tag.
2. CellScaffold WP11: kontrakt, hvelvcelle, gruppecelle, registrering, tester.
3. CellScaffold WP12: passkey-rute, flatene «Informasjonssystemer» og «Gi rolle».
4. CellScaffold WP13: «Mine roller».

Kartleggingen bak dette ligger i trådens arbeidsnotater. Kildehenvisninger med fil og linje kan jeg legge ved hvis du vil se dem.
