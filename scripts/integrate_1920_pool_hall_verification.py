from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


def write(rel, text):
    (ROOT / rel).write_text(text, encoding="utf-8")


def append_once(rel, marker, block):
    text = read(rel)
    if marker in text:
        return
    write(rel, text.rstrip() + "\n\n" + block.strip() + "\n")


def replace_once(rel, old, new):
    text = read(rel)
    if new in text:
        return
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"Expected exactly one anchor in {rel!r}, found {count}: {old[:100]!r}")
    write(rel, text.replace(old, new, 1))


SOURCE_CAPTURE = "evidence/source-captures/1920-fifth-sixth-main-pool-hall-visual-verification-2026-08-31.md"

# 1. Source and evidence registries.
append_once(
    "evidence/source-register.md",
    "## S-150 — Oregon City Enterprise 1920 Fifth–Sixth Main pool-hall source set",
    r'''## S-150 — Oregon City Enterprise 1920 Fifth–Sixth Main pool-hall source set
Type: Primary newspaper scans; **VISUALLY VERIFIED TARGETED SOURCE SET** 31 August 2026.
Canonical PDFs:
- https://oregonnews.uoregon.edu/lccn/sn00063700/1920-02-13/ed-1/seq-5.pdf
- https://oregonnews.uoregon.edu/lccn/sn00063700/1920-06-04/ed-1/seq-3.pdf
- https://oregonnews.uoregon.edu/lccn/sn00063700/1920-12-03/ed-1/seq-1.pdf
Repository PDFs:
- `newspapers/oregon-city-enterprise/1920-02-13-page-5.pdf`
- `newspapers/oregon-city-enterprise/1920-06-04-page-3.pdf`
- `newspapers/oregon-city-enterprise/1920-12-03-page-1.pdf`
Evidence: `E-135`.
Repository source capture: `evidence/source-captures/1920-fifth-sixth-main-pool-hall-visual-verification-2026-08-31.md`.
Notes: February identifies Clem Dollar as proprietor of a pool hall on Main between Fifth and Sixth; June reports the City Council granted **A. Leland** permission to operate a pool hall at **505½ Main** and erect an electric street sign; December again mentions a pool hall in the Fifth–Sixth Main block. The pages do not prove that the three references are the same hall, do not establish succession, and do not date construction of the surviving 505 building. Do not merge A. Leland with O. H. Leland without independent evidence.'''
)

append_once(
    "database/sources.yml",
    "  - id: S-150\n",
    r'''  - id: S-150
    name: Oregon City Enterprise 1920 Fifth–Sixth Main pool-hall source set
    url: https://oregonnews.uoregon.edu/lccn/sn00063700/1920-06-04/ed-1/seq-3.pdf
    notes: Primary newspaper scans visually verified 31 August 2026. February identifies Clem Dollar as proprietor of a pool hall on Main between Fifth and Sixth; June reports the City Council granted A. Leland permission to operate a pool hall at 505½ Main and erect an electric street sign; December again mentions a pool hall in the block. Same-hall succession and construction date are not proved. Related evidence E-135; full provenance and limits in evidence/source-register.md and the 1920 visual-verification capture.'''
)

append_once(
    "evidence/evidence-register.md",
    "## E-135 — 1920 pool-hall anchors at Fifth–Sixth Main and 505½ Main",
    r'''## E-135 — 1920 pool-hall anchors at Fifth–Sixth Main and 505½ Main
Type: Primary newspaper business/location and reported municipal-action evidence; **direct visual inspection**.
Source: `S-150`.
Related building: `B-002`.
Repository source capture: `evidence/source-captures/1920-fifth-sixth-main-pool-hall-visual-verification-2026-08-31.md`.
Claims:
- *Oregon City Enterprise*, 13 February 1920, identifies **Clem Dollar** as proprietor of a pool hall on Main between Fifth and Sixth streets.
- *Oregon City Enterprise*, 4 June 1920, reports that the City Council granted **A. Leland** permission to operate a pool hall at **505½ Main Street** and to erect an electric street sign.
- *Oregon City Enterprise*, 3 December 1920, refers to a pool hall between Fifth and Sixth streets on Main.
- The June item is an exact 505½ business/use anchor between Wolf & Miller at 505 in October 1918 (`E-027`) and Dr. Freeze at 505/505½ in 1921–1922 (`E-028`). It does **not** establish new construction in 1920.
- No source in this set proves that Clem Dollar's hall, A. Leland's 505½ premises, and the December pool hall were the same business or room; no succession is inferred.
- A. Leland is not merged with O. H. Leland (`E-126`) without an independent identity bridge.
Confidence: **Very High** for the visually verified printed names, address, block locations, and reported council action; **unresolved** for operator identity links, succession, property ownership, physical room relationship, and building construction date.'''
)

