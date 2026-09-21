# Dataflyt — entitetsdata egen kontroll

Skrevet 2026-09-21 til G2. Kildene er lest, ikke gjettet; filreferansene er sjekket.

## 1. Den ene setningen

Alt som endrer entitetsdata går gjennom **én** sluse: et forslag som blir stående til eieren
signerer, og som da skrives som én `entity.batchPersist` med ett chronicle-innslag. Det finnes ingen
annen vei inn, og det er hele poenget.

## 2. Tre veier inn, én vei gjennom

```
  FIL                    DIREKTE                  MODELL
  SkeletonFileUpload     redigering i             AIGateway (i Binding,
  (supportsDrop)         editor / ark             identityUnique, eid av
       │                      │                   eierens private identitet)
       │                      │                        │
       │                      │                   trustedModels-sjekk ──► avvist hvis
       │                      │                        │                  ukjent/revokert
       ▼                      ▼                        ▼
  ┌──────────────────────────────────────────────────────────────┐
  │  FORSLAGSKØ            (ingen skriverett, uansett opphav)     │
  │  hvert forslag: keypath, fra-verdi, til-verdi, opphav,        │
  │  formål (purpose://), og modellreferanse hvis en modell laget │
  │  det                                                          │
  └──────────────────────────────────────────────────────────────┘
                              │
                     EIERENS SIGNATUR
                     (krever bevis, se §3)
                              │
                              ▼
                   entity.batchPersist  ── én konvolutt, idempotent på mutasjons-id
                              │
                              ▼
                   EntityAnchorCell
                     person · purposes · relations · agreements
                     identityLinks · trustedModels · chronicle[+]
```

Ingen pil går utenom køen. En modell som kunne skrive direkte ville gjort «modellen foreslår, eieren
signerer» til en høflighetsformulering.

## 3. Autorisasjonsveien — hva som skjer før noe som helst

Både lesing og skriving går gjennom det samme. I dag stopper den ved identitet; etter WP2 går den
til entitet.

```
forespørsel (requester: Identity, keypath, handling)
     │
     ├─ 1. signatur stammer fra IdentityLinkRecord.linkedIdentity.publicKey ?   nei ─► avvist
     ├─ 2. status == .active, ikke revokert, ikke utløpt ?                      nei ─► avvist
     ├─ 3. handlingen i approvedScopes, domenet i approvedDomains ?             nei ─► avvist
     ├─ 4. entityBinding løser til entiteten som eier cellen ?                  nei ─► avvist
     │
     ▼ ja på alle fire
  slipper gjennom — og bare til det scope lenken faktisk gir
```

`IdentityLinkRecord` ligger i `CellProtocol/Sources/CellBase/Identity/IdentityLinkingModels.swift:290`.
`EntityAnchorCell` holder allerede `identityLinks` med `approveEnrollment`, `completeEnrollment` og
`revoke` (`CellScaffold/Sources/App/Cells/EntityAnchorCell.swift:292-301`). Det som mangler er at
tilgangskontrollen slår opp i den.

**Grensen går ved cellen, ikke ved scaffoldet.** En entitet med admin på et skyscaffold kommer
gjennom skritt 1–3 for sine egne celler og faller på skritt 4 for andres. «Jeg eier maskinen» er
ikke en tilgangsgrunn, og `test.entitet.admin-cannot-enter-foreign-cell` er det som gjør påstanden
etterprøvbar.

## 4. Genesis — det ene øyeblikket som ikke kan gjøres om

```
første gang entitetsdata må persisteres
   (onboarding som samler data · adressebok-import for å invitere · VC-bevis)
              │
              ▼
   EntityAnchorCell opprettes
              │
              ▼
   IdentityLinkRecord #1
     issuerType: .existingDevice
     entityBinding: .localEntityAnchor
     linkedIdentity: initiatorens offentlige nøkkel
              │
              ▼
   FORSEGLET  ── ingen handling setter dette tilbake.
                 Et andre genesis-forsøk avvises (test.entitet.no-refounding).
```

Import og genesis er samme flyt, ikke to runder — avklart 2026-09-15.

## 5. Modellveiene ut

Alt som kan nå en modell går gjennom gatewayen. Det er en påstand som må kunne testes, og
`test.entitet.no-model-outside-gateway` er testen.

| Vei | Transport i dag | Hvem kontrollerer utgangen | Erklæring |
|---|---|---|---|
| Lokal modell | `localLoopback` | vi | endepunkt og modell |
| Hostet modell (OpenAI, Anthropic, …) | `remoteTLS` | vi, via egress-policy + `apiKeyAlias` | endepunkt, modell, nøkkeleier |
| Apple Intelligence — på enheten | **ingen** | Apple | påstand, se under |
| Apple Intelligence — Private Cloud Compute | **ingen** | Apple | påstand, se under |
| Tredjepart gjennom Apple | **ingen** | Apple | påstand, se under |

`AIGatewayEndpointTransport` har i dag bare `localLoopback` og `remoteTLS`
(`CellScaffold/Sources/App/Cells/AI/AIGatewaySupport.swift:668`). Begge er kall *vi* gjør. Apple
Intelligence er et rammeverkskall i prosessen, og det er Apple som avgjør om det blir liggende på
enheten. **Vi kan erklære, ikke håndheve** — og erklæringen må si det, ellers later vi som vi har en
kontroll vi ikke har. Om rammeverket i det hele tatt lar oss velge vei er §6.5, og den er ubesvart.

## 6. Hvor ting ligger

| Det | Hvor | Hvem eier |
|---|---|---|
| Entitetsdata | `EntityAnchorCell`, `identityUnique` | eierens private identitet |
| API-nøkler | `OwnerScopedCredentialStore`, innenfor entiteten | eieren |
| Tillitserklæringer | `trustedModels.<id>` under ankeret | eieren, signert |
| Forslagskø | gateway-cellen, kortlivet | eieren |
| Chronicle | under ankeret, kun tillegg | eieren |
| Prompt og svar | innenfor entiteten, uansett hvor modellen kjører | eieren |

Det siste er hele grunnen til at gatewayen skal ligge i appen og ikke bare på serveren: en gateway
utenfor entiteten gjør prompten til noen andres data.
