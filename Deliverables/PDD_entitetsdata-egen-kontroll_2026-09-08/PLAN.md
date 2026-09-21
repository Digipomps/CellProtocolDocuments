# PLAN — entitetsdata egen kontroll

Oppgavemappe: `PDD_entitetsdata-egen-kontroll_2026-09-08` · Skrevet 2026-09-21 · **venter på G2**

G1 godkjent 2026-09-15, delta godkjent 2026-09-19. G1-GUI godkjent 2026-09-15.
Én arbeidspakke per bladformål, i avhengighetsrekkefølge. Ingen pakke er «ferdig» før testene
den navngir er grønne og utdataene ligger i `TESTRESULT.md`.

## 0. To ting du bør vite før du leser videre

**0.1 Jeg kan ikke bygge Swift herfra.** Cowork-VM-en har ingen verktøykjede — det ble bekreftet
da jeg forsøkte å kjøre benchmarken i ark-oppgaven. Alt som rører Swift går derfor til Codex eller
Xcode, og leveres som idempotente skript med tørrkjøring som standard
(`pkg.std.codex-handoff`, se `handoff/README.md`). Det jeg selv kan gjøre er kontrakter,
skjelett-JSON, dokumenter, og lesing av kildekode. Kolonnen «Utfører» sier hvem som gjør hva, og
den er ikke en høflighetsformulering.

**0.2 §5 manglet åtte tester.** Formålstreet i §1 navngir `test.entitet.genesis-once`,
`no-refounding`, `read-without-proof-refused`, `chat-keypath-lookup`, `chat-change-is-a-proposal`,
`general-editor-covers-anchor`, `linked-identity-accepted` og `foreign-entity-refused`, men §5
definerte dem ikke. Jeg har lagt dem inn i §5 nå, med hvordan og hvor beviset lander. Treet er
uendret; det var tabellen som var ufullstendig. Sier du at dette burde vært fanget før G1, er jeg
enig — det er en regel skillet allerede har («hvert blad får minst én test i §5») og som ingen sjekk
håndhever. Foreslått som verktøysak i §5 under.

## 1. Rekkefølgen, og hvorfor den er slik

Fire pakker legger grunnen. Ingen av de andre kan testes ærlig før de står, fordi alle handler om
hvem som får gjøre hva.

```
WP1 genesis ──► WP2 autorisasjon kjenner entiteten ──┬──► WP3 lesing krever bevis
   (anker +    (IdentityLink slås opp i tilgangs-    │
    første     kontrollen)                           ├──► WP4 skriving krever eierbevis
    lenke)                                           │
                                                     └──► WP5 spor per endring
                                                             │
        ┌────────────────────────────────────────────────────┤
        ▼                          ▼                         ▼
   WP6–8 veier inn          WP9–13 gateway              WP14 flaten
   (fil, direkte,           (i appen, egne nøkler,      (tre veier synlige)
    generell editor)         erklærte veier, tillit,
                             foreslå-så-signer)
```

Grunnen til at genesis kommer før autorisasjonen, og ikke motsatt: autorisasjonen slår opp i en
`IdentityLink` med `entityBinding: localEntityAnchor`. Den lenken må finnes. Genesis er det som
lager den første. Etter WP1 er det sirkelen lukker seg — også re-forsegling avvises av WP2.

## 2. Arbeidspakkene

Hver rad i «Endrer» er en fil jeg har lest, ikke en gjetning.

### WP1 — Genesis forsegler entiteten til den som startet den

| | |
|---|---|
| **purposeRef** | `purpose://candidate.entitetsdata.genesis-seals-to-initiator` |
| **Utfører** | Codex (Swift), jeg skriver kontrakten først |
| **Avhenger av** | ingenting |
| **Endrer** | `CellScaffold/Sources/App/Cells/EntityAnchorCell.swift` (genesis-handling + første selvlenke), `CellProtocol/Sources/CellBase/Identity/IdentityLinkingModels.swift` (les, endre bare hvis noe mangler) |
| **Tester** | `test.entitet.genesis-once`, `test.entitet.no-refounding` |
| **Artefakt til §3** | `contract/entityanchor_genesis_v1.json` |

