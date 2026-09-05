from pathlib import Path
import json, urllib.parse, urllib.request

BASE='https://maps.orcity.org/ArcGIS/rest/services/ArmyCorpsHistoricalPhotos/MapServer/export'
# 500 ft square centered on established 5th/Main coordinate transformed to EPSG:2913.
BBOX='7659549.8,622938.4,7660049.8,623438.4'
YEARS={1936:17,1940:16,1944:15,1950:14,1955:13,1961:12,1969:11,1972:10,1974:9}
out=Path('/tmp/aerial-direct'); out.mkdir(parents=True,exist_ok=True)
for year,layer in YEARS.items():
    q={'bbox':BBOX,'bboxSR':'2913','layers':f'show:{layer}','size':'1200,1200','imageSR':'2913','format':'jpg','transparent':'false','f':'json'}
    url=BASE+'?'+urllib.parse.urlencode(q)
    req=urllib.request.Request(url,headers={'User-Agent':'Main-Street-Archive/1.0'})
    with urllib.request.urlopen(req,timeout=45) as r:
        meta=json.load(r)
    href=meta.get('href')
    if not href:
        raise SystemExit(f'{year}: no export href: {meta}')
    req=urllib.request.Request(href,headers={'User-Agent':'Main-Street-Archive/1.0'})
    with urllib.request.urlopen(req,timeout=45) as r:
        data=r.read()
    if not data.startswith(b'\xff\xd8'):
        raise SystemExit(f'{year}: expected JPEG, got {data[:80]!r}')
    (out/f'{year}.jpg').write_bytes(data)
    print(year,len(data),href,flush=True)
