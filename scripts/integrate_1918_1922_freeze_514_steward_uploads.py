from pathlib import Path
import hashlib
import re
import urllib.request

PAGES = [
    {
        "key": "freeze0408",
        "url": "https://oregonnews.uoregon.edu/lccn/sn00063700/1921-04-08/ed-1/seq-3.pdf",
        "sha256": "f86f0ca8d7f503db4fd5b67b812d97e058f323b9623560a4c25a52341734f11f",
        "size": 781471,
        "repo_path": "newspapers/oregon-city-enterprise/1921-04-08-page-3-dr-freeze-505-half-main.pdf",
        "upload_name": "505 & half Main (Dr Freeze) Oregon City enterprise., April 08, 1921, Page Page 3, Image 3.pdf",
    },
    {
        "key": "freeze0520",
        "url": "https://oregonnews.uoregon.edu/lccn/sn00063700/1921-05-20/ed-1/seq-3.pdf",
        "sha256": "02eb3a4676826d0feff19c3b59b61ce648466034bddc927d4173bd3b8455d875",
        "size": 917426,
        "repo_path": "newspapers/oregon-city-enterprise/1921-05-20-page-3-dr-freeze-505-half-witham-munden-514-main.pdf",
        "upload_name": "514 Main Oregon City enterprise., May 20, 1921, Page Page 3, Image 3.pdf",
    },
    {
        "key": "wolf1918",
        "url": "https://oregonnews.uoregon.edu/lccn/sn00063698/1918-10-10/ed-1/seq-4.pdf",
        "sha256": "bbed6092aa4743f7e86286c4c25f03544648bc1e523bf5d5da557d487af302c0",
        "size": 866276,
        "repo_path": "newspapers/oregon-city-courier/1918-10-10-page-4-wolf-miller-505-main.pdf",
        "upload_name": "Main Street Addresseas Oregon City courier., October 10, 1918, Page 4, Image 4.pdf",
    },
    {
        "key": "freeze1028",
        "url": "https://oregonnews.uoregon.edu/lccn/sn00063700/1921-10-28/ed-1/seq-5.pdf",
        "sha256": "ac865f8074f809383b5dd1277ac9a522ba1ddd5a50a60f2c5790de4cc064e8c0",
        "size": 802035,
        "repo_path": "newspapers/oregon-city-enterprise/1921-10-28-page-5-dr-freeze-505-main.pdf",
        "upload_name": "505 & half Main (Dr Freeze) Oregon City enterprise., October 28, 1921, Page Page 5, Image 5.pdf",
    },
    {
        "key": "freeze0630",
        "url": "https://oregonnews.uoregon.edu/lccn/sn00063700/1922-06-30/ed-1/seq-3.pdf",
        "sha256": "0d9dc181d387e55cef7c6631e9b848d7aa89374268edf2b1ce5bfddcafe4b013",
        "size": 885419,
        "repo_path": "newspapers/oregon-city-enterprise/1922-06-30-page-3-dr-freeze-505-half-masonic-move.pdf",
        "upload_name": "505 & half Main (Dr Freeze) Oregon City enterprise., June 30, 1922, Page Page 3, Image 3.pdf",
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
    Path(path).write_text(text, encoding="utf-8")


def replace_md_section(path: str, heading: str, block: str) -> None:
    text = read(path)
    pattern = re.compile(r"(?ms)^" + re.escape(heading) + r"\n.*?(?=^## |\Z)")
    match = pattern.search(text)
    if not match:
        raise SystemExit(f"Missing Markdown section {heading!r} in {path}")
    new = block.rstrip() + "\n\n"
    write(path, text[:match.start()] + new + text[match.end():])


def replace_yaml_record(path: str, ident: str, block: str) -> None:
    text = read(path)
    pattern = re.compile(r"(?ms)^  - id: " + re.escape(ident) + r"\n.*?(?=^  - id: |\Z)")
    match = pattern.search(text)
    if not match:
        raise SystemExit(f"Missing YAML record {ident} in {path}")
    new = block.rstrip() + "\n\n"
    write(path, text[:match.start()] + new + text[match.end():])


def append_md_once(path: str, marker: str, block: str) -> None:
    text = read(path)
    if marker in text:
        return
    write(path, text.rstrip() + "\n\n" + block.strip() + "\n")


def append_yaml_once(path: str, ident: str, block: str) -> None:
    text = read(path)
    if re.search(r"(?m)^  - id: " + re.escape(ident) + r"$", text):
        return
    write(path, text.rstrip() + "\n\n" + block.rstrip() + "\n")


def replace_exact(path: str, old: str, new: str) -> None:
    text = read(path)
    if old not in text:
        raise SystemExit(f"Expected text not found in {path}: {old[:90]!r}")
    write(path, text.replace(old, new, 1))


# Reconcile every supplied page by SHA-256 before downloading anything new.
existing_by_hash = {}
for pdf in Path(".").rglob("*.pdf"):
    try:
        existing_by_hash.setdefault(digest(pdf), str(pdf))
    except OSError:
        pass

for item in PAGES:
    if item["sha256"] in existing_by_hash:
        item["actual_path"] = existing_by_hash[item["sha256"]]
        item["handling"] = "already present; deduplicated"
        continue

    req = urllib.request.Request(item["url"], headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=90) as response:
        data = response.read()
    got = hashlib.sha256(data).hexdigest()
    if got != item["sha256"] or len(data) != item["size"]:
        raise SystemExit(
            f"Canonical page mismatch for {item['key']}: sha={got}, bytes={len(data)}; "
            f"expected sha={item['sha256']}, bytes={item['size']}"
        )
    target = Path(item["repo_path"])
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    item["actual_path"] = item["repo_path"]
    item["handling"] = "newly preserved"
    existing_by_hash[item["sha256"]] = item["repo_path"]

by = {item["key"]: item for item in PAGES}

# Current immutable-ID availability guard.
for ident, path in (("S-191", "evidence/source-register.md"), ("E-170", "evidence/evidence-register.md")):
    if re.search(r"(?m)^## " + re.escape(ident) + r" —", read(path)):
        raise SystemExit(f"{ident} already assigned in {path}")
for ident, path in (("S-191", "database/sources.yml"), ("E-170", "database/evidence.yml")):
    if re.search(r"(?m)^  - id: " + re.escape(ident) + r"$", read(path)):
        raise SystemExit(f"{ident} already assigned in {path}")

# Broaden S-034 only to record another fact printed on the same already-preserved page.
replace_md_section(
    "evidence/source-register.md",
    "## S-034 — Oregon City Courier, 10 October 1918, Wolf and Miller",
    f'''## S-034 — Oregon City Courier, 10 October 1918, Wolf and Miller
Source/location: https://oregonnews.uoregon.edu/lccn/sn00063698/1918-10-10/ed-1/seq-4/
Repository PDF: `{by['wolf1918']['actual_path']}`
Original uploaded filenames reconciled to this same page include `505 Main (Wolf & Miller) Oregon City courier., October 10, 1918, Page 4, Image 4.pdf` and `{by['wolf1918']['upload_name']}`.
Related evidence: `E-027`; cross-reference `E-166`, `E-167`, `E-170`
Notes: The visually verified page directly prints **Wolf & Miller, 505 Main** in the shoe/clothing and shoe-repair feature. The same `Who's Who in Oregon City` page also directly prints **A. A. Mundin, 514 Main** in its new/second-hand furniture entry; that 514 reading is reused by `E-170` and independently corroborated by the 20 May 1921 `A. A. Munden` / Witham article. The separate 31 October 1918 answer key prints Wolf & Miller at 503 Main, and the separate 24 October business directory has an unresolved `MUNDEN, A. A., 614 Main` reading; neither conflict is silently corrected. Exact steward-upload PDF preserved, SHA-256 `{by['wolf1918']['sha256']}`.'''
)

replace_md_section(
    "evidence/source-register.md",
    "## S-035 — Dr. Freeze Eye Specialist advertisements, 1921-1922",
    f'''## S-035 — Dr. Freeze Eye Specialist advertisements, 1921-1922
Source/location: https://oregonnews.uoregon.edu/lccn/sn00063700/1921-11-11/ed-1/seq-5/
Related evidence: `E-028`
Exact steward-upload page PDFs now preserved:
- 8 Apr. 1921 p. 3 — `{by['freeze0408']['actual_path']}` — **505½ Main Street** — SHA-256 `{by['freeze0408']['sha256']}`
- 20 May 1921 p. 3 — `{by['freeze0520']['actual_path']}` — **505½ Main St.** — SHA-256 `{by['freeze0520']['sha256']}`
- 28 Oct. 1921 p. 5 — `{by['freeze1028']['actual_path']}` — **505 Main St., Opposite Postoffice** — SHA-256 `{by['freeze1028']['sha256']}`
- 30 Jun. 1922 p. 3 — `{by['freeze0630']['actual_path']}` — **505½ Main St.** plus `After July 1 will be at my new location 207 Masonic Bldg.` — SHA-256 `{by['freeze0630']['sha256']}`
Notes: All four supplied Enterprise page scans were visually verified. The October 1921 omission of the half-number is preserved as printed address variation; it does **not** by itself prove a physical move between an upstairs/half-numbered office and a ground-floor 505 storefront. The 30 June 1922 Enterprise ad independently repeats the move notice documented one day earlier in the Banner-Courier.'''
)

replace_md_section(
    "evidence/evidence-register.md",
    "## E-028 — Dr. Freeze, Eye Specialist, 505 / 505 1/2 Main, 1921-1922",
    '''## E-028 — Dr. Freeze, Eye Specialist, 505 / 505 1/2 Main, 1921-1922
Type: Primary newspaper advertisements; supplied pages **VISUALLY VERIFIED**  
Sources: `S-035`  
Claims: The 8 April and 20 May 1921 *Oregon City Enterprise* advertisements print **Dr. Freeze, Eye Specialist, 505½ Main**. The 28 October 1921 advertisement instead prints **505 Main St., Opposite Postoffice** without the half-number. The 30 June 1922 advertisement returns to **505½ Main St.** and says that **after July 1** Freeze will be at **207 Masonic Bldg.** This provides a direct end-of-June move marker. The 505-versus-505½ wording is preserved as a source-level address variation and is not converted into a claim about floor, room, storefront, ownership, or physical relocation within the building.  
Confidence: Very High for the printed dates, address forms, professional title, and move notice; physical room arrangement unresolved.'''
)

# New source/evidence pair for the 514 Main succession statement on the 20 May 1921 page.
append_md_once(
    "evidence/source-register.md",
    "## S-191 — Oregon City Enterprise, 20 May 1921, p. 3, Witham / A. A. Munden at 514 Main",
    f'''## S-191 — Oregon City Enterprise, 20 May 1921, p. 3, Witham / A. A. Munden at 514 Main
Canonical PDF: {by['freeze0520']['url']}  
Repository PDF: `{by['freeze0520']['actual_path']}`  
Original uploaded filename: `{by['freeze0520']['upload_name']}`  
Type: Primary newspaper article; **VISUALLY VERIFIED**.  
Related evidence: `E-170`; cross-reference source `S-034`.  
Notes: The article **Witham Buys Stock Of Terk Brothers** says W. O. Witham came to Oregon City about two and one-half years earlier from Salem and purchased the furniture store of **A. A. Munden at 514 Main street**; it also says he gradually added stock before purchasing Terk Brothers' furniture/household-goods stock. The article does not state an exact Munden-to-Witham transfer date or legal transaction mechanics. SHA-256 `{by['freeze0520']['sha256']}`.'''
)

append_md_once(
    "evidence/evidence-register.md",
    "## E-170 — W. O. Witham / A. A. Munden furniture-store succession at 514 Main",
    '''## E-170 — W. O. Witham / A. A. Munden furniture-store succession at 514 Main
Type: Primary newspaper article plus visually verified comparison page  
Sources: `S-191`, `S-034`  
Claims: The 20 May 1921 *Oregon City Enterprise* states that W. O. Witham had come from Salem about two and one-half years earlier and purchased **A. A. Munden's furniture store at 514 Main street**, later expanding the stock and then purchasing Terk Brothers' stock. The visually verified 10 October 1918 *Oregon City Courier* independently prints **A. A. Mundin, 514 Main** in its new/second-hand furniture profile. These two pages materially strengthen **514 Main** as the intended address and preserve the `Mundin`/`Munden` spelling variation. They do **not** erase the separate 24 October 1918 directory reading `MUNDEN, A. A., 614 Main`, which remains an unresolved scan-level conflict, and the 1921 retrospective wording does not establish an exact purchase date.  
Confidence: Very High for the printed 514 address and 1921 succession statement; Strong for approximate late-1918 timing only; 514/614 conflict unresolved.'''
)

# YAML mirrors.
replace_yaml_record(
    "database/sources.yml",
    "S-034",
    f'''  - id: S-034
    name: Oregon City Courier, 10 October 1918, Wolf and Miller
    url: https://oregonnews.uoregon.edu/lccn/sn00063698/1918-10-10/ed-1/seq-4/
    notes: >-
      Visually verified page directly prints Wolf & Miller at 505 Main and also A. A. Mundin at 514 Main. Exact PDF preserved at {by['wolf1918']['actual_path']}, SHA-256 {by['wolf1918']['sha256']}. Related evidence E-027 and E-170; Wolf & Miller's 31 October 503 reading and A. A. Munden's separate 24 October 614 reading remain unresolved conflicts.'''
)

replace_yaml_record(
    "database/sources.yml",
    "S-035",
    f'''  - id: S-035
    name: Dr. Freeze Eye Specialist advertisements, 1921-1922
    url: https://oregonnews.uoregon.edu/lccn/sn00063700/1921-11-11/ed-1/seq-5/
    notes: >-
      Exact visually verified supplied PDFs preserved for 8 Apr 1921 at 505½ Main ({by['freeze0408']['actual_path']}), 20 May 1921 at 505½ Main ({by['freeze0520']['actual_path']}), 28 Oct 1921 at printed 505 Main opposite Postoffice ({by['freeze1028']['actual_path']}), and 30 Jun 1922 at 505½ Main with after-July-1 move notice to 207 Masonic Bldg ({by['freeze0630']['actual_path']}). Address-form variation does not prove physical room/floor movement. Related evidence E-028.'''
)

replace_yaml_record(
    "database/evidence.yml",
    "E-028",
    '''  - id: E-028
    name: "Dr. Freeze, Eye Specialist, 505 / 505 1/2 Main, 1921-1922"
    type: Primary newspaper advertisements; supplied pages visually verified
    claims:
      - 8 April and 20 May 1921 Enterprise advertisements print Dr. Freeze, Eye Specialist, at 505 1/2 Main.
      - 28 October 1921 Enterprise advertisement prints 505 Main St., Opposite Postoffice, without the half-number.
      - 30 June 1922 Enterprise advertisement prints 505 1/2 Main and says that after July 1 Freeze will be at 207 Masonic Bldg.
      - The 505 versus 505 1/2 wording is preserved as source-level address variation and does not prove a floor, room, storefront, ownership, or within-building move.
    confidence: Very High for printed dates, address forms, professional title, and move notice; physical arrangement unresolved.
    related_sources:
      - S-035
    related_people:
      - P-027
    related_businesses:
      - BUS-021
    related_buildings:
      - B-002'''
)

append_yaml_once(
    "database/sources.yml",
    "S-191",
    f'''  - id: S-191
    name: Oregon City Enterprise, 20 May 1921, p. 3, Witham / A. A. Munden at 514 Main
    url: https://oregonnews.uoregon.edu/lccn/sn00063700/1921-05-20/ed-1/seq-3/
    notes: >-
      Visually verified article says W. O. Witham had come from Salem about two and one-half years earlier and purchased A. A. Munden's furniture store at 514 Main street, later adding stock and purchasing Terk Brothers' stock. Exact PDF preserved at {by['freeze0520']['actual_path']}, SHA-256 {by['freeze0520']['sha256']}. Related evidence E-170; exact transfer date and 24 Oct 1918 614-address conflict remain unresolved.'''
)

append_yaml_once(
    "database/evidence.yml",
    "E-170",
    '''  - id: E-170
    name: W. O. Witham / A. A. Munden furniture-store succession at 514 Main
    type: Primary newspaper article plus visually verified comparison page
    claims:
      - 20 May 1921 Oregon City Enterprise says W. O. Witham had come from Salem about two and one-half years earlier and purchased A. A. Munden's furniture store at 514 Main street.
      - The article says Witham gradually added stock and had just purchased Terk Brothers' furniture and household-goods stock.
      - 10 October 1918 Oregon City Courier independently prints A. A. Mundin at 514 Main, preserving a Mundin/Munden spelling variation.
      - A separate 24 October 1918 directory reading of MUNDEN, A. A., 614 Main remains unresolved and is not silently corrected.
      - The 1921 retrospective statement does not provide an exact Munden-to-Witham purchase date or legal transaction mechanics.
    confidence: Very High for printed 514 address and succession statement; Strong for approximate timing; 514/614 conflict unresolved.
    related_sources:
      - S-191
      - S-034'''
)

# Keep business/person mirrors synchronized with the richer S-035/E-028 reading.
replace_yaml_record(
    "database/businesses.yml",
    "BUS-021",
    '''  - id: BUS-021
    name: Dr. Freeze, Eye Specialist
    address: 507 1/2 Main (Mar-Apr 1921); 505 / 505 1/2 Main (Apr 1921-Jun 1922)
    notes: >-
      Harvey Freeze moved his practice from Portland to Oregon City in March 1921. Visually verified ads print 507½ Main on Mar 25 and Apr 1; 505½ Main on Apr 8 and May 20; 505 Main, Opposite Postoffice, on Oct 28; and 505½ Main again on Jun 30 1922 with a notice that after July 1 he would be at 207 Masonic Bldg. The 505/505½ variation is preserved as printed and does not prove a physical room/floor move.
    related_buildings:
      - B-002
      - B-003
    related_people:
      - P-027
    related_evidence:
      - E-028
      - E-137
    related_sources: [S-035, S-153]
    repository_file: businesses/dr-freeze.md'''
)

replace_yaml_record(
    "database/people.yml",
    "P-027",
    '''  - id: P-027
    name: Dr. Freeze
    repository_file: people/profiles/dr-freeze.md
    role: Eye specialist
    notes: >-
      Harvey Freeze moved his practice from Portland to Oregon City in March 1921. Visually verified ads place him at 507½ Main on Mar 25 and Apr 1, 505½ Main on Apr 8 and May 20, printed 505 Main opposite Postoffice on Oct 28, and 505½ Main on Jun 30 1922 with an after-July-1 move notice to 207 Masonic Bldg. Address-form variation does not prove physical room/floor movement.
    related_buildings:
      - B-002
      - B-003
    related_businesses:
      - BUS-021
    related_evidence: [E-028, E-137]
    related_sources: [S-035, S-153]'''
)

append_md_once(
    "businesses/dr-freeze.md",
    "## 2 September 2026 steward-upload address-form supplement",
    '''## 2 September 2026 steward-upload address-form supplement
Four exact Enterprise page scans now physically preserved under `newspapers/` make the address wording explicit: **505½ Main** on 8 April and 20 May 1921; **505 Main St., Opposite Postoffice** on 28 October 1921; and **505½ Main** again on 30 June 1922. The 30 June ad says that **after July 1** Freeze will be at **207 Masonic Bldg.** (`S-035` / `E-028`). The October omission of the half-number is retained as printed variation and is **not** treated as proof that Freeze moved from an upstairs/half-numbered room into the ground-floor 505 storefront.'''
)

append_md_once(
    "people/profiles/dr-freeze.md",
    "## 2 September 2026 exact-page supplement",
    '''## 2 September 2026 exact-page supplement
Steward-supplied Enterprise scans now preserve four exact address-form anchors: **505½ Main** (8 April 1921), **505½ Main** (20 May 1921), **505 Main St., Opposite Postoffice** (28 October 1921), and **505½ Main** (30 June 1922). The 30 June advertisement announces the move to **207 Masonic Bldg. after July 1**. These are professional-location statements, not evidence of real-estate ownership or the physical floor/room arrangement (`S-035` / `E-028`).'''
)

append_md_once(
    "evidence/source-captures/1921-04-08-dr-freeze-505-half-main.md",
    "## 2 September 2026 steward-upload preservation supplement",
    f'''## 2 September 2026 steward-upload preservation supplement
The steward supplied additional exact page PDFs and the archive reconciled them by SHA-256. The 8 April page is now physically preserved at `{by['freeze0408']['actual_path']}`; a 20 May page at `{by['freeze0520']['actual_path']}` again prints **505½ Main**; a 28 October page at `{by['freeze1028']['actual_path']}` prints **505 Main St., Opposite Postoffice** without the half-number; and the 30 June 1922 page at `{by['freeze0630']['actual_path']}` again prints **505½ Main** and repeats the after-1-July move to 207 Masonic Building. The October wording is retained as an address-form variation, not a physical-layout conclusion.'''
)

# Upgrade only the visually verified side of the 514/614 conflict and add the 1921 corroboration.
ledger_path = "evidence/source-captures/1916-numbered-address-ledger.md"
ledger = read(ledger_path)
row_pattern = re.compile(r"(?m)^\| \*\*514/614 Main\*\* \|.*$")
match = row_pattern.search(ledger)
if not match:
    raise SystemExit("514/614 Main row missing from numbered-address ledger")
new_row = "| **514/614 Main** | A. A. Mundin/Munden → W. O. Witham — new/second-hand goods / furniture | 10 Oct 1918 and retrospective 20 May 1921 anchors | MIXED — **10 Oct 1918 and 20 May 1921 VISUALLY VERIFIED**; 24 Oct 1918 `614 Main` reading remains unresolved | The 10 Oct 1918 *Courier* page directly prints **A. A. Mundin, 514 Main** and says the business had operated nearly two years. The 20 May 1921 *Enterprise* independently says Witham had come from Salem about two and one-half years earlier and purchased **A. A. Munden's furniture store at 514 Main street**, then expanded the stock. These strengthen 514 and preserve the Mundin/Munden spelling variation, but the separate 24 Oct 1918 directory's **MUNDEN, A. A., 614 Main** remains a conflict pending visual review; no exact transfer date is inferred. `S-034`, `S-191`, `E-170`. |"
write(ledger_path, ledger[:match.start()] + new_row + ledger[match.end():])

# Update the focused 505 timeline row rather than adding a second competing interval.
replace_exact(
    "timelines/505-main.md",
    "| 8 Apr. 1921–29 Jun. 1922 | **Dr. Freeze at 505/505½ Main**, opposite post office. | **Exact primary**. `E-137` visually places him at 507½ on 25 Mar and 1 Apr, so the 505½ advertised-address shift occurred after 1 Apr and by 8 Apr. Property/room arrangement and Leland succession remain open. | `BUS-021`; `P-027`; `E-028`, `E-137`; `S-035`, `S-153` |",
    "| 8 Apr. 1921–30 Jun. 1922 | **Dr. Freeze at 505/505½ Main**, opposite post office. | **Exact primary.** Supplied scans print 505½ on 8 Apr. and 20 May, 505 without the half-number on 28 Oct., and 505½ again on 30 Jun. 1922; the 30 Jun. ad says he will move to 207 Masonic Bldg. after 1 Jul. Preserve address-form variation; property/floor/room arrangement and Leland succession remain open. | `BUS-021`; `P-027`; `E-028`, `E-137`; `S-035`, `S-153` |"
)

replace_exact(
    "timeline.md",
    "## 1921-1922 — 505 Main\nDr. Freeze advertised as Eye Specialist at **505 / 505 1/2 Main** (`E-028`), providing direct evidence of occupied premises at 505 by 1921.",
    "## 1921-1922 — 505 Main\nExact Enterprise scans now preserve Dr. Freeze's advertised address as **505½ Main** on 8 April and 20 May 1921, **505 Main St., Opposite Postoffice** on 28 October 1921, and **505½ Main** again on 30 June 1922. The 30 June ad says that **after July 1** he will be at **207 Masonic Bldg.** (`E-028`, `S-035`). The 505/505½ variation is retained as printed and does not by itself prove a physical floor/room/storefront move.\n\n## 20 May 1921 — 514 Main furniture-store succession evidence\nThe *Oregon City Enterprise* states that W. O. Witham had come from Salem about two and one-half years earlier and purchased **A. A. Munden's furniture store at 514 Main street**, later adding stock and purchasing Terk Brothers' stock (`E-170`, `S-191`). The visually verified 10 October 1918 *Courier* independently prints **A. A. Mundin, 514 Main** (`S-034`). This strengthens 514 as the intended address and preserves the Mundin/Munden spelling variation, but it does not erase the separate unresolved 24 October 1918 `614 Main` directory reading or supply an exact transfer date."
)

append_md_once(
    "registers/business-timeline.md",
    "## 20 May 1921 — 514 Main / Witham-Munden supplement",
    '''## 20 May 1921 — 514 Main / Witham-Munden supplement
| Date | Address | Business / person | Evidence | Limits |
| --- | --- | --- | --- | --- |
| 10 Oct. 1918 / reported 20 May 1921 | **514 Main** | **A. A. Mundin/Munden → W. O. Witham**, furniture/new-and-second-hand goods | `S-034`, `S-191`, `E-170` — supplied pages visually verified | 1921 article is retrospective and does not give exact sale date; separate 24 Oct. 1918 `614 Main` reading remains unresolved. |'''
)

append_md_once(
    "registers/research-log.md",
    "## 2026-09-02 — Freeze / 514 Main steward-upload supplement",
    '''## 2026-09-02 — Freeze / 514 Main steward-upload supplement
Reconciled five steward-supplied newspaper pages by exact SHA-256. The 10 Oct. 1918 Courier page was already preserved byte-for-byte and was deduplicated. Four Enterprise pages (8 Apr., 20 May, 28 Oct. 1921; 30 Jun. 1922) were newly preserved. Freeze's printed 505½/505 address variation and 30 Jun. Masonic move notice were integrated into `S-035` / `E-028`. The 20 May 1921 article created `S-191` / `E-170` for the A. A. Munden → W. O. Witham furniture-store succession at **514 Main**, while explicitly preserving the separate 24 Oct. 1918 `614 Main` conflict.'''
)

append_md_once(
    "indexes/id-crosswalk.md",
    "## 2 September 2026 Freeze / 514 Main uploaded-page integration",
    '''## 2 September 2026 Freeze / 514 Main uploaded-page integration
- `S-191` ↔ `E-170` — 20 May 1921 *Oregon City Enterprise* p. 3, W. O. Witham retrospective purchase of A. A. Munden's furniture store at **514 Main**; compared with `S-034` 10 Oct. 1918 **A. A. Mundin, 514 Main**.
- Existing `S-035` ↔ `E-028` expanded with exact preserved Freeze pages for 8 Apr., 20 May, 28 Oct. 1921 and 30 Jun. 1922; no new IDs assigned for repeated ads in the same source/evidence family.'''
)

append_md_once(
    "ARCHIVE_INDEX.md",
    "## 2 September 2026 — Freeze / 514 Main steward-upload supplement",
    '''## 2 September 2026 — Freeze / 514 Main steward-upload supplement
Five steward-supplied newspaper pages were reconciled by SHA-256. The 10 Oct. 1918 Courier page was already present and was not duplicated; four Enterprise pages were newly preserved. Dr. Freeze's exact 505½/505 printed-address sequence and 30 Jun. 1922 move notice are integrated under `S-035` / `E-028`. A new `S-191` / `E-170` pair records the 20 May 1921 statement that W. O. Witham purchased A. A. Munden's furniture store at **514 Main**, corroborating the visually verified 10 Oct. 1918 `A. A. Mundin, 514 Main` reading while preserving the separate 24 Oct. 1918 614-address conflict. Permanent provenance: `evidence/source-captures/1918-1922-freeze-514-main-steward-upload-supplement-2026-09-02.md`.'''
)

# Standalone evidence detail.
Path("evidence/E-170-1921-05-20-witham-munden-514-main.md").write_text(
    '''# E-170 — W. O. Witham / A. A. Munden furniture-store succession at 514 Main\n\nType: Primary newspaper article plus visually verified comparison page.\n\nThe 20 May 1921 *Oregon City Enterprise* says W. O. Witham had come from Salem about two and one-half years earlier and purchased **A. A. Munden's furniture store at 514 Main street**. It says he gradually added stock and then purchased Terk Brothers' furniture, dishes, and household-furnishings stock. The visually verified 10 October 1918 *Oregon City Courier* independently prints **A. A. Mundin, 514 Main** in a new/second-hand furniture profile.\n\nThis is strong direct support for **514 Main** and preserves the `Mundin`/`Munden` spelling variation. It does not supply an exact Munden-to-Witham sale date or legal transaction mechanics, and it does **not** silently correct the separate 24 October 1918 directory reading `MUNDEN, A. A., 614 Main`, which remains unresolved pending visual review of that page.\n\nSources: `S-191`, `S-034`.\n''',
    encoding="utf-8",
)

# Permanent page-level provenance for all five steward uploads.
lines = [
    "# 1918–1922 Freeze / 514 Main steward-upload supplement",
    "",
    "Review date: **2 September 2026**.",
    "",
    "Status: **FIVE PROJECT-STEWARD PDF UPLOADS RECONCILED BY SHA-256; FOUR NEW ENTERPRISE PAGES PRESERVED; ONE COURIER PAGE DEDUPLICATED.**",
    "",
]
for item in PAGES:
    lines.extend([
        f"## {item['key']}",
        "",
        f"Original upload: `{item['upload_name']}`  ",
        f"Canonical PDF: {item['url']}  ",
        f"Repository PDF: `{item['actual_path']}`  ",
        f"SHA-256: `{item['sha256']}` ({item['size']} bytes).  ",
        f"Handling: **{item['handling']}**.",
        "",
    ])
lines.extend([
    "## Integrated historical findings",
    "",
    "- **8 Apr. 1921:** Dr. Freeze ad directly prints **505½ Main Street**.",
    "- **20 May 1921:** Dr. Freeze ad again prints **505½ Main St.**; the same page's Witham article says W. O. Witham purchased **A. A. Munden's furniture store at 514 Main street** after coming from Salem about two and one-half years earlier.",
    "- **10 Oct. 1918:** the already-preserved Courier page directly prints **A. A. Mundin, 514 Main** as well as **Wolf & Miller, 505 Main**. The page was not duplicated.",
    "- **28 Oct. 1921:** Dr. Freeze ad prints **505 Main St., Opposite Postoffice**, without the half-number.",
    "- **30 Jun. 1922:** Dr. Freeze ad prints **505½ Main St.** and says, **After July 1 will be at my new location 207 Masonic Bldg.**",
    "",
    "## Interpretive limits",
    "",
    "- The 505 versus 505½ advertisement wording is preserved as printed. It does not prove an upstairs-to-ground-floor move, storefront occupancy, ownership, or the physical room layout.",
    "- The 20 May 1921 Witham article gives retrospective timing and does not provide an exact Munden-to-Witham sale date or legal transaction mechanics.",
    "- `Mundin` (10 Oct. 1918) and `Munden` (20 May 1921) are preserved as spelling variants. These 514 readings materially strengthen 514 as the intended address but do not erase the separate unresolved 24 Oct. 1918 `MUNDEN, A. A., 614 Main` directory reading.",
    "- Reconciliation by SHA-256 establishes binary identity/deduplication status; the historical claims above come from direct visual inspection of the supplied page scans.",
    "",
])
Path("evidence/source-captures/1918-1922-freeze-514-main-steward-upload-supplement-2026-09-02.md").write_text("\n".join(lines), encoding="utf-8")

print("1918-1922 Freeze / 514 steward-upload integration prepared.")
for item in PAGES:
    print(item["key"], item["actual_path"], item["handling"], item["sha256"], item["size"])
