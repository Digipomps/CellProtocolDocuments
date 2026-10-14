# Bounded review: local AdminWorkspace lookup exception

Reviewed the uncommitted change in `PortholeWebSessionSupport.swift` and the two new `PortholeWebRemoteConfigurationTests` against candidate `f26c16fe`. Read-only; no tests/builds or source changes.

## Finding

**P1 — Every legitimate admin lookup misses the new switch.** [The helper switches on `lookup.name`](/private/tmp/haven-prod-20260917/CellScaffold/Sources/App/Controllers/PortholeWebSessionSupport.swift:4445) using mixed-case factory constants such as `Admin Control Plane Overview`. However [decodeLookupObject](/private/tmp/haven-prod-20260917/CellScaffold/Sources/App/Controllers/PortholeWebPayloads.swift:180) applies `normalizedLookupToken`, which [lowercases every name](/private/tmp/haven-prod-20260917/CellScaffold/Sources/App/Controllers/PortholeWebPayloads.swift:199). Therefore the helper returns nil for all four built-in names and the original remote-export admission still throws `Remote configuration lookup requires an explicit keypath.`

Smallest correction: compare the decoded name against factory names normalized with the existing name-normalization contract. Keep the endpoint comparison exact. The newly added positive test, which covers all four names with and without a catalogue UUID, should detect this failure. Root was notified immediately.

**Follow-up:** root applied `.lowercased()` to all four factory constants. I independently reread the diff and confirmed the correction while the endpoint equality remains unchanged. The source defect is resolved; root is rerunning the targeted tests. No remaining concrete findings in the bounded review.

## Other reviewed boundaries

No additional concrete authorization or overlay defect found in this change. The helper returns only one of four compiled factories, requires the current factory endpoint, rejects decoded configuration bodies and nonempty explicit keypaths, and does not read the caller's UUID as authority. A factory is presentation, not a data grant. [The normal load path](/private/tmp/haven-prod-20260917/CellScaffold/Sources/App/Controllers/PortholeWebSessionSupport.swift:5296) still checks publication, applies the requester-bound source overlay, computes reference requesters and loads through existing resolver/transport access checks. The new early return is before those steps, inside configuration selection only.

The new tests meaningfully check factory replacement of stale active state, skeleton/reference identity, nonmatching endpoints/names, explicit exports and matching-UUID rejection without resolver calls. They directly call the selection function; they do not demonstrate a full authenticated remote data read or denial. They also do not contain a mixed lookup-plus-configuration-body negative case, although the implementation guard for that case is present. These are evidence limits, not additional demonstrated defects.
