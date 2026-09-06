#!/usr/bin/env python3
from pathlib import Path

MARKER = "Albert Flor 1949 Oregon City control — 2026-09-06"
FILES = {
    "capture": Path("evidence/source-captures/albert-d-flor-morton-bridge-pass-2026-09-06.md"),
    "profile": Path("people/profiles/albert-d-flor-family.md"),
    "request": Path("registers/research-requests/morton-wheel-and-oregon-city-wheel-pre-raye-ownership-bridge-request-2026-09-05.md"),
    "manual": Path("MANUAL-FOLLOWUP.md"),
}

def append_once(path, text):
    cur = path.read_text(encoding="utf-8")
    if MARKER in cur:
        return
    path.write_text(cur.rstrip()+"\n\n"+text.strip()+"\n", encoding="utf-8")

def main():
    append_once(FILES["capture"], f'''## Earlier Oregon City control — November 1949
<!-- {MARKER} -->

A further backward search found **Albert D. Flor** in the official Oregon City Commission record for the **9 November 1949 adjourned regular meeting**, when the City Recorder's claims report for **October 1949** was approved. Searchable text in the claims list names `Albert D. Flor` among City payees/vendors; the same record also contains an `Albert Flor` entry in a jury-fee group.

Official source:
https://ormswd.synergydcs.com/HPRMWebDrawer/Record/4723898/File/document

The official PDF endpoint repeatedly timed out when opened for page-image inspection, so this is **OFFICIAL PRIMARY TEXT / VISUAL RENDER RETRIEVAL GAP**, not scan-certified. The searchable text does not identify a restaurant, Kwality Cafe, 503 Main, Margaret Remus, or the basis for the `Albert D. Flor` supply payment. Do not infer a business identity from the payee line alone, and do not assume the jury-fee `Albert Flor` is the same person solely from the similar name.

### Chronology consequence

This moves the exact-name **Albert D. Flor** Oregon City control back from the December 1951 liquor application to **November 1949**. If this is the same Albert D. Flor later associated with the 1951 Flor/Remus application and 1957 restaurant/cocktail-bar management at 503, any hypothesized earlier Morton residence/business role would have to accommodate his documented Oregon City activity by late 1949. This does not rule out a prior Morton connection.

Current evidence sequence is therefore:

- **9 Nov. 1949:** `Albert D. Flor` in Oregon City Commission October claims list — exact-name city presence/payee control; business/premises unknown.
- **5 Dec. 1951:** Albert D. Flor + Margaret Remus jointly approved liquor applicants — premises/trade name unknown.
- **Sept. 1953:** `Al & Marge Kwality Cafe` in City finance/vendor list — surnames/address absent.
- **1953:** Fred Remus identified by City historic survey as a cook at Kwality Cafe.
- **1957:** City historic-resource synthesis places Mr./Mrs. Albert D. Flor managing the restaurant/cocktail bar at 503 Main.

The Flor→Remus→Al & Marge→503 continuity remains a **strong cross-source hypothesis**, not a proved ownership chain.''')

    append_once(FILES["profile"], f'''## November 1949 Oregon City control
<!-- {MARKER} -->

Official Oregon City Commission searchable text for the **9 November 1949** meeting's October claims report includes the exact name **Albert D. Flor** among City payees/vendors. The underlying PDF timed out during visual retrieval, and the text does not identify his business, address, or reason beyond the claims-list context. Classification: **OFFICIAL PRIMARY TEXT / VISUAL RENDER RETRIEVAL GAP**.

This is now the earliest exact-name Oregon City control recovered for the later 503 operator, subject to identity confirmation across the 1949/1951/1957 records. It does not itself connect Flor to Kwality Cafe or 503 Main.''')

    append_once(FILES["request"], f'''## Supplemental date control — Albert D. Flor in Oregon City by November 1949
<!-- {MARKER} -->

Official Oregon City Commission searchable text places **Albert D. Flor** in the City's **October 1949 claims list approved 9 November 1949**, although the payee line does not identify his business/address. When testing a Morton connection for Flor, prioritize records **before November 1949** while still checking later records for travel, former-residence, transfer, or ownership references. Do not treat the 1949 payee entry as proof that Flor already operated Kwality Cafe or 503 Main.''')

    append_once(FILES["manual"], f'''### MF-052 Flor chronology refinement — November 1949 Oregon City control
<!-- {MARKER} -->

Official city text now places the exact name **Albert D. Flor** in Oregon City's October 1949 claims report approved **9 November 1949**. The business/premises are not named and the PDF could not be visually rendered. For the Morton side of MF-052, prioritize Flor searches before November 1949; for the Oregon side, continue seeking the missing record that connects the 1949 payee and 1951 Flor/Remus liquor application to Kwality Cafe / 503 Main.''')

if __name__ == "__main__":
    main()
