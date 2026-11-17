// SPDX-License-Identifier: Apache-2.0
// SPDX-FileCopyrightText: Copyright (c) 2026 Stiftelsen Digipomps and HAVEN contributors

import Foundation
import CellBase

enum PortholeWebPayloads {
    struct CellConfigurationLookup: Equatable {
        let uuid: String?
        let name: String?
        let sourceCellEndpoint: String?

        var hasIdentity: Bool {
            uuid != nil || name != nil || sourceCellEndpoint != nil
        }
    }

    private static let nestedConfigurationKeys = [
        "&cellConfiguration",
        "cellConfiguration",
        "configuration",
        "goal"
    ]
    private static let nestedLookupKeys = [
        "configurationLookup",
        "lookup"
    ]

    static func decodeCellConfiguration(from value: ValueType) -> CellConfiguration? {
        if case let .cellConfiguration(configuration) = value {
            return configuration
        }

        if case let .object(object) = value {
            for key in nestedConfigurationKeys {
                if let nestedValue = object[key],
                   let configuration = decodeCellConfiguration(from: nestedValue) {
                    return configuration
                }
            }
        }

        guard let json = try? value.jsonString() else { return nil }
        let decoder = JSONDecoder()
        if let direct = try? decoder.decode(CellConfiguration.self, fromString: json) {
            return direct
        }

        guard let data = json.data(using: .utf8),
              let rawObject = try? JSONSerialization.jsonObject(with: data) else {
            return nil
        }

        return decodeCellConfiguration(fromJSONObject: rawObject, decoder: decoder)
    }

    static func decodeCellConfigurationLookup(from value: ValueType) -> CellConfigurationLookup? {
        guard case let .object(object) = value else { return nil }

        if let direct = decodeLookupObject(object), direct.hasIdentity {
            return direct
        }

        for key in nestedLookupKeys {
            guard let nestedValue = object[key] else { continue }
            if let nestedLookup = decodeCellConfigurationLookup(from: nestedValue), nestedLookup.hasIdentity {
                return nestedLookup
            }
        }

        for key in nestedConfigurationKeys {
            guard let nestedValue = object[key] else { continue }
            if let nestedLookup = decodeCellConfigurationLookup(from: nestedValue), nestedLookup.hasIdentity {
                return nestedLookup
            }
        }

        return nil
    }

    static func resolveCellConfiguration(
        from value: ValueType,
        candidates: [CellConfiguration]
    ) -> CellConfiguration? {
        if let direct = decodeCellConfiguration(from: value) {
            return direct
        }

        guard let lookup = decodeCellConfigurationLookup(from: value), lookup.hasIdentity else {
            return nil
        }

        let normalizedUUID = normalizedLookupToken(lookup.uuid)
        let normalizedName = normalizedLookupToken(lookup.name)
        let normalizedEndpoint = normalizedLookupToken(lookup.sourceCellEndpoint)

        return candidates.first { configuration in
            if let normalizedUUID,
               normalizedLookupToken(configuration.uuid) == normalizedUUID {
                return true
            }

            if let normalizedName,
               normalizedLookupToken(configuration.name) == normalizedName {
                if let normalizedEndpoint {
                    let candidateEndpoint = normalizedLookupToken(configuration.discovery?.sourceCellEndpoint)
                    return candidateEndpoint == normalizedEndpoint
                }
                return true
            }

            return false
        }
    }

    private static func decodeCellConfiguration(
        fromJSONObject rawObject: Any,
        decoder: JSONDecoder
    ) -> CellConfiguration? {
        guard let dictionary = rawObject as? [String: Any] else { return nil }

        if let data = try? JSONSerialization.data(withJSONObject: dictionary),
           let json = String(data: data, encoding: .utf8),
           let direct = try? decoder.decode(CellConfiguration.self, fromString: json) {
            return direct
        }

        for key in nestedConfigurationKeys {
            if let nested = dictionary[key],
               let configuration = decodeCellConfiguration(fromJSONObject: nested, decoder: decoder) {
                return configuration
            }
        }

        return nil
    }

    private static func decodeLookupObject(_ object: Object) -> CellConfigurationLookup? {
        let uuid = stringValue(object["uuid"])
        let name = stringValue(object["name"])
        let sourceCellEndpoint = stringValue(object["sourceCellEndpoint"])
            ?? stringValue(object["endpoint"])

        let lookup = CellConfigurationLookup(
            uuid: normalizedLookupToken(uuid),
            name: normalizedLookupToken(name),
            sourceCellEndpoint: normalizedLookupToken(sourceCellEndpoint)
        )

        return lookup.hasIdentity ? lookup : nil
    }

    private static func stringValue(_ value: ValueType?) -> String? {
        switch value {
        case .string(let string):
            return string
        case .object(let object):
            return stringValue(object["value"])
        default:
            return nil
        }
    }

    private static func normalizedLookupToken(_ value: String?) -> String? {
        guard let value else { return nil }
        let trimmed = value.trimmingCharacters(in: .whitespacesAndNewlines)
        guard trimmed.isEmpty == false else { return nil }
        return trimmed.lowercased()
    }
}
