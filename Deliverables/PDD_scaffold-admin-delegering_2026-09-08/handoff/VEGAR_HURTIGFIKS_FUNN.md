# Funn: hva som skal til for å gi Vegar publiseringstilgang nå

Dato: 2026-09-09, natt. Read-only undersøkelse på staging. Ingenting ble endret.
Dette er Kjetils Q4 (utenfor selve PDD-en), men funnene hører hjemme her fordi de
er selve begrunnelsen for arbeidspakkene.

## Målt

- Staging-datarot: `/mnt/disk1/app/CellsContainer.staging-f76de5a`, ~1300 identitetskataloger, 147 MB. `.secrets` datert 19. august — dette er den ferske roten.
- `grep -rl publisherAccess` over hele roten gir **nøyaktig én** fil:
  `CellsContainer/7A741743-5F8B-424E-BFF7-E30A8760123D/keypathstorage.json`.
  Den inneholder VC-en utstedt til `linkedIdentity.displayName = vegar`
  (uuid `8DCE5C5A-35E7-443E-A4A6-EDE781746CA4`), `issuanceDate 2026-09-02T08:06:06Z`,
  `validUntil 2026-09-04T08:06:06Z`. Utløpt.
- Det finnes altså **ingen lagret `publisherAccess.issue`-Agreement for noen**.
- `ArendalsukaConfigurationPublisher` nevnes i fire `CellConfiguration.json` under
  Arendalsuka Participant Program og i `ScaffoldOrchestrator/NamedEmitters.json`,
  men ingen av dem eksponerer en eier-post for selve publisher-cellen. Cellen har
  ingen synlig persistert eierregistrering i denne dataroten.

## Hva det betyr

`VaporConferenceMVP` avviser i preflight fordi `publicationAccessIssuanceDecision`
for den innloggede nettleseridentiteten verken gir `ownerProof` eller
`signedContract`. Kilden er eksplisitt: «Control-plane role labels are deliberately
absent» — at Kjetil er `admin.operator` teller ikke.

`portholeRuntimeOwner` (ScaffoldKit) returnerer requesteren som eier bare hvis
requesteren *er* den lagrede eieridentiteten kryptografisk **og** er bundet til den
tilknyttede home-vaulten. Med ingen synlig eierregistrering i den ferske roten er
det ikke gitt at noen nettleserinnlogging i dag oppfyller det.

## Konsekvens

«Fiks nå med dagens mekanisme» er derfor **ikke** bekreftet som en enkel handling.
Det er ikke verifisert at det finnes en innlogging på staging som løser seg til
cellens eier. Alternativene, i økende inngripen:

1. Finn ut om en eksisterende innlogging faktisk løser til eier (krever en
   autentisert kjøring, ikke en filsjekk — kan ikke avgjøres read-only).
2. Utsted Agreement på `publisherAccess.issue` til Kjetils identitet via
   scaffoldets egen signeringseier. Krever et lite, revidert skript kjørt på
   serveren — altså en engangshandling av samme type som PDD-en skal erstatte.
3. Vent på WP1/WP2. Da er dette en `mandate.issue` fra `entity:digipomps`, med
   revisjonsspor og tilbakekall, og den samme situasjonen kan ikke oppstå stille igjen.

**Anbefaling:** ikke gjør 2 på natten uten Kjetil. Alternativ 1 tar minutter når han
er våken og logget inn; hvis den feiler, er 3 uansett kort vei unna, og 2 blir en
engangsting vi må rydde opp i etterpå.

Dette er ikke en blokker for WP0/WP1.
