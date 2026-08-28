#!/usr/bin/env python3
import json, re
from pathlib import Path

ROOT = Path('.')
SAMPLE_DIR = ROOT/'newspapers/oregon-city-courier/1917-first-issue-monthly-sample'
MANIFEST = SAMPLE_DIR/'manifest.json'
CAPTURE = ROOT/'evidence/source-captures/1917-courier-first-issue-monthly-sample.md'

def read(path): return path.read_text()
def write(path, text): path.write_text(text)
def max_id(text, prefix, width):
    vals=[int(x) for x in re.findall(rf'\b{re.escape(prefix)}-(\d{{{width}}})\b', text)]
    return max(vals) if vals else 0

def append_once(path, marker, block):
    text=read(path)
    if marker not in text:
        if not text.endswith('\n'): text+='\n'
        text += '\n' + block.strip() + '\n'
        write(path,text)

def add_yaml_related(text, bus_id, field, value):
    pat=rf'(?ms)(^  - id: {re.escape(bus_id)}\n.*?)(?=^  - id: BUS-|\Z)'
    m=re.search(pat,text)
    if not m: raise SystemExit(f'Missing {bus_id} in businesses.yml')
    block=m.group(1)
    if value in block:
        return text
    fpat=rf'(?ms)^    {re.escape(field)}:\n((?:      - .*\n|    - .*\n)+)'
    fm=re.search(fpat,block)
    if fm:
        indent = '      ' if '      - ' in fm.group(1) else '    '
        repl=f'    {field}:\n'+fm.group(1)+f'{indent}- {value}\n'
        block=block[:fm.start()]+repl+block[fm.end():]
    else:
        block += f'    {field}:\n    - {value}\n'
    return text[:m.start(1)]+block+text[m.end(1):]

source_md=ROOT/'evidence/source-register.md'
evidence_md=ROOT/'evidence/evidence-register.md'
media_md=ROOT/'media/photo-metadata-register.md'
source_yml=ROOT/'database/sources.yml'
evidence_yml=ROOT/'database/evidence.yml'

S_num=max_id(read(source_md),'S',3)+1
E_num=max_id(read(evidence_md),'E',3)+1
IMG_num=max_id(read(media_md),'IMG',4)+1
S=f'S-{S_num:03d}'; E=f'E-{E_num:03d}'

manifest=json.loads(MANIFEST.read_text())
items=manifest['items']
assert len(items)==96, len(items)
start_img=IMG_num
for i,item in enumerate(items):
    item['review_status']='VISUALLY VERIFIED'
    item['media_id']=f'IMG-{start_img+i:04d}'
manifest['visual_review']={
    'date':'2026-08-28',
    'status':'96/96 sampled page images visually inspected',
    'method':'Actual page scans rendered to contact sheets for systematic inspection; candidate findings re-opened at high resolution. OCR/text used only for discovery.',
    'scope_limit':'First available Courier issue of each calendar month only; not exhaustive annual newspaper coverage.'
}
MANIFEST.write_text(json.dumps(manifest,indent=2)+'\n')
IMG_first=f'IMG-{start_img:04d}'; IMG_last=f'IMG-{start_img+95:04d}'

