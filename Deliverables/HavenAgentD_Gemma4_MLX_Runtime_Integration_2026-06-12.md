# HAVENAgentD Gemma 4 MLX Runtime Integration

Date: 2026-06-12

Status: integration note for the next HAVENAgentD test round. The Gemma 4
backend itself was verified locally through `mlx_vlm.server`; a full
CellProtocol bridge invocation through AgentD is the next step.

## Why HAVENAgentD

Kjetil was right to push this through HAVENAgentD. Running Gemma directly from
ad-hoc benchmark scripts proves the model works, but it does not prove the
product boundary we actually want.

The useful product shape is:

- MLX/VLM owns accelerated local inference on the MacBook Pro M5.
- HAVENAgentD owns the local model provider profile, loopback boundary,
  credentials boundary and CellProtocol surface.
- Co-pilot, Binding, Porthole or phone/iPad clients call AgentD through HAVEN,
  not the raw model server socket.
- Deterministic policy and action validation stay outside the language model.

This matches the existing AgentD design. `AgentLocalModelCell` already exposes:

- endpoint: `cell:///agent/local-model`
- bridge route: `local-model`
- action keys: `llm.health`, `llm.generate`
- flow topic: `agent.localModel`

It also already sends an OpenAI-compatible chat completion request and decodes
`choices[0].message.content`, which matches `mlx_vlm.server`.

## Verified Backend

The working Gemma backend is:

```bash
/Users/kjetil/Build/Digipomps/HAVEN/CellProtocolDocuments/Artifacts/gemma4-runtime/venv-arm64/bin/python \
  -m mlx_vlm.server \
  --host 127.0.0.1 \
  --port 8094 \
  --model /Users/kjetil/Build/Digipomps/HAVEN/CellProtocolDocuments/Artifacts/gemma4-runtime/mlx/mlx-community-gemma-4-E4B-it-qat-4bit \
  --max-tokens 512 \
  --log-level INFO
```

Verified locally:

- `GET http://127.0.0.1:8094/v1/models`
- `POST http://127.0.0.1:8094/v1/chat/completions`

Important detail:

For this server run, the chat completion request had to use the local model
path as the `model` value:

```text
/Users/kjetil/Build/Digipomps/HAVEN/CellProtocolDocuments/Artifacts/gemma4-runtime/mlx/mlx-community-gemma-4-E4B-it-qat-4bit
```

Using only `gemma-4-E4B-it-qat-4bit` caused the server to try resolving that as
a Hugging Face repo id. AgentD should hide this by exposing a stable provider
id while keeping the local path in its backend config.

## AgentD Environment

Run `haven-agentd` with:

```bash
HAVEN_AGENTD_LOCAL_LLM_PROFILE=gemma4-e4b-qat-mlx-vlm \
HAVEN_AGENTD_LOCAL_LLM_PROVIDER_ID=local.gemma4.e4b.qat.mlx-vlm \
HAVEN_AGENTD_LOCAL_LLM_BASE_URL=http://127.0.0.1:8094 \
HAVEN_AGENTD_LOCAL_LLM_API_PATH=/v1/chat/completions \
HAVEN_AGENTD_LOCAL_LLM_MODEL=/Users/kjetil/Build/Digipomps/HAVEN/CellProtocolDocuments/Artifacts/gemma4-runtime/mlx/mlx-community-gemma-4-E4B-it-qat-4bit \
HAVEN_AGENTD_LOCAL_LLM_TIMEOUT_MS=45000 \
/Users/kjetil/Build/Digipomps/HAVEN/Binding/HavenAgentD/.build/debug/haven-agentd run \
  --config ~/Library/Application\ Support/HAVENAgent/config.json
```

For an isolated local smoke run:

```bash
HAVEN_AGENTD_LOCAL_LLM_PROFILE=gemma4-e4b-qat-mlx-vlm \
HAVEN_AGENTD_LOCAL_LLM_PROVIDER_ID=local.gemma4.e4b.qat.mlx-vlm \
HAVEN_AGENTD_LOCAL_LLM_BASE_URL=http://127.0.0.1:8094 \
HAVEN_AGENTD_LOCAL_LLM_API_PATH=/v1/chat/completions \
HAVEN_AGENTD_LOCAL_LLM_MODEL=/Users/kjetil/Build/Digipomps/HAVEN/CellProtocolDocuments/Artifacts/gemma4-runtime/mlx/mlx-community-gemma-4-E4B-it-qat-4bit \
HAVEN_AGENTD_LOCAL_LLM_TIMEOUT_MS=45000 \
/Users/kjetil/Build/Digipomps/HAVEN/Binding/HavenAgentD/.build/debug/haven-agentd run \
  --root /tmp/haven-gemma4-agentd
```

