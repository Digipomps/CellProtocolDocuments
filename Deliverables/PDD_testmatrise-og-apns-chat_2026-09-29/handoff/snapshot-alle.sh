#!/bin/bash
# T6 purpose://candidate.testmatrise.nothing-uncommitted-is-lost
# Tar vare på ucommittet arbeid i flere repoer som pushede wip-commits — UTEN å røre noen checkout:
# ingen checkout, ingen endring av HEAD, indeks eller arbeidstre (egen midlertidig indeks, commit-tree,
# push av en ref som ikke er utsjekket). Tørrkjøring er standard. Hemmeligheter og bygg-rot holdes ute.
#   ./snapshot-alle.sh            tørrkjøring: hva ville gått med / holdt ute
#   ./snapshot-alle.sh --go       lag wip-commit og push (én gren per repo)
set -uo pipefail
MODE="${1:-}"
BASE="${HAVEN_BASE:-$HOME/Build/Digipomps/HAVEN}"
[ -d "$BASE" ] || BASE="$HOME/mnt"
DATE="$(date +%Y-%m-%d)"
STAMP="$(date +%Y%m%d-%H%M%S)"
REPOS=(CellProtocol CellScaffold Binding CellProtocolDocuments)
MAXBYTES=$((5*1024*1024))
OUT="${OUT:-$PWD/snapshot-alle-$STAMP}"
mkdir -p "$OUT"
PY=""
for c in /usr/bin/python3 /opt/homebrew/bin/python3 /usr/local/bin/python3 python3; do
  if "$c" -c 'import sys; sys.exit(0 if sys.version_info[0]==3 else 1)' >/dev/null 2>&1; then PY="$c"; break; fi
done
[ -n "$PY" ] || { echo "FEIL: fant ingen fungerende python3 (på Macen var /usr/local/bin/python3 en x86-binær uten Rosetta). Stopper uten å skrive noe."; exit 1; }
echo "python: $PY"
TMPD="$(mktemp -d)"; trap 'rm -rf "$TMPD"' EXIT

# Mapper/mønstre som aldri går med (bygg-rot, andre tråders worktrees, hemmeligheter, støy).
EXCLUDE_RE='(^|/)(\.build|build|DerivedData|node_modules|\.swiftpm|_wt[^/]*|_to_delete|__pycache__|\.git|\.sprout|xcuserdata|\.havenbuild|_dry|snapshot-alle-[^/]*|workspaces|corpus-[^/]*|[^/]*-test-logs|[^/]*\.xcresult|[^/]*\.xcarchive)(/|$)|\.(p8|pem|key|p12|cer|mobileprovision|xcuserstate|profraw|profdata|o|a|dylib|xcarchive|ipa|dmg|zip|tar|gz|sqlite|db)$|(^|/)\.env(\.|$)|(^|/)default\.profraw$|(^|/)\.DS_Store$|(^|/)(id_rsa|id_ed25519)(\.pub)?$'
SECRET_RE='BEGIN (EC |RSA |OPENSSH |)PRIVATE KEY|APNS_PRIVATE_KEY(_P8|_BASE64)?=[A-Za-z0-9+/=-]{20,}|sk-[A-Za-z0-9]{32,}|ghp_[A-Za-z0-9]{30,}|AKIA[0-9A-Z]{16}'

summary="$OUT/summary.tsv"
printf "repo\tbranch\thead\tendret\tslettet\tuspora\tgar_med\tholdt_ute_monster\tholdt_ute_stor\tholdt_ute_hemmelig\n" > "$summary"

# Måling: ALDRI mot repoets egen indeks. `git diff-files` uten refresh viser stat-støy som «endret»
# når skrivemaskinen er en annen enn den som sist skrev indeksen (VM-en mot macOS ga 882 «endrede» filer
# der 0 var endret, 29.09). Vi måler mot en kopi av indeksen som refreshes ferskt — repoets indeks røres ikke.
refreshed_index() { # $1 = repo, $2 = målfil
  local gd; gd="$(git -C "$1" rev-parse --absolute-git-dir)"
  cp "$gd/index" "$2" && GIT_INDEX_FILE="$2" git -C "$1" update-index -q --refresh 2>/dev/null
  return 0
}
gitm() { local r="$1"; shift; GIT_INDEX_FILE="$REFIDX" git -C "$r" "$@"; }
fingerprint() { # HEAD + hva som er endret/uspora
  local r="$1" t; t="$(mktemp)"; refreshed_index "$r" "$t"
  { git -C "$r" rev-parse HEAD; GIT_INDEX_FILE="$t" git -C "$r" diff-files --name-status; GIT_INDEX_FILE="$t" git -C "$r" ls-files -o --exclude-standard; } | grep -Ev '/_dry/|snapshot-alle-' | shasum | cut -c1-16
  rm -f "$t"
}

for name in "${REPOS[@]}"; do
  R="$BASE/$name"
  [ -d "$R/.git" ] || [ -f "$R/.git" ] || { echo "hopper over $name (ikke funnet)"; continue; }
  echo "== $name =="
  BRANCH="$(git -C "$R" rev-parse --abbrev-ref HEAD)"
  HEAD="$(git -C "$R" rev-parse --short HEAD)"
  D="$OUT/$name"; mkdir -p "$D"
  REFIDX="$TMPD/$name.refidx"; refreshed_index "$R" "$REFIDX"
  gitm "$R" diff-files --name-only > "$D/endret.txt"
  gitm "$R" diff-files --diff-filter=D --name-only > "$D/slettet.txt"
  gitm "$R" ls-files -o --exclude-standard > "$D/uspora.txt"
  rm -f "$REFIDX"
  cat "$D/endret.txt" "$D/uspora.txt" | sort -u > "$D/kandidater.txt"

    "$PY" - "$R" "$D" "$MAXBYTES" "$EXCLUDE_RE" "$SECRET_RE" <<'PYEOF'
