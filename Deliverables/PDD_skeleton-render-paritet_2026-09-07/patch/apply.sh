#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright (c) 2026 Stiftelsen Digipomps and HAVEN contributors
#
# Legger SkeletonStyleParity-CSS-fiksen paa ferske worktrees fra origin/main i
# begge repoer, bygger og kjoerer testene.
#
# Eier: kjetil. En kommando.
#
#   bash apply.sh              tørrkjøring, endrer ingenting
#   bash apply.sh --apply      lager worktrees, kopierer filer, bygger, tester
#
# Idempotent: kjoerer du den to ganger med --apply gjenbrukes worktreene.

set -euo pipefail

PATCH_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HAVEN_ROOT="${HAVEN_ROOT:-$HOME/Build/Digipomps/HAVEN}"
SLUG="style-parity-css-20260907"
BRANCH="claude/${SLUG}"
WT_ROOT="${HAVEN_ROOT}/_wt-${SLUG}"
WT_CP="${WT_ROOT}/CellProtocol"
WT_CS="${WT_ROOT}/CellScaffold"

APPLY=0
if [ "${1:-}" = "--apply" ]; then
    APPLY=1
fi

say() { printf '\n\033[1m== %s\033[0m\n' "$*"; }
run() {
    printf '   $ %s\n' "$*"
    if [ "$APPLY" -eq 1 ]; then
        "$@"
    fi
}

say "Forutsetninger"
for repo in CellProtocol CellScaffold; do
    if [ ! -d "${HAVEN_ROOT}/${repo}/.git" ]; then
        echo "MANGLER: ${HAVEN_ROOT}/${repo}" >&2
        exit 64
    fi
done
echo "   HAVEN_ROOT = ${HAVEN_ROOT}"
echo "   worktrees  = ${WT_ROOT}/{CellProtocol,CellScaffold}"
echo "   gren       = ${BRANCH}"

say "Base for endringen — bekreft at origin/main ikke har flyttet fila"
BASE_SHA_EXPECTED="e040c4c57e193845e5ae4fe9d58e7cc0e3c8353c0039e60983baed290a824d80"
git -C "${HAVEN_ROOT}/CellProtocol" fetch origin --quiet
ACTUAL="$(git -C "${HAVEN_ROOT}/CellProtocol" show origin/main:Sources/CellBase/Skeleton/SkeletonStyleParity.swift | shasum -a 256 | cut -d' ' -f1)"
echo "   forventet base : ${BASE_SHA_EXPECTED}"
echo "   origin/main na : ${ACTUAL}"
if [ "$ACTUAL" != "$BASE_SHA_EXPECTED" ]; then
    cat >&2 <<'MSG'

   STOPP. SkeletonStyleParity.swift paa origin/main er ikke den fila endringen
   ble laget mot. Endringen erstatter hele fila, saa den ville skrevet over det
   som har kommet til.

   Gjoer i stedet: diff patch/CellProtocol/SkeletonStyleParity.BASE.swift mot
   origin/main-versjonen, se hva som er nytt, og be Losen flette.
MSG
    exit 65
fi
echo "   OK — samme fil"

say "Worktrees fra origin/main"
run mkdir -p "${WT_ROOT}"
if [ ! -d "${WT_CP}" ]; then
    run git -C "${HAVEN_ROOT}/CellProtocol" worktree add -b "${BRANCH}" "${WT_CP}" origin/main
else
    echo "   finnes allerede: ${WT_CP}"
fi
git -C "${HAVEN_ROOT}/CellScaffold" fetch origin --quiet
if [ ! -d "${WT_CS}" ]; then
    run git -C "${HAVEN_ROOT}/CellScaffold" worktree add -b "${BRANCH}" "${WT_CS}" origin/main
else
    echo "   finnes allerede: ${WT_CS}"
fi

say "Kopier inn endringene"
run cp "${PATCH_DIR}/CellProtocol/Sources/CellBase/Skeleton/SkeletonStyleParity.swift" \
       "${WT_CP}/Sources/CellBase/Skeleton/SkeletonStyleParity.swift"
run cp "${PATCH_DIR}/CellScaffold/Tests/AppTests/SkeletonStyleParityCSSDriftTests.swift" \
       "${WT_CS}/Tests/AppTests/SkeletonStyleParityCSSDriftTests.swift"

say "CellProtocol — bygg og test"
run bash "${WT_CP}/Scripts/haven-swiftpm.sh" build --package-path "${WT_CP}"
run bash "${WT_CP}/Scripts/haven-swiftpm.sh" test --package-path "${WT_CP}" --filter SkeletonStyleParity

say "CellScaffold — drift-testen mot stilarkene"
if [ "$APPLY" -eq 1 ]; then
    (
        cd "${WT_CS}"
        CELLPROTOCOL_LOCAL_PACKAGE_PATH="${WT_CP}" \
        HAVEN_SWIFTPM_RUNNER="${WT_CP}/Scripts/haven-swiftpm.sh" \
        zsh Scripts/run_tests_isolated.sh --filter SkeletonStyleParityCSSDrift
    )
else
    echo "   \$ cd ${WT_CS} && CELLPROTOCOL_LOCAL_PACKAGE_PATH=${WT_CP} zsh Scripts/run_tests_isolated.sh --filter SkeletonStyleParityCSSDrift"
fi

say "Diff"
run git -C "${WT_CP}" --no-pager diff --stat
run git -C "${WT_CS}" --no-pager status --short

if [ "$APPLY" -eq 0 ]; then
    printf '\n\033[1mTørrkjøring. Kjør på nytt med --apply for å gjøre det.\033[0m\n\n'
else
    printf '\n\033[1mFerdig. Ikke commitet — se over diffen først.\033[0m\n\n'
fi
