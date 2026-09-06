from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ORIGINAL = ROOT / "scripts/integrate_1917_march_15_29.py"
src = ORIGINAL.read_text(encoding="utf-8")

src = src.replace(
    'name: "Oregon City Courier 15/22/29 March 1917 complete-page visual-review batch"',
    'name: "Oregon City Courier, 15/22/29 March 1917 complete-page visual-review batch"',
    1,
)
src = src.replace(
    'name: "March 1917 continuation moves Jones Drug exact 617 Main anchor back to 15 March and clears 28 pages"',
    'name: "March 1917 continuation moves Jones Drug\'s exact 617 Main anchor back to 15 March and clears 28 pages"',
    1,
)

exec(compile(src, str(ORIGINAL), "exec"), {"__name__": "__main__", "__file__": str(ORIGINAL)})
