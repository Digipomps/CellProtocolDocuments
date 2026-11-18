# Dataflyt — modellvalg og læring i AI-hjelperen

Skrevet 2026-11-18, fra koden i CellScaffold-grenen `claude/project-thread-fkjjgp`.

```
Developer Workbench (skjelett)
  │  models.setDraft* · models.add (nøkkel fra skjult felt) · models.use · models.test · models.remove
  │  learning.toggle · learning.remove · learning.clear · learning.exportTestSet · learning.suggestWords
  │  helper.ask · helper.accept · helper.discard · helper.undo
  ▼
WorkbenchHelper ──create · issueKeyInput · writeKey · secret · remove──► BYOK-lageret
  │                                                   └──forseglet under reservert alias──► OwnerScopedCredentialStore
  │  (bare når reglene ikke forstår bestillingen, og en modell er valgt)
  ├──invokeWithHostedKey(rute fra oppsettet, eierens nøkkel)──► AIGateway ──HTTPS, vert i egress-listen──► leverandøren
  │  ◄── tekst, eller feillinjer («HTTP 401: …») ──┘
  ├──setStatus × N──► WorkItem   (uendret fra forrige PDD)
  └──eksempel {bestilling, sett, modell, svar, handling, formål, utfall}──► egen tilstand (eierens entitet)
```

| Kant | Fra | Til | Keypath / kall | Kontrakt |
|---|---|---|---|---|
| 1 | Developer Workbench | WorkbenchHelper | `models.*` | `contract/models-state.v0.example.json`, `WorkbenchHelperCell.swift` |
| 2 | Developer Workbench | WorkbenchHelper | `learning.*` | `contract/learning-example.v0.example.json`, `contract/testset.v0.example.json` |
| 3 | WorkbenchHelper | BYOK-lageret | `create`, `issueKeyInput`, `writeKey`, `secret`, `remove`, `list`, `read` | `ButlerProviderConfigurationStore.swift`, `ButlerProviderConfigurationContract.swift` |
| 4 | BYOK-lageret | OwnerScopedCredentialStore | `upsert`, `secret`, `remove` under alias `butler-byok-<configID>` | `OwnerScopedCredentialStore.swift` |
| 5 | WorkbenchHelper | AIGateway | `invokeWithHostedKey` | `AIGatewayCell.swift`; ruten bygges i `WorkbenchHelperProviders.request` |
| 6 | AIGateway | leverandøren | `https://api.anthropic.com/v1/messages`, `https://api.openai.com/v1/responses`, `https://api.mistral.ai/v1/chat/completions` | `AIGatewayEgressPolicy` (uendret) |

Det som krysser grensen ut av HAVEN er bestillingen, settets instruksjoner og listen over
handlinger (kant 6), og bare til leverandøren eieren har valgt. Nøkkelen går i kant 3–6 og
ligger aldri i kant 1–2 tilbake til flaten. Eksemplene forlater ikke cellen før eieren
eksporterer; eksporten vises i flaten og sendes ingen steder.

Ikke bygget i denne runden: kanten til `cell:///PurposeQualityMonitor`
(`quality.compareChatPrompts`). Testsettet har formen den cellen leser; kjøringen (T-L3)
gjøres på eksempler fra staging. I flaten måles treffraten med regelmotoren selv.
