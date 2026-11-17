// Oracle-only support, NOT production CellProtocol types. Restricted plain JSON subset.
import Foundation
import CryptoKit
public typealias Object = [String: ValueType]
public indirect enum ValueType: Codable, Sendable {
    case bool(Bool), number(Int), integer(Int), float(Double), string(String), object(Object), list([ValueType]), null
    public init(from decoder: Decoder) throws {
        let c = try decoder.singleValueContainer()
        if c.decodeNil() { self = .null }
        else if let v = try? c.decode(Bool.self) { self = .bool(v) }
        else if let v = try? c.decode(Int.self) { self = .integer(v) }
        else if let v = try? c.decode(Double.self) { self = .float(v) }
        else if let v = try? c.decode(String.self) { self = .string(v) }
        else if let v = try? c.decode(Object.self) { self = .object(v) }
        else { self = .list(try c.decode([ValueType].self)) }
    }
    public func encode(to encoder: Encoder) throws {
        var c = encoder.singleValueContainer()
        switch self {
        case .bool(let v): try c.encode(v)
        case .number(let v), .integer(let v): try c.encode(v)
        case .float(let v): try c.encode(v)
        case .string(let v): try c.encode(v)
        case .object(let v): try c.encode(v)
        case .list(let v): try c.encode(v)
        case .null: try c.encodeNil()
        }
    }
}
public enum ValueTypeError: Error { case unexpectedValueType }
public struct FlowElement: Sendable { public var content: ValueType; public var topic: String; public var id: String }
public enum FlowHasher {
    public static func sha256Hex(_ data: Data) -> String {
        SHA256.hash(data: data).map { String(format: "%02x", $0) }.joined()
    }
}