Første gang entiteten må persistere entitetsdata, opprettes ankeret og forsegles: en
`IdentityLinkRecord` med `issuerType: .existingDevice`, `entityBinding: .localEntityAnchor`, og
initiatorens offentlige nøkkel. Forseglingen er irreversibel — det finnes ingen handling som setter
ankeret tilbake til uforseglet, og et andre genesis-forsøk mot et forseglet anker avvises.

**Ferdig når:** to negative tester er grønne, og `contract/entityanchor_genesis_v1.json` har en
positiv og en negativ fixture som begge kjører.

### WP2 — Autorisasjonen kjenner entiteten, ikke bare identiteten

| | |
|---|---|
| **purposeRef** | `purpose://candidate.entitetsdata.authorization-resolves-entity` |
| **Utfører** | Codex |
| **Avhenger av** | WP1 |
| **Endrer** | `CellProtocol/Sources/CellBase/.../CellResolver` (eierskapssjekken), `GeneralCell.validateIdentityUniqueOwner` |
| **Tester** | `test.entitet.linked-identity-accepted`, `test.entitet.foreign-entity-refused` |
| **Artefakt til §3** | `TESTRESULT.md#auth` |

De fire skrittene fra §2A.2: signaturen stammer fra `linkedIdentity.publicKey`; lenken er `.active`
og ikke revokert; handlingen ligger i `approvedScopes` og domenet i `approvedDomains`;
`entityBinding` løser til den entiteten som eier cellen.

**Merk:** `CellResolver.swift` sto som ucommittet hos en annen tråd i august. Codex må sjekke
`git status` før pakken starter, og stoppe hvis filen har ulagrede endringer — ikke flette forbi dem.

**Ferdig når:** oppstartsidentiteten og Face ID-identiteten, som er to representanter for samme
entitet, begge slipper til — og en identitet fra en annen entitet ikke gjør det.

### WP3 — Lesing krever bevis, ikke bare mutasjon

| | |
|---|---|
| **purposeRef** | `purpose://candidate.entitetsdata.read-requires-entity-proof` |
| **Utfører** | Codex |
| **Avhenger av** | WP2 |
| **Endrer** | `EntityAnchorCell.swift` lese-intercepts (`identityLinks`, `person`, `relations`, `agreements`, `chronicle`) |
| **Tester** | `test.entitet.read-without-proof-refused` |

I dag går `validateAccess("r---", …)` på identitet. Etter WP2 skal den gå på entitet. Dette er den
halvparten av kravet ditt som er lettest å glemme, fordi mutasjon er den synlige halvparten.

### WP4 — Ingen andre kan endre mine entitetsdata

| | |
|---|---|
| **purposeRef** | `purpose://candidate.entitetsdata.no-write-without-owner-proof` |
| **Utfører** | Codex |
| **Avhenger av** | WP2 |
| **Endrer** | testmål først; kode bare der en negativ test faktisk faller |
| **Tester** | `test.entitet.auth-negative`, `test.entitet.admin-cannot-enter-foreign-cell` |

Fem avvisninger i én suite: feil identitet, usignert forslag, revokert modell, ukjent formål, og
direkte skriving utenom batch-veien. Pluss den nye fra §2A.1: **en entitet med admin på scaffoldet
kommer ikke inn i en celle eid av en identitet i en annen entitet.** Den siste krever et testoppsett
med to entiteter på samme scaffold, og det oppsettet er selv en leveranse — uten det er påstanden
«jeg eier serveren er ingen tilgangsgrunn» utestet.

### WP5 — Hver endring etterlater spor

