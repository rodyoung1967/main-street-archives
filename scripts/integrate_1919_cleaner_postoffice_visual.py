#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


def write(rel, text):
    (ROOT / rel).write_text(text, encoding="utf-8")


def append_raw(rel, marker, block):
    text = read(rel)
    if marker in text:
        return
    write(rel, text.rstrip() + "\n\n" + block.rstrip() + "\n")


def replace_once(rel, old, new):
    text = read(rel)
    if new in text:
        return
    n = text.count(old)
    if n != 1:
        raise RuntimeError(f"Expected one anchor in {rel}, found {n}: {old[:100]!r}")
    write(rel, text.replace(old, new, 1))


capture = '''# 1 Aug 1919 — unnamed cleaner/dyer two doors south of new Post Office

Status: **VISUALLY VERIFIED PRIMARY NEWSPAPER PAGE; exact address normalization and advertiser identity unresolved**

## Source

**Oregon City Enterprise, 1 Aug 1919, p. 7**

Canonical page:
https://oregonnews.uoregon.edu/lccn/sn00063700/1919-08-01/ed-1/seq-7.pdf

Repository PDF:
`newspapers/oregon-city-enterprise/1919-08-01-page-7.pdf`

SHA-256:
`2ab8bf63876373495ed91a42a6cbaf28f35da99a2313cd99439ffd8517758923`

Source/evidence: `S-151` / `E-136`.

The original full page was downloaded from Historic Oregon Newspapers, rendered at high resolution, and directly inspected on 31 August 2026.

## Exact visually verified advertisement

The classified is a separate item, divided from the Theroux Music House advertisement above it. It reads:

> **Clothes cleaned, pressed and dyed.**  
> **500 Fifth and Main streets, two doors south of new post office. Phone 260 — Adv.**

The printed **500** is genuine page text and is **not an OCR hallucination**. The advertisement itself does **not** print a business or proprietor name.

## Safe facts

The page directly establishes that on 1 August 1919:

- an unnamed concern offered clothes cleaning, pressing and dyeing;
- its printed location line began **`500 Fifth and Main streets`**;
- it described itself as **two doors south of the new post office**;
- it used **Phone 260**.

The phrase **new post office** is consistent with the independently documented September 1918 relocation of Oregon City's Post Office into an M. D. Latourette-owned building on the east side of Main between Fifth and Sixth.

## Address-normalization limit

Do **not** silently normalize the printed wording to either **500 Main** or **500 Fifth**. The historical ad's syntax is unusual, and the archive has not yet recovered a directory, repeat advertisement, phone listing, lease, or other source that explains how the advertiser intended the `500 Fifth and Main streets` line to be read.

There is a strong reason to test **500 Main** as a hypothesis: a visually verified 24 October 1918 business guide separately places **Pantorium Cleaners at 500 Main**. But that earlier Pantorium listing uses **Phone 185-J**, not 260, and the 1919 ad gives no business name. The two records therefore remain separate evidence streams.

## Post Office spatial hypothesis — not yet evidence

The post-1918 Post Office is strongly constrained to some bay in the later City inventory's **504–514 Main** Latourette-David-Barlow range. If two further propositions were eventually proved—(1) the 1919 `500` means **500 Main**, and (2) `two doors south` counts adjacent Main Street storefronts literally—the ad could help identify the Post Office's exact bay near the south end of that range.

Those propositions are **not yet proved**. No exact Post Office number is assigned from this ad.

## Relationship to cleaner/dyer chronology

Separate verified evidence currently establishes:

- Oregon City Dye Works — 319 Main in March 1912;
- Pantorium — 416 Main in February 1914;
- Pantorium Cleaners — **500 Main, Phone 185-J**, October 1918 (`E-124` / `S-138`);
- this **unnamed** cleaner/dyer — printed `500 Fifth and Main streets`, Phone 260, August 1919 (`E-136` / `S-151`);
- Pantorium active in the cleaning/dyeing trade in January 1922;
- Pantorium at 519 Main immediately after the July 1922 fire.

No identity, ownership, relocation, or succession bridge is inferred between the 1918 Pantorium and the 1919 unnamed advertiser.

## Next checks

1. Search repeat 1919–1920 advertisements for **Phone 260** and the exact cleaning/pressing/dyeing wording.
2. Locate a 1919 telephone or city directory identifying Phone 260.
3. Determine whether the printed location normalizes to **500 Main**, **500 Fifth**, or another period convention.
4. Identify the exact 1918–1922 Post Office bay within 504–514 Main.
5. Only then use `two doors south` as an exact storefront-counting constraint.
'''
write("evidence/source-captures/1919-cleaning-dyeing-two-doors-south-new-post-office-ocr-lead.md", capture)

