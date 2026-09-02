#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import tarfile
import tempfile
from pathlib import Path

ROOT = Path('.')
BRANCH = 'origin/research-1902-1903-courier'
AUDIT = ROOT / 'registers/branch-consolidation-research-1902-1903-courier-2026-09-01.md'
MARKER = 'LEGACY_BRANCH_INTEGRATED_V1'


def run(*args: str) -> str:
    return subprocess.check_output(args, text=True).strip()


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding='utf-8')


def write(path: str, text: str) -> None:
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding='utf-8')


def append_once(path: str, marker: str, text: str) -> None:
    current = read(path)
    if marker in current:
        return
    if not current.endswith('\n'):
        current += '\n'
    write(path, current + '\n' + text.rstrip() + '\n')


def insert_before(path: str, anchor: str, marker: str, text: str) -> None:
    current = read(path)
    if marker in current:
        return
    if anchor not in current:
        raise RuntimeError(f'anchor not found in {path}: {anchor!r}')
    write(path, current.replace(anchor, text.rstrip() + '\n\n' + anchor, 1))


def replace_required(path: str, old: str, new: str) -> None:
    current = read(path)
    if new in current:
        return
    if old not in current:
        raise RuntimeError(f'required text not found in {path}')
    write(path, current.replace(old, new, 1))


def next_num(prefix: str, paths: list[str]) -> int:
    rx = re.compile(rf'\b{re.escape(prefix)}-(\d+)\b')
    nums: list[int] = []
    for path in paths:
        nums.extend(int(x) for x in rx.findall(read(path)))
    return max(nums, default=0) + 1


def ids(prefix: str, start: int, count: int, width: int) -> list[str]:
    return [f'{prefix}-{n:0{width}d}' for n in range(start, start + count)]


def add_source_to_e061_yaml(source_id: str) -> None:
    path = 'database/evidence.yml'
    text = read(path)
    start = text.index('  - id: E-061\n')
    end = text.index('\n  - id: E-062\n', start)
    block = text[start:end]
    if source_id in block:
        return
    needle = '    related_sources:\n      - S-075\n'
    if needle not in block:
        raise RuntimeError('E-061 related_sources shape changed')
    block = block.replace(needle, needle + f'      - {source_id}\n', 1)
    write(path, text[:start] + block + text[end:])


def make_branch_snapshot() -> tuple[str, str, list[str], str]:
    branch_sha = run('git', 'rev-parse', BRANCH)
    main_sha = run('git', 'rev-parse', 'HEAD')
    merge_base = run('git', 'merge-base', 'HEAD', BRANCH)
    changed = [x for x in run('git', 'diff', '--name-only', f'{merge_base}..{BRANCH}').splitlines() if x]
    out = ROOT / 'records/repository-history/research-1902-1903-courier-legacy-branch-snapshot.tar.gz'
    out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        base = Path(td) / 'research-1902-1903-courier'
        (base / 'branch-files').mkdir(parents=True)
        (base / 'BRANCH_SHA.txt').write_text(branch_sha + '\n', encoding='utf-8')
        (base / 'MAIN_BASELINE_SHA.txt').write_text(main_sha + '\n', encoding='utf-8')
        (base / 'MERGE_BASE_SHA.txt').write_text(merge_base + '\n', encoding='utf-8')
        (base / 'commits.txt').write_text(
            run('git', 'log', '--reverse', '--format=fuller', f'{merge_base}..{BRANCH}') + '\n', encoding='utf-8'
        )
        (base / 'branch.diff').write_text(
            subprocess.check_output(['git', 'diff', '--binary', f'{merge_base}..{BRANCH}'], text=True), encoding='utf-8'
        )
        file_hashes = {}
        for path in changed:
            data = subprocess.check_output(['git', 'show', f'{BRANCH}:{path}'])
            dest = base / 'branch-files' / path
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(data)
            file_hashes[path] = hashlib.sha256(data).hexdigest()
        (base / 'manifest.json').write_text(
            json.dumps({'branch': BRANCH, 'branch_sha': branch_sha, 'merge_base': merge_base,
                        'main_baseline': main_sha, 'changed_files': changed, 'sha256': file_hashes}, indent=2) + '\n',
            encoding='utf-8'
        )
        with tarfile.open(out, 'w:gz') as tf:
            tf.add(base, arcname=base.name)
    digest = hashlib.sha256(out.read_bytes()).hexdigest()
    manifest_path = 'records/repository-history/research-1902-1903-courier-legacy-branch-snapshot.json'
    write(manifest_path, json.dumps({
        'branch': 'research-1902-1903-courier', 'branch_sha': branch_sha, 'merge_base': merge_base,
        'main_baseline': main_sha, 'archive': str(out), 'archive_sha256': digest, 'changed_files': changed
    }, indent=2) + '\n')
    return branch_sha, main_sha, changed, digest


