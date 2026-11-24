# Dataflyt — konferanse mal og eierskap

```
arrangør (groups-form) <── event.ownedBy ── konferanse-entitet ── template.ref/version ──> mal v0
        │                                          ▲
        └─ liste over arrangementer                │ referanse (uuid)
           (bygges ved dekoding)          deltaker: conference.<konferanse-uuid>
                                                   └─ entityRepresentationRefs ──> EntityRepresentasjoner (utenfor posten)
```

Lagring: konferanse-, arrangør- og deltakerdata skrives til EntityAnchor under røttene som `EntityTemplateRoots` åpner (CellProtocol #103).

| Kant | Kontrakt |
|---|---|
| konferanse `event.ownedBy` → arrangør-uuid | `conference_entity_template_v0.json#/$defs/Event` |
| arrangør → liste over arrangementer | bygges ved dekoding fra `event.ownedBy`, lagres ikke |
| konferanse `template.ref`/`version` → mal | `#/$defs/Template` |
| deltaker `conference.<uuid>` → konferanse-entitet og EntityRepresentasjoner | `#/$defs/ParticipantSlice`, bare referanser |
| utvidelse brukt av flere → forslag til mal | `#/$defs/TemplateProposal` |
