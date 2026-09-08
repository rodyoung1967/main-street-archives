from pathlib import Path
import hashlib
import re

MARKER = "<!-- 2026-09-07-session-1910-1925-structural-reconciliation -->"
YMARKER = "# 2026-09-07-session-1910-1925-structural-reconciliation"
CAPTURE = "evidence/source-captures/2026-09-07-1910-photo-1911-1925-geometry-steward-reconciliation.md"
SHEET16 = "maps/sanborn/originals/1911-16 (5th-Main).pdf"


def read(path):
    return Path(path).read_text(encoding="utf-8")


def write(path, content):
    Path(path).write_text(content, encoding="utf-8")


def append_once(path, marker, block):
    text = read(path)
    if marker in text:
        return False
    write(path, text.rstrip() + "\n\n" + block.rstrip() + "\n")
    return True


def insert_before_once(path, marker, anchor, block):
    text = read(path)
    if marker in text:
        return False
    if anchor not in text:
        raise SystemExit(f"Anchor not found in {path}: {anchor!r}")
    write(path, text.replace(anchor, block.rstrip() + "\n\n" + anchor, 1))
    return True


def next_yaml_id(path, prefix):
    text = read(path)
    nums = [int(x) for x in re.findall(rf"(?m)^\s*- id:\s*{re.escape(prefix)}-(\d{{3,4}})\s*$", text)]
    return max(nums, default=0) + 1


def next_map_id(path):
    text = read(path)
    nums = [int(x) for x in re.findall(r"(?m)^## SM-(\d{3,4})\b", text)]
    return max(nums, default=0) + 1


def fmt(prefix, num):
    return f"{prefix}-{num:03d}"


def add_yaml_relation(path, entity_id, key, value):
    text = read(path)
    pattern = re.compile(rf"(?ms)^  - id: {re.escape(entity_id)}\s*$.*?(?=^  - id: |\Z)")
    m = pattern.search(text)
    if not m:
        raise SystemExit(f"Entity {entity_id} not found in {path}")
    block = m.group(0)

    if re.search(rf"(?<![A-Za-z0-9-]){re.escape(value)}(?![A-Za-z0-9-])", block):
        return False

    inline = re.search(rf"(?m)^    {re.escape(key)}:\s*\[([^\]]*)\]\s*$", block)
    if inline:
        current = inline.group(1).strip()
        replacement = f"    {key}: [{current}, {value}]" if current else f"    {key}: [{value}]"
        new_block = block[:inline.start()] + replacement + block[inline.end():]
    else:
        multi = re.search(rf"(?m)^    {re.escape(key)}:\s*$", block)
        if multi:
            start = multi.end()
            tail = block[start:]
            next_key = re.search(r"(?m)^    [A-Za-z_][A-Za-z0-9_-]*:\s*", tail)
            insert_at = start + (next_key.start() if next_key else len(tail))
            before = block[:insert_at].rstrip("\n")
            after = block[insert_at:].lstrip("\n")
            new_block = before + f"\n      - {value}\n" + after
        else:
            new_block = block.rstrip() + f"\n    {key}: [{value}]\n"

    write(path, text[:m.start()] + new_block + text[m.end():])
    return True


def add_markdown_related_id(path, label, value):
    text = read(path)
    pat = re.compile(rf"(?m)^- {re.escape(label)}: (.+)$")
    m = pat.search(text)
    if not m:
        raise SystemExit(f"{label} line not found in {path}")
    if value in m.group(1):
        return False
    new_line = m.group(0) + f", `{value}`"
    write(path, text[:m.start()] + new_line + text[m.end():])
    return True


if MARKER in read("evidence/evidence-register.md"):
    print("Session reconciliation already integrated.")
    raise SystemExit(0)

if not Path(SHEET16).exists():
    raise SystemExit(f"Expected preserved map missing: {SHEET16}")

