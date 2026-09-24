# 36 — Formålssammensetning (purpose composition)

Status: **forslag, venter Kjetils ord.** Skrevet 2026-09-09.
Endrer ikke Book 23 kanonisk; se `changePolicy` i
`Book/haven_purpose_knowledge_base_v0.json`.

---

## 1 Hullet

`Book/haven_purpose_knowledge_base_v0.json` har 57 noder. Hver node har
`parentRef`. `compatibility.model` er
`single-parent-tree-with-cross-cutting-facets`.

**Ingen node sier hva det betyr at den er oppfylt gitt barna sine.** Søk etter
`allOf`, `anyOf`, `oneOf`, `sequence`, `composition` eller `nOf` i
kunnskapsbasen, i `Book/haven_purpose_packages_v0.json` og i
`Tools/PurposePackages/purpose_dev.py` gir null treff.

Konsekvensen er ikke teoretisk. Alle antar stilltiende «alle barna må
oppfylles», og en stilltiende antakelse har ingen port. Commiten `ba14895` i
HavenAgentD landet correspondence-MCP-en uten `AgentIdentityStore`-endringen
den er avhengig av, og passerte, fordi ingenting sa hva helheten krevde.

---

## 2 Regelen

> **`composition` er påkrevd på hver ikke-løvnode. Ingen default.**
> En forelder uten `composition` stryker på `purpose_dev.py validate`.

Ingen default, med vilje. En default gjenoppretter nøyaktig dagens tilstand,
der alle antar `allOf` uten at noen har sagt det.

---

## 3 Kombinatorene

### 3.1 `allOf`

Alle barn må være grønne. Rekkefølge er likegyldig; barna kan forsøkes
parallelt.

    "composition": { "kind": "allOf" }

### 3.2 `sequence`

Barna i den rekkefølgen de er definert. Et senere barn **kan ikke forsøkes**
før forrige er verifisert grønt.

Dette er ikke en avhengighetsannotasjon — det er en kontrollsetning. Forskjellen
er at `allOf` med rekkefølgehint tillater at et senere steg startes og feiler;
`sequence` forbyr at det startes.

    "composition": { "kind": "sequence" }

Eksempel: `Deliverables/Handoff_Correspondence_Til_Main_2026-09-09.md` WP-1..WP-7.
Skrevet som prosa fordi konstruksjonen ikke fantes.

### 3.3 `anyOf`

Minst `min` barn må være grønne. `min` er default 1.

    "composition": { "kind": "anyOf", "min": 1 }

`min` lik antall barn er semantisk identisk med `allOf`; foretrekk `allOf` da,
av lesbarhetshensyn. `min` > 1 dekker kvorum og gjør en egen `nOf` unødvendig.

Eksempel: «les faktisk tilstand på staging» kan oppfylles av SSH-inventar,
deploy-CLI eller en statusflate — hvilken som helst holder. Codex stoppet
2026-09-09 fordi det ikke fantes noen måte å uttrykke det på.

### 3.4 `firstOf`

Preferanseordnet disjunksjon. Prøv barna i definert rekkefølge; første grønne
avslutter samlingen. **Hvilken gren som ble tatt skal registreres** i
resultatet — en `firstOf` uten registrert gren er ikke verifisert.

    "composition": { "kind": "firstOf" }

Forskjellen fra `anyOf`: `anyOf` er likegyldig til hvilket barn som lyktes,
`firstOf` er det ikke.

Eksempel: `codex-collaboration`-skillen har allerede dette i prosa — «the only
routes are, in order: 1. MCP, 2. computer use, 3. file handoff».

### 3.5 `invariant`

Barna er ikke steg, men betingelser som må holde **før og etter hvert** steg i
foreldrenoden. Brudd stopper hele samlingen umiddelbart; ingenting rulles
tilbake automatisk.

    "composition": { "kind": "invariant", "over": "<purposeRef>" }

`over` peker på samlingen invarianten gjelder for.

Eksempel: «ingen commit som brekker noe når `origin/main`». Dette er ikke et
steg i en sekvens — det gjelder over alle steg, og er nøyaktig porten `ba14895`
ville strøket på.

### 3.6 Negative formål

Ikke en kombinator. `prohibited` finnes allerede som nodestatus og brukes
uformelt, f.eks. `…root.no-attachments-on-plaintext-path` i
`Deliverables/PDD_correspondence-vedlegg_2026-09-04/FORMAALSSPEC.md`.
Formaliseres som status, ikke som samling.

---

## 4 Verifikasjon

En samling er grønn bare når dens `composition` sier den er det. Reglene:

| kind | grønn når |
|---|---|
| `allOf` | hvert barn grønt |
| `sequence` | hvert barn grønt, og hvert barn ble forsøkt etter at forrige var grønt |
| `anyOf` | minst `min` barn grønne |
| `firstOf` | ett barn grønt, og grenen er registrert |
| `invariant` | betingelsen holdt ved hver måling, før og etter hvert steg i `over` |

En samling der et barn er `blocked` er ikke grønn. `blocked` er ikke `red`, men
det er heller ikke `green` — det skal rapporteres som sin egen tilstand med
årsak, aldri rundes av.

---

## 5 `validate`-krav

`Tools/PurposePackages/purpose_dev.py validate` skal avvise:

1. ikke-løvnode uten `composition`
2. `sequence` der barnas rekkefølge ikke er entydig definert
3. `anyOf` med `min` større enn antall barn
4. `firstOf` som er rapportert grønn uten registrert gren
5. `invariant` uten `over`, eller med `over` som peker utenfor treet
6. en samling rapportert grønn i strid med tabellen i §4

---

## 6 Hva dette ikke løser

Kombinatorene sier hva som må være oppfylt. De sier ingenting om hvorvidt
verifikatoren faktisk måler det den påstår. En `allOf` med tre grønne barn hvis
verifikatorer er selvrapporterte påstander, er like verdiløs som ingen struktur.

Regelen fra `34_Audio_Analysis_Cell.md` gjelder uendret og er den egentlige
bæreren: **en måling, en slutning og en mening er tre forskjellige slags
påstand og skal aldri dele felt.**
