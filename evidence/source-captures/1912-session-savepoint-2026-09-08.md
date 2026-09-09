# 1912 Session Savepoint — 8 September 2026

Purpose: preserve all 1912 research knowledge from the current session before any later rebase/integration against the rapidly advancing `main` branch.

## Durable research files already created

- `evidence/E-089-1912-smith-pool-room-503-main.md`
- `evidence/E-090-1912-main-street-demolition-rebuilding.md`
- `evidence/E-091-1912-gambrinus-saloon-sixth-main.md`
- `evidence/E-092-1912-main-address-ladder-young-harding.md`
- `evidence/E-093-1912-schrader-main-street-bakery-sale.md`
- `evidence/source-captures/1912-main-street-research.md`

## High-confidence 1912 findings

1. **5 January 1912 address ladder, visually verified from the Courier page image:**
   - H. N. Smith — pool room — **503 Main Street** (OCR incorrectly reads 603).
   - G. H. Young — **507 Main Street**.
   - H. P. Brightbill — **509 Main Street** (OCR incorrectly reads 609).
   - Geo. A. Harding — **511 Main Street** (OCR garbles the number; visual page reads 511).
2. **503 Main pool-hall sequence:** 24 March Morning Enterprise notice signed **H. H. Smith** applies for a pool-hall license at his place of business, **503 Main Street**; 12 July Courier says H. H. Smith, who had conducted a pool hall at Fifth and Main, left for Aurora. Preserve the **H. N. vs H. H. initials conflict**; do not silently merge without further evidence.
3. **Gambrinus Saloon at Sixth & Main:** 24 March Morning Enterprise identifies the Gambrinus Saloon at Sixth and Main and names **William Trudell** as proprietor.
4. **Confirmed Main Street demolition/rebuilding in May 1912:** 10 May Courier states Oregon City was tearing down buildings on Main Street and building new buildings in their places. The article does **not** identify a block, owner, business, or address. Do not assign this event to 501/503/505/507 without further evidence.
5. **Schrader bakery business transfer:** 20 December Courier reports Herman Schrader sold two bakeries, including the Main Street bakery, to **Wemmo & Haas**. Exact Main Street number remains unresolved.
6. **Harding / Willamette implication:** G. H. Young at 507 on 5 January 1912 strengthens, but does not prove, the hypothesis that the Willamette Building he entered one door north in March 1911 corresponded to 507 Main. Do not backdate 507 without continuity evidence.
7. **Geo. A. Harding at 511 Main** on the same 5 January page reinforces that Harding's business address and the separately named Harding Building must be reconstructed independently.

## Target-address research status for 1912

- **501 Main:** no exact 1912 occupant recovered in the current pass.
- **503 Main:** positive exact use/occupancy — Smith pool room/pool hall.
- **505 Main:** no exact-number 1912 occupant recovered in the current pass. Chicago Store appears on 5 January only as `Main St. just below Postoffice`; its 1911 505 address is not automatically carried forward.
- **507 Main:** G. H. Young on 5 January.
- **509 Main:** H. P. Brightbill on 5 January.
- **511 Main:** Geo. A. Harding on 5 January.

Missing exact listings are research-status findings only, not evidence of vacancy.

## Construction / fire / demolition handling

- No direct 1912 source recovered in this pass reports a fire at a premises identified as 501, 503, 505, or 507 Main.
- The May 1912 Main Street demolition/rebuilding statement is real and highly relevant to the predecessor-building question but remains geographically unresolved.
- Exact 1912 address occupancy proves use of numbered addresses, not survival of the present 503/505 buildings.

## Courier page-review status

The annual issue/page-review protocol was used alongside targeted search. Accessible/indexed pages materially helped recover the January address ladder and the May demolition statement. Some 1912 page images are not exposed/retrievable through the current interface and are **not** counted as visually reviewed.

Pending follow-ups to preserve:
- **RL-036** — complete visual review of 1912 Courier pages not exposed by the current interface.
- **RL-037** — resolve whether H. N. Smith and H. H. Smith at/near 503 Main are the same person or separate people / newspaper-initial error.
- **RL-038** — identify the specific Main Street buildings being torn down/replaced in the May 1912 editorial and test whether any were in the Fifth–Sixth block.

## Repository synchronization warning

At this savepoint, `research/1912-main-street` was reconstructed from commit `e195e44d2812fec580960c7cab1dac9495f49f83` after its branch ref temporarily disappeared. The research files and consolidated source capture were verified intact.

Current `main` has advanced substantially through parallel project workflows and must be treated as authoritative. A compare immediately before this savepoint reported the 1912 branch as **8 commits ahead and 1323 commits behind** current `main`, with merge base `23664acf5edeeba1a9430ac0af270702a27247fb` and then-current main SHA `46921db51fa5ce7988585dc8c34d49fe2061da21`.

**Do not merge or force-update this 1912 branch without first synchronizing/rebasing carefully against the latest `main` and preserving all newer repository work.**

## Master-file integration state

Already updated on the 1912 branch before this savepoint:
- `evidence/source-register.md` — 1912 source entries added.
- `timeline.md` — 1912 chronology expanded.

Still requires careful reconciliation against the latest `main` before final 1912 closeout:
- master `evidence/evidence-register.md` entries for E-089–E-093;
- `evidence/research-leads.md` entries RL-036–RL-038 and any 1912 updates to existing Harding/Willamette leads;
- `maps/sanborn-comparison-503-505-507.md` 1912 implications;
- validation and PR audit after synchronization.

This file is the authoritative savepoint for the session state if later branch integration becomes complicated.