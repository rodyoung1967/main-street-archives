from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MARKER = "1967-wheel-olcc-permanent-commission-route-2026-09-07"
CAPTURE = ROOT / "evidence/source-captures/1967-wheel-olcc-permanent-commission-records-route-2026-09-07.md"


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


def write(rel, text):
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def replace_required(rel, old, new):
    text = read(rel)
    if new in text:
        return
    if old not in text:
        raise SystemExit(f"{rel}: required synchronization text not found: {old[:160]!r}")
    write(rel, text.replace(old, new, 1))


def append_once(rel, marker, block):
    text = read(rel)
    if marker in text:
        return
    if not text.endswith("\n"):
        text += "\n"
    write(rel, text + "\n" + block.strip() + "\n")


capture_text = """# 1967 Wheel — OLCC permanent Commission-record route

Date of research pass: **7 September 2026**  
Status: **ONLINE ROUTE REFINED — NO NAMED APPLICANT RECOVERED; PERMANENT OLCC COMMISSION RECORD SERIES IDENTIFIED AS THE HIGHEST-SURVIVAL-PROBABILITY NEXT SOURCE**

## Purpose

Continue the focused test of the project-steward recollection that **Raye and/or Floyd LaFarlette may have acquired The Wheel around 1967**, with priority on the underlying licensing record behind `S-027` / `E-025`.

The evidence-separation rule remains controlling: a municipal or OLCC liquor action is not automatically a business sale, business ownership, real-estate ownership, tenancy, or trade-name transfer. A named applicant/licensee and transaction context are still required.

## Local municipal control re-confirmed

The official Oregon City Commission searchable text for WebDrawer record **4723655**, bound page **453**, records a motion by Conrad, seconded by Danielson, authorizing the mayor to sign a liquor application for:

- **the Wheel located at 503 Main Street**; and
- **4-Falls Tavern located at 1206 - 8th Street**.

The vote is recorded as **McElroy, Conrad, Danielson — Ayes; None — Nays**. The same preceding-meeting section then adopts a proposed salary schedule effective 1 July 1967 and new League of Oregon Cities Blue Cross rates effective 1 August 1967. Only after that meeting adjourns does the page print the heading **Oregon City, Oregon June 7, 1967 — REGULAR MEETING**. The June 7 roll call names McElroy and Conrad, not Danielson.

Classification: **PRIMARY MUNICIPAL SEARCHABLE TEXT / DATE-BOUNDARY CONTROL**. The original page image still cannot be opened through the current retrieval route, so scan-level visual re-certification remains a **RETRIEVAL GAP**.

Safe date wording remains **before 7 June 1967, exact preceding-meeting date unresolved**. Repeated targeted searches for May/early-June meeting headings did not recover the missing preceding heading. Do not infer a specific May date from meeting cadence.

## Oregon State Archives retention-schedule breakthrough

The Oregon State Archives' official January 2024 records-retention schedule for the Oregon Liquor Control Commission, schedule **2001-0010**, Administration / Commission, identifies:

- **001 Commission Meeting Records, 1934–[ongoing]**;
- records include **minutes, agendas, and exhibits**;
- the schedule directs that those minutes, agendas, and exhibits be retained **permanently** and transferred to the **State Archives after 20 years**;
- meeting tapes are a separate temporary record series.

Official indexed/searchable schedule URL:
https://sos.oregon.gov/archives/Documents/recordsmgmt/sched/schedule-liquor-control.pdf

Classification: **OFFICIAL STATE-ARCHIVES SEARCHABLE/INDEXED TEXT / RESEARCH-ROUTE EVIDENCE**. The PDF itself returned a retrieval error in the current browser path, so this pass does not claim visual certification of the schedule page.

## Why this changes the search strategy

The same current schedule gives ordinary **License Files**, **License Tradename Cards**, and **Licensee History Cards** finite retention periods rather than permanent retention. Therefore a missing 1967 operational license file cannot be treated as evidence that no application, license change, transfer, or licensee existed; destruction or non-transfer is a records-survival possibility.

The permanent **OLCC Commission Meeting Records — especially agendas and exhibits — are now the highest-survival-probability state record class** for recovering the identity behind the 1967 Wheel action. A Commission exhibit or agenda attachment could potentially preserve the applicant/licensee name, staff recommendation, premises/trade name, license class, or change/transfer context even if the ordinary licensing file no longer survives.

This is a research-route conclusion, not proof that the Wheel application was actually included as an OLCC Commission exhibit. The specific 1967 packet still has to be located.

## Online search result

Targeted public-web searches were repeated for combinations of:

- **The Wheel / Wheel Cafe / Wheel Restaurant / 503 Main / Oregon City**;
- **Raye LaFarlette / Rae LaFarlette / Mrs. Floyd LaFarlette / Floyd E. LaFarlette / La Farlette / Raye Grisham**;
- **OLCC / Oregon Liquor Control Commission / liquor application / license / transfer / new management / proprietor**;
- 1966–1970 date controls.

No contemporary online source was recovered that names Raye or Floyd as the Wheel's 1967 applicant, purchaser, proprietor, operator, or licensee. No digitized/indexed 1967 OLCC Commission agenda/exhibit for the Wheel was recovered in this pass.

Classification: **BOUNDED ONLINE NO-HIT / RETRIEVAL STATEMENT ONLY**. It is not evidence that the LaFarlettes were uninvolved.

## Highest-value next record

Under existing manual follow-up **MF-052**, prioritize the Oregon State Archives / OLCC permanent **Commission Meeting Records** around the local action **before 7 June 1967**. Search or request inspection by:

- trade name: **The Wheel / Wheel Cafe / Wheel Cafe & Lounge / Wheel Restaurant**;
- premises: **503 Main Street, Oregon City**;
- applicant variants: **Raye LaFarlette, Rae LaFarlette, Mrs. Floyd LaFarlette, Floyd E. LaFarlette, Raye Grisham**;
- predecessor controls: **Albert D. Flor, Mrs. Albert D. Flor, Margaret/Marge Remus, Kwality Cafe**.

The immediate objective is to determine **applicant/licensee identity and transaction type**. If a LaFarlette is named, then work backward to the prior licensee/proprietor/seller. If a different person is named, that person becomes the preceding-proprietor target.

## Current acquisition conclusion

**1967 remains a leading LaFarlette acquisition/involvement hypothesis, not a proved purchase date.** The municipal action is real and specifically tied to The Wheel at 503, but the public minutes do not name the applicant or say whether the action was a renewal, new license, change of licensee, ownership transfer, or another licensing event.

No institutional request, email, phone call, paid lookup, or manual outreach was sent in this pass.
"""

