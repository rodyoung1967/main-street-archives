from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]

SOURCE_ID = "S-240"
EVIDENCE_ID = "E-214"
BUSINESS_ID = "BUS-099"
MARKER = "P-1043 / Fain's 511 Main address follow-up — 2026-09-05"


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


def write(rel, text):
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def append_once(rel, block, marker):
    text = read(rel)
    if marker in text:
        return False
    if not text.endswith("\n"):
        text += "\n"
    write(rel, text + "\n" + block.strip() + "\n")
    return True


# Hard-stop on accidental ID reuse by unrelated records.
for rel, ident in [
    ("evidence/source-register.md", SOURCE_ID),
    ("evidence/evidence-register.md", EVIDENCE_ID),
    ("businesses/business-index.md", BUSINESS_ID),
]:
    text = read(rel)
    if ident in text and MARKER not in text:
        raise SystemExit(f"{ident} already appears in {rel}; stop rather than reuse/renumber")

capture_rel = "evidence/source-captures/1943-03-01-amplifier-fains-mens-store-511-main-ocr-lead-2026-09-05.md"
capture = r'''# 1943-03-01 *The Amplifier* — Fain's Men's Store at 511 Main (OCR/text-only address anchor)

<!-- P-1043 / Fain's 511 Main address follow-up — 2026-09-05 -->

Reviewed **5 September 2026** as a follow-up to CCHS `P-1043` (`S-237` / `E-211` / `IMG-0758`), the 1930–1939 Main Street photograph that directly shows a **FAIN'S MEN'S STORE** sign on the west / odd-numbered side of Main between Sixth and Fifth.

Archive IDs: source `S-240`; evidence `E-214`; business `BUS-099`.

## Source

- Publication: ***The Amplifier*** (West Linn/Oregon City-area school newspaper)
- Date: **1 March 1943**
- Page: **4**
- Historic Oregon Newspapers stable page: https://oregonnews.uoregon.edu/lccn/2017260114/1943-03-01/ed-1/seq-4/
- PDF route attempted: https://oregonnews.uoregon.edu/lccn/2017260114/1943-03-01/ed-1/seq-4.pdf
- Discovery state in this research session: the official Historic Oregon Newspapers indexed/page text was retrieved, but the scanned PDF/page image could not be opened through the available retrieval route.

## Exact-address text lead

The official page text places the Fain advertisement as:

> **FAIN'S MEN'S STORE ... 511 Main Oregon City**

The same advertisement includes the wording **For Better School Clothing**.

Because the actual scan was not visually inspected in this session, this remains **OCR/TEXT ONLY**, not `VISUALLY VERIFIED`. The address should nevertheless be retained as a strong exact-address lead from the official newspaper page text.

## Relationship to CCHS P-1043

CCHS `P-1043`, dated only **1930–1939**, independently and visually shows **FAIN'S MEN'S STORE** in the west-side business-sign sequence. The 1943 newspaper text supplies a later exact numbered address, **511 Main**.

These two facts make **Fain's at 511 in the photographed 1930s state probable**, but they do **not** yet prove continuous occupancy or prove that the P-1043 storefront itself was already 511 during the exposure. A 1930s directory, advertisement, license, tax record, or another photograph with a numbered control is still required before promoting `P-1043 Fain's = 511` to `DOCUMENTED / DIRECT`.

## Other P-1043 sign/address follow-up performed

### Sandwich Nook

Targeted web searches for **Sandwich Nook + Oregon City** did not recover a reliable historic Oregon City exact-address source. The sign remains directly readable in P-1043, but its numbered address is **UNRESOLVED**. Search failure is coverage information only, not evidence that the business was absent from directories or newspapers.

### Tourist Hotel

A secondary biographical webpage reports that Thomas Deo Edwards purchased the Tourist Hotel at **524½ Main Street** in February 1932. This is a useful **UNVERIFIED SECONDARY ADDRESS LEAD** because P-1043 directly shows the Tourist Hotel on the east/even side of Main. It is not promoted here to direct evidence; locate a contemporary directory, advertisement, deed/business record, or newspaper report before treating `524½` as the controlling photo-period address.

Secondary lead URL: https://sites.google.com/a/numismaticmall.com/www/encyclopedic-dictionary-of-numismatic-philatelic-biographies/edwards-thomas-deo

### American Cleaners

A later City/ODOT technical memorandum summarizing EDR city-directory abstracts reports **502/506 Main** for Midway Cleaners / Pat's American Cleaners / American Cleaners from **1953 through 1992**. This is useful later continuity/location context only. It does **not** prove that the **AMERICAN CLEANERS** sign in P-1043 (1930–1939) occupied 502 or 506, and it does not by itself merge the 1930s sign with the later `BUS-097` operation photographed at Fifth/Main.

Official memo: https://www.orcity.org/DocumentCenter/View/12817/Tech-Memo-6-Most-Promising-Alternatives

### Oregon City Auto Parts

The City of Oregon City Downtown Final Report associates a historic-resource entry at **1020–1024 Main Street** with the name **Oregon City Auto Parts**. That address is geographically outside the photographed Sixth-to-Fifth block, so this later/secondary inventory association must **not** be used to assign the P-1043 sign to a storefront in the target block. The photograph's `OREGON CITY AUTO PARTS` sign remains an identity/address research target pending a contemporary source.

Official report: https://www.orcity.org/DocumentCenter/View/4025/Downtown-Final-Report---2000-PDF

### Alexander's Market and other partial signs

No new controlling exact-number source was recovered for **ALEXANDER'S MKT.**, the partial `...MONDS CAFE`, or the clipped `... SHOE SHOP` sign in this pass. They remain open address-sequence targets.

## Evidence classification

- **DOCUMENTED / DIRECT VISUAL (existing P-1043):** the 1930–1939 photograph visibly shows the Fain's Men's Store sign.
- **OCR/TEXT ONLY (new S-240):** 1 March 1943 official Historic Oregon Newspapers page text gives **Fain's Men's Store — 511 Main, Oregon City**.
- **PROBABLE / WORKING HYPOTHESIS:** Fain's occupied 511 Main when P-1043 was photographed.
- **UNVERIFIED SECONDARY LEAD:** Tourist Hotel at 524½ Main in February 1932.
- **LATER ADDRESS CONTEXT ONLY:** American Cleaners / related cleaner listings at 502/506 Main from 1953 forward.
- **UNRESOLVED:** Sandwich Nook, Oregon City Auto Parts in the P-1043 frame, Alexander's Market, partial cafe/shoe-shop signs, and the precise exposure year.

## Next retrieval steps

1. Visually inspect the original 1 March 1943 *Amplifier* page 4 scan and promote or correct the 511 transcription accordingly.
2. Inspect the actual **1941 Oregon City directory** pages already targeted elsewhere in the archive for Fain's, Sandwich Nook, Harding/Rexall, Tourist Hotel, Alexander's Market and neighboring addresses.
3. Search 1930–1939 contemporary advertisements/directories for Fain's with an exact number; this is the required bridge for converting the P-1043 511 mapping from probable to direct.
4. Use each confirmed address as a spatial control to assign the remaining west-side storefront sequence toward 509 → 507 → 505 → 503.
'''
if (ROOT / capture_rel).exists():
    existing = read(capture_rel)
    if MARKER not in existing:
        raise SystemExit(f"{capture_rel} exists without expected marker")
