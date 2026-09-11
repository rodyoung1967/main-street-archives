
from pathlib import Path
import re

MARKER = "<!-- 1960-wells-sign-lock-2026-09-11 -->"
DATE = "11 September 2026"
PHOTO = "media/photos/main-street/IMG-0771_1960-5th-main-from-bluff-cchs-2008-008-049-037.jpg"
ORIGINAL_CAPTURE = "evidence/source-captures/cchs-2008-008-049-037-1960-fifth-main-bluff-photo.md"
CAPTURE = "evidence/source-captures/1960-cchs-2008-008-049-037-wells-sign-rereview-2026-09-11.md"
PUBLIC = "https://hub.catalogit.app/clackamas-county-historical-society/folder/photographs/entry/oregon-city-at-5th-and-main-from-the-bluff-1960"
CATALOG = "2008.008.049.037"
MEDIA = "IMG-0771"
BUSINESS = "BUS-015"
BUILDING = "B-002"

def rd(path):
    return Path(path).read_text(encoding="utf-8")

def wr(path, text):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")

def append_once(path, marker, block):
    text = rd(path)
    if marker in text:
        return
    wr(path, text.rstrip() + "\n\n" + block.rstrip() + "\n")

def next_id(path, prefix, width):
    vals = [int(x) for x in re.findall(rf"\b{re.escape(prefix)}-(\d+)\b", rd(path))]
    if not vals:
        raise SystemExit(f"No {prefix} IDs found in {path}")
    return f"{prefix}-{max(vals)+1:0{width}d}"

def yaml_add_list_item(path, entity_id, field, item):
    text = rd(path)
    m = re.search(rf"(?m)^  - id: {re.escape(entity_id)}\s*$", text)
    if not m:
        raise SystemExit(f"{entity_id} not found in {path}")
    n = re.search(r"(?m)^  - id: ", text[m.end():])
    end = m.end() + n.start() if n else len(text)
    section = text[m.start():end]
    if re.search(rf"(?m)^\s+- {re.escape(item)}\s*$", section):
        return
    fm = re.search(rf"(?m)^    {re.escape(field)}:\s*$", section)
    if not fm:
        inline = re.search(rf"(?m)^    {re.escape(field)}:\s*\[([^\]]*)\]\s*$", section)
        if inline:
            inside = inline.group(1).strip()
            vals = [x.strip() for x in inside.split(",") if x.strip()]
            if item in vals:
                return
            vals.append(item)
            new_line = f"    {field}: [{', '.join(vals)}]"
            abs_start = m.start() + inline.start()
            abs_end = m.start() + inline.end()
            text = text[:abs_start] + new_line + text[abs_end:]
            wr(path, text)
            return
        raise SystemExit(f"Field {field} not found for {entity_id} in {path}")
    field_start = m.start() + fm.end()
    after = text[field_start:end]
    nf = re.search(r"(?m)^    [A-Za-z0-9_]+:", after)
    insert_at = field_start + (nf.start() if nf else len(after))
    insertion = f"\n      - {item}"
    text = text[:insert_at].rstrip("\n") + insertion + "\n" + text[insert_at:].lstrip("\n")
    wr(path, text)

if Path(CAPTURE).exists() or MARKER in rd(ORIGINAL_CAPTURE):
    print("1960 WELLS sign rereview already integrated; no changes needed.")
    raise SystemExit(0)

SID = next_id("evidence/source-register.md", "S", 3)
EID = next_id("evidence/evidence-register.md", "E", 3)
TID = next_id("database/timeline.yml", "T", 3)

