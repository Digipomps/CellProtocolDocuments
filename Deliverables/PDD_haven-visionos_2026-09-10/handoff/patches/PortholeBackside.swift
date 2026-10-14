// SPDX-License-Identifier: Apache-2.0
// SPDX-FileCopyrightText: Copyright (c) 2026 Stiftelsen Digipomps and HAVEN contributors
//
// Baksiden av Porthole-flaten.
// PDD haven-visionos (CellProtocolDocuments::Deliverables/PDD_haven-visionos_2026-09-10), gren B:
// purpose://candidate.porthole.backside — blad .flip og .honest-absence.
//
// Flaten viser hvilke datastrømmer som leveres til Porthole:
//   Absorbert  – cellReferences i den lastede CellConfiguration (label, endepunkt, set-nøkler)
//   Abonnert   – subscribeFeed og underabonnementer per referanse
//   Puls       – FlowElements som har truffet Porthole, med ankomsttid (FlowElement har ikke tidsstempel)
//   Set/get    – finnes ikke som strukturert strøm i dag (bare tekstlinjen fra CellResolver.logAction),
//                og vises derfor i ærlig fravær-tilstand til F3 (purpose://candidate.cell.interaction-events).
// Tilstand per referanse kommer fra GeneralCell.attachedStatuses: ikke koblet / stille / lest.
// «uleselig» (element mottatt men ikke dekodbart) måles ikke i denne skiven og påstås derfor ikke.

import Foundation
import SwiftUI
import CellBase

// MARK: - Modell

public struct PortholeBacksideReference: Identifiable, Hashable {
    public enum State: String {
        case read = "lest"
        case quiet = "stille"
        case notConnected = "ikke koblet"
        case unknown = "status ikke hentet"
    }

    public var id: String { label + "|" + endpoint }
    public let label: String
    public let endpoint: String
    public let subscribeFeed: Bool
    public let subscriptions: [String]
    public let setKeys: [String]
    public let connected: Bool?
    public let active: Bool?
    public let lastPulse: Date?

    public init(label: String, endpoint: String, subscribeFeed: Bool, subscriptions: [String], setKeys: [String], connected: Bool?, active: Bool?, lastPulse: Date?) {
        self.label = label
        self.endpoint = endpoint
        self.subscribeFeed = subscribeFeed
        self.subscriptions = subscriptions
        self.setKeys = setKeys
        self.connected = connected
        self.active = active
        self.lastPulse = lastPulse
    }

    public var state: State {
        guard let connected else { return .unknown }
        if !connected { return .notConnected }
        if lastPulse != nil { return .read }
        return .quiet
    }
}

public struct PortholePulseEntry: Identifiable, Hashable {
    public let id: String
    public let receivedAt: Date
    public let title: String
    public let topic: String
    public let origin: String?
    public let kind: String
    public let label: String?

    public init(id: String = UUID().uuidString, receivedAt: Date, title: String, topic: String, origin: String?, kind: String, label: String?) {
        self.id = id
        self.receivedAt = receivedAt
        self.title = title
        self.topic = topic
        self.origin = origin
        self.kind = kind
        self.label = label
    }
}

public struct PortholeBacksideSnapshot {
    public var configurationName: String?
    public var references: [PortholeBacksideReference]
    public var statusCount: Int
    public var capturedAt: Date
    public var statusError: String?

    public init(configurationName: String?, references: [PortholeBacksideReference], statusCount: Int, capturedAt: Date, statusError: String?) {
        self.configurationName = configurationName
        self.references = references
        self.statusCount = statusCount
        self.capturedAt = capturedAt
        self.statusError = statusError
    }
}

// MARK: - Flipp

/// Legger en forside og en bakside i samme ramme og snur mellom dem rundt y-aksen.
/// Knappen nederst til høyre snur; verten eier tilstanden.
public struct PortholeFlipContainer<Front: View, Back: View>: View {
    public var showsBackside: Bool
    public var onToggle: () -> Void
    private let front: Front
    private let back: Back

    public init(showsBackside: Bool, onToggle: @escaping () -> Void, @ViewBuilder front: () -> Front, @ViewBuilder back: () -> Back) {
        self.showsBackside = showsBackside
        self.onToggle = onToggle
        self.front = front()
        self.back = back()
    }

    public var body: some View {
        ZStack {
            front
                .opacity(showsBackside ? 0 : 1)
                .rotation3DEffect(.degrees(showsBackside ? 180 : 0), axis: (x: 0, y: 1, z: 0), perspective: 0.5)
                .allowsHitTesting(!showsBackside)
                .accessibilityHidden(showsBackside)
            back
                .opacity(showsBackside ? 1 : 0)
                .rotation3DEffect(.degrees(showsBackside ? 0 : -180), axis: (x: 0, y: 1, z: 0), perspective: 0.5)
                .allowsHitTesting(showsBackside)
                .accessibilityHidden(!showsBackside)
        }
        .animation(.easeInOut(duration: 0.45), value: showsBackside)
        .overlay(alignment: .bottomTrailing) {
            Button(action: onToggle) {
                Label(showsBackside ? "Forside" : "Bakside", systemImage: "arrow.2.squarepath")
                    .font(.caption)
            }
            .buttonStyle(.bordered)
            .padding(12)
            .accessibilityLabel(showsBackside ? "Snu til forsiden" : "Snu til baksiden")
        }
    }
}

