from pathlib import Path


def append_once(path, marker, block):
    p = Path(path)
    t = p.read_text()
    if marker not in t:
        p.write_text(t.rstrip() + "\n\n" + block.strip("\n") + "\n")


def replace_once(path, old, new):
    p = Path(path)
    t = p.read_text()
    if old not in t:
        raise SystemExit(f"missing expected text in {path}: {old}")
    p.write_text(t.replace(old, new, 1))


append_once(
    "evidence/source-register.md",
    "## S-334 — Oregon City Enterprise, 5 May 1916",
    r'''
## S-334 — Oregon City Enterprise, 5 May 1916, complete issue visual review
Type: Primary newspaper page scans; **VISUALLY VERIFIED 8/8 PAGES** on 12 September 2026.  
Publication/date: *Oregon City Enterprise*, **5 May 1916**, edition 1.  
Canonical URL: https://oregonnews.uoregon.edu/lccn/sn00063700/1916-05-05/ed-1/  
Repository originals: `newspapers/oregon-city-enterprise/1916/1916-05-05/`.  
Source capture: `evidence/source-captures/1916-enterprise-may05-visual-review-2026-09-12.md`.  
Related evidence: `E-307`.  
Notes: Page 4 reports a Treasury combined building-and-site estimate of $70,000 for Oregon City and a $15,000 site estimate; the implied $55,000 building component is arithmetic, not separately printed wording. No site/address/acquisition/construction/move or target-frontage bridge is stated. No source-explicit target-premises event.

## S-335 — Oregon City Enterprise, 12 May 1916, archive-sequence visual review with page-8 anomaly
Type: Primary newspaper page scans; **ALL 8 DELIVERED ARCHIVE SCANS VISUALLY INSPECTED; 7 GENUINE WEEKLY PAGES CERTIFIED; SEQUENCE 8 WRONG-TITLE** on 12 September 2026.  
Publication/date: intended *Oregon City Enterprise*, **12 May 1916**, edition 1.  
Canonical URL: https://oregonnews.uoregon.edu/lccn/sn00063700/1916-05-12/ed-1/  
Repository originals: `newspapers/oregon-city-enterprise/1916/1916-05-12/`.  
Source capture: `evidence/source-captures/1916-enterprise-may12-visual-review-2026-09-12.md`.  
Related evidence: `E-308`.  
Notes: Sequences 1–7 visibly identify as Oregon City Enterprise. Sequence 8 visibly reads “MORNING ENTERPRISE, FRIDAY, MAY 12, 1916” and is not counted as a genuine weekly page. True weekly page 8 remains a RETRIEVAL GAP. No source-explicit target-premises event.
''',
)

append_once(
    "evidence/evidence-register.md",
    "## E-307 — 5 May 1916 Enterprise complete visual review",
    r'''
## E-307 — 5 May 1916 Enterprise complete visual review
Type: Primary newspaper visual evidence / annual issue-level coverage.  
Source: `S-334`.  
Claims: all **8/8 pages** visually inspected from original scans; page 4 gives a Treasury combined building-and-site estimate of **$70,000** for Oregon City and a **$15,000 site estimate**, yielding an arithmetic $55,000 building component consistent with the earlier federal-building proposal; the page names no Oregon City site/address and proves no acquisition, construction, move, or target-frontage connection; no page establishes a 501/503/505/505½/507 Main target-premises event; no-hit is bounded coverage only.  
Classification: **DOCUMENTED / DIRECT** for visual coverage and printed $70,000/$15,000 figures; **ARITHMETIC INFERENCE** for the $55,000 component; **COVERAGE ONLY / NO TARGET-PREMISES BRIDGE** for target frontage.  
Confidence: **Very High** for page coverage and printed figures.

## E-308 — 12 May 1916 Enterprise archive-sequence visual review and page-8 retrieval gap
Type: Primary newspaper visual evidence / annual issue-level coverage / retrieval-gap control.  
Source: `S-335`.  
Claims: all **8/8 delivered archive scans** visually inspected; sequences **1–7** visibly identify as *Oregon City Enterprise* and count as seven genuine weekly pages; sequence **8** visibly identifies as **“MORNING ENTERPRISE, FRIDAY, MAY 12, 1916”** and is not counted as genuine weekly page 8; sequences 9–14 are unavailable at the weekly issue URL; the genuine weekly page 8 remains a **RETRIEVAL GAP**; no inspected page establishes a 501/503/505/505½/507 Main target-premises event; cumulative certified Enterprise coverage is **161/426**, combined newspaper coverage **619/884**, with **265** Enterprise pages uncertified.  
Classification: **DOCUMENTED / DIRECT** for the visible title mismatch and seven genuine weekly pages; **RETRIEVAL GAP** for true weekly page 8; **COVERAGE ONLY / NO TARGET-PREMISES BRIDGE** for target frontage.  
Confidence: **Very High** for the visual title distinction and page coverage.
''',
)

