from pathlib import Path

source = Path('scripts/maintenance/integrate_1916_enterprise_mar10_mar17.py').read_text()
source = source.replace("block.strip()", "block.strip('\\n')")
exec(compile(source, 'integrate_1916_enterprise_mar10_mar17_fixed', 'exec'))
