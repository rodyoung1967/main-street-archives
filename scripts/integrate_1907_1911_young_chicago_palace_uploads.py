from pathlib import Path
import hashlib
import re
import urllib.request

PAGES = [
    dict(key='young1907', url='https://oregonnews.uoregon.edu/lccn/sn00063700/1907-08-16/ed-1/seq-5.pdf', sha='8790cfbaa0af8b70be37cc1fbece4c835fe786dcdf41296edb5fcd78a0a9686f', size=549924, target="newspapers/oregon-city-enterprise/1907-08-16-page-5-youngs-secondhand-store-505-main.pdf", original="505 Main (Young's Second Hand Store) Oregon City enterprise., August 16, 1907, Page 5, Image 5.pdf"),
    dict(key='chi0331', url='https://oregonnews.uoregon.edu/lccn/sn00063698/1911-03-31/ed-1/seq-6.pdf', sha='fc3c0bfc057251e1232530342229bcd4d548c50acda3bda52f98d26d30da5507', size=645029, target='newspapers/oregon-city-courier/1911-03-31-page-6-chicago-store-505-main.pdf', original='505 Main (Chicago Store) Oregon City courier., March 31, 1911, Page 6, Image 6.pdf'),
    dict(key='chi0407', url='https://oregonnews.uoregon.edu/lccn/sn00063698/1911-04-07/ed-1/seq-6.pdf', sha='a06940a0d58fe72639ac8fb3753b5451000169b1ddf207c73f23e081ad10b664', size=662883, target='newspapers/oregon-city-courier/1911-04-07-page-6-chicago-store-505-main.pdf', original='505 Main (Chicago Store) Oregon City courier., April 07, 1911, Page 6, Image 6.pdf'),
    dict(key='chi0428', url='https://oregonnews.uoregon.edu/lccn/sn00063698/1911-04-28/ed-1/seq-7.pdf', sha='fe0458e8c500e00a3653b21cf2ebc1a471ddcaa2ec885647380636bfbf383e99', size=716160, target='newspapers/oregon-city-courier/1911-04-28-page-7-chicago-store-505-main.pdf', original='505 Main (Chicago Store) Oregon City courier., April 28, 1911, Page 7, Image 7.pdf'),
    dict(key='pal0314', url='https://oregonnews.uoregon.edu/lccn/sn00063701/1911-03-14/ed-1/seq-3.pdf', sha='f7fbbf6e23b10967bec4b7201633b9b9084babfb8ba697ce9bf6e4d9b254c86b', size=871363, target='newspapers/morning-enterprise/1911-03-14-page-3-palace-saloon-joseph-wilson-license.pdf', original='Palace Saloon (Liquor Licence) Morning enterprise., March 14, 1911, Page 3, Image 3.pdf'),
]

def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()

def read(path):
    return Path(path).read_text(encoding='utf-8')

def write(path, text):
    Path(path).write_text(text, encoding='utf-8')

def append_once(path, marker, block):
    text = read(path)
    if marker not in text:
        write(path, text.rstrip() + '\n\n' + block.strip() + '\n')

def replace_md_section(path, heading, block):
    text = read(path)
    pattern = re.compile(r'(?ms)^' + re.escape(heading) + r'\n.*?(?=^## |\Z)')
    if not pattern.search(text):
        raise SystemExit(f'missing section {heading} in {path}')
    write(path, pattern.sub(block.strip() + '\n\n', text, count=1))

def replace_yaml_block(path, ident, block):
    text = read(path)
    pattern = re.compile(r'(?ms)^  - id: ' + re.escape(ident) + r'\n.*?(?=^  - id: |\Z)')
    if not pattern.search(text):
        raise SystemExit(f'missing yaml id {ident} in {path}')
    write(path, pattern.sub(block.strip() + '\n\n', text, count=1))

