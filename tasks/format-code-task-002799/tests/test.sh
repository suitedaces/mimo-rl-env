#!/usr/bin/env bash
set -uo pipefail
mkdir -p /logs/verifier
cd -- /workspace/repo || exit 1
if ! git apply --check /tests/test.patch; then
  echo 0 > /logs/verifier/reward.txt
  exit 0
fi
if ! git apply /tests/test.patch; then
  echo 0 > /logs/verifier/reward.txt
  exit 0
fi
bash -lc 'bash /workspace/repo/mimo_test_command.sh'
status=$?
if [ "$status" -eq 0 ]; then
  echo 1 > /logs/verifier/reward.txt
else
  echo 0 > /logs/verifier/reward.txt
fi
