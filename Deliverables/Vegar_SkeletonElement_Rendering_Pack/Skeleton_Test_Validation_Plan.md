# Skeleton Test & Validation Plan

## 1. Testmål

Verifisere at parser, resolver-integrasjon og renderer følger Skeleton-spesifikasjonen og er stabile i produksjon.

## 2. Testkategorier

### 2.1 Decoder/encoder contract tests

- Parse av alle støttede elementtyper.
- Avvisning av ugyldig top-level (ikke single-key).
- `Object` wrapped decode + legacy unwrapped decode.
- `flowElementSkeleton` canonical decode + legacy alias decode.
- Re-encode til canonical form.

### 2.2 Modifier tests

- Hver modifier påvirker forventet UI-atferd.
- Kombinasjonstester: size + padding + alignment + style.
- Ugyldige verdier skal ikke krasje renderer.

### 2.3 Dynamic data tests

- `Text.keypath` med gyldig/ugyldig path.
- `Text.url` resolver success/failure.
- `Button` med og uten payload (set/get-ruting).
- `Toggle` writeback + revert ved feil.

### 2.4 Collection/layout tests

- `VStack`/`HStack` child order bevares.
- `List` med `flowElementSkeleton` item-template.
- `Grid` kolonnedefinisjoner (fixed/flexible/adaptive).
- `Section` header/content/footer variasjoner.

### 2.5 Regression tests

- Snapshot/UI-tester for representative skjermer.
- Golden JSON fixtures beholdes versjonert.
- Regressions ved parserendringer stoppes i CI.

## 3. Foreslåtte fixtures i denne pakken

- `fixtures/text_static.json`
- `fixtures/vstack_basic.json`
- `fixtures/list_with_template.json`
- `fixtures/object_wrapped.json`
- `fixtures/object_legacy_unwrapped.json`
- `fixtures/reference_feed.json`
- `fixtures/interactive_controls.json`

## 4. CI-gating (minimum)

- Alle contract tests må passere.
- Ingen ukjente node-typer i produksjonsfixtures.
- Snapshot-diff må godkjennes eksplisitt.
- Feil i resolver-mocktester blokkerer merge.

## 5. Observability-krav under test

Logg per testkall:

- parse duration
- resolve duration
- render duration
- node count
- warnings/errors per node type

## 6. Feilsøkingsstrategi

Hvis test feiler:

1. isoler node som feiler (path + type)
2. valider fixture-format mot single-key-regelen
3. sjekk canonical felt og legacy alias-håndtering
4. kjør resolver-mock separat for å skille I/O-feil fra render-feil
5. sammenlikn snapshot med siste godkjente baseline

## 7. Done-definition før utrulling

- Decoder coverage for alle elementtyper i kapittel 12.
- 0 krasj på ugyldige noder (graceful fallback).
- Konsekvent rendering i minst to plattformer/enheter.
- Dokumentert fallback-policy for resolver-feil.
