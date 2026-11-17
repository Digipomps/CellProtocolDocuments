// HavenHostCapabilities.swift — REFERANSE, ikke lagt i repoet (PDD_haven-visionos_2026-09-10, gren E).
// Formål: purpose://candidate.platform.capability-axis — verten beskrives med kapabiliteter, ikke OS-navn.
//
// Regelen filen håndhever:
//   1. `#if os(...)` brukes bare der et API faktisk bare finnes på én plattform (klasse A i auditen).
//      Foretrekk `canImport(Rammeverk)` framfor `os(Plattform)` — det er rammeverket som avgjør om koden
//      kompilerer, ikke plattformnavnet. `os(iOS) … #else <AppKit>` er mønsteret som ga tre
//      kompileringsfeil på visionOS.
//   2. Alle UX-/vertsvalg (paneler vs. overlays, avstander, materiale, sheet-størrelse, meny-stil …)
//      spør denne strukturen. Den avledes ETT sted (`resolveCurrent`), og bare der står `os(...)`.
//   3. `targetEnvironment(simulator)` brukes bare for simulator-feil (Keychain-tilgangskontroll),
//      aldri for UX. Simulatoren rapporteres som `isSimulator` og påvirker `biometrics`, `haptics`,
//      `nearbyPrecision` og `pushRegistration`.
//
// Referansetabellen for hver vert ligger i host_capability_profiles_v0.json; testen
// test.host.capability-profile sammenligner `profile(for:isSimulator:)` mot den tabellen.

import Foundation
#if canImport(UIKit)
import UIKit
#endif

public enum HavenHostFamily: String, Codable, CaseIterable {
    case mac, iPhone, iPad, vision, unknown
}

public struct HavenHostCapabilities: Equatable, Codable {
    public enum EditorPanels: String, Codable { case floatingPanels, separateWindows, overlay }
    public enum Presentation: String, Codable { case panel, sheet }
    public enum SheetSizing: String, Codable { case minSize, detents }
    public enum Spacing: String, Codable { case compact, regular, spatial }
    public enum SurfaceMaterial: String, Codable { case opaqueSystem, glass }
    public enum Biometrics: String, Codable { case none, touchID, faceID, opticID, simulated }

    public var family: HavenHostFamily
    public var isSimulator: Bool

    // Vindus- og scenemodell
    public var multiWindow: Bool                 // `openWindow` virker (krever UIApplicationSupportsMultipleScenes på iPad/visionOS)
    public var windowRestoration: Bool           // systemet gjenoppretter vinduer ved neste start
    public var editorPanels: EditorPanels        // hvor skeleton-editorens paneler bor
    public var diagnosticsPresentation: Presentation
    public var sheetSizing: SheetSizing
    public var ornaments: Bool
    public var immersiveSpace: Bool
    public var volumetricWindows: Bool

    // Layout
    public var spacingProfile: Spacing           // HIG visionOS: ≥ 60 pt mellom interaktive mål
    public var surfaceMaterial: SurfaceMaterial  // glass på visionOS: ingen opake systembakgrunner
    public var edgeMenus: Bool                   // dagens `usesPerspectiveDrivenEdgeMenus`

    // Inndata
    public var keyboardToolbar: Bool             // ToolbarItemGroup(placement: .keyboard)
    public var fileDrop: Bool                    // onDrop av filer inn i flaten
    public var haptics: Bool                     // UIImpactFeedbackGenerator finnes og gir noe
    public var hoverEffects: Bool

    // Sensorer og tjenester
    public var nearbyPrecision: Bool             // NearbyInteraction (UWB)
    public var speechInput: Bool                 // Speech + AVFoundation
    public var pushRegistration: Bool            // registerForRemoteNotifications gir ekte token
    public var localAgentRuntime: Bool           // launchctl/Process (HavenAgentD)
    public var biometrics: Biometrics

