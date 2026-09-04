#!/usr/bin/env bash
# CANNBot-Sentry unified installer.
# Usage:
#   ./install.sh                  # interactive / help
#   ./install.sh insight          # single package
#   ./install.sh cpx sift         # combination
#   ./install.sh all              # all packages
#
# Copyright (c) 2025-2026 Huawei Technologies Co., Ltd.
# This program is free software, you can redistribute it and/or modify it under the terms and conditions of
# CANN Open Software License Agreement Version 2.0 (the License).
# Please refer to the License for details. You may not use this file except in compliance with the License.
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY, OR FITNESS FOR A PARTICULAR PURPOSE.
# See LICENSE in the root of the software repository for the full text of the License.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ALL_PACKAGES=(insight cpx sift)

usage() {
    cat <<EOF
CANNBot-Sentry installer

Usage: ./install.sh [package ... | all]

Packages:
  insight   Session observability (Observe)
  cpx       Gateway, traffic capture (Capture)
  sift      Audit & evaluation (Audit / Evaluate)
  all       Install all packages
EOF
}

need() {
    command -v "$1" >/dev/null 2>&1 || { echo "[install] missing dependency: $1 (Node.js >= 20 recommended)" >&2; exit 1; }
}

install_package() {
    local pkg="$1"
    local dir="${REPO_ROOT}/packages/${pkg}"

    # Delegate to the package's own installer once the package has been migrated in.
    if [ -f "${dir}/install.sh" ]; then
        echo "[install] installing package: ${pkg}"
        bash "${dir}/install.sh"
        return
    fi

    echo "[install] package '${pkg}' is not migrated yet (placeholder); nothing to install." >&2
    return 1
}

main() {
    [ "$#" -eq 0 ] && { usage; exit 0; }

    local targets=()
    if [ "$1" = "all" ]; then
        targets=("${ALL_PACKAGES[@]}")
    else
        for arg in "$@"; do
            if [[ " ${ALL_PACKAGES[*]} " != *" ${arg} "* ]]; then
                echo "[install] unknown package: ${arg}" >&2
                usage
                exit 1
            fi
            targets+=("${arg}")
        done
    fi

    local failed=0
    for pkg in "${targets[@]}"; do
        install_package "${pkg}" || failed=1
    done
    [ "${failed}" -eq 0 ] && echo "[install] done." || echo "[install] finished with warnings (see above)." >&2
    exit "${failed}"
}

main "$@"
