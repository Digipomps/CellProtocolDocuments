#!/bin/zsh
# KJOR-SELV-visionos.command — HAVEN i visionOS-simulatoren, steg 0–3 i PLAN.md, i ett dobbeltklikk.
#
# Kjøres av Kjetil (dobbeltklikk i Finder) eller `zsh KJOR-SELV-visionos.command [--dry-run]` fra Terminal.
# Når: etter «G2 godkjent» (gitt 2026-09-16), med Macen våken og på nett. Tar 20–60 minutter første gang.
#
# Hva den gjør, i rekkefølge (alt logges til handoff/logs/KJOR-<tid>.log og TESTRESULT.md):
#   0  Forhåndssjekk: Xcode, ledig disk, xrsimulator-SDK, simulator-kjøretid, branch/HEAD/skitne filer.
#   1  Egne worktrees (søsken, fordi prosjektet refererer ../CellProtocol):
#        _worktrees/visionos-<dato>/Binding og _worktrees/visionos-<dato>/CellProtocol, gren losen/visionos-sim-<dato>.
#      Hovedtrærne røres ikke.
#   P  H1-måling: bare prosjektfilen patches (xros/xrsimulator) → bygg for visionOS-simulator → feil per fil.
#   A  Steg 2: de tre AppKit-i-#else + død haptikk-kode rettes → bygg → boot «Apple Vision Pro» → installer →
#      start → skjermbilde images/simulator-steg2-<dato>.png
#   B  Steg 3: baksiden av flaten (PortholeBackside.swift + view-modell + flipp) → bygg → start med
#      -HAVENShowBackside 1 → skjermbilde images/simulator-steg3-<dato>.png; deretter Mac-bygg og
#      images/mac-steg3-<dato>.png (skjermbilde av hele skjermen — slett det hvis noe privat kom med).
#   Ingen commit, ingen push, ingen sletting. Rydding (worktrees + DerivedData) skjer etter Kjetils ja.
#
# Feil i ett steg stopper de neste stegene som avhenger av det, men resultatet så langt skrives alltid.
set -uo pipefail
MODE="${1:---run}"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PDD_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
HAVEN_ROOT="$(cd "$SCRIPT_DIR/../../../.." && pwd)"
STAMP="$(date +%Y%m%d)"
RUNSTAMP="$(date +%Y%m%d-%H%M%S)"
WT="$HAVEN_ROOT/_worktrees/visionos-$STAMP"
BRANCH="losen/visionos-sim-$STAMP"
DD="$WT/DerivedData"
LOGDIR="$PDD_DIR/handoff/logs"
LOG="$LOGDIR/KJOR-$RUNSTAMP.log"
RESULT="$PDD_DIR/TESTRESULT.md"
IMAGES="$PDD_DIR/images"
PATCHER="$PDD_DIR/handoff/patches/apply_patches.py"
BUNDLE_ID="org.digipomps.haven"
XC_COMMON=(-derivedDataPath "$DD" ENABLE_USER_SCRIPT_SANDBOXING=NO)
XC_XRSIM=(-project Binding.xcodeproj -scheme HAVEN -destination 'generic/platform=visionOS Simulator' "${XC_COMMON[@]}" CODE_SIGNING_ALLOWED=NO CODE_SIGNING_REQUIRED=NO)
XC_MAC=(-project Binding.xcodeproj -scheme HAVEN -destination 'platform=macOS,arch=arm64' "${XC_COMMON[@]}")

mkdir -p "$LOGDIR" "$IMAGES"
exec > >(tee -a "$LOG") 2>&1

say() { print -- "$@"; }
step() { say ""; say "== $1  ($(date +%H:%M:%S))"; }
now_utc() { date -u +%Y-%m-%dT%H:%M:%SZ; }
count_errors() { grep -E ':[0-9]+:[0-9]+: error: ' "$1" | sed -E 's/:[0-9]+:[0-9]+: error: .*//' | sort | uniq -c | sort -rn; }
n_errors() { grep -cE ':[0-9]+:[0-9]+: error: ' "$1" 2>/dev/null || true; }
result_header() {
  if [[ ! -f "$RESULT" ]]; then
    { say "# TESTRESULT — haven visionos"; say ""; say "Ekte kjøringer, aldri tall fra en rapport. Skrevet av \`handoff/KJOR-SELV-visionos.command\`."; } > "$RESULT"
  fi
}
result() { result_header; print -l -- "$@" >> "$RESULT"; }

