#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def write(rel: str, text: str) -> None:
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    if p.exists() and p.read_text(encoding="utf-8") == text:
        return
    p.write_text(text, encoding="utf-8")


def replace_once(rel: str, old: str, new: str) -> None:
    text = read(rel)
    if new in text and old not in text:
        return
    if old not in text:
        raise RuntimeError(f"Expected text not found in {rel}: {old[:120]!r}")
    write(rel, text.replace(old, new, 1))


def insert_once(rel: str, marker: str, insert: str, unique: str) -> None:
    text = read(rel)
    if unique in text:
        return
    if marker not in text:
        raise RuntimeError(f"Insertion marker not found in {rel}: {marker[:120]!r}")
    write(rel, text.replace(marker, insert + marker, 1))


def existing_or_next_id(text: str, prefix: str, title_fragment: str) -> str:
    m = re.search(rf"## ({re.escape(prefix)}-\d+) — [^\n]*{re.escape(title_fragment)}", text, re.I)
    if m:
        return m.group(1)
    nums = [int(n) for n in re.findall(rf"\b{re.escape(prefix)}-(\d+)\b", text)]
    return f"{prefix}-{max(nums, default=0) + 1:03d}"


source_register = read("evidence/source-register.md")
evidence_register = read("evidence/evidence-register.md")
SID = existing_or_next_id(source_register, "S", "Water Rent Record Book 3")
EID = existing_or_next_id(evidence_register, "E", "Water Rent Book 3")

