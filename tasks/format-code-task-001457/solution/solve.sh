#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from pathlib import Path

action = Path('/testbed/src/action.js')
source = action.read_text()
before = "core.getInput('secrets', { required: true });"
after = "core.getInput('secrets', { required: false }) || '';"
if source.count(before) != 1:
    raise ValueError('unexpected action.js content')
action.write_text(source.replace(before, after))

metadata = Path('/testbed/action.yml')
source = metadata.read_text()
before = "  secrets:\n    description: 'A semicolon-separated list of secrets to retrieve. These will automatically be converted to environmental variable keys. See README for more details'\n    required: true"
after = before.replace('required: true', 'required: false')
if source.count(before) != 1:
    raise ValueError('unexpected action.yml content')
metadata.write_text(source.replace(before, after))
PY
npm run build
