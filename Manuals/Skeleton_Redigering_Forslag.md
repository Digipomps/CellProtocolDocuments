---
doc_id: manual-skeleton-redigering-forslag
title: Skeleton-redigering – brister og forslag til flateendringer
repo: CellProtocolDocuments
audience: human
status: draft
last_verified: 2026-10-22
---

# Skeleton-redigering: brister og forslag

Funnet under arbeidet med [brukermanualen](Skeleton_Redigering.md). Dette er
**forslag**; ingenting er implementert. Hvert punkt trenger Kjetils ja før det
bygges. Kodehenvisninger gjelder CellScaffold `main` 0b776a4 og CellProtocol
`main` 4252c82.

## Må fikses (fører til at folk mister eller lagrer arbeid uten å vite det)

### F1. «Vis» lagrer ulagrede endringer i det stille
`editor.mode.set` med `view` kjører `applyWorkingDocument` når kladden er endret
(`PortholeWebSessionSupport.swift`, case `editor.mode.set`). Brukeren tror **Vis**
er «se resultatet», men det er «lagre».
**Forslag:** Når kladden er endret, spør: *Lagre* / *Forkast* / *Fortsett å
redigere*. Alternativt: la **Vis** beholde kladden urørt og bare skjule panelene.

### F2. «Bruk» betyr to forskjellige ting uten at det vises
For kildebaserte flater lagrer **Bruk** varig i eiercellen. For alle andre setter
den bare øktens konfigurasjon, som forsvinner når du bytter flate. I det siste
tilfellet vises ingen banner (`resolveEditorAccessNotice` returnerer `null`).
**Forslag:** Vis et banner «Endringer gjelder bare denne visningen» og gi
knappen teksten **Bruk midlertidig**, med lenke til «Lagre som egen versjon» (Studio).

## Gjør redigering mulig å forklare enkelt

### F3. Ingen «Tilbakestill til original»
Kontrakten har `resetEditableCellConfiguration`, men Porthole har ingen knapp.
**Forslag:** Knapp **Tilbakestill til original** under **Mer** for kildebaserte
flater med lagret endring, med bekreftelse.

### F4. Kan ikke legge til enkle byggeklosser eller flytte noe
Paletten (`PortholeWebComponentCatalog.defaultItems`) har bare ti sammensatte
komponenter. Man kan ikke legge til en overskrift, en knapp eller et felt, og kan
ikke flytte eller duplisere et element.
**Forslag:** Gruppen «Byggeklosser» i paletten (Tekst, Knapp, Felt, Seksjon,
Stabel, Skillelinje) og knappene **Flytt opp / Flytt ned / Dupliser** i
inspektøren. Dette er editor-funksjonalitet, ikke nye skeleton-elementer.

### F5. Inspektøren kan ikke sette slippsoner, synlighet eller lister
Bare enkle verdier kan endres (`isEditableScalarValue`). Dermed kan en
flate-eier ikke selv merke et område som slippsone (`acceptedDragRoles:
["component"]`), selv om dra-og-slipp bygger på det.
**Forslag:** En avkrysningsboks **Tar imot komponenter** på beholdere, og et
enkelt felt for lister (kommaseparert).

### F6. To redigeringsveier med ulikt språk
Porthole sier **Bruk / Forkast**; Studio sier **Publiser til valgt eiercelle /
Forkast lokale endringer**. JSON-panelet i Porthole er skrivebeskyttet, så større
endringer krever kopier → fil → last opp i Studio.
**Forslag:** Knapp **Rediger som JSON** i Porthole som åpner kladden direkte som
Studio-utkast, og samme ord begge steder («Lagre», «Forkast»).

### F7. Teknisk språk i panelene
«Parameters», «Modifiers», «Raw node», «Dirty», «working/committed
CellConfiguration», «References», «Path root.2.0» og en åpen Debug-seksjon.
**Forslag:** Norske, vanlige navn (Innhold, Utseende, Endret, Lagret versjon,
Koblede celler) og flytt Raw/Debug bak **Avansert**.

## Kvalitet og paritet

### F8. «Struktur OK» skjuler uoppnåelige handlinger
Valideringen i inspektøren sjekker referanser og bindinger, men ikke om
seksjoner og knapper kan nås. `SkeletonReachabilityAudit` finnes i CellBase.
**Forslag:** Vis «N handlinger kan ikke nås» i inspektøren ved å kjøre auditen
på kladden.

### F9. Studio-flaten skjuler seksjoner i HAVEN-appen
`CellConfigurationStudioConfigurationFactory` gater «Arbeidsflate» og
«Versjonshistorikk» med rot-betingelser (`scope: .root, exists: true`). Web løser
dem mot state; Binding evaluerer rot uten verdi, så seksjonene vises aldri der,
og «Konfigurasjonene lastes …» blir stående. Ikke verifisert visuelt.
**Forslag:** Bytt til liste-mønsteret (0 eller 1 rad) som skillen beskriver.

### F10. Ingen redigering i HAVEN-appen
Binding har ingen redigeringsmodus. Det er greit, men appen bør si det: en lenke
«Rediger i nettleseren» der en eier ser en flate.

## Anbefalt rekkefølge
F1 og F2 først (små endringer, stor risiko i dag), så F7 og F3, deretter F4–F6.
