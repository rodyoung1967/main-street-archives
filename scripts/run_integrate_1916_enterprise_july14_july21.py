from pathlib import Path

path = Path('scripts/integrate_1916_enterprise_july14_july21.py')
s = path.read_text()
s = s.replace(
    "('Combined certified newspaper coverage: **683/884**', 'Combined certified newspaper coverage: **699/884**'),",
    "('- Combined: **683/884 certified**', '- Combined: **699/884 certified**'),"
)
s = s.replace(
    "('**201 Enterprise pages remain uncertified**', '**185 Enterprise pages remain uncertified**'),",
    "('- Enterprise pages remaining uncertified: **201**', '- Enterprise pages remaining uncertified: **185**'),"
)
s = s.replace(
    "('next ordinary unreviewed issue is **14 July 1916**', 'next ordinary unreviewed issue is **28 July 1916**'),",
    "('The next ordinary unreviewed Enterprise issue is **14 July 1916**', 'The next ordinary unreviewed Enterprise issue is **28 July 1916**'),"
)
exec(compile(s, str(path), 'exec'))
