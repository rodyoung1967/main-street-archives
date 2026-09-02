from pathlib import Path
import hashlib
import re
import urllib.request

PAGES = [
    {
        "key": "justin1907",
        "url": "https://oregonnews.uoregon.edu/lccn/sn00063698/1907-12-13/ed-1/seq-3.pdf",
        "sha256": "3c42bc92aca99f178e60e76c0430571b1aaee47869fd26e52b17fd614be0ae50",
        "size": 662306,
        "repo_path": "newspapers/oregon-city-courier/1907-1908-surber-justin-review/1907-12-13-seq-03.pdf",
        "upload_name": "5th & Main (Justin & Hitchman) Oregon City courier., December 13, 1907, Page 3, Image 3.pdf",
        "existing_source": "S-136",
    },
    {
        "key": "justin1908",
        "url": "https://oregonnews.uoregon.edu/lccn/sn00063698/1908-09-18/ed-1/seq-9.pdf",
        "sha256": "62ce8e70f6e13a3614bc85eae7c3071a33dd83f36eda9973bf1ba75f4b7fe11a",
        "size": 787391,
        "repo_path": "newspapers/oregon-city-courier/1907-1908-surber-justin-review/1908-09-18-seq-09.pdf",
        "upload_name": "5th & Main (Justin & Hitchman) Oregon City courier., September 18, 1908, Image 9.pdf",
        "existing_source": "S-137",
    },
    {
        "key": "chicago1913",
        "url": "https://oregonnews.uoregon.edu/lccn/sn00063698/1913-12-25/ed-1/seq-1.pdf",
        "sha256": "f876dda085a7ab945fa575eb38f7ff32e7d65b9527add2f8a9530b1ef11e62c5",
        "size": 861081,
        "repo_path": "newspapers/oregon-city-courier/1913-12-25-page-1-chicago-store-fire-george-harding.pdf",
        "upload_name": "Chicago Store (possibly 505 main) Oregon City courier., December 25, 1913, Image 1.pdf",
        "new_source": "S-192",
    },
    {
        "key": "fire1922",
        "url": "https://oregonnews.uoregon.edu/lccn/sn00063699/1922-07-20/ed-1/seq-1.pdf",
        "sha256": "0ab3c8107f64353d0a40c6d98c4fe832d0851c983da219a85062f52dad5bfdfa",
        "size": 747595,
        "repo_path": "newspapers/banner-courier/1922-07-20-page-1-fifth-main-fire.pdf",
        "upload_name": "5th & Main Fire The banner-courier., July 20, 1922, Image 1.pdf",
        "existing_source": "S-117",
    },
    {
        "key": "jagers1940",
        "url": "https://oregonnews.uoregon.edu/lccn/2017260114/1940-10-18/ed-1/seq-3.pdf",
        "sha256": "fead077f125cc8bc3e7bf551dfe09102a04ecebc8ee39f1daf4ed34abfc74b20",
        "size": 494158,
        "repo_path": "newspapers/the-amplifier/1940-10-18-page-3-jagers-503-main.pdf",
        "upload_name": "503 Main (Jagers) The amplifier., October 18, 1940, Page 3, Image 3.pdf",
        "new_source": "S-193",
    },
]

def digest(path: Path) -> str:
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

def replace_once(path: str, old: str, new: str, required: bool = True) -> None:
    text = read(path)
    if old not in text:
        if required:
            raise SystemExit(f"Expected text not found in {path}: {old[:120]!r}")
        return
    write(path, text.replace(old, new, 1))

def replace_all(path: str, old: str, new: str) -> None:
    text = read(path)
    if old in text:
        write(path, text.replace(old, new))

def replace_md_section(path: str, heading: str, block: str) -> None:
    text = read(path)
    pattern = re.compile(r"(?ms)^" + re.escape(heading) + r"\n.*?(?=^## |\Z)")
    match = pattern.search(text)
    if not match:
        raise SystemExit(f"Missing Markdown section {heading!r} in {path}")
    write(path, text[:match.start()] + block.rstrip() + "\n\n" + text[match.end():])

def replace_yaml_record(path: str, ident: str, block: str) -> None:
    text = read(path)
    pattern = re.compile(r"(?ms)^  - id: " + re.escape(ident) + r"\n.*?(?=^  - id: |\Z)")
    match = pattern.search(text)
    if not match:
        raise SystemExit(f"Missing YAML record {ident} in {path}")
    write(path, text[:match.start()] + block.rstrip() + "\n\n" + text[match.end():])

# Immutable-ID availability guards. Scripts are ignored by archive validation, but live records may not collide.
guards = [
    ("S-192", "evidence/source-register.md", r"(?m)^## S-192\b"),
    ("S-193", "evidence/source-register.md", r"(?m)^## S-193\b"),
    ("E-171", "evidence/evidence-register.md", r"(?m)^## E-171\b"),
    ("E-172", "evidence/evidence-register.md", r"(?m)^## E-172\b"),
    ("BUS-084", "businesses/business-index.md", r"(?m)^\| BUS-084 \|"),
    ("T-063", "database/timeline.yml", r"(?m)^  - id: T-063$"),
    ("T-064", "database/timeline.yml", r"(?m)^  - id: T-064$"),
]
for ident, path, pattern in guards:
    if re.search(pattern, read(path)):
        raise SystemExit(f"{ident} is already assigned in {path}; stop rather than reuse/renumber.")

