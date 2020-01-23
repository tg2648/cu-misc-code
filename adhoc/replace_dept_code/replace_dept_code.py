"""
Replace 4-digit codes with names in a csv
"""

import os
import csv
import json
from pathlib import Path
from dotenv import load_dotenv

BASEDIR = Path(__file__).parent.resolve()
env_path = BASEDIR / '.env'
load_dotenv(dotenv_path=env_path)

with open(os.getenv('DEPT_NAMES_PATH')) as f:
    dept_names = json.load(f)

with open(os.getenv('INPUT_PATH'), 'r') as f_in:
    codes = [line.rstrip() for line in f_in]

names = []

for i, code in enumerate(codes):
    code_parts = code.split('/')
    name_parts = []
    if len(code_parts) == 1:
        name_parts.append(dept_names.get(code_parts[0]))
    else:
        name_parts = [dept_names.get(code_part) for code_part in code_parts]

    names.append(['; '.join(name_parts)])

with open(os.getenv('OUTPUT_PATH'), 'w', newline='') as f_out:
    writer = csv.writer(f_out)
    writer.writerows(names)
