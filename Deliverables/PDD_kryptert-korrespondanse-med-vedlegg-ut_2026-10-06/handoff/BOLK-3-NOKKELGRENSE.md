# Eierens nøkkelgrense — vurdering, ikke implementert sikkerhet

Godkjent første pakke bruker samme deltakeridentitet. En separat agentidentitet
innføres ikke. Den uavhengige gjennomgangen vurderer følgende som mulig innen
omfanget, med brokerprosessen som betrodd sikkerhetsgrense:

- Native UI/broker eier hele klienten og den autentiserte eierkanalen.
- Agenten får bare typet ordinær meldings-/vedleggs-MCP; ingen rå signering,
  nøkkelbevis, vilkårlige keypaths eller join-/agreement-administrasjon.
- Samme eiernøkkel finnes i brokerens særskilte Data Protection Keychain-gruppe:
  ordinær bruk etter opplåsing, separat userPresence-beskyttet lesing for hver
  administrativ handling. Begge kopier er utilgjengelige for agentprosessen.
- UI fryser dokumentet før autentisering. Fersk LAContext, ingen gjenbruk,
  ingen fallback til ordinær nøkkel ved avslag/feil. Bare det fryste dokumentet
  signeres. Nøkkelen genereres i broker; ingen ubegrenset eldre kopi migreres
  inn uten en eksplisitt sikker migrering.

Dette er ikke kryptografisk bevis for at en kompromittert broker ikke kan
administrere: dens ordinære nøkkel kan teknisk signere samme dokumenttyper.
Typed kode og prosess-/nøkkelgruppeisolasjon må derfor prøves sammen.

## Lest og målt

Apple krever autoriserte entitlements/provisioning for Data Protection Keychain.
Eksisterende pakke har bare automation-entitlement, ikke en særskilt brokergruppe.
Et lokalt, skrivefritt metadata-inventar dekodet 30 provisioning-filer: to
Mac-distribusjonsprofiler var gyldige etter oppgitt utløpsdato, men ingen gav
det foreslåtte broker-ID-et og en nøkkelgruppe. Inventaret verifiserte ikke
sertifikatkjeden eller faktisk OS-aksept. Apples CMS-dekoder forsøkte import
og ble avvist; OpenSSL ble bare brukt til lokal metadatautpakking uten import.
Ingen profil, nøkkelring, Developer Portal eller signeringsidentitet er endret.

For denne konkrete grensen mangler dermed en egnet Developer ID Mac-profil
for en særskilt HAVEN-brokerapp. En profil for en annen app skal ikke gjenbrukes
ved å utgi brokeren for den appen. File-based ACL er et annet, deprecated
Apple-API; det er ikke prøvd eller valgt som automatisk sikkerhetserstatning.

## Prøver før sikkerhetskravet kan bli grønt

1. Signert CLI og søsken uten broker-entitlement får ikke noen av nøklene.
2. MCP-avslag på rå signering, proof, vilkårlig RPC og admin gir ingen effekt.
3. Meldings-/vedleggsdata kan ikke brukes som signeringsoracle for admin.
4. Kansellert/feilet userPresence gir ingen signatur eller wire-effekt selv om
   den ordinære nøkkelen er tilgjengelig i broker.
5. To adminhandlinger gir to autentiseringer; ordinær bruk mellom dem gir ingen.
6. Endret forespørsel under dialog kan ikke endre det fryste dokumentet.
7. Oppstart, fixture-/legacyvalg og omstart åpner ikke en agentvei til nøkkelen.

## Primærkilder

- [Apple TN3137: Mac keychains](https://developer.apple.com/documentation/technotes/tn3137-on-mac-keychains)
- [Apple: Keychain access groups](https://developer.apple.com/documentation/security/ksecattraccessgroup)
- [Apple: userPresence og Keychain](https://developer.apple.com/documentation/localauthentication/accessing-keychain-items-with-face-id-or-touch-id)
- [Apple: LAContext ved nøkkeltilgang](https://developer.apple.com/documentation/security/ksecuseauthenticationcontext)

Ingen GUI-, Touch ID-, signerings-, pakke- eller prosessisolasjonsprøve er hevdet
bestått her. Nøkkelgrensen er ikke implementert.
