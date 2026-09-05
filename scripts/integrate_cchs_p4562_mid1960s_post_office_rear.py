from pathlib import Path
import hashlib, re
from PIL import Image

TARGET = "P-4562"
REVIEW = "2026-09-05"
STAGED = Path("research-inbox/p4562-steward-post-office-rear.jpg")
ORIGINAL = {
    "filename": "Oregon City 1960's - Street Scene - Southwest Corner of Main and McLoughlin - Mid 1960's.jpg",
    "width": 2048,
    "height": 1639,
    "bytes": 615961,
    "sha256": "979b74ea9aa53844a7e207aa3d8f8132c7b0a8da428a5fe5205f3dc8ae91a56f",
}
DERIVATIVE = {
    "width": 2400,
    "height": 1921,
    "bytes": 531979,
    "sha256": "aa0e7ce4106998fb835d3b42d852157bbe9fe8c703cae7162abff66b2d0e42f9",
}
TITLE = "Oregon City 1960's - Street Scene - Corner of Main and McLoughlin - Mid 1960's"
DESCRIPTION = "U.S. Post Office (rear view) (5th and Main Street) circa mid-1960s? U-1426.005109d"
OTHER_NO = "U-1426.005109d"

def rd(p):
    return Path(p).read_text(encoding="utf-8")

def wr(p, s):
    q = Path(p); q.parent.mkdir(parents=True, exist_ok=True)
    q.write_text(s, encoding="utf-8")

def append_once(p, marker, block):
    s = rd(p)
    if marker in s:
        return
    wr(p, s.rstrip() + "\n\n" + block.rstrip() + "\n")

def maxid(p, prefix):
    vals = [int(x) for x in re.findall(rf"\b{re.escape(prefix)}-(\d+)\b", rd(p))]
    return max(vals)

for p in ["evidence/source-register.md", "media/photo-metadata-register.md", "indexes/id-crosswalk.md"]:
    if TARGET in rd(p) or OTHER_NO in rd(p):
        print(f"{TARGET}/{OTHER_NO} already integrated; no changes needed.")
        raise SystemExit(0)

if not STAGED.exists():
    raise SystemExit(f"Missing staged local derivative: {STAGED}")
data = STAGED.read_bytes()
sha = hashlib.sha256(data).hexdigest()
with Image.open(STAGED) as im:
    w, h = im.size
if (w, h) != (DERIVATIVE["width"], DERIVATIVE["height"]) or len(data) != DERIVATIVE["bytes"] or sha != DERIVATIVE["sha256"]:
    raise SystemExit(f"Staged derivative mismatch: {(w,h)} {len(data)} {sha}")

SID = f"S-{maxid('evidence/source-register.md','S')+1:03d}"
EID = f"E-{maxid('evidence/evidence-register.md','E')+1:03d}"
MID = f"IMG-{maxid('media/photo-metadata-register.md','IMG')+1:04d}"
TID = f"T-{maxid('timeline.md','T')+1:03d}"

IMAGE = Path(f"media/photos/main-street/{MID}_circa-mid-1960s-us-post-office-rear-5th-main-cchs-p4562.jpg")
IMAGE.parent.mkdir(parents=True, exist_ok=True)
STAGED.replace(IMAGE)

CAP = "evidence/source-captures/cchs-p4562-mid-1960s-post-office-rear-5th-main-2026-09-05.md"
SOURCE_NAME = "CCHS P-4562 — circa-mid-1960s rear view of the 1933 U.S. Post Office at Fifth/Main"
EVIDENCE_NAME = "Circa-mid-1960s photograph shows the Fifth/Main U.S. Post Office intact before demolition"

