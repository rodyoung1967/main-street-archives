#!/usr/bin/env python3
"""Validate Main Street Archive ID consistency between Markdown and YAML."""

from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML is required. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parent.parent

ID_PATTERN = re.compile(
    r"\b(B-\d{3}|BUS-\d{3}|P-\d{3}|E-\d{3}|S-\d{3}|A-\d{3}|OH-\d{3}|"
    r"T-\d{3}|RL-\d{3}|OQ-\d{3}|SM-\d{3}|R-\d{3}|IMG-\d{4}|DOC-\d{4}|MAP-\d{4})\b"
)

PREFIX_FOR_ID = {
    "B": "B",
    "BUS": "BUS",
    "P": "P",
    "E": "E",
    "S": "S",
    "A": "A",
    "OH": "OH",
    "T": "T",
    "RL": "RL",
    "OQ": "OQ",
    "SM": "SM",
    "R": "R",
    "IMG": "IMG",
    "DOC": "DOC",
    "MAP": "MAP",
}

REGISTER_FILES = {
    "E": ROOT / "evidence" / "evidence-register.md",
    "P": ROOT / "people" / "people-index.md",
    "BUS": ROOT / "businesses" / "business-index.md",
    "S": ROOT / "evidence" / "source-register.md",
    "OQ": ROOT / "evidence" / "open-questions.md",
    "RL": ROOT / "evidence" / "research-leads.md",
    "OH": ROOT / "oral-history" / "oral-history-index.md",
    "SM": ROOT / "maps" / "sanborn-map-register.md",
}

MEDIA_FILES = [
    ROOT / "media" / "catalog.md",
    ROOT / "media" / "photo-metadata-register.md",
]

ARTIFACT_REGISTER = ROOT / "artifacts" / "matchbooks.md"
RECORDS_DIR = ROOT / "records"

YAML_FILES = {
    "people": ("P", ROOT / "database" / "people.yml", "people"),
    "businesses": ("BUS", ROOT / "database" / "businesses.yml", "businesses"),
    "buildings": ("B", ROOT / "database" / "buildings.yml", "buildings"),
    "evidence": ("E", ROOT / "database" / "evidence.yml", "evidence"),
    "sources": ("S", ROOT / "database" / "sources.yml", "sources"),
    "artifacts": ("A", ROOT / "database" / "artifacts.yml", "artifacts"),
    "oral-history": ("OH", ROOT / "database" / "oral-history.yml", "oral-history"),
    "timeline": ("T", ROOT / "database" / "timeline.yml", "timeline"),
    "maps": ("SM", ROOT / "database" / "maps.yml", "maps"),
}

SYNC_PAIRS = [
    ("People", "P"),
    ("Businesses", "BUS"),
    ("Buildings", "B"),
    ("Evidence", "E"),
    ("Sources", "S"),
    ("Oral history", "OH"),
    ("Maps", "SM"),
    ("Artifacts", "A"),
]

TABLE_ROW_PATTERNS = {
    "P": re.compile(r"^\| (P-\d{3}) \|", re.MULTILINE),
    "BUS": re.compile(r"^\| (BUS-\d{3}) \|", re.MULTILINE),
    "OH": re.compile(r"^\| (OH-\d{3}) \|", re.MULTILINE),
}

MEDIA_TABLE_PATTERN = re.compile(
    r"^\| (IMG-\d{4}|DOC-\d{4}|MAP-\d{4}) \|", re.MULTILINE
)
MEDIA_HEADING_PATTERN = re.compile(r"^## (IMG-\d{4}) —", re.MULTILINE)
RECORD_ID_PATTERN = re.compile(r"Record ID:\s*`(R-\d{3})`")
ARTIFACT_REGISTER_PATTERN = re.compile(r"`(A-\d{3})`")

LINK_PATTERN = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
EVIDENCE_BLOCK_PATTERN = re.compile(r"^## (E-\d{3}) —", re.MULTILINE)

SKIP_SCAN_DIRS = {".git", "scripts", ".cursor"}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def extract_heading_ids(path: Path, prefix: str) -> set[str]:
    heading = re.compile(rf"^## ({prefix}-\d{{3}})\b", re.MULTILINE)
    return set(heading.findall(read_text(path)))


