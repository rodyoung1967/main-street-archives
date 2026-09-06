from pathlib import Path

SOURCE = Path("scripts/integrate_708_monroe_canonical_sync.py")
src = SOURCE.read_text(encoding="utf-8")

# Allocate IDs from YAML entity lists rather than broad Markdown text, which can
# contain external catalog IDs such as CCHS P-9379 that are not archive people.
src = src.replace(
    's0 = next_num("evidence/source-register.md", "S")\ne0 = next_num("evidence/evidence-register.md", "E")\np0 = next_num("people/people-index.md", "P")\nb0 = next_num("database/buildings.yml", "B")',
    's0 = next_num("database/sources.yml", "S")\ne0 = next_num("database/evidence.yml", "E")\np0 = next_num("database/people.yml", "P")\nb0 = next_num("database/buildings.yml", "B")'
)

# The generic ID scanner still sees related IDs in YAML. Restrict it to actual
# list-item ID declarations before executing the integration.
old_func = '''def next_num(path, prefix):\n    text = read(path)\n    nums = [int(x) for x in re.findall(rf"\\b{re.escape(prefix)}-(\\d{{3,4}})\\b", text)]\n    return max(nums, default=0) + 1\n'''
new_func = '''def next_num(path, prefix):\n    text = read(path)\n    nums = [int(x) for x in re.findall(rf"(?m)^\\s*- id:\\s*{re.escape(prefix)}-(\\d{{3,4}})\\s*$", text)]\n    return max(nums, default=0) + 1\n'''
if old_func not in src:
    raise SystemExit("Expected next_num implementation not found")
src = src.replace(old_func, new_func, 1)

# HTML comments are valid in Markdown but invalid as top-level YAML lines.
src = src.replace(
    'MARKER = "<!-- 708-monroe-canonical-sync-2026-09-06 -->"',
    'MARKER = "<!-- 708-monroe-canonical-sync-2026-09-06 -->"\nYMARKER = "# 708-monroe-canonical-sync-2026-09-06"',
    1,
)
for name in ("source_yaml", "evidence_yaml", "people_yaml", "building_yaml"):
    src = src.replace(f"{name} = f'''{{MARKER}}", f"{name} = f'''{{YMARKER}}", 1)

src = src.replace('append_once("database/sources.yml", MARKER, source_yaml)', 'append_once("database/sources.yml", YMARKER, source_yaml)', 1)
src = src.replace('append_once("database/evidence.yml", MARKER, evidence_yaml)', 'append_once("database/evidence.yml", YMARKER, evidence_yaml)', 1)
src = src.replace('append_once("database/people.yml", MARKER, people_yaml)', 'append_once("database/people.yml", YMARKER, people_yaml)', 1)
src = src.replace('append_once("database/buildings.yml", MARKER, building_yaml)', 'append_once("database/buildings.yml", YMARKER, building_yaml)', 1)

exec(compile(src, str(SOURCE), "exec"), {"__name__": "__main__"})
