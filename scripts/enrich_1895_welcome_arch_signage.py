from pathlib import Path
import re

CAPTURE = "evidence/source-captures/1895-cchs-2008-008-046-040-welcome-arch-6th-main-target-frontage-2026-09-04.md"
DUP_FILENAME = "Welcome Arch, O.C. Main St., 1895(1).jpg"
DUP_SHA = "90a533ef0c721ed65ed45d090d07ac0dcc372cba0f8d138543f96a2b7035924e"
SIGN_MARKER = "E. E. WILLIAMS"


def read(path):
    return Path(path).read_text(encoding="utf-8")


def write(path, text):
    Path(path).write_text(text, encoding="utf-8")


def insert_before(path, needle, marker, block):
    text = read(path)
    if marker in text:
        return
    pos = text.find(needle)
    if pos < 0:
        raise SystemExit(f"Missing insertion point {needle!r} in {path}")
    text = text[:pos].rstrip() + "\n\n" + block.rstrip() + "\n\n" + text[pos:].lstrip()
    write(path, text)


def append_to_md_section(path, header_re, next_header_re, marker, block):
    text = read(path)
    m = re.search(header_re, text, re.M)
    if not m:
        raise SystemExit(f"Section not found in {path}: {header_re}")
    n = re.search(next_header_re, text[m.end():], re.M)
    end = m.end() + n.start() if n else len(text)
    section = text[m.start():end]
    if marker in section:
        return
    new_section = section.rstrip() + "\n\n" + block.rstrip() + "\n"
    text = text[:m.start()] + new_section + text[end:].lstrip("\n")
    write(path, text)


def insert_yaml_claims(path, entity_id, marker, claims):
    text = read(path)
    m = re.search(rf"(?m)^  - id: {re.escape(entity_id)}\s*$", text)
    if not m:
        raise SystemExit(f"Missing YAML entity {entity_id} in {path}")
    n = re.search(r"(?m)^  - id: ", text[m.end():])
    end = m.end() + n.start() if n else len(text)
    section = text[m.start():end]
    if marker in section:
        return
    c = re.search(r"(?m)^    confidence:", section)
    if not c:
        raise SystemExit(f"Missing confidence field for {entity_id} in {path}")
    insert_at = m.start() + c.start()
    block = "".join(f"      - {claim}\n" for claim in claims)
    text = text[:insert_at] + block + text[insert_at:]
    write(path, text)


def replace_yaml_summary(path, entity_id, marker, summary):
    text = read(path)
    m = re.search(rf"(?m)^  - id: {re.escape(entity_id)}\s*$", text)
    if not m:
        raise SystemExit(f"Missing YAML timeline entity {entity_id}")
    n = re.search(r"(?m)^  - id: ", text[m.end():])
    end = m.end() + n.start() if n else len(text)
    section = text[m.start():end]
    if marker in section:
        return
    section2, count = re.subn(r"(?m)^    summary:.*$", "    summary: " + summary, section, count=1)
    if count != 1:
        raise SystemExit(f"Could not replace summary for {entity_id}")
    write(path, text[:m.start()] + section2 + text[end:])


def append_to_paragraph(path, needle, marker, sentence):
    text = read(path)
    if marker in text:
        return
    pos = text.find(needle)
    if pos < 0:
        raise SystemExit(f"Paragraph needle not found in {path}")
    end = text.find("\n\n", pos)
    if end < 0:
        end = len(text)
    text = text[:end].rstrip() + " " + sentence.strip() + text[end:]
    write(path, text)


def replace_exact(path, old, new):
    text = read(path)
    if old not in text:
        return False
    write(path, text.replace(old, new))
    return True


