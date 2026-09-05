from pathlib import Path
import hashlib, json, re, urllib.parse, urllib.request
from io import BytesIO
from PIL import Image

TARGET='P-4565'
ACCOUNT='4813'
REVIEW='2026-09-04'
STEWARD={'filename':"Oregon City 1960's - Street Scene - Corner of Main and McLoughlin.jpg",'width':2048,'height':1639,'bytes':539871,'sha256':'e1cc91d86616daf4cc863b30159742e0bc98e5e698bf56fcd671cfa0a56a8a59'}

def rd(p): return Path(p).read_text(encoding='utf-8')
def wr(p,s):
    q=Path(p); q.parent.mkdir(parents=True,exist_ok=True); q.write_text(s,encoding='utf-8')
def append_once(p,marker,block):
    s=rd(p)
    if marker in s: return
    wr(p,s.rstrip()+'\n\n'+block.rstrip()+'\n')
def maxid(p,prefix):
    vals=[int(x) for x in re.findall(rf'\b{re.escape(prefix)}-(\d+)\b',rd(p))]
    return max(vals)
def get_json(url):
    req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 Main-Street-Archive/1.0'})
    with urllib.request.urlopen(req,timeout=90) as r: return json.load(r)
def get_bytes(url):
    req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 Main-Street-Archive/1.0'})
    with urllib.request.urlopen(req,timeout=90) as r: return r.read()
def catno(d):
    try:return d['properties']['hasCatalogNumber']['value_text']
    except:return None
def find(obj):
    if isinstance(obj,dict):
        if catno(obj)==TARGET:return obj
        for v in obj.values():
            z=find(v)
            if z is not None:return z
    elif isinstance(obj,list):
        for v in obj:
            z=find(v)
            if z is not None:return z
    return None
def derivative(entry):
    a=[]
    for m in entry.get('media',[]):
        for k,v in m.get('derivatives',{}).items():
            if not isinstance(v,dict) or not v.get('path') or 'thumbnail' in k: continue
            w,h=int(v.get('width') or 0),int(v.get('height') or 0)
            if w and h:a.append((w*h,w,h,k,v['path']))
    if not a: raise SystemExit('No public image derivative found')
    a.sort(reverse=True); _,w,h,k,u=a[0]; return {'key':k,'width':w,'height':h,'url':u}

# duplicate guard
for p in ['evidence/source-register.md','media/photo-metadata-register.md','indexes/id-crosswalk.md']:
    if TARGET in rd(p):
        print(f'{TARGET} already integrated; no changes needed.'); raise SystemExit(0)

SID=f"S-{maxid('evidence/source-register.md','S')+1:03d}"
EID=f"E-{maxid('evidence/evidence-register.md','E')+1:03d}"
MID=f"IMG-{maxid('media/photo-metadata-register.md','IMG')+1:04d}"
TID=f"T-{maxid('timeline.md','T')+1:03d}"
b=maxid('businesses/business-index.md','BUS')
COAST=f'BUS-{b+1:03d}'; VOA=f'BUS-{b+2:03d}'; SEID=f'BUS-{b+3:03d}'

SEARCH='https://api.catalogit.app/api/public/search?'+urllib.parse.urlencode({'query':TARGET,'size':50})
match=find(get_json(SEARCH))
if match is None: raise SystemExit('Exact CCHS P-4565 not returned by catalog search')
entry_id=match.get('id')
ENTRY=f'https://api.catalogit.app/api/public/accounts/{ACCOUNT}/entries/{entry_id}'
entry=get_json(ENTRY)
if catno(entry)!=TARGET: raise SystemExit('Fetched catalog entry mismatch')
der=derivative(entry); data=get_bytes(der['url'])
if not data.startswith(b'\xff\xd8'): raise SystemExit('Selected derivative is not JPEG')
im=Image.open(BytesIO(data)); w,h=im.size
sha=hashlib.sha256(data).hexdigest(); n=len(data)
slug=entry.get('slug') or match.get('slug')
HUB=f'https://hub.catalogit.app/clackamas-county-historical-society/folder/photographs/entry/{slug}' if slug else ENTRY
IMAGE=f'media/photos/main-street/{MID}_circa-mid-1960s-503-517-main-business-lineup-cchs-p4565.jpg'
Path(IMAGE).parent.mkdir(parents=True,exist_ok=True); Path(IMAGE).write_bytes(data)
CAP='evidence/source-captures/cchs-p4565-mid-1960s-main-fifth-business-lineup-2026-09-04.md'
API='evidence/source-captures/cchs-p4565-mid-1960s-main-fifth-business-lineup-api-2026-09-04.json'
api={'reviewed':REVIEW,'catalog':TARGET,'search_url':SEARCH,'entry_url':ENTRY,'hub_url':HUB,'selected_derivative':der,'repository_file':IMAGE,'repository_image':{'width':w,'height':h,'bytes':n,'sha256':sha},'steward_upload':STEWARD,'entry':entry}
wr(API,json.dumps(api,indent=2,ensure_ascii=False)+'\n')

