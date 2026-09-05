from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
DATE = "5 September 2026"
CAPTURE = ROOT / "evidence/source-captures/1940-aerial-501-removal-505-depth-rereview-2026-09-05.md"


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


def write(rel, text):
    (ROOT / rel).write_text(text, encoding="utf-8")


def replace_required(rel, old, new):
    text = read(rel)
    if new in text:
        return
    if old not in text:
        raise SystemExit(f"{rel}: required text not found: {old[:120]!r}")
    write(rel, text.replace(old, new, 1))


def append_once(rel, marker, block):
    text = read(rel)
    if marker in text:
        return
    if not text.endswith("\n"):
        text += "\n"
    write(rel, text + "\n" + block.strip() + "\n")


def replace_section(rel, heading, next_heading, body):
    text = read(rel)
    pattern = re.compile(rf"(?ms)^{re.escape(heading)}\n.*?(?=^{re.escape(next_heading)}\n)")
    replacement = heading + "\n" + body.strip() + "\n\n"
    if replacement in text:
        return
    new, n = pattern.subn(replacement, text, count=1)
    if n != 1:
        raise SystemExit(f"{rel}: section {heading!r} not found uniquely")
    write(rel, new)


def update_md_evidence_entry(eid, note_marker, note):
    rel = "evidence/evidence-register.md"
    text = read(rel)
    if note_marker in text:
        return
    m = re.search(rf"(?ms)^## {re.escape(eid)}\b.*?(?=^## E-\d+\b|\Z)", text)
    if not m:
        raise SystemExit(f"{rel}: {eid} entry not found")
    entry = m.group(0).rstrip() + "\n\n" + note.strip() + "\n\n"
    write(rel, text[:m.start()] + entry + text[m.end():])


def update_yaml_evidence_claim(eid, claim_marker, claim, replacements=()):
    rel = "database/evidence.yml"
    text = read(rel)
    m = re.search(rf"(?ms)^  - id: {re.escape(eid)}\n.*?(?=^  - id: E-\d+\n|\Z)", text)
    if not m:
        raise SystemExit(f"{rel}: {eid} entry not found")
    entry = m.group(0)
    for old, new in replacements:
        entry = entry.replace(old, new)
    if claim_marker not in entry:
        anchor = "    claims:\n"
        if anchor not in entry:
            raise SystemExit(f"{rel}: {eid} claims anchor missing")
        entry = entry.replace(anchor, anchor + f"      - {claim}\n", 1)
    write(rel, text[:m.start()] + entry + text[m.end():])