issues=[
('1917-01-04',8,'p2 R. L. Holman ad prints Fifth and Main; p2 Electric Store ad prints Andresen Bldg., 619 Main; p4 Scripture & May prints 108 Fifth.'),
('1917-02-01',8,'p5 Scripture & May prints 108 Fifth; p5 reports Dr. G. F. Anderson preparing to move his lower-Main rooming-house building back two inches and remodel it, with barber-shop improvements noted.'),
('1917-03-01',10,'p1 reports T. L. Charman preparing to move a large residence from Ninth/Main to Tenth/Water so Miller-Parker can erect a modern garage/business block; this is Ninth/Main context, not the target frontage. Holman Fifth/Main advertising recurs.'),
('1917-04-05',8,'Holman Fifth/Main advertising recurs; Scripture & May appears without a new exact-number finding in this sampled issue.'),
('1917-05-03',8,'Holman Fifth/Main advertising recurs; Scripture & May appears without a new exact-number finding in this sampled issue.'),
('1917-06-07',8,'Holman Fifth/Main advertising recurs. No exact 501/503/505 or new target-numbered Fifth occupant established.'),
('1917-07-05',8,'Holman/Fifth-Main continuity is present in the sampled issue; Scripture & May also appears. No exact target Main number established.'),
('1917-08-02',6,'p2 reports Owen Thomas accepted a position in Scripture & May\'s blacksmith shop in Oregon City; no street number printed in that item.'),
('1917-09-06',8,'Scripture & May appears; sampled issue supplies no new exact 501/503/505 or numbered Fifth target.'),
('1917-10-04',8,'p2 directly gives Theroux Music House, 519 Main Street, extending the F. F. Theroux address anchor into 1917.'),
('1917-11-01',8,'p3 Jones Drug Co. advertisement directly prints 617 Main Street, supplying an exact number for BUS-040 after its 1916 prospective move into former PRL&P/Schilling quarters.'),
('1917-12-06',8,'p3 Adams Department Store closing-out advertisement says part of the building is to be torn down soon; the ad does not give a numbered address, so no target-building demolition is inferred.'),
]
rows='\n'.join(f'| {d} | {n} | **VISUALLY VERIFIED {n}/{n}** | {note} |' for d,n,note in issues)

