from pathlib import Path
import re


def read(path):
    return Path(path).read_text(encoding="utf-8")


def write(path, text):
    Path(path).write_text(text, encoding="utf-8")

# The media validator recognizes canonical media IDs from level-2 headings in the
# canonical photo metadata register. Normalize the P-6974 section created by the
# integration script without hard-coding the dynamically allocated IMG number.
p = "media/photo-metadata-register.md"
text = read(p)
text2 = re.sub(
    r"(?m)^### (IMG-\d{4}) — 1908 Friedrich's Hardware and Little's Confectionery, 510–512 7th Street$",
    r"## \1 — 1908 Friedrich's Hardware and Little's Confectionery, 510–512 7th Street",
    text,
)
if text2 == text:
    raise SystemExit("P-6974 media metadata heading was not found for normalization")
write(p, text2)

# Keep Markdown/YAML source display names identical.
p = "database/sources.yml"
text = read(p)
old = "name: CCHS P-6974 — Friedrich's Hardware and Little's Confectionery, 510–512 7th Street, 1908"
new = "name: CCHS P-6974, Friedrich's Hardware and Little's Confectionery, 510–512 7th Street, 1908"
if old not in text and new not in text:
    raise SystemExit("P-6974 source YAML name was not found")
write(p, text.replace(old, new))

# Keep the person index and YAML display name identical while preserving the
# separate 1908 identity record rather than merging it with any later Friedrich.
p = "database/people.yml"
text = read(p)
pattern = re.compile(
    r"(?m)^(  - id: P-\d+\n    name: )Richard Friedrichs(\n    role: Friedrich's Hardware cataloged subject, 1908)$"
)
if not pattern.search(text):
    if "name: Richard Friedrichs — 1908 CCHS identification\n    role: Friedrich's Hardware cataloged subject, 1908" not in text:
        raise SystemExit("P-6974 Richard Friedrichs YAML record was not found")
else:
    text = pattern.sub(r"\1Richard Friedrichs — 1908 CCHS identification\2", text)
write(p, text)

print("Normalized P-6974 media/source/person metadata for archive validation.")