else:
    write(capture_rel, capture)

business_rel = "businesses/fains-mens-store.md"
business = r'''# Fain's Men's Store

<!-- P-1043 / Fain's 511 Main address follow-up — 2026-09-05 -->

Business ID: `BUS-099`.

## Documented visual identity

CCHS `P-1043` (`S-237` / `E-211` / `IMG-0758`), cataloged **1930–1939**, directly shows a projecting **FAIN'S MEN'S STORE** sign on the west / odd-numbered side of Main Street in the Sixth-to-Fifth block. Smaller wording includes **SHOES** and **UNION MADE GOODS**, with **CLEANERS** also visible below/near the sign.

## 511 Main address lead

Historic Oregon Newspapers page text for ***The Amplifier***, **1 March 1943, p.4** (`S-240` / `E-214`), prints Fain's Men's Store with **511 Main, Oregon City**. The scan could not be visually opened in the current session, so the 1943 address is classified **OCR/TEXT ONLY** pending scan verification.

The 1943 exact-address text and the independent 1930s photograph make **Fain's at 511 Main in the P-1043 photographed state probable**, but do not yet prove uninterrupted occupancy back into the 1930s. Do not use the 1943 line alone to call the P-1043 storefront `511` as a documented/direct fact.

## Research priority

Find a 1930–1939 directory, advertisement, license, or other exact-address record for Fain's. If 511 is confirmed during the exposure period, the Fain storefront becomes a high-value spatial control for reconstructing the neighboring 509 → 507 → 505 → 503 sequence in P-1043.
'''
if (ROOT / business_rel).exists():
    existing = read(business_rel)
    if MARKER not in existing:
        raise SystemExit(f"{business_rel} already exists without expected marker")
