#!/usr/bin/env python3
"""Rebuild repository-history tarballs from their recorded Git object IDs.

The original archives were omitted because the repository ignored ``*.tar.gz``.
This recovery uses only commit IDs and metadata already preserved on ``main``.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import re
import subprocess
import tarfile
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
HISTORY = ROOT / "records" / "repository-history"
RECOVERY_DATE = "2026-09-08"
LEGACY_MANIFEST = HISTORY / "research-1902-1903-courier-legacy-branch-snapshot.json"
ALL_BRANCHES_MANIFEST = HISTORY / "all-non-main-branch-refs-2026-09-01-manifest.json"


def git(*args: str, binary: bool = False) -> str | bytes:
    return subprocess.check_output(
        ["git", *args], cwd=ROOT, text=not binary
    ).strip() if not binary else subprocess.check_output(["git", *args], cwd=ROOT)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def safe_name(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "__", value)


def ensure_commit(commit: str) -> None:
    subprocess.run(
        ["git", "cat-file", "-e", f"{commit}^{{commit}}"],
        cwd=ROOT,
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8")


def write_json(path: Path, value: dict) -> None:
    write_text(path, json.dumps(value, indent=2))


def deterministic_tar(source: Path, destination: Path) -> None:
    def normalize(info: tarfile.TarInfo) -> tarfile.TarInfo:
        info.uid = 0
        info.gid = 0
        info.uname = ""
        info.gname = ""
        info.mtime = 0
        return info

    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as compressed:
            with tarfile.open(fileobj=compressed, mode="w") as archive:
                archive.add(source, arcname=source.name, filter=normalize)


def capture_branch(root: Path, name: str, tip: str, main_baseline: str) -> dict:
    ensure_commit(tip)
    ensure_commit(main_baseline)
    merge_base = str(git("merge-base", main_baseline, tip))
    changed = [
        line for line in str(git("diff", "--name-only", f"{merge_base}..{tip}")).splitlines()
        if line
    ]
    destination = root / safe_name(name)
    files_dir = destination / "branch-files"
    files_dir.mkdir(parents=True)

    log = str(git("log", "--reverse", "--format=fuller", f"{merge_base}..{tip}"))
    write_text(destination / "branch-only-commits.txt", log)
    (destination / "branch.diff").write_bytes(
        bytes(git("diff", "--binary", f"{merge_base}..{tip}", binary=True))
    )

    file_records: dict[str, dict[str, int | str]] = {}
    deleted_paths: list[str] = []
    for repository_path in changed:
        exists = subprocess.run(
            ["git", "cat-file", "-e", f"{tip}:{repository_path}"],
            cwd=ROOT,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        ).returncode == 0
        if not exists:
            deleted_paths.append(repository_path)
            continue
        data = bytes(git("show", f"{tip}:{repository_path}", binary=True))
        file_path = files_dir / repository_path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_bytes(data)
        file_records[repository_path] = {
            "bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest(),
        }

    metadata = {
        "name": name,
        "tip": tip,
        "merge_base": merge_base,
        "main_at_original_archive": main_baseline,
        "changed_files_from_merge_base": changed,
        "deleted_paths": deleted_paths,
        "files": file_records,
    }
    write_json(destination / "metadata.json", metadata)
    return metadata


def recover_legacy(recovery_head: str, force: bool) -> None:
    manifest = json.loads(LEGACY_MANIFEST.read_text(encoding="utf-8"))
    output = ROOT / manifest["archive"]
    if output.exists() and not force:
        raise FileExistsError(f"refusing to overwrite {output}; use --force")

    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary) / "research-1902-1903-courier"
        metadata = capture_branch(
            root.parent,
            "research-1902-1903-courier",
            manifest["branch_sha"],
            manifest["main_baseline"],
        )
        branch_root = root
        write_text(branch_root / "BRANCH_SHA.txt", manifest["branch_sha"])
        write_text(branch_root / "MAIN_BASELINE_SHA.txt", manifest["main_baseline"])
        write_text(branch_root / "MERGE_BASE_SHA.txt", metadata["merge_base"])
        deterministic_tar(branch_root, output)

    manifest["merge_base"] = metadata["merge_base"]
    manifest["changed_files"] = metadata["changed_files_from_merge_base"]
    manifest.setdefault("original_recorded_archive_sha256", manifest["archive_sha256"])
    manifest["archive_sha256"] = sha256(output)
    manifest["archive_bytes"] = output.stat().st_size
    manifest["recovered_on"] = RECOVERY_DATE
    manifest["recovery_head"] = recovery_head
    manifest["recovery_note"] = (
        "Original ignored tarball was absent; deterministically rebuilt from the recorded "
        "branch SHA and historical main baseline."
    )
    write_json(LEGACY_MANIFEST, manifest)


def recover_all_branches(recovery_head: str, force: bool) -> None:
    manifest = json.loads(ALL_BRANCHES_MANIFEST.read_text(encoding="utf-8"))
    stored_files = manifest.get("stored_files", [])
    if len(stored_files) != 1:
        raise ValueError("recovery expects the recorded single-file archive layout")
    output = ROOT / stored_files[0]["path"]
    if output.exists() and not force:
        raise FileExistsError(f"refusing to overwrite {output}; use --force")

    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary) / "all-non-main-branch-refs-2026-09-01"
        root.mkdir()
        recovered = []
        for branch in manifest["branches"]:
            metadata = capture_branch(
                root,
                branch["name"],
                branch["tip"],
                manifest["main_at_archive"],
            )
            recovered.append(metadata)
        write_json(
            root / "manifest.json",
            {
                "recovered_on": RECOVERY_DATE,
                "recovery_head": recovery_head,
                "main_at_original_archive": manifest["main_at_archive"],
                "source_manifest": ALL_BRANCHES_MANIFEST.relative_to(ROOT).as_posix(),
                "branches": recovered,
            },
        )
        write_text(
            root / "README.md",
            "# Recovered non-main branch-ref archive\n\n"
            "This archive was rebuilt from the branch tip IDs preserved in the repository's "
            "2026-09-01 manifest after the original tarball was found missing. Each branch "
            "directory contains metadata, a branch-only commit log, a binary Git diff, and "
            "the tip version of every path changed from its merge base.",
        )
        deterministic_tar(root, output)

    digest = sha256(output)
    size = output.stat().st_size
    manifest.setdefault("original_recorded_logical_archive_sha256", manifest["logical_archive_sha256"])
    manifest.setdefault("original_recorded_logical_archive_bytes", manifest["logical_archive_bytes"])
    manifest["logical_archive_sha256"] = digest
    manifest["logical_archive_bytes"] = size
    manifest["stored_files"] = [
        {"path": output.relative_to(ROOT).as_posix(), "bytes": size, "sha256": digest}
    ]
    manifest["recovered_on"] = RECOVERY_DATE
    manifest["recovery_head"] = recovery_head
    manifest["recovery_note"] = (
        "Original ignored tarball was absent; deterministically rebuilt from the 24 recorded "
        "branch names/tips and historical main baseline."
    )
    write_json(ALL_BRANCHES_MANIFEST, manifest)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true", help="overwrite recovered archives")
    args = parser.parse_args()
    recovery_head = str(git("rev-parse", "HEAD"))
    recover_legacy(recovery_head, args.force)
    recover_all_branches(recovery_head, args.force)
    print(f"recovered {LEGACY_MANIFEST.name}")
    print(f"recovered {ALL_BRANCHES_MANIFEST.name}")


if __name__ == "__main__":
    main()
