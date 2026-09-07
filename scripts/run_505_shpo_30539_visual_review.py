from pathlib import Path

SOURCE = Path("scripts/integrate_505_shpo_30539_visual_review.py")
src = SOURCE.read_text(encoding="utf-8")

# The 505 business timeline has continued to evolve in parallel. Patch the
# integration script's expected baseline rows to the current canonical wording
# without weakening the historical assertions or bypassing validation.
src = src.replace(
    'old_h = "| 1945 (City synthesis) | Harr\'s Recreation Center | `BUS-014` | `E-032` | Official secondary | Original directory page/citation still needed. |"',
    'old_h = "| 1945; directly documented Feb.–late 1948 | Harr\'s Recreation Center | `BUS-014` | `E-032`; `evidence/source-captures/1948-harrs-recreation-center-505-main.md` | Official secondary for 1945; Very High primary-text for 1948 | City inventory places Harr\'s Recreation Center in 1945. 11 Feb. 1948 Commission minutes show Harr and McDougald appearing as pool-hall operators; later-1948 liquor-license record directly names **Carl R. Harr**, **Harr\'s Recreation Center**, **505 Main Street**. Exact Farr→Harr transition remains unresolved. |"',
    1,
)
src = src.replace(
    'old_w = "| 1953 (City synthesis) | “Well\'s Recreation” | `BUS-015` | `E-032` | Official secondary | Original directory page/spelling/proprietor still needed. |"',
    'old_w = "| 1953 | \\"Well\'s Recreation\\" | `BUS-015` | `E-032` | Official secondary | Spelling to verify. |"',
    1,
)

# Keep the canonical Markdown business name identical to the YAML name. The
# quotation marks belong to source wording in notes/evidence, not to BUS-015's
# canonical entity name.
src = src.replace(
    "| BUS-015 | [“Well's Recreation”](wells-recreation.md) | 505 Main | May 2000 individual survey scan visually verifies",
    "| BUS-015 | [Well's Recreation](wells-recreation.md) | 505 Main | May 2000 individual survey scan visually verifies",
    1,
)

exec(compile(src, str(SOURCE), "exec"), {"__name__": "__main__"})