else:
    write(business_rel, business)

source_block = r'''## S-240 — 1 March 1943 *The Amplifier* p.4, Fain's Men's Store 511 Main page-text lead
<!-- P-1043 / Fain's 511 Main address follow-up — 2026-09-05 -->
Type: Historic Oregon Newspapers official page text / newspaper source; **OCR/TEXT ONLY — scan not visually verified in this session**.  
Date: **1 March 1943**  
Page: **4**  
URL: https://oregonnews.uoregon.edu/lccn/2017260114/1943-03-01/ed-1/seq-4/  
Related evidence/business/photo: `E-214` / `BUS-099` / `S-237` / `E-211` / `IMG-0758`.  
Capture: `evidence/source-captures/1943-03-01-amplifier-fains-mens-store-511-main-ocr-lead-2026-09-05.md`.  
Notes: Official indexed page text places **FAIN'S MEN'S STORE** at **511 Main Oregon City**. The original scan/PDF could not be opened through the available retrieval route, so do not label the transcription visually verified. This is a later exact-address anchor, not proof that the 1930–1939 P-1043 storefront was already 511 or that occupancy was uninterrupted.'''
append_once("evidence/source-register.md", source_block, MARKER)

evidence_block = r'''## E-214 — 1943 page text places Fain's Men's Store at 511 Main; 1930s P-1043 mapping remains probable
<!-- P-1043 / Fain's 511 Main address follow-up — 2026-09-05 -->
Source: `S-240`  
Related photograph/evidence: `S-237` / `E-211` / `IMG-0758`  
Related business: `BUS-099`  
Type: Newspaper exact-address text lead plus cross-source photographic comparison  
Claims:
- Historic Oregon Newspapers indexed text for ***The Amplifier***, **1 March 1943, p.4**, places **Fain's Men's Store at 511 Main, Oregon City**.
- The page scan was not successfully opened in this research session; the 1943 address evidence is therefore **OCR/TEXT ONLY** pending visual inspection.
- Independently, CCHS `P-1043` directly shows **FAIN'S MEN'S STORE** in the 1930–1939 west-side Main Street sequence.
- Combining the two makes **Fain's = 511 in the P-1043 photographed state probable**, but does not prove continuous occupancy or a 1930s exact address.
- Targeted searches did not recover a reliable historic exact address for **Sandwich Nook**; that address remains unresolved rather than negatively inferred.
- A Tourist Hotel 524½ Main statement was located only in a secondary biography and remains an unverified lead; later 502/506 American Cleaners directory-summary data does not establish the 1930s address.
Classification: **OCR/TEXT ONLY** for the 1943 exact-address newspaper transcription; **DOCUMENTED / DIRECT** for the already-reviewed P-1043 Fain business-name sign; **PROBABLE / WORKING HYPOTHESIS** for Fain at 511 during the P-1043 exposure.  
Confidence: **High** that the official indexed 1943 page text associates Fain's with 511; **Unresolved pending scan** for exact visual transcription; **Probable** for the 1930s photo-address mapping.'''
append_once("evidence/evidence-register.md", evidence_block, MARKER)