append_raw(
    "evidence/source-register.md",
    "## S-151 — Oregon City Enterprise, 1 August 1919, page 7 cleaner/dyer classified",
    '''## S-151 — Oregon City Enterprise, 1 August 1919, page 7 cleaner/dyer classified
Type: Primary newspaper scan; **VISUALLY VERIFIED** 31 August 2026.
Canonical PDF: https://oregonnews.uoregon.edu/lccn/sn00063700/1919-08-01/ed-1/seq-7.pdf
Repository PDF: `newspapers/oregon-city-enterprise/1919-08-01-page-7.pdf`.
SHA-256: `2ab8bf63876373495ed91a42a6cbaf28f35da99a2313cd99439ffd8517758923`.
Related evidence: `E-136`.
Repository source capture: `evidence/source-captures/1919-cleaning-dyeing-two-doors-south-new-post-office-ocr-lead.md`.
Notes: A separate classified directly prints **“Clothes cleaned, pressed and dyed. 500 Fifth and Main streets, two doors south of new post office. Phone 260”**. The printed `500` is visually confirmed, but the unusual location wording is not normalized to 500 Main or 500 Fifth. No advertiser/business name is printed. Do not merge with Pantorium solely from trade or proximity.'''
)

append_raw(
    "database/sources.yml",
    "  - id: S-151\n",
    '''  - id: S-151
    name: Oregon City Enterprise, 1 August 1919, page 7 cleaner/dyer classified
    url: https://oregonnews.uoregon.edu/lccn/sn00063700/1919-08-01/ed-1/seq-7.pdf
    notes: Primary newspaper scan visually verified 31 August 2026. Classified prints clothes cleaning/pressing/dyeing, the unusual location wording `500 Fifth and Main streets`, `two doors south of new post office`, and Phone 260. No business name is printed; do not normalize the address or merge with Pantorium without an independent bridge. Related evidence E-136.'''
)

append_raw(
    "evidence/evidence-register.md",
    "## E-136 — 1919 cleaner/dyer two doors south of new Post Office",
    '''## E-136 — 1919 cleaner/dyer two doors south of new Post Office
Type: Primary newspaper business-use and relative-location evidence; **direct visual inspection**.
Source: `S-151`.
Repository source capture: `evidence/source-captures/1919-cleaning-dyeing-two-doors-south-new-post-office-ocr-lead.md`.
Claims:
- The 1 August 1919 *Oregon City Enterprise* prints a separate classified reading **“Clothes cleaned, pressed and dyed. 500 Fifth and Main streets, two doors south of new post office. Phone 260.”**
- Direct scan review confirms that **500** is genuinely printed; it is not an OCR artifact.
- The ad prints no business/proprietor name, and its unusual `500 Fifth and Main streets` wording is not yet safely normalizable to 500 Main or 500 Fifth.
- `two doors south of new post office` independently supplies a relative spatial relationship to the post-September-1918 Oregon City Post Office.
- The 1918 Pantorium record at 500 Main (`E-124`) uses Phone 185-J, while this unnamed 1919 advertiser uses Phone 260. No identity, move, ownership, succession, or uninterrupted occupancy is inferred.
- If future evidence proves the 1919 number means 500 Main and confirms literal storefront door counting, the phrase may constrain the exact Post Office bay within the 504–514 Main Latourette-David-Barlow range; that is a working spatial hypothesis only.
Confidence: **Very High** for the visible wording, date, trade, relative-location phrase and phone number; **unresolved** for normalized exact address, advertiser identity, relationship to Pantorium, and exact Post Office bay.'''
)