capture = f"""# 1960 CCHS {CATALOG} — 505 Main WELLS sign re-review

{MARKER}

Reviewed **{DATE}** from the committed CCHS photograph `{MEDIA}` / `{PHOTO}` and the project-steward supplied 2048 × 1387 copy.

Archive IDs: source `{SID}`; evidence `{EID}`; timeline `{TID}`; business `{BUSINESS}`; building `{BUILDING}`.

## Source control
- Institution: **Clackamas County Historical Society**
- Object: **{CATALOG}**
- Title: **Oregon City at 5th and Main, from the Bluff - 1960**
- Institutional date: **1960**
- Repository image: `{PHOTO}`
- Existing image capture: `{ORIGINAL_CAPTURE}`
- Public record: {PUBLIC}

## Re-review prompted by project steward

The project steward specifically proposed that the vertical sign on the **505 Main** frontage reads **WELLS**, consistent with the separately preserved 1953 historic-resource statement that a city directory listed **“Well's Recreation”** at 505 Main (`S-284` / `E-257`).

The photograph was re-examined at high enlargement rather than relying on the earlier general sign-reading pass.

## Visual result

The vertical 505-frontage sign is best read as **WELLS**.

The re-review resolves approximately **five stacked letter positions**, matching **W-E-L-L-S**. That pattern is materially more consistent with **WELLS** than the earlier tentative `TAVERN` thought, which would require six letters and does not fit the re-reviewed sign geometry.

The raw pixels remain soft enough that the photograph should not be described as a perfectly crisp letter-by-letter transcription independent of context. The project therefore distinguishes two propositions:

1. **Photographic sign reading:** **WELLS** on the 505 frontage in the exact-dated 1960 frame — accepted as the project's best visual reading, with the steward identification and enlarged re-review preserved.
2. **Business identification:** that sign represents the same **Well's Recreation** reported at 505 by the 1953 directory synthesis — **STRONG CROSS-SOURCE INFERENCE**, because the underlying 1953 directory page and a 1960 proprietor/license record have not yet been recovered.

## Chronological consequence

For project chronology, **Wells / Well's Recreation is now anchored at 505 Main in 1960** at the business-sign level.

- **1953:** official historic-resource survey says the city directory listed **“Well's Recreation”** at 505.
- **1960:** exact-dated CCHS photograph shows **WELLS** signage at 505.
- **11 November 1965:** municipal liquor-renewal evidence names **505 Tavern** at 505.

Thus the surviving public-facing evidence changes from a **WELLS** sign state in 1960 to documented **505 Tavern** by November 1965. The exact rename, sale, operator, licensee, or ownership transition remains unresolved. A retained sign could outlast a business transfer, so the photograph alone does not prove uninterrupted operation by the same proprietor from 1953 through 1960.

## Evidence classification

- **DOCUMENTED / DIRECT:** CCHS object identity and institutional date **1960**.
- **PROJECT VISUAL READING / STRONGLY SUPPORTED:** vertical **WELLS** sign on the 505 frontage after steward-led enlarged re-review.
- **STRONG CROSS-SOURCE INFERENCE:** the 1960 WELLS sign corresponds to the **Well's Recreation** business named in the 1953 directory synthesis at the same address.
- **UNRESOLVED:** proprietor/licensee identity in 1960; formal spelling/trade-name form in 1960; exact Harr→Well transition; exact Wells→505 Tavern transition; whether the sign remained after any operator change.

This supersedes the earlier blanket statement in `{ORIGINAL_CAPTURE}` that no useful 505 trade-name reading should be taken from `{MEDIA}`. That earlier limitation remains valid for other soft storefront lettering in the frame, but not for this specifically re-reviewed vertical 505 sign.
"""
wr(CAPTURE, capture)

append_once("evidence/source-register.md", f"## {SID} —", f"""## {SID} — CCHS {CATALOG}, 1960 Fifth/Main bluff photograph
{MARKER}
Type: Primary institutional historic photograph; **VISUALLY VERIFIED / RE-REVIEWED {DATE}**.
Institution: Clackamas County Historical Society.
Catalog ID: `{CATALOG}`.
Date: **1960**.
Repository image: `{PHOTO}`.
Capture: `{CAPTURE}`.
Public record: {PUBLIC}
Related evidence/media/timeline: `{EID}` / `{MEDIA}` / `{TID}`.
Related building/business: `{BUILDING}` / `{BUSINESS}`.
Notes: Project-steward prompted enlarged re-review identifies the vertical sign on the 505 Main frontage as **WELLS**. The exact-dated photograph plus the independently preserved 1953 “Well's Recreation” directory synthesis supports a strong cross-source 1960 Wells/Well's Recreation business-sign anchor. Proprietor and licensee remain unresolved.""")

