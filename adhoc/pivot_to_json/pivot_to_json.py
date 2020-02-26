"""
Converts

Col A | Col B
-------------
1     | Type A
2     | Type A

to

{'Type A' : ['1', '2']}
"""

import os
import json
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv

BASEDIR = Path(__file__).parent.resolve()
env_path = BASEDIR / '.env'
load_dotenv(dotenv_path=env_path)

df = pd.read_excel(os.getenv('FILE_PATH'))

pivot = {}
pivot_col = 'Short Type'
value_col = 'Column ID'

unique = df[pivot_col].unique()

for i in unique:
    pivot.setdefault(i, [])
    vals = []
    for val in df[df[pivot_col] == i][value_col]:
        vals.append(val)
    pivot[i] = vals

json_path = os.getenv('JSON_PATH')
with open(json_path, 'w') as f:
    json_data = json.dumps(pivot)
    f.write(json_data)

print(f'Created {json_path}')