def mutate_yaml_block(path, ident, fn):
    text = read(path)
    pattern = re.compile(r'(?ms)^  - id: ' + re.escape(ident) + r'\n.*?(?=^  - id: |\Z)')
    match = pattern.search(text)
    if not match:
        raise SystemExit(f'missing yaml id {ident} in {path}')
    new = fn(match.group(0).rstrip()) + '\n\n'
    write(path, text[:match.start()] + new + text[match.end():])

existing = {}
for p in Path('.').rglob('*.pdf'):
    try:
        existing.setdefault(sha256(p), str(p))
    except OSError:
        pass

for item in PAGES:
    if item['sha'] in existing:
        item['actual'] = existing[item['sha']]
        item['status'] = 'already present; deduplicated'
        continue
    req = urllib.request.Request(item['url'], headers={'User-Agent': 'Mozilla/5.0'})
    data = urllib.request.urlopen(req, timeout=60).read()
    got = hashlib.sha256(data).hexdigest()
    if got != item['sha'] or len(data) != item['size']:
        raise SystemExit(f"hash/size mismatch for {item['key']}: {got} {len(data)}")
    path = Path(item['target'])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    item['actual'] = item['target']
    item['status'] = 'newly preserved'
    existing[item['sha']] = item['target']

by = {item['key']: item for item in PAGES}

replace_md_section('evidence/source-register.md', '## S-032 — Chicago Store advertisements, 1911-1913', f'''## S-032 — Chicago Store advertisements, 1911-1913
URL: https://oregonnews.uoregon.edu/lccn/sn00063698/1911-04-14/ed-1/seq-7/ocr/  
Related evidence: `E-026`, `E-108`  
Repository PDFs now preserved:
- `{by['chi0331']['actual']}` — 31 March 1911 p. 6, SHA-256 `{by['chi0331']['sha']}`
- `{by['chi0407']['actual']}` — 7 April 1911 p. 6, SHA-256 `{by['chi0407']['sha']}`
- `{by['chi0428']['actual']}` — 28 April 1911 p. 7, SHA-256 `{by['chi0428']['sha']}`
Notes: Primary advertisements place The Chicago Store at **505 Main** by 31 March and through April 1911. Also see `S-061` for its 5 January 1912 wording "Main St. just below Postoffice." The supplied 505 advertisements do not identify Wolf & Nat as proprietors.''')

replace_md_section('evidence/evidence-register.md', '## E-026 — The Chicago Store at 505 Main, 1911-1913', '''## E-026 — The Chicago Store at 505 Main, 1911-1913
Type: Primary newspaper advertisements; **VISUALLY VERIFIED** for the supplied 31 March, 7 April and 28 April 1911 pages.  
Sources: `S-032`  
Claims: The 31 March, 7 April, 14 April and 28 April 1911 *Oregon City Courier* advertisements place The Chicago Store at **505 Main**; the supplied pages advertise new/second-hand clothing plus cleaning and repairing. Morning Enterprise 8 January 1913 again places the store at 505.  
Confidence: Very High for the printed business/address on the supplied scans; proprietor identity after the move and property/building ownership remain unresolved.''')

replace_yaml_block('database/sources.yml', 'S-032', f'''  - id: S-032
    name: Chicago Store advertisements, 1911-1913
    url: https://oregonnews.uoregon.edu/lccn/sn00063698/1911-04-14/ed-1/seq-7/ocr/
    notes: Exact supplied page PDFs preserved for 31 March, 7 April and 28 April 1911 at 505 Main; also 14 April 1911 Courier and 8 January 1913 Morning Enterprise. Related evidence E-026. Repository PDFs: {by['chi0331']['actual']}; {by['chi0407']['actual']}; {by['chi0428']['actual']}.''')

