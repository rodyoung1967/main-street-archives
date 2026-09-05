from pathlib import Path

REVIEW = "2026-09-04"


def read(path):
    return Path(path).read_text(encoding="utf-8")


def write(path, content):
    Path(path).write_text(content, encoding="utf-8")


def insert_before(path, marker, heading, block):
    text = read(path)
    if heading in text:
        return False
    if marker not in text:
        raise SystemExit(f"Expected marker not found in {path}: {marker}")
    text = text.replace(marker, block.rstrip() + "\n\n" + marker, 1)
    write(path, text)
    return True


def replace_once(path, old, new):
    text = read(path)
    if new in text:
        return False
    if old not in text:
        raise SystemExit(f"Expected text not found in {path}: {old}")
    write(path, text.replace(old, new, 1))
    return True


def append_once(path, marker, block):
    text = read(path)
    if marker in text:
        return False
    write(path, text.rstrip() + "\n\n" + block.rstrip() + "\n")
    return True


recon = "evidence/source-captures/1945-1948-liquor-license-list-reconstruction-pass-2026-09-04.md"
brand_heading = "## Additional procedural control — pre-4 August 1948 one-applicant Brandt endorsement"
brand_block = r'''## Additional procedural control — pre-4 August 1948 one-applicant Brandt endorsement

Official Oregon City WebDrawer record:

`https://ormswd.synergydcs.com/HPRMWebDrawer/Record/4726672/File/document`

The recovered record begins on municipal page **502** with the close of a Commission meeting. Immediately after final passage of Ordinance No. 1332, the minutes state:

> Upon motion the Commission endorsed the following applicant for a liquor license:

The complete applicant universe in this action is one entry:

1. **C. H. Brandt and Nellie Brandt — Buena Vista Store.**

The meeting then adjourns. On the same municipal page 502 the next visible header begins **Oregon City, Oregon, August 4, 1948 — REGULAR MEETING**. The August 4 meeting lacked a quorum and adjourned to August 6.

The opening header/date of the meeting containing the Brandt endorsement is **not present in this recovered excerpt**. Therefore the defensible date is only **before 4 August 1948**; do not silently assign the endorsement to a presumed July regular-meeting date without recovering the preceding page(s) and header.

No Farr, Harr or 505 Main wording appears in this complete one-applicant action. That statement applies only to this particular endorsement and is not evidence about other unrecovered 1948 actions.

The Brandts later appear again in the late-1948 17-applicant approval list as **C. H. & Nellie Brandt, Buena Vista Store, 1427 16th Street**. The earlier one-applicant endorsement therefore also demonstrates that an applicant appearing in the annual late-year universe could have a separate in-year Commission action.

### Research significance

Together with the **5 May 1948 two-applicant endorsement**, municipal page 502 establishes that Oregon City handled liquor-license business in very small in-year batches, including a **single applicant**. The Farr→Harr search therefore cannot rely on annual renewal lists alone: individual endorsements, transfers, relocations and ownership-change actions throughout the license year remain necessary targets.

The official PDF text is retrievable, but this addition is preserved as **PRIMARY MUNICIPAL OCR/TEXT ONLY** until the page image is visually certified under repository standards.'''
insert_before(recon, "## February–March 1948 municipal pagination / directory clue", brand_heading, brand_block)

replace_once(
    recon,
    "5. Search the same minute windows for smaller in-year lists and individual transfers, because the 5 May 1948 two-applicant endorsement proves this procedural form existed.",
    "5. Search the same minute windows for individual and small-batch actions, because the 5 May 1948 two-applicant endorsement and the pre-4 August 1948 single-applicant Brandt endorsement prove that liquor-license business could be handled outside the annual list in batches as small as one applicant."
)

