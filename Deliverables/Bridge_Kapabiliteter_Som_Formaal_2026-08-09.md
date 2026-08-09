# Broens kapabiliteter uttrykt som formål

Dato: 2026-08-09
Status: kildeforankret kapabilitetsnotat. Dokumentet skiller mellom egenskaper
i transporten, policy i endepunktene og ønsket produktatferd.

## Hvorfor dette dokumentet finnes

2026-08-09 leste en kodeassistent porthole-laget, observerte korrekt at det bare
abonnerer på flows, og konkluderte at **broen ikke kan sende data begge veier**.
Konklusjonen var feil. Transporten er full duplex.

Ingen kontrollert kilde ble brukt til å motsi den. Evnen lå implisitt i en
Swift-protokoll og var ikke erklært i dokumentasjonen assistenten leste.
Gjetningen ble derfor videreformidlet uten kildekontroll.

Feilen var ikke slurv. Den var **å slutte fra én observert bruksmåte til en
egenskap ved arkitekturen**. Det er en feilklasse som gjentar seg så lenge
kapabiliteten er uuttalt, uansett hvor grundig den enkelte leser koden.

Derfor: broen erklærer hva den kan, i formål.

---

## F1 — Bære toveis meldinger mellom en lokal agent og et scaffold

**Dokumentert i transporten:** Full duplex over WebSocket.
`LightweightBridgeTransport` er registrert
for `ws` og `wss` gjennom `registerDefaultWebSocketBridgeTransports()`.
Protokollen er symmetrisk: `send(text:)`, `send(data:)`,
`client(_:didReceive text:)`, `client(_:didReceive data:)`, pluss
`connect`/`disconnect`/`ping`.

**Kilde:** `CellProtocol/Sources/CellBase/Cells/Bridging/LightweightBridgeTransport.swift`

**Avgrensning:** Retning begrenses ikke av selve transportgrensesnittet. Det
beviser ikke at alle høyere protokoller eller registrerte Cells eksponerer
handlinger i begge retninger.

> **Skille som må holdes:** at et lag *bruker* kanalen énveis i dag er ikke det
> samme som at kanalen *er* énveis. Porthole-laget abonnerer. Transporten bærer
> begge veier. Dette er hele grunnen til at dokumentet finnes.

---

## F2 — La den lokale agenten ta initiativet til nettforbindelsen

**Dokumentert i gjeldende AgentD-integrasjon:** Agenten starter `sprout
bootstrap join` mot `scaffold.discoveryURL`, og native-porthole-dokumentasjonen
beskriver agenten som klient uten innkommende lyttepunkt.

**Produktkrav:** Scaffoldet skal ikke kreve at den lokale agenten aksepterer en
innkommende nettforbindelse. En laptop bak NAT, på mobilnett eller i dvale skal
ikke måtte være nåbar fra internett. Dette er en begrensning i den aktuelle
integrasjonen, ikke en generell egenskap ved alle mulige bridge-transporter.

**Hvorfor det er et formål og ikke en detalj:** retningen på *forbindelsen* og
retningen på *dataene* er to forskjellige spørsmål. Broen er toveis for data og
énveis for initiativ. Å blande dem er nettopp feilen i innledningen.

---

## F3 — Bevare identitets- og kontraktsgrenser rundt en lokal ressurs

**Dokumentert i scaffold-integrasjonen:** Bridgeheaden får et
identitetsdomene på formen `bridgehead:<bridgeReference>:<requester.uuid>`.
Native local-model-sesjonen registrerer også avtalens capability grants og
utløp.

**Viktig sikkerhetsgrense:** Dette navneskopet er ikke alene et bevis på at bare
eieren kan påkalle ressursen. Autorisasjon må håndheves av resolver,
adgangskontrakt og endepunktpolicy. Besittelse av WebSocket-kanalen er ikke en
kapabilitet. En lokal modell skal derfor ikke registreres som en global
provider, og tester må vise at andre identiteter avvises.

**Konsekvens for design:** Når en lokal modell kobles på, skal den bindes til
eierens verifiserte Entity/identitet og en tidsavgrenset avtale. Transportlaget
skal ikke eie eller omgå denne policyen.

---

## F4 — Verifisere signerte, ferske og avgrensede remote intents

**Dokumentert i AgentD:** `RemoteIntentVerifier` kontrollerer issuer, tillatte
topics og action-ID-er, signatur, tidsstempler, utløp og argumentgrenser etter
`remoteIntentPolicy`
(`issuers`, `requireExpiry`, `maxClockSkewSeconds`, `maxArgumentCount`).