say "KJOR-SELV-visionos  $RUNSTAMP  modus=$MODE"
say "HAVEN-rot:     $HAVEN_ROOT"
say "Oppgavemappe:  $PDD_DIR"
say "Worktrees:     $WT  (gren $BRANCH)"
say "Logg:          $LOG"

# ---------------------------------------------------------------- 0 forhåndssjekk
step "0 Forhåndssjekk"
XCODE_VERSION="$(xcodebuild -version 2>/dev/null | head -1)"
[[ -n "$XCODE_VERSION" ]] || XCODE_VERSION="xcodebuild mangler"
say "Xcode:               $XCODE_VERSION"
FREE_GB="$(df -g "$HAVEN_ROOT" 2>/dev/null | awk 'NR==2{print $4}')"
say "Ledig disk:          ${FREE_GB:-?} GB (stopper under 30)"
if [[ -n "${FREE_GB:-}" && "$FREE_GB" -lt 30 ]]; then say "STOPP: for lite disk."; exit 3; fi
XR_SDK="$(xcodebuild -showsdks 2>/dev/null | grep -i 'xrsimulator' | head -1 | awk '{print $NF}')"
XR_RUNTIME="$(xcrun simctl list runtimes 2>/dev/null | grep -i 'visionOS' | head -1 | sed 's/^[[:space:]]*//')"
say "visionOS-SDK:        ${XR_SDK:-MANGLER}"
say "Simulator-kjøretid:  ${XR_RUNTIME:-MANGLER}"
for repo in Binding CellProtocol; do
  [[ -d "$HAVEN_ROOT/$repo/.git" ]] || { say "STOPP: $HAVEN_ROOT/$repo er ikke et git-repo"; exit 2; }
  say "$repo: branch=$(git -C "$HAVEN_ROOT/$repo" branch --show-current) head=$(git -C "$HAVEN_ROOT/$repo" rev-parse --short HEAD) skitne=$(git -C "$HAVEN_ROOT/$repo" status --porcelain | wc -l | tr -d ' ')"
done
[[ -f "$PATCHER" ]] || { say "STOPP: finner ikke $PATCHER"; exit 2; }
# Målt 16.09: `xcodebuild -showsdks` lister xrsimulator26.2 selv om visionOS-plattformen IKKE er installert
# («visionOS 26.2 is not installed. Please download and install the platform from Xcode > Settings > Components»).
# Kjøretiden er derfor testen. Uten den hoppes visionOS-fasene over, og bare Mac-delen kjøres.
VISIONOS_OK=1
if [[ -z "$XR_SDK" || -z "$XR_RUNTIME" ]]; then
  VISIONOS_OK=0
  say "BLOCKED for visionOS: plattformen/kjøretiden er ikke installert. Kjetil: Xcode › Settings › Components › visionOS 26.2 (plattform + simulator)."
  say "         Mac-delen (steg 3 på Mac) kjøres likevel. Kjør filen på nytt når visionOS er installert."
fi
if [[ "$MODE" == "--dry-run" ]]; then
  say ""; say "Tørrkjøring ferdig. Ingenting er endret. Dobbeltklikk filen, eller kjør uten --dry-run, for å bygge."
  exit 0
fi

# ---------------------------------------------------------------- 1 worktrees
step "1 Worktrees"
mkdir -p "$WT"
for repo in Binding CellProtocol; do
  if [[ -e "$WT/$repo/.git" ]]; then
    say "$repo: finnes allerede ($WT/$repo)"
    continue
  fi
  if git -C "$HAVEN_ROOT/$repo" show-ref --verify --quiet "refs/heads/$BRANCH"; then
    git -C "$HAVEN_ROOT/$repo" worktree add "$WT/$repo" "$BRANCH" || { say "STOPP: worktree add feilet for $repo"; exit 2; }
  else
    git -C "$HAVEN_ROOT/$repo" worktree add -b "$BRANCH" "$WT/$repo" HEAD || { say "STOPP: worktree add feilet for $repo"; exit 2; }
  fi
  say "$repo: laget $WT/$repo fra $(git -C "$HAVEN_ROOT/$repo" rev-parse --short HEAD)"
done
BINDING_SHA="$(git -C "$WT/Binding" rev-parse --short HEAD)"
CP_SHA="$(git -C "$WT/CellProtocol" rev-parse --short HEAD)"

