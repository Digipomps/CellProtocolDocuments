# Swift -> Kotlin Mapping Guide (CellProtocol)

Denne guiden er et praktisk oversettelseskart fra dagens Swift-beskrivelser til en Kotlin-implementasjon.

## 1. Concurrency-modell

- Swift `actor` -> Kotlin `class` med `CoroutineScope` + tydelig serialisering (for eksempel `Mutex` eller single-threaded dispatcher per cell).
- Krav: state-endringer må være deterministiske og uten race conditions.

## 2. Intercepts og cell-API

Swift-eksempler bruker `addInterceptForGet` / `addInterceptForSet`.

Kotlin-forslag:

- `registerGet(key: String, handler: suspend (requester, keypath) -> ValueType)`
- `registerSet(key: String, handler: suspend (requester, keypath, value) -> ValueType)`

Hold dette som tydelig `Meddle`/`Emit`-grense, ikke som direkte mutable public API.

## 3. Resolver som policy-motor

Swift har en singleton-lignende resolver i eksemplene.

Kotlin-forslag:

- Eksplisitt `CellResolver`-instans injiseres i runtime/scaffold.
- All innkommende handling går via resolver før celle.
- Forbud mot bypass (ingen direkte kall til state-mutating handlers uten resolver).

## 4. ValueType og serialisering

- Modellér `ValueType` som sealed hierarchy i Kotlin.
- Unngå implicit konvertering; bruk eksplisitt mapping mellom JSON og domenetyper.
- Innfør golden test-fixtures for stabil wire-kontrakt.

## 5. Skeleton UI

- Behold JSON-kontrakt nøyaktig som spesifisert i `12_Skeleton_Spec.md`.
- Kotlin renderer kan være Compose eller annen UI-motor, men parseren må lese samme elementmodell.
- Elementkode bør være datadrevet (type + payload), ikke hardkodet per feature.

## 6. Scaffold-sammensetning

Minimumskomponenter:

- `Resolver`
- `Storage`
- `IdentityVault`
- `ReplayEngine`
- `TransportBridge`
- `Supervisor`

Kritisk regel: transport skal ikke endre semantikk, kun levere payload i riktig rekkefølge/integritet.

## 7. Portable references

For distribuert matching på tvers av runtime-installer:

- støtt lokale refs og `portableRefs-v1`
- hold slug-strategi deterministisk
- returner nok metadata til forklarbar scoring

## 8. Foreslått Kotlin leveransefaser

1. Fase A: kjernetyper + resolver + enkel local scaffold
2. Fase B: `CellConfiguration` + skeleton parser
3. Fase C: replay + transport policy + remote routing
4. Fase D: perspective matching (`14_...`) ved behov
