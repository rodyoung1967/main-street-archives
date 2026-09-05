from pathlib import Path

replacements = {
    "database/sources.yml": [
        (
            'name: "CCHS P-1032 — Oregon City from bluff, 1936–1939"',
            'name: "CCHS P-1032, Oregon City from bluff, 1936–1939"',
        )
    ],
    "database/evidence.yml": [
        (
            'name: "1936-1939 bluff photograph provides dated lower-Oregon-City context but no secure 503/505 sign reading"',
            'name: "1936–1939 bluff photograph provides dated lower-Oregon-City context but no secure 503/505 sign reading"',
        )
    ],
}

for filename, pairs in replacements.items():
    path = Path(filename)
    text = path.read_text(encoding="utf-8")
    for old, new in pairs:
        text = text.replace(old, new)
    path.write_text(text, encoding="utf-8")

print("Synchronized P-1032 Markdown/YAML names")