capture_text = """# 1940 aerial re-review — 501 removal and 505 rear depth

Reviewed **5 September 2026** as a focused follow-up to `E-021`, `E-101`, `E-102`, `E-203`, `OQ-003`, `OQ-005`, and `RL-005`.

## Canonical evidence reviewed

The primary visual targets were the **already committed local repository images** from source `S-023`:

- `media/photos/aerials/IMG-0007_aerial_5th-main_1936.jpg`
- `media/photos/aerials/IMG-0008_aerial_5th-main_1940.jpg`
- `media/photos/aerials/IMG-0009_aerial_5th-main_1944.jpg`
- `media/photos/aerials/IMG-0010_aerial_5th-main_1955.jpg`
- `media/photos/aerials/IMG-0011_aerial_5th-main_1961.jpg`
- `media/photos/aerials/IMG-0012_aerial_5th-main_1974.jpg`

The independent CCHS `P-1293` aerial (`IMG-0750` / `S-229` / `E-203`) was used as a later-state control.

During analysis, direct ArcGIS renders of the **same Oregon City photocompare layers** were temporarily generated to remove viewer labels and align the frames at a common extent. Those renders are **not new or independent historical photographs** and are not treated as a separate evidence source; the committed `S-023` images remain canonical.

## 501 Main — removal interval narrowed

Using the established 5th/Main address mapping, the **1936** frame shows the separate 501 roof while the **1940** frame shows the mapped 501 corner footprint absent. The 1944 frame remains a later confirmation.

Therefore the defensible aerial bracket is now:

- **present in 1936** (`IMG-0007`)
- **absent by 1940** (`IMG-0008`)
- removal occurred **between the 1936 and 1940 aerial states**

Classification: **DOCUMENTED / DIRECT** for the two photographed states; **Moderate to High confidence** because the early aerial resolution is limited but the corner mapping is established. The aerial does not establish the demolition date, owner, tenant, legal cause, or whether highway work caused removal.

This supersedes the earlier project bracket **1936–1944** in `D-003` / `E-021`; the older decision remains in the decision log for audit history and is superseded by a new decision entry.

## 505 Main — deeper rear footprint visible by 1940

The frame sequence was then reviewed specifically for the rear edges of 503 and 505:

| Frame | Rear-depth reading | Confidence / limit |
| --- | --- | --- |
| 1936 (`IMG-0007`) | The 503/505 rear-edge relationship is not secure enough to call the later asymmetry. | Ambiguous; no negative inference. |
| 1940 (`IMG-0008`) | The mapped 505 roof/footprint extends materially farther rearward/westward than adjacent 503. | Moderate; direct frame-visible relative geometry. |
| 1944 (`IMG-0009`) | 501 absence is clear; early-frame quality does not improve the 505 change-date call beyond 1940. | Moderate. |
| 1955 (`IMG-0010`) | Deeper-505 relationship remains probable. | Moderate. |
| 1961 (`IMG-0011`) | Deeper 505 relative to 503 is clear. | High for relative geometry. |
| 1974 (`IMG-0012`) | Deeper 505 relative to 503 is clear. | High for relative geometry. |
| 1975 (`IMG-0750`) | Independent CCHS image clearly confirms the deeper 505 state. | High to Very High; `E-203`. |

The **earliest reviewed photocompare frame in which the deeper 505 state can be distinguished is 1940**. This materially strengthens `E-101` as a possible explanation for the official 1940 inventory date, but it does **not** prove that construction occurred in 1940. The 1936 frame's ambiguity is not evidence that the deeper rear portion did not already exist.

The exact alteration date, scope, permit, owner, builder, assessor change, and physical material break remain unresolved. Primary permit and assessor records remain the highest-value next evidence class.

## Research consequence

- `OQ-005`: removal timing narrows from **1936–1944** to **1936–1940**; removal cause remains open.
- `OQ-003` / `RL-005`: the question changes from whether 505 is historically deeper to **when and how the deeper rear portion was created**. Aerial evidence now supplies a by-1940 later-state endpoint, not a construction date.
- `E-203`: the 1975 image remains independent later-state corroboration; it no longer supplies the earliest known deep-505 endpoint.
"""
if CAPTURE.exists():
    if CAPTURE.read_text(encoding="utf-8") != capture_text:
        raise SystemExit(f"{CAPTURE}: unexpected existing content")
else:
    CAPTURE.write_text(capture_text, encoding="utf-8")

