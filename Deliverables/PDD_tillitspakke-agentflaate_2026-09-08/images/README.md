# images/ — referansebilder for G1-GUI (PDD_tillitspakke-agentflaate)

Alle bilder er rendret **fra skeleton-JSON i `skeleton/`** av en minimal HTML-renderer (`render.html`, denne mappen)
med fixture-data for en flåte «Research-assistent» = PurposeBoundAIGateway + WebFetch + ScopedCredential.
Telefon: 390×844 @2x (full høyde). Skrivebord: 1180×860 @2x — to kolonner er *mockup-layout*, se punkt 6 under.

**Dette er mockups (skill-preferanse 2), ikke Porthole-preview (preferanse 1).** Grunn: `cell:///AgentTrustPackage`
finnes ikke ennå, så en Porthole-preview ville vist tomme bindinger for alle `trustPackage.*`-keypaths. Ekte
preview/paritet (`npm run skeleton:iterate -- --mode preview --base-url http://127.0.0.1:9089 …`) planlegges som egen
slice i P5 (`test.gui.parity`) når cellen leverer state (lesson.scaffold-without-porthole-host-has-no-preview, samme
mønster som PDD_palazzo-husk-det-jeg-sa).

| Bilde | Skeleton | Tilstand |
|---|---|---|
| tillitspakke-for-tom-v1.png | tillitspakke-for.json | ingen flåte konfigurert (lister tomme) |
| tillitspakke-for-fylt-v1.png | tillitspakke-for.json | utkast, 3 celler, rekkevidde, innsnevring, «Godkjenn pakke» |
| tillitspakke-for-feil-v1.png | tillitspakke-for.json | gjeldende policy-digest ≠ godkjent (nytt whitelist-mønster etter godkjenning) |
| tillitspakke-etter-ok-v1.png | tillitspakke-etter.json | 0 avvik, 3 kvitteringer signert/verifisert |
| tillitspakke-etter-brudd-v1.png | tillitspakke-etter.json | 2 avvik (ny destinasjon, credential forsøkt), «Stopp flåten» |
| tillitspakke-for-fylt-desktop-v1.png | tillitspakke-for.json | samme som fylt, skrivebordsbredde |
| tillitspakke-etter-brudd-desktop-v1.png | tillitspakke-etter.json | samme som brudd, skrivebordsbredde |

## Hva dagens skeleton IKKE kan rendre (og hva mockupen derfor viser annerledes)

1. **Graf.** Rekkevidde vises som rader (`List` med to `Text`), ikke som tegnet graf. Skeleton har ingen graf-/diagram-element.
2. **Farger på status og kort** (grønn/rød overskrift, rødt avvikskort, blått rekkevidde-kort, primær/fare-knapp) er
   `styleClasses`-metadata (`tp-*`) som et tema kan plukke opp; uten tema er alt nøytralt og alle knapper like.
3. **Monospace for digester** (`tp-mono`) er også `styleClasses`; rendereren garanterer ikke fast bredde.
4. **Store bokstaver på seksjonstitler** er mockup-CSS; `Section.header` rendres som vanlig overskrift.
5. **Skjulte tomme linjer** (f.eks. «Åpne instruksjon» bare på celler med instruksjon) bruker item-scoped
   `modifiers.visibility.when {scope: item, keypath: hasInstruction, equals: true}` inne i List-raden. Finnes i
   `SkeletonDescription.swift` (SkeletonVisibilityRule/SkeletonConditionExpression); må verifiseres i Porthole.
6. **To kolonner på skrivebord** er mockup-layout. Skeleton er én `VStack`; Porthole rendrer én kolonne med mindre
   flaten bygges om med `Grid`/`HStack` — ikke gjort her, fordi telefonbildet er referansen.
7. **«Åpne instruksjon» / «Åpne kvittering»** er `Button` med keypath + payload `{cellID: $id}` / `{receiptID: $id}`;
   cellen må svare med noe rendereren kan navigere til (Reference/flate). Ikke en hyperlenke.
8. **Toggle-layout** (etikett venstre, bryter høyre) er renderers valg; skeleton sier bare `Toggle{label,keypath,isOn}`.

## Må verifiseres i Porthole før P5 (står også i hver JSON under `_verify_in_porthole`)

- `Button` inne i `List`-rad med payload som bærer radens id (`$id`) — samme forbehold som husk-PDD.
- `Toggle` skriver bool til keypath; bekreft set-payload-form.
- `TextArea` med `sourceKeypath` + `targetKeypath` på samme celle (whitelist-mønstre, ett per linje).
- Item-scoped visibility inne i List-rad (punkt 5).
- `$packageDigest` i «Godkjenn pakke»-payload er fabrikk-substitusjon ved bygging, ikke runtime.