replace_yaml_block('database/evidence.yml', 'E-026', '''  - id: E-026
    name: The Chicago Store at 505 Main, 1911-1913
    type: Primary newspaper advertisements; supplied 1911 pages visually verified
    claims:
      - Oregon City Courier advertisements directly place The Chicago Store at 505 Main by 31 March 1911 and continue the address through April 1911.
      - The supplied 31 March, 7 April and 28 April scans advertise new and second-hand clothing plus cleaning and repairing.
      - The supplied 505 advertisements do not identify Wolf & Nat as proprietors; proprietor continuity after the move remains unresolved.
    confidence: Very High for printed business/address and advertised services; proprietor/title/structure continuity unresolved.
    related_sources: [S-032]
    related_businesses: [BUS-011]
    related_buildings: [B-002]''')

for sid in ('S-189', 'S-190'):
    if f'## {sid} —' in read('evidence/source-register.md') or f'  - id: {sid}\n' in read('database/sources.yml'):
        raise SystemExit(f'{sid} already assigned unexpectedly')
for eid in ('E-168', 'E-169'):
    if f'## {eid} —' in read('evidence/evidence-register.md') or f'  - id: {eid}\n' in read('database/evidence.yml'):
        raise SystemExit(f'{eid} already assigned unexpectedly')

append_once('evidence/source-register.md', '## S-189 —', f'''## S-189 — Oregon City Enterprise, 16 August 1907, p. 5, Young's Second Hand Store at 505 Main
Canonical PDF: {by['young1907']['url']}  
Repository PDF: `{by['young1907']['actual']}`  
Original uploaded filename: `{by['young1907']['original']}`  
Type: Primary newspaper advertisement; **VISUALLY VERIFIED**.  
Related evidence: `E-168`; business `BUS-067`; building `B-002`.  
Notes: Auction advertisement directly prints **Young's Second Hand Store / 505 Main Street, Oregon City, Oregon**. It does not print George Young's given name, so identity with `P-076` remains a strong trade-name/address inference rather than an explicit personal identification. SHA-256 `{by['young1907']['sha']}`.''')
append_once('evidence/source-register.md', '## S-190 —', f'''## S-190 — Morning Enterprise, 14 March 1911, p. 3, Joseph Wilson Palace Saloon license notice
Canonical PDF: {by['pal0314']['url']}  
Repository PDF: `{by['pal0314']['actual']}`  
Original uploaded filename: `{by['pal0314']['original']}`  
Type: Primary newspaper liquor-license notice; **VISUALLY VERIFIED**.  
Related evidence: `E-169`; business `BUS-024`; person `P-037` by strong Joe/Joseph identity inference.  
Notes: Notice names **JOSEPH WILSON** applying for a three-month liquor license at **The Palace Saloon, Fifth and Main streets**. It does not print 501 or prove that the Council granted the license. SHA-256 `{by['pal0314']['sha']}`.''')

append_once('evidence/evidence-register.md', '## E-168 —', '''## E-168 — Young's Second Hand Store at 505 Main, 16 August 1907
Type: Primary newspaper advertisement; **VISUALLY VERIFIED**.  
Source: `S-189`  
Claims: The 16 August 1907 *Oregon City Enterprise* auction advertisement directly prints **Young's Second Hand Store, 505 Main Street, Oregon City, Oregon**. This establishes the trade name and exact numbered address by that date. The advertisement itself does not name George/G. H. Young, establish property ownership, or prove continuity with the surviving 505 building.  
Confidence: Very High for printed trade name and exact address; Strong inference only for identity with `P-076` / later Young records.''')
append_once('evidence/evidence-register.md', '## E-169 —', '''## E-169 — Joseph Wilson at Palace Saloon, Fifth and Main, 14 March 1911
Type: Primary newspaper liquor-license notice; **VISUALLY VERIFIED**.  
Source: `S-190`  
Claims: The 14 March 1911 *Morning Enterprise* notice names **Joseph Wilson** applying for a three-month liquor license at **The Palace Saloon, Fifth and Main streets**. It moves verified Wilson/Palace evidence back from June 1911 to March 1911. The notice does not print 501, prove a license grant, property ownership, or uninterrupted succession.  
Confidence: Very High for printed applicant/trade-name/intersection wording; Joe Wilson = Joseph Wilson remains a strong identity inference.''')

