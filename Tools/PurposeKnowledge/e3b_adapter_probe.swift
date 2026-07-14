// E3b Step 0: prove that this Swift SDK/runtime exposes the custom-adapter path.
// With no argument, the probe intentionally uses a missing .fmadapter asset.
// Pass a real adapter path later to exercise compile + model construction.
import Foundation
import FoundationModels

@main
struct E3bAdapterProbe {
    static func main() async {
        let suppliedPath = CommandLine.arguments.dropFirst().first
        let adapterURL = URL(
            fileURLWithPath: suppliedPath ?? "/tmp/e3b_intentionally_missing_adapter.fmadapter"
        )

        print("default_model_availability=\(SystemLanguageModel.default.availability)")
        print("adapter_path=\(adapterURL.path)")

        do {
            let adapter = try SystemLanguageModel.Adapter(fileURL: adapterURL)
            print("adapter_asset_initialized=true")
            print("creator_metadata=\(adapter.creatorDefinedMetadata)")

            try await adapter.compile()
            print("adapter_compile_succeeded=true")

            let model = SystemLanguageModel(adapter: adapter)
            print("adapter_model_constructed=true")
            print("adapter_model_availability=\(model.availability)")
        } catch let error as SystemLanguageModel.Adapter.AssetError {
            // For the default missing path, reaching this public runtime error is
            // the expected positive signal that the adapter-loading API is wired.
            print("adapter_api_reached=true")
            print("adapter_asset_error=\(error)")
            if let suppliedPath {
                fputs("Failed to load supplied adapter at \(suppliedPath): \(error)\n", stderr)
                exit(2)
            }
        } catch {
            fputs("Unexpected adapter-loading error: \(error)\n", stderr)
            exit(3)
        }
    }
}
