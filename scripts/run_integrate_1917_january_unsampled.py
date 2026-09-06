from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
target = ROOT / "scripts/integrate_1917_january_unsampled.py"
src = target.read_text(encoding="utf-8")

old = r'''    def add_inline(block_text, key, values):
        pat = re.compile(rf"(?m)^    {re.escape(key)}: \[(.*?)\]$")
        mm = pat.search(block_text)
        if not mm:
            raise SystemExit(f"B-016 {key} inline list not found")
        items = [x.strip() for x in mm.group(1).split(",") if x.strip()]
        for value in values:
            if value not in items:
                items.append(value)
        return block_text[:mm.start()] + f"    {key}: [{', '.join(items)}]" + block_text[mm.end():]
'''

new = r'''    def add_inline(block_text, key, values):
        # Preserve the file's existing style. Some older records use inline
        # lists; B-016 currently uses block sequences.
        inline = re.compile(rf"(?m)^    {re.escape(key)}: \[(.*?)\]$")
        mm = inline.search(block_text)
        if mm:
            items = [x.strip() for x in mm.group(1).split(",") if x.strip()]
            for value in values:
                if value not in items:
                    items.append(value)
            return block_text[:mm.start()] + f"    {key}: [{', '.join(items)}]" + block_text[mm.end():]

        sequence = re.compile(
            rf"(?m)^    {re.escape(key)}:\n(?P<items>(?:    - [^\n]+\n?)*)"
        )
        mm = sequence.search(block_text)
        if not mm:
            raise SystemExit(f"B-016 {key} list not found")
        existing = [
            line.strip()[2:].strip()
            for line in mm.group("items").splitlines()
            if line.strip().startswith("-")
        ]
        additions = [value for value in values if value not in existing]
        if not additions:
            return block_text
        replacement = mm.group(0).rstrip("\n") + "\n" + "\n".join(
            f"    - {value}" for value in additions
        )
        if mm.group(0).endswith("\n"):
            replacement += "\n"
        return block_text[:mm.start()] + replacement + block_text[mm.end():]
'''

if old not in src:
    raise SystemExit("expected add_inline implementation not found; stop rather than patch unknown script")

patched = src.replace(old, new, 1)

# Keep generated Markdown/YAML identity strings byte-for-byte consistent and
# satisfy the source schema's required URL field. The Jan. 25 p.6 landing page
# is the direct page supporting E-221; the batch manifest retains all 24 pages.
patched = patched.replace(
    'name: "Oregon City Courier 11/18/25 January 1917 complete-page visual-review batch"\n    type:',
    'name: "Oregon City Courier, 11/18/25 January 1917 complete-page visual-review batch"\n    url: "https://oregonnews.uoregon.edu/lccn/sn00063698/1917-01-25/ed-1/seq-6/"\n    type:',
    1,
)
patched = patched.replace(
    '# Strebig Meat Market — former 427 Main occupant named in 1917',
    '# Strebig Meat Market — former 427 occupant',
    1,
)
patched = patched.replace(
    'name: "Strebig Meat Market — former 427 Main occupant named in 1917"',
    'name: "Strebig Meat Market — former 427 occupant"',
    1,
)

for required in [
    'name: "Oregon City Courier, 11/18/25 January 1917 complete-page visual-review batch"',
    'url: "https://oregonnews.uoregon.edu/lccn/sn00063698/1917-01-25/ed-1/seq-6/"',
    '# Strebig Meat Market — former 427 occupant',
    'name: "Strebig Meat Market — former 427 occupant"',
]:
    if required not in patched:
        raise SystemExit(f"expected metadata patch missing: {required}")

code = compile(patched, str(target), "exec")
globals_dict = {"__name__": "__main__", "__file__": str(target)}
exec(code, globals_dict)
