#!/usr/bin/env python3
"""Integrate the steward-supplied CCHS P-498 Harding Drug Store photograph.

The current ChatGPT attachment cannot be mounted inside a GitHub Actions runner, so this
script recovers the same catalog object from the public CCHS CatalogIt record and preserves
the largest public image derivative.  It separately records the steward attachment's exact
filename, dimensions, byte size, and SHA-256 so provenance is not collapsed.
"""

from __future__ import annotations

import hashlib
import html
import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SITEMAP = "https://hub.catalogit.app/clackamas-county-historical-society/sitemap.html"
ACCOUNT_ROOT = "https://hub.catalogit.app/clackamas-county-historical-society/"
TARGET = ROOT / "media/photos/early-main-street/IMG-0740_circa-1885-harding-drug-store-505-main-cchs-p498.jpg"
CAPTURE = ROOT / "evidence/source-captures/circa-1885-cchs-p498-harding-drug-store-505-main-photo-2026-09-04.md"
JSON_CAPTURE = ROOT / "evidence/source-captures/circa-1885-cchs-p498-catalogit-recovery-2026-09-04.json"

STEWARD_FILENAME = "Harding Drug Store - 505 Main Street.jpg"
STEWARD_WIDTH = 2048
STEWARD_HEIGHT = 1359
STEWARD_BYTES = 528546
STEWARD_SHA256 = "11037b073c6d17b1196b118e9ab3bed0c24b38b0edd72e76323ce9c6244d4e1c"

UA = "Mozilla/5.0 (compatible; main-street-archives/1.0; historical-research)"


def request_bytes(url: str, timeout: int = 120) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def request_text(url: str, timeout: int = 120) -> str:
    raw = request_bytes(url, timeout)
    return raw.decode("utf-8", errors="replace")


def clean_anchor_text(value: str) -> str:
    value = re.sub(r"<[^>]+>", " ", value)
    return re.sub(r"\s+", " ", html.unescape(value)).strip()


def candidate_record_urls() -> list[str]:
    urls: list[str] = []
    try:
        sitemap = request_text(SITEMAP, timeout=180)
        for href, label in re.findall(
            r"<a\b[^>]*href=[\"']([^\"']+)[\"'][^>]*>(.*?)</a>",
            sitemap,
            flags=re.I | re.S,
        ):
            label_text = clean_anchor_text(label).lower()
            if "harding" in label_text and "drug store" in label_text and "505 main" in label_text:
                urls.append(urllib.parse.urljoin(ACCOUNT_ROOT, html.unescape(href)))
        # Some sitemap renderings expose URLs in text without an anchor label.
        for href in re.findall(r"https://hub\.catalogit\.app/clackamas-county-historical-society/[^\s\"'<>]+", sitemap):
            if "harding" in href.lower() and "505" in href.lower():
                urls.append(html.unescape(href))
    except Exception as exc:
        print(f"CatalogIt sitemap retrieval warning: {exc}", file=sys.stderr)

    # Slug fallbacks.  The first pair is intentionally distinct from the older
    # 'George Harding Drug Store' record already archived as IMG-0724.
    urls.extend(
        [
            ACCOUNT_ROOT + "folder/entry/harding-drug-store-505-main-street",
            ACCOUNT_ROOT + "folder/photographs/entry/harding-drug-store-505-main-street",
            ACCOUNT_ROOT + "folder/entry/harding-drug-store---505-main-street",
            ACCOUNT_ROOT + "folder/photographs/entry/harding-drug-store---505-main-street",
            ACCOUNT_ROOT + "folder/entry/george-a.-harding-store-505-main-street",
            ACCOUNT_ROOT + "folder/photographs/entry/george-a.-harding-store-505-main-street",
        ]
    )

    seen: set[str] = set()
    ordered: list[str] = []
    for url in urls:
        url = url.rstrip(".,)")
        if url not in seen:
            seen.add(url)
            ordered.append(url)
    return ordered