def extract_register_ids(path: Path, prefix: str) -> set[str]:
    if prefix in TABLE_ROW_PATTERNS:
        return set(TABLE_ROW_PATTERNS[prefix].findall(read_text(path)))
    return extract_heading_ids(path, prefix)


def load_yaml_ids(path: Path, root_key: str) -> set[str]:
    data = yaml.safe_load(read_text(path))
    items = data.get(root_key, []) if data else []
    return {item["id"] for item in items if item.get("id")}


def load_yaml_items(path: Path, root_key: str) -> list[dict]:
    data = yaml.safe_load(read_text(path))
    return data.get(root_key, []) if data else []


def collect_all_yaml_ids() -> dict[str, set[str]]:
    result: dict[str, set[str]] = {}
    for _, (prefix, path, root_key) in YAML_FILES.items():
        if path.exists():
            result[prefix] = load_yaml_ids(path, root_key)
    return result


def collect_all_register_ids() -> dict[str, set[str]]:
    result: dict[str, set[str]] = {}
    for prefix, path in REGISTER_FILES.items():
        if path.exists():
            result[prefix] = extract_register_ids(path, prefix)
    result["B"] = {"B-001", "B-002", "B-003"}
    return result


def collect_media_ids() -> set[str]:
    ids: set[str] = set()
    for path in MEDIA_FILES:
        if not path.exists():
            continue
        text = read_text(path)
        ids.update(MEDIA_TABLE_PATTERN.findall(text))
        ids.update(MEDIA_HEADING_PATTERN.findall(text))
    return ids


def collect_record_ids() -> set[str]:
    ids: set[str] = set()
    if not RECORDS_DIR.exists():
        return ids
    for path in RECORDS_DIR.glob("*.md"):
        ids.update(RECORD_ID_PATTERN.findall(read_text(path)))
    return ids


def collect_artifact_register_ids() -> set[str]:
    if not ARTIFACT_REGISTER.exists():
        return set()
    return set(ARTIFACT_REGISTER_PATTERN.findall(read_text(ARTIFACT_REGISTER)))


def build_known_ids(
    register_ids: dict[str, set[str]],
    yaml_ids: dict[str, set[str]],
    media_ids: set[str],
    record_ids: set[str],
) -> dict[str, set[str]]:
    known: dict[str, set[str]] = {}
    for prefix in PREFIX_FOR_ID.values():
        known[prefix] = set()
    for prefix, ids in register_ids.items():
        known[prefix].update(ids)
    for prefix, ids in yaml_ids.items():
        known[prefix].update(ids)
    for media_id in media_ids:
        prefix = media_id.split("-")[0]
        known[prefix].add(media_id)
    for record_id in record_ids:
        known["R"].add(record_id)
    return known


def id_prefix(entity_id: str) -> str:
    if entity_id.startswith("BUS-"):
        return "BUS"
    return entity_id.split("-", 1)[0]


def compare_sets(
    label: str, markdown_ids: set[str], yaml_ids: set[str]
) -> tuple[list[str], list[str]]:
    missing_in_yaml = sorted(markdown_ids - yaml_ids)
    extra_in_yaml = sorted(yaml_ids - markdown_ids)
    missing_msgs = [
        f"{label}: in Markdown but missing from YAML -> {id_}" for id_ in missing_in_yaml
    ]
    extra_msgs = [
        f"{label}: in YAML but not in Markdown register -> {id_}" for id_ in extra_in_yaml
    ]
    return missing_msgs, extra_msgs


def markdown_register_for_sync(prefix: str, register_ids: dict[str, set[str]]) -> set[str]:
    if prefix == "A":
        return collect_artifact_register_ids()
    if prefix == "T":
        return set()
    return register_ids.get(prefix, set())


def find_broken_links() -> list[str]:
    errors: list[str] = []
    for md_path in ROOT.rglob("*.md"):
        if any(part in SKIP_SCAN_DIRS for part in md_path.parts):
            continue
        rel_dir = md_path.parent
        text = read_text(md_path)
        for match in LINK_PATTERN.finditer(text):
            target = match.group(1)
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            resolved = (rel_dir / target).resolve()
            if not resolved.exists():
                errors.append(f"{md_path.relative_to(ROOT)}: broken link -> {target}")
    return errors


