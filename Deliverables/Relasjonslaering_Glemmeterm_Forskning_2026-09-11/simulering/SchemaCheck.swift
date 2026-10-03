import Foundation
struct ResearchDefinitions: Decodable { let goals: [GoalDefinition]; let claims: [ClaimDefinition] }
@main struct Check {
  static func main() throws {
    let data = try Data(contentsOf: URL(fileURLWithPath: CommandLine.arguments[1]))
    let result = try JSONDecoder().decode(ResearchDefinitions.self, from: data)
    precondition(result.goals.count == 3 && result.claims.count == 8)
    precondition(result.goals.allSatisfy { $0.schema == GoalDefinition.schemaID })
    precondition(result.claims.allSatisfy { $0.schema == ClaimDefinition.schemaID })
    print("Decoded 3 GoalDefinition and 8 ClaimDefinition values using unchanged runtime types.")
  }
}
