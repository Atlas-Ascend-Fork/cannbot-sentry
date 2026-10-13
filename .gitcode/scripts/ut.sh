#!/bin/bash
# -----------------------------------------------------------------------------------------------------------
# Copyright (c) 2025 Huawei Technologies Co., Ltd.
# This program is free software, you can redistribute it and/or modify it under the terms and conditions of
# CANN Open Software License Agreement Version 2.0 (the "License").
# Please refer to the License for details. You may not use this file except in compliance with the License.
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY, OR FITNESS FOR A PARTICULAR PURPOSE.
# See LICENSE in the root of the software repository for the full text of the License.
# -----------------------------------------------------------------------------------------------------------
set -x
echo $(grep -E "^VERSION_ID=" /etc/os-release | cut -d'"' -f2)
if sudo update-alternatives --set gcc /usr/bin/gcc-16 2>/dev/null; then
    echo "Switched to gcc-16"
elif sudo update-alternatives --set gcc /usr/bin/gcc-15 2>/dev/null; then
    echo "Switched to gcc-15"
elif sudo update-alternatives --set gcc /usr/bin/gcc-14 2>/dev/null; then
    echo "gcc-16/15 not available, fell back to gcc-14"
fi

if gcc --version | head -n1 | grep -q "15\."; then
    rm -rf /home/jenkins/opensource/lib_cache
    if [ -d /home/jenkins/opensource/gcc15 ]; then
        rm -rf /home/jenkins/opensource/gcc15/lib_cache/abseil-cpp
        rm -rf /home/jenkins/opensource/gcc15/lib_cache/device/abseil-cpp
        ln -s /home/jenkins/opensource/gcc15/lib_cache/ /home/jenkins/opensource/lib_cache
    elif [ -d /home/jenkins/opensource/gcc15x86 ]; then
        rm -rf /home/jenkins/opensource/gcc15x86/lib_cache/abseil-cpp
        rm -rf /home/jenkins/opensource/gcc15x86/lib_cache/device/abseil-cpp
        ln -s /home/jenkins/opensource/gcc15x86/lib_cache/ /home/jenkins/opensource/lib_cache
    fi
elif gcc --version | head -n1 | grep -q "14\."; then
    gcc --version
else
    gcc --version
    rm -rf /home/jenkins/opensource/lib_cache
    ln -s /home/jenkins/opensource/ubuntu20/lib_cache /home/jenkins/opensource/lib_cache
fi
gcc --version
source /home/jenkins/Ascend/cann/bin/setenv.bash
set +e

# node 兜底：insight 要求 node>=22.12.0、cpx 要求 >=20，apt 源只有 18 不够；
# 从华为云 nodejs 镜像下载官方 v22 二进制到 /opt（同节点复用时缓存生效）
NODE_VER="v22.14.0"
NODE_DIR="/opt/node-${NODE_VER}"
need_node=0
if ! command -v node >/dev/null 2>&1; then
    need_node=1
elif [ "$(node -p 'parseInt(process.versions.node, 10)' 2>/dev/null || echo 0)" -lt 20 ]; then
    need_node=1
fi
if [ "$need_node" = 1 ] && [ ! -x "${NODE_DIR}/bin/node" ]; then
    echo "[ut] node >= 20 缺失，下载 ${NODE_VER}（华为云镜像）..."
    ARCH=$(uname -m); [ "$ARCH" = "aarch64" ] && NARCH="linux-arm64" || NARCH="linux-x64"
    curl -sSL --max-time 600 -o /tmp/node.tar.xz \
        "https://repo.huaweicloud.com/nodejs/${NODE_VER}/node-${NODE_VER}-${NARCH}.tar.xz" \
    && mkdir -p "${NODE_DIR}" \
    && tar -xJf /tmp/node.tar.xz -C "${NODE_DIR}" --strip-components=1 \
    && rm -f /tmp/node.tar.xz \
        || echo "[ut] WARN: node 下载/解压失败，insight/cpx 将无法执行"
fi
[ -x "${NODE_DIR}/bin/node" ] && export PATH="${NODE_DIR}/bin:$PATH"
node --version 2>/dev/null
npm --version 2>/dev/null

# sift 依赖前置：pyproject-only 包的 editable 安装（PEP 660）需要 pip>=21.3 + setuptools>=64，
# 容器 venv 自带 pip 可能是 21.2.4，预建 venv 并升级工具链后再进 run-tests.sh
if [ ! -x packages/sift/.venv/bin/python ]; then
    python3 -m venv packages/sift/.venv 2>/dev/null || true
fi
if [ -x packages/sift/.venv/bin/python ]; then
    packages/sift/.venv/bin/python -m pip install -U 'pip>=21.3' 'setuptools>=64' wheel \
        || echo "[ut] WARN: sift venv 工具链升级失败，继续按原流程执行"
fi

bash scripts/run-tests.sh all
ret=$?


if [ $ret -ne 200 ] && [ $ret -ne 0 ]; then
    echo "run ut fail"
    exit 1
fi
if [ $ret -eq 0 ]; then
    if [ "$coverage_save" = "true" ];then
    echo "ut_process=coverage" >> $ATOMGIT_OUTPUT
    else
    echo "ut_process=ut_cov" >> $ATOMGIT_OUTPUT
    fi
fi
exit 0