# Reconcile supplied pages by exact SHA-256. Existing exact files are deduplicated; missing files are fetched from canonical archive pages.
existing_by_hash = {}
for pdf in Path(".").rglob("*.pdf"):
    try:
        existing_by_hash.setdefault(digest(pdf), str(pdf))
    except OSError:
        pass

for item in PAGES:
    found = existing_by_hash.get(item["sha256"])
    if found:
        item["actual_path"] = found
        item["handling"] = "already present; deduplicated"
        if Path(found).stat().st_size != item["size"]:
            raise SystemExit(f"Unexpected size for existing hash-matched file {found}")
        continue

    req = urllib.request.Request(item["url"], headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=90) as response:
        data = response.read()
    got = hashlib.sha256(data).hexdigest()
    if got != item["sha256"] or len(data) != item["size"]:
        raise SystemExit(
            f"Canonical page mismatch for {item['key']}: got sha={got}, bytes={len(data)}; "
            f"expected sha={item['sha256']}, bytes={item['size']}"
        )
    target = Path(item["repo_path"])
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    item["actual_path"] = item["repo_path"]
    item["handling"] = "newly preserved"
    existing_by_hash[item["sha256"]] = item["repo_path"]

by = {x["key"]: x for x in PAGES}

# Hard dedupe expectations for pages known to have been preserved in earlier work.
for key in ("justin1907", "justin1908", "fire1922"):
    if by[key]["handling"] != "already present; deduplicated":
        raise SystemExit(f"{key} was expected to deduplicate but did not: {by[key]}")
# The two newly supplied gaps should become physical repository files in this integration.
for key in ("chicago1913", "jagers1940"):
    if not Path(by[key]["actual_path"]).exists():
        raise SystemExit(f"Missing expected preserved file for {key}")

# Permanent reconciliation/provenance note covering all five supplied uploads.
capture = f"""# 1907–1940 steward-upload reconciliation: Justin & Hitchman, Chicago Store fire, Fifth/Main fire, and JAGERS

Review date: **2 September 2026**.

Status: **FIVE PROJECT-STEWARD PDF UPLOADS RECONCILED BY SHA-256; TWO NEW PAGE FILES PRESERVED; THREE EXACT DUPLICATES RETAINED UNDER EXISTING SOURCE IDS.** This is page-level source integration only and does not change any annual completion status.

## File reconciliation

| Supplied file | SHA-256 / bytes | Repository file | Handling | Record |
| --- | --- | --- | --- | --- |
| `{by['justin1907']['upload_name']}` | `{by['justin1907']['sha256']}` / {by['justin1907']['size']} | `{by['justin1907']['actual_path']}` | **{by['justin1907']['handling']}** | `S-136` / `E-122` |
| `{by['justin1908']['upload_name']}` | `{by['justin1908']['sha256']}` / {by['justin1908']['size']} | `{by['justin1908']['actual_path']}` | **{by['justin1908']['handling']}** | `S-137` / `E-122`, `E-123` |
| `{by['chicago1913']['upload_name']}` | `{by['chicago1913']['sha256']}` / {by['chicago1913']['size']} | `{by['chicago1913']['actual_path']}` | **{by['chicago1913']['handling']}** | `S-192` / `E-171` |
| `{by['fire1922']['upload_name']}` | `{by['fire1922']['sha256']}` / {by['fire1922']['size']} | `{by['fire1922']['actual_path']}` | **{by['fire1922']['handling']}** | `S-117` / `E-103` |
| `{by['jagers1940']['upload_name']}` | `{by['jagers1940']['sha256']}` / {by['jagers1940']['size']} | `{by['jagers1940']['actual_path']}` | **{by['jagers1940']['handling']}** | `S-193` / `E-172` |

## Integrated historical findings

### 13 December 1907 — Justin & Hitchman
The already-preserved *Oregon City Courier* page visually prints a liquor-license application by **Justin & Hitchman** at the **corner of Main and Fifth streets**, for six months. It does not print 501, 503, 505, a historical trade name, a license grant, or a property title. No new source ID is created.

### 18 September 1908 — Justin & Hitchman / Surber
The already-preserved *Courier* image 9 prints separate liquor-license applications for **Justin & Hitchman** and **A. J. Surber**, each at Main/Fifth, and also prints Thomas Hartman on Main between Fifth and Sixth. Common intersection wording does not establish the physical relationship of the premises or a succession. No new source ID is created.

### 25 December 1913 — Chicago Store fire / George Harding
The newly preserved and visually inspected *Oregon City Courier* front page reports that the **Chicago clothing store on Main Street, south of the postoffice, was gutted by fire** on the preceding Saturday night. It says the interior and goods were badly damaged and explicitly states **“The building was owned by George Harding.”** The fire article itself does **not** print 505 Main.

Independent exact-address Chicago Store advertising already places the business at **505 Main** in 1911 and again in January 1913 (`S-032` / `E-026`). Therefore the fire-page wording upgrades the George Harding building-owner statement from OCR/TEXT ONLY to **VISUALLY VERIFIED**, while the identification of the burned premises with the documented 505 Main Chicago Store remains a **STRONG CROSS-SOURCE INFERENCE**, not deed-level title or proof of surviving-building continuity.

### 20 July 1922 — Fifth/Main fire
The supplied *Banner-Courier* page is byte-for-byte identical to existing `S-117` / `E-103`. It remains the visually verified local fire account: ignition in the vacant former Schieremann tailor room, S. Wolf named owner, adjoining pool hall water/fire damage, and destruction of the laundry/garage/restaurant/shoe-repair/confectionery cluster. Exact 501/503/505 mapping remains unresolved. No duplicate source is created.

### 18 October 1940 — JAGERS at 503 Main
The newly preserved *Amplifier* page contains a boxed advertisement reading **“TIRED? Drop in at JAGERS / Cozy place for / A Tasty Pickup / 503 Main St. Oregon City.”** This is direct exact-address evidence for a business/trade style **JAGERS at 503 Main on 18 October 1940** and for a food/refreshment-oriented “tasty pickup” context.

The ad does **not** print `J. Jager`, `New Kwality Cafe`, `Kwality Cafe`, proprietor, ownership, or legal-entity wording. Because existing artifact evidence separately identifies **J. Jager** as proprietor of **New Kwality Cafe, 503 Main**, the same-address/name resemblance is an important research bridge, but the archive keeps **JAGERS (`BUS-084`) separate from New Kwality Cafe (`BUS-002`) and P-003 unless a direct identity/name-change source is recovered**.

## Interpretive limits

- Intersection language is not converted into 501/503/505 without exact-number evidence.
- A liquor-license application is not a license grant, deed, or proof of uninterrupted operation.
- The 1913 fire article's George Harding statement concerns **the building containing the Chicago clothing store**; it is not by itself a deed or exact modern parcel description.
- The 1940 `JAGERS` advertisement establishes the printed business style/address only. It does not prove that JAGERS and New Kwality Cafe were the same business or that `JAGERS` was named for P-003.
- The 1922 fire page remains an exact duplicate of the existing local fire source and does not resolve the storefront-number model.
"""
write("evidence/source-captures/1907-1940-steward-upload-reconciliation-2026-09-02.md", capture)