append_once(
    "database/evidence.yml",
    "  - id: E-135\n",
    r'''  - id: E-135
    name: 1920 pool-hall anchors at Fifth–Sixth Main and 505½ Main
    type: Primary newspaper business/location and reported municipal-action evidence; direct visual inspection
    claims:
      - Oregon City Enterprise, 13 February 1920, identifies Clem Dollar as proprietor of a pool hall on Main between Fifth and Sixth streets.
      - Oregon City Enterprise, 4 June 1920, reports that the City Council granted A. Leland permission to operate a pool hall at 505½ Main Street and to erect an electric street sign.
      - Oregon City Enterprise, 3 December 1920, refers to a pool hall between Fifth and Sixth streets on Main.
      - The June item is an exact 505½ business/use anchor between Wolf & Miller at 505 in October 1918 and Dr. Freeze at 505/505½ in 1921–1922; it does not establish new construction in 1920.
      - No source in this set proves that the February, June, and December pool-hall references are the same business or room, and A. Leland is not merged with O. H. Leland without an independent bridge.
    confidence: Very High for visually verified printed names, address, block locations, and reported council action; unresolved for operator identity links, succession, property ownership, physical room relationship, and building construction date.
    related_sources: [S-150]
    related_buildings: [B-002]
    repository_file: evidence/source-captures/1920-fifth-sixth-main-pool-hall-visual-verification-2026-08-31.md'''
)

