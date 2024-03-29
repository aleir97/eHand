

from pathlib import Path
from datetime import datetime

date = datetime.today().strftime('%d-%Y-%m')

# Definition of important Paths
ehand_path = Path('..')
py_path  = Path('.')

measure_dir = ehand_path / "emg_data" / date
blender_dir = py_path  / "3D"
models_dir  = py_path  / "models"