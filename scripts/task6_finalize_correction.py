#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent


def rd(rel): return (ROOT/rel).read_text(encoding='utf-8')
def wr(rel, text): (ROOT/rel).write_text(text, encoding='utf-8')

# Evidence register E-095: reclassify from conversion lead to direct correct-side title lead.
rel = 'evidence/evidence-register.md'
t = rd(rel)
pat = re.compile(r'(?ms)^## E-095 — OHS MSS 1503 Main/Fifth Title-Abstract Index Entry\n.*?(?=^## E-096 —)')
m = pat.search(t)
if not m: raise RuntimeError('E-095 register block not found')
new = '''## E-095 — OHS MSS 1503 Main/Fifth Title-Abstract Index Entry
Type: Official institutional archival index and collection finding aid; direct visual inspection of index page
Date: Index current as published online; visual audit 24 August 2026; underlying collection circa 1850–1997
Sources: `S-109`, `S-110`
Related record: `evidence/source-captures/ohs-mss1503-block4-lots3-4-title-abstract-lead.md`
Claims: The visually verified first page of the official OHS MSS 1503 index lists a Box 19 item at **Main St., 5th St.**, Oregon City, Clackamas County. Its Legal Address / Title field reads **Block 4, Lots 3 & 4, Oregon City**, but its separate Lot field reads **3, 4, 5**; both readings remain preserved as an unresolved internal index conflict. The ArchivesWest finding aid confirms that Series B Box 19 contains Clackamas County title abstracts and describes their potential ownership-chain/map content. **Task 6 corrects the cadastral interpretation:** original Block 4 is the odd-numbered target frontage, and the 1913 assessment independently lists G. A. Harding at Block 4 Lots 3–4. The Box 19 item is therefore a potentially direct target-property title source, not a bridge from Block 26 into a later Block 4 system. The actual abstract remains unretrieved and proves no owner chain, S. Wolf connection, 1922 transaction, improvement ownership, or exact parcel boundary until inspected.
Confidence: Very High for the visually verified index fields and official finding-aid facts; Strong as a correct-side title-chain retrieval lead after Task 6; Unresolved for the abstract's actual contents, lot scope, ownership chain and 1922 boundaries.

'''
wr(rel, t[:m.start()] + new + t[m.end():])

# Database E-095 claims, preserving relationships.
rel = 'database/evidence.yml'
y = rd(rel)
pat = re.compile(r'(?ms)^  - id: E-095\n.*?(?=^  - id: E-096\n)')
m = pat.search(y)
if not m: raise RuntimeError('E-095 YAML block not found')
b = m.group(0)
claims = '''    claims:\n      - The visually verified OHS index lists a Box 19 Oregon City item at Main and Fifth whose title says Block 4 Lots 3 & 4 and whose separate Lot field says 3, 4, 5.\n      - The conflicting title and Lot-field values are preserved; the abstract's exact lot scope remains unresolved.\n      - Task 6 establishes original Block 4 as the odd-numbered target frontage and independently places G. A. Harding at Block 4 Lots 3 and 4 in 1913.\n      - The Box 19 abstract is therefore a potentially direct target-property title source rather than a supposed Block 26-to-Block 4 conversion bridge.\n      - The actual abstract remains an open MANUAL CALLOUT and proves no S. Wolf connection, 1922 ownership, improvement ownership, exact parcel identity, or deed boundary until inspected.\n'''
b, n = re.subn(r'(?ms)^    claims:\n.*?(?=^    confidence:)', claims, b, count=1)
if n != 1: raise RuntimeError('E-095 claims replacement failed')
b = re.sub(r'(?m)^    confidence: .*$', '    confidence: Very High for index fields and finding-aid facts; Strong as a correct-side title-chain retrieval lead after Task 6; actual abstract contents and property-history conclusions unresolved.', b, count=1)
wr(rel, y[:m.start()] + b + y[m.end():])

# Address register: give 505 the same corrected cadastral context as 503.
rel = 'registers/address-register.md'
a = rd(rel)
old = '| 505 Main Street, Oregon City, Oregon | `B-002` | `buildings/505-main.md` | `BUS-005`, `BUS-006`, `BUS-009`, `BUS-010`, `BUS-016` | `E-004`, `E-005`, `E-006`, `E-008`, `E-009`, `E-010`, `E-011`, `E-012`, `E-022`, `E-029`, `E-030`, `E-035`, `E-038`, `E-046`, `E-094`, `E-095`, `E-096`, `E-097`, `E-100`, `E-101`, `E-102` | Current Rodney and Mitchell Young / 505 LLC ownership. The Wheel is at 503, not 505. 1973–1987 Brass Rail/Hansen interval: partial anchors only; see `evidence/source-captures/1973-1987-503-505-research-pass.md`. Rear/1940 hypothesis: `E-101`; footprint pass: `E-102`. |'
newrow = '| 505 Main Street, Oregon City, Oregon | `B-002` | `buildings/505-main.md` | `BUS-005`, `BUS-006`, `BUS-009`, `BUS-010`, `BUS-016` | `E-004`, `E-005`, `E-006`, `E-008`, `E-009`, `E-010`, `E-011`, `E-012`, `E-022`, `E-029`, `E-030`, `E-035`, `E-038`, `E-046`, `E-094`, `E-095`, `E-096`, `E-097`, `E-100`, `E-101`, `E-102` | Current legal-description lead: parts Lots 3 & 4, original Block 4; current Rodney and Mitchell Young / 505 LLC ownership. The Wheel is at 503, not 505. 1973–1987 Brass Rail/Hansen interval: partial anchors only. Rear/1940 hypothesis: `E-101`; footprint pass: `E-102`. |'
if old not in a: raise RuntimeError('505 address-register row not found')
wr(rel, a.replace(old, newrow, 1))

# Remove the temporary runner and script from the resulting commit.
for rel in ['scripts/task6_finalize_correction.py', '.github/workflows/task6-finalize.yml']:
    try: (ROOT/rel).unlink()
    except FileNotFoundError: pass

print('Task 6 final structured cleanup applied')
