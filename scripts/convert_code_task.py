#!/usr/bin/env python3

import argparse
import hashlib
import json
import re
import shlex
from pathlib import Path
from urllib.parse import quote
from urllib.request import urlopen

import pyarrow.parquet as pq


def image_digest(repository: str, tag: str) -> str:
    url = f"https://hub.docker.com/v2/repositories/{repository}/tags/{quote(tag, safe='')}"
    with urlopen(url, timeout=30) as response:
        data = json.load(response)
    images = [image for image in data.get("images", []) if image.get("os") == "linux" and image.get("architecture") == "amd64"]
    if len(images) != 1 or not images[0].get("digest"):
        raise ValueError(f"expected one Linux amd64 image for {repository}:{tag}")
    return images[0]["digest"]


def load_row(parquet: Path, instance_id: str) -> tuple[int, dict, dict]:
    table = pq.read_table(parquet)
    for offset, row in enumerate(table.to_pylist()):
        extra = row["extra_info"]
        if extra["instance_id"] == instance_id:
            instance = json.loads(extra["instance_json"])
            if instance["instance_id"] != instance_id:
                raise ValueError("instance id mismatch")
            return offset, row, instance
    raise ValueError(f"instance id not found: {instance_id}")


def write_task_from_row(row_offset: int, row: dict, instance: dict, image_repo: str, digest: str, source_revision: str, parquet_sha256: str, output: Path) -> None:
    instance_id = instance["instance_id"]
    if not re.fullmatch(r"[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+", image_repo):
        raise ValueError(f"invalid Docker Hub repository: {image_repo}")
    if not re.fullmatch(r"sha256:[0-9a-f]{64}", digest):
        raise ValueError(f"invalid image digest: {digest}")
    if row["extra_info"]["instance_id"] != instance_id:
        raise ValueError("instance id mismatch")
    prompt = row["prompt"]
    if len(prompt) != 1 or prompt[0]["role"] != "user":
        raise ValueError("expected one user prompt")
    if prompt[0]["content"] != instance["problem_statement"]:
        raise ValueError("prompt and problem statement differ")
    if row["reward_model"]["style"] != "rule":
        raise ValueError("expected a rule-based verifier")
    cwd = instance["cwd"]
    if not re.fullmatch(r"/[a-zA-Z0-9_./-]*", cwd):
        raise ValueError("invalid working directory")
    original_image = instance["docker_image"]
    match = re.fullmatch(r"([a-zA-Z0-9_.-]+):latest", original_image)
    if not match or match.group(1) != instance_id:
        raise ValueError(f"unexpected source image name: {original_image}")
    image = f"{image_repo}@{digest}"
    patch = instance["test_patch"]
    command = instance["test_command"]
    if not (patch.startswith("diff --git ") or patch.startswith("--- ")) or not command:
        raise ValueError("missing test patch or command")
    if output.exists():
        raise FileExistsError(output)
    tests = output / "tests"
    tests.mkdir(parents=True)
    environment = output / "environment"
    environment.mkdir()
    (environment / "Dockerfile").write_text(
        f"FROM --platform=linux/amd64 {image}\n"
        f"WORKDIR {cwd}\n"
    )
    (output / "instruction.md").write_text(prompt[0]["content"].rstrip() + "\n")
    (tests / "test.patch").write_text(patch)
    (output / "task.toml").write_text(
        'schema_version = "1.3"\n\n'
        '[metadata]\n'
        f'source_dataset = "XiaomiMiMo/MiMo-V2.6-RL-oss"\n'
        f'source_revision = {json.dumps(source_revision)}\n'
        f'source_split = "code/train"\n'
        f'source_row_offset = {row_offset}\n'
        f'source_instance_id = {json.dumps(instance_id)}\n'
        f'source_image = {json.dumps(original_image)}\n'
        f'source_image_digest = {json.dumps(digest)}\n\n'
        '[verifier]\n'
        f'timeout_sec = {instance["verifier_timeout_sec"]}\n\n'
        '[environment]\n'
        f'workdir = {json.dumps(cwd)}\n'
    )
    test_script = f'''#!/usr/bin/env bash
set -uo pipefail
mkdir -p /logs/verifier
cd -- {shlex.quote(cwd)} || exit 1
if ! git apply --check /tests/test.patch; then
  echo 0 > /logs/verifier/reward.txt
  exit 0
fi
if ! git apply /tests/test.patch; then
  echo 0 > /logs/verifier/reward.txt
  exit 0
fi
bash -lc {shlex.quote(command)}
status=$?
if [ "$status" -eq 0 ]; then
  echo 1 > /logs/verifier/reward.txt
else
  echo 0 > /logs/verifier/reward.txt
fi
'''
    script_path = tests / "test.sh"
    script_path.write_text(test_script)
    script_path.chmod(0o755)
    provenance = {
        "dataset": "XiaomiMiMo/MiMo-V2.6-RL-oss",
        "revision": source_revision,
        "parquet_sha256": parquet_sha256,
        "row_offset": row_offset,
        "instance_id": instance_id,
        "docker_image": image,
        "original_test_command": command,
        "test_patch_sha256": hashlib.sha256(patch.encode()).hexdigest(),
    }
    (output / "source.json").write_text(json.dumps(provenance, indent=2) + "\n")


def write_task(parquet: Path, instance_id: str, image_repo: str, source_revision: str, expected_sha256: str, output: Path) -> None:
    parquet_sha256 = hashlib.sha256(parquet.read_bytes()).hexdigest()
    if parquet_sha256 != expected_sha256:
        raise ValueError(f"Parquet SHA-256 mismatch: {parquet_sha256}")
    row_offset, row, instance = load_row(parquet, instance_id)
    digest = image_digest(image_repo, instance_id)
    write_task_from_row(row_offset, row, instance, image_repo, digest, source_revision, parquet_sha256, output)
    print(output)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--parquet", type=Path, required=True)
    parser.add_argument("--instance-id", required=True)
    parser.add_argument("--image-repo", required=True)
    parser.add_argument("--source-revision", required=True)
    parser.add_argument("--expected-sha256", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    write_task(args.parquet, args.instance_id, args.image_repo, args.source_revision, args.expected_sha256, args.output)


if __name__ == "__main__":
    main()
