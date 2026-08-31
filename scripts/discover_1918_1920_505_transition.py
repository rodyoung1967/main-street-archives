#!/usr/bin/env python3
"""Targeted OCR discovery for the 501/503/505 Main transition, Oct 1918-Jun 1920.

OCR is discovery only. Candidate hits must be checked against original page images
before promotion to source/evidence records.
"""
from datetime import date, timedelta
from html.parser import HTMLParser
from html import unescape
from pathlib import Path
import re, json, time
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "evidence/source-captures/1918-1920-505-transition-ocr-discovery.md"
JSON_OUT = ROOT / "evidence/source-captures/1918-1920-505-transition-ocr-discovery.json"
LCCN = "sn00063700"
START = date(1918, 10, 1)
END = date(1920, 6, 30)
UA = "main-street-archives archival discovery/1.0"

class P(HTMLParser):
    def __init__(self): super().__init__(); self.parts=[]
    def handle_data(self, data): self.parts.append(data)
    def text(self): return re.sub(r"\s+", " ", unescape(" ".join(self.parts))).strip()

def get(url):
    try:
        with urlopen(Request(url, headers={"User-Agent": UA}), timeout=20) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except HTTPError as e: return e.code, ""
    except (URLError, TimeoutError): return None, ""

def text(html): p=P(); p.feed(html); return p.text()
def valid(t): return len(t) > 500 and "page not found" not in t.lower()
def snip(t,m,r=420): return t[max(0,m.start()-r):min(len(t),m.end()+r)]

patterns = {
    "wolf_miller": re.compile(r"wolf\s*(?:&|and)\s*miller", re.I),
    "gilbert_miller": re.compile(r"gilbert\s+miller", re.I),
    "clem_dollar": re.compile(r"clem(?:ent)?\s+dollar", re.I),
    "a_leland": re.compile(r"\bA\.?\s+Leland\b", re.I),
    "leland": re.compile(r"\bLeland\b", re.I),
    "505half": re.compile(r"505\s*(?:1\s*/\s*2|½|one[- ]half)", re.I),
    "505_main": re.compile(r"\b505\b.{0,25}\bMain\b|\bMain\b.{0,25}\b505\b", re.I),
    "503_main": re.compile(r"\b503\b.{0,25}\bMain\b|\bMain\b.{0,25}\b503\b", re.I),
    "501_main": re.compile(r"\b501\b.{0,25}\bMain\b|\bMain\b.{0,25}\b501\b", re.I),
    "pool_hall": re.compile(r"pool\s*(?:hall|room)|billiard\s*(?:hall|room)", re.I),
    "fifth_sixth_main": re.compile(r"(?:fifth|5th).{0,80}(?:sixth|6th).{0,80}main|main.{0,80}(?:fifth|5th).{0,80}(?:sixth|6th)", re.I),
    "electric_sign": re.compile(r"electric\s+(?:street\s+)?sign", re.I),
    "construction": re.compile(r"new\s+(?:brick\s+)?building|construct(?:ed|ion|ing)?|erect(?:ed|ion|ing)?|rebuild(?:ing|t)?|remodel(?:ed|ing)?|demolish(?:ed|ing)?|tear(?:ing)?\s+down|torn\s+down", re.I),
    "lease_move": re.compile(r"(?:lease|leased|leasing|move|moved|moving|remove|removed|removing|vacate|vacated|vacating|occupy|occupied|occupying)", re.I),
}

# Candidate rules: exact targets always; broader construction/pool terms only with Main/block context.
def candidate(found, t):
    exact={"wolf_miller","gilbert_miller","clem_dollar","a_leland","505half","505_main","503_main","501_main"}
    if exact.intersection(found): return True
    if "leland" in found and ("pool_hall" in found or "electric_sign" in found): return True
    if "pool_hall" in found and "fifth_sixth_main" in found: return True
    if "electric_sign" in found and ("leland" in found or "505half" in found or "505_main" in found): return True
    # Construction/lease terms must occur on a page that also has 500-block address/block language.
    if ("construction" in found or "lease_move" in found) and ("fifth_sixth_main" in found or "505_main" in found or "503_main" in found or "501_main" in found): return True
    return False