# Canonical aerial-series narrative.
replace_required(
    "evidence/aerial-5th-main-photocompare-series.md",
    "The **501 Main removal window (1936–1944)** overlaps the period of visible highway-corridor change",
    "The **501 Main removal window (1936–1940)** overlaps the period of visible highway-corridor change",
)
replace_required(
    "evidence/aerial-5th-main-photocompare-series.md",
    "| When was 501 removed? | **Between 1936 and 1944.** Present in 1936 (`IMG-0007`); absent by 1944 (`IMG-0009`). Exact year within that window not yet pinned (1940 frame may narrow further). | **Partially answered** — removal window established |",
    "| When was 501 removed? | **Between 1936 and 1940.** Present in 1936 (`IMG-0007`); absent in the 1940 frame (`IMG-0008`), with 1944 (`IMG-0009`) as later confirmation. | **Partially answered** — narrower removal interval established; exact date/cause unresolved |",
)
replace_required(
    "evidence/aerial-5th-main-photocompare-series.md",
    "**Working conclusion:** The aerial series adds **positive evidence** that **501 Main existed as a separable building through at least 1936** and was **removed by 1944**, with a related east-side footprint across from **500 Main** also gone by 1944.",
    "**Working conclusion:** The aerial series adds **positive evidence** that **501 Main existed as a separable building through at least 1936** and was **removed by the 1940 aerial**, narrowing the removal interval to **1936–1940**. The related east-side footprint across from **500 Main** is also gone by 1944.",
)
replace_required(
    "evidence/aerial-5th-main-photocompare-series.md",
    "- **503 & 505:** Remain part of the Main frontage north from the former 501 corner after 1944; finer legal/physical boundary not readable from aerials alone (`OQ-004` unchanged). **`E-101`** proposes testing whether **505's rear depth** changed between **1936 (`IMG-0007`)**, **1940 (`IMG-0008`)**, and **1944 (`IMG-0009`)** as a possible explanation for the inventory **1940** date. **`E-102`** (August 2026) preliminarily compared those frames: block-level built coverage appears denser by **1940**, but **505-specific rear-edge transcription remains open** (`RL-005`). See `evidence/source-captures/505-rear-expansion-footprint-pass-2026-08-24.md`.",
    "- **503 & 505:** Remain part of the Main frontage north from the former 501 corner. A focused **5 September 2026** re-review of the canonical local `S-023` frames now identifies **1940 (`IMG-0008`) as the earliest reviewed frame in which 505 can be distinguished as extending farther rearward/westward than 503**. The 1936 frame does not securely show the later asymmetry, but that ambiguity is not negative evidence. The deeper state remains visible in later frames and is independently confirmed by 1975 CCHS `P-1293` (`E-203`). Exact construction date/scope remains open under `OQ-003` / `RL-005`; see `evidence/source-captures/1940-aerial-501-removal-505-depth-rereview-2026-09-05.md`.",
)
replace_required(
    "evidence/aerial-5th-main-photocompare-series.md",
    "| `IMG-0008` | 1940 | Compare against 1936/1944 for narrowing 501 removal year |",
    "| `IMG-0008` | 1940 | **501 absent; first reviewed frame with distinguishable deeper 505 rear footprint relative to 503** |",
)
replace_required(
    "evidence/aerial-5th-main-photocompare-series.md",
    "- Pin exact 501 removal year between 1940 and 1944 using `IMG-0008` and any intermediate sources.",
    "- Pin the exact 501 removal date within the **1936–1940** aerial bracket using demolition/highway/property records; no intermediate aerial is presently established.",
)
replace_required(
    "evidence/aerial-5th-main-photocompare-series.md",
    "The 501 observation only corroborates the existing 1936–1944 removal bracket. The 505 observation sharpens the rear-expansion research question: determine the earliest photocompare frame in which the 505-vs-503 depth asymmetry becomes visible.",
    "The 501 observation now corroborates the **1936–1940** removal bracket established by the focused re-review. The 505 observation remains an independent later-state control; the earliest reviewed photocompare frame in which the 505-vs-503 depth asymmetry can be distinguished is now **1940**.",
)

# E-102 standalone evidence note.
replace_required(
    "evidence/E-102-505-sanborn-aerial-footprint-pass-2026-08-24.md",
    "**Aerial — preliminary only:**\n\n- Cropped **1936 → 1940 → 1944** comparison suggests **increased built coverage** in the Main/McLoughlin block by **1940**, but **does not yet isolate 505** specifically.",
    "**Aerial — 5 September 2026 address-level re-review:**\n\n- The canonical local `S-023` screenshots were re-reviewed frame by frame. Direct renders of the same city layers were used only as temporary alignment/zoom aids, not as independent evidence.\n- **1936 (`IMG-0007`)**: 501 is present; the 503/505 rear-depth relationship is too ambiguous for a secure asymmetry call.\n- **1940 (`IMG-0008`)**: 501 is absent, narrowing its removal interval to **1936–1940**; 505 can be distinguished as extending farther rearward/westward than 503.\n- **1944 (`IMG-0009`)**: confirms 501 remains absent; frame quality does not narrow the 505 construction date beyond the by-1940 state.\n- Later 1955/1961/1974 frames maintain the deeper-505 condition, independently confirmed by CCHS `P-1293` in 1975 (`E-203`).",
)
replace_required(
    "evidence/E-102-505-sanborn-aerial-footprint-pass-2026-08-24.md",
    "This pass **strengthens plausibility** that the inventory **1940** line may reflect **mid-century improvement or block reconfiguration** (including concrete-floor notation at **505** by 1950) rather than first-ever erection of the entire premises. It does **not** confirm a **505-specific rear expansion** around 1940.",
    "The re-review now establishes a stronger photographic endpoint: the **deeper 505-vs-503 rear-footprint relationship is distinguishable by the 1940 frame**. This materially strengthens the possibility that the inventory **1940** line reflects substantial improvement or rear work rather than first-ever erection of the Main-frontage premises. It still does **not** date the work to 1940; permit/assessor/physical evidence is required.",
)
replace_required(
    "evidence/E-102-505-sanborn-aerial-footprint-pass-2026-08-24.md",
    "- Moderate for **block-level aerial density change 1936→1940** — preliminary, address unresolved.\n- Unresolved for **505 rear-wall movement** and for any specific **1940** physical event.",
    "- Moderate for the address-level reading that **505 is deeper than 503 by 1940**; early aerial resolution limits exact rear-wall transcription.\n- Moderate to High for **501 present in 1936 and absent by 1940**.\n- Unresolved for the exact **date, scope, permit, owner, or builder** of any 505 rear alteration and for whether 1940 specifically marks construction.",
)
append_once(
    "evidence/E-101-505-rear-expansion-1940-date-hypothesis.md",
    "## 5 September 2026 — address-level aerial re-review",
    """## 5 September 2026 — address-level aerial re-review

A focused re-review of the canonical local `S-023` images now identifies **1940 (`IMG-0008`) as the earliest reviewed frame in which 505 can be distinguished as extending materially farther rearward/westward than 503**. The 1936 frame does not securely show the later asymmetry; that ambiguity is not evidence that the deeper portion did not exist. Later frames and independent 1975 CCHS `P-1293` (`E-203`) confirm the deeper state.

This materially strengthens the rear-expansion/remodel interpretation but does **not** prove a 1940 construction event. The same re-review narrows the separate 501 removal interval to **1936–1940**. Full method/limits: `evidence/source-captures/1940-aerial-501-removal-505-depth-rereview-2026-09-05.md`.""",
)

