# Runde 1 — genesis (WP1) og autorisasjon via IdentityLink (WP2)

Skrevet 2026-09-22. Én patch, tre skript. Kjør dem i rekkefølge fra denne mappen på macOS.

    ./preflight.sh
    ./apply.sh
    ./apply.sh --go
    ./verify.sh

`preflight.sh` endrer ingenting. `apply.sh` uten `--go` er tørrkjøring. Ingen av skriptene committer.

## Hva patchen gjør

| Fil | Endring | Formål |
|---|---|---|
| `Sources/CellBase/Identity/EntityGenesis.swift` | **ny** — `EntityGenesisSeal`, `EntityGenesisService.seal/verify` | WP1 |
| `Sources/CellBase/Identity/EntityLinkAuthorization.swift` | **ny** — `EntityLinkAuthorizer.authorize`, fire skritt | WP2 |
| `Sources/CellBase/Cells/GeneralCell/CellAuthorization.swift` | ny sti `.linkedIdentity`, nytt felt `linkRef`, ny parameter på `decide` | WP2 |
| `Sources/CellBase/Cells/GeneralCell/GeneralCell.swift` | ny `open func authorizeLinkedIdentity`, kalles bare når requester ikke er eierreferansen | WP2 |
| `Sources/CellBase/Security/CellSecurityEvent.swift` | uttømmende switch utvidet | WP2 |
| `Sources/CellVapor/Cells/EntityAnchorCell.swift` | genesis-handling, immutabel seal, revoke nekter genesis, forsegling ved første batchPersist, `authorizeLinkedIdentity`-override | WP1+WP2 |
| `Sources/CellApple/Cells/EntityAnchorCell.swift` | identisk, 8 samme erstatninger | WP1+WP2 |
| `Tests/CellBaseTests/EntityGenesisTests.swift` | **ny** — ren logikk, 6 tester | genesis-once |
| `Tests/CellBaseTests/EntityLinkAuthorizationTests.swift` | **ny** — ren logikk, 12 tester | linked-identity-accepted, foreign-entity-refused |
| `Tests/CellBaseTests/EntityAnchorGenesisTests.swift` | **ny** — mot Vapor-ankeret, 7 tester (macOS) | genesis-once, no-refounding, begge autorisasjonstestene |

De to ren-logikk-filene er de sterkeste bevisene: ingen scaffold, ingen fil-I/O, bare
krypto og regler. Ankertestene bruker samme harness som `VaporCellRuntimeReadinessContractTests`.

## Det jeg ikke har kunnet sjekke — se på disse først hvis noe er rødt

Jeg har lest kildene og fulgt mønstrene, men ingenting er kompilert. Fire steder er jeg
minst sikker:

1. **`Identity(uuid, displayName:, identityVault:)`** — brukt i testene for å lage en
   bedrager med samme UUID. Signaturen er lest fra `MockIdentityVault`; hvis `init` heter noe
   annet, rett i testene, ikke i produksjonskoden.
2. **Prefiks-dispatch for set.** `testGenesisCannotBeRevokedOrOverwritten` setter
   `identityLinks.genesis.trigger` og forventer at rot-intercepten `identityLinks` fanger det
   og går til `default`-grenen i `handleIdentityLinksSet`, der guarden ligger. Lest fra
   `GeneralCell.set` linje ~1736 (exact → rot). Faller den ikke dit, er det testen som må
   sette keypathen på en annen måte — guarden skal stå.
3. **`storage.set` sync vs. async.** Jeg brukte `try storage.set(...)` (sync, som i
   `handleIdentityLinksSet`). Andre steder i samme fil står `try await self.storage.set(...)`.
   Kompilatoren sier fra om ett av dem.
4. **`EntityBindingDescriptor(mode:bindingID:audience:)`** i `testPairwiseBindingDoesNotOpenTheAnchor`.
   Init-en har de parameterne i revisjonen jeg leste (`IdentityLinkingModels.swift:55`), men
   utdraget var kuttet. Klager kompilatoren, sett `entityAnchorReference: nil` eksplisitt.

## Det som IKKE er testet i denne runden, med vilje

**Forsegling ved første `batchPersist`.** De fire linjene i `persistBatchEnvelope` kjører bare
som feed-intercept når ankeret absorberer en annen celles flow gjennom auditoren. Ingen
CellBase-test bygger den harnessen i dag, og `GeneralCell.intercepts` er privat.
`TESTRESULT.md` skal si **blocked** for den halvparten av `test.entitet.genesis-once`, ikke
utelate den. Runde 2 (WP3–WP5) trenger den harnessen uansett.

## Etter grønt

Commit på `pdd/entitetsdata-egen-kontroll` med referanse til
`purpose://candidate.entitetsdata.genesis-seals-to-initiator` og
`purpose://candidate.entitetsdata.authorization-resolves-entity` i meldingen. Ikke push til main.
Lim de tre resultatlinjene fra `verify-*.log` inn i `TESTRESULT.md#genesis` og `#auth`.

## Kjente konsekvenser å vite om

- `PurposeBoundExternalAction.authorityEvidence` har `default:` → en lenket identitet får
  `.none` som autoritetssti for eksterne handlinger. Det er konservativt og riktig: en lenke
  gir tilgang til entitetsdata, ikke eierens tak for eksterne effekter. Nevnt så ingen tror
  det er glemt.
- `authorizeLinkedIdentity` dekoder alle lenkeposter fra storage ved hvert oppslag, men bare
  for requestere som *ikke* er eieren. Eierens varme sti er urørt. Cache når det trengs.
- Per-nøkkel direkte `set` (`person`, `relations`, …) forsegler ikke. Bare batch-veien og den
  eksplisitte handlingen gjør det. Det er tilsiktet: de direkte stiene skal bak forslagskøen
  (WP7), og dataflow.md §2 sier at ingen pil går utenom den.