if CAPTURE.exists():
    existing = CAPTURE.read_text(encoding="utf-8")
    if existing != capture_text:
        raise SystemExit(f"{CAPTURE}: unexpected existing content")
else:
    CAPTURE.write_text(capture_text, encoding="utf-8")

# Correct the canonical S-027 / E-025 date boundary in both Markdown and YAML.
replace_required(
    "evidence/source-register.md",
    "## S-027 — Oregon City Commission minutes, 7 June 1967\nSource/location: https://ormswd.synergydcs.com/HPRMWebDrawer/Record/4723655/File/document\nRelated evidence: `E-025`\nNotes: Liquor application for the Wheel at 503 Main Street. Related evidence E-025.",
    "## S-027 — Oregon City Commission bound minutes, Wheel liquor action before 7 June 1967\nSource/location: https://ormswd.synergydcs.com/HPRMWebDrawer/Record/4723655/File/document\nRelated evidence: `E-025`\nNotes: Bound page 453 authorizes the mayor to sign a liquor application for the Wheel at 503 Main Street in the closing portion of the meeting immediately preceding the printed 7 June 1967 heading. Exact preceding-meeting date and applicant/licensee remain unresolved; do not cite the action as exactly 7 June 1967. Related evidence E-025.",
)

replace_required(
    "evidence/evidence-register.md",
    "## E-025 — The Wheel at 503 Main, Oregon City Commission, 7 June 1967\nType: Primary municipal record  \nSources: `S-027`  \nClaims: Commission minutes authorize the mayor to sign a liquor application for \"the Wheel located at 503 Main Street.\"  \nConfidence: Very High for address and name as of that date.",
    "## E-025 — The Wheel at 503 Main, municipal liquor action before 7 June 1967\nType: Primary municipal searchable text; exact preceding-meeting date / scan re-certification unresolved  \nSources: `S-027`  \nClaims: Bound Commission page 453 authorizes the mayor to sign a liquor application for \"the Wheel located at 503 Main Street\" in the meeting section immediately preceding the printed 7 June 1967 heading. The public text does not name the applicant/licensee or identify the action as a renewal, new license, ownership/licensee transfer, or sale.  \nConfidence: Very High for the printed business/address action and its placement before the 7 June heading; unresolved for exact preceding-meeting date, applicant identity, transaction type, and acquisition significance.",
)

