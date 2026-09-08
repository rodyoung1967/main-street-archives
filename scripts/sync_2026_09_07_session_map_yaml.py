from pathlib import Path
import re

MARKER = "<!-- 2026-09-07-session-1910-1925-structural-reconciliation -->"
YMARKER = "# 2026-09-07-session-1910-1925-structural-reconciliation"
REGISTER = Path("maps/sanborn-map-register.md")
MAP_YAML = Path("database/maps.yml")

register = REGISTER.read_text(encoding="utf-8")
pos = register.find(MARKER)
if pos < 0:
    raise SystemExit("Session map marker not found in map register")
chunk = register[pos:pos + 1800]
mid = re.search(r"## (SM-\d+) — 1911 Sanborn Sheet 16", chunk)
sid = re.search(r"- Source ID: `(S-\d+)`", chunk)
if not mid or not sid:
    raise SystemExit("Could not extract map/source IDs from registered Sheet 16 block")
SMID = mid.group(1)
SID = sid.group(1)

text = MAP_YAML.read_text(encoding="utf-8")
if re.search(rf"(?m)^\s*- id: {re.escape(SMID)}\s*$", text):
    print(f"{SMID} already present in database/maps.yml")
    raise SystemExit(0)

block = f'''\n\n{YMARKER}\n  - id: {SMID}\n    source_id: {SID}\n    title: 1911 Sanborn Sheet 16, Fifth/Main target block\n    date: November 1911\n    source_status: Canonical binary PDF committed at maps/sanborn/originals/1911-16 (5th-Main).pdf; visually verified in the project 1911-to-1925 target-frontage comparison.\n    related_buildings:\n      - B-005\n      - B-001\n      - B-002\n    notes: Correct downtown Fifth/Main sheet for the later 501/503/505 frontage. Visual comparison with 1925 Sheet 6 shows changed storefront/footprint geometry but does not date each demolition or rebuild. SM-007 / S-020 Sheet 22 is Canemah and remains geographic control only.\n'''
MAP_YAML.write_text(text.rstrip() + block, encoding="utf-8")
print(f"Synchronized {SMID} / {SID} into database/maps.yml")
