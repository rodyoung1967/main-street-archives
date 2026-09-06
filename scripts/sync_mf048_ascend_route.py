from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel):
    return (ROOT / rel).read_text(encoding='utf-8')


def write(rel, text):
    (ROOT / rel).write_text(text, encoding='utf-8')


def replace_once(rel, old, new):
    text = read(rel)
    if new in text:
        return
    if old not in text:
        raise SystemExit(f'Expected anchor not found in {rel}')
    write(rel, text.replace(old, new, 1))


def append_once(rel, marker, block):
    text = read(rel)
    if marker in text:
        return
    write(rel, text.rstrip() + '\n\n' + block.rstrip() + '\n')

old_row = '| 18 | **MF-048** | Retrieve the **503 Main parcel-first ownership/deed-reference chain**, including the Wiitanen acquisition deed and conveyance out, with special attention to the reported **2 Dec. 2002 / $200,000** transaction | New 2010 assessment-derived evidence names Maurice Shahtout at 503 while the Wiitanens remain at 505, but the 2002 parties are hidden; deed proof is now the decisive bridge | **ACTIVE MANUAL — TWO-STAGE DRAFT READY**. [503 deed-chain draft](registers/research-requests/503-wiitanen-conveyance-deed-request-2026-09-05.md) |'
new_row = '| 18 | **MF-048** | Resolve the **503 Main parcel-first ownership/deed-reference chain**, including the Wiitanen acquisition deed and conveyance out, with special attention to the reported **2 Dec. 2002 / $200,000** transaction | Official Clackamas County **Ascend** can expose recording number, sale amount, grantor and grantee; target account `00572650` still requires interactive lookup. Use institutional outreach only if Ascend/history-card self-service does not resolve the chain | **ACTIVE — ASCEND SELF-SERVICE FIRST / FALLBACK DRAFT READY**. [Ascend route](evidence/source-captures/clackamas-ascend-503-sales-history-route-2026-09-05.md) · [503 deed-chain fallback draft](registers/research-requests/503-wiitanen-conveyance-deed-request-2026-09-05.md) |'
replace_once('MANUAL-FOLLOWUP.md', old_row, new_row)

replace_once(
    'MANUAL-FOLLOWUP.md',
    'The current practical list is the **17-item active queue in section 1**. Every immediate-action item that requires institutional outreach now has a **directly linked, ready-to-send recipient + subject + body**. The two `ACTIVE — COMBINE` request pairs also have finished linked correspondence. Several prior items remain merged, deferred, online-first, optional, or housekeeping. The new later-ownership work is concentrated in **MF-034** (parcel ownership sequence + deed proof) and **MF-047** (1983 survey owner snapshot).',
    'The current practical list is the **18-item active queue in section 1**. Every immediate-action item that requires institutional outreach has a **directly linked, ready-to-send recipient + subject + body**. The two `ACTIVE — COMBINE` request pairs also have finished linked correspondence. Several prior items remain merged, deferred, online-first, optional, or housekeeping. The later-ownership work is concentrated in **MF-034** (505 parcel ownership sequence + deed proof), **MF-047** (1983 505 survey owner snapshot), and **MF-048** (503 chain, now **Ascend self-service first** before fallback outreach).'
)

replace_once(
    'MANUAL-FOLLOWUP.md',
    '**ACTIVE MANUAL.** Retrieve the 503 Main parcel-first owner/deed-reference history and the actual deeds into and out of Dick/Sheila Wiitanen; test the reported 2 Dec. 2002 / $200,000 transaction without assuming its parties. Draft: `registers/research-requests/503-wiitanen-conveyance-deed-request-2026-09-05.md`. Keep separate from MF-034 (505).',
    '**ACTIVE — ASCEND SELF-SERVICE FIRST.** Search official Clackamas County Ascend by account **00572650** and preserve the target parcel Events/Sales History, especially recording number, deed type, grantor, grantee and sale amount for the reported 2 Dec. 2002 / $200,000 event. If Ascend does not expose the older chain, use the Assessment & Taxation history-card and Recording fallback draft at `registers/research-requests/503-wiitanen-conveyance-deed-request-2026-09-05.md`. Route capture: `evidence/source-captures/clackamas-ascend-503-sales-history-route-2026-09-05.md`. Keep separate from MF-034 (505).'
)

append_once(
    'registers/research-log.md',
    '## MF-048 Ascend self-service refinement — 5 September 2026',
    '''## MF-048 Ascend self-service refinement — 5 September 2026

- Confirmed Clackamas County's official Ascend system accepts an eight-digit account-number search and that indexed parcel pages expose **Events** and **Sales History** with recording number, sale amount, deed/transfer type, **grantor (seller)** and **grantee (buyer)**.
- The 503 target is account **00572650** / tax lot **2-2E-31AB-08200**. The available web-research interface could not submit the target account form or safely open an unobserved target query URL, so the actual 503 Sales History remains **uninspected** rather than a no-hit.
- Created `evidence/source-captures/clackamas-ascend-503-sales-history-route-2026-09-05.md` and revised `MF-048` so Ascend self-service is first; Assessment & Taxation history-card / Recording outreach is fallback after the recording number(s) are identified or if older history is omitted.
- No email, public-record request, paid search or deed-copy order was made.'''
)

print('Synchronized MF-048 with the official Ascend self-service route.')
