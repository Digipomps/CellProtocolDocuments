# Explore Contract Audit

Source root: `/Users/kjetil/.codex/worktrees/perspective-context-events/CellProtocol`

## Summary

- Registration calls inspected after literal expansion: 585
- Handler operations: 335
- Complete contract operations: 324
- Findings: 27
- Errors: 7
- Warnings: 20

## Findings

### ERROR implicit_handler_contract

- Location: `Sources/CellApple/Cells/EntityAnchorCell.swift:149`
- Cell/type: `EntityAnchorCell`
- Key: `agreements`
- Method: `get`
- Message: Handler is not preceded by a complete same-scope Explore contract for this exact key and method. Strict mode may reject it; permissive mode may publish unknown metadata.

### WARN dynamic_key_needs_manual_review

- Location: `Sources/CellApple/Intelligence/AppleIntelligenceCell.swift:361`
- Cell/type: `AppleIntelligenceCell`
- Key: `"\(AIKeys.root).\(key)"`
- Method: `get`
- Message: Handler key or method is computed and cannot be proven by this source audit.

### WARN dynamic_key_needs_manual_review

- Location: `Sources/CellApple/Intelligence/AppleIntelligenceCell.swift:371`
- Cell/type: `AppleIntelligenceCell`
- Key: `"\(AIKeys.root).\(ownerOnlyKey)"`
- Method: `get`
- Message: Handler key or method is computed and cannot be proven by this source audit.

### WARN dynamic_key_needs_manual_review

- Location: `Sources/CellApple/Intelligence/AppleIntelligenceCell.swift:384`
- Cell/type: `AppleIntelligenceCell`
- Key: `"\(AIKeys.root).state"`
- Method: `get`
- Message: Handler key or method is computed and cannot be proven by this source audit.

### WARN dynamic_key_needs_manual_review

- Location: `Sources/CellApple/Intelligence/AppleIntelligenceCell.swift:389`
- Cell/type: `AppleIntelligenceCell`
- Key: `Self.dequeueOutboxKey`
- Method: `set`
- Message: Handler key or method is computed and cannot be proven by this source audit.

### WARN dynamic_key_needs_manual_review

- Location: `Sources/CellApple/Intelligence/AppleIntelligenceCell.swift:404`
- Cell/type: `AppleIntelligenceCell`
- Key: `"\(AIKeys.root).discover"`
- Method: `set`
- Message: Handler key or method is computed and cannot be proven by this source audit.

### WARN dynamic_key_needs_manual_review

- Location: `Sources/CellApple/Intelligence/AppleIntelligenceCell.swift:412`
- Cell/type: `AppleIntelligenceCell`
- Key: `"\(AIKeys.root).rank"`
- Method: `set`
- Message: Handler key or method is computed and cannot be proven by this source audit.

### WARN dynamic_key_needs_manual_review

- Location: `Sources/CellApple/Intelligence/AppleIntelligenceCell.swift:423`
- Cell/type: `AppleIntelligenceCell`
- Key: `"\(AIKeys.root).ensurePurpose"`
- Method: `set`
- Message: Handler key or method is computed and cannot be proven by this source audit.

### WARN dynamic_key_needs_manual_review

- Location: `Sources/CellApple/Intelligence/AppleIntelligenceCell.swift:432`
- Cell/type: `AppleIntelligenceCell`
- Key: `"\(AIKeys.root).buildCluster"`
- Method: `set`
- Message: Handler key or method is computed and cannot be proven by this source audit.

### WARN dynamic_key_needs_manual_review

- Location: `Sources/CellApple/Intelligence/AppleIntelligenceCell.swift:439`
- Cell/type: `AppleIntelligenceCell`
- Key: `"\(AIKeys.root).\(AIKeys.promptText)"`
- Method: `get`
- Message: Handler key or method is computed and cannot be proven by this source audit.

### WARN dynamic_key_needs_manual_review

- Location: `Sources/CellApple/Intelligence/AppleIntelligenceCell.swift:443`
- Cell/type: `AppleIntelligenceCell`
- Key: `"\(AIKeys.root).\(AIKeys.promptText)"`
- Method: `set`
- Message: Handler key or method is computed and cannot be proven by this source audit.

### WARN dynamic_key_needs_manual_review

- Location: `Sources/CellApple/Intelligence/AppleIntelligenceCell.swift:457`
- Cell/type: `AppleIntelligenceCell`
- Key: `"\(AIKeys.root).\(AIKeys.promptInstructions)"`
- Method: `get`
- Message: Handler key or method is computed and cannot be proven by this source audit.

### WARN dynamic_key_needs_manual_review

- Location: `Sources/CellApple/Intelligence/AppleIntelligenceCell.swift:461`
- Cell/type: `AppleIntelligenceCell`
- Key: `"\(AIKeys.root).\(AIKeys.promptInstructions)"`
- Method: `set`
- Message: Handler key or method is computed and cannot be proven by this source audit.

### WARN dynamic_key_needs_manual_review

