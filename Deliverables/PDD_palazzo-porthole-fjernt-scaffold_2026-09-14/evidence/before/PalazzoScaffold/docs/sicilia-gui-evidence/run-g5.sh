#!/usr/bin/env bash
# Written for a later run with TCP/Chromium access. Do not source this file.
set -euo pipefail

EVIDENCE_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
LOCK_DIR="$EVIDENCE_DIR/.run-g5.lock"
if ! mkdir "$LOCK_DIR" 2>/dev/null; then
    printf '%s\n' 'G5 FAILED: forberedelse — en kjøring pågår eller .run-g5.lock må undersøkes' >> "$EVIDENCE_DIR/run-g5.log"
    exit 1
fi
exec > "$EVIDENCE_DIR/run-g5.log" 2>&1
umask 077

HAVEN_ROOT='/Users/kjetil/Build/Digipomps/HAVEN'
PALAZZO="$HAVEN_ROOT/PalazzoScaffold"
PORTHOLE="$HAVEN_ROOT/CellScaffold"
DELIVERABLE="$HAVEN_ROOT/CellProtocolDocuments/Deliverables/PDD_palazzo-sicilia-artikler_2026-09-07"
FIXTURE="$DELIVERABLE/content/artikler_v1.json"
VERIFY_DIR="$DELIVERABLE/images/verify"
RUN_ROOT=''
STEP='forberedelse'
FIRST_FAILURE=''
COMPLETED=0
PROCESS_GROUPS=()
LAST_PID=''

owned_group_snapshot() {
    python3 - "$$" "$RUN_ROOT" "${PROCESS_GROUPS[@]:-}" <<'PY'
import os
import subprocess
import sys

root_pid = int(sys.argv[1])
runtime = sys.argv[2]
owned = {int(value) for value in sys.argv[3:] if value}
rows = []
for line in subprocess.check_output(["ps", "-ax", "-o", "pid=,ppid=,pgid=,command="], text=True).splitlines():
    fields = line.strip().split(None, 3)
    if len(fields) == 4:
        rows.append((int(fields[0]), int(fields[1]), int(fields[2]), fields[3]))
our_group = os.getpgid(root_pid)
pids = {pid for pid, _, group, _ in rows if group in owned}
# Playwright launches Chromium detached. Its unique user-data directory also
# identifies that browser if its npm/node parent has already exited.
profiles = [runtime, os.path.realpath(runtime)] if runtime else []
for pid, _, _, command in rows:
    if any("--user-data-dir=" + path + "/tmp/" in command for path in profiles):
        pids.add(pid)
while True:
    children = {pid for pid, parent, _, _ in rows if parent in pids}
    if children <= pids:
        break
    pids.update(children)
groups = {group for pid, _, group, _ in rows if pid in pids}
for group in sorted(groups - owned - {our_group, 0, 1}):
    print(group)
PY
}

