# TranscriptStoreCell — funksjonstestplan

**Dato:** 2026-08-03 · **Celle:** `TranscriptStoreCell` (`cell:///TranscriptStore`)
**Enhetstester som allerede kjører grønt:** `CellScaffold/Tests/AppTests/TranscriptStoreCellTests.swift`, 9/9

Enhetstestene beviser at kontrakten oppfører seg riktig i isolasjon. Denne planen
dekker det de ikke kan: at cellen faktisk gjør nytte for en bruker, i den
arbeidsflyten den ble bygget for.

---

## 1. Hva som allerede er dekket, og hva som ikke er det

| Egenskap | Enhetstest | Status |
|---|---|---|
| Innhold hashes, holdes utenfor lister, leses eksplisitt | `testStoreHashesContentAndKeepsItOutOfListings` | ✅ |
| Requester-isolasjon | `testEntriesAreScopedPerRequester` | ✅ |
| Frigivelse gir innhold én gang og etterlater gravstein | `testReleaseReturnsContentOnceAndLeavesATombstone` | ✅ |
| Utløpt oppføring slettes ikke uten policy | `testExpiredEntryIsNotSweptUnlessPolicyAllowsAutoDeletion` | ✅ |
| Modus slår policy | `testKeepUntilReleasedIsNeverSweptEvenWhenPolicyPermitsDeletion` | ✅ |
| Rydding, standard og `all` | `testTidyRemovesOnlyReleasedEntriesByDefault` | ✅ |
| Byte-tak | `testStoreRejectsContentAboveTheByteCap` | ✅ |
| State og policy overlever koding | `testStoredEntriesAndPolicySurviveEncodingRoundTrip` | ✅ |
| Oppdagbar i scaffold-katalogen | `testTranscriptConfigurationIsDiscoverableInTheScaffoldCatalog` | ✅ |

**Ikke dekket, og det er dette planen handler om:**

- at cellen faktisk erstatter filskrivingen i en ekte panelkjøring
- at Porthole-flaten kan betjenes av et menneske uten forklaring
- at kontrakten er byttbar, altså at en variant kan tre inn uten at kallere endres
- at sletting virkelig sletter, også fra persistert lager
- at flow-hendelsene er nok til å revidere hva som skjedde med materialet

---

## 2. Formål og Goals

| ID | Formål | Goal (målbart ferdig-kriterium) |
|---|---|---|
| F1 | Cellen kan bære evidensen fra en panelkjøring | Alle sju runde 1-svar lagres, leses tilbake **byte-identisk**, og hashene stemmer med runnerens egne |
| F2 | De tre utgangene virker for et menneske, ikke bare for en test | En bruker som ikke har lest koden klarer frigi, kjøre opprydding og rydde fra Porthole-flaten |
| F3 | Kontrakten er faktisk byttbar | En andre implementasjon av samme kontrakt betjener de samme kallene uten at kalleren endres |
| F4 | Sletting er sletting | Etter `tidy(all)` finnes innholdet ikke i persistert tilstand |
| F5 | Oppbevaring er reviderbar | Flow-hendelsene alene forteller hva som ble lagret, frigitt, feid og ryddet |

---

## 3. Testene

### T1 — Ekte panelkjøring gjennom cellen (F1). **Høyest verdi.**

Den eneste testen som beviser at cellen løser problemet den ble laget for.

1. Kjør `run_advisory_panel.py` mot en liten spec (2 panelister, billig modell).
2. Skriv hvert verbatim svar til `transcript.store` med `sourceEndpoint: cell:///AIGateway`
   og `correlationID` lik panelets `panelID`.
3. Les hver oppføring tilbake med `transcript.read`.
4. Sammenlign byte for byte mot `responseText` i runnerens JSON.
5. Sammenlign `contentHash` mot runnerens `responseHash`.

**Består når:** alle svar er byte-identiske og alle hasher er like.
**Feiler stygt hvis:** normalisering, klipping eller tegnsett-konvertering endrer
noe. Det ville gjøre cellen ubrukelig som evidenslager, og det er nettopp
grunnen til å teste dette først.

### T2 — Menneskelig gjennomgang i Porthole (F2)

Ikke skriptet. En person som ikke har lest denne koden får oppgaven:
«Du har fem lagrede transkripsjoner. Behold én, flytt én ut, og bli kvitt resten.»

Observer uten å hjelpe. Noter hvert sted personen nøler eller velger feil.

