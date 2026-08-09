# Broens kapabiliteter uttrykt som formål

Dato: 2026-08-09
Status: kapabilitetserklæring, ment å leses av kodeassistenter før de resonnerer
om hva broen kan bære.

## Hvorfor dette dokumentet finnes

2026-08-09 leste en kodeassistent porthole-laget, observerte korrekt at det bare
abonnerer på flows, og konkluderte at **broen ikke kan sende data begge veier**.
Konklusjonen var feil. Transporten er full duplex.

Ingenting i systemet motsa den. Evnen lå implisitt i en Swift-protokoll som
ingen erklærer, ingen kan spørre om og ingen dokumenterer. Assistenten gjettet,
og gjetningen ble videreformidlet av en annen assistent uten å bli kontrollert.

Feilen var ikke slurv. Den var **å slutte fra én observert bruksmåte til en
egenskap ved arkitekturen**. Det er en feilklasse som gjentar seg så lenge
kapabiliteten er uuttalt, uansett hvor grundig den enkelte leser koden.

Derfor: broen erklærer hva den kan, i formål.

---

## F1 — Bære toveis meldinger mellom en lokal agent og et scaffold

**Kan:** Full duplex over WebSocket. `LightweightBridgeTransport` er registrert
for `ws` og `wss` gjennom `registerDefaultWebSocketBridgeTransports()`.
Protokollen er symmetrisk: `send(text:)`, `send(data:)`,
`client(_:didReceive text:)`, `client(_:didReceive data:)`, pluss
`connect`/`disconnect`/`ping`.

**Kilde:** `CellProtocol/Sources/CellBase/Cells/Bridging/LightweightBridgeTransport.swift`

**Kan ikke:** Ingen begrensning på retning i selve transporten.

> **Skille som må holdes:** at et lag *bruker* kanalen énveis i dag er ikke det
> samme som at kanalen *er* énveis. Porthole-laget abonnerer. Transporten bærer
> begge veier. Dette er hele grunnen til at dokumentet finnes.

---

## F2 — La den lokale agenten ta initiativet, aldri scaffoldet

**Kan:** Agenten registrerer seg utover med `startupMode: join` mot
`scaffold.discoveryURL`. Forbindelsen holdes åpen fra agentsiden.

**Kan ikke — og skal aldri kunne:** Scaffoldet oppretter ikke innkommende
forbindelse til agenten. En laptop bak NAT, på mobilnett eller i dvale skal
aldri måtte være naaebar fra internett.

**Hvorfor det er et formål og ikke en detalj:** retningen på *forbindelsen* og
retningen på *dataene* er to forskjellige spørsmål. Broen er toveis for data og
énveis for initiativ. Å blande dem er nettopp feilen i innledningen.

---

## F3 — Bare den identiteten som eier ressursen kan påkalle den

**Kan:** Bridgeheaden er skopet per identitet som
`bridgehead:<bridgeReference>:<requester.uuid>`.

**Kan ikke:** En kapabilitet som eksponeres over broen blir ikke
tjenesteomfattende. Én brukers lokale modell er ikke en provider for alle andre.

**Konsekvens for design:** når en lokal modell kobles på, skal den bindes til
eierens identitet — ikke registreres som en global provider i scaffoldet.

---

## F4 — Utføre bare det som er signert, ferskt og avgrenset

**Kan:** Signerte intents med utløp, styrt av `remoteIntentPolicy`
(`issuers`, `requireExpiry`, `maxClockSkewSeconds`, `maxArgumentCount`).

**Kan ikke:** Usignerte, utløpte eller ubegrensede kommandoer. Denne policyen
er en sikkerhetskontroll og skal ikke svekkes for å få noe til å virke.

---

## F5 — Degradere når motparten er borte

**Kan:** Den påkallende siden skal falle tilbake på eksisterende oppførsel når
agenten ikke er tilkoblet.

**Kan ikke:** En kapabilitet som er borte skal ikke gi feil til sluttbrukeren.

**Hvorfor dette er en kapabilitetsegenskap og ikke en implementasjonsdetalj:**
motparten er en laptop. Den sovner, mister nett og sitter på buss. Fravær er
normaltilstand, ikke unntak. En integrasjon som ikke har definert fallback, har
ikke definert kapabiliteten ferdig.

---

## Kapabilitetsnavn i bruk

| Navn | Formål | Merknad |
| --- | --- | --- |
| `cap.discover` | F2 | grunnleggende join |
| `cap.native_porthole` | F1, F3 | flate mot agenten |
| `cap.local_automation` | F3, F4 | lokal handling på eierens maskin |
| `cap.local_email_draft` | F3, F4 | |
| `cap.local_model.generate` | F1, F3, F4, F5 | lokal modell; `AgentLocalModelCell` eksponerer `llm.generate` |

Kapabilitetene forhandles gjennom scaffoldets discovery-deskriptor.
`scaffold.requestedCapabilities` i agentens `config.json` alene etablerer ikke
kontrakten — `SproutBootstrapClient` ber om det deskriptoren erklærer.

---

## Modellbinding

Bind til **provider-id**, ikke til modell: `local.gemma4.e4b.qat.mlx-vlm`.
Da kan Qwen, Gemma eller Mistral byttes uten at kallende kode endres.

Målt norsk ytelse (8 caser, 2026-06-12): Qwen3-8B Q4 79,2 %, Gemma 4 E4B QAT
MLX 75 %. Den fungerende kjøretiden er MLX/VLM QAT 4-bit.
Kilde: `Deliverables/Gemma4_Local_Runtime_Test_Log_2026-06-12.md` og
`Deliverables/Kallimachos_Norsk_Modellstrategi_2026-08-05.md`.

---

## Regelen som gjelder alle fremtidige påstander om broen

En påstand om hva broen kan eller ikke kan, skal oppgi **fil og linje**, og skal
skille mellom:

- **bevist** — transporten eller kontrakten har funksjonen;
- **brukt** — et lag benytter den i dag;
- **antatt** — ingen av delene er kontrollert.

«Broen kan ikke X» uten kilde er en antakelse, ikke et funn. Er svaret at noe
mangler, skal det pekes på hvilken funksjon eller kontrakt som mangler — ikke
gjentas som en generell egenskap.