snum = next_yaml_id("database/sources.yml", "S")
enum = next_yaml_id("database/evidence.yml", "E")
smnum = next_map_id("maps/sanborn-map-register.md")
SID = fmt("S", snum)
EID = fmt("E", enum)
SMID = fmt("SM", smnum)
sha256 = hashlib.sha256(Path(SHEET16).read_bytes()).hexdigest()

capture = f'''# 1910 photograph / 1911–1925 geometry — steward reconciliation

Date preserved: **7 September 2026**  
Status: **PROJECT-STEWARD VISUAL OBSERVATION + EXISTING PRIMARY MAP/PHOTO SYNTHESIS; EXACT REPLACEMENT DATE AND 1922 STOREFRONT MODEL REMAIN UNRESOLVED.**

Related: `{SID}` / `{EID}` / `{SMID}`; existing `S-149` / `E-134` 1910 Young photograph; `S-021` 1925 Sanborn; `S-033` legacy City 505 resource synthesis; `B-002` 505 Main.

## Why this record exists

During the focused 1911–1925 physical-change research session, the project steward explicitly rejected a literal **1908 construction date for the surviving/current 505 building** based on direct visual comparison of the early frontage and the Sanborn geometry. Later parallel repository work integrated nearly all of the session's newspaper/property findings. This record preserves the remaining steward-supplied structural observation and reconciles it with the already-registered evidence instead of duplicating later IDs.

## Steward visual observation

The project steward states that:

1. the **1910 photograph** showing Young's Secondhand Store at **505 Main** depicts the **earlier/predecessor building configuration**;
2. that 1910 building is the **same earlier building appearance seen in the flood-era photographs** used in the project comparison;
3. comparison of the **correct downtown 1911 Sanborn Sheet 16** with the **1925 Sanborn Sheet 6** shows that the later 501/503/505 frontage does **not** match the earlier building width/footprint arrangement;
4. therefore **1908 cannot be the construction date of the surviving/current 505 building**.

Classification: **PROJECT-STEWARD VISUAL OBSERVATION / CROSS-SOURCE SYNTHESIS.** The observation is strong for rejecting a literal 1908 date for the surviving building, but it does not by itself date the replacement or prove which 1922 fire/rebuild footprint became modern 501, 503, or 505.

Important geometry correction already established in the repository: **Fifth Street itself is labeled 60 feet wide on both the 1911 and 1925 target sheets.** The steward's width observation concerns the **building/storefront geometry**, not a proven narrowing of Fifth Street.

## Correct 1911 target map registration

The correct downtown source is now formally registered as `{SMID}` / `{SID}`:

- Sanborn Fire Insurance Map, Oregon City, November 1911, **Sheet 16**;
- repository file: `{SHEET16}`;
- SHA-256: `{sha256}`;
- coverage: the downtown Fifth/Main target frontage including the later 501/503/505 area.

The previously registered 1911 **Sheet 22** (`SM-007` / `S-020`) is a genuine Canemah sheet and remains preserved as a geographic-control source. It must not be substituted for Sheet 16 in the downtown reconstruction.

## 1908-value handling

A commercial property-data lead surfaced during the session with a **1908** value for 505. The session did **not** recover a parcel-specific official assessor/GIS row proving what that value represented. It therefore remains an **UNVERIFIED LEAD**, not a source for construction history.

More importantly, the registered City 505 resource history already says the older **1983 c.1908 survey estimate was superseded** by later Sanborn comparison placing construction between **1911 and 1925**, perhaps around 1920 (`S-033`). The steward's photo/map comparison independently supports rejecting 1908 as the surviving-building construction date.

Do not interpret an assessor/property-data year as proof of unchanged physical fabric when photographs and fire-insurance maps show a different predecessor configuration.

## Focused-session findings already integrated elsewhere — do not duplicate

Later parallel work already preserved the following results from this research thread. They are listed here so the session is complete without creating duplicate evidence IDs:

- **1922 remains the strongest documented physical-change anchor.** The 13 July Harding→Gates/Wolf property division, 18 July fire, and 17–18 August Gates hollow-tile replacement are already canonical in `E-096`, `E-097`, `E-103` and `evidence/source-captures/1922-harding-wolf-gates-sale-and-rebuild.md`.
- The fire-adjacent **pool hall was damaged but not described as wholly destroyed**; its exact address/operator remains unproved. Leland & Little, Timms Pool Hall, and other billiards chains remain separate unless an exact-address record bridges them.
- **Leland & Little existed by February 1922**; the July fire did not create that partnership. The June roster separately names Timms Pool Hall, Walter Little, and O. H. Leland. Exact premises remain unresolved.
- **Dr. Freeze** was still advertising at **505½ Main** in June 1922 and announced a move to the Masonic Building after July 1. This is a pre-fire occupancy bracket, not construction proof.
- **Gilbert Miller** did not simply return to the burned row: he reopened at **209 Fifth** by September and later advertised at **419 Main**. Post-fire relocation means burned-business identity cannot be projected automatically onto a rebuilt footprint.
- The **Quality Restaurant / George Newton** lead was later resolved away from the tentative 503 hypothesis. `E-179` directly places Quality Restaurant at **427 Main** without proprietor; `E-180` names Newton as proprietor of the saved Quality restaurant and says it was **across the way from Oregon City Laundry**. Newton→427 remains probable, but **no recovered source places Newton's saved restaurant at 503** and no Gates model follows from that lead.

## Session-only lead retained below promotion threshold

A discovery/text reading during the session suggested that a **21 July 1922 Enterprise** account may describe the ignition room as the **vacant half of a store building**. That exact wording was not promoted into the canonical fire evidence during this reconciliation because the original page has not been preserved here as a visually verified source for that phrase.

Classification: **OCR/TEXT-ONLY / VISUAL VERIFICATION REQUIRED.** Re-check the original scan before using this wording to infer that the ignition structure contained two commercial halves or to map it to a modern storefront.

## Current structural conclusion

The defensible bracket is:

- **1910 photograph / 1911 Sheet 16:** predecessor frontage/building configuration;
- **1925 Sheet 6:** materially changed 501/503/505 storefront/footprint arrangement;
- **July–August 1922:** strongest directly documented construction/rebuild event within the bracket;
- **exact modern storefront mapping:** still unresolved.

Thus **1908 is rejected as a literal construction date for the surviving/current 505 building**, while **1911–1925** remains the stronger physical-change bracket. The evidence does not yet prove whether the surviving 505 fabric dates specifically to 1922, an earlier point after 1911, or a later alteration within the bracket.

## Propagation audit

Updated by this integration: 505 building record, Sanborn map register, source/evidence registers and YAML, map comparison, crosswalk, archive index, research log, and the existing 1911–1925 checkpoint.

No new person, business, occupancy, ownership, or dated construction event is created by the steward observation itself, so no people/business/timeline entity record is manufactured. Existing construction leads `RL-005` / `RL-024` and the 1922 model remain open.
'''