# Older footprint source capture: preserve original pass and add the completed follow-up.
replace_required(
    "evidence/source-captures/505-rear-expansion-footprint-pass-2026-08-24.md",
    "Status: **PARTIAL PASS — Sanborn visually verified; aerial preliminary; permits not recovered**",
    "Status: **FOLLOW-UP COMPLETE FOR AERIAL ADDRESS TRANSCRIPTION — permits/assessor records still unresolved**",
)
append_once(
    "evidence/source-captures/505-rear-expansion-footprint-pass-2026-08-24.md",
    "## 5 September 2026 address-level aerial follow-up",
    """## 5 September 2026 address-level aerial follow-up

The pending steward-verified aerial transcription in manual callout 4 has now been completed against the canonical local `S-023` frames. **501 is present in 1936 and absent in 1940**, narrowing its removal bracket to **1936–1940**. The **1940 frame is also the earliest reviewed frame in which 505 can be distinguished as deeper rearward/westward than 503**. The 1936 rear-edge relationship remains ambiguous and is not treated as evidence of absence.

This resolves the frame-transcription portion of `RL-005`, but not the construction-date question. Original permits, assessor cards, and physical material evidence remain necessary. See `evidence/source-captures/1940-aerial-501-removal-505-depth-rereview-2026-09-05.md`.""",
)

# Open questions and research lead.
replace_section(
    "evidence/open-questions.md",
    "## OQ-003 — 505 Rear Addition",
    "## OQ-004 — 503 / 505 Boundary",
    """Was the rear portion of 505 Main Street added later? If yes, when, by whom, and under what permit or assessor change?

Status: **Open, but aerial endpoint materially narrowed.** Mitch Young's recollection supports a later rear portion (`E-010`), and independent 1975 CCHS `P-1293` confirms 505 is deeper than 503 (`E-203`). A focused 5 September 2026 re-review of the canonical local `S-023` aerials (`E-102`) now identifies **1940 (`IMG-0008`) as the earliest reviewed frame in which the deeper 505 rear footprint can be distinguished**. The 1936 frame is ambiguous and is not negative evidence. Therefore the aerials establish a **by-1940 later-state endpoint**, not a construction year. Exact date, scope, owner, permit, assessor change, and physical material break remain unresolved. See `RL-005` and `evidence/source-captures/1940-aerial-501-removal-505-depth-rereview-2026-09-05.md`.""",
)
replace_section(
    "evidence/open-questions.md",
    "## OQ-005 — 501 Main Occupants, Title, and Removal",
    "## OQ-006 — Kwality / Quality Cafe Names",
    """Status: **Map and removal-window portions answered; occupant/title/removal cause remain open.** `E-020` establishes that the 1925 Sanborn maps **501 as a separate store**, alongside a 503 restaurant and 505 billiards/cigars. A focused 5 September 2026 re-review of `E-021` establishes a distinct 501 roof in **1936** and the mapped corner footprint **absent in 1940**, narrowing the removal interval from the earlier 1936–1944 bracket to **1936–1940**. `E-104` visually verifies separately named liquor-license premises at 501 in March 1912 (Joe Wilson's Palace Saloon) and October 1913 (Hunsaker & Taylor), but does not establish transfer, continuous operation, ownership, the July 1922 occupant, later tenants, exact demolition date, or why the building was removed. Highway causation remains open under `OQ-023`.""",
)
replace_section(
    "evidence/research-leads.md",
    "## RL-005 — 505 Rear Addition / Building Footprint",
    "## RL-006 — 503 / 505 Width and Boundary Relationship",
    """Compare assessor sketches, permits, tax cards, Sanborn maps, deeds, parcel maps, and physical measurements to determine when and how the rear portion of 505 became deeper than 503.

**5 September 2026 update:** the address-level aerial transcription is no longer open. Focused re-review of the canonical local `S-023` frames (`E-021` / `E-102`) identifies **1940 (`IMG-0008`) as the earliest reviewed frame in which 505 can be distinguished as extending farther rearward/westward than 503**. The 1936 frame is ambiguous and is not negative evidence. CCHS `P-1293` (`E-203`) independently confirms the deeper state in 1975. This strongly improves the later-state chronology but does **not** prove construction occurred in 1940.

Remaining priority tests: Oregon City Building Division historic permit files; Clackamas County assessor improvement cards/tax rolls, especially 1936–1941; deed/parcel history; and physical material breaks. The exact alteration date, owner, builder, permit, dimensions, and relationship to the official 1940 inventory date remain unresolved. See `evidence/source-captures/1940-aerial-501-removal-505-depth-rereview-2026-09-05.md`, `evidence/source-captures/505-rear-expansion-1940-date-hypothesis.md`, and `evidence/source-captures/505-rear-expansion-footprint-pass-2026-08-24.md`.""",
)

