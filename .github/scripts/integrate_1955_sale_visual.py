from pathlib import Path
import hashlib, re, subprocess, urllib.request


def run(*cmd, check=True):
    print('+', ' '.join(cmd))
    return subprocess.run(cmd, check=check, text=True)


def replace_required(path, old, new, count=1):
    p = Path(path)
    s = p.read_text(encoding='utf-8')
    if old not in s:
        raise SystemExit(f'missing replacement in {path}: {old!r}')
    p.write_text(s.replace(old, new, count), encoding='utf-8')


run('git', 'config', 'user.name', 'main-street-archive-bot')
run('git', 'config', 'user.email', '49879113+rodyoung1967@users.noreply.github.com')
run('git', 'pull', '--rebase', 'origin', 'main')

# Preserve the same original JP2 that was visually reviewed in the research session.
url = 'https://oregonnews.uoregon.edu/lccn/sn85042472/1955-11-20/ed-1/seq-30.jp2'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 Main-Street-Archive/1.0'})
with urllib.request.urlopen(req, timeout=60) as r:
    data = r.read()
sha = hashlib.sha256(data).hexdigest()
expected = '50a237e527267eae87393ec3e8d5b45e9c87fca60e7bb66d46fa06d6efd2ef48'
print('JP2', len(data), sha)
if sha != expected:
    raise SystemExit(f'JP2 hash mismatch: {sha}')
out = Path('newspapers/eugene-register-guard/1955-11-20-image-30.jp2')
out.parent.mkdir(parents=True, exist_ok=True)
out.write_bytes(data)

# Upgrade the dedicated source capture from OCR-only to scan-certified.
p = Path('evidence/source-captures/1955-11-20-505-main-beer-pool-sale-ad-original-ocr.md')
s = p.read_text(encoding='utf-8')
s = s.replace(
    'Status: **PRIMARY NEWSPAPER PAGE LOCATED / OCR TEXT RECOVERED; PAGE IMAGE NOT VISUALLY CERTIFIED IN THIS PASS; SELLER UNNAMED; PHONE OCR CONFLICT UNRESOLVED.**',
    'Status: **PRIMARY NEWSPAPER PAGE / ORIGINAL JP2 RETRIEVED AND VISUALLY VERIFIED; SELLER UNNAMED; CONTACT PHONE VISUALLY READ AS 9179.**'
)
s = s.replace(
    'University of Oregon Historic Oregon Newspapers OCR route:\n\n`https://oregonnews.uoregon.edu/lccn/sn85042472/1955-11-20/ed-1/seq-30/ocr/`',
    'University of Oregon Historic Oregon Newspapers page:\n\n`https://oregonnews.uoregon.edu/lccn/sn85042472/1955-11-20/ed-1/seq-30/`\n\nOriginal JP2:\n\n`https://oregonnews.uoregon.edu/lccn/sn85042472/1955-11-20/ed-1/seq-30.jp2`\n\nRepository source file:\n\n`newspapers/eugene-register-guard/1955-11-20-image-30.jp2`\n\nSHA-256: `50a237e527267eae87393ec3e8d5b45e9c87fca60e7bb66d46fa06d6efd2ef48`.'
)
phone_block = '''## Telephone number — resolved by visual inspection

The original 3724 × 5408 JP2 was visually inspected. The printed contact line is clearly legible as **“Phone 9179”**.

This supersedes two earlier non-visual readings:

- the University of Oregon OCR rendered the number as `0179`;
- earlier project work had carried `6179` as a working reading.

The original page image controls this transcription. The canonical contact number for this **20 November 1955 sale advertisement** is therefore **9179**.

This does not establish whether `9179` was a business line, a seller's residence line, an agent's line, or another contact number. Subscriber identity remains unresolved.

'''
s2, n = re.subn(r'(?ms)^## Telephone-number boundary\n.*?(?=^## What this source establishes)', phone_block, s, count=1)
if n != 1:
    raise SystemExit('telephone boundary block not found')