SOURCE_NAME="CCHS P-4565 — Oregon City mid-1960s Main Street business lineup"
EVIDENCE_NAME="Circa mid-1960s photograph documents 503/505 and neighboring Main Street businesses"
TIMELINE_NAME="Circa mid-1960s — photographed Main Street lineup before the 1967 fire"

capture=f'''# {SOURCE_NAME}\n\nReviewed **4 September 2026** from the project-steward supplied photograph and the exact Clackamas County Historical Society public catalog object recovered as `{TARGET}`.\n\nArchive IDs: source `{SID}`; evidence `{EID}`; media `{MID}`; timeline `{TID}`.\n\n## Catalog metadata supplied by project steward\n\n- Name/Title: **Oregon City 1960's - Street Scene - Corner of Main and McLoughlin**\n- Entry/Object ID: `{TARGET}`\n- Description: **Corner of Main and McLoughlin Blvd., Oregon City. Commercial buildings. Circa mid-1960s The Wheel, 505 Tavern, Coast to Coast Store, Dixon's Pastry Shop, Harding (sp?) Drugs, Thrift Store, Seid's Restaurant.**\n- Exposure date: **not exact; catalog description says circa mid-1960s**.\n- Public record: {HUB}\n- Public API: {ENTRY}\n\n## Steward upload\n\n- Filename: `{STEWARD['filename']}`\n- Dimensions: **{STEWARD['width']} × {STEWARD['height']}**\n- Bytes: **{STEWARD['bytes']:,}**\n- SHA-256: `{STEWARD['sha256']}`\n\n## Repository image\n\n- File: `{IMAGE}`\n- Largest public CCHS derivative recovered: **{w} × {h}**, {n:,} bytes\n- SHA-256: `{sha}`\n\n## Direct visual review\n\nThe photograph shows the east-side Main Street commercial row beginning with the Wheel/503 corner area and continuing past 505 toward the later 507–517 storefront sequence. Important readable features include:\n\n- the street blades **5th ST** and **MAIN** at the corner;\n- prominent wheel motifs on the catalog-identified **The Wheel** frontage; the words “The Wheel” themselves are not clearly legible in this scan;\n- a window/facade sign reading **RAIN CHECK / Room / BREAKFAST / LUNCH & DINNERS** on the Wheel-side frontage; whether “Rain Check Room” was a room name, sub-operation of The Wheel, or a separate establishment is unresolved;\n- a projecting sign reading **TAVERN** with vertical **505**, directly documenting the 505-numbered tavern frontage;\n- **COAST TO COAST STORES**;\n- **DIXON'S Pastry Shop**;\n- **HARDING DRUGS** (the catalog transcriber marked the Harding spelling with “sp?”);\n- **VOLUNTEERS / AMERICA / THRIFT STORE**;\n- **Seid's** with **RESTAURANT** signage and a nearby **CAFE** sign.\n\n## Cross-source significance\n\n- `BUS-004` The Wheel is independently fixed at **503 Main** by primary municipal evidence in 1967; this photograph adds visual facade context.\n- `BUS-005` 505 Tavern is independently documented by the **11 November 1965** Oregon City liquor renewal (`S-038` / `E-029`). The photograph's **TAVERN / 505** sign is direct visual corroboration, not the sole basis for dating the name.\n- `BUS-023` Dixon's Pastry Shop is independently documented at **509 Main** on 10 June 1964 (`S-144` / `E-129`).\n- `BUS-007` Harding Drug Store is separately named among businesses gutted in the **1 September 1967** fire (`S-052` / `E-045`).\n- The same 1967 fire report names **Coast Hardware Co.**, **Dixon's Bakery**, **Hardings Drug Store**, and **Volunteers of America Thrift Shop** as gutted, while **Wheel Restaurant** and **505 Tavern** were spared by flames but had smoke/water damage. The photo therefore provides a visual pre-fire lineup for several businesses independently named in that article.\n- A 1948 municipal liquor-license list separately places **Seid's Restaurant at 517 Main** with Wallace and Mary R. Seid. The mid-1960s photograph shows the Seid's sign farther along the same row, but an exact 1960s street number is not readable in the photograph itself.\n\n## Location wording conflict\n\nCCHS's supplied title/description says **Corner of Main and McLoughlin Blvd.** The photograph itself visibly carries **5th ST** and **MAIN** street signs at the photographed corner. The archive preserves both facts. The catalog wording may describe the broader camera/roadway context rather than the exact signed intersection, but that explanation is not proved. For the target 503/505 frontage, the visible **5th/Main** street blades are the stronger direct spatial observation.\n\n## Evidence classification\n\n- **DOCUMENTED / DIRECT:** readable business/sign text listed above, including **TAVERN / 505**, Coast to Coast Stores, Dixon's Pastry Shop, Harding Drugs, Volunteers of America Thrift Store, and Seid's/Restaurant.\n- **DOCUMENTED / DIRECT (institutional catalog):** CCHS identifies The Wheel and the listed business lineup and dates the scene only as circa mid-1960s.\n- **STRONG CROSS-SOURCE CONTEXT:** the photograph visually brackets the Main Street business row shortly before the 1 September 1967 fire and agrees with independently dated 1964–1967 records.\n- **UNRESOLVED:** exact exposure date; catalog Main/McLoughlin wording versus visible 5th/Main street blades; exact individual street numbers for Coast to Coast, Harding Drugs, Volunteers thrift, and the photographed Seid's storefront; status/ownership of the Rain Check Room wording.\n'''
wr(CAP,capture)

