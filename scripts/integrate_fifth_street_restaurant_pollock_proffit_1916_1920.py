#!/usr/bin/env python3
from pathlib import Path
import hashlib
import re
import urllib.request

ROOT = Path('.')

NEW_ITEMS = [
    {
        'source_id': 'S-184',
        'evidence_id': 'E-164',
        'date': '1 September 1916',
        'url': 'https://oregonnews.uoregon.edu/lccn/sn00063700/1916-09-01/ed-1/seq-5.pdf',
        'repo_path': 'newspapers/oregon-city-enterprise/1916-09-01-page-5-fifth-street-restaurant-pollock-inspection.pdf',
        'uploaded_name': 'Fifth Street Resturant (Exists) Oregon City enterprise., September 01, 1916, Image 5.pdf',
        'sha256': '530d674b3d7f1d2207a4952064118898d9caa7f126a4dea88aadfb383217bfb0',
        'size': 578627,
    },
    {
        'source_id': 'S-185',
        'evidence_id': 'E-165',
        'date': '19 November 1920',
        'url': 'https://oregonnews.uoregon.edu/lccn/sn00063700/1920-11-19/ed-1/seq-5.pdf',
        'repo_path': 'newspapers/oregon-city-enterprise/1920-11-19-page-5-fifth-street-restaurant-guy-proffit-interest.pdf',
        'uploaded_name': 'Fifth Street Resturant (Interest) Oregon City enterprise., November 19, 1920, Page Page 5, Image 5.pdf',
        'sha256': 'eb2077d3e859b5c52e188884135304110a42ec97003be6150fd14424e9eadc6f',
        'size': 738828,
    },
]

DUPLICATE_1922 = {
    'repo_path': 'newspapers/oregon-city-enterprise/1922-07-21-page-1-fifth-street-restaurant-fire-ownership.pdf',
    'sha256': 'ed47337b2918af305399cf62ed1b9cd29ddba1d9ec10c1ab02f198516adbe6d1',
    'size': 849840,
    'aliases': [
        'Fifth Street Resturant (Fire-Owners) Oregon City enterprise., July 21, 1922, Image 1.pdf',
        'Fifth Street Resturant & other businesses (Fire) Oregon City enterprise., July 21, 1922, Image 1.pdf',
    ],
}


def read(path):
    return (ROOT / path).read_text(encoding='utf-8')


def write(path, text):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding='utf-8')


def append_once(path, marker, block):
    text = read(path)
    if marker in text:
        return
    if not text.endswith('\n'):
        text += '\n'
    write(path, text + '\n' + block.strip('\n') + '\n')


def replace_once(path, old, new):
    text = read(path)
    if new in text:
        return
    if old not in text:
        raise RuntimeError(f'Expected text not found in {path}: {old[:120]!r}')
    write(path, text.replace(old, new, 1))