append_once(
    "database/sources.yml",
    "  - id: S-334",
    r'''
  - id: S-334
    name: "Oregon City Enterprise, 5 May 1916, complete issue visual review"
    url: "https://oregonnews.uoregon.edu/lccn/sn00063700/1916-05-05/ed-1/"
    type: "Primary newspaper page scans; visually verified 8/8 pages"
    date: "1916-05-05"
    repository_file: "evidence/source-captures/1916-enterprise-may05-visual-review-2026-09-12.md"
    related_evidence: [E-307]
    notes: "Page 4 prints a $70,000 combined building-and-site estimate for Oregon City and a $15,000 site estimate; $55,000 is the arithmetic building component. No site/address/acquisition/construction/move or target-frontage bridge is stated."
  - id: S-335
    name: "Oregon City Enterprise, 12 May 1916, archive-sequence visual review with page-8 anomaly"
    url: "https://oregonnews.uoregon.edu/lccn/sn00063700/1916-05-12/ed-1/"
    type: "Primary newspaper page scans; 8 delivered scans visually inspected; 7 genuine weekly pages certified; sequence 8 wrong-title"
    date: "1916-05-12"
    repository_file: "evidence/source-captures/1916-enterprise-may12-visual-review-2026-09-12.md"
    related_evidence: [E-308]
    notes: "Sequences 1-7 visibly identify as Oregon City Enterprise. Sequence 8 visibly identifies as Morning Enterprise, Friday, May 12, 1916; true weekly page 8 remains a RETRIEVAL GAP. No source-explicit target-premises event."
''',
)

append_once(
    "database/evidence.yml",
    "  - id: E-307",
    r'''
  - id: E-307
    name: "5 May 1916 Enterprise complete visual review"
    type: "Primary newspaper visual evidence / annual issue-level coverage"
    claims:
      - "All 8/8 pages visually inspected from original scans."
      - "Page 4 prints a Treasury combined building-and-site estimate of $70,000 for Oregon City and a $15,000 site estimate; the $55,000 building component is arithmetic from those printed figures."
      - "The page identifies no Oregon City site/address and proves no acquisition, construction, move, or target-frontage connection."
      - "No page establishes a 501/503/505/505½/507 Main target-premises event; no-hit is bounded coverage only."
    confidence: "Very High"
    related_sources: [S-334]
    related_businesses: []
    related_buildings: []
    repository_file: "evidence/source-captures/1916-enterprise-may05-visual-review-2026-09-12.md"
  - id: E-308
    name: "12 May 1916 Enterprise archive-sequence visual review and page-8 retrieval gap"
    type: "Primary newspaper visual evidence / annual issue-level coverage / retrieval-gap control"
    claims:
      - "All 8/8 delivered archive scans visually inspected."
      - "Sequences 1-7 visibly identify as Oregon City Enterprise and count as seven genuine weekly pages."
      - "Sequence 8 visibly identifies as Morning Enterprise, Friday, May 12, 1916 and is not counted as genuine weekly page 8; true weekly page 8 remains a RETRIEVAL GAP."
      - "No inspected page establishes a 501/503/505/505½/507 Main target-premises event."
      - "Cumulative certified Enterprise coverage is 161/426 and combined newspaper coverage 619/884, with 265 Enterprise pages uncertified."
    confidence: "Very High"
    related_sources: [S-335]
    related_businesses: []
    related_buildings: []
    repository_file: "evidence/source-captures/1916-enterprise-may12-visual-review-2026-09-12.md"
''',
)

