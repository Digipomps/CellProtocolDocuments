#!/usr/bin/env bash
# Provision one existing PRODUCTION web identity as a CellProtocol representative.
# Production counterpart of provision-scaffold-administrator-staging.sh. The
# application validates the identity binding and signs the authority; this
# wrapper owns quiescing, backup, restart verification, and rollback.
#
# Opened by Kjetil 2026-09-23 ("Ja, åpne for prod") after staging was provisioned
# and verified the same day. Differs from staging in exactly these ways:
#  - production container, environment and relying party, and the production
#    approval reference (G3:user-approved:2026-09-23);
#  - the backup covers EVERY writable directory bind of the container, not only
#    /app/CellsContainer. Production keeps its database (/app/Database) and its
#    identity vaults (/app/IdentityVaults) outside CellsContainer; a rollback that
#    restored only CellsContainer would leave the database and the vaults
#    half-provisioned (measured with docker inspect 2026-09-23T09:43Z);
#  - evidence goes to the existing production evidence root next to the data.
set -Eeuo pipefail
umask 077

usage() {
  cat <<'EOF'
Usage:
  provision-scaffold-administrator-production.sh <40-hex revision> <0600 request.json> [--preflight]

This command is production-only. It derives the port and data paths from the
running production container and never accepts a container or data path from
the caller.
EOF
}

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
  usage
  exit 0
fi

REVISION="${1:-}"
REQUEST_FILE="${2:-}"
MODE="${3:-run}"
DEPLOY_LOCK=/run/lock/haven/haven-deploy.lock
CONTAINER=cellscaffold-production-app-1

[[ "${REVISION}" =~ ^[0-9a-f]{40}$ ]] || { echo "status=refused reason=invalid_revision"; exit 2; }
[[ -n "${REQUEST_FILE}" ]] || { usage; exit 2; }
[[ "${MODE}" == "run" || "${MODE}" == "--preflight" ]] || { echo "status=refused reason=invalid_mode"; exit 2; }

for command_name in awk curl date df dirname docker du find flock grep id jq mktemp sed seq sha256sum sleep stat tar; do
  command -v "${command_name}" >/dev/null || { echo "status=refused reason=missing_${command_name}"; exit 2; }
done
[[ -f "${DEPLOY_LOCK}" && -r "${DEPLOY_LOCK}" ]] || { echo "status=refused reason=deploy_lock_unavailable"; exit 2; }
[[ -f "${REQUEST_FILE}" && ! -L "${REQUEST_FILE}" ]] || { echo "status=refused reason=request_not_regular"; exit 2; }
[[ "$(stat -c %u "${REQUEST_FILE}")" == "$(id -u)" ]] || { echo "status=refused reason=request_wrong_owner"; exit 2; }
[[ "$(stat -c %a "${REQUEST_FILE}")" == "600" ]] || { echo "status=refused reason=request_mode_not_0600"; exit 2; }
REQUEST_BYTES="$(stat -c %s "${REQUEST_FILE}")"
[[ "${REQUEST_BYTES}" -gt 0 && "${REQUEST_BYTES}" -le 32768 ]] || { echo "status=refused reason=request_size_invalid"; exit 2; }

# Open the root-owned deploy lock read-only. flock(2) still provides an
# exclusive advisory lock on local Linux filesystems without changing it.
exec 9<"${DEPLOY_LOCK}"
flock -n 9 || { echo "status=refused reason=deploy_in_progress"; exit 75; }

docker inspect "${CONTAINER}" >/dev/null 2>&1 || { echo "status=refused reason=container_missing"; exit 2; }
[[ "$(docker inspect "${CONTAINER}" --format '{{.State.Running}}')" == "true" ]] \
  || { echo "status=refused reason=container_not_running"; exit 2; }
