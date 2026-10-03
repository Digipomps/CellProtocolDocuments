# Dataflyt — «Husk det jeg sa»

```
Hus (PalazzoContent)                 Gjest (PalazzoEntity)                    Hus (PalazzoHouse / StaffShell)
content.draft.apply ─┐
  → proposedTags     │
content.draft.tags.approve           
content.publish ─────┼──► content.signals ──(publisert lesing)──► match.refresh
                     │                                             │ PalazzoOneLayerTagMatcher
                     │                                             ▼
                     │                                        match.pending (owner only)
                     │                                             │ match.open → consent.request(kind: match)
                     │                                             ▼
                     │                                        consent.prompt (modal, 2 grants)
                     │                                             │ match.decide ×2
                     │                                             ▼
                     │                                   kontrakt(er) gjest→hus  ──┐
                     │                                        PalazzoTrustPacket   │
                     │                                             │               ▼
                     │                                        match.shared ──► house.remember.receive ──► staff.state.lastBrief.remembered
                     │                                             │ match.revoke
                     └──────────────────────────────────────────── ┴──────────► house.remember.revoke
```

| # | Fra | Til | Endepunkt/event | Kontrakt |
|---|---|---|---|---|
| 1 | eier (hus) | PalazzoContent | `content.draft.apply` (set) | eksisterende, owner |
| 2 | PalazzoContent | eier | `content.draft.tags.pending` (get) | ny, owner |
| 3 | eier | PalazzoContent | `content.draft.tags.approve` / `.skip` (set) | ny, owner |
| 4 | eier | PalazzoContent | `content.publish` (set) → kompilerer signaler | eksisterende, owner |
| 5 | PalazzoEntity (gjest) | PalazzoContent | `content.signals` (get) | ny, `.ownerPublishedRead` som `content.published` |
| 6 | gjest | PalazzoEntity | `match.refresh` (set) | ny, owner |
| 7 | gjest | PalazzoEntity | `match.pending` / `match.expired` / `match.shared` (get) | ny, owner only — hus avvises |
| 8 | gjest | PalazzoEntity | `match.open` / `match.dismiss` (set) | ny, owner |
| 9 | PalazzoEntity | gjest | `consent.prompt` (get, kind match) | eksisterende, utvidet |
| 10 | gjest | PalazzoEntity | `match.decide` (set) → kontrakt + policy | ny, owner |
| 11 | PalazzoEntity | PalazzoAccessContracts | gjeste-utstedt kontrakt, keypath `match.<id>.verdict` / `.action` | eksisterende mekanisme, ny bruk |
| 12 | PalazzoEntity | PalazzoHouse | `house.remember.receive` (set, payload = TrustPacket) | ny; requester = gjestens identitet |
| 13 | PalazzoHouse | PalazzoStaffShell | `house.remember.list` (get) → `staff.state.lastBrief.remembered` | ny, hus/staff |
| 14 | gjest | PalazzoEntity → PalazzoHouse | `match.revoke` → `house.remember.revoke` | ny |
| 15 | hus | PalazzoEntity | `insight.query.interests.match` | **deprecated** — returnerer status, ingen liste/score |