def sha256(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()

# Guard immutable IDs. If any of these IDs landed independently, stop rather than collide.
for path, ids in [
    ('evidence/source-register.md', ['S-184', 'S-185']),
    ('evidence/evidence-register.md', ['E-164', 'E-165']),
    ('people/people-index.md', ['P-104']),
    ('database/timeline.yml', ['T-059', 'T-060']),
]:
    text = read(path)
    for ident in ids:
        if ident in text and '1916-1920-pollock-proffit-supplement' not in text:
            raise RuntimeError(f'ID {ident} already in use in {path}; reallocate before integration')

# Confirm both steward July 1922 filenames are byte-identical aliases of the already-preserved S-183 page.
dup_path = ROOT / DUPLICATE_1922['repo_path']
if not dup_path.exists():
    raise RuntimeError('Expected existing S-183 July 21 1922 PDF is missing')
if dup_path.stat().st_size != DUPLICATE_1922['size'] or hashlib.sha256(dup_path.read_bytes()).hexdigest() != DUPLICATE_1922['sha256']:
    raise RuntimeError('Existing S-183 July 21 1922 PDF does not match steward upload hash/size')

# Download canonical Oregon Digital derivatives and require exact byte identity with steward uploads.
existing_hashes = {}
for p in ROOT.rglob('*.pdf'):
    try:
        existing_hashes.setdefault(hashlib.sha256(p.read_bytes()).hexdigest(), str(p))
    except OSError:
        pass

for item in NEW_ITEMS:
    with urllib.request.urlopen(item['url'], timeout=60) as r:
        data = r.read()
    got = hashlib.sha256(data).hexdigest()
    if got != item['sha256'] or len(data) != item['size']:
        raise RuntimeError(f"Canonical PDF differs from steward upload for {item['date']}: {got}/{len(data)}")
    duplicate = existing_hashes.get(got)
    if duplicate:
        item['actual_repo_path'] = duplicate
        item['already_preserved'] = True
    else:
        p = ROOT / item['repo_path']
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(data)
        item['actual_repo_path'] = item['repo_path']
        item['already_preserved'] = False
        existing_hashes[got] = item['repo_path']

capture_path = 'evidence/source-captures/1916-1920-fifth-street-restaurant-pollock-proffit-supplement-2026-09-02.md'
capture = f'''# Fifth Street Restaurant Pollock / Proffit supplement, 1916–1920

Review date: **2 September 2026**.

Status: **FOUR PROJECT-STEWARD UPLOADS ACCOUNTED FOR; TWO NEW EXACT PAGE PDFs VISUALLY VERIFIED AND PRESERVED; TWO JULY 1922 UPLOADS DEDUPLICATED TO EXISTING S-183.**

## Duplicate handling — 21 July 1922

The two steward filenames below are byte-for-byte identical to each other and to the already-preserved `S-183` page at `{DUPLICATE_1922['repo_path']}`:

- `{DUPLICATE_1922['aliases'][0]}`
- `{DUPLICATE_1922['aliases'][1]}`

SHA-256: `{DUPLICATE_1922['sha256']}` ({DUPLICATE_1922['size']} bytes). No duplicate source ID or duplicate repository PDF was created.

## S-184 / E-164 — Oregon City Enterprise, 1 September 1916, p. 5

The state dairy-and-food-commissioner report directly lists **“Fifth Street restaurant, W. W. Pollock, 75.3.”** This supplies a named-person bridge that the 31 August 1916 Courier summary (`S-180` / `E-160`) did not print.

Supported:
- W. W. Pollock is directly associated with the Fifth Street Restaurant on 1 September 1916;
- inspection score **75.3**.

Limits:
- no numbered address or real-estate ownership is printed;
- this dated association plus the 1919 “conducting” evidence does not by itself prove uninterrupted operation throughout 1916–1919.

Repository file: `{NEW_ITEMS[0]['actual_repo_path']}`  
Canonical URL: {NEW_ITEMS[0]['url']}  
Original upload: `{NEW_ITEMS[0]['uploaded_name']}`  
SHA-256: `{NEW_ITEMS[0]['sha256']}` ({NEW_ITEMS[0]['size']} bytes).

## S-185 / E-165 — Oregon City Enterprise, 19 November 1920, p. 5

In the marriage notice for **Guy Proffit** and **Leathel Cross**, the paper states that Proffit **“is interested in the Fifth Street Restaurant in this city”** and that he **“will retain his interests here,”** while making daily trips to Portland.

Supported:
- Guy Proffit held an explicitly reported business interest in the Fifth Street Restaurant on this date;
- the article anticipated that he would retain that interest after establishing his Portland home.

Limits:
- “interested in” / “interests” does not establish sole proprietorship, ownership percentage, leasehold, land/building ownership, or uninterrupted continuity from Pollock;
- the exact numbered premises remains unresolved.

Repository file: `{NEW_ITEMS[1]['actual_repo_path']}`  
Canonical URL: {NEW_ITEMS[1]['url']}  
Original upload: `{NEW_ITEMS[1]['uploaded_name']}`  
SHA-256: `{NEW_ITEMS[1]['sha256']}` ({NEW_ITEMS[1]['size']} bytes).

## Bounded chronology effect

The new pages tighten the restaurant chronology to a named Pollock association in September 1916, Pollock conducting the restaurant in October 1919, Guy Proffit holding a reported interest in November 1920, active-place evidence in August 1921, and the conflicting owner/operator reports around the July 1922 fire. They do **not** establish a continuous partnership or ownership chain.
'''
if not (ROOT / capture_path).exists():
    write(capture_path, capture)

append_once('evidence/source-register.md', '## S-184 — Oregon City Enterprise, 1 September 1916', f'''
## S-184 — Oregon City Enterprise, 1 September 1916, p. 5, Fifth Street Restaurant / W. W. Pollock inspection listing
Type: Primary newspaper scan; **VISUALLY VERIFIED**; exact steward-upload PDF bytes preserved.  
Canonical page/PDF: {NEW_ITEMS[0]['url']}  
Repository file: `{NEW_ITEMS[0]['actual_repo_path']}`  
Original uploaded filename: `{NEW_ITEMS[0]['uploaded_name']}`  
Related evidence: `E-164`; business `BUS-070`; person `P-101`.  
Notes: State dairy-and-food-commissioner report directly lists Fifth Street restaurant, W. W. Pollock, 75.3. No numbered address or property ownership. SHA-256 `{NEW_ITEMS[0]['sha256']}`.

## S-185 — Oregon City Enterprise, 19 November 1920, p. 5, Guy Proffit interest in Fifth Street Restaurant
Type: Primary newspaper scan; **VISUALLY VERIFIED**; exact steward-upload PDF bytes preserved.  
Canonical page/PDF: {NEW_ITEMS[1]['url']}  
Repository file: `{NEW_ITEMS[1]['actual_repo_path']}`  
Original uploaded filename: `{NEW_ITEMS[1]['uploaded_name']}`  
Related evidence: `E-165`; business `BUS-070`; person `P-104`.  
Notes: Marriage item says Guy Proffit is interested in Fifth Street Restaurant and will retain his interests there; scope/legal character of the interest and exact premises are not printed. SHA-256 `{NEW_ITEMS[1]['sha256']}`.
''')

append_once('evidence/evidence-register.md', '## E-164 — 1 September 1916 Enterprise names W. W. Pollock at Fifth Street Restaurant', f'''
## E-164 — 1 September 1916 Enterprise names W. W. Pollock at Fifth Street Restaurant
Type: Primary newspaper visual evidence.  
Confidence: Very High for the directly printed Pollock/business/score wording; exact premises, title, and continuity unresolved.  
Source: `S-184` — *Oregon City Enterprise*, 1 September 1916, p. 5.  
Status: **VISUALLY VERIFIED**.  
Claims:
- The inspection report directly lists **Fifth Street restaurant, W. W. Pollock, 75.3**.
- This names Pollock at the restaurant one day after the separate Courier inspection summary (`E-160`) printed the restaurant and same score without a proprietor.
- No numbered address, land/building ownership, or continuous 1916–1919 operating span is proved.
Related business: `BUS-070`; related person: `P-101`.  
Repository capture: `{capture_path}`.

## E-165 — 19 November 1920 Enterprise identifies Guy Proffit interest in Fifth Street Restaurant
Type: Primary newspaper visual evidence.  
Confidence: Very High for the directly printed business-interest wording; legal character/percentage, exact premises, ownership, and continuity unresolved.  
Source: `S-185` — *Oregon City Enterprise*, 19 November 1920, p. 5.  
Status: **VISUALLY VERIFIED**.  
Claims:
- The marriage item directly says **Guy Proffit is interested in the Fifth Street Restaurant** in Oregon City.
- It says he **will retain his interests here** while making daily trips to Portland.
- The wording does not establish sole ownership, percentage interest, lease, or real-estate title.
Related business: `BUS-070`; related person: `P-104`.  
Repository capture: `{capture_path}`.
''')

append_once('database/sources.yml', '  - id: S-184', f'''
  - id: S-184
    name: Oregon City Enterprise, 1 September 1916, p. 5, Fifth Street Restaurant / W. W. Pollock inspection listing
    type: Primary newspaper scan
    date: 1 September 1916
    review_state: VISUALLY VERIFIED
    repository_file: {NEW_ITEMS[0]['actual_repo_path']}
    url: {NEW_ITEMS[0]['url']}
    notes: "Exact steward-upload PDF bytes preserved. Report directly lists Fifth Street restaurant, W. W. Pollock, 75.3; no numbered address or property ownership. E-164/BUS-070/P-101. SHA-256 {NEW_ITEMS[0]['sha256']}."
  - id: S-185
    name: Oregon City Enterprise, 19 November 1920, p. 5, Guy Proffit interest in Fifth Street Restaurant
    type: Primary newspaper scan
    date: 19 November 1920
    review_state: VISUALLY VERIFIED
    repository_file: {NEW_ITEMS[1]['actual_repo_path']}
    url: {NEW_ITEMS[1]['url']}
    notes: "Exact steward-upload PDF bytes preserved. Article says Guy Proffit is interested in Fifth Street Restaurant and will retain his interests; legal character/percentage and exact premises unresolved. E-165/BUS-070/P-104. SHA-256 {NEW_ITEMS[1]['sha256']}."
''')

append_once('database/evidence.yml', '  - id: E-164', f'''
  - id: E-164
    name: 1 September 1916 Enterprise names W. W. Pollock at Fifth Street Restaurant
    type: Primary newspaper visual evidence
    status: VISUALLY VERIFIED
    claims:
      - Fifth Street Restaurant is directly listed with W. W. Pollock and inspection score 75.3.
      - No numbered address, real-estate ownership, or uninterrupted 1916-1919 operating span is proved.
    confidence: Very High for directly printed Pollock/business/score wording; exact premises, title, and continuity unresolved.
    related_sources: [S-184]
    related_businesses: [BUS-070]
    related_people: [P-101]
    repository_file: {capture_path}
  - id: E-165
    name: 19 November 1920 Enterprise identifies Guy Proffit interest in Fifth Street Restaurant
    type: Primary newspaper visual evidence
    status: VISUALLY VERIFIED
    claims:
      - Article directly says Guy Proffit is interested in Fifth Street Restaurant and will retain his interests there.
      - Wording does not establish sole proprietorship, percentage interest, leasehold, property title, exact premises, or continuity from Pollock.
    confidence: Very High for directly printed business-interest wording; legal character, premises, ownership, and continuity unresolved.
    related_sources: [S-185]
    related_businesses: [BUS-070]
    related_people: [P-104]
    repository_file: {capture_path}
''')

# Update Pollock's existing canonical person record and profile.
replace_once('database/people.yml', '    related_evidence: [E-161]\n    related_sources: [S-181]\n    repository_file: people/profiles/w-w-pollock.md', '    related_evidence: [E-161, E-164]\n    related_sources: [S-181, S-184]\n    repository_file: people/profiles/w-w-pollock.md')
append_once('people/profiles/w-w-pollock.md', '## 1 September 1916 inspection listing', '''
## 1 September 1916 inspection listing

The 1 September 1916 *Oregon City Enterprise* state inspection report directly lists **“Fifth Street restaurant, W. W. Pollock, 75.3”** (`E-164` / `S-184`). This moves Pollock's documented association with the restaurant back to September 1916. It does not prove uninterrupted operation from 1916 through the separate October 1919 “conducting” report, nor does it establish property ownership or a numbered address.
''')

# Add Guy Proffit as a distinct person.
if not (ROOT / 'people/profiles/guy-proffit.md').exists():
    write('people/profiles/guy-proffit.md', '''# Guy Proffit

Person ID: `P-104`. Related business: `BUS-070` Fifth Street Restaurant.

The 19 November 1920 *Oregon City Enterprise*, in reporting his marriage to Leathel Cross, directly states that **Guy Proffit “is interested in the Fifth Street Restaurant in this city”** and **“will retain his interests here,”** while making daily trips to Portland (`E-165` / `S-185`).

The wording establishes a reported business-interest role on that date. It does not establish sole proprietorship, percentage ownership, a partnership with W. W. Pollock, leasehold, land/building title, exact street number, or uninterrupted continuity before or after the report.
''')
append_once('people/people-index.md', '| P-104 | [Guy Proffit]', '''

## 2 September 2026 Fifth Street Restaurant supplement

| ID | Name | Role | Notes |
| --- | --- | --- | --- |
| P-104 | [Guy Proffit](profiles/guy-proffit.md) | Reported business-interest holder, Fifth Street Restaurant | 19 Nov. 1920 Enterprise says he was “interested in” the restaurant and would retain his interests; exact legal/ownership character and premises unresolved. `E-165` / `S-185`. |
''')
append_once('database/people.yml', '  - id: P-104', '''
  - id: P-104
    name: Guy Proffit
    role: Reported business-interest holder in Fifth Street Restaurant
    notes: 19 November 1920 Enterprise says Proffit was interested in Fifth Street Restaurant and would retain his interests while making daily trips to Portland. This is not proof of sole proprietorship, ownership percentage, leasehold, property title, or continuity from Pollock.
    related_businesses: [BUS-070]
    related_evidence: [E-165]
    related_sources: [S-185]
    repository_file: people/profiles/guy-proffit.md
''')

# Sync BUS-070 YAML mirror and add a concise index supplement.
replace_once('database/businesses.yml',
    '    notes: Named by 1916 inspection, W. W. Pollock conducting it in 1919, and active-place evidence in 1921. July 1922 property/fire records place the restaurant in the Fifth/Main cluster; one Enterprise account prints L. E. Blakely/Blakely for restaurant ownership and C. P. Gates for building ownership, while other reports print J. Blake / Ed. Blake / Ed Gage and C. / C. E. Gates. Conflicts preserved; building burned and C. E. Gates replacement followed.\n    related_people: [P-036, P-087, P-088, P-092, P-101, P-102, P-103]\n    related_evidence: [E-096, E-097, E-103, E-160, E-161, E-162, E-163]\n    related_sources: [S-111, S-112, S-113, S-117, S-180, S-181, S-182, S-183]',
    '    notes: Named by 1916 inspection; 1 September 1916 directly associates W. W. Pollock with it, and Pollock is described as conducting it in 1919. Guy Proffit held a reported interest in November 1920; active-place evidence follows in 1921. July 1922 property/fire records place the restaurant in the Fifth/Main cluster; one Enterprise account prints L. E. Blakely/Blakely for restaurant ownership and C. P. Gates for building ownership, while other reports print J. Blake / Ed. Blake / Ed Gage and C. / C. E. Gates. Conflicts preserved; building burned and C. E. Gates replacement followed.\n    related_people: [P-036, P-087, P-088, P-092, P-101, P-102, P-103, P-104]\n    related_evidence: [E-096, E-097, E-103, E-160, E-161, E-162, E-163, E-164, E-165]\n    related_sources: [S-111, S-112, S-113, S-117, S-180, S-181, S-182, S-183, S-184, S-185]')
append_once('businesses/fifth-street-restaurant.md', '## Pollock / Proffit supplement — 2 September 2026', '''
## Pollock / Proffit supplement — 2 September 2026

Two additional visually verified Enterprise pages tighten the pre-fire chronology. On **1 September 1916**, the state inspection list directly prints **Fifth Street restaurant, W. W. Pollock, 75.3** (`E-164` / `S-184`). On **19 November 1920**, a marriage item says **Guy Proffit** was **interested in the Fifth Street Restaurant** and would **retain his interests** there (`E-165` / `S-185`).

These dated facts do not establish a continuous Pollock-to-Proffit transfer, partnership shares, real-estate ownership, or a numbered address. The two separately uploaded 21 July 1922 fire PDFs supplied with this supplement are exact duplicates of the already-preserved `S-183` page and therefore were not added again.
''')
append_once('businesses/business-index.md', '## 2 September 2026 Fifth Street Restaurant Pollock / Proffit supplement', '''

## 2 September 2026 Fifth Street Restaurant Pollock / Proffit supplement

`BUS-070` now has direct **W. W. Pollock** association on 1 September 1916 (`E-164` / `S-184`) and a reported **Guy Proffit** business interest on 19 November 1920 (`E-165` / `S-185`). Neither record proves the exact numbered premises, property title, partnership percentage, or uninterrupted succession.
''')

append_once('database/timeline.yml', '  - id: T-059', '''
  - id: T-059
    date: 1 September 1916
    summary: Oregon City Enterprise state inspection report directly lists Fifth Street restaurant, W. W. Pollock, 75.3, supplying a named Pollock association one day after a separate Courier inspection summary.
    confidence: Very High for printed business/person/score; exact premises, title, and continuity unresolved.
    related_evidence: [E-164]
    related_sources: [S-184]
    related_people: [P-101]
    related_businesses: [BUS-070]
  - id: T-060
    date: 19 November 1920
    summary: Oregon City Enterprise says Guy Proffit is interested in Fifth Street Restaurant and will retain his interests there while making daily trips to Portland.
    confidence: Very High for printed interest wording; legal character/percentage, property title, exact premises, and continuity unresolved.
    related_evidence: [E-165]
    related_sources: [S-185]
    related_people: [P-104]
    related_businesses: [BUS-070]
''')
append_once('timeline.md', '### 1 September 1916 — Pollock directly named at Fifth Street Restaurant', '''

### 1 September 1916 — Pollock directly named at Fifth Street Restaurant
The *Oregon City Enterprise* state inspection list directly prints **Fifth Street restaurant, W. W. Pollock, 75.3** (`E-164` / `S-184`). This is a dated person/business association, not proof of property ownership, exact number, or uninterrupted operation through 1919.

### 19 November 1920 — Guy Proffit reported with an interest in the Fifth Street Restaurant
The *Oregon City Enterprise* states that **Guy Proffit** “is interested in the Fifth Street Restaurant” and “will retain his interests here” (`E-165` / `S-185`). The wording does not establish sole ownership, percentage, leasehold, or a transfer from Pollock.
''')
append_once('registers/business-timeline.md', '| 1 Sep. 1916 | Fifth Street Restaurant — W. W. Pollock directly named', '''
| 1 Sep. 1916 | Fifth Street Restaurant — W. W. Pollock directly named with inspection score 75.3 | `BUS-070` | `E-164` / `S-184` | Very High | No numbered address or property title; continuity to 1919 not assumed. |
| 19 Nov. 1920 | Fifth Street Restaurant — Guy Proffit reported “interested in” business and retaining his interests | `BUS-070` | `E-165` / `S-185` | Very High for wording | Exact legal interest, percentage, premises, and continuity unresolved. |
''')
append_once('indexes/id-crosswalk.md', '| `S-184` / `E-164` / `P-101`', '''
| `S-184` / `E-164` / `P-101` | `BUS-070`; `T-059` | 1 Sep. 1916 direct Pollock / Fifth Street Restaurant / 75.3 inspection listing; exact premises and continuity unresolved. |
| `S-185` / `E-165` / `P-104` | `BUS-070`; `T-060` | 19 Nov. 1920 Guy Proffit reported business interest; legal character/percentage and exact premises unresolved. |
| `S-183` / `E-163` duplicate aliases | `BUS-070` | Two steward filenames uploaded 2 Sep. 2026 are byte-identical to existing 21 Jul. 1922 source; no duplicate PDF or ID created. |
''')
append_once('ARCHIVE_INDEX.md', '### Fifth Street Restaurant Pollock / Proffit supplement — 2 September 2026', f'''

### Fifth Street Restaurant Pollock / Proffit supplement — 2 September 2026
- `S-184` / `E-164`: 1 Sep. 1916 Enterprise p. 5 directly names W. W. Pollock at Fifth Street Restaurant with inspection score 75.3; preserved at `{NEW_ITEMS[0]['actual_repo_path']}`.
- `S-185` / `E-165`: 19 Nov. 1920 Enterprise p. 5 reports Guy Proffit interested in the restaurant and retaining his interests; preserved at `{NEW_ITEMS[1]['actual_repo_path']}`.
- Two separately named 21 Jul. 1922 steward uploads are exact SHA-256 duplicates of existing `S-183` and are provenance aliases only.
- Review/provenance: `{capture_path}`.
''')
append_once('evidence/open-questions.md', '### OQ — Pollock / Proffit Fifth Street Restaurant relationship', '''

### OQ — Pollock / Proffit Fifth Street Restaurant relationship
**OPEN.** `E-164` directly names W. W. Pollock at Fifth Street Restaurant in September 1916 and `E-161` calls him its conductor in October 1919; `E-165` reports Guy Proffit with an interest in November 1920. Determine whether these represent continuity, a partnership, a transfer, or distinct operating arrangements. Do not infer a transaction from sequence alone.
''')
append_once('evidence/research-leads.md', '## Fifth Street Restaurant Pollock / Proffit business-interest lead — 2 September 2026', '''

## Fifth Street Restaurant Pollock / Proffit business-interest lead — 2 September 2026
Search 1916–1921 city licenses, directories, tax/assessment records, partnership notices, legal notices, and additional newspapers for **W. W. Pollock**, **Guy Proffit**, and Fifth Street Restaurant. Target the legal character of Proffit's “interests,” any Pollock-to-Proffit relationship/transfer, and a numbered premises. Preserve search silence as non-proof.
''')
append_once('registers/research-log.md', '## 2026-09-02 — Fifth Street Restaurant Pollock / Proffit steward uploads', f'''

## 2026-09-02 — Fifth Street Restaurant Pollock / Proffit steward uploads
Visually verified and integrated 1 Sep. 1916 Enterprise p. 5 (`S-184` / `E-164`) and 19 Nov. 1920 Enterprise p. 5 (`S-185` / `E-165`). Exact Oregon Digital PDF bytes were required to match steward-upload SHA-256/size before preservation. Two separately named 21 Jul. 1922 uploads matched existing `S-183` byte-for-byte and were deduplicated. See `{capture_path}`.
''')

print('Integrated Fifth Street Restaurant Pollock/Proffit supplement:')
for item in NEW_ITEMS:
    print(item['source_id'], item['actual_repo_path'], item['sha256'], 'existing' if item['already_preserved'] else 'new')
print('July 1922 duplicate aliases -> S-183', DUPLICATE_1922['sha256'])