# New source records.
append_once(
    "evidence/source-register.md",
    "## S-192 — Oregon City Courier, 25 December 1913, Chicago Store fire and George Harding building-owner statement",
    f"""## S-192 — Oregon City Courier, 25 December 1913, Chicago Store fire and George Harding building-owner statement
Canonical PDF: {by['chicago1913']['url']}  
Repository PDF: `{by['chicago1913']['actual_path']}`  
Original uploaded filename: `{by['chicago1913']['upload_name']}`  
Type: Primary newspaper fire report; **VISUALLY VERIFIED**.  
Related evidence: `E-171`; cross-reference `E-026`, `E-108`.  
Notes: Front-page report says the Chicago clothing store on Main Street south of the postoffice was gutted in the preceding Saturday-night fire and explicitly says **the building was owned by George Harding**. The article itself does not print 505 Main. Independent Chicago Store exact-address advertising at 505 Main makes the 505 identification a strong cross-source inference, not a deed or a direct exact-address statement from this fire page. SHA-256 `{by['chicago1913']['sha256']}`."""
)
append_once(
    "evidence/source-register.md",
    "## S-193 — The Amplifier, 18 October 1940, JAGERS at 503 Main",
    f"""## S-193 — The Amplifier, 18 October 1940, JAGERS at 503 Main
Canonical PDF: {by['jagers1940']['url']}  
Repository PDF: `{by['jagers1940']['actual_path']}`  
Original uploaded filename: `{by['jagers1940']['upload_name']}`  
Type: Primary newspaper advertisement; **VISUALLY VERIFIED**.  
Related evidence: `E-172`; related business `BUS-084`; address `B-001`.  
Notes: Page-three advertisement reads **JAGERS**, “Cozy place for A Tasty Pickup,” **503 Main St. Oregon City**. It does not identify J. Jager, New Kwality Cafe, a proprietor, property ownership, or a legal entity. Same-address/name resemblance to existing J. Jager/New Kwality evidence is retained as a research bridge only. SHA-256 `{by['jagers1940']['sha256']}`."""
)

