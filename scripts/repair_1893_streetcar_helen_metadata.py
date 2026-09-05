from pathlib import Path
import re

SOURCE_ID="S-218"
EVIDENCE_ID="E-198"
MEDIA_ID="IMG-0747"
CAPTURE="evidence/source-captures/1893-streetcar-helen-sixth-main-ee-williams-2026-09-04.md"

def read(p): return Path(p).read_text(encoding='utf-8')
def write(p,s): Path(p).write_text(s,encoding='utf-8')
def append_once(p,marker,block):
    s=read(p)
    if marker not in s: write(p,s.rstrip()+"\n\n"+block.rstrip()+"\n")

# Add validator-required fields to the Markdown evidence block generated in this working tree.
p="evidence/evidence-register.md"
s=read(p)
start=s.find(f"## {EVIDENCE_ID} —")
if start>=0:
    end=s.find("\n## E-",start+4)
    if end<0: end=len(s)
    block=s[start:end]
    if "\nType:" not in block:
        block=block.replace(f"Source: `S-218`\nMedia: `IMG-0747`\nClassification:",
            "Source: `S-218`\nMedia: `IMG-0747`\nType: Primary photographic evidence\nClaims:\n- The 1893 Sixth/Main Streetcar Helen photograph directly shows the storefront name E. E. WILLIAMS on the right/east side of Main.\n- A separate DRUGS sign is directly visible farther south on the same side.\n- The repeated E. E. Williams name in the independently reviewed 1895 Welcome Arch photograph provides a two-date business/signage anchor, but the exact later 501/503/505 bay remains unresolved.\nConfidence: Very High for the visible E. E. WILLIAMS and DRUGS transcriptions; Moderate/working-hypothesis for exact mapping to a later 501/503/505 bay.\nClassification:")
        s=s[:start]+block+s[end:]
        write(p,s)

append_once("database/sources.yml",f"  - id: {SOURCE_ID}\n",f'''  - id: {SOURCE_ID}
    name: 1893 Streetcar Helen at Sixth/Main photograph
    url: Internal repository photograph / {CAPTURE}
    notes: Historic photograph identified as the first streetcar Helen entering Oregon City at Sixth and Main in 1893. Direct visual review reads E. E. WILLIAMS on the east/right storefront and a separate DRUGS sign farther south. Steward original is preserved by filename, dimensions, bytes and SHA-256; exact later 501/503/505 bay assignment remains unresolved.
''')

append_once("database/evidence.yml",f"  - id: {EVIDENCE_ID}\n",f'''  - id: {EVIDENCE_ID}
    name: 1893 E. E. Williams storefront visible in Streetcar Helen photograph
    type: Primary photographic evidence
    claims:
      - The 1893 Sixth/Main Streetcar Helen photograph directly shows E. E. WILLIAMS on the right/east Main Street storefront.
      - A separate DRUGS sign is directly visible farther south on the same side.
      - The matching E. E. Williams name in the 1895 Welcome Arch photograph provides a two-date visual business/signage anchor, while the individual later 501/503/505 storefront assignment remains unresolved.
    confidence: Very High for visible sign transcription; Moderate / working hypothesis for exact later-address bay mapping.
    related_sources:
      - {SOURCE_ID}
    related_buildings:
      - B-005
      - B-001
      - B-002
''')
print("Repaired Helen source/evidence YAML and validator-required Markdown fields.")
