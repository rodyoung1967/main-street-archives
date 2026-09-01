#!/usr/bin/env python3
"""Reduce the 1920-1921 505½ handoff OCR inventory to genuinely local/high-signal windows.

Discovery triage only; no OCR wording is promoted as evidence.
"""
from pathlib import Path
import json, re

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "evidence/source-captures/1920-1921-505half-handoff-ocr-discovery.json"
OUT = ROOT / "evidence/source-captures/1920-1921-505half-handoff-strong-candidates.md"
JSON_OUT = ROOT / "evidence/source-captures/1920-1921-505half-handoff-strong-candidates.json"

RX = {
    "505": re.compile(r"\b505\s*(?:½|1\s*/\s*2|1[- ]?2|'?4)?\b", re.I),
    "507": re.compile(r"\b507\s*(?:½|1\s*/\s*2|1[- ]?2|'?4)?\b", re.I),
    "main": re.compile(r"\bmain\s*(?:st(?:reet)?\.?)?\b", re.I),
    "leland": re.compile(r"\b(?:a\.?\s+)?leland\b", re.I),
    "clem": re.compile(r"\bclem\s+dollar\b", re.I),
    "freeze": re.compile(r"\b(?:dr\.?\s+|harvey\s+)?freeze\b", re.I),
    "harding_drug": re.compile(r"\bharding(?:s|'s)?\s+(?:drug|pharmacy)|\bover\s+harding(?:s|'s)?\s+drug", re.I),
    "pool": re.compile(r"\bpool\s*(?:hall|room)?\b|\bbilliard", re.I),
    "cigar": re.compile(r"\bcigar|\btobacco\b", re.I),
    "move": re.compile(r"\b(?:move[ds]?|moving|open(?:ed|ing)?|close[ds]?|closing|sold|sell|sale|lease[ds]?|rent(?:ed|ing)?|transfer(?:red)?|change[ds]?|permit(?:ted)?|license[ds]?|sign|vacant|occup(?:y|ied|ancy))\b", re.I),
}

def clean(s): return re.sub(r"\s+", " ", s).strip()

def classify(text):
    p={k for k,r in RX.items() if r.search(text)}
    reasons=[]
    # exact address + Main is always high signal
    if "main" in p and "505" in p: reasons.append("505 + Main in same local window")
    if "main" in p and "507" in p: reasons.append("507 + Main in same local window")
    # named handoff actors need local use/address context
    if "leland" in p and ({"505","pool"} & p): reasons.append("A./Leland + 505/pool context")
    if "clem" in p and ({"505","pool"} & p): reasons.append("Clem Dollar + 505/pool context")
    if "freeze" in p and ({"505","507","harding_drug"} & p): reasons.append("Freeze + exact address/Harding Drug context")
    if "harding_drug" in p and ({"507","freeze"} & p): reasons.append("Harding Drug + 507/Freeze context")
    # exact address plus transaction/use language can reveal a handoff even without name
    if ({"505","507"} & p) and "move" in p and ("main" in p or "pool" in p):
        reasons.append("exact target number + move/transfer/use language")
    return sorted(p), sorted(set(reasons))

def main():
    data=json.loads(SRC.read_text(encoding="utf-8"))
    out=[]
    for hit in data.get("hits",[]):
        selected=[]; rs=[]
        for w in hit.get("windows",[]):
            text=clean(w.get("text",""))
            terms,reasons=classify(text)
            if reasons:
                selected.append({"terms":terms,"reasons":reasons,"text":text})
                rs.extend(reasons)
        if selected:
            out.append({"date":hit["date"],"seq":hit["seq"],"url":hit["url"],"reasons":sorted(set(rs)),"windows":selected})
    result={"source":str(SRC.relative_to(ROOT)),"retained_pages_in_broad_handoff":len(data.get("hits",[])),"strong_pages":len(out),"hits":out,"status":"OCR discovery triage only; visual verification required"}
    JSON_OUT.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    lines=["# 1920–1921 505½ handoff strong-candidate index","","Status: **OCR DISCOVERY TRIAGE ONLY — direct scan review required before promotion**","",f"Broad handoff retained pages: **{result['retained_pages_in_broad_handoff']}**; high-signal pages after same-window filtering: **{len(out)}**.","","## High-signal pages",""]
    if not out: lines.append("No high-signal pages survived. This is a bounded search result, not evidence of historical absence.")
    for i,h in enumerate(out,1):
        lines += [f"### {i}. {h['date']} — page {h['seq']}",f"OCR URL: {h['url']}",f"Reasons: {'; '.join(h['reasons'])}",""]
        seen=set()
        for w in h["windows"][:5]:
            t=w["text"]
            key=t[:180]
            if key in seen: continue
            seen.add(key)
            lines.append(f"- Terms: {', '.join(w['terms'])}. OCR context: {t}")
        lines.append("")
    lines += ["## Limits","","- This filter only prioritizes visual-review candidates; it does not convert OCR to evidence.","- A filtered-out page is not evidence of absence, closure, vacancy, or non-operation.","- The 1919–1920 Banner-Courier microfilm gap remains material."]
    OUT.write_text("\n".join(lines)+"\n",encoding="utf-8")
    print(f"handoff strong filter: {result['retained_pages_in_broad_handoff']} -> {len(out)} pages")

if __name__ == '__main__': main()