ledger = f'''# 1914–1915 Water Rent Record Book 3 — target and Fifth/Main visual audit

Status: **official primary municipal source; relevant target/Fifth-Main pages visually reviewed from the full-resolution City scan; 1915 target-source reconciliation complete**

Source ID: `{SID}`  
Evidence ID: `{EID}`

Official source page:  
https://www.orcity.org/1710/Historic-Documents-and-Research

Direct official Book 3 document URL:  
https://www.orcity.org/DocumentCenter/View/6213/1914-1915-Water-Rent-Record-Book-3

Preserved reviewed page extracts:  
`records/municipal/water-rent/1914-1915-book-3-review-pages/`

## Review scope and preservation

On 28 August 2026 the official City PDF was downloaded directly and verified as a PDF. The complete source contains **139 scanned PDF pages**. For the project-specific audit, official PDF pages **1–12** were extracted at source quality and the relevant downtown Main/Fifth sequences were visually inspected from those full-resolution scans. The preserved extracts include the target Main Street run and nearby Fifth Street records used below.

This is a **target-source audit**, not a claim that all 139 pages were exhaustively transcribed. The 1915 annual standard requires relevant online source classes to be reviewed for the established target categories; these reviewed municipal pages cover the 501/503/possible-505 sequence, nearby Fifth Street address anchors, and the notation question that was left open by the earlier screenshot review.

The earlier 23 August user-supplied screenshots remain useful provenance, but the readings below are based on the official high-resolution City scan.

## Target Main Street sequence — visually confirmed

Official PDF page 7 / printed ledger page 5 shows the Block 4 Main Street sequence:

**511 Main → 509 Main → 507 Main → [unnumbered entry] → 503 Main → 503½ Main → 501 Main**

**G. A. Harding, Agt.** appears repeatedly as owner/agent in this group.

The entry between 507 and 503 has **no house number written in the house-number field**. Because 505 is the missing odd number in that numerical position, it remains a plausible 505 account, but the ledger does not itself write **505** there. Do not promote the row to an exact 505 address without corroboration.

## The standalone `V` notation — now strongly supported as vacancy

The unnumbered row between 507 and 503 contains a standalone handwritten **V** in the tenant field.

The earlier review treated `V = Vacant` as probable but lacked a comparison example. The official scan supplies independent comparison rows on PDF page 6 / printed ledger page 4:

- **523 Main**, owner **Schram Estate** (handwriting abbreviated), classification **Saloon** — standalone **V** in the tenant field;
- **521 Main**, owner **Ed Kelly**, classification **Barber Shop** — standalone **V** in the tenant field.

These unrelated accounts use the same one-letter mark where a tenant name would otherwise appear. That repeated pattern **strongly supports / makes it very likely that `V` is the ledger's vacancy notation**. No printed glossary or formal key has yet been located, so preserve the wording as a high-confidence interpretation rather than a quoted definition.

Some `V` rows still carry account/payment information. Therefore `V` should not be interpreted as proof that water service was physically disconnected; it is evidence about the tenant/occupancy status recorded by the ledger.

### Consequence for the possible 505 row

Two questions must remain separate:

1. **What does V mean?** — now **high confidence: vacant/vacancy notation**.
2. **Is the blank-number row 505 Main?** — still **plausible / moderate-confidence hypothesis only** because the number is not written.

Accordingly, the ledger materially strengthens the hypothesis that **505 was vacant during at least part of the 1914–1915 ledger period**, but it still does **not** prove the sentence “505 Main was vacant” as an exact-address fact.

The ledger spans more than one year and the row does not establish the exact month in which the `V` condition applied.

## 503, 503½ and 501 — classifications visible

The same printed ledger page directly records:

- **503 Main — Store**;
- **503½ Main — Barber Shop**;
- **501 Main — layered/changed Restaurant and Saloon classification writing**.

The 503 and 503½ tenant names remain too faint/layered for a responsible final transcription. The 503 writing may be worth comparing with the independently documented 1914 L. Hylton record, but no identity is assigned from visual resemblance alone.

The 501 classification is layered across the multi-year ledger record and should not be converted into a single dated 1915 business or occupant. Likewise, a ledger classification is a municipal use/account description, not automatically a trade name or ownership statement.

The separate 503½ row confirms that the ledger explicitly used half-addresses and should **not** be treated as a disguised notation for 505.

## New exact Fifth Street anchors

### 110 Fifth — Stable

Official PDF page 5 / printed ledger page 3 directly records:

- **110 Fifth**;
- **Block 3**;
- classification **Stable**.

This is a high-confidence **1914–1915 ledger-period address/use anchor**. The ledger alone does not identify the exact month/year within the book's span.

The tenant field contains layered/crossed handwriting that appears **consistent with “Scripture & May”**, but the overwriting prevents a sufficiently confident transcription. Preserve this only as a **probable visual lead**.

Important limits:

- do **not** state that Scripture & May definitely occupied 110 Fifth from this scan alone;
- do **not** backdate their independently verified **108 Fifth** address from 1916 to 1915;
- do **not** equate **110 Fifth / Stable** with the newspaper's unnumbered **Fashion Stable, Fifth between Main and Water** without an independent bridge.

The 110 Fifth record is nevertheless an important new numbered anchor for testing both questions.

### 107 Fifth — Blacksmith

Official PDF page 7 / printed ledger page 5 directly records:

- **107 Fifth**;
- **Block 4**;
- classification **Blacksmith**.

The tenant handwriting is too faint for a confident transcription. This is a useful opposite-side Fifth Street anchor, but it is not assigned to Scripture & May, S. F. Scripture, or another named blacksmith solely from trade and location.

## Comparison with 1916–1917 Book 4

The later Book 4 review shows:

**511 → 509 → 507 → 503 → 503½ → 501 Main**

with no separate 505 entry in the expected position. Taken with Book 3:

- **1914–15:** a blank-number account appears between 507 and 503 and carries the now-strongly-supported vacancy mark `V`;
- **1916–17:** 505 is absent from the expected sequence while 503 and 503½ remain separately recorded.

This strengthens the long-running 505 inactivity/vacancy hypothesis but does not establish why the address is blank/absent or exclude shared service, storage, unlisted use, or another municipal-account arrangement.

## Confidence / handling table

| Finding | Status |
| --- | --- |
| 503 Main is explicitly recorded | **Very High / visually verified** |
| 503½ Main is explicitly separate | **Very High / visually verified** |
| 503 classified Store | **Very High / visually verified** |
| 503½ classified Barber Shop | **Very High / visually verified** |
| 501 carries layered Restaurant/Saloon classification | **High / visually verified; exact timing unresolved** |
| G. A. Harding, Agt. repeats in target group | **Very High / visually verified** |
| Blank-number row exists between 507 and 503 | **Very High / visually verified** |
| Blank row carries standalone V in tenant field | **Very High / visually verified** |
| `V` means vacancy/vacant | **High-confidence interpretation; no glossary found** |
| Blank row equals 505 Main | **Plausible / moderate hypothesis only** |
| “505 Main was vacant” as an exact-address fact | **Not established** |
| 110 Fifth / Block 3 / Stable | **Very High / visually verified ledger-period anchor** |
| Tenant at 110 appears to include Scripture & May | **Probable visual lead only; layered handwriting** |
| 110 Fifth is Fashion Stable | **Unresolved; do not infer** |
| 107 Fifth / Block 4 / Blacksmith | **Very High / visually verified ledger-period anchor** |
| 107 Fifth tenant identity | **Unresolved** |

## Remaining ledger-specific questions

The relevant 1915 target audit is complete. Remaining questions are historical interpretation/bridge questions rather than unperformed target-page review:

1. Find a formal ledger key or municipal instruction explicitly defining `V`, if one survives.
2. Find an independent numbered source that either assigns or rejects **505 Main** for the blank row.
3. Resolve the faint/layered tenant names at 503, 503½ and 110 Fifth only with better handwriting comparison or independent documentary evidence.
4. Test whether **110 Fifth Stable** is related to the newspaper's **Fashion Stable**; do not assume identity from the shared stable use.
5. Test the probable Scripture & May reading at 110 against directories, licenses, advertisements and later 108 Fifth evidence.
'''
write("evidence/source-captures/1914-1915-water-rent-record-book-3-visual-review.md", ledger)

