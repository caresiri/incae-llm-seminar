from __future__ import annotations

from pathlib import Path

import nbformat


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    notebooks = sorted((repo_root / "notebooks").rglob("*.ipynb"))

    if not notebooks:
        raise SystemExit("No notebooks found under notebooks/.")

    for nb_path in notebooks:
        with nb_path.open("r", encoding="utf-8") as handle:
            nbformat.read(handle, as_version=4)
        print(f"Validated notebook JSON: {nb_path}")


if __name__ == "__main__":
    main()

