#!/usr/bin/env swift
// E3: Apple on-device Foundation Models guided-generation micro-task.
// Reads e3_input.json (Norwegian prompt + English candidate descriptions),
// runs one @Generable yes/no/unsure verdict per candidate (constrained
// decoding = zero format failures), writes answers JSONL. macOS 26 + Apple
// Intelligence required.
import FoundationModels
import Foundation

@Generable
enum Verdict: String { case yes, no, unsure }

@Generable
struct MicroAnswer {
    @Guide(description: "yes if the request requires this purpose, no if not, unsure if genuinely unclear")
    let verdict: Verdict
}

struct Candidate: Codable { let ref: String; let resolverScore: Double; let title: String; let summary: String; let goalOutcome: String }
struct Case: Codable { let id: String; let prompt: String; let candidates: [Candidate] }

let inputPath = CommandLine.arguments.count > 1 ? CommandLine.arguments[1] : "e3_input.json"
let outPath = CommandLine.arguments.count > 2 ? CommandLine.arguments[2] : "e3_apple_answers.jsonl"

let data = try Data(contentsOf: URL(fileURLWithPath: inputPath))
let cases = try JSONDecoder().decode([Case].self, from: data)

let model = SystemLanguageModel.default
guard case .available = model.availability else {
    FileHandle.standardError.write("model unavailable\n".data(using: .utf8)!)
    exit(1)
}

var lines: [String] = []
var done = 0
let total = cases.reduce(0) { $0 + $1.candidates.count }
let start = Date()

for c in cases {
    for cand in c.candidates {
        let prompt = """
        A user wrote this request to a software assistant:
        "\(c.prompt)"

        Candidate purpose from our taxonomy:
        \(cand.ref) — \(cand.title)
        Summary: \(cand.summary)
        Goal outcome: \(cand.goalOutcome)

        Question: Does fulfilling the user's request require this purpose? Consider it required if the request clearly needs it, even implicitly.
        """
        // Fresh session per candidate keeps judgments independent (no transcript carryover).
        let session = LanguageModelSession()
        var verdict = "error"
        var attempt = 0
        while attempt < 3 {
            attempt += 1
            do {
                let r = try await session.respond(to: prompt, generating: MicroAnswer.self)
                verdict = r.content.verdict.rawValue
                break
            } catch {
                if attempt == 3 {
                    verdict = "error"
                    FileHandle.standardError.write("err \(cand.ref): \(error)\n".data(using: .utf8)!)
                }
            }
        }
        let esc = { (s: String) in s.replacingOccurrences(of: "\\", with: "\\\\").replacingOccurrences(of: "\"", with: "\\\"") }
        lines.append("{\"caseID\":\"\(esc(c.id))\",\"ref\":\"\(esc(cand.ref))\",\"resolverScore\":\(cand.resolverScore),\"answer\":\"\(verdict)\"}")
        done += 1
        if done % 25 == 0 {
            let rate = Double(done) / Date().timeIntervalSince(start)
            FileHandle.standardError.write("  \(done)/\(total) (\(String(format: "%.1f", rate))/s)\n".data(using: .utf8)!)
        }
    }
}

try lines.joined(separator: "\n").appending("\n").write(toFile: outPath, atomically: true, encoding: .utf8)
FileHandle.standardError.write("wrote \(outPath): \(lines.count) answers in \(String(format: "%.0f", Date().timeIntervalSince(start)))s\n".data(using: .utf8)!)