Path(CAPTURE).write_text(capture, encoding="utf-8")

source_md = f'''{MARKER}
## {SID} — Sanborn Fire Insurance Map, Oregon City, November 1911, Sheet 16 — Fifth/Main target block
Type: Primary fire-insurance map scan; **VISUALLY VERIFIED in project 1911→1925 comparison**.  
Date: November 1911.  
Sheet: **16**.  
Repository: `{SHEET16}`.  
SHA-256: `{sha256}`.  
Map ID: `{SMID}`.  
Related evidence/buildings: `{EID}`; `B-005`, `B-001`, `B-002`.  
Notes: This is the correct downtown Fifth/Main sheet for the later 501/503/505 frontage. The earlier registered 1911 Sheet 22 (`SM-007` / `S-020`) is Canemah and remains a valid geographic-control source, not the target block. Visual comparison with `S-021` / 1925 Sheet 6 shows changed storefront/footprint geometry by 1925; the map does not itself date each demolition or rebuild.
'''
append_once("evidence/source-register.md", MARKER, source_md)

source_yaml = f'''{YMARKER}
  - id: {SID}
    name: "Sanborn Fire Insurance Map, Oregon City, November 1911, Sheet 16 — Fifth/Main target block"
    url: "{SHEET16}"
    type: "Primary Sanborn fire-insurance map scan; visually verified in 1911-to-1925 comparison"
    date: "1911-11"
    repository_file: "{SHEET16}"
    notes: "Correct downtown Fifth/Main sheet for later 501/503/505 frontage. 1911 Sheet 22 is Canemah and must not be substituted. Visual comparison with 1925 Sheet 6 shows changed storefront/footprint geometry but does not date each physical change."
    related_evidence: [{EID}]
    related_buildings: [B-005, B-001, B-002]'''
