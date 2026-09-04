#!/usr/bin/env python3
"""Run the P-498 integration with two narrow safeguards.

1. Preserve leading YAML indentation when appending generated records.
2. Select a CatalogIt derivative whose aspect ratio matches the steward-reviewed
   2048x1359 photograph, so unrelated square page assets cannot win by pixel area.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
MODULE_PATH = ROOT / "scripts/integrate_cchs_p498_harding_505_photo.py"

spec = importlib.util.spec_from_file_location("p498_integration", MODULE_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError(f"Cannot load {MODULE_PATH}")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def append_once_preserving_indentation(relpath: str, marker: str, block: str) -> None:
    path = ROOT / relpath
    text = path.read_text(encoding="utf-8")
    if marker in text:
        print(f"Already present: {relpath} :: {marker}")
        return
    if not text.endswith("\n"):
        text += "\n"
    # Do not .strip() here: the first two spaces on YAML list items are structural.
    text += "\n" + block.rstrip() + "\n"
    path.write_text(text, encoding="utf-8")


def recover_matching_image(page: str):
    urls = mod.extract_image_urls(page)
    if not urls:
        raise RuntimeError("P-498 record was found, but no public CCHS CloudFront JPEG derivative was exposed.")

    target_ratio = mod.STEWARD_WIDTH / mod.STEWARD_HEIGHT
    choices = []
    diagnostics = []
    tmp = ROOT / ".p498-candidate.jpg"

    for url in urls[:30]:
        try:
            data = mod.request_bytes(url, timeout=120)
            tmp.write_bytes(data)
            with Image.open(tmp) as im:
                width, height = im.size
                im.verify()
            ratio = width / height
            rel_error = abs(ratio - target_ratio) / target_ratio
            diagnostics.append(f"{width}x{height} rel_aspect_error={rel_error:.4f} {url}")
            if rel_error <= 0.08:
                name_rank = 3 if ("lg@2x" in url or "lg-nt@2x" in url) else 2 if "@2x" in url else 1
                choices.append((width * height, len(data), name_rank, -rel_error, url, data, width, height))
        except Exception as exc:
            diagnostics.append(f"ERROR {url}: {exc}")

    if tmp.exists():
        tmp.unlink()

    print("P-498 public derivative candidates:")
    for item in diagnostics:
        print("  " + item)

    if not choices:
        raise RuntimeError(
            "No exposed P-498 JPEG derivative matched the steward-reviewed photograph aspect ratio."
        )

    choices.sort(reverse=True, key=lambda item: (item[0], item[1], item[2], item[3]))
    _, _, _, _, url, data, width, height = choices[0]
    print(f"Selected aspect-matched derivative: {width}x{height} {url}")
    return url, data, width, height


mod.append_once = append_once_preserving_indentation
mod.recover_best_image = recover_matching_image
mod.main()