| | |
|---|---|
| **purposeRef** | `purpose://candidate.entitetsdata.change-leaves-a-trace` |
| **Utfører** | Codex |
| **Avhenger av** | WP4 |
| **Endrer** | `EntityAnchorCell.swift` batch-veien |
| **Tester** | `test.entitet.trace` |

Hvert akseptert `entity.batchPersist` gir ett chronicle-innslag med signatur, hva som ble endret, og
modellreferansen hvis en modell foreslo det. Én batch, ett innslag — ikke ett per felt.

### WP6 — En fil eieren slipper inn lander i egen entitet

| | |
|---|---|
| **purposeRef** | `purpose://candidate.entitetsdata.file-into-entity` |
| **Utfører** | Claude (skjelett-JSON) → Codex (celle) → Kjetil (Xcode, kjør med den ekte fila) |
| **Avhenger av** | WP1, WP5 |
| **Endrer** | `Binding/Cells/ContactImportCell.swift`, ny skjelettkonfigurasjon |
| **Tester** | `test.entitet.file-roundtrip` |
| **Artefakt til §3** | kjørende flate + `skeleton/import_v1.json` |

`SkeletonFileUpload` med `supportsDrop` finnes (`AttachmentSurface.swift:292`). Rendereren sender en
kortlivet payload; cellen må validere type og størrelse selv. Importen er samme flyt som genesis, ikke
to runder — det er avklaringen fra 15.09.

**Prøvefila er `Binding/.sprout/import/HAVEN_import_bokprosjekt.xlsx` med 189 ekte personer. Den er
gitignorert og skal aldri inn i et repo, heller ikke som testfixture.** Fixturen lages syntetisk, med
de to radene som deler telefonnummer gjenskapt, siden det var den feilen bare ende-til-ende-testen
fant.

### WP7 — Ren redigering uten AI

| | |
|---|---|
| **purposeRef** | `purpose://candidate.entitetsdata.direct-edit` |
| **Utfører** | Claude (skjelett) → Codex (celle) |
| **Avhenger av** | WP4, WP5 |
| **Tester** | `test.entitet.direct-edit` |

Ett felt endret, ingen modell involvert, eiersignatur likevel. Denne pakken er liten og bør gjøres
tidlig: den beviser at signaturveien virker uten at noe AI-lag kan skjule en feil i den.

### WP8 — Et enkelt og helt generelt redigeringsverktøy

| | |
|---|---|
| **purposeRef** | `purpose://candidate.entitetsdata.general-editor` |
| **Utfører** | Claude (skjelett) → Codex |
| **Avhenger av** | WP7 |
| **Tester** | `test.entitet.general-editor-covers-anchor` |
| **Artefakt til §3** | `skeleton/editor_v1.json` |

«Generell» er målbart her: editoren skal nå hvert felt EntityAnchor eksponerer — `person`,
`purposes`, `relations`, `agreements`, `identityLinks`, `trustedModels` — ikke en håndplukket
delmengde. Testen teller feltene mot ankerets egen nøkkelliste, så editoren ikke kan råtne når ankeret
får et felt til.

**Avhengighet mot ark-oppgaven:** bildene viser tabeller. `PDD_ark-regneark_2026-09-17` eier
tabellelementet. Fram til det står, bygges editoren med `List` og faste bredder, og
`images/README.md` sier allerede at kolonnejusteringen blir omtrentlig. Ikke vent på arket.

### WP9 — Gatewayen bor i entiteten

| | |
|---|---|
| **purposeRef** | `purpose://candidate.entitetsdata.gateway-inside-entity` |
| **Utfører** | Codex |
| **Avhenger av** | WP2 |
| **Endrer** | Binding: registrer `cell:///AIGateway` `identityUnique`; port fra `CellScaffold/Sources/App/Cells/AI/` |
| **Tester** | `test.entitet.gateway-owned` |
| **Artefakt til §3** | `contract/aigateway_contract_v1.json` |

