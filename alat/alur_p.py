"""Pintu masuk kompatibel: seluruh regenerasi memakai konten edisi 3."""
import runpy
from pathlib import Path
def build():
 return runpy.run_path(str(Path(__file__).with_name("konten_interaktif.py")),run_name="__main__")
if __name__=="__main__":build()
