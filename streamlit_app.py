from pathlib import Path
import runpy

runpy.run_path(str(Path(__file__).parent / "frontend" / "app.py"))