- Location: `Sources/CellApple/Intelligence/AppleIntelligenceCell.swift:475`
- Cell/type: `AppleIntelligenceCell`
- Key: `"\(AIKeys.root).\(AIKeys.sendFlowOnIngest)"`
- Method: `get`
- Message: Handler key or method is computed and cannot be proven by this source audit.

### WARN dynamic_key_needs_manual_review

- Location: `Sources/CellApple/Intelligence/AppleIntelligenceCell.swift:479`
- Cell/type: `AppleIntelligenceCell`
- Key: `"\(AIKeys.root).\(AIKeys.sendFlowOnIngest)"`
- Method: `set`
- Message: Handler key or method is computed and cannot be proven by this source audit.

### WARN dynamic_key_needs_manual_review

- Location: `Sources/CellApple/Intelligence/AppleIntelligenceCell.swift:490`
- Cell/type: `AppleIntelligenceCell`
- Key: `"\(AIKeys.root).\(AIKeys.rankEnabled)"`
- Method: `get`
- Message: Handler key or method is computed and cannot be proven by this source audit.

### WARN dynamic_key_needs_manual_review

- Location: `Sources/CellApple/Intelligence/AppleIntelligenceCell.swift:495`
- Cell/type: `AppleIntelligenceCell`
- Key: `"\(AIKeys.root).\(AIKeys.rankEnabled)"`
- Method: `set`
- Message: Handler key or method is computed and cannot be proven by this source audit.

### WARN dynamic_key_needs_manual_review

- Location: `Sources/CellApple/Intelligence/AppleIntelligenceCell.swift:506`
- Cell/type: `AppleIntelligenceCell`
- Key: `"\(AIKeys.root).ingestConfigurations"`
- Method: `set`
- Message: Handler key or method is computed and cannot be proven by this source audit.

### WARN dynamic_key_needs_manual_review

- Location: `Sources/CellApple/Intelligence/AppleIntelligenceCell.swift:516`
- Cell/type: `AppleIntelligenceCell`
- Key: `"\(AIKeys.root).send"`
- Method: `set`
- Message: Handler key or method is computed and cannot be proven by this source audit.

### WARN dynamic_key_needs_manual_review

- Location: `Sources/CellApple/Intelligence/AppleIntelligenceCell.swift:568`
- Cell/type: `AppleIntelligenceCell`
- Key: `"\(AIKeys.root).sendPrompt"`
- Method: `set`
- Message: Handler key or method is computed and cannot be proven by this source audit.

### ERROR implicit_handler_contract

- Location: `Sources/CellApple/PurposeAndInterest/Cells/PerspectiveCell+Entities.swift:38`
- Cell/type: `PerspectiveCell`
- Key: `entities`
- Method: `get`
- Message: Handler is not preceded by a complete same-scope Explore contract for this exact key and method. Strict mode may reject it; permissive mode may publish unknown metadata.

### ERROR implicit_handler_contract

- Location: `Sources/CellApple/PurposeAndInterest/Cells/PerspectiveCell+Entities.swift:46`
- Cell/type: `PerspectiveCell`
- Key: `addEntity`
- Method: `set`
- Message: Handler is not preceded by a complete same-scope Explore contract for this exact key and method. Strict mode may reject it; permissive mode may publish unknown metadata.

### ERROR implicit_handler_contract

- Location: `Sources/CellApple/PurposeAndInterest/Cells/PerspectiveCell+Entities.swift:54`
- Cell/type: `PerspectiveCell`
- Key: `removeEntity`
- Method: `set`
- Message: Handler is not preceded by a complete same-scope Explore contract for this exact key and method. Strict mode may reject it; permissive mode may publish unknown metadata.

### ERROR implicit_handler_contract

- Location: `Sources/CellApple/PurposeAndInterest/Cells/PerspectiveCell+Entities.swift:63`
- Cell/type: `PerspectiveCell`
- Key: `projectEntities`
- Method: `set`
- Message: Handler is not preceded by a complete same-scope Explore contract for this exact key and method. Strict mode may reject it; permissive mode may publish unknown metadata.

### ERROR implicit_handler_contract

- Location: `Sources/CellApple/PurposeAndInterest/Cells/PerspectiveCell+Entities.swift:71`
- Cell/type: `PerspectiveCell`
- Key: `perspective.query.activeEntities`
- Method: `set`
- Message: Handler is not preceded by a complete same-scope Explore contract for this exact key and method. Strict mode may reject it; permissive mode may publish unknown metadata.

### WARN dynamic_key_needs_manual_review

- Location: `Sources/CellBase/Cells/Vault/VaultCell.swift:125`
- Cell/type: `VaultCell`
- Key: `operation`
- Method: `set`
- Message: Handler key or method is computed and cannot be proven by this source audit.

### ERROR implicit_handler_contract

- Location: `Sources/CellVapor/Cells/EntityAnchorCell.swift:194`
- Cell/type: `EntityAnchorCell`
- Key: `agreements`
- Method: `get`
- Message: Handler is not preceded by a complete same-scope Explore contract for this exact key and method. Strict mode may reject it; permissive mode may publish unknown metadata.
