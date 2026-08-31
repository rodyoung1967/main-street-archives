#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


def write(rel, text):
    (ROOT / rel).write_text(text, encoding="utf-8")


def append_once(rel, marker, block):
    text = read(rel)
    if marker in text:
        return
    write(rel, text.rstrip() + "\n\n" + block.rstrip() + "\n")


def replace_once(rel, old, new):
    text = read(rel)
    if new in text:
        return
    n = text.count(old)
    if n != 1:
        raise RuntimeError(f"Expected exactly one anchor in {rel}, found {n}: {old[:120]!r}")
    write(rel, text.replace(old, new, 1))


# New primary source set: seven repeat scans beyond the already registered 1 Aug page.
append_once(
    "evidence/source-register.md",
    "## S-152 — Oregon City Enterprise, 1919 cleaner/dyer repeat advertisement set",
    '''## S-152 — Oregon City Enterprise, 1919 cleaner/dyer repeat advertisement set
Type: Primary newspaper scans; **VISUALLY VERIFIED** 31 August 2026.
Dates/pages: 18 Jul, 25 Jul, 8 Aug, 15 Aug, 22 Aug, 29 Aug, and 5 Sep 1919, each p. 7. The separately registered 1 Aug page is `S-151`.
Repository directory: `newspapers/oregon-city-enterprise/1919-cleaner-repeat-pages/`.
Integrity: `newspapers/oregon-city-enterprise/1919-cleaner-repeat-pages/SHA256SUMS.txt`.
Related evidence: `E-136`.
Repository source capture: `evidence/source-captures/1919-cleaner-repeat-visual-verification-2026-08-31.md`.
Notes: Direct visual comparison shows the unnamed cleaner/dyer classified repeated for eight consecutive weekly issues from 18 Jul through 5 Sep 1919 when the 1 Aug `S-151` page is included. Every visually inspected occurrence prints **`500 Fifth and Main streets`**, **`two doors south of new post office`**, and Phone **260**. OCR readings of `600` on 25 Jul and 5 Sep are false; the scans print `500`. No business/proprietor name is printed, and the unusual location phrase is not normalized to 500 Main or 500 Fifth.'''
)

append_once(
    "database/sources.yml",
    "  - id: S-152\n",
    '''  - id: S-152
    name: Oregon City Enterprise 1919 cleaner/dyer repeat advertisement set
    url: https://oregonnews.uoregon.edu/lccn/sn00063700/1919-07-18/ed-1/seq-7.pdf
    notes: Seven additional primary p.7 scans, 18 Jul through 5 Sep 1919, visually verified 31 Aug 2026; together with S-151 they establish eight consecutive weekly appearances of the unnamed cleaner/dyer ad. Every checked scan prints `500 Fifth and Main streets`, `two doors south of new post office`, and Phone 260. OCR `600` readings on 25 Jul and 5 Sep are incorrect. No advertiser name or address normalization is inferred. Related evidence E-136; files and hashes under newspapers/oregon-city-enterprise/1919-cleaner-repeat-pages/.'''
)

# Strengthen, rather than duplicate, E-136.
replace_once(
    "evidence/evidence-register.md",
    "Source: `S-151`.\nRepository source capture: `evidence/source-captures/1919-cleaning-dyeing-two-doors-south-new-post-office-ocr-lead.md`.",
    "Sources: `S-151`, `S-152`.\nRepository source captures: `evidence/source-captures/1919-cleaning-dyeing-two-doors-south-new-post-office-ocr-lead.md`; `evidence/source-captures/1919-cleaner-repeat-visual-verification-2026-08-31.md`."
)
replace_once(
    "evidence/evidence-register.md",
    "- Direct scan review confirms that **500** is genuinely printed; it is not an OCR artifact.\n",
    "- Direct scan review confirms that **500** is genuinely printed; it is not an OCR artifact.\n- Seven additional page-7 scans show the same classified in every weekly issue from **18 July through 5 September 1919** when the 1 August page is included: eight consecutive weekly appearances.\n- Direct visual comparison resolves OCR conflicts on **25 July** and **5 September**: both scans print **500**, not `600`. The repeated `500` is therefore stable newspaper text across the run, not a one-issue anomaly.\n"
)
replace_once(
    "evidence/evidence-register.md",
    "Confidence: **Very High** for the visible wording, date, trade, relative-location phrase and phone number; **unresolved** for normalized exact address, advertiser identity, relationship to Pantorium, and exact Post Office bay.",
    "Confidence: **Very High** for the repeated visible wording, `500` numeral, eight-week advertising run, trade, relative-location phrase and phone number; **unresolved** for normalized exact address, advertiser identity, relationship to Pantorium, and exact Post Office bay."
)