assessment = f'''# 505 Main — 1914–1917 vacancy / occupancy assessment

Status: **working synthesis from visually reviewed municipal water ledgers plus directory/newspaper evidence**

Primary Book 3 audit: `evidence/source-captures/1914-1915-water-rent-record-book-3-visual-review.md` (`{SID}` / `{EID}`)

## 1914–1915

The official 1914–1915 water-rent ledger scan visually shows the Main Street sequence:

**511 → 509 → 507 → [unnumbered entry] → 503 → 503½ → 501**

The unnumbered entry between 507 and 503 contains a standalone handwritten **V** in the tenant field. Because 505 is the missing odd-numbered address in that exact numerical position, the entry is a plausible 505 account. The house-number field, however, is blank.

### What the new comparison review changes

The earlier assessment had two uncertain steps: whether the row was 505 and whether `V` meant vacant. The high-resolution official scan now shows the **same standalone V in the tenant field of unrelated accounts at 523 Main and 521 Main**. Those rows otherwise behave like normal property accounts and use V where a tenant name would be expected.

That makes **V = vacant/vacancy notation a high-confidence interpretation**, although no printed ledger glossary has been found. It does **not** solve the separate address question.

The evidentiary chain is therefore now:

1. blank row exists between 507 and 503 — **direct / very high**;
2. that row contains `V` — **direct / very high**;
3. `V` means vacant — **strongly supported / high confidence**;
4. blank row equals 505 Main — **plausible / moderate hypothesis only**.

Working confidence that **505 was vacant during at least some portion of the 1914–15 ledger period remains moderate, but is materially strengthened** because the vacancy notation itself is no longer a one-off interpretation. The limiting uncertainty is now principally the missing house number.

Important chronological caution: the ledger covers a multi-year period. It does not establish the exact month in which the blank/V condition applied. A V row can also carry account/payment information, so vacancy should not be equated automatically with physical disconnection of water service.

## 1916–1917

The visually reviewed 1916–1917 water-rent ledger shows:

**511 → 509 → 507 → 503 → 503½ → 501**

There is **no separate 505 Main account** in the expected position. This is a positive visual observation, not OCR silence. The ledger separately recognizes 503½ and multiple other half-addresses, so 503½ should not be treated as a disguised 505.

Independent corroboration comes from Oregon City's historic-resource research, which reports that the **1916 city directory listed no business at 505 Main**. Targeted 1916–17 newspaper research has likewise failed to identify an occupant at 505.

Taken together, these clues support the working conclusion that **505 Main was probably vacant or at least lacked a separately operating/listed business and separate municipal water account in 1916**.

Working confidence for **probable vacancy / no active separately listed business in 1916: medium-high**.

This still falls short of absolute proof of physical vacancy because possibilities such as shared water service, unlisted use, storage, or another accounting arrangement cannot be excluded.

## Comparative conclusion

- **1914–15:** a strong vacancy notation occurs in the expected 505 position, but the address number itself is blank. Overall: **moderate, strengthened evidence** that 505 was vacant during at least part of the period.
- **1916:** 505 disappears from the expected account sequence and the 1916 directory independently lists no business there. Overall: **medium-high confidence** that 505 was vacant or at minimum had no active separately listed business/water account.

Neither period establishes the exact reason, exact start/end date, or physical condition of the storefront.

## Implication for 1918 research

Do not assume Wolf & Miller necessarily displaced a named predecessor when they appeared at 505 by October 1918. A credible alternative hypothesis is that they occupied a storefront that had been vacant or commercially inactive for some time. Search 1917–1918 for **lease, rent, store room, vacant store, remodeled, fitted up, opening, new store, moved into, secured quarters, and business transfer** language in addition to named predecessor searches.
'''
write("evidence/source-captures/1914-1917-505-vacancy-assessment.md", assessment)

# Current 1915 overview.
replace_once(
    "evidence/source-captures/1915-main-street-research.md",
    "| Water ledger | Online review/reconciliation still pending |",
    "| Water ledger | **Relevant 1914–1915 Book 3 target/Fifth-Main audit complete**; exact-date and faint-handwriting bridge questions preserved |",
)

ledger_section = f'''## Municipal water ledger — relevant 1914–1915 Book 3 audit complete

The official high-resolution **1914–1915 Water Rent Record Book 3** was revisited specifically to finish the target/Fifth-Main questions left open by the earlier screenshot review. Reviewed source extracts are preserved under `records/municipal/water-rent/1914-1915-book-3-review-pages/`; the detailed audit is [here](1914-1915-water-rent-record-book-3-visual-review.md) (`{SID}` / `{EID}`).

The target Main Street sequence is directly visible as **511 → 509 → 507 → [unnumbered] → 503 → 503½ → 501**. The blank-number row between 507 and 503 carries a standalone **V** in the tenant field. The same tenant-field V appears independently at **523 Main** and **521 Main**, making **V = vacancy/vacant a high-confidence ledger interpretation**. The blank row itself still does not print 505, so assigning it to **505 Main remains a moderate-confidence hypothesis**, not an exact-address fact.

The same ledger supplies useful 1914–15-period classifications: **503 Main = Store**, **503½ Main = Barber Shop**, and **501 Main** carries layered **Restaurant/Saloon** classification writing. These are multi-year municipal account/use descriptions; they do not establish a specific 1915 trade name or occupant. The faint 503/503½ tenant names remain unresolved.

Two exact Fifth Street anchors are newly incorporated:

- **110 Fifth, Block 3 — Stable.** The layered tenant handwriting appears consistent with **Scripture & May**, but not clearly enough for a final transcription. This is a probable lead only. It does not backdate the independently verified 108 Fifth address from 1916, and **110 Fifth is not equated with Fashion Stable** without another source.
- **107 Fifth, Block 4 — Blacksmith.** The use is visually clear; the tenant is not confidently readable and is not assigned by trade alone.

Because Book 3 spans 1914–1915, these rows are period anchors rather than exact-month 1915 occupancy statements. The relevant ledger source-class audit is now complete for the 1915 closeout; the remaining ledger questions are interpretation/corroboration questions, not unreviewed target pages.

'''
insert_once(
    "evidence/source-captures/1915-main-street-research.md",
    "## Main Street paving and streetscape chronology\n",
    ledger_section,
    "## Municipal water ledger — relevant 1914–1915 Book 3 audit complete",
)

