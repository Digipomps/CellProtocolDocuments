# Binding startup secret release blocker

Observed in integrated main and original WIP: BindingStartupIdentityVault.scopedSecretData derives bytes from the public tag and counter with SHA256. Different installations therefore share the same encryption material. No real user Keychain items or encrypted user files have been read, changed or rotated during this task.

Required fix before distributing this native candidate:

- Durable random per-vault root secret in Keychain, insert-if-absent (never update an existing root during startup). Ephemeral roots remain in memory. HMAC derivation must preserve prefixes across requested lengths and isolate tags/vaults. Read/corruption/write failures fail closed.
- Existing storage cannot simply switch keys. CellResolver configures the storage master as SHA256(scopedSeed), so the legacy master is SHA256(SHA256(tag + big-endian zero counter)).
- Existing CELLENC1 envelope uses version1, ownerIdentityUUID, ChaChaPoly combined; key is SHA256(master + ownerOrUnderscore + dot + binding); AAD is cell-persistence-v1 + NUL + owner + NUL + binding. Typed-cell binding is cell UUID. EntityAnchor side-file binding is entity-anchor-side-file-v1:<UTF8 UUID length>:<UUID>:<filename>.
- Known files: CellsContainer/<UUID>/typedCell.json, keypathstorage.json, entity-authority-journal.json. Confirm current source before migration. FileIO and CellStoragePathPolicy reject symbolic/hard links and excessive lengths.
- Application-owned migration must preflight all affected files before changing originals, retain protected rollback copies, verify exact plaintext parity, atomically replace files only after verifying no concurrent change, resume mixed old/new generations after interruption, and keep the random secret durable before changing any file. Unknown/corrupt ciphertext must stop migration without overwriting source.
- No CellProtocol shared semantic change or source/image bump required for the web release. All migration verification uses synthetic data; real native installation remains pending.

Tests required: distinct vaults/tags, stable relaunch and lengths, corrupt/inaccessible key no overwrite, actual CellPersistenceCrypto/EntityAnchorPersistence parity, interrupted migration resume, corrupt file preflight no partial source changes, symlink/hardlink rejection, and preserved recoverable originals.