# New evidence records.
append_once(
    "evidence/evidence-register.md",
    "## E-171 — Chicago Store fire and George Harding building ownership, December 1913",
    """## E-171 — Chicago Store fire and George Harding building ownership, December 1913
Type: Primary newspaper fire report plus exact-address cross-source comparison  
Sources: `S-192`, `S-032`  
Claims: The visually verified 25 December 1913 *Oregon City Courier* front page reports that the Chicago clothing store on Main Street south of the postoffice was gutted by fire and explicitly states that **the building was owned by George Harding**. The fire report itself does not print 505 Main. Independent exact-address Chicago Store advertising at **505 Main** in 1911 and January 1913 supports a **strong cross-source inference** that the reported burned Chicago Store premises were the documented 505 Main premises. This is not deed-level fee-title proof and does not establish continuity with the surviving 505 building.  
Confidence: **Very High** for visually verified fire/report/building-owner wording; **Strong inference** for the 505 mapping; property legal description and surviving-building continuity unresolved.  
Related record: `evidence/E-171-1913-chicago-store-fire-george-harding.md`"""
)
append_once(
    "evidence/evidence-register.md",
    "## E-172 — JAGERS advertised at 503 Main, 18 October 1940",
    """## E-172 — JAGERS advertised at 503 Main, 18 October 1940
Type: Primary newspaper advertisement  
Sources: `S-193`  
Claims: A visually verified 18 October 1940 *Amplifier* advertisement directly prints **JAGERS** and **503 Main St. Oregon City**, describing it as a “Cozy place for A Tasty Pickup.” This establishes the printed business/trade style, exact address, and refreshment-oriented advertising context on that date. The ad does not print J. Jager, New Kwality Cafe, proprietor, ownership, or legal-entity wording. The same-address/name resemblance to P-003 / BUS-002 is a research bridge only and is not an identity or renaming conclusion.  
Confidence: **Very High** for the printed JAGERS name/address/ad wording; relationship to J. Jager / New Kwality Cafe unresolved.  
Related record: `evidence/E-172-1940-jagers-503-main.md`"""
)
write("evidence/E-171-1913-chicago-store-fire-george-harding.md", """# E-171 — Chicago Store fire and George Harding building ownership, December 1913

Type: Primary newspaper fire report plus exact-address cross-source comparison.  
Sources: `S-192`, `S-032`.  
Related business: `BUS-011`; person: `P-001`; building context: `B-002`.

The visually verified 25 December 1913 *Oregon City Courier* front page reports that the **Chicago clothing store on Main Street, south of the postoffice, was gutted by fire** on the preceding Saturday night. It explicitly states that **the building was owned by George Harding**.

The fire article itself does **not** print `505 Main`. Independent exact-address Chicago Store advertisements place the business at **505 Main** in 1911 and again in January 1913. The combined evidence therefore supports a **strong cross-source inference** that the burned Chicago Store premises were the documented 505 Main premises.

This is not a deed, does not establish the legal description of the land, and does not prove that the fire-damaged structure was the surviving 505 building or that no intervening move occurred after January 1913. The key upgrade supplied by `S-192` is that the George Harding building-owner wording is now **VISUALLY VERIFIED**, rather than OCR/TEXT ONLY.
""")
write("evidence/E-172-1940-jagers-503-main.md", """# E-172 — JAGERS advertised at 503 Main, 18 October 1940

Type: Primary newspaper advertisement.  
Source: `S-193`.  
Related business: `BUS-084`; building: `B-001`.

The page-three advertisement in the 18 October 1940 *Amplifier* directly reads:

**JAGERS**  
**Cozy place for A Tasty Pickup**  
**503 Main St. Oregon City**

This directly establishes an advertised business/trade style **JAGERS at 503 Main** on that date and a food/refreshment-oriented advertising context.

The ad does **not** name `J. Jager`, `New Kwality Cafe`, a proprietor, a legal entity, or property ownership. Existing matchbook evidence separately identifies J. Jager as proprietor of New Kwality Cafe at the same address. That overlap makes a relationship worth testing, but it is not enough to merge `BUS-084` with `BUS-002` or to assign the 1940 advertisement to `P-003`.
""")

# New business record.
append_once(
    "businesses/business-index.md",
    "| BUS-084 | [JAGERS](jagers.md) | 503 Main |",
    """| BUS-084 | [JAGERS](jagers.md) | 503 Main | Exact 18 Oct. 1940 *Amplifier* ad: “Cozy place for A Tasty Pickup.” Same-address/name relationship to J. Jager / New Kwality Cafe remains unresolved; not merged. `E-172` / `S-193`. |"""
)
write("businesses/jagers.md", """# JAGERS

Business ID: `BUS-084`. Address: **503 Main Street** (`B-001`).

A visually verified advertisement in the **18 October 1940** *Amplifier* prints **JAGERS**, describes it as a **“Cozy place for A Tasty Pickup,”** and gives **503 Main St., Oregon City** (`E-172` / `S-193`).

This is a direct dated business-name/address anchor. The advertisement does **not** name J. Jager, New Kwality Cafe, a proprietor, a legal entity, or property ownership.

The archive already contains undated matchbook evidence identifying **J. Jager** as proprietor of **New Kwality Cafe at 503 Main** (`P-003`, `BUS-002`, `E-002`). The same address and Jager/JAGERS name resemblance are meaningful research clues, but they are not enough to equate the businesses or establish a name-change sequence. Keep `BUS-084` distinct until a directory, license, advertisement, sale/rename notice, or other direct bridge is recovered.
""")

# YAML source mirrors.
append_once(
    "database/sources.yml",
    "  - id: S-192\n",
    f"""  - id: S-192
    name: Oregon City Courier, 25 December 1913, Chicago Store fire and George Harding building-owner statement
    url: {by['chicago1913']['url']}
    notes: >-
      Visually verified front-page fire report. Chicago clothing store on Main south of the postoffice was gutted; the report explicitly says the building was owned by George Harding. Article does not print 505. Repository PDF {by['chicago1913']['actual_path']}; SHA-256 {by['chicago1913']['sha256']}. Related evidence E-171 and E-108."""
)
append_once(
    "database/sources.yml",
    "  - id: S-193\n",
    f"""  - id: S-193
    name: The Amplifier, 18 October 1940, JAGERS at 503 Main
    url: {by['jagers1940']['url']}
    notes: >-
      Visually verified advertisement directly prints JAGERS, “Cozy place for A Tasty Pickup,” 503 Main St., Oregon City. Does not print J. Jager or New Kwality Cafe. Repository PDF {by['jagers1940']['actual_path']}; SHA-256 {by['jagers1940']['sha256']}. Related evidence E-172."""
)