cleanup() {
    local result=$? group alive deadline additional_groups
    trap - EXIT INT TERM HUP
    set +e
    printf '\nOpprydding: stopper alle prosessgrupper startet av denne kjøringen.\n'
    if additional_groups="$(owned_group_snapshot)"; then
        for group in $additional_groups; do PROCESS_GROUPS+=("$group"); done
    else
        FIRST_FAILURE="${FIRST_FAILURE:-opprydding — kunne ikke kartlegge frakoblede barn}"
    fi
    for group in "${PROCESS_GROUPS[@]:-}"; do
        [[ -n "$group" ]] && kill -TERM -- "-$group" 2>/dev/null
    done
    deadline=$((SECONDS + 10))
    while (( SECONDS < deadline )); do
        alive=0
        for group in "${PROCESS_GROUPS[@]:-}"; do
            if [[ -n "$group" ]] && kill -0 -- "-$group" 2>/dev/null; then alive=1; fi
        done
        (( alive == 0 )) && break
        sleep 1
    done
    for group in "${PROCESS_GROUPS[@]:-}"; do
        if [[ -n "$group" ]]; then
            kill -KILL -- "-$group" 2>/dev/null
            wait "$group" 2>/dev/null
        fi
    done
    # Only the unique mktemp child belonging to this invocation is removed.
    if [[ -n "$RUN_ROOT" ]]; then
        case "$RUN_ROOT" in
            /tmp/sicilia-g5/run.*)
                if ! rm -rf -- "$RUN_ROOT"; then
                    FIRST_FAILURE="${FIRST_FAILURE:-opprydding av midlertidige filer}"
                fi ;;
            *) FIRST_FAILURE="${FIRST_FAILURE:-opprydding — uventet midlertidig sti}" ;;
        esac
    fi
    if ! rmdir "$LOCK_DIR"; then FIRST_FAILURE="${FIRST_FAILURE:-opprydding av kjørelås}"; fi
    set +m
    if (( result == 0 && COMPLETED == 1 )) && [[ -z "$FIRST_FAILURE" ]]; then
        printf '%s\n' 'G5 DONE'
        exit 0
    fi
    printf 'G5 FAILED: %s\n' "${FIRST_FAILURE:-$STEP}"
    exit 1
}
trap cleanup EXIT
trap 'STEP="avbrutt (SIGINT) under $STEP"; exit 130' INT
trap 'STEP="avbrutt (SIGTERM) under $STEP"; exit 143' TERM
trap 'STEP="avbrutt (SIGHUP) under $STEP"; exit 129' HUP

# Bash job control gives every background command its own process group.
# The EXIT snapshot additionally finds Playwright's detached Chromium groups.
set -m
start_in() {
    local directory=$1
    shift
    (cd "$directory" && exec "$@") <&0 &
    LAST_PID=$!
    PROCESS_GROUPS+=("$LAST_PID")
}
run_in() {
    start_in "$@"
    wait "$LAST_PID"
}
failed_preview() {
    printf 'FEIL: %s\n' "$1"
    FIRST_FAILURE="${FIRST_FAILURE:-$1}"
}
port_free() {
    ! lsof -nP -iTCP:"$1" -sTCP:LISTEN
}
wait_http() {
    local pid=$1 port=$2 deadline=$((SECONDS + 60))
    while (( SECONDS < deadline )); do
        if ! kill -0 "$pid" 2>/dev/null; then
            printf 'Serverprosessen %s avsluttet før port %s ble klar.\n' "$pid" "$port"
            return 1
        fi
        if curl --noproxy '*' --silent --show-error --fail --connect-timeout 1 --max-time 1 \
            --output /dev/null "http://127.0.0.1:$port/health"; then
            # Do not accidentally seed a different process that won a port race.
            if lsof -nP -a -p "$pid" -iTCP:"$port" -sTCP:LISTEN; then
                printf 'Klar: http://127.0.0.1:%s (PID %s).\n' "$port" "$pid"
                return 0
            fi
        fi
        (( SECONDS < deadline )) && sleep 1
    done
    printf 'Tidsavbrudd: port %s svarte ikke fra riktig prosess innen 60 sekunder.\n' "$port"
    return 1
}
ensure_build() {
    local project=$1
    # An incremental build also notices changes in resources and dependencies.
    run_in "$project" swift build --disable-sandbox --product Run
    [[ -x "$project/.build/debug/Run" ]]
}
start_palazzo() {
    local port=$1 vault=$2
    mkdir -p "$vault"
    start_in "$PALAZZO" env \
        CELL_VAULT_DOCUMENT_ROOT="$vault" \
        PALAZZO_GATEWAY_TOKEN="$PALAZZO_GATEWAY_TOKEN" \
        PALAZZO_BRIDGEHEAD_ENABLED=true \
        PALAZZO_BRIDGEHEAD_TOKEN="$PALAZZO_BRIDGEHEAD_TOKEN" \
        PALAZZO_HAVEN_HOST='' \
        .build/debug/Run serve --hostname 127.0.0.1 --port "$port"
}

