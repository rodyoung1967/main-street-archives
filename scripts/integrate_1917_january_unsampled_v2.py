from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
ORIGINAL = ROOT / "scripts/integrate_1917_january_unsampled.py"

src = ORIGINAL.read_text(encoding="utf-8")

# Replace only the B-016 YAML synchronization section. The archive contains a
# mix of inline lists, indented block sequences, and older records where a
# relationship key is absent. Preserve whatever representation exists and add
# a missing key only inside B-016.
section_pat = re.compile(
    r"# Synchronize B-016's YAML lists and concise note without reserializing the file\.\n"
    r".*?"
    r"(?=# Update the canonical address-register row by address rather than positional assumptions\.)",
    re.S,
)
section_replacement = r'''# Synchronize B-016's YAML lists and concise note without reserializing the file.
buildings = read("database/buildings.yml")
m = re.search(r"(?ms)^  - id: B-016\n.*?(?=^  - id:|\Z)", buildings)
if not m:
    raise SystemExit("B-016 block not found in database/buildings.yml")
block = m.group(0)
if EVIDENCE_ID not in block:
    def ensure_values(block_text, key, values):
        # Inline list form: key: [A, B]
        inline_pat = re.compile(rf"(?m)^    {re.escape(key)}: \[(.*?)\]$")
        mm = inline_pat.search(block_text)
        if mm:
            items = [x.strip() for x in mm.group(1).split(",") if x.strip()]
            for value in values:
                if value not in items:
                    items.append(value)
            return block_text[:mm.start()] + f"    {key}: [{', '.join(items)}]" + block_text[mm.end():]

        # Standard indented sequence form used by database/buildings.yml.
        multi_pat = re.compile(
            rf"(?ms)^    {re.escape(key)}:\n(?P<items>(?:      - [^\n]+\n)+)"
        )
        mm = multi_pat.search(block_text)
        if mm:
            existing = [
                line.strip()[2:].strip()
                for line in mm.group("items").splitlines()
                if line.strip().startswith("- ")
            ]
            additions = "".join(
                f"      - {value}\n" for value in values if value not in existing
            )
            return block_text[:mm.end("items")] + additions + block_text[mm.end("items"):]

        # Some generated YAML uses an indentless block sequence at key level.
        indentless_pat = re.compile(
            rf"(?ms)^    {re.escape(key)}:\n(?P<items>(?:    - [^\n]+\n)+)"
        )
        mm = indentless_pat.search(block_text)
        if mm:
            existing = [
                line.strip()[2:].strip()
                for line in mm.group("items").splitlines()
                if line.strip().startswith("- ")
            ]
            additions = "".join(
                f"    - {value}\n" for value in values if value not in existing
            )
            return block_text[:mm.end("items")] + additions + block_text[mm.end("items"):]

        # Relationship key is genuinely absent: add it at the end of B-016.
        addition = f"    {key}:\n" + "".join(f"      - {value}\n" for value in values)
        if not block_text.endswith("\n"):
            block_text += "\n"
        return block_text + addition

    block = ensure_values(block, "related_businesses", [EDDY_BUSINESS_ID, STREBIG_1917_BUSINESS_ID])
    block = ensure_values(block, "related_evidence", [EVIDENCE_ID])
    block = ensure_values(block, "related_sources", [SOURCE_ID])
    block = re.sub(
        r"(?m)^    notes: (.*)$",
        lambda mm: "    notes: " + mm.group(1) + " Jan 25 1917 Courier directly fixes 427 Main as corner Fifth for W. B. Eddy's Store and names Strebig Meat Market as former building occupant; cross-period business identity and physical-building continuity remain unresolved.",
        block,
        count=1,
    )
    buildings = buildings[:m.start()] + block + buildings[m.end():]
    write("database/buildings.yml", buildings)

'''

patched, count = section_pat.subn(lambda _m: section_replacement, src, count=1)
if count != 1:
    raise SystemExit("Could not patch B-016 synchronization section")

exec(compile(patched, str(ORIGINAL), "exec"), {"__name__": "__main__", "__file__": str(ORIGINAL)})
