# Butterpop Studio: knappen brukeren ikke kan bruke

Egen tråd, startet 2026-10-02 av Losen etter Kjetils beskjed: «Legg Butterpop Studio-knappen til annen tråd - start den om du kan.» Den hører ikke til PDD palazzo-tolkning-og-vektjustering.

## Intensjon (P0)

Flaten «Butterpop Studio» i HAVEN (Binding) har en knapp, «Åpne Butterpop Studio», som brukeren ikke kan bruke. Den skal enten virke eller ikke stå der.

## Formål (forslag, ikke godkjent av Kjetil)

- purpose://butterpop.open-studio-reachable: den som åpner flaten Butterpop Studio, kan komme videre til studioet med knappen.
  - Mål: `SkeletonReachabilityAudit.reachableActionKeypaths` inneholder knappens handling, og `testNoLocalSurfaceHidesItsOwnWaysIn` er grønn for alle 20 flater.
- pkg.std.everything-works: bygg, full BindingTests, dokumentasjon i samme endring.

## Det som er observert

- Binding `origin/main` 8ce634f, `BindingTests.CellConfigurationVerifierXCTest.testNoLocalSurfaceHidesItsOwnWaysIn`: «1 of 20 surfaces hide part of themselves: Butterpop Studio: 1 unreachable element(s) [missingRequiredAction] ScrollView[0].VStack[1].Section[2].HStack[0].Button — Button requires keypath or keypathKeypath.»
- Kilden er `Cells/ConfigurationCatalogCell.swift`, `butterpopStudioMenuConfiguration()`: `personalActionButton(keypath: "", label: "Åpne Butterpop Studio", url: "/butterpop", payload: nil)`.
- Feilen er lik før og etter CellProtocol-pinnen 253b4af (WP7, `HAVEN-Deploy/_handoff/PALAZZO-VEKT/wp7-20260930T202115Z`).

## Avgjort av Kjetil 2026-10-03

«Rett kontrollen»: knappen er en gyldig lenke-knapp. Kontrollen i CellProtocol skal lære at en knapp med lenke og uten cellehandling er navigasjon, og telle den som nåbar. Endringen går gjennom portene, og Kjetil sier ja før main.

## Formål etter avgjørelsen

- purpose://skeleton.reachability-knows-navigation: reachability-auditten gjengir den navigasjonskontrakten rendereren allerede har (`SkeletonButtonNavigation`): tom `keypath` og ikke-tom `url` er navigasjon.
  - Mål 1: en slik knapp gir ikke `missingRequiredAction`.
  - Mål 2: auditten oppgir navigasjonsmålet, slik at en test kan kreve at «Åpne Butterpop Studio» er nåbar.
  - Mål 3: en knapp uten både handling og lenke gir fortsatt `missingRequiredAction`. Auditten svekkes ikke.
- purpose://butterpop.open-studio-reachable (som over): måles i Binding når pinnen er løftet til den nye CellProtocol-commiten.

## Åpent (fra før avgjørelsen)

- Hva knappen skal gjøre: åpne en URL (`/butterpop`), bytte flate, eller kalle en handling på `MusicPublishingConsoleCell`. Codex undersøker hva andre knapper med `url:` gjør og hva rendereren støtter, og foreslår.
- Viser det seg at svaret krever en ny kapabilitet i skjelettformatet, stopper arbeidet og Kjetil blir spurt.

## Status

Se `STATUS.md` i denne mappen.