Because `AgentLocalModelProfile.knownProfiles` does not yet include a Gemma
profile, `selectedProfile` will not resolve to a rich known profile object
until the Binding/HavenAgentD repo is updated. The backend config should still
work because `AgentLocalModelBackendConfig.load()` accepts explicit env values.

## Proposed AgentD Profile

When we update `Binding/HavenAgentD`, add a profile roughly like this:

```swift
public static let gemma4E4BQATMlxVLM = AgentLocalModelProfile(
    id: "gemma4-e4b-qat-mlx-vlm",
    title: "Gemma 4 E4B QAT MLX/VLM",
    summary: "Apple Silicon local Gemma profile for Norwegian Co-pilot and multimodal conference helper experiments.",
    providerID: "local.gemma4.e4b.qat.mlx-vlm",
    model: "/Users/kjetil/Build/Digipomps/HAVEN/CellProtocolDocuments/Artifacts/gemma4-runtime/mlx/mlx-community-gemma-4-E4B-it-qat-4bit",
    repoID: "mlx-community/gemma-4-E4B-it-qat-4bit",
    quantization: "qat-4bit",
    parameterCount: "E4B",
    role: "m5-local-multimodal-conference-assistant",
    defaultPort: 8094,
    purposeRefs: [
        "personal.ai.provider.agent-local-model",
        "personal.ai.provider.gdpr-local-processing",
        "personal.chat.assist.private-local-model",
        "personal.chat.assist.norwegian-language",
        "conference.co-pilot.local-multimodal-helper",
        "agent.local-model.gemma4-m5"
    ],
    interests: [
        "agentd",
        "gemma",
        "mlx",
        "mlx-vlm",
        "apple-silicon",
        "m5",
        "norwegian",
        "norsk",
        "personvern",
        "local",
        "offline",
        "private",
        "conference",
        "multimodal"
    ],
    privacyLevel: "local_agent_loopback_no_external_provider",
    executionScope: "local_agent",
    gdprProcessingNote: "Prompt and response stay on the operator-controlled local AgentD backend when the MLX/VLM server is bound to loopback; Agreement grants, retention policy and logging policy are still required.",
    isExperimental: true,
    sourceURL: "https://huggingface.co/mlx-community/gemma-4-E4B-it-qat-4bit"
)
```

Then add it to `knownProfiles`.

## Credentials And Web Fetching

Credentialed retrieval should be AgentD-owned, not prompt-owned:

- Credentials must not appear in benchmark scripts, prompt text, result JSONL
  files or model logs.
- A credentialed fetch Cell should receive a named source/request, use local
  credentials, and return a bounded sanitized content object.
- The model should receive only the sanitized content and explicit provenance.
- The Cell should record purpose, requester, source, data categories and
  retention expectations through the Agreement/control plane.

That gives us the workflow Kjetil described: if we need credentials for a
network service, AgentD can own the cells that fetch pages with credentials,
while the language model stays behind a safer summarization/classification
boundary.

## Test Cases For The AgentD Path

Minimum next tests:

1. Start `mlx_vlm.server` on `127.0.0.1:8094`.
2. Start `haven-agentd` with the Gemma env values above.
3. Read `cell:///agent/local-model` `state` through the loopback bridge and
   verify:
   - backend base URL is `http://127.0.0.1:8094`;
   - provider id is `local.gemma4.e4b.qat.mlx-vlm`;
   - selected model is the local E4B QAT path.
4. Set `llm.health` with a short health prompt and expect `status=healthy`.
5. Set `llm.generate` with a Norwegian daily-speech conference prompt.
6. Verify an `agent.localModel` flow event.
7. Confirm no raw credential, contact-info or private-data access is available
   to the model.

## Product Position

Use Gemma 4 E4B QAT as:

- local Norwegian helper/drafter;
- multimodal conference-test model;
- screenshot/poster/slide/audio candidate;
- fallback when local/private execution matters.

Do not use it as:

- sponsor-consent authority;
- private contact-info authority;
- autonomous publisher/deleter/scheduler;
- proof that HAVEN has a production-approved local AI assistant.

The model can make the assistant feel competent, but the product competence
must come from good retrieval, explicit Agreements, deterministic policy and
validated actions.