replace_required(
    "database/sources.yml",
    "  - id: S-027\n    name: Oregon City Commission minutes, 7 June 1967\n    url: https://ormswd.synergydcs.com/HPRMWebDrawer/Record/4723655/File/document\n    notes: Liquor application for the Wheel at 503 Main Street. Related evidence E-025.",
    "  - id: S-027\n    name: Oregon City Commission bound minutes, Wheel liquor action before 7 June 1967\n    url: https://ormswd.synergydcs.com/HPRMWebDrawer/Record/4723655/File/document\n    notes: Bound page 453 authorizes the mayor to sign a liquor application for the Wheel at 503 Main Street in the meeting section immediately before the printed 7 June 1967 heading. Exact preceding-meeting date and applicant/licensee are unresolved; do not cite the action as exactly 7 June 1967. Related evidence E-025.",
)

replace_required(
    "database/evidence.yml",
    "  - id: E-025\n    name: \"The Wheel at 503 Main, Oregon City Commission, 7 June 1967\"\n    type: Primary municipal record\n    claims:\n      - Commission minutes authorize a liquor application for the Wheel located at 503 Main Street.\n    confidence: Very High for address and name as of that date.",
    "  - id: E-025\n    name: \"The Wheel at 503 Main, municipal liquor action before 7 June 1967\"\n    type: Primary municipal searchable text; exact preceding-meeting date and scan re-certification unresolved\n    claims:\n      - Bound Commission page 453 authorizes the mayor to sign a liquor application for the Wheel located at 503 Main Street in the meeting section immediately preceding the printed 7 June 1967 heading.\n      - The public text does not identify the applicant/licensee or establish whether the action was a renewal, new license, ownership/licensee transfer, business sale, or another licensing event.\n    confidence: Very High for the business/address action and its placement before the 7 June heading; unresolved for exact preceding-meeting date, applicant identity, transaction type, and acquisition significance.",
)

# Correct remaining current narrative occurrences that accidentally promoted the heading date.
replace_required(
    "buildings/503-main.md",
    "- Primary municipal evidence (`E-025`): 7 June 1967 Commission minutes, liquor application for \"the Wheel located at 503 Main Street.\"",
    "- Primary municipal evidence (`E-025`): a 1967 Commission bound page records a liquor application for \"the Wheel located at 503 Main Street\" in the meeting section immediately **before the printed 7 June 1967 heading**; exact preceding-meeting date and applicant remain unresolved.",
)

replace_required(
    "evidence/source-captures/morton-wheel-1945-1947-online-access-and-lafarlette-control-pass-2026-09-06.md",
    "The repository already directly anchors **Wheel Cafe & Lounge, 503 Main Street, Oregon City, phone 9106** in August and November 1958, with a 1959 continuation lead, and the 7 June 1967 Oregon City Commission minutes record a liquor application for the Wheel at 503 Main. The public minute text does not name the applicant.",
    "The repository already directly anchors **Wheel Cafe & Lounge, 503 Main Street, Oregon City, phone 9106** in 1958, with a 1959 continuation lead, and a 1967 Oregon City Commission bound page records a liquor application for the Wheel at 503 Main in the meeting section immediately **before the printed 7 June heading**. The exact preceding-meeting date and applicant remain unresolved.",
)

