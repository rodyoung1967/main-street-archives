#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import tarfile
import tempfile
from pathlib import Path

ROOT = Path('.')
DATE = '2026-09-01'
OUTDIR = ROOT / 'records/repository-history'
AUDIT = ROOT / f'registers/branch-deletion-audit-{DATE}.md'
MARKER = 'ALL_NON_MAIN_BRANCH_REFS_ARCHIVED_V1'
CHUNK = 70 * 1024 * 1024


def run(*args: str, check: bool = True) -> str:
    p = subprocess.run(args, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=check)
    return p.stdout.strip()


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding='utf-8')


def write(path: str, text: str) -> None:
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding='utf-8')


def append_once(path: str, marker: str, text: str) -> None:
    cur = read(path)
    if marker in cur:
        return
    if not cur.endswith('\n'):
        cur += '\n'
    write(path, cur + '\n' + text.rstrip() + '\n')


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def safe(name: str) -> str:
    return re.sub(r'[^A-Za-z0-9._-]+', '__', name)


def remote_branches() -> list[str]:
    refs = run('git', 'for-each-ref', '--format=%(refname:short)', 'refs/remotes/origin/').splitlines()
    result = []
    for ref in refs:
        if ref in {'origin/HEAD', 'origin/main'} or ref.endswith('/HEAD'):
            continue
        if ref.startswith('origin/'):
            result.append(ref)
    return sorted(set(result))