append_once('evidence/source-register.md',f'## {SID} —',f'''## {SID} — {SOURCE_NAME}\nType: Primary historic photograph with CCHS institutional catalog metadata; **VISUALLY VERIFIED** 4 September 2026.\nInstitution: Clackamas County Historical Society.\nCatalog ID: `{TARGET}`.\nDate: **circa mid-1960s** per catalog description; exact exposure date unresolved.\nRepository image: `{IMAGE}`.\nCapture: `{CAP}`.\nPublic record: {HUB}\nRelated evidence/media/timeline: `{EID}` / `{MID}` / `{TID}`.\nNotes: Directly readable signs include **TAVERN / 505**, Coast to Coast Stores, Dixon's Pastry Shop, Harding Drugs, Volunteers of America Thrift Store, and Seid's/Restaurant. The image visibly shows **5th ST / MAIN** street blades; CCHS's supplied title/description instead says Main and McLoughlin Blvd., so both are preserved as a location-wording conflict.''')

append_once('evidence/evidence-register.md',f'## {EID} —',f'''## {EID} — {EVIDENCE_NAME}\nSource: `{SID}`\nMedia: `{MID}`\nType: Primary photographic evidence with institutional catalog metadata\nClaims:\n- CCHS catalogs the scene as circa mid-1960s and lists **The Wheel, 505 Tavern, Coast to Coast Store, Dixon's Pastry Shop, Harding (sp?) Drugs, Thrift Store, and Seid's Restaurant**.\n- Visual review directly reads **TAVERN / 505**, **COAST TO COAST STORES**, **DIXON'S Pastry Shop**, **HARDING DRUGS**, **VOLUNTEERS / AMERICA / THRIFT STORE**, and **Seid's / RESTAURANT**, plus a **RAIN CHECK Room / BREAKFAST / LUNCH & DINNERS** sign whose relationship to The Wheel is unresolved.\n- The image directly shows **5th ST** and **MAIN** street blades at the target corner, while the CCHS title/description says Main and McLoughlin Blvd.; preserve the conflict.\n- This provides visual pre-fire context for businesses independently named in the 1 September 1967 fire report (`E-045`), and corroborates the 1965 505 Tavern renewal (`E-029`) and 1964 Dixon's 509 Main advertisement (`E-129`).\nClassification: **DOCUMENTED / DIRECT** for visible lettering and institutional catalog description; **STRONG CROSS-SOURCE CONTEXT** for the pre-1967-fire lineup; exact exposure date and several exact storefront numbers unresolved.\nConfidence: **Very High** for visible signage and P-4565 identity; **High** for broad circa-mid-1960s/pre-fire context; location wording conflict preserved rather than resolved by assumption.''')

