#!/usr/bin/env python3
"""Targeted OCR discovery for the 505/505½ pool-hall transition, Jul 1920-Dec 1922.

OCR is discovery only. Any substantive claim requires direct scan review.
"""
from datetime import date, timedelta
from html.parser import HTMLParser
from html import unescape
from pathlib import Path
import json, re, time
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "evidence/source-captures/1920-1922-505-poolhall-transition-ocr-discovery.md"
JSON_OUT = ROOT / "evidence/source-captures/1920-1922-505-poolhall-transition-ocr-discovery.json"
LCCN = "sn00063700"
START = date(1920, 7, 1)
END = date(1922, 12, 31)
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

def valid(t): return len(t) > 500 and "page not found" not in t.lower()

patterns = {
    "leland": re.compile(r"\bleland\b", re.I),
    "clem_dollar": re.compile(r"\bclem\s+dollar\b", re.I),
    "timms": re.compile(r"\btim+['’]?s?\b|\btimms\b", re.I),
    "505": re.compile(r"\b505(?:\s*[½1][/-]?2)?\b|\b505\s*1\s*/\s*2\b", re.I),
    "pool_hall": re.compile(r"pool\s*(?:hall|room)|billiard", re.I),
    "cigar_tobacco": re.compile(r"cigar|tobacco", re.I),
    "freeze": re.compile(r"\b(?:dr\.?\s+)?freeze\b", re.I),
    "wolf_miller": re.compile(r"wolf\s*(?:&|and)\s*miller", re.I),
}

def snip(t,m,r=420): return t[max(0,m.start()-r):min(len(t),m.end()+r)]

def main():
    issues=[]; hits=[]; errors=[]
    day=START
    while day <= END:
        ds=day.isoformat()
        u1=f"https://oregonnews.uoregon.edu/lccn/{LCCN}/{ds}/ed-1/seq-1/ocr/"
        st,h=get(u1); t1=text(h) if st == 200 else ""
        if st == 200 and valid(t1):
            pages=0; missing=0
            for seq in range(1,17):
                u=f"https://oregonnews.uoregon.edu/lccn/{LCCN}/{ds}/ed-1/seq-{seq}/ocr/"
                if seq == 1: st2,h2=st,h
                else: st2,h2=get(u)
                t=text(h2) if st2 == 200 else ""
                if st2 == 200 and valid(t):
                    pages += 1; missing=0
                    found={k:list(p.finditer(t)) for k,p in patterns.items()}
                    found={k:v for k,v in found.items() if v}
                    names=any(k in found for k in ("leland","clem_dollar","timms","freeze","wolf_miller"))
                    address_context=("505" in found and any(k in found for k in ("pool_hall","cigar_tobacco")))
                    if names or address_context:
                        snippets=[]; seen=set()
                        preferred=("leland","clem_dollar","timms","505","pool_hall","freeze","wolf_miller","cigar_tobacco")
                        for k in preferred:
                            for m in found.get(k,[])[:2]:
                                s=re.sub(r"\s+"," ",snip(t,m)).strip()
                                key=s[:120]
                                if key not in seen: snippets.append(s); seen.add(key)
                                if len(snippets)>=10: break
                            if len(snippets)>=10: break
                        hits.append({"date":ds,"seq":seq,"url":u,"groups":sorted(found),"snippets":snippets})
                else:
                    missing += 1
                    if pages and missing >= 2: break
                time.sleep(.02)
            issues.append({"date":ds,"pages":pages})
        elif st not in (404,410): errors.append({"date":ds,"status":st})
        day += timedelta(days=1)
        time.sleep(.01)

    data={"title":"Oregon City Enterprise","range":[START.isoformat(),END.isoformat()],"issues":issues,"page_count":sum(x['pages'] for x in issues),"hits":hits,"errors":errors,"status":"OCR discovery only; direct scan review required"}
    JSON_OUT.write_text(json.dumps(data,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    lines=["# 1920–1922 Enterprise 505/505½ pool-hall transition OCR discovery","","Status: **OCR DISCOVERY ONLY — direct page review required for any new claim**","",f"Date range: **{START.isoformat()} through {END.isoformat()}**.",f"Issues found: **{len(issues)}**; OCR pages checked: **{data['page_count']}**; candidate pages: **{len(hits)}**.","","Purpose: follow the June 1920 A. Leland 505½ pool-hall/sign anchor forward toward Clem Dollar/Timms/Dr. Freeze and later 505 use. Search silence is not evidence of absence.","","## Candidate pages",""]
    for h in hits:
        lines += [f"### {h['date']} — page sequence {h['seq']}", f"URL: {h['url']}", f"Groups: {', '.join(h['groups'])}", ""]
        for s in h['snippets']: lines.append(f"- OCR snippet: {s}")
        lines.append("")
    lines += ["## Limits","","- OCR is discovery only under `RESEARCH-STANDARD.md`.","- Names may refer to unrelated people; 505 may occur in unrelated addresses/numbers.","- Direct page-image review is required before any new occupant, succession, relocation, or construction claim is promoted."]
    OUT.write_text("\n".join(lines)+"\n",encoding="utf-8")
    print(f"1920-1922 poolhall discovery: {len(issues)} issues / {data['page_count']} pages / {len(hits)} candidate pages")

if __name__ == "__main__": main()