replace_once(
    "evidence/source-captures/1915-main-street-research.md",
    "| 501 Main | Exact 1915 numbered occupant/use unresolved | Earlier 1912–1913 numbered liquor-premises evidence exists, but the 1915 Fifth/Main undertaking evidence is not automatically 501 |",
    "| 501 Main | Exact 1915 numbered occupant remains unresolved; Book 3 carries layered Restaurant/Saloon classification | Ledger is a 1914–15 period record, not a single dated 1915 occupant; Fifth/Main undertaking evidence is still not automatically 501 |",
)
replace_once(
    "evidence/source-captures/1915-main-street-research.md",
    "| 503 Main | Exact 1915 occupant/use unresolved | L. Hylton is directly documented at 503 in 1914; 1915 continuity is not proven. Cox's June 1915 hall is positively located elsewhere, between Seventh and Eighth |",
    "| 503 Main | Book 3 directly records 503 as a **Store**; exact 1915 tenant still unresolved | L. Hylton is directly documented at 503 in 1914, but the faint ledger tenant is not confidently transcribed and 1915 continuity is not assumed. Cox's June hall is elsewhere |",
)
replace_once(
    "evidence/source-captures/1915-main-street-research.md",
    "| 505 Main | Exact 1915 occupant/use unresolved | Post-1913 Chicago Store/fire succession remains unresolved |",
    "| 505 Main | Exact 1915 occupant/use unresolved; blank-position Book 3 row with vacancy mark is a strengthened hypothesis | V very likely means vacant, but the row between 507 and 503 is **unnumbered**; do not convert it into proven 505 vacancy |",
)
replace_once(
    "evidence/source-captures/1915-main-street-research.md",
    "| Fifth between Main and Water | W. S. Eddy / Fashion Stable | Direct relative-location evidence; no street number printed |\n| 102/104/106/108/110 Fifth | No exact 1915 numbered listing established in the visual work completed so far | Coverage only; never treat as vacancy/non-use evidence |",
    f"| Fifth between Main and Water | W. S. Eddy / Fashion Stable | Direct newspaper relative-location evidence; no street number printed and no automatic equation to 110 Fifth |\n| 107 Fifth | Book 3: **Blacksmith**, Block 4 | Very high for the 1914–15 ledger-period address/use; tenant unresolved |\n| 110 Fifth | Book 3: **Stable**, Block 3 | Very high for the 1914–15 ledger-period address/use; tenant appears consistent with Scripture & May but remains a probable reading only |\n| 102/104/106/108 Fifth | No exact 1915 numbered listing established by the work completed so far | 108 is independently verified later (1916); do not backdate it or treat current silence as vacancy |",
)
replace_once(
    "evidence/source-captures/1915-main-street-research.md",
    "- a new exact 1915 **102/104/106/108/110 Fifth** occupant;",
    "- an exact 1915 **102/104/106/108 Fifth** occupant; 110 Fifth is now a 1914–15 ledger-period Stable anchor but its layered tenant/date remains unresolved;",
)
replace_once(
    "evidence/source-captures/1915-main-street-research.md",
    "1. **Finish the Enterprise visual review:** pages **226–428**; 203 images remain.\n2. **Finish the 1915 water-ledger review and reconciliation.** Integrate useful address, tenant, account/status and Fifth Street clues without treating silence as vacancy.\n3. **Finish the other applicable online source classes** required by `RESEARCH-STANDARD.md`, including directories, municipal/public-works records, property/deed/tax sources, maps, historic-resource records, photographs and official databases where useful and available.\n4. **Reconcile outstanding OCR/search leads** against visually inspected originals and ensure all conflicts/retrieval gaps are preserved accurately.\n5. **Make reasonable online recovery attempts for Courier M01–M04.** Any issue that remains inaccessible or physically ambiguous after online attempts must be precisely copied into the numbered manual-work callout list.\n6. **Run the final 1915 integration/consistency audit:** source register, evidence register, address/business/building/person files, timeline, YAML sidecars and year-status register must agree.\n7. **Write the formal 1915 closeout record** and only then determine whether the year qualifies as `ONLINE COMPLETE`.",
    "1. **Finish the Enterprise visual review:** pages **226–428**; 203 images remain.\n2. **Finish the other applicable online source classes** required by `RESEARCH-STANDARD.md`, including directories, municipal/public-works records beyond the completed water-ledger target audit, property/deed/tax sources, maps, historic-resource records, photographs and official databases where useful and available.\n3. **Reconcile outstanding OCR/search leads** against visually inspected originals and ensure all conflicts/retrieval gaps are preserved accurately.\n4. **Make reasonable online recovery attempts for Courier M01–M04.** Any issue that remains inaccessible or physically ambiguous after online attempts must be precisely copied into the numbered manual-work callout list.\n5. **Run the final 1915 integration/consistency audit:** source register, evidence register, address/business/building/person files, timeline, YAML sidecars and year-status register must agree.\n6. **Write the formal 1915 closeout record** and only then determine whether the year qualifies as `ONLINE COMPLETE`.",
)
replace_once(
    "evidence/source-captures/1915-main-street-research.md",
    "- Continue watching for exact numbered Fifth Street anchors, especially **102, 104, 106, 108 and 110 Fifth**, and relative descriptions such as “between Main and Water” and “between Main and Railroad.”",
    "- Continue watching for exact numbered Fifth Street anchors, especially **102, 104, 106 and 108 Fifth**. **110 Fifth is now established as a Stable in Book 3**, but its tenant/date and relationship to Fashion Stable remain unresolved. Continue tracking relative descriptions such as “between Main and Water” and “between Main and Railroad.”",
)
replace_once(
    "evidence/source-captures/1915-main-street-research.md",
    "The strongest direct 1915 numbered evidence remains the later-year neighboring ladder at **507 / 509 / 511**, with additional anchors at 519 and 527. The Fifth/Main undertaking evidence provides an important south-end block anchor but does not yet map to a numbered 501/503/505 storefront. The June Enterprise Cox article is a significant correction because it positively removes Cox's raid-period pool hall from the 503 hypothesis.\n\nThe target addresses **503 and 505 remain unresolved for 1915** as of Enterprise page 225. That statement describes the current evidence state only. It is not evidence that either premises was vacant, unused, demolished or absent.",
    "The strongest direct dated 1915 newspaper evidence remains the later-year neighboring ladder at **507 / 509 / 511**, with additional anchors at 519 and 527. Book 3 now adds municipal period evidence: **503 = Store**, **503½ = Barber Shop**, a likely-vacancy unnumbered row in the expected 505 position, **107 Fifth = Blacksmith**, and **110 Fifth = Stable**. Those ledger rows span 1914–15 and cannot by themselves fix an exact 1915 occupant or month. The Fifth/Main undertaking evidence still does not map automatically to a numbered 501/503/505 storefront, and the June Enterprise Cox article positively removes Cox's raid-period pool hall from the 503 hypothesis.\n\nThe exact 1915 tenants of **503 and 505 remain unresolved** as of Enterprise page 225. The 505 vacancy hypothesis is stronger because `V` is now corroborated as a repeated ledger vacancy notation, but the target row remains unnumbered. These statements describe the evidence state only; they are not proof of a specific vacancy interval, demolition, or non-use.",
)