capture=f'''# 1917 Oregon City Courier — first-issue-of-each-month visual sample

Status: **SAMPLING PASS COMPLETE — 12/12 selected issues, 96/96 page images visually reviewed; 1917 remains IN PROGRESS**

Source: `{S}`  
Evidence: `{E}`  
Media: `{IMG_first}`–`{IMG_last}`  
Preserved originals: `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/`

## Scope and method

At the project steward's request, this pass reviewed the **first available Oregon City Courier issue in every calendar month of 1917**. It is a structured sampling pass, not an annual-completion claim. All 96 selected page PDFs were preserved with source URLs and SHA-256 hashes. Every actual scanned page image was visually inspected; OCR/text extraction was used only to discover candidate material, and material promoted below was checked against the scans, with high-resolution enlargement where needed.

Sampling rule: first available Courier issue in each month. Selected dates: **4 Jan, 1 Feb, 1 Mar, 5 Apr, 3 May, 7 Jun, 5 Jul, 2 Aug, 6 Sep, 4 Oct, 1 Nov, 6 Dec 1917**.

## Issue log

| Issue | Pages | Visual status | Main/Fifth findings and limits |
| --- | ---: | --- | --- |
{rows}

## Verified findings

### Scripture & May — 108 Fifth continues into early 1917

The **4 January p4** and **1 February p5** scans both visibly advertise **SCRIPTURE & MAY — 108 Fifth St.** This extends the independently verified 108 Fifth chronology from the selected September–December 1916 ads into January and February 1917. It does **not** prove that the probable layered Scripture & May reading at 110 Fifth in the 1914–15 water ledger is the same premises or establish a move date from 110 to 108.

The **2 August p2** scan separately reports that **Owen Thomas had accepted a position in Scripture & May's blacksmith shop in Oregon City**. That item proves continuing operation of the business name in August but prints no street number.

### R. L. Holman — Fifth and Main continuity

Multiple sampled pages from January through July repeat R. L. Holman's undertaking advertisement at **Fifth and Main**. This corroborates the already established 1917 intersection continuity. The wording still does not identify **501, 503, or 505 Main**, and no numbered storefront is assigned from the intersection description.

### Electric Store — 619 Main on 4 January 1917

The **4 January p2** scan directly prints the Portland Railway Light & Power Co. **Electric Store — Andresen Bldg., 619 Main St.** This is strong dated corroboration of the July 1916 report that the Electric Store/power offices moved one door north from the Beaver Building/617 to Andresen 619. It does not prove a deed, lease date, or the occupancy of every Andresen Building room.

### Jones Drug Co. — 617 Main by 1 November 1917

The **1 November p3** scan contains a large **Jones Drug Co.** advertisement whose footer directly prints **617 Main Street — Oregon City**. This supplies the numbered destination missing from the June 1916 prospective-rearrangement story: Jones Drug had been reported preparing to move into the PRL&P/Schilling room, and by this sampled 1917 ad it is directly at 617. This does not by itself establish the exact move day or a direct legal succession/lease from the Electric Store.

### F. F. Theroux — 519 Main continuity

The **4 October p2** scan says: **Theroux Music House, 519 Main street, Oregon City**. This extends the previously documented 1915–1916 519 Main anchor into October 1917 without assuming uninterrupted occupancy between sampled dates.

### Main Street / downtown building-change context

Two sampled items are useful but do not map to 501/503/505:

- **1 February p5:** Dr. G. F. Anderson was preparing, at council request, to move his rooming-house building on **lower Main street** back two inches; the item says the barber shop had recently been re-equipped and the building would be remodeled when moved.
- **1 March p1:** T. L. Charman was preparing to move a large residence from the **corner of Ninth and Main** to **Tenth and Water** to clear the site for a Miller-Parker modern garage/business block. The article says the new building would occupy about 80 by 128 feet. This is positive Ninth/Main construction evidence, not target-frontage evidence.
- **6 December p3:** Adams Department Store's closing-out ad says **“PART OF BUILDING TO BE TORN DOWN SOON”**. The sampled ad does not print an address, so it is retained only as an unnumbered downtown demolition/business-closure lead and is not assigned to the target block.

## Exact target-address result

Across the **96 visually reviewed sample pages**, this pass did **not** establish a defensible exact 1917 occupant at **501, 503, 505, 507, 509, or 511 Main**. This is a bounded result for twelve sampled issues only. It is **not** evidence of vacancy, non-use, demolition, closure, or absence at any address.

The sample also does not replace the full 1917 title/issue/page inventory or exhaustive page-by-page review required for `ONLINE COMPLETE`.

## Relationship to existing 1917 gaps

The following remain open and are not resolved by this sample:

1. The complete 1917 Courier annual visual audit outside these twelve selected issues.
2. The complete relevant-title annual review beyond already verified pages.
3. The true **13 December 1917 Courier page 21** retrieval gap.
4. The **Sohns & Woodbeck 1916–1917 directory, Oregon City section** manual/restricted-access gap.
5. Exact 1917 occupants of 501/503/505 and the historical reasons for the 505 water-ledger/directory gap.

## Handling rule

Absence of an exact target address in the twelve sampled issues is coverage only. No vacancy, non-use, demolition, closure, relocation, or building-survival conclusion is drawn from silence.
'''
CAPTURE.write_text(capture)

append_once(source_md, f'## {S} —', f'''## {S} — Oregon City Courier 1917 first-issue monthly visual sample
Type: Primary newspaper scans / structured monthly sampling pass.  
Dates: 4 Jan, 1 Feb, 1 Mar, 5 Apr, 3 May, 7 Jun, 5 Jul, 2 Aug, 6 Sep, 4 Oct, 1 Nov, 6 Dec 1917; **12 complete selected issues / 96 page images**.  
Repository: `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/`; exact source URLs, SHA-256 hashes, media IDs and visual statuses in `manifest.json`.  
Media: `{IMG_first}` through `{IMG_last}`.  
Evidence: `{E}`; detailed log `evidence/source-captures/1917-courier-first-issue-monthly-sample.md`.  
Notes: All 96 sampled scans visually inspected. Jan4/Feb1 directly verify Scripture & May at 108 Fifth; Jan4 directly verifies Electric Store at Andresen 619 Main; Oct4 verifies Theroux Music House 519 Main; Nov1 directly verifies Jones Drug Co. 617 Main. No exact 501/503/505/507/509/511 occupant established in the sample; coverage only. This sampling pass is not annual completion.''')

