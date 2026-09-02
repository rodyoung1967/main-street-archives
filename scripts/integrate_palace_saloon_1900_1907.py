from pathlib import Path
import hashlib, json

ROOT = Path(__file__).resolve().parents[1]

FILES = [
    {
        "source_id":"S-174","evidence_id":"E-154",
        "repo_path":"newspapers/oregon-city-courier-herald/1900-04-06-page-5-palace-saloon-albert-knapp-purchase.pdf",
        "url":"https://oregonnews.uoregon.edu/lccn/sn00063697/1900-04-06/ed-1/seq-5.pdf",
        "uploaded_name":"Palace Saloon (sale of) Oregon City Courier Herald Apr 1900 page 3(2).pdf",
        "uploaded_sha256":"412fd48faf5a832759a22983d685d365acb72a9cdc85ae51f7c90d880e05f5e0",
        "uploaded_bytes":631511,
    },
    {
        "source_id":"S-175","evidence_id":"E-155",
        "repo_path":"newspapers/oregon-city-courier/1905-02-24-page-5-palace-saloon-knapp-surber-sale.pdf",
        "url":"https://oregonnews.uoregon.edu/lccn/sn00063698/1905-02-24/ed-1/seq-5.pdf",
        "uploaded_name":"Palace Saloon (sale of) Oregon City Courier  Feb 1905(2).pdf",
        "uploaded_sha256":"cec0e28008bf28a16ae87a0daef601551b5e3ac4f9fa8a9e657552d9192ca8fb",
        "uploaded_bytes":538495,
    },
    {
        "source_id":"S-176","evidence_id":"E-156",
        "repo_path":"newspapers/oregon-city-enterprise/1907-07-19-page-1-palace-saloon-fifth-street.pdf",
        "url":"https://oregonnews.uoregon.edu/lccn/sn00063700/1907-07-19/ed-1/seq-1.pdf",
        "uploaded_name":"Palace Saloon 1907(2).pdf",
        "uploaded_sha256":"072ef700c3573eded5aa4f82cf2f3f400f537b6d764cb444bf3a4cce8548c3bc",
        "uploaded_bytes":473270,
    },
]

def read(path):
    return (ROOT / path).read_text(encoding="utf-8")

def write(path, text):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")

def append_once(path, marker, block):
    text = read(path)
    if marker in text:
        return
    if not text.endswith("\n"):
        text += "\n"
    write(path, text + "\n" + block.strip() + "\n")

def replace_once(path, old, new):
    text = read(path)
    if new in text:
        return
    if old not in text:
        raise RuntimeError(f"Anchor not found in {path}: {old[:120]!r}")
    write(path, text.replace(old, new, 1))

def insert_before(path, anchor, marker, block):
    text = read(path)
    if marker in text:
        return
    if anchor not in text:
        raise RuntimeError(f"Anchor not found in {path}: {anchor[:120]!r}")
    write(path, text.replace(anchor, block.rstrip() + "\n" + anchor, 1))

def file_meta(item):
    p = ROOT / item["repo_path"]
    b = p.read_bytes()
    if not b.startswith(b"%PDF"):
        raise RuntimeError(f"Downloaded file is not PDF: {item['repo_path']}")
    return len(b), hashlib.sha256(b).hexdigest()

for token, path in [
    ("S-174", "evidence/source-register.md"),
    ("S-175", "evidence/source-register.md"),
    ("S-176", "evidence/source-register.md"),
    ("E-154", "evidence/evidence-register.md"),
    ("E-155", "evidence/evidence-register.md"),
    ("E-156", "evidence/evidence-register.md"),
    ("P-099", "people/people-index.md"),
]:
    if token in read(path):
        raise RuntimeError(f"{token} already exists in {path}; resync and allocate new IDs")

for item in FILES:
    size, sha = file_meta(item)
    item["repo_bytes"] = size
    item["repo_sha256"] = sha

