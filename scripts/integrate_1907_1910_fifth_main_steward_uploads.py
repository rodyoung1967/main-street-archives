from pathlib import Path
import hashlib
import json
import re
import urllib.request

PAGES = [
    {
        "key": "sawyer1907",
        "date": "1907-03-01",
        "url": "https://oregonnews.uoregon.edu/lccn/sn00063698/1907-03-01/ed-1/seq-5.pdf",
        "target": "newspapers/oregon-city-courier/1907-03-01-page-5-sawyer-albright-meat-fifth-main.pdf",
        "upload_name": "5th & Main (Meat Business) Oregon City courier., March 01, 1907, Page 5, Image 5.pdf",
        "upload_sha256": "5a55f5ce3439f41c5bd71f57c71228520943f40634b3a1c389d589efcd41bd19",
        "upload_bytes": 512720,
        "source": "S-194",
        "evidence": "E-173",
    },
    {
        "key": "surber1907",
        "date": "1907-10-04",
        "url": "https://oregonnews.uoregon.edu/lccn/sn00063698/1907-10-04/ed-1/seq-3.pdf",
        "target": "newspapers/oregon-city-courier/1907-1908-surber-justin-review/1907-10-04-seq-03.pdf",
        "upload_name": "501 Main st (A. J. Surber) Oregon City courier., October 04, 1907, Page 3, Image 3.pdf",
        "upload_sha256": "beb6866b1046249b86eb0548d0b6963909be706d35a6c60ed63a705974bc679e",
        "upload_bytes": 594976,
        "existing_source": "S-135",
        "existing_evidence": "E-121",
    },
    {
        "key": "justin1908",
        "date": "1908-03-20",
        "url": "https://oregonnews.uoregon.edu/lccn/sn00063698/1908-03-20/ed-1/seq-7.pdf",
        "target": "newspapers/oregon-city-courier/1907-1908-surber-justin-review/1908-03-20-seq-07.pdf",
        "upload_name": "5th & Main (Justin & Hitchman) Oregon City courier., March 20, 1908, Page 7, Image 7.pdf",
        "upload_sha256": "93d82bbfb2de38cd6b8a96500353907e8316e4ed4e48c1e6b6ef36a70e306761",
        "upload_bytes": 756761,
        "source": "S-195",
        "evidence": "E-174",
    },
    {
        "key": "andresen1910",
        "date": "1910-02-11",
        "url": "https://oregonnews.uoregon.edu/lccn/sn00063698/1910-02-11/ed-1/seq-1.pdf",
        "target": "newspapers/oregon-city-courier/1910-02-11-page-1-andresen-stevens-main-water-property.pdf",
        "upload_name": "Main & Water Oregon City courier., February 11, 1910, Image 1.pdf",
        "upload_sha256": "9cc0596dbc2ddfeaf0e8c1b575dcca7b14c9af832e83f104b6b6e674dd0041b2",
        "upload_bytes": 659852,
        "source": "S-196",
        "evidence": "E-175",
    },
    {
        "key": "mt_hood1910",
        "date": "1910-03-18",
        "url": "https://oregonnews.uoregon.edu/lccn/sn00063698/1910-03-18/ed-1/seq-6.pdf",
        "target": "newspapers/oregon-city-courier/1910-03-18-page-6-m-justin-mt-hood-cafe-fifth-main.pdf",
        "upload_name": "5th & Main (M. Justin) Oregon City courier., March 18, 1910, Page 6, Image 6.pdf",
        "upload_sha256": "2b3ba938dd98cf3f0123c782c7e377b0f96b76ab39a53613f4f7b493edf1ed24",
        "upload_bytes": 530730,
        "source": "S-197",
        "evidence": "E-176",
    },
]


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_path(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def write(path: str, text: str) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def append_once(path: str, marker: str, block: str) -> None:
    text = read(path)
    if marker in text:
        return
    write(path, text.rstrip() + "\n\n" + block.rstrip() + "\n")


# Immutable-ID guards. Stop rather than reuse or renumber an existing record.
guards = [
    ("S-194", "evidence/source-register.md", r"(?m)^## S-194\b"),
    ("S-195", "evidence/source-register.md", r"(?m)^## S-195\b"),
    ("S-196", "evidence/source-register.md", r"(?m)^## S-196\b"),
    ("S-197", "evidence/source-register.md", r"(?m)^## S-197\b"),
    ("E-173", "evidence/evidence-register.md", r"(?m)^## E-173\b"),
    ("E-174", "evidence/evidence-register.md", r"(?m)^## E-174\b"),
    ("E-175", "evidence/evidence-register.md", r"(?m)^## E-175\b"),
    ("E-176", "evidence/evidence-register.md", r"(?m)^## E-176\b"),
    ("BUS-085", "businesses/business-index.md", r"(?m)^\| BUS-085 \|"),
    ("BUS-086", "businesses/business-index.md", r"(?m)^\| BUS-086 \|"),
    ("T-065", "database/timeline.yml", r"(?m)^  - id: T-065$"),
    ("T-066", "database/timeline.yml", r"(?m)^  - id: T-066$"),
    ("T-067", "database/timeline.yml", r"(?m)^  - id: T-067$"),
    ("T-068", "database/timeline.yml", r"(?m)^  - id: T-068$"),
    ("RL-047", "evidence/research-leads.md", r"(?m)^## RL-047\b"),
]
for ident, path, pattern in guards:
    if re.search(pattern, read(path)):
        raise SystemExit(f"{ident} is already assigned in {path}; refusing to reuse/renumber.")

# Download the canonical archive derivative for each issue/page, then deduplicate by its actual SHA-256.
existing_hashes = {}
for pdf in Path(".").rglob("*.pdf"):
    try:
        existing_hashes.setdefault(sha256_path(pdf), str(pdf))
    except OSError:
        pass

for item in PAGES:
    req = urllib.request.Request(item["url"], headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=90) as response:
        data = response.read()
    canonical_sha = sha256_bytes(data)
    canonical_bytes = len(data)
    item["canonical_sha256"] = canonical_sha
    item["canonical_bytes"] = canonical_bytes

    exact_existing = existing_hashes.get(canonical_sha)
    if exact_existing:
        item["repo_path"] = exact_existing
        item["repo_sha256"] = canonical_sha
        item["repo_bytes"] = Path(exact_existing).stat().st_size
        item["handling"] = "already present; canonical page derivative deduplicated"
    else:
        target = Path(item["target"])
        if target.exists():
            raise SystemExit(
                f"Target path collision for {item['key']}: {target} exists but does not match current canonical page bytes."
            )
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        item["repo_path"] = item["target"]
        item["repo_sha256"] = canonical_sha
        item["repo_bytes"] = canonical_bytes
        item["handling"] = "newly preserved canonical archive page"
        existing_hashes[canonical_sha] = item["target"]

    item["binary_relation"] = (
        "byte-for-byte identical to supplied upload"
        if item["repo_sha256"] == item["upload_sha256"] and item["repo_bytes"] == item["upload_bytes"]
        else "same issue/page; supplied upload is a different PDF binary derivative"
    )

# The 4 Oct. 1907 source must resolve to the established S-135 repository path, not create a second source page.
surber = next(x for x in PAGES if x["key"] == "surber1907")
if surber["repo_path"] != surber["target"]:
    raise SystemExit(f"Unexpected Surber canonical path: {surber['repo_path']}")

# The four previously missing issue/pages must be physically represented after reconciliation.
for key in ("sawyer1907", "justin1908", "andresen1910", "mt_hood1910"):
    item = next(x for x in PAGES if x["key"] == key)
    if not Path(item["repo_path"]).exists():
        raise SystemExit(f"Missing reconciled repository PDF for {key}")

by = {x["key"]: x for x in PAGES}

# Permanent provenance/reconciliation record.
rows = []
for item in PAGES:
    record = (
        f"`{item.get('existing_source')}` / `{item.get('existing_evidence')}`"
        if item.get("existing_source")
        else f"`{item['source']}` / `{item['evidence']}`"
    )
    rows.append(
        f"| `{item['upload_name']}` | `{item['upload_sha256']}` / {item['upload_bytes']} | "
        f"`{item['repo_path']}` | `{item['repo_sha256']}` / {item['repo_bytes']} | "
        f"**{item['handling']}**; {item['binary_relation']} | {record} |"
    )

capture = f"""# 1907–1910 Fifth/Main steward-upload reconciliation — Sawyer/Albright, Surber, Justin & Hitchman, Andresen/Stevens, Mt. Hood Cafe

Review date: **2 September 2026**.

Status: **FIVE PROJECT-STEWARD NEWSPAPER PAGE UPLOADS VISUALLY REVIEWED AND RECONCILED TO CANONICAL OREGON DIGITAL ISSUE/PAGE ROUTES. FOUR PREVIOUSLY MISSING ISSUE/PAGES ARE NOW REPRESENTED IN THE REPOSITORY; THE 4 OCTOBER 1907 SURBER PAGE REMAINS UNDER ITS EXISTING `S-135` / `E-121` RECORD.** Page-level integration does not change annual completion status.

## File reconciliation

| Supplied file | Supplied SHA-256 / bytes | Repository PDF | Repository SHA-256 / bytes | Handling | Record |
| --- | --- | --- | --- | --- | --- |
{chr(10).join(rows)}

The supplied PDF binaries and the canonical archive PDF derivatives are not assumed to be byte-identical. Where hashes differ, the archive preserves the canonical issue/page PDF and records the supplied upload hash as provenance rather than storing a redundant encoding of the same newspaper page.

## 1 March 1907 — R. A. Sawyer succeeds Charles Albright's meat business at Fifth/Main

The advertisement directly says **R. A. Sawyer** purchased **the Meat Business of Charles Albright**, would continue at **the old stand**, and gives **5th and Main Sts., Oregon City**. It also labels Sawyer **“Successor to Charles Albright.”** This is direct business-succession and intersection-location evidence by 1 March 1907.

Limits: the ad does not print a numbered street address, deed, building owner, exact sale date, or 501/503/505 mapping. A separate 4 October 1907 Strebig advertisement says **“Albright's Old Stand”** at the same intersection. Together they create a useful location-chain question, but they do not prove that Strebig bought directly from Sawyer or occupied the identical room without interruption.

## 4 October 1907 — A. J. Surber exact 501 Main page already preserved

The supplied page is the same newspaper issue/page already registered as `S-135` / `E-121`. It directly says A. J. Surber will apply for renewal at **the corner of Main and Fifth streets**, his **present place of business, No. 501**. The notice does not print Palace Saloon, prove the license was granted, or establish real-estate ownership. No duplicate source or evidence ID is created merely because the supplied PDF is a different binary derivative.

## 20 March 1908 — Justin & Hitchman and A. J. Surber separately at Main/Fifth

The page prints separate liquor-license applications for **Justin & Hitchman** and **A. J. Surber**, each describing a place of business at the **corner of Fifth and Main streets**, each seeking a six-month license. This materially bridges the December 1907 and September 1908 intersection-only records.

Limits: neither March notice prints 501 or a trade name; same-page/same-intersection wording does not prove the premises were the same room, that one applicant succeeded the other, that either application was granted, or that Surber's March 1908 premises were still the exact 501 room documented in October 1907.

## 11 February 1910 — William Andresen / H. C. Stevens Main-to-Water property article

The front-page article reports that **William Andresen**, identified as of Burmeister & Andresen, took a **one-half interest** in a business-district property, while **the other half was owned by H. C. Stevens**. It describes the property as **60 × 210 feet**, fronting **Main and Water streets** and running through the block. Two dwellings stood on the Water Street side; on the Main Street front, the article says the existing frame building **would soon be removed and a brick block constructed as soon as weather permitted**.

Limits: the article prints no numbered address, block, lot, or legal description. It does not establish that the property was 503/505, that Burmeister & Andresen the firm owned it, or that the announced demolition/brick construction actually occurred. Those statements remain individual ownership/context and **planned construction**, not completed-building proof.

## 18 March 1910 — M. Justin at the Mt. Hood Cafe, Fifth/Main

A liquor-license notice directly names **M. Justin** applying at **the Mt. Hood Cafe, 5th and Main streets**, for three months. This establishes the named trade style, applicant, and intersection context on 18 March 1910.

Limits: the notice does not print a street number, prove license grant, or identify M. Justin as either member of the earlier Justin & Hitchman partnership. The relationship between `BUS-046` Justin & Hitchman and `BUS-086` Mt. Hood Cafe remains unresolved.

## Interpretive rules retained

- Intersection-only evidence stays unassigned to 501/503/505 unless a source prints the number or a separate property bridge proves it.
- Liquor-license applications are not license grants, deeds, or proof of uninterrupted operation.
- “Old stand” language is a predecessor-location clue, not title evidence or proof of an unbroken occupant chain.
- Future-tense demolition/construction wording is not converted into completed work.
- M. Justin is not silently merged with an unidentified member of Justin & Hitchman.
"""
write("evidence/source-captures/1907-1910-fifth-main-steward-upload-reconciliation-2026-09-02.md", capture)

manifest = {
    "review_date": "2026-09-02",
    "status": "five uploads reconciled; four missing issue/pages represented; Surber 1907 page deduplicated under S-135/E-121",
    "files": PAGES,
}
write(
    "evidence/source-captures/1907-1910-fifth-main-steward-upload-reconciliation-manifest.json",
    json.dumps(manifest, indent=2) + "\n",
)

# Source register.
source_blocks = {
    "S-194": f"""## S-194 — Oregon City Courier, 1 March 1907, R. A. Sawyer succeeds Charles Albright meat business at Fifth/Main
Canonical PDF: {by['sawyer1907']['url']}  
Repository PDF: `{by['sawyer1907']['repo_path']}`  
Original uploaded filename: `{by['sawyer1907']['upload_name']}`  
Type: Primary newspaper advertisement; **VISUALLY VERIFIED**.  
Related evidence: `E-173`; related businesses `BUS-085`, `BUS-047`.  
Notes: R. A. Sawyer says he purchased Charles Albright's meat business, will continue at the old stand, and prints 5th and Main Sts.; the ad labels him successor to Charles Albright. No street number, deed, building owner, exact sale date, or 501/503/505 mapping. Repository canonical SHA-256 `{by['sawyer1907']['repo_sha256']}`; supplied upload SHA-256 `{by['sawyer1907']['upload_sha256']}`.""",
    "S-195": f"""## S-195 — Oregon City Courier, 20 March 1908, Justin & Hitchman and A. J. Surber at Fifth/Main
Canonical PDF: {by['justin1908']['url']}  
Repository PDF: `{by['justin1908']['repo_path']}`  
Original uploaded filename: `{by['justin1908']['upload_name']}`  
Type: Primary newspaper liquor-license notices; **VISUALLY VERIFIED**.  
Related evidence: `E-174`; cross-reference `E-121`, `E-122`, `E-123`.  
Notes: Separate six-month applications by Justin & Hitchman and A. J. Surber each say corner Fifth/Main. Neither prints 501 or a trade name; same intersection does not establish same room, succession, grant, or ownership. Repository canonical SHA-256 `{by['justin1908']['repo_sha256']}`; supplied upload SHA-256 `{by['justin1908']['upload_sha256']}`.""",
    "S-196": f"""## S-196 — Oregon City Courier, 11 February 1910, William Andresen / H. C. Stevens Main-to-Water property article
Canonical PDF: {by['andresen1910']['url']}  
Repository PDF: `{by['andresen1910']['repo_path']}`  
Original uploaded filename: `{by['andresen1910']['upload_name']}`  
Type: Primary newspaper property report; **VISUALLY VERIFIED**.  
Related evidence: `E-175`; contextual business `BUS-041`.  
Notes: William Andresen reportedly takes one-half interest; other half owned by H. C. Stevens. Property is described as 60x210 feet fronting Main and Water, with two Water-side dwellings and a Main-front frame building planned for removal/replacement by a brick block. No number/block/lot/legal description; planned work is not completed-construction proof and property is not assigned to 503/505. Repository canonical SHA-256 `{by['andresen1910']['repo_sha256']}`; supplied upload SHA-256 `{by['andresen1910']['upload_sha256']}`.""",
    "S-197": f"""## S-197 — Oregon City Courier, 18 March 1910, M. Justin at Mt. Hood Cafe, Fifth/Main
Canonical PDF: {by['mt_hood1910']['url']}  
Repository PDF: `{by['mt_hood1910']['repo_path']}`  
Original uploaded filename: `{by['mt_hood1910']['upload_name']}`  
Type: Primary newspaper liquor-license notice; **VISUALLY VERIFIED**.  
Related evidence: `E-176`; related business `BUS-086`; cross-reference `BUS-046`.  
Notes: M. Justin applies for a three-month liquor license at the Mt. Hood Cafe, 5th and Main streets. No number, grant, property ownership, or proof that M. Justin was a member of the earlier Justin & Hitchman partnership. Repository canonical SHA-256 `{by['mt_hood1910']['repo_sha256']}`; supplied upload SHA-256 `{by['mt_hood1910']['upload_sha256']}`.""",
}
for ident, block in source_blocks.items():
    append_once("evidence/source-register.md", f"## {ident} —", block)

# Evidence register and individual evidence records.
evidence_blocks = {
    "E-173": """## E-173 — R. A. Sawyer succeeds Charles Albright meat business at Fifth/Main, 1 March 1907
Type: Primary newspaper advertisement  
Source: `S-194`  
Claims: R. A. Sawyer directly states that he purchased Charles Albright's meat business, will continue at the old stand, and gives 5th and Main Sts., Oregon City; the ad labels Sawyer successor to Charles Albright. A separate October 1907 Strebig ad later uses “Albright's Old Stand” at the same intersection, providing a location-chain clue but not proof of a Sawyer→Strebig transaction.  
Confidence: **Very High** for Sawyer/Albright business succession wording and Fifth/Main location by 1 March 1907; exact number, property title, exact sale date, and Sawyer→Strebig succession unresolved.  
Related businesses: `BUS-085`, `BUS-047`.  
Related record: `evidence/E-173-1907-sawyer-albright-meat-fifth-main.md`""",
    "E-174": """## E-174 — Justin & Hitchman and A. J. Surber separately apply at Fifth/Main, 20 March 1908
Type: Primary newspaper liquor-license notices  
Source: `S-195`  
Claims: The same visually verified page prints separate six-month liquor-license applications for Justin & Hitchman and A. J. Surber, each describing a place of business at the corner of Fifth and Main streets. Neither March notice prints 501 or a trade name.  
Confidence: **Very High** for the two separate applications and intersection wording; exact room/number, relationship between premises, succession, license grant, and property ownership unresolved.  
Related businesses: `BUS-046`, `BUS-045`. Cross-reference `E-121`, `E-122`, `E-123`.  
Related record: `evidence/E-174-1908-justin-hitchman-surber-fifth-main.md`""",
    "E-175": """## E-175 — William Andresen / H. C. Stevens Main-to-Water property and planned brick block, 11 February 1910
Type: Primary newspaper property report  
Source: `S-196`  
Claims: The report says William Andresen of Burmeister & Andresen took a one-half interest in a central business property, the other half being owned by H. C. Stevens; describes it as 60x210 feet fronting Main and Water and running through the block; notes two dwellings on the Water side; and says the Main-front frame building would soon be removed and a brick block constructed when weather permitted.  
Confidence: **Very High** for the printed ownership/property-description/future-plan wording; exact parcel/address, firm versus individual ownership, completed demolition, and completed brick construction unresolved.  
Contextual business: `BUS-041`.  
Related record: `evidence/E-175-1910-andresen-stevens-main-water-property.md`""",
    "E-176": """## E-176 — M. Justin at Mt. Hood Cafe, Fifth/Main, 18 March 1910
Type: Primary newspaper liquor-license notice  
Source: `S-197`  
Claims: M. Justin directly applies for a three-month liquor license at the Mt. Hood Cafe, 5th and Main streets.  
Confidence: **Very High** for applicant, trade name, intersection, and application period; street number, license grant, ownership, and M. Justin's relationship to Justin & Hitchman unresolved.  
Related business: `BUS-086`; cross-reference `BUS-046`.  
Related record: `evidence/E-176-1910-m-justin-mt-hood-cafe.md`""",
}
for ident, block in evidence_blocks.items():
    append_once("evidence/evidence-register.md", f"## {ident} —", block)

write("evidence/E-173-1907-sawyer-albright-meat-fifth-main.md", """# E-173 — R. A. Sawyer succeeds Charles Albright meat business at Fifth/Main, 1 March 1907

Type: Primary newspaper advertisement.  
Source: `S-194`.  
Related businesses: `BUS-085`, `BUS-047`.

The visually verified advertisement directly states that **R. A. Sawyer** purchased **the Meat Business of Charles Albright**, would continue to do business **at the old stand**, and gives **5th and Main Sts., Oregon City**. It labels Sawyer **Successor to Charles Albright**.

This is direct business-succession and intersection-location evidence by 1 March 1907. It does not give a numbered street address, deed, building ownership, legal entity, or exact sale date.

A separate 4 October 1907 page (`E-123`) advertises **Strebig** fresh meats at **Albright's Old Stand, Cor. 5th and Main Sts.** The shared predecessor-location wording is a meaningful site chronology clue, but no source yet proves that Strebig purchased directly from Sawyer or that there was uninterrupted occupancy of the same room.
""")
write("evidence/E-174-1908-justin-hitchman-surber-fifth-main.md", """# E-174 — Justin & Hitchman and A. J. Surber separately apply at Fifth/Main, 20 March 1908

Type: Primary newspaper liquor-license notices.  
Source: `S-195`.  
Related businesses: `BUS-046`, `BUS-045`; cross-reference `E-121`, `E-122`, `E-123`.

The 20 March 1908 *Oregon City Courier* page directly prints separate six-month liquor-license applications for **Justin & Hitchman** and **A. J. Surber**. Each describes a place of business at the **corner of Fifth and Main streets**.

This bridges the December 1907 Justin & Hitchman record and the September 1908 page where Justin & Hitchman and Surber again appear separately at the same intersection.

Neither March notice prints **501**, **Palace Saloon**, or another trade name. Same-page/same-intersection wording does not establish the same room, a transfer/succession between applicants, a license grant, or real-estate ownership. Surber's exact 501 anchor remains the 4 October 1907 notice (`S-135` / `E-121`).
""")
write("evidence/E-175-1910-andresen-stevens-main-water-property.md", """# E-175 — William Andresen / H. C. Stevens Main-to-Water property and planned brick block, 11 February 1910

Type: Primary newspaper property report.  
Source: `S-196`.  
Contextual business: `BUS-041` Burmeister & Andresen.

The visually verified front-page report says **William Andresen**, identified as of Burmeister & Andresen, took a **one-half interest** in a central business-district property and that **the other half was owned by H. C. Stevens**. The property is described as **60x210 feet**, fronting **Main and Water streets** and running through the block. It had two dwellings on the Water Street side. On the Main Street front, the report says the existing frame building **would soon be removed and a brick block constructed as soon as the weather permitted**.

The article does not print a street number, block, lot, parcel, or legal description. The ownership wording is about William Andresen individually and does not by itself prove that Burmeister & Andresen the firm owned the property. The future-tense construction language is a plan, not proof that demolition or brick construction was completed. No 503/505 assignment is made without a parcel bridge.
""")
write("evidence/E-176-1910-m-justin-mt-hood-cafe.md", """# E-176 — M. Justin at Mt. Hood Cafe, Fifth/Main, 18 March 1910

Type: Primary newspaper liquor-license notice.  
Source: `S-197`.  
Related business: `BUS-086`; cross-reference `BUS-046` Justin & Hitchman.

The visually verified notice says **M. Justin** will apply for a three-month liquor license at **the Mt. Hood Cafe, 5th and Main streets**.

This directly establishes the applicant, trade name, intersection, and requested period on 18 March 1910. It does not print a numbered address, prove the license was granted, or establish building/property ownership.

Although the surname and location are relevant to the earlier Justin & Hitchman records, the source does not identify M. Justin as either partner. The archive therefore keeps the Mt. Hood Cafe (`BUS-086`) distinct from Justin & Hitchman (`BUS-046`) pending a direct identity or succession source.
""")

# New business records, deliberately avoiding unsupported formal-name/person identity assumptions.
write("businesses/r-a-sawyer-meat-business.md", """# R. A. Sawyer meat business

Business ID: `BUS-085`.

On **1 March 1907**, R. A. Sawyer advertised that he had purchased **the Meat Business of Charles Albright**, would continue at **the old stand**, and gave **5th and Main Sts., Oregon City** (`E-173` / `S-194`). The advertisement labels Sawyer **Successor to Charles Albright**.

This archive label is descriptive; the source does not supply a separate formal trade name. It also does not give a street number, title/deed, building owner, or exact sale date.

A 4 October 1907 Strebig fresh-meat advertisement later says **Albright's Old Stand** at Fifth/Main (`BUS-047`, `E-123`). That common predecessor-location wording is a strong research clue, but no direct Sawyer→Strebig sale or uninterrupted same-room chain has yet been proved.
""")
write("businesses/mt-hood-cafe.md", """# Mt. Hood Cafe

Business ID: `BUS-086`.

A visually verified **18 March 1910** *Oregon City Courier* liquor-license notice names **M. Justin** applying at **the Mt. Hood Cafe, 5th and Main streets**, for three months (`E-176` / `S-197`).

The source does not print a numbered address, prove that the application was granted, identify property ownership, or state that M. Justin was one of the earlier **Justin & Hitchman** partners. Because that identity/succession bridge is missing, `BUS-086` remains separate from `BUS-046`.
""")
append_once("businesses/business-index.md", "## 2 September 2026 Sawyer / Mt. Hood Cafe steward-page additions", """## 2 September 2026 Sawyer / Mt. Hood Cafe steward-page additions

| ID | Business Name | Address / Association | Notes |
| --- | --- | --- | --- |
| BUS-085 | [R. A. Sawyer meat business](r-a-sawyer-meat-business.md) | Fifth/Main; no number | 1 Mar. 1907 Sawyer says he purchased Charles Albright's meat business and continues at the old stand; direct predecessor wording. Later Strebig “Albright's Old Stand” is a site-chain clue, not a proved Sawyer→Strebig transfer. `E-173` / `S-194`. |
| BUS-086 | [Mt. Hood Cafe](mt-hood-cafe.md) | Fifth/Main; no number | 18 Mar. 1910 M. Justin liquor-license application directly names the Mt. Hood Cafe at Fifth/Main. Relationship to Justin & Hitchman unresolved. `E-176` / `S-197`. |""")

# Existing profiles/records get concise addenda rather than silent reinterpretation.
append_once("businesses/strebig-market.md", "## 1 March 1907 predecessor-site update", """## 1 March 1907 predecessor-site update
`S-194` / `E-173` now directly shows **R. A. Sawyer** announcing that he purchased **Charles Albright's meat business** and would continue at **the old stand, 5th and Main Sts.** This sharpens the predecessor-site context for the 4 October 1907 Strebig advertisement at **Albright's Old Stand**. It does **not** prove a direct Sawyer→Strebig sale, the exact room, or a numbered address.""")
append_once("businesses/justin-hitchman.md", "## 20 March 1908 bridge and 1910 Mt. Hood Cafe lead", """## 20 March 1908 bridge and 1910 Mt. Hood Cafe lead
`S-195` / `E-174` adds a visually verified **20 March 1908** page where **Justin & Hitchman** and **A. J. Surber** separately apply at the corner of Fifth/Main, each for six months. This sits between the 13 December 1907 and 18 September 1908 Justin & Hitchman records but still supplies no numbered address.

`S-197` / `E-176` visually verifies the previously noted **18 March 1910 M. Justin** notice and adds the printed trade name **Mt. Hood Cafe** at Fifth/Main. The source does not identify M. Justin as either member of Justin & Hitchman, so `BUS-046` and `BUS-086` remain separate pending a direct bridge.""")
append_once("businesses/a-j-surber.md", "## 20 March 1908 unnumbered Fifth/Main application", """## 20 March 1908 unnumbered Fifth/Main application
`S-195` / `E-174` directly prints a separate six-month A. J. Surber liquor-license application at the **corner of Fifth and Main streets** on the same page as Justin & Hitchman. Unlike Surber's 4 October 1907 notice (`S-135` / `E-121`), the March 1908 notice does **not** print 501 or Palace Saloon. It therefore supports continued intersection-level Surber activity, not exact-501 continuity or a transfer between the two applicants.""")
append_once("people/profiles/a-j-surber.md", "## 20 March 1908 unnumbered application", """## 20 March 1908 unnumbered application
A visually verified 20 March 1908 *Courier* page (`S-195` / `E-174`) separately lists A. J. Surber and Justin & Hitchman applying at the corner of Fifth/Main. Surber's notice on this date does not print 501 or Palace Saloon, so it is not used to extend exact-number or trade-name continuity beyond what other sources directly state.""")

# Extend the existing visual review rather than replacing its earlier conclusions.
append_once("evidence/source-captures/1907-1908-surber-justin-main-visual-review.md", "## 2 September 2026 supplied-page addendum", """## 2 September 2026 supplied-page addendum

Two steward-supplied pages sharpen the 1907–1908 sequence:

- **1 March 1907 (`S-194` / `E-173`)** — R. A. Sawyer says he purchased Charles Albright's meat business and continues at the old stand, **5th and Main Sts.** No number. This adds a predecessor-site bridge to the 4 October Strebig “Albright's Old Stand” advertisement without proving Sawyer→Strebig succession.
- **20 March 1908 (`S-195` / `E-174`)** — Justin & Hitchman and A. J. Surber separately apply for six-month liquor licenses at **Fifth/Main** on the same page. Neither notice prints a number. This strengthens the chronology between December 1907 and September 1908 but does not establish same room, succession, or exact-501 continuity.

The supplied **4 October 1907 Surber** page was also reconciled against existing `S-135` / `E-121`; it remains the direct exact **No. 501** anchor and is not duplicated under a new source ID.""")

# Source/evidence YAML mirrors.
for ident, name, url, notes in [
    ("S-194", "Oregon City Courier, 1 March 1907, R. A. Sawyer succeeds Charles Albright meat business at Fifth/Main", by['sawyer1907']['url'], f"Visually verified advertisement. R. A. Sawyer says he purchased Charles Albright's meat business, continues at the old stand, and prints Fifth/Main. No number or property title. Repository PDF {by['sawyer1907']['repo_path']}; canonical SHA-256 {by['sawyer1907']['repo_sha256']}. Related E-173."),
    ("S-195", "Oregon City Courier, 20 March 1908, Justin & Hitchman and A. J. Surber at Fifth/Main", by['justin1908']['url'], f"Visually verified separate six-month liquor-license applications for Justin & Hitchman and A. J. Surber at Fifth/Main. Neither prints 501 or trade name. Repository PDF {by['justin1908']['repo_path']}; canonical SHA-256 {by['justin1908']['repo_sha256']}. Related E-174."),
    ("S-196", "Oregon City Courier, 11 February 1910, William Andresen / H. C. Stevens Main-to-Water property article", by['andresen1910']['url'], f"Visually verified property report: Andresen one-half interest, Stevens other half, 60x210 Main-to-Water property, two Water-side dwellings, planned Main-front frame removal and brick block. No number/legal description; future plan not completed work. Repository PDF {by['andresen1910']['repo_path']}; canonical SHA-256 {by['andresen1910']['repo_sha256']}. Related E-175."),
    ("S-197", "Oregon City Courier, 18 March 1910, M. Justin at Mt. Hood Cafe, Fifth/Main", by['mt_hood1910']['url'], f"Visually verified liquor-license notice naming M. Justin at Mt. Hood Cafe, Fifth/Main. No number/grant/property ownership; relationship to Justin & Hitchman unresolved. Repository PDF {by['mt_hood1910']['repo_path']}; canonical SHA-256 {by['mt_hood1910']['repo_sha256']}. Related E-176."),
]:
    append_once("database/sources.yml", f"  - id: {ident}\n", f"""  - id: {ident}
    name: {name}
    url: {url}
    notes: >-
      {notes}""")

for ident, name, type_, claims, confidence, sources, businesses, repo_file in [
    ("E-173", "R. A. Sawyer succeeds Charles Albright meat business at Fifth/Main, 1 March 1907", "Primary newspaper advertisement", ["R. A. Sawyer states that he purchased Charles Albright's meat business, will continue at the old stand, and gives Fifth/Main; the ad labels Sawyer successor to Charles Albright.", "The later Strebig wording 'Albright's Old Stand' at the same intersection is a location-chain clue, not proof of a direct Sawyer-to-Strebig transaction."], "Very High for printed succession/location wording; exact number, title, exact sale date, and Sawyer-to-Strebig succession unresolved.", ["S-194"], ["BUS-085", "BUS-047"], "evidence/E-173-1907-sawyer-albright-meat-fifth-main.md"),
    ("E-174", "Justin & Hitchman and A. J. Surber separately apply at Fifth/Main, 20 March 1908", "Primary newspaper liquor-license notices", ["The same page separately lists Justin & Hitchman and A. J. Surber applying for six-month liquor licenses at the corner of Fifth/Main.", "Neither March notice prints 501 or a trade name; same intersection does not prove same room, succession, grant, or ownership."], "Very High for the separate applications and intersection wording; exact premises and relationship unresolved.", ["S-195"], ["BUS-046", "BUS-045"], "evidence/E-174-1908-justin-hitchman-surber-fifth-main.md"),
    ("E-175", "William Andresen / H. C. Stevens Main-to-Water property and planned brick block, 11 February 1910", "Primary newspaper property report", ["William Andresen reportedly took a one-half interest and H. C. Stevens owned the other half in a 60x210-foot property fronting Main and Water and running through the block.", "The report notes two Water-side dwellings and says the Main-front frame building would soon be removed and a brick block constructed when weather permitted.", "No number, block, lot, legal description, or completed-construction proof is supplied."], "Very High for printed ownership/property-description/future-plan wording; parcel identity and completed work unresolved.", ["S-196"], ["BUS-041"], "evidence/E-175-1910-andresen-stevens-main-water-property.md"),
    ("E-176", "M. Justin at Mt. Hood Cafe, Fifth/Main, 18 March 1910", "Primary newspaper liquor-license notice", ["M. Justin applies for a three-month liquor license at the Mt. Hood Cafe, Fifth/Main.", "The notice does not print a number, prove grant/ownership, or identify M. Justin as a member of Justin & Hitchman."], "Very High for applicant/trade-name/intersection wording; exact number, grant, ownership, and Justin identity relationship unresolved.", ["S-197"], ["BUS-086"], "evidence/E-176-1910-m-justin-mt-hood-cafe.md"),
]:
    claims_yaml = "\n".join(f"      - {c}" for c in claims)
    srcs = ", ".join(sources)
    buses = ", ".join(businesses)
    append_once("database/evidence.yml", f"  - id: {ident}\n", f"""  - id: {ident}
    name: {name}
    type: {type_}
    claims:
{claims_yaml}
    confidence: >-
      {confidence}
    related_sources: [{srcs}]
    related_businesses: [{buses}]
    repository_file: {repo_file}""")

append_once("database/businesses.yml", "  - id: BUS-085\n", """  - id: BUS-085
    name: R. A. Sawyer meat business
    repository_file: businesses/r-a-sawyer-meat-business.md
    address: Fifth/Main; no number
    notes: Descriptive archive label. 1 Mar. 1907 Sawyer says he purchased Charles Albright's meat business and continues at the old stand. Later Strebig 'Albright's Old Stand' is a site-chain clue, not a proved direct transfer.
    related_evidence: [E-173]
    related_sources: [S-194]""")
append_once("database/businesses.yml", "  - id: BUS-086\n", """  - id: BUS-086
    name: Mt. Hood Cafe
    repository_file: businesses/mt-hood-cafe.md
    address: Fifth/Main; no number
    notes: 18 Mar. 1910 M. Justin liquor-license application names Mt. Hood Cafe at Fifth/Main. Relationship to Justin & Hitchman remains unresolved.
    related_evidence: [E-176]
    related_sources: [S-197]""")

# Timeline YAML.
for ident, date, summary, confidence, evidence, sources, businesses in [
    ("T-065", "1 March 1907", "R. A. Sawyer advertises that he purchased Charles Albright's meat business, will continue at the old stand, and gives Fifth/Main; later Strebig 'Albright's Old Stand' is a site-chain clue only.", "Very High for printed succession and Fifth/Main; no number/title or direct Sawyer-to-Strebig transfer.", ["E-173"], ["S-194"], ["BUS-085", "BUS-047"]),
    ("T-066", "20 March 1908", "Justin & Hitchman and A. J. Surber separately apply for six-month liquor licenses at the corner of Fifth/Main on the same Courier page.", "Very High for separate applications/intersection wording; neither notice prints 501, a trade name, grant, same-room relationship, or succession.", ["E-174"], ["S-195"], ["BUS-046", "BUS-045"]),
    ("T-067", "11 February 1910", "Courier reports William Andresen took one-half interest and H. C. Stevens owned the other half in a 60x210 Main-to-Water property; a Main-front frame building was planned for removal and replacement by a brick block.", "Very High for printed report; no number/legal description and future construction is not completed-work proof.", ["E-175"], ["S-196"], ["BUS-041"]),
    ("T-068", "18 March 1910", "M. Justin applies for a three-month liquor license at the Mt. Hood Cafe, Fifth/Main.", "Very High for applicant/trade name/intersection; number, grant, ownership, and relationship to Justin & Hitchman unresolved.", ["E-176"], ["S-197"], ["BUS-086"]),
]:
    append_once("database/timeline.yml", f"  - id: {ident}\n", f"""  - id: {ident}
    date: {date}
    summary: >-
      {summary}
    confidence: >-
      {confidence}
    related_evidence: [{', '.join(evidence)}]
    related_sources: [{', '.join(sources)}]
    related_businesses: [{', '.join(businesses)}]""")

# Human-readable timeline/address/register integration.
append_once("timeline.md", "## 1907 — Sawyer succeeds Albright meat business at Fifth/Main", """## 1907 — Sawyer succeeds Albright meat business at Fifth/Main
On **1 March 1907**, R. A. Sawyer directly advertised that he had purchased **Charles Albright's meat business**, would continue at **the old stand**, and gave **5th and Main Sts.** (`S-194` / `E-173`; `BUS-085`). On **4 October**, Strebig advertised fresh meats at **Albright's Old Stand** at the same intersection (`E-123`; `BUS-047`). The shared Albright-site wording supports a location-chain lead but does not prove a direct Sawyer→Strebig transfer, exact room, or numbered address.

On **20 March 1908**, Justin & Hitchman and A. J. Surber separately applied at the corner of Fifth/Main on the same page (`S-195` / `E-174`). Neither notice prints 501 or a trade name, so Surber's exact-501 anchor remains 4 October 1907 and no same-room/succession claim is made.""")
append_once("timeline.md", "## 1910 — Main/Water property article and Mt. Hood Cafe at Fifth/Main", """## 1910 — Main/Water property article and Mt. Hood Cafe at Fifth/Main
On **11 February 1910**, the *Courier* reported that William Andresen took one-half interest and H. C. Stevens owned the other half in a **60×210-foot** property fronting Main and Water; two dwellings were on the Water side, while a Main-front frame building was planned for removal and replacement by a brick block (`S-196` / `E-175`). No number/legal description is printed and the planned construction is not treated as completed work or assigned to 503/505.

On **18 March 1910**, **M. Justin** applied for a liquor license at **the Mt. Hood Cafe, Fifth and Main streets** (`S-197` / `E-176`; `BUS-086`). No number or grant is printed, and M. Justin is not automatically identified as a member of Justin & Hitchman.""")
append_once("registers/business-timeline.md", "## 1907–1910 Fifth/Main supplied-page additions — 2 September 2026", """## 1907–1910 Fifth/Main supplied-page additions — 2 September 2026

| Date | Printed location | Business/person | Evidence | Limits |
| --- | --- | --- | --- | --- |
| 1 Mar. 1907 | Fifth/Main | R. A. Sawyer, successor to Charles Albright meat business | `S-194` / `E-173`; `BUS-085` | No number/title/exact sale date; later Strebig old-stand wording does not prove direct transfer. |
| 4 Oct. 1907 | Main/Fifth, **No. 501** | A. J. Surber | existing `S-135` / `E-121` | Supplied page is same issue/page and was deduplicated; notice is application/renewal, not grant/title; no Palace name. |
| 20 Mar. 1908 | Fifth/Main | Justin & Hitchman; separately A. J. Surber | `S-195` / `E-174` | Neither prints 501/trade name; no same-room or succession inference. |
| 18 Mar. 1910 | Fifth/Main | M. Justin — **Mt. Hood Cafe** | `S-197` / `E-176`; `BUS-086` | No number/grant/title; relationship to Justin & Hitchman unresolved. |""")
append_once("registers/address-register.md", "## 2 September 2026 — 1907–1910 supplied-page address additions", """## 2 September 2026 — 1907–1910 supplied-page address additions

| Printed location | Date | Named person/business | Classification / limit |
| --- | --- | --- | --- |
| Fifth/Main; no number | 1 Mar. 1907 | R. A. Sawyer, successor to Charles Albright meat business | Direct visually verified intersection/business-succession wording (`E-173`); no 501/503/505 assignment. |
| Main/Fifth, **No. 501** | 4 Oct. 1907 | A. J. Surber | Existing exact-number anchor (`E-121`); supplied PDF derivative deduplicated under `S-135`. |
| Fifth/Main; no number | 20 Mar. 1908 | Justin & Hitchman; separately A. J. Surber | Direct visually verified intersection applications (`E-174`); no same-room/501 continuity inference. |
| Main and Water frontage; 60x210 ft; no number/legal description | 11 Feb. 1910 | William Andresen / H. C. Stevens property interests | Direct reported property description (`E-175`); unassigned to target parcels. |
| Fifth/Main; no number | 18 Mar. 1910 | M. Justin, Mt. Hood Cafe | Direct visually verified trade-name/intersection notice (`E-176`); no 501/503/505 assignment. |""")

append_once("evidence/research-leads.md", "## RL-047 — Resolve 1907–1910 Fifth/Main business and Main/Water property bridges", """## RL-047 — Resolve 1907–1910 Fifth/Main business and Main/Water property bridges
New visually verified supplied pages create three focused bridge questions:

1. **Albright → Sawyer → Strebig meat-business site:** locate licenses, directories, sale notices, deeds/leases, or other ads showing whether R. A. Sawyer's March 1907 “old stand” at Fifth/Main and Strebig's October 1907 “Albright's Old Stand” were the same room and whether Strebig acquired directly from Sawyer.
2. **Justin & Hitchman → M. Justin / Mt. Hood Cafe:** identify the partners' given names and determine whether the M. Justin at Mt. Hood Cafe in March 1910 was one of them or a separate person/business; do not infer identity from surname/intersection alone.
3. **Andresen / Stevens Main-to-Water property:** recover deed, assessment, plat, permit, or follow-up construction evidence identifying the 60x210 property and determining whether the announced frame-building removal and brick-block construction occurred. Do not assign it to 503/505 without a legal/property bridge.
""")
append_once("registers/research-log.md", "### 2026-09-02 — Reconcile 1907–1910 Fifth/Main steward uploads", """### 2026-09-02 — Reconcile 1907–1910 Fifth/Main steward uploads
- Reconciled five steward-supplied newspaper page PDFs to canonical Oregon Digital issue/page routes and preserved upload-vs-repository SHA-256 provenance.
- Kept the 4 Oct. 1907 Surber page under existing `S-135` / `E-121` rather than creating a duplicate historical source for a different PDF encoding.
- Added `S-194` / `E-173`: R. A. Sawyer succeeds Charles Albright's meat business at Fifth/Main, 1 Mar. 1907; created descriptive `BUS-085` and linked the later Strebig “Albright's Old Stand” clue without asserting direct succession.
- Added `S-195` / `E-174`: separate Justin & Hitchman and Surber Fifth/Main applications, 20 Mar. 1908; no exact-number/same-room inference.
- Added `S-196` / `E-175`: William Andresen / H. C. Stevens 60x210 Main-to-Water property report and future brick-block plan, 11 Feb. 1910; no target-parcel or completed-construction assertion.
- Added `S-197` / `E-176`: M. Justin at Mt. Hood Cafe, Fifth/Main, 18 Mar. 1910; created `BUS-086` while keeping Justin & Hitchman identity/continuity unresolved.
- Added `RL-047` for the three resulting bridge questions. No annual completion-status change.""")
append_once("indexes/id-crosswalk.md", "## 2 September 2026 — 1907–1910 Fifth/Main supplied-page additions", """## 2 September 2026 — 1907–1910 Fifth/Main supplied-page additions
- `S-194` ↔ `E-173` ↔ `BUS-085` — 1 Mar. 1907 R. A. Sawyer / Charles Albright meat-business succession at Fifth/Main; later `BUS-047` Strebig old-stand clue.
- Existing `S-135` ↔ `E-121` — 4 Oct. 1907 A. J. Surber exact No. 501; supplied PDF derivative reconciled without duplicate ID.
- `S-195` ↔ `E-174` ↔ `BUS-046`, `BUS-045` — 20 Mar. 1908 separate Justin & Hitchman and Surber Fifth/Main applications.
- `S-196` ↔ `E-175` ↔ contextual `BUS-041` — 11 Feb. 1910 Andresen/Stevens 60x210 Main-to-Water property and planned brick-block report; parcel unresolved.
- `S-197` ↔ `E-176` ↔ `BUS-086` — 18 Mar. 1910 M. Justin at Mt. Hood Cafe, Fifth/Main; relationship to `BUS-046` unresolved.
- Timeline IDs: `T-065` through `T-068`. Follow-up: `RL-047`.""")
append_once("ARCHIVE_INDEX.md", "## Steward uploads — 1907–1910 Fifth/Main Sawyer/Surber/Justin/Andresen/Mt. Hood reconciliation", """## Steward uploads — 1907–1910 Fifth/Main Sawyer/Surber/Justin/Andresen/Mt. Hood reconciliation
[Reconciliation audit](evidence/source-captures/1907-1910-fifth-main-steward-upload-reconciliation-2026-09-02.md) accounts for five supplied PDFs and records both supplied-upload and repository/canonical SHA-256 values. The **4 Oct. 1907 A. J. Surber exact-501 page** stays under existing `S-135` / `E-121`; no duplicate source is created for a different PDF encoding. New source/evidence pairs are **`S-194` / `E-173`** (R. A. Sawyer succeeds Charles Albright meat business at Fifth/Main), **`S-195` / `E-174`** (Justin & Hitchman and Surber separately at Fifth/Main on 20 Mar. 1908), **`S-196` / `E-175`** (Andresen/Stevens Main-to-Water property and future brick-block plan), and **`S-197` / `E-176`** (M. Justin at Mt. Hood Cafe, Fifth/Main). New descriptive business records are `BUS-085` and `BUS-086`. Intersection-only pages remain unassigned to 501/503/505; planned construction remains uncompleted until separately proved.""")

print("Reconciled pages:")
for item in PAGES:
    print(
        f"{item['date']} {item['key']}: {item['handling']} -> {item['repo_path']} | "
        f"repo {item['repo_sha256']} {item['repo_bytes']} bytes | upload {item['upload_sha256']} {item['upload_bytes']} bytes | {item['binary_relation']}"
    )