printf 'G5 start: %s\n' "$(date -u '+%Y-%m-%dT%H:%M:%SZ')"
printf 'Kun lokal preview; ingen gjestereaksjoner eller runtime-commit.\n'
for tool in swift npm node python3 curl lsof mktemp ps; do command -v "$tool"; done
[[ -r "$FIXTURE" && -r "$PORTHOLE/package.json" ]]
for name in gjest-sicilia-liste gjest-sicilia-artikkel hus-artikkel-tagger; do
    [[ -r "$EVIDENCE_DIR/inputs/$name.skeleton.json" ]]
done
port_free 18083
port_free 18080
mkdir -p /tmp/sicilia-g5
RUN_ROOT="$(mktemp -d /tmp/sicilia-g5/run.XXXXXXXX)"
mkdir -p "$RUN_ROOT/tmp" "$RUN_ROOT/porthole" "$VERIFY_DIR"
export TMPDIR="$RUN_ROOT/tmp/"
export CELLPROTOCOL_LOCAL_PACKAGE_PATH="$HAVEN_ROOT/CellProtocol"
export PALAZZO_GATEWAY_TOKEN="$(python3 -c 'import secrets; print(secrets.token_hex(32))')"
export PALAZZO_BRIDGEHEAD_TOKEN="$(python3 -c 'import secrets; print(secrets.token_hex(32))')"
# Let skeleton:iterate create disposable local accounts, as its default does.
unset CONFERENCE_DEMO_USERNAME CONFERENCE_DEMO_PASSWORD CONFERENCE_DEMO_BASE_URL
printf 'Isolert runtime: %s\n' "$RUN_ROOT"

STEP='forutsetninger — npm og Playwright-Chromium'
run_in "$PORTHOLE" node - <<'JS'
const fs = require('node:fs');
const { chromium } = require('@playwright/test');
const executable = chromium.executablePath();
if (!fs.existsSync(executable)) throw new Error('Chromium mangler: npm run test:conference-smoke:install-browser');
console.log('Playwright-pakke og Chromium finnes. Browserstart kontrolleres først i preview.');
JS

# Preserve earlier evidence before any new previews. Never reuse stale PNGs.
ARCHIVE="$EVIDENCE_DIR/run-g5-archive/$(date -u '+%Y%m%dT%H%M%SZ')-$$"
mkdir -p "$ARCHIVE"
for name in gjest-sicilia-liste gjest-sicilia-artikkel hus-artikkel-tagger gjest-sicilia-tom; do
    if [[ -e "$EVIDENCE_DIR/porthole-$name" ]]; then
        mv "$EVIDENCE_DIR/porthole-$name" "$ARCHIVE/"
    fi
    for viewport in desktop mobile; do
        target="$VERIFY_DIR/porthole-$name-$viewport-v1.png"
        if [[ -e "$target" ]]; then mv "$target" "$ARCHIVE/"; fi
    done
done
printf 'Tidligere preview-artefakter arkiveres i %s\n' "$ARCHIVE"

cat > "$RUN_ROOT/palazzo_seed.py" <<'PY'
import json
import os
import sys
import urllib.error
import urllib.request

fixture_path, base, mode = sys.argv[1:]
with open(fixture_path, encoding="utf-8") as source:
    articles = json.load(source)["articles"]
assert len(articles) == 8 and len({a["id"] for a in articles}) == 8, "Forventet åtte unike artikler"
assert all(a["proposedTags"] and 0 < len(a["body"]) <= 900 for a in articles)
opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))

def request(path, payload=None, statuses=None):
    data = None if payload is None else json.dumps(payload, ensure_ascii=False).encode("utf-8")
    method = "GET" if data is None else "POST"
    print(f"{method} {base}{path}", flush=True)
    req = urllib.request.Request(base + path, data=data, headers={
        "Content-Type": "application/json",
        "X-Palazzo-Principal": "house",
        "Authorization": "Bearer " + os.environ["PALAZZO_GATEWAY_TOKEN"],
    }, method=method)
    try:
        with opener.open(req, timeout=30) as response:
            raw = response.read().decode("utf-8")
            code = response.status
    except urllib.error.HTTPError as error:
        print(error.read().decode("utf-8", errors="replace"), flush=True)
        raise
    print(f"HTTP {code}: {raw}", flush=True)
    assert code == 200, f"{path}: forventet HTTP 200, fikk {code}"
    value = json.loads(raw)["value"]
    if statuses is not None:
        assert value.get("status") in statuses, f"{path}: uventet status {value}"
    return value