# YAML mirror of E-136.
replace_once(
    "database/evidence.yml",
    "      - Direct scan review confirms that 500 is genuinely printed and not an OCR artifact.\n",
    "      - Direct scan review confirms that 500 is genuinely printed and not an OCR artifact.\n      - Seven additional scans, together with the 1 August page, establish eight consecutive weekly appearances from 18 July through 5 September 1919.\n      - Visual comparison proves OCR readings of 600 on 25 July and 5 September are errors; both scans print 500, making the numeral stable repeated newspaper text.\n"
)
replace_once(
    "database/evidence.yml",
    "    confidence: Very High for visible wording, date, trade, relative location and phone; unresolved for exact normalized address, advertiser identity, Pantorium relationship and exact Post Office bay.\n    related_sources: [S-151]",
    "    confidence: Very High for repeated visible wording, the 500 numeral, eight-week run, trade, relative location and phone; unresolved for exact normalized address, advertiser identity, Pantorium relationship and exact Post Office bay.\n    related_sources: [S-151, S-152]"
)

# Add repeat-set result to the original visual capture.
append_once(
    "evidence/source-captures/1919-cleaning-dyeing-two-doors-south-new-post-office-ocr-lead.md",
    "## 31 August 2026 repeat-set verification",
    '''## 31 August 2026 repeat-set verification
A subsequent full-year OCR discovery pass found the same classified on page 7 in every weekly issue from **18 July through 5 September 1919**. Seven additional original PDFs were preserved and visually compared (`S-152`); together with this 1 August page (`S-151`) they form an eight-week consecutive run.

Direct visual review shows **every inspected repeat prints `500`**, including 25 July and 5 September, where OCR had incorrectly rendered `600`. The stable advertisement continues to print the same trade, **`two doors south of new post office`**, and Phone **260**. This materially strengthens the printed-number and relative-location evidence but still does not identify the advertiser or explain whether period wording `500 Fifth and Main streets` should normalize to 500 Main, 500 Fifth, or another convention.

Detailed repeat-set capture: `evidence/source-captures/1919-cleaner-repeat-visual-verification-2026-08-31.md`.'''
)

# Sharpen the construction checkpoint without changing the construction conclusion.
cp_rel = "evidence/source-captures/1919-1920-501-503-505-construction-checkpoint.md"
cp = read(cp_rel)
old = "5. **Completed visual check:** the **1 August 1919 Enterprise page 7** cleaner/dyer ad genuinely prints `500 Fifth and Main streets`, `two doors south of new post office`, and Phone 260 (`E-136` / `S-151`). Next identify Phone 260 and normalize the unusual location wording before using it as an exact storefront constraint."
new = "5. **Completed repeat-set visual check:** `S-151`/`S-152` now show the same cleaner/dyer ad in **eight consecutive weekly issues, 18 Jul–5 Sep 1919**. Every inspected scan prints `500 Fifth and Main streets`, `two doors south of new post office`, and Phone 260; OCR `600` readings on 25 Jul and 5 Sep are false. Next identify Phone 260 and normalize the unusual location wording before using it as an exact storefront constraint."
if old in cp:
    write(cp_rel, cp.replace(old, new, 1))
elif new not in cp:
    raise RuntimeError("Cleaner checkpoint anchor not found")

# Add repeat stability to the Post Office reconstruction.
post_rel = "evidence/source-captures/1918-1922-post-office-east-main-fifth-sixth-anchor.md"
post = read(post_rel)
old_post = "Spatially, this confirms that by August 1919 the relocated post-1918 office was locally described as the **new post office** and that an active cleaning/dyeing premises stood two doors south of it. If future evidence proves that the 1919 line means 500 Main and that `two doors` counts adjacent Main storefronts literally, it may help identify the exact postal bay within 504–514. Until then, the exact Post Office number remains unresolved."
new_post = old_post + " A subsequent visual review of seven repeat pages (`S-152`) establishes that the same wording ran weekly from 18 July through 5 September 1919 and that OCR `600` readings on two weeks are errors; the scans consistently print `500`."
if old_post in post:
    write(post_rel, post.replace(old_post, new_post, 1))
elif new_post not in post:
    raise RuntimeError("Post Office repeat anchor not found")

append_once(
    "registers/research-log.md",
    "### 2026-08-31 — 1919 cleaner repeat-set visually verified",
    '''### 2026-08-31 — 1919 cleaner repeat-set visually verified
- Full 1919 *Enterprise* OCR discovery checked 52 issues / 416 pages and located eight consecutive weekly appearances of the unnamed cleaner/dyer ad from 18 Jul through 5 Sep, all on p. 7.
- Preserved and directly inspected seven additional page scans under `newspapers/oregon-city-enterprise/1919-cleaner-repeat-pages/` (`S-152`), supplementing the already verified 1 Aug page (`S-151`).
- Visual comparison proves OCR `600` readings on 25 Jul and 5 Sep are errors: both pages print **500**. The stable run repeatedly gives `500 Fifth and Main streets`, `two doors south of new post office`, and Phone 260.
- Strengthened existing `E-136`; did not create a duplicate evidence identity, identify the unnamed advertiser, normalize the unusual address syntax, merge it with Pantorium, or assign the exact Post Office bay.'''
)

print("Prepared S-152 / E-136 cleaner-repeat integration")
