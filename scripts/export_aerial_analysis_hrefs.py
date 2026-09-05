from pathlib import Path
import json, urllib.parse, urllib.request

BASE = 'https://maps.orcity.org/ArcGIS/rest/services/ArmyCorpsHistoricalPhotos/MapServer/export'
BBOX = '7659300,622700,7660300,623700'
YEARS = {1936:17, 1940:16, 1944:15, 1950:14, 1955:13, 1961:12, 1969:11, 1972:10, 1974:9}
rows=[]
for year, layer in YEARS.items():
    q = {
        'bbox': BBOX,
        'bboxSR': '2913',
        'layers': f'show:{layer}',
        'size': '2000,2000',
        'imageSR': '2913',
        'format': 'jpg',
        'transparent': 'false',
        'f': 'json',
    }
    url = BASE + '?' + urllib.parse.urlencode(q)
    req=urllib.request.Request(url,headers={'User-Agent':'Main-Street-Archive/1.0'})
    with urllib.request.urlopen(req,timeout=90) as r:
        data=json.load(r)
    href=data.get('href')
    if not href:
        raise SystemExit(f'{year}: no href: {data}')
    rows.append((year,layer,url,href,data.get('width'),data.get('height'),data.get('extent')))

out=['# Temporary aligned aerial exports','',f'BBOX EPSG:2913: `{BBOX}`. Generated for visual comparison; temporary navigation data only.','']
for year,layer,url,href,w,h,extent in rows:
    out += [f'## {year}',f'- layer: `{layer}`',f'- request: {url}',f'- image: {href}',f'- dimensions: {w} × {h}',f'- extent: `{json.dumps(extent,sort_keys=True)}`','']
Path('research-inbox/aerial-analysis-export-hrefs-2026-09-05.md').write_text('\n'.join(out),encoding='utf-8')
print('\n'.join(f'{y}: {h}' for y,_,_,h,_,_,_ in rows))
