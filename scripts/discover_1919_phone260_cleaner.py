#!/usr/bin/env python3
"""Targeted OCR discovery for the visually verified 1 Aug 1919 cleaner ad.

OCR is discovery only. Search all calendar dates in 1919 for available Oregon
City Enterprise OCR pages and preserve hits for phone 260 / cleaner / new Post
Office wording. Any substantive hit still requires direct page-image review.
"""
from datetime import date, timedelta
from html.parser import HTMLParser
from html import unescape
from pathlib import Path
import re
import json
import time
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "evidence/source-captures/1919-phone260-cleaner-ocr-discovery.md"
JSON_OUT = ROOT / "evidence/source-captures/1919-phone260-cleaner-ocr-discovery.json"
LCCN = "sn00063700"
START = date(1919, 1, 1)
END = date(1919, 12, 31)
UA = "main-street-archives archival discovery/1.0"

class P(HTMLParser):
    def __init__(self):
        super().__init__(); self.parts=[]
    def handle_data(self, data): self.parts.append(data)
    def text(self): return re.sub(r"\s+", " ", unescape(" ".join(self.parts))).strip()

def get(url):
    try:
        with urlopen(Request(url, headers={"User-Agent": UA}), timeout=20) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except HTTPError as e:
        return e.code, ""
    except (URLError, TimeoutError):
        return None, ""

def text(html):
    p=P(); p.feed(html); return p.text()

def valid(t):
    return len(t) > 500 and "page not found" not in t.lower()

patterns = {
    "phone260": re.compile(r"phone\s*260\b", re.I),
    "cleaned_pressed_dyed": re.compile(r"clothes\s+cleaned.{0,20}pressed.{0,20}dyed", re.I),
    "new_postoffice": re.compile(r"new\s+post\s*office|new\s+postoffice", re.I),
    "two_doors_south": re.compile(r"two\s+doors\s+south", re.I),
    "500_fifth_main": re.compile(r"500.{0,30}(?:fifth|5th).{0,30}main|500.{0,30}main.{0,30}(?:fifth|5th)", re.I),
    "pantorium": re.compile(r"pantorium", re.I),
    "cleaner_dyer": re.compile(r"clean(?:er|ers|ing|ed)|dye(?:r|rs|ing|d)", re.I),
}

def snip(t, m, r=320):
    return t[max(0,m.start()-r):min(len(t),m.end()+r)]

def main():
    issues=[]; hits=[]; errors=[]
    day=START
    while day <= END:
        ds=day.isoformat()
        u1=f"https://oregonnews.uoregon.edu/lccn/{LCCN}/{ds}/ed-1/seq-1/ocr/"
        st,h=get(u1)
        if st == 200 and valid(text(h)):
            pages=0
            missing=0
            for seq in range(1, 17):
                u=f"https://oregonnews.uoregon.edu/lccn/{LCCN}/{ds}/ed-1/seq-{seq}/ocr/"
                if seq == 1:
                    st2,h2=st,h
                else:
                    st2,h2=get(u)
                t=text(h2) if st2 == 200 else ""
                if st2 == 200 and valid(t):
                    pages += 1; missing=0
                    found={k:list(p.finditer(t)) for k,p in patterns.items()}
                    found={k:v for k,v in found.items() if v}
                    # Keep exact discriminators, plus cleaner+new-postoffice contextual combinations.
                    exact=any(k in found for k in ("phone260","cleaned_pressed_dyed","two_doors_south","500_fifth_main","pantorium"))
                    contextual=("new_postoffice" in found and "cleaner_dyer" in found)
                    if exact or contextual:
                        snippets=[]; seen=set()
                        for k,ms in found.items():
                            for m in ms[:2]:
                                s=re.sub(r"\s+"," ",snip(t,m)).strip()
                                key=s[:100]
                                if key not in seen:
                                    snippets.append(s); seen.add(key)
                                if len(snippets) >= 8: break
                            if len(snippets) >= 8: break
                        hits.append({"date":ds,"seq":seq,"url":u,"groups":sorted(found),"snippets":snippets})
                else:
                    missing += 1
                    if pages and missing >= 2: break
                time.sleep(.025)
            issues.append({"date":ds,"pages":pages})
        elif st not in (404,410):
            errors.append({"date":ds,"status":st})
        day += timedelta(days=1)
        time.sleep(.015)

    data={"title":"Oregon City Enterprise","year":1919,"issues":issues,"page_count":sum(x['pages'] for x in issues),"hits":hits,"errors":errors,"status":"OCR discovery only; direct scan review required"}
    JSON_OUT.write_text(json.dumps(data,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    lines=["# 1919 Enterprise Phone 260 / cleaner OCR discovery","","Status: **OCR DISCOVERY ONLY — direct page review required for any new claim**","",f"Issues found: **{len(issues)}**; OCR pages checked: **{data['page_count']}**; matched pages: **{len(hits)}**.","","Purpose: identify repeats or naming/address bridges for the visually verified 1 Aug 1919 unnamed cleaner/dyer (`S-151` / `E-136`).","","## Hits",""]
    if not hits:
        lines.append("No matched OCR pages. Search silence is not evidence of absence.")
    for h in hits:
        lines += [f"### {h['date']} — page sequence {h['seq']}",f"URL: {h['url']}",f"Groups: {', '.join(h['groups'])}",""]
        for s in h['snippets']: lines.append(f"- OCR snippet: {s}")
        lines.append("")
    lines += ["## Limits","","- OCR is discovery only under `RESEARCH-STANDARD.md`.","- The already visually verified 1 Aug page controls where OCR differs.","- Do not identify Phone 260, normalize `500 Fifth and Main streets`, or merge the advertiser with Pantorium without an independent source bridge."]
    OUT.write_text("\n".join(lines)+"\n",encoding="utf-8")
    print(f"1919 targeted discovery: {len(issues)} issues / {data['page_count']} pages / {len(hits)} matched pages")

if __name__ == "__main__": main()
