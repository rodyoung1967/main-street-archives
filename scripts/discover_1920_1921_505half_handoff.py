#!/usr/bin/env python3
"""Targeted OCR discovery for the A. Leland -> Dr. Freeze 505½ handoff.

OCR is discovery only. Search every available Oregon City Enterprise page from
4 Jun 1920 through 8 Apr 1921 and retain only local context windows containing
exact target address/name/use terms. Any new claim requires direct scan review.
"""
from datetime import date, timedelta
from html.parser import HTMLParser
from html import unescape
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
import json, re, time

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "evidence/source-captures/1920-1921-505half-handoff-ocr-discovery.md"
JSON_OUT = ROOT / "evidence/source-captures/1920-1921-505half-handoff-ocr-discovery.json"
LCCN = "sn00063700"
START = date(1920, 6, 4)
END = date(1921, 4, 8)
UA = "main-street-archives targeted archival discovery/1.0"

class P(HTMLParser):
    def __init__(self): super().__init__(); self.parts=[]
    def handle_data(self, data): self.parts.append(data)
    def text(self): return re.sub(r"\s+", " ", unescape(" ".join(self.parts))).strip()

def get(url):
    try:
        with urlopen(Request(url, headers={"User-Agent": UA}), timeout=25) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except HTTPError as e: return e.code, ""
    except (URLError, TimeoutError): return None, ""

def txt(html): p=P(); p.feed(html); return p.text()
def valid(t): return len(t) > 500 and "page not found" not in t.lower()

patterns = {
    "505": re.compile(r"\b505\s*(?:[½]|1\s*/\s*2|1[- ]?2|'?4)?\b", re.I),
    "507": re.compile(r"\b507\s*(?:[½]|1\s*/\s*2|1[- ]?2|'?4)?\b", re.I),
    "leland": re.compile(r"\b(?:a\.?\s+|o\.?\s*h\.?\s+)?leland\b", re.I),
    "clem_dollar": re.compile(r"\bclem\s+dollar\b", re.I),
    "freeze": re.compile(r"\b(?:dr\.?\s+|harvey\s+)?freeze\b", re.I),
    "harding": re.compile(r"\bharding(?:s|'s)?\b", re.I),
    "pool": re.compile(r"\bpool\s*(?:hall|room)?\b|\bbilliard", re.I),
    "cigar": re.compile(r"\bcigar|\btobacco\b", re.I),
    "transition": re.compile(r"\b(?:move[ds]?|moving|open(?:ed|ing)?|close[ds]?|closing|sold|sell|sale|lease[ds]?|rent(?:ed|ing)?|transfer(?:red)?|change[ds]?|permit(?:ted)?|license[ds]?|sign|remodel(?:ed|ing)?|repair(?:ed|ing)?|build(?:ing|s)?|construct(?:ed|ion|ing)?|vacant|occup(?:y|ied|ancy))\b", re.I),
    "main": re.compile(r"\bmain\b", re.I),
}

TARGET = {"505","507","leland","clem_dollar","freeze","harding","pool"}

def windows(t, radius=520):
    spans=[]
    for key in TARGET:
        for m in patterns[key].finditer(t):
            spans.append((m.start(), m.end(), key))
    out=[]; seen=set()
    for s,e,key in spans:
        a=max(0,s-radius); b=min(len(t),e+radius)
        w=re.sub(r"\s+"," ",t[a:b]).strip()
        sig=w[:180]
        if sig in seen: continue
        seen.add(sig)
        present=sorted(k for k,rx in patterns.items() if rx.search(w))
        # Keep exact address windows or person/use windows with Main/transition context.
        strong=("505" in present or "507" in present or
                (({"leland","clem_dollar","freeze","harding"} & set(present)) and
                 ({"pool","main","transition"} & set(present))))
        if strong:
            out.append({"trigger":key,"terms":present,"text":w})
    return out

def main():
    issues=[]; hits=[]; errors=[]
    d=START
    while d <= END:
        ds=d.isoformat()
        u1=f"https://oregonnews.uoregon.edu/lccn/{LCCN}/{ds}/ed-1/seq-1/ocr/"
        st,h=get(u1); t1=txt(h) if st==200 else ""
        if st==200 and valid(t1):
            pages=0; missing=0
            for seq in range(1,13):
                u=f"https://oregonnews.uoregon.edu/lccn/{LCCN}/{ds}/ed-1/seq-{seq}/ocr/"
                st2,h2=(st,h) if seq==1 else get(u)
                t=txt(h2) if st2==200 else ""
                if st2==200 and valid(t):
                    pages+=1; missing=0
                    ws=windows(t)
                    if ws:
                        hits.append({"date":ds,"seq":seq,"url":u,"windows":ws})
                else:
                    missing+=1
                    if pages and missing>=2: break
                time.sleep(.02)
            issues.append({"date":ds,"pages":pages})
        elif st not in (404,410): errors.append({"date":ds,"status":st})
        d += timedelta(days=1); time.sleep(.01)

    data={"title":"Oregon City Enterprise","range":[START.isoformat(),END.isoformat()],
          "issues":issues,"page_count":sum(x['pages'] for x in issues),"hits":hits,
          "errors":errors,"status":"OCR discovery only; direct scan review required"}
    JSON_OUT.write_text(json.dumps(data,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    lines=["# 1920–1921 Enterprise 505½ handoff OCR discovery","",
           "Status: **OCR DISCOVERY ONLY — direct scan review required before promotion**","",
           f"Range: **{START.isoformat()} through {END.isoformat()}**; issues found: **{len(issues)}**; OCR pages checked: **{data['page_count']}**; pages with retained target context: **{len(hits)}**.","",
           "Purpose: narrow the gap between A. Leland's visually verified 4 June 1920 505½ pool-hall permit (`E-135`) and Dr. Freeze's visually verified 8 April 1921 505½ advertisement (`E-028`/`E-137`).","","## Retained pages",""]
    if not hits: lines.append("No retained pages. Search silence is not evidence of historical absence.")
    for h in hits:
        lines += [f"### {h['date']} — page {h['seq']}",f"OCR URL: {h['url']}",""]
        for w in h['windows'][:6]:
            lines.append(f"- Terms: {', '.join(w['terms'])}. OCR context: {w['text']}")
        lines.append("")
    lines += ["## Limits","","- OCR is discovery only under `RESEARCH-STANDARD.md`.","- Generic 505/507 numbers can refer to non-Main addresses; visual/context review is mandatory.","- Absence of a Leland or pool-hall hit does not establish closure, vacancy, transfer, demolition, or non-operation.","- The unavailable-online *Banner-Courier* remains a material gap for this interval."]
    OUT.write_text("\n".join(lines)+"\n",encoding="utf-8")
    print(f"handoff discovery: {len(issues)} issues / {data['page_count']} pages / {len(hits)} retained pages")

if __name__ == "__main__": main()
