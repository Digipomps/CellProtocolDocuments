import Foundation
struct Query: Codable { var at: Double; var snapshot: RelationalContextSnapshot }
struct Input: Codable { var events: [RelationalLearningEventEnvelope]; var queries: [Query]; var config: RelationalLearningConfig? }
struct Output: Codable {
    var edges: [RelationalEdge]
    var scores: [[RelationalPurposeScore]]
    var generatedUpdates: [RelationalWeightUpdateEvent]
    var journal: RelationalLearningPersistedJournal
    var replayEqual: Bool
    var restoreEqual: Bool
    var weightOnlyEqual: Bool
    var mixedReplayEqual: Bool
}
func bytes<T: Encodable>(_ x: T) throws -> Data { let enc = JSONEncoder(); enc.outputFormatting = [.sortedKeys]; return try enc.encode(x) }
@main struct Oracle {
    static func main() async throws {
        let input = try JSONDecoder().decode(Input.self, from: FileHandle.standardInput.readDataToEndOfFile())
        let engine = RelationalLearningEngine(config: input.config ?? .default)
        var updates: [RelationalWeightUpdateEvent] = []
        for event in input.events { updates += try await engine.applyEnvelopeTransaction(event).weightUpdates }
        let edges = await engine.edges()
        let journal = await engine.journalSnapshot()
        var scores: [[RelationalPurposeScore]] = []
        for query in input.queries { scores.append(await engine.scorePurposes(contextSnapshot: query.snapshot, at: query.at, explainTopN: 10000)) }
        let replayer = RelationalLearningEngine(config: input.config ?? .default)
        _ = try await replayer.replayTransaction(events: input.events, resetFirst: true)
        let replayEdges = await replayer.edges()
        let restored = RelationalLearningEngine(config: input.config ?? .default)
        try await restored.restore(from: journal)
        let restoreEdges = await restored.edges()
        let weights = RelationalLearningEngine(config: input.config ?? .default)
        let weightEnvelopes = try updates.map { try RelationalLearningEventEnvelope.from($0) }
        _ = try await weights.replayTransaction(events: weightEnvelopes, resetFirst: true)
        let weightEdges = await weights.edges()
        let mixed = RelationalLearningEngine(config: input.config ?? .default)
        _ = try await mixed.replayTransaction(events: input.events + weightEnvelopes, resetFirst: true)
        let mixedEdges = await mixed.edges()
        let output = try Output(edges: edges, scores: scores, generatedUpdates: updates, journal: journal,
            replayEqual: bytes(edges) == bytes(replayEdges), restoreEqual: bytes(edges) == bytes(restoreEdges),
            weightOnlyEqual: bytes(edges) == bytes(weightEdges), mixedReplayEqual: bytes(edges) == bytes(mixedEdges))
        FileHandle.standardOutput.write(try bytes(output))
        FileHandle.standardOutput.write(Data("\n".utf8))
    }
}