capture = f"""# {SOURCE_NAME}

Reviewed **5 September 2026** from the project-steward supplied photograph and supplied Clackamas County Historical Society metadata.

Archive IDs: source `{SID}`; evidence `{EID}`; media `{MID}`; timeline `{TID}`.

## Supplied institutional metadata

- Name/Title: **{TITLE}**
- Entry/Object ID: **{TARGET}**
- Description: **{DESCRIPTION}**
- Other number embedded in description: **{OTHER_NO}**
- Date wording: **circa mid-1960s?** — the question mark is preserved. This is a tentative catalog/date attribution, not an exact exposure date.

The exact live CCHS CatalogIt object was retrieved by catalog number to preserve a valid repository image derivative. The steward-supplied metadata and original-file provenance are preserved separately.

## Project-steward original

- Original filename: `{ORIGINAL['filename']}`
- Dimensions: **{ORIGINAL['width']} × {ORIGINAL['height']}**
- Bytes: **{ORIGINAL['bytes']:,}**
- SHA-256: `{ORIGINAL['sha256']}`

## Repository binary

The committed repository copy is the **largest public image derivative recovered from the exact CCHS P-4562 object**. The steward-supplied original remains separately tracked by filename, dimensions, bytes and SHA-256:

- File: `{IMAGE.as_posix()}`
- Dimensions: **{DERIVATIVE['width']} × {DERIVATIVE['height']}**
- Bytes: **{DERIVATIVE['bytes']:,}**
- SHA-256: `{DERIVATIVE['sha256']}`
- Public derivative source: https://d8e7jbdw4fu0e.cloudfront.net/4813/f9d16500-d1cb-11ee-9dd0-db3630b944dc-vdUfFTx.lg@2x.jpg (CatalogIt derivative key `public_highres_2x`).

The exact original-file metadata above preserves the steward copy for audit and future exact-file reconciliation.

## Direct visual review

The supplied photograph directly shows an **intact brick institutional building** with a prominent gabled end, masonry trim, tall multi-pane windows, a large chimney, and a covered side/rear service or loading area. Mid-century automobiles and neighboring commercial/industrial context are visible.

The photograph itself does not display a readable construction date, demolition date, or street number. Identification as the **U.S. Post Office (rear view), Fifth and Main** comes from the supplied CCHS metadata.

## Cross-source relationship to the existing Post Office record

Existing archive evidence independently establishes:

- the 1950 Sanborn maps the **U.S. Post Office at the southeast corner of Fifth and Main** and marks it **BUILT 1933** (`E-102`);
- CCHS `U-1426.005098a` (`S-207` / `E-187` / `IMG-0736`) photographs that same 1933 Post Office **during demolition**, but the demolition photograph itself has no established exposure/demolition date.

`{TARGET}` therefore adds an earlier **intact-state photograph** of the same institution/location. The architectural and location connection is a **STRONG CROSS-SOURCE INFERENCE** from the supplied Post Office identification plus the independently mapped 1933 Fifth/Main Post Office and the existing demolition record.

Because the supplied description says **“circa mid-1960s?”** with a question mark, this image does **not** establish a firm mid-1960s terminus post quem for demolition. If the tentative attribution proves correct, demolition necessarily followed the photographed intact state; the exact demolition year remains unresolved.

## Evidence classification

- **DOCUMENTED / DIRECT (photographic):** an intact brick institutional building and its visible architectural/service-area condition.
- **DOCUMENTED / DIRECT (supplied institutional metadata):** CCHS object `{TARGET}` is described as the **U.S. Post Office (rear view), (5th and Main Street)** with related number `{OTHER_NO}`.
- **PROBABLE / TENTATIVE DATE:** “circa mid-1960s?” is preserved with its original uncertainty.
- **STRONG CROSS-SOURCE INFERENCE:** this is an intact-state view of the 1933 Fifth/Main Post Office already mapped in `E-102` and later represented in demolition by `E-187`.
- **UNRESOLVED:** exact exposure date; exact demolition date; demolition cause/project; precise sequence between this intact state and `IMG-0736`.

## Research consequence

This photograph materially improves the demolition chronology without closing it. The highest-value next step is to date either `{TARGET}` / `{OTHER_NO}` or the demolition image `U-1426.005098a` using city redevelopment records, federal/postal disposal records, permits, newspapers, or adjacent dated CCHS frames.
"""
wr(CAP, capture)

append_once("evidence/source-register.md", f"## {SID} —", f"""## {SID} — {SOURCE_NAME}
Type: Primary historic photograph with project-steward supplied CCHS metadata; **VISUALLY VERIFIED** 5 September 2026.
Institution: Clackamas County Historical Society (per supplied metadata).
Catalog ID: `{TARGET}`; related number `{OTHER_NO}`.
Date: **circa mid-1960s?** per supplied description; exact exposure date unresolved.
Repository image: `{IMAGE.as_posix()}`.
Capture: `{CAP}`.
Related evidence/media/timeline: `{EID}` / `{MID}` / `{TID}`.
Related prior Post Office evidence: `E-102`, `S-207` / `E-187` / `IMG-0736`.
Notes: Supplied metadata identifies the intact building as the U.S. Post Office rear view at Fifth/Main. The repository binary is a public CCHS derivative recovered from the exact P-4562 object; the steward original is separately tracked by its supplied file metadata.""")