**Avgrensning:** Denne kontrollen ligger i AgentD, ikke i
`LightweightBridgeTransport`. Andre konsumenter av transporten får ikke samme
garanti automatisk. For AgentD skal usignerte, utløpte, ikke-tillatte eller for
store intents avvises, og policyen skal ikke svekkes for å få en integrasjon til
å virke.

---

## F5 — Degradere når motparten er borte

**Dokumentert for native local-model-flyten:** Integrasjonsnotatet krever at
Butler fortsetter med eksisterende provider-valg når agenten sover, kobles fra,
har utløpt kontrakt, feiler eller gir timeout.

**Avgrensning:** Dette er ikke en generell transportgaranti. Hver konsument må
implementere og teste fallback; fravær av motpart kan ellers fortsatt bli en
brukersynlig feil.

**Hvorfor dette er en kapabilitetsegenskap og ikke en implementasjonsdetalj:**
motparten er en laptop. Den sovner, mister nett og sitter på buss. Fravær er
normaltilstand, ikke unntak. En integrasjon som ikke har definert fallback, har
ikke definert kapabiliteten ferdig.

---

## Kapabilitetsnavn i bruk

| Navn | Formål | Merknad |
| --- | --- | --- |
| `cap.discover` | F2 | grunnleggende join |
| `cap.native_porthole` | F1, F3 | transportflate; autorisasjon må håndheves utenfor transporten |
| `cap.local_automation` | F3, F4 | lokal handling; krever eksplisitt endepunktpolicy |
| `cap.local_email_draft` | F3, F4 | krever eksplisitt endepunktpolicy |
| `cap.local_model.generate` | F1, F3, F4, F5 | lokal modell; `AgentLocalModelCell` eksponerer `llm.generate` |

`scaffold.requestedCapabilities` sendes av `SproutBootstrapClient` som en
forespørsel til bootstrap-flyten. En forespørsel etablerer ikke i seg selv en
grant eller adgangskontrakt; dette må avgjøres og håndheves av discovery-/
resolver-flyten.

---

## Modellbinding

Bind til **provider-id**, ikke til modell: `local.gemma4.e4b.qat.mlx-vlm`.
Da kan Qwen, Gemma eller Mistral byttes uten at kallende kode endres.

Et lokalt notat rapporterer norsk ytelse fra åtte caser 2026-06-12: Qwen3-8B
Q4 79,2 % og Gemma 4 E4B QAT MLX 75 %. Dette er en liten intern måling, ikke en
generell kvalitetsbenchmark. Notatene beskriver MLX/VLM QAT 4-bit som den
verifiserte kjøretiden i den testen.
Kilde: `Deliverables/Gemma4_Local_Runtime_Test_Log_2026-06-12.md` og
`Deliverables/Kallimachos_Norsk_Modellstrategi_2026-08-05.md`.

---

## Regelen som gjelder alle fremtidige påstander om broen

En påstand om hva broen kan eller ikke kan, skal oppgi **fil og relevant symbol
eller linje**, og skal
skille mellom:

- **dokumentert** — koden eller en test viser den avgrensede funksjonen;
- **brukt** — et lag benytter den i dag;
- **krav** — ønsket atferd som må ha separat implementasjon og test;
- **antatt** — ingen av delene er kontrollert.

«Broen kan ikke X» uten kilde er en antakelse, ikke et funn. Er svaret at noe
mangler, skal det pekes på hvilken funksjon eller kontrakt som mangler — ikke
gjentas som en generell egenskap.

## Kontrollerte kodepunkter

- `CellProtocol/Sources/CellBase/Cells/Bridging/LightweightBridgeTransport.swift`:
  `LightweightWebSocketClient`, `sendData`, `client(_:didReceive:)` og `setup`.
- `CellProtocol/Sources/CellBase/Cells/CellResolver/CellResolverProtocol+LightweightBridgeTransport.swift`:
  registrering av `ws` og `wss`.
- `CellScaffold/Sources/App/Controllers/VaporSproutResolver.swift` og
  `VaporBridgehead.swift`: native-porthole-kontrakt, sesjonsgrants og
  identitetsdomene.
- `Binding/HavenAgentD/Sources/HavenAgentRuntime/SproutBootstrapClient.swift`:
  `bootstrap join`, discovery-URL og requested capabilities.
- `Binding/HavenAgentD/Sources/HavenAgentRuntime/RemoteIntentVerifier.swift` og
  `Docs/NativeLocalModelReverseRPC.md`: AgentD-policy og lokalmodell-fallback.