append_once("evidence/evidence-register.md", f"## {EID} —", f"""## {EID} — 1960 CCHS photograph anchors WELLS signage at 505 Main
{MARKER}
Source: `{SID}`
Media: `{MEDIA}`
Type: Primary photographic evidence plus cross-source business-name inference
Claims:
- CCHS `{CATALOG}` is institutionally dated **1960** and depicts the Fifth/Main frontage.
- Project-steward prompted enlarged re-review identifies the vertical sign on the 505 Main frontage as **WELLS**, with five stacked letter positions materially more consistent with W-E-L-L-S than the earlier tentative TAVERN thought.
- Independent `S-284` / `E-257` says a 1953 city directory listed **“Well's Recreation”** at 505 Main.
- Taken together, the evidence provides a **STRONG CROSS-SOURCE INFERENCE** that Wells / Well's Recreation remained the public-facing business identity at 505 in the 1960 photographed state.
- This narrows the later name-state transition to after the 1960 WELLS photograph and by the exact 11 November 1965 505 Tavern municipal record, without proving a sale, proprietor, licensee, or uninterrupted operation.
Classification: **DOCUMENTED / DIRECT** for the 1960 photo/date; **STRONGLY SUPPORTED PROJECT VISUAL READING** for WELLS; **STRONG CROSS-SOURCE INFERENCE** for Well's Recreation at 505 in 1960.
Confidence: **High** for WELLS sign reading; **High** for the 1960 Well's Recreation identification when combined with the independent 1953 same-address source; proprietor/licensee unresolved.
Related building: `{BUILDING}`.
Related business: `{BUSINESS}`.""")

append_once("database/sources.yml", f"  - id: {SID}\n", f"""  - id: {SID}
    name: "CCHS {CATALOG}, Oregon City at 5th and Main from the Bluff, 1960"
    type: "Primary institutional historic photograph"
    date: "1960"
    url: "{PUBLIC}"
    repository_file: "{CAPTURE}"
    notes: "Exact-dated CCHS photograph. Steward-led enlarged rereview reads vertical WELLS signage on 505 Main; connect to Well's Recreation only as cross-source inference, not as proprietor/license proof."
""")

append_once("database/evidence.yml", f"  - id: {EID}\n", f"""  - id: {EID}
    name: "1960 CCHS photograph anchors WELLS signage at 505 Main"
    type: "Primary photographic evidence plus cross-source business-name inference"
    claims:
      - "CCHS {CATALOG} is institutionally dated 1960."
      - "Steward-led enlarged rereview identifies the vertical 505 Main sign as WELLS."
      - "Combined with S-284/E-257, the 1960 sign strongly supports Well's Recreation as the public-facing business identity at 505 in the photographed state."
      - "The evidence does not identify the 1960 proprietor or licensee and does not prove uninterrupted operation from 1953."
    confidence: "High for WELLS sign reading; High as a cross-source 1960 Well's Recreation business-sign anchor; proprietor/licensee unresolved."
    related_sources:
      - {SID}
      - S-284
    related_buildings:
      - {BUILDING}
    related_businesses:
      - {BUSINESS}
    related_media:
      - {MEDIA}
    repository_file: "{CAPTURE}"
""")

summary = ("Exact-dated CCHS photograph 2008.008.049.037 shows the 505 Main frontage in 1960. "
           "Project-steward prompted enlarged rereview reads the vertical sign as WELLS. "
           "Combined with the 1953 directory synthesis naming Well's Recreation at 505, this is a strong cross-source "
           "1960 Wells/Well's Recreation business-sign anchor. Proprietor/licensee and the exact transition to 505 Tavern remain unresolved.")
