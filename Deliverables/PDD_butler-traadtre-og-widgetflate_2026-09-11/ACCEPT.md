# ACCEPT — Butler-trådtre og widgetflate

Oppdatert 2026-09-19 av Astra (Codex), etter WP-R3b.
Dette er åpne avvik, ikke en godkjenning av leveransen eller G3.

## Parity

| Navngitt avvik | Status og konsekvens | Gjenstående verifisering |
|---|---|---|
| **R6 — generisk drag/drop-adapter i Binding mangler** | **ÅPENT.** Sekvensert etter web etter Kjetils beslutning 2026-09-18. CellApple har nå felles dragkontekst og rendereradaptergrense, men Binding-adapteren er fortsatt utenfor denne pakken. Native drag/drop kan ikke telles som bestått T-F3. | Implementer Binding-adapteren; kjør dragstart, slipp, avbrudd, global målmarkering, kilde-/målpayload og faktisk kortpreview. |
| **ComponentSurface — kildehandlinger og vertsadapter** | **DELVIS.** Runtimekontrakten er lukket i iterasjon 6 §2.2. Web og native har monterings-/databinding. Native callback beholder payload og mount adskilt, men vertsadapter med kildecellens Agreement-flyt mangler. Reference/AttachmentField/FileUpload/NavigationBar/Visualization er foreløpig eksplisitt blokkert i native monterte definisjoner. | Fullfør scoped I/O og vertsintegrasjon. Test to instanser og faktisk kildehandling/avvisning mot felles fixture. Se [WP-R3-NATIVE.md](handoff/WP-R3-NATIVE.md). |
| **C1 — native funksjons- og bildeparitet** | **IKKE VERIFISERT.** WP-R3b er committet og CellApple bygger; 132 tester passer (21 nye native). Dette er modell-, kontrakt-, attributt- og avgrensede statiske rastertester. | Kjetil bygger Binding i Xcode med WP-R3b-revisjonen og kjører tastatur/VoiceOver/state-restaurering. Native skjermbilde må ha samme kandidat-JSON, nodedata, layoutkontekst og flate som web. Webens T-F3-nettleserbevis gjenstår også. |
| **ComponentSurface — revisjon/fokus/scroll/utkast** | **IKKE FUNKSJONSBEVIST.** Native har stabil instans-/feltidentitet, separate utkastlagre og macOS-scrollobservasjon. Modelltest er grønn; endret understruktur og faktisk GUI-state er ikke målt. | Native/web-økt med kildeoppdatering, ny revisjon, omordning og variantskifte; kontroller fokus, tekstmarkering og scroll. |

Grunnlag: [SKJELETT_ELEMENTER.md](handoff/SKJELETT_ELEMENTER.md) §2.2 og §3,
[WP-R2-WEB.md](handoff/WP-R2-WEB.md), [WP-R3-NATIVE.md](handoff/WP-R3-NATIVE.md).
