#!/usr/bin/env python3

import argparse
import hashlib
import json
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import pyarrow.parquet as pq


ACCEPT = ", ".join([
    "application/vnd.oci.image.index.v1+json",
    "application/vnd.docker.distribution.manifest.list.v2+json",
    "application/vnd.oci.image.manifest.v1+json",
    "application/vnd.docker.distribution.manifest.v2+json",
])


def read_instance_ids(parquet: Path) -> list[str]:
    rows = pq.read_table(parquet, columns=["extra_info"]).to_pylist()
    ids = []
    for row in rows:
        extra = row["extra_info"]
        instance = json.loads(extra["instance_json"])
        instance_id = extra["instance_id"]
        if not re.fullmatch(r"[a-zA-Z0-9_.-]+", instance_id):
            raise ValueError(f"invalid instance id: {instance_id!r}")
        if instance["instance_id"] != instance_id:
            raise ValueError(f"instance id mismatch: {instance_id}")
        if instance["docker_image"] != f"{instance_id}:latest":
            raise ValueError(f"unexpected image reference: {instance_id}")
        ids.append(instance_id)
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate instance ids")
    return ids


def registry_token(repository: str) -> str:
    query = urlencode({"service": "registry.docker.io", "scope": f"repository:{repository}:pull"})
    with urlopen(f"https://auth.docker.io/token?{query}", timeout=30) as response:
        return json.load(response)["token"]


def fetch_tags(repository: str, token: str) -> set[str]:
    url = f"https://registry-1.docker.io/v2/{repository}/tags/list?n=10000"
    request = Request(url, headers={"Authorization": f"Bearer {token}"})
    with urlopen(request, timeout=30) as response:
        if response.headers.get("Link"):
            raise ValueError("tag list is paginated")
        return set(json.load(response).get("tags") or [])


def check_manifest(repository: str, instance_id: str, token: str) -> dict:
    url = f"https://registry-1.docker.io/v2/{repository}/manifests/{instance_id}"
    headers = {"Authorization": f"Bearer {token}", "Accept": ACCEPT}
    for attempt in range(4):
        try:
            with urlopen(Request(url, headers=headers, method="HEAD"), timeout=30) as response:
                return {
                    "instance_id": instance_id,
                    "http_status": response.status,
                    "digest": response.headers.get("Docker-Content-Digest"),
                    "content_type": response.headers.get("Content-Type"),
                }
        except HTTPError as error:
            if error.code not in (429, 500, 502, 503, 504) or attempt == 3:
                return {"instance_id": instance_id, "http_status": error.code, "error": str(error)}
        except (URLError, TimeoutError, OSError) as error:
            if attempt == 3:
                return {"instance_id": instance_id, "http_status": None, "error": str(error)}
        time.sleep(2 ** attempt)
    raise AssertionError("unreachable")


def write_report(path: Path, repository: str, parquet_sha256: str, ids: list[str], tags: set[str], results: list[dict]) -> None:
    resolved = sum(
        result.get("http_status") == 200
        and re.fullmatch(r"sha256:[0-9a-f]{64}", result.get("digest") or "") is not None
        for result in results
    )
    report = {
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "repository": repository,
        "parquet_sha256": parquet_sha256,
        "method": "anonymous registry tag list and manifest HEAD",
        "summary": {
            "total_dataset_images": len(ids),
            "tags_present": len(set(ids) & tags),
            "tags_missing": len(set(ids) - tags),
            "manifests_checked": len(results),
            "manifests_resolved": resolved,
            "manifest_errors": len(results) - resolved,
        },
        "results": sorted(results, key=lambda result: result["instance_id"]),
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--parquet", type=Path, required=True)
    parser.add_argument("--expected-sha256", required=True)
    parser.add_argument("--repository", default="xiaomimimo/mimo-v2.6-rl-oss")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--workers", type=int, default=6)
    args = parser.parse_args()
    if not re.fullmatch(r"[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+", args.repository):
        raise ValueError("invalid repository")
    if args.workers < 1 or args.workers > 16:
        raise ValueError("workers must be between 1 and 16")
    parquet_sha256 = hashlib.sha256(args.parquet.read_bytes()).hexdigest()
    if parquet_sha256 != args.expected_sha256:
        raise ValueError(f"Parquet SHA-256 mismatch: {parquet_sha256}")
    ids = read_instance_ids(args.parquet)
    tags = fetch_tags(args.repository, registry_token(args.repository))
    results = []
    for start in range(0, len(ids), 250):
        token = registry_token(args.repository)
        batch = ids[start:start + 250]
        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            futures = [pool.submit(check_manifest, args.repository, instance_id, token) for instance_id in batch]
            for future in as_completed(futures):
                results.append(future.result())
        write_report(args.output, args.repository, parquet_sha256, ids, tags, results)
        print(f"checked {len(results)}/{len(ids)}", flush=True)
    print(json.dumps(json.loads(args.output.read_text())["summary"], indent=2))


if __name__ == "__main__":
    main()