append_once('media/photo-metadata-register.md',f'## {MID} —',f'''## {MID} — CCHS P-4565, circa-mid-1960s Main Street business lineup\n- Type: Historic street-level commercial photograph\n- Date: **circa mid-1960s** per CCHS catalog description; exact exposure date unresolved\n- Location: target row at **5th/Main visibly signed in photograph**; CCHS title/description says Main and McLoughlin Blvd.\n- Source/Evidence: `{SID}` / `{EID}`\n- Repository file: `{IMAGE}`\n- CCHS catalog: `{TARGET}`\n- Repository dimensions: **{w} × {h}**; SHA-256 `{sha}`\n- Steward original: `{STEWARD['filename']}`; {STEWARD['width']}×{STEWARD['height']}; {STEWARD['bytes']:,} bytes; SHA-256 `{STEWARD['sha256']}`\n- Visual business/sign findings: **TAVERN / 505**, Coast to Coast Stores, Dixon's Pastry Shop, Harding Drugs, Volunteers of America Thrift Store, Seid's/Restaurant, and unresolved **Rain Check Room** wording; CCHS also identifies The Wheel.''')
append_once('media/photos/inventory.md',f'### {MID} —',f'''### {MID} — Circa-mid-1960s Main Street business lineup\n- File: `{IMAGE}`\n- Source/evidence: `{SID}` / `{EID}`\n- CCHS: `{TARGET}`\n- Key value: visual lineup of The Wheel/503, **TAVERN 505**, Coast to Coast, Dixon's Pastry Shop, Harding Drugs, Volunteers thrift, and Seid's before the 1967 fire; visible **5th/Main** street blades preserved against conflicting catalog Main/McLoughlin wording.''')

# New businesses introduced by the photograph / existing primary context.
new_businesses=[
 (COAST,'Coast to Coast Stores','businesses/coast-to-coast-stores.md','Main Street between 5th and 6th; exact number unresolved in this photo',"Directly legible in CCHS P-4565. Relationship to the 1967 fire article's 'Coast Hardware Co.' is plausible but not silently equated without an exact business-name/address bridge."),
 (VOA,'Volunteers of America Thrift Store','businesses/volunteers-of-america-thrift-store.md','Main Street between 5th and 6th; exact number unresolved in this photo',"Directly legible in CCHS P-4565 and independently named in the 1 September 1967 fire report; this is strong continuity to the same distinctive establishment name."),
 (SEID,"Seid's Restaurant",'businesses/seids-restaurant.md','517 Main documented in 1948; exact number not readable in this mid-1960s photo',"A 1948 municipal license list directly places Seid's Restaurant at 517 Main with Wallace and Mary R. Seid; CCHS P-4565 visibly shows Seid's/Restaurant in the later streetscape. Continuous operators/address through the whole interval are not assumed."),
]
idx=rd('businesses/business-index.md').rstrip()
for bid,name,path,address,notes in new_businesses:
    if f'| {bid} |' not in idx:
        idx += f"\n| {bid} | [{name}]({path.split('/')[-1]}) | {address} | {notes} |"
    wr(path,f'''# {name}\n\nBusiness ID: `{bid}`.\n\nAddress/status: **{address}**.\n\n{notes}\n\n## Mid-1960s photograph\n\nCCHS `{TARGET}` (`{SID}` / `{EID}` / `{MID}`) provides direct visual or catalog evidence for this business in the photographed Main Street lineup. Exact exposure date remains **circa mid-1960s**.\n''')
wr('businesses/business-index.md',idx+'\n')

# append structured new business records without reformatting existing YAML
by=rd('database/businesses.yml').rstrip()
for bid,name,path,address,notes in new_businesses:
    if f'  - id: {bid}\n' not in by:
        safe_notes=notes.replace("'","''")
        by += f"\n\n  - id: {bid}\n    name: {name}\n    repository_file: {path}\n    address: \"{address}\"\n    notes: \"{notes.replace(chr(34), chr(39))}\"\n    related_evidence: [{EID}]\n    related_sources: [{SID}]\n    related_media: [{MID}]"
wr('database/businesses.yml',by+'\n')