    /// Kapabilitetene en gitt vert har. Rent oppslag — ingen `os(...)` her, så den kan testes på Mac
    /// for alle familier. `compactChrome` er bevisst IKKE her: den kommer fra størrelsesklassen i
    /// visningen (`horizontalSizeClass == .compact`), som er riktig på alle verter.
    public static func profile(for family: HavenHostFamily, isSimulator: Bool) -> HavenHostCapabilities {
        var c: HavenHostCapabilities
        switch family {
        case .mac:
            c = HavenHostCapabilities(
                family: family, isSimulator: isSimulator,
                multiWindow: true, windowRestoration: false, editorPanels: .floatingPanels,
                diagnosticsPresentation: .panel, sheetSizing: .minSize, ornaments: false,
                immersiveSpace: false, volumetricWindows: false,
                spacingProfile: .regular, surfaceMaterial: .opaqueSystem, edgeMenus: false,
                keyboardToolbar: false, fileDrop: true, haptics: false, hoverEffects: true,
                nearbyPrecision: false, speechInput: true, pushRegistration: true,
                localAgentRuntime: true, biometrics: .touchID)
        case .iPhone:
            c = HavenHostCapabilities(
                family: family, isSimulator: isSimulator,
                multiWindow: false, windowRestoration: false, editorPanels: .overlay,
                diagnosticsPresentation: .sheet, sheetSizing: .detents, ornaments: false,
                immersiveSpace: false, volumetricWindows: false,
                spacingProfile: .compact, surfaceMaterial: .opaqueSystem, edgeMenus: true,
                keyboardToolbar: true, fileDrop: false, haptics: true, hoverEffects: false,
                nearbyPrecision: true, speechInput: true, pushRegistration: true,
                localAgentRuntime: false, biometrics: .faceID)
        case .iPad:
            c = HavenHostCapabilities(
                family: family, isSimulator: isSimulator,
                multiWindow: true, windowRestoration: true, editorPanels: .overlay,
                diagnosticsPresentation: .sheet, sheetSizing: .detents, ornaments: false,
                immersiveSpace: false, volumetricWindows: false,
                spacingProfile: .regular, surfaceMaterial: .opaqueSystem, edgeMenus: true,
                keyboardToolbar: true, fileDrop: true, haptics: false, hoverEffects: true,
                nearbyPrecision: false, speechInput: true, pushRegistration: true,
                localAgentRuntime: false, biometrics: .touchID)
        case .vision:
            c = HavenHostCapabilities(
                family: family, isSimulator: isSimulator,
                multiWindow: true, windowRestoration: true, editorPanels: .separateWindows,
                diagnosticsPresentation: .sheet, sheetSizing: .detents, ornaments: true,
                immersiveSpace: true, volumetricWindows: true,
                spacingProfile: .spatial, surfaceMaterial: .glass, edgeMenus: true,
                keyboardToolbar: true, fileDrop: true, haptics: false, hoverEffects: true,
                nearbyPrecision: false, speechInput: true, pushRegistration: true,
                localAgentRuntime: false, biometrics: .opticID)
        case .unknown:
            c = HavenHostCapabilities(
                family: family, isSimulator: isSimulator,
                multiWindow: false, windowRestoration: false, editorPanels: .overlay,
                diagnosticsPresentation: .sheet, sheetSizing: .detents, ornaments: false,
                immersiveSpace: false, volumetricWindows: false,
                spacingProfile: .regular, surfaceMaterial: .opaqueSystem, edgeMenus: true,
                keyboardToolbar: false, fileDrop: false, haptics: false, hoverEffects: false,
                nearbyPrecision: false, speechInput: false, pushRegistration: false,
                localAgentRuntime: false, biometrics: .none)
        }
        if isSimulator {
            // Simulatoren har ingen UWB, ingen haptikk, ingen ekte push-token, og biometri er simulert.
            c.nearbyPrecision = false
            c.haptics = false
            c.pushRegistration = false
            c.biometrics = .simulated
        }
        return c
    }

    /// Det ENESTE stedet i appen som spør om OS. Alt annet spør `HavenHostCapabilities.current`.
    public static func resolveCurrent() -> HavenHostCapabilities {
        #if targetEnvironment(simulator)
        let simulator = true
        #else
        let simulator = false
        #endif
        #if os(macOS)
        return profile(for: .mac, isSimulator: simulator)
        #elseif os(visionOS)
        return profile(for: .vision, isSimulator: simulator)
        #elseif os(iOS)
        // iPhone og iPad er samme OS; skillet er runtime.
        let family: HavenHostFamily = UIDevice.current.userInterfaceIdiom == .pad ? .iPad : .iPhone
        return profile(for: family, isSimulator: simulator)
        #else
        return profile(for: .unknown, isSimulator: simulator)
        #endif
    }

    /// Runtime-justeringer som ikke kan leses av plattformnavnet alene. Kalles én gang ved oppstart.
    /// Eksempel: `nearbyPrecision` er sann på iPhone bare hvis `NISession.isSupported` (UWB-brikke);
    /// `pushRegistration` er sann bare hvis brukeren har gitt varsel-tillatelse. Slike fakta legges
    /// på toppen av profilen — profilen sier hva verten *kan*, justeringen sier hva den *har*.
    public func adjusted(nearbyPrecisionSupported: Bool? = nil) -> HavenHostCapabilities {
        var c = self
        if let nearbyPrecisionSupported { c.nearbyPrecision = c.nearbyPrecision && nearbyPrecisionSupported }
        return c
    }
}

// MARK: - SwiftUI-miljø (referanse)
//
// private struct HavenHostCapabilitiesKey: EnvironmentKey {
//     static let defaultValue = HavenHostCapabilities.resolveCurrent()
// }
// extension EnvironmentValues {
//     var hostCapabilities: HavenHostCapabilities {
//         get { self[HavenHostCapabilitiesKey.self] } set { self[HavenHostCapabilitiesKey.self] = newValue }
//     }
// }
//
// Bruk i ContentView (erstatter `#if os(iOS)`-valg):
//   @Environment(\.hostCapabilities) private var host
//   switch host.editorPanels { case .floatingPanels: … case .separateWindows: openWindow(id: "editor-panels") case .overlay: … }
//   .padding(host.spacingProfile == .spatial ? 24 : host.spacingProfile == .compact ? 8 : 16)
//   background: host.surfaceMaterial == .glass ? Color.clear : platformCanvasColor
//
// Tester (avledet av formålet):
//   test.host.capability-profile — for hver rad i host_capability_profiles_v0.json:
//       XCTAssertEqual(HavenHostCapabilities.profile(for: rad.family, isSimulator: rad.isSimulator), rad.forventet)
//   test.host.current-is-known — HavenHostCapabilities.resolveCurrent().family != .unknown på alle byggemål.
//   test.lint.platform-conditionals — lint_platform_conditionals.sh gir 0 (ingen nye `os(`-valg utenfor tillatelseslisten).
