from pathlib import Path
import runpy

checkpoint = Path("evidence/source-captures/1916-online-audit-checkpoint.md")
s = checkpoint.read_text()
old_combined = "- Combined: **667/884 certified**"
old_remaining = "- Enterprise pages remaining uncertified: **217**"
if old_combined not in s or old_remaining not in s:
    raise SystemExit("checkpoint normalization anchors missing")
s = s.replace(old_combined, "Combined certified newspaper coverage: **667/884**", 1)
s = s.replace(old_remaining, "**217 Enterprise pages remain uncertified**", 1)
checkpoint.write_text(s)

runpy.run_path("scripts/integrate_1916_enterprise_june30_july07.py", run_name="__main__")

s = checkpoint.read_text()
s = s.replace("Combined certified newspaper coverage: **683/884**", "- Combined: **683/884 certified**", 1)
s = s.replace("**201 Enterprise pages remain uncertified**", "- Enterprise pages remaining uncertified: **201**", 1)
checkpoint.write_text(s)