# 2. Promote the checkpoint from OCR leads to visual-verification status.
checkpoint = r'''# 1919-1920 construction search checkpoint: 501, 503, and 505 Main

Status: **resumed; three preserved 1920 pages visually verified; construction question IN PROGRESS**  
Checkpoint date: 2026-08-31

## Question

Were the narrow storefronts shown at 501, 503, and 505 Main on the 1911 Sanborn map demolished, enlarged, or reconstructed during 1919-1920? The city inventory's approximate construction dates make this period a priority, but those dates are not themselves proof of a construction event.

## Map correction and visually established facts

- The downtown 501-505 Main block is on **1911 Sanborn Sheet 16**, preserved as `maps/sanborn/originals/1911-16 (5th-Main).pdf`.
- The previously preserved 1911 Sheet 22 is a Canemah sheet and is not the target-block map. It remains useful as an authentic geographic-control sheet and should not be deleted.
- Visual comparison of 1911 Sheet 16 with 1925 Sheet 6 shows a changed storefront/footprint arrangement at 501-505 Main. The maps support physical change by 1925, but do not date each demolition or replacement.
- Fifth Street is labeled **60 feet wide on both the 1911 and 1925 target sheets**. The maps do not support a 60-to-50-foot narrowing of Fifth Street. What changed is the storefront/lot configuration.

## Bounded OCR discovery pass

Downloaded and searched OCR for all available issues/pages in this bounded corpus:

- *Oregon City Enterprise*: all available 1919 and 1920 issues.
- *Oregon City Courier*: January-July 1919, through the end of that title's available run.
- Total inventoried: **132 issues / 1,004 page records**.

This was an OCR discovery pass, not a page-by-page visual annual review. It does not complete or certify either year. Both years remain **IN PROGRESS** under `RESEARCH-STANDARD.md`.

## Visual verification completed

The three preserved Enterprise pages have now been directly inspected. Full transcription/context and limits are in `evidence/source-captures/1920-fifth-sixth-main-pool-hall-visual-verification-2026-08-31.md` (`S-150` / `E-135`).

1. **13 February 1920, page 5** (`1920-02-13-page-5.pdf`)
   - Visually verified: **Clem Dollar** is identified as proprietor of a pool hall on Main between Fifth and Sixth streets.
   - This is block-level occupancy evidence only; no numbered address or construction event is printed.

2. **4 June 1920, page 3** (`1920-06-04-page-3.pdf`)
   - Visually verified council report: **“The application of A. Leland to operate a pool hall at 505½ Main street and to erect an electric street sign was granted.”**
   - This establishes an exact **505½ Main** business/use anchor by the council meeting reported 4 June 1920.
   - It does **not** prove that the premises or surviving 505 building was newly constructed in 1920.
   - Do not merge A. Leland with O. H. Leland without independent identity evidence.

3. **3 December 1920, page 1** (`1920-12-03-page-1.pdf`)
   - Visually verified: an article refers to **the pool hall between Fifth and Sixth streets on Main**.
   - This is block-level context only; no operator or numbered address is printed.

## Municipal-record retrieval status

The City of Oregon City historical meeting archive indicates that Commission records exist for the 1920s. The underlying **Wednesday, 2 June 1920** council/Commission record corresponding to the Enterprise report has not yet been recovered in the present web/tool environment. This is a **retrieval gap/manual follow-up**, not negative evidence.

## Current interpretation

- The bounded OCR pass plus targeted follow-up has not produced a 1919-1920 newspaper notice explicitly saying that 503 or 505 was demolished, rebuilt, enlarged, or replaced. This is search status only, **not evidence that no such work occurred**.
- The June 1920 page now directly establishes a usable/business premises at **505½ Main**. It narrows the occupancy chronology between Wolf & Miller at 505 in October 1918 (`E-027`) and Dr. Freeze at 505/505½ in 1921–1922 (`E-028`).
- The February Clem Dollar hall and December block-located hall are also visually verified, but no evidence yet proves that either was the same hall as A. Leland's 505½ premises or that one operator succeeded another.
- No direct 1919-1920 exact-number occupant for **503 Main** has yet been established in this pass.
- The 1911→1925 footprint change remains real, but the exact demolition/rebuild date for the surviving 503 and 505 structures remains unresolved.

## Resume point

1. Recover and inspect the **2 June 1920** Oregon City Commission minutes, including any permit, sign, room, owner, or building-work wording attached to A. Leland's application.
2. Search late 1918 through June 1920 for Wolf & Miller exit/sale, Clem Dollar, A. Leland, lease/license/sign, construction, demolition, remodeling, and relocation language tied to 505/505½ or the Fifth–Sixth Main block.
3. Identify **A. Leland** independently before considering any relationship to **O. H. Leland**, Timms Pool Hall, or Leland & Little.
4. Continue primary permit/assessor/deed/improvement-record work for the c.1919/c.1920 construction estimates; do not substitute modern listing dates for construction proof.
5. Continue annual visual-review work separately. This targeted source set does not advance 1919 or 1920 to ONLINE COMPLETE.

## File integrity

- `1911-16 (5th-Main).pdf`: `ffd9349d0c88fff7ce31f70cba115163296ae6b4dd19b6e7e6fb044cc1e319dd`
- `1920-02-13-page-5.pdf`: `dfd5be8e1fad8ad1c7dca8516590bb67d1a3d7c3f41cc5e4c1a1cb69a04eb004`
- `1920-06-04-page-3.pdf`: `3b419bb26e96d77aaf5be8dcb7f0954c7755ab9be890788fad119ca79702c245`
- `1920-12-03-page-1.pdf`: `1110d255815ccefe6e68614f9582f82fd1d4752b7f17ebcaea2bb7ec8fc44721`
'''
write("evidence/source-captures/1919-1920-501-503-505-construction-checkpoint.md", checkpoint)

