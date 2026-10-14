# STATUS — rekkefølge i publisert liste

2026-10-06 · punkt 3 av seks

## Porter
- G1: dekket av at Kjetil godkjente rekkefølgen på arbeidet og sa «gjør det nå» 2026-10-05
- G1-GUI: **venter på Kjetil** — `images/rekkefolge-v1.png`
- G2/G3: ikke egne porter; lite nok til å gå rett på når bildet er godkjent

## Valg som ligger i bildet
- Ny fane «Utgivelser» i Studio. Sju faner; på telefon fire og tre.
- En ny sang legges øverst til den blir flyttet.
- Piler, ikke dra-og-slipp.
- Samme rett som å publisere (`release.publish`).

## Skrevet (gren `pdd/rekkefolge-i-publisert-liste`, av `origin/main` @ e5c34345, tupp `19c2b198`)
- `MusicCatalogOrdering` i `Sources/App/Cells/MusicPublishing/MusicPublishingSupport.swift`:
  ren logikk som leser en innsendt rekkefølge og legger lista ut.
- `MusicLibraryCell`: lagrer `catalogOrder`, bruker den i `publicCatalog`, ny nøkkel
  `setCatalogOrder`.
- `MusicReleasePipeline.setCatalogOrder` og arbeidsromshandlingen `setCatalogOrder`
  (krever `release.publish`), ført opp i kontrollerens liste over handlinger.
- To tester i `Tests/AppTests/MusicPublishingCellsTests.swift`.

## Ikke skrevet
- Flaten: fanen, lista med piler, lagring. Venter på G1-GUI.
- Test av handlingen gjennom arbeidsrommet og ruta. `MusicUsageStatisticsTests` kjører
  i CI og har mønsteret (hel app, innlogget bruker); den testen er ikke skrevet.

## Hvordan det er kjent

| Hva | Hvordan det er kjent |
|---|---|
| Koden kompilerer | **Ikke sjekket.** Ingen Swift-kompilator der dette ble skrevet. Jobb `04-rekkefolge-bygg-og-test` i `CellScaffold/_losen-jobber/` bygger og tester på Mac-en, og pusher ingenting |
| Ingen nye syntaksfeil | **Sett**: tree-sitter-swift mot de seks filene, sammenlignet med utgavene på main — ingen nye feilnoder. Det er ikke kompilatoren og finner ikke typefeil. Sjekken slo ut da en klamme ble tatt bort |
| Literal-gaten | **Sett**: kjørt i Losens VM mot hele `Sources` på grenen, grønn |
| Testene består, og feiler uten fiksen | **Ikke sjekket.** Jobb 04 har tre negative kontroller med hver sin forventede melding |
| Lytterens rute bevarer rekkefølgen | **Utledet**: `catalogWithCurrentPricing` i kontrolleren går gjennom sangene med `map`, som ikke endrer rekkefølge. Lest, ikke kjørt |

## Neste
1. Kjetil ser på `images/rekkefolge-v1.png`.
2. Jobb 04 kjøres. Feiler bygget, rettes det før flaten skrives.
3. Flaten skrives på samme gren, med Playwright-prøver som legges i workflowen.
