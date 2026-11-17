// SPDX-License-Identifier: Apache-2.0
// SPDX-FileCopyrightText: Copyright (c) 2026 Stiftelsen Digipomps and HAVEN contributors

import CellBase
import Foundation
import Vapor

/// Opt-in transport admission for named bridgeheads, independent of Cell authority.
public struct RemoteBridgeheadAccess: Sendable {
    public enum ConfigurationError: Error {
        case tokenAndHostsRequired, invalidHost, invalidToken, conflictingRoute
    }

    private let token: String
    private let endpoints: [URL]

    public static func fromEnvironment(_ environment: [String: String] = ProcessInfo.processInfo.environment) throws -> Self? {
        let token = (environment["HAVEN_BRIDGEHEAD_TOKEN"] ?? "").trimmingCharacters(in: .whitespacesAndNewlines)
        let hosts = (environment["HAVEN_BRIDGEHEAD_HOSTS"] ?? "").trimmingCharacters(in: .whitespacesAndNewlines)
        if token.isEmpty && hosts.isEmpty { return nil }
        guard !token.isEmpty, !hosts.isEmpty else { throw ConfigurationError.tokenAndHostsRequired }
        guard token.unicodeScalars.allSatisfy({ (33...126).contains($0.value) }) else { throw ConfigurationError.invalidToken }
        let endpoints = try hosts.split(separator: ",", omittingEmptySubsequences: false).map { raw -> URL in
            let authority = raw.trimmingCharacters(in: .whitespacesAndNewlines)
            guard let url = URL(string: "cell://" + authority), let host = url.host, !host.isEmpty,
                  let port = url.port, (1...65535).contains(port),
                  url.user == nil, url.password == nil, url.path.isEmpty,
                  url.query == nil, url.fragment == nil else { throw ConfigurationError.invalidHost }
            return url
        }
        return Self(token: token, endpoints: endpoints)
    }

    func headers(for endpoint: URL) -> HTTPHeaders? {
        guard ["ws", "wss"].contains(endpoint.scheme?.lowercased() ?? ""),
              endpoint.user == nil, endpoint.password == nil,
              endpoint.path.split(separator: "/").first == "bridgehead",
              endpoints.contains(where: {
                  $0.host?.lowercased() == endpoint.host?.lowercased()
                      && $0.port == (endpoint.port ?? (endpoint.scheme?.lowercased() == "wss" ? 443 : 80))
              }) else { return nil }
        var headers = HTTPHeaders()
        headers.bearerAuthorization = .init(token: token)
        return headers
    }

    public func registerRemoteHosts(on resolver: CellResolverProtocol) throws {
        let route = RemoteCellHostRoute(websocketEndpoint: "bridgehead", schemePreference: .automatic,
                                        pathLayout: .endpointThenPublisherUUID, connectionSharing: .dedicated)
        let hosts = Set(endpoints.compactMap { $0.host?.lowercased() })
        let existing = resolver.remoteCellHostRoutesSnapshot()
        // Resolver routes are keyed by hostname, whereas token scope includes port.
        guard hosts.allSatisfy({ existing[$0] == nil || existing[$0] == route }) else {
            throw ConfigurationError.conflictingRoute
        }
        for host in hosts.sorted() { resolver.registerRemoteCellHost(host, route: route) }
    }
}