# Building narratives.
text = read("buildings/501-main.md")
for old, new in [
    ("By the 1944 aerial, that footprint is gone (`E-021` / `S-023`). Therefore the historic 501 structure survived at least into 1936 and was removed sometime between 1936 and 1944.",
     "A focused 5 September 2026 re-review of the 1940 frame shows that mapped corner footprint already gone (`E-021` / `S-023`). Therefore the historic 501 structure survived at least into 1936 and was removed sometime between the **1936 and 1940 aerial states**; 1944 is later confirmation."),
    ("| 1936–1944 | 501 structure removed during this interval | Moderate–High |",
     "| 1936–1940 | 501 structure removed during this interval | Moderate–High |"),
    ("Why was the 501 structure removed between 1936 and 1944?", "Why was the 501 structure removed between 1936 and 1940?"),
]:
    if old in text:
        text = text.replace(old, new, 1)
write("buildings/501-main.md", text)
append_once(
    "buildings/505-main.md",
    "## 5 September 2026 aerial rear-depth re-review",
    """## 5 September 2026 aerial rear-depth re-review

Focused address-level re-review of the canonical local aerial series (`S-023` / `E-021` / `E-102`) now identifies **1940 (`IMG-0008`) as the earliest reviewed frame in which 505 can be distinguished as extending farther rearward/westward than adjacent 503**. The 1936 frame is ambiguous; no absence inference is made. Later 1961/1974 frames and independent CCHS 1975 `P-1293` (`E-203`) confirm the deeper state.

This strengthens—but does not prove—the `E-101` interpretation that the official **1940** date may relate to substantial rear work or remodeling rather than first construction of the Main-frontage premises. Permit, assessor, deed, and physical-fabric evidence remain required to date and explain the change.""",
)

# Timelines and media navigation.
text = read("timelines/501-main.md")
text = text.replace("| 1936–1944 | Distinct 501 structure disappears between aerials. | Removal window only; cause/date unresolved. | `E-021`; `S-023` |",
                    "| 1936–1940 | Distinct 501 structure disappears between aerial states; 1940 frame shows the mapped corner footprint absent. | Removal window narrowed; exact date/cause unresolved. | `E-021`; `S-023` |")
text = text.replace("1936–1944 removal cause", "1936–1940 removal cause")
write("timelines/501-main.md", text)
text = read("timelines/505-main.md")
text = text.replace("| 1936–1950 | Aerial/Sanborn evidence retains the 503/505 Main-frontage structures while the separate 501 structure disappears by 1944. | Physical continuity context only; does not identify 505 tenant or prove unchanged fabric. | `E-021`; `S-023`; `SM-009` |",
                    "| 1936–1940 | Aerial re-review shows 501 present in 1936 and absent by 1940; 1940 is also the earliest reviewed frame with distinguishable deeper 505 rear depth relative to 503. | Direct relative-footprint state; does not date construction or prove unchanged fabric. | `E-021`; `E-102`; `S-023` |")