capture_path = "evidence/source-captures/1900-1907-palace-saloon-sale-location-supplement-2026-09-01.md"
capture = f"""# Palace Saloon sale and location supplement, 1900–1907

Review date: **1 September 2026**.

Status: **THREE PROJECT-STEWARD NEWSPAPER PAGE UPLOADS VISUALLY VERIFIED; REPOSITORY COPIES PRESERVED FROM THE CANONICAL OREGON DIGITAL ISSUE/PAGE ROUTES.**

The historical claims below were taken from visual inspection of the supplied page scans, not from filenames or OCR alone.

## S-174 / E-154 — 6 April 1900 Oregon City Courier-Herald, p. 5

The local-news item says **Albert Knapp** purchased **the Palace saloon**, described as **opposite the post-office on the corner**, and intended to improve and fit it up in first-class manner while carrying wines, liquors, and cigars.

What this proves:
- Albert Knapp was reported as purchasing the Palace Saloon by 6 April 1900;
- the Palace was then described by relative location as opposite the post office and on a corner;
- the article reports a planned improvement/refit after purchase.

Limits:
- no street number is printed;
- the item does not identify which corner by street names;
- the improvement language does not prove a particular structural alteration or construction date;
- business purchase is not real-estate title.

Repository file: `{FILES[0]["repo_path"]}`
Canonical URL: {FILES[0]["url"]}
Original uploaded filename: `{FILES[0]["uploaded_name"]}`. The filename says “page 3,” but the supplied scan/canonical issue route is page/image 5.
Uploaded SHA-256: `{FILES[0]["uploaded_sha256"]}` ({FILES[0]["uploaded_bytes"]} bytes).
Repository SHA-256: `{FILES[0]["repo_sha256"]}` ({FILES[0]["repo_bytes"]} bytes).

## S-175 / E-155 — 24 February 1905 Oregon City Courier, p. 5

The local-notes item states: **“The Palace saloon has been sold by A. Knapp to A. J. Surber, formerly of Kalama, Wash.”**

What this proves:
- a reported Palace Saloon business sale from A. Knapp to A. J. Surber by 24 February 1905;
- A. J. Surber is directly connected to the Palace Saloon trade name in 1905;
- the item identifies Surber as formerly of Kalama, Washington.

Limits:
- no numbered address or street intersection is printed;
- the article does not establish real-estate ownership, license transfer/grant details, or uninterrupted operation after the sale;
- the later 1907 exact-501 Surber license premises cannot automatically be declared the same Palace room without an address bridge.

Repository file: `{FILES[1]["repo_path"]}`
Canonical URL: {FILES[1]["url"]}
Original uploaded filename: `{FILES[1]["uploaded_name"]}`
Uploaded SHA-256: `{FILES[1]["uploaded_sha256"]}` ({FILES[1]["uploaded_bytes"]} bytes).
Repository SHA-256: `{FILES[1]["repo_sha256"]}` ({FILES[1]["repo_bytes"]} bytes).

## S-176 / E-156 — 19 July 1907 Oregon City Enterprise, p. 1

The item **“IN BURNS COLLEGE”** reports that Joe Kramer sat down **“in the rear of the Palace saloon on Fifth street”** before being taken into custody.

What this proves:
- by 19 July 1907 the Palace Saloon was described as **on Fifth Street**;
- the report supplies a direct street-location clue independent of the May 1907 citywide saloon list.

Limits:
- no street number or proprietor is printed;
- “on Fifth street” is not silently converted to 501 Main;
- this page does not prove that A. J. Surber still operated the Palace in July 1907;
- it does not by itself prove that Surber's October 1907 No. 501 liquor premises were the Palace Saloon.

Repository file: `{FILES[2]["repo_path"]}`
Canonical URL: {FILES[2]["url"]}
Original uploaded filename: `{FILES[2]["uploaded_name"]}`
Uploaded SHA-256: `{FILES[2]["uploaded_sha256"]}` ({FILES[2]["uploaded_bytes"]} bytes).
Repository SHA-256: `{FILES[2]["repo_sha256"]}` ({FILES[2]["repo_bytes"]} bytes).

## Chronology effect

The new sequence is now:

- **6 Apr. 1900:** Albert Knapp reported purchasing Palace Saloon, opposite the post office on a corner.
- **24 Feb. 1905:** A. Knapp reported selling Palace Saloon to A. J. Surber.
- **24 May 1907:** Palace trade name appears among Oregon City's sixteen saloons; address/operator omitted (`E-151`).
- **19 Jul. 1907:** Palace Saloon described as on Fifth Street.
- **4 Oct. 1907:** A. J. Surber independently appears at No. 501, Main/Fifth, but that notice does not print the Palace name (`E-121`).
- **17 Sep. 1909:** Ralph O. Smith at Palace Saloon, corner Main/Fifth (`E-152`).
- **19 Mar. 1912:** Joe Wilson's Palace Saloon at exact 501 Main (`E-104`).
- **20 Jun. 1912:** Joseph Wilson at The Palace Saloon, Fifth/Main (`E-153`).

The 1905 sale **does directly establish Surber's Palace Saloon relationship**, superseding the earlier statement that no Palace trade-name connection to Surber was known. It still does not prove uninterrupted Surber operation to October 1907 or prove that the later exact-501 room was the same room.

## Binary provenance

The supplied uploads were the copies visually inspected. The repository copies were fetched from the canonical Oregon Digital issue/page URLs during integration. Uploaded and repository hashes are recorded separately above. If a repository PDF derivative differs byte-for-byte from the supplied PDF, the difference is treated as a binary-derivative distinction unless the page content itself differs.
"""
write(capture_path, capture)

