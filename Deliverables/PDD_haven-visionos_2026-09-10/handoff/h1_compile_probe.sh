#!/bin/zsh
# H1-byggeprobe: bygger HAVEN-appen og CellProtocol for visionOS-simulator i en REN eksport av
# gjeldende HEAD i Binding og CellProtocol, og skriver feil per fil til TESTRESULT.md#h1.
#
# Tørrkjøring er standard. Bare `--go` bygger.
#   ./h1_compile_probe.sh          viser stegene og forhåndssjekkene, endrer ingenting (steg 0 i PLAN.md)
#   ./h1_compile_probe.sh --go     kjører (15–45 min; Mac-en må være våken)            (steg 1 i PLAN.md)
#   ./h1_compile_probe.sh --go --again   kjør på nytt samme dag (sletter dagens scratch først)
#
# Regler: ingen git-skriving (bare `rev-parse`, `branch --show-current`, `status`, `archive`), ingen
# endring i hovedtrærne, ingen docker. Én kjøring per dag med mindre --again er gitt.
# Bygges med `-project` (schemet HAVEN er delt i xcshareddata) så eksporten ikke avhenger av
# om Binding.xcworkspace er sporet i git. Simulatorbyggene får CODE_SIGNING_ALLOWED=NO:
# proben måler kompilering, ikke signering.
set -uo pipefail

MODE="${1:---dry-run}"
AGAIN="${2:-}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PDD_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
HAVEN_ROOT="$(cd "$SCRIPT_DIR/../../../.." && pwd)"
STAMP="$(date +%Y%m%d)"
SCRATCH="$HAVEN_ROOT/_h1-visionos-probe-$STAMP"
RESULT="$PDD_DIR/TESTRESULT.md"
LOG="$SCRATCH/probe.log"

say() { print -- "$@"; }
step() { say "== $1"; }

step "Forhåndssjekk"
say "HAVEN-rot:      $HAVEN_ROOT"
say "Oppgavemappe:   $PDD_DIR"
say "Scratch:        $SCRATCH"
for repo in Binding CellProtocol; do
  if [[ ! -d "$HAVEN_ROOT/$repo/.git" ]]; then
    say "STOPP: $HAVEN_ROOT/$repo er ikke et git-repo"; exit 2
  fi
  say "$repo: branch=$(git -C "$HAVEN_ROOT/$repo" branch --show-current) head=$(git -C "$HAVEN_ROOT/$repo" rev-parse --short HEAD) skitne=$(git -C "$HAVEN_ROOT/$repo" status --porcelain | wc -l | tr -d ' ')"
done
XCODE_VERSION="$(xcodebuild -version 2>/dev/null | head -1 || echo 'xcodebuild mangler')"
say "Xcode:          $XCODE_VERSION"
FREE_GB="$(df -g "$HAVEN_ROOT" 2>/dev/null | awk 'NR==2{print $4}')"
say "Ledig disk:     ${FREE_GB:-?} GB (proben anslås til 3–8 GB; under 30 GB ledig stopper den)"
if [[ -n "${FREE_GB:-}" && "$FREE_GB" -lt 30 ]]; then
  say "STOPP: for lite ledig disk til proben. Rydd først (feedback-diskbruk)."; exit 3
fi
XR_SDK="$(xcodebuild -showsdks 2>/dev/null | grep -i 'xrsimulator' | head -1 | awk '{print $NF}')"
if [[ -z "$XR_SDK" ]]; then
  say "BLOCKED: ingen visionOS-simulator-SDK i denne Xcode-installasjonen (xcodebuild -showsdks viser ingen xrsimulator)."
  say "         Kjetil: Xcode › Settings › Components › visionOS — installer, og kjør steg 0 på nytt."
  if [[ "$MODE" == "--go" ]]; then
    mkdir -p "$SCRATCH"
    {
      say ""
      say "## H1 — byggeprobe visionOS <a id=\"h1\"></a>"
      say ""
      say "- $(date -u +%Y-%m-%dT%H:%M:%SZ): **blocked** — ingen \`xrsimulator\`-SDK i $XCODE_VERSION. Installer visionOS-komponenten i Xcode (Settings › Components) og kjør på nytt."
    } >> "$RESULT"
  fi
  exit 0
