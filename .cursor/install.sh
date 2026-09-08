#!/usr/bin/env bash
# Idempotent repository bootstrap for TheRock Cloud Agent environments.
#
# Installs the Python build-tooling and test/lint dependencies into the shared
# virtual environment created by .cursor/Dockerfile (already on PATH), then
# pre-caches the pre-commit hook environments so the first lint run is fast.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${REPO_ROOT}"

python -m pip install --upgrade pip

# requirements.txt (build tooling: meson, pre-commit, CppHeaderParser, ...) and
# requirements-test.txt (pytest and friends) pin conflicting versions of a few
# shared packages (notably boto3), so a single combined resolve fails. Install
# them sequentially the way the project's own CI and build flows do; the
# test-requirements pins win for the overlapping packages.
python -m pip install -r requirements.txt
python -m pip install -r requirements-test.txt

# Warm the pre-commit hook caches (black, clang-format, mdformat, actionlint,
# ...). Safe to re-run; pre-commit reuses already-installed hook environments.
if [ -f .pre-commit-config.yaml ]; then
    pre-commit install-hooks
fi