def find_record() -> tuple[str, str]:
    attempts: list[str] = []
    for url in candidate_record_urls():
        try:
            page = request_text(url, timeout=90)
        except Exception as exc:
            attempts.append(f"{url} -> {type(exc).__name__}: {exc}")
            continue
        flat = clean_anchor_text(page)
        # Require the external object ID plus the relevant Harding/505 wording.
        if "P-498" in flat and "Harding" in flat and "505 Main" in flat:
            return url, page
        attempts.append(f"{url} -> fetched but did not match external object P-498")
    raise RuntimeError("Could not locate the CCHS P-498 record. Attempts:\n" + "\n".join(attempts[:30]))


def extract_image_urls(page: str) -> list[str]:
    expanded = html.unescape(page)
    expanded = expanded.replace("\\u002F", "/").replace("\\/", "/")
    expanded = expanded.replace("\\u0040", "@").replace("\\u0026", "&")
    found = re.findall(
        r"https://(?:d8e7jbdw4fu0e|d3f1jyudfg58oi)\.cloudfront\.net/[^\"'<>\s\\]+?\.(?:jpg|jpeg)",
        expanded,
        flags=re.I,
    )
    urls: list[str] = []
    seen: set[str] = set()
    for url in found:
        url = urllib.parse.unquote(url).replace("&amp;", "&")
        if url not in seen:
            seen.add(url)
            urls.append(url)
    return urls


def recover_best_image(page: str) -> tuple[str, bytes, int, int]:
    urls = extract_image_urls(page)
    if not urls:
        raise RuntimeError("P-498 record was found, but no public CCHS CloudFront JPEG derivative was exposed.")

    choices: list[tuple[int, int, int, str, bytes, int, int]] = []
    tmp = ROOT / ".p498-candidate.jpg"
    for url in urls[:20]:
        try:
            data = request_bytes(url, timeout=120)
            tmp.write_bytes(data)
            with Image.open(tmp) as im:
                width, height = im.size
                im.verify()
            # Favor pixel area, then byte size.  A small name-rank breaks otherwise equal ties.
            name_rank = 3 if ("lg@2x" in url or "lg-nt@2x" in url) else 2 if "@2x" in url else 1
            choices.append((width * height, len(data), name_rank, url, data, width, height))
        except Exception as exc:
            print(f"Derivative warning: {url} -> {exc}", file=sys.stderr)
    if tmp.exists():
        tmp.unlink()
    if not choices:
        raise RuntimeError("No exposed P-498 JPEG derivative could be downloaded and verified.")
    choices.sort(reverse=True, key=lambda item: (item[0], item[1], item[2]))
    _, _, _, url, data, width, height = choices[0]
    return url, data, width, height


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def append_once(relpath: str, marker: str, block: str) -> None:
    path = ROOT / relpath
    text = path.read_text(encoding="utf-8")
    if marker in text:
        print(f"Already present: {relpath} :: {marker}")
        return
    if not text.endswith("\n"):
        text += "\n"
    text += "\n" + block.strip() + "\n"
    path.write_text(text, encoding="utf-8")