// MARK: - Bakside-flaten

public struct PortholeBacksideView: View {
    @ObservedObject private var viewModel: PortholeBindingViewModel
    /// Konfigurasjonen verten selv viser (f.eks. ContentView.activeConfiguration). Brukes når Porthole-cellen
    /// ikke er koblet til ennå eller ikke har lastet noen konfigurasjon — da vises referansene som «ikke koblet».
    private let fallbackConfiguration: CellConfiguration?

    public init(viewModel: PortholeBindingViewModel, fallbackConfiguration: CellConfiguration? = nil) {
        self.viewModel = viewModel
        self.fallbackConfiguration = fallbackConfiguration
    }

    private static let timeFormatter: DateFormatter = {
        let formatter = DateFormatter()
        formatter.dateFormat = "HH:mm:ss"
        return formatter
    }()

    public var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 16) {
                header
                zone(title: "Absorbert", count: viewModel.backside?.references.count) {
                    absorbedRows
                }
                zone(title: "Abonnert", count: subscribedCount) {
                    subscribedRows
                }
                zone(title: "Puls", count: viewModel.pulse.count) {
                    pulseRows
                }
                zone(title: "Set / get", count: nil) {
                    absenceRow(
                        symbol: "bolt.slash",
                        title: "Ikke koblet",
                        detail: "Set og get logges i dag bare som tekstlinje (CellResolver.logAction). Strukturert hendelsesstrøm er formålet purpose://candidate.cell.interaction-events (F3) og er ikke bygget ennå."
                    )
                }
                legend
            }
            .padding(16)
        }
        .background(.regularMaterial)
        .task {
            await viewModel.refreshBackside(fallback: fallbackConfiguration)
        }
        .onReceive(viewModel.$pulse) { _ in
            Task { await viewModel.refreshBackside(fallback: fallbackConfiguration) }
        }
    }

    // MARK: Deler

    private var header: some View {
        HStack(alignment: .firstTextBaseline) {
            VStack(alignment: .leading, spacing: 2) {
                Text("Bakside")
                    .font(.title3.weight(.semibold))
                Text(headerSubtitle)
                    .font(.caption)
                    .foregroundStyle(.secondary)
            }
            Spacer()
            Button {
                Task { await viewModel.refreshBackside(fallback: fallbackConfiguration) }
            } label: {
                Label("Oppdater", systemImage: "arrow.clockwise")
                    .font(.caption)
            }
            .buttonStyle(.bordered)
        }
    }

    private var headerSubtitle: String {
        guard let snapshot = viewModel.backside else {
            return "Henter datastrømmer …"
        }
        let name = snapshot.configurationName ?? "ingen konfigurasjon lastet"
        let time = Self.timeFormatter.string(from: snapshot.capturedAt)
        if let error = snapshot.statusError {
            return "\(name) · lest \(time) · status: \(error)"
        }
        return "\(name) · lest \(time) · \(snapshot.statusCount) tilkoblingsstatus(er)"
    }

    private var subscribedCount: Int? {
        guard let references = viewModel.backside?.references else { return nil }
        return references.filter { $0.subscribeFeed }.count + references.reduce(0) { $0 + $1.subscriptions.count }
    }

    @ViewBuilder
    private var absorbedRows: some View {
        if let snapshot = viewModel.backside {
            if snapshot.references.isEmpty {
                absenceRow(symbol: "tray", title: "Ingen celler absorbert", detail: snapshot.configurationName == nil
                    ? "Ingen CellConfiguration er lastet i Porthole."
                    : "Konfigurasjonen «\(snapshot.configurationName ?? "")» har ingen cellReferences.")
            } else {
                ForEach(snapshot.references) { reference in
                    HStack(alignment: .top, spacing: 10) {
                        stateDot(reference.state)
                        VStack(alignment: .leading, spacing: 2) {
                            Text(reference.label)
                                .font(.subheadline.weight(.medium))
                            Text(reference.endpoint)
                                .font(.caption.monospaced())
                                .foregroundStyle(.secondary)
                                .lineLimit(1)
                                .truncationMode(.middle)
                            if !reference.setKeys.isEmpty {
                                Text("set ved lasting: " + reference.setKeys.joined(separator: ", "))
                                    .font(.caption2)
                                    .foregroundStyle(.secondary)
                            }
                        }
                        Spacer()
                        Text(reference.state.rawValue)
                            .font(.caption2.weight(.semibold))
                            .padding(.horizontal, 6)
                            .padding(.vertical, 2)
                            .background(stateColor(reference.state).opacity(0.18), in: Capsule())
                    }
                }
            }
        } else {
            ProgressView()
        }
    }

    @ViewBuilder
    private var subscribedRows: some View {
        if let snapshot = viewModel.backside {
            let subscribed = snapshot.references.filter { $0.subscribeFeed || !$0.subscriptions.isEmpty }
            if subscribed.isEmpty {
                absenceRow(symbol: "antenna.radiowaves.left.and.right.slash", title: "Ingen abonnement", detail: "Ingen referanse har subscribeFeed eller underabonnement.")
            } else {
                ForEach(subscribed) { reference in
                    VStack(alignment: .leading, spacing: 2) {
                        HStack(spacing: 8) {
                            Image(systemName: reference.subscribeFeed ? "antenna.radiowaves.left.and.right" : "antenna.radiowaves.left.and.right.slash")
                                .foregroundStyle(reference.subscribeFeed ? Color.accentColor : Color.secondary)
                            Text(reference.label)
                                .font(.subheadline.weight(.medium))
                            Spacer()
                            if let lastPulse = reference.lastPulse {
                                Text("sist " + Self.timeFormatter.string(from: lastPulse))
                                    .font(.caption2)
                                    .foregroundStyle(.secondary)
                            } else {
                                Text("ingen elementer ennå")
                                    .font(.caption2)
                                    .foregroundStyle(.secondary)
                            }
                        }
                        ForEach(reference.subscriptions, id: \.self) { endpoint in
                            Text("↳ " + endpoint)
                                .font(.caption.monospaced())
                                .foregroundStyle(.secondary)
                                .lineLimit(1)
                                .truncationMode(.middle)
                        }
                    }
                }
            }
        } else {
            ProgressView()
        }
    }

    @ViewBuilder
    private var pulseRows: some View {
        if viewModel.pulse.isEmpty {
            absenceRow(symbol: "waveform.path", title: "Stille", detail: "Ingen FlowElements har truffet Porthole siden appen startet.")
        } else {
            ForEach(viewModel.pulse) { entry in
                HStack(alignment: .top, spacing: 10) {
                    Text(Self.timeFormatter.string(from: entry.receivedAt))
                        .font(.caption.monospaced())
                        .foregroundStyle(.secondary)
                    VStack(alignment: .leading, spacing: 1) {
                        Text(entry.title.isEmpty ? "(uten tittel)" : entry.title)
                            .font(.caption.weight(.medium))
                            .lineLimit(1)
                        Text((entry.label ?? "ukjent opphav") + " · " + entry.kind + " · " + entry.topic)
                            .font(.caption2)
                            .foregroundStyle(.secondary)
                            .lineLimit(1)
                    }
                    Spacer()
                }
            }
        }
    }

    private var legend: some View {
        VStack(alignment: .leading, spacing: 4) {
            Text("Tilstander")
                .font(.caption.weight(.semibold))
            HStack(spacing: 12) {
                legendItem(.read, "lest — koblet og elementer mottatt")
                legendItem(.quiet, "stille — koblet, ingen elementer")
                legendItem(.notConnected, "ikke koblet")
            }
            .font(.caption2)
            Text("«uleselig» måles ikke i denne skiven.")
                .font(.caption2)
                .foregroundStyle(.secondary)
        }
    }

    private func legendItem(_ state: PortholeBacksideReference.State, _ text: String) -> some View {
        HStack(spacing: 4) {
            stateDot(state)
            Text(text)
        }
    }

    private func zone<Content: View>(title: String, count: Int?, @ViewBuilder content: () -> Content) -> some View {
        VStack(alignment: .leading, spacing: 8) {
            HStack {
                Text(title)
                    .font(.headline)
                if let count {
                    Text("\(count)")
                        .font(.caption.weight(.semibold))
                        .padding(.horizontal, 6)
                        .padding(.vertical, 1)
                        .background(Color.secondary.opacity(0.15), in: Capsule())
                }
                Spacer()
            }
            content()
        }
        .padding(12)
        .frame(maxWidth: .infinity, alignment: .leading)
        .background(.thinMaterial, in: RoundedRectangle(cornerRadius: 12, style: .continuous))
    }

    private func absenceRow(symbol: String, title: String, detail: String) -> some View {
        HStack(alignment: .top, spacing: 10) {
            Image(systemName: symbol)
                .foregroundStyle(.secondary)
            VStack(alignment: .leading, spacing: 2) {
                Text(title)
                    .font(.subheadline.weight(.medium))
                Text(detail)
                    .font(.caption)
                    .foregroundStyle(.secondary)
            }
            Spacer()
        }
    }

    private func stateDot(_ state: PortholeBacksideReference.State) -> some View {
        Circle()
            .fill(stateColor(state))
            .frame(width: 9, height: 9)
            .padding(.top, 4)
    }

    private func stateColor(_ state: PortholeBacksideReference.State) -> Color {
        switch state {
        case .read: return .green
        case .quiet: return .yellow
        case .notConnected: return .red
        case .unknown: return .gray
        }
    }
}