append_once("database/timeline.yml", f"  - id: {TID}\n", f"""  - id: {TID}
    date: "1960"
    summary: "{summary}"
    confidence: "High for WELLS sign reading; strong cross-source inference for Well's Recreation at 505 in 1960."
    related_sources:
      - {SID}
      - S-284
    related_evidence:
      - {EID}
      - E-257
    related_businesses:
      - {BUSINESS}
    related_buildings:
      - {BUILDING}
""")

yaml_add_list_item("database/buildings.yml", BUILDING, "related_evidence", EID)
yaml_add_list_item("database/buildings.yml", BUILDING, "related_sources", SID)
yaml_add_list_item("database/businesses.yml", BUSINESS, "related_evidence", EID)
yaml_add_list_item("database/businesses.yml", BUSINESS, "related_sources", SID)

dbbiz = rd("database/businesses.yml")
old_note = "    notes: City inventory reports 1953 directory; spelling to verify."
new_note = ('    notes: "City/SHPO survey reports a 1953 directory entry as Well\\'s Recreation; '
            'exact-dated 1960 CCHS photograph, on steward-led enlarged rereview, strongly supports vertical WELLS signage at 505. '
            'The underlying 1953 directory page, 1960 proprietor/licensee, and exact formal 1960 trade-name spelling remain unresolved."')
if old_note in dbbiz:
    dbbiz = dbbiz.replace(old_note, new_note, 1)
    wr("database/businesses.yml", dbbiz)

append_once("businesses/wells-recreation.md", MARKER, f"""## 1960 WELLS sign anchor
{MARKER}

CCHS `{CATALOG}` (`{SID}` / `{EID}` / `{MEDIA}` / `{TID}`) is institutionally dated **1960**. After a project-steward prompted high-enlargement re-review, the vertical sign on the **505 Main** frontage is best read as **WELLS**. The five-letter sign pattern is materially more consistent with `WELLS` than the earlier tentative `TAVERN` reading.

Combined with the visually verified 2000 SHPO form (`S-284` / `E-257`) stating that a **1953 city directory** listed **“Well's Recreation”** at 505, the archive now treats **Wells / Well's Recreation at 505 in 1960 as a STRONG CROSS-SOURCE INFERENCE and a project chronology anchor**.

This does **not** identify the 1960 proprietor or liquor licensee, prove uninterrupted operation from 1953, or establish the exact formal 1960 trade-name punctuation/spelling. The underlying 1953 directory page remains unrecovered.

The next exact later business-name anchor is **505 Tavern on 11 November 1965** (`E-029`). The Wells→505 Tavern business-name/operator transition therefore remains unresolved within the post-1960 / by-November-1965 interval.""")

append_once("buildings/505-main.md", MARKER, f"""## 1960 CCHS WELLS signage
{MARKER}

Exact-dated CCHS photograph `{CATALOG}` (`{SID}` / `{EID}` / `{MEDIA}` / `{TID}`) has been re-reviewed at high enlargement after the project steward identified the vertical 505-frontage sign as **WELLS**. The sign presents five stacked letter positions and is now accepted as the project's best visual reading.

Because the May 2000 SHPO form independently says a **1953 city directory** listed **“Well's Recreation” at 505** (`S-284` / `E-257`), the archive now uses the 1960 photograph as a **STRONG CROSS-SOURCE INFERENCE** that Wells / Well's Recreation remained the public-facing business identity at 505 in the photographed state.

This updates the chronology without merging separate relationship questions: the photograph does not identify the 1960 proprietor, tenant, building owner, liquor licensee, or exact transaction history. The next exact municipal business-name anchor is **505 Tavern on 11 November 1965** (`E-029`).""")