**Består når:** oppgaven fullføres uten at noen forklarer forskjellen på
`release`, `sweep` og `tidy`.
**Dette er testen jeg forventer at feiler først** — tre utganger med
overlappende betydning er lett å forstå i kode og vanskelig i et grensesnitt.
Et negativt resultat her er et designfunn, ikke en feil i implementasjonen.

### T3 — Variantbytte (F3)

Poenget med å skille cellen ut. Skriv en `EphemeralTranscriptStoreCell` som
implementerer nøyaktig `TranscriptStoreContract` men aldri persisterer.

1. Kjør T1s lagre/les-sekvens mot den, uten å endre kallerkoden — bare endepunktet.
2. Verifiser at alle seks action-keypath-er svarer med samme statusverdier.
3. Verifiser at `transcript.sweep` på varianten respekterer samme policyregel.

**Består når:** kallersiden er uendret bortsett fra endepunktet.
**Hvis den feiler:** kontrakten lekker implementasjonsdetaljer, og
byttbarheten — hele begrunnelsen for en egen celle — er ikke reell.

### T4 — Sletting når helt ned (F4)

1. Lagre en oppføring med en kjent, søkbar streng.
2. Kod cellen, bekreft at strengen finnes i den kodede formen.
3. `transcript.tidy` med `scope: all`.
4. Kod på nytt, søk etter strengen igjen.

**Består når:** strengen er borte fra den nye kodede formen.
**Merk:** dette tester cellens eget lager, ikke sikkerhetskopier eller
lagringslag under. Den avgrensningen skal stå i resultatet — «slettet fra
cellen» er ikke «slettet fra maskinen», og rapporten må ikke antyde noe annet.

### T5 — Revisjon fra flow alene (F5)

Kjør en full livssyklus: lagre tre, frigi én, la én utløpe og feie den,
rydd resten. Ta så **kun** flow-hendelsene (`transcript.stored`,
`transcript.released`, `transcript.swept`, `transcript.tidied`,
`transcript.policy.updated`) og rekonstruer hva som skjedde.

**Består når:** rekonstruksjonen stemmer med den faktiske sekvensen, inkludert
hvilken policy som gjaldt da feiingen kjørte.

### T6 — Grenser under press

Rask, men verdt å ha:

- `maxEntriesPerRequester` nås → `store_full`, og feilen sier hva brukeren skal gjøre
- Samtidig `store` og `sweep` fra flere tasks → ingen krasj, ingen tapt oppføring
  (`stateQueue` skal holde, men det er ikke bevist under samtidighet)
- `ttlSeconds` = 0 og negativ → oppføringen er umiddelbart utløpt, ikke evig

---

## 4. Rekkefølge og hva som stopper hva

```
T1 ──► T3 ──► T2
 │      │
 └─► T4 └─► T5 ──► T6
```

**T1 først.** Feiler den, er resten uten mening.
**T3 før T2**, fordi et variantbytte kan tvinge kontraktsendringer som gjør
grensesnittet om igjen — og da må T2 kjøres på nytt uansett.
**T2 sist av de tre**, fordi den krever et menneske og ikke kan gjentas billig.

---

## 5. Kjente begrensninger som skal med i resultatet

Disse er allerede kjent og skal ikke rapporteres som overraskelser:

| Begrensning | Konsekvens |
|---|---|
| En dekodet celle re-registrerer ikke keypath-ene sine, fordi `restoreOwner` ikke finner eier i nyttelasten. Gjelder hele WebKnowledge/PersonalCopilot-familien, ikke bare denne cellen | Persistert *tilstand* overlever; *kontrakten* må reetableres av verten. `ensureReady()` finnes, men hjelper bare når eier faktisk ble kodet |
| Lagring er i minne med Codable-persistens, ikke et lagringslag med egne slettegarantier | T4 tester cellen, ikke disken |
| Ingen kryptering i ro | En variant som krypterer er nettopp det kontraktsskillet er til for |

---

## 6. Hva som ikke skal testes her

- Om `AIGatewayCell` bør kalle denne cellen. Det er integrasjonsarbeid og hører
  til migreringen beskrevet i `AIGatewayCell_Panel_Readiness_2026-08-03.md`.
- Om retensjonsvokabularet er riktig modellert mot GDPR eller
  `personal-data-trust-package`. Det er en egen gjennomgang.
- Ytelse på store transkripsjoner. Byte-taket gjør dette uinteressant inntil
  taket heves.
