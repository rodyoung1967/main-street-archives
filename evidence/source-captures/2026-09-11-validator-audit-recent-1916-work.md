# Validator audit — recent 1916 work

Date: 11 September 2026
Workstream: ANNUAL-1916

## Existing validator

The repository already contains `scripts/validate_archive.py` and `.github/workflows/validate-archive.yml`.

The workflow is configured to run on every push to `main`, on pull requests, and by manual dispatch. It installs PyYAML and runs:

`python scripts/validate_archive.py`

The validator checks repository-wide consistency, including Markdown/YAML ID synchronization, cross-references, internal links, duplicate IDs, required evidence metadata, JSON parsing, year-status structure, repository-file targets, repository-history archive integrity, and project-specific accuracy rules.

## Recent 1916 commits covered by repository-wide validation

Because the workflow runs against the whole checked-out repository on every push to `main`, each later push re-validates all earlier retained work, not only the file changed in that commit. The recent 1916 sequence through 19 October therefore receives another full-repository validator invocation whenever the latest commits are pushed.

Recent work included:

- 21 September 1916 complete issue visual review and ledger update.
- 28 September 1916 complete issue visual review and ledger update.
- 12 October 1916 complete issue visual review and ledger update.
- 19 October 1916 complete issue visual review and ledger update.

## Independent rerun attempt

A fresh local clone followed by `python scripts/validate_archive.py` was attempted from the research environment on 11 September 2026. The clone could not start because that environment could not resolve `github.com`. This was an environment DNS/network failure, not a validator result.

Accordingly, do **not** record a local PASS or FAIL from that attempt. The GitHub Actions workflow remains the canonical automated validator route for these pushes.

## Current interpretation

- No replacement validator should be created; the existing validator is the project standard.
- New repository writes should continue to be made on current `main`, which automatically triggers repository-wide validation.
- If an Actions failure is observed, inspect the failing validator output and correct the repository rather than bypassing or weakening the checks.