# Current checklist checkpoint. Historical earlier checkpoints remain as historical text.
replace_once(
    "evidence/source-captures/1915-page-review-checklist.md",
    "Status: **IN PROGRESS - Courier visual pass complete; Enterprise paused at 225/428 images; other-source work pending**",
    "Status: **IN PROGRESS - Courier visual pass complete; Enterprise paused at 225/428 images; water-ledger target audit complete; other-source work pending**",
)
check_section = f'''## Water-ledger source-class checkpoint — 28 August 2026

- Official **1914–1915 Water Rent Record Book 3** target/Fifth-Main pages were re-reviewed from the full-resolution City scan; reviewed page extracts are preserved under `records/municipal/water-rent/1914-1915-book-3-review-pages/`. Source `{SID}`, evidence `{EID}`; [detailed audit](1914-1915-water-rent-record-book-3-visual-review.md).
- The target sequence is visually confirmed as **511 → 509 → 507 → [unnumbered/V] → 503 → 503½ → 501**. The same standalone tenant-field **V** appears independently at 523 and 521 Main, strongly supporting **V = vacant/vacancy notation**. The blank target row still does not print 505; exact 505 vacancy remains an inference, not a direct address fact.
- Book 3 directly adds **503 = Store**, **503½ = Barber Shop**, layered **501 Restaurant/Saloon** classification, **107 Fifth = Blacksmith**, and **110 Fifth = Stable**. The layered 110 tenant appears consistent with Scripture & May but is not clear enough for a final transcription; 110 is not equated with Fashion Stable.
- Because Book 3 spans 1914–15, these are ledger-period anchors rather than exact-month 1915 occupant statements. The relevant water-ledger target review is complete; other online source classes and Enterprise pages 226–428 remain.

'''
insert_once(
    "evidence/source-captures/1915-page-review-checklist.md",
    "## Latest Enterprise pause checkpoint - chronological page 225 / 16 July 1915 p1\n",
    check_section,
    "## Water-ledger source-class checkpoint — 28 August 2026",
)
replace_once(
    "evidence/source-captures/1915-page-review-checklist.md",
    "- Courier remains 123/123; M01-M04, water-ledger/other-source review and year closeout remain open. **1915 is not ONLINE COMPLETE.**",
    "- Courier remains 123/123; M01-M04, other online-source review and year closeout remain open. The relevant water-ledger target audit is complete. **1915 is not ONLINE COMPLETE.**",
)