append_once(evidence_md, f'## {E} —', f'''## {E} — 1917 Courier first-issue monthly visual sample
Type: Primary newspaper visual review; source `{S}`.  
Record: `evidence/source-captures/1917-courier-first-issue-monthly-sample.md`.  
Claims:
- All **96 page images** from twelve first-monthly Courier issues were visually inspected; this is a sampling pass, not exhaustive annual coverage.
- Jan4 p4 and Feb1 p5 directly print **Scripture & May, 108 Fifth St.**; Aug2 p2 reports Owen Thomas taking a position in Scripture & May's Oregon City blacksmith shop without a number.
- Sampled Holman advertising corroborates **Fifth and Main** continuity but does not establish 501/503/505.
- Jan4 p2 directly prints the Electric Store at **Andresen Bldg., 619 Main St.**, corroborating its reported 1916 move from 617.
- Oct4 p2 directly prints **Theroux Music House, 519 Main street**.
- Nov1 p3 directly prints **Jones Drug Co., 617 Main Street**, supplying a numbered 1917 location after the 1916 prospective move/rearrangement report.
- Feb1 lower-Main building movement/remodeling, Mar1 Ninth/Main Miller-Parker redevelopment, and Dec6 Adams Department Store building-removal wording are contextual; none is assigned to 501/503/505.
- No exact 501/503/505/507/509/511 occupant established in the twelve sampled issues; this is bounded coverage only, never vacancy/non-use evidence.
Confidence: Very High for the visually readable exact-address and business-location wording; exact transaction/move days, target occupancy and unnumbered building locations remain unresolved.''')

sy=read(source_yml)
if f'  - id: {S}\n' not in sy:
    sy += f'''\n\n  - id: {S}\n    name: Oregon City Courier 1917 first-issue monthly visual sample\n    url: https://oregonnews.uoregon.edu/lccn/sn00063698/1917-01-04/ed-1/\n    notes: 12 selected first-monthly issues / 96 scans visually verified and preserved under newspapers/oregon-city-courier/1917-first-issue-monthly-sample/. Related evidence {E}; media {IMG_first}-{IMG_last}. Sampling pass only, not annual completion.\n'''
    write(source_yml,sy)

ey=read(evidence_yml)
if f'  - id: {E}\n' not in ey:
    ey += f'''\n\n  - id: {E}\n    name: 1917 Courier first-issue monthly visual sample\n    type: Primary newspaper visual review of 96 sampled page images\n    claims:\n      - Twelve complete first-monthly Courier issues, 96 scans total, were visually inspected; sampling only, not annual completion.\n      - January 4 and February 1 directly place Scripture & May at 108 Fifth; August 2 confirms the business operating without printing a number.\n      - January 4 prints the Electric Store at Andresen Building 619 Main; October 4 prints Theroux Music House at 519 Main; November 1 prints Jones Drug Co. at 617 Main.\n      - Holman Fifth/Main continuity is corroborated without assigning 501/503/505.\n      - No exact 501/503/505/507/509/511 occupant was established in these twelve sampled issues; coverage only, not vacancy evidence.\n    confidence: Very High for visually readable printed wording; exact move/transaction dates and target occupancy unresolved.\n    related_sources: [{S}]\n    related_businesses: [BUS-029, BUS-031, BUS-035, BUS-039, BUS-040]\n    repository_file: evidence/source-captures/1917-courier-first-issue-monthly-sample.md\n'''
    write(evidence_yml,ey)

media_rows=[]
for item in items:
    media_rows.append(f"| {item['media_id']} | `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/{item['file']}` | {item['date']} / seq{item['sequence']} / visually verified |")
