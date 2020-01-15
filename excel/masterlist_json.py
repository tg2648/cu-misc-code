"""
Imports various JSON files for the FacultyMasterlistHandler
"""

import json
import os
from pathlib import Path
from dotenv import load_dotenv

BASEDIR = Path(__file__).parent.resolve()
env_path = BASEDIR / '.env'
load_dotenv(dotenv_path=env_path)

with open(os.getenv('INPUT_COLUMN_MAPPING_PATH')) as f:
    INPUT_COLUMN_MAPPING = json.load(f)

with open(os.getenv('OUTPUT_COLUMN_MAPPING_PATH')) as f:
    OUTPUT_COLUMN_MAPPING = json.load(f)

with open(os.getenv('RANK_CORRECTIONS_PATH')) as f:
    RANK_CORRECTIONS = json.load(f)

with open(os.getenv('TENURE_STATUS_CORRECTIONS_PATH')) as f:
    TENURE_STATUS_CORRECTIONS = json.load(f)

with open(os.getenv('DEPT_CODE_CORRECTIONS_PATH')) as f:
    DEPT_CODE_CORRECTIONS = json.load(f)

with open(os.getenv('DEPT_CODE_PATH')) as f:
    DEPT_CODE = json.load(f)