# Canonical year-status row.
year_path = "registers/year-status.md"
year = read(year_path)
old_year = "| 1915 | **IN PROGRESS** | `evidence/source-captures/1915-courier-sheets-073-100.md`; `evidence/source-captures/1915-courier-sheets-101-110.md`; `evidence/source-captures/1915-courier-sheets-111-123.md`; `evidence/source-captures/1915-enterprise-pages-001-120.md`; `evidence/source-captures/1915-enterprise-pages-121-160.md`; `evidence/source-captures/1915-enterprise-pages-161-200.md`; `evidence/source-captures/1915-enterprise-pages-201-225.md`; `evidence/source-captures/1915-page-review-checklist.md` | Courier **123/123** through year end. Enterprise **225/428 images**, visually reviewed through **16 Jul p1**; next 16 Jul p2, **203 images remain**. Water-ledger/other-source work pending; Courier M01-M04 remain open. |"
new_year = "| 1915 | **IN PROGRESS** | `evidence/source-captures/1915-courier-sheets-073-100.md`; `evidence/source-captures/1915-courier-sheets-101-110.md`; `evidence/source-captures/1915-courier-sheets-111-123.md`; `evidence/source-captures/1915-enterprise-pages-001-120.md`; `evidence/source-captures/1915-enterprise-pages-121-160.md`; `evidence/source-captures/1915-enterprise-pages-161-200.md`; `evidence/source-captures/1915-enterprise-pages-201-225.md`; `evidence/source-captures/1915-page-review-checklist.md`; `evidence/source-captures/1914-1915-water-rent-record-book-3-visual-review.md` | Courier **123/123** through year end. Enterprise **225/428 images**, visually reviewed through **16 Jul p1**; next 16 Jul p2, **203 images remain**. **Relevant Book 3 water-ledger target/Fifth-Main audit complete**; other online source classes pending; Courier M01-M04 remain open. |"
if new_year not in year:
    if old_year not in year:
        raise RuntimeError("1915 year-status row changed unexpectedly")
    write(year_path, year.replace(old_year, new_year, 1))

# Address register: add the new numbered Fifth anchors and update current reconstruction note.
addr_path = "registers/address-register.md"
addr = read(addr_path)
row108 = "| 108 Fifth Street, Oregon City, Oregon (historic commercial address) | Unassigned | `evidence/source-captures/scripture-may-108-fifth-predecessor-lead.md` | Scripture & May; later S. F. Scripture | `E-109` is 1915 name-only corroboration; exact 108 Fifth evidence is visually verified in the linked 1916/1922 source capture | Scripture & May is visually verified at **108 Fifth St.** on 5 October 1916; S. F. Scripture is visually verified at **108 Fifth St., between Main and Water**, on 8 June 1922. The recurring Oct.–Nov. 1915 Scripture & May ads do **not** print an address, so 108 must not be backdated to 1915. Historic odd/even geometry and relationship to 109 Fifth remain unresolved. |"
new_rows = f"| 107 Fifth Street, Oregon City, Oregon (1914–1915 ledger-period commercial address) | Unassigned | `evidence/source-captures/1914-1915-water-rent-record-book-3-visual-review.md` | Tenant unresolved | `{EID}` | Book 3 printed ledger p5 directly records **107 Fifth, Block 4, Blacksmith**. Tenant handwriting is not confidently readable. Do not assign a named blacksmith from trade/location alone. |\n{row108}\n| 110 Fifth Street, Oregon City, Oregon (1914–1915 ledger-period commercial address) | Unassigned | `evidence/source-captures/1914-1915-water-rent-record-book-3-visual-review.md` | Probable Scripture & May tenant reading only; relationship to Fashion Stable unresolved | `{EID}` | Book 3 printed ledger p3 directly records **110 Fifth, Block 3, Stable**. Layered tenant writing appears consistent with Scripture & May but is not clear enough for a final transcription. Do not backdate 108 Fifth or equate 110 with Fashion Stable without an independent bridge. |"
if "| 110 Fifth Street, Oregon City" not in addr:
    if row108 not in addr:
        raise RuntimeError("108 Fifth row changed unexpectedly")
    addr = addr.replace(row108, new_rows, 1)
old_para = "**Fifth Street remains in scope.** Holman/Randall's Fifth/Main wording, unnumbered Scripture & May advertisements, numbered 108 Fifth and 513 Fifth records, and the separately documented 109 Fifth record must remain distinct. The completed December Courier batch establishes no new numbered Fifth occupant and no exact 102/104/106/108/110 Fifth listing. The November 25 Fifth Street crushed-rock/day-labor report concerns road work only; exact segment and authority remain RL-043."
new_para = f"**Fifth Street remains in scope.** Holman/Randall's Fifth/Main wording, unnumbered 1915 Scripture & May advertisements, later numbered 108 Fifth, 513 Fifth and separately documented 109 Fifth records must remain distinct. The completed December Courier batch itself established no new numbered Fifth occupant; the subsequent Book 3 municipal audit (`{SID}` / `{EID}`) now supplies period anchors **107 Fifth = Blacksmith** and **110 Fifth = Stable**. The layered 110 tenant is only a probable Scripture & May reading and is not a bridge to later 108 Fifth or to Fashion Stable. The November 25 Fifth Street crushed-rock/day-labor report concerns road work only; exact segment and authority remain RL-043."
if new_para not in addr:
    if old_para not in addr:
        raise RuntimeError("Fifth Street current paragraph changed unexpectedly")
    addr = addr.replace(old_para, new_para, 1)