fi
say "visionOS-SDK:   $XR_SDK   (SDK-en følger Xcode og holder til å KOMPILERE — steg 1)"
XR_RUNTIME="$(xcrun simctl list runtimes 2>/dev/null | grep -i 'visionOS' | head -1 | sed 's/^[[:space:]]*//')"
if [[ -z "$XR_RUNTIME" ]]; then
  say "Simulator-kjøretid: MANGLER — steg 1 (kompilering) går, men steg 2 (starte appen) trenger kjøretiden."
  say "         Kjetil: Xcode › Settings › Components › visionOS Simulator (~7–8 GB) — kan installeres mens steg 1 kjører."
else
  say "Simulator-kjøretid: $XR_RUNTIME   (trengs først i steg 2)"
fi
if [[ "$MODE" == "--go" && -f "$SCRATCH/probe.log" && "$AGAIN" != "--again" ]]; then
  say "STOPP: $SCRATCH/probe.log finnes allerede — én kjøring per dag. Bruk '--go --again' for å kjøre på nytt (sletter dagens scratch)."; exit 4
fi

step "Steg som kjøres med --go"
say "1. git archive HEAD for Binding og CellProtocol → $SCRATCH/{Binding,CellProtocol} (ren eksport, ingen ucommittede filer)"
say "   MERK: skitne filer over > 0 betyr at eksporten IKKE er det som står i hovedtreet. Er baseline rød, kan H1 ikke måles (PLAN.md §5)."
say "2. Baseline: xcodebuild HAVEN for macOS i eksporten (viser om HEAD i det hele tatt bygger rent — lesson.main-does-not-build-without-unlanded-changes)"
say "3. Patch i eksporten: SUPPORTED_PLATFORMS += xros xrsimulator; TARGETED_DEVICE_FAMILY = 1,2,7; XROS_DEPLOYMENT_TARGET = 26.0 (alle mål — det er en probe)"
say "4. xcodebuild CellApple (pakken) for 'generic/platform=visionOS Simulator'  (CODE_SIGNING_ALLOWED=NO)"
say "5. xcodebuild HAVEN for 'generic/platform=visionOS Simulator'              (CODE_SIGNING_ALLOWED=NO)"
say "6. Feil per fil (sortert) → $RESULT under ankeret #h1, pluss full logg i $LOG, og hvor mye disk scratch-mappen tok"
say "   Nett: SwiftPM klarer alle avhengigheter i fersk DerivedData (også de som ikke bygges) — Mac-en må ha nett."
if [[ "$MODE" != "--go" ]]; then
  say ""
  say "Tørrkjøring ferdig. Ingenting er endret. Kjør med --go for å bygge."
  exit 0
fi

step "1. Ren eksport"
rm -rf "$SCRATCH"; mkdir -p "$SCRATCH/Binding" "$SCRATCH/CellProtocol"
git -C "$HAVEN_ROOT/Binding" archive HEAD | tar -x -C "$SCRATCH/Binding"
git -C "$HAVEN_ROOT/CellProtocol" archive HEAD | tar -x -C "$SCRATCH/CellProtocol"
BINDING_SHA="$(git -C "$HAVEN_ROOT/Binding" rev-parse --short HEAD)"
CELLPROTOCOL_SHA="$(git -C "$HAVEN_ROOT/CellProtocol" rev-parse --short HEAD)"
: > "$LOG"

count_errors() {
  # skriver «antall  fil» sortert synkende for linjer på formen /sti/fil.swift:12:3: error: …
  grep -E ':[0-9]+:[0-9]+: error: ' "$1" | sed -E 's/:[0-9]+:[0-9]+: error: .*//' | sort | uniq -c | sort -rn
}

step "2. Baseline macOS"
BASE_LOG="$SCRATCH/baseline-macos.log"
( cd "$SCRATCH/Binding" && xcodebuild -project Binding.xcodeproj -scheme HAVEN -destination 'platform=macOS,arch=arm64' -derivedDataPath "$SCRATCH/DerivedData" build ) > "$BASE_LOG" 2>&1
BASE_STATUS=$?
say "baseline exit=$BASE_STATUS"

