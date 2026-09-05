import json
import urllib.parse
import urllib.request

QUERIES = [
    "Oregon City 1960's - Street Scene - Corner of Main and McLoughlin Blvd",
    'Corner of Main and McLoughlin Blvd',
    'Oregon City Mobil Main McLoughlin',
    'L H Hagen Oregon City',
]


def get_json(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 Main-Street-Archive/1.0'})
    with urllib.request.urlopen(req, timeout=90) as r:
        return json.load(r)


def walk(obj, out):
    if isinstance(obj, dict):
        props = obj.get('properties')
        if isinstance(props, dict) and obj.get('id'):
            text = json.dumps(props, ensure_ascii=False)
            if any(k.lower() in text.lower() for k in ['oregon city', 'mcloughlin', 'mobil', 'hagen']):
                out[obj['id']] = obj
        for v in obj.values():
            walk(v, out)
    elif isinstance(obj, list):
        for v in obj:
            walk(v, out)


def prop_text(entry, key):
    try:
        return entry['properties'][key].get('value_text')
    except Exception:
        return None


all_entries = {}
for q in QUERIES:
    url = 'https://api.catalogit.app/api/public/search?' + urllib.parse.urlencode({'query': q, 'size': 100})
    data = get_json(url)
    found = {}
    walk(data, found)
    print('\nQUERY:', q)
    print('URL:', url)
    print('candidate_count:', len(found))
    all_entries.update(found)

for entry_id, entry in all_entries.items():
    print('\n=== CANDIDATE ===')
    print('id:', entry_id)
    print('slug:', entry.get('slug'))
    print('catalog:', prop_text(entry, 'hasCatalogNumber'))
    print('name:', prop_text(entry, 'hasName'))
    print('description:', prop_text(entry, 'hasDescription'))
    print('date:', prop_text(entry, 'hasDate'))
    print('properties:', json.dumps(entry.get('properties', {}), ensure_ascii=False, sort_keys=True))