Gatewayen finnes i CellScaffold (3462 linjer) og ikke i Binding. Dette er en flytting, ikke en
nyskriving. Registrer `identityUnique` — ikke `scaffoldUnique`; det var den feilen som ga
`deniedNoGrant` for hver andre identitet og 1778 ms oppstart på Entity Scanner.

### WP10 — Eieren kobler på sin egen modell

| | |
|---|---|
| **purposeRef** | `purpose://candidate.entitetsdata.owner-brings-their-own-model` |
| **Utfører** | Codex |
| **Avhenger av** | WP9 |
| **Endrer** | `OwnerScopedCredentialStore` på Binding-siden |
| **Tester** | `test.entitet.own-key-scoped`, `test.entitet.key-removal-is-complete` |

Nøkkelmekanismen finnes allerede server-side. Kravet her er at nøkkelen ligger eier-scopet innenfor
entiteten, bare brukes til ruter eieren har erklært, og at fjerning er fullstendig — neste kall skal
feile med manglende hemmelighet, ikke falle tilbake på noe.

### WP11 — Hver modellvei er erklært, også Apples

| | |
|---|---|
| **purposeRef** | `purpose://candidate.entitetsdata.every-model-path-is-declared` |
| **Utfører** | Claude (undersøkelse) → Kjetil (§6.5) → Codex |
| **Avhenger av** | WP9 |
| **Status** | **blokkert på §6.5** |
| **Tester** | `test.entitet.no-model-outside-gateway`, `test.entitet.no-silent-escalation` |

`test.no-model-outside-gateway` kan gjøres nå: en kildeinspeksjon som slår fast at ingen kodesti når
en modell utenom gatewayen, `AppleIntelligenceCell` inkludert.

`test.no-silent-escalation` kan ikke designes før §6.5 er besvart: vi vet ikke om `FoundationModels`
lar oss *velge* vei eller bare observere hvilken som ble brukt. Kan vi ikke velge, er «på enheten»
en erklæring vi ikke kan håndheve, og da er spørsmålet om vi skal tilby den. **Første steg i denne
pakken er at jeg leser Apples dokumentasjon og kommer tilbake med et svar, ikke en gjetning.**

### WP12 — Tillit til en modell er en erklæring eieren gjør

| | |
|---|---|
| **purposeRef** | `purpose://candidate.entitetsdata.trusted-model-declaration` |
| **Utfører** | Claude (skjema) → Codex |
| **Avhenger av** | WP9 |
| **Tester** | `test.entitet.untrusted-model-refused` |
| **Artefakt til §3** | `contract/trustedmodels_v1.json` |

`trustedModels.<id>` under EntityAnchor: hvem modellen er, hvor den kjører, hva den får foreslå, når
erklæringen ble gitt. Eiersignert, inspiserbar, revokerbar. Testen dekker to tilfeller — modell
utenfor registeret, og modell som var der og er revokert.

### WP13 — Modellen foreslår, eieren signerer

| | |
|---|---|
| **purposeRef** | `purpose://candidate.entitetsdata.ai-proposes-owner-signs` |
| **Utfører** | Codex |
| **Avhenger av** | WP5, WP12 |
| **Tester** | `test.entitet.unsigned-proposal-refused` |

Forslagskøen foran batch-veien. Modellen holder aldri skriverett; den legger et forslag i kø, og køen
tømmes bare av en signatur. Prototypen i ark-oppgaven viser interaksjonen — gult til signert.

### WP14 — Chat som slår opp keypaths og endrer

| | |
|---|---|
| **purposeRef** | `purpose://candidate.entitetsdata.keypath-chat` |
| **Utfører** | Claude (skjelett) → Codex |
| **Avhenger av** | WP13 |
| **Tester** | `test.entitet.chat-keypath-lookup`, `test.entitet.chat-change-is-a-proposal` |
| **Artefakt til §3** | `skeleton/keypathchat_v1.json` |

To ting som må testes hver for seg: at chatten *finner* riktig keypath, og at den aldri skriver —
endringen havner i samme kø som WP13.

