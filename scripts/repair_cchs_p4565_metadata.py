from pathlib import Path

p = Path("database/evidence.yml")
s = p.read_text(encoding="utf-8")
name = 'Circa mid-1960s photograph documents 503/505 and neighboring Main Street businesses'
needle = f'    name: "{name}"\n'
replacement = needle + '    type: Primary photographic evidence with institutional catalog metadata\n'

if needle in s:
    start = s.index(needle)
    tail = s[start:start + 500]
    if '\n    type:' not in tail:
        s = s.replace(needle, replacement, 1)

p.write_text(s, encoding="utf-8")