replace_required(
    "evidence/source-captures/cchs-p1311-1955-1965-bluff-4th-looking-northwest-wheel-503-505-tavern-2026-09-05.md",
    "For **503 Main**, the image independently complements the 30 November 1960 **Wheel Cafe** newspaper anchor (`E-044`) and the later exact 7 June 1967 municipal 503 Main record (`E-025`).",
    "For **503 Main**, the image independently complements the 30 November 1960 **Wheel Cafe** newspaper anchor (`E-044`) and the later **1967 municipal liquor-action record before the printed 7 June heading** (`E-025`).",
)

# Add the permanent-record survival route directly to the business page.
replace_required(
    "businesses/the-wheel.md",
    "The application text names no applicant or licensee and does not prove a LaFarlette purchase. See [`1967-wheel-liquor-date-boundary-lafarlette-acquisition-control-2026-09-07.md`](../evidence/source-captures/1967-wheel-liquor-date-boundary-lafarlette-acquisition-control-2026-09-07.md).",
    "The application text names no applicant or licensee and does not prove a LaFarlette purchase. See [`1967-wheel-liquor-date-boundary-lafarlette-acquisition-control-2026-09-07.md`](../evidence/source-captures/1967-wheel-liquor-date-boundary-lafarlette-acquisition-control-2026-09-07.md). A follow-up State Archives retention-schedule pass identifies **OLCC Commission Meeting Records (minutes, agendas, exhibits), 1934–ongoing, as permanent records transferred to the State Archives after 20 years**. That permanent series is now the preferred survival route for the underlying 1967 applicant/license context; ordinary license files/cards have finite retention. See [`1967-wheel-olcc-permanent-commission-records-route-2026-09-07.md`](../evidence/source-captures/1967-wheel-olcc-permanent-commission-records-route-2026-09-07.md).",
)

# Correct and sharpen the unsent OLCC request draft without sending it.
replace_required(
    "registers/research-requests/morton-wheel-and-oregon-city-wheel-pre-raye-ownership-bridge-request-2026-09-05.md",
    "Contemporary newspaper advertising places **Wheel Cafe & Lounge at 503 Main Street by 22 August 1958**, telephone **9106**. Oregon City Commission minutes later place **the Wheel at 503 Main Street on 7 June 1967** in connection with a liquor application, but the public minute text available to me does not identify the individual applicant.",
    "Contemporary newspaper advertising places **Wheel Cafe & Lounge at 503 Main Street by 1958**, telephone **9106**. Oregon City Commission bound page 453 later records **the Wheel at 503 Main Street** in connection with a liquor application in the meeting section immediately **before the printed 7 June 1967 heading**; the exact preceding-meeting date and individual applicant are not identified in the public text.\n\nThe Oregon State Archives' January 2024 OLCC retention schedule identifies **Commission Meeting Records (minutes, agendas, and exhibits), 1934–ongoing, as permanent records transferred to the State Archives after 20 years**. If the ordinary 1967 license file/history card no longer survives, please prioritize any **1967 OLCC Commission agenda, minutes, exhibit packet, staff recommendation, or related permanent meeting record** that may identify the applicant/licensee or transaction type for The Wheel at 503 Main.",
)

