#!/usr/bin/env python3

import argparse
import hashlib
import json
import tomllib
from pathlib import Path

import pyarrow.parquet as pq

from convert_code_split import read_audits


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--parquet", type=Path, required=True)
    parser.add_argument("--expected-sha256", required=True)
    parser.add_argument("--image-audit", type=Path, required=True)
    parser.add_argument("--image-metadata", type=Path, required=True)
    parser.add_argument("--image-repo", required=True)
    parser.add_argument("--source-revision", required=True)
    parser.add_argument("--task-root", type=Path, required=True)
    args = parser.parse_args()

    parquet_sha256 = hashlib.sha256(args.parquet.read_bytes()).hexdigest()
    if parquet_sha256 != args.expected_sha256:
        raise ValueError("source Parquet SHA-256 mismatch")
    rows = pq.read_table(args.parquet).to_pylist()
    digests = read_audits(args.image_audit, args.image_metadata, parquet_sha256, args.image_repo)
    task_dirs = {p.name: p for p in args.task_root.iterdir() if p.is_dir()}
    ids = {row["extra_info"]["instance_id"] for row in rows}
    if len(rows) != len(ids) or set(task_dirs) != ids or set(digests) != ids:
        raise ValueError("task folders, source rows, or image manifests differ")

    for offset, row in enumerate(rows):
        instance = json.loads(row["extra_info"]["instance_json"])
        instance_id = instance["instance_id"]
        task = task_dirs[instance_id]
        image = f"{args.image_repo}@{digests[instance_id]}"
        source = json.loads((task / "source.json").read_text())
        if source != {
            "dataset": "XiaomiMiMo/MiMo-V2.6-RL-oss",
            "revision": args.source_revision,
            "parquet_sha256": parquet_sha256,
            "row_offset": offset,
            "instance_id": instance_id,
            "docker_image": image,
            "original_test_command": instance["test_command"],
            "test_patch_sha256": hashlib.sha256(instance["test_patch"].encode()).hexdigest(),
        }:
            raise ValueError(f"source provenance differs: {instance_id}")
        if (task / "tests" / "test.patch").read_bytes() != instance["test_patch"].encode():
            raise ValueError(f"test patch differs: {instance_id}")
        if f"FROM --platform=linux/amd64 {image}\n" not in (task / "environment" / "Dockerfile").read_text():
            raise ValueError(f"Dockerfile image differs: {instance_id}")
        instruction = (task / "instruction.md").read_bytes()
        prompt = row["prompt"][0]["content"].rstrip()
        if instance_id == "format-code-task-001457":
            if not instruction.decode().replace("\r\n", "\n").startswith(prompt.replace("\r\n", "\n") + "\n"):
                raise ValueError(f"pilot source instruction differs: {instance_id}")
        elif instruction != (prompt + "\n").encode():
            raise ValueError(f"instruction differs: {instance_id}")
        script = (task / "tests" / "test.sh").read_text()
        if f"bash -lc '{instance['test_command']}'" not in script and f"bash -lc {instance['test_command']}" not in script:
            raise ValueError(f"test command differs: {instance_id}")
        config = tomllib.loads((task / "task.toml").read_text())
        if config["metadata"]["source_row_offset"] != offset or config["metadata"]["source_image_digest"] != digests[instance_id]:
            raise ValueError(f"task metadata differs: {instance_id}")
        if config["environment"]["workdir"] != instance["cwd"] or config["verifier"]["timeout_sec"] != instance["verifier_timeout_sec"]:
            raise ValueError(f"task environment or verifier differs: {instance_id}")
        if not (task / "tests" / "test.sh").stat().st_mode & 0o111:
            raise ValueError(f"verifier is not executable: {instance_id}")
    print(json.dumps({"source_rows": len(rows), "validated_task_folders": len(task_dirs), "validated_dockerfiles": len(task_dirs), "validated_test_patches": len(task_dirs)}))


if __name__ == "__main__":
    main()