append_once('database/sources.yml', '  - id: S-189', f'''  - id: S-189
    name: Oregon City Enterprise, 16 August 1907, p. 5, Young's Second Hand Store at 505 Main
    url: {by['young1907']['url']}
    notes: Visually verified exact 505 Main auction advertisement for Young's Second Hand Store. Repository PDF {by['young1907']['actual']}; E-168/BUS-067/B-002. SHA-256 {by['young1907']['sha']}.

  - id: S-190
    name: Morning Enterprise, 14 March 1911, p. 3, Joseph Wilson Palace Saloon license notice
    url: {by['pal0314']['url']}
    notes: Visually verified Joseph Wilson three-month liquor-license application at The Palace Saloon, Fifth and Main streets. No 501 number or grant proof. Repository PDF {by['pal0314']['actual']}; E-169/BUS-024. SHA-256 {by['pal0314']['sha']}.''')
append_once('database/evidence.yml', '  - id: E-168', '''  - id: E-168
    name: Young's Second Hand Store at 505 Main, 16 August 1907
    type: Primary newspaper advertisement; visually verified
    claims:
      - The advertisement directly prints Young's Second Hand Store, 505 Main Street, Oregon City, Oregon.
      - It establishes the trade name and exact numbered address by 16 August 1907.
      - It does not explicitly name George/G. H. Young, prove property ownership, or prove surviving-building continuity.
    confidence: Very High for printed trade name and exact address; Strong inference only for individual identity with later Young records.
    related_sources: [S-189]
    related_businesses: [BUS-067]
    related_buildings: [B-002]

  - id: E-169
    name: Joseph Wilson at Palace Saloon, Fifth and Main, 14 March 1911
    type: Primary newspaper liquor-license notice; visually verified
    claims:
      - Joseph Wilson announces a three-month liquor-license application at The Palace Saloon, Fifth and Main streets.
      - The notice does not print 501 Main or prove the license was granted.
      - Joe Wilson equals Joseph Wilson remains a strong identity inference from the repeated trade name/location sequence.
    confidence: Very High for printed applicant, trade name and intersection; exact number, grant, title and uninterrupted succession unresolved.
    related_sources: [S-190]
    related_people: [P-037]
    related_businesses: [BUS-024]''')

Path('evidence/E-168-1907-08-16-youngs-second-hand-store-505-main.md').write_text("""# E-168 — Young's Second Hand Store at 505 Main, 16 August 1907

Type: Primary newspaper advertisement; **VISUALLY VERIFIED**.

The 16 August 1907 *Oregon City Enterprise* auction advertisement directly prints **Young's Second Hand Store, 505 Main Street, Oregon City, Oregon** (`S-189`). The ad does not name George/G. H. Young, establish property title, or prove continuity with the surviving building.
""", encoding='utf-8')
Path('evidence/E-169-1911-03-14-joseph-wilson-palace-saloon.md').write_text("""# E-169 — Joseph Wilson at Palace Saloon, Fifth and Main, 14 March 1911

Type: Primary newspaper liquor-license notice; **VISUALLY VERIFIED**.

The 14 March 1911 *Morning Enterprise* notice directly names **Joseph Wilson** applying for a three-month license at **The Palace Saloon, Fifth and Main streets** (`S-190`). It does not print 501 Main or prove a grant, title, or uninterrupted succession.
""", encoding='utf-8')

mutate_yaml_block('database/businesses.yml', 'BUS-067', lambda b: b.replace('related_evidence: [E-085, E-092, E-134]', 'related_evidence: [E-085, E-092, E-134, E-168]').replace('related_sources: [S-098, S-102, S-149]', 'related_sources: [S-098, S-102, S-149, S-189]'))

