#!/usr/bin/env python3

from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import re
from urllib.parse import urlparse
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1] / "references"
INDEX_URL = "https://docs.harborframework.com/llms.txt"


def download(url: str) -> bytes:
    request = Request(url, headers={"User-Agent": "harbor-skill-docs-sync/1.0"})
    with urlopen(request, timeout=30) as response:
        content_type = response.headers.get("Content-Type", "")
        if "text/markdown" not in content_type and "text/plain" not in content_type:
            raise ValueError(f"unexpected content type for {url}: {content_type}")
        return response.read()


def main() -> None:
    index = download(INDEX_URL)
    urls = re.findall(rb"https://docs\.harborframework\.com/[^)]+\.md", index)
    if len(urls) != len(set(urls)):
        raise ValueError("documentation index has duplicate page URLs")
    decoded = [url.decode() for url in urls]
    with ThreadPoolExecutor(max_workers=8) as pool:
        pages = list(pool.map(download, decoded))
    manifest = {
        "source": INDEX_URL,
        "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
        "index_sha256": sha256(index).hexdigest(),
        "pages": {},
    }
    ROOT.mkdir(parents=True, exist_ok=True)
    (ROOT / "docs-index.md").write_bytes(index)
    for url, body in zip(decoded, pages):
        relative = urlparse(url).path.lstrip("/")
        destination = ROOT / "docs" / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(body)
        manifest["pages"][relative] = sha256(body).hexdigest()
    (ROOT / "snapshot.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"downloaded {len(pages)} Harbor documentation pages")


if __name__ == "__main__":
    main()
