from pathlib import Path

SOURCE_REGISTER = Path('evidence/source-register.md')
DATABASE_SOURCES = Path('database/sources.yml')
CAPTURE = Path('evidence/source-captures/1912-courier-jan-19-pages-1-4-visual-review-2026-09-09.md')
RESEARCH_LOG = Path('registers/research-log.md')

source_marker = '## S-307 — Oregon City Courier, 19 January 1912, pages 1–4 visual-review batch'
db_marker = '  - id: S-307\n'

source_text = SOURCE_REGISTER.read_text(encoding='utf-8')
db_text = DATABASE_SOURCES.read_text(encoding='utf-8')

if source_marker in source_text or db_marker in db_text:
    raise SystemExit('S-307 already allocated; refusing to collide')

source_entry = r'''

## S-307 — Oregon City Courier, 19 January 1912, pages 1–4 visual-review batch
<!-- 1912 Courier Jan 19 pages 1-4 steward visual review and binary preservation — 2026-09-09 -->
Type: Primary newspaper page scans; **VISUALLY VERIFIED 4/4 PAGES** on 9 September 2026; exact archive PDF derivatives preserved.  
Publication: *Oregon City Courier*.  
Date/pages: **19 January 1912, printed pages 1–4**.  
Canonical issue: https://oregonnews.uoregon.edu/lccn/sn00063698/1912-01-19/ed-1/  
Repository originals: `newspapers/oregon-city-courier/1912-01-19-page-1.pdf`, `newspapers/oregon-city-courier/1912-01-19-page-2.pdf`, `newspapers/oregon-city-courier/1912-01-19-page-3.pdf`, `newspapers/oregon-city-courier/1912-01-19-page-4.pdf`.  
SHA-256: page 1 `47f0ee2c0e090e3ec6947831250ea06ee4fe64850382581dce5877aa96f85679`; page 2 `01e202249f48757ecada6946ca361c7d5b3cf5087d49a0778a382c4cab75af99`; page 3 `c261c85d058f2ac376fa59975ce49eea0fcbd66e8703e99908dfc2b3c4521611`; page 4 `36c385cc184da7d14070ebe3f645b4d1225e92ce03f48e39f267263839e7b07e`.  
Binary preservation commit: `975e5b03ee365278f3b8fde8567b2ffd3a2f0187`.  
Source capture: `evidence/source-captures/1912-courier-jan-19-pages-1-4-visual-review-2026-09-09.md`.  
Notes: The four project-steward re-uploads with `(1)` filename suffixes were byte-identical to the first supplied copies and therefore were not preserved as duplicate files. Complete visual screening found no defensible new 501/503/505/507/509/511 Main occupant, ownership, business-transition, or structural claim. Page 1 directly records a high-Willamette event reaching the end of Main Street and a separate Portland–Oregon City channel-dredging proposal; these are retained as non-target city/infrastructure context only. The separate 19 January page/image 8 Percy Cross / Harding Drug Store lead remains **OCR/TEXT ONLY** because page 8 is not in this four-page batch. No new `E-###` is assigned from the bounded no-hit/context result.
'''
SOURCE_REGISTER.write_text(source_text.rstrip() + source_entry + '\n', encoding='utf-8')

db_entry = r'''

  - id: S-307
    name: "Oregon City Courier, 19 January 1912, pages 1–4 visual-review batch"
    url: "https://oregonnews.uoregon.edu/lccn/sn00063698/1912-01-19/ed-1/"
    type: "Primary newspaper page scans; visually verified 4/4 pages; exact repository PDFs preserved"
    date: "1912-01-19"
    repository_file: "evidence/source-captures/1912-courier-jan-19-pages-1-4-visual-review-2026-09-09.md"
    notes: "Four steward-supplied pages were visually reviewed and exact archive PDF derivatives preserved under newspapers/oregon-city-courier/. Duplicate (1) re-uploads are byte-identical and were not duplicated. No new target-block claim; page-1 high-water and river-channel items remain non-target context. Page-8 Percy Cross / Harding Drug Store lead is still OCR/TEXT ONLY."
'''
DATABASE_SOURCES.write_text(db_text.rstrip() + db_entry + '\n', encoding='utf-8')