def write_new(path: Path, content: str) -> None:
    if path.exists():
        existing = path.read_text(encoding="utf-8")
        if existing == content:
            return
        raise RuntimeError(f"Refusing to replace existing non-identical file: {path.relative_to(ROOT)}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def assert_ids_available() -> None:
    checks = [
        ("evidence/source-register.md", "## S-211 —"),
        ("evidence/evidence-register.md", "## E-191 —"),
        ("media/photo-metadata-register.md", "## IMG-0740 —"),
        ("database/sources.yml", "  - id: S-211\n"),
        ("database/evidence.yml", "  - id: E-191\n"),
    ]
    occupied = [(p, m) for p, m in checks if m in (ROOT / p).read_text(encoding="utf-8")]
    if occupied:
        # A complete prior run is harmless.
        if len(occupied) == len(checks) and TARGET.exists():
            print("P-498 integration already complete.")
            raise SystemExit(0)
        raise RuntimeError(f"Partial/pre-existing ID collision detected: {occupied}")


def main() -> None:
    assert_ids_available()

    record_url, page = find_record()
    image_url, image_bytes, repo_width, repo_height = recover_best_image(page)
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    TARGET.write_bytes(image_bytes)
    repo_sha = sha256(image_bytes)
    repo_bytes = len(image_bytes)

    # Archive the recovery metadata in machine-readable form without storing the full HTML page.
    recovery = {
        "reviewed": "2026-09-04",
        "institution": "Clackamas County Historical Society",
        "external_object_id": "P-498",
        "record_url": record_url,
        "selected_public_derivative_url": image_url,
        "repository_file": str(TARGET.relative_to(ROOT)),
        "repository_derivative": {
            "width": repo_width,
            "height": repo_height,
            "bytes": repo_bytes,
            "sha256": repo_sha,
        },
        "steward_attachment": {
            "filename": STEWARD_FILENAME,
            "width": STEWARD_WIDTH,
            "height": STEWARD_HEIGHT,
            "bytes": STEWARD_BYTES,
            "sha256": STEWARD_SHA256,
        },
        "catalog_metadata_supplied_by_steward": {
            "title": "Harding Drug Store - 505 Main Street",
            "description": "Harding Drug Store - 505 Main Street. George A. Harding store. Harding moved to the shop north and George Young moved into this location JAH 11/2022",
            "date_made": "circa 1885",
            "city": "Oregon City",
            "county": "Clackamas",
            "state": "Oregon",
            "country": "United States of America",
            "continent": "North America",
            "medium": "Photographic Paper",
        },
    }
    JSON_CAPTURE.write_text(json.dumps(recovery, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    same_bytes = repo_sha == STEWARD_SHA256
    derivative_note = (
        "The committed public derivative is an exact byte match to the steward attachment."
        if same_bytes
        else "The committed file is the largest live public CCHS derivative recovered from the same MOT:P-498 record; it is not byte-identical to the steward attachment."
    )

    capture_text = f"""# CCHS MOT:P-498 — Harding Drug Store, 505 Main Street, circa 1885

Reviewed **4 September 2026** from the project-steward supplied 2048 × 1359 JPEG and the live Clackamas County Historical Society CatalogIt record recovered by the repository integration runner.

Status: **INSTITUTIONAL CATALOG METADATA + DIRECT VISUAL PHOTOGRAPH REVIEW; DATE/ADDRESS RETROSPECTIVE CAUTION APPLIES.**

Archive IDs: source `S-211`; evidence `E-191`; image `IMG-0740`; business `BUS-007`; person `P-001`; building/address record `B-002`.

## Catalog record

- Institutional title: **Harding Drug Store - 505 Main Street**
- External Entry/Object ID: `MOT:P-498` (the supplied catalog display reads **P‑498**; namespaced here to avoid collision with Main Street Archive person IDs)
- Description supplied by the catalog/steward: **Harding Drug Store - 505 Main Street. George A. Harding store. Harding moved to the shop north and George Young moved into this location JAH 11/2022**
- Date made: **circa 1885**
- Place: Oregon City, Clackamas County, Oregon, United States of America, North America
- Medium: **Photographic Paper**
- Live record: {record_url}

## Steward attachment

- Original filename: `{STEWARD_FILENAME}`
- Dimensions: **{STEWARD_WIDTH} × {STEWARD_HEIGHT}**
- Bytes: **{STEWARD_BYTES:,}**
- SHA-256: `{STEWARD_SHA256}`

## Repository image

- File: `{TARGET.relative_to(ROOT)}`
- Recovered live CCHS derivative: {image_url}
- Dimensions: **{repo_width} × {repo_height}**
- Bytes: **{repo_bytes:,}**
- SHA-256: `{repo_sha}`
- Integrity/provenance: {derivative_note}

## Direct visual observation

The full-frame photograph visibly shows the **George A. Harding** storefront fascia, two large display windows, the central entrance, merchandise displays, and several men posed in front. The supplied full frame also carries a **Clackamas County Historical Society** watermark across the image. No street number is visibly readable in the photographed storefront.

## Relationship to existing IMG-0724

`IMG-0724` / `S-148` / `E-133` preserves a separate CCHS catalog object (`2008.008.046.080`) for what appears to be the **same underlying historical exposure**, but that steward-supplied file was only a **400 × 400 crop** of the upper fascia. MOT:P-498 is therefore not discarded as a redundant byte duplicate: it supplies a materially fuller frame, a distinct institutional object ID/provenance trail, a different date statement (**circa 1885** rather than the older record's structured **1880** / caption **1880s**), a different medium statement, and the later JAH 11/2022 catalog annotation.

Treat the two CCHS catalog records as **substantive-image relatives / likely same exposure**, not as interchangeable metadata records. Their differing date precision is preserved as a catalog conflict rather than silently harmonized.

## Historical limits

1. **505 Main is institutional retrospective metadata**, not a number visible in the photograph. Oregon City's formal citywide numbering work is documented in 1906, so the circa-1885 image cannot prove that `505` was displayed or officially assigned at exposure time.
2. **Circa 1885 is catalog dating**, not a date visible in the image. The separate CCHS record behind `IMG-0724` uses 1880/1880s wording.
3. The JAH 11/2022 statement that Harding moved north and George Young moved into this location is preserved as a **retrospective catalog annotation**. It is useful as a research lead and is compatible with the independently documented later Young-at-505 / move-north sequence, but it does not supply an exact move date or by itself prove that the same physical structure survived into Young's occupancy.
4. The photograph does **not** prove continuity to the surviving 505 Main building, property ownership, the exact footprint of the later Harding Building, or uninterrupted tenancy.

## Corroborating project context

Independent project evidence directly advertises **Young's Second Hand Store at 505 Main on 16 August 1907** (`S-189` / `E-168`) and visibly shows Young's Secondhand Store with **505** above the doorway in the CCHS photograph dated 1910 (`S-149` / `E-134` / `IMG-0725`). A March 1911 newspaper report then says Young moved one door north from Harding Building premises into the Willamette Building (`E-085`), and later exact records place Young at 507. Those sources make the 2022 catalog annotation historically plausible, but they remain separate evidence and do not convert the circa-1885 photograph into proof of a precise Harding→Young transfer date.
"""
    write_new(CAPTURE, capture_text)

    append_once(
        "evidence/source-register.md",
        "## S-211 —",
        f"""## S-211 — Clackamas County Historical Society MOT:P-498, Harding Drug Store — 505 Main Street, circa 1885
Type: Institutional photograph/catalog metadata plus steward-supplied image; **VISUALLY VERIFIED 4 September 2026**.  
Catalog record: {record_url}  
Repository image: `{TARGET.relative_to(ROOT)}`  
Source capture: `{CAPTURE.relative_to(ROOT)}`  
Related evidence/media: `E-191` / `IMG-0740`; related business/person/building: `BUS-007` / `P-001` / `B-002`.  
Notes: Catalog title identifies Harding Drug Store at 505 Main, date made circa 1885, medium Photographic Paper, and carries a later JAH 11/2022 annotation saying Harding moved north and George Young moved into this location. The full photograph visibly shows the Harding fascia/storefront but no street number. Because formal citywide numbering is documented in 1906, 505 is treated as retrospective institutional metadata. MOT:P-498 appears to preserve the same underlying exposure as the older cropped `IMG-0724` record but is retained because it supplies a materially fuller frame and distinct catalog metadata/provenance. Steward attachment SHA-256 `{STEWARD_SHA256}`; committed derivative SHA-256 `{repo_sha}`.""",
    )

    append_once(
        "evidence/evidence-register.md",
        "## E-191 —",
        """## E-191 — CCHS MOT:P-498 catalogs Harding Drug Store at 505 Main circa 1885
Type: Institutional photograph/catalog metadata plus direct visual review; **DOCUMENTED / VISUALLY VERIFIED**, with retrospective-address and date-precision cautions.  
Source: `S-211`; image `IMG-0740`; related `S-148` / `E-133` / `IMG-0724`.  
Claims: CCHS MOT:P-498 catalogs **Harding Drug Store - 505 Main Street**, date **circa 1885**, medium **Photographic Paper**. The full-frame image visibly shows the George A. Harding storefront fascia, display windows and entrance, but no readable street number. The catalog description also preserves a JAH 11/2022 note that Harding moved north and George Young moved into this location. That move statement is retrospective institutional annotation, not a contemporary transfer record. MOT:P-498 appears to show the same underlying exposure as cropped `IMG-0724`, but the records carry different date/medium metadata and are not collapsed.  
Limits: `505 Main` is not visible in the image and may be a retrospective post-1906 address; circa 1885 is not an image-visible date; no present-building continuity, property ownership, exact Harding→Young transfer date, or surviving fabric is proved.  
Confidence: **Very High** for catalog wording and direct visible storefront content; **UNRESOLVED** for exact exposure date, retrospective numbered-address precision, and structural continuity.""",
    )

    append_once(
        "database/sources.yml",
        "  - id: S-211\n",
        f'''  - id: S-211
    name: "Clackamas County Historical Society MOT:P-498, Harding Drug Store — 505 Main Street, circa 1885"
    url: "{record_url}"
    repository_file: "{TARGET.relative_to(ROOT)}"
    notes: "CCHS MOT:P-498; steward-supplied 2048x1359 JPEG visually verified. Catalog identifies Harding Drug Store - 505 Main Street, date circa 1885, medium Photographic Paper, and carries a retrospective JAH 11/2022 Harding-moved-north/George-Young-moved-in annotation. Image itself shows the Harding storefront but no readable street number. 505 is retrospective institutional metadata because formal citywide numbering is documented in 1906. MOT:P-498 appears to be the same underlying historical exposure as cropped IMG-0724 but is preserved as a distinct catalog object/full-frame derivative. Steward SHA-256 {STEWARD_SHA256}; repository derivative SHA-256 {repo_sha}."
    related_evidence: [E-191]
    related_media: [IMG-0740]''',
    )

    append_once(
        "database/evidence.yml",
        "  - id: E-191\n",
        '''  - id: E-191
    name: "CCHS MOT:P-498 catalogs Harding Drug Store at 505 Main circa 1885"
    type: "Institutional photograph/catalog metadata plus direct visual review; documented/visually verified with retrospective-address and date-precision cautions"
    claims:
      - "CCHS MOT:P-498 catalogs Harding Drug Store - 505 Main Street, date circa 1885, medium Photographic Paper."
      - "The full-frame photograph visibly shows the George A. Harding storefront fascia, display windows and entrance; no readable street number is visible."
      - "The JAH 11/2022 Harding-moved-north/George-Young-moved-in statement is retrospective catalog annotation, not a contemporary transfer record."
      - "MOT:P-498 appears to preserve the same underlying exposure as cropped IMG-0724, but the distinct catalog records and differing date/medium metadata are retained rather than collapsed."
    confidence: "Very High for catalog wording and visible storefront content; unresolved for exact exposure date, retrospective numbered-address precision, Harding-to-Young transfer timing and structural continuity."
    related_sources: [S-211, S-148]
    related_people: [P-001, P-076]
    related_businesses: [BUS-007, BUS-067]
    related_buildings: [B-002]''',
    )

    append_once(
        "media/photo-metadata-register.md",
        "## IMG-0740 —",
        f"""## IMG-0740 — CCHS MOT:P-498 Harding Drug Store, 505 Main, circa 1885 full frame

- Type: Institutional historic photograph / full storefront view
- CCHS external object: `MOT:P-498` (catalog display **P‑498**)
- Catalog title: **Harding Drug Store - 505 Main Street**
- Catalog date: **circa 1885**
- Repository file: `{TARGET.relative_to(ROOT)}`
- Status: `committed`
- Repository derivative: {repo_width} × {repo_height}; {repo_bytes:,} bytes; SHA-256 `{repo_sha}`
- Steward attachment: `{STEWARD_FILENAME}`; {STEWARD_WIDTH} × {STEWARD_HEIGHT}; {STEWARD_BYTES:,} bytes; SHA-256 `{STEWARD_SHA256}`
- Source/evidence: `S-211` / `E-191`
- Related business/person/building: `BUS-007` / `P-001` / `B-002`
- Visual note: Full frame visibly shows the George A. Harding fascia, display windows, central entrance, merchandise and several posed men; no readable street number is visible.
- Duplicate/provenance note: Appears to be the same underlying exposure as `IMG-0724`, but `IMG-0724` is only a 400 × 400 crop tied to a different CCHS catalog object and 1880/1880s metadata. MOT:P-498 is retained as a materially fuller frame and distinct institutional record.
- Historical caution: `505 Main` and circa 1885 are catalog metadata. The 2022 Harding/Young move annotation is retrospective and is not treated as a contemporary transfer record or proof of present-building continuity.""",
    )

    append_once(
        "media/photos/inventory.md",
        "### IMG-0740 —",
        f"""### IMG-0740 — CCHS MOT:P-498 Harding Drug Store, 505 Main, circa 1885
- File: `{TARGET.relative_to(ROOT)}`
- Source/evidence: `S-211` / `E-191`
- CCHS object: `MOT:P-498`; catalog display **P‑498**; date **circa 1885**.
- Full storefront frame; materially broader than the existing 400 × 400 `IMG-0724` crop of the apparent same historical exposure.
- Repository SHA-256: `{repo_sha}`; steward attachment SHA-256: `{STEWARD_SHA256}`.
- 505 address is institutional retrospective metadata; no number is visible in the image.""",
    )

    append_once(
        "media/photos/early-main-street/README.md",
        "## IMG-0740 —",
        f"""## IMG-0740 — CCHS MOT:P-498 Harding Drug Store, 505 Main, circa 1885

`IMG-0740_circa-1885-harding-drug-store-505-main-cchs-p498.jpg` preserves the largest live public CCHS derivative recovered from the MOT:P-498 record. The steward supplied a 2048 × 1359 JPEG of the same catalog object; its exact SHA-256 is recorded in `S-211` and the photo metadata register. The full frame visibly shows the George A. Harding storefront but no readable street number. It appears to be the same underlying exposure as `IMG-0724`; both are retained because IMG-0724 is only a 400 × 400 crop attached to a different institutional object/date record. See `E-191` for retrospective-address/date cautions.""",
    )

    append_once(
        "businesses/harding-drug-store.md",
        "## CCHS MOT:P-498 full-frame storefront record",
        """## CCHS MOT:P-498 full-frame storefront record

`S-211` / `E-191` / `IMG-0740` adds the CCHS MOT:P-498 full-frame photograph cataloged **Harding Drug Store - 505 Main Street**, **circa 1885**. The photograph visibly shows the George A. Harding fascia, full display windows and doorway, but not a readable street number. CCHS's later JAH 11/2022 annotation says Harding moved to the shop north and George Young moved into this location; preserve that as retrospective institutional metadata, not as a contemporary dated transfer record.

This appears to be the same historical exposure as the older `IMG-0724` crop but is a distinct catalog object with a materially fuller frame and different date/medium metadata. The archive therefore preserves both. The pre-1906 `505` label remains retrospective-address evidence and does not prove present-building continuity.""",
    )

    append_once(
        "people/profiles/george-a-harding.md",
        "## CCHS MOT:P-498 full-frame circa-1885 catalog record",
        """## CCHS MOT:P-498 full-frame circa-1885 catalog record

CCHS MOT:P-498 (`S-211` / `E-191` / `IMG-0740`) catalogs **Harding Drug Store - 505 Main Street** at **circa 1885**. The full frame visibly bears the George A. Harding storefront fascia but no readable street number. The catalog's JAH 11/2022 note saying Harding moved north and George Young moved into this location is retained as a retrospective annotation. It does not independently date a Harding→Young succession, establish title, or prove survival of the photographed structure.""",
    )

    append_once(
        "buildings/505-main.md",
        "## CCHS MOT:P-498 full-frame Harding storefront supplement",
        """## CCHS MOT:P-498 full-frame Harding storefront supplement

`S-211` / `E-191` / `IMG-0740` preserves a materially fuller CCHS frame cataloged **Harding Drug Store - 505 Main Street**, **circa 1885**. It appears to show the same underlying exposure as the existing `IMG-0724` crop, but the separate MOT:P-498 record carries distinct date/medium metadata and a 2022 Harding→Young move annotation. The image itself shows the Harding storefront but no readable `505`; because citywide numbering is documented in 1906, this remains retrospective location metadata. No continuity to the surviving 505 building is inferred.""",
    )

    append_once(
        "timelines/505-main.md",
        "## 4 September 2026 — MOT:P-498 Harding-photo supplement",
        """## 4 September 2026 — MOT:P-498 Harding-photo supplement

The CCHS MOT:P-498 full-frame image (`S-211` / `E-191` / `IMG-0740`) is cataloged **Harding Drug Store - 505 Main Street**, **circa 1885**. It visibly shows the Harding storefront but no readable street number and appears to be the same underlying historical exposure as cropped `IMG-0724`. The separate catalog's circa-1885 date and JAH 11/2022 Harding-moved-north/Young-moved-in annotation are preserved without replacing the older CCHS 1880/1880s metadata. Treat `505` as retrospective pre-numbering location metadata and the move note as a later institutional annotation, not an exact transfer date or building-continuity proof.""",
    )

    append_once(
        "timeline.md",
        "## Circa 1885 catalog supplement — CCHS MOT:P-498 full Harding storefront",
        """## Circa 1885 catalog supplement — CCHS MOT:P-498 full Harding storefront

A second CCHS catalog object, MOT:P-498 (`S-211` / `E-191` / `IMG-0740`), preserves a full-frame version of the Harding storefront photograph and catalogs it **Harding Drug Store - 505 Main Street**, **circa 1885**. It appears to be the same underlying exposure as the older 400 × 400 `IMG-0724` crop, but the records differ in date precision/medium and are not merged. The full image visibly shows the George A. Harding storefront but no readable street number. A JAH 11/2022 catalog annotation says Harding moved north and George Young moved into this location; that later annotation is compatible with independent Young-at-505 evidence but is not a contemporary dated transfer source. The pre-1906 `505` label remains retrospective-address metadata, and no surviving-building continuity is inferred.""",
    )

    append_once(
        "evidence/source-captures/1880-1910-505-main-harding-young-photo-records.md",
        "## 4 September 2026 MOT:P-498 full-frame follow-up",
        """## 4 September 2026 MOT:P-498 full-frame follow-up

CCHS MOT:P-498 is now preserved separately as `IMG-0740` / `S-211` / `E-191`. It appears to show the same underlying Harding storefront exposure as the 400 × 400 `IMG-0724` crop but supplies the full storefront frame, a distinct catalog object, **circa 1885** dating, Photographic Paper medium metadata, and a JAH 11/2022 note that Harding moved north and George Young moved into the location. The distinct records are retained and their metadata conflict is explicit; the later note is not promoted to a contemporary transfer fact.""",
    )

    append_once(
        "indexes/id-crosswalk.md",
        "## S-211 / E-191 / IMG-0740 — CCHS MOT:P-498 Harding Drug Store",
        """## S-211 / E-191 / IMG-0740 — CCHS MOT:P-498 Harding Drug Store

- Source: `S-211` — CCHS MOT:P-498 catalog record.
- Evidence: `E-191` — circa-1885 catalog/address and direct full-frame visual content, with retrospective-address caution.
- Media: `IMG-0740` — full Harding storefront frame.
- Related entities: `BUS-007` Harding Drug Store; `P-001` George A. Harding; `B-002` 505 Main; context `BUS-067` / `P-076` George Young.
- Related prior image record: `S-148` / `E-133` / `IMG-0724` (apparent same exposure, 400 × 400 crop, distinct CCHS object and 1880/1880s metadata).
- Review: `evidence/source-captures/circa-1885-cchs-p498-harding-drug-store-505-main-photo-2026-09-04.md`.""",
    )

    append_once(
        "registers/research-log.md",
        "CCHS MOT:P-498 Harding full-frame integration",
        f"""- **4 Sep 2026 — CCHS MOT:P-498 Harding full-frame integration:** Preserved `IMG-0740` / `S-211` / `E-191`, cataloged **Harding Drug Store - 505 Main Street**, circa 1885. Full frame visually reviewed; no street number visible. Recorded steward attachment `{STEWARD_FILENAME}` ({STEWARD_WIDTH}×{STEWARD_HEIGHT}, SHA-256 `{STEWARD_SHA256}`) and recovered the largest live public CCHS derivative (SHA-256 `{repo_sha}`). Kept separate from `IMG-0724` because that record is only a 400×400 crop tied to a distinct CCHS object and 1880/1880s metadata. Preserved the JAH 11/2022 Harding→Young note as retrospective annotation, not a contemporary exact-date fact. CCHS MOT:P-498 Harding full-frame integration.""",
    )

    print(f"Integrated MOT:P-498 from {record_url}")
    print(f"Committed derivative candidate: {repo_width}x{repo_height}, {repo_bytes} bytes, sha256={repo_sha}")


if __name__ == "__main__":
    main()
