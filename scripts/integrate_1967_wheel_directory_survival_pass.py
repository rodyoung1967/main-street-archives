from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MARKER = "1967-wheel-directory-record-survival-pass-2026-09-07"
CAPTURE = ROOT / "evidence/source-captures/1967-wheel-record-survival-directory-pass-2026-09-07.md"


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


def write(rel, text):
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def append_once(rel, marker, block):
    text = read(rel)
    if marker in text:
        return
    if not text.endswith("\n"):
        text += "\n"
    write(rel, text + "\n" + block.strip() + "\n")


capture = """# 1967 Wheel — local record survival and 1965–1970 directory route

Date of research pass: **7 September 2026**  
Status: **BOUNDED ONLINE PASS — NO NAMED LAFARLETTE→WHEEL PROPRIETOR/SALE RECORD RECOVERED; LOCAL RECORD-SURVIVAL RISK AND A YEAR-BY-YEAR TELEPHONE-DIRECTORY ROUTE NOW DOCUMENTED**

## Question

Continue testing whether **Raye and/or Floyd LaFarlette acquired The Wheel at 503 Main around 1967**, and identify online substitutes for the unnamed municipal liquor application recorded before the printed 7 June 1967 Commission heading (`S-027` / `E-025`).

The controlling separation rule remains unchanged: business ownership, operation, tenancy, real-estate ownership, liquor licensing, and trade-name use are different propositions and must not be collapsed.

## 1. Oregon City later authorized destruction of 1966–1967 business-license applications

Official Oregon City Commission searchable text in WebDrawer record **4752045** records a later old-records disposal action. The Commission was given a list of old records and authorized the City Recorder to dispose of them under the Secretary of State records-management schedule. The listed series includes:

- **Business License Applications — Jan., 1966 to Dec., 1967**.

Source: City of Oregon City WebDrawer record 4752045  
URL: https://ormswd.synergydcs.com/HPRMWebDrawer/Record/4752045/File/document

The surrounding official searchable text places the disposal action in the **14 October 1976 adjourned regular Commission meeting**.

Classification: **PRIMARY MUNICIPAL SEARCHABLE TEXT / OCR-TEXT ONLY FOR THIS PASS**. The original page image did not open through the current retrieval route, so visual scan certification remains a **RETRIEVAL GAP**.

### Claim boundary

This is evidence of a real local records-survival problem across the suspected 1967 Wheel takeover interval. It does **not** prove that the separate Wheel liquor-license application was among the destroyed records. The disposal list names **Business License Applications** but does not separately identify liquor-license applications. Do not convert this later destruction authorization into evidence about who owned or operated The Wheel.

## 2. NYPL preserves a continuous telephone-directory sequence across the suspected takeover interval

The New York Public Library finding aid **Guide to the United States Telephone Directories** identifies an Oregon City series described as:

- **Oregon City — Includes Gladstone, West Linn. White and yellow pages.**

The finding aid lists the following relevant holdings:

- **1965**
- **1966**
- **1966–1967**
- **1967–1968**
- **1968–1969**
- **1969–1970**

Finding aid URL: https://nyplorg-data-archives.s3.amazonaws.com/uploads/collection/pdf_finding_aid/grdusteldir.pdf

Classification: **INSTITUTIONAL HOLDINGS METADATA / DIRECT COLLECTION CONTROL**. The finding aid establishes that the volumes are held; it does not establish their individual Wheel or LaFarlette contents because the directory pages themselves were not inspected online in this pass.

### Why these volumes matter

The sequence permits a year-by-year test of:

1. **Wheel Cafe / The Wheel / 503 Main** business listings;
2. telephone-number continuity or change from the documented **9106** number still printed in February 1959;
3. **Floyd / Raye / Rae LaFarlette / La Farlette** residential listings;
4. any occupation or business notation printed with a LaFarlette listing;
5. classified/yellow-page restaurant or cocktail-lounge listings that may name a proprietor or show a changed number.

A number or directory-entry change can bracket a business transition, but cannot by itself prove a sale or ownership change.

## 3. Other directory-access controls

Public genealogy directory indexes confirm a FamilySearch Library catalog entry titled **Oregon City (Clackamas County, Oregon) city directory: including Gladstone, West Linn and Willamette, also a buyers' guide and a complete classified business directory**. The live FamilySearch content was not successfully retrieved in this environment, so no 1967–1970 page content is certified from that route.

A currently indexed private-market listing also confirms the physical existence of a **1967–1968 Oregon telephone directory, area code 503, Oregon City / Gladstone**. No purchase was made and listing photographs did not expose the target Wheel/LaFarlette pages. Treat the sale listing only as a physical-copy/access lead, not historical content evidence.

## 4. 1969 EDR directory abstract — attachment gap

A City-hosted hazardous-materials technical memorandum states that EDR city-directory listings for **1953, 1960, 1964, 1969, 1974** and later years were reviewed and that the **EDR-City Directory Abstract is included in Appendix D**.

Official City document URL: https://www.orcity.org/DocumentCenter/View/12817/Tech-Memo-6-Most-Promising-Alternatives

The posted report text identifies selected notable Main Street businesses, but not 503 Main. The posted PDF available through the current route ends with the consultant report body and does not expose the promised Appendix D directory abstract. Therefore the raw **1969** 503 listing cannot be tested from the posted file.

Classification: **OFFICIAL SECONDARY REPORT / APPENDIX RETRIEVAL GAP**. Omission from the report's selected notable-listing narrative is not evidence that The Wheel or 503 Main was absent from the underlying 1969 directory.

## 5. 1959 telephone control retained

The 13 February 1959 *Clackamas County News* searchable/OCR text still prints:

- **WHEEL CAFE & LOUNGE**
- **503 Main St.**
- **Ph: 9106**

The same page shows other Oregon City-area businesses already using `OL 6-xxxx` format, making the subsequent Wheel number transition a useful directory question. This 1959 item remains **OCR/TEXT ONLY unless/until its original scan is visually certified**; earlier 1958 exact-address Wheel advertisements are already scan-certified in the archive.

## 6. Raye obituary target narrowed but text not recovered

The Clackamas Review obituary index identifies:

- **Grisham, Raye LaFarlette**
- born **30 Dec. 1918**
- died **30 June 2012**
- obituary: **11 July 2012, p. A9**

The City of Oregon City mausoleum/burial list independently records **RAYE W. GRISHAM**, maiden name **WEAVER**, death **6/30/2012**, age 94.

The actual 11 July 2012 obituary page was not recovered online in this pass. Therefore no claim is made that the obituary mentions The Wheel or gives an acquisition date. It is now an exact manual/microfilm page target rather than a vague obituary search.

## 7. Bounded direct-owner search result

Fresh searches were run using combinations and variants of:

- `Raye LaFarlette`, `Rae LaFarlette`, `Mrs. Floyd LaFarlette`, `Raye La Farlette`, `Raye E. LaFarlette`;
- `Floyd LaFarlette`, `Floyd E. LaFarlette`, `La Farlette`;
- `Wheel Cafe`, `Wheel Cafe & Lounge`, `Wheel Restaurant`, `The Wheel`, `503 Main`;
- `owner`, `proprietor`, `new management`, `sale`, `transfer`, `liquor`, `OLCC`;
- 1965–1970 date controls.

No contemporary online source recovered in this pass explicitly names Raye or Floyd as owner, proprietor, purchaser, operator, or licensee of The Wheel at 503 Main.

Classification: **BOUNDED ONLINE NO-HIT / COVERAGE STATEMENT ONLY**. This is not negative evidence.

## Research consequence

The evidence state for the suspected takeover remains:

- **DOCUMENTED:** The Wheel existed at 503 before the LaFarlette ownership date is known.
- **DOCUMENTED:** a 1967 municipal liquor application action for The Wheel at 503 appears in the meeting section immediately before the printed 7 June 1967 heading; applicant and transaction type are absent from the public text.
- **FAMILY / ORAL HISTORY:** Raye later owned The Wheel and sold it to Dick and Sheila Wiitanen.
- **PROBABLE / WORKING HYPOTHESIS:** c.1967 remains a strong acquisition/involvement hypothesis.
- **UNRESOLVED:** no recovered contemporary source yet connects a LaFarlette name directly to The Wheel or identifies the seller/predecessor.

## Highest-value next actions

Under existing **MF-052**:

1. inspect the NYPL Oregon City telephone directories **1965, 1966, 1966–67, 1967–68, 1968–69, 1969–70** for Wheel/503/LaFarlette and phone-number continuity;
2. inspect the permanent **OLCC Commission Meeting Records (agenda/exhibits/staff material)** around the local pre-7-June-1967 action;
3. retrieve the **11 July 2012 Clackamas Review, p. A9** Raye LaFarlette Grisham obituary as a possible retrospective ownership/date clue;
4. continue to treat any missing local 1966–67 ordinary business-license file as a survival/retrieval issue, not proof of no transfer.

No institutional request, purchase, email, phone call, or other outreach was made in this pass.
"""