# Append synchronized YAML records safely.
sources_path = ROOT / "database/sources.yml"
sources_text = sources_path.read_text(encoding="utf-8")
if SOURCE_ID not in sources_text:
    sources_text = sources_text.rstrip() + r'''

  - id: S-240
    name: "1 March 1943 *The Amplifier* p.4, Fain's Men's Store 511 Main page-text lead"
    url: "https://oregonnews.uoregon.edu/lccn/2017260114/1943-03-01/ed-1/seq-4/"
    type: "Historic Oregon Newspapers official page text / newspaper source; OCR/TEXT ONLY pending scan inspection"
    date: "1943-03-01"
    repository_file: "evidence/source-captures/1943-03-01-amplifier-fains-mens-store-511-main-ocr-lead-2026-09-05.md"
    notes: "Official indexed page text associates Fain's Men's Store with 511 Main Oregon City. Scan not visually opened in this session; later exact-address anchor only, not proof of 1930s P-1043 address continuity."
    related_evidence: [E-214]
    related_businesses: [BUS-099]
    related_media: [IMG-0758]
''' + "\n"
    sources_path.write_text(sources_text, encoding="utf-8")

evidence_path = ROOT / "database/evidence.yml"
evidence_text = evidence_path.read_text(encoding="utf-8")
if EVIDENCE_ID not in evidence_text:
    evidence_text = evidence_text.rstrip() + r'''

  - id: E-214
    name: "1943 page text places Fain's Men's Store at 511 Main; 1930s P-1043 mapping remains probable"
    type: "Newspaper exact-address text lead plus cross-source photographic comparison"
    date: "1943-03-01"
    claims:
      - "Historic Oregon Newspapers indexed text for The Amplifier, 1 March 1943 p.4, places Fain's Men's Store at 511 Main, Oregon City."
      - "The scan was not successfully opened in this session, so the 1943 address is OCR/TEXT ONLY pending visual verification."
      - "CCHS P-1043 independently and directly shows Fain's Men's Store in the 1930-1939 west-side Main Street sequence."
      - "Fain's at 511 in the P-1043 photographed state is probable, not yet documented/direct, because continuity back from 1943 is unproved."
      - "Sandwich Nook exact address remains unresolved after targeted online search; no absence inference is made."
    confidence: "High for the official 1943 indexed-text association; unresolved pending scan visual verification; probable for the 1930s P-1043 511 mapping."
    related_sources: [S-240, S-237]
    related_businesses: [BUS-099]
    related_media: [IMG-0758]
    repository_file: "evidence/source-captures/1943-03-01-amplifier-fains-mens-store-511-main-ocr-lead-2026-09-05.md"
''' + "\n"
    evidence_path.write_text(evidence_text, encoding="utf-8")

businesses_path = ROOT / "database/businesses.yml"
businesses_text = businesses_path.read_text(encoding="utf-8")
if BUSINESS_ID not in businesses_text:
    businesses_text = businesses_text.rstrip() + r'''

  - id: BUS-099
    name: "Fain's Men's Store"
    repository_file: businesses/fains-mens-store.md
    address: "511 Main by 1 March 1943 official page text (OCR/TEXT ONLY); exact P-1043 1930s address not yet proved"
    notes: "CCHS P-1043 directly shows Fain's Men's Store during 1930-1939. Historic Oregon Newspapers indexed text gives 511 Main in 1943; continuity and exact 1930s number remain to verify."
    related_evidence: [E-211, E-214]
    related_sources: [S-237, S-240]
    related_media: [IMG-0758]
''' + "\n"
    businesses_path.write_text(businesses_text, encoding="utf-8")

# Human-readable business index row: insert after BUS-098 if possible.
index_path = ROOT / "businesses/business-index.md"
index_text = index_path.read_text(encoding="utf-8")
if BUSINESS_ID not in index_text:
    row = "| BUS-099 | [Fain's Men's Store](fains-mens-store.md) | 511 Main by 1 Mar. 1943 official page text (**OCR/TEXT ONLY**); P-1043 1930s number unproved | P-1043 directly shows the business sign in 1930–1939; the 1943 text supplies a later exact-number anchor. Treat Fain's=511 in the photographed state as probable pending a 1930s exact-address source. `E-211` / `E-214`. |"
    lines = index_text.splitlines()
    inserted = False
    for i, line in enumerate(lines):
        if line.startswith("| BUS-098 |"):
            lines.insert(i + 1, row)
            inserted = True
            break
    if not inserted:
        lines.append(row)
    index_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

