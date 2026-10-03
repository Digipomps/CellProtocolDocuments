# baseline/ — reparasjon av rød baseline (16.09.2026)

Binding HEAD `775fc93d` bygger ikke mot CellProtocol HEAD `561d34a`: fire «switch must be exhaustive»-feil
fordi `SkeletonElement.NavigationBar` finnes i CellProtocol, men ikke håndteres i tre filer i Binding
(`SkeletonTreeQueries.swift:18,52`, `SkeletonTreeMutations.swift:161`, `SkeletonElementParameterCatalog.swift:1293`).
Hovedtreet hadde rettelsen som **ucommitterte** endringer (kun NavigationBar-tilleggene). Disse tre filene er
kopiert hit fra hovedtreet 2026-09-16 og legges inn i worktreet av `KJOR-SELV-visionos.command` (steg «1b baseline»).
De er Kjetils egne endringer, ikke Losens, og hører hjemme i en egen commit i Binding.