# ---------------------------------------------------------------- 1b baseline-reparasjon
step "1b Baseline-reparasjon (se handoff/patches/baseline/README.md)"
BASELINE_DIR="$PDD_DIR/handoff/patches/baseline"
BASELINE_NOTE="ingen"
if [[ -d "$BASELINE_DIR/Binding" ]]; then
  BASELINE_NOTE=""
  ( cd "$BASELINE_DIR/Binding" && find . -type f -name '*.swift' ) | while read -r rel; do
    rel="${rel#./}"
    if ! cmp -s "$BASELINE_DIR/Binding/$rel" "$WT/Binding/Binding/$rel"; then
      cp "$BASELINE_DIR/Binding/$rel" "$WT/Binding/Binding/$rel" && say "kopierte $rel inn i worktreet (rød baseline: NavigationBar-case)"
    else
      say "$rel er allerede lik"
    fi
  done
  BASELINE_NOTE="tre filer i Binding/SkeletonEditor fra hovedtreets ucommittede NavigationBar-rettelse (handoff/patches/baseline/)"
fi

# ---------------------------------------------------------------- P H1-måling
step "P H1-måling (bare prosjektfilen patchet)"
python3 "$PATCHER" "$WT/Binding" "$WT/CellProtocol" --phase P || { say "STOPP: patch P feilet"; exit 2; }
P_LOG="$LOGDIR/build-P-xrsim-$RUNSTAMP.log"
if [[ $VISIONOS_OK -eq 1 ]]; then
( cd "$WT/Binding" && xcodebuild "${XC_XRSIM[@]}" build ) > "$P_LOG" 2>&1
P_STATUS=$?
else
  : > "$P_LOG"; P_STATUS="blocked"
fi
say "H1: exit=$P_STATUS feil=$(n_errors "$P_LOG")"
result "" "## H1 — byggeprobe visionOS <a id=\"h1\"></a>" "" \
  "Kjørt $(now_utc) med $XCODE_VERSION, SDK $XR_SDK, kjøretid: ${XR_RUNTIME:-mangler}. Worktrees \`_worktrees/visionos-$STAMP/\` fra Binding \`$BINDING_SHA\` og CellProtocol \`$CP_SHA\`. Bare prosjektfilen patchet (xros/xrsimulator, familie 7, XROS_DEPLOYMENT_TARGET 26.0, entitlements/manifest per SDK), ingen Swift-rettelser. Signering av." "" \
  "Baseline-reparasjon: $BASELINE_NOTE. visionOS-plattform installert: $( [[ $VISIONOS_OK -eq 1 ]] && echo ja || echo 'NEI — blocked, bare Mac-delen kjørt' )." "" \
  "| Steg | Exit | Feil (unike linjer) |" "|---|---|---|" "| HAVEN → xrsimulator, urettet | $P_STATUS | $(n_errors "$P_LOG") |" "" \
  "Feil per fil:" "" '```'
count_errors "$P_LOG" | head -60 >> "$RESULT"
result '```' "" "De ti første feilmeldingene:" "" '```'
grep -E ':[0-9]+:[0-9]+: error: ' "$P_LOG" | head -10 | sed "s#$WT/##" >> "$RESULT"
result '```' "" "Full logg: \`handoff/logs/$(basename "$P_LOG")\`."