append_once(media_md, f'## 1917 Courier first-issue monthly sample — {S} / {E}', f'''## 1917 Courier first-issue monthly sample — {S} / {E}

All 96 unchanged original page PDFs are **VISUALLY VERIFIED**. Exact source URLs and SHA-256 hashes are preserved in `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/manifest.json`. This is a sampling pass only.

| Media ID | Repository file | Issue / sequence / status |
| --- | --- | --- |
'''+ '\n'.join(media_rows))

append_once(ROOT/'evidence/source-captures/1917-courier-review-start.md', '## First-issue monthly sampling checkpoint — 28 August 2026', f'''## First-issue monthly sampling checkpoint — 28 August 2026

A new structured first-issue-of-each-month pass (`{S}` / `{E}`) visually reviewed **12 complete selected issues / 96 pages**: Jan4, Feb1, Mar1, Apr5, May3, Jun7, Jul5, Aug2, Sep6, Oct4, Nov1 and Dec6. [Detailed log and preserved-page links](1917-courier-first-issue-monthly-sample.md).

Verified additions include Scripture & May at **108 Fifth** on Jan4/Feb1, Electric Store at **619 Main** on Jan4, Theroux Music House at **519 Main** on Oct4, and Jones Drug Co. at **617 Main** on Nov1. The sample establishes no exact 501/503/505/507/509/511 occupant. Sampling silence is not vacancy evidence. 1917 remains **IN PROGRESS**; the 13 Dec true-p21 and Sohns & Woodbeck Oregon City directory gaps remain open, and this sample does not substitute for exhaustive annual page review.''')

append_once(ROOT/'evidence/source-captures/scripture-may-108-fifth-predecessor-lead.md', '## January–August 1917 sampled continuity', f'''## January–August 1917 sampled continuity

`{E}` / `{S}`, [monthly sample log](1917-courier-first-issue-monthly-sample.md), visually verifies **Scripture & May — 108 Fifth St.** on **4 January 1917 p4** and **1 February 1917 p5**. This extends the selected 108 Fifth exact-address chronology from September–December 1916 into early 1917. It still does not prove that the probable 110 Fifth ledger reading represents the same business/premises or establish a move date from 110 to 108.

The **2 August 1917 p2** sample separately reports that **Owen Thomas had accepted a position in Scripture & May's blacksmith shop in Oregon City**. That item verifies continuing operation of the business name in August but gives no number. The 19 April partner-name item retains its own OCR/TEXT ONLY status until directly visually checked.''')

append_once(ROOT/'businesses/electric-store.md', '## 1917 numbered continuation', f'''## 1917 numbered continuation

`{E}` / `{S}` visually verifies a **4 January 1917 p2** Electric Store advertisement printing **Andresen Bldg., 619 Main St.** This is dated corroboration of the July 1916 report that the Electric Store/power offices moved one door north from 617 to Andresen 619. The sampled ad does not establish the legal lease/deed terms or exact move day.''')

