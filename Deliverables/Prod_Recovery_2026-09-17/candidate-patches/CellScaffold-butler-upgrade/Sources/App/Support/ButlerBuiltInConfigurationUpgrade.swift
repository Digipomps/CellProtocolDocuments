// SPDX-License-Identifier: Apache-2.0
// SPDX-FileCopyrightText: Copyright (c) 2026 Stiftelsen Digipomps and HAVEN contributors

import Foundation
import Crypto
import CellBase

/// Recognizes a complete former built-in skeleton, never the mere absence of
/// thread controls. Custom text, actions, payloads and layout remain untouched.
enum ButlerBuiltInConfigurationUpgrade {
    // Generated from former production source b4a2779a, factory blob
    // 190adab4999ced1c1abab519e5ca9ea9d5fccb5c. Filled by the fixture proof.
    static let previousSkeletonDigest = "PENDING_VERIFIED_LEGACY_FIXTURE"

    static func upgraded(
        _ configuration: CellConfiguration,
        using current: CellConfiguration
    ) -> CellConfiguration? {
        guard configuration.name == "Co-Pilot Chat",
              configuration.discovery?.sourceCellEndpoint == PersonalChatHubContract.endpoint,
              current.discovery?.sourceCellEndpoint == PersonalChatHubContract.endpoint,
              let skeleton = configuration.skeleton,
              let currentSkeleton = current.skeleton,
              fingerprint(skeleton) == previousSkeletonDigest,
              fingerprint(currentSkeleton) != previousSkeletonDigest,
              let chat = configuration.cellReferences?.first(where: { $0.label == "chatHub" }),
              [PersonalChatHubContract.endpoint, PersonalChatHubAccountCompatibility.endpoint].contains(chat.endpoint)
        else { return nil }

        // Preserve UUID, discovery, localization, reference authority and any
        // additional references. Only the exact built-in skeleton is replaced.
        var upgraded = configuration
        upgraded.skeleton = currentSkeleton
        return upgraded
    }

    static func fingerprint(_ skeleton: SkeletonElement) -> String? {
        guard let data = try? JSONEncoder().encode(skeleton),
              let value = try? JSONSerialization.jsonObject(with: data),
              let canonical = try? JSONSerialization.data(
                  withJSONObject: normalizeElementIDs(value),
                  options: [.sortedKeys, .withoutEscapingSlashes]
              ) else { return nil }
        return SHA256.hash(data: canonical).map { String(format: "%02x", $0) }.joined()
    }

    /// Some typed Skeleton elements generate a fresh renderer UUID at creation.
    /// Ignore only that own element identifier. Panel IDs, action payload IDs,
    /// keypaths, conditions and every user-visible value participate in the hash.
    private static func normalizeElementIDs(_ value: Any) -> Any {
        if let values = value as? [Any] { return values.map(normalizeElementIDs) }
        guard var object = value as? [String: Any] else { return value }
        let elementKinds: Set<String> = [
            "Text", "TextField", "TextArea", "Image", "Spacer", "HStack", "VStack",
            "ZStack", "List", "Object", "Reference", "Button", "Divider", "ScrollView",
            "Section", "Grid", "Toggle", "Picker", "FileUpload", "AttachmentField", "Tabs"
        ]
        if object.count == 1, let kind = object.keys.first, elementKinds.contains(kind),
           var body = object[kind] as? [String: Any],
           let id = body["id"] as? String, UUID(uuidString: id) != nil {
            body.removeValue(forKey: "id")
            object[kind] = body
        }
        for (key, child) in object where key != "payload" {
            object[key] = normalizeElementIDs(child)
        }
        return object
    }
}