step "3. Patch prosjektfil i eksporten"
PBX="$SCRATCH/Binding/Binding.xcodeproj/project.pbxproj"
sed -i '' 's/SUPPORTED_PLATFORMS = "iphoneos iphonesimulator macosx";/SUPPORTED_PLATFORMS = "iphoneos iphonesimulator macosx xros xrsimulator";/' "$PBX"
sed -i '' 's/TARGETED_DEVICE_FAMILY = "1,2";/TARGETED_DEVICE_FAMILY = "1,2,7";/' "$PBX"
sed -i '' 's/^\([[:space:]]*\)MACOSX_DEPLOYMENT_TARGET = 26.1;/\1MACOSX_DEPLOYMENT_TARGET = 26.1;\
\1XROS_DEPLOYMENT_TARGET = 26.0;/' "$PBX"
grep -c "xrsimulator" "$PBX" | sed 's/^/xrsimulator-treff i pbxproj: /'
grep -c "XROS_DEPLOYMENT_TARGET" "$PBX" | sed 's/^/XROS_DEPLOYMENT_TARGET-treff i pbxproj: /'

step "4. CellApple for visionOS-simulator"
PKG_LOG="$SCRATCH/cellapple-xrsim.log"
( cd "$SCRATCH/CellProtocol" && xcodebuild -scheme CellApple -destination 'generic/platform=visionOS Simulator' -derivedDataPath "$SCRATCH/DerivedData" CODE_SIGNING_ALLOWED=NO CODE_SIGNING_REQUIRED=NO build ) > "$PKG_LOG" 2>&1
PKG_STATUS=$?
say "CellApple exit=$PKG_STATUS"

step "5. HAVEN for visionOS-simulator"
APP_LOG="$SCRATCH/haven-xrsim.log"
( cd "$SCRATCH/Binding" && xcodebuild -project Binding.xcodeproj -scheme HAVEN -destination 'generic/platform=visionOS Simulator' -derivedDataPath "$SCRATCH/DerivedData" CODE_SIGNING_ALLOWED=NO CODE_SIGNING_REQUIRED=NO build ) > "$APP_LOG" 2>&1
APP_STATUS=$?
say "HAVEN exit=$APP_STATUS"
SCRATCH_SIZE="$(du -sh "$SCRATCH" 2>/dev/null | awk '{print $1}')"
say "scratch-mappen tok $SCRATCH_SIZE — slettes med: rm -rf \"$SCRATCH\"  (etter at TESTRESULT.md#h1 er lest; Kjetils ja)"

step "6. Resultat"
{
  say ""
  say "## H1 — byggeprobe visionOS <a id=\"h1\"></a>"
  say ""
  say "Kjørt $(date -u +%Y-%m-%dT%H:%M:%SZ) med $XCODE_VERSION, SDK $XR_SDK, simulator-kjøretid: ${XR_RUNTIME:-mangler}. Ren eksport av Binding \`$BINDING_SHA\` og CellProtocol \`$CELLPROTOCOL_SHA\` i \`_h1-visionos-probe-$STAMP/\` (ikke hovedtrærne). Scratch: $SCRATCH_SIZE — slettes etter lesing (Kjetils ja)."
  say ""
  say "| Steg | Exit | Feil (unike linjer) |"
  say "|---|---|---|"
  say "| Baseline macOS | $BASE_STATUS | $(grep -cE ':[0-9]+:[0-9]+: error: ' "$BASE_LOG") |"
  say "| CellApple → xrsimulator | $PKG_STATUS | $(grep -cE ':[0-9]+:[0-9]+: error: ' "$PKG_LOG") |"
  say "| HAVEN → xrsimulator | $APP_STATUS | $(grep -cE ':[0-9]+:[0-9]+: error: ' "$APP_LOG") |"
  say ""
  if [[ $BASE_STATUS -ne 0 ]]; then
    say "**Baseline er rød** — H1 kan ikke måles før HEAD bygger rent for macOS. Feil per fil (baseline):"
    say ""; say '```'; count_errors "$BASE_LOG" | head -40; say '```'
  fi
  say "Feil per fil, CellApple → xrsimulator:"
  say ""; say '```'; count_errors "$PKG_LOG" | head -60; say '```'
  say ""
  say "Feil per fil, HAVEN → xrsimulator:"
  say ""; say '```'; count_errors "$APP_LOG" | head -80; say '```'
  say ""
  say "De ti første feilmeldingene (HAVEN):"
  say ""; say '```'; grep -E ':[0-9]+:[0-9]+: error: ' "$APP_LOG" | head -10; say '```'
  say ""
  say "Fulle logger: \`_h1-visionos-probe-$STAMP/baseline-macos.log\`, \`cellapple-xrsim.log\`, \`haven-xrsim.log\`."
} >> "$RESULT"
say "Skrevet til $RESULT (#h1)."
