# Dataflyt — leveranse 1

```
Flate «Mitt lager» ──set──▶ ObjectStorageAdapter (per eier)
   │                          │ nøkkel(eier, alias) ◀── OwnerScopedCredentialStore (i prosessen, ikke en cellekant)
   │                          │ entry(serviceID)  ──get──▶ StorageServiceRegistry (per scaffold)
   │                          └─ HTTPS (SigV4) ─────────▶ lagringstjeneste (Hetzner …)
   └── stor fil: PUT til signert adresse ───────────────▶ lagringstjeneste
Flate «Lagringstjenester» ──get/set──▶ StorageServiceRegistry
Musikk / Publisering / Personlig side / Kunstnersalg ──putObject──▶ ObjectStorageAdapter   (planlagt i AP10; ingen kaller den i dag)
```

| Kant | Fra → til | Endepunkt / hendelse | Kontrakt |
|---|---|---|---|
| K1 | flate → ObjectStorageAdapter | `set putObject` (små filer, ca. 2,9 MB i web) | `contract/object_storage_adapter_v2.json#putObject` |
| K2 | flate → ObjectStorageAdapter | `set presignUpload`, `set confirmUpload` | `…#presignUpload`, `…#confirmUpload` |
| K3 | flate → ObjectStorageAdapter | `set presignRead`, `set getObject`, `set headObject`, `set deleteObject` | `…#presignRead` m.fl. |
| K4 | flate → ObjectStorageAdapter | `set selectService`, `set testConnection`, `get state`, `get usage` | `…#selectService` m.fl. |
| K5 | ObjectStorageAdapter → OwnerScopedCredentialStore | oppslag i prosessen på eierens identitet + alias; ingen cellekant, ingen grant | `…#credentialLookup` |
| K6 | ObjectStorageAdapter → StorageServiceRegistry | `set entry` (les én oppføring) | `contract/storage_service_registry_v1.json#entry` |
| K7 | ObjectStorageAdapter → tjeneste | HTTPS PUT/GET/HEAD/DELETE, SigV4 | `…#transport` |
| K8 | nettleser → tjeneste | HTTPS PUT/GET mot signert adresse | `…#presignUpload` |
| K9 | flate → StorageServiceRegistry | `get entries`, `set rank`, `set proposeEntry` | `contract/storage_service_registry_v1.json` |
| K10 | scaffold-eier → StorageServiceRegistry | `set approveEntry`, `set retireEntry` | `…#approveEntry` |
| K11 | ObjectStorageAdapter → flow | `object-storage.object.put.v1`, `…deleted.v1`, `…service.selected.v1` | `…#flow` |
