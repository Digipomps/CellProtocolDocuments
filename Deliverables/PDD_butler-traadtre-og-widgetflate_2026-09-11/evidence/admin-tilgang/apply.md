Legger til i **operator + security** i produksjon:

| | UUID |
| --- | --- |
| Kjetil | `87fa1cf0-6e67-451d-bcdd-7ce2bfa52c34` |
| Vegar | `836f624a-502c-4375-9bdd-5d44784c1f94` |

Foer: revisjon `77a922bc301a0ea7586a6b3677a87c2b1e0f73f7`, /health/ready svarte `200`.

```text
MVP_ADMIN_OBSERVER_USER_IDS=87fa1cf0-6e67-451d-bcdd-7ce2bfa52c34
MVP_ADMIN_OPERATOR_USER_IDS=87fa1cf0-6e67-451d-bcdd-7ce2bfa52c34
```

## Planen

`haven-admin-access production --plan …` → exit 0

```text
{
  "app_revision": "77a922bc301a0ea7586a6b3677a87c2b1e0f73f7",
  "container": "cellscaffold-production-app-1",
  "deploy_required": true,
  "environment": "production",
  "existing_set_env_file": "/etc/haven/deploy-production.secrets.env",
  "host_mutation": false,
  "plan_token": "3255ccab9bbaf9c4d44bbd99713f49f25613474d5cb136a79b64ea3e9a0a57ac",
  "preserves_existing_file_path": true,
  "roles": {
    "MVP_ADMIN_OPERATOR_USER_IDS": {
      "added": [
        "836f624a-502c-4375-9bdd-5d44784c1f94"
      ],
      "after": [
        "836f624a-502c-4375-9bdd-5d44784c1f94",
        "87fa1cf0-6e67-451d-bcdd-7ce2bfa52c34"
      ],
      "before": [
        "87fa1cf0-6e67-451d-bcdd-7ce2bfa52c34"
      ]
    },
    "MVP_ADMIN_SECURITY_USER_IDS": {
      "added": [
        "836f624a-502c-4375-9bdd-5d44784c1f94",
        "87fa1cf0-6e67-451d-bcdd-7ce2bfa52c34"
      ],
      "after": [
        "836f624a-502c-4375-9bdd-5d44784c1f94",
        "87fa1cf0-6e67-451d-bcdd-7ce2bfa52c34"
      ],
      "before": []
    }
  },
  "schema": "haven.admin-access.plan.v1",
  "users": [
    {
      "id": "836f624a-502c-4375-9bdd-5d44784c1f94",
      "username": "Vegar"
    },
```

Plan-token funnet (vises ikke her).

`haven-deploy-doctor production` → exit 0.

## Endringen

`haven-admin-access production --apply …` → exit 0

```text
{
  "app_revision": "77a922bc301a0ea7586a6b3677a87c2b1e0f73f7",
  "container": "cellscaffold-production-app-1",
  "deploy_required": true,
  "environment": "production",
  "existing_set_env_file": "/etc/haven/deploy-production.secrets.env",
  "host_mutation": true,
  "plan_token": "3255ccab9bbaf9c4d44bbd99713f49f25613474d5cb136a79b64ea3e9a0a57ac",
  "preserves_existing_file_path": true,
  "roles": {
    "MVP_ADMIN_OPERATOR_USER_IDS": {
      "added": [
        "836f624a-502c-4375-9bdd-5d44784c1f94"
      ],
      "after": [
        "836f624a-502c-4375-9bdd-5d44784c1f94",
        "87fa1cf0-6e67-451d-bcdd-7ce2bfa52c34"
      ],
      "before": [
        "87fa1cf0-6e67-451d-bcdd-7ce2bfa52c34"
      ]
    },
    "MVP_ADMIN_SECURITY_USER_IDS": {
      "added": [
        "836f624a-502c-4375-9bdd-5d44784c1f94",
        "87fa1cf0-6e67-451d-bcdd-7ce2bfa52c34"
      ],
      "after": [
        "836f624a-502c-4375-9bdd-5d44784c1f94",
        "87fa1cf0-6e67-451d-bcdd-7ce2bfa52c34"
```

## Env satt i kraft

`haven-deploy production current --env-only` → exit 0.

```text
2026-09-23T07:34:31Z PREFLIGHT miljoe=production commit=77a922bc301a0ea7586a6b3677a87c2b1e0f73f7 txn=20260923T073431Z-production-77a922bc
2026-09-23T07:34:33Z PREFLIGHT_GREEN prev=77a922bc301a0ea7586a6b3677a87c2b1e0f73f7 image=sha256:6999ea6203e77e9e1d91943bf9cb6c10bf241ae517a66a7ddce3b3c8b1cadefe
2026-09-23T07:34:40Z READY_OK (foerste-start) etter 10s
2026-09-23T07:34:46Z READY_OK (restart) etter 10s
2026-09-23T07:34:46Z COMMITTED_VERIFIED
2026-09-23T07:34:46Z FERDIG — bevis i /mnt/HC_Volume_104775511/haven-production-evidence/deploy/20260923T073431Z-production-77a922bc
```

## Etterpaa

```text
MVP_ADMIN_OBSERVER_USER_IDS=87fa1cf0-6e67-451d-bcdd-7ce2bfa52c34
MVP_ADMIN_OPERATOR_USER_IDS=836f624a-502c-4375-9bdd-5d44784c1f94,87fa1cf0-6e67-451d-bcdd-7ce2bfa52c34
MVP_ADMIN_SECURITY_USER_IDS=836f624a-502c-4375-9bdd-5d44784c1f94,87fa1cf0-6e67-451d-bcdd-7ce2bfa52c34
```

Revisjon: `77a922bc301a0ea7586a6b3677a87c2b1e0f73f7` (var `77a922bc301a0ea7586a6b3677a87c2b1e0f73f7`). /health/ready: `200` (var `200`).


Neste for full Arendalsuka-adgang: `ARENDALSUKA_REMOTE_CONFIGURATION_ACCESS` er tom i prod (staging har `public`), og publisher-tilgangen er et CellProtocol-bevis (`ArendalsukaConfigurationPublisherAccessCredential`), ikke en env-variabel. Begge deler er egne beslutninger — se ADMIN-TILGANG.md.