def post(path, value, *statuses):
    return request(path, {"value": value}, statuses)

def reset_empty():
    # Same baseline reset as PalazzoSiciliaGUITests.seed; no guest operations.
    post("/api/content/discard", {}, "discarded", "no_draft")
    post("/api/content/draft", {"articles": [], "menuHighlights": []}, "draft_updated")
    post("/api/content/publish", {}, "published")
    assert request("/api/content")["articles"] == [], "Tom-instansen har publiserte artikler"

if mode in ("seed", "empty"):
    reset_empty()
if mode == "seed":
    post("/api/content/draft", {"articles": articles}, "draft_updated")
    for article in articles:
        post("/api/content/tags/approve", {"articleID": article["id"], "tags": article["proposedTags"]}, "approved")
    post("/api/content/publish", {}, "published")
    actual = request("/api/content")["articles"]
    assert len(actual) == 8 and {a["id"] for a in actual} == {a["id"] for a in articles}
    by_id = {a["id"]: a for a in actual}
    for article in articles:
        stored = by_id[article["id"]]
        for field in ("title", "body", "region", "origin"):
            assert stored[field] == article[field], f"Innholdsavvik: {article['id']} {field}"
        assert set(stored["tags"]) == set(article["proposedTags"]), f"Taggavvik: {article['id']}"
    print("Åtte artikler publisert med godkjente tagger; ingen gjestereaksjoner.")
elif mode == "house":
    before = request("/api/content")
    # Publishing clears proposals. Redraft the original, unapproved fixture;
    # its empty approved tags differ from the published, approved articles.
    post("/api/content/draft", {"articles": articles}, "draft_updated")
    pending = request("/api/content/tags/pending")
    rows = [r for r in pending if r.get("kind") == "article"]
    assert len(rows) == 8 and {r["articleID"] for r in rows} == {a["id"] for a in articles}, "Forventet åtte artikkelrader i husutkastet"
    assert request("/api/content") == before, "Husutkastet endret publisert innhold"
    print("Husutkast klart med åtte taggforslag; publisert gjesteflate uendret.")
elif mode != "empty":
    raise ValueError(f"Ukjent HTTP-modus: {mode}")
PY

cat > "$RUN_ROOT/collect.py" <<'PY'
import json
import pathlib
import shutil
import sys

evidence, verify, fixture, name = sys.argv[1:]
source = pathlib.Path(evidence) / ("porthole-" + name)
summary = json.loads((source / "run-summary.json").read_text())
assert summary["mode"] == "preview" and summary["baseURL"] == "http://127.0.0.1:18080"
assert {v["name"] for v in summary["viewports"]} == {"desktop", "mobile"}
assert all(v["pageErrorCount"] == 0 for v in summary["viewports"]), "JavaScript page errors"
articles = json.loads(pathlib.Path(fixture).read_text())["articles"]
normalized = lambda text: " ".join(text.split())
files = []
for viewport in ("desktop", "mobile"):
    folder = source / viewport
    dom = normalized((folder / f"{viewport}.dom.txt").read_text())
    if name == "gjest-sicilia-tom":
        assert "Fra Sicilia" not in dom, "Tomtilstanden viser Sicilia-seksjonen"
        assert not any(normalized(a["title"]) in dom for a in articles), "Tomtilstanden viser artikler"
    elif name == "gjest-sicilia-artikkel":
        article = next(a for a in articles if a["id"] == "art-pistasj-bronte")
        for text in (article["title"], article["body"], "Vil smake", "Interessant", "Ikke for meg"):
            assert normalized(text) in dom, f"Artikkelinnhold mangler: {text}"
    else:
        for article in articles:
            assert normalized(article["title"]) in dom, f"Artikkelrad mangler: {article['id']}"
        assert ("Fra Sicilia" if name == "gjest-sicilia-liste" else "Publiser") in dom
    png = folder / f"{viewport}.png"
    assert png.read_bytes().startswith(b"\x89PNG\r\n\x1a\n"), f"Ugyldig PNG: {png}"
    target = pathlib.Path(verify) / f"porthole-{name}-{viewport}-v1.png"
    files.append((png, target))
