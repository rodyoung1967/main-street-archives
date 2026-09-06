from pathlib import Path

BUSINESS_TIMELINE = Path("registers/business-timeline.md")
CHECKPOINT = Path("evidence/source-captures/2026-09-05-farr-harr-closeout-checkpoint.md")

old_row = "| By 1934 context | Farr's Pool Hall | `BUS-013` | `E-033` | High official | Operating span incomplete. |"
new_row = "| 1936 photographic state; 1934 residence context | Farr's Pool Hall | `BUS-013` | `E-033`, `E-210` | Strong cross-source inference for 1936; official-secondary business identity | CCHS `P-1128` is independently dated 1936; steward mapping plus probable `FARR'S` / likely pool-related signage, combined with the City business/address evidence, strongly supports Farr's operating at 505 in 1936. The 1934 residence acquisition is not a business opening date. |"

text = BUSINESS_TIMELINE.read_text(encoding="utf-8")
if old_row in text:
    text = text.replace(old_row, new_row, 1)
elif new_row not in text:
    raise SystemExit("Expected Farr business-timeline row not found; stop rather than guess around concurrent edits.")
BUSINESS_TIMELINE.write_text(text, encoding="utf-8")

text = CHECKPOINT.read_text(encoding="utf-8")
anchor = "Current evidence remains:\n\n"
photo_bullet = "- CCHS `P-1128` is independently dated **1936**; steward mapping of the 505 storefront plus probable **FARR'S** / likely pool-related signage, combined with the City's independent Farr/505 business identification, provides a **STRONG CROSS-SOURCE INFERENCE** that Farr's Pool Hall was operating at 505 in the photographed state. This is an operating-state anchor, not an opening date.\n"
if photo_bullet not in text:
    if anchor not in text:
        raise SystemExit("Historical-status anchor missing from Farr-Harr closeout checkpoint.")
    text = text.replace(anchor, anchor + photo_bullet, 1)

old_gfo = "Genealogical Forum of Oregon lobby-sale item **TF0767 — “Clackamas Co. Directory 1947-48”** was publicly listed through at least October 2025. GFO's current shop instructions still provide a remote lobby-sales ordering/availability route.\n\nPresent physical availability must be confirmed before treating the volume as obtainable. No purchase or email was made in this pass."
new_gfo = "On **5 September 2026**, GFO's currently linked lobby-sales list was visually rechecked and still showed **TF0767 — “Clackamas Co. Directory 1947-48” — quantity 1 — $60.00**. GFO's current shop instructions still require contacting Lobby Sales to confirm actual physical availability and total cost.\n\nThe current-list row materially strengthens the acquisition route, but it is not proof that the copy remains unsold at the instant of inquiry. No purchase or email was made in this pass."
if old_gfo in text:
    text = text.replace(old_gfo, new_gfo, 1)
elif new_gfo not in text:
    raise SystemExit("Expected GFO closeout text not found; stop rather than overwrite concurrent edits.")

CHECKPOINT.write_text(text, encoding="utf-8")
print("Synchronized 1936 Farr anchor and current TF0767 status into central chronology/checkpoint.")