append_once("timelines/505-main.md", f"`{EID}`; `{SID}`; `{MEDIA}`", f"""| 1960 | Exact-dated CCHS `{CATALOG}` shows the 505 frontage; steward-led enlarged re-review reads the vertical sign as **WELLS**. Combined with the 1953 directory synthesis naming **Well's Recreation** at 505, this anchors Wells/Well's Recreation in the 1960 photographed state. | **STRONG CROSS-SOURCE INFERENCE** for the business identity; proprietor/licensee and uninterrupted operation unresolved. | `{EID}`; `{SID}`; `{MEDIA}`; `E-257`; `S-284` |""")

append_once("timeline.md", f"## {TID} — 1960 — WELLS signage at 505 Main", f"""## {TID} — 1960 — WELLS signage at 505 Main
{MARKER}

Exact-dated CCHS `{CATALOG}` (`{SID}` / `{EID}` / `{MEDIA}`) shows the Fifth/Main frontage. Project-steward prompted enlarged re-review reads the vertical 505 Main sign as **WELLS**. With the independent 1953 SHPO/directory-synthesis statement naming **Well's Recreation** at 505 (`S-284` / `E-257`), the project now treats Wells / Well's Recreation at 505 in 1960 as a **STRONG CROSS-SOURCE INFERENCE**.

This is a business-name/signage anchor, not proof of 1960 proprietor, licensee, property ownership, or uninterrupted operation from 1953. The next exact later trade-name anchor is **505 Tavern, 11 November 1965** (`E-029`).""")

append_once(ORIGINAL_CAPTURE, MARKER, f"""## 11 September 2026 sign re-review — WELLS at 505
{MARKER}

The earlier general sign-reading caution above is **superseded in part for one specific sign only**. After the project steward proposed `WELLS`, the vertical sign on the 505 Main frontage was re-examined at high enlargement. The best reading is **WELLS**, with approximately five stacked letter positions. This is materially more consistent with W-E-L-L-S than the earlier tentative TAVERN thought.

The dedicated evidence review is `{CAPTURE}` (`{SID}` / `{EID}` / `{TID}`). Combined with `S-284` / `E-257` (1953 directory synthesis: **“Well's Recreation” at 505**), the archive now carries a strong cross-source **1960 Wells / Well's Recreation** business-sign anchor. Other soft storefront lettering in this photograph remains subject to the original caution.""")

append_once("media/photo-metadata-register.md", MARKER, f"""### {MEDIA} sign re-review — 11 September 2026
{MARKER}
- Project-steward prompted enlarged review of the vertical **505 Main** sign now reads **WELLS**.
- Sign geometry: approximately five stacked letter positions, materially more consistent with `WELLS` than the earlier tentative `TAVERN` thought.
- Related source/evidence/timeline: `{SID}` / `{EID}` / `{TID}`.
- Cross-source control: `S-284` / `E-257` reports a **1953 city directory** listing **“Well's Recreation”** at 505.
- Project conclusion: **1960 Wells / Well's Recreation business-sign anchor = STRONG CROSS-SOURCE INFERENCE**. Proprietor/licensee and uninterrupted 1953–1960 operation remain unresolved.
- This supersedes only the earlier no-trade-name conclusion for this specific vertical 505 sign; other soft signs in `{MEDIA}` remain unresolved.""")

append_once("media/photos/inventory.md", MARKER, f"""#### {MEDIA} 1960 WELLS sign re-review
{MARKER}
- Enlarged steward-led rereview reads the vertical 505 Main sign as **WELLS**.
- Source/evidence/timeline: `{SID}` / `{EID}` / `{TID}`.
- With `S-284` / `E-257`, this is the project’s **1960 Wells / Well's Recreation** business-sign anchor; proprietor/licensee remains unresolved.""")

append_once("indexes/id-crosswalk.md", f"`{MEDIA}` CCHS `{CATALOG}` | `{SID}`, `{EID}`, `{TID}`", f"""| `{MEDIA}` CCHS `{CATALOG}` | `{SID}`, `{EID}`, `{TID}`, `{BUSINESS}`, `{BUILDING}` | Exact-dated 1960 Fifth/Main bluff photograph; steward-led enlarged re-review reads vertical 505 sign as **WELLS**. Combined with `S-284`/`E-257`, strong cross-source 1960 Well's Recreation anchor; proprietor/licensee unresolved. |""")