# Exact duplicate re-upload: preserve provenance, do not create another media ID.
signage_block = f"""## Signage re-review — 4 September 2026

A second project-steward upload, `{DUP_FILENAME}`, was checked against the originally recorded steward JPEG. It is an **exact byte-identical duplicate**: 2048 × 1285, 886,058 bytes, SHA-256 `{DUP_SHA}`. No second `IMG-####` record is created; both uploads resolve to `IMG-0744`.

Dedicated enlarged visual review of the right-background frontage adds the following sign transcription:

- the large grocery sign reads **E. E. WILLIAMS.** above **GROCERIES** and **FRUIT-FEED**;
- a separate more distant storefront sign on the same steward-identified frontage visibly contains the word **FASHION**; the surrounding wording is too indistinct to identify the full business name safely;
- the project steward clarifies that the photograph is looking **south from Sixth/Main toward Fifth Street** and that these signs are on the predecessor frontage later associated with **501/503/505 Main**.

The sign text is direct visual evidence in the 1895 photograph. The later-number mapping is not: no 501, 503 or 505 number is visible, and the archive does **not** yet assign E. E. Williams or the `FASHION` sign to one specific later numbered storefront. Individual 501-vs-503-vs-505 boundaries remain **PROBABLE / WORKING HYPOTHESIS** pending photo/Sanborn alignment."""
insert_before(CAPTURE, "## Target-frontage interpretation", SIGN_MARKER, signage_block)

# Claim-level evidence register.
evidence_block = f"""Signage re-review, 4 September 2026: enlarged visual inspection of `IMG-0744` reads **E. E. WILLIAMS. / GROCERIES / FRUIT-FEED** on the grocery sign. A separate distant sign visibly contains **FASHION**, but the rest of that business name is unresolved. The project steward places both signs on the right-background predecessor frontage later associated with 501/503/505 while looking south from Sixth/Main toward Fifth; no individual later number is assigned. A re-upload named `{DUP_FILENAME}` is byte-identical to the already tracked steward JPEG (SHA-256 `{DUP_SHA}`), so no duplicate media ID was created."""
append_to_md_section("evidence/evidence-register.md", r"^## E-195\b.*$", r"^## E-\d+\b", SIGN_MARKER, evidence_block)

insert_yaml_claims(
    "database/evidence.yml",
    "E-195",
    SIGN_MARKER,
    [
        'Direct enlarged visual re-review of IMG-0744 reads "E. E. WILLIAMS." above "GROCERIES" and "FRUIT-FEED" on a grocery sign.',
        'A separate more distant sign on the steward-identified target frontage visibly contains "FASHION"; surrounding wording and the full business identity remain unresolved.',
        'The project steward identifies the view as looking south from Sixth/Main toward Fifth and places these signs on the predecessor frontage later associated with 501/503/505; no individual later-number assignment is made.',
        f'The re-upload {DUP_FILENAME} is byte-identical to the already tracked steward JPEG (2048 x 1285; 886058 bytes; SHA-256 {DUP_SHA}); no duplicate media ID was created.',
    ],
)

# Media provenance and inventory.
media_block = f"""### 4 September 2026 signage re-review / duplicate reconciliation
- Enlarged visual transcription: **E. E. WILLIAMS. / GROCERIES / FRUIT-FEED**; a separate distant sign visibly contains **FASHION**, with fuller wording unresolved.
- Steward spatial annotation: signs are on the right-background predecessor frontage later associated with 501/503/505 in a view looking south from Sixth/Main toward Fifth; exact later storefront number remains unresolved.
- Re-upload `{DUP_FILENAME}` is an **exact byte duplicate** of the original steward upload: 2048 × 1285; 886,058 bytes; SHA-256 `{DUP_SHA}`. It is therefore retained as provenance only and does not receive a new media ID."""
append_to_md_section("media/photo-metadata-register.md", r"^## IMG-0744\b.*$", r"^## IMG-\d+\b", SIGN_MARKER, media_block)
append_to_md_section("media/photos/inventory.md", r"^### IMG-0744\b.*$", r"^### IMG-\d+\b", SIGN_MARKER, "- Signage re-review: **E. E. WILLIAMS. / GROCERIES / FRUIT-FEED** is visually readable; a separate sign contains **FASHION**, fuller wording unresolved. The `(1)` re-upload is byte-identical to the already recorded steward file, so no duplicate binary/media ID is added.")

# Address records and unified timelines: signage belongs to the shared predecessor frontage, not a numbered 1895 occupant.
shared_note = "Enlarged re-review of `IMG-0744` now directly reads **E. E. WILLIAMS. / GROCERIES / FRUIT-FEED** and separately the word **FASHION** on the steward-identified right-background predecessor frontage. This strengthens 1895 commercial-frontage evidence but does **not** assign either sign/business to later 501, 503, or 505 individually; the numbers are not visible and the exact storefront boundaries remain unresolved (`E-195`)."
for path in ["buildings/501-main.md", "buildings/503-main.md", "buildings/505-main.md"]:
    append_to_md_section(path, r"^## 1895 Welcome Arch photograph.*$", r"^## ", SIGN_MARKER, shared_note)
