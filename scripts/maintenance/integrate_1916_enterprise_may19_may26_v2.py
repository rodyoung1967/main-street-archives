import runpy

# The base integration script now emits validator-compliant Markdown and YAML.
# Keep this wrapper so the newer workflow path remains intact.
runpy.run_path('scripts/maintenance/integrate_1916_enterprise_may19_may26.py', run_name='__main__')