def add_palace_refs(block):
    if '      - E-169' not in block and '    related_sources:' in block:
        block = block.replace('    related_sources:', '      - E-169\n    related_sources:', 1)
    if '      - S-190' not in block and '    repository_file:' in block:
        block = block.replace('    repository_file:', '      - S-190\n    repository_file:', 1)
    block = block.replace('Joseph Wilson applies at Palace, Fifth/Main in June 1911;', 'Joseph Wilson applies at Palace, Fifth/Main in March and June 1911;')
    return block
mutate_yaml_block('database/businesses.yml', 'BUS-024', add_palace_refs)

append_once('businesses/chicago-store.md', '## Preserved 1911 505 Main page scans', f'''## Preserved 1911 505 Main page scans
The project-steward uploads for **31 March**, **7 April**, and **28 April 1911** are now preserved as exact page PDFs under `S-032` / `E-026`: `{by['chi0331']['actual']}`, `{by['chi0407']['actual']}`, and `{by['chi0428']['actual']}`. Each visibly prints The Chicago Store at **505 Main**. These ads do not themselves repeat the earlier Wolf & Nat proprietor line.''')
append_once('businesses/gh-young-curio-man.md', '## 16 August 1907 exact-505 advertisement', '''## 16 August 1907 exact-505 advertisement
`S-189` / `E-168` visually verifies an *Oregon City Enterprise* auction advertisement for **Young's Second Hand Store, 505 Main Street** on 16 August 1907. This pushes the exact-numbered trade-name anchor back from the CCHS photograph dated 1910. Because the ad does not print George/G. H. Young's given name, the individual identity link remains a strong inference rather than explicit wording.''')
append_once('businesses/palace-saloon.md', '## 14 March 1911 Joseph Wilson evidence', '''## 14 March 1911 Joseph Wilson evidence
`S-190` / `E-169` visually verifies **Joseph Wilson** applying for a three-month liquor license at **The Palace Saloon, Fifth and Main streets** on 14 March 1911. This precedes the already-preserved 20 June 1911 notice. It does not print 501 Main or prove the license was granted.''')
append_once('people/profiles/joe-wilson.md', '## 14 March 1911 update', '''## 14 March 1911 update
`S-190` / `E-169` adds an earlier **Joseph Wilson** Palace Saloon license notice at **Fifth and Main** dated 14 March 1911. Read with June 1911, March 1912 and June 1912 notices, the Joe/Joseph identity inference is strengthened, but no source explicitly states that Joe is a nickname or legal-name equivalent.''')
append_once('buildings/505-main.md', '## 1907 Young / 1911 Chicago page-scan supplement', '''## 1907 Young / 1911 Chicago page-scan supplement
`S-189` / `E-168` directly places **Young's Second Hand Store at 505 Main** on 16 August 1907. Exact steward-supplied Chicago Store page scans now preserved under `S-032` / `E-026` directly place **The Chicago Store at 505 Main** on 31 March, 7 April and 28 April 1911. These are occupancy/trade-name anchors, not proof of real-estate ownership or surviving-building continuity.''')
append_once('timelines/505-main.md', '## 2 September 2026 early-source supplement', '''## 2 September 2026 early-source supplement
- **16 Aug. 1907:** Young's Second Hand Store is directly advertised at **505 Main** (`S-189` / `E-168`); the ad itself does not name George Young.
- **31 Mar., 7 Apr., 28 Apr. 1911:** exact preserved Chicago Store page scans directly print **505 Main** (`S-032` / `E-026`), strengthening the documented post-405 move chronology.''')
append_once('timeline.md', "## 16 August 1907 — Young's Second Hand Store at 505 Main", '''## 16 August 1907 — Young's Second Hand Store at 505 Main
A visually verified *Oregon City Enterprise* auction advertisement directly prints **Young's Second Hand Store, 505 Main Street, Oregon City, Oregon** (`S-189` / `E-168`). The advertisement does not itself identify George/G. H. Young or prove building/property ownership.

## 14 March 1911 — Joseph Wilson at the Palace Saloon, Fifth and Main
A visually verified *Morning Enterprise* notice names **Joseph Wilson** applying for a three-month liquor license at **The Palace Saloon, Fifth and Main streets** (`S-190` / `E-169`). The notice does not print 501 or prove the license was granted.''')
append_once('registers/business-timeline.md', "| 16 Aug. 1907 | Young's Second Hand Store", """| 16 Aug. 1907 | Young's Second Hand Store | `BUS-067` | `E-168`; `S-189` | Very High for printed trade name/address | Exact 505 Main auction ad; individual George Young identity is inferred, not printed. |
| 14 Mar. 1911 | Palace Saloon / Joseph Wilson | `BUS-024` | `E-169`; `S-190` | Very High for printed applicant/trade-name/intersection | Fifth/Main only; no 501 number or license-grant proof. |""")
append_once('indexes/id-crosswalk.md', '| `S-189` / `E-168`', """| `S-189` / `E-168` | `BUS-067`; `B-002` | 16 Aug. 1907 Young's Second Hand Store exact 505 Main advertisement; George Young individual identity not explicit. |
| `S-190` / `E-169` | `BUS-024`; `P-037` inference | 14 Mar. 1911 Joseph Wilson Palace Saloon, Fifth/Main license notice; no exact 501 or grant proof. |""")
append_once('ARCHIVE_INDEX.md', '## 1907–1911 Young / Chicago / Palace steward-upload supplement', '''## 1907–1911 Young / Chicago / Palace steward-upload supplement
Five steward-supplied newspaper PDFs are now accounted for in `evidence/source-captures/1907-1911-young-chicago-palace-steward-upload-supplement-2026-09-02.md`. Three Chicago Store pages remain under existing `S-032` / `E-026`; the new 1907 Young exact-505 anchor is `S-189` / `E-168`, and the new 14 March 1911 Joseph Wilson Palace notice is `S-190` / `E-169`.''')
append_once('registers/research-log.md', '1907–1911 Young / Chicago / Palace steward uploads', '''- **2026-09-02 — 1907–1911 Young / Chicago / Palace steward uploads:** verified five supplied PDFs by SHA-256, preserved/deduplicated exact page files, updated `S-032` / `E-026`, and integrated new `S-189` / `E-168` and `S-190` / `E-169` with uncertainty limits preserved.''')