# YAML evidence mirrors.
append_once(
    "database/evidence.yml",
    "  - id: E-171\n",
    """  - id: E-171
    name: Chicago Store fire and George Harding building ownership, December 1913
    type: Primary newspaper fire report plus exact-address cross-source comparison
    claims:
      - The visually verified 25 December 1913 Courier says the Chicago clothing store on Main Street south of the postoffice was gutted by fire and explicitly says the building was owned by George Harding.
      - The fire article itself does not print 505 Main; independent exact Chicago Store advertising at 505 Main supports a strong cross-source 505 mapping, not deed-level proof.
      - The evidence does not establish surviving-building continuity or the legal land description.
    confidence: Very High for the visually verified fire/report/building-owner wording; Strong inference for the 505 mapping; legal title and surviving-building continuity unresolved.
    related_sources: [S-192, S-032]
    related_people: [P-001]
    related_businesses: [BUS-011]
    related_buildings: [B-002]
    repository_file: evidence/E-171-1913-chicago-store-fire-george-harding.md"""
)
append_once(
    "database/evidence.yml",
    "  - id: E-172\n",
    """  - id: E-172
    name: JAGERS advertised at 503 Main, 18 October 1940
    type: Primary newspaper advertisement
    claims:
      - The visually verified 18 October 1940 Amplifier ad directly prints JAGERS, “Cozy place for A Tasty Pickup,” and 503 Main St., Oregon City.
      - The ad does not name J. Jager, New Kwality Cafe, a proprietor, property ownership, or a legal entity.
      - Same-address/name resemblance to existing J. Jager / New Kwality evidence is a research bridge only, not a proved identity or rename.
    confidence: Very High for printed business style/address/ad wording; relationship to J. Jager / New Kwality Cafe unresolved.
    related_sources: [S-193]
    related_businesses: [BUS-084]
    related_buildings: [B-001]
    repository_file: evidence/E-172-1940-jagers-503-main.md"""
)

# YAML business mirror.
append_once(
    "database/businesses.yml",
    "  - id: BUS-084\n",
    """  - id: BUS-084
    name: JAGERS
    repository_file: businesses/jagers.md
    address: 503 Main
    notes: 18 Oct. 1940 Amplifier ad says JAGERS, “Cozy place for A Tasty Pickup,” at exact 503 Main. The ad does not name J. Jager or New Kwality Cafe; keep separate from BUS-002 pending a direct bridge.
    related_buildings: [B-001]
    related_evidence: [E-172]
    related_sources: [S-193]"""
)

# Timeline YAML.
append_once(
    "database/timeline.yml",
    "  - id: T-063\n",
    """  - id: T-063
    date: 20 December 1913 (reported 25 December)
    summary: Oregon City Courier reports the Chicago clothing store on Main Street south of the postoffice was gutted by fire and explicitly says the building was owned by George Harding. Exact Chicago Store advertising supports a strong 505 Main mapping, but the fire article itself does not print 505.
    confidence: Very High for visually verified fire/report/building-owner wording; Strong cross-source inference for 505; deed and surviving-building continuity unresolved.
    related_evidence: [E-171]
    related_sources: [S-192, S-032]
    related_people: [P-001]
    related_businesses: [BUS-011]
    related_buildings: [B-002]"""
)
append_once(
    "database/timeline.yml",
    "  - id: T-064\n",
    """  - id: T-064
    date: 18 October 1940
    summary: The Amplifier advertises JAGERS as a “Cozy place for A Tasty Pickup” at exact 503 Main St., Oregon City.
    confidence: Very High for visually verified printed name/address/ad wording; relationship to J. Jager / New Kwality Cafe unresolved.
    related_evidence: [E-172]
    related_sources: [S-193]
    related_businesses: [BUS-084]
    related_buildings: [B-001]"""
)

# Upgrade the old 1913 OCR-only capture now that the exact page scan is supplied and preserved.
write("evidence/source-captures/1913-chicago-store-fire-george-harding-owner.md", f"""# December 1913 Chicago Store fire — George Harding building-owner lead for 505 Main

Status: **VISUALLY VERIFIED PRIMARY NEWSPAPER PAGE; EXACT 505 MAPPING REMAINS A STRONG CROSS-SOURCE INFERENCE**

The *Oregon City Courier* front page for **25 December 1913** has now been physically preserved and visually inspected.

Source: {by['chicago1913']['url']}  
Repository PDF: `{by['chicago1913']['actual_path']}`  
Registered source/evidence: `S-192` / `E-171`.

## What the report says

Under **THREE BIG FIRES IN THREE NIGHTS**, the article says the **Chicago clothing store on Main street, south of the postoffice, was gutted by fire** on the preceding Saturday night. It says the interior was eaten by flames, the goods were ruined, the stock was reportedly fully insured, and explicitly states:

**The building was owned by George Harding.**

This wording is now **VISUALLY VERIFIED**, superseding the earlier OCR/TEXT-ONLY status.

## Relationship to 505 Main

Independent primary advertising places the **Chicago Store at 505 Main Street** in 1911 and again in January 1913 (`S-032` / `E-026`). The fire article itself does **not** print `505 Main`; it gives Main Street south of the postoffice.

Accordingly:

- **Very High / visually verified:** Chicago Store fire and the statement that George Harding owned the building.
- **Strong cross-source inference:** the burned Chicago Store premises were the independently documented 505 Main premises.
- **Unresolved:** deed/legal description, exact land title, any post-January move before the fire, and continuity with the surviving 505 structure.

## Why this matters

The result upgrades an old retrieval gap without overclaiming the parcel:
- 1911–Jan. 1913 — Chicago Store directly documented at **505 Main**;
- 20 Dec. 1913 (reported 25 Dec.) — Chicago clothing store gutted by fire; **building owned by George Harding**;
- 1914–1917 — occupant/rebuild/lease history remains incomplete;
- Oct. 1918 — Wolf & Miller directly at **505 Main**.

## Remaining research targets

1. Search late Dec. 1913–1914 for repairs, rebuilding, insurance, leases, reopening, or relocation after the fire.
2. Recover deed/tax/assessment evidence tying George Harding's building ownership to a legal description corresponding to the 505 premises.
3. Determine the Chicago Store's post-fire business disposition.
4. Identify intervening 1914–1917 occupants and any structural work.

The former task “visually inspect the 25 December 1913 front page” is **RESOLVED** by `S-192`; it should not remain a retrieval gap.
""")

