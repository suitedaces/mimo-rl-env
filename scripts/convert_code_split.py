#!/usr/bin/env python3

import argparse
import hashlib
import json
import os
import re
import subprocess
import tempfile
from pathlib import Path

import pyarrow.parquet as pq

from convert_code_task import write_task_from_row


def read_audits(audit_path: Path, metadata_path: Path, parquet_sha256: str, image_repo: str) -> dict[str, str]:
    audit = json.loads(audit_path.read_text())
    metadata = json.loads(metadata_path.read_text())
    if audit["parquet_sha256"] != parquet_sha256 or metadata["source_parquet_sha256"] != parquet_sha256:
        raise ValueError("image audits do not match the source Parquet")
    if audit["repository"] != image_repo or metadata["repository"] != image_repo:
        raise ValueError("image audits do not match the image repository")
    manifest_results = audit["results"]
    platform_results = metadata["results"]
    manifests = {item["instance_id"]: item for item in manifest_results}
    platforms = {item["instance_id"]: item for item in platform_results}
    if len(manifests) != len(manifest_results) or len(platforms) != len(platform_results) or set(manifests) != set(platforms):
        raise ValueError("image audit IDs are missing or duplicated")
    digests = {}
    for instance_id, manifest in manifests.items():
        images = platforms[instance_id]["linux_amd64_images"]
        digest = manifest["digest"]
        if manifest["http_status"] != 200 or platforms[instance_id]["tag_status"] != "active":
            raise ValueError(f"image is unavailable: {instance_id}")
        if len(images) != 1 or images[0]["digest"] != digest or not re.fullmatch(r"sha256:[0-9a-f]{64}", digest):
            raise ValueError(f"image manifest and platform metadata differ: {instance_id}")
        digests[instance_id] = digest
    return digests


def check_existing(task: Path, row_offset: int, instance: dict, source_revision: str, parquet_sha256: str, image: str) -> None:
    source = json.loads((task / "source.json").read_text())
    expected = {
        "dataset": "XiaomiMiMo/MiMo-V2.6-RL-oss",
        "revision": source_revision,
        "parquet_sha256": parquet_sha256,
        "row_offset": row_offset,
        "instance_id": instance["instance_id"],
        "docker_image": image,
        "original_test_command": instance["test_command"],
        "test_patch_sha256": hashlib.sha256(instance["test_patch"].encode()).hexdigest(),
    }
    if source != expected:
        raise ValueError(f"existing task has different source provenance: {task}")
    if (task / "tests" / "test.patch").read_bytes() != instance["test_patch"].encode():
        raise ValueError(f"existing task has different source test patch: {task}")
    if f"FROM --platform=linux/amd64 {image}\n" not in (task / "environment" / "Dockerfile").read_text():
        raise ValueError(f"existing task has different image: {task}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--parquet", type=Path, required=True)
    parser.add_argument("--expected-sha256", required=True)
    parser.add_argument("--image-audit", type=Path, required=True)
    parser.add_argument("--image-metadata", type=Path, required=True)
    parser.add_argument("--image-repo", required=True)
    parser.add_argument("--source-revision", required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    args = parser.parse_args()

    parquet_sha256 = hashlib.sha256(args.parquet.read_bytes()).hexdigest()
    if parquet_sha256 != args.expected_sha256:
        raise ValueError(f"Parquet SHA-256 mismatch: {parquet_sha256}")
    rows = pq.read_table(args.parquet).to_pylist()
    digests = read_audits(args.image_audit, args.image_metadata, parquet_sha256, args.image_repo)
    instances = []
    for offset, row in enumerate(rows):
        instance = json.loads(row["extra_info"]["instance_json"])
        instance_id = instance["instance_id"]
        if not re.fullmatch(r"format-code-task-[0-9]{6}", instance_id):
            raise ValueError(f"invalid task ID: {instance_id}")
        patch = instance["test_patch"]
        result = subprocess.run(["git", "apply", "--stat"], input=patch, text=True, capture_output=True)
        if result.returncode or not result.stdout:
            raise ValueError(f"test patch cannot be parsed for {instance_id}: {result.stderr}")
        instances.append((offset, row, instance))
    ids = [instance["instance_id"] for _, _, instance in instances]
    if len(ids) != len(set(ids)) or set(ids) != set(digests):
        raise ValueError("source task IDs and image audit IDs differ")

    args.output_root.mkdir(parents=True, exist_ok=True)
    created = 0
    skipped = 0
    for offset, row, instance in instances:
        instance_id = instance["instance_id"]
        image = f"{args.image_repo}@{digests[instance_id]}"
        task = args.output_root / instance_id
        if task.exists():
            check_existing(task, offset, instance, args.source_revision, parquet_sha256, image)
            skipped += 1
            continue
        with tempfile.TemporaryDirectory(prefix=".staging-", dir=args.output_root) as staging:
            staged_task = Path(staging) / instance_id
            write_task_from_row(offset, row, instance, args.image_repo, digests[instance_id], args.source_revision, parquet_sha256, staged_task)
            os.rename(staged_task, task)
        created += 1
    print(json.dumps({"source_rows": len(rows), "created": created, "verified_existing": skipped, "task_root": str(args.output_root)}))


if __name__ == "__main__":
    main()