dirpath = "evidence/source-captures/1941-oregon-city-directory-page-181-locator-and-polk-disambiguation-2026-09-04.md"
dir_heading = "### Ancestry image-online discovery route"
dir_block = r'''### Ancestry image-online discovery route

LDSGenealogy's Oregon City directory inventory now gives a concrete online-image discovery route for the exact target year:

`https://ldsgenealogy.com/OR/Oregon-City.htm`

Under **Oregon City City Directories** it lists:

> **Oregon City, Oregon, City Directory, 1941 (in U.S. City Directories collection) — Ancestry — Image: online**

The parallel Clackamas County directory inventory repeats the same listing:

`https://ldsgenealogy.com/OR/Clackamas-County-City-Directories.htm`

This is a **discovery/access index**, not inspection of the Ancestry images themselves. No Ancestry directory page was opened in this pass, so no Farr, Harr, 505 Main or neighboring-address claim is promoted from this listing. The value is retrievability: a holder with Ancestry access now has a specifically identified image collection to open rather than an open-ended catalog search.

### Independent Pacific Directory Service scope control — West Linn nomination

An official City of West Linn historic nomination for the historic City Hall uses the 1941 directory in its discussion of Columbia Food Stores and cites it in footnote 58 as:

> **Pacific Directory Service 1941 Directory: Oregon City-West Linn-Gladstone**

Official nomination PDF:

`https://westlinnoregon.gov/sites/default/files/fileattachments/communications/page/54306/final_nomination_application_city_hall_and_area_history.pdf`

The nomination states that the 1941 directory lists two Columbia Food Stores in Oregon City and one in West Linn. This is independent evidence that a recent official historic-resource researcher actually consulted a Pacific Directory Service 1941 directory covering **Oregon City, West Linn and Gladstone**. It strengthens the bibliographic/scope identification already preserved from Oregon City's 2000 Downtown Final Report.

It still does **not** expose the target directory pages or establish a Farr/Harr/505 occupancy. The actual 1941 directory images remain the required primary-source check.'''
insert_before(dirpath, "## Separate 1941 PT&T telephone-directory locator — page 112", dir_heading, dir_block)

replace_once(
    dirpath,
    "When requesting or opening the **Pacific Directory Service 1941 Directory of Oregon City**, provide **pages 71 and 181** as two independent control locators. Ask the holder to confirm:",
    "When requesting or opening the **Pacific Directory Service 1941 Directory of Oregon City / Oregon City-West Linn-Gladstone**, use the newly identified **Ancestry U.S. City Directories image-online route** as well as the existing physical/catalog routes, and provide **pages 71 and 181** as two independent control locators. Ask the holder to confirm:"
)

log_block = r'''### 2026-09-04 — Farr→Harr continuation: single-applicant 1948 endorsement and 1941 directory image route
- Recovered official Oregon City WebDrawer record `4726672`, municipal p.502, showing a **one-applicant** liquor-license endorsement for **C. H. Brandt and Nellie Brandt — Buena Vista Store** immediately before the visible 4 August 1948 meeting header. The action's own opening meeting header/date is missing, so it is recorded only as **pre-4 August 1948** and **PRIMARY MUNICIPAL OCR/TEXT ONLY** pending scan certification.
- This complements the 5 May 1948 two-applicant action and confirms that annual renewal lists alone cannot exhaust the Farr→Harr transition search.
- LDSGenealogy identifies **Oregon City, Oregon, City Directory, 1941** in Ancestry's U.S. City Directories collection as **Image: online**; the images were not inspected in this pass.
- An official West Linn historic nomination independently cites **Pacific Directory Service 1941 Directory: Oregon City-West Linn-Gladstone**, strengthening the directory's publisher/scope control without adding any Farr/Harr/505 occupant claim.
- The Farr's Pool Hall → Harr's Recreation Center transition date remains unresolved.'''
append_once("registers/research-log.md", "### 2026-09-04 — Farr→Harr continuation: single-applicant 1948 endorsement and 1941 directory image route", log_block)

print("Integrated 1948 one-applicant endorsement and strengthened 1941 directory access controls; no transition date changed.")