# ---------------------------------------------------------------- simulator-hjelpere
sim_udid() {
  xcrun simctl list devices available -j 2>/dev/null | python3 -c '
import json, sys
devices = json.load(sys.stdin)["devices"]
for runtime, entries in devices.items():
    if "xrOS" in runtime or "visionOS" in runtime:
        for entry in entries:
            if entry.get("isAvailable", True):
                print(entry["udid"]); sys.exit(0)
'
}
ensure_sim() {
  UDID="$(sim_udid)"
  if [[ -z "$UDID" ]]; then
    RUNTIME_ID="$(xcrun simctl list runtimes -j | python3 -c '
import json, sys
for runtime in json.load(sys.stdin)["runtimes"]:
    if ("xrOS" in runtime.get("identifier", "") or "visionOS" in runtime.get("name", "")) and runtime.get("isAvailable", True):
        print(runtime["identifier"]); sys.exit(0)
')"
    if [[ -z "$RUNTIME_ID" ]]; then
      say "Ingen visionOS-kjøretid — kan bygge, men ikke starte. Kjetil: Xcode › Settings › Components › visionOS Simulator."
      return 1
    fi
    xcrun simctl create "HAVEN Vision" "com.apple.CoreSimulator.SimDeviceType.Apple-Vision-Pro" "$RUNTIME_ID" >/dev/null || return 1
    UDID="$(sim_udid)"
  fi
  [[ -n "$UDID" ]] || return 1
  xcrun simctl boot "$UDID" >/dev/null 2>&1 || true
  open -a Simulator --args -CurrentDeviceUDID "$UDID" >/dev/null 2>&1 || true
  xcrun simctl bootstatus "$UDID" -b >/dev/null 2>&1 || true
  say "Simulator: $UDID"
  return 0
}
xrsim_app() {
  ( cd "$WT/Binding" && xcodebuild "${XC_XRSIM[@]}" -showBuildSettings 2>/dev/null | awk -F' = ' '/ BUILT_PRODUCTS_DIR = /{print $2; exit}' )
}
run_in_sim() { # $1 = skjermbildefil, resten = launch-argumenter
  local shot="$1"; shift
  ensure_sim || return 1
  local app="$(xrsim_app)/HAVEN.app"
  [[ -d "$app" ]] || { say "Fant ikke $app"; return 1; }
  xcrun simctl terminate "$UDID" "$BUNDLE_ID" >/dev/null 2>&1 || true
  xcrun simctl install "$UDID" "$app" || { say "simctl install feilet"; return 1; }
  xcrun simctl launch "$UDID" "$BUNDLE_ID" "$@" || { say "simctl launch feilet"; return 1; }
  sleep 20
  xcrun simctl io "$UDID" screenshot "$shot" >/dev/null 2>&1 && say "Skjermbilde: $shot" || { say "screenshot feilet"; return 1; }
  return 0
}

# ---------------------------------------------------------------- A steg 2
step "A Steg 2 — plattformrettelser, bygg, start i simulator"
python3 "$PATCHER" "$WT/Binding" "$WT/CellProtocol" --phase A || { say "STOPP: patch A feilet"; exit 2; }
A_LOG="$LOGDIR/build-A-xrsim-$RUNSTAMP.log"
if [[ $VISIONOS_OK -eq 1 ]]; then
( cd "$WT/Binding" && xcodebuild "${XC_XRSIM[@]}" build ) > "$A_LOG" 2>&1
A_STATUS=$?
else
  : > "$A_LOG"; A_STATUS="blocked"
fi
say "Steg 2 bygg: exit=$A_STATUS feil=$(n_errors "$A_LOG")"
A_SHOT="$IMAGES/simulator-steg2-$STAMP.png"
A_RUN="ikke forsøkt"
if [[ "$A_STATUS" == "0" ]]; then
  if run_in_sim "$A_SHOT"; then A_RUN="startet, skjermbilde tatt"; else A_RUN="bygget, men start/skjermbilde feilet (se logg)"; fi
fi
result "" "## Steg 2 — HAVEN starter nativt i visionOS-simulatoren <a id=\"steg2\"></a>" "" \
  "Kjørt $(now_utc). Rettelser (fase A i \`handoff/patches/apply_patches.py\`): ContentView 1687–1700 og RootView 185–189 til canImport-form med nøytral #else; ubrukt UIImpactFeedbackGenerator fjernet fra ScannerService." "" \
  "| Steg | Exit | Feil (unike linjer) | Kjøring |" "|---|---|---|---|" "| HAVEN → xrsimulator, rettet | $A_STATUS | $(n_errors "$A_LOG") | $A_RUN |" "" \
  "Feil per fil (tom = grønt):" "" '```'
count_errors "$A_LOG" | head -60 >> "$RESULT"
result '```' "" "Skjermbilde: \`images/$(basename "$A_SHOT")\` ($( [[ -f "$A_SHOT" ]] && echo finnes || echo 'ikke tatt' )). Full logg: \`handoff/logs/$(basename "$A_LOG")\`."

# ---------------------------------------------------------------- B steg 3
step "B Steg 3 — baksiden av flaten"
python3 "$PATCHER" "$WT/Binding" "$WT/CellProtocol" --phase B || { say "STOPP: patch B feilet"; exit 2; }
B_LOG="$LOGDIR/build-B-xrsim-$RUNSTAMP.log"
if [[ $VISIONOS_OK -eq 1 ]]; then
( cd "$WT/Binding" && xcodebuild "${XC_XRSIM[@]}" build ) > "$B_LOG" 2>&1
B_STATUS=$?
else
  : > "$B_LOG"; B_STATUS="blocked"
