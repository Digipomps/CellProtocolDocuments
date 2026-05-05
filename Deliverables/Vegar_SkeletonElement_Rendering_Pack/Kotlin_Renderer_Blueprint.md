# Kotlin Renderer Blueprint (SkeletonElement)

## 1. Mål

Implementere en Kotlin-basert renderer (typisk Jetpack Compose) som er kompatibel med Skeleton-specen og robust nok for produksjon.

## 2. Foreslått arkitektur

- `SkeletonParser`
  - input: JSON
  - output: `SkeletonElement` sealed model
- `SkeletonResolver`
  - ansvar: keypath/url/cell-oppslag via resolver-adapter
- `SkeletonRenderer`
  - ansvar: map elementmodell til Compose UI
- `ModifierMapper`
  - ansvar: map JSON modifiers -> Compose `Modifier` + style
- `SkeletonRuntime`
  - orkestrerer parse -> resolve -> render, logging, feilpolicy

## 3. Sealed model (skisse)

```kotlin
sealed interface SkeletonElement {
    data class Text(...): SkeletonElement
    data class TextField(...): SkeletonElement
    data class Image(...): SkeletonElement
    data class Spacer(...): SkeletonElement
    data class HStack(val elements: List<SkeletonElement>): SkeletonElement
    data class VStack(val elements: List<SkeletonElement>): SkeletonElement
    data class ListElement(...): SkeletonElement
    data class ObjectElement(...): SkeletonElement
    data class Reference(...): SkeletonElement
    data class Button(...): SkeletonElement
    data class Divider(...): SkeletonElement
    data class ScrollView(...): SkeletonElement
    data class Section(...): SkeletonElement
    data class ZStack(...): SkeletonElement
    data class Grid(...): SkeletonElement
    data class Toggle(...): SkeletonElement
}
```

## 4. Parser-strategi

- Parse hvert nodeobjekt som `Map<String, JsonElement>`.
- Valider at map har nøyaktig 1 nøkkel.
- Dispatch på nøkkel (`Text`, `VStack`, osv.).
- For `Object`: støtt både wrapped og legacy unwrapped decode.
- For `flowElementSkeleton`: les både canonical + legacy alias i decode.

Pseudo:

```kotlin
fun parseNode(obj: JsonObject): SkeletonElement {
    require(obj.size == 1) { "Skeleton node must be single-key" }
    val (type, payload) = obj.entries.single()
    return when (type) {
        "Text" -> parseText(payload)
        "VStack" -> VStack(parseChildren(payload))
        // ...
        else -> UnknownNode(type, payload)
    }
}
```

## 5. Resolver-adapter

Definer et rent grensesnitt mot CellResolver:

```kotlin
interface CellDataGateway {
    suspend fun get(keypathOrUrl: String): ValueType?
    suspend fun set(keypathOrUrl: String, payload: ValueType): ValueType?
    suspend fun subscribe(ref: ReferenceSpec): Flow<ValueType>
}
```

- UI-laget kjenner kun gateway, ikke transportdetaljer.
- `cell://` normalisering legges her.

## 6. Compose-mapping

- `Text` -> `Text(...)`
- `TextField` -> `TextField(...)` med lokal state + commit handler
- `Image` -> `Image(...)` / async image loader
- `HStack` -> `Row`
- `VStack` -> `Column`
- `List` -> `LazyColumn`
- `ZStack` -> `Box`
- `Grid` -> `LazyVerticalGrid`
- `Toggle` -> `Switch`
- `Divider` -> `Divider`
- `ScrollView` -> `Column` + `verticalScroll` / row + `horizontalScroll`
- `Section` -> composable wrapper med header/content/footer

## 7. Modifier mapping

Lag én sentral mapper i stedet for per-element duplisering.

- layout: width/height/padding/alignment
- style: colors/opacity/font
- decoration: corner/border/shadow
- behavior: hidden

Anbefaling: skil ut tekstspesifikke style-felt (`fontSize`, `fontWeight`) fra generelle layout modifiers.

## 8. State og sideeffekter

- Parse-fasen er ren.
- Resolve-fasen gjør I/O (get/set/subscription).
- Render-fasen er sideeffektfri, bortsett fra brukerhandlinger (`Button`, `Toggle`, `TextField`).

Bruk `remember`/`LaunchedEffect` kontrollert for dynamiske noder.

## 9. Feilpolicy

- Unknown type: render `UnknownNodePlaceholder` i debug, no-op i release.
- Decode-feil i child node: hopp over node, fortsett med siblings.
- Resolver timeout: vis fallback + retry-mulighet.

## 10. Performance

- Cache parse-resultat per skeleton hash.
- Cache resolved data per keypath/url med TTL der semantikk tillater.
- Bruk stable keys i list/grid for å minimere recomposition.
- Instrumenter latency parse/resolve/render.

## 11. Anbefalt API mot resten av appen

```kotlin
@Composable
fun SkeletonView(
    skeletonJson: String,
    gateway: CellDataGateway,
    userContext: Map<String, Any?> = emptyMap(),
    onError: (Throwable) -> Unit = {}
)
```

Dette gjør det enkelt å teste og å bytte runtime-gateway i ulike miljøer.

## 12. Leveransekriterier

- Samme JSON-fixtures dekoder identisk i alle miljøer.
- Element-type coverage = 100% mot kapittel 12.
- Snapshot-tester verifiserer sentrale layouts.
- Resolver-integrasjon har kontraktstester for `get/set/subscribe`.