append_once("database/sources.yml", YMARKER, source_yaml)

evidence_md = f'''{MARKER}
## {EID} — Steward visual comparison rejects c.1908 as surviving 505 construction date
Type: Project-steward visual observation / primary photo-and-map cross-source synthesis.  
Sources: `S-149`, `{SID}`, `S-021`, `S-033`.  
Record: `{CAPTURE}`.  
Claims:
- The 1910 CCHS Young's Secondhand Store photograph (`S-149` / `E-134`) visibly shows the **505** address in the earlier frontage.
- The project steward identifies that 1910 frontage as the same **predecessor-building appearance** seen in the project's flood-era photographs.
- The correct 1911 downtown Sanborn Sheet 16 (`{SID}` / `{SMID}`) and the 1925 Sheet 6 (`S-021`) show a materially different 501/503/505 storefront/footprint arrangement.
- Fifth Street is 60 feet wide on both target sheets; the relevant change is building/storefront geometry, not a proved street narrowing.
- Taken with the City's later survey correction (`S-033`), this is strong evidence that **c.1908 must not be used as the construction date of the surviving/current 505 building**.
- The comparison does **not** date the replacement precisely or choose between the competing 1922 Gates/Wolf storefront models.
Classification: **HIGH-CONFIDENCE PROJECT-STEWARD VISUAL SYNTHESIS for rejecting a literal 1908 surviving-building date; exact replacement date remains unresolved.**  
Confidence: Very High for the registered map-geometry change; High for the steward photograph-to-flood-era building match; none for a precise construction year beyond the 1911–1925 bracket.
'''
append_once("evidence/evidence-register.md", MARKER, evidence_md)

evidence_yaml = f'''{YMARKER}
  - id: {EID}
    name: "Steward visual comparison rejects c.1908 as surviving 505 construction date"
    type: "Project-steward visual observation and primary photo/map cross-source synthesis"
    claims:
      - "The 1910 Young's Secondhand Store photograph visibly shows 505 in the earlier frontage; the project steward identifies that frontage as the predecessor-building appearance also seen in flood-era photographs."
      - "Correct 1911 Sanborn Sheet 16 and 1925 Sheet 6 show materially different 501/503/505 storefront/footprint geometry; Fifth Street itself is 60 feet wide on both target sheets."
      - "Together with the City's later survey correction, c.1908 must not be used as the construction date of the surviving/current 505 building."
      - "The comparison does not prove an exact replacement date or select a 1922 Gates/Wolf storefront model."
    confidence: "Very High for map-geometry change; High for steward photo/flood-era visual match; exact construction year unresolved within the 1911-1925 bracket"
    related_sources: [S-149, {SID}, S-021, S-033]
    related_buildings: [B-005, B-001, B-002]
    repository_file: "{CAPTURE}"'''
append_once("database/evidence.yml", YMARKER, evidence_yaml)

