#!/usr/bin/env python3
"""Temporary fast inventory-only probe for 1912 Historic Oregon Newspapers."""
from __future__ import annotations
import csv, json, re
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import urljoin
import requests

BASE="https://oregonnews.uoregon.edu"
TITLES={
 "courier":("sn00063698","Oregon City Courier"),
 "enterprise":("sn00063700","Oregon City Enterprise"),
 "morning-enterprise":("sn00063701","Morning Enterprise"),
}
OUT=Path("inventory-results"); OUT.mkdir(exist_ok=True)
S=requests.Session(); S.headers.update({"User-Agent":"MainStreetArchiveResearch/1.0"})

def get(url):
 r=S.get(url,timeout=30); r.raise_for_status(); return r.text

def issue_links(lccn):
 u=f"{BASE}/lccn/{lccn}/issues/1912/"
 h=get(u)
 rx=re.compile(r'href=["\']([^"\']*/lccn/'+re.escape(lccn)+r'/1912-\d{2}-\d{2}/ed-\d+/)["\']')
 links=[urljoin(BASE,x) for x in rx.findall(h)]
 if not links:
  rx=re.compile(r'href=["\']([^"\']*1912-\d{2}-\d{2}/ed-\d+/)["\']')
  links=[urljoin(u,x) for x in rx.findall(h)]
 return sorted(set(links))

def inspect(issue):
 h=get(issue)
 seq=sorted({int(x) for x in re.findall(r'/seq-(\d+)/',h)} or {int(x) for x in re.findall(r'seq-(\d+)',h)})
 d=re.search(r'/(1912-\d{2}-\d{2})/',issue)
 return d.group(1) if d else "UNKNOWN",seq,issue

def main():
 rows=[]; summary={}; errors=[]
 for key,(lccn,title) in TITLES.items():
  try: issues=issue_links(lccn)
  except Exception as e:
   errors.append({"title":key,"stage":"calendar","error":repr(e)}); continue
  out=[]
  with ThreadPoolExecutor(max_workers=16) as ex:
   futs={ex.submit(inspect,u):u for u in issues}
   for f in as_completed(futs):
    try: out.append(f.result())
    except Exception as e: errors.append({"title":key,"issue":futs[f],"stage":"issue","error":repr(e)})
  out.sort()
  pages=sum(len(s) for _,s,_ in out)
  summary[key]={"lccn":lccn,"title":title,"issue_count":len(issues),"inspected_issue_count":len(out),"page_count":pages,"first_issue":out[0][0] if out else None,"last_issue":out[-1][0] if out else None}
  for date,seqs,url in out:
   rows.append({"title_key":key,"title":title,"lccn":lccn,"date":date,"issue_url":url,"page_count":len(seqs),"sequences":" ".join(map(str,seqs))})
 with (OUT/"inventory.csv").open("w",newline="",encoding="utf-8") as f:
  w=csv.DictWriter(f,fieldnames=["title_key","title","lccn","date","issue_url","page_count","sequences"]); w.writeheader(); w.writerows(rows)
 (OUT/"inventory.json").write_text(json.dumps(rows,indent=2),encoding="utf-8")
 (OUT/"summary.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
 (OUT/"errors.json").write_text(json.dumps(errors,indent=2),encoding="utf-8")
 print(json.dumps(summary,indent=2)); print("errors",len(errors))

if __name__=="__main__": main()