s = s2
s = s.replace(
    'This advertisement directly establishes that on **20 November 1955** an unnamed seller offered for sale an established **beer/pool tavern business at 505 Main Street** with three pool tables, beer/wine sales, and amusement machines.',
    'This advertisement directly establishes that on **20 November 1955** an unnamed seller offered for sale an established **beer/pool tavern business at 505 Main Street** with three pool tables, beer/wine sales, amusement machines, and contact phone **9179**.'
)
s = s.replace('- the seller\'s identity;\n', '- the seller\'s identity;\n- who subscribed to telephone **9179**;\n', 1)
s = s.replace(
    '1. visually inspect the original Register-Guard page image to resolve the telephone number;\n2. search both **0179** and **6179** independently in 1953–55 Oregon City telephone directories and contemporary newspaper advertising;',
    '1. search **9179** in 1953–55 Oregon City telephone directories, city directories, and contemporary advertising to identify the subscriber/contact;'
)
if '## Cross-record propagation audit' not in s:
    s += '''\n## Cross-record propagation audit\n\nThis visual review changes a source transcription and strengthens `E-039`; it does **not** create a new proprietor, business name, business-transfer date, building-owner fact, or real-estate transaction. The 505 timeline, business timeline, source/evidence registers, YAML evidence/source records, 1953/1960 directory leads, and Enterprise Courier retrieval plan are synchronized. No new person/business ID or crosswalk relationship is warranted.\n'''
p.write_text(s, encoding='utf-8')

# Propagate the verified number through later retrieval controls.
replace_required(
    'evidence/source-captures/1953-oregon-city-vicinity-directory-lead.md',
    'Nov 1955 classified: unnamed long-established beer/pool tavern at **505 Main**, phone **6179**, three pool tables.',
    'Nov 1955 classified: unnamed long-established beer/pool tavern at **505 Main**, contact phone **9179** visually verified from the original page image, three pool tables.'
)
replace_required(
    'evidence/source-captures/1960-oregon-city-directory-505-main-lead.md',
    'November 1955 classified: long-established **beer / pool** business at **505 Main**, phone 6179, three pool tables; business name not recovered;',
    'November 1955 classified: long-established **beer / pool** business at **505 Main**, contact phone **9179** visually verified from the original page image, three pool tables; business name not recovered;'
)
replace_required(
    'evidence/source-captures/1950-1992-oregon-city-enterprise-courier-local-microfilm-route-2026-09-07.md',
    '- phone `0179` and `6179` as separate discovery variants until the original regional ad is visually resolved;',
    '- visually verified contact phone **`9179`** from the original 20 Nov. 1955 regional ad; search that number for subscriber, proprietor, sale, transfer, and reopening references;'
)

# Source register + YAML.
p = Path('evidence/source-register.md')
s = p.read_text(encoding='utf-8')
old = '## S-037 — Eugene Register-Guard, 20 November 1955, beer-pool classified\nSource/location: https://oregonnews.uoregon.edu/lccn/sn85042472/1955-11-20/ed-1/seq-30/ocr/'
new = '## S-037 — Eugene Register-Guard, 20 November 1955, beer-pool classified\nSource/location: https://oregonnews.uoregon.edu/lccn/sn85042472/1955-11-20/ed-1/seq-30/\nRepository scan: `newspapers/eugene-register-guard/1955-11-20-image-30.jp2` (SHA-256 `50a237e527267eae87393ec3e8d5b45e9c87fca60e7bb66d46fa06d6efd2ef48`)\nVisual verification: Original JP2 inspected 7 Sep. 2026; the ad prints contact phone **9179**. OCR `0179` and prior working reading `6179` are superseded.'
if old not in s:
    raise SystemExit('S-037 source pattern missing')
p.write_text(s.replace(old, new, 1), encoding='utf-8')
replace_required('database/sources.yml', '    url: https://oregonnews.uoregon.edu/lccn/sn85042472/1955-11-20/ed-1/seq-30/ocr/', '    url: https://oregonnews.uoregon.edu/lccn/sn85042472/1955-11-20/ed-1/seq-30/')