capture = Path('evidence/source-captures/1907-1911-young-chicago-palace-steward-upload-supplement-2026-09-02.md')
lines = [
    '# 1907–1911 Young / Chicago / Palace steward-upload supplement',
    '',
    'Review date: **2 September 2026**.',
    '',
    'Status: **FIVE PROJECT-STEWARD PDF UPLOADS ACCOUNTED FOR BY SHA-256; EXACT CANONICAL PAGE BYTES PRESERVED OR DEDUPLICATED.**',
    '',
]
for item in PAGES:
    lines += [
        f"## {item['key']}", '',
        f"Original upload: `{item['original']}`  ",
        f"Canonical URL: {item['url']}  ",
        f"Repository PDF: `{item['actual']}`  ",
        f"SHA-256: `{item['sha']}` ({item['size']} bytes).  ",
        f"Handling: **{item['status']}**.", '',
    ]
lines += [
    '## Interpretive limits', '',
    "- `E-168` proves the **Young's Second Hand Store** trade name at exact **505 Main** in August 1907; the ad does not print George Young's given name.",
    '- The three Chicago Store pages reinforce exact **505 Main** occupancy in late March/April 1911; they do not themselves identify Wolf & Nat as proprietors.',
    '- `E-169` proves **Joseph Wilson / Palace Saloon / Fifth and Main** on 14 March 1911; it does not print 501 Main or prove a license grant.', '',
]
capture.write_text('\n'.join(lines), encoding='utf-8')

print('1907-1911 steward-upload integration prepared successfully.')
for item in PAGES:
    print(item['key'], item['actual'], item['status'])
