#!/usr/bin/env python3
"""Patcher for PDD haven-visionos (steg 2 og 3 i PLAN.md).

Bruk:
    apply_patches.py <Binding-rot> <CellProtocol-rot> --phase P|A|B|AB [--dry-run]

Fase P (bare prosjektfilen — brukes til å MÅLE H1 før Swift-rettelsene):
  A4 alene.

Fase A (gren E, purpose://candidate.platform.visionos-native):
  A1  Binding/Binding/ContentView.swift  – to AppKit-i-#else byttes til canImport-form med nøytral #else
  A2  Binding/Binding/RootView.swift     – samme
  A3  CellProtocol/…/EntityRadar/ScannerService.swift – ubrukt UIImpactFeedbackGenerator fjernes (død kode)
  A4  Binding/Binding.xcodeproj/project.pbxproj – HAVEN-målet: xros/xrsimulator, enhetsfamilie 7,
      XROS_DEPLOYMENT_TARGET, entitlements og scene-manifest per xros-SDK

Fase B (gren B, purpose://candidate.porthole.backside):
  B1  CellProtocol/…/Skeleton/Suggestion/PortholeBackside.swift – ny fil (kopieres fra patches/)
  B2  CellProtocol/…/Skeleton/Suggestion/PortholeBindingViewModel.swift – puls + bakside-snapshot
  B3  Binding/Binding/ContentView.swift – @State, flipp rundt PortholeCanvas, menyvalg «Bakside»

Hvert anker må treffe nøyaktig det antallet som er oppgitt, ellers endres ingenting i den filen
(exit 2). Idempotent: en fil som allerede bærer markøren «PDD haven-visionos» for sitt steg hoppes over.
Skriver aldri utenfor de to rotmappene som oppgis.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MARK = "PDD haven-visionos"


class PatchError(Exception):
    pass


def read(path):
    with open(path, encoding="utf-8") as handle:
        return handle.read()


def write(path, text, dry):
    if dry:
        return
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(text)


def replace_exact(text, old, new, expected, what):
    count = text.count(old)
    if count != expected:
        raise PatchError(f"{what}: ankeret traff {count} ganger, forventet {expected}")
    return text.replace(old, new)


def patch_file(path, steps, marker, dry, log):
    """steps: liste av (old, new, expected, what)."""
    text = read(path)
    if marker in text:
        log(f"  hopper over (allerede patchet): {path}")
        return False
    for old, new, expected, what in steps:
        text = replace_exact(text, old, new, expected, what)
    write(path, text, dry)
    log(f"  {'ville patchet' if dry else 'patchet'}: {path}")
    return True


# ---------------------------------------------------------------- fase A

def phase_baseline(binding, dry, log):
    """Rød baseline (målt 16.09): Binding HEAD 775fc93d mangler `.NavigationBar`-case mot CellProtocol HEAD 561d34a.
    Tre SkeletonEditor-filer kopieres av KJOR-SELV fra patches/baseline/; FullLibraryView har mye annet WIP i
    hovedtreet, så bare de seks linjene legges inn her. Ikke Losens endring — hører hjemme i Kjetils egen commit."""
    full_library = os.path.join(binding, "Binding", "FullLibraryView.swift")
    if not os.path.exists(full_library):
        return
    text = read(full_library)
    if "case .NavigationBar(let navigationBar):" in text:
        log(f"  baseline ok: {full_library}")
        return
    anchor = ("                    tabs.selectionActionKeypath != nil\n"
              "            )\n"
              "\n"
              "        case .Visualization(let visualization):\n"
              "            return placeholderCollection(\n"
              "                title: \"Preview \\(visualization.kind)\",")
    new = ("                    tabs.selectionActionKeypath != nil\n"
           "            )\n"
           "\n"
           "        case .NavigationBar(let navigationBar):\n"
           "            return PreparedPreview(\n"
           "                element: .NavigationBar(navigationBar),\n"
           "                usesPlaceholders: false\n"
           "            )\n"
           "\n"
           "        case .Visualization(let visualization):\n"
           "            return placeholderCollection(\n"
           "                title: \"Preview \\(visualization.kind)\",")
    text = replace_exact(text, anchor, new, 1, "baseline FullLibraryView NavigationBar")
    write(full_library, text, dry)
    log(f"  {'ville patchet' if dry else 'patchet'} (baseline NavigationBar-case): {full_library}")


def phase_a(binding, cellprotocol, dry, log, include_swift=True):
    log("Fase A — plattform (gren E)" if include_swift else "Fase P — bare prosjektfilen (H1-måling)")
    phase_baseline(binding, dry, log)
    if include_swift:
        phase_a_swift(binding, cellprotocol, dry, log)
    phase_a_pbxproj(binding, dry, log)


def phase_a_swift(binding, cellprotocol, dry, log):

    content_view = os.path.join(binding, "Binding", "ContentView.swift")
    patch_file(content_view, [
        (
            "    private var personalCopilotPlatformCanvasColor: Color {\n"
            "#if os(iOS)\n"
            "        Color(uiColor: .systemGroupedBackground)\n"
            "#else\n"
            "        Color(nsColor: .windowBackgroundColor)\n"
            "#endif\n"
            "    }\n",
            "    private var personalCopilotPlatformCanvasColor: Color {\n"
            "        // PDD haven-visionos steg 2: API-gate med canImport og nøytral #else (auditen §4.1).\n"
            "#if canImport(UIKit)\n"
            "        Color(uiColor: .systemGroupedBackground)\n"
            "#elseif canImport(AppKit)\n"
            "        Color(nsColor: .windowBackgroundColor)\n"
            "#else\n"
            "        Color.clear\n"
            "#endif\n"
            "    }\n",
            1, "A1 canvasColor",
        ),
        (
            "    private var personalCopilotPlatformSurfaceColor: Color {\n"
            "#if os(iOS)\n"
            "        Color(uiColor: .systemBackground)\n"
            "#else\n"
            "        Color(nsColor: .controlBackgroundColor)\n"
            "#endif\n"
            "    }\n",
            "    private var personalCopilotPlatformSurfaceColor: Color {\n"
            "#if canImport(UIKit)\n"
            "        Color(uiColor: .systemBackground)\n"
            "#elseif canImport(AppKit)\n"
            "        Color(nsColor: .controlBackgroundColor)\n"
            "#else\n"
            "        Color.clear\n"
            "#endif\n"
            "    }\n",
            1, "A1 surfaceColor",
        ),
    ], MARK + " steg 2", dry, log)

    root_view = os.path.join(binding, "Binding", "RootView.swift")
    patch_file(root_view, [
        (
            "    private var launchBackgroundColor: Color {\n"
            "#if os(iOS)\n"
            "        Color(uiColor: .systemBackground)\n"
            "#else\n"
            "        Color(nsColor: .windowBackgroundColor)\n"
            "#endif\n"
            "    }\n",
            "    private var launchBackgroundColor: Color {\n"
            "        // PDD haven-visionos steg 2: API-gate med canImport og nøytral #else (auditen §4.1).\n"
            "#if canImport(UIKit)\n"
            "        Color(uiColor: .systemBackground)\n"
            "#elseif canImport(AppKit)\n"
            "        Color(nsColor: .windowBackgroundColor)\n"
            "#else\n"
            "        Color.clear\n"
            "#endif\n"
            "    }\n",
            1, "A2 launchBackgroundColor",
        ),
    ], MARK + " steg 2", dry, log)

    scanner = os.path.join(cellprotocol, "Sources", "CellApple", "EntityRadar", "ScannerService.swift")
    scanner_text = read(scanner)
    uses = scanner_text.count("impactGenerator")
    if uses != 2 and MARK not in scanner_text:
        raise PatchError(f"A3 ScannerService: 'impactGenerator' forekommer {uses} ganger (forventet 2: deklarasjon + #else). "
                         "Har den fått et bruksted, skal den gates med `#if canImport(UIKit) && !os(visionOS)` og allowlisten oppdateres.")
    patch_file(scanner, [
        (
            "#if canImport(UIKit)\n"
            "    let impactGenerator = UIImpactFeedbackGenerator(style: .medium)\n"
            "#else\n"
            "    // UIKit haptics unavailable on this platform\n"
            "    let impactGenerator: Any? = nil\n"
            "#endif\n",
            "    // PDD haven-visionos steg 2: UIImpactFeedbackGenerator finnes ikke i visionOS-SDK-en og\n"
            "    // egenskapen hadde ingen bruksted (målt 2026-09-16) — fjernet som død kode.\n",
            1, "A3 impactGenerator",
        ),
    ], MARK + " steg 2", dry, log)



def phase_a_pbxproj(binding, dry, log):
    pbx = os.path.join(binding, "Binding.xcodeproj", "project.pbxproj")
    pbx_text = read(pbx)
    if MARK in pbx_text or "xrsimulator" in pbx_text:
        log(f"  hopper over (allerede patchet): {pbx}")
    else:
        # HAVEN-målet har to konfigurasjoner (Debug/Release) med disse nøklene; testmålene har dem også,
        # så treffantallet i hele filen er 6 for SUPPORTED_PLATFORMS/TARGETED_DEVICE_FAMILY. Vi patcher
        # bare blokkene som har PRODUCT_BUNDLE_IDENTIFIER = org.digipomps.haven (app-målet).
        blocks = pbx_text.split("PRODUCT_BUNDLE_IDENTIFIER = org.digipomps.haven;")
        if len(blocks) != 3:
            raise PatchError(f"A4 pbxproj: fant {len(blocks) - 1} app-mål-konfigurasjoner, forventet 2")
        # Nøklene ligger ETTER PRODUCT_BUNDLE_IDENTIFIER i samme blokk (alfabetisk), fram til neste '};'
        out = [blocks[0]]
        for index in (1, 2):
            block = blocks[index]
            head, sep, tail = block.partition("\t\t\t};")
            if not sep:
                raise PatchError("A4 pbxproj: fant ikke blokkslutt")
            head = replace_exact(head,
                                 'SUPPORTED_PLATFORMS = "iphoneos iphonesimulator macosx";',
                                 'SUPPORTED_PLATFORMS = "iphoneos iphonesimulator macosx xros xrsimulator";',
                                 1, f"A4 SUPPORTED_PLATFORMS blokk {index}")
            head = replace_exact(head,
                                 'TARGETED_DEVICE_FAMILY = "1,2";',
                                 'TARGETED_DEVICE_FAMILY = "1,2,7";\n\t\t\t\tXROS_DEPLOYMENT_TARGET = 26.0;',
                                 1, f"A4 TARGETED_DEVICE_FAMILY blokk {index}")
            out.append("PRODUCT_BUNDLE_IDENTIFIER = org.digipomps.haven;" + head + sep + tail)
        pbx_text = "".join(out)
        # Per-SDK-nøkler i den felles app-konfigurasjonen (samme sted som iphoneos-variantene).
        pbx_text = replace_exact(
            pbx_text,
            '\t\t\t\t"CODE_SIGN_ENTITLEMENTS[sdk=iphonesimulator*]" = "Binding/Binding-iOS.entitlements";\n',
            '\t\t\t\t"CODE_SIGN_ENTITLEMENTS[sdk=iphonesimulator*]" = "Binding/Binding-iOS.entitlements";\n'
            '\t\t\t\t"CODE_SIGN_ENTITLEMENTS[sdk=xros*]" = "Binding/Binding-iOS.entitlements";\n'
            '\t\t\t\t"CODE_SIGN_ENTITLEMENTS[sdk=xrsimulator*]" = "Binding/Binding-iOS.entitlements";\n',
            2, "A4 entitlements per SDK (Debug+Release)")
        pbx_text = replace_exact(
            pbx_text,
            '\t\t\t\t"INFOPLIST_KEY_UIApplicationSceneManifest_Generation[sdk=iphonesimulator*]" = YES;\n',
            '\t\t\t\t"INFOPLIST_KEY_UIApplicationSceneManifest_Generation[sdk=iphonesimulator*]" = YES;\n'
            '\t\t\t\t"INFOPLIST_KEY_UIApplicationSceneManifest_Generation[sdk=xros*]" = YES;\n'
            '\t\t\t\t"INFOPLIST_KEY_UIApplicationSceneManifest_Generation[sdk=xrsimulator*]" = YES;\n',
            2, "A4 scene manifest per SDK (Debug+Release)")
        pbx_text = replace_exact(
            pbx_text,
            '\t\t\t\t"INFOPLIST_KEY_UILaunchScreen_Generation[sdk=iphoneos*]" = YES;\n',
            '\t\t\t\t"INFOPLIST_KEY_UILaunchScreen_Generation[sdk=iphoneos*]" = YES;\n'
            '\t\t\t\t"INFOPLIST_KEY_UILaunchScreen_Generation[sdk=xros*]" = YES;\n'
            '\t\t\t\t"INFOPLIST_KEY_UILaunchScreen_Generation[sdk=xrsimulator*]" = YES;\n',
            2, "A4 launch screen per SDK (Debug+Release)")
        write(pbx, pbx_text, dry)
        log(f"  {'ville patchet' if dry else 'patchet'}: {pbx}")


# ---------------------------------------------------------------- fase B

def phase_b(binding, cellprotocol, dry, log):
    log("Fase B — baksiden (gren B)")
    suggestion = os.path.join(cellprotocol, "Sources", "CellApple", "Cells", "Porthole",
                              "Utility Views", "Skeleton", "Suggestion")
    if not os.path.isdir(suggestion):
        raise PatchError(f"B1 finner ikke {suggestion}")

    target = os.path.join(suggestion, "PortholeBackside.swift")
    source = os.path.join(HERE, "PortholeBackside.swift")
    if os.path.exists(target):
        log(f"  finnes allerede: {target}")
    else:
        if not dry:
            shutil.copyfile(source, target)
        log(f"  {'ville kopiert' if dry else 'kopierte'}: {target}")

    view_model = os.path.join(suggestion, "PortholeBindingViewModel.swift")
    patch_file(view_model, [
        (
            "    @Published public var cellReferences = [CellReference]()\n"
            "    @Published  var flowElements = [FlowElement]()\n",
            "    @Published public var cellReferences = [CellReference]()\n"
            "    @Published  var flowElements = [FlowElement]()\n"
            "    // PDD haven-visionos steg 3 (gren B): puls med ankomsttid og bakside-snapshot.\n"
            "    @Published public var pulse: [PortholePulseEntry] = []\n"
            "    @Published public var backside: PortholeBacksideSnapshot?\n"
            "    var pulseLimit = 24\n",
            1, "B2 stored properties",
        ),
        (
            "    @MainActor\n"
            "    func appendFlowELement(_ flowElement: FlowElement) {\n",
            "    /// Leser baksiden av flaten fra cellen selv (ikke fra view-modellens kopi, som er tom etter\n"
            "    /// kaldstart når cellen lastet lagret konfigurasjon). Tilstand per label fra attachedStatuses.\n"
            "    public func refreshBackside(fallback: CellConfiguration? = nil) async {\n"
            "        let porthole = self.portholeMeddle as? OrchestratorCell\n"
            "        // Cellens egen konfigurasjon først; ellers den verten viser (ContentView.activeConfiguration).\n"
            "        let configuration = porthole?.getCellConfiguration() ?? fallback\n"
            "        var statuses: [ConnectionStatus] = []\n"
            "        var statusError: String?\n"
            "        if let porthole {\n"
            "            if let vault = CellBase.defaultIdentityVault,\n"
            "               let identity = await vault.identity(for: \"private\", makeNewIfNotFound: true) {\n"
            "                do {\n"
            "                    statuses = try await porthole.attachedStatuses(requester: identity)\n"
            "                } catch {\n"
            "                    statusError = \"\\(error)\"\n"
            "                }\n"
            "            } else {\n"
            "                statusError = \"ingen identitet\"\n"
            "            }\n"
            "        } else {\n"
            "            statusError = \"Porthole-cellen er ikke koblet til ennå\"\n"
            "        }\n"
            "        var statusByName: [String: ConnectionStatus] = [:]\n"
            "        for status in statuses where statusByName[status.name] == nil {\n"
            "            statusByName[status.name] = status\n"
            "        }\n"
            "        let references: [PortholeBacksideReference] = (configuration?.cellReferences ?? []).map { reference in\n"
            "            let status = statusByName[reference.label]\n"
            "            let lastPulse = self.pulse.first(where: { $0.label == reference.label })?.receivedAt\n"
            "            return PortholeBacksideReference(\n"
            "                label: reference.label,\n"
            "                endpoint: reference.endpoint,\n"
            "                subscribeFeed: reference.subscribeFeed,\n"
            "                subscriptions: reference.subscriptions.map { $0.endpoint },\n"
            "                setKeys: reference.setKeysAndValues.map { $0.key },\n"
            "                connected: porthole == nil ? false : status?.connected,\n"
            "                active: porthole == nil ? false : status?.active,\n"
            "                lastPulse: lastPulse\n"
            "            )\n"
            "        }\n"
            "        self.backside = PortholeBacksideSnapshot(configurationName: configuration?.name, references: references,\n"
            "                                                 statusCount: statuses.count, capturedAt: Date(), statusError: statusError)\n"
            "    }\n"
            "\n"
            "    private func recordPulse(_ flowElement: FlowElement) {\n"
            "        var label: String?\n"
            "        if let origin = flowElement.origin {\n"
            "            let candidates = (self.portholeMeddle as? OrchestratorCell)?.getCellConfiguration()?.cellReferences ?? self.cellReferences\n"
            "            label = candidates.first(where: { origin == $0.endpoint || origin.hasPrefix($0.endpoint) })?.label\n"
            "        }\n"
            "        let entry = PortholePulseEntry(\n"
            "            receivedAt: Date(),\n"
            "            title: flowElement.title,\n"
            "            topic: flowElement.topic,\n"
            "            origin: flowElement.origin,\n"
            "            kind: flowElement.properties?.type.rawValue ?? \"ukjent\",\n"
            "            label: label\n"
            "        )\n"
            "        self.pulse.insert(entry, at: 0)\n"
            "        if self.pulse.count > pulseLimit {\n"
            "            self.pulse.removeLast()\n"
            "        }\n"
            "    }\n"
            "\n"
            "    @MainActor\n"
            "    func appendFlowELement(_ flowElement: FlowElement) {\n"
            "        recordPulse(flowElement)\n",
            1, "B2 methods",
        ),
    ], MARK + " steg 3", dry, log)

    content_view = os.path.join(binding, "Binding", "ContentView.swift")
    patch_file(content_view, [
        (
            "    @State private var editorMode: EditorMode = .view\n",
            "    @State private var editorMode: EditorMode = .view\n"
            "    // PDD haven-visionos steg 3 (gren B): baksiden av flaten.\n"
            "    @State private var showsPortholeBackside = UserDefaults.standard.bool(forKey: \"HAVENShowBackside\")\n",
            1, "B3 state",
        ),
        (
            "    private var portholeCanvas: some View {\n"
            "        PortholeCanvas(\n",
            "    private var portholeCanvas: some View {\n"
            "        PortholeFlipContainer(showsBackside: showsPortholeBackside, onToggle: {\n"
            "            showsPortholeBackside.toggle()\n"
            "        }, front: {\n"
            "            portholeFrontCanvas\n"
            "        }, back: {\n"
            "            PortholeBacksideView(viewModel: viewModel, fallbackConfiguration: activeConfiguration)\n"
            "        })\n"
            "    }\n"
            "\n"
            "    private var portholeFrontCanvas: some View {\n"
            "        PortholeCanvas(\n",
            1, "B3 flip wrapper",
        ),
        (
            "                Button {\n"
            "                    editorMode = .edit\n"
            "                } label: {\n"
            "                    Label(\"Rediger\", systemImage: \"square.and.pencil\")\n"
            "                }\n",
            "                Button {\n"
            "                    editorMode = .edit\n"
            "                } label: {\n"
            "                    Label(\"Rediger\", systemImage: \"square.and.pencil\")\n"
            "                }\n"
            "\n"
            "                Button {\n"
            "                    showsPortholeBackside.toggle()\n"
            "                } label: {\n"
            "                    Label(showsPortholeBackside ? \"Forside\" : \"Bakside\", systemImage: \"arrow.2.squarepath\")\n"
            "                }\n",
            1, "B3 menu item",
        ),
    ], MARK + " steg 3", dry, log)


def main(argv):
    if len(argv) < 4:
        print(__doc__)
        return 1
    binding = os.path.abspath(argv[1])
    cellprotocol = os.path.abspath(argv[2])
    phase = "AB"
    dry = False
    args = argv[3:]
    while args:
        arg = args.pop(0)
        if arg == "--phase":
            phase = args.pop(0).upper()
        elif arg == "--dry-run":
            dry = True
        else:
            print(f"ukjent argument {arg}")
            return 1
    for root in (binding, cellprotocol):
        if not os.path.isdir(root):
            print(f"finnes ikke: {root}")
            return 1
    log = lambda line: print(line, flush=True)
    log(f"Binding: {binding}\nCellProtocol: {cellprotocol}\nfase: {phase}{' (tørrkjøring)' if dry else ''}")
    try:
        if "A" in phase:
            phase_a(binding, cellprotocol, dry, log, include_swift=True)
        elif "P" in phase:
            phase_a(binding, cellprotocol, dry, log, include_swift=False)
        if "B" in phase:
            phase_b(binding, cellprotocol, dry, log)
    except PatchError as error:
        print(f"STOPP: {error}")
        return 2
    log("ferdig")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
