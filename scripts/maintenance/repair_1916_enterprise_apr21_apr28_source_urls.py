from pathlib import Path
p=Path('database/sources.yml')
t=p.read_text()
for sid,date in [('S-332','1916-04-21'),('S-333','1916-04-28')]:
    marker=f'  - id: {sid}\n    name:'
    if marker not in t:
        raise SystemExit(f'{sid} missing after integration')
    block_start=t.index(f'  - id: {sid}\n')
    next_start=t.find('\n  - id:', block_start+1)
    if next_start < 0: next_start=len(t)
    block=t[block_start:next_start]
    if '\n    url:' not in block:
        needle='\n    type:'
        block=block.replace(needle,f'\n    url: "https://oregonnews.uoregon.edu/lccn/sn00063700/{date}/ed-1/"'+needle,1)
        t=t[:block_start]+block+t[next_start:]
p.write_text(t)
