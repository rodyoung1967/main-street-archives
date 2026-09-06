from pathlib import Path
import re

p = Path('scripts/integrate_cchs_2008_008_005_002_1896_6th_main.py')
text = p.read_text(encoding='utf-8')
pattern = re.compile(
    r"def yaml_add_list_item\(path, entity_id, field, item\):\n.*?\n\n# Exact-object idempotency",
    re.S,
)
new_func = '''def yaml_add_list_item(path, entity_id, field, item):
    text = rd(path)
    m = re.search(rf"(?m)^  - id: {re.escape(entity_id)}\\s*$", text)
    if not m:
        return
    n = re.search(r"(?m)^  - id: ", text[m.end():])
    end = m.end() + n.start() if n else len(text)
    section = text[m.start():end]

    inline = re.search(rf"(?m)^    {re.escape(field)}:\\s*\\[(.*?)\\]\\s*$", section)
    if inline:
        items = [x.strip() for x in inline.group(1).split(',') if x.strip()]
        if item in items:
            return
        items.append(item)
        replacement = f"    {field}: [{', '.join(items)}]"
        a = m.start() + inline.start()
        b = m.start() + inline.end()
        wr(path, text[:a] + replacement + text[b:])
        return

    block = re.search(rf"(?m)^    {re.escape(field)}:\\s*$", section)
    if block:
        field_start = m.start() + block.end()
        after = text[field_start:end]
        nf = re.search(r"(?m)^    [A-Za-z0-9_]+:", after)
        insert_at = field_start + (nf.start() if nf else len(after))
        existing_field_text = text[field_start:insert_at]
        if re.search(rf"(?m)^      - {re.escape(item)}\\s*$", existing_field_text):
            return
        text = text[:insert_at].rstrip("\\n") + f"\\n      - {item}\\n" + text[insert_at:].lstrip("\\n")
        wr(path, text)
        return

    insert_at = end
    text = text[:insert_at].rstrip("\\n") + f"\\n    {field}: [{item}]\\n\\n" + text[insert_at:].lstrip("\\n")
    wr(path, text)
'''
replacement = new_func + '\n\n# Exact-object idempotency'
new_text, count = pattern.subn(replacement, text, count=1)
if count != 1:
    if 'inline = re.search' in text:
        print('yaml helper already patched')
        raise SystemExit(0)
    raise SystemExit(f'Expected to patch one yaml_add_list_item helper, patched {count}')
p.write_text(new_text, encoding='utf-8')
print('patched yaml_add_list_item helper')