# existing business/building narrative updates
for path,title,text in [
 ('businesses/the-wheel.md','Mid-1960s P-4565 photograph',f'CCHS `{TARGET}` (`{SID}` / `{EID}` / `{MID}`) catalogs **The Wheel** in this circa-mid-1960s Main Street lineup. Wheel motifs are directly visible on the 503-side frontage; the words “The Wheel” are not clearly readable in the scan. A **RAIN CHECK Room / BREAKFAST / LUNCH & DINNERS** sign is directly visible on the same facade zone, but its relationship to The Wheel is unresolved.'),
 ('businesses/the-505.md','Mid-1960s P-4565 photograph',f'CCHS `{TARGET}` (`{SID}` / `{EID}` / `{MID}`) directly shows a projecting **TAVERN** sign with vertical **505** on the 505 frontage. This visually corroborates, but does not replace, the exact **11 November 1965** municipal liquor-renewal evidence (`E-029`).'),
 ('businesses/dixons-bakery.md','Mid-1960s P-4565 photograph',f'CCHS `{TARGET}` (`{SID}` / `{EID}` / `{MID}`) directly shows **DIXON’S Pastry Shop** in the photographed row. This visually corroborates the independent 10 June 1964 advertisement at **509 Main** (`E-129`) and precedes the 1 September 1967 fire report naming Dixon’s Bakery (`E-045`).'),
 ('businesses/harding-drug-store.md','Mid-1960s P-4565 photograph',f'CCHS `{TARGET}` (`{SID}` / `{EID}` / `{MID}`) directly shows **HARDING DRUGS** signage in the pre-fire row. The catalog description transcribes “Harding (sp?) Drugs”; the 1 September 1967 fire article independently names Hardings Drug Store among the gutted businesses (`E-045`).'),
 ('buildings/503-main.md','Mid-1960s P-4565 facade view',f'CCHS `{TARGET}` (`{SID}` / `{EID}` / `{MID}`) supplies a street-level view of the 503/The Wheel frontage with wheel motifs immediately beside the directly numbered **TAVERN / 505** sign. The image also shows **5th ST / MAIN** street blades at the corner.'),
 ('buildings/505-main.md','Mid-1960s P-4565 facade view',f'CCHS `{TARGET}` (`{SID}` / `{EID}` / `{MID}`) directly shows the **TAVERN / 505** projecting sign and the 505 facade next to the catalog-identified Wheel frontage. This is visual corroboration of the 1965 505 Tavern documentary record, not evidence of ownership.'),
 ('buildings/507-harding-building.md','Mid-1960s P-4565 pre-fire storefront row',f'CCHS `{TARGET}` (`{SID}` / `{EID}` / `{MID}`) visually documents the neighboring pre-1967-fire row, including Coast to Coast Stores, Dixon’s Pastry Shop, Harding Drugs, Volunteers of America Thrift Store, and Seid’s/Restaurant. Only Dixon’s 509 address is independently exact in the current mid-1960s evidence; do not assign the other visible storefronts exact numbers from photograph order alone.'),
]:
    append_once(path,f'## {title}',f'## {title}\n\n{text}')

append_once('timelines/503-main.md',f'| Circa mid-1960s | CCHS {TARGET}',f'| Circa mid-1960s | CCHS `{TARGET}` photographs The Wheel/503 facade with wheel motifs beside the directly signed **TAVERN / 505** frontage; visible 5th/Main street blades. | Primary photograph + catalog; exact exposure date unresolved. | `{EID}`; `{SID}`; `{MID}` |')
append_once('timelines/505-main.md',f'| Circa mid-1960s | CCHS {TARGET}',f'| Circa mid-1960s | CCHS `{TARGET}` directly shows **TAVERN / 505** on the 505 frontage, visually corroborating the Nov. 1965 renewal. | Primary photograph; exact exposure date unresolved. | `{EID}`; `{SID}`; `{MID}` |')
append_once('timeline.md',f'## {TID} —',f'''## {TID} — {TIMELINE_NAME}\n\nCCHS `{TARGET}` (`{SID}` / `{EID}` / `{MID}`) shows the Main Street commercial row with the catalog-identified **The Wheel**, directly readable **TAVERN / 505**, Coast to Coast Stores, Dixon's Pastry Shop, Harding Drugs, Volunteers of America Thrift Store, and Seid's/Restaurant. The photograph directly shows **5th ST / MAIN** street blades; CCHS's supplied description instead says Main and McLoughlin Blvd., so the archive preserves the conflict. The image is strong visual context for the businesses independently documented immediately before the **1 September 1967** fire (`E-045`).''')

