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

### Tier 3 — Structural metadata and accuracy rules

- Every `E-###` block in `evidence-register.md` must include `Type:` and `Confidence:`
- Every `evidence.yml` entry must include `type`, `confidence`, and `claims`
- Mitch Young / 505 handling: structured files must not label his confirmed period as The Wheel without `BUS-009` / 505 Main Street business context

```bash
pip install -r requirements.txt
python scripts/validate_archive.py
```

Exit code 0 = pass; 1 = errors found.
