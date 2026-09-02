from pathlib import Path


def replace_once(path, old, new, marker):
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    if marker in text:
        return
    if old not in text:
        raise RuntimeError(f"Anchor not found in {path}: {old[:100]!r}")
    p.write_text(text.replace(old, new, 1), encoding="utf-8")


def append_once(path, marker, block):
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    if marker in text:
        return
    p.write_text(text.rstrip() + "\n\n" + block.strip() + "\n", encoding="utf-8")


replace_once(
    "evidence/source-register.md",
    "Notes: Official synthesis. Related evidence E-032.",
    "Notes: Official secondary synthesis. The City page explicitly says little historic information was found, describes the building as apparently constructed circa 1919, and attributes Wolf-family ownership from about 1922 to 1972 to research conducted during the 1983 survey. Treat c.1919 as an approximate historic-survey conclusion, not primary construction proof; the ownership span is survey-derived rather than deed proof on this page. Related evidence E-032.",
    "ownership span is survey-derived rather than deed proof on this page",
)

replace_once(
    "database/sources.yml",
    "    notes: Official synthesis. Related evidence E-032.",
    "    notes: Official secondary synthesis. The City page says little historic information was found, describes the building as apparently constructed circa 1919, and attributes Wolf-family ownership about 1922-1972 to research conducted during the 1983 survey. Treat c.1919 as an approximate survey conclusion rather than primary construction proof; related evidence E-032.",
    "attributes Wolf-family ownership about 1922-1972 to research conducted during the 1983 survey",
)

replace_once(
    "evidence/evidence-register.md",
    "Claims: City 503 record reports c.1919 construction estimate, Kwality Restaurant 1926, Kwality Cafe 1947, Flor 1957, Wolf-family ownership roughly 1922-1972.",
    "Claims: City 503 record explicitly says little historic information was found, describes the building as apparently constructed circa 1919, and reports Kwality Restaurant 1926, Kwality Cafe 1947, and Flor 1957. It attributes Wolf-family ownership roughly 1922-1972 to research conducted during the 1983 survey. The c.1919 wording is therefore an approximate historic-survey conclusion, not primary construction proof, and the Wolf span is not deed proof from this page.",
    "The c.1919 wording is therefore an approximate historic-survey conclusion",
)

replace_once(
    "evidence/evidence-register.md",
    "Confidence: Medium-high as official synthesis; underlying pages preferable.",
    "Confidence: High for what the City survey page reports and for its stated 1983-survey provenance; Low-to-Moderate for treating c.1919 as the literal construction year without primary construction records; underlying construction and title records remain preferable.",
    "Low-to-Moderate for treating c.1919 as the literal construction year",
)

replace_once(
    "database/evidence.yml",
    "      - City 503 record reports c.1919 construction estimate, Kwality chronology, Flor, and Wolf-family ownership roughly 1922-1972.",
    "      - City 503 record says little historic information was found and describes the building as apparently constructed circa 1919; this is an approximate historic-survey conclusion rather than primary construction proof.\n      - The same 503 page attributes Wolf-family ownership roughly 1922-1972 to research conducted during the 1983 survey; the page itself is not deed proof of that ownership span.",
    "the page itself is not deed proof of that ownership span",
)

replace_once(
    "database/evidence.yml",
    "    confidence: Medium-high as official synthesis; underlying pages preferable.",
    "    confidence: High for what the City survey pages report and their stated provenance; Low-to-Moderate for treating c.1919 as the literal 503 construction year without primary construction records; underlying construction and title records remain preferable.",
    "Low-to-Moderate for treating c.1919 as the literal 503 construction year",
)

replace_once(
    "buildings/503-main.md",
    "The 503 **c.1919** date is therefore no longer merely an indexed-text lead in this archive; it is **visually verified as the date assigned by the official City historic inventory**. It remains a historic-inventory estimate for the surviving building, not primary proof of the exact construction day/year and not evidence that Kwality opened in 1919.",
    "The 503 **c.1919** date is therefore no longer merely an indexed-text lead in this archive; it is **visually verified as the date assigned by the official City historic inventory**. It remains a historic-inventory estimate for the surviving building, not primary proof of the exact construction day/year and not evidence that Kwality opened in 1919. The legacy City resource page further qualifies its own conclusion: it says little historic information was found and describes the building as only **apparently** constructed circa 1919. The page also attributes the Wolf-family circa-1922-to-1972 ownership chronology to research conducted during the **1983 survey**. This makes c.1919 explicitly an approximate survey conclusion rather than a primary construction record.",
    "This makes c.1919 explicitly an approximate survey conclusion rather than a primary construction record",
)

replace_once(
    "database/buildings.yml",
    "Also includes c.1919 surviving-building estimate and 503/505 boundary questions.",
    "Also includes a c.1919 surviving-building estimate that the legacy City page explicitly qualifies as an apparent date reached despite little historic information, plus 503/505 boundary questions. The same City page attributes Wolf-family ownership about 1922-1972 to 1983 survey research rather than a cited deed on that page.",
    "an apparent date reached despite little historic information",
)

append_once(
    "evidence/source-captures/1919-1920-construction-occupancy-online-closeout-2026-09-01.md",
    "## 2 September 2026 — 503 historic-survey provenance clarification",
    """## 2 September 2026 — 503 historic-survey provenance clarification

A direct review of the registered City legacy page `S-026` clarifies the evidentiary weight of the often-repeated **c.1919** date for 503 Main. The page itself says that little historic information was found and characterizes the building as **apparently** constructed circa 1919. It separately attributes the Wolf-family ownership span of about 1922–1972 to research conducted during the **1983 survey**.

**Disposition:** no new source/evidence ID is created because this is a provenance clarification of existing `S-026` / `E-032`. The c.1919 date remains an official historic-survey estimate, but it is now explicitly treated as an approximate secondary conclusion rather than primary construction proof. The 1983-survey ownership statement remains a title lead, not deed proof. This clarification does not alter the established 1911→1925 footprint-change bracket or resolve whether the surviving 503 fabric dates to 1919, the 1922 fire/rebuild sequence, or another event within that interval.
""",
)

print("503 survey provenance clarification integrated")