append_once('indexes/id-crosswalk.md',f'`{MID}` CCHS `{TARGET}`',f'| `{MID}` CCHS `{TARGET}` | `{SID}`, `{EID}`, `{TID}`, `BUS-004`, `BUS-005`, `BUS-007`, `BUS-023`, `{COAST}`, `{VOA}`, `{SEID}`, `B-001`, `B-002`, `B-003` | Circa-mid-1960s pre-fire Main Street business lineup; directly shows TAVERN/505 and multiple neighboring signs; visible 5th/Main blades conflict with catalog Main/McLoughlin wording. |')
append_once('registers/research-log.md',f'## 4 September 2026 — CCHS {TARGET}',f'''## 4 September 2026 — CCHS {TARGET} mid-1960s business-lineup photograph\n\n- Integrated `{MID}` / `{SID}` / `{EID}` from exact CCHS catalog object `{TARGET}`.\n- Direct visual review records **TAVERN / 505**, Coast to Coast Stores, Dixon's Pastry Shop, Harding Drugs, Volunteers of America Thrift Store, Seid's/Restaurant, and unresolved **Rain Check Room** wording; CCHS also identifies The Wheel.\n- Preserved location-wording conflict: photograph visibly shows **5th ST / MAIN** blades while supplied CCHS description says Main and McLoughlin Blvd.\n- Added new business records `{COAST}`, `{VOA}`, `{SEID}`; linked existing `BUS-004`, `BUS-005`, `BUS-007`, and `BUS-023`.\n- Photo supplies a visual pre-fire lineup that aligns with independently dated 1964–1967 records; exact exposure date remains unresolved within “circa mid-1960s.”''')
append_once('evidence/research-leads.md','Rain Check Room sign in CCHS P-4565',f'''### Rain Check Room sign in CCHS P-4565\n\nThe circa-mid-1960s photograph `{MID}` directly shows **RAIN CHECK Room / BREAKFAST / LUNCH & DINNERS** on the facade zone associated spatially with the Wheel/503 corner. Determine from directories, advertisements, liquor/restaurant licenses, or telephone books whether **Rain Check Room** was a room/trade style within The Wheel, a separate business, or an adjacent operation. Do not merge it into `BUS-004` without an independent name/address bridge. Related `{SID}` / `{EID}`.''')

# structured source/evidence/timeline append
sy=rd('database/sources.yml').rstrip()
sy += f'''\n\n  - id: {SID}\n    name: "{SOURCE_NAME}"\n    url: "{CAP}"\n    notes: "CCHS P-4565, circa mid-1960s. Directly readable business signs and visible 5th/Main street blades; catalog Main/McLoughlin wording preserved as conflict."\n    related_media: [{MID}]\n    related_evidence: [{EID}]'''
wr('database/sources.yml',sy+'\n')
ey=rd('database/evidence.yml').rstrip()
ey += f'''\n\n  - id: {EID}\n    name: "{EVIDENCE_NAME}"\n    classification: DOCUMENTED / DIRECT\n    claims:\n      - "CCHS P-4565 directly documents multiple circa-mid-1960s Main Street business signs, including TAVERN/505, Coast to Coast Stores, Dixon's Pastry Shop, Harding Drugs, Volunteers of America Thrift Store, and Seid's/Restaurant."\n      - "The photograph visibly shows 5th ST and MAIN street blades while the CCHS supplied description says Main and McLoughlin Blvd.; preserve both."\n      - "The image is strong pre-fire visual context for businesses independently named in 1964-1967 sources."\n    confidence: "Very High for visible lettering and P-4565 identity; High for broad circa-mid-1960s/pre-fire context; exact exposure date unresolved."\n    related_sources: [{SID}]\n    related_businesses: [BUS-004, BUS-005, BUS-007, BUS-023, {COAST}, {VOA}, {SEID}]\n    related_buildings: [B-001, B-002, B-003]\n    related_media: [{MID}]\n    repository_file: {CAP}'''
wr('database/evidence.yml',ey+'\n')
ty=rd('database/timeline.yml').rstrip()
ty += f'''\n\n  - id: {TID}\n    date: "circa mid-1960s"\n    title: "{TIMELINE_NAME}"\n    summary: "CCHS P-4565 visually documents the 503/505 frontage and neighboring Main Street businesses before the 1967 fire; exact exposure date unresolved."\n    confidence: "High for scene/business lineup; exact exposure date unresolved."\n    related_sources: [{SID}]\n    related_evidence: [{EID}]\n    related_businesses: [BUS-004, BUS-005, BUS-007, BUS-023, {COAST}, {VOA}, {SEID}]\n    related_buildings: [B-001, B-002, B-003]'''
wr('database/timeline.yml',ty+'\n')

print(f'Integrated {MID}/{SID}/{EID}/{TID}; new businesses {COAST},{VOA},{SEID}; image {IMAGE}')
