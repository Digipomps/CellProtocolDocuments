import CoreGraphics
import Foundation
import Darwin

// Only window metadata: no image capture or permission request APIs.
guard CommandLine.arguments.count == 2,
      let ownerPID = Int32(CommandLine.arguments[1]), ownerPID > 0 else {
    fputs("Usage: window-list <owner-pid>\n", stderr)
    exit(64)
}

let raw = CGWindowListCopyWindowInfo(.optionAll, kCGNullWindowID)
var result: [String: Any] = [
    "timestampUTC": ISO8601DateFormatter().string(from: Date()),
    "probePID": getpid(),
    "targetPID": ownerPID,
    "api": "CGWindowListCopyWindowInfo",
    "options": "kCGWindowListOptionAll",
    "relativeToWindow": kCGNullWindowID,
    "returnedNull": raw == nil,
]
var status: Int32 = 0
if let windows = raw as? [[String: Any]] {
    result["totalWindowCount"] = windows.count
    let owned = windows.filter {
        ($0[kCGWindowOwnerPID as String] as? NSNumber)?.int32Value == ownerPID
    }
    result["targetWindowCount"] = owned.count
    result["windows"] = owned
    // An empty global list is not evidence that this app has no windows.
    if windows.isEmpty { status = 3 }
} else {
    result["error"] = "CGWindowListCopyWindowInfo returned NULL or a non-dictionary array"
    status = 2
}
let json = try JSONSerialization.data(withJSONObject: result, options: [.prettyPrinted, .sortedKeys])
FileHandle.standardOutput.write(json)
FileHandle.standardOutput.write(Data("\n".utf8))
exit(status)