bi=ROOT/'businesses/business-index.md'
text=read(bi)
text=re.sub(r'^\| BUS-029 \|.*$', f'| BUS-029 | F. F. Theroux pianos and sewing machines | 519 Main | Exact 1915 address (`E-107`, `P-044`); **4 Oct 1917 p2** directly repeats Theroux Music House at 519 Main (`{E}`/`{S}`). No uninterrupted-occupancy or target-storefront inference. |', text, flags=re.M)
text=re.sub(r'^\| BUS-031 \|.*$', f'| BUS-031 | [Portland Railway Light & Power Co. Electric Store](electric-store.md) | 617 Main (earlier); **619 Main by 1916–17** | 1915 Beaver/617 evidence; July 1916 move to Andresen 619; **4 Jan 1917 p2** directly repeats Andresen Bldg., 619 Main (`{E}`/`{S}`). Exact lease/move day unresolved. |', text, flags=re.M)
text=re.sub(r'^\| BUS-039 \|.*$', f'| BUS-039 | Scripture & May | 108 Fifth | Exact address verified Sep–Dec 1916 and again **4 Jan / 1 Feb 1917**; Aug2 reports an employee joining the Oregon City blacksmith shop without a number. Ledger 110 and May & Washburn bridges unresolved. `{E}`/`{S}`. |', text, flags=re.M)
text=re.sub(r'^\| BUS-040 \|.*$', f'| BUS-040 | Jones Drug Company | **617 Main by 1 Nov 1917**; Andresen Building move prospect in 1916 | June 1916 announced move into former PRL&P/Schilling room; Nov1 1917 p3 directly prints Jones Drug Co., 617 Main Street. Exact move day and legal succession terms unresolved. `{E}`/`{S}`. |', text, flags=re.M)
write(bi,text)

byp=ROOT/'database/businesses.yml'; byt=read(byp)
for bus in ['BUS-029','BUS-031','BUS-039','BUS-040']:
    byt=add_yaml_related(byt,bus,'related_evidence',E)
    byt=add_yaml_related(byt,bus,'related_sources',S)
byt=re.sub(r'(?ms)(  - id: BUS-039\n    name: Scripture & May\n    address: ).*?(\n    notes: ).*?(\n    related_people:|\n    related_evidence:)',
           rf'\g<1>108 Fifth\g<2>Exact address verified in selected September-December 1916 ads and again January 4 and February 1, 1917; August 2 reports an employee joining the blacksmith shop without a number. Ledger 110 tenant reading and May & Washburn bridge unresolved.\g<3>', byt)
byt=re.sub(r'(?ms)(  - id: BUS-040\n    name: Jones Drug Company\n    address: ).*?(\n    notes: ).*?(\n    related_people:|\n    related_evidence:)',
           rf'\g<1>617 Main by 1 November 1917; Andresen Building move prospect in 1916\g<2>June 1916 prospective move into former PRL&P/Schilling room; November 1, 1917 p3 directly prints Jones Drug Co., 617 Main Street. Exact move day and legal succession/lease terms unresolved.\g<3>', byt)
write(byp,byt)

ar=ROOT/'registers/address-register.md'; art=read(ar)
art=re.sub(r'^\| 108 Fifth Street,.*$', f'| 108 Fifth Street, Oregon City, Oregon (historic commercial address) | Unassigned | `evidence/source-captures/scripture-may-108-fifth-predecessor-lead.md` | `BUS-039` Scripture & May; later S. F. Scripture | `E-109`, `E-119`, `{E}`; later 1922 exact evidence in linked capture | Scripture & May is visually verified at **108 Fifth St.** in selected Sep–Dec 1916 ads and again **4 Jan / 1 Feb 1917**; Aug2 1917 confirms the blacksmith shop operating without printing a number. S. F. Scripture is visually verified at 108 Fifth between Main/Water on 8 Jun 1922. Do not backdate to the probable 110 Fifth ledger row or infer adjacency from numbering. |', art, flags=re.M)
art=re.sub(r'^\| 519 Main Street,.*$', f'| 519 Main Street, Oregon City, Oregon (historic listing) | Unassigned; historic building not identified | `evidence/source-captures/1915-sheets-073-100-integration-audit.md` | `BUS-029` | `E-107`, `{E}` | F. F. Theroux at 519 is documented in dated 1915 listings; **4 Oct 1917 p2** directly prints **Theroux Music House, 519 Main street**. Do not infer uninterrupted occupancy or a target-storefront identity. |', art, flags=re.M)
art=re.sub(r'^\| 617 Main Street,.*$', f'| 617 Main Street, Oregon City, Oregon (historic listing) | Unassigned | `businesses/electric-store.md` | `BUS-031` Electric Store (earlier); `BUS-040` Jones Drug Co. (1917) | `E-109`, `E-119`, `{E}` | Electric Store was at Beaver Building/617 in 1915 and moved to Andresen **619 Main** in 1916. **1 Nov 1917 p3** directly prints Jones Drug Co. at **617 Main Street**. This establishes dated occupants, not legal succession/lease terms. |', art, flags=re.M)
if '| 619 Main Street, Oregon City, Oregon (historic listing) |' not in art:
    anchor=f'| 617 Main Street, Oregon City, Oregon (historic listing) | Unassigned | `businesses/electric-store.md` | `BUS-031` Electric Store (earlier); `BUS-040` Jones Drug Co. (1917) | `E-109`, `E-119`, `{E}` | Electric Store was at Beaver Building/617 in 1915 and moved to Andresen **619 Main** in 1916. **1 Nov 1917 p3** directly prints Jones Drug Co. at **617 Main Street**. This establishes dated occupants, not legal succession/lease terms. |\n'
    new=f'| 619 Main Street, Oregon City, Oregon (historic listing) | Unassigned | `businesses/electric-store.md` | `BUS-031` | `E-119`, `{E}` | July 1916 report says Electric Store/power offices moved one door north to Andresen Building **619 Main**; selected ads repeat 619, and **4 Jan 1917 p2** directly prints Andresen Bldg., 619 Main St. No deed/lease or all-tenant numbering inference. |\n'
    art=art.replace(anchor,anchor+new)
