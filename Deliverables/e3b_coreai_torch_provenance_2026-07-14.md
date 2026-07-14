# E3b: `coreai-torch` provenance and stop decision

Date checked: 2026-07-14 (Europe/Oslo)

## Decision

**STOP before installation or training.** `coreai-torch` is an official Apple
package, but it is not the Foundation Models adapter-training toolkit and does
not provide the version-locked system-model assets required to train a loadable
`.fmadapter` for the current on-device model.

No package was installed or imported, no package code was executed, no virtual
environment was created, and no weights or training data were produced.

## PyPI provenance

Source: [PyPI JSON API](https://pypi.org/pypi/coreai-torch/json), read-only
response retrieved 2026-07-14.

- Project: `coreai-torch`
- Latest version at check time: `0.4.1`
- Release upload: 2026-07-01 23:11:00–23:11:02 UTC
- PyPI ownership metadata: organization `apple`; no individual role entries
- `author`, `author_email`, `maintainer`, and `maintainer_email`: unset
- Project URLs: `https://github.com/apple/coreai-torch` for homepage and
  repository, and the corresponding repository issue tracker
- Summary: “Convert PyTorch models to CoreAI format”
- License metadata: Apple Inc. copyright 2026, BSD 3-Clause
- Published artifacts: a 199,132-byte universal Python wheel and a
  212,648-byte source archive
- Source archive SHA-256:
  `2499429cc94f9e487122420b36b84c83b39a142505c4a54572572147bccc50fa`

The ownership block and project URLs establish that the PyPI project is tied to
Apple's real GitHub organization. PyPI does not name an individual publisher.

## GitHub provenance and actual purpose

Sources:

- [apple/coreai-torch](https://github.com/apple/coreai-torch)
- [README](https://github.com/apple/coreai-torch/blob/main/README.md)
- [License](https://github.com/apple/coreai-torch/blob/main/LICENSE)
- [Package metadata](https://github.com/apple/coreai-torch/blob/main/pyproject.toml)
- [Source manifest](https://github.com/apple/coreai-torch/blob/main/MANIFEST.in)

Repository metadata identifies owner `apple` as a GitHub Organization (owner
ID `10639145`) and the public repository as ID `1250651738`, with default branch
`main`. The license is BSD 3-Clause with Apple Inc. copyright 2026.

The README describes `coreai-torch` as a bridge from PyTorch to Core AI IR. Its
public entry point, `TorchConverter`, lowers `torch.export.ExportedProgram`
operations to Core AI dialect operations. It also supports custom lowerings,
composite operations, externalized submodules, and inline Metal kernels. This
is model conversion/authoring infrastructure for the Core AI inference stack.

It is **not** described as tooling for any of the required E3b steps:

- fine-tuning Apple's on-device Foundation Model;
- rank-32 LoRA adapter training;
- exporting `.fmadapter` bundles;
- matching an adapter to a system-model version; or
- distributing the adapter through Background Assets.

Repository searches returned no matches for `adapter` or `fmadapter`. The
package metadata declares conversion dependencies such as `coreai-core` and
PyTorch. Its package-data and source manifests include Python source and
`py.typed`, not model checkpoints or Foundation Models assets.

## Version-locked assets

`coreai-torch` does not include a Foundation Models base-model checkpoint,
version manifest for the installed system model, tokenizer/training asset
bundle, or other version-locked model resources. The small, platform-neutral
wheel/source archive and the explicit source manifest independently rule out
the gated model assets being embedded in this package.

Apple documents adapter training separately at
[Foundation Models adapter training](https://developer.apple.com/apple-intelligence/foundation-models-adapter/).
That is the relevant product path; the inspected `coreai-torch` README and
package metadata do not identify `coreai-torch` as its toolkit.

## What remains missing

E3b remains blocked pending an official Apple Foundation Models adapter toolkit
bundle that provides all of the following for the system model installed on
this Mac:

1. the exact target base-model identifier/version;
2. the matching version-locked training/model assets;
3. the Foundation Models fine-tuning and rank-32 LoRA training workflow;
4. the supported `.fmadapter` export/compile utilities; and
5. the documented Background Assets packaging/distribution workflow.

Once that bundle is obtained, its model-version manifest must be checked against
the current on-device model before the planned smoke test. Only after the smoke
adapter loads and produces a harness score should the full rank-32 E3b run
start. The held-out E3 split remains case index `% 5 >= 3` and must not be used
for training.

## Baseline retained for the future run

- Gated held-out: 85%
- Selection-only: 96%
- Over-selection YES-rate: 87%

No E3b metric is reported because training did not start.