# Validate both viewports before copying either file.
for png, target in files:
    shutil.copy2(png, target)
    print(f"Skjermbilde: {target}")
PY

STEP='1 — bygg PalazzoScaffold'
ensure_build "$PALAZZO"
STEP='1 — start Palazzo på 18083'
start_palazzo 18083 "$RUN_ROOT/palazzo-published"
PALAZZO_PID=$LAST_PID
wait_http "$PALAZZO_PID" 18083

STEP='2 — seed, godkjenn tagger og publiser åtte artikler'
run_in "$PALAZZO" python3 "$RUN_ROOT/palazzo_seed.py" "$FIXTURE" http://127.0.0.1:18083 seed
STEP='2 — klargjør husutkast uten å endre publiserte artikler'
run_in "$PALAZZO" python3 "$RUN_ROOT/palazzo_seed.py" "$FIXTURE" http://127.0.0.1:18083 house

STEP='3 — bygg CellScaffold'
ensure_build "$PORTHOLE"
STEP='3 — start Porthole på 18080'
# README's Swift Run server hosts /porthole. package.json has no npm dev server.
start_in "$PORTHOLE" env \
    HAVEN_BRIDGEHEAD_TOKEN="$PALAZZO_BRIDGEHEAD_TOKEN" \
    HAVEN_BRIDGEHEAD_HOSTS='127.0.0.1:18083,127.0.0.1:18084' \
    CELL_SCAFFOLD_RUNTIME_ROOT="$RUN_ROOT/porthole" \
    CELL_VAULT_DOCUMENT_ROOT="$RUN_ROOT/porthole/CellsContainer" \
    SQLITE_DATABASE_PATH="$RUN_ROOT/porthole/db.sqlite" \
    CELL_SCAFFOLD_OWNER_CONTEXT=Scaffold \
    CELL_SCAFFOLD_OWNER_CREATE_IF_MISSING=true \
    CELL_SCAFFOLD_EAGER_BOOTSTRAP_PROVISION_ONLY=false \
    RP_ID=127.0.0.1 RP_ORIGIN=http://127.0.0.1:18080 \
    .build/debug/Run serve --env development --hostname 127.0.0.1 --port 18080
PORTHOLE_PID=$LAST_PID
wait_http "$PORTHOLE_PID" 18080

printf '%s\n' \
    'G7: PalazzoGuestShell og PalazzoContent er publisert over bridgehead; Porthole-serveren sender Bearer-token til de to lokale Palazzo-portene.' \
    'Tokenet gir transportadgang. Husflaten krever fortsatt husets eieridentitet.' \
    'Konfigurasjonsoppslag må også støttes av runtime. Feil beholdes som feil; se ../Rapport_Sicilia_G7_2026-09-08.md.'

preview() {
    local name=$1 status=0
    shift
    STEP="4 — preview $name"
    printf '\nPreview: %s\n' "$name"
    # These argv are the three original log commands, including both viewports.
    run_in "$PORTHOLE" "$@" || status=$?
    if (( status != 0 )); then
        failed_preview "$STEP (exit $status)"
        return 0  # Try the other required surfaces as well.
    fi
    STEP="5 — kontroller og kopier $name"
    run_in "$PORTHOLE" python3 "$RUN_ROOT/collect.py" "$EVIDENCE_DIR" "$VERIFY_DIR" "$FIXTURE" "$name" || status=$?
    if (( status != 0 )); then failed_preview "$STEP (exit $status)"; fi
}