if CAPTURE.exists():
    if CAPTURE.read_text(encoding="utf-8") != capture:
        raise SystemExit(f"{CAPTURE}: unexpected existing content")
else:
    CAPTURE.write_text(capture, encoding="utf-8")

append_once(
    "MANUAL-FOLLOWUP.md",
    MARKER,
    f"""### MF-052 refinement — 1965–1970 Oregon City directories and 1966–67 local record survival
<!-- {MARKER} -->

A 7 September 2026 focused continuation found two materially useful controls for the unresolved LaFarlette→Wheel acquisition date. First, Oregon City's later old-record disposal action explicitly included **Business License Applications, Jan. 1966–Dec. 1967**; this creates a genuine local records-survival risk but does **not** prove that the separate Wheel liquor application was destroyed. Second, the **New York Public Library** finding aid confirms a continuous Oregon City/Gladstone/West Linn telephone-directory run for **1965, 1966, 1966–67, 1967–68, 1968–69, and 1969–70**.

**Next manual action under MF-052, not yet sent:** inspect those six directory volumes for **The Wheel / Wheel Cafe / 503 Main / 9106 / later number**, plus **Floyd, Raye/Rae LaFarlette and La Farlette** variants. Use the permanent OLCC Commission agenda/exhibit route in parallel. Also retrieve the exact **11 July 2012 Clackamas Review p. A9** obituary for **Raye LaFarlette Grisham**; the index is recovered, but the obituary text is not online in the current route.

Source capture: `evidence/source-captures/1967-wheel-record-survival-directory-pass-2026-09-07.md`.
""",
)