fi
say "Steg 3 bygg (xrsimulator): exit=$B_STATUS feil=$(n_errors "$B_LOG")"
B_SHOT="$IMAGES/simulator-steg3-$STAMP.png"
B_RUN="ikke forsøkt"
if [[ "$B_STATUS" == "0" ]]; then
  if run_in_sim "$B_SHOT" -HAVENShowBackside 1; then B_RUN="startet med baksiden, skjermbilde tatt"; else B_RUN="bygget, men start/skjermbilde feilet"; fi
fi
M_LOG="$LOGDIR/build-B-macos-$RUNSTAMP.log"
( cd "$WT/Binding" && xcodebuild "${XC_MAC[@]}" build ) > "$M_LOG" 2>&1
M_STATUS=$?
say "Steg 3 bygg (macOS): exit=$M_STATUS feil=$(n_errors "$M_LOG")"
M_SHOT="$IMAGES/mac-steg3-$STAMP.png"
M_RUN="ikke forsøkt"
if [[ "$M_STATUS" == "0" ]]; then
  MAC_APP="$( cd "$WT/Binding" && xcodebuild "${XC_MAC[@]}" -showBuildSettings 2>/dev/null | awk -F' = ' '/ BUILT_PRODUCTS_DIR = /{print $2; exit}' )/HAVEN.app"
  if [[ -d "$MAC_APP" ]]; then
    # Bare instansen fra DETTE worktreet avsluttes før ny start — Kjetils vanlige HAVEN.app ligger et annet sted.
    pkill -f "$DD/Build/Products/Debug/HAVEN.app/Contents/MacOS/HAVEN" 2>/dev/null || true
    sleep 1
    open -n "$MAC_APP" --args -HAVENShowBackside 1 && sleep 15 && screencapture -x "$M_SHOT" && M_RUN="startet med baksiden, skjermbilde av hele skjermen tatt" || M_RUN="startet med baksiden; screencapture feilet (Terminal mangler Skjermopptak-tillatelse i Systeminnstillinger › Personvern) — se skjermbildet tatt via Losen"
  else
    M_RUN="fant ikke $MAC_APP"
  fi
fi
result "" "## Steg 3 — baksiden av flaten <a id=\"steg3\"></a>" "" \
  "Kjørt $(now_utc). Fase B: \`PortholeBackside.swift\` (ny, CellApple), puls + bakside-snapshot i \`PortholeBindingViewModel\`, flipp og menyvalg «Bakside» i ContentView. Startet med \`-HAVENShowBackside 1\` så baksiden vises uten klikk." "" \
  "| Bygg | Exit | Feil (unike linjer) | Kjøring |" "|---|---|---|---|" \
  "| HAVEN → xrsimulator | $B_STATUS | $(n_errors "$B_LOG") | $B_RUN |" \
  "| HAVEN → macOS | $M_STATUS | $(n_errors "$M_LOG") | $M_RUN |" "" \
  "Feil per fil, xrsimulator (tom = grønt):" "" '```'
count_errors "$B_LOG" | head -40 >> "$RESULT"
result '```' "" "Feil per fil, macOS (tom = grønt):" "" '```'
count_errors "$M_LOG" | head -40 >> "$RESULT"
result '```' "" "Skjermbilder: \`images/$(basename "$B_SHOT")\` ($( [[ -f "$B_SHOT" ]] && echo finnes || echo 'ikke tatt' )), \`images/$(basename "$M_SHOT")\` ($( [[ -f "$M_SHOT" ]] && echo finnes || echo 'ikke tatt' )). Logger: \`handoff/logs/$(basename "$B_LOG")\`, \`handoff/logs/$(basename "$M_LOG")\`."

# ---------------------------------------------------------------- oppsummering
step "Ferdig"
WT_SIZE="$(du -sh "$WT" 2>/dev/null | awk '{print $1}')"
say "Worktrees + DerivedData: $WT_SIZE i $WT"
say "Endringer ligger UCOMMITTET i worktree-grenen $BRANCH (Binding og CellProtocol). Ingen commit er gjort."
say "Rydding etter Kjetils ja:  rm -rf \"$DD\"  og  git -C \"$HAVEN_ROOT/Binding\" worktree remove \"$WT/Binding\"  (tilsvarende for CellProtocol)."
result "" "- $(now_utc): kjøring ferdig. Worktrees + DerivedData: $WT_SIZE. Endringer ucommittet på \`$BRANCH\`."
say ""
say "Resultat: $RESULT"