def find_orphan_references(
    yaml_ids: dict[str, set[str]], known: dict[str, set[str]]
) -> list[str]:
    all_ids: set[str] = set()
    for ids in yaml_ids.values():
        all_ids.update(ids)
    for ids in known.values():
        all_ids.update(ids)

    errors: list[str] = []
    for _, (_, path, root_key) in YAML_FILES.items():
        if not path.exists():
            continue
        for item in load_yaml_items(path, root_key):
            entity_id = item.get("id", "?")
            for key, value in item.items():
                if key.startswith("related_") and isinstance(value, list):
                    for ref in value:
                        if ref not in all_ids:
                            errors.append(
                                f"{path.name} [{entity_id}]: orphan reference -> {ref}"
                            )
    return errors


def find_unknown_id_references(known: dict[str, set[str]]) -> list[str]:
    errors: list[str] = []
    for md_path in ROOT.rglob("*.md"):
        if any(part in SKIP_SCAN_DIRS for part in md_path.parts):
            continue
        rel = md_path.relative_to(ROOT)
        text = read_text(md_path)
        for match in ID_PATTERN.finditer(text):
            entity_id = match.group(1)
            prefix = id_prefix(entity_id)
            if entity_id not in known.get(prefix, set()):
                errors.append(f"{rel}: unknown ID reference -> {entity_id}")
    return sorted(set(errors))


def validate_evidence_register_metadata() -> list[str]:
    path = REGISTER_FILES["E"]
    text = read_text(path)
    errors: list[str] = []
    matches = list(EVIDENCE_BLOCK_PATTERN.finditer(text))
    for index, match in enumerate(matches):
        entity_id = match.group(1)
        start = match.start()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        block = text[start:end]
        if "Type:" not in block:
            errors.append(f"evidence-register.md [{entity_id}]: missing Type:")
        if "Confidence:" not in block:
            errors.append(f"evidence-register.md [{entity_id}]: missing Confidence:")
    return errors


def validate_yaml_evidence_fields() -> list[str]:
    path = YAML_FILES["evidence"][1]
    errors: list[str] = []
    for item in load_yaml_items(path, "evidence"):
        entity_id = item.get("id", "?")
        for field in ("type", "confidence", "claims"):
            value = item.get(field)
            if not value:
                errors.append(f"evidence.yml [{entity_id}]: missing or empty '{field}'")
            elif field == "claims" and not isinstance(value, list):
                errors.append(f"evidence.yml [{entity_id}]: 'claims' must be a list")
    return errors


def validate_oral_history_index_accuracy() -> list[str]:
    path = REGISTER_FILES["OH"]
    errors: list[str] = []
    for line in read_text(path).splitlines():
        if "P-011" not in line or not line.startswith("| OH-"):
            continue
        if "BUS-004" in line and "BUS-009" not in line:
            errors.append(
                "oral-history-index.md [OH-001]: P-011 must use BUS-009 / The 505 as "
                "primary related business, not BUS-004 / The Wheel alone"
            )
        if "The Wheel" in line and "BUS-009" not in line:
            errors.append(
                "oral-history-index.md [OH-001]: do not label Mitch Young testimony "
                "as The Wheel without BUS-009 / The 505 context"
            )
    return errors