text = text.replace("| 1940 / date unresolved | 2009/2021 inventories assign the surviving resource 1940. Rear-addition recollection, observed 503/505 depth difference, and the 1925–1950 footprint pass raise a major-remodel/rear-expansion explanation. | Official-secondary date plus **unresolved hypothesis**; no 505-specific permit, assessor card, or rear-wall movement recovered. | `E-010`, `E-011`, `E-100`, `E-101`, `E-102`; `S-006`, `S-008`, `S-063`, `S-116` |",
                    "| 1940 / date unresolved | 2009/2021 inventories assign the surviving resource 1940; address-level aerial re-review now shows the deeper 505-vs-503 rear footprint already visible in the 1940 frame. | Official-secondary date plus strengthened **unresolved hypothesis**; aerial gives a by-1940 state, not a construction date; permit/assessor evidence still missing. | `E-010`, `E-011`, `E-100`, `E-101`, `E-102`; `S-006`, `S-008`, `S-023`, `S-063`, `S-116` |")
write("timelines/505-main.md", text)
replace_required(
    "timeline.md",
    "## 1936-1944 — 501 Main removal window\nAerial evidence establishes that a distinct **501 Main structure existed in 1936 and was removed by 1944** (`E-021`). Its exact tenant history, ownership, removal date, and relationship to McLoughlin/US99E work remain open.",
    "## 1936-1940 — 501 Main removal window\nFocused re-review of the canonical local aerial series establishes that a distinct **501 Main structure existed in 1936 and the mapped corner footprint was absent in the 1940 frame** (`E-021` / `E-102`). The exact tenant history, ownership, demolition date, and relationship to McLoughlin/US99E work remain open. The same 1940 frame is the earliest reviewed aerial in which **505 can be distinguished as deeper rearward/westward than 503**; this is a photographed state, not proof of a 1940 construction event.",
)
replace_required(
    "media/photos/aerials/README.md",
    "Oregon City photocompare aerial screenshots (`S-023`), cataloged under `E-021`. Key frames: **1936** (`IMG-0007`) — three distinct roofs at 501, 503, 505 Main; **1944** (`IMG-0009`) — 501 absent, east-side building across from 500 Main also absent (`D-003`).",
    "Oregon City photocompare aerial screenshots (`S-023`), cataloged under `E-021`. Key frames after the 5 September 2026 re-review: **1936** (`IMG-0007`) — three distinct roofs at 501, 503, 505 Main; **1940** (`IMG-0008`) — 501 absent and earliest reviewed frame with distinguishable deeper 505 rear footprint relative to 503; **1944** (`IMG-0009`) — later confirmation of 501 absence, with the east-side building across from 500 Main also absent.",
)
text = read("media/photo-metadata-register.md")
text = text.replace("removal window 1936–1944 (`D-003`, `E-021`)", "removal window narrowed to 1936–1940 by 5 September 2026 re-review (`D-011`, `E-021`, `E-102`)")
write("media/photo-metadata-register.md", text)

# 1975 capture: keep later-state value but stop calling the old bracket current.
text = read("evidence/source-captures/1975-cchs-p1293-oregon-city-aerial-503-505-501-2026-09-05.md")
text = text.replace("existing `E-021` removal bracket of 1936–1944", "newly narrowed `E-021` removal bracket of 1936–1940")
text = text.replace("existing 1936–1944 removal bracket", "newly narrowed 1936–1940 removal bracket")
write("evidence/source-captures/1975-cchs-p1293-oregon-city-aerial-503-505-501-2026-09-05.md", text)

