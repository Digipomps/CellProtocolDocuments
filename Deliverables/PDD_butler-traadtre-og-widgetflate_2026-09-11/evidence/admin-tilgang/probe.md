## Wrapperen ops har NOPASSWD paa

### haven-admin-access uten argumenter

`sudo -n haven-admin-access 2>&1 | head -40` → exit 0

```text
usage: haven-admin-access [-h] (--plan | --apply PLAN_TOKEN)
                          {staging,production} first_uuid second_uuid
haven-admin-access: error: the following arguments are required: environment, first_uuid, second_uuid
```

### Hva wrapperen er

`file /usr/local/sbin/haven-admin-access; sudo -n head -60 /usr/local/sbin/haven-admin-access 2>/dev/null || echo '(kan ikke lese filen som ops)'` → exit 0

```text
bash: line 1: file: command not found
(kan ikke lese filen som ops)
```

## Hvem er admin akkurat naa

### staging (cellscaffold-app-1)

```text
MVP_ADMIN_OBSERVER_USER_IDS=C046B080-845A-47DE-A70C-8D4594E17DC9,347839EA-6F5C-40C4-B13E-6C1F382CD096
MVP_ADMIN_OPERATOR_USER_IDS=347839ea-6f5c-40c4-b13e-6c1f382cd096,c046b080-845a-47de-a70c-8d4594e17dc9,c2a12943-7cd8-4a02-b325-a2ea17b4769f,c8c99783-8522-40de-a427-03e409090587
MVP_ADMIN_SECURITY_USER_IDS=347839ea-6f5c-40c4-b13e-6c1f382cd096,c046b080-845a-47de-a70c-8d4594e17dc9,c2a12943-7cd8-4a02-b325-a2ea17b4769f,c8c99783-8522-40de-a427-03e409090587
ARENDALSUKA_REMOTE_CONFIGURATION_ACCESS=public
```

### production (cellscaffold-production-app-1)

```text
MVP_ADMIN_OBSERVER_USER_IDS=87fa1cf0-6e67-451d-bcdd-7ce2bfa52c34
MVP_ADMIN_OPERATOR_USER_IDS=87fa1cf0-6e67-451d-bcdd-7ce2bfa52c34
MVP_ADMIN_SECURITY_USER_IDS=ARENDALSUKA_REMOTE_CONFIGURATION_ACCESS=```

## Brukerne bak UUID-ene

```text
  beb6ecf4-b391-4f05-8291-79fc10250635   arendalsuka-participant-807e5000-20260902t0525
  66639939-ab4a-45d1-94ce-0677967c8bcc   arendalsuka-participant-canary-20260901T193957274Z
  dda6f843-217b-4380-80f1-824bdf91812f   arendalsuka-participant-canary-20260901T202922394Z
  70b916c9-1fa8-4b7a-9df1-861b42f12849   arendalsuka-participant-canary-20260901T203718038Z
  93c7eb9f-4996-4f44-984a-6bc2b7b2eec3   arendalsuka-swarm-20260908-33c9c624-1
  2ccefd68-1ad9-4f25-9594-cd75b4e54024   arendalsuka-swarm-20260908-33c9c624-2
  bcf7d11f-30c7-4cac-b44c-d8c0972248b1   butler-807e5000-20260902
  d266007a-4efa-45b0-8715-230eefc396c3   butler-explicit-helper-2995-desktop
  f399c7e8-7058-4d04-95a0-feaa99c632da   butler-explicit-helper-2995-mobile-375
  efdf95dd-174f-46d8-ab3c-8722782c7228   butler-explicit-helper-50884-desktop
  de9fc5d1-34a5-4c97-a164-e52bd11ad305   butler-explicit-helper-57366-desktop
  b64704b6-8377-4f62-82d2-cedc45045460   butler-explicit-helper-59182-desktop
  2a96a934-b720-418c-bbfc-51996b41ffa4   butler-explicit-helper-59182-mobile-375
  209efcf9-d7dc-4e6f-814c-86c63068d30f   butler-explicit-helper-73348-desktop
  8f8fddda-ee7b-43c3-9110-9d0666f593df   butler-explicit-helper-73348-mobile-375
  6ee25971-aa21-4d67-ac38-b19d549f51f0   butler-release-6ae-1788337381355-desktop
  6a7bf720-3be5-4b4a-9030-4e35fb2972fc   butler-release-inspect-1788337434587
  0ae879f7-109e-415d-a18f-21404da8cf0b   butler-release-pass-6ae-1788337497157-desktop
  062fb19e-b307-41fe-9761-c402a843e95e   butler-release-pass-6ae-1788337507537-mobile-375
  301ca758-4b8f-4bae-98e6-82e229720fdd   conference-smoke-web-ladder-atlas
  63cf9c70-c85e-4bf6-a35f-fbdc793adf41   conference-smoke-web-ladder-baseline
  ac86aea5-ca38-42e6-8db7-1552b3de288e   conference-smoke-web-ladder-transcript
  c9aa1354-09ed-4e95-aa29-c186293f1913   conference-smoke-web-lookup-hit
  ff488011-5009-40d7-964f-86c285b7db9c   conference-smoke-web-lookup-miss
  8c1c605d-ad46-45bb-88e3-092278d2f32b   document-live-1789076756479
  9c22b2c0-3ab8-47b1-a7b6-6af98c868649   document-live-1789076981457
  e2495ec6-ecef-4865-b622-ac94a00d783b   document-live-1789076981457-outsider
  c8c99783-8522-40de-a427-03e409090587   kjetil2
  efc13929-b721-4ce9-a0a2-242bb6de6b9a   parity-f365c8de
  41024ed3-0ccb-4a8f-8a5e-da25334462b4   probe-does-not-exist
  c2a12943-7cd8-4a02-b325-a2ea17b4769f   vegar
  bf5f87e9-4b0f-4078-89c4-0c41e7fa4fa9   vegar-cellconfiguration-upload-8010
```

## Arendalsuka-utstederen (forberedt 2026-09-16, aldri kjoert)

Skriptene `_handoff/ADMIN/ROOT-gi-admin.sh`, `_handoff/ADMIN/ROOT-vis-admin.sh` og
`_handoff/ARENDALSUKA/ROOT-arendalsuka-utsteder.sh` krever alle root paa verten.
`ops` har `(ALL : ALL) ALL` i sudoers, men den linjen krever passord — og verten tar
ikke passord. Derfor er spoersmaalet over: hva kan `haven-admin-access` gjoere uten det.