# Add the new route to the existing date-boundary capture.
append_once(
    "evidence/source-captures/1967-wheel-liquor-date-boundary-lafarlette-acquisition-control-2026-09-07.md",
    MARKER,
    f"""## 7 September 2026 — OLCC permanent Commission-record survival route
<!-- {MARKER} -->

A follow-up Oregon State Archives retention-schedule pass materially improves the record-survival strategy. The official January 2024 OLCC schedule identifies **Commission Meeting Records, 1934–ongoing** — specifically **minutes, agendas, and exhibits** — as **permanent** records transferred to the State Archives after 20 years. Ordinary License Files, License Tradename Cards, and Licensee History Cards are finite-retention series under the current schedule.

Therefore the highest-value surviving state target is now the **OLCC Commission meeting agenda/exhibit packet around the local Wheel action before 7 June 1967**, not an assumption that the ordinary licensing file still exists. No digitized target packet or named LaFarlette applicant was recovered online in this pass. See `evidence/source-captures/1967-wheel-olcc-permanent-commission-records-route-2026-09-07.md`.

No request was sent.
""",
)

# Preserve the route under the existing MF-052 dashboard item without creating a duplicate manual item.
append_once(
    "MANUAL-FOLLOWUP.md",
    MARKER,
    f"""### MF-052 refinement — 1967 Wheel OLCC permanent Commission-record route
<!-- {MARKER} -->

The 7 September 2026 acquisition pass identified a materially better survival route for the **1967 Wheel / 503 Main** liquor action. Oregon State Archives' January 2024 OLCC schedule says **Commission Meeting Records (minutes, agendas, exhibits), 1934–ongoing** are **permanent** and transferred to the State Archives after 20 years. Ordinary license files/history/tradename cards have finite retention, so non-recovery of a 1967 operational file would be a **records-survival/retrieval gap**, not negative evidence.

**Next manual action under MF-052, not yet sent:** prioritize the permanent OLCC Commission agenda/exhibit packet around the Oregon City action **before 7 June 1967** and search **The Wheel / 503 Main / Raye or Rae LaFarlette / Mrs. Floyd LaFarlette / Floyd E. LaFarlette / Raye Grisham**, with **Albert D. Flor / Margaret or Marge Remus / Kwality Cafe** as predecessor controls. The immediate question is applicant/licensee identity and transaction type.

Source capture: `evidence/source-captures/1967-wheel-olcc-permanent-commission-records-route-2026-09-07.md`.
""",
)

append_once(
    "evidence/research-leads.md",
    MARKER,
    f"""## RL-1967-WHEEL-OLCC — Recover the permanent OLCC Commission exhibit behind the 1967 Wheel action
<!-- {MARKER} -->

A 7 September 2026 State Archives retention-schedule pass shows that **OLCC Commission Meeting Records — minutes, agendas, exhibits — are permanent from 1934 onward and transferred after 20 years**, while ordinary license files/cards are finite-retention series. The 503 Main Wheel action occurs in Oregon City's bound minutes **before the printed 7 June 1967 heading**, but the public text omits the applicant and transaction type. Highest-value next evidence is the corresponding OLCC Commission agenda/exhibit/staff packet. Treat non-recovery of an ordinary license file as a survival gap, not evidence against a 1967 transfer. Coordinate under `MF-052`; do not send a request without steward authorization.
""",
)

append_once(
    "registers/research-log.md",
    MARKER,
    f"""## 7 September 2026 — 1967 Wheel OLCC permanent-record route
<!-- {MARKER} -->

- Re-confirmed the Oregon City bound-page sequence: the Wheel/503 liquor action is **before the printed 7 June 1967 heading**, exact preceding-meeting date unresolved.
- Repeated targeted online searches did not recover a named LaFarlette applicant or a digitized 1967 OLCC Wheel packet; bounded retrieval result only.
- Oregon State Archives' January 2024 OLCC retention schedule identifies **Commission Meeting Records (minutes, agendas, exhibits), 1934–ongoing** as permanent and transferred after 20 years.
- Current schedule shows ordinary license files/history/tradename cards are finite-retention records; missing 1967 operational files therefore cannot be treated as negative evidence.
- Corrected stale `S-027` / `E-025` exact-7-June wording in canonical Markdown/YAML and related narratives.
- Refined existing `MF-052` and the unsent OLCC request draft; **no institutional request was sent**.
""",
)

print("Integrated 1967 Wheel OLCC permanent Commission-record route and corrected date boundary.")
