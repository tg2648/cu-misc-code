# Standard Library
import os
from pathlib import Path

# Third-party
import pandas as pd
import numpy as np
from dotenv import load_dotenv

# Load environment variables
basedir = Path(__file__).parent.resolve()
env_path = basedir / '.env'
load_dotenv(dotenv_path=env_path)


df = pd.read_csv(os.getenv('DATA_PATH'), dtype=np.str, keep_default_na=False)
df = df.iloc[2:]  # Remove the first two rows (leave only Qualtrics question IDs)

SCHOOL_COLUMN = 'Q2'
df[SCHOOL_COLUMN] = df[SCHOOL_COLUMN].replace('', 'Did not indicate school')

# Filter
FILTER_COLUMN = 'Q116'
df = df[df[FILTER_COLUMN] != 'Yes']

qualtrics_columns = pd.read_excel(os.getenv('COLUMNS_PATH'), dtype=np.str)

if __name__ == "__main__":
    pass