map_block = f'''{MARKER}
## {SMID} — 1911 Sanborn Sheet 16, Fifth/Main target block

- Source ID: `{SID}`
- Repository file: `{SHEET16}`
- Date: November 1911
- Sheet: **16**
- Coverage: Downtown Oregon City Fifth/Main target frontage including the later 501/503/505 area.
- Use: Controlling 1911 fire-insurance-map baseline for comparing the predecessor frontage with 1925 Sheet 6. Visual comparison shows changed storefront/footprint geometry by 1925; it does not date each demolition/rebuild or map the later Gates/Wolf property line.
- Correction: `SM-007` / `S-020` Sheet 22 is Canemah and remains a geographic-control sheet only.
- Related evidence: `{EID}`.
- Archive status: `committed` — binary PDF already preserved; this integration corrects the missing register/source metadata.
'''
insert_before_once("maps/sanborn-map-register.md", MARKER, "## SM-008 — 1925 Sanborn, 5th Area", map_block)

# README inventory correction for the already-preserved binary.
readme = read("maps/sanborn/originals/README.md")
if "1911-16 (5th-Main).pdf" not in readme:
    if "1911-22 (5th).pdf" not in readme:
        raise SystemExit("README 1911-22 anchor missing")
    readme = readme.replace("1911-22 (5th).pdf", "1911-16 (5th-Main).pdf\n1911-22 (5th).pdf", 1)
    write("maps/sanborn/originals/README.md", readme)

# Add the corrected source to the map-comparison source set and preserve the steward synthesis.
comparison = read("maps/sanborn-comparison-503-505-507.md")
if f"`{SMID}` / `{SID}`" not in comparison:
    anchor = "- `SM-007` / `S-020` — 1911 sheet 22"
    if anchor not in comparison:
        raise SystemExit("Sanborn comparison source-set anchor missing")
    comparison = comparison.replace(anchor, anchor + f"\n- `{SMID}` / `{SID}` — 1911 sheet 16, corrected downtown Fifth/Main target block", 1)
    write("maps/sanborn-comparison-503-505-507.md", comparison)
append_once("maps/sanborn-comparison-503-505-507.md", MARKER, f'''{MARKER}
## Steward structural reconciliation — 7 September 2026

`{EID}` preserves the project steward's explicit visual comparison: the 1910 Young/505 photograph represents the earlier predecessor frontage also recognized in flood-era photographs, while the corrected 1911 Sheet 16 (`{SMID}` / `{SID}`) and 1925 Sheet 6 (`SM-008` / `S-021`) show materially different storefront/footprint geometry.

This strengthens the **1911–1925 physical-change bracket** and rejects a literal **c.1908 construction date for the surviving/current 505 building**. It does not assign an exact replacement year or select a 1922 Gates/Wolf storefront model. Fifth Street itself remains 60 feet wide on both target Sanborn sheets; the changed width/geometry is the commercial frontage, not a proven street narrowing.
''')

# 505 page: relate the evidence/source and preserve the steward correction next to the c.1908 discussion.
add_markdown_related_id("buildings/505-main.md", "Related evidence", EID)
add_markdown_related_id("buildings/505-main.md", "Related sources", SID)
anchor = "This is official secondary evidence that **c.1908 should not be used as the construction date of the surviving 505 building**."
text = read("buildings/505-main.md")
if MARKER not in text:
    pos = text.find(anchor)
    if pos < 0:
        raise SystemExit("505 c.1908 anchor missing")
    paragraph_end = text.find("\n\n", pos)
    if paragraph_end < 0:
        paragraph_end = pos + len(anchor)
    insert = f'''\n\n{MARKER}\n**Project-steward visual cross-check (`{EID}`):** the steward identifies the 1910 Young's Secondhand Store / 505 frontage as the same predecessor-building appearance seen in the project's flood-era photographs. The corrected 1911 Sheet 16 and 1925 Sheet 6 show materially different 501/503/505 storefront/footprint geometry. This independently reinforces the conclusion that **1908 is not the construction date of the surviving/current 505 building**. The comparison narrows the physical problem to the established **1911–1925 change window** but does not prove an exact replacement year or which July–August 1922 rebuild footprint became modern 505. The width difference concerns the building/storefront configuration; Fifth Street is mapped at 60 feet on both target sheets.''' 
    text = text[:paragraph_end] + insert + text[paragraph_end:]
    write("buildings/505-main.md", text)