old_goal = "During every remaining year-by-year visual review, actively watch for **numbered Fifth Street addresses—especially the even-numbered 100-series sequence 102, 104, 106, 108 and 110—and location wording such as “between Main and Water,” “between Main and Railroad,” or equivalent intersection/adjacency descriptions**. Preserve each exact number as its own address anchor and use it to reconstruct the historic odd/even geometry and the 1922 fire-area business cluster. Do not infer adjacency, shared walls, or a 503/505 relationship from consecutive numbering alone."
new_goal = "During every remaining year-by-year visual review, actively watch for **numbered Fifth Street addresses—especially unresolved 102, 104, 106 and 108 during 1915—and location wording such as “between Main and Water,” “between Main and Railroad,” or equivalent intersection/adjacency descriptions**. Book 3 now establishes 107 Fifth/Blacksmith and 110 Fifth/Stable as 1914–15 ledger-period anchors; later 108 Fifth evidence remains separately dated. Preserve each exact number as its own anchor and use it to reconstruct historic odd/even geometry and the 1922 fire-area cluster. Do not infer adjacency, shared walls, business identity, or a 503/505 relationship from consecutive numbering or matching trade type alone."
if new_goal not in addr:
    if old_goal not in addr:
        raise RuntimeError("Fifth Street goal paragraph changed unexpectedly")
    addr = addr.replace(old_goal, new_goal, 1)
write(addr_path, addr)

# Scripture & May predecessor lead: add the newly discovered but deliberately qualified 110 Fifth clue.
scripture_section = f'''## 1914–1915 Book 3 — probable 110 Fifth predecessor clue

The official Oregon City **1914–1915 Water Rent Record Book 3** target/Fifth-Main audit (`{SID}` / `{EID}`) directly records **110 Fifth, Block 3, classification Stable**. The tenant field is layered/crossed; visually it appears consistent with **Scripture & May**, but not clearly enough for a final transcription.

This is therefore a **probable predecessor-location lead only**. It does not establish a precise date within the 1914–15 book span and does not prove a move from 110 to the independently verified **108 Fifth** address in October 1916. It also does not prove that 110 Fifth was the newspaper's unnumbered **Fashion Stable**. Those bridges require independent evidence.

The same municipal audit separately records **107 Fifth, Block 4, Blacksmith**, with tenant handwriting unresolved. Trade similarity alone is not an identity bridge.

'''
insert_once(
    "evidence/source-captures/scripture-may-108-fifth-predecessor-lead.md",
    "## 5 October 1916 — 108 Fifth visually verified\n",
    scripture_section,
    "## 1914–1915 Book 3 — probable 110 Fifth predecessor clue",
)

# Source and evidence registers.
source_register = read("evidence/source-register.md")
source_entry = f'''\n\n## {SID} — Oregon City Water Rent Record Book 3, 1914–1915
Canonical URL: https://www.orcity.org/DocumentCenter/View/6213/1914-1915-Water-Rent-Record-Book-3  
Type: Primary official municipal water-rent ledger; relevant target/Fifth-Main pages **visually verified from full-resolution scans**.  
Repository reviewed extracts: `records/municipal/water-rent/1914-1915-book-3-review-pages/` (official PDF pages 1–12 plus source/page hashes and provenance).  
Related evidence: `{EID}`.  
Repository source capture: `evidence/source-captures/1914-1915-water-rent-record-book-3-visual-review.md`.  
Notes: The full City source is 139 scanned PDF pages; this project audit preserves/reviews the relevant downtown extracts, not an exhaustive transcription of all 139 pages. Target printed p5 shows 511→509→507→blank/V→503→503½→501; comparison p4 supplies independent V tenant marks at 523 and 521, strongly supporting V as vacancy notation. Printed p3 supplies 110 Fifth/Stable; p5 supplies 107 Fifth/Blacksmith. The blank target row remains unnumbered and is not promoted to exact 505.
'''
if f"## {SID} — Oregon City Water Rent Record Book 3" not in source_register:
    write("evidence/source-register.md", source_register.rstrip() + source_entry + "\n")

evidence_register = read("evidence/evidence-register.md")
evidence_entry = f'''\n\n## {EID} — 1914–1915 Water Rent Book 3 target/Fifth-Main audit
Type: Primary municipal ledger visual review and notation comparison.  
Source: `{SID}`.  
Record: `evidence/source-captures/1914-1915-water-rent-record-book-3-visual-review.md`.  
Claims: Official high-resolution scans directly verify the Block 4 sequence **511, 509, 507, unnumbered/V, 503, 503½, 501 Main**; 503 is classified Store and 503½ Barber Shop, while 501 carries layered Restaurant/Saloon writing. Independent tenant-field V marks at **523 Main** and **521 Main** strongly support `V` as the ledger's vacancy notation, but the target blank row never prints 505, so exact 505 vacancy remains a moderate hypothesis. Book 3 also directly records **110 Fifth / Block 3 / Stable** and **107 Fifth / Block 4 / Blacksmith**. The layered 110 tenant appears consistent with Scripture & May but remains a probable reading only; it does not backdate later 108 Fifth or identify Fashion Stable.  
Confidence: **Very High** for visually readable numbers, classifications, sequence and repeated V marks; **High-confidence interpretation** for V=vacant; **Moderate hypothesis** for blank row=505; **Probable only** for Scripture & May at 110. Exact month within the 1914–15 ledger span and faint target tenants remain unresolved.  
Related: `B-001`, `B-002`, `B-005`; `evidence/source-captures/1914-1917-505-vacancy-assessment.md`; `evidence/source-captures/scripture-may-108-fifth-predecessor-lead.md`.
'''
if f"## {EID} — 1914–1915 Water Rent Book 3" not in evidence_register:
    write("evidence/evidence-register.md", evidence_register.rstrip() + evidence_entry + "\n")