for path in ["timelines/501-main.md", "timelines/503-main.md", "timelines/505-main.md"]:
    append_to_md_section(path, r"^## 1895 — Welcome Arch / Sixth-Main fixed-location photo context\s*$", r"^## ", SIGN_MARKER, shared_note)

# Repair the three stale unified-timeline regressions from the previously recorded IMG-0743 orientation correction.
for address, path in [("501", "timelines/501-main.md"), ("503", "timelines/503-main.md"), ("505", "timelines/505-main.md")]:
    replace_exact(path, f"the east-side block later containing **{address} Main** is visible along the left side", f"the east-side block later containing **{address} Main** is visible along the right side")

# Sanborn/photo alignment note.
append_to_md_section(
    "maps/sanborn-comparison-503-505-507.md",
    r"^## 1895 CCHS Welcome Arch / Sixth-Main photo cross-check\s*$",
    r"^## ",
    SIGN_MARKER,
    "Dedicated sign review adds two alignment anchors on the steward-identified right-background target frontage: **E. E. WILLIAMS. / GROCERIES / FRUIT-FEED** and a separate sign containing **FASHION**. Use those sign-bearing walls together with facade widths, party walls and roof forms when matching the 1895 view to `SM-005`/`SM-006`; do not assign either sign to a later 501/503/505 number until that geometry is demonstrated (`E-195`).",
)

# Master timeline + structured T-078.
append_to_paragraph(
    "timeline.md",
    "CCHS `2008.008.046.040` (`S-215` / `E-195` / `IMG-0744` / `T-078`)",
    SIGN_MARKER,
    "Enlarged re-review directly reads **E. E. WILLIAMS. / GROCERIES / FRUIT-FEED** plus a separate sign containing **FASHION** on the steward-identified right-background predecessor frontage; exact later 501/503/505 assignment remains unresolved.",
)
replace_yaml_summary(
    "database/timeline.yml",
    "T-078",
    SIGN_MARKER,
    "CCHS Welcome Arch photograph is cataloged at Sixth/Main in 1895; project steward identifies the predecessor frontage later associated with 501/503/505 in the right background. Enlarged visual re-review reads E. E. WILLIAMS. / GROCERIES / FRUIT-FEED and a separate FASHION sign on that steward-identified frontage; individual later-number assignment remains unresolved.",
)

# Crosswalk and audit log.
append_to_md_section(
    "indexes/id-crosswalk.md",
    r"^## S-215 / E-195 / IMG-0744 / T-078\b.*$",
    r"^## ",
    SIGN_MARKER,
    "- Signage re-review: `IMG-0744` directly shows **E. E. WILLIAMS. / GROCERIES / FRUIT-FEED** and a separate sign containing **FASHION**; later 501/503/505 storefront assignment remains unresolved. The `(1)` steward re-upload is an exact byte duplicate and does not create a new ID.",
)

log_block = f"""## 4 September 2026 — IMG-0744 Welcome Arch signage re-review

- Re-reviewed the 1895 Welcome Arch image at enlarged scale.
- Directly transcribed **E. E. WILLIAMS. / GROCERIES / FRUIT-FEED**; a separate sign visibly contains **FASHION**, while its remaining wording is unresolved.
- Preserved the project-steward clarification that the view looks south from Sixth/Main toward Fifth and that the signs lie on the predecessor frontage later associated with 501/503/505; no individual later number is assigned.
- Re-upload `{DUP_FILENAME}` is byte-identical to the previously tracked steward JPEG (2048 × 1285; 886,058 bytes; SHA-256 `{DUP_SHA}`), so no duplicate media object was created.
- Also corrected stale `left side` wording that had reappeared in the three unified timelines for `IMG-0743`; the already-recorded steward correction is **RIGHT side** when looking south from Sixth toward Fifth."""
text = read("registers/research-log.md")
if "IMG-0744 Welcome Arch signage re-review" not in text:
    write("registers/research-log.md", text.rstrip() + "\n\n" + log_block + "\n")

print("Enriched E-195/IMG-0744 with 1895 signage transcription and duplicate provenance.")