container_env() {
  local key="$1"
  docker inspect "${CONTAINER}" | jq -r --arg key "${key}" \
    '.[0].Config.Env[] | select(startswith($key + "=")) | split("=")[1:] | join("=")'
}
[[ "$(container_env VAPOR_ENV)" == "production" ]] || { echo "status=refused reason=not_production_environment"; exit 2; }
[[ "$(container_env RP_ID)" == "haven.digipomps.org" ]] || { echo "status=refused reason=not_production_rp"; exit 2; }
[[ "$(container_env RP_ORIGIN)" == "https://haven.digipomps.org" ]] || { echo "status=refused reason=not_production_origin"; exit 2; }
CURRENT_REVISION="$(docker inspect "${CONTAINER}" | jq -r '.[0].Config.Env[] | select(startswith("APP_BUILD_REVISION=")) | split("=")[1]')"
[[ "${CURRENT_REVISION}" == "${REVISION}" ]] || { echo "status=refused reason=running_revision_mismatch"; exit 2; }
IMAGE_ID="$(docker inspect "${CONTAINER}" --format '{{.Image}}')"
[[ "${IMAGE_ID}" =~ ^sha256:[0-9a-f]{64}$ ]] || { echo "status=refused reason=image_not_immutable"; exit 2; }
IMAGE_REVISION="$(docker image inspect "${IMAGE_ID}" --format '{{index .Config.Labels "org.opencontainers.image.revision"}}')"
[[ "${IMAGE_REVISION}" == "${REVISION}" ]] || { echo "status=refused reason=image_revision_mismatch"; exit 2; }