# Upgrade stale OCR-only language in related 1913/1922 bridge files, without changing the Strong inference classification.
replacements = [
    (
        "evidence/source-captures/1913-building-vs-land-ownership-caution-for-1922-wolf-search.md",
        "The 25 December 1913 *Oregon City Courier* primary OCR/text report says the Chicago clothing-store building was owned by **George Harding**. The page image has not yet been visually certified, so that owner wording remains **primary OCR/text-only**.",
        "The 25 December 1913 *Oregon City Courier* page is now physically preserved and **VISUALLY VERIFIED** (`S-192` / `E-171`): it says the Chicago clothing-store building was owned by **George Harding**. The fire article itself still does not print 505 Main, so the Harding↔505 connection remains a **strong cross-source inference** rather than a direct exact-address or deed statement."
    ),
    (
        "evidence/source-captures/task7-address-to-property-bridge-2026-08-26.md",
        "Classification: **STRONG MULTI-SOURCE INFERENCE**; December 1913 owner wording remains **OCR/TEXT-ONLY** pending visual certification.",
        "Classification: **STRONG MULTI-SOURCE INFERENCE** for Harding↔505; the December 1913 Chicago Store fire/building-owner wording is now **VISUALLY VERIFIED** by `S-192` / `E-171`, but the fire article itself does not print 505."
    ),
    (
        "evidence/E-108-block4-harding-address-property-bridge.md",
        "A 25 December 1913 *Oregon City Courier* primary OCR/text report says the Chicago clothing-store building was owned by **George Harding**. Because that page image has not yet been visually certified, the Harding-building wording remains **primary OCR/text-only**, while the combined Harding↔505 connection is a **strong multi-source inference**.",
        "A 25 December 1913 *Oregon City Courier* page is now physically preserved and **VISUALLY VERIFIED** (`S-192` / `E-171`): it says the Chicago clothing-store building was owned by **George Harding**. The fire article itself does not print 505 Main; the combined Harding↔505 connection therefore remains a **strong multi-source inference** rather than direct exact-address or deed proof."
    ),
]
for path, old, new in replacements:
    replace_once(path, old, new, required=False)

# Remove/resolve stale visual-certification target if present.
replace_all(
    "evidence/source-captures/1913-building-vs-land-ownership-caution-for-1922-wolf-search.md",
    "5. Visual certification of the 25 December 1913 Harding-owner article.",
    "5. **RESOLVED 2 Sep. 2026:** `S-192` visually certifies the 25 December 1913 Harding-owner article; retain only the exact-address/deed mapping questions."
)

# Replace E-108 Markdown section to sync its confidence statement and cross-reference E-171.
e108_text = read("evidence/evidence-register.md")
pattern = re.compile(r"(?ms)^## E-108 —.*?(?=^## E-|\Z)")
m = pattern.search(e108_text)
if not m:
    raise SystemExit("Missing E-108 evidence register section")
block = m.group(0)
block2 = block.replace(
    "with the December 1913 owner wording still primary OCR/text-only",
    "with the December 1913 building-owner wording now visually verified by `S-192` / `E-171`, while the fire article itself does not print 505"
)
block2 = block2.replace(
    "Related record: `evidence/E-108-block4-harding-address-property-bridge.md`",
    "Related record: `evidence/E-108-block4-harding-address-property-bridge.md`; visual-owner upgrade: `E-171` / `S-192`"
)
if block2 != block:
    write("evidence/evidence-register.md", e108_text[:m.start()] + block2 + e108_text[m.end():])

# Replace E-108 YAML phrases and attach E-171/S-192 as cross-reference if not already present.
e108 = read("database/evidence.yml")
pattern = re.compile(r"(?ms)^  - id: E-108\n.*?(?=^  - id: |\Z)")
m = pattern.search(e108)
if not m:
    raise SystemExit("Missing E-108 YAML record")