if '## 1917 first-monthly Courier sample' not in art:
    art += f'''\n## 1917 first-monthly Courier sample\n\n**{E}/{S}** adds exact sampled anchors at **108 Fifth (Scripture & May, Jan4/Feb1)**, **519 Main (Theroux Music House, Oct4)**, **617 Main (Jones Drug Co., Nov1)** and **619 Main (Electric Store, Jan4)**. The 96 sampled pages establish no exact 501/503/505/507/509/511 occupant; that is bounded sample coverage only, not vacancy evidence.\n'''
write(ar,art)

ys=ROOT/'registers/year-status.md'; yst=read(ys)
new1917=f'| 1917 | **IN PROGRESS** | `evidence/source-captures/1917-closeout.md`; `evidence/source-captures/1917-courier-review-start.md`; `evidence/source-captures/1917-courier-first-issue-monthly-sample.md` | Structured first-issue monthly sample now **12/12 selected issues / 96 pages visually verified**, with exact 108 Fifth, 519, 617 and 619 Main anchors. Sampling is not exhaustive annual coverage. True 13 Dec p21 and Sohns & Woodbeck Oregon City directory remain gaps; full relevant-title/page audit still unfinished. |'
yst=re.sub(r'^\| 1917 \|.*$',new1917,yst,flags=re.M)
write(ys,yst)

append_once(ROOT/'registers/research-log.md','### 2026-08-28 — 1917 Courier first-issue monthly sample', f'''### 2026-08-28 — 1917 Courier first-issue monthly sample
- Preserved and visually inspected **96/96 pages** across the first available Courier issue in each month (12 issues).
- `{S}` / `{E}`; originals/manifests at `newspapers/oregon-city-courier/1917-first-issue-monthly-sample/`; detailed log `evidence/source-captures/1917-courier-first-issue-monthly-sample.md`.
- Verified Scripture & May 108 Fifth on Jan4/Feb1; Electric Store 619 Main Jan4; Theroux Music House 519 Main Oct4; Jones Drug Co. 617 Main Nov1; contextual lower-Main/Ninth-Main/Adams building-change items retained with location limits.
- No exact 501/503/505/507/509/511 occupant in the sample. Coverage only, no vacancy inference. 1917 remains IN PROGRESS.''')

print(json.dumps({'source':S,'evidence':E,'media_first':IMG_first,'media_last':IMG_last},indent=2))