capture = CAPTURE.read_text(encoding='utf-8')
old_binary = "The current connector permits repository text updates but does not provide a direct local-file-to-binary-upload path. The four PDF bytes therefore are **not yet preserved in `newspapers/` by this checkpoint**. Their original filenames and SHA-256 values are retained here so later binary ingest can be verified exactly rather than guessed or silently substituted."
new_binary = "The four exact page PDFs are now preserved in `newspapers/oregon-city-courier/` as `1912-01-19-page-1.pdf` through `1912-01-19-page-4.pdf`. A one-time repository ingest downloaded the canonical Oregon Historic Newspapers derivatives and required their SHA-256 values to match the steward uploads before committing them. The verified binary-preservation commit is `975e5b03ee365278f3b8fde8567b2ffd3a2f0187`. The temporary ingest workflow was then removed."
if old_binary not in capture:
    raise SystemExit('Expected binary-ingest paragraph not found in capture')
capture = capture.replace(old_binary, new_binary)

old_table_tail = "| `Courier Jan 19, 1912 p4.pdf` | 4 | `36c385cc184da7d14070ebe3f645b4d1225e92ce03f48e39f267263839e7b07e` |\n"
new_table_tail = old_table_tail + "\nThe later uploads `Courier Jan 19, 1912 p1(1).pdf` through `p4(1).pdf` are byte-for-byte duplicates of the first four supplied files: all four SHA-256 values match exactly. They were therefore treated as duplicate aliases and not archived as second copies.\n"
if old_table_tail not in capture:
    raise SystemExit('Expected integrity table tail not found')
capture = capture.replace(old_table_tail, new_table_tail, 1)

old_cross = "No new `E-###` or `S-###` is created from this bounded review because the batch changes visual-audit coverage and adds non-target city context but does not materially alter a target building, business, person, ownership, timeline, crosswalk, open-question, or YAML/database fact."
new_cross = "No new `E-###` is created from this bounded review because it does not materially alter a target building, business, person, ownership, timeline, crosswalk, open-question, or YAML/database fact. The preserved four-page primary-source batch is indexed as `S-307` in the source register and `database/sources.yml`; that source registration records provenance and audit coverage rather than manufacturing a target-block historical event."
if old_cross not in capture:
    raise SystemExit('Expected cross-record paragraph not found')
capture = capture.replace(old_cross, new_cross)

old_next = "2. When a supported binary-ingest route is available, preserve the four supplied PDFs under `newspapers/oregon-city-courier/` and verify them against the SHA-256 values above.\n3. Continue the issue-by-issue *Courier* visual audit and target screening under the current 1912 `IN PROGRESS` status."
new_next = "2. Continue the issue-by-issue *Courier* visual audit and target screening under the current 1912 `IN PROGRESS` status.\n3. Reuse the preserved page files and `S-307` as the provenance/coverage control; do not create duplicate binaries for byte-identical steward re-uploads."
if old_next not in capture:
    raise SystemExit('Expected next-action block not found')
capture = capture.replace(old_next, new_next)
CAPTURE.write_text(capture, encoding='utf-8')

log = RESEARCH_LOG.read_text(encoding='utf-8')
log_marker = '### 2026-09-09 — 19 January 1912 Courier pages 1–4 steward batch'
if log_marker not in log:
    log_entry = r'''

### 2026-09-09 — 19 January 1912 Courier pages 1–4 steward batch
- Visually reviewed printed pages 1–4 and credited all four pages under the 1912 exhaustive audit.
- Re-upload aliases with `(1)` suffixes were byte-identical to the first supplied PDFs by SHA-256; no duplicate binaries were retained.
- Preserved exact canonical page PDFs at `newspapers/oregon-city-courier/1912-01-19-page-1.pdf` through `page-4.pdf` after hash-gated archive download; preservation commit `975e5b03ee365278f3b8fde8567b2ffd3a2f0187`.
- Registered the batch as `S-307`; no new `E-###` was created because target screening produced no defensible new 501/503/505/507/509/511 claim. Page-1 high-water and dredging items remain non-target context. Page/image 8 Percy Cross / Harding Drug Store remains OCR/TEXT ONLY and pending visual review.
'''
    RESEARCH_LOG.write_text(log.rstrip() + log_entry + '\n', encoding='utf-8')