append_once("evidence/open-questions.md", MARKER, f"""### 11 September 2026 — Wells→505 Tavern transition narrowed by exact-dated 1960 photograph
{MARKER}

CCHS `{CATALOG}` (`{SID}` / `{EID}` / `{MEDIA}`) is exact-dated **1960**. Steward-led enlarged re-review reads the vertical 505 Main sign as **WELLS**. Combined with the independently preserved 1953 **“Well's Recreation”** directory synthesis (`S-284` / `E-257`), the project now anchors Wells / Well's Recreation at 505 in the 1960 photographed state.

The unresolved question is therefore narrower: **who operated/licensed 505 in 1960, and when/how did the public/business identity change from Wells / Well's Recreation to 505 Tavern by the exact 11 November 1965 municipal record (`E-029`)?** Do not infer the proprietor, a sale, or uninterrupted 1953–1960 operation from the sign alone.""")

append_once("evidence/research-leads.md", MARKER, f"""### 11 September 2026 — 1960 WELLS photograph refines the mid-century 505 search
{MARKER}

New exact-dated photographic evidence (`{SID}` / `{EID}` / `{MEDIA}`) now places **WELLS signage at 505 Main in 1960**, strongly linking the photographed state to the 1953 **“Well's Recreation”** directory synthesis (`S-284` / `E-257`).

Research priority shifts from asking whether Well's survived into the early 1960s to identifying **who the 1960 proprietor/licensee was and the exact post-1960 transition to 505 Tavern by 11 November 1965**. Highest-value sources remain the actual 1960 Oregon City directory, 1959–64 assumed-business-name volumes, permanent OLCC Commission records, and targeted 1960–65 local newspaper/microfilm. Preserve spelling variants `Well's / Wells / Well / Welle / Welsh`; the photo sign itself reads **WELLS** without establishing punctuation.""")

append_once("MANUAL-FOLLOWUP.md", MARKER, f"""## 11 September 2026 — MF-058 refined by 1960 WELLS photographic anchor
{MARKER}

CCHS `{CATALOG}` (`{SID}` / `{EID}` / `{MEDIA}`) is exact-dated **1960** and, after steward-led enlarged re-review, shows **WELLS** signage on the 505 Main frontage. With `S-284` / `E-257`, this strongly anchors Wells / Well's Recreation in the 1960 photographed state.

`MF-058` remains active, but its question is now narrower: identify the **1960 proprietor/licensee** and the **post-1960 transition to 505 Tavern by 11 November 1965**. The actual 1960 directory and 1959–64 assumed-name volumes become especially high-value. No outreach or fee is authorized by this update.""")

append_once("registers/research-log.md", MARKER, f"""### 2026-09-11 — 1960 WELLS sign re-review at 505 Main
{MARKER}
- Re-reviewed committed CCHS `{CATALOG}` / `{MEDIA}` after project-steward identification of the vertical 505 sign as **WELLS**.
- Enlarged review resolves approximately five stacked letter positions and accepts **WELLS** as the project's best visual reading, superseding the earlier tentative TAVERN thought for this sign.
- Integrated `{SID}` / `{EID}` / `{TID}` and linked `{BUSINESS}` / `{BUILDING}`.
- Combined with `S-284` / `E-257`, the archive now treats **Wells / Well's Recreation at 505 in 1960** as a **STRONG CROSS-SOURCE INFERENCE**.
- Preserved limits: 1960 proprietor/licensee, formal punctuation, uninterrupted 1953–1960 operation, and exact Wells→505 Tavern transition remain unresolved.
- No institutional request sent and no fee authorized.""")

print(f"Integrated 1960 WELLS sign anchor as {SID} / {EID} / {TID}.")