append_raw(
    "database/evidence.yml",
    "  - id: E-136\n",
    '''  - id: E-136
    name: 1919 cleaner/dyer two doors south of new Post Office
    type: Primary newspaper business-use and relative-location evidence; direct visual inspection
    claims:
      - The 1 August 1919 Oregon City Enterprise prints a classified for clothes cleaning, pressing and dyeing with the location wording `500 Fifth and Main streets`, `two doors south of new post office`, and Phone 260.
      - Direct scan review confirms that 500 is genuinely printed and not an OCR artifact.
      - The ad prints no business or proprietor name; the unusual location wording is not yet normalized to 500 Main or 500 Fifth.
      - The relative-location phrase independently connects the premises spatially to the post-September-1918 Oregon City Post Office.
      - The 1918 Pantorium record at 500 Main uses Phone 185-J; no identity or succession with the unnamed 1919 advertiser is inferred.
      - A future 500-Main normalization plus literal storefront door count could constrain the Post Office bay, but that remains a hypothesis.
    confidence: Very High for visible wording, date, trade, relative location and phone; unresolved for exact normalized address, advertiser identity, Pantorium relationship and exact Post Office bay.
    related_sources: [S-151]
    related_evidence: [E-124]
    repository_file: evidence/source-captures/1919-cleaning-dyeing-two-doors-south-new-post-office-ocr-lead.md'''
)

# Add the new 1919 anchor to the established Post Office reconstruction.
post_rel = "evidence/source-captures/1918-1922-post-office-east-main-fifth-sixth-anchor.md"
post = read(post_rel)
anchor = "## 8 June 1922 — two visually verified spatial anchors\n"
section = '''## 1 August 1919 — unnamed cleaner/dyer two doors south of the new Post Office

The actual **Oregon City Enterprise, 1 Aug 1919, p. 7** scan has now been visually inspected (`S-151` / `E-136`). A separate classified directly prints:

- **Clothes cleaned, pressed and dyed**;
- **`500 Fifth and Main streets`**;
- **`two doors south of new post office`**;
- **Phone 260**.

The printed `500` is genuine, but the unusual location wording is **not** normalized to 500 Main or 500 Fifth. The advertiser is unnamed. A 1918 Pantorium listing at 500 Main uses a different phone number (185-J), so no identity bridge is assumed.

Spatially, this confirms that by August 1919 the relocated post-1918 office was locally described as the **new post office** and that an active cleaning/dyeing premises stood two doors south of it. If future evidence proves that the 1919 line means 500 Main and that `two doors` counts adjacent Main storefronts literally, it may help identify the exact postal bay within 504–514. Until then, the exact Post Office number remains unresolved.

'''
if "## 1 August 1919 — unnamed cleaner/dyer" not in post:
    if anchor not in post:
        raise RuntimeError("Post Office insertion anchor missing")
    write(post_rel, post.replace(anchor, section + anchor, 1))

# Update the main 1919-1920 checkpoint from pending to completed visual review.
cp_rel = "evidence/source-captures/1919-1920-501-503-505-construction-checkpoint.md"
cp = read(cp_rel)
old = "5. Visually resolve the **1 August 1919 Enterprise page 7** cleaner/dyer advertisement currently preserved as an OCR-only lead; its “two doors south of new post office” wording may sharpen storefront geometry, but the advertiser and exact address remain unproved until the scan is read."
new = "5. **Completed visual check:** the **1 August 1919 Enterprise page 7** cleaner/dyer ad genuinely prints `500 Fifth and Main streets`, `two doors south of new post office`, and Phone 260 (`E-136` / `S-151`). Next identify Phone 260 and normalize the unusual location wording before using it as an exact storefront constraint."
if old in cp:
    write(cp_rel, cp.replace(old, new, 1))
elif new not in cp:
    raise RuntimeError("Checkpoint cleaner anchor missing")

append_raw(
    "registers/research-log.md",
    "### 2026-08-31 — 1 August 1919 cleaner/new-Post-Office scan verified",
    '''### 2026-08-31 — 1 August 1919 cleaner/new-Post-Office scan verified
- Preserved original *Oregon City Enterprise*, 1 Aug 1919 p. 7 PDF under `newspapers/oregon-city-enterprise/` and directly inspected a high-resolution render.
- Promoted the former OCR-only lead to `S-151` / `E-136`: the classified genuinely prints **`500 Fifth and Main streets, two doors south of new post office. Phone 260`**.
- No business name is printed. The number is not normalized to 500 Main or 500 Fifth, and the advertiser is not merged with 1918 Pantorium (500 Main / Phone 185-J).
- Added the verified relative-location anchor to the 1918–1922 Post Office reconstruction. Exact postal bay and advertiser identity remain open.'''
)

print("Prepared 1919 cleaner/Post Office visual integration")
