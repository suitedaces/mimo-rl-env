#!/usr/bin/env bash
set -uo pipefail
mkdir -p /logs/verifier
cd -- /testbed || exit 1
if ! git apply --check /tests/test.patch; then
  echo 0 > /logs/verifier/reward.txt
  exit 0
fi
if ! git apply /tests/test.patch; then
  echo 0 > /logs/verifier/reward.txt
  exit 0
fi
bash -lc 'bash /testbed/mimo_test_command.sh'
source_status=$?
node -e "const fs=require('fs'); const yaml=require('js-yaml'); const action=(yaml.load || yaml.safeLoad)(fs.readFileSync('action.yml', 'utf8')); if (action.inputs.secrets.required !== false || action.runs.main !== 'dist/index.js') process.exit(1)"
metadata_status=$?
touch /logs/verifier/github-env
env -u INPUT_SECRETS GITHUB_ENV=/logs/verifier/github-env INPUT_URL=http://vault.invalid:8200 INPUT_TOKEN=EXAMPLE INPUT_EXPORTTOKEN=true node dist/index.js > /logs/verifier/bundle.log 2>&1
bundle_status=$?
if [ "$source_status" -eq 0 ] && [ "$metadata_status" -eq 0 ] && [ "$bundle_status" -eq 0 ] && grep -q '^VAULT_TOKEN<<' /logs/verifier/github-env && grep -Fxq EXAMPLE /logs/verifier/github-env; then
  echo 1 > /logs/verifier/reward.txt
else
  echo "source_status=$source_status metadata_status=$metadata_status bundle_status=$bundle_status" >&2
  cat /logs/verifier/bundle.log >&2
  echo 0 > /logs/verifier/reward.txt
fi