block = m.group(0)
block2 = block.replace(
    "Chicago Store exact-address evidence at 505 plus the December 1913 primary OCR/text report naming George Harding as building owner creates a strong Harding-to-505 bridge, pending visual certification of that owner wording.",
    "Chicago Store exact-address evidence at 505 plus the visually verified 25 December 1913 fire report naming George Harding as building owner creates a strong Harding-to-505 bridge; the fire report itself does not print 505, so exact-address/deed proof remains unresolved."
)
block2 = block2.replace(
    "Strong multi-source inference for Harding↔505 with the December 1913 owner wording still primary OCR/text-only",
    "Strong multi-source inference for Harding↔505 with the December 1913 owner wording now visually verified; the fire article itself does not print 505"
)
write("database/evidence.yml", e108[:m.start()] + block2 + e108[m.end():])

# Business and person profiles.
append_once(
    "businesses/chicago-store.md",
    "## 25 December 1913 fire page now visually verified",
    f"""## 25 December 1913 fire page now visually verified
The exact *Oregon City Courier* front page is now preserved at `{by['chicago1913']['actual_path']}` (`S-192` / `E-171`). It directly says the Chicago clothing-store building was **owned by George Harding**. The article gives Main Street south of the postoffice, not 505; the 505 identification remains a strong cross-source inference from the store's independent exact-address advertising, not a deed or a direct number printed in the fire report."""
)
append_once(
    "people/profiles/j-jager.md",
    "## 18 October 1940 JAGERS same-address lead",
    """## 18 October 1940 JAGERS same-address lead
A visually verified *Amplifier* advertisement (`S-193` / `E-172`) prints **JAGERS** at **503 Main St.** and calls it a “Cozy place for A Tasty Pickup.” The ad does **not** name J. Jager or New Kwality Cafe. Because P-003 is independently tied to New Kwality Cafe at the same exact address, this is an important identity/name-change lead, but it is not yet sufficient to merge P-003 with the 1940 `JAGERS` business record (`BUS-084`)."""
)
append_once(
    "businesses/kwality-cafe.md",
    "## 18 October 1940 JAGERS exact-address bridge",
    """## 18 October 1940 JAGERS exact-address bridge
`S-193` / `E-172` adds a dated **18 October 1940** advertisement for **JAGERS at 503 Main**, describing a “Cozy place for A Tasty Pickup.” This is highly relevant to the later/undated J. Jager and New Kwality Cafe evidence at 503, but the 1940 ad does not print `J. Jager`, `New Kwality Cafe`, or a name-change statement. The archive therefore retains `JAGERS` as separate `BUS-084` pending a direct continuity source."""
)

# Building files.
append_once(
    "buildings/503-main.md",
    "## 18 October 1940 JAGERS exact-address advertisement",
    """## 18 October 1940 JAGERS exact-address advertisement
A visually verified *Amplifier* page (`S-193` / `E-172`) directly advertises **JAGERS at 503 Main St., Oregon City** with the phrase “Cozy place for A Tasty Pickup.” This supplies a dated 1940 occupant/business-name anchor between the 1937 generic KWALITY sale advertisement and the City's 1947 Kwality Cafe directory synthesis. It does not by itself identify J. Jager or establish that JAGERS and New Kwality Cafe were the same business."""
)
append_once(
    "buildings/505-main.md",
    "## December 1913 Chicago Store fire — visual owner-wording upgrade",
    """## December 1913 Chicago Store fire — visual owner-wording upgrade
The exact 25 December 1913 *Oregon City Courier* front page is now visually verified (`S-192` / `E-171`). It reports the Chicago clothing store on Main Street south of the postoffice gutted by fire and says **the building was owned by George Harding**. The article itself does not print 505 Main. Because the Chicago Store is independently documented at 505 Main, the address mapping is a strong cross-source inference, not direct exact-number wording from the fire report or deed-level title proof."""
)

# Unified timelines.
old505 = "| Dec. 1913 | Fire in Chicago Store building; premises strongly associated with George Harding. | Strong inference, not deed/surviving-building proof. | Chicago Store fire capture |"
new505 = "| 20 Dec. 1913 (reported 25 Dec.) | **Chicago Store** on Main south of the postoffice gutted by fire; report says **the building was owned by George Harding**. | **Very High, visually verified** for fire/report/owner wording; **Strong cross-source inference** this was the store's independently documented 505 Main premises. Article itself does not print 505; deed/surviving-building continuity unproved. | `BUS-011`; `P-001`; `E-171`; `S-192` |"
replace_once("timelines/505-main.md", old505, new505, required=False)

t503 = read("timelines/503-main.md")
row1940 = "| 18 Oct. 1940 | **JAGERS** — “Cozy place for A Tasty Pickup” — at **503 Main St.** | **Exact, visually verified primary ad** for printed business style/address. Ad does not itself name J. Jager or New Kwality Cafe; relationship remains open. | `BUS-084`; `E-172`; `S-193` |\n"
if row1940 not in t503:
    anchor = "| 1947 | City synthesis reports **Kwality Cafe** at 503."
    idx = t503.find(anchor)
    if idx < 0:
        raise SystemExit("Could not find 1947 Kwality row in timelines/503-main.md")
    t503 = t503[:idx] + row1940 + t503[idx:]
t503 = t503.replace(
    "Sequence (chronology only): Brightbill → Smith → Hylton → unnamed 1925 restaurant → Kwality / New Kwality / Larry's Kwality (artifact-name order unresolved) / Flor → Wheel → White Rabbit/Black Ink.",
    "Sequence (chronology only): Brightbill → Smith → Hylton → unnamed 1925 restaurant → Kwality context → **JAGERS (1940; relationship to J. Jager/New Kwality open)** → New Kwality / Larry's Kwality (artifact-name order/dates unresolved) / Flor → Wheel → White Rabbit/Black Ink."
)
write("timelines/503-main.md", t503)

