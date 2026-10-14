// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "HavenAgentD",
    platforms: [
        .macOS(.v13)
    ],
    products: [
        .library(name: "HavenMacAutomation", targets: ["HavenMacAutomation"]),
        .library(name: "HavenRuntimeBootstrap", targets: ["HavenRuntimeBootstrap"]),
        .library(name: "HavenAgentRuntime", targets: ["HavenAgentRuntime"]),
        .library(name: "HavenAgentCells", targets: ["HavenAgentCells"]),
        .library(name: "HavenAgentCellRuntime", targets: ["HavenAgentCellRuntime"]),
        .executable(name: "haven-agentd", targets: ["HavenAgentD"]),
        .executable(name: "haven-agentd-mcp", targets: ["HavenAgentDMCP"]),
        .executable(name: "haven-correspondence-mcp", targets: ["HavenCorrespondenceMCP"])
    ],
    dependencies: [
        .package(
            url: "https://github.com/Digipomps/CellProtocol.git",
            revision: "b5b7282b495e96a7899a189087592581426f4bfb"
        ),
        .package(
            url: "https://github.com/Digipomps/Sprout.git",
            revision: "473d6998bf5417c6355de053fe806ebdf91383e6"
        ),
        .package(url: "https://github.com/vapor/vapor.git", from: "4.0.1")
    ],
    targets: [
        .target(
            name: "HavenMacAutomation"
        ),
        .target(
            name: "HavenRuntimeBootstrap"
        ),
        .target(
            name: "HavenAgentRuntime",
            dependencies: [
                "HavenMacAutomation",
                "HavenRuntimeBootstrap",
                .product(name: "CellBase", package: "CellProtocol"),
                .product(name: "SproutAppSupport", package: "sprout"),
                .product(name: "SproutCore", package: "sprout"),
                .product(name: "SproutCrypto", package: "sprout"),
                .product(name: "SproutResolverAdapter", package: "sprout")
            ]
        ),
        .target(
            name: "HavenAgentCells",
            dependencies: [
                "HavenAgentRuntime",
                "HavenMacAutomation",
                .product(name: "CellBase", package: "CellProtocol"),
                .product(name: "CellApple", package: "CellProtocol"),
                .product(name: "SproutCrypto", package: "sprout")
            ]
        ),
        .target(
            name: "HavenAgentCellRuntime",
            dependencies: [
                "HavenMacAutomation",
                "HavenAgentRuntime",
                "HavenAgentCells",
                "HavenRuntimeBootstrap",
                .product(name: "CellBase", package: "CellProtocol"),
                .product(name: "CellVapor", package: "CellProtocol"),
                .product(name: "Vapor", package: "vapor")
            ],
            resources: [
                .copy("Resources")
            ]
        ),
        .executableTarget(
            name: "HavenAgentD",
            dependencies: [
                "HavenAgentRuntime",
                "HavenRuntimeBootstrap",
                "HavenMacAutomation",
                "HavenAgentCells",
                "HavenAgentCellRuntime",
                .product(name: "SproutCore", package: "sprout"),
                .product(name: "SproutCrypto", package: "sprout"),
                .product(name: "SproutResolverAdapter", package: "sprout")
            ]
        ),
        .executableTarget(
            name: "HavenAgentDMCP",
            dependencies: [
                "HavenMacAutomation",
                "HavenAgentRuntime",
                "HavenRuntimeBootstrap",
                "HavenAgentCells",
                "HavenAgentCellRuntime"
            ]
        ),
        .executableTarget(
            name: "HavenCorrespondenceMCP",
            dependencies: [
                "HavenAgentRuntime",
                .product(name: "CellBase", package: "CellProtocol")
            ]
        ),
        .testTarget(
            name: "HavenMacAutomationTests",
            dependencies: [
                "HavenMacAutomation"
            ]
        ),
        .testTarget(
            name: "HavenAgentRuntimeTests",
            dependencies: [
                "HavenAgentRuntime",
                "HavenRuntimeBootstrap",
                "HavenMacAutomation",
                .product(name: "SproutResolverAdapter", package: "sprout"),
                .product(name: "SproutCrypto", package: "sprout")
            ]
        ),
        .testTarget(
            name: "HavenAgentCellsTests",
            dependencies: [
                "HavenAgentCellRuntime",
                "HavenAgentCells",
                .product(name: "CellBase", package: "CellProtocol")
            ]
        ),
        .testTarget(
            name: "HavenAgentCellRuntimeTests",
            dependencies: [
                "HavenAgentCellRuntime",
                "HavenAgentCells",
                "HavenRuntimeBootstrap",
                .product(name: "CellBase", package: "CellProtocol"),
                .product(name: "SproutCrypto", package: "sprout")
            ]
        ),
        .testTarget(
            name: "HavenAgentDMCPTests",
            dependencies: [
                "HavenAgentDMCP",
                "HavenAgentCellRuntime",
                "HavenMacAutomation",
                "HavenAgentRuntime",
                "HavenRuntimeBootstrap",
                .product(name: "SproutCrypto", package: "sprout")
            ]
        ),
        .testTarget(
            name: "HavenCorrespondenceMCPTests",
            dependencies: [
                "HavenCorrespondenceMCP",
                "HavenAgentRuntime",
                .product(name: "CellBase", package: "CellProtocol")
            ]
        )
    ]
)
