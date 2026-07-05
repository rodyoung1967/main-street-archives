#!/usr/bin/env python3
"""One-time helper: move research-inbox aerials to media/photos/aerials/."""

from __future__ import annotations

import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INBOX = ROOT / "research-inbox"
OUT_DIR = ROOT / "media" / "photos" / "aerials"
START_ID = 6


def parse_name(name: str) -> tuple[int, str, str]:
    match = re.match(r"Aerial view 5th & Main (\d{4})(?: \((.+)\))?\.jpg", name, re.I)
    if not match:
        raise ValueError(f"Unexpected filename: {name}")
    year = int(match.group(1))
    note = match.group(2) or ""
    slug = str(year)
    if note:
        slug += "-" + re.sub(r"[^a-z0-9]+", "-", note.lower()).strip("-")
    return year, slug, note


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    files = sorted(INBOX.glob("*.jpg"), key=lambda p: parse_name(p.name))
    rows: list[str] = []
    for index, src in enumerate(files):
        year, slug, note = parse_name(src.name)
        img_id = f"IMG-{START_ID + index:04d}"
        dest_name = f"{img_id}_aerial_5th-main_{slug}.jpg"
        dest = OUT_DIR / dest_name
        shutil.move(str(src), str(dest))
        label = f"{year}" + (f" ({note})" if note else "")
        rows.append(
            f"| `{img_id}` | {label} | `{dest.relative_to(ROOT).as_posix()}` |"
        )
    readme = OUT_DIR / "README.md"
    readme.write_text(
        "# Aerial Photos — 5th & Main Street\n\n"
        "Oregon City photocompare aerial screenshots (`S-023`), cataloged under `E-021`.\n\n"
        "| Media ID | Year | Repository file |\n"
        "| --- | --- | --- |\n"
        + "\n".join(rows)
        + "\n",
        encoding="utf-8",
    )
    print(f"Moved {len(files)} files to {OUT_DIR}")
    print(f"Wrote {readme}")


if __name__ == "__main__":
    main()