def main() -> None:
    if AUDIT.exists() and MARKER in AUDIT.read_text(encoding='utf-8'):
        print('legacy branch already integrated')
        return

    branch_sha, baseline_sha, changed, snapshot_sha = make_branch_snapshot()

    s_start = next_num('S', ['evidence/source-register.md', 'database/sources.yml'])
    e_start = next_num('E', ['evidence/evidence-register.md', 'database/evidence.yml'])
    b_start = next_num('BUS', ['businesses/business-index.md', 'database/businesses.yml'])
    rl_start = next_num('RL', ['evidence/research-leads.md'])
    oq_start = next_num('OQ', ['evidence/open-questions.md'])

    S = ids('S', s_start, 10, 3)
    E = ids('E', e_start, 6, 3)
    B = ids('BUS', b_start, 3, 3)
    RL = f'RL-{rl_start:03d}'
    OQ = f'OQ-{oq_start:03d}'

    source_capture = f'''# 1902–1904 legacy-branch consolidation — Main Street context

Integration date: **1 September 2026**  
Legacy branch: `research-1902-1903-courier` at `{branch_sha}`  
Baseline `main`: `{baseline_sha}`  
Annual status: **IN PROGRESS** for 1902, 1903, and 1904.

This capture preserves and normalizes the useful source trail from the old branch without reusing its obsolete `E-057`–`E-064` identifiers, which now refer to different canonical evidence on `main`. The complete old branch state is retained byte-for-byte inside `records/repository-history/research-1902-1903-courier-legacy-branch-snapshot.tar.gz`.

**Verification caution:** this consolidation did not newly inspect the remote newspaper scans. It preserves the legacy branch's recorded readings and canonical URLs. Where the old branch used OCR endpoints, those items remain **OCR/TEXT ONLY** until a scan is visually re-certified. No annual closeout status changes here.

## {S[0]} — Courier-Herald, 3 January 1902, p. 24
URL: https://oregonnews.uoregon.edu/lccn/sn00063697/1902-01-03/ed-1/seq-24.pdf  
Legacy reading: Herman Schrader's profile says that before purchasing his then-current bakery about a year earlier he had worked nearly eighteen years in the **Main-Street Bakery**. This does not identify a later 5xx storefront or prove continuity with his later Main Street bakery.

## {S[1]} — Courier-Herald, 24 October 1902, p. 5
URL: https://oregonnews.uoregon.edu/lccn/sn00063697/1902-10-24/ed-1/seq-5.pdf  
Legacy reading: Huntley Bros. occupied two adjoining store rooms that were remodeled into essentially one store; a partition was removed and a plate-glass front installed. The notice does not place those rooms on the Fifth–Sixth study block.

## {S[2]} — Oregon City Courier, 7 November 1902, p. 1
URLs:  
- https://oregonnews.uoregon.edu/lccn/sn00063698/1902-11-07/ed-1/seq-1/  
- https://oregonnews.uoregon.edu/lccn/sn00063698/1902-11-07/ed-1/seq-1.pdf  
Legacy reading: **The Union Store**, Michael proprietor, advertised a closing/liquidation sale at **“Main St., between 5th and 6th Sts.”** Stock and fixtures were to be sold and the stock was to be gone by New Year. This is block-level evidence only; no later number is assigned.

## {S[3]} — Oregon City Courier, 2 January 1903, p. 4
URL: https://oregonnews.uoregon.edu/lccn/sn00063698/1903-01-02/ed-1/seq-4.pdf  
Legacy reading: **Portland Clothing House — “Next Door to Harding's Drug Store.”** This establishes adjacency, not a number. A separate local item says M. Michael expected to leave for Baker City after the Union Store liquidation; that is continuity context, not a numbered-address bridge.

## {S[4]} — Fair Store 1903 source set
Primary URL: https://oregonnews.uoregon.edu/lccn/sn00063698/1903-01-23/ed-1/seq-3/  
Additional legacy URLs:  
- https://oregonnews.uoregon.edu/lccn/sn00063698/1903-04-24/ed-1/seq-9/ocr/  
- https://oregonnews.uoregon.edu/lccn/sn00063700/1903-05-15/ed-1/seq-8/ocr/  
Legacy reading: **The Fair Store** advertised **“Opposite Postoffice”** on 23 January. April copy described a stock reduction in anticipation of a May 1 move, and the May OCR says **“The Fair Store Must Move.”** The April/May items are **OCR/TEXT ONLY** in this consolidation. Later 1905 Willamette-Building evidence does not by itself prove the spring-1903 destination.

## {S[5]} — Clackamas County Record, 6 April 1903, p. 8
URLs:  
- https://oregonnews.uoregon.edu/lccn/sn00063710/1903-04-06/ed-1/seq-8/  
- https://oregonnews.uoregon.edu/lccn/sn00063710/1903-04-06/ed-1/seq-8.pdf  
Legacy reading: **Geo. A. Harding — Willamette Building — The Leading Drug Store of Oregon City.** This directly associates Harding's drug business with the named building in 1903 but supplies no later street number.

## {S[6]} — 1904 Courier mapping-context set
Legacy URLs:  
- 3 Jun p4: https://oregonnews.uoregon.edu/lccn/sn00063698/1904-06-03/ed-1/seq-4.pdf  
- 12 Aug p8: https://oregonnews.uoregon.edu/lccn/sn00063698/1904-08-12/ed-1/seq-8/  
- 26 Aug p3: https://oregonnews.uoregon.edu/lccn/sn00063698/1904-08-26/ed-1/seq-3/  
- 2 Dec p10: https://oregonnews.uoregon.edu/lccn/sn00063698/1904-12-02/ed-1/seq-10.pdf  
Recorded context: Cross & Shaw on Main; Dr. O. A. Stuart in the **Willamette Building**; a New Book Store opening in **Lamb & Sawyer's Building, next to Oregon City Bank**; Willamette Grocery in the Stevens Building at Sixth/Main; Petzold's Cash Market on Main (later direct evidence places Petzold at 696 Main, so it is not treated as a target-block candidate). No 1904 Courier target number or secure Fifth–Sixth tenant was recovered; this is not vacancy evidence.

## {S[7]} — Oregon City Enterprise, 15 January 1904, p. 3
URL: https://oregonnews.uoregon.edu/lccn/sn00063700/1904-01-15/ed-1/seq-3/  
Legacy context: Farmers' Store on Main opposite Barlow's Grocery and Electric Grocery on Main next to Albright's Market. Neither is mapped to the target block here.

## {S[8]} — Oregon City Courier, 24 August 1906, p. 3
OCR URL: https://oregonnews.uoregon.edu/lccn/sn00063698/1906-08-24/ed-1/seq-3/ocr/  
Legacy reading: council reporting says an ordinance was passed **“Providing for numbering of houses.”** This is **OCR/TEXT ONLY** here and corroborates the broader, already canonical 1906 numbering record `E-061`; it does not replace the richer ordinance/plat evidence already on `main`.

## Mapping synthesis retained from the old branch

The strongest pre-numbering relationships are relational rather than numeric:

- Union Store → **Main between Fifth and Sixth** (1902).
- Portland Clothing House → **next door to Harding's Drug Store** (1903).
- Harding Drug Store → **Willamette Building** (1903).
- Fair Store → **opposite Post Office** and moving in spring 1903.
- Willamette Building remains active commercial/office premises in 1904.

The legacy branch also noted that the Fair Store appears in a **Harding Block** advertisement in April 1905 and in the **Willamette Building** in later 1905 Courier advertising. Whether those names were the same building, overlapping premises, or different locations remains open under `{RL}`. Do not project later 5xx addresses backward without a bridging source.
'''
    write('evidence/source-captures/1902-1904-legacy-branch-consolidation.md', source_capture)

    holman_capture = f'''# 26 February 1914 — R. L. Holman move from Eighth/Main to Fifth/Main

Source: `{S[9]}`  
Evidence: `{E[5]}`  
Legacy branch: `research-1902-1903-courier` at `{branch_sha}`  
Status: **legacy primary-page reading preserved; scan not independently re-certified during this branch-consolidation run**.

Canonical page: https://oregonnews.uoregon.edu/lccn/sn00063698/1914-02-26/ed-1/seq-7/  
Canonical PDF: https://oregonnews.uoregon.edu/lccn/sn00063698/1914-02-26/ed-1/seq-7.pdf

The legacy branch records that the *Oregon City Courier* reported **R. L. Holman moved his undertaking establishment from the Caufield Building on Eighth and Main Street to his building on Fifth and Main Street**.

This moves the documented Fifth/Main relocation back from the separately visually verified 28 August 1914 *Morning Enterprise* advertisement. The wording **“his building”** is evidence of a reported ownership relationship to the Fifth/Main premises, but no numbered Main address or legal parcel is printed. Do not equate the premises with 501 Main without an independent address/property bridge.

The exact old branch file and its full context are retained inside the repository-history snapshot tarball.
'''
    write('evidence/source-captures/1914-02-26-holman-move-fifth-main-legacy-branch-integration.md', holman_capture)

    business_pages = {
        B[0]: ('union-store-1902.md', f'''# The Union Store\n\nBusiness ID: `{B[0]}`.\n\nA 7 November 1902 *Oregon City Courier* advertisement, preserved from the legacy branch as `{S[2]}` / `{E[1]}`, places **The Union Store** on **Main Street between Fifth and Sixth Streets** and identifies the proprietor only as **Michael**. The advertisement announces liquidation/closing and says stock and fixtures are to be sold by New Year.\n\nThe exact later 5xx storefront, legal ownership, opening date, proprietor's full identity, and whether the liquidation completed exactly as advertised remain unresolved. Do not infer vacancy after the advertisement without a later source.\n'''),
        B[1]: ('portland-clothing-house.md', f'''# Portland Clothing House\n\nBusiness ID: `{B[1]}`.\n\nA 2 January 1903 *Oregon City Courier* advertisement, preserved as `{S[3]}` / `{E[2]}`, places **Portland Clothing House next door to Harding's Drug Store**. The source does not print a number.\n\nThis is a storefront-adjacency anchor only. It must not be assigned to 505, 507, 509, 511, or another later number without an independent pre-/post-numbering bridge.\n'''),
        B[2]: ('fair-store.md', f'''# The Fair Store\n\nBusiness ID: `{B[2]}`.\n\nA 23 January 1903 *Oregon City Courier* advertisement places **The Fair Store opposite the Post Office**. April and May 1903 legacy records indicate an impending move; those later items remain OCR/TEXT ONLY in this consolidation. See `{S[4]}` / `{E[3]}`.\n\nThe old branch also recorded Fair Store advertisements in **Harding Block** and the **Willamette Building** in 1905. Whether the spring-1903 move led to that building, and whether Harding Block and Willamette Building were the same or overlapping premises, remain unresolved under `{RL}`.\n'''),
    }
    for bid, (filename, body) in business_pages.items():
        write(f'businesses/{filename}', body)

    evidence_files = [
        (E[0], '1902-schrader-main-street-bakery-background.md', 'Schrader Main-Street Bakery background, 1902', S[0],
         'A 3 January 1902 Courier-Herald profile says Herman Schrader had worked nearly eighteen years in the Main-Street Bakery before purchasing his then-current bakery about a year earlier. This extends the Main Street bakery chronology but does not identify a later numbered storefront or prove physical continuity.',
         'Legacy primary-source reading; exact-address and storefront continuity unresolved.'),
        (E[1], '1902-union-store-main-between-fifth-sixth.md', 'Union Store on Main between Fifth and Sixth, 1902', S[2],
         'A 7 November 1902 Courier advertisement places The Union Store, Michael proprietor, on Main Street between Fifth and Sixth Streets and announces liquidation of stock and fixtures. The exact later storefront number and later disposition are not established.',
         'Very high for the legacy branch transcription of the printed block location; visual recertification and exact-number mapping pending.'),
        (E[2], '1903-portland-clothing-next-harding.md', 'Portland Clothing House next to Harding Drug Store, 1903', S[3],
         "A 2 January 1903 Courier advertisement places Portland Clothing House next door to Harding's Drug Store. The source supplies adjacency but no street number.",
         'Very high for the preserved adjacency reading; exact premises and later-number mapping unresolved.'),
        (E[3], '1903-fair-store-postoffice-move.md', 'Fair Store opposite Post Office and spring move, 1903', S[4],
         'The 23 January 1903 Courier places The Fair Store opposite the Post Office. Legacy April/May records indicate an impending move; those later records are retained as OCR/TEXT ONLY. The destination is not established.',
         'High for the preserved January relative-location reading; April/May move wording needs scan recertification; destination unresolved.'),
        (E[4], '1903-harding-drug-willamette-building.md', 'Harding Drug Store in Willamette Building, 1903', S[5],
         'A 6 April 1903 Clackamas County Record item identifies Geo. A. Harding and his leading drug store in the Willamette Building. It does not print a later Main Street number.',
         'Very high for the preserved building-name association; exact numbered footprint and continuity unresolved.'),
        (E[5], '1914-holman-moves-fifth-main-february.md', 'R. L. Holman moves from Eighth/Main to his Fifth/Main building, 26 February 1914', S[9],
         'The legacy branch records a 26 February 1914 Courier notice saying R. L. Holman moved his undertaking establishment from the Caufield Building at Eighth and Main to his building at Fifth and Main. This predates the separately verified August 1914 Fifth/Main advertisement. The notice prints no numbered address.',
         "Very high for the preserved move wording; 'his building' is reported ownership language, while exact parcel/number remains unresolved."),
    ]
    for eid, filename, name, sid, claim, confidence in evidence_files:
        related = ''
        if eid == E[0]: related = f'\nRelated person: `P-096`  \nRelated business: `BUS-063`'
        elif eid == E[1]: related = f'\nRelated business: `{B[0]}`'
        elif eid == E[2]: related = f'\nRelated business: `{B[1]}`  \nAdjacent business: `BUS-007`'
        elif eid == E[3]: related = f'\nRelated business: `{B[2]}`'
        elif eid == E[4]: related = '\nRelated person: `P-001`  \nRelated business: `BUS-007`'
        elif eid == E[5]: related = '\nRelated person: `P-050`  \nCandidate building relationship: `B-005`'
        body = f'''# {eid} — {name}\n\nType: Primary newspaper reading recovered from legacy branch; verification state preserved conservatively  \nSource: `{sid}`{related}\n\n## Claim supported\n\n{claim}\n\n## Verification / limits\n\nThe complete pre-consolidation branch record is retained in `records/repository-history/research-1902-1903-courier-legacy-branch-snapshot.tar.gz`. This integration did not newly inspect the remote scan, so it does not upgrade the legacy verification state.\n\nConfidence: **{confidence}**\n'''
        write(f'evidence/{eid}-{filename}', body)

    source_rows = [
        (S[0], 'Courier-Herald, 3 January 1902, p. 24, Schrader profile', 'https://oregonnews.uoregon.edu/lccn/sn00063697/1902-01-03/ed-1/seq-24.pdf', E[0]),
        (S[1], 'Courier-Herald, 24 October 1902, p. 5, Huntley Bros. remodel', 'https://oregonnews.uoregon.edu/lccn/sn00063697/1902-10-24/ed-1/seq-5.pdf', None),
        (S[2], 'Oregon City Courier, 7 November 1902, p. 1, Union Store', 'https://oregonnews.uoregon.edu/lccn/sn00063698/1902-11-07/ed-1/seq-1/', E[1]),
        (S[3], 'Oregon City Courier, 2 January 1903, p. 4, Portland Clothing House', 'https://oregonnews.uoregon.edu/lccn/sn00063698/1903-01-02/ed-1/seq-4.pdf', E[2]),
        (S[4], 'Fair Store 1903 Post Office / move source set', 'https://oregonnews.uoregon.edu/lccn/sn00063698/1903-01-23/ed-1/seq-3/', E[3]),
        (S[5], 'Clackamas County Record, 6 April 1903, p. 8, Harding / Willamette Building', 'https://oregonnews.uoregon.edu/lccn/sn00063710/1903-04-06/ed-1/seq-8/', E[4]),
        (S[6], 'Oregon City Courier 1904 mapping-context source set', 'https://oregonnews.uoregon.edu/lccn/sn00063698/1904-08-26/ed-1/seq-3/', None),
        (S[7], 'Oregon City Enterprise, 15 January 1904, p. 3, Main Street adjacencies', 'https://oregonnews.uoregon.edu/lccn/sn00063700/1904-01-15/ed-1/seq-3/', None),
        (S[8], 'Oregon City Courier, 24 August 1906, p. 3, house-numbering ordinance report', 'https://oregonnews.uoregon.edu/lccn/sn00063698/1906-08-24/ed-1/seq-3/ocr/', 'E-061'),
        (S[9], 'Oregon City Courier, 26 February 1914, p. 7, Holman move notice', 'https://oregonnews.uoregon.edu/lccn/sn00063698/1914-02-26/ed-1/seq-7/', E[5]),
    ]
    src_md = ['## Legacy branch sources integrated 1 September 2026', '',
              'These source IDs preserve previously branch-only research. The branch snapshot is retained under `records/repository-history/`. Verification states are not silently upgraded during consolidation.', '']
    src_yaml = []
    for sid, name, url, evid in source_rows:
        src_md += [f'## {sid} — {name}', f'URL: {url}  ', 'Type: Primary newspaper source / legacy-branch source trail.  ',
                   f'Related evidence: `{evid}`  ' if evid else 'Related evidence: contextual source only; no standalone claim-level record assigned.  ',
                   'Repository capture: `evidence/source-captures/1902-1904-legacy-branch-consolidation.md`  ' if sid != S[9] else 'Repository capture: `evidence/source-captures/1914-02-26-holman-move-fifth-main-legacy-branch-integration.md`  ',
                   'Notes: Preserved from legacy branch; this consolidation did not independently re-certify the remote scan. OCR endpoints remain OCR/TEXT ONLY where applicable.', '']
        src_yaml += [f'  - id: {sid}', f'    name: {json.dumps(name)}', f'    url: {json.dumps(url)}',
                     '    notes: ' + json.dumps('Preserved from research-1902-1903-courier during branch consolidation. Full readings, URLs, verification caveats and branch-snapshot provenance are in the integration capture. No verification state was upgraded merely by consolidation.'), '']
    append_once('evidence/source-register.md', '## Legacy branch sources integrated 1 September 2026', '\n'.join(src_md))
    append_once('database/sources.yml', f'  - id: {S[0]}\n', '\n'.join(src_yaml))

    ev_md = ['## Legacy 1902–1903 / February 1914 evidence integrated 1 September 2026', '']
    ev_yaml = []
    for idx, (eid, filename, name, sid, claim, confidence) in enumerate(evidence_files):
        repo_file = f'evidence/{eid}-{filename}'
        ev_md += [f'## {eid} — {name}', 'Type: Primary newspaper reading recovered from legacy branch; conservative verification state.  ',
                  f'Sources: `{sid}`  ', f'Related record: `{repo_file}`  ', f'Claims: {claim}  ', f'Confidence: {confidence}', '']
        ev_yaml += [f'  - id: {eid}', f'    name: {json.dumps(name)}',
                    '    type: ' + json.dumps('Primary newspaper reading recovered from legacy branch; verification state preserved conservatively'),
                    '    claims:', '      - ' + json.dumps(claim), f'    confidence: {json.dumps(confidence)}',
                    f'    related_sources: [{sid}]']
        if idx == 0:
            ev_yaml += ['    related_businesses: [BUS-063]', '    related_people: [P-096]']
        elif idx == 1:
            ev_yaml += [f'    related_businesses: [{B[0]}]']
        elif idx == 2:
            ev_yaml += [f'    related_businesses: [{B[1]}, BUS-007]']
        elif idx == 3:
            ev_yaml += [f'    related_businesses: [{B[2]}]']
        elif idx == 4:
            ev_yaml += ['    related_businesses: [BUS-007]', '    related_people: [P-001]']
        elif idx == 5:
            ev_yaml += ['    related_people: [P-050]', '    related_buildings: [B-005]']
        ev_yaml += [f'    repository_file: {repo_file}', '']
    append_once('evidence/evidence-register.md', '## Legacy 1902–1903 / February 1914 evidence integrated 1 September 2026', '\n'.join(ev_md))
    append_once('database/evidence.yml', f'  - id: {E[0]}\n', '\n'.join(ev_yaml))

    biz_index = f'''## 1902–1903 businesses promoted from legacy branch consolidation

| ID | Business | Address / Association | Notes |
| --- | --- | --- | --- |
| {B[0]} | [The Union Store](union-store-1902.md) | Main between Fifth and Sixth, 7 Nov. 1902 | Liquidation ad; proprietor printed only as Michael; exact later number and completed disposition unresolved. `{E[1]}` / `{S[2]}`. |
| {B[1]} | [Portland Clothing House](portland-clothing-house.md) | Next door to Harding's Drug Store, 2 Jan. 1903 | Adjacency only; no later number assigned. `{E[2]}` / `{S[3]}`. |
| {B[2]} | [The Fair Store](fair-store.md) | Opposite Post Office, Jan. 1903; spring move pending | April/May move items retain OCR/TEXT ONLY status; later Willamette/Harding Block relationship unresolved. `{E[3]}` / `{S[4]}`. |
'''
    append_once('businesses/business-index.md', '## 1902–1903 businesses promoted from legacy branch consolidation', biz_index)
    biz_yaml = f'''  - id: {B[0]}
    name: The Union Store
    repository_file: businesses/union-store-1902.md
    address: Main Street between Fifth and Sixth Streets (1902); exact later number unresolved
    notes: Legacy 7 Nov 1902 advertisement announces liquidation and identifies proprietor only as Michael; do not infer vacancy or completed closure without later evidence.
    related_evidence: [{E[1]}]
    related_sources: [{S[2]}]

  - id: {B[1]}
    name: Portland Clothing House
    repository_file: businesses/portland-clothing-house.md
    address: Next door to Harding's Drug Store (1903); number unresolved
    notes: Relative-location anchor only; no property ownership or later numbered storefront assigned.
    related_evidence: [{E[2]}]
    related_sources: [{S[3]}]

  - id: {B[2]}
    name: The Fair Store
    repository_file: businesses/fair-store.md
    address: Opposite Post Office (Jan 1903); later move destination unresolved
    notes: Legacy April/May move records preserved conservatively; later 1905 Harding Block/Willamette Building relationship is a research lead, not an established move destination.
    related_evidence: [{E[3]}]
    related_sources: [{S[4]}]
'''
    append_once('database/businesses.yml', f'  - id: {B[0]}\n', biz_yaml)

    append_once('businesses/schraders-bakery.md', '## 1902 Main-Street Bakery background', f'''## 1902 Main-Street Bakery background

Legacy-branch source `{S[0]}` / evidence `{E[0]}` preserves a 3 January 1902 profile saying Herman Schrader had worked nearly eighteen years in the **Main-Street Bakery** before purchasing his then-current bakery about a year earlier. This extends the trade chronology but does not prove the exact later Main Street storefront or continuity to the 1912 premises.
''')
    append_once('businesses/harding-drug-store.md', '## 1903 Willamette Building anchor', f'''## 1903 Willamette Building anchor

Legacy-branch source `{S[5]}` / evidence `{E[4]}` records George A. Harding's drug store in the **Willamette Building** on 6 April 1903. No later street number is back-projected. This early building-name anchor should be tested together with the 1911–1912 Harding/Willamette evidence, not collapsed into a single storefront without proof.
''')
    append_once('people/profiles/george-a-harding.md', '## 1903 Willamette Building business anchor', f'''## 1903 Willamette Building business anchor

`{S[5]}` / `{E[4]}` preserves the legacy-branch reading that Harding's drug business was in the **Willamette Building** in April 1903. The source predates formal citywide numbering and does not justify assigning a later 5xx number to the 1903 premises.
''')
    append_once('people/profiles/herman-schrader.md', '## 1902 Main-Street Bakery background', f'''## 1902 Main-Street Bakery background

`{S[0]}` / `{E[0]}` preserves a 1902 profile stating that Schrader had worked nearly eighteen years in the **Main-Street Bakery** before buying his then-current bakery about a year earlier. Exact premises and continuity to the later Main Street bakery remain unresolved.
''')

    replace_required('evidence/E-061-1906-formal-street-numbering.md',
                     'Source: `S-075`  ', f'Sources: `S-075`, `{S[8]}`  ')
    e061 = read('evidence/E-061-1906-formal-street-numbering.md')
    bullet = f'- **24 August 1906:** a legacy-branch *Courier* council report, retained as `{S[8]}`, says an ordinance was passed “Providing for numbering of houses.” The retained endpoint is OCR/TEXT ONLY in this consolidation and is corroborating context, not a replacement for the visually/independently established ordinance-and-plat trail.\n'
    anchor = '- **3 October 1913:**'
    if bullet.strip() not in e061:
        e061 = e061.replace(anchor, bullet + anchor, 1)
        write('evidence/E-061-1906-formal-street-numbering.md', e061)
    add_source_to_e061_yaml(S[8])

    append_once('evidence/E-054-holman-fifth-main-1915-1917.md', '## 26 February 1914 antecedent', f'''## 26 February 1914 antecedent

The legacy-branch record now retained as `{S[9]}` / `{E[5]}` moves the Fifth/Main chronology back to **26 February 1914**: the *Courier* reported Holman moving from the Caufield Building at Eighth/Main to **his building at Fifth/Main**. The exact later numbered address remains unproved. The separately visually verified 28 August 1914 advertisement independently confirms that Holman had moved to Fifth/Main by that later date.
''')
    b501 = read('buildings/501-main.md')
    if f'`{S[9]}`' not in b501:
        old = '- **28 August 1914:** an *Oregon City Enterprise* advertisement for **R. L. Holman, Leading Funeral Director**, states that he **“has moved to more commodious parlors 5th and Main Sts.”** The original page has now been recovered and reviewed. See `evidence/source-captures/1914-08-28-holman-move-fifth-main.md`.\n'
        new = f'- **26 February 1914:** a *Courier* notice preserved from the legacy branch reports **R. L. Holman moved his undertaking establishment from the Caufield Building at Eighth & Main to his building at Fifth & Main** (`{E[5]}` / `{S[9]}`). The wording “his building” is a reported ownership relationship, not a legal-description or 501-number proof.\n' + old
        if old not in b501:
            raise RuntimeError('501 Holman anchor changed')
        b501 = b501.replace(old, new, 1)
        b501 = b501.replace('from August 1914 onward', 'from February 1914 onward', 1)
        b501 = b501.replace('| Aug. 1914–1917 | Holman / Holman-Randall / Holman undertaking business at **Fifth & Main** | Very High |',
                            '| Feb. 1914–1917 | Holman / Holman-Randall / Holman undertaking business at **Fifth & Main** | Very High for preserved dated sources; exact 501 mapping unresolved |', 1)
        write('buildings/501-main.md', b501)

    stale = '## February 1914\nL. Hylton was profiled at 503 Main (`E-024`). An earlier project statement that undertaker R. L. Holman moved to Fifth & Main in 1914 is **not currently accepted as established** because the contemporaneous move notice has not been recovered (`RL-020`).'
    fresh = f'''## February 1914
L. Hylton was profiled at 503 Main (`E-024`). Separately, the **26 February 1914** *Courier* notice preserved from the legacy branch reports **R. L. Holman moving his undertaking establishment from the Caufield Building at Eighth & Main to his building at Fifth & Main** (`{E[5]}` / `{S[9]}`). This establishes Fifth/Main by that date but does not prove the later number 501 or a legal parcel. The separately visually verified 28 August 1914 *Morning Enterprise* advertisement independently confirms the Fifth/Main location.'''
    replace_required('timeline.md', stale, fresh)

    pre1904 = f'''## 1902 — exact study-block business and older Main Street bakery context
A 7 November *Courier* advertisement places **The Union Store** directly on **Main Street between Fifth and Sixth Streets** (`{E[1]}` / `{S[2]}`). The ad announces liquidation and identifies the proprietor only as Michael; no later number or completed closure is inferred. A January profile separately says Herman Schrader had spent nearly eighteen years in the **Main-Street Bakery** before purchasing his then-current bakery (`{E[0]}` / `{S[0]}`); that history is not assigned to a later numbered storefront. A Huntley Bros. two-room remodel is preserved as `{S[1]}` but was not shown to be on the study block.

## 1903 — Harding/Willamette, Portland Clothing, and Fair Store relative geography
The legacy branch supplies three useful pre-numbering relationships: **Portland Clothing House next door to Harding's Drug Store** (`{E[2]}` / `{S[3]}`); **George A. Harding's drug store in the Willamette Building** (`{E[4]}` / `{S[5]}`); and **The Fair Store opposite the Post Office** with a spring move pending (`{E[3]}` / `{S[4]}`). These are relational anchors only. Later numbers such as Harding's 511 Main address are not projected backward, and the Fair Store's destination remains unproved.

## 1904 — legacy Courier mapping context
A consolidated legacy review (`{S[6]}` / `{S[7]}`) preserves additional building and adjacency anchors, including the active **Willamette Building** and a New Book Store in **Lamb & Sawyer's Building next to Oregon City Bank**. It recovered no defensible 1904 Courier target number or secure named target-block tenant. That is research coverage only, not vacancy evidence. The full old branch is preserved in the repository-history snapshot.
'''
    insert_before('timeline.md', '## Late 1904 — I. Tolpolar on Main Street', '## 1902 — exact study-block business', pre1904)

    old_rl20 = '## RL-020 — Recover the Claimed 1914 Holman Move Notice\nStatus: **Completed.** The 28 August 1914 *Morning Enterprise*, page 3, was recovered and visually reviewed; it reports Holman moving to Fifth and Main. This establishes the intersection-level move but does **not** prove that the premises carried the exact number 501. Exact-number mapping remains under `RL-019` and `RL-025`.'
    new_rl20 = f'''## RL-020 — Recover the Claimed 1914 Holman Move Notice
Status: **Completed and chronology advanced.** The separately visually verified 28 August 1914 *Morning Enterprise* advertisement confirms Holman at Fifth/Main. Legacy-branch source `{S[9]}` / evidence `{E[5]}` now preserves an earlier **26 February 1914 Courier** notice saying Holman moved from the Caufield Building at Eighth/Main to **his building at Fifth/Main**. The February source moves the documented relocation earlier and adds reported ownership wording, but it still does **not** prove the later number 501 or a legal parcel. Exact-number/property mapping remains under `RL-019` and `RL-025`.'''
    replace_required('evidence/research-leads.md', old_rl20, new_rl20)
    leads = read('evidence/research-leads.md')
    if S[8] not in leads:
        needle = 'Primary 1906 newspaper evidence (`E-061` / `S-075`) shows that Mayor Caufield approved a street-numbering ordinance'
        repl = f'Primary 1906 newspaper evidence (`E-061` / `S-075`; corroborating legacy Courier source `{S[8]}`) shows that Mayor Caufield approved a street-numbering ordinance'
        if needle not in leads:
            raise RuntimeError('RL-025 wording changed')
        leads = leads.replace(needle, repl, 1)
        write('evidence/research-leads.md', leads)
    new_lead = f'''## {RL} — Resolve Harding Block / Willamette Building and Fair Store move, 1903–1905
Legacy-branch evidence now preserved on `main` establishes **Harding Drug Store in the Willamette Building** in April 1903 (`{E[4]}` / `{S[5]}`), **Portland Clothing House next door to Harding's** in January 1903 (`{E[2]}` / `{S[3]}`), and **The Fair Store opposite the Post Office** while preparing to move in spring 1903 (`{E[3]}` / `{S[4]}`). The old branch also recorded a 21 April 1905 *Enterprise* Fair Store ad at **Main Street, Harding Block** and later 1905 Courier Fair Store ads in the **Willamette Building**.

Determine whether **Harding Block** and **Willamette Building** were the same building, overlapping/multi-bay premises, adjoining buildings, or different Fair Store locations. Also determine the Fair Store's actual spring-1903 destination. Current later anchors—including Harding at 511 Main by January 1911 and the 1911–1912 Willamette relationships—must not be back-projected automatically. Use directories, deeds, Sanborn detail, building histories, advertisements, and the 1906 numbering plat. Preserve all building-name ambiguity until bridged.
'''
    append_once('evidence/research-leads.md', f'## {RL} — Resolve Harding Block / Willamette Building', new_lead)

    oq = f'''## {OQ} — Which later storefronts correspond to the 1902–1905 pre-numbering relationships?
The legacy-branch consolidation adds a direct 1902 block occupant (**Union Store, Main between Fifth and Sixth**) plus 1903 relative geography (**Portland Clothing next to Harding; Harding in Willamette Building; Fair Store opposite Post Office and moving**). Which original Block 4 storefronts and later 5xx numbers correspond to those descriptions? The 1906 numbering plat and `{RL}` are the primary bridge targets. Do not infer vacancy, same-building identity, or later numbers from adjacency alone.
'''
    append_once('evidence/open-questions.md', f'## {OQ} — Which later storefronts correspond', oq)

    cross = f'''## 1902–1904 legacy branch consolidation

| Source / evidence | Connected records | Scope / limits |
| --- | --- | --- |
| `{S[0]}` / `{E[0]}` | `P-096`; `BUS-063` | Schrader Main-Street Bakery background; no exact later storefront. |
| `{S[2]}` / `{E[1]}` | `{B[0]}` | Union Store directly between Fifth/Sixth; later number unresolved. |
| `{S[3]}` / `{E[2]}` | `{B[1]}`; `BUS-007` adjacency | Portland Clothing next to Harding; no number. |
| `{S[4]}` / `{E[3]}` | `{B[2]}` | Fair Store opposite Post Office; move destination unresolved. |
| `{S[5]}` / `{E[4]}` | `P-001`; `BUS-007` | Harding Drug Store in Willamette Building; later number not backdated. |
| `{S[8]}` | `E-061`; `RL-025` | 24 Aug 1906 Courier OCR corroboration of house-numbering ordinance; not a replacement for canonical plat evidence. |
| `{S[9]}` / `{E[5]}` | `P-050`; candidate `B-005` relationship | Holman move to his Fifth/Main building by 26 Feb 1914; exact 501 mapping unresolved. |

Complete old-branch files, diff and commit log are preserved in `records/repository-history/research-1902-1903-courier-legacy-branch-snapshot.tar.gz`.
'''
    append_once('indexes/id-crosswalk.md', '## 1902–1904 legacy branch consolidation', cross)

    archive_index = f'''## Legacy branch consolidation — 1902–1904 / Holman 1914

The former `research-1902-1903-courier` branch was reconciled against current `main` without merging its obsolete IDs. [Consolidation audit](registers/branch-consolidation-research-1902-1903-courier-2026-09-01.md) and the repository-history snapshot preserve the complete branch-only state. Canonical promoted records are `{E[0]}`–`{E[5]}` / `{S[0]}`–`{S[9]}` with new businesses `{B[0]}`–`{B[2]}`. The 1906 numbering item was attached to existing `E-061`; no duplicate evidence ID was created.
'''
    append_once('ARCHIVE_INDEX.md', '## Legacy branch consolidation — 1902–1904 / Holman 1914', archive_index)

    log_entry = f'''### 2026-09-01 — Consolidate legacy `research-1902-1903-courier` branch
- Compared the 18-commit legacy branch against current `main`; direct merge/cherry-pick was rejected because old branch evidence IDs now collide with different canonical records.
- Preserved the branch tip, merge base, {len(changed)} changed files, commit log and binary diff in `records/repository-history/research-1902-1903-courier-legacy-branch-snapshot.tar.gz` (SHA-256 `{snapshot_sha}`).
- Promoted genuinely missing 1902–1903 relative-location evidence and the 26 February 1914 Holman move using fresh IDs `{E[0]}`–`{E[5]}` / `{S[0]}`–`{S[9]}` and businesses `{B[0]}`–`{B[2]}`; attached the 24 August 1906 Courier numbering corroboration to existing `E-061` instead of creating duplicate evidence.
- Corrected the stale master-timeline statement about the missing Holman move notice; no annual status was advanced. Remote scans were not newly re-certified during branch consolidation, so OCR/text-only and legacy-verification caveats remain explicit.
- Added `{RL}` / `{OQ}` for the unresolved Harding Block–Willamette Building/Fair Store and pre-numbering storefront mapping questions.
'''
    append_once('registers/research-log.md', '### 2026-09-01 — Consolidate legacy `research-1902-1903-courier` branch', log_entry)

    audit = f'''# Legacy branch consolidation audit — `research-1902-1903-courier`

{MARKER}

Integration date: **1 September 2026**  
Branch tip: `{branch_sha}`  
Baseline `main` when integration script started: `{baseline_sha}`  
Snapshot SHA-256: `{snapshot_sha}`

## Why the branch was not merged directly

The old branch reused evidence/source identifiers that now have different meanings on the authoritative archive. For example, its old `E-057` was a Schrader 1902 record while current `E-057` is Tolpolar 1904. A merge or cherry-pick would therefore corrupt canonical identity. The integration instead preserved the complete branch byte-for-byte and promoted missing claims under fresh IDs.

## Complete branch preservation

Archive: `records/repository-history/research-1902-1903-courier-legacy-branch-snapshot.tar.gz`  
Manifest: `records/repository-history/research-1902-1903-courier-legacy-branch-snapshot.json`

The archive contains the branch tip SHA, merge-base SHA, integration baseline SHA, full branch-only commit log, a binary-capable Git diff, and each of the {len(changed)} files changed on the branch:

''' + '\n'.join(f'- `{x}`' for x in changed) + f'''

## Canonical promotion decisions

- Fresh evidence: `{E[0]}`–`{E[5]}`.
- Fresh sources: `{S[0]}`–`{S[9]}`.
- Fresh businesses: `{B[0]}`–`{B[2]}`.
- New follow-up: `{RL}`; new open question: `{OQ}`.
- The branch's 24 August 1906 house-numbering report was added as corroboration to existing `E-061`; its old conflicting evidence ID was not reused.
- The 1904 contextual review and Huntley remodel are preserved in the canonical consolidation capture and source register but were not over-promoted into target-address conclusions.
- The 26 February 1914 Holman notice was promoted because it materially advances the already accepted August 1914 chronology.

## Deletion criterion

Once this commit has passed `python3 scripts/validate_archive.py` and is present on authoritative `main`, no unique information from `research-1902-1903-courier` depends on retaining that Git branch: its complete branch-only state is preserved in the snapshot and its materially useful missing findings are represented in canonical archive records. This statement applies only to this branch; final all-branch deletion safety requires the separate post-integration branch audit.
'''
    write(str(AUDIT), audit)

    print(json.dumps({'branch_sha': branch_sha, 'baseline': baseline_sha, 'sources': S, 'evidence': E,
                      'businesses': B, 'research_lead': RL, 'open_question': OQ, 'snapshot_sha256': snapshot_sha}, indent=2))


if __name__ == '__main__':
    main()