def main():
    issues=[]; hits=[]; errors=[]
    day=START
    while day<=END:
        ds=day.isoformat(); u1=f"https://oregonnews.uoregon.edu/lccn/{LCCN}/{ds}/ed-1/seq-1/ocr/"
        st,h=get(u1); t1=text(h) if st==200 else ""
        if st==200 and valid(t1):
            pages=0; missing=0
            for seq in range(1,17):
                u=f"https://oregonnews.uoregon.edu/lccn/{LCCN}/{ds}/ed-1/seq-{seq}/ocr/"
                st2,h2=(st,h) if seq==1 else get(u); t=text(h2) if st2==200 else ""
                if st2==200 and valid(t):
                    pages+=1; missing=0
                    found={k:list(p.finditer(t)) for k,p in patterns.items()}
                    found={k:v for k,v in found.items() if v}
                    if candidate(set(found), t):
                        snippets=[]; seen=set()
                        priority=["505half","505_main","503_main","501_main","wolf_miller","gilbert_miller","clem_dollar","a_leland","leland","pool_hall","electric_sign","fifth_sixth_main","construction","lease_move"]
                        for k in priority:
                            for m in found.get(k,[])[:3]:
                                s=re.sub(r"\s+"," ",snip(t,m)).strip(); key=s[:120]
                                if key not in seen: snippets.append(s); seen.add(key)
                                if len(snippets)>=10: break
                            if len(snippets)>=10: break
                        hits.append({"date":ds,"seq":seq,"url":u,"groups":sorted(found),"snippets":snippets})
                else:
                    missing+=1
                    if pages and missing>=2: break
                time.sleep(.02)
            issues.append({"date":ds,"pages":pages})
        elif st not in (404,410): errors.append({"date":ds,"status":st})
        day+=timedelta(days=1); time.sleep(.01)

    data={"title":"Oregon City Enterprise","range":[START.isoformat(),END.isoformat()],"issues":issues,"page_count":sum(x['pages'] for x in issues),"hits":hits,"errors":errors,"status":"OCR discovery only; direct scan review required"}
    JSON_OUT.write_text(json.dumps(data,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    lines=["# 1918–1920 Enterprise 501/503/505 transition OCR discovery","","Status: **OCR DISCOVERY ONLY — direct page review required for any new claim**","",f"Date range: **{START.isoformat()} through {END.isoformat()}**.",f"Issues found: **{len(issues)}**; OCR pages checked: **{data['page_count']}**; candidate pages: **{len(hits)}**.","","Purpose: targeted follow-up for Wolf & Miller exit/succession, Clem Dollar, A. Leland, 501/503/505/505½ Main, pool-hall/sign wording, and construction/demolition/remodel/lease/move language around Main between Fifth and Sixth.","","## Candidate pages",""]
    if not hits: lines.append("No candidate OCR pages. Search silence is not evidence of absence.")
    for h in hits:
        lines += [f"### {h['date']} — page sequence {h['seq']}",f"URL: {h['url']}",f"Groups: {', '.join(h['groups'])}",""]
        for s in h['snippets']: lines.append(f"- OCR snippet: {s}")
        lines.append("")
    lines += ["## Limits","","- OCR is discovery only under `RESEARCH-STANDARD.md`; no new historical claim is promoted from this file alone.","- Generic construction/move language can be unrelated even when it appears on the same page as a target address; visually inspect context.","- Search silence does not establish vacancy, demolition, non-operation, or absence of construction.","- The unavailable-online 1919–1920 *Banner-Courier* remains a material manual microfilm gap."]
    OUT.write_text("\n".join(lines)+"\n",encoding="utf-8")
    print(f"Transition discovery: {len(issues)} issues / {data['page_count']} pages / {len(hits)} candidates")

if __name__=="__main__": main()