append_once("evidence/evidence-register.md", f"## {EID} —", f"""## {EID} — {EVIDENCE_NAME}
Source: `{SID}`
Media: `{MID}`
Type: Primary photographic evidence plus supplied institutional metadata and cross-source structural chronology
Claims:
- The photograph directly shows an intact brick institutional building with gabled masonry elevation, tall windows, chimney and covered side/rear service area.
- Supplied CCHS metadata identifies `{TARGET}` as **U.S. Post Office (rear view) (5th and Main Street)** and gives related number `{OTHER_NO}`.
- Existing `E-102` independently places the U.S. Post Office at Fifth/Main and dates the building to 1933; `E-187` preserves an undated demolition photograph of that Post Office.
- The supplied “circa mid-1960s?” wording is tentative; this photograph does not establish an exact exposure or demolition date.
Classification: **DOCUMENTED / DIRECT** for visible condition and supplied metadata; **STRONG CROSS-SOURCE INFERENCE** for same-building chronology; **PROBABLE / TENTATIVE** for the mid-1960s date.
Confidence: Very High for the visible intact state; High for Post Office/Fifth-Main identification as supplied institutional metadata plus independent map context; Moderate for circa-mid-1960s dating because the supplied metadata includes a question mark.
Related evidence: `E-102`, `E-187`.""")

append_once("media/photo-metadata-register.md", f"## {MID} —", f"""## {MID} — CCHS P-4562, U.S. Post Office rear view at Fifth/Main
- Type: Historic street-level institutional-building photograph
- Date: **circa mid-1960s?** per supplied CCHS description; exact exposure date unresolved
- CCHS catalog: `{TARGET}`; description also gives `{OTHER_NO}`
- CCHS title: **{TITLE}**
- Repository file: `{IMAGE.as_posix()}`
- Status: `committed`
- Repository derivative: **{DERIVATIVE['width']} × {DERIVATIVE['height']}**; {DERIVATIVE['bytes']:,} bytes; SHA-256 `{DERIVATIVE['sha256']}`
- Steward original: `{ORIGINAL['filename']}`; **{ORIGINAL['width']} × {ORIGINAL['height']}**; {ORIGINAL['bytes']:,} bytes; SHA-256 `{ORIGINAL['sha256']}`
- Derivative note: repository binary is the largest valid public CCHS derivative recovered from the exact P-4562 CatalogIt object; the steward original is separately tracked by supplied filename/dimensions/bytes/SHA-256.
- Source/Evidence/Timeline: `{SID}` / `{EID}` / `{TID}`
- Related prior Post Office record: `S-207` / `E-187` / `IMG-0736`
- Key value: intact pre-demolition state of the 1933 Fifth/Main Post Office; supplied date remains tentative.""")

append_once("media/photos/inventory.md", f"### {MID} —", f"""### {MID} — Circa-mid-1960s? U.S. Post Office rear view at Fifth/Main
- File: `{IMAGE.as_posix()}`
- Source/evidence/timeline: `{SID}` / `{EID}` / `{TID}`
- CCHS: `{TARGET}`; supplied description references `{OTHER_NO}`
- Key value: photographs the 1933 Fifth/Main Post Office intact before the separately preserved demolition view (`IMG-0736`); exact exposure and demolition dates remain unresolved.
- Repository binary is a public derivative from the exact CCHS P-4562 object; exact steward-original filename/dimensions/size/hash are preserved in `media/photo-metadata-register.md`.""")

append_once("indexes/id-crosswalk.md", f"`{MID}` / `{SID}` / `{EID}` / CCHS `{TARGET}`", f"""| `{MID}` / `{SID}` / `{EID}` / CCHS `{TARGET}` | `{IMAGE.as_posix()}`; `{CAP}` | Supplied CCHS metadata identifies intact U.S. Post Office rear view at Fifth/Main, related `{OTHER_NO}`; cross-check `E-102` and demolition image `S-207` / `E-187` / `IMG-0736`. “Circa mid-1960s?” remains tentative. |""")