def main() -> None:
    if AUDIT.exists() and MARKER in AUDIT.read_text(encoding='utf-8'):
        print('all branch refs already archived')
        return

    OUTDIR.mkdir(parents=True, exist_ok=True)
    main_sha = run('git', 'rev-parse', 'HEAD')
    branches = remote_branches()
    if not branches:
        raise RuntimeError('no non-main remote branches found; fetch step likely failed')

    rows = []
    archive_path = OUTDIR / f'all-non-main-branch-refs-{DATE}.tar.gz'
    with tempfile.TemporaryDirectory() as td:
        root = Path(td) / f'all-non-main-branch-refs-{DATE}'
        root.mkdir(parents=True)
        all_manifest = {'created_for_main': main_sha, 'date': DATE, 'branches': []}

        for ref in branches:
            name = ref.removeprefix('origin/')
            tip = run('git', 'rev-parse', ref)
            merge_base = run('git', 'merge-base', 'HEAD', ref)
            counts = run('git', 'rev-list', '--left-right', '--count', f'HEAD...{ref}').split()
            main_only, branch_only = map(int, counts)
            ancestor = subprocess.run(['git', 'merge-base', '--is-ancestor', ref, 'HEAD']).returncode == 0
            changed = [x for x in run('git', 'diff', '--name-only', f'{merge_base}..{ref}').splitlines() if x]
            branch_dir = root / safe(name)
            (branch_dir / 'branch-files').mkdir(parents=True)

            meta = {
                'name': name,
                'remote_ref': ref,
                'tip': tip,
                'merge_base': merge_base,
                'main_at_archive': main_sha,
                'tip_is_ancestor_of_main': ancestor,
                'main_only_commits': main_only,
                'branch_only_commits': branch_only,
                'changed_files_from_merge_base': changed,
                'files': {},
            }
            (branch_dir / 'metadata.json').write_text(json.dumps(meta, indent=2) + '\n', encoding='utf-8')
            log = run('git', 'log', '--reverse', '--format=fuller', f'{merge_base}..{ref}', check=False)
            (branch_dir / 'branch-only-commits.txt').write_text(log + ('\n' if log else ''), encoding='utf-8')
            diff = subprocess.check_output(['git', 'diff', '--binary', f'{merge_base}..{ref}'])
            (branch_dir / 'branch.diff').write_bytes(diff)

            deleted = []
            for path in changed:
                exists = subprocess.run(['git', 'cat-file', '-e', f'{ref}:{path}'], stdout=subprocess.DEVNULL,
                                        stderr=subprocess.DEVNULL).returncode == 0
                if not exists:
                    deleted.append(path)
                    continue
                data = subprocess.check_output(['git', 'show', f'{ref}:{path}'])
                dest = branch_dir / 'branch-files' / path
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(data)
                meta['files'][path] = {'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data)}
            meta['deleted_paths'] = deleted
            (branch_dir / 'metadata.json').write_text(json.dumps(meta, indent=2) + '\n', encoding='utf-8')
            all_manifest['branches'].append(meta)
            rows.append((name, tip, ancestor, main_only, branch_only, len(changed)))

        (root / 'manifest.json').write_text(json.dumps(all_manifest, indent=2) + '\n', encoding='utf-8')
        (root / 'README.md').write_text(
            '# Non-main branch ref archive\n\n'
            'Each branch directory contains its tip/merge-base metadata, branch-only commit log, a binary-capable Git diff, '
            'and the tip version of every path changed from the merge base. The merge-base commits remain in authoritative '
            '`main` history. This archive is intended to preserve branch-only state after remote branch refs are deleted.\n',
            encoding='utf-8')
        with tarfile.open(archive_path, 'w:gz') as tf:
            tf.add(root, arcname=root.name)

    full_hash = sha256(archive_path)
    size = archive_path.stat().st_size
    stored = []
    if size > CHUNK:
        with archive_path.open('rb') as src:
            idx = 1
            while True:
                data = src.read(CHUNK)
                if not data:
                    break
                p = OUTDIR / f'{archive_path.name}.part{idx:03d}'
                p.write_bytes(data)
                stored.append({'path': str(p), 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()})
                idx += 1
        archive_path.unlink()
    else:
        stored.append({'path': str(archive_path), 'bytes': size, 'sha256': full_hash})

    manifest_path = OUTDIR / f'all-non-main-branch-refs-{DATE}-manifest.json'
    manifest_path.write_text(json.dumps({
        'main_at_archive': main_sha,
        'branch_count': len(rows),
        'logical_archive_sha256': full_hash,
        'logical_archive_bytes': size,
        'stored_files': stored,
        'reassembly': 'Concatenate parts in numeric order if split, then verify logical_archive_sha256.',
        'branches': [
            {'name': n, 'tip': tip, 'tip_is_ancestor_of_main': anc, 'main_only_commits': mo,
             'branch_only_commits': bo, 'changed_paths_from_merge_base': ch}
            for n, tip, anc, mo, bo, ch in rows
        ]
    }, indent=2) + '\n', encoding='utf-8')

    table = [
        '| Branch | Tip | Ancestor of main? | Main-only commits | Branch-only commits | Changed paths from merge base |',
        '| --- | --- | ---: | ---: | ---: | ---: |',
    ]
    for n, tip, anc, mo, bo, ch in rows:
        table.append(f'| `{n}` | `{tip[:12]}` | {"yes" if anc else "no"} | {mo} | {bo} | {ch} |')

    audit = f'''# Final branch deletion audit — {DATE}

{MARKER}

Authoritative `main` at archive start: `{main_sha}`  
Non-main branch refs archived: **{len(rows)}**  
Logical archive SHA-256: `{full_hash}`  
Logical archive size: **{size} bytes**  
Manifest: `records/repository-history/all-non-main-branch-refs-{DATE}-manifest.json`

## Purpose

This is the final branch-ref safety archive. It does **not** make superseded hypotheses canonical. Instead, before any branch ref is deleted, it preserves every non-main branch's exact branch-only state: tip SHA, merge base, branch-only commit log, binary-capable diff, and tip versions/hashes of all paths changed from the merge base.

The previously substantive `research-1902-1903-courier` branch was separately reconciled into canonical records and fully snapshotted in `registers/branch-consolidation-research-1902-1903-courier-2026-09-01.md`. The current archive additionally preserves that ref together with every other non-main ref, including squash-merged, superseded, helper/no-op, Cursor, Codex, and closed-unmerged historical branches.

## Branch inventory

''' + '\n'.join(table) + f'''

## Deletion safety rule

After this archive commit is present on `main` **and** `python3 scripts/validate_archive.py` passes, deleting these non-main branch refs will not discard their historical Git-side research state. Branch tips that are ancestors are already in `main` history; branch tips that are not ancestors are recoverable from this archive relative to their merge-base commit, which remains in `main` history.

This audit does not authorize deletion of the repository or of `main`; it applies only to the non-main branch refs listed above.
'''
    write(str(AUDIT), audit)

    archive_note = f'''## Final non-main branch-ref archive — {DATE}

All **{len(rows)}** non-main branch refs were archived before branch cleanup. The [branch deletion audit](registers/branch-deletion-audit-{DATE}.md) records every tip and divergence count; `records/repository-history/all-non-main-branch-refs-{DATE}-manifest.json` records archive hashes and storage chunks. This is repository-history preservation, not promotion of superseded branch hypotheses.
'''
    append_once('ARCHIVE_INDEX.md', f'## Final non-main branch-ref archive — {DATE}', archive_note)

    log = f'''### {DATE} — Archive all non-main branch refs before cleanup
- Archived {len(rows)} non-main branch refs with tip SHA, merge base, commit log, binary diff and changed-file tip state.
- Logical archive SHA-256 `{full_hash}`; storage/chunk hashes are in `records/repository-history/all-non-main-branch-refs-{DATE}-manifest.json`.
- This follows canonical integration of `research-1902-1903-courier`; superseded/unmerged branch states remain historical records, not silently accepted claims.
- Branch refs may be deleted only after this archive is committed to `main` and archive validation passes.
'''
    append_once('registers/research-log.md', f'### {DATE} — Archive all non-main branch refs before cleanup', log)
    print(json.dumps({'main': main_sha, 'branch_count': len(rows), 'archive_sha256': full_hash, 'stored': stored}, indent=2))


if __name__ == '__main__':
    main()
