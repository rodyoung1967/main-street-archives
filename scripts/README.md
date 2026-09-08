# Archive Scripts

## validate_archive.py

Checks archive consistency across Markdown registers, YAML sidecar files, and cross-references.

### Tier 1 — ID sync (Markdown ↔ YAML)

- People, businesses, buildings, evidence, sources
- Oral history (`oral-history-index.md` ↔ `oral-history.yml`)
- Maps (`sanborn-map-register.md` ↔ `maps.yml`)
- Artifacts (`artifacts/matchbooks.md` ↔ `artifacts.yml`)
- Timeline (`timeline.yml`; narrative `timeline.md` has no `T-###` IDs — validated via cross-references only)

Markdown-only registers (OQ, RL, media, records) are included in reference checks but not required in YAML.

### Tier 2 — Reference integrity

- Unknown ID references in any `.md` file
- Orphan `related_*` cross-references in YAML
- Broken internal Markdown links
- Media catalog cross-references to evidence and sources
- Duplicate IDs in canonical registers or YAML
- Markdown/YAML name mismatches for people, businesses, evidence, and sources
- Missing YAML `repository_file` and `repository_files` targets
- Relationship-field type and duplicate enforcement (`related_sources` may contain only unique `S-###` IDs, etc.)
- Rejection of legacy `source`, `sources`, and `evidence` aliases in structured YAML

External collection identifiers must be explicitly namespaced so they are not mistaken for archive IDs. Current examples: `MOT:P-391` for a Museum of the Oregon Territory catalog item and `TEL:A-229` for a historic telephone identifier.

### Tier 3 — Structural metadata and accuracy rules

- Every `E-###` block in `evidence-register.md` must include `Type:` and `Confidence:`
- Every `evidence.yml` entry must include `type`, `confidence`, and `claims`
- `registers/year-status.md` must contain exactly one valid status row for each audited year, 1904–1918
- Mitch Young / 505 handling: structured files must not label his confirmed period as The Wheel without `BUS-009` / 505 Main Street business context
- Repository-history manifests must point to present, byte/hash-matching, readable tar archives
- Every committed JSON file must parse successfully

## recover_repository_history_archives.py

Rebuilds the two September 2026 repository-history tarballs from the branch-tip IDs and historical `main` baselines preserved in their manifests. It is a recovery utility for the `.gitignore` omission documented by the 8 September 2026 integrity audit, not a general branch-archive creator. The historical commits must exist in the local object database; the script does not fetch them.

```bash
python scripts/recover_repository_history_archives.py
```

Use `--force` only when intentionally regenerating the existing deterministic archives.

```bash
pip install -r requirements.txt
python scripts/validate_archive.py
```

Exit code 0 = pass; 1 = errors found.