# Machine-readable source/evidence sidecars.
sources_yml = read("database/sources.yml")
if f"  - id: {SID}\n" not in sources_yml:
    sources_yml = sources_yml.rstrip() + f'''\n\n  - id: {SID}
    name: Oregon City Water Rent Record Book 3, 1914–1915
    url: https://www.orcity.org/DocumentCenter/View/6213/1914-1915-Water-Rent-Record-Book-3
    notes: Primary official municipal water-rent ledger. Relevant target/Fifth-Main pages visually verified from full-resolution City scans; official PDF pages 1–12 preserved under records/municipal/water-rent/1914-1915-book-3-review-pages/. Related evidence {EID}. Full source has 139 scanned pages; no all-volume transcription claim.
'''
    write("database/sources.yml", sources_yml + "\n")

evidence_yml = read("database/evidence.yml")
if f"  - id: {EID}\n" not in evidence_yml:
    evidence_yml = evidence_yml.rstrip() + f'''\n\n  - id: {EID}
    name: 1914–1915 Water Rent Book 3 target/Fifth-Main audit
    type: Primary municipal ledger visual review and notation comparison
    claims:
      - Official scans verify 511, 509, 507, an unnumbered V row, 503, 503½ and 501 Main in sequence; 503 is Store, 503½ Barber Shop, and 501 has layered Restaurant/Saloon classification writing.
      - Independent tenant-field V marks at 523 and 521 Main strongly support V as vacancy notation, but the target row never prints 505; exact 505 vacancy remains a hypothesis.
      - Book 3 directly records 110 Fifth, Block 3, Stable and 107 Fifth, Block 4, Blacksmith.
      - Layered tenant writing at 110 appears consistent with Scripture & May but is not clear enough for a final transcription; later 108 Fifth and Fashion Stable identities are not backdated or merged.
    confidence: Very High for visible sequence/numbers/classifications and repeated V; high-confidence interpretation for V=vacant; moderate for blank row=505; probable only for Scripture & May at 110.
    related_sources: [{SID}]
    related_buildings: [B-001, B-002, B-005]
    repository_file: evidence/source-captures/1914-1915-water-rent-record-book-3-visual-review.md
'''
    write("database/evidence.yml", evidence_yml + "\n")

# Research log audit trail.
log_path = "registers/research-log.md"
log = read(log_path)
log_marker = "## 2026-08-28 — 1914–1915 Water Rent Book 3 target/Fifth-Main audit"
if log_marker not in log:
    log += f'''\n\n{log_marker}

- Retrieved the official 139-page City Book 3 scan and visually rechecked the relevant downtown target/Fifth-Main pages from full-resolution extracts; reviewed official PDF pages 1–12 are preserved under `records/municipal/water-rent/1914-1915-book-3-review-pages/`.
- `{SID}` / `{EID}`: confirmed **511→509→507→blank/V→503→503½→501** and found comparison V marks at 523 and 521 Main, strongly supporting V as vacancy notation while leaving blank-row=505 unresolved.
- Added exact 1914–15 ledger-period anchors **107 Fifth = Blacksmith** and **110 Fifth = Stable**. The 110 tenant appears consistent with Scripture & May but remains a layered/probable reading; no 108 backdating or Fashion Stable merger.
- 503 is classified Store, 503½ Barber Shop, and 501 has layered Restaurant/Saloon writing; faint tenant names and exact timing remain unresolved.
- The relevant 1915 water-ledger target audit is complete. 1915 remains **IN PROGRESS** because Enterprise pages 226–428, other online source classes, M01–M04 handling and final closeout remain.
'''
    write(log_path, log)

# README for preserved administrative source extracts (PDF files are copied by the workflow).
readme = f'''# Oregon City Water Rent Record Book 3 — reviewed extracts

Source: City of Oregon City, **1914–1915 Water Rent Record Book 3**  
Canonical URL: https://www.orcity.org/DocumentCenter/View/6213/1914-1915-Water-Rent-Record-Book-3  
Source ID: `{SID}`  
Evidence ID: `{EID}`

The official source contains 139 scanned PDF pages. The files in this folder are source-quality extracts of **official PDF pages 1–12**, preserved because those pages contain the relevant downtown Main/Fifth sequences inspected for the 1915 target audit. `source-sha256.txt` records the checksum of the complete downloaded City PDF; `page-pdfs-sha256.txt` records the extracted-page hashes. `pdfinfo.txt` records the downloaded source metadata.

The preservation of pages 1–12 does **not** assert that all 139 pages were exhaustively transcribed. The research conclusions and confidence limits are documented in:

`evidence/source-captures/1914-1915-water-rent-record-book-3-visual-review.md`

Important limits: the blank/V row between 507 and 503 is not numbered 505 in the source; 110 Fifth's layered tenant is not treated as a definitive Scripture & May transcription; 110 Fifth is not automatically equated with Fashion Stable.
'''
write("records/municipal/water-rent/1914-1915-book-3-review-pages/README.md", readme)

print(f"Integrated Book 3 as {SID} / {EID}")