preview gjest-sicilia-liste npm run skeleton:iterate -- --mode preview --base-url http://127.0.0.1:18080 --configuration-name 'Palazzo Gjest' --source-cell-endpoint cell://127.0.0.1:18083/PalazzoGuestShell --skeleton-file /Users/kjetil/Build/Digipomps/HAVEN/PalazzoScaffold/docs/sicilia-gui-evidence/inputs/gjest-sicilia-liste.skeleton.json --output-dir /Users/kjetil/Build/Digipomps/HAVEN/PalazzoScaffold/docs/sicilia-gui-evidence/porthole-gjest-sicilia-liste --viewports desktop,mobile
preview gjest-sicilia-artikkel npm run skeleton:iterate -- --mode preview --base-url http://127.0.0.1:18080 --configuration-name 'Palazzo artikkel' --source-cell-endpoint cell://127.0.0.1:18083/PalazzoGuestShell --skeleton-file /Users/kjetil/Build/Digipomps/HAVEN/PalazzoScaffold/docs/sicilia-gui-evidence/inputs/gjest-sicilia-artikkel.skeleton.json --output-dir /Users/kjetil/Build/Digipomps/HAVEN/PalazzoScaffold/docs/sicilia-gui-evidence/porthole-gjest-sicilia-artikkel --viewports desktop,mobile
preview hus-artikkel-tagger npm run skeleton:iterate -- --mode preview --base-url http://127.0.0.1:18080 --configuration-name 'Palazzo Hus — utkast' --source-cell-endpoint cell://127.0.0.1:18083/PalazzoContent --skeleton-file /Users/kjetil/Build/Digipomps/HAVEN/PalazzoScaffold/docs/sicilia-gui-evidence/inputs/hus-artikkel-tagger.skeleton.json --output-dir /Users/kjetil/Build/Digipomps/HAVEN/PalazzoScaffold/docs/sicilia-gui-evidence/porthole-hus-artikkel-tagger --viewports desktop,mobile

STEP='4 — valgfri tomtilstand på 18084'
empty_status=0
if [[ ! -r "$EVIDENCE_DIR/inputs/gjest-sicilia-tom.skeleton.json" ]] || ! port_free 18084; then
    printf '%s\n' 'Tomtilstand utelatt: tom-skeleton mangler eller port 18084 er opptatt.'
else
    start_palazzo 18084 "$RUN_ROOT/palazzo-empty"
    EMPTY_PID=$LAST_PID
    if wait_http "$EMPTY_PID" 18084; then
        run_in "$PALAZZO" python3 "$RUN_ROOT/palazzo_seed.py" "$FIXTURE" http://127.0.0.1:18084 empty || empty_status=$?
        if (( empty_status == 0 )); then
            run_in "$PORTHOLE" npm run skeleton:iterate -- --mode preview --base-url http://127.0.0.1:18080 --configuration-name 'Palazzo Gjest' --source-cell-endpoint cell://127.0.0.1:18084/PalazzoGuestShell --skeleton-file "$EVIDENCE_DIR/inputs/gjest-sicilia-tom.skeleton.json" --output-dir "$EVIDENCE_DIR/porthole-gjest-sicilia-tom" --viewports desktop,mobile || empty_status=$?
        fi
        if (( empty_status == 0 )); then
            run_in "$PORTHOLE" python3 "$RUN_ROOT/collect.py" "$EVIDENCE_DIR" "$VERIFY_DIR" "$FIXTURE" gjest-sicilia-tom || empty_status=$?
        fi
        if (( empty_status != 0 )); then
            printf 'Tomtilstand utelatt: seed, Porthole-preview eller artefaktkontroll feilet (exit %s); se utdata over.\n' "$empty_status"
        else
            printf '%s\n' 'Tomtilstand inkludert: verifisert tom publisert artikkelliste på separat Palazzo-instans.'
        fi
    else
        printf '%s\n' 'Tomtilstand utelatt: separat Palazzo-instans ble ikke klar innen 60 sekunder.'
    fi
fi

STEP='sluttkontroll'
[[ -z "$FIRST_FAILURE" ]] || exit 1
printf '%s\n' 'Tre pålagte previews og seks PNG-er kontrollert. Visuell paritetsakseptanse må vurderes fra artefaktene.'
COMPLETED=1
# cleanup writes the final log line, after stopping every child process.
