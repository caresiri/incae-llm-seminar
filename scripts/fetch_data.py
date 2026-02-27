from __future__ import annotations

import argparse
import hashlib
import urllib.request
from pathlib import Path

import yaml


def sha256_of_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def download_file(url: str, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url) as response, target.open("wb") as handle:
        handle.write(response.read())


def main() -> None:
    parser = argparse.ArgumentParser(description="Download external data/model artifacts from a YAML manifest.")
    parser.add_argument(
        "--manifest",
        default=str(Path(__file__).resolve().parents[1] / "configs" / "data_sources.yaml"),
        help="Path to manifest YAML file",
    )
    args = parser.parse_args()

    manifest_path = Path(args.manifest).resolve()
    with manifest_path.open("r", encoding="utf-8") as handle:
        manifest = yaml.safe_load(handle) or {}

    entries = manifest.get("sources", [])
    if not entries:
        print("No sources found in manifest.")
        return

    repo_root = manifest_path.parents[1]
    for entry in entries:
        name = entry["name"]
        url = entry["url"]
        target = repo_root / entry["target"]
        expected_sha = entry.get("sha256")

        print(f"Downloading {name} -> {target}")
        download_file(url, target)

        if expected_sha:
            actual_sha = sha256_of_file(target)
            if actual_sha != expected_sha:
                raise ValueError(f"SHA256 mismatch for {name}: expected {expected_sha}, got {actual_sha}")

    print("Download complete.")


if __name__ == "__main__":
    main()