manifest = {
    "review_date":"2026-09-01",
    "status":"VISUALLY VERIFIED supplied scans; canonical issue/page PDFs preserved",
    "files": FILES,
}
write("evidence/source-captures/1900-1907-palace-saloon-sale-location-manifest.json", json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")

source_block = f"""
## S-174 — Oregon City Courier-Herald, 6 April 1900, p. 5 — Albert Knapp purchases Palace Saloon
Canonical URL: {FILES[0]["url"]}
Repository file: `{FILES[0]["repo_path"]}`
Original uploaded filename: `{FILES[0]["uploaded_name"]}` (filename page number differs from the verified issue/page route).
Type: Primary newspaper / business-sale and relative-location evidence.
Related evidence: `E-154`
Notes: Visually verified supplied scan reports Albert Knapp purchased the Palace saloon, opposite the post office on the corner, and planned to improve/refit it. No street number, legal title, or completed construction is established. Uploaded SHA-256 `{FILES[0]["uploaded_sha256"]}`; repository SHA-256 `{FILES[0]["repo_sha256"]}`.

## S-175 — Oregon City Courier, 24 February 1905, p. 5 — Palace Saloon sale from A. Knapp to A. J. Surber
Canonical URL: {FILES[1]["url"]}
Repository file: `{FILES[1]["repo_path"]}`
Original uploaded filename: `{FILES[1]["uploaded_name"]}`
Type: Primary newspaper / reported business-sale evidence.
Related evidence: `E-155`
Notes: Visually verified page directly reports that A. Knapp sold the Palace saloon to A. J. Surber, formerly of Kalama, Washington. No numbered address, deed/title, or license-grant record is printed. Uploaded SHA-256 `{FILES[1]["uploaded_sha256"]}`; repository SHA-256 `{FILES[1]["repo_sha256"]}`.

## S-176 — Oregon City Enterprise, 19 July 1907, p. 1 — Palace Saloon on Fifth Street
Canonical URL: {FILES[2]["url"]}
Repository file: `{FILES[2]["repo_path"]}`
Original uploaded filename: `{FILES[2]["uploaded_name"]}`
Type: Primary newspaper / business-location evidence.
Related evidence: `E-156`
Notes: Visually verified item says Joe Kramer sat in the rear of the Palace saloon on Fifth Street. It supplies a Fifth Street location clue but no number or proprietor and is not automatically normalized to 501 Main. Uploaded SHA-256 `{FILES[2]["uploaded_sha256"]}`; repository SHA-256 `{FILES[2]["repo_sha256"]}`.
"""
append_once("evidence/source-register.md", "## S-174 —", source_block)

evidence_block = """
## E-154 — Albert Knapp reported purchase of Palace Saloon, 6 April 1900
Type: Primary newspaper / reported business purchase and relative-location evidence
Date: 6 April 1900
Sources: `S-174`
Related record: `evidence/E-154-1900-palace-saloon-albert-knapp-purchase.md`
Claims:
- The *Oregon City Courier-Herald* reports that Albert Knapp purchased the Palace saloon.
- The Palace is described as opposite the post office and on a corner.
- Knapp intended to improve and fit up the saloon in first-class manner.
Limits:
- No numbered address or named street corner is printed.
- A business purchase is not real-estate title, and planned improvements are not proof of a completed structural project.
Confidence: Very High for the printed report; unresolved for precise address, title, and scope/completion of improvements.

## E-155 — Palace Saloon reported sold from A. Knapp to A. J. Surber, 24 February 1905
Type: Primary newspaper / reported business sale
Date: 24 February 1905
Sources: `S-175`
Related record: `evidence/E-155-1905-palace-saloon-knapp-surber-sale.md`
Claims:
- The *Oregon City Courier* reports that the Palace saloon was sold by A. Knapp to A. J. Surber.
- The item says Surber was formerly of Kalama, Washington.
- This directly establishes A. J. Surber's relationship to the Palace Saloon trade name in February 1905.
Limits:
- No numbered address, deed, real-estate ownership, license transfer/grant, or uninterrupted later operation is proved.
- The later exact-501 Surber liquor premises are not automatically equated with the 1905 Palace room.
Confidence: Very High for the reported sale and parties; unresolved for legal transaction details and later room continuity.

## E-156 — Palace Saloon described on Fifth Street, 19 July 1907
Type: Primary newspaper / business-location evidence
Date: 19 July 1907
Sources: `S-176`
Related record: `evidence/E-156-1907-palace-saloon-fifth-street.md`
Claims:
- The *Oregon City Enterprise* reports that Joe Kramer sat in the rear of the Palace saloon on Fifth Street.
- The wording directly supplies Fifth Street location context for the Palace Saloon by that date.
Limits:
- No street number or proprietor is printed.
- The record does not prove A. J. Surber remained proprietor in July 1907 or that the October 1907 No. 501 Surber premises were the Palace.
Confidence: Very High for the printed Fifth Street wording; unresolved for numbered storefront and operator.
"""
append_once("evidence/evidence-register.md", "## E-154 —", evidence_block)

write("evidence/E-154-1900-palace-saloon-albert-knapp-purchase.md", """# E-154 — Albert Knapp reported purchase of Palace Saloon, 6 April 1900

Source: `S-174`.

The visually verified *Oregon City Courier-Herald* page reports that **Albert Knapp purchased the Palace saloon**, described as **opposite the post office on the corner**, and intended to improve and fit it up in first-class manner.

This is a reported **business purchase and improvement intention**. It is not a deed, numbered-address proof, license grant, or proof of completed construction.

See `evidence/source-captures/1900-1907-palace-saloon-sale-location-supplement-2026-09-01.md`.
""")
write("evidence/E-155-1905-palace-saloon-knapp-surber-sale.md", """# E-155 — Palace Saloon reported sold from A. Knapp to A. J. Surber, 24 February 1905

Source: `S-175`.

The visually verified *Oregon City Courier* page reports: **“The Palace saloon has been sold by A. Knapp to A. J. Surber, formerly of Kalama, Wash.”**

This directly connects **A. J. Surber** to the **Palace Saloon** trade name in February 1905. The page does not print a numbered address, deed/title, or license-transfer details, and it does not by itself prove that Surber's October 1907 No. 501 premises were the same room.

See `evidence/source-captures/1900-1907-palace-saloon-sale-location-supplement-2026-09-01.md`.
""")
write("evidence/E-156-1907-palace-saloon-fifth-street.md", """# E-156 — Palace Saloon described on Fifth Street, 19 July 1907

Source: `S-176`.

The visually verified *Oregon City Enterprise* item says Joe Kramer sat **“in the rear of the Palace saloon on Fifth street.”**

This is direct Fifth Street location context for the Palace Saloon. The page does not print a street number or proprietor, so it is not silently assigned to 501 Main and does not prove Surber's July 1907 operation.

See `evidence/source-captures/1900-1907-palace-saloon-sale-location-supplement-2026-09-01.md`.
""")

old = """Business ID: `BUS-024`. Exact numbered address is directly proved at **501 Main Street (`B-005`) in March 1912**; separate 1909 and June 1912 notices use the **Main/Fifth** intersection.

## Verified chronology

- **24 May 1907 — `E-151` / `S-171`:** an *Oregon City Courier* article listing the city's sixteen saloons includes **The Palace Saloon**. No Palace address or proprietor is printed.
"""
new = """Business ID: `BUS-024`. Exact numbered address is directly proved at **501 Main Street (`B-005`) in March 1912**. Earlier evidence now establishes a reported 1900 Knapp purchase, a 1905 Knapp→Surber Palace sale, and a July 1907 Fifth Street location clue without a numbered storefront.

## Verified chronology

- **6 April 1900 — `E-154` / `S-174`:** **Albert Knapp (`P-099`)** is reported purchasing **the Palace saloon**, described as opposite the post office on a corner, with plans to improve/refit it. No street number, deed, or completed construction is proved.
- **24 February 1905 — `E-155` / `S-175`:** the *Courier* reports **A. Knapp sold the Palace saloon to A. J. Surber (`P-055`)**, formerly of Kalama, Washington. This directly establishes Surber's Palace trade-name relationship on this date but does not prove a numbered address or later continuity.
- **24 May 1907 — `E-151` / `S-171`:** an *Oregon City Courier* article listing the city's sixteen saloons includes **The Palace Saloon**. No Palace address or proprietor is printed.
- **19 July 1907 — `E-156` / `S-176`:** the *Enterprise* describes the **Palace saloon on Fifth Street**. No number or proprietor is printed, so this is not automatically assigned to 501.
"""
replace_once("businesses/palace-saloon.md", old, new)
replace_once("businesses/palace-saloon.md", """The archive does **not** presently prove:
- that the May 1907 Palace Saloon occupied 501 Main;
- that A. J. Surber's October 1907 exact-501 liquor premises were the Palace Saloon;
- a continuous Palace Saloon operation from 1907 through 1912;
- the transfer sequence among Surber, Justin & Hitchman, Ralph O. Smith, E. R. Case, Joe/Joseph Wilson, or Hunsaker & Taylor;
- license grants, real-estate ownership, or building ownership from these application notices.
""", """The archive does **not** presently prove:
- the exact numbered address of the 1900 or 1905 Palace Saloon;
- that A. J. Surber remained the Palace proprietor through July/October 1907;
- that A. J. Surber's October 1907 exact-501 liquor premises were the Palace Saloon, despite the newly established 1905 Palace purchase;
- a continuous Palace Saloon operation from 1900 through 1912;
- the full transfer sequence after Surber among Justin & Hitchman, Ralph O. Smith, E. R. Case, Joe/Joseph Wilson, or Hunsaker & Taylor;
- license grants or real-estate/building ownership from the newspaper business/license reports.
""")
replace_once("businesses/palace-saloon.md", """See the [uploaded-page visual review](../evidence/source-captures/1907-1912-palace-saloon-uploaded-pages-visual-review-2026-09-01.md), [501 Main unified timeline](../timelines/501-main.md), `OQ-032`, and `RL-045`.
""", """See the [1900–1907 sale/location supplement](../evidence/source-captures/1900-1907-palace-saloon-sale-location-supplement-2026-09-01.md), the [1907–1912 uploaded-page visual review](../evidence/source-captures/1907-1912-palace-saloon-uploaded-pages-visual-review-2026-09-01.md), [501 Main unified timeline](../timelines/501-main.md), `OQ-032`, and `RL-045`.
""")

write("people/profiles/a-j-surber.md", """# A. J. Surber

Person ID: `P-055`. Related businesses: `BUS-024`, `BUS-045`.

Roles: reported **Palace Saloon purchaser** in 1905; later retail-liquor renewal applicant.

- **24 February 1905 (`E-155` / `S-175`):** the *Oregon City Courier* reports that **A. Knapp sold the Palace saloon to A. J. Surber**, formerly of Kalama, Washington. This is direct Palace trade-name evidence for Surber on that date.
- **4 October 1907 (`E-121` / `S-135`):** Surber's present retail-liquor place of business is printed as **No. 501, Main/Fifth**.
- **18 September 1908 (`E-121` / `S-137`):** Surber again applies at Main/Fifth, but the number is omitted.

The 1905 sale materially narrows the earlier uncertainty: Surber **was** directly associated with the Palace Saloon in 1905. It still does not prove that he remained Palace proprietor continuously to 1907, or that his October 1907 exact-501 premises were the same Palace room.

See the [1900–1907 Palace supplement](../../evidence/source-captures/1900-1907-palace-saloon-sale-location-supplement-2026-09-01.md) and the [1907–1908 visual review](../../evidence/source-captures/1907-1908-surber-justin-main-visual-review.md). Open question `OQ-032`; lead `RL-045`.
""")
write("businesses/a-j-surber.md", """# A. J. Surber liquor premises / Palace Saloon relationship

Business ID: `BUS-045`. Person: `P-055`. Related trade-name business: `BUS-024`.

- **24 February 1905 (`E-155` / `S-175`):** newspaper reports that **A. Knapp sold the Palace saloon to A. J. Surber**. No numbered address is printed.
- **4 October 1907 (`E-121` / `S-135`):** Surber's present retail-liquor place of business is directly printed as **No. 501, Main/Fifth**; the notice does not use the Palace trade name.
- **18 September 1908 (`E-121` / `S-137`):** Surber applies again at Main/Fifth without a number.

The 1905 source directly proves a Surber/Palace business relationship, superseding the prior statement that no Palace trade-name connection was known. It does **not** prove uninterrupted operation from 1905 to 1907, property title, a license grant, or that the 1905 Palace room and October 1907 No. 501 room were identical.

See the [1900–1907 Palace supplement](../evidence/source-captures/1900-1907-palace-saloon-sale-location-supplement-2026-09-01.md), `OQ-032`, and `RL-045`.
""")
write("people/profiles/albert-knapp.md", """# Albert Knapp / A. Knapp

Person ID: `P-099`. Related business: `BUS-024`.

- **6 April 1900 (`E-154` / `S-174`):** the *Oregon City Courier-Herald* reports **Albert Knapp** purchased the Palace Saloon, opposite the post office on a corner, and planned to improve/refit it.
- **24 February 1905 (`E-155` / `S-175`):** the *Oregon City Courier* reports **A. Knapp** sold the Palace Saloon to A. J. Surber.

The same surname/initial, same business, and seller-after-earlier-purchase chronology make **Albert Knapp = A. Knapp a strong identity inference**, but the 1905 item itself does not spell out the given name. Do not merge this person with other Knapp-named liquor applicants solely by surname.

Business purchase/sale is separate from real-estate title and liquor-license ownership.
""")

append_once("people/people-index.md", "| P-099 |", """## Palace Saloon 1900–1907 supplement

| ID | Name | Role | Notes |
| --- | --- | --- | --- |
| P-099 | [Albert Knapp / A. Knapp](profiles/albert-knapp.md) | Palace Saloon purchaser / later reported seller | 1900 report names Albert Knapp purchasing Palace; 1905 report names A. Knapp selling Palace to A. J. Surber. Same-person identity is a strong inference from same business/chronology, not solely the surname. `E-154`, `E-155`; `S-174`, `S-175`. |
""")

replace_once("businesses/business-index.md", "| BUS-024 | [Palace Saloon](palace-saloon.md) | 501 Main exact Mar. 1912; Main/Fifth in Sep. 1909 & Jun. 1912 | Trade name attested by May 1907; Ralph O. Smith applicant 1909; Joe/Joseph Wilson 1912. Grants, property ownership and operator succession remain unresolved. |", "| BUS-024 | [Palace Saloon](palace-saloon.md) | Opposite post office/on a corner in 1900; Fifth Street Jul. 1907; Main/Fifth Sep. 1909 & Jun. 1912; 501 Main exact Mar. 1912 | 1900 Albert Knapp purchase; 1905 A. Knapp→A. J. Surber sale directly establishes Surber's Palace relationship; May/Jul. 1907 trade-name/location context; Ralph O. Smith 1909; Joe/Joseph Wilson 1912. Exact early number, legal title, grants and uninterrupted succession remain unresolved. |")
replace_once("businesses/business-index.md", "| BUS-045 | [A. J. Surber liquor premises](a-j-surber.md) | 501 Main, at Main/Fifth (4 October 1907); Main/Fifth only (18 September 1908) | 1907 notice prints No. 501 and calls it his present place of business. The 1908 notice requests six months but prints only the intersection. No Palace trade name, grant, title or uninterrupted operation proved. E-121; P-055. |", "| BUS-045 | [A. J. Surber liquor premises](a-j-surber.md) | Palace Saloon relationship in Feb. 1905 (number omitted); 501 Main at Main/Fifth on 4 Oct. 1907; Main/Fifth only 18 Sep. 1908 | 1905 sale directly reports A. Knapp selling Palace Saloon to Surber. 1907 notice prints No. 501 but not Palace trade name; uninterrupted Palace→501 continuity, grant and title remain unproved. `E-155`, `E-121`; `P-055`. |")

insert_before("timelines/501-main.md", "| 24 May 1907 | **Palace Saloon** named among Oregon City's sixteen saloons.", "| 6 Apr. 1900 | **Palace Saloon**", """| 6 Apr. 1900 | **Palace Saloon** reported purchased by Albert Knapp; described opposite the post office on a corner. | **Business/relative-location context only**; no number or named corner, not assigned to 501. | `BUS-024`; `P-099`; `E-154`; `S-174` |
| 24 Feb. 1905 | **Palace Saloon** reported sold by A. Knapp to **A. J. Surber**. | **Direct Surber/Palace relationship**, but no number; does not prove the later exact-501 room is identical. | `BUS-024`; `BUS-045`; `P-055`; `P-099`; `E-155`; `S-175` |
""")
insert_before("timelines/501-main.md", "| 4 Oct. 1907 | A. J. Surber liquor-renewal application", "| 19 Jul. 1907 | Palace Saloon", """| 19 Jul. 1907 | Palace Saloon described **on Fifth Street**. | Street-location context only; no number/proprietor, so not assigned to 501. | `BUS-024`; `E-156`; `S-176` |
""")
replace_once("timelines/501-main.md", "Open: Surber→Palace→Hunsaker succession; Case/Pioneer/Holman/Restaurant exact assignment; 1922 boundary/fire room; 1925 tenant; 1936–1944 removal cause.", "Open: Palace 1900/1905 exact location; Surber's 1905 Palace→1907 No.501 room continuity; later Surber/Smith/Case/Wilson/Hunsaker succession; Case/Pioneer/Holman/Restaurant exact assignment; 1922 boundary/fire room; 1925 tenant; 1936–1944 removal cause.")

replace_once("buildings/501-main.md", "- Related people: `P-055`, `P-037`, `P-038`", "- Related people: `P-055`, `P-037`, `P-038`, `P-099`")
replace_once("buildings/501-main.md", "- Related evidence: `E-020`, `E-021`, `E-054`, `E-055`, `E-056`, `E-094`, `E-096`, `E-097`, `E-103`, `E-104`, `E-108`, `E-121`, `E-122`", "- Related evidence: `E-020`, `E-021`, `E-054`, `E-055`, `E-056`, `E-094`, `E-096`, `E-097`, `E-103`, `E-104`, `E-108`, `E-121`, `E-122`, `E-154`, `E-155`, `E-156`")
replace_once("buildings/501-main.md", "- Related sources: `S-021`, `S-023`, `S-064` through `S-069`, `S-107`, `S-108`, `S-111` through `S-113`, `S-117` through `S-119`, `S-135` through `S-137`", "- Related sources: `S-021`, `S-023`, `S-064` through `S-069`, `S-107`, `S-108`, `S-111` through `S-113`, `S-117` through `S-119`, `S-135` through `S-137`, `S-174` through `S-176`")
insert_before("buildings/501-main.md", "## Direct 1907 Numbered Occupancy Evidence", "## Palace Saloon context, 1900–1907", """## Palace Saloon context, 1900–1907

Three newly integrated visually verified pages add earlier business-history context (`E-154`–`E-156`; `S-174`–`S-176`):

- **6 Apr. 1900:** Albert Knapp is reported purchasing Palace Saloon, opposite the post office on a corner, with an intended refit.
- **24 Feb. 1905:** A. Knapp is reported selling Palace Saloon to **A. J. Surber**. This directly proves Surber's Palace relationship on that date.
- **19 Jul. 1907:** Palace Saloon is described as **on Fifth Street**.

None of these pages prints 501. They therefore do not move the direct numbered anchor earlier than the **4 Oct. 1907 Surber No.501** notice, nor do they prove the 1905 Palace room and the 1907 No.501 room were identical.
""")
replace_once("buildings/501-main.md", "Only the **19 March 1912** source directly prints **501 Main** for Palace Saloon. Do not backfill 501 onto the 1907 or 1909 pages, equate Surber's exact-501 premises with Palace solely from proximity, or treat application notices as license grants/title.", "Only the **19 March 1912** source directly prints **501 Main** together with the Palace Saloon trade name. The 1905 sale now directly ties Surber to Palace, but do not backfill 501 onto 1900/1905/July-1907/1909 pages or equate the 1905 Palace room with Surber's later exact-501 premises without an address-continuity bridge.")

insert_before("registers/business-timeline.md", "| 24 May 1907 | Palace Saloon |", "| 6 Apr. 1900 | Palace Saloon / Albert Knapp", """| 6 Apr. 1900 | Palace Saloon / Albert Knapp | `BUS-024` | `E-154` | Very High for reported purchase | Opposite post office/on a corner; no number or deed; planned refit not completed-construction proof. |
| 24 Feb. 1905 | Palace Saloon / A. Knapp → A. J. Surber | `BUS-024` | `E-155` | Very High for reported business sale | Direct Surber/Palace trade-name link; no numbered address, deed/title or later continuity. |
""")
insert_before("registers/business-timeline.md", "| 4 Oct.1907 | A. J. Surber liquor premises |", "| 19 Jul. 1907 | Palace Saloon |", """| 19 Jul. 1907 | Palace Saloon | `BUS-024` | `E-156` | Very High for Fifth Street wording | Described on Fifth Street; no number/proprietor; not assigned to 501. |
""")

append_once("timeline.md", "## 1900–1907 — Palace Saloon ownership/location supplement", """## 1900–1907 — Palace Saloon ownership/location supplement

Three project-steward supplied pages, visually verified and preserved as `S-174`–`S-176`, refine the early Palace Saloon chronology:

- **6 Apr. 1900 (`E-154`):** Albert Knapp reportedly purchased Palace Saloon, opposite the post office on a corner, and intended to improve/refit it.
- **24 Feb. 1905 (`E-155`):** A. Knapp reportedly sold Palace Saloon to **A. J. Surber**. This directly establishes Surber's Palace trade-name relationship in 1905.
- **19 Jul. 1907 (`E-156`):** Palace Saloon is directly described as **on Fifth Street**.

These records do not print 501. The direct 501 Surber anchor remains 4 Oct. 1907 (`E-121`), and the first source printing **Palace Saloon + 501 Main together** remains 19 Mar. 1912 (`E-104`). No uninterrupted 1905→1907 or 1907→1912 operator/room continuity is inferred.
""")
append_once("evidence/open-questions.md", "### OQ-032 update — Palace Saloon 1900–1907 supplement", """### OQ-032 update — Palace Saloon 1900–1907 supplement

`E-154`–`E-156` materially narrow the early Palace question. The 1905 *Courier* directly reports **A. Knapp selling Palace Saloon to A. J. Surber**, so Surber's Palace relationship is no longer an open trade-name question. Remaining questions are the 1900/1905 exact premises, whether Surber remained Palace operator through July/October 1907, whether the October 1907 No.501 room was the same Palace room, and the later Smith/Case/Wilson succession. Do not infer continuity solely from the later intersection/number evidence.
""")
append_once("evidence/research-leads.md", "### RL-045 update — Palace sale/location chain", """### RL-045 update — Palace sale/location chain

New direct evidence (`E-154`–`E-156`) supplies a 1900 Knapp purchase, a **1905 Knapp→A. J. Surber Palace Saloon sale**, and a July 1907 Fifth Street location. Next documentary targets: liquor-license grants/transfers and city-council minutes around the 1900 and 1905 sales; city directory/address evidence locating Palace in 1900–1907; and any record explicitly bridging Surber's 1905 Palace to his October 1907 No.501 premises.
""")
append_once("registers/research-log.md", "1900–1907 Palace Saloon sale/location supplement", """| 2026-09-01 | Palace Saloon 1900–1907 sale/location supplement | Visually verified three project-steward supplied pages; preserved canonical issue/page PDFs. 1900: Albert Knapp buys Palace; 1905: A. Knapp sells Palace to A. J. Surber; Jul.1907: Palace described on Fifth Street. Registered `S-174`–`S-176`, `E-154`–`E-156`, and `P-099`; no 501 backfill or uninterrupted-operation claim. |
""")
append_once("ARCHIVE_INDEX.md", "## Palace Saloon 1900–1907 sale/location supplement", """## Palace Saloon 1900–1907 sale/location supplement

The early Palace chronology is now extended with three visually verified primary pages:

- `S-174` / `E-154` — 6 Apr. 1900 Albert Knapp purchase; opposite post office/on a corner; intended refit.
- `S-175` / `E-155` — 24 Feb. 1905 **A. Knapp → A. J. Surber Palace Saloon sale**.
- `S-176` / `E-156` — 19 Jul. 1907 Palace Saloon **on Fifth Street**.

This directly establishes Surber's Palace relationship in 1905 but does not prove the exact early street number or continuity to his October 1907 No.501 liquor premises. See `evidence/source-captures/1900-1907-palace-saloon-sale-location-supplement-2026-09-01.md`.
""")
append_once("indexes/id-crosswalk.md", "`P-099` Albert Knapp", """| `P-099` Albert Knapp / A. Knapp | `BUS-024`; `E-154`, `E-155`; `S-174`, `S-175` | 1900 Palace purchaser; 1905 A. Knapp reported seller to A. J. Surber. Same-person identity is a strong inference from same-business chronology, not surname alone. |
| `P-055` A. J. Surber — Palace supplement | `BUS-024`, `BUS-045`; `E-155`, `E-121`; `S-175`, `S-135`, `S-137` | 1905 Palace purchaser; later 1907 exact-501 liquor applicant. The 1905 Palace room is not automatically equated with 501. |
""")

append_once("database/sources.yml", "  - id: S-174", f"""  - id: S-174
    name: Oregon City Courier-Herald, 6 April 1900, p.5 — Albert Knapp purchases Palace Saloon
    url: {FILES[0]["url"]}
    notes: "Primary newspaper; visually verified supplied scan. Repository file {FILES[0]["repo_path"]}. Original upload {FILES[0]["uploaded_name"]}. Reports Albert Knapp purchased Palace saloon opposite post office/on a corner and planned refit. Uploaded SHA-256 {FILES[0]["uploaded_sha256"]}; repository SHA-256 {FILES[0]["repo_sha256"]}. Related evidence E-154."
  - id: S-175
    name: Oregon City Courier, 24 February 1905, p.5 — Palace Saloon sold A. Knapp to A. J. Surber
    url: {FILES[1]["url"]}
    notes: "Primary newspaper; visually verified supplied scan. Repository file {FILES[1]["repo_path"]}. Original upload {FILES[1]["uploaded_name"]}. Direct reported Palace sale to Surber; no number/title/license grant. Uploaded SHA-256 {FILES[1]["uploaded_sha256"]}; repository SHA-256 {FILES[1]["repo_sha256"]}. Related evidence E-155."
  - id: S-176
    name: Oregon City Enterprise, 19 July 1907, p.1 — Palace Saloon on Fifth Street
    url: {FILES[2]["url"]}
    notes: "Primary newspaper; visually verified supplied scan. Repository file {FILES[2]["repo_path"]}. Original upload {FILES[2]["uploaded_name"]}. Reports rear of Palace saloon on Fifth Street; no number/proprietor. Uploaded SHA-256 {FILES[2]["uploaded_sha256"]}; repository SHA-256 {FILES[2]["repo_sha256"]}. Related evidence E-156."
""")
append_once("database/evidence.yml", "  - id: E-154", """  - id: E-154
    name: Albert Knapp reported purchase of Palace Saloon, 6 April 1900
    type: Primary newspaper / reported business purchase and relative-location evidence
    claims:
      - Albert Knapp was reported purchasing Palace Saloon, opposite the post office on a corner.
      - The item says he intended to improve/refit the saloon.
      - No numbered address, deed/title, or completed construction is proved.
    confidence: Very High for printed report; unresolved for precise address/title/improvement completion.
    related_sources: [S-174]
    related_businesses: [BUS-024]
    related_people: [P-099]
    repository_file: evidence/E-154-1900-palace-saloon-albert-knapp-purchase.md
  - id: E-155
    name: Palace Saloon reported sold from A. Knapp to A. J. Surber, 24 February 1905
    type: Primary newspaper / reported business sale
    claims:
      - A. Knapp was reported selling Palace Saloon to A. J. Surber, formerly of Kalama, Washington.
      - This directly establishes Surber's Palace Saloon relationship in February 1905.
      - No numbered address, real-estate title, license grant/transfer, or uninterrupted later operation is proved.
    confidence: Very High for printed sale report; unresolved for legal transaction details and later room continuity.
    related_sources: [S-175]
    related_businesses: [BUS-024, BUS-045]
    related_people: [P-055, P-099]
    repository_file: evidence/E-155-1905-palace-saloon-knapp-surber-sale.md
  - id: E-156
    name: Palace Saloon described on Fifth Street, 19 July 1907
    type: Primary newspaper / business-location evidence
    claims:
      - The Enterprise reports Joe Kramer in the rear of the Palace saloon on Fifth Street.
      - This directly supplies Fifth Street location context.
      - No street number or proprietor is printed; the record is not automatically assigned to 501.
    confidence: Very High for printed Fifth Street wording; unresolved for numbered storefront and operator.
    related_sources: [S-176]
    related_businesses: [BUS-024]
    related_people: []
    repository_file: evidence/E-156-1907-palace-saloon-fifth-street.md
""")
append_once("database/people.yml", "  - id: P-099", """  - id: P-099
    name: Albert Knapp / A. Knapp
    role: Palace Saloon purchaser / later reported seller
    notes: 1900 report spells Albert Knapp purchasing Palace; 1905 report spells A. Knapp selling Palace to A. J. Surber. Same-person identity is a strong inference from the same-business sequence, not surname alone. Business transaction is not real-estate title.
    related_businesses: [BUS-024]
    repository_file: people/profiles/albert-knapp.md
""")
replace_once("database/people.yml", "    notes: 1907 notice prints No. 501 and calls it his present place of business. The 1908 notice requests six months but prints only the intersection. No Palace trade name, grant, title or uninterrupted operation proved.", "    notes: 24 February 1905 report says A. Knapp sold Palace Saloon to A. J. Surber, directly establishing Surber's Palace relationship on that date. The 1907 notice prints No. 501 and the 1908 notice repeats only the intersection; neither later notice prints the Palace name. Continuous Palace operation to the exact-501 room, grant and title remain unproved.")
replace_once("database/businesses.yml", "    notes: The Palace Saloon trade name is listed citywide by May 1907 without address/operator. Ralph O. Smith is a September 1909 applicant at the Palace Saloon, corner Main/Fifth; Joe Wilson is exact 501 in March 1912 and Joseph Wilson is Fifth/Main in June 1912. No grant, property title or uninterrupted succession proved.", "    notes: 6 April 1900 report has Albert Knapp purchasing Palace Saloon opposite the post office/on a corner; 24 February 1905 reports A. Knapp selling Palace to A. J. Surber, directly establishing Surber's Palace relationship. May 1907 lists the trade name citywide; July 1907 places Palace on Fifth Street without number/proprietor; Ralph O. Smith is at Main/Fifth in Sep.1909; Joe Wilson is exact 501 in Mar.1912 and Joseph Wilson Fifth/Main in Jun.1912. Early exact number, grants, property title and uninterrupted succession remain unproved.")
replace_once("database/businesses.yml", "    notes: 1907 notice prints No. 501 and calls it his present place of business. The 1908 notice requests six months\n      but prints only the intersection. No Palace trade name, grant, title or uninterrupted operation proved.", "    notes: 24 February 1905 report directly says A. Knapp sold Palace Saloon to A. J. Surber. The 4 October 1907 notice prints No.501 and the 1908 notice repeats only Main/Fifth; those later notices do not print Palace. Continuous 1905 Palace-to-501 room identity, grant and title remain unproved.")
replace_once("database/buildings.yml", "    notes: 4 October 1907 Surber notice explicitly prints No.501/Main-Fifth;1908 repeats only the intersection. No title, Palace trade-name or later-premises identity inferred.", "    notes: 1905 Palace sale directly connects A. J. Surber to the Palace trade name without a number; July 1907 puts Palace on Fifth Street without proprietor/number. 4 October 1907 Surber notice explicitly prints No.501/Main-Fifth but not Palace; continuity between the 1905 Palace and 1907 No.501 room remains unproved.")
replace_once("database/buildings.yml", "      - E-121\n      - E-122\n      - E-116", "      - E-154\n      - E-155\n      - E-156\n      - E-121\n      - E-122\n      - E-116")
replace_once("database/buildings.yml", "      - S-135\n      - S-136\n      - S-137\n      - S-130", "      - S-174\n      - S-175\n      - S-176\n      - S-135\n      - S-136\n      - S-137\n      - S-130")
replace_once("database/buildings.yml", "      - P-055\n      - P-037\n      - P-038", "      - P-055\n      - P-099\n      - P-037\n      - P-038")
append_once("database/timeline.yml", "    date: 6 April 1900\n    summary: Albert Knapp", """  - date: 6 April 1900
    summary: Albert Knapp is reported purchasing Palace Saloon, opposite the post office on a corner, with an intended refit; no number/title/completed-construction proof.
    related_evidence: [E-154]
  - date: 24 February 1905
    summary: A. Knapp is reported selling Palace Saloon to A. J. Surber, directly establishing Surber's Palace relationship; no numbered address or later room continuity proved.
    related_evidence: [E-155]
  - date: 19 July 1907
    summary: Palace Saloon is described on Fifth Street; no number/proprietor and no automatic 501 assignment.
    related_evidence: [E-156]
""")

print("Integrated Palace Saloon 1900–1907 supplement.")
for item in FILES:
    print(item["repo_path"], item["repo_bytes"], item["repo_sha256"])