def validate_structured_mitch_young_labels() -> list[str]:
    errors: list[str] = []
    wheel_primary = re.compile(
        r"owned and operated The Wheel|operated The Wheel from March 1991",
        re.IGNORECASE,
    )

    people_path = YAML_FILES["people"][1]
    for item in load_yaml_items(people_path, "people"):
        if item.get("id") != "P-011":
            continue
        notes = item.get("notes", "")
        if wheel_primary.search(notes) and "505 Main Street business" not in notes:
            errors.append(
                "people.yml [P-011]: notes must not equate Mitch Young period with "
                "The Wheel without 505 Main Street business / The 505 wording"
            )

    evidence_path = YAML_FILES["evidence"][1]
    for item in load_yaml_items(evidence_path, "evidence"):
        if item.get("id") != "E-004":
            continue
        for claim in item.get("claims", []):
            if wheel_primary.search(str(claim)) and "505 Main Street business" not in str(
                claim
            ):
                errors.append(
                    "evidence.yml [E-004]: claims must not equate Mitch testimony with "
                    "The Wheel without 505 Main Street business context"
                )

    oral_path = YAML_FILES["oral-history"][1]
    for item in load_yaml_items(oral_path, "oral-history"):
        if item.get("id") != "OH-001":
            continue
        summary = item.get("summary", "")
        if wheel_primary.search(summary) and "505 Main Street business" not in summary:
            errors.append(
                "oral-history.yml [OH-001]: summary must not equate testimony with "
                "The Wheel without 505 Main Street business context"
            )
        related = item.get("related_businesses", [])
        if "BUS-004" in related and "BUS-009" not in related:
            errors.append(
                "oral-history.yml [OH-001]: related_businesses must include BUS-009, "
                "not BUS-004 alone"
            )

    timeline_path = YAML_FILES["timeline"][1]
    for item in load_yaml_items(timeline_path, "timeline"):
        if item.get("id") != "T-007":
            continue
        summary = item.get("summary", "")
        if wheel_primary.search(summary) and "505 Main Street business" not in summary:
            errors.append(
                "timeline.yml [T-007]: summary must not equate Mitch period with "
                "The Wheel without 505 Main Street business context"
            )
        related = item.get("related_businesses", [])
        if related == ["BUS-004"]:
            errors.append(
                "timeline.yml [T-007]: related_businesses must use BUS-009, not BUS-004 alone"
            )

    return errors


def validate_media_catalog_crossrefs(known: dict[str, set[str]]) -> list[str]:
    errors: list[str] = []
    catalog = ROOT / "media" / "catalog.md"
    if not catalog.exists():
        return errors

    for line in read_text(catalog).splitlines():
        if not line.startswith("| IMG-") and not line.startswith("| DOC-") and not line.startswith("| MAP-"):
            continue
        if line.startswith("| Media ID"):
            continue
        if line.startswith("| ---"):
            continue

        media_match = MEDIA_TABLE_PATTERN.match(line)
        if not media_match:
            continue
        media_id = media_match.group(1)

        for entity_id in ID_PATTERN.findall(line):
            prefix = id_prefix(entity_id)
            if prefix in {"IMG", "DOC", "MAP"}:
                continue
            if entity_id == "Pending":
                continue
            if entity_id not in known.get(prefix, set()):
                errors.append(
                    f"media/catalog.md [{media_id}]: unknown cross-reference -> {entity_id}"
                )
    return errors


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    register_ids = collect_all_register_ids()
    yaml_ids = collect_all_yaml_ids()
    media_ids = collect_media_ids()
    record_ids = collect_record_ids()
    known = build_known_ids(register_ids, yaml_ids, media_ids, record_ids)

    print("Main Street Archive Validation")
    print("=" * 40)

    for label, prefix in SYNC_PAIRS:
        if prefix == "T":
            continue
        md_set = markdown_register_for_sync(prefix, register_ids)
        yml_set = yaml_ids.get(prefix, set())
        missing, extra = compare_sets(label, md_set, yml_set)
        errors.extend(missing)
        warnings.extend(extra)

    errors.extend(find_orphan_references(yaml_ids, known))
    errors.extend(find_broken_links())
    errors.extend(find_unknown_id_references(known))
    errors.extend(validate_evidence_register_metadata())
    errors.extend(validate_yaml_evidence_fields())
    errors.extend(validate_oral_history_index_accuracy())
    errors.extend(validate_structured_mitch_young_labels())
    errors.extend(validate_media_catalog_crossrefs(known))

    if warnings:
        print(f"\nWarnings ({len(warnings)}):")
        for msg in warnings:
            print(f"  - {msg}")

    if errors:
        print(f"\nErrors ({len(errors)}):")
        for msg in errors:
            print(f"  - {msg}")
        print("\nValidation FAILED.")
        return 1

    print("\nValidation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