append_once("timeline.md", f"## {TID} —", f"""## {TID} — Circa mid-1960s? — U.S. Post Office still intact at Fifth/Main

CCHS `{TARGET}` (`{SID}` / `{EID}` / `{MID}`), from project-steward supplied metadata, identifies an **intact rear view of the U.S. Post Office at Fifth and Main**. Existing map evidence independently identifies the building as the **1933 Post Office** (`E-102`), while `IMG-0736` / `E-187` shows it later during demolition. The supplied **“circa mid-1960s?”** date is tentative, so this is not a firm demolition bracket; exact exposure and demolition dates remain unresolved.""")

append_once("registers/research-log.md", "CCHS P-4562 Post Office rear-view photograph", f"""### 2026-09-05 — CCHS P-4562 Post Office rear-view photograph
- Integrated the project-steward supplied photograph as `{MID}` / `{SID}` / `{EID}` / `{TID}`.
- Supplied metadata: `{TARGET}`, **U.S. Post Office (rear view) (5th and Main Street) circa mid-1960s?**, related number `{OTHER_NO}`.
- Direct visual review shows the institutional building intact; cross-source comparison links it to the 1933 Fifth/Main Post Office in `E-102` and the undated demolition view `E-187` / `IMG-0736`.
- Preserved the question mark on the mid-1960s attribution; no exact demolition-date inference was made.
- **Repository-image recovery:** the prior staged derivative could not be decoded by Pillow. The exact CCHS P-4562 CatalogIt object was therefore used to recover a valid public derivative; the steward original filename/dimensions/bytes/SHA-256 remain preserved in metadata.
- This integration does not alter annual research-status certifications.""")

append_once(
    "evidence/source-captures/undated-cchs-u1426-005098a-post-office-demolition-5th-main-photo-2026-09-03.md",
    "## 5 September 2026 intact-state cross-check — CCHS P-4562",
    f"""## 5 September 2026 intact-state cross-check — CCHS P-4562

New `{MID}` / `{SID}` / `{EID}` preserves CCHS `{TARGET}`, supplied as **U.S. Post Office (rear view) (5th and Main Street) circa mid-1960s?** and related number `{OTHER_NO}`. The photograph shows the Post Office intact, before the demolition state in `IMG-0736`. Because the P-4562 date itself is tentative, this narrows the chronology only **probabilistically**, not to a firm demolition bracket. Exact demolition date remains unresolved."""
)

append_once("database/sources.yml", f"  - id: {SID}", f"""  - id: {SID}
    name: "{SOURCE_NAME}"
    url: "https://hub.catalogit.app/clackamas-county-historical-society/folder/photographs/entry/oregon-city-1960s-street-scene-corner-of-main-and-mcloughlin-mid-1960s"
    type: Primary historic photograph with supplied CCHS metadata
    date: "circa mid-1960s?"
    repository_file: "{IMAGE.as_posix()}"
    notes: "Steward-supplied metadata identifies P-4562 as U.S. Post Office rear view at Fifth/Main, related U-1426.005109d. Repository binary is a valid public derivative recovered from the exact CCHS P-4562 object; steward-original provenance is preserved separately."
    related_evidence: [{EID}]
    related_media: [{MID}]""")

append_once("database/evidence.yml", f"  - id: {EID}", f"""  - id: {EID}
    name: "{EVIDENCE_NAME}"
    type: Primary photographic evidence plus supplied institutional metadata
    claims:
      - "Photograph directly shows the institutional building intact."
      - "Supplied CCHS metadata identifies P-4562 as U.S. Post Office rear view at Fifth/Main and references U-1426.005109d."
      - "Existing E-102 identifies the Fifth/Main Post Office as built 1933; E-187 preserves a later demolition-state photograph."
      - "The supplied circa mid-1960s? date is tentative and does not establish an exact demolition date."
    confidence: "Very High for visible intact state; High for supplied Post Office/location identification with independent map context; Moderate for tentative mid-1960s date."
    related_sources: [{SID}]
    related_media: [{MID}]
    repository_file: "{CAP}"
""")

append_once("database/timeline.yml", f"  - id: {TID}", f"""  - id: {TID}
    date: "circa mid-1960s?"
    title: "Circa mid-1960s? — U.S. Post Office intact at Fifth/Main"
    summary: "CCHS P-4562, from steward-supplied metadata, shows the Fifth/Main U.S. Post Office intact before the separately preserved demolition view; exact exposure and demolition dates remain unresolved."
    confidence: "High for intact-state/location relationship; Moderate for tentative date."
    related_sources: [{SID}]
    related_evidence: [{EID}]""")

print(f"Integrated {TARGET}: {SID} {EID} {MID} {TID}")