# Human-readable evidence register updates.
update_md_evidence_entry(
    "E-021",
    "5 September 2026 re-review supersedes the earlier 1936–1944 removal bracket",
    """### 5 September 2026 re-review
Focused re-review of the canonical local `IMG-0007` / `IMG-0008` / `IMG-0009` frames **supersedes the earlier 1936–1944 removal bracket**: 501 is present in 1936 and the mapped corner footprint is absent in 1940, narrowing removal to **1936–1940**. The same re-review identifies **1940 as the earliest reviewed frame in which 505 can be distinguished as extending farther rearward/westward than 503**. The 1936 rear-edge relationship is ambiguous and is not treated as negative evidence. Exact 505 alteration date and 501 removal cause remain unresolved. Method: `evidence/source-captures/1940-aerial-501-removal-505-depth-rereview-2026-09-05.md`.""",
)
update_md_evidence_entry(
    "E-102",
    "5 September 2026 address-level follow-up",
    """### 5 September 2026 address-level follow-up
The pending aerial transcription is complete. `IMG-0008` (1940) shows the mapped 501 corner footprint absent and provides the earliest reviewed distinguishable deeper-505-vs-503 state. This strengthens the rear-remodel hypothesis but does not date construction to 1940; permits/assessor evidence remain required. See `evidence/source-captures/1940-aerial-501-removal-505-depth-rereview-2026-09-05.md`.""",
)
update_md_evidence_entry(
    "E-203",
    "5 September 2026 later same-day re-review",
    """### 5 September 2026 later same-day re-review
The 1975 CCHS image remains independent later-state corroboration, but it no longer supplies the earliest known deep-505 endpoint: focused `S-023` re-review now identifies the deeper 505 state by **1940** and narrows 501 removal to **1936–1940**. `E-203` does not date the 505 alteration itself.""",
)

# YAML sidecar synchronization.
update_yaml_evidence_claim(
    "E-021",
    "Focused 5 September 2026 re-review",
    "Focused 5 September 2026 re-review of canonical local IMG-0007/IMG-0008 narrows 501 removal to 1936-1940 and identifies 1940 as the earliest reviewed frame with distinguishable deeper 505 rear depth relative to 503; exact 505 alteration date remains unresolved.",
    replacements=(("501 Main was removed between 1936 and 1944.", "501 Main was removed between the 1936 and 1940 aerial states."),
                  ("Moderate to high for 501 existence in 1936 and removal by 1944", "Moderate to high for 501 existence in 1936 and absence by 1940")),
)
update_yaml_evidence_claim(
    "E-102",
    "5 September 2026 address-level aerial follow-up",
    "5 September 2026 address-level aerial follow-up identifies 1940 as the earliest reviewed frame with distinguishable deeper 505 rear depth relative to 503; 1936 is ambiguous and no construction date is inferred.",
)
update_yaml_evidence_claim(
    "E-203",
    "Later same-day S-023 re-review",
    "Later same-day S-023 re-review moves the earliest reviewed distinguishable deeper-505 endpoint to 1940 and narrows 501 removal to 1936-1940; this does not change P-1293's value as independent 1975 corroboration.",
    replacements=(("existing 1936-1944 removal bracket", "newly narrowed 1936-1940 removal bracket"),),
)

# Decision log: preserve D-003 but supersede its bracket explicitly.
rel = "docs/DECISIONS.md"
text = read(rel)
if "| D-011 | 2026-09-05 |" not in text:
    anchor = "\n## D-001 Operating Rules"
    row = "| D-011 | 2026-09-05 | **Supersede D-003 only as to the 501 removal bracket: 501 is present in the 1936 aerial and absent in the 1940 aerial, narrowing removal to 1936–1940. The 1940 frame is also the earliest reviewed photocompare frame in which 505 can be distinguished as deeper rearward/westward than 503.** | Focused re-review of canonical local `S-023` images; early-frame resolution warrants Moderate–High confidence for the 501 bracket and Moderate confidence for relative 505/503 depth. Neither finding proves demolition cause or a 1940 construction event. | `E-021`; `E-101`; `E-102`; `IMG-0007`; `IMG-0008`; `IMG-0009`; `E-203` |\n"
    if anchor not in text:
        raise SystemExit(f"{rel}: decision insertion anchor missing")
    text = text.replace(anchor, "\n" + row + anchor, 1)
    write(rel, text)

# Research log audit note.
append_once(
    "registers/research-log.md",
    "Integrated 1940 aerial address-level re-review",
    "| 2026-09-05 | Integrated 1940 aerial address-level re-review | Re-reviewed canonical local `S-023` frames; narrowed 501 removal from 1936–1944 to **1936–1940** and established **1940 as earliest reviewed distinguishable deeper-505-vs-503 state**. Direct same-source ArcGIS renders used only as temporary alignment aids, not independent evidence. | Exact 501 demolition cause/date and exact 505 alteration date/scope/permit/assessor change remain open. |",
)

print("Integrated 1940 aerial re-review and synchronized core records.")