MOUNT_COUNT="$(docker inspect "${CONTAINER}" | jq '[.[0].Mounts[] | select(.Destination == "/app/CellsContainer" and .Type == "bind" and .RW == true)] | length')"
[[ "${MOUNT_COUNT}" == "1" ]] || { echo "status=refused reason=cells_mount_not_unique_writable_bind"; exit 2; }
CELLS_SOURCE="$(docker inspect "${CONTAINER}" | jq -r '.[0].Mounts[] | select(.Destination == "/app/CellsContainer" and .Type == "bind" and .RW == true) | .Source')"
[[ "${CELLS_SOURCE}" == /* ]] || { echo "status=refused reason=cells_mount_source_invalid"; exit 2; }
HOST_PORT_COUNT="$(docker inspect "${CONTAINER}" | jq '[
  .[0].NetworkSettings.Ports
  | to_entries[]
  | .value[]?
  | select(.HostIp == "127.0.0.1" or .HostIp == "0.0.0.0")
] | length')"
[[ "${HOST_PORT_COUNT}" == "1" ]] || { echo "status=refused reason=health_port_not_unique"; exit 2; }
HOST_PORT="$(docker inspect "${CONTAINER}" | jq -r '
  .[0].NetworkSettings.Ports
  | to_entries[]
  | .value[]?
  | select(.HostIp == "127.0.0.1" or .HostIp == "0.0.0.0")
  | .HostPort
')"
[[ "${HOST_PORT}" =~ ^[0-9]{2,5}$ ]] || { echo "status=refused reason=health_port_invalid"; exit 2; }
HEALTH_URL="http://127.0.0.1:${HOST_PORT}"
EVIDENCE_PARENT="$(dirname "${CELLS_SOURCE}")-evidence"
[[ -d "${EVIDENCE_PARENT}" && ! -L "${EVIDENCE_PARENT}" ]] || { echo "status=refused reason=evidence_root_missing"; exit 2; }

# Every writable bind of the running container is state this operation may change
# (the one-shot inherits them all through --volumes-from). Back up and restore all
# of them. A writable bind that is not a plain directory is refused, not skipped.
mapfile -t RW_MOUNTS < <(docker inspect "${CONTAINER}" | jq -r '.[0].Mounts[] | select(.Type == "bind" and .RW == true) | "\(.Source)\t\(.Destination)"')
[[ "${#RW_MOUNTS[@]}" -ge 1 ]] || { echo "status=refused reason=no_writable_binds"; exit 2; }
BACKUP_MOUNT_ARGS_RO=()
BACKUP_MOUNT_ARGS_RW=()
MOUNT_MANIFEST=""
for index in "${!RW_MOUNTS[@]}"; do
  source_path="${RW_MOUNTS[$index]%%$'\t'*}"
  destination_path="${RW_MOUNTS[$index]#*$'\t'}"
  [[ "${source_path}" == /* && -d "${source_path}" && ! -L "${source_path}" ]] \
    || { echo "status=refused reason=writable_bind_not_directory destination=${destination_path}"; exit 2; }
  BACKUP_MOUNT_ARGS_RO+=(-v "${source_path}:/m${index}:ro")
  BACKUP_MOUNT_ARGS_RW+=(-v "${source_path}:/m${index}")
  MOUNT_MANIFEST+="${index} ${destination_path}"$'\n'
done
MOUNT_INDEXES="${!RW_MOUNTS[*]}"

READY_STATUS="$(curl -fsS --max-time 15 "${HEALTH_URL}/health/ready" | jq -r '.status')" \
  || { echo "status=refused reason=readiness_probe_failed"; exit 2; }
[[ "${READY_STATUS}" == "ready" ]] || { echo "status=refused reason=service_not_ready"; exit 2; }
SERVED_REVISION="$(curl -fsS --max-time 15 "${HEALTH_URL}/health/build" | jq -r '.app_revision')" \
  || { echo "status=refused reason=build_probe_failed"; exit 2; }
[[ "${SERVED_REVISION}" == "${REVISION}" ]] || { echo "status=refused reason=served_revision_mismatch"; exit 2; }

jq -e --arg revision "${REVISION}" '
  type == "object" and
  (keys | sort) == ([
    "administratorEntityRef", "approvalReference", "authorityActions",
    "expectedAppRevision", "representative", "requiredSignatures",
    "scaffoldRef", "schema", "targetEnvironment", "thresholdReason",
    "validityDays"
  ] | sort) and
  .schema == "haven.scaffold-administrator.provision.v1" and
  .targetEnvironment == "production" and
  .expectedAppRevision == $revision and
  .scaffoldRef == "scaffold:cellscaffold" and
  .administratorEntityRef == "entity:digipomps" and
  .requiredSignatures == 1 and
  .thresholdReason == "utviklingsfase, styreleder alene" and
  .authorityActions == ["mandate.issue", "mandate.revoke", "orgLink.issue", "orgLink.revoke"] and
  .validityDays == 90 and
  .approvalReference == "G3:user-approved:2026-09-23" and
  (.representative | type == "object") and
  (.representative | keys | sort) == (["expectedIdentityUUID", "fidoUserID"] | sort) and
  (.representative.fidoUserID | type == "string" and test("^[0-9A-Fa-f-]{36}$")) and
  (.representative.expectedIdentityUUID | type == "string" and test("^[0-9A-Fa-f-]{36}$"))
' "${REQUEST_FILE}" >/dev/null || { echo "status=refused reason=request_contract_invalid"; exit 2; }

# Verify that the exact deployed image has the tools required for backup and
# restore before touching the service.
docker run --rm --user 0:0 --network none --entrypoint /bin/sh "${IMAGE_ID}" -c \
  'command -v tar >/dev/null && command -v sha256sum >/dev/null && command -v find >/dev/null' \
  || { echo "status=refused reason=image_backup_tools_missing"; exit 2; }

CAPACITY="$(docker run --rm --user 0:0 --network none \
  "${BACKUP_MOUNT_ARGS_RO[@]}" -v "${EVIDENCE_PARENT}:/evidence:ro" \
  --entrypoint /bin/sh "${IMAGE_ID}" -c '
    set -eu
    size=0
    for index in $1; do
      part=$(du -sk "/m$index" | awk "{print \$1}")
      size=$((size + part))
    done
    free=$(df -Pk /evidence | awk "NR == 2 {print \$4}")
    printf "%s %s\n" "$size" "$free"
  ' sh "${MOUNT_INDEXES}")" || { echo "status=refused reason=capacity_probe_failed"; exit 2; }
read -r DATA_KIB FREE_KIB <<<"${CAPACITY}"
[[ "${DATA_KIB}" =~ ^[0-9]+$ && "${FREE_KIB}" =~ ^[0-9]+$ ]] \
  || { echo "status=refused reason=capacity_probe_invalid"; exit 2; }
REQUIRED_KIB=$((DATA_KIB * 2 + 1048576))
[[ "${FREE_KIB}" -ge "${REQUIRED_KIB}" ]] || { echo "status=refused reason=insufficient_backup_capacity"; exit 2; }

if [[ "${MODE}" == "--preflight" ]]; then
  printf 'status=preflight_ready revision=%s dataKiB=%s freeKiB=%s writableBinds=%s\n' "${REVISION}" "${DATA_KIB}" "${FREE_KIB}" "${#RW_MOUNTS[@]}"
  printf '%s' "${MOUNT_MANIFEST}" | sed 's/^/writableBind=/' 
  exit 0
fi

TXN="$(date -u +%Y%m%dT%H%M%SZ)-production-${REVISION:0:8}"
EVIDENCE_REL="scaffold-administrator/${TXN}"
TMP_DIR="$(mktemp -d /tmp/haven-scaffold-admin.XXXXXX)"
ENV_FILE="${TMP_DIR}/container.env"
PROCESS_OUTPUT="${TMP_DIR}/provision.log"
BACKUP_READY=0
MUTATION_ATTEMPTED=0
SERVICE_STOPPED=0
COMMITTED=0

wait_ready() {
  local attempt body
  for attempt in $(seq 1 72); do
    body="$(curl -sS --max-time 10 "${HEALTH_URL}/health/ready" 2>/dev/null || true)"
    case "${body}" in
      *'"status":"ready"'*|*'"status": "ready"'*) return 0 ;;
    esac
    [[ "$(docker inspect "${CONTAINER}" --format '{{.State.Running}}' 2>/dev/null || true)" == "true" ]] || return 1
    sleep 5
  done
  return 1
}

restore_backup() {
  # Verify every archive before deleting anything, then restore every writable bind.
  docker run --rm --user 0:0 --network none \
    "${BACKUP_MOUNT_ARGS_RW[@]}" -v "${EVIDENCE_PARENT}:/evidence:ro" \
    --entrypoint /bin/sh "${IMAGE_ID}" -c '
      set -eu
      rel=$1
      indexes=$2
      cd "/evidence/$rel"
      sha256sum -c backup.sha256 >/dev/null
      for index in $indexes; do
        find "/m$index" -mindepth 1 -delete
        tar -C "/m$index" -xpf "mount-$index.tar"
      done
    ' sh "${EVIDENCE_REL}" "${MOUNT_INDEXES}"
}

on_exit() {
  local status=$?
  trap - EXIT
  if [[ "${status}" -ne 0 && "${SERVICE_STOPPED}" -eq 1 && "${COMMITTED}" -eq 0 ]]; then
    docker stop -t 30 "${CONTAINER}" >/dev/null 2>&1 || true
    if [[ "${MUTATION_ATTEMPTED}" -eq 1 && "${BACKUP_READY}" -eq 1 ]]; then
      if ! restore_backup; then
        echo "status=rollback_failed reason=restore_failed"
        rm -rf "${TMP_DIR}"
        exit 70
      fi
    fi
    if docker start "${CONTAINER}" >/dev/null 2>&1 && wait_ready; then
      echo "status=rolled_back revision=${REVISION}"
    else
      echo "status=rollback_failed reason=service_not_ready"
      rm -rf "${TMP_DIR}"
      exit 70
    fi
  fi
  rm -rf "${TMP_DIR}"
  exit "${status}"
}
trap on_exit EXIT

# Preserve all inherited environment values without printing them, replacing
# only the three one-shot controls.
docker inspect "${CONTAINER}" | jq -r '
  .[0].Config.Env
  | map(select((split("=")[0]) as $key | [
      "CELL_SCAFFOLD_EAGER_BOOTSTRAP_MODE",
      "CELL_SCAFFOLD_EAGER_BOOTSTRAP_PROVISION_ONLY",
      "CELL_SCAFFOLD_ADMIN_PROVISION_ONLY"
    ] | index($key) | not))
  | .[]
' > "${ENV_FILE}"
printf '%s\n' \
  'CELL_SCAFFOLD_EAGER_BOOTSTRAP_MODE=provision-if-missing' \
  'CELL_SCAFFOLD_EAGER_BOOTSTRAP_PROVISION_ONLY=true' \
  'CELL_SCAFFOLD_ADMIN_PROVISION_ONLY=true' >> "${ENV_FILE}"
chmod 600 "${ENV_FILE}"

docker stop -t 60 "${CONTAINER}" >/dev/null
SERVICE_STOPPED=1
printf '%s' "${MOUNT_MANIFEST}" > "${TMP_DIR}/mounts.txt"
docker run --rm --user 0:0 --network none \
  "${BACKUP_MOUNT_ARGS_RO[@]}" -v "${EVIDENCE_PARENT}:/evidence" -v "${TMP_DIR}/mounts.txt:/run/mounts.txt:ro" \
  --entrypoint /bin/sh "${IMAGE_ID}" -c '
    set -eu
    rel=$1
    indexes=$2
    mkdir -p "/evidence/$rel"
    chmod 700 "/evidence/$rel"
    cp /run/mounts.txt "/evidence/$rel/mounts.txt"
    for index in $indexes; do
      tar -C "/m$index" -cpf "/evidence/$rel/mount-$index.tar" .
    done
    cd "/evidence/$rel"
    sha256sum mount-*.tar mounts.txt > backup.sha256
    chmod 400 mount-*.tar mounts.txt backup.sha256
    sha256sum -c backup.sha256 >/dev/null
  ' sh "${EVIDENCE_REL}" "${MOUNT_INDEXES}"
BACKUP_READY=1

MUTATION_ATTEMPTED=1
docker run --rm -i --network none --volumes-from "${CONTAINER}" \
  --env-file "${ENV_FILE}" "${IMAGE_ID}" \
  < "${REQUEST_FILE}" > "${PROCESS_OUTPUT}" 2>&1

RECEIPT_COUNT="$(grep -c '^scaffold_administrator_provisioning_receipt=' "${PROCESS_OUTPUT}" || true)"
[[ "${RECEIPT_COUNT}" == "1" ]] || { echo "status=failed reason=receipt_missing_or_ambiguous"; exit 1; }
RECEIPT="$(sed -n 's/^scaffold_administrator_provisioning_receipt=//p' "${PROCESS_OUTPUT}")"
jq -e --arg revision "${REVISION}" '
  .schema == "haven.scaffold-administrator.provision-receipt.v1" and
  (.status == "provisioned" or .status == "already_provisioned") and
  .environment == "production" and .appRevision == $revision and
  .scaffoldRef == "scaffold:cellscaffold" and
  .administratorEntityRef == "entity:digipomps" and
  .requiredSignatures == 1 and
  .authorityActions == ["mandate.issue", "mandate.revoke", "orgLink.issue", "orgLink.revoke"] and
  (.representativeBindingSHA256 | test("^sha256:[0-9a-f]{64}$")) and
  .approvalReference == "G3:user-approved:2026-09-23"
' <<<"${RECEIPT}" >/dev/null || { echo "status=failed reason=receipt_contract_invalid"; exit 1; }

docker start "${CONTAINER}" >/dev/null
wait_ready || { echo "status=failed reason=first_start_not_ready"; exit 1; }
SERVED_REVISION="$(curl -fsS --max-time 15 "${HEALTH_URL}/health/build" | jq -r '.app_revision')"
[[ "${SERVED_REVISION}" == "${REVISION}" ]] || { echo "status=failed reason=served_revision_mismatch"; exit 1; }
docker restart -t 60 "${CONTAINER}" >/dev/null
wait_ready || { echo "status=failed reason=restart_not_ready"; exit 1; }
SERVED_REVISION="$(curl -fsS --max-time 15 "${HEALTH_URL}/health/build" | jq -r '.app_revision')"
[[ "${SERVED_REVISION}" == "${REVISION}" ]] || { echo "status=failed reason=restart_revision_mismatch"; exit 1; }

OPERATOR_RECEIPT="$(jq -cn \
  --arg completedAt "$(date -u +%FT%TZ)" \
  --arg revision "${REVISION}" \
  --arg transactionID "${TXN}" \
  --argjson provisioning "${RECEIPT}" \
  --argjson writableBinds "${#RW_MOUNTS[@]}" \
  '{schema:"haven.scaffold-administrator.production-operation.v1",status:"committed_verified",environment:"production",writableBindsBackedUp:$writableBinds,appRevision:$revision,transactionID:$transactionID,networkDuringProvisioning:"none",backupDisposition:"cleanup_pending_after_verified_restart",completedAt:$completedAt,provisioning:$provisioning}')"
printf '%s\n' "${OPERATOR_RECEIPT}" | docker run --rm -i --user 0:0 --network none \
  -v "${EVIDENCE_PARENT}:/evidence" --entrypoint /bin/sh "${IMAGE_ID}" -c '
    set -eu
    rel=$1
    cat > "/evidence/$rel/receipt.json"
    chmod 400 "/evidence/$rel/receipt.json"
  ' sh "${EVIDENCE_REL}"
# The durable receipt commits the verified operation. Cleanup failures must not
# stop the healthy service or attempt rollback from already removed material.
COMMITTED=1
docker run --rm --user 0:0 --network none \
  -v "${EVIDENCE_PARENT}:/evidence" --entrypoint /bin/sh "${IMAGE_ID}" -c '
    set -eu
    rel=$1
    rm -f "/evidence/$rel"/mount-*.tar "/evidence/$rel/backup.sha256"
  ' sh "${EVIDENCE_REL}"
OPERATOR_RECEIPT="$(jq -c '.backupDisposition = "deleted_after_verified_restart"' <<<"${OPERATOR_RECEIPT}")"
printf '%s\n' "${OPERATOR_RECEIPT}" | docker run --rm -i --user 0:0 --network none \
  -v "${EVIDENCE_PARENT}:/evidence" --entrypoint /bin/sh "${IMAGE_ID}" -c '
    set -eu
    rel=$1
    chmod 600 "/evidence/$rel/receipt.json"
    cat > "/evidence/$rel/receipt.json"
    chmod 400 "/evidence/$rel/receipt.json"
  ' sh "${EVIDENCE_REL}"
printf 'scaffold_administrator_production_receipt=%s\n' "${OPERATOR_RECEIPT}"
