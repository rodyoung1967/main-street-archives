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

# 505 Main: clarify that the legacy City page explicitly supersedes the 1983 c.1908 survey date.
replace_once(
    "evidence/source-register.md",
    "Notes: Construction interpretation and directory entries. Related evidence E-032.",
    "Notes: Official secondary construction interpretation and directory synthesis. The page states that the 1983 survey indicated c.1908, but explicitly concludes from Sanborn-map comparison that the surviving building was constructed sometime between 1911 and 1925, perhaps about 1920. Thus c.1908 is a superseded survey date for the surviving building, while c.1920 remains tentative secondary interpretation rather than primary construction proof. Related evidence E-032.",
    "c.1908 is a superseded survey date for the surviving building",
)

replace_once(
    "database/sources.yml",
    "    notes: Construction interpretation and directory entries. Related evidence E-032.",
    "    notes: Official secondary construction interpretation and directory synthesis. The page says the 1983 survey indicated c.1908 but concludes from Sanborn-map comparison that the surviving building was constructed sometime between 1911 and 1925, perhaps about 1920. Treat c.1908 as superseded for the surviving building and c.1920 as tentative secondary interpretation, not primary construction proof. Related evidence E-032.",
    "Treat c.1908 as superseded for the surviving building",
)

replace_once(
    "evidence/evidence-register.md",
    "City 505 record reports no 1916 directory listing (not proof of vacancy), c.1920/1925 construction estimate, 1941 Dr. Roy Briggs at 505 1/2, 1945 \"Harr's Recreation Center,\" 1953 \"Well's Recreation.\"",
    "City 505 record says the 1983 survey indicated c.1908, but explicitly concludes from Sanborn-map comparison that the surviving building was constructed sometime between 1911 and 1925, perhaps about 1920. It also reports no 1916 directory listing (not proof of vacancy), 1941 Dr. Roy Briggs at 505 1/2, 1945 \"Harr's Recreation Center,\" and 1953 \"Well's Recreation.\" The c.1908 survey date is therefore superseded within the City's own later synthesis; c.1920 remains tentative secondary interpretation, not primary construction proof.",
    "The c.1908 survey date is therefore superseded within the City's own later synthesis",
)

replace_once(
    "database/evidence.yml",
    "      - City 505 record reports 1916 directory silence, c.1920/1925 construction estimate, 1941 Dr. Roy Briggs, 1945 Harr's Recreation Center, and 1953 Well's Recreation.",
    "      - City 505 record says the 1983 survey indicated c.1908, but concludes from Sanborn-map comparison that the surviving building was constructed sometime between 1911 and 1925, perhaps about 1920; c.1908 is therefore superseded within the City's own later synthesis and c.1920 remains tentative secondary interpretation rather than primary construction proof.\n      - The same 505 page reports 1916 directory silence, 1941 Dr. Roy Briggs, 1945 Harr's Recreation Center, and 1953 Well's Recreation; directory silence is not proof of vacancy.",
    "c.1908 is therefore superseded within the City's own later synthesis",
)

replace_once(
    "evidence/evidence-register.md",
    "Confidence: High for what the City survey page reports and for its stated 1983-survey provenance; Low-to-Moderate for treating c.1919 as the literal construction year without primary construction records; underlying construction and title records remain preferable.",
    "Confidence: High for what the City survey pages report, including the explicit 505 rejection of the 1983 c.1908 date and the 1911-1925 Sanborn-derived bracket; Low-to-Moderate for treating c.1919 at 503 or c.1920 at 505 as literal construction years without primary construction records; underlying construction and title records remain preferable.",
    "explicit 505 rejection of the 1983 c.1908 date",
)

replace_once(
    "database/evidence.yml",
    "    confidence: High for what the City survey pages report and their stated provenance; Low-to-Moderate for treating c.1919 as the literal 503 construction year without primary construction records; underlying construction and title records remain preferable.",
    "    confidence: High for what the City survey pages report, including the explicit 505 rejection of the 1983 c.1908 date and the 1911-1925 Sanborn-derived bracket; Low-to-Moderate for treating c.1919 at 503 or c.1920 at 505 as literal construction years without primary construction records; underlying construction and title records remain preferable.",
    "explicit 505 rejection of the 1983 c.1908 date",
)

replace_once(
    "buildings/505-main.md",
    "### 2000 City inventory — c.1920, now visually verified",
    """### Legacy City resource page — 1983 c.1908 date explicitly superseded

The registered City historic-resource page (`S-033`) preserves an important survey correction. It says the **1983 survey indicated c.1908**, but the later City synthesis rejects that date for the surviving building: using Sanborn-map comparison, it places construction **sometime between 1911 and 1925**, with **about 1920** offered only as a possibility.

This is official secondary evidence that **c.1908 should not be used as the construction date of the surviving 505 building**. It agrees with the project's independent visual conclusion that the pre-1925 address/business evidence must be separated from surviving-building fabric. The **1911–1925 bracket** is substantially stronger than the tentative c.1920 estimate, but it is still a secondary map-based conclusion; primary permit, assessment, deed, contractor, or construction-notice evidence is still needed to date the physical replacement precisely.

Legacy City source:
https://legacyorcity.teammunicode.com/planning/505-main-street

### 2000 City inventory — c.1920, now visually verified""",
    "1983 c.1908 date explicitly superseded",
)

replace_once(
    "database/buildings.yml",
    "The July 1922 Gates/Wolf division and 28 August model test do not decide the\n      exact 505 role; post-fire footprint, pre-fire division and ignition room require separate proof.",
    "The legacy City page says the 1983 survey indicated c.1908 but explicitly supersedes that date for the surviving building, placing construction from Sanborn comparison sometime between 1911 and 1925 and only tentatively around 1920. The July 1922 Gates/Wolf division and 28 August model test do not decide the\n      exact 505 role; post-fire footprint, pre-fire division and ignition room require separate proof.",
    "explicitly supersedes that date for the surviving building",
)

append_once(
    "evidence/source-captures/1919-1920-construction-occupancy-online-closeout-2026-09-01.md",
    "## 2 September 2026 — 505 c.1908 survey date superseded by City Sanborn bracket",
    """## 2 September 2026 — 505 c.1908 survey date superseded by City Sanborn bracket

Direct review of the registered City legacy page `S-033` resolves the meaning of the **c.1908** value encountered in later property-data searching. The City page says the **1983 survey indicated c.1908**, but then explicitly states that, according to its Sanborn-map comparison, the surviving 505 building was constructed **sometime between 1911 and 1925**, perhaps about 1920.

**Disposition:** this is a provenance/interpretive correction to existing `S-033` / `E-032`, so no new source or evidence ID is created. The archive now treats **c.1908 as a superseded 1983 survey date for the surviving 505 building**. The **1911–1925 physical-change bracket** is the stronger official-secondary conclusion; **c.1920 remains tentative** until primary construction, permit, assessment, deed, contractor, or contemporary newspaper evidence dates the replacement more precisely. This correction is consistent with, but does not replace, the project's independent map/photo analysis and does not by itself choose among the unresolved 1922 Gates/Wolf footprint models.
""",
)

print("503/505 survey provenance clarification integrated")
