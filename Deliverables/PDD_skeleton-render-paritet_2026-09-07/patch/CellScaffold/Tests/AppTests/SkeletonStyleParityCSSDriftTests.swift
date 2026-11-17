// SPDX-License-Identifier: Apache-2.0
// SPDX-FileCopyrightText: Copyright (c) 2026 Stiftelsen Digipomps and HAVEN contributors

import CellBase
import XCTest

/// Holder `SkeletonStyleParity.webStylesheetRoles` mot stilarkene den paastaar
/// aa speile.
///
/// `applyElementModifiers` i `Public/js/skeleton-runtime.js` legger paa klassen
/// `style-role-<navn>` for *hver* rolle, betingelsesloest. En rolle er derfor
/// stylet av web saa snart det finnes en `.style-role-<navn>`-regel - uten at
/// noen har skrevet spesialkode for den.
///
/// Lista over slike roller bor i CellProtocol, mens reglene bor her. To repoer,
/// ett faktum: uten denne testen driver de fra hverandre uten at noen merker
/// det. Det er nettopp det som hadde skjedd foer 2026-09-07 - `webOnlyRoles`
/// kjente bare de tre JS-spesialbehandlede rollene, saa fem roller som appen
/// bruker og web styler ble rapportert som `unclaimed`, altsaa "ingen rendrer
/// tolker den".
final class SkeletonStyleParityCSSDriftTests: XCTestCase {

    /// Filtyper som kan baere en `.style-role-*`-regel.
    private static let scannedExtensions: Set<String> = ["css", "html", "js"]

    func testWebStylesheetRolesMatchesTheStylesheets() throws {
        let (found, byFile) = try scanForStyleRoleSelectors()

        XCTAssertFalse(
            found.isEmpty,
            """
            Fant ingen `.style-role-*`-regler under Public/. Enten er testen \
            kjoert fra feil arbeidskatalog, eller saa er stilarkene borte. \
            Arbeidskatalog: \(FileManager.default.currentDirectoryPath)
            """
        )

        let declared = SkeletonStyleParity.webStylesheetRoles

        let missing = found.subtracting(declared)
        let stale = declared.subtracting(found)

        if missing.isEmpty == false {
            let lines = missing.sorted().map { role -> String in
                let files = (byFile[role] ?? []).sorted().joined(separator: ", ")
                return "  \"\(role)\",   // \(files)"
            }.joined(separator: "\n")
            XCTFail(
                """
                \(missing.count) rolle(r) har en `.style-role-*`-regel i web, men \
                mangler i `SkeletonStyleParity.webStylesheetRoles`.

                Konsekvens: `SkeletonStyleParity.classify` kaller dem `.unclaimed` \
                - "ingen rendrer tolker den" - naar web faktisk styler dem. \
                Funnstroemmen fra `normalizedForParity` underrapporterer dermed \
                forskjellen mellom web og native.

                Legg dem inn i CellProtocol/Sources/CellBase/Skeleton/SkeletonStyleParity.swift:

                \(lines)
                """
            )
        }

        if stale.isEmpty == false {
            XCTFail(
                """
                \(stale.count) rolle(r) staar i `SkeletonStyleParity.webStylesheetRoles`, \
                men har ingen `.style-role-*`-regel i Public/ lenger:

                \(stale.sorted().map { "  \($0)" }.joined(separator: "\n"))

                Fjern dem fra CellProtocol/Sources/CellBase/Skeleton/SkeletonStyleParity.swift. \
                En rolle som ikke lenger styles av web skal klassifiseres `.unclaimed`, \
                ikke `.webOnly`.
                """
            )
        }
    }

    /// De tre JS-spesialbehandlede rollene styles av kode, ikke av en regel.
    /// Faar en av dem en `.style-role-*`-regel, hoerer den i `webStylesheetRoles`
    /// i stedet - ellers staar samme rolle i to sett med hver sin begrunnelse.
    func testJavaScriptRolesAreNotAlsoStylesheetRoles() throws {
        let (found, _) = try scanForStyleRoleSelectors()
        let overlap = SkeletonStyleParity.webJavaScriptRoles.intersection(found)
        XCTAssertTrue(
            overlap.isEmpty,
            """
            \(overlap.sorted().joined(separator: ", ")) staar i `webJavaScriptRoles`, \
            men har ogsaa en `.style-role-*`-regel. Velg ett sett.
            """
        )
    }

    // MARK: - Skanning

    private func scanForStyleRoleSelectors() throws -> (
        roles: Set<String>,
        byFile: [String: Set<String>]
    ) {
        let publicRoot = URL(
            fileURLWithPath: FileManager.default.currentDirectoryPath,
            isDirectory: true
        ).appendingPathComponent("Public", isDirectory: true)

        var roles: Set<String> = []
        var byFile: [String: Set<String>] = [:]

        // `.style-role-` etterfulgt av navnet. Klassenavn i CSS kan avsluttes av
        // whitespace, komma, kolon, punktum, klammer eller kombinatorer.
        let pattern = try NSRegularExpression(pattern: "\\.style-role-([a-z0-9-]+)")

        guard let walker = FileManager.default.enumerator(
            at: publicRoot,
            includingPropertiesForKeys: [.isRegularFileKey]
        ) else {
            return ([], [:])
        }

        for case let url as URL in walker {
            guard Self.scannedExtensions.contains(url.pathExtension.lowercased()) else { continue }
            guard let text = try? String(contentsOf: url, encoding: .utf8) else { continue }

            let range = NSRange(text.startIndex..<text.endIndex, in: text)
            let relativePath = url.path.replacingOccurrences(
                of: FileManager.default.currentDirectoryPath + "/",
                with: ""
            )

            for match in pattern.matches(in: text, range: range) {
                guard let captured = Range(match.range(at: 1), in: text) else { continue }
                let role = String(text[captured])
                roles.insert(role)
                byFile[role, default: []].insert(relativePath)
            }
        }

        return (roles, byFile)
    }
}