import os, re, sys
R, D, maxb, exc, sec = sys.argv[1], sys.argv[2], int(sys.argv[3]), re.compile(sys.argv[4]), re.compile(sys.argv[5].encode())
def lines(name):
    return open(os.path.join(D, name), encoding="utf-8", errors="replace").read().split("\n")
slettet = set(lines("slettet.txt")) - {""}
out = {k: open(os.path.join(D, k + ".txt"), "w", encoding="utf-8") for k in ("gar-med", "ute-monster", "ute-stor", "ute-hemmelig")}
for f in lines("kandidater.txt"):
    if not f:
        continue
    if exc.search(f):
        out["ute-monster"].write(f + "\n"); continue
    if f in slettet:
        out["gar-med"].write(f + "\n"); continue
    p = os.path.join(R, f)
    if not os.path.isfile(p):
        continue
    sz = os.path.getsize(p)
    if sz > maxb:
        out["ute-stor"].write("%s\t%d\n" % (f, sz)); continue
    if sz < 2000000:
        with open(p, "rb") as fh:
            data = fh.read()
        if b"\0" not in data[:8000] and sec.search(data):
            out["ute-hemmelig"].write(f + "\n"); continue
    out["gar-med"].write(f + "\n")
for fh in out.values():
    fh.close()
PYEOF

  n() { wc -l < "$1" | tr -d ' '; }
  printf "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" "$name" "$BRANCH" "$HEAD" "$(n "$D/endret.txt")" "$(n "$D/slettet.txt")" "$(n "$D/uspora.txt")" "$(n "$D/gar-med.txt")" "$(n "$D/ute-monster.txt")" "$(n "$D/ute-stor.txt")" "$(n "$D/ute-hemmelig.txt")" >> "$summary"
  echo "  gren $BRANCH @ $HEAD: endret $(n "$D/endret.txt"), uspora $(n "$D/uspora.txt") → går med $(n "$D/gar-med.txt"); ute: mønster $(n "$D/ute-monster.txt"), stor $(n "$D/ute-stor.txt"), hemmelig $(n "$D/ute-hemmelig.txt")"
  echo "  største mapper som går med:"; sed 's#/[^/]*$##' "$D/gar-med.txt" | awk -F/ '{print $1"/"$2}' | sort | uniq -c | sort -rn | head -6 | sed 's/^/    /'
  [ -s "$D/ute-hemmelig.txt" ] && { echo "  HEMMELIGHET-TREFF holdt ute (filnavn, ikke innhold):"; head -10 "$D/ute-hemmelig.txt" | sed 's/^/    /'; }
done

echo; column -t -s $'\t' "$summary" 2>/dev/null || cat "$summary"
echo "Detaljer per repo: $OUT/<repo>/{gar-med,ute-monster,ute-stor,ute-hemmelig}.txt"

if [ "$MODE" != "--go" ]; then
  echo; echo "Tørrkjøring ferdig — ingenting er skrevet i noe repo. Se over listene, kjør så med --go."
  exit 0
fi

echo; echo "== --go: wip-commit uten å røre checkouts =="
for name in "${REPOS[@]}"; do
  R="$BASE/$name"; D="$OUT/$name"
  [ -s "$D/gar-med.txt" ] || { echo "$name: ingenting å ta vare på"; continue; }
  BEFORE="$(fingerprint "$R")"
  WIP="wip/ucommittet-$DATE-$(git -C "$R" rev-parse --abbrev-ref HEAD | tr '/' '-')"
  git -C "$R" show-ref --verify -q "refs/heads/$WIP" && WIP="$WIP-$STAMP"
  IDX="$TMPD/$name.index"; rm -f "$IDX"
  export GIT_INDEX_FILE="$IDX"
  git -C "$R" read-tree HEAD || { echo "$name: read-tree feilet"; unset GIT_INDEX_FILE; continue; }
  git -C "$R" add -A --pathspec-from-file="$D/gar-med.txt" 2>"$D/add.err" || { echo "$name: add feilet (se $D/add.err)"; unset GIT_INDEX_FILE; continue; }
  TREE="$(git -C "$R" write-tree)"
  unset GIT_INDEX_FILE
  COMMIT="$(printf 'wip(%s): snapshot av ucommittet arbeid %s\n\nTatt vare på uten å røre checkouten (egen indeks, commit-tree). Ikke bygget/testet som en enhet.\nHoldt ute: bygg-rot, hemmeligheter, filer > 5 MB (se snapshot-alle-*/%s/ute-*.txt).\n\nCo-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_0166zoWBapoQ3R6iiJrhd2xx\n' "$name" "$DATE" "$name" | git -C "$R" commit-tree "$TREE" -p HEAD)"
  git -C "$R" update-ref "refs/heads/$WIP" "$COMMIT"
  git -C "$R" push -q origin "refs/heads/$WIP:refs/heads/$WIP" 2>&1 | tail -2
  REMOTE="$(git -C "$R" ls-remote --heads origin "$WIP" | cut -c1-7)"
  AFTER="$(fingerprint "$R")"
  echo "$name: $WIP  lokal $(git -C "$R" rev-parse --short "$COMMIT")  origin $REMOTE  uberørt: $([ "$BEFORE" = "$AFTER" ] && echo JA || echo 'NEI — AVVIK')"
  echo "  $(git -C "$R" diff --shortstat HEAD "$COMMIT")"
done
echo "== ferdig =="