# Canonical year status: retain IN PROGRESS and explicitly preserve the unresolved 12 May page-8 slot.
p = Path("registers/year-status.md")
t = p.read_text()
old = "Enterprise **146/426 visually reviewed through 28 April 1916**. Combined certified newspaper coverage **604/884**; **280 Enterprise pages remain**. The next ordinary unreviewed Enterprise issue is **5 May 1916**."
new = "Enterprise **161/426 certified visually reviewed pages through 12 May 1916**; all 8 delivered 12 May scans were inspected, but archive sequence 8 is visibly *Morning Enterprise* and the genuine weekly page 8 remains a **RETRIEVAL GAP**. Combined certified newspaper coverage **619/884**; **265 Enterprise pages remain uncertified**. The immediate chronological unresolved item is **12 May 1916 genuine weekly page 8**; after that gap is resolved or formally carried forward, the next ordinary issue is **19 May 1916**."
if old not in t:
    raise SystemExit("year status changed; refusing overwrite")
t = t.replace(old, new, 1)
anchor = "`evidence/source-captures/1916-enterprise-april28-visual-review-2026-09-11.md`"
addition = anchor + "; `evidence/source-captures/1916-enterprise-may05-visual-review-2026-09-12.md`; `evidence/source-captures/1916-enterprise-may12-visual-review-2026-09-12.md`"
if "1916-enterprise-may12-visual-review-2026-09-12.md" not in t:
    if anchor not in t:
        raise SystemExit("year-status capture anchor missing")
    t = t.replace(anchor, addition, 1)
p.write_text(t)

# Annual checkpoint: update only the current canonical checkpoint/resume fields, not historical embedded old checkpoints.
p = Path("evidence/source-captures/1916-online-audit-checkpoint.md")
t = p.read_text()
replacements = [
    ("**146/426 visually reviewed through 28 April 1916**", "**161/426 certified visually reviewed pages through 12 May 1916; true 12 May weekly page 8 remains a RETRIEVAL GAP**"),
    ("**604 visually reviewed; 280 pending**", "**619 certified visually reviewed; 265 uncertified**"),
    ("- Enterprise: **146/426**", "- Enterprise: **161/426 certified weekly pages**; 12 May true weekly p8 remains a **RETRIEVAL GAP**"),
    ("- Combined: **604/884**", "- Combined: **619/884 certified**"),
    ("- Enterprise pages remaining: **280**", "- Enterprise pages remaining uncertified: **265**"),
    ("The next ordinary unreviewed *Oregon City Enterprise* issue is **5 May 1916**. Continue the Enterprise chronologically from that date unless newer parallel work on current `main` advances the ledger first. Preserve any future non-rendering or misassociated page as a precisely identified **RETRIEVAL GAP** after reasonable online recovery attempts.", "The **5 May 1916** issue is now 8/8 visually certified. For **12 May 1916**, all eight delivered archive scans were visually inspected, but only sequences 1–7 visibly belong to the weekly *Oregon City Enterprise*; sequence 8 is visibly headed *Morning Enterprise*. The immediate chronological unresolved item is therefore **12 May 1916 genuine weekly page 8**, preserved as a **RETRIEVAL GAP**. After that gap is resolved or formally carried forward under the research standard, continue with the next ordinary issue, **19 May 1916**."),
]
for old, new in replacements:
    if old not in t:
        raise SystemExit(f"checkpoint changed; missing: {old}")
    t = t.replace(old, new, 1)
anchor = "- `1916-enterprise-april28-visual-review-2026-09-11.md`\n"
if "- `1916-enterprise-may12-visual-review-2026-09-12.md`" not in t:
    if anchor not in t:
        raise SystemExit("checkpoint link anchor missing")
    t = t.replace(anchor, anchor + "- `1916-enterprise-may05-visual-review-2026-09-12.md`\n- `1916-enterprise-may12-visual-review-2026-09-12.md`\n", 1)
p.write_text(t)