add_yaml_relation("database/buildings.yml", "B-002", "related_evidence", EID)
add_yaml_relation("database/buildings.yml", "B-002", "related_sources", SID)

append_once("evidence/source-captures/1911-1925-physical-change-research-checkpoint-2026-09-02.md", MARKER, f'''{MARKER}
## 7 September 2026 reconciliation — steward visual comparison and map registration

The remaining session knowledge is now formally preserved in `{CAPTURE}` as `{EID}`. The steward explicitly identifies the 1910 505 frontage as the earlier predecessor-building appearance also seen in flood-era photographs and notes that the 1911→1925 comparison does not match the later storefront width/footprint. The correct 1911 downtown Sheet 16 binary was already preserved but is now formally registered as `{SMID}` / `{SID}`.

This reinforces the existing conclusion: **c.1908 is not a defensible construction date for the surviving/current 505 building; 1911–1925 is the stronger physical-change bracket.** It does not select a precise construction year or a Gates/Wolf storefront model. The later Newton/Quality, Freeze, pool-hall, Miller and 1922 rebuild results were already integrated elsewhere and were not duplicated.
''')

append_once("ARCHIVE_INDEX.md", MARKER, f'''{MARKER}
## 1910 photograph / 1911–1925 structural reconciliation — 7 September 2026

- [Steward photo/map reconciliation]({CAPTURE}): preserves the explicit visual rejection of a literal 1908 surviving-505 construction date, registers corrected downtown 1911 Sanborn Sheet 16 as `{SMID}` / `{SID}`, and reconciles the focused 1922 research without duplicating later integrated evidence. Related evidence: `{EID}`.
''')

append_once("indexes/id-crosswalk.md", MARKER, f'''{MARKER}
## {SMID} / {SID} / {EID} — corrected 1911 Fifth/Main map and steward structural comparison
- `{SMID}` → `{SID}` → `{SHEET16}`: correct November 1911 Sanborn Sheet 16 for the downtown Fifth/Main target frontage.
- `{EID}` → `S-149`, `{SID}`, `S-021`, `S-033` → `B-002` (also target-frontage context `B-005` / `B-001`): steward visual synthesis rejecting c.1908 as the surviving/current 505 construction date while retaining the 1911–1925 physical-change bracket.
- `SM-007` / `S-020` remains the separate Canemah Sheet 22 geographic-control source.
''')

append_once("registers/research-log.md", MARKER, f'''{MARKER}
### 2026-09-07 — reconciled focused 1911–1925 construction research and steward observation
- Re-synchronized against current `main`; later parallel commits already contained the session's verified 1922 property/fire/rebuild, Freeze 505½, pool-hall caution, Gilbert Miller relocation and Newton/Quality follow-up. Those facts were **not duplicated**.
- Preserved the project steward's explicit visual conclusion as `{EID}`: the 1910 Young/505 frontage is the earlier predecessor-building appearance also seen in flood-era photographs, while the corrected 1911→1925 map comparison shows changed storefront/footprint geometry. This rejects c.1908 as the surviving/current 505 construction date without inventing an exact replacement year.
- Formally registered the already-preserved correct downtown 1911 Sanborn Sheet 16 as `{SMID}` / `{SID}`; retained Sheet 22 as Canemah geographic control.
- Preserved two below-promotion session leads in the reconciliation capture: a commercial 1908 property-data value lacked parcel-specific official confirmation, and a 21 July 1922 "vacant half of a store building" wording remains OCR/TEXT-ONLY pending visual verification.
- Propagation audit: building, map, source/evidence registers/YAML, crosswalk, archive index and checkpoint updated. No person/business/timeline fact manufactured because this integration adds structural interpretation rather than a new dated historical event.
''')

print(f"Integrated session reconciliation as {SMID} / {SID} / {EID}")