# Evidence register + YAML.
p = Path('evidence/evidence-register.md')
s = p.read_text(encoding='utf-8')
m = re.search(r'(?ms)^## E-039 .*?(?=^## E-040 )', s)
if not m:
    raise SystemExit('E-039 block missing')
block = m.group(0)
if '9179' not in block:
    block = block.rstrip() + '\nVisual verification (7 Sep. 2026): Original `S-037` JP2 inspected; the classified prints contact phone **9179**. University OCR `0179` and earlier working `6179` are superseded. Seller/subscriber identity remains unresolved.\n\n'
    s = s[:m.start()] + block + s[m.end():]
    p.write_text(s, encoding='utf-8')

p = Path('database/evidence.yml')
s = p.read_text(encoding='utf-8')
claim = '      - November 20 1955 Eugene Register-Guard offered a beer-and-pool tavern for sale with inquiries to 505 Main Street, Oregon City.\n'
add = '      - Original page visual review confirms the advertisement printed contact phone 9179; OCR 0179 and earlier working 6179 readings are superseded.\n'
if claim not in s:
    raise SystemExit('E-039 YAML claim missing')
if add not in s:
    p.write_text(s.replace(claim, claim + add, 1), encoding='utf-8')

# Chronology.
p = Path('timelines/505-main.md')
s = p.read_text(encoding='utf-8')
s2, n = re.subn(r'\| Nov\. 1955 \| Unnamed beer-and-pool tavern\. \| Primary use lead; no invented trade name\. \| `E-039` \|', '| Nov. 1955 | Unnamed beer-and-pool tavern offered for sale; contact phone **9179**. | **Primary newspaper page visually verified**; seller and trade name unprinted/unresolved. | `E-039`; `S-037` |', s, count=1)
if n != 1:
    raise SystemExit('505 timeline 1955 row missing')
p.write_text(s2, encoding='utf-8')
replace_required('registers/business-timeline.md', '| Nov. 1955 | Beer-and-pool tavern (unnamed in ad) | | `E-039` | Very High | |', '| Nov. 1955 | Beer-and-pool tavern (unnamed in ad) | | `E-039` | Very High / original page visually verified | Contact phone **9179**; seller and trade name remain unresolved. |')

# Research log.
p = Path('registers/research-log.md')
s = p.read_text(encoding='utf-8')
if '1955 505 Main sale-ad visual certification' not in s:
    s = s.rstrip() + '''\n\n## 7 September 2026 — 1955 505 Main sale-ad visual certification\n- Retrieved and preserved the original University of Oregon JP2 for *Eugene Register-Guard*, 20 Nov. 1955, Image 30 at `newspapers/eugene-register-guard/1955-11-20-image-30.jp2` (`S-037`; SHA-256 `50a237e527267eae87393ec3e8d5b45e9c87fca60e7bb66d46fa06d6efd2ef48`).\n- Visual inspection directly reads **505 Main Street, Oregon City** and **Phone 9179** in the **BEER — POOL** classified. UO OCR `0179` and earlier project reading `6179` are superseded.\n- Seller/proprietor, telephone subscriber, trade name, sale completion, and buyer remain unresolved. No new person/business/crosswalk relationship was created.\n'''
    p.write_text(s + '\n', encoding='utf-8')

# Remove temporary tooling, including this script/workflow.
for f in [
    '.github/workflows/fetch-1955-505-sale-page-scan.yml',
    '.github/workflows/integrate-1955-505-sale-visual-review.yml',
    '.github/workflows/integrate-1955-505-sale-v2.yml',
    '.github/scripts/integrate_1955_sale_visual.py',
]:
    Path(f).unlink(missing_ok=True)

run('python3', 'scripts/validate_archive.py')
run('git', 'add', '-A')
run('git', 'status', '--short')
run('git', 'commit', '-m', 'Visually verify 1955 505 sale ad phone 9179')
for attempt in range(3):
    r = subprocess.run(['git', 'push', 'origin', 'HEAD:main'], text=True)
    if r.returncode == 0:
        print('push succeeded')
        break
    print('push failed; rebasing onto current main')
    run('git', 'pull', '--rebase', 'origin', 'main')
else:
    raise SystemExit('push failed after retries')