append_once(
    "evidence/research-leads.md",
    MARKER,
    f"""### 7 September 2026 — year-by-year directory bracket for the LaFarlette/Wheel transition
<!-- {MARKER} -->

The strongest new non-OLCC route is now a confirmed **1965–1970 Oregon City telephone-directory sequence** held by NYPL: 1965, 1966, 1966–67, 1967–68, 1968–69, and 1969–70, covering Oregon City/Gladstone/West Linn. Compare **Wheel / 503 Main / telephone number** and **LaFarlette household/name variants** year by year. A directory-number or listing transition may narrow the takeover interval but is not ownership proof by itself.

Oregon City's 1976 disposal authorization separately lists **Business License Applications, Jan. 1966–Dec. 1967**, so non-recovery of an ordinary local business-license application in the suspected takeover window must be treated as a survival gap. The permanent OLCC Commission records remain the higher-value applicant/licensee route. See `evidence/source-captures/1967-wheel-record-survival-directory-pass-2026-09-07.md`; coordinate manual work under `MF-052`.
""",
)

append_once(
    "businesses/the-wheel.md",
    MARKER,
    f"""## 7 September 2026 — 1965–1970 directory and local-record survival control
<!-- {MARKER} -->

The c.1967 LaFarlette acquisition hypothesis remains **unproved** after another owner/proprietor sweep. A later Oregon City records-disposal action explicitly included **Business License Applications, Jan. 1966–Dec. 1967**, establishing a records-survival risk but not proving that the separate 1967 Wheel liquor application was destroyed. NYPL, however, confirms a continuous Oregon City/Gladstone/West Linn telephone-directory sequence for **1965 through 1969–70**. Those volumes are now the best non-OLCC route for bracketing a Wheel listing/phone-number change and the first local LaFarlette household/business appearance. See `evidence/source-captures/1967-wheel-record-survival-directory-pass-2026-09-07.md` and `MF-052`.
""",
)

append_once(
    "registers/research-log.md",
    MARKER,
    f"""### 7 September 2026 — 1967 Wheel directory / record-survival continuation
<!-- {MARKER} -->

- Re-synced current `main` before the continuation; parallel 1955-sale work was left untouched.
- Repeated LaFarlette/Wheel owner-proprietor searches for 1965–1970; no contemporary direct LaFarlette→Wheel hit recovered. Classified as bounded no-hit only.
- Recovered official Oregon City searchable text showing a later disposal authorization that included **Business License Applications, Jan. 1966–Dec. 1967**. This is a local records-survival control, not proof that the liquor application was destroyed.
- Confirmed via NYPL's institutional finding aid that Oregon City/Gladstone/West Linn telephone directories survive for **1965, 1966, 1966–67, 1967–68, 1968–69, 1969–70**.
- Confirmed that a City-hosted technical memo used a **1969 EDR city directory**, but its promised Appendix D abstract is not exposed in the posted report route; preserved as an attachment retrieval gap.
- Narrowed Raye's obituary to **Clackamas Review, 11 July 2012, p. A9**; actual obituary text remains unrecovered.
- Cross-record propagation decision: because this batch establishes research-route/survival facts rather than a new ownership/occupancy event, no new timeline acquisition event, owner, licensee, or seller was created. Updated the source capture, `MF-052`, research leads, The Wheel research page, and this log only.
- No outreach or purchase was made.
""",
)
