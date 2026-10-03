import Foundation
import XCTest
@main struct Main {
 static func main() {
   let suite = RelationalLearningEngineTests.defaultTestSuite
   suite.run()
   let run = suite.testRun!
   print("Executed \(run.executionCount) tests, failures \(run.totalFailureCount), success \(run.hasSucceeded)")
   exit(run.hasSucceeded && run.executionCount == 7 ? 0 : 1)
 }
}