# 3. 505 building and timeline.
replace_once(
    "buildings/505-main.md",
    "`E-127`, `E-133`, `E-134`",
    "`E-127`, `E-133`, `E-134`, `E-135`"
)
replace_once(
    "buildings/505-main.md",
    "`S-138`, `S-142`, `S-148`, `S-149`",
    "`S-138`, `S-142`, `S-148`, `S-149`, `S-150`"
)
replace_once(
    "buildings/505-main.md",
    "Later documented occupants include The Chicago Store (1911-1913) and Wolf & Miller (1918), so a 1918 vacancy/rebuild story is not supported for the **address**. The construction date of the **surviving building** still has conflicting historic-resource estimates; see `Construction-date conflict` below.",
    "Later documented occupants include The Chicago Store (1911-1913) and Wolf & Miller (1918), so a 1918 vacancy/rebuild story is not supported for the **address**. A visually verified 4 June 1920 council report then says **A. Leland** was granted permission to operate a pool hall at **505½ Main Street** and erect an electric street sign (`E-135` / `S-150`). This is an exact business/use anchor, not proof of new construction or of physical continuity with the surviving 505 building. The construction date of the **surviving building** still has conflicting historic-resource estimates; see `Construction-date conflict` below."
)
replace_once(
    "buildings/505-main.md",
    "- **1918:** Wolf & Miller directly occupies 505 Main, proving address use before either construction-date estimate.\n- **1925:** Sanborn visually shows a distinct 505 billiards/cigars occupancy.",
    "- **1918:** Wolf & Miller directly occupies 505 Main, proving address use before either construction-date estimate.\n- **June 1920:** A. Leland is granted permission to operate a pool hall at **505½ Main** and erect an electric street sign (`E-135` / `S-150`). This narrows exact-address use around the c.1920 inventory estimate but does **not** prove construction.\n- **1925:** Sanborn visually shows a distinct 505 billiards/cigars occupancy."
)
replace_once(
    "buildings/505-main.md",
    "The best next test is assessor cards **1938–1942**, Oregon City Building Division archives for **1939–1941 permits**, steward-verified aerial rear-edge transcription for **`IMG-0007` / `IMG-0008` / `IMG-0009`**, and physical building analysis. See `RL-005`.",
    "The best next tests are (1) the underlying **2 June 1920 Oregon City Commission minutes** and late-1918–1920 permit/lease/property records for the c.1920 front/core question, and (2) assessor cards **1938–1942**, Oregon City Building Division archives for **1939–1941 permits**, steward-verified aerial rear-edge transcription for **`IMG-0007` / `IMG-0008` / `IMG-0009`**, and physical building analysis for the 1940/rear-work question. See `RL-005` and `RL-024`."
)

# Keep database/building relationship mirror synchronized without otherwise reformatting YAML.
replace_once(
    "database/buildings.yml",
    "      - E-133\n      - E-134\n    related_sources:",
    "      - E-133\n      - E-134\n      - E-135\n    related_sources:"
)
replace_once(
    "database/buildings.yml",
    "      - S-148\n      - S-149\n    related_maps:",
    "      - S-148\n      - S-149\n      - S-150\n    related_maps:"
)

# Insert exact 1920 chronology row and sequence wording.
timeline_anchor = "| 10, 24 Oct. 1918 | **Wolf & Miller at 505 Main**, shoe/repair trade. | **Exact, visually verified**; Wolf identity and Miller discrepancy open. | `BUS-012`; `E-027`, `E-124`; `S-034`, `S-138` |"
timeline_row = timeline_anchor + "\n| 2/4 Jun. 1920 | City Council reportedly granted **A. Leland** permission to operate a pool hall at **505½ Main** and erect an electric street sign. | **Exact, visually verified primary report**; council action was reported 4 June for the Wednesday meeting. Business use is proved; new construction, property ownership, and Clem Dollar/O. H. Leland identity or succession are not. | `E-135`; `S-150` |"
replace_once("timelines/505-main.md", timeline_anchor, timeline_row)
replace_once(
    "timelines/505-main.md",
    "Chicago Store → Wolf & Miller → Freeze → unnamed billiards/cigars",
    "Chicago Store → Wolf & Miller → A. Leland pool-hall permit at 505½ → Freeze → unnamed billiards/cigars"
)

