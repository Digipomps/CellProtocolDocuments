STATUS: LEVERT — fiksen er ute i begge miljøer. **RETTET 2026-09-23 11:45Z — tre feil i første utgave, se nederst.**

# Arendalsuka-tilgang: hva som er gjort, og hva du må ta stilling til

Skrevet 2026-09-23T10:15Z. Bevis: `evidence/admin-tilgang/`, `evidence/arendalsuka-utsteder/`.

## Rotårsaken til 403-en

`agreement_or_proof_required` handlet aldri om Vegar. Publisher-cellen er `scaffoldUnique` med
eget identitetsdomene, så eieren er en identitet i *serverens* IdentityVault — ikke et menneske.
Kjeden må være `server (eier) → første menneske (issue-grant) → mottaker (publiserings-VC)`.
Ledd 2 og 3 hadde HTTP-vei. **Ledd 1 hadde ingen**: den eneste veien til det første grantet
fantes in-process, i testene. Ingen menneskelig identitet hadde publiseringsmyndighet i noe
miljø, og rollemerkelapper gir ikke myndighet her — cellen sier det selv
(`roleLabelsAreAuthoritative: false`).

## Det som er ute nå

| | staging | produksjon |
| --- | --- | --- |
| `MVP_ADMIN_OPERATOR_USER_IDS` | Kjetil + Vegar | Kjetil + Vegar |
| `MVP_ADMIN_SECURITY_USER_IDS` | Kjetil + Vegar | Kjetil + Vegar |
| `HAVEN_ARENDALSUKA_PUBLISHER_BOOTSTRAP_USERNAME` | `kjetil2` (09:39Z) | `kjetil2` (10:10Z) |

Begge satt med `haven-deploy <env> current --env-only`, som leser revisjonen ut av containeren:
`COMMITTED_VERIFIED`, revisjonen **uendret** på `77a922bc`, `/health/ready` ready. Ingen deploy,
ingen ny sha.

## Det ene steget bare du kan ta (2 minutter, i nettleseren)

Logg inn som **`kjetil2`**, gå til admin-flaten, skriv **`Vegar`** (prod) eller **`vegar`** (staging) i feltet for
publiseringstilgang og trykk. Ett kall gjør begge deler: bootstrap-steget kjører *før* subjektet
slås opp og gir deg selv ett Agreement med nøyaktig ett grant — `rw-s` på
`publisherAccess.issue`, ett år — og deretter utstedes publiserings-VC-en til Vegar.

To presisjoner, lest i kilden i dag:

- **Skriv brukernavnet eksakt slik miljøet har det:** prod har `Vegar` (stor V), **staging har `vegar`** (liten v). Oppslaget filtrerer på eksakt `username`; feil variant gir 404.
- Du trenger *ikke* et første kall «uten subjectUsername». Det sto i skriptet fra 16. september,
  men admin-GUI-et nekter å sende kallet uten navn, og bootstrappen er uansett uavhengig av det.
  Rettet i `ROOT-arendalsuka-utsteder.sh` med begrunnelsen i koden.

Gjør det i staging først hvis du vil se det virke uten risiko. Etterpå kan env-variabelen fjernes
— Agreementet står, og det er da autoriteten ligger i CellProtocol i stedet for i env.

## Det du må ta stilling til

### 1. Skal `pdd/scaffold-admin-delegering` leveres? (den største)

Dette er «CellProtocol-styrt adgang, ikke juksing med env-variabler» — og den er **skrevet
ferdig**. `PDD_scaffold-admin-delegering_2026-09-08`: WP1–WP8 committet 9. september på
`pdd/scaffold-admin-delegering`, seks commits (`bcaf1e5e`), 18 filer, +2910/−336, WP9
dokumentasjon utført. Full regresjon 2150 tester, null nye feil mot baselinen.

**Den er aldri pushet.** Det finnes ingen `origin/pdd/scaffold-admin-delegering`. Målt mot
`Leveransegap.md` er det et gap, ikke en tilstand: «ligger på en gren» teller ikke som levert.
Årsaken oppgitt den gang: push er git-administratorens avgjørelse — din.

At hullet er reelt ser du i prods egen readiness akkurat nå:

```text
"runtimeAdvisories":[
  "scaffold_administrator_not_provisioned scaffold=scaffold:cellscaffold",
  "scaffold_administrator_threshold_below_two ... requiredSignatures=1 reason=utviklingsfase, styreleder alene"
]
```

