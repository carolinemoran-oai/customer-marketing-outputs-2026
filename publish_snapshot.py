from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parent
OUTPUT_PATH = ROOT / "data" / "latest_snapshot.csv"
PRIORITY_TERMS = (
    "dane",
    "master",
    "customer marketing",
    "goal tracking",
    "output",
)


def find_recent_csv() -> Path | None:
    candidates: list[tuple[int, float, Path]] = []
    for directory in (Path.home() / "Desktop", Path.home() / "Downloads"):
        if not directory.exists():
            continue
        for path in directory.glob("*.csv"):
            name = path.name.lower()
            score = sum(term in name for term in PRIORITY_TERMS)
            candidates.append((score, path.stat().st_mtime, path))

    candidates.sort(reverse=True)
    if not candidates or candidates[0][0] == 0:
        return None
    return candidates[0][2]


def validate_csv(path: Path) -> None:
    df = pd.read_csv(path, header=None, engine="python", on_bad_lines="skip").fillna("")
    text_values = {
        str(value).replace("\n", " ").strip().lower()
        for value in df.to_numpy().flatten()
        if str(value).strip()
    }
    required = {"annual goals", "ships grand total", "quarterly goals"}
    missing = sorted(required - text_values)
    if missing:
        raise ValueError(f"{path} does not look like the Dane dashboard CSV. Missing: {', '.join(missing)}")


def run(command: list[str]) -> None:
    subprocess.run(command, cwd=ROOT, check=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Publish the latest Dane dashboard CSV snapshot.")
    parser.add_argument("csv_path", nargs="?", type=Path, help="CSV export to publish. Defaults to the newest matching CSV in Desktop/Downloads.")
    parser.add_argument("--push", action="store_true", help="Commit and push the snapshot after publishing it.")
    args = parser.parse_args()

    source_path = args.csv_path or find_recent_csv()
    if source_path is None:
        raise SystemExit("No matching CSV found in Desktop or Downloads. Pass a CSV path explicitly.")

    source_path = source_path.expanduser().resolve()
    validate_csv(source_path)

    OUTPUT_PATH.parent.mkdir(exist_ok=True)
    shutil.copyfile(source_path, OUTPUT_PATH)
    print(f"Published {source_path.name} to {OUTPUT_PATH.relative_to(ROOT)}")

    if args.push:
        run(["git", "add", str(OUTPUT_PATH.relative_to(ROOT))])
        run(["git", "commit", "-m", "Update dashboard CSV snapshot"])
        run(["git", "push", "origin", "main"])


if __name__ == "__main__":
    main()