# 4. Open questions, research leads, and crosswalk.
needle = "No **1939–1941** permit recovered. Assessor cards, address-level aerial transcription, or physical analysis are still needed."
replace_once(
    "evidence/open-questions.md",
    needle,
    needle + "\n\n**31 August 2026 update:** `E-135` / `S-150` now visually establishes **A. Leland's 505½ Main pool-hall permit/use anchor by June 1920**. This strengthens exact-address occupancy around the c.1920 inventory estimate but does **not** prove that the surviving building was erected in 1920. The underlying 2 June 1920 Commission minutes remain a retrieval/manual follow-up."
)

rl1920 = "**1920 update:** `E-135` / `S-150` visually verifies Clem Dollar's block-located pool hall in February, A. Leland's exact **505½ Main** pool-hall/sign approval in June, and a block-located pool hall in December. These are occupancy/use anchors, **not construction evidence**. Do not merge the three hall references, A. Leland with O. H. Leland, or infer that the surviving 505 structure was new. Highest-value next source is the underlying **2 June 1920 Commission record**, followed by late-1918–1920 permit, lease, assessor, deed/improvement, and relocation records."
rl_anchor = "**1912 update:** `E-090` / `S-105` proves that buildings were actively being torn down and replaced **somewhere on Main Street** in May 1912. The source does not identify the Fifth–Sixth block or any numbered target premises. Continue treating 1912 as a confirmed Main Street structural-change year while keeping the exact buildings unresolved under `RL-038`."
replace_once("evidence/research-leads.md", rl_anchor, rl_anchor + "\n\n" + rl1920)

replace_once(
    "indexes/id-crosswalk.md",
    "`S-149`/`E-134`/`IMG-0725` visibly establishes Young at 505 in 1910. Includes distinct Farr",
    "`S-149`/`E-134`/`IMG-0725` visibly establishes Young at 505 in 1910. `S-150`/`E-135` adds a visually verified June 1920 exact-use anchor at 505½ Main; it is not construction proof. Includes distinct Farr"
)

# 5. Research log.
append_once(
    "registers/research-log.md",
    "### 2026-08-31 — 1920 Fifth–Sixth Main pool-hall pages visually verified",
    r'''### 2026-08-31 — 1920 Fifth–Sixth Main pool-hall pages visually verified
- Resumed the 1919–1920 501/503/505 construction checkpoint after commit `ef2a431`.
- Directly inspected the preserved Enterprise pages for 13 Feb., 4 Jun., and 3 Dec. 1920.
- Verified Clem Dollar as proprietor of a pool hall on Main between Fifth and Sixth in February; verified the 4 June report that City Council granted A. Leland permission to operate a pool hall at **505½ Main** and erect an electric street sign; verified a December block-located pool-hall reference.
- Registered the source set as `S-150` and evidence as `E-135`; integrated the exact 505½ anchor into `B-002`, the 505 unified timeline, open questions, research leads, crosswalk, and YAML mirrors.
- No same-hall/operator succession is inferred; A. Leland is not merged with O. H. Leland. No construction date is inferred from business occupancy.
- Underlying **2 June 1920** Commission minutes remain a retrieval/manual follow-up. 1919 and 1920 remain **IN PROGRESS**; the bounded OCR pass and these targeted visual pages do not certify either year.
- Detailed capture: `evidence/source-captures/1920-fifth-sixth-main-pool-hall-visual-verification-2026-08-31.md`.'''
)

# Remove the one-time integration machinery so the final commit contains only durable archive content.
for rel in [
    "scripts/integrate_1920_pool_hall_verification.py",
    ".github/workflows/integrate-1920-pool-hall-verification.yml",
]:
    p = ROOT / rel
    if p.exists():
        p.unlink()

print("1920 pool-hall verification integration prepared")
