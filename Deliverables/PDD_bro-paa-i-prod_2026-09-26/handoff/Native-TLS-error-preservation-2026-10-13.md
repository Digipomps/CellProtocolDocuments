# Native TLS failure preservation — local candidate

WebSocketTaskConnection2 now retains the first current-task native failure before
notifying a delegate that may close the gate. Receive and task completion share
this decision; startup covers resume, receive admission and waiting for open.
No trust handler, anchor override, ATS exception, wire change or resolver/identity
relaxation is introduced. Explicitly closed connections remain closed.

Final candidate fbe9b1ff12741f19ab5542acfc6430f827fba509 includes published2026.9.9
compatibility and a repaired concurrent-Flow test race.1700 full package tests
pass locally (five skips), and10focused Thread Sanitizer tests pass without a
sanitizer report. Seven native error-preservation regressions are included.
Stale and duplicate failures cannot replace the first current-task failure. An
observed subscription barrier covers failure during an active connect wait.
Mutation evidence proves the removed retention/publication matters; only the
first test completed red before a duplicate-fulfillment test abort. Full fixed
source was restored and tested after that mutation.

Foundation's WSS NSError may omit the public peer-trust and failing-URL metadata
that HTTPS provides; error preservation does not guarantee that metadata exists.
The Binding certificate test uses exact native certificate rejection and an
outgoing certificate-emission witness plus a separate ordinary OS hostname-policy
check. The latter is not represented as URLSession's original underlying error.

CS native fixture holds its irreversibly unprivileged socket creator and original
FD until owner cleanup; the creator has a separate stop marker and210second bound.
Keeping only the process alive produced intermittent local errors; keeping the FD
passed30 consecutive controls. Hosted macOS Admin trust removal remains unresolved.
No new CI acceptance, release image or deploy is established by this note.

The repaired Flow test now observes actual shared pending-flight selection
before releasing the upstream failure; Task.yield was not an admission barrier.
The former full-suite hang and intermediate fixture failures remain in evidence.

Evidence: CellScaffold/Documentation/Evidence/BridgeRollout-2026-10-12/
Native-TLS-current-checkpoint-20261013.md and tls-diagnostics-local-20261013/.