# Add the cross-source result to the P-1043 capture.
p1043_rel = "evidence/source-captures/cchs-p1043-1930s-main-6th-looking-south-business-roster-2026-09-05.md"
p1043_marker = "### 1943 Fain's 511 Main follow-up"
p1043_block = r'''### 1943 Fain's 511 Main follow-up

Follow-up `S-240` / `E-214` finds official Historic Oregon Newspapers indexed text for ***The Amplifier***, **1 March 1943 p.4**, associating **Fain's Men's Store with 511 Main, Oregon City**. The original scan was not visually opened in that research session, so the address is **OCR/TEXT ONLY** pending scan inspection.

This materially strengthens the west-side sequence reconstruction but does **not** yet turn the P-1043 storefront into a documented 511 address. The photo is dated only 1930–1939; a contemporary 1930s exact-address source is still needed to prove continuity. Current state: **PROBABLE that the photographed Fain's storefront is 511 Main**.

Targeted follow-up did not recover a reliable historic exact-number source for **Sandwich Nook**, so it remains unresolved. A secondary 1932 `524½ Main` Tourist Hotel lead and later `502/506 Main` American Cleaners directory-summary data are retained as leads/context only, not promoted to controlling P-1043 address assignments. See `evidence/source-captures/1943-03-01-amplifier-fains-mens-store-511-main-ocr-lead-2026-09-05.md`.
'''
append_once(p1043_rel, p1043_block, p1043_marker)

lead_block = r'''### P-1043 address-sequence follow-up — Fain's later 511 anchor
<!-- P-1043 / Fain's 511 Main address follow-up — 2026-09-05 -->

`S-240` / `E-214` adds official Historic Oregon Newspapers **page text** placing **Fain's Men's Store at 511 Main** on 1 March 1943. Because the scan was not visually opened, keep that exact-address item **OCR/TEXT ONLY**. Read with visually verified P-1043, this makes `Fain's = 511` in the 1930s photographed state **PROBABLE**, not direct.

Next priority is now sharply defined: find **one 1930–1939 exact-address Fain source** and visually inspect it. Then use that fixed storefront to walk the P-1043 west-side sequence toward 509, 507, 505 and 503. **Sandwich Nook** remains the highest-value adjacent exact-address target; targeted online search in this pass did not resolve it. Tourist Hotel `524½` is secondary-only and American Cleaners `502/506` is later-only context, so neither is yet a controlling 1930s anchor.
'''
append_once("evidence/research-leads.md", lead_block, MARKER)

log_block = r'''### 2026-09-05 — P-1043 Fain's address-sequence follow-up
<!-- P-1043 / Fain's 511 Main address follow-up — 2026-09-05 -->
- Followed the steward request to tie readable P-1043 signs to numbered addresses rather than leaving the photo as a sign roster only.
- Official Historic Oregon Newspapers indexed text for *The Amplifier*, **1 March 1943 p.4**, places **Fain's Men's Store at 511 Main, Oregon City** (`S-240` / `E-214` / `BUS-099`).
- The original scan/PDF could not be opened in the current retrieval route, so the 1943 address remains **OCR/TEXT ONLY**, not visually verified.
- P-1043 independently and visually shows **FAIN'S MEN'S STORE** during 1930–1939; therefore Fain's=511 in the photographed state is now **PROBABLE / WORKING HYPOTHESIS**, not documented/direct continuity.
- Targeted searches did not resolve a historic exact address for **Sandwich Nook**. Preserved that as an unresolved search result, not negative evidence.
- Preserved—but did not promote—a secondary **Tourist Hotel 524½ Main (1932)** lead and later **American Cleaners 502/506 Main (1953+)** directory-summary context. The City historic-resource association of Oregon City Auto Parts with 1020–1024 Main is geographically outside the photographed block and is not used to assign the P-1043 sign.
- No annual closeout status changed.
'''
append_once("registers/research-log.md", log_block, MARKER)

crosswalk_block = r'''| `S-240` / `E-214` / `BUS-099` | `S-237` / `E-211` / `IMG-0758` | 1 Mar. 1943 *Amplifier* official page text gives Fain's Men's Store at **511 Main**; scan not visually opened, so OCR/TEXT ONLY. Combined with direct P-1043 sign, 1930s Fain's=511 is probable pending contemporary exact-address confirmation. <!-- P-1043 / Fain's 511 Main address follow-up — 2026-09-05 --> |'''
append_once("indexes/id-crosswalk.md", crosswalk_block, MARKER)

print("Integrated P-1043 / Fain's 511 Main follow-up as S-240 / E-214 / BUS-099")