**Ditt valg:** skal jeg pushe grenen og kjøre den gjennom kjeden (origin/main → staging → prod),
slik vi gjorde med skjelettrunden i går? Da blir både du og Vegar administratorer i CellProtocol
i stedet for i `MVP_ADMIN_*`.

To ting den PDD-en selv sier gjenstår, og som er dine og ikke mine: `entity:digipomps` og
`entity:dimy` med representantoppsett er ikke opprettet noe sted (det er det «som representanter
for Digipomps» faktisk betyr i CellProtocol-termer), og juristvurderingen mangler.

### 2. Skal Arendalsuka-programmet være offentlig i prod?

`ARENDALSUKA_REMOTE_CONFIGURATION_ACCESS` er **tom i prod**; staging har `public`. Dette er en
databeslutning, ikke en deploy-fiks (`a8811576 Protect the public Arendalsuka data boundary`).

Og den har en reell risiko som er verdt å vite om før du sier ja: med flagget satt tar koden den
*andre* grenen — `ensurePublishedProgramReadAgreement` går forbi nil-stien og krever `.signed`,
som krever at `requireLocalSigningOwner` lykkes for `arendalsuka-public-landing`. Eieren finnes,
men at `addAgreement` returnerer `.signed` er ikke verifiserbart utenfra. Slår det feil, står prod
på 503 med en ny grunnkode.

**Min anbefaling:** ja, men som egen enkeltendring etter at utstederen din er på plass, og med
tilbakerulling = én miljøvariabel. Jeg kan kjøre det på staging først og vise deg
`/arendalsuka`-visningen før vi rører prod. Si fra.

### 3. Observer-listen (kosmetisk, ingen hast)

`MVP_ADMIN_OBSERVER_USER_IDS` har bare deg. Det spiller ingen praktisk rolle:
`MVPAdminAccess.authorization` lar både operator og security implisere observer, så Vegar har
observer-rettighetene. Å føre ham inn eksplisitt er ryddighet, ikke funksjon.

## Spørsmålet ditt om «Identity UUID» — svaret er nei, det trengs ikke

Du skrev at «Vegar og min sin `MVP_ADMIN_*_USER_IDS` Identity UUID må også settes». Det er
allerede riktig satt, og det er ikke en Identity-UUID:

- `MVPAdminAccess.requireAdminUser` bruker `user.requireID().uuidString.lowercased()` — altså
  **FidoUser-radens** UUID. Det er nøyaktig de to som står i prod nå: `87fa1cf0…` (`kjetil2`) og
  `836f624a…` (`Vegar`).
- Bootstrappen bruker med vilje **brukernavn**, ikke identity-UUID. Fra
  `Arendalsuka_Publisher_Bootstrap_2026-09-09.md`: «identiteten er nettleserbundet og ulik per
  miljø, mens brukernavnet er stabilt» — og det holder identity-ID-er ute av konfigurasjon, slik
  Vegar-handoffen §A5 krever.

Så det finnes ingen tredje UUID som mangler. Hvis du likevel så en identity-UUID et sted i GUI-et
som virket ubrukt, send meg skjermbildet — forrige kom ikke gjennom.


---

## Rettelser 2026-09-23 11:45Z — tre ting i første utgave var feil

1. **«`pdd/scaffold-admin-delegering` er aldri pushet … et gap» — feil.** Innholdet landet på main
   2026-09-18 i #247 (`87256f9a` «Restore Butler workflows and verified admin deployment path»):
   11 av grenens 18 filer er byte-identiske med main, de 7 andre er *utvidet* der, og
   provisjoneringsverktøyet kom i tillegg. Koden kjører i begge miljøer. Jeg målte om grenens *ref*
   fantes på origin — det er squash-merge-fellen jeg selv skrev ned samme morgen. Det som faktisk
   manglet var WP10: selve registreringen. **Den er nå gjort i staging** (se
   `PDD_scaffold-admin-delegering_2026-09-08/handoff/WP10-STAGING-20260923.md`).
2. **«Identity UUID trengs ikke» — feil for den CellProtocol-styrte veien.** For `MVP_ADMIN_*`
   stemmer det (FidoUser-UUID). Men provisjoneringen av representanter krever
   `representative.expectedIdentityUUID` = `FidoUser.identity_id` — nøyaktig det du sa måtte settes.
   Verdiene er lest fra databasene: staging kjetil2 `DF8D4644…`, vegar `8DCE5C5A…`; prod kjetil2
   `E027291A…`, Vegar `ABA68006…`.
3. **«Skriv `Vegar` med stor V» gjaldt bare prod.** Staging har `vegar`. Rettet over.
