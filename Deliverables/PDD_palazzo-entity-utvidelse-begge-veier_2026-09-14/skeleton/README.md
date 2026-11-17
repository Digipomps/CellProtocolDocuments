Bildene i `images/` er mockups rendret fra `images/render.html` (HTML), ikke fra skeleton-JSON — se
`lesson.scaffold-without-porthole-host-has-no-preview`. Skeleton-JSON for tilbudssheetet skrives i WP-G etter
samtykkemønsteret i `PalazzoScaffold::Sources/App/Skeleton/PalazzoConsentConfigurationFactory.swift`
(`SkeletonPresentation(kind: .modal)`, mobileFallback sheet) og legges her før Porthole-preview/paritet.
Hva dagens skeleton ikke kan rendre står i `images/README.md`.
