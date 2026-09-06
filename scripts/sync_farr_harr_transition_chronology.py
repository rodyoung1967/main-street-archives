from pathlib import Path

BUSINESS_TIMELINE = Path("registers/business-timeline.md")

old_row = "| By 1934 context | Farr's Pool Hall | `BUS-013` | `E-033` | High official | Operating span incomplete. |"
new_row = "| 1936 photographic state; 1934 residence context | Farr's Pool Hall | `BUS-013` | `E-033`, `E-210` | Strong cross-source inference for 1936; official-secondary business identity | CCHS `P-1128` is independently dated 1936; steward mapping plus probable `FARR'S` / likely pool-related signage, combined with the City business/address evidence, strongly supports Farr's operating at 505 in 1936. The 1934 residence acquisition is not a business opening date. |"

text = BUSINESS_TIMELINE.read_text(encoding="utf-8")
if old_row in text:
    text = text.replace(old_row, new_row, 1)
elif new_row not in text:
    raise SystemExit("Expected Farr business-timeline row not found; stop rather than guess around concurrent edits.")
BUSINESS_TIMELINE.write_text(text, encoding="utf-8")
print("Synchronized the 1936 Farr anchor into registers/business-timeline.md.")
