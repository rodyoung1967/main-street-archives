from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
ORIGINAL = ROOT / "scripts/integrate_1917_january_unsampled.py"

src = ORIGINAL.read_text(encoding="utf-8")

pattern = re.compile(
    r"    def add_inline\(block_text, key, values\):\n.*?(?=    block = add_inline\(block, \"related_businesses\")",
    re.S,
)
replacement = r'''    def add_inline(block_text, key, values):
        # Support both compact YAML lists (`key: [A, B]`) and the archive's
        # established multiline list style (`key:\n      - A`). Preserve the
        # existing representation instead of reserializing the whole file.
        inline_pat = re.compile(rf"(?m)^    {re.escape(key)}: \\[(.*?)\\]$")
        mm = inline_pat.search(block_text)
        if mm:
            items = [x.strip() for x in mm.group(1).split(",") if x.strip()]
            for value in values:
                if value not in items:
                    items.append(value)
            return block_text[:mm.start()] + f"    {key}: [{', '.join(items)}]" + block_text[mm.end():]

        multiline_pat = re.compile(
            rf"(?ms)^    {re.escape(key)}:\\n(?P<items>(?:      - [^\\n]+\\n)+)"
        )
        mm = multiline_pat.search(block_text)
        if not mm:
            raise SystemExit(f"B-016 {key} list not found in inline or multiline form")
        items_text = mm.group("items")
        existing = [
            line.strip()[2:].strip()
            for line in items_text.splitlines()
            if line.strip().startswith("- ")
        ]
        additions = ""
        for value in values:
            if value not in existing:
                additions += f"      - {value}\\n"
        return block_text[:mm.end("items")] + additions + block_text[mm.end("items"):]
'''

# Use a callable replacement so backslashes inside the injected Python source
# are preserved literally rather than interpreted by re.sub replacement rules.
patched, count = pattern.subn(lambda _m: replacement, src, count=1)
if count != 1:
    raise SystemExit("Could not patch add_inline helper in January integration script")

exec(compile(patched, str(ORIGINAL), "exec"), {"__name__": "__main__", "__file__": str(ORIGINAL)})