### WP15 — Flaten tilbyr faktisk de tre veiene

| | |
|---|---|
| **purposeRef** | `purpose://candidate.entitetsdata.surface-offers-three-ways` |
| **Utfører** | Claude (skjelett) → Codex (test) |
| **Avhenger av** | WP6, WP7, WP13 |
| **Tester** | `test.skeleton.purpose-actions-reachable`, `test.skeleton.no-unreachable-elements` |

Filopplasting, AI-forslag og direkte redigering skal alle ligge i `reachableActionKeypaths` — og
ingen av dem bak en `visible(when:)` i rotscope. Det var nøyaktig den feilen som gjorde Relasjoner
tom, og `SkeletonReachabilityAudit` finnes for å fange den.

**Merk:** `testNoLocalSurfaceHidesItsOwnWaysIn` er rød i dag, med vilje — Relasjoner har sju døde
seksjoner. Den må enten bli grønn i denne oppgaven, eller få en navngitt unntaksliste med en sak bak
seg. Et rødt testmål som «alle vet om» er hvordan neste feil blir usynlig.

## 3. Hva som ikke er en arbeidspakke

- **Betaling.** Avhenger av DiMyMint og DiMyMicropayments, og må gjennom
  `dimy-payment-regulatory-guardrails` før noe designes.
- **Tabellelementet.** Eies av `PDD_ark-regneark_2026-09-17`.
- **Invitasjon og registre.** Eies av `PDD_invitasjon-tillit_2026-09-15`.
- **Å gjøre `styleRole` til et temasystem.** Eies av skjelett-tråden, se
  `SKELETON_UTVIDELSESFORSLAG_2026-09-15.md` F6.

## 4. Rekkefølge jeg foreslår å levere i

| Runde | Pakker | Hvorfor sammen |
|---|---|---|
| 1 | WP1–WP2 | Grunnen. Ingenting under kan testes ærlig uten. |
| 2 | WP3–WP5 | Lese, skrive, spore — hele tilgangsflaten på én gang, én commit-pakke. |
| 3 | WP7, WP6 | Direkte redigering først (beviser signaturveien uten AI), så fil. |
| 4 | WP9–WP10, WP12 | Gateway i appen med egne nøkler og tillitsregister. |
| 5 | WP13–WP14 | Foreslå-så-signer, og chatten oppå. |
| 6 | WP8, WP15 | Generell editor og reachability til slutt, når alle veiene finnes. |
| — | WP11 | Når §6.5 er besvart. Kan komme inn hvor som helst etter runde 4. |

Commit-pakke etter hver runde, ikke etter siste arbeidspakke — `lesson.branch-is-empty-after-eight-work-packages`.
Og `git rev-parse <branch>` mot `git rev-parse origin/main` som del av hver verifikasjon som påstår
at noe ligger på en gren.

## 5. Det jeg vil legge til i verktøyet

§5 manglet åtte tester uten at noe sa fra. Regelen finnes i skillet — hvert blad skal ha minst én
test i §5 — men `purpose_dev.py validate` sjekker den ikke. Det er en tre-linjers sjekk: samle alle
`test.*`-referanser i §1, samle alle i §5, og melde differansen. Jeg foreslår å legge den inn før G3,
så neste oppgave ikke arver samme hull. Sier du nei, lar jeg det ligge.

## 6. Det jeg trenger fra deg

1. **G2** på denne planen, eller rettelser.
2. **§6.5** — Apple Intelligence-veiene. Jeg undersøker først og kommer tilbake; det er ikke et
   spørsmål du skal svare på i blinde.
3. **§6.6** fra spesifikasjonen — om admin-rollen skal kunne vises frem som begrenset. Egen oppgave
   eller her?
4. **Hvem kjører Codex.** Jeg kan skrive handoff-skriptene, men noen må fyre dem av på macOS, og
   det avgjør tempoet.