# Master timeline and business timeline.
append_once(
    "timeline.md",
    "## 1940 — JAGERS exact 503 Main advertisement",
    """## 1940 — JAGERS exact 503 Main advertisement
A visually verified **18 October 1940** *Amplifier* advertisement directly prints **JAGERS — 503 Main St., Oregon City**, describing it as a **“Cozy place for A Tasty Pickup”** (`S-193` / `E-172`). This is a dated exact-address business-name anchor for 503. It does not itself identify `J. Jager` or `New Kwality Cafe`; the same-address/name relationship remains a research question and `BUS-084` is kept separate from `BUS-002`."""
)
append_once(
    "timeline.md",
    "### 1913 Chicago Store fire visual-certification update — 2 September 2026",
    """### 1913 Chicago Store fire visual-certification update — 2 September 2026
The 25 December 1913 *Courier* front page is now physically preserved and **VISUALLY VERIFIED** (`S-192` / `E-171`). It says the Chicago clothing store on Main Street south of the postoffice was gutted and **the building was owned by George Harding**. The article itself does not print 505 Main; the 505 mapping remains a strong cross-source inference from independent exact-address Chicago Store advertising."""
)
append_once(
    "registers/business-timeline.md",
    "## 18 October 1940 — JAGERS at 503 Main",
    """## 18 October 1940 — JAGERS at 503 Main
A visually verified *Amplifier* ad places **JAGERS** at **503 Main St.** and calls it a “Cozy place for A Tasty Pickup” (`BUS-084`; `E-172`; `S-193`). The ad does not name J. Jager or New Kwality Cafe, so no business merge/name-change sequence is asserted."""
)
append_once(
    "registers/business-timeline.md",
    "## 20 December 1913 Chicago Store fire — reported 25 December",
    """## 20 December 1913 Chicago Store fire — reported 25 December
The visually verified *Courier* report says the Chicago clothing store on Main south of the postoffice was gutted and **the building was owned by George Harding** (`BUS-011`; `E-171`; `S-192`). Independent exact-address advertising supports a strong 505 Main mapping, but the fire page itself does not print 505 and is not deed evidence."""
)

# Crosswalk, archive index, and research log.
append_once(
    "indexes/id-crosswalk.md",
    "| `S-192` / `E-171` | `BUS-011`; `P-001`; `B-002` |",
    """| `S-192` / `E-171` | `BUS-011`; `P-001`; `B-002` | 25 Dec. 1913 Chicago Store fire page; George Harding building-owner wording visually verified; exact 505 mapping remains cross-source inference. |
| `S-193` / `E-172` | `BUS-084`; `B-001` | 18 Oct. 1940 JAGERS exact 503 Main advertisement; J. Jager/New Kwality relationship unresolved. |"""
)
append_once(
    "ARCHIVE_INDEX.md",
    "## Steward uploads — 1907–1940 Justin/Chicago fire/Fifth-Main fire/JAGERS reconciliation",
    """## Steward uploads — 1907–1940 Justin/Chicago fire/Fifth-Main fire/JAGERS reconciliation
[Reconciliation audit](evidence/source-captures/1907-1940-steward-upload-reconciliation-2026-09-02.md) accounts for five supplied PDFs by SHA-256. The 1907 Justin & Hitchman (`S-136`), 1908 Justin & Hitchman/Surber (`S-137`), and 20 Jul. 1922 Fifth/Main fire (`S-117`) pages were already preserved byte-for-byte and were not duplicated. New exact page files are the **25 Dec. 1913 Chicago Store fire / George Harding building-owner page** (`S-192` / `E-171`) and **18 Oct. 1940 JAGERS at 503 Main** (`S-193` / `E-172`, `BUS-084`). The 1913 page resolves the prior visual-certification gap but does not turn the cross-source 505 mapping into deed proof; the 1940 JAGERS ad is not automatically merged with J. Jager/New Kwality Cafe."""
)
append_once(
    "registers/research-log.md",
    "### 2026-09-02 — Reconcile Justin/Hitchman, 1913 Chicago fire, 1922 fire, and 1940 JAGERS uploads",
    """### 2026-09-02 — Reconcile Justin/Hitchman, 1913 Chicago fire, 1922 fire, and 1940 JAGERS uploads
- Reconciled five steward-supplied page PDFs by exact SHA-256.
- Deduplicated the already-preserved 13 Dec. 1907 (`S-136`), 18 Sep. 1908 (`S-137`), and 20 Jul. 1922 (`S-117`) pages without new source IDs.
- Preserved and visually certified the 25 Dec. 1913 *Courier* Chicago Store fire page as `S-192` / `E-171`; the report directly names George Harding as building owner, while 505 remains a cross-source inference.
- Preserved the 18 Oct. 1940 *Amplifier* JAGERS ad as `S-193` / `E-172` and created separate `BUS-084`; direct exact 503 Main, but no automatic J. Jager/New Kwality merge.
- Permanent audit: `evidence/source-captures/1907-1940-steward-upload-reconciliation-2026-09-02.md`. No annual completion-status change."""
)

print("Reconciliation complete.")
for item in PAGES:
    print(f"{item['key']}: {item['handling']} -> {item['actual_path']}")
