"""Download the pinned third-party dataset files and verify SHA-256 checksums."""

from __future__ import annotations

import argparse
import hashlib
import urllib.request
from pathlib import Path

FILES = {
    "source_train.csv": (
        "https://huggingface.co/datasets/winvoker/turkish-sentiment-analysis-dataset/"
        "resolve/main/train.csv?download=true",
        "65316364341c2b8ff212f02022ebf0afcd6a384862e60613498bc41ecdb8c66e",
    ),
    "source_test.csv": (
        "https://huggingface.co/datasets/winvoker/turkish-sentiment-analysis-dataset/"
        "resolve/main/test.csv?download=true",
        "d3b72254ca956631081ecd60c847e2552615c56765216ee0ca31d72095172194",
    ),
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("data/raw"))
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    for name, (url, expected) in FILES.items():
        destination = args.output / name
        if not destination.exists() or sha256(destination) != expected:
            print(f"Downloading {name}...")
            urllib.request.urlretrieve(url, destination)
        actual = sha256(destination)
        if actual != expected:
            destination.unlink(missing_ok=True)
            raise RuntimeError(f"Checksum mismatch for {name}: {actual}")
        print(f"OK {name} {actual}")


if __name__ == "__main__":
    main()

